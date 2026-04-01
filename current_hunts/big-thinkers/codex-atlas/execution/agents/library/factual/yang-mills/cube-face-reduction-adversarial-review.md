---
topic: Cube-face reduction proof for Conjecture 1 — adversarial review verdict CONDITIONAL PASS
confidence: provisional
date: 2026-03-29
source: "yang-mills-conjecture strategy exploration-007; yang-mills-conjecture strategy-002 exploration-006 (independent adversarial review)"
---

## Overview

Independent adversarial review of a 5-step algebraic proof for Conjecture 1 (lambda_max(M(Q)) <= 4d = 16 for all Q on all L). **Verdict: CONDITIONAL PASS.** The core algebraic proof (Steps 1-5) establishing the per-vertex bound lambda_max(M_total) <= 64 on L=2 is **correct** — all identities, the Combined Bound Lemma, and the expansion verified numerically with high precision. However, the chain from this per-vertex bound to the full Conjecture 1 has **two gaps**: (1) the proof only bounds the staggered mode Rayleigh quotient, not the full operator norm, and (2) the proof formula is specific to even L. Both gaps are supported numerically (no violations found) but not closed analytically.

**Verification scorecard: 13 VERIFIED, 5 COMPUTED, 1 CONJECTURED.**

## Proof Structure (Steps 0-5)

**Step 0 — Cube-face reduction:** Partition plaquettes by base vertex (96 plaquettes = 16 vertices x 6 each on L=2). If F_x <= 64|n|^2 for all x, Q, then Sum F_x <= 64 * L^d * |n|^2 = 4d * |v|^2, giving staggered Rayleigh quotient <= 4d. **[VERIFIED]** — partition exact, sum identity |Sum F_x - n^T M_stag n| < 2.3e-13.

**Step 1 — Sign structure:** For each plaquette (mu,nu), 6 cross-term signs determined by ab = (-1)^{mu+nu+1}. Active planes (4): all 6 signs positive. Inactive planes (2): 2 positive, 4 negative. Total: 28 positive, 8 negative, net sigma = 20. c + Tr(P) = 24 + 2*20 = 64. **[VERIFIED]** — enumeration confirmed.

**Step 3 — Expansion:** 64 - n^T M_total n = 2 * [group_02 + group_13 + group_active], where each group collects terms from inactive/active plaquettes with their base-link budgets. **[VERIFIED]** — max |LHS - RHS| < 4.26e-14 over 100,000 tests. All three groups non-negative (min values 0.0007, 0.00009, 4.675 over 100k tests).

**Step 4 — Combined Bound Lemma:** f(A) + f(B) + f(AD) + f(DB^T) - f(D) - f(ADB^T) = n^T(I-A)D(I-B^T)n + f(A) + f(B) >= 0 via Cauchy-Schwarz + AM-GM. **[VERIFIED]** — algebraic identity to 2.66e-15; Cauchy-Schwarz ratio < 0.9999964 over 200k tests; adversarial gradient descent (200 starts, 3000 steps) found no violations.

**Step 5 — Assembly:** Budget-demand allocation correct: active plaquettes provide 2x f(R_mu) per base link; inactive need 1x each. Budget >= demand on standard (4+/2-) sign structure. **[VERIFIED]**

## Gap 1: Staggered Mode != Full Operator — **CLOSED** (S002-E005)

The proof establishes staggered mode Rayleigh quotient <= 16 but does NOT prove lambda_max(M(Q)) <= 16 for the full operator. At Q=I, the 9-dimensional top eigenspace (eigenvalue 16) contains:
- **3 staggered modes** (overlap SVD: 1.0, 1.0, 1.0)
- **6 non-staggered modes** (complex lattice modes not addressed by per-vertex argument)

**E008 investigation:** See `full-eigenspace-gap1-investigation.md`. Per-vertex reduction to 12×12 constrained eigenvalue problem; 110K+ tests, 0 violations (best adversarial: 15.997).

**S002-E005 PROVED the per-vertex bound for all 9D modes** via contraction bound: sum_S ≥ 0 proved using M9 affine in D + Cauchy-Schwarz + cancellation. See `lemma-d-rdr-false-sum-s-nonneg.md` for full proof. **Gap 1 is CLOSED.** Combined with the cube-face reduction (Steps 0-5), this proves the B_□ inequality for even L.

