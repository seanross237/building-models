#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "$0")" && pwd)/common.sh"

MISSION="${1:-}"
INTERVAL_SECONDS="${2:-900}"

[[ -n "$MISSION" ]] || fail "Usage: bin/start-babysitter.sh <mission> [interval-seconds]"

MISSION_TOKEN="$(sanitize_token "$MISSION")"
SESSION_NAME="${SESSION_PREFIX}-${MISSION_TOKEN}-babysitter"
LOG_FILE="$PATLAS_ROOT/runtime/logs/${SESSION_NAME}.log"

mkdir -p "$PATLAS_ROOT/runtime/logs"
tmux kill-session -t "$SESSION_NAME" 2>/dev/null || true
tmux new-session -d -s "$SESSION_NAME" \
  "cd '$PATLAS_ROOT' && bash '$PATLAS_ROOT/bin/babysit-mission.sh' '$MISSION' '$INTERVAL_SECONDS' >> '$LOG_FILE' 2>&1"

echo "session_name=$SESSION_NAME"
echo "log_file=$LOG_FILE"
