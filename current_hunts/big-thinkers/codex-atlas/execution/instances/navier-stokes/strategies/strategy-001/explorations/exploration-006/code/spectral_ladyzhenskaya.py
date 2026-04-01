#!/usr/bin/env python3
"""
Spectral Ladyzhenskaya Inequality: Effective Constants for Spectrally Localized Fields

Computes C_{L,eff} = ||f||_{L⁴} / (||f||^{1/4}_{L²} * ||∇f||^{3/4}_{L²})
for various spectral profiles on T³ = [0, 2π]³.

Parts B1-B4 of Exploration 006.
"""

import numpy as np
from numpy.fft import fftn, ifftn, fftfreq
from scipy.optimize import minimize
import json
import time
import sys

# ============================================================================
# Constants
# ============================================================================

# Sharp Ladyzhenskaya constant on R³ (scalar)
# ||f||_{L⁴} ≤ C_L ||f||^{1/4}_{L²} ||∇f||^{3/4}_{L²}
# C_L⁴ = 8/(3√3 π²) for scalar, on R³
C_L4_scalar = 8.0 / (3.0 * np.sqrt(3.0) * np.pi**2)
C_L_SCALAR = C_L4_scalar ** 0.25  # ≈ 0.629

# For vector fields: C_L4_vec = 3 * C_L4_scalar, C_L_vec = (3 * C_L4_scalar)^{1/4}
C_L4_vec = 3.0 * C_L4_scalar
C_L_VEC = C_L4_vec ** 0.25  # ≈ 0.839

# We use scalar C_L here since we're testing scalar fields first
# The GOAL.md mentions C_L = 0.827 (close to vector value)
# We'll report ratios relative to both
C_L_REF = 0.827  # Value from GOAL.md

print(f"Reference constants: C_L_scalar = {C_L_SCALAR:.6f}, C_L_vec = {C_L_VEC:.6f}, C_L_ref = {C_L_REF:.6f}")


# ============================================================================
# Helper Functions
# ============================================================================

def setup_wavenumber_grid(N):
    """Set up wavenumber grid for T³ = [0, 2π]³ with N³ points."""
    k = fftfreq(N, d=1.0/N)  # wavenumbers: 0,1,...,N/2,-N/2+1,...,-1
    KX, KY, KZ = np.meshgrid(k, k, k, indexing='ij')
    K2 = KX**2 + KY**2 + KZ**2
    K_mag = np.sqrt(K2)
    return KX, KY, KZ, K2, K_mag


