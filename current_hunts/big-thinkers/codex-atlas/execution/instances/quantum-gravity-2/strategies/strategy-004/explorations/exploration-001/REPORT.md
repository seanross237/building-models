# Exploration 001: Ghost Propagator Specification — Detailed Report

## Goal
Derive the specific quantitative predicted outcome of the spin-2 ghost propagator computation in C²-extended FRG for the Unified QG+F–AS Framework. Make the prediction precise enough to specify a concrete calculation with numerical values.

---

## Section 1: Fixed-Point Values from Benedetti et al. 2009

### Source
Benedetti, Machado, Saueressig — "Asymptotic safety in higher-derivative gravity" (arXiv:0901.2984), with summary proceedings in arXiv:0909.3265.

### Action Ansatz
The four-derivative truncation (Eq. 4 of 0901.2984):

    Γₖ = ∫d⁴x√g [u₀ + u₁R − (ω/3λ)R² + (1/2λ)C² + (θ/λ)E]

where E is the Gauss-Bonnet density. Linear combinations used:
- u₂ = −ω/(3λ) + θ/(6λ)  → R²-related
- u₃ = 1/(2λ) + θ/λ → C²-related

Dimensionless couplings: gᵢ = k^(−dᵢ) uᵢ. For the higher-derivative terms (dimension-0 operators), g₂ = u₂ and g₃ = u₃ directly.

### NGFP Fixed-Point Values (Eq. 12)

| Coupling | Value | Physical meaning |
|----------|-------|------------------|
| g₀* | 0.00442 | Cosmological constant (dim-4) |
| g₁* | −0.0101 | Newton's constant (dim-2, Euclidean sign) |
| g₂* | 0.00754 | R²-related (dimensionless) |
| g₃* | −0.0050 | C²-related (dimensionless) |

### Critical Exponents (Eq. 13)

| Exponent | Value | Direction |
|----------|-------|-----------|
| θ₀ | 2.51 | UV-attractive |
| θ₁ | 1.69 | UV-attractive |
| θ₂ | 8.40 | UV-attractive |
| θ₃ | −2.11 | UV-repulsive |

Universal product: (GΛ)* = 0.427, consistent with f(R) results.

### Critical Finding
**The higher-derivative couplings g₂* and g₃* are FINITE and NON-ZERO at the NGFP.** This contrasts with perturbative asymptotic freedom where these couplings vanish. The C²-related coupling g₃* = −0.0050 does not flow to zero. Therefore:
- The Becker-Ripken-Saueressig mass-divergence mechanism (where ghost mass → ∞ because the higher-derivative coupling → 0) **cannot operate for the spin-2 ghost**
- The ghost mass remains finite at the NGFP: m₂ ~ O(M_P)

---

## Section 2: Pole Structure from Draper et al. 2020

### Source
Draper, Knorr, Ripken, Saueressig — "Finite Quantum Gravity Amplitudes: No Strings Attached" (PRL 125, 181301; arXiv:2007.00733)

### Graviton Propagator Form
The flat-space propagator decomposes into spin-2 and spin-0 projectors:

    G(p²) ∝ Π^TT × [1/(p²(1 + p²f_C(p²)))] − 2Π⁰ × [1/(p²(1 + p²f_R(p²)))]

where f_C(p²) and f_R(p²) are momentum-dependent form factors encoding all quantum corrections.

### Form Factor Parametrization
The authors use a hyperbolic tangent form extracted from FRG data:

    f_{R,C}(Δ) = c_{R,C} · G_N · tanh(c_{R,C} · G_N · Δ)

where c_R, c_C > 0 are dimensionless parameters. Equivalently, defining Λ_{R,C}² = 1/(c_{R,C} G_N):

    f_{R,C}(p²) = (1/Λ_{R,C}²) · tanh(p²/Λ_{R,C}²)

### Pole Positions — Complex Conjugate Towers
Setting 1 + p²f_C(p²) = 0 yields poles at **purely imaginary p²**:

    p²_n = ±(iπn/c_C) · M²_Pl,    n = 1, 2, 3, ...    (spin-2 sector)
    p²_n = ±(iπn/c_R) · M²_Pl,    n = 1, 2, 3, ...    (spin-0 sector)

