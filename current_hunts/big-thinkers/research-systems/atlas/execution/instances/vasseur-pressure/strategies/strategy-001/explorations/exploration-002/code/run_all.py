#!/usr/bin/env python3
"""
Main runner: DNS + De Giorgi level-set measurement across ICs and Reynolds numbers.

Outputs results to results.json and progress to progress.txt.
"""

import sys
import os
import json
import time
import traceback
import numpy as np

# Add code directory to path
CODE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CODE_DIR)

from ns_solver import NavierStokesSolver
from degiorgi_measure import (
    measure_degiorgi_sequence,
    compute_bottleneck_integral,
)

RESULTS_DIR = os.path.dirname(CODE_DIR)
PROGRESS_FILE = os.path.join(RESULTS_DIR, "progress.txt")
RESULTS_FILE = os.path.join(RESULTS_DIR, "results.json")


def log_progress(msg):
    with open(PROGRESS_FILE, "a") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    print(msg, flush=True)


# ============================================================
# Initial Conditions
# ============================================================

def taylor_green_ic(solver):
    """Taylor-Green vortex: u = (sin(x)cos(y)cos(z), -cos(x)sin(y)cos(z), 0)"""
    X, Y, Z = solver.X, solver.Y, solver.Z
    ux = np.sin(X) * np.cos(Y) * np.cos(Z)
    uy = -np.cos(X) * np.sin(Y) * np.cos(Z)
    uz = np.zeros_like(X)
    ux_hat, uy_hat, uz_hat = solver.project(
        solver.to_spectral(ux), solver.to_spectral(uy), solver.to_spectral(uz))
    return solver.dealias(ux_hat), solver.dealias(uy_hat), solver.dealias(uz_hat)


def antiparallel_vortex_tubes_ic(solver):
    """Two counter-rotating Gaussian vortex tubes along z-axis."""
    X, Y, Z = solver.X, solver.Y, solver.Z
    # Two tubes centered at (pi-0.5, pi, z) and (pi+0.5, pi, z)
    sigma = 0.4
    x1, y1 = np.pi - 0.5, np.pi
    x2, y2 = np.pi + 0.5, np.pi

    r1_sq = (X - x1)**2 + (Y - y1)**2
    r2_sq = (X - x2)**2 + (Y - y2)**2

    # Vorticity omega_z = +Gamma for tube 1, -Gamma for tube 2
    omega_z = np.exp(-r1_sq / (2*sigma**2)) - np.exp(-r2_sq / (2*sigma**2))

    # Get velocity from vorticity via stream function: -Delta psi = omega_z
    # u = d psi/dy, v = -d psi/dx
    omega_hat = solver.to_spectral(omega_z)
    psi_hat = omega_hat / solver.K2_safe
    psi_hat[0, 0, 0] = 0

    ux_hat = 1j * solver.KY * psi_hat
    uy_hat = -1j * solver.KX * psi_hat
    uz_hat = np.zeros_like(ux_hat)

    ux_hat, uy_hat, uz_hat = solver.project(ux_hat, uy_hat, uz_hat)
    ux_hat = solver.dealias(ux_hat)
    uy_hat = solver.dealias(uy_hat)
    uz_hat = solver.dealias(uz_hat)

    # Normalize to unit characteristic velocity
    ux = solver.to_physical(ux_hat)
    uy = solver.to_physical(uy_hat)
    u_max = max(np.max(np.abs(ux)), np.max(np.abs(uy)), 1e-14)
    ux_hat /= u_max
    uy_hat /= u_max
    uz_hat /= u_max

    return ux_hat, uy_hat, uz_hat


def random_gaussian_ic(solver, seed=42):
    """Random Gaussian with k^{-5/3} spectrum, projected to div-free."""
    rng = np.random.RandomState(seed)
    N = solver.N

    ux_hat = rng.randn(N, N, N) + 1j * rng.randn(N, N, N)
    uy_hat = rng.randn(N, N, N) + 1j * rng.randn(N, N, N)
    uz_hat = rng.randn(N, N, N) + 1j * rng.randn(N, N, N)

    K_mag = solver.K_mag
    K_mag_safe = np.where(K_mag == 0, 1, K_mag)

    # k^{-5/3} spectrum: amplitude ~ k^{-5/6} (energy ~ amplitude^2 ~ k^{-5/3})
    # But also cut off at high k to avoid aliasing
    envelope = K_mag_safe**(-5.0/6.0) * np.exp(-K_mag_safe**2 / (2 * (N/4)**2))
    envelope[0, 0, 0] = 0

    ux_hat *= envelope
    uy_hat *= envelope
    uz_hat *= envelope

    ux_hat, uy_hat, uz_hat = solver.project(ux_hat, uy_hat, uz_hat)
    ux_hat = solver.dealias(ux_hat)
    uy_hat = solver.dealias(uy_hat)
    uz_hat = solver.dealias(uz_hat)

    # Normalize to unit energy
    ux = solver.to_physical(ux_hat)
    uy = solver.to_physical(uy_hat)
    uz = solver.to_physical(uz_hat)
    E = 0.5 * np.mean(ux**2 + uy**2 + uz**2)
    if E > 0:
        scale = 1.0 / np.sqrt(2 * E)  # so 0.5 * mean(|u|^2) = 0.5
        ux_hat *= scale
        uy_hat *= scale
        uz_hat *= scale

    return ux_hat, uy_hat, uz_hat


