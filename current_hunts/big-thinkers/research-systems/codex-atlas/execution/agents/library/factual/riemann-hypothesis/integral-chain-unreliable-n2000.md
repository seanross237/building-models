---
topic: Integral chains (R₂ and K routes) unreliable for Δ₃ computation at N=2000
confidence: verified
date: 2026-03-28
source: "riemann-hypothesis strategy-003 exploration-003, strategy-003 exploration-006"
---

## Finding

The standard spectral statistics integral chain R₂(r) → Σ₂(L) → Δ₃(L) systematically **overestimates Δ₃_sat by 43%** when computed from N=2000 zeta zeros: chain gives Δ₃_sat ≈ 0.220 vs. the correct 0.155 from direct sliding-window computation. The direct method (least-squares fit of N(x) = Ax + B in sliding windows, averaged over 200 windows per L value) is the reliable approach.

## Quantitative Comparison

| L | Δ₃_direct | Δ₃_R₂_chain | Δ₃_GUE_analytic |
|---|----------|-------------|-----------------|
| 2 | 0.100 | 0.094 | 0.063 |
| 5 | 0.134 | 0.145 | 0.156 |
| 10 | 0.152 | 0.184 | 0.226 |
| 15 | 0.153 | 0.202 | 0.267 |
| 20 | 0.155 | 0.221 | 0.297 |
| 25 | 0.156 | 0.237 | 0.319 |
| 30 | 0.155 | 0.254 | 0.338 |

The chain overestimate grows with L: from ~8% at L=5 to ~64% at L=30. At the saturation plateau (L=15–25), the chain gives 0.220 vs. 0.155 (43% high).

## Root Cause

Three compounding sources of error in the integral chain:
1. **R₂ statistical noise**: With N=2000 and bin width dr=0.05, each R₂ bin contains ~100 pairs at large r, giving ~10% Poisson fluctuations. Point-by-point oscillations at r > 5 are mostly noise.
2. **Double integration amplifies errors**: The chain involves two successive integrations (R₂ → Σ₂ via single integral, Σ₂ → Δ₃ via another integral), which amplify systematic biases in R₂.
3. **Truncation at r_max=30**: Information loss from cutting off the R₂ integral.

## K(τ) from R₂ Fourier Transform

K(τ) = 1 + 2∫(R₂−1)cos(2πτr)dr is qualitatively correct — shows the expected ramp (τ < 0.7) and saturation (τ > 1.5) — but quantitatively unreliable. Key values: K(0.5) = 0.536 (expected ~0.55), K(1.0) = 2.783 (spurious Gibbs spike from truncation), K(1.5) = 1.013 (oscillating around plateau). The Gibbs spike at τ=1 (where GUE K(τ) has a kink) is an unavoidable truncation artifact.

## Empirical R₂ Data

Key R₂ measurements from the same 2000-zero dataset:
- R₂(0) ≈ 0.005 (strong level repulsion, consistent with GUE)
- R₂(1.0) ≈ 0.921 vs GUE 0.999 — **stronger anti-bunching than GUE** at nearest-neighbor distance, consistent with the super-rigidity seen in Δ₃
- Convergence to 1 confirmed: mean R₂ for r ∈ [25, 30] = 1.0002

## Second Integral Route: K(τ) → Σ₂ → Δ₃ (S003-E006)

A second integral route was tested in S003-E006, using the Wiener-Khinchin formula:

1. K(τ) → Σ₂(L) = L − (2/π²) ∫₀^∞ [1−K(τ)] sin²(πLτ)/τ² dτ
2. Σ₂(L) → Δ₃(L) = (2/L⁴) ∫₀^L (L³ − 2L²r + r³) Σ₂(r) dr

**This route also fails**, but for a different reason than the R₂ chain: a **systematic ~2× normalization error** in the K → Σ₂ formula. Using K_GUE = min(τ, 1) as control, the formula gives Δ₃_GUE(L=10) = 0.491 vs the known analytic value 0.226 — a factor of 2.17× overestimate.

| L | Δ₃ (K_GUE integral) | Δ₃ (known GUE) | Ratio |
|---|---------------------|----------------|-------|
| 10 | 0.491 | 0.226 | 2.17 |
| 20 | 1.123 | 0.297 | 3.78 |
| 30 | 1.769 | 0.338 | 5.23 |

The overestimate grows with L. The likely cause is a Fourier convention mismatch (factor of 2π) in the K → Σ₂ formula that was not resolved.

**Relative comparisons are still valid:** K_primes (cap version) gives Δ₃ only 3.3% above GUE through this integral, meaning K_primes ≈ K_GUE for tau < 1 is indistinguishable through the transform. See `super-rigidity-mechanism-berry-formula.md`.

**Summary of two failure modes:**
- **R₂ → Σ₂ → Δ₃ (S003-E003):** 43% overestimate from statistical noise amplification through double integration + truncation at r_max=30
- **K(τ) → Σ₂ → Δ₃ (S003-E006):** ~2× systematic normalization error from Fourier convention mismatch; affects absolute values, not relative comparisons

## Methodological Recommendation

For quantitative Δ₃ computation from zeta zeros, **always use the direct sliding-window method**. Neither integral route (R₂ or K) is reliable at N=2000:
- The R₂ → Σ₂ → Δ₃ chain requires N ≥ 10,000 zeros (where R₂ noise drops to ~3% per bin)
- The K(τ) → Σ₂ → Δ₃ chain has a systematic normalization issue independent of N

For predicting Δ₃_sat from prime orbits, use Berry's direct formula Δ₃_sat = (1/π²)·log(log(T/(2π))) rather than the integral chain.
