# Proxies API

Manage saved proxies. A proxy is a reusable record that can be referenced by UUID from a profile, or supplied inline on a profile payload.

A saved proxy is either a regular proxy (`http`, `https`, `socks`, `socks5`, `ssh`) or a VPN tunnel (`type: "vpn"`) defined by a WireGuard or AmneziaWG (AWG) configuration file (Octo 3.1+). Proxies bought from the providers built into Octo Browser (the Proxy Shop) are managed separately and do not appear in `GET /proxies` — see [proxy-providers.md](proxy-providers.md).

All endpoints return the standard envelope `{ "success": bool, "msg": string, "data": ..., "code": string | null }`.

## Get Proxies

**Endpoint**: `GET /proxies`

Returns all saved proxies as a bare array (no pagination). Every item carries `conf`, `vpn_protocol` and `syn_mode`; on regular proxies they are `null`. On VPN proxies `conf` holds the full base64-encoded configuration, `login` and `password` are `""`, and `host`/`port` are taken from the config's `Endpoint` line.

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
      "conf": null,
      "uuid": "963d30cb2d7247c89da222c8a9dcab29",
      "type": "socks5",
      "port": 29801,
      "host": "localhost",
      "login": "some_login",
      "password": "some_password",
      "change_ip_url": "https://localhost/api/v1/change-ip?uuid=c26dc4d6-0de7-4aeb-bbef-de3d98362f4e",
      "external_id": null,
      "vpn_protocol": null,
      "syn_mode": null,
      "title": "example proxy",
      "profiles_count": 0
    },
    {
      "conf": "W0ludGVyZmFjZV0KUHJpdmF0ZUtleSA9IEFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUE9CkFkZHJlc3MgPSAxMC4wLjAuMi8zMgoKW1BlZXJdClB1YmxpY0tleSA9IEJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkI9CkFsbG93ZWRJUHMgPSAwLjAuMC4wLzAKRW5kcG9pbnQgPSAxOTIuMC4yLjE6NTE4MjAK",
      "uuid": "23b512d979394d4097c5a6ddf04217b0",
      "type": "vpn",
      "port": 51820,
      "host": "192.0.2.1",
      "login": "",
      "password": "",
      "change_ip_url": null,
      "external_id": null,
      "vpn_protocol": "wireguard",
      "syn_mode": "profile_based",
      "title": "my-vpn-proxy",
      "profiles_count": 0
    }
  ],
  "code": null
}
```

> **Security note**: proxy `login` and `password` are returned in clear text, and a VPN proxy's `conf` decodes to the full WireGuard/AmneziaWG config including the client `PrivateKey`. Avoid logging full responses.

## Create Proxy

**Endpoint**: `POST /proxies`

**Required permission:** Create proxies.

Returns HTTP `201 Created`. Unknown body fields are rejected. The body has two forms, chosen by `type`: the regular form below and the [VPN form](#vpn-proxies). Validation errors name the form in `loc` — `["plain", ...]` for the regular form, `["vpn", ...]` for the VPN form.

**Request Body** (regular form):
- `type` (string, required) — one of `http`, `https`, `socks`, `socks5`, `ssh` (or `vpn` for the VPN form).
- `host` (string, required) — an IPv4/IPv6 address or a hostname of 4–253 characters.
- `port` (integer, required) — 0–65535.
- `title` (string, required) — 1–255 characters.
- `login` (string, optional) — up to 255 characters.
- `password` (string, optional) — up to 255 characters.
- `change_ip_url` (string, optional) — URL hit by the rotate-IP action; a valid URI, 1–65536 characters.
- `external_id` (string, optional) — your own identifier, up to 255 characters; preserved in responses.

**Response**: the created proxy object, including `uuid`, `profiles_count` (number of profiles using the proxy, `0` for a new proxy), and `conf`/`vpn_protocol`/`syn_mode` (`null` for a regular proxy).

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
    "conf": null,
    "uuid": "789f4d3f898d4e10acf2bebd249fcf95",
    "type": "socks",
    "port": 1081,
    "host": "localhost",
    "login": "user",
    "password": "secret111",
    "change_ip_url": "http://example.com",
    "external_id": "12345",
    "vpn_protocol": null,
    "syn_mode": null,
    "title": "super proxy",
    "profiles_count": 0
  },
  "code": null
}
```

