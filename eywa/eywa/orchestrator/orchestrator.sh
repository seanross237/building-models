#!/usr/bin/env bash
set -euo pipefail

# Eywa Orchestrator — recursive task-tree state machine
# Polls every 10s, manages node lifecycles, spawns agents via tmux.

EYWA_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENTS_DIR="$EYWA_ROOT/agent-prompts-and-guides"
POLL_INTERVAL=10
MAX_DEPTH=5
PLAN_THRESHOLD=30    # adjusted C × I must exceed this to plan
ZOMBIE_TIMEOUT=180   # 3 min no file activity
CLAUDE_INIT_WAIT=12  # seconds before sending task prompt
COMP_TIMEOUT=1800    # 30 min for long computations

usage() {
    echo "Usage: bash orchestrator.sh <mission_directory>"
    echo "  e.g. bash orchestrator.sh missions/sf-date-005"
    exit 1
}

[[ $# -lt 1 ]] && usage
MISSION_DIR="$(cd "$1" && pwd)"
MISSION_ID="$(basename "$MISSION_DIR")"
LOG_FILE="$MISSION_DIR/orchestrator.jsonl"
TREE_ROOT="$MISSION_DIR/tree/root"
[[ ! -d "$MISSION_DIR" ]] && echo "Error: $MISSION_DIR not found" >&2 && exit 1

# Initialize root node from mission-goal.md if tree doesn't exist yet
if [[ ! -d "$TREE_ROOT" ]]; then
    [[ ! -f "$MISSION_DIR/mission-goal.md" ]] && echo "Error: $MISSION_DIR/mission-goal.md not found" >&2 && exit 1
    mkdir -p "$TREE_ROOT/input" "$TREE_ROOT/output" "$TREE_ROOT/for-orchestrator"
    cp "$MISSION_DIR/mission-goal.md" "$TREE_ROOT/input/goal.md"
    echo "planner" > "$TREE_ROOT/for-orchestrator/agent-mode"
    echo "pending" > "$TREE_ROOT/for-orchestrator/this-nodes-current-status"
    echo "  [init] Created tree/root from mission-goal.md (mode=planner)"
fi

echo "Eywa orchestrator: $MISSION_ID"
echo "  dir=$MISSION_DIR  log=$LOG_FILE  poll=${POLL_INTERVAL}s"

# ---- Core helpers ----------------------------------------------------------

log_event() {
    local node="$1" evt="$2" from="${3:-}" to="${4:-}" detail="${5:-}"
    printf '{"ts":"%s","node":"%s","event":"%s","from":"%s","to":"%s","details":"%s"}\n' \
        "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "${node#"$MISSION_DIR"/}" "$evt" "$from" "$to" "$detail" \
        >> "$LOG_FILE"
}

read_status() {
    local sf="$1/for-orchestrator/this-nodes-current-status"
    [[ -f "$sf" ]] && cat "$sf" || echo ""
}

# Compare-and-swap status using mkdir as atomic lock (works on macOS + Linux).
write_status() {
    local node="$1" expected="$2" new="$3"
    local sf="$node/for-orchestrator/this-nodes-current-status"
    local lockdir="$node/for-orchestrator/.status.lock"
    # Acquire lock (mkdir is atomic)
    local tries=0
    while ! mkdir "$lockdir" 2>/dev/null; do
        ((tries++))
        (( tries > 50 )) && { rm -rf "$lockdir"; mkdir "$lockdir" 2>/dev/null || true; break; }
        sleep 0.1
    done
    # CAS check
    local cur=""; [[ -f "$sf" ]] && cur="$(cat "$sf")"
    if [[ "$cur" != "$expected" ]]; then
        rm -rf "$lockdir"
        return 1
    fi
    echo "$new" > "$sf"
    rm -rf "$lockdir"
    log_event "$node" "status_change" "$expected" "$new"
    return 0
}

get_depth() {
    local rel="${1#"$2"}" count=0
    while [[ "$rel" == *"/children/"* ]]; do rel="${rel#*/children/}"; ((count++)); done
    echo "$count"
}

sanitize_session_name() {
    echo "eywa-${MISSION_ID}-$(echo "${1#"$MISSION_DIR"/}" | tr '/' '-' | tr -cd 'a-zA-Z0-9_-')-$2"
}

kill_agent() { tmux kill-session -t "$1" 2>/dev/null || true; }

# ---- Instructions generation -----------------------------------------------

write_instructions() {
    local node="$1" mode="$2"
    mkdir -p "$node/input"
    local f="$node/input/instructions-${mode}.md"
    local hdr="# Eywa Instructions: ${mode}

Node: $node
"
    case "$mode" in
        executor)
            local depth; depth="$(get_depth "$node" "$TREE_ROOT")"
            local goal_content=""
            if [[ -f "$node/input/parent-instructions-and-relevant-information.md" ]]; then goal_content="$(cat "$node/input/parent-instructions-and-relevant-information.md")"
            elif [[ -f "$node/input/goal.md" ]]; then goal_content="$(cat "$node/input/goal.md")"; fi
            local knowledge_content=""; [[ -f "$node/input/retrieved_relevant_knowledge_from_library.md" ]] && knowledge_content="$(cat "$node/input/retrieved_relevant_knowledge_from_library.md")"
            cat > "$f" <<INSTRUCTIONS
# Eywa Executor Instructions

You are an executor at depth ${depth} of ${MAX_DEPTH} in a recursive task tree.
Your job is to execute this task directly and produce results. Do not decompose into subtasks — just do the work.

## Your Goal

${goal_content}

## Knowledge From Library

${knowledge_content}

## What To Do

Execute this task. Write your findings to output/final-output.md incrementally (not all at the end).
Make output/final-output.md self-contained — your parent reads it without seeing anything else.

## If This Task Is Impossible

If you determine this task is fundamentally impossible or based on wrong premises (not just hard), write output/escalation.md explaining what you attempted, what you learned, and why you can't continue.
INSTRUCTIONS
            ;;
        planner)
            local depth; depth="$(get_depth "$node" "$TREE_ROOT")"
            local goal_content=""
            if [[ -f "$node/input/parent-instructions-and-relevant-information.md" ]]; then goal_content="$(cat "$node/input/parent-instructions-and-relevant-information.md")"
            elif [[ -f "$node/input/goal.md" ]]; then goal_content="$(cat "$node/input/goal.md")"; fi
            local knowledge_content=""; [[ -f "$node/input/retrieved_relevant_knowledge_from_library.md" ]] && knowledge_content="$(cat "$node/input/retrieved_relevant_knowledge_from_library.md")"
            local plan_design_content=""; [[ -f "$AGENTS_DIR/architect/plan-design.md" ]] && plan_design_content="$(cat "$AGENTS_DIR/architect/plan-design.md")"
            local state_section=""
            [[ -f "$node/output/state.md" ]] && state_section="## Prior State (You Are Re-spawned)

$(cat "$node/output/state.md")

---
"
            cat > "$f" <<INSTRUCTIONS
# Eywa Planner Instructions

You are a planner at depth ${depth} of ${MAX_DEPTH} in a recursive task tree.
Your job is to decompose this task into a plan with scored steps.

${state_section}## Your Goal

${goal_content}

## Knowledge From Library

${knowledge_content}

## What To Do

Design a plan to accomplish your goal. Write output/plan.md following the strict format in the Plan Design Guidance below.
Score each step with Complexity (1-10) and Importance (1-10). The orchestrator adjusts both by child depth (subtracts depth, min 1) then checks if adjusted C × I > 30 to decide planner vs executor. Deeper nodes need higher scores to justify planning.

Then write output/state.md (brain dump: what you decided, alternatives considered, uncertainties).

## If This Task Is Impossible

If you determine this task is fundamentally impossible or based on wrong premises, write output/escalation.md explaining what you attempted, what you learned, and why you can't continue.

---

## Plan Design Guidance

${plan_design_content}
INSTRUCTIONS
            ;;
        retrieval) cat > "$f" <<INSTRUCTIONS
${hdr}Read input/goal.md or input/parent-instructions-and-relevant-information.md (whichever exists). Navigate the library at $EYWA_ROOT/library/ using hierarchical
indexes. Write relevant knowledge to input/retrieved_relevant_knowledge_from_library.md. If nothing relevant, write
input/retrieved_relevant_knowledge_from_library.md noting that.
INSTRUCTIONS
            ;;
        reviewer) cat > "$f" <<INSTRUCTIONS
${hdr}You are a plan reviewer. Your system prompt has your full role description.
Read input/goal.md or input/parent-instructions-and-relevant-information.md (whichever exists), output/plan.md, input/retrieved_relevant_knowledge_from_library.md. Write assessment to output/review.md.
INSTRUCTIONS
            ;;
        decider) cat > "$f" <<INSTRUCTIONS
