# Exploration 003 Summary

- Goal:
  write the unified Step-2 Tao-screen verdict for the three frozen exact
  rewrite candidates in `step-006`, under one fixed localized LEI standard.

- What I tried:
  read `exploration-001/REPORT.md` and `exploration-002/REPORT.md`, then
  calibrated their candidate verdicts against the fixed Step-5 branch setup,
  the Step-6 goal, the controller memo, the earlier far-field negative, the
  geometry-branch kill, and the Vasseur-pressure negatives.

- Outcome:
  `succeeded`

- Branch-level result:
  all three candidates are rejected as `Tao-insufficient`, no candidate is
  admitted to Step 3, and the exact-rewrite branch should be killed now rather
  than continued cosmetically.

- One key takeaway:
  within the frozen `I_flux[phi]` audit, every exact rewrite stays at the
  level of pre-localization packaging and none becomes estimate-level action on
  the localized cutoff-flux coefficient.

- Candidate verdicts:
  - `divergence / stress form`:
    claimed feature is incompressible divergence rewriting of convection;
    Tao-screen status `preserved`; insertion point is only the transport-side
    IBP slot on `I_flux[phi]`; rejection reason is that the same
    stress-against-`∇phi` burden returns.
  - `Lamb-vector / Helmholtz-projected form`:
    claimed feature is exact gradient isolation plus projected Lamb-vector
    structure, with exact Beltrami as anchor; Tao-screen status `weakened`;
    insertion point is only the same cutoff-flux bundle after localization;
    rejection reason is that projection / pressure / CZ / commutator debt
    restores the same burden.
  - `vorticity transport / Biot-Savart form`:
    claimed feature is vorticity-side relocation of the same quadratic
    interaction with Biot-Savart recovery; Tao-screen status `preserved`;
    insertion point is only formal substitution inside the same localized
    estimate; rejection reason is that Biot-Savart reinsertion repays the same
    nonlocal debt.

- Leads worth pursuing:
  - None inside this frozen branch.
  - If controller wants follow-up, it should be treated as a different branch:
    either a pressure-tensor question on the live obstruction, or an openly
    revised geometry/stretching package.

- Unexpected findings:
  - The three candidates fail under one common criterion, not three unrelated
    ones:
    no source-backed coefficient shrinkage on the fixed localized
    `I_flux[phi]` balance.
  - The Lamb-vector and vorticity candidates only look stronger if one quietly
    reopens the killed geometry/stretching route.

- What this step newly tested:
  it did not re-prove the `beta = 4/3` sharpness record, the H^1-pressure
  dead ends, or the geometry branch kill.
  It tested a narrower question those negatives had not yet settled:
  whether the frozen exact-rewrite family itself contains any Tao-sensitive
  insertion point on the localized cutoff-flux bundle.
  The answer is `no`.

- Computations worth doing later:
  none inside scope.
