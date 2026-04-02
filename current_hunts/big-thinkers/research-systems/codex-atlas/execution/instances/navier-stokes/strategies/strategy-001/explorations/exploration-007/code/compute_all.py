#!/usr/bin/env python3
"""
Exploration 007: BMO norms, intermittency calibration, BKM vs Ladyzhenskaya advantage.

Computes:
  Part A: BKM slack ratio vs Ladyzhenskaya/Agmon slack ratio
  Part B: BMO norms of vorticity
  Part C: Spatial intermittency (flatness, volume fractions)
  Part D: Conditional enstrophy bound synthesis

Uses the NS solver infrastructure from exploration 002.
"""

import numpy as np
from numpy.fft import fftn, ifftn
import json
import time
import sys
import os

# Add exploration 002 code to path
E002_CODE = os.path.join(os.path.dirname(__file__), '..', '..', 'exploration-002', 'code')
sys.path.insert(0, E002_CODE)

from ns_solver import NavierStokesSolver, taylor_green_ic
from slack_measurements import compute_extended_diagnostics, compute_constants_on_torus

# Output directory
OUTDIR = os.path.dirname(__file__)
RESULTS_FILE = os.path.join(OUTDIR, '..', 'results_007.json')
PROGRESS_FILE = os.path.join(OUTDIR, '..', 'progress.txt')

def write_progress(msg):
    with open(PROGRESS_FILE, 'a') as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    print(msg)


# =============================================================================
# Part A: BKM Slack Computation
# =============================================================================

def compute_bkm_quantities(solver, ux_hat, uy_hat, uz_hat):
    """
    Compute BKM-related quantities:
    - ||omega||_{L^inf}
    - ||omega||_{H^1} / ||omega||_{L^2}
    - ||nabla u||_{L^inf} (actual)
    - BKM bound: C_{BKM} * ||omega||_{L^inf} * (1 + log(1 + ||omega||_{H1}/||omega||_{L2}))

    The BKM inequality (Beale-Kato-Majda 1984, Beirao da Veiga variant):
    ||nabla u||_{L^inf} <= C * ||omega||_{L^inf} * (1 + log^+(||omega||_{H^1}/||omega||_{L^2}))

    The constant C is universal (dimension-dependent). For T^3, a safe estimate is C ~ 1/(4*pi).
    The logarithmic term is what makes this much tighter than Agmon for smooth fields.

    Returns dict with all quantities.
    """
    N = solver.N
    vol = (2 * np.pi)**3
    norm_factor = vol / N**6

    # Vorticity in spectral space
    omega_x_hat = 1j * (solver.KY * uz_hat - solver.KZ * uy_hat)
    omega_y_hat = 1j * (solver.KZ * ux_hat - solver.KX * uz_hat)
    omega_z_hat = 1j * (solver.KX * uy_hat - solver.KY * ux_hat)

    # Vorticity in physical space
    omega_x = solver.to_physical(omega_x_hat)
    omega_y = solver.to_physical(omega_y_hat)
    omega_z = solver.to_physical(omega_z_hat)

    omega_mag = np.sqrt(omega_x**2 + omega_y**2 + omega_z**2)
    omega_Linf = np.max(omega_mag)

    # ||omega||_{L^2} via Parseval
    omega_L2_sq = norm_factor * (np.sum(np.abs(omega_x_hat)**2) +
                                  np.sum(np.abs(omega_y_hat)**2) +
                                  np.sum(np.abs(omega_z_hat)**2)).real
    omega_L2 = np.sqrt(omega_L2_sq)

    # ||nabla omega||_{L^2} via Parseval
    K2 = solver.K2
    grad_omega_L2_sq = norm_factor * (np.sum(K2 * np.abs(omega_x_hat)**2) +
                                       np.sum(K2 * np.abs(omega_y_hat)**2) +
                                       np.sum(K2 * np.abs(omega_z_hat)**2)).real
    grad_omega_L2 = np.sqrt(grad_omega_L2_sq)

    # ||omega||_{H^1} = (||omega||_{L^2}^2 + ||nabla omega||_{L^2}^2)^{1/2}
    omega_H1 = np.sqrt(omega_L2_sq + grad_omega_L2_sq)

    # H1/L2 ratio
    h1_l2_ratio = omega_H1 / omega_L2 if omega_L2 > 1e-30 else 1.0

    # ||nabla u||_{L^inf} (actual)
    dux_dx = solver.to_physical(1j * solver.KX * ux_hat)
    dux_dy = solver.to_physical(1j * solver.KY * ux_hat)
    dux_dz = solver.to_physical(1j * solver.KZ * ux_hat)
    duy_dx = solver.to_physical(1j * solver.KX * uy_hat)
    duy_dy = solver.to_physical(1j * solver.KY * uy_hat)
    duy_dz = solver.to_physical(1j * solver.KZ * uy_hat)
    duz_dx = solver.to_physical(1j * solver.KX * uz_hat)
    duz_dy = solver.to_physical(1j * solver.KY * uz_hat)
    duz_dz = solver.to_physical(1j * solver.KZ * uz_hat)

    grad_sq = (dux_dx**2 + dux_dy**2 + dux_dz**2 +
               duy_dx**2 + duy_dy**2 + duy_dz**2 +
               duz_dx**2 + duz_dy**2 + duz_dz**2)
    grad_u_Linf = np.sqrt(np.max(grad_sq))

    # BKM bound constant
    # From the Biot-Savart law on T^3: u = K * omega, nabla u = nabla K * omega
    # ||nabla u||_{L^inf} <= C * ||omega||_{L^inf} * (1 + log(||omega||_{H^1}/||omega||_{L^2}))
    # The constant C on T^3 comes from the kernel estimate.
    # We use C = 1 as the universal order-1 constant (the goal is the RATIO comparison,
    # so the absolute value of C cancels in BKM_slack vs Ladyzhenskaya_slack).
    # Actually, to get a meaningful slack ratio, we need a valid upper bound.
    # From BKM/Beirao da Veiga: C depends only on dimension.
    # A standard estimate: C_{BKM} ~ 1/(4*pi) * 3 (accounting for dim 3) ~ 0.24
    # But more commonly in the literature, C ~ O(1). We'll calibrate below.

    # For comparing slack ratios, we compute the BKM bound with an empirically calibrated
    # constant that makes the bound valid (bound >= actual at all times).
    # BKM bound (with C=1 placeholder):
    log_term = 1.0 + np.log(1.0 + h1_l2_ratio)
    bkm_bound_no_C = omega_Linf * log_term

    return {
        'omega_Linf': omega_Linf,
        'omega_L2': omega_L2,
        'omega_H1': omega_H1,
        'grad_omega_L2': grad_omega_L2,
        'h1_l2_ratio': h1_l2_ratio,
        'log_term': log_term,
        'grad_u_Linf': grad_u_Linf,
        'bkm_bound_no_C': bkm_bound_no_C,
        # Fields for BMO computation
        'omega_x': omega_x,
        'omega_y': omega_y,
        'omega_z': omega_z,
        'omega_mag': omega_mag,
    }


