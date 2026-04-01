#!/usr/bin/env python3
"""
Task 2: Finite-dimensional primal — maximize level-set measure over div-free fields.

We search over div-free Fourier fields on T³ = [0,2π]³ with |k| ≤ N,
and for each field compute the "Chebyshev ratio":
    R = |{|u| > λ}| / (λ^{-10/3} ||u||_{10/3}^{10/3})

If R → 1 is achievable by div-free fields, Chebyshev is tight.
If R stays bounded away from 1, div-free constrains the distribution.

We also compute R for UNCONSTRAINED fields (no div-free) to compare.
"""

import numpy as np
from scipy.optimize import minimize, differential_evolution
import sys
import time

# =================================================================
# Setup: Div-free Fourier parameterization on T³
# =================================================================

def get_fourier_modes(N):
    """Get all non-zero integer vectors k with |k|_∞ ≤ N,
    selecting only one from each (k, -k) pair to avoid double counting."""
    modes = []
    for kx in range(-N, N+1):
        for ky in range(-N, N+1):
            for kz in range(-N, N+1):
                if kx == 0 and ky == 0 and kz == 0:
                    continue
                k = (kx, ky, kz)
                # Take only one from each (k, -k) pair:
                # use lexicographic ordering
                neg_k = (-kx, -ky, -kz)
                if k > neg_k:  # lexicographic
                    continue
                modes.append(np.array(k, dtype=float))
    return modes

def divfree_basis(k):
    """
    Given k ∈ Z³\{0}, return two orthonormal vectors e1, e2 perpendicular to k.
    These span the divergence-free subspace for mode k.
    """
    k_norm = np.linalg.norm(k)
    k_hat = k / k_norm

    # Find a vector not parallel to k
    if abs(k_hat[0]) < 0.9:
        v = np.array([1.0, 0.0, 0.0])
    else:
        v = np.array([0.0, 1.0, 0.0])

    e1 = v - np.dot(v, k_hat) * k_hat
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(k_hat, e1)
    e2 /= np.linalg.norm(e2)

    return e1, e2

def params_to_field_divfree(params, modes, grid_x, grid_y, grid_z):
    """
    Convert parameter vector to a divergence-free field on the spatial grid.

    For each mode k, we have 4 real parameters: (a1, b1, a2, b2)
    representing û_k = (a1 + i*b1)*e1 + (a2 + i*b2)*e2
    where e1, e2 are the div-free basis vectors for k.

    The field is: u(x) = Σ_k [û_k e^{ikx} + conj(û_k) e^{-ikx}]
                       = 2 Σ_k Re[û_k e^{ikx}]
    """
    n_modes = len(modes)
    # Shape of grid: (Ng, Ng, Ng)
    Ng = grid_x.shape[0]
    ux = np.zeros((Ng, Ng, Ng))
    uy = np.zeros((Ng, Ng, Ng))
    uz = np.zeros((Ng, Ng, Ng))

    for i, k in enumerate(modes):
        a1, b1, a2, b2 = params[4*i:4*i+4]
        e1, e2 = divfree_basis(k)

        # û_k = (a1 + i*b1)*e1 + (a2 + i*b2)*e2
        uk_real = a1 * e1 + a2 * e2
        uk_imag = b1 * e1 + b2 * e2

        # Phase: k · x
        phase = k[0]*grid_x + k[1]*grid_y + k[2]*grid_z
        cos_phase = np.cos(phase)
        sin_phase = np.sin(phase)

        # 2 Re[û_k e^{ikx}] = 2[uk_real cos(kx) - uk_imag sin(kx)]
        ux += 2 * (uk_real[0] * cos_phase - uk_imag[0] * sin_phase)
        uy += 2 * (uk_real[1] * cos_phase - uk_imag[1] * sin_phase)
        uz += 2 * (uk_real[2] * cos_phase - uk_imag[2] * sin_phase)

    return ux, uy, uz

