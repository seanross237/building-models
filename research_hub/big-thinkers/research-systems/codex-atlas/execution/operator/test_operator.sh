#!/bin/bash
# Test harness for the operator script
# Creates a fake strategy directory structure and verifies the operator
# detects goals, launches sessions, detects completions, and nudges correctly.
#
# NOTE: This test creates real tmux sessions but uses 'echo' instead of Claude
# to avoid token costs. It tests the operator's detection and orchestration logic.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TEST_DIR="/tmp/atlas-operator-test-$$"
STRATEGY_DIR="$TEST_DIR/strategies/strategy-001"
EXPLORATIONS_DIR="$STRATEGY_DIR/explorations"
PREFIX="test-op"
MISSIONARY_SESSION="test-op-missionary"
STRATEGIZER_SESSION="test-op-strategizer"

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'
PASS=0
FAIL=0
TESTS=0

assert() {
    local description="$1"
    local condition="$2"
    TESTS=$((TESTS + 1))
    if eval "$condition"; then
        echo -e "  ${GREEN}PASS${NC}: $description"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}FAIL${NC}: $description"
        FAIL=$((FAIL + 1))
    fi
}

cleanup() {
    tmux kill-session -t "$MISSIONARY_SESSION" 2>/dev/null || true
    tmux kill-session -t "$STRATEGIZER_SESSION" 2>/dev/null || true
    tmux kill-session -t "test-op-exploration-001" 2>/dev/null || true
    tmux kill-session -t "test-op-exploration-002" 2>/dev/null || true
    tmux kill-session -t "test-op-operator" 2>/dev/null || true
    rm -rf "$TEST_DIR"
}

trap cleanup EXIT

# ============================================================
# Setup
# ============================================================
echo "=== Setting up test environment ==="

mkdir -p "$EXPLORATIONS_DIR"

# Create state.json
cat > "$STRATEGY_DIR/state.json" << 'EOF'
{"iteration": 0, "done": false, "current_exploration": "", "directions_tried": [], "explorations_completed": []}
EOF

# Create fake missionary and strategizer sessions
tmux new-session -d -s "$MISSIONARY_SESSION" -x 120 -y 40
tmux new-session -d -s "$STRATEGIZER_SESSION" -x 120 -y 40

# Patch the operator to not actually launch Claude (use echo instead)
# We create a modified version that skips the Claude launch
PATCHED_OPERATOR="$TEST_DIR/operator-test.sh"
sed 's|tmux send-keys -t "$session_name" "claude --system-prompt-file.*|tmux send-keys -t "$session_name" "echo EXPLORER_STARTED" Enter|' \
    "$SCRIPT_DIR/operator.sh" | \
sed 's|sleep 10|sleep 1|' | \
sed 's|tmux send-keys -t "$session_name" "Read GOAL.md.*|tmux send-keys -t "$session_name" "echo GOAL_RECEIVED" Enter|' | \
sed 's|POLL_INTERVAL=30|POLL_INTERVAL=2|' \
    > "$PATCHED_OPERATOR"
chmod +x "$PATCHED_OPERATOR"

echo ""

# ============================================================
# Test 1: Operator detects new GOAL.md and launches explorer
# ============================================================
echo "=== Test 1: Detect GOAL.md and launch explorer ==="

# Start operator in background
tmux new-session -d -s "test-op-operator" "bash $PATCHED_OPERATOR $STRATEGY_DIR $PREFIX $MISSIONARY_SESSION 2>&1"

# Create an exploration with a GOAL.md
mkdir -p "$EXPLORATIONS_DIR/exploration-001"
cat > "$EXPLORATIONS_DIR/exploration-001/GOAL.md" << 'EOF'
# Test Goal
Do some science.
EOF

# Wait for operator to detect and launch
sleep 5

assert "Explorer tmux session created" \
    "tmux has-session -t test-op-exploration-001 2>/dev/null"

assert "Exploration marked as launched in state file" \
    "grep -q 'launched:exploration-001' '$STRATEGY_DIR/operator-state.txt'"

