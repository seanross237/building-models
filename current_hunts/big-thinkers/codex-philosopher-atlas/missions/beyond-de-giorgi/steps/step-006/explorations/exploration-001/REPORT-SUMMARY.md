# Exploration 001 Summary

- Goal:
  Tao-screen `divergence / stress form` and
  `Lamb-vector / Helmholtz-projected form` against the fixed localized LEI
  audit.
- What I tried:
  read the Step-5 freeze, the exact-rewrite audit files, the Tao-gate
  calibration notes, and the mission/controller framing; then forced both
  candidates to answer the same mechanical question:
  what coefficient on `I_flux[phi]` gets smaller?
- Outcome:
  `succeeded`
- Candidate outcomes:
  - `divergence / stress form`:
    Tao verdict `preserves`;
    classification `reject as Tao-insufficient`.
  - `Lamb-vector / Helmholtz-projected form`:
    Tao verdict `weakens`;
    classification `reject as Tao-insufficient`.
- One key takeaway:
  both candidates keep an exact algebraic identity, but neither names a
  smaller effective coefficient on the fixed cutoff-flux balance after
  localization debt is restored.
- Leads worth pursuing:
  let the separate vorticity exploration decide whether the third frozen
  candidate contributes anything genuinely different; for these two candidates,
  any rescue would have to change the architecture or reopen geometry.
- Unexpected findings:
  the sharper distinction is not "does Tao destroy the identity?" but "does
  the identity survive as an estimate lever after the cutoff is inserted?"
- Computations worth doing later:
  none before Step 3, because no credible insertion point survived.
