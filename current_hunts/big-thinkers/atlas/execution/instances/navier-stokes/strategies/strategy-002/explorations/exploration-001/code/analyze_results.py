#!/usr/bin/env python3
"""
Analyze BKM comparison results in detail.
Generates tables and analysis for the report.
"""

import json
import numpy as np
import os

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')


def load_results():
    with open(os.path.join(RESULTS_DIR, 'all_results.json')) as f:
        return json.load(f)


def safe_float(v):
    if v is None:
        return float('nan')
    if isinstance(v, str):
        if v == 'inf':
            return float('inf')
        elif v == '-inf':
            return float('-inf')
        elif v == 'nan':
            return float('nan')
        return float(v)
    return float(v)


def analyze_case(r):
    """Deep analysis of a single case."""
    diags = r['diagnostics']
    times = r['times']
    bl = r['blowup']

    # Extract time series
    n = len(diags)
    ts = np.array([safe_float(t) for t in times[:n]])
    enstrophies = np.array([d['enstrophy'] for d in diags])
    omega_L2s = np.array([d['omega_L2'] for d in diags])
    omega_Linfs = np.array([d['omega_Linf'] for d in diags])
    grad_omega_L2s = np.array([d['grad_omega_L2'] for d in diags])
    abs_vs = np.array([d['abs_vs'] for d in diags])
    VS_Lads = np.array([d['VS_Lad'] for d in diags])
    VS_BKMs = np.array([d['VS_BKM'] for d in diags])
    slacks_Lad = np.array([safe_float(d['slack_Lad']) for d in diags])
    slacks_BKM = np.array([safe_float(d['slack_BKM']) for d in diags])
    advantages = np.array([safe_float(d['advantage']) for d in diags])
    omega_ratios = np.array([safe_float(d['omega_ratio']) if d['omega_ratio'] is not None else float('nan') for d in diags])
    log_factors = np.array([d['log_factor'] for d in diags])
    RHS_actuals = np.array([d['RHS_actual'] for d in diags])
    RHS_Lads = np.array([d['RHS_Lad'] for d in diags])
    RHS_BKMs = np.array([d['RHS_BKM'] for d in diags])
    RHS_Lad_Youngs = np.array([d['RHS_Lad_Young'] for d in diags])
    RHS_BKM_Youngs = np.array([d['RHS_BKM_Young'] for d in diags])
    C_CZ_emps = np.array([safe_float(d['C_CZ_emp']) if d['C_CZ_emp'] is not None else float('nan') for d in diags])
    dissipations = np.array([d['dissipation'] for d in diags])

    # Filter out first timestep where VS might be zero
    valid = abs_vs > 1e-20
    if np.sum(valid) == 0:
        valid = np.ones(n, dtype=bool)

    result = {}
    result['ic_name'] = r['ic_name']
    result['Re'] = r['Re']
    result['N'] = r['N']
    result['n_snapshots'] = n

    # Peak enstrophy
    peak_idx = np.argmax(enstrophies)
    result['peak_enstrophy'] = float(enstrophies[peak_idx])
    result['t_peak'] = float(ts[peak_idx])

    # Slack statistics (exclude zeros and infinities)
    finite_Lad = slacks_Lad[valid & np.isfinite(slacks_Lad)]
    finite_BKM = slacks_BKM[valid & np.isfinite(slacks_BKM)]
    finite_adv = advantages[valid & np.isfinite(advantages) & ~np.isnan(advantages)]

    if len(finite_Lad) > 0:
        result['min_slack_Lad'] = float(np.min(finite_Lad))
        result['median_slack_Lad'] = float(np.median(finite_Lad))
        result['max_slack_Lad'] = float(np.max(finite_Lad))
    else:
        result['min_slack_Lad'] = float('nan')
        result['median_slack_Lad'] = float('nan')
        result['max_slack_Lad'] = float('nan')

    if len(finite_BKM) > 0:
        result['min_slack_BKM'] = float(np.min(finite_BKM))
        result['median_slack_BKM'] = float(np.median(finite_BKM))
        result['max_slack_BKM'] = float(np.max(finite_BKM))
    else:
        result['min_slack_BKM'] = float('nan')
        result['median_slack_BKM'] = float('nan')
        result['max_slack_BKM'] = float('nan')

    if len(finite_adv) > 0:
        result['min_advantage'] = float(np.min(finite_adv))
        result['median_advantage'] = float(np.median(finite_adv))
        result['max_advantage'] = float(np.max(finite_adv))
    else:
        result['min_advantage'] = float('nan')
        result['median_advantage'] = float('nan')
        result['max_advantage'] = float('nan')

    # omega ratio statistics
    finite_ratios = omega_ratios[~np.isnan(omega_ratios)]
    if len(finite_ratios) > 0:
        result['min_omega_ratio'] = float(np.min(finite_ratios))
        result['max_omega_ratio'] = float(np.max(finite_ratios))
        result['mean_omega_ratio'] = float(np.mean(finite_ratios))
        # How does it change: ratio at peak enstrophy vs initial
        result['omega_ratio_initial'] = float(finite_ratios[0])
        result['omega_ratio_peak'] = float(omega_ratios[peak_idx]) if not np.isnan(omega_ratios[peak_idx]) else float('nan')
    else:
        result['min_omega_ratio'] = float('nan')
        result['max_omega_ratio'] = float('nan')
        result['mean_omega_ratio'] = float('nan')
        result['omega_ratio_initial'] = float('nan')
        result['omega_ratio_peak'] = float('nan')

    # Log factor statistics
    result['mean_log_factor'] = float(np.mean(log_factors))
    result['max_log_factor'] = float(np.max(log_factors))

    # C_CZ empirical
    finite_CZ = C_CZ_emps[~np.isnan(C_CZ_emps) & valid]
    if len(finite_CZ) > 0:
        result['min_C_CZ_emp'] = float(np.min(finite_CZ))
        result['max_C_CZ_emp'] = float(np.max(finite_CZ))
        result['median_C_CZ_emp'] = float(np.median(finite_CZ))
    else:
        result['min_C_CZ_emp'] = float('nan')
        result['max_C_CZ_emp'] = float('nan')
        result['median_C_CZ_emp'] = float('nan')

    # ODE RHS comparison: at how many timesteps does BKM bound < Lad bound?
    bkm_tighter = np.sum(RHS_BKMs < RHS_Lads)
    result['bkm_tighter_count'] = int(bkm_tighter)
    result['total_valid'] = int(np.sum(valid))

    # After Young's: at how many timesteps does BKM_Young < Lad_Young?
    bkm_young_tighter = np.sum(RHS_BKM_Youngs < RHS_Lad_Youngs)
    result['bkm_young_tighter_count'] = int(bkm_young_tighter)

    # Blow-up times
    result['T_Lad'] = safe_float(bl['T_Lad'])
    result['T_BKM'] = safe_float(bl['T_BKM'])
    result['T_ratio'] = safe_float(bl['T_ratio'])
    result['alpha_fit'] = safe_float(bl['alpha_fit'])

    # Time series (sampled for report)
    sample_indices = np.linspace(0, n-1, min(20, n), dtype=int)
    result['time_series'] = []
    for i in sample_indices:
        result['time_series'].append({
            't': float(ts[i]),
            'enstrophy': float(enstrophies[i]),
            'abs_vs': float(abs_vs[i]),
            'VS_Lad': float(VS_Lads[i]),
            'VS_BKM': float(VS_BKMs[i]),
            'slack_Lad': float(slacks_Lad[i]) if np.isfinite(slacks_Lad[i]) else 'inf',
            'slack_BKM': float(slacks_BKM[i]) if np.isfinite(slacks_BKM[i]) else 'inf',
            'advantage': float(advantages[i]) if np.isfinite(advantages[i]) and not np.isnan(advantages[i]) else 'N/A',
            'omega_ratio': float(omega_ratios[i]) if not np.isnan(omega_ratios[i]) else 'N/A',
            'log_factor': float(log_factors[i]),
            'RHS_actual': float(RHS_actuals[i]),
            'RHS_Lad_Young': float(RHS_Lad_Youngs[i]),
            'RHS_BKM_Young': float(RHS_BKM_Youngs[i]),
        })

    return result


