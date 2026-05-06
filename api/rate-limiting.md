# Rate Limiting

The cloud API enforces a Requests-Per-Minute (RPM) and Requests-Per-Hour (RPH) budget. Limits are **shared across the whole team** — every subaccount's calls draw from the same bucket. Repeatedly ignoring `429` responses will cause us to enforce stricter limits on the team.

## Limits by Subscription

| Plan      | RPM                          | RPH                                |
|-----------|------------------------------|------------------------------------|
| Base      | 50                           | 500                                |
| Team      | 100                          | 1,500                              |
| Advanced  | 200, expandable up to 1,000  | 3,000, expandable up to 50,000     |

For limits beyond 1,000 RPM or 50,000 RPH, contact Octo Browser Technical Support.

## Cost-Multiplier Endpoints

Some endpoints cost more than one point per call. The costs are charged against both RPM and RPH counters:

- `POST /api/profiles/one_time/start` (local client API) — counts as **4 requests**.

Other complex calls may also cost more than one point.

## Rate Limit Headers

Every cloud API response carries:

```
Retry-After: 0                  # seconds; 0 means you may send the next request now
X-Ratelimit-Limit: 200          # current RPM limit
X-Ratelimit-Limit-Hour: 3000    # current RPH limit
X-Ratelimit-Remaining: 4        # remaining points this minute
X-Ratelimit-Remaining-Hour: 2999 # remaining points this hour
X-Ratelimit-Reset: 1671789217   # unix timestamp when the minute window resets
```

`X-Ratelimit-Remaining` is the authoritative signal — drop your request rate as it approaches `0`.

## Handling 429 Responses

When the bucket is empty, the API returns `429 Too Many Requests` with a non-zero `Retry-After` header.

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
5. **Local client API has no rate limit** — drive `start`, `stop`, and `force_stop` against `localhost:58888` freely.
