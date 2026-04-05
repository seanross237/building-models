#!/usr/bin/env python3
"""
Level-set distribution measurement for 3D Navier-Stokes DNS.

Computes:
1. μ(λ) = |{x : |u(x,t)| > λ}| / |Ω| for log-spaced λ values
2. Power-law tail fits: μ(λ) ~ A · λ^{-p}
3. De Giorgi tightness ratios: (Chebyshev bound) / A_k

Reuses the spectral NS solver from Strategy-001.
"""

import sys
import os
import json
import time
import traceback
import numpy as np
from numpy.fft import fftn, ifftn, fftfreq
from scipy import stats

# Add Strategy-001 code to path
STRATEGY1_CODE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', '..', '..', '..', 'strategy-001', 'explorations', 'exploration-002', 'code'
)
sys.path.insert(0, os.path.abspath(STRATEGY1_CODE))

from ns_solver import NavierStokesSolver

# Output paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRESS_FILE = os.path.join(BASE_DIR, "progress.txt")
RESULTS_FILE = os.path.join(BASE_DIR, "results.json")


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
    'RandomGauss': random_gaussian_ic,
    'ABC': abc_flow_ic,
}


# ============================================================
# Level-set distribution measurement
# ============================================================

def compute_mu_lambda(u_mag, n_lambdas=50, lambda_min_frac=0.1, lambda_max_frac=0.99):
    """
    Compute μ(λ) = |{x : |u(x)| > λ}| / |Ω| for log-spaced λ values.

    Args:
        u_mag: velocity magnitude field (N^3 array)
        n_lambdas: number of λ values
        lambda_min_frac: minimum λ as fraction of max(|u|)
        lambda_max_frac: maximum λ as fraction of max(|u|)

    Returns:
        lambdas: array of λ values
        mu_values: array of μ(λ) values (fractions of domain)
    """
    u_max = np.max(u_mag)
    if u_max < 1e-14:
        return np.zeros(n_lambdas), np.zeros(n_lambdas)

    lambda_min = lambda_min_frac * u_max
    lambda_max = lambda_max_frac * u_max

    lambdas = np.logspace(np.log10(lambda_min), np.log10(lambda_max), n_lambdas)
    N_total = u_mag.size

    mu_values = np.array([np.sum(u_mag > lam) / N_total for lam in lambdas])

    return lambdas, mu_values


def fit_power_law(lambdas, mu_values, mu_min=1e-4, mu_max=0.3):
    """
    Fit μ(λ) ~ A · λ^{-p} in the region where μ ∈ [mu_min, mu_max].

    Returns:
        p: power-law exponent
        A: prefactor
        p_stderr: standard error on p
        r_squared: R² of fit
        n_points: number of points used in fit
        lambda_range: (lambda_min, lambda_max) used in fit
    """
    # Select points in the valid range
    mask = (mu_values >= mu_min) & (mu_values <= mu_max) & (mu_values > 0) & (lambdas > 0)

    if np.sum(mask) < 5:
        # Relax bounds
        mask = (mu_values >= mu_min/10) & (mu_values <= min(mu_max*3, 0.9)) & (mu_values > 0) & (lambdas > 0)

    if np.sum(mask) < 3:
        return np.nan, np.nan, np.nan, np.nan, 0, (np.nan, np.nan)

    log_lam = np.log(lambdas[mask])
    log_mu = np.log(mu_values[mask])

    # Linear regression: log(μ) = log(A) - p * log(λ)
    slope, intercept, r_value, p_value, std_err = stats.linregress(log_lam, log_mu)

    p = -slope  # μ ~ λ^{-p} => log(μ) ~ -p * log(λ)
    A = np.exp(intercept)
    r_squared = r_value**2
    p_stderr = std_err

    lambda_range = (lambdas[mask][0], lambdas[mask][-1])

    return p, A, p_stderr, r_squared, int(np.sum(mask)), lambda_range


