# Proxies API

Manage saved proxies. A proxy is a reusable record that can be referenced by UUID from a profile, or supplied inline on a profile payload.

All endpoints return the standard envelope `{ "success": bool, "msg": string, "data": ... }`.

## Get Proxies

**Endpoint**: `GET /proxies`

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/proxies" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": [
    {
      "uuid": "963d30cb2d7247c89da222c8a9dcab29",
      "type": "socks5",
      "port": 29801,
      "host": "localhost",
      "login": "some_login",
      "password": "some_password",
      "change_ip_url": "https://localhost/api/v1/change-ip?uuid=c26dc4d6-0de7-4aeb-bbef-de3d98362f4e",
      "external_id": null,
      "profiles_count": 0,
      "title": "example proxy"
    }
  ]
}
```

> **Security note**: proxy `login` and `password` are returned in clear text. Avoid logging full responses.

## Create Proxy

**Endpoint**: `POST /proxies`

**Request Body**:
- `type` (string, required) — one of `http`, `https`, `socks`, `socks5`, `ssh`.
- `host` (string, required)
- `port` (integer, required)
- `title` (string, required)
- `login` (string, optional)
- `password` (string, optional)
- `change_ip_url` (string, optional) — URL hit by the rotate-IP action.
- `external_id` (string, optional) — your own identifier; preserved in responses.

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/proxies" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "socks",
    "host": "localhost",
    "port": 1081,
    "login": "user",
    "password": "secret111",
    "title": "super proxy",
    "change_ip_url": "http://example.com",
    "external_id": "12345"
  }'
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": {
    "uuid": "789f4d3f898d4e10acf2bebd249fcf95",
    "type": "socks",
    "port": 1081,
    "host": "localhost",
    "login": "user",
    "password": "secret111",
    "change_ip_url": "http://localhost:1082/change_ip",
    "external_id": "my_custom_id=1",
    "profiles_count": 0,
    "title": "super proxy"
  }
}
```

## Update Proxy

**Endpoint**: `PATCH /proxies/{uuid}`

All body fields are optional; supply only the fields you want to change.

```bash
curl -X PATCH "https://app.octobrowser.net/api/v2/automation/proxies/5246b94778f549859e2e6577d98d90aa" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"renew title","port":40000}'
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": {
    "uuid": "5246b94778f549859e2e6577d98d90aa",
    "type": "socks5",
    "port": 40000,
    "host": "127.0.0.1",
    "login": "",
    "password": "",
    "change_ip_url": null,
    "external_id": null,
    "profiles_count": 0,
    "title": "renew title"
  }
}
```

## Remove Proxy

**Endpoint**: `DELETE /proxies/{uuid}`

```bash
curl -X DELETE "https://app.octobrowser.net/api/v2/automation/proxies/789f4d3f898d4e10acf2bebd249fcf95" \
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

## Using Proxies with Profiles

### Reference a Saved Proxy by UUID

```json
{
  "title": "Profile with saved proxy",
  "fingerprint": { "os": "win" },
  "proxy": { "uuid": "789f4d3f898d4e10acf2bebd249fcf95" }
}
```

### Inline Proxy on a Profile

The same proxy fields accepted by `POST /proxies` may be embedded directly inside a profile payload. The proxy is then attached to that profile only and is not added to `GET /proxies`.

```json
{
  "title": "Profile with inline proxy",
  "fingerprint": { "os": "win" },
  "proxy": {
    "type": "http",
    "host": "proxy.example.com",
    "port": 8080,
    "login": "user",
    "password": "pass"
  }
}
```

### Filter Profiles by Proxy

`GET /profiles` accepts the `proxies` query parameter — a comma-separated list of proxy UUIDs. The special token `@no-proxies-filter` returns profiles that have no proxy attached.

```bash
# Profiles attached to specific proxies
curl -X GET "https://app.octobrowser.net/api/v2/automation/profiles?page_len=10&page=0&proxies=789f4d3f898d4e10acf2bebd249fcf95,963d30cb2d7247c89da222c8a9dcab29" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"

# Profiles with no proxy
curl -X GET "https://app.octobrowser.net/api/v2/automation/profiles?page_len=10&page=0&proxies=@no-proxies-filter" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

## Proxy Types

| Value     | Description |
|-----------|-------------|
| `http`    | HTTP proxy |
| `https`   | HTTPS proxy |
| `socks`   | SOCKS4 proxy |
| `socks5`  | SOCKS5 proxy |
| `ssh`     | SSH-tunnel proxy |

## Common Errors

- **400 Bad Request** — invalid `type`, missing `host`/`port`/`title`, or malformed body.
- **404 Not Found** — proxy UUID does not exist.
- **409 Conflict** — proxy is in use by a running profile and cannot be modified or deleted.

See [errors.md](errors.md) for the standard error envelope.
