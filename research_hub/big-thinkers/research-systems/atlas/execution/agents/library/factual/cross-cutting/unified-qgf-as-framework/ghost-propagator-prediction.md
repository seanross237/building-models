---
topic: unified-qgf-as-framework
confidence: provisional
date: 2026-03-26
source: exploration-s4-001-ghost-propagator-specification (quantum-gravity-2 strategy-004)
---

# Ghost Propagator Prediction: Quantitative Specification

Detailed quantitative prediction of the unified QG+F–AS framework for how the spin-2 ghost dissolves. Contains specific numerical values, mathematical forms, pole migration pattern, and the amplitude equivalence test. **This is the framework's most concrete and discriminating prediction.**

## Ghost Mass at the NGFP

From the Stelle action linearized around flat space, the spin-2 TT propagator gives a ghost mass:

    m₂² = u₁/u₃

Using Benedetti, Machado, Saueressig (2009, arXiv:0901.2984) NGFP fixed-point values:

| Coupling | Value | Physical meaning |
|----------|-------|------------------|
| g₀* | 0.00442 | Cosmological constant (dim-4) |
| g₁* | −0.0101 | Newton's constant (dim-2, Euclidean sign) |
| g₂* | 0.00754 | R²-related (dimensionless) |
| g₃* | −0.0050 | C²-related (dimensionless) |

**Key numerical result:**

    m₂²/k² = g₁*/g₃* = (−0.0101)/(−0.0050) = 2.02
    m₂/k ≈ √2.02 ≈ 1.42 at the NGFP

The ghost mass is approximately **1.4 times the RG cutoff scale** at the fixed point — comparable to the Planck mass, neither parametrically large nor parametrically small.

**Physical ghost mass:** m₂^phys ≈ O(1) × M̄_P ≈ 0.5–2 × 10¹⁸ GeV (range reflects trajectory choice and truncation effects).

### BH Instability Scale

From Lü, Perkins, Pope, Stelle (2015, PRL 114, 171601), the Schwarzschild/non-Schwarzschild branch crossing occurs at r_H^cross ≈ 0.876/m₂. Using m₂ ≈ 1.4 M_P:

    r_H^cross ≈ 0.876/(1.4 M_P) ≈ **0.63 l_P**

This is **sub-Planckian** — the ghost-driven instability only triggers for BHs smaller than the Planck length, deep in the non-perturbative regime where AS takes over. Consistent with the unified framework.

## Predicted Ghost Dissolution Mechanism: Complex Pole Tower

The unified framework predicts the perturbative ghost pole dissolves into complex conjugate pole pairs via the Draper et al. (2020) mechanism.

### Mathematical Form

The spin-2 TT propagator:

    G_TT(p²) = 1/(p²(1 + p² f_C(p²)))

where f_C(p²) is the Weyl-squared form factor interpolating between:

**IR limit (p² << m₂²):**

    f_C(p²) → 1/m₂² = const

Recovers Stelle propagator with ghost pole at p² = −m₂²: G_TT → 1/p² − 1/(p² + m₂²)

**UV limit (p² >> m₂²):**

    f_C(p²) → (1/Λ_C²) tanh(p²/Λ_C²)

where Λ_C² = m₂²/c_C for some O(1) dimensionless constant c_C. Gives poles at:

    p²_n = ±iπn Λ_C²,    n = 1, 2, 3, ...

Properties of these poles:
- **Infinite tower** with Regge-type spacing Δ(p²) = πM²_Pl/c_C
- **Complex conjugate pairs** at imaginary p² — do NOT contribute to absorptive part
- **No real poles** except p² = 0 (massless graviton)
- Unitarity bounds: c_C > 1/60 (from partial wave analysis)

### Predicted Pole Migration Pattern

    p² << m₂²:    Single real pole at p² = −m₂²
    p² ~ m₂²:     Pole splits: p² = −m₂² ± iΓ₁, with Γ₁ growing
    p² ~ few × m₂²: Multiple conjugate pairs emerge
    p² >> m₂²:    Infinite tower at p² = ±iπn M²_Pl/c_C

**Transition scale:**

    p²_transition ≈ m₂² ≈ 2 M̄_P² ≈ (1.7 × 10¹⁸ GeV)²