def params_to_field_unconstrained(params, modes, grid_x, grid_y, grid_z):
    """
    Same as above but WITHOUT div-free constraint.
    Each mode has 6 real parameters (3 complex components).
    """
    n_modes = len(modes)
    Ng = grid_x.shape[0]
    ux = np.zeros((Ng, Ng, Ng))
    uy = np.zeros((Ng, Ng, Ng))
    uz = np.zeros((Ng, Ng, Ng))

    for i, k in enumerate(modes):
        ax, bx, ay, by, az, bz = params[6*i:6*i+6]

        phase = k[0]*grid_x + k[1]*grid_y + k[2]*grid_z
        cos_phase = np.cos(phase)
        sin_phase = np.sin(phase)

        ux += 2 * (ax * cos_phase - bx * sin_phase)
        uy += 2 * (ay * cos_phase - by * sin_phase)
        uz += 2 * (az * cos_phase - bz * sin_phase)

    return ux, uy, uz

def compute_norms_and_levelset(ux, uy, uz, lam, dx):
    """Compute L^2, L^{10/3} norms and level-set measure."""
    mag_sq = ux**2 + uy**2 + uz**2
    mag = np.sqrt(mag_sq)

    vol = dx**3  # volume element

    # L^2 norm
    L2_sq = np.sum(mag_sq) * vol
    L2 = np.sqrt(L2_sq)

    # L^{10/3} norm
    p = 10.0/3.0
    Lp_p = np.sum(mag**p) * vol
    Lp = Lp_p**(1.0/p)

    # Level set measure
    level_set = np.sum(mag > lam) * vol

    # Chebyshev bound
    cheb_bound = lam**(-p) * Lp_p

    # Ratio
    ratio = level_set / cheb_bound if cheb_bound > 1e-15 else 0.0

    return {
        'L2': L2, 'Lp': Lp, 'Lp_p': Lp_p,
        'level_set': level_set, 'cheb_bound': cheb_bound,
        'ratio': ratio, 'max_mag': np.max(mag)
    }

# =================================================================
# Grid setup
# =================================================================
Ng = 32  # Spatial grid points per dimension
dx = 2*np.pi / Ng
x1d = np.arange(Ng) * dx
grid_x, grid_y, grid_z = np.meshgrid(x1d, x1d, x1d, indexing='ij')
total_vol = (2*np.pi)**3

print(f"Grid: {Ng}³ = {Ng**3} points, dx = {dx:.4f}")
print(f"Total volume = (2π)³ = {total_vol:.4f}")

# =================================================================
# Experiment 1: Random div-free fields — Chebyshev ratio survey
# =================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 1: Chebyshev ratio for random div-free fields")
print("=" * 70)

N_freq = 2  # Max frequency (|k|_∞ ≤ N_freq)
modes = get_fourier_modes(N_freq)
n_modes = len(modes)
n_params_df = 4 * n_modes  # div-free: 4 params per mode pair
n_params_uc = 6 * n_modes  # unconstrained: 6 params per mode pair

print(f"N_freq = {N_freq}: {n_modes} mode pairs")
print(f"  Div-free params: {n_params_df}, Unconstrained params: {n_params_uc}")

# Survey: random div-free fields
n_trials = 500
lam_frac = 0.5  # λ = frac * max|u|

print(f"\nSurveying {n_trials} random div-free fields (λ = {lam_frac}*max|u|)...")
ratios_df = []
ratios_uc = []

np.random.seed(42)
for trial in range(n_trials):
    # Random div-free field
    params_df = np.random.randn(n_params_df)
    ux, uy, uz = params_to_field_divfree(params_df, modes, grid_x, grid_y, grid_z)
    mag = np.sqrt(ux**2 + uy**2 + uz**2)
    lam_val = lam_frac * np.max(mag)
    if lam_val < 1e-10:
        continue
    res = compute_norms_and_levelset(ux, uy, uz, lam_val, dx)
    ratios_df.append(res['ratio'])

    # Random unconstrained field (same number of effective modes)
    params_uc = np.random.randn(n_params_uc)
    ux2, uy2, uz2 = params_to_field_unconstrained(params_uc, modes, grid_x, grid_y, grid_z)
    mag2 = np.sqrt(ux2**2 + uy2**2 + uz2**2)
    lam_val2 = lam_frac * np.max(mag2)
    if lam_val2 < 1e-10:
        continue
    res2 = compute_norms_and_levelset(ux2, uy2, uz2, lam_val2, dx)
    ratios_uc.append(res2['ratio'])

