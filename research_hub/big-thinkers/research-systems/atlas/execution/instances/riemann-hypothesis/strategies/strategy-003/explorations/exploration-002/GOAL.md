# Exploration 002: Li's Criterion — Computational Probing

## Mission Context

You are working on the Riemann Hypothesis. The mission is to understand whether there are novel patterns in the spectral properties of zeta zeros that could contribute to a proof strategy.

The **Li equivalence** (1997): RH is equivalent to λ_n ≥ 0 for all n ≥ 1, where:

**λ_n = Σ_ρ [1 − (1 − 1/ρ)^n]**

summed over ALL non-trivial zeros ρ (i.e., both ρ and ρ* = 1-ρ are included).

This is a completely independent line of attack from the random matrix/spectral rigidity approach used in the previous 18 explorations.

## Background: What Li's Criterion Is

**Li (1997) proved:** RH is true if and only if λ_n ≥ 0 for all integers n ≥ 1.

The λ_n are the "Li coefficients" or "Li numbers." They can also be written as:

**Alternative formula via the ξ function:**
λ_n = (1/(n-1)!) × d^n/ds^n [s^(n-1) log ξ(s)] at s=1

where ξ(s) = (1/2)s(s-1)π^(-s/2)Γ(s/2)ζ(s) is the completed zeta function.

**Known asymptotics (Li 1997, Bombieri-Lagarias 1999):**
λ_n ~ (n/2)·log(n/(2πe)) + (n/2)·(γ_E − 1) + (1/2)·log(π) + (1/2) + O(log n)

where γ_E ≈ 0.5772156649 is the Euler-Mascheroni constant.

**More precise asymptotics (Coffey 2004):**
λ_n = (n/2)·log(n/2π) + (n/2)·(γ_E − 1) + (1/2)·log(π) + (1/8)·log(4π/e) + (1/2) + O((log n)/n)

Check both forms.

**Practical computation:** The cleanest way to compute λ_n uses mpmath's built-in Riemann zeta zeros:
```python
from mpmath import mp, mpf, nstr, zetazero, log, pi, gamma, euler, fsum
mp.dps = 50  # 50 decimal digits

def compute_lambda_n(n, num_zeros=2000):
    """Compute Li coefficient lambda_n using first num_zeros zero pairs."""
    total = mpf(0)
    for k in range(1, num_zeros + 1):
        rho = zetazero(k)
        # Add contribution from rho AND its conjugate 1 - rho*
        # Note: zeta zeros come in pairs (rho, 1-rho*) = (1/2+it, 1/2-it)
        # For each zero rho = 1/2 + it, the conjugate is rho_bar = 1/2 - it
        # Both contribute: [1-(1-1/rho)^n] + [1-(1-1/rho_bar)^n]
        term_rho = 1 - (1 - 1/rho)**n
        term_rho_bar = 1 - (1 - 1/rho.conjugate())**n
        total += term_rho + term_rho_bar
    return total
```

**Note on zero pairs:** Each zetazero(k) gives one zero in the upper half plane (Im > 0). The sum over ALL non-trivial zeros includes both ρ and ρ̄ = 1 - ρ* (its complex conjugate). Since ζ(s) = ζ(1-s̄)* (functional equation), if ρ is a zero then so is 1-ρ* = ρ̄.

## Your Task

### Task 1: Compute λ_n for n = 1 to 100

Start with n=1 to 100 using 2000 zero pairs (4000 zeros total including conjugates), mpmath at 50-digit precision.

After completing this task, IMMEDIATELY write results to REPORT.md. Mark [SECTION COMPLETE] and save the λ values as a .npy or .npz file.

**Expected values (sanity checks):**
- λ_1 should equal log(4π) + γ_E/2 - 2 ≈ 0.0231... (Bombieri-Lagarias formula for n=1)
- λ_1 > 0 always (this is known)
- All λ_n should be positive (RH is true to billions of zeros)
- λ_n should grow like (n/2)·log(n) for large n

### Task 2: Extend to n = 1 to 500 (or maximum feasible)

If n=100 takes less than 10 minutes, extend to n=500. If it takes more than 10 minutes per 100 values, stop at n=200.

**Time estimate:** mpmath zetazero for 2000 zeros takes ~6-10 minutes. But λ_n computation can be vectorized — all n values can be computed from the same set of zeros. So: compute the 2000 zero pairs ONCE, then compute all n values from the stored zeros.

```python
# Efficient: compute all zeros first
zeros = [zetazero(k) for k in range(1, 2001)]  # ~6-10 min
# Then for each n, sum over stored zeros (fast)
for n in range(1, 501):
    lambda_n = sum((1-(1-1/rho)**n) + (1-(1-1/rho.conjugate())**n) for rho in zeros)
```

After completing this task, IMMEDIATELY write results to REPORT.md. Mark [SECTION COMPLETE] and save all λ values as a .npz file.

### Task 3: Verify Asymptotic Behavior

Compute the residual:
**δ_n = λ_n − [(n/2)·log(n/2πe) + (n/2)·(γ_E − 1)]**

Also try the Coffey (2004) correction:
**δ_n^Coffey = λ_n − [(n/2)·log(n/2π) + (n/2)·(γ_E − 1) + (1/2)·log(π) + (1/8)·log(4π/e) + (1/2)]**

For each:
- What is the magnitude of δ_n for large n?
- Does δ_n show systematic trends (monotone, oscillating, random)?
- Does Coffey's correction reduce |δ_n|?

