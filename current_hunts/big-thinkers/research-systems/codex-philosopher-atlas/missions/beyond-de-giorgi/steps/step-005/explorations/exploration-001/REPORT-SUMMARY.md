# Exploration 001 Summary

- Goal:
  choose one inherited architecture and one named bad term for the exact
  reformulation audit.
- What I tried:
  compared `De Giorgi truncation`, `local-energy flux/localization`, and
  `vorticity stretching localization` against the already-earned pressure and
  geometry negatives and against the run-003 chain materials.
- Outcome:
  `local-energy flux/localization` wins.
- Key takeaway:
  the right fixed target is the localized LEI cutoff-flux bundle
  `I_flux[φ] = ∬ (|u|^2 + 2p) u · ∇φ`, not the already-killed far-field
  pressure coefficient and not the full-stretching geometry target.
- Leads worth pursuing:
  freeze the weak-solution package and the cutoff/projection bookkeeping around
  this exact term before choosing the rewrite family.
- Unexpected findings:
  the strongest reason to reject De Giorgi here is not lack of documentation
  but overdocumentation: the relevant pressure-side negatives are already too
  settled to make it the fairest architecture for this branch.
- Computations worth doing later:
  candidate-by-candidate loss ledger on `I_flux[φ]` under one frozen protocol.
