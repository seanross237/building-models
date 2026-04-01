# Exploration 001 Goal — Exact Far-Field Pressure Obstruction Reconstruction

## Objective

Reconstruct the exact surviving far-field pressure pairing for the `beyond-de-giorgi` step from the copied `vasseur-pressure` and related NS architecture materials, then state precisely:

- the exact live formula for `I_p^far`
- which pressure pieces or harmonic modes are already annihilated by the localization/test structure
- what the actual bad coefficient is
- what quantity would need to become smaller for there to be real progress

## Success Criteria

- Produce an explicit formula sheet, not a summary-level paraphrase.
- Distinguish the full pairing from the dominant live term.
- Mark claims as `[VERIFIED]` when directly supported by source files and `[INFERRED]` when they are structural deductions from those files.
- Name exact source files used.
- Make clear why cosmetic control of killed modes does not count as progress.

## Failure Criteria

- Leaves the key formula implicit.
- Confuses local pressure with the far-field obstruction.
- Claims a gain without tying it to the coefficient `C_far ~ ||u||_{L^2}^2 / r_k^3` or an equivalent coefficient-side quantity.

## Required Source Anchors

- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/vasseur-pressure/library-inbox/exploration-002-pressure-dissection-de-giorgi.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/vasseur-pressure/steps/step-001/RESULTS.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/vasseur-pressure/steps/step-002/RESULTS.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/navier-stokes/library-inbox/vasseur-2007-proof-architecture.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/planning-runs/run-001/attacks/chain-01.md`

## Constraints

- Do not rerun general De Giorgi background.
- Do not claim that harmonic smoothness alone improves the obstruction.
- Separate:
  - modes already killed by `div(v_k φ_k^2 ê)`
  - the surviving affine-or-higher harmonic content that still couples to `∇φ_k`
  - the true operative coefficient.

## Deliverables

Write:

1. `REPORT.md` with the reconstruction and source-based reasoning.
2. `REPORT-SUMMARY.md` with:
   - goal
   - what was checked
   - outcome
   - one key takeaway
   - any live target quantity for Step 2, if one survives
