#!/bin/bash

# Strategizer — Stop Hook (simplified)
# One job: keep the strategizer alive across context resets.
# The strategizer handles its own completion and missionary handoff.

set -euo pipefail

# ── Read hook input from stdin ──
HOOK_INPUT=$(cat)

# ── Paths ──
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STATE_DIR="$SCRIPT_DIR"
LOOP_STATE="$STATE_DIR/LOOP-STATE.md"
DEBUG_LOG="/tmp/strategizer-hook.log"

# ── Emergency escape hatch ──
if [[ -f "$STATE_DIR/PAUSE_HOOK" ]]; then
  echo "$(date): PAUSED by PAUSE_HOOK file" >> "$DEBUG_LOG"
  exit 0
fi

# ── Check if loop is active ──
if [[ ! -f "$LOOP_STATE" ]]; then
  exit 0
fi

# ── Parse hook input ──
TRANSCRIPT_PATH=$(echo "$HOOK_INPUT" | jq -r '.transcript_path // empty')

# ── Is this my session? ──
# The strategizer runs from the strategy directory, so its transcript path
# contains the strategy directory name encoded in the project key.
# This is set at session start and never changes.
STRATEGY_DIR_NAME=$(basename "$SCRIPT_DIR")
if [[ -z "$TRANSCRIPT_PATH" ]] || [[ "$TRANSCRIPT_PATH" != *"$STRATEGY_DIR_NAME"* ]]; then
  exit 0
fi

# ── Debug logging (to FILE, never stdout) ──
echo "$(date): HOOK FIRED for $TRANSCRIPT_PATH" >> "$DEBUG_LOG"

# ── Parse LOOP-STATE.md ──
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$LOOP_STATE")
ITERATION=$(echo "$FRONTMATTER" | grep '^iteration:' | sed 's/iteration: *//')
MAX_ITERATIONS=$(echo "$FRONTMATTER" | grep '^max_iterations:' | sed 's/max_iterations: *//')

# ── Validate ──
if [[ ! "$ITERATION" =~ ^[0-9]+$ ]] || [[ ! "$MAX_ITERATIONS" =~ ^[0-9]+$ ]]; then
  echo "$(date): ERROR — corrupted state (iteration=$ITERATION, max=$MAX_ITERATIONS)" >> "$DEBUG_LOG"
  exit 0
fi

# ── Safety cap: max restarts ──
if [[ $MAX_ITERATIONS -gt 0 ]] && [[ $ITERATION -ge $MAX_ITERATIONS ]]; then
  echo "$(date): MAX RESTARTS reached ($MAX_ITERATIONS) — letting session die" >> "$DEBUG_LOG"
  exit 0
fi

# ── Continue the loop ──
NEXT_ITERATION=$((ITERATION + 1))
TEMP_FILE="${LOOP_STATE}.tmp.$$"
sed "s/^iteration: .*/iteration: $NEXT_ITERATION/" "$LOOP_STATE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$LOOP_STATE"

echo "$(date): CONTINUING — restart $NEXT_ITERATION of $MAX_ITERATIONS" >> "$DEBUG_LOG"

# ── Meta-prompt ──
META_PROMPT=$(cat <<'PROMPT_EOF'
You are the Strategizer in autonomous loop mode. A context reset occurred. Resume your work.

## Startup Sequence

1. **Read `state.json`** — your iteration, phase, explorations completed.
2. **Read `STRATEGY.md`** — your strategic direction.
3. **Read `HISTORY.md`** — summaries of all completed explorations.
4. **If needed**, check the library INDEX at `../../../../agents/library/factual/INDEX.md`.
5. **Determine your phase** from state.json:
   - If an exploration was in progress: treat as failed, plan next.
   - If between explorations: decide what to explore next.

Continue running explorations until you reach 20 total, then write your final report and launch the missionary.
PROMPT_EOF
)

SYSTEM_MSG="Strategizer Loop — restart $NEXT_ITERATION of $MAX_ITERATIONS"

# ── Output JSON to block the stop ──
jq -n \
  --arg prompt "$META_PROMPT" \
  --arg msg "$SYSTEM_MSG" \
  '{
    "decision": "block",
    "reason": $prompt,
    "systemMessage": $msg
  }'

exit 0
