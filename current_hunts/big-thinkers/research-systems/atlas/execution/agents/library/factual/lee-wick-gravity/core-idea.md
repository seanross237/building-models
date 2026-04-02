---
topic: lee-wick-gravity
confidence: verified
date: 2026-03-24
source: exploration-003-lee-wick-qg-assessment (strategy-002), updating exploration-001-escape-routes-survey
---

# Lee-Wick Quantum Gravity: Status and Relationship to QG+F

## The Meromorphic Loophole

The ghost/d_s=2 no-go theorem (`constraints/structural/ghost-spectral-dimension-no-go.md`) applies to propagators that are entire functions (no poles). Meromorphic propagators — with complex conjugate mass poles — escape the theorem entirely because:

1. The propagator is meromorphic, not entire
2. The extra poles are complex, not on the real axis
3. The Källén-Lehmann representation doesn't apply in its standard form (requires positive spectral density, which Lee-Wick theories violate)

This was the original motivation for Lee-Wick quantum gravity as a potential escape route.

## The Action

The simplest (four-derivative) Lee-Wick QG has the **same action as Stelle's quadratic gravity** (= QG+F):

    S = ∫ d⁴x √(-g) [M_P² R/2 + α R_μν R^μν + β R² + Λ]

Equivalently (using the Gauss-Bonnet identity in 4D):

    S = ∫ d⁴x √(-g) [M_P² R/2 - (1/2f₂²) C²_μνρσ + (1/6f₀²) R² ]

The **six-derivative (super-renormalizable) version** adds R³-type terms, giving UV behavior ~ 1/p⁶ or higher. Modesto's construction with N pairs of complex poles gives UV behavior ~ 1/p^{2(N+1)}.

## Propagator Structure

**Four-derivative (Stelle action):** Propagator decomposes into:
- Spin-2 sector: 1/p² − 1/(p² + M₂²) where M₂ is the massive spin-2 mass
- Spin-0 sector: 1/(p² + M₀²) where M₀ is the massive scalar mass

In this case, M₂² is real and positive → the massive spin-2 is a ghost (same as Stelle gravity).

**Six-derivative and higher:** The masses become complex conjugate pairs M² = m² ± iΓ, giving propagator components:

    𝒢̃(-k²) = -iM² / [(k² + m²)² + M⁴]

This is purely imaginary, driving the need for a specific prescription for how to handle the complex poles.

## Spectral Dimension

For the four-derivative theory (same action as QG+F): **d_s = 2** (propagator ~ 1/p⁴). For the six-derivative version with N pairs of complex poles: d_s depends on the UV propagator behavior. The spectral dimension depends on the ACTION, not the prescription — both Lee-Wick and fakeon prescriptions applied to the same action yield the same d_s.

## The Prescription Problem — RESOLVED

The theory's fate depends entirely on which prescription handles the complex/ghost poles. Four inequivalent prescriptions exist — see `prescription-comparison.md` for details. **The definitive result (Anselmi, Briscese, Calcagni & Modesto 2025, co-authored by the creator of LW QG): only the fakeon/AP prescription is physically viable.**

The CLOP (Lee-Wick) prescription:
- ❌ **Breaks Lorentz invariance** at the quantum level (Nakanishi 1971, confirmed 2025)
- ❌ **Violates unitarity** above the ghost threshold (Kubo & Kugo 2023, confirmed by multiple groups)
- ❌ **Non-Hermitian classical limit** (Anselmi 2022)

See `unitarity-resolution.md` for the 5 independent lines of evidence.

## Relationship to QG+F — CRITICAL FINDING

**Four-derivative LW action + fakeon prescription = QG+F exactly.** Not a distinct theory.

**Six-derivative LW action + fakeon prescription = super-renormalizable QG with fakeons.** This IS distinct from four-derivative QG+F — it's a super-renormalizable cousin. Pros: super-renormalizable (better UV than QG+F, only finitely many divergent diagrams). Cons: more free parameters (masses of additional complex pole pairs), less predictive.

## Super-Renormalizability

In even dimensions, the six-derivative version has only finitely many divergent diagrams. In odd dimensions, the theory is outright finite. This is *better* than QG+F's four-derivative action (which is merely renormalizable). However, this advantage comes at the cost of additional free parameters and applies only to the six-derivative extension, which must itself use the fakeon prescription.

## Research Program Status

~15-25 papers directly on Lee-Wick QG (distinct from the larger Lee-Wick QFT literature in particle physics). Community of ~5-10 active researchers. The program is now **effectively absorbed into the fakeon program** — Modesto (the creator) co-authored the 2025 paper concluding only the fakeon prescription works.

Key trajectory:
- 2015-2016: Modesto & Shapiro propose LW QG. Optimistic claims about CLOP unitarity.
- 2017: Anselmi & Piva reformulate LW QFT, developing the fakeon.
- 2022-2023: Multiple independent groups show CLOP fails unitarity.
- 2025 (March): Anselmi AND Modesto co-author paper: only fakeon is viable. **LW QG as independent program effectively ends.**
- 2025-2026: Remaining work on ghost bound states/resonances yields negative conclusions (Oda 2026).

## Tier 1 Validation

| Criterion | LW/CLOP Prescription | Fakeon Prescription (= QG+F) |
|-----------|---------------------|------------------------------|
| Correct DOF (massless spin-2) | ✅ Graviton is only real pole | ✅ |
| Unitarity | ❌ Violated above threshold | ✅ Proven to all orders |
| Ghost freedom | ❌ Complex ghosts created | ✅ Fakeons purely virtual |
| UV completion | ✅ Super-renorm (6-deriv) | ✅ Renormalizable (4-deriv) |
| Diffeomorphism invariance | ✅ By construction | ✅ |
| Lorentz invariance | ❌ Broken at quantum level | ✅ Preserved |

**With LW/CLOP prescription — FAILS Tier 1 (unitarity AND Lorentz invariance).**
**With fakeon prescription — PASSES Tier 1, but IS QG+F (4-deriv) or a variant (6-deriv).**

## Computation Gaps in the 6-Derivative Extension

- Full two-loop calculations with fakeon prescription
- Explicit cosmological predictions specific to the super-renormalizable version
- Non-perturbative aspects of ghost confinement
- Complete RG flow to low energies with fakeon prescription

## Overall Verdict

**Lee-Wick QG is not a viable independent theory.** With the CLOP prescription it fails unitarity and Lorentz invariance. With the fakeon prescription, the four-derivative version IS QG+F; the six-derivative version is a known super-renormalizable extension with more free parameters but the same leading-order predictions. The program is now effectively absorbed into Anselmi's fakeon framework.

Sources: Modesto (arXiv:1602.02421), Modesto & Shapiro (arXiv:1512.07600), Anselmi & Piva (arXiv:1703.04584, arXiv:1806.03605), Anselmi (arXiv:1704.07728, arXiv:2202.10483), Kubo & Kugo (arXiv:2308.09006), Anselmi+Modesto et al. (arXiv:2503.01841), Oda (arXiv:2602.05562), Buoninfante (arXiv:2501.04097), Asorey et al. (arXiv:2408.16514)
