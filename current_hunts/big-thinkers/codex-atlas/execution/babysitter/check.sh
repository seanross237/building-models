#!/bin/bash
# Atlas Babysitter — zero-token health check
# Handles known patterns with bash. Only calls Claude for unknowns.
# Claude can update this script's KNOWN_PATTERNS to learn new scenarios.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%S)
LOG_FILE="$LOG_DIR/$(date +%Y%m%d).log"

mkdir -p "$LOG_DIR"

# Get all atlas-related tmux sessions
SESSIONS=$(tmux list-sessions -F '#{session_name}' 2>/dev/null | grep -E '(explorer|strategizer|missionary)' || true)

if [ -z "$SESSIONS" ]; then
    echo "[$TIMESTAMP] No active sessions" >> "$LOG_FILE"
    exit 0
fi

NEEDS_CLAUDE=false
CLAUDE_CONTEXT=""
ACTIONS_TAKEN=""

for SESSION in $SESSIONS; do
    PANE=$(tmux capture-pane -t "$SESSION" -p 2>/dev/null | tail -20)

    if [ -z "$PANE" ]; then
        continue
    fi

    # ============================================================
    # KNOWN_PATTERNS — bash handles these directly, zero tokens
    # Claude can add new patterns here when it encounters unknowns
    # Pattern order matters! More specific patterns go first.
    # ============================================================

    # Pattern: Permission prompt (settings.json edit)
    if echo "$PANE" | grep -q "Do you want to make this edit to settings.json"; then
        tmux send-keys -t "$SESSION" Down Enter 2>/dev/null
        ACTIONS_TAKEN="${ACTIONS_TAKEN}[$TIMESTAMP] $SESSION: approved settings.json edit\n"
        continue
    fi

    # Pattern: Generic permission prompt (Yes/No)
    if echo "$PANE" | grep -qE "❯ 1\. Yes"; then
        # Only auto-approve if it's a settings edit or file write in the exploration dir
        if echo "$PANE" | grep -qE "(settings\.json|REPORT|GOAL|STRATEGY|state\.json|REASONING|HISTORY)"; then
            tmux send-keys -t "$SESSION" "1" Enter 2>/dev/null
            ACTIONS_TAKEN="${ACTIONS_TAKEN}[$TIMESTAMP] $SESSION: approved permission prompt\n"
            continue
        fi
    fi

    # Pattern: Rate limited
    if echo "$PANE" | grep -q "You've hit your limit"; then
        RESET_TIME=$(echo "$PANE" | grep -oE "resets [0-9:]+[ap]m" | head -1)
        ACTIONS_TAKEN="${ACTIONS_TAKEN}[$TIMESTAMP] $SESSION: rate limited ($RESET_TIME)\n"
        # Try nudging — harmless if still limited
        tmux send-keys -t "$SESSION" "continue" Enter 2>/dev/null
        ACTIONS_TAKEN="${ACTIONS_TAKEN}[$TIMESTAMP] $SESSION: nudged after rate limit\n"
        continue
    fi

    # Pattern: Completed work — "Cooked/Crunched/Worked/Brewed for" means the
    # agent finished its last response. Check this BEFORE the spinner check,
    # because the completion line itself contains a spinner character (✻).
    if echo "$PANE" | grep -qE "(Cooked|Crunched|Worked|Brewed) for"; then
        # Check if mission/strategy is complete
        if echo "$PANE" | grep -qiE "(strategy is complete|mission.complete|FINAL-REPORT|State set to done|Nothing more to do)"; then
            ACTIONS_TAKEN="${ACTIONS_TAKEN}[$TIMESTAMP] $SESSION: idle (strategy/mission complete)\n"
        else
            ACTIONS_TAKEN="${ACTIONS_TAKEN}[$TIMESTAMP] $SESSION: idle (completed work)\n"
        fi
        continue
    fi

    # Pattern: Mission/strategy complete without a work marker
    if echo "$PANE" | grep -qiE "(strategy is complete|mission.complete|FINAL-REPORT written|State set to done|Nothing more to do)"; then
        ACTIONS_TAKEN="${ACTIONS_TAKEN}[$TIMESTAMP] $SESSION: idle (strategy/mission complete)\n"
        continue
    fi

    # Pattern: Actively working (spinner visible or computation running)
    if echo "$PANE" | grep -qE "(✳|✶|✽|✢|✻|·|Thinking|Running|Initializing)"; then
        if echo "$PANE" | grep -q "Running…"; then
            TIMEOUT_INFO=$(echo "$PANE" | grep -oE "Running… \([^)]+\)" | tail -1)
            ACTIONS_TAKEN="${ACTIONS_TAKEN}[$TIMESTAMP] $SESSION: computing ($TIMEOUT_INFO)\n"
        else
            PROGRESS=$(echo "$PANE" | grep -oE "[0-9]+%" | tail -1)
            TOKENS=$(echo "$PANE" | grep -oE "[0-9.]+k tokens" | tail -1)
            ACTIONS_TAKEN="${ACTIONS_TAKEN}[$TIMESTAMP] $SESSION: working ($PROGRESS, $TOKENS)\n"
        fi
        continue
    fi

    # Pattern: Session exists but pane is blank/minimal (< 3 non-empty lines)
    LINE_COUNT=$(echo "$PANE" | grep -cve '^\s*$' || true)
    if [ "$LINE_COUNT" -lt 3 ]; then
        ACTIONS_TAKEN="${ACTIONS_TAKEN}[$TIMESTAMP] $SESSION: blank/starting\n"
        continue
    fi

    # Pattern: Error loop (3+ lines containing error/failed)
    ERROR_LINES=$(echo "$PANE" | grep -c "Error\|error\|ERROR\|failed\|Failed" || true)
    if [ "$ERROR_LINES" -ge 3 ]; then
        NEEDS_CLAUDE=true
        CLAUDE_CONTEXT="${CLAUDE_CONTEXT}\n=== $SESSION (ERROR LOOP DETECTED) ===\n$PANE\n"
        continue
    fi

    # ============================================================
    # UNKNOWN — nothing matched. Queue for Claude.
    # ============================================================
    NEEDS_CLAUDE=true
    CLAUDE_CONTEXT="${CLAUDE_CONTEXT}\n=== $SESSION (UNKNOWN STATE) ===\n$PANE\n"

done

# Log actions
if [ -n "$ACTIONS_TAKEN" ]; then
    echo -e "$ACTIONS_TAKEN" >> "$LOG_FILE"
fi

# Only call Claude if something unknown was found
if [ "$NEEDS_CLAUDE" = true ]; then
    echo "[$TIMESTAMP] Spawning Claude for unknown scenario" >> "$LOG_FILE"

    PROMPT="You are the Atlas babysitter. The following tmux sessions have states that the automated check script couldn't handle. Diagnose each one and take action if needed (approve prompts, nudge stuck agents, etc.).

IMPORTANT: If you identify a new pattern that should be handled automatically in the future, update the bash script at $SCRIPT_DIR/check.sh — add a new pattern in the KNOWN_PATTERNS section following the existing format. This teaches the babysitter to handle it without tokens next time.

$(echo -e "$CLAUDE_CONTEXT")

After taking action, write a brief summary of what you did and any patterns you added."

    # Spawn a fresh, short-lived Claude — minimal context, no history
    cd "$SCRIPT_DIR"
    claude -p --permission-mode bypassPermissions --no-session-persistence "$PROMPT" >> "$LOG_FILE" 2>&1

    echo "[$TIMESTAMP] Claude session complete" >> "$LOG_FILE"
fi
