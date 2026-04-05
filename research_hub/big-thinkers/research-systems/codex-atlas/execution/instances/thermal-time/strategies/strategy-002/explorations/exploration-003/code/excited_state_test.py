#!/usr/bin/env python3
"""
Excited-State Modular Flow: Testing State-Dependent Time in TTH
================================================================

For a one-particle excitation |1_m> = b_m^+ |0> of a free scalar field on a
1+1D lattice, computes and compares:
  C_local(tau): correlator under modular flow of the excited-state reduced density matrix
  C_full(tau):  correlator under full Hamiltonian evolution

Uses Dirichlet BC (no zero mode), Williamson decomposition for the bosonic
modular Hamiltonian, and the Gaussian approximation for the excited state.

The excited state's two-point functions have rank-1 corrections:
  X^(1) = X^(0) + u_m u_m^T / omega_m
  P^(1) = P^(0) + u_m u_m^T * omega_m

These are exact, but the state is non-Gaussian. The Gaussian approximation
constructs a modular Hamiltonian from these modified covariance matrices.

References:
- Peschel 2003, J. Phys. A 36 L205
- Casini & Huerta 2009, J. Phys. A 42, 504007
- Lashkari 2016, arXiv:1508.03506
"""

import numpy as np
from scipy.linalg import expm, eigh
import json
import os
import sys

# ============================================================================
# Stage 1: Lattice Setup (Dirichlet BC, from exploration-001)
# ============================================================================

def build_lattice(N):
    """
    Free massless scalar field on N sites with Dirichlet BC.
    H = (1/2) sum_i [pi_i^2 + (phi_{i+1} - phi_i)^2]
    with phi_0 = phi_{N+1} = 0.

    Returns: omega (frequencies), U (mode functions), K (coupling matrix)
    """
    K = np.zeros((N, N))
    for i in range(N):
        K[i, i] = 2.0
        if i > 0:
            K[i, i-1] = -1.0
        if i < N-1:
            K[i, i+1] = -1.0

    # Analytical eigensystem
    k_modes = np.arange(1, N+1)
    omega_sq = 4.0 * np.sin(np.pi * k_modes / (2*(N+1)))**2
    omega = np.sqrt(omega_sq)

    # U[j,k] = sqrt(2/(N+1)) * sin(pi*(j+1)*(k)/(N+1))
    j_sites = np.arange(N)
    U = np.sqrt(2.0/(N+1)) * np.sin(np.pi * np.outer(j_sites+1, k_modes) / (N+1))

    return omega, U, K


# ============================================================================
# Stage 2: Vacuum Correlation Matrices
# ============================================================================

def vacuum_correlations(omega, U):
    """
    X_ij = <0|phi_i phi_j|0> = sum_k U[i,k]*U[j,k] / (2*omega_k)
    P_ij = <0|pi_i pi_j|0>  = sum_k U[i,k]*U[j,k] * omega_k / 2
    """
    X = U @ np.diag(1.0 / (2.0 * omega)) @ U.T
    P = U @ np.diag(omega / 2.0) @ U.T
    return X, P


def restrict_to_subsystem(M, start, n):
    """Restrict matrix M to sites [start, start+n)."""
    idx = list(range(start, start + n))
    return M[np.ix_(idx, idx)]


# ============================================================================
# Stage 3: Excited-State Correlation Matrices
# ============================================================================

def excited_correlations(omega, U, mode_idx):
    """
    For |1_m> = b_m^+ |0>, the two-point functions are:
    X^(1)_{ij} = X^(0)_{ij} + U[i,m]*U[j,m] / omega_m
    P^(1)_{ij} = P^(0)_{ij} + U[i,m]*U[j,m] * omega_m

    These are EXACT (derived from Wick's theorem for one-particle states).
    """
    m = mode_idx
    X0 = U @ np.diag(1.0 / (2.0 * omega)) @ U.T
    P0 = U @ np.diag(omega / 2.0) @ U.T

    u_m = U[:, m]
    X1 = X0 + np.outer(u_m, u_m) / omega[m]
    P1 = P0 + np.outer(u_m, u_m) * omega[m]

    return X1, P1, X0, P0


# ============================================================================
# Stage 4: Modular Hamiltonian via Williamson Decomposition
# ============================================================================

