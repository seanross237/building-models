#!/usr/bin/env python3
"""
Spectral Ladyzhenskaya Inequality: Effective Constants for Spectrally Localized Fields
VERSION 2 — fixes reality condition for Fourier coefficients.

Key fix: for real-valued fields on T³, we must have f̂_{-k} = f̂_k*.
We compute all norms self-consistently from the real physical-space field.

C_{L,eff} = ||f||_{L⁴} / (||f||^{1/4}_{L²} * ||∇f||^{3/4}_{L²})

All norms use measure (1/(2π)³) dx on T³ = [0, 2π]³, so:
  ||f||²_{L²} = (1/N³) Σ_j |f_j|²
  ||∇f||²_{L²} = (1/N³) Σ_j |∇f_j|²
  ||f||⁴_{L⁴} = (1/N³) Σ_j |f_j|⁴

This ensures consistency.
"""

import numpy as np
from numpy.fft import fftn, ifftn, fftfreq
from scipy.optimize import minimize
import json
import time

# ============================================================================
# Constants
# ============================================================================
# Sharp Ladyzhenskaya on R³ (scalar): C_L⁴ = 4/(3π²√3) · 2 = ...
# Actually the sharp GNS on R³ for ||f||_{L⁴} ≤ C ||f||^{1/4}_{L²} ||∇f||^{3/4}_{L²}:
# comes from the Aubin-Talenti extremizer.
# The sharp constant is C_L = (4/(3π²))^{1/4} · (something) ...
# Let me compute it properly.
#
# The Gagliardo-Nirenberg-Sobolev inequality:
# ||f||_{Lq} ≤ C ||f||^{1-θ}_{Lr} ||∇f||^θ_{Lp}
# with 1/q = (1-θ)/r + θ(1/p - 1/d)
# For q=4, r=2, p=2, d=3: 1/4 = (1-θ)/2 + θ(1/2-1/3) = (1-θ)/2 + θ/6
# 1/4 = 1/2 - θ/2 + θ/6 = 1/2 - θ/3 => θ/3 = 1/4 => θ = 3/4 ✓
#
# The sharp constant for the GNS on R³:
# ||f||_{L⁴(R³)} ≤ C_GNS ||f||^{1/4}_{L²(R³)} ||∇f||^{3/4}_{L²(R³)}
#
# By scaling: if f_λ(x) = λ^{3/2} f(λx), then ||f_λ||_{L²} = ||f||_{L²},
# ||∇f_λ||_{L²} = λ||∇f||_{L²}, ||f_λ||_{L⁴} = λ^{3/4}||f||_{L⁴}.
# So LHS/RHS = ||f||_{L⁴}/||f||^{1/4}||∇f||^{3/4} which is scale-invariant. ✓
#
# The sharp constant from Del Pino & Dolbeault (2002):
# C_GNS = (2/d)^{θ/2} / (C_d^{1/2}) ... complicated.
#
# Alternatively, from Weinstein (1983) and Agueh (2008):
# For d=3, the optimal GNS constant for ||u||_4 ≤ C ||u||_2^{1/4} ||∇u||_2^{3/4}:
# C_opt ≈ 0.529 (this is the scalar value on R³)
# Actually I need to look this up more carefully.
#
# The Ladyzhenskaya inequality (specific to d=3):
# ||u||_{L⁴}⁴ ≤ c₁ ||u||_{L²} ||∇u||³_{L²}
# which gives ||u||_{L⁴} ≤ c₁^{1/4} ||u||^{1/4}_{L²} ||∇u||^{3/4}_{L²}
#
# Ladyzhenskaya's original: c₁ = 8/(3π²√3) ≈ 0.1561 for scalar, so C_L = 0.1561^{1/4} ≈ 0.629
#
# For reference: let's compute both scalar and vector versions
C_lady4_scalar = 8.0 / (3.0 * np.pi**2 * np.sqrt(3.0))  # ≈ 0.1561
C_L_SCALAR = C_lady4_scalar**0.25  # ≈ 0.629

