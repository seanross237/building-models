---
topic: Gauss matrix Δ₃ spectral rigidity and the complete rigidity hierarchy
confidence: verified
date: 2026-03-28
source: "riemann-hypothesis strategy-003 exploration-005"
---

## Finding

Spectral rigidity Δ₃ was computed for Gauss sum matrices H_{jk} = Λ(|j-k|+1) × exp(2πi·(j+1)(k+1)/p) at 6 key primes, establishing a complete rigidity hierarchy across all tested constructions and revealing that β (level repulsion) and Δ₃ (long-range rigidity) decouple.

## Gauss Δ₃ Results (N=500)

| p | β_W | Δ₃(5) | Δ₃(15) | Δ₃(30) | Δ₃(50) | Δ₃_sat(25-50) | Pair corr. MRD% |
|---|-----|-------|--------|--------|--------|---------------|-----------------|
| 97 | 0.857 | 0.167 | 0.290 | 0.426 | 0.522 | **0.454** | 16.9 |
| 499 | 0.703 | 0.192 | 0.338 | 0.496 | 0.671 | **0.550** | 16.0 |
| 809 | 1.145 | 0.162 | 0.271 | 0.392 | 0.469 | **0.415** | 16.7 |
| 997 | 1.045 | 0.169 | 0.310 | 0.435 | 0.501 | **0.452** | 15.8 |
| 1801 | 1.061 | 0.172 | 0.304 | 0.402 | 0.480 | **0.426** | 18.3 |
| 9973 | 0.676 | 0.177 | 0.326 | 0.488 | 0.726 | **0.559** | 17.8 |

## Complete Rigidity Hierarchy

```
Zeta zeros:          Δ₃_sat = 0.155    (27% of GUE∞)  — "super-rigid"
N=500 GUE/C1/flat:   Δ₃_sat = 0.23–0.29 (40–50%)     — finite-size GUE baseline
Gauss best (p=809):  Δ₃_sat = 0.415    (71%)          — "mildly rigid"
Gauss worst (p=9973): Δ₃_sat = 0.559   (96%)          — "near GUE∞"
GUE∞ (analytic):     Δ₃_sat = 0.581    (100%)         — infinite-N baseline
```

**Caveat on C1 value:** The report computed C1 Δ₃_sat = 0.285 (5 realizations). However, S002-E009 found C1 Δ₃_sat = 0.243 ± 0.017 (3 realizations), indistinguishable from H_flat (0.256) and GUE control (0.227). The C1 "anomalous rigidity" claim was retracted in E009 — C1's Δ₃ is generic finite-size N=500 GUE behavior (see `von-mangoldt-amplitude-irrelevant-to-delta3.md`). The hierarchy remains valid regardless: all N=500 random-phase ensembles (0.23–0.29) are more rigid than all Gauss matrices (0.42–0.56).

## Key Findings

### 1. Random phases produce stronger long-range correlations than arithmetic phases

Even the best Gauss matrix (p=809, β=1.145) has Δ₃_sat = 0.415 — at least 1.4× LESS rigid than random-phase N=500 constructions (0.23–0.29). This is counterintuitive: random phases produce stronger long-range spectral order than the structured arithmetic phases from Gauss sums.

**Physical explanation:** Random phases (drawn independently from U(1) per off-diagonal entry) provide maximal "phase diversity." Gauss sum phases exp(2πi·jk/p) are globally correlated through the quadratic form jk/p — this systematic structure permits GOE-like short-range repulsion (β≈1) but prevents the long-range correlations needed for GUE-level rigidity.

### 2. β and Δ₃ decouple

Within the Gauss family, higher β weakly correlates with lower Δ₃ (more rigid): p=809 (β=1.145, Δ₃_sat=0.415) vs. p=9973 (β=0.676, Δ₃_sat=0.559). However, C1 (β≈1.18) breaks this pattern dramatically — it achieves much lower Δ₃ than any Gauss matrix with comparable β. Short-range level repulsion (β) and long-range spectral rigidity (Δ₃) are controlled by different structural features of the matrix.

### 3. Gauss pair correlation universally worse than C1

All Gauss matrices show MRD = 15.8–18.3% for pair correlation, about 2× worse than C1's 7.9% (5-realization average). The Gauss matrices satisfy Montgomery's formula at the ~20% level.

### 4. The spectral rigidity gap

The gap between zeta zeros (0.155) and the best construction (finite-size GUE at ~0.23–0.26) remains unresolved. This is the signature of whatever additional structure in the Riemann zeros goes beyond random matrix theory. No construction tested in 19+ explorations achieves Δ₃_sat < 0.2.

## See Also

- `gauss-sum-phases-permanently-goe.md` — β sweep showing GOE cap
- `von-mangoldt-amplitude-irrelevant-to-delta3.md` — C1 rigidity retraction (E009)
- `c1-constraint-scorecard.md` — Full C1 evaluation
- `berry-saturation-confirmed.md` — Zeta zero Δ₃_sat = 0.1550 ± 0.0008
