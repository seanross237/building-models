"""
Pseudospectral DNS solver for 3D incompressible Navier-Stokes on T^3 = [0, 2pi]^3.
Adapted from Strategy-001 exploration-002.

Features:
- FFT-based pseudospectral method with 2/3 dealiasing
- RK4 time stepping with adaptive CFL-based dt
- Pressure projection to enforce incompressibility
"""

import numpy as np
from numpy.fft import fftn, ifftn, fftfreq


class NavierStokesSolver:
    """3D pseudospectral NS solver on periodic box [0, 2pi]^3."""

    def __init__(self, N, nu, cfl=0.5):
        self.N = N
        self.nu = nu
        self.cfl = cfl

        # Physical grid
        self.dx = 2 * np.pi / N
        x = np.arange(N) * self.dx
        self.X, self.Y, self.Z = np.meshgrid(x, x, x, indexing='ij')

        # Wavenumber grid
        k = fftfreq(N, d=1.0/N)
        self.KX, self.KY, self.KZ = np.meshgrid(k, k, k, indexing='ij')
        self.K2 = self.KX**2 + self.KY**2 + self.KZ**2
        self.K2_safe = np.where(self.K2 == 0, 1, self.K2)

        # Dealiasing mask: 2/3 rule
        kmax = N // 3
        self.dealias_mask = (
            (np.abs(self.KX) <= kmax) &
            (np.abs(self.KY) <= kmax) &
            (np.abs(self.KZ) <= kmax)
        ).astype(np.float64)

        self.K_mag = np.sqrt(self.K2)

    def to_spectral(self, u_phys):
        return fftn(u_phys)

    def to_physical(self, u_hat):
        return ifftn(u_hat).real

    def dealias(self, u_hat):
        return u_hat * self.dealias_mask

    def project(self, fx_hat, fy_hat, fz_hat):
        """Leray-Helmholtz projection: remove divergent part."""
        kdotf = (self.KX * fx_hat + self.KY * fy_hat + self.KZ * fz_hat) / self.K2_safe
        kdotf[0, 0, 0] = 0
        px_hat = fx_hat - self.KX * kdotf
        py_hat = fy_hat - self.KY * kdotf
        pz_hat = fz_hat - self.KZ * kdotf
        return px_hat, py_hat, pz_hat

    def compute_rhs(self, ux_hat, uy_hat, uz_hat):
        """Compute RHS of NS in spectral space: -P(u.grad u) + nu * Laplacian u."""
        ux_d = self.to_physical(self.dealias(ux_hat))
        uy_d = self.to_physical(self.dealias(uy_hat))
        uz_d = self.to_physical(self.dealias(uz_hat))

        ux_hat_d = self.dealias(ux_hat)
        uy_hat_d = self.dealias(uy_hat)
        uz_hat_d = self.dealias(uz_hat)

        dux_dx = self.to_physical(1j * self.KX * ux_hat_d)
        dux_dy = self.to_physical(1j * self.KY * ux_hat_d)
        dux_dz = self.to_physical(1j * self.KZ * ux_hat_d)
        duy_dx = self.to_physical(1j * self.KX * uy_hat_d)
        duy_dy = self.to_physical(1j * self.KY * uy_hat_d)
        duy_dz = self.to_physical(1j * self.KZ * uy_hat_d)
        duz_dx = self.to_physical(1j * self.KX * uz_hat_d)
        duz_dy = self.to_physical(1j * self.KY * uz_hat_d)
        duz_dz = self.to_physical(1j * self.KZ * uz_hat_d)

        nlx = ux_d * dux_dx + uy_d * dux_dy + uz_d * dux_dz
        nly = ux_d * duy_dx + uy_d * duy_dy + uz_d * duy_dz
        nlz = ux_d * duz_dx + uy_d * duz_dy + uz_d * duz_dz

        nlx_hat = self.dealias(self.to_spectral(nlx))
        nly_hat = self.dealias(self.to_spectral(nly))
        nlz_hat = self.dealias(self.to_spectral(nlz))

        visc_x = -self.nu * self.K2 * ux_hat
        visc_y = -self.nu * self.K2 * uy_hat
        visc_z = -self.nu * self.K2 * uz_hat

        rhsx = -nlx_hat + visc_x
        rhsy = -nly_hat + visc_y
        rhsz = -nlz_hat + visc_z

        rhsx, rhsy, rhsz = self.project(rhsx, rhsy, rhsz)
        return rhsx, rhsy, rhsz

    def compute_dt(self, ux_hat, uy_hat, uz_hat):
        ux = self.to_physical(ux_hat)
        uy = self.to_physical(uy_hat)
        uz = self.to_physical(uz_hat)

        u_max = max(np.max(np.abs(ux)), np.max(np.abs(uy)), np.max(np.abs(uz)))
        if u_max < 1e-14:
            return 0.01

        dt_cfl = self.cfl * self.dx / u_max
        dt_visc = self.cfl * self.dx**2 / (6 * self.nu) if self.nu > 0 else np.inf
        return min(dt_cfl, dt_visc)

    def rk4_step(self, ux_hat, uy_hat, uz_hat, dt):
        k1x, k1y, k1z = self.compute_rhs(ux_hat, uy_hat, uz_hat)
        k2x, k2y, k2z = self.compute_rhs(
            ux_hat + 0.5*dt*k1x, uy_hat + 0.5*dt*k1y, uz_hat + 0.5*dt*k1z)
        k3x, k3y, k3z = self.compute_rhs(
            ux_hat + 0.5*dt*k2x, uy_hat + 0.5*dt*k2y, uz_hat + 0.5*dt*k2z)
        k4x, k4y, k4z = self.compute_rhs(
            ux_hat + dt*k3x, uy_hat + dt*k3y, uz_hat + dt*k3z)

        ux_hat_new = ux_hat + (dt/6) * (k1x + 2*k2x + 2*k3x + k4x)
        uy_hat_new = uy_hat + (dt/6) * (k1y + 2*k2y + 2*k3y + k4y)
        uz_hat_new = uz_hat + (dt/6) * (k1z + 2*k2z + 2*k3z + k4z)

        ux_hat_new, uy_hat_new, uz_hat_new = self.project(ux_hat_new, uy_hat_new, uz_hat_new)
        ux_hat_new = self.dealias(ux_hat_new)
        uy_hat_new = self.dealias(uy_hat_new)
        uz_hat_new = self.dealias(uz_hat_new)

        return ux_hat_new, uy_hat_new, uz_hat_new