## Gap 2: Odd L Sign Structures (MINOR for physics)

The proof formula A = a(I + R_mu D) + b(R_mu + R_mu D R_nu^T) is specific to **even L**. On L=2 and L=4, all vertices have the same sign structure — verified to < 1.42e-14. On L=3, there are **8 distinct sign structures** (vertices where some coordinate = L-1 = 2 have different parity behavior); max proof formula discrepancy = **31.8** (genuine, not rounding).

Root cause: on even L, (x_mu + 1) mod L always changes parity. On odd L, when x_mu = L-1, (x_mu + 1) mod L = 0 does NOT change parity.

Despite the formula mismatch, the per-vertex bound F_x <= 64 DOES hold numerically on L=3 (max 56.68 over 500 x 81 tests), and lambda_max(full M) <= 14.13 on L=3.

### L=3 Eigenvalue Structure at Q=I (S002-E006) [COMPUTED]

L=3, d=4 full matrix (972×972) at Q=I: eigenvalues = {0(×252), 3(×72), 6(×216), 9(×288), 12(×144)}. **lambda_max = 12.0** (not 16!). Eigenvalue formula: **4d·sin²(π/L) = 16·(3/4) = 12** for L=3 (max momentum at k=2π/3, not k=π). The staggered vector (period-2 pattern) is NOT a single momentum mode at L=3 (period 2 doesn't divide L=3). Random Q (30 tests): max lambda_max = 14.1, 0 violations of 16. The per-vertex bound is even more slack at odd L.

**For the physically relevant limit L -> infinity (through even L), Gap 2 is irrelevant.**

## Full M(Q) Eigenvalue Structure at Identity

**[VERIFIED]** Full 192x192 M(Q) at Q=I:

| Eigenvalue | Multiplicity |
|------------|-------------|
| 0          | 57          |
| 4          | 36          |
| 8          | 54          |
| 12         | 36          |
| 16         | 9           |

Spectrum {0, 4, 8, 12, 16} with total dimension 192. Top eigenspace (dim 9) = 3 staggered + 6 non-staggered modes.

### Momentum Decomposition (S002-E006) [VERIFIED]

The eigenvalues at Q=I correspond to momenta k ∈ {0,π}^4 with **eigenvalue = 4 × (number of π-components)**:

| Momentum class | Eigenvalue | # momenta | Multiplicity |
|---------------|------------|-----------|-------------|
| k = (0,0,0,0) | 0 | 1 | 12 |
| 1 component = π | 4 | 4 | 36 |
| 2 components = π | 8 | 6 | 54 |
| 3 components = π | 12 | 4 | 36 |
| k = (π,π,π,π) | 16 | 1 | 9+3 |

**Key observation:** The non-staggered eigenvalue 12 (from k with 3 π-components) **grows to 14.6** as Q deviates from I. This is NOT constrained by the per-vertex proof, which only bounds the staggered (all-π) subspace.

### Non-Staggered Quantitative Data (S002-E006, 200 random Q) [COMPUTED]

| Quantity | Q=I | Random Q (200 tests) |
|----------|-----|---------------------|
| Staggered eigenvalue | 16.0 | max 9.5, mean 8.4 |
| Non-staggered max eigenvalue | 12.0 | max 14.6, mean 14.1 |
| Full lambda_max | 16.0 | max 14.5, mean 14.1 |
| Top eigenvector staggered projection | 1.0 | 0.19–0.48 |
| Non-stag > stag? | No | **100% of trials** |

For ALL random Q, the top eigenvector is predominantly non-staggered. The per-vertex proof bounds the wrong subspace for non-trivial Q — resolved by S002-E005's contraction bound which covers all 9D modes.

## Relationship to B_□ Inequality Program

This proof represents a specific attack strategy for the same conjecture tracked in `b-square-inequality-proof-progress.md`. The cube-face reduction approach succeeds for staggered modes but requires additional work for the full operator. The per-vertex → staggered → full chain is the key bottleneck. See also `weitzenbock-exact-formula.md` (R(Q)|_P <= 0 approach) and `hnorm-conjecture-numerical-resolution.md` (100+ config numerical support).
