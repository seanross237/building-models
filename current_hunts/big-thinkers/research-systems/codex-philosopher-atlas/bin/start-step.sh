#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "$0")" && pwd)/common.sh"

MISSION="${1:-}"
STEP="${2:-}"

[[ -n "$MISSION" ]] || fail "Usage: bin/start-step.sh <mission> <step>"
[[ -n "$STEP" ]] || fail "Usage: bin/start-step.sh <mission> <step>"

ensure_runtime_dirs
"$PATLAS_ROOT/bin/ensure-dispatcher.sh" >/dev/null

if [[ "$STEP" =~ ^[0-9]+$ ]]; then
  STEP_ID="$(printf 'step-%03d' "$STEP")"
else
  STEP_ID="$STEP"
fi

MISSION_DIR="$PATLAS_ROOT/missions/$MISSION"
STEP_DIR="$MISSION_DIR/steps/$STEP_ID"
GOAL_FILE="$STEP_DIR/GOAL.md"
RESULTS_FILE="$STEP_DIR/RESULTS.md"
TASK_FILE="$PATLAS_ROOT/runtime/tasks/${SESSION_PREFIX}-$(sanitize_token "$MISSION")-strategizer-${STEP_ID}.md"
SESSION_NAME="${SESSION_PREFIX}-$(sanitize_token "$MISSION")-strategizer-${STEP_ID}"

[[ -d "$MISSION_DIR" ]] || fail "Missing mission: $MISSION_DIR"
[[ -d "$STEP_DIR" ]] || fail "Missing step directory: $STEP_DIR"
[[ -f "$GOAL_FILE" ]] || fail "Missing GOAL.md: $GOAL_FILE"

cat > "$TASK_FILE" <<EOF
Execute the Strategizer role for the copied mission step below.

- Mission: $MISSION
- Step: $STEP_ID
- Operational workdir: $STEP_DIR
- Primary input: $GOAL_FILE
- Mission chain context: $MISSION_DIR/CHAIN.md
- Chain history: $MISSION_DIR/CHAIN-HISTORY.md
- Local library root: $PATLAS_ROOT/library

Required behavior:
- Run the full strategizer loop for this step until you either complete the step or hit a clear blocker.
- Write or update RESULTS.md in the step directory before finishing.
- Keep state.json, REASONING.md, and HISTORY-OF-REPORT-SUMMARIES.md in sync with the work you do.
- Use \$CODEX_PATLAS_ROOT/bin/run-role.sh for synchronous receptionist queries.
- Use \$CODEX_PATLAS_ROOT/bin/launch-role.sh to launch explorers and curator sessions.
- Use session names beginning with $SESSION_PREFIX.
- For each explorer, set the sentinel file to that exploration's REPORT-SUMMARY.md.
- For curator runs, set the sentinel file to the expected library/meta output you just created or updated.
- Do not read or write anything outside this repository.
EOF

"$PATLAS_ROOT/bin/launch-role.sh" \
  --role strategizer \
  --workdir "$STEP_DIR" \
  --task-file "$TASK_FILE" \
  --session-name "$SESSION_NAME" \
  --sentinel-file "$RESULTS_FILE"
