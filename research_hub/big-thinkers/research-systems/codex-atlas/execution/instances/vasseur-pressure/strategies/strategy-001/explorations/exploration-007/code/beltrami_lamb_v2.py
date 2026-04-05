"""
Exploration 007 v2: Beltrami deficit of u_below + Hessian/Remainder decomposition.

CRITICAL FIX: The truncation u_below = u * min(1, lambda_k/|u|) is NOT divergence-free,
even when u is. The identity d_id_j(u_iu_j) = Delta(|u|^2/2) + div(omega x u)
ONLY holds when div(u) = 0.

CORRECT DECOMPOSITION:
  P_total: from -Delta P = d_id_j(u_{b,i} u_{b,j})   [Poisson solve]
  P_hessian = -|u_b|^2/2                                [analytic, CZ-lossless]
  P_remainder = P_total - P_hessian                      [everything else: Lamb + compressibility]

For exact Beltrami + div-free: P_remainder = 0
For near-Beltrami with small div: P_remainder is small
This is the correct proxy for "how much CZ-lossy pressure is in the bottleneck."
"""

import sys
import os
import json
import time
import numpy as np
from numpy.fft import fftn, ifftn, fftfreq

SOLVER_PATH = '/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/vasseur-pressure/strategies/strategy-001/explorations/exploration-002/code'
sys.path.insert(0, SOLVER_PATH)
from ns_solver import NavierStokesSolver

EXPLORATION_DIR = '/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/vasseur-pressure/strategies/strategy-001/explorations/exploration-007'
PROGRESS_FILE = os.path.join(EXPLORATION_DIR, 'progress_v2.txt')
RESULTS_FILE = os.path.join(EXPLORATION_DIR, 'code', 'results_v2.json')


def log_progress(msg):
    with open(PROGRESS_FILE, 'a') as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    print(msg, flush=True)


# ============================================================
# Initial Conditions
# ============================================================

def abc_flow_ic(solver, A=1.0, B=1.0, C=1.0):
    X, Y, Z = solver.X, solver.Y, solver.Z
    ux = B * np.sin(Y) + C * np.cos(Z)
    uy = C * np.sin(Z) + A * np.cos(X)
    uz = A * np.sin(X) + B * np.cos(Y)
    ux_hat = solver.to_spectral(ux)
    uy_hat = solver.to_spectral(uy)
    uz_hat = solver.to_spectral(uz)
    ux_hat, uy_hat, uz_hat = solver.project(ux_hat, uy_hat, uz_hat)
    return solver.dealias(ux_hat), solver.dealias(uy_hat), solver.dealias(uz_hat)


def taylor_green_ic(solver):
    X, Y, Z = solver.X, solver.Y, solver.Z
    ux = np.sin(X) * np.cos(Y) * np.cos(Z)
    uy = -np.cos(X) * np.sin(Y) * np.cos(Z)
    uz = np.zeros_like(X)
    ux_hat, uy_hat, uz_hat = solver.project(
        solver.to_spectral(ux), solver.to_spectral(uy), solver.to_spectral(uz))
    return solver.dealias(ux_hat), solver.dealias(uy_hat), solver.dealias(uz_hat)


def random_gaussian_ic(solver, seed=42):
    rng = np.random.RandomState(seed)
    N = solver.N
    ux_hat = rng.randn(N, N, N) + 1j * rng.randn(N, N, N)
    uy_hat = rng.randn(N, N, N) + 1j * rng.randn(N, N, N)
    uz_hat = rng.randn(N, N, N) + 1j * rng.randn(N, N, N)
    K_mag = solver.K_mag
    K_mag_safe = np.where(K_mag == 0, 1, K_mag)
    envelope = K_mag_safe**(-5.0/6.0) * np.exp(-K_mag_safe**2 / (2 * (N/4)**2))
    envelope[0, 0, 0] = 0
    ux_hat *= envelope
    uy_hat *= envelope
    uz_hat *= envelope
    ux_hat, uy_hat, uz_hat = solver.project(ux_hat, uy_hat, uz_hat)
    ux_hat = solver.dealias(ux_hat)
    uy_hat = solver.dealias(uy_hat)
    uz_hat = solver.dealias(uz_hat)
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
    'ABC': abc_flow_ic,
    'TaylorGreen': taylor_green_ic,
    'RandomGauss': random_gaussian_ic,
}


