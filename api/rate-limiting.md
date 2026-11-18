# Rate Limiting

The cloud API enforces a Requests-Per-Minute (RPM) and Requests-Per-Hour (RPH) budget. Limits are **shared across the whole team** — calls made with any of the team's API tokens (and by any subaccount) draw from the same bucket. Repeatedly ignoring `429` responses will cause us to enforce stricter limits on the team.

## Limits by Subscription

| Plan      | RPM                          | RPH                                |
|-----------|------------------------------|------------------------------------|
| Base      | 50                           | 500                                |
| Team      | 100                          | 1,500                              |
| Advanced  | 200, expandable up to 1,000  | 3,000, expandable up to 50,000     |

For limits beyond 1,000 RPM or 50,000 RPH, contact Octo Browser Technical Support.

## Point Costs of Local Client Operations

Local client API calls (`localhost:58888`) are charged against the same RPM/RPH budget as cloud calls:

| Local operation | Cost |
|-----------------|------|
| `POST /api/profiles/start` | 1 request |
| `POST /api/profiles/stop` | 1 request |
| `POST /api/profiles/password` (set) | 1 request |
| `DELETE /api/profiles/password` | 1 request |
| `POST /api/profiles/force_stop` | 2 requests |
| `POST /api/profiles/one_time/start` | 4 requests |

The following local requests are **not counted** toward the limits: List Active Profiles (`GET /api/profiles/active`), Login, Logout, Get Client Version, Update Client, and Username.

## Cost of Failed Requests

Responses with status `400`, `409` and `422` cost extra rate-limit points. Per the official API FAQ, a `400` costs 6 RPM and 1 RPH. Validate requests before sending them, and fix the request instead of retrying it unchanged.

## Rate Limit Headers

Every cloud API response carries:

```text
Retry-After: 0                   # seconds; 0 means you may send the next request now
X-Ratelimit-Limit: 100           # current RPM limit
X-Ratelimit-Limit-Hour: 1500     # current RPH limit
X-Ratelimit-Remaining: 98        # remaining points this minute
X-Ratelimit-Remaining-Hour: 1460 # remaining points this hour
X-Ratelimit-Reset: 1793102460    # unix timestamp when the minute window resets
```

`X-Ratelimit-Remaining` is the authoritative signal — drop your request rate as it approaches `0`.

Responses also carry the IETF draft `RateLimit` / `RateLimit-Policy` headers (live-verified 2026-11-18):

```text
RateLimit: per_1minute;r=98;t=17, per_1hour;r=1460;t=2057
RateLimit-Policy: per_1minute;q=100;w=60, per_1hour;q=1500;w=3600
```

- `RateLimit`: per window, `r` = remaining points and `t` = seconds until the window resets. The values match `X-Ratelimit-Remaining` / `X-Ratelimit-Remaining-Hour`.
- `RateLimit-Policy`: per window, `q` = quota (limit) and `w` = window length in seconds. The live header can list further policies after these two.

## Reading the Current Budget

[`GET /teams/subscription`](teams.md#get-subscription) returns the current budget in the body, which is handy before starting a large job:

```json
{
  "rate_limits": {
    "rpm": { "limit": 100, "remaining": 98, "reset_at": "2026-10-27T12:01:00" },
    "rph": { "limit": 1500, "remaining": 1460, "reset_at": "2026-10-27T12:35:00" }
  }
}
```

`remaining` already counts this request. `reset_at` is ISO 8601 in **UTC** without a timezone suffix (like all timestamps in response bodies); `rpm.reset_at` equals `X-Ratelimit-Reset` converted to UTC.

## Handling 429 Responses

When the bucket is empty, the API returns `429 Too Many Requests` with a non-zero `Retry-After` header. Because the budget is team-wide, **stop all requests across the team** (not just the one that got the `429`) and pause for `Retry-After` seconds before retrying. Ignoring `429` responses may lead to stricter limits being enforced on the team.

```python
import time
import requests

def request_with_retry(method, url, headers, **kwargs):
    while True:
        response = requests.request(method, url, headers=headers, **kwargs)
        if response.status_code != 429:
            return response
        retry_after = int(response.headers.get("Retry-After", "1"))
        time.sleep(max(retry_after, 1))
```

## Best Practices

1. **Watch the headers.** Slow down before you hit `0` rather than after.
2. **Linear pacing beats bursts.** Spread heavy jobs evenly across the minute.
3. **Cache lookups.** Don't call `GET /tags`, `GET /proxies`, or `GET /fingerprint/renderers` on every iteration.
4. **One-time profiles cost 4×.** When scraping at volume, batch with saved profiles where possible.
5. **Local client calls count too.** Profile start/stop/password operations on `localhost:58888` draw from the same team budget (see the point-cost table above); only the read-only client endpoints are free.
6. **Don't retry failed requests blindly.** `400`/`409`/`422` responses cost extra points; fix the request first.
