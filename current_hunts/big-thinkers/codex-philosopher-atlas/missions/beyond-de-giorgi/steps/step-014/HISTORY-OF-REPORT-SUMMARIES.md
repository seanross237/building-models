# History of Report Summaries

Exploration summaries will be appended here as they land.

## Exploration 001

- [VERIFIED] The repository-native exact-rewrite shortlist for this branch is
  already bounded to three families:
  `divergence / stress`,
  `Lamb-vector / projected`,
  `vorticity / Biot-Savart`.
- [INFERRED] Frozen active candidates for Step 2:
  `Lamb-vector / Helmholtz-projected form` and
  `vorticity transport / Biot-Savart form`.
- [INFERRED] Frozen reserve:
  `divergence / stress form`.
- [INFERRED] Reason for the active pair:
  they are the only exact-rewrite-native families on disk with a nontrivial
  claimed theorem-facing delta and a named route, however fragile, back to the
  frozen `I_flux[phi]` burden.
- [INFERRED] Reason divergence stays reserve:
  it is admissible but appears to localize immediately back to the same
  stress-against-`∇phi` burden with no sharper candidate-specific leverage.
- [VERIFIED] Strain / pressure-Hessian language was not promoted because it
  belongs to older pressure-branch or geometry-adjacent materials rather than
  the frozen exact-rewrite shortlist for this branch.

## Exploration 002

- [INFERRED] `Lamb-vector / projected` exact packet:
  `∂_t u - Δu - u × ω + ∇(p + |u|^2/2) = 0`,
  or projected `∂_t u - Δu - P(u × ω) = 0`.
- [INFERRED] Localized Lamb conclusion:
  the pointwise cancellation `u · (u × ω) = 0` does not shrink the frozen LEI
  burden because localization immediately restores the same flux term through
  `p + |u|^2/2`.
- [INFERRED] `vorticity / Biot-Savart` exact packet:
  `∂_t ω - Δω + (u · ∇)ω - (ω · ∇)u = 0`,
  with `u = BS[ω]`.
- [INFERRED] Localized vorticity conclusion:
  the native vorticity equation touches the frozen theorem-facing burden only
  after full Biot-Savart and pressure reconstruction inside the same
  `I_flux[phi]` bundle.
- [INFERRED] Visible debts now explicit:
  pressure re-entry,
  cutoff commutators,
  vector reconstruction,
  admissibility,
  and locality loss.
- [INFERRED] Equation-level shared result:
  both active candidates return to the same localized LEI ledger once their own
  nonlocal and commutator debts are charged.

## Exploration 003

- [INFERRED] `Lamb-vector / projected` exchange memo:
  any live gain would need a transfer lemma from Lamb-vector or Beltrami-deficit
  control to a smaller full `I_flux[phi]` coefficient after pressure,
  projection, and cutoff debt.
  No such lemma appears on the repository record.
- [INFERRED] `vorticity / Biot-Savart` exchange memo:
  any live gain would need a localized estimate showing that Biot-Savart-based
  substitution inside the same LEI bundle still leaves positive-margin
  coefficient shrinkage after full reconstruction debt.
  No such lemma appears on the repository record.
- [VERIFIED] Visible losses are already active before promotion for both
  candidates:
  pressure re-entry or pressure reconstruction,
  nonlocal operator debt,
  cutoff commutators,
  admissibility,
  and locality loss.
- [INFERRED] Nearest prior-art comparators are already on the repository record
  for both active candidates, and the current Step-2 packets add no new
  theorem-facing mathematical delta beyond those same exact identities.
- [VERDICT]
  `exchange-failure obstruction, branch should stop before anti-repackaging gate`
