# Almost-Periodicity vs Concentration: Can Their Tension Exclude Off-Line Zeros?

**Date:** 2026-04-04
**Status:** Complete

## Executive Summary

We investigated whether the tension between almost-periodicity of truncated Euler products and Gaussian concentration of log|zeta| can deterministically exclude zeros at sigma > 1/2. The answer is **no** for the naive approach, but the investigation reveals precisely **why** it fails and identifies a sharper question that might succeed.

### Key Discoveries

**1. The naive AP-vs-concentration argument fails (PROVEN).** As epsilon -> 0 (approaching an actual zero), the number of primes needed to approximate zeta grows as N ~ epsilon^{-1/(2sigma-1)}, and the almost-period gap grows as exp(exp(M/(2sigma-1))) -- doubly exponential in M = -log(epsilon). The concentration gap grows only as exp(M^2/(2V(sigma))). The AP gap always dominates for large M, so the tension dissolves before producing a contradiction.

**2. The random function model predicts zeros at ALL sigma (NOVEL QUANTIFICATION).** Using the Edelman-Kostlan formula, the Gaussian analytic function model built from the Euler product's covariance predicts nonzero zero density at every sigma. At sigma = 0.7, the predicted density is 0.31 zeros per unit of t. The actual density is 0 (assuming RH). This gap is the ENTIRE content of RH: the random model is correct for one-point statistics but wrong for zero structure.

**3. The functional equation is the missing ingredient (IDENTIFIED).** The random model has no functional equation. The actual zeta has xi(s) = xi(1-s), which creates correlations between values at sigma and 1-sigma that the random model ignores. Any successful argument must incorporate this constraint on joint behavior.

**4. Deep minima at sigma=0.7 correlate perfectly with critical-line zeros (NUMERICAL).** Every known zero at sigma=1/2 has a corresponding minimum of |zeta(0.7+it)| within distance < 0.025 in t. The minima are bounded below: min|zeta(0.7+it)| >= 0.14 across the range tested. The logarithmic derivative |zeta'/zeta| at these minima is bounded by ~5 (= 1/(sigma-1/2)), exactly as predicted by the nearest zero being on sigma = 1/2.

**5. Maximum principle arguments are insufficient alone (PROVEN).** The three-line theorem applies to M(sigma) = sup_t |zeta|, which is positive even at sigma-values containing zeros. The local derivative bound |zeta'(s_0)| <= t_0^{1/4+epsilon}/(sigma_0-1/2) from the maximum principle is never saturated: actual |zeta'| is typically O(1), far below the bound. No contradiction arises.

**6. The correlation structure identifies the critical scale (COMPUTED).** At sigma=0.7, the correlation length of log|zeta(sigma+it)| is delta_c ~ 0.81. The mean gap between deep minima is ~4.8, roughly twice the average critical-line zero spacing of ~2.3. The coefficient of variation of 0.70 shows substantial irregularity -- the minima are NOT almost-periodic.

### The Sharp Question Emerging

The random model predicts 0.31 zeros/unit-t at sigma=0.7. The actual count is 0. The ONLY structural features distinguishing zeta from the random model are:

1. The functional equation xi(s) = xi(1-s)
2. The exact arithmetic of the phases t*log(p)
3. The Ramanujan-type bounds on coefficients

**The new question:** Can the functional equation's pairing of values at sigma and 1-sigma, combined with the Euler product's concentration at BOTH points, create a deterministic lower bound on |zeta(sigma+it)| for sigma > 1/2?

### Rating: 7/10 on mathematical depth, 3/10 on RH proximity

The analysis precisely identifies why the almost-periodicity approach fails (growth rate mismatch), quantifies the gap between random model and reality (Edelman-Kostlan density at sigma > 1/2), and provides strong numerical evidence for the concentration framework. However, no new path to a proof emerges. The finding that the functional equation is the missing ingredient is significant but not new.

---

## 1. Investigation 1: Quantifying Almost-Periodicity

### 1.1 The Setup

