"""
Exploration 003: Two-Point Formula + Kernel Operator Construction
=================================================================

Goals:
1. Compute spectral form factor from zeta zeros F_zeros(τ)
2. Compute spectral form factor from prime sums F_primes(τ) (Berry normalization)
3. Compare both to GUE theoretical K_GUE(τ) = min(|τ|, 1)
4. Compute pair correlation R₂ from zeros vs Montgomery formula
5. Construct kernel operator from R₂ and score against constraint catalog

"""

import numpy as np
import json
import time
import os
import sys

EXPLORATION_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE_DIR = os.path.join(EXPLORATION_DIR, 'code')

def log(msg):
    print(msg, flush=True)
    sys.stdout.flush()

# ============================================================
# PART 0: Load zeta zeros
# ============================================================

def load_zeros():
    """Load pre-computed zeros or compute them."""
    # First try local cache
    cache_file = os.path.join(CODE_DIR, 'zeta_zeros_2000.npy')
    if os.path.exists(cache_file):
        zeros = np.load(cache_file)
        log(f"Loaded {len(zeros)} zeros from local cache.")
        return zeros

    # Try from prior exploration
    prior_file = '/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-004/zeta_zeros.json'
    if os.path.exists(prior_file):
        with open(prior_file) as f:
            zeros = np.array(json.load(f))
        log(f"Loaded {len(zeros)} zeros from prior exploration.")
        np.save(cache_file, zeros)
        return zeros

    # Compute fresh
    log("Computing 2000 zeta zeros with mpmath (takes ~6 min)...")
    from mpmath import zetazero, mp
    mp.dps = 25
    N = 2000
    zeros = np.zeros(N)
    t0 = time.time()
    for n in range(1, N+1):
        zeros[n-1] = float(zetazero(n).imag)
        if n % 100 == 0:
            log(f"  {n}/{N} zeros ({time.time()-t0:.0f}s)")
    np.save(cache_file, zeros)
    log(f"Done in {time.time()-t0:.0f}s")
    return zeros


# ============================================================
# PART 1A: Unfolding
# ============================================================

def N_smooth(T):
    """Smooth counting function: N(T) ~ (T/2π) log(T/(2πe)) + 7/8"""
    if T <= 0:
        return 0.0
    return T/(2*np.pi) * np.log(T/(2*np.pi)) - T/(2*np.pi) + 7.0/8.0

def unfold_zeros(zeros):
    """Unfold zeros to mean spacing 1."""
    unfolded = np.array([N_smooth(g) for g in zeros])
    spacings = np.diff(unfolded)
    mean_spacing = np.mean(spacings)
    log(f"  Raw unfolded mean spacing: {mean_spacing:.6f} (should be ~1)")
    # Renormalize to exact mean spacing = 1
    unfolded = unfolded / mean_spacing
    spacings_norm = np.diff(unfolded)
    log(f"  After renorm: mean spacing = {np.mean(spacings_norm):.6f}, std = {np.std(spacings_norm):.6f}")
    return unfolded


# ============================================================
# PART 1B: Form factor from zeros
# ============================================================

def form_factor_zeros(tau_vals, unfolded):
    """
    K_zeros(τ) = (1/N)|∑_n exp(2πiτε_n)|²
    """
    N = len(unfolded)
    K = np.zeros(len(tau_vals))
    for i, tau in enumerate(tau_vals):
        phases = 2.0 * np.pi * tau * unfolded
        re = np.sum(np.cos(phases))
        im = np.sum(np.sin(phases))
        K[i] = (re**2 + im**2) / N
    K[0] = 0.0  # Remove trivial peak at τ=0
    return K


# ============================================================
# PART 1C: Form factor from primes (Berry normalization)
# ============================================================

