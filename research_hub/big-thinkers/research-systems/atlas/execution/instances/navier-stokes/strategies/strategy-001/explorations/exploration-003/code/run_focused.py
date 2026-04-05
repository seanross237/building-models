#!/usr/bin/env python3
"""
Focused simulation runner: measures VS slack for each IC at N=64.
Normalizes by peak velocity (max|u| ≈ 1) for comparable CFL timesteps.
"""

import numpy as np
import json
import time
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from ns_solver import NavierStokesSolver
from slack_measurements import (
    compute_extended_diagnostics, compute_all_slacks,
    compute_constants_on_torus, INEQUALITY_PAIRS
)
from initial_conditions import (
    taylor_green_ic, abc_flow_ic, random_gaussian_ic,
    vortex_tube_ic, anti_parallel_tubes_ic,
    project_and_dealias
)
from numpy.fft import fftn


def normalize_peak_velocity(solver, ux_hat, uy_hat, uz_hat, target_umax=1.0):
    """Normalize so max|u| ≈ target_umax."""
    ux = solver.to_physical(ux_hat)
    uy = solver.to_physical(uy_hat)
    uz = solver.to_physical(uz_hat)
    u_max = np.sqrt(np.max(ux**2 + uy**2 + uz**2))
    if u_max > 1e-14:
        scale = target_umax / u_max
        return ux_hat * scale, uy_hat * scale, uz_hat * scale
    return ux_hat, uy_hat, uz_hat


def run_and_measure(solver, ux_hat, uy_hat, uz_hat, T_final, n_samples,
                    constants, label=""):
    """Run simulation and return VS slack time series."""
    N = solver.N
    nu = solver.nu
    K2 = solver.K2
    norm_factor = (2*np.pi)**3 / N**6

    diag0 = compute_extended_diagnostics(solver, ux_hat, uy_hat, uz_hat)
    initial_energy_L2_sq = diag0['u_L2_sq']
    cumulative_dissipation = 0.0

    t = 0.0
    step = 0
    dt_sample = T_final / n_samples
    next_sample = 0.0
    records = []

    wall_start = time.time()

    while t < T_final:
        dt = solver.compute_dt(ux_hat, uy_hat, uz_hat)
        dt = min(dt, T_final - t)
        if dt < 1e-12:
            break

        ux_hat_new, uy_hat_new, uz_hat_new = solver.rk4_step(ux_hat, uy_hat, uz_hat, dt)

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
                'energy': float(diag['energy']),
                'enstrophy': float(diag['enstrophy']),
                'vs_actual': float(slacks['E2E3_Vortex_Stretching']['actual']),
                'vs_bound': float(slacks['E2E3_Vortex_Stretching']['bound']),
                'vs_slack': float(slacks['E2E3_Vortex_Stretching']['slack']),
            }
            # Also record other key slacks
            for name in ['F1_Ladyzhenskaya', 'F3_Sobolev_H1_L6', 'F4G1_Agmon']:
                record[f'slack_{name}'] = float(slacks[name]['slack'])

            records.append(record)
            next_sample += dt_sample

    wall_time = time.time() - wall_start
    return records, step, wall_time


