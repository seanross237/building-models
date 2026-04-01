# Exploration 001 — Code

All scripts require Python 3 with numpy, scipy, matplotlib. No other dependencies.

## Scripts

| File | Description | Run |
|------|-------------|-----|
| `part1_scales.py` | Computes all physical scales (Compton, Unruh, de Sitter, MOND) | `python part1_scales.py` |
| `part2_dimensional_analysis.py` | Dimensional analysis: matching conditions, mass dependence, de Sitter modification | `python part2_dimensional_analysis.py` |
| `part3_detector_response.py` | Unruh-DeWitt detector response analysis + Plots 4 & 5 | `python part3_detector_response.py` |
| `part4_plots.py` | Generates Plots 1-3 (temperatures, energies, de Sitter comparison) | `python part4_plots.py` |

## Outputs

| File | Description |
|------|-------------|
| `plot1_temperatures.png` | T_U(a) and T_dS(a) vs acceleration, with T_GH floor |
| `plot2_energies.png` | E_U(a) vs E_C(proton), showing 43-order-of-magnitude gap |
| `plot3_deSitter_comparison.png` | De Sitter vs flat Unruh temperature in low-a regime |
| `plot4_detector_response.png` | Detector response R(E) for various accelerations |
| `plot5_response_vs_acceleration.png` | R(m_p c^2, a) vs a — no peak or resonance |

## Run Order

Scripts are independent. Run in any order.
