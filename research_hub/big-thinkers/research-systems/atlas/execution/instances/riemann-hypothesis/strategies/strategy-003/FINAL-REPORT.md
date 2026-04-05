# Strategy-003 Final Report: Spectral Rigidity and Li Criterion Investigation

**Date:** 2026-03-28
**Explorations:** 9 (budget: 10)
**Session prefix:** rh3
**Mission:** Riemann Hypothesis — spectral statistics gap investigation

---

## Executive Summary

Strategy-003 pursued two main lines: (1) confirming the super-rigidity gap explanation via Berry's prime orbit formula, and (2) investigating whether Li criterion coefficients provide a novel cross-community observable connecting number theory to random matrix theory.

**Main result:** No novel publishable claims survive from this strategy. The central super-rigidity gap (Δ₃_sat=0.155 vs GUE 0.294) is confirmed computationally and explained analytically by Berry's 1985 formula — this is established prior art. The candidate novel claim (λ_n^zeta < λ_n^GUE crossover) was identified as promising in E002/E007 but definitively refuted in E008/E009 as a truncation artifact of the linear GUE scaling method.

---

## What We Accomplished

### Phase 1: Off-Diagonal Form Factor and Li Criterion (E001-E002)

**E001** extracted the Berry-Keating off-diagonal form factor and computed its contribution to Δ₃. Result: R²_c closes only 1.6% of the gap (0.211 → 0.210, target 0.155). The perturbative expansion requires T >> 10^{10} to be valid — completely outside the range of the first 2000 zeros. This rules out the perturbative approach for explaining the gap.

**E002** computed Li coefficients λ_n for n=1-500 using 2000 zeta zeros. All 500 coefficients strictly positive (consistent with RH). Key structural insight: |1-1/ρ| = 1 exactly for all critical-line zeros, so λ_n converges by phase cancellation, not amplitude decay. The comparison to GUE Li coefficients showed λ_n^zeta/λ_n^GUE < 1 for n > 272 (ratio 0.949 at n=500, 17.8σ below 1 with N=K=2000).

### Phase 2: Non-Perturbative Approach and Universality Test (E003-E004)