# =============================================================================
# Initial Conditions
# =============================================================================

def taylor_green_ic(solver):
    """Taylor-Green vortex: u = (sin x cos y cos z, -cos x sin y cos z, 0)"""
    X, Y, Z = solver.X, solver.Y, solver.Z
    ux = np.sin(X) * np.cos(Y) * np.cos(Z)
    uy = -np.cos(X) * np.sin(Y) * np.cos(Z)
    uz = np.zeros_like(X)

    ux_hat = solver.to_spectral(ux)
    uy_hat = solver.to_spectral(uy)
    uz_hat = solver.to_spectral(uz)

    ux_hat, uy_hat, uz_hat = solver.project(ux_hat, uy_hat, uz_hat)
    ux_hat = solver.dealias(ux_hat)
    uy_hat = solver.dealias(uy_hat)
    uz_hat = solver.dealias(uz_hat)
    return ux_hat, uy_hat, uz_hat


def random_gaussian_ic(solver, k0=4, seed=42):
    """Random Gaussian IC with Kolmogorov-like spectrum."""
    rng = np.random.RandomState(seed)
    N = solver.N

    ux_hat = (rng.randn(N, N, N) + 1j * rng.randn(N, N, N))
    uy_hat = (rng.randn(N, N, N) + 1j * rng.randn(N, N, N))
    uz_hat = (rng.randn(N, N, N) + 1j * rng.randn(N, N, N))

    K_mag = solver.K_mag
    K_mag_safe = np.where(K_mag == 0, 1, K_mag)

    # Kolmogorov spectrum: E(k) ~ k^{-5/3} for k > k0, rising for k < k0
    # Use smooth envelope: k^2 * exp(-k^2/(2*k0^2)) which peaks at k ~ k0
    envelope = K_mag_safe**2 * np.exp(-K_mag_safe**2 / (2 * k0**2))
    envelope[0, 0, 0] = 0

    ux_hat *= envelope
    uy_hat *= envelope
    uz_hat *= envelope

    ux_hat, uy_hat, uz_hat = solver.project(ux_hat, uy_hat, uz_hat)
    ux_hat = solver.dealias(ux_hat)
    uy_hat = solver.dealias(uy_hat)
    uz_hat = solver.dealias(uz_hat)

    # Normalize to target energy ~ 0.5
    ux_phys = solver.to_physical(ux_hat)
    uy_phys = solver.to_physical(uy_hat)
    uz_phys = solver.to_physical(uz_hat)
    current_energy = 0.5 * np.mean(ux_phys**2 + uy_phys**2 + uz_phys**2)
    if current_energy > 0:
        scale = np.sqrt(0.5 / current_energy)
        ux_hat *= scale
        uy_hat *= scale
        uz_hat *= scale

    return ux_hat, uy_hat, uz_hat