def form_factor_primes_binned(tau_vals, T, P_max, M_max=5):
    """
    Compute K_primes(τ) using Berry's diagonal approximation:

    K_primes(τ) = (1/T_H²) × Σ_{p^m: τ_p ∈ [τ, τ+dτ]} (ln p)²/p^m × (1/dτ)

    where τ_p = ln(p^m) / T_H and T_H = ln(T/(2π)).

    This is the "binning" approach: each prime power contributes at its
    dimensionless time τ_p with weight (ln p)²/p^m.

    After normalization by T_H², the ramp should give K_primes(τ) ≈ τ.
    """
    from sympy import primerange
    T_H = np.log(T / (2 * np.pi))  # Heisenberg time in log units
    log(f"    T_H = {T_H:.4f}, primes up to {P_max}")

    # Collect prime power contributions
    primes = np.array(list(primerange(2, int(P_max) + 1)), dtype=float)
    positions = []  # τ_p = ln(p^m) / T_H
    weights = []    # (ln p)² / p^m

    for j, p in enumerate(primes):
        ln_p = np.log(p)
        pm = p
        for m in range(1, M_max + 1):
            ln_pm = m * ln_p
            tau_p = ln_pm / T_H
            if tau_p > max(tau_vals) * 1.1:
                break
            w = ln_p**2 / pm  # = (ln p)^2 / p^m
            positions.append(tau_p)
            weights.append(w)
            pm *= p

    positions = np.array(positions)
    weights = np.array(weights)
    log(f"    {len(positions)} prime power contributions")

    # Bin into tau_vals
    dtau = tau_vals[1] - tau_vals[0]
    K_raw = np.zeros(len(tau_vals))
    for pos, w in zip(positions, weights):
        idx = int(round((pos - tau_vals[0]) / dtau))
        if 0 <= idx < len(K_raw):
            K_raw[idx] += w

    # Normalize: divide by (T_H² × dtau) to get density
    K_density = K_raw / (T_H**2 * dtau)

    # Smooth with Gaussian kernel (width σ_τ ≈ 0.05)
    sigma_bins = max(int(0.05 / dtau), 2)
    x_kern = np.arange(-3*sigma_bins, 3*sigma_bins+1)
    kernel = np.exp(-x_kern**2 / (2*sigma_bins**2))
    kernel /= np.sum(kernel)
    K_smooth = np.convolve(K_density, kernel, mode='same')

    return K_smooth, K_density, positions, weights, T_H


def form_factor_primes_cos(tau_vals, T, P_max, M_max=5):
    """
    Alternative formula from the GOAL (cosine series):
    F_primes(τ) = (2π/T) × Σ_{p^m ≤ P_max} (ln p)²/p^m × cos(2πτ × ln(p^m) / ln(T/(2π)))
    """
    from sympy import primerange
    T_H = np.log(T / (2 * np.pi))
    primes = np.array(list(primerange(2, int(P_max) + 1)), dtype=float)

    K = np.zeros(len(tau_vals))
    for j, p in enumerate(primes):
        ln_p = np.log(p)
        pm = p
        for m in range(1, M_max + 1):
            ln_pm = m * ln_p
            w = ln_p**2 / pm
            arg = 2 * np.pi * tau_vals * ln_pm / T_H
            K += w * np.cos(arg)
            pm *= p
            if pm > P_max:
                break

    K *= (2 * np.pi / T)
    return K


# ============================================================
# PART 2: Pair correlation R₂
# ============================================================

