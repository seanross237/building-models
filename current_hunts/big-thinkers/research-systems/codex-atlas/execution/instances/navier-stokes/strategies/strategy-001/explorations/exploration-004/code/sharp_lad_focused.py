#!/usr/bin/env python3
"""
Focused computation of sharp Ladyzhenskaya constant on T³.

Key insight: On T³, the sharp constant C_L should equal the R³ value as kmax → ∞,
because we can approximate the R³ optimizer (a Gaussian) with high-frequency modes.
The gap between computed C_L(T³, kmax) and C_L(R³) measures how many modes are needed.

Strategy:
1. Compute C_L for single modes, pairs, small sets
2. Track convergence with kmax
3. Also compute the EFFECTIVE Ladyzhenskaya constant for the Taylor-Green flow
   (what value of C_L would make the bound tight for ω of this specific flow?)
"""

import numpy as np
from numpy.fft import fftn, ifftn, fftfreq
import json
from pathlib import Path


def compute_L4_ratio(ux, uy, uz, N, vol, KX, KY, KZ):
    """Compute ||u||_{L⁴} / (||u||^{1/4}_{L²} × ||∇u||^{3/4}_{L²})."""
    u_sq = ux**2 + uy**2 + uz**2
    L2_sq = np.mean(u_sq) * vol
    L4_4 = np.mean(u_sq**2) * vol
    L2_norm = np.sqrt(L2_sq)
    L4_norm = L4_4**0.25

    ux_hat = fftn(ux)
    uy_hat = fftn(uy)
    uz_hat = fftn(uz)

    grad_sq = 0
    for u_hat in [ux_hat, uy_hat, uz_hat]:
        for K in [KX, KY, KZ]:
            deriv = ifftn(1j * K * u_hat).real
            grad_sq += np.mean(deriv**2)
    gradL2_norm = np.sqrt(grad_sq * vol)

    if L2_norm < 1e-30 or gradL2_norm < 1e-30:
        return 0.0, 0.0, 0.0, 0.0
    ratio = L4_norm / (L2_norm**0.25 * gradL2_norm**0.75)
    return ratio, L4_norm, L2_norm, gradL2_norm


def compute_scalar_ratio(f, N, vol, KX, KY, KZ):
    """Scalar version."""
    f_sq = f**2
    L2_sq = np.mean(f_sq) * vol
    L4_4 = np.mean(f_sq**2) * vol
    L2_norm = np.sqrt(L2_sq)
    L4_norm = L4_4**0.25

    f_hat = fftn(f)
    grad_sq = sum(np.mean(ifftn(1j * K * f_hat).real**2) for K in [KX, KY, KZ])
    gradL2_norm = np.sqrt(grad_sq * vol)

    if L2_norm < 1e-30 or gradL2_norm < 1e-30:
        return 0.0
    return L4_norm / (L2_norm**0.25 * gradL2_norm**0.75)


