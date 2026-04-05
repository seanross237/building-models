# Code Directory — Exploration 005

## Files

| File | Purpose | Run order |
|------|---------|-----------|
| `qm_rates_corrected.py` | QM tunneling rates for all λ via finite-difference Schrödinger | 1 |
| `sed_sim_corrected.py` | SED simulations with omega_max UV cutoff (matches E001) | 2 |
| `final_analysis.py` | Full statistical analysis, linear fit, R² | 3 |
| `sed_sim_all.py` | SED simulations WITHOUT omega_max (GOAL.md code, gives higher A) | optional |
| `analysis.py` | Analysis for the no-cutoff results | optional |
| `qm_rates.py` | Early QM script (wrong S_WKB — includes outer walls; see debug_swkb.py) | deprecated |
| `debug_swkb.py` | Diagnoses S_WKB computation — why outer wall contribution must be excluded | reference |
| `sanity_check_lam010.py` | Reproduces E001 λ=0.10 result at ~5% accuracy | reference |

## Key Results Files

- `results_corrected.json` — E005 SED simulation results (omega_max cutoff applied)
- `results_all_lambda.json` — E005 SED results without omega_max cutoff

## Dependencies

```
numpy, scipy, time, json
```

## Important Notes

1. **omega_max cutoff**: E001's actual code applies `ω ≤ 10` cutoff to ZPF PSD.
   The GOAL.md snippet incorrectly omits this. Use `sed_sim_corrected.py`.

2. **S_WKB**: Computed over central barrier only (inner turning points).
   The naive `np.trapz(sqrt(2*(V-E0)), x)` includes outer wall contributions and is wrong.
   See `debug_swkb.py` and `qm_rates_corrected.py` for the correct implementation.

3. **Reproducibility**: All simulations use fixed seeds (see JSON files).
   Re-running with different seeds gives ~5-15% variation in Gamma_SED for deep barriers.
