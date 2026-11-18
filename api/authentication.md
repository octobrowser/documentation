# Authentication

All cloud API requests require an API token. The local client API on `http://localhost:58888` is **unauthenticated** and intended for use by code running on the same machine. When the desktop client is started with `OCTO_API_TOKEN`, it acts with that token's permissions: local API calls that need a permission the token lacks fail with `no_permission`, and the client's actions appear in the Action Log as `<token name> (API)`.

## Getting Your API Token

API tokens are managed in **Team settings → API tokens** in the Octo Browser desktop app (Base plan or higher). A team can have several **named** tokens, each with its own [permissions](#api-token-permissions):

| Plan     | API tokens |
|----------|------------|
| Base     | 1          |
| Team     | 3          |
| Advanced | 5          |

- The token issued by earlier versions keeps working. It is listed as "API token" with full permissions and counts toward the limit.
- On plans with a single team member, every token has full permissions.
- A token can be regenerated. A desktop client signed in with the old token (via `OCTO_API_TOKEN`) is signed out; update the environment variable and restart the client.

## Using the API Token

Include the token in the `X-Octo-Api-Token` header on every request to `https://app.octobrowser.net/api/v2/automation/...`:

```bash
curl -H "X-Octo-Api-Token: YOUR_API_TOKEN" \
  https://app.octobrowser.net/api/v2/automation/profiles
```

Every token authenticates the same team workspace, but each token carries its own permissions and may be restricted to certain folders. A call the token is not allowed to make returns `403`:

```json
{
  "success": false,
  "msg": "No permission",
  "data": "",
  "code": "no_permission"
}
```

## API Token Permissions

Each token can call only the endpoints its permissions allow. The endpoints below require the listed permission; all paths are relative to `https://app.octobrowser.net/api/v2/automation`.

| Permission | Endpoints |
|------------|-----------|
| Create profiles | `POST /profiles`, `POST /profiles/{uuid}/import_cookies`, `POST /profiles/import` (sending `password` on create also needs Profile passwords) |
| Edit profiles | `PATCH /profiles/{uuid}` (without it, `GET /profiles` returns `description` masked as `**`) |
| Delete profiles | `DELETE /profiles`, `GET /profiles/trash_bin`, `POST /profiles/trash_bin/restore` |
| Transfer profiles | `POST /profiles/transfer`, `GET /profiles/export`, `GET /profiles/export/{uuid}`, `POST /profiles/export` |
| Profile passwords | `POST /profiles/set_password`, `POST /profiles/{uuid}/clear_password` |
| Edit tags | `POST /tags`, `PATCH /tags/{uuid}`, `DELETE /tags/{uuid}` |
| Edit folders | `POST /folders`, `PATCH /folders/{uuid}`, `DELETE /folders/{uuid}` (setting `assignable_wo_permission` also needs Manage team) |
| Create proxies | `POST /proxies` |
| Edit proxies | `PATCH /proxies/{uuid}`, `PATCH /proxy_providers/proxies/{uuid}` |
| Delete proxies | `DELETE /proxies/{uuid}`, `DELETE /proxy_providers/proxies/{uuid}` |
| Create paid proxies | `POST /proxy_providers/proxies` |
| Delete extensions | `DELETE /teams/extensions` |
| Manage team | `/teams/subaccounts` and `/teams/invites` (all methods) |
| Action log | `wss://app.octobrowser.net/api/v2/automation/ws/action_log` (see [action-log.md](action-log.md)) |

All other endpoints, including read-only lists and lookups (`GET /profiles`, `GET /folders`, `GET /proxies`, `GET /teams/subscription`, …), need no specific permission, but their results are scoped to the token:

- `GET /profiles` returns only profiles visible to the token.
- `GET /folders` returns only folders available to the token (possibly an empty list).
- Passing a `folder` the token cannot access on profile create, update, or import returns `403 no_permission`.

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

The desktop client also reads `OCTO_API_TOKEN` at startup and signs in automatically, which lets you script cold-start automation without `POST /api/auth/login` — see [local-client.md](local-client.md#signing-in-with-an-api-token) for per-OS launch commands.

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

- Treat the token like a password. Anyone holding it can act on the team's workspace within the token's permissions.
- Never commit tokens to version control. Add `.env`, secret files, and IDE run-configs to `.gitignore`.
- Rotate tokens periodically from **Team settings → API tokens**, and give each script a token with only the permissions it needs.
- Server-side responses may include cleartext proxy credentials (see [proxies.md](proxies.md)) — log responses carefully.
