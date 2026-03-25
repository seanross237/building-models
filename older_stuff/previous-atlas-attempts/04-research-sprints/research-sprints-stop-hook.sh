#!/bin/bash

# Research Sprints — Focused Physics Investigation Loop Stop Hook
# Keeps the autonomous sprint loop going by feeding a meta-prompt each iteration.
# Only activates when LOOP-STATE.md exists in the research-sprints directory.
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
echo "$(date): HOOK FIRED" >> /tmp/research-sprints-hook.log
echo "$HOOK_INPUT" >> /tmp/research-sprints-hook.log

# Only activate for sessions running inside 04-research-sprints/
SESSION_CWD=$(echo "$HOOK_INPUT" | jq -r '.cwd // empty')
TRANSCRIPT_PATH=$(echo "$HOOK_INPUT" | jq -r '.transcript_path // empty')

if [[ -n "$SESSION_CWD" ]] && [[ "$SESSION_CWD" != *"04-research-sprints"* ]]; then
  # CWD does not match — check transcript path as fallback
  if [[ "$TRANSCRIPT_PATH" != *"04-research-sprints"* ]]; then
    echo "$(date): SKIPPED — cwd=$SESSION_CWD, transcript=$TRANSCRIPT_PATH" >> /tmp/research-sprints-hook.log
    exit 0
  fi
elif [[ -z "$SESSION_CWD" ]]; then
  if [[ "$TRANSCRIPT_PATH" != *"04-research-sprints"* ]]; then
    echo "$(date): SKIPPED — no cwd and transcript does not match" >> /tmp/research-sprints-hook.log
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
  echo "Warning: Research Sprints state file corrupted (iteration: $ITERATION). Stopping." >&2
  rm "$STATE_FILE"
  exit 0
fi

if [[ ! "$MAX_ITERATIONS" =~ ^[0-9]+$ ]]; then
  echo "Warning: Research Sprints state file corrupted (max_iterations: $MAX_ITERATIONS). Stopping." >&2
  rm "$STATE_FILE"
  exit 0
fi

# Helper: remove the stop hook from settings.local.json
remove_stop_hook() {
  local settings="/Users/seanross/kingdom_of_god/science/.claude/settings.local.json"
  local hook_cmd="/Users/seanross/kingdom_of_god/science/previous-attempts/04-research-sprints/research-sprints-stop-hook.sh"
  if [[ -f "$settings" ]] && jq -e ".hooks.Stop[]? | select(.hooks[]?.command == \"$hook_cmd\")" "$settings" > /dev/null 2>&1; then
    jq --arg cmd "$hook_cmd" '.hooks.Stop = [.hooks.Stop[] | select(.hooks | map(.command) | contains([$cmd]) | not)]' "$settings" > "${settings}.tmp.$$"
    mv "${settings}.tmp.$$" "$settings"
  fi
}

# Check if max iterations reached
if [[ $MAX_ITERATIONS -gt 0 ]] && [[ $ITERATION -ge $MAX_ITERATIONS ]]; then
  echo "Research Sprints: Max iterations ($MAX_ITERATIONS) reached."
  echo ""
  echo "   Check KNOWLEDGE.md for accumulated findings."
  echo "   Check FINAL-SUMMARY.md for the final summary (if generated)."
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

      if [[ -n "$PROMISE_TEXT" ]] && [[ "$PROMISE_TEXT" = "RESEARCH SPRINTS COMPLETE" ]]; then
        echo "Research Sprints — Focused Physics Investigation COMPLETE!"
        echo ""
        echo "   Knowledge Document: KNOWLEDGE.md"
        echo "   Final Summary: FINAL-SUMMARY.md"
        echo "   Sprint Records: sprints/"
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
You are in **Research Sprints — Focused Physics Investigation** mode. Continue your autonomous research.

## Every Iteration — Follow This Checklist

1. **Read** `PROMPT.md` — the full sprint protocol (SEED, SPRINT, REGROUP cycle)
2. **Read** `KNOWLEDGE.md` — accumulated findings from all completed sprints
3. **Read** `HANDOFF.md` — where you left off last iteration and what to do next
4. **Read** `state.json` — structured state (iteration, phase, current sprint)
5. **Read the validation suite** at `~/kingdom_of_god/science/validation/` when you need experimental data or test criteria
6. **Read** `~/kingdom_of_god/science/previous-attempts/03-grand-unified-theory/GRAND-THEORY.md` when you need foundation knowledge
7. **Determine phase** based on HANDOFF.md:
   - SEED: Generate 3-5 focused questions, pick the best one
   - SPRINT: Execute the current question (2-3 iterations max)
   - REGROUP: Record results, look for patterns, pick next sprint
8. **Execute** the iteration following the protocol in PROMPT.md
9. **Update ALL state files** — KNOWLEDGE.md, state.json, HANDOFF.md, sprint record file

## Key Principles
- **Max 3 iterations per question** — if you cannot answer it in 3, record what you learned and move on
- **Always have a Skeptic** — no exceptions, every sprint needs adversarial review
- **Use real data when possible** — check the validation suite for datasets and experimental values
- **Aggressive pivoting** — if something does not work, do NOT try a slight variation, step way back
- **Failures are valuable** — a clean "no" is worth more than a vague "maybe"
- **Record everything** — every sprint gets a file in sprints/ with question, method, result, and lessons
- **Math or it did not happen** — every claim must be backed by a calculation
- **Build on FDCG** — the fracton dipole condensate framework is the foundation
- **Testable predictions** — push for predictions at every stage

## Completion
When ALL iterations are done OR you believe the research is sufficiently complete, write `FINAL-SUMMARY.md` then output:
`<promise>RESEARCH SPRINTS COMPLETE</promise>`

IMPORTANT: Only output the promise when you have genuinely completed all iterations and generated the final summary document.
PROMPT_EOF
)

SYSTEM_MSG="Research Sprints — Focused Physics Investigation, iteration $NEXT_ITERATION of $MAX_ITERATIONS"

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