# =============================================================================
# Part B: BMO Norm Computation
# =============================================================================

def compute_bmo_norm(omega_mag, N, n_radii=5, n_centers=200, rng=None):
    """
    Compute the BMO semi-norm of |omega| on T^3 = [0, 2*pi]^3.

    ||f||_{BMO} = sup_B (1/|B|) int_B |f - f_B| dx

    We approximate by sampling balls of various radii at random centers.
    On the discrete grid, a "ball" is all grid points within distance r.

    Args:
        omega_mag: |omega| on the grid (N x N x N)
        N: grid size
        n_radii: number of radii to sample
        n_centers: number of random centers per radius
        rng: random state

    Returns:
        bmo_norm: estimated BMO norm
        bmo_by_radius: BMO norm estimate at each radius
    """
    if rng is None:
        rng = np.random.RandomState(42)

    dx = 2 * np.pi / N
    L = 2 * np.pi

    # Radii to sample (from L/4 down to L/64)
    radii = [L / (2**k) for k in range(2, 2 + n_radii)]  # L/4, L/8, L/16, L/32, L/64

    max_osc = 0.0
    bmo_by_radius = {}

    for r in radii:
        r_grid = int(np.ceil(r / dx))  # radius in grid points
        if r_grid < 1:
            r_grid = 1
        if r_grid > N // 2:
            r_grid = N // 2

        # Precompute the ball mask (relative offsets within radius r)
        offsets = []
        for di in range(-r_grid, r_grid + 1):
            for dj in range(-r_grid, r_grid + 1):
                for dk in range(-r_grid, r_grid + 1):
                    dist = np.sqrt((di * dx)**2 + (dj * dx)**2 + (dk * dx)**2)
                    if dist <= r:
                        offsets.append((di, dj, dk))

        n_ball = len(offsets)
        if n_ball == 0:
            continue

        offsets = np.array(offsets, dtype=int)

        max_osc_r = 0.0

        for _ in range(n_centers):
            # Random center
            ci = rng.randint(0, N)
            cj = rng.randint(0, N)
            ck = rng.randint(0, N)

            # Extract values in ball (periodic boundary)
            ii = (ci + offsets[:, 0]) % N
            jj = (cj + offsets[:, 1]) % N
            kk = (ck + offsets[:, 2]) % N

            vals = omega_mag[ii, jj, kk]

            # Mean oscillation: (1/|B|) * sum |f - f_B|
            f_B = np.mean(vals)
            mean_osc = np.mean(np.abs(vals - f_B))

            if mean_osc > max_osc_r:
                max_osc_r = mean_osc
            if mean_osc > max_osc:
                max_osc = mean_osc

        bmo_by_radius[r] = max_osc_r

    return max_osc, bmo_by_radius


