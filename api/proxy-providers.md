# Proxy Providers API

Buy and manage proxies from the proxy providers built into Octo Browser (the Proxy Shop), available through the API since Octo 3.2 (November 2026). Each provider offers one or more proxy kinds:

| Kind          | Location levels you can choose |
|---------------|--------------------------------|
| `data_center` | country |
| `residential` | country → region → city |
| `mobile`      | country → carrier (ISP) → region → city |

Traffic is counted in bytes per provider and is bought with tokens from the team balance (there is no API endpoint for buying traffic). Provider proxies are listed and managed here, separately from the saved proxies in [proxies.md](proxies.md): they do not appear in `GET /proxies`.

All endpoints return the standard envelope `{ "success": bool, "msg": string, "data": ..., "code": string | null }`. The read-only endpoints need no specific token permission.

> **Costs money**: `POST /proxy_providers/proxies` buys proxies — it creates paid proxies that consume the team's traffic with that provider, and fails with `proxy_providers.empty_balance` when none is left. Whether traffic is charged at creation or only as the proxy is used is not documented upstream. This endpoint was **not live-tested** (only its validation errors were); its success response below comes from the official spec and Postman collection. Every other endpoint on this page is read-only or only renames/deletes existing proxies.

## Typical Flow

1. `GET /proxy_providers` — pick a provider `uuid` and one of its `kinds`; check that `traffic` is above `0` and `can_create_proxy` is `true`.
2. `GET /proxy_providers/{provider_uuid}/{kind}/countries` — pick a `country_code`.
3. Optionally narrow the location:
   - `mobile`: ISPs → regions of that ISP → cities of that region.
   - `residential`: regions → cities of that region.
   - `data_center`: no further levels.
4. `POST /proxy_providers/proxies` with the chosen codes and a `quantity`.

Location codes are the provider's own and their format differs between providers (e.g. uppercase ISO country codes with numeric region codes, or lowercase slugs). Pass codes back **exactly** as returned: path codes are case-sensitive, and a wrongly cased code (e.g. `us` instead of `US`) returns an empty list rather than an error. Lookups are answered by the provider's API; cache their results instead of calling them before every purchase.

## Get Proxy Providers

Lists the proxy providers available to the team. `data` is a bare array; the response is not paginated.

**Endpoint**: `GET /proxy_providers`

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/proxy_providers" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

Each provider object:

| Field              | Type     | Description |
|--------------------|----------|-------------|
| `uuid`             | string   | Provider UUID; pass it as `provider` / `{provider_uuid}` in the other requests. |
| `name`             | string   | Display name. |
| `kinds`            | string[] | Proxy kinds the provider offers: `data_center`, `mobile`, `residential`. |
| `traffic`          | integer  | Remaining team traffic for this provider, in bytes. |
| `proxy_count`      | integer  | Number of team proxies from this provider. |
| `can_create_proxy` | bool     | Whether proxies can be created from this provider right now. |
| `can_buy_traffic`  | bool     | Whether traffic for this provider can be bought right now. |

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": [
    {
      "uuid": "9f1c2e7a4b3d4f6e8a1b2c3d4e5f6a7b",
      "name": "ExampleProxy",
      "kinds": ["residential"],
      "traffic": 5000000000,
      "proxy_count": 3,
      "can_create_proxy": true,
      "can_buy_traffic": true
    },
    {
      "uuid": "0a1b2c3d4e5f60718293a4b5c6d7e8f9",
      "name": "ExampleMobile",
      "kinds": ["mobile"],
      "traffic": 0,
      "proxy_count": 0,
      "can_create_proxy": true,
      "can_buy_traffic": true
    }
  ],
  "code": null
}
```

## Get Provider Proxies

Lists the team's proxies created from proxy providers.

**Endpoint**: `GET /proxy_providers/proxies`

| Parameter  | Type    | Description |
|------------|---------|-------------|
| `page`     | integer | Zero-based page number. Defaults to `0`. |
| `page_len` | integer | Page size: one of `10`, `25`, `50`, `100` (anything else → `400`). Defaults to `10`. |
| `provider` | string  | Only proxies of this provider `uuid`. |
| `kind`     | string  | Only proxies of this kind: `data_center`, `mobile`, `residential`. |

Unlike `GET /proxies`, this list is paginated: the response carries `total_count` and `page` next to `data`.

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/proxy_providers/proxies?page=0&page_len=25&kind=residential" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

A provider proxy has the same fields as a saved proxy in [proxies.md](proxies.md) except `conf` (`uuid`, `type`, `port`, `host`, `login`, `password`, `change_ip_url`, `external_id`, `vpn_protocol`, `syn_mode`, `title`, `profiles_count`; `vpn_protocol` and `syn_mode` are `null`), plus:

| Field      | Type   | Description |
|------------|--------|-------------|
| `provider` | object | `{ "uuid", "name" }` of the provider. |
| `kind`     | string | `data_center`, `mobile`, or `residential`. |
| `geo`      | object | Location the proxy was created for. Always has the four keys `country_code`, `region_code`, `city_code`, `isp_code`; levels that were not chosen are `null`. Codes are in the provider's own format (see [Typical Flow](#typical-flow)). |

`change_ip_url` of a provider proxy points to Octo Browser itself: `https://app.octobrowser.net/change_ip/<proxy uuid>`.

