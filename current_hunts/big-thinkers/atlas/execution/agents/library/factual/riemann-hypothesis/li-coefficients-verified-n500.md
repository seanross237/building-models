---
topic: Li's criterion — all 500 coefficients verified positive
confidence: verified
date: 2026-03-28
source: "riemann-hypothesis strategy-003 exploration-002, strategy-003 exploration-008 (5000-zero convergence test), strategy-003 exploration-009 (multi-K confirmation)"
---

## Finding

All 500 Li criterion coefficients lambda_n (n=1 to 500) are strictly positive, consistent with RH. Computed using 2000 non-trivial zeta zero pairs at 50-digit precision (mpmath).

## Computation Details

- **Zeros:** 2000 non-trivial zeros (t_1 = 14.1347... to t_2000 = 2515.2865...) pre-computed in ~569s
- **Formula:** lambda_n = Sum_rho [1 - (1 - 1/rho)^n] summed over all zeros and conjugates
- **Precision:** 50 decimal digits (mpmath); all imaginary parts exactly 0.00e+00 (conjugate-pair sum is real)
- **Runtime:** ~80s for all 500 values after zero pre-computation

## Key Values

| n | lambda_n |
|---|----------|
| 1 | 0.02265 |
| 10 | 2.235 |
| 50 | 42.43 |
| 100 | 114.18 |
| 200 | 288.97 |
| 500 | 881.43 |

- **Minimum:** lambda_1 = 0.02265 (smallest, as expected)
- **Growth:** Consistent with (n/2)*log(n) asymptotic

## Sanity Check

lambda_1 computed = 0.022653 vs. exact (Bombieri-Lagarias, infinite zeros) = 0.023096. Difference 4.42x10^-4, entirely from truncation at 2000 zeros. Corrected value 0.02316, within 7x10^-5 of exact.

## Truncation Analysis `[COMPUTED]`

Convergence measured at multiple truncation levels K = 100, 200, 500, 1000, 1500, 2000. **Geometric convergence ratio r ~= 0.646, remarkably uniform across all n values.** The truncation error at K=2000 is approximately 1.83x the last increment. For lambda_500, estimated missing tail contribution: ~130.5 (corrected value ~1012).

The uniform r ~= 0.646 across all n suggests the truncation error has a universal structure depending on zero density, not on n. `[CONJECTURED]`

## Asymptotic Comparison `[COMPUTED]`

Coffey (2004) asymptotic is **2.44x better** than Bombieri-Lagarias (mean |delta| for n >= 50: BL = 98.41, Coffey = 40.35). The Coffey residual becomes increasingly negative for large n due to truncation (computed lambda_n systematically low from missing zeros k > 2000).

## Extended Convergence Test: 5000 Zeros (E008) `[COMPUTED]`

E008 computed all 5000 zeros (t₁=14.13 to t₅₀₀₀=5447.86) and recomputed λ_n:

| n | λ_n (2k zeros) | λ_n (5k zeros) | Change |
|---|---------------|---------------|--------|
| 100 | 114.18 | 116.34 | +1.9% |
| 300 | 479.91 | 499.29 | +4.0% |
| 500 | 881.43 | 935.20 | **+6.1%** |
| 1000 | 1885.47 | 2099.41 | +11.4% |

**For n ≥ 300, the sum is NOT well-converged at K=2000.** Each 1000-zero block adds ~2% to λ_500. The geometric convergence model (r ≈ 0.646) predicted a corrected λ_500 ≈ 1012 (missing tail ~130.5). At K=5000, λ_500 = 935.20, consistent with slow approach to that limit (~41% of predicted missing tail captured). The r ≈ 0.646 ratio remains a useful estimate of the infinite-K limit but substantially underestimates how many zeros are needed to approach it.

**Positivity is unaffected** — all λ_n remain strictly positive at 5000 zeros. The truncation concern is about the comparison to GUE (see li-gue-comparison-super-rigidity.md), not about Li's criterion itself.

**E009 multi-K confirmation:** E009 computed zeta λ_n at K=500, 1000, 2000, 3000, 5000 for n=100..500, confirming monotonic growth with K at all n values (sublinear, decelerating). The convergence behavior is consistent with the r≈0.646 geometric model. Example: λ_500 = 707.4 (K=500), 812.6 (K=1000), 881.4 (K=2000), 909.4 (K=3000), 935.2 (K=5000).

## Negative Results `[COMPUTED]`

- **No prime-correlated structure:** Welch's t = -1.333 (p > 0.05) comparing |delta_C| at prime vs. non-prime n. Slight bias is statistical (primes thin out at larger n where |delta| is larger).
- **No physically meaningful FFT peaks:** Dominant FFT peaks (451.0, 225.5, 90.2) are harmonics of the 451-point window length. Prime-period matches at high frequency have negligible power (~0.1 vs. dominant ~4 million).
- **Coffey residual does NOT converge as delta/log(n):** ratio grows from -0.94 (n=100) to -17.43 (n=500), super-logarithmic, consistent with O(n) truncation error.