# ============================================================
# Core Computations
# ============================================================

def compute_u_below(solver, ux_hat, uy_hat, uz_hat, k_level, norm_factor):
    """
    Compute u_below = u_norm * min(1, lambda_k / |u_norm|).
    Also returns u_norm and speed for reuse.
    """
    ux = solver.to_physical(solver.dealias(ux_hat)) / norm_factor
    uy = solver.to_physical(solver.dealias(uy_hat)) / norm_factor
    uz = solver.to_physical(solver.dealias(uz_hat)) / norm_factor

    threshold_k = 1.0 - 2.0**(-k_level)
    speed = np.sqrt(ux**2 + uy**2 + uz**2)
    speed_safe = np.maximum(speed, 1e-30)

    factor = np.minimum(1.0, threshold_k / speed_safe)
    factor = np.where(speed < 1e-30, 1.0, factor)

    ub_x = ux * factor
    ub_y = uy * factor
    ub_z = uz * factor

    return ub_x, ub_y, ub_z, ux, uy, uz, speed


def spectral_curl_from_physical(solver, ux, uy, uz):
    """Compute curl from physical-space fields."""
    ux_hat = solver.dealias(solver.to_spectral(ux))
    uy_hat = solver.dealias(solver.to_spectral(uy))
    uz_hat = solver.dealias(solver.to_spectral(uz))
    wx = solver.to_physical(1j * solver.KY * uz_hat - 1j * solver.KZ * uy_hat)
    wy = solver.to_physical(1j * solver.KZ * ux_hat - 1j * solver.KX * uz_hat)
    wz = solver.to_physical(1j * solver.KX * uy_hat - 1j * solver.KY * ux_hat)
    return wx, wy, wz


def spectral_div(solver, fx, fy, fz):
    """Compute divergence from physical-space vector field."""
    fx_hat = solver.dealias(solver.to_spectral(fx))
    fy_hat = solver.dealias(solver.to_spectral(fy))
    fz_hat = solver.dealias(solver.to_spectral(fz))
    div_hat = 1j * (solver.KX * fx_hat + solver.KY * fy_hat + solver.KZ * fz_hat)
    return solver.to_physical(div_hat)


def compute_beltrami_deficit(solver, ub_x, ub_y, ub_z):
    """
    Beltrami deficit:
      lambda_opt = <curl(u), u> / ||u||^2
      B = ||curl(u) - lambda_opt * u||_L2 / ||u||_L2
    """
    vol = (2 * np.pi)**3
    dV = vol / solver.N**3

    wx, wy, wz = spectral_curl_from_physical(solver, ub_x, ub_y, ub_z)

    curl_dot_u = np.sum(wx * ub_x + wy * ub_y + wz * ub_z) * dV
    u_sq = np.sum(ub_x**2 + ub_y**2 + ub_z**2) * dV

    if u_sq < 1e-30:
        return 0.0, 0.0

    lambda_opt = curl_dot_u / u_sq

    residual_sq = np.sum(
        (wx - lambda_opt * ub_x)**2 +
        (wy - lambda_opt * ub_y)**2 +
        (wz - lambda_opt * ub_z)**2
    ) * dV

    B_deficit = np.sqrt(residual_sq / u_sq)
    return lambda_opt, B_deficit


