#!/usr/bin/env bash
# Regenerate sitemap.xml + llms.txt from posts/*.html.
# Run after adding, removing, or renaming any post. Idempotent.
#
# Usage:  ./scripts/build-meta.sh

set -euo pipefail
cd "$(dirname "$0")/.."

DOMAIN="https://sachinai.com"
TODAY=$(date +%Y-%m-%d)
TAB=$'\t'

declare -a POSTS=()
for f in posts/*.html; do
  slug=$(basename "$f" .html)
  title=$(grep -oE '<title>[^<]*</title>' "$f" | head -1 | sed 's|<[^>]*>||g; s/ — Sachin Rai$//')
  desc=$(grep -oE '<meta name="description" content="[^"]*"' "$f" | head -1 | sed 's|.*content="\([^"]*\)".*|\1|')
  date=$(git log -1 --format=%ad --date=short -- "$f" 2>/dev/null || true)
  [ -z "$date" ] && date="$TODAY"
  POSTS+=("${date}${TAB}${slug}${TAB}${title}${TAB}${desc}")
done

# Sort newest first
IFS=$'\n' read -r -d '' -a SORTED < <(printf '%s\n' "${POSTS[@]}" | sort -r && printf '\0') || true

# ── sitemap.xml ─────────────────────────────────────────────
{
  echo '<?xml version="1.0" encoding="UTF-8"?>'
  echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
  echo
  echo '  <url>'
  echo "    <loc>${DOMAIN}/</loc>"
  echo "    <lastmod>${TODAY}</lastmod>"
  echo '    <changefreq>weekly</changefreq>'
  echo '    <priority>1.0</priority>'
  echo '  </url>'
  echo
  for entry in "${SORTED[@]}"; do
    IFS=$'\t' read -r date slug title desc <<<"$entry"
    echo '  <url>'
    echo "    <loc>${DOMAIN}/posts/${slug}.html</loc>"
    echo "    <lastmod>${date}</lastmod>"
    echo '    <changefreq>monthly</changefreq>'
    echo '    <priority>0.9</priority>'
    echo '  </url>'
    echo
  done
  echo '</urlset>'
} > sitemap.xml

# ── llms.txt ────────────────────────────────────────────────
{
  cat <<'HEADER'
# Sachin Rai — Where AI Meets Enterprise Selling

> A build log from an Enterprise AE at Freshworks who ships AI tools at night.
> 7× President's Club · $2.3M ACV · 200% quota attainment.

## About

Sachin Rai writes about the intersection of AI and enterprise GTM:
- AI tools he's built to prospect faster, close bigger, and automate the grind
- What's actually changing in enterprise sales (not the hype version)
- Claude Code workflows, multi-agent pipelines, and real build logs

## Posts

HEADER
  for entry in "${SORTED[@]}"; do
    IFS=$'\t' read -r date slug title desc <<<"$entry"
    echo "- [${title}](${DOMAIN}/posts/${slug}.html) — ${desc}"
  done
  cat <<'FOOTER'

## Tools Built

- [Cold Email Generator](https://sachinai1981-web.github.io/cold-email-generator) — AI-powered cold email writer
- [Subject Line Scorer](https://sachinai1981-web.github.io/subject-line-scorer) — Score and rewrite cold email subject lines

## Contact

- LinkedIn: https://www.linkedin.com/in/sachinr1/
- Email: sachinai1981@gmail.com
FOOTER
} > llms.txt

echo "✓ Regenerated sitemap.xml + llms.txt from $(ls posts/*.html | wc -l | tr -d ' ') posts."