def matrix_sqrt_sym(A):
    """Matrix square root of symmetric positive (semi-)definite matrix."""
    eigvals, V = eigh(A)
    eigvals = np.maximum(eigvals, 0.0)
    return V @ np.diag(np.sqrt(eigvals)) @ V.T


def compute_modular_hamiltonian(X_R, P_R, epsilon_max=200.0):
    """
    Compute modular Hamiltonian K = (1/2) phi^T h_phi phi + (1/2) pi^T h_pi pi
    via Williamson decomposition.

    Returns: h_phi, h_pi, epsilon (modular energies), nu (symplectic eigenvalues),
             recon_err (reconstruction error)
    """
    n = X_R.shape[0]
    X_half = matrix_sqrt_sym(X_R)
    X_half_inv = np.linalg.inv(X_half)

    D = X_half @ P_R @ X_half
    D = (D + D.T) / 2.0  # Symmetrize

    nu_sq, V = eigh(D)
    nu = np.sqrt(np.maximum(nu_sq, 0.25))  # nu >= 1/2

    # Sort
    sort_idx = np.argsort(nu)
    nu = nu[sort_idx]
    V = V[:, sort_idx]

    # Modular energies
    ratio = (2*nu + 1) / np.maximum(2*nu - 1, 1e-15)
    epsilon = np.log(ratio)
    epsilon = np.minimum(epsilon, epsilon_max)

    # Williamson transformation
    S_phi = np.diag(np.sqrt(nu)) @ V.T @ X_half_inv
    S_pi = np.diag(1.0/np.sqrt(nu)) @ V.T @ X_half

    # Modular Hamiltonian matrices
    h_phi = S_phi.T @ np.diag(epsilon) @ S_phi
    h_pi = S_pi.T @ np.diag(epsilon) @ S_pi

    # Symmetrize
    h_phi = (h_phi + h_phi.T) / 2
    h_pi = (h_pi + h_pi.T) / 2

    # Verify reconstruction
    X_R_recon = np.linalg.inv(S_phi) @ np.diag(nu) @ np.linalg.inv(S_phi.T)
    recon_err = np.linalg.norm(X_R - X_R_recon) / np.linalg.norm(X_R)

    return h_phi, h_pi, epsilon, nu, recon_err


# ============================================================================
# Stage 5: Correlator Computation
# ============================================================================

def compute_modular_correlator(h_phi, h_pi, X_R, P_R, probe, tau_array):
    """
    C_local(tau) = Tr[rho sigma_tau(phi_k) phi_k]

    Modular flow: xi(tau) = exp(A*tau) xi(0)
    A = [[0, h_pi/(2pi)], [-h_phi/(2pi), 0]]

    For a Gaussian state: C_local(tau) = [e^{A tau} Sigma]_{k,k}
    where Sigma = [[X_R, (i/2)I], [(-i/2)I, P_R]] is the unsymmetrized correlation matrix.

    Using the REAL (symmetrized) correlator:
    C_local(tau) = Re[e^{A tau} Sigma]_{k,k} = [e^{A tau} Sigma_sym]_{k,k}
    where Sigma_sym = [[X_R, 0], [0, P_R]].

    Note: The exploration-001 code uses this real/symmetrized form.
    We compute both real and complex parts.
    """
    n = X_R.shape[0]
    k = probe

    # Evolution generator
    A = np.zeros((2*n, 2*n))
    A[:n, n:] = h_pi / (2*np.pi)
    A[n:, :n] = -h_phi / (2*np.pi)

    # Full (complex) correlation matrix <xi_i xi_j>
    Sigma_complex = np.zeros((2*n, 2*n), dtype=complex)
    Sigma_complex[:n, :n] = X_R
    Sigma_complex[n:, n:] = P_R
    Sigma_complex[:n, n:] = (1j/2) * np.eye(n)
    Sigma_complex[n:, :n] = (-1j/2) * np.eye(n)

    # Symmetrized correlation matrix
    Sigma_real = np.zeros((2*n, 2*n))
    Sigma_real[:n, :n] = X_R
    Sigma_real[n:, n:] = P_R

    C_complex = np.zeros(len(tau_array), dtype=complex)
    C_real = np.zeros(len(tau_array))

    for idx, tau in enumerate(tau_array):
        eAt = expm(A * tau)
        C_complex[idx] = (eAt @ Sigma_complex)[k, k]
        C_real[idx] = (eAt @ Sigma_real)[k, k]

    return C_real, C_complex


