# Exploration 002: Black Hole Evaporation Phase Transition — Quantitative Predictions

## Goal
Derive specific quantitative predictions from the BH evaporation phase transition in the unified QG+F–AS framework. For each prediction, classify as DISCRIMINATING / NOVEL / CONSISTENCY CHECK / INHERITED.

## Status: IN PROGRESS

---

## 1. Critical Transition Mass M_crit

### Derivation

Three inputs combine to fix M_crit:

1. **Bonanno et al. 2025 instability threshold:** The Schwarzschild solution becomes linearly unstable in quadratic gravity when r_H ≈ 0.876/m₂, where m₂ is the massive spin-2 ghost mass.

2. **Ghost mass at NGFP (Exploration 001):** From Benedetti et al. (2009) fixed-point values g₁* = −0.0101, g₃* = −0.0050:
   - m₂/k = √(|g₁*/g₃*|) = √(0.0101/0.0050) = √2.02 ≈ **1.42**
   - At k ~ M_P (the scale where NGFP physics dominates): **m₂ ≈ 1.42 M_P**

3. **Schwarzschild relation:** r_H = 2GM = 2M/M_P² (in natural units ℏ = c = 1, G = 1/M_P²)

**Calculation:**

Setting r_H = 0.876/m₂:

```
2M_crit/M_P² = 0.876/(1.42 M_P)

M_crit = (0.876 × M_P²) / (2 × 1.42 × M_P)
       = 0.876 / (2 × 1.42) × M_P
       = 0.308 M_P
```

### Result

| Quantity | Value |
|---|---|
| M_crit | **0.308 M_P** |
| M_crit (kg) | **6.70 × 10⁻⁹ kg** |
| M_crit (GeV) | **3.76 × 10¹⁸ GeV** |
| r_H at transition | **0.617 l_P** |

### Convention Note
The factor 1.42 comes from NGFP dimensionless couplings. Whether m₂ = 1.42 M_P (standard Planck mass) or 1.42 M̄_P (reduced Planck mass, smaller by √(8π) ≈ 5.01) depends on the convention in Benedetti et al.'s coupling definitions. The GOAL document states "m₂ ~ 0.5–2 M̄_P," suggesting the reduced convention. If m₂ = 1.42 M̄_P = 0.283 M_P, then M_crit = 0.876/(2 × 0.283) M_P = 1.55 M_P. The calculation is sensitive to this convention choice — this is a **significant systematic uncertainty**.

| Convention | m₂ | M_crit | r_H,crit |
|---|---|---|---|
| m₂ = 1.42 M_P | 1.74 × 10¹⁹ GeV | 0.308 M_P = 6.7 × 10⁻⁹ kg | 0.617 l_P |
| m₂ = 1.42 M̄_P | 3.46 × 10¹⁸ GeV | 1.55 M_P = 3.4 × 10⁻⁸ kg | 3.09 l_P |

I proceed with both values but highlight the m₂ = 1.42 M_P convention as the baseline.

### Classification: **NOVEL**
Neither QG+F alone nor AS alone predicts this specific transition mass. QG+F gives the instability criterion (r_H ≈ 0.876/m₂) but leaves m₂ as a free parameter. AS provides the fixed-point value m₂/k = 1.42. Only the unified framework combines both to predict M_crit.

---

## 2. Hawking Temperature at Transition

### Derivation

Standard Hawking temperature: T_H = M_P²/(8πM)

At M = M_crit = 0.308 M_P:

```
T_crit = M_P² / (8π × 0.308 × M_P)
       = M_P / (8π × 0.308)
       = M_P / 7.73
       = 0.129 M_P
```

### Result

| Quantity | Value |
|---|---|
| T_crit | **0.129 M_P** |
| T_crit (GeV) | **1.58 × 10¹⁸ GeV** |
| T_crit (K) | **1.83 × 10³¹ K** |

For the reduced Planck mass convention (M_crit = 1.55 M_P):
- T_crit = M_P/(8π × 1.55) = M_P/38.9 = 0.0257 M_P = 3.14 × 10¹⁷ GeV = 3.64 × 10³⁰ K

### Comparison with QCD

| Property | QCD deconfinement | BH evaporation transition |
|---|---|---|
| T_c | 156.5 ± 1.5 MeV | 0.03–0.13 M_P (convention-dependent) |
| T_c/Λ_theory | T_c/Λ_QCD ≈ 0.5–0.7 | T_crit/M_P ≈ 0.03–0.13 |
| Ratio to fundamental scale | O(1) | O(0.1) |

