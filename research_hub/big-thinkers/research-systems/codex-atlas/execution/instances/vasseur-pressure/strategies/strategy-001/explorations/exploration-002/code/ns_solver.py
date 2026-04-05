"""
Pseudospectral DNS solver for 3D incompressible Navier-Stokes on T^3 = [0, 2pi]^3.
Reused from prior exploration with minor adaptations.
"""

import numpy as np
from numpy.fft import fftn, ifftn, fftfreq

class NavierStokesSolver:
    """3D pseudospectral NS solver on periodic box [0, 2pi]^3."""

    def __init__(self, N, nu, cfl=0.5):
        self.N = N
        self.nu = nu
        self.cfl = cfl

        self.dx = 2 * np.pi / N
        x = np.arange(N) * self.dx
        self.X, self.Y, self.Z = np.meshgrid(x, x, x, indexing='ij')

        k = fftfreq(N, d=1.0/N)
        self.KX, self.KY, self.KZ = np.meshgrid(k, k, k, indexing='ij')
        self.K2 = self.KX**2 + self.KY**2 + self.KZ**2
        self.K2_safe = np.where(self.K2 == 0, 1, self.K2)

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
        kdotf = (self.KX * fx_hat + self.KY * fy_hat + self.KZ * fz_hat) / self.K2_safe
        kdotf[0, 0, 0] = 0
        return fx_hat - self.KX * kdotf, fy_hat - self.KY * kdotf, fz_hat - self.KZ * kdotf

    def compute_rhs(self, ux_hat, uy_hat, uz_hat):
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

        rhsx, rhsy, rhsz = self.project(-nlx_hat + visc_x, -nly_hat + visc_y, -nlz_hat + visc_z)
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
        k2x, k2y, k2z = self.compute_rhs(ux_hat + 0.5*dt*k1x, uy_hat + 0.5*dt*k1y, uz_hat + 0.5*dt*k1z)
        k3x, k3y, k3z = self.compute_rhs(ux_hat + 0.5*dt*k2x, uy_hat + 0.5*dt*k2y, uz_hat + 0.5*dt*k2z)
        k4x, k4y, k4z = self.compute_rhs(ux_hat + dt*k3x, uy_hat + dt*k3y, uz_hat + dt*k3z)

        ux_new = ux_hat + (dt/6) * (k1x + 2*k2x + 2*k3x + k4x)
        uy_new = uy_hat + (dt/6) * (k1y + 2*k2y + 2*k3y + k4y)
        uz_new = uz_hat + (dt/6) * (k1z + 2*k2z + 2*k3z + k4z)

        ux_new, uy_new, uz_new = self.project(ux_new, uy_new, uz_new)
        return self.dealias(ux_new), self.dealias(uy_new), self.dealias(uz_new)

    def run(self, ux_hat, uy_hat, uz_hat, T_final, snapshot_interval=None):
        """Run simulation to T_final, optionally saving snapshots."""
        t = 0.0
        snapshots = []
        if snapshot_interval is not None:
            snapshots.append((t, ux_hat.copy(), uy_hat.copy(), uz_hat.copy()))
            next_snap = snapshot_interval

        while t < T_final:
            dt = self.compute_dt(ux_hat, uy_hat, uz_hat)
            if t + dt > T_final:
                dt = T_final - t
            ux_hat, uy_hat, uz_hat = self.rk4_step(ux_hat, uy_hat, uz_hat, dt)
            t += dt

            if snapshot_interval is not None and t >= next_snap - 1e-14:
                snapshots.append((t, ux_hat.copy(), uy_hat.copy(), uz_hat.copy()))
                next_snap += snapshot_interval

        if snapshot_interval is not None:
            return ux_hat, uy_hat, uz_hat, snapshots
        return ux_hat, uy_hat, uz_hat
