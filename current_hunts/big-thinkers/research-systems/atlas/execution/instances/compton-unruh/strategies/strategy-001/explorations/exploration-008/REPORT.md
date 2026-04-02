# Exploration 008 — Adversarial Stress Test of the T_U/T_dS Modified Inertia Approach

## Goal Summary

This is an adversarial analysis of the T_U/T_dS modified inertia model accumulated in explorations 001–006. The model defines inertial mass as:

    m_i = m × μ(g_N/a₀)

where μ(x) = x/√(1+x²) (standard MOND interpolation function), a₀ ≈ cH₀/6 ≈ 1.1×10⁻¹⁰ m/s², and the formula derives from the ratio T_U(a)/T_dS(a) of Unruh to de Sitter temperatures. The exact algebraic identity is:

    T_U(a)/T_dS(a) = a/√(a² + c²H₀²)

which is the MOND interpolation function with a₀ = cH₀ (or a₀ = cH₀/6 with Verlinde correction).

Known strengths going in: galaxy rotation curves (χ²/dof ~ 0.5–1.3), BTFR, solar system consistency. Known weaknesses: no first-principles derivation, free-fall objection unresolved, factor of 1/6 imported from Verlinde.

**This exploration attacks the model.**

---

## Critical New Finding: Internal Inconsistency on Rotation Curves

Before the standard observational tests, a fundamental internal inconsistency emerged from the stress test that deserves front-page treatment.

**The T_U/T_dS formula produces three distinct models depending on which "a" enters μ:**

### Case A: a = proper acceleration
The Unruh temperature T_U = ℏa/(2πck_B) uses proper acceleration. For a star in circular orbit (geodesic motion), proper acceleration = 0. Therefore:

    T_U(0)/T_dS(0) = 0 → m_i = 0

This gives zero inertial mass for any freely-falling body. **Catastrophic failure** — instantly killed by the free-fall objection (Milgrom 1999, now 25 years unresolved).

### Case B: a = centripetal acceleration (v²/r)
If we substitute a = v²/r into T_U/T_dS, we get the standard MOND formula:

    μ(a/a₀) × a = g_N   where a = v²/r

This is Milgrom's original MOND. For circular orbits in the deep MOND limit:
- a × (a/a₀) = GM/r²  →  a² = a₀ × GM/r²
- v²/r = √(a₀ × GM)/r  →  v⁴ = GM × a₀ = CONSTANT

This gives **flat rotation curves** ✓. This is what explorations 004 and 006 actually computed.

### Case C: a = Newtonian gravitational acceleration g_N
The GOAL.md notation "m_i = m × μ(g_N/a₀)" implies this case. Then:

    m × μ(g_N/a₀) × v²/r = m × g_N
    v² = g_N × r / μ(g_N/a₀)

In deep MOND (g_N << a₀): μ ≈ g_N/a₀, so:
- v² = (g_N/a₀) × r / (g_N/a₀) × ... = a₀ × r
- v ∝ √r — **NOT flat rotation curves**

This case **fails to reproduce the key MOND phenomenology**. The exploration 004/006 rotation curve fits were done with Case B (standard MOND), not Case C as the model notation implies.

**Bottom line on this ambiguity:**
- Case A: free-fall objection (the dominant obstacle from explorations 001–007)
- Case B: gives correct MOND, but the identification a = v²/r with Unruh proper acceleration is ad hoc
- Case C: as stated in GOAL.md, gives v ∝ √r (wrong rotation curves)

The model is internally inconsistent: the notation in GOAL.md (Case C) contradicts the rotation curve fits (which used Case B). This is a new, previously unidentified problem.

---

## Section 1: The Bullet Cluster (1E 0657-558) — CRITICAL FAILURE

### Setup
The Bullet Cluster is the canonical test for dark matter models. Two galaxy clusters collided at ~3600 km/s. The hot X-ray gas (86% of the baryonic mass) was slowed by ram pressure and lags behind the stellar component. Gravitational lensing peaks are observed at the **stellar** locations, NOT the gas.

### Why Modified Inertia Fails

Modified inertia (T_U/T_dS model) changes m_i but leaves the **gravitational mass** m_g and the gravitational potential equation unchanged:

    ∇²Φ = 4πG × ρ_baryon  (standard Poisson equation)

