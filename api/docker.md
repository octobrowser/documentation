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

## Golden Image (Pre-Authenticated Snapshot)

The basic recipe above authenticates with email/password on every container start and re-downloads ~1.8–2.2 GB of browser components (`Octium`, `Tentacle`, `Profile_Parser`, `Tentacle_Ssh`, `userdata`) unless the cache is persisted. Octo offers two ways to avoid that:

- **Method 1 — components folder on the host.** Suitable when you have a static host that builds and runs the containers. Mount the components directory into every container:

  ```bash
  -v '/srv/docker_octo/cache:/home/octo/.Octo Browser/' \
  ```

  or in `docker-compose.yaml`:

  ```yaml
  volumes:
    - /srv/docker_octo/cache:/home/octo/.Octo Browser/
  ```

- **Method 2 — snapshot baked into the image.** Suitable when there is no static host: the image can be shipped to any number of machines and containers start with components already in place. Authentication is done by passing an API token via the `OCTO_API_TOKEN` environment variable. The rest of this section covers this method.

Caveat for either method: you may hit operational limits if you run more than 5 containers simultaneously **and** they all share the same IP address **and** log into the same Octo account.

### Requirements

- Docker, Bash, and `jq` on the build machine (Git Bash or WSL2 on Windows).
- An Octo Browser API token.
- About 6 GB of free disk space: `octo:base` ~2.3 GB, `octo:ready` ~4.9 GB (layers shared with the base image are not duplicated), snapshot ~700 MB.
- 15–40 minutes for the first full build depending on network speed — most of it is package installation in the base image and downloading ~1.8–2.2 GB of components.

Place all five files below in one folder and run the build from that folder.

### Step 1: `creds.json`

```json
{"octo_api_token":"your_token_here"}
```

Replace `your_token_here` with your API token.

### Step 2: `dockerfile` — base image

Same as the basic Dockerfile, but sets `HOME`, `APPIMAGE_EXTRACT_AND_RUN=1` and `OCTO_DATA` in `ENV`, adds `jq x11vnc libgl1 libglib2.0-0 zip`, and ends with `CMD ["/bin/bash"]` instead of launching the browser — the entrypoint is added later in `dockerfile.final`.

```dockerfile
FROM ubuntu:22.04
ARG TZ=America/Los_Angeles
ARG DEBIAN_FRONTEND=noninteractive
ENV LANG="C.UTF-8" HOME=/home/octo \
    APPIMAGE_EXTRACT_AND_RUN=1 \
    OCTO_DATA="/home/octo/.Octo Browser"
RUN apt-get update && apt-get install -y \
    apt-transport-https ca-certificates curl gnupg unzip jq \
    libgles2 libegl1 xvfb x11vnc --no-install-recommends \
 && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
 && echo "deb https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
 && apt-get update && apt-get install -y \
    fontconfig fonts-ipafont-gothic fonts-kacst fonts-noto fonts-symbola \
    fonts-thai-tlwg fonts-wqy-zenhei fonts-freefont-ttf \
    connect-proxy dnsutils iproute2 iptables iputils-ping net-tools \
    openvpn procps socat ssh sshpass sudo tcpdump telnet traceroute \
    tzdata vim-nox libgl1 libglib2.0-0 zip \
 && rm -rf /var/lib/apt/lists/*
RUN curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /tmp/chrome.deb \
 && apt-get update && apt-get install -y /tmp/chrome.deb && rm -f /tmp/chrome.deb \
 && rm -rf /var/lib/apt/lists/*
RUN groupadd -r octo \
 && useradd -r -g octo -s /bin/bash -m -G audio,video,sudo \
        -p "$(echo 1 | openssl passwd -1 -stdin)" octo \
 && mkdir -p /home/octo/browser && chown -R octo:octo /home/octo \
 && mkdir -p /etc/sudoers.d \
 && echo 'octo ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/octo && chmod 0440 /etc/sudoers.d/octo
USER octo
RUN curl -o /home/octo/browser/octo-browser.tar.gz \
        https://binaries.octobrowser.net/releases/installer/OctoBrowser.linux.tar.gz \
 && tar -xzf /home/octo/browser/octo-browser.tar.gz -C /home/octo/browser \
 && rm -f /home/octo/browser/octo-browser.tar.gz
CMD ["/bin/bash"]
```

