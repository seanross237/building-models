#!/bin/bash
# Atlas Operator — drives the exploration workflow
# Pure bash, zero tokens. Launches explorers, nudges strategizer, handles plumbing.
#
# Usage: bash operator.sh <strategy-dir> <session-prefix> <missionary-session>
#
# Example: bash operator.sh /path/to/strategies/strategy-001 ns missionary-ns

set -euo pipefail

STRATEGY_DIR="${1:?Usage: operator.sh <strategy-dir> <session-prefix> <missionary-session>}"
PREFIX="${2:?Usage: operator.sh <strategy-dir> <session-prefix> <missionary-session>}"
MISSIONARY_SESSION="${3:?Usage: operator.sh <strategy-dir> <session-prefix> <missionary-session>}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
EXPLORATIONS_DIR="$STRATEGY_DIR/explorations"
STRATEGIZER_SESSION="${PREFIX}-strategizer"
LOG_FILE="$STRATEGY_DIR/operator.log"
STATE_FILE="$STRATEGY_DIR/operator-state.txt"

# Agent system prompts
EXPLORER_PROMPT="$(cd "$SCRIPT_DIR/.." && pwd)/agents/explorer/system-prompt.md"
MATH_EXPLORER_PROMPT="$(cd "$SCRIPT_DIR/.." && pwd)/agents/math-explorer/system-prompt.md"

POLL_INTERVAL=30  # seconds between checks

log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%S)] $1" | tee -a "$LOG_FILE"
}

# Send a prompt to a Claude Code tmux session, handling the 800-char paste limit.
# Claude Code silently drops prompts >= 800 chars sent via `tmux send-keys "..." Enter`
# because it treats rapid large input as a paste and absorbs the Enter.
# Workaround: send text with -l flag, sleep, then send Enter separately.
# See TMUX-SEND-KEYS-800-CHAR-LIMIT.md for full analysis.
safe_send_prompt() {
    local session="$1"
    local prompt="$2"
    tmux send-keys -t "$session" -l "$prompt"
    sleep 0.3
    tmux send-keys -t "$session" Enter
}

# Initialize state file (tracks which explorations have been launched/completed)
touch "$STATE_FILE"

# Check if an exploration has been launched
is_launched() {
    grep -q "^launched:$1$" "$STATE_FILE" 2>/dev/null
}

# Check if an exploration has been completed (result delivered to strategizer)
is_completed() {
    grep -q "^completed:$1$" "$STATE_FILE" 2>/dev/null
}

mark_launched() {
    echo "launched:$1" >> "$STATE_FILE"
}

mark_completed() {
    echo "completed:$1" >> "$STATE_FILE"
}

# Determine explorer type from GOAL.md content
# First checks for explicit <!-- explorer-type: math --> comment, then falls back to content heuristics
get_explorer_type() {
    local goal_file="$1"
    # Check for explicit type comment
    if grep -q "explorer-type: math" "$goal_file" 2>/dev/null; then
        echo "math"
    elif grep -q "explorer-type: standard" "$goal_file" 2>/dev/null; then
        echo "standard"
    # Fallback: content heuristics
    elif grep -qi "math explorer\|formal verification\|lean 4\|prove.*theorem\|machine-check\|numerical experiment\|computation\|simulate\|eigenvalue\|DNS" "$goal_file" 2>/dev/null; then
        echo "math"
    else
        echo "standard"
    fi
}

# Launch an explorer for a given exploration directory
launch_explorer() {
    local exploration_dir="$1"
    local exploration_name=$(basename "$exploration_dir")
    local session_name="${PREFIX}-${exploration_name}"
    local goal_file="$exploration_dir/GOAL.md"

    # Determine explorer type
    local explorer_type=$(get_explorer_type "$goal_file")
    local prompt_file="$EXPLORER_PROMPT"
    if [ "$explorer_type" = "math" ]; then
        prompt_file="$MATH_EXPLORER_PROMPT"
    fi

    log "Launching $explorer_type explorer: $session_name"

    # Create tmux session in the exploration directory
    tmux new-session -d -s "$session_name" -c "$exploration_dir" 2>/dev/null || {
        log "ERROR: Failed to create tmux session $session_name"
        return 1
    }

    # Start Claude
    tmux send-keys -t "$session_name" "claude --system-prompt-file $prompt_file --permission-mode bypassPermissions" Enter

    # Wait for Claude to initialize
    sleep 10

    # Send the goal (use safe_send_prompt to handle the 800-char tmux paste limit)
    safe_send_prompt "$session_name" "Read GOAL.md in your current directory and execute the task. Write your detailed findings to REPORT.md and a concise summary (under 300 words) to REPORT-SUMMARY.md in this same directory. Your current directory is: $exploration_dir"

    mark_launched "$exploration_name"
    log "Explorer $session_name launched ($explorer_type)"
}

