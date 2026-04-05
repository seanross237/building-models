#!/usr/bin/env python3
"""
Initial conditions for 3D Navier-Stokes on T³ = [0, 2π]³.

Implements:
1. Taylor-Green Vortex (baseline)
2. ABC Flow (Arnold-Beltrami-Childress)
3. Random-Phase Gaussian
4. Concentrated Vortex Tube
5. Anti-Parallel Vortex Tubes
6. Parametric Anti-Parallel (for adversarial search)
"""

import numpy as np
from numpy.fft import fftn, ifftn


def tgv_energy():
    """Return the TGV energy = π³ ≈ 31.006 for matching."""
    return np.pi**3


def normalize_energy(solver, ux_hat, uy_hat, uz_hat, target_energy=None):
    """Normalize velocity field to have 0.5 * ||u||²_{L²} = target_energy.
    Default: match TGV energy = π³.
    """
    if target_energy is None:
        target_energy = tgv_energy()
    N = solver.N
    vol = (2 * np.pi)**3
    norm_factor = vol / N**6

    u_L2_sq = norm_factor * (np.sum(np.abs(ux_hat)**2) +
                              np.sum(np.abs(uy_hat)**2) +
                              np.sum(np.abs(uz_hat)**2)).real
    current_energy = 0.5 * u_L2_sq

    if current_energy > 1e-30:
        scale = np.sqrt(target_energy / current_energy)
        return ux_hat * scale, uy_hat * scale, uz_hat * scale
    return ux_hat, uy_hat, uz_hat


def project_and_dealias(solver, ux_hat, uy_hat, uz_hat):
    """Project to divergence-free and apply dealiasing."""
    ux_hat, uy_hat, uz_hat = solver.project(ux_hat, uy_hat, uz_hat)
    ux_hat = solver.dealias(ux_hat)
    uy_hat = solver.dealias(uy_hat)
    uz_hat = solver.dealias(uz_hat)
    return ux_hat, uy_hat, uz_hat


# === 1. Taylor-Green Vortex ===

def taylor_green_ic(solver):
    """Taylor-Green vortex: u = (sin x cos y cos z, -cos x sin y cos z, 0)."""
    X, Y, Z = solver.X, solver.Y, solver.Z
    ux = np.sin(X) * np.cos(Y) * np.cos(Z)
    uy = -np.cos(X) * np.sin(Y) * np.cos(Z)
    uz = np.zeros_like(X)

    ux_hat = solver.to_spectral(ux)
    uy_hat = solver.to_spectral(uy)
    uz_hat = solver.to_spectral(uz)

    return project_and_dealias(solver, ux_hat, uy_hat, uz_hat)


# === 2. ABC Flow ===

def abc_flow_ic(solver, A=1.0, B=1.0, C=1.0):
    """Arnold-Beltrami-Childress flow. This is a Beltrami flow (ω = u).

    u_x = A sin(z) + C cos(y)
    u_y = B sin(x) + A cos(z)
    u_z = C sin(y) + B cos(x)
    """
    X, Y, Z = solver.X, solver.Y, solver.Z

    ux = A * np.sin(Z) + C * np.cos(Y)
    uy = B * np.sin(X) + A * np.cos(Z)
    uz = C * np.sin(Y) + B * np.cos(X)

    ux_hat = solver.to_spectral(ux)
    uy_hat = solver.to_spectral(uy)
    uz_hat = solver.to_spectral(uz)

    # ABC flow is already divergence-free by construction, but project to be safe
    ux_hat, uy_hat, uz_hat = project_and_dealias(solver, ux_hat, uy_hat, uz_hat)

    # Normalize to comparable energy as TGV
    return normalize_energy(solver, ux_hat, uy_hat, uz_hat)


# === 3. Random-Phase Gaussian ===

