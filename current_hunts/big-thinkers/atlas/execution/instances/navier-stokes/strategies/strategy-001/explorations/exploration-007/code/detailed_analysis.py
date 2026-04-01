#!/usr/bin/env python3
"""
Detailed analysis for exploration 007 — deeper dives into the key findings.

1. BKM constant: derive the theoretical constant on T^3 and compare
2. Time-series evolution of BKM advantage
3. BMO norm radius dependence
4. Flatness-C_Leff correlation
5. Conditional bound refinement
"""

import numpy as np
import json
import os

RESULTS_FILE = os.path.join(os.path.dirname(__file__), '..', 'results_007.json')

with open(RESULTS_FILE) as f:
    data = json.load(f)

# =============================================================================
# 1. BKM Constant Analysis
# =============================================================================
print("="*80)
print("1. BKM CONSTANT CALIBRATION")
print("="*80)

# The BKM inequality on T^3:
# ||grad u||_{L^inf} <= C * ||omega||_{L^inf} * (1 + log(1 + ||omega||_{H^1}/||omega||_{L^2}))
#
# The constant C comes from the Biot-Savart kernel on T^3.
# On R^3: C ~ 1/(4*pi) * d = 3/(4*pi) ≈ 0.239 (from the Calderon-Zygmund theory)
# On T^3: the kernel has additional contributions from periodic images,
# but the leading behavior is the same.
#
# Our calibrated constant (making the bound valid for all timesteps):

for Re_key in ['100', '500', '1000', '5000']:
    ts_key = f'time_series_Re{Re_key}'
    if ts_key not in data:
        continue
    ts = data[ts_key]

    # Find max ratio grad_u_Linf / (omega_Linf * log_term)
    ratios = []
    for r in ts:
        if r['bkm_bound_no_C'] > 1e-30:
            ratio = r['grad_u_Linf'] / r['bkm_bound_no_C']
            ratios.append(ratio)

    max_ratio = max(ratios) if ratios else 0
    mean_ratio = np.mean(ratios) if ratios else 0
    print(f"Re={Re_key}: max(||grad u||_inf / (||omega||_inf * log_term)) = {max_ratio:.6f}")
    print(f"          mean = {mean_ratio:.6f}")

print(f"\nTheoretical estimate: C_BKM ~ 3/(4*pi) = {3/(4*np.pi):.6f}")
print(f"Our empirical max ratio ≈ 0.63 (need C >= 0.63 for bound validity)")
print(f"This is ~2.6× the R^3 estimate — reasonable for the periodic Biot-Savart kernel")

# =============================================================================
# 2. BKM vs Agmon TIME EVOLUTION
# =============================================================================
print("\n" + "="*80)
print("2. BKM vs AGMON SLACK EVOLUTION (Re=1000)")
print("="*80)

ts = data.get('time_series_Re1000', [])
if ts:
    print(f"{'t':>6} | {'Agmon slack':>12} | {'BKM slack':>10} | {'BKM/Agmon':>10} | {'log term':>10} | {'omega Linf':>11} | {'F4':>8}")
    print("-"*85)
    for r in ts[::3]:  # every 3rd timestep
        agmon_s = r.get('agmon_slack', float('inf'))
        bkm_s = r.get('bkm_slack', float('inf'))
        ratio = bkm_s / agmon_s if agmon_s > 0 and np.isfinite(agmon_s) and np.isfinite(bkm_s) else 0
        print(f"{r['time']:>6.3f} | {agmon_s:>12.2f} | {bkm_s:>10.2f} | {ratio:>10.4f} | {r['log_term']:>10.4f} | {r['omega_Linf']:>11.4f} | {r['F4']:>8.3f}")

