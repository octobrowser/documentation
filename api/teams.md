# Teams API

Manage team-wide resources: shared browser extensions, team members (subaccounts), and pending invitations.

All endpoints return the standard envelope `{ "success": bool, "msg": string, "data": ... }`. Listing endpoints additionally return `total_count`.

> Team features require a team or enterprise subscription.

## Get Extensions

Returns extensions used by the team, installed in any profile.

**Endpoint**: `GET /teams/extensions`

**Query Parameters**:
- `start` (int, optional) — offset (zero-based).
- `limit` (int, optional) — page size, maximum `100`.

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
  ]
}
```

The extension `uuid` is the canonical extension id appended with `@<version>`.

## Delete Extensions

Remove team-installed extensions by UUID.

**Endpoint**: `DELETE /teams/extensions`

**Request Body**:
- `uuids` (string[], required) — up to 100 extension UUIDs per request.

> If a profile is running while the extension is deleted, the running session keeps using the extension. Once that profile stops, the extension reappears in the team's extension list. Make sure no profile is using the extensions you are about to remove.

```bash
curl -X DELETE "https://app.octobrowser.net/api/v2/automation/teams/extensions" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"uuids":["54d6ff5042c545b990349a7a7e653e81@2.0.12"]}'
```

### Example Response

```json
{ "success": true, "msg": "Extensions deleted successfully", "data": "" }
```

## Get Subaccounts

List the team's members.

**Endpoint**: `GET /teams/subaccounts`

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
      "created_at": "2023-11-27 13:07:28",
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
        "visible_tags": ["tag_name"]
      }
    }
  ]
}
```

`master: true` marks the workspace owner.

## Create Subaccount

Invite a new member to the team. The address receives an email invitation; the subaccount becomes active once the invite is accepted.

**Endpoint**: `POST /teams/subaccounts`

**Request Body**:
- `email` (string, required) — invitee's email.
- `permissions` (object, optional) — see [Permission Reference](#permission-reference). Any permission you do not list defaults to `false`.

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
      "visible_tags": ["tag_name"]
    }
  }'
```

### Example Response

```json
{ "success": true, "msg": "Invite sent", "data": "" }
```

## Update Subaccount

Change a subaccount's permissions. The subaccount is identified by `email`.

**Endpoint**: `PATCH /teams/subaccounts`

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
      "visible_tags": []
    }
  }'
```

### Example Response

```json
{
  "success": true,
  "msg": "Team member updated",
  "data": { "uuid": "d2874db6b3344506946c1bb91bd17bf8" }
}
```

## Delete Subaccount

Remove a team member by email.

**Endpoint**: `DELETE /teams/subaccounts`

**Request Body**:
- `email` (string, required)

```bash
curl -X DELETE "https://app.octobrowser.net/api/v2/automation/teams/subaccounts" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@octo.net"}'
```

### Example Response

```json
{ "success": true, "msg": "Team member deleted", "data": "" }
```

## Get Invites

List pending invitations created via `POST /teams/subaccounts` that have not yet been accepted.

**Endpoint**: `GET /teams/invites`

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
    { "receiver": "test_receiver@octo.net", "created_at": "2023-11-27 13:07:28" }
  ]
}
```

## Delete Invite

Cancel a pending invitation by recipient email.

**Endpoint**: `DELETE /teams/invites`

**Request Body**:
- `receiver` (string, required) — email address the invite was sent to.

```bash
curl -X DELETE "https://app.octobrowser.net/api/v2/automation/teams/invites" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"receiver":"test@octo.net"}'
```

### Example Response

```json
{ "success": true, "msg": "Invite deleted", "data": "" }
```

## Permission Reference

Top-level boolean flags:

| Field               | Description |
|---------------------|-------------|
| `manage_team`       | Add, edit, and remove subaccounts. |
| `edit_tags`         | Create, rename, recolour, and delete tags. |
| `view_all_tags`     | See every tag on the workspace; otherwise the subaccount only sees tags listed in `visible_tags`. |
| `manage_action_log` | Access and manage the team's action log. |

Nested permission groups:

| Group           | Sub-permissions |
|-----------------|------------------|
| `proxies`       | `create`, `edit`, `delete` |
| `paid_proxies`  | `create` |
| `profiles`      | `create`, `edit`, `delete`, `transfer`, `clone`, `passwords` |
| `templates`     | `create`, `edit`, `delete` |
| `extensions`    | `delete` |
| `tasks`         | `view`, `manage` |

`visible_tags` is an array of tag names — when `view_all_tags` is `false`, the subaccount can see only profiles tagged with at least one of these tag names.

## Common Errors

- **400 Bad Request** — invalid email, malformed permissions, or missing required field.
- **403 Forbidden** — the calling token does not have `manage_team` permission.
- **404 Not Found** — subaccount, invite, or extension UUID does not exist.
- **409 Conflict** — subaccount already exists with that email, or an invite has already been issued.
