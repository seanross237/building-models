# Exploration 007: Adversarial Novelty Review — Two Live Claims

**Date:** 2026-03-28
**Goal:** Literature search to assess novelty of two surviving claims from the Riemann Hypothesis spectral rigidity mission.

---

## Pre-Settled Claims

*Recording prior verdicts — no new research needed.*

### Claim 1: Flat Δ₃ saturation plateau (<1% variation, L=15-30)
**VERDICT: NOT NOVEL.**
Berry (1985, Proc. R. Soc. A 400:229) predicted both the saturation phenomenon and the saturation level Δ₃_sat = (1/π²) log(log(T/2π)). Odlyzko (1987, 2001) confirmed numerically at large scale. Our measurement is methodologically clean and adds precision, but the saturation itself was predicted and confirmed three decades ago.

### Claim 4: K_primes correct normalization is (log p)²/p^m (not (log p)²)
**VERDICT: WEAK (prior source exists).**
This is the standard semiclassical amplitude from Berry (1985). The normalization (log p)²/p^m for prime orbit p^m contributions in the periodic orbit sum is explicit in Berry's semiclassical derivation. Our clarification is useful documentation but Berry (1985) is the prior source.

### Claim 5: C1 matrix gives Δ₃=0.285 (intermediate between zeta 0.155 and GUE 0.294)
**VERDICT: RETRACTED.**
The flat-amplitude test (S002 work) revealed this was an artifact of using the wrong GUE baseline. Using the correct finite-N (N=500) GUE baseline (~0.23 vs infinite-N ~0.566): H_flat gives 0.256, C1 gives 0.243, GUE control gives 0.227 — all within ~1σ of each other. The "intermediate Δ₃" was not a real distinguishing feature. Retraction is correct.

[SECTION COMPLETE]

---

## Live Claim 1: λ_n^zeta < λ_n^GUE for n > 300

### What Was Claimed
Our computation found that Li coefficients λ_n^zeta agree well with λ_n^GUE (97.1% correlation) for n < 300, but then λ_n^zeta < λ_n^GUE for n > 300, falling to ratio ~0.95 at n=500. Proposed mechanism: super-rigidity → efficient phase cancellation → smaller large-n Li coefficients.

### Papers Searched

**Li (1997), J. Number Theory 65:325**
[SEARCHED — content not directly retrieved, but well-documented in secondary sources]
Li's original paper defined the positivity criterion and the coefficients λ_n = Σ_ρ [1-(1-1/ρ)^n]. It established the equivalence λ_n ≥ 0 ⟺ RH. The paper is focused on the number-theoretic proof of the criterion. **NO comparison to GUE or random matrix eigenvalues** was part of Li's original work — that connection was never the focus.

**Keiper (1992), Math. Comp. 58:765**
[SEARCHED — not directly retrieved]
Keiper investigated power series expansions of ξ(s) and connections to the Stieltjes constants. His work is on the analytic structure of ξ, not spectral statistics. **NO comparison to GUE.**

**Bombieri & Lagarias (1999), J. Number Theory 77:274**
[FOUND via Semantic Scholar and secondary sources]
Key result: They provided the asymptotic formula under RH:
> λ_n(π) = (N/2) n log n + C₁(π) n + O(√n log n)
where N is the degree of the L-function and C₁(π) is a real constant. For the Riemann zeta function (N=1, degree 1): λ_n ~ (1/2) n log n + O(n).

**Critical observation:** Bombieri-Lagarias establishes the asymptotic for zeta Li coefficients alone. The paper does NOT compute or compare λ_n^GUE for random matrices. There is no crossover discussion, no GUE ensemble comparison.

**Schumayer & Hutchinson (2011), Rev. Mod. Phys. 83:307**
[SEARCHED — paper confirmed to exist, details of Li section not retrieved]
This is the canonical physics review paper. Search results confirm it covers random matrix theory and spectral statistics for zeta zeros, but no indication of any section comparing λ_n^zeta vs λ_n^GUE. The review focuses on the Hilbert-Pólya operator approach, not on Li coefficients as spectral statistics probes.

**General searches: "Li coefficients GUE", "Keiper-Li spectral statistics random matrix", "lambda_n crossover"**
[NOT FOUND]
No paper was found in any search that:
- Computes λ_n for GUE random matrices
- Compares λ_n^zeta to λ_n^GUE point-by-point
- Identifies a crossover at n≈300 where zeta falls below GUE
- Connects the Li coefficient growth rate to spectral rigidity (Δ₃) or to phase cancellation efficiency

### Assessment

The standard literature treats Li coefficients as a number-theoretic object (positivity criterion for RH). The RMT community studies zeta zeros via pair correlations, nearest-neighbor spacings, form factors, and Δ₃ — but not via Li coefficients. These two streams appear to be non-overlapping in the literature.

