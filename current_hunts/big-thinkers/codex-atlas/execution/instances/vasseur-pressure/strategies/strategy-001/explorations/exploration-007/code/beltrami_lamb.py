"""
Exploration 007: Beltrami deficit of u_below + Hessian/Lamb decomposition.

Task A: Measure Beltrami deficit B_k = ||curl(u_below) - lambda_opt * u_below||_L2 / ||u_below||_L2
Task B: Decompose P_k^{21} pressure source into Hessian and Lamb pieces.

Uses NS solver and ICs from exploration-002.
"""

import sys
import os
import json
import time
import numpy as np
from numpy.fft import fftn, ifftn, fftfreq

# Add exploration-002 code to path
SOLVER_PATH = '/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/atlas/execution/instances/vasseur-pressure/strategies/strategy-001/explorations/exploration-002/code'
sys.path.insert(0, SOLVER_PATH)
from ns_solver import NavierStokesSolver

EXPLORATION_DIR = '/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/atlas/execution/instances/vasseur-pressure/strategies/strategy-001/explorations/exploration-007'
PROGRESS_FILE = os.path.join(EXPLORATION_DIR, 'progress.txt')
RESULTS_FILE = os.path.join(EXPLORATION_DIR, 'code', 'results.json')


def log_progress(msg):
    with open(PROGRESS_FILE, 'a') as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    print(msg, flush=True)


# ============================================================
# Initial Conditions (from exploration-002)
# ============================================================

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

    return ux_hat, uy_hat, uz_hat


def taylor_green_ic(solver):
    """Taylor-Green vortex."""
    X, Y, Z = solver.X, solver.Y, solver.Z
    ux = np.sin(X) * np.cos(Y) * np.cos(Z)
    uy = -np.cos(X) * np.sin(Y) * np.cos(Z)
    uz = np.zeros_like(X)
    ux_hat, uy_hat, uz_hat = solver.project(
        solver.to_spectral(ux), solver.to_spectral(uy), solver.to_spectral(uz))
    return solver.dealias(ux_hat), solver.dealias(uy_hat), solver.dealias(uz_hat)