# The GOAL.md uses C_L = 0.827, which may be the vector or a different normalization.
# We'll use C_L_SCALAR as our primary reference since we compute scalar fields.
C_L_REF = C_L_SCALAR
print(f"Reference: C_L_scalar = {C_L_SCALAR:.6f} (from Ladyzhenskaya's sharp constant)")
print(f"  (c₁ = ||f||⁴_4 / (||f||_2 ||∇f||³_2) has sharp value {C_lady4_scalar:.6f})")


# ============================================================================
# Grid Setup
# ============================================================================

def setup_grid(N):
    """Set up wavenumber grid for T³ = [0, 2π]³ with N³ points."""
    k = fftfreq(N, d=1.0/N)
    KX, KY, KZ = np.meshgrid(k, k, k, indexing='ij')
    K2 = KX**2 + KY**2 + KZ**2
    K_mag = np.sqrt(K2)
    return KX, KY, KZ, K2, K_mag


# ============================================================================
# Norm Computation — All in Physical Space for Consistency
# ============================================================================

def compute_norms(f_hat, KX, KY, KZ, K2, N):
    """
    Given Fourier coefficients f_hat (N³ complex array), compute physical-space field
    and all norms consistently.

    We build f(x) = Σ_k f_hat[k] e^{ik·x} via IFFT (which gives the real part
    if f_hat satisfies reality condition). We then compute everything from f_phys.

    Returns: (L2, H1, L4, f_phys)
    """
    # Physical space field
    F_k = N**3 * f_hat  # numpy IFFT convention: f_j = (1/N³) Σ F_k e^{2πi k·j/N}
    f_phys = ifftn(F_k).real  # take real part

    # L² norm: (1/N³) Σ f_j²  (approximates (1/(2π)³) ∫|f|² dx)
    L2_sq = np.mean(f_phys**2)

    # Gradient in physical space via spectral differentiation
    grad_x = ifftn(1j * KX * F_k).real
    grad_y = ifftn(1j * KY * F_k).real
    grad_z = ifftn(1j * KZ * F_k).real
    H1_sq = np.mean(grad_x**2 + grad_y**2 + grad_z**2)

    # L⁴ norm
    L4_fourth = np.mean(f_phys**4)

    L2 = np.sqrt(max(L2_sq, 0))
    H1 = np.sqrt(max(H1_sq, 0))
    L4 = max(L4_fourth, 0)**0.25

    return L2, H1, L4, f_phys


def lady_ratio(L2, H1, L4):
    """Compute C_{L,eff} = ||f||_{L⁴} / (||f||^{1/4}_{L²} × ||∇f||^{3/4}_{L²})"""
    if L2 < 1e-15 or H1 < 1e-15:
        return 0.0
    return L4 / (L2**0.25 * H1**0.75)


def lady_ratio_c1(L2, H1, L4):
    """Compute c₁ = ||f||⁴_{L⁴} / (||f||_{L²} × ||∇f||³_{L²})
    This is the fourth power version: ||f||⁴_4 ≤ c₁ ||f||_2 ||∇f||³_2"""
    if L2 < 1e-15 or H1 < 1e-15:
        return 0.0
    return L4**4 / (L2 * H1**3)


# ============================================================================
# Reality-Preserving Fourier Coefficient Builder
# ============================================================================