Properties:
- **Infinite towers** with Regge-type spacing Δ(p²) = πM²_Pl/c_{R,C}
- **Complex conjugate pairs** at imaginary p² → do NOT contribute to absorptive part of amplitudes
- **No real poles** except p² = 0 (massless graviton)
- Reminiscent of Lee-Wick construction

### Partial Wave Results
For φφ→χχ scattering:

    a₀(s) = (G_N/12) s² G_R(s)  →  lim(s→∞) = 1/(12c_R)
    a₂(s) = −(G_N/60) s² G_C(s)  →  lim(s→∞) = −1/(60c_C)

All higher partial waves vanish. Amplitudes saturate **finite bounds** at trans-Planckian energy. Unitarity bounds require c_R > 1/12, c_C > 1/60.

### Key Limitation
This computation was done in the **Einstein-Hilbert truncation** with form factors. The C² term was not included in the effective action — the spin-2 ghost sector was modeled by the form factor f_C, not derived from an explicit C² computation in the FRG. The tanh form is an ansatz motivated by FRG data, not a first-principles result for the ghost sector specifically.

---

## Section 3: Ghost Mass and Critical Scale Derivation

### Ghost Mass Formula
From the Stelle action linearized around flat space, the spin-2 TT propagator is:

    G_TT(p²) = 1/(u₁ p² + u₃ p⁴) = 1/(u₃ p²(p² + m₂²))

where the ghost mass squared is:

    m₂² = u₁/u₃

In standard conventions (Salvio 2018; Bonanno et al. 2025):

    m₂² = M̄_P²/(4α)    [reduced Planck mass M̄_P = 1/√(8πG)]

or equivalently:

    m₂² = f₂² M̄_P²/2    [where f₂² = 1/(2α) is the dimensionless Weyl coupling]

### Ghost Mass at the NGFP — Key Numerical Result

At the NGFP, using Benedetti et al. values:

    m₂²/k² = g₁*/g₃* = (−0.0101)/(−0.0050) = **2.02**

Therefore:

    **m₂/k ≈ √2.02 ≈ 1.42 at the NGFP**

This means the ghost mass is approximately **1.4 times the RG cutoff scale** at the fixed point. The ghost mass is comparable to the Planck mass — it is neither parametrically large nor parametrically small.

### Physical Ghost Mass
The physical ghost mass depends on the RG trajectory (which trajectory connects the NGFP to the IR). The NGFP ratio m₂/k ≈ 1.42 sets the UV boundary condition. The physical mass is:

    m₂^phys ≈ O(1) × M̄_P ≈ 0.5–2 × 10¹⁸ GeV

The range reflects uncertainty in the trajectory choice and truncation effects (critical exponents shift the fixed-point values by O(1) factors across different truncation orders).

### Critical BH Instability Scale
From Lü, Perkins, Pope, Stelle (2015, PRL 114, 171601): the Schwarzschild and non-Schwarzschild black hole branches cross at:

    r_H^cross ≈ 0.876/m₂

Using m₂ ≈ 1.4 M_P:

    r_H^cross ≈ 0.876/(1.4 M_P) ≈ **0.63 l_P**

This is **sub-Planckian**. The ghost-driven instability only triggers for black holes smaller than the Planck length, deep in the non-perturbative regime. This is consistent: the ghost's effects are hidden below the Planck scale, where the non-perturbative completion (AS) takes over.

---

## Section 4: The Predicted Form of Ghost Dissolution

### Why Mass Divergence Is Ruled Out for Spin-2
Becker, Ripken, Saueressig (2017, arXiv:1709.09098) showed that for scalar fields with higher-derivative couplings:
- At NGFP₀ (y* = 0): ghost mass μ² = k²/y → ∞ (ghost decouples for all k)
- This works because the scalar higher-derivative coupling flows to y* = 0 exactly

For the gravitational spin-2 ghost, the C²-related coupling flows to g₃* = −0.0050 ≠ 0. The coupling does NOT vanish at the NGFP. Therefore:

**The mass-divergence mechanism is structurally excluded for the spin-2 ghost.** The ghost mass stays finite. Something else must happen.

