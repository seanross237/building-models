# Code for Exploration 002: Pressure Term Dissection

## Scripts

All scripts require Python 3 with `sympy` installed.

### `exponent_tracking.py`
Main exponent tracking script. Verifies:
- Sobolev embeddings in 3D
- Calderón-Zygmund estimates for pressure
- Hölder conjugate relationships
- Parabolic Sobolev (2/p + 3/q = 3/2) exponents
- The annotated inequality chain A → ... → β = 4/3
- NS scaling dimensions
- Drift-diffusion vs NS comparison table

### `recursion_power_counting.py`
Detailed power counting for the De Giorgi recursion:
- Computes U_k exponent σ(β) for each pressure exponent β
- Decomposes pressure into local + far-field contributions
- Shows local part has δ_local = 3/5 > 0 (superlinear — closes)
- Shows far-field has σ_far < 1 (sublinear — needs ε-regularity)
- Explains why β > 3/2 would give full regularity (bootstrap)

### `bogovskii_scaling.py`
Bogovskii corrector analysis:
- Computes W^{1,q} estimates for the corrector on thin annuli
- Shows C(Ω_k) ~ 2^k geometric blowup
- Demonstrates 2^{2k} compound growth (∇φ_k × Bogovskii constant)
- Shows corrector introduces sublinear U_k perturbation (best: 9/10 < 1)
- Concludes Bogovskii approach is not viable for De Giorgi iteration

## Running

```bash
python3 exponent_tracking.py
python3 recursion_power_counting.py
python3 bogovskii_scaling.py
```
