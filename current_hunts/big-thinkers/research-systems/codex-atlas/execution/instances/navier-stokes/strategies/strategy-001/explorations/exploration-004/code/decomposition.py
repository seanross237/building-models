#!/usr/bin/env python3
"""
Vortex stretching slack decomposition and strain-vorticity alignment statistics.

Decomposes the total slack VS_bound / VS_actual into three factors:
  α_geom × α_Lad × α_sym = total_slack

And computes detailed alignment statistics between vorticity and strain eigenvectors.
"""

import numpy as np
from numpy.fft import fftn, ifftn, fftfreq
import sys
import os
import json
from pathlib import Path

# ============================================================================
# NS Solver (copied from exploration-002 with needed functions)
# ============================================================================

class NavierStokesSolver:
    """3D pseudospectral NS solver on periodic box [0, 2π]³."""

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
        px_hat = fx_hat - self.KX * kdotf
        py_hat = fy_hat - self.KY * kdotf
        pz_hat = fz_hat - self.KZ * kdotf
        return px_hat, py_hat, pz_hat

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


def taylor_green_ic(solver, Re):
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


# ============================================================================
# Core decomposition and alignment computations
# ============================================================================

def compute_full_gradients(solver, ux_hat, uy_hat, uz_hat):
    """Compute all 9 velocity gradient components in physical space."""
    grads = {}
    for i, (name_i, u_hat) in enumerate(zip(['x', 'y', 'z'], [ux_hat, uy_hat, uz_hat])):
        for j, (name_j, K_j) in enumerate(zip(['x', 'y', 'z'], [solver.KX, solver.KY, solver.KZ])):
            grads[f'du{name_i}_d{name_j}'] = solver.to_physical(1j * K_j * u_hat)
    return grads


def compute_strain_tensor(grads):
    """Compute strain rate tensor S_{ij} = 0.5 * (du_i/dx_j + du_j/dx_i) at each grid point.

    Returns: S as array of shape (N, N, N, 3, 3)
    """
    N = grads['dux_dx'].shape[0]
    S = np.zeros((N, N, N, 3, 3))

    names = ['x', 'y', 'z']
    for i in range(3):
        for j in range(3):
            key_ij = f'du{names[i]}_d{names[j]}'
            key_ji = f'du{names[j]}_d{names[i]}'
            S[:, :, :, i, j] = 0.5 * (grads[key_ij] + grads[key_ji])

    return S


def compute_vorticity(grads):
    """Compute vorticity ω = ∇ × u."""
    omega_x = grads['duz_dy'] - grads['duy_dz']
    omega_y = grads['dux_dz'] - grads['duz_dx']
    omega_z = grads['duy_dx'] - grads['dux_dy']
    return omega_x, omega_y, omega_z


def compute_curl_omega(solver, omega_x, omega_y, omega_z):
    """Compute ∇ω in spectral space for ||∇ω||_{L²}."""
    ox_hat = solver.to_spectral(omega_x)
    oy_hat = solver.to_spectral(omega_y)
    oz_hat = solver.to_spectral(omega_z)

    grad_omega_sq = 0.0
    for o_hat in [ox_hat, oy_hat, oz_hat]:
        for K_j in [solver.KX, solver.KY, solver.KZ]:
            deriv = solver.to_physical(1j * K_j * o_hat)
            grad_omega_sq += deriv**2

    return grad_omega_sq


