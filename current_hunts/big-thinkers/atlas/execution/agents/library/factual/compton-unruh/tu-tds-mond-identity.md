---
topic: T_U/T_dS = MOND interpolation function — algebraic identity and rotation curve consequences
confidence: provisional
date: 2026-03-27
source: "compton-unruh strategy-001 exploration-004"
---

## Finding

The ratio T_U(a)/T_dS(a) is **algebraically identical** to the standard MOND interpolation function μ(a/cH₀). If inertial mass is proportional to this ratio (m_i = m · T_U/T_dS), the model reproduces MOND rotation curves, the baryonic Tully-Fisher relation, and all solar system constraints. The predicted critical acceleration is a₀ = cH₀ — within factor 5.5 of the observed value; using Verlinde's factor yields 8% agreement.

## The Key Algebraic Identity

    T_U(a) / T_dS(a) = [ℏa/(2πck_B)] / [(ℏ/(2πck_B))·√(a² + c²H₀²)]
                     = a / √(a² + c²H₀²)

Setting x = a/(cH₀):

    T_U/T_dS = x / √(1 + x²)  ≡  μ_standard(x)

This is **exactly** the "standard" MOND interpolation function μ(x) = x/√(1+x²) (Milgrom 1983), with a₀ = cH₀. The identity is algebraically trivial and therefore certain.

**Status: [COMPUTED] — identity. Physical significance requires a derivation of why m_i ~ T_U/T_dS, which does not currently exist.**

## Ratio Hypothesis Equation of Motion

Under m_i = m · T_U/T_dS, the equation of motion g_N = μ(a/cH₀) · a gives:
- For a ≫ cH₀: μ → 1, so a = g_N (Newton recovered)
- For a ≪ cH₀: μ → a/(cH₀), so a²/(cH₀) = g_N, hence a = √(cH₀ · g_N) (deep MOND)

**Physical interpretation:** Inertia arises from the fraction of the thermal environment attributable to acceleration (T_U) versus the total thermal environment (T_dS). At high accelerations, T_U dominates and μ → 1. At low accelerations, T_GH dominates the bath and the acceleration-dependent fraction shrinks.

## Rotation Curves and BTFR

| Galaxy Mass (M☉) | v_flat Newton (km/s) | v_flat MOND | v_flat this model (a₀=cH₀) | v_flat (a₀=cH₀/6) |
|-----------------|---------------------|------------|---------------------------|-------------------|
| 10⁹ | 12 | 63 | 97 | 62 |
| 10¹⁰ | 38 | 112 | 172 | 110 |
| 10¹¹ | 120 | 200 | 306 | 195 |
| 10¹² | 379 | 355 | 544 | 348 |

With a₀ = cH₀: v_flat is ~1.53× too high. With a₀ = cH₀/6 (Verlinde's factor): within 11% of MW observed value (220 km/s).

The model predicts M_bar = v_flat⁴ / (G·a₀) — identical in form to MOND's BTFR; normalization factor ~5.5 vs observed (or ~8% off with Verlinde factor).

## a₀ Scale Problem

| Approach | Predicted a₀ (m/s²) | Ratio to observed (1.2×10⁻¹⁰) |
|----------|--------------------|-----------------------------|
| This model | cH₀ = 6.60×10⁻¹⁰ | 5.50× |
| Verlinde (2016) | cH₀/(2π) = 1.10×10⁻¹⁰ | 0.92 |
| McCulloch (2007) | 2c²/(πR_H) = 4.20×10⁻¹⁰ | 3.50× |

The factor of ~5.5 could arise from: field degrees of freedom, numerical prefactors in entropy-area relations, or whether the de Sitter vs. particle horizon sets the scale.

## Solar System Consistency

At Earth's orbital acceleration (a ~ 5.9×10⁻³ m/s²):

    μ = 1 - 6.2 × 10⁻¹⁵

No conflict with any solar system precision test.

## Provenance

Individual ingredients are all known:
- T_dS(a): Deser & Levin (1997)
- Verlinde entropic force (F = T·dS/dx → F = ma): Verlinde (2010)
- μ(x) = x/√(1+x²): Milgrom (1983)
- a₀ ~ cH₀: Milgrom (1983) cosmological coincidence

**The specific statement that T_U/T_dS IS μ_MOND appears not to have been explicitly published** (the algebra is too simple to require a paper, but no explicit statement found). Verlinde (2016) derives a similar conclusion through a different mechanism (elastic entropy of dark energy).

## Critical Weakness

The ratio ansatz m_i = m · T_U/T_dS has NO first-principles derivation. Three possible ansatze were tested:
- F ~ T_dS: WRONG SIGN (anti-MOND) — see `desitter-force-mechanisms-assessment.md`
- F ~ T_dS - T_GH: MOND-like but a₀ wrong by 11×, physically ad hoc
- F ~ T_U²/T_dS (i.e., m_i ~ T_U/T_dS): MOND exact, but physically unjustified

The ratio form gives the right answer but is **motivated by the desired result**, not derived from the physics. A rigorous derivation would require computing the back-reaction of the de Sitter vacuum on a uniformly accelerating particle from first principles (DeWitt-Brehme self-force in de Sitter — not yet done).

## Updates from Later Explorations (E005–E006)

**Novelty confirmed (E005):** Thorough search of six directly relevant papers (Milgrom 1999, Deser-Levin 1997, Verlinde 2016, Pikhitsa 2010, Smolin 2017, Luo 2026) and a direct web search found zero prior publications of T_U/T_dS = μ_MOND. Milgrom 1999, the closest prior work, uses the temperature EXCESS (T_dS − T_GH), not the ratio — a different formula with a different interpolation function. See `tu-tds-novelty-survey.md`.

**Free-fall objection — RESOLVED (E007):** The free-fall objection has been resolved by two independent methods: (1) de Sitter-relative acceleration = g_N exactly (Λ cancels — proven by symbolic algebra + 3 numerical test cases); (2) Jacobson local Rindler surface gravity = g_N (coordinate-independent). Both give identical formulas. Replace "proper acceleration" with "de Sitter-relative acceleration" to resolve the objection. See `free-fall-objection-analysis.md`.

**FDT does not give the ratio (E006):** Explicit FDT analysis shows χ''_dS = χ''_flat exactly (T-independent), so the standard FDT produces NO inertia modification. Furthermore, γ_dS > γ_flat (more damping, wrong direction). The sign problem is confirmed. See `fdt-no-inertia-modification.md`.

**Galaxy rotation curve fits (E006):** Numerical fits to NGC 3198 and NGC 2403 confirm cH₀ is decisively ruled out (χ²/dof ~ 130–140). With a₀ = cH₀/6, fits reach χ²/dof ~ 1, as good as or better than standard MOND. The functional form μ(x) = x/√(1+x²) is correct; only the scale needs a factor of ~5.7 correction. See `galaxy-rotation-curve-fits.md`.
