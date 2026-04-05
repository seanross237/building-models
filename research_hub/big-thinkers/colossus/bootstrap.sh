#!/bin/bash
# =============================================================================
# Colossus Bootstrap
# =============================================================================
# Starts the controller loop in a tmux session.
# The controller runs every 5 minutes, reads state, makes decisions,
# spawns workers, and exits. Workers run in separate tmux windows.
#
# Usage:
#   ./bootstrap.sh          Start the controller
#   tmux attach -t colossus Watch it work
#   tmux kill-session -t colossus   Stop everything
# =============================================================================

set -e

COLOSSUS_DIR="$(cd "$(dirname "$0")" && pwd)"

# --- Preflight checks ---

# Budget must be set
if grep -q '____' "$COLOSSUS_DIR/BUDGET.md"; then
    echo "ERROR: Set your daily budget in BUDGET.md before starting."
    echo "  Replace \$____ with your daily spend limit (e.g., \$50)."
    exit 1
fi

# tmux must be available
if ! command -v tmux &> /dev/null; then
    echo "ERROR: tmux is required. Install with: brew install tmux"
    exit 1
fi

# claude must be available
if ! command -v claude &> /dev/null; then
    echo "ERROR: claude CLI not found in PATH."
    exit 1
fi

# Kill existing session if running
if tmux has-session -t colossus 2>/dev/null; then
    echo "Existing colossus session found. Kill it first:"
    echo "  tmux kill-session -t colossus"
    exit 1
fi

# --- Start ---

echo "=== Colossus ==="
echo "Directory: $COLOSSUS_DIR"
echo ""

# Create tmux session
tmux new-session -d -s colossus -n controller -c "$COLOSSUS_DIR"

# Controller loop: invoke claude every 5 minutes
# Each invocation is a fresh controller cycle.
# Using 'claude -p' for non-interactive execution with tool access.
CONTROLLER_CMD="cd $COLOSSUS_DIR && while true; do
  echo \"\"
  echo \"======================================\"
  echo \"Controller cycle: \$(date)\"
  echo \"======================================\"
  claude -p 'You are the Colossus controller. Read CONTROLLER.md for your full operating instructions, then execute one control cycle. Be decisive and concise.'
  echo \"\"
  echo \"Cycle complete: \$(date). Next cycle in 5 minutes.\"
  sleep 300
done"

tmux send-keys -t colossus:controller "$CONTROLLER_CMD" Enter

echo "Colossus is running."
echo ""
echo "  Watch:  tmux attach -t colossus"
echo "  Logs:   tmux capture-pane -t colossus:controller -p"
echo "  Stop:   tmux kill-session -t colossus"
echo ""
echo "The controller will run its first cycle now."
echo "Check STATE.md and DECISIONS.md to monitor progress."
