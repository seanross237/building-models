# Exploration 003 Goal

## Objective

After `exploration-001` and `exploration-002` are complete, write the unified
Step-2 verdict for `step-006`.

This synthesis must:

- compare all three frozen candidates under one Tao-screen standard,
- decide whether any candidate is admitted to Step 3,
- write the branch-level continue-or-kill recommendation,
- and calibrate the result against the De Giorgi sharpness record, the
  pressure-route negatives, and the killed geometry branch.

## Required Inputs

Read these before writing the verdict:

- `missions/beyond-de-giorgi/steps/step-006/explorations/exploration-001/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-006/explorations/exploration-002/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-006/GOAL.md`
- `missions/beyond-de-giorgi/steps/step-005/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-001/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-002/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-004/RESULTS.md`
- `missions/vasseur-pressure/steps/step-001/RESULTS.md`
- `missions/vasseur-pressure/steps/step-002/RESULTS.md`
- `missions/beyond-de-giorgi/MISSION.md`
- `missions/beyond-de-giorgi/controller/decisions/decision-008.md`

## Required Questions

1. For each of the three candidates, what is the exact claimed NS-specific
   feature, and is it `destroyed`, `weakened`, or `preserved` by Tao-style
   averaging?
2. For each candidate, where does the claimed distinction enter the fixed
   localized balance on `I_flux[φ]`, if anywhere?
3. What is the admission/rejection classification for each candidate?
4. Does the branch remain alive after the Tao screen?
5. If at least one candidate survives, what exact one-sentence Step-3 estimate
   question should be tested for that survivor?
6. If none survive, why should the branch stop now rather than drift into a
   cosmetic Step 3?
7. What does this step newly test that the prior De Giorgi, pressure, and
   geometry negatives did not already settle?

## Success Criteria

- One unified candidate table with consistent standards.
- One branch verdict with no ambiguity about continue vs kill.
- One prior-art calibration note that keeps the claim narrow and non-duplicated.

## Failure Criteria

- The verdict depends on a new candidate, new architecture, or new hypothesis
  not fixed in `step-005`.
- The memo relies on rhetoric such as "promising rewrite" without identifying
  a localized insertion point on `I_flux[φ]`.

If failure occurs, say so directly and recommend branch invalidation.

## Output Requirements

Write:

- `REPORT.md`
- `REPORT-SUMMARY.md`

Use source-based labels such as `[VERIFIED]`, `[INFERRED]`, and `[PROPOSED]`.
Keep the verdict bounded to the tested family and fixed protocol.
