# Exploration 001 Summary: Off-Diagonal Form Factor and Predicted Δ₃

## Goal
Compute the off-diagonal form factor correction from Berry-Keating (1999), predict Δ₃_sat, and compare to the measured 0.155.

## Outcome: PARTIAL SUCCESS

The off-diagonal correction formula was extracted and implemented, producing a **specific number**: the Hardy-Littlewood R²_c correction reduces Δ₃(20) from 0.211 to 0.210, closing **1.6% of the gap** between GUE and zeta zeros. However, the perturbative approach breaks down at T=1682 for the dominant diagonal correction.

## Key Results

1. **GUE ground truth [VERIFIED]:** Δ₃_GUE(N=500) = 0.217 ± 0.002 at L=20 (20 matrix trials)
2. **Off-diagonal effect [COMPUTED]:** R²_c reduces Δ₃(20) by 0.001 (1.6% of gap). Correct direction but far too small alone.
3. **Diagonal correction [COMPUTED]:** R¹_c blows up at T=1682 — the perturbative expansion in 1/(π⟨d⟩)² requires ⟨d⟩ >> 1, but ⟨d⟩ = 0.89 at T=1682.
4. **Berry's formula [COMPUTED]:** (1/π²)log(log(T/(2π))) = 0.174 at T=1682 (12% high), = 0.154 at T=600 (0.6% match!).
5. **Correct Δ₃ formula [VERIFIED]:** Σ₂ → Δ₃ via kernel (L³−2L²r+r³), confirmed to 3% vs matrices.

## Verification Scorecard
- **[VERIFIED]**: 2 (GUE Δ₃, formula route)
- **[COMPUTED]**: 6 (R²_c, R¹_c, Berry predictions, Σ₂, gap closure, height dependence)
- **[CONJECTURED]**: 1 (perturbative breakdown threshold)

## Key Takeaway

**The 40% gap cannot be closed perturbatively at T ≈ 1682.** The Berry-Keating corrections are asymptotic expansions in 1/⟨d⟩², where ⟨d⟩ = 0.89 at T=1682 — far from the ⟨d⟩ >> 1 regime needed. The off-diagonal (Hardy-Littlewood) correction is real but contributes only 1.6%. The dominant diagonal correction (98%+) requires non-perturbative methods.

Berry's closed-form saturation formula already captures the full effect and predicts 0.154 at T=600 (0.6% match), making it the best available predictor.

## Leads Worth Pursuing

1. **Non-perturbative K(τ) from explicit prime sums:** Instead of the perturbative R_c corrections, compute K(τ) directly from the prime orbit sum (eq 4.18) and evaluate Σ₂ → Δ₃. This would be non-perturbative and valid at any T.
2. **Verify at high T:** Use zeros at T ~ 10^{12} (Odlyzko data) where ⟨d⟩ ≈ 3.9 and the perturbative expansion should work.
3. **Effective T investigation:** Why does Berry's formula match at T≈600 rather than T≈1682? The "effective T" for the pair correlation may differ from the height of the zeros.

## Proof Gaps
- The correct R₂ → Δ₃ kernel remains uncertain (the (L-r)²(2Lr-r²) kernel gives wrong results; only the Σ₂ → Δ₃ route was verified).
- No Lean formalization attempted (task was computational).

## Unexpected Findings
- **The perturbative regime threshold is VERY high:** ⟨d⟩ >> 1 requires T >> 10^{10}, far beyond the T ≈ 1682 used in prior explorations.
- **Berry's formula accuracy at T=600:** The prediction 0.154 matches 0.155 to 0.6%, suggesting T=600 might be the "natural" scale for the ~1000th zero statistics.
