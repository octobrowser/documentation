# Error Handling

The cloud API uses two distinct error envelopes: a **business error envelope** (returned for most non-2xx responses, including auth failures, missing resources, and conflicts) and a **validation envelope** (returned when the request body or query string is malformed).

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
- `data` is `""` for most errors and an object for partial-failure responses (e.g. mass `force_stop`).

Real samples:

```http
HTTP/2 401
{"success":false,"msg":"Invalid or missing API token.","data":"","code":"api_token"}
```

```http
HTTP/2 404
{"success":false,"msg":"Cannot find profile by uuid","data":"","code":"not_found"}
```

## Validation Envelope

Bad query parameters or body fields return HTTP 400 with a different shape:

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

Body validation uses the same shape, replacing `query_params` with `body_params`:

```json
{
  "validation_error": {
    "body_params": [
      { "type": "string_too_long", "loc": ["name"], "msg": "String should have at most 20 characters", "input": "this-name-is-way-too-long" }
    ]
  }
}
```

When you receive a 400, look for `validation_error` first. If it is missing, parse the response as a business error.

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200  | OK |
| 400  | Bad request — body or query failed validation, or a domain rule rejected the call. |
| 401  | Invalid or missing `X-Octo-Api-Token`. |
| 403  | The token is valid but the subaccount lacks the required permission, or a quota was reached. |
| 404  | Resource (profile, tag, proxy, subaccount, …) does not exist. |
| 409  | Conflict — resource is locked, running, or in a state that forbids the operation. |
| 422  | Less common variant of 400 returned by some FastAPI validators. The body is `{ "detail": [{ "loc": [...], "msg": "...", "type": "..." }] }`. |
| 429  | Rate limit exceeded; see [rate-limiting.md](rate-limiting.md). |
| 5xx  | Server-side issue. Retry with exponential backoff. |

## Error Code Reference

The `code` field on the business error envelope. Codes prefixed with a domain (`profiles.`, `tags.`, …) are scoped to that resource.

### General

| Code | Meaning |
|------|---------|
| `api_token`         | Invalid or missing `X-Octo-Api-Token`. |
| `not_found`         | Resource UUID does not exist. |
| `no_permission`     | Subaccount does not have permission for this action. |
| `limit_reached`     | Resource limit reached on the current subscription. |
| `already_exists`    | Conflict — a record with the same key already exists. |
| `internal_error`    | Server-side fault. Retry. |
| `rate_limit_exceeded` | RPM/RPH bucket empty. See [rate-limiting.md](rate-limiting.md). |

### Profiles

| Code | Meaning |
|------|---------|
| `profiles.started`               | Profile is already running. |
| `profiles.not_started`           | Profile is not running. |
| `profiles.stop_error`            | Bulk force-stop had at least one failure. `data.failed` lists the offending UUIDs. |
| `profiles.consistency_error`     | `version` passed to `force_stop` does not match the server-side version. |
| `profiles.update_error`          | Update payload was rejected. |
| `profiles.password_error`        | Password set/clear failed (wrong `old_password` or missing password). |
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
| `subscriptions.inactive`          | Workspace has no active subscription. |
| `proxy_providers.empty_balance`   | Built-in proxy provider has no balance. |
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

        # Validation error?
        if "validation_error" in body:
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
- For 400s, inspect `validation_error` first; it pinpoints the offending field with `loc`.
- For 429s, slow your request rate before retrying; never tight-loop on `Retry-After: 0` if the body still says you are rate-limited.
- For 5xx, retry with exponential backoff. If the failure persists, file a support ticket including the trace id.
