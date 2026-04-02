---
topic: T_U/T_dS modified inertia is observationally falsified by gravitational lensing at cluster scales
confidence: verified
date: 2026-03-27
source: "compton-unruh strategy-001 exploration-008"
---

## Finding

The T_U/T_dS modified inertia model is **observationally falsified** by gravitational lensing data.
This failure is intrinsic to the modified-inertia framework, not a tunable parameter issue: modified
inertia changes m_i but leaves the gravitational potential Φ unchanged, so photon geodesics are
unaffected by the modification. Cluster lensing masses are 5–10× above baryonic masses in all
well-studied systems — a factor-of-3 discrepancy in arc radii, far beyond any observational
uncertainty.

## Why Modified Inertia Cannot Fix Lensing

In the T_U/T_dS model, the equation of motion is:

    m_i × a = m × g_N      →     m × μ(g_N/a₀) × a = m × g_N

The gravitational potential Φ still satisfies the **standard Poisson equation**:

    ∇²Φ = 4πG × ρ_baryon    (unmodified)

Photons travel on geodesics of the metric, determined entirely by Φ. Therefore:
- Lensing convergence κ = Σ_baryon / Σ_cr  (standard formula)
- Einstein radius θ_E = √(4GM_baryon/c² × D_LS/(D_L D_S))  (baryonic mass only)
- Lensing mass = baryonic mass  (no dark matter contribution, no MOND enhancement)

This is an inescapable structural consequence of modified inertia. No choice of a₀ or μ function
fixes it.

## The Bullet Cluster (1E 0657-558) — CRITICAL FAILURE [COMPUTED]

The Bullet Cluster is the canonical cluster collision test. Two clusters collided at ~3600 km/s. Hot
X-ray gas (86% of baryonic mass) was slowed by ram pressure and lags behind the stellar component.
Lensing peaks are observed at the **stellar** locations, NOT the gas.

**Baryonic mass:**
- Hot X-ray gas: 3.0×10¹³ M_sun (86%)
- Stellar mass: 5.0×10¹² M_sun (14%)
- Total baryonic: 3.5×10¹³ M_sun

**Observed lensing mass (Clowe et al. 2006):** 2.0×10¹⁴ M_sun

**Failure 1 (amplitude):** Modified inertia predicts lensing mass = 3.5×10¹³ M_sun. Observed =
2.0×10¹⁴ M_sun. **Discrepancy: 5.7×.** (Einstein radii would be off by √5.7 ≈ 2.4×.)

**Failure 2 (morphology):** Modified inertia predicts lensing peaks at the gas location (86% of
baryons). Observed: lensing peaks at the stellar component, spatially separated from the gas by
720 kpc projected. Modified inertia predicts the **opposite morphology** from what is observed.

## General Cluster Lensing — CRITICAL FAILURE [COMPUTED]

For typical strong-lensing clusters:
- Observed lensing mass: ~10¹⁵ M_sun
- Baryonic mass: ~10¹⁴ M_sun
- Ratio: 10:1

Modified inertia predicts lensing mass 10× too low. Arc radii would be underestimated by
a factor of √10 ≈ 3.2. For El Gordo cluster (ACT-CL J0102-4915, z=0.87):
- Baryonic mass: ~2×10¹³ M_sun
- Lensing mass: ~2×10¹⁴ M_sun
- Factor: 10×

## Contrast With Modified Gravity (MOND/AQUAL)

Modified gravity modifies the Poisson equation:

    ∇·[μ(|∇Φ|/a₀) × ∇Φ] = 4πG × ρ_baryon

This creates an enhanced potential, so both dynamics AND lensing are boosted. For the Bullet Cluster
at r = 0.5 Mpc:
- g_N = 1.95×10⁻¹¹ m/s², x = g_N/a₀ = 0.18, μ = 0.176
- MOND effective lensing mass = M_baryon/μ ≈ 2.0×10¹⁴ M_sun  (matches Clowe et al.!)

MOND gravity can explain the **amplitude** of Bullet Cluster lensing (though morphology still fails
because lensing follows total baryon distribution, not just stars). Modified inertia **cannot** explain
either amplitude OR morphology.

**Modified inertia is strictly worse than modified gravity for cluster lensing:** it fails both the
amplitude (5.7× deficit) AND the morphology.

## Verdict

**OBSERVATIONALLY FALSIFIED.** This is not a marginal result. The lensing failure is:
1. **Intrinsic** — follows from the definition of modified inertia, not a tunable parameter
2. **Quantitative** — factor 5–10× in mass, factor ~3× in arc radii
3. **Double** — both amplitude and morphology fail simultaneously
4. **Comprehensive** — applies to every well-studied galaxy cluster

To rescue the observational predictions, the model would need to be reformulated as a modified
**gravity** theory (modifying the Poisson equation), not modified inertia.

## Relationship to Other Entries

- `tu-tds-viability-scorecard.md` — full model assessment
- `mond-phenomenology-coincidences.md` — background on MOND cluster failures (MOND gravity inherits
  different, milder failure)
- `verlinde-emergent-gravity-a0.md` — Verlinde's modified-gravity reformulation which bypasses this
