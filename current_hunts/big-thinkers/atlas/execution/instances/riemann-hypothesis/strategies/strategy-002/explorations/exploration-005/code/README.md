# Code — Exploration 005

## Scripts (run in order)

1. **`part_a_c1_rescore.py`** — Builds 5 N=500 C1 matrices with random phases, computes corrected pair correlation R₂(r) and spectral rigidity Δ₃(L). Outputs `part_a_results.json`.

2. **`save_part_a_data.py`** — Saves C1 eigenvalues and unfolded spectra as `part_a_data.npz` for reproducibility.

3. **`part_b_complete.py`** — Full Gauss prime sweep: 6 main primes + 41 fine-sweep primes. Saves `part_b_complete_results.json`, `part_b_data.npz` (main eigenvalues), `part_b_fine_data.npz` (β vs p for all 47 primes).

4. **`gauss_delta3.py`** — Computes Δ₃ spectral rigidity for Gauss matrices at 6 key primes (97, 499, 809, 997, 1801, 9973). Outputs `gauss_delta3_results.json`.

## Data Files (.npz)

- `part_a_data.npz` — C1 eigenvalues (5×500), unfolded spectra, von Mangoldt values
- `part_b_data.npz` — Gauss eigenvalues for main sweep primes
- `part_b_fine_data.npz` — β_Wigner vs p for all 47 primes tested

## Data Files (.json)

- `part_a_results.json` — Full Part A results (β, MRD, Δ₃, scorecard)
- `part_b_complete_results.json` — Full Part B results (main + fine sweep)
- `gauss_delta3_results.json` — Δ₃ values for Gauss matrices at key primes

## Older files (superseded)

- `part_b_gauss_sweep.py`, `part_b_gauss_sweep_v2.py` — Used 0-indexed construction (incorrect)
- `part_b_gauss_sweep_v3.py` — 1-indexed, used tiling artifact for N_REP=3. β values correct.
- `part_b_results.json`, `part_b_results_v2.json`, `part_b_results_v3.json`, `part_b_fine_sweep.json` — Superseded by `part_b_complete_results.json`

## Key Findings

- Part A: Pair correlation MRD=7.9% (PASS), Δ₃ saturation=0.285 (~50% of GUE)
- Part B: β peaks at p=809 (β=1.154), declines for large p. β→2 hypothesis REFUTED.
- NEW: Gauss Δ₃ saturation 0.415-0.559 — universally less rigid than C1 (0.285)

## Dependencies

- Python 3, numpy, scipy
- No SageMath or Lean required
