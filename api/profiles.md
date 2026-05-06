# Profiles API

Browser profiles bundle a fingerprint, an optional proxy, browser storage settings and metadata. Profiles are identified by 32-character hex `uuid` strings.

All endpoints return the standard envelope `{ "success": bool, "msg": string, "data": ..., "code": null }`. List endpoints additionally return `total_count` and `page`.

## Get Profiles

**Endpoint**: `GET /profiles`

**Query Parameters**:

| Param         | Type    | Notes |
|---------------|---------|-------|
| `page_len`    | int     | Page size; one of `10, 25, 50, 100`. |
| `page`        | int     | Zero-based page number. |
| `fields`      | string  | Comma-separated list of fields to include in each item. Allowed: `title`, `description`, `proxy`, `start_pages`, `tags`, `status`, `last_active`, `version`, `storage_options`, `created_at`, `updated_at`, `has_user_password`, `pinned_tag`, `launch_args`, `images_load_limit`, `local_cache`, `extra_info`. Without this parameter only `uuid` is returned. |
| `ordering`    | string  | One of `created`, `-created`, `active`, `-active`, `title`, `-title`. |
| `search`      | string  | Filter profiles whose title starts with the given string. |
| `search_tags` | string  | Comma-separated list of tag UUIDs. A profile is returned only when it has **all** of the listed tags. |
| `status`      | int     | Filter by status code. |
| `password`    | bool    | `true` returns only profiles with passwords; `false` returns only profiles without; omit for all. |
| `proxies`     | string  | Comma-separated list of proxy UUIDs, or the special token `@no-proxies-filter` to return only profiles without a proxy. |

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/profiles?page_len=100&page=0&fields=title,description,proxy,start_pages,tags,status,last_active,version,storage_options,created_at,updated_at&ordering=active" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": [
    { "uuid": "4bbdc824762342f485bed4968533b28a" },
    { "uuid": "4565940d5b9b41f99341fae6f5f3d855" }
  ],
  "total_count": 25,
  "page": 0,
  "code": null
}
```

## Get Profile

Fetch a single profile with the full nested fingerprint.

**Endpoint**: `GET /profiles/{uuid}`

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/profiles/cfd673b04de3433caca327836ae69d19" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": {
    "uuid": "cfd673b04de3433caca327836ae69d19",
    "title": "Quick befitting-sick",
    "description": "",
    "start_pages": [],
    "bookmarks": [],
    "tags": [],
    "pinned_tag": null,
    "proxy": null,
    "status": 0,
    "version": "0",
    "storage_options": {
      "cookies": true, "passwords": true, "extensions": true,
      "localstorage": false, "history": false, "bookmarks": true, "serviceworkers": false
    },
    "last_active": null,
    "fingerprint": {
      "os": "win", "os_version": "11", "os_arch": "x86",
      "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...",
      "screen": "1440x900",
      "renderer": "NVIDIA GeForce GT 710",
      "languages": { "type": "ip", "data": null },
      "timezone":  { "type": "ip", "data": null },
      "geolocation": { "type": "ip", "data": null },
      "webrtc": { "type": "ip", "data": null },
      "noise": { "webgl": false, "canvas": false, "audio": false, "client_rects": false },
      "media_devices": { "video_in": 1, "audio_in": 1, "audio_out": 1 },
      "fonts": ["Arial", "Times New Roman", "..."],
      "cpu": 12, "ram": 16, "dns": null
    },
    "image": "55e228c7227946b3889f370b54be26c1",
    "extensions": [],
    "local_cache": false,
    "has_user_password": true,
    "password_set_at": "2024-08-21T15:41:11",
    "created_at": "2024-08-21T15:40:15",
    "updated_at": "2024-08-21T15:41:11"
  },
  "code": null
}
```

## Create Profile

**Endpoint**: `POST /profiles`

> If you omit a parameter, the server generates a sensible value for it. Only override what you specifically need to control.

**Request Body** — top-level fields:

