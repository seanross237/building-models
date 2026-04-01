#!/bin/bash
# Test harness for the babysitter check script
# Tests pattern matching in isolation by mocking tmux capture-pane output

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
PASS=0
FAIL=0
TESTS_RUN=0

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# We test the PATTERN MATCHING logic directly, not through real tmux.
# For each test: feed mock pane content through the same grep/logic the script uses.

test_pattern() {
    local description="$1"
    local pane_content="$2"
    local expected_action="$3"  # "working|computing|rate limited|approved|idle|blank|error_loop|unknown"

    TESTS_RUN=$((TESTS_RUN + 1))

    local result="unknown"
    local PANE="$pane_content"

    # Replicate the script's pattern matching logic exactly (same order as check.sh)
    if echo "$PANE" | grep -q "Do you want to make this edit to settings.json"; then
        result="approved_settings"
    elif echo "$PANE" | grep -qE "❯ 1\. Yes" && echo "$PANE" | grep -qE "(settings\.json|REPORT|GOAL|STRATEGY|state\.json|REASONING|HISTORY)"; then
        result="approved_permission"
    elif echo "$PANE" | grep -q "You've hit your limit"; then
        result="rate_limited"
    elif echo "$PANE" | grep -qE "(Cooked|Crunched|Worked|Brewed) for"; then
        if echo "$PANE" | grep -qiE "(strategy is complete|mission.complete|FINAL-REPORT|State set to done|Nothing more to do)"; then
            result="idle_mission_complete"
        else
            result="idle_completed"
        fi
    elif echo "$PANE" | grep -qiE "(strategy is complete|mission.complete|FINAL-REPORT written|State set to done|Nothing more to do)"; then
        result="idle_mission_complete"
    elif echo "$PANE" | grep -qE "(✳|✶|✽|✢|✻|·|Thinking|Running|Initializing)"; then
        if echo "$PANE" | grep -q "Running…"; then
            result="computing"
        else
            result="working"
        fi
    else
        LINE_COUNT=$(echo "$PANE" | grep -cve '^\s*$' || true)
        if [ "$LINE_COUNT" -lt 3 ]; then
            result="blank"
        else
            ERROR_LINES=$(echo "$PANE" | grep -c "Error\|error\|ERROR\|failed\|Failed" || true)
            if [ "$ERROR_LINES" -ge 3 ]; then
                result="error_loop"
            else
                result="unknown"
            fi
        fi
    fi

    if [ "$result" = "$expected_action" ]; then
        echo -e "  ${GREEN}PASS${NC}: $description (got: $result)"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}FAIL${NC}: $description (expected: $expected_action, got: $result)"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== Pattern Matching Tests ==="
echo ""

# ---- Active working ----
echo "Category: Active working"

test_pattern "Explorer with spinner and tokens" \
"✳ Thinking… (5m 30s · ↓ 10.5k tokens · thinking with high effort)

────────────────────────────────────────────────────────────────────────────
❯
────────────────────────────────────────────────────────────────────────────
  ██░░░░░░░░░░░░░░░░░░ 12%
  ⏵⏵ bypass permissions on (shift+tab to cycle)" \
"working"

test_pattern "Explorer with different spinner (✶)" \
"✶ Warping… (2m 12s · ↓ 4.1k tokens · thinking with high effort)

────────────────────────────────────────────────────────────────────────────
❯" \
"working"

test_pattern "Explorer with dot spinner (·)" \
"· Envisioning… (5m 59s · ↓ 11.0k tokens · thinking with high effort)

────────────────────────────────────────────────────────────────────────────
❯" \
"working"

test_pattern "Explorer with Initializing" \
"   └─Survey alternative closures · 0 tool uses · 17.1k tokens
      ⎿  Initializing…

❯" \
"working"

# ---- Computing ----
echo ""
echo "Category: Computing"

test_pattern "Foreground computation with timeout" \
"⏺ Bash(python3 spectral_solver.py 2>&1)
  ⎿  Running… (7m 30s · timeout 10m)
     (ctrl+b ctrl+b (twice) to run in background)

✻ Burrowing… (45m · ↓ 18.0k tokens)

❯" \
"computing"

test_pattern "Background computation poll (sleep && cat)" \
"  Bash(sleep 300 && cat results.json)
  ⎿  Running… (3m 36s · timeout 7m)

✢ Ideating… (2h 5m · ↓ 22.5k tokens)

❯" \
"computing"

# ---- Rate limited ----
echo ""
echo "Category: Rate limited"

test_pattern "Standard rate limit message" \
"     … +293 lines (ctrl+o to expand)
  ⎿  You've hit your limit · resets 9:45pm (Asia/Katmandu)
     /extra-usage to finish what you're working on.

✻ Brewed for 3m 5s

────────────────────────────────────────────────────────────────────────────
❯
────────────────────────────────────────────────────────────────────────────
  █░░░░░░░░░░░░░░░░░░░ 6%
  ⏵⏵ bypass permissions on (shift+tab to cycle)" \
"rate_limited"

test_pattern "Rate limit without reset time" \
"  ⎿  You've hit your limit
     /extra-usage to finish what you're working on.

❯" \
"rate_limited"

# ---- Permission prompts ----
echo ""
echo "Category: Permission prompts"

test_pattern "Settings.json edit prompt" \
' Do you want to make this edit to settings.json?
 ❯ 1. Yes
   2. Yes, and allow Claude to edit its own settings for this session
   3. No

 Esc to cancel · Tab to amend' \
"approved_settings"

test_pattern "Generic prompt for REPORT.md" \
' Do you want to allow this file write?
 File: REPORT.md
 ❯ 1. Yes
   2. No

 Esc to cancel' \
"approved_permission"