Gravitational lensing is determined by photon geodesics in the potential Φ. Since Φ is unchanged, lensing traces the **baryonic mass only**, with no enhancement.

In the Bullet Cluster, the baryonic mass is:
- Hot X-ray gas: 3.0×10¹³ M_sun (86%)
- Stellar mass: 5.0×10¹² M_sun (14%)
- Total baryonic: 3.5×10¹³ M_sun

Observed lensing mass: 2.0×10¹⁴ M_sun (Clowe et al. 2006)

**Failure 1 (amplitude):** Modified inertia predicts lensing mass = 3.5×10¹³ M_sun. Observed = 2.0×10¹⁴ M_sun. **Discrepancy: 5.7×**.

**Failure 2 (morphology):** Modified inertia predicts lensing peaks at the gas location (86% of baryons). Observed: lensing peaks at the stellar component. This is the diagnostic signal: the gas and the "dark matter" are spatially separated by 720 kpc projected. Modified inertia predicts the OPPOSITE morphology from what is observed.

### Comparison to MOND Gravity

Modified gravity (MOND/AQUAL), which modifies the Poisson equation:
    ∇·[μ(|∇Φ|/a₀) × ∇Φ] = 4πG × ρ_baryon

creates an enhanced potential. At r = 0.5 Mpc from the Bullet cluster center:
- g_N = G × M_baryon / r² = 1.95×10⁻¹¹ m/s²
- x = g_N/a₀ = 0.18
- μ = 0.176
- MOND effective mass = M_baryon/μ ≈ 2.0×10¹⁴ M_sun

This matches the observed lensing mass! MOND gravity can explain the **amplitude** of lensing (the enhanced potential from non-linear Poisson equation acts like extra mass). However, MOND gravity still predicts lensing follows the gas (total baryon distribution), not just the stellar component, so the **morphology failure** applies to MOND gravity too — unless neutrino dark matter is invoked.

**Modified inertia is worse than modified gravity here:** It fails both the amplitude (5.7× deficit) AND the morphology.

### Verdict: CRITICAL FAILURE — The Bullet Cluster alone is sufficient to rule out modified inertia models where the gravitational potential is not modified.

---

## Section 2: CMB Third Acoustic Peak — FAILS

### Does Modified Inertia Affect CMB Dynamics?

The de Sitter temperature is T_dS = ℏH₀/(2πck_B), which involves the current H₀. There are two scenarios:

**Scenario A: a₀ evolves as a₀(z) = cH(z)/6**

At z = 1100 (recombination), H(z=1100) ≈ 2.3×10⁴ × H₀, so a₀(z=1100) ≈ 2.3×10⁴ × a₀(today) ≈ 2.5×10⁻⁶ m/s².

Typical gravitational acceleration in CMB density perturbations (at the sound horizon scale ~140 kpc physical at z=1100, δρ/ρ ~ 10⁻⁴):
- g_CMB ≈ 4/3 π G ρ_baryon δ r_sound ≈ 6.7×10⁻¹¹ m/s²

With a₀(z=1100) ≈ 2.5×10⁻⁶:  x = g_CMB/a₀ ≈ 2.6×10⁻⁵ → μ ≈ 2.6×10⁻⁵

**Deep MOND at recombination: catastrophic.** All acoustic modes have essentially zero inertial mass. Structure formation and acoustic oscillations are completely disrupted. **Evolving a₀ is observationally ruled out.**