def analyze_records(records):
    """Extract summary statistics from time series."""
    if not records:
        return {'vs_min': float('inf')}

    # Skip initial 20% for transient
    n_skip = max(1, len(records) // 5)
    recs = records[n_skip:]

    vs_slacks = [r['vs_slack'] for r in recs if np.isfinite(r['vs_slack']) and r['vs_slack'] < 1e15]

    if not vs_slacks:
        return {'vs_min': float('inf'), 'vs_mean': float('inf')}

    min_idx = np.argmin(vs_slacks)
    min_rec = [r for r in recs if np.isfinite(r['vs_slack']) and r['vs_slack'] < 1e15][min_idx]

    result = {
        'vs_min': min(vs_slacks),
        'vs_mean': float(np.mean(vs_slacks)),
        'vs_std': float(np.std(vs_slacks)),
        'vs_min_time': min_rec['time'],
        'peak_enstrophy': max(r['enstrophy'] for r in recs),
    }

    # Other inequality minimums
    for ineq in ['F1_Ladyzhenskaya', 'F3_Sobolev_H1_L6', 'F4G1_Agmon']:
        key = f'slack_{ineq}'
        vals = [r[key] for r in recs if key in r and np.isfinite(r[key]) and r[key] < 1e15]
        result[f'{ineq}_min'] = min(vals) if vals else float('inf')

    return result


def main():
    N = 64
    T_final = 5.0
    n_samples = 100
    constants = compute_constants_on_torus(N_sum=30)

    Re_list = [100, 500, 1000]

    # Define ICs with their creation functions
    ic_defs = {
        'taylor_green': {
            'name': 'Taylor-Green Vortex',
            'create': lambda solver: taylor_green_ic(solver),
            'normalize': False,  # TGV already has peak|u| ~ 1
        },
        'abc': {
            'name': 'ABC Flow (A=B=C=1)',
            'create': lambda solver: abc_flow_ic(solver, A=1, B=1, C=1),
            'normalize': True,
        },
        'random_gaussian': {
            'name': 'Random-Phase Gaussian',
            'create': lambda solver: random_gaussian_ic(solver, k_peak=4, seed=42),
            'normalize': True,
        },
        'vortex_tube': {
            'name': 'Vortex Tube (z-perturbed)',
            'create': lambda solver: vortex_tube_ic(solver, sigma=0.2, Gamma=1.0, perturb_amp=0.3),
            'normalize': True,
        },
        'anti_parallel': {
            'name': 'Anti-Parallel Tubes (z-perturbed)',
            'create': lambda solver: anti_parallel_tubes_ic(solver, d=np.pi/2, sigma=0.2, Gamma=1.0, perturb_amp=0.5),
            'normalize': True,
        },
    }

    all_results = {}

    for ic_key, ic_def in ic_defs.items():
        all_results[ic_key] = {'name': ic_def['name'], 'runs': {}}

        for Re in Re_list:
            nu = 1.0 / Re
            solver = NavierStokesSolver(N, nu, cfl=0.5)

            ux_hat, uy_hat, uz_hat = ic_def['create'](solver)

            if ic_def['normalize']:
                ux_hat, uy_hat, uz_hat = normalize_peak_velocity(
                    solver, ux_hat, uy_hat, uz_hat, target_umax=1.0)

            # Check initial state
            ux = solver.to_physical(ux_hat)
            uy = solver.to_physical(uy_hat)
            uz = solver.to_physical(uz_hat)
            vol = (2*np.pi)**3
            E = 0.5 * np.mean(ux**2 + uy**2 + uz**2) * vol
            u_max = np.sqrt(np.max(ux**2 + uy**2 + uz**2))

            print(f"\n{'='*70}")
            print(f"IC: {ic_def['name']} | Re={Re} | N={N}")
            print(f"  E={E:.4f}, max|u|={u_max:.4f}")
            print(f"{'='*70}")

            records, n_steps, wall_time = run_and_measure(
                solver, ux_hat, uy_hat, uz_hat,
                T_final, n_samples, constants,
                label=f"{ic_key}_Re{Re}"
            )

            summary = analyze_records(records)
            summary['N'] = N
            summary['Re'] = Re
            summary['n_steps'] = n_steps
            summary['wall_time'] = wall_time
            summary['initial_energy'] = float(E)
            summary['initial_umax'] = float(u_max)

            all_results[ic_key]['runs'][Re] = summary

            vs_min = summary.get('vs_min', float('inf'))
            vs_mean = summary.get('vs_mean', float('inf'))
            print(f"  Completed: {n_steps} steps in {wall_time:.1f}s")
            if np.isfinite(vs_min):
                print(f"  VS Slack: min={vs_min:.2f}×, mean={vs_mean:.2f}×, "
                      f"t_min={summary.get('vs_min_time', 0):.3f}")
            else:
                print(f"  VS Slack: inf (no measurable vortex stretching)")

        # Save intermediate results
        outpath = os.path.join(os.path.dirname(__file__), '..', 'focused_results.json')
        serializable = {}
        for k, v in all_results.items():
            serializable[k] = {
                'name': v['name'],
                'runs': {str(re): s for re, s in v['runs'].items()}
            }
        with open(outpath, 'w') as f:
            json.dump(serializable, f, indent=2,
                      default=lambda x: float(x) if isinstance(x, (np.floating, np.integer)) else str(x))
        print(f"\n  [Intermediate results saved]")

    # Final comparison table
    print(f"\n\n{'='*100}")
    print(f"VORTEX STRETCHING SLACK COMPARISON TABLE")
    print(f"{'='*100}")

    tgv_min = float('inf')
    if 'taylor_green' in all_results:
        for Re, s in all_results['taylor_green']['runs'].items():
            if s['vs_min'] < tgv_min:
                tgv_min = s['vs_min']

    header = f"{'IC':<35}"
    for Re in Re_list:
        header += f" | {'Re='+str(Re):>12}"
    header += f" | {'Min':>8} | {'vs TGV':>8} | {'Agmon':>8}"
    print(header)
    print("-"*100)

    for ic_key, ic_data in all_results.items():
        row = f"{ic_data['name']:<35}"
        overall_min = float('inf')
        agmon_min = float('inf')

        for Re in Re_list:
            if Re in ic_data['runs']:
                s = ic_data['runs'][Re]
                vs_min = s['vs_min']
                overall_min = min(overall_min, vs_min)
                agmon_val = s.get('F4G1_Agmon_min', float('inf'))
                agmon_min = min(agmon_min, agmon_val)

                if np.isfinite(vs_min):
                    row += f" | {vs_min:>10.1f}×"
                else:
                    row += f" | {'inf':>11}"
            else:
                row += f" | {'N/A':>12}"

        if np.isfinite(overall_min) and np.isfinite(tgv_min) and tgv_min > 0:
            ratio = overall_min / tgv_min
            row += f" | {overall_min:>6.1f}× | {ratio:>6.2f}× | {agmon_min:>6.1f}×"
        elif np.isfinite(overall_min):
            row += f" | {overall_min:>6.1f}× | {'N/A':>8} | {agmon_min:>6.1f}×"
        else:
            row += f" | {'inf':>8} | {'N/A':>8} | {agmon_min:>6.1f}×"

        print(row)

    print("="*100)

    # Print time series for the IC with lowest slack
    print(f"\nTime series for lowest-slack IC:")
    best_ic = None
    best_min = float('inf')
    for ic_key, ic_data in all_results.items():
        for Re, s in ic_data['runs'].items():
            if s['vs_min'] < best_min:
                best_min = s['vs_min']
                best_ic = (ic_key, Re)

    if best_ic:
        print(f"  {all_results[best_ic[0]]['name']} at Re={best_ic[1]}: min VS slack = {best_min:.2f}×")


if __name__ == '__main__':
    main()