def compute_pressure_decomposition(solver, ub_x, ub_y, ub_z):
    """
    Correct decomposition of the pressure P_k^{21}:

    P_total: from -Delta P = d_id_j(u_{b,i} u_{b,j})
    P_hessian = -|u_b|^2/2  (analytic Bernoulli piece)
    P_remainder = P_total - P_hessian  (Lamb + compressibility)

    Also computes div(u_below) to quantify incompressibility violation.
    """
    N = solver.N
    K = [solver.KX, solver.KY, solver.KZ]
    vol = (2 * np.pi)**3
    dV = vol / N**3

    u_b = [ub_x, ub_y, ub_z]

    # --- P_total from Poisson: -Delta P = d_id_j(u_{b,i} u_{b,j}) ---
    rhs_hat = np.zeros((N, N, N), dtype=complex)
    for i in range(3):
        for j in range(3):
            uiuj_hat = fftn(u_b[i] * u_b[j])
            rhs_hat += K[i] * K[j] * uiuj_hat

    P_total_hat = rhs_hat / solver.K2_safe
    P_total_hat[0, 0, 0] = 0
    P_total = ifftn(P_total_hat).real

    # --- P_hessian = -|u_b|^2/2 (exact, no Poisson needed) ---
    half_speed_sq = 0.5 * (ub_x**2 + ub_y**2 + ub_z**2)
    P_hessian = -half_speed_sq
    # Remove mean to match P_total (zero mean)
    P_hessian = P_hessian - np.mean(P_hessian)

    # --- P_remainder = P_total - P_hessian ---
    P_remainder = P_total - P_hessian

    # --- Divergence of u_below ---
    div_ub = spectral_div(solver, ub_x, ub_y, ub_z)
    div_ub_L2 = np.sqrt(np.sum(div_ub**2) * dV)
    div_ub_Linf = np.max(np.abs(div_ub))

    # --- Also compute Lamb vector ||omega x u|| for reference ---
    wx, wy, wz = spectral_curl_from_physical(solver, ub_x, ub_y, ub_z)
    Lx = wy * ub_z - wz * ub_y
    Ly = wz * ub_x - wx * ub_z
    Lz = wx * ub_y - wy * ub_x
    Lamb_L2 = np.sqrt(np.sum(Lx**2 + Ly**2 + Lz**2) * dV)

    # --- Norms ---
    P_total_L2 = np.sqrt(np.sum(P_total**2) * dV)
    P_hessian_L2 = np.sqrt(np.sum(P_hessian**2) * dV)
    P_remainder_L2 = np.sqrt(np.sum(P_remainder**2) * dV)

    P_total_Linf = np.max(np.abs(P_total))
    P_hessian_Linf = np.max(np.abs(P_hessian))
    P_remainder_Linf = np.max(np.abs(P_remainder))

    # Verification: P_total = P_hessian + P_remainder by construction (exact)
    verify_err = np.max(np.abs(P_total - P_hessian - P_remainder))

    # Hessian fraction = ||P_hessian||_L2 / ||P_total||_L2
    hessian_frac = P_hessian_L2 / max(P_total_L2, 1e-30)
    remainder_frac = P_remainder_L2 / max(P_total_L2, 1e-30)

    return {
        'P_total': P_total,
        'P_hessian': P_hessian,
        'P_remainder': P_remainder,
        'P_total_L2': float(P_total_L2),
        'P_hessian_L2': float(P_hessian_L2),
        'P_remainder_L2': float(P_remainder_L2),
        'P_total_Linf': float(P_total_Linf),
        'P_hessian_Linf': float(P_hessian_Linf),
        'P_remainder_Linf': float(P_remainder_Linf),
        'hessian_frac_L2': float(hessian_frac),
        'remainder_frac_L2': float(remainder_frac),
        'Lamb_L2': float(Lamb_L2),
        'div_ub_L2': float(div_ub_L2),
        'div_ub_Linf': float(div_ub_Linf),
        'verify_err': float(verify_err),
    }


