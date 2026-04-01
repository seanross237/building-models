# Exploration 005 Summary: Operationally Relevant Classicality Budget

## Goal

Replace the Bekenstein bound with actual thermodynamic/statistical mechanical entropy
in the classicality budget formula R_δ ≤ S_eff/S_T − 1. Compute for 6 systems and
determine: does the budget become constraining with realistic entropy?

## What Was Tried

Wrote a Python script (`code/classicality_budget_thermal.py`) computing:
- S_eff from first-principles thermodynamics formulas for all 6 systems:
  (1) Room photons: Stefan-Boltzmann photon entropy
  (2) Air: Sackur-Tetrode + rotational (diatomic gas)
  (3) CMB: blackbody photon entropy in observable universe volume
  (4) Brain: liquid water molar entropy (NIST tabulated)
  (5) BH horizon: Hawking photon entropy near Schwarzschild radius
  (6) Quantum computer: thermal photons + Debye phonon entropy at 10mK

Cross-verified formulas (two independent derivations for photon entropy agree to 10⁻⁹),
compared to literature values (CMB cross-checked against Penrose's 10⁸⁸ figure).

## Outcome: SUCCEEDED — with dramatic results for one system

The computation ran successfully for all 6 systems.

**Key finding: The budget becomes constraining for EXACTLY ONE system — the black hole
horizon environment (Hawking radiation).**

## Verification Scorecard

- **[COMPUTED]**: 12 entropy values, 24 classicality budget values
- **[CHECKED]**: 3 (photon formula cross-check, CMB vs. literature, BH entropy vs. Exploration 002)
- **[CONJECTURED]**: 2 (BH information paradox interpretation, Planck-mass BH edge case)
- **[VERIFIED]**: 1 (two-formula photon entropy agreement to 10⁻⁹)

## Master Results Table

| System                     | S_eff (bits) | S_Bek (bits) | R_δ (S_T=1) | Constraining? |
|----------------------------|--------------|--------------|-------------|---------------|
| Room photons (300K, 1m³)  | 2.85 × 10¹⁵ | 1.60 × 10⁴³ | 2.85 × 10¹⁵ | NO            |
| Air molecules (STP, 1m³)   | 8.58 × 10²⁶ | 1.92 × 10⁴³ | 8.58 × 10²⁶ | NO            |
| CMB (observable universe)  | 7.61 × 10⁸⁹ | 3.40 × 10¹²⁴| 7.61 × 10⁸⁹ | NO            |
| Brain water (310K, 1.4kg)  | 4.74 × 10²⁶ | 2.47 × 10⁴² | 4.74 × 10²⁶ | NO            |
| BH horizon (solar, Hawking)| 2.67 × 10⁻³ | 1.51 × 10⁷⁷ | **−0.997**  | **YES — zero**|
| QC phonons (10mK, 1cm³)   | 5.23 × 10⁹  | 2.58 × 10³⁸ | 5.23 × 10⁹  | Somewhat      |

## Key Takeaway

**The Bekenstein bound overestimates actual encoding capacity by 16–80 orders of magnitude
for these systems. For all non-gravitational systems, the realistic classicality budget
is non-constraining for any physically realizable fact.**

The exception is the black hole horizon: S_Hawking ≈ 0.003 bits in the near-horizon
region of a solar-mass BH. The Hawking photon wavelength (~0.3 AU) vastly exceeds the
Schwarzschild radius (2.95 km), so there is typically less than 10⁻³ photons present
near the horizon. R_δ ≈ −1 for all fact sizes — no classical reality via quantum Darwinism
is possible based on Hawking radiation alone.

For the quantum computer (10mK, Si substrate), the phonon entropy (5.23×10⁹ bits)
dominates over photon entropy (10⁻⁴ bits) by 13 orders of magnitude. For the full
1000-qubit register (S_T = 1000 bits), R_δ = 5×10⁶ — not constraining, but 29 orders
of magnitude below the Bekenstein estimate.

## Leads Worth Pursuing

1. **Planck-mass BH transition**: For BHs lighter than some crossover mass, T_H becomes
   high enough that λ_photon ~ r_s, and S_Hawking might exceed S_T for modest facts.
   Compute the crossover mass where S_Hawking(r_s sphere) = 1 bit. This is likely near
   M ~ 10⁻⁸ kg (Planck mass), where Hawking effects are extreme.

2. **BH evaporation endpoint**: As a BH evaporates from M_sun to M_Planck, at what
   mass does the Hawking environment first support a single-bit redundant copy?
   This would define a "classicality onset mass" for BH evaporation.

3. **Brain photon environment**: The EM photon field inside the brain (4.2×10¹² bits)
   gives R_δ ≈ 41 for the full neural state (10¹¹ bits). This is the most "interesting"
   non-BH result — it means the photon EM environment can support only ~41 independent
   verifications of the brain's full neural configuration. This deserves investigation:
   is the EM photon field the right environment for neural classicality? Or is it the
   molecular phonon bath (which is much larger)?

4. **Cryogenic QC phonon bath**: The Si phonon entropy at 10mK is 5.23×10⁹ bits in 1cm³.
   This is the dominant decoherence environment. What is the threshold temperature
   below which the phonon bath cannot support a single redundant copy of the 1000-qubit
   register? Computed: T_cross_phonon = 5.76×10⁻⁵ K — far below current technology.

## Unexpected Findings

1. **Air >> photons by 11 orders**: Air molecules carry ~300,000× more entropy than the
   photon field in the same volume at room temperature. For quantum Darwinism,
   molecules are a more powerful (if less elegant) encoding medium than photons.

2. **CMB factor-of-37 discrepancy with Penrose explained**: Penrose's 10⁸⁸ figure uses
   the Hubble sphere volume (c/H₀ ≈ 14 Gly); the full observable universe (46 Gly)
   is 37× larger by volume. Both are correct; my code uses the full observable universe.

3. **Phonons dominate QC entropy by 13 orders**: At 10mK, Si phonon entropy (5.23×10⁹ bits)
   dominates photon entropy (10⁻⁴ bits) by 13 orders of magnitude. The substrate phonon
   bath is the primary environmental encoding medium for quantum computers, not the
   photon field — which has implications for understanding QC decoherence dynamics.

## Proof Gaps / Formal Issues

- The "operationally relevant" entropy should ideally be the entropy accessible to
  environment fragments that scatter off the system, not the total environmental entropy.
  This exploration uses total thermodynamic entropy as a proxy. A tighter computation
  would restrict to the entropy of environment modes that actually couple to the system.

- For the QC phonon result, the Debye T³ law requires T << θ_D = 645K. At T = 10mK,
  T/θ_D = 1.6×10⁻⁵ << 1, so the approximation is excellent. [CHECKED]

## Computations Identified for Follow-Up

1. **BH mass crossover**: Find M_* such that S_Hawking(r_s sphere, T_H(M_*)) = 1 bit.
   ~5 lines of algebra; gives the "classicality onset mass" for BH evaporation.

2. **Phonon vs. photon decoherence coupling**: For each system, restrict to the entropy
   of the modes that actually couple to the system (e.g., long-wavelength photons for
   macroscopic objects, near-resonant phonons for qubits). This gives a "coupled mode
   entropy" that's a tighter lower bound on S_eff than total thermodynamic entropy.

3. **Full BH evaporation track**: Plot S_Hawking vs. M as BH evaporates from M_sun to
   M_Planck. At what mass does the budget first become non-constraining?