# =============================================================================
# Part C: Intermittency Measures
# =============================================================================

def compute_intermittency(omega_mag, omega_L2_sq, N):
    """
    Compute intermittency measures for the vorticity field.

    Args:
        omega_mag: |omega| field (N x N x N)
        omega_L2_sq: ||omega||_{L^2}^2 (volume integral)
        N: grid size

    Returns:
        dict with flatness, volume fractions, etc.
    """
    vol = (2 * np.pi)**3

    # Flatness F_4 = ||omega||^4_{L^4} / (||omega||^2_{L^2})^2
    # ||omega||^4_{L^4} = int |omega|^4 dx
    omega_L4_4 = np.mean(omega_mag**4) * vol
    # ||omega||^2_{L^2} = omega_L2_sq (already a volume integral)

    F4 = omega_L4_4 / omega_L2_sq**2 if omega_L2_sq > 1e-30 else 0.0

    # Note: For a 3-component vector field with Gaussian components,
    # |omega|^2 = omega_x^2 + omega_y^2 + omega_z^2 ~ chi^2_3
    # E[|omega|^4] / (E[|omega|^2])^2 = E[chi^4_3] / (E[chi^2_3])^2 = 15/9 = 5/3
    # So the Gaussian prediction is F_4 = 5/3 ≈ 1.667
    # (where E[chi^4_3] = 3*5 = 15, E[chi^2_3] = 3)
    # Wait, need to be careful. Let sigma^2 = variance of each component.
    # |omega|^2 = omega_x^2 + omega_y^2 + omega_z^2 = sigma^2 * chi^2_3
    # E[|omega|^4] = sigma^4 * E[(chi^2_3)^2] = sigma^4 * (3^2 + 2*3) = sigma^4 * 15
    # (E[|omega|^2])^2 = (sigma^2 * 3)^2 = 9 * sigma^4
    # F_4 = 15/9 = 5/3
    # But our definition is with L^p norms (volume integrals):
    # F_4 = (int |omega|^4 dx) / (int |omega|^2 dx)^2
    # For a homogeneous field: = E[|omega|^4] * vol / (E[|omega|^2] * vol)^2
    # = E[|omega|^4] / (vol * E[|omega|^2]^2)
    # Hmm, this doesn't simplify the same way.
    # Actually with the volume-averaged definition:
    # F_4 = <|omega|^4> / <|omega|^2>^2  (where <.> = volume average = (1/vol) int)
    # = E[|omega|^4] / E[|omega|^2]^2 = 5/3 for Gaussian
    # But with the L^p norm definition:
    # ||omega||^4_{L^4} = int |omega|^4 dx = vol * <|omega|^4>
    # ||omega||^2_{L^2} = int |omega|^2 dx = vol * <|omega|^2>
    # (||omega||^2_{L^2})^2 = vol^2 * <|omega|^2>^2
    # So F_4 = vol * <|omega|^4> / (vol^2 * <|omega|^2>^2) = <|omega|^4> / (vol * <|omega|^2>^2)
    # This gives a volume-dependent quantity. The goal likely means the DIMENSIONLESS flatness:
    # F_4 = <|omega|^4> / <|omega|^2>^2 (volume averages)

    omega_4_avg = np.mean(omega_mag**4)
    omega_2_avg = np.mean(omega_mag**2)
    F4_dimless = omega_4_avg / omega_2_avg**2 if omega_2_avg > 1e-30 else 0.0

    # Volume fractions mu(lambda)
    omega_Linf = np.max(omega_mag)
    lambdas = [0.1, 0.3, 0.5, 0.7, 0.9]
    mu = {}
    for lam in lambdas:
        threshold = lam * omega_Linf
        mu[lam] = np.mean(omega_mag > threshold)  # fraction of grid points

    return {
        'F4': F4,
        'F4_dimless': F4_dimless,
        'omega_4_avg': omega_4_avg,
        'omega_2_avg': omega_2_avg,
        'omega_Linf': omega_Linf,
        'mu': mu,
    }