ratios_df = np.array(ratios_df)
ratios_uc = np.array(ratios_uc)

print(f"\nDiv-free fields (n={len(ratios_df)}):")
print(f"  Ratio mean = {np.mean(ratios_df):.6f}")
print(f"  Ratio max  = {np.max(ratios_df):.6f}")
print(f"  Ratio min  = {np.min(ratios_df):.6f}")
print(f"  Ratio std  = {np.std(ratios_df):.6f}")

print(f"\nUnconstrained fields (n={len(ratios_uc)}):")
print(f"  Ratio mean = {np.mean(ratios_uc):.6f}")
print(f"  Ratio max  = {np.max(ratios_uc):.6f}")
print(f"  Ratio min  = {np.min(ratios_uc):.6f}")
print(f"  Ratio std  = {np.std(ratios_uc):.6f}")

print(f"\nMax ratio comparison:")
print(f"  Div-free max / Unconstrained max = {np.max(ratios_df) / np.max(ratios_uc):.4f}")

# =================================================================
# Experiment 2: Optimized div-free field — maximize Chebyshev ratio
# =================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 2: Optimize div-free field to MAXIMIZE Chebyshev ratio")
print("=" * 70)

def neg_chebyshev_ratio_divfree(params, modes, grid_x, grid_y, grid_z, lam_frac, dx):
    """Negative Chebyshev ratio for minimization (div-free)."""
    try:
        ux, uy, uz = params_to_field_divfree(params, modes, grid_x, grid_y, grid_z)
        mag = np.sqrt(ux**2 + uy**2 + uz**2)
        max_mag = np.max(mag)
        if max_mag < 1e-10:
            return 0.0
        lam_val = lam_frac * max_mag
        p = 10.0/3.0
        vol = dx**3
        Lp_p = np.sum(mag**p) * vol
        level_set = np.sum(mag > lam_val) * vol
        cheb = lam_val**(-p) * Lp_p
        if cheb < 1e-15:
            return 0.0
        return -level_set / cheb
    except:
        return 0.0

def neg_chebyshev_ratio_unconstrained(params, modes, grid_x, grid_y, grid_z, lam_frac, dx):
    """Negative Chebyshev ratio for minimization (unconstrained)."""
    try:
        ux, uy, uz = params_to_field_unconstrained(params, modes, grid_x, grid_y, grid_z)
        mag = np.sqrt(ux**2 + uy**2 + uz**2)
        max_mag = np.max(mag)
        if max_mag < 1e-10:
            return 0.0
        lam_val = lam_frac * max_mag
        p = 10.0/3.0
        vol = dx**3
        Lp_p = np.sum(mag**p) * vol
        level_set = np.sum(mag > lam_val) * vol
        cheb = lam_val**(-p) * Lp_p
        if cheb < 1e-15:
            return 0.0
        return -level_set / cheb
    except:
        return 0.0

# Optimize with multiple random starts (Nelder-Mead)
print("\nOptimizing div-free (multi-start Nelder-Mead)...")
best_ratio_df = 0.0
best_params_df = None

t0 = time.time()
for trial in range(50):
    x0 = np.random.randn(n_params_df) * 1.0
    res = minimize(neg_chebyshev_ratio_divfree, x0,
                   args=(modes, grid_x, grid_y, grid_z, 0.5, dx),
                   method='Nelder-Mead',
                   options={'maxiter': 2000, 'xatol': 1e-6, 'fatol': 1e-8})
    ratio = -res.fun
    if ratio > best_ratio_df:
        best_ratio_df = ratio
        best_params_df = res.x

t1 = time.time()
print(f"  Best ratio (div-free, λ=0.5*max): {best_ratio_df:.6f}  [{t1-t0:.1f}s]")

print("\nOptimizing unconstrained (multi-start Nelder-Mead)...")
best_ratio_uc = 0.0
best_params_uc = None

