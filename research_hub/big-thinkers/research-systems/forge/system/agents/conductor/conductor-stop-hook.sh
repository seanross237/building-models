#!/bin/bash

# Forge Conductor — Stop Hook
# ────────────────────────────
# Template: gets copied into the mission root during setup.
# Placeholders __PREFIX__ and __MISSION_ID__ are replaced at install time.
#
# The Conductor is typically dormant — it launches Planners and checks back
# periodically. This hook is simpler than the Planner's and exists mainly
# for future expansion where the Conductor needs active monitoring.
#
# Flow:
#   1. Emergency stop check (PAUSE_HOOK file)
#   2. Mission complete check (MISSION-COMPLETE.md exists)
#   3. Session ownership check (transcript_path match)
#   4. Max iterations safety cap
#   5. Increment iteration, log restart, emit block decision

set -euo pipefail

# ── Read hook input from stdin ──────────────────────────────────────────────
HOOK_INPUT=$(cat)

# ── Paths ───────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STATE_DIR="$SCRIPT_DIR"
LOOP_STATE="$STATE_DIR/LOOP-STATE.md"
STATE_JSON="$STATE_DIR/state.json"
RESTART_LOG="$STATE_DIR/logs/restarts.jsonl"
DEBUG_LOG="$STATE_DIR/logs/forge-__PREFIX__-conductor-hook.log"

debug() {
  echo "$(date '+%Y-%m-%dT%H:%M:%S%z'): $*" >> "$DEBUG_LOG"
}

# ── 1. Emergency escape hatch ──────────────────────────────────────────────
if [[ -f "$STATE_DIR/PAUSE_HOOK" ]]; then
  debug "PAUSED — PAUSE_HOOK file present. Letting session die."
  exit 0
fi

# ── 2. Mission complete — let session die ──────────────────────────────────
if [[ -f "$STATE_DIR/MISSION-COMPLETE.md" ]]; then
  debug "MISSION COMPLETE — letting session die."
  exit 0
fi

# Also check state.json done flag
if [[ -f "$STATE_JSON" ]]; then
  DONE=$(jq -r '.done // false' "$STATE_JSON" 2>/dev/null || echo "false")
  if [[ "$DONE" == "true" ]]; then
    debug "CONDUCTOR DONE — state.json has done:true. Letting session die."
    exit 0
  fi
fi

# ── 3. Check LOOP-STATE.md exists and is active ───────────────────────────
if [[ ! -f "$LOOP_STATE" ]]; then
  debug "No LOOP-STATE.md found. Exiting."
  exit 0
fi

FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$LOOP_STATE")

ACTIVE=$(echo "$FRONTMATTER" | grep '^active:' | sed 's/active: *//')
if [[ "$ACTIVE" != "true" ]]; then
  debug "Loop not active (active=$ACTIVE). Letting session die."
  exit 0
fi

# ── 4. Session awareness ─────────────────────────────────────────────────
TRANSCRIPT_PATH=$(echo "$HOOK_INPUT" | jq -r '.transcript_path // empty')

if [[ -z "$TRANSCRIPT_PATH" ]]; then
  debug "No transcript_path in hook input. Exiting."
  exit 0
fi

BOUND_TRANSCRIPT=$(echo "$FRONTMATTER" | grep '^session_transcript:' | sed 's/session_transcript: *"\{0,1\}\([^"]*\)"\{0,1\}$/\1/')

if [[ -z "$BOUND_TRANSCRIPT" ]]; then
  # First fire — claim this session
  debug "First fire — claiming session: $TRANSCRIPT_PATH"
  TEMP_FILE="${LOOP_STATE}.tmp.$$"
  sed "s|^session_transcript:.*|session_transcript: \"$TRANSCRIPT_PATH\"|" "$LOOP_STATE" > "$TEMP_FILE"
  mv "$TEMP_FILE" "$LOOP_STATE"
  BOUND_TRANSCRIPT="$TRANSCRIPT_PATH"
