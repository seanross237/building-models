# Meta-Learning Note — Exploration 003 (Strategy-002)

**Date:** 2026-03-27
**Task:** SED hydrogen — time to self-ionization vs angular momentum L

## What Worked Well

1. **The L-scan design** (four L values: 1.0, 0.9, 0.7, 0.5) was exactly right. The pattern was clear from just four points.

2. **20 trajectories per L value** gave reasonable statistics. Could use more for L=1.0 (only 2/20 ionized in 200 periods, giving a noisy estimate of long-run rate), but was good for L=0.5.

3. **Including Nieuwenhuizen's L_crit = 0.588ħ explicitly** in the goal meant the explorer tested above and below this threshold and confirmed it's real.

4. **Setting a 200-period cap** was appropriate for the first exploration. The explorer flagged that 200 periods is too short for L=1.0 — useful self-diagnosis.

## What Didn't Work Well

1. **τ value in goal was wrong** (1.57×10⁻⁵ vs physical 2.6×10⁻⁷ — factor ~60 off). The explorer flagged this in the report. This means T_ion values are ~60× too short compared to physical timescales. Should have double-checked the physical τ value before writing the goal.

   Lesson: For physical SED simulations (not normalized natural units), always verify τ against the exact formula τ = e²/(6πε₀m_ec³) in the correct unit system BEFORE writing the goal. Provide it in two unit systems (SI and atomic units) to reduce confusion.

2. **2D → 3D transition**: The goal correctly specified 3D simulation, but the explorer's initial simulation may have effectively been 2D (planar orbit in xy). True 3D should initialize z randomly to test stability to out-of-plane perturbations.

## Key Finding

The novel T_ion(L) measurements are the main contribution. The reconciliation of Cole & Zou (short-run optimism) with Nieuwenhuizen (long-run pessimism) is clean: both are right, just at different timescales.

## Scope Assessment

Scope was right. 4 L values × 20 trajectories was manageable. The 200-period cap was good for initial exploration.

## Recommendations

- For any follow-up: use physical τ = 2.6×10⁻⁷ in atomic units to match Nieuwenhuizen's timescales
- Extend L=1.0 run to 5,000+ periods to estimate 50% ionization time
- Scan L more finely in [0.5, 0.7] to locate the precise 50%-ionization threshold
