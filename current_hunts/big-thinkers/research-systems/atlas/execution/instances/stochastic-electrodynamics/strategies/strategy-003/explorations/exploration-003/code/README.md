# Code for Exploration 003 — 3D ZPF Correlator

## Files

- `compute_3d_correlator.py` — Main computation script
- `C_xx_3D_vs_1D.png` — Plot comparing 3D and 1D correlators

## Running

```bash
python3 compute_3d_correlator.py
```

Requires: numpy, scipy, matplotlib (python3 / homebrew python)

## What it computes

1. The analytic formula C_xx(d) = (3/2q³)[(q²-1)sin(q) + q cos(q)]
2. Direct numerical integration of I(q) = ∫_{-1}^{1} (1+u²) e^{iqu} du
3. Spherical Bessel function form: j₀(q) - (1/2) j₂(q)
4. Monte Carlo verification over N=500,000 random k-vector directions
5. Limiting cases: near-field (q≪1) and far-field (q≫1)
6. Comparison to 1D result cos(ω₀d/c)

## Key result

C_xx(d) ≠ 0 in 3D. The 3D orientational average does not eliminate SED correlations.
