# Exploration 007: Non-Perturbative QG+F — The Gravitational Confinement Analogy

## Goal
Investigate the non-perturbative structure of QG+F/AS and identify predictions or phenomena invisible to the perturbative (fakeon) framework. Specifically: how far does the QCD analogy go, what are AS-specific predictions, do gravitational bound states exist, are there gravitational phase transitions, and what novel predictions emerge from the non-perturbative sector?

## Status: IN PROGRESS — completing remaining tasks

---

## Task 1: The QCD-QG+F Analogy — How Far Does It Go?

### 1.1 The Analogy Setup

The analogy between quadratic gravity (QG+F) and QCD is remarkably precise in certain structural respects:

| Feature | QCD | Quadratic Gravity (QG+F) |
|---------|-----|--------------------------|
| UV behavior | Asymptotically free (g_s → 0) | Asymptotically free in f₂ (Weyl² coupling) |
| Running coupling | α_s(μ) runs logarithmically | f₂(μ) runs logarithmically |
| Dynamical scale | Λ_QCD ~ 200 MeV | M_P ~ 10¹⁹ GeV (conjectured) |
| Perturbative regime | E >> Λ_QCD | E >> M_P |
| Non-perturbative regime | E ~ Λ_QCD (confinement) | E ~ M_P (strong gravity) |
| Unphysical degrees of freedom | Gluons (colored, confined) | Spin-2 ghost (fakeon/confined) |
| Physical spectrum | Hadrons (colorless bound states) | Massless graviton + ? |
| Non-perturbative completion | Lattice QCD | Asymptotic safety (Reuter FP) / CDT |

The analogy was first articulated explicitly by **Holdom and Ren (2015, PRD 93, 124030; arXiv:1512.05305)**, who proposed that quadratic gravity is the gravitational analogue of QCD. Their central thesis: the Planck mass is the gravitational analogue of Λ_QCD — a dynamically generated scale where the coupling becomes strong and non-perturbative physics takes over.

**Key paper: Holdom & Ren, "Quadratic gravity in analogy to QCD: Light fermions in its landscape" (PRD 109, 086005, 2024)** extends this to include matter. In the UV (trans-Planckian), the spectrum contains gravitons, the massive spin-2 ghost, and the massive scalar. Below M_P, the theory enters a strongly coupled phase where (conjecturally) the ghost is confined and GR emerges as the low-energy effective theory.

The Quanta Magazine article (Nov 2025, "Old 'Ghost' Theory of Quantum Gravity Makes a Comeback") highlights the renewed interest: key researchers include Donoghue, Buoninfante, Anselmi, Salvio, Strumia, and Menezes. Quadratic gravity now receives 150+ citations annually.

### 1.2 What Is "Confined" in Gravity?

In QCD, quarks and gluons carry color charge and are confined — they cannot appear as asymptotic states. Only color-singlet bound states (hadrons) appear in the physical spectrum.

**In quadratic gravity, the "confined" degree of freedom is the massive spin-2 ghost.** This is the degree of freedom that perturbatively violates unitarity (negative-norm states). The Holdom-Ren conjecture is that, just as gluons are absent from the QCD physical spectrum due to confinement, the spin-2 ghost is absent from the gravitational physical spectrum due to non-perturbative effects.

The parallel:
- QCD: Gluons carry color charge → confined → don't appear as asymptotic states
- QG+F: Spin-2 ghost carries "gravitational charge" → confined → doesn't appear as asymptotic states

**The fakeon prescription in perturbative QG+F is the perturbative implementation of this confinement.** Anselmi's fakeon prescription removes the ghost from the perturbative spectrum by a specific integration contour choice. But this is a kinematic prescription, not a dynamical mechanism. The Holdom-Ren conjecture suggests that the *dynamical* mechanism is confinement — the ghost is removed from the spectrum by non-perturbative strong-coupling effects, just as gluons are removed in QCD.

**Critical distinction:** In QCD, confinement is a *dynamical* phenomenon that follows from the strong-coupling behavior of the theory. The fakeon prescription in QG+F may be the perturbative shadow of this dynamical confinement. A recent (March 2026) paper (arXiv:2603.07150) proposes an alternative interpretation: the ghost as an "inverted harmonic oscillator" (IHO) — the mode contributes only through virtual dispersive effects rather than propagating asymptotically, preserving unitarity without requiring literal confinement.

