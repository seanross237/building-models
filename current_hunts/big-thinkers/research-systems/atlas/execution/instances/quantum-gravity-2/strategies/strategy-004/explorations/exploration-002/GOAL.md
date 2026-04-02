# Exploration 002: Black Hole Evaporation Phase Transition — Quantitative Predictions

## Mission Context

The Unified QG+F–AS Framework treats Quadratic Gravity with Fakeons (QG+F) and Asymptotic Safety (AS) as perturbative/non-perturbative descriptions of one UV-complete quantum gravity theory. The framework predicts a **phase transition** during black hole evaporation at M ~ M_P, analogous to QCD deconfinement. We need to extract every concrete, quantitative prediction from this phase transition.

## Your Task

**One question:** What are the specific quantitative predictions of the BH evaporation phase transition in the unified framework, derived using dimensional analysis, the QCD deconfinement analogy, and existing published results?

## What You Must Deliver

For each prediction, classify it as DISCRIMINATING (true only if unified), NOVEL (neither QG+F alone nor AS alone predicts this), CONSISTENCY CHECK (true for unified, also true for separate), or INHERITED (predicted by one/both standalone frameworks).

### Required Deliverables

1. **Critical transition mass M_crit.** The mass at which the Schwarzschild solution becomes unstable and the perturbative→non-perturbative transition occurs. Derive this from:
   - Bonanno et al. 2025 instability threshold: r_H ≈ 0.876/m₂
   - From our exploration-001: m₂ ≈ 1.42 M_P (derived from Benedetti et al. NGFP fixed-point values g₁* = -0.0101, g₃* = -0.0050)
   - Schwarzschild relation: r_H = 2GM
   - Give the transition mass in kg and Planck masses. Be specific.

2. **Hawking temperature at transition.** T_H = 1/(8πGM) at M = M_crit. Give in GeV and Kelvin.

3. **Order of the transition.** Is it first-order (with latent heat), second-order (continuous), or crossover?
   - Use the QCD deconfinement analogy: QCD deconfinement is a crossover for Nf = 2+1 physical quarks (at μ_B = 0), but first-order for pure gauge theory and at high μ_B. Map this: what is the gravitational analog of "quark flavors"?
   - Use the CDT phase diagram: Phase C→A transition is observed. What is its order?
   - If first-order: estimate the latent heat by dimensional analysis (L ~ T_c⁴ in QCD; what's the gravitational analog?)

4. **Remnant mass and temperature.**
   - AS predicts a Planck-mass remnant m_rem ~ 10⁻⁵ g. Under unification, can we sharpen this?
   - The remnant mass should depend on BOTH g* (AS parameter) AND m₂ (QG+F parameter). Under unification, these are related — does this constrain m_rem?
   - What is the remnant temperature? T → 0 is claimed — is it exactly zero or exponentially small?

5. **Heat capacity signature.** BH heat capacity is negative (C = -8πGM²). At the transition, C must change sign (remnants have C > 0 or T → 0). Derive the form of C(M) through the transition region.

6. **PBH dark matter predictions.** If remnants exist:
   - What initial PBH mass range produces remnants today? (Using standard Hawking evaporation time τ ~ M³/M_P⁴)
   - What is the maximum remnant abundance as a fraction of DM density? Are there existing observational constraints?

7. **Observable signatures.** For each prediction, assess:
   - Is it observationally accessible? When? With what instrument?
   - How does it differ from the "no phase transition" scenario (pure AS, no ghost confinement trigger)?

## Pre-loaded Context

**From Exploration 001:**
- Ghost mass at NGFP: m₂/k = √(g₁*/g₃*) ≈ 1.42, so m₂ ~ 0.5–2 M̄_P
- Ghost mass stays FINITE at NGFP (mass divergence ruled out for spin-2)
- Complex pole tower is the predicted mechanism for ghost dissolution

**From the library (BH predictions in QG+F):**
- Fakeon selects Schwarzschild uniquely (S₂⁻ = 0)
- QG+F corrections negligible for astrophysical BHs: ΔS/S ~ 10⁻⁷⁶ for solar mass
- Hawking spectrum modified by additional massive scalar channel when T_H > m₀
- QG+F makes NO testable BH prediction for astrophysical BHs

**From the library (Bonanno-Reuter BH):**
- RG-improved metric: f(r) = 1 - 4G₀mr²/[2r³ + g*⁻¹ξ²G₀(2r + 9mG₀)]
- Singularity resolution: G(r) → 0 as r → 0 (anti-screening)
- Two horizons (resembles Reissner-Nordström)
- Remnant mass ~10⁻⁵ g, T → 0
- g* typical range: 0.1–1.2 across truncations; Bonanno et al. 2024 uses g* = 540π/833 ≈ 2.04

**From the library (three-phase evaporation):**
- Phase I (M >> M_P): Standard Schwarzschild, ghost = fakeon
- Phase transition (M ~ M_P): Schwarzschild becomes unstable at r_H ≈ 0.876/m₂
- Phase II (M < M_P): AS regime, de Sitter core, T → 0, remnant

**QCD deconfinement features to map:**
- QCD crossover temperature: T_c ≈ 155 MeV (for physical quark masses)
- Lattice QCD establishes crossover (not sharp transition) at μ_B = 0
- First-order line at high μ_B (expected critical point at μ_B ~ 300-500 MeV)
- Pure SU(3) gauge: first-order with latent heat L ≈ 1.4 T_c⁴
- Order parameter: Polyakov loop ⟨L⟩ (Z(3) center symmetry)
- Chiral condensate as secondary order parameter
- Search for gravitational analogs of these order parameters

## Failure Path

If the QCD analogy breaks down for quantitative BH predictions (very possible given the 3 HIGH-severity breakdown points):
1. Explain WHERE it breaks — which step in the mapping fails
2. Derive whatever predictions CAN be made from dimensional analysis alone, without the QCD analogy
3. Assess: are the BH phase transition predictions genuinely NOVEL (neither QG+F alone nor AS alone predicts them), or are they just AS predictions dressed up with a "ghost confinement trigger"?
4. If the latter, be honest — the novelty is only the TRIGGER mechanism, not the endpoint

## Output

Write findings to:
- `explorations/exploration-002/REPORT.md` (200-400 lines)
- `explorations/exploration-002/REPORT-SUMMARY.md` (30-50 lines, write LAST)
