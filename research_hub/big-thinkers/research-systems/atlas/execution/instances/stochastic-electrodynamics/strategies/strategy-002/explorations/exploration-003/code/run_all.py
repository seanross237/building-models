#!/usr/bin/env python3
"""
Run complete SED hydrogen ionization simulation for all L values.
Exploration 003 — Strategy 002

Runs L = 1.0, 0.9, 0.7, 0.5 with 20 trajectories each.
Saves results to JSON. Prints statistics and ASCII plots.
"""

import sys
import os
import time
import json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sed_hydrogen_sim import (
    run_full_sed, run_batch, run_zpf_only, run_pure_coulomb,
    generate_zpf, zpf_rms_theoretical, T_ORB, DT, TAU, OMEGA_MAX,
    ascii_plot_r
)

# ============================================================
# Configuration
# ============================================================
L_VALUES = [1.0, 0.9, 0.7, 0.5]
N_TRAJ = 20
N_PERIODS = 200          # cap at 200 orbital periods per trajectory
BASE_SEED = 42
DT_SIM = 0.01            # timestep

N_STEPS = int(N_PERIODS * T_ORB / DT_SIM) + 1

print(f"\n{'='*65}")
print(f"SED Hydrogen Self-Ionization — Exploration 003")
print(f"{'='*65}")
print(f"Parameters:")
print(f"  TAU       = {TAU:.2e} a.u.")
print(f"  omega_max = {OMEGA_MAX} a.u.")
print(f"  dt        = {DT_SIM} a.u.")
print(f"  T_cap     = {N_PERIODS} orbital periods = {N_PERIODS*T_ORB:.1f} a.u.")
print(f"  N_steps   = {N_STEPS:,} per trajectory")
print(f"  N_traj    = {N_TRAJ} per L value")
print(f"  ZPF RMS   = {zpf_rms_theoretical():.3f} a.u./component")
print(f"  Memory    ≈ {N_STEPS*6*8/1e6:.1f} MB per trajectory")
print()

# ============================================================
# Sanity Check: Pure Coulomb Orbit
# ============================================================
print("[SANITY CHECK] Pure Coulomb orbit (no ZPF, no radiation reaction)")
t_arr, r_arr, E_arr = run_pure_coulomb(n_periods=100)
r_std = np.std(r_arr)
E_std = np.std(E_arr)
print(f"  r: mean = {np.mean(r_arr):.8f} a0 (expected 1.0)")
print(f"  r: std  = {r_std:.2e} a0 (expected ~0)")
print(f"  E: mean = {np.mean(E_arr):.8f} a.u. (expected -0.5)")
print(f"  E: std  = {E_std:.2e} a.u. (expected ~0)")
sanity_result = {
    'r_mean': float(np.mean(r_arr)),
    'r_std': float(r_std),
    'E_mean': float(np.mean(E_arr)),
    'E_std': float(E_std),
}
print()

# ============================================================
# Sanity Check: ZPF Statistics
# ============================================================
print("[SANITY CHECK] ZPF noise statistics")
N_test = 200000
F_test, dF_test = generate_zpf(N_test, dt=DT_SIM, seed=0)
rms_measured = float(np.sqrt(np.mean(F_test**2)))
rms_theory = zpf_rms_theoretical()
print(f"  Measured per-component RMS: {rms_measured:.4f} a.u.")
print(f"  Theoretical:                {rms_theory:.4f} a.u.")
print(f"  Ratio: {rms_measured/rms_theory:.4f}")

# Low-frequency ZPF (omega < 1)
omega_test = 2*np.pi*np.fft.rfftfreq(N_test, d=DT_SIM)
# Theoretical sigma for low freq
import math
sigma_low_sq = TAU * 1.0**4 / (4 * math.pi)
sigma_low = math.sqrt(sigma_low_sq)
print(f"  Theoretical low-freq RMS (omega<1): {sigma_low:.4f} a.u.")
print()

# ============================================================
# ZPF only (no radiation reaction)
# ============================================================
print("[SANITY CHECK] ZPF only (no radiation reaction), L=1.0, 100 periods")
N_zpf_max = int(100 * T_ORB / DT_SIM) + 1
zpf_only_t_ions = []
for seed_k in range(5):
    t_ion_zpf, r_zpf = run_zpf_only(1.0, N_zpf_max, seed=seed_k*1000)
    if not np.isnan(t_ion_zpf):
        print(f"  seed={seed_k*1000}: ionized at {t_ion_zpf/T_ORB:.2f} periods")
        zpf_only_t_ions.append(t_ion_zpf/T_ORB)
    else:
        print(f"  seed={seed_k*1000}: NOT ionized (r={r_zpf:.3f})")