def compute_degiorgi_tightness(solver, ux_hat, uy_hat, uz_hat, K_max=10, time_snapshots=None):
    """
    Compute the De Giorgi level-set tightness ratios.

    For the truncated velocity v_k = [|u| - (1-2^{-k})]_+, compute:
    - A_k = |{v_{k-1} > 2^{-k}}| (the actual level-set measure)
    - Chebyshev bound: 2^{10k/3} · ||v_{k-1}||_{L^{10/3}}^{10/3}
    - Tightness ratio: (Chebyshev bound) / A_k

    If time_snapshots is provided, computes the parabolic L^{10/3} norm.
    Otherwise, uses the instantaneous L^{10/3}_x norm.

    Args:
        solver: NavierStokesSolver
        ux_hat, uy_hat, uz_hat: spectral velocity data (single snapshot)
        K_max: maximum k in the iteration
        time_snapshots: list of (t, ux_hat, uy_hat, uz_hat) for parabolic norm

    Returns:
        dict with A_k, chebyshev_bound, tightness_ratio arrays
    """
    N = solver.N
    vol = (2 * np.pi)**3
    dV = vol / N**3

    # Get velocity magnitude for single snapshot
    ux = solver.to_physical(ux_hat)
    uy = solver.to_physical(uy_hat)
    uz = solver.to_physical(uz_hat)
    u_mag = np.sqrt(ux**2 + uy**2 + uz**2)

    # Normalize by L^inf
    u_max = np.max(u_mag)
    if u_max < 1e-14:
        return None
    u_mag_norm = u_mag / u_max

    results = {
        'u_max': float(u_max),
        'k_values': [],
        'A_k': [],
        'chebyshev_bound_instant': [],
        'tightness_ratio_instant': [],
        'v_km1_L10_3': [],
    }

    if time_snapshots is not None:
        results['chebyshev_bound_parabolic'] = []
        results['tightness_ratio_parabolic'] = []
        results['v_km1_L10_3_parabolic'] = []

    for k in range(1, K_max + 1):
        # v_{k-1} = [|u_norm| - (1 - 2^{-(k-1)})]_+
        threshold_km1 = 1.0 - 2.0**(-(k-1))
        v_km1 = np.maximum(u_mag_norm - threshold_km1, 0.0)

        # A_k = |{v_{k-1} > 2^{-k}}| / |Ω|
        cutoff_k = 2.0**(-k)
        A_k_count = np.sum(v_km1 > cutoff_k)
        A_k = A_k_count / u_mag.size  # fraction of domain

        if A_k < 1e-30:
            # Level set is empty — stop
            results['k_values'].append(k)
            results['A_k'].append(0.0)
            results['chebyshev_bound_instant'].append(0.0)
            results['tightness_ratio_instant'].append(np.inf)
            results['v_km1_L10_3'].append(0.0)
            if time_snapshots is not None:
                results['chebyshev_bound_parabolic'].append(0.0)
                results['tightness_ratio_parabolic'].append(np.inf)
                results['v_km1_L10_3_parabolic'].append(0.0)
            continue

        # ||v_{k-1}||_{L^{10/3}_x}^{10/3} at fixed t
        # = (1/|Ω|) * int |v_{k-1}|^{10/3} dx  (volumetric average)
        # Actually: ||v_{k-1}||_{L^{10/3}}^{10/3} = int |v_{k-1}|^{10/3} dx
        v_km1_L10_3_pow = np.sum(v_km1**(10.0/3.0)) * dV  # integral, not average
        v_km1_L10_3 = v_km1_L10_3_pow**(3.0/10.0)

        # Chebyshev bound: |{v_{k-1} > 2^{-k}}| ≤ 2^{10k/3} · ||v_{k-1}||_{10/3}^{10/3}
        # But careful: A_k is in fraction of domain, bound is in absolute measure
        # A_k (absolute) = A_k_count * dV
        A_k_abs = A_k_count * dV

        cheb_bound_instant = (2.0**(10.0*k/3.0)) * v_km1_L10_3_pow
        tightness_instant = cheb_bound_instant / max(A_k_abs, 1e-30)

        results['k_values'].append(k)
        results['A_k'].append(float(A_k_abs))
        results['chebyshev_bound_instant'].append(float(cheb_bound_instant))
        results['tightness_ratio_instant'].append(float(tightness_instant))
        results['v_km1_L10_3'].append(float(v_km1_L10_3))

        # Parabolic L^{10/3} norm if time snapshots available
        if time_snapshots is not None:
            # Parabolic norm: (∫_0^T ∫ |v_{k-1}|^{10/3} dx dt)^{3/10}
            # We integrate over time using trapezoidal rule
            parabolic_integrands = []
            times = []
            for t_s, ux_hat_s, uy_hat_s, uz_hat_s in time_snapshots:
                ux_s = solver.to_physical(ux_hat_s)
                uy_s = solver.to_physical(uy_hat_s)
                uz_s = solver.to_physical(uz_hat_s)
                u_mag_s = np.sqrt(ux_s**2 + uy_s**2 + uz_s**2)
                u_mag_norm_s = u_mag_s / u_max  # same normalization
                v_km1_s = np.maximum(u_mag_norm_s - threshold_km1, 0.0)
                spatial_int = np.sum(v_km1_s**(10.0/3.0)) * dV
                parabolic_integrands.append(spatial_int)
                times.append(t_s)

            times = np.array(times)
            parabolic_integrands = np.array(parabolic_integrands)

            if len(times) > 1:
                parabolic_L10_3_pow = np.trapezoid(parabolic_integrands, times)
            else:
                parabolic_L10_3_pow = parabolic_integrands[0]

            parabolic_L10_3 = max(parabolic_L10_3_pow, 0.0)**(3.0/10.0)

            # Chebyshev bound with parabolic norm
            # For parabolic: need to think about what A_k means over time
            # The Vasseur proof uses: μ(level set over space-time)
            # For fair comparison: use A_k at the worst (peak) snapshot
            cheb_bound_parabolic = (2.0**(10.0*k/3.0)) * parabolic_L10_3_pow
            tightness_parabolic = cheb_bound_parabolic / max(A_k_abs, 1e-30)

            results['chebyshev_bound_parabolic'].append(float(cheb_bound_parabolic))
            results['tightness_ratio_parabolic'].append(float(tightness_parabolic))
            results['v_km1_L10_3_parabolic'].append(float(parabolic_L10_3))

    return results


