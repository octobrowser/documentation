# Fingerprint API

The `fingerprint` object on a profile controls every detectable browser characteristic. Four lookup endpoints expose the values accepted by that object.

All endpoints return the standard envelope `{ "success": bool, "msg": string, "data": ..., "code": string | null }`. The renderers endpoint also returns `total_count` and `page` for pagination; platforms, screens and device models return a bare `data` array.

## Fingerprint Object

The `fingerprint` field is required on profile creation. Only `os` is mandatory inside it; the other fields are optional and the server fills sensible defaults when omitted.

### Common Fields

| Field         | Type    | Notes |
|---------------|---------|-------|
| `os`          | enum    | `win`, `mac`, `android`. Required. Any other value (`ios`, `lin`) is rejected with `400` (`Input should be 'win', 'mac' or 'android'`) — iOS profiles cannot be created through the API (see [iOS profiles](profiles.md#ios-profiles)). |
| `os_arch`     | string  | `x86` or `arm`. Defaults depend on `os`; use `arm` for Android and Apple silicon Macs. Valid `os`/`os_arch` pairs are listed by [Get Platforms](#get-platforms). |
| `os_version`  | string  | Must be one of the versions [Get Platforms](#get-platforms) lists for the `os`/`os_arch` pair: currently `10`, `11` for Windows; `13`, `14`, `15`, `26` for macOS; `12`–`15` for Android (model-dependent — use only versions listed in `os_versions` for the chosen `device_model`, otherwise the API returns `fingerprints.invalid_mobile_model`). An unsupported desktop version (e.g. macOS `11`) returns `400` `{"success":false,"msg":"OS version does not match allowed versions for the platform","data":"","code":"validation_error"}`. |
| `user_agent`  | string  | Up to 255 chars. |
| `screen`      | string  | `<width>x<height> @<scale> <SDR\|HDR>[ P3][ ext]`, 3–32 chars, e.g. `1920x1080 @1 SDR`, `1440x900 @2 HDR P3`. Pick from [`GET /fingerprint/screens`](#get-screens). A legacy bare resolution such as `1920x1080` is still accepted and normalised to `1920x1080 @1 SDR`. |
| `cpu`         | int     | One of `2, 4, 6, 8, 10, 11, 12, 14, 15, 16, 18, 20, 24, 32`. |
| `ram`         | int     | One of `2, 4, 8, 12, 16, 24, 32, 36, 48, 64, 128` (GB). |
| `renderer`    | string  | WebGL renderer; pick from `GET /fingerprint/renderers`. |
| `fonts`       | array   | List of system font names. |
| `dns`         | string  | Custom DNS server. |
| `noise`       | object  | Anti-fingerprinting noise toggles, see below. |
| `media_devices` | object | Number of `video_in`, `audio_in`, `audio_out` devices (integers 0–5), flat or wrapped in `{"type": "manual", "data": {...}}`. See [Media Devices](#media-devices). |
| `languages`   | object  | See [Languages](#languages-configuration). |
| `timezone`    | object  | See [Timezone](#timezone-configuration). |
| `geolocation` | object  | See [Geolocation](#geolocation-configuration). |
| `webrtc`      | object  | See [WebRTC](#webrtc-configuration). |

### Mobile Fields

When `os` is `android`, the following extra fields apply:

| Field           | Type   | Notes |
|-----------------|--------|-------|
| `device_type`   | enum   | `phone` or `tablet`. Optional; when sent it is validated against the chosen `device_model` — a mismatch (e.g. `tablet` for a phone model) or any other value returns `400` `{"success":false,"msg":"invalid mobile type","data":"","code":"fingerprints.invalid_mobile_type"}`. |
| `device_model`  | string | Model identifier from `GET /fingerprint/device_models`. |

Mobile (Android) profiles do not support browser extensions. `GET /profiles/{uuid}` returns an Android fingerprint without `screen`, `cpu`, `ram`, `renderer`, `fonts`, `noise` and `media_devices` — those are derived from the device model.

## Get Platforms

List the supported operating systems with their architectures and OS versions. Use these values for `os`, `os_arch` and `os_version` in the profile fingerprint.

**Endpoint**: `GET /fingerprint/platforms`

Takes no parameters (query parameters are ignored). Not paginated. There is no iOS entry — iOS profiles cannot be created through the API.

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/fingerprint/platforms" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": [
    { "os": "win", "archs": [ { "arch": "x86", "os_versions": ["10", "11"] } ] },
    { "os": "mac", "archs": [
        { "arch": "x86", "os_versions": ["13", "14", "15", "26"] },
        { "arch": "arm", "os_versions": ["13", "14", "15", "26"] }
    ] },
    { "os": "android", "archs": [ { "arch": "arm", "os_versions": ["12", "13", "14", "15"] } ] }
  ],
  "code": null
}
```

## Get Renderers

List WebGL renderer strings filtered by OS and architecture. Paginated.

**Endpoint**: `GET /fingerprint/renderers`

**Query Parameters**:
- `os` (string, optional) — `win`, `mac`, or `android`. Defaults to `win`. Any other value (e.g. `lin`) is rejected with `400` (`Input should be 'win', 'mac' or 'android'`).
- `os_arch` (string, optional) — `x86` or `arm`.
- `page_len` (int, optional) — page size; must be one of `10, 25, 50, 100`, any other value is rejected with `400`.
- `page` (int, optional) — zero-based page number.

`os=android` currently returns an empty list — mobile renderers are derived from the `device_model`.

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
  "code": null,
  "total_count": 250,
  "page": 0
}
```

## Get Screens

List screen configurations for the requested platform. Not paginated.

**Endpoint**: `GET /fingerprint/screens`

**Query Parameters**:
- `os` (string, optional) — `win`, `mac`, or `android`. Defaults to `win`; other values are rejected with `400`.
- `os_arch` (string, optional) — `x86` or `arm`.

`os=android` currently returns an empty list — mobile screens are derived from the `device_model`.

Each `value` has the form `<width>x<height> @<scale> <SDR|HDR>[ P3][ ext]`: the CSS resolution, the device pixel ratio (`1`, `1.25`, `1.5`, `1.75`, `2`, …), the dynamic range, an optional `P3` wide-gamut colour flag and an optional `ext` suffix. Several entries can share the same resolution. Pass the `value` verbatim as `fingerprint.screen`.

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
    { "value": "1280x720 @1 SDR ext",  "platform": "win", "archs": ["x86"] },
    { "value": "1280x720 @1.5 HDR P3", "platform": "win", "archs": ["x86"] },
    { "value": "1440x900 @1 SDR",      "platform": "win", "archs": ["x86"] },
    { "value": "1920x1080 @1 SDR",     "platform": "win", "archs": ["x86"] },
    { "value": "2560x1440 @1.25 SDR",  "platform": "win", "archs": ["x86"] }
  ],
  "code": null
}
```

For `os=mac`, entries such as `{ "value": "1440x900 @2 HDR P3", "platform": "mac", "archs": ["x86", "arm"] }` list both architectures.

## Get Mobile Device Models

List Android device models that can be used for mobile fingerprints.

**Endpoint**: `GET /fingerprint/device_models`

**Query Parameters**:
- `device_type` (string, optional) — `phone` or `tablet`. Does not actually filter, see the note below.
- `os` (string, optional), `os_arch` (string, optional), `os_version` (string, optional, `12`–`15`) — additional filters (per the official spec).

The response is not paginated — all models (800+) are returned in one call, so cache it client-side. Each item is `{ value, os, os_versions[], archs[], device_type }`.

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
    { "value": "M2102J20SG", "os": "android", "os_versions": ["12", "13"], "archs": ["arm"], "device_type": "phone" },
    { "value": "SM-M526B",   "os": "android", "os_versions": ["13"], "archs": ["arm"], "device_type": "phone" },
    { "value": "moto g32",   "os": "android", "os_versions": ["13"], "archs": ["arm"], "device_type": "phone" }
  ],
  "code": null
}
```

> The endpoint returns both phones and tablets regardless of the requested `device_type` (`device_type=phone` still includes tablets such as `SM-T870`). Filter the response client-side on the `device_type` field if you need a strict match.

## Configuration Types

### Languages Configuration

```json
{ "type": "manual", "data": ["en-US", "en"] }
```

- `type` — `ip` (auto-detect from proxy IP), `real` (system languages), or `manual`.
- `data` — array of language tags. Required only when `type=manual`. The API stores any strings verbatim without validation or normalisation (both `["ru-RU","en-US"]` and `["[ru-RU] Russian (Russia)"]` are accepted), so use well-formed BCP-47 tags such as `en-US` to keep the browser's `navigator.languages` realistic.

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

On create and update, two equivalent input forms are accepted — flat:

```json
{ "video_in": 1, "audio_in": 1, "audio_out": 2 }
```

or wrapped, as in the official spec:

```json
{ "type": "manual", "data": { "video_in": 1, "audio_in": 1, "audio_out": 2 } }
```

Each counter accepts integers 0–5 (the official spec defaults each to `1`). `GET /profiles/{uuid}` always returns the flat form, whichever form was sent. The official spec also lists `{ "type": "real" }` (not verified).

## Fingerprint Examples

### Basic Windows Fingerprint

```json
{
  "os": "win",
  "os_version": "10",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "screen": "1920x1080 @1 SDR",
  "cpu": 8,
  "ram": 16
}
```

### macOS (Apple Silicon) Fingerprint

```json
{
  "os": "mac",
  "os_arch": "arm",
  "os_version": "14",
  "screen": "1440x900 @2 HDR P3"
}
```

### Android Mobile Fingerprint

```json
{
  "os": "android",
  "os_arch": "arm",
  "os_version": "13",
  "device_type": "phone",
  "device_model": "M2102J20SG",
  "user_agent": "Mozilla/5.0 (Linux; Android 13; M2102J20SG) AppleWebKit/537.36 Mobile Safari/537.36",
  "languages": { "type": "ip", "data": null },
  "timezone": { "type": "ip", "data": null },
  "geolocation": { "type": "ip", "data": null },
  "webrtc": { "type": "ip" }
}
```

### Android Tablet Fingerprint

```json
{
  "os": "android",
  "os_arch": "arm",
  "os_version": "13",
  "device_type": "tablet",
  "device_model": "SM-T870"
}
```

### Fully Specified Desktop Fingerprint

```json
{
  "os": "win",
  "os_version": "11",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "screen": "1920x1080 @1 SDR",
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

- Use values from `/fingerprint/platforms`, `/fingerprint/renderers`, `/fingerprint/screens`, and `/fingerprint/device_models` rather than guessing — invalid values are rejected.
- Keep `user_agent` consistent with `os` and `os_version`.
- Do not attach `extensions` to Android profiles — mobile profiles do not support them.
- Match `timezone`/`geolocation` to your proxy's location when realism matters.
- For mobile profiles, always pair `device_type` with a `device_model` from the lookup endpoint, and pick `os_version` from that model's `os_versions` list — a version the model does not support is rejected with `fingerprints.invalid_mobile_model`, a `device_type` that does not match the model with `fingerprints.invalid_mobile_type`.