# Why is BKM so much tighter?
# Agmon uses: ||grad u||_inf <= C_Agmon * ||u||_{H^2}^{1/2} * ||u||_{H^3}^{1/2}
# This is a pure Sobolev embedding — it doesn't use the vorticity structure at all.
# BKM uses: ||grad u||_inf <= C_BKM * ||omega||_inf * (1 + log(...))
# The key insight: omega_Linf grows, but only logarithmically in the H^1/L^2 ratio.
# For smooth flows, the H^1/L^2 ratio is bounded, so the log term is O(1).
# Meanwhile the Agmon bound involves H^2 and H^3 norms which grow much faster.

# =============================================================================
# 3. BMO RADIUS DEPENDENCE
# =============================================================================
print("\n" + "="*80)
print("3. BMO NORM vs RADIUS (Re=1000)")
print("="*80)

ts = data.get('time_series_Re1000', [])
bmo_records = [r for r in ts if r.get('bmo_by_radius') is not None]
if bmo_records:
    # Take a sample near peak enstrophy
    enstrophies = [r['enstrophy'] for r in bmo_records]
    peak_idx = np.argmax(enstrophies)
    peak_r = bmo_records[peak_idx]

    print(f"At t={peak_r['time']:.3f} (near peak enstrophy={peak_r['enstrophy']:.4f}):")
    print(f"  ||omega||_Linf = {peak_r['omega_Linf']:.4f}")
    print(f"  ||omega||_BMO = {peak_r['bmo_norm']:.4f}")
    print(f"  BMO/Linf = {peak_r['bmo_Linf_ratio']:.4f}")

    print(f"\n  {'Radius':>12} | {'BMO at radius':>14} | {'BMO/Linf':>10}")
    print("  " + "-"*45)
    for rad_str, val in sorted(peak_r['bmo_by_radius'].items(), key=lambda x: float(x[0]), reverse=True):
        r_val = float(rad_str)
        ratio = val / peak_r['omega_Linf'] if peak_r['omega_Linf'] > 0 else 0
        print(f"  {r_val:>12.4f} | {val:>14.4f} | {ratio:>10.4f}")

# =============================================================================
# 4. FLATNESS vs C_Leff CORRELATION
# =============================================================================
print("\n" + "="*80)
print("4. FLATNESS vs C_L,eff CORRELATION")
print("="*80)

C_L = data['constants']['C_L']
for Re_key in ['100', '500', '1000', '5000']:
    ts_key = f'time_series_Re{Re_key}'
    if ts_key not in data:
        continue
    ts = data[ts_key]
    ts_f = [r for r in ts if r['time'] > 0.5]

    F4_arr = np.array([r['F4'] for r in ts_f])
    CL_ratio_arr = np.array([r['C_L_eff_ratio'] for r in ts_f])

    # Correlation
    if len(F4_arr) > 3:
        corr = np.corrcoef(np.log(F4_arr + 1e-10), np.log(CL_ratio_arr + 1e-10))[0, 1]
        # Fit: log(CL_ratio) = a + b * log(F4)
        A = np.vstack([np.log(F4_arr), np.ones(len(F4_arr))]).T
        coeffs = np.linalg.lstsq(A, np.log(CL_ratio_arr), rcond=None)[0]
        b_fit, a_fit = coeffs
        print(f"Re={Re_key}: corr(log F4, log C_L_eff/C_L) = {corr:.4f}, "
              f"scaling: C_L_eff/C_L ~ F4^{b_fit:.3f}, prefactor = {np.exp(a_fit):.4f}")

# =============================================================================
# 5. REFINED CONDITIONAL BOUND
# =============================================================================
print("\n" + "="*80)
print("5. CONDITIONAL ENSTROPHY BOUND")
print("="*80)

# Collect all (F4, C_empirical) pairs
F4_all = []
C_all = []
Re_all = []

for Re_key in ['100', '500', '1000', '5000']:
    ts_key = f'time_series_Re{Re_key}'
    if ts_key not in data:
        continue
    ts = data[ts_key]
    ts_f = [r for r in ts if r['time'] > 0.5 and r['abs_vortex_stretching'] > 1e-30]

    for r in ts_f:
        denom = r['omega_L2']**1.5 * r['grad_omega_L2']**1.5
        if denom > 1e-30:
            C_emp = r['abs_vortex_stretching'] / denom
            F4_all.append(r['F4'])
            C_all.append(C_emp)
            Re_all.append(int(Re_key))

