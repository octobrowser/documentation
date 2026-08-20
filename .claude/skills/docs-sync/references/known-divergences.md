# Intentional divergences from upstream (live-verified 2026-08-17, re-probed 2026-08-20)

The mirror deliberately differs from docs.octobrowser.net / the official OpenAPI
spec where the live API contradicted them. A sub-agent must NOT "fix" these back
to upstream unless a fresh live probe shows the behaviour changed.

| Topic | Upstream says | Live API (mirror) says |
|---|---|---|
| Tags in profile payloads | UUIDs (OpenAPI); names (Postman) | **names** (≤20 chars) for `tags[]`, `pinned_tag`, `search_tags`; UUIDs rejected with `string_too_long`; unknown names are **silently dropped** (no 4xx, no auto-create) |
| Fingerprint `os` enum | includes `lin` | `win\|mac\|android` only |
| Android `os_version` | free-form | must be in chosen `device_model.os_versions` (else `fingerprints.invalid_mobile_model`) |
| `force_stop` body | — | `version` required but nullable: `{}` → 400, `{"version":null}` OK |
| Validation errors | `422` + `detail` | cloud: `400` + `{"validation_error":{"body_params":[…]}}` (no envelope); **local client** really does use `422` + `detail` |
| Create status codes | 200 (OpenAPI); Postman shows folders → 201 | `POST /profiles`, `POST /tags`, `POST /proxies` → **201**; `POST /folders` → **200** (Postman's 201 is wrong) |
| Envelope | 3 fields | `{success,msg,data,code}`; `code` null on success; errors carry `data:""` |
| Profile PATCH `fingerprint.os` | Postman marks `os` `[required]` in PATCH body | `os` in a PATCH → `400 profiles.update_error "You can't update os."`; partial fingerprint PATCH without `os` works |
| `GET /profiles/{uuid}?fields=` | — | `fields` ignored on single-profile GET (full object) |
| Proxy field forms | `{uuid}` or inline object | also plain-string uuid; `null` detaches; inline = temp proxy shown with `uuid:""`; unknown uuid → `404 not_found` |
| Renderers/screens `os` query | OpenAPI `win\|mac` | `win\|mac\|android` (android lists empty); `page_len` ∈ {10,25,50,100} |
| One-time profile defaults (local) | mirror said `headless` false | `headless` **true**, `debug_port` true (client spec + probe) |
| Action Log WebSocket | Postman documents `wss://…/ws/action_log` | HTTP upgrade → `404 not_found` on 2026-08-20; documented as upstream-only, unverified |
| Pagination | uniform | only `GET /profiles` and `GET /fingerprint/renderers` return `total_count`+`page`; subaccounts/invites `total_count` only; tags/proxies/folders/extensions/screens/device_models are bare arrays; `/teams/extensions` uses `start`/`limit` |
| Local client rate limits | unlimited (old page) | counts toward RPM/RPH: start/stop=1, force_stop=2, one_time=4 (per API FAQ) |
| Subaccount permissions | — | Octo 3.0 folder flags: `edit_folders`, `view_all_folders`, `visible_folders`, `view_profiles_wo_folders` |

Local `openapi.json` = official server spec + 9 extra live-verified endpoints and a
few live-verified request properties, each annotated with `x-source`. "paths only local" in the spec diff is expected for those.

Update this table whenever a divergence is confirmed, retired, or newly found.