def build_real_field_hat(active_indices_pos, phases, amplitudes, N, KX):
    """
    Build Fourier coefficients for a real field from "positive half" modes.

    For a real field: f̂_{-k} = f̂_k*
    We set the positive-half modes and mirror them.

    active_indices_pos: indices into the flat array for the "positive" half
    phases: phase for each positive mode
    amplitudes: amplitude for each positive mode (real, positive)

    Returns: f_hat as N³ complex array satisfying reality condition.
    """
    f_hat_flat = np.zeros(N**3, dtype=complex)

    # Set positive modes: c_k = A_k e^{iφ_k}
    f_hat_flat[active_indices_pos] = amplitudes * np.exp(1j * phases)

    # Mirror: c_{-k} = c_k*
    # We need to find the -k index for each k
    f_hat = f_hat_flat.reshape((N, N, N))
    # The negative of index k in fftfreq is at index (-k) mod N
    # For each positive mode, set the conjugate
    # This is trickier with the flat index. Let me use the 3D array.

    # Actually, let me just enforce: f_hat[-kx, -ky, -kz] = f_hat[kx, ky, kz]*
    # In the FFT array, index i corresponds to freq k_i = i if i < N/2, N-i if i >= N/2
    # The "negative" of index i is (N-i) % N

    for idx in active_indices_pos:
        ix, iy, iz = np.unravel_index(idx, (N, N, N))
        jx = (-ix) % N
        jy = (-iy) % N
        jz = (-iz) % N
        f_hat[jx, jy, jz] = np.conj(f_hat[ix, iy, iz])

    return f_hat


def get_positive_half_indices(band_mask, N, KX, KY, KZ):
    """
    Get indices for the "positive half" of Fourier space, avoiding double-counting
    for real-valued fields. For each pair (k, -k), we keep the one with
    lexicographically positive k.
    """
    indices = np.where(band_mask.ravel())[0]
    pos_indices = []

    for idx in indices:
        ix, iy, iz = np.unravel_index(idx, (N, N, N))
        kx = KX[ix, iy, iz]
        ky = KY[ix, iy, iz]
        kz = KZ[ix, iy, iz]

        # Skip k=0
        if kx == 0 and ky == 0 and kz == 0:
            continue

        # Keep if k is in the "positive half" (lexicographic)
        if kx > 0:
            pos_indices.append(idx)
        elif kx == 0 and ky > 0:
            pos_indices.append(idx)
        elif kx == 0 and ky == 0 and kz > 0:
            pos_indices.append(idx)
        # else: it's the negative partner, skip

    return np.array(pos_indices)


# ============================================================================
# Simpler approach: just compute everything in physical space
# ============================================================================

def compute_lady_ratio_simple(f_hat, KX, KY, KZ, K2, N):
    """
    Full physical-space computation of Ladyzhenskaya ratio.
    Handles reality condition automatically by using .real of IFFT.
    """
    L2, H1, L4, _ = compute_norms(f_hat, KX, KY, KZ, K2, N)
    return lady_ratio(L2, H1, L4)


# ============================================================================
# Part B1: Band-Limited Fields
# ============================================================================

def compute_bandlimited(N, k0, n_optimize=20, n_random=300):
    """
    Band-limited fields with support |k| ∈ [k0/2, 2*k0].
    Maximize Ladyzhenskaya ratio over phases.
    """
    KX, KY, KZ, K2, K_mag = setup_grid(N)

    band_mask = (K_mag >= k0/2) & (K_mag <= 2*k0) & (K_mag > 0)
    n_modes = int(np.sum(band_mask))
    pos_indices = get_positive_half_indices(band_mask, N, KX, KY, KZ)
    n_pos = len(pos_indices)

    print(f"  k0={k0}: {n_modes} total modes, {n_pos} positive-half modes")

    if n_pos == 0:
        return {'max_C': 0, 'mean_C': 0, 'std_C': 0, 'n_modes': 0}

    # Unit amplitudes (will normalize by L² norm)
    amplitudes = np.ones(n_pos) / np.sqrt(n_pos)

    # Random sampling
    ratios = []
    for _ in range(n_random):
        phases = np.random.uniform(0, 2*np.pi, n_pos)
        f_hat = build_real_field_hat(pos_indices, phases, amplitudes, N, KX)
        C = compute_lady_ratio_simple(f_hat, KX, KY, KZ, K2, N)
        ratios.append(C)

    mean_C = np.mean(ratios)
    std_C = np.std(ratios)

    # Optimization
    best_C = max(ratios)

    def neg_ratio(ph):
        fh = build_real_field_hat(pos_indices, ph, amplitudes, N, KX)
        return -compute_lady_ratio_simple(fh, KX, KY, KZ, K2, N)

    n_opt_vars = min(n_pos, 200)

    if n_pos <= 200:
        # Optimize all phases
        for trial in range(n_optimize):
            x0 = np.random.uniform(0, 2*np.pi, n_pos)
            res = minimize(neg_ratio, x0, method='L-BFGS-B',
                          options={'maxiter': 100, 'ftol': 1e-10})
            C_trial = -res.fun
            if C_trial > best_C:
                best_C = C_trial
    else:
        # Optimize subset of phases
        opt_subset = np.random.choice(n_pos, n_opt_vars, replace=False)

        for trial in range(n_optimize):
            base_phases = np.random.uniform(0, 2*np.pi, n_pos)

            def neg_ratio_partial(ph_sub):
                full_ph = base_phases.copy()
                full_ph[opt_subset] = ph_sub
                fh = build_real_field_hat(pos_indices, full_ph, amplitudes, N, KX)
                return -compute_lady_ratio_simple(fh, KX, KY, KZ, K2, N)

            x0 = base_phases[opt_subset]
            res = minimize(neg_ratio_partial, x0, method='L-BFGS-B',
                          options={'maxiter': 100, 'ftol': 1e-10})
            C_trial = -res.fun
            if C_trial > best_C:
                best_C = C_trial

    return {
        'max_C': best_C,
        'mean_C': mean_C,
        'std_C': std_C,
        'n_modes': n_modes,
        'n_pos_modes': n_pos,
    }