| Field             | Type     | Required | Notes |
|-------------------|----------|----------|-------|
| `title`           | string   | yes      | 1–90 characters. |
| `fingerprint`     | object   | yes      | See [fingerprint.md](fingerprint.md). Only `os` is mandatory inside it. |
| `description`     | string   | no       | Up to 1024 characters. |
| `start_pages`     | string[] | no       | Up to 20 URLs (each ≤ 2048 chars). |
| `bookmarks`       | object[] | no       | Up to 100 `{name, url}` items. |
| `tags`            | string[] | no       | Tag UUIDs to attach. |
| `pinned_tag`      | string   | no       | Tag UUID rendered prominently in the UI. |
| `password`        | string   | no       | Profile password (4–255 chars). |
| `proxy`           | object   | no       | Inline proxy data **or** `{ "uuid": "<saved-proxy-uuid>" }`. |
| `storage_options` | object   | no       | Toggles for cookies, passwords, extensions, localstorage, history, bookmarks, serviceworkers. |
| `cookies`         | array \| string | no | JSON, Mozilla, or Netscape format (see below). |
| `image`           | string   | no       | Profile avatar identifier. |
| `extensions`      | string[] | no       | Extension UUIDs. |
| `launch_args`     | string[] | no       | Extra Chromium command-line flags. |
| `images_load_limit` | int    | no       | Max images cached per page (bytes). |
| `local_cache`     | bool     | no       | Persist HTTP cache between sessions. |
| `extra_info`      | object   | no       | Arbitrary JSON, accessible from extensions via `chrome.cookies.getOctoProfileExtraInfo`. |

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/profiles" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test profile from api",
    "description": "test description",
    "start_pages": ["https://fb.com"],
    "tags": ["7891009afee84952a926b03e7bc0af52"],
    "pinned_tag": "7891009afee84952a926b03e7bc0af52",
    "launch_args": ["--start-maximized"],
    "proxy": {
      "type": "socks5",
      "host": "1.1.1.1",
      "port": 5555,
      "login": "",
      "password": ""
    },
    "storage_options": {
      "cookies": true, "passwords": true, "extensions": true,
      "localstorage": false, "history": false, "bookmarks": true
    },
    "fingerprint": {
      "os": "mac",
      "os_version": "11",
      "os_arch": "x86",
      "renderer": "AMD Radeon Pro 450",
      "screen": "1920x1080",
      "languages":  { "type": "ip" },
      "timezone":   { "type": "ip" },
      "geolocation":{ "type": "ip" },
      "webrtc":     { "type": "ip" },
      "cpu": 4,
      "ram": 8
    }
  }'
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": { "uuid": "21d471786f4e4038811e1e78371831d9" },
  "code": null
}
```

### Cookie Formats

The `cookies` field on create/update accepts either an array or a single string in any of these formats:

**JSON**

```json
[
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
```

**Mozilla**

```json
[
  {
    "Path raw": "/",
    "Samesite raw": "no_restriction",
    "Name raw": "NID",
    "Content raw": "2021-11-10-11",
    "Expires raw": "1639134293",
    "Host raw": "https://.google.com/",
    "This domain only raw": "false",
    "HTTP only raw": "false",
    "Send for raw": "true"
  }
]
```

**Netscape** — tab-separated text:

```
.google.com\tTRUE\t/\tTRUE\t1639134293\t1P_JAR\t2021-11-10-1\t544
```

### `extra_info` from Extensions

Add `"permissions": ["cookies"]` to the extension's `manifest.json` and call `chrome.cookies.getOctoProfileExtraInfo` from the extension's service-worker:

```js
chrome.cookies.getOctoProfileExtraInfo((extraInfo) => {
  console.log(extraInfo);
});
```

## Update Profile

**Endpoint**: `PATCH /profiles/{uuid}`

All fields are optional. The body shape matches `POST /profiles`. The full `fingerprint` object is replaced when provided — sub-fields are not deep-merged.

> Updating running profiles works, but for synchronisation safety prefer to update stopped profiles.

```bash
curl -X PATCH "https://app.octobrowser.net/api/v2/automation/profiles/d9623a2be9a0431784aacc4500d7963a" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "new title",
    "description": "new description",
    "tags": ["7891009afee84952a926b03e7bc0af52"],
    "fingerprint": { "os": "win", "os_version": "11", "screen": "1920x1080" }
  }'
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": { "uuid": "d9623a2be9a0431784aacc4500d7963a" },
  "code": null
}
```

## Delete Profiles

**Endpoint**: `DELETE /profiles`

**Request Body**:
- `uuids` (string[], required) — profiles to delete.
- `skip_trash_bin` (bool, optional, default `true`) — bypass the trash bin and delete immediately.

```bash
curl -X DELETE "https://app.octobrowser.net/api/v2/automation/profiles" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"uuids":["a4708a63d55742a09b7f1a600c248484","d7226450b9fb4bac8526c24fc3669814"], "skip_trash_bin": true}'
```

### Example Response

```json
{
  "success": true,
  "msg": "Profiles deleted",
  "data": {
    "deleted_uuids": ["a4708a63d55742a09b7f1a600c248484"],
    "active_uuids":  ["d7226450b9fb4bac8526c24fc3669814"]
  }
}
```

`active_uuids` lists profiles that could not be deleted because they were running — stop them first and retry.

## Import Cookies

**Endpoint**: `POST /profiles/{uuid}/import_cookies`

**Request Body**: `{ "cookies": <array or string> }` — accepts the same JSON, Mozilla and Netscape formats described under [Create Profile](#cookie-formats). Cookies can also be uploaded as `multipart/form-data` under the `cookies` field.

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/profiles/d9623a2be9a0431784aacc4500d7963a/import_cookies" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"cookies":[{"domain":".google.com","name":"1P_JAR","value":"2021-11-10-11","path":"/","secure":true,"httpOnly":false,"hostOnly":false,"sameSite":"no_restriction","expirationDate":1639134293.313654}]}'
```

