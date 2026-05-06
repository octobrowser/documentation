# Tags API

Tags are coloured labels attached to browser profiles. They are managed independently and referenced by UUID from profile payloads.

All endpoints return the standard envelope `{ "success": bool, "msg": string, "data": ... }`.

## Get Tags

List every tag on the account.

**Endpoint**: `GET /tags`

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/tags" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": [
    {
      "uuid": "3524ff6e3f0245ffbbcb5ea3d0446a8e",
      "name": "aaaa",
      "color": "grey"
    },
    {
      "uuid": "07fd5038fc0743cd955d963a19edb3d9",
      "name": "facebook",
      "color": "blue"
    },
    {
      "uuid": "ab1391ce01aa46fcbdd9d02a4569bec4",
      "name": "google",
      "color": "yellow"
    },
    {
      "uuid": "7891009afee84952a926b03e7bc0af52",
      "name": "octo",
      "color": "orange"
    }
  ]
}
```

## Create Tag

**Endpoint**: `POST /tags`

**Request Body**:
- `name` (string, required) — tag name.
- `color` (string, optional) — one of: `grey`, `blue`, `cyan`, `orange`, `green`, `purple`, `red`, `yellow`. Defaults to `grey`. Hex colours are not accepted.

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/tags" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"supertag","color":"blue"}'
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": {
    "uuid": "ab003313e690425cb1f01e67b9b3a5da",
    "name": "supertag",
    "color": "blue"
  }
}
```

## Update Tag

**Endpoint**: `PATCH /tags/{uuid}`

Both `name` and `color` are optional; supply only the fields you want to change.

```bash
curl -X PATCH "https://app.octobrowser.net/api/v2/automation/tags/ab003313e690425cb1f01e67b9b3a5da" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"supertag1","color":"orange"}'
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": {
    "uuid": "ab003313e690425cb1f01e67b9b3a5da",
    "name": "supertag1",
    "color": "orange"
  }
}
```

## Remove Tag

**Endpoint**: `DELETE /tags/{uuid}`

```bash
curl -X DELETE "https://app.octobrowser.net/api/v2/automation/tags/ab003313e690425cb1f01e67b9b3a5da" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": ""
}
```

## Using Tags with Profiles

Profile payloads accept tags by UUID. The `tags` field on a profile is an array of tag UUIDs:

```json
{
  "title": "My Profile",
  "tags": ["3524ff6e3f0245ffbbcb5ea3d0446a8e", "ab1391ce01aa46fcbdd9d02a4569bec4"],
  "fingerprint": { "os": "win" }
}
```

### Search Profiles by Tags

`GET /profiles` accepts `search_tags`, a comma-separated list of tag UUIDs. A profile is returned only when it has **all** listed tags (logical AND, not OR).

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/profiles?page_len=10&page=0&search_tags=3524ff6e3f0245ffbbcb5ea3d0446a8e,ab1391ce01aa46fcbdd9d02a4569bec4" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

## Common Errors

- **400 Bad Request** — invalid colour, missing `name`, or malformed UUID.
- **404 Not Found** — tag UUID does not exist.
- **409 Conflict** — tag name already exists on the account.

See [errors.md](errors.md) for the standard error envelope and validation-error payload.
