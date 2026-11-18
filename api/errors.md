# Error Handling

The cloud API uses two distinct error envelopes: a **business error envelope** (returned for most non-2xx responses, including auth failures, missing resources, and conflicts) and a **validation envelope** (returned when the request body, query string, or path parameters are malformed).

Data types in response bodies: dates are ISO 8601 in **UTC** without a timezone suffix (`"2026-10-27T12:00:00"`); prices and balances are decimal strings (`"125.5"`, `"12.5"`).

## Business Error Envelope

```json
{
  "success": false,
  "msg": "Human-readable message",
  "code": "machine_readable_code",
  "data": ""
}
```

- `success` is always `false` on errors.
- `code` is a stable identifier you can branch on. The list below is not exhaustive.
- `data` is `""` for most errors and an object for partial-failure responses (e.g. mass `force_stop`, `DELETE /profiles` with nothing deleted, `POST /profiles/trash_bin/restore` with nothing restored).

Real samples:

```http
HTTP/2 401
{"success":false,"msg":"Invalid or missing API token.","data":"","code":"api_token"}
```

```http
HTTP/2 403
{"success":false,"msg":"No permission","data":"","code":"no_permission"}
```

```http
HTTP/2 404
{"success":false,"msg":"Cannot find profile by uuid","data":"","code":"not_found"}
```

```http
HTTP/2 404
{"success":false,"msg":"Profiles not found or active","data":{"deleted_uuids":[],"active_uuids":[],"protected_uuids":[],"not_found_uuids":["a1b2c3d4e5f60718293a4b5c6d7e8f90"]},"code":"not_found"}
```

The last sample is `DELETE /profiles` when nothing was deleted: unlike most errors, `data` carries the result lists.

Some semantic validation errors also use the business envelope, with `code` set to `"validation_error"` (distinct from the `{"validation_error": {…}}` object below). Example — creating a `mac` profile with an `os_version` the platform does not allow:

```http
HTTP/2 400
{"success":false,"msg":"OS version does not match allowed versions for the platform","data":"","code":"validation_error"}
```

## Validation Envelope

Bad query parameters, body fields, or path parameters return HTTP 400 with a different shape (no `success`/`msg`/`code` fields):

```json
{
  "validation_error": {
    "query_params": [
      {
        "type": "enum",
        "loc": ["page_len"],
        "msg": "Input should be 10, 25, 50 or 100",
        "input": "1"
      }
    ]
  }
}
```

The key says where the invalid field is: `query_params`, `body_params`, or `path_params`. Body validation example:

```json
{
  "validation_error": {
    "body_params": [
      { "type": "string_too_long", "loc": ["name"], "msg": "String should have at most 20 characters", "input": "this-name-is-way-too-long" }
    ]
  }
}
```

Path validation example (unknown proxy `kind` in a provider lookup URL):

```json
{
  "validation_error": {
    "path_params": [
      { "type": "enum", "loc": ["kind"], "msg": "Input should be 'mobile', 'residential' or 'data_center'", "input": "bogus" }
    ]
  }
}
```

