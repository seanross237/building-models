#!/bin/bash

# Quantum Gravity Research Loop Setup Script
# Creates state files and activates the autonomous research loop

set -euo pipefail

# Parse arguments
MAX_ITERATIONS=30

while [[ $# -gt 0 ]]; do
  case $1 in
    --max-iterations)
      if [[ -z "${2:-}" ]]; then
        echo "❌ Error: --max-iterations requires a number" >&2
        exit 1
      fi
      if ! [[ "$2" =~ ^[0-9]+$ ]]; then
        echo "❌ Error: --max-iterations must be a positive integer, got: $2" >&2
        exit 1
      fi
      MAX_ITERATIONS="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

SLUG="quantum-gravity"
STATE_DIR="scripts/quantum-gravity"

# Check if already active
if [[ -f "$STATE_DIR/LOOP-STATE.md" ]]; then
  CURRENT_ITERATION=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$STATE_DIR/LOOP-STATE.md" | grep '^iteration:' | sed 's/iteration: *//')
  echo "⚠️  Quantum Gravity loop is already active (iteration $CURRENT_ITERATION)" >&2
  echo "   Run /cancel-quantum-gravity first to start fresh." >&2
  exit 1
fi

# Initialize state.json if it doesn't exist
if [[ ! -f "$STATE_DIR/state.json" ]]; then
  cat > "$STATE_DIR/state.json" <<'STATEOF'
{
  "iteration": 0,
  "done": false,
  "target_iterations": 30,
  "theories_explored": [],
  "promising_theories": [],
  "dead_ends": [],
  "research_frontiers": [
    {
      "direction": "Spacetime Emergence",
      "promise": "high",
      "notes": "Unexplored — entanglement, information, computation"
    },
    {
      "direction": "Modified Gravity",
      "promise": "medium",
      "notes": "Unexplored — modifications to GR for quantization"
    },
    {
      "direction": "Extended Quantum Mechanics",
      "promise": "medium",
      "notes": "Unexplored — objective collapse, non-linear QM"
    },
    {
      "direction": "Mathematical Frameworks",
      "promise": "high",
      "notes": "Unexplored — non-commutative geometry, category theory, topos theory"
    },
    {
      "direction": "Information-Theoretic",
      "promise": "high",
      "notes": "Unexplored — holography, ER=EPR, computational gravity"
    },
    {
      "direction": "Discrete Approaches",
      "promise": "medium",
      "notes": "Unexplored — causal sets, CDT, spin foams"
    },
    {
      "direction": "Emergent/Analog",
      "promise": "medium",
      "notes": "Unexplored — condensed matter analogs, thermodynamic gravity"
    },
    {
      "direction": "Radical Departures",
      "promise": "unknown",
      "notes": "Unexplored — reject assumptions of both QM and GR"
    }
  ],
  "cross_connections": [],
  "learnings": [],
  "strategies_tried": []
}
STATEOF
  echo "   Created state.json"
fi

# Initialize THEORIES.md
if [[ ! -f "$STATE_DIR/THEORIES.md" ]]; then
  cat > "$STATE_DIR/THEORIES.md" <<'THEORIESEOF'
# Quantum Gravity Theory Catalog

A living document of theories explored by the autonomous research loop.

## Promising Theories (Score >= 7)

(none yet)

## Interesting Theories (Score 5-6)

(none yet)

## Dead Ends

(none yet)

---

*This catalog is updated each iteration by the research loop.*
THEORIESEOF
  echo "   Created THEORIES.md"
fi

# Initialize HANDOFF.md
if [[ ! -f "$STATE_DIR/HANDOFF.md" ]]; then
  cat > "$STATE_DIR/HANDOFF.md" <<'HANDOFFEOF'
# Quantum Gravity Research — Handoff

## Current Status
Starting first iteration. No theories explored yet.

## Last Explored
(none)

## Recommended Next Direction
Start with **Spacetime Emergence** or **Information-Theoretic** approaches — these are the most active areas of current research and likely to produce interesting results early.

## Cross-Connections to Pursue
(none yet)

## Notes
This is the first iteration. Cast a wide net and see what sticks.
HANDOFFEOF
  echo "   Created HANDOFF.md"
fi

# Create loop state file (activates the stop hook)
cat > "$STATE_DIR/LOOP-STATE.md" <<EOF
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
rm -f "$STATE_DIR/PAUSE_HOOK"

# Dynamically add the stop hook to settings.local.json
SETTINGS_FILE=".claude/settings.local.json"
HOOK_CMD="./scripts/quantum-gravity/quantum-gravity-stop-hook.sh"

if [[ -f "$SETTINGS_FILE" ]]; then
  if ! jq -e ".hooks.Stop[]? | select(.hooks[]?.command == \"$HOOK_CMD\")" "$SETTINGS_FILE" > /dev/null 2>&1; then
    jq --arg cmd "$HOOK_CMD" '.hooks.Stop = [{"hooks":[{"type":"command","command":$cmd}]}] + .hooks.Stop' "$SETTINGS_FILE" > "${SETTINGS_FILE}.tmp.$$"
    mv "${SETTINGS_FILE}.tmp.$$" "$SETTINGS_FILE"
    echo "   Hook added to settings.local.json"
  fi
fi

# Output activation message
cat <<EOF
🔬 Quantum Gravity Research Loop activated!

   Iteration: 1
   Max iterations: $MAX_ITERATIONS

   State:    $STATE_DIR/state.json
   Theories: $STATE_DIR/THEORIES.md
   Handoff:  $STATE_DIR/HANDOFF.md
   Loop:     $STATE_DIR/LOOP-STATE.md

   The stop hook is now active. Each time you finish a turn,
   you'll receive a meta-prompt to continue researching.

   Only THIS session will be trapped — other sessions can exit normally.

   To cancel: /cancel-quantum-gravity
EOF