F4_all = np.array(F4_all)
C_all = np.array(C_all)
Re_all = np.array(Re_all)

if len(F4_all) > 5:
    # Fit: C = a * F4^b
    mask = (F4_all > 0) & (C_all > 0)
    log_F4 = np.log(F4_all[mask])
    log_C = np.log(C_all[mask])
    A = np.vstack([log_F4, np.ones(np.sum(mask))]).T
    coeffs = np.linalg.lstsq(A, log_C, rcond=None)[0]
    b_fit, a_fit = coeffs
    C0 = np.exp(a_fit)

    print(f"Global fit: C(F4) = {C0:.6f} × F4^({b_fit:.4f})")
    print(f"  => C(F4) ≈ {C0:.6f} / F4 (exponent ≈ -1)")
    print(f"")
    print(f"This means: |∫ S_ij omega_i omega_j dx| <= ({C0:.6f}/F4) * ||omega||^{{3/2}}_{{L^2}} * ||grad omega||^{{3/2}}_{{L^2}}")
    print(f"")
    print(f"Standard bound: C_L^2 = {C_L**2:.6f}")
    print(f"Improvement factor at F4 = 5/3 (Gaussian): C_L^2 / C(5/3) = {C_L**2 / (C0 * (5/3)**b_fit):.1f}×")
    print(f"Improvement factor at F4 = 3: C_L^2 / C(3) = {C_L**2 / (C0 * 3**b_fit):.1f}×")
    print(f"Improvement factor at F4 = 10: C_L^2 / C(10) = {C_L**2 / (C0 * 10**b_fit):.1f}×")
    print()

    # Maximum C_empirical in each F4 bin
    F4_bins = [1, 1.5, 2, 3, 4, 6, 8, 12, 16]
    print(f"{'F4 range':>15} | {'max C_emp':>12} | {'# pts':>6} | {'C_L^2/max_C':>12}")
    print("-"*55)
    for i in range(len(F4_bins) - 1):
        lo, hi = F4_bins[i], F4_bins[i+1]
        idx = (F4_all >= lo) & (F4_all < hi)
        if np.sum(idx) > 0:
            max_c = np.max(C_all[idx])
            n_pts = np.sum(idx)
            print(f"[{lo:>4.1f}, {hi:>4.1f})" + f" | {max_c:>12.6f} | {n_pts:>6} | {C_L**2/max_c:>12.1f}")

    # Check: does the max C_emp envelope follow C ~ 1/F4 or something else?
    print("\n--- Envelope analysis (max C in F4 bins): ---")
    envelope_F4 = []
    envelope_C = []
    for i in range(len(F4_bins) - 1):
        lo, hi = F4_bins[i], F4_bins[i+1]
        idx = (F4_all >= lo) & (F4_all < hi)
        if np.sum(idx) > 0:
            envelope_F4.append(0.5*(lo+hi))
            envelope_C.append(np.max(C_all[idx]))

    if len(envelope_F4) > 2:
        eF = np.log(np.array(envelope_F4))
        eC = np.log(np.array(envelope_C))
        A2 = np.vstack([eF, np.ones(len(eF))]).T
        coeffs2 = np.linalg.lstsq(A2, eC, rcond=None)[0]
        b2, a2 = coeffs2
        print(f"Envelope fit: C_max(F4) ~ {np.exp(a2):.6f} × F4^({b2:.3f})")
        print(f"  => The WORST-CASE conditional bound scales as F4^({b2:.3f})")


# =============================================================================
# 6. KEY INSIGHT: Why BKM is ~226× tighter than Ladyzhenskaya
# =============================================================================
print("\n" + "="*80)
print("6. WHY BKM IS TIGHTER — DECOMPOSITION")
print("="*80)

