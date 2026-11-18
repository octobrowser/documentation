# Intentional divergences from upstream (live-verified 2026-08-17/20, re-probed 2026-11-18)

The mirror deliberately differs from docs.octobrowser.net / the official OpenAPI
spec / the Postman collection where the live API contradicted them. A sub-agent must NOT "fix" these back
to upstream unless a fresh live probe shows the behaviour changed.

| Topic | Upstream says | Live API (mirror) says |
|---|---|---|
| Tags in profile payloads | names (OpenAPI and Postman agree since 2026-11) | **names** (≤20 chars) for `tags[]`, `pinned_tag`, `search_tags`; UUIDs rejected with `string_too_long`; unknown names are **silently dropped** (no 4xx, no auto-create) |
| Fingerprint `os` enum | OpenAPI `win\|mac\|android` (agrees since 2026-11); Postman renderer sample still shows `lin` | `win\|mac\|android` only; `lin` and `ios` → 400 (re-probed 2026-11-18). iOS profiles exist in responses but cannot be created |
| Android `os_version` | free-form | must be in chosen `device_model.os_versions` (else `fingerprints.invalid_mobile_model`) |
| Android `device_type` on create | absent from OpenAPI `CreateProfileFingerprintValidator` (`additionalProperties:false`) | accepted and validated against the model; mismatch → `400 fingerprints.invalid_mobile_type` (2026-11-18) |
| `force_stop` body | Postman: `version` optional ("omit to stop the current session") | `version` required but nullable: `{}` → 400, `{"version":null}` OK; accepts int or numeric string (re-probed 2026-11-18) |
| Validation errors | OpenAPI agrees on `400` + `validation_error` since 2026-11 | cloud: `400` + `{"validation_error":{"body_params"\|"query_params"\|"path_params":[…]}}` (no envelope); some semantic checks use the envelope with `code:"validation_error"` (e.g. mac `os_version`); **local client** really does use `422` + `detail` |
| Create status codes | OpenAPI agrees since 2026-11; Postman shows folders → 201 | `POST /profiles`, `POST /tags`, `POST /proxies` → **201**; `POST /folders` → **200** (re-probed 2026-11-18; Postman's 201 is wrong) |
| Envelope | OpenAPI includes `code` since 2026-11 | `{success,msg,data,code}`; `code` null on success; errors carry `data:""` — except `DELETE /profiles` 404 and `trash_bin/restore` 400, which return the result lists in `data` |
| Delete responses `data` | OpenAPI `BaseResponse_NoneType_` → `null` | tags/folders/proxies DELETE → `data: null` (proxies re-probed 2026-11-18) |
| Profile PATCH `fingerprint.os` | Postman marks `os` `[required]`; OpenAPI allows it | `os` in a PATCH → `400 profiles.update_error "You can't update os."` (re-probed 2026-11-18) |
| `GET /profiles/{uuid}?fields=` | — | `fields` ignored on single-profile GET (full object) |
| Proxy field forms | OpenAPI lists string uuid, `{uuid}`, inline, VPN, `null` (agrees since 2026-11) | as upstream; inline/VPN temp proxy shown with `uuid:""`; inline VPN `conf` is **not** returned on the profile; unknown uuid → `404 not_found` |
| Renderers/screens `os` query | OpenAPI `win\|mac\|android` (agrees since 2026-11) | android lists empty; `page_len` ∈ {10,25,50,100} |
| Screen format | OpenAPI `<W>x<H> @<scale> <SDR\|HDR>[ P3][ ext]`; Postman Get Screens sample still `2560x1440 (2K)` | new format live; legacy `1920x1080` accepted on create and normalised to `1920x1080 @1 SDR` |
| `media_devices` | OpenAPI request `{type:"manual",data:{…}}`\|`{type:"real"}` | both that and the flat `{video_in,audio_in,audio_out}` accepted; GET returns flat |
| One-time profile defaults (local) | mirror said `headless` false | `headless` **true**, `debug_port` true (client spec + probe) |
| Pagination | uniform | `total_count`+`page`: `GET /profiles`, `/profiles/trash_bin`, `/fingerprint/renderers`, `/proxy_providers/proxies`; `total_count` only: subaccounts/invites; `GET /profiles/export` nested `{data:{data,total,page}}`; bare arrays: tags/proxies/folders/extensions/screens/device_models/platforms/proxy_providers and location lookups; `/teams/extensions` uses `start`/`limit` |
| `DELETE /profiles` default | — | `skip_trash_bin` defaults to **true** (permanent); only `false` moves to the trash bin (2026-11-18) |
| Proxy provider errors | — | unknown provider → **400** `proxy_providers.not_exists` (not 404); kind not offered → 400 `proxy_providers.invalid`; unknown provider-proxy uuid on PATCH/DELETE → 404 `not_found` |
| Provider `geo` codes | OpenAPI `country_code` etc. | 4 keys always present; code case/format depends on provider (`bg` vs `KZ`/`172`); location lookups are case-sensitive |
| Local client rate limits | unlimited (old page) | counts toward RPM/RPH: start/stop=1, force_stop=2, one_time=4 (per API FAQ) |
| Subaccount permissions | — | Octo 3.0 folder flags: `edit_folders`, `view_all_folders`, `visible_folders`, `view_profiles_wo_folders`; `permissions` required on create (2026-11-18) |

Retired: "Action Log WebSocket 404" (2026-08-20) — the upgrade returned `101 Switching Protocols` on 2026-11-18.

Local `openapi.json` = official server spec + extra live-verified endpoints and request properties, each annotated with `x-source`.
`scripts/fetch-upstream.sh` normalises the upstream server-URL prefix and path-param names, so "paths only local" should be `none`.

Update this table whenever a divergence is confirmed, retired, or newly found.