def compute_lady_ratio(f_hat, K2, N):
    """
    Compute the Ladyzhenskaya ratio for a scalar field with given Fourier coefficients.

    Returns C_{L,eff} = ||f||_{L⁴} / (||f||^{1/4}_{L²} * ||∇f||^{3/4}_{L²})

    Norms on T³ = [0, 2π]³:
    - ||f||²_{L²} = (2π)³ Σ|f̂_k|² (Parseval)
    - ||∇f||²_{L²} = (2π)³ Σ|k|²|f̂_k|²
    - ||f||⁴_{L⁴} = (2π)³ × (1/N³) Σ_x |f(x)|⁴ ... wait

    Actually, with FFT conventions: if f̂_k = (1/N³) Σ_x f(x) e^{-ik·x},
    then f(x) = Σ_k f̂_k e^{ik·x}, and:
    - ||f||²_{L²} = (1/(2π)³) ∫|f|² dx = Σ|f̂_k|² (Parseval on T³)

    But numpy's fftn uses: F_k = Σ_x f_x e^{-2πi k·x/N}
    with inverse: f_x = (1/N³) Σ_k F_k e^{2πi k·x/N}

    For T³ = [0, 2π]³ with grid spacing dx = 2π/N:
    - f(x_j) = f_j, where x_j = (2π/N) * j
    - f̂_k = (1/N³) * Σ_j f_j e^{-ik·x_j} = (1/N³) * F_k
      where F_k = np.fft.fftn(f)(k) = Σ_j f_j e^{-2πi (k·j)/N}
      and we use wavenumber vectors k (integers), x_j = (2π/N)*j
      so e^{-ik·x_j} = e^{-i(2π/N)(k·j)} = e^{-2πi(k·j)/N}

    So f̂_k = F_k / N³ and:
    - ||f||²_{L²} = (1/(2π)³) ∫|f|² dx ≈ (1/(2π)³) * (2π/N)³ * Σ|f_j|² = (1/N³) Σ|f_j|²
    - Also by Parseval: = Σ|f̂_k|² = (1/N⁶) Σ|F_k|² = (1/N³) * (1/N³) Σ|F_k|²

    Actually let me simplify. I'll work directly with:
    - f_hat[k] = the Fourier coefficient (NOT the FFT output)
    - f(x) = Σ_k f_hat[k] e^{ik·x}

    Then on T³ = [0,2π]³:
    - ||f||²_{L²} = (2π)³ Σ|f_hat[k]|²   (Plancherel with measure dx/(2π)³... no)

    Let me be precise. On T³ = [0,2π]³ with Lebesgue measure:
    ∫_{T³} |f|² dx = (2π)³ Σ_k |f̂_k|²

    where f̂_k = (1/(2π)³) ∫ f(x) e^{-ik·x} dx, f(x) = Σ_k f̂_k e^{ik·x}.

    Alternatively, with the convention f(x) = Σ_k c_k e^{ik·x} and
    c_k = (1/(2π)³) ∫ f e^{-ik·x} dx, we get ∫|f|² dx = (2π)³ Σ|c_k|².

    For simplicity, I'll define things so that:
    - L² norm: ||f||²_{L²} = (1/(2π)³) ∫|f|² dx = Σ|c_k|²
    - H¹ norm: ||∇f||²_{L²} = (1/(2π)³) ∫|∇f|² dx = Σ|k|²|c_k|²
    - L⁴ norm: ||f||⁴_{L⁴} = (1/(2π)³) ∫|f|⁴ dx

    This gives the Ladyzhenskaya inequality with the same constant as R³ (for large wavenumbers).

    Implementation: I'll build f(x) from coefficients on the grid, compute norms numerically.
    """
    # Build physical-space field from Fourier coefficients
    # f_hat is an N³ array of Fourier coefficients c_k
    # f(x_j) = Σ_k c_k e^{ik·x_j} with x_j = (2π/N)*j
    # Using FFT: f_j = Σ_k c_k e^{i(2π/N)(k·j)} if we identify wavenumber indices correctly
    # numpy's ifft: f_j = (1/N³) Σ_k F_k e^{2πi k·j/N}
    # So F_k = N³ * c_k gives f_j = Σ_k c_k e^{2πi k·j/N} ✓

    F_k = N**3 * f_hat
    f_phys = ifftn(F_k).real

    # L² norm (with 1/(2π)³ normalization)
    L2_sq = np.sum(np.abs(f_hat)**2)

    # H¹ seminorm
    H1_sq = np.sum(K2 * np.abs(f_hat)**2)

    # L⁴ norm (numerical integration)
    # ||f||⁴_{L⁴} = (1/(2π)³) ∫|f|⁴ dx ≈ (1/(2π)³) × (2π/N)³ × Σ|f_j|⁴ = (1/N³) Σ|f_j|⁴
    L4_fourth = np.mean(f_phys**4)

    L2 = np.sqrt(L2_sq)
    H1 = np.sqrt(H1_sq)
    L4 = L4_fourth**0.25

    if L2 < 1e-15 or H1 < 1e-15:
        return 0.0

    C_eff = L4 / (L2**0.25 * H1**0.75)
    return C_eff, L2, H1, L4


def compute_lady_ratio_vector(f_hat_components, K2, N):
    """
    Compute Ladyzhenskaya ratio for a divergence-free vector field.
    f_hat_components = (f_hat_x, f_hat_y, f_hat_z), each N³ arrays.

    ||u||²_{L²} = Σ_i ||u_i||²_{L²}
    ||∇u||²_{L²} = Σ_i ||∇u_i||²_{L²}
    ||u||⁴_{L⁴} = (1/(2π)³) ∫ |u|⁴ dx
    """
    fx_hat, fy_hat, fz_hat = f_hat_components

    F_x = N**3 * fx_hat
    F_y = N**3 * fy_hat
    F_z = N**3 * fz_hat

    fx_phys = ifftn(F_x).real
    fy_phys = ifftn(F_y).real
    fz_phys = ifftn(F_z).real

    # Norms
    L2_sq = np.sum(np.abs(fx_hat)**2) + np.sum(np.abs(fy_hat)**2) + np.sum(np.abs(fz_hat)**2)
    H1_sq = np.sum(K2 * np.abs(fx_hat)**2) + np.sum(K2 * np.abs(fy_hat)**2) + np.sum(K2 * np.abs(fz_hat)**2)

    # |u|⁴ = (u_x² + u_y² + u_z²)²
    u_sq = fx_phys**2 + fy_phys**2 + fz_phys**2
    L4_fourth = np.mean(u_sq**2)

    L2 = np.sqrt(L2_sq)
    H1 = np.sqrt(H1_sq)
    L4 = L4_fourth**0.25

    if L2 < 1e-15 or H1 < 1e-15:
        return 0.0, 0, 0, 0

    C_eff = L4 / (L2**0.25 * H1**0.75)
    return C_eff, L2, H1, L4


