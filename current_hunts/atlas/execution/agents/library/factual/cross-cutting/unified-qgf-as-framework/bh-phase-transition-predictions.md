---
topic: unified-qgf-as-framework
confidence: provisional
date: 2026-03-26
source: exploration-s4-002-bh-phase-transition (quantum-gravity-2 strategy-004)
---

# BH Evaporation Phase Transition: Quantitative Predictions

Detailed quantitative predictions for the black hole evaporation phase transition in the unified QG+F–AS framework. See `novel-predictions.md` #3 for the qualitative picture (three phases, trigger mechanism).

## Critical Transition Mass

Three inputs combine to fix M_crit:

1. **Bonanno et al. 2025 instability threshold:** Schwarzschild becomes linearly unstable at r_H ≈ 0.876/m₂
2. **Ghost mass at NGFP:** m₂/k = √(|g₁*/g₃*|) = √2.02 ≈ 1.42 (Benedetti et al. 2009)
3. **Schwarzschild relation:** r_H = 2GM = 2M/M_P²

Setting r_H = 0.876/m₂ with m₂ = 1.42 M_P:

    M_crit = 0.876/(2 × 1.42) × M_P = **0.308 M_P** (6.70 × 10⁻⁹ kg, 3.76 × 10¹⁸ GeV)
    r_H at transition = 0.617 l_P

### Convention Uncertainty (Largest Systematic)

Whether m₂ = 1.42 M_P (standard) or 1.42 M̄_P (reduced, smaller by √(8π) ≈ 5.01) depends on Benedetti et al.'s coupling definitions. This creates a ~5× spread:

| Convention | m₂ | M_crit | r_H,crit |
|---|---|---|---|
| m₂ = 1.42 M_P | 1.74 × 10¹⁹ GeV | 0.308 M_P | 0.617 l_P |
| m₂ = 1.42 M̄_P | 3.46 × 10¹⁸ GeV | 1.55 M_P | 3.09 l_P |

**This convention dependence is the single largest systematic uncertainty in the framework's BH predictions.**

## Hawking Temperature at Transition

T_H = M_P²/(8πM) at M = M_crit:

| Convention | T_crit | T_crit (GeV) |
|---|---|---|
| m₂ = 1.42 M_P | 0.129 M_P | 1.58 × 10¹⁸ |
| m₂ = 1.42 M̄_P | 0.026 M_P | 3.14 × 10¹⁷ |

Ratio T_crit/M_P ~ 0.03–0.13 is comparable to T_c/Λ_QCD ~ 0.5–0.7 in order-of-magnitude terms.

## M_rem vs M_crit Ordering

**Key finding:** The ordering depends on convention and determines whether the ghost trigger is operative or preempted.

| Convention | M_crit | M_rem (Bonanno-Reuter) | Ordering | Implication |
|---|---|---|---|---|
| m₂ = 1.42 M_P | 0.308 M_P | ~0.46 M_P | M_rem > M_crit ✅ | AS transition **preempts** perturbative instability (QCD analog: confinement before Landau pole) |
| m₂ = 1.42 M̄_P | 1.55 M_P | ~0.46 M_P | M_crit > M_rem ⚠️ | Ghost instability **triggers first**, drives BH into non-perturbative regime → eventually settles to AS remnant |

The reduced-convention scenario (M_crit > M_rem) produces the stronger, more genuinely novel picture: the ghost confinement instability IS the physical trigger that forces the transition.

Under unification, M_rem should depend on both g* (AS) and m₂/k = 1.42 (QG+F). This reduces the parameter space from (g*, m₂) independently to (g*, 1.42), narrowing M_rem ≈ 0.3–0.7 M_P.

## Transition Order

### Prediction: First-order (pure gravity), crossover (gravity + SM matter)

By QCD analogy:

- **Pure SU(3) gauge theory:** First-order deconfinement at T_c ≈ 270 MeV (latent heat h = 1.175(10), Polyakov loop discontinuous)
- **Physical quarks (N_f = 2+1):** Analytic crossover at T_c = 156.5 ± 1.5 MeV (quarks explicitly break Z(3) → transition smoothed)
- **Pure gravity:** CDT confirms A–C transition is first-order (see `../cdt-phase-diagram.md`)
- **Gravity + SM (~100 DOF):** By analogy, matter fields soften the transition to crossover

**Gravitational Polyakov loop analog:** In QCD, ⟨L⟩ = ⟨Tr P exp(i∮ A₀ dτ)⟩. In gravity: ⟨P exp(∮ Γ dτ)⟩ around the thermal circle, related to the conical deficit at the horizon. Smooth Euclidean section at T_H = ordered phase; conical defect at T ≠ T_H = disordered phase.

### Where the Analogy Breaks

