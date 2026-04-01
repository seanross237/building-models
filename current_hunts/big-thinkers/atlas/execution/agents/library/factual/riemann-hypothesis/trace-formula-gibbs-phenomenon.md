---
topic: Trace formula Gibbs phenomenon — irreducible 1/2 offset at zeros
confidence: verified
date: 2026-03-27
source: "riemann-hypothesis strategy-001 exploration-004"
---

## Finding

The explicit formula for the oscillatory part of the zero counting function,

```
N_osc(T) = -(1/π) Σ_p Σ_m [1/(m·p^{m/2})] sin(m·T·ln(p))
```

exhibits a **Gibbs phenomenon** at the actual zeta zeros. Because the prime sum is a sum of continuous sine functions, it converges to the **midpoint** of the left and right limits at step discontinuities in N(T). This produces an irreducible 1/2 offset at every zero, independent of how many primes are included.

## Quantitative Evidence

After correcting for the 1/2 offset, the residual converges extremely slowly as **P_max^{-0.13}**:

| P_max | # primes | Mean |residual| (after 1/2 correction) |
|-------|----------|--------------------------------------|
| 10    | 4        | 0.099                                |
| 100   | 25       | 0.065                                |
| 1,000 | 168      | 0.049                                |
| 10,000| 1,229    | 0.036                                |

To reach residual 0.01 would require P_max ~ 10^7.5 ≈ 30 million primes.

## Formula Correction

**Important**: The correct explicit formula does NOT contain a ln(p) factor. The formula `N_osc ≈ -(1/π) Σ [ln(p)/(m·p^{m/2})] sin(...)` is WRONG — the ln(p) factor belongs in Chebyshev's ψ(x), not in N(T). Verified numerically: without ln(p) matches direct computation within ~3%; with ln(p) the error is ~48%.

## Individual Prime Contributions

Each prime p contributes with RMS amplitude ~1/(π√p). The total contribution from primes up to P is ~√P/ln(P), which diverges — individual contributions don't converge, but the combined oscillatory sum converges conditionally.

## Significance

This is a fundamental structural limitation of the trace formula approach: the prime sum can approximate N_osc to arbitrary accuracy **between** zeros but not **at** them. Since zero reconstruction requires N_osc at (or very near) the zeros, the Gibbs phenomenon sets a hard floor on what the explicit formula can achieve for individual zero positions.
