#!/usr/bin/env bash
# Fetch the official Octo Browser API docs + OpenAPI specs into an evidence
# directory and diff them against this mirror. Read-only; never touches the repo.
# Usage: scripts/fetch-upstream.sh <evidence-dir>
set -uo pipefail
cd "$(dirname "$0")/.."
EV="${1:?usage: $0 <evidence-dir>}"; mkdir -p "$EV/upstream"
UA="Mozilla/5.0 (X11; Linux x86_64) docs-mirror-sync"
PAGES="authentication rate-limiting errors profiles tags folders proxies teams fingerprint local-client docker automation"

get() { curl -fsSL --max-time 60 -A "$UA" "$1" -o "$2" && echo "OK      $1" || { echo "FAILED  $1"; return 1; }; }

{
echo "# Upstream fetch $(date -u +%FT%TZ)"
get https://docs.octobrowser.net/llms.txt "$EV/upstream/llms.txt"
for p in $PAGES; do get "https://docs.octobrowser.net/api/$p.md" "$EV/upstream/$p.md"; done
get https://static.octobrowser.net/openapi/server_automation_api.json "$EV/upstream/server_automation_api.json"
get https://static.octobrowser.net/openapi/client_public_api.json "$EV/upstream/client_public_api.json"
get https://docs.octobrowser.net/en/faq/api-faq/ "$EV/upstream/api-faq.html"
get https://docs.octobrowser.net/en/changelog/octo-browser-changelog/ "$EV/upstream/changelog.html"
# Postman collection (documenter.getpostman.com/view/1801428/UVC6i6eA) — the JSON behind the page.
get "https://documenter.getpostman.com/api/collections/1801428/UVC6i6eA?segregateAuth=true&versionTag=latest" "$EV/upstream/postman_collection.json"

echo; echo "# Postman collection (flattened -> readable md; diff vs committed baseline; cross-check vs mirror)"
PM_BASE=".claude/skills/docs-sync/references/postman-baseline.md"
if [ -s "$EV/upstream/postman_collection.json" ]; then
  python3 scripts/postman-flatten.py "$EV/upstream/postman_collection.json" "$EV/upstream/postman.md" "$EV/upstream/postman_inventory.json"
  if [ -s "$PM_BASE" ]; then
    if diff -q "$PM_BASE" "$EV/upstream/postman.md" >/dev/null; then echo "IDENTICAL postman (vs baseline $(sed -n 's/^<!-- fetched \(.*\) -->$/\1/p' "$PM_BASE"))"
    else
      diff -u "$PM_BASE" "$EV/upstream/postman.md" > "$EV/diff_postman.patch"
      echo "DIFFERS   postman: $(grep -c '^[-+][^-+]' "$EV/diff_postman.patch") changed lines -> $EV/diff_postman.patch"
      echo "          sections touched:"; grep -E '^@@.*@@ ' "$EV/diff_postman.patch" | sed -E 's/^@@[^@]*@@ //' | sort -u | sed 's/^/            /'
      echo "          (after adopting, refresh baseline: cp $EV/upstream/postman.md $PM_BASE)"
    fi
  else echo "NO-BASELINE postman: first run; after review copy $EV/upstream/postman.md to $PM_BASE"; fi
  python3 scripts/postman-crosscheck.py "$EV/upstream/postman_inventory.json" openapi.json api > "$EV/postman_crosscheck.md"
  echo "cross-check: $(grep -c '^### ' "$EV/postman_crosscheck.md") requests with discrepancies -> $EV/postman_crosscheck.md"
fi

echo; echo "# Markdown diff (mirror vs upstream)"
for p in $PAGES; do
  if [ ! -s "$EV/upstream/$p.md" ]; then echo "UPSTREAM-MISSING api/$p.md"; continue; fi
  [ -f "api/$p.md" ] || { echo "LOCAL-MISSING    api/$p.md"; continue; }
  if diff -q "api/$p.md" "$EV/upstream/$p.md" >/dev/null; then echo "IDENTICAL api/$p.md"
  else echo "DIFFERS   api/$p.md"; diff -u "api/$p.md" "$EV/upstream/$p.md" > "$EV/diff_$p.patch"; fi
done
diff -q llms.txt "$EV/upstream/llms.txt" >/dev/null && echo "IDENTICAL llms.txt" || { echo "DIFFERS   llms.txt"; diff -u llms.txt "$EV/upstream/llms.txt" > "$EV/diff_llms.patch"; }

echo; echo "# OpenAPI diff (local openapi.json vs upstream server spec)"
python3 - "$EV" <<'PY'
import json, sys, difflib, pathlib
ev = pathlib.Path(sys.argv[1])
try:
    off = json.load(open(ev/'upstream/server_automation_api.json')); loc = json.load(open('openapi.json'))
except Exception as e:
    print('spec diff skipped:', e); sys.exit(0)
print('versions: upstream', off.get('info',{}).get('version'), '| local', loc.get('info',{}).get('version'))
op, lp = set(off['paths']), set(loc['paths'])
print('paths only upstream:', sorted(op-lp) or 'none')
extra = sorted(lp-op)
print('paths only local   :', extra or 'none', '(expected: x-source annotated live-verified endpoints)')
out = []
for p in sorted(op & lp):
    a = json.dumps(loc['paths'][p], indent=1, sort_keys=True).splitlines()
    b = json.dumps(off['paths'][p], indent=1, sort_keys=True).splitlines()
    if a != b:
        print('DIFFERS path', p); out += [f'### {p}'] + list(difflib.unified_diff(a, b, 'local', 'upstream', lineterm='', n=2))
so, sl = off.get('components',{}).get('schemas',{}), loc.get('components',{}).get('schemas',{})
print('schemas only upstream:', sorted(set(so)-set(sl)) or 'none')
print('schemas only local   :', sorted(set(sl)-set(so)) or 'none')
for s in sorted(set(so)&set(sl)):
    a = json.dumps(sl[s], indent=1, sort_keys=True).splitlines(); b = json.dumps(so[s], indent=1, sort_keys=True).splitlines()
    if a != b:
        print('DIFFERS schema', s); out += [f'### schema {s}'] + list(difflib.unified_diff(a, b, 'local', 'upstream', lineterm='', n=2))
(ev/'spec_diffs.txt').write_text('\n'.join(out) + '\n')
print('detail written to', ev/'spec_diffs.txt')
PY
} | tee "$EV/diff_summary.txt"