def kida_vortex_ic(solver):
    """Kida-like symmetric vortex: high-symmetry vortex on T^3."""
    X, Y, Z = solver.X, solver.Y, solver.Z
    # Kida vortex: superposition of symmetric modes
    ux = np.sin(X) * (np.cos(3*Y) * np.cos(Z) - np.cos(Y) * np.cos(3*Z))
    uy = np.sin(Y) * (np.cos(3*Z) * np.cos(X) - np.cos(Z) * np.cos(3*X))
    uz = np.sin(Z) * (np.cos(3*X) * np.cos(Y) - np.cos(X) * np.cos(3*Y))

    ux_hat = solver.to_spectral(ux)
    uy_hat = solver.to_spectral(uy)
    uz_hat = solver.to_spectral(uz)

    ux_hat, uy_hat, uz_hat = solver.project(ux_hat, uy_hat, uz_hat)
    ux_hat = solver.dealias(ux_hat)
    uy_hat = solver.dealias(uy_hat)
    uz_hat = solver.dealias(uz_hat)

    # Normalize
    ux = solver.to_physical(ux_hat)
    uy = solver.to_physical(uy_hat)
    uz = solver.to_physical(uz_hat)
    E = 0.5 * np.mean(ux**2 + uy**2 + uz**2)
    if E > 0:
        scale = 1.0 / np.sqrt(2 * E)
        ux_hat *= scale
        uy_hat *= scale
        uz_hat *= scale

    return ux_hat, uy_hat, uz_hat


def abc_flow_ic(solver, A=1.0, B=1.0, C=1.0):
    """Arnold-Beltrami-Childress flow: exact eigenfunction of curl."""
    X, Y, Z = solver.X, solver.Y, solver.Z
    ux = B * np.sin(Y) + C * np.cos(Z)
    uy = C * np.sin(Z) + A * np.cos(X)
    uz = A * np.sin(X) + B * np.cos(Y)

    ux_hat = solver.to_spectral(ux)
    uy_hat = solver.to_spectral(uy)
    uz_hat = solver.to_spectral(uz)

    ux_hat, uy_hat, uz_hat = solver.project(ux_hat, uy_hat, uz_hat)
    ux_hat = solver.dealias(ux_hat)
    uy_hat = solver.dealias(uy_hat)
    uz_hat = solver.dealias(uz_hat)

    # Normalize to unit characteristic velocity
    ux = solver.to_physical(ux_hat)
    uy = solver.to_physical(uy_hat)
    uz = solver.to_physical(uz_hat)
    E = 0.5 * np.mean(ux**2 + uy**2 + uz**2)
    if E > 0:
        scale = 1.0 / np.sqrt(2 * E)
        ux_hat *= scale
        uy_hat *= scale
        uz_hat *= scale

    return ux_hat, uy_hat, uz_hat


IC_FUNCS = {
    'TaylorGreen': taylor_green_ic,
    'VortexTubes': antiparallel_vortex_tubes_ic,
    'RandomGauss': random_gaussian_ic,
    'KidaVortex': kida_vortex_ic,
    'ABC': abc_flow_ic,
}


# ============================================================
# Main Measurement
# ============================================================

