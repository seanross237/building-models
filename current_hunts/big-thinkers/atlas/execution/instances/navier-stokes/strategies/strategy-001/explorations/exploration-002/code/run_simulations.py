#!/usr/bin/env python3
"""
Run Taylor-Green vortex simulations and measure slack ratios for 8 NS inequalities.

Usage: python run_simulations.py [--re RE] [--N N] [--T T]
Default: runs all Re = 100, 500, 1000, 5000 at N=64 to T=5.
"""

import numpy as np
import json
import time
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(__file__))
from ns_solver import NavierStokesSolver, taylor_green_ic
from slack_measurements import (
    compute_extended_diagnostics, compute_all_slacks,
    compute_constants_on_torus, INEQUALITY_PAIRS
)


def check_resolution(diag, N):
    """
    Check if the simulation is adequately resolved.
    Returns (is_resolved, kmax_active, spectrum_ratio).

    Criterion: E(k > 2N/3) / E(k=1) < 1e-4
    """
    spec = diag['energy_spectrum']
    kmax_dealias = N // 3
    E1 = spec[1] if len(spec) > 1 else 1.0

    # Energy in the last 1/4 of the dealiased range
    k_check = max(1, int(0.75 * kmax_dealias))
    E_tail = np.mean(spec[k_check:kmax_dealias+1]) if k_check < len(spec) else 0

    ratio = E_tail / E1 if E1 > 1e-30 else 0
    is_resolved = ratio < 1e-4

    # Find k where E(k) drops below 1e-10 of E(1)
    kmax_active = 0
    for k in range(1, min(len(spec), kmax_dealias+1)):
        if spec[k] > 1e-10 * E1:
            kmax_active = k

    return is_resolved, kmax_active, ratio


