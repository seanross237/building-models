# Code Directory — Exploration 001: SED Double-Well Barrier Crossing

## Files

| Script | Purpose |
|--------|---------|
| `sanity_check_ho.py` | Verify SED harmonic oscillator gives var_x ≈ 0.500. Run this first. |
| `double_well_lam025.py` | Double-well simulation, λ=0.25 (V_barrier=1.0). Moderate barrier. |
| `double_well_lam010.py` | Double-well simulation, λ=0.10 (V_barrier=2.5). Deep barrier. |
| `double_well_lam100.py` | Double-well simulation, λ=1.0 (V_barrier=0.25). Shallow/over-barrier. |
| `wkb_rates.py` | Exact QM diagonalization + WKB action integral for all three λ values. |

## Run Order

```bash
python sanity_check_ho.py       # ~30s, verifies noise normalization
python wkb_rates.py             # ~2s, gets QM reference rates
python double_well_lam025.py    # ~7s, λ=0.25 (main result)
python double_well_lam010.py    # ~7s, λ=0.10 (deep barrier)
python double_well_lam100.py    # ~7s, λ=1.0 (over-barrier)
```

## Dependencies

Python 3 with: numpy, scipy (scipy.integrate, scipy.linalg)

## Key Parameters

- `ω₀=1.0`, `m=1.0`, `ħ=1.0`, `τ=0.001`
- `ω_max=10.0` (UV cutoff), `dt=0.05`, `N=200,000` steps per trajectory
- `N_traj=100` (50 for sanity check)
- Integrator: Symplectic Euler (Euler-Cromer)
- ZPF PSD: `S_F(ω) = 2τħω³/m` (one-sided)
- FFT amplitude: `A_k = sqrt(S_F(ω) × N / (2dt))`

## Key Results

| λ | V_barrier | Γ_SED (ω₀) | Γ_exact_QM (ω₀) | Ratio |
|---|-----------|------------|-----------------|-------|
| 0.25 | 1.0 | 0.0663±0.0035 | 0.05780 | **1.15** |
| 0.10 | 2.5 | 0.00790±0.00137 | 0.000428 | **18.5** |
| 1.0 | 0.25 | 0.2038±0.0047 | N/A (over-barrier) | — |
