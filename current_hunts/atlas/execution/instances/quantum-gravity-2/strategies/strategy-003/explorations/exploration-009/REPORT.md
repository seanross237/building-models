# Exploration 009: Discriminating Predictions for the Unified QG+F–AS Framework

## Goal

Find predictions that discriminate the UNIFIED QG+F–AS framework from:
1. Standalone QG+F or standalone AS
2. The "compatible-but-separate" interpretation (both theories correct, no deeper unity)

A discriminating prediction must be TRUE if unified, FALSE or INDETERMINATE if separate, and computationally or experimentally testable.

---

## 1. The Spin-2 Ghost Propagator — The Make-or-Break Computation

### What the unified framework predicts

If QG+F and AS are the same theory, the full non-perturbative graviton propagator (computed via C²-extended FRG) should show the spin-2 ghost pole **dissolving** — either into complex pole towers (Draper et al. 2020 pattern) or via mass divergence (Becker et al. 2017 mechanism). A persistent real ghost pole at negative residue would **kill** the framework.

### Current state of the computation

**Nobody has done this calculation.** The specific computation — reconstructing the transverse-traceless spin-2 sector of the graviton propagator within an (R + R² + C²) FRG truncation — has not been performed. Here is what exists:

- **Knorr & Saueressig (2022, SciPost Phys. 12, 001):** Reconstructed the graviton propagator from Euclidean FRG data. Found the spectral function of the *background* graviton necessarily has negative parts (indicating ghost-like contributions), while the *dynamical* graviton spectral function is positive. But this was done in an Einstein-Hilbert truncation — no C² term.

- **Draper, Knorr, Ripken & Saueressig (2020, PRL 125, 181301):** Computed finite gravity scattering amplitudes using momentum-dependent form factors. Found that ghost-like poles migrate to complex momenta, forming infinite towers. Crucially, physical amplitudes remain finite despite the poles. But this used a general form-factor ansatz, not specifically Stelle's ghost from C².

- **Antoniou, Gualtieri & Pani (2024, arXiv:2412.15037):** Computed QNMs of Schwarzschild BHs in quadratic gravity. Found new QNM classes corresponding to massive spin-2 degrees of freedom — the ghost modes. These are *perturbative* QNMs; they don't address the non-perturbative fate.

- **Platania & Wetterich (2020, PLB 811, 135911):** Argued that ghost poles in truncated effective actions can be "fictitious" — artifacts that vanish when all operators are included. Conceptual, not computational for the spin-2 case.

### Discrimination value

**HIGH — this is the single most discriminating computation.** Here's why:

| Outcome | Unified framework | Compatible-but-separate | Standalone QG+F |
|---------|-------------------|------------------------|-----------------|
| Ghost dissolves into complex towers | **PREDICTED** | Not predicted (no reason for AS dynamics to affect QG+F's ghost) | Contradicts perturbative ghost |
| Ghost mass → ∞ at NGFP | **PREDICTED** | Not predicted | Contradicts finite ghost mass |
| Ghost persists as real pole | **FALSIFIED** | Compatible | Standard prediction |

The "compatible-but-separate" view has no mechanism for the ghost to dissolve — it would require AS dynamics reaching into QG+F's perturbative structure. Only the unified theory predicts this because it identifies the ghost as a *perturbative artifact* of a single underlying theory.

### Feasibility

The calculation is well-defined but technically demanding. Requires:
1. FRG flow equations for the (R + R² + C²) truncation (partially available: Falls et al. 2023, SWY 2022)
2. Momentum-dependent form factors in the spin-2 sector (methodology exists from Knorr-Saueressig)
3. Spectral reconstruction from Euclidean to Lorentzian (methodology exists from Bonanno et al. 2022)

**Estimated difficulty:** A PhD-thesis-level computation. 1-2 years for an expert group (Knorr, Saueressig, or Platania groups). No fundamental obstruction.

**Verdict: DISCRIMINATING. Computationally testable. Not yet performed.**

---

## 2. The b Parameter — Can the NGFP Pin Down Inflation?

### What the unified framework predicts

The Bonanno-Platania inflation model uses:

    L_eff = (M_P²/2) R + (a/2) R² / [1 + b ln(R/μ²)]

where b parameterizes the NGFP correction strength. In standalone AS, b is a free parameter depending on truncation-dependent critical exponents. The unified framework predicts: **b is determined by the NGFP critical exponents**, not free.

### What the literature says

**Bonanno & Platania (2015, PLB 750, 638; 2018, PRD 98, 043505):** The parameter b is related to the anomalous scaling dimension near the NGFP. Specifically, the NGFP generates operators R^(2−θ/2) where θ > 0 is a critical exponent. The logarithmic correction arises as the leading modification to R² from the NGFP. The authors state the value of b₀ depends on the truncation and ask whether it can be constrained.

**The answer is: partially.** The critical exponents of the NGFP have been computed in many truncations:
- Einstein-Hilbert: θ₁,₂ = 1.48 ± 3.04i (complex pair)
- R² truncation: θ₁ = 2.38, θ₂,₃ = 1.26 ± 2.74i
- Higher truncations: values shift but remain O(1)

The parameter b is related to these via b ~ θ/(16π²), giving b ~ O(10⁻²). But the precise relation depends on the truncation, and no one has derived b from first principles in a controlled approximation.

### Discrimination value

**MODERATE.** Here's the issue:

| Scenario | Unified framework | Compatible-but-separate |
|----------|-------------------|------------------------|
| b computed from NGFP | **PREDICTED** — b is fixed, giving sharp r | Not predicted — b remains free |
| b remains free | Framework is weakened but not falsified | Default expectation |

If b could be computed from first principles and the resulting r matched observation, this would support unification. But the "compatible-but-separate" view could also accommodate a computed b — it would just mean AS independently predicts b, not that the two theories are unified.

**The discrimination is indirect:** the unified theory *requires* b to be computable; the separate theory merely *allows* it.

### Feasibility

Computing b from NGFP critical exponents requires tracking how the R² coupling flows from the NGFP to the inflationary regime, including the C² sector. This is essentially the same calculation as the AF→NGFP trajectory (open problem #1). Not yet done, but well-defined.

**Verdict: WEAKLY DISCRIMINATING. Computationally testable. More of a consistency check than a sharp discriminator.**

---

## 3. Fakeon Average Continuation Applied to FRG

### What the unified framework predicts

AS's Euclidean FRG (Wetterich equation) produces an effective action in Euclidean signature. Extracting Lorentzian physics requires analytic continuation. Standard Wick rotation is obstructed by complex poles (Donoghue 2020, Draper et al. 2020). The unified framework predicts: **Anselmi's fakeon average continuation is the correct prescription** for this extraction.

### Has anyone tried this?

**No.** No paper applies the fakeon average continuation to AS's Euclidean effective action. However, closely related work exists:

- **Baldazzi, D'Angelo, Knorr (2025, PRD 111, 106007; arXiv:2501.03752):** "Foliated Asymptotically Safe Gravity" — uses ADM decomposition to study Euclidean↔Lorentzian relations. Shows that Euclidean and Lorentzian FRG flows agree within Einstein-Hilbert truncation when using analytic continuation of the lapse function. The Lorentzian two-point function has the causal structure of the **Feynman propagator**. But they do NOT use the fakeon/average continuation — they use the standard Feynman prescription.

- **D'Angelo et al. (2024, PRD 109, 066012):** Demonstrated the NGFP directly in Lorentzian signature without any Wick rotation at all. This sidesteps the problem rather than solving it.

### Discrimination value

**MODERATE-TO-HIGH.** The key question is sharp:

| Outcome | Unified framework | Compatible-but-separate |
|---------|-------------------|------------------------|
| Average continuation produces well-defined Lorentzian physics from Euclidean FRG | **PREDICTED** — this is the framework's raison d'être | Not predicted — no reason to use QG+F's prescription in AS |
| Standard Wick rotation works fine (e.g., via Lorentzian AS) | Framework prediction is unnecessary | Default expectation |
| No consistent Euclidean→Lorentzian continuation exists | Both frameworks in trouble | Both in trouble |

The discrimination hinges on whether AS *needs* the average continuation. If Lorentzian AS (D'Angelo et al.) works perfectly without it, the unified framework's "average continuation resolves AS's problem" prediction becomes moot. This is a live research question.

### Feasibility

Applying the average continuation to the Wetterich equation is conceptually straightforward but technically novel. Requires:
1. Computing the Euclidean effective action in an (R + R² + C²) truncation
2. Applying Anselmi's average continuation prescription instead of standard Wick rotation
3. Comparing physical predictions (scattering amplitudes, spectral functions) with standard methods

**Estimated difficulty:** A single focused paper. 6-12 months for an expert.

**Verdict: MODERATELY DISCRIMINATING. Computationally testable but may be rendered moot by Lorentzian AS progress.**

---

## 4. Near-Term Predictions (Before 2030)

### QNM signatures from massive spin-2 modes

The most exciting near-term prospect. Antoniou, Gualtieri & Pani (2024) showed that Schwarzschild BHs in quadratic gravity have **new QNM classes** from massive spin-2 degrees of freedom. These are the ghost modes ringing.

**Key prediction from the unified framework:** If the ghost is confined (unified theory), these massive spin-2 QNMs should be **absent or suppressed** for astrophysical BHs (M >> M_P), because confinement removes the ghost from the physical spectrum at low energies. If the ghost is not confined (standalone QG+F with fakeon), the modes exist but are purely virtual — they don't contribute to the ringdown signal.

**Discrimination:** Both the unified framework and standalone QG+F predict the massive spin-2 QNMs are unobservable for astrophysical BHs (too heavy, ~M_P). The modes would only appear for Planck-mass BHs. **Not discriminating before 2030.**

### CMB tensor-to-scalar ratio

BICEP Array (2027-2028) will reach σ(r) ~ 0.003. This can detect r > 0.01 (strong standalone AS), but the unified framework predicts r ~ 0.003, right at the detection threshold. **Not cleanly discriminating before 2030.**

### Existing CMB tensions

The n_s tension (observed 0.974 vs. Starobinsky 0.967) is intriguing. The unified framework offers two resolution paths:
1. NGFP correction b ~ 10⁻² shifts n_s to ~0.975
2. Six-derivative terms from NGFP hierarchy give n_s ~ 0.974

But standalone AS also predicts these corrections. **Not uniquely discriminating.**

### LIGO O4/O5 gravitational waves

LIGO has logged 200+ GW events in O4. Higher-derivative corrections to GW waveforms are suppressed by (M_P/M_BH)² ~ 10⁻⁷⁶ for stellar-mass BHs. **Completely unobservable.**

**Verdict: NO discriminating experimental prediction before 2030.** The physics lives at the Planck scale; all near-term observations probe energy scales 15+ orders of magnitude too low.

---

## 5. The Null Hypothesis: "Compatible-but-Separate"

### Explicit statement

**Hypothesis H₀:** QG+F and AS are both valid descriptions of quantum gravity in their respective regimes — QG+F perturbatively above the Planck scale, AS non-perturbatively around it — but they are not manifestations of a single theory. They are compatible in the same way that chiral perturbation theory and lattice QCD are compatible descriptions of the strong force, without implying a deeper unity beyond QCD itself.

Wait — that analogy actually supports *unification*, not separation. Chiral perturbation theory and lattice QCD ARE the same theory (QCD) in different regimes.

**Better formulation of H₀:** QG+F and AS are both correct but describe *different aspects* of quantum gravity that happen to be compatible. Think of it like Newtonian gravity and thermodynamics — both correct, compatible, but not unified into a single framework in any deep sense. The compatibility is coincidental or reflects very general consistency constraints, not a shared underlying structure.

### What H₀ predicts differently

Under H₀:
- **Ghost fate:** The spin-2 ghost is QG+F's problem, and AS has its own separate mechanism for unitarity. There's no reason for AS's FRG dynamics to affect the ghost's pole structure.
- **b parameter:** Free, or determined by AS's own internal logic, with no connection to QG+F's C² coupling.
- **Average continuation:** Irrelevant to AS; AS solves its own Wick rotation problem independently (e.g., via Lorentzian AS).
- **Fixed points:** AF and NGFP are separate UV completions. No connecting trajectory needed or expected.

### Can ANY observation distinguish H_unified from H₀?

This is the crux. I identify **three** potential discriminators:

**Discriminator A: The ghost propagator computation** (Section 1). If the FRG in the (R + R² + C²) truncation shows the ghost dissolving, this *favors* unification because it means AS dynamics non-perturbatively resolves QG+F's ghost. Under H₀, there's no reason for this to happen — the ghost is QG+F's business, not AS's.

**Discriminator B: Coupling unification at the Planck scale.** If the unified theory predicts that QG+F's couplings (α_R², α_C²) at the Planck scale exactly match AS's NGFP fixed-point values, this requires a shared underlying structure. Under H₀, the couplings are independent.

**Discriminator C: Cross-framework consistency checks.** If the spectral dimension profile d_s(E) computed perturbatively (QG+F) and non-perturbatively (AS) match in the overlap regime (E ~ M_P), this suggests a single theory. If they disagree, it suggests separation.

### Honest assessment

**Discriminators B and C are consistency checks, not predictions.** They can *support* or *tension* the framework, but a match could also be explained by H₀ (both theories are correct, so of course they agree where applicable).

**Only Discriminator A is genuinely novel to unification.** The ghost dissolution is predicted *because* QG+F and AS share the same action; it is *not predicted* by the compatible-but-separate view.

---

## 6. Verdict: Is the Framework Falsifiable?

### The honest answer

**The unified QG+F–AS framework is falsifiable in principle but not in practice within 5 years.** Its falsifiability rests entirely on computational tests — specifically the spin-2 ghost propagator computation — not on near-term experiments.

### Discriminating predictions identified: 2

**Prediction 1 (STRONG): Ghost pole dissolution in the C²-extended FRG.**
- True if unified, false if separate
- Computationally testable (1-2 year calculation)
- Clear pass/fail criterion: ghost dissolves → supports; ghost persists → falsifies
- This is the ONE prediction that genuinely discriminates

**Prediction 2 (MODERATE): The average continuation produces correct Lorentzian physics from Euclidean FRG.**
- True if unified, unnecessary if separate
- Computationally testable (6-12 month calculation)
- Less clean: if Lorentzian AS works independently, this becomes moot

### What would make the framework more falsifiable

1. **Compute the AF→NGFP trajectory.** If it exists, extract the b parameter and predict a specific r value. If that r is measured by LiteBIRD (~2037), the framework gains an experimental test.
2. **Compute the ghost confinement scale.** If the unified theory predicts Λ_ghost = M_P from dynamics (not by hand), this is a non-trivial consistency check.
3. **Find a matter-sector prediction.** The Shaposhnikov-Wetterich Higgs mass prediction (m_H ~ 126 GeV) could become discriminating if it requires the fakeon prescription to work — but this hasn't been investigated.

### Bottom line

The framework is a **well-formed scientific conjecture** with **one genuinely discriminating computational prediction** (ghost dissolution) and **several weaker consistency checks**. It is not currently experimentally falsifiable. Its scientific status depends entirely on whether the ghost propagator computation is performed. Until then, it remains a conjecture — not wrong, not right, not testable in practice.

The "compatible-but-separate" interpretation is simpler (Occam's razor) and makes no prediction that the unified framework contradicts. The unified framework's advantage is that it *explains* the compatibility rather than treating it as coincidental — but this explanatory advantage only becomes scientific if the ghost dissolution prediction is confirmed computationally.
