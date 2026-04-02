#!/usr/bin/env python3
"""
Compile and analyze results from all simulations.
Produces the unified Slack Atlas Table and time-series analysis.
"""

import numpy as np
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

def load_results(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return data

def compile_all():
    """Run all 4 Re values and compile."""
    from ns_solver import NavierStokesSolver, taylor_green_ic
    from slack_measurements import compute_extended_diagnostics, compute_all_slacks, compute_constants_on_torus, INEQUALITY_PAIRS
    from run_simulations import run_single_simulation, analyze_results, print_summary_table

    re_values = [100, 500, 1000, 5000]
    N = 64
    T = 5.0

    all_results = []
    all_summaries = []

    for Re in re_values:
        print(f"\n{'#'*60}")
        print(f"# Running Re={Re}")
        print(f"{'#'*60}")
        results = run_single_simulation(N, Re, T, n_samples=60)
        summary = analyze_results(results)
        all_results.append(results)
        all_summaries.append(summary)

    # Print unified table
    print_summary_table(all_summaries)

    # Save combined results
    outdir = os.path.join(os.path.dirname(__file__), '..')
    with open(os.path.join(outdir, 'results_combined.json'), 'w') as f:
        serializable_results = []
        for r in all_results:
            r_copy = dict(r)
            # Truncate time series for storage
            r_copy['time_series_summary'] = [{k: v for k, v in rec.items()
                                                if not k.startswith('energy_spectrum')}
                                              for rec in r['time_series']]
            del r_copy['time_series']
            serializable_results.append(r_copy)
        json.dump({
            'results': serializable_results,
            'summaries': all_summaries
        }, f, indent=2, default=lambda x: float(x) if isinstance(x, (np.floating, np.integer)) else str(x))

    # Detailed time-series for Re=1000
    r1000 = next(r for r in all_results if r['Re'] == 1000)
    print_time_series_detail(r1000)

    # Trend analysis
    print_trend_analysis(all_summaries)

    # Empirical constant analysis
    print_empirical_constants(all_results)

    return all_results, all_summaries


def print_time_series_detail(results):
    """Print detailed time series for one Re value."""
    Re = results['Re']
    ts = results['time_series']
    ineq_names = ['F1_Ladyzhenskaya', 'F3_Sobolev_H1_L6', 'E2E3_Vortex_Stretching',
                  'E1_Energy', 'R1F2_Prodi_Serrin', 'F4G1_Agmon', 'F5_CZ_Pressure', 'E4_Kato_Ponce']

    print(f"\n{'='*140}")
    print(f"Detailed Time Series: Re={Re}")
    print(f"{'='*140}")

    header = f"{'t':>6} | {'Energy':>10} | {'Enstrophy':>10}"
    for name in ineq_names:
        short = name[:8]
        header += f" | {short:>8}"
    print(header)
    print("-"*140)

    for r in ts[::max(1, len(ts)//25)]:
        row = f"{r['time']:>6.3f} | {r['energy']:>10.4f} | {r['enstrophy']:>10.4f}"
        for name in ineq_names:
            val = r.get(f'slack_{name}', float('inf'))
            val = min(val, 9999.99)
            row += f" | {val:>8.2f}"
        print(row)


def print_trend_analysis(summaries):
    """Analyze how slack ratios trend with Re."""
    ineq_names = ['F1_Ladyzhenskaya', 'F3_Sobolev_H1_L6', 'E2E3_Vortex_Stretching',
                  'E1_Energy', 'R1F2_Prodi_Serrin', 'F4G1_Agmon', 'F5_CZ_Pressure', 'E4_Kato_Ponce']

    Re_values = [s['Re'] for s in summaries]

    print(f"\n{'='*80}")
    print("TREND ANALYSIS: How slack changes with Re")
    print(f"{'='*80}")

    for name in ineq_names:
        means = [s.get(f'{name}_mean', float('inf')) for s in summaries]
        mins = [s.get(f'{name}_min', float('inf')) for s in summaries]

        # Skip if any are inf
        if any(not np.isfinite(m) for m in means):
            print(f"\n{name}: insufficient data")
            continue

        # Linear regression on log(Re) vs mean slack
        log_Re = np.log(Re_values)
        if all(m > 0 for m in means):
            log_mean = np.log(means)
            # Fit log(slack) = a + b * log(Re)
            A = np.vstack([log_Re, np.ones(len(log_Re))]).T
            b, a = np.linalg.lstsq(A, log_mean, rcond=None)[0]
            trend = "GROWS" if b > 0.1 else ("SHRINKS" if b < -0.1 else "STABLE")
            exponent = b
        else:
            trend = "N/A"
            exponent = 0

        # Min slack trend
        if all(m > 0 for m in mins):
            log_mins = np.log(mins)
            b_min, a_min = np.linalg.lstsq(A, log_mins, rcond=None)[0]
            min_trend = "GROWS" if b_min > 0.1 else ("SHRINKS" if b_min < -0.1 else "STABLE")
        else:
            min_trend = "N/A"

        print(f"\n{name}:")
        print(f"  Mean slack vs Re: {trend} (scaling ∝ Re^{exponent:.2f})")
        print(f"  Min  slack vs Re: {min_trend}")
        print(f"  Re={Re_values[0]:5d}: mean={means[0]:>10.2f}, min={mins[0]:>10.4f}")
        print(f"  Re={Re_values[-1]:5d}: mean={means[-1]:>10.2f}, min={mins[-1]:>10.4f}")
        print(f"  Range of means: {min(means):.2f} — {max(means):.2f}")


def print_empirical_constants(all_results):
    """For each inequality, compute the tightest empirical constant."""
    ineq_names = ['F1_Ladyzhenskaya', 'F3_Sobolev_H1_L6', 'E2E3_Vortex_Stretching',
                  'R1F2_Prodi_Serrin', 'F4G1_Agmon', 'F5_CZ_Pressure', 'E4_Kato_Ponce']

    print(f"\n{'='*80}")
    print("EMPIRICAL CONSTANT ANALYSIS")
    print("(ratio = actual/bound_without_constant, tight constant = max ratio)")
    print(f"{'='*80}")

    from slack_measurements import INEQUALITY_PAIRS, compute_constants_on_torus
    constants = compute_constants_on_torus(N_sum=30)

    # Map from inequality name to the constant used
    const_map = {
        'F1_Ladyzhenskaya': ('C_L', lambda d,C: d['u_L2']**0.25 * d['grad_u_L2']**0.75),
        'F3_Sobolev_H1_L6': ('S3_vec', lambda d,C: d['grad_u_L2']),
        'E2E3_Vortex_Stretching': ('C_L', lambda d,C: d['omega_L2']**1.5 * d['grad_omega_L2']**1.5),
        'R1F2_Prodi_Serrin': ('C_PS', lambda d,C: d['u_L2']**0.25 * d['u_H1']**1.75),
        'F4G1_Agmon': ('C_Agmon', lambda d,C: d['u_H2']**0.5 * d['u_H3']**0.5),
        'F5_CZ_Pressure': ('C_CZ', lambda d,C: d['u_L3']**2),
        'E4_Kato_Ponce': ('C_KP', lambda d,C: d['grad_u_Linf'] * d['u_H2dot_sq_val']),
    }

    for name in ineq_names:
        if name not in const_map:
            continue

        const_name, formula_fn = const_map[name]
        bound_fn, actual_fn = INEQUALITY_PAIRS[name]

        max_ratio = 0
        worst_case = None

        for results in all_results:
            Re = results['Re']
            for rec in results['time_series']:
                # Reconstruct diag-like dict from record
                diag = rec  # our records have the needed fields
                a = actual_fn(diag, constants)
                # Compute the formula without constant
                try:
                    f = formula_fn(diag, constants)
                except:
                    continue

                if f > 1e-30 and a > 1e-30:
                    ratio = a / f
                    if ratio > max_ratio:
                        max_ratio = ratio
                        worst_case = (Re, rec['time'])

        used_const = constants.get(const_name, 'N/A')
        print(f"\n{name}:")
        print(f"  Used constant ({const_name}): {used_const:.6f}")
        print(f"  Tightest empirical constant: {max_ratio:.6f}")
        if worst_case:
            print(f"  Worst case: Re={worst_case[0]}, t={worst_case[1]:.3f}")
        if isinstance(used_const, float) and max_ratio > 0:
            print(f"  Slack from constant alone: {used_const / max_ratio:.4f}")


if __name__ == '__main__':
    compile_all()