t0 = time.time()
for trial in range(50):
    x0 = np.random.randn(n_params_uc) * 1.0
    res = minimize(neg_chebyshev_ratio_unconstrained, x0,
                   args=(modes, grid_x, grid_y, grid_z, 0.5, dx),
                   method='Nelder-Mead',
                   options={'maxiter': 2000, 'xatol': 1e-6, 'fatol': 1e-8})
    ratio = -res.fun
    if ratio > best_ratio_uc:
        best_ratio_uc = ratio
        best_params_uc = res.x

t1 = time.time()
print(f"  Best ratio (unconstrained, λ=0.5*max): {best_ratio_uc:.6f}  [{t1-t0:.1f}s]")

print(f"\nRatio comparison (optimized):")
print(f"  Div-free best:       {best_ratio_df:.6f}")
print(f"  Unconstrained best:  {best_ratio_uc:.6f}")
print(f"  DF / UC:             {best_ratio_df / best_ratio_uc:.4f}" if best_ratio_uc > 0 else "  UC ratio is 0")

# =================================================================
# Experiment 3: Vary λ threshold and compare
# =================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 3: Chebyshev ratio vs threshold λ/max|u|")
print("=" * 70)

lam_fracs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

print(f"\n{'λ/max':>8} {'DF mean':>10} {'DF max':>10} {'UC mean':>10} {'UC max':>10} {'DF/UC max':>10}")
print("-" * 65)

for lf in lam_fracs:
    rdf = []
    ruc = []
    np.random.seed(123)
    for trial in range(200):
        # Div-free
        p_df = np.random.randn(n_params_df)
        ux, uy, uz = params_to_field_divfree(p_df, modes, grid_x, grid_y, grid_z)
        mag = np.sqrt(ux**2 + uy**2 + uz**2)
        lam_val = lf * np.max(mag)
        if lam_val < 1e-10:
            continue
        res = compute_norms_and_levelset(ux, uy, uz, lam_val, dx)
        rdf.append(res['ratio'])

        # Unconstrained
        p_uc = np.random.randn(n_params_uc)
        ux2, uy2, uz2 = params_to_field_unconstrained(p_uc, modes, grid_x, grid_y, grid_z)
        mag2 = np.sqrt(ux2**2 + uy2**2 + uz2**2)
        lam_val2 = lf * np.max(mag2)
        if lam_val2 < 1e-10:
            continue
        res2 = compute_norms_and_levelset(ux2, uy2, uz2, lam_val2, dx)
        ruc.append(res2['ratio'])

    rdf = np.array(rdf)
    ruc = np.array(ruc)
    if len(rdf) > 0 and len(ruc) > 0:
        dfuc_ratio = np.max(rdf) / np.max(ruc) if np.max(ruc) > 0 else float('inf')
        print(f"{lf:8.2f} {np.mean(rdf):10.4f} {np.max(rdf):10.4f} {np.mean(ruc):10.4f} {np.max(ruc):10.4f} {dfuc_ratio:10.4f}")

# =================================================================
# Experiment 4: Attempt to construct near-extremizer
# =================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 4: Construct Chebyshev near-extremizer (div-free)")
print("=" * 70)
print("""
The Chebyshev extremizer for L^p is f = c · 1_A (constant on a set A).
In Fourier space, this corresponds to a "box" function.
For div-free fields, the closest analog is a field that is nearly constant
in magnitude on a large region and small elsewhere.

Strategy: use low-frequency div-free modes to create a field that
concentrates its L^{10/3} norm in a set where |u| is just above λ.
This is like building a "plateau" function using div-free modes.
""")

# Try: single mode (k = (1,0,0), e1 direction) — this gives u ~ sin(x)
# The magnitude varies smoothly; can't make a plateau.
# Try: superposition of modes to approximate a plateau.

# Best approach: use optimization with a FIXED λ (not relative to max)
def neg_ratio_fixed_lambda(params, modes, grid_x, grid_y, grid_z, lam_fixed, dx):
    """Maximize ratio with a FIXED λ (not relative to max)."""
    try:
        ux, uy, uz = params_to_field_divfree(params, modes, grid_x, grid_y, grid_z)
        mag = np.sqrt(ux**2 + uy**2 + uz**2)
        p = 10.0/3.0
        vol = dx**3
        Lp_p = np.sum(mag**p) * vol
        level_set = np.sum(mag > lam_fixed) * vol
        cheb = lam_fixed**(-p) * Lp_p
        if cheb < 1e-15:
            return 0.0
        return -level_set / cheb
    except:
        return 0.0

