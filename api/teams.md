# Teams API

Manage team-wide resources: shared browser extensions, team members (subaccounts), pending invitations, and read the team's subscription, plan usage and current API rate limits.

All endpoints return the standard envelope `{ "success": bool, "msg": string, "data": ..., "code": string | null }`. The subaccounts and invites listings additionally return `total_count`; the extensions listing does not.

Profile tasks cannot be managed through the API (per the official API FAQ).

> Team features require a team or enterprise subscription.

## Get Extensions

Returns extensions used by the team, installed in any profile.

**Endpoint**: `GET /teams/extensions`

**Query Parameters**:
- `start` (int, optional) — offset (zero-based), default `0`.
- `limit` (int, optional) — page size, `1`–`100`, default `25`.

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/teams/extensions?start=0&limit=25" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": [
    {
      "uuid": "54d6ff5042c545b990349a7a7e653e81@2.0.12",
      "name": "Google Translate",
      "version": "2.0.12"
    }
  ],
  "code": null
}
```

The extension `uuid` is the canonical extension id appended with `@<version>` (e.g. `54d6ff5042c545b990349a7a7e653e81@2.0.12`). Always use the value as reported by `GET /teams/extensions`, not the bare store id.

## Delete Extensions

Remove team-installed extensions by UUID.

**Endpoint**: `DELETE /teams/extensions`

**Required permission:** Delete extensions.

**Request Body**:
- `uuids` (string[], required) — 1 to 100 extension UUIDs per request, in the `<extension-id>@<version>` form returned by `GET /teams/extensions`.

The request has a JSON body — make sure your HTTP client sends a body with `DELETE` requests.

A `200` does not mean anything was deleted: well-formed but unknown extension ids are silently ignored (live-verified: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@1.0.0` → `200 "Extensions deleted successfully"`). Malformed ids — the extension id part must be 32 characters `a`–`p`, as in Chrome — are rejected with `400`:

```json
{"validation_error":{"body_params":[{"type":"value_error","loc":["uuids"],"msg":"Value error, Incorrect extension ids","input":["0000000000000000000000000000dead@1.0.0"]}]}}
```

> If a profile is running while the extension is deleted, the running session keeps using the extension. Once that profile stops, the extension reappears in the team's extension list. Make sure no profile is using the extensions you are about to remove.

```bash
curl -X DELETE "https://app.octobrowser.net/api/v2/automation/teams/extensions" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"uuids":["54d6ff5042c545b990349a7a7e653e81@2.0.12"]}'
```

### Example Response

```json
{ "success": true, "msg": "Extensions deleted successfully", "data": "", "code": null }```

## Get Subaccounts

List the team's members.

**Endpoint**: `GET /teams/subaccounts`

**Required permission:** Manage team.

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/teams/subaccounts" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "total_count": 1,
  "data": [
    {
      "uuid": "54d6ff5042c545b990349a7a7e653e81",
      "email": "test@octo.com",
      "master": false,
      "created_at": "2023-11-27T13:07:28",
      "permissions": {
        "manage_team": false,
        "edit_tags": false,
        "view_all_tags": false,
        "manage_action_log": false,
        "proxies":      { "create": false, "edit": false, "delete": false },
        "paid_proxies": { "create": false },
        "profiles":     { "transfer": false, "clone": false, "create": false, "edit": false, "delete": false, "passwords": false },
        "templates":    { "create": false, "edit": false, "delete": false },
        "extensions":   { "delete": false },
        "tasks":        { "view": false, "manage": false },
        "visible_tags": ["tag_name"],
        "view_all_folders": false,
        "visible_folders": [],
        "edit_folders": false,
        "view_profiles_wo_folders": false
      }
    }
  ],
  "code": null
}
```

`master: true` marks the workspace owner. `created_at` is an ISO 8601 timestamp without a timezone suffix (`YYYY-MM-DDTHH:MM:SS`).

## Create Subaccount

Invite a new member to the team. The address receives an email invitation; the subaccount becomes active once the invite is accepted.

**Endpoint**: `POST /teams/subaccounts`

**Required permission:** Manage team.

**Request Body**:
- `email` (string, required) — invitee's email.
- `permissions` (object, required) — see [Permission Reference](#permission-reference). The object itself must be present (omitting it → `400` `validation_error` `missing` at `["permissions"]`, live-verified), but any permission you do not list inside it defaults to `false`.

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/teams/subaccounts" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@octo.net",
    "permissions": {
      "manage_team": false,
      "edit_tags": false,
      "view_all_tags": false,
      "manage_action_log": false,
      "proxies":      { "create": false, "edit": false, "delete": false },
      "paid_proxies": { "create": false },
      "profiles":     { "transfer": false, "clone": false, "create": false, "edit": false, "delete": false, "passwords": false },
      "templates":    { "create": false, "edit": false, "delete": false },
      "extensions":   { "delete": false },
      "tasks":        { "view": false, "manage": false },
      "visible_tags": ["tag_name"],
      "view_all_folders": false,
      "visible_folders": [],
      "edit_folders": false,
      "view_profiles_wo_folders": false
    }
  }'
```

### Example Response

```json
{ "success": true, "msg": "Invite sent", "data": "", "code": null }```

## Update Subaccount

Change a subaccount's permissions. The subaccount is identified by `email`.

**Endpoint**: `PATCH /teams/subaccounts`

**Required permission:** Manage team.

