---
topic: constraints/recovery
confidence: verified
date: 2026-03-24
source: exploration-001-structural-recovery-constraints
---

# Post-Newtonian Corrections and PPN Parameters (Constraints B7 / D3 / D4)

**Statement:** The theory must reproduce the correct post-Newtonian expansion of GR, parameterized by the PPN formalism, to within experimental precision.

**Quantitative bounds:**

| Parameter | Bound | Source | Significance |
|-----------|-------|--------|-------------|
| γ (light bending, Shapiro delay) | γ = 1 + (2.1 ± 2.3) × 10⁻⁵ | Cassini (2003) | Still the best bound |
| β (perihelion precession) | |β - 1| < 8 × 10⁻⁵ | Mercury + lunar laser ranging | — |
| GR prediction | γ = β = 1 | — | — |

**Mathematical form (1PN metric):**
- g₀₀ = -1 + 2U - 2βU² + ...
- g₀ᵢ = -(1/2)(4γ + 3 + α₁ - α₂)Vᵢ + ...
- gᵢⱼ = (1 + 2γU)δᵢⱼ + ...

**Restrictiveness: HIGH**

The Cassini bound |γ - 1| < 2.3 × 10⁻⁵ is extremely restrictive for any theory predicting deviations from GR at the post-Newtonian level. Specific implications:
- Constrains Brans-Dicke parameter: ω_BD > 40,000
- Rules out most scalar-tensor theories without screening mechanisms
- Any quantum gravity theory with matter couplings that generate effective scalar-tensor behavior must satisfy these bounds

## Dependency

Derived from the graviton propagator IR matching (B3) — follows from the post-Newtonian expansion of whatever field equations emerge from the quantum theory.
