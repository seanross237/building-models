# Joint Distribution of (zeta, zeta') at sigma > 1/2

**Date:** 2026-04-04
**Status:** COMPLETE
**Predecessor:** Four-Fold Architecture (which identified the joint (zeta, zeta') reformulation as the most promising next step)

## Executive Summary

We investigate the JOINT distribution of (zeta(sigma+it), zeta'(sigma+it)) for sigma > 1/2, motivated by the reformulation from the Four-Fold Architecture experiment:

**Reformulation:** RH is equivalent to the statement that the joint distribution of (zeta(sigma+it), zeta'(sigma+it)) as t varies never realizes (0, w) for any w satisfying |w| = |chi(sigma+it)| * |zeta'((1-sigma)+it)| at the same t.

**Critical Correction:** The original framing claimed the derivative at an off-line zero must be "vanishingly small." This is WRONG. The derivative must grow as t^{0.85-sigma_0}, which is positive growth for all sigma_0 < 0.85. The chi-constraint is weaker than originally stated.

**Bottom line:** The joint distribution approach reveals genuine structure (very high zeta-zeta' correlation, specific conditional scaling), but does NOT provide a proof path. The conditional distribution of |zeta'| given |zeta| near zero is already compatible with the chi-constraint in 94-98% of near-zero events, meaning the joint distribution does not exclude off-line zeros.

**Rating: 5.5/10 promise, 8/10 mathematical depth, 8/10 novelty.**

---

## 1. Investigation 1: Joint Distribution of (zeta, zeta')

### 1.1 Setup

Sampled (zeta(sigma+it), zeta'(sigma+it)) at ~3300 t-values from t=100 to t=10000 (step 3) for sigma = 0.6, 0.7, 0.8. Derivative computed by central finite difference with h = 10^{-8}.

### 1.2 Correlation Structure

The correlation between |zeta| and |zeta'| is remarkably high:

| sigma | Pearson(|zeta|,|zeta'|) | Pearson(log|zeta|,log|zeta'|) | E[|zeta|] | E[|zeta'|] |
|-------|------------------------|-------------------------------|-----------|------------|
| 0.6   | 0.949                  | 0.852                         | 1.484     | 4.793      |
| 0.7   | 0.957                  | 0.858                         | 1.318     | 2.894      |
| 0.8   | 0.932                  | 0.805                         | 1.227     | 1.873      |

This is NOT consistent with independence -- the joint distribution is far from the product of marginals.

### 1.3 Conditional Distribution of |zeta'| Given |zeta| Small

| sigma | epsilon | Count (of 3301) | min |zeta'| | mean |zeta'| | median |zeta'| |
|-------|---------|-----------------|--------------|---------------|----------------|
| 0.6   | 0.1     | 7 (0.21%)       | 0.692        | 0.841         | 0.787          |
| 0.6   | 0.5     | 734 (22.2%)     | 0.033        | 1.625         | 1.608          |
| 0.6   | 1.0     | 1678 (50.8%)    | 0.033        | 2.268         | 2.053          |
| 0.7   | 0.5     | 576 (17.5%)     | 0.055        | 0.901         | 0.895          |
| 0.7   | 1.0     | 1745 (52.9%)    | 0.014        | 1.286         | 1.184          |
| 0.8   | 0.5     | 443 (13.4%)     | 0.055        | 0.672         | 0.653          |
| 0.8   | 1.0     | 1758 (53.3%)    | 0.009        | 0.861         | 0.781          |

**Key observation:** The conditional mean of |zeta'| decreases with epsilon, but the minimum also decreases. There is no hard lower bound on |zeta'| near |zeta| = 0.

### 1.4 Dense Sampling Near Minimum |zeta| Events

At the t-values where |zeta| was smallest in our survey, we refined with dense sampling (step 0.01):

| sigma | t (approx) | min |zeta| | |zeta'| at min | chi-threshold | ratio |zeta'|/threshold |
|-------|------------|-------------|----------------|---------------|-------------------------|
| 0.6   | 6295       | 0.0719      | 0.591          | 36.4          | 0.016                   |
| 0.6   | 7267       | 0.0745      | 0.581          | 38.5          | 0.015                   |
| 0.7   | 6295       | 0.1338      | 0.664          | 18.3          | 0.036                   |
| 0.7   | 7267       | 0.1398      | 0.724          | 19.0          | 0.038                   |
| 0.8   | 6295       | 0.2013      | 0.674          | 9.15          | 0.074                   |
| 0.8   | 7267       | 0.2138      | 0.740          | 9.40          | 0.079                   |

The derivative at near-zero events is 15-65x SMALLER than the chi-threshold. This initially seems to support the exclusion argument, but see Section 6 for why it doesn't.

### 1.5 Accessibility Check

At ALL near-zero events (|zeta| < 0.5), |zeta'| was below the chi-threshold. This means the actual zeta derivative in the near-zero region is already compatible with the chi-constraint.

---

## 2. Investigation 2: Euler Product and Log-Derivative Structure

### 2.1 Can log|zeta| Diverge to -infinity?

For the Euler product (with 46 primes up to 200) to produce a zero, we need log|zeta| = -infinity. Tested 10,000 random t-values for each sigma:

| sigma | E[log|zeta|] | Std | Min achieved | Stds below mean |
|-------|-------------|-----|-------------|-----------------|
| 0.55  | 0.003       | 0.926 | -3.005    | 3.2             |
| 0.60  | 0.004       | 0.838 | -2.520    | 3.0             |
| 0.70  | 0.005       | 0.716 | -2.023    | 2.8             |
| 0.80  | -0.008      | 0.617 | -1.833    | 3.0             |
| 1.00  | -0.002      | 0.486 | -1.216    | 2.5             |

The minimum log|zeta| achieved is only 2.5-3.2 standard deviations below the mean. The distribution is approximately Gaussian with FINITE variance for sigma > 1/2. The finite variance follows from sum_p p^{-2sigma} < infinity.

**But:** A Gaussian distribution with finite variance CAN take any real value -- it just does so with exponentially small probability. The minimum in 10,000 samples is ~3 sigma, consistent with P(< -3sigma) ~ 0.001. With more samples, we'd get more extreme values.

### 2.2 Random Euler Product Joint (Z, Z')

Using the Bohr-Jessen random model with 46 primes and 100,000 samples:

| sigma | Corr(|Z|,|Z'|) | min |Z| | min |Z'| | Cond mean |Z'| given |Z|<0.1 |
|-------|----------------|---------|----------|------------------------------|
| 0.6   | 0.913          | 0.065   | 0.009    | 0.496                        |
| 0.7   | 0.894          | 0.119   | 0.006    | (too few at <0.1)            |
| 0.8   | 0.875          | 0.153   | 0.003    | (too few at <0.1)            |

### 2.3 Log-Derivative Stability

**Critical finding:** The ratio |Z'/Z| (the log-derivative magnitude) is remarkably stable across different |Z| bins:

sigma=0.6:
| |Z| bin    | n     | mean |Z'/Z| | median |Z'/Z| |
|------------|-------|-------------|---------------|
| [0, 0.1)   | 55    | 5.74        | 5.65          |
| [0.1, 0.5) | 21443 | 2.64        | 2.58          |
| [0.5, 1.0) | 30576 | 1.90        | 1.77          |
| [1.0, 2.0) | 27265 | 1.98        | 1.84          |
| [2.0, 5.0) | 17167 | 2.60        | 2.53          |

**The log-derivative INCREASES as |Z| -> 0.** This is the opposite of what we'd need for exclusion. When |Z| is small, |Z'/Z| is LARGER than average, meaning the derivative is proportionally larger relative to the function value. This makes sense: near a zero, the log-derivative diverges (pole structure).

---

## 3. Investigation 3: Derivative at Zeros via Euler Product

### 3.1 The Pole Structure of zeta'/zeta

At any zero rho of zeta:
- zeta(s) = (s-rho)*g(s) where g(rho) = zeta'(rho) (nonzero for simple zero)
- zeta'/zeta(s) = 1/(s-rho) + g'(s)/g(s) (simple pole with residue 1)
- The Euler product sum over primes DIVERGES at rho

### 3.2 Prime Sum vs Exact Log-Derivative Near Zeros

Near critical-line zeros (delta = distance from zero):

| Zero (t)  | delta | |zeta|     | Exact |zeta'/zeta| | Prime sum |
|-----------|-------|-----------|----------------------|-----------|
| 14.135    | 1.0   | 8.35e-1   | 1.11                 | 1.70      |
| 14.135    | 0.1   | 7.99e-2   | 10.09                | 3.54      |
| 14.135    | 0.01  | 7.92e-3   | 100.3                | 3.41      |
| 14.135    | 0.001 | 7.73e-4   | 1025.9               | 3.39      |

**Key finding:** As we approach the zero, the exact log-derivative diverges as 1/delta (pole), but the prime sum (with 100 primes) SATURATES at ~3.4. The prime sum captures the "regular part" of the log-derivative, not the pole. The pole comes from the collective behavior of ALL primes, which the finite partial sum misses.

### 3.3 Critical-Line Derivative Growth

From the first 100 zeros of zeta:

|zeta'(1/2+it)| ~ t^{0.354}

This power-law growth means the mirror derivative at height t grows approximately as t^{0.35}.

---

## 4. Investigation 4: Davenport-Heilbronn Comparison

### 4.1 Off-Line Zeros Found

The DH function (5000 terms) has 4 off-line zeros detected in [0.5, 1.0] x [0, 100]:

| sigma    | t       | |f|      | |f'|   | |chi| approx | |f'|/|chi| |
|----------|---------|----------|--------|-------------|------------|
| 0.50157  | 75.911  | 9.4e-15  | 3.653  | 0.996       | 3.67       |
| 0.50320  | 8.937   | 1.8e-15  | 2.136  | 0.999       | 2.14       |
| 0.50078  | 89.437  | 4.3e-14  | 4.621  | 0.998       | 4.63       |
| 0.50231  | 99.682  | 6.1e-14  | 3.800  | 0.994       | 3.82       |

**All DH off-line zeros have |f'|/|chi| >> 1** (ratios 2.1-4.6). This means the mirror derivative is substantial (2-5 times the function value at the paired zero). DH zeros are very close to sigma = 1/2 (within 0.003), so |chi| is close to 1.

### 4.2 Joint Distribution Comparison

Quantile comparison of (function, derivative) distributions:

sigma=0.7:
| Quantile | |zeta| | |DH|  | |zeta'| | |DH'|  |
|----------|--------|-------|---------|--------|
| 1%       | 0.226  | 0.216 | 0.206   | 0.348  |
| 5%       | 0.316  | 0.420 | 0.489   | 0.744  |
| 10%      | 0.391  | 0.530 | 0.718   | 1.010  |
| 50%      | 0.955  | 1.020 | 1.808   | 2.030  |

The distributions are qualitatively similar. DH has slightly smaller |f| values in the lower tail but larger derivatives. The DH function produces off-line zeros NOT because its joint distribution differs dramatically from zeta's, but because it lacks the Euler product structure that constrains where zeros can appear.

### 4.3 DH Correlation Structure

| sigma | Corr(|f|,|f'|) for DH | Corr(|zeta|,|zeta'|) for zeta |
|-------|----------------------|-------------------------------|
| 0.6   | 0.855                | 0.949                         |
| 0.7   | 0.871                | 0.957                         |
| 0.8   | 0.816                | 0.932                         |

**Zeta has HIGHER correlation between function and derivative than DH at all sigma values.** The Euler product creates tighter coupling between zeta and zeta'. This is a genuine structural difference, though it does not translate directly into zero exclusion.

---

## 5. Investigation 5: Information-Theoretic Analysis

### 5.1 Mutual Information

| sigma | I(|zeta|;|zeta'|) | I(log|zeta|;log|zeta'|) | Fraction of H(log|zeta'|) explained |
|-------|-------------------|-------------------------|-------------------------------------|
| 0.6   | 0.823 nats        | 0.905 nats              | 76.0%                               |
| 0.7   | 0.906 nats        | 0.937 nats              | 75.4%                               |
| 0.8   | 0.807 nats        | 0.838 nats              | 67.2%                               |

Knowing |zeta| explains 67-76% of the uncertainty in log|zeta'|. This is a very high mutual information.

### 5.2 Conditional Entropy by |zeta| Range

sigma=0.6:
| |zeta| range | n   | H(|zeta'|) | mean |zeta'| | std  |
|-------------|-----|------------|---------------|------|
| [0, 0.5)    | 580 | 1.18       | 1.70          | 0.83 |
| [0.5, 1.0)  | 693 | 1.55       | 2.71          | 1.26 |
| [1.0, 2.0)  | 609 | 1.78       | 4.26          | 1.62 |
| [2.0, 5.0)  | 481 | 2.24       | 7.97          | 2.52 |

The conditional entropy of |zeta'| DECREASES sharply as |zeta| decreases (from 2.24 nats for |zeta| in [2,5) to 1.18 nats for |zeta| < 0.5). The derivative distribution is much more concentrated when |zeta| is small.

### 5.3 Scaling Exponent

Fitted |zeta'| ~ |zeta|^alpha in different regions:

| sigma | Alpha (bottom bins) | Alpha (middle bins) | Alpha (top bins) |
|-------|--------------------|--------------------|-----------------|
| 0.6   | 0.64               | 0.59               | 0.67            |
| 0.7   | 0.36               | 0.74               | 0.99            |
| 0.8   | 0.57               | (varies)           | 1.15            |

Alpha < 1 means the log-derivative |zeta'/zeta| grows as |zeta| -> 0. At the bottom tail, alpha ~ 0.4-0.6, confirming that the derivative shrinks slower than the function.

---

## 6. Critical Correction: The Chi-Constraint is Weaker Than Claimed

### 6.1 The Original Claim (WRONG)

The original setup stated that at an off-line zero rho = sigma_0 + it_0:
> |zeta'(rho)| must be "vanishingly small," decaying as (t_0/2pi)^{1/2-sigma_0}

### 6.2 The Corrected Analysis

The functional equation derivative relation is:
    |zeta'(rho)| = |chi(sigma_0+it_0)| * |zeta'((1-sigma_0)+it_0)|

Where:
- |chi(sigma_0+it_0)| ~ (t_0/2pi)^{1/2-sigma_0} -- this factor DECAYS
- |zeta'((1-sigma_0)+it_0)| -- the mirror derivative -- this factor GROWS

The mirror derivative at height t_0 grows. From the first 100 critical-line zeros:
    |zeta'(1/2+it)| ~ t^{0.354}

For the mirror zero at 1-sigma_0 < 1/2, the derivative grows at least this fast (and likely faster, since the chi factor amplifies fluctuations on the left half).

Combined: |zeta'(rho)| ~ t^{1/2-sigma_0} * t^{0.354} = t^{0.854-sigma_0}

| sigma_0 | Effective exponent | Behavior as t -> infinity |
|---------|-------------------|--------------------------|
| 0.6     | 0.254             | GROWS                    |
| 0.7     | 0.154             | GROWS                    |
| 0.8     | 0.054             | GROWS (slowly)           |
| 0.854   | 0.000             | BOUNDED                  |
| 0.9     | -0.046            | DECAYS                   |

**The derivative at a hypothetical off-line zero GROWS with height for sigma_0 < 0.854.** It is NOT vanishingly small. The chi-factor's decay is more than compensated by the mirror derivative's growth.

Only for sigma_0 very close to 1 does the derivative genuinely decay.

### 6.3 Verification

We computed |zeta'(sigma_0+it)| at the heights of the first 20 critical-line zeros and compared with the chi-bound:

sigma_0=0.7:
| gamma    | actual |zeta'| | chi-bound | ratio |
|----------|----------------|-----------|-------|
| 14.135   | 0.6747         | 0.6745    | 1.000 |
| 21.022   | 0.8938         | 0.8929    | 1.001 |
| 25.011   | 1.0412         | 1.0406    | 1.001 |
| 30.425   | 0.9569         | 0.9512    | 1.006 |
| 32.935   | 0.9985         | 0.9923    | 1.006 |

The actual derivative matches the chi-bound to 3-4 decimal places at critical-line zero heights. This is because the functional equation is an exact identity -- at t values where there IS a zero on the critical line, the chi-relation is automatically satisfied everywhere on the line sigma = sigma_0.

---

## 7. Near-Zero Derivative vs Chi-Bound

### 7.1 At General t Values

Scanning t = 100 to 5000 (step 5) for each sigma:

| sigma_0 | Points | |zeta'| < chi-bound | Fraction |
|---------|--------|--------------------|---------:|
| 0.6     | 981    | 526                | 53.6%    |
| 0.7     | 981    | 501                | 51.1%    |
| 0.8     | 981    | 462                | 47.1%    |

About HALF of all points have derivative below the chi-bound. This means the chi-constraint is not a tight exclusion -- many points (including those far from zeros) already satisfy it.

### 7.2 At Near-Zero Events

Among events with |zeta| < 0.5:

| sigma_0 | Near-zero events | Fraction with |zeta'| < chi-bound |
|---------|-----------------|-----------------------------------|
| 0.6     | 580             | 93.97%                            |
| 0.7     | 445             | 97.98%                            |
| 0.8     | 333             | 94.89%                            |

Near-zero events almost always have derivative below the chi-bound. This means the conditional derivative distribution at small |zeta| is NOT bounded away from the chi-constraint region -- it is solidly WITHIN it.

**This is the death blow for the joint distribution approach.** If 94-98% of near-zero events already satisfy the chi-constraint, then the constraint provides no exclusion.

---

## 8. The Euler Product: Why It Doesn't Give a Hard Exclusion

### 8.1 The Product-Sum Relationship

- zeta(s) = PRODUCT of 1/(1-p^{-s}) (multiplicative)
- zeta'(s) = zeta(s) * SUM of -log(p)*p^{-s}/(1-p^{-s}) (additive, via the log-derivative)

The log-derivative zeta'/zeta is an ADDITIVE function of the prime contributions, while zeta itself is MULTIPLICATIVE. This creates the high correlation but not a hard constraint.

### 8.2 The Convergence Argument (and Its Limits)

For sigma > 1/2:
- The variance of log|zeta| is FINITE: V(sigma) = sum_p 1/(2*p^{2sigma}) < infinity
- The log-derivative sum is CONVERGENT (away from zeros)
- By CLT-type results, log|zeta| is approximately Gaussian with finite variance

For a zero, we'd need log|zeta| = -infinity. A Gaussian with finite variance assigns probability 0 to any single point, but the density f_sigma(0) > 0 (established in the Four-Fold Architecture experiment). So the probability of |zeta| < epsilon is O(epsilon^2), not zero.

The Euler product tells us that zeros at sigma > 1/2 would require the sum of independent random contributions to produce an extreme event -- possible but very rare. The rarity is polynomial (not exponentially impossible), which is consistent with the known zero-density estimates N(sigma, T) << T^{A(sigma)}.

### 8.3 Large-Scale Scaling Analysis (1M Random Euler Product Samples)

Using 1,000,000 samples from the random Euler product with 60 primes, we measured the scaling exponent alpha in |Z'| ~ |Z|^alpha with high precision:

| sigma | alpha (bottom 3 bins) | Bottom 0.01% min |Z'| | Bottom 0.01% mean |Z'/Z| |
|-------|-----------------------|-----------------------|--------------------------|
| 0.55  | 0.482                 | 0.320                 | 7.84                     |
| 0.60  | 0.424                 | 0.370                 | 6.54                     |
| 0.70  | 0.302                 | 0.420                 | 4.56                     |
| 0.80  | 0.166                 | 0.475                 | 3.32                     |

**Alpha decreases with sigma.** At sigma=0.8, alpha ~ 0.17, meaning |Z'| barely decreases as |Z| -> 0. The log-derivative |Z'/Z| grows rapidly, approaching the pole-like behavior expected near actual zeros.

**Critical observation:** The minimum |Z'| in the bottom 0.01% is BOUNDED AWAY FROM ZERO even with 1M samples. At sigma=0.6, the smallest |Z'| seen is 0.370, and at sigma=0.8 it is 0.475. The derivative does not approach zero in the random Euler product model.

However, this is a finite-sample effect. The true Bohr-Jessen distribution has positive density at (0, w) for all w, so arbitrarily small |Z'| values are possible in principle -- just extremely rare.

### 8.4 Conditional Derivative vs Chi-Bound by Height

The ratio of conditional mean derivative (at near-zero events) to chi-bound, broken by t-range:

| sigma | t range     | cond/bound ratio |
|-------|------------|-----------------|
| 0.6   | [100, 500)  | 0.73            |
| 0.6   | [500, 2000) | 0.50            |
| 0.6   | [2000,5000) | 0.43            |
| 0.6   | [5000,10000)| 0.31            |
| 0.7   | [100, 500)  | 0.68            |
| 0.7   | [500, 2000) | 0.44            |
| 0.7   | [2000,5000) | 0.41            |
| 0.7   | [5000,10000)| 0.36            |
| 0.8   | [100, 500)  | 0.68            |
| 0.8   | [500, 2000) | 0.55            |
| 0.8   | [2000,5000) | 0.60            |
| 0.8   | [5000,10000)| 0.57            |

The ratio DECREASES with height for sigma=0.6 and 0.7 (from 0.73 down to 0.31-0.36). This means the conditional derivative grows SLOWER than the chi-bound as t increases. The gap between the conditional derivative and the chi-bound is WIDENING.

**This is a glimmer of hope -- the conditional derivative falls further below the chi-bound at greater heights.** But it never reaches zero, and the gap is insufficient to prove exclusion. The conditional derivative is 30-70% of the chi-bound, not approaching it from above or being bounded away from it from below.

### 8.5 Why Convergence Doesn't Prevent Zeros

The sum sum_p p^{-sigma} converges for sigma > 1/2 -- but only BARELY. The rate of convergence slows as sigma -> 1/2+. This means:

- At sigma = 0.51, the sum converges but extremely slowly (takes primes up to ~10^{100})
- The partial sums have large fluctuations before settling down
- In the "window" where partial sums are still fluctuating, they can temporarily cancel

A zero of zeta corresponds to such a cancellation becoming permanent (in the limit). The Euler product doesn't rule this out because conditional convergence ALLOWS individual partial sums to be arbitrarily negative.

---

## 9. Honest Assessment

### 9.1 What This Investigation Establishes

1. **The joint (zeta, zeta') distribution is highly non-trivial.** Correlation > 0.93, mutual information explaining 67-76% of derivative entropy. The marginal distributions greatly undercount the joint structure.

2. **The chi-constraint is WEAKER than originally claimed.** The derivative at a hypothetical off-line zero GROWS with height (as t^{0.85-sigma_0}), not shrinks. The original framing confused the chi-factor's decay with the total constraint.

3. **The conditional derivative distribution at small |zeta| falls WITHIN the chi-bound region.** In 94-98% of near-zero events, the derivative is already below the chi-threshold. The joint distribution approach provides no exclusion.

4. **Zeta has higher (zeta, zeta') correlation than the DH function.** Correlations differ by 0.05-0.09 in favor of zeta. This structural difference comes from the Euler product but doesn't translate to zero exclusion.

5. **DH off-line zeros have substantial derivatives.** |f'|/|chi| ratios of 2-5 at DH zeros, showing that the mirror derivative at off-line zeros can be large. DH zeros are very close to sigma=1/2 (within 0.003).

6. **The log-derivative |zeta'/zeta| grows as |zeta| -> 0.** Scaling exponent alpha ~ 0.4-0.6, meaning the derivative shrinks slower than the function. This is consistent with the pole structure at genuine zeros.

### 9.2 What This Investigation Does NOT Establish

1. **No proof or partial proof of RH.** The joint distribution approach does not exclude off-line zeros.

2. **No new rigorous bound.** All findings are computational/heuristic and do not constitute rigorous theorems.

3. **No improvement over Conrey's 40%.** The approach doesn't connect to the mollifier technology needed for such results.

### 9.3 What We Learned That Is Novel

1. **Corrected the chi-constraint analysis.** The derivative at off-line zeros is NOT vanishing -- it grows as t^{0.85-sigma_0}. This is an important correction to the Four-Fold Architecture findings.

2. **Quantified the joint distribution structure.** Tables of conditional distributions, scaling exponents, and information measures that don't appear in the literature.

3. **Established the zeta vs DH correlation gap.** Zeta's Euler product creates 5-9% higher function-derivative correlation than DH, a measurable structural difference.

4. **The log-derivative stability phenomenon.** |zeta'/zeta| has a remarkably stable distribution that changes slowly with |zeta|, except for the pole-induced growth at |zeta| near 0.

### 9.4 Remaining Questions

1. **Can the log-derivative growth rate as |zeta| -> 0 be made rigorous?** If alpha < 1 can be proven, it would give a lower bound on derivative growth at near-zeros.

2. **Is there a sigma-dependent exclusion?** For sigma close to 1, the chi-constraint DOES require vanishing derivatives (the effective exponent becomes negative). Can this be leveraged for zero-free regions wider than the classical ones?

3. **What happens in the COMPLEX plane?** Our analysis focused on real sigma and varying t. The joint distribution in a 2D neighborhood of a hypothetical zero might reveal additional constraints.

---

## 10. Computation Scripts

- `joint_distribution.py` -- Main survey of (zeta, zeta') at 3300 t-values for sigma=0.6, 0.7, 0.8. Conditional analysis, chi-constraint check, dense sampling near near-zero events.
- `euler_product_analysis.py` -- Euler product log-divergence analysis, random Euler product joint distribution (100K samples), log-derivative stability, prime sum behavior near zeros.
- `davenport_heilbronn.py` -- DH function construction, off-line zero search and derivative analysis, joint distribution comparison with zeta.
- `information_theory.py` -- Mutual information, conditional entropy, log-derivative distribution, scaling exponent analysis.
- `pole_structure_analysis.py` -- Critical-line derivative growth fit, chi-constraint bounds at hypothetical zeros, near-zero derivative vs chi-bound scan.
- `deep_analysis.py` -- Large-scale random Euler product (1M samples), extreme tail analysis, corrected chi-constraint theory, fundamental obstruction analysis.

---

## 11. References

1. Bohr, Jessen. "On the distribution of the values of the Riemann zeta function." Amer. J. Math. 58 (1936).
2. Davenport, Heilbronn. "On the zeros of certain Dirichlet series." J. London Math. Soc. 11 (1936).
3. Titchmarsh. "The Theory of the Riemann Zeta-Function." Oxford, 1986.
4. Selberg. "Contributions to the theory of the Riemann zeta-function." Archiv for Mathematik og Naturvidenskab 48 (1946).
5. Conrey. "More than two fifths of the zeros of the Riemann zeta function are on the critical line." J. Reine Angew. Math. 399 (1989).
6. Steuding. "Value-Distribution of L-Functions." Springer Lecture Notes 1877 (2007).
7. Saksman, Webb. "The Riemann zeta function and Gaussian multiplicative chaos." Annals of Probability 48(6), 2020.
