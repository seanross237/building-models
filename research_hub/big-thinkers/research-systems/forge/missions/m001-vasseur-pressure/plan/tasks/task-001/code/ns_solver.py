"""
Pseudospectral DNS solver for 3D incompressible Navier-Stokes on T³ = [0, 2π]³.

Adapted from Atlas mission code. Extended to compute and output the pressure field
explicitly, required for Vasseur pressure exponent analysis.

Features:
- FFT-based pseudospectral method
- 2/3 dealiasing rule (mandatory)
- RK4 time stepping with adaptive CFL-based dt
- Pressure projection to enforce incompressibility
- Explicit pressure field computation via Fourier Poisson solve
- L^q norms of pressure for q = 1, 3/2, 2, 3, inf
- Energy conservation check

Physical setting:
  ∂u/∂t + (u·∇)u = -∇p + ν Δu
  ∇·u = 0
on T³ = [0, 2π]³.

Pressure Poisson equation:
  Δp = -∂ᵢ∂ⱼ(uᵢuⱼ)  ==>  p̂(k) = i(k · NL^(k)) / |k|²  (k ≠ 0)
where NL = (u·∇)u is the nonlinear (advective) term.
"""

import numpy as np
from numpy.fft import fftfreq
from scipy.fft import fftn, ifftn

# Number of parallel workers for FFT.  -1 means use all available CPU cores.
_FFT_WORKERS = -1