def compute_bottleneck_contributions(solver, ub_x, ub_y, ub_z,
                                     ux_norm, uy_norm, uz_norm,
                                     k_level, P_total, P_hessian, P_remainder):
    """
    Bottleneck integral contributions from each pressure piece.

    I_k = int |P| * |d_k| * 1_{v_k>0} dx

    For P_total, P_hessian, P_remainder separately.
    """
    vol = (2 * np.pi)**3
    N = solver.N
    dV = vol / N**3

    u_mag_norm = np.sqrt(ux_norm**2 + uy_norm**2 + uz_norm**2)
    threshold_k = 1.0 - 2.0**(-k_level)
    v_k = np.maximum(u_mag_norm - threshold_k, 0.0)
    active = v_k > 0

    if not np.any(active):
        return 0.0, 0.0, 0.0

    # Compute |d_k|
    ux_hat = solver.dealias(solver.to_spectral(ux_norm))
    uy_hat = solver.dealias(solver.to_spectral(uy_norm))
    uz_hat = solver.dealias(solver.to_spectral(uz_norm))

    dux_dx = solver.to_physical(1j * solver.KX * ux_hat)
    dux_dy = solver.to_physical(1j * solver.KY * ux_hat)
    dux_dz = solver.to_physical(1j * solver.KZ * ux_hat)
    duy_dx = solver.to_physical(1j * solver.KX * uy_hat)
    duy_dy = solver.to_physical(1j * solver.KY * uy_hat)
    duy_dz = solver.to_physical(1j * solver.KZ * uy_hat)
    duz_dx = solver.to_physical(1j * solver.KX * uz_hat)
    duz_dy = solver.to_physical(1j * solver.KY * uz_hat)
    duz_dz = solver.to_physical(1j * solver.KZ * uz_hat)

    grad_u_sq = (dux_dx**2 + dux_dy**2 + dux_dz**2 +
                 duy_dx**2 + duy_dy**2 + duy_dz**2 +
                 duz_dx**2 + duz_dy**2 + duz_dz**2)

    u_mag_safe = np.where(u_mag_norm > 1e-14, u_mag_norm, 1.0)
    grad_umag_x = (ux_norm * dux_dx + uy_norm * duy_dx + uz_norm * duz_dx) / u_mag_safe
    grad_umag_y = (ux_norm * dux_dy + uy_norm * duy_dy + uz_norm * duz_dy) / u_mag_safe
    grad_umag_z = (ux_norm * dux_dz + uy_norm * duy_dz + uz_norm * duz_dz) / u_mag_safe

    mask_zero = u_mag_norm < 1e-14
    grad_umag_x[mask_zero] = 0.0
    grad_umag_y[mask_zero] = 0.0
    grad_umag_z[mask_zero] = 0.0
    grad_umag_sq = grad_umag_x**2 + grad_umag_y**2 + grad_umag_z**2

    term1 = np.where(u_mag_norm > 1e-14, (v_k / u_mag_safe) * grad_umag_sq, 0.0)
    term2 = np.zeros_like(v_k)
    term2[active] = (threshold_k / u_mag_safe[active]) * grad_u_sq[active]
    dk_sq = term1 + term2
    dk_abs = np.sqrt(np.maximum(dk_sq, 0.0))

    active_float = active.astype(float)
    I_total = np.sum(np.abs(P_total) * dk_abs * active_float) * dV
    I_hessian = np.sum(np.abs(P_hessian) * dk_abs * active_float) * dV
    I_remainder = np.sum(np.abs(P_remainder) * dk_abs * active_float) * dV

    return float(I_total), float(I_hessian), float(I_remainder)


# ============================================================
# Also verify: for the INITIAL (t=0) ABC flow (exact Beltrami),
# check that Beltrami deficit is truly zero and P_remainder ~ 0
# ============================================================

