# Exploration 006 Summary — Adversarial Review and Novelty Search

**Date:** 2026-03-27

## Goal
Attack the 4 SED anharmonic oscillator findings from E001–E004 via: (1) literature search for prior numerical work, (2) methodology flaws, (3) robustness/novelty/significance ratings, (4) key remaining check.

## What was tried
- 12 web searches across PubMed/Google Scholar/arXiv for prior numerical anharmonic SED simulations
- Computed: equilibration adequacy, sample autocorrelation, Euler-Cromer accuracy, UV cutoff harmonic analysis, Langevin validity criterion, LL O(τ²) error estimates
- Rated all 4 findings on robustness, novelty, significance
- Identified the most important remaining check

## Outcome: MIXED — two findings survive attack; two are weaker than claimed

## Key Takeaway

**The most novel and robust finding is F3 (ALD + β^0.40 residual),** not F2 or F4.

**Finding 2 (Langevin O(β) failure)** is a real numerical result but is a demonstration that the Langevin approximation breaks down, not a fundamental SED failure. Finding 2 should be reframed accordingly.

**Finding 4 (linearity boundary)** is conceptually well-known since Boyer (1975) and explicitly stated in Boyer (2019, Atoms 7:29). Not novel as a concept; only the naming and quantification are new.

**Ratings:**

| Finding | Robustness | Novelty | Significance | Verdict |
|---------|-----------|---------|--------------|---------|
| F1 (HO numerical) | 5/5 | 2/5 | 2/5 | Confirmatory |
| F2 (Langevin O(β)) | 4/5 | 3/5 | 3/5 | Real but requires reframing |
| F3 (ALD + β^0.40) | 4/5 | 4/5 | 4/5 | **Main result** |
| F4 (linearity boundary) | 5/5 | 1/5 | 2/5 | Known concept, new label |

## Novelty Search Verdict
No prior time-domain numerical simulations of the anharmonic SED oscillator found. The closest prior work: Moore & Ramírez (1981, Nuovo Cimento B 64:275) analyzed the anharmonic SED oscillator analytically in the τ→0 "zero charge" limit. This does NOT contradict our results (different regime: no radiation reaction = no ZPF noise pumping).

Pesquera & Claverie (1982) is purely analytical (Fokker-Planck perturbation theory), no numerical simulation. The Landau-Lifshitz order reduction applied to SED appears genuinely new.

## Methodology Concerns Found

**Significant (requires action):**
1. **5.4σ claim at β=0.01 is overstated.** The 5.4σ compares absolute SED value to QM target, not controlling for the β=0 offset. Correctly adjusted, the O(β) trend significance at β=0.01 is ~2.5σ. Large-β results (23–50σ) are unaffected.

**Medium (explain, don't fix):**
2. **UV cutoff as source of β^0.40.** At β≈1, the 5th harmonic of the anharmonic oscillator (at 10.77 rad/s) exceeds ω_max=10. This explains the sub-O(β²) residual as a numerical artifact. E005 must confirm this.

**Cleared:**
3. Equilibration: 100–464 relaxation times — adequate.
4. Sample autocorrelation: oscillatory C(t) makes samples near-independent; std_var values correct.
5. LL O(τ²) errors: negligible (10⁻⁴ vs 0.030 signal).
6. Euler-Cromer: O(dt²) = 0.25% equilibrium error, negligible.

## Recommended Most Important Remaining Check
**Run ω_max scan (10, 20, 50) at β=1.** This is E005's program. The result determines:
- **UV artifact confirmed (Δe→0 with increasing ω_max):** ALD agrees with P&C (1982); main finding is that Langevin approximation fails but full ALD approximately works. Moderate positive result for SED.
- **β^0.40 persists (Δe constant with ω_max):** P&C (1982) is wrong. SED fails as β^0.40 intrinsically, not β². This would be the most significant finding of the mission.

## Unexpected Findings
- **Moore & Ramirez (1981):** An earlier paper claims "qualitative agreement" for the SED anharmonic oscillator in the zero-charge limit. This paper is NOT in our current library. It should be added and the distinction from our simulation regime (τ=0.01 vs. τ→0) should be explicitly noted.
- **5.4σ correction:** The significance at β=0.01 was overstated due to a subtle difference between "significance vs. QM" and "significance of the trend." This only matters for the lowest-β point.
- **No prior numerical work exists** for this system despite a 44-year-old analytical prediction (P-C 1982). The numerical confirmation gap is larger than expected.

## Computations Identified
- **ω_max sweep** (already in E005): necessary for interpreting β^0.40. Scripts exist; run ω_max=10, 20, 50 at β=1. Low difficulty, critical result.
- **τ-scan** (already in E005): τ=0.01 → 0.001 at β=1, ω_max=10. Tests P-C's τ→0 regime.
- **Moore & Ramirez check**: Reproduce the τ→0 "zero charge" limit calculation for var_x at β=0.01 to confirm/refute their "qualitative agreement" claim. ~20-line analytical calculation.
