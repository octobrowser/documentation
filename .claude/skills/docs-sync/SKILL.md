---
name: docs-sync
description: Sync this Octo API docs mirror with upstream after an update — fetch official docs/specs, diff, live-probe changed endpoints, apply edits, then run verify + proofread sub-agents before a single squashed commit. Use when the user says upstream docs/API changed or asks to recheck the documentation.
argument-hint: "[optional: what changed / which area to focus on]"
---

You are the **orchestrator**. Do the deterministic steps yourself; delegate every
reading/verification/proofreading unit to sub-agents (Agent tool), launching
independent ones in parallel. Evidence lives in `$EV` (scratchpad), never in the repo.

Read `references/known-divergences.md` (next to this file) first and pass its
contents to every sub-agent — intentional divergences are not bugs.

## Phase 0 — Collect evidence (you)

```bash
EV=<scratchpad>/docs-sync; mkdir -p "$EV"
scripts/fetch-upstream.sh "$EV"        # upstream copies + diff_summary.txt + *.patch + spec_diffs.txt
                                       # + Postman: upstream/postman.md (flattened), diff_postman.patch, postman_crosscheck.md
git status --short; git log --oneline -5
```
Upstream has **four** sources, all fetched by the script: the markdown pages,
the OpenAPI specs, FAQ/changelog HTML, and the **Postman collection**
(`documenter.getpostman.com/view/1801428/UVC6i6eA`, fetched as JSON). The Postman
collection is the richest and changes most often while the markdown stays
byte-identical, so never conclude "no changes" from the markdown diff alone.

`scripts/postman-flatten.py` turns the collection into deterministic readable
markdown (`$EV/upstream/postman.md`, one `###` per request: URL, description,
query, headers, body, every response) and an inventory JSON.
`scripts/postman-crosscheck.py` compares that inventory with `openapi.json` and
`api/*.md` (missing endpoints, params, body keys, status codes, unmentioned
fields) → `$EV/postman_crosscheck.md`. The readable markdown is diffed against
the committed baseline `references/postman-baseline.md` → `$EV/diff_postman.patch`
(the summary lists which `###` sections the hunks touch).

Read `$EV/diff_summary.txt`. If everything is IDENTICAL (markdown **and** Postman
vs baseline), the spec diff is clean (only expected "paths only local") and the
cross-check shows no discrepancies, report "no upstream changes" and stop —
unless the user's argument points at a change the diff can't see (FAQ, changelog,
live behaviour); then continue with that scope only.

## Phase 1 — Analyse (sub-agents, parallel)

Launch together, each returning a structured report with file:line references:

1. **Upstream-diff analyst** — inputs: `$EV/diff_*.patch` (incl. `diff_postman.patch`),
   `$EV/spec_diffs.txt`, `$EV/postman_crosscheck.md`, `$EV/upstream/api-faq.html`,
   `$EV/upstream/changelog.html`, known-divergences. For Postman hunks, read the
   surrounding `###` section of `$EV/upstream/postman.md` and the matching
   `api/*.md` section so the verdict is about facts, not example noise (emails,
   uuids, timestamps). If there is no baseline yet (`NO-BASELINE`), split
   `postman.md` by top-level 📁 folder across several analysts instead.
   Classify every hunk as: (a) upstream addition/fix → adopt; (b) conflicts with a
   known divergence → keep ours, flag for re-probe; (c) upstream regression/typo →
   ignore, note it. Also list changelog/FAQ entries since the last commit date that
   touch the API (new endpoints, limits, permissions, point costs).
2. **Internal-consistency auditor** — read all `api/*.md`, `llms.txt`, `README.md`,
   `index.html`, `openapi.json`. Report: endpoint inventory per file vs spec; md↔spec
   mismatches (paths, methods, params, enums, shapes); endpoint-count claims in
   README/llms.txt vs reality; cross-file constants (base URLs, header name,
   rate-limit numbers, `page_len` values, envelope shape, mirror hosts); broken links.
3. **Live prober** (only if there are endpoints/behaviours to confirm) — uses
   `OCTO_API_TOKEN` from `.envrc` (`direnv`/`source .envrc`), base
   `https://app.octobrowser.net/api/v2/automation`, header `X-Octo-Api-Token`.
   Rules: pipe every output through `sed "s/$OCTO_API_TOKEN/<TOKEN>/g"`; save raw
   responses to `$EV/probes/`; prefer GETs; any created resource is named
   `docs-probe-*` and deleted in the same run; never touch existing profiles;
   respect rate limits (≤1 req/s). For each probed fact return: request, status,
   response shape, and verdict vs (i) upstream and (ii) the mirror.

## Phase 2 — Apply (you, or one editor sub-agent for large changes)

Merge the reports into a change list, then edit `api/*.md`, `openapi.json`
(annotate new non-upstream endpoints with `x-source`), `llms.txt`, `README.md`,
`index.html`, and `scripts/build.sh`'s file lists when a page is added. Keep the
mirror's voice and structure (match the neighbouring sections). Update
`references/known-divergences.md` if a divergence was confirmed, retired, or found.
Then `./scripts/build.sh` and `git diff --stat`.

## Phase 3 — Verify + proofread (sub-agents, parallel; gate before commit)

Launch together, each given `git diff` of the working tree plus `$EV`:

4. **Adversarial fact-checker** — for every changed factual claim (path, method,
   field, enum, status code, limit, count), try to refute it against the upstream
   copies and probe evidence. Output per claim: CONFIRMED / REFUTED (with source) /
   UNVERIFIABLE. Also confirm `openapi.json` is valid JSON and every `x-source`
   endpoint still exists in markdown.
5. **Proofreader** — changed files only: grammar, terminology consistency
   (endpoint names, `page_len`, `X-Octo-Api-Token`, Octo 3.0 terms), heading
   levels, table alignment, code-block language tags, example JSON validity,
   consistent tone with unchanged sections. Return concrete `file:line → fix` edits,
   not prose.
6. **Build/index checker** — copy repo to a temp dir, run `scripts/build.sh`, diff
   `llms-full.txt`, `sitemap.xml`, `.well-known/llms.txt` against the working tree
   (must be FRESH); verify every `api/*.md` appears in `llms.txt`, `README.md`,
   `index.html`, `build.sh`, `sitemap.xml`; check relative links resolve.

Apply fixes from 4–6, rebuild, and re-run only the agents whose findings you
changed (REFUTED claims must be resolved, not dropped silently).

## Phase 4 — Report + commit

Write `$EV/REPORT.md` (adopted changes, kept divergences with evidence, ignored
upstream issues, unresolved items) — do **not** commit it. Then commit with
**one** single-line message covering the whole sync (squash intermediate commits;
no bodies), e.g. `Sync with upstream: add X, fix Y (live-verified)`. Don't push
unless asked. Finish with a short recap: what changed, what was verified live,
what remains open.
