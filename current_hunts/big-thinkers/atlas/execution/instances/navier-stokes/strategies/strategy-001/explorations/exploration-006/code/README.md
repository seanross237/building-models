# Exploration 006: Code

## Files

- `spectral_ladyzhenskaya_v2.py` — Main computation: effective Ladyzhenskaya constants for band-limited, power-law, div-free, and NS spectral profiles. Run: `python3 spectral_ladyzhenskaya_v2.py`

- `analytical_ceff.py` — Analytical computation of C_eff in the Gaussian regime using numerical integration. Computes scaling law C_eff ~ Re^{-3/8}. Run: `python3 analytical_ceff.py`

- `scaling_analysis.py` — Detailed scaling analysis: asymptotic formula verification, provable bound analysis. Run: `python3 scaling_analysis.py`

- `littlewood_paley.py` — Littlewood-Paley decomposition analysis: diagonal vs cross-term contributions to ||f||⁴_{L⁴}. Run: `python3 littlewood_paley.py`

- `verify_divfree.py` — Verification of the divergence-free reduction factor across multiple k₀ values.

## Dependencies

- numpy, scipy (standard)
- No external data needed; all fields are generated synthetically

## Key Results

The main outputs are printed to stdout and saved to `results_partB_v2.json`. The analytical results are in the stdout of `analytical_ceff.py` and `scaling_analysis.py`.