class NavierStokesSolver:
    """3D pseudospectral NS solver on periodic box [0, 2π]³."""

    def __init__(self, N, nu, cfl=0.5):
        """
        Args:
            N: grid resolution (N³ points)
            nu: kinematic viscosity  (nu = 1/Re for unit-domain TGV)
            cfl: CFL number for adaptive time stepping
        """
        self.N = N
        self.nu = nu
        self.cfl = cfl

        # Physical grid
        self.dx = 2 * np.pi / N
        x = np.arange(N) * self.dx
        self.X, self.Y, self.Z = np.meshgrid(x, x, x, indexing='ij')

        # Wavenumber grid
        k = fftfreq(N, d=1.0 / N)  # wavenumbers: 0, 1, ..., N/2, -N/2+1, ..., -1
        self.KX, self.KY, self.KZ = np.meshgrid(k, k, k, indexing='ij')
        self.K2 = self.KX**2 + self.KY**2 + self.KZ**2
        self.K2_safe = np.where(self.K2 == 0, 1, self.K2)  # avoid division by zero at k=0

        # Dealiasing mask: 2/3 rule
        kmax = N // 3  # N/2 * 2/3 = N/3
        self.dealias_mask = (
            (np.abs(self.KX) <= kmax) &
            (np.abs(self.KY) <= kmax) &
            (np.abs(self.KZ) <= kmax)
        ).astype(np.float64)

        # Magnitude of wavenumber
        self.K_mag = np.sqrt(self.K2)

    # ------------------------------------------------------------------
    # Fast spectral-only diagnostics (no FFT required)
    # ------------------------------------------------------------------

    def spectral_energy(self, ux_hat, uy_hat, uz_hat):
        """Compute kinetic energy directly from spectral coefficients (no FFT).

        By Parseval: ½ ∫|u|² dx = ½ * vol/N^6 * Σ(|ûx|² + |ûy|² + |ûz|²)
        This avoids physical-space transforms and is fast.
        """
        vol = (2 * np.pi)**3
        N6 = self.N**6
        return 0.5 * vol / N6 * float(
            np.sum(np.abs(ux_hat)**2 + np.abs(uy_hat)**2 + np.abs(uz_hat)**2))

    def spectral_dissipation(self, ux_hat, uy_hat, uz_hat):
        """Compute viscous dissipation ε = ν ‖∇u‖² from spectral coefficients.

        By Parseval: ‖∇u‖²_{L²} = vol/N^6 * Σ_k |k|² (|ûx|² + |ûy|² + |ûz|²)
        This is exact and requires no FFT.
        """
        vol = (2 * np.pi)**3
        N6 = self.N**6
        vel_sq = np.abs(ux_hat)**2 + np.abs(uy_hat)**2 + np.abs(uz_hat)**2
        return self.nu * vol / N6 * float(np.sum(self.K2 * vel_sq))

    def spectral_max_u(self, ux_hat, uy_hat, uz_hat):
        """Estimate max velocity for CFL, using dealiased physical transform."""
        ux = self.to_physical(self.dealias(ux_hat))
        uy = self.to_physical(self.dealias(uy_hat))
        uz = self.to_physical(self.dealias(uz_hat))
        return max(float(np.max(np.abs(ux))),
                   float(np.max(np.abs(uy))),
                   float(np.max(np.abs(uz))))

    # ------------------------------------------------------------------
    # Core spectral operations
    # ------------------------------------------------------------------

    def to_spectral(self, u_phys):
        """Transform field from physical space to spectral (Fourier) space."""
        return fftn(u_phys, workers=_FFT_WORKERS)

    def to_physical(self, u_hat):
        """Transform field from spectral space to physical space (take real part)."""
        return ifftn(u_hat, workers=_FFT_WORKERS).real

    def dealias(self, u_hat):
        """Apply 2/3 dealiasing: zero out modes with |kᵢ| > N/3."""
        return u_hat * self.dealias_mask

    def project(self, fx_hat, fy_hat, fz_hat):
        """Leray-Helmholtz projection: remove divergent (longitudinal) part.

        P[F] = F - k(k·F)/|k|²
        This enforces ∇·u = 0 in spectral space.
        The removed part k(k·F)/|k|² corresponds to the pressure gradient.
        """
        kdotf = (self.KX * fx_hat + self.KY * fy_hat + self.KZ * fz_hat) / self.K2_safe
        # k=0 mode: projection is identity (mean flow is not removed)
        kdotf[0, 0, 0] = 0.0

        px_hat = fx_hat - self.KX * kdotf
        py_hat = fy_hat - self.KY * kdotf
        pz_hat = fz_hat - self.KZ * kdotf
        return px_hat, py_hat, pz_hat

    # ------------------------------------------------------------------
    # Pressure computation
    # ------------------------------------------------------------------

    def compute_pressure(self, ux_hat, uy_hat, uz_hat):
        """Compute the pressure field p(x) from velocity in spectral space.

        Derivation:
          NS:  ∂u/∂t = -NL - ∇p + ν Δu,  ∇·u = 0
          Taking divergence:  0 = -∇·NL - Δp
          So:  Δp = -∇·NL = -∂ⱼNLⱼ
          Fourier:  -|k|² p̂ = -ikⱼ NLⱼ^(k)
          =>  p̂(k) = i(k·NL^(k)) / |k|²   for k ≠ 0; p̂(0) = 0

        The nonlinear term NL = (u·∇)u must be computed with dealiasing,
        identical to how it is computed in compute_rhs().

        Returns:
            p_hat: pressure in spectral space (complex array, shape N³)
            p_phys: pressure in physical space (real array, shape N³)
        """
        # Dealiased velocities in physical space
        ux_d = self.to_physical(self.dealias(ux_hat))
        uy_d = self.to_physical(self.dealias(uy_hat))
        uz_d = self.to_physical(self.dealias(uz_hat))

        # Dealiased velocity hats for gradient computation
        ux_hat_d = self.dealias(ux_hat)
        uy_hat_d = self.dealias(uy_hat)
        uz_hat_d = self.dealias(uz_hat)

        # Velocity gradients via spectral differentiation
        dux_dx = self.to_physical(1j * self.KX * ux_hat_d)
        dux_dy = self.to_physical(1j * self.KY * ux_hat_d)
        dux_dz = self.to_physical(1j * self.KZ * ux_hat_d)

        duy_dx = self.to_physical(1j * self.KX * uy_hat_d)
        duy_dy = self.to_physical(1j * self.KY * uy_hat_d)
        duy_dz = self.to_physical(1j * self.KZ * uy_hat_d)

        duz_dx = self.to_physical(1j * self.KX * uz_hat_d)
        duz_dy = self.to_physical(1j * self.KY * uz_hat_d)
        duz_dz = self.to_physical(1j * self.KZ * uz_hat_d)

        # Nonlinear term NL = (u·∇)u in physical space
        nlx = ux_d * dux_dx + uy_d * dux_dy + uz_d * dux_dz
        nly = ux_d * duy_dx + uy_d * duy_dy + uz_d * duy_dz
        nlz = ux_d * duz_dx + uy_d * duz_dy + uz_d * duz_dz

        # Transform to spectral and dealias (same as in compute_rhs)
        nlx_hat = self.dealias(self.to_spectral(nlx))
        nly_hat = self.dealias(self.to_spectral(nly))
        nlz_hat = self.dealias(self.to_spectral(nlz))

        # Pressure from Poisson equation:
        # p̂(k) = i(k·NL^) / |k|²  for k ≠ 0
        kdot_nl = self.KX * nlx_hat + self.KY * nly_hat + self.KZ * nlz_hat
        p_hat = 1j * kdot_nl / self.K2_safe
        p_hat[0, 0, 0] = 0.0  # zero mean pressure (gauge choice)

        p_phys = self.to_physical(p_hat)
        return p_hat, p_phys

    def compute_pressure_norms(self, p_phys):
        """Compute L^q norms of pressure for several values of q.

        The Calderón-Zygmund exponent q=3/2 is key for Vasseur's analysis.

        Args:
            p_phys: pressure field in physical space (real array)

        Returns:
            dict with keys 'L1', 'L1p5', 'L2', 'L3', 'Linf' and their values
        """
        vol = (2 * np.pi)**3
        ap = np.abs(p_phys)

        norms = {
            'L1':    (np.mean(ap) * vol),
            'L1p5':  (np.mean(ap**1.5) * vol)**(1.0 / 1.5),
            'L2':    np.sqrt(np.mean(ap**2) * vol),
            'L3':    (np.mean(ap**3) * vol)**(1.0 / 3.0),
            'Linf':  np.max(ap),
        }
        return norms

    # ------------------------------------------------------------------
    # RHS computation
    # ------------------------------------------------------------------

    def compute_rhs(self, ux_hat, uy_hat, uz_hat):
        """Compute RHS of NS in spectral space: -P(u·∇u) + ν Δu.

        Returns:
            (rhsx_hat, rhsy_hat, rhsz_hat): spectral RHS components
        """
        # Dealiased physical-space velocities
        ux_d = self.to_physical(self.dealias(ux_hat))
        uy_d = self.to_physical(self.dealias(uy_hat))
        uz_d = self.to_physical(self.dealias(uz_hat))

        # Dealiased velocity hats for gradient computation
        ux_hat_d = self.dealias(ux_hat)
        uy_hat_d = self.dealias(uy_hat)
        uz_hat_d = self.dealias(uz_hat)

        # ∂uᵢ/∂xⱼ via spectral differentiation
        dux_dx = self.to_physical(1j * self.KX * ux_hat_d)
        dux_dy = self.to_physical(1j * self.KY * ux_hat_d)
        dux_dz = self.to_physical(1j * self.KZ * ux_hat_d)

        duy_dx = self.to_physical(1j * self.KX * uy_hat_d)
        duy_dy = self.to_physical(1j * self.KY * uy_hat_d)
        duy_dz = self.to_physical(1j * self.KZ * uy_hat_d)

        duz_dx = self.to_physical(1j * self.KX * uz_hat_d)
        duz_dy = self.to_physical(1j * self.KY * uz_hat_d)
        duz_dz = self.to_physical(1j * self.KZ * uz_hat_d)

        # Nonlinear term: (u·∇)u
        nlx = ux_d * dux_dx + uy_d * dux_dy + uz_d * dux_dz
        nly = ux_d * duy_dx + uy_d * duy_dy + uz_d * duy_dz
        nlz = ux_d * duz_dx + uy_d * duz_dy + uz_d * duz_dz

        # Transform and dealias
        nlx_hat = self.dealias(self.to_spectral(nlx))
        nly_hat = self.dealias(self.to_spectral(nly))
        nlz_hat = self.dealias(self.to_spectral(nlz))

        # Viscous term: ν Δu = -ν|k|² û
        visc_x = -self.nu * self.K2 * ux_hat
        visc_y = -self.nu * self.K2 * uy_hat
        visc_z = -self.nu * self.K2 * uz_hat

        # RHS = -NL + viscous, then project to enforce ∇·u = 0
        rhsx = -nlx_hat + visc_x
        rhsy = -nly_hat + visc_y
        rhsz = -nlz_hat + visc_z

        rhsx, rhsy, rhsz = self.project(rhsx, rhsy, rhsz)
        return rhsx, rhsy, rhsz

    # ------------------------------------------------------------------
    # Time stepping
    # ------------------------------------------------------------------

    def compute_dt(self, ux_hat, uy_hat, uz_hat, u_max=None):
        """Adaptive time step from CFL and viscous stability conditions.

        Args:
            ux_hat, uy_hat, uz_hat: spectral velocity
            u_max: pre-computed max velocity (optional, avoids redundant IFFT)
        """
        if u_max is None:
            u_max = self.spectral_max_u(ux_hat, uy_hat, uz_hat)

        if u_max < 1e-14:
            return 0.01  # fallback for near-zero velocity

        dt_cfl = self.cfl * self.dx / u_max
        dt_visc = self.cfl * self.dx**2 / (6 * self.nu) if self.nu > 0 else np.inf

        return min(dt_cfl, dt_visc)

    def rk4_step(self, ux_hat, uy_hat, uz_hat, dt):
        """Classical 4th-order Runge-Kutta time step."""
        k1x, k1y, k1z = self.compute_rhs(ux_hat, uy_hat, uz_hat)

        k2x, k2y, k2z = self.compute_rhs(
            ux_hat + 0.5 * dt * k1x,
            uy_hat + 0.5 * dt * k1y,
            uz_hat + 0.5 * dt * k1z)

        k3x, k3y, k3z = self.compute_rhs(
            ux_hat + 0.5 * dt * k2x,
            uy_hat + 0.5 * dt * k2y,
            uz_hat + 0.5 * dt * k2z)

        k4x, k4y, k4z = self.compute_rhs(
            ux_hat + dt * k3x,
            uy_hat + dt * k3y,
            uz_hat + dt * k3z)

        ux_new = ux_hat + (dt / 6) * (k1x + 2 * k2x + 2 * k3x + k4x)
        uy_new = uy_hat + (dt / 6) * (k1y + 2 * k2y + 2 * k3y + k4y)
        uz_new = uz_hat + (dt / 6) * (k1z + 2 * k2z + 2 * k3z + k4z)

        # Re-project and dealias after RK4 to maintain incompressibility
        ux_new, uy_new, uz_new = self.project(ux_new, uy_new, uz_new)
        ux_new = self.dealias(ux_new)
        uy_new = self.dealias(uy_new)
        uz_new = self.dealias(uz_new)

        return ux_new, uy_new, uz_new