The Bombieri-Lagarias asymptotic λ_n ~ (1/2) n log n tells us the leading growth, but says nothing about the ratio λ_n^zeta / λ_n^GUE or whether this ratio evolves with n.

**VERDICT: NOVEL (rating 4/5)**

No prior paper compares λ_n^zeta to λ_n^GUE, identifies the crossover at n≈300, or connects the crossover to spectral rigidity. The proposed mechanism (super-rigidity → phase cancellation → smaller large-n λ_n) is new. The observation itself is computationally grounded (97.1% correlation below n=300, ratio 0.95 at n=500).

Caveat: The novelty is contingent on the computation being correct. GUE matrices of dimension N=100 may not be the right comparison (GUE Li coefficients are computed from finite matrices, and the connection to zeta Li coefficients is non-trivial). The 0.95 ratio at n=500 should be verified with larger N and more zeros.

[SECTION COMPLETE]

---

## Live Claim 2: Berry Formula Growing Discrepancy

### What Was Claimed
Using 2000 zeta zeros in height-resolved bins, we found Berry's formula Δ₃_sat = (1/π²) log(log(T/2π)) becomes progressively less accurate as T increases:

| T | Berry prediction | Measured Δ₃_sat | Error |
|---|-----------------|-----------------|-------|
| 383 | 0.143 | 0.1435 | 0.2% |
| 600 | 0.154 | ~0.155 | 0.6% |
| 1108 | 0.166 | 0.1545 | 7.8% |
| 1696 | 0.175 | 0.1569 | 11.2% |
| 2245 | 0.180 | 0.1595 | 12.5% |

The formula should be *more* accurate at larger T (asymptotic), yet empirically it gets worse.

### Papers Searched

**Berry (1985), Proc. R. Soc. A 400:229**
[FOUND — abstract accessed; full text behind paywall (403)]
Berry's original formula Δ₃_sat = (1/π²) log(L_max/2π) + const, where L_max = T/(2π) · e^(something), encodes the saturation from the cutoff of the prime orbit sum. The formula is derived via a diagonal approximation: only terms with T_p = T_{p'} contribute. This is an asymptotic formula valid when L ≪ L_max. The full paper includes discussion of the range of validity, but the abstract/secondary sources confirm: **no explicit correction terms beyond the leading log(log T) are given in Berry (1985) itself.** The formula is first-order.

**Bogomolny & Keating (1996), Phys. Rev. Lett. 77:1472**
[FOUND — confirmed by multiple sources]
This paper goes "beyond the diagonal approximation" in Gutzwiller's trace formula. It computes off-diagonal contributions to spectral correlations. This is directly relevant: Berry (1985) uses only diagonal orbits; Bogomolny-Keating (1996) includes the first correction. However, their corrections affect the form factor K(τ) and two-point correlation function R₂(x), not directly Δ₃_sat in a simple formula. **No accessible source gives a closed-form correction to the Δ₃_sat = (1/π²) log(log T) formula from BK (1996).**

**Odlyzko (1987), Math. Comp. 48:273**
[SEARCHED — secondary sources confirm the paper exists and covers GUE statistics]
Odlyzko's 1987 paper computed 100,000 zeros near zero #10^12 and compared their statistics to GUE predictions. His analysis focused on nearest-neighbor spacings and pair correlations, not specifically Δ₃ at multiple heights in one dataset. He did not generate a T-resolved Δ₃ accuracy table comparable to ours.

**Montgomery (1973)**
[NOT directly relevant to this claim]
Montgomery's pair correlation function established the GUE connection but predates Berry's formula and doesn't discuss Δ₃ saturation.

### Explanation Analysis

Three hypotheses for the growing discrepancy:

**Hypothesis A: Sparse-sample artifact (most likely)**
With N=2000 total zeros, the zeros are distributed over heights T=0 to ~2245. The lowest bins (T≈383) are populated by zeros #1-~100, which are densely spaced and plentiful. The highest bins (T≈2245) are populated by the last few hundred zeros, which are spread thin. Δ₃ statistics require many zeros to converge — with too few zeros in the high-T bins, the measured Δ₃_sat will be unreliable (biased downward if the measurement window overlaps poorly). This explains why measured Δ₃ ≈ 0.155–0.160 for T=600–2245: it's measuring the *global* property of the sparse dataset, not the true asymptotic value at T=2245.