# Nudge the strategizer that a result is ready
nudge_strategizer() {
    local exploration_name="$1"
    local summary_file="$EXPLORATIONS_DIR/$exploration_name/REPORT-SUMMARY.md"

    log "Nudging strategizer: $exploration_name complete"

    # Check strategizer session exists
    if ! tmux has-session -t "$STRATEGIZER_SESSION" 2>/dev/null; then
        log "ERROR: Strategizer session $STRATEGIZER_SESSION not found"
        return 1
    fi

    safe_send_prompt "$STRATEGIZER_SESSION" "$exploration_name is complete. Read the report summary at explorations/$exploration_name/REPORT-SUMMARY.md, process it (update HISTORY, REASONING, state.json, launch curator, write meta-learning), then write the next GOAL.md if needed."

    mark_completed "$exploration_name"
}

# Nudge the missionary that the strategy is done
nudge_missionary() {
    log "Strategy complete — nudging missionary"

    if ! tmux has-session -t "$MISSIONARY_SESSION" 2>/dev/null; then
        log "ERROR: Missionary session $MISSIONARY_SESSION not found"
        return 1
    fi

    local strategy_name=$(basename "$STRATEGY_DIR")
    safe_send_prompt "$MISSIONARY_SESSION" "$strategy_name is complete. Read the final report at strategies/$strategy_name/FINAL-REPORT.md, the report summaries at strategies/$strategy_name/HISTORY-OF-REPORT-SUMMARIES.md, the reasoning log at strategies/$strategy_name/REASONING.md, and the meta-learning notes in meta-inbox/. Evaluate both the science results and how well the methodology worked. Decide what's next."
}

# Check if strategizer session is alive
check_strategizer() {
    if ! tmux has-session -t "$STRATEGIZER_SESSION" 2>/dev/null; then
        log "WARNING: Strategizer session gone. Strategy may have completed or crashed."
        return 1
    fi
    return 0
}

log "Operator started"
log "  Strategy dir: $STRATEGY_DIR"
log "  Prefix: $PREFIX"
log "  Missionary: $MISSIONARY_SESSION"
log "  Strategizer: $STRATEGIZER_SESSION"
log "  Poll interval: ${POLL_INTERVAL}s"

# Main loop
while true; do
    # 1. Check for FINAL-REPORT.md (strategy complete)
    if [ -f "$STRATEGY_DIR/FINAL-REPORT.md" ]; then
        # Check if we already notified
        if ! grep -q "^final_report_sent$" "$STATE_FILE" 2>/dev/null; then
            nudge_missionary
            echo "final_report_sent" >> "$STATE_FILE"
            log "Strategy complete. Operator exiting."
            exit 0
        fi
    fi

    # 2. Check for new GOAL.md files (need to launch explorers)
    for goal_file in "$EXPLORATIONS_DIR"/*/GOAL.md; do
        [ -f "$goal_file" ] || continue
        exploration_dir=$(dirname "$goal_file")
        exploration_name=$(basename "$exploration_dir")

        if ! is_launched "$exploration_name"; then
            launch_explorer "$exploration_dir"
        fi
    done

    # 3. Check for new REPORT-SUMMARY.md files (explorers finished)
    for summary_file in "$EXPLORATIONS_DIR"/*/REPORT-SUMMARY.md; do
        [ -f "$summary_file" ] || continue
        exploration_dir=$(dirname "$summary_file")
        exploration_name=$(basename "$exploration_dir")

        if is_launched "$exploration_name" && ! is_completed "$exploration_name"; then
            # Kill the explorer session (it's done)
            explorer_session="${PREFIX}-${exploration_name}"
            tmux kill-session -t "$explorer_session" 2>/dev/null && \
                log "Killed explorer session: $explorer_session"

            # Nudge strategizer
            nudge_strategizer "$exploration_name"
        fi
    done

    # 4. Check strategizer health
    if ! check_strategizer; then
        # Check if strategy is done (state.json done=true)
        if python3 -c "import json;exit(0 if json.load(open('$STRATEGY_DIR/state.json'))['done'] else 1)" 2>/dev/null; then
            log "Strategy marked done in state.json. Waiting for FINAL-REPORT.md."
        else
            log "ERROR: Strategizer session lost and strategy not done. Manual intervention needed."
        fi
    fi

    sleep "$POLL_INTERVAL"
done
