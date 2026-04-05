# Code for Exploration 001

## Key scripts (in order of importance)

- **`delta3_fast.py`** — Main computation. Pre-computes R¹_c and R²_c on a grid, then evaluates Σ₂ → Δ₃ for all scenarios. Produces `delta3_fast_results.npz` and `correction_grid.npz`.

- **`delta3_correct.py`** — GUE ground truth. Generates N=500 GUE matrices, computes Δ₃ directly from eigenvalues, and verifies the Σ₂ → Δ₃ formula. Produces `gue_delta3_ground_truth.npz`.

- **`verify_delta3_formula.py`** — Formula verification. Tests multiple Δ₃ formulas and identifies the correct one (Σ₂ route).

## Other scripts

- `compute_delta3.py` — Initial attempt (has the wrong Δ₃ formula, kept for reference)
- `delta3_final.py` — Full computation attempt (too slow due to mpmath, replaced by `delta3_fast.py`)

## Data files

- `gue_delta3_ground_truth.npz` — GUE Δ₃ values from random matrices
- `delta3_fast_results.npz` — Main results (GUE, +R¹_c, +R²_c, Full)
- `correction_grid.npz` — Pre-computed R¹_c, R²_c on x-grid

## Dependencies

- numpy, scipy, mpmath, sympy, pymupdf (for PDF extraction)