# ============================================================
# Main runner
# ============================================================

def run_case(ic_name, Re, N=128, T_final=None, n_snapshots=20, K_max=10):
    """Run a single DNS case and measure level-set distributions."""
    nu = 1.0 / Re
    if T_final is None:
        # Choose T_final based on Re
        if Re <= 100:
            T_final = 2.0
        elif Re <= 500:
            T_final = 1.0
        elif Re <= 1600:
            T_final = 0.5
        else:
            T_final = 0.3

    log_progress(f"\n{'='*60}")
    log_progress(f"Case: IC={ic_name}, Re={Re}, N={N}, T_final={T_final}")
    log_progress(f"{'='*60}")

    solver = NavierStokesSolver(N, nu, cfl=0.4)
    snap_interval = T_final / n_snapshots

    # Initialize
    ux_hat, uy_hat, uz_hat = IC_FUNCS[ic_name](solver)

    # Check initial state
    ux = solver.to_physical(ux_hat)
    uy = solver.to_physical(uy_hat)
    uz = solver.to_physical(uz_hat)
    E0 = 0.5 * np.mean(ux**2 + uy**2 + uz**2)
    u_max_0 = np.max(np.sqrt(ux**2 + uy**2 + uz**2))
    log_progress(f"  Initial energy: {E0:.6f}, max|u|: {u_max_0:.6f}")

    # Run DNS
    t0 = time.time()
    _, _, _, snapshots = solver.run(ux_hat, uy_hat, uz_hat, T_final,
                                     snapshot_interval=snap_interval)
    dns_time = time.time() - t0
    log_progress(f"  DNS done in {dns_time:.1f}s, {len(snapshots)} snapshots")

    # Check final state
    ux_f = solver.to_physical(snapshots[-1][1])
    uy_f = solver.to_physical(snapshots[-1][2])
    uz_f = solver.to_physical(snapshots[-1][3])
    E_final = 0.5 * np.mean(ux_f**2 + uy_f**2 + uz_f**2)
    u_mag_final = np.sqrt(ux_f**2 + uy_f**2 + uz_f**2)
    u_max_final = np.max(u_mag_final)
    log_progress(f"  Final energy: {E_final:.6f} (decay: {E_final/max(E0,1e-30):.4f}), max|u|: {u_max_final:.6f}")

    # Find the snapshot with maximum enstrophy (most turbulent)
    max_enstrophy_idx = 0
    max_enstrophy = 0
    for i, (t_s, ux_h, uy_h, uz_h) in enumerate(snapshots):
        # Enstrophy ~ sum K^2 |u_hat|^2
        enstrophy = np.sum(solver.K2 * (np.abs(ux_h)**2 + np.abs(uy_h)**2 + np.abs(uz_h)**2)).real / solver.N**6
        if enstrophy > max_enstrophy:
            max_enstrophy = enstrophy
            max_enstrophy_idx = i
    log_progress(f"  Peak enstrophy at snapshot {max_enstrophy_idx} (t={snapshots[max_enstrophy_idx][0]:.3f})")

    # ============================================================
    # Measure μ(λ) at multiple time snapshots
    # ============================================================
    log_progress("  Computing μ(λ) curves...")

    # Select snapshots: initial, peak enstrophy, and 2 others spread out
    snap_indices = sorted(set([
        0,
        max_enstrophy_idx,
        len(snapshots) // 3,
        2 * len(snapshots) // 3,
        len(snapshots) - 1,
    ]))

    mu_results = {}
    for idx in snap_indices:
        t_s, ux_h, uy_h, uz_h = snapshots[idx]
        ux_s = solver.to_physical(ux_h)
        uy_s = solver.to_physical(uy_h)
        uz_s = solver.to_physical(uz_h)
        u_mag_s = np.sqrt(ux_s**2 + uy_s**2 + uz_s**2)

        lambdas, mu_values = compute_mu_lambda(u_mag_s, n_lambdas=50)
        p, A, p_stderr, r_sq, n_pts, lam_range = fit_power_law(lambdas, mu_values)

        mu_results[f"snap_{idx}_t{t_s:.3f}"] = {
            'snapshot_idx': idx,
            'time': float(t_s),
            'u_max': float(np.max(u_mag_s)),
            'lambdas': lambdas.tolist(),
            'mu_values': mu_values.tolist(),
            'power_law_exponent_p': float(p) if not np.isnan(p) else None,
            'power_law_prefactor_A': float(A) if not np.isnan(A) else None,
            'p_stderr': float(p_stderr) if not np.isnan(p_stderr) else None,
            'r_squared': float(r_sq) if not np.isnan(r_sq) else None,
            'n_fit_points': n_pts,
            'lambda_range': [float(lam_range[0]) if not np.isnan(lam_range[0]) else None,
                             float(lam_range[1]) if not np.isnan(lam_range[1]) else None],
            'chebyshev_exponent': 10.0/3.0,
            'excess_over_chebyshev': float(p - 10.0/3.0) if not np.isnan(p) else None,
        }

        log_progress(f"    snap {idx} (t={t_s:.3f}): p = {p:.4f} ± {p_stderr:.4f}, "
                     f"Δp = {p - 10.0/3.0:.4f}, R² = {r_sq:.4f}, n = {n_pts}")

    # ============================================================
    # De Giorgi tightness ratios at peak enstrophy snapshot
    # ============================================================
    log_progress("  Computing De Giorgi tightness ratios...")

    peak_t, peak_ux_h, peak_uy_h, peak_uz_h = snapshots[max_enstrophy_idx]
    dg_tightness = compute_degiorgi_tightness(
        solver, peak_ux_h, peak_uy_h, peak_uz_h,
        K_max=K_max,
        time_snapshots=snapshots
    )

    if dg_tightness is not None:
        for i, k in enumerate(dg_tightness['k_values']):
            A_k = dg_tightness['A_k'][i]
            tr_i = dg_tightness['tightness_ratio_instant'][i]
            log_progress(f"    k={k}: A_k={A_k:.2e}, Cheb_bound={dg_tightness['chebyshev_bound_instant'][i]:.2e}, "
                         f"tightness_instant={tr_i:.2f}")
            if 'tightness_ratio_parabolic' in dg_tightness:
                tr_p = dg_tightness['tightness_ratio_parabolic'][i]
                log_progress(f"           Cheb_bound_parabolic={dg_tightness['chebyshev_bound_parabolic'][i]:.2e}, "
                             f"tightness_parabolic={tr_p:.2f}")

    # ============================================================
    # Also measure the L^{10/3} distribution directly
    # ============================================================
    log_progress("  Computing L^{10/3} norm structure...")

    # At peak enstrophy: compute ||v_{k-1}||_{10/3}^{10/3} and compare
    # with what Chebyshev assumes
    peak_ux = solver.to_physical(peak_ux_h)
    peak_uy = solver.to_physical(peak_uy_h)
    peak_uz = solver.to_physical(peak_uz_h)
    peak_u_mag = np.sqrt(peak_ux**2 + peak_uy**2 + peak_uz**2)
    peak_u_max = np.max(peak_u_mag)
    peak_u_mag_norm = peak_u_mag / max(peak_u_max, 1e-30)

    # Lp norms for various p
    dV = (2*np.pi)**3 / N**3
    lp_norms = {}
    for p_val in [2.0, 3.0, 10.0/3.0, 4.0, 5.0, 6.0, 10.0]:
        lp_norm = (np.sum(peak_u_mag_norm**p_val) * dV)**(1.0/p_val)
        lp_norms[f"L{p_val:.2f}"] = float(lp_norm)
    log_progress(f"    Lp norms of |u|/max|u|: {lp_norms}")

    # Assemble result
    case_result = {
        'IC': ic_name,
        'Re': Re,
        'N': N,
        'T_final': T_final,
        'n_snapshots': len(snapshots),
        'E_initial': float(E0),
        'E_final': float(E_final),
        'u_max_initial': float(u_max_0),
        'u_max_final': float(u_max_final),
        'peak_enstrophy_idx': max_enstrophy_idx,
        'peak_enstrophy_time': float(snapshots[max_enstrophy_idx][0]),
        'dns_time_s': dns_time,
        'mu_lambda_results': mu_results,
        'degiorgi_tightness': dg_tightness,
        'lp_norms_normalized': lp_norms,
    }

    return case_result


