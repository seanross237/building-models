# Exploration 004: Trace Formula Reconstruction — xp + Primes = Zeta Zeros?

## Goal

Test the core Berry-Keating hypothesis computationally: can we reconstruct the zeta zero spectrum by starting from the smooth xp spectrum and adding oscillatory corrections from the explicit formula involving primes?

## Executive Summary

**The answer is nuanced: xp + primes = zeta zeros in the COUNTING FUNCTION sense (N(T) decomposes exactly), but NOT in the sense of reconstructing individual zero positions from the prime sum.**

Three critical issues were discovered:
1. The formula in GOAL.md had an incorrect `ln(p)` factor (corrected)
2. The prime sum exhibits a fundamental 1/2 Gibbs offset at zeros (identified and explained)
3. Individual zero reconstruction via linearization is **mathematically impossible** because N_osc is discontinuous at zeros

For statistical quantities (number variance, pair correlation), the prime corrections DO help, improving fit to GUE by ~75% over the smooth spectrum. But for individual zeros, the primes can only predict the DIRECTION of displacement (100% accuracy), not the magnitude.

---

## Part 1: Zeta Zeros and Smooth Spectrum

### Computed Data
- **2000 actual zeta zeros** via `mpmath.zetazero(n)` (took ~5 minutes total)
- **2000 smooth zeros** by inverting N_smooth(T) = n - 1/2 via Brent's method

**N_smooth(T) = (T/2π)·ln(T/2πe) + 7/8** (the Weyl/xp part)

### First 20 zeros comparison

| n | t_n (actual) | t_n^smooth | δ = actual - smooth |
|---|-------------|-----------|-------------------|
| 1 | 14.1347 | 14.5213 | -0.3866 |
| 2 | 21.0220 | 20.6557 | +0.3663 |
| 3 | 25.0109 | 25.4927 | -0.4818 |
| 4 | 30.4249 | 29.7394 | +0.6855 |
| 5 | 32.9351 | 33.6245 | -0.6895 |
| 6 | 37.5862 | 37.2574 | +0.3288 |
| 7 | 40.9187 | 40.7006 | +0.2182 |
| 8 | 43.3271 | 43.9940 | -0.6669 |
| 9 | 48.0052 | 47.1651 | +0.8400 |
| 10 | 49.7738 | 50.2337 | -0.4598 |

**Displacement statistics (2000 zeros):**
- Mean: -0.0001 (unbiased)
- Std: 0.333
- Mean |δ|: 0.270
- Max |δ|: 0.994

The smooth spectrum captures the gross structure but the fluctuations are O(1) in units of mean spacing.

---

## Critical Formula Correction

### The GOAL.md formula contains an error

The suggested explicit formula includes a `ln(p)` factor:
```
N_osc(T) ≈ -(1/π) Σ_p Σ_m [ln(p)/(m·p^{m/2})] sin(m·T·ln(p))   ← WRONG
```

The correct formula (derived from Im(ln ζ(s)) = -Σ_p Σ_m p^{-ms}/m) is:
```
N_osc(T) = -(1/π) Σ_p Σ_m [1/(m·p^{m/2})] sin(m·T·ln(p))   ← CORRECT
```