The ratio T_crit/M_P ~ 0.03–0.13 is comparable to T_c/Λ_QCD ~ 0.5–0.7 in order-of-magnitude terms. Both transitions occur at temperatures parametrically close to but somewhat below the fundamental scale.

### Classification: **NOVEL**
Same reasoning as M_crit — requires both frameworks.

---

## 3. Order of the Transition

### QCD Deconfinement: The Template

From lattice QCD (web search results):

**Pure SU(3) gauge theory (N_f = 0):**
- **First-order** transition at T_c ≈ 270 MeV
- Latent heat: h = Δs/T_c³ = 1.175(10) (arXiv:2502.03875, 2025)
- Order parameter: Polyakov loop ⟨L⟩ — discontinuous jump from 0 (confined, Z(3) symmetric) to finite (deconfined, Z(3) broken)
- Entropy density discontinuity: s(T_c⁻)/T_c³ = 0.293, s(T_c⁺)/T_c³ = 1.471

**Physical quarks (N_f = 2+1, physical masses):**
- **Analytic crossover** at T_c = 156.5 ± 1.5 MeV (HotQCD 2019, arXiv:1812.08235)
- No latent heat, no discontinuity, smooth but rapid change over ~10–20 MeV window
- Quarks **explicitly break** Z(3) center symmetry → Polyakov loop is nonzero even below T_c → transition smoothed to crossover

**At high baryon density:**
- First-order line terminated by critical endpoint at T_c = 114 ± 7 MeV, μ_B = 602 ± 62 MeV (arXiv:2410.16206, 2024)

**What determines the order:**
- Pure gauge (no quarks): first-order (Z(3) is an exact symmetry, spontaneously broken)
- Adding quark flavors: quarks **explicitly break** Z(3) → transition weakened
- Enough quarks at light masses: transition becomes crossover (physical QCD)
- Key parameter: number and masses of dynamical fermions

### Mapping to Gravity

**The gravitational "quark flavors" are matter fields.** In QCD, dynamical quarks couple to the gauge field and explicitly break Z(3) center symmetry, converting the first-order deconfinement transition into a crossover. In gravity, matter fields (scalars, fermions, gauge bosons of the Standard Model) couple to the metric and could play an analogous role.

**Pure gravity → pure gauge analogy:**
- CDT (Causal Dynamical Triangulations) provides lattice evidence for pure gravity:
  - Phase A (crumpled) ↔ Phase C (physical/de Sitter): **first-order** transition
  - Phase B (branched polymer) ↔ Phase C: second-order transition
- The A–C transition is most relevant: Phase A has strong gravitational fluctuations (many simplices at few vertices), analogous to the confined/strong-coupling phase
- **CDT confirms: pure gravity transition is first-order**, consistent with pure gauge QCD analogy

**Gravity + Standard Model matter → physical QCD analogy:**
- The SM has ~100 degrees of freedom (12 gauge bosons, 45 Weyl fermions, 4 Higgs DOF)
- By analogy with QCD, this many matter fields could explicitly break whatever gravitational "center symmetry" exists, converting the first-order transition to a crossover
- However: the gravitational center symmetry analog is unclear. The most natural candidate is the **thermal holonomy** — the gravitational connection integrated around the Euclidean thermal circle — but this is not well-studied

**Gravitational Polyakov loop analog:**
- In QCD: ⟨L⟩ = ⟨Tr P exp(i∮ A₀ dτ)⟩ measures free energy of static quark
- In gravity: the analog would be ⟨P exp(∮ Γ dτ)⟩ around the thermal circle, related to the conical deficit at the horizon
- For a Schwarzschild BH at the correct Hawking temperature, the Euclidean section is smooth (no conical defect) — this is the "ordered" phase
- At T ≠ T_H, there IS a conical defect — this signals the "disordered" phase
- The transition between smooth and singular Euclidean geometry could be the gravitational analog of the Polyakov loop phase transition

### Assessment: Where the Analogy Breaks

The QCD deconfinement analogy works qualitatively:
- ✅ Pure gauge → pure gravity: first-order (CDT confirms)
- ✅ Adding flavors → adding matter: softens transition
- ✅ Order parameter exists (thermal holonomy / conical structure)