After completing this task, IMMEDIATELY write results to REPORT.md. Mark [SECTION COMPLETE].

### Task 4: Pattern Search in the Residual

Look for structure in δ_n:

**4a: Oscillation test**
- Is there a dominant oscillation frequency? Compute FFT of δ_n for n=50 to 500
- If δ_n oscillates with period ~log(p) for some prime p, this would be highly significant
- If δ_n ~ C·cos(2πn/p) for some prime p, plot δ_n and check visually

**4b: Growth rate analysis**
- Compute δ_n/log(n) — does it converge to a constant?
- Compute δ_n/√n — does it look like random noise?
- The difference between these behaviors tells you whether corrections are systematic or statistical

**4c: Prime correlation test**
- Does δ_n show any structure at n = prime - 1 or n = prime?
- Compute running average of |δ_n| for n near primes vs n away from primes
- (If the Li criterion connects to prime distribution, one might expect prime-correlated structure)

**4d: Comparison to GUE expectation**
- If the zeta zeros behave like GUE eigenvalues, what does the Li sum look like?
- Generate a GUE random matrix (N=500 or larger), compute its "Li coefficients":
  λ_n^GUE = Σ_ρ_GUE [1 - (1 - 1/ρ_GUE)^n]
  where ρ_GUE are the (scaled) eigenvalues of the GUE matrix
- Compare the residual δ_n^GUE to δ_n^zeta
- Do they have similar structure? This would be novel: it would connect Li coefficients to RMT

After completing these tests, IMMEDIATELY write results to REPORT.md. Mark [SECTION COMPLETE].

### Task 5: Connection to Spectral Statistics

The prior 18 explorations established that:
- Zeta zeros are GUE class (β=2)
- Δ₃_sat = 0.155 (super-rigid)
- Berry's formula connects Δ₃ to prime sums

**Question for this task:** Is there a direct connection between λ_n and the spectral rigidity Δ₃?

Approach:
- For the GUE comparison in Task 4d, also compute Δ₃ for the GUE matrix
- Compare to the λ_n^GUE residual structure
- If the GUE eigenvalues with the correct Δ₃ (≈0.23) have different λ_n structure than eigenvalues with Δ₃ = 0.155, this would suggest Li coefficients can detect super-rigidity

**This is speculative.** It's fine if nothing interesting emerges. The question is whether it's worth reporting.

After completing this task, IMMEDIATELY write results to REPORT.md. Mark [SECTION COMPLETE].

## Success and Failure Criteria

### This exploration SUCCEEDS if:
1. λ_n computed for n = 1 to at least 100 (ideally 500), all positive
2. Residual δ_n analyzed and any structure reported
3. Either: a pattern is found, OR: absence of pattern is documented with quantitative confidence

### This exploration PARTIALLY SUCCEEDS if:
- n < 50 due to computational speed (mpmath too slow)
- Pattern tests are inconclusive (common — say so clearly)

### This exploration FAILS if:
- mpmath crashes or produces NaN values
- λ_n < 0 for any n (this would be a falsification of RH — IMMEDIATELY flag as CRITICAL FINDING)
- Cannot complete even n=1 to 20

## Warning: Known Pitfalls

1. **scipy.optimize is BROKEN in this environment** (numpy.Inf removed in newer numpy). Do not use scipy.optimize at all.

2. **mpmath speed:** zetazero(k) for k=1 to 2000 takes ~6-10 minutes. Pre-compute ALL zeros first, then iterate over n values. Do NOT recompute zeros for each n.

3. **Numerical precision:** At high n and large magnitude zeros, (1-1/ρ)^n can overflow. Use mpmath's full precision throughout. Do not convert to numpy floats until the final step.

4. **The sum over PAIRS:** Each zetazero(k) gives ρ = 1/2 + i·t_k (upper half plane). The full sum includes both ρ and its conjugate ρ̄ = 1/2 - i·t_k. If you include only the upper half plane zeros, you get HALF the correct λ_n.

5. **GUE "Li coefficients" in Task 4d:** GUE eigenvalues are real, not complex. The "Li formula" for real eigenvalues x_k needs to be adapted — you're looking for 1 - (1 - 1/x_k)^n. This is only well-defined if x_k ≠ 0. Scale the GUE eigenvalues to be in the range [1, T] matching the zeta zero imaginary parts.

## Required Output Structure

Write REPORT.md in this directory. Use incremental writing — write each section immediately after completing it:

```
## Section 1: Li Coefficients n=1..100 [SECTION COMPLETE or FAILED]
[Table of λ_n values, sanity check results]

## Section 2: Extension to n=500 [SECTION COMPLETE or FAILED/ABORTED at n=X]
[Final range achieved, time taken]

## Section 3: Asymptotic Residual Analysis [SECTION COMPLETE or FAILED]
[δ_n magnitude, Coffey comparison, growth rate]

## Section 4: Pattern Search [SECTION COMPLETE or FAILED]
[FFT results, prime correlation, GUE comparison]

## Section 5: Connection to Spectral Statistics [SECTION COMPLETE or FAILED]
[GUE Δ₃ comparison, any connection found]

## Section 6: Summary and Novel Findings [SECTION COMPLETE]
```

**After each section: save .npz with computed values.**

Write REPORT-SUMMARY.md last — a concise 1-page summary.

## Exploration Directory

Your working directory: `explorations/exploration-002/` within the strategy-003 directory.
Put all code in `code/` subdirectory.
