#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "$0")" && pwd)/common.sh"

MISSION="${1:-}"
INTERVAL_SECONDS="${2:-900}"

[[ -n "$MISSION" ]] || fail "Usage: bin/babysit-mission.sh <mission> [interval-seconds]"

MISSION_DIR="$PATLAS_ROOT/missions/$MISSION"
STATE_FILE="$MISSION_DIR/mission-state.json"
BABYSIT_DIR="$PATLAS_ROOT/runtime/babysit"
LOG_FILE="$BABYSIT_DIR/$(sanitize_token "$MISSION").log"
LATEST_FILE="$BABYSIT_DIR/$(sanitize_token "$MISSION")-latest.md"

mkdir -p "$BABYSIT_DIR"

snapshot() {
  {
    echo "# Mission Babysit Snapshot"
    echo
    echo "- timestamp: $(timestamp_utc)"
    echo "- mission: $MISSION"
    if [[ -f "$STATE_FILE" ]]; then
      echo "- mission-state:"
      sed 's/^/  /' "$STATE_FILE"
    else
      echo "- mission-state: missing"
    fi
    echo "- active-runtime-statuses:"
    python3 - "$PATLAS_ROOT/runtime/status" "$(sanitize_token "$MISSION")" <<'PY'
import glob
import json
import os
import sys

status_root, mission_token = sys.argv[1:3]
active = []
for path in sorted(glob.glob(os.path.join(status_root, f"codex-patlas-{mission_token}*.json"))):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if data.get("state") == "active":
        active.append(
            f"  - {os.path.basename(path)} | role={data.get('role','')} | session={data.get('session_name','')}"
        )
if active:
    print("\n".join(active))
else:
    print("  - none")
PY
  } > "$LATEST_FILE"

  {
    echo "===== $(timestamp_utc) ====="
    cat "$LATEST_FILE"
    echo
  } >> "$LOG_FILE"
}

while true; do
  snapshot
  sleep "$INTERVAL_SECONDS"
done