${hdr}You are a plan decider. Your system prompt has your full role description.
Read input/goal.md or input/parent-instructions-and-relevant-information.md (whichever exists), output/plan.md, output/review.md, input/retrieved_relevant_knowledge_from_library.md.
Either revise output/plan.md (set Status: approved) or write output/escalation.md.
INSTRUCTIONS
            ;;
        evaluation) cat > "$f" <<INSTRUCTIONS
${hdr}You are re-spawned to evaluate a child result.
Read output/state.md, output/plan.md, then check children/ for the latest completed child.
Read that child's output/final-output.md or output/escalation.md.

Decide: continue, replan, or escalate.

If you decide "continue" and the next step in the plan depends on completed steps, write
output/context-for-next-step.md FIRST with a concise summary of relevant findings the next step will need.
Only include what's relevant — don't dump raw outputs. If the next step is independent, skip this file.

Update output/state.md with your reasoning.

LAST (after all other files are written), write ONLY ONE of these words to for-orchestrator/eval-decision:
- "continue" — the plan is on track, proceed to next step
- "replan" — goal still achievable but approach needs to change (also update output/plan.md first, set Status: draft)
- "escalate" — cannot produce what parent expects (also write output/escalation.md first)

eval-decision is the trigger the orchestrator acts on — write it LAST so all other files are ready.