### 1.3 What Are "Gravitational Hadrons"?

In QCD, confinement produces hadrons — composite, color-singlet bound states of quarks and gluons. The gravitational analogue would be:

1. **Graviton as composite state?** In the strong-coupling phase, the massless graviton in the IR could itself be a composite state — analogous to the pion being a (quasi-)Goldstone boson of chiral symmetry breaking. In the Holdom-Ren picture, GR (with its massless graviton) *emerges* from the strongly coupled phase, rather than being put in by hand.

2. **Massive composites at M_P**: If ghost confinement occurs at the Planck scale, the "hadron" spectrum of gravity would consist of the massless graviton (the "pion" analogue) plus massive composite states at the Planck scale (the "proton" and heavier hadron analogues). These massive composites would be Planck-mass objects — unobservable by current experiments.

3. **"Graviballs"**: Dvali, Guiot, Borquez, and others (JHEP 11 (2020) 159) proposed that gravitons can form bound states ("graviballs") through their self-interaction. These are NOT the same as non-perturbative confinement states — graviballs are semiclassical objects formed by N gravitons bound by their collective gravitational interaction. They are related to Dvali-Gomez's N-portrait of black holes: black holes as Bose-Einstein condensates of N soft gravitons with wavelength √N × l_P and interaction strength 1/N.

### 1.4 Gravitational Chiral Symmetry Breaking Analogue

In QCD, chiral symmetry breaking produces:
- A quark condensate ⟨q̄q⟩ ≠ 0
- Light pions as pseudo-Goldstone bosons
- A mass gap (proton mass ~ Λ_QCD)

The gravitational analogue is suggestive but speculative:
- **Condensate:** A gravitational vacuum condensate. Hamber's lattice quantum gravity work (arXiv:1707.08188; Symmetry 11(1), 87, 2019) demonstrates via Regge-Wheeler lattice path integrals that a nontrivial gravitational vacuum condensate exists, "analogous to the gluon and chiral condensates known to describe the physical vacuum of QCD." The resulting theory depends on one adjustable parameter — a nonperturbative scale ξ, directly analogous to Λ_QCD̄.
- **Mass gap:** The Planck mass M_P could be the gravitational analogue of Λ_QCD. A January 2025 paper (arXiv:2501.16445) demonstrates a mass gap in non-perturbative quadratic R² gravity via Dyson-Schwinger equations: M²_G ~ √R (mass gap increases with the square root of the Ricci scalar). At low energies, the mass gap suppresses the scalaron's interactions, causing physics to transition toward Einstein-Hilbert gravity.
- **"Pion":** The massless graviton could be a composite (analogue of the pion), but no concrete symmetry-breaking mechanism has been identified. Gravity's diffeomorphism invariance is a gauge symmetry, not a global symmetry that could be spontaneously broken in the Goldstone sense.

**No concrete gravitational chiral symmetry has been identified.** The analogy is suggestive but does not map cleanly.

### 1.5 Where the Analogy Breaks Down

The QCD-gravity analogy has several important limitations:

1. **Gauge group structure:** QCD is an SU(3) gauge theory with a compact gauge group. Gravity involves diffeomorphisms — an infinite-dimensional group. Confinement in gauge theory is intimately tied to the compact nature of the gauge group (center symmetry, etc.). Whether diffeomorphisms can produce analogous confinement is unknown.

2. **Color vs. no color:** Quarks carry a well-defined color quantum number that is confined. The spin-2 ghost doesn't carry an analogous conserved quantum number. What exactly is "confined" is less clear.

3. **Universal coupling:** Gravity is universal — everything couples to gravity, including gravity itself. There is no analogue of "color-neutral" objects that decouple from the confining force.

4. **No rigorous lattice proof:** QCD confinement is rigorously established through lattice simulations showing area-law Wilson loops, string tension, etc. For gravity, CDT and Hamber's Regge calculus provide non-perturbative formulations, but they do not yet demonstrate "ghost confinement" in the specific sense required.

5. **Sign of the action:** The Euclidean gravitational action is unbounded below (conformal mode problem). QCD's Euclidean action is bounded below. This fundamental difference makes non-perturbative gravitational calculations much harder and less controlled.