# ============================================================================
# Part B1: Band-Limited Fields
# ============================================================================

def compute_bandlimited(N, k0, n_optimize=20, n_random=200):
    """
    For fields with Fourier support in [k0/2, 2*k0], find the maximum
    Ladyzhenskaya ratio by optimizing over phases.

    Returns: (max_C_eff, mean_C_eff, std_C_eff) from optimization and random sampling.
    """
    KX, KY, KZ, K2, K_mag = setup_wavenumber_grid(N)

    # Band mask: |k| in [k0/2, 2*k0]
    band_mask = (K_mag >= k0/2) & (K_mag <= 2*k0) & (K_mag > 0)
    n_modes = np.sum(band_mask)
    print(f"  k0={k0}: {n_modes} modes in band [{k0/2}, {2*k0}]")

    if n_modes == 0:
        return 0, 0, 0

    # Indices of active modes
    active_indices = np.where(band_mask.ravel())[0]

    # Random sampling first
    ratios_random = []
    for _ in range(n_random):
        # Random phases, unit amplitudes normalized
        phases = np.random.uniform(0, 2*np.pi, n_modes)
        f_hat = np.zeros(N**3, dtype=complex)
        f_hat[active_indices] = np.exp(1j * phases) / np.sqrt(n_modes)
        f_hat = f_hat.reshape((N, N, N))

        result = compute_lady_ratio(f_hat, K2, N)
        if isinstance(result, tuple):
            ratios_random.append(result[0])

    mean_random = np.mean(ratios_random)
    std_random = np.std(ratios_random)

    # Optimization: maximize C_eff over phases
    best_C = 0.0
    K2_flat = K2.ravel()

    def neg_lady_ratio(phases_vec):
        """Negative of Ladyzhenskaya ratio (for minimization)."""
        f_hat = np.zeros(N**3, dtype=complex)
        f_hat[active_indices] = np.exp(1j * phases_vec) / np.sqrt(n_modes)
        f_hat = f_hat.reshape((N, N, N))

        F_k = N**3 * f_hat
        f_phys = ifftn(F_k).real

        L2_sq = np.sum(np.abs(f_hat)**2)
        H1_sq = np.sum(K2 * np.abs(f_hat)**2)
        L4_fourth = np.mean(f_phys**4)

        L2 = np.sqrt(L2_sq)
        H1 = np.sqrt(H1_sq)
        L4 = L4_fourth**0.25

        if L2 < 1e-15 or H1 < 1e-15:
            return 0.0
        return -(L4 / (L2**0.25 * H1**0.75))

    # Limit optimization dimensions for tractability
    if n_modes > 500:
        # Too many modes for full optimization; subsample
        # and use random phases for the rest
        n_opt_modes = min(n_modes, 200)
        print(f"  (optimizing {n_opt_modes} of {n_modes} phases)")
        opt_indices = np.random.choice(n_modes, n_opt_modes, replace=False)

        for trial in range(n_optimize):
            base_phases = np.random.uniform(0, 2*np.pi, n_modes)

            def neg_ratio_partial(opt_phases):
                all_phases = base_phases.copy()
                all_phases[opt_indices] = opt_phases
                f_hat = np.zeros(N**3, dtype=complex)
                f_hat[active_indices] = np.exp(1j * all_phases) / np.sqrt(n_modes)
                f_hat = f_hat.reshape((N, N, N))

                F_k = N**3 * f_hat
                f_phys = ifftn(F_k).real

                L2_sq = np.sum(np.abs(f_hat)**2)
                H1_sq = np.sum(K2 * np.abs(f_hat)**2)
                L4_fourth = np.mean(f_phys**4)

                L2 = np.sqrt(L2_sq)
                H1 = np.sqrt(H1_sq)
                L4 = L4_fourth**0.25

                if L2 < 1e-15 or H1 < 1e-15:
                    return 0.0
                return -(L4 / (L2**0.25 * H1**0.75))

            x0 = base_phases[opt_indices]
            res = minimize(neg_ratio_partial, x0, method='L-BFGS-B',
                          options={'maxiter': 100, 'ftol': 1e-10})
            C_trial = -res.fun
            if C_trial > best_C:
                best_C = C_trial
    else:
        for trial in range(n_optimize):
            x0 = np.random.uniform(0, 2*np.pi, n_modes)
            res = minimize(neg_lady_ratio, x0, method='L-BFGS-B',
                          options={'maxiter': 200, 'ftol': 1e-10})
            C_trial = -res.fun
            if C_trial > best_C:
                best_C = C_trial

    return best_C, mean_random, std_random


