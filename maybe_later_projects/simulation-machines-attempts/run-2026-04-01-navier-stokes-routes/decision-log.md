# Decision Log

## Cycle 1

- Action: Generate route families for the Navier-Stokes problem under a tight budget.
- Score: `criticality-and-concentration` 0.82, `partial-regularity-and-epsilon-bootstrapping` 0.74, `frequency-cascade-and-structure-rules` 0.58, `barrier-and-morrey-control` 0.51.
- Decision: Choose `criticality-and-concentration` as the primary route and retain `partial-regularity-and-epsilon-bootstrapping` as backup.
- Reason: Best long-horizon leverage and strongest option value.

## Cycle 2

- Action: Re-evaluate the primary route by asking whether it yields a short list of sharp intermediate checkpoints.
- Score: `criticality-and-concentration` 0.77, `partial-regularity-and-epsilon-bootstrapping` 0.79.
- Decision: Switch the active route to `partial-regularity-and-epsilon-bootstrapping`.
- Reason: It better satisfies the budget constraint because it creates concrete subgoals and clearer falsifiers.

## Cycle 3

- Action: Compare the two top routes after a budget-focused replanning step.
- Score: `partial-regularity-and-epsilon-bootstrapping` 0.84, `criticality-and-concentration` 0.76.
- Decision: Keep `partial-regularity-and-epsilon-bootstrapping` as the favored route and prune the weakest branches.
- Reason: It is the most executable route for a short run and the most likely to produce a useful next-step research agenda.