Build the base image:

```bash
docker build -t octo:base -f dockerfile .
```

### Step 3: `entrypoint.sh` — launching the browser in the container

Starts a virtual display and Octo Browser in headless mode on every container start. The browser is kept as a direct child so signals reach it and the container lives exactly as long as the browser does.

```bash
#!/usr/bin/env bash
# entrypoint.sh — boot headless OctoBrowser inside octo:ready.
set -u
export DISPLAY=:1
OCTO_DATA="${OCTO_DATA:-/home/octo/.Octo Browser}"
rm -f /tmp/.X1-lock "$OCTO_DATA/local_port"
rm -rf /tmp/.X11-unix
Xvfb :1 -ac -screen 0 1920x1080x24 >/tmp/x.log 2>&1 &
for _ in $(seq 1 10); do
    sleep 1
    [ -S /tmp/.X11-unix/X1 ] && break
done
# Keep OctoBrowser as our own child so signals reach it and the container
# lives exactly as long as the browser does.
OCTO_HEADLESS=1 /home/octo/browser/OctoBrowser.AppImage >/tmp/octo.log 2>&1 &
OCTO_PID=$!
term() { kill -TERM "$OCTO_PID" 2>/dev/null || true; }
trap term TERM INT
wait "$OCTO_PID"
```

### Step 4: `dockerfile.final` — image with the snapshot

```dockerfile
# dockerfile.final — build octo:ready from octo:base + the golden snapshot.
# Build: docker build -t octo:ready -f ./dockerfile.final .
FROM octo:base
# --chown so the unprivileged Octo user can extract the snapshot and own the result.
COPY --chown=octo:octo logged-in-state.tar.gz /tmp/logged-in-state.tar.gz
USER octo
RUN mkdir -p "$OCTO_DATA" \
 && tar -xzf /tmp/logged-in-state.tar.gz -C "$OCTO_DATA" \
 && rm -f /tmp/logged-in-state.tar.gz
COPY --chown=octo:octo entrypoint.sh /home/octo/entrypoint.sh
RUN chmod +x /home/octo/entrypoint.sh
ENTRYPOINT ["/home/octo/entrypoint.sh"]
```

You do not build this manually — `build-golden.sh` does it.

### Step 5: `build-golden.sh` — creating the snapshot

Copy the script verbatim. What it does, in order:

1. Reads the token from `creds.json`, starts an `octo-golden` container from `octo:base` with `OCTO_API_TOKEN` set, launches `Xvfb` + `OctoBrowser.AppImage` with `OCTO_HEADLESS=1`.
2. Waits up to 90 s for the client to write its port to `~/.Octo Browser/local_port`.
3. Verifies authentication via `GET /api/username` on that port (restarts the app every 4th failed attempt).
4. Waits up to 20 min for components under `~/.Octo Browser/bin` — `Octium`, `Tentacle`, `Profile_Parser`, `Tentacle_Ssh`, `userdata` — to appear and their size to stabilise. `Ui` is the GUI frontend and is not downloaded in headless mode.
5. Warms up the component cache by starting a one-time profile (`POST /api/profiles/one_time/start`, `headless: true`, flags `--no-sandbox --disable-dev-shm-usage`), waits for `~/.Octo Browser/tmp/components` to stabilise, then stops it.
6. Tars `~/.Octo Browser` into `logged-in-state.tar.gz`, excluding `bcache`, `logs`, `local_port`, `localpersist.data` and `updates`. `localpersist.data` holds the machine HID — baking it in would make every container look like the same machine, and a second container would steal the first one's session.
7. Builds `octo:ready` from `dockerfile.final`, starts a throw-away `octo-check` container and confirms `GET /api/username` returns a username; on failure it dumps `docker logs`, `/tmp/octo.log` and `/tmp/x.log`.

