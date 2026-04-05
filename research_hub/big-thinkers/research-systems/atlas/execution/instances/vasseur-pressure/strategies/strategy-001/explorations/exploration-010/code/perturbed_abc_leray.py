"""
Exploration 010: Perturbed-ABC Near-Beltrami Test + Leray Projection.

Task A: Generate perturbed ABC flows u = (1-eps)*u_ABC + eps*u_random (div-free),
        run DNS at Re=500, N=64, measure B_k, R_frac, beta_eff for eps in [0.01, 0.05, 0.1, 0.2, 0.5].
        Also measure at t=0 for comparison.

Task B: Leray-project u_below for exact ABC, compare with unprojected.

Uses CORRECTED sign convention from E007v3: p_hat = -k_ik_j FFT(u_iu_j) / K^2.
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
from degiorgi_measure import measure_degiorgi_sequence

EXPLORATION_DIR = '/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/vasseur-pressure/strategies/strategy-001/explorations/exploration-010'
PROGRESS_FILE = os.path.join(EXPLORATION_DIR, 'progress.txt')
RESULTS_FILE = os.path.join(EXPLORATION_DIR, 'code', 'results.json')


def log_progress(msg):
    with open(PROGRESS_FILE, 'a') as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    print(msg, flush=True)


# ============================================================
# Initial Conditions
# ============================================================

def abc_flow_ic(solver, A=1.0, B=1.0, C=1.0):
    """Standard ABC flow (Beltrami: curl u = u for A=B=C=1)."""
    X, Y, Z = solver.X, solver.Y, solver.Z
    ux = B * np.sin(Y) + C * np.cos(Z)
    uy = C * np.sin(Z) + A * np.cos(X)
    uz = A * np.sin(X) + B * np.cos(Y)
    ux_hat = solver.to_spectral(ux)
    uy_hat = solver.to_spectral(uy)
    uz_hat = solver.to_spectral(uz)
    ux_hat, uy_hat, uz_hat = solver.project(ux_hat, uy_hat, uz_hat)
    return solver.dealias(ux_hat), solver.dealias(uy_hat), solver.dealias(uz_hat)


def random_divfree_ic(solver, seed=137, spectrum='kolmogorov'):
    """Generate random divergence-free field with k^{-5/3} spectrum."""
    rng = np.random.RandomState(seed)
    N = solver.N
    ux_hat = rng.randn(N, N, N) + 1j * rng.randn(N, N, N)
    uy_hat = rng.randn(N, N, N) + 1j * rng.randn(N, N, N)
    uz_hat = rng.randn(N, N, N) + 1j * rng.randn(N, N, N)

    K_mag = solver.K_mag
    K_mag_safe = np.where(K_mag == 0, 1, K_mag)

    if spectrum == 'kolmogorov':
        # E(k) ~ k^{-5/3} => amplitude ~ k^{-5/6} (since E ~ |u_hat|^2 * k^2)
        envelope = K_mag_safe**(-5.0/6.0) * np.exp(-K_mag_safe**2 / (2 * (N/4)**2))
    else:
        envelope = np.exp(-K_mag_safe**2 / (2 * (N/4)**2))
    envelope[0, 0, 0] = 0

    ux_hat *= envelope
    uy_hat *= envelope
    uz_hat *= envelope

    # Project div-free
    ux_hat, uy_hat, uz_hat = solver.project(ux_hat, uy_hat, uz_hat)
    ux_hat = solver.dealias(ux_hat)
    uy_hat = solver.dealias(uy_hat)
    uz_hat = solver.dealias(uz_hat)

    return ux_hat, uy_hat, uz_hat


def perturbed_abc_ic(solver, eps, seed=137):
    """
    Generate perturbed ABC: u = (1-eps)*u_ABC + eps*u_random.
    Both components are div-free. Sum is div-free.
    Normalize so max|u| = 1 (L^inf normalization).
    """
    ux_abc, uy_abc, uz_abc = abc_flow_ic(solver)
    ux_rnd, uy_rnd, uz_rnd = random_divfree_ic(solver, seed=seed)

    # Match energy of random to ABC
    ux_a = solver.to_physical(ux_abc)
    uy_a = solver.to_physical(uy_abc)
    uz_a = solver.to_physical(uz_abc)
    E_abc = 0.5 * np.mean(ux_a**2 + uy_a**2 + uz_a**2)

    ux_r = solver.to_physical(ux_rnd)
    uy_r = solver.to_physical(uy_rnd)
    uz_r = solver.to_physical(uz_rnd)
    E_rnd = 0.5 * np.mean(ux_r**2 + uy_r**2 + uz_r**2)

    if E_rnd > 0:
        scale = np.sqrt(E_abc / E_rnd)
        ux_rnd *= scale
        uy_rnd *= scale
        uz_rnd *= scale

    # Combine
    ux_hat = (1 - eps) * ux_abc + eps * ux_rnd
    uy_hat = (1 - eps) * uy_abc + eps * uy_rnd
    uz_hat = (1 - eps) * uz_abc + eps * uz_rnd

    # Project (should already be div-free, but ensure)
    ux_hat, uy_hat, uz_hat = solver.project(ux_hat, uy_hat, uz_hat)

    # L^inf normalize
    ux_p = solver.to_physical(ux_hat)
    uy_p = solver.to_physical(uy_hat)
    uz_p = solver.to_physical(uz_hat)
    Linf = np.max(np.sqrt(ux_p**2 + uy_p**2 + uz_p**2))
    if Linf > 0:
        ux_hat /= Linf
        uy_hat /= Linf
        uz_hat /= Linf

    return solver.dealias(ux_hat), solver.dealias(uy_hat), solver.dealias(uz_hat)


# ============================================================
# Core Computations (from E007v3, adapted)
# ============================================================

def spectral_curl_phys(solver, ux, uy, uz):
    """Curl from physical fields."""
    ux_h = solver.dealias(solver.to_spectral(ux))
    uy_h = solver.dealias(solver.to_spectral(uy))
    uz_h = solver.dealias(solver.to_spectral(uz))
    wx = solver.to_physical(1j * solver.KY * uz_h - 1j * solver.KZ * uy_h)
    wy = solver.to_physical(1j * solver.KZ * ux_h - 1j * solver.KX * uz_h)
    wz = solver.to_physical(1j * solver.KX * uy_h - 1j * solver.KY * ux_h)
    return wx, wy, wz


def spectral_div_phys(solver, fx, fy, fz):
    """Divergence from physical fields."""
    fx_h = solver.dealias(solver.to_spectral(fx))
    fy_h = solver.dealias(solver.to_spectral(fy))
    fz_h = solver.dealias(solver.to_spectral(fz))
    return solver.to_physical(1j * (solver.KX * fx_h + solver.KY * fy_h + solver.KZ * fz_h))


def compute_u_below(solver, ux_hat, uy_hat, uz_hat, k_level, norm_factor):
    """Compute u_below = u_norm * min(1, lambda_k / |u_norm|)."""
    ux = solver.to_physical(solver.dealias(ux_hat)) / norm_factor
    uy = solver.to_physical(solver.dealias(uy_hat)) / norm_factor
    uz = solver.to_physical(solver.dealias(uz_hat)) / norm_factor
    threshold_k = 1.0 - 2.0**(-k_level)
    speed = np.sqrt(ux**2 + uy**2 + uz**2)
    speed_safe = np.maximum(speed, 1e-30)
    factor = np.minimum(1.0, threshold_k / speed_safe)
    factor = np.where(speed < 1e-30, 1.0, factor)
    return ux * factor, uy * factor, uz * factor, ux, uy, uz, speed


def compute_beltrami_deficit(solver, ub_x, ub_y, ub_z):
    """B = ||curl(u) - lambda_opt * u||_L2 / ||u||_L2"""
    vol = (2 * np.pi)**3
    dV = vol / solver.N**3
    wx, wy, wz = spectral_curl_phys(solver, ub_x, ub_y, ub_z)
    curl_dot_u = np.sum(wx * ub_x + wy * ub_y + wz * ub_z) * dV
    u_sq = np.sum(ub_x**2 + ub_y**2 + ub_z**2) * dV
    if u_sq < 1e-30:
        return 0.0, 0.0
    lambda_opt = curl_dot_u / u_sq
    residual_sq = np.sum((wx - lambda_opt*ub_x)**2 + (wy - lambda_opt*ub_y)**2 + (wz - lambda_opt*ub_z)**2) * dV
    return lambda_opt, np.sqrt(residual_sq / u_sq)


def solve_pressure_poisson(solver, u_x, u_y, u_z):
    """
    Solve -Delta p = d_id_j(u_iu_j).
    p_hat = -k_ik_j FFT(u_iu_j) / K^2 (CORRECT sign from E007v3).
    """
    N = solver.N
    K = [solver.KX, solver.KY, solver.KZ]
    u = [u_x, u_y, u_z]

    p_hat = np.zeros((N, N, N), dtype=complex)
    for i in range(3):
        for j in range(3):
            uiuj_hat = fftn(u[i] * u[j])
            p_hat -= K[i] * K[j] * uiuj_hat

    p_hat = p_hat / solver.K2_safe
    p_hat[0, 0, 0] = 0
    return ifftn(p_hat).real


def compute_pressure_decomposition(solver, ub_x, ub_y, ub_z):
    """Pressure decomposition: P_total, P_hessian (Bernoulli), P_remainder."""
    N = solver.N
    vol = (2 * np.pi)**3
    dV = vol / N**3

    P_total = solve_pressure_poisson(solver, ub_x, ub_y, ub_z)
    P_hessian = -0.5 * (ub_x**2 + ub_y**2 + ub_z**2)
    P_hessian -= np.mean(P_hessian)
    P_remainder = P_total - P_hessian

    div_ub = spectral_div_phys(solver, ub_x, ub_y, ub_z)
    div_ub_L2 = float(np.sqrt(np.sum(div_ub**2) * dV))

    wx, wy, wz = spectral_curl_phys(solver, ub_x, ub_y, ub_z)
    Lx = wy * ub_z - wz * ub_y
    Ly = wz * ub_x - wx * ub_z
    Lz = wx * ub_y - wy * ub_x
    Lamb_L2 = float(np.sqrt(np.sum(Lx**2 + Ly**2 + Lz**2) * dV))

    P_total_L2 = float(np.sqrt(np.sum(P_total**2) * dV))
    P_hessian_L2 = float(np.sqrt(np.sum(P_hessian**2) * dV))
    P_remainder_L2 = float(np.sqrt(np.sum(P_remainder**2) * dV))

    hessian_frac = P_hessian_L2 / max(P_total_L2, 1e-30)
    remainder_frac = P_remainder_L2 / max(P_total_L2, 1e-30)

    return {
        'P_total_L2': P_total_L2, 'P_hessian_L2': P_hessian_L2, 'P_remainder_L2': P_remainder_L2,
        'hessian_frac_L2': hessian_frac, 'remainder_frac_L2': remainder_frac,
        'Lamb_L2': Lamb_L2, 'div_ub_L2': div_ub_L2,
    }


def leray_project_physical(solver, fx, fy, fz):
    """
    Leray projection: P_L(f) = f - grad(Delta^{-1}(div f)).
    In Fourier: zero out the irrotational component.
    """
    fx_h = solver.to_spectral(fx)
    fy_h = solver.to_spectral(fy)
    fz_h = solver.to_spectral(fz)
    fx_h, fy_h, fz_h = solver.project(fx_h, fy_h, fz_h)
    return solver.to_physical(fx_h), solver.to_physical(fy_h), solver.to_physical(fz_h)


# ============================================================
# Task A: Perturbed ABC
# ============================================================

def run_task_a(N=64, Re=500, T_final=2.0, eps_values=None):
    """Run perturbed ABC at multiple eps values."""
    if eps_values is None:
        eps_values = [0.0, 0.01, 0.05, 0.1, 0.2, 0.5]

    nu = 1.0 / Re
    k_values = list(range(9))
    results = {}

    for eps in eps_values:
        log_progress(f"\n{'='*60}")
        log_progress(f"Task A: eps={eps}, Re={Re}, N={N}")
        log_progress(f"{'='*60}")

        solver = NavierStokesSolver(N, nu, cfl=0.4)

        if eps == 0.0:
            ux_hat, uy_hat, uz_hat = abc_flow_ic(solver)
            # L^inf normalize to match perturbed cases
            ux_p = solver.to_physical(ux_hat)
            uy_p = solver.to_physical(uy_hat)
            uz_p = solver.to_physical(uz_hat)
            Linf = np.max(np.sqrt(ux_p**2 + uy_p**2 + uz_p**2))
            ux_hat /= Linf
            uy_hat /= Linf
            uz_hat /= Linf
        else:
            ux_hat, uy_hat, uz_hat = perturbed_abc_ic(solver, eps)

        # --- Measure at t=0 ---
        ux_p = solver.to_physical(solver.dealias(ux_hat))
        uy_p = solver.to_physical(solver.dealias(uy_hat))
        uz_p = solver.to_physical(solver.dealias(uz_hat))
        speed_0 = np.sqrt(ux_p**2 + uy_p**2 + uz_p**2)
        nf_0 = max(np.max(speed_0), 1e-30)
        log_progress(f"  t=0: max|u| = {nf_0:.6f}")

        # B_k at t=0 for each k
        Bk_t0 = []
        Rfrac_t0 = []
        for k in k_values:
            ub_x, ub_y, ub_z, ux_n, uy_n, uz_n, spd = compute_u_below(
                solver, ux_hat, uy_hat, uz_hat, k, nf_0)
            _, B_k = compute_beltrami_deficit(solver, ub_x, ub_y, ub_z)
            decomp = compute_pressure_decomposition(solver, ub_x, ub_y, ub_z)
            Bk_t0.append(float(B_k))
            Rfrac_t0.append(decomp['remainder_frac_L2'])

        # Full-field B at t=0
        _, B_full_t0 = compute_beltrami_deficit(solver, ux_p/nf_0, uy_p/nf_0, uz_p/nf_0)

        log_progress(f"  t=0: B_full={B_full_t0:.6f}")
        for k in [0, 2, 4, 6, 8]:
            log_progress(f"    k={k}: B={Bk_t0[k]:.6f}, R_frac={Rfrac_t0[k]:.6f}")

        # --- DNS evolution ---
        snap_interval = T_final / 10
        log_progress(f"  Evolving to T={T_final}...")
        ux_hat_f, uy_hat_f, uz_hat_f, snapshots = solver.run(
            ux_hat, uy_hat, uz_hat, T_final, snapshot_interval=snap_interval)
        log_progress(f"  Got {len(snapshots)} snapshots")

        # Final snapshot
        _, ux_hat_s, uy_hat_s, uz_hat_s = snapshots[-1]
        ux_p = solver.to_physical(solver.dealias(ux_hat_s))
        uy_p = solver.to_physical(solver.dealias(uy_hat_s))
        uz_p = solver.to_physical(solver.dealias(uz_hat_s))
        speed_f = np.sqrt(ux_p**2 + uy_p**2 + uz_p**2)
        nf_f = max(np.max(speed_f), 1e-30)
        E_final = 0.5 * np.mean(ux_p**2 + uy_p**2 + uz_p**2)
        log_progress(f"  t=T: max|u| = {nf_f:.6f}, E = {E_final:.6f}")

        # B_k at t=T_final
        Bk_tf = []
        Rfrac_tf = []
        divub_tf = []
        lambda_opts_tf = []
        for k in k_values:
            ub_x, ub_y, ub_z, ux_n, uy_n, uz_n, spd = compute_u_below(
                solver, ux_hat_s, uy_hat_s, uz_hat_s, k, nf_f)
            lam_k, B_k = compute_beltrami_deficit(solver, ub_x, ub_y, ub_z)
            decomp = compute_pressure_decomposition(solver, ub_x, ub_y, ub_z)
            Bk_tf.append(float(B_k))
            Rfrac_tf.append(decomp['remainder_frac_L2'])
            divub_tf.append(decomp['div_ub_L2'])
            lambda_opts_tf.append(float(lam_k))

        _, B_full_tf = compute_beltrami_deficit(solver, ux_p/nf_f, uy_p/nf_f, uz_p/nf_f)

        log_progress(f"  t=T: B_full={B_full_tf:.6f}")
        for k in [0, 2, 4, 6, 8]:
            log_progress(f"    k={k}: B={Bk_tf[k]:.6f}, R_frac={Rfrac_tf[k]:.6f}")

        # --- De Giorgi beta_eff ---
        log_progress(f"  Computing beta_eff...")
        dg_result = measure_degiorgi_sequence(solver, snapshots, K_max=8)
        beta_eff = dg_result['beta_eff']
        beta_stderr = dg_result['beta_stderr']
        fit_r2 = dg_result['fit_r2']
        U_k_values = dg_result['U_k_values'].tolist()
        log_progress(f"  beta_eff = {beta_eff:.4f} +/- {beta_stderr:.4f}, R^2 = {fit_r2:.4f}")

        # Compute BN exponent (gamma) from U_k
        # gamma = log(U_k / U_{k-1}) / log(2)  averaged
        gammas = []
        for k in range(1, len(U_k_values)):
            if U_k_values[k] > 1e-30 and U_k_values[k-1] > 1e-30:
                gammas.append(np.log2(U_k_values[k] / U_k_values[k-1]))
        gamma_avg = float(np.mean(gammas)) if gammas else float('nan')

        results[str(eps)] = {
            'eps': eps,
            'N': N, 'Re': Re, 'T_final': T_final,
            'nf_t0': float(nf_0), 'nf_tf': float(nf_f),
            'E_final': float(E_final),
            'B_full_t0': float(B_full_t0), 'B_full_tf': float(B_full_tf),
            'Bk_t0': Bk_t0, 'Bk_tf': Bk_tf,
            'Rfrac_t0': Rfrac_t0, 'Rfrac_tf': Rfrac_tf,
            'divub_tf': divub_tf, 'lambda_opts_tf': lambda_opts_tf,
            'beta_eff': float(beta_eff), 'beta_stderr': float(beta_stderr),
            'fit_r2': float(fit_r2), 'gamma_avg': gamma_avg,
            'U_k_values': U_k_values,
        }

        # Save intermediate
        with open(RESULTS_FILE, 'w') as f:
            json.dump({'task_a': results}, f, indent=2)

    return results


# ============================================================
# Task B: Leray Projection
# ============================================================

def run_task_b(N=64, Re=500, T_final=2.0):
    """Leray projection of u_below for exact ABC."""
    log_progress(f"\n{'='*60}")
    log_progress(f"Task B: Leray Projection, Re={Re}, N={N}")
    log_progress(f"{'='*60}")

    nu = 1.0 / Re
    solver = NavierStokesSolver(N, nu, cfl=0.4)
    ux_hat, uy_hat, uz_hat = abc_flow_ic(solver)

    # L^inf normalize
    ux_p = solver.to_physical(ux_hat)
    uy_p = solver.to_physical(uy_hat)
    uz_p = solver.to_physical(uz_hat)
    Linf = np.max(np.sqrt(ux_p**2 + uy_p**2 + uz_p**2))
    ux_hat /= Linf
    uy_hat /= Linf
    uz_hat /= Linf

    # Evolve
    snap_interval = T_final / 10
    _, _, _, snapshots = solver.run(ux_hat, uy_hat, uz_hat, T_final, snapshot_interval=snap_interval)

    # Use final snapshot
    _, ux_hat_s, uy_hat_s, uz_hat_s = snapshots[-1]
    ux_p = solver.to_physical(solver.dealias(ux_hat_s))
    uy_p = solver.to_physical(solver.dealias(uy_hat_s))
    uz_p = solver.to_physical(solver.dealias(uz_hat_s))
    speed = np.sqrt(ux_p**2 + uy_p**2 + uz_p**2)
    nf = max(np.max(speed), 1e-30)

    k_values = list(range(9))
    results_unprojected = []
    results_projected = []

    for k in k_values:
        # Unprojected u_below
        ub_x, ub_y, ub_z, ux_n, uy_n, uz_n, spd = compute_u_below(
            solver, ux_hat_s, uy_hat_s, uz_hat_s, k, nf)

        lam_u, B_u = compute_beltrami_deficit(solver, ub_x, ub_y, ub_z)
        decomp_u = compute_pressure_decomposition(solver, ub_x, ub_y, ub_z)

        # Leray-projected u_below
        ub_lx, ub_ly, ub_lz = leray_project_physical(solver, ub_x, ub_y, ub_z)

        lam_l, B_l = compute_beltrami_deficit(solver, ub_lx, ub_ly, ub_lz)
        decomp_l = compute_pressure_decomposition(solver, ub_lx, ub_ly, ub_lz)

        # Difference between projected and unprojected
        diff_L2 = float(np.sqrt(np.mean((ub_x - ub_lx)**2 + (ub_y - ub_ly)**2 + (ub_z - ub_lz)**2)))
        ub_L2 = float(np.sqrt(np.mean(ub_x**2 + ub_y**2 + ub_z**2)))
        rel_diff = diff_L2 / max(ub_L2, 1e-30)

        results_unprojected.append({
            'k': k, 'B_deficit': float(B_u), 'lambda_opt': float(lam_u),
            'remainder_frac': decomp_u['remainder_frac_L2'],
            'div_ub_L2': decomp_u['div_ub_L2'],
            'Lamb_L2': decomp_u['Lamb_L2'],
        })
        results_projected.append({
            'k': k, 'B_deficit': float(B_l), 'lambda_opt': float(lam_l),
            'remainder_frac': decomp_l['remainder_frac_L2'],
            'div_ub_L2': decomp_l['div_ub_L2'],
            'Lamb_L2': decomp_l['Lamb_L2'],
            'leray_rel_diff': float(rel_diff),
        })

        log_progress(f"  k={k}: B_unproj={B_u:.6f}, B_proj={B_l:.6f}, "
                   f"R_unproj={decomp_u['remainder_frac_L2']:.6f}, R_proj={decomp_l['remainder_frac_L2']:.6f}, "
                   f"div_unproj={decomp_u['div_ub_L2']:.4e}, div_proj={decomp_l['div_ub_L2']:.4e}, "
                   f"rel_diff={rel_diff:.4e}")

    # Also test at t=0 as known-answer check
    log_progress(f"\n  Leray at t=0 (exact ABC, should be trivial):")
    solver2 = NavierStokesSolver(N, nu, cfl=0.4)
    ux_hat0, uy_hat0, uz_hat0 = abc_flow_ic(solver2)
    ux_p0 = solver2.to_physical(ux_hat0)
    uy_p0 = solver2.to_physical(uy_hat0)
    uz_p0 = solver2.to_physical(uz_hat0)
    Linf0 = np.max(np.sqrt(ux_p0**2 + uy_p0**2 + uz_p0**2))
    ux_hat0 /= Linf0; uy_hat0 /= Linf0; uz_hat0 /= Linf0
    nf0 = 1.0  # normalized

    t0_check = []
    for k in [0, 4, 8]:
        ub_x, ub_y, ub_z, _, _, _, _ = compute_u_below(solver2, ux_hat0, uy_hat0, uz_hat0, k, nf0)
        div_ub = spectral_div_phys(solver2, ub_x, ub_y, ub_z)
        div_L2 = float(np.sqrt(np.mean(div_ub**2)))

        ub_lx, ub_ly, ub_lz = leray_project_physical(solver2, ub_x, ub_y, ub_z)
        _, B_u = compute_beltrami_deficit(solver2, ub_x, ub_y, ub_z)
        _, B_l = compute_beltrami_deficit(solver2, ub_lx, ub_ly, ub_lz)

        diff_L2 = float(np.sqrt(np.mean((ub_x - ub_lx)**2 + (ub_y - ub_ly)**2 + (ub_z - ub_lz)**2)))
        t0_check.append({'k': k, 'div_L2': div_L2, 'B_unproj': float(B_u), 'B_proj': float(B_l),
                         'leray_diff_L2': diff_L2})
        log_progress(f"    k={k}: div_L2={div_L2:.4e}, B_unproj={B_u:.6f}, B_proj={B_l:.6f}, diff={diff_L2:.4e}")

    return {
        'unprojected': results_unprojected,
        'projected': results_projected,
        't0_check': t0_check,
        'norm_factor': float(nf),
    }


# ============================================================
# Main
# ============================================================

def main():
    with open(PROGRESS_FILE, 'w') as f:
        f.write(f"Exploration 010 started: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    all_results = {}

    # Task A
    log_progress("="*60)
    log_progress("TASK A: Perturbed ABC")
    log_progress("="*60)
    task_a = run_task_a(N=64, Re=500, T_final=2.0,
                        eps_values=[0.0, 0.01, 0.05, 0.1, 0.2, 0.5])
    all_results['task_a'] = task_a

    # Task B
    log_progress("\n" + "="*60)
    log_progress("TASK B: Leray Projection")
    log_progress("="*60)
    task_b = run_task_b(N=64, Re=500, T_final=2.0)
    all_results['task_b'] = task_b

    # Save final results
    with open(RESULTS_FILE, 'w') as f:
        json.dump(all_results, f, indent=2)

    log_progress(f"\nAll done: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_progress("DONE")

    return all_results


if __name__ == '__main__':
    main()
