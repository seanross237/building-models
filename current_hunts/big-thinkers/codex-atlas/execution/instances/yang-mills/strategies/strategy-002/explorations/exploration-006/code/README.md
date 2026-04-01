# Exploration 006: 4D Hessian Slack Verification + Worst-Case Search

## Overview

This directory contains code and results for measuring the SZZ Lemma 4.1 Hessian bound on 4D Yang-Mills lattice and searching for adversarial configurations.

## Files

### Code

- **`hessian_4d.py`** — Main 4D Hessian measurement code
  - Implements Lattice4D class with heat-bath MCMC sampling
  - Measures H_normalized = |HessS(v,v)| / (48β × |v|²)
  - Runs at β = 0.02, 0.1, 0.5, 1.0
  - 10 configurations × 5 tangent vectors per β
  - ~5-10 minutes runtime

- **`worst_case_search.py`** — Adversarial configuration search
  - Three strategies: aligned configs, gradient ascent, eigenvalue search
  - Tests at β=0.02
  - ~2 minutes runtime

### Results

- **`results_4d.json`** — Summary statistics for each β
  - Columns: beta, mean, std, max, min, median, avg_plaq, bound_factor, n_values
  - All four β values measured
  - max H_norm values are the key results

- **`worst_case_results.json`** — Worst-case max H_norm from each search strategy
  - aligned: 0.00480 (slack = 208×)
  - gradient_ascent: 0.00463 (slack = 216×)
  - eigenvalue_search: 0.00569 (slack = 176×)

### Logs

- **`hessian_4d_output.log`** — Full terminal output from hessian_4d.py
- **`worst_case_output.log`** — Full terminal output from worst_case_search.py

## Key Results Summary

### 4D Hessian Measurements

| β    | max H_norm | slack_factor | condition |
|------|------------|--------------|-----------|
| 0.02 | 0.00725    | 138×         | **below critical** β_c = 1/48 = 0.0208 |
| 0.1  | 0.00791    | 127×         | above critical |
| 0.5  | 0.02023    | 49×          | well above critical |
| 1.0  | 0.03452    | 29×          | deep in strong coupling |

### Worst-Case Search Results

**At β=0.02, overall max H_norm = 0.00569** (slack = 176×)

All adversarial strategies underperformed compared to random Gibbs configurations.

## How to Run

### Full 4D measurement:
```bash
python hessian_4d.py
```
Output: `results_4d.json`, `hessian_4d_output.log`

### Worst-case search:
```bash
python worst_case_search.py
```
Output: `worst_case_results.json`, `worst_case_output.log`

## Dependencies

- numpy
- json
- os

No external packages beyond numpy are required.

## Technical Details

### 4D Lattice Setup
- Dimensions: 4⁴ (L=4)
- SU(2) gauge theory
- Bound formula: H_norm = |HessS| / (8(d-1)N β |v|²) = |HessS| / (48β |v|²)
- Heat-bath: Kennedy-Pendleton sampling
- Thermalization: 500 sweeps before measurement

### Hessian Computation
- Finite-difference: [S(Q exp(εv)) - 2S(Q) + S(Q exp(-εv))] / ε²
- ε = 10⁻⁴
- Tangent vectors: random unit vectors in su(2) algebra

### Worst-Case Search
1. **Aligned configuration:** U_e = exp(iα_e σ₃), random α_e
2. **Gradient ascent:** Random perturbations toward increasing H_norm
3. **Eigenvalue search:** Power iteration probing Hessian structure

## Reproducibility

All computations are deterministic (seeded random numbers in hessian_4d.py).

To reproduce:
```bash
# For exact 4D results, set seed=42 in main() of hessian_4d.py
python hessian_4d.py

# For worst-case search, set seed=42 in main() of worst_case_search.py
python worst_case_search.py
```

## Comparison with E005 (3D Results)

| Dimension | β    | max H_norm | slack |
|-----------|------|------------|-------|
| 3D (E005) | 0.02 | 0.0224     | 45×   |
| 4D (E006) | 0.02 | 0.00725    | 138×  |

**Key finding:** 4D is ~3× tighter than 3D. Suggests plaquette cancellation improves with dimension.

---

**Generated:** 2026-03-27
**Author:** Math Explorer (Atlas mission: Yang-Mills)