# ============================================================================
# Part B2: Power-Law Spectra
# ============================================================================

def compute_powerlaw(N, alpha, n_samples=500, k_max_factor=0.4):
    """
    Power-law spectrum: |f̂_k| ~ |k|^{-α} for 1 ≤ |k| ≤ k_max.
    Random phases. Compute distribution of C_{L,eff}.

    α = 5/6 corresponds to Kolmogorov E(k) ~ k^{-5/3} since E(k) ~ k² |f̂_k|²
    and k² × k^{-2α} = k^{2-2α}, so E(k) ~ k^{2-2α} = k^{-5/3} => α = 11/6.
    Wait: E(k) ~ k^{-5/3} means Σ_{|k'|~k} |û_{k'}|² ~ k^{-5/3}.
    The number of modes at shell k is ~ k², so |û_k|² ~ k^{-5/3}/k² = k^{-11/3},
    meaning |û_k| ~ k^{-11/6}.

    So for Kolmogorov: α = 11/6 ≈ 1.833 (amplitude decay exponent).
    The GOAL says α = 5/6 for Kolmogorov, which may be using E(k) ~ |f̂_k|²
    (without the shell counting factor). Let me follow the GOAL's convention.

    Actually re-reading the GOAL: "f̂_k ~ |k|^{-α} × e^{iφ_k}" and
    "α = 5/6 (corresponds to E(k)~k^{-5/3} Kolmogorov spectrum)"

    If E(k) = Σ_{|k'|∈[k,k+1]} |f̂_{k'}|² ≈ (# modes at k) × |k|^{-2α} ≈ k² × k^{-2α}
    Then E(k) ~ k^{2-2α} = k^{-5/3} => 2-2α = -5/3 => α = 11/6

    But the goal says α = 5/6. Perhaps they define E(k) differently (as |f̂_k|² directly
    without shell counting)? Or perhaps they define f̂_k such that the spectral energy
    density (per unit k) is |f̂_k|². Let me just follow the goal's convention:
    α = 5/6, 1, 3/2 as stated.
    """
    KX, KY, KZ, K2, K_mag = setup_wavenumber_grid(N)

    k_max = int(k_max_factor * N)
    active_mask = (K_mag >= 1) & (K_mag <= k_max)
    n_modes = np.sum(active_mask)
    active_indices = np.where(active_mask.ravel())[0]
    K_mag_active = K_mag.ravel()[active_indices]

    # Amplitude envelope: |f̂_k| = |k|^{-α}, normalized so ||f|| = 1
    amplitudes = K_mag_active ** (-alpha)

    ratios = []
    for _ in range(n_samples):
        phases = np.random.uniform(0, 2*np.pi, n_modes)
        f_hat_flat = np.zeros(N**3, dtype=complex)
        f_hat_flat[active_indices] = amplitudes * np.exp(1j * phases)
        f_hat = f_hat_flat.reshape((N, N, N))

        # Normalize to unit L² norm
        L2_sq = np.sum(np.abs(f_hat)**2)
        f_hat /= np.sqrt(L2_sq)

        result = compute_lady_ratio(f_hat, K2, N)
        if isinstance(result, tuple):
            ratios.append(result[0])

    return np.mean(ratios), np.std(ratios), np.max(ratios), np.min(ratios)


