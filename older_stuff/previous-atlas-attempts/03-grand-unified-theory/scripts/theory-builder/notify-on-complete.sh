#!/bin/bash

# Monitor the Theory Builder research loop and send a Telegram notification when done.
# Checks every 2 minutes.

set -euo pipefail

source /Users/seanross/kingdom_of_god/serve_boldly/.env

STATE_DIR="/Users/seanross/kingdom_of_god/grand-unified-theory/scripts/theory-builder"
STATE_FILE="$STATE_DIR/state.json"
LOOP_STATE="$STATE_DIR/LOOP-STATE.md"

echo "Monitoring Theory Builder research loop for completion..."
echo "   Checking every 2 minutes."
echo "   PID: $$"

while true; do
  # Check if done flag is set in state.json
  DONE=$(jq -r '.done' "$STATE_FILE" 2>/dev/null || echo "false")
  ITERATION=$(jq -r '.iteration' "$STATE_FILE" 2>/dev/null || echo "?")
  PHASE=$(jq -r '.current_phase' "$STATE_FILE" 2>/dev/null || echo "?")
  FRONTIER=$(jq -r '.current_frontier // "none"' "$STATE_FILE" 2>/dev/null || echo "?")
  ESTABLISHED=$(jq -r '.established_count' "$STATE_FILE" 2>/dev/null || echo "?")
  DEAD_ENDS=$(jq -r '.dead_ends_count' "$STATE_FILE" 2>/dev/null || echo "?")

  # Loop is done if: done=true OR LOOP-STATE.md is gone (hook cleaned it up)
  if [[ "$DONE" == "true" ]] || [[ ! -f "$LOOP_STATE" ]]; then
    echo "Research loop complete! Sending Telegram..."

    # Play sound notification
    say "Theory Builder research loop is complete. Check the results." &

    MESSAGE="*Grand Unified Theory — Theory Builder COMPLETE*

Iteration $ITERATION | $ESTABLISHED established results | $DEAD_ENDS dead ends

*How to see results:*

*Knowledge Document* (the good stuff):
\`cat ~/kingdom_of_god/grand-unified-theory/GRAND-THEORY.md\`

*Final Theory* (if generated):
\`cat ~/kingdom_of_god/grand-unified-theory/FINAL-THEORY.md\`

*Calculations*:
\`cat ~/kingdom_of_god/grand-unified-theory/scripts/theory-builder/CALCULATIONS.md\`

*Full State*:
\`cat ~/kingdom_of_god/grand-unified-theory/scripts/theory-builder/state.json | jq .\`

*Last Handoff*:
\`cat ~/kingdom_of_god/grand-unified-theory/scripts/theory-builder/HANDOFF.md\`"

    printf '%s' "{\"message\":$(echo "$MESSAGE" | jq -Rs .)}" | curl -s -X POST "https://bkylbyjmbgulyedyyplo.supabase.co/functions/v1/telegram-me" \
      -H "Authorization: Bearer $VITE_SUPABASE_PUBLISHABLE_KEY" \
      -H "Content-Type: application/json" -d @-

    echo ""
    echo "Notification sent! Exiting monitor."
    exit 0
  fi

  echo "   [$(date '+%H:%M')] Iteration $ITERATION | Phase $PHASE | Frontier: $FRONTIER | Established: $ESTABLISHED | Dead ends: $DEAD_ENDS. Still running..."
  sleep 120
done
