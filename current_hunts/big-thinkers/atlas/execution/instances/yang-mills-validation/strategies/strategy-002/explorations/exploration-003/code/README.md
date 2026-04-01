# Exploration 003 Code

All scripts use `python3` with numpy and scipy. Run from the `code/` directory.

## Core
- `lattice_core.py` — Shared infrastructure: SU(2) operations, lattice class, Wilson action, FD Hessian, B² formula Hessian

## Perturbation Theory (Part 1)
- `part1_d2_only.py` — Full perturbation analysis at d=2 (20 directions, eigenstructure, second-order matrix)
- `part1_perturbation.py` — Perturbation analysis at d=2 and d=4
- `part1_d4_targeted.py` — Targeted d=4 line scans (8 directions)

## Line Scans & Gauge (Parts 2-3)
- `part2_gauge_and_scans.py` — Gauge orbit verification + detailed line scans (d=2,3,4)

## Gradient/Random Walk Ascent (Part 4)
- `part3_gradient_ascent.py` — Numerical gradient ascent (slow, d=2 only)
- `part4_fast_gradient_ascent.py` — Random walk + simulated annealing ascent (d=2)

## Proof Analysis (Part 5)
- `part5_proof_analysis.py` — D(Q) = H(I) - H(Q) Loewner order analysis
- `check_formula_d4.py` — Formula Hessian invariance under one-hot perturbations

## Verification
- `verify_counterexample.py` — Multi-h verification of d=3/d=4 one-hot counterexample
- `verify_d2_excess.py` — Multi-h verification of d=2 random walk excess

## Utilities
- `extract_summary.py` — Extract statistics from Part 1 d=2 results