**E003** computed K(τ) non-perturbatively and confirmed Δ₃_sat = 0.1545 directly via sliding-window least-squares on 2000 unfolded zeros (0.3% match to Berry's prediction of 0.155). The saturation plateau is extremely flat (<1% variation from L=15 to L=30). GUE is 47% less rigid at the same scale.

**E004** tested whether the Gauss sum matrix peak Brody parameter has a universal scaling N²/p ≈ 275. Result: REJECTED. Peak β_max decreases monotonically with N (1.318 → 1.154 → 1.019), and peak N²/p varies 1.5× across matrix sizes. This eliminates the Gauss sum matrix as a candidate for explaining or reproducing zeta zero statistics.

### Phase 3: Prime Orbit K(τ), Adversarial Review, and Li Coefficient Validation (E005-E009)

**E005** computed the rigidity hierarchy for various matrix ensembles (C1, Gauss, GUE) and established: Zeta(0.155) < C1(0.285) < Gauss-best(0.415) < GUE(0.581). The key finding: Δ₃ and the level-spacing parameter β decouple — matrices with similar β can have 1.46× different Δ₃ values.

**E006** computed K(τ) from Berry's diagonal approximation and found: Berry's direct formula (1/π²)log(log(T/2π)) gives 0.154 at T=600 (0.6% accuracy). The integral route K(τ) → Σ₂ → Δ₃ has a ~2× normalization error (Fourier convention mismatch, not yet fixed). The diagonal approximation K_primes ≈ 0.94τ for τ < 1 is too close to GUE (K_GUE = τ) to differentiate them; the super-rigidity comes from the saturation plateau (τ > 1 region) which Berry's formula captures analytically.

**E007** (adversarial literature search) confirmed: NO prior paper compares λ_n^zeta to λ_n^GUE (Li 1997, Keiper 1992, Bombieri-Lagarias 1999, Coffey 2004, Schumayer-Hutchinson 2011 all checked). The crossover was rated NOVEL (4/5). Berry formula accuracy table = likely artifact of sparse sampling at high T.

**E008** validated E002's Li coefficient computation with 5,000 zeros and 100 GUE realizations. Confirmed: at K=N=2000, ratio = 0.949 (7.3σ below 1, 100 realizations). BUT discovered: going to K=4500 zeros vs fixed N=2000 GUE gives ratio > 1. The comparison is only valid when K=N. Corrected a GOAL.md error (λ_100^zeta = 114.18, not 59.72). **Truncation sensitivity identified.**

**E009** (decisive test) computed the matched ratio at K=N=500, 1000, 2000, 3000, 5000:

| K=N | λ_500^zeta | λ_500^GUE | Ratio | Significance |
|-----|-----------|-----------|-------|--------------|
| 500 | 707.36 | 796.24±3.99 | 0.888 | -22.3σ |
| 1000 | 812.56 | 904.72±5.47 | 0.898 | -16.9σ |
| 2000 | 881.43 | 925.62±6.09 | 0.952 | -7.3σ |
| 3000 | 909.39 | 906.08±6.39 | 1.004 | +0.5σ (≈1.0) |
| 5000 | 935.20 | 858.19±7.92 | 1.090 | +9.7σ |

**The ratio is monotonically increasing and crosses 1.0 between K=N=2000 and K=N=3000.** At K=N=5000, the ratio is 1.090 — zeta EXCEEDS GUE by 9%. The crossover point at n≈272 (seen at K=N=2000) disappears entirely at K=N ≥ 3000. **Novel claim REFUTED.**

Root cause: Linear scaling of N GUE eigenvalues (semicircle distribution) to [t_1, t_K] creates density mismatch. As K grows, GUE eigenvalues spread to large t values where each contributes negligibly to λ_n. Meanwhile, zeta zeros have logarithmically growing density and the sum converges to a finite limit. This structural asymmetry makes the ratio K-dependent by construction.

---

## Novel Claims Assessment

### NONE survived

**Claim 1 (Flat saturation plateau):** NOT NOVEL — Berry (1985, Proc. R. Soc. A 400:229) predicted both the saturation and the level. Odlyzko (1987) confirmed numerically. Our computation is methodologically clean but adds only precision.

**Claim 2 (Li coefficient crossover):** REFUTED — Truncation artifact of linear GUE scaling (E009). Valid only at K=N=2000; reverses at K=N=3000 and exceeds 1.09 at K=N=5000. No novel publishable content.

**Claim 3 (Berry formula accuracy table):** ARTIFACT — Growing discrepancy at high T explained by sparse sampling (fewer zeros in high-T bins). Not novel.

**Claim 4 (K_primes normalization):** WEAK — Berry (1985) is prior source. Useful technical clarification.

**Claim 5 (C1/Gauss rigidity hierarchy):** POTENTIALLY NEW but not well-motivated as a scientific finding. C1 matrix with independent U(1) phases produces stronger long-range rigidity than Gauss sum matrices with correlated arithmetic phases — this decoupling of Δ₃ and β is computationally established but lacks theoretical explanation or connection to a broader question.

**Interesting mathematical observation (not novel claim):** GUE Li coefficient λ_n(N=K) for the matched comparison is non-monotone in K, peaking around K≈2000 before decreasing. This reflects the competition between adding eigenvalues and spreading them over a wider range. While interesting, this follows directly from the properties of the Li coefficient formula and is not a deep finding.

---

## What Stands and Is Well-Established (Prior Art)

All of the following are confirmed computationally but are known results:

1. **Δ₃_sat(zeta) = 0.1545** — matches Berry's formula (1/π²)log(log(T/2π)) = 0.154 at T=600 to 0.3%
2. **47% super-rigidity gap** vs GUE analytic prediction
3. **Explanation**: Prime orbit structure saturates K(τ) at τ > 1 — Berry (1985) explains this analytically
4. **Berry formula accuracy**: 0.6% at T=600, degrades at higher T (sparse-sampling artifact)
5. **All 500 Li coefficients positive** — consistent with RH, as expected
6. **Phase cancellation mechanism**: |1-1/ρ| = 1 exactly for critical-line zeros — convergence by phase, not amplitude

---

## Recommendations for Next Strategy

### Priority 1: Fix the Li Coefficient Comparison

The Li-vs-GUE comparison is a genuinely novel methodological idea that was never done before (E007). But the implementation was flawed. The correct approach:

- **Unfold both spectra to unit mean spacing** before computing Li coefficients
- For zeta: use the standard unfolded coordinates ξ_k = N(t_k)/N where N(t) is the zero-counting function
- For GUE: use the empirical CDF of eigenvalues
- With both in unit-spacing coordinates, the comparison is scale-invariant and K-independent

This would revive the comparison on a solid foundation. The question "do zeta Li coefficients differ from GUE Li coefficients at unit spacing?" is still unanswered and could yield a genuine signal.

### Priority 2: Fix the K→Σ₂ Normalization

E006 identified a ~2× normalization error in the K(τ) → Σ₂ → Δ₃ integral chain. The COMPUTATIONS-FOR-LATER.md has this as item 19. Fixing this would:
- Validate the prime orbit sum → Δ₃ prediction path
- Test whether the diagonal approximation is sufficient or off-diagonal (Sieber-Richter) pairs are needed

### Priority 3: Off-Diagonal Orbit Pairs (Sieber-Richter)

The theoretical explanation for why K(τ) = 1 for τ > 1 (the saturation that Berry's formula captures) involves off-diagonal orbit pairs (Sieber 2001, Müller et al. 2004). This has never been explored computationally in this mission. Computing the off-diagonal K(τ) contribution and verifying it predicts Δ₃_sat = 0.155 would be a first-principles numerical confirmation of the theory. See COMPUTATIONS-FOR-LATER.md item 19.

### Priority 4: High-T Zeros

Using Odlyzko's precomputed zeros at T ~ 10^6-10^9 would:
- Give a cleaner Berry formula comparison (formula should be more accurate at large T)
- Enable direct test of whether GUE agreement improves at large T
- Potentially reveal whether the super-rigidity gap persists or narrows

---

## Operational Lessons

1. **Math Explorer context pressure at 33-52 min**: Any computation taking >15 min risks context pressure. For large computations, explicitly run as background jobs and write intermediate results.

2. **Pre-supply key numbers in emergency nudges**: When forcing REPORT-SUMMARY.md, providing the actual numerical results in the nudge text allows the explorer to write the summary without recomputing.

3. **CWD check as Task 0 works**: 100% success rate in E007-E009 for preventing directory confusion.

4. **Standard Explorer (E007) stalls longer than Math Explorer**: Web search loops cause 45+ min delays. "Write partial results after every 5 searches" instruction needed.

5. **Scope to minimum**: E008 ran 4 computation paths when 2 were needed. E009 ran correctly scoped. Pre-identifying the single decisive test saves time.

---

## Budget Usage

| Exploration | Type | Goal | Outcome |
|-------------|------|------|---------|
| E001 | Math | Off-diagonal form factor | PARTIAL: 1.6% gap closure, perturbative invalid |
| E002 | Math | Li criterion computation | SUCCEEDED: λ_n > 0 confirmed, crossover found |
| E003 | Math | Non-perturbative K(τ) | SUCCEEDED: Δ₃=0.1545 confirmed |
| E004 | Math | N²/p universality test | SUCCEEDED (negative): universality REJECTED |
| E005 | Math | Rigidity hierarchy | SUCCEEDED: hierarchy established |
| E006 | Math | K(τ) from prime orbit sums | PARTIAL: Berry formula confirmed, K→Σ₂ broken |
| E007 | Standard | Adversarial novelty review | PARTIAL: Li ratio NOVEL (4/5); Berry = artifact |
| E008 | Math | Li ratio validation (5k zeros) | PARTIAL: ratio confirmed at K=N=2000, truncation found |
| E009 | Math | Li ratio convergence test | SUCCEEDED: ARTIFACT confirmed, claim refuted |

9 of 10 explorations used. 10th budget unit used for this report.

---

*Strategizer: Strategy-003, Atlas mission, Riemann Hypothesis*
*2026-03-28*