assert "Launch logged" \
    "grep -q 'Launching.*exploration-001' '$STRATEGY_DIR/operator.log'"

echo ""

# ============================================================
# Test 2: Operator detects REPORT-SUMMARY.md and nudges strategizer
# ============================================================
echo "=== Test 2: Detect REPORT-SUMMARY and nudge strategizer ==="

# Simulate explorer completing
cat > "$EXPLORATIONS_DIR/exploration-001/REPORT-SUMMARY.md" << 'EOF'
# Summary
Found something interesting.
EOF

# Wait for operator to detect
sleep 5

assert "Exploration marked as completed" \
    "grep -q 'completed:exploration-001' '$STRATEGY_DIR/operator-state.txt'"

assert "Explorer session killed" \
    "! tmux has-session -t test-op-exploration-001 2>/dev/null"

assert "Strategizer nudged (message sent)" \
    "grep -q 'Nudging strategizer.*exploration-001' '$STRATEGY_DIR/operator.log'"

echo ""

# ============================================================
# Test 3: Operator handles parallel explorations
# ============================================================
echo "=== Test 3: Parallel explorations ==="

mkdir -p "$EXPLORATIONS_DIR/exploration-002"
cat > "$EXPLORATIONS_DIR/exploration-002/GOAL.md" << 'EOF'
# Test Goal 2
Do different science. Use math explorer and Lean 4 formal verification.
EOF

sleep 5

assert "Second explorer launched" \
    "tmux has-session -t test-op-exploration-002 2>/dev/null"

assert "Second exploration marked launched" \
    "grep -q 'launched:exploration-002' '$STRATEGY_DIR/operator-state.txt'"

# It should detect "math explorer" / "Lean 4" / "formal verification" in the goal
assert "Math explorer type detected in log" \
    "grep -q 'math.*exploration-002\|exploration-002.*math' '$STRATEGY_DIR/operator.log'"

echo ""

# ============================================================
# Test 4: Operator doesn't re-launch already launched explorations
# ============================================================
echo "=== Test 4: No re-launch of existing explorations ==="

LAUNCH_COUNT_BEFORE=$(grep -c "Launching.*exploration-001" "$STRATEGY_DIR/operator.log")
sleep 5
LAUNCH_COUNT_AFTER=$(grep -c "Launching.*exploration-001" "$STRATEGY_DIR/operator.log")

assert "Exploration-001 not re-launched" \
    "[ $LAUNCH_COUNT_BEFORE -eq $LAUNCH_COUNT_AFTER ]"

echo ""

# ============================================================
# Test 5: Operator detects FINAL-REPORT.md and nudges missionary
# ============================================================
echo "=== Test 5: Detect FINAL-REPORT and nudge missionary ==="

# Complete exploration-002 first
cat > "$EXPLORATIONS_DIR/exploration-002/REPORT-SUMMARY.md" << 'EOF'
Done.
EOF
sleep 3

# Create FINAL-REPORT.md
cat > "$STRATEGY_DIR/FINAL-REPORT.md" << 'EOF'
# Final Report
Strategy complete.
EOF

sleep 5

assert "Missionary nudged" \
    "grep -q 'nudging missionary' '$STRATEGY_DIR/operator.log'"

assert "Final report sent marked in state" \
    "grep -q 'final_report_sent' '$STRATEGY_DIR/operator-state.txt'"

# Operator should have exited
sleep 3
assert "Operator exited after strategy complete" \
    "! tmux has-session -t test-op-operator 2>/dev/null"

echo ""

# ============================================================
# Summary
# ============================================================
echo "============================================"
echo "Results: $PASS passed, $FAIL failed out of $TESTS tests"
echo "============================================"

if [ "$FAIL" -gt 0 ]; then
    echo ""
    echo "Operator log:"
    cat "$STRATEGY_DIR/operator.log"
    echo ""
    echo "State file:"
    cat "$STRATEGY_DIR/operator-state.txt"
    exit 1
fi
