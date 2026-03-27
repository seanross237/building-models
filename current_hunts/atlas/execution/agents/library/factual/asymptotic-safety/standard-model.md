---
topic: asymptotic-safety
confidence: verified
date: 2026-03-22
source: https://www.frontiersin.org/journals/astronomy-and-space-sciences/articles/10.3389/fspas.2018.00047/full
---

# Asymptotic Safety and Standard Model Compatibility and Predictions

A critical question for asymptotic safety is whether the gravitational fixed point survives in the presence of realistic matter content. Substantial evidence indicates compatibility with the Standard Model, and the framework generates specific particle physics predictions.

## Matter Field Bounds

Dona, Eichhorn, and Percacci (Phys. Rev. D 89, 084035, 2014) showed that within the Einstein-Hilbert truncation:

- For a given number of vector fields, there is an **upper bound** on the number of scalar and fermion fields compatible with asymptotic safety (positive Newton coupling at the fixed point).
- The **Standard Model** field content (12 vector bosons, 45 Weyl fermions, 4 real scalars) is compatible with the fixed point.
- Extensions with right-handed neutrinos, an axion, and simple dark matter models (single scalar) are also compatible.
- However, extensions with large numbers of additional scalars or fermions are severely constrained.

## Higgs Boson Mass Prediction (Shaposhnikov-Wetterich 2009)

Mikhail Shaposhnikov and Christof Wetterich published "Asymptotic safety of gravity and the Higgs boson mass" (arXiv:0912.0208, Physics Letters B 683:196-200, 2010) making a specific prediction for the Higgs boson mass based on asymptotic safety.

### Key Assumptions
1. The Standard Model plus gravity is valid up to arbitrarily high energies
2. There are no intermediate energy scales between the Fermi and Planck scales
3. Gravity is asymptotically safe

### The Mechanism

At scales above the Planck mass, gravity contributes an anomalous dimension A_λ to the Higgs quartic coupling. The modified beta function:

    β_λ = β_λ^SM + A_λ · λ

**For A_λ > 0 (favored by explicit AS calculations):** The fixed point at λ = 0 becomes UV-attractive. This provides a boundary condition λ(M_Pl) ≈ 0. Running down to the electroweak scale using SM RG equations uniquely determines m_H = m_min ≈ **126 GeV**.

**Why 126 GeV specifically:** λ(M_Pl) ≈ 0 corresponds to the minimum Higgs mass consistent with vacuum stability — the boundary between stability and metastability. The observed SM near-criticality is not accidental but follows from the AS boundary condition.

**For A_λ < 0:** The window opens: 126 < m_H < 174 GeV. Less predictive.

### The Prediction
This yields m_H = m_min = **126 ± 3 GeV**, with uncertainty dominated by the top quark mass and strong coupling constant.

**Uncertainty budget:**
- **Top quark mass (m_top):** Dominant. δm_H ≈ 1 GeV per 1 GeV shift in m_top. The original prediction uses m_top ≈ 171 GeV; current world average m_top = 172.57 ± 0.29 GeV pushes the predicted value slightly higher (125–132 GeV range depending on exact m_top).
- **Strong coupling (α_s):** Enters through QCD corrections to top Yukawa running. Subdominant but non-negligible (~1 GeV effect).
- **Higher-loop SM corrections:** ~0.5 GeV.
- **Gravitational parameters:** ~0 (only sign of A_λ matters — structural/topological prediction).

### Significance
This prediction was made in 2009, **three years before** the Higgs was discovered at 125.1 GeV at the LHC in July 2012. It is arguably the most impressive predictive success of the AS/QG+F program and the only confirmed particle physics prediction from any quantum gravity framework.

### Robustness
The prediction is remarkably robust: independent of details of UV running (only the sign of A_λ matters), holds for a "wide class of extensions of the SM." Only requires the big desert assumption (no new physics between Fermi and Planck scales). The prediction is "topological" — it depends on the fixed-point structure (which eigenoperators are relevant/irrelevant) rather than numerical values of anomalous dimensions.