# ------------------------------------------------------------------
# Initial conditions
# ------------------------------------------------------------------

def taylor_green_ic(solver):
    """Taylor-Green vortex initial condition on [0, 2π]³.

    u = (sin x cos y cos z, -cos x sin y cos z, 0)

    This is the classical TGV: exactly divergence-free, energy = (2π)³/4,
    characteristic velocity U=1, length scale L=1, Re=U*L/nu=1/nu.
    """
    X, Y, Z = solver.X, solver.Y, solver.Z

    ux = np.sin(X) * np.cos(Y) * np.cos(Z)
    uy = -np.cos(X) * np.sin(Y) * np.cos(Z)
    uz = np.zeros_like(X)

    ux_hat = solver.to_spectral(ux)
    uy_hat = solver.to_spectral(uy)
    uz_hat = solver.to_spectral(uz)

    # Project and dealias
    ux_hat, uy_hat, uz_hat = solver.project(ux_hat, uy_hat, uz_hat)
    ux_hat = solver.dealias(ux_hat)
    uy_hat = solver.dealias(uy_hat)
    uz_hat = solver.dealias(uz_hat)

    return ux_hat, uy_hat, uz_hat


# ------------------------------------------------------------------
# Diagnostics
# ------------------------------------------------------------------

def compute_diagnostics(solver, ux_hat, uy_hat, uz_hat, include_pressure=True):
    """Compute all diagnostic quantities for validation and analysis.

    Args:
        solver: NavierStokesSolver instance
        ux_hat, uy_hat, uz_hat: velocity in spectral space
        include_pressure: if True, compute pressure field and its L^q norms

    Returns:
        dict with diagnostic quantities
    """
    N = solver.N
    vol = (2 * np.pi)**3

    # Physical velocities (from full spectral field, no extra dealiasing here)
    ux = solver.to_physical(ux_hat)
    uy = solver.to_physical(uy_hat)
    uz = solver.to_physical(uz_hat)

    # Velocity gradients (from spectral field)
    dux_dx = solver.to_physical(1j * solver.KX * ux_hat)
    dux_dy = solver.to_physical(1j * solver.KY * ux_hat)
    dux_dz = solver.to_physical(1j * solver.KZ * ux_hat)
    duy_dx = solver.to_physical(1j * solver.KX * uy_hat)
    duy_dy = solver.to_physical(1j * solver.KY * uy_hat)
    duy_dz = solver.to_physical(1j * solver.KZ * uy_hat)
    duz_dx = solver.to_physical(1j * solver.KX * uz_hat)
    duz_dy = solver.to_physical(1j * solver.KY * uz_hat)
    duz_dz = solver.to_physical(1j * solver.KZ * uz_hat)

    # Vorticity: ω = ∇ × u
    omega_x = duz_dy - duy_dz
    omega_y = dux_dz - duz_dx
    omega_z = duy_dx - dux_dy

    # Energy: ½‖u‖²_{L²}
    u_sq = ux**2 + uy**2 + uz**2
    L2_sq = np.mean(u_sq) * vol
    energy = 0.5 * L2_sq

    # Dissipation rate: ε = 2ν ‖S‖²_{L²}  where S is strain rate tensor
    # For incompressible flow: ε = ν ‖∇u‖²_{L²} (using integration by parts)
    grad_sq = (dux_dx**2 + dux_dy**2 + dux_dz**2 +
               duy_dx**2 + duy_dy**2 + duy_dz**2 +
               duz_dx**2 + duz_dy**2 + duz_dz**2)
    gradL2_sq = np.mean(grad_sq) * vol
    dissipation = solver.nu * gradL2_sq  # ε = ν ‖∇u‖²

    # Enstrophy: ½‖ω‖²_{L²}
    omega_sq = omega_x**2 + omega_y**2 + omega_z**2
    enstrophy = 0.5 * np.mean(omega_sq) * vol

    # Note: for incompressible flow, enstrophy = ½‖∇u‖²_{L²} (Poincaré-like identity)
    # so enstrophy ≈ 0.5 * gradL2_sq and dissipation = 2 * nu * enstrophy

    # Divergence check: should be near machine epsilon
    div = dux_dx + duy_dy + duz_dz
    divergence_max = np.max(np.abs(div))

    # Energy spectrum: E(k) vs shell-averaged wavenumber
    # Computed via Parseval: ‖u‖² = (1/N³) Σ |û|²
    energy_spectrum = _compute_energy_spectrum(solver, ux_hat, uy_hat, uz_hat)

    result = {
        'energy':         energy,
        'dissipation':    dissipation,
        'enstrophy':      enstrophy,
        'gradL2_sq':      gradL2_sq,
        'divergence_max': divergence_max,
        'energy_spectrum': energy_spectrum,
    }

    if include_pressure:
        p_hat, p_phys = solver.compute_pressure(ux_hat, uy_hat, uz_hat)
        p_norms = solver.compute_pressure_norms(p_phys)
        result['pressure_L1']   = p_norms['L1']
        result['pressure_L1p5'] = p_norms['L1p5']
        result['pressure_L2']   = p_norms['L2']
        result['pressure_L3']   = p_norms['L3']
        result['pressure_Linf'] = p_norms['Linf']
        # Save p_phys for downstream use if needed
        result['pressure_field'] = p_phys

    return result


