# Exploration 001 Summary

## Goal

Freeze the single carried witness `F_SS(1/12)` on the canonical one-bridge
role-labeled helical packet ledger, identify the controlling repaired Step-6
authority sheets for `G_tmpl` and `G_leak`, log the earlier `L_cross` drift
as historical variance only, and state the same-currency rule later steps must
inherit.

## What I Tried

- Read the Step-6 step-level handoff first, then the Step-5 repair record, the
  Step-4 witness dossier, and the Step-2 packet-sheet freeze.
- Compared step-level outputs against exploration-level reports to isolate
  whether any threshold remained live, especially on `L_cross`.
- Reconstructed the exact object called `F_SS(1/12)` from the frozen packet,
  gauge, sign/phase, normalization, and window conventions already on disk.

## Outcome

`succeeded`

## One Key Takeaway

The branch now has one unambiguous Step-1 freeze:
`F_SS(1/12)` is the `mu = 1/12` endpoint of the engineered-sign sparse-triad
family on the canonical one-bridge packet sheet, and the controlling scorecard
is the Step-6 repaired pair
`G_tmpl = (1/4, 49/256)` and
`G_leak = (1/4, 1/12, 1/12, 1/16, 1/24)`,
with `L_cross <= 1/24` fixed by the later branch record rather than left as a
live choice.

## Leads Worth Pursuing

- Chain Step 2 can now derive the exact closure ledger for `F_SS(1/12)` on the
  same frozen packet sheet.
- Any later claim that tries to turn `G_tmpl` evidence into `G_leak` evidence,
  or vice versa, needs an explicit same-currency transfer statement first.

## Unexpected Findings

- The `L_cross` mismatch is concrete, not vague:
  `steps/step-005/explorations/exploration-001/REPORT.md` keeps
  `Lambda_cross = 1/12`,
  while later step-level outputs freeze
  `L_cross <= 1/24`.
- Step 6 does not collapse the scorecard:
  repaired `G_tmpl` and repaired `G_leak` remain two distinct promoted objects,
  not one conjunction or dominance relation.

## Computations Worth Doing Later

- Compute the exact closure-forced mode ledger for `F_SS(1/12)` with mandatory
  conjugates and any closure-forced companions on the same ledger.
- If closure is finite, evaluate exact dynamics on `I = [0, 1]` against the
  frozen `G_tmpl` and `G_leak` gates only, keeping itinerary times as
  diagnostics rather than pass/fail criteria.
