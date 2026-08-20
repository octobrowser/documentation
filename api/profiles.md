# Profiles API

Browser profiles bundle a fingerprint, an optional proxy, browser storage settings and metadata. Profiles are identified by 32-character hex `uuid` strings.

All endpoints return the standard envelope `{ "success": bool, "msg": string, "data": ..., "code": string | null }`. List endpoints additionally return `total_count` and `page`.

## Get Profiles

**Endpoint**: `GET /profiles`

**Query Parameters**:

| Param         | Type    | Notes |
|---------------|---------|-------|
| `page_len`    | int     | Page size; one of `10, 25, 50, 100`. Default `10`. |
| `page`        | int     | Zero-based page number. Default `0`. |
| `fields`      | string  | Comma-separated list of fields to include in each item. Allowed: `title`, `description`, `proxy`, `start_pages`, `tags`, `status`, `last_active`, `version`, `storage_options`, `created_at`, `updated_at`, `has_user_password`, `pinned_tag`, `folder`, `launch_args`, `images_load_limit`, `local_cache`, `extra_info`. Without this parameter only `uuid` is returned. |
| `ordering`    | string  | One of `created`, `-created`, `active`, `-active`, `title`, `-title`. |
| `search`      | string  | Filter profiles whose title starts with the given string. |
| `search_tags` | string  | Comma-separated list of tag **names**. A profile is returned only when it has **all** of the listed tags. |
| `status`      | int     | Filter by status code. |
| `password`    | bool    | `true` returns only profiles with passwords; `false` returns only profiles without; omit for all. |
| `proxies`     | string  | Comma-separated list of proxy UUIDs, or the special token `@no-proxies-filter` to return only profiles without a proxy. |

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/profiles?page_len=100&page=0&fields=title,description,folder,proxy,start_pages,tags,status,last_active,version,storage_options,created_at,updated_at&ordering=active" \
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

Fetch a single profile with the full nested fingerprint. The full object is always returned — a `fields` query parameter is ignored here. `folder` is `null` when the profile is not in a folder. The official Postman sample also shows a `user_agent_changed_by_user` field inside `fingerprint`; it was not returned by the live API on 2026-08-20.

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
    "folder": null,
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
    "launch_args": [],
    "images_load_limit": null,
    "local_cache": false,
    "extra_info": null,
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