def main():
    results = load_results()
    analyses = []

    print("=" * 100)
    print("DETAILED BKM vs LADYZHENSKAYA ANALYSIS")
    print("=" * 100)

    # 1. Summary table
    print("\n## 1. Summary Table: Blow-up Times and Advantage Factors\n")
    header = f"{'IC':<15} {'Re':<6} {'N':<4} {'T_Lad':<12} {'T_BKM':<12} {'T_ratio':<14} {'min_adv':<10} {'med_adv':<10} {'alpha':<8} {'max_omega_r':<12}"
    print(header)
    print("-" * len(header))

    for r in results:
        a = analyze_case(r)
        analyses.append(a)
        print(f"{a['ic_name']:<15} {a['Re']:<6} {a['N']:<4} "
              f"{a['T_Lad']:<12.3e} {a['T_BKM']:<12.3e} {a['T_ratio']:<14.2e} "
              f"{a['min_advantage']:<10.1f} {a['median_advantage']:<10.1f} "
              f"{a['alpha_fit']:<8.3f} {a['max_omega_ratio']:<12.4f}")

    # 2. Slack comparison
    print("\n\n## 2. Slack Statistics\n")
    header = f"{'IC':<15} {'Re':<6} {'min_s_Lad':<12} {'med_s_Lad':<12} {'min_s_BKM':<12} {'med_s_BKM':<12} {'BKM_tighter':<12}"
    print(header)
    print("-" * len(header))

    for a in analyses:
        print(f"{a['ic_name']:<15} {a['Re']:<6} "
              f"{a['min_slack_Lad']:<12.1f} {a['median_slack_Lad']:<12.1f} "
              f"{a['min_slack_BKM']:<12.1f} {a['median_slack_BKM']:<12.1f} "
              f"{a['bkm_tighter_count']}/{a['total_valid']}")

    # 3. omega_Linf / omega_L2 dynamics
    print("\n\n## 3. ||omega||_Linf / ||omega||_L2 Dynamics\n")
    header = f"{'IC':<15} {'Re':<6} {'ratio_init':<12} {'ratio_peak':<12} {'ratio_max':<12} {'alpha_fit':<10}"
    print(header)
    print("-" * len(header))

    for a in analyses:
        print(f"{a['ic_name']:<15} {a['Re']:<6} "
              f"{a['omega_ratio_initial']:<12.4f} {a['omega_ratio_peak']:<12.4f} "
              f"{a['max_omega_ratio']:<12.4f} {a['alpha_fit']:<10.3f}")

    # 4. C_CZ empirical values
    print("\n\n## 4. Empirical Calderon-Zygmund Constants\n")
    header = f"{'IC':<15} {'Re':<6} {'min_C_CZ':<12} {'med_C_CZ':<12} {'max_C_CZ':<12} {'theoretical':<12}"
    print(header)
    print("-" * len(header))

    for a in analyses:
        print(f"{a['ic_name']:<15} {a['Re']:<6} "
              f"{a['min_C_CZ_emp']:<12.4f} {a['median_C_CZ_emp']:<12.4f} "
              f"{a['max_C_CZ_emp']:<12.4f} {'0.24':<12}")

    # 5. Time series for key cases
    print("\n\n## 5. Key Time Series\n")
    key_cases = [a for a in analyses if (a['ic_name'] == 'TGV' and a['Re'] in [100, 1000]) or
                 (a['ic_name'] == 'Gaussian' and a['Re'] == 1000) or
                 (a['ic_name'] == 'AntiParallel' and a['Re'] == 500)]

    for a in key_cases:
        print(f"\n### {a['ic_name']} Re={a['Re']} N={a['N']}")
        header = f"  {'t':<7} {'enstrophy':<12} {'|VS|':<12} {'VS_Lad':<12} {'VS_BKM':<12} {'adv':<8} {'w_ratio':<10} {'log_f':<8}"
        print(header)
        print("  " + "-" * (len(header)-2))
        for pt in a['time_series']:
            adv = f"{pt['advantage']:<8.1f}" if isinstance(pt['advantage'], float) else f"{'N/A':<8}"
            wr = f"{pt['omega_ratio']:<10.4f}" if isinstance(pt['omega_ratio'], float) else f"{'N/A':<10}"
            print(f"  {pt['t']:<7.3f} {pt['enstrophy']:<12.4e} {pt['abs_vs']:<12.4e} "
                  f"{pt['VS_Lad']:<12.4e} {pt['VS_BKM']:<12.4e} {adv} {wr} {pt['log_factor']:<8.3f}")

    # 6. ODE RHS comparison: Lad_Young vs BKM_Young
    print("\n\n## 6. ODE RHS After Young's Inequality\n")
    for a in key_cases:
        print(f"\n### {a['ic_name']} Re={a['Re']}")
        header = f"  {'t':<7} {'RHS_actual':<14} {'RHS_Lad_Y':<14} {'RHS_BKM_Y':<14} {'Lad_Y/BKM_Y':<12}"
        print(header)
        print("  " + "-" * (len(header)-2))
        for pt in a['time_series']:
            ratio = pt['RHS_Lad_Young'] / pt['RHS_BKM_Young'] if abs(pt['RHS_BKM_Young']) > 1e-30 else float('inf')
            print(f"  {pt['t']:<7.3f} {pt['RHS_actual']:<14.4e} {pt['RHS_Lad_Young']:<14.4e} "
                  f"{pt['RHS_BKM_Young']:<14.4e} {ratio:<12.1f}")

    # 7. Convergence check
    print("\n\n## 7. Convergence Check: TGV Re=1000\n")
    n64 = [a for a in analyses if a['ic_name'] == 'TGV' and a['Re'] == 1000 and a['N'] == 64][0]
    n128 = [a for a in analyses if a['ic_name'] == 'TGV' and a['Re'] == 1000 and a['N'] == 128]
    if n128:
        n128 = n128[0]
        print(f"  N=64:  T_Lad={n64['T_Lad']:.3e}, T_BKM={n64['T_BKM']:.3e}, alpha_fit={n64['alpha_fit']:.3f}")
        print(f"  N=128: T_Lad={n128['T_Lad']:.3e}, T_BKM={n128['T_BKM']:.3e}, alpha_fit={n128['alpha_fit']:.3f}")
        print(f"  Peak enstrophy: N=64={n64['peak_enstrophy']:.4e} at t={n64['t_peak']:.3f}")
        print(f"                  N=128={n128['peak_enstrophy']:.4e} at t={n128['t_peak']:.3f}")
        print(f"  min_slack_Lad: N=64={n64['min_slack_Lad']:.1f}, N=128={n128['min_slack_Lad']:.1f}")
        print(f"  min_slack_BKM: N=64={n64['min_slack_BKM']:.1f}, N=128={n128['min_slack_BKM']:.1f}")

    # 8. Verdict
    print("\n\n## 8. VERDICT\n")
    all_T_ratios = [a['T_ratio'] for a in analyses if np.isfinite(a['T_ratio'])]
    min_ratio = min(all_T_ratios) if all_T_ratios else 0
    max_ratio = max(all_T_ratios) if all_T_ratios else 0

    print(f"  T_BKM/T_Lad range: {min_ratio:.2e} to {max_ratio:.2e}")
    print(f"  Success criterion: T_BKM/T_Lad > 10")
    if min_ratio > 10:
        print(f"  RESULT: BKM DIRECTION MASSIVELY VALIDATED")
        print(f"  The BKM enstrophy bypass gives {min_ratio:.0e}x to {max_ratio:.0e}x later blow-up times")
    else:
        print(f"  RESULT: BKM direction unclear")

    # Check if any case has T_BKM = inf (no finite-time blow-up)
    inf_cases = [a for a in analyses if not np.isfinite(a['T_BKM'])]
    if inf_cases:
        print(f"\n  {len(inf_cases)} case(s) show NO FINITE-TIME BLOW-UP under BKM ODE:")
        for a in inf_cases:
            print(f"    {a['ic_name']} Re={a['Re']}: alpha_fit={a['alpha_fit']:.3f} (needs alpha>0 for finite-time blowup)")

    # Save analysis
    with open(os.path.join(RESULTS_DIR, 'analysis.json'), 'w') as f:
        json.dump(analyses, f, indent=2, default=str)


if __name__ == '__main__':
    main()
