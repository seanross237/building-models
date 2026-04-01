# Exploration 003 Code

## Files

- `ns_solver.py` — Pseudospectral 3D NS solver on T^3. Copied from exploration 002.
- `slack_measurements.py` — 8 inequality bound/actual pairs + diagnostics. Copied from exploration 002.
- `initial_conditions.py` — Implements 5 ICs (TGV, ABC, random Gaussian, vortex tube, anti-parallel tubes) + parametric anti-parallel for adversarial search. All use Biot-Savart inversion from vorticity, with z-perturbation for tube ICs.
- `run_focused.py` — Main simulation runner. Runs 5 ICs at Re=100,500,1000 with N=64, peak-velocity normalized.
- `run_multi_ic.py` — Earlier version of multi-IC runner (used for preliminary/energy-normalized runs).
- `adversarial_search.py` — Grid search over tube parameters (d, sigma, delta, tilt, Gamma_ratio) at N=32, validates at N=64.

## How to Run

```bash
# Five-IC comparison
python run_focused.py

# Adversarial search
python adversarial_search.py
```

## Dependencies

- numpy (with FFT)
- scipy (optional, for adversarial optimization)
- Python 3.8+