def compute_pair_correlation(unfolded, max_r=5.0, n_bins=100):
    """
    Compute R₂(r) = number density of pairs at separation r (unfolded).
    Uses all pairs within max_r unfolded spacings.
    """
    N = len(unfolded)
    r_bins = np.linspace(0, max_r, n_bins + 1)
    r_centers = (r_bins[:-1] + r_bins[1:]) / 2
    dr = r_bins[1] - r_bins[0]

    counts = np.zeros(n_bins)
    # Efficient: for each zero, find neighbors within max_r
    for i in range(N):
        # Search forward (symmetric, so multiply by 2)
        for j in range(i+1, N):
            diff = unfolded[j] - unfolded[i]
            if diff >= max_r:
                break
            bin_idx = int(diff / dr)
            if 0 <= bin_idx < n_bins:
                counts[bin_idx] += 1

    # counts[k] = number of pairs with separation in [k*dr, (k+1)*dr]
    # Two-sided (including i<j and i>j, so multiply by 2):
    counts *= 2

    # Normalize: R₂(r) = (number of pairs in [r, r+dr]) / (N * dr * N/L)
    # For mean spacing = 1, the number density of pairs at r = R₂(r)
    # Expected for Poisson (R₂ = 1): N*(N-1)*dr/L pairs per bin where L is span
    # With unfolded mean spacing = 1, L ≈ N, so expected = (N-1)*dr ≈ N*dr
    # So R₂(r) = counts[k] / (N * N * dr) -- but this gives dimensionless density

    # Standard normalization: R₂(r) dr = probability of finding a pair in [r, r+dr]
    # from a randomly chosen zero
    # = counts / (N * (N-1) * dr) * N    [the N factor normalizes per zero]
    # Simpler: normalize so R₂ → 1 as r → ∞

    # Use: R₂(r) = counts / (N * dr) × (1 / mean_density²)
    # With mean density = 1 (unfolded), R₂(r) = counts / (N * dr)
    R2 = counts / (N * dr)

    # Also compute using window normalization (normalize to large-r limit)
    # At large r, R₂ → 1, so normalize by asymptotic value
    mask_large = r_centers > 3.0
    if mask_large.sum() > 0:
        asymptote = np.mean(R2[mask_large])
        log(f"  Large-r asymptote of R₂: {asymptote:.4f} (should be ~1)")
        R2_normalized = R2 / asymptote
    else:
        R2_normalized = R2

    return r_centers, R2, R2_normalized


# ============================================================
# PART 3: Kernel operator construction and eigenvalue analysis
# ============================================================

def build_kernel_matrix(N, r2_func=None):
    """
    Build N×N kernel matrix with H_{jk} = R₂(|j-k|) / N
    Default uses Montgomery formula: R₂(r) = 1 - (sin(πr)/(πr))²
    """
    log(f"  Building {N}×{N} kernel matrix...")
    j_idx = np.arange(N)
    H = np.zeros((N, N))
    for j in range(N):
        for k in range(N):
            r = abs(j - k)
            if r == 0:
                H[j, k] = 1.0  # R₂(0) = 1
            else:
                if r2_func is not None:
                    H[j, k] = r2_func(r)
                else:
                    H[j, k] = 1.0 - (np.sin(np.pi * r) / (np.pi * r))**2
    H /= N
    return H


def build_kernel_matrix_fast(N, r2_func=None):
    """Faster Toeplitz construction."""
    log(f"  Building {N}×{N} Toeplitz kernel matrix (fast)...")
    r_vals = np.arange(N, dtype=float)
    col = np.zeros(N)
    col[0] = 1.0  # R₂(0) = 1
    for r in range(1, N):
        if r2_func is not None:
            col[r] = r2_func(r)
        else:
            col[r] = 1.0 - (np.sin(np.pi * r) / (np.pi * r))**2

    from scipy.linalg import toeplitz
    H = toeplitz(col) / N
    return H


