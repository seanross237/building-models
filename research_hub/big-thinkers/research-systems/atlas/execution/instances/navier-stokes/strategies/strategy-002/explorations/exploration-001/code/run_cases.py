#!/usr/bin/env python3
"""
Run BKM comparison cases incrementally, saving each result.
"""

import numpy as np
import json
import os
import sys
import time as time_module
from ns_solver import (NavierStokesSolver, taylor_green_ic,
                       random_gaussian_ic, antiparallel_tubes_ic)

# Constants
C_L = 0.827
C_CZ = 0.24

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)

PROGRESS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'progress.txt')


def log(msg):
    with open(PROGRESS_FILE, 'a') as f:
        f.write(f"[{time_module.strftime('%H:%M:%S')}] {msg}\n")
    print(msg, flush=True)


def compute_diagnostics(solver, ux_hat, uy_hat, uz_hat):
    """Compute all BKM vs Ladyzhenskaya diagnostics."""
    N = solver.N
    vol = (2 * np.pi)**3
    norm_factor = vol / N**6

    ux = solver.to_physical(ux_hat)
    uy = solver.to_physical(uy_hat)
    uz = solver.to_physical(uz_hat)

    dux_dx = solver.to_physical(1j * solver.KX * ux_hat)
    dux_dy = solver.to_physical(1j * solver.KY * ux_hat)
    dux_dz = solver.to_physical(1j * solver.KZ * ux_hat)
    duy_dx = solver.to_physical(1j * solver.KX * uy_hat)
    duy_dy = solver.to_physical(1j * solver.KY * uy_hat)
    duy_dz = solver.to_physical(1j * solver.KZ * uy_hat)
    duz_dx = solver.to_physical(1j * solver.KX * uz_hat)
    duz_dy = solver.to_physical(1j * solver.KY * uz_hat)
    duz_dz = solver.to_physical(1j * solver.KZ * uz_hat)

    omega_x = duz_dy - duy_dz
    omega_y = dux_dz - duz_dx
    omega_z = duy_dx - dux_dy

    S11 = dux_dx
    S22 = duy_dy
    S33 = duz_dz
    S12 = 0.5 * (dux_dy + duy_dx)
    S13 = 0.5 * (dux_dz + duz_dx)
    S23 = 0.5 * (duy_dz + duz_dy)

    vs_integrand = (S11 * omega_x**2 + S22 * omega_y**2 + S33 * omega_z**2 +
                    2*S12 * omega_x * omega_y + 2*S13 * omega_x * omega_z +
                    2*S23 * omega_y * omega_z)
    vortex_stretching = float(np.mean(vs_integrand) * vol)

    omega_sq = omega_x**2 + omega_y**2 + omega_z**2
    omega_L2_sq = float(np.mean(omega_sq) * vol)
    omega_L2 = float(np.sqrt(max(omega_L2_sq, 0)))
    omega_Linf = float(np.sqrt(np.max(omega_sq)))

    # grad omega via spectral
    omega_x_hat = 1j * (solver.KY * uz_hat - solver.KZ * uy_hat)
    omega_y_hat = 1j * (solver.KZ * ux_hat - solver.KX * uz_hat)
    omega_z_hat = 1j * (solver.KX * uy_hat - solver.KY * ux_hat)

    grad_omega_L2_sq = float(norm_factor * (
        np.sum(solver.K2 * np.abs(omega_x_hat)**2) +
        np.sum(solver.K2 * np.abs(omega_y_hat)**2) +
        np.sum(solver.K2 * np.abs(omega_z_hat)**2)
    ).real)
    grad_omega_L2 = float(np.sqrt(max(grad_omega_L2_sq, 0)))

    # Strain L^inf (Frobenius upper bound for speed)
    S_Frob_sq = S11**2 + S22**2 + S33**2 + 2*S12**2 + 2*S13**2 + 2*S23**2
    S_Linf = float(np.sqrt(np.max(S_Frob_sq)))

    u_sq = ux**2 + uy**2 + uz**2
    energy = float(0.5 * np.mean(u_sq) * vol)
    enstrophy = 0.5 * omega_L2_sq

    dissipation = solver.nu * grad_omega_L2_sq

    # Ladyzhenskaya bound
    VS_Lad = C_L**2 * omega_L2**1.5 * grad_omega_L2**1.5

    # BKM bound
    log_ratio = 0.0
    if omega_L2 > 1e-14 and grad_omega_L2 > omega_L2:
        log_ratio = np.log(grad_omega_L2 / omega_L2)
    log_factor = 1.0 + log_ratio

    VS_BKM = C_CZ * omega_L2_sq * omega_Linf * log_factor

    # Direct bound (no CZ, use measured strain)
    VS_BKM_direct = omega_L2_sq * S_Linf

    # Empirical C_CZ
    abs_vs = abs(vortex_stretching)
    denom = omega_L2_sq * omega_Linf * log_factor
    C_CZ_emp = abs_vs / denom if denom > 1e-20 else None

    # Slacks
    if abs_vs > 1e-20:
        slack_Lad = VS_Lad / abs_vs
        slack_BKM = VS_BKM / abs_vs
        slack_direct = VS_BKM_direct / abs_vs
        advantage = VS_Lad / VS_BKM if VS_BKM > 1e-20 else float('inf')
    else:
        slack_Lad = float('inf')
        slack_BKM = float('inf')
        slack_direct = float('inf')
        advantage = float('nan')

    # ODE RHS (before and after Young's)
    RHS_Lad = VS_Lad - dissipation
    RHS_BKM = VS_BKM - dissipation
    RHS_actual = vortex_stretching - dissipation

    # Ladyzhenskaya Young's optimized: d/dt y <= alpha_Lad * y^3
    alpha_Lad = 27 * C_L**8 / (128 * solver.nu**3)
    RHS_Lad_Young = alpha_Lad * omega_L2_sq**3

    # BKM Young's (dropping dissipation): d/dt y <= 2*C_CZ*y*omega_Linf*log_factor
    RHS_BKM_Young = 2 * C_CZ * omega_L2_sq * omega_Linf * log_factor

    omega_ratio = omega_Linf / omega_L2 if omega_L2 > 1e-14 else None

    return {
        'energy': energy,
        'enstrophy': enstrophy,
        'omega_L2': omega_L2,
        'omega_L2_sq': omega_L2_sq,
        'omega_Linf': omega_Linf,
        'grad_omega_L2': grad_omega_L2,
        'S_Linf': S_Linf,
        'vortex_stretching': vortex_stretching,
        'abs_vs': abs_vs,
        'VS_Lad': VS_Lad,
        'VS_BKM': VS_BKM,
        'VS_BKM_direct': VS_BKM_direct,
        'slack_Lad': slack_Lad,
        'slack_BKM': slack_BKM,
        'slack_direct': slack_direct,
        'advantage': advantage,
        'C_CZ_emp': C_CZ_emp,
        'RHS_actual': RHS_actual,
        'RHS_Lad': RHS_Lad,
        'RHS_BKM': RHS_BKM,
        'RHS_Lad_Young': RHS_Lad_Young,
        'RHS_BKM_Young': RHS_BKM_Young,
        'dissipation': dissipation,
        'omega_ratio': omega_ratio,
        'log_factor': log_factor,
        'alpha_Lad': alpha_Lad,
    }


