#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "$0")" && pwd)/common.sh"

MISSION="${1:-}"
MODE="${2:---loop}"

[[ -n "$MISSION" ]] || fail "Usage: bin/run-mission-controller.sh <mission> [--once|--loop]"
[[ "$MODE" == "--once" || "$MODE" == "--loop" ]] || fail "Usage: bin/run-mission-controller.sh <mission> [--once|--loop]"

ensure_runtime_dirs
"$PATLAS_ROOT/bin/ensure-dispatcher.sh" >/dev/null

MISSION_DIR="$PATLAS_ROOT/missions/$MISSION"
[[ -d "$MISSION_DIR" ]] || fail "Missing mission: $MISSION_DIR"

MISSION_TOKEN="$(sanitize_token "$MISSION")"
SESSION_NAME="${SESSION_PREFIX}-${MISSION_TOKEN}-mission-controller"
STATUS_FILE="$PATLAS_ROOT/runtime/status/${SESSION_NAME}.json"
LOG_FILE="${LOG_FILE:-$PATLAS_ROOT/runtime/logs/${SESSION_NAME}.log}"
STATE_FILE="$MISSION_DIR/mission-state.json"
CONTROL_DIR="$MISSION_DIR/controller"
DECISIONS_DIR="$CONTROL_DIR/decisions"
TASKS_DIR="$PATLAS_ROOT/runtime/tasks"
CONTROLLER_POLL_SECONDS="${MISSION_CONTROLLER_POLL_SECONDS:-10}"

mkdir -p "$CONTROL_DIR" "$DECISIONS_DIR"

write_controller_status() {
  local state="$1"
  local error_message="${2:-}"
  export STATUS_SESSION_NAME="$SESSION_NAME"
  export STATUS_ROLE="mission-controller"
  export STATUS_MODEL="script"
  export STATUS_STATE="$state"
  export STATUS_WORKSPACE_ROOT="$PATLAS_ROOT"
  export STATUS_OPERATIONAL_WORKDIR="$MISSION_DIR"
  export STATUS_PROMPT_FILE="$PATLAS_ROOT/bin/run-mission-controller.sh"
  export STATUS_TASK_FILE=""
  export STATUS_RESULT_FILE=""
  export STATUS_LOG_FILE="$LOG_FILE"
  export STATUS_SENTINEL_FILE="$MISSION_DIR/MISSION-COMPLETE.md"
  export STATUS_SESSION_PREFIX="$SESSION_PREFIX"
  export STATUS_STARTED_AT="${STATUS_STARTED_AT:-$(timestamp_utc)}"
  export STATUS_FINISHED_AT=""
  export STATUS_LAST_UPDATED="$(timestamp_utc)"
  export STATUS_SEARCH_ENABLED="false"
  export STATUS_ERROR_MESSAGE="$error_message"
  write_status_json "$STATUS_FILE"
}

mission_state_get() {
  local field="$1"
  python3 - "$STATE_FILE" "$field" <<'PY'
import json
import sys

path, field = sys.argv[1:3]
with open(path, encoding="utf-8") as fh:
    data = json.load(fh)
value = data.get(field, "")
if value is None:
    print("")
else:
    print(value)
PY
}