### Example Response

```json
{
  "success": true,
  "msg": "",
  "data": [
    {
      "uuid": "963d30cb2d7247c89da222c8a9dcab29",
      "type": "socks5",
      "port": 1080,
      "host": "203.0.113.10",
      "login": "user",
      "password": "pass",
      "change_ip_url": "https://app.octobrowser.net/change_ip/963d30cb2d7247c89da222c8a9dcab29",
      "external_id": null,
      "vpn_protocol": null,
      "syn_mode": null,
      "title": "DE residential 1",
      "profiles_count": 0,
      "provider": {
        "uuid": "9f1c2e7a4b3d4f6e8a1b2c3d4e5f6a7b",
        "name": "ExampleProxy"
      },
      "kind": "residential",
      "geo": {
        "country_code": "DE",
        "region_code": "101",
        "city_code": "Munich",
        "isp_code": null
      }
    }
  ],
  "code": null,
  "total_count": 1,
  "page": 0
}
```

> **Security note**: provider proxy `login` and `password` are returned in clear text. Avoid logging full responses.

## Create Provider Proxies

Buys 1–100 proxies from a proxy provider in one request. **This spends the team's provider traffic** — see the note at the top of the page.

**Endpoint**: `POST /proxy_providers/proxies`

**Required permission:** Create paid proxies.

Returns HTTP `201 Created` with the created proxies, and unknown body fields are rejected (both per the official spec, not verified).