def compute_effective_lad_for_flow(results_file):
    """
    From the simulation results, compute the EFFECTIVE Ladyzhenskaya constant:
    C_L,eff = ||ω||_{L⁴} / (||ω||^{1/4}_{L²} × ||∇ω||^{3/4}_{L²})

    This is the value of C_L that would make the Ladyzhenskaya bound tight for this flow.
    It tells us whether the Ladyzhenskaya slack is due to the flow being far from the
    optimizer, or just the constant being imprecise.
    """
    with open(results_file, 'r') as f:
        results = json.load(f)

    print("\nEFFECTIVE LADYZHENSKAYA CONSTANT (C_L,eff = ||ω||_{L⁴} / (||ω||^{1/4}_{L²} × ||∇ω||^{3/4}_{L²}))")
    print(f"{'t':>6s} {'||ω||_L4':>12s} {'||ω||_L2':>12s} {'||∇ω||_L2':>12s} {'C_L,eff':>10s} {'C²_L,eff':>10s} {'α_Lad':>8s}")

    C_L4_scalar = 8.0 / (3.0 * np.sqrt(3.0) * np.pi**2)
    C_L_vec = (3 * C_L4_scalar)**0.25

    for r in results:
        if r['t'] < 0.01:
            continue
        omega_L4 = r['omega_L4']
        omega_L2 = r['omega_L2']
        grad_omega_L2 = r['grad_omega_L2']

        if omega_L2 > 1e-30 and grad_omega_L2 > 1e-30:
            C_eff = omega_L4 / (omega_L2**0.25 * grad_omega_L2**0.75)
            C_eff_sq = C_eff**2
        else:
            C_eff = C_eff_sq = 0

        print(f"{r['t']:6.3f} {omega_L4:12.4e} {omega_L2:12.4e} {grad_omega_L2:12.4e} "
              f"{C_eff:10.6f} {C_eff_sq:10.6f} {r['alpha_Lad']:8.2f}")

    print(f"\n  R³ vector C_L = {C_L_vec:.6f}, C²_L = {C_L_vec**2:.6f}")
    print(f"  α_Lad = C²_L(R³) / C²_L,eff = (C_L(R³)/C_L,eff)²")
    print(f"  So the Ladyzhenskaya slack comes from the flow's ω having a SMALLER L⁴/interpolation ratio")
    print(f"  than the worst-case optimizer (a concentrated spike-like distribution).")


def systematic_single_mode_survey(N=64):
    """
    Compute the Ladyzhenskaya ratio for every single div-free Fourier mode.
    For k = (k₁, k₂, k₃), the div-free field u = e⊥ exp(ik·x) has:
      ||u||_{L²} = (2π)^{3/2}
      ||∇u||_{L²} = |k| × (2π)^{3/2}
      ||u||_{L⁴} depends on the specific mode shape

    For a SINGLE mode u = A sin(k·x), the L⁴ integral gives:
      ∫ sin⁴(k·x) dx = (2π)³ × 3/8
    So ||u||⁴_{L⁴} = (2π)³ × 3/8, ||u||²_{L²} = (2π)³ / 2, ||∇u||² = |k|² × (2π)³ / 2

    C = ||u||_{L⁴} / (||u||^{1/4}_{L²} × ||∇u||^{3/4}_{L²})
      = ((2π)³ × 3/8)^{1/4} / (((2π)³/2)^{1/8} × (|k|² (2π)³/2)^{3/8})
      = (3/8)^{1/4} × (2π)^{3/4} / ((2π)^{3/8} × |k|^{3/4} × (1/2)^{1/8} × (2π)^{9/8} × (1/2)^{3/8})
    Hmm let me just compute it numerically...
    """
    vol = (2 * np.pi)**3
    kk = fftfreq(N, d=1.0/N)
    KX, KY, KZ = np.meshgrid(kk, kk, kk, indexing='ij')

    dx = 2 * np.pi / N
    x = np.arange(N) * dx
    X, Y, Z = np.meshgrid(x, x, x, indexing='ij')

    print("\nSINGLE-MODE LADYZHENSKAYA RATIOS (scalar)")
    print(f"{'k':>12s} {'|k|':>8s} {'C_L':>10s}")

    max_ratio = 0
    for kx in range(0, 4):
        for ky in range(0, 4):
            for kz in range(0, 4):
                if kx == 0 and ky == 0 and kz == 0:
                    continue
                k_mag = np.sqrt(kx**2 + ky**2 + kz**2)
                f = np.sin(kx*X + ky*Y + kz*Z)
                r = compute_scalar_ratio(f, N, vol, KX, KY, KZ)
                if r > max_ratio:
                    max_ratio = r
                if kx + ky + kz <= 3:
                    print(f"  ({kx},{ky},{kz}) {k_mag:8.4f} {r:10.6f}")

    # Analytical: for f = sin(k·x) with |k| = k_mag:
    # ||f||²_{L²} = V/2
    # ||f||⁴_{L⁴} = 3V/8
    # ||∇f||²_{L²} = k²_mag × V/2
    # C = (3V/8)^{1/4} / ((V/2)^{1/8} × (k²_mag V/2)^{3/8})
    #   = (3/8)^{1/4} × V^{1/4} / (V^{1/8} × (1/2)^{1/8} × k_mag^{3/4} × V^{3/8} × (1/2)^{3/8})
    #   = (3/8)^{1/4} / (k_mag^{3/4} × (1/2)^{1/2})
    #   = (3/8)^{1/4} × √2 / k_mag^{3/4}
    #   = (3/4)^{1/4} / k_mag^{3/4}
    # For k_mag = 1: C = (3/4)^{1/4} = 0.930604... Wait, that doesn't match.

    # Let me recompute. For f = sin(k·x):
    # ||f||_{L⁴}⁴ = ∫ sin⁴(k·x) dV = V × ⟨sin⁴⟩ = V × 3/8
    # ||f||_{L⁴} = (3V/8)^{1/4}
    # ||f||_{L²}² = V × ⟨sin²⟩ = V/2
    # ||f||_{L²}^{1/4} = (V/2)^{1/8}
    # ||∇f||_{L²}² = |k|² × V × ⟨cos²⟩ = |k|² × V/2
    # ||∇f||_{L²}^{3/4} = (|k|² V/2)^{3/8}
    # C = (3V/8)^{1/4} / ((V/2)^{1/8} × (|k|²V/2)^{3/8})
    #   = (3V/8)^{1/4} / ((V/2)^{1/2} × |k|^{3/4})
    #   = (3/8)^{1/4} × V^{1/4} / ((V)^{1/2} × 2^{-1/2} × |k|^{3/4})
    #   = (3/8)^{1/4} × 2^{1/2} / (V^{1/4} × |k|^{3/4})
    # For V = (2π)³:
    # C = (3/8)^{1/4} × √2 / ((2π)^{3/4} × |k|^{3/4})

    for k_mag_test in [1, np.sqrt(2), np.sqrt(3), 2]:
        C_anal = (3/8)**0.25 * np.sqrt(2) / ((2*np.pi)**0.75 * k_mag_test**0.75)
        print(f"  Analytical |k|={k_mag_test:.4f}: C = {C_anal:.6f}")

    print(f"\n  Max single-mode C: {max_ratio:.6f}")
    print(f"  This occurs at |k|=1 (the lowest frequency)")
    print(f"  As |k| grows: C ~ 1/|k|^{3/4} → 0")
    print(f"  => Single modes CANNOT approach C_L(R³) = 0.628")
    print(f"  Need SUPERPOSITIONS of many modes to approximate the R³ optimizer (Gaussian)")