mission_state_update() {
  python3 - "$STATE_FILE" \
    "${1:-__KEEP__}" \
    "${2:-__KEEP__}" \
    "${3:-__KEEP__}" \
    "${4:-__KEEP__}" \
    "${5:-__KEEP__}" \
    "${6:-__KEEP__}" \
    "${7:-__KEEP__}" \
    "${8:-__KEEP__}" \
    "${9:-__KEEP__}" \
    "${10:-__KEEP__}" \
    <<'PY'
import json
import sys
from datetime import datetime, timezone

(
    path,
    status,
    active_chain_run_id,
    active_step_id,
    active_step_chain_run_id,
    last_evaluated_step_id,
    last_evaluated_chain_run_id,
    last_decision_file,
    chain_bootstrap_completed_for_run_id,
    terminal_status,
    blocked_reason,
) = sys.argv[1:]

with open(path, encoding="utf-8") as fh:
    data = json.load(fh)

updates = {
    "status": status,
    "active_chain_run_id": active_chain_run_id,
    "active_step_id": active_step_id,
    "active_step_chain_run_id": active_step_chain_run_id,
    "last_evaluated_step_id": last_evaluated_step_id,
    "last_evaluated_chain_run_id": last_evaluated_chain_run_id,
    "last_decision_file": last_decision_file,
    "chain_bootstrap_completed_for_run_id": chain_bootstrap_completed_for_run_id,
    "terminal_status": terminal_status,
    "blocked_reason": blocked_reason,
}

for key, value in updates.items():
    if value != "__KEEP__":
        data[key] = value

data["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

with open(path, "w", encoding="utf-8") as fh:
    json.dump(data, fh, indent=2, sort_keys=True)
    fh.write("\n")
PY
}

latest_planning_run_id() {
  local latest
  latest="$(find "$MISSION_DIR/planning-runs" -maxdepth 1 -type d -name 'run-*' 2>/dev/null | sort | tail -1 || true)"
  if [[ -n "$latest" ]]; then
    basename "$latest"
  fi
}

latest_step_id() {
  local latest
  latest="$(find "$MISSION_DIR/steps" -maxdepth 1 -type d -name 'step-*' 2>/dev/null | sort | tail -1 || true)"
  if [[ -n "$latest" ]]; then
    basename "$latest"
  fi
}

step_dir() {
  printf '%s/steps/%s\n' "$MISSION_DIR" "$1"
}

step_exists() {
  [[ -d "$(step_dir "$1")" ]]
}

step_state_done() {
  local step_id="$1"
  local path
  path="$(step_dir "$step_id")/state.json"
  [[ -f "$path" ]] || return 1
  [[ "$(python3 - "$path" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as fh:
    data = json.load(fh)
print("true" if data.get("done") else "false")
PY
)" == "true" ]] || return 1
  [[ -f "$(step_dir "$step_id")/RESULTS.md" ]]
}

step_strategizer_error() {
  local step_id="$1"
  local file="$PATLAS_ROOT/runtime/status/${SESSION_PREFIX}-${MISSION_TOKEN}-strategizer-${step_id}.json"
  [[ -f "$file" ]] || return 1
  [[ "$(status_field "$file" state)" == "error" ]]
}

next_step_id() {
  local latest
  latest="$(latest_step_id)"
  if [[ -z "$latest" ]]; then
    printf 'step-001\n'
    return
  fi
  local n="${latest#step-}"
  printf 'step-%03d\n' "$((10#$n + 1))"
}

next_decision_id() {
  local latest
  latest="$(find "$DECISIONS_DIR" -maxdepth 1 -type f -name 'decision-*.json' 2>/dev/null | sort | tail -1 || true)"
  if [[ -z "$latest" ]]; then
    printf 'decision-001\n'
    return
  fi
  local name="${latest##*/}"
  local n="${name#decision-}"
  n="${n%.json}"
  printf 'decision-%03d\n' "$((10#$n + 1))"
}

init_step_scaffold() {
  local step_id="$1"
  local dir
  dir="$(step_dir "$step_id")"
  mkdir -p "$dir/explorations"
  if [[ ! -f "$dir/state.json" ]]; then
    cat > "$dir/state.json" <<'EOF'
{
  "iteration": 0,
  "done": false,
  "current_exploration": null,
  "explorations_completed": []
}
EOF
  fi
  if [[ ! -f "$dir/REASONING.md" ]]; then
    cat > "$dir/REASONING.md" <<'EOF'
# Strategizer Reasoning

The strategizer will append its execution reasoning here.
EOF
  fi
  if [[ ! -f "$dir/HISTORY-OF-REPORT-SUMMARIES.md" ]]; then
    cat > "$dir/HISTORY-OF-REPORT-SUMMARIES.md" <<'EOF'
# History of Report Summaries

Exploration summaries will be appended here as they land.
EOF
  fi
}

write_initial_state() {
  local inferred_chain_run="$1"
  local inferred_step_id="$2"
  cat > "$STATE_FILE" <<EOF
{
  "mission": "$MISSION",
  "status": "idle",
  "active_chain_run_id": "$inferred_chain_run",
  "active_step_id": "$inferred_step_id",
  "active_step_chain_run_id": "$inferred_chain_run",
  "last_evaluated_step_id": "",
  "last_evaluated_chain_run_id": "",
  "last_decision_file": "",
  "chain_bootstrap_completed_for_run_id": "",
  "terminal_status": "",
  "blocked_reason": "",
  "updated_at": "$(timestamp_utc)"
}
EOF
}

init_mission_state() {
  if [[ -f "$STATE_FILE" ]]; then
    return
  fi

  local chain_run step_id
  chain_run="$(latest_planning_run_id)"
  step_id="$(latest_step_id)"
  if [[ -z "$step_id" ]]; then
    step_id=""
  fi
  write_initial_state "$chain_run" "$step_id"
}

evaluate_and_write_decision() {
  local mode="$1"
  local step_id="$2"
  local chain_run_id="$3"
  local decision_id task_file decision_json decision_md next_step goal_file mission_complete_file latest_run_dir

  decision_id="$(next_decision_id)"
  task_file="$TASKS_DIR/${SESSION_PREFIX}-${MISSION_TOKEN}-${decision_id}-step-evaluator.md"
  decision_json="$DECISIONS_DIR/${decision_id}.json"
  decision_md="$DECISIONS_DIR/${decision_id}.md"
  next_step="$(next_step_id)"
  goal_file="$(step_dir "$next_step")/GOAL.md"
  mission_complete_file="$MISSION_DIR/MISSION-COMPLETE.md"
  latest_run_dir="$MISSION_DIR/planning-runs/$chain_run_id"

  cat > "$task_file" <<EOF
Evaluate the mission state and decide whether the mission should proceed with the current chain, replan, or terminate.

Mode: $mode
Mission: $MISSION
Active chain run: $chain_run_id
Mission file: $MISSION_DIR/MISSION.md
Current chain: $MISSION_DIR/CHAIN.md
Chain history: $MISSION_DIR/CHAIN-HISTORY.md
Latest planning run directory: $latest_run_dir
Decision JSON output: $decision_json
Decision memo output: $decision_md
If decision is proceed, write GOAL.md here: $goal_file
If decision is terminate, write mission completion note here: $mission_complete_file
Chronological next step id: $next_step
EOF

  if [[ "$mode" == "post-step" ]]; then
    cat >> "$task_file" <<EOF

Latest completed step:
- Step id: $step_id
- Step goal: $(step_dir "$step_id")/GOAL.md
- Step results: $(step_dir "$step_id")/RESULTS.md
- Step state: $(step_dir "$step_id")/state.json
- Step reasoning: $(step_dir "$step_id")/REASONING.md
- Step summaries: $(step_dir "$step_id")/HISTORY-OF-REPORT-SUMMARIES.md
EOF
  fi

  cat >> "$task_file" <<'EOF'

Write the decision JSON with exactly this schema:
{
  "decision": "proceed" | "replan" | "terminate",
  "reason": "short paragraph",
  "chain_assessment": "active" | "invalidated" | "completed",
  "step_id_evaluated": "step-XYZ or empty string",
  "next_step_id": "step-XYZ or empty string",
  "next_logical_chain_step": "short label or empty string",
  "termination_status": "empty string, negative_complete, positive_complete, or blocked",
  "mission_complete": true | false
}

Rules:
- Choose `proceed` only if the current chain still looks like the right next path.
- Choose `replan` if the latest step weakens, closes, or invalidates the branch enough that the mission should compare paths again.
- Choose `terminate` only if the mission should now stop with a terminal result.
- If `proceed`, write a full step GOAL.md for the provided next step path.
- The step directory number is mission chronology, not proof that the logical chain-step number is the same.
- If `terminate`, write the mission completion note.
- Keep the strategizer step-scoped. You are deciding mission control, not executing the next step.
EOF

  "$PATLAS_ROOT/bin/run-role.sh" \
    --role step-evaluator \
    --workdir "$MISSION_DIR" \
    --task-file "$task_file" \
    --session-name "${SESSION_PREFIX}-${MISSION_TOKEN}-${decision_id}-step-evaluator" \
    --sentinel-file "$decision_json" \
    >/dev/null

  [[ -f "$decision_json" ]] || fail "Step evaluator did not write $decision_json"
  printf '%s\n' "$decision_json"
}

decision_field() {
  local file="$1"
  local field="$2"
  python3 - "$file" "$field" <<'PY'
import json
import sys

path, field = sys.argv[1:3]
with open(path, encoding="utf-8") as fh:
    data = json.load(fh)
value = data.get(field, "")
if isinstance(value, bool):
    print("true" if value else "false")
else:
    print(value)
PY
}

run_planning() {
  write_controller_status "planning"
  local output
  if ! output="$("$PATLAS_ROOT/bin/start-planning-run.sh" "$MISSION")"; then
    mission_state_update "blocked" "__KEEP__" "__KEEP__" "__KEEP__" "__KEEP__" "__KEEP__" "__KEEP__" "__KEEP__" "__KEEP__" "planning failed"
    write_controller_status "error" "planning failed"
    return 1
  fi
  local planning_run
  planning_run="$(printf '%s\n' "$output" | awk -F= '/^planning_run=/{print $2}' | xargs basename)"
  mission_state_update "idle" "$planning_run" "" "" "__KEEP__" "__KEEP__" "__KEEP__" "" "__KEEP__" ""
  return 0
}

launch_step_from_goal() {
  local step_id="$1"
  init_step_scaffold "$step_id"
  write_controller_status "executing"
  "$PATLAS_ROOT/bin/start-step.sh" "$MISSION" "$step_id" >/dev/null
  mission_state_update "executing" "__KEEP__" "$step_id" "$(mission_state_get active_chain_run_id)" "__KEEP__" "__KEEP__" "__KEEP__" "$(mission_state_get active_chain_run_id)" "__KEEP__" ""
}

apply_decision() {
  local decision_file="$1"
  local evaluated_step_id="$2"
  local current_chain_run="$3"
  local decision next_step termination_status mission_complete_file

  decision="$(decision_field "$decision_file" decision)"
  next_step="$(decision_field "$decision_file" next_step_id)"
  termination_status="$(decision_field "$decision_file" termination_status)"
  mission_complete_file="$MISSION_DIR/MISSION-COMPLETE.md"

  case "$decision" in
    proceed)
      [[ -n "$next_step" ]] || fail "Decision $decision_file chose proceed without next_step_id"
      [[ -f "$(step_dir "$next_step")/GOAL.md" ]] || fail "Decision $decision_file chose proceed without writing GOAL.md"
      mission_state_update "idle" "__KEEP__" "" "" "$evaluated_step_id" "$current_chain_run" "$decision_file" "$current_chain_run" "__KEEP__" ""
      launch_step_from_goal "$next_step"
      ;;
    replan)
      mission_state_update "replanning" "__KEEP__" "" "" "$evaluated_step_id" "$current_chain_run" "$decision_file" "" "__KEEP__" ""
      run_planning
      ;;
    terminate)
      if [[ ! -f "$mission_complete_file" ]]; then
        cp "${decision_file%.json}.md" "$mission_complete_file"
      fi
      mission_state_update "terminated" "__KEEP__" "" "" "$evaluated_step_id" "$current_chain_run" "$decision_file" "__KEEP__" "$termination_status" ""
      write_controller_status "done"
      ;;
    *)
      fail "Unknown decision in $decision_file: $decision"
      ;;
  esac
}