def random_gaussian_ic(solver, k_peak=4, seed=42):
    """Random Gaussian IC with energy spectrum E(k) ~ k⁴ exp(-2(k/k_peak)²).

    Enforces Hermitian symmetry so the physical-space field is real.
    """
    rng = np.random.RandomState(seed)
    N = solver.N

    ux_hat = (rng.randn(N, N, N) + 1j * rng.randn(N, N, N))
    uy_hat = (rng.randn(N, N, N) + 1j * rng.randn(N, N, N))
    uz_hat = (rng.randn(N, N, N) + 1j * rng.randn(N, N, N))

    K_mag = solver.K_mag
    K_mag_safe = np.where(K_mag == 0, 1, K_mag)
    envelope = K_mag_safe**2 * np.exp(-K_mag_safe**2 / (2 * k_peak**2))
    envelope[0, 0, 0] = 0

    ux_hat *= envelope
    uy_hat *= envelope
    uz_hat *= envelope

    # Enforce Hermitian symmetry: go to physical space (take real), then back
    # This ensures ifftn(hat).real == ifftn(hat), no energy loss
    ux_hat = fftn(ifftn(ux_hat).real)
    uy_hat = fftn(ifftn(uy_hat).real)
    uz_hat = fftn(ifftn(uz_hat).real)

    ux_hat, uy_hat, uz_hat = project_and_dealias(solver, ux_hat, uy_hat, uz_hat)
    return normalize_energy(solver, ux_hat, uy_hat, uz_hat)


# === 4. Concentrated Vortex Tube ===

def vortex_tube_ic(solver, sigma=0.2, Gamma=1.0, perturb_amp=0.3):
    """Concentrated vortex tube along z-axis with z-perturbation for stretching.

    ω_z = Γ/(πσ²) × exp(-(x² + y²)/σ²) × [1 + A cos(z)]
    ω_x = ω_y = 0

    The cos(z) modulation breaks z-invariance, enabling vortex stretching.
    Without it, (ω·∇)u has no z-derivatives and VS ≡ 0.

    Recover u from ω via Biot-Savart in Fourier space:
    û(k) = i k × ω̂(k) / |k|²
    """
    N = solver.N
    X, Y, Z = solver.X, solver.Y, solver.Z

    # Center the tube at (π, π) in x-y
    dx = X - np.pi
    dy = Y - np.pi
    dx = np.where(dx > np.pi, dx - 2*np.pi, dx)
    dx = np.where(dx < -np.pi, dx + 2*np.pi, dx)
    dy = np.where(dy > np.pi, dy - 2*np.pi, dy)
    dy = np.where(dy < -np.pi, dy + 2*np.pi, dy)
    r_sq = dx**2 + dy**2

    # Vorticity with z-modulation
    omega_z = (Gamma / (np.pi * sigma**2)) * np.exp(-r_sq / sigma**2) * (1 + perturb_amp * np.cos(Z))
    omega_x = np.zeros_like(X)
    omega_y = np.zeros_like(X)

    return _biot_savart_inversion(solver, omega_x, omega_y, omega_z)


def _biot_savart_inversion(solver, omega_x, omega_y, omega_z, target_energy=None):
    """Recover velocity from vorticity via Biot-Savart in Fourier space."""
    omega_x_hat = fftn(omega_x)
    omega_y_hat = fftn(omega_y)
    omega_z_hat = fftn(omega_z)

    KX, KY, KZ = solver.KX, solver.KY, solver.KZ
    K2_safe = solver.K2_safe

    # û = i(k × ω̂) / |k|²
    cross_x = KY * omega_z_hat - KZ * omega_y_hat
    cross_y = KZ * omega_x_hat - KX * omega_z_hat
    cross_z = KX * omega_y_hat - KY * omega_x_hat

    ux_hat = 1j * cross_x / K2_safe
    uy_hat = 1j * cross_y / K2_safe
    uz_hat = 1j * cross_z / K2_safe

    ux_hat[0, 0, 0] = 0
    uy_hat[0, 0, 0] = 0
    uz_hat[0, 0, 0] = 0

    ux_hat, uy_hat, uz_hat = project_and_dealias(solver, ux_hat, uy_hat, uz_hat)
    return normalize_energy(solver, ux_hat, uy_hat, uz_hat, target_energy=target_energy)


# === 5. Anti-Parallel Vortex Tubes ===

