# Exploration 010: The IHO Ghost Interpretation and Novel CMB Signatures

## Goal
Four tasks: (1) Scrutinize the March 2026 IHO ghost paper (arXiv:2603.07150), (2) Catalog all QG+F CMB predictions beyond n_s and r, (3) Construct an AS vs QG+F discrimination table, (4) Map the experimental timeline for testing.

## Status: COMPLETE

---

## Task 1: The IHO Ghost Paper (arXiv:2603.07150)

### 1.1 Paper Overview

**Title:** "Quantum (quadratic) gravity: replacing the massive tensor ghost with an inverted harmonic oscillator-like instability"
**Authors:** K. Sravan Kumar, Joao Marto
**Date:** March 7, 2026
**Framework:** Direct-Sum Quantum Field Theory (DQFT)

### 1.2 The IHO Interpretation — Mechanism

The central claim is that the massive spin-2 ghost in quadratic gravity (the mode from the Weyl-squared C² term) can be reinterpreted not as a ghost (negative-norm state) but as an **inverted harmonic oscillator (IHO)-like instability**. The key distinction:

| Mode Type | Hamiltonian | Behavior | Particle? |
|-----------|------------|----------|-----------|
| **Ghost** | H = -ω/2(p² + q²) | Negative definite, unbounded below | Yes (negative norm) |
| **IHO** | H = ω/2(p² - q²) | Indefinite but Hermitian | No — hyperbolic evolution |
| **Dual IHO** | H = ω/2(-p² + q²) | Indefinite but Hermitian | No — the actual spin-2 mode |

**The physical mechanism:** By flipping the sign of the Weyl-squared coefficient in the action, the ghost mode is transformed into a mode with:
- **Hyperbolic (exponential) evolution** instead of oscillatory
- **Spacelike momentum support** (k² > 0), meaning it cannot go on-shell as a particle
- **No asymptotic particle interpretation** — it contributes only virtually

The mode is quantized within DQFT using **geometric superselection sectors**: the phase space splits into four regions related by discrete PT symmetries, with the Hilbert space decomposing as H = H_(+E) ⊕ H_(-E). Sectors related by time-reversal have opposite commutation relations:

[Q_III, P_III] = iℏ  vs.  [Q_IV, P_IV] = -iℏ

### 1.3 Comparison to Fakeon Prescription

| Feature | Fakeon (Anselmi) | IHO/DQFT (Sravan Kumar) |
|---------|-----------------|------------------------|
| Ghost treatment | Modified Feynman prescription (no -iε) | Structural reinterpretation of the mode |
| Mechanism | Kinematic: ghost projected out of spectrum | Dynamic: mode has no particle interpretation |
| Unitarity | Proven perturbatively | Argued via geometric superselection |
| Ghost appears as | "Purely virtual particle" | "IHO-like instability" |
| Hamiltonian | Not modified | Modified sign structure |
| Particle content | Ghost removed by prescription | No ghost to begin with |
| Status | Well-established (many papers, >150 citations/yr) | New proposal (March 2026) |

**Key difference:** The fakeon approach keeps the standard action but modifies the quantization prescription (the integration contour in the propagator). The IHO/DQFT approach modifies the interpretation of the mode itself — it's not a ghost at all, but a healthy IHO instability. These are **competing interpretations**, not compatible frameworks.

### 1.4 CMB Anomalies and Statistical Evidence

The paper builds on Sravan Kumar's earlier work on "Direct-Sum Inflation" (DSI), which claims to explain three longstanding CMB anomalies:

1. **Parity asymmetry** — Unequal power in even vs. odd multipoles at large angular scales
2. **Low quadrupole moment** — Suppressed ℓ=2 power relative to ΛCDM predictions
3. **Hemispherical power asymmetry** — Power dipole favoring one sky hemisphere

**The 650× statistical evidence claim:** A Bayesian evidence ratio (Bayes factor) comparing DSI to standard inflation:

B = P(data|DSI) / P(data|ΛCDM) ≈ 50-650

depending on which statistics are combined. Using combined parity + low-ℓ power spectrum statistics, DSI is claimed to be up to 650× more probable than standard inflation. This uses Planck 2018 temperature and polarization data.