```bash
#!/usr/bin/env bash
# build-golden.sh — capture a golden snapshot and build octo:ready.
# Requires: octo:base already built, creds.json with an API token, docker, jq.
# Run: bash build-golden.sh
set -euo pipefail
cd "$(dirname "$0")"
step()    { printf '\n\033[36m=== %s ===\033[0m\n' "$1"; }
err()     { printf '\033[31m%s\033[0m\n' "$*" >&2; }
ok()      { printf '\033[32m%s\033[0m\n' "$*"; }
warn()    { printf '\033[33m%s\033[0m\n' "$*"; }
filesize(){ stat -c%s "$1" 2>/dev/null || stat -f%z "$1" 2>/dev/null || echo 0; }
TOKEN=$(jq -r '.octo_api_token // empty' creds.json 2>/dev/null || true)
if [ -z "$TOKEN" ] || printf '%s' "$TOKEN" | grep -qE '^(PASTE|<|TOKEN)'; then
    err 'creds.json does not contain octo_api_token. Format: {"octo_api_token":"..."}'
    exit 1
fi
printf 'Token: %s... (length %d)\n' "${TOKEN:0:8}" "${#TOKEN}"
step "Starting golden container"
docker rm -f octo-golden 2>/dev/null || true
docker run -d --name octo-golden --security-opt seccomp:unconfined \
    -e "OCTO_API_TOKEN=$TOKEN" \
    --entrypoint bash octo:base -lc "sleep 3600"
step "Start Xvfb + OctoBrowser (auth via OCTO_API_TOKEN)"
docker exec octo-golden bash -lc '
  rm -f /tmp/.X1-lock "$HOME/.Octo Browser/local_port"; rm -rf /tmp/.X11-unix
  setsid bash -c "Xvfb :1 -ac -screen 0 1920x1080x24 >/tmp/x.log 2>&1" &
  for i in $(seq 1 10); do sleep 1; [ -S /tmp/.X11-unix/X1 ] && break; done
  DISPLAY=:1 setsid bash -c "OCTO_HEADLESS=1 /home/octo/browser/OctoBrowser.AppImage >/tmp/octo.log 2>&1" &
'
step "Waiting for local_port to appear (up to 90 sec)"
PORT=""
for i in $(seq 1 18); do
    sleep 5
    PORT=$(docker exec octo-golden bash -lc 'cat "$HOME/.Octo Browser/local_port" 2>/dev/null' 2>/dev/null || true)
    if [ -n "$PORT" ]; then printf '  port: %s\n' "$PORT"; break; fi
    printf '  ...not yet (%ds)\n' "$((i*5))"
done
if [ -z "$PORT" ]; then
    err "OctoBrowser did not come up. docker exec octo-golden cat /tmp/octo.log"
    exit 1
fi
step "Checking authorization (OCTO_API_TOKEN)"
AUTHED=false
for i in $(seq 1 12); do
    RESP=$(docker exec octo-golden bash -lc '
      P=$(cat "$HOME/.Octo Browser/local_port" 2>/dev/null)
      [ -n "$P" ] && curl -s http://127.0.0.1:$P/api/username 2>/dev/null
    ' 2>/dev/null || true)
    printf '  [attempt %d] %s\n' "$i" "$RESP"
    if printf '%s' "$RESP" | grep -q '"username"'; then AUTHED=true; break; fi
    if [ $((i % 4)) -eq 0 ] && [ "$i" -lt 12 ]; then
        warn "  restarting the application..."
        docker exec octo-golden bash -lc '
          pkill -f OctoBrowser.AppImage; sleep 3
          rm -f "$HOME/.Octo Browser/local_port"
          DISPLAY=:1 setsid bash -c "OCTO_HEADLESS=1 /home/octo/browser/OctoBrowser.AppImage >>/tmp/octo.log 2>&1" &
        ' >/dev/null 2>&1 || true
        sleep 20
    fi
    sleep 5
done
if [ "$AUTHED" != "true" ]; then
    err "Authorization not confirmed. Check the token / docker exec octo-golden cat /tmp/octo.log"
    exit 1
fi
step "Waiting for components to download (up to 20 min)"
docker exec octo-golden bash -lc '
  B="$HOME/.Octo Browser/bin"
  stable=0; prev=0
  for i in $(seq 1 120); do
    cur=$(du -sm "$B" 2>/dev/null | cut -f1); cur=${cur:-0}
    missing=""
    # Ui is the GUI frontend and is not downloaded in headless mode.
    for c in Octium Tentacle Profile_Parser Tentacle_Ssh userdata; do
      sz=$(du -sm "$B/$c" 2>/dev/null | cut -f1); sz=${sz:-0}
      [ "$sz" -ge 10 ] || missing="$missing $c"
    done
    if [ -z "$missing" ] && [ "$cur" = "$prev" ]; then stable=$((stable+1)); else stable=0; fi
    [ "$stable" -ge 6 ] && { echo "stable ${cur}MB, all components present"; break; }
    prev=$cur; sleep 10
  done
  [ -n "$missing" ] && echo "WARNING: did not wait for:$missing"
  du -sm "$B"/* 2>/dev/null | sort -rn
'
step "Starting profile (warm-up + component-cache stabilization)"
docker exec octo-golden bash -lc '
  COMP="$HOME/.Octo Browser/tmp/components"
  P=$(cat "$HOME/.Octo Browser/local_port")
  RESP=$(curl -s -X POST http://127.0.0.1:$P/api/profiles/one_time/start \
    -H "Content-Type: application/json" \
    -d "{\"profile_data\":{\"fingerprint\":{\"os\":\"win\"}},\"headless\":true,\"timeout\":120,\"flags\":[\"--no-sandbox\",\"--disable-dev-shm-usage\"]}")
  UUID=$(echo "$RESP" | jq -r ".uuid // empty")
  echo "UUID=$UUID resp=$RESP"
  stable=0; prev=-1
  for i in $(seq 1 60); do
    cur=$(du -sm "$COMP" 2>/dev/null | cut -f1); cur=${cur:-0}
    if [ "$cur" = "$prev" ] && [ "$cur" -gt 0 ]; then stable=$((stable+1)); else stable=0; fi
    echo "  components: ${cur}MB (stable=$stable)"
    [ "$stable" -ge 3 ] && { echo "stable ${cur}MB"; break; }
    prev=$cur; sleep 5
  done
  [ "${cur:-0}" -eq 0 ] && echo "WARN: component cache stayed empty (non-fatal)"
  [ -n "$UUID" ] && curl -s -X POST http://127.0.0.1:$P/api/profiles/stop \
    -H "Content-Type: application/json" -d "{\"uuid\":\"$UUID\"}" >/dev/null \
    && echo "profile stopped" || echo "WARN: stop failed (non-fatal)"
'
step "Capturing snapshot logged-in-state.tar.gz"
docker exec octo-golden bash -lc '
  sleep 2
  cd "$HOME/.Octo Browser"
  # localpersist.data holds the machine HID: baking it in makes every container
  # look like the same machine, and a second container steals the first session.
  # The --warning/--ignore-failed-read flags keep the still-running daemon from
  # turning a changed file into a fatal tar error.
  tar --warning=no-file-changed --warning=no-file-removed --ignore-failed-read \
      --exclude=bcache --exclude=logs --exclude=local_port --exclude=localpersist.data \
      --exclude=updates \
      -czf /tmp/logged-in-state.tar.gz . || [ "$?" -eq 1 ]
'
docker cp octo-golden:/tmp/logged-in-state.tar.gz ./logged-in-state.tar.gz
docker rm -f octo-golden
SZ=$(filesize logged-in-state.tar.gz)
printf 'Snapshot: %d MB\n' "$((SZ / 1024 / 1024))"
step "Building octo:ready"
docker build -t octo:ready -f ./dockerfile.final .
step "Checking octo:ready"
docker rm -f octo-check 2>/dev/null || true
docker run -d --init --name octo-check --security-opt seccomp:unconfined \
    -e "OCTO_API_TOKEN=$TOKEN" octo:ready
OK=false
DEAD=false
for i in $(seq 1 18); do
    sleep 5
    if [ "$(docker inspect -f '{{.State.Running}}' octo-check 2>/dev/null || true)" != "true" ]; then
        DEAD=true; break
    fi
    RESP=$(docker exec octo-check bash -lc '
      P=$(cat "$HOME/.Octo Browser/local_port" 2>/dev/null)
      [ -n "$P" ] && curl -s http://127.0.0.1:$P/api/username 2>/dev/null
    ' 2>/dev/null || true)
    if printf '%s' "$RESP" | grep -q '"username"'; then
        ok "  OK: $RESP"; OK=true; break
    fi
    printf '  ...%ds: %s\n' "$((i*5))" "$RESP"
done
if [ "$OK" != "true" ]; then
    # Collect the logs before removing the container, or the evidence is gone.
    err "Check failed."
    if [ "$DEAD" = "true" ]; then
        CODE=$(docker inspect -f '{{.State.ExitCode}}' octo-check 2>/dev/null || true)
        err "  container is not running (exit code: ${CODE:-unknown})"
    fi
    printf '\n[docker logs octo-check]\n'
    docker logs octo-check 2>&1 | tail -n 40 || true
    printf '\n[/tmp/octo.log]\n'
    docker exec octo-check bash -lc 'tail -n 40 /tmp/octo.log' 2>&1 \
        || echo "(unavailable — container not running)"
    printf '\n[/tmp/x.log]\n'
    docker exec octo-check bash -lc 'tail -n 20 /tmp/x.log' 2>&1 \
        || echo "(unavailable — container not running)"
fi
docker rm -f octo-check >/dev/null
if [ "$OK" = "true" ]; then
    ok "DONE: octo:ready built, authorization works."
else
    exit 1
fi
```

