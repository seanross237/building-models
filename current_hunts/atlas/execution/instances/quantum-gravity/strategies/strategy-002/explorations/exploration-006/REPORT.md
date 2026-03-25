# Exploration 006: The Cosmological Constant Problem in QG+F — Can Causal Set Discreteness Help?

## 1. Executive Summary

The everpresent-Λ mechanism (Sorkin 1987, Ahmed et al. 2004) is the most impressive prediction in quantum gravity — it predicted Λ ~ H₀² ~ 10⁻¹²² M_P⁴ roughly a decade before the 1998 supernova observations confirmed cosmic acceleration. The mechanism combines two ingredients: (1) the Λ-V conjugacy from unimodular gravity (δΛ · δV ~ ℏ), and (2) Poisson fluctuations from causal set discreteness (δV ~ √V). Together these give δΛ ~ 1/√V ~ H².

**However, everpresent-Λ cannot be imported into QG+F.** The Poisson fluctuation ingredient requires discrete spacetime atoms — a concept foreign to continuum QFT. No known continuum mechanism reproduces the crucial δV ~ √V scaling. Additionally, the everpresent-Λ model has serious observational difficulties: it cannot simultaneously fit CMB and SN Ia data (only 0.017% of random realizations fit SN Ia alone), and its characteristic large fluctuations conflict with CMB precision constraints.

