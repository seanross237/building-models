#!/bin/bash

# DQCP Formalization Research Loop — Stop Hook
# Keeps the autonomous research loop going by feeding a meta-prompt each iteration.
# Only activates when scripts/dqcp-formalize/LOOP-STATE.md exists.
# SESSION-AWARE: Only traps the session that started the loop.

set -euo pipefail

# Read hook input from stdin
HOOK_INPUT=$(cat)

STATE_DIR="scripts/dqcp-formalize"
STATE_FILE="$STATE_DIR/LOOP-STATE.md"

# Emergency escape hatch
if [[ -f "$STATE_DIR/PAUSE_HOOK" ]]; then
  exit 0
fi

# Check if loop is active
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0
fi

# Get this session's transcript path
TRANSCRIPT_PATH=$(echo "$HOOK_INPUT" | jq -r '.transcript_path')

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
  echo "⚠️  DQCP Formalize: State file corrupted (iteration: '$ITERATION'). Stopping." >&2
  rm "$STATE_FILE"
  exit 0
fi

if [[ ! "$MAX_ITERATIONS" =~ ^[0-9]+$ ]]; then
  echo "⚠️  DQCP Formalize: State file corrupted (max_iterations: '$MAX_ITERATIONS'). Stopping." >&2
  rm "$STATE_FILE"
  exit 0
fi

# Helper: remove the stop hook from settings.local.json
remove_stop_hook() {
  local settings=".claude/settings.local.json"
  local hook_cmd="./scripts/dqcp-formalize/dqcp-stop-hook.sh"
  if [[ -f "$settings" ]] && jq -e ".hooks.Stop[]? | select(.hooks[]?.command == \"$hook_cmd\")" "$settings" > /dev/null 2>&1; then
    jq --arg cmd "$hook_cmd" '.hooks.Stop = [.hooks.Stop[] | select(.hooks | map(.command) | contains([$cmd]) | not)]' "$settings" > "${settings}.tmp.$$"
    mv "${settings}.tmp.$$" "$settings"
  fi
}

# Check if max iterations reached
if [[ $MAX_ITERATIONS -gt 0 ]] && [[ $ITERATION -ge $MAX_ITERATIONS ]]; then
  echo "🛑 DQCP Formalize: Max iterations ($MAX_ITERATIONS) reached."
  echo ""
  echo "   Check scripts/dqcp-formalize/RESULTS.md for accumulated results."
  echo "   Check scripts/dqcp-formalize/FINAL-VERDICT.md for the final verdict (if generated)."
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

      if [[ -n "$PROMISE_TEXT" ]] && [[ "$PROMISE_TEXT" = "DQCP FORMALIZATION COMPLETE" ]]; then
        echo "✅ DQCP Formalization Research Loop complete!"
        echo ""
        echo "   Final Verdict: scripts/dqcp-formalize/FINAL-VERDICT.md"
        echo "   Results Catalog: scripts/dqcp-formalize/RESULTS.md"
        echo "   State: scripts/dqcp-formalize/state.json"
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
You are in **DQCP Formalization Research Loop** mode. Continue your autonomous research.

## Every Iteration — Follow This Checklist

1. **Read** `scripts/dqcp-formalize/PROMPT.md` — the full research protocol
2. **Read** `scripts/dqcp-formalize/HANDOFF.md` — where you left off last iteration and what to tackle next
3. **Read** `scripts/dqcp-formalize/state.json` — full research state
4. **Read** `scripts/dqcp-formalize/RESULTS.md` — accumulated results catalog
5. **Execute** the next iteration following the protocol in PROMPT.md
6. **Update** all state files (state.json, RESULTS.md, HANDOFF.md)

## Key Principles
- **Rigor first** — every claim must have math behind it. This is a formalization project.
- **Always have a Skeptic** — at least one agent per iteration should be trying to disprove the DQCP claim
- **Honest verdicts** — "It's NOT a DQCP" is a perfectly valid conclusion. Don't force the result.
- **Stay focused** — you're answering ONE question: is the FDCG transition a DQCP?
- **Build on published DQCP literature** — use what's known about DQCPs in condensed matter as your guide
- **Failures are data** — a clean failure that rules something out is more useful than a vague success

## Completion
When ALL iterations are done (or you've reached a definitive verdict), write `scripts/dqcp-formalize/FINAL-VERDICT.md` then output:
`<promise>DQCP FORMALIZATION COMPLETE</promise>`

IMPORTANT: Only output the promise when you have genuinely completed all iterations and generated the verdict.
PROMPT_EOF
)

SYSTEM_MSG="🔬 DQCP Formalization — iteration $NEXT_ITERATION of $MAX_ITERATIONS"

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
