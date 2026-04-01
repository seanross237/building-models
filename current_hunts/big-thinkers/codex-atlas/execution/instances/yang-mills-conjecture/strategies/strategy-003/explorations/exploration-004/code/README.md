# Exploration 004: Code

## Files

- `hessian_core.py` — Core Hessian computation (lattice, plaquettes, analytical Hessian formula). Copied from E003 with additions.
- `adversarial_search.py` — Full adversarial search: random survey, structured configs, gradient descent with Hellmann-Feynman fast gradients.
- `best_config.npz` — Best config from run 1 (λ_min = -14.097, from perturbed anti-instanton)
- `best_config_optimized.npz` — Best config from GD on axes (0,0,2,1) anti-instanton (λ_min = -14.734)

## Key result

sup|λ_min| ≈ 14.73 (d=4, L=2, β=1, N=2). Achieved by GD-optimized anti-instanton with axes (0,0,2,1).

## Dependencies

Python 3 with numpy. No other dependencies.
