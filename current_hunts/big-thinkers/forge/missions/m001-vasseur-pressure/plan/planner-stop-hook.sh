#!/bin/bash

# Forge Planner — Stop Hook
# ─────────────────────────
# Template: gets copied into each strategy directory during setup.
# Placeholders m001-vasseur-pressure and m001-vasseur-pressure are replaced at install time.
#
# Purpose: keep the Planner alive across context resets by blocking the
# stop event and injecting a meta-prompt that reconstructs state.
#
# Flow:
#   1. Emergency stop check (PAUSE_HOOK file)
#   2. Strategy complete check (state.json done:true)
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
RESTART_LOG="$STATE_DIR/../../logs/restarts.jsonl"
DEBUG_LOG="$STATE_DIR/../../logs/forge-m001-vasseur-pressure-hook.log"

debug() {
  echo "$(date '+%Y-%m-%dT%H:%M:%S%z'): $*" >> "$DEBUG_LOG"
}

# ── 1. Emergency escape hatch ──────────────────────────────────────────────
if [[ -f "$STATE_DIR/PAUSE_HOOK" ]]; then
  debug "PAUSED — PAUSE_HOOK file present. Letting session die."
  exit 0
fi

# ── 2. Strategy complete — let session die ─────────────────────────────────
if [[ -f "$STATE_JSON" ]]; then
  DONE=$(jq -r '.done // false' "$STATE_JSON" 2>/dev/null || echo "false")
  if [[ "$DONE" == "true" ]]; then
    debug "STRATEGY DONE — state.json has done:true. Letting session die."
    exit 0
  fi
fi

# ── 3. Check LOOP-STATE.md exists and is active ───────────────────────────
if [[ ! -f "$LOOP_STATE" ]]; then
  debug "No LOOP-STATE.md found. Exiting."
  exit 0
fi

# Parse YAML frontmatter (between --- delimiters)
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$LOOP_STATE")

ACTIVE=$(echo "$FRONTMATTER" | grep '^active:' | sed 's/active: *//')
if [[ "$ACTIVE" != "true" ]]; then
  debug "Loop not active (active=$ACTIVE). Letting session die."
  exit 0
fi

# ── 4. Session awareness — claim or match transcript ──────────────────────
TRANSCRIPT_PATH=$(echo "$HOOK_INPUT" | jq -r '.transcript_path // empty')

if [[ -z "$TRANSCRIPT_PATH" ]]; then
  debug "No transcript_path in hook input. Exiting."
  exit 0
fi

# Read the stored transcript binding
BOUND_TRANSCRIPT=$(echo "$FRONTMATTER" | grep '^session_transcript:' | sed 's/session_transcript: *"\{0,1\}\([^"]*\)"\{0,1\}$/\1/')

if [[ -z "$BOUND_TRANSCRIPT" ]]; then
  # First fire — claim this session
  debug "First fire — claiming session: $TRANSCRIPT_PATH"
  TEMP_FILE="${LOOP_STATE}.tmp.$$"
  sed "s|^session_transcript:.*|session_transcript: \"$TRANSCRIPT_PATH\"|" "$LOOP_STATE" > "$TEMP_FILE"
  mv "$TEMP_FILE" "$LOOP_STATE"
  BOUND_TRANSCRIPT="$TRANSCRIPT_PATH"
elif [[ "$TRANSCRIPT_PATH" != "$BOUND_TRANSCRIPT" ]]; then
  # Different session — not ours, don't interfere
  debug "Session mismatch. Bound=$BOUND_TRANSCRIPT, Got=$TRANSCRIPT_PATH. Exiting."
  exit 0
fi

debug "HOOK FIRED for session: $TRANSCRIPT_PATH"

# ── Re-read frontmatter (may have been updated by claim above) ────────────
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$LOOP_STATE")

ITERATION=$(echo "$FRONTMATTER" | grep '^iteration:' | sed 's/iteration: *//')
MAX_ITERATIONS=$(echo "$FRONTMATTER" | grep '^max_iterations:' | sed 's/max_iterations: *//')
SLUG=$(echo "$FRONTMATTER" | grep '^slug:' | sed 's/slug: *//')

# ── Validate parsed values ────────────────────────────────────────────────
if [[ ! "$ITERATION" =~ ^[0-9]+$ ]] || [[ ! "$MAX_ITERATIONS" =~ ^[0-9]+$ ]]; then
  debug "ERROR — corrupted LOOP-STATE (iteration=$ITERATION, max=$MAX_ITERATIONS). Exiting."
  exit 0
fi

# ── 5. Safety cap — max iterations ────────────────────────────────────────
if [[ $MAX_ITERATIONS -gt 0 ]] && [[ $ITERATION -ge $MAX_ITERATIONS ]]; then
  debug "MAX ITERATIONS reached ($ITERATION >= $MAX_ITERATIONS). Letting session die."
  exit 0
fi

# ── Increment iteration counter ───────────────────────────────────────────
NEXT_ITERATION=$((ITERATION + 1))
TEMP_FILE="${LOOP_STATE}.tmp.$$"
sed "s/^iteration: .*/iteration: $NEXT_ITERATION/" "$LOOP_STATE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$LOOP_STATE"

debug "CONTINUING — restart $NEXT_ITERATION of $MAX_ITERATIONS"

# ── Log restart to JSONL ──────────────────────────────────────────────────
# Ensure logs directory exists
mkdir -p "$(dirname "$RESTART_LOG")"

STRATEGY_NAME=$(basename "$SCRIPT_DIR")

jq -n \
  --arg ts "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" \
  --arg agent "planner" \
  --arg session "$TRANSCRIPT_PATH" \
  --arg strategy "$STRATEGY_NAME" \
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

# ── Meta-prompt — tell the Planner how to reconstruct state ───────────────
META_PROMPT=$(cat <<'PROMPT_EOF'
You are the Forge Planner in autonomous loop mode. A context reset just occurred — you have no memory of previous work. Reconstruct your state before doing anything.

## Startup Sequence (follow exactly)

1. **Read `state.json`** — your iteration count, current task, current approach, what approaches have been tried, and the task budget.
2. **Read `STRATEGY.md`** — your methodology and goals for this strategy.
3. **Read `HISTORY.md`** — summaries of all completed tasks. Only the last 2-3 entries need close reading; skim older ones.
4. **Read `REASONING.md`** (last 2-3 entries only) — your recent reasoning for decisions made.
5. **Check for running worker sessions** — run `tmux list-sessions 2>/dev/null` to see if any worker is still active.
6. **Process finished workers** — look in `tasks/` for any task directory containing a `RESULT-SUMMARY.md` that is NOT yet listed in HISTORY.md. If found, read it, update HISTORY.md and state.json.
7. **Re-evaluate** — based on what you now know, decide if the current approach is still the best path forward, or if you should pivot.
8. **Continue** — pick up from where you left off. If you were between tasks, plan the next one. If a task was in progress and the worker is gone, treat it as failed and decide whether to retry or move on.

Do NOT start new work until you have completed steps 1-7.
PROMPT_EOF
)

SYSTEM_MSG="Forge Planner Loop — restart $NEXT_ITERATION of $MAX_ITERATIONS | mission=m001-vasseur-pressure | strategy=$STRATEGY_NAME"

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
