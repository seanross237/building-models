# Mission Complete — Compton-Unruh Resonance

## Result

**The Compton-Unruh resonance does not exist, and the related de Sitter thermal crossover identity is falsified as a modified inertia mechanism.** The mission produced a rigorous negative result on the original hypothesis and discovered an apparently novel mathematical identity along the way.

## Summary of Findings

### The original hypothesis is dead

A particle's Compton frequency resonating with Unruh radiation at acceleration a ~ cH₀ is dimensionally impossible. The matching acceleration for a proton is a* = 2πmc³/ℏ ≈ 2.69 × 10³³ m/s², which is 43 orders of magnitude above cH₀ ≈ 6.6 × 10⁻¹⁰ m/s². The matching is mass-dependent (no universal a₀), the cosmological scale H₀ doesn't appear in the matching condition, and the Boltzmann suppression at a ~ cH₀ is exp(−10⁴²). This is as decisive as dimensional analysis gets.

### What was found instead

Exploring the de Sitter thermal crossover at a ~ cH₀ (the one feature at the right scale), the investigation discovered that the ratio of flat-space Unruh temperature to de Sitter-modified Unruh temperature is algebraically identical to the standard MOND interpolation function:

**T_U(a) / T_dS(a) = a / √(a² + c²H₀²) = μ(a/cH₀)** where μ(x) = x/√(1+x²)

