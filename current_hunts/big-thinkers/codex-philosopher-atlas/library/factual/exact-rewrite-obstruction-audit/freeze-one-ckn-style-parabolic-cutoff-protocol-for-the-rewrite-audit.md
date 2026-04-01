# Freeze One CKN-Style Parabolic Cutoff Protocol For The Rewrite Audit

Status: `INFERRED` with `VERIFIED` CKN support

The fixed localization protocol for this branch is one CKN-style parabolic
cylinder with one standard smooth cutoff, shared by every candidate rewrite.

The concrete protocol is:

- region:
  `Q_r(x_*, t_*) = B_r(x_*) x (t_* - r^2, t_*)`
- cutoff:
  one `phi ∈ C_c^∞(Q_r)` with `0 ≤ phi ≤ 1`, `phi ≡ 1` on the inner
  half-cylinder, `|∇phi| ≤ C/r`, and `|∂_t phi| + |Δphi| ≤ C/r^2`
- target estimate:
  the localized LEI balance with fixed bad term
  `I_flux[phi] = ∬ (|u|^2 + 2p) u . ∇phi`
- bookkeeping rule:
  every candidate starts from the same `I_flux[phi]` target and pays all
  localization costs in that same package
- projection and CZ rule:
  if a candidate uses Helmholtz projection or pressure reconstruction after
  localization, its nonlocal and commutator costs are charged to that
  candidate
- vorticity and Biot-Savart rule:
  if a candidate rewrites through `omega`, all Biot-Savart reinsertions and
  cutoff-commutation costs are charged in the same ledger

This is the fairest protocol because it is the least adapted package that
keeps the chosen local-energy architecture visible while preventing candidates
from changing the region, operator placement, or cutoff discipline mid-audit.

Filed from:
- `missions/beyond-de-giorgi/library-inbox/step-005-exploration-002-compatibility-localization-protocol.md`