def _compute_energy_spectrum(solver, ux_hat, uy_hat, uz_hat):
    """Shell-averaged energy spectrum E(k).

    E(k) is the kinetic energy in the shell [k-0.5, k+0.5).
    Returns dict: {k_shell: E(k)} for integer k from 1 to N/2.
    """
    N = solver.N
    # Energy per Fourier mode: ½ |û|² / N^6 (Parseval normalization for numpy's fftn)
    # numpy's fftn: sum |û(k)|² / N³ = integral |u(x)|² dx / (2π)³ * (2π)³
    # Actually: for numpy fftn, Parseval: sum |û|² = N³ * sum |u|²
    # So ½ integral |u|² dx = ½ * (2π)³/N³ * sum |u_phys|²
    #                       = ½ * (2π)³/N^6 * sum |û|²
    vol = (2 * np.pi)**3
    norm = vol / N**6  # factor to convert sum |û|² → integral |u|² dx

    energy_sq = 0.5 * norm * (np.abs(ux_hat)**2 + np.abs(uy_hat)**2 + np.abs(uz_hat)**2)

    K_mag = solver.K_mag
    k_max = N // 2

    spectrum = {}
    for k in range(1, k_max + 1):
        mask = (K_mag >= k - 0.5) & (K_mag < k + 0.5)
        spectrum[k] = float(np.sum(energy_sq[mask]))

    return spectrum


