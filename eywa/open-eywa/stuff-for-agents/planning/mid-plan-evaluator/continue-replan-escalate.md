# Continue / Replan / Escalate Guidance

## Continue

Choose continue when the plan is still on track and the next step still makes sense given what you have learned.

Also choose continue when the latest child completed successfully and the node can still finish normally.

If the latest child completed the final planned step successfully, still choose continue. The orchestrator will advance the node to final synthesis/completion from there.

Action:

- if needed, write `output/context-for-next-step.md`
- update `output/state.md`
- end your final assistant message with `NEXT_ACTION_AFTER_CHILD_REPORT: continue`

## Replan

Choose replan when the goal is still achievable but the remaining steps should change.

Action:

- write an updated `output/plan.md` with `Status: draft`
- update `output/state.md`
- end your final assistant message with `NEXT_ACTION_AFTER_CHILD_REPORT: replan`

Preserve completed valid work when you replan.

## Escalate

Choose escalate when you can no longer produce what your parent expects.

Action:

- write `output/escalation.md`
- update `output/state.md`
- end your final assistant message with `NEXT_ACTION_AFTER_CHILD_REPORT: escalate`

Do not choose escalate merely because there are no more remaining child steps after a successful final step. That is a normal successful path and should be `continue`.

## The Core Question

Can this node still produce what its parent expects, given what is now known?