def compute_decomposition(solver, ux_hat, uy_hat, uz_hat):
    """
    Compute the full decomposition of vortex stretching slack.

    Returns dict with all quantities needed for Part A and Part B.
    """
    N = solver.N
    vol = (2 * np.pi)**3

    # Compute velocity gradients
    grads = compute_full_gradients(solver, ux_hat, uy_hat, uz_hat)

    # Strain tensor
    S = compute_strain_tensor(grads)

    # Vorticity
    omega_x, omega_y, omega_z = compute_vorticity(grads)
    omega = np.stack([omega_x, omega_y, omega_z], axis=-1)  # (N,N,N,3)
    omega_sq = omega_x**2 + omega_y**2 + omega_z**2  # |ω|² at each point

    # ============================================================================
    # Part A: Slack decomposition
    # ============================================================================

    # 1. Actual vortex stretching: VS_actual = |∫ S_{ij} ω_i ω_j dx|
    # S_{ij} ω_i ω_j = ω^T S ω at each point
    Somega = np.einsum('...ij,...j->...i', S, omega)  # (N,N,N,3)
    omegaS_omega = np.sum(omega * Somega, axis=-1)    # (N,N,N) = ω·Sω at each point
    VS_actual = abs(np.mean(omegaS_omega) * vol)

    # 2. Hölder product: VS_Hölder = ||S||_{L²} × ||ω||²_{L⁴}
    # ||S||_{L²}² = ∫ S_{ij} S_{ij} dx = ∫ tr(S^T S) dx
    S_sq = np.sum(S**2, axis=(-2, -1))  # |S|² at each point (Frobenius norm squared)
    S_L2_sq = np.mean(S_sq) * vol
    S_L2 = np.sqrt(S_L2_sq)

    # ||ω||_{L⁴}² = (∫ |ω|⁴ dx)^{1/2}
    omega_L4_4 = np.mean(omega_sq**2) * vol
    omega_L4_sq = np.sqrt(omega_L4_4)  # ||ω||_{L⁴}²
    omega_L4 = omega_L4_4**0.25

    VS_Holder = S_L2 * omega_L4_sq

    # 3. ||ω||_{L²} and ||∇ω||_{L²}
    omega_L2_sq = np.mean(omega_sq) * vol
    omega_L2 = np.sqrt(omega_L2_sq)

    grad_omega_sq = compute_curl_omega(solver, omega_x, omega_y, omega_z)
    grad_omega_L2_sq = np.mean(grad_omega_sq) * vol
    grad_omega_L2 = np.sqrt(grad_omega_L2_sq)

    # 4. ||∇u||_{L²}
    grad_u_sq = sum(grads[key]**2 for key in grads)
    grad_u_L2_sq = np.mean(grad_u_sq) * vol
    grad_u_L2 = np.sqrt(grad_u_L2_sq)

    # 5. Ladyzhenskaya constant (scalar, R³)
    # ||f||_{L⁴} ≤ C_L ||f||_{L²}^{1/4} ||∇f||_{L²}^{3/4}
    # C_L = (8/(3√3 π²))^{1/4} ≈ 0.629 for scalar
    # For vector: C_L_vec = (3 × C_L⁴)^{1/4} ≈ 0.839
    # But in the VS chain, we need Ladyzhenskaya for ||ω||_{L⁴}
    # ω is a vector field, so use vector constant
    C_L4_scalar = 8.0 / (3.0 * np.sqrt(3.0) * np.pi**2)
    C_L_scalar = C_L4_scalar ** 0.25
    C_L4_vec = 3.0 * C_L4_scalar
    C_L_vec = C_L4_vec ** 0.25

    # The bound chain:
    # |∫ S_{ij} ω_i ω_j dx| ≤ ||S||_{L²} × ||ω||²_{L⁴}     (Hölder)
    #                        ≤ ||S||_{L²} × C²_L × ||ω||^{1/2}_{L²} × ||∇ω||^{3/2}_{L²}  (Ladyzhenskaya on ||ω||_{L⁴})
    #                        ≤ ||∇u||_{L²} × C²_L × ||ω||^{1/2}_{L²} × ||∇ω||^{3/2}_{L²}  (||S|| ≤ ||∇u||)
    # But actually for div-free: ||ω||_{L²} = ||∇u||_{L²} (for periodic, zero-mean)
    # So the bound becomes:
    # ≤ C²_L × ||∇u||_{L²} × ||ω||^{1/2}_{L²} × ||∇ω||^{3/2}_{L²}
    # = C²_L × ||ω||_{L²} × ||ω||^{1/2}_{L²} × ||∇ω||^{3/2}_{L²}   (using ||∇u|| = ||ω||)
    # = C²_L × ||ω||^{3/2}_{L²} × ||∇ω||^{3/2}_{L²}
    # Wait, that doesn't match the goal's formula.

    # Goal says: VS_bound = C²_L × ||ω||^{3/2}_{L²} × ||∇ω||^{3/2}_{L²}
    # This comes from:
    # |∫ S ω ω| ≤ ||S||_{L²} × ||ω||²_{L⁴}  (Hölder)
    # ||ω||²_{L⁴} ≤ C²_L × ||ω||^{1/2}_{L²} × ||∇ω||^{3/2}_{L²}  (Ladyzhenskaya squared)
    # ||S||_{L²} ≤ ||∇u||_{L²} = ||ω||_{L²}  (for periodic div-free)
    # So: ≤ ||ω||_{L²} × C²_L × ||ω||^{1/2}_{L²} × ||∇ω||^{3/2}_{L²}
    #     = C²_L × ||ω||^{3/2}_{L²} × ||∇ω||^{3/2}_{L²}

    # The Ladyzhenskaya bound on ||ω||²_{L⁴}:
    # ||ω||_{L⁴} ≤ C_L × ||ω||^{1/4}_{L²} × ||∇ω||^{3/4}_{L²}
    # ||ω||²_{L⁴} ≤ C²_L × ||ω||^{1/2}_{L²} × ||∇ω||^{3/2}_{L²}
    Lad_bound_omega_L4_sq = C_L_vec**2 * omega_L2**0.5 * grad_omega_L2**1.5

    VS_bound = grad_u_L2 * Lad_bound_omega_L4_sq  # using ||S|| ≤ ||∇u|| chain
    # But using ||∇u|| = ||ω||:
    VS_bound_via_omega = C_L_vec**2 * omega_L2**1.5 * grad_omega_L2**1.5

    # Decomposition factors
    if VS_actual > 1e-30:
        alpha_geom = VS_Holder / VS_actual
        alpha_Lad = Lad_bound_omega_L4_sq / omega_L4_sq
        alpha_sym = grad_u_L2 / S_L2
        total_check = VS_bound / VS_actual
        product_check = alpha_geom * alpha_Lad * alpha_sym
    else:
        alpha_geom = alpha_Lad = alpha_sym = total_check = product_check = float('inf')

    # ============================================================================
    # Part B: Alignment statistics
    # ============================================================================

    alignment_stats = compute_alignment_statistics(S, omega, omega_sq, vol, N)

    # ============================================================================
    # Compile results
    # ============================================================================

    results = {
        # Part A quantities
        'VS_actual': VS_actual,
        'VS_Holder': VS_Holder,
        'VS_bound': VS_bound,
        'VS_bound_via_omega': VS_bound_via_omega,
        'S_L2': S_L2,
        'omega_L2': omega_L2,
        'omega_L4': omega_L4,
        'omega_L4_sq': omega_L4_sq,
        'grad_omega_L2': grad_omega_L2,
        'grad_u_L2': grad_u_L2,
        'Lad_bound_omega_L4_sq': Lad_bound_omega_L4_sq,
        'C_L_vec': C_L_vec,
        'alpha_geom': alpha_geom,
        'alpha_Lad': alpha_Lad,
        'alpha_sym': alpha_sym,
        'total_slack': total_check,
        'product_check': product_check,
        'enstrophy': 0.5 * omega_L2_sq,
        # Part B
        **alignment_stats,
    }

    return results


