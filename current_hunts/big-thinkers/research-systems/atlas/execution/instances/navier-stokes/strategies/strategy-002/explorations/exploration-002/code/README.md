# Exploration 002 Code

## Files

- **`proof_verification.py`** — Main verification script. Runs 8 parts:
  1. L⁴ bound verification (853 timesteps)
  2. Bound comparison (L⁴ vs Hölder vs Ladyzhenskaya)
  3. Enstrophy ODE comparison
  4. Individual proof step verification
  5. BGW 3D obstruction analysis
  6. Prodi-Serrin comparison
  7. Scaling verification (T_Lad × Re³)
  8. DNS stress test at Re=2000

- **`verify_S_L2_identity.py`** — Verifies ||S||_{L²} = ||ω||_{L²}/√2 to machine precision across 3 ICs × 2 resolutions.

- **`verify_bkm_proof.py`** — Original (pre-revision) verification script from the first pass. Uses the BGW approach (which was found to be flawed in 3D).

## Dependencies

- numpy
- The NS solver from `../../exploration-001/code/ns_solver.py`
- Results data from `../../exploration-001/results/all_results.json`

## Running

```bash
python proof_verification.py        # ~5 min (includes Re=2000 DNS stress test)
python verify_S_L2_identity.py      # ~30 sec
```