advance_once() {
  local state active_chain_run active_step last_eval_step last_eval_chain bootstrap_run

  state="$(mission_state_get status)"
  active_chain_run="$(mission_state_get active_chain_run_id)"
  active_step="$(mission_state_get active_step_id)"
  last_eval_step="$(mission_state_get last_evaluated_step_id)"
  last_eval_chain="$(mission_state_get last_evaluated_chain_run_id)"
  bootstrap_run="$(mission_state_get chain_bootstrap_completed_for_run_id)"

  if [[ "$state" == "terminated" ]]; then
    write_controller_status "done"
    return 1
  fi
  if [[ "$state" == "blocked" ]]; then
    local blocked_reason
    blocked_reason="$(mission_state_get blocked_reason)"
    if [[ "$blocked_reason" == "planning failed" ]]; then
      mission_state_update "replanning" "__KEEP__" "__KEEP__" "__KEEP__" "__KEEP__" "__KEEP__" "__KEEP__" "__KEEP__" "__KEEP__" ""
      run_planning
      return 0
    fi
    write_controller_status "error" "$blocked_reason"
    return 1
  fi

  # If a new plan has landed, a completed step from an older plan must not stay
  # marked as the active step. Clear stale step ownership so the controller can
  # bootstrap the current plan into the next chronological step.
  if [[ -n "$active_step" ]]; then
    local active_step_chain_run
    active_step_chain_run="$(mission_state_get active_step_chain_run_id)"
    if [[ ! -d "$(step_dir "$active_step")" ]]; then
      mission_state_update "__KEEP__" "__KEEP__" "" "" "__KEEP__" "__KEEP__" "__KEEP__" "__KEEP__" "__KEEP__" ""
      active_step=""
    elif [[ -n "$active_chain_run" && -n "$active_step_chain_run" && "$active_step_chain_run" != "$active_chain_run" ]]; then
      if step_state_done "$active_step"; then
        mission_state_update "__KEEP__" "__KEEP__" "" "" "__KEEP__" "__KEEP__" "__KEEP__" "__KEEP__" "__KEEP__" ""
        active_step=""
      fi
    fi
  fi

  if [[ -n "$active_step" ]]; then
    if step_strategizer_error "$active_step"; then
      mission_state_update "blocked" "__KEEP__" "__KEEP__" "__KEEP__" "__KEEP__" "__KEEP__" "__KEEP__" "__KEEP__" "__KEEP__" "strategizer error for $active_step"
      write_controller_status "error" "strategizer error for $active_step"
      return 1
    fi

    if step_state_done "$active_step"; then
      if [[ "$last_eval_step" != "$active_step" || "$last_eval_chain" != "$active_chain_run" ]]; then
        write_controller_status "evaluating"
        local decision_file
        decision_file="$(evaluate_and_write_decision "post-step" "$active_step" "$active_chain_run")"
        apply_decision "$decision_file" "$active_step" "$active_chain_run"
        return 0
      fi

      write_controller_status "active"
      return 1
    fi

    write_controller_status "active"
    return 1
  fi

  if [[ -z "$active_chain_run" || ! -f "$MISSION_DIR/CHAIN.md" ]]; then
    run_planning
    return 0
  fi

  if [[ "$bootstrap_run" != "$active_chain_run" ]]; then
    write_controller_status "evaluating"
    local decision_file
    decision_file="$(evaluate_and_write_decision "bootstrap" "" "$active_chain_run")"
    apply_decision "$decision_file" "" "$active_chain_run"
    return 0
  fi

  write_controller_status "active"
  return 1
}

init_mission_state
write_controller_status "active"

while true; do
  advance_once || true
  if [[ "$MODE" == "--once" ]]; then
    break
  fi
  sleep "$CONTROLLER_POLL_SECONDS"
done

if [[ "$(mission_state_get status)" == "terminated" ]]; then
  write_controller_status "done"
else
  write_controller_status "active"
fi