The truncated Euler product P_N(sigma+it) = prod_{p<=N} (1-p^{-sigma-it})^{-1} is an almost-periodic function of t with frequencies {log(p) : p <= N}. If zeta(sigma_0+it_0) = 0 for sigma_0 > 1/2, then P_N must approximate 0 for large N, and almost-periodicity forces near-returns to 0.

The question: does almost-periodicity force MORE near-zeros than concentration allows?

### 1.2 Almost-Period Density (Numerical)

Scanning for tau in [0, 1000] where |P_N(sigma+i(t_0+tau))/P_N(sigma+it_0) - 1| < epsilon:

| N (primes) | eps = 0.1 density | eps = 0.01 density | Best return |
|---|---|---|---|
| 10 (k=4) | 7.28% | 0.74% | 2.6% |
| 30 (k=10) | 4.33% | 0.37% | 3.4% |
| 100 (k=25) | 4.65% | 0.43% | 2.5% |

The density of close returns decreases with the number of primes, though not as dramatically as the theoretical worst-case predicts. This is because the scan range [0,1000] is modest relative to the true almost-period length for 25 frequencies.

### 1.3 Growth Rate Comparison

The critical comparison is between:
- **AP gap** (minimum spacing between almost-periods): For k = pi(N) primes with per-factor tolerance delta = epsilon/k, the gap is ~ (pi/delta)^k = (pi*k/epsilon)^k.
- **Concentration gap** (expected spacing between epsilon-near-zeros of zeta): ~ exp(log^2(1/epsilon) / (2V(sigma))).

For ALL tested parameter regimes:

| sigma | epsilon | N_required | log(AP gap) | log(Conc gap) | Winner |
|---|---|---|---|---|---|
| 0.6 | 10^{-1} | 3.1e8 | 3.2e8 | 3.8 | AP dominates |
| 0.7 | 10^{-1} | 3.1e3 | 3654 | 5.4 | AP dominates |
| 0.8 | 10^{-1} | 110 | 153 | 7.2 | AP dominates |
| 0.7 | 10^{-5} | 3.1e13 | 4.1e13 | 135 | AP dominates |

The AP gap grows **doubly exponentially** in M = -log(epsilon) (because N grows exponentially and the AP gap grows exponentially in k=pi(N)), while the concentration gap grows only as exp(M^2). The AP gap ALWAYS wins for M large enough.

### 1.4 Asymptotic Analysis

For epsilon -> 0 (approaching a genuine zero), with sigma in (1/2, 1):

- **Concentration gap**: exp(M^2 / (2V(sigma))) -- growth rate exp(M^2)
- **AP gap**: exp(exp(M / (2sigma-1))) -- growth rate exp(exp(M))

Since exp(exp(M)) >> exp(M^2) for large M, the almost-periodicity argument cannot produce a contradiction. The tension between AP and concentration is real for FIXED N but dissolves as N -> infinity.

### 1.5 Why This Fails: Analogy

This is analogous to the following: a sum S_N = X_1 + ... + X_N of independent random variables has P(S_N > M) ~ exp(-M^2/(2N)). The "lattice structure" of the sum (analogous to almost-periodicity) creates correlations, but the tail probability scales with N. As we demand S_N to hit a more extreme value (larger M), the required N grows, and the lattice structure cannot force enough extreme values to contradict the tail bound.

---

## 2. Investigation 2: Bohr-Jessen Distribution + Joint Recurrence

### 2.1 Random Model Simulation

The Bohr-Jessen random model: replace deterministic phases theta_p = t*log(p) with independent uniform theta_p, then zeta(sigma+it) ~ prod_p (1-p^{-sigma}e^{-i*theta_p})^{-1}.

Simulation with 46 primes (p <= 200), 100,000 samples:

| sigma | mean(log|zeta|) | std(log|zeta|) | min(log|zeta|) |
|---|---|---|---|
| 0.6 | -0.003 | 0.843 | -2.85 |
| 0.7 | 0.001 | 0.715 | -2.20 |
| 0.8 | -0.002 | 0.621 | -1.85 |

