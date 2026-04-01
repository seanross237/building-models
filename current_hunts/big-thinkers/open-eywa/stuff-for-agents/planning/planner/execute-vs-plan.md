# Execute vs. Plan Guidance

Your first question is:

Should this node do the work directly, or should it break the work into child steps?

## Default Heuristic

Execute directly if one focused agent can complete the task with a clear path from start to finish.

Plan if the task has multiple distinct sub-problems, different approaches, or sequential dependencies where later steps depend on earlier discoveries.

## Signals Favoring Direct Execution

- the task is self-contained
- the success criteria are obvious
- one competent agent can finish it in one session
- decomposition would only create 1-2 trivial sub-steps
- the node is already deep in the tree

## Signals Favoring Planning

- the task clearly has multiple separable sub-problems
- different steps need different approaches or expertise
- the right path depends on intermediate findings
- decomposition would clarify a vague goal
- failure in one branch should not waste work done in another

## Key Question

Would fresh child agents have enough context to succeed independently?

If not, either include that context explicitly in their goals or execute directly instead of planning.

## Anti-Patterns

- over-splitting
- under-splitting
- splitting for outline aesthetics rather than real task boundaries
- forcing every problem into the same linear template