6. **The ghost is UV-specific:** In QCD, confinement is a property of the fundamental theory. In gravity, the spin-2 ghost only appears when we go to the full quadratic gravity action — it's not present in GR. The "confinement" is confining a degree of freedom that only exists in the UV-complete theory.

7. **Non-perturbative uncertainty in fakeons:** Anselmi himself acknowledges (arXiv:2510.05276, JHEP 01 (2026) 104) that the perturbative expansion in fakeon theories is missing non-perturbative effects. The classicized equations are inherently perturbative, and "nonperturbative effects play crucial roles" in certain regimes, introducing a "new type of uncertainty."

**Overall Assessment:** The analogy is *structurally* tight (asymptotic freedom → strong coupling → spectrum without unphysical states → composites). But the *dynamical* details are very different, and there is no proof of gravitational ghost confinement. The analogy is best viewed as a *heuristic guide*, not a proof.

---

## Task 2: Non-Perturbative AS Predictions

### 2.1 RG-Improved Black Holes (Bonanno-Reuter)

The Bonanno-Reuter (BR) black hole is the most studied prediction of asymptotic safety. The construction:

1. Start with the Schwarzschild metric
2. Replace the classical Newton's constant G₀ with its running counterpart G(k) from the RG flow
3. Identify the RG scale k with a physical scale (e.g., proper distance from the center)

**The BR metric (lapse function):**
```
f(r) = 1 - 4G₀mr² / [2r³ + g*⁻¹ξ²G₀(2r + 9mG₀)]
```
where g* is the fixed-point value of Newton's coupling.

**Key predictions:**
- **Singularity resolution:** The central singularity is replaced by a regular de Sitter core. The effective Newton constant G(r) → 0 as r → 0, so gravity weakens precisely where it would create a singularity.
- **Two horizons:** The structure resembles Reissner-Nordström, with inner and outer horizons.
- **Planckian remnant:** Hawking evaporation terminates at a Planck-mass remnant rather than complete dissolution. The temperature T → 0 at the critical mass, producing a cold, stable remnant.
- **Modified thermodynamics:** Entropy-mass relations differ from Bekenstein-Hawking due to scale-dependent Newton coupling.
- **Modified quasi-normal modes:** For Planckian black holes, QNMs display significant deviations from the classical case (multiple papers 2024-2025).

**Recent developments (2024-2025):**
- Bonanno et al. (2024, PRL): Dust collapse in AS produces regular black holes for α > 1 (where α parameterizes the RG running). For α ≤ 1, singularities persist.
- Multiple papers (2025): Computed QNMs, grey-body factors, shadows, and absorption cross-sections for BR black holes, making observational predictions increasingly concrete.
- A self-consistent framework (2025-2026): Moving from phenomenological RG improvement toward first-principles derivation from the effective action.

