#!/usr/bin/env python3
"""
Adversarial parametric search for initial conditions that minimize
the vortex stretching slack ratio.

Strategy: grid search over anti-parallel tube parameters (d, σ, δ, tilt),
then refine with scipy.optimize around the best point found.

Uses N=32 for the search (speed), then validates best candidates at N=64.
"""

import numpy as np
import time
import sys
import os
import json
from itertools import product

sys.path.insert(0, os.path.dirname(__file__))
from ns_solver import NavierStokesSolver
from slack_measurements import (
    compute_extended_diagnostics, compute_all_slacks,
    compute_constants_on_torus
)
from initial_conditions import parametric_anti_parallel_ic, project_and_dealias, normalize_energy


def measure_min_vs_slack(solver, ux_hat, uy_hat, uz_hat, T_final, n_samples,
                          constants, nu):
    """Run a simulation and return the minimum VS slack ratio."""
    N = solver.N
    K2 = solver.K2
    norm_factor = (2*np.pi)**3 / N**6

    diag0 = compute_extended_diagnostics(solver, ux_hat, uy_hat, uz_hat)
    initial_energy_L2_sq = diag0['u_L2_sq']
    cumulative_dissipation = 0.0

    t = 0.0
    step = 0
    dt_sample = T_final / n_samples
    next_sample = 0.0
    min_vs_slack = float('inf')
    min_vs_time = 0.0

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
            vs_slack = slacks['E2E3_Vortex_Stretching']['slack']

            if np.isfinite(vs_slack) and vs_slack < min_vs_slack:
                min_vs_slack = vs_slack
                min_vs_time = t

            next_sample += dt_sample

    return min_vs_slack, min_vs_time


def grid_search(N=32, Re=100, T_final=3.0, n_samples=30):
    """Grid search over anti-parallel tube parameters."""
    nu = 1.0 / Re
    constants = compute_constants_on_torus(N_sum=20)

    # Parameter grid
    d_values = [0.3, 0.5, np.pi/4, np.pi/2, np.pi, 1.5]
    sigma_values = [0.15, 0.2, 0.3, 0.5, 0.8]
    perturb_values = [0.2, 0.5, 0.8, 1.2]
    tilt_values = [0.0, 0.3, 0.6, np.pi/4]

    # First pass: coarse grid (d, σ, δ) with tilt=0
    print(f"Phase 1: Coarse grid search ({len(d_values)}×{len(sigma_values)}×{len(perturb_values)} = {len(d_values)*len(sigma_values)*len(perturb_values)} points)")
    print(f"  N={N}, Re={Re}, T={T_final}")

    results = []
    best_slack = float('inf')
    best_params = None
    total = len(d_values) * len(sigma_values) * len(perturb_values)
    count = 0

    wall_start = time.time()

    for d in d_values:
        for sigma in sigma_values:
            for delta in perturb_values:
                count += 1
                params = {
                    'd': d,
                    'sigma': sigma,
                    'perturb_amp': delta,
                    'Gamma_ratio': -1.0,
                    'perturb_k': 1,
                    'tilt': 0.0,
                }

                try:
                    solver = NavierStokesSolver(N, nu, cfl=0.5)
                    ux_hat, uy_hat, uz_hat = parametric_anti_parallel_ic(solver, params)
                    min_slack, min_time = measure_min_vs_slack(
                        solver, ux_hat, uy_hat, uz_hat,
                        T_final, n_samples, constants, nu
                    )
                except Exception as e:
                    min_slack = float('inf')
                    min_time = 0.0

                result = {
                    'd': d, 'sigma': sigma, 'perturb_amp': delta,
                    'min_slack': min_slack, 'min_time': min_time,
                }
                results.append(result)

                if min_slack < best_slack:
                    best_slack = min_slack
                    best_params = params.copy()

                if count % 10 == 0:
                    elapsed = time.time() - wall_start
                    rate = count / elapsed
                    remaining = (total - count) / rate
                    print(f"  [{count}/{total}] best={best_slack:.1f}× "
                          f"(d={best_params['d']:.2f}, σ={best_params['sigma']:.2f}, δ={best_params['perturb_amp']:.2f}) "
                          f"[{remaining:.0f}s remaining]")

    print(f"\nPhase 1 complete in {time.time()-wall_start:.0f}s")
    print(f"Best: slack={best_slack:.2f}× at d={best_params['d']:.3f}, σ={best_params['sigma']:.3f}, δ={best_params['perturb_amp']:.3f}")

    # Phase 2: Add tilt to the best (d, σ, δ) combinations
    # Sort by slack, take top 5
    finite_results = [r for r in results if np.isfinite(r['min_slack'])]
    finite_results.sort(key=lambda r: r['min_slack'])
    top5 = finite_results[:5]

    print(f"\nPhase 2: Adding tilt dimension to top 5 configurations")
    phase2_results = []

    for base in top5:
        for tilt in tilt_values:
            params = {
                'd': base['d'],
                'sigma': base['sigma'],
                'perturb_amp': base['perturb_amp'],
                'Gamma_ratio': -1.0,
                'perturb_k': 1,
                'tilt': tilt,
            }

            try:
                solver = NavierStokesSolver(N, nu, cfl=0.5)
                ux_hat, uy_hat, uz_hat = parametric_anti_parallel_ic(solver, params)
                min_slack, min_time = measure_min_vs_slack(
                    solver, ux_hat, uy_hat, uz_hat,
                    T_final, n_samples, constants, nu
                )
            except Exception as e:
                min_slack = float('inf')
                min_time = 0.0

            result = {
                'd': base['d'], 'sigma': base['sigma'],
                'perturb_amp': base['perturb_amp'], 'tilt': tilt,
                'min_slack': min_slack, 'min_time': min_time,
            }
            phase2_results.append(result)

            if min_slack < best_slack:
                best_slack = min_slack
                best_params = params.copy()
                print(f"  New best: slack={best_slack:.2f}× (tilt={tilt:.3f})")

    # Phase 3: Gamma ratio exploration
    print(f"\nPhase 3: Exploring asymmetric circulations around best config")
    gamma_ratios = [-0.5, -0.7, -0.8, -0.9, -1.0, -1.1, -1.2, -1.5, -2.0]
    phase3_results = []

    for gr in gamma_ratios:
        params = dict(best_params)
        params['Gamma_ratio'] = gr

        try:
            solver = NavierStokesSolver(N, nu, cfl=0.5)
            ux_hat, uy_hat, uz_hat = parametric_anti_parallel_ic(solver, params)
            min_slack, min_time = measure_min_vs_slack(
                solver, ux_hat, uy_hat, uz_hat,
                T_final, n_samples, constants, nu
            )
        except Exception as e:
            min_slack = float('inf')
            min_time = 0.0

        result = dict(params)
        result['min_slack'] = min_slack
        result['min_time'] = min_time
        phase3_results.append(result)

        if min_slack < best_slack:
            best_slack = min_slack
            best_params = params.copy()
            print(f"  New best: slack={best_slack:.2f}× (Γ_ratio={gr:.2f})")

    # Summary
    print(f"\n{'='*60}")
    print(f"ADVERSARIAL SEARCH SUMMARY")
    print(f"{'='*60}")
    print(f"Best VS slack: {best_slack:.2f}×")
    print(f"Parameters:")
    for k, v in best_params.items():
        print(f"  {k}: {v:.4f}")

    # Save all results
    all_search_results = {
        'phase1': results,
        'phase2': phase2_results,
        'phase3': phase3_results,
        'best_params': {k: float(v) for k, v in best_params.items()},
        'best_slack': float(best_slack),
        'N': N,
        'Re': Re,
        'T_final': T_final,
    }

    return all_search_results