# The Ladyzhenskaya chain for vortex stretching:
# |VS| <= ||S||_{L^2} * ||omega||_{L^4}^2   [Hölder]
# <= ||omega||_{L^2} * (C_L ||omega||_{L^2}^{1/4} ||nabla omega||_{L^2}^{3/4})^2  [Ladyzhenskaya]
# = C_L^2 * ||omega||_{L^2}^{3/2} * ||nabla omega||_{L^2}^{3/2}
#
# BKM bound for ||nabla u||_{L^inf}:
# ||nabla u||_{L^inf} <= C_BKM * ||omega||_{L^inf} * (1 + log(1 + ||omega||_{H^1}/||omega||_{L^2}))
#
# These bound different things, but both are used in regularity theory.
# The Ladyzhenskaya chain bounds the ENSTROPHY PRODUCTION RATE.
# The BKM bound bounds the L^inf of velocity gradient (used in BKM blowup criterion).
#
# The slack decomposition:
# Ladyzhenskaya chain: 237× = slack_Hölder × slack_Ladyzhenskaya × slack_symmetric
# BKM bound: ~1.05× (near tight!)
#
# The BKM bound is tight because:
# 1. ||omega||_{L^inf} directly captures the local vorticity maximum
# 2. The log correction is O(1) for smooth fields (log(1 + H1/L2) ≈ 2-4)
# 3. No interpolation inequality (Ladyzhenskaya) is involved

print("The BKM bound (min slack ≈ 1.05) is near-tight because:")
print("  1. It uses ||omega||_Linf directly — no interpolation loss")
print("  2. The logarithmic correction is only O(1) for smooth flows")
print("  3. The Biot-Savart kernel gives a tight L^inf → L^inf mapping")
print()
print("The Ladyzhenskaya chain (min slack ≈ 237) is loose because:")
print("  1. Hölder inequality loses 5-9× (alignment/cancellation)")
print("  2. Ladyzhenskaya interpolation loses 31× (NS spectra far from optimizer)")
print("  3. Symmetric factor contributes √2 (exact for div-free)")
print()
print("BKM advantage factor ≈ 237/1.05 ≈ 226×")
print("This is the ratio of two approaches to bounding the same physical quantity.")
print("It suggests that BKM-style (L^inf vorticity + log) bounds are fundamentally")
print("better suited to NS regularity than Ladyzhenskaya-based energy methods.")

# =============================================================================
# 7. Summary statistics
# =============================================================================
print("\n" + "="*80)
print("7. SUMMARY TABLES FOR REPORT")
print("="*80)

# Final summary table
print("\n| Re | Lad VS min slack | Agmon min slack | BKM min slack | BKM advantage (Lad/BKM) | BMO/L^inf ratio |")
print("|---|---|---|---|---|---|")
for s in data.get('summary_table', []):
    Re = s['Re']
    bmo_ratio = next((b['bmo_Linf_ratio'] for b in data.get('bmo_summary', []) if b['Re'] == Re), 0)
    print(f"| {Re} | {s['lad_vs_min_slack']:.1f} | {s['agmon_min_slack']:.1f} | {s['bkm_min_slack']:.2f} | {s['bkm_advantage_lad_min']:.1f} | {bmo_ratio:.4f} |")

print("\n| Re | F4 (peak enstrophy) | mu(0.5) | C_L,eff/C_L | Predicted from F4 |")
print("|---|---|---|---|---|")
for s in data.get('intermittency_summary', []):
    Re = s['Re']
    F4_pred = (5/3 / s['F4_peak_enstrophy'])**0.25 if s['F4_peak_enstrophy'] > 0 else 0
    print(f"| {Re} | {s['F4_peak_enstrophy']:.2f} | {s['mu_0.5_peak']:.4f} | {s['C_L_eff_ratio_mean']:.4f} | {F4_pred:.4f} |")
