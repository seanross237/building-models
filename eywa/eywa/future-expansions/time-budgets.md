# Time Budgets

## Problem
Sub-trees can rabbit-hole, spending disproportionate time on tasks that don't warrant it. A meta-analysis step might create sub-planners that create more sub-children, burning 30+ minutes on what should be a 5-minute synthesis.

## Design

### Time budget propagation
1. Mission gets a total budget (e.g., `bash orchestrator.sh missions/x 15` for 15 minutes)
2. Root gets the full budget. Its instructions say "You have 15 minutes total."
3. Planner allocates `Minutes: N` to each step in its plan (must sum ≤ its budget)
4. Each child inherits its step's minute budget
5. That child's instructions say "You have N minutes for this task"
6. If that child plans, it subdivides its N minutes among its own steps

### Orchestrator enforcement
- Each node gets a `time_budget_minutes` file in for-orchestrator/
- Orchestrator tracks when each node started
- If a node has < 5 minutes budget: force executor mode regardless of C×I score
- If a node exceeds its budget: force to executor mode on next spawn (no more planning allowed)
- If the global mission deadline passes: kill everything, re-spawn root in synthesis mode with whatever results exist. Accept partial output.

### Why it works
Planners naturally make better decisions when they see the clock. A planner with 3 minutes left won't create a 5-step plan — it'll either execute directly or create 2 quick steps. The time pressure flows down through the tree organically.

### Plan format addition
Each step gets a `Minutes: N` field alongside Complexity and Importance.

### Key rule
Any node with < 5 minutes budget must execute, cannot plan.