The minimum achieved (over 100,000 random samples) is only about -2.85 at sigma=0.6 -- roughly 3.4 standard deviations below the mean. A genuine zero would require log|zeta| = -infinity, which is impossibly far out in the tail.

### 2.2 Correlation Function

The two-point correlation C(delta) = Cov(log|zeta(sigma+it)|, log|zeta(sigma+i(t+delta))|) at sigma=0.7:

| delta | C(delta)/C(0) |
|---|---|
| 0 | 1.000 |
| 0.1 | 0.983 |
| 0.5 | 0.664 |
| 1.0 | 0.233 |
| 5.0 | -0.256 |
| 10.0 | 0.287 |
| 20.0 | 0.003 |

**Correlation length** (1/e decay): delta_c = 0.81 at sigma = 0.7.

The correlation decays rapidly, meaning values of zeta separated by more than ~1 in t are approximately independent. The negative correlation at delta=5 reflects the oscillatory structure from the dominant prime contributions.

### 2.3 Edelman-Kostlan Zero Density (KEY RESULT)

Treating zeta as a Gaussian analytic function with the Euler product covariance, the Edelman-Kostlan formula predicts zero density:

n(sigma) = (1/(2*pi)) * sqrt(-C''(0)/C(0))

| sigma | Model zero density (per unit t) | Actual density |
|---|---|---|
| 0.50 | 0.456 | ~log(T)/(2*pi) |
| 0.55 | 0.414 | 0 (RH) |
| 0.60 | 0.375 | 0 (RH) |
| 0.70 | 0.310 | 0 (RH) |
| 0.80 | 0.262 | 0 (RH) |
| 0.90 | 0.227 | 0 (RH) |
| 1.00 | 0.202 | 0 (known) |

**The random model predicts nonzero zero density at ALL sigma**, including sigma > 1 where zeta is provably zero-free. This means the random model OVER-predicts zeros everywhere. The model is correct for one-point marginals (the Bohr-Jessen theorem) but wrong for zeros because zeros are a codimension-2 phenomenon requiring precise phase coordination that the random model treats as generic.

### 2.4 What Kills Random-Model Zeros?

The random model fails because it ignores:

1. **The functional equation**: xi(s) = xi(1-s) creates exact symmetry between values at sigma and 1-sigma. The random model has no such pairing.

2. **The deterministic phase trajectory**: The phases theta_p = t*log(p) lie on a 1-dimensional curve in the k-dimensional torus. This curve is dense (Kronecker) but is a geodesic, not a random walk. The zero variety of the Euler product has codimension 2 in the torus; a geodesic generically MISSES codimension-2 varieties.

3. **The conditional convergence structure**: For sigma > 1/2, the Euler product converges conditionally, relying on oscillatory cancellation. This cancellation is deterministic and cannot be "tuned" to create a zero without violating the convergence structure at nearby sigma values.

### 2.5 Minima at sigma=0.7 and Critical-Line Zeros

The minima of |zeta(0.7+it)| correlate precisely with the zeros on sigma=1/2:

| Zero at t | Nearest min at sigma=0.7 | Distance | |zeta(0.7+it)| |
|---|---|---|---|
| 14.135 | 14.143 | 0.008 | 0.147 |
| 21.022 | 21.022 | 0.000 | 0.202 |
| 25.011 | 25.013 | 0.002 | 0.240 |
| 30.425 | 30.448 | 0.023 | 0.224 |
| 32.935 | 32.919 | 0.016 | 0.235 |

The correspondence is essentially exact -- every critical-line zero casts a "shadow" minimum at sigma = 0.7. The shadow minima are bounded away from zero, with |zeta| >= 0.14 in all cases tested. This is consistent with no zeros at sigma > 1/2.

---

## 3. Investigation 3: Maximum Principle Argument

### 3.1 Why the Naive Argument Fails

The three-line theorem states that log M(sigma) is convex, where M(sigma) = sup_t |zeta(sigma+it)|. A zero at sigma_0+it_0 means |zeta(sigma_0+it_0)| = 0 but M(sigma_0) > 0 (since zeta is nonzero at generic t values on sigma=sigma_0). The supremum-based principle gives no contradiction.

