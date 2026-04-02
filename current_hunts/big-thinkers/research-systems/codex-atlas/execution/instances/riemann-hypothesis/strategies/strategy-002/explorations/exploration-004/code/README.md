# Code Directory — Exploration 004

## Files

### Primary analysis
- **berry_saturation_full.py** — Complete analysis: integral Δ₃, Berry formula variants, height bins
  - Run: `python3 berry_saturation_full.py`
  - Output: prints all results and saves `berry_saturation_results.npz`

### Supporting/diagnostic scripts
- **delta3_integral_correct.py** — Formula comparison: sum vs integral, Poisson/GUE tests
  - Run: `python3 delta3_integral_correct.py`
  - Tests both sum and integral formulas on Poisson, regular lattice, GUE, and zeta zeros

- **delta3_computation.py** — Initial (sum formula) computation, for reference
  - Uses the incorrect sum formula; yields values ~2× too small

### Data
- **berry_saturation_results.npz** — Main results (Δ₃ vs L, saturation levels, bin analysis)
- **delta3_both_formulas.npz** — Sum vs integral comparison for L=1-50
- **delta3_results.npz** — Sum formula results (reference only)
- **zeta_zeros_2000.npy** — Loaded from `../exploration-003/code/zeta_zeros_2000.npy`

## Key Finding

The correct Dyson-Mehta Δ₃ formula is the **integral** form:
```
Δ₃(L) = (1/L) × min_{a,b} ∫₀^L [N(x) - ax - b]² dx
```

NOT the sum form `(1/L) Σᵢ (kᵢ - a·xᵢ - b)²`. The sum formula gives ~2× too small.

The analytic implementation (delta3_integral):
```python
I0 = n * L - sum(ys)
I1 = n * L**2 / 2 - sum(ys**2) / 2
I2 = n**2 * L - sum((2k-1) * ys)  where k = 1..n
Δ₃ = (I2 - I0²/L - 12(I1 - I0*L/2)²/L³) / L
```

## Dependencies
- numpy, scipy
- zeta_zeros_2000.npy from exploration-003
