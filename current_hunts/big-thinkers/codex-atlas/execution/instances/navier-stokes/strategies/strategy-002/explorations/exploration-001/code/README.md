# BKM Enstrophy Bypass — Code

## Files

- `ns_solver.py` — Pseudospectral DNS solver for 3D Navier-Stokes on T³ = [0, 2π]³. Includes Taylor-Green, Random Gaussian, and Anti-parallel tubes initial conditions.
- `run_cases.py` — Main runner. Executes all 13 cases (12 primary + 1 convergence check), saves results incrementally to `../results/`.
- `analyze_results.py` — Post-processing analysis. Generates tables, statistics, and the verdict.
- `bkm_comparison.py` — Earlier monolithic version (kept for reference).

## How to Run

```bash
# Run all cases (saves incrementally, skips already-computed cases)
python run_cases.py

# Analyze results
python analyze_results.py
```

## Dependencies

- Python 3, NumPy (FFT-based solver)
- No external libraries beyond standard NumPy

## Output

Results are saved to `../results/` as JSON files:
- `result_<IC>_Re<Re>_N<N>.json` — individual case results
- `all_results.json` — combined results
- `analysis.json` — post-processed analysis