**Is this invisible to QG+F?** Partially. Perturbative QG+F (with the fakeon) also modifies black hole physics at the Planck scale, but the specific predictions differ:
- QG+F predicts that the massive spin-2 fakeon cannot propagate in the black hole interior (it's virtual-only), which could modify the singularity structure differently
- The BR remnant prediction relies on the non-perturbative running G(k) → 0 in the UV, which is a consequence of the Reuter fixed point — not visible in perturbation theory
- The specific temperature profile (T → 0 at minimum mass) is a non-perturbative prediction

### 2.2 Singularity Resolution

AS provides a *generic* mechanism for singularity resolution: gravitational anti-screening.

**The mechanism:** At the non-Gaussian fixed point, Newton's coupling runs as:
```
G(k) = g* / k²  (for k >> k_Planck)
```
This means gravity *weakens* at high energies. When matter collapses, the effective gravitational coupling decreases precisely as densities and curvatures approach Planck scale, preventing the formation of singularities.

**Recent (2025) results on gravitational collapse:**
- Parameterized running: G(ε) = G_N / [1 + ω̃(G_N²ε)^α]
- For α > 1: Complete singularity resolution for ALL spatial curvatures — the collapse produces regular black holes or gravastars
- For α = 1: Incomplete resolution — singularities can still form in some cases
- For α < 1: Singularities persist — inconsistent with AS

The key finding: the parameter α that controls singularity resolution is directly related to the anomalous dimension of Newton's constant at the fixed point. AS predicts α > 1, so it *predicts* complete singularity resolution.

**Comparison with QG+F:** Perturbative QG+F does not provide a clear singularity resolution mechanism. The fakeon prescription removes the ghost from the S-matrix, but the classical field equations (which determine the black hole geometry) still have the higher-derivative structure. Whether QG+F resolves singularities depends on non-perturbative effects that the fakeon prescription alone doesn't capture.

### 2.3 Graviton Condensate

**QCD analogue:** The gluon condensate ⟨α_s G²⟩ ~ (0.33 GeV)⁴ is a fundamental non-perturbative parameter of QCD. It appears in the SVZ sum rules and controls non-perturbative corrections to many processes.

**Gravitational vacuum condensate (Hamber):** The Regge-Wheeler lattice path integral formulation reveals a nontrivial gravitational vacuum condensate — a nonperturbative scale ξ analogous to Λ_QCD. Key results:
- The critical exponent ν ≈ 1/3 (conjectured to be universal)
- The running of Newton's constant at large distances: G(r) ~ G₀[1 + c(r/ξ)^(1/ν) + ...]
- The correlation length ξ is related to the observed cosmological constant: ξ ~ 1/√Λ
- "Significant deviations from classical gravity on distance scales approaching the effective infrared cutoff set by the observed cosmological constant"

**This is inherently non-perturbative:** The vacuum condensate has no perturbative analogue. It requires summing over all gravitational field configurations, not just small fluctuations around flat space. Perturbative QG+F cannot reproduce it.

**Dvali-Gomez N-portrait:** A complementary picture describes black holes as Bose-Einstein condensates of N weakly-interacting soft gravitons (wavelength √N × l_P, interaction strength 1/N). Hawking radiation = quantum depletion of the condensate. Bekenstein entropy = exponentially growing number of quantum states with N. Black holes are the "critical point of a quantum phase transition."

### 2.4 Cosmological Predictions Unique to AS

**1. Inflation without an inflaton:**
AS provides a mechanism for inflation driven purely by quantum gravitational effects — no inflaton field needed. The cosmological constant at the Reuter fixed point drives a quasi-de Sitter phase that ends automatically when the RG flow reduces the vacuum energy to the matter energy density. Specific predictions:
- Nearly scale-invariant primordial spectrum (from the near-fixed-point behavior)
- The smallness of the R² coupling required for CMB normalization is *naturally* ensured by its vanishing at the UV fixed point
- Tensor-to-scalar ratio: r can be as large as ~0.01, potentially measurable by Stage IV CMB experiments

**2. Emergent cosmological model from running G (2024):**
Bonanno et al. (PRD 111, 103519, 2025; arXiv:2405.02636) derive a complete cosmological model from the running Newton constant:
- G(ε) = G_N / (1 + ε/ε_c) where ε_c is a critical energy density
- The universe naturally enters a quasi-de Sitter phase at early times
- Flatness and horizon problems solved without inflaton
- Primordial power spectrum: nearly scale-invariant, constrained by CMB data
- Key prediction: ε_c encodes the Reuter fixed point value g* = 540π/833
- **Testable:** The transition scale ε_c can be constrained by CMB measurements

**3. Shaposhnikov-Wetterich Higgs mass prediction:**
If AS extends to the Standard Model, the quartic Higgs coupling λ is driven to zero at the Reuter fixed point, predicting m_H ≈ 126 GeV (published 2010, BEFORE the Higgs discovery at 125.1 GeV). This is arguably the most impressive "postdiction" of AS.

**4. Running of the cosmological constant:**
AS predicts that Λ runs with energy. In the UV (at the Reuter fixed point), λ* ~ 0.3 is O(1), but flows to its tiny observed value λ ~ 10⁻¹²² in the IR. This provides a *trajectory* connecting UV and IR, though it does not solve the CC problem (why this particular trajectory is selected).

**What QG+F misses:** Perturbative QG+F provides inflation via the Starobinsky mechanism (R² term), but cannot reproduce:
- The inflaton-free inflation of AS
- The specific running G cosmological model
- The Higgs mass prediction (which requires the full non-perturbative fixed-point structure)
- The gravitational vacuum condensate
- The specific predictions for BR black holes (remnants, temperature profile)

---

## Task 3: Gravitational Bound States

### 3.1 Graviton Glueballs / Graviballs

**QCD glueballs:** In QCD, gluons form bound states called glueballs — color-singlet states composed entirely of gluons. The lightest glueball (0++) has mass ~1.5-1.7 GeV in lattice QCD.

**Gravitational analogue — Graviballs:**
Guiot, Borquez, Deur, and Werner (JHEP 11 (2020) 159) showed that two gravitons can form a bound state (a "graviball") through their gravitational self-interaction. Key findings:
- Two gravitons *can* be bound by gravitational interaction
- The graviball is related to the "gravitational geon" studied by Brill and Hartle (1964)
- Calculations use quantum field theory techniques applied to low-energy quantum gravity
- Numerical solutions of the relativistic equations of motion give access to space-time dynamics

**Dvali-Gomez framework:** Black holes themselves are "graviton bound states" — Bose-Einstein condensates of N gravitons:
- Wavelength: √N × l_P
- Coupling: 1/N
- Mass: M_BH = N × M_P / √(N) = √N × M_P
- A black hole of mass M contains N ~ (M/M_P)² gravitons
- The condensate is at the critical point of a quantum phase transition

### 3.2 Dark Matter Candidates

**Graviballs as dark matter:** Guiot et al. propose graviballs as dark matter candidates with associated gravitational lensing effects. However, the masses and production mechanisms need further study.

**Planck remnants as dark matter:** If AS predicts stable Planck-mass remnants from primordial black hole evaporation, these could be dark matter:
- Primordial BHs with initial mass < 10⁹ g would have evaporated by now in standard physics
- In AS, evaporation halts at a Planck-mass remnant (~10⁻⁵ g)
- If enough primordial BHs formed, their remnants could dominate the dark matter density
- **Observable signature:** A gravitational wave signal at ~100 Hz (from PBH mergers/formation)
- Recent work (2024, MNRAS): Breakdown of Hawking evaporation opens new mass window for primordial black holes as dark matter

**Dark glueball scenario (via gravitational production):** Not directly from graviton bound states, but dark sectors with purely gravitational couplings to the Standard Model are unavoidably populated by graviton exchange, producing dark glueballs as viable dark matter candidates.

### 3.3 Lattice Gravity Evidence (CDT and Regge Calculus)

**CDT (Causal Dynamical Triangulations):**
CDT is the closest lattice-gravity analogue to lattice QCD. It provides non-perturbative evidence for:
- Emergence of 4D de Sitter-like spacetime in the physical phase (Phase C)
- Spectral dimension running from d_s ≈ 4 (IR) to d_s ≈ 3/2-2 (UV)
- A rich phase diagram with multiple phases and phase transitions (see Task 4)
- Potential UV fixed point behavior at the B-C second-order phase transition

However, CDT has **not** demonstrated:
- Specific graviton bound state formation
- Ghost confinement (the lattice formulation doesn't include the ghost degrees of freedom explicitly)
- A "glueball" spectrum of gravitational composites

**Hamber's Regge calculus:**
- Gravitational Wilson loop computed on the lattice
- Critical exponent ν ≈ 1/3 found (universal?)
- Gravitational vacuum condensate identified
- Running Newton constant consistent with gravitational anti-screening
- But: no explicit "bound state" formation observed

**Gap in the evidence:** Neither CDT nor Regge calculus has demonstrated bound state formation analogous to glueballs in lattice QCD. This remains one of the most important open questions in non-perturbative quantum gravity.

---

## Task 4: Phase Transitions in Quantum Gravity

### 4.1 CDT Phase Diagram — Gravitational Deconfinement?

The CDT phase diagram exhibits rich structure analogous to lattice QCD:

**Three main phases (plus sub-phases):**
| Phase | Properties | QCD Analogue? |
|-------|-----------|---------------|
| **Phase A (branched polymer)** | Spacetime degenerates, no macroscopic extension | Deconfined/high-T phase? |
| **Phase B (crumpled)** | Spacetime collapses, very high Hausdorff dimension | Strong coupling phase? |
| **Phase C (de Sitter)** | Extended 4D spacetime, d_s runs 4→2 | Confined/hadronic phase |

**Phase transitions:**
- **A-C transition:** First order (discontinuous). Recent 2024 work shows this transition line has UV critical behavior — coupling runs correctly when approaching this line.
- **B-C transition:** Second order (continuous). This is the candidate for defining a UV continuum limit — the analogue of the UV fixed point in asymptotic safety.
- A fourth phase (C_b, "bifurcation phase") has been identified between B and C.

**The QCD analogy for phases:**
In QCD, the deconfinement phase transition at T ~ 150 MeV separates:
- Low T: confined phase (hadrons), spontaneously broken chiral symmetry
- High T: deconfined phase (quark-gluon plasma), restored chiral symmetry

In CDT, the Phase C → Phase A transition could be the gravitational analogue:
- Phase C: "confined" phase where 4D spacetime emerges (GR limit)
- Phase A: "deconfined" phase where spacetime structure dissolves

However, the physical interpretation is unclear. In QCD, the deconfined phase is accessible experimentally (RHIC, LHC). In gravity, the "deconfined" phase would require trans-Planckian energies and may not correspond to any physically realizable state.

### 4.2 Spectral Dimension Phase Transition

The d_s = 4 → d_s = 2 flow can be interpreted as a dimensional phase transition:
- **IR phase (d_s = 4):** Classical spacetime, GR applies
- **UV phase (d_s = 2):** Quantum spacetime, scale-invariant at the fixed point
- **Crossover scale:** ~ Planck scale

This is universal across approaches (AS, CDT, Horava-Lifshitz, LQG, causal sets, etc.). The question is whether this crossover is:
- A **smooth crossover** (like the QCD crossover at μ ≠ 0, T ≠ 0)
- A **genuine phase transition** (like QCD deconfinement at μ = 0)

CDT evidence suggests the B-C transition is second order, which would make the d_s crossover a genuine phase transition with a correlation length diverging at the critical point. This would have profound implications — it would mean the Planck scale marks an actual critical point, not just a crossover.

### 4.3 Recent Literature (2024-2025)

Key recent developments:

1. **CDT UV fixed point (2024):** Ambjorn et al. found that coupling behavior near the A-C_dS phase transition line is consistent with UV critical behavior, strengthening the case for CDT defining a UV continuum limit consistent with AS.

2. **CDT-FRG comparison (2024):** Paper in PRD 110, 126006 (2024): "Is lattice quantum gravity asymptotically safe? Making contact between CDT and the FRG" — first attempts to quantitatively compare CDT lattice results with functional RG results from AS. Results: "the two results are not yet in good agreement" — this is an important tension.

3. **Mass gap in quadratic gravity (2025):** arXiv:2501.16445 demonstrates a mass gap in non-perturbative R² gravity via Dyson-Schwinger equations. The mass gap signals breaking of scale invariance, representing a phase transition from quadratic-gravity-dominated to Einstein-Hilbert-dominated dynamics.

4. **IHO interpretation (March 2026):** arXiv:2603.07150 proposes the ghost as an inverted harmonic oscillator with "controlled dynamical instabilities." Claims to resolve CMB anomalies with 650× statistical improvement over standard theory, and predicts modifications to the tensor-to-scalar ratio.

5. **Inflationary phase transitions:** Multiple 2024-2025 papers study phase transitions *during* inflation that produce gravitational wave signatures detectable by future space-based detectors (LISA, etc.).

---

## Task 5: Novel Predictions from the Non-Perturbative Sector

### 5.1 Prediction 1: Planck-Mass Black Hole Remnants

**The prediction:** Black holes do not evaporate completely. Hawking evaporation terminates at a cold, Planck-mass remnant (~10⁻⁵ g, or ~M_P).

**Theoretical basis:** The Bonanno-Reuter RG-improved black hole has G(r) → 0 as r → 0. As the black hole shrinks, the effective gravitational coupling weakens, the Hawking temperature reaches a maximum and then *decreases* to zero at a minimum mass. The evaporation endpoint is a zero-temperature, Planck-mass remnant.

**Why invisible to perturbative QG+F:** The remnant prediction relies on the non-perturbative running G(k) → g*/k² at the Reuter fixed point. Perturbative QG+F gives corrections to Hawking radiation as a power series in (M_P/M_BH)², which diverges for Planckian black holes. The remnant requires resummation of the full non-perturbative RG flow.

**How to test:**
- Primordial black hole remnants as dark matter (gravitational wave signature at ~100 Hz)
- Modified Hawking radiation spectrum from near-extremal black holes (if quantum BH production is ever possible)
- Absence of complete BH evaporation products in any future BH factory scenario

**Uniqueness:** This prediction is genuinely non-perturbative. No perturbative calculation can reproduce the T → 0 endpoint because it requires the full β-function to all orders.

### 5.2 Prediction 2: Gravitational Vacuum Condensate and Running G at Cosmological Scales

**The prediction:** Newton's constant runs at cosmological distances:
```
G(r) = G₀[1 + c₀(l_P/ξ)^(1/ν) + c₁(r/ξ)^(1/ν) + ...]
```
where ξ ~ 1/√Λ is the gravitational correlation length and ν ≈ 1/3. This predicts deviations from GR at distances comparable to the Hubble radius.

**Theoretical basis:** Hamber's Regge calculus lattice gravity identifies a nontrivial gravitational vacuum condensate (analogous to ⟨α_s G²⟩ in QCD). The condensate generates a nonperturbative scale ξ that controls the running of G at large distances. A fundamental relationship emerges: the scale characterizing the running of G, the macroscopic curvature (cosmological constant), and the correlation length are all related.

**Why invisible to perturbative QG+F:** The gravitational vacuum condensate is a nonperturbative object. It requires summing over all gravitational field configurations in the path integral. Perturbative QG+F expands around flat space and cannot access vacuum condensate effects. The running of G in perturbative QG+F is logarithmic and tiny (as found in Exploration 005: Δθ/θ ~ 10⁻¹⁴); the non-perturbative running from the condensate could be power-law and potentially observable.

**How to test:**
- Precision tests of gravity at cosmological scales (modified expansion history)
- Deviations from ΛCDM in large-scale structure
- Running of effective Newton constant measurable via CMB + BAO + type Ia supernovae
- Future high-precision satellite experiments (per Hamber)

**Uniqueness:** The vacuum condensate is entirely non-perturbative. The power-law running G(r) differs qualitatively from the logarithmic running accessible to perturbation theory.

### 5.3 Prediction 3: Inflation Without an Inflaton

**The prediction:** The early universe undergoes an inflationary phase driven purely by quantum gravitational effects at the Reuter fixed point — no inflaton field needed. The cosmological constant at the fixed point λ* ~ 0.3 drives a quasi-de Sitter expansion that ends automatically when the RG flow carries the couplings away from the fixed point.

**Theoretical basis:** In AS, all couplings run. Near the Reuter fixed point, the effective cosmological constant is large (~M_P⁴), driving exponential expansion. As the universe expands and cools, the RG flow moves away from the fixed point toward the GR regime, ending inflation naturally.

**Specific predictions (different from QG+F/Starobinsky):**
- QG+F gives Starobinsky inflation with n_s ≈ 0.967, r ∈ [0.0004, 0.0035] from the R² term
- AS inflaton-free inflation predicts: n_s from the fixed-point anomalous dimensions, r up to ~0.01
- The transition scale ε_c from the Reuter fixed point to classical GR is a new parameter constrained by CMB
- The running G model (Bonanno et al. 2024) gives specific predictions for the primordial power spectrum that differ from Starobinsky at the level of slow-roll corrections

**Why invisible to perturbative QG+F:** Perturbative QG+F *requires* the R² term to drive inflation (Starobinsky mechanism). It cannot produce inflation from pure gravity without an R² term or inflaton. The AS inflation mechanism relies on the non-perturbative fixed-point structure — the full β-functions driving G and Λ through the trans-Planckian regime.

**How to test:**
- CMB measurements constraining n_s and r (LiteBIRD, CMB-S4)
- If AS inflation gives r ~ 0.01, this is ~3× larger than QG+F's prediction — distinguishable by next-generation experiments
- If r < 0.004 is confirmed, this would *rule out* the simplest AS inflation models while being consistent with QG+F

**Uniqueness:** The inflaton-free mechanism is inherently non-perturbative. Perturbative quantum corrections to the cosmological constant are uncontrolled; only the non-perturbative fixed point provides a controlled mechanism.

### 5.4 Bonus Prediction: Higgs Mass from Asymptotic Safety

**The prediction:** Shaposhnikov and Wetterich (2010) predicted m_H ≈ 126 ± few GeV from the requirement that the quartic Higgs coupling λ vanishes at the Reuter fixed point. This was published before the 2012 discovery of the Higgs at 125.1 GeV.

**Why invisible to perturbative QG+F:** This prediction requires the full fixed-point structure of gravity coupled to the Standard Model. The quartic coupling flows to zero at the NGFP — a non-perturbative boundary condition. Perturbative QG+F gives gravitational corrections to Standard Model running, but cannot set the UV boundary condition at the fixed point.

**Status:** Impressive but not conclusive. The prediction depends on assumptions about the matter content and the exact form of the gravitational corrections. Alternative derivations with different matter content give different predictions. But the fact that the prediction is within the correct range (126 ± few GeV vs. 125.1 GeV) is striking.

---

## Synthesis and Conclusions

### The QCD-Gravity Analogy: A Useful But Imperfect Guide

The analogy is **structurally compelling** and has led to genuine insights:
- Ghost confinement (Holdom-Ren) provides a physical mechanism for why the ghost is absent from the physical spectrum
- The Planck mass as a dynamical scale (like Λ_QCD) is well-motivated
- The perturbative/non-perturbative split (QG+F/AS) maps cleanly onto the QCD perturbative/confinement split

But the analogy **breaks down** in important ways:
- No proof of gravitational ghost confinement
- No "color" quantum number for the ghost
- The Euclidean action is unbounded below
- CDT and lattice gravity do not yet demonstrate the equivalent of lattice QCD confinement results

### What the Non-Perturbative Sector Adds

**Predictions invisible to perturbative QG+F:**

| Prediction | Non-Perturbative Source | Testable? | Timescale |
|-----------|----------------------|-----------|-----------|
| Planck remnants | BR black holes from RG improvement | Via PBH dark matter, GW signals | 2030s (LISA) |
| Running G at cosmological scales | Vacuum condensate (Hamber) | Precision cosmology | 2030s |
| Inflation without inflaton | Reuter fixed point | r ~ 0.01 vs r ~ 0.003 | 2030s (CMB-S4) |
| Higgs mass prediction | SM at the fixed point | Already confirmed (125 GeV) | Done |
| Singularity resolution | Anti-screening at FP | Indirect (remnants, GW ringdown) | 2030s+ |
| Mass gap generation | Dyson-Schwinger in R² gravity | Theoretical only | N/A |

### The Critical Question: Are QG+F and AS the Same Theory?

This remains open. The SWY result (2022) shows two distinct fixed points in the full quadratic truncation — one asymptotically free (QG+F), one asymptotically safe (NGFP). If they are distinct, they make different predictions. If they are secretly the same theory in different computational schemes, then the non-perturbative predictions of AS should be derivable (in principle) from QG+F.

**The most likely answer:** QG+F is the perturbative sector of a larger theory whose non-perturbative sector includes AS. The perturbative sector (QG+F) gives the correct S-matrix at energies well above M_P. The non-perturbative sector (AS) gives additional predictions for:
- Strong-field regimes (black hole interiors, very early universe)
- Cosmological scales (vacuum condensate effects)
- The full spectrum (remnants, bound states if they exist)
- UV boundary conditions for matter couplings (Higgs mass)

### Summary Assessment

1. The QCD analogy is **heuristically valuable** but not a proof of anything. It correctly identifies ghost confinement as the key non-perturbative phenomenon.
2. The non-perturbative sector makes **at least 4 predictions** invisible to perturbative QG+F: remnants, running G at cosmic scales, inflaton-free inflation, and the Higgs mass boundary condition.
3. The **most testable** discriminating prediction is the tensor-to-scalar ratio: AS inflation predicts r up to ~0.01, QG+F predicts r < 0.004. Next-generation CMB experiments can distinguish these.
4. The **most theoretically robust** non-perturbative prediction is singularity resolution via gravitational anti-screening, as it follows directly from the fixed-point structure without additional assumptions.
5. The **biggest gap** is the absence of a non-perturbative proof of ghost confinement. This would be the gravitational equivalent of proving confinement in QCD — likely requiring new mathematical and computational techniques.