## Why Other Mechanisms Are Excluded

### Mass Divergence (Becker et al. 2017)

Works for scalar ghosts (y* = 0 at NGFP₀). **Structurally excluded for spin-2**: g₃* = −0.0050 ≠ 0 at the NGFP. The C²-related coupling does NOT vanish, so the ghost mass cannot diverge.

### Residue Vanishing (Platania-Wetterich 2020)

Not demonstrated for the Stelle ghost across truncation orders. The fact that g₃* is finite at the NGFP works against residue vanishing — if the coupling doesn't flow to zero, the residue has no reason to vanish. **Possible but undemonstrated.**

## The Amplitude Equivalence Test

**The single sharpest discriminating claim** of the unified framework:

The scattering amplitudes computed from the non-perturbative complex-pole-tower propagator must equal the scattering amplitudes computed from the fakeon prescription (ghost-pole averaging) at tree level.

- **If amplitude equivalence holds** → fakeon is the perturbative shadow of AS dynamics → unification strongly supported (because there's no a priori reason for the equivalence to hold in the "compatible-but-separate" picture)
- **If amplitude equivalence fails** → the frameworks are dynamically incompatible → unification **refuted**
- **If ghost simply absent** (fictitious ghost) → neither framework wrong, but fakeon is superfluous

**Important caveat:** The complex pole tower might emerge from AS dynamics regardless of whether the unified picture is correct (non-perturbative QG naturally generates momentum-dependent form factors). The discriminating content is NOT "does the ghost dissolve?" but rather "does the ghost dissolve IN A WAY CONSISTENT WITH THE FAKEON PRESCRIPTION?"

## Honest Assessment

**Verdict: This is a well-specified consistency check, not a sharp discriminating prediction.**

It can **refute** unification (if ghost persists as real pole, or if amplitudes disagree) but cannot **uniquely confirm** it (complex poles could emerge for non-unified reasons). This is still valuable — refutability is the hallmark of a scientific prediction — but it's weaker than "measure X and get Y ± Z."

### Three Unknowns Blocking Full Quantitative Prediction

1. **The dimensionless parameter c_C** — controls pole spacing and high-energy amplitude behavior. Constrained only by unitarity (c_C > 1/60). Requires C²-extended FRG computation.
2. **The RG trajectory** — physical ghost mass depends on which UV-to-IR trajectory is chosen. NGFP fixes only m₂/k ≈ 1.42, not m₂^phys.
3. **The form factor functional form** — tanh is an ansatz motivated by FRG data, not first-principles for the C² sector.

## Computational Specification

The proposed computation (never performed):

1. Start from Γₖ including R, R², and C² terms with momentum-dependent form factors f_R(p²,k) and f_C(p²,k)
2. Derive the Wetterstein equation projected onto the spin-2 TT sector
3. Extract the anomalous dimension η_TT(p²) and running form factor f_C(p²,k)
4. Reconstruct the Lorentzian propagator via Padé approximants
5. Identify the pole structure of G_TT(p²)

**Available parameters:**
- From Knorr-Saueressig (2022): η_h ≈ 1.03, Z_h^UV = 0.64, g* ≈ 2.15 (Einstein-Hilbert)
- From Benedetti et al. (2009): g₁* = −0.0101, g₃* = −0.0050, m₂²/k² = 2.02 (will shift in C² truncation)

Cross-references: `../../asymptotic-safety/ghost-fate-strong-coupling.md` (ghost fate survey), `./discriminating-predictions.md` (discrimination analysis), `./open-problems.md` (#2 spin-2 confinement), `../../quadratic-gravity-fakeon/black-hole-predictions.md` (BH branch crossing)

Sources: Benedetti, Machado, Saueressig (2009, arXiv:0901.2984); Draper, Knorr, Ripken, Saueressig (2020, PRL 125, 181301); Knorr & Saueressig (2022, SciPost Phys. 12, 001); Becker, Ripken, Saueressig (2017, JHEP 12, 121); Platania & Wetterich (2020, arXiv:2009.06637); Lü, Perkins, Pope, Stelle (2015, PRL 114, 171601); Holdom & Ren (2016); Bonanno et al. (2025, arXiv:2505.05027); Salvio (2018, Front. Phys. 6, 77)
