---
topic: EFT-hedron — computational verification of positivity bounds
confidence: verified
date: 2026-03-27
source: "amplituhedron strategy-001 exploration-006; Arkani-Hamed, T.-C. Huang, Y.-T. Huang arXiv:2012.15849 JHEP 2021; Adams, Arkani-Hamed, Dubovsky, Nicolis, Rattazzi hep-th/0602178 (2006)"
---

## Overview

Computational verification of the EFT-hedron positivity bounds (see `eft-hedron-positivity-constraints.md` for the conceptual overview). Four stages of numerical computation: spectral density models, forward limit bounds, Hankel matrix bounds, and photon-photon (Euler-Heisenberg). All bounds verified against analytic expectations and published results. **Full success on all four stages.**

---

## Stage 1: Spectral Density Models

Three physical UV spectral density models were implemented:
1. **Narrow Breit-Wigner resonance** — Im M(s,0) = Lorentzian × θ(s − s_thr); threshold critical near resonance peak (not at s=0).
2. **Power-law continuum** — Im M(s,0) ∝ (s/M²−1)^α × θ(s−M²) for α<1.
3. **Delta-function resonance** — exact analytic limit for a single heavy particle.

**Implementation note:** BW threshold must be set near the resonance peak (s_thr = (M_res − 5Γ)²), not at 0. Setting it to 0 is a physics bug: it introduces unphysical absorptive strength below the resonance. Explorer caught this via the "unphysical" test: the moments g_{n,0} came out wrong in scale before the bug was fixed.

**Numerical verification of BW model** (M_res = 2.0, Γ = 0.005×M_res):
- Im M(s,0) ≥ 0 at all 1000 sample points (confirmed)
- Integral = 152.84 (analytic: 16π² = 157.91; 3.2% deficit from finite threshold)
- Peak at s ≈ 4.02 (expect M_res² = 4.00; 0.5% error)

---

## Stage 2: Forward Limit Bounds

**g_{n,0} ≥ 0 for n = 2, ..., 8 — computed and verified.**

The dispersive representation: g_{n,0} = (1/π) ∫ Im M(s,0) / s^{n+1} ds is a moment of a positive measure, so the bound follows immediately from unitarity (Im M ≥ 0).

| Model | g_{2,0} | g_{3,0} | g_{4,0} | All ≥ 0? |
|-------|---------|---------|---------|---------|
| Single resonance (M_res=2) | 7.495e−01 | 1.873e−01 | 4.684e−02 | ✓ YES |
| Two resonances (M1=1.5, M2=3) | 4.228e+00 | 1.872e+00 | 8.320e−01 | ✓ YES |
| Power-law continuum (α=0.5) | 1.250e−01 | 6.249e−02 | 3.906e−02 | ✓ YES |
| Ghost (negative spectral density) | −7.495e−01 | −1.873e−01 | −4.684e−02 | ✗ VIOLATION |

**Ratio check**: g_{3,0}/g_{2,0} = 0.2499 ≈ 1/M_res² = 0.25 (single resonance); confirms dispersive formula is self-consistent.

**EFT series convergence**: At s = 0.1 (expansion parameter s/M_res² = 0.025), each successive term is ~25× smaller. Series converges rapidly, validating the EFT expansion region.

**Analytic vs. numerical**: For narrow BW, ratio = 0.953–0.957 (constant 4.5% offset from finite resonance width vs. perfect delta function). All ratios consistent — validates dispersive implementation.

---

## Stage 3: Hankel Matrix Bounds

**Hankel positivity bounds** arise from the Hamburger moment problem: the moments m_k = g_{k+2,0} are moments of a positive measure, so the Hankel matrix H_{ij} = m_{i+j} is PSD.

### Physical Interpretation

The n×n Hankel PSD condition is equivalent to: the EFT data g_{2,0}, ..., g_{2n−2,0} can be reproduced by at least **n distinct** heavy particles.
- det(H_2) ≈ 0: minimal UV completion requires ONE heavy particle
- det(H_2) > 0: UV completion requires at least TWO distinct heavy states
- det(H_3) > 0: UV completion requires at least THREE distinct heavy states

### Numerical Results

**Single resonance** (M_res = 2.5, Γ = 0.013):
- det(H_2) = 4.76e−07 (≈ 0; normalized = 1.23e−05)
- Saturation ratio g_{3,0}/√(g_{2,0}·g_{4,0}) = **0.999760** (analytic = 1.000000; 0.024% error from finite width)

**Two resonances** (M1 = 1.5, M2 = 3.0):
- det(H_2) = **9.417e−03** > 0 (strict inequality confirmed)
- det(H_3) = 2.307e−07 > 0
- Saturation ratio = 0.998664 < 1