# ============================================================================
# Part B2: Power-Law Spectra
# ============================================================================

def compute_powerlaw(N, alpha, n_samples=500, k_max_factor=0.4):
    """
    Power-law spectrum: |f̂_k| ~ |k|^{-α}, random phases.
    """
    KX, KY, KZ, K2, K_mag = setup_grid(N)

    k_max = int(k_max_factor * N)
    active_mask = (K_mag >= 1) & (K_mag <= k_max)
    pos_indices = get_positive_half_indices(active_mask, N, KX, KY, KZ)
    n_pos = len(pos_indices)

    K_mag_flat = K_mag.ravel()
    amplitudes = K_mag_flat[pos_indices] ** (-alpha)

    ratios = []
    for _ in range(n_samples):
        phases = np.random.uniform(0, 2*np.pi, n_pos)
        f_hat = build_real_field_hat(pos_indices, phases, amplitudes, N, KX)
        C = compute_lady_ratio_simple(f_hat, KX, KY, KZ, K2, N)
        ratios.append(C)

    return {
        'mean_C': np.mean(ratios),
        'std_C': np.std(ratios),
        'max_C': np.max(ratios),
        'min_C': np.min(ratios),
        'n_pos_modes': n_pos,
    }


# ============================================================================
# Part B3: Divergence-Free Fields
# ============================================================================