def compute_effective_lady_constant(solver, ux_hat, uy_hat, uz_hat):
    """
    Compute the effective Ladyzhenskaya constant for this flow state.

    C_{L,eff}^4 = ||u||^4_{L^4} / (||u||_{L^2} * ||grad u||_{L^2}^3)

    Also compute for vorticity:
    C_{L,eff,omega}^4 = ||omega||^4_{L^4} / (||omega||_{L^2} * ||grad omega||_{L^2}^3)
    """
    N = solver.N
    vol = (2 * np.pi)**3
    norm_factor = vol / N**6

    # Velocity norms
    ux = solver.to_physical(ux_hat)
    uy = solver.to_physical(uy_hat)
    uz = solver.to_physical(uz_hat)
    u_sq = ux**2 + uy**2 + uz**2

    u_L4_4 = np.mean(u_sq**2) * vol
    u_L2_sq = norm_factor * (np.sum(np.abs(ux_hat)**2) + np.sum(np.abs(uy_hat)**2) + np.sum(np.abs(uz_hat)**2)).real
    u_L2 = np.sqrt(u_L2_sq)

    K2 = solver.K2
    grad_u_L2_sq = norm_factor * (np.sum(K2 * np.abs(ux_hat)**2) + np.sum(K2 * np.abs(uy_hat)**2) + np.sum(K2 * np.abs(uz_hat)**2)).real
    grad_u_L2 = np.sqrt(grad_u_L2_sq)

    if u_L2 > 1e-30 and grad_u_L2 > 1e-30:
        C_L_eff_4 = u_L4_4 / (u_L2 * grad_u_L2**3)
    else:
        C_L_eff_4 = 0.0

    # Vorticity norms
    omega_x_hat = 1j * (solver.KY * uz_hat - solver.KZ * uy_hat)
    omega_y_hat = 1j * (solver.KZ * ux_hat - solver.KX * uz_hat)
    omega_z_hat = 1j * (solver.KX * uy_hat - solver.KY * ux_hat)

    omega_x = solver.to_physical(omega_x_hat)
    omega_y = solver.to_physical(omega_y_hat)
    omega_z = solver.to_physical(omega_z_hat)
    omega_sq = omega_x**2 + omega_y**2 + omega_z**2

    omega_L4_4 = np.mean(omega_sq**2) * vol
    omega_L2_sq = norm_factor * (np.sum(np.abs(omega_x_hat)**2) + np.sum(np.abs(omega_y_hat)**2) + np.sum(np.abs(omega_z_hat)**2)).real
    omega_L2 = np.sqrt(omega_L2_sq)

    grad_omega_L2_sq = norm_factor * (np.sum(K2 * np.abs(omega_x_hat)**2) + np.sum(K2 * np.abs(omega_y_hat)**2) + np.sum(K2 * np.abs(omega_z_hat)**2)).real
    grad_omega_L2 = np.sqrt(grad_omega_L2_sq)

    if omega_L2 > 1e-30 and grad_omega_L2 > 1e-30:
        C_L_eff_omega_4 = omega_L4_4 / (omega_L2 * grad_omega_L2**3)
    else:
        C_L_eff_omega_4 = 0.0

    return {
        'C_L_eff_4': C_L_eff_4,
        'C_L_eff': C_L_eff_4 ** 0.25 if C_L_eff_4 > 0 else 0,
        'C_L_eff_omega_4': C_L_eff_omega_4,
        'C_L_eff_omega': C_L_eff_omega_4 ** 0.25 if C_L_eff_omega_4 > 0 else 0,
    }


# =============================================================================
# Main Simulation Loop
# =============================================================================

