# Authentication

All cloud API requests require an API token. The local client API on `http://localhost:58888` is **unauthenticated** and intended for use by code running on the same machine.

## Getting Your API Token

1. Open the Octo Browser desktop app.
2. Navigate to **Settings → API**.
3. Copy your API token.

## Using the API Token

Include the token in the `X-Octo-Api-Token` header on every request to `https://app.octobrowser.net/api/v2/automation/...`:

```bash
curl -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  https://app.octobrowser.net/api/v2/automation/profiles
```

The token is shared across the team — every team member's token authenticates the same workspace, with permissions scoped per [subaccount](teams.md#permission-reference).

## Alternative Endpoints

If your network blocks the canonical host, the API is also reachable on these mirrors:

- `https://app.octobrowser-mirror1.com`
- `https://app.octobrowser-mirror1.net`
- `https://app.octobrowser-mirror1.org`

The path, headers, and behaviour are identical.

## Environment Variable

Avoid embedding the token in source code. Store it in an environment variable:

```bash
export OCTO_API_TOKEN="your_token_here"
```

```python
import os
import requests

headers = {"X-Octo-Api-Token": os.environ["OCTO_API_TOKEN"]}
response = requests.get(
    "https://app.octobrowser.net/api/v2/automation/profiles?page_len=10&page=0",
    headers=headers,
)
```

## Security Notes

- Treat the token like a password. Anyone holding it can act on the team's workspace.
- Never commit tokens to version control. Add `.env`, secret files, and IDE run-configs to `.gitignore`.
- Rotate tokens periodically from the **Settings → API** screen.
- Server-side responses may include cleartext proxy credentials (see [proxies.md](proxies.md)) — log responses carefully.