But it fails quantitatively:
- ❌ In QCD, the crossover is at a LOWER temperature than the pure-gauge transition. In gravity, we don't know if matter lowers or raises M_crit.
- ❌ The gravitational "center symmetry" is not a discrete symmetry like Z(3). Diffeomorphism invariance is continuous and unbroken. The analogy is structural, not mathematical.
- ❌ The "number of flavors" threshold for crossover behavior is unknown for gravity.

### Prediction

**Most likely: first-order for pure gravity, crossover for gravity + SM matter.**

If first-order (pure gravity):
- Latent heat by dimensional analysis: L ~ h × T_crit⁴ where h ~ O(1) by QCD analogy
- L ~ (0.129 M_P)⁴ × O(1) = 2.8 × 10⁻⁴ M_P⁴ per Planck volume
- Total latent heat per BH: Q ~ L × V_transition ~ L × r_H³ ~ 2.8 × 10⁻⁴ × (0.617)³ × M_P = 6.6 × 10⁻⁵ M_P ≈ 8 × 10⁻¹⁴ kg c² ≈ 7 × 10³ J
- This is tiny: ~10⁻⁵ of the BH's rest mass energy at transition

If crossover (gravity + SM):
- No latent heat
- Transition occurs over a mass window ΔM/M_crit ~ O(0.1), analogous to the ~10 MeV width of the QCD crossover (ΔT/T_c ~ 0.1)
- ΔM ~ 0.03 M_P

### Classification: **NOVEL** (three-phase picture and trigger mechanism are new; order depends on matter content — a testable prediction within the framework)

---

## 4. Remnant Mass and Temperature

### AS Remnant (Bonanno-Reuter)

The RG-improved Schwarzschild metric has two horizons that merge at a critical mass:

- M_rem ~ 10⁻⁵ g ≈ 10⁻⁸ kg ≈ **0.46 M_P** (from Bonanno-Reuter 2000)
- This depends on the AS fixed-point coupling g*:
  - g* ≈ 0.1–1.2 (across truncations)
  - Bonanno et al. 2024 uses g* = 540π/833 ≈ 2.04
  - Larger g* → smaller M_rem (roughly M_rem ∝ g*^{-1/2})

### Critical Consistency Check: M_rem vs M_crit

**Key finding:** M_rem > M_crit (for the m₂ = 1.42 M_P convention).

| Quantity | m₂ = 1.42 M_P | m₂ = 1.42 M̄_P |
|---|---|---|
| M_crit | 0.308 M_P | 1.55 M_P |
| M_rem (Bonanno-Reuter) | ~0.46 M_P | ~0.46 M_P |
| Ordering | M_rem > M_crit ✅ | M_crit > M_rem ⚠️ |

**For m₂ = 1.42 M_P:** M_rem > M_crit. The AS remnant forms (horizons merge, T → 0) BEFORE the perturbative Schwarzschild instability is reached. This means:
- The ghost confinement instability is **preempted** by the AS transition
- The transition is driven by AS effects (running G(k), de Sitter core formation), not by the perturbative instability
- This is analogous to QCD: confinement sets in before the perturbative Landau pole is reached

**For m₂ = 1.42 M̄_P:** M_crit > M_rem. The Schwarzschild instability triggers first, at M_crit = 1.55 M_P, driving the BH into the non-perturbative regime where it eventually settles to the AS remnant at M_rem ≈ 0.46 M_P. This is the scenario where the ghost confinement trigger is active and operative.

**This convention dependence is the single largest systematic uncertainty in the framework's BH predictions.**

### Sharpening M_rem Under Unification

Under the unified framework, M_rem should depend on BOTH g* (AS) and m₂ (QG+F). At the NGFP, these are related:
- g* encodes the gravitational fixed-point coupling: G(k) = g*/k²
- m₂/k = √(|g₁*/g₃*|) = 1.42 encodes the ghost mass ratio

If we identify k = M_P and use the Bonanno-Reuter remnant formula with the running m₂:
- The de Sitter core forms when the running G(r) ~ g*/r² becomes strong enough to resolve the singularity
- The ghost mass at this scale is m₂(k ~ 1/r_core) ≈ 1.42 × (1/r_core)
- Self-consistency: r_core ~ √(g*) l_P, so m₂(r_core) ~ 1.42/(√(g*) l_P) = 1.42 M_P/√(g*)

For g* = 2.04: m₂(r_core) ≈ M_P, and r_core ≈ 1.43 l_P.
For g* = 0.5: m₂(r_core) ≈ 2.0 M_P, and r_core ≈ 0.71 l_P.