def run_single_simulation(N, Re, T_final, n_samples=100, verbose=True):
    """
    Run a Taylor-Green vortex simulation and collect slack measurements.

    Args:
        N: grid resolution
        Re: Reynolds number
        T_final: final simulation time
        n_samples: number of diagnostic samples
        verbose: print progress

    Returns:
        results dict with time series of all slack ratios
    """
    nu = 1.0 / Re
    solver = NavierStokesSolver(N, nu, cfl=0.5)
    constants = compute_constants_on_torus(N_sum=30)

    if verbose:
        print(f"\n{'='*60}")
        print(f"Taylor-Green Vortex: N={N}, Re={Re}, ν={nu:.6f}, T={T_final}")
        print(f"{'='*60}")

    # Initial condition
    ux_hat, uy_hat, uz_hat = taylor_green_ic(solver, Re)

    # Initial diagnostics
    diag0 = compute_extended_diagnostics(solver, ux_hat, uy_hat, uz_hat)
    initial_energy_L2_sq = diag0['u_L2_sq']
    initial_energy = diag0['energy']

    if verbose:
        print(f"Initial: E={initial_energy:.6f}, ||u||_L2={diag0['u_L2']:.6f}, "
              f"enstrophy={diag0['enstrophy']:.6f}")

    # Time stepping
    t = 0.0
    step = 0
    dt_sample = T_final / n_samples
    next_sample = 0.0

    # Tracking
    cumulative_dissipation = 0.0  # 2ν ∫₀ᵗ ||∇u||² ds
    time_series = []
    resolution_warnings = []

    wall_start = time.time()

    while t < T_final:
        # Adaptive time step
        dt = solver.compute_dt(ux_hat, uy_hat, uz_hat)
        dt = min(dt, T_final - t)  # don't overshoot
        if dt < 1e-12:
            print(f"WARNING: dt too small ({dt:.2e}) at t={t:.4f}, stopping.")
            break

        # RK4 step
        ux_hat_new, uy_hat_new, uz_hat_new = solver.rk4_step(ux_hat, uy_hat, uz_hat, dt)

        # Accumulate dissipation: 2ν × ||∇u||² × dt (trapezoidal)
        # Use midpoint approximation: compute ||∇u||² at current state
        K2 = solver.K2
        norm_factor = (2*np.pi)**3 / N**6
        grad_sq_spectral = norm_factor * (np.sum(K2 * np.abs(ux_hat)**2) +
                                           np.sum(K2 * np.abs(uy_hat)**2) +
                                           np.sum(K2 * np.abs(uz_hat)**2)).real
        cumulative_dissipation += 2 * nu * grad_sq_spectral * dt

        ux_hat, uy_hat, uz_hat = ux_hat_new, uy_hat_new, uz_hat_new
        t += dt
        step += 1

        # Sample diagnostics
        if t >= next_sample - 1e-10:
            diag = compute_extended_diagnostics(solver, ux_hat, uy_hat, uz_hat)

            # Add energy inequality tracking quantities
            diag['initial_energy_L2_sq'] = initial_energy_L2_sq
            diag['cumulative_dissipation'] = cumulative_dissipation

            # Compute slacks
            slacks = compute_all_slacks(diag, constants)

            # Resolution check
            is_resolved, kmax_active, spec_ratio = check_resolution(diag, N)

            record = {
                'time': t,
                'step': step,
                'dt': dt,
                'energy': diag['energy'],
                'enstrophy': diag['enstrophy'],
                'u_L2': diag['u_L2'],
                'grad_u_L2': diag['grad_u_L2'],
                'omega_L2': diag['omega_L2'],
                'grad_omega_L2': diag['grad_omega_L2'],
                'u_H1': diag['u_H1'],
                'u_H2': diag['u_H2'],
                'u_H3': diag['u_H3'],
                'grad_u_Linf': diag['grad_u_Linf'],
                'u_dot_grad_u_L2': diag['u_dot_grad_u_L2'],
                'p_L32': diag['p_L32'],
                'vortex_stretching': diag['vortex_stretching'],
                'divergence_max': diag['divergence_max'],
                'cumulative_dissipation': cumulative_dissipation,
                'is_resolved': is_resolved,
                'kmax_active': kmax_active,
                'spec_ratio': spec_ratio,
                'energy_conservation_error': abs(diag['u_L2_sq'] + cumulative_dissipation - initial_energy_L2_sq) / initial_energy_L2_sq,
            }

            # Add slack ratios
            for name, s in slacks.items():
                record[f'slack_{name}'] = s['slack']
                record[f'bound_{name}'] = s['bound']
                record[f'actual_{name}'] = s['actual']

            time_series.append(record)

            if not is_resolved and t > 0.1:
                resolution_warnings.append((t, spec_ratio, kmax_active))

            if verbose and len(time_series) % 10 == 0:
                E_err = record['energy_conservation_error']
                print(f"  t={t:.3f}, step={step}, E={diag['energy']:.6f}, "
                      f"enstrophy={diag['enstrophy']:.6f}, E_err={E_err:.2e}, "
                      f"resolved={is_resolved}")

            next_sample += dt_sample

    wall_elapsed = time.time() - wall_start

    if verbose:
        print(f"\nCompleted: {step} steps in {wall_elapsed:.1f}s")
        if resolution_warnings:
            print(f"  Resolution warnings at {len(resolution_warnings)} timesteps")
            worst = max(resolution_warnings, key=lambda x: x[1])
            print(f"  Worst: t={worst[0]:.3f}, spec_ratio={worst[1]:.2e}, kmax_active={worst[2]}")

    # Compile results
    results = {
        'N': N,
        'Re': Re,
        'nu': nu,
        'T_final': T_final,
        'n_steps': step,
        'wall_time': wall_elapsed,
        'initial_energy': initial_energy,
        'initial_energy_L2_sq': initial_energy_L2_sq,
        'time_series': time_series,
        'resolution_warnings': len(resolution_warnings),
        'constants': {k: float(v) for k, v in constants.items()},
    }

    return results


def analyze_results(results):
    """
    Analyze slack ratio time series and produce summary statistics.
    """
    ts = results['time_series']
    if not ts:
        return {}

    Re = results['Re']
    ineq_names = list(INEQUALITY_PAIRS.keys())

    summary = {'Re': Re, 'N': results['N']}

    # Filter to t > 0.5 for time-averaged stats (skip initial transient)
    ts_filtered = [r for r in ts if r['time'] > 0.5]
    if not ts_filtered:
        ts_filtered = ts

    for name in ineq_names:
        key = f'slack_{name}'
        values = [r[key] for r in ts_filtered if key in r and np.isfinite(r[key]) and r[key] < 1e15]

        if values:
            summary[f'{name}_mean'] = np.mean(values)
            summary[f'{name}_std'] = np.std(values)
            summary[f'{name}_min'] = np.min(values)
            summary[f'{name}_max'] = np.max(values)

            # Find time of minimum slack
            min_idx = np.argmin(values)
            # Map back to find the time
            filtered_with_times = [(r['time'], r[key]) for r in ts_filtered
                                    if key in r and np.isfinite(r[key]) and r[key] < 1e15]
            if filtered_with_times:
                min_time = min(filtered_with_times, key=lambda x: x[1])[0]
                summary[f'{name}_min_time'] = min_time
        else:
            summary[f'{name}_mean'] = float('inf')
            summary[f'{name}_std'] = 0
            summary[f'{name}_min'] = float('inf')

    # Energy conservation check
    if ts_filtered:
        e_errors = [r['energy_conservation_error'] for r in ts_filtered]
        summary['energy_conservation_max_error'] = max(e_errors)
        summary['energy_conservation_mean_error'] = np.mean(e_errors)

    # Resolution check
    resolved_fraction = sum(1 for r in ts_filtered if r['is_resolved']) / len(ts_filtered) if ts_filtered else 0
    summary['resolved_fraction'] = resolved_fraction

    return summary