**Critical assessment of the 650× claim:**
- The Bayes factor is computed using P(M|D) rather than the standard P(D|M), which the authors argue "undermines the importance of low-ℓ physics"
- The range 50-650× depends heavily on which anomaly statistics are combined
- No independent group has reproduced this analysis
- The anomalies themselves are at ~2-3σ level individually — not statistically overwhelming
- The Bayesian framework choice (prior-dependent) introduces model-selection ambiguity

### 1.5 Specific Predictions

The IHO paper claims:
- Modified tensor-to-scalar ratio (relative to pure Starobinsky) — the IHO spin-2 mode modifies r "in a predictive manner"
- Parity-odd oscillations in the tensor power spectrum at large scales
- No extra propagating degrees of freedom visible in CMB or primordial GWs
- Large-scale correlations in primordial gravitational waves

However, **no explicit numerical predictions** are provided for n_s, r, or other standard observables in the paper itself. The quantitative predictions are deferred to the earlier DSI papers and future work.

### 1.6 Unitarity Assessment

The unitarity argument is:
1. The IHO mode has spacelike momentum support → cannot go on-shell
2. Unitarity cutting rules (Optical Theorem) exclude spacelike momentum contributions
3. Geometric superselection ensures pure states evolve to pure states
4. The asymptotic spectrum contains only the massless graviton and scalaron

**Assessment:** This is argued constructively, not proven via theorem. The argument is physically plausible but has not been subjected to the same level of scrutiny as the fakeon unitarity proofs (which are perturbatively rigorous to all loop orders).

### 1.7 Riemann Zeta Connection

An intriguing mathematical aside: the IHO quantization connects to the Riemann zeta function. The Berry-Keating quantization gives a spectral density:

N(E) = (|E|/2πℏ)[ln(|E|/2πℏ) - 1] + 7/8

which matches the Riemann zero density. This is mathematically interesting but physically speculative — the Hilbert-Polya connection to the Riemann Hypothesis remains unproven.

### 1.8 Critical Assessment — Overall Verdict

**Strengths:**
- Addresses a genuine problem (the ghost in quadratic gravity) with a novel approach
- The IHO interpretation is mathematically coherent (Hermitian Hamiltonian, unitary evolution within sectors)
- Connection to CMB parity asymmetry is observationally motivated
- The DQFT framework has been developed over several papers (not just this one)

**Weaknesses:**
- **The sign flip is ad hoc.** Changing the sign of the Weyl-squared coefficient changes the theory — it's no longer the same quadratic gravity. The ghost is a prediction of the standard theory; removing it by changing the sign is not a resolution.
- **Competing with well-established fakeon approach.** The fakeon prescription has been proven to preserve unitarity to all perturbative orders. The IHO/DQFT approach is newer and less tested.
- **The 650× Bayes factor is not robust.** It depends on Bayesian methodology choices, and the underlying anomalies are individually not highly significant (~2-3σ).
- **No independent verification.** Only the authors' group has developed DQFT and applied it to CMB.
- **Geometric superselection sectors are exotic.** The interpretation of "two arrows of time" and loss of conventional temporal ordering is conceptually radical without strong physical motivation beyond the ghost problem.
- **Limited quantitative predictions.** The paper provides no specific numerical values for standard observables beyond qualitative modifications.

**Verdict: INTERESTING BUT NOT YET CREDIBLE AS A BREAKTHROUGH.** The IHO interpretation is a creative approach to the ghost problem, but it requires:
1. Independent verification of the DQFT framework
2. Explicit numerical predictions for r, n_s, etc. that can be compared to data
3. Demonstration that unitarity holds to all orders (not just argued)
4. Explanation of why the sign of C² should be flipped

The fakeon approach remains more robust and better established. The CMB anomaly connection is intriguing but not yet at the level of a definitive test.

---

## Task 2: Complete Catalog of QG+F CMB Predictions

### 2.1 Framework: R + R² + C² with Fakeon Prescription

The theory is:
S = ∫d⁴x √g [R/(16πG) + (1/2m₀²)R² - (1/2m₂²)C²]

