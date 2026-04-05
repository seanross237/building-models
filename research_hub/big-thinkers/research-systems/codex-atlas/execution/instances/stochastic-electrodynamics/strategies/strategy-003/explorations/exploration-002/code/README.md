# Code README — Exploration 002

## Files

| File | Description |
|------|-------------|
| `integrate_chunk.c` | C implementation of RK4 Landau-Lifshitz integration inner loop |
| `libsed.so` | Compiled shared library (gcc -O3 -march=native -ffast-math) |
| `sed_physical_tau.py` | Main simulation driver: ZPF generation, ctypes interface, multiprocessing |
| `analyze_results.py` | Post-processing: statistics, power-law fit, comparison with E003 |
| `scan_results.json` | Raw results from the full T_ion(L) scan (all 140 trajectories) |

## How to Reproduce

### Compile the C library (if libsed.so is missing or stale)
```bash
gcc -O3 -march=native -ffast-math -shared -fPIC -o libsed.so integrate_chunk.c -lm
```

### Run sanity checks
```bash
python3 sed_physical_tau.py --sanity
```

### Run the full scan (all 7 L values × 20 trajectories)
```bash
python3 sed_physical_tau.py --scan --n_traj 20 --workers 10 --output scan_results.json
```

### Run a single L value
```bash
python3 sed_physical_tau.py --L 0.7 --n_traj 20 --cap 10000 --workers 10
```

### Reproduce the analysis
```bash
python3 analyze_results.py   # requires scan_results.json in current dir
```
(Run from the parent exploration directory: `cd exploration-002 && python3 code/analyze_results.py`)

## Physical Parameters
- τ = 2.591×10⁻⁷ a.u. = 2/(3 × 137.036³)  [physical radiation-reaction time]
- ω_max = 100 a.u.  [ZPF UV cutoff]
- dt = 0.01 a.u.    [timestep]
- T_orb = 2π a.u.   [n=1 Bohr orbital period]
- CHUNK_STEPS = 131,071 = 2^17 - 1 per chunk

## Dependencies
- Python 3.x, numpy
- gcc (for compilation)
- multiprocessing (stdlib)
- ctypes (stdlib)