**Unimodular QG+F (Salvio 2024) provides half the solution.** It makes Λ a radiatively stable integration constant, solving the "old" CC problem (why Λ isn't ~ M_P⁴). Vacuum energy truly doesn't gravitate in this formulation. But the "new" CC problem (why Λ ~ 10⁻¹²²) remains unsolved.

**No approach within QG+F predicts the observed CC value.** Asymptotic safety doesn't help (Λ_IR is a free parameter on the RG trajectory). Vacuum energy sequestering (Kaloper-Padilla) is potentially compatible but untested. The six-derivative extension's scalars are too heavy for late-time effects. Pre-geometric topological quantization (Addazi & Meluccio 2025) is a novel idea but requires physics far beyond QG+F.

**Recommendation:** Adopt unimodular QG+F as the default formulation (it costs nothing and solves the old CC problem). Accept Λ as an input parameter for now. The most promising untested direction is the compatibility of Kaloper-Padilla vacuum energy sequestering with QG+F. The CC problem remains the Achilles heel of ALL continuum QFT approaches to quantum gravity, not just QG+F.

## 2. The Everpresent-Λ Mechanism: Deep Dive

### 2.1 Origins and Core Idea

The everpresent-Λ mechanism originates from Rafael Sorkin's 1987 talk (later formalized with Ahmed, Dodelson, and Greene in Phys. Rev. D 69, 103523, 2004). It combines two independent ideas:

1. **Unimodular gravity** — In this formulation of GR, the cosmological constant Λ is not a parameter in the action but an integration constant. Crucially, the spacetime 4-volume V and Λ become conjugate variables, yielding an uncertainty relation:

   δΛ/(8πG) · δV ≥ ℏ/2

2. **Causal set discreteness** — Spacetime is fundamentally a discrete partial order (causal set). Points are "sprinkled" into spacetime via a Poisson process at density ρ_cs ~ 1/ℓ_P⁴. The number of elements N in a region of volume V follows a Poisson distribution: ⟨N⟩ = ρ_cs · V, with fluctuations δN ~ √N.

The key insight: the Poisson statistics of causal set elements translate into fluctuations of the spacetime 4-volume:

   δV = √N / ρ_cs ~ √V (in Planck units)

### 2.2 Mathematical Reconstruction

**Step 1: The conjugacy.** From the path integral of unimodular gravity, constraining the total spacetime volume and Fourier transforming to the conjugate variable gives the uncertainty relation δΛ · δV ~ ℏ (in natural units with 8πG = 1).

**Step 2: The Poisson fluctuations.** For a causal set faithfully embedding in a region of volume V, we have N ~ ρ_P · V elements, where ρ_P ~ ℓ_P⁻⁴. The Poisson fluctuation gives δN ~ √N, hence δV ~ √(V/ρ_P) ~ √V in Planck units.

**Step 3: Combining.** Substituting δV ~ √V into the uncertainty relation:

   δΛ ~ 1/√V

For an FLRW universe, the 4-volume of the causal past of an observer at time t scales as V ~ H⁻⁴ (where H is the Hubble parameter), giving:

   **δΛ ~ H² ~ 10⁻¹²² M_P⁴ (today)**

This is the observed value, and the prediction was made ~decade before the 1998 supernova observations.

**Step 4: Stochastic evolution.** The phenomenological Model 1 (Ahmed et al. 2004) treats each new causal set element as contributing ±(8πα)/ℓ²_cs with probability 1/2, where α = (ℓ_P/ℓ_cs)²/2. The recursive evolution:

   Λ(x_n) = [Λ(x_{n-1})V(x_{n-1}) + 8πα√(ΔV_n)·ξ_n] / V(x_n)

where ξ_n are independent standard normal variables. This ensures δΛ ∝ 1/√V is maintained throughout cosmic evolution, with Λ fluctuating in both magnitude and sign approximately every Hubble time.

### 2.3 The Prediction: Λ ~ H₀²

The prediction's power lies in its naturalness:
- **No fine-tuning**: Λ is always of order the ambient energy density, by construction
- **The coincidence problem is dissolved**: Why is Λ ~ ρ_matter today? Because Λ is always ~ ρ_dominant at every epoch
- **The "old" CC problem is avoided**: Vacuum energy doesn't gravitate in unimodular gravity (or more precisely, its contribution is absorbed into the integration constant)

However, the prediction is statistical — it gives the standard deviation of Λ, not its exact value. The observed Λ is one realization of a stochastic process.

### 2.4 Latest Observational Tests (2023-2025)

Two key papers test everpresent-Λ against modern data:

**Zwane, Afshordi, Sorkin (2018, CQG 35, 194002):** First systematic confrontation with SN Ia and CMB data. Found that everpresent-Λ can fit data comparably to ΛCDM for some realizations, and further removes H₀ tension and BAO Lyman-α tension at z ~ 2-3.

**"Aspects of Everpresent Λ (II): Cosmological Tests of Current Models" (arXiv:2307.13743, revised Oct 2024):** Most comprehensive test to date, using:
- Pantheon+SH0ES sample: 1550 SN Ia events + 42 calibrators
- Planck CMB likelihood
- 90,000 random seeds tested

**Results:**
- **SN Ia**: Only 0.017% of seeds (16 out of 90,000) produce fits better than ΛCDM (best χ² = 1481.9 vs ΛCDM's 1485.3). Best-fit H₀ = 72.18 km/s/Mpc with Ω_m = 0.33.
- **CMB**: The model **struggles significantly**. Even with modifications suppressing Λ fluctuations near recombination, CMB χ² remains much larger than ΛCDM.
- **H₀ tension**: Bayesian-averaged H₀ = 73.27 ± 1.27 km/s/Mpc, aligning with SH0ES (73.04 ± 1.04). But this comes from selecting good seeds, not from a fundamental resolution.
- **Key limitation**: The large fluctuations (~dominant energy density) characteristic of everpresent-Λ conflict with tight CMB constraints, particularly the ISW effect.

**Bottom line:** The model can fit SN Ia data for rare seeds but **cannot simultaneously satisfy both CMB and SN Ia constraints** in its current formulation. The α parameter (fluctuation magnitude) that works for SN Ia (~0.009) implies fluctuations far too large for CMB consistency.

### 2.5 Criticisms and Weaknesses

1. **Zero-mean assumption**: The assumption ⟨Λ⟩ = 0 is put in by hand — "this assumption does not stem from any fundamental aspect of causal set theory" (from the paper itself)
2. **Element-wise ansatz**: The independent contribution of each causal set element is phenomenological; the true quantum dynamics are unknown
3. **Non-conservation**: A varying Λ violates the Bianchi identity (∇_μ G^μν = 0), requiring energy non-conservation or backreaction — addressed only phenomenologically by using the Friedmann equation alone
4. **H² < 0 problem**: Some realizations produce H² < 0 (contracting universes), and "the correct dynamics for H² < 0 situations is not known," forcing researchers to discard such realizations
5. **CMB incompatibility**: The characteristic large fluctuations are in serious tension with CMB precision data
6. **No microscopic derivation**: The stochastic models are phenomenological ansätze, not derived from a fundamental causal set dynamics (which doesn't yet exist)
7. **Selection bias**: The need to search ~90,000 seeds to find ~16 that fit SN Ia data is problematic — it amounts to a form of fine-tuning (selecting the right realization)

## 3. Can Everpresent-Λ Work in Continuum QG+F?

### 3.1 The Discreteness Requirement

The everpresent-Λ mechanism has two essential ingredients:

1. **Unimodular gravity** (the Λ-V conjugacy): This is purely a property of how the theory is formulated — it works in the continuum. No discreteness needed for this piece.

2. **Poisson fluctuations of spacetime volume** (δV ~ √V): This is where causal set discreteness enters. The fluctuation δN ~ √N comes from Poisson statistics of discrete sprinkling. In a smooth continuum spacetime, the 4-volume of a region is a definite number, not a fluctuating quantity.

**The critical question:** Can a continuum theory reproduce δV ~ √V? There are several logical possibilities:

- **Path-integral measure fluctuations**: In the gravitational path integral, the volume is an integrated quantity over all metrics. However, the dominant saddle-point contribution gives a definite volume; fluctuations around the saddle are suppressed by e^{-S}, not enhanced by √V. The path integral naturally produces quantum fluctuations, but these scale differently from Poisson fluctuations.

- **Spacetime foam**: At Planck scale, quantum fluctuations of the metric might produce effective "graininess" that mimics discreteness. However, the amplitude of these fluctuations is model-dependent and there is no generic argument that they produce Poisson-type statistics.

- **Effective discreteness from dimensional reduction**: In asymptotic safety, the spectral dimension flows from 4 to 2 at the Planck scale. This suggests the effective number of degrees of freedom is reduced, but this is a property of the propagator, not of spacetime points. It does not directly produce Poisson volume fluctuations.

**Assessment:** There is no known mechanism in continuum quantum gravity that reproduces the specific δV ~ √V scaling that comes from counting discrete spacetime atoms. This is the fundamental obstacle to importing everpresent-Λ into QG+F.

### 3.2 Unimodular QG+F (Salvio 2024)

Salvio (Phys. Lett. B 858, 138920, 2024; arXiv:2406.12958) showed that the unimodular constraint can be imposed on quadratic gravity (QG+F):

**How it works:**
- Insert a delta function ∏_x δ(√g(x) - fixed) into the path integral
- Equivalently, introduce a Lagrange multiplier field l(x)
- The cosmological constant becomes an integration constant of the field equations
- The constraint is coordinate-independent and preserves general covariance

**What it solves:**
- **Old CC problem**: YES. Vacuum energy from matter loops no longer gravitates. The CC is decoupled from the particle physics mass scales. Quantum corrections to vacuum energy are converted into a total derivative and do not affect the CC.
- **New CC problem (why Λ ~ 10⁻¹²²)**: NO. The CC is an integration constant, but its value is undetermined. Salvio proposes anthropic selection in a "multiverse of eras" within a single big bang.

**Key observational difference from standard QG+F:**
- An extra isocurvature mode B that is present in ordinary QG+F **decouples** in unimodular QG+F
- This could be testable with future CMB observations
- The inflationary predictions for n_s and r are unchanged

**Compatibility with fakeon:**
- The paper builds on the "renormalizable and unitary" quadratic gravity framework — i.e., the fakeon prescription is implicitly assumed
- The unimodular constraint does not interfere with the fakeon prescription for the massive spin-2 mode

**Bottom line:** Unimodular QG+F is a well-defined theory that solves the old CC problem. It provides half of the everpresent-Λ mechanism (the Λ-V conjugacy) but not the Poisson fluctuation half.

### 3.3 Asymptotic Safety and Effective Discreteness

The QG+F ↔ AS duality (explored in prior explorations) suggests a non-perturbative sector. Could this provide effective discreteness?

**What AS says about the UV:**
- The spectral dimension flows d_s: 4 → 2 at the Planck scale (well-established in AS literature: Lauscher & Reuter 2005, Reuter & Saueressig 2012)
- Spacetime acquires a fractal structure with Hausdorff dimension d_H = 2 at trans-Planckian scales
- This "effective dimensionality reduction" is reminiscent of discreteness but is NOT the same thing

**Why AS does NOT give Poisson fluctuations:**
- AS is a continuum framework by definition — it uses the functional renormalization group on a smooth manifold
- The d_s = 2 fractal structure describes how propagators and diffusion processes behave, not a discrete counting of spacetime atoms
- There is no "N" (number of elements) in AS; the volume of a region is still a continuous variable
- Even on a lattice (used as a regularization), the physical results are obtained in the continuum limit, where lattice artifacts vanish

**What about AS predictions for Λ?**
- The Reuter fixed point has a dimensionless cosmological constant λ* ≈ 0.19 (typical value from truncations)
- The dimensionless product G·Λ is fixed at the UV: (G·Λ)* ≈ 0.12
- But the IR value of Λ is NOT predicted — it depends on which RG trajectory flows out of the fixed point
- The trajectory selection is an initial condition, not determined by the theory
- Some AS approaches explore an IR fixed point at Λ → 0, but this is speculative and unproven

**Assessment:** AS does not provide the discrete degrees of freedom needed for the everpresent-Λ mechanism. The non-perturbative sector introduces rich UV structure but does not produce Poisson-type volume fluctuations.

### 3.4 Continuum Analogues of Poisson Fluctuations

Could there be a continuum mechanism that mimics the δV ~ √V scaling without actual discreteness? Let me examine this conceptually:

**Option A: Gravitational path-integral fluctuations**
In the Euclidean path integral Z = ∫ Dg e^{-S[g]}, the volume V = ∫ √g d⁴x is a functional of the metric. Its expectation value ⟨V⟩ and variance ⟨(δV)²⟩ are computable in principle. However:
- For a saddle-point (semiclassical) approximation: δV/V ~ ℓ_P²/L² where L is the characteristic scale, giving δV ~ V·(ℓ_P/L)² ≪ √V for macroscopic V
- Perturbative quantum corrections are too small by many orders of magnitude
- Only a strongly-coupled non-perturbative sector could produce δV ~ √V, and there's no evidence for this

**Option B: Stochastic quantization / stochastic inflation**
In stochastic inflation (Starobinsky 1986), the long-wavelength modes of a scalar field undergo a random walk, with the stochastic noise from short-wavelength quantum fluctuations crossing the Hubble horizon. Could a similar mechanism produce Λ fluctuations?
- The stochastic noise for a light scalar field gives δφ ~ H/(2π) per e-fold
- If Λ were a dynamical scalar field (quintessence), its fluctuations would scale as δΛ ~ H²/M² (where M is the field mass), which CAN give δΛ ~ H² for M ~ M_P
- But this is quintessence, not the cosmological constant — it introduces a new degree of freedom and a fine-tuned potential

**Option C: Topological fluctuations / spacetime foam**
Spacetime foam (Wheeler 1955) suggests Planck-scale topology changes. If topology changes contribute ±1 in Planck units to the effective volume, and there are N ~ V/ℓ_P⁴ independent such fluctuations, then δV ~ √N · ℓ_P⁴ ~ √V in Planck units — exactly the Poisson scaling! However:
- There is no controlled calculation of spacetime foam in any approach
- In QG+F, the theory is perturbative and there are no topology changes in the path integral
- The AS non-perturbative sector might in principle host topology changes, but this is pure speculation

**Assessment:** The only known mechanism that robustly produces δV ~ √V is discrete Poisson sprinkling. Continuum analogues either give much smaller fluctuations (perturbative QG) or require uncontrolled non-perturbative effects (spacetime foam). This is a fundamental conceptual gap.

### 3.5 Assessment: Compatibility with QG+F

**Summary of findings:**

| Ingredient | Available in QG+F? | Status |
|---|---|---|
| Unimodular gravity (Λ-V conjugacy) | YES (Salvio 2024) | Well-established |
| Poisson volume fluctuations (δV ~ √V) | NO | Fundamental obstacle |
| Stochastic Λ evolution | Possible via quintessence | But changes the framework |
| Old CC problem solution | YES (unimodular) | Solved |
| New CC problem solution | NO | Not addressed |

**Verdict: The everpresent-Λ mechanism CANNOT be directly imported into QG+F.** The mechanism's core prediction (δΛ ~ H²) requires discrete spacetime atoms — a concept that is foreign to QG+F as a continuum QFT. Unimodular QG+F provides half the mechanism but not the crucial half.

**However**, the everpresent-Λ idea reveals a productive direction: if one could find a continuum mechanism that produces effective Poisson-type fluctuations of the 4-volume at the Planck scale, it would complete the picture. This is the key open question (see Section 6).

## 4. Alternative Approaches to Λ Within QG+F

### 4.1 Unimodular Gravity and the "Old" CC Problem

The "old" cosmological constant problem: why doesn't vacuum energy from quantum field theory (expected to be ~ M_P⁴ or at least ~ M_EW⁴ ~ 10⁻⁶⁷ M_P⁴) gravitate and curve spacetime enormously?

**Unimodular gravity's answer:**
- In unimodular gravity, the trace of the Einstein equations is removed. The cosmological constant is not a coupling in the action but an integration constant.
- Vacuum energy ρ_vac contributes a term proportional to g_μν in T_μν. In standard GR, this directly sources Λ_eff = Λ_bare + 8πG·ρ_vac. In unimodular gravity, the vacuum energy contribution is automatically absorbed into the integration constant — it does not gravitate.
- This has been verified at the quantum level: quantum corrections do not generate a gravitating cosmological constant in unimodular gravity. The one-loop effective action differs from standard gravity only in the treatment of the global conformal mode.

**Limitations and the Quantum Equivalence Debate:**
- This solves the OLD problem (why Λ isn't huge) but NOT the NEW problem (why Λ has the specific small value we observe)
- **Important caveat:** There is an active debate about whether unimodular gravity genuinely solves even the old CC problem at the full quantum level. Critics (notably Padilla et al. in the 2023 review arXiv:2301.01662) argue that: (a) classically, UG is just a gauge-fixed version of GR and yields identical dynamics; (b) at the quantum level, the CC problem is reformulated as a fine-tuning of initial conditions rather than eliminated; (c) statements about solving the CC problem are "wholly nugatory" and fail to appreciate that the problem is one of radiative instability within effective field theory
- **Defenders argue:** The unimodular path integral differs from GR's path integral in the treatment of the global conformal mode, which is physically meaningful; one-loop calculations explicitly show that vacuum energy doesn't gravitate
- **A recent novel approach:** Josset et al. (arXiv:2511.12897, Nov 2025) propose that nonlinear quantum mechanics in unimodular gravity can cause the "shadow" stress-energy (which acts as a CC) to redshift away over cosmic time, dynamically solving the old CC problem without fine-tuning initial conditions. This is speculative but represents a genuinely new direction.
- The all-orders status remains debated, but the one-loop result is robust

**In QG+F context:** Salvio (2024) demonstrated that unimodular quadratic gravity is consistent and well-defined. The fakeon prescription is compatible with the unimodular constraint. This gives QG+F a clean solution to the old CC problem with no additional assumptions beyond choosing the unimodular formulation.

### 4.2 Radiative Stability in QG+F

**The question:** Even if we set Λ to a small value at tree level, do quantum corrections from QG+F loops destabilize it?

**Standard QG+F (non-unimodular):**
- Quadratic gravity is renormalizable, so the CC receives finite (not divergent) quantum corrections at each loop order
- However, these corrections are generically ~ M₂⁴ (the fakeon mass) or ~ M₀⁴ (the scalar mass), both of which are ~ 10⁻⁸ M_P⁴ (for M₂ ~ 10⁻¹ M_P)
- This is still 10¹¹⁴ times larger than the observed Λ ~ 10⁻¹²² M_P⁴
- So the CC is NOT radiatively stable in standard QG+F — fine-tuning is required

**Unimodular QG+F:**
- In the unimodular formulation, the CC is an integration constant and does NOT receive radiative corrections
- This is the key advantage: radiative stability is automatic
- The CC can be set to any value (including the observed small value) without being destabilized by loops

**Technical naturalness:**
- In the 't Hooft sense, a parameter is technically natural if setting it to zero enhances the symmetry. For the CC in unimodular gravity, setting Λ = 0 does enhance a symmetry (volume-preserving diffeomorphisms become exact)
- However, the symmetry is restored continuously, not discretely — there's no special reason for Λ = 0 vs. Λ = 10⁻¹²²
- So Λ is radiatively stable at ANY value, but no specific small value is preferred

### 4.3 Vacuum Energy Sequestering (Kaloper-Padilla)

**The mechanism (Kaloper & Padilla, PRL 112, 091304, 2014; PRD 90, 084023, 2014):**

A reformulation of GR where the dimensional parameters in the matter sector are made into functionals of the 4-volume of the universe. The action includes global (non-local) variables:

   S = ∫ d⁴x √g [M_P²R/2 - Λ(σ)] + S_matter[g, σ·g_μν] + σ⁴·F(Λ/σ⁴)

where σ is a global scaling parameter and Λ is a global cosmological constant, both of which are dynamical but non-local (they are functionals of the entire spacetime).

**What it achieves:**
- ALL vacuum energy from the matter sector (classical + quantum, including phase transitions) is completely sequestered from gravity
- The residual CC in an old, large universe is automatically very small: Λ_eff ~ ⟨ρ_matter⟩_spacetime ~ small for large universes
- Makes specific predictions: w ≈ -1 (transient), the universe will eventually collapse

**Compatibility with QG+F:**
- The sequestering mechanism works at the level of the gravitational action + matter coupling
- In principle, it could be applied to the QG+F action: replace R with the full quadratic gravity Lagrangian and include the global variables
- However, the mechanism requires the 4-volume to be finite (so the global variables are well-defined), which may conflict with eternal inflation or de Sitter space
- The relationship between sequestering's global variables and the fakeon prescription has not been studied
- The mechanism is inherently non-local (it uses functionals of the entire spacetime), which may clash with QG+F's emphasis on locality and microcausality

**Assessment:** Promising in principle but untested in the QG+F context. The non-locality is a potential conceptual conflict. Worth investigating but not a natural fit.

### 4.4 Asymptotic Safety Predictions for Λ

**The status of AS predictions for Λ:**

At the Reuter fixed point (the UV non-Gaussian fixed point of pure gravity):
- The dimensionless CC is λ* ≈ 0.19 and Newton's constant is g* ≈ 0.71 (typical values from the Einstein-Hilbert truncation)
- The product (g·λ)* ≈ 0.13 is a UV-fixed quantity
- However, these are dimensionless quantities at the UV scale k → ∞

For the IR (observable) value:
- Λ_IR depends on which RG trajectory connects the UV fixed point to the IR
- This is a one-parameter family (for pure gravity, λ is the single relevant direction), so Λ_IR is a free parameter
- **AS does NOT predict the IR value of Λ**

**Novel ideas from recent AS research:**
- Some models explore an IR fixed point that could predict Λ → 0 in the deep IR, but this remains speculative
- The "AS swiss cheese model" (arXiv:2410.07818) tries to connect local AS effects around galaxies to cosmic acceleration, but the mechanism is unclear
- The beta functions diverge near k ~ H₀, making the connection to observations technically challenging

**In the QG+F context:**
- If the QG+F ↔ AS duality holds, then the UV fixed point constrains the relationship between couplings at the Planck scale
- But Λ remains a free parameter in the IR — the duality doesn't help predict it
- The RG running of Λ from the UV to IR is computable in principle, but the initial condition (where on the trajectory) is not determined

**Assessment:** AS provides no prediction for the observed CC value. The UV fixed point constrains UV physics but the IR value of Λ is a free parameter selected by initial conditions.

### 4.5 Other Mechanisms

**Pre-geometric gravity (Addazi & Meluccio, arXiv:2602.16840, Feb 2025):**
- Proposes that spacetime emerges from spontaneous symmetry breaking of a fundamental gauge symmetry
- The Gauss-Bonnet topological coupling acts as a gravitational θ-angle, quantizing Λ into discrete topological sectors
- SSB dynamics selects the sector matching observed Λ
- Very recent (Feb 2025), not yet peer-reviewed or scrutinized
- Would require major modification of QG+F to incorporate pre-geometric structure

**Spacetime foam / Wheeler-DeWitt fluctuations:**
- If Planck-scale topology fluctuations produce ±1 Planck-unit volume fluctuations, then δV ~ √V naturally
- But no controlled calculation exists in any framework
- QG+F is perturbative and does not include topology change

**Dynamical dark energy / quintessence:**
- Replace Λ with a slowly rolling scalar field
- QG+F's scalar mode (the R² scalar) is massive (m ~ 10¹³ GeV) and cannot serve as quintessence
- An additional light scalar could be added but would be ad hoc and introduce fine-tuning

## 5. The Deep Question: Why 10⁻¹²²?

### 5.1 The Anthropic Argument

The anthropic argument (Weinberg 1987, Bousso & Polchinski 2000):
- In a multiverse with many possible values of Λ, most values either prevent galaxy formation (Λ too large positive → expansion too fast) or produce recollapse (Λ too negative)
- The observed value |Λ| ≲ 10⁻¹²¹ M_P⁴ is roughly the largest value consistent with structure formation
- If the landscape of vacua is dense enough, some vacua will have Λ in this range
- Observers necessarily find themselves in such vacua → anthropic selection

**Status in QG+F context:**
- Salvio (2024) adopts this approach for unimodular QG+F, proposing a "multiverse of eras" within a single big bang
- This requires the CC to vary between eras, which is natural in unimodular gravity where Λ is an integration constant that can change at era boundaries
- The mechanism avoids the string landscape's 10^{500} vacua but requires a mechanism to generate different eras

**Criticism:**
- Anthropic selection is unfalsifiable in practice
- It explains Λ ~ 10⁻¹²² but not its exact value
- Many physicists consider it a "failure mode" rather than a solution
- It provides no testable prediction beyond "Λ should be in the anthropic window"

### 5.2 Non-Anthropic Approaches

**a) Causal set fluctuations (everpresent-Λ):**
- The only approach that PREDICTED the right order of magnitude before observation
- But as shown in Section 2, it has serious observational difficulties (CMB tension) and requires spacetime discreteness foreign to QG+F

**b) Radiative stability arguments:**
- In unimodular QG+F, Λ is technically natural at any value
- But this doesn't explain why it has THIS specific value — it just explains why it stays there once set

**c) Symmetry-based arguments:**
- Supersymmetry predicts Λ = 0 (boson-fermion cancellation), but SUSY is broken and the breaking scale is too high
- No known symmetry predicts Λ = 10⁻¹²² M_P⁴
- Scale invariance (conformal symmetry) would predict Λ = 0 but is badly broken

**d) Holographic arguments:**
- The de Sitter entropy S_dS = π/(G·Λ) ~ 10¹²² gives the number of degrees of freedom in our universe
- Some argue this has information-theoretic significance (our universe has maximal entropy / complexity)
- But this reverses the logic: it uses the observed Λ to compute S, not the other way around

