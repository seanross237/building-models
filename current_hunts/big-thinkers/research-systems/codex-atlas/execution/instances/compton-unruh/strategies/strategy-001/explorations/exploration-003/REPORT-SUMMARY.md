# Exploration 003 — Summary

## Goal
Survey major proposals connecting the Unruh effect to inertia modification (McCulloch QI, Haisch-Rueda SED, MOND, Verlinde), identify no-go theorems, and assess whether a fatal obstacle exists for all Unruh-based inertia proposals.

## What Was Done
- Surveyed 5 proposals (McCulloch QI, Haisch-Rueda-Puthoff SED, Milgrom's MOND, Verlinde's emergent gravity, Jacobson/Padmanabhan thermodynamic gravity)
- Evaluated 7 no-go arguments with specific references and numerical computations
- Computed all key scales: T_U(a₀) = 4.9×10⁻³¹ K, u(Unruh)/u(CMB) = 10⁻¹²³, Wien wavelength at a₀ = 44× Hubble radius, McCulloch's critical acceleration = 2.0×10⁻¹⁰ m/s² (yields negative inertial mass at a₀!)
- Identified published critiques: Renda (2019) vs QI, Levin (2009) vs HRP (fatal), Visser (2011) vs Verlinde

## Outcome: NO UNIVERSAL NO-GO, BUT SEVERE CONSTRAINTS

**There is no single theorem killing all Unruh-based inertia proposals.** However:

**DEAD mechanisms:**
- Direct Compton-Unruh resonance (43 orders of magnitude, Expl. 001)
- Haisch-Rueda-Puthoff SED inertia (Levin 2009: relevant force = zero relativistically)
- McCulloch's QI *as literally formulated* (negative inertial mass at a₀; Renda 2019 derivation errors; predicted time-variation of a₀ conflicts with high-z observations)
- Any thermal-detection-based mechanism (T_U = 10⁻³¹ K drowned by CMB at 2.7 K; energy density ratio 10¹²³)

**SURVIVING mechanisms:**
- Vacuum structure / mode counting (Casimir analogy — not subject to temperature argument)
- Verlinde's entropic gravity (derives a₀ = cH₀/6 ≈ 1.1×10⁻¹⁰ m/s², matches MOND to ~10%)
- De Sitter crossover at a ~ cH₀ (area vs volume entropy competition)

## Key Takeaway
The Compton frequency plays NO role in any surviving proposal. The relevant physics is the **de Sitter horizon crossover** at a ~ cH₀, where cosmological entropy effects begin dominating over local gravitational effects. Verlinde's 2017 framework is the most developed version of this idea, deriving MOND-like phenomenology from de Sitter thermodynamics. However, it faces its own serious objections (dwarf galaxy failures, Visser's entropy critique, Bullet Cluster).

The strongest surviving objection for any new proposal: **stars in galaxies are in free fall (zero proper acceleration), so the standard Unruh effect should not apply to them.** Any mechanism must specify what "acceleration" enters the formula for freely-falling objects in curved spacetime.

## Leads Worth Pursuing
1. **Verlinde's de Sitter entropy displacement as the mechanism** — this IS the de Sitter crossover from Exploration 001, viewed from a holographic perspective. Could be computed more rigorously.
2. **The modified-inertia formulation of MOND** (Milgrom 2022, arXiv:2208.07073) — time-nonlocal action principle that may connect to vacuum structure effects.
3. **Whether a₀ varies with cosmic time** — direct test distinguishing QI (predicts variation) from Verlinde (unclear) and MOND (empirical constant).

## Unexpected Findings
- McCulloch's core equation gives **negative inertial mass** at MOND-relevant accelerations — the formula as published is unphysical in exactly the regime it's supposed to explain. This is a more fundamental problem than the Renda critique.
- The numerical coincidences are striking: cH₀/6 = 1.10×10⁻¹⁰, cH₀/(2π) = 1.05×10⁻¹⁰, observed a₀ = 1.2×10⁻¹⁰. Multiple derivations converge on the same scale.
- DARPA has invested $18.7M+ in QI-related research despite the theory being widely considered pseudoscience.

## Computations Identified
1. **Verlinde's entropy displacement for a specific galaxy** — Compute the predicted rotation curve from the full entropic force formula (not just the deep-MOND limit) and compare to SPARC data. Requires: Verlinde (2017) equations, galaxy baryonic mass profiles. Difficulty: ~100-line Python script.
2. **de Sitter Wightman function modification at a ~ cH₀** — Compute the exact detector response rate for an Unruh-DeWitt detector in de Sitter space as a function of proper acceleration, to see if the crossover produces any enhanced response. Requires: massive field Wightman function in de Sitter. Difficulty: moderate (known integrals but with hypergeometric functions).
3. **Time variation of a₀ at high redshift** — Model the expected variation of QI's critical acceleration 2c²/Θ(z) vs cosmic time and compare to observed radial acceleration relation at z = 0.5–2. Difficulty: ~50-line script using standard cosmology.
