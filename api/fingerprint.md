# Fingerprint API

The `fingerprint` object on a profile controls every detectable browser characteristic. Three lookup endpoints expose the values accepted by that object.

All endpoints return the standard envelope `{ "success": bool, "msg": string, "data": ... }`. The renderers endpoint also returns `total_count` and `page` for pagination.

## Fingerprint Object

The `fingerprint` field is required on profile creation. Only `os` is mandatory inside it; the other fields are optional and the server fills sensible defaults when omitted.

### Common Fields

| Field         | Type    | Notes |
|---------------|---------|-------|
| `os`          | enum    | `win`, `mac`, `lin`, `android`. Required. |
| `os_arch`     | string  | `x86` or `arm`. Defaults depend on `os`. |
| `os_version`  | string  | E.g. `10`, `11` for Windows; `13`, `14`, `15` for Android. |
| `user_agent`  | string  | Up to 255 chars. |
| `screen`      | string  | E.g. `1920x1080`. Pick from `GET /fingerprint/screens`. |
| `cpu`         | int     | One of `2, 4, 6, 8, 10, 11, 12, 14, 16, 20, 24`. |
| `ram`         | int     | One of `2, 4, 8, 12, 16, 24, 32, 64` (GB). |
| `renderer`    | string  | WebGL renderer; pick from `GET /fingerprint/renderers`. |
| `fonts`       | array   | List of system font names. |
| `dns`         | string  | Custom DNS server. |
| `noise`       | object  | Anti-fingerprinting noise toggles, see below. |
| `media_devices` | object | `video_in`, `audio_in`, `audio_out` — integers 0–5. |
| `languages`   | object  | See [Languages](#languages-configuration). |
| `timezone`    | object  | See [Timezone](#timezone-configuration). |
| `geolocation` | object  | See [Geolocation](#geolocation-configuration). |
| `webrtc`      | object  | See [WebRTC](#webrtc-configuration). |

### Mobile Fields

When `os` is `android`, the following extra fields apply:

| Field           | Type   | Notes |
|-----------------|--------|-------|
| `device_type`   | enum   | `phone` or `tablet`. |
| `device_model`  | string | Model identifier from `GET /fingerprint/device_models`. |

## Get Renderers

List WebGL renderer strings filtered by OS and architecture. Paginated.

**Endpoint**: `GET /fingerprint/renderers`

**Query Parameters**:
- `os` (string, optional) — `win`, `mac`, `lin`, `android`.
- `os_arch` (string, optional) — `x86` or `arm`.
- `page_len` (int, optional) — page size; one of `10, 25, 50, 100`.
- `page` (int, optional) — zero-based page number.

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/fingerprint/renderers?os=win&os_arch=x86&page_len=100&page=0" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": [
    { "value": "ATI Radeon HD 3200 Graphics (Microsoft Corporation WDDM 1.1)", "platform": "win", "archs": ["x86"] },
    { "value": "NVIDIA GeForce GTX 660", "platform": "win", "archs": ["x86"] },
    { "value": "AMD Radeon HD 6800 Series", "platform": "win", "archs": ["x86"] },
    { "value": "Apple M2 Pro", "platform": "mac", "archs": ["arm"] }
  ],
  "total_count": 250,
  "page": 0
}
```

## Get Screens

List screen resolutions for the requested platform.

**Endpoint**: `GET /fingerprint/screens`

**Query Parameters**:
- `os` (string, optional) — `win`, `mac`, `lin`, `android`.
- `os_arch` (string, optional) — `x86` or `arm`.

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/fingerprint/screens?os=win&os_arch=x86" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": [
    { "value": "1440x900",  "platform": "win", "archs": ["x86"] },
    { "value": "1920x1080", "platform": "win", "archs": ["x86"] },
    { "value": "2560x1440 (2K)", "platform": "win", "archs": ["x86"] }
  ]
}
```

## Get Mobile Device Models

List Android device models that can be used for mobile fingerprints.

**Endpoint**: `GET /fingerprint/device_models`

**Query Parameters**:
- `device_type` (string, required) — `phone` or `tablet`.

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/fingerprint/device_models?device_type=phone" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": [
    { "value": "M2102J20SG", "os": "android", "os_versions": ["12"], "archs": ["arm"], "device_type": "phone" },
    { "value": "SM-M526B",   "os": "android", "os_versions": ["13"], "archs": ["arm"], "device_type": "phone" },
    { "value": "moto g32",   "os": "android", "os_versions": ["13"], "archs": ["arm"], "device_type": "phone" }
  ]
}
```

> The endpoint returns both phones and tablets regardless of the requested `device_type`. Filter the response client-side on the `device_type` field if you need a strict match.

## Configuration Types

### Languages Configuration

```json
{ "type": "manual", "data": ["en-US", "en"] }
```

- `type` — `ip` (auto-detect from proxy IP), `real` (system languages), or `manual`.
- `data` — array of BCP-47 language tags. Required only when `type=manual`.

### Timezone Configuration

```json
{ "type": "manual", "data": "America/New_York" }
```

- `type` — `ip`, `real`, or `manual`.
- `data` — IANA timezone string. Required only when `type=manual`.

### Geolocation Configuration

```json
{ "type": "manual", "data": { "latitude": 40.7128, "longitude": -74.0060, "accuracy": 100 } }
```

- `type` — `ip`, `real`, or `manual`.
- `data` — `{latitude, longitude, accuracy}`. Required only when `type=manual`.

### WebRTC Configuration

```json
{ "type": "ip" }
```

- `type` — `ip` (use proxy IP), `real`, or `disable_non_proxied_udp`.
- `data` — optional explicit IP override. Not accepted when `type=real` or `type=disable_non_proxied_udp`.

### Noise Configuration

```json
{ "webgl": true, "canvas": false, "audio": true, "client_rects": false }
```

All four flags are independent booleans controlling fingerprint noise injection.

### Media Devices

```json
{ "video_in": 1, "audio_in": 1, "audio_out": 2 }
```

Each counter accepts integers 0–5.

## Fingerprint Examples

### Basic Windows Fingerprint

```json
{
  "os": "win",
  "os_version": "10",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "screen": "1920x1080",
  "cpu": 8,
  "ram": 16
}
```

### Android Mobile Fingerprint

```json
{
  "os": "android",
  "os_arch": "arm",
  "os_version": "15",
  "device_type": "phone",
  "device_model": "SM-S911U",
  "user_agent": "Mozilla/5.0 (Linux; Android 15; SM-S911U) AppleWebKit/537.36 Mobile Safari/537.36",
  "languages": { "type": "ip", "data": null },
  "timezone": { "type": "ip", "data": null },
  "geolocation": { "type": "ip", "data": null },
  "webrtc": { "type": "ip" }
}
```

### Fully Specified Desktop Fingerprint

```json
{
  "os": "win",
  "os_version": "11",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "screen": "1920x1080",
  "cpu": 8,
  "ram": 16,
  "renderer": "ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0)",
  "languages": { "type": "manual", "data": ["en-US", "en"] },
  "timezone":  { "type": "manual", "data": "America/New_York" },
  "geolocation": { "type": "manual", "data": { "latitude": 40.7128, "longitude": -74.0060, "accuracy": 100 } },
  "webrtc": { "type": "ip" },
  "noise": { "webgl": true, "audio": true, "canvas": false, "client_rects": false },
  "fonts": ["Arial", "Verdana", "Times New Roman"],
  "media_devices": { "video_in": 1, "audio_in": 1, "audio_out": 2 },
  "dns": "8.8.8.8"
}
```

## Best Practices

- Use values from `/fingerprint/renderers`, `/fingerprint/screens`, and `/fingerprint/device_models` rather than guessing — invalid values are rejected.
- Keep `user_agent` consistent with `os` and `os_version`.
- Match `timezone`/`geolocation` to your proxy's location when realism matters.
- For mobile profiles, always pair `device_type` with a `device_model` from the lookup endpoint.