**e) Topological quantization (Addazi & Meluccio 2025):**
- If Λ is quantized by topology, the observed value corresponds to a specific topological sector
- This is novel but speculative and requires pre-geometric gravity

### 5.3 What Would It Take for QG+F to Predict Λ?

For QG+F (or its extensions) to genuinely predict Λ, one would need:

1. **A mechanism that fixes the integration constant** in unimodular QG+F. Possible routes:
   - A boundary condition (e.g., the Hartle-Hawking no-boundary condition selects a specific Λ)
   - A self-consistency condition (e.g., the theory is consistent only for specific values of Λ)
   - A dynamical mechanism (e.g., Λ relaxes to its observed value during cosmic evolution)

2. **A connection between Λ and the known parameters of QG+F.** The theory has three parameters: G, M₂ (fakeon mass), M₀ (scalar mass). Could Λ be determined by these? For instance:
   - Λ ~ M₀⁴/M_P² would give Λ ~ 10⁻¹⁰ M_P⁴ — too large by 10¹¹²
   - Λ ~ e^{-M_P²/M₂²} · M_P⁴ could give exponential suppression, but this requires M₂ ~ 0.24 M_P (since e^{-17.3} ~ 10⁻⁸... doesn't work straightforwardly)
   - No natural combination of G, M₂, M₀ gives 10⁻¹²²

3. **A new principle or mechanism.** For example:
   - If the number of e-folds of inflation N_e determines Λ via Λ ~ e^{-N_e} · M_P⁴, and N_e ~ 280 (since e^{-280} ~ 10⁻¹²²), that would require ~280 e-folds — possible but arbitrary
   - If there is a deep connection between the de Sitter entropy S_dS ~ 10¹²² and the number of Planck-scale degrees of freedom, this could be constructive

**Honest assessment:** With current understanding, QG+F cannot predict Λ. The cosmological constant is a free parameter (integration constant in the unimodular formulation). No known extension of the framework determines its value without either fine-tuning, anthropic selection, or spacetime discreteness.

## 6. Synthesis: A Novel Approach?

Based on the analysis in Sections 2-5, here is my assessment of possible novel approaches:

### 6.1 The "Unimodular QG+F + Effective Poisson" Idea

**Concept:** Combine unimodular QG+F (which provides the Λ-V conjugacy and radiative stability) with some mechanism that produces effective Poisson fluctuations of the 4-volume.

**The obstacle:** No known continuum mechanism produces δV ~ √V. The everpresent-Λ mechanism specifically requires counting discrete spacetime atoms.

**A speculative possibility:** If the QG+F path integral, when evaluated non-perturbatively (perhaps via the AS dual), exhibits a first-order-like phase transition at the Planck scale, the volume could fluctuate between discrete vacua. In analogy with nucleation in first-order transitions, the number of "bubbles" per Hubble volume would follow Poisson statistics. This is highly speculative but identifies a conceptual direction.

**Viability:** LOW. The perturbative framework of QG+F provides no mechanism for this, and the non-perturbative sector is not well enough understood.

### 6.2 The "Sequestered QG+F" Idea

**Concept:** Apply Kaloper-Padilla vacuum energy sequestering to the QG+F action.

**What it would achieve:**
- Vacuum energy from all matter loops (including heavy fakeon loops!) is sequestered from gravity
- The residual CC is automatically small for a large, old universe
- Specific prediction: w ≈ -1 but the universe eventually collapses

**Obstacles:**
- Requires finite 4-volume (incompatible with eternal inflation)
- The global (non-local) variables in the sequestering mechanism may conflict with QG+F's locality
- The relationship between sequestering and the fakeon prescription is unexplored
- The prediction of future collapse is specific but currently untestable

**Viability:** MEDIUM. The Kaloper-Padilla mechanism is well-defined and addresses the right questions. The compatibility with QG+F is an open question worth investigating.

### 6.3 The "Topological Sector Selection" Idea

**Concept:** If the QG+F path integral includes topological sectors (as in the pre-geometric gravity approach of Addazi & Meluccio), the CC could be quantized and the correct sector selected dynamically.

**What it would achieve:**
- Λ is no longer continuously variable but takes discrete values
- SSB selects the observed sector
- No anthropic argument needed

**Obstacles:**
- Requires incorporating the Gauss-Bonnet term and topological structure into QG+F
- The Gauss-Bonnet term is topological in 4D and doesn't affect local dynamics — how it quantizes Λ is unclear
- The pre-geometric framework is very new (Feb 2025) and not yet validated

**Viability:** LOW-MEDIUM. Interesting conceptually but requires too many new ingredients beyond QG+F.

### 6.4 The Most Promising Direction: "Unimodular QG+F with Stochastic Scalar"

**Concept:** In the six-derivative extension of QG+F (motivated by the n_s tension, see Exploration 005), there are additional scalar degrees of freedom. If one of these scalars has the right properties, it could:

1. Couple to the trace of the Einstein equations (as in unimodular gravity)
2. Undergo stochastic fluctuations during and after inflation (via the stochastic inflation mechanism)
3. Produce an effective "fluctuating Λ" that mimics the everpresent-Λ without requiring discreteness

**More concretely:**
- In the six-derivative theory, the R³ term introduces a new scalar mode (beyond the R² Starobinsky scalar)
- If this mode is very light (m ≪ H₀), its quantum fluctuations during inflation produce a random field
- In the unimodular formulation, this field's VEV contributes to the effective Λ
- The variance of Λ contributions from this field scales as δΛ ~ H_inf² · (H₀/m)^{some power}

**Key calculation needed:** What is the mass of the additional scalar in the six-derivative QG+F theory? If it's ultra-light, it could produce observable dark energy fluctuations. If it's heavy (~ M_P), it decays quickly and has no late-time effect.

**From Exploration 005:** The R³ coefficient δ₃ ~ 10⁻⁴ suggests a new physics scale Λ_new ~ 3 × 10¹⁵ GeV. The additional scalar mass from the six-derivative theory is likely ~ Λ_new ~ 10⁻³ M_P, which is FAR too heavy to affect late-time cosmology.

**Assessment:** This doesn't work quantitatively. The six-derivative scalar is too heavy to produce late-time Λ fluctuations. A truly light scalar would need to be added by hand, which defeats the purpose.

### 6.5 Honest Assessment

**None of the above ideas provide a compelling, self-contained solution to the CC problem within QG+F.** The fundamental issue is:

1. **Unimodular QG+F solves the old CC problem** (why Λ isn't huge) — this is a genuine achievement
2. **The new CC problem** (why Λ ~ 10⁻¹²²) remains open in QG+F, as in all other approaches except:
   - Everpresent-Λ (requires discreteness, has observational problems)
   - Anthropic selection (unfalsifiable)
   - Pre-geometric topological quantization (too new, unvalidated)

3. **The most honest statement:** QG+F, combined with the unimodular formulation, provides a framework where Λ is a radiatively stable integration constant that doesn't receive quantum corrections. This is the best any continuum QFT approach can do. Explaining the specific value 10⁻¹²² likely requires either:
   - New physics beyond QG+F (spacetime discreteness, new symmetries, or topological structure)
   - Anthropic selection in a multiverse
   - A yet-undiscovered mechanism

## 7. Conclusions

### 7.1 Key Findings

1. **The everpresent-Λ mechanism is the most impressive prediction in quantum gravity** — it predicted Λ ~ H₀² before observation. But it requires spacetime discreteness and has serious observational difficulties (CMB tension, seed selection).

2. **Everpresent-Λ cannot be imported into QG+F.** The mechanism requires Poisson fluctuations from discrete spacetime atoms. No continuum analogue reproduces the crucial δV ~ √V scaling.

3. **Unimodular QG+F (Salvio 2024) solves the old CC problem.** Vacuum energy doesn't gravitate; the CC is a radiatively stable integration constant. This is a clean, well-defined framework.

4. **No approach within QG+F predicts the observed CC value.** The new CC problem remains open. Asymptotic safety doesn't help (Λ_IR is a free parameter). Vacuum energy sequestering is potentially compatible but untested. The six-derivative extension's new scalars are too heavy for late-time effects.

5. **The CC problem is the Achilles heel of all continuum QFT approaches to quantum gravity**, not just QG+F. Only approaches with spacetime discreteness (causal sets) or a very large landscape (string theory + anthropics) have claimed to address it.

### 7.2 Recommendations

1. **Adopt unimodular QG+F as the default formulation.** It costs nothing (same local physics) and solves the old CC problem.

2. **Investigate the compatibility of Kaloper-Padilla sequestering with QG+F.** This is the most promising untested combination.

3. **Track the everpresent-Λ observational program.** If a modified model (with suppressed high-z fluctuations) passes CMB tests, it would motivate finding a continuum analogue.

4. **Accept that Λ may be an input parameter.** Just as the Standard Model has ~19 free parameters, QG+F having Λ as a free parameter is not a failure — it's the honest statement of current understanding.

5. **The pre-geometric gravity approach (Addazi & Meluccio 2025) is worth watching** as a genuinely novel idea, but it requires substantial development before it can be evaluated against QG+F.
