#!/usr/bin/env python3
"""
Post-hoc analysis: deeper power-law fitting + De Giorgi tightness ratios.

This script:
1. Loads results from the main run
2. Does additional statistical analysis on power-law fits
3. Tests whether tail decay is power-law vs exponential vs Gaussian
4. Computes De Giorgi tightness ratios (fixed np.trapz -> np.trapezoid)
5. Runs smaller N=64 cases to get quick tightness ratio data

Can be run after the main computation finishes.
"""

import sys
import os
import json
import time
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit

CODE_DIR = os.path.dirname(os.path.abspath(__file__))
STRATEGY1_CODE = os.path.join(CODE_DIR, '..', '..', '..', '..', 'strategy-001', 'explorations', 'exploration-002', 'code')
sys.path.insert(0, os.path.abspath(STRATEGY1_CODE))

from ns_solver import NavierStokesSolver

BASE_DIR = os.path.dirname(CODE_DIR)
RESULTS_FILE = os.path.join(BASE_DIR, "results.json")
ANALYSIS_FILE = os.path.join(BASE_DIR, "analysis_results.json")
PROGRESS_FILE = os.path.join(BASE_DIR, "progress_analysis.txt")


def log_progress(msg):
    with open(PROGRESS_FILE, "a") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    print(msg, flush=True)


# ============================================================
# Initial Conditions (same as main script)
# ============================================================

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
    K_mag_safe = np.where(solver.K_mag == 0, 1, solver.K_mag)
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


def abc_flow_ic(solver, A=1.0, B=1.0, C=1.0):
    X, Y, Z = solver.X, solver.Y, solver.Z
    ux = B * np.sin(Y) + C * np.cos(Z)
    uy = C * np.sin(Z) + A * np.cos(X)
    uz = A * np.sin(X) + B * np.cos(Y)
    ux_hat = solver.to_spectral(ux); uy_hat = solver.to_spectral(uy); uz_hat = solver.to_spectral(uz)
    ux_hat, uy_hat, uz_hat = solver.project(ux_hat, uy_hat, uz_hat)
    ux_hat = solver.dealias(ux_hat); uy_hat = solver.dealias(uy_hat); uz_hat = solver.dealias(uz_hat)
    ux = solver.to_physical(ux_hat); uy = solver.to_physical(uy_hat); uz = solver.to_physical(uz_hat)
    E = 0.5 * np.mean(ux**2 + uy**2 + uz**2)
    if E > 0:
        scale = 1.0 / np.sqrt(2 * E)
        ux_hat *= scale; uy_hat *= scale; uz_hat *= scale
    return ux_hat, uy_hat, uz_hat


IC_FUNCS = {
    'TaylorGreen': taylor_green_ic,
    'RandomGauss': random_gaussian_ic,
    'ABC': abc_flow_ic,
}


# ============================================================
# Better fitting: test power-law vs exponential vs stretched-exp
# ============================================================

def power_law_model(log_lam, log_A, p):
    """log(μ) = log_A - p * log(λ)"""
    return log_A - p * log_lam

def exponential_model(lam, A, alpha):
    """μ = A * exp(-alpha * λ)"""
    return A * np.exp(-alpha * lam)

def stretched_exp_model(lam, A, alpha, beta):
    """μ = A * exp(-alpha * λ^beta)"""
    return A * np.exp(-alpha * lam**beta)