When you receive a 400, check whether `validation_error` is an **object** (validation envelope). Otherwise parse the response as a business error — its `code` may itself be the string `"validation_error"`.

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200  | OK |
| 201  | Created — returned by `POST /profiles`, `POST /tags`, and `POST /proxies` (`POST /folders` returns 200). |
| 207  | Multi-Status — declared by the official OpenAPI spec for partial results of `POST /profiles/import`, `POST /profiles/export`, `POST /profiles/trash_bin/restore` and mass `POST /profiles/force_stop` (the Postman collection also documents it for mass force-stop). Not live-verified. |
| 400  | Bad request — body, query or path failed validation, or a domain rule rejected the call. Costs extra rate-limit points (see [rate-limiting.md](rate-limiting.md#cost-of-failed-requests)). |
| 401  | Invalid or missing `X-Octo-Api-Token`. |
| 403  | The token lacks the required permission (`no_permission`), the profile/folder is not available to the token, a plan limit was reached, or the API is disabled for the subscription. |
| 404  | Resource (profile, tag, proxy, subaccount, …) does not exist. |
| 409  | Conflict — resource is locked, running, or in a state that forbids the operation. Costs extra rate-limit points. |
| 415  | Unsupported Media Type — a request body was sent with a non-JSON `Content-Type` (per the official Postman collection). |
| 422  | Not used by the cloud API: validation failures are `400` with the `validation_error` envelope above, and the current official OpenAPI spec no longer declares 422 (older versions did). The **local client** API does return `422` with `{ "detail": [{ "loc": [...], "msg": "...", "type": "..." }] }` — see [local-client.md](local-client.md#error-responses). |
| 429  | Rate limit exceeded; see [rate-limiting.md](rate-limiting.md). |
| 5xx  | Server-side issue. Retry with exponential backoff. |

## Error Code Reference

The `code` field on the business error envelope. Codes prefixed with a domain (`profiles.`, `tags.`, …) are scoped to that resource.

### General

| Code | Meaning |
|------|---------|
| `api_token`         | Invalid or missing `X-Octo-Api-Token`. |
| `not_found`         | Resource UUID does not exist (also returned for an unknown or temporary proxy UUID in a profile's `proxy` field: `proxy not found:`). |
| `no_permission`     | The API token (or its folder scope) does not allow this action. See [API Token Permissions](authentication.md#api-token-permissions). |
| `validation_error`  | Semantic validation failed (business envelope form, e.g. mac `os_version` not allowed for the platform). Not to be confused with the `validation_error` object of the validation envelope. |
| `limit_reached`     | Resource limit reached on the current subscription. |
| `already_exists`    | Conflict — a record with the same key already exists. |
| `internal_error`    | Server-side fault. Retry. |
| `unknown_error`     | Unclassified failure (from the OpenAPI spec's `ErrorCode` enum). |
| `no_tokens`         | No API token exists for the workspace (from the OpenAPI spec's `ErrorCode` enum). |
| `rate_limit_exceeded` | RPM/RPH bucket empty. See [rate-limiting.md](rate-limiting.md). |

### Profiles

| Code | Meaning |
|------|---------|
| `profiles.started`               | Profile is already running (`409`, e.g. `POST /profiles/{uuid}/import_cookies` on a running profile). |
| `profiles.not_started`           | Profile is not running (`409`, e.g. `POST /profiles/{uuid}/force_stop` on a stopped profile: `"Profile is not started"`). |
| `profiles.access_error`          | `DELETE /profiles`: none of the requested profiles is accessible to the token (`403`). |
| `profiles.maximum_saved_error`   | `POST /profiles/trash_bin/restore` would exceed the plan's profile limit; nothing is restored (`403`). |
| `profiles.restore_error`         | `POST /profiles/trash_bin/restore` restored nothing (`400`, `"No profiles to restore"`). `data` carries `restored_uuids`, `payment_required_uuids`, `not_found_uuids`. |
| `profiles.stop_error`            | Bulk force-stop stopped none of the profiles (`400`). `data.failed` lists the offending UUIDs. |
| `profiles.consistency_error`     | `version` passed to `force_stop` does not match the server-side version. |
| `profiles.update_error`          | Update payload was rejected, e.g. `fingerprint.os` on `PATCH /profiles/{uuid}` (`You can't update os.`). |
| `profiles.password_error`        | Password set/clear failed (wrong `old_password`/`password`, or a listed profile is running on another machine); nothing is changed. |
| `profiles.invalid_cookie`        | Cookies field is not in JSON, Mozilla, or Netscape format. |
| `profiles.transfer_error`        | Generic transfer failure. |
| `profiles.transfer_no_receiver`  | `receiver_email` is not a member of the workspace. |
| `profiles.transfer_no_profiles`  | None of the supplied UUIDs are eligible for transfer. |
| `profiles.export_error`          | Export operation failed. |
| `profiles.export_limit_exceeded` | Export rate or volume limit reached. |
| `profiles.import_error`          | Import operation failed. |
| `profiles.import_limit_exceeded` | Import rate or volume limit reached. |
| `profiles.import_no_valid_profiles` | None of the supplied export blobs decoded into valid profiles. |

### Other Resources

| Code | Meaning |
|------|---------|
| `fingerprints.invalid`            | Fingerprint object failed server-side validation. |
| `fingerprints.invalid_mobile_model` | `device_model` is unknown, or the chosen `os_version` is not in that model's `os_versions` list. |
| `fingerprints.invalid_mobile_type` | Android `fingerprint.device_type` is not valid or does not match the chosen `device_model` (`400`, `"invalid mobile type"`). |
| `subscriptions.inactive`          | Workspace has no active subscription. |
| `proxy_providers.empty_balance`   | No traffic left for this provider (`400`, `POST /proxy_providers/proxies`). |
| `proxy_providers.not_exists`      | Unknown or unavailable proxy provider UUID (`400`, not 404; `"Proxy provider is invalid, or not available"`). |
| `proxy_providers.invalid`         | The provider does not offer the requested proxy kind (`400`, same `msg` as above). |
| `proxy.vpn_field_not_applicable`  | `PATCH /proxies/{uuid}` on a VPN proxy with connection fields such as `host` or `login` (`400`, `"Connection fields cannot be set on a VPN proxy"`). |
| `proxy.limit_reached`             | The plan limit of provider proxies is reached (`403`, `POST /proxy_providers/proxies`; per the official Postman collection). |
| `proxy.maximum_saved_error`       | Proxy quota reached on the subscription. |

## Handling Errors in Code

```python
import time
import requests

def call(method, url, headers, max_retries=3, **kwargs):
    for attempt in range(max_retries):
        response = requests.request(method, url, headers=headers, **kwargs)

        if response.status_code == 429:
            time.sleep(int(response.headers.get("Retry-After", "1")))
            continue

        if response.status_code >= 500:
            time.sleep(2 ** attempt)
            continue

        body = response.json()
        if response.ok and body.get("success"):
            return body

        # Validation envelope? (the business envelope can also carry code "validation_error")
        if isinstance(body.get("validation_error"), dict):
            raise ValueError(f"Validation failed: {body['validation_error']}")

        # Business error
        code = body.get("code")
        msg  = body.get("msg")
        if code == "profiles.started":
            raise RuntimeError("Profile is running — stop it first.")
        if code == "limit_reached":
            raise RuntimeError("Subscription limit reached.")
        raise RuntimeError(f"{response.status_code} {code}: {msg}")

    raise RuntimeError("Exhausted retries")
```

## Debugging Tips

- Log `x-trace-id` from the response headers — Octo Browser support uses it to look up the call server-side.
- For 400s, inspect the `validation_error` object first; it pinpoints the offending field with `loc`. Don't retry a 400 unchanged — it costs extra rate-limit points.
- For 429s, slow your request rate before retrying; never tight-loop on `Retry-After: 0` if the body still says you are rate-limited.
- For 5xx, retry with exponential backoff. If the failure persists, file a support ticket including the trace id.
