#!/bin/bash

# Usain Bolt Stop Hook
# Keeps the autonomous sprint loop going by feeding a meta-prompt each iteration.
# Only activates when .usain-bolt/USAIN-BOLT-STATE.md exists.
# SESSION-AWARE: Only traps the session that started the sprint.

set -euo pipefail

# Read hook input from stdin
HOOK_INPUT=$(cat)

# Emergency escape hatch: create .usain-bolt/PAUSE_HOOK to disable for ALL sessions
if [[ -f ".usain-bolt/PAUSE_HOOK" ]]; then
  exit 0
fi

# Check if sprint is active
STATE_FILE=".usain-bolt/USAIN-BOLT-STATE.md"

if [[ ! -f "$STATE_FILE" ]]; then
  # No active sprint — allow normal exit
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
# If session_transcript is empty, this is the first trigger after setup.
# Claim the sprint for this session by recording its transcript path.
if [[ -z "$SESSION_TRANSCRIPT" ]]; then
  # First trigger — claim this session as the sprinter
  TEMP_FILE="${STATE_FILE}.tmp.$$"
  sed "s|^session_transcript: .*|session_transcript: \"$TRANSCRIPT_PATH\"|" "$STATE_FILE" > "$TEMP_FILE"
  mv "$TEMP_FILE" "$STATE_FILE"
elif [[ "$SESSION_TRANSCRIPT" != "$TRANSCRIPT_PATH" ]]; then
  # Different session — let it exit normally
  exit 0
fi
# If we get here, this IS the sprinting session — continue with the loop

# Validate numeric fields
if [[ ! "$ITERATION" =~ ^[0-9]+$ ]]; then
  echo "Usain Bolt: State file corrupted (iteration: '$ITERATION'). Stopping." >&2
  rm "$STATE_FILE"
  exit 0
fi

if [[ ! "$MAX_ITERATIONS" =~ ^[0-9]+$ ]]; then
  echo "Usain Bolt: State file corrupted (max_iterations: '$MAX_ITERATIONS'). Stopping." >&2
  rm "$STATE_FILE"
  exit 0
fi

# Helper: remove the stop hook from settings.local.json
remove_stop_hook() {
  local settings=".claude/settings.local.json"
  if [[ -f "$settings" ]] && jq -e '.hooks.Stop[]? | select(.hooks[]?.command == "./scripts/usain-bolt/usain-bolt-stop-hook.sh")' "$settings" > /dev/null 2>&1; then
    jq '.hooks.Stop = [.hooks.Stop[] | select(.hooks | map(.command) | contains(["./scripts/usain-bolt/usain-bolt-stop-hook.sh"]) | not)]' "$settings" > "${settings}.tmp.$$"
    mv "${settings}.tmp.$$" "$settings"
  fi
}

# Check if max iterations reached
if [[ $MAX_ITERATIONS -gt 0 ]] && [[ $ITERATION -ge $MAX_ITERATIONS ]]; then
  echo "Usain Bolt: Max iterations ($MAX_ITERATIONS) reached."
  echo ""
  echo "   Check .usain-bolt/USAIN-BOLT-${SLUG}-PROGRESS.md for status."
  echo "   Check .usain-bolt/USAIN-BOLT-${SLUG}-REPORT.md for the final report (if generated)."
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

      if [[ -n "$PROMISE_TEXT" ]] && [[ "$PROMISE_TEXT" = "SPRINT COMPLETE" ]]; then
        echo "Usain Bolt sprint complete!"
        echo ""
        echo "   Report:   .usain-bolt/USAIN-BOLT-${SLUG}-REPORT.md"
        echo "   Progress: .usain-bolt/USAIN-BOLT-${SLUG}-PROGRESS.md"
        rm "$STATE_FILE"
        remove_stop_hook
        exit 0
      fi
    fi
  fi
fi

# Not complete — continue loop
NEXT_ITERATION=$((ITERATION + 1))

# Update iteration counter in state file
TEMP_FILE="${STATE_FILE}.tmp.$$"
sed "s/^iteration: .*/iteration: $NEXT_ITERATION/" "$STATE_FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$STATE_FILE"

# Build the meta-prompt
META_PROMPT=$(cat <<PROMPT_EOF
You are in **Usain Bolt sprint mode**. Keep sprinting.

The feature slug for this sprint is **${SLUG}**. All sprint files use this slug.

## Every Iteration — Follow This Checklist

1. **Read** \`.usain-bolt/USAIN-BOLT-${SLUG}-HANDOFF.md\` — where you left off last iteration
2. **Read** \`.usain-bolt/USAIN-BOLT-${SLUG}-PROGRESS.md\` — the full checklist of work items
3. **Read** \`.usain-bolt/USAIN-BOLT-${SLUG}-PLAN.md\` if you need full context on what's being built
4. **Work** on the next incomplete item in the progress checklist
5. **Update** \`.usain-bolt/USAIN-BOLT-${SLUG}-PROGRESS.md\` — check off completed items, update attempt counts
6. **Update** \`.usain-bolt/USAIN-BOLT-${SLUG}-HANDOFF.md\` before finishing — write what you did, where you stopped, what's next

## Handling Blocks
When something is not working:
- **Attempts 1-3**: Keep trying with adjusted approach
- **Attempt 4**: Try a fundamentally different approach
- **Attempt 5**: Mark as BLOCKED in PROGRESS.md, move to next item

## Testing
Test your work as you go. Do not save all testing for the end.

## Completion
When ALL items in PROGRESS.md are either complete or blocked:
1. Generate \`.usain-bolt/USAIN-BOLT-${SLUG}-REPORT.md\` with:
   - **Summary**: What was built
   - **How to see it**: URLs, commands, pages to visit
   - **How to test it**: Steps to verify
   - **Blocked items**: What could not be completed and why
2. Then output: <promise>SPRINT COMPLETE</promise>

IMPORTANT: Only output the promise when you have genuinely completed all items and generated the report. Do not lie to exit the loop.
PROMPT_EOF
)

SYSTEM_MSG="Usain Bolt ($SLUG) — iteration $NEXT_ITERATION of $MAX_ITERATIONS"

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
