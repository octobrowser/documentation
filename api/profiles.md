# Profiles API

Browser profiles bundle a fingerprint, an optional proxy, browser storage settings and metadata. Profiles are identified by 32-character hex `uuid` strings.

All endpoints return the standard envelope `{ "success": bool, "msg": string, "data": ..., "code": string | null }`. The list endpoints `GET /profiles` and `GET /profiles/trash_bin` additionally return top-level `total_count` and `page`; `GET /profiles/export` nests its pagination inside `data` (see [List Exports](#list-exports)).

Most endpoints need a specific API token permission (Octo 3.2+), noted as **Required permission** under each endpoint; a call without it fails with `403` `no_permission` (see [API Token Permissions](authentication.md#api-token-permissions)). Endpoints without a **Required permission** line (e.g. `GET /profiles`, `GET /profiles/{uuid}`) need no specific permission, but their results are limited to what the token can see.

## Get Profiles

**Endpoint**: `GET /profiles`

Only profiles visible to the API token are returned. Without the Edit profiles permission, `description` is returned masked as `**`.

**Query Parameters**:

| Param         | Type    | Notes |
|---------------|---------|-------|
| `page_len`    | int     | Page size; one of `10, 25, 50, 100`. Default `10`. |
| `page`        | int     | Zero-based page number. Default `0`. |
| `fields`      | string  | Comma-separated list of fields to include in each item. Allowed: `title`, `description`, `proxy`, `start_pages`, `tags`, `status`, `last_active`, `version`, `storage_options`, `created_at`, `updated_at`, `has_user_password`, `pinned_tag`, `folder`, `launch_args`, `images_load_limit`, `local_cache`, `extra_info`. Without this parameter only `uuid` is returned. |
| `ordering`    | string  | One of `created`, `-created`, `active`, `-active`, `title`, `-title`. Default `-created`. |
| `search`      | string  | Filter profiles whose title starts with the given string. |
| `search_tags` | string  | Comma-separated list of tag **names**. A profile is returned only when it has **all** of the listed tags. |
| `status`      | int     | Filter by status: `0` not running, `1` running, `2` error. |
| `password`    | bool    | `true` returns only profiles with passwords; `false` returns only profiles without; omit for all. |
| `proxies`     | string  | Comma-separated list of proxy UUIDs, or the special token `@no-proxies-filter` to return only profiles without a proxy. |
| `origin_platforms` | string[] | Filter by profile origin: `desktop`, `android`, `ios` (per the official spec; parameter encoding not verified). |

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

Fetch a single profile with the full nested fingerprint. The full object is always returned — a `fields` query parameter is ignored here. `folder` is `null` when the profile is not in a folder. `status` is `0` not running, `1` running, `2` error. The official Postman sample also shows a `user_agent_changed_by_user` field inside `fingerprint`; it was not returned by the live API on 2026-11-18.

The response has one of three shapes depending on the profile's platform: desktop (below), Android (the `fingerprint` carries `device_type`/`device_model` and no `screen`, `cpu`, `ram`, `renderer`, `fonts`, `noise` or `media_devices`; the profile has no `extensions` field — see [fingerprint.md](fingerprint.md#mobile-fields)), or iOS (see [iOS Profiles](#ios-profiles)). `media_devices` is always returned in the flat form, whichever input form was used.

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
      "screen": "1440x900 @1 SDR",
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

Dates are ISO 8601 in UTC without a timezone suffix. A saved proxy in `proxy` carries `uuid`, `type`, `host`, `port`, `login`, `password`, `change_ip_url`, `external_id`, `vpn_protocol`, `syn_mode`, `title` and `profiles_count` (per the official spec); a temporary proxy has the same fields with `"uuid": ""` and no `title`/`profiles_count`. For a VPN proxy `type` is `"vpn"` and `host`/`port` come from the config's `Endpoint`; the config itself (`conf`) is not returned here:

```json
{
  "uuid": "",
  "type": "vpn",
  "host": "203.0.113.10",
  "port": 51820,
  "login": "",
  "password": "",
  "change_ip_url": null,
  "external_id": null,
  "vpn_protocol": "wireguard",
  "syn_mode": "profile_based"
}
```

### iOS Profiles

Profiles created in the Octo iOS app can be listed and read through the API, but not created: `fingerprint.os` accepts only `win`, `mac` and `android` (`"ios"` is rejected with `400`). Per the official spec, an iOS profile has no `extensions`, and its `fingerprint` is a different object:

| Field           | Type   | Notes |
|-----------------|--------|-------|
| `model`         | string | Device model. |
| `user_agent`    | string | |
| `languages`     | object | `{ "type": "ip" }` or `{ "type": "manual", "value": ["en-US", ...] }`. |
| `locale`        | object | `{ "type": "ip" }` or `{ "type": "manual", "value": "en-US" }`. |
| `webrtc_policy` | enum   | `blocked`, `realIP`, `proxyIP`. |
| `geolocation`   | object | `{ "type": "auto" }`, `{ "type": "real" }`, or `{ "type": "manual", "latitude": "...", "longitude": "...", "accuracy": "..." }` (string values). |

## Create Profile

**Endpoint**: `POST /profiles`

**Required permission:** Create profiles. Sending `password` also requires Profile passwords.

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
| `tags`            | string[] | no       | Tag **names** to attach (each 1–20 chars). Tags are referenced by name here, not by UUID. Unknown names are silently ignored. |
| `pinned_tag`      | string   | no       | Tag **name** rendered prominently in the UI. Added to `tags` if missing; an unknown name is ignored. |
| `folder`          | string   | no       | Folder UUID or name to place the profile in (see [folders.md](folders.md)). Octo 3.0+. The folder must be available to the token, otherwise `403` `no_permission`. |
| `password`        | string   | no       | Profile password (4–255 chars). Also requires the Profile passwords permission. |
| `proxy`           | object \| string \| null | no       | Saved proxy by UUID, inline temporary proxy, inline VPN, or `null`. See [Proxy Field](#proxy-field). |
| `storage_options` | object   | no       | Toggles for cookies, passwords, extensions, localstorage, history, bookmarks, serviceworkers. |
| `cookies`         | array \| string | no | JSON array, or a string in JSON, Mozilla, or Netscape format (see below). The string may be base64-encoded; string form is capped at 16 MiB. |
| `image`           | string   | no       | Profile avatar UUID, as in the `image` field of a profile. An unknown UUID falls back to the default image. |
| `extensions`      | string[] | no       | Extensions as `<id>@<version>`, exactly as the `uuid` field of [`GET /teams/extensions`](teams.md). |
| `launch_args`     | string[] | no       | Extra Chromium command-line flags. |
| `images_load_limit` | int \| null | no  | Image size limit in bytes (0–102400000); `null` disables the limit. |
| `local_cache`     | bool     | no       | Persist HTTP cache between sessions. |
| `extra_info`      | object   | no       | Arbitrary JSON **object**, accessible from extensions via `chrome.cookies.getOctoProfileExtraInfo`. Any other JSON type is rejected with `400` (`Value error, should be JSON-object`), although the official spec types it as a string. |

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
      "os_version": "14",
      "os_arch": "x86",
      "renderer": "AMD Radeon Pro 450",
      "screen": "1920x1080 @1 SDR",
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

Mobile profiles pick a `device_model` (see [fingerprint.md](fingerprint.md)); `os_version` must be one of that model's `os_versions`. `device_type` is optional, but when sent it must match the model (`400` `fingerprints.invalid_mobile_type` otherwise). Mobile profiles do not support extensions.

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

The `proxy` field on create/update accepts four forms:

- `{ "uuid": "<proxy-uuid>" }` — attach a saved proxy from [proxies.md](proxies.md). A plain string, `"proxy": "<proxy-uuid>"`, is accepted and means the same.
- `{ "type": "...", "host": "...", "port": ..., "login": "...", "password": "..." }` — a temporary proxy bound to this profile only. In `GET` responses a temporary proxy appears with `"uuid": ""` and no `title`/`profiles_count`.
- `{ "type": "vpn", "conf": "<base64 WireGuard/AmneziaWG config>", "vpn_protocol": "wireguard", "syn_mode": "profile_based" }` — a temporary VPN proxy bound to this profile only (Octo 3.1+). Only `type` and `conf` are required; `vpn_protocol` defaults to `wireguard` (the only value) and `syn_mode` to `profile_based`. See [VPN Proxies](proxies.md#vpn-proxies) for the config requirements and `syn_mode` values. In `GET` responses it appears with `"uuid": ""`, `host`/`port` taken from the config, and without `conf`; it is not listed by `GET /proxies`.
- `null` — detach the proxy. A temporary proxy is deleted in this case, as it is when the profile is switched from it to a saved proxy.

On `PATCH`, an inline proxy or VPN object updates only the passed fields of the profile's own temporary proxy, or creates one if the profile has none.

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

`extra_info` is delivered to the extension as a JSON string. In the API it must be sent as an object, e.g. `"extra_info": { "any": "value" }`.

## Update Profile

**Endpoint**: `PATCH /profiles/{uuid}`

**Required permission:** Edit profiles.

All fields are optional. The body shape matches `POST /profiles`, except that `password` is not accepted here — use [`POST /profiles/set_password`](#set-profiles-password) instead. A partial `fingerprint` object is accepted (only the listed sub-fields change), but `fingerprint.os` cannot be changed: any `fingerprint` containing `os` — even the current value — is rejected with `400` `profiles.update_error` (`You can't update os.`). `images_load_limit` is accepted here.

Clearing values:
- `tags: []` removes all tags.
- `pinned_tag: null` unpins the tag.
- `folder: null` removes the profile from its folder. A target `folder` must be available to the token, otherwise `403` `no_permission`.
- `proxy: null` detaches the proxy (see [Proxy Field](#proxy-field)).

> Updating running profiles works, but for synchronisation safety prefer to update stopped profiles.

```bash
curl -X PATCH "https://app.octobrowser.net/api/v2/automation/profiles/d9623a2be9a0431784aacc4500d7963a" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "new title",
    "description": "new description",
    "tags": ["octo"],
    "fingerprint": { "os_version": "11", "screen": "1920x1080 @1 SDR" }
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

**Required permission:** Delete profiles.

**Request Body**:
- `uuids` (string[], required) — profiles to delete, 1–100 per request.
- `skip_trash_bin` (bool, optional, default `true`) — `true` (the default) deletes the profiles permanently; `false` moves them to the trash bin, from where they can be listed with [Get Trash Bin](#get-trash-bin) and returned with [Restore Profiles](#restore-profiles).

The request has a JSON body — make sure your HTTP client sends a body with `DELETE` requests.

```bash
curl -X DELETE "https://app.octobrowser.net/api/v2/automation/profiles" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"uuids":["a4708a63d55742a09b7f1a600c248484","d7226450b9fb4bac8526c24fc3669814","9f0e1d2c3b4a49588776655443322110"], "skip_trash_bin": false}'
```

### Example Response

```json
{
  "success": true,
  "msg": "Profiles deleted",
  "data": {
    "deleted_uuids":   ["a4708a63d55742a09b7f1a600c248484"],
    "active_uuids":    ["d7226450b9fb4bac8526c24fc3669814"],
    "protected_uuids": [],
    "not_found_uuids": ["9f0e1d2c3b4a49588776655443322110"]
  },
  "code": null
}
```

The response splits the requested UUIDs into four lists:
- `deleted_uuids` — deleted (or moved to the trash bin);
- `active_uuids` — running, not deleted — stop them first and retry;
- `protected_uuids` — protected against deletion through the API (Octo 3.2+), not deleted;
- `not_found_uuids` — not in your team, or not accessible to the token.

A `200` does not mean every profile was deleted: check `deleted_uuids`. If nothing was deleted, the request returns `404` `not_found` ("Profiles not found or active") with the four lists in `data` (live-verified for the all-unknown case):

```json
{
  "success": false,
  "msg": "Profiles not found or active",
  "data": {
    "deleted_uuids": [],
    "active_uuids": [],
    "protected_uuids": [],
    "not_found_uuids": ["9f0e1d2c3b4a49588776655443322110"]
  },
  "code": "not_found"
}
```

If none of the requested profiles is accessible to the token, the request returns `403` `profiles.access_error` (per the official Postman collection).

## Get Trash Bin

List profiles in the team trash bin, newest first.

**Endpoint**: `GET /profiles/trash_bin`

**Required permission:** Delete profiles.

**Query Parameters**:
- `page` (int, optional) — zero-based page number, default `0`.
- `page_len` (int, optional) — one of `10, 25, 50, 100`, default `10`; any other value is rejected with `400`.
- `search` (string, optional) — filter by profile title; must not be empty (`?search=` returns `400` `string_too_short`).

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/profiles/trash_bin?page=0&page_len=10" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": [
    {
      "uuid": "4bbdc824762342f485bed4968533b28a",
      "title": "Profile 1",
      "deleted_at": "2026-10-27T10:15:00",
      "deleted_by": "API token (API)",
      "by_automation_api": true,
      "restore": { "paid": false, "price": "0", "free_at": null }
    },
    {
      "uuid": "4565940d5b9b41f99341fae6f5f3d855",
      "title": "Profile 2",
      "deleted_at": "2026-10-26T18:40:00",
      "deleted_by": "user@example.com",
      "by_automation_api": false,
      "restore": { "paid": true, "price": "1", "free_at": "2026-10-28T18:40:00" }
    }
  ],
  "code": null,
  "total_count": 2,
  "page": 0
}
```

- `deleted_by` — the email of the member who deleted the profile, or `"<token name> (API)"` when it was deleted with an API token; `by_automation_api` is `true` for profiles deleted through the API.
- `restore` — current restore terms. Each profile can be restored for free a limited number of times per period; after that a restore costs tokens. `paid` is `true` when restoring now costs tokens, `price` is the price in tokens as a decimal string (`"0"` when free), and `free_at` is when the next free restore becomes available (`null` if it is free now).

## Restore Profiles

Restore profiles from the trash bin. Restorable profiles are restored, the rest are skipped.

**Endpoint**: `POST /profiles/trash_bin/restore`

**Required permission:** Delete profiles.

**Request Body**:
- `uuids` (string[], required) — 1–100 per request (an empty list is rejected with `400` `too_short`).

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/profiles/trash_bin/restore" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"uuids":["4bbdc824762342f485bed4968533b28a","4565940d5b9b41f99341fae6f5f3d855"]}'
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": {
    "restored_uuids": ["4bbdc824762342f485bed4968533b28a"],
    "payment_required_uuids": ["4565940d5b9b41f99341fae6f5f3d855"],
    "not_found_uuids": []
  },
  "code": null
}
```

- `restored_uuids` — restored.
- `payment_required_uuids` — in the trash bin, but restoring costs tokens (see `restore` in [Get Trash Bin](#get-trash-bin)). Paid restores are not available through the API: these profiles stay in the trash bin; restore them in the Octo Browser client.
- `not_found_uuids` — not in your team's trash bin (including profiles that were deleted permanently).

A `200` does not mean profiles were restored: check `restored_uuids`. When nothing was restored, the request returns `400` `profiles.restore_error` with the three lists in `data`:

```json
{
  "success": false,
  "msg": "No profiles to restore",
  "data": {
    "restored_uuids": [],
    "payment_required_uuids": [],
    "not_found_uuids": ["4bbdc824762342f485bed4968533b28a"]
  },
  "code": "profiles.restore_error"
}
```

If restoring would exceed the profile limit of your plan, the request returns `403` `profiles.maximum_saved_error` and nothing is restored (per the official Postman collection). The official spec also declares `207` for a partial restore (not verified).

## Import Cookies

**Endpoint**: `POST /profiles/{uuid}/import_cookies`

**Required permission:** Create profiles.

**Request Body**: `{ "cookies": <array or string> }` — accepts the same JSON, Mozilla and Netscape formats described under [Cookie Formats](#cookie-formats). Cookies can also be uploaded as `multipart/form-data` under the `cookies` field. Cookies are applied on the next profile start. The profile must not be running (`409` `profiles.started` otherwise).

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/profiles/d9623a2be9a0431784aacc4500d7963a/import_cookies" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"cookies":[{"domain":".google.com","name":"1P_JAR","value":"2021-11-10-11","path":"/","secure":true,"httpOnly":false,"hostOnly":false,"sameSite":"no_restriction","expirationDate":1639134293.313654}]}'
```

### Example Response

```json
{ "success": true, "msg": "Cookies imported", "data": "", "code": null }
```

## Force Stop Profile

Marks a running profile as stopped without syncing. **Unsynced changes are lost.**

**Endpoint**: `POST /profiles/{uuid}/force_stop`

**Request Body**:
- `version` (int | numeric string | null, required) — running session version for an optimistic concurrency check; a positive integer or a string of digits such as `"1"`. The field must be present; pass `null` to stop the current session without the check. Omitting it (`{}`) returns a `400` validation error (`Field required`), as does a non-numeric string.

Errors: a `version` that does not match the running session returns `409` `profiles.consistency_error`; a profile that is not running returns `409` `{"success":false,"msg":"Profile is not started","data":"","code":"profiles.not_started"}`.

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/profiles/d9623a2be9a0431784aacc4500d7963a/force_stop" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"version": null}'
```

### Example Response

```json
{ "success": true, "msg": "Profile stopped", "data": "", "code": null }
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

**Required permission:** Transfer profiles.

**Request Body**:
- `uuids` (string[], required) — 1–100 entries per request.
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
{ "success": true, "msg": "Profiles transferred successfully", "data": "", "code": null }
```

A `200` means at least one profile was transferred; the rest are skipped without being listed.

## Export Profiles

Encode profiles into transferable strings.

**Endpoint**: `POST /profiles/export`

**Required permission:** Transfer profiles.

> Paid action — costs 0.5 tokens per profile. Up to 100 profiles per request; duplicate UUIDs are silently ignored.

**Request Body**:
- `uuids` (string[], required) — 1–100 per request.
- `export_proxy` (bool, required) — include the attached proxy data in the export blob. Omitting it returns `400` (`Field required`).

No other fields are accepted: an extra field such as `app_version` is rejected with `400` `extra_forbidden`.

A `200` does not mean every profile was exported: check `exported` and `failed`. The official spec also declares `207` for a partial export and `400` when nothing was exported (not verified).

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
  },
  "code": null
}
```

## List Exports

Paginated list of previously generated exports for the account.

**Endpoint**: `GET /profiles/export`

**Required permission:** Transfer profiles.

**Query Parameters**:
- `page` (int, optional) — zero-based page number, default `0`.
- `page_len` (int, optional) — one of `10, 25, 50, 100`, default `10`.

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
  },
  "code": null
}
```

> Note: this endpoint wraps its list in a nested object — the items are in `data.data`, and pagination uses `data.total` and `data.page` (not top-level `total_count`/`page`). An empty list is returned as `"data": {"data": [], "total": 0, "page": 0}`.

## Get Export

Fetch a single previously generated export.

**Endpoint**: `GET /profiles/export/{uuid}`

**Required permission:** Transfer profiles.

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
  },
  "code": null
}
```

## Import Profiles

Restore profiles from export blobs.

**Endpoint**: `POST /profiles/import`

**Required permission:** Create profiles.

> Up to 100 profiles per request.

**Request Body**:
- `data` (array, required) — up to 100 items, each in one of three forms:
  - a string — the `data` blob from [`POST /profiles/export`](#export-profiles);
  - an object `{ "data", "title", "uuid" }` — an entry from a new-format export file, passed verbatim;
  - an object `{ "data": "<json string>", "signature" }` — an entry from an old (V1) export file.
- `folder` (string, optional) — folder UUID or name to place the imported profiles in (see [folders.md](folders.md)). Octo 3.0+. The folder must be available to the token, otherwise `403` `no_permission`.

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
  "data": { "failed": [] },
  "code": null
}
```

## Set Profiles Password

Set or change the password protecting one or more profiles. The same password is applied to every listed profile. The request is all-or-nothing: if `old_password` does not match for one of the profiles, or one of them is currently running on another machine, the whole request fails with `400` and no profile is changed.

**Endpoint**: `POST /profiles/set_password`

**Required permission:** Profile passwords.

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
{ "success": true, "msg": "Password has been set for selected profiles", "data": "", "code": null }
```

## Clear Profile Password

Remove the password from a single profile. The current password must be provided; if it does not match, the request fails with `400` `profiles.password_error`.

**Endpoint**: `POST /profiles/{uuid}/clear_password`

**Required permission:** Profile passwords.

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
{ "success": true, "msg": "Password has been cleared", "data": "", "code": null }
```

## Common Errors

- **400 Bad Request** — body fails validation (see the `validation_error` object in [errors.md](errors.md)), an unsupported `os_version` for the platform (envelope with `code: "validation_error"`), a `device_model`/`device_type` mismatch (`fingerprints.invalid_mobile_model`, `fingerprints.invalid_mobile_type`), `fingerprint.os` sent on `PATCH` (`profiles.update_error`), a wrong password (`profiles.password_error`), a mass `force_stop` that stopped nothing (`profiles.stop_error`), or a trash-bin restore that restored nothing (`profiles.restore_error`).
- **403 Forbidden** — the token lacks the required permission or the `folder` is not available to it (`no_permission`), none of the profiles in `DELETE /profiles` is accessible to the token (`profiles.access_error`), or a restore would exceed the plan's profile limit (`profiles.maximum_saved_error`).
- **404 Not Found** — profile UUID does not exist, `DELETE /profiles` deleted nothing (`not_found`, with the four lists in `data`), or the `proxy` UUID is unknown or belongs to a temporary proxy (`proxy not found:`).
- **409 Conflict** — profile is locked, running (`profiles.started`, e.g. on `import_cookies`), not running on `force_stop` (`profiles.not_started`), or its `version` does not match (`profiles.consistency_error`).
- Unknown tag **names** (≤ 20 chars) in `tags[]` are not an error: the request succeeds and the tag is silently dropped (no tag is auto-created). Names longer than 20 characters return `400` `string_too_long`.