Do NOT create child directories or write goal files for next steps. The orchestrator handles child creation.
INSTRUCTIONS
            ;;
        synthesis) cat > "$f" <<INSTRUCTIONS
${hdr}You are re-spawned to synthesize all child results.
Read output/state.md, input/goal.md or input/parent-instructions-and-relevant-information.md (whichever exists), output/plan.md, then output/final-output.md from every child in children/.
Write output/final-output.md and "synthesize" to for-orchestrator/eval-decision. Update output/state.md.
INSTRUCTIONS
            ;;
    esac
}

# ---- Spawn / zombie -------------------------------------------------------

spawn_agent() {
    local node="$1" mode="$2"
    local session
    session="$(sanitize_session_name "$node" "$mode")"
    kill_agent "$session"

    local prompt_file=""
    case "$mode" in
        executor)  prompt_file="$AGENTS_DIR/architect/system-prompt.md" ;;
        planner)   prompt_file="$AGENTS_DIR/architect/system-prompt.md" ;;
        retrieval) prompt_file="$AGENTS_DIR/library-retriever/system-prompt.md" ;;
        reviewer)  prompt_file="$AGENTS_DIR/plan-reviewer/system-prompt.md" ;;
        decider)   prompt_file="$AGENTS_DIR/plan-decider/system-prompt.md" ;;
    esac

    write_instructions "$node" "$mode"

    local task_prompt
    case "$mode" in
        executor)    task_prompt="Read input/instructions-executor.md and execute the task." ;;
        planner)     task_prompt="Read input/instructions-planner.md and design a plan." ;;
        retrieval)   task_prompt="Read input/instructions-retrieval.md and retrieve relevant knowledge." ;;
        reviewer)    task_prompt="Read input/instructions-reviewer.md and review the plan." ;;
        decider)     task_prompt="Read input/instructions-decider.md and decide on the final plan." ;;
        evaluation)  task_prompt="Read input/instructions-evaluation.md and evaluate the child result." ;;
        synthesis)   task_prompt="Read input/instructions-synthesis.md and synthesize all child results." ;;
    esac

    tmux new-session -d -s "$session" -c "$node"

    # Model assignment per agent type
    local model_flag=""
    case "$mode" in
        executor)                model_flag="--model claude-haiku-4-5-20251001" ;;
        planner|retrieval)       model_flag="--model claude-sonnet-4-6" ;;
        # evaluation, synthesis, reviewer, decider use default (Opus)
    esac

    local cmd="claude --allowedTools 'Read,Write,Edit,Bash,Glob,Grep' --permission-mode bypassPermissions"
    [[ -n "$model_flag" ]] && cmd="$cmd $model_flag"
    [[ -n "$prompt_file" && -f "$prompt_file" ]] && cmd="$cmd --system-prompt-file '$prompt_file'"

    tmux send-keys -t "$session" "$cmd" Enter
    sleep "$CLAUDE_INIT_WAIT"
    tmux send-keys -t "$session" -l "$task_prompt"
    sleep 0.3
    tmux send-keys -t "$session" Enter

    # Reset zombie state and set fresh spawn timestamp
    rm -f "$node/for-orchestrator/.zombie_state" "$node/for-orchestrator"/.spawn_ts_*
    touch "$node/for-orchestrator/.spawn_ts_${mode}"
    log_event "$node" "spawn" "" "" "mode=$mode session=$session"
    echo "  [spawn] $session ($mode)"
}