### Why Residue Vanishing Is Unlikely
The Platania-Wetterich (2020) "fictitious ghost" mechanism proposes that ghost residues vanish as truncation order increases. However:
- No one has demonstrated this for the Stelle ghost across multiple truncation orders
- The Benedetti et al. result (ghost coupling remains finite at NGFP) works against residue vanishing — if the coupling doesn't flow to zero, the residue has no reason to vanish
- Assessment: **possible but undemonstrated**, no quantitative support

### The Predicted Mechanism: Complex Pole Tower (Draper et al.)

The unified framework predicts that the spin-2 ghost pole **dissolves into complex conjugate pole pairs** at imaginary p², via the same mechanism found by Draper et al. (2020) in the Einstein-Hilbert sector.

**Specific mathematical form of the predicted propagator:**

In the spin-2 TT sector, the full non-perturbative propagator takes the form:

    G_TT(p²) = 1/(p²(1 + p² f_C(p²)))

where f_C(p²) is the Weyl-squared form factor that interpolates between:

**IR limit (p² << m₂²):**

    f_C(p²) → 1/m₂² = const

This recovers the Stelle propagator with ghost pole at p² = −m₂²:

    G_TT → 1/p² − 1/(p² + m₂²)

**UV limit (p² >> m₂²):**

    f_C(p²) → (1/Λ_C²) tanh(p²/Λ_C²)

where Λ_C² = m₂²/c_C for some O(1) dimensionless constant c_C. This gives the complex pole tower:

    poles at p² = ±iπn Λ_C²,    n = 1, 2, 3, ...

**Transition region (p² ~ m₂²):**

The single real ghost pole at p² = −m₂² **splits into a pair of complex conjugate poles** that migrate to imaginary p². As p² increases through the transition, more conjugate pairs appear, building up the infinite tower.

### Predicted Pole Migration Pattern

    p² << m₂²:  Single real pole at p² = −m₂²
    p² ~ m₂²:   Pole splits: p² = −m₂² ± iΓ₁, with Γ₁ growing
    p² ~ few × m₂²:  Multiple conjugate pairs emerge
    p² >> m₂²:  Infinite tower at p² = ±iπn M²_Pl/c_C

The transition scale is:

    **p²_transition ≈ m₂² ≈ 2 M̄_P² ≈ (1.7 × 10¹⁸ GeV)²**

(using m₂/k ≈ 1.42 from the NGFP values and k ~ M_P at the transition).

---

## Section 5: Computational Specification

### The Proposed Computation

**Compute** the transverse-traceless spin-2 sector of the graviton propagator using the functional renormalization group (FRG) in the **(R + R² + C²) truncation**, with momentum-dependent form factors following the methodology of Knorr & Saueressig (2022, SciPost Phys. 12, 001).

Specifically:
1. Start from the effective average action Γₖ including R, R², and C² terms with momentum-dependent form factors f_R(p²,k) and f_C(p²,k)
2. Derive the Wetterstein equation projected onto the spin-2 TT sector
3. Extract the anomalous dimension η_TT(p²) and the running form factor f_C(p²,k)
4. Reconstruct the Lorentzian propagator via Padé approximants (or another spectral reconstruction)
5. Identify the pole structure of G_TT(p²)

### Parameters from existing FRG data

From Knorr-Saueressig (2022):
- Fluctuation graviton anomalous dimension: η_h ≈ 1.03
- Z_h^UV = 0.64
- g* = 570π/833 ≈ 2.15
- Spectral function: positive (dynamical graviton)

From Benedetti et al. (2009):
- g₁* = −0.0101 (Newton coupling)
- g₃* = −0.0050 (C² coupling)
- m₂²/k² = g₁*/g₃* = 2.02 at NGFP

### What the unified framework predicts

**Prediction:** The spin-2 TT propagator in the C²-extended truncation will exhibit:

1. A massless graviton pole at p² = 0 (retained, positive residue)
2. NO real ghost pole at p² = −m₂² (the perturbative ghost pole dissolves)
3. An infinite tower of complex conjugate poles at imaginary p², with spacing ~ πm₂²/c_C
4. The dynamical spin-2 spectral function remains positive for real timelike momenta
5. Scattering amplitudes computed from this propagator satisfy unitarity bounds

### What the null hypothesis (compatible-but-separate) predicts

