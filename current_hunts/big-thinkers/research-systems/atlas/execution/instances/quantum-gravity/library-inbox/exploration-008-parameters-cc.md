# Exploration 008: Cosmological Constant, Matter Content, and Parameter Determination

## Goal
Investigate three interconnected questions for quadratic gravity + fakeon:
1. Can the 2 free parameters (M₂ fakeon mass, M₀ scalar mass) be determined by additional constraints?
2. Does the theory address the cosmological constant problem?
3. What matter content is required for UV completeness (f₀ UV fixed point)?

## Context from Prior Explorations
- Exp 002: d_s = 4→2 uniquely selects quadratic gravity + fakeon; 2 free params M₂, M₀
- Exp 003: Theory passes 7/7 validation tests; r ∈ [0.0004, 0.0035] is key prediction
- Exp 004: QG+F is the perturbative face of asymptotic safety; f₀ needs UV fixed point
- Exp 006: BH entropy is exactly A/(4G) for Schwarzschild
- Exp 007: Only testable prediction is r; n_s already in mild tension with ACT DR6

---

## Q1: Can the Free Parameters Be Fixed?

The quadratic gravity action is:

S = ∫ d⁴x √(-g) [ M_P² R/2 + R²/(6f₀²) - C_μνρσ C^μνρσ/(2f₂²) - Λ ]

This propagates three modes: the massless graviton, a massive scalar (mass M₀ = f₀ M_P/√2, the inflaton/scalaron), and a massive spin-2 particle (mass M₂ = f₂ M_P, the fakeon). The question is whether M₀ and M₂ can be determined.

### 1.1 M₀ Is Fixed by CMB Normalization — It Is NOT Free

**This is the most important finding of Q1: M₀ is already determined.**

The R² term drives Starobinsky inflation. In the Einstein frame, the scalaron potential is:

V(φ) = (3 M₀² M_P²/4)(1 - e^{-√(2/3) φ/M_P})²

The CMB power spectrum amplitude A_s ≈ 2.1 × 10⁻⁹ (measured by Planck) directly fixes:

**M₀ ≈ 3 × 10¹³ GeV ≈ 1.3 × 10⁻⁵ M_P**

This is a hard observational constraint, not a free parameter. The measurement uncertainty on A_s is ~1%, so M₀ is determined to within a few percent. This leaves only **one genuinely free parameter: M₂** (the fakeon mass).

The inflationary predictions are then:
- n_s ≈ 1 - 2/N_★ ≈ 0.967 (for N_★ ≈ 60 e-folds)
- r ≈ 12/N_★² ≈ 0.0033

**Status of the n_s tension (late 2025):** The ACT DR6 combined with Planck gives n_s = 0.974 ± 0.003, which is ~2.3σ above the basic Starobinsky prediction of 0.967. However, refined calculations (arXiv:2504.20757) show:
- Including higher-order corrections: n_s ≈ 0.967-0.972 for N_★ = 58-69
- The refined approximation n_s ≈ 1 - 2/(N_★ - (3/4)ln(2/N_★)) shifts the prediction upward
- For N_★ = 60, the model remains within the 2σ allowed region
- The apparent 3.9σ tension (claimed elsewhere using DESI BAO data) was based on overly simplified approximations

**Verdict on M₀: DETERMINED by observation. Not free.**

### 1.2 Constraints on M₂ from the Fakeon Mass Bound

Anselmi, Bianchi & Piva (JHEP 07(2020)211) computed the full inflationary predictions including the Weyl-squared term (which introduces the fakeon). The key results:

**Lower bound:** m_χ > m_φ/4 (i.e., M₂ > M₀/4 ≈ 7.5 × 10¹² GeV)

This bound comes from requiring the perturbation theory to be consistent — specifically, that the fakeon effects on the tensor and scalar power spectra remain under control. Below this bound, the Weyl-squared corrections would dominate and invalidate the perturbative expansion.

**Effect on r:** The tensor-to-scalar ratio depends on M₂/M₀:
- For M₂ → ∞ (pure Starobinsky limit): r ≈ 12/N_★² ≈ 0.0033
- For M₂ → M₀/4 (lower bound): r decreases to ~0.0004
- Full range: **0.0004 ≲ r ≲ 0.0035** (equivalently, 0.4 ≲ 1000r ≲ 3.5)