- ❌ No gravitational Z(3) discrete center symmetry — diffeomorphism invariance is continuous
- ❌ Unknown if matter raises or lowers M_crit (in QCD, quarks lower T_c)
- ❌ "Number of flavors" threshold for crossover is undefined for gravity
- ❌ Quantitative latent heat ratio cannot be reliably transported from QCD

### If First-Order (Pure Gravity)

Latent heat by dimensional analysis: L ~ h × T_crit⁴ with h ~ O(1) (QCD analog). Total per BH: Q ~ 6.6 × 10⁻⁵ M_P ≈ **7 kJ** (~10⁻⁵ of BH rest mass energy at transition).

### If Crossover (Gravity + SM)

No latent heat. Transition window ΔM/M_crit ~ O(0.1), i.e. ΔM ~ 0.03 M_P.

## Heat Capacity Signature (Inherited from AS)

The Bonanno-Reuter temperature profile produces:
- M >> M_P: C = −8πM²/M_P² (standard, negative)
- M = M_max: C diverges (heat capacity sign change)
- M_rem < M < M_max: C > 0, approaching 0 (thermodynamically stable)
- M = M_rem: T → 0, C → 0⁺

Observational signature: burst at T_max followed by cooling to T → 0, rather than T → ∞ explosion. The unified framework adds only the specific T_max value (via m₂ constraint).

## Observability Assessment

| Prediction | Observable? | Why/Why Not |
|---|---|---|
| M_crit, T_crit | No | Requires observing Planck-mass BH evaporation |
| Transition order | No | Planck-scale BH thermodynamics inaccessible |
| Remnant existence | Possibly | Femtolensing, GW detectors (>2040) |
| Remnant DM fraction | Possibly | Indirect gravitational effects |
| Heat capacity divergence | No | Real-time Planck-scale observation |
| Final evaporation burst | Possibly | γ-ray telescopes, if PBH evaporation observed |

**The unified framework's ONLY observational distinction from pure AS is the specific value of T_max** (determined by m₂). Since T_max ~ 0.1 M_P in both cases, this distinction is practically unobservable.

## Full Prediction Classification

| # | Prediction | Classification | Justification |
|---|---|---|---|
| 1 | M_crit = 0.31 M_P | **NOVEL** | Requires both instability criterion (QG+F) and m₂ at NGFP (AS) |
| 2 | T_crit = 0.13 M_P | **NOVEL** | Derived from M_crit |
| 3 | Three-phase evaporation | **NOVEL** | Neither framework alone gives this picture |
| 4 | Transition order (pure gravity: 1st-order) | **NOVEL** | CDT evidence + QCD analogy |
| 5 | Transition order (gravity+SM: crossover) | **NOVEL** | QCD flavor analog |
| 6 | Latent heat Q ~ 7 kJ | **NOVEL** | Dimensional analysis + QCD ratio |
| 7 | Remnant mass M_rem ≈ 0.3–0.7 M_P | **INHERITED** (AS) | Bonanno-Reuter; unified only narrows range |
| 8 | Remnant temperature T → 0 | **INHERITED** (AS) | Extremal geometry |
| 9 | Heat capacity sign change | **INHERITED** (AS) | Generic to remnant scenarios |
| 10 | M_rem > M_crit ordering | **CONSISTENCY CHECK** | AS preempts perturbative instability |
| 11 | PBH remnant DM limited | **INHERITED** (AS) | γ-ray constraints too stringent |
| 12 | Ghost confinement trigger | **DISCRIMINATING** | True ONLY if QG+F and AS are unified |

## Honest Assessment

**Most BH evaporation predictions (7/12) are inherited from AS alone.** The unified framework adds:

1. A trigger mechanism (ghost confinement instability) — but may be preempted if M_rem > M_crit
2. Specific numerical values (M_crit, T_crit) — but unobservable
3. A three-phase narrative — conceptually elegant but not independently testable
4. The transition order prediction — genuine (AS alone doesn't address this) but untestable

**Bottom line:** The BH evaporation phase transition is "AS predictions dressed up with a ghost confinement trigger mechanism." The novelty is real but narrow: it's the trigger mechanism, not the endpoint.

**Caveat:** If the reduced Planck mass convention is correct (M_crit = 1.55 M_P > M_rem ≈ 0.46 M_P), the ghost instability IS the causal trigger, making the three-phase picture not just narrative but physically operative. This is the stronger scenario.

Sources: Bonanno et al. (2025, arXiv:2505.20360); Benedetti et al. (2009); Bonanno & Reuter (2000); arXiv:2502.03875 (QCD latent heat 2025); HotQCD (2019, arXiv:1812.08235); arXiv:2410.16206 (QCD critical endpoint 2024); exploration-s4-002 (strategy-004)