**Null prediction:** The C²-extended FRG propagator either:
(a) Shows the ghost pole persisting as a real pole at p² = −m₂² with finite negative residue, requiring the fakeon prescription as an **additional principle** imposed by hand, OR
(b) Shows ghost dissolution, but through a mechanism that is **generic to AS** (not specific to the unified picture) — in which case the fakeon prescription is an unnecessary complication

### The discrimination criterion

**If** the pole structure of the C²-extended FRG propagator reproduces the scattering amplitudes that the fakeon prescription yields at tree level (ghost-pole averaging ↔ complex-pole-tower summation), this would constitute evidence for unification.

**If** the pole structure contradicts the fakeon amplitudes, the frameworks are incompatible.

**If** the ghost simply isn't there (fictitious ghost), neither framework makes the wrong prediction but the fakeon prescription is superfluous.

---

## Section 6: Classification of the Prediction

### DISCRIMINATING: Partially Yes

The prediction discriminates between unified and compatible-but-separate IF the null hypothesis predicts a persistent real ghost pole. The key test:

| Outcome | Unified interpretation | Separate interpretation |
|---------|----------------------|----------------------|
| Complex pole tower | Confirmed — fakeon emerges dynamically | Unexpected but not fatal |
| Real ghost pole | Refuted | Confirmed — fakeon needed by hand |
| No ghost at all | Consistent (fictitious ghost) | Consistent (truncation artifact) |
| Residue vanishing | Partially consistent | Partially consistent |

The complex pole tower outcome is the ONLY one that clearly favors unification. All other outcomes are ambiguous.

### NOVEL: Yes

Neither QG+F alone nor AS alone predicts the complex pole tower in the C² sector:
- QG+F provides only the perturbative ghost pole + fakeon prescription (no non-perturbative statement)
- AS in Einstein-Hilbert truncation has no ghost pole at all (C² absent from truncation)
- The combined prediction (ghost pole → complex tower) requires BOTH the C² coupling at the NGFP (from AS) AND the fakeon interpretation (from QG+F)

### Numerical Specificity

| Quantity | Value | Source | Precision |
|----------|-------|--------|-----------|
| m₂/k at NGFP | √2.02 ≈ 1.42 | Benedetti et al. g₁*/g₃* | Order-of-magnitude (truncation-dependent) |
| Physical m₂ | ~0.5–2 M̄_P | NGFP + trajectory | Factor of ~4 uncertainty |
| r_H instability | ~0.63 l_P | m₂ + Lü et al. crossing | Sub-Planckian |
| Pole spacing | ~πm₂²/c_C | Draper et al. formula | c_C unknown (O(1)) |
| η_h at NGFP | 1.03 | Knorr-Saueressig (EH) | Will shift in C² truncation |
| g* (Newton) | 570π/833 ≈ 2.15 | Knorr-Saueressig (EH) | Will shift in C² truncation |

---

## Section 7: Honest Assessment — Can This Be Sharpened?

### What blocks a sharper prediction?

**Three unknowns prevent a fully quantitative prediction:**

1. **The dimensionless parameter c_C.** This controls the pole spacing and the high-energy behavior of the amplitude. In the Draper et al. construction, c_C is a free parameter (constrained only by unitarity: c_C > 1/60). A first-principles FRG computation of the C²-extended form factor would determine c_C.

2. **The RG trajectory.** The physical ghost mass m₂ depends on which UV-to-IR trajectory is chosen. The NGFP fixes only the ratio m₂/k at the fixed point (≈ 1.42), not the physical mass. The trajectory is specified by fixing initial conditions at some scale — analogous to fixing Λ_QCD in QCD.

3. **The form factor functional form.** The tanh is an ansatz. The actual FRG computation might yield a different functional form that still produces complex poles but with different positions and residues.

### Is the ghost propagator prediction actually discriminating?

**Partially, with an important caveat.**

The caveat: the complex pole tower might emerge from AS dynamics **regardless** of whether the unified picture is correct. AS is a non-perturbative completion that naturally generates momentum-dependent form factors. These form factors could produce complex poles simply because that's what non-perturbative quantum gravity does, with no reference to fakeons.

The discriminating content is NOT "does the ghost dissolve?" but rather **"does the ghost dissolve IN A WAY CONSISTENT WITH THE FAKEON PRESCRIPTION?"** Specifically:
- Do the scattering amplitudes from the complex pole tower equal the amplitudes from ghost-pole averaging (fakeon)?
- If yes → the fakeon is the perturbative shadow of AS dynamics → unification confirmed
- If no → the frameworks are dynamically incompatible → unification refuted

