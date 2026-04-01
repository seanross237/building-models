# Code for Exploration 007

## Scripts

### desitter_acceleration.py
**Part 1**: De Sitter-relative acceleration computation.
- Symbolic derivation with Sympy showing Λ cancels
- Numerical verification for 3 test cases (galaxy star, solar system, deep MOND)
- Result: |a_dS_rel|/g_N = 1.0 to machine precision in all cases

### factor_sixth.py
**Part 2**: Factor of 1/6 = 1/(2π) origin analysis.
- Temperature formulas showing 2π cancels in T_U/T_dS ratio
- Verlinde area-volume entropy derivation
- 4 independent approaches failing to produce 1/(2π) internally
- Numerical comparison of a₀ values

### jacobson_rindler.py
**Part 3**: Jacobson local Rindler interpretation.
- Local Rindler surface gravity κ = g_N derivation
- Temperature comparison for 3 test cases
- Comparison table: dS-relative vs Jacobson approaches

### ngc3198_modified_a0.py
**Part 4 WRONG**: First attempt with incorrect v_obs = 120 km/s (that's NGC 2403).

### ngc3198_corrected.py
**Part 4 CORRECTED**: NGC 3198 with correct v_flat ≈ 150 km/s.
- Exponential disk (Freeman 1970) with Bessel functions
- Modified inertia formula: μ(a/a₀)×a = g_N, exact solution
- Chi-squared comparison for 4 models
- Best-fit a₀ scan over 3 decades
- Result: a₀_best = 1.175e-10 ≈ 0.98 × a₀_MOND

## Run Order
```
python code/desitter_acceleration.py
python code/factor_sixth.py
python code/jacobson_rindler.py
python code/ngc3198_corrected.py
```

## Dependencies
- numpy, sympy, scipy (standard Python scientific stack)
- scipy.special: iv, kv (modified Bessel functions for disk profile)