where the C² ghost is treated as a fakeon (purely virtual particle). Inflation is driven by the R² term (Starobinsky mechanism), with the C² term providing quantum gravity corrections.

The key parameters are:
- **m₀**: mass of the scalar (inflaton/scalaron) from R²
- **m₂ = m_χ**: mass of the spin-2 fakeon from C²
- **N**: number of e-foldings (~50-60)
- **α = 1/(4πN)**: the inflationary running coupling (~1/115 for N~55)

### 2.2 Predictions Catalog

#### Scalar Spectral Index: n_s

**Pure Starobinsky (no C² corrections):**
n_s = 1 - 2/N ≈ 0.964 (N=55) to 0.967 (N=60)

**QG+F (with C² corrections):**
The C² term provides subleading corrections proportional to α = 1/(4πN). To leading order, n_s is the same as Starobinsky:
- n_s ≈ 1 - 2/N + O(α²) ≈ 0.964-0.967

**Six-derivative extension (from Exploration 008):**
- n_s ≈ 0.974 (from the additional R³/C□C terms, with δ₃ ≈ -10⁻⁴)

#### Tensor-to-Scalar Ratio: r

**Pure Starobinsky:**
r = 12/N² ≈ 0.004 (N=55) to 0.0033 (N=60)

**QG+F (with C² corrections):**
The leading-order prediction is bounded by:
4/3 < N²r < 12

which gives:
- r_min = 4/(3N²) ≈ 0.00044 (N=55)
- r_max = 12/N² ≈ 0.004 (N=55)

The actual value depends on the ratio m_χ/m₀:
- When m_χ >> m₀: r → 12/N² (pure Starobinsky limit)
- When m_χ → m₀/4 (lower bound): r → 4/(3N²) ≈ 0.00044
- Constraint: m_χ > m₀/4 (from causality/consistency)

The C² correction factor is: r ≃ 3(1 - β/6α)(n_s - 1)² where β parameterizes the C² strength relative to R².

**Six-derivative extension:**
- r ≈ 0.0045

#### Running of the Spectral Index: α_s = dn_s/d ln k

**Pure Starobinsky:**
α_s = -2/N² ≈ -6.6 × 10⁻⁴ (N=55)

**QG+F:**
α_s ≃ -(1/2)(n_s - 1)² ≈ -6.5 × 10⁻⁴

This is essentially the same as Starobinsky to leading order. The C² corrections enter at O(α³) ≈ 10⁻⁶, well below any foreseeable measurement precision.

**Six-derivative extension:**
α_s ≈ -8 × 10⁻⁴ (slightly larger magnitude due to the extra derivative terms)

#### Running of the Running: β_s = dα_s/d ln k

**Pure Starobinsky:**
β_s = 4/N³ ≈ 2.4 × 10⁻⁵ (N=55)

**QG+F:**
β_s ≈ 4/N³ + O(α⁴) ≈ 2.4 × 10⁻⁵

Again, indistinguishable from Starobinsky at any foreseeable precision.

#### Tensor Spectral Tilt: n_T

**Pure Starobinsky:**
n_T = -r/8 ≈ -5 × 10⁻⁴ (consistency relation)

**QG+F:**
The consistency relation r ≈ -8n_T is NOT affected by the C² term to leading order:
n_T ≈ -r/8

The first correction was computed by Anselmi (2021, JCAP 01 048):
r + 8n_T = O(α²) ≈ 10⁻⁴

This tiny violation of the standard consistency relation is a distinctive QG+F prediction, but it is far below any foreseeable measurement precision.

**Six-derivative extension:**
The C□C term modifies the tensor propagator differently from C². The tensor tilt receives corrections from the new spin-2 modes, but the modification to the consistency relation remains tiny.

#### Non-Gaussianity: f_NL

**Pure Starobinsky:**
f_NL ~ O(slow-roll parameters) ≈ O(1/N²) ~ 10⁻⁴

This is the standard single-field inflation prediction: negligible non-Gaussianity.

