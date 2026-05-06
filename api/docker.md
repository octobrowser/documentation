# Docker & Kubernetes

Octo Browser does not ship a public registry image — you build a container yourself by downloading the Linux release inside a Dockerfile. The recipes below come straight from the official Postman documentation and run the desktop app inside a virtual X server (`Xvfb`) so its local API on port `58888` is reachable from the host.

## Dockerfile

Builds an Ubuntu 22.04 image, installs Chrome, Octo dependencies, the Octo Browser AppImage, and starts everything under `Xvfb` in headless mode.

```dockerfile
FROM ubuntu:22.04
ARG TZ=America/Los_Angeles
ARG DEBIAN_FRONTEND=noninteractive
ENV LANG="C.UTF-8"

RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    unzip \
    libgles2 libegl1 xvfb \
    --no-install-recommends \
 && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
 && echo "deb https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
 && apt-get update && apt-get install -y \
    fontconfig \
    fonts-ipafont-gothic \
    fonts-kacst \
    fonts-noto \
    fonts-symbola \
    fonts-thai-tlwg \
    fonts-wqy-zenhei \
    connect-proxy \
    dnsutils \
    fonts-freefont-ttf \
    iproute2 \
    iptables \
    iputils-ping \
    net-tools \
    openvpn \
    procps \
    socat \
    ssh \
    sshpass \
    sudo \
    tcpdump \
    telnet \
    traceroute \
    tzdata \
    vim-nox

RUN curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb --output /tmp/chrome.deb
RUN apt install -y /tmp/chrome.deb

# Octo dependencies
RUN apt update && apt install -y libgl1 libglib2.0-0 xvfb zip

RUN mkdir -p /home/octo/browser

# Create the unprivileged "octo" user
RUN groupadd -r octo \
 && useradd -r -g octo -s /bin/bash -m -G audio,video,sudo -p $(echo 1 | openssl passwd -1 -stdin) octo \
 && mkdir -p /home/octo/ \
 && chown -R octo:octo /home/octo

RUN mkdir -p /etc/sudoers.d \
 && echo 'octo ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/octo \
 && chmod 0440 /etc/sudoers.d/octo
RUN usermod -a -G sudo octo
USER octo

# Install Octo Browser
RUN curl -o /home/octo/browser/octo-browser.tar.gz https://binaries.octobrowser.net/releases/installer/OctoBrowser.linux.tar.gz
RUN tar -xzf /home/octo/browser/octo-browser.tar.gz -C /home/octo/browser

# Start Xvfb and Octo Browser in headless mode
CMD Xvfb :1 -ac -screen 0 "1920x1080x24" -nolisten tcp +extension GLX +render -noreset & \
    sudo chown -R octo:octo /home/octo && \
    sleep 5 && DISPLAY=:1 OCTO_HEADLESS=1 /home/octo/browser/OctoBrowser.AppImage
```

## run.sh

Build the image, run the container with the local API mapped to host port `58895`, then sign in and start a profile via the local API.

```bash
export EMAIL=your_email
export PASSWORD=your_password
export PROFILE_UUID=PUT_UUID_HERE

docker build -t octobrowser:latest .
docker run --name octo -it --rm \
       --security-opt seccomp:unconfined \
       -v '/srv/docker_octo/cache:/home/octo/.Octo Browser/' \
       -p 58895:58888 \
       octobrowser:latest

# Drive the container's local API (xh: https://github.com/ducaale/xh/releases)
xh POST localhost:58895/api/auth/login email=${EMAIL} password=${PASSWORD}
xh POST localhost:58895/api/profiles/start uuid=${PROFILE_UUID} headless:=true debug_port:=true
```

The volume mount under `/home/octo/.Octo Browser/` persists profile cache between runs.

After `start`, the response contains `ws_endpoint` and `debug_port`. Connect your automation library (Puppeteer, Playwright, Selenium) to those exactly as in [automation.md](automation.md).

## Kubernetes

Running the same image in a Kubernetes pod requires extra capabilities and shared-memory tuning, otherwise Chromium will crash:

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: cloud-instance
          image: {{ .Values.octoImage }}:{{ .Values.tag }}
          securityContext:
            capabilities:
              add:
                - NET_ADMIN
                - SYS_ADMIN
          volumeMounts:
            - name: dshm
              mountPath: /dev/shm
      volumes:
        - name: default-data
          emptyDir:
            medium: Memory
            sizeLimit: 1Gi
        - name: dshm
          emptyDir:
            medium: Memory
            sizeLimit: 4Gi
```

Key points:

- `NET_ADMIN` is required for proxy and DNS configuration.
- `SYS_ADMIN` is required by Chromium's sandbox (alternative: launch Chromium with `--no-sandbox`, but this weakens isolation).
- `/dev/shm` defaults to 64 MB in Kubernetes, which is too small for Chromium — mount an in-memory volume of at least 1–4 GB.

## Best Practices

- **Persist the profile cache** with a volume mount on `/home/octo/.Octo Browser/` so re-runs do not re-download fingerprint data.
- **Bind the local API to the host loopback** (`-p 127.0.0.1:58895:58888`) — the local API has no auth.
- **Use `OCTO_HEADLESS=1`** as in the Dockerfile; combined with `Xvfb` this is the supported headless mode.
- **One container per parallel session** — the local API on `:58888` controls a single desktop app instance.
