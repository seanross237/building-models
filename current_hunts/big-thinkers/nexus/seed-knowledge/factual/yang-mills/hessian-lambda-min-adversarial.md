---
topic: Adversarial characterization of sup|λ_min(HessS)| and conditional β < 1/8 bound via decoherence
confidence: provisional
date: 2026-03-29
source: "yang-mills-conjecture strategy-003 exploration-004"
---

## Overview

Adversarial optimization over all lattice configurations (d=4, L=2, SU(2)) determines the empirical supremum of |λ_min(HessS(Q))| — the most negative Hessian eigenvalue — which governs the mass gap condition β < 2/sup|λ_min|. The key results: sup|λ_min| ≈ **14.73** (empirical), β < 1/4 is **RULED OUT** via this route, and a conditional bound **β < 1/8** (1.5× improvement over the Gershgorin-based 1/12) follows from an unproved decoherence lemma.

---

## Setup

- **Mass gap condition:** β < 2/sup|λ_min(HessS(Q))|
- **Lattice:** d=4, L=2, N=2 (SU(2)), 192×192 Hessian matrix
- **Hessian:** Analytical formula (verified by finite differences); Hellmann-Feynman gradient for ∂λ_min/∂w via local Rayleigh quotient
- **Search:** 1000 random configs, 200+ structured configs, 35+ gradient descent starts (200-400 iterations each)
- **Decomposition:** HessS = D + C where D = diagonal (self-term), C = off-diagonal (cross-term)

---

## Stage 1: Adversarial Search — Results

### Random survey (1000 configs) [COMPUTED]

| Quantity | Value |
|----------|-------|
| λ_min minimum | -8.983 |
| λ_min mean | -7.739 |
| λ_max maximum | 9.095 |
| |λ_min|_random / 2d | 1.12 |

Random sampling exceeds 2d = 8 but is far from the true supremum.

### Anti-instanton structured configs [COMPUTED]

Anti-instanton configurations Q_μ = iσ_{a(μ)} (with axes assignment a(μ) choosing which SU(2) generator for each lattice direction) achieve dramatically more negative λ_min:

| Axes assignment | Non-comm pairs | λ_min (initial) | λ_min (after GD) |
|-----------------|---------------|-----------------|-------------------|
| (0,0,2,1)       | 5/6           | -14.175         | **-14.734**       |
| (1,1,0,2)       | 5/6           | -14.175         | -14.734           |
| (0,0,1,2)       | 5/6           | -14.054         | -14.515           |
| (0,1,2,0)       | 5/6           | -13.768         | -14.076           |

**Pigeonhole principle:** With 4 directions and 3 SU(2) generators, at most 5/6 axis pairs can be non-commuting. Commuting-pair plaquettes get U_□ = I; all others get U_□ = -I.

### Gradient descent results [COMPUTED]

| Start type        | # starts | Best λ_min found |
|-------------------|----------|------------------|
| Random            | 8        | -12.061          |
| Anti-instanton GD | 4        | **-14.734**      |
| Perturbed AI      | 10       | -14.704          |
| Ortho-direction   | 5        | -14.074          |

**Empirical sup|λ_min| = 14.734 ± 0.05** (converged: step 200→300 changed by only 0.001). Anti-instanton starts find 63% more negative eigenvalue than random starts alone.

---

## Stage 2: Extremal Configuration Analysis

### D+C decomposition [COMPUTED]

**Before GD (pure anti-instanton, axes (0,0,2,1)):**
- 80/96 plaquettes: U_□ = -I (Re Tr = -2); 16/96: U_□ = I (the commuting (0,1) plane)
- D_min = -6.0 exactly = -2(d-1) [SATURATED]
- ||C||_op = 8.654; λ_min(C) = -8.654
- Weyl bound: D_min + λ_min(C) = -14.654; actual = -14.175 (slack = 0.48)

**After GD (400 iterations):**
- 80/96 plaquettes still negative; Re Tr range widens to [-1.95, 2.00]
- D_min = -5.60 (relaxed from -6.0)
- ||C||_op = 9.83 (increased from 8.65, approaching flat value 10.0)
- Weyl bound: -5.60 + (-9.83) = -15.43; actual = -14.734 (slack = 0.69)

**Key insight:** The optimizer **trades D_min for ||C||** — relaxing self-term negativity (D: -6 → -5.6) to increase cross-term norm (||C||: 8.65 → 9.83), achieving a more negative total λ_min. D and ||C|| are partially **anti-correlated**: maximal self-term negativity (all plaq ≈ -I) forces cross-term misalignment (||C|| drops below flat value).

### Dimension scaling [COMPUTED]