def compute_blowup(diag_list, nu):
    """Compute blow-up times from diagnostic history."""
    if len(diag_list) < 3:
        return {'T_Lad': float('inf'), 'T_BKM': float('inf'), 'T_ratio': float('nan'),
                'alpha_fit': float('nan'), 'C_fit': float('nan')}

    d0 = diag_list[0]
    y0 = d0['omega_L2_sq']
    alpha_Lad = d0['alpha_Lad']

    T_Lad = 1.0 / (2 * alpha_Lad * y0**2) if alpha_Lad > 0 and y0 > 0 else float('inf')

    # Fit omega_Linf ~ C * y^alpha
    ys = np.array([d['omega_L2_sq'] for d in diag_list])
    oLinfs = np.array([d['omega_Linf'] for d in diag_list])
    lfs = np.array([d['log_factor'] for d in diag_list])

    mask = (ys > 1e-14) & (oLinfs > 1e-14)
    if np.sum(mask) > 3:
        log_y = np.log(ys[mask])
        log_o = np.log(oLinfs[mask])
        coeffs = np.polyfit(log_y, log_o, 1)
        alpha_fit = float(coeffs[0])
        C_fit = float(np.exp(coeffs[1]))
        mean_lf = float(np.mean(lfs[mask]))
    else:
        alpha_fit = 0.5
        C_fit = 1.0
        mean_lf = 1.0

    # BKM ODE: d/dt y = 2*C_CZ*C_fit*mean_lf * y^{1+alpha_fit}
    beta = 2 * C_CZ * C_fit * mean_lf
    if alpha_fit > 0.01 and y0 > 0:
        T_BKM = 1.0 / (beta * alpha_fit * y0**alpha_fit)
    else:
        T_BKM = float('inf')

    T_ratio = T_BKM / T_Lad if T_Lad > 0 and T_Lad < 1e30 else float('inf')

    return {
        'T_Lad': T_Lad,
        'T_BKM': T_BKM,
        'T_ratio': T_ratio,
        'alpha_fit': alpha_fit,
        'C_fit': C_fit,
        'mean_log_factor': mean_lf,
        'y0': y0,
        'alpha_Lad': alpha_Lad,
    }


