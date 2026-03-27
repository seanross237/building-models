# Exploration 005: Predictions of the Unified QG+F–AS Framework in Three Domains

## Goal

Assess what the unified QG+F–AS framework **actually predicts** in three specific domains — spectral dimension, cosmological constant, and gravitational waves — and classify each prediction honestly as:

- **DISCRIMINATING** — uniquely distinguishes this framework from alternatives; testable
- **NOVEL** — new prediction not found in constituent frameworks alone
- **CONSISTENCY CHECK** — matches expected or universal behavior; necessary but not unique
- **INHERITED** — prediction comes from a sub-theory (Starobinsky, AS, or standalone QG+F), not from the unified combination

The instruction is to be honest: if the unified framework has nothing new in a domain, say so.

---

## Domain 1: Spectral Dimension

### What Is the Spectral Dimension?

The spectral dimension d_s measures the effective dimensionality of spacetime as probed by a diffusion process (random walk) at a given length scale. It is defined through the return probability of a random walker:

```
P(σ) ~ σ^{-d_s/2}
```

where σ is the diffusion time (a proxy for length scale). For a quantum field theory with propagator G(k) ~ 1/k^{2n}, the heat kernel trace evaluates to:

```
K(σ) = ∫ d^d k/(2π)^d  exp(−σ k^{2n}) ~ σ^{−d/(2n)}
```

Reading off: **d_s = d/n**, where d is the topological spacetime dimension and n is the power of the kinetic operator in the UV.

This formula was placed on rigorous footing by Sotiriou, Visser & Weinfurtner (2011, PRD 84, 104018; arXiv:1105.6098), who showed how to assign a spectral dimension to any dispersion relation. For Hořava–Lifshitz gravity with dynamical exponent z in D+1 dimensions, the related formula is d_s = 1 + D/z.

### The Universal d_s = 2 Result

Carlip (2019, Universe 5, 83; arXiv:1904.04379) surveyed spectral dimension results across quantum gravity and found that d_s → 2 in the UV is near-universal:

| Approach | UV spectral dimension | Mechanism |
|----------|----------------------|-----------|
| Causal Dynamical Triangulations | d_s ≈ 2 (numerical, Ambjorn et al. 2005) | Lattice path integral over geometries |
| Asymptotic Safety | d_s = 2 (analytic) | Anomalous dimension η_N = −2 at NGFP |
| Hořava–Lifshitz (z = 3) | d_s = 1 + 3/3 = 2 | Anisotropic scaling between space and time |
| Loop Quantum Gravity | d_s ~ 2 (indications, Modesto 2009) | Area quantization modifies propagation |
| Causal Set Theory | d_s ~ 2 (indications) | Discrete spacetime structure |
| Multi-fractional spacetimes | d_s = 2 (Calcagni 2010, 2012) | Fractional calculus; telegraph process |

Calcagni (JHEP 03, 120, 2010; arXiv:1204.2550, 2012) showed that a fractional telegraph process describes quantum spacetimes with d_s = 2 in the UV rising monotonically to 4 in the IR. He established this as a universal feature of quantum geometry, not tied to any particular quantization scheme.

### What QG+F Predicts

**Four-derivative QG+F:** The graviton propagator in quadratic gravity (R + R² + C²) scales as 1/k⁴ at high momenta — this is the defining UV property that makes the theory renormalizable (Stelle 1977). Applying the formula:

```
n = 2  →  d_s = 4/2 = 2    (UV limit)
```

The full flow profile:
- d_s = 4 for E ≪ M₀ (inflaton mass, ~3×10¹³ GeV) — standard GR regime
- d_s transitions through intermediate values for M₀ < E < M₂
- d_s → 2 for E ≫ M₂ (fakeon mass, 10¹³–10¹⁷ GeV) — quadratic gravity regime

**Six-derivative extension:** If the theory is extended to include R³ and other dimension-6 operators (motivated by the n_s tension — see exploration 005 Part B in the earlier report), the propagator scales as 1/k⁶ in the deep UV:

```
n = 3  →  d_s = 4/3 ≈ 1.33    (deep UV limit)
```

This gives a two-step flow: d_s = 4 (IR) → 2 (QG+F regime) → 4/3 (six-derivative regime). The second transition occurs at the six-derivative mass scale, Λ₆ ~ 100 M₀ ~ 3×10¹⁵ GeV.

### What the Unified QG+F–AS Framework Adds

The unified framework requires that the spectral dimension profile matches between the perturbative (QG+F) and non-perturbative (AS) descriptions in the overlap regime around the Planck scale. The library's novel-predictions.md (Prediction #5) states this explicitly:

> "The interpolation d_s = 4 (IR) → d_s = 2 (UV) must match between both descriptions. Disagreement in the overlap regime would falsify the unified framework."

This is a self-consistency requirement, not a prediction about the world.

### Top Predictions and Classification

**Prediction 1: d_s → 2 in the UV**
- **Classification: CONSISTENCY CHECK**
- This is the same universal result found in every major quantum gravity approach. It follows trivially from QG+F's 1/k⁴ propagator. The AS side independently gives d_s = 2 from η_N = −2. Their agreement is required for internal consistency of the unified framework, not a new prediction about nature.
- **Honest verdict:** The framework passes the test but adds zero new information. Any theory with improved UV propagator behavior gets d_s = 2 for free.

**Prediction 2: Two-step flow d_s = 4 → 2 → 4/3 (six-derivative extension only)**
- **Classification: NOVEL (but unobservable)**
- The second step (2 → 4/3) is unique to six-derivative gravity. Most QG approaches predict monotonic flow from 4 to 2. A non-monotonic or multi-step profile would be distinctive.
- However: this occurs at energies above 3×10¹⁵ GeV. No known observable probes the spectral dimension at these scales. The prediction is unique but untestable by any foreseeable experiment.

### Honest Assessment for Spectral Dimension

**The unified QG+F–AS framework has nothing genuinely new to say about the spectral dimension.** The d_s = 2 result is universal — you get it from the propagator structure alone, with no input from the specific dynamics of the theory. The specific interpolating profile d_s(E) through the QG+F mass scales might differ from AS or CDT in detail, but:

1. Nobody has computed the full interpolating profile for QG+F with specific particle content
2. Even if computed, the intermediate regime (E ~ 10¹³–10¹⁹ GeV) is completely unobservable
3. The agreement between QG+F and AS on d_s = 2 is valuable as a self-consistency check but adds zero predictive content about nature

---

## Domain 2: Cosmological Constant

### The Problem

The cosmological constant problem has two parts:
- **Old problem:** Why isn't Λ at least as large as the largest particle mass scale? Radiative corrections generate δΛ ~ M⁴/(16π²) for any mass M in the theory.
- **New problem:** Why does the observed Λ ~ (2.3 × 10⁻³ eV)⁴ ≈ 4 × 10⁻⁴⁷ GeV⁴ have its particular tiny value?

### What QG+F Predicts

**QG+F does NOT solve the cosmological constant problem.** The massive fields in QG+F generate standard radiative corrections to Λ:

```
δΛ ~ M₂⁴/(16π²)
```

For M₂ ~ 10¹³ to 10¹⁷ GeV (the fakeon mass range):
```
δΛ ~ 10⁴⁸ to 10⁶⁴ GeV⁴
```

The observed value is Λ_obs ~ 4 × 10⁻⁴⁷ GeV⁴. The discrepancy is **95 to 111 orders of magnitude**. QG+F treats Λ as a free parameter that must be fine-tuned, exactly as in standard GR + QFT.

Anselmi (2019, JHEP 12, 027; arXiv:1909.04955) addressed the cosmological constant only insofar as showing that scattering amplitudes expanded around flat space "obey the optical theorem up to corrections due to Λ, which are negligible for all practical purposes." The fakeon prescription does not provide any mechanism for explaining the smallness of Λ.

### What Asymptotic Safety Predicts (Bonanno–Reuter)

Bonanno & Reuter (2002, PLB 527, 9; PRD 65, 043508) showed that in asymptotic safety the dimensionless cosmological constant λ(k) = Λ(k)/k² runs to a fixed-point value at the NGFP:

```
λ(k) → λ* ~ O(0.1–0.3)    as k → ∞
```

This means Λ(k) ~ λ* k² in the UV (very large), flowing to a small IR value. The critical features:

- The running provides a **mechanism** (dimensional transmutation from the UV fixed point) for Λ to be small in the IR
- But the exact IR value depends on which RG trajectory the universe follows
- The trajectory is selected by initial conditions — it is a **free parameter**
- Different trajectories give different values of Λ_obs

**The running replaces one fine-tuning (bare Λ) with another (trajectory selection).** This is analogous to QCD: the running coupling explains why α_s is small at high energies, but Λ_QCD ~ 200 MeV is a free parameter, not predicted from first principles.

Bonanno & Reuter argued that if the universe is in a "classical regime" (necessary for observers), then Λ is automatically much smaller than M_P². But this is an anthropic/naturalness argument, not a dynamical prediction. The specific observed value (2.3 × 10⁻³ eV)⁴ is not derived.

### The Unimodular Variant (Salvio 2024)

