# Code for Exploration 003: Experimental Test Proposal

## Files

- `experimental_test.py` — Main computation script. No dependencies beyond numpy/scipy.

## Running

```bash
python3 experimental_test.py
```

Output is printed to stdout. All computed values in REPORT.md come from this script.

## Dependencies

- Python 3.8+
- numpy
- scipy

## What it computes

1. S_eff (actual thermodynamic entropy) for 8 experimental systems using:
   - Photon gas formula (Stefan-Boltzmann)
   - 1D phonon gas (numerical Bose-Einstein sum with UV cutoff)
   - Debye solid phonon formula
2. S_Bek (Bekenstein entropy bound)
3. R_max = S_eff/S_T - 1 (classicality budget, delta=0, S_T=1 bit)
4. Temperature and length scans for BEC, and n̄ scans for ion trap
5. Comparison table and key findings summary

## Key results reproduced

- BH horizon: S_eff = 2.672e-3 bits, R_max = -0.997 [matches Exploration 005]
- BEC (L=100μm, T=50nK): S_eff = 474.9 bits, R_max = 473.9 [CONSTRAINED]
- 50-ion trap (n̄=0.1): S_eff = 72.5 bits, R_max = 71.5 [CONSTRAINED]
- 20-ion trap (n̄=0.01): S_eff = 4.86 bits, R_max = 3.86 [TIGHT]
- Nanodot 10nm at 4K: S_eff = 10.25 bits, R_max = 9.25 [TIGHT]
- Inflation (H=1e13 GeV): S_eff = 0.021 bits, R_max = -0.979 [FORBIDDEN]
