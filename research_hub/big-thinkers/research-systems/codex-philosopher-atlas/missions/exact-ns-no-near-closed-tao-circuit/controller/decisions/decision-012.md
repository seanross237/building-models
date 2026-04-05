# Decision Memo - exact-ns-no-near-closed-tao-circuit / decision-012

## Decision

`replan`

## Mission-Control Verdict

`step-008` does not keep the active witness-local chain alive. The step ends
with the explicit branch verdict that **Chain Step 3 is not well posed** and
that the branch should **stop at exact closure**. On the frozen Step-7 ledger,
the repository now earns only a classwise exact-closure picture plus the
constructive verdict

```text
exact non-isolability / arbitrary-truncation requirement
```

for `F_SS(1/12)`. It does not earn the one finite exact closed subsystem that
the current chain needed before an honest dynamic stress test could begin.

That is a real branch result, not a null run. It materially weakens the branch
and closes it in its present form. The result is useful because it narrows the
live search space and sharpens the obstruction story, but it is still
witness-local and ledger-scoped. It does not yet answer the full mission
question about whether a quantitative no-near-closed Tao-circuit statement can
be formulated and tested across the mission's surviving exact objects. Mission
control should therefore replan.

## Why `proceed` Is Wrong

Proceeding would require treating Chain Step 3 as the next in-order move.
`step-008` explicitly rejects that. The step says no finite honest closed
system was produced that later dynamics could inherit unchanged, and its own
kill condition fires because the exact closure picture remains too implicit for
a dynamic audit on the same frozen ledger.

So there is no honest `step-009` GOAL on the current chain. Writing one would
bypass the branch's failed closure gate and would turn a useful negative result
into blind momentum.

## Why `terminate` Is Wrong

The mission-level question is still open. `step-008` does not deliver:

- a mission-level impossibility theorem;
- a definitive near-circuit counterexample; or
- a final definition-level kill covering the whole surviving mission scope.

Instead it delivers a branch-local negative on one named witness,
`F_SS(1/12)`. That is strong enough to stop this chain, but not strong enough
to stop the mission.

## Required Next Controller Move

Mission control should replan now.

The replanning pass should treat the current chain as `invalidated`, not
`active` and not `completed`. The branch did not finish its intended exact-
audit route; it failed its closure gate before the dynamic phase. The new
planning input should therefore combine:

- the Step-6 promoted downstream object set and guardrails;
- the run-002 comparison record; and
- the new Step-8 witness-local negative that `F_SS(1/12)` does not presently
  yield one finite exact closed subsystem on the frozen ledger.

The next planning comparison should decide which remaining exact branch best
uses that new negative evidence, rather than reopening the invalidated
`F_SS(1/12)` dynamic-audit chain in order.