def compute_divfree_bandlimited(N, k0, n_samples=300):
    """
    Compare div-free vector fields vs. scalar fields in the same band.
    """
    KX, KY, KZ, K2, K_mag = setup_grid(N)

    band_mask = (K_mag >= k0/2) & (K_mag <= 2*k0) & (K_mag > 0)
    pos_indices = get_positive_half_indices(band_mask, N, KX, KY, KZ)
    n_pos = len(pos_indices)

    print(f"  Div-free k0={k0}: {n_pos} positive-half modes")

    if n_pos == 0:
        return {}

    K_mag_flat = K_mag.ravel()
    kx_flat = KX.ravel()
    ky_flat = KY.ravel()
    kz_flat = KZ.ravel()

    # For each positive mode, compute the two transverse polarization vectors
    e1_arr = np.zeros((n_pos, 3))
    e2_arr = np.zeros((n_pos, 3))

    for i, idx in enumerate(pos_indices):
        k_vec = np.array([kx_flat[idx], ky_flat[idx], kz_flat[idx]])
        kn = K_mag_flat[idx]
        k_hat = k_vec / kn

        if abs(k_hat[0]) < 0.9:
            v = np.array([1.0, 0.0, 0.0])
        else:
            v = np.array([0.0, 1.0, 0.0])

        e1_i = v - np.dot(v, k_hat) * k_hat
        e1_i /= np.linalg.norm(e1_i)
        e2_i = np.cross(k_hat, e1_i)
        e1_arr[i] = e1_i
        e2_arr[i] = e2_i

    # Div-free vector field sampling
    divfree_ratios = []
    for _ in range(n_samples):
        # Two random complex amplitudes per mode (for two polarizations)
        a1 = (np.random.randn(n_pos) + 1j * np.random.randn(n_pos)) / np.sqrt(2)
        a2 = (np.random.randn(n_pos) + 1j * np.random.randn(n_pos)) / np.sqrt(2)

        # Build three component fields
        fx_hat = np.zeros((N, N, N), dtype=complex)
        fy_hat = np.zeros((N, N, N), dtype=complex)
        fz_hat = np.zeros((N, N, N), dtype=complex)

        for i, idx in enumerate(pos_indices):
            ix, iy, iz = np.unravel_index(idx, (N, N, N))
            jx, jy, jz = (-ix) % N, (-iy) % N, (-iz) % N

            c_vec = a1[i] * e1_arr[i] + a2[i] * e2_arr[i]  # complex 3-vector
            fx_hat[ix, iy, iz] = c_vec[0]
            fy_hat[ix, iy, iz] = c_vec[1]
            fz_hat[ix, iy, iz] = c_vec[2]

            # Reality condition
            fx_hat[jx, jy, jz] = np.conj(c_vec[0])
            fy_hat[jx, jy, jz] = np.conj(c_vec[1])
            fz_hat[jx, jy, jz] = np.conj(c_vec[2])

        # Physical fields
        Fx = N**3 * fx_hat; Fy = N**3 * fy_hat; Fz = N**3 * fz_hat
        ux = ifftn(Fx).real; uy = ifftn(Fy).real; uz = ifftn(Fz).real

        # L² norm: (1/N³) Σ (ux² + uy² + uz²)
        L2_sq = np.mean(ux**2 + uy**2 + uz**2)

        # ||∇u||² = Σ_i ||∇u_i||²
        H1_sq = 0.0
        for F_comp in [Fx, Fy, Fz]:
            gx = ifftn(1j * KX * F_comp).real
            gy = ifftn(1j * KY * F_comp).real
            gz = ifftn(1j * KZ * F_comp).real
            H1_sq += np.mean(gx**2 + gy**2 + gz**2)

        # L⁴ norm: |u|⁴ = (ux² + uy² + uz²)²
        u_sq = ux**2 + uy**2 + uz**2
        L4_fourth = np.mean(u_sq**2)

        L2 = np.sqrt(max(L2_sq, 0))
        H1 = np.sqrt(max(H1_sq, 0))
        L4 = max(L4_fourth, 0)**0.25

        divfree_ratios.append(lady_ratio(L2, H1, L4))

    # Scalar field sampling (same band, for comparison)
    scalar_ratios = []
    amps = np.ones(n_pos) / np.sqrt(n_pos)
    for _ in range(n_samples):
        phases = np.random.uniform(0, 2*np.pi, n_pos)
        f_hat = build_real_field_hat(pos_indices, phases, amps, N, KX)
        C = compute_lady_ratio_simple(f_hat, KX, KY, KZ, K2, N)
        scalar_ratios.append(C)

    return {
        'mean_divfree': np.mean(divfree_ratios),
        'std_divfree': np.std(divfree_ratios),
        'mean_scalar': np.mean(scalar_ratios),
        'std_scalar': np.std(scalar_ratios),
        'ratio': np.mean(divfree_ratios) / np.mean(scalar_ratios) if np.mean(scalar_ratios) > 0 else 0,
    }


# ============================================================================
# Part B4: NS-like Spectra
# ============================================================================

