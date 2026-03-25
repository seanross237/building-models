#!/bin/bash

# Theory Builder — Grand Unified Theory Research Loop Stop Hook
# Keeps the autonomous research loop going by feeding a meta-prompt each iteration.
# Only activates when scripts/theory-builder/LOOP-STATE.md exists.
# SESSION-AWARE: Only traps the session that started the loop.

set -euo pipefail

# Read hook input from stdin
HOOK_INPUT=$(cat)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STATE_DIR="$SCRIPT_DIR"
STATE_FILE="$STATE_DIR/LOOP-STATE.md"

# Emergency escape hatch
if [[ -f "$STATE_DIR/PAUSE_HOOK" ]]; then
  exit 0
fi

# Check if loop is active
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0
fi

# Debug: log hook input so we can see what Claude sends
echo "$(date): HOOK FIRED" >> /tmp/theory-builder-hook.log
echo "$HOOK_INPUT" >> /tmp/theory-builder-hook.log

# Only activate for sessions running inside 03-grand-unified-theory/
SESSION_CWD=$(echo "$HOOK_INPUT" | jq -r '.cwd // empty')
TRANSCRIPT_PATH=$(echo "$HOOK_INPUT" | jq -r '.transcript_path // empty')

if [[ -n "$SESSION_CWD" ]] && [[ "$SESSION_CWD" != *"03-grand-unified-theory"* ]]; then
  # CWD does not match — check transcript path as fallback
  if [[ "$TRANSCRIPT_PATH" != *"03-grand-unified-theory"* ]]; then
    echo "$(date): SKIPPED — cwd=$SESSION_CWD, transcript=$TRANSCRIPT_PATH" >> /tmp/theory-builder-hook.log
    exit 0
  fi
elif [[ -z "$SESSION_CWD" ]]; then
  if [[ "$TRANSCRIPT_PATH" != *"03-grand-unified-theory"* ]]; then
    echo "$(date): SKIPPED — no cwd and transcript does not match" >> /tmp/theory-builder-hook.log
    exit 0
  fi
fi

# Parse YAML frontmatter
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$STATE_FILE")
SLUG=$(echo "$FRONTMATTER" | grep '^slug:' | sed 's/slug: *//')
ITERATION=$(echo "$FRONTMATTER" | grep '^iteration:' | sed 's/iteration: *//')
MAX_ITERATIONS=$(echo "$FRONTMATTER" | grep '^max_iterations:' | sed 's/max_iterations: *//')
SESSION_TRANSCRIPT=$(echo "$FRONTMATTER" | grep '^session_transcript:' | sed 's/session_transcript: *//; s/^"//; s/"$//')

# --- Session-aware check ---
if [[ -z "$SESSION_TRANSCRIPT" ]]; then
  # First trigger — claim this session
  TEMP_FILE="${STATE_FILE}.tmp.$$"
  sed "s|^session_transcript: .*|session_transcript: \"$TRANSCRIPT_PATH\"|" "$STATE_FILE" > "$TEMP_FILE"
  mv "$TEMP_FILE" "$STATE_FILE"
elif [[ "$SESSION_TRANSCRIPT" != "$TRANSCRIPT_PATH" ]]; then
  # Different session — let it exit normally
  exit 0
fi

# Validate numeric fields
if [[ ! "$ITERATION" =~ ^[0-9]+$ ]]; then
  echo "Warning: Theory Builder state file corrupted (iteration: $ITERATION). Stopping." >&2
  rm "$STATE_FILE"
  exit 0
fi

if [[ ! "$MAX_ITERATIONS" =~ ^[0-9]+$ ]]; then
  echo "Warning: Theory Builder state file corrupted (max_iterations: $MAX_ITERATIONS). Stopping." >&2
  rm "$STATE_FILE"
  exit 0
fi

# Helper: remove the stop hook from settings.local.json
remove_stop_hook() {
  local settings="/Users/seanross/kingdom_of_god/science/.claude/settings.local.json"
  local hook_cmd="/Users/seanross/kingdom_of_god/science/previous-attempts/03-grand-unified-theory/scripts/theory-builder/theory-builder-stop-hook.sh"
  if [[ -f "$settings" ]] && jq -e ".hooks.Stop[]? | select(.hooks[]?.command == \"$hook_cmd\")" "$settings" > /dev/null 2>&1; then
    jq --arg cmd "$hook_cmd" '.hooks.Stop = [.hooks.Stop[] | select(.hooks | map(.command) | contains([$cmd]) | not)]' "$settings" > "${settings}.tmp.$$"
    mv "${settings}.tmp.$$" "$settings"
  fi
}

