# Exploration 008: Code

All scripts require Python 3, NumPy, SciPy, and SymPy.

## Scripts

| Script | Run time | Description |
|--------|----------|-------------|
| `task1_pointwise_dual.py` | ~5s | LP-based pointwise dual with 1, 2, and 3 norms |
| `task2_divfree_primal.py` | ~30min | Heavy optimization on 32³ grid (not needed for main result) |
| `task2_fast_verification.py` | ~10min | Fast comparison on 16³ grid |
| `task3_constant_field_extremizer.py` | ~5s | **Core result** — constant field as extremizer |
| `task4_symbolic_verification.py` | ~2s | SymPy verification of β = 4/3 |
| `task5_degiorgi_truncation.py` | ~5s | Truncation analysis, Kato inequality |
| `task6_dns_comparison.py` | ~10s | Taylor-Green and DNS parameter comparison |

## Key result

The constant field u = (c, 0, 0) is div-free and achieves Chebyshev ratio → 1. Run `task3_constant_field_extremizer.py` for the complete proof.