def compute_alignment_statistics(S, omega, omega_sq, vol, N):
    """
    Compute strain-vorticity alignment statistics.

    At each grid point:
    1. Eigendecompose S to get λ₁ ≥ λ₂ ≥ λ₃ and eigenvectors e₁, e₂, e₃
    2. Compute cos²(θ_i) = (ω̂ · e_i)² for i=1,2,3
    3. Compute volume-averaged and enstrophy-weighted statistics
    """
    # Flatten spatial dimensions for eigendecomposition
    S_flat = S.reshape(-1, 3, 3)  # (N³, 3, 3)
    omega_flat = omega.reshape(-1, 3)  # (N³, 3)
    omega_sq_flat = omega_sq.reshape(-1)  # (N³,)

    n_points = S_flat.shape[0]

    # Eigendecomposition of S at each point
    # np.linalg.eigh returns sorted eigenvalues in ascending order
    eigenvalues, eigenvectors = np.linalg.eigh(S_flat)  # eigenvalues: (N³, 3), eigvecs: (N³, 3, 3)

    # eigh returns ascending order: λ₃ ≤ λ₂ ≤ λ₁ → reverse to get λ₁ ≥ λ₂ ≥ λ₃
    eigenvalues = eigenvalues[:, ::-1]  # (N³, 3) now λ₁ ≥ λ₂ ≥ λ₃
    eigenvectors = eigenvectors[:, :, ::-1]  # (N³, 3, 3) columns reversed

    lambda_1 = eigenvalues[:, 0]
    lambda_2 = eigenvalues[:, 1]
    lambda_3 = eigenvalues[:, 2]

    # Vorticity unit vector
    omega_mag = np.sqrt(omega_sq_flat)
    # Avoid division by zero at points where |ω| ≈ 0
    mask = omega_mag > 1e-12 * np.max(omega_mag)
    omega_hat = np.zeros_like(omega_flat)
    omega_hat[mask] = omega_flat[mask] / omega_mag[mask, np.newaxis]

    # cos²(θ_i) = (ω̂ · e_i)² for i=1,2,3
    # eigenvectors[:, :, i] is the i-th eigenvector
    cos2_theta = np.zeros((n_points, 3))
    for i in range(3):
        dot = np.sum(omega_hat * eigenvectors[:, :, i], axis=-1)  # (N³,)
        cos2_theta[:, i] = dot**2

    # Volume-averaged alignment (uniform weight)
    dV = vol / N**3
    cos2_vol_avg = np.mean(cos2_theta, axis=0)  # (3,)

    # Enstrophy-weighted alignment: ⟨cos²θ_i⟩_ω = ∫ cos²θ_i |ω|² dx / ∫ |ω|² dx
    total_enstrophy = np.sum(omega_sq_flat)
    if total_enstrophy > 1e-30:
        cos2_enstrophy_avg = np.zeros(3)
        for i in range(3):
            cos2_enstrophy_avg[i] = np.sum(cos2_theta[:, i] * omega_sq_flat) / total_enstrophy
    else:
        cos2_enstrophy_avg = np.array([1/3, 1/3, 1/3])

    # Eigenvalue statistics (enstrophy-weighted)
    if total_enstrophy > 1e-30:
        lambda_avg = np.zeros(3)
        for i in range(3):
            lambda_avg[i] = np.sum(eigenvalues[:, i] * omega_sq_flat) / total_enstrophy
    else:
        lambda_avg = np.zeros(3)

    # Constantin-Fefferman depletion factor
    # Actual: ∫ (λ₁ cos²θ₁ + λ₂ cos²θ₂ + λ₃ cos²θ₃) |ω|² dx
    actual_alignment_integral = np.sum(
        (lambda_1 * cos2_theta[:, 0] + lambda_2 * cos2_theta[:, 1] + lambda_3 * cos2_theta[:, 2])
        * omega_sq_flat
    ) * dV

    # Worst case: all vorticity aligned with λ₁ (maximum stretching)
    worst_case_integral = np.sum(lambda_1 * omega_sq_flat) * dV

    if abs(worst_case_integral) > 1e-30:
        depletion_factor = actual_alignment_integral / worst_case_integral
    else:
        depletion_factor = 1.0

    # Histograms of cos²θ at each eigenvalue, weighted by enstrophy
    n_bins = 50
    hist_data = {}
    for i, name in enumerate(['extensional', 'intermediate', 'compressive']):
        # Only include points with significant vorticity
        weights = omega_sq_flat[mask]
        values = cos2_theta[mask, i]
        hist, bin_edges = np.histogram(values, bins=n_bins, range=(0, 1), weights=weights, density=True)
        bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
        hist_data[name] = {'centers': bin_centers.tolist(), 'density': hist.tolist()}

    # Vorticity direction gradient ||∇ξ||_{L²}
    # ξ = ω/|ω|, but this requires careful computation at points where |ω| is small
    # We'll compute this separately to avoid numerical issues
    xi_grad_L2 = compute_vorticity_direction_gradient(omega_flat.reshape(N, N, N, 3),
                                                        omega_mag.reshape(N, N, N),
                                                        mask.reshape(N, N, N),
                                                        N, vol)

    # Check incompressibility of eigenvalues
    trace_check = np.mean(np.abs(lambda_1 + lambda_2 + lambda_3))

    return {
        'cos2_vol_avg': cos2_vol_avg.tolist(),
        'cos2_enstrophy_avg': cos2_enstrophy_avg.tolist(),
        'lambda_avg': lambda_avg.tolist(),
        'depletion_factor': depletion_factor,
        'actual_alignment_integral': actual_alignment_integral,
        'worst_case_integral': worst_case_integral,
        'hist_data': hist_data,
        'xi_grad_L2': xi_grad_L2,
        'trace_check': trace_check,
    }