**Request Body**:
- `provider` (string, required) — provider `uuid` from `GET /proxy_providers`.
- `kind` (string, required) — `data_center`, `mobile`, or `residential`; must be one of the provider's `kinds`.
- `country_code` (string, required) — `code` from [Get Countries](#get-countries).
- `region_code` (string or null, optional) — `code` from [Get Mobile Regions](#get-mobile-regions) or [Get Residential Regions](#get-residential-regions).
- `city_code` (string or null, optional) — `code` from [Get Mobile Cities](#get-mobile-cities) or [Get Residential Cities](#get-residential-cities).
- `isp_code` (string or null, optional, `mobile` only) — `code` from [Get Mobile ISPs](#get-mobile-isps). Omit it to get a proxy from any carrier in the country.
- `quantity` (integer, required) — 1–100.

```bash
curl -X POST "https://app.octobrowser.net/api/v2/automation/proxy_providers/proxies" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "9f1c2e7a4b3d4f6e8a1b2c3d4e5f6a7b",
    "kind": "residential",
    "country_code": "DE",
    "region_code": "101",
    "city_code": null,
    "quantity": 1
  }'
```

### Example Response

`data` is an array of the created proxies, in the same shape as [Get Provider Proxies](#get-provider-proxies) (per the official spec and Postman collection; not live-verified):

```json
{
  "success": true,
  "msg": "",
  "data": [
    {
      "uuid": "963d30cb2d7247c89da222c8a9dcab29",
      "type": "socks5",
      "port": 1080,
      "host": "203.0.113.10",
      "login": "user",
      "password": "pass",
      "change_ip_url": "https://app.octobrowser.net/change_ip/963d30cb2d7247c89da222c8a9dcab29",
      "external_id": null,
      "vpn_protocol": null,
      "syn_mode": null,
      "title": "DE residential 1",
      "profiles_count": 0,
      "provider": {
        "uuid": "9f1c2e7a4b3d4f6e8a1b2c3d4e5f6a7b",
        "name": "ExampleProxy"
      },
      "kind": "residential",
      "geo": {
        "country_code": "DE",
        "region_code": "101",
        "city_code": null,
        "isp_code": null
      }
    }
  ],
  "code": null
}
```

### Errors

| Status | `code`                          | When |
|--------|---------------------------------|------|
| 400    | `validation_error` object       | Missing `provider`/`kind`/`country_code`/`quantity`, `quantity` outside 1–100, unknown `kind` (live-verified for missing `country_code` and `quantity: 0`). |
| 400    | `proxy_providers.empty_balance` | No traffic left for this provider. |
| 400    | `proxy_providers.invalid`       | The provider does not offer this `kind`. |
| 400    | `bad_request`                   | The provider is unavailable or the location is invalid (details in `msg`). |
| 403    | `proxy.limit_reached`           | The plan's limit of provider proxies is reached. |
| 403    | `no_permission`                 | The token lacks the Create paid proxies permission. |

The business errors are documented upstream and were not reproduced live. Upstream sample:

```json
{
  "success": false,
  "msg": "Proxy provider traffic balance is empty",
  "data": "",
  "code": "proxy_providers.empty_balance"
}
```

Live validation sample (`quantity: 0`):

```json
{
  "validation_error": {
    "body_params": [
      {
        "type": "greater_than_equal",
        "loc": ["quantity"],
        "msg": "Input should be greater than or equal to 1",
        "input": 0
      }
    ]
  }
}
```

## Update Provider Proxy

Renames a provider proxy. `title` is the only field that can be changed.

**Endpoint**: `PATCH /proxy_providers/proxies/{proxy_uuid}`

**Required permission:** Edit proxies.

**Request Body**:
- `title` (string, required) — 1–255 characters. Other fields are rejected.

```bash
curl -X PATCH "https://app.octobrowser.net/api/v2/automation/proxy_providers/proxies/963d30cb2d7247c89da222c8a9dcab29" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"DE residential 1"}'
```

### Example Response

`data` is the updated proxy, in the same shape as [Get Provider Proxies](#get-provider-proxies):

```json
{
  "success": true,
  "msg": "",
  "data": {
    "uuid": "963d30cb2d7247c89da222c8a9dcab29",
    "type": "socks5",
    "port": 1080,
    "host": "203.0.113.10",
    "login": "user",
    "password": "pass",
    "change_ip_url": "https://app.octobrowser.net/change_ip/963d30cb2d7247c89da222c8a9dcab29",
    "external_id": null,
    "vpn_protocol": null,
    "syn_mode": null,
    "title": "DE residential 1",
    "profiles_count": 0,
    "provider": {
      "uuid": "9f1c2e7a4b3d4f6e8a1b2c3d4e5f6a7b",
      "name": "ExampleProxy"
    },
    "kind": "residential",
    "geo": {
      "country_code": "DE",
      "region_code": "101",
      "city_code": "Munich",
      "isp_code": null
    }
  },
  "code": null
}
```

An unknown `proxy_uuid` returns `404` (`{"success":false,"msg":"Not Found","data":"","code":"not_found"}`).

## Delete Provider Proxy

**Endpoint**: `DELETE /proxy_providers/proxies/{proxy_uuid}`

**Required permission:** Delete proxies.

```bash
curl -X DELETE "https://app.octobrowser.net/api/v2/automation/proxy_providers/proxies/963d30cb2d7247c89da222c8a9dcab29" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

### Example Response

Per the official spec and Postman, `data` is `null` (same as `DELETE /proxies`; a successful delete of a paid proxy was not live-tested):

```json
{
  "success": true,
  "msg": "",
  "data": null,
  "code": null
}
```

An unknown `proxy_uuid` returns `404` (live-verified):

```json
{
  "success": false,
  "msg": "Not Found",
  "data": "",
  "code": "not_found"
}
```

## Location Lookups

The six lookup endpoints below return `data` as a flat, unpaginated array of `{ "code", "name" }` objects. Pass `code` to the next lookup and to [Create Provider Proxies](#create-provider-proxies). A level with nothing to offer (e.g. a country without regions) returns an empty array.

They share these errors:

| Status | `code`                       | When |
|--------|------------------------------|------|
| 400    | `proxy_providers.not_exists` | Unknown provider UUID, or the provider is not available. |
| 400    | `proxy_providers.invalid`    | The provider does not offer this kind. |
| 400    | `bad_request`                | The provider's API returned an error; try again later (per upstream). |
| 400    | `validation_error` object    | `{kind}` is not `data_center`, `mobile` or `residential` (`path_params`). |

Both `proxy_providers.*` errors carry the same message (live):

```json
{
  "success": false,
  "msg": "Proxy provider is invalid, or not available",
  "data": "",
  "code": "proxy_providers.not_exists"
}
```

### Get Countries

Countries where the provider offers proxies of the given kind.

**Endpoint**: `GET /proxy_providers/{provider_uuid}/{kind}/countries`

`{kind}` is `data_center`, `mobile`, or `residential`.

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/proxy_providers/9f1c2e7a4b3d4f6e8a1b2c3d4e5f6a7b/residential/countries" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

```json
{
  "success": true,
  "msg": "",
  "data": [
    { "code": "DE", "name": "Germany" },
    { "code": "US", "name": "United States" }
  ],
  "code": null
}
```

### Get Mobile ISPs

Mobile carriers (ISPs) of the provider in the country. The ISP is optional when creating proxies.

**Endpoint**: `GET /proxy_providers/{provider_uuid}/mobile/countries/{country_code}/isps`

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/proxy_providers/0a1b2c3d4e5f60718293a4b5c6d7e8f9/mobile/countries/DE/isps" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

```json
{
  "success": true,
  "msg": "",
  "data": [
    { "code": "1a2b3c4d5e6f7a8b", "name": "ExampleTel" },
    { "code": "9c8d7e6f5a4b3c2d", "name": "SampleMobile" }
  ],
  "code": null
}
```

### Get Mobile Regions

Regions where the carrier is available in the country.

**Endpoint**: `GET /proxy_providers/{provider_uuid}/mobile/countries/{country_code}/isps/{isp_code}/regions`

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/proxy_providers/0a1b2c3d4e5f60718293a4b5c6d7e8f9/mobile/countries/DE/isps/1a2b3c4d5e6f7a8b/regions" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

```json
{
  "success": true,
  "msg": "",
  "data": [
    { "code": "101", "name": "Bavaria" },
    { "code": "102", "name": "Berlin" }
  ],
  "code": null
}
```

### Get Mobile Cities

Cities where the carrier is available in the region.

**Endpoint**: `GET /proxy_providers/{provider_uuid}/mobile/countries/{country_code}/isps/{isp_code}/regions/{region_code}/cities`

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/proxy_providers/0a1b2c3d4e5f60718293a4b5c6d7e8f9/mobile/countries/DE/isps/1a2b3c4d5e6f7a8b/regions/101/cities" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

```json
{
  "success": true,
  "msg": "",
  "data": [
    { "code": "Munich", "name": "Munich" },
    { "code": "Nuremberg", "name": "Nuremberg" }
  ],
  "code": null
}
```

### Get Residential Regions

Regions where the provider offers residential proxies in the country. Residential proxies have no ISP level.

**Endpoint**: `GET /proxy_providers/{provider_uuid}/residential/countries/{country_code}/regions`

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/proxy_providers/9f1c2e7a4b3d4f6e8a1b2c3d4e5f6a7b/residential/countries/DE/regions" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

```json
{
  "success": true,
  "msg": "",
  "data": [
    { "code": "101", "name": "Bavaria" },
    { "code": "102", "name": "Berlin" }
  ],
  "code": null
}
```

### Get Residential Cities

Cities where the provider offers residential proxies in the region.

**Endpoint**: `GET /proxy_providers/{provider_uuid}/residential/countries/{country_code}/regions/{region_code}/cities`

```bash
curl -X GET "https://app.octobrowser.net/api/v2/automation/proxy_providers/9f1c2e7a4b3d4f6e8a1b2c3d4e5f6a7b/residential/countries/DE/regions/101/cities" \
  -H "X-Octo-Api-Token: YOUR_API_TOKEN"
```

```json
{
  "success": true,
  "msg": "",
  "data": [
    { "code": "Munich", "name": "Munich" },
    { "code": "Nuremberg", "name": "Nuremberg" }
  ],
  "code": null
}
```

## Using Provider Proxies with Profiles

Provider proxies count the profiles using them (`profiles_count`), but they are not part of `GET /proxies`. The profile `proxy` field accepts the UUID of an existing proxy (see [Proxy Field](profiles.md#proxy-field)); passing a provider proxy's `uuid` there is expected to work the same way, but attaching provider proxies through the API was not verified.

## Common Errors

- **400 Bad Request** — validation failure (`quantity` outside 1–100, a missing required field, an unknown `kind`, a `page_len` other than 10/25/50/100, or an unknown body field), or one of the business errors listed above (`proxy_providers.not_exists`, `proxy_providers.invalid`, `proxy_providers.empty_balance`, `bad_request`). Validation errors have no `success`/`msg`/`data`/`code` envelope, only `validation_error`.
- **403 Forbidden** — the token lacks the required permission (`no_permission`), or the plan's provider-proxy limit is reached (`proxy.limit_reached`).
- **404 Not Found** — provider proxy UUID does not exist (`not_found`). An unknown *provider* UUID is a `400` (`proxy_providers.not_exists`), not a 404.

See [errors.md](errors.md) for the standard error envelope.
