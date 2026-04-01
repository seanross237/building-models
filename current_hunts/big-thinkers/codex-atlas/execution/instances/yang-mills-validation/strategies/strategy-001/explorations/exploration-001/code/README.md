# Code for Exploration 001

All scripts run with Python 3 + NumPy. Do NOT import scipy (NumPy 2.0 incompatibility).

## Run Order

1. `stage0_sanity_check.py` — Convention check, builds M matrix saved to /tmp/
2. `stage1_szz_framework.py` — Analytical HessS derivation (depends on M matrix from stage0)
3. `stage2_fourier_analysis.py` — Fourier analysis at Q=I (depends on M matrix)
4. `stage4_random_Q_verification.py` — Random Q sampling (standalone, computes own Hessians)
5. `stage4b_saturation_analysis.py` — CS saturation at U=iσ₃, FD verification (standalone)
6. `stage5_comparison.py` — Summary comparison (standalone, no dependencies)

## Key Functions

`adjoint_rep(g)`: Computes 3×3 adjoint representation of g ∈ SU(2)
`compute_hessian(U_links, ...)`: Builds 192×192 Hessian matrix from formula HessS = (β/2N)Σ|B_□|²
`random_su2()`: Haar-distributed random SU(2) matrix via quaternion parameterization

## Key Results

| Script | Key Result |
|--------|------------|
| stage0 | λ_max(H(I)) = 4β, convention SZZ/S2 confirmed |
| stage1 | CS bound gives HessS ≤ 6β|v|² → β < 1/6 |
| stage2 | Staggered mode v_{x,μ} = (-1)^(|x|+μ) maximizes at Q=I |
| stage4 | Random Q: max observed H_norm/β = 4.25 (well below 6) |
| stage4b | U_all=iσ₃: λ_max = 6β exactly, all 96 plaquettes CS-tight |
| stage5 | Independent derivation confirms β < 1/6 with no errors |

## Saved Data

After running stages, /tmp/ contains:
- `M_matrix.npy`: 64×64 oriented plaquette adjacency matrix at Q=I
- `evals_M.npy`: Eigenvalues of M
- `all_h_norms.npy`: H_norm/β for 200 random samples
- `U_isig3.npy`: The U_all=iσ₃ extremal configuration
- `v_extremal.npy`: The extremal eigenvector (achieves λ=6β)
- `H_isig3.npy`: Full 192×192 Hessian at U_all=iσ₃
