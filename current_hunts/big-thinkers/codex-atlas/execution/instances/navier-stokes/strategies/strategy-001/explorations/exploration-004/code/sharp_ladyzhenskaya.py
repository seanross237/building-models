#!/usr/bin/env python3
"""
Compute the sharp Ladyzhenskaya constant on T³ restricted to divergence-free fields.

Uses manual gradient-free optimization (Nelder-Mead from scratch) to avoid scipy dependency.
"""

import numpy as np
from numpy.fft import fftn, ifftn, fftfreq


def nelder_mead(func, x0, maxiter=5000, tol=1e-10):
    """Minimal Nelder-Mead implementation."""
    n = len(x0)
    alpha, gamma, rho, sigma = 1.0, 2.0, 0.5, 0.5

    # Initialize simplex
    simplex = np.zeros((n+1, n))
    simplex[0] = x0
    for i in range(n):
        simplex[i+1] = x0.copy()
        simplex[i+1][i] += 0.05 * (1.0 + abs(x0[i]))

    values = np.array([func(simplex[i]) for i in range(n+1)])

    for iteration in range(maxiter):
        order = np.argsort(values)
        simplex = simplex[order]
        values = values[order]

        if np.std(values) < tol:
            break

        centroid = np.mean(simplex[:-1], axis=0)
        xr = centroid + alpha * (centroid - simplex[-1])
        fr = func(xr)

        if fr < values[0]:
            xe = centroid + gamma * (xr - centroid)
            fe = func(xe)
            if fe < fr:
                simplex[-1] = xe
                values[-1] = fe
            else:
                simplex[-1] = xr
                values[-1] = fr
        elif fr < values[-2]:
            simplex[-1] = xr
            values[-1] = fr
        else:
            if fr < values[-1]:
                xc = centroid + rho * (xr - centroid)
            else:
                xc = centroid + rho * (simplex[-1] - centroid)
            fc = func(xc)
            if fc < values[-1]:
                simplex[-1] = xc
                values[-1] = fc
            else:
                for i in range(1, n+1):
                    simplex[i] = simplex[0] + sigma * (simplex[i] - simplex[0])
                    values[i] = func(simplex[i])

    best_idx = np.argmin(values)
    return simplex[best_idx], values[best_idx]


def compute_L4_ratio_from_fields(ux, uy, uz, N, vol, KX, KY, KZ):
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
        return 0.0
    return L4_norm / (L2_norm**0.25 * gradL2_norm**0.75)


