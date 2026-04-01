---
topic: unified-qgf-as-framework
confidence: verified
date: 2026-03-26
source: exploration-s4-004-higgs-mass-consistency (quantum-gravity-2 strategy-004)
---

# Higgs Mass Consistency Check: Fakeon Does Not Affect SW Prediction

The unified QG+F–AS framework **inherits the Shaposhnikov-Wetterich Higgs mass prediction unchanged.** The fakeon prescription for the C² ghost does not modify the prediction m_H ≈ 126 ± 3 GeV.

**Classification:** CONSISTENCY CHECK — not a novel prediction; inherited from standalone AS.

## Three Independent Arguments

### 1. UV Divergences Are Prescription-Independent (General QFT Result)

The beta functions are determined by the **real part** of loop integrals. The fakeon prescription modifies only the **imaginary/absorptive part** — it changes how one handles the ghost pole for physical cross sections, but not the UV-divergent part.

UV divergences arise from the **short-distance (high-momentum) regime** where all propagator prescriptions (Feynman, retarded, advanced, fakeon) agree. Prescriptions differ only near the mass shell (p² ≈ m²), which is an IR effect.

**Confirmation:** Anselmi (JHEP 06, 058, 2022) explicitly states that fakeons "disentangle the real part of the self energy from the imaginary part." Beta functions of quadratic gravity are **identical** under fakeon and standard quantization.

### 2. The NGFP Is Euclidean → Prescription-Independent

The FRG (Wetterich equation) operates in **Euclidean signature**. The fakeon prescription is a **Lorentzian** concept modifying the iε contour in Minkowski spacetime. In Euclidean signature there is no iε — propagators are real.

**Therefore:** The NGFP, the gravitational anomalous dimension A_λ, and the boundary condition λ(M_Pl) ≈ 0 are **all identical** regardless of how the ghost is quantized in Lorentzian signature.

Confirmed by D'Angelo et al. (2025, PRD 111, 106007): foliated AS showing Euclidean and Lorentzian NGFP belong to the same universality class.

### 3. Absorptive Part Vanishes Below Threshold (Kinematic Suppression)

At the ghost mass threshold M₂ ≈ 1.42 M_Pl, the matching condition could in principle depend on the prescription. However:

- The logarithmic and power-divergent parts are prescription-independent
- The imaginary part (the ONLY part affected by the fakeon) is proportional to θ(p² − 4M₂²)
- For the Higgs sector at the EW scale: p² ~ (125 GeV)² << M₂² ~ M_Pl² → θ = 0 **exactly**
- The ghost is far too heavy to contribute absorptively at the EW scale

## Quantitative Upper Bound

**At one loop:** Δλ_H(EW) = 0 exactly from the fakeon modification (no on-shell ghost pair production).

**At two loops:** Subdivergences suppressed by (m_H/M₂)² ≈ (125/10¹⁸)² ≈ 10⁻³² — utterly negligible.

**At the NGFP:** Δλ_H = 0 exactly (Euclidean FRG is prescription-independent).

**Conservative upper bound:** In the perturbative regime below the NGFP, f₂ runs to small values (asymptotically free). At scales where perturbation theory is valid (μ ~ 10¹⁵ GeV), f₂ ~ 10⁻² or smaller:

    |Δλ_H| ~ (10⁻²)⁴/(16π²) ~ 10⁻¹¹
    |Δm_H| ~ v² × 10⁻¹¹ / m_H ~ 10⁻⁷ GeV

This is **six orders of magnitude below** experimental uncertainty (±0.17 GeV) and **seven orders below** the theoretical uncertainty from m_top (±3 GeV).

## Comparison of Uncertainty Sources

| Source of uncertainty | |Δm_H| (GeV) | Relative to measurement |
|-----------------------|-------------|------------------------|
| Top quark mass (m_top) | ~3 | ~18× experimental error |
| Strong coupling (α_s) | ~1 | ~6× experimental error |
| Higher-loop SM corrections | ~0.5 | ~3× experimental error |
| Gravitational A_λ value | ~0 (sign only) | N/A — structural |
| **Fakeon prescription** | **< 10⁻⁷** | **< 10⁻⁶ × experimental error** |

## Structural Robustness: The "Topological" Nature of SW

The SW mechanism depends only on the **SIGN** of A_λ, not its value. For any A_λ > 0, the UV-attractive fixed point at λ = 0 pulls all trajectories to λ(M_Pl) ≈ 0. The prediction is "topological" — it depends on fixed-point structure (which eigenoperators are relevant/irrelevant) rather than numerical anomalous dimensions.

## The C² Ghost Is Already Implicit in AS

Even within standard AS (without explicit fakeon quantization), the C² term and its ghost mode are present:
- Benedetti et al. (2009): g₃* = −0.0050 (C² coupling at NGFP)
- Ghost mass at NGFP: m₂ ≈ 1.42k (from exploration s4-001)
- The FRG flow integrates over all modes including the ghost-like one

The question is not "does the C² ghost contribute?" (it does, within the FRG) but "does the fakeon prescription change HOW it contributes?" Answer: **NO** — the FRG is Euclidean, where prescriptions are indistinguishable.

## Eichhorn-Held Refinements Also Unaffected

The same three arguments apply to:
- **Top mass prediction** (m_top ≈ 171 GeV, Eichhorn-Held PLB 777, 2018): gravitational parameters f_y, f_λ computed from Euclidean FRG, prescription-independent
- **Dark portal extension** (Eichhorn et al. JHEP 10, 2021): same reasoning

## Residual Open Questions

1. **Non-perturbative Lorentzian effects:** If the Wick rotation is obstructed, the Lorentzian NGFP might differ from Euclidean. This would be an AS issue, not specifically a fakeon issue.
2. **Higher-loop threshold corrections:** Suppressed by f₂⁴/(16π²)² ~ 10⁻⁵ even with f₂ ~ 1, and further by running of f₂.
3. **Precise A_λ in higher-derivative truncations:** While SIGN is robust, value in C²-extended truncations remains to be computed (Dona-Eichhorn-Percacci 2014 used Einstein-Hilbert only).

**Key open calculation:** Compute A_λ for the Higgs quartic coupling in the **C²-extended FRG truncation**. If A_λ remains positive, the SW prediction is confirmed in the higher-derivative setting. This is an AS truncation question, not a fakeon question.

Sources: Shaposhnikov & Wetterich (2010, PLB 683, 196); Eichhorn & Held (2018, PLB 777); Anselmi (2022, JHEP 06, 058); Benedetti et al. (2009, arXiv:0901.2984); D'Angelo et al. (2025, PRD 111, 106007); Salvio & Strumia (2014, JHEP 06, 080); Dona, Eichhorn & Percacci (2014, PRD 89, 084035); exploration-s4-004
