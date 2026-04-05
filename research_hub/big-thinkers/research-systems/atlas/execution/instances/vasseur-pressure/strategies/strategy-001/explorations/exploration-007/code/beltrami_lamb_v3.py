"""
Exploration 007 v3: Beltrami deficit + Hessian/Remainder decomposition.

KEY FIX: Sign convention in pressure Poisson solve.
  -Delta p = d_id_j(u_iu_j)
  In Fourier: K^2 p_hat = -k_ik_j FFT(u_iu_j)
  => p_hat = -k_ik_j FFT(u_iu_j) / K^2

Previous versions were MISSING the minus sign, giving P = -p.
This caused P_hessian = -|u|^2/2 and P_total = +|u|^2/2 to differ by 2x.

Now: P_total = p (actual pressure), P_hessian = -|u_b|^2/2 (Bernoulli).
For exact Beltrami: P_remainder = P_total - P_hessian = 0.
"""

import sys
import os
import json
import time
import numpy as np
from numpy.fft import fftn, ifftn

SOLVER_PATH = '/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/vasseur-pressure/strategies/strategy-001/explorations/exploration-002/code'
sys.path.insert(0, SOLVER_PATH)
from ns_solver import NavierStokesSolver

EXPLORATION_DIR = '/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/vasseur-pressure/strategies/strategy-001/explorations/exploration-007'
PROGRESS_FILE = os.path.join(EXPLORATION_DIR, 'progress_v3.txt')
RESULTS_FILE = os.path.join(EXPLORATION_DIR, 'code', 'results_v3.json')


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
    ux_hat *= envelope; uy_hat *= envelope; uz_hat *= envelope
    ux_hat, uy_hat, uz_hat = solver.project(ux_hat, uy_hat, uz_hat)
    ux_hat = solver.dealias(ux_hat); uy_hat = solver.dealias(uy_hat); uz_hat = solver.dealias(uz_hat)
    ux = solver.to_physical(ux_hat); uy = solver.to_physical(uy_hat); uz = solver.to_physical(uz_hat)
    E = 0.5 * np.mean(ux**2 + uy**2 + uz**2)
    if E > 0:
        scale = 1.0 / np.sqrt(2 * E)
        ux_hat *= scale; uy_hat *= scale; uz_hat *= scale
    return ux_hat, uy_hat, uz_hat


IC_FUNCS = {'ABC': abc_flow_ic, 'TaylorGreen': taylor_green_ic, 'RandomGauss': random_gaussian_ic}


