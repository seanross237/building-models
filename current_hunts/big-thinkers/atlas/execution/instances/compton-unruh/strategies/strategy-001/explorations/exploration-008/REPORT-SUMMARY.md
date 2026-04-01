# Exploration 008 — Summary: Adversarial Stress Test of T_U/T_dS Modified Inertia

## What Was the Goal
Attack the T_U/T_dS modified inertia model (m_i = m × μ(g_N/a₀)) against the hardest observational constraints and theoretical consistency checks. Identify fatal weaknesses and assess viability.

## What Was Tried
Six observational tests + four theoretical consistency checks, all computed quantitatively using Python (numpy). Comparison with literature values for Bullet Cluster (Clowe 2006), Coma cluster (White 1993), CMB peaks (Planck 2018), wide binaries (Chae 2023), and solar system precision tests.

## Outcome: DECISIVE NEGATIVE — Multiple Critical Failures

**The model is observationally falsified by gravitational lensing data.**

### Fatal Failures

1. **Bullet Cluster (CRITICAL):** Modified inertia leaves the gravitational potential unchanged (∇²Φ = 4πGρ_baryon). Lensing traces baryons only. Predicted lensing mass = 3.5×10¹³ M_sun; observed = 2.0×10¹⁴ M_sun (5.7× discrepancy). More damning: lensing peaks at stellar location (14% of baryons), while model predicts lensing peaks at gas (86% of baryons). Wrong morphology AND wrong amplitude. No rescue possible without modifying the Poisson equation.

2. **Cluster Gravitational Lensing (CRITICAL):** For any galaxy cluster, lensing mass deficit is 5–10×. Einstein radius underestimated by factor √10 ≈ 3.2. Immediately detectable in any lensing survey.

3. **CMB 3rd Acoustic Peak (SEVERE):** If a₀ evolves with H(z), all CMB-scale modes are in deep MOND at z=1100 (catastrophic). If a₀ is fixed at today's H₀ (required for consistency), CMB dynamics are unaffected BUT there is no dark matter, so the 3rd/1st acoustic peak ratio is suppressed by ~2× relative to ΛCDM. Planck data matches ΛCDM to 1%.

4. **Cluster Dynamics — moderate:** Inherits MOND cluster failure (~2× missing mass from temperature profile analysis, Sanders 2003). Coma virial is actually near MOND prediction (σ_MOND = 872 km/s, σ_obs = 900 km/s) with correct M_baryon = 4×10¹³ M_sun, but detailed X-ray profiles require more mass.

5. **EFE and wide binaries:** Model predicts strong EFE suppression at 10,000 AU (enhancement only 7% vs 36% without EFE), which is mildly inconsistent with observed ~20–40% excess. The EFE formulation remains ambiguous.

6. **Solar system (PASSES):** Deviations < 10⁻⁸ everywhere, completely consistent.

### New Critical Internal Problem Identified

The T_U/T_dS formula has a fundamental ambiguity about which "a" enters μ:
- **Case A** (proper acceleration = 0 for orbiting stars): m_i = 0, kills the model immediately
- **Case B** (centripetal acceleration v²/r): gives standard MOND, flat rotation curves ✓, but the identification with Unruh acceleration is ad hoc
- **Case C** (Newtonian g_N, as written in GOAL.md): gives v ∝ r^(1/2), NOT flat rotation curves ✗

The model as stated in GOAL.md (Case C) is internally inconsistent with the rotation curve fits (which used Case B). This is a NEW problem not previously identified.

### Theoretical Summary
- Momentum NOT conserved (no action principle; m_i varies along trajectory)
- WEP preserved (all particles have same μ → universality of free fall holds)
- SEP violated (EFE, like all MOND theories)
- No ghost/negative-mass instability (μ > 0 always)
- No first-principles derivation; FDT route closed (exploration 006)
- Factor of 1/6 requires Verlinde input

## Key Takeaway

The T_U/T_dS modified inertia model is falsified by gravitational lensing observations. The fundamental failure is intrinsic to the modified-inertia framework: changing m_i does not change m_g or the gravitational potential, so photon geodesics (lensing) are unaffected. Any model that claims to explain "missing mass" only through modified dynamics — without modifying the potential — will fail all lensing tests. The mathematical identity T_U/T_dS = μ_MOND is real, but its physical realization must be as a modified gravity (not modified inertia) theory to survive observational scrutiny.

## Viability Ratings
- **Theoretical: 2/10**
- **Observational: 3/10** (galaxy scales only; cluster and CMB scales falsified)

## Leads Worth Pursuing

1. **Reformulation as modified gravity:** If T_U/T_dS modifies the Poisson equation (not just m_i), the lensing objection is avoided. This would connect to TeVeS or AQUAL. Is there a route from the temperature ratio formula to a modified Poisson equation?

2. **Dark matter + T_U/T_dS:** Perhaps the identity T_U/T_dS = μ_MOND explains galaxy-scale MOND behavior as an effect of de Sitter physics ON TOP OF standard ΛCDM dark matter (not replacing it). This hybrid would pass lensing tests.

3. **Sterile neutrinos as cluster dark matter:** The MOND literature often invokes ~2 eV sterile neutrinos to fill the cluster mass gap. If the T_U/T_dS model is combined with ~2 eV sterile neutrinos, the cluster dynamics failure is rescued. The lensing failure (Bullet Cluster morphology) is harder to fix.

## Unexpected Findings (Outside Goal Scope)

1. **The Coma cluster virial DOES match MOND** with correct baryon mass (~4×10¹³ M_sun). The standard claim "MOND fails at Coma" refers to X-ray temperature profiles (spatially resolved), not the global virial theorem. This nuance matters for how sharply the cluster failure is characterized.

2. **The GOAL.md notation (Case C: μ depends on g_N) is INTERNALLY INCONSISTENT with the rotation curve fits** (which used Case B: μ depends on actual acceleration a). This ambiguity was not previously flagged in explorations 001–007 and represents a gap in the model's internal consistency.

## Computations Performed
All results computed numerically. Key scripts:
- `code/adversarial_tests.py`: Bullet Cluster, CMB epoch analysis, lensing comparison, solar system table
- `code/coma_cluster_corrected.py`: Coma cluster corrected analysis, CMB peak ratio quantitative, EFE wide binary table, falsification scorecard
