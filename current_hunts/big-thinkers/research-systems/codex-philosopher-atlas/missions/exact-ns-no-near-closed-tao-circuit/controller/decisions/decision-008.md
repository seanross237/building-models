# Decision Memo - exact-ns-no-near-closed-tao-circuit / decision-008

## Decision

`proceed`

## Mission-Control Verdict

`step-005` passes the active chain's fifth gate. The latest step does not leave
the branch in a soft maybe-state. It turns the Step-4 survivor set into a
decision-grade shortlist:

- repaired `Template-Defect Near-Closure` survives with tightened
  `lambda_tmpl = 1/4`
  and
  `lambda_spec = 49/256`;
- repaired `Windowed Spectator-Leakage Budget` survives with the repaired
  classwise budget vector
  `(1/4, 1/12, 1/12, 1/16, 1/24)`;
- `pre-trigger delay filter` is discarded as
  `not useful for the target theorem or counterexample question`;
- `next-stage transfer-start filter` is discarded as
  `not well-defined`;
- no Step-5 kill condition fired; and
- Chain Step 6 is explicitly declared well-posed.

That keeps the current chain active. The branch has now done what Step 5 was
supposed to do: use one honest repair pass to separate promotable objects from
dead routes and attach concrete downstream gates to the survivors. Mission
control should therefore proceed to `step-006`.

The wrapper stalls noted in the step package do not change that verdict. The
local record now contains the mathematical outputs that matter for control:
the repaired shortlist, the failure buckets for the discarded itinerary route,
and the explicit Step-6 handoff tasks.

## Why `replan` Is Wrong

Replanning is appropriate when the current branch has been materially weakened,
closed, or overtaken by a better path. `step-005` does the opposite. It narrows
the branch to two exact survivor objects on the frozen packet ledger and names
the precise failure modes of the behavior route. Opening a fresh branch
comparison now would throw away the chain at the moment it becomes most ready
for a final object-freeze judgment.

## Why `terminate` Is Wrong

The mission has not yet reached a terminal positive obstruction, terminal
counterexample, or terminal negative kill. Two candidates still survive the
full Step-5 repair pass and now have honest downstream gates. Stopping now
would confuse a successful shortlist freeze with a completed mission answer.

## Chain Assessment

The chain remains `active`.

The next logical move is:
**Freeze the downstream object set with explicit next tests.**

That next step should stay tightly scoped to Chain Step 6. It should freeze the
two surviving objects on the repaired thresholds and existing packet ledger,
assign one first exact theorem question or counterexample search to each, name
the smallest meaningful carried-forward witness family and invariant gate for
each, record the exact data still missing, and refuse any claim that reaches
beyond the audited packet class.