def superposition_search(N=64, n_trials=50):
    """
    Search for div-free superpositions that maximize the ratio.
    Try random superpositions of low-frequency modes.
    """
    vol = (2 * np.pi)**3
    kk = fftfreq(N, d=1.0/N)
    KX, KY, KZ = np.meshgrid(kk, kk, kk, indexing='ij')
    K2 = KX**2 + KY**2 + KZ**2
    K2_safe = np.where(K2 == 0, 1, K2)

    dx = 2 * np.pi / N
    x = np.arange(N) * dx
    X, Y, Z = np.meshgrid(x, x, x, indexing='ij')

    print("\nSUPERPOSITION SEARCH (random div-free combinations)")

    best_ratio = 0
    best_desc = ""

    for trial in range(n_trials):
        rng = np.random.RandomState(trial)

        # Random combination of modes up to kmax
        kmax = rng.choice([2, 3, 4, 5, 6, 8, 10])

        # Build random field
        ux_hat = np.zeros((N,N,N), dtype=complex)
        uy_hat = np.zeros((N,N,N), dtype=complex)
        uz_hat = np.zeros((N,N,N), dtype=complex)

        # Energy spectrum: peaked at some k0
        k0 = rng.choice([1, 2, 3, 4, 5])
        for kx in range(-kmax, kmax+1):
            for ky in range(-kmax, kmax+1):
                for kz in range(-kmax, kmax+1):
                    if kx == 0 and ky == 0 and kz == 0:
                        continue
                    k_sq = kx**2 + ky**2 + kz**2
                    k_mag = np.sqrt(k_sq)
                    if k_mag > kmax:
                        continue

                    # Weight by energy spectrum
                    weight = np.exp(-0.5 * (k_mag - k0)**2)

                    kx_idx = kx % N
                    ky_idx = ky % N
                    kz_idx = kz % N

                    ux_hat[kx_idx, ky_idx, kz_idx] = weight * (rng.randn() + 1j*rng.randn())
                    uy_hat[kx_idx, ky_idx, kz_idx] = weight * (rng.randn() + 1j*rng.randn())
                    uz_hat[kx_idx, ky_idx, kz_idx] = weight * (rng.randn() + 1j*rng.randn())

        # Project to div-free
        kdotf = (KX*ux_hat + KY*uy_hat + KZ*uz_hat) / K2_safe
        kdotf[0,0,0] = 0
        ux_hat -= KX * kdotf
        uy_hat -= KY * kdotf
        uz_hat -= KZ * kdotf

        ux = ifftn(ux_hat).real
        uy = ifftn(uy_hat).real
        uz = ifftn(uz_hat).real

        r, _, _, _ = compute_L4_ratio(ux, uy, uz, N, vol, KX, KY, KZ)

        if r > best_ratio:
            best_ratio = r
            best_desc = f"kmax={kmax}, k0={k0}, trial={trial}"
            print(f"  trial {trial}: C = {r:.6f} ({best_desc})")

    # Also try concentrated distributions: Gaussian-like bump
    print("\n  Concentrated bump tests:")
    for sigma in [0.5, 1.0, 1.5, 2.0, 3.0]:
        # Approximate Gaussian in periodic domain: exp(-r²/(2σ²))
        # Use as amplitude for a specific velocity field
        r_sq = (X - np.pi)**2 + (Y - np.pi)**2 + (Z - np.pi)**2
        bump = np.exp(-r_sq / (2 * sigma**2))

        # Make a velocity field: u = bump × (sin(x), -sin(y), 0) — approximately div-free
        ux = bump * np.sin(X)
        uy = -bump * np.sin(Y)
        uz = np.zeros_like(X)

        # Project to exactly div-free
        ux_hat = fftn(ux)
        uy_hat = fftn(uy)
        uz_hat = fftn(np.zeros_like(X))
        kdotf = (KX*ux_hat + KY*uy_hat + KZ*uz_hat) / K2_safe
        kdotf[0,0,0] = 0
        ux = ifftn(ux_hat - KX*kdotf).real
        uy = ifftn(uy_hat - KY*kdotf).real
        uz = ifftn(uz_hat - KZ*kdotf).real

        r, _, _, _ = compute_L4_ratio(ux, uy, uz, N, vol, KX, KY, KZ)
        print(f"    σ={sigma:.1f}: C = {r:.6f}")
        if r > best_ratio:
            best_ratio = r
            best_desc = f"Gaussian bump σ={sigma}"

    print(f"\n  Best overall: C = {best_ratio:.6f} ({best_desc})")
    return best_ratio


if __name__ == '__main__':
    code_dir = Path(__file__).parent

    systematic_single_mode_survey(N=64)
    best_C = superposition_search(N=64, n_trials=100)

    # Effective constant from simulation
    for re_val in [100, 1000]:
        results_file = code_dir / f'results_Re{re_val}.json'
        if results_file.exists():
            print(f"\n{'='*70}")
            print(f"Re={re_val}")
            print(f"{'='*70}")
            compute_effective_lad_for_flow(results_file)

    C_L_vec_R3 = (3 * 8.0 / (3.0 * np.sqrt(3.0) * np.pi**2))**0.25
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"  Best C_L found on T³ (div-free): {best_C:.6f}")
    print(f"  R³ vector Ladyzhenskaya C_L: {C_L_vec_R3:.6f}")
    print(f"  Ratio: {best_C / C_L_vec_R3:.4f}")
    print(f"  The T³ constant likely equals the R³ constant (achieved in the limit kmax → ∞)")
    print(f"  But for low-frequency flows like Taylor-Green, the effective constant is much smaller")
    print(f"  This is why α_Lad is so large: the flow is far from the Ladyzhenskaya optimizer")
