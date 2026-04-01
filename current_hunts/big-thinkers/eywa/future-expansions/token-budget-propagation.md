# Token Budget Propagation

## Problem
Without token limits, a sub-tree can burn through disproportionate API spend. A planner that spawns many children, each of which spawns their own children, can rack up significant token costs on a branch that doesn't warrant it. There's no mechanism to constrain spend per subtree relative to its importance.

## Design
Parent allocates a token budget to each child step, similar to how time budgets work. The orchestrator tracks cumulative token usage per subtree and enforces limits.

### Budget flow
1. Mission gets a total token budget
2. Root planner allocates tokens per step (must sum <= its budget)
3. Each child inherits its step's token budget
4. If a child plans, it subdivides its token budget among its own steps

### Enforcement
- Track token usage per node (requires parsing API usage from agent output or using a proxy/wrapper)
- When a subtree approaches its budget: warn the agent in its next spawn's instructions
- When a subtree exceeds its budget: force to executor mode (no more planning), or force synthesis with partial results

## Key Considerations
- Token tracking is harder than time tracking. Need a reliable way to measure tokens consumed per agent session.
- Token budgets and time budgets are complementary -- a fast agent can still be expensive if it generates long outputs. Both constraints may be useful simultaneously.
- Budget allocation adds cognitive load to planners. May want to auto-allocate proportional to Importance scores as a default, with manual override.
