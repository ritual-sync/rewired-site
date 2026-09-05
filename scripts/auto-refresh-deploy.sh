#!/usr/bin/env bash
# Auto-refresh the vendored Rewired episodes feed and deploy if it changed.
#
# WHY THIS EXISTS: the Episodes section reads a VENDORED copy of the Substack
# podcast RSS (assets/episodes.xml) because Substack 403s GitHub Actions' CI IPs
# on every feed endpoint — the site can only be refreshed from a non-blocked
# (residential) IP. That made "new episode appears on the site" a manual biweekly
# chore, which silently rotted (ep4 never appeared until this job was built).
#
# This wrapper runs from Matt's Mac (a non-blocked IP) via launchd:
#   1. re-fetch the feed into assets/episodes.xml (scripts/refresh-episodes.sh)
#   2. if — and only if — that file changed, commit JUST that file and push
#   3. the push triggers .github/workflows/deploy.yml -> Hugo rebuild -> Pages
#
# Fail-loud: any failure writes a SENTINEL file and exits non-zero (launchd logs
# it). A clean run removes a stale sentinel. It NEVER `git add .` — only the one
# vendored file — so it can't sweep up unrelated working-tree changes.
#
# Paired launchd job: ~/Library/LaunchAgents/net.ritualsync.rewired-episode-refresh.plist
# That plist is GENERATED, not committed — scripts/install-launchagent.sh is its
# only source of truth. Run that script to install/repair the agent on any
# machine (including after this checkout moves); see its header for details.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FEED_FILE="assets/episodes.xml"
STATIC_FILE="static/episodes.xml"   # published copy -> https://rewired.show/episodes.xml (proxy feed for falkensmage.com)
SENTINEL="$HOME/Library/Logs/rewired-episode-refresh.SENTINEL.md"
STAMP="$(date '+%Y-%m-%d %H:%M:%S %z')"

fail() {
  {
    echo "# Rewired episode auto-refresh FAILED"
    echo
    echo "- when: $STAMP"
    echo "- stage: ${1:-unknown}"
    echo "- detail: ${2:-none}"
    echo
    echo "Investigate, then clear this file (or a later clean run clears it):"
    echo "    rm \"$SENTINEL\""
    echo
    echo "Manual recovery:"
    echo "    cd $REPO && ./scripts/refresh-episodes.sh && \\"
    echo "      git add $FEED_FILE && git commit -m 'chore(episodes): refresh feed' && git push"
  } > "$SENTINEL"
  echo "[$STAMP] FAILED at ${1:-unknown}: ${2:-none} (sentinel: $SENTINEL)" >&2
  exit 1
}

echo "[$STAMP] rewired episode auto-refresh: start"

cd "$REPO" || fail "cd" "cannot cd into $REPO"

# Only ever operate on main — never deploy from a feature branch mid-work.
branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '?')"
if [ "$branch" != "main" ]; then
  echo "[$STAMP] on branch '$branch', not main — skipping this run (no-op)."
  exit 0
fi

# Re-fetch the feed (this script self-guards: refuses to overwrite on 0 items).
./scripts/refresh-episodes.sh || fail "fetch" "refresh-episodes.sh returned non-zero (feed blocked/empty?)"

# No change -> nothing to deploy. Clear any stale sentinel and finish.
if git diff --quiet -- "$FEED_FILE" "$STATIC_FILE"; then
  echo "[$STAMP] no feed change — site already current. Done."
  rm -f "$SENTINEL"
  exit 0
fi

latest="$(grep -o '<title>[^<]*' "$FEED_FILE" | sed 's/<title>//' | sed -n '2p')"
echo "[$STAMP] feed changed — newest item: ${latest:-unknown}. Committing + pushing."

git add "$FEED_FILE" "$STATIC_FILE" || fail "add" "git add feed files"
git commit -m "chore(episodes): auto-refresh vendored feed (${latest:-new episode})" -- "$FEED_FILE" "$STATIC_FILE" \
  || fail "commit" "git commit"

# Push; if rejected because origin moved, replay our single commit on top once.
if ! git push origin main; then
  echo "[$STAMP] push rejected — attempting rebase onto origin/main and retry."
  git pull --rebase --autostash origin main || fail "rebase" "pull --rebase (conflict on $FEED_FILE?)"
  git push origin main || fail "push" "git push after rebase"
fi

rm -f "$SENTINEL"
echo "[$STAMP] deployed — push landed, GitHub Actions will rebuild the site."