**Important:** The mechanism was formulated in the **Einstein-Hilbert truncation** of AS. It does not explicitly include higher-derivative terms (C², R²). The anomalous dimension A_λ is computed from the NGFP in the Einstein-Hilbert sector. Higher-derivative truncations with full matter coupling remain to be computed (Dona-Eichhorn-Percacci 2014 confirmed NGFP survival with SM content in E-H truncation only).

### Fakeon Compatibility (Exploration s4-004)

The unified QG+F–AS framework inherits the SW prediction **unchanged**. The fakeon prescription for the C² ghost does not affect the prediction: (1) UV divergences / beta functions are prescription-independent, (2) the NGFP is an Euclidean computation where prescriptions are indistinguishable, (3) threshold corrections at M₂ ~ M_Pl have absorptive parts that vanish at the EW scale (kinematic suppression by (m_H/M_Pl)²). Conservative bound: |Δm_H| < 10⁻⁷ GeV. See `../cross-cutting/unified-qgf-as-framework/higgs-mass-consistency.md` for the full analysis.

### Connection to QG+F
The Higgs mass prediction is a **non-perturbative** AS result. In perturbative QG+F, gravity corrections to λ_H are suppressed by (μ/M_Pl)² — far too small to drive λ → 0. QG+F is consistent with the prediction (same theory, different regime) but cannot derive it perturbatively. Analogous to perturbative QCD not deriving the proton mass.

## Top Quark Mass Prediction

- The top Yukawa coupling becomes an irrelevant direction at the gravitational fixed point, making the top quark mass predictable.
- For Higgs mass ~ 125 GeV, the predicted top quark mass is approximately 171 GeV, consistent with experimental measurements.
- Source: Eichhorn and Held, arXiv:1707.01107

## Conformal Standard Model Extension

Grabowski et al. (arXiv:1810.08461) explored the Conformal Standard Model supplemented with asymptotically safe gravity:
- Predicted second scalar particle mass: approximately 300 GeV
- Predicted heavy neutrino masses: approximately 340 GeV
- These predictions are described as "explicitly testable in the nearby future"

## Asymptotically Safe Grand Unification

One of the most interesting connections between AS and particle physics:

1. **α_em calculability (Eichhorn, Held & Wetterich 2018, Phys. Lett. B 782):** The balance of gravity and matter fluctuations at the UV FP determines a fixed-point value α* of the unified gauge coupling. Running down to low energies could in principle predict α_em ≈ 1/137. Current computational uncertainties are too large for a sharp prediction.

2. **Predictive GUT scalar potential (Eichhorn & Held 2020, JHEP 08, 111):** In asymptotically safe grand unification, the UV FP determines ALL quartic couplings of the GUT scalar potential. GUT scale, proton lifetime, and scalar spectrum become calculable predictions rather than free parameters.

3. **Asymptotic grand unification (2025, JHEP 08, 042):** SO(10) with one extra dimension — gauge couplings reach non-trivial UV FP, providing alternative to traditional grand unification.

## SM Near-Criticality

The measured Higgs mass (125.1 GeV) and top mass (172.7 GeV) place the SM vacuum almost exactly at the stability/instability boundary. This near-criticality is **explained** by the Shaposhnikov-Wetterich AS boundary condition (λ → 0 at UV FP) — it is a prediction, not an accident.

## Gravity-Matter Coupling

Gravitational quantum fluctuations can:
1. Support asymptotic freedom in gauge couplings (or leave them unchanged at leading order)
2. Drive the Yukawa couplings toward fixed-point values
3. Render the Higgs quartic coupling irrelevant, constraining it

## Robustness

Kotlarski, Kowalska, Rizzo, and Sessolo (arXiv:2304.08959) systematically examined uncertainty sources in asymptotic safety predictions for particle physics, analyzing the gauged B-L model and the leptoquark S_3 model. Studies show predictions carry systematic uncertainties from truncation, loop order, and the definition of the Planck scale threshold.

Sources:
- https://www.frontiersin.org/journals/astronomy-and-space-sciences/articles/10.3389/fspas.2018.00047/full
- https://arxiv.org/abs/0912.0208
- https://arxiv.org/abs/1707.01107
- https://arxiv.org/abs/1811.11706
- https://arxiv.org/abs/2304.08959