def main():
    log_progress("=" * 70)
    log_progress("Level-Set Distribution vs Chebyshev Bound — Full Measurement")
    log_progress("=" * 70)

    all_results = []

    # Cases from GOAL.md
    cases = [
        ('TaylorGreen', 100, 128),
        ('TaylorGreen', 500, 128),
        ('TaylorGreen', 1600, 128),
        ('RandomGauss', 100, 128),
        ('RandomGauss', 500, 128),
        ('ABC', 100, 128),
        ('ABC', 500, 128),
    ]

    for ic_name, Re, N in cases:
        try:
            result = run_case(ic_name, Re, N)
            all_results.append(result)

            # Save incrementally
            with open(RESULTS_FILE, 'w') as f:
                json.dump(all_results, f, indent=2, default=str)

        except Exception as e:
            log_progress(f"  FAILED: {ic_name} Re={Re}: {e}")
            traceback.print_exc()
            all_results.append({
                'IC': ic_name, 'Re': Re, 'N': N,
                'error': str(e),
            })

    # ============================================================
    # Summary statistics
    # ============================================================
    log_progress("\n" + "=" * 70)
    log_progress("SUMMARY TABLE: Power-law exponents p")
    log_progress("=" * 70)
    log_progress(f"{'IC':<15} {'Re':>5} {'Snapshot':>12} {'p':>8} {'±':>1} {'stderr':>6} "
                 f"{'p-10/3':>8} {'R²':>6} {'n':>4}")
    log_progress("-" * 75)

    all_p_values = []
    all_excess = []

    for r in all_results:
        if 'error' in r:
            continue
        ic = r['IC']
        Re = r['Re']
        for snap_key, snap_data in r['mu_lambda_results'].items():
            p = snap_data.get('power_law_exponent_p')
            if p is not None:
                stderr = snap_data.get('p_stderr', 0)
                excess = snap_data.get('excess_over_chebyshev', 0)
                r2 = snap_data.get('r_squared', 0)
                n_pts = snap_data.get('n_fit_points', 0)
                log_progress(f"{ic:<15} {Re:>5} {snap_key:>12} {p:>8.4f} ± {stderr:>6.4f} "
                             f"{excess:>+8.4f} {r2:>6.3f} {n_pts:>4}")
                all_p_values.append(p)
                all_excess.append(excess)

    if all_p_values:
        log_progress(f"\nOverall: mean(p) = {np.mean(all_p_values):.4f} ± {np.std(all_p_values):.4f}")
        log_progress(f"         mean(p - 10/3) = {np.mean(all_excess):.4f} ± {np.std(all_excess):.4f}")
        log_progress(f"         min(p) = {np.min(all_p_values):.4f}, max(p) = {np.max(all_p_values):.4f}")
        log_progress(f"         Chebyshev exponent = {10/3:.4f}")
        if np.mean(all_excess) > 0:
            log_progress(f"  ==> NS solutions show FASTER tail decay than Chebyshev predicts!")
        else:
            log_progress(f"  ==> NS solutions match or are slower than Chebyshev prediction")

    # Tightness ratio summary
    log_progress("\n" + "=" * 70)
    log_progress("SUMMARY: De Giorgi Tightness Ratios (Chebyshev bound / actual A_k)")
    log_progress("=" * 70)

    for r in all_results:
        if 'error' in r or r.get('degiorgi_tightness') is None:
            continue
        dg = r['degiorgi_tightness']
        log_progress(f"\n{r['IC']} Re={r['Re']}:")
        for i, k in enumerate(dg['k_values']):
            A_k = dg['A_k'][i]
            if A_k > 0:
                tr_i = dg['tightness_ratio_instant'][i]
                log_progress(f"  k={k}: A_k={A_k:.4e}, tightness={tr_i:.2f}x")

    # Final save
    with open(RESULTS_FILE, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)

    log_progress("\n" + "=" * 70)
    log_progress("ALL DONE")
    log_progress("=" * 70)


if __name__ == '__main__':
    main()