The remnant mass under unification:
- **M_rem = M_rem(g*, m₂/k) where m₂/k = 1.42 is fixed by the NGFP**
- This removes one parameter: instead of (g*, m₂) independently, we have (g*, 1.42)
- Concretely: M_rem ≈ 0.3–0.7 M_P with reduced spread compared to AS alone

### Remnant Temperature

T → 0 as M → M_rem. The approach is governed by the near-extremal geometry:
- Bonanno-Reuter metric near the remnant resembles extremal Reissner-Nordström
- For extremal RN: T = 0 exactly (zero surface gravity)
- For near-extremal: T ~ (M - M_rem)^{1/2}

**The remnant temperature is exactly T = 0 in the extremal limit.** The remnant is thermodynamically stable — it has zero temperature and zero entropy flux.

Correction: the remnant entropy is NOT zero. Using the Bekenstein-Hawking formula:
- S_rem = A/(4G) = 4π r_rem²/(4G) = π r_rem² M_P²
- r_rem ~ l_P, so S_rem ~ π ≈ 3

So the remnant has O(1) entropy in Planck units — a quantum gravitational object with a few bits of information.

### Classification

- M_rem: **INHERITED** from AS (slightly sharpened by unified constraint m₂/k = 1.42)
- T → 0: **INHERITED** from AS
- M_rem(g*, 1.42) constraint: **CONSISTENCY CHECK** (reduces parameter space but doesn't predict new value)

---

## 5. Heat Capacity Signature

### Standard BH Heat Capacity

```
T_H = M_P² / (8πM)
C = dM/dT = 1/(dT/dM) = -8πM²/M_P²
```

At M = M_crit = 0.308 M_P: C = -8π(0.308)² = **−2.39** (in Planck units)

### Through the Transition

The Bonanno-Reuter temperature profile has a **maximum** at some M = M_max:
- For M > M_max: T increases as M decreases (standard BH), C < 0
- At M = M_max: dT/dM = 0, |C| → ∞ (heat capacity divergence)
- For M_rem < M < M_max: T decreases as M decreases, C > 0
- At M = M_rem: T → 0, and C → 0⁺ (via T ~ (M − M_rem)^{1/2})

The heat capacity follows:
```
C(M) = { -8πM²/M_P²                     for M >> M_P  (Phase I)
        { diverges at M = M_max           (transition)
        { positive, approaching 0          for M → M_rem (Phase II)
```

The maximum temperature is:
- T_max ~ O(0.1–0.3) M_P (model-dependent)
- At T_max, the BH transitions from thermodynamically unstable (C < 0) to stable (C > 0)

### Observational Signature

The heat capacity divergence produces a characteristic feature in the Hawking radiation spectrum: a **burst** of radiation as the BH passes through T_max, followed by a rapid cooling toward T → 0. This is qualitatively different from the standard picture (T → ∞ as M → 0, explosive final burst).

| Scenario | Final stage of evaporation |
|---|---|
| Standard GR (no remnant) | T → ∞, explosive burst, complete evaporation |
| AS alone | T → T_max then T → 0, cooling to remnant |
| Unified QG+F–AS | Same as AS, but with specific T_max fixed by m₂ and g* |

### Classification: **INHERITED** from AS
The heat capacity sign change and divergence are predicted by AS alone. The unified framework adds only the specific numerical value of T_max (via the m₂ constraint), which is a modest sharpening, not a new prediction.

---

## 6. PBH Dark Matter Predictions

### Which PBHs Produce Remnants?

Standard Hawking evaporation time: τ = 5120π G²M³/(ℏc⁴) = 5120π (M/M_P)³ t_P

A BH evaporates in the age of the universe (t_U ≈ 4.35 × 10¹⁷ s) if:

```
M ≤ M* where (M*/M_P)³ = t_U / (5120π t_P)
= 8.07 × 10⁶⁰ / 16085
= 5.02 × 10⁵⁶

M*/M_P ≈ 3.68 × 10¹⁸
M* ≈ 8.0 × 10¹⁰ kg (without species factor)
M* ≈ 5 × 10¹¹ kg (with ~100 SM species)
```

**All PBHs with M_init ≲ 5 × 10¹¹ kg (≈ 5 × 10¹⁴ g ≈ 2.3 × 10¹⁹ M_P) have evaporated by now.** In the unified framework, each leaves a Planck-mass remnant.

### Remnant Abundance

Mass conversion factor: M_rem/M_init ~ M_P / (5 × 10¹¹ kg) ~ 4 × 10⁻²⁰

The remnant mass density today:
```
ρ_rem = n_PBH,evaporated × M_rem
```

For PBH remnants to constitute ALL of dark matter (ρ_DM ≈ 2.5 × 10⁻²⁷ kg/m³):
```
n_rem = ρ_DM / M_rem ≈ 2.5 × 10⁻²⁷ / (2 × 10⁻⁸) ≈ 1.2 × 10⁻¹⁹ m⁻³
```

This requires an initial PBH number density (at formation, diluted by expansion) that translates to an initial mass fraction β:
```
β(M*) ~ 10⁻¹⁸ (order of magnitude, for M_init ~ M* ~ 5 × 10¹¹ kg)
```

### Observational Constraints on β

| Mass range | Constraint | Source |
|---|---|---|
| M ~ 10⁹–10¹¹ kg | β < 10⁻²⁵ to 10⁻²⁸ | Extragalactic γ-ray background |
| M ~ 10⁹–10¹³ kg | β < 10⁻²⁰ to 10⁻²⁴ | BBN light element abundances |
| M ~ 10⁶–10¹³ kg | β < 10⁻²⁰ | CMB spectral distortions |

**Conclusion:** For the mass range M ~ 10⁹–10¹¹ kg (the ones evaporating today), the γ-ray constraints (β < 10⁻²⁵) are MUCH tighter than what's needed for all-DM (β ~ 10⁻¹⁸). So:

**PBH remnants cannot be ALL of dark matter** if the PBHs formed with M_init ~ M*. The γ-ray constraints on evaporating PBHs are too stringent.

However, very light PBHs (M_init ~ 10⁴–10⁶ g = 10–1000 kg) that evaporated very early (within seconds of the Big Bang) have weaker constraints and could potentially contribute a significant DM fraction. But these form at extremely high temperatures (T_form > 10¹² GeV) and require non-standard formation mechanisms.

### Remnant Properties as DM Candidate

| Property | Value | Implication |
|---|---|---|
| Mass | ~M_P ≈ 2 × 10⁻⁸ kg | Ultra-heavy DM (10¹⁹ GeV) |
| Charge | 0 (Schwarzschild origin) | No electromagnetic interaction |
| Spin | Unknown (could retain angular momentum) | Potentially detectable via frame-dragging |
| Cross-section | σ ~ l_P² ~ 10⁻⁷⁰ m² | Essentially undetectable directly |
| Temperature | T = 0 | No Hawking radiation — dark |

### Classification: **INHERITED** from AS
PBH remnant DM is an AS prediction. The unified framework adds nothing observationally new here — the remnant properties are determined by AS physics.

---

## 7. Observable Signatures

### Summary of Observability

| Prediction | Observable? | Instrument | Timeline |
|---|---|---|---|
| M_crit = 0.31 M_P | No | Would require observing final BH evaporation | Never (no known Planck-mass BHs) |
| T_crit = 0.13 M_P | No | Same as above | Never |
| Transition order | No | Would need Planck-scale BH thermodynamics | Never |
| Remnant existence | Possibly | Gravitational lensing (femtolensing), GW detectors | >2040 |
| Remnant DM | Possibly | Missing mass accounting, gravitational effects | Indirect only |
| Heat capacity divergence | No | Would need to observe transition in real time | Never |
| Final evaporation burst | Possibly | γ-ray telescopes | If PBH evaporation observed |

### Difference from "No Phase Transition" Scenarios

| Scenario | Final evaporation | Endpoint | γ-ray signature |
|---|---|---|---|
| Pure GR (no new physics) | T → ∞, explosive | Complete evaporation | Bright burst, all particle species |
| Pure AS (no ghost trigger) | T → T_max → 0 | Remnant, gradual cooling | Burst at T_max, then fading |
| Unified QG+F–AS | T → T_max → 0 | Remnant, specific T_max | Burst at specific T_max = 0.13 M_P |
| QG+F alone (no AS) | T → ∞ until instability | Unknown (no non-pert. completion) | Unknown |

The unified framework's ONLY observational distinction from pure AS is the **specific value of T_max** (determined by m₂). Since T_max ~ 0.1 M_P ~ 10¹⁸ GeV in either case, this distinction is practically unobservable — it would require resolving Planck-scale temperatures.

---

## 8. Prediction Classification Table

| # | Prediction | Value | Classification | Justification |
|---|---|---|---|---|
| 1 | Critical transition mass | M_crit = 0.31 M_P (6.7 × 10⁻⁹ kg) | **NOVEL** | Requires both instability criterion (QG+F) and m₂ at NGFP (AS) |
| 2 | Transition temperature | T_crit = 0.13 M_P (1.6 × 10¹⁸ GeV) | **NOVEL** | Same — derived from M_crit |
| 3 | Three-phase evaporation | Phase I → transition → Phase II | **NOVEL** | Neither framework alone gives this picture |
| 4 | Transition order (pure gravity) | First-order | **NOVEL** | CDT evidence + QCD analogy (pure gauge ↔ pure gravity) |
| 5 | Transition order (gravity + SM) | Likely crossover | **NOVEL** | QCD analogy (physical quarks → crossover) |
| 6 | Latent heat (if first-order) | Q ~ 10⁻⁵ M_P per BH (~7 kJ) | **NOVEL** | Dimensional analysis + QCD latent heat ratio |
| 7 | Remnant mass | M_rem ≈ 0.3–0.7 M_P | **INHERITED** (AS) | Bonanno-Reuter; unified only narrows range slightly |
| 8 | Remnant temperature | T → 0 (exactly) | **INHERITED** (AS) | Extremal geometry; universal to AS |
| 9 | Heat capacity sign change | C: −∞ → +∞ → 0⁺ | **INHERITED** (AS) | Generic to any remnant scenario |
| 10 | M_rem > M_crit ordering | 0.46 M_P > 0.31 M_P | **CONSISTENCY CHECK** | AS transition preempts perturbative instability |
| 11 | PBH remnant DM | Can't be all DM (γ-ray constraints) | **INHERITED** (AS) | AS prediction; unified adds nothing |
| 12 | Ghost confinement trigger | Schwarzschild instability at r_H < 0.876/m₂ | **DISCRIMINATING** | True ONLY if QG+F and AS are unified; pure AS has no trigger mechanism |

---

## 9. Honest Assessment: What's Genuinely New?

### The Uncomfortable Truth

Most BH evaporation predictions (7 out of 12) are **INHERITED from AS alone**. The unified framework adds:

1. **A trigger mechanism** (ghost confinement instability) — but this may be preempted by the AS transition (if M_rem > M_crit)
2. **Specific numerical values** (M_crit, T_crit) — but these are unobservable
3. **A three-phase narrative** — conceptually elegant but not independently testable

The truly **NOVEL** predictions (#1–6) all involve Planck-scale physics that is completely inaccessible to observation. The truly **DISCRIMINATING** prediction (#12) — that there exists a ghost confinement trigger — is a theoretical statement about the mechanism, not an observable signature.

### Where the QCD Analogy Adds Value

The QCD analogy's primary contribution is predicting the **order of the transition**:
- Pure gravity: first-order (supported by CDT)
- With SM matter: crossover

This is a genuine prediction that AS alone does not make (AS remnant models don't address the order of the transition). But it cannot be tested observationally.

### Where the QCD Analogy Fails

1. **No gravitational Z(3) symmetry.** The center symmetry of SU(3) has no direct gravitational analog. The mapping is structural, not mathematical.
2. **No lattice data for full gravity + matter.** CDT phase transitions are for pure gravity. Adding matter to CDT is technically difficult and not well-explored.
3. **The "flavor" counting is ambiguous.** How many gravitational "flavors" does each SM field count as? This is undefined.
4. **Quantitative latent heat.** The QCD ratio L/T_c⁴ ~ 1.2 cannot be reliably transported to gravity. The dimensional analysis gives L ~ T_c⁴ × O(1), but the O(1) factor is unconstrained.

### Bottom Line

The BH evaporation phase transition in the unified framework is **AS predictions dressed up with a ghost confinement trigger mechanism**. The novelty is real but narrow: it's the trigger mechanism, not the endpoint. The endpoint (remnant, T → 0, C sign change) is entirely AS. The trigger (Schwarzschild instability at r_H = 0.876/m₂) is entirely QG+F. The unified framework combines them into a coherent narrative but generates no new observationally testable prediction beyond what AS alone gives.

The one caveat: if the reduced Planck mass convention is correct (m₂ = 1.42 M̄_P), then M_crit = 1.55 M_P > M_rem ≈ 0.46 M_P, and the ghost confinement instability IS the trigger that drives the transition. In this case, the three-phase picture is not just narrative but causal: the BH hits the instability, which forces it into the non-perturbative regime, which then relaxes to the AS remnant. This is a stronger and more genuinely novel scenario.