def run_case(N, Re, ic_name, T_final=5.0, save_dt=0.05):
    """Run one simulation and return results."""
    nu = 1.0 / Re
    solver = NavierStokesSolver(N, nu, cfl=0.5)

    log(f"Starting: N={N}, Re={Re}, IC={ic_name}, T={T_final}")

    if ic_name == 'TGV':
        ux_hat, uy_hat, uz_hat = taylor_green_ic(solver)
    elif ic_name == 'Gaussian':
        ux_hat, uy_hat, uz_hat = random_gaussian_ic(solver)
    elif ic_name == 'AntiParallel':
        ux_hat, uy_hat, uz_hat = antiparallel_tubes_ic(solver)
    else:
        raise ValueError(f"Unknown IC: {ic_name}")

    times = [0.0]
    diag_list = [compute_diagnostics(solver, ux_hat, uy_hat, uz_hat)]

    t = 0.0
    next_save = save_dt
    step = 0
    t_wall = time_module.time()

    while t < T_final:
        dt = solver.compute_dt(ux_hat, uy_hat, uz_hat)
        dt = min(dt, T_final - t, 0.05)  # cap dt at 0.05 for safety

        if dt < 1e-12:
            log(f"  dt too small at t={t:.4f}")
            break

        ux_hat, uy_hat, uz_hat = solver.rk4_step(ux_hat, uy_hat, uz_hat, dt)
        t += dt
        step += 1

        if t >= next_save or t >= T_final - 1e-10:
            diag = compute_diagnostics(solver, ux_hat, uy_hat, uz_hat)
            times.append(t)
            diag_list.append(diag)
            next_save += save_dt

        if step % 200 == 0:
            elapsed = time_module.time() - t_wall
            log(f"  step={step}, t={t:.3f}/{T_final}, E={diag_list[-1]['enstrophy']:.3e}, dt={dt:.2e}, wall={elapsed:.0f}s")

    elapsed = time_module.time() - t_wall
    blowup = compute_blowup(diag_list, nu)

    log(f"Done: N={N}, Re={Re}, IC={ic_name}, steps={step}, wall={elapsed:.1f}s")
    log(f"  T_Lad={blowup['T_Lad']:.3e}, T_BKM={blowup['T_BKM']:.3e}, ratio={blowup['T_ratio']:.2f}, alpha_fit={blowup['alpha_fit']:.3f}")

    return {
        'N': N, 'Re': Re, 'ic_name': ic_name, 'nu': nu,
        'times': times, 'diagnostics': diag_list,
        'blowup': blowup, 'n_steps': step, 'wall_time': elapsed,
    }


def sanitize(obj):
    """Make JSON-safe."""
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize(v) for v in obj]
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        v = float(obj)
        return str(v) if (np.isnan(v) or np.isinf(v)) else v
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, np.ndarray):
        return sanitize(obj.tolist())
    elif isinstance(obj, float):
        return str(obj) if (np.isnan(obj) or np.isinf(obj)) else obj
    return obj


def save_result(result, filename):
    filepath = os.path.join(RESULTS_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(sanitize(result), f, indent=2)
    log(f"Saved: {filepath}")


def main():
    log("=" * 60)
    log("BKM Enstrophy Bypass — Incremental Runner")
    log("=" * 60)

    cases = [
        # (N, Re, IC, T_final)
        # TGV first (fast, known to work)
        (64, 100, 'TGV', 5.0),
        (64, 500, 'TGV', 5.0),
        (64, 1000, 'TGV', 5.0),
        (64, 5000, 'TGV', 2.0),
        # Gaussian IC
        (64, 100, 'Gaussian', 5.0),
        (64, 500, 'Gaussian', 3.0),
        (64, 1000, 'Gaussian', 2.0),
        (64, 5000, 'Gaussian', 1.0),
        # AntiParallel
        (64, 100, 'AntiParallel', 5.0),
        (64, 500, 'AntiParallel', 3.0),
        (64, 1000, 'AntiParallel', 2.0),
        (64, 5000, 'AntiParallel', 1.0),
        # Convergence check
        (128, 1000, 'TGV', 3.0),
    ]

    all_results = []
    for N, Re, ic, T in cases:
        fname = f"result_{ic}_Re{Re}_N{N}.json"
        fpath = os.path.join(RESULTS_DIR, fname)

        # Skip if already computed
        if os.path.exists(fpath):
            log(f"Skipping (already exists): {fname}")
            with open(fpath) as f:
                all_results.append(json.load(f))
            continue

        try:
            result = run_case(N, Re, ic, T_final=T)
            save_result(result, fname)
            all_results.append(result)
        except Exception as e:
            log(f"FAILED: {ic} Re={Re} N={N}: {e}")
            import traceback
            traceback.print_exc()

    # Save combined results
    save_result(all_results, 'all_results.json')
    log("All cases complete.")


if __name__ == '__main__':
    main()