def print_summary_table(summaries):
    """Print the Slack Atlas Table."""
    ineq_names = list(INEQUALITY_PAIRS.keys())
    Re_values = sorted(set(s['Re'] for s in summaries))

    print("\n" + "="*120)
    print("SLACK ATLAS TABLE")
    print("="*120)

    header = f"{'Inequality':<25}"
    for Re in Re_values:
        header += f" | Re={Re:>5} (mean±std)"
    header += f" | {'Min Slack':>12} | {'@ Re':>6}"
    print(header)
    print("-"*120)

    for name in ineq_names:
        row = f"{name:<25}"
        min_slack_overall = float('inf')
        min_Re = None

        for Re in Re_values:
            s = next((s for s in summaries if s['Re'] == Re), None)
            if s and f'{name}_mean' in s and np.isfinite(s[f'{name}_mean']):
                mean = s[f'{name}_mean']
                std = s[f'{name}_std']
                row += f" | {mean:>8.2f} ± {std:<8.2f}"

                if s[f'{name}_min'] < min_slack_overall:
                    min_slack_overall = s[f'{name}_min']
                    min_Re = Re
            else:
                row += f" | {'inf':>20}"

        if min_Re is not None and np.isfinite(min_slack_overall):
            row += f" | {min_slack_overall:>12.4f} | {min_Re:>6}"
        else:
            row += f" | {'inf':>12} | {'N/A':>6}"

        print(row)

    print("="*120)

    # Energy conservation summary
    print("\nEnergy Conservation Check:")
    for Re in Re_values:
        s = next((s for s in summaries if s['Re'] == Re), None)
        if s:
            print(f"  Re={Re}: max error = {s.get('energy_conservation_max_error', 'N/A'):.2e}, "
                  f"resolved fraction = {s.get('resolved_fraction', 'N/A'):.1%}")


def main():
    parser = argparse.ArgumentParser(description='Run NS slack measurements')
    parser.add_argument('--re', type=int, nargs='+', default=[100, 500, 1000, 5000])
    parser.add_argument('--N', type=int, default=64)
    parser.add_argument('--T', type=float, default=5.0)
    parser.add_argument('--samples', type=int, default=100)
    parser.add_argument('--output', type=str, default='results.json')
    args = parser.parse_args()

    all_results = []
    all_summaries = []

    for Re in args.re:
        results = run_single_simulation(args.N, Re, args.T, n_samples=args.samples)
        summary = analyze_results(results)
        all_results.append(results)
        all_summaries.append(summary)

        # Save intermediate results
        outpath = os.path.join(os.path.dirname(__file__), '..', args.output)
        with open(outpath, 'w') as f:
            # Convert time_series to serializable format
            serializable = []
            for r in all_results:
                r_copy = dict(r)
                r_copy['time_series'] = r['time_series']  # already dicts of floats
                serializable.append(r_copy)
            json.dump({'results': serializable, 'summaries': all_summaries},
                      f, indent=2, default=lambda x: float(x) if isinstance(x, (np.floating, np.integer)) else str(x))

    print_summary_table(all_summaries)

    # Print time series for Re=1000 (or closest available)
    target_Re = 1000
    r1000 = next((r for r in all_results if r['Re'] == target_Re), all_results[-1])
    print(f"\n{'='*80}")
    print(f"Time Series: Re={r1000['Re']}, N={r1000['N']}")
    print(f"{'='*80}")
    print(f"{'t':>6} | {'Energy':>10} | {'F1_Lady':>8} | {'E2E3_VS':>8} | {'F4G1_Ag':>8} | {'E1_En':>8} | {'Resolved':>8}")
    print("-"*80)
    for r in r1000['time_series'][::max(1, len(r1000['time_series'])//20)]:
        f1 = r.get('slack_F1_Ladyzhenskaya', float('inf'))
        e2 = r.get('slack_E2E3_Vortex_Stretching', float('inf'))
        f4 = r.get('slack_F4G1_Agmon', float('inf'))
        e1 = r.get('slack_E1_Energy', float('inf'))
        print(f"{r['time']:>6.3f} | {r['energy']:>10.6f} | {min(f1,9999):>8.2f} | {min(e2,9999):>8.2f} | "
              f"{min(f4,9999):>8.2f} | {min(e1,9999):>8.4f} | {r['is_resolved']}")


if __name__ == '__main__':
    main()
