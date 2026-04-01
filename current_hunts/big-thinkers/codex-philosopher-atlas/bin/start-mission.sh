#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "$0")" && pwd)/common.sh"

MISSION="${1:-}"
[[ -n "$MISSION" ]] || fail "Usage: bin/start-mission.sh <mission>"

ensure_runtime_dirs
"$PATLAS_ROOT/bin/ensure-dispatcher.sh" >/dev/null

MISSION_TOKEN="$(sanitize_token "$MISSION")"
SESSION_NAME="${SESSION_PREFIX}-${MISSION_TOKEN}-mission-controller"
STATUS_FILE="$PATLAS_ROOT/runtime/status/${SESSION_NAME}.json"
LOG_FILE="$PATLAS_ROOT/runtime/logs/${SESSION_NAME}.log"
RUNNER_FILE="$PATLAS_ROOT/runtime/tmp/${SESSION_NAME}.sh"

if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
  fail "tmux session already exists: $SESSION_NAME"
fi

{
  echo "#!/usr/bin/env bash"
  echo "set -euo pipefail"
  printf 'exec bash %q %q --loop >%q 2>&1\n' \
    "$PATLAS_ROOT/bin/run-mission-controller.sh" \
    "$MISSION" \
    "$LOG_FILE"
} > "$RUNNER_FILE"

chmod +x "$RUNNER_FILE"
tmux new-session -d -s "$SESSION_NAME" -c "$PATLAS_ROOT" "$RUNNER_FILE"

echo "session_name=$SESSION_NAME"
echo "status_file=$STATUS_FILE"
echo "log_file=$LOG_FILE"