def fit_all_models(lambdas, mu_values, mu_min=1e-4, mu_max=0.3):
    """Fit multiple models and compare using AIC/BIC."""
    mask = (mu_values >= mu_min) & (mu_values <= mu_max) & (mu_values > 0) & (lambdas > 0)
    if np.sum(mask) < 5:
        mask = (mu_values >= mu_min/10) & (mu_values <= min(mu_max*3, 0.9)) & (mu_values > 0) & (lambdas > 0)
    if np.sum(mask) < 5:
        return {}

    lam_fit = lambdas[mask]
    mu_fit = mu_values[mask]
    n = len(lam_fit)

    results = {}

    # 1. Power law: μ ~ A * λ^{-p}
    try:
        log_lam = np.log(lam_fit)
        log_mu = np.log(mu_fit)
        slope, intercept, r_value, p_value, std_err = stats.linregress(log_lam, log_mu)
        p_pl = -slope
        A_pl = np.exp(intercept)
        mu_pred = A_pl * lam_fit**(-p_pl)
        rss_pl = np.sum((mu_fit - mu_pred)**2)
        aic_pl = n * np.log(max(rss_pl/n, 1e-100)) + 2*2  # 2 params
        results['power_law'] = {
            'p': float(p_pl), 'A': float(A_pl), 'r2': float(r_value**2),
            'p_stderr': float(std_err), 'rss': float(rss_pl), 'aic': float(aic_pl),
            'n_points': n,
        }
    except Exception as e:
        results['power_law'] = {'error': str(e)}

    # 2. Exponential: μ ~ A * exp(-α * λ)
    try:
        popt, pcov = curve_fit(exponential_model, lam_fit, mu_fit,
                               p0=[1.0, 1.0], maxfev=5000,
                               bounds=([0, 0], [np.inf, np.inf]))
        mu_pred = exponential_model(lam_fit, *popt)
        rss_exp = np.sum((mu_fit - mu_pred)**2)
        aic_exp = n * np.log(max(rss_exp/n, 1e-100)) + 2*2
        results['exponential'] = {
            'A': float(popt[0]), 'alpha': float(popt[1]),
            'rss': float(rss_exp), 'aic': float(aic_exp),
            'n_points': n,
        }
    except Exception as e:
        results['exponential'] = {'error': str(e)}

    # 3. Stretched exponential: μ ~ A * exp(-α * λ^β)
    try:
        popt, pcov = curve_fit(stretched_exp_model, lam_fit, mu_fit,
                               p0=[1.0, 1.0, 2.0], maxfev=10000,
                               bounds=([0, 0, 0.1], [np.inf, np.inf, 20]))
        mu_pred = stretched_exp_model(lam_fit, *popt)
        rss_se = np.sum((mu_fit - mu_pred)**2)
        aic_se = n * np.log(max(rss_se/n, 1e-100)) + 2*3  # 3 params
        results['stretched_exp'] = {
            'A': float(popt[0]), 'alpha': float(popt[1]), 'beta': float(popt[2]),
            'rss': float(rss_se), 'aic': float(aic_se),
            'n_points': n,
        }
    except Exception as e:
        results['stretched_exp'] = {'error': str(e)}

    # Identify best model by AIC
    valid_models = {k: v for k, v in results.items() if 'aic' in v}
    if valid_models:
        best = min(valid_models.keys(), key=lambda k: valid_models[k]['aic'])
        results['best_model'] = best

    return results


# ============================================================
# De Giorgi tightness ratios (fixed, no parabolic norm to avoid np.trapz)
# ============================================================