So r is a monotonic function of M₂/M₀. If r is measured by LiteBIRD or CMB-S4, this **directly determines M₂**.

**Verdict on M₂: constrained to M₂ > M₀/4 ≈ 7.5 × 10¹² GeV; will be fully determined once r is measured.**

### 1.3 The Unique Asymptotically Free Trajectory (Physical Beta Functions)

Buccio, Cacciapaglia, Lucini & Salvio (PRL 133, 021604, 2024; arXiv:2403.02397) made a breakthrough by computing the **physical** running of couplings in quadratic gravity — i.e., the momentum dependence of scattering amplitudes, not the renormalization-scale dependence (which differs due to tadpole contributions).

The physical beta functions are:

βλ = -(1/(4π)²) × (1617λ - 20ξ)λ/90

βξ = -(1/(4π)²) × (ξ² - 36λξ - 2520λ²)/36

where λ and ξ are the rescaled Weyl-squared and R² couplings respectively.

**Key finding:** There exists a **unique trajectory** (the separatrix s₂) that is:
1. Asymptotically free
2. Entirely in the tachyon-free region (λ > 0, ξ < 0)

This trajectory satisfies:

**ξ/λ = (569 - √386761)/15 ≈ -3.53**

This is remarkable: **the requirement of tachyon-free asymptotic freedom fixes the ratio ξ/λ**, and therefore the ratio of the coupling constants f₀/f₂. This in turn constrains M₀/M₂.

However, translating this precisely into a constraint on M₀/M₂ requires careful matching between the UV asymptotic ratio and the IR physical masses (the running changes the ratio between the UV and IR). The exact mapping depends on the full RG trajectory.

**Verdict: The physical beta functions provide a unique trajectory that constrains f₀/f₂, potentially fixing M₂ once M₀ is known. This is a strong theoretical constraint but the precise numerical value of M₂ requires solving the full RG flow.**

### 1.4 The Hierarchy Problem and Agravity

Salvio & Strumia's "agravity" scenario (JHEP 1406, 080, 2014) and "softened gravity" (PRD 94, 096007, 2016) propose a different approach to fixing the mass scale:

**The hierarchy problem argument:** If gravity "softens" (i.e., becomes weakly-coupled quadratic gravity) at energy scale M₂, then quantum gravitational corrections to the Higgs mass are proportional to M₂² rather than M_P². For the hierarchy problem to be solved without fine-tuning:

**M₂ ≲ 10¹¹ GeV**

This would mean the fakeon mass is ~10¹¹ GeV rather than ~10¹³ GeV.

**Tension with our framework:** This creates a problem:
- CMB normalization fixes M₀ ≈ 3 × 10¹³ GeV
- The hierarchy problem suggests M₂ ≲ 10¹¹ GeV
- But the Anselmi bound requires M₂ > M₀/4 ≈ 7.5 × 10¹² GeV

These three requirements are **mutually inconsistent**. If M₂ ≲ 10¹¹ GeV, then M₂ < M₀/4, violating the perturbative bound.

**Resolution:** The agravity scenario assumes a different parametric regime where the Planck mass is generated dynamically (there is no M_P in the fundamental action). In this case, the masses M₀ and M₂ are not simply related to f₀ M_P and f₂ M_P. The Coleman-Weinberg mechanism generates all scales. In our constraint-driven approach (where we take the spectral dimension as fundamental), the hierarchy problem remains unsolved in the standard sense.

**Verdict: The agravity hierarchy solution is incompatible with the CMB-derived value of M₀ in the standard parameterization. The hierarchy problem is NOT solved by the minimal theory.**

### 1.5 Spectral Dimension Profile Matching

The spectral dimension flow d_s(σ) in quadratic gravity is:

d_s(σ) = -2 d ln P(σ)/d ln σ

where P(σ) is the return probability of a random walk at diffusion time σ. For the quadratic gravity propagator G(p) ~ 1/(p² + m₀²) + corrections from the 1/p⁴ UV behavior:

- At σ → ∞ (IR): d_s → 4 (standard 4D)
- At σ → 0 (UV): d_s → 2 (due to the 1/p⁴ propagator)
- The crossover occurs at σ ~ 1/M₀² (or 1/M₂², whichever is smaller)