def validate_best(best_params, N_values=[64, 128], Re_values=[100, 500, 1000],
                   T_final=5.0, n_samples=100):
    """Validate the best configuration at higher resolution and multiple Re."""
    constants = compute_constants_on_torus(N_sum=30)
    validation_results = {}

    for N in N_values:
        for Re in Re_values:
            nu = 1.0 / Re
            solver = NavierStokesSolver(N, nu, cfl=0.5)

            print(f"\nValidation: N={N}, Re={Re}")
            ux_hat, uy_hat, uz_hat = parametric_anti_parallel_ic(solver, best_params)
            min_slack, min_time = measure_min_vs_slack(
                solver, ux_hat, uy_hat, uz_hat,
                T_final, n_samples, constants, nu
            )
            print(f"  Min VS slack: {min_slack:.2f}× at t={min_time:.3f}")

            validation_results[(N, Re)] = {
                'min_slack': float(min_slack),
                'min_time': float(min_time),
            }

    return validation_results


def main():
    print("Adversarial Parametric Search for Minimum VS Slack")
    print("="*60)

    # Phase 1-3: Grid search at N=32, Re=100
    search_results = grid_search(N=32, Re=100, T_final=3.0, n_samples=30)

    # Save intermediate results
    outdir = os.path.dirname(__file__)
    with open(os.path.join(outdir, '..', 'adversarial_results.json'), 'w') as f:
        json.dump(search_results, f, indent=2,
                  default=lambda x: float(x) if isinstance(x, (np.floating, np.integer)) else str(x))

    # Validate best at N=64 and multiple Re
    best_params = search_results['best_params']
    print(f"\nValidating best configuration at N=64...")
    validation = validate_best(best_params, N_values=[64], Re_values=[100, 500, 1000],
                                T_final=5.0, n_samples=100)

    search_results['validation'] = {f"N{N}_Re{Re}": v for (N, Re), v in validation.items()}

    with open(os.path.join(outdir, '..', 'adversarial_results.json'), 'w') as f:
        json.dump(search_results, f, indent=2,
                  default=lambda x: float(x) if isinstance(x, (np.floating, np.integer)) else str(x))

    print("\nDone! Results saved to adversarial_results.json")


if __name__ == '__main__':
    main()
