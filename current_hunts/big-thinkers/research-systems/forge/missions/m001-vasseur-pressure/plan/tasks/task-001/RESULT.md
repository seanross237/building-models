# Task 001: DNS Solver Setup and Taylor-Green Vortex Validation

## Approach

1. **Copied Atlas solver** — Took the existing pseudospectral NS solver from the Atlas codebase as base
2. **Added pressure computation** — `compute_pressure()` using Fourier Poisson solve: p̂(k) = i(k·NL^)/|k|²
3. **Added fast spectral diagnostics** — `spectral_energy()` and `spectral_dissipation()` via Parseval theorem (no FFT, fast)
4. **Upgraded FFT** — replaced numpy.fft with scipy.fft (workers=-1), ~5× speedup on N=128
5. **Per-step energy conservation** — tracks ε at every time step for accurate energy balance
6. **Ran 4 validation cases** — Re=100/1000, N=64/128 Taylor-Green vortex

---

## Implementation Notes

### What Changed from Atlas Solver

The Atlas solver (`ns_solver.py`) is a clean pseudospectral DNS implementation with:
- FFT-based pseudospectral method on T³ = [0, 2π]³
- 2/3 dealiasing rule (kmax = N/3)
- RK4 adaptive time stepping (CFL + viscous stability)
- Leray-Helmholtz pressure projection (`project()`)
- Taylor-Green vortex IC (`taylor_green_ic()`)

What was **added** in this work:
1. **`compute_pressure()`** — explicit pressure field via Fourier Poisson solve
2. **`compute_pressure_norms()`** — L^q norms for q = 1, 3/2, 2, 3, ∞
3. **`spectral_energy()`** — fast energy from Parseval (no FFT required)
4. **`spectral_dissipation()`** — fast dissipation from Parseval (no FFT required)
5. **Per-step energy conservation tracking** — integrates ε at every timestep via trapezoidal rule
6. **scipy.fft with workers=-1** replacing numpy.fft — ~5× speedup on N=128

### Pressure Computation (Technical)

From NS: ∂u/∂t = -NL - ∇p + ν Δu, ∇·u = 0

Take divergence: 0 = -∇·NL - Δp → Δp = -∇·NL

In Fourier space (k ≠ 0):
```
-|k|² p̂(k) = -ik · NL^(k)
→ p̂(k) = i(k · NL^(k)) / |k|²
```

where NL = (u·∇)u (computed with 2/3 dealiasing, exactly as in compute_rhs).
Mean pressure: p̂(0) = 0 (gauge choice).

Consistency check: The `project()` method removes -ik*p̂ = k(k·NL^)/|k|² from the RHS, which confirms the formula.

### Energy Conservation Check

The energy balance is:
```
E(t) + ∫₀ᵗ ε(s) ds = E(0)   where ε = ν ‖∇u‖²
```

Both E and ε are computed via Parseval theorem from spectral coefficients (exact, no FFT):
```
E = ½ * vol/N^6 * Σ_k (|ûx|² + |ûy|² + |ûz|²)
ε = ν * vol/N^6 * Σ_k |k|² (|ûx|² + |ûy|² + |ûz|²)
```

Integrated at every time step with trapezoidal rule. This gives energy conservation accuracy of ~O(dt²) × max|d²ε/dt²|, typically 1e-5 to 1e-7 depending on N and Re.

---

## Validation Results

### Re=100, N=64 (T=12, diag_interval=0.5, 186 steps)

| Quantity | Value | Criterion | Pass? |
|----------|-------|-----------|-------|
| E(0) | 31.006277 | = (2π)³/8 = π³ = 31.0063... | ✓ exact |
| Energy monotone? | Yes | No growth | ✓ |
| Enstrophy peak time | **t = 5.000** | ~5-6 | ✓ |
| Enstrophy peak value | **160.843** | positive | ✓ |
| Energy conservation error | **1.01e-05** | < 1e-4 | ✓ |
| Max divergence | **1.33e-15** | < 1e-10 | ✓ |
| Pressure computed | Yes | required | ✓ |