def try_known_maximizers(N=64):
    """Test known candidate maximizers."""
    vol = (2 * np.pi)**3
    dx = 2 * np.pi / N
    x = np.arange(N) * dx
    X, Y, Z = np.meshgrid(x, x, x, indexing='ij')

    kk = fftfreq(N, d=1.0/N)
    KX, KY, KZ = np.meshgrid(kk, kk, kk, indexing='ij')

    print("="*60)
    print("KNOWN MAXIMIZER CANDIDATES")
    print("="*60)

    # 1. Single mode k=(1,0,0), e=(0,1,0) — div-free
    ux = np.zeros_like(X)
    uy = np.sin(X)
    uz = np.zeros_like(X)
    r = compute_L4_ratio_from_fields(ux, uy, uz, N, vol, KX, KY, KZ)
    print(f"  Single mode sin(x)ey: C = {r:.6f}")

    # Scalar single mode
    f = np.sin(X)
    f_sq = f**2
    fL2 = np.sqrt(np.mean(f_sq) * vol)
    fL4 = (np.mean(f_sq**2) * vol)**0.25
    f_hat = fftn(f)
    fgrad_sq = sum(np.mean(ifftn(1j * K * f_hat).real**2) for K in [KX, KY, KZ])
    fgradL2 = np.sqrt(fgrad_sq * vol)
    r_scalar = fL4 / (fL2**0.25 * fgradL2**0.75)
    print(f"  Scalar sin(x): C = {r_scalar:.6f}")

    # Analytical: for f = sin(x), ||f||² = (2π)³/2 = 4π³, ||∇f||² = (2π)³/2 = 4π³
    # ||f||⁴ = ∫sin⁴(x) dx = (2π)³ × 3/8, so ||f||_4 = ((2π)³ × 3/8)^{1/4}
    # Ratio = ((2π)³ × 3/8)^{1/4} / ((4π³)^{1/8} × (4π³)^{3/8})
    #       = ((2π)³ × 3/8)^{1/4} / (4π³)^{1/2}
    #       = (3/8)^{1/4} × (2π)^{3/4} / (4π³)^{1/2}
    #       = (3/8)^{1/4} × (2π)^{3/4} / (2π^{3/2})
    #       = (3/8)^{1/4} × 2^{3/4} × π^{3/4} / (2 × π^{3/2})
    #       = (3/8)^{1/4} × 2^{-1/4} × π^{-3/4}
    #       = (3/16)^{1/4} × π^{-3/4}
    vol_check = (2*np.pi)**3
    L2_sq_analytical = vol_check / 2
    L4_4_analytical = vol_check * 3 / 8
    gradL2_sq_analytical = vol_check / 2
    r_analytical = L4_4_analytical**0.25 / (L2_sq_analytical**(1/8) * gradL2_sq_analytical**(3/8))
    print(f"  Scalar sin(x) analytical: C = {r_analytical:.6f}")

    # 2. Taylor-Green vortex — div-free
    ux = np.sin(X) * np.cos(Y) * np.cos(Z)
    uy = -np.cos(X) * np.sin(Y) * np.cos(Z)
    uz = np.zeros_like(X)
    r = compute_L4_ratio_from_fields(ux, uy, uz, N, vol, KX, KY, KZ)
    print(f"  Taylor-Green: C = {r:.6f}")

    # 3. ABC flow — div-free (Beltrami, ω = u)
    ux = np.sin(Z) + np.cos(Y)
    uy = np.sin(X) + np.cos(Z)
    uz = np.sin(Y) + np.cos(X)
    r = compute_L4_ratio_from_fields(ux, uy, uz, N, vol, KX, KY, KZ)
    print(f"  ABC flow (A=B=C=1): C = {r:.6f}")

    # 4. Single mode k=(1,1,0), e=(0,0,1)
    ux = np.zeros_like(X)
    uy = np.zeros_like(X)
    uz = np.sin(X + Y)
    r = compute_L4_ratio_from_fields(ux, uy, uz, N, vol, KX, KY, KZ)
    print(f"  Mode k=(1,1,0)ez: C = {r:.6f}")

    # 5. Two orthogonal modes: sin(x)ey + sin(y)ex — this is NOT div-free
    # Project it
    ux = np.sin(Y)
    uy = np.sin(X)
    uz = np.zeros_like(X)
    K2 = KX**2 + KY**2 + KZ**2
    K2_safe = np.where(K2 == 0, 1, K2)
    ux_hat = fftn(ux); uy_hat = fftn(uy); uz_hat = fftn(np.zeros_like(X))
    kdotf = (KX*ux_hat + KY*uy_hat + KZ*uz_hat) / K2_safe
    kdotf[0,0,0] = 0
    ux = ifftn(ux_hat - KX*kdotf).real
    uy = ifftn(uy_hat - KY*kdotf).real
    uz = ifftn(uz_hat - KZ*kdotf).real
    r = compute_L4_ratio_from_fields(ux, uy, uz, N, vol, KX, KY, KZ)
    print(f"  Two-mode (projected): C = {r:.6f}")

    # 6. Concentrated vortex tube (Gaussian approximation in Fourier)
    # Not attempted — too many modes needed

    C_L4_scalar = 8.0 / (3.0 * np.sqrt(3.0) * np.pi**2)
    C_L_scalar_R3 = C_L4_scalar ** 0.25
    C_L_vec_R3 = (3 * C_L4_scalar)**0.25
    print(f"\n  Reference R³ scalar C_L = {C_L_scalar_R3:.6f}")
    print(f"  Reference R³ vector C_L = {C_L_vec_R3:.6f}")

    return r_scalar  # for comparison


def generate_modes(kmax):
    """Generate div-free mode basis."""
    modes = []
    for kx in range(-kmax, kmax+1):
        for ky in range(-kmax, kmax+1):
            for kz in range(-kmax, kmax+1):
                if kx == 0 and ky == 0 and kz == 0:
                    continue
                k = np.array([kx, ky, kz], dtype=float)
                k_hat = k / np.linalg.norm(k)

                if abs(k_hat[0]) < 0.9:
                    v = np.array([1, 0, 0], dtype=float)
                else:
                    v = np.array([0, 1, 0], dtype=float)

                e1 = v - np.dot(v, k_hat) * k_hat
                e1 /= np.linalg.norm(e1)
                e2 = np.cross(k_hat, e1)
                e2 /= np.linalg.norm(e2)

                modes.append((k, e1, e2))
    return modes