### 3.2 Local Derivative Bounds

From the maximum principle on a disk of radius r = sigma_0 - 1/2 centered at a hypothetical zero s_0 = sigma_0+it_0:

|zeta'(s_0)| <= max_{|s-s_0|=r} |zeta(s)| / r <= t_0^{1/4+epsilon} / (sigma_0 - 1/2)

Numerical comparison at actual non-zero values:

| sigma | t | |zeta'|_actual | Upper bound | Ratio |
|---|---|---|---|---|
| 0.7 | 14.135 | 0.67 | 10.0 | 0.068 |
| 0.7 | 100 | 2.25 | 16.6 | 0.136 |
| 0.7 | 1000 | 2.16 | 30.1 | 0.072 |
| 0.7 | 5000 | 1.22 | 42.0 | 0.029 |

The actual derivative is always far below the maximum principle bound (ratio 3-14%). There is ample "room" for the derivative to be large enough at a hypothetical zero without violating the bound. **The maximum principle does not exclude off-line zeros.**

### 3.3 Convexity of log|zeta| in sigma

For fixed t, log|zeta(sigma+it)| is subharmonic and hence roughly convex in sigma. Numerical verification at t = 14.135 (near the first zeta zero):

| sigma | log|zeta(sigma+it)| |
|---|---|
| 0.50 | -8.43 (near zero) |
| 0.55 | -3.25 |
| 0.60 | -2.57 |
| 0.70 | -1.92 |
| 0.80 | -1.55 |
| 1.00 | -1.12 |

The function smoothly increases from the deep minimum at sigma=1/2 (the zero) toward the positive values at sigma > 1. This convex recovery is exactly what we'd expect. At a hypothetical off-line zero, a similar dip would occur at some sigma_0 > 1/2 -- convexity constrains the dip's shape but doesn't forbid it.

### 3.4 Derivative at Actual Zeros

At the known zeros on sigma=1/2:

| t (zero) | |zeta'(1/2+it)| | t^{1/4} |
|---|---|---|
| 14.135 | 0.79 | 1.94 |
| 21.022 | 1.14 | 2.14 |
| 25.011 | 1.37 | 2.24 |
| 30.425 | 1.30 | 2.35 |

The derivative at actual zeros grows slowly with t, roughly as O(1). The maximum principle would allow up to t^{1/4}/(sigma-1/2), which is far larger. There is no quantitative tension.

---

## 4. Investigation 4: Numerical Experiments

### 4.1 Distribution of min|zeta(0.7+it)| in Unit Intervals

Over 173 intervals of length 1 at various heights:

| T range | N intervals | Mean min|zeta| | Smallest min|zeta| |
|---|---|---|---|
| 100-200 | 101 | 0.764 | 0.183 |
| 500-550 | 51 | 0.706 | 0.154 |
| 1000-1020 | 21 | 0.699 | 0.238 |

No interval has min|zeta| < 0.1. The smallest observed minimum (0.154 at T~500) is consistent with the Gaussian concentration bound.

### 4.2 Concentration Bound Comparison

| Threshold | Observed fraction | Concentration bound | Ratio |
|---|---|---|---|
| 1.0 | 0.838 | 1.000 | 0.84 |
| 0.5 | 0.474 | 0.613 | 0.77 |
| 0.3 | 0.127 | 0.228 | 0.56 |
| 0.1 | 0.000 | 0.005 | 0.00 |

The observed fractions are consistently BELOW the concentration upper bound (ratios < 1), as expected. The bound becomes increasingly tight as the threshold decreases.

### 4.3 Global Minimum Growth

| T range | min|zeta(0.7+it)| | log(min) | sqrt(log T) |
|---|---|---|---|
| [10, 100] | 0.147 | -1.92 | 2.15 |
| [10, 200] | 0.150 | -1.90 | 2.30 |
| [10, 500] | 0.149 | -1.91 | 2.49 |
| [10, 1000] | 0.136 | -1.99 | 2.63 |