# ============================================================
# Core Computations
# ============================================================

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

    In Fourier: K^2 p_hat = -k_ik_j FFT(u_iu_j)
    => p_hat = -k_ik_j FFT(u_iu_j) / K^2

    Returns p in physical space (correct sign!).
    """
    N = solver.N
    K = [solver.KX, solver.KY, solver.KZ]
    u = [u_x, u_y, u_z]

    p_hat = np.zeros((N, N, N), dtype=complex)
    for i in range(3):
        for j in range(3):
            uiuj_hat = fftn(u[i] * u[j])
            p_hat -= K[i] * K[j] * uiuj_hat  # NOTE: minus sign!

    p_hat = p_hat / solver.K2_safe
    p_hat[0, 0, 0] = 0  # zero mean
    return ifftn(p_hat).real


def compute_pressure_decomposition(solver, ub_x, ub_y, ub_z):
    """
    P_total: from Poisson solve (correct sign: -Delta p = d_id_j(u_{b,i}u_{b,j}))
    P_hessian = -|u_b|^2/2 (Bernoulli piece, zero mean)
    P_remainder = P_total - P_hessian (everything non-Bernoulli)

    For exact Beltrami + div-free: P_remainder = 0.
    """
    N = solver.N
    vol = (2 * np.pi)**3
    dV = vol / N**3

    # Full pressure (correct sign)
    P_total = solve_pressure_poisson(solver, ub_x, ub_y, ub_z)

    # Bernoulli piece
    P_hessian = -0.5 * (ub_x**2 + ub_y**2 + ub_z**2)
    P_hessian -= np.mean(P_hessian)  # zero mean

    # Remainder
    P_remainder = P_total - P_hessian

    # Divergence of u_below
    div_ub = spectral_div_phys(solver, ub_x, ub_y, ub_z)
    div_ub_L2 = float(np.sqrt(np.sum(div_ub**2) * dV))
    div_ub_Linf = float(np.max(np.abs(div_ub)))

    # Lamb vector norm
    wx, wy, wz = spectral_curl_phys(solver, ub_x, ub_y, ub_z)
    Lx = wy * ub_z - wz * ub_y
    Ly = wz * ub_x - wx * ub_z
    Lz = wx * ub_y - wy * ub_x
    Lamb_L2 = float(np.sqrt(np.sum(Lx**2 + Ly**2 + Lz**2) * dV))

    # Norms
    P_total_L2 = float(np.sqrt(np.sum(P_total**2) * dV))
    P_hessian_L2 = float(np.sqrt(np.sum(P_hessian**2) * dV))
    P_remainder_L2 = float(np.sqrt(np.sum(P_remainder**2) * dV))

    hessian_frac = P_hessian_L2 / max(P_total_L2, 1e-30)
    remainder_frac = P_remainder_L2 / max(P_total_L2, 1e-30)

    return {
        'P_total': P_total, 'P_hessian': P_hessian, 'P_remainder': P_remainder,
        'P_total_L2': P_total_L2, 'P_hessian_L2': P_hessian_L2, 'P_remainder_L2': P_remainder_L2,
        'hessian_frac_L2': hessian_frac, 'remainder_frac_L2': remainder_frac,
        'Lamb_L2': Lamb_L2, 'div_ub_L2': div_ub_L2, 'div_ub_Linf': div_ub_Linf,
    }


def compute_bottleneck_contributions(solver, ux_norm, uy_norm, uz_norm, k_level,
                                     P_total, P_hessian, P_remainder):
    """Bottleneck integrals: I = int |P| * |d_k| * 1_{v_k>0} dx"""
    vol = (2 * np.pi)**3
    N = solver.N
    dV = vol / N**3

    u_mag = np.sqrt(ux_norm**2 + uy_norm**2 + uz_norm**2)
    threshold_k = 1.0 - 2.0**(-k_level)
    v_k = np.maximum(u_mag - threshold_k, 0.0)
    active = v_k > 0
    if not np.any(active):
        return 0.0, 0.0, 0.0

    # Velocity gradients for d_k
    ux_h = solver.dealias(solver.to_spectral(ux_norm))
    uy_h = solver.dealias(solver.to_spectral(uy_norm))
    uz_h = solver.dealias(solver.to_spectral(uz_norm))

    grads = []
    for comp_h in [ux_h, uy_h, uz_h]:
        for Ki in [solver.KX, solver.KY, solver.KZ]:
            grads.append(solver.to_physical(1j * Ki * comp_h))

    # |grad u|^2
    grad_u_sq = sum(g**2 for g in grads)

    # grad|u|
    u_safe = np.where(u_mag > 1e-14, u_mag, 1.0)
    u_vec = [ux_norm, uy_norm, uz_norm]
    grad_umag_sq = 0.0
    for j in range(3):
        comp = sum(u_vec[i] * grads[i*3+j] for i in range(3)) / u_safe
        comp = np.where(u_mag > 1e-14, comp, 0.0)
        grad_umag_sq = grad_umag_sq + comp**2

    # d_k^2
    term1 = np.where(u_mag > 1e-14, (v_k / u_safe) * grad_umag_sq, 0.0)
    term2 = np.zeros_like(v_k)
    term2[active] = (threshold_k / u_safe[active]) * grad_u_sq[active]
    dk_abs = np.sqrt(np.maximum(term1 + term2, 0.0))

    af = active.astype(float)
    I_total = float(np.sum(np.abs(P_total) * dk_abs * af) * dV)
    I_hessian = float(np.sum(np.abs(P_hessian) * dk_abs * af) * dV)
    I_remainder = float(np.sum(np.abs(P_remainder) * dk_abs * af) * dV)
    return I_total, I_hessian, I_remainder


def verify_abc_t0(N=64):
    """Sanity check: exact ABC at t=0."""
    log_progress("\n" + "="*60)
    log_progress("SANITY CHECK: ABC t=0 (exact Beltrami, div-free)")
    log_progress("="*60)

    solver = NavierStokesSolver(N, 1.0, cfl=0.4)
    ux_hat, uy_hat, uz_hat = abc_flow_ic(solver)
    ux = solver.to_physical(solver.dealias(ux_hat))
    uy = solver.to_physical(solver.dealias(uy_hat))
    uz = solver.to_physical(solver.dealias(uz_hat))
    speed = np.sqrt(ux**2 + uy**2 + uz**2)
    nf = np.max(speed)
    log_progress(f"  norm_factor = {nf:.6f}")

    # Verify full field
    lam, B = compute_beltrami_deficit(solver, ux/nf, uy/nf, uz/nf)
    div_u = spectral_div_phys(solver, ux/nf, uy/nf, uz/nf)
    log_progress(f"  Full: B_deficit={B:.2e}, lambda_opt={lam:.6f}, div_L2={np.sqrt(np.mean(div_u**2)):.2e}")

    results = []
    for k in range(9):
        ub_x, ub_y, ub_z, ux_n, uy_n, uz_n, spd = compute_u_below(
            solver, ux_hat, uy_hat, uz_hat, k, nf)
        lam_k, B_k = compute_beltrami_deficit(solver, ub_x, ub_y, ub_z)
        decomp = compute_pressure_decomposition(solver, ub_x, ub_y, ub_z)

        # fraction of domain where |u_norm| > threshold
        threshold = 1.0 - 2.0**(-k)
        frac_above = float(np.mean(spd > threshold))

        results.append({
            'k': k, 'B_deficit': float(B_k), 'lambda_opt': float(lam_k),
            'hessian_frac': decomp['hessian_frac_L2'],
            'remainder_frac': decomp['remainder_frac_L2'],
            'div_ub_L2': decomp['div_ub_L2'],
            'Lamb_L2': decomp['Lamb_L2'],
            'frac_above': frac_above,
        })

        log_progress(f"  k={k}: B={B_k:.6f}, H_frac={decomp['hessian_frac_L2']:.4f}, "
                   f"R_frac={decomp['remainder_frac_L2']:.6f}, div={decomp['div_ub_L2']:.4e}, "
                   f"Lamb={decomp['Lamb_L2']:.4e}, frac_above={frac_above:.4f}")

    return results


def run_all():
    with open(PROGRESS_FILE, 'w') as f:
        f.write(f"Exploration 007 v3 started: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Sanity check
    sanity = verify_abc_t0(N=64)

    ic_names = ['ABC', 'TaylorGreen', 'RandomGauss']
    re_values = [100, 500, 1000]
    k_values = list(range(9))
    N = 64

    all_results = {'sanity_check': sanity, 'task_a': [], 'task_b': [], 'convergence': None}

    for ic_name in ic_names:
        for Re in re_values:
            log_progress(f"\n{'='*60}")
            log_progress(f"IC={ic_name}, Re={Re}, N={N}")
            log_progress(f"{'='*60}")

            try:
                nu = 1.0 / Re
                solver = NavierStokesSolver(N, nu, cfl=0.4)
                ux_hat, uy_hat, uz_hat = IC_FUNCS[ic_name](solver)

                T_final = min(2.0 * np.pi / max(Re**0.5 * 0.01, 0.1), 5.0)
                T_final = max(T_final, 0.5)
                snap_interval = T_final / 10

                log_progress(f"  Evolving to T={T_final:.3f}...")
                _, _, _, snapshots = solver.run(ux_hat, uy_hat, uz_hat, T_final,
                                                 snapshot_interval=snap_interval)
                log_progress(f"  Got {len(snapshots)} snapshots")

                # Use last snapshot
                _, ux_hat_s, uy_hat_s, uz_hat_s = snapshots[-1]
                ux_p = solver.to_physical(solver.dealias(ux_hat_s))
                uy_p = solver.to_physical(solver.dealias(uy_hat_s))
                uz_p = solver.to_physical(solver.dealias(uz_hat_s))
                spd = np.sqrt(ux_p**2 + uy_p**2 + uz_p**2)
                nf = max(np.max(spd), 1e-30)
                log_progress(f"  norm_factor = {nf:.6f}")

                # Check energy decay
                E_final = 0.5 * np.mean(ux_p**2 + uy_p**2 + uz_p**2)
                log_progress(f"  E_final = {E_final:.6f}")

                # Task A
                ta = {'ic': ic_name, 'Re': Re, 'N': N, 'norm_factor': float(nf),
                      'E_final': float(E_final),
                      'beltrami_deficits': [], 'lambda_opts': [],
                      'div_ub_L2': [], 'frac_above': []}

                for k in k_values:
                    ub_x, ub_y, ub_z, ux_n, uy_n, uz_n, sp = compute_u_below(
                        solver, ux_hat_s, uy_hat_s, uz_hat_s, k, nf)
                    lam_k, B_k = compute_beltrami_deficit(solver, ub_x, ub_y, ub_z)
                    div_ub = spectral_div_phys(solver, ub_x, ub_y, ub_z)
                    threshold = 1.0 - 2.0**(-k)
                    fa = float(np.mean(sp > threshold))

                    ta['beltrami_deficits'].append(float(B_k))
                    ta['lambda_opts'].append(float(lam_k))
                    ta['div_ub_L2'].append(float(np.sqrt(np.sum(div_ub**2) * (2*np.pi)**3 / N**3)))
                    ta['frac_above'].append(fa)

                lam_full, B_full = compute_beltrami_deficit(solver, ux_p/nf, uy_p/nf, uz_p/nf)
                ta['B_full'] = float(B_full)
                ta['lambda_opt_full'] = float(lam_full)

                log_progress(f"  Task A: B_full={B_full:.6f}")
                for k in [0, 2, 4, 6, 8]:
                    log_progress(f"    k={k}: B={ta['beltrami_deficits'][k]:.6f}, "
                               f"div={ta['div_ub_L2'][k]:.4e}, frac_above={ta['frac_above'][k]:.4f}")

                all_results['task_a'].append(ta)

                # Task B
                tb = {'ic': ic_name, 'Re': Re, 'N': N, 'k_results': []}

                for k in k_values:
                    ub_x, ub_y, ub_z, ux_n, uy_n, uz_n, sp = compute_u_below(
                        solver, ux_hat_s, uy_hat_s, uz_hat_s, k, nf)
                    decomp = compute_pressure_decomposition(solver, ub_x, ub_y, ub_z)
                    I_t, I_h, I_r = compute_bottleneck_contributions(
                        solver, ux_n, uy_n, uz_n, k,
                        decomp['P_total'], decomp['P_hessian'], decomp['P_remainder'])

                    r_frac = I_r / max(I_t, 1e-30) if I_t > 1e-30 else 0.0
                    h_frac_bn = I_h / max(I_t, 1e-30) if I_t > 1e-30 else 0.0

                    kr = {
                        'k': k,
                        'P_total_L2': decomp['P_total_L2'],
                        'P_hessian_L2': decomp['P_hessian_L2'],
                        'P_remainder_L2': decomp['P_remainder_L2'],
                        'hessian_frac_L2': decomp['hessian_frac_L2'],
                        'remainder_frac_L2': decomp['remainder_frac_L2'],
                        'Lamb_L2': decomp['Lamb_L2'],
                        'div_ub_L2': decomp['div_ub_L2'],
                        'I_total': I_t, 'I_hessian': I_h, 'I_remainder': I_r,
                        'remainder_bn_frac': float(r_frac),
                        'hessian_bn_frac': float(h_frac_bn),
                    }
                    tb['k_results'].append(kr)

                log_progress(f"  Task B:")
                for k in [0, 2, 4, 6, 8]:
                    kr = tb['k_results'][k]
                    log_progress(f"    k={k}: H_frac={kr['hessian_frac_L2']:.4f}, "
                               f"R_frac={kr['remainder_frac_L2']:.6f}, "
                               f"I_r/I_t={kr['remainder_bn_frac']:.4f}, "
                               f"I_h/I_t={kr['hessian_bn_frac']:.4f}")

                all_results['task_b'].append(tb)

                with open(RESULTS_FILE, 'w') as f:
                    json.dump(all_results, f, indent=2)

            except Exception as e:
                log_progress(f"  ERROR: {e}")
                import traceback; traceback.print_exc()

    # Convergence: ABC Re=500, N=128
    log_progress(f"\n{'='*60}")
    log_progress("CONVERGENCE: ABC Re=500, N=128")
    log_progress(f"{'='*60}")

    try:
        Re = 500; Nc = 128; nu = 1.0/Re
        solver = NavierStokesSolver(Nc, nu, cfl=0.4)
        ux_hat, uy_hat, uz_hat = abc_flow_ic(solver)
        T_final = min(2.0 * np.pi / max(Re**0.5 * 0.01, 0.1), 5.0)
        T_final = max(T_final, 0.5)
        snap_interval = T_final / 10

        log_progress(f"  Evolving to T={T_final:.3f}...")
        _, _, _, snapshots = solver.run(ux_hat, uy_hat, uz_hat, T_final, snapshot_interval=snap_interval)
        _, ux_hat_s, uy_hat_s, uz_hat_s = snapshots[-1]
        ux_p = solver.to_physical(solver.dealias(ux_hat_s))
        uy_p = solver.to_physical(solver.dealias(uy_hat_s))
        uz_p = solver.to_physical(solver.dealias(uz_hat_s))
        spd = np.sqrt(ux_p**2 + uy_p**2 + uz_p**2)
        nf = max(np.max(spd), 1e-30)

        conv = {'ic': 'ABC', 'Re': Re, 'N': Nc, 'norm_factor': float(nf),
                'B_deficits': [], 'remainder_fracs': [], 'remainder_bn_fracs': []}

        for k in k_values:
            ub_x, ub_y, ub_z, ux_n, uy_n, uz_n, sp = compute_u_below(
                solver, ux_hat_s, uy_hat_s, uz_hat_s, k, nf)
            lam_k, B_k = compute_beltrami_deficit(solver, ub_x, ub_y, ub_z)
            decomp = compute_pressure_decomposition(solver, ub_x, ub_y, ub_z)
            I_t, I_h, I_r = compute_bottleneck_contributions(
                solver, ux_n, uy_n, uz_n, k,
                decomp['P_total'], decomp['P_hessian'], decomp['P_remainder'])
            r_frac = I_r / max(I_t, 1e-30) if I_t > 1e-30 else 0.0

            conv['B_deficits'].append(float(B_k))
            conv['remainder_fracs'].append(decomp['remainder_frac_L2'])
            conv['remainder_bn_fracs'].append(float(r_frac))

            if k in [0, 4, 8]:
                log_progress(f"  N=128 k={k}: B={B_k:.6f}, R_frac={decomp['remainder_frac_L2']:.6f}, "
                           f"R_bn={r_frac:.4f}")

        all_results['convergence'] = conv

    except Exception as e:
        log_progress(f"  CONVERGENCE ERROR: {e}")
        import traceback; traceback.print_exc()

    with open(RESULTS_FILE, 'w') as f:
        json.dump(all_results, f, indent=2)
    log_progress(f"\nCompleted: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_progress("DONE")
    return all_results


if __name__ == '__main__':
    run_all()