def verify_abc_initial(N=64):
    """
    Sanity check: for the exact ABC flow at t=0 (before any evolution),
    verify Beltrami deficit = 0 and P_remainder ~ 0 for all k.
    """
    log_progress("\n" + "="*60)
    log_progress("SANITY CHECK: ABC flow at t=0 (exact Beltrami)")
    log_progress("="*60)

    solver = NavierStokesSolver(N, 1.0, cfl=0.4)  # nu doesn't matter for t=0
    ux_hat, uy_hat, uz_hat = abc_flow_ic(solver)

    ux = solver.to_physical(solver.dealias(ux_hat))
    uy = solver.to_physical(solver.dealias(uy_hat))
    uz = solver.to_physical(solver.dealias(uz_hat))
    speed = np.sqrt(ux**2 + uy**2 + uz**2)
    norm_factor = np.max(speed)

    log_progress(f"  norm_factor = {norm_factor:.6f}")

    # Check full field is Beltrami
    ux_n = ux / norm_factor
    uy_n = uy / norm_factor
    uz_n = uz / norm_factor
    lambda_opt_full, B_full = compute_beltrami_deficit(solver, ux_n, uy_n, uz_n)
    log_progress(f"  Full field: B_deficit = {B_full:.2e}, lambda_opt = {lambda_opt_full:.6f}")

    # Check div(u) = 0 for full field
    div_u = spectral_div(solver, ux_n, uy_n, uz_n)
    log_progress(f"  div(u_full) L2 = {np.sqrt(np.mean(div_u**2)):.2e}")

    results = {'k': [], 'B_deficit': [], 'div_ub_L2': [], 'remainder_frac': [],
               'hessian_frac': [], 'Lamb_L2': []}

    for k in range(9):
        ub_x, ub_y, ub_z, ux_norm, uy_norm, uz_norm, spd = compute_u_below(
            solver, ux_hat, uy_hat, uz_hat, k, norm_factor)

        lambda_opt, B_deficit = compute_beltrami_deficit(solver, ub_x, ub_y, ub_z)
        decomp = compute_pressure_decomposition(solver, ub_x, ub_y, ub_z)

        results['k'].append(k)
        results['B_deficit'].append(B_deficit)
        results['div_ub_L2'].append(decomp['div_ub_L2'])
        results['remainder_frac'].append(decomp['remainder_frac_L2'])
        results['hessian_frac'].append(decomp['hessian_frac_L2'])
        results['Lamb_L2'].append(decomp['Lamb_L2'])

        threshold = 1.0 - 2.0**(-k)
        frac_above = np.mean(spd / norm_factor > threshold)
        log_progress(f"  k={k}: B={B_deficit:.6f}, div_ub={decomp['div_ub_L2']:.4e}, "
                   f"H_frac={decomp['hessian_frac_L2']:.4f}, R_frac={decomp['remainder_frac_L2']:.4f}, "
                   f"Lamb={decomp['Lamb_L2']:.4e}, frac_above={frac_above:.4f}")

    return results


# ============================================================
# Main Runner
# ============================================================