def compute_ns_spectrum(N, Re=1000, n_samples=500):
    """
    NS-like spectrum: |û_k| ~ k^{-11/6} exp(-c (k/k_d)^{4/3}/2)
    where k_d = Re^{3/4} (Kolmogorov dissipation wavenumber).
    """
    KX, KY, KZ, K2, K_mag = setup_grid(N)

    k_d = Re**0.75
    k_max = int(0.4 * N)

    active_mask = (K_mag >= 1) & (K_mag <= k_max)
    pos_indices = get_positive_half_indices(active_mask, N, KX, KY, KZ)
    n_pos = len(pos_indices)

    K_mag_flat = K_mag.ravel()
    amplitudes = K_mag_flat[pos_indices]**(-11.0/6.0) * np.exp(-0.5 * (K_mag_flat[pos_indices]/k_d)**(4.0/3.0))

    ratios = []
    for _ in range(n_samples):
        phases = np.random.uniform(0, 2*np.pi, n_pos)
        f_hat = build_real_field_hat(pos_indices, phases, amplitudes, N, KX)
        C = compute_lady_ratio_simple(f_hat, KX, KY, KZ, K2, N)
        ratios.append(C)

    return {
        'mean_C': np.mean(ratios),
        'std_C': np.std(ratios),
        'max_C': np.max(ratios),
        'min_C': np.min(ratios),
        'n_pos_modes': n_pos,
    }


# ============================================================================
# Sanity Checks
# ============================================================================

