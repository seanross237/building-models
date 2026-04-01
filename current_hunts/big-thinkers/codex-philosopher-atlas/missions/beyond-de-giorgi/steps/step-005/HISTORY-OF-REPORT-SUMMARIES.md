# History of Report Summaries

Exploration summaries will be appended here as they land.

## Exploration 001: Architecture And Bad-Term Screening

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

## Exploration 002: Compatibility And Localization Protocol

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

## Exploration 003: Gain Currency And Candidate Family

- Goal:
  choose one gain currency, freeze the exact-rewrite family, and decide whether
  the branch is concrete enough for the Tao screen.
- What I tried:
  inherited the architecture and protocol from Explorations 001 and 002, then
  used the run-003 chain-01 materials plus the mission background to freeze a
  bounded `2-3` item rewrite family.
- Outcome:
  the gain currency is `coefficient shrinkage in the fixed localized LEI
  balance`, and the candidate family is:
  divergence/stress form, Lamb-vector/projected form, and vorticity
  transport/Biot-Savart form.
- Key takeaway:
  the branch is ready for Step 2 precisely because it is now narrow: one bad
  term, one protocol, one gain currency, three exact rewrites, and no hybrid
  escape hatch at this stage.
