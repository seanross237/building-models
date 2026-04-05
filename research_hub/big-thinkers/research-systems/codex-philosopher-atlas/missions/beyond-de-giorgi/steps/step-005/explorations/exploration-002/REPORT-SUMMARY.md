# Exploration 002 Summary

- Goal:
  fix the compatible weak-solution package and one frozen localization
  protocol for the chosen architecture.
- What I tried:
  read the CKN and Vasseur architecture files and the run-003 chain-01
  discipline documents, then translated those constraints into one explicit
  LEI-based package for the exact-rewrite audit.
- Outcome:
  `suitable weak solutions` in the Leray-Hopf energy class with LEI remain the
  correct package, and the frozen protocol is one CKN-style parabolic cutoff on
  one cylinder.
- Key takeaway:
  the first explicit honesty risk is pretending that projection, Lamb-vector,
  or vorticity identities stay exact after localization without paying the
  resulting commutator/CZ/Biot-Savart cost.
- Leads worth pursuing:
  use this exact cutoff/projection ledger when bounding the final `2-3`
  rewrite family.
- Unexpected findings:
  the compatibility issue is less about existence of a suitable solution class
  and more about operator placement after localization.
- Computations worth doing later:
  candidate-by-candidate loss accounting for moving from `I_flux[φ]` to
  projected, Lamb-vector, and vorticity forms.