**Request Body**: same shape as [Create Subaccount](#create-subaccount). Permissions you omit default to `false`, so always send the full permissions block when patching.

```bash
curl -X PATCH "https://app.octobrowser.net/api/v2/automation/teams/subaccounts" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@octo.net",
    "permissions": {
      "manage_team": true,
      "edit_tags": true,
      "view_all_tags": true,
      "manage_action_log": false,
      "proxies":      { "create": true, "edit": true, "delete": true },
      "paid_proxies": { "create": true },
      "profiles":     { "transfer": true, "clone": true, "create": true, "edit": true, "delete": true, "passwords": true },
      "templates":    { "create": true, "edit": true, "delete": true },
      "extensions":   { "delete": true },
      "tasks":        { "view": true, "manage": true },
      "visible_tags": [],
      "view_all_folders": true,
      "visible_folders": [],
      "edit_folders": true,
      "view_profiles_wo_folders": true
    }
  }'
```

### Example Response

```json
{
  "success": true,
  "msg": "Team member updated",
  "data": { "uuid": "d2874db6b3344506946c1bb91bd17bf8" },
  "code": null
}
```

## Delete Subaccount

Remove a team member by email.

**Endpoint**: `DELETE /teams/subaccounts`

**Required permission:** Manage team.

**Request Body**:
- `email` (string, required)

The request has a JSON body — make sure your HTTP client sends a body with `DELETE` requests.

```bash
curl -X DELETE "https://app.octobrowser.net/api/v2/automation/teams/subaccounts" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@octo.net"}'
```

### Example Response

```json
{ "success": true, "msg": "Team member deleted", "data": "", "code": null }```

## Get Invites

List pending invitations created via `POST /teams/subaccounts` that have not yet been accepted.

**Endpoint**: `GET /teams/invites`

**Required permission:** Manage team.

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/teams/invites" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "total_count": 1,
  "data": [
    { "receiver": "test_receiver@octo.net", "created_at": "2023-11-27T13:07:28" }
  ],
  "code": null
}
```

## Delete Invite

Cancel a pending invitation by recipient email.

**Endpoint**: `DELETE /teams/invites`

**Required permission:** Manage team.

**Request Body**:
- `receiver` (string, required) — email address the invite was sent to.

The request has a JSON body — make sure your HTTP client sends a body with `DELETE` requests.

```bash
curl -X DELETE "https://app.octobrowser.net/api/v2/automation/teams/invites" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"receiver":"test@octo.net"}'
```

### Example Response

```json
{ "success": true, "msg": "Invite deleted", "data": "", "code": null }```

## Get Subscription

Returns the team's subscription, balance, usage of the plan limits, and the current API rate-limit budget.

**Endpoint**: `GET /teams/subscription`

No parameters. No specific token permission is required.

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/teams/subscription" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": {
    "plan": "team",
    "expiration": "2026-11-27T00:00:00",
    "auto_renew": true,
    "balance": "125.5",
    "profiles": { "used": 120, "limit": 500 },
    "team_members": { "used": 2, "limit": 5 },
    "api_tokens": { "used": 2, "limit": 3 },
    "rate_limits": {
      "rpm": { "limit": 100, "remaining": 98, "reset_at": "2026-10-27T12:01:00" },
      "rph": { "limit": 1500, "remaining": 1460, "reset_at": "2026-10-27T12:35:00" }
    }
  },
  "code": null
}
```

| Field | Description |
|-------|-------------|
| `plan` | Plan name (e.g. `base`, `team`, `advanced`). |
| `expiration` | Subscription end date, UTC, ISO 8601 without timezone suffix. |
| `auto_renew` | Whether the subscription renews automatically. |
| `balance` | Team balance as a decimal string (e.g. `"125.5"`). |
| `profiles`, `team_members`, `api_tokens` | `{ "used", "limit" }` for each plan limit. `team_members` does not count the account owner. |
| `rate_limits.rpm`, `rate_limits.rph` | Requests per minute / per hour: `limit`, `remaining` (already counting this request) and `reset_at` (UTC) — for a moving window, when the oldest counted request expires and frees a slot; for a fixed window, when the window resets. |

The same budget is also reported in the `X-Ratelimit-*` response headers; see [rate-limiting.md](rate-limiting.md). Note that this call itself consumes one request.

## Permission Reference

Top-level boolean flags:

| Field               | Description |
|---------------------|-------------|
| `manage_team`       | Add, edit, and remove subaccounts. |
| `edit_tags`         | Create, rename, recolour, and delete tags. |
| `view_all_tags`     | See every tag on the workspace; otherwise the subaccount only sees tags listed in `visible_tags`. |
| `manage_action_log` | Access and manage the team's action log (see [action-log.md](action-log.md)). |
| `edit_folders`      | Create, rename, and delete folders (Octo 3.0+). |
| `view_all_folders`  | See every folder on the workspace; otherwise the subaccount only sees folders listed in `visible_folders`. |
| `view_profiles_wo_folders` | See profiles that are not assigned to any folder. |

Nested permission groups:

| Group           | Sub-permissions |
|-----------------|------------------|
| `proxies`       | `create`, `edit`, `delete` |
| `paid_proxies`  | `create` |
| `profiles`      | `create`, `edit`, `delete`, `transfer`, `clone`, `passwords` |
| `templates`     | `create`, `edit`, `delete` |
| `extensions`    | `delete` |
| `tasks`         | `view`, `manage` — see and manage tasks. |

`visible_tags` is an array of tag names — when `view_all_tags` is `false`, the subaccount can see only profiles tagged with at least one of these tag names. `visible_folders` works the same way for folders when `view_all_folders` is `false` (Octo 3.0+).

## Common Errors

- **400 Bad Request** — invalid email, malformed permissions, missing required field (including `permissions` on create), or malformed extension ids (`"Incorrect extension ids"`).
- **403 Forbidden** — `no_permission`: the API token lacks the required permission (Manage team / Delete extensions).
- **404 Not Found** — subaccount or invite does not exist.
- **409 Conflict** — subaccount already exists with that email, or an invite has already been issued.
