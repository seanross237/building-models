# Exploration 002 Summary

- Goal:
  Tao-screen the frozen `vorticity transport / Biot-Savart form` candidate in
  the fixed localized LEI audit.
- What I tried:
  read the Step-5 freeze, the exact-rewrite obstruction files, the Tao-gate
  calibration notes, and the mission background on the vorticity formulation;
  then asked whether rewriting through `omega` makes the coefficient on
  `I_flux[phi]` smaller before any architecture change.
- Outcome:
  `succeeded`
- One key takeaway:
  inside the frozen LEI architecture, the vorticity/Biot-Savart rewrite is
  only a re-expression of the same quadratic interaction and does not identify
  a Tao-sensitive coefficient gain on `I_flux[phi]`.
- Leads worth pursuing:
  none in this branch; any serious follow-up belongs to a different
  stretching/geometry architecture, not Step 3 here.
- Unexpected findings:
  the route sounds more Navier-Stokes-specific than the first two candidates,
  but the local source record still treats that specialness as representation-
  level only unless the branch drifts.
- Computations worth doing later:
  none before a controller explicitly reopens a vorticity-stretching route.
