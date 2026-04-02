---
topic: unified-qgf-as-framework
confidence: provisional
date: 2026-03-26
source: exploration-007-unified-framework (quantum-gravity-2 strategy-003)
---

# The Unified QG+F--AS Framework Conjecture

## The Conjecture

Quantum gravity is described by a single UV-complete theory whose action is the most general four-derivative extension of Einstein gravity:

    S = integral d^4x sqrt(-g) [ (M_P^2/2) R - Lambda + (1/2f_2^2) C_{munurho sigma} C^{munurho sigma} + (1/f_0^2) R^2 ]

This theory possesses **two complementary descriptions**, related as perturbative and non-perturbative sectors of a single dynamics:

1. **Perturbative sector (QG+F):** Above the Planck scale, f_2 is asymptotically free (Fradkin-Tseytlin 1982). The ghost is quantized via the fakeon prescription (Anselmi 2017-2018), preserving unitarity and Lorentz invariance at the cost of analyticity. Controls: trans-Planckian scattering, inflationary dynamics, perturbative BH exteriors.

2. **Non-perturbative sector (AS):** The same theory treated via the functional RG exhibits the Reuter NGFP (1998). At and below the Planck scale, ghost is confined, singularities resolved by gravitational anti-screening (G(k) -> g_*/k^2), and Planck-mass remnants form. Controls: Planck-scale physics, BH interiors, deep IR cosmological running.

**Key insight:** QG+F and AS are not competing theories. They are two approximation schemes applied to the same underlying dynamics, valid in complementary regimes.

## The QCD Analogy -- Made Precise

The structural parallel is not metaphorical but a detailed mapping (Holdom & Ren 2015, PRD 93, 124030; 2016, arXiv:1605.05006):

| Feature | QCD | Unified QG+F--AS |
|---------|-----|------------------|
| UV behavior | Asymptotically free (g_s -> 0) | Asymptotically free (f_2 -> 0) |
| Running coupling | alpha_s(mu) logarithmic | f_2(mu) logarithmic |
| Dynamical scale | Lambda_QCD ~ 200 MeV | M_P ~ 10^19 GeV |
| Unphysical DOF (perturbative) | Quarks/gluons (colored, confined) | Spin-2 ghost (fakeon, confined) |
| Confinement mechanism | Color confinement, mass gap | Ghost confinement, Planck mass gap |
| Non-perturbative tool | Lattice QCD | FRG / Asymptotic Safety |
| Perturbative tool | pQCD, Feynman diagrams | QG+F, fakeon Feynman rules |
| Fixed point (UV) | Gaussian (AF) | AF fixed point (perturbative) |
| Fixed point (non-pert.) | N/A (confines before) | NGFP (Reuter fixed point) |
| Hadronization | Colored partons -> colorless hadrons | Ghost + massless graviton -> confined graviton |
| Most concrete realization | Lattice QCD + confinement proofs | Draper et al. (2020) complex pole tower |

Most concrete realization: Draper et al. (2020, PRL 125, 181301) -- ghost pole dissolves into infinite tower of complex conjugate pairs that do not contribute to absorptive part of scattering amplitudes, the gravitational analog of quark confinement.

See `../../quadratic-gravity-fakeon/qcd-analogy-ghost-confinement.md` for the analogy's 7 breakdown points.

## Master Regime Table