def compute_full_correlator_vacuum(omega, U, probe_global, tau_array):
    """
    C_full^(0)(tau) = <0|phi_k(tau) phi_k(0)|0>

    Real (symmetrized) part:
    Re[C] = sum_m U[k,m]^2 cos(omega_m tau) / (2 omega_m)

    Full Wightman function:
    C = sum_m U[k,m]^2 exp(-i omega_m tau) / (2 omega_m)
    """
    k = probe_global
    N = len(omega)

    C_real = np.zeros(len(tau_array))
    C_complex = np.zeros(len(tau_array), dtype=complex)

    for m in range(N):
        weight = U[k, m]**2 / (2.0 * omega[m])
        C_real += weight * np.cos(omega[m] * tau_array)
        C_complex += weight * np.exp(-1j * omega[m] * tau_array)

    return C_real, C_complex


def compute_full_correlator_excited(omega, U, probe_global, mode_idx, tau_array):
    """
    C_full^(1)(tau) = <1_m|phi_k(tau) phi_k(0)|1_m>

    = C_full^(0)(tau) + U[k,m]^2 / omega_m * cos(omega_m tau)

    This is EXACT (from Wick's theorem for the one-particle state).
    The correction is a single cosine at the excited mode's frequency.
    """
    m = mode_idx
    k = probe_global

    C0_real, C0_complex = compute_full_correlator_vacuum(omega, U, k, tau_array)

    correction_real = U[k, m]**2 / omega[m] * np.cos(omega[m] * tau_array)
    correction_complex = U[k, m]**2 / omega[m] * np.cos(omega[m] * tau_array)

    return C0_real + correction_real, C0_complex + correction_complex


# ============================================================================
# Stage 6: Mode Selection
# ============================================================================

