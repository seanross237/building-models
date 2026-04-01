# Exploration History

## Exploration 001: Map the Escape Routes from the No-Go Theorem

**Goal:** Systematically classify all 5 "escape routes" from the no-go theorem (which selects QG+F as the unique Lorentz-invariant, diff-invariant, renormalizable theory with d_s = 2) as EMPTY, SINGLETON, or OPEN.

**What Was Tried:** Investigated each of the 5 routes via web search of 2024-2025 literature, analysis of the no-go theorem's assumptions, and assessment of existing vs. novel theory space.

**Outcome: All 5 Routes Are OPEN, But With Very Different Promise**

Ranked from most to least promising:

1. **Route 5 (Alternative Axioms): OPEN — MOST PROMISING.** Information-theoretic constructive axioms (positivity of relative entropy, maximal vacuum entanglement, quantum focusing condition, Bianconi's entropic action) provide genuinely novel foundations not systematically explored as starting points for UV-complete quantum gravity.

2. **Route 4 (Relax Locality): OPEN — HIGH POTENTIAL.** Lee-Wick quantum gravity with meromorphic propagators (complex conjugate poles) escapes the no-go theorem entirely. Super-renormalizable, ghost-free in Lee-Wick sense, distinct from QG+F at loop level. Key uncertainty: higher-loop unitarity debated.

3. **Route 2 (Asymptotic Safety): OPEN — MEDIUM, with SINGLETON risk.** Multiple fixed points exist (SWY 2022). Bimetric structure opens unexplored theory space. But real risk all variations are secretly QG+F in different clothing.

4. **Route 3 (Relax d_s = 2): OPEN — VAST but UNDERCONSTRAINED.** Best used in combination with Route 5: use alternative axioms to construct a theory, then predict d_s as output.

5. **Route 1 (Relax Lorentz Invariance): OPEN but NARROW.** Essentially HL gravity only. GRB 221009A bounds exceed E_Pl for linear LIV.

**Key Takeaway:** The most promising path is Route 5 (alternative constructive axioms), possibly combined with Route 4 (Lee-Wick propagator structure). Specific leads: (1) Bianconi's entropic-action QG (2025), (2) Lee-Wick QG, (3) UV extension of Jacobson's maximal entanglement, (4) Theory from Holographic Emergence Bound axioms, (5) Route 5+4 hybrid.

## Exploration 002: Scrutinize Bianconi's Entropic Action Quantum Gravity (2025)

**Goal:** Critically assess Bianconi's 2025 "Gravity from entropy" paper (Phys. Rev. D 111, 066001) as a candidate quantum gravity theory.

**Outcome: FAILS Tier 1 — Not a viable quantum gravity theory.**

The proposal fails on multiple counts:
1. **Not quantum at all** — entirely classical, no Hilbert space, no quantization
2. **Probable ghost problem** — fourth-order equations of motion, no ghost analysis performed
3. **No UV completion** — despite claims, this is classical modified gravity
4. **Phenomenological construction** — the induced metric is designed to reproduce GR by construction

Novelty: The specific idea (action = quantum relative entropy between two metrics) IS genuinely novel. But the output is a classical modified gravity theory. The entire entropic gravity program (Jacobson, Verlinde, Padmanabhan, Bianconi) shares the same fundamental weakness: derives classical Einstein equations from thermodynamic/information arguments but never provides UV completion.

**Key Takeaway:** Move on from Bianconi. Any serious information-theoretic approach to QG must address ghosts, unitarity, and UV completion from the start. The lesson: the "action = relative entropy" idea could be valuable if implemented within an actually quantized framework (e.g., asymptotic safety or path integrals).

## Exploration 003: Lee-Wick Quantum Gravity — Full Viability Assessment

**Goal:** Assess Lee-Wick quantum gravity as a complete theory and compare to QG+F.

**Outcome: FAILED — Lee-Wick QG is not a viable independent theory.**

Key findings:
1. **Unitarity VIOLATED** with Lee-Wick/CLOP prescription above threshold energy (Kubo & Kugo, PTEP 2023). Complex ghosts are actually created.
2. **CLOP breaks Lorentz invariance** at quantum level (Nakanishi 1971, confirmed by Anselmi+Modesto 2025).
3. **Fakeon prescription is the only viable option** — Modesto himself co-authored the 2025 paper (JHEP05(2025)145) concluding this.
4. **Identity problem:** LW QG and QG+F share the SAME action. The only difference is the quantization prescription. Since LW prescription fails, "LW QG with correct prescription" IS QG+F.
5. Six-derivative super-renormalizable variant exists but still requires fakeon — it's "QG+F with better UV behavior," not a novel theory.

**Key Takeaway:** Lee-Wick QG collapses onto QG+F. Any theory sharing the quadratic gravity action is forced to use the fakeon prescription. Must look for theories with fundamentally different propagator structures, not just different prescriptions for the same poles.

## Exploration 004: The n_s Tension — Working Backward from Data to Theory

**Goal:** Assess the CMB spectral index tension (ACT DR6: n_s = 0.974 ± 0.003 vs QG+F n_s ≈ 0.967) and identify what modifications could resolve it.

**Outcome: SUCCEEDED — Clear picture with actionable leads.**

Key findings:
1. **The tension is real but DESI-driven** — CMB alone gives n_s = 0.969 ± 0.003 (barely 1σ tension). The 2.3-3.9σ tension comes from adding DESI BAO data.
2. **The fakeon doesn't help** — QG+F's C² term modifies the tensor sector (r), NOT the scalar sector (n_s). n_s is determined by the R² term (Starobinsky inflation).
3. **Three viable modifications identified:**
   - R³ curvature correction (δ₃ ≈ −10⁻⁴): natural in six-derivative gravity, resolves tension exactly
   - RG running of R² coupling (γ ≈ 0.007): equivalent to R^(2−2γ), motivated by AS and perturbative QG running
   - Radiative corrections from matter coupling: model-dependent
4. **Physical beta functions now available** (Branchina et al. 2024 PRL): gauge-invariant beta functions for quadratic gravity make the RG running calculation unambiguous for the first time.

**Key Takeaway:** The single most valuable next step is computing n_s from QG+F's known physical beta functions. This is a well-defined, no-free-parameter calculation that could either confirm or challenge QG+F. The six-derivative extension (R³ term) provides a natural backup if perturbative RG running doesn't produce enough shift.


## Exploration 005: n_s from QG+F Beta Functions and Six-Derivative Extension

**Goal:** Determine if RG running of R² coupling can shift n_s by +0.007, and evaluate six-derivative extension.

**Outcome: SUCCEEDED — Clear quantitative answers.**

Key findings:
1. **RG running CANNOT resolve the tension** — Physical beta functions give Δθ/θ ~ 10⁻¹⁴ during inflation. Twelve orders of magnitude too small. Robust result.
2. **R³ extension DOES resolve it** — Cubic curvature correction with δ₃ = −1.19×10⁻⁴ gives n_s ≈ 0.974, r ≈ 0.0045. Moderately natural (new physics at ~3×10¹⁵ GeV).
3. **Physical beta functions:** β_λ = −(1617λ−20ξ)λ/(90×16π²), β_ξ = −(ξ²−36λξ−2520λ²)/(36×16π²)
4. **Six-derivative theory:** 10 independent couplings in 4D, super-renormalizable, fits within QG+F framework as next-order EFT correction.

**Key Takeaway:** RG running is a dead end for n_s. The R³ (six-derivative) extension is the path forward. The finding that running is negligible means QG+F predictions are robust. If n_s ≈ 0.974 is confirmed, it points to six-derivative QG+F with one new parameter δ₃ ~ 10⁻⁴.


## Exploration 006: Cosmological Constant Problem in QG+F

**Goal:** Investigate everpresent-Λ mechanism import and alternative CC approaches within QG+F.

**Outcome: Clear negative result with constructive recommendations.**

Key findings:
1. **Everpresent-Λ cannot be imported into QG+F** — mechanism requires discrete Poisson fluctuations (δV ~ √V). No continuum analogue exists. Perturbative path-integral fluctuations give wrong scaling.
2. **Everpresent-Λ has observational problems** — only 0.017% of seeds fit SN Ia, CMB fits worse than ΛCDM, ISW effect kills most realizations.
3. **Unimodular QG+F solves old CC problem** — Salvio 2024 showed compatibility. Vacuum energy doesn't gravitate. But debate on whether this genuinely solves or just reformulates.
4. **No approach within QG+F predicts Λ ~ 10⁻¹²²** — AS, Kaloper-Padilla, six-derivative extension all fail to predict the value.

**Key Takeaway:** The CC problem is the Achilles heel of ALL continuum QFT approaches. Best QG+F can do: unimodular formulation (old CC solved, Λ = integration constant). Explaining Λ ~ 10⁻¹²² likely requires discreteness, anthropics, or unknown mechanism. Don't over-invest in CC — it puts QG+F on equal footing with every other approach.


## Exploration 007: Non-Perturbative QG+F — Gravitational Confinement Analogy

**Goal:** Investigate how far QCD-gravity analogy extends and identify non-perturbative predictions.

**Outcome: SUCCEEDED — Clear map of non-perturbative predictions.**

Key findings:
1. **Ghost confinement conjecture (Holdom-Ren):** The spin-2 ghost is removed by non-perturbative effects; fakeon = perturbative shadow of confinement. Unproven but structurally motivated.
2. **Four predictions invisible to perturbative QG+F:**
   - Planck-mass BH remnants (potential dark matter)
   - Power-law running of G at cosmological scales (Hamber lattice gravity)
   - Inflation without inflaton (Reuter FP drives inflation, r up to ~0.01 vs QG+F's <0.004)
   - Higgs mass prediction (Shaposhnikov-Wetterich, m_H ≈ 126 GeV)
3. **CDT phase diagram:** Rich structure with second-order B-C transition as candidate UV critical point.
4. **Mass gap in R² gravity** demonstrated via Dyson-Schwinger (2025).

**Key Takeaway:** Sharpest discriminator between perturbative QG+F and non-perturbative AS: tensor-to-scalar ratio. AS inflation predicts r up to ~0.01, QG+F predicts r < 0.004. CMB-S4/LiteBIRD can distinguish in 2030s. Also: a March 2026 paper (arXiv:2603.07150) claims IHO interpretation of ghost resolves CMB anomalies — needs scrutiny.


## Exploration 008: Full Validation of Six-Derivative QG+F (R³ Extension)

**Goal:** Complete Tier 1-4 validation of six-derivative QG+F.

**Outcome: PASSES ALL FOUR TIERS.**

Key findings:
1. **Tier 1 (Structural):** 14 DOF (vs 8 in QG+F). Ghosts resolved via complex-mass pairs + fakeon. Super-renormalizable (one-loop divergences only). Asymptotically free. Unitarity proven (Piva 2023).
2. **Tier 2 (Known Physics):** GR recovered, PPN correct, GW speed = c.
3. **Tier 3 (Precision):** Wald BH entropy well-defined. **d_s = 4/3** (vs 2 for QG+F). Stelle potential with extra Yukawa terms.
4. **Tier 4 (Predictions):** n_s ≈ 0.974, r ≈ 0.0045, α_s ≈ −0.0008. All testable by LiteBIRD/CMB-S4 ~2032.
5. **Not a novel theory** — it's the next term in the EFT expansion of QG+F, adding one new parameter δ₃.
6. **Open question:** Is δ₃ ~ 10⁻⁴ predicted by the RG structure or must be fit?

**Key Takeaway:** Six-derivative QG+F is QG+F's natural next-order correction. Passes validation, fixes n_s, but adds one parameter. The UV spectral dimension d_s = 4/3 is a notable difference from QG+F's d_s = 2.


## Exploration 009: Entanglement Equilibrium as UV Axiom — Construction Attempt

**Goal:** Attempt to construct a UV-complete QG theory from Jacobson's maximal vacuum entanglement hypothesis.

**Outcome: The construction produces QG+F, not a novel theory.**

Key findings:
1. **Self-consistency bootstrap uniquely selects QG+F:** MVEH links UV entanglement to gravitational equations. Self-consistency + renormalizability → quadratic gravity + fakeon.
2. **MVEH only gives linearized equations** for higher-derivative gravity (Bueno et al. 2017). Full nonlinear action needs renormalizability as additional input.
3. **Alternative axioms (QFC, relative entropy, modular flow) all converge on QG+F.** Most elegant: MVEH + modular flow unitarity → fakeon prescription (novel derivation of why ghost must be fakeon).
4. **Path to genuine novelty:** would require non-perturbative, background-independent entanglement structures beyond standard QFT.

**Key Takeaway:** Entanglement approach provides beautiful alternative DERIVATION of QG+F but cannot produce an alternative THEORY. QG+F's uniqueness reinforced from yet another direction.

## Exploration 010: IHO Ghost Paper and CMB Predictions Catalog

**Goal:** Scrutinize March 2026 IHO ghost paper, catalog all CMB predictions, build AS vs QG+F discrimination table.

**Outcome: SUCCEEDED — Complete assessment.**

Key findings:
1. **IHO paper:** Creative but not credible. Ad hoc sign flip, unitarity argued not proven, 650x Bayes factor methodology-dependent. Competing (not compatible) with fakeon.
2. **QG+F CMB predictions:** Nearly indistinguishable from Starobinsky beyond n_s and r. α_s ≈ −6.5×10⁻⁴, n_T = −r/8, f_NL ~ 10⁻⁴.
3. **r is the SOLE realistic discriminator:** QG+F: r < 0.005. AS: r up to ~0.01. If r > 0.005 → AS favored. If r < 0.003 → QG+F favored.
4. **CMB-S4 CANCELLED (July 2025).** Discrimination timeline: SO enhanced ~2030-2034 (earliest), LiteBIRD ~2036-2037 (definitive).

**Key Takeaway:** r is the only realistic test. LiteBIRD gives definitive answer ~2037. CMB-S4 cancellation is a setback but not fatal.


## Exploration 011: Black Hole Predictions in QG+F

**Goal:** Catalog all BH predictions in QG+F and six-derivative extension.

**Outcome: QG+F makes NO testable BH predictions for astrophysical BHs.**

All corrections suppressed by (l_P/r_H)² ~ 10⁻⁷⁶ to 10⁻⁹⁶. Static BHs are Schwarzschild under fakeon. Wald entropy = A/(4G) + negligible. QNMs include massive spin-2 but purely virtual under fakeon. Singularity NOT resolved perturbatively; only AS resolves it non-perturbatively.

**Key Takeaway:** BH sector is QG+F's weakest. Fakeon eliminates ghost from physical spectrum → eliminates all classical BH modifications. Testable predictions entirely in CMB sector.

## Exploration 012: QG+F and Standard Model Connections

**Goal:** Investigate QG+F connections to particle physics.

**Outcome: The QG+F/AS program has ONE confirmed particle physics prediction (Higgs mass).**

Key findings:
1. QG+F does NOT predict SM gauge group or constrain matter content. f₂ AF for any matter.
2. Shaposhnikov-Wetterich m_H ≈ 126 GeV (2010, before discovery) is the most impressive success. Non-perturbative AS result.
3. Agravity (Salvio-Strumia) IS QG+F with classical scale invariance + SM. Addresses hierarchy via technical naturalness.
4. Fakeon collider phenomenology severely limited — near Planck mass.
5. AS grand unification (Eichhorn-Held) most promising for future SM predictions.

**Key Takeaway:** QG+F/AS is the ONLY QG framework with a confirmed particle physics prediction. Strong constraints come from non-perturbative AS, not perturbative QG+F.


## Exploration 013: Dimensional Transmutation and CC in Agravity

**Outcome: CC cannot be predicted in agravity/QG+F.** CW mechanism gives Λ=0 at tree level; one-loop gives 10⁻³⁴ M_P⁴ (88 orders too large). Cascading transmutation is numerology without physical mechanism. Unimodular + anthropics is the best available.

## Exploration 014: Non-CMB Experimental Signatures

**Outcome: ALL non-CMB signatures undetectable.** 15-order gap between probe energies and QG+F mass scales. GW, table-top, cosmological, and scattering signatures all Planck-suppressed. QG+F is effectively a one-prediction theory: r from CMB. The r measurement by LiteBIRD (~2036-2037) is the only game in town.


## Exploration 015: QG+F Uniqueness Theorem

**Outcome:** 8 independent derivation paths all lead to QG+F. Minimal axiom set: {Lorentz, diffeo, locality, perturbative renormalizability, unitarity}. QG+F is the quantum-gravitational Lovelock theorem — the unique perturbative quantum gravity in 4D. Escape routes fully mapped.

## Exploration 016: Complete Theory Synthesis

**Outcome:** Full theory assembled: QG+F + six-derivative + unimodular + agravity-SM. ~50 parameters. 17 predictions total: 2 confirmed (m_H, vacuum near-criticality), 4-6 testable by 2037 (r, n_s, α_s). QG+F is the only QG framework with both a confirmed prediction and a near-term falsifiable test. Strategy-002 contributions: entanglement bootstrap derivation, six-derivative n_s resolution, uniqueness from 3 angles, definitive elimination of alternatives.