| Regime | Energy/Scale | Valid Description | Key Physics | Observational Handle |
|--------|-------------|-------------------|-------------|---------------------|
| Trans-Planckian | E >> M_P | QG+F perturbative | AF in f_2; fakeon prescription; all 4 couplings run perturbatively | -- (inaccessible) |
| Planck-scale | E ~ M_P | Full non-perturbative (AS/FRG) | Ghost confinement; phase transition; both descriptions overlap | Inflation, PBH remnants |
| Sub-Planckian | E << M_P | Einstein gravity (GR) | GR + tiny corrections; graviton only propagating DOF; ghost confined | Standard gravity experiments |
| Inflationary | H ~ H_inf | R^2 Starobinsky + NGFP corrections | Slow-roll from R^2; r in [0.0004, 0.004]; corrections from b parameter | CMB (LiteBIRD, SO) |
| BH exterior | r >> l_P | QG+F perturbative (Schwarzschild) | Fakeon => S_2^- = 0 => Schwarzschild; Wald entropy corrections ~ (l_P/r_H)^2 | EHT, GW (LIGO/Virgo) |
| BH interior | r ~ l_P | AS non-perturbative | G(r) -> 0; singularity resolved; de Sitter core; two horizons | PBH evaporation (future) |
| BH evaporation endpoint | M ~ M_P | Phase transition regime | Perturbative Schwarzschild -> non-perturbative remnant; ghost confinement scale | PBH remnant searches (LISA era) |
| Cosmological IR | H ~ H_0 | GR + AS running corrections | Running G(r) at cosmological scales (power-law); potential dark energy contribution | Galaxy rotation, H_0 tension (speculative) |

## Phase Transition at M_P

The transition between regimes is a crossover (not sharp), analogous to the QCD crossover at T ~ Lambda_QCD. Three independent lines of evidence locate it at the Planck scale:

1. **Coupling strength:** f_2(mu) runs logarithmically and becomes O(1) at mu ~ M_P, signaling perturbative breakdown.
2. **Ghost mass threshold:** m_2^2 = M_P^2/(2 alpha_W) sets the scale where the massive spin-2 mode becomes dynamically relevant.
3. **BH branch crossing:** Bonanno et al. (2025, arXiv:2505.20360) showed Schwarzschild becomes linearly unstable below r_H ~ 0.876/m_2, triggering transition to exotic configuration.

## Five Bridge Mechanisms (Summary)

Each bridge connects a perturbative (QG+F) phenomenon to its non-perturbative (AS) counterpart:

| Bridge | QG+F Side | AS Side | Status | Detailed Entry |
|--------|-----------|---------|--------|----------------|
| Ghost | Fakeon (virtual particle) | Confinement (pole migration/dissolution) | CRITICAL GAP: no spin-2 computation | `../../asymptotic-safety/ghost-fate-strong-coupling.md` |
| Fixed Point | AF (Gaussian FP) | NGFP (Reuter FP) | INCONCLUSIVE: same vs. distinct | `../../asymptotic-safety/af-ngfp-fixed-point-connection.md` |
| Inflation | R^2 Starobinsky | NGFP-generated R^2 | SUPPORTS (MODERATE) | `../qgf-vs-as-cmb-discrimination.md` |
| Black Holes | Schwarzschild (exact) | Bonanno-Reuter (resolved) | SUPPORTS | `../qgf-vs-as-bh-compatibility.md` |
| Analyticity | Average continuation | Obstructed Wick rotation | SUPPORTS | `../qgf-vs-as-analyticity-compatibility.md` |

Central unified interpretation under SWY picture: AF fixed point is the UV attractor (trans-Planckian QG+F), NGFP is the crossover fixed point (Planck-scale), and Einstein-Hilbert is the IR endpoint:

    AF (GFP) --[E >> M_P]--> perturbative QG+F --[E ~ M_P]--> NGFP crossover --[E << M_P]--> GR (IR)

**Critical prediction:** A connecting RG trajectory AF -> NGFP -> GR has NOT been computed. Its existence is the central open conjecture.

## Comparison: What Unification Adds

| Prediction | QG+F Alone | AS Alone | Unified |
|------------|-----------|----------|---------|
| Ghost fate at strong coupling | Fakeon (perturbative) | No ghost in truncation | Fakeon -> confinement transition |
| BH evaporation endpoint | Unknown (pert. breaks down) | Remnant (assumed) | Remnant via phase transition |
| Wick rotation resolution | Average continuation | Problem acknowledged | Average continuation applied to FRG |
| Lambda_ghost = M_P | m_2 is free parameter | No ghost to confine | Dynamically generated |
| r prediction | [0.0004, 0.0035] | ~0.003 (b-dependent) | Sharper: b determined by NGFP |
| n_s tension resolution | Needs 6-deriv extension | Needs large b | b or R^3 from NGFP hierarchy |
| Higgs mass | Free parameter | Prediction (126 GeV) | Prediction + fakeon compatibility check |
| Spectral dimension profile | d_s -> 2 (UV) | d_s -> 2 (UV) | Full d_s(E) profile must match |

