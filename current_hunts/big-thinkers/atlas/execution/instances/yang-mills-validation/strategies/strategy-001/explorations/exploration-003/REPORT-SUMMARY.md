# Exploration 003 Summary: B-square Formula and Convention Verification

## Goal
Verify the corrected B_□ formula and resolve whether E001's finding of H_norm = 1/8 at U_all = iσ₃ is real or an artifact.

## What Was Done
Wrote and ran code comparing both LEFT (corrected) and RIGHT (E001's) B_□ formulas at U=I and U_all = iσ₃. Verified the LEFT formula with finite differences (diagonal AND off-diagonal).

## Outcome: E001's COUNTEREXAMPLE IS WRONG — Conjecture 1 SURVIVES

The LEFT formula (corrected, prior mission's) gives λ_max = 4β at U=iσ₃. Conjecture 1 holds.
The RIGHT formula (E001's) gives λ_max = 6β at U=iσ₃. This is an ARTIFACT of the wrong formula.

Key results:
- LEFT and RIGHT agree at Q=I (both give 4β) — sanity check passes
- LEFT and RIGHT DISAGREE at Q≠I: 4β vs 6β at U=iσ₃
- LEFT formula verified by FD (diagonal and off-diagonal, all < 10⁻⁴ error)
- The eigenvalue equivalence argument (left ↔ right via Ad) fails because the partial holonomies in the formulas change under convention swap

## Verification Scorecard
- [VERIFIED] LEFT B_□ formula matches FD at U=iσ₃ (diagonal + off-diagonal)
- [VERIFIED] λ_max = 4β at Q=I (both formulas)
- [VERIFIED] λ_max = 4β at U=iσ₃ (LEFT formula) — Conjecture 1 survives
- [COMPUTED] 5 random Q: all H_norm < 1/12
- [DISPROVED] E001's claim of CS saturation at U=iσ₃ (used wrong formula)

## Key Takeaway
The B_□ formula with P3 = Q1·Q2·Q3⁻¹ (including backward edge's own link) is correct. The formula without Q3⁻¹ gives wrong eigenvalues at Q ≠ I. E001's finding of H_norm = 1/8 was an artifact. β < 1/6 is confirmed but the CS bound is NOT tight — the actual maximum is 4β = 1/12 at Q=I and flat connections.