def anti_parallel_tubes_ic(solver, d=np.pi/2, sigma=0.2, Gamma=1.0, perturb_amp=0.5):
    """Two counter-rotating vortex tubes with z-perturbation for reconnection.

    Tube 1 at y = π + d/2, with x-center perturbed as π + δ sin(z)
    Tube 2 at y = π - d/2, with x-center perturbed as π - δ sin(z)

    The sinusoidal perturbation brings the tubes closer at z=π/2 and
    further apart at z=3π/2, driving vortex reconnection and strong
    vortex stretching.
    """
    N = solver.N
    X, Y, Z = solver.X, solver.Y, solver.Z

    delta = perturb_amp  # x-perturbation amplitude

    # Tube 1: center at (π + δ sin(z), π + d/2)
    cx1 = np.pi + delta * np.sin(Z)
    cy1 = np.pi + d/2
    dx1 = X - cx1
    dy1 = Y - cy1
    dx1 = np.where(dx1 > np.pi, dx1 - 2*np.pi, dx1)
    dx1 = np.where(dx1 < -np.pi, dx1 + 2*np.pi, dx1)
    dy1 = np.where(dy1 > np.pi, dy1 - 2*np.pi, dy1)
    dy1 = np.where(dy1 < -np.pi, dy1 + 2*np.pi, dy1)
    r1_sq = dx1**2 + dy1**2

    # Tube 2: center at (π - δ sin(z), π - d/2)
    cx2 = np.pi - delta * np.sin(Z)
    cy2 = np.pi - d/2
    dx2 = X - cx2
    dy2 = Y - cy2
    dx2 = np.where(dx2 > np.pi, dx2 - 2*np.pi, dx2)
    dx2 = np.where(dx2 < -np.pi, dx2 + 2*np.pi, dx2)
    dy2 = np.where(dy2 > np.pi, dy2 - 2*np.pi, dy2)
    dy2 = np.where(dy2 < -np.pi, dy2 + 2*np.pi, dy2)
    r2_sq = dx2**2 + dy2**2

    # Combined vorticity: +Γ for tube 1, -Γ for tube 2 (both in z direction)
    omega_z = (Gamma / (np.pi * sigma**2)) * (
        np.exp(-r1_sq / sigma**2) - np.exp(-r2_sq / sigma**2)
    )
    omega_x = np.zeros_like(X)
    omega_y = np.zeros_like(X)

    return _biot_savart_inversion(solver, omega_x, omega_y, omega_z)


# === 6. Parametric Anti-Parallel (for adversarial search) ===

def parametric_anti_parallel_ic(solver, params):
    """Parametric version of anti-parallel tubes for adversarial optimization.

    params dict:
        d: tube separation (default π/2)
        sigma: tube radius (default 0.2)
        Gamma_ratio: Γ₂/Γ₁ ratio (default -1.0, counter-rotating)
        perturb_amp: sinusoidal perturbation amplitude (default 0.5)
        perturb_k: wavenumber of z-perturbation (default 1)
        tilt: tube tilt from z-axis (default 0)
    """
    N = solver.N
    X, Y, Z = solver.X, solver.Y, solver.Z

    d = params.get('d', np.pi/2)
    sigma = params.get('sigma', 0.2)
    Gamma_ratio = params.get('Gamma_ratio', -1.0)
    delta = params.get('perturb_amp', 0.5)
    k_perturb = params.get('perturb_k', 1)
    tilt = params.get('tilt', 0.0)

    Gamma1 = 1.0
    Gamma2 = Gamma_ratio * Gamma1

    # Tube 1: center at (π + δ sin(k z), π + d/2)
    cx1 = np.pi + delta * np.sin(k_perturb * Z)
    cy1 = np.pi + d/2
    dx1 = X - cx1
    dy1 = Y - cy1
    dx1 = np.where(dx1 > np.pi, dx1 - 2*np.pi, dx1)
    dx1 = np.where(dx1 < -np.pi, dx1 + 2*np.pi, dx1)
    dy1 = np.where(dy1 > np.pi, dy1 - 2*np.pi, dy1)
    dy1 = np.where(dy1 < -np.pi, dy1 + 2*np.pi, dy1)
    r1_sq = dx1**2 + dy1**2

    # Tube 2: center at (π - δ sin(k z), π - d/2)
    cx2 = np.pi - delta * np.sin(k_perturb * Z)
    cy2 = np.pi - d/2
    dx2 = X - cx2
    dy2 = Y - cy2
    dx2 = np.where(dx2 > np.pi, dx2 - 2*np.pi, dx2)
    dx2 = np.where(dx2 < -np.pi, dx2 + 2*np.pi, dx2)
    dy2 = np.where(dy2 > np.pi, dy2 - 2*np.pi, dy2)
    dy2 = np.where(dy2 < -np.pi, dy2 + 2*np.pi, dy2)
    r2_sq = dx2**2 + dy2**2

    # Vorticity profiles
    profile1 = (Gamma1 / (np.pi * sigma**2)) * np.exp(-r1_sq / sigma**2)
    profile2 = (Gamma2 / (np.pi * sigma**2)) * np.exp(-r2_sq / sigma**2)

    cos_t = np.cos(tilt)
    sin_t = np.sin(tilt)

    # With tilt, vorticity has x and z components
    omega_x = sin_t * (profile1 + profile2)
    omega_y = np.zeros_like(X)
    omega_z = cos_t * (profile1 + profile2)

    return _biot_savart_inversion(solver, omega_x, omega_y, omega_z)


