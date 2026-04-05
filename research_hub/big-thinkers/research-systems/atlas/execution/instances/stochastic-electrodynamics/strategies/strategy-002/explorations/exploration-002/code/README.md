# Code for Exploration 002 — Two SED Oscillators

## Files

- `sed_two_oscillators.py` — Main simulation script. Runs N_traj=200 trajectories × N=100,000 steps for d = 0, 0.1, 1.0, 10.0. Outputs C_xx, C_pp, and Bell-CHSH S_max for each separation. Run time: ~3-5 min on a modern laptop.
- `analytic_verify.py` — Analytical verification of C_xx(d) via numerical integration of the response function. Verifies C_xx ≈ cos(ω₀d/c) analytically. Run time: <1 min.
- `chsh_analysis.py` — Analysis of CHSH behavior for correlated Gaussian distributions. Uses the arcsin formula and grid-search over thresholds. Note: contains a prefactor bug (1/π instead of 1/(2π)) in var_x that does NOT affect normalized C_xx values.
- `results.json` — Raw results from main simulation.

## Run Order

```bash
python sed_two_oscillators.py    # main results
python analytic_verify.py        # confirm C_xx = cos(w0*d/c)
```

## Dependencies

numpy, scipy (standard scientific Python)

## Key Results

| d | C_xx | C_xx = cos(ω₀d/c) | S_max |
|---|------|---------------------|-------|
| 0.0 | 1.0000 | 1.0000 | 2.000 |
| 0.1 | 0.9948 | 0.9950 | 1.949 |
| 1.0 | 0.5384 | 0.5400 | 1.092 |
| 10.0 | -0.8328 | -0.8391 | 1.613 |

Individual variance var_x ≈ 0.50 ≈ ℏ/(2mω₀) [QM prediction]. Bell-CHSH S ≤ 2 always.