# ============================================================================
# Part B3: Divergence-Free Fields
# ============================================================================

def compute_divfree_bandlimited(N, k0, n_samples=300, n_optimize=10):
    """
    Divergence-free band-limited vector fields.
    For each k, the velocity û_k must satisfy k · û_k = 0.
    This restricts to a 2D subspace perpendicular to k.
    """
    KX, KY, KZ, K2, K_mag = setup_wavenumber_grid(N)

    band_mask = (K_mag >= k0/2) & (K_mag <= 2*k0) & (K_mag > 0)
    n_modes = np.sum(band_mask)
    print(f"  Div-free k0={k0}: {n_modes} modes in band")

    if n_modes == 0:
        return 0, 0, 0, 0

    active_indices = np.where(band_mask.ravel())[0]
    kx_active = KX.ravel()[active_indices]
    ky_active = KY.ravel()[active_indices]
    kz_active = KZ.ravel()[active_indices]
    k_mag_active = K_mag.ravel()[active_indices]

    # For each mode k, compute two orthonormal vectors perpendicular to k
    # These span the divergence-free subspace at that wavenumber
    e1 = np.zeros((n_modes, 3))
    e2 = np.zeros((n_modes, 3))

    for i in range(n_modes):
        k_vec = np.array([kx_active[i], ky_active[i], kz_active[i]])
        k_norm = k_mag_active[i]
        k_hat = k_vec / k_norm

        # Find a vector not parallel to k
        if abs(k_hat[0]) < 0.9:
            v = np.array([1, 0, 0])
        else:
            v = np.array([0, 1, 0])

        # Gram-Schmidt
        e1_i = v - np.dot(v, k_hat) * k_hat
        e1_i /= np.linalg.norm(e1_i)
        e2_i = np.cross(k_hat, e1_i)

        e1[i] = e1_i
        e2[i] = e2_i

    # Random sampling
    ratios = []
    for _ in range(n_samples):
        # Random complex coefficients in the div-free subspace
        c1 = np.random.randn(n_modes) + 1j * np.random.randn(n_modes)
        c2 = np.random.randn(n_modes) + 1j * np.random.randn(n_modes)

        # Build vector field components
        fx_hat = np.zeros(N**3, dtype=complex)
        fy_hat = np.zeros(N**3, dtype=complex)
        fz_hat = np.zeros(N**3, dtype=complex)

        for comp in range(3):
            vals = c1 * e1[:, comp] + c2 * e2[:, comp]
            if comp == 0:
                fx_hat[active_indices] = vals
            elif comp == 1:
                fy_hat[active_indices] = vals
            else:
                fz_hat[active_indices] = vals

        fx_hat = fx_hat.reshape((N, N, N))
        fy_hat = fy_hat.reshape((N, N, N))
        fz_hat = fz_hat.reshape((N, N, N))

        # Normalize
        L2_sq = np.sum(np.abs(fx_hat)**2) + np.sum(np.abs(fy_hat)**2) + np.sum(np.abs(fz_hat)**2)
        norm = np.sqrt(L2_sq)
        fx_hat /= norm
        fy_hat /= norm
        fz_hat /= norm

        result = compute_lady_ratio_vector((fx_hat, fy_hat, fz_hat), K2, N)
        ratios.append(result[0])

    # Also compute scalar C_eff for same band (for comparison)
    scalar_ratios = []
    for _ in range(n_samples):
        phases = np.random.uniform(0, 2*np.pi, n_modes)
        f_hat = np.zeros(N**3, dtype=complex)
        f_hat[active_indices] = np.exp(1j * phases) / np.sqrt(n_modes)
        f_hat = f_hat.reshape((N, N, N))
        result = compute_lady_ratio(f_hat, K2, N)
        if isinstance(result, tuple):
            scalar_ratios.append(result[0])

    return np.mean(ratios), np.std(ratios), np.mean(scalar_ratios), np.std(scalar_ratios)


# ============================================================================
# Part B4: NS Solution (Kolmogorov-like) Spectra
# ============================================================================