## Overall Assessment (Post-Adversarial, Final)

**Status: Structural conjecture — organizational, not predictive.**

After exhaustive prediction extraction (6 explorations) and rigorous adversarial testing (E006 devil's advocate, E008 mission validation):
- **Internally consistent** — no falsified predictions, no mathematical contradictions
- **Identifies three critical computations** that could generate genuine discriminating predictions
- **Makes zero novel discriminating predictions** that survive adversarial scrutiny — every claimed prediction is either inherited from one standalone component (QG+F or AS) or currently untestable
- **Practically unfalsifiable** on current timescales for its unification claims specifically
- **Null hypothesis (H₀: compatible-but-separate) is simpler and equally explanatory** — H₀ explains all evidence without requiring a confinement mechanism, by Occam's razor should be preferred until the framework produces a prediction H₀ cannot match

**Strengths:**
1. Coherent organizational structure unifying two major QG programs
2. Physical mechanism (ghost confinement) for perturbative/non-perturbative transition
3. Inherits best features of both: renormalizability + unitarity + singularity resolution + remnants + Starobinsky inflation
4. Three critical computations are genuinely valuable open questions for the field, worth pursuing regardless of whether unification proves correct
5. Internal consistency — survived dedicated adversarial assessment

**Weaknesses:**
1. Two central open problems (AF→NGFP trajectory, spin-2 ghost confinement) are UNRESOLVED
2. QCD analogy breaks at its three most load-bearing joints: (a) no compact gauge group, (b) no quantum number to confine, (c) no lattice evidence after 11 years
3. Non-perturbative uncertainty (Anselmi 2026, arXiv:2601.06346) not yet quantified
4. All novel predictions at or beyond reach of current experiments
5. Every testable prediction traces to one standalone component — the "unification" adds nothing testable

**What would change this assessment:**
1. If C²-extended FRG propagator shows complex pole tower AND resulting amplitudes match fakeon-prescription amplitudes → first genuinely discriminating prediction (amplitude matching NOT predicted by H₀)
2. If full g̃₃* → δ₃ mapping yields δ₃ ∈ [−2×10⁻⁴, −5×10⁻⁵] → specific testable CMB prediction standalone QG+F cannot make
3. If AF → NGFP connecting trajectory exists → structural conjecture gains mathematical substance beyond analogy

**Verdict:** Research program, not predictive theory. Most parsimonious interpretation of existing results but adds nothing testable beyond standalone components. Value is organizational — it shows why two approaches may be complementary and specifies exactly what calculations would prove or disprove this.

**Comparison to Alternatives:**
- vs. Standalone QG+F: Adds ghost fate mechanism, BH interiors, dynamical ghost mass, potential n_s resolution. Does NOT add any testable prediction.
- vs. Standalone AS: Adds perturbative control, average continuation, fakeon mechanism. Does NOT add any prediction.
- vs. String Theory: Fewer dimensions (4 vs. 10–11), fewer parameters, no SUSY required. But far less mathematical maturity and fewer predictions.
- vs. LQG: Different UV structure (fixed point vs. discrete geometry), similar BH singularity resolution. LQG has concrete non-perturbative formulation (spin foams).
- Overall: competitive but not clearly superior to any alternative.

See `./mission-validation-assessment.md` for formal 5-tier mission validation (3 PASS, 2 MARGINAL, 0 FAIL).

Sources: Holdom & Ren (2015, 2016, 2024); Draper et al. (2020, PRL 125, 181301); Sen-Wetterich-Yamada (2022, 2023); Falls-Kluth-Litim (2023); Codello & Percacci (2006); Bonanno et al. (2025); Anselmi (2017, 2018); Reuter (1998); Fradkin & Tseytlin (1982); exploration-007-unified-framework