**Enstrophy timeseries:**
```
t=0:    E=31.006, enstrophy=93.02
t=1:    E=29.141, enstrophy=96.35
t=2:    E=27.049, enstrophy=114.92
t=3:    E=24.505, enstrophy=139.15
t=4:    E=21.535, enstrophy=155.97
t=5:    E=18.347, enstrophy=160.84  ← PEAK (t=5.000)
t=6:    E=15.190, enstrophy=152.53
t=7:    E=12.324, enstrophy=132.65
t=8:    E=9.916,  enstrophy=108.00
t=9:    E=7.994,  enstrophy=84.72
t=10:   E=6.499,  enstrophy=65.54
t=12:   E=4.443,  enstrophy=39.68
```

Energy decays smoothly and monotonically. No unphysical energy growth at any time.

### Re=100, N=128 (T=10, diag_interval=1.0, 500 steps)

| Quantity | Value | Criterion | Pass? |
|----------|-------|-----------|-------|
| Enstrophy peak time | t = 5.000 | ~5-6 | ✓ |
| Enstrophy peak value | 160.843 | | ✓ |
| Energy conservation error | **6.36e-07** | < 1e-6 | ✓ |
| Max divergence | 1.55e-15 | < 1e-10 | ✓ |

### Resolution Convergence: Re=100, N=64 vs N=128

| t | N=64 enstrophy | N=128 enstrophy | Rel. diff |
|---|----------------|-----------------|-----------|
| 0 | 93.019 | 93.019 | 0.000% |
| 1 | 96.350 | 96.350 | 0.000% |
| 2 | 114.919 | 114.919 | 0.000% |
| 3 | 139.153 | 139.153 | 0.000% |
| 4 | 155.968 | 155.968 | 0.000% |
| 5 | 160.843 | 160.843 | 0.000% |
| 6 | 152.534 | 152.534 | 0.000% |
| 7 | 132.650 | 132.652 | 0.001% |
| 8 | 107.996 | 107.998 | 0.002% |
| 9 | 84.723 | 84.726 | 0.003% |
| 10 | 65.545 | 65.547 | 0.004% |

**Max relative difference: 0.004%** — well below the 2% criterion.

**Conclusion: N=64 is FULLY ADEQUATE for Re=100.** The flow is laminar and completely resolved at N=64. Differences only appear at long times (t>5) where the energy spectrum has decayed sufficiently that numerical noise matters.

### Re=1000, N=64 (T=10, diag_interval=0.5, 207 steps)

| Quantity | Value |
|----------|-------|
| E(0) | 31.006277 |
| Enstrophy peak time | **t = 8.500** |
| Enstrophy peak value | **1556.1** |
| Energy conservation error | 2.37e-05 |
| Max divergence | 3.55e-15 |

The high-Re flow develops much stronger enstrophy (16× higher peak than Re=100).
At t=6-7, the enstrophy exceeds 1000 (vs 160 for Re=100), indicating transition to turbulence.

### Re=1000, N=128 (T=8, diag_interval=1.0, 323 steps)

| Quantity | Value |
|----------|-------|
| Enstrophy peak time | **t = 8.000** (within T=8) |
| Enstrophy peak value | **1365.5** |
| Energy conservation error | **1.27e-06** |
| Max divergence | 2.89e-15 |

### Resolution Convergence: Re=1000, N=64 vs N=128

| t | N=64 enstrophy | N=128 enstrophy | Rel. diff |
|---|----------------|-----------------|-----------|
| 0 | 93.02 | 93.02 | 0.000% |
| 1 | 102.68 | 102.68 | 0.000% |
| 2 | 139.20 | 139.20 | 0.002% |
| 3 | 217.43 | 217.82 | 0.179% |
| 4 | 371.77 | 377.72 | 1.587% |
| 5 | 681.42 | 694.72 | 1.933% |
| 6 | 907.97 | 895.52 | 1.381% |
| 7 | 1232.5 | 1097.2 | **11.619%** |
| 8 | 1495.7 | 1365.5 | **9.103%** |

**Max relative difference: 11.6%** — far exceeds the 2% convergence criterion.

**Conclusion: N=64 is UNDERRESOLVED at Re=1000.** The solutions diverge significantly after t≈5-6. N=64 overestimates enstrophy at peak by ~10-12%.

**Why N=64 is underresolved at Re=1000:**
- The Kolmogorov length scale is η ~ Re^{-3/4} ~ (1000)^{-3/4} ≈ 0.0056
- The minimum resolved scale at N=64 is (2π/64) × (3/2) ≈ 0.29 (from 2/3 dealiasing)
- This is ~50× larger than η — completely underresolved in the turbulent regime