# === IC Registry ===

IC_REGISTRY = {
    'taylor_green': {
        'name': 'Taylor-Green Vortex',
        'func': taylor_green_ic,
        'args': {},
    },
    'abc': {
        'name': 'ABC Flow (A=B=C=1)',
        'func': abc_flow_ic,
        'args': {'A': 1.0, 'B': 1.0, 'C': 1.0},
    },
    'random_gaussian': {
        'name': 'Random-Phase Gaussian',
        'func': random_gaussian_ic,
        'args': {'k_peak': 4, 'seed': 42},
    },
    'vortex_tube': {
        'name': 'Vortex Tube (σ=0.2, z-perturbed)',
        'func': vortex_tube_ic,
        'args': {'sigma': 0.2, 'Gamma': 1.0, 'perturb_amp': 0.3},
    },
    'anti_parallel': {
        'name': 'Anti-Parallel Tubes (z-perturbed)',
        'func': anti_parallel_tubes_ic,
        'args': {'d': np.pi/2, 'sigma': 0.2, 'Gamma': 1.0, 'perturb_amp': 0.5},
    },
}


def create_ic(solver, ic_name):
    """Create initial condition by name."""
    if ic_name not in IC_REGISTRY:
        raise ValueError(f"Unknown IC: {ic_name}. Available: {list(IC_REGISTRY.keys())}")

    entry = IC_REGISTRY[ic_name]
    return entry['func'](solver, **entry['args'])


if __name__ == '__main__':
    """Quick test: create all ICs and print basic diagnostics."""
    from ns_solver import NavierStokesSolver, compute_diagnostics

    N = 32
    nu = 0.01
    solver = NavierStokesSolver(N, nu)

    for ic_name, entry in IC_REGISTRY.items():
        print(f"\n{'='*60}")
        print(f"IC: {entry['name']}")
        print(f"{'='*60}")

        ux_hat, uy_hat, uz_hat = create_ic(solver, ic_name)
        diag = compute_diagnostics(solver, ux_hat, uy_hat, uz_hat)

        print(f"  Energy:        {diag['energy']:.6f}")
        print(f"  ||u||_L²:     {diag['L2_norm']:.6f}")
        print(f"  ||∇u||_L²:    {diag['gradL2_norm']:.6f}")
        print(f"  ||ω||_L²:     {diag['omega_L2']:.6f}")
        print(f"  Enstrophy:     {diag['enstrophy']:.6f}")
        print(f"  div_max:       {diag['divergence_max']:.2e}")
        print(f"  VS:            {diag['vortex_stretching']:.6e}")