**QG+F:**
No published explicit calculation of f_NL from the C² correction exists in the literature. However, the fakeon enters only through loop corrections to the scalar bispectrum, which are suppressed by α ~ 1/115. The expected contribution is:
f_NL(QG+F) ~ O(α/N) ~ 10⁻⁴

This is unmeasurably small. Planck constrains f_NL^local = -0.9 ± 5.1, and CMB-S4 would achieve σ(f_NL) ~ 1, both far above the QG+F prediction.

**Six-derivative extension:**
Similarly negligible. Multi-field inflation (QG+F coupled to a scalar with quadratic potential, the φ² model) could produce larger non-Gaussianity, but this is a model-dependent choice, not a prediction of the gravity theory itself.

#### Isocurvature Modes

**QG+F (standard):**
No isocurvature modes. Single-field inflation from R² produces only adiabatic perturbations.

**QG+F (unimodular extension):**
If unimodular gravity is adopted (trace-free Einstein equations), the cosmological constant appears as an integration constant, which could introduce isocurvature modes during the transition from inflation to radiation domination. However, this is speculative and no detailed calculation exists.

**Multi-field QG+F:**
If φ² inflation is combined with R+R²+C², the second scalar field can produce isocurvature modes. Anselmi et al. (2021, arXiv:2105.05864) studied this: the scalar mixing affects only subleading corrections, confirming single-field predictions to leading order.

#### Spectral Features from the Ghost/Fakeon Sector

**QG+F:**
The fakeon produces no spectral features at leading order — it contributes only through virtual corrections that modify the overall amplitude and tilt smoothly. No oscillatory features, no bumps, no steps.

**IHO/DQFT (Sravan Kumar):**
Claims parity-odd oscillations in the tensor power spectrum at large angular scales. This is the one observable that could distinguish the IHO interpretation from the fakeon prescription — but it's specific to the DQFT framework, not to standard QG+F.

### 2.3 Summary Predictions Table

| Observable | Pure Starobinsky | QG+F (4-deriv) | QG+F (6-deriv) | Current Data |
|-----------|-----------------|----------------|----------------|--------------|
| n_s | 1 - 2/N ≈ 0.964 | ≈ 0.964-0.967 | **≈ 0.974** | 0.9682 ± 0.0032 |
| r | 12/N² ≈ 0.004 | 0.0004-0.004 | **≈ 0.0045** | < 0.034 (95%) |
| α_s | -2/N² ≈ -6.6×10⁻⁴ | ≈ -6.6×10⁻⁴ | ≈ -8×10⁻⁴ | -0.0045 ± 0.0067 |
| β_s | 4/N³ ≈ 2.4×10⁻⁵ | ≈ 2.4×10⁻⁵ | ~ 10⁻⁵ | Not constrained |
| n_T | -r/8 ≈ -5×10⁻⁴ | ≈ -r/8 + O(10⁻⁴) | ≈ -r/8 | Not measured |
| f_NL | ~ 10⁻⁴ | ~ 10⁻⁴ | ~ 10⁻⁴ | -0.9 ± 5.1 |
| Isocurvature | None | None | None | < 0.038 (95%) |
| Parity features | None | None | None | ~2-3σ anomaly |

---

## Task 3: AS vs QG+F Discrimination Table

### 3.1 The Key Distinction

**QG+F (perturbative quadratic gravity with fakeon)** drives inflation via the R² Starobinsky mechanism. The C² term provides quantum gravity corrections that are perturbatively small (suppressed by α = 1/(4πN) ~ 1/115).

**AS (asymptotic safety)** drives inflation via the Reuter non-Gaussian fixed point — a non-perturbative mechanism where the running cosmological constant at the fixed point provides the effective inflaton. No explicit inflaton field is needed.

The two approaches make overlapping but distinct predictions because:
- QG+F is a perturbative expansion around the Starobinsky solution
- AS involves non-perturbative RG running that modifies the Starobinsky predictions

### 3.2 AS Inflation Predictions (Bonanno-Platania Framework)

The AS effective Lagrangian (Bonanno & Platania 2018, PRD 98, 043505):
L_eff = M_P² R/2 + (a/2) R²/[1 + b ln(R/μ²)]

where b parameterizes the strength of AS corrections to Starobinsky inflation. Key results:

**For b → 0 (pure Starobinsky):**
- n_s = 1 - 2/N ≈ 0.964-0.967
- r = 12/N² ≈ 0.003-0.004
- α_s ≈ -5 × 10⁻⁴

**For b ~ 10⁻³ (maximal AS corrections consistent with Planck):**
- n_s increases toward ~0.97
- r increases up to ~0.01
- α_s ≈ -5 × 10⁻⁴ (unchanged to this precision)

**The critical finding:** r is the sharpest discriminator. AS allows r up to ~0.01, while QG+F constrains r < 0.004.

### 3.3 The Emergent Cosmology Model (Bonanno et al. 2025)

The running Newton constant model (PRD 111, 103519, 2025; arXiv:2405.02636) uses:
G(ε) = G_N / (1 + ε/ε_c) with ε_c determined by g* = 540π/833

This produces a quasi-de Sitter phase at early times that naturally transitions to standard cosmology. The transition scale ε_c is a new observable constrained by CMB data. However, explicit n_s and r predictions have not yet been published for this model.

### 3.4 Discrimination Table

| Observable | QG+F (4-deriv) | QG+F (6-deriv) | AS (Reuter FP) | Discriminating? |
|-----------|----------------|----------------|----------------|-----------------|
| **n_s** | 0.964-0.967 | ~0.974 | 0.964-0.97 | WEAK — overlapping ranges |
| **r** | **0.0004-0.004** | ~0.0045 | **up to 0.01** | **YES — SHARPEST** |
| **α_s** | ~-6.5×10⁻⁴ | ~-8×10⁻⁴ | ~-5×10⁻⁴ | NO — below measurement precision |
| **β_s** | ~2.4×10⁻⁵ | ~10⁻⁵ | ~10⁻⁵ | NO — unmeasurable |
| **n_T** | -r/8 | -r/8 | -r/8 (likely) | NO — both satisfy consistency relation |
| **f_NL** | ~10⁻⁴ | ~10⁻⁴ | ~10⁻⁴ | NO — both negligible |
| **Inflaton needed?** | Yes (R² scalaron) | Yes | **No** | YES — conceptual, not directly observable |
| **Running G at cosmic scales** | Logarithmic, tiny (~10⁻¹⁴) | Same | **Power-law, potentially observable** | YES — via precision cosmology |
| **BH remnants** | No prediction | No prediction | **Planck-mass remnants** | YES — via PBH dark matter |
| **Higgs mass prediction** | No | No | **~126 GeV (Shaposhnikov-Wetterich)** | YES — but already observed |
| **Spectral dimension (UV)** | d_s = 2 | d_s = 4/3 | d_s ~ 2 | WEAK — not directly observable |
| **Consistency relation violation** | r + 8n_T ~ 10⁻⁴ | Similar | Unknown | NO — too small to measure |
| **Speed of sound modification** | c_t/c_s = 1 + β/(6α) | Modified | Standard (c_t = c_s = 1?) | POSSIBLY — if precision improves |

### 3.5 The r Discriminator — Detailed Analysis

The tensor-to-scalar ratio is the cleanest discriminator because:

**QG+F prediction:**
- r ∈ [0.0004, 0.004] (4-derivative)
- r ≈ 0.0045 (6-derivative)
- Upper bound: r < 0.005 in all variants

**AS prediction (Bonanno-Platania):**
- r ∈ [0.003, 0.01] depending on b parameter
- For b ~ 10⁻³: r ≈ 0.01
- For b → 0: r → 0.003-0.004 (converges to Starobinsky)

**The discrimination window:**
- If r > 0.005: Favors AS over QG+F
- If 0.003 < r < 0.005: Ambiguous — both allowed
- If r < 0.003: Favors QG+F over simplest AS models
- If r < 0.0004: Only QG+F with heavy fakeon consistent

**Current experimental status:** r < 0.034 (95% CL, BICEP/Keck + Planck 2021)
**Required precision to discriminate:** σ(r) < 0.002, ideally σ(r) ~ 0.001

### 3.6 Other Potential Discriminators

