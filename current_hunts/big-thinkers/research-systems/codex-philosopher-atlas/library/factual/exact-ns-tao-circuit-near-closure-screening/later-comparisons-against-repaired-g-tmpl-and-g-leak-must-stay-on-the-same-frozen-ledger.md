# Later Comparisons Against Repaired G_tmpl And G_leak Must Stay On The Same Frozen Ledger

Status: `VERIFIED` frozen ledger definitions with `INFERRED` same-currency carry rule

The branch-specific interaction currency remains fixed from the earlier
freeze:

`D_on(t) := |Q_clk(t)| + |Q_seed(t)| + |Q_amp(t)| + |Q_rot^D(t)| + |Q_rot^A(t)| + |Q_next(t)|`

`D_off(t) := D_mirror(t) + D_companion(t) + D_feedback(t) + D_cross(t)`

Any later closure or dynamics comparison against repaired `G_tmpl` or
repaired `G_leak` is honest only on this same frozen canonical packet ledger:
the same packet semantics, the same role order, the same sign / amplitude /
phase sheet, the same spectator partition, the same `D_on` / `D_off` split,
and the same fixed window `I = [0, 1]`.

Changing packet semantics, changing the sign or phase sheet, changing the
spectator partition, changing the `D_on` / `D_off` split, changing the
window, or inserting a comparison in a different bookkeeping currency does
not sharpen the repaired Step-6 objects.
It leaves the branch's frozen ledger and becomes a different comparison.

Step 7 therefore carries a same-currency rule as part of the downstream
authority sheet:
later work may test or sharpen the repaired objects only on the exact ledger
that already fixed the witness, packet conventions, and classwise currencies.

Step 7 also fixes the line between closure-forced bookkeeping and rescue on
that ledger.
Extra bridge,
shell-locked mode,
post hoc companion,
witness swap,
threshold retuning,
alternate bookkeeping currency,
and post hoc rephasing are not honest downstream additions.
If exact closure forces the branch outside the audited one-bridge class or
forces uncontrolled packet growth, that is a negative closure result rather
than permission to rewrite Step 1 after the fact.

Filed from:
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-007-exploration-001-frozen-witness-and-authority-sheet.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-007-exploration-002-scorecard-guardrails-and-step-2-readiness.md`