**Full PSD check:**
```
Single resonance M_res=2.5:
  H_1: det=+1.97e−01  min_eig=+1.97e−01  [PSD ✓]
  H_2: det=+4.76e−07  min_eig=+2.36e−06  [PSD ✓]
  H_3: det=+8.75e−16  min_eig=+1.69e−09  [PSD ✓]

Two resonances M1=1.5, M2=3.0:
  H_1: det=+4.24e+00  [PSD ✓]
  H_2: det=+9.42e−03  min_eig=+1.86e−03  [PSD ✓]
  H_3: det=+2.31e−07  min_eig=+1.79e−05  [PSD ✓]

Ghost resonance:
  H_1: min_eig=−7.52e−01  [NOT PSD ✗]
  H_2: min_eig=−7.99e−01  [NOT PSD ✗]
  H_3: min_eig=−8.01e−01  [NOT PSD ✗]
```

### Analytic Formula Verification

For two delta resonances, the exact analytic formula:
```
det(H_2) = (16π)² × A × B × (M₁² − M₂²)² / (M₁ M₂)^{10}
```

**[VERIFIED to machine precision]** For M1=2, M2=3:
- Numerical = 1.044641e−03
- Analytic = 1.044641e−03
- Agreement: **0.000000%**

### Saturation Scan (Novel Physical Insight)

Saturation ratio g_{3,0}/√(g_{2,0}·g_{4,0}) vs. mass ratio M2/M1:

| M2/M1 | Saturation ratio | Interpretation |
|-------|-----------------|---------------|
| 1.01 | 0.999951 | nearly degenerate → near saturation |
| 1.25 | 0.987738 | maximum deviation from saturation |
| 1.50 | 0.987543 | both resonances contributing equally |
| 3.90 | 0.999876 | heavy second resonance → near saturation |
| 8.00 | 0.999998 | second resonance irrelevant → effectively single |

**Physical insight**: The saturation ratio is non-monotonic in M2/M1 — it is closest to 1 (single-resonance behavior) for nearly-degenerate (M2→M1) and very-heavy second resonances (M2→∞), and most deviated (~0.988) at M2/M1 ≈ 1.25–1.5. This is a fingerprint: measuring g_{n,0} from an EFT can discriminate between single-resonance and two-resonance UV completions.

---

## Stage 4: Photon-Photon (Euler-Heisenberg)

**Euler-Heisenberg Lagrangian** (1-loop QED, below m_e):
```
L = −(1/4)F² + c₁(F_{μν}F^{μν})² + c₂(F_{μν}F̃^{μν})²
```
where c₁ = 4α²/(90 m_e⁴) and c₂ = 7α²/(90 m_e⁴), giving ratio c₂/c₁ = 7/4.

**Computed values** (α = 1/137.036, m_e = 0.511 MeV):
```
c₁ = 3.471 × 10⁷ GeV⁻⁴
c₂ = 6.074 × 10⁷ GeV⁻⁴
c₂/c₁ = 1.7500 [exact match to 7/4]
```

**EFT-hedron bounds satisfied:**
```
c₁ + c₂ = 9.545 × 10⁷ GeV⁻⁴ ≥ 0  ✓
c₁       = 3.471 × 10⁷ GeV⁻⁴ ≥ 0  ✓
c₂       = 6.074 × 10⁷ GeV⁻⁴ ≥ 0  ✓
4c₁c₂   = 8.434 × 10¹⁵ GeV⁻⁸ ≥ 0  ✓
```

**Violation test** — setting c₁ → −c₁: both the c₁ ≥ 0 and 4c₁c₂ ≥ 0 bounds violated. Confirms any EFT with c₁ < 0 is not UV-completable.

**Allowed region**: Systematic scan confirms allowed region = first quadrant c₁ ≥ 0 AND c₂ ≥ 0 (both conditions independently necessary). QED sits in the allowed region; no hypothetical EFT type with c₁ < 0 or c₂ < 0 is UV-completable.

---

## Summary of Key Numerical Results

| Quantity | Value | Status |
|----------|-------|--------|
| g_{2,0} single resonance M=2 | 7.495e−01 | [COMPUTED] |
| g_{3,0}/g_{2,0} | 0.2499 ≈ 1/M² | [COMPUTED ✓] |
| det(H_2) single resonance | 4.76e−07 ≈ 0 | [COMPUTED] |
| det(H_2) two resonances | 9.42e−03 > 0 | [COMPUTED] |
| det(H_2) analytic formula | 0.000000% error | [VERIFIED] |
| c₁ Euler-Heisenberg | 3.471e+07 GeV⁻⁴ | [COMPUTED] |
| c₂/c₁ Euler-Heisenberg | 1.7500 = 7/4 | [COMPUTED ✓] |
| Saturation ratio (2-resonance min) | 0.988 at M2/M1≈1.25 | [COMPUTED] |

---

## Limitations

1. **Non-forward bounds not implemented** — full EFT-hedron includes bounds from t≠0. Only forward-limit subsector computed here.
2. **Crossing symmetry not fully imposed** — for crossing-symmetric amplitudes, additional linear relations between g_{p,q} exist; not enforced here.
3. **Two-sided bounds not computed** — for crossing-symmetric theories, some g_{p,q} acquire two-sided bounds.
4. **Graviton EFT sector not fully implemented** — requires helicity-2 partial waves; discussed but not numerically computed.