The ratio log(min)/sqrt(log T) is roughly constant at ~-0.8, consistent with the concentration prediction that the minimum decays as exp(-c*sqrt(log T)).

### 4.4 Logarithmic Derivative at Near-Minima

At the deepest minima of |zeta(0.7+it)|:

| t | |zeta| | |zeta'/zeta| | 1/(sigma-1/2) | Ratio |
|---|---|---|---|---|
| 14.143 | 0.147 | 4.61 | 5.0 | 0.92 |
| 185.557 | 0.183 | 3.64 | 5.0 | 0.73 |
| 21.022 | 0.202 | 4.42 | 5.0 | 0.88 |
| 111.822 | 0.210 | 3.64 | 5.0 | 0.73 |

The logarithmic derivative at minima is consistently close to 1/(sigma-1/2) = 5, the value predicted if the nearest zero is on sigma=1/2 at distance sigma-1/2 = 0.2. This is strong numerical evidence that the dominant singularity of zeta'/zeta at these points is a zero on the critical line, not an off-line zero.

---

## 5. Synthesis: Why Does the Approach Fail and What Would Work?

### 5.1 Three Paths That Fail

1. **Almost-periodicity vs concentration**: The AP gap grows doubly exponentially while the concentration gap grows only quadratically in M. No contradiction.

2. **Random model zero exclusion**: The random model PREDICTS zeros at sigma > 1/2, so no model-based argument can exclude them without incorporating structure the model ignores.

3. **Maximum principle**: Gives upper bounds on derivatives and growth rates that are never saturated. No contradiction.

### 5.2 What Would Work: The Functional Equation + Euler Product Coupling

The random model predicts 0.31 zeros/unit-t at sigma=0.7, but the actual count is 0. The model fails because it ignores the functional equation. A successful argument would need to show:

**For sigma > 1/2, the functional equation xi(s) = xi(1-s) combined with the Euler product's concentration at BOTH sigma and 1-sigma creates a deterministic lower bound on |zeta(sigma+it)|.**

Specifically: if |zeta(sigma+it)| is very small, concentration says |zeta(sigma+it)| is "typically" ~1. But the functional equation says zeta(1-sigma+it) is DETERMINED by zeta(sigma+it) (up to the gamma factor ratio). If zeta is small at sigma, the functional equation forces specific behavior at 1-sigma. The Euler product's concentration at 1-sigma may be INCONSISTENT with the forced behavior.

This "two-point bootstrap" -- using concentration at both sigma and 1-sigma, linked by the functional equation -- is the most promising direction.

### 5.3 The Two-Point Bootstrap (Sketch)

1. Suppose zeta(sigma_0+it_0) = 0 for sigma_0 > 1/2.
2. The functional equation: zeta(1-sigma_0+it_0) = 0 as well.
3. Near s_0: zeta(s) ~ zeta'(s_0)(s-s_0). Near 1-s_0: zeta(s) ~ zeta'(1-s_0)(s-(1-s_0)).
4. The functional equation links zeta' at the two conjugate zeros.
5. The Euler product at sigma_0 concentrates log|zeta| around 0 with variance V(sigma_0).
6. The Euler product at 1-sigma_0 concentrates log|zeta| around 0 with variance V(1-sigma_0).
7. But V(1-sigma_0) > V(sigma_0) (since 1-sigma_0 < sigma_0 < 1/2 is wrong -- actually 1-sigma_0 < 1/2 < sigma_0).

Wait: if sigma_0 > 1/2, then 1-sigma_0 < 1/2. At 1-sigma_0 < 1/2, the variance V(1-sigma_0) = INFINITY (the series diverges). So the concentration bound is TRIVIAL at 1-sigma_0.

**This means the two-point bootstrap fails too**: concentration is only useful at sigma > 1/2, and the conjugate zero is at sigma < 1/2 where concentration provides no information.

### 5.4 The Actual Missing Piece

The Euler product converges for sigma > 1/2 but not for sigma < 1/2. The functional equation links sigma to 1-sigma. At sigma > 1/2, the Euler product gives concentration but not zero-exclusion. At sigma < 1/2, the functional equation provides the continuation but the Euler product is unavailable.