# Check if max iterations reached
if [[ $MAX_ITERATIONS -gt 0 ]] && [[ $ITERATION -ge $MAX_ITERATIONS ]]; then
  echo "Theory Builder: Max iterations ($MAX_ITERATIONS) reached."
  echo ""
  echo "   Check GRAND-THEORY.md for accumulated knowledge."
  echo "   Check FINAL-THEORY.md for the final theory (if generated)."
  rm "$STATE_FILE"
  remove_stop_hook
  exit 0
fi

# Check for completion promise in last assistant message
if [[ -f "$TRANSCRIPT_PATH" ]] && grep -q '"role":"assistant"' "$TRANSCRIPT_PATH"; then
  LAST_LINE=$(grep '"role":"assistant"' "$TRANSCRIPT_PATH" | tail -1)

  if [[ -n "$LAST_LINE" ]]; then
    LAST_OUTPUT=$(echo "$LAST_LINE" | jq -r '
      .message.content |
      map(select(.type == "text")) |
      map(.text) |
      join("\n")
    ' 2>/dev/null || echo "")

    if [[ -n "$LAST_OUTPUT" ]]; then
      PROMISE_TEXT=$(echo "$LAST_OUTPUT" | perl -0777 -pe 's/.*?<promise>(.*?)<\/promise>.*/$1/s; s/^\s+|\s+$//g; s/\s+/ /g' 2>/dev/null || echo "")

      if [[ -n "$PROMISE_TEXT" ]] && [[ "$PROMISE_TEXT" = "THEORY BUILDER COMPLETE" ]]; then
        echo "Theory Builder — Grand Unified Theory Research COMPLETE!"
        echo ""
        echo "   Knowledge Document: GRAND-THEORY.md"
        echo "   Final Theory: FINAL-THEORY.md"
        echo "   Calculations: scripts/theory-builder/CALCULATIONS.md"
        echo "   State: scripts/theory-builder/state.json"
        rm "$STATE_FILE"
        remove_stop_hook
        exit 0
      fi
    fi
  fi
fi

# Not complete — continue loop
NEXT_ITERATION=$((ITERATION + 1))

# Update iteration counter
TEMP_FILE="${STATE_FILE}.tmp.$$"
sed "s/^iteration: .*/iteration: $NEXT_ITERATION/" "$STATE_FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$STATE_FILE"

# Build the meta-prompt
META_PROMPT=$(cat <<'PROMPT_EOF'
You are in **Theory Builder — Grand Unified Theory Research Loop** mode. Continue your autonomous research.

## Every Iteration — Follow This Checklist

1. **Read** `GRAND-THEORY.md` — the living knowledge document (source of truth for everything established)
2. **Read** `scripts/theory-builder/PROMPT.md` — the full research protocol (three-phase cycle: Theorize, Investigate, Verdict)
3. **Read** `scripts/theory-builder/HANDOFF.md` — where you left off last iteration and what to do next
4. **Read** `scripts/theory-builder/state.json` — structured state (iteration, phase, current theory)
5. **Determine phase** based on HANDOFF.md:
   - Phase A (Theorize): Generate candidate theories for the current frontier
   - Phase B (Investigate): Do the math — calculate, verify, scrutinize
   - Phase C (Verdict): Assess results, update knowledge, choose next direction
6. **Execute** the iteration following the protocol in PROMPT.md
7. **Update ALL state files** — GRAND-THEORY.md, state.json, HANDOFF.md, CALCULATIONS.md

## Key Principles
- **Math or it did not happen** — every claim must be backed by a calculation
- **Adversarial rigor** — always include a Skeptic agent to challenge results
- **Fail fast** — if something does not work, record why and move on
- **Update the knowledge doc** — every iteration must leave GRAND-THEORY.md richer
- **Be bold** — you are trying to unify physics, take calculated risks
- **Build on FDCG** — the fracton dipole condensate framework is the foundation
- **Testable predictions** — push for predictions at every stage
- **Cross-pollinate** — connect different fields, look for unexpected links

## Completion
When ALL iterations are done OR you believe the theory is sufficiently complete, write `FINAL-THEORY.md` then output:
`<promise>THEORY BUILDER COMPLETE</promise>`

IMPORTANT: Only output the promise when you have genuinely completed all iterations and generated the final theory document.
PROMPT_EOF
)

SYSTEM_MSG="Theory Builder — Grand Unified Theory, iteration $NEXT_ITERATION of $MAX_ITERATIONS"

# Output JSON to block the stop and feed the meta-prompt
jq -n \
  --arg prompt "$META_PROMPT" \
  --arg msg "$SYSTEM_MSG" \
  '{
    "decision": "block",
    "reason": $prompt,
    "systemMessage": $msg
  }'

exit 0