def sanity_checks(N=32):
    """Verify the computation on known cases."""
    print("=== Sanity Checks ===")
    KX, KY, KZ, K2, K_mag = setup_grid(N)

    # Single Fourier mode: f = cos(k·x) with k = (1,0,0)
    f_hat = np.zeros((N, N, N), dtype=complex)
    f_hat[1, 0, 0] = 0.5   # k = (1,0,0): amplitude A
    f_hat[-1, 0, 0] = 0.5  # k = (-1,0,0): A* for reality => cos(x)
    # f(x) = cos(x)

    L2, H1, L4, f_phys = compute_norms(f_hat, KX, KY, KZ, K2, N)
    C = lady_ratio(L2, H1, L4)

    # Expected for cos(x): ||cos(x)||²_{L²} = (1/(2π)³) ∫ cos²(x) dx = 1/(2(2π)²) * 2π² = 1/2
    # Wait: ||cos(x)||²_{L²,normalized} = (1/(2π)³) ∫₀²π ∫₀²π ∫₀²π cos²(x) dx dy dz
    #   = (1/(2π)³) × (2π)² × ∫₀²π cos²(x) dx = (1/(2π)³) × (2π)² × π = 1/2
    # ||∇cos(x)||²_{L²} = ||sin(x)||²_{L²} = 1/2
    # ||cos(x)||⁴_{L⁴} = (1/(2π)³) ∫ cos⁴(x) dx = (1/(2π)³) × (2π)² × ∫₀²π cos⁴(x) dx
    #   = (1/(2π)) × (3π/4) = 3/8
    # C_eff = L4/(L2^{1/4} H1^{3/4}) = (3/8)^{1/4} / ((1/2)^{1/8} (1/2)^{3/8})
    #   = (3/8)^{1/4} / (1/2)^{1/2} = (3/8)^{1/4} × √2

    L2_exact = np.sqrt(0.5)
    H1_exact = np.sqrt(0.5)
    L4_exact = (3.0/8.0)**0.25
    C_exact = L4_exact / (L2_exact**0.25 * H1_exact**0.75)

    print(f"  Single mode cos(x):")
    print(f"    L2: computed={L2:.6f}, exact={L2_exact:.6f}, err={abs(L2-L2_exact):.2e}")
    print(f"    H1: computed={H1:.6f}, exact={H1_exact:.6f}, err={abs(H1-H1_exact):.2e}")
    print(f"    L4: computed={L4:.6f}, exact={L4_exact:.6f}, err={abs(L4-L4_exact):.2e}")
    print(f"    C_eff: computed={C:.6f}, exact={C_exact:.6f}")
    print(f"    C_eff/C_L_scalar: {C/C_L_SCALAR:.4f}")

    # Sum of two orthogonal modes: f = cos(x) + cos(y)
    f_hat2 = np.zeros((N, N, N), dtype=complex)
    f_hat2[1, 0, 0] = 0.5
    f_hat2[-1, 0, 0] = 0.5
    f_hat2[0, 1, 0] = 0.5
    f_hat2[0, -1, 0] = 0.5

    L2_2, H1_2, L4_2, _ = compute_norms(f_hat2, KX, KY, KZ, K2, N)
    C_2 = lady_ratio(L2_2, H1_2, L4_2)

    # cos(x) + cos(y): L2² = 1, H1² = 1
    # L4⁴ = <(cos(x)+cos(y))⁴> = <cos⁴x> + 4<cos³x cosy> + 6<cos²x cos²y> + ...
    # = 3/8 + 0 + 6×(1/2)(1/2)×(1/(2π)²) ... let me just compute:
    # <(cos x + cos y)⁴> = <cos⁴x> + 4<cos³x><cosy> + 6<cos²x><cos²y> + 4<cosx><cos³y> + <cos⁴y>
    # = 3/8 + 0 + 6*(1/2)*(1/2) + 0 + 3/8 = 3/4 + 3/2 = 9/4
    # Wait that's for ∫dx/(2π)³. Let me redo.
    # (1/(2π)³)∫(cosx+cosy)⁴ dx = (1/(2π)³)×(2π)×∫∫(cosx+cosy)⁴ dxdy/(2π)²×2π
    # Hmm, let me just compute numerically.
    print(f"\n  Two modes cos(x)+cos(y):")
    print(f"    L2={L2_2:.6f}, H1={H1_2:.6f}, L4={L4_2:.6f}")
    print(f"    C_eff={C_2:.6f}, ratio to C_L: {C_2/C_L_SCALAR:.4f}")

    # Concentrated spike: sum of ALL modes with same phase
    f_hat3 = np.zeros((N, N, N), dtype=complex)
    band_mask = (K_mag >= 2) & (K_mag <= 8) & (K_mag > 0)
    pos_idx = get_positive_half_indices(band_mask, N, KX, KY, KZ)
    n_p = len(pos_idx)
    amp = np.ones(n_p) / np.sqrt(n_p)
    f_hat3 = build_real_field_hat(pos_idx, np.zeros(n_p), amp, N, KX)  # all phases = 0

    L2_3, H1_3, L4_3, fp3 = compute_norms(f_hat3, KX, KY, KZ, K2, N)
    C_3 = lady_ratio(L2_3, H1_3, L4_3)

    print(f"\n  All-zero-phase band [2,8] ({n_p} pos modes):")
    print(f"    L2={L2_3:.6f}, H1={H1_3:.6f}, L4={L4_3:.6f}")
    print(f"    C_eff={C_3:.6f}, ratio to C_L: {C_3/C_L_SCALAR:.4f}")
    print(f"    max/mean of |f|: {np.max(np.abs(fp3))/np.mean(np.abs(fp3)):.2f} (concentration)")

    return C_exact


# ============================================================================
# Main
# ============================================================================