Salvio (2024, PLB 856, 138920; arXiv:2406.12958) proposed unimodular quadratic gravity, which imposes the unimodular constraint (det g = fixed) on the non-perturbative quantum path integral. Key results:

- The unimodular constraint makes Λ an **integration constant** rather than a parameter in the action
- Vacuum energy contributions (zero-point fluctuations, phase transitions) do **not** gravitationally weigh — addressing the old CC problem
- However, the new CC problem (why Λ has its observed value) is **not solved**; Salvio resorts to anthropic reasoning
- The unimodular constraint leads to "slightly different predictions for some inflationary quantum observables" — but these differences are within current observational uncertainties

Crucially: unimodular gravity is a **generic modification** applicable to any metric theory. It is not specific to QG+F or the unified framework.

### What the Unified QG+F–AS Framework Adds

**Nothing beyond what the individual frameworks already provide.**

- From QG+F: Λ is a free parameter, fine-tuning needed
- From AS: Λ runs from large UV values to small IR values, but trajectory is free
- From the combination: no new mechanism emerges

The unified framework does not even offer a novel *perspective* on the CC problem. The QCD analogy (which is central to the unified framework's structure) actually makes the situation *worse*: in QCD, the analog of Λ (i.e., Λ_QCD) is a free parameter determined by experiment, not predicted from the theory. By this same structural analogy, Λ_gravity would also be a free parameter — exactly the unsatisfying status quo.

### Top Predictions and Classification

**Prediction 1: Radiative corrections δΛ ~ M₂⁴/(16π²) ≫ Λ_obs**
- **Classification: INHERITED (from standard QFT)**
- This is the same cosmological constant problem that afflicts every quantum field theory. QG+F inherits it without modification. The framework has no mechanism to cancel or suppress these contributions.

**Prediction 2: (If unimodular variant adopted) Vacuum energy decoupled from Λ**
- **Classification: INHERITED (from unimodular gravity, not from the unified framework)**
- Unimodular gravity predates QG+F and can be combined with any gravitational theory. Its application to quadratic gravity is natural but not a prediction of the unified QG+F–AS framework. The CC value remains unexplained.

### Honest Assessment for Cosmological Constant

**The unified QG+F–AS framework has nothing new to say about the cosmological constant.** This is the single largest gap in the framework's predictive power. The CC problem is arguably the most important open problem in theoretical physics, and the framework offers:

- No mechanism for the smallness of Λ
- No dynamical explanation for its value
- No qualitative improvement over the standard (deeply unsatisfying) situation
- Not even a novel reformulation of the problem

The Bonanno–Reuter running in AS is the most interesting ingredient, but it does not constitute a prediction — it replaces one free parameter with another. The honest conclusion: **the CC problem is completely open within this framework.**

---

## Domain 3: Gravitational Waves

### Background

Gravitational wave observations offer the most promising near-term tests of quantum gravity through three channels:

1. **Primordial tensor spectrum** (from inflation): tensor-to-scalar ratio r and tensor spectral index n_T
2. **Stochastic gravitational wave background**: from reheating, phase transitions, cosmic strings
3. **Modified GW propagation**: dispersion, speed changes, extra polarizations from massive modes

### What QG+F Predicts: Tensor-to-Scalar Ratio

Anselmi, Bianchi & Piva (2020, JHEP 07, 211; arXiv:2005.10293) derived the inflationary tensor spectrum in QG+F. The C² term (with the spin-2 ghost quantized as a fakeon) introduces a suppression factor:

```
r = r_Starobinsky × (1 + 2H*²/M₂²)⁻¹
```

where H* is the Hubble parameter at horizon crossing and M₂ = f₂ M_P/√2 is the fakeon mass.

**Regime analysis:**
- M₂ ≫ H* (heavy fakeon): r → r_Starobinsky = 12/N² ≈ 0.003–0.004
- M₂ ~ H* (comparable masses): r ≈ r_Starobinsky/3 ≈ 0.001
- M₂ = M₀/4 (minimum from consistency): r → 4/(3N²) ≈ 4 × 10⁻⁴

The consistency condition M₂ > M₀/4 (from perturbative unitarity of the inflaton-fakeon system) gives the combined bound:

```
4/3 < N²r < 12
```

For N = 55 e-folds: **r ∈ [4.4 × 10⁻⁴, 4.0 × 10⁻³]**

This was confirmed independently by Bianchi & Gamonal (2025, arXiv:2502.03543), who computed the full tensor power spectrum implementing the fakeon prescription. They found the suppression factor (1 + 2H*²/m_gh²)⁻¹ applies to both the amplitude and spectral index.

### What QG+F Predicts: Consistency Relation

Bianchi & Gamonal (2025) proved that the standard single-field consistency relation is preserved in QG+F:

```
r = −8 n_T    (to leading order in slow-roll)
```

This is a **non-trivial** result. The C² term adds a massive spin-2 degree of freedom (the fakeon), which could in principle modify the tensor spectrum in a way that breaks this relation. Theories with additional propagating tensor modes (e.g., bigravity) do violate it. The fact that the fakeon, being purely virtual, leaves the relation intact is a specific prediction about the tensor sector.

### What QG+F Predicts: Absence of Beyond-GR GW Effects

The fakeon is purely virtual — it does not propagate as a classical wave. Therefore QG+F predicts:

- **No extra GW polarizations** beyond the two standard ones (+ and ×)
- **No modified GW dispersion** (no frequency-dependent speed)
- **No anomalous GW speed** (c_GW = c exactly, at tree level)
- **No massive graviton effects** in interferometer signals

This is a **negative prediction** — QG+F predicts the absence of the signatures that many alternative gravity theories produce. Current LIGO/Virgo/KAGRA observations already constrain some of these effects, and all current data are consistent with QG+F's prediction of GR-like propagation.

The only channel for massive spin-2 effects is through quasi-normal modes of black holes. But these are suppressed by (M_P/M_BH)² ~ 10⁻⁷⁶ for astrophysical black holes — completely unobservable with any foreseeable technology (see library discriminating-predictions.md).

### What About the Stochastic Background?

**Important clarification:** Calcagni & Modesto (2024, JHEP 12, 024; arXiv:2206.07066) predicted a blue-tilted stochastic gravitational wave background observable by DECIGO, with r₀.₀₅ ≈ 0.01. However, their prediction is for **nonlocal quantum gravity** (Weyl-invariant, nonpolynomial entire functions) — a fundamentally different theory from QG+F. QG+F is local and polynomial. The blue-tilt prediction does NOT transfer to QG+F.

For QG+F specifically: the primordial tensor spectrum is **red-tilted** (n_T < 0, with n_T ≈ −r/8 ~ −4 × 10⁻⁴), following the standard slow-roll consistency relation. Any post-inflationary stochastic background contribution depends on the reheating mechanism, which involves model-dependent assumptions about matter couplings and is not a clean prediction of the gravitational sector alone.

### What the Unified Framework Adds

The unified QG+F–AS framework sharpens the r prediction through the NGFP parameter b (from novel-predictions.md, Prediction #4):

```
r = 3(1 − β/(6α))(n_s − 1)² / (1 + b ln(R/μ²))
```

where b is determined by NGFP anomalous dimensions. Most reliable AS calculations give b ~ 0, predicting r ~ 0.003 for N = 55. But:

- b has NOT been derived from first principles in a controlled approximation
- The relation between b and NGFP critical exponents θ is not established quantitatively
- Until b is computed, this is a framework for a prediction, not a prediction itself

The six-derivative extension (with R³ correction δ₃ ≈ −1.2 × 10⁻⁴) gives:
- r ≈ 0.004–0.005 (slightly enhanced over pure Starobinsky)
- Correlated with n_s ≈ 0.974
- This (n_s, r) pair is a specific testable prediction of the extended theory

### Top Predictions and Classification

**Prediction 1: Bounded tensor-to-scalar ratio r ∈ [4×10⁻⁴, 4×10⁻³]**
- **Classification: DISCRIMINATING**
- The **upper bound** (r < 12/N² ≈ 0.004) is INHERITED from Starobinsky inflation — not unique to QG+F.
- The **lower bound** (r > 4/(3N²) ≈ 4×10⁻⁴) is GENUINELY NEW. It comes from: (1) the fakeon mass must exceed M₀/4 from perturbative unitarity in QG+F, (2) this limits how much the tensor spectrum can be suppressed. No other inflationary model has this specific lower bound from quantum gravity consistency.
- **Testability:** LiteBIRD (launch ~2032) aims for σ(r) ~ 3 × 10⁻³. CMB-S4 aims for σ(r) ~ 10⁻³. If r < 4 × 10⁻⁴ is measured, the standard QG+F framework with Starobinsky inflation is falsified. If r is detected in the predicted range, it constrains M₂/M₀ (the fakeon-to-inflaton mass ratio).
- **This is the strongest prediction of the framework across all three domains.**

**Prediction 2: Slow-roll consistency relation r = −8 n_T preserved**
- **Classification: CONSISTENCY CHECK**
- The preservation of this relation is non-trivial (the C² term could break it) and has been verified computationally (Bianchi & Gamonal 2025). However, any theory without new propagating tensor degrees of freedom at the inflationary scale will preserve it. Since the fakeon is purely virtual, this is expected. It confirms the framework's internal consistency but does not uniquely distinguish it from standard single-field inflation.

---

## Cross-Domain Summary Table

| Domain | Top Prediction | Classification | Testable? | Honest Verdict |
|--------|---------------|---------------|-----------|----------------|
| Spectral Dimension | d_s: 4 → 2 in UV | CONSISTENCY CHECK | No | Universal result. Framework adds nothing. |
| Spectral Dimension | Two-step 4→2→4/3 (6-deriv) | NOVEL | No | Unique but trans-Planckian. Unobservable. |
| Cosmological Constant | Λ is free; δΛ ~ M₂⁴/(16π²) | INHERITED | N/A | Standard CC problem. No new mechanism. |
| Cosmological Constant | (Unimodular) Λ as integration const. | INHERITED | Marginal | Not specific to this framework. |
| **Gravitational Waves** | **r ∈ [4×10⁻⁴, 4×10⁻³]** | **DISCRIMINATING** | **Yes (2032–2035)** | **The one strong prediction.** |
| Gravitational Waves | r = −8 n_T preserved | CONSISTENCY CHECK | Yes (needs r first) | Non-trivial but not unique. |

---

## Bottom Line

The unified QG+F–AS framework has **one genuinely discriminating prediction** across these three domains: the bounded tensor-to-scalar ratio from the fakeon mass constraint, testable by LiteBIRD and CMB-S4 within the next decade.

The spectral dimension prediction is a universal consistency check that every quantum gravity approach passes — the framework adds nothing here. The cosmological constant is a complete blank — the framework inherits the standard problem without any improvement, mechanism, or even novel reformulation.

**The framework's predictive power is narrowly concentrated in the CMB/inflationary sector** (n_s, r, and their correlations). This is not a criticism — the inflationary predictions are genuinely strong and testable — but any claims of broad predictive reach across quantum gravity phenomenology should be tempered by the honest absence of novel content in spectral dimension and cosmological constant.

The most productive next steps for expanding the framework's predictive reach are:
1. Computing the full d_s(E) interpolation profile in QG+F (might reveal non-trivial structure in the transition regime, even if unobservable)
2. Investigating whether the ghost confinement mechanism has any implications for the CC problem (currently unexplored)
3. Computing the NGFP parameter b to sharpen the r prediction from "bounded range" to "specific value"

---

## References

1. Carlip, "Dimension and Dimensional Reduction in Quantum Gravity," Universe 5, 83 (2019). [arXiv:1904.04379](https://arxiv.org/abs/1904.04379)
2. Calcagni, "Quantum field theory, gravity and cosmology in a fractal universe," JHEP 03, 120 (2010).
3. Calcagni, "Diffusion in quantum geometry," [arXiv:1204.2550](https://arxiv.org/abs/1204.2550) (2012).
4. Sotiriou, Visser & Weinfurtner, "From dispersion relations to spectral dimension — and back again," PRD 84, 104018 (2011). [arXiv:1105.6098](https://arxiv.org/abs/1105.6098)
5. Bonanno & Reuter, "Cosmology with self-adjusting vacuum energy density from a renormalization group fixed point," PLB 527, 9 (2002).
6. Bonanno & Reuter, "Cosmology of the Planck era from a renormalization group for quantum gravity," PRD 65, 043508 (2002).
7. Salvio, "Unimodular Quadratic Gravity and the Cosmological Constant," PLB 856, 138920 (2024). [arXiv:2406.12958](https://arxiv.org/abs/2406.12958)
8. Anselmi, Bianchi & Piva, "Predictions of quantum gravity in inflationary cosmology: effects of the Weyl-squared term," JHEP 07, 211 (2020). [arXiv:2005.10293](https://arxiv.org/abs/2005.10293)
9. Bianchi & Gamonal, "Primordial Gravitational Waves in Quadratic Gravity," (2025). [arXiv:2502.03543](https://arxiv.org/abs/2502.03543)
10. Anselmi, "Fakeons, unitarity, massive gravitons and the cosmological constant," JHEP 12, 027 (2019). [arXiv:1909.04955](https://arxiv.org/abs/1909.04955)
11. Calcagni & Modesto, "Testing quantum gravity with primordial gravitational waves," JHEP 12, 024 (2024). [arXiv:2206.07066](https://arxiv.org/abs/2206.07066)
12. Buccio, Donoghue, Menezes & Percacci, "Physical running of couplings in quadratic gravity," PRL 133, 021604 (2024). [arXiv:2403.02397](https://arxiv.org/abs/2403.02397)