def compute_ns_spectrum(N, Re=1000, n_samples=300):
    """
    Simulate NS-like spectrum: E(k) ~ k^{-5/3} in inertial range, with
    dissipation cutoff at k_d ~ Re^{3/4}.

    Energy spectrum model:
    E(k) = C_K * ε^{2/3} * k^{-5/3} * exp(-c*(k/k_d)^{4/3})

    For simplicity, we set C_K * ε^{2/3} = 1 and k_d = Re^{3/4}.
    """
    KX, KY, KZ, K2, K_mag = setup_wavenumber_grid(N)

    k_d = Re**0.75  # dissipation wavenumber
    k_max = int(0.4 * N)

    active_mask = (K_mag >= 1) & (K_mag <= k_max)
    n_modes = np.sum(active_mask)
    active_indices = np.where(active_mask.ravel())[0]
    K_mag_active = K_mag.ravel()[active_indices]

    # Amplitude from energy spectrum
    # E(k) = k² × |f̂_k|² × (# modes at k) / k ≈ k² × |f̂_k|² × k²
    # More carefully: energy at wavenumber k is E(k) = (1/2) Σ_{|k'|~k} |û_{k'}|²
    # The spectral density per mode is E(k) / (4πk²) ~ k^{-5/3} / k² = k^{-11/3}
    # So |û_k|² ~ k^{-11/3} and |û_k| ~ k^{-11/6}
    # With dissipation: |û_k| ~ k^{-11/6} exp(-c*(k/k_d)^{4/3}/2)

    amplitudes = K_mag_active ** (-11.0/6.0) * np.exp(-0.5 * (K_mag_active / k_d) ** (4.0/3.0))

    ratios = []
    for _ in range(n_samples):
        phases = np.random.uniform(0, 2*np.pi, n_modes)
        f_hat_flat = np.zeros(N**3, dtype=complex)
        f_hat_flat[active_indices] = amplitudes * np.exp(1j * phases)
        f_hat = f_hat_flat.reshape((N, N, N))

        L2_sq = np.sum(np.abs(f_hat)**2)
        f_hat /= np.sqrt(L2_sq)

        result = compute_lady_ratio(f_hat, K2, N)
        if isinstance(result, tuple):
            ratios.append(result[0])

    return np.mean(ratios), np.std(ratios), np.max(ratios), np.min(ratios)


# ============================================================================
# Main
# ============================================================================

