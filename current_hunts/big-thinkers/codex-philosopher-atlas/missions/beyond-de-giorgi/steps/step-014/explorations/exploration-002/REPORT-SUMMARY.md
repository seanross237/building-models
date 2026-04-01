# Exploration 002 Summary

- Goal:
  for the two active Step-2 candidates, derive the exact full evolution, the
  localized packet that actually interfaces with the frozen LEI burden
  `I_flux[phi] = ∬ (|u|^2 + 2p) u . ∇phi`, and the visible debt ledger.

- What I tried:
  read the step-013 freeze record and the step-014 candidate slate; reused the
  fixed localization/debt rules from the local audit files; derived the Lamb /
  projected and vorticity / Biot-Savart equations directly from Navier-Stokes;
  then forced each candidate back through the same localized LEI packet instead
  of letting it drift to stretching, geometry, or another surrogate target.

- Outcome:
  `succeeded`

- One key takeaway:
  both active candidates are exact at the PDE level, but neither stays cleaner
  than the frozen LEI flux bundle after localization:
  the Lamb route immediately pays exact pressure/projection re-entry, while the
  vorticity route reaches the target only after full Biot-Savart and pressure
  reconstruction.

- Leads worth pursuing:
  write the next-step insertion test in the same ledger currency;
  for the Lamb route, check whether any positive-margin coefficient change can
  survive the exact commutator identity
  `- ∬ ∇Δ^{-1}(u . ∇phi) . (u x omega) = ∬ pi u . ∇phi`;
  for the vorticity route, test whether any decomposition of
  `phi BS[omega] = BS[phi omega] + [phi, BS]omega` can do better than pure
  repayment once the full pressure term is included.

- Unexpected findings:
  the Lamb candidate's candidate-specific nonlinear term disappears completely
  in the local-energy pairing, so the only surviving full-burden packet is the
  restored Bernoulli-pressure flux;
  the vorticity candidate's native localized PDE is not even the right object
  for this branch, because the frozen target remains a velocity-pressure flux.

- Computations worth doing later:
  make the Lamb commutator-to-pressure identity into an explicit coefficient
  comparison inside the frozen LEI inequality;
  expand the exact Biot-Savart and Riesz commutator terms under the fixed CKN
  cutoff to see whether any cancellation survives on the same full
  `I_flux[phi]` bundle;
  audit whether the pressure gauge/local harmonic remainder changes any local
  reconstruction bookkeeping under the suitable-weak solution floor.
