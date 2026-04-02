# Decision Memo - exact-ns-no-near-closed-tao-circuit / decision-009

## Decision

`replan`

## Mission-Control Verdict

The active chain should not proceed in order any further. `step-006` succeeds
at exactly the job Chain Step 6 was meant to do: it freezes a downstream object
set and hands off explicit next-test assignments.

Its result is positive at the branch level:

- two survivors are promoted on the frozen one-bridge packet ledger:
  repaired `Template-Defect Near-Closure` and repaired
  `Windowed Spectator-Leakage Budget`;
- each promoted object now has a fixed criterion, threshold sheet, packet
  semantics, canonicalization policy, invariant gate, and named first exact
  theorem question;
- the discarded itinerary route stays closed in named buckets:
  `pre-trigger delay filter` as
  `not useful for the target theorem or counterexample question`,
  and
  `next-stage transfer-start filter` as
  `not well-defined`;
- no Step-6 kill condition fired; and
- the step explicitly packages the result as a branch handoff to later exact
  work.

That is not an `active` continuation signal for the same chain. It is a
successful chain completion. The current branch has finished its ordered job:
freeze the object set and specify the next-test handoff. The mission has not
yet earned a theorem, counterexample, or terminal negative kill, so the
correct conservative move is to replan from this completed branch output.

## Why `proceed` Is Wrong

Proceeding would assume there is another in-order step inside `CHAIN.md`, but
the canonical chain ends at Chain Step 6. Its final ordered action is exactly
the downstream-object freeze that `step-006` has now completed.

The next choices are no longer chain-internal execution choices. They are
mission-control choices about what exact downstream branch to run next from the
frozen handoff:

- the theorem-facing `G_tmpl` test on `F_SL(rho)` for `0 < rho <= 1/16`;
- the obstruction-facing `G_leak` test on the carried stress set
  `{F_SS(1/12), F_SL(1/16)}`; or
- some explicitly compared follow-on structure that decides how those two
  promoted objects should be pursued.

That comparison belongs to replanning, not blind continuation under a chain
whose ordered steps are already exhausted.

## Why `terminate` Is Wrong

The mission-level question is still open. `step-006` does not deliver a final
no-near-circuit theorem, a final counterexample, or a terminal definition-level
failure. It delivers two honest promoted objects with strict no-overclaim
guardrails and concrete next-test assignments.

That is a strong branch output, but it is not mission completion. Stopping now
would confuse a successful object-freeze handoff with a finished answer to the
mission's central question.

## Required Next Controller Move

Mission control should replan now.

The replanning pass should treat the current chain as `completed`, not
invalidated, and use the Step-6 handoff as the new input record. It should
compare the next live branch options on the frozen packet sheet and earned
guardrails, rather than reopening the completed definition/repair chain.

At minimum, the next planning comparison should decide whether the best next
mission move is:

- a theorem-facing branch centered on repaired `Template-Defect Near-Closure`;
- an obstruction-facing branch centered on repaired
  `Windowed Spectator-Leakage Budget`; or
- a deliberately structured follow-on that keeps both promoted objects but
  assigns them non-overlapping exact roles.

Whatever wins next should start from the frozen Step-6 object set, invariant
gates, and no-overclaim limits already earned.