def select_boundary_mode(U, N, omega):
    """
    Select the mode with maximum amplitude near the boundary between
    left and right sublattices (site N//2 - 1 or N//2, 0-indexed).

    Returns: mode_idx, mode_info dict
    """
    n_R = N - N // 2
    boundary_site = N // 2  # first right sublattice site (0-indexed)

    # Amplitude at boundary for each mode
    amplitudes = np.abs(U[boundary_site, :])

    # Also consider amplitude at boundary-1
    if boundary_site > 0:
        amplitudes_left = np.abs(U[boundary_site - 1, :])
        amplitudes = np.maximum(amplitudes, amplitudes_left)

    mode_idx = np.argmax(amplitudes)

    # Also compute the fraction of mode weight in right sublattice
    right_sites = np.arange(N // 2, N)
    p_R = np.sum(U[right_sites, mode_idx]**2)

    info = {
        'mode_idx': int(mode_idx),
        'frequency': float(omega[mode_idx]),
        'boundary_amplitude': float(np.abs(U[boundary_site, mode_idx])),
        'p_R': float(p_R),  # probability of excitation being in R
    }

    return mode_idx, info


# ============================================================================
# Main Computation
# ============================================================================

def run_full_test(N, tau_max=15.0, n_tau=800, verbose=True):
    """Run the complete excited-state modular flow test."""

    start_site = N // 2  # first site of right sublattice
    n_R = N - start_site

    if verbose:
        print(f"\n{'='*70}")
        print(f"  EXCITED-STATE MODULAR FLOW TEST: N = {N}")
        print(f"{'='*70}")

    # --- Stage 1: Build lattice ---
    omega, U, K_mat = build_lattice(N)
    if verbose:
        print(f"\nStage 1: Lattice (Dirichlet BC)")
        print(f"  N = {N}, n_R = {n_R}")
        print(f"  omega range: [{omega.min():.6f}, {omega.max():.6f}]")

    # --- Stage 2: Vacuum correlations ---
    X_full, P_full = vacuum_correlations(omega, U)
    X_R_vac = restrict_to_subsystem(X_full, start_site, n_R)
    P_R_vac = restrict_to_subsystem(P_full, start_site, n_R)

    # Uncertainty relation check
    XP_eigs = np.sort(np.real(np.linalg.eigvals(X_R_vac @ P_R_vac)))
    if verbose:
        print(f"\nStage 2: Vacuum correlations")
        print(f"  XP eigenvalue range: [{XP_eigs.min():.6f}, {XP_eigs.max():.6f}]")
        print(f"  min XP eig >= 0.25: {XP_eigs.min() >= 0.25 - 1e-10}")

    # --- Stage 3: Vacuum modular Hamiltonian ---
    h_phi_vac, h_pi_vac, eps_vac, nu_vac, recon_err_vac = compute_modular_hamiltonian(X_R_vac, P_R_vac)
    if verbose:
        print(f"\nStage 3: Vacuum modular Hamiltonian")
        print(f"  Symplectic eigenvalues: [{nu_vac.min():.6f}, {nu_vac.max():.6f}]")
        print(f"  # entangled modes (nu > 0.501): {np.sum(nu_vac > 0.501)}/{n_R}")
        print(f"  Modular energies: [{eps_vac.min():.4f}, {eps_vac.max():.4f}]")
        print(f"  Reconstruction error: {recon_err_vac:.2e}")

    # --- Stage 4: Mode selection ---
    mode_idx, mode_info = select_boundary_mode(U, N, omega)
    if verbose:
        print(f"\nStage 4: Excited mode selection")
        print(f"  Mode index: {mode_info['mode_idx']}")
        print(f"  Frequency: omega_m = {mode_info['frequency']:.6f}")
        print(f"  |u_m(boundary)| = {mode_info['boundary_amplitude']:.6f}")
        print(f"  p_R (weight in right sublattice) = {mode_info['p_R']:.6f}")

    # --- Stage 5: Excited-state correlations ---
    X1_full, P1_full, X0_full, P0_full = excited_correlations(omega, U, mode_idx)
    X_R_exc = restrict_to_subsystem(X1_full, start_site, n_R)
    P_R_exc = restrict_to_subsystem(P1_full, start_site, n_R)

    # Verify positive definiteness
    X_exc_eigs = np.linalg.eigvalsh(X_R_exc)
    P_exc_eigs = np.linalg.eigvalsh(P_R_exc)
    XP_exc_eigs = np.sort(np.real(np.linalg.eigvals(X_R_exc @ P_R_exc)))

    if verbose:
        print(f"\nStage 5: Excited-state correlations (Gaussian approx)")
        print(f"  X_R^(1) eigenvalues: [{X_exc_eigs.min():.6f}, {X_exc_eigs.max():.6f}]")
        print(f"  P_R^(1) eigenvalues: [{P_exc_eigs.min():.6f}, {P_exc_eigs.max():.6f}]")
        print(f"  XP^(1) eigenvalue range: [{XP_exc_eigs.min():.6f}, {XP_exc_eigs.max():.6f}]")

    # --- Stage 6: Excited-state modular Hamiltonian ---
    h_phi_exc, h_pi_exc, eps_exc, nu_exc, recon_err_exc = compute_modular_hamiltonian(X_R_exc, P_R_exc)
    if verbose:
        print(f"\nStage 6: Excited-state modular Hamiltonian (Gaussian approx)")
        print(f"  Symplectic eigenvalues: [{nu_exc.min():.6f}, {nu_exc.max():.6f}]")
        print(f"  Modular energies: [{eps_exc.min():.4f}, {eps_exc.max():.4f}]")
        print(f"  Reconstruction error: {recon_err_exc:.2e}")

        # Compare modular Hamiltonian change
        dh_phi = h_phi_exc - h_phi_vac
        dh_pi = h_pi_exc - h_pi_vac
        print(f"  ||delta h_phi|| / ||h_phi_vac|| = {np.linalg.norm(dh_phi)/np.linalg.norm(h_phi_vac):.6f}")
        print(f"  ||delta h_pi|| / ||h_pi_vac|| = {np.linalg.norm(dh_pi)/np.linalg.norm(h_pi_vac):.6f}")

    # --- Stage 7: Compute correlators ---
    tau_array = np.linspace(0, tau_max, n_tau)

    # Multiple probe sites
    probes = {
        'near_boundary': 2,       # 2 sites from boundary
        'quarter': n_R // 4,      # quarter into sublattice
        'mid': n_R // 2,          # middle of sublattice
    }

    all_results = {
        'N': N, 'n_R': n_R, 'start_site': start_site,
        'mode_info': mode_info,
        'tau_max': tau_max, 'n_tau': n_tau,
        'nu_vac': nu_vac.tolist(),
        'nu_exc': nu_exc.tolist(),
        'eps_vac': eps_vac.tolist(),
        'eps_exc': eps_exc.tolist(),
        'recon_err_vac': recon_err_vac,
        'recon_err_exc': recon_err_exc,
        'probes': {},
    }

    for probe_name, probe_local in probes.items():
        if probe_local >= n_R:
            continue

        probe_global = start_site + probe_local

        if verbose:
            print(f"\n--- Probe: {probe_name} (local={probe_local}, global={probe_global}) ---")

        # Vacuum correlators
        C_local_vac_real, C_local_vac_cplx = compute_modular_correlator(
            h_phi_vac, h_pi_vac, X_R_vac, P_R_vac, probe_local, tau_array
        )
        C_full_vac_real, C_full_vac_cplx = compute_full_correlator_vacuum(
            omega, U, probe_global, tau_array
        )

        # Excited-state correlators
        C_local_exc_real, C_local_exc_cplx = compute_modular_correlator(
            h_phi_exc, h_pi_exc, X_R_exc, P_R_exc, probe_local, tau_array
        )
        C_full_exc_real, C_full_exc_cplx = compute_full_correlator_excited(
            omega, U, probe_global, mode_idx, tau_array
        )

        # === Analysis ===

        # Equal-time check
        et_vac = abs(C_local_vac_real[0] - C_full_vac_real[0])
        et_exc = abs(C_local_exc_real[0] - C_full_exc_real[0])

        # L2 relative discrepancy
        def l2_rel(a, b):
            diff = np.sqrt(np.mean((a - b)**2))
            norm = np.sqrt(np.mean(b**2))
            return diff / norm if norm > 1e-15 else float('inf')

        def linf_rel(a, b):
            diff = np.max(np.abs(a - b))
            norm = np.max(np.abs(b))
            return diff / norm if norm > 1e-15 else float('inf')

        disc_vac_l2 = l2_rel(C_local_vac_real, C_full_vac_real)
        disc_exc_l2 = l2_rel(C_local_exc_real, C_full_exc_real)
        disc_vac_linf = linf_rel(C_local_vac_real, C_full_vac_real)
        disc_exc_linf = linf_rel(C_local_exc_real, C_full_exc_real)

        # State-dependence: delta_C = C^(1) - C^(0)
        delta_C_local = C_local_exc_real - C_local_vac_real
        delta_C_full = C_full_exc_real - C_full_vac_real

        delta_disc_l2 = l2_rel(delta_C_local, delta_C_full)
        delta_disc_linf = linf_rel(delta_C_local, delta_C_full)

        if verbose:
            print(f"  Equal-time check: |C_loc(0)-C_full(0)| = {et_vac:.2e} (vac), {et_exc:.2e} (exc)")
            print(f"  Vacuum discrepancy:  L2={disc_vac_l2:.6f}, Linf={disc_vac_linf:.6f}")
            print(f"  Excited discrepancy: L2={disc_exc_l2:.6f}, Linf={disc_exc_linf:.6f}")
            print(f"  max|delta_C_local| = {np.max(np.abs(delta_C_local)):.6e}")
            print(f"  max|delta_C_full|  = {np.max(np.abs(delta_C_full)):.6e}")
            print(f"  State-dep discrepancy: L2={delta_disc_l2:.6f}, Linf={delta_disc_linf:.6f}")

        # FFT analysis
        dt = tau_array[1] - tau_array[0]
        freqs = np.fft.rfftfreq(n_tau, dt)

        fft_loc_vac = np.abs(np.fft.rfft(C_local_vac_real))
        fft_full_vac = np.abs(np.fft.rfft(C_full_vac_real))
        fft_loc_exc = np.abs(np.fft.rfft(C_local_exc_real))
        fft_full_exc = np.abs(np.fft.rfft(C_full_exc_real))
        fft_delta_loc = np.abs(np.fft.rfft(delta_C_local))
        fft_delta_full = np.abs(np.fft.rfft(delta_C_full))

        # Find dominant frequencies
        def top_freqs(fft_data, freqs, n_top=3):
            amps = fft_data.copy()
            amps[0] = 0  # skip DC
            top_idx = np.argsort(amps)[-n_top:][::-1]
            return [(float(freqs[i]), float(amps[i])) for i in top_idx]

        if verbose:
            print(f"\n  FFT dominant frequencies:")
            print(f"    Vac local:  {top_freqs(fft_loc_vac, freqs)}")
            print(f"    Vac full:   {top_freqs(fft_full_vac, freqs)}")
            print(f"    Exc local:  {top_freqs(fft_loc_exc, freqs)}")
            print(f"    Exc full:   {top_freqs(fft_full_exc, freqs)}")
            print(f"    delta local: {top_freqs(fft_delta_loc, freqs)}")
            print(f"    delta full:  {top_freqs(fft_delta_full, freqs)}")

            # Excited mode frequency for reference
            print(f"    omega_m/(2pi) = {omega[mode_idx]/(2*np.pi):.6f}")

        # Store results
        all_results['probes'][probe_name] = {
            'probe_local': int(probe_local),
            'probe_global': int(probe_global),
            'equal_time_vac': float(et_vac),
            'equal_time_exc': float(et_exc),
            'disc_vac_l2': float(disc_vac_l2),
            'disc_exc_l2': float(disc_exc_l2),
            'disc_vac_linf': float(disc_vac_linf),
            'disc_exc_linf': float(disc_exc_linf),
            'delta_disc_l2': float(delta_disc_l2),
            'delta_disc_linf': float(delta_disc_linf),
            'max_delta_C_local': float(np.max(np.abs(delta_C_local))),
            'max_delta_C_full': float(np.max(np.abs(delta_C_full))),
            'C_local_vac': C_local_vac_real.tolist(),
            'C_full_vac': C_full_vac_real.tolist(),
            'C_local_exc': C_local_exc_real.tolist(),
            'C_full_exc': C_full_exc_real.tolist(),
            'delta_C_local': delta_C_local.tolist(),
            'delta_C_full': delta_C_full.tolist(),
            'tau': tau_array.tolist(),
            'fft_freqs': freqs.tolist(),
            'fft_loc_vac': fft_loc_vac.tolist(),
            'fft_full_vac': fft_full_vac.tolist(),
            'fft_loc_exc': fft_loc_exc.tolist(),
            'fft_full_exc': fft_full_exc.tolist(),
            'fft_delta_loc': fft_delta_loc.tolist(),
            'fft_delta_full': fft_delta_full.tolist(),
        }

    return all_results


# ============================================================================
# Additional mode comparison
# ============================================================================

def test_multiple_modes(N, n_modes=5, tau_max=15.0, n_tau=800, verbose=True):
    """Test several modes to see how state-dependence varies with mode choice."""

    start_site = N // 2
    n_R = N - start_site
    boundary_site = start_site

    omega, U, K_mat = build_lattice(N)
    X_full, P_full = vacuum_correlations(omega, U)
    X_R_vac = restrict_to_subsystem(X_full, start_site, n_R)
    P_R_vac = restrict_to_subsystem(P_full, start_site, n_R)
    h_phi_vac, h_pi_vac, _, _, _ = compute_modular_hamiltonian(X_R_vac, P_R_vac)

    tau_array = np.linspace(0, tau_max, n_tau)
    probe_local = n_R // 4
    probe_global = start_site + probe_local

    # Sort modes by boundary amplitude
    boundary_amps = np.abs(U[boundary_site, :])
    sorted_modes = np.argsort(boundary_amps)[::-1][:n_modes]

    results = []

    if verbose:
        print(f"\n{'='*70}")
        print(f"  MULTI-MODE COMPARISON: N = {N}")
        print(f"{'='*70}")
        print(f"  {'Mode':>5} | {'omega_m':>8} | {'|u(bdy)|':>9} | {'p_R':>6} | {'disc_vac_L2':>12} | {'disc_exc_L2':>12} | {'delta_disc':>11}")
        print(f"  {'-'*75}")

    for mode_idx in sorted_modes:
        mode_idx = int(mode_idx)

        # Excited-state correlations
        X1_full, P1_full, _, _ = excited_correlations(omega, U, mode_idx)
        X_R_exc = restrict_to_subsystem(X1_full, start_site, n_R)
        P_R_exc = restrict_to_subsystem(P1_full, start_site, n_R)

        try:
            h_phi_exc, h_pi_exc, _, _, _ = compute_modular_hamiltonian(X_R_exc, P_R_exc)
        except Exception as e:
            if verbose:
                print(f"  {mode_idx:>5} | FAILED: {e}")
            continue

        # Correlators
        C_loc_vac, _ = compute_modular_correlator(h_phi_vac, h_pi_vac, X_R_vac, P_R_vac, probe_local, tau_array)
        C_full_vac, _ = compute_full_correlator_vacuum(omega, U, probe_global, tau_array)
        C_loc_exc, _ = compute_modular_correlator(h_phi_exc, h_pi_exc, X_R_exc, P_R_exc, probe_local, tau_array)
        C_full_exc, _ = compute_full_correlator_excited(omega, U, probe_global, mode_idx, tau_array)

        def l2_rel(a, b):
            d = np.sqrt(np.mean((a-b)**2))
            n = np.sqrt(np.mean(b**2))
            return d/n if n > 1e-15 else float('inf')

        disc_vac = l2_rel(C_loc_vac, C_full_vac)
        disc_exc = l2_rel(C_loc_exc, C_full_exc)

        delta_loc = C_loc_exc - C_loc_vac
        delta_full = C_full_exc - C_full_vac
        delta_disc = l2_rel(delta_loc, delta_full)

        p_R = float(np.sum(U[start_site:, mode_idx]**2))

        results.append({
            'mode_idx': mode_idx,
            'omega_m': float(omega[mode_idx]),
            'boundary_amp': float(boundary_amps[mode_idx]),
            'p_R': p_R,
            'disc_vac_l2': disc_vac,
            'disc_exc_l2': disc_exc,
            'delta_disc_l2': delta_disc,
        })

        if verbose:
            print(f"  {mode_idx:>5} | {omega[mode_idx]:>8.4f} | {boundary_amps[mode_idx]:>9.6f} | {p_R:>6.3f} | {disc_vac:>12.6f} | {disc_exc:>12.6f} | {delta_disc:>11.6f}")

    return results


# ============================================================================
# Run everything
# ============================================================================

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Main test: N=50
    print("Running main test with N=50...")
    results_50 = run_full_test(N=50, tau_max=15.0, n_tau=800)

    # Multi-mode comparison
    print("\n\nRunning multi-mode comparison...")
    multi_mode_50 = test_multiple_modes(N=50, n_modes=8)

    # Convergence: N=20, 30, 50, 100
    convergence = {}
    for N_test in [20, 30, 50, 100]:
        print(f"\n\nConvergence test: N={N_test}")
        r = run_full_test(N=N_test, tau_max=15.0, n_tau=800, verbose=(N_test != 50))
        convergence[str(N_test)] = {
            'N': N_test,
            'probes': {
                k: {kk: vv for kk, vv in v.items()
                    if kk not in ('C_local_vac', 'C_full_vac', 'C_local_exc', 'C_full_exc',
                                  'delta_C_local', 'delta_C_full', 'tau',
                                  'fft_freqs', 'fft_loc_vac', 'fft_full_vac',
                                  'fft_loc_exc', 'fft_full_exc', 'fft_delta_loc', 'fft_delta_full')}
                for k, v in r['probes'].items()
            },
            'mode_info': r['mode_info'],
        }

    # Convergence table
    print(f"\n\n{'='*90}")
    print("CONVERGENCE TABLE")
    print(f"{'='*90}")
    print(f"{'N':>5} | {'Probe':>15} | {'Disc vac L2':>12} | {'Disc exc L2':>12} | {'Delta disc L2':>14} | {'max|dC_loc|':>12} | {'max|dC_full|':>12}")
    print(f"{'-'*90}")
    for N_str in ['20', '30', '50', '100']:
        for probe_name in convergence[N_str]['probes']:
            p = convergence[N_str]['probes'][probe_name]
            print(f"{N_str:>5} | {probe_name:>15} | {p['disc_vac_l2']:>12.6f} | {p['disc_exc_l2']:>12.6f} | {p['delta_disc_l2']:>14.6f} | {p['max_delta_C_local']:>12.6e} | {p['max_delta_C_full']:>12.6e}")

    # Save results
    output = {
        'main_N50': results_50,
        'multi_mode_N50': multi_mode_50,
        'convergence': convergence,
    }

    with open('results.json', 'w') as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to results.json")
