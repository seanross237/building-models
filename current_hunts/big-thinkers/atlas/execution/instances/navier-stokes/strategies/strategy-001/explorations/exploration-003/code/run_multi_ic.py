#!/usr/bin/env python3
"""
Run vortex stretching slack measurements across multiple initial conditions.

Measures the E2E3_Vortex_Stretching slack ratio for each IC at Re=100,500,1000.
Also records all 8 inequality slacks for comparison.

Usage: python run_multi_ic.py [--ics IC1 IC2 ...] [--re RE1 RE2 ...] [--N N]
"""

import numpy as np
import json
import time
import sys
import os
import argparse
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from ns_solver import NavierStokesSolver
from slack_measurements import (
    compute_extended_diagnostics, compute_all_slacks,
    compute_constants_on_torus, INEQUALITY_PAIRS
)
from initial_conditions import IC_REGISTRY, create_ic


def run_simulation(solver, ux_hat, uy_hat, uz_hat, T_final, n_samples=100,
                   constants=None, verbose=True, label=""):
    """
    Run a single NS simulation and collect slack measurements at each sample point.

    Returns dict with time series of diagnostics and slacks.
    """
    N = solver.N
    nu = solver.nu

    if constants is None:
        constants = compute_constants_on_torus(N_sum=30)

    # Initial diagnostics
    diag0 = compute_extended_diagnostics(solver, ux_hat, uy_hat, uz_hat)
    initial_energy_L2_sq = diag0['u_L2_sq']

    if verbose:
        print(f"  Initial: E={diag0['energy']:.6f}, ||u||_L2={diag0['u_L2']:.6f}, "
              f"enstrophy={diag0['enstrophy']:.6f}, div_max={diag0['divergence_max']:.2e}")

    # Time stepping
    t = 0.0
    step = 0
    dt_sample = T_final / n_samples
    next_sample = 0.0
    cumulative_dissipation = 0.0
    time_series = []

    K2 = solver.K2
    norm_factor = (2*np.pi)**3 / N**6

    wall_start = time.time()

    while t < T_final:
        dt = solver.compute_dt(ux_hat, uy_hat, uz_hat)
        dt = min(dt, T_final - t)
        if dt < 1e-12:
            if verbose:
                print(f"  WARNING: dt too small ({dt:.2e}) at t={t:.4f}, stopping.")
            break

        ux_hat_new, uy_hat_new, uz_hat_new = solver.rk4_step(ux_hat, uy_hat, uz_hat, dt)

        # Accumulate dissipation
        grad_sq_spectral = norm_factor * (np.sum(K2 * np.abs(ux_hat)**2) +
                                           np.sum(K2 * np.abs(uy_hat)**2) +
                                           np.sum(K2 * np.abs(uz_hat)**2)).real
        cumulative_dissipation += 2 * nu * grad_sq_spectral * dt

        ux_hat, uy_hat, uz_hat = ux_hat_new, uy_hat_new, uz_hat_new
        t += dt
        step += 1

        if t >= next_sample - 1e-10:
            diag = compute_extended_diagnostics(solver, ux_hat, uy_hat, uz_hat)
            diag['initial_energy_L2_sq'] = initial_energy_L2_sq
            diag['cumulative_dissipation'] = cumulative_dissipation

            slacks = compute_all_slacks(diag, constants)

            record = {
                'time': float(t),
                'step': step,
                'energy': float(diag['energy']),
                'enstrophy': float(diag['enstrophy']),
                'omega_L2': float(diag['omega_L2']),
                'grad_omega_L2': float(diag['grad_omega_L2']),
                'vortex_stretching': float(diag['vortex_stretching']),
                'divergence_max': float(diag['divergence_max']),
            }

            # Add all slack ratios
            for name, s in slacks.items():
                record[f'slack_{name}'] = float(s['slack'])
                record[f'bound_{name}'] = float(s['bound'])
                record[f'actual_{name}'] = float(s['actual'])

            time_series.append(record)
            next_sample += dt_sample

            if verbose and len(time_series) % 25 == 0:
                vs_slack = record.get('slack_E2E3_Vortex_Stretching', float('inf'))
                print(f"  t={t:.3f}, E={diag['energy']:.6f}, enstr={diag['enstrophy']:.6f}, "
                      f"VS_slack={vs_slack:.2f}")

    wall_elapsed = time.time() - wall_start

    if verbose:
        print(f"  Completed: {step} steps in {wall_elapsed:.1f}s")

    return {
        'time_series': time_series,
        'n_steps': step,
        'wall_time': wall_elapsed,
    }


