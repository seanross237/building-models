# Execute vs. Plan Guidance

When you receive a task, your first decision is: do I execute this myself, or break it into a plan?

## Default Heuristic

**Execute** if the task can be completed in a single focused session of work. **Plan** if it requires multiple distinct sub-tasks, different angles of investigation, or sequential steps where later steps depend on what earlier steps discover.

## Signals Favoring Execution

- The task is self-contained within a single domain
- You can see a clear path from start to finish
- Success criteria are obvious
- The task is a leaf-level investigation, computation, or verification
- You are at **depth 5** (max depth — you MUST execute, planning is not an option)
- The task would decompose into only 1-2 trivial sub-steps (just do them yourself)

## Signals Favoring Planning

- The task has identifiable sub-problems that are distinct from each other
- Different steps require different expertise or approaches
- You need to gather information before you can determine the right approach
- The task is vague enough that decomposition would clarify it
- Failure of one part shouldn't waste the work of other parts
- You are at depth 1-2 (plenty of room to decompose)

## Depth Awareness

Your depth in the tree should bias your decision:

- **Depth 1-2:** Lean toward planning. You have room to decompose and the overhead is worth it for better-structured work.
- **Depth 3-4:** Lean toward execution unless the task clearly has distinct sub-problems. You're getting close to the limit.
- **Depth 5:** You MUST execute. This is a hard constraint.

## The Key Question

Before you split, ask yourself:

> "Will the children I create have enough context to succeed independently? Or will they need information that only exists in my reasoning right now?"

If the answer is "they'll need what's in my head," you either need to:
1. Include that context explicitly in their goals (and plan anyway), or
2. Just execute it yourself

## Anti-Patterns

- **Over-splitting:** Creating a 2-step plan where step 1 is "gather context" and step 2 is "do the thing." Just do the thing.
- **Under-splitting:** Taking on a task with 3+ distinct sub-problems and trying to do them all in one session, producing shallow work on each.
- **Splitting for structure's sake:** Creating a plan that mirrors an outline rather than reflecting actual task boundaries.
- **Linear-only plans:** Every step depends on the previous one and could have been done sequentially by a single agent. If there are no natural breakpoints, don't create artificial ones.

## What to Capture

Include your reasoning in output/state.md (your brain dump):
- What factors you weighed
- What you considered and rejected
- Your confidence in the decision
- What would change your mind