CDT simulations show the crossover happening at a scale ~E_P/25 (roughly 5 × 10¹⁷ GeV), which would correspond to a mass ~5 × 10¹⁷ GeV. This is much higher than M₀ ≈ 3 × 10¹³ GeV, but the CDT result has large uncertainties and the comparison is not straightforward (CDT uses Euclidean signature, different regularization, etc.).

LQG calculations show d_s running from 2 to 4 with a crossover related to the area gap, giving a different profile shape.

**Verdict: The spectral dimension profile is qualitatively consistent (d_s = 4→2) but does not currently constrain M₀ or M₂ beyond what inflation already provides. The crossover scale is sensitive to the specific definition of spectral dimension and the regularization scheme.**

### 1.6 Summary of Parameter Status

| Parameter | Status | Value | Determined By |
|-----------|--------|-------|---------------|
| M₀ (scalar/inflaton) | **FIXED** | 3 × 10¹³ GeV | CMB amplitude A_s |
| M₂ (fakeon) | **Bounded** | > 7.5 × 10¹² GeV | Perturbative consistency |
| M₂ (fakeon) | **Constrained** | Related to M₀ via ξ/λ ≈ -3.53 | Unique AF trajectory |
| M₂ (fakeon) | **Will be determined** | From r measurement | LiteBIRD/CMB-S4 (~2031-35) |

**The theory has effectively 1 free parameter (M₂), not 2, and this will be measured within a decade.**

---

## Q2: The Cosmological Constant Problem

### 2.1 Unimodular Quadratic Gravity (Salvio 2024)

Salvio (arXiv:2406.12958, Phys. Lett. B 856, 138920, 2024) showed that the unimodular version of quadratic gravity addresses the **"old" cosmological constant problem**:

**The Old CC Problem:** Why isn't the cosmological constant at least as large as the largest particle mass scale (~M_P⁴ or ~M_GUT⁴)? Quantum corrections from all known particles contribute ~(100 GeV)⁴ to vacuum energy, while the observed value is ~(10⁻³ eV)⁴ — a discrepancy of ~120 orders of magnitude.

**Unimodular Mechanism:** In unimodular gravity, the metric determinant √(-g) is fixed (non-dynamical). This has a profound consequence:
1. The spacetime volume is not a dynamical degree of freedom
2. The cosmological constant becomes an **integration constant** of the equations of motion rather than a coefficient in the action
3. **Vacuum energy does not gravitate** — contributions from particle physics loops can be absorbed into the non-dynamical volume element without affecting the CC

The field equations of unimodular QG are the traceless part of Einstein's equations (plus quadratic corrections). The trace part, which would normally couple to vacuum energy, is absent by construction.

**Mathematical implementation:** The unimodular constraint in the quadratic gravity action S = ∫d⁴x√(-g)[R²/(6f₀²) - C²/(2f₂²) + M_P² R/2 - Λ₀] is implemented by restricting det(g) to be a c-number function. This makes the CC an integration constant Λ_{eff} that is independent of Λ₀ and of all vacuum energy contributions.

**The New CC Problem (unsolved):** Why does Λ_{eff} take the observed tiny value ~10⁻¹²² M_P⁴? Unimodularity converts this from a fine-tuning problem into a selection problem — the CC is a free integration constant, and we need an additional principle to explain its value.

**Salvio's proposal:** A "multiverse of eras" within a single Big Bang, where different cosmological eras have different effective CC values. The observed CC is explained anthropically — life requires sufficient cosmic time to develop, so observers exist at the latest epoch where ρ_Λ ~ ρ_matter. This avoids the usual landscape problem because unimodularity already eliminates the old CC problem.

**Observable prediction:** Unimodular QG **removes an isocurvature mode** that standard QG predicts during inflation. Specifically, the perturbation constraint Φ = 3Ψ (in conformal Newtonian gauge) eliminates a scalar degree of freedom. If future CMB observations detect an isocurvature power spectrum from inflation, this would **rule out** unimodular QG while supporting standard QG. Absence of this mode would favor unimodularity.

### 2.2 Running Vacuum Energy in Asymptotic Safety

In the asymptotic safety framework (which is the non-perturbative completion of quadratic gravity), the cosmological constant is one of the relevant parameters at the Reuter fixed point. Key findings:

