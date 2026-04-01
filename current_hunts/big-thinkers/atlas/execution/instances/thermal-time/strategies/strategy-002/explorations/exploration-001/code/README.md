# Code — Rindler Wedge Verification

## Dependencies

- Python 3.9+
- NumPy
- SciPy

## Files

### `rindler_verification.py` (main)
The main computation. Runs the full BW verification for N = 50, 100, 200:
- Builds lattice scalar field with Dirichlet BC
- Computes vacuum correlators and restricts to right half-lattice
- Extracts modular Hamiltonian via Williamson decomposition
- Computes three correlators: modular flow, full-H time evolution, and boost
- Checks BW profile, KMS condition, vacuum consistency
- Saves results to `results.json`

Run: `python3 rindler_verification.py`

### `entropy_check.py`
Extended entanglement entropy scaling analysis for N = 20..400:
- Verifies Calabrese-Cardy scaling S = (c/6) ln(N) + const
- Analyzes the modular spectrum in detail

Run: `python3 entropy_check.py`

## Output

`results.json`: Full results including correlator data, BW profiles, KMS check, and entropy values.
