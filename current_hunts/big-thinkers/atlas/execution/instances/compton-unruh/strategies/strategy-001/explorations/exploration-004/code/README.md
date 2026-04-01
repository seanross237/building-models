# Exploration 004 — Code

## Scripts

- `part1_wightman_analysis.py` — Wightman function forms, spectral density comparison, temperature crossover analysis. Produces plots 1-3.
- `part2_radiation_reaction.py` — Radiation reaction force analysis, three approaches (naive entropic, excess temperature, ratio), MOND comparison. Produces plots 4-5.
- `part3_rotation_curves.py` — Modified equation of motion, galaxy rotation curves, BTFR, solar system consistency. Produces plots 6-8.

## Dependencies

Python 3 with: numpy, scipy, matplotlib

## Run Order

Scripts are independent; run in any order. Each produces its own plots and console output.

```
python part1_wightman_analysis.py
python part2_radiation_reaction.py
python part3_rotation_curves.py
```

## Outputs

- `plot1_spectral_density_comparison.png` — Planckian spectra at several accelerations (Rindler vs dS)
- `plot2_temperature_crossover.png` — T_U vs T_dS and their ratio
- `plot3_wightman_comparison.png` — |G+(s)| for Rindler vs dS at 4 accelerations
- `plot4_force_law_comparison.png` — Newton vs MOND vs naive dS force law
- `plot5_all_force_laws.png` — All force laws including ratio model
- `plot6_inertial_mass_ratio.png` — mu(a) for different a0 values
- `plot7_rotation_curves.png` — Galaxy rotation curves
- `plot8_tully_fisher.png` — Baryonic Tully-Fisher relation