if not zpf_only_t_ions:
    print(f"  ZPF-only: no ionization in 5 trajectories within 100 periods")
    print(f"  (Unexpected if ZPF alone should ionize rapidly)")
print()

# ============================================================
# Main Simulation: All L Values
# ============================================================
all_stats = {}
all_traces = {}

total_t0 = time.time()

for L in L_VALUES:
    print(f"\n{'─'*65}")
    print(f"Running L = {L} ħ  ({N_TRAJ} trajectories, cap = {N_PERIODS} periods)")
    print(f"{'─'*65}")

    t_L_start = time.time()
    results, stats = run_batch(L, N_TRAJ, N_STEPS,
                               base_seed=BASE_SEED, verbose=True)
    t_L_elapsed = time.time() - t_L_start

    all_stats[L] = stats
    # Save first trajectory trace
    all_traces[L] = results[0][2]  # r_trace from first trajectory

    print(f"\n  --- Summary for L = {L} ħ ---")
    print(f"  Fraction ionized:  {stats['fraction_ionized']:.0%}  ({stats['n_ionized']}/{N_TRAJ})")
    if not np.isnan(stats['mean_T_ion_periods']):
        t_ions = stats['t_ions_periods']
        print(f"  Mean T_ion:        {stats['mean_T_ion_periods']:.1f} ± {stats['std_T_ion_periods']:.1f} periods")
        print(f"  Median T_ion:      {np.median(t_ions):.1f} periods")
        print(f"  Min T_ion:         {min(t_ions):.2f} periods")
        print(f"  Max T_ion:         {max(t_ions):.1f} periods")
    else:
        print(f"  No ionization within {N_PERIODS} periods")
    print(f"  Mean r (early):    {stats['mean_r_early']:.3f} a0")
    print(f"  Wall time:         {t_L_elapsed:.1f} s")

    # ASCII plot
    if all_traces[L]:
        ascii_plot_r(all_traces[L], title=f"r(t) for L={L} (trajectory 1, cap={N_PERIODS} periods)")

total_elapsed = time.time() - total_t0

# ============================================================
# Summary Table
# ============================================================
print(f"\n\n{'='*65}")
print(f"SUMMARY TABLE: T_ion vs Angular Momentum L")
print(f"{'='*65}")
print(f"{'L/hbar':>8}  {'Frac Ion':>10}  {'Mean T_ion':>12}  {'Std T_ion':>10}  {'<r>/a0':>8}")
print(f"{'─'*8}  {'─'*10}  {'─'*12}  {'─'*10}  {'─'*8}")
for L in L_VALUES:
    s = all_stats[L]
    frac = f"{s['fraction_ionized']:.0%}"
    mean_t = f"{s['mean_T_ion_periods']:.1f}" if not np.isnan(s['mean_T_ion_periods']) else ">200"
    std_t = f"{s['std_T_ion_periods']:.1f}" if not np.isnan(s['std_T_ion_periods']) else "—"
    r_early = f"{s['mean_r_early']:.3f}" if not np.isnan(s['mean_r_early']) else "—"
    print(f"  {L:6.1f}  {frac:>10}  {mean_t:>12}  {std_t:>10}  {r_early:>8}")

print(f"\nTotal wall time: {total_elapsed:.1f} s ({total_elapsed/60:.1f} min)")

# ============================================================
# Save Results to JSON
# ============================================================
# Convert numpy types to Python types for JSON serialization
def convert(obj):
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, list):
        return [convert(x) for x in obj]
    if isinstance(obj, dict):
        return {k: convert(v) for k, v in obj.items()}
    return obj

results_json = {
    'parameters': {
        'tau': TAU,
        'omega_max': OMEGA_MAX,
        'dt': DT_SIM,
        'n_periods_cap': N_PERIODS,
        'n_traj': N_TRAJ,
        'L_values': L_VALUES,
        'base_seed': BASE_SEED,
    },
    'sanity': convert(sanity_result),
    'zpf_rms': {'measured': rms_measured, 'theoretical': rms_theory},
    'results': {str(L): convert(all_stats[L]) for L in L_VALUES},
}

output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           'code', 'results.json')
with open(output_path, 'w') as f:
    json.dump(results_json, f, indent=2)
print(f"\nResults saved to: {output_path}")
print("\nDone.")
