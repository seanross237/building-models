#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "$0")" && pwd)/common.sh"

ensure_runtime_dirs

DISPATCHER_SESSION="${SESSION_PREFIX}-dispatcher"
RUNNER_FILE="$ATLAS_ROOT/runtime/tmp/${DISPATCHER_SESSION}.sh"

if tmux has-session -t "$DISPATCHER_SESSION" 2>/dev/null; then
  echo "session_name=$DISPATCHER_SESSION"
  exit 0
fi

{
  echo "#!/usr/bin/env bash"
  echo "set -euo pipefail"
  printf 'exec %q --loop\n' "$ATLAS_ROOT/bin/dispatch-requests.sh"
} > "$RUNNER_FILE"

chmod +x "$RUNNER_FILE"
tmux new-session -d -s "$DISPATCHER_SESSION" -c "$ATLAS_ROOT" "$RUNNER_FILE"

echo "session_name=$DISPATCHER_SESSION"
