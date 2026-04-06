# Jensen's Formula Bridge: From Probabilistic Concentration to Deterministic Zero-Free Regions

**Date:** 2026-04-04
**Status:** Complete

## Executive Summary

We investigated whether Jensen's formula can bridge the gap from probabilistic concentration (Euler product gives Gaussian tails for log|zeta|) to deterministic zero-free regions. The answer is **decisively negative across all four approaches**, but the investigation precisely identifies WHY and WHERE the obstruction lies.

### Key Findings

**1. Concentration + Jensen gives zero-density exponent A(sigma) = 1 (NEGATIVE RESULT).** This is worse than all classical bounds: Ingham gives 3(1-sigma)/(2-sigma), Huxley gives 12(1-sigma)/5, Guth-Maynard gives 30(1-sigma)/13. The reason: Jensen requires ~T disks to cover height T, and concentration only improves the O(log T) factor per disk, not the O(T) factor from covering. Classical methods use the mean-value theorem for Dirichlet polynomials, which exploits multiplicative structure more efficiently than concentration alone.

**2. Jensen + concentration cannot improve on classical zero-free regions (NEGATIVE RESULT).** For any fixed sigma > 1/2, the convexity bound on the far side of the Jensen circle grows as log(T), while the Jensen "budget" log(R/r) is T-independent. Even the Lindelof hypothesis would not fix this. The best achievable is the de la Vallee Poussin type w ~ c/log(T), while Vinogradov-Korobov achieves w ~ c/(log T)^{2/3}(log log T)^{1/3} via exponential sum estimates that go beyond concentration.

**3. Borel-Cantelli is a dead end due to a precision gap (NEGATIVE RESULT).** In the random model, P(A_T) ~ exp(-C(log T)^2) is super-exponentially small and summable. But the random model approximation error is only |P_actual - P_model| ~ (log T)^{-A}, which dominates. The root cause: truncating the Euler product needs T^{1/sigma} primes, but equidistribution only handles O(log T) primes.

**4. Gaussian concentration is numerically verified (POSITIVE RESULT).** The variance of log|zeta(sigma+it)| matches the predicted V(sigma) = sum_p p^{-2sigma}/2 with ratio ~0.93-0.95. The distribution is close to Gaussian with slightly lighter tails than predicted (zero 3-sigma or 4-sigma excursions in 2000 samples vs 5.4 predicted). Near the first zero at sigma=0.6, the minimum |zeta| is only ~2.8 standard deviations below the mean -- well within normal Gaussian fluctuations.

**5. Zeros are simple and |zeta| vanishes linearly (VERIFIED).** |zeta(sigma+igamma_1)| ~ 0.7932 * (sigma - 1/2) as sigma -> 1/2+, confirming simple zeros with |zeta'(rho_1)| ~ 0.7932.

### The Fundamental Obstruction (CRITICAL INSIGHT)

Jensen's formula converts pointwise information into counting information:
"small |zeta| at center => zeros in disk"

But we need the OPPOSITE direction:
"average |zeta| not too small (concentration) => no zeros pointwise"

This is a **category error in the approach direction**. Jensen gives upper bounds on zero counts from pointwise lower bounds on |f|. We have statistical lower bounds (concentration) and need pointwise zero-free results. Jensen points from pointwise -> counting; we need global/average -> pointwise. **The arrow goes the wrong way.**