def compute_vorticity_direction_gradient(omega_3d, omega_mag_3d, mask_3d, N, vol):
    """
    Compute ||∇ξ||_{L²} where ξ = ω/|ω| (Constantin-Fefferman quantity).

    Uses spectral differentiation on the ξ field, restricted to regions where |ω| > threshold.
    """
    # Compute ξ = ω/|ω| at points with sufficient vorticity
    xi = np.zeros_like(omega_3d)
    omega_mag_safe = np.where(mask_3d, omega_mag_3d, 1.0)
    xi = omega_3d / omega_mag_safe[..., np.newaxis]
    xi[~mask_3d] = 0.0  # zero out where vorticity is too small

    # Compute ∇ξ via finite differences (spectral differentiation would require FFT of discontinuous field)
    # Use periodic finite differences: (ξ[i+1] - ξ[i-1]) / (2dx)
    dx = 2 * np.pi / N

    grad_xi_sq = 0.0
    for comp in range(3):  # components of ξ
        for axis in range(3):  # differentiation direction
            dxi = (np.roll(xi[..., comp], -1, axis=axis) - np.roll(xi[..., comp], 1, axis=axis)) / (2 * dx)
            grad_xi_sq += dxi**2

    # Weight by mask and integrate
    grad_xi_sq_masked = grad_xi_sq * mask_3d
    xi_grad_L2_sq = np.mean(grad_xi_sq_masked) * vol
    xi_grad_L2 = np.sqrt(xi_grad_L2_sq)

    return xi_grad_L2