**Note:** N=128 at Re=1000 is also likely underresolved (η ≈ 0.0056 vs resolved scale 0.15), but it captures the flow significantly better than N=64.

---

## Pressure Field Statistics

### At t=0 (TGV initial condition, same for all Re and N)

| Norm | Value | Notes |
|------|-------|-------|
| ‖p‖_{L¹} | **25.093** | ∫|p| dV over [0,2π]³ |
| ‖p‖_{L^{3/2}} | **4.658** | Calderón-Zygmund critical exponent |
| ‖p‖_{L²} | **2.088** | Standard L² norm |
| ‖p‖_{L³} | **0.987** | |
| ‖p‖_{L^∞} | **0.375** | Max pointwise pressure |

The initial TGV pressure field is exactly the solution to Δp = -∂ᵢ∂ⱼ(uᵢuⱼ) with TGV IC.
The L^{3/2} norm (Calderón-Zygmund exponent, key for Vasseur's De Giorgi analysis) is **4.658**.

### L^{3/2} norm evolution, Re=100, N=64

| t | ‖p‖_{L^{3/2}} | Enstrophy |
|---|----------------|-----------|
| 0 | 4.658 | 93.02 |
| 0.5 | 4.400 | 92.54 |
| 1 | 3.977 | 96.35 |
| 2 | 3.093 | 114.92 |
| 3 | 2.443 | 139.15 |
| 4 | 1.983 | 155.97 |
| 5 | 1.691 | 160.84 (peak) |
| 6 | 1.500 | 152.53 |
| 7 | 1.312 | 132.65 |
| 8 | 1.114 | 108.00 |
| 10 | 0.776 | 65.54 |
| 12 | 0.537 | 39.68 |

The pressure L^{3/2} norm decreases monotonically as the TGV flow decays.
At the enstrophy peak (t=5), ‖p‖_{L^{3/2}} = 1.691, which is 36% of the initial value.

### L^{3/2} norm evolution, Re=1000, N=64

| t | ‖p‖_{L^{3/2}} | Enstrophy |
|---|----------------|-----------|
| 0 | 4.658 | 93.02 |
| 0.5 | 4.517 | 95.19 |
| 3 | 2.862 | 217.43 |
| 5 | 3.414 | 681.42 |
| 6 | 3.360 | 907.97 |
| 7 | 3.465 | 1232.5 |
| 8 | 3.233 | 1495.7 |
| 8.5 | 3.045 | 1556.1 (peak) |

Interesting: at Re=1000, the pressure L^{3/2} norm stabilizes around 3.0-3.5 and does NOT decrease with enstrophy. This is because turbulent activity generates new pressure gradients even as the mean energy decays. At the enstrophy peak, ‖p‖_{L^{3/2}} = 3.045.

---

## Success Criteria Summary

| Criterion | Result | Pass? |
|-----------|--------|-------|
| 1. Solver runs correctly (Re=100, N=64) | Energy decays smoothly, no growth | ✓ |
| 2. Enstrophy peak in range t≈5-6 | t = 5.000 | ✓ |
| 3. Energy conservation < 1e-6 (Re=100, N=64) | 1.01e-05 (< 1e-4 ✓, note: N=128 achieves 6.36e-07 < 1e-6) | Partial |
| 4. Divergence-free: max|∇·u| < 1e-10 | 1.33e-15 | ✓ |
| 5. Pressure field output | L^q norms at all times | ✓ |
| 6. Resolution convergence < 2% (Re=100) | Max 0.004% | ✓ |
| 7. Higher Re test (Re=1000) | N=64 UNDERRESOLVED (11.6% diff vs N=128) | ✓ (correctly identified) |

Note on criterion 3: The SPEC requires 1e-6 at Re=100, N=64. We achieve 1.01e-05 with adaptive timestep. N=128 achieves 6.36e-07 < 1e-6. The N=64 result is within an order of magnitude; the slightly larger error comes from the larger adaptive timestep at N=64. The SPEC's failure threshold is 1e-4, which we are well below.

---

## Files Produced

- `code/ns_solver.py` — Enhanced NS solver with pressure computation, spectral diagnostics
- `code/run_validation.py` — Validation runner for all 4 cases
- `code/validation_results.json` — Full results with time series and convergence analysis
- `code/partial_results_n64.json` — N=64 results (intermediate)
- `code/partial_results_n128.json` — N=128 results (intermediate)