elif [[ "$TRANSCRIPT_PATH" != "$BOUND_TRANSCRIPT" ]]; then
  debug "Session mismatch. Bound=$BOUND_TRANSCRIPT, Got=$TRANSCRIPT_PATH. Exiting."
  exit 0
fi

debug "HOOK FIRED for session: $TRANSCRIPT_PATH"

# ── Re-read frontmatter ──────────────────────────────────────────────────
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$LOOP_STATE")

ITERATION=$(echo "$FRONTMATTER" | grep '^iteration:' | sed 's/iteration: *//')
MAX_ITERATIONS=$(echo "$FRONTMATTER" | grep '^max_iterations:' | sed 's/max_iterations: *//')

if [[ ! "$ITERATION" =~ ^[0-9]+$ ]] || [[ ! "$MAX_ITERATIONS" =~ ^[0-9]+$ ]]; then
  debug "ERROR — corrupted LOOP-STATE (iteration=$ITERATION, max=$MAX_ITERATIONS). Exiting."
  exit 0
fi

# ── 5. Safety cap ────────────────────────────────────────────────────────
if [[ $MAX_ITERATIONS -gt 0 ]] && [[ $ITERATION -ge $MAX_ITERATIONS ]]; then
  debug "MAX ITERATIONS reached ($ITERATION >= $MAX_ITERATIONS). Letting session die."
  exit 0
fi

# ── Increment iteration ──────────────────────────────────────────────────
NEXT_ITERATION=$((ITERATION + 1))
TEMP_FILE="${LOOP_STATE}.tmp.$$"
sed "s/^iteration: .*/iteration: $NEXT_ITERATION/" "$LOOP_STATE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$LOOP_STATE"

debug "CONTINUING — restart $NEXT_ITERATION of $MAX_ITERATIONS"

# ── Log restart ───────────────────────────────────────────────────────────
mkdir -p "$(dirname "$RESTART_LOG")"

jq -n \
  --arg ts "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" \
  --arg agent "conductor" \
  --arg session "$TRANSCRIPT_PATH" \
  --arg strategy "conductor" \
  --argjson iter_before "$ITERATION" \
  --argjson iter_after "$NEXT_ITERATION" \
  --arg trigger "stop_hook" \
  '{
    timestamp: $ts,
    agent_type: $agent,
    session: $session,
    strategy: $strategy,
    iteration_before: $iter_before,
    iteration_after: $iter_after,
    trigger: $trigger
  }' >> "$RESTART_LOG"

# ── Meta-prompt ───────────────────────────────────────────────────────────
META_PROMPT=$(cat <<'PROMPT_EOF'
You are the Forge Conductor in autonomous loop mode. A context reset just occurred. Reconstruct your state.

## Startup Sequence

1. **Read `state.json`** — which strategies exist, their status, and overall mission progress.
2. **Read `MISSION.md`** — the mission goal and constraints.
3. **Check strategy directories** — for each strategy in `strategies/`, check its `state.json` to see if any strategy completed while you were down.
4. **Check for FINAL-REPORT.md** in any strategy directory — a completed strategy will have this file.
5. **Process completions** — if a strategy finished, read its FINAL-REPORT.md, update your state.json, and decide whether to launch another strategy or declare the mission complete.
6. **Continue** — if no strategies completed, check if active strategies still have running sessions and decide if intervention is needed.

Do NOT start new work until you have completed steps 1-5.
PROMPT_EOF
)

SYSTEM_MSG="Forge Conductor Loop — restart $NEXT_ITERATION of $MAX_ITERATIONS | mission=__MISSION_ID__"

# ── Output JSON to block the stop ─────────────────────────────────────────
jq -n \
  --arg prompt "$META_PROMPT" \
  --arg msg "$SYSTEM_MSG" \
  '{
    "decision": "block",
    "reason": $prompt,
    "systemMessage": $msg
  }'

exit 0