# ============================================================================
# Main simulation and data collection
# ============================================================================

def run_simulation(N, Re, T_final, n_snapshots=20):
    """Run NS simulation and collect decomposition data at regular intervals."""
    nu = 1.0 / Re
    solver = NavierStokesSolver(N, nu, cfl=0.4)
    ux_hat, uy_hat, uz_hat = taylor_green_ic(solver, Re)

    t = 0.0
    dt_snap = T_final / n_snapshots
    next_snap = 0.0

    results_list = []
    step = 0

    print(f"Running Re={Re}, N={N}, T_final={T_final}, n_snapshots={n_snapshots}")
    print(f"ν = {nu:.6e}")

    while t < T_final:
        # Snapshot
        if t >= next_snap - 1e-10:
            print(f"  t={t:.4f}: Computing decomposition...", end='', flush=True)
            res = compute_decomposition(solver, ux_hat, uy_hat, uz_hat)
            res['t'] = t
            res['step'] = step
            results_list.append(res)
            print(f" VS_actual={res['VS_actual']:.4e}, α_geom={res['alpha_geom']:.2f}, "
                  f"α_Lad={res['alpha_Lad']:.2f}, α_sym={res['alpha_sym']:.4f}, "
                  f"product={res['product_check']:.2f}")
            next_snap += dt_snap

        # Time step
        dt = solver.compute_dt(ux_hat, uy_hat, uz_hat)
        dt = min(dt, T_final - t)
        if dt < 1e-15:
            break
        ux_hat, uy_hat, uz_hat = solver.rk4_step(ux_hat, uy_hat, uz_hat, dt)
        t += dt
        step += 1

    # Final snapshot
    if abs(t - results_list[-1]['t']) > 1e-10:
        print(f"  t={t:.4f}: Computing final decomposition...", end='', flush=True)
        res = compute_decomposition(solver, ux_hat, uy_hat, uz_hat)
        res['t'] = t
        res['step'] = step
        results_list.append(res)
        print(f" VS_actual={res['VS_actual']:.4e}, α_geom={res['alpha_geom']:.2f}")

    return results_list