def score_eigenvalues(eigenvalues, N, name="Kernel"):
    """
    Score eigenvalues against constraint catalog.
    Returns dict with all metrics.
    """
    # Sort ascending
    eigs = np.sort(eigenvalues)

    # Remove edge effects - use bulk
    n_bulk = int(0.8 * len(eigs))
    i_start = int(0.1 * len(eigs))
    eigs_bulk = eigs[i_start:i_start + n_bulk]

    # Normalize bulk spacings to mean = 1
    spacings = np.diff(eigs_bulk)
    if len(spacings) == 0:
        return {}
    mean_s = np.mean(spacings)
    if mean_s <= 0:
        return {}
    s = spacings / mean_s

    results = {}

    # === Constraint 1: β parameter (level repulsion) ===
    # From small-spacing distribution p(s) ~ s^β
    # For GUE β=2, GOE β=1, Poisson β=0
    small_s = s[s < 0.3]
    if len(small_s) > 10:
        # Linear regression of log p(s) vs log s for small s
        hist_s, bins_s = np.histogram(s, bins=50, density=True)
        bin_centers = (bins_s[:-1] + bins_s[1:]) / 2
        small_mask = (bin_centers < 0.5) & (hist_s > 0)
        if small_mask.sum() > 3:
            log_bins = np.log(bin_centers[small_mask])
            log_hist = np.log(hist_s[small_mask])
            beta_fit = np.polyfit(log_bins, log_hist, 1)[0]
            results['beta'] = beta_fit
        else:
            results['beta'] = None
    else:
        results['beta'] = None

    # === Constraint 3: Spacing distribution (Wigner surmise for GUE) ===
    # GUE: p(s) = (32/π²) s² exp(-4s²/π)
    hist_s, bins_s = np.histogram(s, bins=50, density=True)
    bin_centers = (bins_s[:-1] + bins_s[1:]) / 2
    # GUE Wigner surmise
    p_GUE = (32/np.pi**2) * bin_centers**2 * np.exp(-4*bin_centers**2/np.pi)
    # GOE Wigner surmise
    p_GOE = (np.pi/2) * bin_centers * np.exp(-np.pi*bin_centers**2/4)
    # Poisson
    p_Poisson = np.exp(-bin_centers)

    mae_GUE = np.mean(np.abs(hist_s - p_GUE))
    mae_GOE = np.mean(np.abs(hist_s - p_GOE))
    mae_Poisson = np.mean(np.abs(hist_s - p_Poisson))

    results['mae_GUE'] = mae_GUE
    results['mae_GOE'] = mae_GOE
    results['mae_Poisson'] = mae_Poisson
    results['hist_s'] = hist_s
    results['bin_centers'] = bin_centers
    results['p_GUE'] = p_GUE
    results['p_GOE'] = p_GOE
    results['p_Poisson'] = p_Poisson

    # === Constraint 4: GUE vs GOE discrimination ===
    # Better fit to GUE means β > 1.5
    results['best_fit'] = 'GUE' if mae_GUE < mae_GOE else 'GOE'

    # === Constraint 5: Level variance Σ²(L) ===
    # GUE: Σ²(L) ~ (2/π²) ln(L) for large L
    L_vals = np.array([1, 2, 4, 8, 16])
    sigma2_vals = []
    for L in L_vals:
        # Count levels in windows of length L
        window_counts = []
        for i in range(0, len(eigs_bulk) - int(L/mean_s), max(1, int(L/mean_s)//2)):
            E0 = eigs_bulk[i]
            E1 = E0 + L * mean_s
            count = np.sum((eigs_bulk >= E0) & (eigs_bulk < E1))
            window_counts.append(count)
        if window_counts:
            sigma2_vals.append(np.var(window_counts))
        else:
            sigma2_vals.append(np.nan)

    results['L_vals'] = L_vals
    results['sigma2_vals'] = sigma2_vals

    # Estimate slope of Σ²(L) vs ln(L)
    valid = [(L, s2) for L, s2 in zip(L_vals, sigma2_vals)
             if not np.isnan(s2) and L > 1 and s2 > 0]
    if len(valid) >= 2:
        log_L = np.array([np.log(x[0]) for x in valid])
        s2 = np.array([x[1] for x in valid])
        slope = np.polyfit(log_L, s2, 1)[0]
        results['sigma2_slope'] = slope
        results['sigma2_slope_GUE_theory'] = 2/np.pi**2  # ≈ 0.203
    else:
        results['sigma2_slope'] = None

    log(f"\n  === Eigenvalue Analysis for {name} ===")
    log(f"  N = {N}, {len(eigs)} eigenvalues")
    log(f"  Range: [{eigs[0]:.4f}, {eigs[-1]:.4f}]")
    log(f"  Bulk spacings: mean = {mean_s:.4f}")

    if results['beta'] is not None:
        log(f"  Level repulsion β = {results['beta']:.3f} (GUE target: 2.0, GOE: 1.0, Poisson: 0.0)")
    log(f"  MAE vs GUE spacing: {mae_GUE:.4f}")
    log(f"  MAE vs GOE spacing: {mae_GOE:.4f}")
    log(f"  MAE vs Poisson:     {mae_Poisson:.4f}")
    log(f"  Best fit: {results['best_fit']}")
    if results.get('sigma2_slope') is not None:
        log(f"  Σ²(L) slope: {results['sigma2_slope']:.4f} (GUE theory: {results['sigma2_slope_GUE_theory']:.4f})")

    return results, eigs, s


# ============================================================
# MAIN COMPUTATION
# ============================================================

def main():
    t0 = time.time()
    log("=" * 70)
    log("EXPLORATION 003: Two-Point Formula + Kernel Operator Construction")
    log("=" * 70)

    # --- Load zeros ---
    log("\n[STEP 1] Loading zeta zeros...")
    zeros = load_zeros()
    N_zeros = len(zeros)
    log(f"  N = {N_zeros} zeros, range: [{zeros[0]:.4f}, {zeros[-1]:.4f}]")
    T_max = zeros[-1]  # Use last zero as T

    # --- Unfold ---
    log("\n[STEP 2] Unfolding zeros...")
    unfolded = unfold_zeros(zeros)
    spacings = np.diff(unfolded)
    log(f"  Unfolded zero range: [{unfolded[0]:.4f}, {unfolded[-1]:.4f}]")

    # --- Form factor from zeros ---
    log("\n[STEP 3] Computing form factor K_zeros(τ)...")
    tau_vals = np.linspace(0.0, 2.5, 251)
    t1 = time.time()
    K_zeros = form_factor_zeros(tau_vals, unfolded)
    log(f"  Done in {time.time()-t1:.1f}s")

    # Smooth K_zeros
    sigma_bins = max(int(0.05 / (tau_vals[1]-tau_vals[0])), 2)
    x_kern = np.arange(-3*sigma_bins, 3*sigma_bins+1)
    kernel = np.exp(-x_kern**2 / (2*sigma_bins**2))
    kernel /= np.sum(kernel)
    K_zeros_smooth = np.convolve(K_zeros, kernel, mode='same')

    # GUE prediction
    K_GUE = np.minimum(tau_vals, 1.0)

    log("\n  Form Factor K_zeros vs K_GUE:")
    log(f"  {'tau':>6} {'K_GUE':>8} {'K_zeros':>10} {'K_smooth':>10} {'ratio_sm':>10}")
    log("  " + "-"*50)
    for tau_target in [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5, 2.0]:
        dtau = tau_vals[1] - tau_vals[0]
        idx = int(round(tau_target / dtau))
        if idx < len(tau_vals):
            tau = tau_vals[idx]
            gue = K_GUE[idx]
            kz = K_zeros[idx]
            ks = K_zeros_smooth[idx]
            ratio = ks/gue if gue > 0 else float('inf')
            log(f"  {tau:6.3f} {gue:8.4f} {kz:10.4f} {ks:10.4f} {ratio:10.4f}")

    # MAE metrics
    dtau = tau_vals[1] - tau_vals[0]
    mask_ramp = (tau_vals > 0.05) & (tau_vals < 0.95)
    mask_plat = (tau_vals > 1.05) & (tau_vals < 2.0)
    mae_ramp = np.mean(np.abs(K_zeros_smooth[mask_ramp] - K_GUE[mask_ramp]))
    mae_plat = np.mean(np.abs(K_zeros_smooth[mask_plat] - K_GUE[mask_plat]))
    log(f"\n  MAE K_zeros vs K_GUE (ramp, 0.05-0.95):  {mae_ramp:.6f}")
    log(f"  MAE K_zeros vs K_GUE (plateau, 1.05-2.0): {mae_plat:.6f}")

    # --- Form factor from primes ---
    log("\n[STEP 4] Computing form factor K_primes(τ) from prime sums (Berry normalization)...")
    T_ref = T_max  # Use last zero height as reference height
    log(f"  Using T = {T_ref:.1f}, T_H = ln(T/(2π)) = {np.log(T_ref/(2*np.pi)):.4f}")

    P_max_list = [100, 1000, 10000]
    K_primes_results = {}

    for P_max in P_max_list:
        log(f"\n  === P_max = {P_max} ===")
        K_sm, K_dn, pos, wts, T_H = form_factor_primes_binned(tau_vals, T_ref, P_max)
        K_primes_results[P_max] = {
            'K_smooth': K_sm, 'K_density': K_dn,
            'positions': pos, 'weights': wts, 'T_H': T_H
        }

        # Error metrics
        mae_p_ramp = np.mean(np.abs(K_sm[mask_ramp] - K_GUE[mask_ramp]))
        mae_p_gue = np.mean(np.abs(K_sm[mask_ramp] - K_GUE[mask_ramp]))
        # Compare to K_zeros_smooth
        mae_p_zeros = np.mean(np.abs(K_sm[mask_ramp] - K_zeros_smooth[mask_ramp]))

        log(f"  K_primes MAE vs K_GUE (ramp):   {mae_p_ramp:.6f}")
        log(f"  K_primes MAE vs K_zeros (ramp):  {mae_p_zeros:.6f}")

        log(f"  {'tau':>6} {'K_GUE':>8} {'K_zeros_sm':>12} {'K_primes_sm':>13}")
        log("  " + "-"*45)
        for tau_target in [0.1, 0.3, 0.5, 0.7, 1.0, 1.5]:
            idx = int(round(tau_target / dtau))
            if idx < len(tau_vals):
                log(f"  {tau_vals[idx]:6.3f} {K_GUE[idx]:8.4f} {K_zeros_smooth[idx]:12.4f} {K_sm[idx]:13.4f}")

    # Also compute cosine-series version for P_max = 1000
    log("\n  === Cosine-series formula (P_max=1000) ===")
    K_cos = form_factor_primes_cos(tau_vals, T_ref, 1000)
    # Smooth it
    K_cos_smooth = np.convolve(K_cos, kernel, mode='same')
    mae_cos_ramp = np.mean(np.abs(K_cos_smooth[mask_ramp] - K_GUE[mask_ramp]))
    log(f"  Cosine formula MAE vs K_GUE (ramp): {mae_cos_ramp:.6f}")

    # --- Pair Correlation R₂ ---
    log("\n[STEP 5] Computing pair correlation R₂(r)...")
    t1 = time.time()
    r_centers, R2_raw, R2_norm = compute_pair_correlation(unfolded, max_r=5.0, n_bins=100)
    log(f"  Done in {time.time()-t1:.1f}s")

    # Montgomery formula
    R2_montgomery = 1 - (np.sinc(r_centers))**2  # sinc(x) = sin(πx)/(πx)

    log("\n  Pair Correlation R₂(r): zeros vs Montgomery")
    log(f"  {'r':>6} {'R₂_Mont':>10} {'R₂_zeros':>10} {'R₂_norm':>10} {'diff_raw':>10}")
    log("  " + "-"*50)
    for r_target in [0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
        dr = r_centers[1] - r_centers[0]
        idx = int(round(r_target / dr))
        if idx < len(r_centers):
            r = r_centers[idx]
            mont = R2_montgomery[idx]
            r2r = R2_raw[idx]
            r2n = R2_norm[idx]
            log(f"  {r:6.3f} {mont:10.4f} {r2r:10.4f} {r2n:10.4f} {r2r - mont:10.4f}")

    # MAE for pair correlation
    mask_r = (r_centers > 0.1) & (r_centers < 4.0)
    mae_R2_raw = np.mean(np.abs(R2_raw[mask_r] - R2_montgomery[mask_r]))
    mae_R2_norm = np.mean(np.abs(R2_norm[mask_r] - R2_montgomery[mask_r]))
    log(f"\n  MAE R₂_raw vs Montgomery (0.1-4.0):  {mae_R2_raw:.6f}")
    log(f"  MAE R₂_norm vs Montgomery (0.1-4.0): {mae_R2_norm:.6f}")
    log(f"  Fractional deviation (raw): {mae_R2_raw:.2%}")
    log(f"  Fractional deviation (norm): {mae_R2_norm:.2%}")

    # --- Kernel Operator Construction ---
    log("\n[STEP 6] Constructing kernel operator from Montgomery R₂...")
    from scipy.linalg import toeplitz

    for N_kern in [200, 500]:
        log(f"\n  === N = {N_kern} kernel matrix ===")
        H = build_kernel_matrix_fast(N_kern)
        log(f"  Matrix built, computing eigenvalues...")
        t1 = time.time()
        eigs = np.linalg.eigvalsh(H)
        log(f"  Eigenvalues computed in {time.time()-t1:.1f}s")
        log(f"  Eigenvalue range: [{eigs[0]:.6f}, {eigs[-1]:.6f}]")

        results, eigs_sorted, s_norm = score_eigenvalues(eigs, N_kern, name=f"Montgomery R₂ Kernel (N={N_kern})")

    # Also try with numerical R₂ from zeros
    log("\n[STEP 7] Kernel from NUMERICAL R₂ (from actual zeros)...")
    # Build kernel using R2_norm interpolation
    from scipy.interpolate import interp1d
    r2_interp = interp1d(r_centers, R2_norm, kind='linear',
                         bounds_error=False, fill_value=1.0)

    N_kern = 300
    log(f"  Building {N_kern}×{N_kern} numerical kernel matrix...")
    col = np.zeros(N_kern)
    col[0] = 1.0
    for r in range(1, N_kern):
        col[r] = float(r2_interp(r))

    H_numerical = toeplitz(col) / N_kern
    eigs_num = np.linalg.eigvalsh(H_numerical)
    results_num, eigs_num_sorted, s_num = score_eigenvalues(
        eigs_num, N_kern, name=f"Numerical R₂ Kernel (N={N_kern})")

    # === Save all results ===
    log("\n[STEP 8] Saving results...")
    np.savez(os.path.join(CODE_DIR, 'all_results.npz'),
             tau_vals=tau_vals, K_zeros=K_zeros, K_zeros_smooth=K_zeros_smooth,
             K_GUE=K_GUE,
             K_primes_100=K_primes_results[100]['K_smooth'],
             K_primes_1000=K_primes_results[1000]['K_smooth'],
             K_primes_10000=K_primes_results[10000]['K_smooth'],
             K_cos=K_cos_smooth,
             r_centers=r_centers, R2_raw=R2_raw, R2_norm=R2_norm,
             R2_montgomery=R2_montgomery,
             zeros=zeros, unfolded=unfolded,
             mae_ramp=np.array([mae_ramp]),
             mae_plat=np.array([mae_plat]),
             mae_R2_raw=np.array([mae_R2_raw]),
             mae_R2_norm=np.array([mae_R2_norm]),
             eigs_kern200=np.sort(np.linalg.eigvalsh(build_kernel_matrix_fast(200))),
             eigs_num=np.sort(eigs_num)
             )

    log(f"\nTotal computation time: {time.time()-t0:.1f}s")

    # === Summary ===
    log("\n" + "=" * 70)
    log("SUMMARY OF RESULTS")
    log("=" * 70)
    log(f"\n1. Form Factor from zeros (K_zeros vs K_GUE):")
    log(f"   MAE in ramp region:    {mae_ramp:.4f}")
    log(f"   MAE in plateau region: {mae_plat:.4f}")

    log(f"\n2. Form Factor from primes (K_primes vs K_GUE, ramp):")
    for P_max in P_max_list:
        K_sm = K_primes_results[P_max]['K_smooth']
        mae = np.mean(np.abs(K_sm[mask_ramp] - K_GUE[mask_ramp]))
        log(f"   P_max = {P_max:>6}: MAE = {mae:.4f}")

    log(f"\n3. Pair Correlation deviation from Montgomery:")
    log(f"   MAE (raw):  {mae_R2_raw:.4f}  ({mae_R2_raw:.2%})")
    log(f"   MAE (norm): {mae_R2_norm:.4f}  ({mae_R2_norm:.2%})")

    # Return key metrics for report
    return {
        'mae_ramp': mae_ramp,
        'mae_plat': mae_plat,
        'mae_R2_raw': mae_R2_raw,
        'mae_R2_norm': mae_R2_norm,
        'K_primes_maes': {P: np.mean(np.abs(K_primes_results[P]['K_smooth'][mask_ramp] - K_GUE[mask_ramp]))
                          for P in P_max_list},
        'kernel_results': results,
        'kernel_results_num': results_num,
    }


if __name__ == '__main__':
    main()
