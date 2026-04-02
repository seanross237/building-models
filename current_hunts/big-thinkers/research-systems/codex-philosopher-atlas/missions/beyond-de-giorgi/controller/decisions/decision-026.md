# Decision Memo - beyond-de-giorgi / decision-026

## Decision

`proceed`

## Mission-Control Verdict

This is a bootstrap review after planning run `run-011`, not a post-step audit
of a completed step inside the new chain. The relevant question is whether the
replanning result is concrete enough to execute immediately or whether mission
control should reopen branch comparison again before spending step budget.

It is concrete enough.

`run-011` selected
`Chain 01 - Calibrated Tao Differential Audit With Exact Theorem-Floor Freeze And Mandatory Evidence Gate`
as the canonical next branch and installed that branch into `CHAIN.md`. That is
the right response to the current mission state created by `step-015`: the
geometry-first chain is already dead, but the mission question is still open and
the remaining exact-Navier-Stokes candidate families have not yet been filtered
through a single fixed Tao-differential and theorem-facing standard.

The new chain exists precisely to do that filtering before the mission commits
to geometry, pressure harmonicity, helical structure, or any other family. It
does not need another planning pass first. It needs its own Step 1 scope lock.

## Why `proceed` Is Right

The planning artifacts are aligned rather than conflicted:

- `final-decider.md` names Refined Chain 01 as the winner.
- `winning-chain.md` gives a concrete ordered chain with explicit kill
  conditions.
- `CHAIN.md` matches that winning chain exactly.

There is also no new negative evidence against this chain itself. The only new
negative evidence in the mission state is against the prior geometry branch, and
that failure is exactly why the new Tao-differential audit was chosen.

So the correct move is to execute logical Chain Step 1 now: freeze the exact
comparison contract, the comparison level, the theorem floor, the primary
endpoint family, the four ledgers, and one clear pass/fail pair for the Tao
filter.

## Why `replan` Is Wrong

Replanning again would amount to discarding the result of `run-011` before it
has been tested. The mission already paid for a fresh comparison after the
geometry branch died. That comparison produced a sharper chain whose whole point
is to stop the mission from making another premature mechanism commitment.

Nothing in the planning output suggests ambiguity severe enough to justify a new
selector pass. The next uncertainty is execution uncertainty, and that belongs
inside Step 1 of the active chain rather than inside another planning run.

## Why `terminate` Is Wrong

The mission is not complete. `step-015` killed one geometry-first route, but it
did not show that every exact-NS structural candidate fails, and `run-011` was
explicitly designed to compare the surviving families under harsher evidence
rules.

There is therefore no positive completion and no terminal negative completion.
At most, the mission has reached a new branch-selection state, and that state
has already been resolved by the planning run.

## Required Next Controller Move

Proceed into `step-016` as logical Chain Step 1 of the active chain.

That step should stay narrow and activation-focused. It should:

- define exactly what counts as Tao destruction at one fixed comparison level;
- distinguish the allowed status classes, not just `destroyed` versus
  `preserved`;
- freeze one theorem floor and one primary endpoint family for the audit;
- freeze the Tao distinctiveness, theorem-floor admissibility, endpoint
  contact, and bridge-debt ledgers; and
- give one clear passing example and one clear failing example for the
  Tao-differential rule.

If those items cannot be frozen concretely, the chain should stop immediately
with an under-specified comparison memo rather than drifting into candidate
cards.
