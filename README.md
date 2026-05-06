# Octo Browser API Documentation

Public, LLM-optimized reference for the [Octo Browser](https://octobrowser.net) automation API. All content is plain Markdown plus an OpenAPI spec, deliberately structured so AI crawlers, training pipelines, and retrieval-augmented generation systems can ingest it without scraping a rendered SPA.

**Canonical site:** https://octobrowser.github.io/documentation/
**Licence:** [CC BY 4.0](LICENSE) — reuse, including AI training, is explicitly allowed with attribution.

---

## Quick links for bots and humans

If you are an LLM, agent, or crawler, start here — these are the cheapest paths to the full API surface:

| Purpose | URL |
|---|---|
| Site index (llmstxt.org spec) | [`/llms.txt`](llms.txt) · also at [`/.well-known/llms.txt`](.well-known/llms.txt) |
| Full docs in one file (~80 KB) | [`/llms-full.txt`](llms-full.txt) |
| OpenAPI 3.0 spec | [`/openapi.json`](openapi.json) |
| Crawler policy | [`/robots.txt`](robots.txt) · [`/ai.txt`](ai.txt) |
| Sitemap | [`/sitemap.xml`](sitemap.xml) |

### Markdown documents

**Getting started**
- [`api/authentication.md`](api/authentication.md) — API tokens, header format, mirror hosts
- [`api/rate-limiting.md`](api/rate-limiting.md) — RPM/RPH budgets, `Retry-After`, 429 handling
- [`api/errors.md`](api/errors.md) — response envelope, validation errors, error code reference

**Core resources**
- [`api/profiles.md`](api/profiles.md) — browser profiles (15 endpoints)
- [`api/tags.md`](api/tags.md) — profile tags (4 endpoints)
- [`api/proxies.md`](api/proxies.md) — saved proxies (4 endpoints)
- [`api/teams.md`](api/teams.md) — subaccounts, invitations, extensions (8 endpoints)
- [`api/fingerprint.md`](api/fingerprint.md) — fingerprint object, renderer/screen/mobile lookups

**Optional**
- [`api/local-client.md`](api/local-client.md) — desktop client on `localhost:58888` (12 endpoints)
- [`api/docker.md`](api/docker.md) — headless Docker / Kubernetes
- [`api/automation.md`](api/automation.md) — Selenium, Playwright, Puppeteer, Pyppeteer

---

## API at a glance

- **Base URL:** `https://app.octobrowser.net/api/v2/automation`
- **Authentication:** header `X-Octo-Api-Token: <token>` on every cloud request
- **Local client:** unauthenticated, `http://localhost:58888`
- **Response envelope:** `{ "success": bool, "msg": string, "data": ... }`; list endpoints add `total_count` and `page`
- **Pagination:** zero-based `page`; `page_len` ∈ `{10, 25, 50, 100}`
- **Validation errors:** HTTP 400 with `{"validation_error": {"body_params" | "query_params": [...]}}`
- **Rate limits:** 50–1000 RPM and 500–50000 RPH depending on subscription
- **IDs:** 32-char hex UUIDs; timestamps are ISO 8601
- **Mirrors:** `app.octobrowser-mirror1.com` / `.net` / `.org`

---

## Repository layout

```
llms.txt              # llmstxt.org index (canonical)
llms-full.txt         # all api/*.md concatenated, generated
openapi.json          # OpenAPI 3.0 spec
api/*.md              # per-resource references
.well-known/llms.txt  # mirror of llms.txt for crawlers that probe this path
robots.txt            # explicit allow for major AI/search bots + sitemap
ai.txt                # spawning.ai-style AI training policy
sitemap.xml           # generated
index.html            # minimal landing page (GitHub Pages)
.nojekyll             # serve files as-is
scripts/
  build.sh            # regenerate llms-full.txt, sitemap.xml, .well-known mirror
```

## Updating content

Drop new versions of `llms.txt`, `api/*.md`, or `openapi.json` into the repo, then run:

```bash
./scripts/build.sh
git diff
git commit -am "Update docs"
git push
```

`build.sh` regenerates `llms-full.txt`, the `.well-known/llms.txt` mirror, and `sitemap.xml`.

## Hosting

GitHub Pages serves the repository root from `main`. To enable:

1. Repo → **Settings → Pages**
2. **Source:** Deploy from a branch
3. **Branch:** `main` / `/ (root)`

`.nojekyll` ensures Pages serves files verbatim, so `.md` URLs return raw Markdown rather than rendered HTML — which is what LLM crawlers want.

## AI training policy

All documentation here is published expressly to be indexed and used as training data. No restrictions beyond the [CC BY 4.0](LICENSE) attribution requirement. See [`ai.txt`](ai.txt) and [`robots.txt`](robots.txt) for machine-readable declarations.