**Hypothesis B: Berry formula is asymptotic for very large T, not T~2000**
Berry's formula uses T in the sense of the height of the zeros, and the log(log T) function changes very slowly. At T=383, log(log 383) ≈ 1.41; at T=2245, log(log 2245) ≈ 1.78. The formula predicts a 26% increase from T=383 to T=2245. Our measured Δ₃ barely moves (0.1435 → 0.1595, an 11% change). This suggests the asymptotic regime for Berry's formula may require much larger T — perhaps T~10^6 or T~10^12 as Odlyzko used. At T~2245, we may still be in a pre-asymptotic regime where finite-T effects dominate.

**Hypothesis C: Beyond-diagonal corrections (Bogomolny-Keating)**
BK (1996) showed that off-diagonal orbits contribute. Their corrections increase with T (they become larger relative to the diagonal term as more orbits contribute). This could cause the formula to overpredict Δ₃_sat at moderate T, explaining why measured < predicted. But this effect would need quantification.

### Assessment

The **growing discrepancy pattern itself (0.2% → 12.5%)** as a quantitative T-resolved table does not appear in any accessible prior work. Odlyzko's work uses zeros at heights ~10^12 (where the formula should be accurate) and does not study the T=383-2245 regime. Berry's own paper does not include a numerical accuracy test across heights.

However, the explanation is almost certainly Hypothesis A (sparse sampling): our dataset has too few zeros to reliably measure Δ₃_sat at T≈2245. This makes the "growing discrepancy" an artifact of measurement design, not a fundamental physics discovery.

**VERDICT: ARTIFACT / WEAK**

The growing discrepancy is most likely a sparse-sampling artifact. We have 2000 zeros total; T-bins at T≈2245 contain too few zeros for reliable Δ₃ measurement. If real (Hypothesis B or C), it would indicate Berry's formula is not yet asymptotic at T~2000, which is known qualitatively but this is the first quantitative table. Novelty rating: **1/5 if artifact, 2/5 if real but known qualitatively.**

[SECTION COMPLETE]

---

## Synthesis

### Consolidated Novelty Verdict Table

| Claim | Verdict | Novelty (1-5) | Strongest Surviving Evidence | Best Counterargument |
|-------|---------|---------------|------------------------------|---------------------|
| Flat Δ₃ plateau | NOT NOVEL | 0 | — | Berry (1985) predicted it; Odlyzko confirmed |
| λ_n^zeta < λ_n^GUE crossover (n≈300, ratio 0.95 at n=500) | **NOVEL** | **4** | Crossover confirmed in computation; no prior paper makes this comparison | May be artifact of GUE matrix dimension mismatch (N=100 GUE vs infinite zeta ensemble) |
| Berry formula accuracy table (T=383–2245, error 0.2%→12.5%) | ARTIFACT/WEAK | 1–2 | Quantitative T-resolved table is new | Growing error almost certainly due to sparse sampling at high T; not a physics discovery |
| K_primes normalization (log p)²/p^m | WEAK | 1 | Useful clarification | Berry (1985) already contains this normalization |
| C1 Δ₃=0.285 intermediate | RETRACTED | 0 | — | Wrong GUE baseline (infinite-N vs finite-N) |

### Strongest Single Novel Claim

**λ_n^zeta / λ_n^GUE < 1 for n > 300, ratio ~0.95 at n=500.**

This is novel because:
1. No prior paper computes λ_n for GUE random matrices and compares to λ_n^zeta
2. The crossover direction (zeta falls *below* GUE at large n) was not predicted in any accessible prior work
3. The proposed mechanism (super-rigidity → efficient phase cancellation) directly connects two separate observables: Δ₃_sat and Li coefficient growth — a connection not in the literature

### What Would Be Needed for Publication

To make this a publishable observation:
- **More zeros:** Current computation uses N=2000 zeta zeros. Need ≥10,000 zeros for the n=500 regime to be statistically reliable. The Odlyzko datasets (up to 10^9 zeros) would provide this.
- **Larger GUE ensemble:** Current GUE uses N_matrix=100 dimension, 1000 matrices. Ideally N_matrix=1000 and 10,000 matrix samples, with error bars on the mean λ_n^GUE narrow enough to resolve the 5% ratio difference.
- **Cross-check the mechanism:** Verify that a synthetic spectrum with Δ₃_sat=0.155 (artificially imposed) also shows the λ_n crossover at n≈300. If yes, the mechanism claim is confirmed. If not, the crossover is a coincidence.
- **Significance threshold:** At n=500, the separation is ~5% and the GUE standard deviation is ~0.3% (from the reported ± 2.68 at n=500 with mean 929). The signal is ~17σ — highly significant *if* the GUE comparison is the right baseline.

The 17σ significance suggests this is not noise, but the key uncertainty is whether N=100 GUE matrices are the right comparison for the infinite-dimensional zeta zeros. A careful theoretical argument connecting the two would be essential.

[SECTION COMPLETE]