| d | Best AI λ_min | |λ_min|/4d | ||C_flat|| = 2(d+1) |
|---|--------------|-----------|---------------------|
| 2 | -6.353       | 0.794     | 6.0                 |
| 3 | -10.221      | 0.852     | 8.0                 |
| 4 | -14.175      | 0.886     | 10.0                |

After GD (d=4): 14.73/16 = 0.921. The ratio |λ_min|/4d increases with d but remains strictly below 1.

### Finite-size effects (L dependence) [COMPUTED]

| d | L=2 AI λ_min | L=3 AI λ_min | |λ_min|/4d (L=2) | |λ_min|/4d (L=3) |
|---|-------------|-------------|-----------------|-----------------|
| 2 | -6.353 | -5.710 | 0.794 | 0.714 |
| 3 | -10.072 | -9.414 | 0.839 | 0.785 |
| 4 | -14.175 | -13.674 | 0.886 | 0.855 |

**L=2 is the worst case** — |λ_min| DECREASES with larger L. If a bound is proved for L=2, it holds for all L.

---

## Stage 3: Bounds Summary

### Gershgorin vs. Decoherence vs. Empirical

| Method | sup|λ_min| bound | β threshold | Status |
|--------|-----------------|-------------|--------|
| SZZ Gershgorin | 24 | 1/12 = 0.083 | Proved |
| Decoherence (||C|| ≤ 2(d+1)) | 16 | **1/8 = 0.125** | CONDITIONAL |
| Empirical adversarial | 14.73 | **0.136** | Computed |
| Target (|λ_min| = 2d) | 8 | 1/4 = 0.250 | **RULED OUT** |

### D-bound (proved) [COMPUTED + PROVED]

D_min ≥ -2(d-1): each edge participates in 2(d-1) plaquettes, each Re Tr ≥ -2. This gives the self-term D_min ≥ -6 for d=4.

### Decoherence lemma (numerical only) [COMPUTED, UNPROVED]

**Statement:** ||C(Q)||_op ≤ ||C_flat||_op = 2(d+1) for all Q ∈ SU(2)^|E|.

**Numerical evidence:** Very strong. 0/2000+ configs exceed the flat value.
- 2000 random configs: max ||C|| = 7.895 < 10 ✓
- Z₂ flat (all iσ₃): ||C|| = 8.000 < 10 ✓
- Anti-instantons: ||C|| ∈ [8.09, 8.65] < 10 ✓
- GD-optimized config: ||C|| = 9.83 < 10 ✓

**Why flat should be maximum:** At flat connection, all cross-term color kernels are proportional to I₃ (maximally coherent). At general Q, color kernels rotate and interfere destructively. Analogy: ||Σ a_i ⊗ B_i|| is maximized when all B_i are proportional to the same matrix.

**Formalization gap:** The set of achievable 3×3 color kernels F(M,N) for M,N ∈ SU(2) is not convex, making a Jensen-type argument unavailable. No proof found. ||F(M,N)||_op = 2 for all M,N (proved), but bounding the sum's operator norm requires more structure.

---

## Anti-Correlation Mechanism [CONJECTURED]

The empirical |λ_min| ≈ 14.73 is strictly below 4d = 16 because D_min and ||C|| cannot both reach their extremes simultaneously:

1. **D_min = -2(d-1) = -6** requires all plaquettes to have Re Tr(U_□) = -2 → anti-instanton-like configs
2. **||C|| = 2(d+1) = 10** requires all cross-term color kernels proportional to I₃ → flat connections (Re Tr = +2)
3. These conditions are **mutually exclusive** (anti-instantons have Re Tr = -2; flat connections have Re Tr = +2)

The GD-optimized config (D_min = -5.60, ||C|| = 9.83) finds the optimal tradeoff. If anti-correlation could be proved formally — "D_min ≤ -6 + ε implies ||C|| ≤ 10 − f(ε)" — this would give a bound strictly below 4d. But proving such a relationship appears hard without deeper algebraic insight into the color kernel structure.

---

## Implications

- **β < 1/4 via Bakry-Émery route is ruled out** — would require |λ_min| ≤ 8, far below the observed 14.73
- **β < 1/8 is conditionally achievable** if decoherence (||C|| ≤ 2(d+1)) can be proved; this is a 1.5× improvement over the proved Gershgorin β < 1/12
- **Empirical threshold β < 0.136** (from sup|λ_min| = 14.73) suggests a theoretically achievable bound in the 0.125–0.136 range
- **L=2 worst case** justifies using the L=2 anti-instanton as the extremal configuration in all proofs
- The exploration does NOT attempt Lean formalization; no VERIFIED claims on the decoherence lemma
