#!/bin/bash

# Monitor the DQCP formalization research loop and send a Telegram notification when done.
# Checks every 2 minutes.

set -euo pipefail

source /Users/seanross/kingdom_of_god/serve_boldly/.env

STATE_DIR="/Users/seanross/kingdom_of_god/worktrees/serve_boldly_dqcp-formalize/scripts/dqcp-formalize"
STATE_FILE="$STATE_DIR/state.json"
LOOP_STATE="$STATE_DIR/LOOP-STATE.md"

echo "🔬 Monitoring DQCP formalization research loop for completion..."
echo "   Checking every 2 minutes."
echo "   PID: $$"

while true; do
  # Check if done flag is set in state.json
  DONE=$(jq -r '.done' "$STATE_FILE" 2>/dev/null || echo "false")
  ITERATION=$(jq -r '.iteration' "$STATE_FILE" 2>/dev/null || echo "?")
  CONFIDENCE=$(jq -r '.confidence' "$STATE_FILE" 2>/dev/null || echo "?")
  ANSWERED=$(jq -r '.questions_answered | length' "$STATE_FILE" 2>/dev/null || echo "?")
  TOTAL_Q=$(jq -r '.open_questions | length' "$STATE_FILE" 2>/dev/null || echo "?")

  # Loop is done if: done=true OR LOOP-STATE.md is gone (hook cleaned it up)
  if [[ "$DONE" == "true" ]] || [[ ! -f "$LOOP_STATE" ]]; then
    echo "✅ Research loop complete! Sending Telegram..."

    MESSAGE="🔬 *DQCP Formalization Research Loop — COMPLETE*

$ANSWERED questions answered, confidence: $CONFIDENCE%.

*How to see results:*

📖 *Final Verdict* (the main result):
\`cat ~/kingdom_of_god/worktrees/serve_boldly_dqcp-formalize/scripts/dqcp-formalize/FINAL-VERDICT.md\`

📊 *Results Catalog* (all derivations):
\`cat ~/kingdom_of_god/worktrees/serve_boldly_dqcp-formalize/scripts/dqcp-formalize/RESULTS.md\`

📈 *Full State* (confidence, evidence, learnings):
\`cat ~/kingdom_of_god/worktrees/serve_boldly_dqcp-formalize/scripts/dqcp-formalize/state.json | jq .\`

🧠 *Quick summary*:
\`cat ~/kingdom_of_god/worktrees/serve_boldly_dqcp-formalize/scripts/dqcp-formalize/HANDOFF.md\`"

    printf '%s' "{\"message\":$(echo "$MESSAGE" | jq -Rs .)}" | curl -s -X POST "https://bkylbyjmbgulyedyyplo.supabase.co/functions/v1/telegram-me" \
      -H "Authorization: Bearer $VITE_SUPABASE_PUBLISHABLE_KEY" \
      -H "Content-Type: application/json" -d @-

    echo ""
    echo "✅ Notification sent! Exiting monitor."
    exit 0
  fi

  echo "   [$(date '+%H:%M')] Iteration $ITERATION — $ANSWERED/$TOTAL_Q questions answered, confidence: $CONFIDENCE%. Still running..."
  sleep 120
done