def build_field(coeffs, modes, N):
    """Build physical-space div-free field from mode coefficients."""
    ux_hat = np.zeros((N, N, N), dtype=complex)
    uy_hat = np.zeros((N, N, N), dtype=complex)
    uz_hat = np.zeros((N, N, N), dtype=complex)

    for i, (k, e1, e2) in enumerate(modes):
        a = coeffs[2*i]
        b = coeffs[2*i + 1]
        u_k = a * e1 + b * e2

        kx_idx = int(k[0]) % N
        ky_idx = int(k[1]) % N
        kz_idx = int(k[2]) % N

        ux_hat[kx_idx, ky_idx, kz_idx] = u_k[0]
        uy_hat[kx_idx, ky_idx, kz_idx] = u_k[1]
        uz_hat[kx_idx, ky_idx, kz_idx] = u_k[2]

    ux = ifftn(ux_hat).real
    uy = ifftn(uy_hat).real
    uz = ifftn(uz_hat).real
    return ux, uy, uz


def neg_ratio(coeffs, modes, N, vol, KX, KY, KZ):
    """Negative of L⁴ ratio for minimization."""
    ux, uy, uz = build_field(coeffs, modes, N)
    return -compute_L4_ratio_from_fields(ux, uy, uz, N, vol, KX, KY, KZ)


def optimize_divfree_constant(kmax, N=None, n_restarts=20):
    """Find sharp C_L for div-free fields via Nelder-Mead."""
    if N is None:
        N = max(4 * kmax + 4, 16)

    vol = (2 * np.pi)**3
    kk = fftfreq(N, d=1.0/N)
    KX, KY, KZ = np.meshgrid(kk, kk, kk, indexing='ij')

    modes = generate_modes(kmax)
    n_params = 2 * len(modes)
    print(f"\nkmax={kmax}: {len(modes)} modes, {n_params} params, N={N}")

    best_ratio = 0.0
    best_coeffs = None

    for restart in range(n_restarts):
        np.random.seed(restart * 137 + 42)
        x0 = np.random.randn(n_params)
        x0 /= np.linalg.norm(x0)

        def obj(c):
            return neg_ratio(c, modes, N, vol, KX, KY, KZ)

        xbest, fbest = nelder_mead(obj, x0, maxiter=3000, tol=1e-10)
        ratio = -fbest

        if ratio > best_ratio:
            best_ratio = ratio
            best_coeffs = xbest
            print(f"  restart {restart:2d}: C = {ratio:.6f} (new best)")

    # Second pass with perturbations around best
    if best_coeffs is not None:
        for trial in range(10):
            np.random.seed(1000 + trial)
            x0 = best_coeffs + 0.1 * np.random.randn(n_params)

            def obj(c):
                return neg_ratio(c, modes, N, vol, KX, KY, KZ)

            xbest, fbest = nelder_mead(obj, x0, maxiter=5000, tol=1e-12)
            ratio = -fbest
            if ratio > best_ratio:
                best_ratio = ratio
                best_coeffs = xbest
                print(f"  refine {trial}: C = {ratio:.6f} (improved)")

    return best_ratio, best_coeffs


if __name__ == '__main__':
    scalar_ref = try_known_maximizers(N=64)

    print("\n" + "="*60)
    print("OPTIMIZATION: Div-free Ladyzhenskaya constant on T³")
    print("="*60)

    C_L_vec_R3 = (3 * 8.0 / (3.0 * np.sqrt(3.0) * np.pi**2))**0.25

    results = []
    for kmax in [1, 2, 3, 4]:
        C_opt, coeffs = optimize_divfree_constant(kmax, n_restarts=15)
        results.append((kmax, C_opt))
        print(f"  => kmax={kmax}: C_L,div-free = {C_opt:.6f}\n")

    print("\n" + "="*60)
    print("CONVERGENCE TABLE")
    print("="*60)
    print(f"{'kmax':>5s} {'n_modes':>8s} {'C_L,div-free':>14s} {'C_L,R³(vec)':>14s} {'Ratio':>8s}")
    for kmax, C in results:
        n_modes = 2 * ((2*kmax+1)**3 - 1)
        print(f"{kmax:5d} {n_modes:8d} {C:14.6f} {C_L_vec_R3:14.6f} {C/C_L_vec_R3:8.4f}")

    print(f"\n  Scalar C_L on T³ (single mode): {scalar_ref:.6f}")
    print(f"  If C_L,div-free < C_L,vec(R³) = {C_L_vec_R3:.6f}:")
    best_C = max(r[1] for r in results)
    improvement = (C_L_vec_R3 / best_C)**2 if best_C > 0 else float('inf')
    print(f"  Best div-free C found: {best_C:.6f}")
    print(f"  Improvement factor: (C_L,R³/C_L,T³)² = {improvement:.4f}")
    print(f"  This would reduce the VS bound by a factor of {improvement:.2f}")