def save_results(results_list, Re, output_dir):
    """Save results to JSON, converting numpy types."""
    def convert(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (np.float64, np.float32)):
            return float(obj)
        if isinstance(obj, (np.int64, np.int32)):
            return int(obj)
        return obj

    clean_results = []
    for r in results_list:
        clean = {}
        for k, v in r.items():
            clean[k] = convert(v)
        clean_results.append(clean)

    filepath = os.path.join(output_dir, f'results_Re{Re}.json')
    with open(filepath, 'w') as f:
        json.dump(clean_results, f, indent=2, default=convert)
    print(f"Results saved to {filepath}")


if __name__ == '__main__':
    output_dir = Path(__file__).parent

    # Run Re=100 first (faster, for validation)
    print("=" * 80)
    print("Re = 100 simulation")
    print("=" * 80)
    results_100 = run_simulation(N=48, Re=100, T_final=3.0, n_snapshots=15)
    save_results(results_100, 100, output_dir)

    # Run Re=1000 (higher resolution needed)
    print("\n" + "=" * 80)
    print("Re = 1000 simulation")
    print("=" * 80)
    results_1000 = run_simulation(N=64, Re=1000, T_final=2.0, n_snapshots=15)
    save_results(results_1000, 1000, output_dir)

    # Print summary tables
    print("\n" + "=" * 80)
    print("SUMMARY: Re=100 Slack Decomposition")
    print("=" * 80)
    print(f"{'t':>6s} {'VS_actual':>12s} {'VS_Hölder':>12s} {'VS_bound':>12s} {'α_geom':>8s} {'α_Lad':>8s} {'α_sym':>8s} {'Product':>8s} {'Total':>8s}")
    for r in results_100:
        print(f"{r['t']:6.3f} {r['VS_actual']:12.4e} {r['VS_Holder']:12.4e} {r['VS_bound']:12.4e} "
              f"{r['alpha_geom']:8.2f} {r['alpha_Lad']:8.2f} {r['alpha_sym']:8.4f} "
              f"{r['product_check']:8.2f} {r['total_slack']:8.2f}")

    print("\n" + "=" * 80)
    print("SUMMARY: Re=1000 Slack Decomposition")
    print("=" * 80)
    print(f"{'t':>6s} {'VS_actual':>12s} {'VS_Hölder':>12s} {'VS_bound':>12s} {'α_geom':>8s} {'α_Lad':>8s} {'α_sym':>8s} {'Product':>8s} {'Total':>8s}")
    for r in results_1000:
        print(f"{r['t']:6.3f} {r['VS_actual']:12.4e} {r['VS_Holder']:12.4e} {r['VS_bound']:12.4e} "
              f"{r['alpha_geom']:8.2f} {r['alpha_Lad']:8.2f} {r['alpha_sym']:8.4f} "
              f"{r['product_check']:8.2f} {r['total_slack']:8.2f}")

    print("\n" + "=" * 80)
    print("ALIGNMENT STATISTICS (Re=1000, peak enstrophy)")
    print("=" * 80)
    # Find peak enstrophy timestep
    peak_idx = max(range(len(results_1000)), key=lambda i: results_1000[i]['enstrophy'])
    r = results_1000[peak_idx]
    print(f"Peak enstrophy at t={r['t']:.4f}")
    print(f"Enstrophy-weighted alignment: cos²θ₁={r['cos2_enstrophy_avg'][0]:.4f}, "
          f"cos²θ₂={r['cos2_enstrophy_avg'][1]:.4f}, cos²θ₃={r['cos2_enstrophy_avg'][2]:.4f}")
    print(f"(Isotropic expectation: 1/3 ≈ 0.3333 for each)")
    print(f"Volume-averaged alignment: cos²θ₁={r['cos2_vol_avg'][0]:.4f}, "
          f"cos²θ₂={r['cos2_vol_avg'][1]:.4f}, cos²θ₃={r['cos2_vol_avg'][2]:.4f}")
    print(f"Enstrophy-weighted eigenvalues: λ₁={r['lambda_avg'][0]:.4f}, "
          f"λ₂={r['lambda_avg'][1]:.4f}, λ₃={r['lambda_avg'][2]:.4f}")
    print(f"Depletion factor: {r['depletion_factor']:.4f}")
    print(f"||∇ξ||_{{L²}}: {r['xi_grad_L2']:.4f}")
    print(f"Trace check (should be ~0): {r['trace_check']:.2e}")
