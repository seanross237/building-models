---
topic: Prime corrections improve bulk statistics but destroy local correlations
confidence: verified
date: 2026-03-27
source: "riemann-hypothesis strategy-001 exploration-004"
---

## Finding

Prime oscillatory corrections to the smooth (xp/Weyl) spectrum **improve bulk statistics** (number variance) but **destroy local correlations** (level repulsion). This reveals that primes carry the right fluctuation information at macroscopic scales but cannot reproduce the fine-grained GUE structure.

## Quantitative Results (P_max = 10,000, 2,000 zeros)

| Statistic           | Actual zeros | Smooth spectrum | Prime-corrected | GUE prediction |
|---------------------|-------------|-----------------|-----------------|----------------|
| Spacing std         | 0.385       | 0 (crystal)     | 0.636 (too large)| ~0.42         |
| NN MSE vs Wigner    | 0.005       | 2.483           | 0.044           | 0              |
| Level repulsion β   | 2.32        | N/A             | 0.03            | 2.0            |
| Number var MSE vs GUE| —          | baseline        | **75.5% improvement** | 0         |

## The Paradox Explained

1. The prime corrections have approximately the **right total variance** — fluctuations match roughly at bulk scales.
2. But they're applied via linearization at smooth zeros, which doesn't preserve the **repulsion structure**.
3. The linearized corrections all have magnitude |δ| = 0.5/N_smooth'(T) regardless of local context — they carry no information about neighbor spacing.

## Significance

This confirms the theoretical expectation: the trace formula (which relates primes to the counting function) captures **spectral density** but not **spectral correlations**. Number variance is a density statistic; level repulsion is a correlation statistic. Primes help with the former, not the latter.