### Example Response

```json
{ "success": true, "msg": "Cookies imported", "data": "" }
```

## Force Stop Profile

Forcibly stops a running profile.

**Endpoint**: `POST /profiles/{uuid}/force_stop`

**Request Body**:
- `version` (int, optional) — profile version for an optimistic concurrency check. Pass `null` (or omit) when you do not track versions.

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/profiles/d9623a2be9a0431784aacc4500d7963a/force_stop" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Example Response

```json
{ "success": true, "msg": "Profile stopped", "data": "" }
```

## Mass Force Stop Profile

Stops several profiles in one call.

**Endpoint**: `POST /profiles/force_stop`

**Request Body**:
- `uuids` (string[], required)

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/profiles/force_stop" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"uuids":["4b8afed25a524f5aa1dc2922279622f8","21d471786f4e4038811e1e78371831d9"]}'
```

### Example Response (partial failure)

```json
{
  "success": false,
  "msg": "Bulk force stop error",
  "code": "profiles.stop_error",
  "data": { "failed": ["4b8afed25a524f5aa1dc2922279622f8"] }
}
```

When every profile is stopped successfully `success` is `true` and `data.failed` is empty.

## Transfer Profiles

Move profiles to another account on the same workspace.

**Endpoint**: `POST /profiles/transfer`

**Request Body**:
- `uuids` (string[], required) — up to 100 entries per request.
- `receiver_email` (string, required) — destination account email.
- `transfer_proxy` (bool, required) — transfer the attached proxies along with the profiles.

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/profiles/transfer" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"uuids":["21d471786f4e4038811e1e78371831d9"], "receiver_email":"team-mate@example.com", "transfer_proxy": true}'
```

### Example Response

```json
{ "success": true, "msg": "Profiles transferred successfully", "data": "" }
```

## Export Profiles

Encode profiles into transferable strings.

**Endpoint**: `POST /profiles/export`

> Paid action — costs 0.5 tokens per profile. Up to 100 profiles per request; duplicate UUIDs are silently ignored.