check_zombie() {
    local node="$1" session="$2"
    local zf="$node/for-orchestrator/.zombie_state" strike=0
    [[ -f "$zf" ]] && strike="$(cat "$zf")"

    # Session dead = immediate failure
    if ! tmux has-session -t "$session" 2>/dev/null; then
        echo "3" > "$zf"
        log_event "$node" "zombie" "" "" "session_dead"
        return 1
    fi

    # Find latest file mod time across output/ and for-orchestrator/
    local now latest_mod=0
    now="$(date +%s)"
    while IFS= read -r f; do
        local mt; mt="$(stat -f %m "$f" 2>/dev/null || echo 0)"
        (( mt > latest_mod )) && latest_mod=$mt
    done < <(find "$node/output" "$node/input" "$node/for-orchestrator" -maxdepth 1 -type f -newer "$node/for-orchestrator/.spawn_ts_"* 2>/dev/null || true)

    if (( latest_mod == 0 )); then
        local spf; spf="$(ls "$node/for-orchestrator"/.spawn_ts_* 2>/dev/null | head -1)"
        [[ -n "$spf" ]] && latest_mod="$(stat -f %m "$spf" 2>/dev/null || echo "$now")" || latest_mod=$now
    fi

    local elapsed=$(( now - latest_mod ))

    # Check tmux pane for thinking indicators
    local pane; pane="$(tmux capture-pane -t "$session" -p -l 5 2>/dev/null || echo "")"
    local thinking=0
    echo "$pane" | grep -qiE '(thinking|⠋|⠙|⠹|⠸|⠼|⠴|⠦|⠧|⠇|⠏|\.\.\.)' && thinking=1

    if (( thinking == 1 || elapsed < ZOMBIE_TIMEOUT )); then
        (( strike > 0 )) && echo "0" > "$zf"
        return 0
    fi

    # Advance strike
    strike=$(( strike + 1 ))
    echo "$strike" > "$zf"

    case $strike in
        1)  log_event "$node" "zombie_nudge" "" "" "strike=1 idle=${elapsed}s"
            tmux send-keys -t "$session" -l "Continue where you left off."
            sleep 0.3; tmux send-keys -t "$session" Enter
            echo "  [zombie] nudge: $session (${elapsed}s idle)" ;;
        2)  log_event "$node" "zombie_respawn" "" "" "strike=2 idle=${elapsed}s"
            local mode; mode="$(echo "$session" | rev | cut -d'-' -f1 | rev)"
            kill_agent "$session"; sleep 1
            spawn_agent "$node" "$mode"
            echo "  [zombie] respawn: $session" ;;
        *)  log_event "$node" "zombie_failed" "" "" "strike=$strike"
            echo "  [zombie] FAILED: $session"; return 1 ;;
    esac
    return 0
}

# ---- Plan parsing ----------------------------------------------------------

get_plan_review_tier() {
    local pf="$1/output/plan.md"
    [[ ! -f "$pf" ]] && echo "low" && return
    local tier; tier="$(grep -m1 '^Review:' "$pf" | sed 's/^Review:[[:space:]]*//' | tr -d '[:space:]')"
    echo "${tier:-low}"
}

plan_is_approved() {
    [[ -f "$1/output/plan.md" ]] && grep -q '^Status:.*approved' "$1/output/plan.md"
}

