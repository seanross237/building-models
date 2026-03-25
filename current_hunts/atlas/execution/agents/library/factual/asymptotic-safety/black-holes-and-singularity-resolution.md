---
topic: asymptotic-safety
confidence: provisional
date: 2026-03-25
source: exploration-007-nonperturbative-QGF (strategy-002)
---

# Black Holes and Singularity Resolution in Asymptotic Safety

## RG-Improved Black Holes (Bonanno-Reuter)

The most studied non-perturbative prediction of asymptotic safety. Construction: start with Schwarzschild metric, replace G_0 with running G(k) from the RG flow, identify the RG scale k with a physical scale (proper distance from center).

### The BR Metric (Lapse Function)

    f(r) = 1 - 4G_0 m r^2 / [2r^3 + g*^{-1} xi^2 G_0 (2r + 9mG_0)]

where g* is the fixed-point value of Newton's coupling.

### Key Predictions

- **Singularity resolution:** Central singularity replaced by a regular de Sitter core. G(r) -> 0 as r -> 0, so gravity weakens precisely where it would create a singularity.
- **Two horizons:** Structure resembles Reissner-Nordstrom with inner and outer horizons.
- **Planckian remnant:** Hawking evaporation terminates at a Planck-mass remnant (~10^{-5} g). Temperature T -> 0 at the critical mass, producing a cold, stable remnant.
- **Modified thermodynamics:** Entropy-mass relations differ from Bekenstein-Hawking due to scale-dependent Newton coupling.
- **Modified quasi-normal modes:** For Planckian black holes, QNMs display significant deviations from classical case (multiple papers 2024-2025).

### Recent Developments (2024-2025)

- Bonanno et al. (2024, PRL): Dust collapse in AS produces regular black holes for alpha > 1 (alpha parameterizes the RG running). For alpha <= 1, singularities persist.
- Multiple papers (2025): QNMs, grey-body factors, shadows, and absorption cross-sections for BR black holes.
- Moving from phenomenological RG improvement toward first-principles derivation from the effective action (2025-2026).

## Singularity Resolution: Generic Mechanism

AS provides a generic mechanism: **gravitational anti-screening**. At the non-Gaussian fixed point:

    G(k) = g* / k^2  (for k >> k_Planck)

Gravity *weakens* at high energies. When matter collapses, the effective gravitational coupling decreases as curvatures approach Planck scale, preventing singularity formation.

### Parameterized Results (2025)

    G(epsilon) = G_N / [1 + omega_tilde (G_N^2 epsilon)^alpha]

- For alpha > 1: Complete singularity resolution for ALL spatial curvatures
- For alpha = 1: Incomplete resolution -- singularities can still form
- For alpha < 1: Singularities persist -- inconsistent with AS

**Key finding:** The parameter alpha is directly related to the anomalous dimension of Newton's constant at the fixed point. AS predicts alpha > 1, therefore *predicts* complete singularity resolution.

## Planck-Mass Remnants as Dark Matter

If AS predicts stable Planck-mass remnants from primordial black hole evaporation:
- Primordial BHs with initial mass < 10^9 g would have evaporated by now classically
- In AS, evaporation halts at a Planck-mass remnant (~10^{-5} g)
- Remnants could dominate dark matter density if enough primordial BHs formed
- **Observable signature:** Gravitational wave signal at ~100 Hz (from PBH mergers/formation)
- Recent work (2024, MNRAS): Breakdown of Hawking evaporation opens new mass window for PBHs as dark matter

## Comparison with Perturbative QG+F

The remnant and singularity resolution predictions are **invisible to perturbative QG+F**:
- QG+F gives corrections as a power series in (M_P/M_BH)^2, which diverges for Planckian BHs
- The T -> 0 endpoint requires the full non-perturbative beta-function to all orders
- The specific running G(k) -> g*/k^2 in the UV is a consequence of the Reuter fixed point, not visible in perturbation theory

## Testability

| Prediction | Test | Timescale |
|-----------|------|-----------|
| Planck remnants | PBH dark matter, GW signals (~100 Hz) | 2030s (LISA) |
| Modified QNMs | Planckian BH quasi-normal modes | Theoretical only |
| Absence of complete evaporation | Future BH factory scenario | Far future |

Sources: Bonanno & Reuter (2000); Bonanno et al. (2024, PRL); arXiv:2405.02636; multiple 2025 papers on BR black hole phenomenology