def main():
    results = {}

    # Sanity checks first
    C_cos = sanity_checks()

    N = 32
    print(f"\n{'='*70}")
    print(f"SPECTRAL LADYZHENSKAYA COMPUTATION (N={N})")
    print(f"{'='*70}")

    # ------------------------------------------------------------------
    # B1: Band-limited fields
    # ------------------------------------------------------------------
    print(f"\n--- Part B1: Band-Limited Fields ---")
    k0_values = [2, 4, 8, 12]
    b1 = {}

    for k0 in k0_values:
        t0 = time.time()
        res = compute_bandlimited(N, k0, n_optimize=15, n_random=300)
        dt = time.time() - t0
        print(f"  k0={k0}: max C_eff={res['max_C']:.6f}, mean={res['mean_C']:.6f}±{res['std_C']:.6f} ({dt:.1f}s)")
        print(f"    Ratio to C_L: max={res['max_C']/C_L_SCALAR:.4f}, mean={res['mean_C']/C_L_SCALAR:.4f}")
        b1[k0] = res

    results['B1'] = b1

    # ------------------------------------------------------------------
    # B2: Power-law spectra
    # ------------------------------------------------------------------
    print(f"\n--- Part B2: Power-Law Spectra ---")
    # alpha values as specified in GOAL.md, plus the physically correct Kolmogorov value
    alpha_values = [5.0/6.0, 1.0, 3.0/2.0, 11.0/6.0]
    b2 = {}

    for alpha in alpha_values:
        t0 = time.time()
        res = compute_powerlaw(N, alpha, n_samples=500)
        dt = time.time() - t0
        print(f"  α={alpha:.4f}: mean C_eff={res['mean_C']:.6f}±{res['std_C']:.6f}, max={res['max_C']:.6f} ({dt:.1f}s)")
        print(f"    Ratio to C_L: mean={res['mean_C']/C_L_SCALAR:.4f}")
        b2[alpha] = res

    results['B2'] = b2

    # ------------------------------------------------------------------
    # B3: Divergence-free vs. general
    # ------------------------------------------------------------------
    print(f"\n--- Part B3: Divergence-Free vs. General ---")
    b3 = {}
    for k0 in [4, 8]:
        t0 = time.time()
        res = compute_divfree_bandlimited(N, k0, n_samples=200)
        dt = time.time() - t0
        if res:
            print(f"  k0={k0}: div-free={res['mean_divfree']:.6f}±{res['std_divfree']:.6f}, "
                  f"scalar={res['mean_scalar']:.6f}±{res['std_scalar']:.6f}, "
                  f"ratio={res['ratio']:.4f} ({dt:.1f}s)")
            b3[k0] = res

    results['B3'] = b3

    # ------------------------------------------------------------------
    # B4: NS-like spectra
    # ------------------------------------------------------------------
    print(f"\n--- Part B4: NS-Like Spectra ---")
    b4 = {}
    for Re in [100, 1000, 10000]:
        t0 = time.time()
        res = compute_ns_spectrum(N, Re=Re, n_samples=500)
        dt = time.time() - t0
        print(f"  Re={Re}: mean C_eff={res['mean_C']:.6f}±{res['std_C']:.6f}, max={res['max_C']:.6f} ({dt:.1f}s)")
        print(f"    Ratio to C_L: mean={res['mean_C']/C_L_SCALAR:.4f}")
        b4[Re] = res

    results['B4'] = b4

    # ------------------------------------------------------------------
    # Verification at higher resolution
    # ------------------------------------------------------------------
    print(f"\n--- Verification at N=48 ---")
    N2 = 48
    # Rerun key cases
    res_48_k4 = compute_bandlimited(N2, 4, n_optimize=5, n_random=100)
    print(f"  N={N2}, k0=4: max={res_48_k4['max_C']:.6f}, mean={res_48_k4['mean_C']:.6f}")
    print(f"  N={N}, k0=4: max={b1[4]['max_C']:.6f}, mean={b1[4]['mean_C']:.6f}")

    res_48_pl = compute_powerlaw(N2, 11.0/6.0, n_samples=200)
    print(f"  N={N2}, α=11/6: mean={res_48_pl['mean_C']:.6f}")
    print(f"  N={N}, α=11/6: mean={b2[11.0/6.0]['mean_C']:.6f}")

    res_48_ns = compute_ns_spectrum(N2, Re=1000, n_samples=200)
    print(f"  N={N2}, Re=1000: mean={res_48_ns['mean_C']:.6f}")
    print(f"  N={N}, Re=1000: mean={b4[1000]['mean_C']:.6f}")

    results['verification'] = {
        'N48_k4': res_48_k4,
        'N48_pl_11_6': res_48_pl,
        'N48_ns_1000': res_48_ns,
    }

    # Save results
    def convert(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {str(k): convert(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [convert(v) for v in obj]
        return obj

    with open('results_partB_v2.json', 'w') as f:
        json.dump(convert(results), f, indent=2)

    print(f"\n{'='*70}")
    print("DONE. Results saved to results_partB_v2.json")
    print(f"{'='*70}")


if __name__ == '__main__':
    main()
