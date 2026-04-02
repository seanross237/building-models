# Decision Memo - exact-ns-no-near-closed-tao-circuit / decision-010

## Decision

`proceed`

## Mission-Control Verdict

This is a bootstrap decision after planning run `run-002`, not a review of a
completed step on the new branch.

That matters because the record is aligned. `decision-009` already marked the
previous chain completed at `step-006`, so the relevant control question now is
whether the replanning run produced one clear successor branch or whether the
mission should compare branches again immediately. The answer is that the new
planning run already did the comparison and converged cleanly:

- `final-decider.md` selects refined Chain 03 as the single execution winner;
- `winning-chain.md` matches the current `CHAIN.md` exactly;
- `judgments/chain-03.md` explains the necessary narrowing of the moonshot
  branch into a disciplined witness-local audit of `F_SS(1/12)`;
- and the numbering mismatch in `selected/chain-03.md` is only historical
  traceability from the portfolio stage, not a live ambiguity about the active
  branch.

So the current chain is active. Its first gate is concrete and conservative:
freeze one named witness, freeze one authoritative Step-6 scorecard, forbid
revival of demoted itinerary gates as pass/fail criteria, and forbid
discretionary repair before exact closure is earned. That is a real next step,
not a vague continuation signal, so mission control should proceed to
`step-007`.

## Why `replan` Is Wrong

Replanning would be correct only if the new branch were already materially
weakened, internally inconsistent, or overtaken by a better path after the
planning run. None of that has happened.

`run-002` already compared the serious follow-on options that Step-6 opened:

- a broader joint-gate synthesis route;
- a leakage-sharpness obstruction route; and
- the witness-local constructive moonshot centered on `F_SS(1/12)`.

The final decider did not leave those branches tied. It chose one winner and
hardened it into the current `CHAIN.md`. Another replanning pass now would not
respond to new evidence. It would only repeat a branch comparison that the
mission has already earned.

## Why `terminate` Is Wrong

The mission-level question is still open. Step-6 froze two promoted downstream
objects, but it did not produce a final no-near-circuit theorem, a terminal
counterexample, or a terminal negative kill. The new witness-local chain has
not yet been executed.

Stopping here would confuse a successful replanning handoff with mission
completion.

## Chain Assessment

The current chain remains `active`.

The next logical move is:
**Chain Step 1 only: Freeze the single witness, authority sheet, and honest
scorecard.**

That next step should stay tightly scoped to the branch's first gate. It
should:

- freeze `F_SS(1/12)` itself, not reopen the larger `F_SS(mu)` family;
- treat the Step-6 repaired `G_tmpl` and `G_leak` sheets as the controlling
  pass/fail authority for this branch;
- log earlier threshold drift, especially the `L_cross` mismatch, as
  historical record variance rather than a live choice;
- keep `t_clk`, `t_trig`, `t_rot`, and `t_next` only as secondary diagnostics;
- forbid discretionary repair or class-changing rescue;
- and stop immediately if the witness cannot be frozen without reopening
  `mu`, packet semantics, or the Step-6 threshold sheet.

## Required Next Move

Proceed to `step-007`.

The correct controller move is to open the new chain on its own terms, not to
restart mission-level branch selection before any step on that chain has been
run.