This is a much harder computation than simply checking for complex poles. It requires computing scattering amplitudes from the non-perturbative propagator and comparing with fakeon-prescription amplitudes at tree level.

### The structural reason the prediction cannot be fully sharpened

The unified framework currently provides:
- A mechanism (complex pole tower) ✓
- A scale (m₂ ~ M_P) ✓
- A qualitative form (tanh-like form factor) ~
- A specific numerical prediction for the amplitude equivalence ✗

The final item requires the actual FRG computation in the C²-extended truncation — which has never been done. The prediction is: "When you do this computation, here's what you'll find." But the prediction is not sharp enough to distinguish it from "any reasonable non-perturbative completion."

### Assessment of the prediction's value

**Honest verdict: This is a well-specified consistency check, not a sharp discriminating prediction.**

It can REFUTE unification (if the ghost persists as a real pole, or if the amplitudes disagree) but it cannot UNIQUELY CONFIRM it (complex poles could emerge for non-unified reasons). This is still valuable — refutability is the hallmark of a scientific prediction. But it's weaker than "measure X and the unified framework predicts Y ± Z while the alternative predicts W ± V."

The single sharpest claim is the **amplitude equivalence test**: fakeon amplitudes = complex-pole-tower amplitudes. If this fails, unification is refuted. If it succeeds, unification gains significant support (because there's no a priori reason for the equivalence to hold in the separate picture).

---

## Summary of Deliverables

### 1. Predicted Form of Ghost Dissolution
**Complex pole tower** (Draper et al. mechanism). The perturbative ghost pole at p² = −m₂² splits into complex conjugate pairs at imaginary p². Mathematical form:

    G_TT(p²) = 1/(p²(1 + p² f_C(p²)))
    f_C(p²) = (1/Λ_C²) tanh(p²/Λ_C²)
    Poles at p² = ±iπn Λ_C², n = 1, 2, 3, ...

### 2. Critical Scale
Ghost mass at the NGFP: **m₂ ≈ √2 × k ≈ 1.42k** (from g₁*/g₃* = 2.02, Benedetti et al. 2009).
Physical ghost mass: **m₂ ~ 0.5–2 M̄_P ≈ 0.6–2.4 × 10¹⁸ GeV**.
BH instability threshold: **r_H ≈ 0.876/m₂ ≈ 0.6 l_P** (sub-Planckian).

### 3. Computational Specification
Compute the spin-2 TT graviton propagator using FRG in the (R + R² + C²) truncation with momentum-dependent form factors. The unified framework predicts complex conjugate pole tower replacing the ghost; the null hypothesis predicts persistent real ghost pole requiring external fakeon prescription.

### 4. Classification
- **DISCRIMINATING:** Partially — can refute but not uniquely confirm unification.
- **NOVEL:** Yes — neither framework alone predicts the C²-sector pole tower.
- **Numerical specificity:** m₂/k ≈ 1.42 at NGFP; physical m₂ uncertain by factor ~4.

---

## Sources

- Benedetti, Machado, Saueressig (2009), arXiv:0901.2984 — NGFP fixed-point values
- Draper, Knorr, Ripken, Saueressig (2020), PRL 125, 181301 — complex pole tower
- Knorr & Saueressig (2022), SciPost Phys. 12, 001 — propagator reconstruction methodology
- Becker, Ripken, Saueressig (2017), JHEP 12, 121 — scalar ghost mass divergence (NOT spin-2)
- Platania & Wetterich (2020), arXiv:2009.06637 — fictitious ghost framework
- Holdom & Ren (2016), arXiv:1605.05006 — ghost propagator scenarios A & B
- Lü, Perkins, Pope, Stelle (2015), PRL 114, 171601 — BH crossing at r_H ≈ 0.876/m₂
- Knorr, Ripken, Saueressig (2021), arXiv:2111.12365 — form factor approach to ghost
- Bonanno et al. (2025), arXiv:2505.05027 — ghost-induced BH phase transition
- Falls, Kluth, Litim (2023), PRD 108, 026005 — UV critical surface dimensionality
- Salvio (2018), Front. Phys. 6, 77 — quadratic gravity review