# Returns step_number|short_name|goal_text|complexity|importance for the first step with no child dir
parse_next_step() {
    local node="$1" pf="$1/output/plan.md" cdir="$1/children"
    [[ ! -f "$pf" ]] && return 1

    local snum="" sname="" goal="" complexity="" importance="" in_goal=0

    while IFS= read -r line; do
        if [[ "$line" =~ ^###[[:space:]]+Step[[:space:]]+([0-9]+):[[:space:]]+(.*) ]]; then
            if [[ -n "$snum" && -n "$goal" ]]; then
                local dn; dn="$(printf "step-%02d-%s" "$snum" "$sname")"
                [[ ! -d "$cdir/$dn" ]] && echo "${snum}|${sname}|${goal}|${complexity:-5}|${importance:-5}" && return 0
            fi
            snum="${BASH_REMATCH[1]}"; sname="${BASH_REMATCH[2]%"${BASH_REMATCH[2]##*[![:space:]]}"}"
            goal=""; complexity=""; importance=""; in_goal=0; continue
        fi
        if [[ "$line" =~ ^Goal:[[:space:]]*(.*) ]]; then
            goal="${BASH_REMATCH[1]}"; in_goal=1; continue
        fi
        if [[ "$line" =~ ^Complexity:[[:space:]]*([0-9]+) ]]; then
            complexity="${BASH_REMATCH[1]}"; in_goal=0; continue
        fi
        if [[ "$line" =~ ^Importance:[[:space:]]*([0-9]+) ]]; then
            importance="${BASH_REMATCH[1]}"; in_goal=0; continue
        fi
        if (( in_goal )); then
            [[ "$line" =~ ^(Complexity|Importance|Dependencies|Independent|Confidence|Verifiable|###) ]] && in_goal=0 || goal+=$'\n'"$line"
        fi
    done < "$pf"

    if [[ -n "$snum" && -n "$goal" ]]; then
        local dn; dn="$(printf "step-%02d-%s" "$snum" "$sname")"
        [[ ! -d "$cdir/$dn" ]] && echo "${snum}|${sname}|${goal}|${complexity:-5}|${importance:-5}" && return 0
    fi
    return 1
}

all_steps_terminal() {
    local node="$1" cdir="$1/children" pf="$1/output/plan.md"
    [[ ! -d "$cdir" ]] && return 1
    local total=0 term=0
    while IFS= read -r line; do
        [[ "$line" =~ ^###[[:space:]]+Step[[:space:]]+[0-9]+: ]] && ((total++))
    done < "$pf"
    (( total == 0 )) && return 1
    for d in "$cdir"/step-*/; do
        [[ ! -d "$d" ]] && continue
        local s; s="$(read_status "$d")"
        [[ "$s" =~ ^(complete|escalated|failed|cancelled)$ ]] && ((term++))
    done
    (( term >= total ))
}

# ---- Node discovery --------------------------------------------------------

find_all_nodes() {
    find "$1" -name "this-nodes-current-status" -type f 2>/dev/null | while read -r f; do
        # Go up from for-orchestrator/this-nodes-current-status to the node dir
        dirname "$(dirname "$f")"
    done
}

find_active_child() {
    local cdir="$1/children"
    [[ ! -d "$cdir" ]] && return 1
    for d in "$cdir"/step-*/; do
        [[ ! -d "$d" ]] && continue
        local s; s="$(read_status "$d")"
        [[ ! "$s" =~ ^(complete|escalated|failed|cancelled)$ ]] && echo "$d" && return 0
    done
    return 1
}

find_latest_terminal_child() {
    local cdir="$1/children" best="" best_t=0
    [[ ! -d "$cdir" ]] && return 1
    for d in "$cdir"/step-*/; do
        [[ ! -d "$d" ]] && continue
        local s; s="$(read_status "$d")"
        if [[ "$s" =~ ^(complete|escalated|failed)$ ]]; then
            local mt; mt="$(stat -f %m "$d/for-orchestrator/this-nodes-current-status" 2>/dev/null || echo 0)"
            (( mt > best_t )) && best_t=$mt && best="$d"
        fi
    done
    [[ -n "$best" ]] && echo "$best" && return 0
    return 1
}

cancel_pending_children() {
    local cdir="$1/children"
    [[ ! -d "$cdir" ]] && return
    for d in "$cdir"/step-*/; do
        [[ ! -d "$d" ]] && continue
        local s; s="$(read_status "$d")"
        [[ "$s" =~ ^(complete|cancelled|failed)$ ]] && continue
        write_status "$d" "$s" "cancelled" || true
        log_event "$d" "cancelled_by_parent" "$s" "cancelled"
    done
}

create_child() {
    local node="$1" snum="$2" sname="$3" goal="$4" complexity="${5:-5}" importance="${6:-5}"
    local dn; dn="$(printf "step-%02d-%s" "$snum" "$sname")"
    local cd="$node/children/$dn"
    [[ -d "$cd" ]] && return 0
    mkdir -p "$cd/input" "$cd/output" "$cd/for-orchestrator"
    echo "$goal" > "$cd/input/parent-instructions-and-relevant-information.md"

    # Depth-adjusted threshold: subtract depth from both scores, then check > PLAN_THRESHOLD
    # This naturally discourages planning at deeper levels
    local depth; depth="$(get_depth "$cd" "$TREE_ROOT")"
    local adj_c=$(( complexity - depth )); (( adj_c < 1 )) && adj_c=1
    local adj_i=$(( importance - depth )); (( adj_i < 1 )) && adj_i=1
    local ci=$(( adj_c * adj_i ))
    local agent_mode="executor"
    (( ci > PLAN_THRESHOLD )) && agent_mode="planner"

    # Max depth nodes must execute regardless of score
    (( depth >= MAX_DEPTH )) && agent_mode="executor"

    echo "$agent_mode" > "$cd/for-orchestrator/agent-mode"
    echo "pending" > "$cd/for-orchestrator/this-nodes-current-status"
    log_event "$node" "child_created" "" "" "child=$dn C=$complexity I=$importance adjC=$adj_c adjI=$adj_i CI=$ci depth=$depth mode=$agent_mode"
    echo "  [child] $dn (C=${complexity} I=${importance} adj=${adj_c}×${adj_i}=${ci} d=${depth} → ${agent_mode})"
}

# ---- Status handlers -------------------------------------------------------

handle_pending() {
    write_status "$1" "pending" "retrieving" && spawn_agent "$1" "retrieval"
}

handle_retrieving() {
    local node="$1"
    if [[ -f "$node/input/retrieved_relevant_knowledge_from_library.md" ]]; then
        # Read agent mode (planner/executor). Default to planner for root.
        local agent_mode="planner"
        [[ -f "$node/for-orchestrator/agent-mode" ]] && agent_mode="$(cat "$node/for-orchestrator/agent-mode")"
        write_status "$node" "retrieving" "running" && spawn_agent "$node" "$agent_mode"
        return
    fi
    check_zombie "$node" "$(sanitize_session_name "$node" "retrieval")" || \
        write_status "$node" "retrieving" "failed" || true
}

handle_running() {
    local node="$1"
    if [[ -f "$node/output/final-output.md" ]]; then
        write_status "$node" "running" "complete" || true; return; fi
    if [[ -f "$node/output/plan.md" ]]; then
        local depth; depth="$(get_depth "$node" "$TREE_ROOT")"
        if (( depth >= MAX_DEPTH )); then
            log_event "$node" "max_depth" "" "" "depth=$depth"
            write_status "$node" "running" "failed" || true; return; fi
        local tier; tier="$(get_plan_review_tier "$node")"
        if [[ "$tier" == "low" ]]; then
            grep -q '^Status:.*approved' "$node/output/plan.md" || \
                sed -i '' 's/^Status:.*/Status: approved/' "$node/output/plan.md"
            write_status "$node" "running" "approved" || true
        else
            write_status "$node" "running" "needs_review" || true
        fi
        return
    fi
    [[ -f "$node/output/escalation.md" ]] && { write_status "$node" "running" "escalated" || true; return; }
    [[ -f "$node/for-orchestrator/WAITING_FOR_COMPUTATION" ]] && { write_status "$node" "running" "waiting_comp" || true; return; }
    # Zombie check — agent mode could be executor or planner
    local agent_mode="planner"
    [[ -f "$node/for-orchestrator/agent-mode" ]] && agent_mode="$(cat "$node/for-orchestrator/agent-mode")"
    check_zombie "$node" "$(sanitize_session_name "$node" "$agent_mode")" || \
        write_status "$node" "running" "failed" || true
}

handle_needs_review() {
    write_status "$1" "needs_review" "reviewing" && spawn_agent "$1" "reviewer"
}

handle_reviewing() {
    local node="$1"
    if [[ -f "$node/output/review.md" ]]; then
        write_status "$node" "reviewing" "needs_decision" || true; return; fi
    check_zombie "$node" "$(sanitize_session_name "$node" "reviewer")" || \
        write_status "$node" "reviewing" "failed" || true
}

handle_needs_decision() {
    write_status "$1" "needs_decision" "deciding" && spawn_agent "$1" "decider"
}

handle_deciding() {
    local node="$1"
    plan_is_approved "$node" && { write_status "$node" "deciding" "approved" || true; return; }
    [[ -f "$node/output/escalation.md" ]] && { write_status "$node" "deciding" "escalated" || true; return; }
    check_zombie "$node" "$(sanitize_session_name "$node" "decider")" || \
        write_status "$node" "deciding" "failed" || true
}

handle_approved() {
    local node="$1" next
    if ! next="$(parse_next_step "$node")"; then
        log_event "$node" "error" "approved" "" "no_steps_in_plan"
        write_status "$node" "approved" "failed" || true; return; fi
    local snum sname goal complexity importance
    IFS='|' read -r snum sname goal complexity importance <<< "$next"
    create_child "$node" "$snum" "$sname" "$goal" "$complexity" "$importance"
    write_status "$node" "approved" "executing" || true
}

handle_executing() {
    local node="$1"
    # If a child is still active, wait
    find_active_child "$node" >/dev/null 2>&1 && return

    local child; child="$(find_latest_terminal_child "$node")" || {
        log_event "$node" "error" "executing" "" "no_children"; return; }
    local cs; cs="$(read_status "$child")"

    case "$cs" in
        complete)
            if all_steps_terminal "$node"; then
                write_status "$node" "executing" "evaluating" && spawn_agent "$node" "synthesis"
            else
                write_status "$node" "executing" "evaluating" && spawn_agent "$node" "evaluation"
            fi ;;
        escalated|failed)
            write_status "$node" "executing" "evaluating" && spawn_agent "$node" "evaluation" ;;
    esac
}

handle_evaluating() {
    local node="$1" df="$1/for-orchestrator/eval-decision"
    # Synthesis mode: the agent writes final-output.md directly
    if [[ -f "$node/output/final-output.md" ]] && [[ ! -f "$df" ]]; then
        write_status "$node" "evaluating" "complete" || true
        return
    fi
    if [[ ! -f "$df" ]]; then
        # Zombie check on whichever eval/synth session is alive
        for m in synthesis evaluation; do
            local s; s="$(sanitize_session_name "$node" "$m")"
            tmux has-session -t "$s" 2>/dev/null && {
                check_zombie "$node" "$s" || write_status "$node" "evaluating" "failed" || true
                return
            }
        done
        return
    fi

    local dec; dec="$(tr -d '[:space:]' < "$df")"
    case "$dec" in
        continue)
            local next; next="$(parse_next_step "$node")" || true
            if [[ -n "$next" ]]; then
                local sn sname goal complexity importance; IFS='|' read -r sn sname goal complexity importance <<< "$next"
                create_child "$node" "$sn" "$sname" "$goal" "$complexity" "$importance"
                # Append context from evaluation agent if present
                local ctx_file="$node/output/context-for-next-step.md"
                if [[ -f "$ctx_file" ]]; then
                    local dn; dn="$(printf "step-%02d-%s" "$sn" "$sname")"
                    local child_pi="$node/children/$dn/input/parent-instructions-and-relevant-information.md"
                    if [[ -f "$child_pi" ]]; then
                        printf '\n\n## Context From Prior Steps\n\n%s\n' "$(cat "$ctx_file")" >> "$child_pi"
                    fi
                    rm -f "$ctx_file"
                    log_event "$node" "context_passed" "" "" "to=step-$(printf '%02d' "$sn")-$sname"
                fi
            fi
            rm -f "$df"; write_status "$node" "evaluating" "executing" || true ;;
        replan)
            cancel_pending_children "$node"
            rm -f "$df"; write_status "$node" "evaluating" "approved" || true ;;
        escalate)
            cancel_pending_children "$node"
            rm -f "$df"; write_status "$node" "evaluating" "escalated" || true ;;
        synthesize)
            [[ -f "$node/output/final-output.md" ]] && { rm -f "$df"; write_status "$node" "evaluating" "complete" || true; } ;;
        *)  log_event "$node" "error" "evaluating" "" "unknown_decision=$dec" ;;
    esac
}

handle_waiting_comp() {
    local node="$1"
    if [[ -f "$node/for-orchestrator/computation_result" ]]; then
        local agent_mode="planner"
        [[ -f "$node/for-orchestrator/agent-mode" ]] && agent_mode="$(cat "$node/for-orchestrator/agent-mode")"
        write_status "$node" "waiting_comp" "running" && spawn_agent "$node" "$agent_mode"; return; fi
    local wf="$node/for-orchestrator/WAITING_FOR_COMPUTATION"
    if [[ -f "$wf" ]]; then
        local started now; started="$(stat -f %m "$wf" 2>/dev/null || echo 0)"; now="$(date +%s)"
        (( now - started > COMP_TIMEOUT )) && {
            log_event "$node" "comp_timeout" "" "" "elapsed=$(( now - started ))s"
            write_status "$node" "waiting_comp" "failed" || true; }
    fi
}

handle_cancelled() {
    for m in executor planner retrieval reviewer decider evaluation synthesis; do
        kill_agent "$(sanitize_session_name "$1" "$m")"
    done
}

# ---- Main loop -------------------------------------------------------------

echo "Entering main loop (Ctrl+C to stop)..."

while true; do
    nodes=()
    while IFS= read -r n; do nodes+=("$n"); done < <(find_all_nodes "$MISSION_DIR")

    for node_path in "${nodes[@]}"; do
        # Chain transitions: after any status change, immediately re-handle
        # the node instead of waiting for the next poll cycle.
        chain_limit=10
        chain_count=0
        while (( chain_count < chain_limit )); do
            status="$(read_status "$node_path")"
            [[ -z "$status" ]] && break
            case "$status" in
                pending)        handle_pending "$node_path" ;;
                retrieving)     handle_retrieving "$node_path" ;;
                running)        handle_running "$node_path" ;;
                needs_review)   handle_needs_review "$node_path" ;;
                reviewing)      handle_reviewing "$node_path" ;;
                needs_decision) handle_needs_decision "$node_path" ;;
                deciding)       handle_deciding "$node_path" ;;
                approved)       handle_approved "$node_path" ;;
                executing)      handle_executing "$node_path" ;;
                evaluating)     handle_evaluating "$node_path" ;;
                waiting_comp)   handle_waiting_comp "$node_path" ;;
                cancelled)      handle_cancelled "$node_path" ;;
                complete|escalated|failed) break ;;
                *) log_event "$node_path" "unknown_status" "$status" "" ""; break ;;
            esac
            new_status="$(read_status "$node_path")"
            [[ "$new_status" == "$status" ]] && break
            ((chain_count++))
        done
    done

    # Also pick up newly created children in the same cycle
    new_nodes=()
    while IFS= read -r n; do new_nodes+=("$n"); done < <(find_all_nodes "$MISSION_DIR")
    for node_path in "${new_nodes[@]}"; do
        status="$(read_status "$node_path")"
        [[ "$status" == "pending" ]] && handle_pending "$node_path"
    done

    # Check root terminal state
    root_status="$(read_status "$TREE_ROOT")"
    case "$root_status" in
        complete)  echo ""; echo "Mission COMPLETE.";  log_event "$TREE_ROOT" "mission_complete" "" ""; exit 0 ;;
        failed)    echo ""; echo "Mission FAILED.";    log_event "$TREE_ROOT" "mission_failed" "" "";   exit 1 ;;
        escalated) echo ""; echo "Root ESCALATED.";    log_event "$TREE_ROOT" "mission_escalated" "" ""; exit 1 ;;
    esac

    sleep "$POLL_INTERVAL"
done
