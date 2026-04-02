"""
Compute Δ₃ spectral rigidity for Gauss matrices at key primes.
Compare to C1 (Δ₃_sat ≈ 0.285) and GUE prediction.
"""

import numpy as np
from scipy.linalg import eigh
import json
import os
import time

def precompute_mangoldt(max_n):
    vals = np.zeros(max_n + 1)
    for n in range(2, max_n + 1):
        temp = n
        found_prime = None
        for p in range(2, int(n**0.5) + 1):
            if temp % p == 0:
                found_prime = p
                while temp % p == 0:
                    temp //= p
                break
        if found_prime is None:
            vals[n] = np.log(n)
        elif temp == 1:
            vals[n] = np.log(found_prime)
    return vals

def build_c3_gauss(N, mgv, p):
    i_idx, j_idx = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    diff_abs = np.abs(i_idx - j_idx)
    amp = mgv[diff_abs + 1]
    jk_mod = ((i_idx + 1) * (j_idx + 1)) % p
    phases = 2 * np.pi * jk_mod / p
    H = amp * np.exp(1j * phases)
    np.fill_diagonal(H, float(np.real(mgv[1])))
    H = (H + H.conj().T) / 2
    return H

def unfold_eigenvalues(evals, deg=7):
    evals_sorted = np.sort(evals)
    N = len(evals_sorted)
    cum = np.arange(1, N + 1, dtype=float)
    x_min, x_max = evals_sorted[0], evals_sorted[-1]
    x_norm = (evals_sorted - x_min) / (x_max - x_min + 1e-15) * 2 - 1
    poly_coeffs = np.polyfit(x_norm, cum, deg=deg)
    unfolded = np.polyval(poly_coeffs, x_norm)
    spacings = np.diff(unfolded)
    mean_sp = spacings.mean()
    if mean_sp > 0:
        unfolded = unfolded / mean_sp
    return unfolded

def delta3_correct(unfolded, L, n_windows=300):
    N_eig = len(unfolded)
    delta3_values = []
    u_min = unfolded[0]
    u_max = unfolded[-1]
    if u_max - u_min <= L:
        return np.nan

    rng_w = np.random.default_rng(12345)
    window_starts = rng_w.uniform(u_min, u_max - L, n_windows)

    for E0 in window_starts:
        E1 = E0 + L
        mask = (unfolded >= E0) & (unfolded < E1)
        ys = unfolded[mask]
        n = len(ys)
        if n < 3:
            continue
        xs = ys - E0
        xs_ext = np.concatenate([[0.0], xs, [L]])
        n_intervals = len(xs_ext) - 1

        S_f2 = S_f1 = S_fx = S_x2 = S_x1 = S_1 = 0.0

        for i in range(n_intervals):
            xl = xs_ext[i]
            xr = xs_ext[i + 1]
            dx = xr - xl
            if dx <= 0:
                continue
            count = float(i)
            int_x = (xr**2 - xl**2) / 2.0
            int_x2 = (xr**3 - xl**3) / 3.0

            S_f2 += count**2 * dx
            S_f1 += count * dx
            S_fx += count * int_x
            S_x2 += int_x2
            S_x1 += int_x
            S_1 += dx

        det = S_x2 * S_1 - S_x1**2
        if abs(det) < 1e-10:
            continue

        a_opt = (S_fx * S_1 - S_f1 * S_x1) / det
        b_opt = (S_f1 * S_x2 - S_fx * S_x1) / det

        delta3_val = (S_f2 - 2*a_opt*S_fx - 2*b_opt*S_f1
                      + a_opt**2*S_x2 + 2*a_opt*b_opt*S_x1 + b_opt**2*S_1) / L
        if delta3_val >= 0:
            delta3_values.append(delta3_val)

    if len(delta3_values) == 0:
        return np.nan
    return np.nanmean(delta3_values)

def delta3_gue_prediction(L):
    gamma_euler = 0.5772156649
    return (1.0 / np.pi**2) * (np.log(2 * np.pi * L) + gamma_euler + 1 - np.pi**2 / 8.0)

def pair_correlation_correct(unfolded, r_bins):
    N = len(unfolded)
    r_max = r_bins[-1]
    diffs = []
    for i in range(N - 1):
        d = unfolded[i+1:] - unfolded[i]
        d = d[d < r_max]
        if len(d) > 0:
            diffs.extend(d.tolist())
    diffs = np.array(diffs)
    counts, _ = np.histogram(diffs, bins=r_bins)
    dr = r_bins[1] - r_bins[0]
    bin_expected = N * dr
    R2 = counts / bin_expected
    return R2

