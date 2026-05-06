#!/usr/bin/env bash
# Regenerate llms-full.txt, sitemap.xml, and the .well-known/llms.txt mirror
# from the markdown sources in this repo. Run after updating llms.txt or any
# api/*.md file.
set -euo pipefail

cd "$(dirname "$0")/.."

BASE_URL="https://octobrowser.github.io/documentation"

# Keep the .well-known mirror in lockstep with the canonical llms.txt.
cp ./llms.txt ./.well-known/llms.txt

# llms-full.txt: llms.txt + every linked markdown doc, in spec order.
{
  cat llms.txt
  echo
  echo "---"
  echo
  for f in \
    api/authentication.md \
    api/rate-limiting.md \
    api/errors.md \
    api/profiles.md \
    api/tags.md \
    api/proxies.md \
    api/teams.md \
    api/fingerprint.md \
    api/local-client.md \
    api/docker.md \
    api/automation.md
  do
    echo "# File: ${f}"
    echo
    cat "$f"
    echo
    echo "---"
    echo
  done
} > llms-full.txt

# sitemap.xml: every public URL.
{
  echo '<?xml version="1.0" encoding="UTF-8"?>'
  echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
  for path in "/" "/llms.txt" "/llms-full.txt" "/openapi.json" \
    "/api/authentication.md" "/api/rate-limiting.md" "/api/errors.md" \
    "/api/profiles.md" "/api/tags.md" "/api/proxies.md" "/api/teams.md" \
    "/api/fingerprint.md" "/api/local-client.md" "/api/docker.md" \
    "/api/automation.md"
  do
    echo "  <url><loc>${BASE_URL}${path}</loc></url>"
  done
  echo '</urlset>'
} > sitemap.xml

echo "Built llms-full.txt ($(wc -c < llms-full.txt) bytes)"
echo "Built sitemap.xml"
