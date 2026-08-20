# Local Client API

The Local Client API runs inside the Octo Browser desktop app on `http://localhost:58888`. It does not require an `X-Octo-Api-Token` header — authentication is implicit via the running session of the desktop app.

Each path below is rooted at `http://localhost:58888`. Responses are bare JSON objects and do **not** use the `{success, msg, data}` envelope of the cloud API.

Although the local API is unauthenticated, profile start/stop/password operations are charged against the team's cloud RPM/RPH budget — see the point-cost table in [rate-limiting.md](rate-limiting.md).

## Prerequisites

- Octo Browser desktop app installed and running.
- The user is signed in (use [Login](#login), or the `OCTO_API_TOKEN` environment variable described below, if you are scripting cold-start automation).
- The local API server listens on `127.0.0.1:58888` only — no remote access.

## Error Responses

The local client uses two error shapes:

- **Business errors** — `400` (or another 4xx/5xx noted per endpoint) with a string `code`, a human-readable `error`, and a legacy numeric `error_code`:

  ```json
  { "code": "profiles.not_found", "error": "Profile not found", "error_code": 6 }
  ```

  `error_code` is deprecated; for start errors it maps to the numeric table in [Start Error Codes](#start-error-codes). Prefer the string `code`.

- **Validation errors** — `422` with a `detail` array describing the offending field:

  ```json
  { "detail": [{ "loc": ["body", "uuid"], "msg": "field required", "type": "value_error.missing" }] }
  ```

Unknown body fields are silently ignored.

## Client Setup

### Silent Installation

```powershell
& '.\Octo_Browser_latest_win.exe' /qn
```

```bash
# macOS
hdiutil attach ./Octo_Browser_latest_mac_arm64.dmg
cp -R /Volumes/Octo\ Browser/Octo\ Browser.app /Applications
hdiutil unmount /Volumes/Octo\ Browser
```

### Signing In With an API Token

The desktop client reads the `OCTO_API_TOKEN` environment variable at startup and logs in automatically, so no interactive login (or [Login](#login) call) is needed.

```powershell
$env:OCTO_API_TOKEN = "YOUR_API_TOKEN"; start 'C:\Program Files\Octo Browser\Octo Browser.exe'
```

```bash
# macOS
OCTO_API_TOKEN="YOUR_API_TOKEN" open -a "Octo Browser"

# Linux (from the folder containing the AppImage)
OCTO_API_TOKEN=YOUR_API_TOKEN ./OctoBrowser.AppImage
```

### Running the Client Headless

Set `OCTO_HEADLESS=1` to start the desktop client itself without a window (for servers and containers — see [docker.md](docker.md) for a complete Docker setup). This is independent of the per-profile `headless` flag below.

```powershell
$env:OCTO_HEADLESS = "1"; start 'C:\Program Files\Octo Browser\Octo Browser.exe'
```

```bash
# macOS
OCTO_HEADLESS=1 open -a "Octo Browser"

# Linux (from the folder containing the AppImage)
OCTO_HEADLESS=1 ./OctoBrowser.AppImage
```

## Profile Control

### List Active Profiles

Show the profiles currently launched on the device. `ws_endpoint` is populated only for profiles started in headless mode.

**Endpoint**: `GET http://localhost:58888/api/profiles/active`

```bash
curl -X GET http://localhost:58888/api/profiles/active
```

#### Example Response

```json
[
  {
    "uuid": "2bbfd1dbaf3349cf979787f15a9e413d",
    "state": "STARTED",
    "headless": true,
    "start_time": 1724173918,
    "ws_endpoint": "ws://127.0.0.1:55834/devtools/browser/a26c9612-6479-43f1-87ef-34590321a99a",
    "debug_port": "55834",
    "one_time": false,
    "browser_pid": 26616
  }
]
```

### Start Profile

**Endpoint**: `POST http://localhost:58888/api/profiles/start`

**Request Body**:
- `uuid` (string, required) — profile UUID.
- `headless` (bool, optional, default `false`).
- `debug_port` (bool | int, optional, default `false`) — `true` allocates a random free port; an integer `1024–65534` pins a specific port.
- `only_local` (bool, optional, default `true`) — bind the debug port to `127.0.0.1` only.
- `flags` (string[], optional, default `[]`) — extra Chromium switches. **Use sparingly.** Recommended values include `--disk-cache-dir=<path>` to keep cache between sessions (by default the cache is cleared every time the profile closes; the path must be outside the profile folder, e.g. `["--disk-cache-dir=C:/Cache"]`) and `--disable-backgrounding-occluded-windows` for parallel automation. Use `--remote-debugging-address=0.0.0.0` to expose the debug port to the LAN.
- `timeout` (int, optional, seconds, default `60`) — overrides the default start timeout; raise it for slow proxies.
- `password` (string, optional) — profile password if one is set.
- `profile_data` (object, optional) — overrides for selected profile fields, e.g. `{"images_load_limit": null}` (size in bytes).

```bash
curl -X POST http://localhost:58888/api/profiles/start \
  -H "Content-Type: application/json" \
  -d '{
    "uuid": "2bbfd1dbaf3349cf979787f15a9e413d",
    "headless": false,
    "debug_port": true,
    "only_local": true,
    "flags": [],
    "timeout": 120
  }'
```

#### Example Response

```json
{
  "uuid": "2bbfd1dbaf3349cf979787f15a9e413d",
  "state": "STARTED",
  "headless": true,
  "start_time": 1724172886,
  "ws_endpoint": "ws://127.0.0.1:54739/devtools/browser/4d05ab38-20bf-45e6-b463-6bc643028107",
  "debug_port": "54739",
  "one_time": false,
  "browser_pid": 10108,
  "connection_data": { "ip": "188.188.188.88", "country": "Germany" }
}
```

#### Error Responses

```json
{ "code": "profiles.not_found", "error": "Profile not found", "error_code": 6 }
```

```json
{ "code": "profiles.already_started", "error": "Profile is already started", "error_code": 2 }
```

```json
{ "code": "profiles.proxy_error", "error": "Failed to get proxy data", "error_code": 4 }
```

A missing `uuid` returns `422` with a `detail` array (see [Error Responses](#error-responses)).

#### Start Error Codes

Legacy numeric `error_code` values:

```text
1  ComponentNotFoundException
2  ProfileAlreadyRunningException
3  ProfileStartFailedException
4  GetProxyDataFailedException
5  InvalidProxyDataException
6  ProfileNotFoundException
7  NoSubscriptionException
8  OutdatedVersionException
9  ProfileVersionConsistencyError
```

### Stop Profile

**Endpoint**: `POST http://localhost:58888/api/profiles/stop`

**Request Body**:
- `uuid` (string, required)

```bash
curl -X POST http://localhost:58888/api/profiles/stop \
  -H "Content-Type: application/json" \
  -d '{"uuid":"2bbfd1dbaf3349cf979787f15a9e413d"}'
```

#### Example Response

```json
{ "msg": "Profile stopped" }
```

### Force Stop Profile

Forcibly terminate a profile. Requires Octo Browser **1.7 or later**.

**Endpoint**: `POST http://localhost:58888/api/profiles/force_stop`

**Request Body**:
- `uuid` (string, required)

```bash
curl -X POST http://localhost:58888/api/profiles/force_stop \
  -H "Content-Type: application/json" \
  -d '{"uuid":"2bbfd1dbaf3349cf979787f15a9e413d"}'
```

#### Example Response

```json
{ "msg": "Profile stopped successfully" }
```

### Start a One-Time Profile

Spin up a temporary profile that is not saved to the account. The full fingerprint/proxy/cookies payload is provided inline.

One-time profiles are faster to create and start, are not synchronised to the cloud, and are removed when stopped, so they do not clutter the profile list — well suited to scraping-style workloads. Each call costs **4 requests** of the RPM/RPH budget (see [rate-limiting.md](rate-limiting.md)).

**Endpoint**: `POST http://localhost:58888/api/profiles/one_time/start`

**Request Body**:
- `profile_data` (object, required) — same shape as `POST /profiles` body in [profiles.md](profiles.md), minus saved-only fields like `tags` and `pinned_tag`. Any field you omit is auto-generated. In addition to `fingerprint` (including `noise`, `dns`, `media_devices`), `proxy` and `start_pages`, it may carry `extensions` (`"<id>@<version>"` strings), `local_cache` (bool) and inline `cookies[]` in Chrome-extension export shape (`domain`, `expirationDate`, `hostOnly`, `httpOnly`, `name`, `path`, `sameSite`, `secure`, `value`).
- `headless` (bool, optional, default `true`) — note the default differs from [Start Profile](#start-profile).
- `debug_port` (bool, optional, default `true`)
- `flags` (string[], optional, default `[]`)
- `timeout` (int, optional, seconds, default `60`)

```bash
curl -X POST http://localhost:58888/api/profiles/one_time/start \
  -H "Content-Type: application/json" \
  -d '{
    "profile_data": {
      "fingerprint": {
        "os": "win",
        "os_version": "11",
        "os_arch": "x86",
        "screen": "1920x1080",
        "languages":  { "type": "ip" },
        "timezone":   { "type": "ip" },
        "geolocation":{ "type": "ip" },
        "webrtc":     { "type": "ip" },
        "cpu": 4,
        "ram": 8,
        "noise": { "webgl": true, "canvas": false, "audio": true, "client_rects": false },
        "dns": "1.1.1.1",
        "media_devices": { "video_in": 1, "audio_in": 1, "audio_out": 1 }
      },
      "extensions": ["ewbjmajocgfcbeboaewbfgobmjsjcoja@1.0"],
      "proxy": { "type": "socks5", "host": "1.1.1.1", "port": 5555, "login": "", "password": "" },
      "start_pages": ["https://fb.com"],
      "local_cache": true,
      "cookies": [
        {
          "domain": ".google.com",
          "expirationDate": 1639134293.313654,
          "hostOnly": false,
          "httpOnly": false,
          "name": "1P_JAR",
          "path": "/",
          "sameSite": "no_restriction",
          "secure": true,
          "value": "2021-11-10-11"
        }
      ]
    },
    "headless": false,
    "debug_port": true,
    "timeout": 60
  }'
```

#### Example Response

```json
{
  "uuid": "9a906e7d45124e6fb37388633277c22f",
  "state": "STARTED",
  "headless": false,
  "start_time": 1702904780,
  "ws_endpoint": "ws://127.0.0.1:63269/devtools/browser/f7aa4e97-c300-404f-b9c7-2633db0c1515",
  "debug_port": "63269",
  "one_time": true,
  "browser_pid": 4684,
  "connection_data": { "ip": "188.188.188.88", "country": "Germany" }
}
```

### Set Profile Password (Local)

Set or update the password protecting a single profile. Length must be 4–255 characters.

**Endpoint**: `POST http://localhost:58888/api/profiles/password`

**Request Body**:
- `uuid` (string, required)
- `password` (string, required)

```bash
curl -X POST http://localhost:58888/api/profiles/password \
  -H "Content-Type: application/json" \
  -d '{"uuid":"9585dc0cdc1e497896afe81ba1fbcdb6","password":"password"}'
```

#### Example Response

```json
{ "msg": "Profile password has been set" }
```

#### Error Responses

`503`:

```json
{ "code": "profiles.password_change_failed", "error": "Failed to change profile password", "error_code": 1 }
```

### Delete Profile Password (Local)

Remove the password from a profile. The current password must be supplied.

**Endpoint**: `DELETE http://localhost:58888/api/profiles/password`

**Request Body**:
- `uuid` (string, required)
- `password` (string, required) — current password.

```bash
curl -X DELETE http://localhost:58888/api/profiles/password \
  -H "Content-Type: application/json" \
  -d '{"uuid":"9585dc0cdc1e497896afe81ba1fbcdb6","password":"password"}'
```

#### Example Response

```json
{ "msg": "Profile password has been cleared" }
```

#### Error Responses

`400`:

```json
{ "code": "profiles.invalid_password", "error": "Profile password incorrect", "error_code": 1 }
```

```json
{ "error": "Another profile's operation in progress", "error_code": 3 }
```

```json
{ "error": "Failed to clear profile password", "error_code": 1 }
```

## Auth

Requires Octo Browser **1.8.0 or later**.

### Login

Sign in the desktop app from a script. Alternatively, launch the client with the `OCTO_API_TOKEN` environment variable set (see [Signing In With an API Token](#signing-in-with-an-api-token)).

**Endpoint**: `POST http://localhost:58888/api/auth/login`

**Request Body**:
- `email` (string, required)
- `password` (string, required)
- `api_token` (string, optional)

```bash
curl -X POST http://localhost:58888/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"useremail@domain.net","password":"userpassword"}'
```

#### Example Response

```json
{ "msg": "Logged in successfully" }
```

### Logout

**Endpoint**: `POST http://localhost:58888/api/auth/logout`

```bash
curl -X POST http://localhost:58888/api/auth/logout
```

#### Example Response

```json
{ "msg": "Logged out successfully" }
```

### Username

Return the email of the currently signed-in user.

**Endpoint**: `GET http://localhost:58888/api/username`

```bash
curl -X GET http://localhost:58888/api/username
```

#### Example Response

```json
{ "username": "user@example.com" }
```

## Updates

### Get Client Version

Returns the installed and the latest available browser versions. `update_required: true` indicates the current version is no longer supported and an update is strongly recommended.

**Endpoint**: `GET http://localhost:58888/api/update`

```bash
curl -X GET http://localhost:58888/api/update
```

#### Example Response

```json
{ "current": "1.8.2", "latest": "1.8.3", "update_required": false }
```

```json
{ "current": "1.7.6", "latest": "1.8.3", "update_required": true }
```

### Update Client

Trigger an in-place update to the latest available version. Returns `409` if the browser is already up to date.

**Endpoint**: `POST http://localhost:58888/api/update`

```bash
curl -X POST http://localhost:58888/api/update
```

#### Example Response

```json
{ "msg": "update to 1.8.3 triggerred successfully" }
```

#### Error Responses

`409`:

```json
{ "code": "client.update_failed", "error": "Update is not triggered. No available version" }
```

## Python Example

```python
import requests

LOCAL = "http://localhost:58888"
PROFILE_UUID = "2bbfd1dbaf3349cf979787f15a9e413d"

start = requests.post(f"{LOCAL}/api/profiles/start", json={
    "uuid": PROFILE_UUID,
    "headless": True,
    "debug_port": True,
}).json()

print("ws_endpoint:", start["ws_endpoint"])

# ... drive Chromium via Playwright/Puppeteer ...

requests.post(f"{LOCAL}/api/profiles/stop", json={"uuid": PROFILE_UUID})
```
