# Template-Defect Near-Closure Honest Step-5 Repair Tightens Thresholds To The Recorded Friendly Maxima

Status: `VERIFIED` Step-4 friendly maxima with `INFERRED` repair sheet

On the frozen Step-4 ledger, the largest recorded friendly values for
`Template-Defect Near-Closure` come from `F_SL(1/16)`:
`Delta_tmpl = 1/4`
and
`Delta_spec = 49/256`.

The inherited Step-4 sheet used
`lambda_tmpl = 1/3`
and
`lambda_spec = 1/4`,
so the unused friendly slack on the recorded ledger was exactly
`1/12`
for template defect and
`15/256`
for spectator defect.

The honest Step-5 repair is therefore:
`lambda_tmpl: 1/3 -> 1/4`
and
`lambda_spec: 1/4 -> 49/256`.

This repair preserves both recorded friendly witnesses, leaves the downstream
gate
`G_tmpl(P_n; I) = (Delta_tmpl, Delta_spec)`
unchanged, and does not alter the hostile failure mechanism already recorded
for `F_DT(delta, eta)`.
It removes bookkeeping slack from the admissibility sheet without changing the
packet object, the window, the spectator classes, or the exact observable.

Filed from:
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-005-exploration-001-authorized-repair-sheet.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-003/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-003/code/pro_circuit_dossier_check.py`