test_pattern "Generic prompt for STRATEGY.md" \
' Do you want to allow this file write?
 STRATEGY.md
 ❯ 1. Yes
   2. No' \
"approved_permission"

test_pattern "Generic prompt for unknown file (should NOT approve)" \
' Do you want to allow this action?
 rm -rf /important/stuff
 ❯ 1. Yes
   2. No' \
"unknown"

# ---- Idle states ----
echo ""
echo "Category: Idle states"

test_pattern "Completed work (Cooked) — strategy complete text triggers mission_complete" \
"  The strategy is complete.

✻ Cooked for 3m 23s

────────────────────────────────────────────────────────────────────────────
❯
────────────────────────────────────────────────────────────────────────────
  █████████░░░░░░░░░░░ 45%" \
"idle_mission_complete"

test_pattern "Completed work (Crunched)" \
"  Done processing results.

✻ Crunched for 5m 14s

────────────────────────────────────────────────────────────────────────────
❯
────────────────────────────────────────────────────────────────────────────
  ██░░░░░░░░░░░░░░░░░░░░ 4%" \
"idle_completed"

test_pattern "Completed work (Worked)" \
"  All tasks finished.

✻ Worked for 1m 6s

────────────────────────────────────────────────────────────────────────────
❯" \
"idle_completed"

test_pattern "Mission complete" \
"  MISSION-COMPLETE.md written. 5 novel claims.

✻ Cooked for 15m 39s

────────────────────────────────────────────────────────────────────────────
❯
────────────────────────────────────────────────────────────────────────────
  █░░░░░░░░░░░░░░░░░░░ 7%" \
"idle_mission_complete"

test_pattern "Strategy complete (no work marker)" \
"  Nothing more to do — the missionary will evaluate the results.

────────────────────────────────────────────────────────────────────────────
❯
────────────────────────────────────────────────────────────────────────────
  █████████░░░░░░░░░░░ 45%" \
"idle_mission_complete"

# ---- Blank/starting ----
echo ""
echo "Category: Blank/starting"

test_pattern "Empty pane" \
"
" \
"blank"

test_pattern "Nearly empty pane" \
"
❯" \
"blank"

# ---- Error loops ----
echo ""
echo "Category: Error loops"

test_pattern "Module install error loop" \
"⏺ Bash(python3 solver.py)
  ⎿  Error: ModuleNotFoundError: No module named 'dedalus'
⏺ Bash(pip install dedalus && python3 solver.py)
  ⎿  Error: Failed to build dedalus
⏺ Bash(pip install --user dedalus)
  ⎿  Error: Failed to build dedalus
⏺ Bash(pip install dedalus==2.0)
  ⎿  Error: No matching distribution

────────────────────────────────────────────────────────────────────────────
❯
────────────────────────────────────────────────────────────────────────────
  ██░░░░░░░░░░░░░░░░░░ 8%" \
"error_loop"

test_pattern "Single error (not a loop)" \
"⏺ Bash(python3 solver.py)
  ⎿  Error: FileNotFoundError: solver.py

⏺ Let me create the file first.

────────────────────────────────────────────────────────────────────────────
❯
────────────────────────────────────────────────────────────────────────────
  ██░░░░░░░░░░░░░░░░░░ 5%" \
"unknown"

# ---- Unknown states ----
echo ""
echo "Category: Unknown states"

test_pattern "Unrecognized output (no spinners, not blank, not error)" \
"This is some random output that the babysitter
has never seen before. It doesn't match any known
patterns. There are enough lines here to not be
blank but no spinners or errors visible.

Some more text about something unexpected." \
"unknown"

# ============================================================
# Integration test: run check.sh against real sessions
# ============================================================
echo ""
echo "=== Integration Test (real sessions) ==="

# Clear log
TEST_LOG="$LOG_DIR/test_integration.log"
> "$TEST_LOG"

# Temporarily override LOG_FILE in the script
REAL_SESSIONS=$(tmux list-sessions -F '#{session_name}' 2>/dev/null | grep -E '(explorer|strategizer|missionary)' | wc -l | tr -d ' ')
echo "  Found $REAL_SESSIONS active sessions"

if [ "$REAL_SESSIONS" -gt 0 ]; then
    # Run the real script
    LOG_FILE_BAK="$LOG_FILE"
    bash "$SCRIPT_DIR/check.sh"

    # Check log file was written to
    TESTS_RUN=$((TESTS_RUN + 1))
    LOG_LINES=$(wc -l < "$LOG_DIR/$(date +%Y%m%d).log" 2>/dev/null || echo 0)
    if [ "$LOG_LINES" -gt 0 ]; then
        echo -e "  ${GREEN}PASS${NC}: Script ran and produced log output ($LOG_LINES lines)"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}FAIL${NC}: Script ran but produced no log output"
        FAIL=$((FAIL + 1))
    fi

    # Check no Claude was spawned (all current sessions should be in known states)
    TESTS_RUN=$((TESTS_RUN + 1))
    if ! grep -q "Spawning Claude" "$LOG_DIR/$(date +%Y%m%d).log"; then
        echo -e "  ${GREEN}PASS${NC}: No Claude spawned for current sessions (all known patterns)"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}FAIL${NC}: Claude was spawned — check if there's a new unknown pattern"
        FAIL=$((FAIL + 1))
    fi
else
    echo "  Skipping integration test (no active sessions)"
fi

# ============================================================
# SUMMARY
# ============================================================
echo ""
echo "============================================"
echo "Results: $PASS passed, $FAIL failed out of $TESTS_RUN tests"
echo "============================================"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