def antiparallel_tubes_ic(solver, sigma=2.5, d_sep=np.pi/4, delta=1.2):
    """Anti-parallel vortex tubes initial condition.

    Two Gaussian vortex tubes with opposite circulation, separated by d_sep.
    """
    X, Y, Z = solver.X, solver.Y, solver.Z

    # Tube 1: centered at (pi, pi - d_sep/2, z), pointing in z-direction
    r1_sq = (X - np.pi)**2 + (Y - np.pi + d_sep/2)**2
    # Tube 2: centered at (pi, pi + d_sep/2, z), pointing in -z-direction
    r2_sq = (X - np.pi)**2 + (Y - np.pi - d_sep/2)**2

    # Gaussian vortex profile
    omega_z1 = delta * np.exp(-r1_sq / (2 * sigma**2))
    omega_z2 = -delta * np.exp(-r2_sq / (2 * sigma**2))

    # Total vorticity in z-direction
    omega_z = omega_z1 + omega_z2

    # Add slight perturbation in x to break symmetry (anti-parallel perturbation)
    omega_x = 0.1 * delta * np.sin(Z) * (np.exp(-r1_sq / (2 * sigma**2)) - np.exp(-r2_sq / (2 * sigma**2)))
    omega_y = np.zeros_like(X)

    # Recover velocity from vorticity using Biot-Savart in Fourier space
    # omega = curl(u), in Fourier: omega_hat = ik x u_hat
    # u_hat = ik x omega_hat / |k|^2 (for div-free fields)
    omega_x_hat = solver.to_spectral(omega_x)
    omega_y_hat = solver.to_spectral(omega_y)
    omega_z_hat = solver.to_spectral(omega_z)

    # u = curl(psi) where Laplacian(psi) = -omega
    # psi_hat = omega_hat / |k|^2
    # u_hat = ik x psi_hat
    K2_safe = solver.K2_safe
    psi_x_hat = omega_x_hat / K2_safe
    psi_y_hat = omega_y_hat / K2_safe
    psi_z_hat = omega_z_hat / K2_safe
    psi_x_hat[0, 0, 0] = 0
    psi_y_hat[0, 0, 0] = 0
    psi_z_hat[0, 0, 0] = 0

    # u = curl(psi): u_x = d_psi_z/dy - d_psi_y/dz, etc.
    ux_hat = 1j * solver.KY * psi_z_hat - 1j * solver.KZ * psi_y_hat
    uy_hat = 1j * solver.KZ * psi_x_hat - 1j * solver.KX * psi_z_hat
    uz_hat = 1j * solver.KX * psi_y_hat - 1j * solver.KY * psi_x_hat

    ux_hat, uy_hat, uz_hat = solver.project(ux_hat, uy_hat, uz_hat)
    ux_hat = solver.dealias(ux_hat)
    uy_hat = solver.dealias(uy_hat)
    uz_hat = solver.dealias(uz_hat)

    return ux_hat, uy_hat, uz_hat