**Fixed point value:** At the Reuter fixed point, the dimensionless cosmological constant λ* = Λ/(k²) takes a non-zero value (typically λ* ≈ 0.2-0.4 depending on the truncation). This means Λ runs as k² in the UV.

**Running law:** The most robust prediction is Λ(k) ~ k² for k → ∞ (UV), transitioning to a constant Λ(k) → Λ_obs for k → 0 (IR). The transition depends on the full RG trajectory.

**Lattice results (2025):** Dai et al. (PRD 111, 034514, 2025) used Euclidean dynamical triangulations (EDT) to study vacuum dynamics. Key findings:
- Deviations from de Sitter geometry are well-described by a cosmological constant that **runs quadratically with the Hubble rate**: Λ(H) ~ Λ₀ + αH²
- The running parameter α is fully determined by lattice simulations
- Predicted deviations from ΛCDM are at the **O(10⁻³) level** — potentially testable by future precision cosmological measurements
- The null energy condition is not violated

**Critical assessment:** Neither the FRG approach nor the lattice approach currently predicts the **value** of Λ_obs from first principles. They predict the running behavior (how Λ changes with scale), but the IR value remains a free parameter, just as in unimodular gravity.

### 2.3 Comparison with Causal Set "Everpresent Lambda"

The causal set theory (CST) approach to the CC problem is qualitatively different and historically remarkable:

**The Sorkin prediction (1987-1990):** Before the discovery of cosmic acceleration, Sorkin argued from causal set principles that:
- Spacetime is fundamentally discrete (a causal set)
- The number of causal set elements N in a spacetime volume V follows Poisson statistics: δN ~ √N
- By unimodular reasoning, the CC fluctuates with amplitude:

  δΛ ~ (ℓ_P/ℓ_cs)² / √V ~ H²

- At the current epoch, this gives Λ ~ H₀² ~ 10⁻¹²² M_P⁴

**This predicted the correct order of magnitude a decade before observation.** The key insight is that Λ fluctuates (changing sign roughly every Hubble time) with amplitude naturally of order H², which happens to be the observed value.

**Comparison with quadratic gravity approaches:**

| Feature | Unimodular QG | AS Running | CST Everpresent Λ |
|---------|--------------|------------|-------------------|
| Solves old CC problem? | ✓ | Partially | ✓ |
| Predicts Λ_obs? | ✗ (free constant) | ✗ (free IR value) | ✓ (order of magnitude) |
| Λ fluctuates? | No | No | Yes (δΛ ~ H²) |
| Mechanism | Integration constant | RG flow | Poisson statistics |
| Testable? | Isocurvature mode | O(10⁻³) deviations | Λ fluctuations |

**Can quadratic gravity reproduce the CST prediction?**

In principle, combining unimodular QG with the observation that the CC is an integration constant, one could argue that the most natural value for an undetermined integration constant is set by the only available scale — which in cosmology is H². But this is a hand-waving argument, not a derivation.

The CST prediction is genuinely more powerful here because it derives δΛ ~ H² from a concrete microscopic mechanism (Poisson statistics of spacetime atoms). Quadratic gravity has no analogous microscopic mechanism — it is a continuum QFT.

**Verdict on the CC problem:** Unimodular quadratic gravity solves the old CC problem cleanly but does not predict Λ_obs. The CST everpresent-Λ mechanism remains the only approach that correctly predicted the order of magnitude. This is a genuine limitation of the quadratic gravity + fakeon framework.

---

## Q3: Matter Content for UV Completion

### 3.1 Beta Functions for f₀ and f₂

The one-loop beta functions for the gravitational couplings in the presence of matter (N_S real scalars, N_F Weyl fermions, N_V gauge vectors) are (Salvio & Strumia, EPJC 78, 2018):

**f₂ (Weyl-squared coupling):**

(4π)² df₂²/d ln μ = -f₂⁴ × (133/10 + N_V/5 + N_F/20 + N_S/60)

**f₀ (R² / conformal mode coupling):**

(4π)² df₀²/d ln μ = (5/3)f₂⁴ + 5f₂²f₀² + (5/6)f₀⁴ + contributions from non-minimal scalar couplings

The crucial asymmetry:
- **f₂ is always asymptotically free** — the coefficient of f₂⁴ is always negative for any non-negative N_V, N_F, N_S. More matter makes it MORE asymptotically free.
- **f₀ has a positive beta function** — the (5/3)f₂⁴ + 5f₂²f₀² + (5/6)f₀⁴ terms are all positive. Neither vectors nor fermions contribute to f₀ at one loop. Only non-conformally-coupled scalars affect f₀, and they make it worse (more positive).

