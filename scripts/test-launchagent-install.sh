#!/usr/bin/env bash
# Assert scripts/install-launchagent.sh generates a correct, portable plist.
#
# Never touches the real ~/Library/LaunchAgents and never invokes launchctl —
# every generation below passes --output into a temp directory, which the
# installer treats as generate-only. Runs on CI (no macOS dependency beyond
# the optional plutil check, which is skipped where plutil is unavailable).
#
# Usage: scripts/test-launchagent-install.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALLER="$REPO_ROOT/scripts/install-launchagent.sh"
LABEL="net.ritualsync.rewired-episode-refresh"

TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

fail() { echo "FAIL - $1" >&2; exit 1; }
pass() { echo "ok   - $1"; }

echo "(a) generated plist matches the installed reference except repo path"
OUT_A="$TMPDIR/a.plist"
"$INSTALLER" --output "$OUT_A" >/dev/null

REFERENCE="$HOME/Library/LaunchAgents/${LABEL}.plist"
if [ -f "$REFERENCE" ]; then
  # Normalize only the repo path segment embedded in ProgramArguments —
  # everything else (Label, both StartCalendarInterval entries, RunAtLoad,
  # PATH, StandardOutPath/StandardErrorPath) must match exactly.
  normalized_ref="$(sed "s#${REPO_ROOT}#__REPO__#g" "$REFERENCE")"
  normalized_a="$(sed "s#${REPO_ROOT}#__REPO__#g" "$OUT_A")"
  if [ "$normalized_ref" != "$normalized_a" ]; then
    diff <(printf '%s\n' "$normalized_ref") <(printf '%s\n' "$normalized_a") >&2 || true
    fail "generated plist differs from installed reference beyond the repo path"
  fi
  pass "matches installed reference except repo path"
else
  echo "skip - no installed reference at $REFERENCE (nothing to diff against on this runner)"
fi

echo "(b) a second generation from the same checkout is byte-identical"
OUT_B="$TMPDIR/b.plist"
"$INSTALLER" --output "$OUT_B" >/dev/null
cmp -s "$OUT_A" "$OUT_B" || fail "two generations from the same checkout differ"
pass "byte-identical across repeat generation"

echo "(c) generating from a copied checkout at a different path names that path"
MOVED="$TMPDIR/moved-checkout"
mkdir -p "$MOVED"
cp -R "$REPO_ROOT/." "$MOVED/"
OUT_C="$TMPDIR/c.plist"
"$MOVED/scripts/install-launchagent.sh" --output "$OUT_C" >/dev/null
grep -q "${MOVED}/scripts/auto-refresh-deploy.sh" "$OUT_C" \
  || fail "plist generated from the moved checkout does not name the moved path"
pass "plist generated from a moved checkout names that checkout's path"

echo "(d) plutil -lint passes on the generated plist"
if command -v plutil >/dev/null 2>&1; then
  plutil -lint "$OUT_A" >/dev/null || fail "plutil -lint failed on generated plist"
  pass "plutil -lint passes"
else
  echo "skip - plutil not available on this runner"
fi

echo "test-launchagent-install: all assertions passed"
