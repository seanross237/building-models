# Exploration 001 Goal - Lock The Authorized Step-5 Repair Sheet

## Objective

Using the fixed Step-4 dossier, determine the only honest threshold repairs for:

- `Template-Defect Near-Closure`
- `Windowed Spectator-Leakage Budget`

This exploration must treat
`missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/RESULTS.md`
as the controlling Step-4 record.
It may tighten thresholds only from quantities already recorded there and in
the landed Step-4 explorer artifacts.

## Required Output

Produce a report that does all of the following:

1. States the inherited Step-4 status for both candidates.
2. Extracts the exact friendly-side maxima already recorded for:
   `Delta_tmpl`,
   `Delta_spec`,
   `L_tot`,
   `L_mirror`,
   `L_companion`,
   `L_feedback`,
   and
   `L_cross`.
3. States the exact old threshold values and the exact repaired values.
4. Justifies each repair directly from the Step-4 anti/pro margins or gaps
   already on the record, without inventing new packet data.
5. States explicitly when an individual budget cannot tighten further because
   the worst recorded friendly witness already saturates it.
6. Restates the downstream gate for each repaired candidate and explains why
   the repaired gate is still non-cosmetic on the frozen packet sheet.

## Success Criteria

- Every threshold change is a one-way tightening supported by the Step-4
  dossier.
- No repair changes packet semantics, spectator classes, interaction currency,
  sign sheet, phase gauge, or the finite window.
- The report clearly separates
  `[VERIFIED]`
  inherited numbers from
  `[INFERRED]`
  repair choices.

## Failure Criteria

- The exploration fails if it invents a new anti-family coefficient table or
  new packet family.
- It fails if it rescues a candidate by moving the window or by redefining the
  defect or leakage observables.
- It fails if it treats an already-saturated friendly witness as if it left
  extra slack.

## Key Local Context

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/REASONING.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-003/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-003/code/pro_circuit_dossier_check.py`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-002-exploration-002-interaction-templates-and-gates.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-003-exploration-002-robustness-audit-and-step-4-readiness.md`
- `library/meta/exploration-goal-design/fix-the-class-partition-and-finite-window-normalization-before-writing-hard-admissibility-sheets.md`
- `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`

## Constraints

- Do not reopen Step 4.
- Do not add new witnesses.
- If one intermediate Step-4 subreport is narrower than the final Step-4
  results, use the final Step-4 result as the controlling branch verdict and
  explain the provenance carefully.
