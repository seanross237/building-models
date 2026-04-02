# Exploration 007 Code

## Files

- `beltrami_lamb_v3.py` — Final computation (correct sign convention). Run: `python beltrami_lamb_v3.py`
- `beltrami_lamb_v2.py` — Intermediate version (correct decomposition, wrong sign)
- `beltrami_lamb.py` — Initial version (wrong decomposition + wrong sign)
- `results_v3.json` — Final results (use this)
- `results_v2.json` — Intermediate results (sign error)
- `results.json` — Initial results (multiple errors)

## Dependencies

- numpy, scipy (standard)
- NS solver from exploration-002: `../exploration-002/code/ns_solver.py`

## Key fix (v2→v3)

The pressure Poisson solve had a missing minus sign:
- Wrong: `p_hat = +k_i k_j FFT(u_iu_j) / K^2` (gives P = -p)
- Correct: `p_hat = -k_i k_j FFT(u_iu_j) / K^2` (gives P = p)

This was caught by the sanity check: for exact Beltrami flow at t=0, the remainder fraction should be ~0 (was ~2.0 with wrong sign).