### VPN Proxies

Send `"type": "vpn"` to create a VPN proxy from a WireGuard or AmneziaWG configuration file.

**Request Body** (VPN form):
- `type` (string, required) — `vpn`.
- `title` (string, required) — 1–255 characters.
- `conf` (string, required) — the configuration file, base64-encoded UTF-8 text; up to 16 KB before encoding (at most 21848 characters encoded). It must contain an `Endpoint = host:port` line: the proxy's `host` and `port` are read from it.
- `syn_mode` (string, optional) — the TCP/IP (SYN) fingerprint the tunnel emulates; default `profile_based`. See the table below.
- `vpn_protocol` (string, optional) — `wireguard`, the only accepted value and the default. Use `wireguard` for AmneziaWG configs too.
- `external_id` (string, optional) — your own identifier, up to 255 characters.

`host`, `port`, `login`, `password` and `change_ip_url` are not accepted in the VPN form (`400`, `extra_forbidden`): the endpoint comes from the config, and a tunnel has no credentials or rotation URL. In responses a VPN proxy has `login`/`password` `""` and `change_ip_url` `null`.

`syn_mode` values:

| Value           | Meaning |
|-----------------|---------|
| `profile_based` | Emulate the OS of the profile the proxy is attached to (default). |
| `win`           | Always emulate Windows, whatever the profile's OS. |
| `mac`           | Always emulate macOS, whatever the profile's OS. |
| `android`       | Always emulate Android, whatever the profile's OS. |
| `real`          | Keep the real TCP/IP stack of the machine running the browser. |

Encode the config file as a single base64 line, e.g. `base64 -w0 wg0.conf` (Linux) or `base64 -i wg0.conf` (macOS). The `conf` in the example below decodes to:

```text
[Interface]
PrivateKey = AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=
Address = 10.0.0.2/32

[Peer]
PublicKey = BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=
AllowedIPs = 0.0.0.0/0
Endpoint = 192.0.2.1:51820
```

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/proxies" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "vpn",
    "title": "my-vpn-proxy",
    "conf": "W0ludGVyZmFjZV0KUHJpdmF0ZUtleSA9IEFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUE9CkFkZHJlc3MgPSAxMC4wLjAuMi8zMgoKW1BlZXJdClB1YmxpY0tleSA9IEJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkI9CkFsbG93ZWRJUHMgPSAwLjAuMC4wLzAKRW5kcG9pbnQgPSAxOTIuMC4yLjE6NTE4MjAK",
    "syn_mode": "profile_based"
  }'