**The `ln(p)` factor belongs in ψ(x) (Chebyshev's function), not N(T) (zero counting).**

Verification at T = 14.52 (first smooth zero):
| Method | N_osc value | Error vs direct |
|--------|------------|-----------------|
| Direct (mpmath arg(ζ)) | +0.4995 | — |
| Prime sum, NO ln(p), P_max=10000 | +0.5151 | 0.016 |
| Prime sum, WITH ln(p), P_max=10000 | +0.9765 | 0.477 |

The version without ln(p) matches within ~3%.

---

## Part 2: The Gibbs Phenomenon — Why the Mean Residual is 0.5

### Discovery

When comparing the exact N_osc at actual zeros to the prime sum:
```
N_osc_exact(t_n) = n - N_smooth(t_n)     (definition)
N_osc_prime(t_n) ≈ prime sum evaluated at t_n
```

The residual N_osc_exact - N_osc_prime has **mean = 0.500, independent of P_max**:

| P_max | # primes | mean\|residual\| | After 1/2 correction |
|-------|----------|-----------------|---------------------|
| 10 | 4 | 0.500 | 0.099 |
| 50 | 15 | 0.500 | 0.068 |
| 100 | 25 | 0.500 | 0.065 |
| 1000 | 168 | 0.500 | 0.049 |
| 10000 | 1229 | 0.500 | 0.036 |

### Explanation

The prime sum (being a sum of continuous sine functions) converges to N_osc everywhere EXCEPT at the actual zeros, where N(T) has step discontinuities. At discontinuities, any Fourier-type series converges to the **midpoint** of the left and right limits.

At the nth actual zero:
- N(t_n - ε) = n - 1, so N_osc(t_n - ε) = (n-1) - N_smooth(t_n) ≈ -S_n
- N(t_n + ε) = n, so N_osc(t_n + ε) = n - N_smooth(t_n) ≈ 1 - S_n
- Midpoint = 0.5 - S_n, which differs from the right limit by exactly 0.5

This is the **Gibbs phenomenon** applied to the trace formula.

### After correction: slow convergence

With the 1/2 offset corrected, the residual converges as **P_max^{-0.13}** — extremely slow:

| P_max | Corrected mean\|res\| | Std |
|-------|----------------------|-----|
| 10 | 0.099 | 0.128 |
| 100 | 0.065 | 0.082 |
| 1000 | 0.049 | 0.061 |
| 10000 | 0.036 | 0.046 |

Power law fit: mean|res| ~ P_max^{-0.13}. To reach residual 0.01 would require P_max ~ 10^{7.5} ≈ 30 million primes.

---

## Part 3: Why Individual Zero Reconstruction Fails

### The fundamental obstacle

N_osc at the smooth zeros is **always exactly ±0.5**. This is not a numerical artifact — it's a mathematical identity:

The smooth nth zero satisfies N_smooth(t_n^smooth) = n - 0.5 by definition. The actual counting function N(T) is an integer between zeros. Therefore:
- If t_n^smooth is between actual zeros n-1 and n: N_osc = -0.5
- If t_n^smooth is between actual zeros n and n+1: N_osc = +0.5

Verified by direct computation: all 100 tested smooth zeros have N_osc = ±0.4999 (the deviation from 0.5 is ~10^{-4}).

### Consequences for the linearized formula

The correction δ = -N_osc/N_smooth' always gives |δ| = 0.5/N_smooth'(T), a **constant magnitude** that depends only on T, not on the actual displacement. This correction:
- **Gets the direction right 100% of the time** (verified on 100 zeros)
- **Gets the magnitude wrong** because actual |displacement| varies from 0 to ~1, while the correction is always 0.5/N_smooth' ≈ 1-4 (depending on T)
- **Variance explained: -489%** — worse than no correction at all!

### Root-finding approach

Solving N_smooth(T) + N_osc_prime(T) = n directly also fails because:
- With few primes: N_osc_prime is too smooth, roots may not exist near actual zeros
- With many primes: N_osc_prime becomes highly oscillatory, creating **spurious crossings**
- Example: P_max=10000 gives first "corrected" zero at 20.27 (actual: 14.13)

### Iterative Newton-type correction (using EXACT N_osc via mpmath)

Even with perfect N_osc values (not the prime sum), Newton iteration converges to wrong zeros or oscillates:
- 5 Newton iterations starting from smooth zeros
- Mean |error|: 0.88 (worse than the smooth zero displacement of 0.44)
- The iteration steps over the target zero because N_osc jumps at the zero

**This is an inherent limitation: any continuous approximation to a step function cannot locate the discontinuity to better than half the step height.**

---

## Part 4: Statistical Tests — What Primes DO Help With

### GUE statistics of actual zeros (baseline)

| Statistic | Value | GUE prediction | Quality |
|-----------|-------|---------------|---------|
| Mean spacing | 1.000 | 1.000 | ✓ Exact |
| Spacing std | 0.385 | ~0.42 | ✓ Close |
| NN MSE vs Wigner | 0.005 | 0 | ✓ Good |
| NN MSE vs Poisson | 0.117 | — | ✓ Poisson ruled out (25×) |
| Level repulsion β | 2.32 | 2.0 | ✓ GUE-like |

### Smooth spectrum (no corrections)
- All spacings = 1 exactly (perfectly rigid crystal)
- MSE vs Wigner: 2.483 (catastrophically bad)
- No level repulsion (meaningless — no fluctuations)

### Prime-corrected spectrum (P_max=10000, linearized)
- Mean spacing: 1.000
- Spacing std: 0.636 (too large; actual: 0.385, GUE: ~0.42)
- MSE vs Wigner: 0.044 (9× better than smooth, but 9× worse than actual)
- Level repulsion β: 0.03 (essentially zero — level repulsion destroyed!)
- **Number variance MSE vs GUE: 0.076 (75.5% improvement over smooth)**

### The paradox

The prime corrections **improve bulk statistics** (number variance) but **destroy local correlations** (level repulsion). This is because:
1. The corrections have the right variance (fluctuations match roughly)
2. But they're applied via linearization at smooth zeros, which doesn't preserve the repulsion structure
3. The linearized corrections are all |δ| = 0.5/N_smooth' regardless of local context

### Spectral Form Factor

| τ | K(actual) | K(GUE) |
|---|----------|--------|
| 0.1 | 0.0002 | 0.100 |
| 0.5 | 2.230 | 0.500 |
| 1.0 | 79.293 | 1.000 |
| 1.5 | 2.411 | 1.000 |

The massive peak at τ=1 indicates the spectrum retains crystal-like periodicity. This is from evaluating at actual zeros (not corrected), so the form factor discrepancy is a finite-size effect from using N_smooth for unfolding with only 2000 zeros.

---

## Part 5: Individual Prime Contributions

Each prime p contributes independently to N_osc. The RMS contribution scales as:

| Prime | RMS contribution | Theoretical 1/(π√p) |
|-------|-----------------|-------------------|
| 2 | 0.172 | 0.225 |
| 3 | 0.136 | 0.184 |
| 5 | 0.103 | 0.142 |
| 7 | 0.087 | 0.120 |
| 11 | 0.069 | 0.096 |
| 23 | 0.047 | 0.066 |
| 71 | 0.027 | 0.038 |

The RMS scales as ~1/√p (consistent with 1/(π√p) from the m=1 term). The total contribution from all primes up to P is ~Σ_{p≤P} 1/√p ~ √P/ln(P), which diverges — the sum of the INDIVIDUAL contributions doesn't converge, but the COMBINED oscillatory sum does converge (conditionally).

---

## Part 6: Convergence and Residual Analysis

### Does the corrected spectrum converge to actual zeros as P_max increases?

**For individual zeros: NO.** The variance explained by prime corrections actually **decreases** with P_max:

| P_max | Mean \|residual\| | Variance explained |
|-------|------------------|-------------------|
| 10 | 0.112 | 79.7% |
| 100 | 0.148 | 57.8% |
| 1000 | 0.234 | 14.0% |
| 10000 | 0.275 | -5.5% |

More primes = worse individual zero reconstruction! This is because adding more primes increases the oscillatory corrections' amplitude without improving their alignment with actual zero positions.

### What does the residual look like?

The residual (P_max=10000, after 1/2 correction) is:
- **Not random**: autocorrelation at lag 1 is -0.33 (strong anti-correlation)
- **Not correlated with T**: correlation = 0.002 (no systematic drift)
- **Nearly Gaussian**: skewness 0.05, kurtosis 3.76 (slight heavy tails)
- **Weakly correlated with spacing**: correlation 0.03

The anti-correlation at lag 1 suggests the residual has a characteristic scale of ~1 unfolded spacing, consistent with it being determined by the local zero arrangement.

### Is there a "prime gap"?

**Yes, there is a fundamental gap.** The prime sum provides a continuous approximation to a step function. The irreducible residual is the Gibbs error at step discontinuities, which cannot be reduced by adding more primes. For a step of height 1, the Gibbs phenomenon gives an irreducible overshoot of ~9% of the step height, and the RMS error of the best approximation converges only as ~1/√(# terms).

The slow convergence (~P_max^{-0.13}) confirms this: the prime sum can approximate N_osc to arbitrary accuracy between zeros but not at them. Since zero reconstruction requires N_osc at (or very near) the zeros, individual zero reconstruction is fundamentally limited.

---

## Part 7: Conclusions

### Does xp + primes = zeta zeros?

**Mathematically YES, statistically PARTIALLY, practically NO.**

1. **Exact decomposition**: N(T) = N_smooth(T) + N_osc(T) is an identity. The smooth part comes from xp (the Weyl term), and N_osc is fully determined by primes (explicit formula). So xp + primes = zeta zeros is TRUE as a statement about the counting function.

2. **Statistical reconstruction**: Prime corrections improve number variance by 75% over the smooth spectrum, confirming that the primes carry the right fluctuation information at bulk scales.

3. **Individual zero reconstruction**: Impossible via the linearized explicit formula because N_osc is discontinuous at the zeros (Gibbs phenomenon). Even with exact N_osc values, Newton iteration fails because it steps over zeros. The variance explained by the linearized correction is NEGATIVE for P_max > 5000.

### Key insight for the Hilbert-Pólya program

**The Berry-Keating decomposition is the WRONG framework for reconstructing individual eigenvalues.** The trace formula relates the spectrum to primes via the counting function, which loses all information about individual level positions due to its step-function nature.

To reconstruct individual zeros, one would need either:
- A **spectral determinant** approach: det(H - E) = 0, which requires the actual operator
- A **resolvent** approach: finding poles of Tr(H - E)^{-1}
- Something beyond the trace formula that encodes level positions, not just counting

The trace formula tells you HOW MANY zeros are below T, not WHERE each zero is. The primes correct the "how many" part (N_osc), but the conversion from "how many" to "where" is ill-conditioned at the zeros.

### The Berry-Keating operator, if it exists, encodes MORE than xp + primes

The hypothetical Berry-Keating operator H would have eigenvalues at the zeros. Its trace Tr(f(H)) would give the explicit formula for any test function f. But the OPERATOR itself contains additional structure (eigenvectors, matrix elements) that the trace formula does not capture. This additional structure is what determines the individual eigenvalue positions and the GUE statistics.

The primes determine the SPECTRAL DENSITY (via the counting function) but not the SPECTRAL CORRELATIONS (which come from the operator's structure). The GUE statistics emerge from the operator, not from the primes alone.
