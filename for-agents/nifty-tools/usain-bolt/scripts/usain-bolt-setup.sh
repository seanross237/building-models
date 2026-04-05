#!/bin/bash

# Usain Bolt Setup Script
# Creates USAIN-BOLT-STATE.md to activate the autonomous sprint loop

set -euo pipefail

# Parse arguments
MAX_ITERATIONS=30
SLUG=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --max-iterations)
      if [[ -z "${2:-}" ]]; then
        echo "Error: --max-iterations requires a number" >&2
        exit 1
      fi
      if ! [[ "$2" =~ ^[0-9]+$ ]]; then
        echo "Error: --max-iterations must be a positive integer, got: $2" >&2
        exit 1
      fi
      MAX_ITERATIONS="$2"
      shift 2
      ;;
    --slug)
      if [[ -z "${2:-}" ]]; then
        echo "Error: --slug requires a value (e.g., lyrics-page)" >&2
        exit 1
      fi
      SLUG="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

if [[ -z "$SLUG" ]]; then
  echo "Error: --slug is required (e.g., --slug lyrics-page)" >&2
  exit 1
fi

# Check if a sprint is already active
if [[ -f ".usain-bolt/USAIN-BOLT-STATE.md" ]]; then
  CURRENT_ITERATION=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' ".usain-bolt/USAIN-BOLT-STATE.md" | grep '^iteration:' | sed 's/iteration: *//')
  echo "A sprint is already active (iteration $CURRENT_ITERATION)" >&2
  echo "   Run /cancel-usain-bolt first to start fresh." >&2
  exit 1
fi

# Verify plan files exist (using slug-based names)
MISSING=()
[[ ! -f ".usain-bolt/USAIN-BOLT-${SLUG}-PLAN.md" ]] && MISSING+=("USAIN-BOLT-${SLUG}-PLAN.md")
[[ ! -f ".usain-bolt/USAIN-BOLT-${SLUG}-PROGRESS.md" ]] && MISSING+=("USAIN-BOLT-${SLUG}-PROGRESS.md")

if [[ ${#MISSING[@]} -gt 0 ]]; then
  echo "Error: Missing required plan files:" >&2
  for f in "${MISSING[@]}"; do
    echo "   - .usain-bolt/$f" >&2
  done
  echo "" >&2
  echo "   Write the plan files before activating the sprint." >&2
  exit 1
fi

# Create state file
# session_transcript is empty initially — the stop hook will record the
# building session's transcript path on first trigger (session-aware lock)
cat > ".usain-bolt/USAIN-BOLT-STATE.md" <<EOF
---
active: true
slug: $SLUG
iteration: 1
max_iterations: $MAX_ITERATIONS
session_transcript: ""
started_at: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
---
EOF

# Clean up any leftover pause file
rm -f ".usain-bolt/PAUSE_HOOK"

# Dynamically add the stop hook to settings.local.json (if not already present)
SETTINGS_FILE=".claude/settings.local.json"
if [[ -f "$SETTINGS_FILE" ]]; then
  if ! jq -e '.hooks.Stop[]? | select(.hooks[]?.command == "./scripts/usain-bolt/usain-bolt-stop-hook.sh")' "$SETTINGS_FILE" > /dev/null 2>&1; then
    jq '.hooks.Stop = [{"hooks":[{"type":"command","command":"./scripts/usain-bolt/usain-bolt-stop-hook.sh"}]}] + .hooks.Stop' "$SETTINGS_FILE" > "${SETTINGS_FILE}.tmp.$$"
    mv "${SETTINGS_FILE}.tmp.$$" "$SETTINGS_FILE"
    echo "   Hook added to settings.local.json"
  fi
fi

# Output activation message
cat <<EOF
Usain Bolt sprint activated! ($SLUG)

   Iteration: 1
   Max iterations: $MAX_ITERATIONS

   State:    .usain-bolt/USAIN-BOLT-STATE.md
   Plan:     .usain-bolt/USAIN-BOLT-${SLUG}-PLAN.md
   Progress: .usain-bolt/USAIN-BOLT-${SLUG}-PROGRESS.md
   Handoff:  .usain-bolt/USAIN-BOLT-${SLUG}-HANDOFF.md

   The stop hook is now active. Each time you finish a turn,
   you'll receive a meta-prompt to continue working.

   Only THIS session will be trapped — other sessions can exit normally.

   To cancel: /cancel-usain-bolt
EOF