# ------------------------------------------------------------------
# Simulation runner
# ------------------------------------------------------------------

def run_simulation(N, Re, T_end, diag_interval=0.5, include_pressure=True, verbose=True):
    """Run a Taylor-Green vortex simulation and collect diagnostics.

    Args:
        N: grid resolution
        Re: Reynolds number  (nu = 1/Re)
        T_end: end time
        diag_interval: time interval between diagnostic outputs
        include_pressure: whether to compute pressure diagnostics at diag points
        verbose: print progress

    Returns:
        dict with time series of diagnostic quantities and validation checks.

    Energy conservation check:
        We track E(t) and ∫ε dt where ε = ν‖∇u‖² at every time step.
        Both E and ε are computed from spectral coefficients via Parseval
        (no physical-space FFT required), so this is exact and efficient.
        The balance E(t) + ∫ε dt = E(0) should hold to ~O(dt⁴) RK4 accuracy.
    """
    nu = 1.0 / Re
    solver = NavierStokesSolver(N=N, nu=nu, cfl=0.5)

    if verbose:
        print(f"  Starting TGV simulation: N={N}, Re={Re}, nu={nu:.6f}, T_end={T_end}")

    # Taylor-Green initial condition
    ux_hat, uy_hat, uz_hat = taylor_green_ic(solver)

    # Initial spectral quantities (no FFT)
    E0 = solver.spectral_energy(ux_hat, uy_hat, uz_hat)
    eps0 = solver.spectral_dissipation(ux_hat, uy_hat, uz_hat)

    # Initial full diagnostics
    diag0 = compute_diagnostics(solver, ux_hat, uy_hat, uz_hat,
                                 include_pressure=include_pressure)

    if verbose:
        print(f"    t=0.00  E={E0:.6f}  enstrophy={diag0['enstrophy']:.6f}  "
              f"div_max={diag0['divergence_max']:.2e}")

    # Diagnostic time series (sampled every diag_interval)
    times          = [0.0]
    energy_ts      = [E0]
    enstrophy_ts   = [diag0['enstrophy']]
    dissipation_ts = [diag0['dissipation']]
    div_max_ts     = [diag0['divergence_max']]
    p_L1_ts        = [diag0.get('pressure_L1', None)]
    p_L1p5_ts      = [diag0.get('pressure_L1p5', None)]
    p_L2_ts        = [diag0.get('pressure_L2', None)]
    p_L3_ts        = [diag0.get('pressure_L3', None)]
    p_Linf_ts      = [diag0.get('pressure_Linf', None)]

    # Per-step energy conservation tracking
    # We accumulate ∫ε dt via trapezoidal rule at every step.
    # E_prev and eps_prev are the previous step's values.
    E_prev = E0
    eps_prev = eps0
    cumulative_dissipation_at_t = 0.0  # ∫₀ᵗ ε ds, updated at every step

    # For the energy conservation error, we need E(t) + ∫ε dt = E(0) at all diagnostic times.
    # We store (t, E(t) + ∫ε dt) at each diagnostic point to compute the max error.
    balance_ts = [E0]  # E(t) + ∫ε dt should equal E(0)

    t = 0.0
    next_diag = diag_interval
    step = 0
    while t < T_end:
        # Adaptive dt: need u_max for CFL (one physical-space computation)
        u_max = solver.spectral_max_u(ux_hat, uy_hat, uz_hat)
        dt = solver.compute_dt(ux_hat, uy_hat, uz_hat, u_max=u_max)
        dt = min(dt, next_diag - t + 1e-12, T_end - t + 1e-12)
        dt = max(dt, 1e-8)  # prevent infinite loops

        # Take RK4 step
        ux_hat, uy_hat, uz_hat = solver.rk4_step(ux_hat, uy_hat, uz_hat, dt)
        t += dt
        step += 1

        # Update energy conservation integral (spectral, no FFT)
        E_now = solver.spectral_energy(ux_hat, uy_hat, uz_hat)
        eps_now = solver.spectral_dissipation(ux_hat, uy_hat, uz_hat)
        cumulative_dissipation_at_t += 0.5 * (eps_prev + eps_now) * dt
        E_prev = E_now
        eps_prev = eps_now

        if t >= next_diag - 1e-10 or t >= T_end - 1e-10:
            # Full diagnostics at this output point
            diag = compute_diagnostics(solver, ux_hat, uy_hat, uz_hat,
                                        include_pressure=include_pressure)

            times.append(float(t))
            energy_ts.append(diag['energy'])
            enstrophy_ts.append(diag['enstrophy'])
            dissipation_ts.append(diag['dissipation'])
            div_max_ts.append(diag['divergence_max'])
            balance_ts.append(E_now + cumulative_dissipation_at_t)

            if include_pressure:
                p_L1_ts.append(diag.get('pressure_L1'))
                p_L1p5_ts.append(diag.get('pressure_L1p5'))
                p_L2_ts.append(diag.get('pressure_L2'))
                p_L3_ts.append(diag.get('pressure_L3'))
                p_Linf_ts.append(diag.get('pressure_Linf'))
            else:
                for lst in [p_L1_ts, p_L1p5_ts, p_L2_ts, p_L3_ts, p_Linf_ts]:
                    lst.append(None)

            if verbose:
                p_str = (f"  p_L1p5={diag.get('pressure_L1p5', 0):.4f}"
                         if include_pressure else "")
                print(f"    t={t:6.3f}  E={diag['energy']:.6f}  "
                      f"enstrophy={diag['enstrophy']:.4f}  "
                      f"div={diag['divergence_max']:.2e}{p_str}")

            next_diag += diag_interval

    # Enstrophy peak detection
    enstrophy_arr = np.array(enstrophy_ts)
    peak_idx = int(np.argmax(enstrophy_arr))
    enstrophy_peak_time  = times[peak_idx]
    enstrophy_peak_value = float(enstrophy_ts[peak_idx])

    # Energy conservation error: max |E(t) + ∫ε dt - E(0)| / E(0)
    balance_arr = np.array(balance_ts)
    energy_conservation_error = float(np.max(np.abs(balance_arr - E0)) / (E0 + 1e-30))

    if verbose:
        print(f"  --> Enstrophy peak: t={enstrophy_peak_time:.3f}, "
              f"value={enstrophy_peak_value:.4f}")
        print(f"  --> Energy conservation error: {energy_conservation_error:.2e}")
        print(f"  --> Total steps: {step}")

    return {
        'N':     N,
        'Re':    Re,
        'nu':    nu,
        'T_end': T_end,
        'times':          times,
        'energy':         energy_ts,
        'enstrophy':      enstrophy_ts,
        'dissipation':    dissipation_ts,
        'divergence_max': div_max_ts,
        'pressure_L1':    p_L1_ts,
        'pressure_L1p5':  p_L1p5_ts,
        'pressure_L2':    p_L2_ts,
        'pressure_L3':    p_L3_ts,
        'pressure_Linf':  p_Linf_ts,
        'enstrophy_peak_time':  enstrophy_peak_time,
        'enstrophy_peak_value': enstrophy_peak_value,
        'energy_conservation_error': energy_conservation_error,
        'E0':    E0,
        'total_steps': step,
    }
