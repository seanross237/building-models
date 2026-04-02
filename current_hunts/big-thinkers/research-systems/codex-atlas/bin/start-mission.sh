#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "$0")" && pwd)/common.sh"

MISSION="${1:-}"
[[ -n "$MISSION" ]] || fail "Usage: bin/start-mission.sh <mission>"

ensure_runtime_dirs
if ! nested_role_execution; then
  "$ATLAS_ROOT/bin/ensure-dispatcher.sh" >/dev/null
fi

MISSION_DIR="$ATLAS_ROOT/execution/instances/$MISSION"
[[ -d "$MISSION_DIR" ]] || fail "Missing mission: $MISSION_DIR"
[[ -f "$MISSION_DIR/MISSION.md" ]] || fail "Missing MISSION.md: $MISSION_DIR/MISSION.md"

MISSION_TOKEN="$(sanitize_token "$MISSION")"
SESSION_NAME="${SESSION_PREFIX}-${MISSION_TOKEN}-missionary"
TASK_FILE="$ATLAS_ROOT/runtime/tasks/${SESSION_NAME}.md"

cat > "$TASK_FILE" <<EOF
Take the next mission-level action for Atlas mission "$MISSION".

Operational workdir:
- $MISSION_DIR

Required behavior:
- Read MISSION.md and MISSION-VALIDATION-GUIDE.md if it exists.
- Read prior strategy outputs and the missionary meta library before deciding.
- If no usable strategy exists, create the next strategy directory, write STRATEGY.md, ensure the standard scaffold exists, and launch a strategizer run for it.
- If the latest strategy has FINAL-REPORT.md, evaluate it, write a missionary meta-learning note, and then either:
  - write MISSION-COMPLETE.md, or
  - create the next strategy and launch its strategizer.
- If a relevant strategizer session is already active, do not duplicate it.
- Use only local launcher scripts inside this repository.
- Do not invoke raw codex exec directly.

Helpful local paths:
- Strategy root: $MISSION_DIR/strategies
- Shared library: $ATLAS_ROOT/execution/agents/library
- Setup guide: $ATLAS_ROOT/execution/SETUP-GUIDE.md
- Strategy launcher: $ATLAS_ROOT/bin/start-strategy.sh
EOF

"$ATLAS_ROOT/bin/launch-role.sh" \
  --role missionary \
  --workdir "$MISSION_DIR" \
  --task-file "$TASK_FILE" \
  --session-name "$SESSION_NAME"
