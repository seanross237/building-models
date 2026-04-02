---
topic: cross-cutting
confidence: provisional
date: 2026-03-26
source: exploration-006-analyticity-reconciliation (quantum-gravity-2 strategy-003)
---

# QG+F vs. AS Analyticity Compatibility Analysis

Systematic assessment of whether QG+F's sacrifice of S-matrix analyticity is compatible with Asymptotic Safety's Euclidean functional RG framework. **Verdict: SUPPORTS — the analyticity sacrifice is not a barrier to QG+F = AS. If anything, it may be a feature that helps AS solve its own known problems.**

## The Apparent Tension

QG+F explicitly forfeits S-matrix analyticity (the fakeon is the ONLY prescription preserving both unitarity and Lorentz invariance — see `../quadratic-gravity-fakeon/analyticity-sacrifice.md`). AS is traditionally formulated in Euclidean signature using the Wetterich equation. At first glance, AS seems to *require* analyticity for Wick rotation (Euclidean → Lorentzian), making the two frameworks incompatible.

**This tension is illusory.** It dissolves under examination in three steps.

## Step 1: AS Does Not Require Analyticity

The Wetterich equation (exact functional RG equation) is formulated in Euclidean signature. It integrates out quantum fluctuations shell-by-shell. However:

1. **The FRG is a computational tool, not an analyticity assumption.** It produces a scale-dependent effective action Γ_k. It requires well-defined Euclidean correlation functions but does NOT require standard analytic continuation properties.

2. **Physical prediction extraction is separate.** Wick rotation from Euclidean → Lorentzian is where analyticity traditionally enters, but this step is separate from the FRG computation itself.

3. **Osterwalder-Schrader is sufficient, not necessary.** The OS framework provides sufficient conditions (reflection positivity) for Euclidean correlators to reconstruct a unitary Lorentzian theory. But theories violating OS axioms may still have consistent Lorentzian physics through alternative continuation procedures.

## Step 2: AS Already Has Non-Standard Analytic Structure

**AS's own pole structure obstructs standard Wick rotation.** The supposed tension — "QG+F breaks analyticity but AS needs it" — is based on a false premise.

### Donoghue's Wick rotation obstruction (Front. Phys. 2020, arXiv:1911.02967)
- The ghost pole in quadratic gravity (the natural truncation of AS) sits in the **upper right quadrant** of the complex q₀ plane
- Standard Wick rotation requires rotating the q₀ contour by 90° — this sweeps over the ghost pole
- **Any truncation without tachyons will likely have poles obstructing analytic continuation**
- Recognized as a major open problem within the AS program itself

### Draper, Knorr, Ripken, Saueressig (PRL 125, 2020; JHEP 2020)
- Graviton propagator has **infinite towers of spin-0 and spin-2 poles at imaginary squared momentum**
- These are not standard real-axis poles
- Scattering amplitudes are compatible with unitarity bounds and causal, but the pole structure is highly non-standard
- Poles at imaginary p² obstruct naive Wick rotation

### Bonanno, Denz, Pawlowski, Reichert (SciPost Phys. 12, 2022)
- Reconstructed Lorentzian graviton spectral function from Euclidean FRG data
- Must **assume** "the existence of a standard Wick rotation at least for backgrounds close to flat ones" — cannot derive it
- **Excludes** complex conjugate poles, stating such extensions "may signal the loss of unitarity"
- Acknowledges Wick rotation remains "one of the remaining challenges yet to be met" in AS

## Step 3: Lorentzian AS Bypasses the Issue Entirely

The Euclidean formulation of AS is NOT fundamental. Lorentzian formulations exist:

### D'Angelo, Drago, Pinamonti, Rejzner (Phys. Rev. D 109, 2024; arXiv:2310.20603)
**Landmark result:** First background-independent evidence of asymptotic safety directly in Lorentzian signature.
- NGFP exists in Lorentzian signature at (g*, λ*) = (1.15, 0.42)
- **No Wick rotation needed** — Lorentzian FRGE developed directly in Lorentzian spacetimes
- **No analyticity required** — operates without analytic continuation
- Fixed point values differ from Euclidean (0.34, 0.3), reflecting different signatures and regulators

### Manrique, Reuter, Saueressig (2011; arXiv:1102.5012)
Introduced causal FRG connecting Euclidean and Lorentzian RG flows without standard analytic continuation.

### Foliated AS (Baldazzi, D'Angelo, Falls, 2025; arXiv:2501.03752)
Achieves Wick rotation by rotating the lapse function rather than time coordinate:
- Euclidean and Lorentzian beta functions are **identical** with careful regulator choice
- Requires spatial regulators that don't introduce new poles
- Equivalence is "highly non-trivial"

**If AS can be formulated entirely in Lorentzian signature, it cannot require analyticity.**

## The Deeper Point: Same Phenomenon, Two Perspectives

The QG+F analyticity sacrifice and AS's Wick rotation obstruction may be **the same phenomenon** seen from different angles:
- **QG+F** explicitly acknowledges the non-analyticity and handles it systematically via the fakeon "average continuation" (Anselmi JHEP 2018, arXiv:1801.00915) — a nonanalytic but well-defined Euclidean→Lorentzian procedure
- **AS** has the same non-analyticity hidden in its complex pole structure but hasn't yet developed a systematic handling procedure
- The fakeon prescription may be **exactly the tool AS needs** for Euclidean→Lorentzian extraction

## Fakeon and FRG Operate at Different Levels

The two mechanisms are compatible because they address different stages:

| Level | Tool | Analyticity role |
|-------|------|-----------------|
| FRG computation (Euclidean) | Wetterich equation | None required — purely Euclidean |
| Physics extraction (E→L) | Standard: Wick rotation | Requires analyticity (fails due to complex poles) |
| Physics extraction (E→L) | Fakeon: average continuation | Does NOT require analyticity (handles complex poles) |
| Direct Lorentzian | Lorentzian FRGE | No continuation needed at all |

## Evidence Strength

| Evidence | Weight |
|---|---|
| Lorentzian AS exists without analyticity (D'Angelo et al. 2024) | Strong |
| AS's own poles obstruct standard Wick rotation (Donoghue, Draper) | Strong |
| FRG is computational tool, not analyticity requirement | Moderate |
| Fakeon average continuation could solve AS's Wick rotation problem | Suggestive |
| Platania-Wetterich ghost disappearance might eliminate the issue entirely | Speculative |

## Verdict: SUPPORTS

The analyticity sacrifice is not a barrier to QG+F = AS. The three-step argument (AS doesn't need analyticity → AS already lacks standard analyticity → Lorentzian AS bypasses analyticity entirely) is robust. The fakeon prescription may be a feature, not a bug: it provides the systematic Euclidean→Lorentzian extraction tool that the AS program currently lacks.

**This is the third SUPPORTS verdict in the QG+F = AS reconciliation program**, joining CMB predictions (`qgf-vs-as-cmb-discrimination.md`, MODERATE) and black hole compatibility (`qgf-vs-as-bh-compatibility.md`, SUPPORTS). No aspect of QG+F examined so far has proven incompatible with AS.

Sources: Anselmi et al. JHEP 05 (2025) 145; Anselmi JHEP 02 (2018) 141; Donoghue Front. Phys. 8 (2020) 56; Draper et al. PRL 125 (2020) 181301; Bonanno et al. SciPost Phys. 12 (2022) 001; D'Angelo et al. Phys. Rev. D 109 (2024) 066012; Manrique et al. arXiv:1102.5012; Baldazzi et al. arXiv:2501.03752; Platania & Wetterich PLB 811 (2020) 135911
