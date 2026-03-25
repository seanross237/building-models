#!/bin/bash

# Monitor the quantum gravity research loop and send a Telegram notification when done.
# Checks every 2 minutes.

set -euo pipefail

source /Users/seanross/kingdom_of_god/serve_boldly/.env

STATE_DIR="/Users/seanross/kingdom_of_god/worktrees/serve_boldly_quantum-gravity/scripts/quantum-gravity"
STATE_FILE="$STATE_DIR/state.json"
LOOP_STATE="$STATE_DIR/LOOP-STATE.md"

echo "🔬 Monitoring quantum gravity research loop for completion..."
echo "   Checking every 2 minutes."
echo "   PID: $$"

while true; do
  # Check if done flag is set in state.json
  DONE=$(jq -r '.done' "$STATE_FILE" 2>/dev/null || echo "false")
  ITERATION=$(jq -r '.iteration' "$STATE_FILE" 2>/dev/null || echo "?")
  PROMISING=$(jq -r '.promising_theories | length' "$STATE_FILE" 2>/dev/null || echo "?")
  TOTAL=$(jq -r '.theories_explored | length' "$STATE_FILE" 2>/dev/null || echo "?")

  # Loop is done if: done=true OR LOOP-STATE.md is gone (hook cleaned it up)
  if [[ "$DONE" == "true" ]] || [[ ! -f "$LOOP_STATE" ]]; then
    echo "✅ Research loop complete! Sending Telegram..."

    MESSAGE="🔬 *Quantum Gravity Research Loop — COMPLETE*

$TOTAL theories explored, $PROMISING promising.

*How to see results:*

📖 *Theory Catalog* (the good stuff):
\`cat ~/kingdom_of_god/worktrees/serve_boldly_quantum-gravity/scripts/quantum-gravity/THEORIES.md\`

📊 *Final Report* (if generated):
\`cat ~/kingdom_of_god/worktrees/serve_boldly_quantum-gravity/scripts/quantum-gravity/FINAL-REPORT.md\`

📈 *Full State* (scores, connections, learnings):
\`cat ~/kingdom_of_god/worktrees/serve_boldly_quantum-gravity/scripts/quantum-gravity/state.json | jq .\`

🧠 *Quick summary*:
\`cat ~/kingdom_of_god/worktrees/serve_boldly_quantum-gravity/scripts/quantum-gravity/HANDOFF.md\`"

    printf '%s' "{\"message\":$(echo "$MESSAGE" | jq -Rs .)}" | curl -s -X POST "https://bkylbyjmbgulyedyyplo.supabase.co/functions/v1/telegram-me" \
      -H "Authorization: Bearer $VITE_SUPABASE_PUBLISHABLE_KEY" \
      -H "Content-Type: application/json" -d @-

    echo ""
    echo "✅ Notification sent! Exiting monitor."
    exit 0
  fi

  echo "   [$(date '+%H:%M')] Iteration $ITERATION — $TOTAL theories, $PROMISING promising. Still running..."
  sleep 120
done