def run_single_case(ic_name, Re, N, K_max=10, T_final=None, n_snapshots=20):
    """
    Run DNS and De Giorgi measurement for a single (IC, Re, N) case.

    T_final is chosen to be a few eddy turnover times.
    """
    nu = 1.0 / Re
    if T_final is None:
        # Eddy turnover time ~ L/U ~ 2pi/1 for unit velocity
        T_final = min(2.0 * np.pi / max(Re**0.5 * 0.01, 0.1), 5.0)
        T_final = max(T_final, 0.5)  # at least 0.5 time units

    log_progress(f"  Starting: IC={ic_name}, Re={Re}, N={N}, T_final={T_final:.3f}")

    solver = NavierStokesSolver(N, nu, cfl=0.4)
    snap_interval = T_final / n_snapshots

    # Initialize
    ic_func = IC_FUNCS[ic_name]
    ux_hat, uy_hat, uz_hat = ic_func(solver)

    # Check initial energy
    ux = solver.to_physical(ux_hat)
    uy = solver.to_physical(uy_hat)
    uz = solver.to_physical(uz_hat)
    E0 = 0.5 * np.mean(ux**2 + uy**2 + uz**2)
    log_progress(f"    Initial energy: {E0:.6f}")

    # Run DNS with snapshots
    t0 = time.time()
    _, _, _, snapshots = solver.run(ux_hat, uy_hat, uz_hat, T_final, snapshot_interval=snap_interval)
    dns_time = time.time() - t0
    log_progress(f"    DNS done in {dns_time:.1f}s, {len(snapshots)} snapshots")

    # Check final energy
    ux_f = solver.to_physical(snapshots[-1][1])
    uy_f = solver.to_physical(snapshots[-1][2])
    uz_f = solver.to_physical(snapshots[-1][3])
    E_final = 0.5 * np.mean(ux_f**2 + uy_f**2 + uz_f**2)
    log_progress(f"    Final energy: {E_final:.6f} (decay ratio: {E_final/max(E0,1e-30):.4f})")

    # De Giorgi measurement
    t0 = time.time()
    dg_result = measure_degiorgi_sequence(solver, snapshots, K_max=K_max)
    dg_time = time.time() - t0
    log_progress(f"    De Giorgi done in {dg_time:.1f}s")
    log_progress(f"    beta_eff = {dg_result['beta_eff']:.4f} +/- {dg_result['beta_stderr']:.4f}")
    log_progress(f"    U_0 = {dg_result['U_0_normalized']:.6f}, monotone = {dg_result['monotone']}")

    # Bottleneck integral for select k values
    t0 = time.time()
    bottleneck_exponents = []
    I_k_values = []

    # Measure I_k for k=2,...,min(K_max, 8)
    k_bn_max = min(dg_result['K_max_used'], 8)
    for k in range(2, k_bn_max + 1):
        if dg_result['U_k_values'][k] > 1e-30:
            I_k = compute_bottleneck_integral(solver, snapshots, k, dg_result['norm_factor'])
            I_k_values.append((k, I_k))

    bn_time = time.time() - t0
    log_progress(f"    Bottleneck done in {bn_time:.1f}s")

    # Fit bottleneck exponent: log(I_k) vs log(U_{k-1})
    bn_exponent = np.nan
    bn_stderr = np.nan
    if len(I_k_values) >= 3:
        ks_bn = [x[0] for x in I_k_values]
        Iks = [x[1] for x in I_k_values]

        valid_bn = [(k, Ik) for k, Ik in zip(ks_bn, Iks)
                     if Ik > 1e-30 and dg_result['U_k_values'][k-1] > 1e-30]

        if len(valid_bn) >= 3:
            log_Ik = np.array([np.log(x[1]) for x in valid_bn])
            log_Ukm1 = np.array([np.log(dg_result['U_k_values'][x[0]-1]) for x in valid_bn])

            # Simple linear regression: log(I_k) = alpha + gamma * log(U_{k-1})
            A_bn = np.column_stack([np.ones(len(log_Ukm1)), log_Ukm1])
            result_bn = np.linalg.lstsq(A_bn, log_Ik, rcond=None)
            bn_exponent = result_bn[0][1]

            n_bn = len(log_Ik)
            if n_bn > 2:
                y_pred = A_bn @ result_bn[0]
                mse = np.sum((log_Ik - y_pred)**2) / (n_bn - 2)
                try:
                    cov = mse * np.linalg.inv(A_bn.T @ A_bn)
                    bn_stderr = np.sqrt(max(cov[1, 1], 0))
                except:
                    bn_stderr = np.nan

    log_progress(f"    Bottleneck exponent: {bn_exponent:.4f} +/- {bn_stderr:.4f}")

    result = {
        'IC': ic_name,
        'Re': Re,
        'N': N,
        'T_final': T_final,
        'n_snapshots': len(snapshots),
        'E_initial': float(E0),
        'E_final': float(E_final),
        'norm_factor': float(dg_result['norm_factor']),
        'Linf': float(dg_result['Linf']),
        'U_0': float(dg_result['U_0_normalized']),
        'U_k_values': [float(x) for x in dg_result['U_k_values']],
        'K_max_used': int(dg_result['K_max_used']),
        'beta_eff': float(dg_result['beta_eff']),
        'beta_stderr': float(dg_result['beta_stderr']),
        'a_coeff': float(dg_result['a_coeff']),
        'fit_r2': float(dg_result['fit_r2']),
        'monotone': bool(dg_result['monotone']),
        'bottleneck_exponent': float(bn_exponent) if not np.isnan(bn_exponent) else None,
        'bottleneck_stderr': float(bn_stderr) if not np.isnan(bn_stderr) else None,
        'I_k_values': [(int(k), float(Ik)) for k, Ik in I_k_values],
        'log_ratios': [(int(k), float(r)) for k, r in dg_result['log_ratios'] if not np.isnan(r)],
        'decay_rates': [(int(k), float(r)) for k, r in dg_result['decay_rates'] if not np.isnan(r)],
        'dns_time_s': dns_time,
        'dg_time_s': dg_time,
        'bn_time_s': bn_time,
    }

    return result