# Use N=3 for more expressiveness
N_freq3 = 3
modes3 = get_fourier_modes(N_freq3)
n_modes3 = len(modes3)
n_params3 = 4 * n_modes3
print(f"\nUsing N_freq={N_freq3}: {n_modes3} mode pairs, {n_params3} params")

lam_fixed = 1.0
print(f"Fixed λ = {lam_fixed}")
print("\nOptimizing (50 random starts, Nelder-Mead)...")

best_ratio_plateau = 0.0
best_params_plateau = None

t0 = time.time()
for trial in range(50):
    x0 = np.random.randn(n_params3) * 2.0
    res = minimize(neg_ratio_fixed_lambda, x0,
                   args=(modes3, grid_x, grid_y, grid_z, lam_fixed, dx),
                   method='Nelder-Mead',
                   options={'maxiter': 5000, 'xatol': 1e-6, 'fatol': 1e-8})
    ratio = -res.fun
    if ratio > best_ratio_plateau:
        best_ratio_plateau = ratio
        best_params_plateau = res.x
t1 = time.time()

print(f"  Best ratio (fixed λ={lam_fixed}): {best_ratio_plateau:.6f}  [{t1-t0:.1f}s]")

# Analyze the best field
if best_params_plateau is not None:
    ux, uy, uz = params_to_field_divfree(best_params_plateau, modes3, grid_x, grid_y, grid_z)
    mag = np.sqrt(ux**2 + uy**2 + uz**2)
    print(f"  max|u| = {np.max(mag):.4f}, min|u| = {np.min(mag):.4f}")
    print(f"  |{'{'}|u|>{lam_fixed}{'}'}| / |Ω| = {np.mean(mag > lam_fixed):.4f}")

    # L^p norm
    p = 10.0/3.0
    vol = dx**3
    Lp_p = np.sum(mag**p) * vol
    print(f"  ||u||_{'{'}10/3{'}'}^{'{'}10/3{'}'} = {Lp_p:.4f}")
    print(f"  Chebyshev bound = {lam_fixed**(-p) * Lp_p:.4f}")
    print(f"  Actual level-set = {np.sum(mag > lam_fixed) * vol:.4f}")

    # Also do unconstrained comparison with N=3
    n_params3_uc = 6 * n_modes3

    def neg_ratio_fixed_lambda_uc(params, modes, grid_x, grid_y, grid_z, lam_fixed, dx):
        try:
            ux, uy, uz = params_to_field_unconstrained(params, modes, grid_x, grid_y, grid_z)
            mag = np.sqrt(ux**2 + uy**2 + uz**2)
            p = 10.0/3.0
            vol = dx**3
            Lp_p = np.sum(mag**p) * vol
            level_set = np.sum(mag > lam_fixed) * vol
            cheb = lam_fixed**(-p) * Lp_p
            if cheb < 1e-15:
                return 0.0
            return -level_set / cheb
        except:
            return 0.0

    print(f"\nUnconstrained comparison (N={N_freq3}, {n_params3_uc} params)...")
    best_ratio_uc3 = 0.0
    t0 = time.time()
    for trial in range(50):
        x0 = np.random.randn(n_params3_uc) * 2.0
        res = minimize(neg_ratio_fixed_lambda_uc, x0,
                       args=(modes3, grid_x, grid_y, grid_z, lam_fixed, dx),
                       method='Nelder-Mead',
                       options={'maxiter': 5000, 'xatol': 1e-6, 'fatol': 1e-8})
        ratio = -res.fun
        if ratio > best_ratio_uc3:
            best_ratio_uc3 = ratio
    t1 = time.time()
    print(f"  Best ratio (unconstrained, fixed λ={lam_fixed}): {best_ratio_uc3:.6f}  [{t1-t0:.1f}s]")
    print(f"\n  DF/UC ratio: {best_ratio_plateau / best_ratio_uc3:.4f}" if best_ratio_uc3 > 0 else "")

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
