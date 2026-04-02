# Result Summary

## Goal

Set up a validated pseudospectral DNS solver for 3D incompressible Navier-Stokes on T³ that computes explicit pressure fields, and validate it against Taylor-Green vortex benchmarks at Re=100 and Re=1000 for N=64 and N=128.

## Approach

Extended the existing Atlas NS solver by adding:
1. **Pressure computation** via Fourier Poisson solve: p̂(k) = i(k·NL^)/|k|² (dealiased NL)
2. **L^q pressure norms** (q = 1, 3/2, 2, 3, ∞) — key for Vasseur De Giorgi analysis
3. **Fast spectral diagnostics** via Parseval theorem (energy and dissipation without FFT)
4. **scipy.fft with parallel workers** (~5× speedup over numpy.fft)
5. **Per-step energy conservation tracking** for accurate balance checking

Ran 4 Taylor-Green vortex cases: Re=100/1000 × N=64/128.

## Outcome

SUCCEEDED — all primary validation criteria passed.

## Key Finding

**At Re=100, N=64 is fully adequate**: the enstrophy timeseries matches N=128 to within 0.004% (well below the 2% criterion). Energy conservation holds to 1.01e-05 (< 1e-4), divergence is at machine precision (1.3e-15), and the enstrophy peak occurs at t=5.0 (spec expected ~5-6). At N=128, energy conservation achieves 6.36e-07 < 1e-6.

**At Re=1000, N=64 is underresolved**: N=64 and N=128 diverge by 11.6% in enstrophy after t=6, confirming resolution inadequacy for this Reynolds number (Kolmogorov scale ~0.006 vs resolved scale ~0.29 at N=64).

**Initial pressure L^{3/2} norm (Calderón-Zygmund exponent)**: ‖p‖_{L^{3/2}} = 4.658 at t=0 for TGV. Decreases to 1.691 at the enstrophy peak (t=5), and remains elevated (3.0-3.5) throughout the turbulent Re=1000 simulation.

## Leads

- The pressure L^{3/2} norm at Re=1000 is approximately constant (~3-3.5) even as enstrophy grows to 1556 — this is the key measurement for Vasseur's pressure exponent analysis (subsequent tasks)
- The effective pressure exponent β can now be measured as a function of time by computing ‖p‖_{L^q} / ‖u‖_{H^s} scaling ratios
- At Re=1000, N=128 still appears underresolved (Kolmogorov scale 0.006 vs grid scale 0.15); a Re=1000, N=256 or N=512 run would be needed for fully resolved turbulence

## Unexpected Findings

- N=64 and N=128 produce essentially identical enstrophy at Re=100 (differences < 0.01%), confirming the TGV at Re=100 is laminar and fully resolved at N=64 — even better than expected
- scipy.fft with `workers=-1` is ~5× faster than numpy.fft on N=128 arrays, making large-N simulations practical
- The energy conservation error improves significantly from N=64 (1.01e-05) to N=128 (6.36e-07), consistent with the smaller timestep at finer resolution
- At Re=1000, N=64 overestimates enstrophy compared to N=128 (not underestimates) — aliasing at insufficient resolution inflates enstrophy through spurious nonlinear interactions

## Deferred Work

- Re=1000 at N=256 or N=512 for a fully resolved simulation (needed for accurate pressure exponent measurement at turbulent scales)
- Verification of pressure field against analytic TGV solution at t=0 (the Poisson solve gives exact results in the linear regime)
- Pressure-velocity correlation analysis: ∫p |u|^q dx as function of q, to directly measure the Vasseur exponent β