def random_gaussian_ic(solver, seed=42):
    """Random Gaussian with k^{-5/3} spectrum, projected to div-free."""
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

    # Normalize to unit energy
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
    Compute u_below = u_norm * min(1, lambda_k / |u_norm|) at each grid point.

    u_norm = u / norm_factor (so max|u_norm| = 1)
    lambda_k = 1 - 2^{-k}
    u_below_i = u_norm_i * min(1, lambda_k / |u_norm|)

    Returns u_below components in physical space (NOT normalized back).
    """
    ux = solver.to_physical(solver.dealias(ux_hat)) / norm_factor
    uy = solver.to_physical(solver.dealias(uy_hat)) / norm_factor
    uz = solver.to_physical(solver.dealias(uz_hat)) / norm_factor

    threshold_k = 1.0 - 2.0**(-k_level)
    speed = np.sqrt(ux**2 + uy**2 + uz**2)
    speed_safe = np.maximum(speed, 1e-30)

    # Truncation factor: min(1, threshold / |u|)
    factor = np.minimum(1.0, threshold_k / speed_safe)
    factor = np.where(speed < 1e-30, 1.0, factor)

    ub_x = ux * factor
    ub_y = uy * factor
    ub_z = uz * factor

    return ub_x, ub_y, ub_z, ux, uy, uz


def spectral_curl(solver, ux_hat, uy_hat, uz_hat):
    """Compute curl(u) in physical space using spectral differentiation.

    curl(u)_x = du_z/dy - du_y/dz
    curl(u)_y = du_x/dz - du_z/dx
    curl(u)_z = du_y/dx - du_x/dy
    """
    wx = solver.to_physical(1j * solver.KY * uz_hat - 1j * solver.KZ * uy_hat)
    wy = solver.to_physical(1j * solver.KZ * ux_hat - 1j * solver.KX * uz_hat)
    wz = solver.to_physical(1j * solver.KX * uy_hat - 1j * solver.KY * ux_hat)
    return wx, wy, wz


def spectral_curl_from_physical(solver, ux, uy, uz):
    """Compute curl from physical-space fields (project to spectral, curl, back)."""
    ux_hat = solver.dealias(solver.to_spectral(ux))
    uy_hat = solver.dealias(solver.to_spectral(uy))
    uz_hat = solver.dealias(solver.to_spectral(uz))
    return spectral_curl(solver, ux_hat, uy_hat, uz_hat)


def compute_beltrami_deficit(solver, ub_x, ub_y, ub_z):
    """
    Compute Beltrami deficit of a vector field:

    lambda_opt = <curl(u), u> / ||u||^2
    B = ||curl(u) - lambda_opt * u||_L2 / ||u||_L2

    Returns lambda_opt, B_deficit
    """
    vol = (2 * np.pi)**3
    dV = vol / solver.N**3

    # Compute curl(u_below) spectrally
    wx, wy, wz = spectral_curl_from_physical(solver, ub_x, ub_y, ub_z)

    # L2 inner products: <curl(u), u> and ||u||^2
    curl_dot_u = np.sum(wx * ub_x + wy * ub_y + wz * ub_z) * dV
    u_sq = np.sum(ub_x**2 + ub_y**2 + ub_z**2) * dV

    if u_sq < 1e-30:
        return 0.0, 0.0  # trivial: u_below ~ 0

    lambda_opt = curl_dot_u / u_sq

    # ||curl(u) - lambda_opt * u||_L2
    residual_sq = np.sum(
        (wx - lambda_opt * ub_x)**2 +
        (wy - lambda_opt * ub_y)**2 +
        (wz - lambda_opt * ub_z)**2
    ) * dV

    B_deficit = np.sqrt(residual_sq / u_sq)

    return lambda_opt, B_deficit


def compute_hessian_lamb_decomposition(solver, ub_x, ub_y, ub_z):
    """
    Decompose the pressure Poisson source for u_below into Hessian and Lamb pieces.

    Full source: -Delta P = d_i d_j (u_{b,i} u_{b,j})
    Hessian piece: -Delta P_H = Delta(|u_b|^2 / 2)
    Lamb piece: -Delta P_L = div(omega_b x u_b)

    Identity: d_i d_j (u_i u_j) = Delta(|u|^2/2) + div(omega x u)

    Returns P_total, P_hessian, P_lamb in physical space, plus norms and decomposition error.
    """
    N = solver.N
    K = [solver.KX, solver.KY, solver.KZ]

    # --- Full pressure P_total from d_i d_j (u_{b,i} u_{b,j}) ---
    u_b = [ub_x, ub_y, ub_z]

    # RHS in spectral: sum_{i,j} k_i k_j FFT(u_{b,i} u_{b,j})
    rhs_hat = np.zeros((N, N, N), dtype=complex)
    for i in range(3):
        for j in range(3):
            uiuj_hat = fftn(u_b[i] * u_b[j])
            rhs_hat += K[i] * K[j] * uiuj_hat

    # Solve: -Delta P = rhs  =>  K^2 P_hat = rhs_hat  =>  P_hat = rhs_hat / K^2
    P_total_hat = rhs_hat / solver.K2_safe
    P_total_hat[0, 0, 0] = 0
    P_total = ifftn(P_total_hat).real

    # --- Hessian piece: from Delta(|u_b|^2/2) ---
    # -Delta P_H = Delta(|u_b|^2/2)
    # In spectral: K^2 P_H_hat = -K^2 * FFT(|u_b|^2/2)
    # => P_H_hat = -FFT(|u_b|^2/2)  ... wait, let me be more careful.
    #
    # Actually the identity is:
    # d_i d_j (u_i u_j) = Delta(|u|^2/2) + div(L)
    # where L = omega x u is the Lamb vector.
    #
    # The pressure Poisson equation is: -Delta P = d_i d_j (u_i u_j)
    # => -Delta P = Delta(|u|^2/2) + div(L)
    #
    # Define P_H by: -Delta P_H = Delta(|u|^2/2)
    # => P_H_hat = -(-K^2) * FFT(|u|^2/2) / K^2 = FFT(|u|^2/2)
    # Wait no. -Delta P_H = Delta(|u|^2/2)
    # In spectral: K^2 * P_H_hat = -K^2 * FFT(|u|^2/2)
    # => P_H_hat = -FFT(|u|^2/2)
    # => P_H = -|u|^2/2  (up to zero mode)
    #
    # That's Bernoulli: P_Hessian = -|u_b|^2 / 2
    #
    # Let me verify: Delta(|u|^2/2) has spectral form -K^2 * FFT(|u|^2/2)
    # -Delta P_H = -K^2 * FFT(|u|^2/2)
    # => K^2 * P_H_hat = -K^2 * FFT(|u|^2/2)
    # => P_H_hat = -FFT(|u|^2/2)
    # => P_H = -|u|^2/2  (yes)

    half_speed_sq = 0.5 * (ub_x**2 + ub_y**2 + ub_z**2)
    half_speed_sq_hat = fftn(half_speed_sq)

    P_hessian_hat = -half_speed_sq_hat
    P_hessian_hat[0, 0, 0] = 0
    P_hessian = ifftn(P_hessian_hat).real

    # --- Lamb piece: from div(L) where L = omega x u ---
    # -Delta P_L = div(L)
    # In spectral: K^2 P_L_hat = -i (kx Lx_hat + ky Ly_hat + kz Lz_hat)
    # Wait: div(L) in spectral is i*k . L_hat
    # So: -Delta P_L = div(L)  =>  K^2 P_L_hat = i*(kx Lx_hat + ky Ly_hat + kz Lz_hat)

    wx, wy, wz = spectral_curl_from_physical(solver, ub_x, ub_y, ub_z)

    # Lamb vector L = omega x u
    Lx = wy * ub_z - wz * ub_y
    Ly = wz * ub_x - wx * ub_z
    Lz = wx * ub_y - wy * ub_x

    Lx_hat = fftn(Lx)
    Ly_hat = fftn(Ly)
    Lz_hat = fftn(Lz)

    # div(L) in spectral: 1j * (kx * Lx_hat + ky * Ly_hat + kz * Lz_hat)
    divL_hat = 1j * (solver.KX * Lx_hat + solver.KY * Ly_hat + solver.KZ * Lz_hat)

    # -Delta P_L = div(L)  =>  K^2 P_L_hat = divL_hat
    P_lamb_hat = divL_hat / solver.K2_safe
    P_lamb_hat[0, 0, 0] = 0
    P_lamb = ifftn(P_lamb_hat).real

    # --- Verify decomposition: P_total should equal P_hessian + P_lamb ---
    decomp_error = np.max(np.abs(P_total - (P_hessian + P_lamb)))
    P_total_max = np.max(np.abs(P_total))
    decomp_rel = decomp_error / max(P_total_max, 1e-30)

    # Norms
    vol = (2 * np.pi)**3
    dV = vol / solver.N**3

    P_total_L2 = np.sqrt(np.sum(P_total**2) * dV)
    P_hessian_L2 = np.sqrt(np.sum(P_hessian**2) * dV)
    P_lamb_L2 = np.sqrt(np.sum(P_lamb**2) * dV)
    Lamb_L2 = np.sqrt(np.sum(Lx**2 + Ly**2 + Lz**2) * dV)

    return {
        'P_total': P_total,
        'P_hessian': P_hessian,
        'P_lamb': P_lamb,
        'Lx': Lx, 'Ly': Ly, 'Lz': Lz,
        'P_total_L2': P_total_L2,
        'P_hessian_L2': P_hessian_L2,
        'P_lamb_L2': P_lamb_L2,
        'Lamb_L2': Lamb_L2,
        'decomp_error_abs': decomp_error,
        'decomp_error_rel': decomp_rel,
    }


def compute_bottleneck_contributions(solver, ub_x, ub_y, ub_z, ux_norm, uy_norm, uz_norm,
                                     k_level, norm_factor, P_total, P_hessian, P_lamb):
    """
    Compute the bottleneck integral contributions from each pressure piece.

    I_k^{total}   = int |P_total| * |d_k| * 1_{v_k>0} dx
    I_k^{Hessian} = int |P_hessian| * |d_k| * 1_{v_k>0} dx
    I_k^{Lamb}    = int |P_lamb| * |d_k| * 1_{v_k>0} dx

    Note: we compute these from the snapshot (no time integration — single snapshot).
    """
    vol = (2 * np.pi)**3
    N = solver.N
    dV = vol / N**3

    # |u_norm| and threshold
    u_mag_norm = np.sqrt(ux_norm**2 + uy_norm**2 + uz_norm**2)
    threshold_k = 1.0 - 2.0**(-k_level)
    v_k = np.maximum(u_mag_norm - threshold_k, 0.0)
    active = v_k > 0

    if not np.any(active):
        return 0.0, 0.0, 0.0

    # Compute |d_k| — needs grad|u| and grad u
    ux_hat = solver.dealias(solver.to_spectral(ux_norm))
    uy_hat = solver.dealias(solver.to_spectral(uy_norm))
    uz_hat = solver.dealias(solver.to_spectral(uz_norm))

    # All velocity gradients
    dux_dx = solver.to_physical(1j * solver.KX * ux_hat)
    dux_dy = solver.to_physical(1j * solver.KY * ux_hat)
    dux_dz = solver.to_physical(1j * solver.KZ * ux_hat)
    duy_dx = solver.to_physical(1j * solver.KX * uy_hat)
    duy_dy = solver.to_physical(1j * solver.KY * uy_hat)
    duy_dz = solver.to_physical(1j * solver.KZ * uy_hat)
    duz_dx = solver.to_physical(1j * solver.KX * uz_hat)
    duz_dy = solver.to_physical(1j * solver.KY * uz_hat)
    duz_dz = solver.to_physical(1j * solver.KZ * uz_hat)

    # |grad u|^2
    grad_u_sq = (dux_dx**2 + dux_dy**2 + dux_dz**2 +
                 duy_dx**2 + duy_dy**2 + duy_dz**2 +
                 duz_dx**2 + duz_dy**2 + duz_dz**2)

    # grad|u|
    u_mag_safe = np.where(u_mag_norm > 1e-14, u_mag_norm, 1.0)
    grad_umag_x = (ux_norm * dux_dx + uy_norm * duy_dx + uz_norm * duz_dx) / u_mag_safe
    grad_umag_y = (ux_norm * dux_dy + uy_norm * duy_dy + uz_norm * duz_dy) / u_mag_safe
    grad_umag_z = (ux_norm * dux_dz + uy_norm * duy_dz + uz_norm * duz_dz) / u_mag_safe

    mask_zero = u_mag_norm < 1e-14
    grad_umag_x[mask_zero] = 0.0
    grad_umag_y[mask_zero] = 0.0
    grad_umag_z[mask_zero] = 0.0
    grad_umag_sq = grad_umag_x**2 + grad_umag_y**2 + grad_umag_z**2

    # d_k^2
    term1 = np.where(u_mag_norm > 1e-14, (v_k / u_mag_safe) * grad_umag_sq, 0.0)
    term2 = np.zeros_like(v_k)
    term2[active] = (threshold_k / u_mag_safe[active]) * grad_u_sq[active]
    dk_sq = term1 + term2
    dk_abs = np.sqrt(np.maximum(dk_sq, 0.0))

    # Bottleneck integrals
    active_float = active.astype(float)
    I_total = np.sum(np.abs(P_total) * dk_abs * active_float) * dV
    I_hessian = np.sum(np.abs(P_hessian) * dk_abs * active_float) * dV
    I_lamb = np.sum(np.abs(P_lamb) * dk_abs * active_float) * dV

    return I_total, I_hessian, I_lamb


# ============================================================
# Main Runner
# ============================================================

def run_all():
    """Run Task A and Task B for all IC/Re/k combinations."""

    with open(PROGRESS_FILE, 'w') as f:
        f.write(f"Exploration 007 started: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    ic_names = ['ABC', 'TaylorGreen', 'RandomGauss']
    re_values = [100, 500, 1000]
    k_values = list(range(9))  # k = 0, 1, ..., 8
    N_primary = 64

    all_results = {
        'task_a': [],   # Beltrami deficit results
        'task_b': [],   # Hessian/Lamb decomposition results
        'convergence': None,  # N=128 check
    }

    for ic_name in ic_names:
        for Re in re_values:
            log_progress(f"\n{'='*60}")
            log_progress(f"IC={ic_name}, Re={Re}, N={N_primary}")
            log_progress(f"{'='*60}")

            try:
                nu = 1.0 / Re
                solver = NavierStokesSolver(N_primary, nu, cfl=0.4)

                # Initialize
                ic_func = IC_FUNCS[ic_name]
                ux_hat, uy_hat, uz_hat = ic_func(solver)

                # Evolve to develop some dynamics
                T_final = min(2.0 * np.pi / max(Re**0.5 * 0.01, 0.1), 5.0)
                T_final = max(T_final, 0.5)
                snap_interval = T_final / 10

                log_progress(f"  Evolving to T={T_final:.3f}...")
                _, _, _, snapshots = solver.run(ux_hat, uy_hat, uz_hat, T_final,
                                                 snapshot_interval=snap_interval)
                log_progress(f"  Got {len(snapshots)} snapshots")

                # Use the LAST snapshot for analysis
                t_snap, ux_hat_snap, uy_hat_snap, uz_hat_snap = snapshots[-1]

                # L^inf normalization
                ux_phys = solver.to_physical(solver.dealias(ux_hat_snap))
                uy_phys = solver.to_physical(solver.dealias(uy_hat_snap))
                uz_phys = solver.to_physical(solver.dealias(uz_hat_snap))
                speed = np.sqrt(ux_phys**2 + uy_phys**2 + uz_phys**2)
                norm_factor = max(np.max(speed), 1e-30)

                log_progress(f"  norm_factor (Linf) = {norm_factor:.6f}")

                # ---- TASK A: Beltrami deficit ----
                task_a_entry = {
                    'ic': ic_name,
                    'Re': Re,
                    'N': N_primary,
                    'norm_factor': float(norm_factor),
                    'beltrami_deficits': [],
                    'lambda_opts': [],
                }

                for k in k_values:
                    ub_x, ub_y, ub_z, ux_norm, uy_norm, uz_norm = compute_u_below(
                        solver, ux_hat_snap, uy_hat_snap, uz_hat_snap, k, norm_factor)
                    lambda_opt, B_deficit = compute_beltrami_deficit(solver, ub_x, ub_y, ub_z)
                    task_a_entry['beltrami_deficits'].append(float(B_deficit))
                    task_a_entry['lambda_opts'].append(float(lambda_opt))

                    if k in [0, 4, 8]:
                        log_progress(f"  k={k}: B_deficit={B_deficit:.6f}, lambda_opt={lambda_opt:.6f}")

                # Also measure Beltrami deficit of the FULL (un-truncated, normalized) velocity
                lambda_opt_full, B_full = compute_beltrami_deficit(
                    solver,
                    ux_phys / norm_factor,
                    uy_phys / norm_factor,
                    uz_phys / norm_factor
                )
                task_a_entry['B_full'] = float(B_full)
                task_a_entry['lambda_opt_full'] = float(lambda_opt_full)
                log_progress(f"  Full field: B={B_full:.6f}, lambda_opt={lambda_opt_full:.6f}")

                all_results['task_a'].append(task_a_entry)

                # ---- TASK B: Hessian/Lamb decomposition ----
                task_b_entry = {
                    'ic': ic_name,
                    'Re': Re,
                    'N': N_primary,
                    'k_results': [],
                }

                for k in k_values:
                    ub_x, ub_y, ub_z, ux_norm, uy_norm, uz_norm = compute_u_below(
                        solver, ux_hat_snap, uy_hat_snap, uz_hat_snap, k, norm_factor)

                    # Decompose
                    decomp = compute_hessian_lamb_decomposition(solver, ub_x, ub_y, ub_z)

                    # Bottleneck contributions
                    I_total, I_hessian, I_lamb = compute_bottleneck_contributions(
                        solver, ub_x, ub_y, ub_z, ux_norm, uy_norm, uz_norm,
                        k, norm_factor,
                        decomp['P_total'], decomp['P_hessian'], decomp['P_lamb'])

                    lamb_frac = I_lamb / max(I_total, 1e-30) if I_total > 1e-30 else 0.0

                    k_result = {
                        'k': k,
                        'P_total_L2': float(decomp['P_total_L2']),
                        'P_hessian_L2': float(decomp['P_hessian_L2']),
                        'P_lamb_L2': float(decomp['P_lamb_L2']),
                        'Lamb_vector_L2': float(decomp['Lamb_L2']),
                        'decomp_error_abs': float(decomp['decomp_error_abs']),
                        'decomp_error_rel': float(decomp['decomp_error_rel']),
                        'I_total': float(I_total),
                        'I_hessian': float(I_hessian),
                        'I_lamb': float(I_lamb),
                        'lamb_fraction': float(lamb_frac),
                    }
                    task_b_entry['k_results'].append(k_result)

                    if k in [0, 2, 4, 6, 8]:
                        log_progress(f"  k={k}: Lamb/Total={lamb_frac:.4f}, "
                                   f"decomp_err={decomp['decomp_error_rel']:.2e}")

                all_results['task_b'].append(task_b_entry)

                # Save incrementally
                with open(RESULTS_FILE, 'w') as f:
                    json.dump(all_results, f, indent=2)

            except Exception as e:
                log_progress(f"  ERROR: {e}")
                import traceback
                traceback.print_exc()

    # ---- Convergence check: ABC Re=500 at N=128 ----
    log_progress(f"\n{'='*60}")
    log_progress(f"CONVERGENCE CHECK: ABC Re=500, N=128")
    log_progress(f"{'='*60}")

    try:
        Re = 500
        N_conv = 128
        nu = 1.0 / Re
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
            'beltrami_deficits': [],
            'lambda_opts': [],
            'lamb_fractions': [],
        }

        for k in k_values:
            ub_x, ub_y, ub_z, ux_norm, uy_norm, uz_norm = compute_u_below(
                solver, ux_hat_snap, uy_hat_snap, uz_hat_snap, k, norm_factor)
            lambda_opt, B_deficit = compute_beltrami_deficit(solver, ub_x, ub_y, ub_z)
            conv_entry['beltrami_deficits'].append(float(B_deficit))
            conv_entry['lambda_opts'].append(float(lambda_opt))

            decomp = compute_hessian_lamb_decomposition(solver, ub_x, ub_y, ub_z)
            I_total, I_hessian, I_lamb = compute_bottleneck_contributions(
                solver, ub_x, ub_y, ub_z, ux_norm, uy_norm, uz_norm,
                k, norm_factor,
                decomp['P_total'], decomp['P_hessian'], decomp['P_lamb'])
            lamb_frac = I_lamb / max(I_total, 1e-30) if I_total > 1e-30 else 0.0
            conv_entry['lamb_fractions'].append(float(lamb_frac))

            if k in [0, 4, 8]:
                log_progress(f"  N=128 k={k}: B={B_deficit:.6f}, Lamb/Total={lamb_frac:.4f}")

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