This identity, if interpreted as m_i = m × T_U/T_dS, reproduces galaxy rotation curves (NGC 3198 χ²/dof = 1.21, NGC 2403 χ²/dof = 0.52 with Verlinde's a₀ = cH₀/2π correction) and the Baryonic Tully-Fisher relation.

### Why it doesn't work as physics

1. **No mechanism:** No first-principles derivation of m_i = m × T_U/T_dS exists. The fluctuation-dissipation theorem gives χ''_dS = χ''_flat exactly — zero modification. The naive entropic approach gives the wrong sign.

2. **Lensing falsification:** As modified inertia, the model does not modify the gravitational potential. Photon geodesics (and thus gravitational lensing) are unaffected. The Bullet Cluster produces a 5.7× lensing mass discrepancy. Cluster lensing universally shows 5-10× mass deficit. The CMB 3rd peak is suppressed ~2× without dark matter.

3. **Factor of 5.5:** The identity predicts a₀ = cH₀ ≈ 6.6×10⁻¹⁰ m/s², but observations require a₀ ≈ 1.2×10⁻¹⁰ m/s². The 2π cancels in the ratio, so the correction cannot come from within the framework — it requires Verlinde's area-volume entropy argument as external input.

4. **Internal inconsistency:** The formula m_i = m × μ(g_N/a₀) with g_N = GM/r² gives v(r) ∝ r^{1/2} in the deep-MOND limit, not the flat rotation curves observed. Getting v = constant requires μ to depend on the actual acceleration (v²/r), creating a self-referential definition.

### Ancillary findings

- **Free-fall objection resolved:** For stars in circular orbit in Schwarzschild-de Sitter spacetime, the acceleration relative to the Hubble flow equals g_N = GM/r² exactly (Λ cancels identically). This resolves Milgrom's 1999 objection about freely-falling objects.

- **McCulloch's QI internally inconsistent:** The core equation m_i = m(1 − 2c²/(Θa)) gives negative inertial mass when a < cH₀, which is precisely the MOND regime where the theory operates.

## Validation Tier Achievement

| Tier | Status | Key Evidence |
|------|--------|-------------|
| 1: Framework | ✅ Complete | QFT setup, Unruh effect derived, dimensional analysis |
| 2: Calculation | ✅ Complete | Key integral evaluated, T_U/T_dS ratio derived, FDT closed |
| 3: Predictions | ✅ Complete | Rotation curves for 2 galaxies, BTFR, solar system |
| 4: Distinctness | ✅ Complete | Distinguished from McCulloch, Verlinde, Milgrom 1999 |
| 5: Consistency | ✅ Complete | Falsified by Bullet Cluster lensing |

## Strategy History

One strategy was sufficient. Strategy-001 ("Adversarial Derivation Protocol") ran 8 explorations (6 succeeded, 1 failed due to context contamination, 1 adversarial stress test). The dimensional analysis in exploration 001 killed the original hypothesis immediately; the remaining explorations investigated the de Sitter crossover as a salvage route before the adversarial test in exploration 008 delivered the final falsification.

---

## Consolidated Novel Claims

### Claim 1: T_U/T_dS = μ_MOND (Standard MOND Interpolation Function)

**Claim:** The ratio of flat-space Unruh temperature to de Sitter-modified Unruh temperature is algebraically identical to the standard MOND interpolation function:

T_U(a)/T_dS(a) = a/√(a² + c²H₀²) = μ(x) = x/√(1+x²), where x = a/cH₀

**Evidence:**
- Direct algebraic computation. T_U = ℏa/(2πck_B), T_dS = (ℏ/2πck_B)√(a² + c²H₀²). The ratio simplifies trivially. Verified numerically with Python.
- Galaxy rotation curve fits using this interpolation function (with Verlinde correction a₀ = cH₀/2π): NGC 3198 χ²/dof = 1.21, NGC 2403 χ²/dof = 0.52.

**Novelty search:**
- Searched arXiv for "Unruh temperature" + "MOND interpolation function," "T_U/T_dS," and related terms. Zero exact matches found.
- **Closest prior work:** Milgrom (1999, astro-ph/9805346) used the *excess* temperature T_dS − T_GH, which gives a different formula: μ_Milgrom = 1 − 1/√(1+x²). This is algebraically distinct and has a₀ = 2cH₀ (further from observations).
- Also checked: Deser & Levin (1997), Padmanabhan (2002-2010), Lee (2012), Pikhitsa (2010), Verlinde (2016), Luo (2026). None state the ratio identity.

**Strongest counterargument:** The identity is algebraically trivial once the de Sitter Unruh temperature T_dS = (ℏ/2πck_B)√(a² + c²H₀²) is written down. The real content would be a physical argument for WHY m_i = m × T_U/T_dS, and no such argument exists. Without a mechanism, the identity relates two known quantities without explaining either. Furthermore, it is falsified as modified inertia by gravitational lensing.

**Status: Novel mathematical observation, falsified as physics.** The algebraic identity is exact and apparently unpublished. But it lacks a physical mechanism, requires an external factor of ~1/6 to match observations, and is observationally falsified as modified inertia (Bullet Cluster, cluster lensing, CMB). Could potentially motivate a modified gravity formulation (AQUAL with this specific μ), but that is a different theory.

---

### Claim 2: Resolution of the Free-Fall Objection via De Sitter-Relative Acceleration

**Claim:** For a star in circular orbit in Schwarzschild-de Sitter spacetime, the acceleration relative to the nearest Hubble flow worldline equals the Newtonian gravitational acceleration g_N = GM/r² exactly. The cosmological constant Λ cancels identically (not perturbatively) in the difference a_star − a_Hubble.

**Evidence:**
- Analytic computation in Schwarzschild-de Sitter spacetime. The star's centripetal acceleration from gravity is −(GM/r² − Λc²r/3). The Hubble flow acceleration at radius r is Λc²r/3. The difference is exactly −GM/r².
- Verified symbolically with Sympy and numerically for three test cases (galaxy star, Earth orbit, deep-MOND regime).
- Jacobson local Rindler approach independently gives a_Rindler = g_N.
- Resolves Milgrom's 1999 objection that freely-falling orbiting stars have zero proper acceleration, so the de Sitter temperature argument "does not obviously apply to circular orbits."

**Novelty search:**
- No paper found that explicitly computes a_dS_rel for orbital motion to resolve Milgrom's 1999 objection. However, the computation is straightforward (Newtonian limit), so it may exist unpublished or in a less visible venue.

**Strongest counterargument:** The computation is in the Newtonian limit. Post-Newtonian corrections might break the exact cancellation. Also, identifying "acceleration" with the de Sitter-relative quantity (rather than proper acceleration = 0 for geodesic motion) is a conceptual choice, not a derivation. One would need a physical principle for why de Sitter-relative acceleration is the operationally relevant quantity.

**Status: Computed, apparently novel, but limited significance.** The computation is clean and resolves a specific objection from the literature. But its significance depends on the T_U/T_dS framework being physically meaningful, which remains unestablished.

---

### Claim 3: McCulloch's Quantized Inertia Gives Negative Inertial Mass at MOND Accelerations

**Claim:** McCulloch's core equation m_i = m(1 − 2c²/(Θa)) gives negative inertial mass when a < 2c²/Θ = cH₀ ≈ 6.6×10⁻¹⁰ m/s², which is the MOND regime where the theory is supposed to operate. At a = a₀_MOND ≈ 1.2×10⁻¹⁰ m/s², the theory predicts m_i/m ≈ −10.

**Evidence:** Direct substitution into McCulloch's published equation. See also Renda (2019) for related critiques.

**Novelty search:** Renda (2019) published a critique of McCulloch identifying derivation errors. Whether this specific negative-mass observation has been published is unclear.

**Strongest counterargument:** McCulloch may intend a different limiting behavior or regularization. The equation as literally published gives negative mass.

**Status: Minor observation.** Algebraically trivial. May be known in the literature. Included for completeness.

---

## Open Leads (Not Pursued)

The following directions were identified but are outside this mission's scope:

1. **Modified gravity reformulation:** The T_U/T_dS identity gives μ(x) = x/√(1+x²), which is the standard MOND interpolation function already used in AQUAL. Embedding this in a modified gravity framework (Bekenstein's TeVeS or Verlinde's holographic approach) could survive the lensing test. This would be a new investigation, not a continuation of the Compton-Unruh question.

2. **Non-equilibrium mechanism:** The FDT closure assumes equilibrium. A non-equilibrium formulation (cosmological expansion as a slow drive) might give a different result, but this is speculative.

3. **Verlinde unification:** Understanding T_U/T_dS within Verlinde's elastic entropy framework could explain the 1/(2π) factor and provide the missing mechanism. This connects two independent lines of research.
