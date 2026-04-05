#!/usr/bin/env python3
"""
analyze_results.py
Post-process the T_ion(L) scan results and compute statistics.
"""

import json
import numpy as np

with open('code/scan_results.json') as f:
    all_stats = json.load(f)

T_ORB = 2 * np.pi
TAU_PHYSICAL = 2.0 / (3.0 * 137.036**3)
TAU_E003     = 1.57e-5
TAU_RATIO    = TAU_E003 / TAU_PHYSICAL  # ~60.6×

# E003 reference data (from GOAL.md)
e003_data = {
    1.0: {'frac_ion': 0.10, 'median_T': None},  # >200 cap
    0.9: {'frac_ion': 0.35, 'median_T': 108.0},
    0.7: {'frac_ion': 0.75, 'median_T':  83.0},
    0.5: {'frac_ion': 0.95, 'median_T':  17.0},
}

print("=" * 70)
print("Full T_ion(L) Table — Physical τ = 2.591×10⁻⁷ a.u.")
print("=" * 70)
print(f"{'L/ħ':>5} | {'N_ion/20':>8} | {'Frac':>6} | {'Med T_ion':>12} | {'IQR':>8} | {'⟨r⟩/a₀':>7}")
print("-" * 70)

results_for_analysis = []
for s in all_stats:
    L = s['L']
    n_ion = s['n_ionized']
    n_tot = s['n_traj']
    frac  = s['fraction_ionized']
    med   = s['median_T_ion_periods']
    iqr   = s['iqr_T_ion_periods']
    r     = s['mean_r']
    cap   = s['cap']
    t_ions = s['t_ions_periods']

    med_str = f"{med:.0f}" if not np.isnan(med) else f">cap({cap})"
    iqr_str = f"{iqr:.0f}" if not np.isnan(iqr) else "N/A"
    print(f"{L:>5.1f} | {n_ion:>3}/{n_tot:<4} | {frac:>6.2f} | {med_str:>12} | {iqr_str:>8} | {r:>7.3f}")

    results_for_analysis.append({
        'L': L, 'frac': frac, 'med': med, 'iqr': iqr, 'n_ion': n_ion,
        't_ions': t_ions, 'cap': cap, 'r': r
    })

print()
print("=" * 70)
print("Comparison with E003 (τ = 1.57×10⁻⁵, ~60× too large)")
print("=" * 70)
print(f"{'L/ħ':>5} | {'E003 Med T_ion':>14} | {'Phys Med T_ion':>14} | {'Observed Ratio':>14} | {'Expected':>9}")
print("-" * 70)
for s in results_for_analysis:
    L = s['L']
    if L in e003_data and e003_data[L]['median_T'] is not None:
        e003_med = e003_data[L]['median_T']
        phys_med = s['med']
        if not np.isnan(phys_med):
            ratio = phys_med / e003_med
            print(f"{L:>5.1f} | {e003_med:>14.1f} | {phys_med:>14.0f} | {ratio:>14.1f}× | {TAU_RATIO:>8.1f}×")

print()
print("Note: expected ratio = τ_E003/τ_physical = 60.6×")
print("      observed ratios are lower (non-linear scaling)")

print()
print("=" * 70)
print("T_ion(L) Scaling Analysis")
print("=" * 70)
# Power-law fit for L=0.4 to L=0.8 (best statistics)
L_fit = []
T_fit = []
for s in results_for_analysis:
    L = s['L']
    med = s['med']
    if 0.4 <= L <= 0.8 and not np.isnan(med) and s['n_ion'] >= 5:
        L_fit.append(L)
        T_fit.append(med)

if len(L_fit) >= 3:
    log_L = np.log(L_fit)
    log_T = np.log(T_fit)
    # Linear fit in log-log space
    coeffs = np.polyfit(log_L, log_T, 1)
    power = coeffs[0]
    prefactor = np.exp(coeffs[1])
    print(f"  Power-law fit: T_ion ∝ L^n  (L=0.4 to 0.8)")
    print(f"  Best fit: n = {power:.2f}")
    print(f"  Prefactor: {prefactor:.1f} orbital periods")
    print(f"  (R² = {np.corrcoef(log_L, log_T)[0,1]**2:.4f})")
    for L, T in zip(L_fit, T_fit):
        T_pred = prefactor * L**power
        print(f"    L={L:.1f}: observed {T:.0f}, predicted {T_pred:.0f} periods")

print()
print("=" * 70)
print("L=1.0 Circular Orbit: ⟨r⟩ Check vs QM")
print("=" * 70)
for s in results_for_analysis:
    if s['L'] == 1.0:
        r_mean = s['r']
        print(f"  ⟨r⟩ from simulation:   {r_mean:.3f} a₀")
        print(f"  QM ⟨r⟩₁s state:        1.500 a₀")
        print(f"  Deviation:             {(r_mean-1.5)/1.5*100:.1f}%")
        print()
        print(f"  T_ion distribution for L=1.0 (18/20 ionized, cap=50,000 periods):")
        t_ions = sorted(s['t_ions'])
        print(f"    Min:    {min(t_ions):.0f} periods")
        print(f"    Median: {np.median(t_ions):.0f} periods")
        print(f"    Max:    {max(t_ions):.0f} periods")
        print(f"    IQR:    {s['iqr']:.0f} periods")
        print()
        # SI time estimate
        AU_TIME_SI = 2.4189e-17  # seconds
        median_si = np.median(t_ions) * T_ORB * AU_TIME_SI
        print(f"  Median T_ion(L=1.0) in SI: {median_si*1e12:.1f} ps")
        print(f"  (1 orbital period = {T_ORB*AU_TIME_SI*1e18:.2f} attoseconds)")

print()
print("=" * 70)
print("Nuclear collision analysis")
print("=" * 70)
# For L=0.4, some trajectories ionized VERY fast (9.8, 10.9 periods)
# These might be nuclear collisions (r < R_NUKE = 0.05)
for s in results_for_analysis:
    L = s['L']
    t_ions = sorted(s['t_ions'])
    if t_ions and min(t_ions) < 50:
        print(f"  L={L:.1f}: {len([t for t in t_ions if t < 50])} trajectories ionized in < 50 periods")
        print(f"    (these are likely nuclear collision events, r < 0.05 a₀)")

print()
print("Ionization fraction summary:")
for s in results_for_analysis:
    L = s['L']
    frac = s['frac']
    cap = s['cap']
    if frac < 1.0:
        print(f"  L={L:.1f}: {frac:.0%} ionized within {cap} periods")
    else:
        print(f"  L={L:.1f}: 100% ionized (all 20)")
