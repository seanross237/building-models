# Exploration 005 Code

## Files

### `classicality_budget_thermal.py`

Main computation script. Computes:
- Thermal entropy (S_eff) for 6 physical systems using actual thermodynamic formulas
  (not Bekenstein bounds)
- Bekenstein bounds for the same systems (for comparison)
- Classicality budgets R_delta <= S_eff/S_T - 1 for multiple S_T values
- Master comparison table
- Temperature sensitivity analysis for quantum computer

**Run:** `python classicality_budget_thermal.py`

**Requirements:** Python 3, numpy, scipy

**Output:** Prints all results to stdout. See REPORT.md for interpretation.

## Physical Formulas Used

- Thermal photon entropy: s = 16σT³/(3c) [Stefan-Boltzmann thermodynamics]
  Verified against Planck distribution formula to 10⁻⁹ relative error.
- Ideal gas entropy: Sackur-Tetrode + rotational (diatomic high-T limit)
- Liquid water entropy: NIST molar entropy (69.91 J/mol/K at 298K) + Cp correction
- Phonon entropy: Debye T³ law (valid for T << θ_D)
- Hawking temperature: T_H = ħc³/(8πGMk_B)
- Bekenstein bound: S_max = 2πRE/(ħc) × k_B

## Key Results (Quick Reference)

| System                     | S_eff (bits) | S_Bek (bits) | R_δ (S_T=1bit) | Constraining? |
|----------------------------|--------------|--------------|-----------------|---------------|
| Room photons (300K, 1m³)  | 2.85e+15     | 1.60e+43     | 2.85e+15        | NO            |
| Air molecules (STP, 1m³)   | 8.58e+26     | 1.92e+43     | 8.58e+26        | NO            |
| CMB (observable universe)  | 7.61e+89     | 3.40e+124    | 7.61e+89        | NO            |
| Brain water (310K, 1.4kg)  | 4.74e+26     | 2.47e+42     | 4.74e+26        | NO            |
| BH Hawking (solar mass)    | 2.67e-03     | 1.51e+77     | -0.997          | YES (zero!)   |
| QC phonons (10mK, 1cm³)   | 5.23e+09     | 2.58e+38     | 5.23e+09        | SOMEWHAT      |
