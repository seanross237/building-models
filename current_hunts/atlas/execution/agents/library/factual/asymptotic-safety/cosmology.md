---
topic: asymptotic-safety
confidence: verified
date: 2026-03-25
source: https://cerncourier.com/a/a-safe-approach-to-quantum-gravity/, exploration-007-nonperturbative-QGF (strategy-002)
---

# Asymptotic Safety: Cosmological and Physical Applications

## Inflation Without an Inflaton

A distinctive non-perturbative prediction of AS: inflation driven purely by quantum gravitational effects at the Reuter fixed point -- no inflaton field needed.

### Mechanism

Near the Reuter fixed point, all couplings run. The effective cosmological constant is large (~M_P^4), driving exponential expansion. As the universe expands and cools, the RG flow moves away from the fixed point toward the GR regime, ending inflation naturally.

The cosmological constant at the fixed point lambda* ~ 0.3 is O(1), but flows to its tiny observed value lambda ~ 10^{-122} in the IR. This provides a *trajectory* connecting UV and IR, though it does not solve the CC problem (why this particular trajectory is selected).

### Specific Predictions (Different from QG+F/Starobinsky)

- QG+F gives Starobinsky inflation with n_s ~ 0.967, r in [0.0004, 0.0035] from the R^2 term
- AS inflaton-free inflation predicts: n_s from the fixed-point anomalous dimensions, r up to ~0.01
- The transition scale epsilon_c from the Reuter fixed point to classical GR is a new parameter constrained by CMB
- Nearly scale-invariant primordial spectrum (from near-fixed-point behavior)
- The smallness of the R^2 coupling required for CMB normalization is *naturally* ensured by its vanishing at the UV fixed point

### Emergent Cosmological Model from Running G (Bonanno et al. 2024)

Bonanno et al. (PRD 111, 103519, 2025; arXiv:2405.02636) derive a complete cosmological model:
- G(epsilon) = G_N / (1 + epsilon/epsilon_c) where epsilon_c is a critical energy density
- Universe naturally enters a quasi-de Sitter phase at early times
- Flatness and horizon problems solved without inflaton
- Primordial power spectrum: nearly scale-invariant, constrained by CMB data
- Key prediction: epsilon_c encodes the Reuter fixed point value g* = 540pi/833
- **Testable:** The transition scale epsilon_c can be constrained by CMB measurements

### Discriminating Test: Tensor-to-Scalar Ratio

If AS inflation gives r ~ 0.01, this is ~3x larger than QG+F's prediction -- distinguishable by next-generation experiments. If r < 0.004 is confirmed, this would *rule out* the simplest AS inflation models while being consistent with QG+F.

## Gravitational Vacuum Condensate and Running G at Cosmological Scales

### Hamber's Lattice Gravity Results

The Regge-Wheeler lattice path integral formulation reveals a nontrivial gravitational vacuum condensate (Hamber, arXiv:1707.08188; Symmetry 11(1), 87, 2019) -- analogous to the gluon and chiral condensates in QCD:
- Critical exponent nu ~ 1/3 (conjectured universal)
- A nonperturbative scale xi, directly analogous to Lambda_QCD

### Running of Newton's Constant at Large Distances

    G(r) = G_0[1 + c_0(l_P/xi)^{1/nu} + c_1(r/xi)^{1/nu} + ...]

where xi ~ 1/sqrt(Lambda) is the gravitational correlation length. This predicts deviations from GR at distances comparable to the Hubble radius.

The running is **power-law** (not logarithmic), which is qualitatively different from perturbative QG+F. Perturbative running (Exploration 005) gives Delta_theta/theta ~ 10^{-14}; the non-perturbative condensate running could be potentially observable.

### Testability

- Precision tests of gravity at cosmological scales (modified expansion history)
- Deviations from LCDM in large-scale structure
- Running of effective Newton constant measurable via CMB + BAO + type Ia supernovae
- Future high-precision satellite experiments

## What Perturbative QG+F Cannot Reproduce

The non-perturbative sector makes at least 4 predictions invisible to perturbative QG+F:

| Prediction | Non-Perturbative Source | Testable? | Timescale |
|-----------|----------------------|-----------|-----------|
| Planck remnants | BR black holes from RG improvement | Via PBH dark matter, GW | 2030s (LISA) |
| Running G at cosmic scales | Vacuum condensate (Hamber) | Precision cosmology | 2030s |
| Inflation without inflaton | Reuter fixed point | r ~ 0.01 vs r ~ 0.003 | 2030s (CMB-S4) |
| Higgs mass prediction | SM at the fixed point | Already confirmed (125 GeV) | Done |

## Connections to Particle Physics

The Reuter fixed point may provide a unified description of all forces:
- Profound consequences for physics inside black holes
- Predictions for SM parameters (Higgs mass, top quark mass; see `standard-model.md`)
- Constraints on BSM physics
- Specific relations between coupling constants testable via particle physics

Research has progressed from theoretical foundations toward empirical testing, becoming "an observationally guided endeavour."

## Textbook Reference

Martin Reuter and Frank Saueressig: "Quantum Gravity and the Functional Renormalization Group: The Road towards Asymptotic Safety" (Cambridge Monographs on Mathematical Physics).

Sources: CERN Courier; Bonanno et al. (2024/2025, PRD 111, 103519; arXiv:2405.02636); Hamber (arXiv:1707.08188; Symmetry 11(1), 87, 2019); Shaposhnikov & Wetterich (2010)