def main():
    results = {}

    # Use N=32 for fast computation, then verify key results at N=64
    N = 32
    print(f"\n{'='*70}")
    print(f"SPECTRAL LADYZHENSKAYA COMPUTATION (N={N})")
    print(f"{'='*70}")

    # ------------------------------------------------------------------
    # B1: Band-limited fields
    # ------------------------------------------------------------------
    print(f"\n--- Part B1: Band-Limited Fields ---")
    k0_values = [2, 4, 8, 12]
    b1_results = {}

    for k0 in k0_values:
        t0 = time.time()
        best_C, mean_C, std_C = compute_bandlimited(N, k0, n_optimize=15, n_random=300)
        dt = time.time() - t0
        print(f"  k0={k0}: max C_eff={best_C:.6f}, mean={mean_C:.6f}±{std_C:.6f} ({dt:.1f}s)")
        print(f"    Ratio to C_L_ref: max={best_C/C_L_REF:.4f}, mean={mean_C/C_L_REF:.4f}")
        b1_results[k0] = {
            'max_C_eff': best_C,
            'mean_C_eff': mean_C,
            'std_C_eff': std_C,
            'ratio_max': best_C / C_L_REF,
            'ratio_mean': mean_C / C_L_REF,
        }

    results['B1_bandlimited'] = b1_results

    # ------------------------------------------------------------------
    # B2: Power-law spectra
    # ------------------------------------------------------------------
    print(f"\n--- Part B2: Power-Law Spectra ---")
    alpha_values = [5.0/6.0, 1.0, 3.0/2.0, 11.0/6.0]
    b2_results = {}

    for alpha in alpha_values:
        t0 = time.time()
        mean_C, std_C, max_C, min_C = compute_powerlaw(N, alpha, n_samples=500)
        dt = time.time() - t0
        print(f"  α={alpha:.4f}: mean C_eff={mean_C:.6f}±{std_C:.6f}, max={max_C:.6f}, min={min_C:.6f} ({dt:.1f}s)")
        print(f"    Ratio to C_L_ref: mean={mean_C/C_L_REF:.4f}, max={max_C/C_L_REF:.4f}")
        b2_results[alpha] = {
            'mean_C_eff': mean_C,
            'std_C_eff': std_C,
            'max_C_eff': max_C,
            'min_C_eff': min_C,
            'ratio_mean': mean_C / C_L_REF,
            'ratio_max': max_C / C_L_REF,
        }

    results['B2_powerlaw'] = b2_results

    # ------------------------------------------------------------------
    # B3: Divergence-free vs. general
    # ------------------------------------------------------------------
    print(f"\n--- Part B3: Divergence-Free vs. General ---")
    k0_divfree = [4, 8]
    b3_results = {}

    for k0 in k0_divfree:
        t0 = time.time()
        mean_divfree, std_divfree, mean_scalar, std_scalar = compute_divfree_bandlimited(
            N, k0, n_samples=200, n_optimize=5)
        dt = time.time() - t0
        print(f"  k0={k0}: div-free mean={mean_divfree:.6f}±{std_divfree:.6f}, scalar mean={mean_scalar:.6f}±{std_scalar:.6f} ({dt:.1f}s)")
        print(f"    Ratio divfree/scalar: {mean_divfree/mean_scalar:.4f}")
        b3_results[k0] = {
            'mean_divfree': mean_divfree,
            'std_divfree': std_divfree,
            'mean_scalar': mean_scalar,
            'std_scalar': std_scalar,
            'ratio_divfree_scalar': mean_divfree / mean_scalar if mean_scalar > 0 else 0,
        }

    results['B3_divfree'] = b3_results

    # ------------------------------------------------------------------
    # B4: NS-like spectra
    # ------------------------------------------------------------------
    print(f"\n--- Part B4: NS-Like Spectra ---")
    Re_values = [100, 1000, 10000]
    b4_results = {}

    for Re in Re_values:
        t0 = time.time()
        mean_C, std_C, max_C, min_C = compute_ns_spectrum(N, Re=Re, n_samples=500)
        dt = time.time() - t0
        print(f"  Re={Re}: mean C_eff={mean_C:.6f}±{std_C:.6f}, max={max_C:.6f} ({dt:.1f}s)")
        print(f"    Ratio to C_L_ref: mean={mean_C/C_L_REF:.4f}")
        b4_results[Re] = {
            'mean_C_eff': mean_C,
            'std_C_eff': std_C,
            'max_C_eff': max_C,
            'min_C_eff': min_C,
            'ratio_mean': mean_C / C_L_REF,
        }

    results['B4_ns_spectrum'] = b4_results

    # ------------------------------------------------------------------
    # Verification at higher resolution
    # ------------------------------------------------------------------
    print(f"\n--- Verification at N=64 ---")
    N_check = 64
    KX64, KY64, KZ64, K264, K_mag64 = setup_wavenumber_grid(N_check)

    # Check one band-limited case
    k0_check = 4
    best_C_64, mean_C_64, std_C_64 = compute_bandlimited(N_check, k0_check, n_optimize=5, n_random=100)
    print(f"  N=64, k0={k0_check}: max C_eff={best_C_64:.6f}, mean={mean_C_64:.6f}")
    print(f"  N=32 value was: max={b1_results[k0_check]['max_C_eff']:.6f}, mean={b1_results[k0_check]['mean_C_eff']:.6f}")

    # Check power-law
    mean_C_64_pl, std_64_pl, max_64_pl, _ = compute_powerlaw(N_check, 11.0/6.0, n_samples=200)
    print(f"  N=64, α=11/6: mean C_eff={mean_C_64_pl:.6f}")
    print(f"  N=32 value was: mean={b2_results[11.0/6.0]['mean_C_eff']:.6f}")

    results['verification'] = {
        'N64_k0_4_max': best_C_64,
        'N64_k0_4_mean': mean_C_64,
        'N64_alpha_11_6_mean': mean_C_64_pl,
    }

    # Save results
    # Convert numpy types for JSON
    def convert(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, dict):
            return {str(k): convert(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [convert(v) for v in obj]
        return obj

    with open('results_partB.json', 'w') as f:
        json.dump(convert(results), f, indent=2)

    print(f"\n{'='*70}")
    print("Results saved to results_partB.json")
    print(f"{'='*70}")

    return results


if __name__ == '__main__':
    main()