The tools that DO go the right direction (pointwise bounds from global structure):
- Exponential sum estimates (Vinogradov's method) -- give zero-free regions
- The large sieve inequality -- gives density estimates
- Halasz-Montgomery method -- gives zero-free regions from L-function moments

All of these exploit the arithmetic/multiplicative structure at a deeper level than concentration of measure. Concentration captures the STATISTICAL behavior of the Euler product but misses the ARITHMETIC structure.

### Rating: 9/10 on mathematical depth, 2/10 on RH proximity

The investigation is thorough and the negative results are definitive. The precise identification of the obstruction (direction mismatch, convexity bound domination, precision gap) is valuable because it closes off a natural line of attack and redirects toward more promising approaches.

---

## 1. Background: The Precise Gap

From the convolution-invariant experiment, we established:

**The Concentration Property:** For sigma > 1/2, the Euler product gives
P(log|zeta(sigma+it)| < -M) <= exp(-M^2 / (2V(sigma)))
where V(sigma) = sum_p p^{-2sigma}/2 converges for sigma > 1/2.

A zero requires log|zeta| = -infinity. The concentration makes this "probabilistically impossible" but doesn't exclude it deterministically.

**The Bridge Strategy:** Use Jensen's formula to convert the *average* behavior (controlled by concentration) into *pointwise* zero counts.

Jensen's formula:
n(r) <= (1/log(R/r)) * [avg of log|f| on circle of radius R - log|f(center)|]

---

## 2. Investigation 1: Zero-Density Estimates from Concentration

### 2.1 Setup

For a rectangle [sigma, 1] x [T, T+H], use Jensen disks centered at sigma_1 + iT_j (sigma_1 = (sigma+1)/2) with:
- R = sigma_1 - 1/2 + delta (big radius, extending past critical line)
- r = sigma_1 - sigma (small radius, containing target zeros)

### 2.2 The Jensen Bound

n(r) per disk <= [convexity bound on circle + |concentration at center|] / log(R/r)

Upper bound on circle: at leftmost point sigma_min = sigma_1 - R = 1/2 - delta, the Phragmen-Lindelof convexity bound gives log|zeta| <= ((1-sigma_min)/2) * log T.

Lower bound at center: concentration gives |log|zeta(center)|| <= C * sqrt(V(sigma_1) * log T) for most T.

Combining: n(r) <= [C1 * delta * log T + C2 * sqrt(V * log T)] / log(R/r)

### 2.3 The Fatal T Factor

To cover [0, T], we need ~T/(2R) disks. Total bound:
N(sigma, T) <= (T/(2R)) * [C1 * log T + C2 * sqrt(V * log T)] / log(R/r) ~ T * log T / C3

This gives zero-density exponent A(sigma) = 1 uniformly, independent of sigma.

### 2.4 Comparison with Classical Bounds

| sigma | A_Ingham | A_Huxley | A_Guth-Maynard | A_concentration |
|-------|----------|----------|----------------|-----------------|
| 0.60 | 0.857 | 0.960 | 0.923 | 1.000 |
| 0.70 | 0.692 | 0.720 | 0.692 | 1.000 |
| 0.75 | 0.600 | 0.600 | 0.577 | 1.000 |
| 0.80 | 0.500 | 0.480 | 0.462 | 1.000 |
| 0.90 | 0.273 | 0.240 | 0.231 | 1.000 |

Our bound is worse across the board. The missing ingredient: the mean-value theorem for Dirichlet polynomials (int_0^T |sum a(n) n^{-it}|^2 dt ~ T * sum |a(n)|^2), which gives cancellation that Jensen alone cannot achieve.

### 2.5 Numerical Confirmation

For T = 144.1 (just above the 50th zero), sigma = 0.8:
- Actual N(0.8, T) = 0 (all zeros on critical line)
- Ingham bound: 12
- Huxley bound: 11
- Concentration-Jensen: ~143

---

## 3. Investigation 2: Pushing Density to Zero (Zero-Free Regions)

### 3.1 The Individual Disk Question

For a SINGLE disk centered at sigma_0 + iT, can we get n(r) < 1?

Condition: avg log|zeta| on circle - log|zeta(center)| < log(R/r)

### 3.2 The Convexity Bound Obstruction

The left side of the Jensen circle reaches sigma < 1/2, where the convexity bound gives log|zeta| ~ C * log(T). This grows with T.

The right side (budget): log(R/r) depends only on sigma, not T.

**For any fixed sigma_0 > 1/2, Jensen's bound exceeds the budget for T large enough.** This is why zero-free regions narrow as T grows.

### 3.3 Impact of Subconvexity

Even the Lindelof hypothesis (mu(1/2) = 0) only reduces the growth to epsilon * log(T), which still grows. A UNIFORM bound on |zeta| for sigma >= 1/2 would suffice, but that is equivalent to RH.

### 3.4 Achievable Zero-Free Region Width

From Jensen + concentration near sigma = 1 (where the pole helps):
- Best achievable: w(T) ~ c/log(T) -- same as de la Vallee Poussin (1896)
- Vinogradov-Korobov: w(T) ~ c/(log T)^{2/3}(log log T)^{1/3} -- better via exponential sums

| T | VK width | Jensen-Conc width |
|------|----------|-------------------|
| 10^6 | 0.0063 | 0.0036 |
| 10^10 | 0.0042 | 0.0022 |
| 10^20 | 0.0025 | 0.0011 |
| 10^50 | 0.0013 | 0.0004 |
| 10^100 | 0.0008 | 0.0002 |

### 3.5 The Direction Mismatch

Jensen's formula: pointwise bound at center => counting bound on zeros
We need: average/statistical bound => pointwise zero-free

**The arrow points the wrong way.** Jensen converts center-value information into zero counts. We want to convert statistical information into center-value bounds. This is fundamentally backwards.

---

## 4. Investigation 3: The Borel-Cantelli Approach

### 4.1 Setup

Define A_T = {zeta has zero with Re > sigma_0 in [T, T+1]}. If sum_T P(A_T) < infinity, Borel-Cantelli gives finitely many A_T.

### 4.2 Grid Covering Bound

Cover [sigma_0, 1] x [T, T+1] with grid spacing delta = T^{-a}:
- N_grid ~ T^{2a}
- Each grid point: P(|zeta| < C * T^mu * delta) <= exp(-(a-mu)^2 * (log T)^2 / (2V))
- P(A_T) <= T^{2a} * exp(-C * (log T)^2)

Since exp(-C * (log T)^2) >> T^{-N} for any N, the sum converges. **In the random model, this proves RH.**

### 4.3 The Fatal Catch: Model Precision Gap

The random model approximation error:
|P_actual - P_model| <= C * (log T)^{-A}

This is MUCH LARGER than the main term exp(-C * (log T)^2).

**Required precision:** super-exponential in log T
**Available precision:** polynomial in log T
**Gap:** unbridgeable with current tools

### 4.4 Root Cause

To approximate the Euler product with k primes:
- Truncation error: O(p_{k+1}^{-sigma}) -- need k > T^{1/sigma} primes
- Equidistribution error: O(C_k / T) with C_k ~ exp(ck) -- need k < C*log T primes

The truncation requirement (polynomial in T) conflicts with the equidistribution limitation (logarithmic in T). This is irreconcilable.

### 4.5 What Borel-Cantelli CAN Give

- RH for random Euler products (already known: Bohr-Jessen 1932)
- Density-one results (already known: Ingham)
- Conditional: if model precision improved to exp(-c*(log T)^2), RH follows

---

## 5. Investigation 4: Numerical Computation

### 5.1 Distribution of log|zeta(sigma+it)|

Computed over 2000 points with t in [10, 2010]:

| sigma | Mean | Var_observed | V_predicted | Ratio | Min | Max |
|-------|------|-------------|-------------|-------|-----|-----|
| 0.6 | -0.003 | 0.773 | 0.828 | 0.933 | -2.60 | 2.14 |
| 0.7 | -0.002 | 0.526 | 0.564 | 0.934 | -2.00 | 1.91 |
| 0.8 | -0.002 | 0.388 | 0.413 | 0.940 | -1.63 | 1.69 |
| 0.9 | -0.001 | 0.299 | 0.316 | 0.947 | -1.36 | 1.51 |

The mean is essentially zero (as predicted). The variance is 93-95% of the predicted V(sigma), with the shortfall from finite T effects. The ratio improves as sigma increases (convergence is faster for larger sigma).

### 5.2 Tail Behavior

| sigma | >2sigma observed | >2sigma Gaussian | >3sigma observed | >3sigma Gaussian |
|-------|-----------------|------------------|-----------------|------------------|
| 0.6 | 70 | 92 | 0 | 5.4 |
| 0.7 | 78 | 92 | 0 | 5.4 |
| 0.8 | 84 | 92 | 0 | 5.4 |
| 0.9 | 85 | 92 | 0 | 5.4 |

The tails are LIGHTER than Gaussian: fewer 2-sigma excursions than predicted, and ZERO 3-sigma excursions (vs 5.4 predicted). This suggests the Euler product structure produces sub-Gaussian tails -- interesting but not helpful for the zero-free problem (we need lower bounds, and lighter tails make it HARDER for |zeta| to be very small).

### 5.3 Jensen Integrals Near the First Zero

For disks centered at sigma + i*14.135 (near first zero at 1/2 + i*14.135):

| Center sigma | R | Jensen sum | n(r) bound | Actual n(r) |
|------|-----|-----------|-----------|-------------|
| 0.6 | 0.2 | 0.693 | <= 1.0 | 1 (the zero) |
| 0.6 | 0.5 | 1.609 | <= 1.0 | 1 |
| 0.7 | 0.5 | 0.916 | <= 1.0 | 1 |
| 0.8 | 0.5 | 0.511 | <= 1.0 | 1 |

Jensen correctly detects the zero at 1/2 + i*14.135. For center sigma = 0.6, the Jensen sum is ~0.69 with R=0.2, consistent with exactly 1 zero at distance r=0.1 (since n*log(R/r) = 1*log(2) ~ 0.69).

### 5.4 Minimum of |zeta| on Vertical Lines

| sigma | min|zeta| | Location (t) | In units of sqrt(V) |
|-------|----------|-------------|---------------------|
| 0.6 | 0.0762 | 14.135 (first zero) | 2.83 |
| 0.7 | 0.1465 | 14.135 | 2.56 |
| 0.8 | 0.2113 | 14.135 | 2.42 |
| 0.9 | 0.2711 | 14.135 | 2.32 |

The minimum always occurs near the first zeta zero. The depth is only 2.3-2.8 standard deviations below the mean -- typical Gaussian fluctuations, not extreme events.

### 5.5 Linear Vanishing Near Zeros

|zeta(sigma + i*gamma_1)| / (sigma - 1/2) converges to 0.7932 as sigma -> 1/2+.

This confirms |zeta'(rho_1)| ~ 0.7932 and that the first zero is simple.

---

## 6. Synthesis: Why This Approach Cannot Work

### 6.1 The Three Obstructions

**Obstruction 1: Direction mismatch.** Jensen converts pointwise -> counting. We need global -> pointwise. The formula is designed to detect zeros from function values, not to exclude zeros from average values.

**Obstruction 2: Convexity bound growth.** Any Jensen circle extending below sigma = 1/2 has average log|zeta| growing as C*log(T). The Jensen budget log(R/r) is T-independent. For large T, the bound always exceeds the budget.

**Obstruction 3: Model precision gap.** The random model gives super-exponentially small "probability" of zeros, but the approximation error is only polynomial in log(T). The error dominates the signal.

### 6.2 What the Concentration DOES Buy

Despite the negative results for zero-free regions, concentration IS useful for:

1. **Understanding the statistical landscape:** V(sigma) ~ (1/2)*log(1/(sigma-1/2)) near sigma = 1/2 precisely quantifies how hard it is for |zeta| to be small.

2. **Confirming the Euler product's role:** The near-perfect variance decomposition (ratio 0.93-0.95) confirms that prime contributions are effectively independent.

3. **Lighter-than-Gaussian tails:** The observed tail behavior (sub-Gaussian) suggests the Euler product constrains extreme fluctuations more than independence alone would predict. This may be exploitable.

4. **Framing the problem:** The concentration gives the correct VALUE of V(sigma) that any successful approach must contend with.

### 6.3 More Promising Directions

The investigation points toward three approaches that DO exploit multiplicative structure at the arithmetic level:

**A. Exponential sum methods (Vinogradov-type).** These directly constrain |sum n^{-it}| using the multiplicative structure of n. They produce zero-free regions by showing |zeta(sigma+it)| > 0 from above (bounding |1/zeta|). This is the direction that WORKS.

**B. Moment methods (Halasz-Montgomery).** Bound int |zeta(sigma+it)|^{2k} dt and use the moments to constrain zero locations. The Euler product structure appears in the combinatorics of the 2k-th moment.

**C. The Selberg sieve + amplification.** Use sieve-theoretic amplifiers to detect zeros. The amplifier is chosen to resonate with the Euler product structure.

All three of these methods exploit the arithmetic structure of the primes (via exponential sums, divisor combinatorics, or sieve weights) rather than just the statistical independence captured by concentration.

---

## 7. Precise Characterization of the Gap

The gap between probabilistic and deterministic is now precisely characterized:

**What we have (probabilistic):**
P(log|zeta(sigma+it)| < -M) <= exp(-M^2/(2V(sigma))) for the random model
V(sigma) < infinity for sigma > 1/2

**What we need (deterministic):**
log|zeta(sigma+it)| > -C(sigma) for ALL t, when sigma > 1/2

**The gap in quantitative terms:**
- Random model gives: zeros have probability 0 (correct for random Euler products)
- Approximation to actual zeta: accuracy ~ (log T)^{-A} (polynomial in log T)
- Required accuracy: ~ exp(-C*(log T)^2) (super-exponential in log T)
- Gap: ~ exp(C*(log T)^2) / (log T)^A, which grows super-exponentially

**The gap in structural terms:**
- Concentration captures: statistical independence of prime contributions
- Classical zero-free methods use: arithmetic structure of primes (exponential sums)
- The missing information: the SPECIFIC phases {t*log(p) mod 2*pi} cannot achieve
  the coordinated cancellation needed for a zero (Vinogradov proves this for sigma near 1)
- Extending Vinogradov from sigma near 1 to sigma > 1/2: requires exponential sum
  control that does not follow from independence alone

---

## 8. Connection to Prior Experiments

| Experiment | Finding | Connection |
|---|---|---|
| Convolution invariant | V(sigma) is the correct structural invariant | This experiment shows V(sigma) enters Jensen's formula but cannot bridge the gap alone |
| Convolution invariant | Probabilistic -> deterministic is the gap | This experiment precisely quantifies the gap: super-exponential vs polynomial precision |
| Euler product repulsion | Multiplicative structure preserves zeros | The arithmetic structure (exponential sums) is what Jensen + concentration MISSES |
| GMC repulsion | sigma = 1/2 is the critical point | V(sigma) divergence at 1/2 is confirmed numerically; the phase transition is real but insufficient for proof |

---

## 9. Honest Assessment

### Rating: 9/10 mathematical depth, 2/10 RH proximity

**What is genuinely valuable:**

1. The **definitive negative result**: concentration + Jensen gives A(sigma) = 1, strictly worse than all classical bounds. This closes off a natural line of attack.
2. The **precise obstruction analysis**: three independent reasons why the approach fails (direction mismatch, convexity growth, precision gap).
3. The **quantification of the model precision gap**: truncation needs T^{1/sigma} primes but equidistribution handles only O(log T). This is the sharpest characterization of WHY the probabilistic approach fails.
4. The **numerical confirmation** of Gaussian concentration: variance ratio 0.93-0.95, sub-Gaussian tails, minimum of |zeta| at ~2.5 standard deviations.
5. The **identification of what DOES work**: exponential sum methods exploit arithmetic structure that concentration misses.

**What is NOT novel:**
- That Jensen's formula gives zero-density estimates (classical, follows Titchmarsh Chapter 9)
- That the random model cannot prove RH (known since Bohr-Jessen)
- That Vinogradov's method uses exponential sums (classical)
- The Gaussian distribution of log|zeta| (Bohr-Jessen 1932, Selberg 1946)

**The bottom line:**
The "Jensen's formula bridge" approach is a dead end. The arrow points the wrong way: Jensen converts pointwise information to counting, but we need the reverse. The concentration inequality, while numerically accurate and structurally illuminating, captures only the statistical independence of the Euler product and misses the arithmetic structure that exponential sum methods exploit. Any successful proof of RH must engage with the arithmetic at a level deeper than concentration of measure.

---

## 10. Files Produced

- `findings.md` -- This document
- `inv1_zero_density.py` -- Zero-density estimate derivation and comparison with classical bounds
- `inv2_zero_free.py` -- Zero-free region analysis, convexity obstruction, comparison with Vinogradov-Korobov
- `inv3_borel_cantelli.py` -- Borel-Cantelli approach, model precision gap, equidistribution limitations
- `inv4_numerical.py` -- Numerical verification: distribution of log|zeta|, Jensen integrals, zero counting

---

## 11. Key References

1. **Jensen (1899):** Jensen's formula relating zero counts to logarithmic integrals
2. **Ingham (1940):** N(sigma, T) <= T^{3(1-sigma)/(2-sigma)+epsilon}, in "On the estimation of N(sigma, T)"
3. **Huxley (1972):** N(sigma, T) <= T^{12(1-sigma)/5+epsilon}, improved density estimate
4. **Guth-Maynard (2024):** N(sigma, T) <= T^{30(1-sigma)/13+epsilon} for sigma near 3/4
5. **Vinogradov (1958):** Exponential sum method giving sigma > 1 - c/(log T)^{2/3}(log log T)^{1/3}
6. **Bohr-Jessen (1932):** Value distribution of log zeta(sigma+it) for sigma > 1/2
7. **Selberg (1946):** Central limit theorem for log|zeta(1/2+it)|
8. **Littlewood (1924):** Conditional results on zero-free regions from RH
9. **Turan (1953):** Power sum method for relating zero distribution to exponential sums
10. **Montgomery (1971):** Halasz-Montgomery method for zero density estimates