This means: **f₀ grows with energy and hits a Landau pole, regardless of matter content** (at one loop).

### 3.2 Standard Model Matter Content

The Standard Model contains:
- **N_S = 4** real scalar degrees of freedom (the Higgs doublet: 2 complex = 4 real)
- **N_F = 45** Weyl fermions (3 generations × (3 colors × 2 quarks + 1 charged lepton + 1 neutrino) × 2 chiralities - but counting only left-handed: 3 × [3×2 + 1×2 + 1] = 3×8 = ... actually N_F = 45 Weyl spinors for the full SM)
- **N_V = 12** gauge vectors (8 gluons + W⁺ + W⁻ + Z + γ)

Plugging into the f₂ beta function:

(4π)² df₂²/d ln μ = -f₂⁴ × (133/10 + 12/5 + 45/20 + 4/60)
                    = -f₂⁴ × (13.3 + 2.4 + 2.25 + 0.067)
                    = -f₂⁴ × 18.02

So f₂ is strongly asymptotically free with SM matter (coefficient = -18.02/(4π)²).

For f₀, the SM Higgs is non-minimally coupled to gravity (the ξ_H |H|² R term), and this coupling runs. At one loop, the SM does NOT make f₀ asymptotically free — it remains problematic.

### 3.3 The f₀ Problem and Its Resolution

The f₀ Landau pole is the central obstacle to UV completion. There are several proposed resolutions:

**Resolution 1: Asymptotic Safety (Non-Perturbative Fixed Point)**

As shown in Exp 004, the non-perturbative FRG analysis reveals a Reuter fixed point where all gravitational couplings (including the f₀ analog) reach finite non-zero values. In this picture:
- f₂ → 0 (asymptotic freedom) at the perturbative fixed point
- f₀ → f₀* (non-zero fixed point value) at the Reuter fixed point
- These are two different fixed points in the same theory space (Sen, Wetterich & Yamada, JHEP 2022)

The perturbative Landau pole of f₀ is an artifact of perturbation theory — non-perturbatively, the coupling approaches a finite fixed point rather than diverging. This is analogous to the g₁ (U(1)_Y) Landau pole in the SM, which is expected to be resolved by non-perturbative UV completion.

**Resolution 2: Conformal Coupling Fixed Point**

Salvio & Strumia (2018) showed that when f₀ grows large, the conformal mode of the graviton decouples. If all scalars become **asymptotically conformally coupled** (ξ_ab → 1/6 in the UV), then:
- The problematic scalar contributions to f₀ vanish
- f₀ effectively decouples from the physical spectrum
- The theory flows to conformal gravity in the UV

This requires that all scalar non-minimal couplings ξ run to 1/6. For the SM Higgs, this means ξ_H → 1/6 in the UV. The RG flow of ξ_H depends on the top Yukawa, gauge couplings, and the Higgs quartic — and numerical studies suggest this is plausible but not guaranteed.

**Resolution 3: Total Asymptotic Freedom with BSM Matter**

A third option is to add enough matter to make the **entire** theory (gravity + matter) totally asymptotically free (TAF). This requires:
- All gauge couplings asymptotically free (restricts gauge group)
- All Yukawa couplings go to zero (restricts fermion content)
- All scalar quartic couplings go to zero (restricts scalar sector)
- All non-minimal couplings ξ → 1/6 (conformal coupling)

The SM fails TAF because:
- g₁ (U(1)_Y hypercharge) is NOT asymptotically free
- The top Yukawa is too large
- The Higgs quartic may not go to zero

**Trinification solution:** Pelaggi, Strumia & Vignali (JHEP 08(2015)130) showed that extending the SM gauge group to SU(3)_L ⊗ SU(3)_R ⊗ SU(3)_c (trinification) achieves TAF:
- All gauge couplings become asymptotically free (U(1)_Y is embedded in non-abelian groups)
- Three generations of chiral fermions and Higgses are needed
- Some extra fermions are required
- All couplings can be extrapolated to infinite energy

This predicts **new particles at the TeV scale** — testable at the LHC or future colliders.

