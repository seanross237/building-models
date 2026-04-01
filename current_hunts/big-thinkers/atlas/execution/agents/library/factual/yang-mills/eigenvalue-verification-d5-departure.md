---
topic: Full Hessian eigenvalue computation confirming λ_max = 4β at Q=I; d=5 staggered mode departure
confidence: verified
date: 2026-03-27
source: "yang-mills strategy-002 exploration-009; strategy-003 exploration-004"
---

## Overview

Complete eigenvalue computation of the 192×192 Hessian matrix at Q=I for SU(2) on a 2⁴ lattice, confirming λ_max = 4β exactly under the SZZ convention (S = −(β/N) Σ Re Tr). The staggered mode is verified as an eigenvector with zero residual. **Critical d=5 finding:** the staggered mode is NOT the global maximum eigenvector in d=5 — a larger eigenvalue exists.

## Setup

- L=2, d=4: 16 sites, 64 links, 3 generators/link → 192×192 Hessian
- SU(2) generators: τ_a = iσ_a/2, inner product |A|² = −2Tr(A²)
- Wilson action (SZZ convention): S = −(β/N) Σ Re Tr(U_□) with N=2

## d=4 Results [VERIFIED]

### Maximum Eigenvalue

Under SZZ convention: **λ_max = 4β** (exact to machine precision)

H_norm = λ_max / (48β) = **1/12** ✓

### Full Eigenvalue Spectrum (K matrix, 64×64)

| K eigenvalue (SZZ) | Multiplicity (K) | Multiplicity (H = K⊗I₃) |
|------------------|-----------------|------------------------|
| 0 | 19 | 57 |
| 1β | 12 | 36 |
| 2β | 18 | 54 |
| 3β | 12 | 36 |
| **4β** | **3** | **9** |

The Hessian is positive semi-definite at Q=I. The maximum eigenspace has dimension 9 (3 spatial modes × 3 generators).

### Staggered Mode Verification

| Check | Result |
|-------|--------|
| Rayleigh quotient | **4β** exactly |
| Eigenvector residual ‖Kw − λw‖ | **0.00e+00** (exact) |
| Projection onto max eigenspace | **1.000000** |
| Is staggered in max eigenspace? | **Yes** |

### Hessian Verification Against Finite Differences

Max |H_analytical − H_numerical| = 2.38×10⁻⁶ (h=10⁻⁴), consistent with O(h²) truncation error.

## Random Q Eigenvalue Test [COMPUTED]

5 random SU(2)⁶⁴ configurations (seed=42):

| Trial | λ_max(Q) / β | Exceeds 4β? |
|-------|-------------|-------------|
| 1 | 2.027 | No |
| 2 | 2.139 | No |
| 3 | 2.002 | No |
| 4 | 2.030 | No |
| 5 | 2.043 | No |

All random Q have λ_max ≈ 2β — roughly half the Q=I value. For random Q, the Hessian has negative eigenvalues (not positive semi-definite), unlike at Q=I. Q=I appears to be the worst case.

## Convention Clarification

Two conventions exist in the literature:

| Convention | Action | λ_max at Q=I |
|-----------|--------|-------------|
| S1 (raw) | S = −β Σ Re Tr(U_□) | 8β |
| S2 (SZZ) | S = −(β/N) Σ Re Tr(U_□) | **4β** |

H_norm = 1/12 requires the SZZ convention (S2). The 1/N = 1/2 factor for SU(2) is critical.

## d=5 DEPARTURE [COMPUTED — IMPORTANT FINDING]

L=2, d=5: 32 sites, 160 links, 480×480 matrix.

| Quantity | Value |
|---------|-------|
| λ_max (full Hessian) | **5β** |
| H_norm (actual) | 5/64 ≈ **0.07813** |
| Staggered mode Rayleigh quotient | 4.8β |
| Staggered mode H_norm | 3/40 = 0.075 |
| Staggered mode is eigenvector? | **No** (residual = 0.98) |

**The staggered mode is NOT an eigenvector in d=5 and NOT the global maximum.** The true λ_max = 5β exceeds the staggered mode's Rayleigh quotient of 4.8β. The Fourier proof's tightness condition (N_active = d²/4) fails in d=5 (N_active = 6 ≠ 25/4).

**[S003-E004 UPDATE: Complete d=5 eigenvector characterization]** The d=5 maximum eigenvectors are v_{l(x,μ),a₀} = (−1)^|x| × f(μ) where f ∈ R^5 satisfies **Σ_μ f(μ) = 0** (zero-sum / "traceless"). Eigenspace dimension = d−1 = 4. Simplest examples: f=(1,−1,0,0,0), f=(1,1,−2,0,0), f=(1,1,1,1,−4). Mode C fails at d=5 because f(μ) = (−1)^μ = (1,−1,1,−1,1) has Σf = 1 ≠ 0. General pattern across all d: λ_max = dβ, H_norm = d/48. Maximum eigenspace uses staggered site factor (−1)^|x| × traceless direction vector. Mode C achieves λ_max only for **even d** (where Σ(−1)^μ = 0). Cross-dimensional verification: K Rayleigh = 4d for all zero-sum f at d=2,3,4,5 (overlap = 1.000000 with numerical eigenvectors).

### d=5 Eigenvalue Spectrum

| K eigenvalue | Multiplicity (K) | Multiplicity (H) |
|-------------|-----------------|------------------|
| 0 | 36 | 108 |
| 1β | 20 | 60 |
| 2β | 40 | 120 |
| 3β | 40 | 120 |
| 4β | 20 | 60 |
| **5β** | **4** | **12** |

## Implications

1. The Fourier proof at Q=I is valid and tight in d=4 but gives a weaker (non-tight) bound in d=5.
2. The staggered mode analysis does NOT generalize straightforwardly to d≥5.
3. For d=4, the staggered mode correctly identifies the maximum — this is the physically relevant case for 4D Yang-Mills.
4. The true maximum in d=5 involves a different eigenvector in a 4-dimensional spatial mode space (12 = 4 × 3 generators).