def analyze_vs_slack(time_series, skip_initial=0.2):
    """Analyze the vortex stretching slack time series.

    Returns summary dict with min, mean, time-of-min for VS slack.
    Also returns all 8 inequality minimum slacks for comparison.
    """
    if not time_series:
        return {'vs_min': float('inf'), 'vs_mean': float('inf')}

    # Filter out initial transient
    T_final = time_series[-1]['time']
    ts = [r for r in time_series if r['time'] > skip_initial * T_final]
    if not ts:
        ts = time_series

    result = {}

    # VS slack
    vs_key = 'slack_E2E3_Vortex_Stretching'
    vs_values = [r[vs_key] for r in ts if vs_key in r and np.isfinite(r[vs_key]) and r[vs_key] < 1e15]

    if vs_values:
        result['vs_min'] = min(vs_values)
        result['vs_mean'] = np.mean(vs_values)
        result['vs_std'] = np.std(vs_values)
        # Find time of minimum
        min_record = min([r for r in ts if vs_key in r and np.isfinite(r[vs_key])],
                         key=lambda r: r[vs_key])
        result['vs_min_time'] = min_record['time']
        result['vs_at_min_enstrophy'] = min_record['enstrophy']
    else:
        result['vs_min'] = float('inf')
        result['vs_mean'] = float('inf')
        result['vs_min_time'] = 0

    # All 8 inequality minimums
    for ineq_name in INEQUALITY_PAIRS.keys():
        key = f'slack_{ineq_name}'
        vals = [r[key] for r in ts if key in r and np.isfinite(r[key]) and r[key] < 1e15]
        if vals:
            result[f'{ineq_name}_min'] = min(vals)
            result[f'{ineq_name}_mean'] = np.mean(vals)
        else:
            result[f'{ineq_name}_min'] = float('inf')
            result[f'{ineq_name}_mean'] = float('inf')

    # Peak enstrophy
    enstrophy_vals = [r['enstrophy'] for r in ts]
    if enstrophy_vals:
        result['peak_enstrophy'] = max(enstrophy_vals)
        peak_record = max(ts, key=lambda r: r['enstrophy'])
        result['peak_enstrophy_time'] = peak_record['time']
        if vs_key in peak_record:
            result['vs_at_peak_enstrophy'] = peak_record[vs_key]

    return result


def run_all_ics(ic_names, Re_list, N=64, T_final=5.0, n_samples=100):
    """Run simulations for all specified ICs and Re values."""
    constants = compute_constants_on_torus(N_sum=30)

    all_results = {}

    for ic_name in ic_names:
        ic_info = IC_REGISTRY[ic_name]
        all_results[ic_name] = {'name': ic_info['name'], 'runs': {}}

        for Re in Re_list:
            nu = 1.0 / Re
            solver = NavierStokesSolver(N, nu, cfl=0.5)

            print(f"\n{'='*70}")
            print(f"IC: {ic_info['name']} | Re={Re} | N={N} | T={T_final}")
            print(f"{'='*70}")

            ux_hat, uy_hat, uz_hat = create_ic(solver, ic_name)

            result = run_simulation(
                solver, ux_hat, uy_hat, uz_hat,
                T_final, n_samples=n_samples,
                constants=constants, verbose=True,
                label=f"{ic_name}_Re{Re}"
            )

            summary = analyze_vs_slack(result['time_series'])
            summary['N'] = N
            summary['Re'] = Re
            summary['n_steps'] = result['n_steps']
            summary['wall_time'] = result['wall_time']

            all_results[ic_name]['runs'][Re] = summary

            # Print VS slack summary
            print(f"\n  VS Slack Summary:")
            print(f"    Min: {summary['vs_min']:.2f}×")
            print(f"    Mean: {summary['vs_mean']:.2f}×")
            print(f"    Time of min: t={summary.get('vs_min_time', 'N/A'):.3f}")
            print(f"    Peak enstrophy: {summary.get('peak_enstrophy', 'N/A'):.6f}")

    return all_results


def print_comparison_table(all_results, Re_list):
    """Print the comparison table of VS slack across ICs."""
    print(f"\n{'='*100}")
    print(f"VORTEX STRETCHING SLACK COMPARISON TABLE")
    print(f"{'='*100}")

    header = f"{'IC':<30}"
    for Re in Re_list:
        header += f" | Re={Re:>5} min"
    header += f" | {'Overall Min':>12} | {'vs TGV':>8}"
    print(header)
    print("-"*100)

    # Get TGV baseline
    tgv_min = float('inf')
    if 'taylor_green' in all_results:
        for Re, summary in all_results['taylor_green']['runs'].items():
            if summary['vs_min'] < tgv_min:
                tgv_min = summary['vs_min']

    for ic_name, ic_data in all_results.items():
        row = f"{ic_data['name']:<30}"
        overall_min = float('inf')

        for Re in Re_list:
            if Re in ic_data['runs']:
                vs_min = ic_data['runs'][Re]['vs_min']
                overall_min = min(overall_min, vs_min)
                row += f" | {vs_min:>11.2f}×"
            else:
                row += f" | {'N/A':>12}"

        if np.isfinite(overall_min) and np.isfinite(tgv_min) and tgv_min > 0:
            ratio = overall_min / tgv_min
            row += f" | {overall_min:>12.2f}× | {ratio:>7.2f}×"
        else:
            row += f" | {overall_min:>12.2f}× | {'N/A':>8}"

        print(row)

    print("="*100)


def main():
    parser = argparse.ArgumentParser(description='Run multi-IC vortex stretching slack measurements')
    parser.add_argument('--ics', nargs='+', default=list(IC_REGISTRY.keys()))
    parser.add_argument('--re', type=int, nargs='+', default=[100, 500, 1000])
    parser.add_argument('--N', type=int, default=64)
    parser.add_argument('--T', type=float, default=5.0)
    parser.add_argument('--samples', type=int, default=100)
    parser.add_argument('--output', type=str, default='multi_ic_results.json')
    args = parser.parse_args()

    all_results = run_all_ics(args.ics, args.re, N=args.N, T_final=args.T,
                               n_samples=args.samples)

    print_comparison_table(all_results, args.re)

    # Save results
    outpath = os.path.join(os.path.dirname(__file__), '..', args.output)
    serializable = {}
    for ic_name, ic_data in all_results.items():
        serializable[ic_name] = {
            'name': ic_data['name'],
            'runs': {str(Re): summary for Re, summary in ic_data['runs'].items()}
        }

    with open(outpath, 'w') as f:
        json.dump(serializable, f, indent=2,
                  default=lambda x: float(x) if isinstance(x, (np.floating, np.integer)) else str(x))
    print(f"\nResults saved to {outpath}")


if __name__ == '__main__':
    main()
