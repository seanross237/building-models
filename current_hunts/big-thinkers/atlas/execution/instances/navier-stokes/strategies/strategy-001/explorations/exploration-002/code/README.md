# Code for Exploration 002: NS Inequality Slack Measurements

## Files

- `ns_solver.py` — Pseudospectral DNS solver for 3D incompressible Navier-Stokes on T³
- `slack_measurements.py` — Measurement infrastructure: 8 bound/actual function pairs, extended diagnostics, sharp constants, validation tests
- `run_simulations.py` — Simulation runner with Taylor-Green vortex IC, adaptive time stepping, diagnostic sampling
- `compile_results.py` — Combined analysis: Slack Atlas Table, trend analysis, empirical constants

## Quick Start

```bash
# Validate measurement infrastructure
python slack_measurements.py

# Run all Reynolds numbers (N=64, T=5)
python run_simulations.py --re 100 500 1000 5000

# Run convergence check (N=128)
python run_simulations.py --re 100 --N 128 --T 3.0

# Combined analysis
python compile_results.py
```

## Dependencies

- Python 3.8+
- NumPy (FFT-based spectral solver)
- No other dependencies