def main():
    """Run all cases and save results."""
    log_progress("=" * 60)
    log_progress("De Giorgi Level-Set Iteration: Full Measurement Campaign")
    log_progress("=" * 60)

    all_results = []

    # Primary grid: 5 ICs x 3 Re values at N=64
    ic_names = ['TaylorGreen', 'VortexTubes', 'RandomGauss', 'KidaVortex', 'ABC']
    re_values = [100, 500, 1000]
    N_primary = 64
    K_max = 10

    for ic_name in ic_names:
        for Re in re_values:
            try:
                result = run_single_case(ic_name, Re, N_primary, K_max=K_max)
                all_results.append(result)

                # Save incrementally
                with open(RESULTS_FILE, 'w') as f:
                    json.dump(all_results, f, indent=2)

                log_progress(f"  => beta={result['beta_eff']:.4f}, "
                           f"R2={result['fit_r2']:.4f}, "
                           f"converged={result['monotone']}")
            except Exception as e:
                log_progress(f"  FAILED: {ic_name} Re={Re}: {e}")
                traceback.print_exc()

    log_progress("\n" + "=" * 60)
    log_progress("Convergence checks: N=128 for TaylorGreen and ABC")
    log_progress("=" * 60)

    # Convergence checks at N=128 for 2 ICs
    for ic_name in ['TaylorGreen', 'ABC']:
        for Re in [100, 500]:
            try:
                result = run_single_case(ic_name, Re, 128, K_max=K_max)
                result['convergence_check'] = True
                all_results.append(result)

                with open(RESULTS_FILE, 'w') as f:
                    json.dump(all_results, f, indent=2)

                log_progress(f"  => N=128: beta={result['beta_eff']:.4f}, "
                           f"R2={result['fit_r2']:.4f}")
            except Exception as e:
                log_progress(f"  FAILED N=128: {ic_name} Re={Re}: {e}")
                traceback.print_exc()

    # Higher Re if budget allows
    log_progress("\n" + "=" * 60)
    log_progress("High Re runs: Re=2000 for TaylorGreen and RandomGauss")
    log_progress("=" * 60)

    for ic_name in ['TaylorGreen', 'RandomGauss']:
        try:
            result = run_single_case(ic_name, 2000, N_primary, K_max=K_max)
            all_results.append(result)

            with open(RESULTS_FILE, 'w') as f:
                json.dump(all_results, f, indent=2)

            log_progress(f"  => Re=2000: beta={result['beta_eff']:.4f}")
        except Exception as e:
            log_progress(f"  FAILED Re=2000: {ic_name}: {e}")
            traceback.print_exc()

    # Final save
    with open(RESULTS_FILE, 'w') as f:
        json.dump(all_results, f, indent=2)

    log_progress("\n" + "=" * 60)
    log_progress("ALL DONE")
    log_progress("=" * 60)

    # Print summary table
    log_progress("\nSummary Table:")
    log_progress(f"{'IC':<15} {'Re':>5} {'N':>4} {'beta_eff':>10} {'stderr':>8} "
                f"{'K_max':>5} {'U_0':>8} {'U_Kmax':>10} {'Mono':>5} {'R2':>6}")
    log_progress("-" * 90)

    for r in all_results:
        U_last = r['U_k_values'][-1] if r['U_k_values'] else float('nan')
        log_progress(f"{r['IC']:<15} {r['Re']:>5} {r['N']:>4} "
                    f"{r['beta_eff']:>10.4f} {r['beta_stderr']:>8.4f} "
                    f"{r['K_max_used']:>5} {r['U_0']:>8.4f} "
                    f"{U_last:>10.2e} {'Y' if r['monotone'] else 'N':>5} "
                    f"{r['fit_r2']:>6.3f}")


if __name__ == '__main__':
    main()