**1. Speed of sound during inflation:**
QG+F predicts a modified speed of tensor perturbations relative to scalar: c_t/c_s ≃ 1 + β/(6α), where β parameterizes the C² strength. This is a unique signature of the C² term, but the correction is tiny (proportional to slow-roll parameters) and likely unmeasurable.

**2. Blue-tilted tensor spectrum:**
A December 2024 paper (JHEP 12 (2024) 024) proposes that certain UV-complete quantum gravity theories with Weyl invariance predict a blue-tilted tensor spectrum (n_T > 0), with r₀.₀₅ ≈ 0.01 detectable by BICEP Array and LiteBIRD. This would be dramatically different from both QG+F and standard AS predictions (which both predict n_T < 0). However, this is a different framework (not standard QG+F or AS).

**3. Stochastic gravitational wave background:**
The stochastic GW background is sensitive to small variations in the tensor tilt and running. Future space-based detectors (DECIGO) could potentially measure n_T with enough precision to distinguish models, but this is decades away.

---

## Task 4: Experimental Timeline

### 4.1 Current Status (March 2026)

| Experiment | Status | Best r Constraint |
|-----------|--------|------------------|
| BICEP/Keck (2021 data) | Published | r < 0.034 (95% CL) |
| Planck (2018 data) | Published | r < 0.10 (95% CL, alone) |
| ACT DR6 | Published (2025) | n_s = 0.9682 ± 0.0032 |
| SPT-3G | Operating | Improving |
| Simons Observatory | **3 SATs operational since 2024** | First r results pending |

### 4.2 Near-Term: 2026-2028

**Simons Observatory (SO):**
- 3 SATs began observations in April-June 2024
- LAT first light in March 2025
- First r results expected ~2026-2027
- Target: σ(r) ≤ 0.003 with 3 SATs (nominal 5-year survey)
- 3 additional SATs being deployed by 2027 (total: 6 SATs)

**BICEP Array:**
- High-frequency receiver installed 2024-2025
- Target: σ(r) ≤ 0.003 with data through 2027 observing season
- Results expected ~2028

**What these can test:**
- If r > 0.01: Detectable by SO and BICEP Array → strong AS signal
- If r ~ 0.003-0.005: Marginal detection possible → ambiguous
- If r < 0.003: Upper limit → consistent with QG+F, constrains AS

### 4.3 Medium-Term: 2028-2035

**Simons Observatory (enhanced):**
- 6 SATs + extended survey to mid-2030s
- Forecasted: σ(r) = 0.0012 (conservative, 10 years)
- Optimistic: σ(r) = 0.0007 (with 70% delensing)
- This is the **first experiment that can distinguish QG+F from AS** if r ~ 0.005-0.01

**LiteBIRD (JAXA):**
- Launch: JFY 2032 (early 2033)
- 3-year survey from Sun-Earth L2
- Target: σ(r) < 0.001 (including systematics)
- Sensitivity: 2.2 μK-arcmin at 0.5° resolution
- 15 frequency bands (34-448 GHz)
- **First results: ~2036-2037**

### 4.4 CMB-S4: CANCELLED

**Critical development:** In July 2025, the U.S. DOE and NSF jointly withdrew support for CMB-S4. The project is undergoing orderly shutdown.

- Original plan: σ(r) ≈ 0.0005, operations starting 2032-2033
- A revised half-cost Chile-only plan was proposed (June 2025) but rejected
- The CMB-S4 Science Collaboration (independent of the project) is developing alternative plans

**Impact on QG vs AS discrimination:**
CMB-S4 was expected to be the definitive experiment for discriminating QG+F from AS. With its cancellation:
- LiteBIRD becomes the primary space mission (σ(r) ~ 0.001)
- SO enhanced becomes the primary ground experiment (σ(r) ~ 0.0007-0.0012)
- The discrimination timeline shifts from "definitive by 2035" to "possible but less precise by 2036-2037"

### 4.5 Long-Term: 2035+

| Experiment | Sensitivity | Timeline | Key Observable |
|-----------|-------------|----------|---------------|
| SO (10yr, 6 SATs) | σ(r) ~ 0.001 | 2034 | r discrimination |
| LiteBIRD | σ(r) < 0.001 | 2036-2037 | r discrimination |
| LISA | GW at mHz | 2037 | Phase transitions |
| DECIGO | GW at 0.1-10 Hz | 2040s | n_T measurement |

