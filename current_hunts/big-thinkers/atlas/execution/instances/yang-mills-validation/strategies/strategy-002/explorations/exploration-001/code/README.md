# Code — Exploration 001: λ_max Inequality Stress Test

Run all scripts from this directory with `/opt/homebrew/bin/python3`.

## Files

| Script | Purpose | Runtime |
|--------|---------|---------|
| `fast_hessian.py` | Core implementation: lattice, Wilson action, FD Hessian, B² formula Hessian. Stages 1 & 2. | ~7s/config (d=4) |
| `lattice_hessian.py` | Original (slower) implementation, kept for reference | — |
| `verify_flat.py` | Verifies flat-connection FD artifacts, near-identity transition, step-size dependence | ~3 min |
| `stage4_characterize.py` | Stage 4: C(Q) spectrum analysis, eigenvector alignment, summary table | ~1 min |
| `adversarial_search.py` | All adversarial strategies (gradient ascent, NM, hill climbing) | Long |
| `adversarial_focused.py` | Combined focused adversarial: d=2 gradient + d=4 hill climb + NM | ~90 min |
| `adversarial_quick.py` | Quick version with unbuffered output | ~60 min |

## Quick Reproduce

```bash
# Stage 1: Identity check (d=4)
python3 fast_hessian.py --stage 1 --L 2 --d 4 --beta 1.0

# Stage 2: 50 random configs
python3 fast_hessian.py --stage 2 --L 2 --d 4 --n_configs 50

# Structured adversarial (d=4)
python3 adversarial_search.py --strategy 2

# Full characterization
python3 stage4_characterize.py

# FD verification
python3 verify_flat.py
```

## Dependencies

- numpy (tested with 2.4.3)
- scipy (tested with 1.17.1)