**Resolution 4: Physical Beta Functions (Buccio et al. 2024)**

The 2024 breakthrough by Buccio et al. showed that using physical (momentum-dependent) beta functions rather than μ-running ones, the tachyon-free condition is compatible with asymptotic freedom along a unique trajectory. This doesn't eliminate the f₀ problem per se, but shows that the physical running is better behaved than the naive RGE would suggest.

### 3.4 What Matter Content Is Actually Required?

The answer depends on which resolution one adopts:

| Resolution | Additional Matter | Testable? |
|-----------|------------------|-----------|
| Asymptotic safety (FP) | None required | No (non-perturbative) |
| Conformal coupling | None (SM may suffice) | Indirectly (ξ_H value) |
| TAF (trinification) | SU(3)³ gauge + extra fermions | Yes (TeV-scale BSM) |
| Gauge-assisted QG | Hidden SU(N) sector | Possibly (dark sector) |

The most conservative resolution is asymptotic safety — the same non-perturbative fixed point that we already established (Exp 004) as the UV completion of the theory. In this case, **no additional matter beyond the Standard Model is strictly required** for UV completion of the gravitational sector.

However, if one demands Total Asymptotic Freedom (all couplings → 0 in the UV), then BSM physics is mandatory, with trinification (SU(3)³) being the simplest viable option.

---

## Synthesis and Conclusions

### The Parameter Count

The theory started with 2 apparently free parameters. We now find:
1. **M₀ is FIXED** at 3 × 10¹³ GeV by CMB normalization — this was never truly free
2. **M₂ is BOUNDED** from below (M₂ > M₀/4 ≈ 7.5 × 10¹² GeV) by perturbative consistency
3. **M₂ is CONSTRAINED** by the unique asymptotically free trajectory (ξ/λ ≈ -3.53)
4. **M₂ WILL BE DETERMINED** by measuring r (tensor-to-scalar ratio) with LiteBIRD/CMB-S4

**The theory has effectively 1 free parameter that will be measured within a decade.** This makes it one of the most predictive quantum gravity frameworks.

### The Cosmological Constant

Quadratic gravity + fakeon addresses the CC problem only partially:
- The **old problem** is solved by the unimodular extension (Salvio 2024) — vacuum energy doesn't gravitate
- The **new problem** (why Λ_obs ≈ 10⁻¹²² M_P⁴) remains unsolved
- The theory cannot match the causal set prediction (δΛ ~ H²) because it lacks a microscopic discreteness mechanism
- The running vacuum energy from AS gives O(10⁻³) deviations from ΛCDM but doesn't predict Λ_obs

This is a genuine gap compared to causal set theory, which uniquely predicted the right order of magnitude.

### Matter Content

For UV completion of the gravitational sector:
- **Minimum requirement:** The asymptotic safety fixed point (already established) provides non-perturbative completion — no BSM matter needed for gravity alone
- **For TAF:** SU(3)³ trinification with extra fermions — predicts TeV-scale new physics
- **The f₀ Landau pole** is not a fundamental obstacle but rather an artifact of perturbation theory, resolved non-perturbatively by the Reuter fixed point

### Concrete Numerical Results

1. **M₀ = 3.0 × 10¹³ GeV** (from A_s = 2.1 × 10⁻⁹)
2. **M₂ > 7.5 × 10¹² GeV** (from m_χ > m_φ/4)
3. **f₂ beta function coefficient with SM: -18.02/(4π)²** (strongly asymptotically free)
4. **Unique AF trajectory ratio: ξ/λ ≈ -3.53** (fixes f₀/f₂ relation)
5. **r ∈ [0.0004, 0.0035]** (maps one-to-one to M₂)
6. **Unimodular QG removes one isocurvature mode** (testable)
7. **Lattice QG predicts O(10⁻³) deviations from ΛCDM** (future test)

### Key Insight

The narrative has shifted: **quadratic gravity + fakeon is not a 2-parameter theory — it is effectively a 1-parameter theory that will be fully determined by CMB B-mode measurements.** Combined with the spectral dimension derivation (Exp 002), the AS connection (Exp 004), and the 7/7 validation (Exp 003/006), this makes it arguably the most constrained and testable quantum gravity framework available.

The remaining weakness is the cosmological constant problem, where the theory's continuum nature prevents it from achieving the kind of microscopic prediction that causal set theory provides.