### 4.6 Timeline for Each Discriminating Observable

| Observable | Required Precision | Experiment | Expected Date |
|-----------|-------------------|------------|---------------|
| **r (primary)** | σ(r) ~ 0.001 | LiteBIRD + SO | **2034-2037** |
| **n_s (secondary)** | σ(n_s) ~ 0.001 | LiteBIRD + SO + Euclid | **2035+** |
| **α_s (running)** | σ(α_s) ~ 10⁻⁴ | Would need CMB-S4+ | **Not feasible before 2040** |
| **n_T (tensor tilt)** | σ(n_T) ~ 10⁻³ | DECIGO | **2040s** |
| **f_NL** | σ(f_NL) ~ 0.01 | Galaxy surveys (SPHEREx) | **Not testable** (prediction ~10⁻⁴) |
| **Running G** | Δ(G)/G ~ 10⁻⁴ | Precision cosmology | **2030s+** |
| **BH remnants** | PBH dark matter signal | LISA, future GW | **2037+** |

### 4.7 The "First Testable Prediction" Timeline

**First opportunity (2027-2028):** BICEP Array results with σ(r) ~ 0.003
- Can detect r > 0.01 (strong AS signal)
- Cannot discriminate if r < 0.005

**Second opportunity (2030-2032):** SO enhanced (5+ years data) with σ(r) ~ 0.001-0.002
- Can discriminate between r = 0.003 (QG+F) and r = 0.01 (AS)
- **This is the earliest date for definitive discrimination**

**Third opportunity (2036-2037):** LiteBIRD first results with σ(r) < 0.001
- Definitive measurement of r down to 0.001
- Can distinguish all variants of QG+F from AS
- **Most reliable discrimination date**

---

## Synthesis and Conclusions

### Key Findings

1. **The IHO ghost paper (arXiv:2603.07150) is interesting but not a breakthrough.** It proposes an alternative to the fakeon prescription by reinterpreting the ghost as an IHO-like instability within the DQFT framework. The CMB parity asymmetry connection is observationally motivated (Bayes factor 50-650×), but the statistical evidence is not robust, the sign-flip is ad hoc, and no explicit numerical predictions for standard observables are provided. The fakeon approach remains more rigorous.

2. **QG+F CMB predictions are sharply defined but hard to distinguish from Starobinsky.** Beyond n_s and r, all other observables (α_s, β_s, n_T, f_NL) are indistinguishable from pure Starobinsky inflation at any foreseeable experimental precision. The C² corrections enter at O(α) ~ 1/115, making them tiny. The only exception is the overall range of r, which depends on the fakeon mass m_χ.

3. **The tensor-to-scalar ratio r is the sole realistic discriminator between QG+F and AS.** AS allows r up to ~0.01; QG+F constrains r < 0.005. The running α_s and tensor tilt n_T are both too small to measure. Non-Gaussianity is negligible in both.

4. **CMB-S4's cancellation (July 2025) is a significant setback.** The discrimination timeline shifts from "definitive by 2035" to "possible by 2034, definitive by 2037" via SO enhanced + LiteBIRD. The σ(r) ~ 0.0005 precision of CMB-S4 is irreplaceable in the near term.

5. **The experimental timeline for discrimination is ~2030-2037.** The earliest possible discrimination is ~2030 (SO enhanced, 5+ years data); the most reliable is ~2036-2037 (LiteBIRD first results). A measurement of r > 0.005 would favor AS; r < 0.003 would favor QG+F.

### What Would Change the Picture

- **If the IHO/DQFT framework develops explicit quantitative predictions** distinguishable from the fakeon framework, it could become a third competitor
- **If the CMB parity anomaly strengthens** with future data (Planck reanalysis, SO), it would boost the IHO/DQFT case
- **If CMB-S4 is revived** (in any form), the discrimination timeline accelerates
- **If r is detected at any level by BICEP Array or SO,** it immediately narrows the playing field

---