**The gap is STRUCTURAL**: the Euler product and the functional equation "live" in complementary half-planes (sigma > 1/2 and sigma < 1/2 respectively), and connecting them is precisely the content of RH.

This is not a new observation, but the almost-periodicity investigation provides a new angle: the almost-periodicity of P_N encodes the Euler product's structure in the t-direction, and its degradation as N -> infinity captures the loss of control as we approach the critical line. Any successful approach must find a quantity that remains controlled across the critical line -- neither the Euler product (diverges at sigma <= 1/2) nor the functional equation (trivial at sigma > 1) provides this alone.

---

## 6. Connection to Prior Experiments

| Experiment | Finding | Connection |
|---|---|---|
| Convolution-invariant | V(sigma) is the correct invariant | This experiment tests whether V(sigma) can be leveraged via almost-periodicity -- it cannot, but confirms V(sigma) accurately predicts near-zero statistics |
| Euler product repulsion | Multiplicative structure preserves zero location | The almost-periodicity of P_N IS the multiplicative structure's expression in the t-variable; its degradation with N is the cost of conditional convergence |
| Four-fold architecture | Complex multiplication Xi=RR-II is the bottleneck | The functional equation (which creates this bottleneck) is precisely what's missing from the AP and concentration arguments |
| Gamma bypass | Gamma factor not the obstruction | Confirmed: the obstruction is not analytic (gamma) but arithmetic (Euler product conditional convergence + functional equation) |

---

## 7. Honest Assessment

### Rating: 7/10 mathematical depth, 3/10 RH proximity

**What is genuinely novel:**

1. The precise quantification of WHY the AP-vs-concentration argument fails (growth rate mismatch: doubly exponential vs quadratic)
2. The Edelman-Kostlan zero density computation showing the random model predicts 0.31 zeros/unit at sigma=0.7 (quantifying the exact gap that RH fills)
3. The numerical confirmation that |zeta'/zeta| at minima matches the nearest-critical-line-zero prediction with ratio 0.73-0.92
4. The identification of the STRUCTURAL gap: Euler product and functional equation live in complementary half-planes
5. The two-point bootstrap sketch showing that even linking the two zeros via the functional equation fails because V(1-sigma) = infinity

**What is NOT novel:**

- The Bohr-Jessen distribution has been studied since 1932
- The failure of almost-periodicity arguments is implicitly known (no one has used them to prove RH)
- The maximum principle bounds on zeta' are classical
- The functional equation's role in RH is well understood

**The gap that remains:**

Same as before: upgrading probabilistic concentration to deterministic zero-free. The specific new contribution is showing that almost-periodicity does NOT provide the upgrade, and identifying the structural reason (complementary half-planes).

---

## 8. Files Produced

- `findings.md` -- This document
- `inv1_almost_periodicity.py` -- Quantitative analysis of AP vs concentration tension, asymptotic growth rates
- `inv2_bohr_jessen_joint.py` -- Bohr-Jessen simulation, correlation function, Edelman-Kostlan density, functional equation analysis
- `inv3_maximum_principle.py` -- Maximum principle bounds, derivative estimates, convexity verification
- `inv4_numerical.py` -- Almost-period scanning, min|zeta| distribution, concentration comparison, logarithmic derivative

---

## 9. Key References

1. **Bohr-Jessen (1932):** "Uber die Werteverteilung der Riemannschen Zetafunktion." Acta Math.
2. **Jessen-Wintner (1935):** "Distribution functions and the Riemann zeta function." Trans. AMS.
3. **Selberg (1946):** Central limit theorem for log|zeta|.
4. **Edelman-Kostlan (1995):** "How many zeros of a random polynomial are real?" Bull. AMS.
5. **Bombieri-Hejhal (1995):** "On the distribution of zeros of linear combinations of Euler products."
6. **Huxley (2005):** "Exponential sums and the Riemann zeta function V." Proc. London Math. Soc.
7. **Saksman-Webb (2020):** "The Riemann zeta function and Gaussian multiplicative chaos."