Run it:

```bash
bash build-golden.sh
```

A successful run ends with:

```text
=== Checking octo:ready ===
OK: {"username":"your@email"}
DONE: octo:ready built, authorization works.
```

### Step 6: Running the Finished Image

```bash
docker run -d --init --name octo-1 --security-opt seccomp:unconfined \
    -e "OCTO_API_TOKEN=your_token_here" octo:ready
```

- `-e OCTO_API_TOKEN` is required for authentication — the client reads it at startup and signs in without `/api/auth/login`.
- `--security-opt seccomp:unconfined` is required for Chrome's sandbox.
- Add `-p 127.0.0.1:<host_port>:58888` if you need to reach the local API from the host; the upstream command omits it, so `octo-1` as shown is only controllable from inside the container (or from other containers on the same Docker network).

### Updating the Snapshot

The snapshot also pins component versions, so it goes stale over time. To rebuild it, delete `logged-in-state.tar.gz` and run `bash build-golden.sh` again. If the browser itself must be updated, rebuild the base image without cache first:

```bash
docker build --no-cache -t octo:base -f dockerfile .
```

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
- **Prefer `OCTO_API_TOKEN` over email/password in containers** — the client honours it at startup and signs in headlessly, so no `/api/auth/login` call is needed (see [Golden Image](#golden-image-pre-authenticated-snapshot)).
- **Discover the local port from `~/.Octo Browser/local_port`** — the client writes its listening port there once it is up; poll that file instead of sleeping a fixed time.
- **Pass `--no-sandbox --disable-dev-shm-usage`** in `flags` when starting profiles inside a container; these are the recommended in-container Chromium flags.
