# Windowed-Spectator Leakage Budget Honest Step-5 Repair Tightens Budgets To The Recorded Friendly Maxima

Status: `VERIFIED` Step-4 friendly maxima with `INFERRED` repair sheet

On the frozen Step-4 ledger, the largest recorded friendly leakage loads
across `F_SS(1/12)` and `F_SL(1/16)` are:
`L_tot = 1/4`,
`L_mirror = 1/12`,
`L_companion = 1/12`,
`L_feedback = 1/16`,
and
`L_cross = 1/24`.

The inherited Step-4 sheet used
`Lambda_tot = 3/8`,
`Lambda_mirror = 1/8`,
`Lambda_companion = 1/12`,
`Lambda_feedback = 1/12`,
and
`Lambda_cross = 1/12`.
Only the companion ceiling was already saturated by the recorded friendly
ledger.

The honest Step-5 repair is therefore:
`Lambda_tot: 3/8 -> 1/4`,
`Lambda_mirror: 1/8 -> 1/12`,
`Lambda_companion: 1/12 -> 1/12`,
`Lambda_feedback: 1/12 -> 1/16`,
and
`Lambda_cross: 1/12 -> 1/24`.

One stale Step-5 exploration record still writes `Lambda_cross = 1/12`, but
the controlling Step-5 result, the Step-6 freeze, and the repaired library
sheet all settle the carried cross budget at `L_cross = 1/24`.
Treat that disagreement as historical record variance only.
It does not reopen the repaired leakage sheet or create a fresh repair choice
downstream.

This strips unused friendly slack from every budget except the already-
saturated companion ceiling, while leaving the downstream gate
`G_leak(P_n; I) = (L_tot, L_mirror, L_companion, L_feedback, L_cross)`
unchanged.
The hostile Step-4 dossier already earns the classwise failure mode through
mirror, companion, feedback, and cross loads on the same frozen ledger, so
the repaired sheet sharpens separation without inventing a new hostile
coefficient table.

Filed from:
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-005-exploration-001-authorized-repair-sheet.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-007-exploration-002-scorecard-guardrails-and-step-2-readiness.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-003/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-003/code/pro_circuit_dossier_check.py`