```

#### Example Response

The created VPN proxy, with `conf` echoed back:

```json
{
  "success": true,
  "msg": "",
  "data": {
    "conf": "W0ludGVyZmFjZV0KUHJpdmF0ZUtleSA9IEFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUE9CkFkZHJlc3MgPSAxMC4wLjAuMi8zMgoKW1BlZXJdClB1YmxpY0tleSA9IEJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkI9CkFsbG93ZWRJUHMgPSAwLjAuMC4wLzAKRW5kcG9pbnQgPSAxOTIuMC4yLjE6NTE4MjAK",
    "uuid": "23b512d979394d4097c5a6ddf04217b0",
    "type": "vpn",
    "port": 51820,
    "host": "192.0.2.1",
    "login": "",
    "password": "",
    "change_ip_url": null,
    "external_id": null,
    "vpn_protocol": "wireguard",
    "syn_mode": "profile_based",
    "title": "my-vpn-proxy",
    "profiles_count": 0
  },
  "code": null
}
```

#### VPN Validation Errors

All are `400` with a `validation_error.body_params` list:

| Problem | `type` / `loc` | `msg` |
|---------|----------------|-------|
| `conf` missing | `missing` / `["vpn","conf"]` | `Field required` |
| `conf` is not base64 | `value_error` / `["vpn","conf"]` | ``Value error, Config must be base64-encoded UTF-8 text`` |
| No `Endpoint` line in the config | `value_error` / `["vpn","conf"]` | ``Value error, Config has no `Endpoint = host:port` `` |
| `vpn_protocol` other than `wireguard` | `enum` / `["vpn","vpn_protocol"]` | `Input should be 'wireguard'` |
| Unknown `syn_mode` | `enum` / `["vpn","syn_mode"]` | `Input should be 'profile_based', 'win', 'mac', 'android' or 'real'` |
| `host`, `port`, `login`, … sent | `extra_forbidden` / `["vpn","host"]` | `Extra inputs are not permitted` |

```json
{
  "validation_error": {
    "body_params": [
      {
        "type": "extra_forbidden",
        "loc": ["vpn", "host"],
        "msg": "Extra inputs are not permitted",
        "input": "192.0.2.10"
      }
    ]
  }
}
```

## Update Proxy

**Endpoint**: `PATCH /proxies/{uuid}`

**Required permission:** Edit proxies.

All body fields are optional; supply only the fields you want to change. Unknown fields are rejected. As with create, the body has a regular and a VPN form.

**Request Body** (regular form):
- `type` (string) — `http`, `https`, `socks`, `socks5`, `ssh`; or `vpn` to convert the proxy into a VPN proxy (then use the VPN form).
- `title` (string) — 1–255 characters.
- `host` (string) — IPv4/IPv6 address or hostname.
- `port` (integer) — 0–65535.
- `login`, `password` (string) — up to 255 characters each; per upstream, an empty string clears the value (not live-verified).
- `change_ip_url` (string).
- `external_id` (string) — up to 255 characters.

**Request Body** (VPN form):
- `type` (string) — `vpn`. Required only when converting a regular proxy; can be omitted for a proxy that is already VPN.
- `conf` (string) — new base64-encoded config with an `Endpoint = host:port` line. Required when converting a regular proxy. Replaces the stored config: `host` and `port` are re-read from it and, per upstream, the last proxy-check result is reset.
- `title` (string) — 1–255 characters.
- `syn_mode` (string) — `profile_based`, `win`, `mac`, `android` or `real`.
- `vpn_protocol` (string) — `wireguard`.
- `external_id` (string) — up to 255 characters.

Connection fields (`host`, `port`, `login`, `password`, `change_ip_url`) cannot be set on a VPN proxy:

```json
{
  "success": false,
  "msg": "Connection fields cannot be set on a VPN proxy",
  "data": "",
  "code": "proxy.vpn_field_not_applicable"
}
```

**Response**: the updated proxy, **without** `title` and `profiles_count` (live-verified for VPN proxies; the official spec declares the same short shape for regular proxies).

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
    "conf": null,
    "uuid": "5246b94778f549859e2e6577d98d90aa",
    "type": "socks5",
    "port": 40000,
    "host": "127.0.0.1",
    "login": "",
    "password": "",
    "change_ip_url": null,
    "external_id": null,
    "vpn_protocol": null,
    "syn_mode": null
  },
  "code": null
}
```

Changing the fingerprint mode of a VPN proxy:

```bash
curl -X PATCH "https://app.octobrowser.net/api/v2/automation/proxies/23b512d979394d4097c5a6ddf04217b0" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"syn_mode":"mac"}'
```

```json
{
  "success": true,
  "msg": "",
  "data": {
    "conf": "W0ludGVyZmFjZV0KUHJpdmF0ZUtleSA9IEFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUE9CkFkZHJlc3MgPSAxMC4wLjAuMi8zMgoKW1BlZXJdClB1YmxpY0tleSA9IEJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkI9CkFsbG93ZWRJUHMgPSAwLjAuMC4wLzAKRW5kcG9pbnQgPSAxOTIuMC4yLjE6NTE4MjAK",
    "uuid": "23b512d979394d4097c5a6ddf04217b0",
    "type": "vpn",
    "port": 51820,
    "host": "192.0.2.1",
    "login": "",
    "password": "",
    "change_ip_url": null,
    "external_id": null,
    "vpn_protocol": "wireguard",
    "syn_mode": "mac"
  },
  "code": null
}
```

## Remove Proxy

**Endpoint**: `DELETE /proxies/{uuid}`

**Required permission:** Delete proxies.

```bash
curl -X DELETE "https://app.octobrowser.net/api/v2/automation/proxies/789f4d3f898d4e10acf2bebd249fcf95" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": null,
  "code": null
}
```

Deleting an unknown or already deleted proxy returns `404`:

```json
{
  "success": false,
  "msg": "Not Found",
  "data": "",
  "code": "not_found"
}
```

## Using Proxies with Profiles

The `proxy` field of a profile payload (`POST /profiles`, `PATCH /profiles/{uuid}`) accepts four forms: a saved-proxy UUID, an inline proxy object, an inline VPN object, or `null` (see [Proxy Field](profiles.md#proxy-field)).

### Reference a Saved Proxy by UUID

Pass the UUID either as a plain string or as an object with a `uuid` key:

```json
{
  "title": "Profile with saved proxy",
  "fingerprint": { "os": "win" },
  "proxy": "789f4d3f898d4e10acf2bebd249fcf95"
}
```

```json
{
  "title": "Profile with saved proxy",
  "fingerprint": { "os": "win" },
  "proxy": { "uuid": "789f4d3f898d4e10acf2bebd249fcf95" }
}
```

An unknown UUID is rejected with `404`:

```json
{
  "success": false,
  "msg": "proxy not found:",
  "data": "",
  "code": "not_found"
}
```

### Inline Proxy on a Profile

The same proxy fields accepted by `POST /proxies` may be embedded directly inside a profile payload. The proxy is then attached to that profile only and is not added to `GET /proxies`. In `GET /profiles/{uuid}` such a temporary proxy is returned with `"uuid": ""` and without `title` or `profiles_count`.

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

### Inline VPN Proxy on a Profile

A temporary VPN proxy can be embedded the same way: `type` (`"vpn"`) and `conf` are required; `syn_mode` and `vpn_protocol` are optional with the same values and defaults as in [VPN Proxies](#vpn-proxies). The inline form has no `title` or `external_id`.

```json
{
  "title": "Profile with inline VPN",
  "fingerprint": { "os": "win" },
  "proxy": {
    "type": "vpn",
    "conf": "W0ludGVyZmFjZV0KUHJpdmF0ZUtleSA9IEFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUE9CkFkZHJlc3MgPSAxMC4wLjAuMi8zMgoKW1BlZXJdClB1YmxpY0tleSA9IEJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkI9CkFsbG93ZWRJUHMgPSAwLjAuMC4wLzAKRW5kcG9pbnQgPSAxOTIuMC4yLjE6NTE4MjAK"
  }
}
```

The proxy is not listed in `GET /proxies`. `GET /profiles/{uuid}` returns it with `"uuid": ""`, `host`/`port` parsed from the config, and **no `conf`** — the config cannot be read back from the profile:

```json
{
  "uuid": "",
  "type": "vpn",
  "port": 51820,
  "host": "192.0.2.1",
  "login": "",
  "password": "",
  "change_ip_url": null,
  "external_id": null,
  "vpn_protocol": "wireguard",
  "syn_mode": "profile_based"
}
```

### Detach a Proxy

Send `"proxy": null` on `PATCH /profiles/{uuid}`; the profile's `proxy` then reads `null`.

```json
{ "proxy": null }
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
| `vpn`     | WireGuard / AmneziaWG tunnel defined by a base64 `conf` (see [VPN Proxies](#vpn-proxies)) |

## Bulk Import Tip

Upstream example scripts import saved proxies from a `.txt` file, one proxy per line, fields in this exact order and separated by `;`:

```text
protocol;host;port;login;password;title;change_ip_url
```

`change_ip_url` is optional; the scripts accept the protocols `socks5`, `http`, and `ssh`. Each line maps directly onto a `POST /proxies` body.

## Common Errors

- **400 Bad Request** — invalid `type`, missing `host`/`port`/`title`, out-of-range `port`, unknown field, or malformed body. For VPN proxies: missing or invalid `conf`, no `Endpoint` line, unsupported `vpn_protocol`/`syn_mode`, or connection fields sent (see [VPN Validation Errors](#vpn-validation-errors)); on `PATCH`, connection fields on a VPN proxy → `proxy.vpn_field_not_applicable`.
- **403 Forbidden** — `no_permission`: the API token lacks the Create proxies, Edit proxies or Delete proxies permission.
- **404 Not Found** — proxy UUID does not exist (`not_found`).
- **409 Conflict** — proxy is in use by a running profile and cannot be modified or deleted.

See [errors.md](errors.md) for the standard error envelope.