**Scenario B: a₀ = cH₀/6 = constant (today's value)**

With fixed a₀:  x = g_CMB/a₀ ≈ 0.6  →  μ ≈ 0.52

The acoustic modes are at the transition between Newtonian and MOND regimes. While not fully Newtonian, the model doesn't catastrophically disrupt CMB physics.

However: even with fixed a₀, the model has no dark matter component. The CMB peak ratios depend critically on the dark matter fraction:

- ΛCDM (Ω_DM = 0.27): 3rd/1st acoustic peak ratio ≈ 0.43 (matches Planck 2018)
- Baryon-only model: 3rd/1st acoustic peak ratio ≈ 0.20 (suppressed by ~2×)

Without dark matter, the 3rd acoustic peak is suppressed by ~2× relative to the 1st peak, because CDM provides the potential wells that enhance odd peaks relative to even peaks. Planck CMB data matches ΛCDM peak ratios to ~1% accuracy.

**Secondary issue:** The model requires a₀ = constant at today's value, but the T_U/T_dS formula naturally gives a₀ = cH/6 where H is the de Sitter Hubble. Why should H be frozen at its today's value for physics throughout cosmic history? No mechanism is provided. This is the "cosmic coincidence" problem in a new form.

**Verdict: FAILS the CMB 3rd peak test.** Even with a fixed a₀ (saving CMB dynamics), the model has no dark matter and predicts the wrong CMB peak ratio by ~2×.

---

## Section 3: Gravitational Lensing Without Dark Matter — CRITICAL FAILURE

### The Core Problem

In modified inertia, the gravitational potential Φ satisfies the standard Poisson equation. Photons travel on geodesics of the spacetime metric, which (in the weak-field limit) is determined entirely by Φ. Therefore:

- Lensing convergence κ = Σ_baryon / Σ_cr  (standard formula, unmodified)
- Einstein radius θ_E = √(4GM_baryon/c² × D_LS/(D_L D_S))  (baryonic mass only)
- Lensing mass = baryonic mass  (no dark matter contribution, no MOND enhancement)

### Observational Comparison

For typical strong-lensing clusters:
- Observed lensing mass: ~10¹⁵ M_sun
- Baryonic mass: ~10¹⁴ M_sun
- Ratio: 10:1

Modified inertia predicts a lensing mass 10× too low. Since Einstein radius θ_E ∝ √M_lens, the model underestimates arc radii by a factor of √10 ≈ 3.2. This is immediately detectable in any lensing survey.

For the El Gordo cluster (ACT-CL J0102-4915, z=0.87, another Bullet Cluster analog):
- Baryonic mass: ~2×10¹³ M_sun
- Lensing mass: ~2×10¹⁴ M_sun
- Factor: 10×

**Contrast with modified gravity (MOND):** In AQUAL or TeVeS (relativistic MOND), the modified Poisson equation creates an enhanced effective potential. For a typical cluster in deep MOND (μ ≈ 0.18 at r = 0.5 Mpc):

    M_eff_lensing ≈ M_baryon/μ ≈ 5.7 × M_baryon

This partially (but not fully) bridges the lensing gap. Modified inertia has NO such enhancement.

**Verdict: CRITICAL FAILURE at all cluster scales. Modified inertia predicts gravitational lensing masses 3–10× below observations, with wrong spatial morphology.**

---

## Section 4: Galaxy Cluster Dynamics (Coma Cluster) — MARGINAL FAILURE

### Setup

Coma cluster parameters (from literature, White et al. 1993, Briel et al. 1992):
- Hot X-ray gas: ~3.5×10¹³ M_sun
- Stellar mass: ~5×10¹² M_sun
- **Total baryonic: ~4×10¹³ M_sun**
- Observed velocity dispersion: σ ≈ 900 km/s
- Dynamical mass (Newtonian virial): ~1.5×10¹⁵ M_sun

Note: The initial calculation in this exploration used M_gas = 3×10¹⁴ M_sun (10× too large). Corrected values are used throughout.

### MOND/Modified-Inertia Prediction

In deep MOND, the virial theorem gives: σ⁴ = G × M_baryon × a₀

With M_baryon = 4×10¹³ M_sun:
- σ_MOND = (G × M_baryon × a₀)^(1/4) = 872 km/s
- Observed: 900 km/s
- Ratio: 0.97 — **near agreement!**

At the cluster periphery (r = 1.5 Mpc):
- g_N = 2.5×10⁻¹² m/s², x = g_N/a₀ = 0.023 (deep MOND)

This superficial agreement is misleading. The standard MOND cluster failure is more nuanced:

### Where the MOND Cluster Failure Actually Lives

1. **X-ray temperature profiles (spatially resolved):** The temperature map of the intracluster gas in hydrostatic equilibrium requires a gravitational potential deeper than baryons alone provide, even in MOND. The temperature at r = 0.5–1 Mpc is too high.

2. **The "2× missing mass" result (Sanders 2003):** A systematic analysis of 26 clusters shows MOND needs ~2× more mass than the observed baryons to match X-ray temperature and velocity dispersion data simultaneously. This modified inertia model inherits this failure identically.

3. **Temperature profile consistency:** The MOND deep-virial σ⁴ = GMa₀ gives a global virial agreement but the spatially-resolved temperature profile (dP/dr = -ρg_MOND) requires more than baryons.

### Verdict for Modified Inertia vs Modified Gravity

- Modified gravity (MOND): Modifies the potential itself, so both dynamics AND lensing are enhanced. Fails cluster scales at ~2× level.
- Modified inertia (T_U/T_dS): Modifies dynamics but NOT the potential. Fails cluster lensing at 5–10× level. Cluster dynamics failure ~2× from Sanders (2003).

**Verdict: MODERATE FAILURE. The model inherits the MOND cluster problem (factor ~2 missing mass in X-ray temperature profiles), compounded by complete lensing failure.**

---

## Section 5: External Field Effect (EFE) — COMPLEX PREDICTION

### Does the Model Predict an EFE?

If the acceleration entering μ is the **total** gravitational acceleration (internal + external), then the model predicts an EFE: the MOND enhancement of a small system is suppressed when it sits in a strong external field. This violates the strong equivalence principle (like all MOND-type theories), but not the weak equivalence principle.

If only the **internal** acceleration enters μ, there is no EFE. The choice is not specified by the T_U/T_dS formula and requires additional physical input.

### Wide Binary Test

At the Sun's position, g_MW ≈ 1.96×10⁻¹⁰ m/s² ≈ 1.80 × a₀ (where a₀ = cH₀/6).

For wide binaries at different separations:

| Separation | g_int | g_ext | v_Keplerian | v_MOND no-EFE | v_MOND with-EFE |
|------------|-------|-------|-------------|----------------|-----------------|
| 3,000 AU   | 1.3×10⁻⁹ (x=12) | 2.0×10⁻¹⁰ | 769 m/s | 412 m/s | 412 m/s |
| 10,000 AU  | 1.2×10⁻¹⁰ (x=1.1) | 2.0×10⁻¹⁰ | 421 m/s | 412 m/s | 451 m/s |
| 30,000 AU  | 1.3×10⁻¹¹ (x=0.12) | 2.0×10⁻¹⁰ | 243 m/s | 412 m/s | 260 m/s |

At 10,000 AU (both g_int and g_ext ~ a₀), the EFE suppresses enhancement from 1.36× to 1.07×.

**Key observation:** The 2024 wide binary study (Chae 2023, 26,615 Gaia binaries) finds ~20–40% excess above Newtonian at these separations. This is:
- Consistent with MOND **without** EFE: ~36% at 10,000 AU
- **Inconsistent** with MOND **with** EFE: only ~7% at 10,000 AU

This creates a dilemma for the T_U/T_dS model:
- WITH EFE: suppressed enhancement inconsistent with wide binary observations
- WITHOUT EFE: violates the standard MOND/modified inertia EFE from non-linear dynamics

**Verdict:** The EFE prediction is testable and potentially discriminating. Current wide binary data mildly disfavors models WITH strong EFE. However, the wide binary observational situation is contested.

---

## Section 6: Solar System Precision Tests — CONSISTENT

### Deviations at Each Planet

At any planetary orbit, the deviation from Newtonian dynamics is:
- δ(m_i/m) = 1 - μ(g_N/a₀)

| Object | r (AU) | g_N (m/s²) | x = g_N/a₀ | 1 - μ |
|--------|--------|------------|------------|--------|
| Mercury | 0.39 | 3.96×10⁻² | 3.6×10⁸ | ~0 |
| Earth | 1.00 | 5.93×10⁻³ | 5.4×10⁷ | 2.2×10⁻¹⁶ |
| Saturn | 9.54 | 6.5×10⁻⁵ | 6.0×10⁵ | 1.4×10⁻¹² |
| Pluto | 39.5 | 3.8×10⁻⁶ | 3.5×10⁴ | 4.1×10⁻¹⁰ |
| 100 AU | 100 | 5.9×10⁻⁷ | 5.4×10³ | 1.7×10⁻⁸ |
| Voyager (~150 AU) | 150 | 2.6×10⁻⁷ | 2.4×10³ | 8.5×10⁻⁸ |

All deviations are well below any current observational precision (best constraint ~10⁻⁵ from Cassini).

**Pioneer anomaly (40–70 AU):** g_N ≈ 3.7×10⁻⁶ m/s² >> a₀. The model predicts zero anomaly. The Pioneer anomaly was subsequently explained by thermal radiation pressure (Turyshev et al. 2012), so this is consistent.

**Lunar laser ranging:** δ(m_i/m) < 10⁻¹⁵ at Earth's gravity — completely unobservable.

**Eötvös tests:** At g = 9.8 m/s², x = 9.0×10¹⁰, μ = 1 - 10⁻²⁸. WEP tests are sensitive to ~10⁻¹⁵. The model predicts zero WEP violation at this level.

**EFE from Milky Way:** The Sun sits at g_MW ≈ 2a₀. With EFE, all solar system objects feel this external field. However, at Earth's orbit g_Sun/g_MW ≈ 3×10⁷, so g_total ≈ g_Sun and μ ≈ 1 to 10⁻¹⁶ precision. At 100 AU, x_total ≈ 5000 → μ ≈ 1 - 10⁻⁸. Still unobservable.

**Verdict: Solar system is fully consistent. Deviations are below 10⁻⁸ even at 100 AU.**

---

## Section 7: Theoretical Consistency

### 7.1 Equivalence Principle

**Weak equivalence principle (WEP) — universality of free fall:**
In the T_U/T_dS model, the equation of motion is F = m_i × a = m × μ × a, while gravitational force is F = m_g × g_N = m × g_N. Setting these equal: a = g_N/μ(g_N/a₀).

Since μ depends only on g_N (a property of the local gravitational field, not the test particle), **all particles at the same location have the same acceleration**. WEP is preserved.

At laboratory scales: deviation is < 10⁻²⁸, completely invisible.

**Strong equivalence principle (SEP) — internal dynamics independent of external field:**
If EFE applies, SEP is violated. The internal dynamics of a dwarf galaxy depend on whether it's isolated or in a cluster. This is the same SEP violation as MOND — it's a defining prediction of the class of theories, not a flaw per se.

**Remark:** If the model is meant to apply to all forces (not just gravity), then applying μ to electromagnetic accelerations would produce observable WEP violations. But the T_U/T_dS derivation is specifically about the gravitational/de Sitter thermal environment, so the modification likely applies only to gravitational dynamics. This needs specification.

### 7.2 Conservation Laws — SERIOUS THEORETICAL DEFECT

In modified inertia, the momentum of an object is:
    p = m_i × v = m × μ(g_N/a₀) × v

As the object moves through the gravitational field, μ changes:
    dp/dt = m × dμ/dt × v + m × μ × a = m × (dμ/dt × v + μ × a)

For Newton's 3rd law: F₁₂ = -F₂₁ (gravitational forces equal and opposite). Then:
    dp₁/dt = F₂₁ ≠ -dp₂/dt = -F₁₂ = -F₂₁

if dμ/dt × v ≠ 0. Total momentum is NOT conserved when inertial mass varies along the trajectory.

In MOND (modified gravity, Bekenstein-Milgrom 1984), the Lagrangian formulation ensures momentum conservation via Noether's theorem. Modified inertia has no such guarantee.

How severe is this violation? For two galaxies passing each other at v ~ 10⁶ m/s with Δμ ~ 0.1 (as the MOND regime transitions): the momentum violation is ~10⁵ m/s per unit gravitational mass per unit time. For a galaxy with M ~ 10¹¹ M_sun, this is a momentum kick of ~10⁵ × M ~ 10⁴⁶ kg⋅m/s per second. Over a merger timescale (~10⁹ years = 3×10¹⁶ s), the total spurious impulse is ~10⁶³ kg⋅m/s — comparable to the galaxy's actual momentum. This is not a small effect.

More fundamentally: **without an action principle, the modified inertia formulation cannot be embedded in quantum field theory or derived from a Lagrangian. It exists as a phenomenological prescription only.**

### 7.3 Causality and Stability

**No negative inertial mass:** μ(x) = x/√(1+x²) > 0 for all x > 0. Therefore m_i > 0 always. No ghost instability or tachyonic behavior from negative kinetic terms.

**Modified Jeans instability:** For density perturbations with modified inertia, the dispersion relation is modified:
    ω² = (c_s² k² - 4πGρ) / μ(g_N/a₀)

In the deep MOND regime (large scales, g_N/a₀ << 1), μ → 0, so ω² → ∞ for the gravitational instability term. This AMPLIFIES Jeans instability on large scales — structure forms more readily. This could help with structure formation, but the large-scale behavior needs careful regularization.

**Superluminal modes:** The dispersion relation above doesn't introduce superluminal propagation at the classical level (it modifies the instability timescale, not signal propagation). No obvious causality violation.

### 7.4 Cosmological Consistency

**The a₀ evolution problem** is one of the most severe theoretical issues.

If a₀ = cH(z)/6 (using instantaneous H at epoch z):
- At z = 1100: a₀ ≈ 2.3×10⁴ × a₀(today) ≈ 2.5×10⁻⁶ m/s²
- All CMB-scale perturbations have g ≪ a₀ → deep MOND → μ → 0 → m_i → 0
- **Catastrophic: structure formation fails, BBN nucleosynthesis rates are wrong**

| z | H(z)/H₀ | a₀(z) if evolving | a₀(z)/a₀(today) |
|---|---------|-------------------|-----------------|
| 0 | 1.0 | 1.09×10⁻¹⁰ m/s² | 1 |
| 1 | 1.78 | 1.94×10⁻¹⁰ | 1.78 |
| 5 | 8.23 | 8.97×10⁻¹⁰ | 8.23 |
| 100 | 573 | 6.25×10⁻⁸ | 573 |
| 1100 | 2.3×10⁴ | 2.55×10⁻⁶ | 2.3×10⁴ |
| 10⁹ (BBN) | 9.5×10¹⁵ | 1.03×10⁶ | 9.5×10¹⁵ |

If a₀ = cH₀/6 = constant (fixed at today's value):
- CMB dynamics and BBN are unaffected (g ≫ a₀ for all early-universe processes)
- MOND effect only kicks in at late times when galactic-scale structures form
- BUT: no mechanism in T_U/T_dS derivation explains why a₀ should be frozen at H₀

**Structure formation without dark matter:**
Even with fixed a₀, the model has no dark matter. Before recombination, CDM seeds density fluctuations that baryons fall into. Without CDM:
1. Acoustic oscillations at z > 1100 are purely baryonic
2. The third acoustic peak (sensitive to CDM enhancement) is suppressed by ~2×
3. Structure formation after recombination is purely baryonic → delayed, too low amplitude
4. BAO scale and matter power spectrum would differ from observations

This requires an alternative explanation of large-scale structure that modified inertia alone cannot provide.

---

## Section 8: Falsification and Viability Assessment

### The Decisive Falsification Test

**Gravitational lensing versus dynamics comparison in galaxy clusters.**

This test is already done. For any cluster with well-measured velocity dispersions AND weak/strong gravitational lensing:
- Modified inertia predicts: κ_lensing ∝ ρ_baryon (unmodified potential)
- ΛCDM predicts: κ_lensing ∝ ρ_baryon + ρ_DM >> ρ_baryon

Observations show lensing masses 5–10× the baryonic mass in all well-studied clusters. Modified inertia **as defined** (changing only m_i, not m_g or the gravitational potential) is **falsified by the cluster lensing data.**

This is not a marginal result. The discrepancy is a factor of ~5–10× in mass, corresponding to a factor of ~3× in arc radii, well above any observational uncertainty.

### What Would Confirm the Model

The model could make distinctive predictions in the galaxy regime where it hasn't been falsified:

1. **Radial Acceleration Relation (RAR):** The T_U/T_dS model (in Case B formulation) predicts the RAR exactly: g_total = μ⁻¹(g_N/a₀) × g_N. The RAR is now measured with high precision using SPARC data. Any deviation from the specific MOND interpolation function shape would discriminate.

2. **EFE signature in wide binaries:** Binaries at different galactic altitudes (different g_ext) should show different levels of MOND enhancement. This would confirm EFE and the class of MOND-like theories.

3. **Extremely isolated dwarf galaxies:** Systems with no external field should show pure MOND enhancement. These provide the cleanest test.

However, all of these confirm **MOND-like phenomenology**, not specifically the T_U/T_dS origin. The model would need to make a prediction that DIFFERS from generic MOND to be confirmed as specifically T_U/T_dS rather than just MOND.

### Viability Scorecard

| Test / Property | Score | Notes |
|-----------------|-------|-------|
| Galaxy rotation curves | 7/10 | Works IF using μ(a/a₀) [Case B, not GOAL.md Case C] |
| BTFR (v ∝ M^1/4) | 8/10 | Automatic consequence of Case B |
| Solar system | 10/10 | Deviations < 10⁻⁸, undetectable |
| Bullet Cluster lensing | 0/10 | Morphology AND amplitude both fail |
| CMB 3rd acoustic peak | 1/10 | No CDM → wrong peak ratios by 2× |
| Cluster dynamics | 3/10 | Inherits MOND ~2× missing mass failure |
| Cluster lensing | 0/10 | 5–10× lensing mass deficit |
| WEP preservation | 9/10 | Universal μ → universality of free fall OK |
| SEP (strong EP) | 3/10 | EFE violates SEP, like all MOND theories |
| Momentum conservation | 2/10 | No action principle; p not conserved |
| First-principles derivation | 0/10 | No mechanism; FDT route closed |
| a₀ value | 4/10 | Factor of 1/6 imported from Verlinde |
| Free-fall objection | 2/10 | 25-year-old unresolved problem |
| Internal consistency (which a?) | 1/10 | Three cases give contradictory results |
| **Average** | **3.6/10** | |

### Final Ratings

**Theoretical viability: 2/10**
- No first-principles derivation of m_i = m × T_U/T_dS
- Momentum not conserved (no action principle)
- Fundamental ambiguity in which acceleration enters μ (Cases A/B/C)
- Free-fall objection (25 years unresolved) with no clear resolution
- Factor of 1/6 must be imported from Verlinde (not derived internally)

**Observational viability: 3/10**
- Rotation curves: works (but this is just MOND — not a distinctive success)
- Bullet Cluster: decisively falsified
- CMB peak ratios: fails by 2× (no CDM)
- Cluster lensing: fails by 5–10×
- Solar system: passes
- Wide binary: marginal/contested

**Overall verdict: The T_U/T_dS model as a MODIFIED INERTIA theory is observationally falsified by gravitational lensing data, most decisively by the Bullet Cluster. The lensing failure is intrinsic to the modified inertia framework — changing m_i leaves the gravitational potential and hence photon geodesics unaffected. To rescue the observational predictions, the model would need to be reformulated as a modified GRAVITY theory that also modifies the potential. Even then, the CMB third peak problem and structure formation would require additional dark matter-like component. The algebraic identity T_U/T_dS = μ_MOND remains a genuine mathematical curiosity of uncertain physical meaning.**

---

## Section 9: What the Model Gets Right (Credit Where Due)

Despite the above criticisms, the model does have genuine content:

1. **The algebraic identity T_U(a)/T_dS(a) = μ_MOND(a/cH₀) is real and appears novel.** No prior publication found with this identity. It's a mathematical fact independent of physical interpretation.

2. **Galaxy rotation curves work beautifully** (with a₀ = cH₀/6) — but this is because the model is equivalent to standard MOND at galaxy scales, and MOND is well-tested there.

3. **Solar system consistency is perfect** — no fine-tuning needed; the scale separation is enormous.

4. **The WEP is technically preserved** — the universality of free fall holds because μ depends on the field, not the test particle.

5. **The connection to de Sitter physics is potentially deep** — the appearance of the Hubble scale H₀ in the MOND acceleration a₀ is not understood within any CDM framework. The T_U/T_dS identity offers one route to understanding this connection, even if the detailed mechanism hasn't been derived.

---

## Appendix: Code

Computations were run in:
- `code/adversarial_tests.py` — Bullet Cluster, CMB, lensing, cluster dynamics, EFE, solar system
- `code/coma_cluster_corrected.py` — Corrected Coma cluster analysis, CMB quantitative analysis, EFE for wide binaries, falsification summary

All numbers cited in this report are from these scripts.
