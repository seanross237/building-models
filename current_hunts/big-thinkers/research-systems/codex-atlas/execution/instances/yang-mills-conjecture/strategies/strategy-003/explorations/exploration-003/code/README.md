# Code for Exploration 003

All scripts run from this directory with `python <script>.py`.

## Core
- `hessian_core.py` — Lattice setup, Hessian computation, SU(2) utilities. Verified against E002.

## Proof Attempts
- `attempt1_gershgorin.py` — Gershgorin bound analysis. Result: FAILS (24 > 16 for d=4).
- `attempt2_perplaquette.py` — Per-plaquette quadratic form. Result: FAILS for d ≥ 3.
- `attempt3_fourier.py` — Fourier analysis at flat connections. Result: SUCCESS, gives K̂(k) formula.
- `analytical_proof.py` — D+C decomposition, cross-term kernel bound, operator norm analysis.

## Numerical Evidence
- `fast_targeted.py` — Key eigenvalue survey (1000 configs), perturbation analysis, mass gap thresholds. **Run this for all key results.**
- `gradient_ascent_and_perturbation.py` — Gradient ascent on λ_max (slow for d=4).
- `lambda_min_and_proof.py` — λ_min bounds and gradient descent (slow).
- `fast_survey.py` — Extended survey with D/C decomposition.

## Dependencies
- numpy (tested with 2.0.2)
- No scipy needed (custom SU(2) exp implementation)
