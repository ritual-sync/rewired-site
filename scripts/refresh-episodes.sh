#!/usr/bin/env bash
# Refresh the vendored Rewired episodes feed.
#
# Substack 403s GitHub Actions' datacenter IPs on every feed endpoint, so the
# site cannot fetch the feed live at build time. Instead we vendor the podcast
# RSS into assets/episodes.xml and read it locally. Run this from a non-blocked
# IP (a laptop / residential connection) whenever new episodes publish, then
# commit + push to trigger a redeploy.
#
# Usage: scripts/refresh-episodes.sh

set -euo pipefail

FEED_URL="https://api.substack.com/feed/podcast/8721195.rss"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$REPO_ROOT/assets/episodes.xml"

echo "Fetching $FEED_URL ..."
tmp="$(mktemp)"
curl -fsSL -A "Mozilla/5.0" "$FEED_URL" -o "$tmp"

count="$(grep -o '<item>' "$tmp" | wc -l | tr -d ' ')"
if [ "$count" -eq 0 ]; then
  echo "ERROR: feed returned 0 items — refusing to overwrite $OUT" >&2
  rm -f "$tmp"
  exit 1
fi

mv "$tmp" "$OUT"

# Also publish a copy under static/, which Hugo copies verbatim to the built site.
# This exposes the feed at https://rewired.show/episodes.xml — a non-blocked
# (GitHub Pages / Cloudflare) URL that OTHER sites (falkensmage.com) can fetch at
# build time, since Substack itself 403s CI datacenter IPs on its own endpoints.
cp "$OUT" "$REPO_ROOT/static/episodes.xml"

echo "Wrote $OUT + static/episodes.xml ($count episodes)."
echo "  static copy serves at https://rewired.show/episodes.xml (proxy feed for falkensmage.com)"
echo "Next: git add assets/episodes.xml static/episodes.xml && git commit && git push"
