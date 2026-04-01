# Continue / Replan / Escalate Guidance

## Continue

Choose continue when the plan is still on track and the next step still makes sense given what you have learned.

Action:

- write `continue` to `for-orchestrator/eval-decision`
- if needed, write `output/context-for-next-step.md`
- update `output/state.md`

## Replan

Choose replan when the goal is still achievable but the remaining steps should change.

Action:

- write an updated `output/plan.md` with `Status: draft`
- write `replan` to `for-orchestrator/eval-decision`
- update `output/state.md`

Preserve completed valid work when you replan.

## Escalate

Choose escalate when you can no longer produce what your parent expects.

Action:

- write `output/escalation.md`
- write `escalate` to `for-orchestrator/eval-decision`
- update `output/state.md`

## The Core Question

Can this node still produce what its parent expects, given what is now known?
