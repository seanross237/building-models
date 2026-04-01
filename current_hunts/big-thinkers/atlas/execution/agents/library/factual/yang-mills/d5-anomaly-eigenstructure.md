---
topic: d=5 anomaly resolution — λ_max(M(I)) = 4d for ALL d, staggered mode NOT maximizer for odd d
confidence: verified
date: 2026-03-29
source: "yang-mills-validation exploration-006"
---

## Overview

Resolution of the d=5 eigenvalue anomaly: λ_max(M(I)) = 4d for ALL d (verified d=3,4,5,6), with multiplicity d−1. The staggered mode is the maximizer ONLY for even d; for odd d, the maximum eigenvector has direction vector c with Σ_μ c_μ = 0. This corrects the prior formula ⌈d/2⌉⌊d/2⌋/(N²d(d−1)) to the universally correct d/(4(d−1)N²).

## Key Formula: λ_max(M(I)) = 4d `[VERIFIED for d=3,4,5,6]`

| d | λ_max(M) | λ_max(H)/β | Stag eig/β | H_norm | CS threshold β < |
|---|----------|------------|------------|--------|------------------|
| 3 | 12 | 3.000 | 2.667 | 3/32 | 1/4 |
| 4 | 16 | 4.000 | 4.000 | 1/12 | 1/6 |
| 5 | 20 | 5.000 | 4.800 | 5/64 | 1/8 |
| 6 | 24 | 6.000 | 6.000 | 3/40 | 1/10 |

## Even/Odd Dichotomy

Maximum eigenvectors have form v_{x,μ} = c_μ (−1)^|x| with Rayleigh quotient Q(c) = 4[d − (c·1̄)²/|c|²].

Maximum Q = 4d achieved when **Σ_μ c_μ = 0** (c ⊥ 1̄).

**Staggered mode:** c_μ = (−1)^μ, so Σ c_μ = (1 − (−1)^d)/2:
- **Even d:** Σ = 0 → staggered IS maximizer (d=4, d=6)
- **Odd d:** Σ = 1 → staggered BELOW maximum (d=3, d=5)

**d=5 specifically:** Staggered c = (1,−1,1,−1,1) gives Q = 19.2, not 20. Maximum at c = (4,−1,−1,−1,−1) gives Q = 20 = 4d. The max eigenspace is 4-dimensional (d−1 = 4). `[VERIFIED: residual < 10⁻⁸]`

## Formula Correction

The prior mission's formula H_norm = ⌈d/2⌉⌊d/2⌋/(N²d(d−1)):
- **Even d:** gives d²/4 / (N²d(d−1)) = d/(4(d−1)N²) ✓ (matches correct formula)
- **Odd d:** gives (d²−1)/4 / (N²d(d−1)) = staggered mode value ✗ (WRONG — gives staggered eigenvalue, not true max)

**Correct formula for ALL d:** H_norm(I) = d/(4(d−1)N²) = d/(16(d−1)) for N=2.

## Eigenvalue Multiplicities (Pascal-Triangle Structure)

| d | Eigenvalues of M(I) (with multiplicities) |
|---|---------------------------------------------|
| 3 | 12(×2), 8(×6), 4(×6), 0(×10) |
| 4 | 16(×3), 12(×12), 8(×18), 4(×12), 0(×19) |
| 5 | 20(×4), 16(×20), 12(×40), 8(×40), 4(×20), 0(×36) |
| 6 | 24(×5), 20(×30), 16(×75), 12(×100), 8(×75), 4(×30), 0(×69) |

Multiplicity of λ_max: always d−1. Eigenvalues are 4k for k=0,...,d.

## Triangle Inequality Generalizes to All d `[COMPUTED]`

The CS proof is structure-identical for all d ≥ 2. Threshold: β < N²/(8(d−1)) = 1/(2(d−1)) for N=2. The CS bound has increasing slack in higher d (ratio H_norm/H_norm_CS = d/(2(d−1)) → 1/2 as d→∞).
