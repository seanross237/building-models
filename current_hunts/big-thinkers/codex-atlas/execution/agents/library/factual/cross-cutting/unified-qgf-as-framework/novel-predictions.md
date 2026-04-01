---
topic: unified-qgf-as-framework
confidence: provisional
date: 2026-03-26
source: exploration-007-unified-framework (quantum-gravity-2 strategy-003)
---

# Novel Predictions of the Unified QG+F--AS Theory

Predictions that emerge **only** from combining QG+F and AS -- neither framework alone produces them.

## 1. Average Continuation Resolves AS's Wick Rotation Problem

**Prediction:** The correct analytic continuation for AS calculations is Anselmi's average continuation, not the standard Wick rotation.

- QG+F alone has the average continuation but no non-perturbative physics
- AS alone has the Wick rotation problem but no resolution
- Unified framework provides both: average continuation (from QG+F) applied to the FRG (from AS)

**How to test:** Compute a physical observable (e.g., scattering amplitude, spectral function) using both average continuation and standard Wick rotation within AS. The natural test observable is the spin-2 sector of the graviton propagator.

**Important caveat:** Baldazzi, D'Angelo, Knorr (2025, PRD 111, 106007) show that "Foliated Asymptotically Safe Gravity" achieves Euclidean↔Lorentzian agreement using analytic continuation of the lapse function, and the resulting Lorentzian two-point function has the causal structure of the **Feynman propagator** (not the fakeon/average continuation). If Lorentzian AS works without the average continuation, this prediction may be **rendered moot**. Estimated difficulty: 6–12 months for an expert.

See `../qgf-vs-as-analyticity-compatibility.md` for the compatibility analysis; `./discriminating-predictions.md` for the full discrimination assessment.

## 2. Ghost Confinement Scale = Planck Mass (Dynamically Generated)

**Prediction:** Lambda_ghost = M_P, dynamically generated, not a free parameter.

- Perturbative (QG+F): ghost mass m_2^2 = M_P^2/(2 alpha_W), set by Weyl-squared coupling
- Non-perturbative (AS): NGFP anomalous dimension eta_N = -2 controls running; G(k) = g_*/k^2; ghost mass scales as mu^2 = k^2/y* (Becker et al. 2017)

**Why novel:** In QG+F alone, m_2 is a free parameter (constrained only by m_chi > m_phi/4). In AS alone, there is no ghost to confine. In the unified theory, m_2 is fixed by the RG flow connecting AF and NGFP regimes.

**Consequence:** The Planck scale is special because it is the gravitational analog of Lambda_QCD -- the ghost confinement scale.

## 3. Black Hole Evaporation Phase Transition

**Prediction:** BHs undergo a perturbative-to-non-perturbative phase transition during Hawking evaporation:

**Phase I (M >> M_P):** Standard Schwarzschild evaporation. QG+F valid. Ghost = fakeon. Tiny O(M_P^2/M^2) corrections.

**Phase transition (M ~ M_P):** At M_crit = **0.308 M_P** (m₂ = 1.42 M_P convention) or **1.55 M_P** (m₂ = 1.42 M̄_P convention), Schwarzschild becomes linearly unstable (Bonanno et al. 2025, r_H ≈ 0.876/m₂). Hawking temperature at transition: T_crit ≈ 0.03–0.13 M_P (convention-dependent). **Convention choice is the largest systematic uncertainty.**

**Phase II (M < M_P):** Non-perturbative AS regime. Bonanno-Reuter metric with regular de Sitter core. Hawking temperature drops. Evaporation halts at Planck-mass remnant (~0.46 M_P, T -> 0).

**Transition order:** By QCD analogy — first-order for pure gravity (supported by CDT A–C transition), likely crossover for gravity + SM matter (~100 DOF explicitly break gravitational "center symmetry" analog, softening the transition). This prediction is unique to the unified framework; AS alone doesn't address transition order.

**M_rem vs M_crit ordering:** If M_rem > M_crit (standard convention), the AS transition preempts the ghost trigger (analogous to QCD confinement before Landau pole). If M_crit > M_rem (reduced convention), the ghost instability IS the physical trigger — the stronger scenario.

**Why novel:** QG+F alone cannot describe the evaporation endpoint. AS alone has no sharp reason for the transition or its order. The unified theory identifies the ghost confinement scale as the physical trigger.

**Observable consequences:**
- PBHs with initial mass < 5 × 10¹¹ kg leave Planck-mass remnants — but γ-ray constraints (β < 10⁻²⁵) preclude remnants being ALL of dark matter
- Remnant detection possibly via femtolensing, GW detectors (>2040)
- Heat capacity divergence at T_max produces characteristic burst then cooling