**Request Body**:
- `uuids` (string[], required)
- `export_proxy` (bool, required) — include the attached proxy data in the export blob.

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/profiles/export" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"uuids":["21d471786f4e4038811e1e78371831d9"], "export_proxy": false}'
```

### Example Response

```json
{
  "success": true,
  "msg": "Profiles exported successfully",
  "data": {
    "exported": [
      {
        "uuid": "21d471786f4e4038811e1e78371831d9",
        "title": "Test profile from api",
        "data": "MEYCIQDcEhji9E69bcOC1853v0zlXIP8kq6ecKwdcejBYkagrwIhAPUU/65bZqoT74AiqKT4IVuKK26zkBN2M9HTFJoZC4rS"
      }
    ],
    "failed": []
  }
}
```

## List Exports

Paginated list of previously generated exports for the account.

**Endpoint**: `GET /profiles/export`

**Query Parameters**:
- `page` (int, optional)
- `page_len` (int, optional)

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/profiles/export?page=0&page_len=10" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": {
    "data": [
      {
        "uuid": "21d471786f4e4038811e1e78371831d9",
        "title": "Test profile from api",
        "data": "JGFlc19nY20kJFpkbkZ6WWlOTVROejNCRnhwVDBuanZJcWp6a0lLemNvV2VpWXEvLkdETC40WFF1QmdwYnlNampRcTRzZ1JSUmJqWHhKMjNWbnVITUxuL1ZTMTBCT1BmaVZZS0E="
      }
    ],
    "total": 1,
    "page": 0
  }
}
```

> Note: pagination keys here are nested under `data` and use `total` (not `total_count`).

## Get Export

Fetch a single previously generated export.

**Endpoint**: `GET /profiles/export/{uuid}`

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/profiles/export/21d471786f4e4038811e1e78371831d9" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": {
    "uuid": "21d471786f4e4038811e1e78371831d9",
    "title": "Test profile from api",
    "data": "JGFlc19nY20kJDMvMzBKcW12d2tXYi91UlRNL1ZHNFNTZEROYUlKSC5wbDRwWTdkaFlac0pBRUE4dkpVOXVRclhnWnpPT3N5eUtUOUlKOGMveTZkekpmemRPMEFMd3Z0YnBsenM="
  }
}
```

## Import Profiles

Restore profiles from export blobs.

**Endpoint**: `POST /profiles/import`

> Up to 100 profiles per request.

**Request Body**:
- `data` (string[], required) — array of export `data` strings.

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/profiles/import" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data":["MEYCIQDcEhji9E69bcOC1853v0zlXIP8kq6ecKwdcejBYkagrwIhAPUU/65bZqoT74AiqKT4IVuKK26zkBN2M9HTFJoZC4rS"]}'
```

### Example Response

```json
{
  "success": true,
  "msg": "Profiles imported successfully",
  "data": { "failed": [] }
}
```

## Set Profiles Password

Set or change the password protecting one or more profiles.

**Endpoint**: `POST /profiles/set_password`

**Request Body**:
- `profiles` (string[], required) — profile UUIDs.
- `password` (string, required) — new password.
- `old_password` (string, required when changing an existing password) — current password. Omit when setting a password for the first time.

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/profiles/set_password" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"profiles":["21d471786f4e4038811e1e78371831d9"], "password":"new-pw", "old_password":"old-pw"}'
```

### Example Response

```json
{ "success": true, "msg": "Password has been set for selected profiles", "data": "" }
```

## Clear Profile Password

Remove the password from a single profile. The current password must be provided.

**Endpoint**: `POST /profiles/{uuid}/clear_password`

**Request Body**:
- `password` (string, required) — current profile password.

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/profiles/21d471786f4e4038811e1e78371831d9/clear_password" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"password":"current-pw"}'
```

### Example Response

```json
{ "success": true, "msg": "Password has been cleared", "data": "" }
```

## Common Errors

- **400 Bad Request** — body fails validation (see the `validation_error` envelope in [errors.md](errors.md)).
- **404 Not Found** — profile UUID does not exist.
- **409 Conflict** — profile is locked, running, or its `version` does not match.
- **422 Unprocessable Entity** — referenced tag/proxy/extension UUID is unknown.