def run_exploration(Re_values, N_base=64, T_final=5.0, n_samples=60):
    """
    Run DNS for each Re value and compute all Part A-C quantities.
    """
    all_results = {}
    constants = compute_constants_on_torus(N_sum=30)
    C_L = constants['C_L']  # vector Ladyzhenskaya constant
    C_Agmon = constants['C_Agmon']

    write_progress(f"Starting exploration 007: Re = {Re_values}")
    write_progress(f"C_L = {C_L:.6f}, C_Agmon = {C_Agmon:.6f}")

    for Re in Re_values:
        # Choose resolution
        if Re <= 100:
            N = min(N_base, 48)
        elif Re <= 1000:
            N = N_base
        else:
            N = N_base  # 64 is enough for Re=5000 with dealiasing up to T~3

        nu = 1.0 / Re
        solver = NavierStokesSolver(N, nu, cfl=0.5)

        write_progress(f"\n=== Re={Re}, N={N}, nu={nu:.6f} ===")

        # Initial condition
        ux_hat, uy_hat, uz_hat = taylor_green_ic(solver, Re)

        t = 0.0
        step = 0
        dt_sample = T_final / n_samples
        next_sample = 0.0

        time_series = []

        t_start = time.time()

        while t < T_final:
            dt = solver.compute_dt(ux_hat, uy_hat, uz_hat)
            dt = min(dt, T_final - t)
            if dt < 1e-12:
                write_progress(f"WARNING: dt too small at t={t:.4f}")
                break

            ux_hat, uy_hat, uz_hat = solver.rk4_step(ux_hat, uy_hat, uz_hat, dt)
            t += dt
            step += 1

            if t >= next_sample - 1e-10:
                # Compute standard diagnostics
                diag = compute_extended_diagnostics(solver, ux_hat, uy_hat, uz_hat)

                # Part A: BKM quantities
                bkm = compute_bkm_quantities(solver, ux_hat, uy_hat, uz_hat)

                # Part B: BMO norm (compute for a subset of timesteps to save time)
                do_bmo = (len(time_series) % 5 == 0)  # every 5th sample
                if do_bmo:
                    bmo_norm, bmo_by_radius = compute_bmo_norm(
                        bkm['omega_mag'], N, n_radii=5, n_centers=150)
                else:
                    bmo_norm = None
                    bmo_by_radius = None

                # Part C: Intermittency
                intermittency = compute_intermittency(
                    bkm['omega_mag'], diag['omega_L2_sq'], N)

                # Effective Ladyzhenskaya constant
                lady_eff = compute_effective_lady_constant(solver, ux_hat, uy_hat, uz_hat)

                # Agmon bound (Ladyzhenskaya-based): C_Agmon * ||u||_{H^2}^{1/2} * ||u||_{H^3}^{1/2}
                agmon_bound = C_Agmon * diag['u_H2']**0.5 * diag['u_H3']**0.5
                agmon_slack = agmon_bound / diag['grad_u_Linf'] if diag['grad_u_Linf'] > 1e-30 else np.inf

                # Ladyzhenskaya slack (vortex stretching):
                # C_L^2 * ||omega||_{L^2}^{3/2} * ||grad_omega||_{L^2}^{3/2} / |vortex_stretching|
                lad_vs_bound = C_L**2 * diag['omega_L2']**1.5 * diag['grad_omega_L2']**1.5
                lad_vs_slack = lad_vs_bound / diag['abs_vortex_stretching'] if diag['abs_vortex_stretching'] > 1e-30 else np.inf

                record = {
                    'time': t,
                    'step': step,
                    'energy': diag['energy'],
                    'enstrophy': diag['enstrophy'],
                    'omega_L2': diag['omega_L2'],
                    'omega_Linf': bkm['omega_Linf'],
                    'omega_H1': bkm['omega_H1'],
                    'h1_l2_ratio': bkm['h1_l2_ratio'],
                    'log_term': bkm['log_term'],
                    'grad_u_Linf': bkm['grad_u_Linf'],
                    'bkm_bound_no_C': bkm['bkm_bound_no_C'],
                    'bkm_ratio': bkm['grad_u_Linf'] / bkm['bkm_bound_no_C'] if bkm['bkm_bound_no_C'] > 1e-30 else 0,
                    'agmon_bound': agmon_bound,
                    'agmon_slack': agmon_slack,
                    'lad_vs_bound': lad_vs_bound,
                    'lad_vs_slack': lad_vs_slack,
                    'abs_vortex_stretching': diag['abs_vortex_stretching'],
                    'grad_omega_L2': diag['grad_omega_L2'],
                    'u_H2': diag['u_H2'],
                    'u_H3': diag['u_H3'],
                    # BMO
                    'bmo_norm': bmo_norm,
                    'bmo_by_radius': {str(k): v for k, v in bmo_by_radius.items()} if bmo_by_radius else None,
                    'bmo_Linf_ratio': bmo_norm / bkm['omega_Linf'] if (bmo_norm is not None and bkm['omega_Linf'] > 1e-30) else None,
                    # Intermittency
                    'F4': intermittency['F4_dimless'],
                    'mu': intermittency['mu'],
                    # Effective Ladyzhenskaya
                    'C_L_eff': lady_eff['C_L_eff'],
                    'C_L_eff_omega': lady_eff['C_L_eff_omega'],
                    'C_L_eff_ratio': lady_eff['C_L_eff'] / C_L if C_L > 0 else 0,
                    'C_L_eff_omega_ratio': lady_eff['C_L_eff_omega'] / C_L if C_L > 0 else 0,
                }

                time_series.append(record)

                if len(time_series) % 10 == 0:
                    write_progress(f"  t={t:.3f}, E={diag['energy']:.4f}, "
                                   f"omega_Linf={bkm['omega_Linf']:.4f}, "
                                   f"BKM_ratio={record['bkm_ratio']:.4f}, "
                                   f"Agmon_slack={agmon_slack:.1f}")

                next_sample += dt_sample

        elapsed = time.time() - t_start
        write_progress(f"Re={Re}: {step} steps in {elapsed:.1f}s")

        # Calibrate BKM constant: find C such that C * bkm_bound_no_C >= grad_u_Linf for all t
        max_bkm_ratio = max(r['bkm_ratio'] for r in time_series if r['bkm_ratio'] > 0)
        C_BKM_calibrated = max_bkm_ratio * 1.05  # 5% safety margin

        # Compute BKM slack with calibrated constant
        for r in time_series:
            r['C_BKM'] = C_BKM_calibrated
            r['bkm_bound'] = C_BKM_calibrated * r['bkm_bound_no_C']
            r['bkm_slack'] = r['bkm_bound'] / r['grad_u_Linf'] if r['grad_u_Linf'] > 1e-30 else np.inf

        all_results[Re] = {
            'N': N,
            'Re': Re,
            'nu': nu,
            'n_steps': step,
            'time_series': time_series,
            'C_BKM_calibrated': C_BKM_calibrated,
            'max_bkm_ratio': max_bkm_ratio,
        }

    return all_results, constants