> Tip: if you are unsure what a working payload looks like, configure a profile in the browser UI, then fetch it with [`GET /profiles/{uuid}`](#get-profile) and reuse the returned fields.

**Request Body** — top-level fields:

| Field             | Type     | Required | Notes |
|-------------------|----------|----------|-------|
| `title`           | string   | yes      | 1–90 characters. |
| `fingerprint`     | object   | yes      | See [fingerprint.md](fingerprint.md). Only `os` is mandatory inside it. With manual `timezone` data you currently have to account for daylight-saving time yourself (upstream caveat). |
| `description`     | string   | no       | Up to 1024 characters. |
| `start_pages`     | string[] | no       | Up to 20 URLs (each ≤ 2048 chars). |
| `bookmarks`       | object[] | no       | Up to 100 `{name, url}` items. |
| `tags`            | string[] | no       | Tag **names** to attach (each 1–20 chars). Tags are referenced by name here, not by UUID. |
| `pinned_tag`      | string   | no       | Tag **name** rendered prominently in the UI. |
| `folder`          | string   | no       | Folder to place the profile in (see [folders.md](folders.md)). Octo 3.0+. |
| `password`        | string   | no       | Profile password (4–255 chars). |
| `proxy`           | object \| string \| null | no       | Saved proxy by UUID, inline temporary proxy, or `null`. See [Proxy Field](#proxy-field). |
| `storage_options` | object   | no       | Toggles for cookies, passwords, extensions, localstorage, history, bookmarks, serviceworkers. |
| `cookies`         | array \| string | no | JSON array, or a string in JSON, Mozilla, or Netscape format (see below). The string may be base64-encoded; string form is capped at 16 MiB. |
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
    "tags": ["octo"],
    "pinned_tag": "octo",
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

### Create Mobile Profile

Mobile profiles pick a `device_model` (see [fingerprint.md](fingerprint.md)); `os_version` must be one of that model's `os_versions`. Mobile profiles do not support extensions.

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/profiles" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test mobile profile from api",
    "description": "Mobile profiles do not support extensions",
    "fingerprint": {
      "device_model": "SM-T870",
      "device_type": "tablet",
      "os": "android",
      "os_arch": "arm",
      "os_version": "13"
    }
  }'
```

### Proxy Field

The `proxy` field on create/update accepts three forms:

- `{ "uuid": "<proxy-uuid>" }` — attach a saved proxy from [proxies.md](proxies.md). A plain string, `"proxy": "<proxy-uuid>"`, is accepted and means the same.
- `{ "type": "...", "host": "...", "port": ..., "login": "...", "password": "..." }` — a temporary proxy bound to this profile only. Sending an inline object again edits the profile's existing temporary proxy in place. In `GET` responses a temporary proxy appears with `"uuid": ""` and no `title`/`profiles_count`.
- `null` — detach the proxy. A temporary proxy is deleted in this case, as it is when the profile is switched from it to a saved proxy.

Temporary proxies cannot be referenced by UUID. Passing the UUID of a temporary proxy, or an unknown UUID, fails with `404`:

```json
{ "success": false, "msg": "proxy not found:", "data": "", "code": "not_found" }
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

**Netscape** — tab-separated text, one cookie per line (newline-separated for several cookies):

```
.google.com\tTRUE\t/\tTRUE\t1639134293\t1P_JAR\t2021-11-10-1\t544
```

As a JSON request value:

```json
{
  "title": "Test profile from api with netscape cookies",
  "fingerprint": { "os": "win" },
  "cookies": "some.host\tTRUE\t/\tTRUE\t123\tname\tvalue\nsome2.host\tTRUE\t/\tTRUE\t111\tname2\tvalue2"
}
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

All fields are optional. The body shape matches `POST /profiles`, except that `password` is not accepted here — use [`POST /profiles/set_password`](#set-profiles-password) instead. A partial `fingerprint` object is accepted (only the listed sub-fields change), but `fingerprint.os` cannot be changed: any `fingerprint` containing `os` — even the current value — is rejected with `400` `profiles.update_error` (`You can't update os.`). Setting `proxy` to `null` detaches the proxy; `images_load_limit` is accepted here.

> Updating running profiles works, but for synchronisation safety prefer to update stopped profiles.

```bash
curl -X PATCH "https://app.octobrowser.net/api/v2/automation/profiles/d9623a2be9a0431784aacc4500d7963a" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "new title",
    "description": "new description",
    "tags": ["octo"],
    "fingerprint": { "os_version": "11", "screen": "1920x1080" }
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
- `uuids` (string[], required) — profiles to delete, 1–100 per request.
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

**Request Body**: `{ "cookies": <array or string> }` — accepts the same JSON, Mozilla and Netscape formats described under [Cookie Formats](#cookie-formats). Cookies can also be uploaded as `multipart/form-data` under the `cookies` field. The profile must not be running (`409` otherwise).

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
- `version` (int | null, required) — profile version for an optimistic concurrency check. The field must be present; pass `null` when you do not track versions. Omitting it entirely returns a `400` validation error (`Field required`).

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/profiles/d9623a2be9a0431784aacc4500d7963a/force_stop" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"version": null}'
```

### Example Response

```json
{ "success": true, "msg": "Profile stopped", "data": "" }
```

## Mass Force Stop Profile

Stops several profiles in one call. Unlike the single-profile endpoint, this one takes no `version` and performs no consistency check.

**Endpoint**: `POST /profiles/force_stop`

**Request Body**:
- `uuids` (string[], required) — 1–100 per request.

**Response**: `data.failed` lists the UUIDs that were not stopped (for example, profiles that were not running). Status codes:

| Code | Meaning |
|------|---------|
| 200  | All requested profiles were stopped; `success` is `true` and `data.failed` is empty. |
| 207  | Multi-Status — only some were stopped, per the official Postman collection (not live-verified). |
| 400  | None were stopped; `code` is `profiles.stop_error`. |

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/profiles/force_stop" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"uuids":["4b8afed25a524f5aa1dc2922279622f8","21d471786f4e4038811e1e78371831d9"]}'
```

### Example Response (400 — none stopped)

```json
{
  "success": false,
  "msg": "Bulk force stop error",
  "code": "profiles.stop_error",
  "data": { "failed": ["4b8afed25a524f5aa1dc2922279622f8", "21d471786f4e4038811e1e78371831d9"] }
}
```

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
- `uuids` (string[], required) — up to 100 per request.
- `export_proxy` (bool, required) — include the attached proxy data in the export blob.
- `app_version` (string, optional) — client version to target the export format at.

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
- `data` (array, required) — up to 100 items, each in one of three forms:
  - a string — the `data` blob from [`POST /profiles/export`](#export-profiles);
  - an object `{ "data", "title", "uuid" }` — an entry from a new-format export file, passed verbatim;
  - an object `{ "data": "<json string>", "signature" }` — an entry from an old (V1) export file.
- `folder` (string, optional) — folder to place the imported profiles in (see [folders.md](folders.md)). Octo 3.0+.

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/profiles/import" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data":["MEYCIQDcEhji9E69bcOC1853v0zlXIP8kq6ecKwdcejBYkagrwIhAPUU/65bZqoT74AiqKT4IVuKK26zkBN2M9HTFJoZC4rS"]}'
```

Import from a new-format export file:

```json
{
  "data": [
    {
      "data": "JGFlc19nY20kJE1mUk9tVS5KUGhrZmZyeGVCcGpzQ1VDa2xOUWRtcGdtVXc2WGdnMldqNWU5bFdHcGFnME5LSzZQa1BZLndsdnZEMWRZdHRudG5GdW5xakk5aUxyRWIycHhWdw==",
      "title": "[Imported] Quick bouncy-reception",
      "uuid": "761c6c15b2e44545851061555c665319"
    }
  ]
}
```

Import from an old-format (V1) export file:

```json
{
  "data": [
    {
      "data": "{\"title\": \"[Imported] Quick rosy-chairlift\", \"exported_at\": \"2023-12-06 08:58:38\", \"profile\": \"gAAAAABlcDhTKzTeRIj2pGHBg-zJggNGMsekvt2DT47uM_iZYua9yoEmov0x3ZQKOu-XSWjgMGLL3CAC8rN92zyj-qOBVw3bnA==\"}",
      "signature": "MEUCIQD4ynaphY6R0TjQPz6hb5cmPaN5W+5pguRT65a6KB4r/gIgDOOcLfRvhrmeYHSpRIKSnjaziXM6lrS1OvVm86vxKVk="
    }
  ]
}
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

Set or change the password protecting one or more profiles. The same password is applied to every listed profile. The request is all-or-nothing: if `old_password` does not match for one of the profiles, or one of them is currently running on another machine, the whole request fails with `400` and no profile is changed.

**Endpoint**: `POST /profiles/set_password`

**Request Body**:
- `profiles` (string[], required) — profile UUIDs.
- `password` (string, required) — new password, 4–255 characters.
- `old_password` (string, required when any listed profile already has a password) — a single value that must match the current password of every listed profile that has one. Omit when none of them has a password yet.

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

Remove the password from a single profile. The current password must be provided; if it does not match, the request fails with `400` `profiles.password_error`.

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

- **400 Bad Request** — body fails validation (see the `validation_error` envelope in [errors.md](errors.md)), `fingerprint.os` sent on `PATCH` (`profiles.update_error`), a wrong password (`profiles.password_error`), or a mass `force_stop` that stopped nothing (`profiles.stop_error`).
- **404 Not Found** — profile UUID does not exist, or the `proxy` UUID is unknown or belongs to a temporary proxy (`proxy not found:`).
- **409 Conflict** — profile is locked, running (e.g. on `import_cookies`), or its `version` does not match.
- Unknown tag **names** (≤ 20 chars) in `tags[]` are not an error: the request succeeds and the tag is silently dropped (no tag is auto-created). Names longer than 20 characters return `400` `string_too_long`.