**Honest caveat:** 7 of 12 detailed predictions are inherited from AS alone. The novelty is real but narrow: trigger mechanism + specific numerical values + transition order. All novel predictions involve unobservable Planck-scale physics.

See `./bh-phase-transition-predictions.md` for full quantitative predictions, classification table, and honest assessment. See `../qgf-vs-as-bh-compatibility.md` for the underlying compatibility analysis.

## 4. Sharpened Inflationary Predictions (Unified r Formula)

**Prediction:** The unified theory constrains r more tightly than either framework alone:

    r = 3(1 - beta/(6 alpha))(n_s - 1)^2 / (1 + b ln(R/mu^2))

where:
- alpha, beta: QG+F couplings (perturbative input)
- b: NGFP logarithmic correction (non-perturbative input, from Bonanno-Platania)

**Key constraint:** In the unified theory, b is NOT free -- it is determined by NGFP anomalous dimensions. The parameter b is related to critical exponents via b ~ θ/(16π²) ~ O(10⁻²), where θ are the NGFP critical exponents:
- Einstein-Hilbert truncation: θ₁,₂ = 1.48 ± 3.04i (complex pair)
- R² truncation: θ₁ = 2.38, θ₂,₃ = 1.26 ± 2.74i
- Higher truncations: values shift but remain O(1)

Most reliable AS calculations give b ~ 0, yielding r ~ 0.003 for N = 55. The precise relation between b and critical exponents has NOT been derived from first principles in a controlled approximation.

**Discrimination windows:**

| Measured r | Interpretation |
|-----------|----------------|
| r > 0.005 | Tension with unified theory; favors standalone AS with large b |
| 0.003 < r < 0.005 | Consistent with both; requires precise n_s to discriminate |
| 0.001 < r < 0.003 | Sweet spot for unified theory; QG+F beta > 0 reduces r |
| 0.0004 < r < 0.001 | Heavy fakeon regime; requires large m_chi/m_phi |
| r < 0.0004 | Falsifies standard single-field picture in both frameworks |

**n_s tension resolution:** Current 2.3-sigma tension (n_s = 0.9737 +/- 0.0025 vs. 0.964-0.967). Unified theory offers:
1. NGFP correction b ~ 10^{-2} shifts n_s to 0.970-0.975
2. Six-derivative terms from NGFP truncation hierarchy give n_s ~ 0.974

See `../qgf-vs-as-cmb-discrimination.md` for the full discrimination analysis.

## 5. Spectral Dimension Profile as Consistency Check

**Prediction:** The full d_s(E) profile from E = 0 to E = infinity must agree between perturbative and non-perturbative calculations in the overlap regime (E ~ M_P).

- **AS result:** d_s -> 2 in UV, robust across all truncations (depends only on eta_N = -2)
- **QG+F result:** Higher-derivative propagators (~ 1/p^4 in UV) give d_s = 2 at short distances

**Novel constraint:** The interpolation d_s = 4 (IR) -> d_s = 2 (UV) must match between both descriptions. Disagreement in the overlap regime (from a lattice gravity or Monte Carlo calculation) would falsify the unified framework.

See `../spectral-dimension-running.md` for the phenomenon; `../spectral-dimension-propagator-constraint.md` for the constructive use.

## 6. Six-Derivative Extension from NGFP Truncation Hierarchy

**Prediction:** The six-derivative extension of QG+F (R^3, R*C^2, R*E terms) corresponds to a specific level of the NGFP truncation hierarchy. The R^3 correction that may resolve the n_s tension should emerge naturally from the NGFP effective action at the appropriate truncation order.

**Quantitative test:** The six-derivative coupling ratios predicted by AS (from NGFP fixed-point values) can be compared with the coupling ratios needed to resolve the n_s tension in QG+F (delta_3 ~ -10^{-4}). Agreement supports the unified framework; disagreement tensions it.

See `../../quadratic-gravity-fakeon/six-derivative-extension.md` for the QG+F six-derivative analysis.

## 7. Higgs Mass as UV Boundary Consistency Check — RESOLVED ✓

**Prediction:** AS's Higgs mass prediction (~126 GeV, Shaposhnikov-Wetterich 2010) must be compatible with QG+F's fakeon quantization of the matter sector.

**Status: RESOLVED — CONSISTENCY CHECK PASSES.** The fakeon prescription does not affect the SW prediction. Three independent arguments:

1. **UV divergences are prescription-independent** — beta functions identical under fakeon and standard quantization (Anselmi JHEP 06, 058, 2022)
2. **The FRG is Euclidean** — the NGFP boundary condition λ(M_Pl) ≈ 0 is prescription-independent; fakeon is a Lorentzian concept with no effect in Euclidean signature
3. **Absorptive part vanishes below threshold** — kinematic suppression by (m_H/M_Pl)² kills all prescription-dependent corrections at the EW scale

**Quantitative bound:** |Δm_H| < 10⁻⁷ GeV — six orders below experimental uncertainty, seven below m_top theoretical uncertainty. The fakeon is the **smallest possible correction** to the Higgs mass.

**Not a novel prediction:** The unified framework inherits the SW prediction unchanged. No shift, no new content. This is valuable as a consistency check but contributes no discriminating power.

**Residual open calculation:** Compute A_λ in the C²-extended FRG truncation (currently computed only in Einstein-Hilbert truncation). This is an AS truncation question, not a fakeon question.

See `./higgs-mass-consistency.md` for the full analysis and quantitative bound. See `../../asymptotic-safety/standard-model.md` for the AS Higgs mass prediction details.

## Consolidated Post-Adversarial Prediction Survival Table

After full adversarial pipeline (E001–E005 derivation, E006 devil's advocate, E007 theory document, E008 mission validation), every prediction has been classified:

| ID | Prediction | Pre-Adversarial | Post-Adversarial | Testable? |
|---|---|---|---|---|
| P-QGF-1 | r ∈ [4×10⁻⁴, 4×10⁻³] | DISCRIMINATING | **INHERITED (QG+F)** | Yes (~2036) |
| P-QGF-2 | r = −8n_T preserved | CONSISTENCY | CONSISTENCY | Yes (post-r detection) |
| P-QGF-3 | CMB matches Starobinsky | CONSISTENCY | CONSISTENCY | Yes (ongoing) |
| P-AS-1 | Higgs mass unchanged | CONSISTENCY | CONSISTENCY (clean) | Done (retrodiction) |
| P-AS-2 | BH remnants, T → 0 | CONSISTENCY | **INHERITED (AS)** | No (Planck scale) |
| P-AS-3 | d_s → 2 | CONSISTENCY | CONSISTENCY (trivial) | No (universal) |
| P-UNI-1 | Ghost complex pole tower | DISCRIMINATING | **CONSISTENCY CHECK** | Theoretically (years) |
| P-UNI-2 | BH phase transition at M_crit | NOVEL | **DEAD** | No (Planck scale, self-undermined) |
| P-UNI-3 | Ghost confinement scale = M_P | NOVEL | **UNCOMPUTED** | Requires AF→NGFP trajectory |
| L1 | NGFP R³ correct sign for n_s | LEAD | **LEAD** (correct sign, unknown magnitude) | Requires g̃₃*→δ₃ mapping |
| L2 | Average continuation for AS | PROMISING | **UNDEMONSTRATED** | May be rendered moot by Lorentzian AS |

**Key downgrades:**
- P-UNI-1 (ghost dissolution): Downgraded from DISCRIMINATING to CONSISTENCY CHECK — circularity problem (assumes unification to predict unification), AS generically produces complex poles without needing unification. The *amplitude equivalence test* (do FRG amplitudes match fakeon amplitudes?) is the genuinely discriminating test, but this has not been formulated as a concrete calculation.
- P-UNI-2 (BH phase transition): Declared DEAD as a scientific prediction — forever observationally inaccessible, self-undermined by M_rem > M_crit ordering in standard convention (AS transition preempts ghost trigger), transition order depends on broken QCD analogy.
- L1 (R³ for n_s): The b parameter cautionary tale is severe — naive NGFP estimate gave b ~ 0.01, actual perturbative calculation gave b ~ 10⁻¹⁴ (suppressed by 12 orders of magnitude by RG running). Naive δ₃ estimates (10⁻¹² to 10⁻²²) suggest similar suppression vs. the needed ~10⁻⁴.

**Bottom line:** Every testable prediction is inherited from one standalone component. The null hypothesis (compatible-but-separate) explains all evidence equally well with fewer assumptions.

Sources: Anselmi (2018, JHEP 02, 141); Bonanno & Platania (2015, 2018); Bianchi & Gamonal (2025, arXiv:2506.10081); Bonanno et al. (2025, arXiv:2505.20360); Becker et al. (2017, arXiv:1709.09098); Shaposhnikov & Wetterich (2010); Falls-Kluth-Litim (2023); exploration-007-unified-framework; exploration-s4-007-complete-theory (quantum-gravity-2 strategy-004)