def analyze_and_print(all_results, constants):
    """Analyze all results and produce summary tables."""
    C_L = constants['C_L']

    write_progress("\n" + "="*100)
    write_progress("PART A: BKM vs Ladyzhenskaya Comparison")
    write_progress("="*100)

    # Table header
    print(f"\n{'Re':>6} | {'Lad VS min slack':>16} | {'Agmon min slack':>16} | {'BKM min slack':>14} | {'BKM adv (Lad/BKM)':>18} | {'BKM adv (Ag/BKM)':>17}")
    print("-"*100)

    summary_table = []

    for Re in sorted(all_results.keys()):
        data = all_results[Re]
        ts = data['time_series']

        # Filter to t > 0.5 to skip transient
        ts_f = [r for r in ts if r['time'] > 0.5]
        if not ts_f:
            ts_f = ts

        lad_slacks = [r['lad_vs_slack'] for r in ts_f if np.isfinite(r['lad_vs_slack'])]
        agmon_slacks = [r['agmon_slack'] for r in ts_f if np.isfinite(r['agmon_slack'])]
        bkm_slacks = [r['bkm_slack'] for r in ts_f if np.isfinite(r['bkm_slack'])]

        lad_min = min(lad_slacks) if lad_slacks else np.inf
        agmon_min = min(agmon_slacks) if agmon_slacks else np.inf
        bkm_min = min(bkm_slacks) if bkm_slacks else np.inf

        lad_mean = np.mean(lad_slacks) if lad_slacks else np.inf
        agmon_mean = np.mean(agmon_slacks) if agmon_slacks else np.inf
        bkm_mean = np.mean(bkm_slacks) if bkm_slacks else np.inf

        bkm_adv_lad = lad_min / bkm_min if bkm_min > 0 else np.inf
        bkm_adv_agmon = agmon_min / bkm_min if bkm_min > 0 else np.inf

        # Time-averaged advantage
        bkm_adv_lad_mean = lad_mean / bkm_mean if bkm_mean > 0 else np.inf
        bkm_adv_agmon_mean = agmon_mean / bkm_mean if bkm_mean > 0 else np.inf

        print(f"{Re:>6} | {lad_min:>16.2f} | {agmon_min:>16.2f} | {bkm_min:>14.2f} | {bkm_adv_lad:>18.2f} | {bkm_adv_agmon:>17.2f}")

        summary_table.append({
            'Re': Re,
            'lad_vs_min_slack': lad_min,
            'lad_vs_mean_slack': lad_mean,
            'agmon_min_slack': agmon_min,
            'agmon_mean_slack': agmon_mean,
            'bkm_min_slack': bkm_min,
            'bkm_mean_slack': bkm_mean,
            'bkm_advantage_lad_min': bkm_adv_lad,
            'bkm_advantage_agmon_min': bkm_adv_agmon,
            'bkm_advantage_lad_mean': bkm_adv_lad_mean,
            'bkm_advantage_agmon_mean': bkm_adv_agmon_mean,
            'C_BKM': data['C_BKM_calibrated'],
        })

    print(f"\nNote: BKM advantage = Ladyzhenskaya_slack / BKM_slack (higher = BKM is tighter)")
    print(f"C_L (vector) = {C_L:.6f}")

    # Time-averaged table
    print(f"\n{'Re':>6} | {'Lad VS mean':>12} | {'Agmon mean':>11} | {'BKM mean':>10} | {'BKM adv mean(L/B)':>18}")
    print("-"*70)
    for s in summary_table:
        print(f"{s['Re']:>6} | {s['lad_vs_mean_slack']:>12.2f} | {s['agmon_mean_slack']:>11.2f} | {s['bkm_mean_slack']:>10.2f} | {s['bkm_advantage_lad_mean']:>18.2f}")

    # =========================================================================
    write_progress("\n" + "="*100)
    write_progress("PART B: BMO Norms")
    write_progress("="*100)

    print(f"\n{'Re':>6} | {'||omega||_Linf mean':>20} | {'||omega||_BMO mean':>20} | {'BMO/Linf ratio':>15} | {'Trend':>10}")
    print("-"*80)

    bmo_summary = []
    for Re in sorted(all_results.keys()):
        ts = all_results[Re]['time_series']
        ts_bmo = [r for r in ts if r['bmo_norm'] is not None and r['time'] > 0.5]

        if not ts_bmo:
            print(f"{Re:>6} | {'no data':>20} |")
            continue

        omega_Linf_vals = [r['omega_Linf'] for r in ts_bmo]
        bmo_vals = [r['bmo_norm'] for r in ts_bmo]
        ratio_vals = [r['bmo_Linf_ratio'] for r in ts_bmo if r['bmo_Linf_ratio'] is not None]

        omega_Linf_mean = np.mean(omega_Linf_vals)
        bmo_mean = np.mean(bmo_vals)
        ratio_mean = np.mean(ratio_vals) if ratio_vals else 0

        print(f"{Re:>6} | {omega_Linf_mean:>20.4f} | {bmo_mean:>20.4f} | {ratio_mean:>15.4f} | {'see text':>10}")

        bmo_summary.append({
            'Re': Re,
            'omega_Linf_mean': omega_Linf_mean,
            'bmo_mean': bmo_mean,
            'bmo_Linf_ratio': ratio_mean,
        })

    # =========================================================================
    write_progress("\n" + "="*100)
    write_progress("PART C: Intermittency Measures")
    write_progress("="*100)

    print(f"\n{'Re':>6} | {'F4 mean':>8} | {'F4 peak_enst':>13} | {'mu(0.1)':>8} | {'mu(0.3)':>8} | {'mu(0.5)':>8} | {'mu(0.7)':>8} | {'mu(0.9)':>8} | {'C_L,eff/C_L':>12}")
    print("-"*110)

    intermittency_summary = []
    for Re in sorted(all_results.keys()):
        ts = all_results[Re]['time_series']
        ts_f = [r for r in ts if r['time'] > 0.5]
        if not ts_f:
            ts_f = ts

        F4_vals = [r['F4'] for r in ts_f]
        F4_mean = np.mean(F4_vals)

        # Find peak enstrophy timestep
        peak_idx = np.argmax([r['enstrophy'] for r in ts_f])
        F4_peak = ts_f[peak_idx]['F4']
        mu_peak = ts_f[peak_idx]['mu']
        CL_ratio = ts_f[peak_idx]['C_L_eff_ratio']

        mu_strs = [f"{mu_peak.get(lam, 0):>8.4f}" for lam in [0.1, 0.3, 0.5, 0.7, 0.9]]

        print(f"{Re:>6} | {F4_mean:>8.3f} | {F4_peak:>13.3f} | {' | '.join(mu_strs)} | {CL_ratio:>12.4f}")

        # C_L_eff values over time
        CL_eff_vals = [r['C_L_eff'] for r in ts_f]
        CL_eff_omega_vals = [r['C_L_eff_omega'] for r in ts_f]
        CL_ratio_vals = [r['C_L_eff_ratio'] for r in ts_f]

        intermittency_summary.append({
            'Re': Re,
            'F4_mean': F4_mean,
            'F4_peak_enstrophy': F4_peak,
            'mu_0.5_peak': mu_peak.get(0.5, 0),
            'C_L_eff_mean': np.mean(CL_eff_vals),
            'C_L_eff_ratio_mean': np.mean(CL_ratio_vals),
            'C_L_eff_omega_mean': np.mean(CL_eff_omega_vals),
        })

    # Gaussian prediction check
    print(f"\nGaussian prediction: F4 = 5/3 = {5/3:.4f}")
    print(f"If F4 > 5/3, the field is MORE intermittent than Gaussian.")
    print(f"Exploration 006 predicted: C_{{L,eff}} ~ F_4^{{-1/4}} x constant")

    for s in intermittency_summary:
        F4_pred_ratio = (5.0/3.0 / s['F4_peak_enstrophy'])**0.25 if s['F4_peak_enstrophy'] > 0 else 0
        print(f"  Re={s['Re']}: C_L_eff/C_L = {s['C_L_eff_ratio_mean']:.4f}, "
              f"predicted from F4: {F4_pred_ratio:.4f} (ratio: {s['C_L_eff_ratio_mean']/F4_pred_ratio:.3f})" if F4_pred_ratio > 0 else "")

    # =========================================================================
    write_progress("\n" + "="*100)
    write_progress("PART D: Synthesis")
    write_progress("="*100)

    # For Part D, we compute the conditional bound:
    # |int S_ij omega_i omega_j dx| <= C(F_max) * ||omega||_{L^2}^{3/2} * ||grad omega||_{L^2}^{3/2}
    # where C(F_max) < C_L^2 when F_max < some threshold.
    #
    # From the vortex stretching bound chain:
    # |VS| <= ||S||_{L^2} * ||omega||_{L^4}^2
    # <= ||omega||_{L^2} * ||omega||_{L^4}^2   (since ||S|| <= ||grad u|| = ||omega|| for div-free)
    #
    # Now ||omega||_{L^4}^4 = F4 * (||omega||_{L^2}^2 / vol)^2 * vol  (from flatness definition)
    # = F4 * ||omega||_{L^2}^4 / vol
    # So ||omega||_{L^4}^2 = (F4)^{1/2} * ||omega||_{L^2}^2 / vol^{1/2}
    #
    # Wait, need to be more careful. Let's use the Ladyzhenskaya inequality:
    # ||omega||_{L^4} <= C_L * ||omega||_{L^2}^{1/4} * ||grad omega||_{L^2}^{3/4}
    #
    # The flatness enters differently. The Ladyzhenskaya slack for vorticity is:
    # C_L * ||omega||_{L^2}^{1/4} * ||grad omega||_{L^2}^{3/4} / ||omega||_{L^4}
    # = C_L / C_{L,eff,omega}
    #
    # So the vortex stretching bound becomes:
    # |VS| <= ||omega||_{L^2} * (C_{L,eff,omega})^2 * ||omega||_{L^2}^{1/2} * ||grad omega||_{L^2}^{3/2}
    # = (C_{L,eff,omega})^2 * ||omega||_{L^2}^{3/2} * ||grad omega||_{L^2}^{3/2}
    #
    # And C_{L,eff,omega} is what we can bound in terms of flatness.

    print("\nConditional Bound Analysis:")
    print(f"{'Re':>6} | {'C(F4) = actual VS / (||omega||^3/2 * ||grad omega||^3/2)':>55} | {'C_L^2':>8} | {'Ratio':>8}")
    print("-"*90)

    C_L_sq = C_L**2
    conditional_data = []

    for Re in sorted(all_results.keys()):
        ts = all_results[Re]['time_series']
        ts_f = [r for r in ts if r['time'] > 0.5 and r['abs_vortex_stretching'] > 1e-30]

        # Compute empirical C(F4) at each timestep
        for r in ts_f:
            denom = r['omega_L2']**1.5 * r['grad_omega_L2']**1.5
            if denom > 1e-30:
                C_empirical = r['abs_vortex_stretching'] / denom
                conditional_data.append({
                    'Re': Re,
                    'F4': r['F4'],
                    'C_empirical': C_empirical,
                    'C_ratio': C_empirical / C_L_sq,
                    'time': r['time'],
                })

        if conditional_data:
            recent = [d for d in conditional_data if d['Re'] == Re]
            max_C = max(d['C_empirical'] for d in recent)
            mean_C = np.mean([d['C_empirical'] for d in recent])
            print(f"{Re:>6} | max C_emp = {max_C:>12.6f}, mean C_emp = {mean_C:>12.6f} | {C_L_sq:>8.4f} | {max_C/C_L_sq:>8.4f}")

    # Fit C(F4) as a function of F4
    if conditional_data:
        F4_arr = np.array([d['F4'] for d in conditional_data])
        C_arr = np.array([d['C_empirical'] for d in conditional_data])

        # Fit: log(C) = a + b * log(F4)
        mask = (F4_arr > 0) & (C_arr > 0)
        if np.sum(mask) > 5:
            log_F4 = np.log(F4_arr[mask])
            log_C = np.log(C_arr[mask])
            A = np.vstack([log_F4, np.ones(np.sum(mask))]).T
            coeffs = np.linalg.lstsq(A, log_C, rcond=None)[0]
            b_fit, a_fit = coeffs
            C0_fit = np.exp(a_fit)

            print(f"\nFit: C(F4) ≈ {C0_fit:.6f} × F4^{b_fit:.3f}")
            print(f"At F4 = 5/3 (Gaussian): C = {C0_fit * (5/3)**b_fit:.6f}")
            print(f"At F4 = 3 (intermittent): C = {C0_fit * 3**b_fit:.6f}")
            print(f"Standard Ladyzhenskaya: C_L^2 = {C_L_sq:.6f}")

    return summary_table, bmo_summary, intermittency_summary, conditional_data


