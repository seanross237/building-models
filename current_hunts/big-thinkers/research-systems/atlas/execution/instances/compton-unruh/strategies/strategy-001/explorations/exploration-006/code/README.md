# Code for Exploration 006

## Scripts (run in order)

1. `fdt_analysis.py` — FDT theoretical analysis
   - Physical constants, temperature formulas
   - Classical FDT: chi''_dS = chi''_flat (key negative result)
   - Non-equilibrium Langevin scenario
   - Spectral density comparison
   - Output: `../fdt_analysis.png`

2. `rotation_curves.py` — Initial galaxy rotation curve fits (stellar disk only)
   - NGC 3198: M_disk=2e10 Msun, Rd=3.5 kpc
   - NGC 2403: M_disk=2.5e9 Msun, Rd=2.0 kpc (INCOMPLETE: missing gas)
   - Output: `../rotation_curves.png`

3. `rotation_curves_corrected.py` — Corrected fits with stellar+gas disks
   - NGC 3198: M_star=2e10, M_gas=1.2e10 (total=3.2e10 Msun)
   - NGC 2403: M_star=2.5e9, M_gas=7.5e9 (total=1.0e10 Msun, still slightly underfit)
   - Chi-squared scans over a0
   - Output: `../rotation_curves_corrected.png`

4. `ngc2403_masscheck.py` — Diagnostic for NGC 2403 mass
   - BTFR-consistent total mass: 1.85e10 Msun
   - Grid search over (Rd_gas, a0) parameter space
   - Final consistent result: chi2/dof ~ 0.88 (MOND), 0.52 (Verlinde), 140 (cH0)

## Dependencies
- Python 3.x
- numpy, scipy, matplotlib
- scipy.special (BesselI, BesselK for exponential disk)
- scipy.optimize (minimize_scalar for best-fit a0)

## Key Results
- Standard FDT gives chi''_dS/chi''_flat = 1.000000 (no modification to inertia)
- cH0 model fails badly: chi2/dof ~ 132-140 for both galaxies
- Verlinde (cH0/6) fits well: chi2/dof ~ 1.2-0.5 for both galaxies
- Best-fit a0 clusters near 0.7-1.0 x a0_MOND for both galaxies
