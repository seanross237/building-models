#!/usr/bin/env python3
"""
Task B: Multi-IC slack atlas validation.

Run the 8-inequality slack atlas from Strategy-001 on multiple ICs:
- Gaussian, Kida-like, Anti-parallel tubes at Re=500, 1000
"""
import numpy as np
import json, os, sys

S001_CODE = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'strategy-001', 'explorations', 'exploration-002', 'code')
E001_CODE = os.path.join(os.path.dirname(__file__), '..', '..', 'exploration-001', 'code')
sys.path.insert(0, S001_CODE)
sys.path.insert(0, E001_CODE)

from ns_solver import NavierStokesSolver, taylor_green_ic, random_gaussian_ic, antiparallel_tubes_ic
from slack_measurements import compute_constants_on_torus, compute_extended_diagnostics, compute_all_slacks, INEQUALITY_PAIRS

RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)


def kida_vortex_ic(solver):
    """Kida-Pelz type symmetric vortex (high-symmetry adversarial IC)."""
    X, Y, Z = solver.X, solver.Y, solver.Z
    ux = np.sin(X)*np.cos(Y)*np.cos(Z) - np.cos(X)*np.sin(Z)*np.cos(Y)
    uy = np.sin(Y)*np.cos(Z)*np.cos(X) - np.cos(Y)*np.sin(X)*np.cos(Z)
    uz = np.sin(Z)*np.cos(X)*np.cos(Y) - np.cos(Z)*np.sin(Y)*np.cos(X)
    ux_hat = solver.to_spectral(ux)
    uy_hat = solver.to_spectral(uy)
    uz_hat = solver.to_spectral(uz)
    ux_hat, uy_hat, uz_hat = solver.project(ux_hat, uy_hat, uz_hat)
    ux_hat = solver.dealias(ux_hat); uy_hat = solver.dealias(uy_hat); uz_hat = solver.dealias(uz_hat)
    return ux_hat, uy_hat, uz_hat


def run_simulation(solver, ux_hat, uy_hat, uz_hat, T_final, n_snapshots=20):
    """Run DNS and collect extended diagnostics at regular intervals."""
    constants = compute_constants_on_torus(N_sum=30)
    snapshots = []
    t = 0; step = 0
    dt_record = T_final / n_snapshots
    next_record = 0

    while t < T_final:
        dt = solver.compute_dt(ux_hat, uy_hat, uz_hat)
        dt = min(dt, T_final - t, 0.05)

        if t >= next_record - 1e-10:
            diag = compute_extended_diagnostics(solver, ux_hat, uy_hat, uz_hat)
            slacks = compute_all_slacks(diag, constants)
            snapshots.append({'t': t, 'diag': diag, 'slacks': slacks})
            next_record = t + dt_record

        ux_hat, uy_hat, uz_hat = solver.rk4_step(ux_hat, uy_hat, uz_hat, dt)
        t += dt; step += 1

    # Final snapshot
    diag = compute_extended_diagnostics(solver, ux_hat, uy_hat, uz_hat)
    slacks = compute_all_slacks(diag, constants)
    snapshots.append({'t': t, 'diag': diag, 'slacks': slacks})

    return snapshots


def run_task_b():
    """Run multi-IC slack atlas."""
    N = 64
    print("=" * 80)
    print("TASK B: MULTI-IC SLACK ATLAS VALIDATION")
    print("=" * 80)

    cases = [
        ("Gaussian", random_gaussian_ic, [500, 1000]),
        ("Kida", kida_vortex_ic, [500, 1000]),
        ("AntiParallel", antiparallel_tubes_ic, [500, 1000]),
        ("TGV", taylor_green_ic, [500, 1000]),  # reference
    ]

    all_results = []
    ineq_names = list(INEQUALITY_PAIRS.keys())

    for ic_name, ic_func, re_list in cases:
        for Re in re_list:
            nu = 1.0/Re
            solver = NavierStokesSolver(N, nu, cfl=0.3)
            ux_hat, uy_hat, uz_hat = ic_func(solver)
            T_final = min(3.0, 500*nu)

            print(f"\n  Running {ic_name} Re={Re} N={N} T={T_final:.1f}...")
            snapshots = run_simulation(solver, ux_hat, uy_hat, uz_hat, T_final, n_snapshots=15)
            print(f"    Collected {len(snapshots)} snapshots")

            # Extract minimum slacks
            min_slacks = {}
            for name in ineq_names:
                slack_vals = [s['slacks'][name]['slack'] for s in snapshots if s['slacks'][name]['slack'] < 1e15]
                if slack_vals:
                    min_slacks[name] = min(slack_vals)
                else:
                    min_slacks[name] = float('inf')

            case_result = {
                'ic': ic_name, 'Re': Re, 'N': N,
                'n_snapshots': len(snapshots),
                'min_slacks': min_slacks,
            }
            all_results.append(case_result)

            print(f"    Min slacks: " + ", ".join(f"{n.split('_')[0]}={min_slacks[n]:.1f}" for n in ineq_names if min_slacks[n] < 1e10))

    # Summary table
    print("\n" + "=" * 120)
    print("SLACK ATLAS SUMMARY")
    print("=" * 120)
    header = f"{'IC':>12} {'Re':>5} | " + " | ".join(f"{n[:12]:>12}" for n in ineq_names)
    print(header)
    print("-" * len(header))
    for r in all_results:
        row = f"{r['ic']:>12} {r['Re']:>5} | "
        row += " | ".join(f"{r['min_slacks'][n]:>12.1f}" if r['min_slacks'][n] < 1e10 else f"{'inf':>12}" for n in ineq_names)
        print(row)

    # IC-robustness analysis
    print("\n  IC-ROBUSTNESS ANALYSIS:")
    print("  Checking which Strategy-001 findings hold across ICs...")
    # For each inequality, check if the ORDERING of slacks is consistent
    for name in ineq_names:
        vals = [(r['ic'], r['Re'], r['min_slacks'][name]) for r in all_results if r['min_slacks'][name] < 1e10]
        if len(vals) >= 4:
            slack_range = max(v[2] for v in vals) / max(min(v[2] for v in vals), 1e-10)
            print(f"    {name:>25}: range factor={slack_range:>8.1f}x, " +
                  f"min={min(v[2] for v in vals):>8.1f}, max={max(v[2] for v in vals):>8.1f}")

    # Save
    save_data = []
    for r in all_results:
        sd = dict(r)
        sd['min_slacks'] = {k: float(v) for k,v in r['min_slacks'].items()}
        save_data.append(sd)
    with open(os.path.join(RESULTS_DIR, 'task_b_results.json'), 'w') as f:
        json.dump(save_data, f, indent=2)

    return all_results


if __name__ == '__main__':
    run_task_b()