def compute_tightness_ratios(solver, snapshots, K_max=10):
    """
    For each snapshot, compute tightness ratios at each De Giorgi level.

    Returns dict with per-snapshot tightness data.
    """
    vol = (2 * np.pi)**3
    dV = vol / solver.N**3

    # Find max |u| across all snapshots for normalization
    u_max_global = 0.0
    for t_s, ux_h, uy_h, uz_h in snapshots:
        ux = solver.to_physical(ux_h)
        uy = solver.to_physical(uy_h)
        uz = solver.to_physical(uz_h)
        u_mag = np.sqrt(ux**2 + uy**2 + uz**2)
        u_max_global = max(u_max_global, np.max(u_mag))

    if u_max_global < 1e-14:
        return None

    # Pick the snapshot with highest max|u| (most likely to show tightness variation)
    best_snap_idx = 0
    best_u_max = 0
    for i, (t_s, ux_h, uy_h, uz_h) in enumerate(snapshots):
        ux = solver.to_physical(ux_h)
        uy = solver.to_physical(uy_h)
        uz = solver.to_physical(uz_h)
        u_mag = np.sqrt(ux**2 + uy**2 + uz**2)
        if np.max(u_mag) > best_u_max:
            best_u_max = np.max(u_mag)
            best_snap_idx = i

    # Compute tightness at multiple snapshots
    snap_indices = sorted(set([0, best_snap_idx, len(snapshots)//2, len(snapshots)-1]))

    all_snap_data = {}

    for si in snap_indices:
        t_s, ux_h, uy_h, uz_h = snapshots[si]
        ux = solver.to_physical(ux_h)
        uy = solver.to_physical(uy_h)
        uz = solver.to_physical(uz_h)
        u_mag = np.sqrt(ux**2 + uy**2 + uz**2)
        u_mag_norm = u_mag / u_max_global

        snap_data = {
            'time': float(t_s),
            'u_max': float(np.max(u_mag)),
            'k_values': [],
            'A_k_abs': [],
            'A_k_frac': [],
            'chebyshev_bound': [],
            'tightness_ratio': [],
            'v_km1_L10_3_pow': [],
        }

        for k in range(1, K_max + 1):
            threshold_km1 = 1.0 - 2.0**(-(k-1))
            v_km1 = np.maximum(u_mag_norm - threshold_km1, 0.0)
            cutoff_k = 2.0**(-k)

            # A_k = measure of {v_{k-1} > 2^{-k}}
            A_k_count = np.sum(v_km1 > cutoff_k)
            A_k_abs = A_k_count * dV
            A_k_frac = A_k_count / u_mag.size

            # ||v_{k-1}||_{L^{10/3}}^{10/3} = integral |v_{k-1}|^{10/3} dx
            v_km1_L10_3_pow = np.sum(v_km1**(10.0/3.0)) * dV

            # Chebyshev bound: |{v_{k-1} > 2^{-k}}| ≤ (2^k)^{10/3} · ||v_{k-1}||_{10/3}^{10/3}
            # = 2^{10k/3} · ||v_{k-1}||_{10/3}^{10/3}
            cheb_bound = (2.0**(10.0*k/3.0)) * v_km1_L10_3_pow

            # Tightness
            tightness = cheb_bound / max(A_k_abs, 1e-30) if A_k_abs > 0 else float('inf')

            snap_data['k_values'].append(k)
            snap_data['A_k_abs'].append(float(A_k_abs))
            snap_data['A_k_frac'].append(float(A_k_frac))
            snap_data['chebyshev_bound'].append(float(cheb_bound))
            snap_data['tightness_ratio'].append(float(tightness))
            snap_data['v_km1_L10_3_pow'].append(float(v_km1_L10_3_pow))

        all_snap_data[f"snap_{si}"] = snap_data

    # Also compute the PARABOLIC tightness (integrating over all snapshots)
    parabolic_data = {
        'k_values': [],
        'A_k_max': [],  # max over snapshots
        'v_km1_parabolic_L10_3_pow': [],  # time integral of spatial L^{10/3}
        'cheb_bound_parabolic': [],
        'tightness_parabolic': [],
    }

    for k in range(1, K_max + 1):
        threshold_km1 = 1.0 - 2.0**(-(k-1))
        cutoff_k = 2.0**(-k)

        spatial_integrals = []
        A_k_vals = []
        times = []

        for t_s, ux_h, uy_h, uz_h in snapshots:
            ux = solver.to_physical(ux_h)
            uy = solver.to_physical(uy_h)
            uz = solver.to_physical(uz_h)
            u_mag = np.sqrt(ux**2 + uy**2 + uz**2)
            u_mag_norm = u_mag / u_max_global

            v_km1 = np.maximum(u_mag_norm - threshold_km1, 0.0)
            spatial_int = np.sum(v_km1**(10.0/3.0)) * dV
            A_k_abs = np.sum(v_km1 > cutoff_k) * dV

            spatial_integrals.append(spatial_int)
            A_k_vals.append(A_k_abs)
            times.append(t_s)

        times = np.array(times)
        spatial_integrals = np.array(spatial_integrals)
        A_k_max = max(A_k_vals)

        if len(times) > 1:
            parabolic_L10_3_pow = np.trapezoid(spatial_integrals, times)
        else:
            parabolic_L10_3_pow = spatial_integrals[0]

        cheb_bound_para = (2.0**(10.0*k/3.0)) * parabolic_L10_3_pow
        tightness_para = cheb_bound_para / max(A_k_max, 1e-30) if A_k_max > 0 else float('inf')

        parabolic_data['k_values'].append(k)
        parabolic_data['A_k_max'].append(float(A_k_max))
        parabolic_data['v_km1_parabolic_L10_3_pow'].append(float(parabolic_L10_3_pow))
        parabolic_data['cheb_bound_parabolic'].append(float(cheb_bound_para))
        parabolic_data['tightness_parabolic'].append(float(tightness_para))

    return {
        'u_max_global': float(u_max_global),
        'per_snapshot': all_snap_data,
        'parabolic': parabolic_data,
    }


def main():
    log_progress("=" * 70)
    log_progress("Post-hoc Analysis: Model Comparison + De Giorgi Tightness")
    log_progress("=" * 70)

    # ============================================================
    # Part 1: Deeper analysis of existing μ(λ) data
    # ============================================================
    log_progress("\nPart 1: Analyzing μ(λ) data from main run...")

    main_results = None
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE) as f:
            main_results = json.load(f)
        log_progress(f"  Loaded {len(main_results)} cases from results.json")

    model_comparison_results = []
    if main_results:
        for case in main_results:
            if 'error' in case:
                continue
            ic = case['IC']
            Re = case['Re']
            for snap_key, snap_data in case.get('mu_lambda_results', {}).items():
                lambdas = np.array(snap_data['lambdas'])
                mu_values = np.array(snap_data['mu_values'])
                if len(lambdas) == 0:
                    continue

                models = fit_all_models(lambdas, mu_values)
                models['IC'] = ic
                models['Re'] = Re
                models['snapshot'] = snap_key
                model_comparison_results.append(models)

                best = models.get('best_model', 'unknown')
                log_progress(f"  {ic} Re={Re} {snap_key}: best={best}")
                for model_name in ['power_law', 'exponential', 'stretched_exp']:
                    if model_name in models and 'error' not in models[model_name]:
                        m = models[model_name]
                        aic_str = f"AIC={m['aic']:.1f}"
                        if model_name == 'power_law':
                            log_progress(f"    {model_name}: p={m['p']:.3f}±{m['p_stderr']:.3f}, {aic_str}")
                        elif model_name == 'exponential':
                            log_progress(f"    {model_name}: α={m['alpha']:.3f}, {aic_str}")
                        elif model_name == 'stretched_exp':
                            log_progress(f"    {model_name}: α={m['alpha']:.3f}, β={m['beta']:.3f}, {aic_str}")

    # ============================================================
    # Part 2: Fresh De Giorgi tightness computations at N=64 (fast)
    # ============================================================
    log_progress("\n" + "=" * 70)
    log_progress("Part 2: De Giorgi Tightness Ratios (N=64, fast)")
    log_progress("=" * 70)

    tightness_results = []

    cases = [
        ('TaylorGreen', 100, 64),
        ('TaylorGreen', 500, 64),
        ('TaylorGreen', 1600, 64),
        ('RandomGauss', 100, 64),
        ('RandomGauss', 500, 64),
        ('ABC', 100, 64),
        ('ABC', 500, 64),
    ]

    for ic_name, Re, N in cases:
        nu = 1.0 / Re
        if Re <= 100:
            T_final = 2.0
        elif Re <= 500:
            T_final = 1.0
        elif Re <= 1600:
            T_final = 0.5
        else:
            T_final = 0.3

        log_progress(f"\n  Case: {ic_name} Re={Re} N={N} T={T_final}")

        try:
            solver = NavierStokesSolver(N, nu, cfl=0.4)
            snap_interval = T_final / 20

            ux_hat, uy_hat, uz_hat = IC_FUNCS[ic_name](solver)

            t0 = time.time()
            _, _, _, snapshots = solver.run(ux_hat, uy_hat, uz_hat, T_final,
                                             snapshot_interval=snap_interval)
            dns_time = time.time() - t0
            log_progress(f"    DNS done in {dns_time:.1f}s, {len(snapshots)} snapshots")

            t0 = time.time()
            tightness = compute_tightness_ratios(solver, snapshots, K_max=10)
            tr_time = time.time() - t0
            log_progress(f"    Tightness done in {tr_time:.1f}s")

            if tightness is not None:
                tightness['IC'] = ic_name
                tightness['Re'] = Re
                tightness['N'] = N
                tightness['T_final'] = T_final

                # Print instantaneous tightness at first snapshot
                for snap_key, sd in tightness['per_snapshot'].items():
                    log_progress(f"    {snap_key} (t={sd['time']:.3f}):")
                    for i, k in enumerate(sd['k_values']):
                        if sd['A_k_abs'][i] > 0:
                            log_progress(f"      k={k}: A_k={sd['A_k_abs'][i]:.4e}, "
                                         f"Cheb={sd['chebyshev_bound'][i]:.4e}, "
                                         f"ratio={sd['tightness_ratio'][i]:.2f}")
                        else:
                            log_progress(f"      k={k}: A_k=0 (level set empty)")
                            break

                # Print parabolic tightness
                log_progress(f"    Parabolic tightness:")
                para = tightness['parabolic']
                for i, k in enumerate(para['k_values']):
                    if para['A_k_max'][i] > 0:
                        log_progress(f"      k={k}: A_k_max={para['A_k_max'][i]:.4e}, "
                                     f"Cheb_para={para['cheb_bound_parabolic'][i]:.4e}, "
                                     f"ratio={para['tightness_parabolic'][i]:.2f}")
                    else:
                        log_progress(f"      k={k}: A_k=0 (empty)")
                        break

                tightness_results.append(tightness)

        except Exception as e:
            log_progress(f"    FAILED: {e}")
            import traceback
            traceback.print_exc()

    # ============================================================
    # Part 3: Summary analysis
    # ============================================================
    log_progress("\n" + "=" * 70)
    log_progress("SUMMARY ANALYSIS")
    log_progress("=" * 70)

    # Tightness ratio trends
    log_progress("\nTightness Ratio Growth with k:")
    log_progress(f"{'IC':<15} {'Re':>5} {'k=1':>8} {'k=2':>8} {'k=3':>8} {'k=4':>8} {'k=5':>8} {'k=6':>8}")
    log_progress("-" * 70)

    for tr in tightness_results:
        row = f"{tr['IC']:<15} {tr['Re']:>5}"
        # Use the snapshot with max u (usually snap_0 for best_snap)
        # Use parabolic for comparison with Vasseur's proof
        para = tr['parabolic']
        for k_idx in range(min(6, len(para['tightness_parabolic']))):
            t = para['tightness_parabolic'][k_idx]
            if t < 1e10:
                row += f" {t:>8.1f}"
            else:
                row += f" {'inf':>8}"
        log_progress(row)

    # Does tightness ratio GROW with k?
    log_progress("\nKey question: Does tightness ratio grow exponentially with k?")
    log_progress("If ratio ~ C^k with C >> 1, then Chebyshev has exponential slack.")
    log_progress("If ratio ~ constant, Chebyshev is tight.")

    for tr in tightness_results:
        para = tr['parabolic']
        valid = [(k, t) for k, t in zip(para['k_values'], para['tightness_parabolic'])
                 if 0 < t < 1e10 and t > 1]
        if len(valid) >= 3:
            ks = np.array([v[0] for v in valid], dtype=float)
            log_t = np.array([np.log(v[1]) for v in valid])
            slope, intercept, r, p, se = stats.linregress(ks, log_t)
            growth_factor = np.exp(slope)
            log_progress(f"  {tr['IC']} Re={tr['Re']}: "
                         f"ratio ~ {growth_factor:.2f}^k, "
                         f"R²={r**2:.3f}")

    # Save all analysis
    analysis_output = {
        'model_comparison': model_comparison_results,
        'tightness_results': tightness_results,
    }

    # Make serializable
    def make_serializable(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, dict):
            return {k: make_serializable(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [make_serializable(v) for v in obj]
        return obj

    with open(ANALYSIS_FILE, 'w') as f:
        json.dump(make_serializable(analysis_output), f, indent=2)

    log_progress(f"\nAnalysis saved to {ANALYSIS_FILE}")
    log_progress("ALL DONE")


if __name__ == '__main__':
    main()
