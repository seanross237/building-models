#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "$0")" && pwd)/common.sh"

MISSION="${1:-}"
STRATEGY="${2:-}"

[[ -n "$MISSION" ]] || fail "Usage: bin/start-strategy.sh <mission> <strategy>"
[[ -n "$STRATEGY" ]] || fail "Usage: bin/start-strategy.sh <mission> <strategy>"

ensure_runtime_dirs
if ! nested_role_execution; then
  "$ATLAS_ROOT/bin/ensure-dispatcher.sh" >/dev/null
fi

if [[ "$STRATEGY" =~ ^[0-9]+$ ]]; then
  STRATEGY_ID="$(printf 'strategy-%03d' "$STRATEGY")"
else
  STRATEGY_ID="$STRATEGY"
fi

MISSION_DIR="$ATLAS_ROOT/execution/instances/$MISSION"
STRATEGY_DIR="$MISSION_DIR/strategies/$STRATEGY_ID"
[[ -d "$MISSION_DIR" ]] || fail "Missing mission: $MISSION_DIR"
[[ -d "$STRATEGY_DIR" ]] || fail "Missing strategy directory: $STRATEGY_DIR"
[[ -f "$STRATEGY_DIR/STRATEGY.md" ]] || fail "Missing STRATEGY.md: $STRATEGY_DIR/STRATEGY.md"

MISSION_TOKEN="$(sanitize_token "$MISSION")"
SESSION_NAME="${SESSION_PREFIX}-${MISSION_TOKEN}-${STRATEGY_ID}-strategizer"
TASK_FILE="$ATLAS_ROOT/runtime/tasks/${SESSION_NAME}.md"
FINAL_REPORT="$STRATEGY_DIR/FINAL-REPORT.md"

cat > "$TASK_FILE" <<EOF
Execute the full Strategizer role for Atlas mission "$MISSION", strategy "$STRATEGY_ID".

Operational workdir:
- $STRATEGY_DIR

Primary inputs:
- Strategy: $STRATEGY_DIR/STRATEGY.md
- Mission: $MISSION_DIR/MISSION.md
- Validation guide: $MISSION_DIR/MISSION-VALIDATION-GUIDE.md
- Prior strategies: $MISSION_DIR/strategies
- Computation registry: $MISSION_DIR/COMPUTATIONS-FOR-LATER.md
- Shared library: $ATLAS_ROOT/execution/agents/library

Required behavior:
- Run the strategizer loop until you produce FINAL-REPORT.md or hit a clear blocker.
- Keep state.json, LOOP-STATE.md, REASONING.md, and HISTORY-OF-REPORT-SUMMARIES.md synchronized with the work.
- Use \$CODEX_ATLAS_ROOT/bin/run-role.sh for synchronous receptionist queries.
- Use \$CODEX_ATLAS_ROOT/bin/launch-role.sh to launch explorers and curator runs.
- Use session names beginning with $SESSION_PREFIX.
- For each explorer, set the sentinel file to REPORT-SUMMARY.md in that exploration directory.
- For curator runs, use a receipt file as the sentinel output.
- Stay entirely inside this repository.
EOF

"$ATLAS_ROOT/bin/launch-role.sh" \
  --role strategizer \
  --workdir "$STRATEGY_DIR" \
  --task-file "$TASK_FILE" \
  --session-name "$SESSION_NAME" \
  --sentinel-file "$FINAL_REPORT"
