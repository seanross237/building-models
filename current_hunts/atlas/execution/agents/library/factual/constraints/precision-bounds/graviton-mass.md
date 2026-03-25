---
topic: constraints/precision-bounds
confidence: verified
date: 2026-03-24
source: exploration-001-structural-recovery-constraints
---

# Graviton Mass Bounds (Constraint D1)

**Statement:** The graviton mass must be extremely small or zero.

**Current best bounds:**

| Method | Bound | Source |
|--------|-------|--------|
| CMB (Yukawa potential) | m_g < 5 × 10⁻³² eV | 2024 |
| Large-scale structure | m_g < 4.7 × 10⁻²³ eV/c² (90% CL) | Sept 2024 |
| LIGO-Virgo-KAGRA (GW) | m_g < 1.27 × 10⁻²³ eV/c² | O3 run |
| S-star orbits (Sgr A*) | Improved over previous | 2024 (GRAVITY) |
| Solar System | m_g < 7.2 × 10⁻²³ eV | 2019 |

The CMB-based Yukawa bound is by far the tightest at m_g < 5 × 10⁻³² eV — 2.5 × 10⁸ times tighter than the LIGO bound — though model-dependent.

**Mathematical form:**
- Massive graviton propagator: G(p²) = 1/(p² - m_g²) × [tensor structure with 5 DOF]
- van Dam-Veltman-Zakharov (vDVZ) discontinuity: lim_{m→0} massive propagator ≠ massless propagator. The massive graviton has 5 DOF vs. 2 for massless, and the scalar mode doesn't decouple in the zero-mass limit.

**Restrictiveness: MEDIUM**

Most quantum gravity theories have a massless graviton by construction (diffeomorphism invariance enforces m_g = 0). This constraint primarily restricts massive gravity and bimetric theories.