def run_all():
    with open(PROGRESS_FILE, 'w') as f:
        f.write(f"Exploration 007 v2 started: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # First: sanity check at t=0
    sanity_results = verify_abc_initial(N=64)

    ic_names = ['ABC', 'TaylorGreen', 'RandomGauss']
    re_values = [100, 500, 1000]
    k_values = list(range(9))
    N_primary = 64

    all_results = {
        'sanity_check': sanity_results,
        'task_a': [],
        'task_b': [],
        'convergence': None,
    }

    for ic_name in ic_names:
        for Re in re_values:
            log_progress(f"\n{'='*60}")
            log_progress(f"IC={ic_name}, Re={Re}, N={N_primary}")
            log_progress(f"{'='*60}")

            try:
                nu = 1.0 / Re
                solver = NavierStokesSolver(N_primary, nu, cfl=0.4)
                ux_hat, uy_hat, uz_hat = IC_FUNCS[ic_name](solver)

                T_final = min(2.0 * np.pi / max(Re**0.5 * 0.01, 0.1), 5.0)
                T_final = max(T_final, 0.5)
                snap_interval = T_final / 10

                log_progress(f"  Evolving to T={T_final:.3f}...")
                _, _, _, snapshots = solver.run(ux_hat, uy_hat, uz_hat, T_final,
                                                 snapshot_interval=snap_interval)
                log_progress(f"  Got {len(snapshots)} snapshots")

                t_snap, ux_hat_snap, uy_hat_snap, uz_hat_snap = snapshots[-1]
                ux_phys = solver.to_physical(solver.dealias(ux_hat_snap))
                uy_phys = solver.to_physical(solver.dealias(uy_hat_snap))
                uz_phys = solver.to_physical(solver.dealias(uz_hat_snap))
                speed = np.sqrt(ux_phys**2 + uy_phys**2 + uz_phys**2)
                norm_factor = max(np.max(speed), 1e-30)
                log_progress(f"  norm_factor = {norm_factor:.6f}")

                # ---- TASK A ----
                task_a_entry = {
                    'ic': ic_name, 'Re': Re, 'N': N_primary,
                    'norm_factor': float(norm_factor),
                    'beltrami_deficits': [], 'lambda_opts': [],
                    'div_ub_L2': [], 'div_ub_Linf': [],
                }

                for k in k_values:
                    ub_x, ub_y, ub_z, ux_n, uy_n, uz_n, spd = compute_u_below(
                        solver, ux_hat_snap, uy_hat_snap, uz_hat_snap, k, norm_factor)
                    lambda_opt, B_deficit = compute_beltrami_deficit(solver, ub_x, ub_y, ub_z)

                    # Measure divergence of u_below
                    div_ub = spectral_div(solver, ub_x, ub_y, ub_z)
                    div_L2 = float(np.sqrt(np.mean(div_ub**2) * (2*np.pi)**3))
                    div_Linf = float(np.max(np.abs(div_ub)))

                    task_a_entry['beltrami_deficits'].append(float(B_deficit))
                    task_a_entry['lambda_opts'].append(float(lambda_opt))
                    task_a_entry['div_ub_L2'].append(div_L2)
                    task_a_entry['div_ub_Linf'].append(div_Linf)

                # Full field Beltrami deficit
                lambda_full, B_full = compute_beltrami_deficit(
                    solver, ux_phys/norm_factor, uy_phys/norm_factor, uz_phys/norm_factor)
                task_a_entry['B_full'] = float(B_full)
                task_a_entry['lambda_opt_full'] = float(lambda_full)

                log_progress(f"  Task A: B_full={B_full:.6f}")
                for k in [0, 2, 4, 6, 8]:
                    log_progress(f"    k={k}: B={task_a_entry['beltrami_deficits'][k]:.6f}, "
                               f"div_ub={task_a_entry['div_ub_L2'][k]:.4e}")

                all_results['task_a'].append(task_a_entry)

                # ---- TASK B ----
                task_b_entry = {
                    'ic': ic_name, 'Re': Re, 'N': N_primary,
                    'k_results': [],
                }

                for k in k_values:
                    ub_x, ub_y, ub_z, ux_n, uy_n, uz_n, spd = compute_u_below(
                        solver, ux_hat_snap, uy_hat_snap, uz_hat_snap, k, norm_factor)

                    decomp = compute_pressure_decomposition(solver, ub_x, ub_y, ub_z)

                    I_total, I_hessian, I_remainder = compute_bottleneck_contributions(
                        solver, ub_x, ub_y, ub_z, ux_n, uy_n, uz_n, k,
                        decomp['P_total'], decomp['P_hessian'], decomp['P_remainder'])

                    remainder_bn_frac = I_remainder / max(I_total, 1e-30) if I_total > 1e-30 else 0.0

                    k_result = {
                        'k': k,
                        'P_total_L2': decomp['P_total_L2'],
                        'P_hessian_L2': decomp['P_hessian_L2'],
                        'P_remainder_L2': decomp['P_remainder_L2'],
                        'hessian_frac_L2': decomp['hessian_frac_L2'],
                        'remainder_frac_L2': decomp['remainder_frac_L2'],
                        'Lamb_L2': decomp['Lamb_L2'],
                        'div_ub_L2': decomp['div_ub_L2'],
                        'div_ub_Linf': decomp['div_ub_Linf'],
                        'I_total': I_total,
                        'I_hessian': I_hessian,
                        'I_remainder': I_remainder,
                        'remainder_bn_frac': float(remainder_bn_frac),
                    }
                    task_b_entry['k_results'].append(k_result)

                log_progress(f"  Task B summary:")
                for k in [0, 2, 4, 6, 8]:
                    kr = task_b_entry['k_results'][k]
                    log_progress(f"    k={k}: H_frac={kr['hessian_frac_L2']:.4f}, "
                               f"R_frac={kr['remainder_frac_L2']:.4f}, "
                               f"R_bn_frac={kr['remainder_bn_frac']:.4f}")

                all_results['task_b'].append(task_b_entry)

                # Save incrementally
                with open(RESULTS_FILE, 'w') as f:
                    json.dump(all_results, f, indent=2)

            except Exception as e:
                log_progress(f"  ERROR: {e}")
                import traceback
                traceback.print_exc()

    # ---- Convergence check: ABC Re=500, N=128 ----
    log_progress(f"\n{'='*60}")
    log_progress("CONVERGENCE CHECK: ABC Re=500, N=128")
    log_progress(f"{'='*60}")

    try:
        Re = 500; N_conv = 128; nu = 1.0 / Re
        solver = NavierStokesSolver(N_conv, nu, cfl=0.4)
        ux_hat, uy_hat, uz_hat = abc_flow_ic(solver)

        T_final = min(2.0 * np.pi / max(Re**0.5 * 0.01, 0.1), 5.0)
        T_final = max(T_final, 0.5)
        snap_interval = T_final / 10

        log_progress(f"  Evolving to T={T_final:.3f}...")
        _, _, _, snapshots = solver.run(ux_hat, uy_hat, uz_hat, T_final,
                                         snapshot_interval=snap_interval)

        t_snap, ux_hat_snap, uy_hat_snap, uz_hat_snap = snapshots[-1]
        ux_phys = solver.to_physical(solver.dealias(ux_hat_snap))
        uy_phys = solver.to_physical(solver.dealias(uy_hat_snap))
        uz_phys = solver.to_physical(solver.dealias(uz_hat_snap))
        speed = np.sqrt(ux_phys**2 + uy_phys**2 + uz_phys**2)
        norm_factor = max(np.max(speed), 1e-30)

        conv_entry = {
            'ic': 'ABC', 'Re': Re, 'N': N_conv,
            'norm_factor': float(norm_factor),
            'beltrami_deficits': [], 'lambda_opts': [],
            'hessian_fracs': [], 'remainder_fracs': [],
            'remainder_bn_fracs': [], 'div_ub_L2s': [],
        }

        for k in k_values:
            ub_x, ub_y, ub_z, ux_n, uy_n, uz_n, spd = compute_u_below(
                solver, ux_hat_snap, uy_hat_snap, uz_hat_snap, k, norm_factor)
            lambda_opt, B_deficit = compute_beltrami_deficit(solver, ub_x, ub_y, ub_z)
            conv_entry['beltrami_deficits'].append(float(B_deficit))
            conv_entry['lambda_opts'].append(float(lambda_opt))

            decomp = compute_pressure_decomposition(solver, ub_x, ub_y, ub_z)
            conv_entry['hessian_fracs'].append(decomp['hessian_frac_L2'])
            conv_entry['remainder_fracs'].append(decomp['remainder_frac_L2'])
            conv_entry['div_ub_L2s'].append(decomp['div_ub_L2'])

            I_total, I_hessian, I_remainder = compute_bottleneck_contributions(
                solver, ub_x, ub_y, ub_z, ux_n, uy_n, uz_n, k,
                decomp['P_total'], decomp['P_hessian'], decomp['P_remainder'])
            r_frac = I_remainder / max(I_total, 1e-30) if I_total > 1e-30 else 0.0
            conv_entry['remainder_bn_fracs'].append(float(r_frac))

            if k in [0, 4, 8]:
                log_progress(f"  N=128 k={k}: B={B_deficit:.6f}, H_frac={decomp['hessian_frac_L2']:.4f}, "
                           f"R_bn_frac={r_frac:.4f}")

        all_results['convergence'] = conv_entry

    except Exception as e:
        log_progress(f"  CONVERGENCE CHECK ERROR: {e}")
        import traceback
        traceback.print_exc()

    # Save final
    with open(RESULTS_FILE, 'w') as f:
        json.dump(all_results, f, indent=2)

    log_progress(f"\nCompleted: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_progress("DONE")
    return all_results


if __name__ == '__main__':
    results = run_all()
