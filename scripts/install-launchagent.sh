#!/usr/bin/env bash
# Generate and install the episode-refresh LaunchAgent.
#
# WHY THIS EXISTS: net.ritualsync.rewired-episode-refresh.plist used to exist
# only as an installed file under ~/Library/LaunchAgents — no source of truth,
# no installer, no test. This script IS the source of truth: it generates the
# plist from a heredoc, deriving the repo path from its own location, then
# (re)loads the agent. No plist file is committed to this repo — a committed
# copy alongside a generator invites the two drifting apart silently.
#
# The schedule, label, and paths below must stay in lockstep with the deployed
# reference plist (scripts/test-launchagent-install.sh asserts this). If you
# change the schedule here, you are changing what fires in production.
#
# Usage:
#   scripts/install-launchagent.sh              # generate + (re)load the real agent
#   scripts/install-launchagent.sh --output P    # generate only, to path P (no load)
#   scripts/install-launchagent.sh --no-load     # generate the real plist, skip launchctl
#
# Safe to re-run any time: after moving this checkout, after editing this
# script, or just to confirm the agent is loaded and healthy.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LABEL="net.ritualsync.rewired-episode-refresh"
LOG="$HOME/Library/Logs/rewired-episode-refresh.launchd.log"

PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
LOAD=1

while [ $# -gt 0 ]; do
  case "$1" in
    --output)
      [ $# -ge 2 ] || { echo "--output requires a path argument" >&2; exit 1; }
      PLIST="$2"
      LOAD=0
      shift 2
      ;;
    --no-load)
      LOAD=0
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

mkdir -p "$(dirname "$PLIST")"

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>${REPO}/scripts/auto-refresh-deploy.sh</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/usr/bin:/bin:/usr/sbin:/sbin</string>
  </dict>
  <key>StartCalendarInterval</key>
  <array>
    <dict>
      <key>Hour</key><integer>12</integer>
      <key>Minute</key><integer>0</integer>
    </dict>
    <dict>
      <key>Hour</key><integer>19</integer>
      <key>Minute</key><integer>0</integer>
    </dict>
  </array>
  <key>RunAtLoad</key>
  <false/>
  <key>StandardOutPath</key>
  <string>${LOG}</string>
  <key>StandardErrorPath</key>
  <string>${LOG}</string>
</dict>
</plist>
EOF

if command -v plutil >/dev/null 2>&1; then
  plutil -lint "$PLIST"
fi

if [ "$LOAD" -eq 1 ]; then
  mkdir -p "$(dirname "$LOG")"
  # Idempotent: unload first (no-op if it wasn't loaded) so a second run
  # doesn't fail on "already loaded".
  launchctl unload "$PLIST" 2>/dev/null || true
  launchctl load "$PLIST"
  echo "Installed and loaded: $PLIST"
else
  echo "Generated: $PLIST"
fi