def montgomery_R2(r):
    r = np.asarray(r, dtype=float)
    result = np.ones_like(r)
    mask = r > 1e-8
    result[mask] = 1.0 - (np.sin(np.pi * r[mask]) / (np.pi * r[mask]))**2
    return result

def main():
    N = 500
    mgv = precompute_mangoldt(2 * N + 1)

    # Key primes to test Δ₃
    test_primes = [97, 499, 809, 997, 1801, 9973]
    L_vals = [5, 10, 15, 20, 25, 30, 40, 50]

    print(f"{'p':>6} | {'β_W':>6} | " + " | ".join([f"Δ₃({L})" for L in L_vals]) + " | sat(25-50) | MRD%")
    print("-" * 120)

    results = {}
    r_bins = np.linspace(0.0, 6.0, 121)
    r_centers = (r_bins[:-1] + r_bins[1:]) / 2
    R2_montgomery = montgomery_R2(r_centers)

    for p in test_primes:
        t0 = time.time()
        H = build_c3_gauss(N, mgv, p)
        evals = eigh(H, eigvals_only=True)
        evals.sort()
        unfolded = unfold_eigenvalues(evals, deg=7)

        # Δ₃ for each L
        d3_vals = {}
        for L in L_vals:
            d3 = delta3_correct(unfolded, L, n_windows=300)
            d3_vals[L] = d3

        sat_vals = [d3_vals[L] for L in [25, 30, 40, 50] if not np.isnan(d3_vals.get(L, np.nan))]
        saturation = np.mean(sat_vals) if sat_vals else np.nan

        # Pair correlation
        R2 = pair_correlation_correct(unfolded, r_bins)
        mask_mrd = (r_centers >= 0.5) & (r_centers <= 4.0)
        denom = R2_montgomery[mask_mrd]
        safe_mask = denom > 0.01
        mrd = np.mean(np.abs(R2[mask_mrd][safe_mask] - R2_montgomery[mask_mrd][safe_mask]) / denom[safe_mask])

        # Quick β estimate
        from scipy.optimize import curve_fit
        from scipy.special import gamma as gamfn
        spacings = np.diff(unfolded)
        spacings = spacings[spacings > 0]
        spacings = spacings / spacings.mean()

        def wigner_interp(s, beta):
            g1 = gamfn((beta + 1) / 2)
            g2 = gamfn((beta + 2) / 2)
            B = (g2 / g1)**2
            A = 2 * (g2**(beta + 1)) / (g1**(beta + 2))
            return A * s**beta * np.exp(-B * s**2)

        bins_sp = np.linspace(0, 4.0, 51)
        hist, edges = np.histogram(spacings, bins=bins_sp, density=True)
        centers = (edges[:-1] + edges[1:]) / 2
        mask_h = hist > 0
        try:
            popt, _ = curve_fit(wigner_interp, centers[mask_h], hist[mask_h], p0=[1.0], bounds=([0.0], [4.0]))
            beta_w = float(popt[0])
        except:
            beta_w = np.nan

        elapsed = time.time() - t0

        d3_strs = [f"{d3_vals[L]:.4f}" if not np.isnan(d3_vals.get(L, np.nan)) else "  NaN " for L in L_vals]
        sat_s = f"{saturation:.4f}" if not np.isnan(saturation) else "  NaN "
        print(f"{p:>6} | {beta_w:>6.3f} | " + " | ".join(d3_strs) + f" | {sat_s:>10} | {mrd*100:.1f}% ({elapsed:.1f}s)")

        results[p] = {
            "beta_wigner": float(beta_w) if np.isfinite(beta_w) else None,
            "delta3": {str(L): float(d3_vals[L]) if np.isfinite(d3_vals[L]) else None for L in L_vals},
            "delta3_saturation": float(saturation) if np.isfinite(saturation) else None,
            "pair_corr_mrd": float(mrd),
        }

    # Print GUE predictions for comparison
    print(f"\n{'GUE':>6} | {'2.000':>6} | " +
          " | ".join([f"{delta3_gue_prediction(L):.4f}" for L in L_vals]) +
          f" | {np.mean([delta3_gue_prediction(L) for L in [25,30,40,50]]):.4f}")
    print(f"{'C1':>6} | {'1.182':>6} | 0.1510 | 0.1963 | 0.2206 | 0.2434 | 0.2609 | 0.2741 | 0.2946 | 0.3125 | {'0.2855':>10}")
    print(f"{'Zeta':>6} | {'~2.0':>6} | {'':>6} | {'':>6} | {'':>6} | {'':>6} | ~0.156 | ~0.156 | ~0.156 | ~0.156 | {'0.1545':>10}")

    # Save
    out_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(out_dir, "gauss_delta3_results.json"), "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to gauss_delta3_results.json")

if __name__ == "__main__":
    main()
