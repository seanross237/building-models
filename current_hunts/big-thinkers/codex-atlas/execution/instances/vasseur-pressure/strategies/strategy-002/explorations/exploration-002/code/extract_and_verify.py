#!/usr/bin/env python3
"""
Extract all results, recompute μ(λ) from scratch at N=64 for verification,
and produce the clean final results.
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
FINAL_FILE = os.path.join(BASE_DIR, "final_results.json")


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


def compute_mu_lambda(u_mag, n_lambdas=50, lambda_min_frac=0.1, lambda_max_frac=0.99):
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
    mask = (mu_values >= mu_min) & (mu_values <= mu_max) & (mu_values > 0) & (lambdas > 0)
    if np.sum(mask) < 5:
        mask = (mu_values >= mu_min/10) & (mu_values <= min(mu_max*3, 0.9)) & (mu_values > 0) & (lambdas > 0)
    if np.sum(mask) < 3:
        return np.nan, np.nan, np.nan, np.nan, 0, (np.nan, np.nan)

    log_lam = np.log(lambdas[mask])
    log_mu = np.log(mu_values[mask])
    slope, intercept, r_value, p_value, std_err = stats.linregress(log_lam, log_mu)
    p = -slope
    A = np.exp(intercept)
    r_squared = r_value**2
    lambda_range = (lambdas[mask][0], lambdas[mask][-1])
    return p, A, std_err, r_squared, int(np.sum(mask)), lambda_range


def compute_tightness_instant(solver, ux_hat, uy_hat, uz_hat, u_max_global, K_max=10):
    """Compute instantaneous tightness ratios (correct Chebyshev comparison)."""
    vol = (2 * np.pi)**3
    dV = vol / solver.N**3

    ux = solver.to_physical(ux_hat)
    uy = solver.to_physical(uy_hat)
    uz = solver.to_physical(uz_hat)
    u_mag = np.sqrt(ux**2 + uy**2 + uz**2)
    u_mag_norm = u_mag / u_max_global

    results = []
    for k in range(1, K_max + 1):
        threshold_km1 = 1.0 - 2.0**(-(k-1))
        v_km1 = np.maximum(u_mag_norm - threshold_km1, 0.0)
        cutoff_k = 2.0**(-k)

        A_k_abs = np.sum(v_km1 > cutoff_k) * dV
        v_km1_L10_3_pow = np.sum(v_km1**(10.0/3.0)) * dV
        cheb_bound = (2.0**(10.0*k/3.0)) * v_km1_L10_3_pow
        tightness = cheb_bound / max(A_k_abs, 1e-30) if A_k_abs > 0 else float('inf')

        results.append({
            'k': k,
            'A_k': float(A_k_abs),
            'cheb_bound': float(cheb_bound),
            'tightness': float(tightness),
            'v_km1_L10_3_10_3': float(v_km1_L10_3_pow),
        })

        if A_k_abs == 0:
            break

    return results


def main():
    print("=" * 70)
    print("Final extraction and verification (N=64)")
    print("=" * 70)

    all_results = []

    cases = [
        ('TaylorGreen', 100, 64, 2.0),
        ('TaylorGreen', 500, 64, 1.0),
        ('TaylorGreen', 1600, 64, 0.5),
        ('RandomGauss', 100, 64, 2.0),
        ('RandomGauss', 500, 64, 1.0),
        ('ABC', 100, 64, 2.0),
        ('ABC', 500, 64, 1.0),
    ]

    for ic_name, Re, N, T_final in cases:
        nu = 1.0 / Re
        print(f"\n--- {ic_name} Re={Re} N={N} T={T_final} ---")

        solver = NavierStokesSolver(N, nu, cfl=0.4)
        snap_interval = T_final / 20
        ux_hat, uy_hat, uz_hat = IC_FUNCS[ic_name](solver)

        t0 = time.time()
        _, _, _, snapshots = solver.run(ux_hat, uy_hat, uz_hat, T_final,
                                         snapshot_interval=snap_interval)
        dns_time = time.time() - t0
        print(f"  DNS: {dns_time:.1f}s, {len(snapshots)} snaps")

        # Find max |u| across all snapshots
        u_max_global = 0
        for t_s, ux_h, uy_h, uz_h in snapshots:
            ux = solver.to_physical(ux_h)
            uy = solver.to_physical(uy_h)
            uz = solver.to_physical(uz_h)
            u_max_global = max(u_max_global, np.max(np.sqrt(ux**2 + uy**2 + uz**2)))

        # Find peak enstrophy
        max_enst_idx = 0
        max_enst = 0
        for i, (t_s, ux_h, uy_h, uz_h) in enumerate(snapshots):
            enst = np.sum(solver.K2 * (np.abs(ux_h)**2 + np.abs(uy_h)**2 + np.abs(uz_h)**2)).real / N**6
            if enst > max_enst:
                max_enst = enst
                max_enst_idx = i

        # Compute μ(λ) at multiple snapshots
        snap_indices = sorted(set([0, max_enst_idx, len(snapshots)//2, len(snapshots)-1]))
        mu_data = []

        for idx in snap_indices:
            t_s, ux_h, uy_h, uz_h = snapshots[idx]
            ux = solver.to_physical(ux_h)
            uy = solver.to_physical(uy_h)
            uz = solver.to_physical(uz_h)
            u_mag = np.sqrt(ux**2 + uy**2 + uz**2)

            lambdas, mu_values = compute_mu_lambda(u_mag)
            p, A, p_stderr, r_sq, n_pts, lam_range = fit_power_law(lambdas, mu_values)

            # Also fit with wider mu range for comparison
            p2, A2, p_stderr2, r_sq2, n_pts2, lam_range2 = fit_power_law(
                lambdas, mu_values, mu_min=1e-3, mu_max=0.5)

            mu_entry = {
                'snap_idx': idx,
                'time': float(t_s),
                'u_max': float(np.max(u_mag)),
                'p': float(p) if not np.isnan(p) else None,
                'p_stderr': float(p_stderr) if not np.isnan(p_stderr) else None,
                'r_squared': float(r_sq) if not np.isnan(r_sq) else None,
                'n_fit_points': n_pts,
                'excess_over_chebyshev': float(p - 10.0/3.0) if not np.isnan(p) else None,
                'p_wider': float(p2) if not np.isnan(p2) else None,
                'r_sq_wider': float(r_sq2) if not np.isnan(r_sq2) else None,
                'lambdas': lambdas.tolist(),
                'mu_values': mu_values.tolist(),
            }
            mu_data.append(mu_entry)

            print(f"  snap {idx} (t={t_s:.3f}): p={p:.3f}±{p_stderr:.3f}, "
                  f"Δp={p-10.0/3.0:+.3f}, R²={r_sq:.3f}, n={n_pts}")

        # Compute tightness at peak enstrophy
        t_p, ux_p, uy_p, uz_p = snapshots[max_enst_idx]
        tightness = compute_tightness_instant(solver, ux_p, uy_p, uz_p, u_max_global)

        print(f"  Tightness at peak enstrophy (t={t_p:.3f}):")
        for tr in tightness:
            if tr['tightness'] < 1e10:
                print(f"    k={tr['k']}: A_k={tr['A_k']:.4e}, ratio={tr['tightness']:.2f}")
            else:
                print(f"    k={tr['k']}: A_k=0 (empty)")

        # Also compute tightness at initial time
        tightness_t0 = compute_tightness_instant(solver, snapshots[0][1], snapshots[0][2], snapshots[0][3], u_max_global)

        all_results.append({
            'IC': ic_name,
            'Re': Re,
            'N': N,
            'T_final': T_final,
            'u_max_global': float(u_max_global),
            'mu_lambda': mu_data,
            'tightness_peak': tightness,
            'tightness_t0': tightness_t0,
            'peak_enst_idx': max_enst_idx,
            'dns_time_s': dns_time,
        })

    # Save
    with open(FINAL_FILE, 'w') as f:
        json.dump(all_results, f, indent=2)

    # ============================================================
    # Grand Summary
    # ============================================================
    print("\n" + "=" * 70)
    print("GRAND SUMMARY")
    print("=" * 70)

    print("\n--- μ(λ) Power-law exponents (all snapshots) ---")
    print(f"{'IC':15s} {'Re':>5} {'t':>6} {'p':>8} {'±':>1} {'se':>6} {'p-10/3':>8} {'R²':>6} {'n':>4}")
    print("-" * 65)

    all_p = []
    all_excess = []
    for r in all_results:
        for m in r['mu_lambda']:
            p = m.get('p')
            if p is not None:
                se = m.get('p_stderr', 0)
                ex = m.get('excess_over_chebyshev', 0)
                r2 = m.get('r_squared', 0)
                n = m.get('n_fit_points', 0)
                print(f"{r['IC']:15s} {r['Re']:>5} {m['time']:>6.3f} {p:>8.3f} ± {se:>6.3f} "
                      f"{ex:>+8.3f} {r2:>6.3f} {n:>4}")
                all_p.append(p)
                all_excess.append(ex)

    print(f"\nOverall statistics:")
    print(f"  mean(p) = {np.mean(all_p):.3f} ± {np.std(all_p):.3f}")
    print(f"  median(p) = {np.median(all_p):.3f}")
    print(f"  min(p) = {np.min(all_p):.3f}, max(p) = {np.max(all_p):.3f}")
    print(f"  Chebyshev exponent = {10/3:.4f}")
    print(f"  Cases with p > 10/3: {sum(1 for p in all_p if p > 10/3)}/{len(all_p)}")
    print(f"  Cases with p < 10/3: {sum(1 for p in all_p if p < 10/3)}/{len(all_p)}")

    # Breakdown by IC
    for ic in ['TaylorGreen', 'RandomGauss', 'ABC']:
        ic_p = [p for p, r in zip(all_p, [m for r2 in all_results for m in r2['mu_lambda'] if m.get('p') is not None])
                if any(r2['IC'] == ic for r2 in all_results)]

    # Better breakdown
    print("\n--- Breakdown by IC type ---")
    for ic in ['TaylorGreen', 'RandomGauss', 'ABC']:
        ic_ps = []
        for r in all_results:
            if r['IC'] == ic:
                for m in r['mu_lambda']:
                    if m.get('p') is not None:
                        ic_ps.append(m['p'])
        if ic_ps:
            print(f"  {ic}: mean(p) = {np.mean(ic_ps):.3f} ± {np.std(ic_ps):.3f}, "
                  f"range [{np.min(ic_ps):.3f}, {np.max(ic_ps):.3f}]")

    print("\n--- Tightness Ratios at t=0 (initial condition) ---")
    print(f"{'IC':15s} {'Re':>5} {'k=1':>8} {'k=2':>8} {'k=3':>8} {'k=4':>8} {'k=5':>8} {'k=6':>8}")
    print("-" * 70)
    for r in all_results:
        row = f"{r['IC']:15s} {r['Re']:>5}"
        for tr in r['tightness_t0'][:6]:
            if tr['tightness'] < 1e6:
                row += f" {tr['tightness']:>8.2f}"
            else:
                row += f" {'∞':>8}"
        print(row)

    print("\n--- Tightness Ratios at peak enstrophy ---")
    print(f"{'IC':15s} {'Re':>5} {'k=1':>8} {'k=2':>8} {'k=3':>8} {'k=4':>8} {'k=5':>8} {'k=6':>8}")
    print("-" * 70)
    for r in all_results:
        row = f"{r['IC']:15s} {r['Re']:>5}"
        for tr in r['tightness_peak'][:6]:
            if tr['tightness'] < 1e6:
                row += f" {tr['tightness']:>8.2f}"
            else:
                row += f" {'∞':>8}"
        print(row)

    print("\nDONE")


if __name__ == '__main__':
    main()