def save_results(all_results, constants, summary_table, bmo_summary, intermittency_summary, conditional_data):
    """Save all results to JSON."""
    output = {
        'constants': {k: float(v) for k, v in constants.items()},
        'summary_table': summary_table,
        'bmo_summary': bmo_summary,
        'intermittency_summary': intermittency_summary,
        'conditional_data_sample': conditional_data[:100] if conditional_data else [],  # save first 100
    }

    # Also save time series (compact form)
    for Re in sorted(all_results.keys()):
        ts = all_results[Re]['time_series']
        compact = []
        for r in ts:
            cr = {k: v for k, v in r.items() if k != 'bmo_by_radius'}
            # Convert mu dict keys to strings
            if 'mu' in cr and isinstance(cr['mu'], dict):
                cr['mu'] = {str(k): v for k, v in cr['mu'].items()}
            compact.append(cr)
        output[f'time_series_Re{Re}'] = compact

    with open(RESULTS_FILE, 'w') as f:
        json.dump(output, f, indent=2, default=lambda x: float(x) if isinstance(x, (np.floating, np.integer, np.bool_)) else str(x))

    write_progress(f"Results saved to {RESULTS_FILE}")


if __name__ == '__main__':
    Re_values = [100, 500, 1000, 5000]

    write_progress("="*60)
    write_progress("Exploration 007: BMO, Intermittency, BKM vs Ladyzhenskaya")
    write_progress("="*60)

    all_results, constants = run_exploration(Re_values, N_base=64, T_final=5.0, n_samples=60)
    summary_table, bmo_summary, intermittency_summary, conditional_data = analyze_and_print(all_results, constants)
    save_results(all_results, constants, summary_table, bmo_summary, intermittency_summary, conditional_data)

    write_progress("\nDone!")
