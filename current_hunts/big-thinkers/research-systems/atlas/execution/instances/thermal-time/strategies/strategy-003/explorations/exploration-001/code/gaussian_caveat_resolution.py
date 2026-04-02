#!/usr/bin/env python3
"""
Gaussian Caveat Resolution: Coherent & Squeezed State Modular Flow Tests
=========================================================================

For a free scalar field on a 1D lattice (Dirichlet BC, right half as subsystem),
compute modular flow responses for:
  Part A: Coherent state (same covariance as vacuum, displaced mean)
  Part B: Single-mode squeezed state (modified covariance, Gaussian-exact)
  Part C: Convergence study (fixed physical frequency across N)
  Part D: Squeezing parameter sweep

Key question: Does modular flow produce spectral weight at the physical
mode frequency omega_m, or only at modular frequencies epsilon_k/(2*pi)?
"""

import numpy as np
from scipy.linalg import expm, eigh
import json
import os
import sys
import time

# ============================================================================
# Stage 1: Lattice Setup (identical to prior explorations)
# ============================================================================

def build_lattice(N):
    """
    Free massless scalar on N sites, Dirichlet BC: phi_0 = phi_{N+1} = 0.
    Coupling matrix K is tridiagonal.

    Returns: omega (N,), U (N, N), K (N, N)
      omega[k] = 2*|sin(pi*(k+1)/(2*(N+1)))| for k=0,...,N-1
      U[j,k] = sqrt(2/(N+1)) * sin(pi*(j+1)*(k+1)/(N+1))
    """
    k_modes = np.arange(1, N + 1)
    omega = 2.0 * np.abs(np.sin(np.pi * k_modes / (2 * (N + 1))))

    j_sites = np.arange(N)
    U = np.sqrt(2.0 / (N + 1)) * np.sin(
        np.pi * np.outer(j_sites + 1, k_modes) / (N + 1)
    )

    K = np.zeros((N, N))
    for i in range(N):
        K[i, i] = 2.0
        if i > 0:
            K[i, i - 1] = -1.0
        if i < N - 1:
            K[i, i + 1] = -1.0

    return omega, U, K


# ============================================================================
# Stage 2: Correlation Matrices
# ============================================================================

def vacuum_correlations(omega, U):
    """X_ij = sum_k U[i,k]*U[j,k]/(2*omega[k]), P_ij = sum_k U[i,k]*U[j,k]*omega[k]/2"""
    X = U @ np.diag(1.0 / (2.0 * omega)) @ U.T
    P = U @ np.diag(omega / 2.0) @ U.T
    return X, P


def restrict_to_subsystem(M, start, n):
    """Extract submatrix M[start:start+n, start:start+n]."""
    return M[start:start + n, start:start + n].copy()


def squeezed_correlations(omega, U, mode_idx, r):
    """
    Single-mode squeezed vacuum: S_m(r)|0>.
    X^{(sq)} = X^{(0)} + U[:,m]*U[:,m]^T / (2*omega_m) * (exp(-2r) - 1)
    P^{(sq)} = P^{(0)} + U[:,m]*U[:,m]^T * omega_m / 2 * (exp(2r) - 1)
    """
    X0 = U @ np.diag(1.0 / (2.0 * omega)) @ U.T
    P0 = U @ np.diag(omega / 2.0) @ U.T

    m = mode_idx
    u_m = U[:, m]
    rank1 = np.outer(u_m, u_m)

    X_sq = X0 + rank1 / (2 * omega[m]) * (np.exp(-2 * r) - 1)
    P_sq = P0 + rank1 * omega[m] / 2 * (np.exp(2 * r) - 1)

    return X_sq, P_sq, X0, P0


# ============================================================================
# Stage 3: Modular Hamiltonian (Williamson Decomposition)
# ============================================================================

def matrix_sqrt_sym(A):
    """Matrix square root of symmetric positive (semi-)definite matrix."""
    eigvals, V = eigh(A)
    eigvals = np.maximum(eigvals, 0.0)
    return V @ np.diag(np.sqrt(eigvals)) @ V.T


def compute_modular_hamiltonian(X_R, P_R, epsilon_max=200.0):
    """
    Compute modular Hamiltonian via Williamson decomposition.

    K_R = (1/2) phi^T h_phi phi + (1/2) pi^T h_pi pi

    Returns: h_phi, h_pi, epsilon (modular energies), nu (symplectic eigenvalues),
             recon_err
    """
    n = X_R.shape[0]
    X_half = matrix_sqrt_sym(X_R)
    X_half_inv = np.linalg.inv(X_half)

    D = X_half @ P_R @ X_half
    D = (D + D.T) / 2.0

    nu_sq, V = eigh(D)
    nu = np.sqrt(np.maximum(nu_sq, 0.25))

    sort_idx = np.argsort(nu)
    nu = nu[sort_idx]
    V = V[:, sort_idx]

    ratio = (2 * nu + 1) / np.maximum(2 * nu - 1, 1e-15)
    epsilon = np.log(ratio)
    epsilon = np.minimum(epsilon, epsilon_max)

    S_phi = np.diag(np.sqrt(nu)) @ V.T @ X_half_inv
    S_pi = np.diag(1.0 / np.sqrt(nu)) @ V.T @ X_half

    h_phi = S_phi.T @ np.diag(epsilon) @ S_phi
    h_pi = S_pi.T @ np.diag(epsilon) @ S_pi

    h_phi = (h_phi + h_phi.T) / 2
    h_pi = (h_pi + h_pi.T) / 2

    # Reconstruction check
    X_R_recon = np.linalg.inv(S_phi) @ np.diag(nu) @ np.linalg.inv(S_phi.T)
    recon_err = np.linalg.norm(X_R - X_R_recon) / np.linalg.norm(X_R)

    return h_phi, h_pi, epsilon, nu, recon_err


# ============================================================================
# Stage 4: Correlator Computation
# ============================================================================

def compute_modular_correlator(h_phi, h_pi, X_R, P_R, probe, tau_array):
    """
    C_local(tau) = [exp(A*tau) * Sigma]_{k,k}

    where A = [[0, h_pi/(2pi)], [-h_phi/(2pi), 0]]
    and Sigma = [[X_R, 0], [0, P_R]] (symmetrized/real correlator).
    """
    n = X_R.shape[0]
    k = probe

    A = np.zeros((2 * n, 2 * n))
    A[:n, n:] = h_pi / (2 * np.pi)
    A[n:, :n] = -h_phi / (2 * np.pi)

    Sigma = np.zeros((2 * n, 2 * n))
    Sigma[:n, :n] = X_R
    Sigma[n:, n:] = P_R

    C = np.zeros(len(tau_array))
    for i, tau in enumerate(tau_array):
        eAt = expm(A * tau)
        C[i] = (eAt @ Sigma)[k, k]
    return C


def compute_modular_correlator_fast(h_phi, h_pi, X_R, P_R, probe, tau_array):
    """
    Faster correlator computation using eigendecomposition of A.
    C_local(tau) = [exp(A*tau) * Sigma]_{k,k}
    """
    n = X_R.shape[0]
    k = probe

    A = np.zeros((2 * n, 2 * n))
    A[:n, n:] = h_pi / (2 * np.pi)
    A[n:, :n] = -h_phi / (2 * np.pi)

    Sigma = np.zeros((2 * n, 2 * n))
    Sigma[:n, :n] = X_R
    Sigma[n:, n:] = P_R

    # Eigendecompose A
    eigenvalues, V = np.linalg.eig(A)
    V_inv = np.linalg.inv(V)

    # Precompute V_inv @ Sigma
    VS = V_inv @ Sigma

    C = np.zeros(len(tau_array))
    for i, tau in enumerate(tau_array):
        exp_eig = np.exp(eigenvalues * tau)
        # exp(A*tau) = V @ diag(exp_eig) @ V_inv
        # [exp(A*tau) @ Sigma]_{k,:} = V[k,:] * exp_eig @ V_inv @ Sigma
        row = (V[k, :] * exp_eig) @ VS
        C[i] = np.real(row[k])
    return C


def compute_full_correlator_vacuum(omega, U, probe_global, tau_array):
    """
    C_full^{(0)}(tau) = sum_m U[k,m]^2 * cos(omega_m * tau) / (2*omega_m)
    (Symmetrized/real Wightman function)
    """
    k = probe_global
    weights = U[k, :] ** 2 / (2.0 * omega)
    C = np.array([np.sum(weights * np.cos(omega * t)) for t in tau_array])
    return C


def compute_full_correlator_squeezed(omega, U, probe_global, mode_idx, r, tau_array):
    """
    C_full^{(sq)}(tau) for squeezed vacuum S_m(r)|0>.

    C^{(sq)} = C^{(0)} + U[k,m]^2/(2*omega_m) * (exp(-2r) - 1) * cos(omega_m * tau)
    """
    C0 = compute_full_correlator_vacuum(omega, U, probe_global, tau_array)
    m = mode_idx
    k = probe_global
    correction = U[k, m] ** 2 / (2 * omega[m]) * (np.exp(-2 * r) - 1) * np.cos(omega[m] * tau_array)
    return C0 + correction


def compute_full_correlator_coherent(omega, U, probe_global, mode_idx, alpha, tau_array):
    """
    C_full^{(alpha)}(tau) for coherent state D_m(alpha)|0>.

    C^{(alpha)} = C^{(0)} + mu_k^2 * cos(omega_m * tau)
    where mu_k = alpha * sqrt(2/omega_m) * U[k,m]
    """
    C0 = compute_full_correlator_vacuum(omega, U, probe_global, tau_array)
    m = mode_idx
    k = probe_global
    mu_k = alpha * np.sqrt(2.0 / omega[m]) * U[k, m]
    correction = mu_k ** 2 * np.cos(omega[m] * tau_array)
    return C0 + correction


# ============================================================================
# Stage 5: FFT Analysis
# ============================================================================

def fft_analysis(signal, tau_array, zero_pad_factor=8, threshold_frac=0.02, n_peaks=8):
    """
    Compute FFT and find peaks.
    Returns: freqs (angular), amplitudes, peaks [(freq, amp), ...]
    """
    dt = tau_array[1] - tau_array[0]
    n = len(signal)
    n_pad = n * zero_pad_factor

    signal_centered = signal - signal.mean()
    fft_vals = np.abs(np.fft.rfft(signal_centered, n=n_pad))
    freq_axis = np.fft.rfftfreq(n_pad, d=dt) * 2 * np.pi

    # Find peaks
    threshold = threshold_frac * fft_vals.max() if fft_vals.max() > 0 else 1e-15
    peaks = []
    for i in range(1, len(fft_vals) - 1):
        if (fft_vals[i] > threshold and
            fft_vals[i] > fft_vals[i - 1] and
            fft_vals[i] > fft_vals[i + 1]):
            peaks.append((freq_axis[i], fft_vals[i]))
    peaks.sort(key=lambda x: -x[1])

    return freq_axis, fft_vals, peaks[:n_peaks]


# ============================================================================
# Part A: Coherent State Test
# ============================================================================

def run_coherent_test(N, alpha=1.0, mode_frac=0.25, tau_max=20.0, n_tau=1000):
    """Run Part A: coherent state test at given N."""
    start_site = N // 2
    n_R = N - start_site
    mode_idx = N // 4  # mode m = N//4

    print(f"\n{'='*70}")
    print(f"  PART A: COHERENT STATE TEST — N = {N}")
    print(f"  alpha = {alpha}, mode = {mode_idx}")
    print(f"{'='*70}")

    # Build lattice
    omega, U, K_mat = build_lattice(N)
    print(f"  omega_m = {omega[mode_idx]:.6f}")

    # Vacuum correlations
    X_full, P_full = vacuum_correlations(omega, U)
    X_R_vac = restrict_to_subsystem(X_full, start_site, n_R)
    P_R_vac = restrict_to_subsystem(P_full, start_site, n_R)

    # Coherent state: SAME covariance as vacuum
    X_R_coh = X_R_vac.copy()
    P_R_coh = P_R_vac.copy()

    # Verify they're identical
    diff_X = np.linalg.norm(X_R_coh - X_R_vac)
    diff_P = np.linalg.norm(P_R_coh - P_R_vac)
    print(f"  ||X_R^(coh) - X_R^(vac)|| = {diff_X:.2e} (should be 0)")
    print(f"  ||P_R^(coh) - P_R^(vac)|| = {diff_P:.2e} (should be 0)")

    # Modular Hamiltonian (same as vacuum)
    h_phi, h_pi, eps, nu, recon_err = compute_modular_hamiltonian(X_R_vac, P_R_vac)
    print(f"  Modular H recon error: {recon_err:.2e}")
    print(f"  Modular energies: eps in [{eps.min():.4f}, {eps.max():.4f}]")
    print(f"  Modular frequencies eps/(2pi): [{eps.min()/(2*np.pi):.6f}, {eps.max()/(2*np.pi):.6f}]")

    # Mean displacement on right sublattice
    probe_local = n_R // 4
    probe_global = start_site + probe_local
    mu_k = alpha * np.sqrt(2.0 / omega[mode_idx]) * U[probe_global, mode_idx]
    print(f"  Probe: local={probe_local}, global={probe_global}")
    print(f"  mu_k = {mu_k:.8f}")
    print(f"  mu_k^2 = {mu_k**2:.8e}")

    # Compute correlators
    tau_array = np.linspace(0, tau_max, n_tau)

    # C_local^{(0)} and C_local^{(alpha)} (connected part only)
    print("  Computing C_local (vacuum modular flow)...", end=" ", flush=True)
    t0 = time.time()
    C_local_vac = compute_modular_correlator_fast(h_phi, h_pi, X_R_vac, P_R_vac, probe_local, tau_array)
    print(f"done ({time.time()-t0:.1f}s)")

    # Since X_R, P_R are identical, C_local connected part is also identical
    C_local_coh_connected = C_local_vac.copy()

    # Full C_local^{(alpha)} includes disconnected part: + mu_k^2 (constant by KMS)
    C_local_coh = C_local_coh_connected + mu_k ** 2
    delta_C_local = C_local_coh - C_local_vac  # = mu_k^2 (constant)

    # C_full^{(0)} and C_full^{(alpha)}
    C_full_vac = compute_full_correlator_vacuum(omega, U, probe_global, tau_array)
    C_full_coh = compute_full_correlator_coherent(omega, U, probe_global, mode_idx, alpha, tau_array)
    delta_C_full = C_full_coh - C_full_vac  # = mu_k^2 * cos(omega_m * tau)

    # Verify analytical predictions
    delta_C_local_expected = mu_k ** 2 * np.ones_like(tau_array)
    delta_C_full_expected = mu_k ** 2 * np.cos(omega[mode_idx] * tau_array)

    err_local = np.max(np.abs(delta_C_local - delta_C_local_expected))
    err_full = np.max(np.abs(delta_C_full - delta_C_full_expected))

    print(f"\n  VERIFICATION:")
    print(f"    max|delta_C_local - mu_k^2| = {err_local:.2e} (should be ~0)")
    print(f"    max|delta_C_full - mu_k^2*cos(w_m*t)| = {err_full:.2e} (should be ~0)")

    # FFT of delta_C_local: should be DC only
    freq_loc, fft_loc, peaks_loc = fft_analysis(delta_C_local, tau_array)
    # FFT of delta_C_full: should peak at omega_m
    freq_full, fft_full, peaks_full = fft_analysis(delta_C_full, tau_array)

    print(f"\n  FFT of delta_C_local peaks (should be DC only):")
    for f, a in peaks_loc[:3]:
        marker = " <-- omega_m" if abs(f - omega[mode_idx]) < 0.05 else ""
        print(f"    freq = {f:.4f}, amp = {a:.6e}{marker}")
    if not peaks_loc:
        print(f"    No peaks (constant signal)")

    print(f"  FFT of delta_C_full peaks (should be omega_m):")
    for f, a in peaks_full[:3]:
        marker = " <-- omega_m" if abs(f - omega[mode_idx]) < 0.05 else ""
        print(f"    freq = {f:.4f}, amp = {a:.6e}{marker}")

    # Vacuum control: C_local(0) vs C_full(0)
    vac_ctrl = abs(C_local_vac[0] - C_full_vac[0])
    print(f"\n  Vacuum control: |C_local(0) - C_full(0)| = {vac_ctrl:.2e}")

    return {
        'N': N, 'alpha': alpha, 'mode_idx': mode_idx,
        'omega_m': float(omega[mode_idx]),
        'mu_k': float(mu_k), 'mu_k_sq': float(mu_k ** 2),
        'recon_err': float(recon_err),
        'err_local': float(err_local),
        'err_full': float(err_full),
        'vac_ctrl': float(vac_ctrl),
        'delta_C_local_std': float(np.std(delta_C_local)),
        'delta_C_full_amplitude': float(mu_k ** 2),
        'peaks_local': [(float(f), float(a)) for f, a in peaks_loc[:5]],
        'peaks_full': [(float(f), float(a)) for f, a in peaks_full[:5]],
    }


# ============================================================================
# Part B: Squeezed State Test
# ============================================================================

def run_squeezed_test(N, r=0.5, mode_idx=None, tau_max=20.0, n_tau=1000, verbose=True):
    """Run Part B: squeezed state test at given N."""
    start_site = N // 2
    n_R = N - start_site
    if mode_idx is None:
        mode_idx = N // 4

    if verbose:
        print(f"\n{'='*70}")
        print(f"  PART B: SQUEEZED STATE TEST — N = {N}")
        print(f"  r = {r}, mode = {mode_idx}")
        print(f"{'='*70}")

    omega, U, K_mat = build_lattice(N)
    omega_m = omega[mode_idx]
    if verbose:
        print(f"  omega_m = {omega_m:.6f}")

    # Vacuum correlations
    X_full_vac, P_full_vac = vacuum_correlations(omega, U)
    X_R_vac = restrict_to_subsystem(X_full_vac, start_site, n_R)
    P_R_vac = restrict_to_subsystem(P_full_vac, start_site, n_R)

    # Squeezed state correlations
    X_full_sq, P_full_sq, _, _ = squeezed_correlations(omega, U, mode_idx, r)
    X_R_sq = restrict_to_subsystem(X_full_sq, start_site, n_R)
    P_R_sq = restrict_to_subsystem(P_full_sq, start_site, n_R)

    # Verify the rank-1 correction
    u_m_R = U[start_site:start_site + n_R, mode_idx]
    dX_expected = np.outer(u_m_R, u_m_R) / (2 * omega_m) * (np.exp(-2 * r) - 1)
    dP_expected = np.outer(u_m_R, u_m_R) * omega_m / 2 * (np.exp(2 * r) - 1)
    err_dX = np.linalg.norm((X_R_sq - X_R_vac) - dX_expected) / np.linalg.norm(dX_expected)
    err_dP = np.linalg.norm((P_R_sq - P_R_vac) - dP_expected) / np.linalg.norm(dP_expected)
    if verbose:
        print(f"  Rank-1 correction error: dX={err_dX:.2e}, dP={err_dP:.2e}")

    # Uncertainty relation check
    XP_vac_eigs = np.sort(np.real(np.linalg.eigvals(X_R_vac @ P_R_vac)))
    XP_sq_eigs = np.sort(np.real(np.linalg.eigvals(X_R_sq @ P_R_sq)))
    if verbose:
        print(f"  XP eigenvalues (vac): [{XP_vac_eigs.min():.6f}, {XP_vac_eigs.max():.6f}]")
        print(f"  XP eigenvalues (sq):  [{XP_sq_eigs.min():.6f}, {XP_sq_eigs.max():.6f}]")

    # Modular Hamiltonians
    h_phi_vac, h_pi_vac, eps_vac, nu_vac, recon_vac = compute_modular_hamiltonian(X_R_vac, P_R_vac)
    h_phi_sq, h_pi_sq, eps_sq, nu_sq, recon_sq = compute_modular_hamiltonian(X_R_sq, P_R_sq)

    if verbose:
        print(f"\n  Vacuum modular H: recon={recon_vac:.2e}")
        print(f"    eps in [{eps_vac.min():.4f}, {eps_vac.max():.4f}]")
        print(f"    eps/(2pi) in [{eps_vac.min()/(2*np.pi):.6f}, {eps_vac.max()/(2*np.pi):.6f}]")
        print(f"  Squeezed modular H: recon={recon_sq:.2e}")
        print(f"    eps in [{eps_sq.min():.4f}, {eps_sq.max():.4f}]")
        print(f"    eps/(2pi) in [{eps_sq.min()/(2*np.pi):.6f}, {eps_sq.max()/(2*np.pi):.6f}]")

        # How much did modular energies shift?
        eps_shift = eps_sq - eps_vac
        print(f"    max|delta_eps| = {np.max(np.abs(eps_shift)):.6f}")
        print(f"    L2 delta_eps / L2 eps_vac = {np.linalg.norm(eps_shift)/np.linalg.norm(eps_vac):.6f}")

    # Compute correlators
    tau_array = np.linspace(0, tau_max, n_tau)
    probe_local = n_R // 4
    probe_global = start_site + probe_local

    if verbose:
        print(f"\n  Probe: local={probe_local}, global={probe_global}")
        print(f"  U[probe, mode]^2 / (2*omega_m) = {U[probe_global, mode_idx]**2 / (2*omega_m):.8e}")

    # C_local vacuum
    print("  Computing C_local (vacuum)...", end=" ", flush=True)
    t0 = time.time()
    C_local_vac = compute_modular_correlator_fast(h_phi_vac, h_pi_vac, X_R_vac, P_R_vac, probe_local, tau_array)
    print(f"done ({time.time()-t0:.1f}s)")

    # C_local squeezed (uses different h_phi, h_pi AND different X_R, P_R)
    print("  Computing C_local (squeezed)...", end=" ", flush=True)
    t0 = time.time()
    C_local_sq = compute_modular_correlator_fast(h_phi_sq, h_pi_sq, X_R_sq, P_R_sq, probe_local, tau_array)
    print(f"done ({time.time()-t0:.1f}s)")

    # C_full vacuum and squeezed
    C_full_vac = compute_full_correlator_vacuum(omega, U, probe_global, tau_array)
    C_full_sq = compute_full_correlator_squeezed(omega, U, probe_global, mode_idx, r, tau_array)

    # Difference signals
    delta_C_local = C_local_sq - C_local_vac
    delta_C_full = C_full_sq - C_full_vac

    # Expected delta_C_full
    expected_amp = U[probe_global, mode_idx] ** 2 / (2 * omega_m) * (np.exp(-2 * r) - 1)
    delta_C_full_expected = expected_amp * np.cos(omega_m * tau_array)
    err_full = np.max(np.abs(delta_C_full - delta_C_full_expected))

    if verbose:
        print(f"\n  RESULTS:")
        print(f"    max|delta_C_full - expected| = {err_full:.2e}")
        print(f"    max|delta_C_local| = {np.max(np.abs(delta_C_local)):.6e}")
        print(f"    max|delta_C_full|  = {np.max(np.abs(delta_C_full)):.6e}")

    # Relative discrepancy
    norm_full = np.sqrt(np.mean(delta_C_full ** 2))
    disc = np.sqrt(np.mean((delta_C_local - delta_C_full) ** 2)) / norm_full if norm_full > 1e-15 else float('inf')

    if verbose:
        print(f"    ||delta_C_local - delta_C_full|| / ||delta_C_full|| = {disc:.6f}")

    # FFT analysis
    freq_loc, fft_loc, peaks_loc = fft_analysis(delta_C_local, tau_array)
    freq_full, fft_full, peaks_full = fft_analysis(delta_C_full, tau_array)

    if verbose:
        print(f"\n  FFT of delta_C_local peaks:")
        for f, a in peaks_loc[:6]:
            markers = []
            if abs(f - omega_m) < 0.05:
                markers.append("omega_m")
            # Check against modular frequencies
            for j, e in enumerate(eps_sq[:min(10, len(eps_sq))]):
                if abs(f - e / (2 * np.pi)) < 0.05:
                    markers.append(f"eps_{j}/(2pi)")
            marker = f" <-- {', '.join(markers)}" if markers else ""
            print(f"    freq = {f:.6f}, amp = {a:.6e}{marker}")

        print(f"  FFT of delta_C_full peaks:")
        for f, a in peaks_full[:3]:
            marker = " <-- omega_m" if abs(f - omega_m) < 0.05 else ""
            print(f"    freq = {f:.6f}, amp = {a:.6e}{marker}")

    # Spectral weight at omega_m
    # Find the FFT amplitude near omega_m in delta_C_local
    idx_om = np.argmin(np.abs(freq_loc - omega_m))
    weight_at_om_local = fft_loc[max(0, idx_om - 3):idx_om + 4].max()
    weight_at_om_full = fft_full[max(0, idx_om - 3):idx_om + 4].max()

    ratio_weight = weight_at_om_local / weight_at_om_full if weight_at_om_full > 1e-15 else 0.0

    if verbose:
        print(f"\n  SPECTRAL WEIGHT AT omega_m = {omega_m:.6f}:")
        print(f"    delta_C_local FFT near omega_m: {weight_at_om_local:.6e}")
        print(f"    delta_C_full  FFT near omega_m: {weight_at_om_full:.6e}")
        print(f"    ratio: {ratio_weight:.6f}")

    # Vacuum control
    vac_ctrl = abs(C_local_vac[0] - C_full_vac[0])
    if verbose:
        print(f"\n  Vacuum control: |C_local(0) - C_full(0)| = {vac_ctrl:.2e}")

    return {
        'N': N, 'r': r, 'mode_idx': int(mode_idx),
        'omega_m': float(omega_m),
        'n_R': n_R,
        'recon_vac': float(recon_vac),
        'recon_sq': float(recon_sq),
        'eps_vac_range': [float(eps_vac.min()), float(eps_vac.max())],
        'eps_sq_range': [float(eps_sq.min()), float(eps_sq.max())],
        'eps_shift_max': float(np.max(np.abs(eps_sq - eps_vac))),
        'discrepancy': float(disc),
        'max_delta_C_local': float(np.max(np.abs(delta_C_local))),
        'max_delta_C_full': float(np.max(np.abs(delta_C_full))),
        'spectral_weight_ratio': float(ratio_weight),
        'weight_at_om_local': float(weight_at_om_local),
        'weight_at_om_full': float(weight_at_om_full),
        'peaks_local': [(float(f), float(a)) for f, a in peaks_loc[:8]],
        'peaks_full': [(float(f), float(a)) for f, a in peaks_full[:5]],
        'vac_ctrl': float(vac_ctrl),
        'delta_C_local': delta_C_local.tolist(),
        'delta_C_full': delta_C_full.tolist(),
        'tau_array': tau_array.tolist(),
        'eps_vac': eps_vac.tolist(),
        'eps_sq': eps_sq.tolist(),
        'nu_vac': nu_vac.tolist(),
        'nu_sq': nu_sq.tolist(),
    }


# ============================================================================
# Part C: Convergence Study (Fixed Physical Frequency)
# ============================================================================

def run_convergence_study(N_values, target_omega=0.3, r=0.5, tau_max=20.0, n_tau=1000):
    """
    Part C: Fixed physical frequency across lattice sizes.
    Choose mode m(N) such that omega_m ≈ target_omega.
    """
    print(f"\n{'='*70}")
    print(f"  PART C: CONVERGENCE STUDY")
    print(f"  target omega = {target_omega}, r = {r}")
    print(f"  N values: {N_values}")
    print(f"{'='*70}")

    results = {}
    for N in N_values:
        omega, U, K_mat = build_lattice(N)

        # Find mode closest to target frequency
        mode_idx = np.argmin(np.abs(omega - target_omega))
        actual_omega = omega[mode_idx]
        print(f"\n  N={N}: mode_idx={mode_idx}, omega={actual_omega:.6f} (target={target_omega})")

        r_result = run_squeezed_test(N, r=r, mode_idx=mode_idx, tau_max=tau_max, n_tau=n_tau, verbose=False)

        results[str(N)] = {
            'N': N,
            'mode_idx': int(mode_idx),
            'omega_m': float(actual_omega),
            'discrepancy': r_result['discrepancy'],
            'spectral_weight_ratio': r_result['spectral_weight_ratio'],
            'recon_sq': r_result['recon_sq'],
            'eps_shift_max': r_result['eps_shift_max'],
            'max_delta_C_local': r_result['max_delta_C_local'],
            'max_delta_C_full': r_result['max_delta_C_full'],
        }

        print(f"    discrepancy = {r_result['discrepancy']:.6f}")
        print(f"    spectral_weight_ratio = {r_result['spectral_weight_ratio']:.6f}")

    # Power law fit if 3+ points
    if len(N_values) >= 3:
        N_arr = np.array(N_values, dtype=float)
        disc_arr = np.array([results[str(N)]['discrepancy'] for N in N_values])
        if np.all(disc_arr > 0):
            log_N = np.log(N_arr)
            log_d = np.log(disc_arr)
            slope, intercept = np.polyfit(log_N, log_d, 1)
            print(f"\n  Power law fit: discrepancy ~ N^{slope:.3f}")
            results['power_law_exponent'] = float(slope)
        else:
            print(f"\n  Cannot fit power law (some discrepancies are zero)")
            results['power_law_exponent'] = None

    return results


# ============================================================================
# Part D: Squeezing Parameter Sweep
# ============================================================================

def run_squeeze_sweep(N=100, r_values=None, tau_max=20.0, n_tau=1000):
    """Part D: Vary squeezing parameter at fixed N."""
    if r_values is None:
        r_values = [0.1, 0.3, 0.5, 0.7, 1.0]

    mode_idx = N // 4

    print(f"\n{'='*70}")
    print(f"  PART D: SQUEEZING PARAMETER SWEEP")
    print(f"  N = {N}, mode = {mode_idx}")
    print(f"  r values: {r_values}")
    print(f"{'='*70}")

    results = {}
    for r in r_values:
        r_result = run_squeezed_test(N, r=r, mode_idx=mode_idx, tau_max=tau_max, n_tau=n_tau, verbose=False)
        results[f"r={r}"] = {
            'r': r,
            'discrepancy': r_result['discrepancy'],
            'spectral_weight_ratio': r_result['spectral_weight_ratio'],
            'max_delta_C_local': r_result['max_delta_C_local'],
            'max_delta_C_full': r_result['max_delta_C_full'],
            'eps_shift_max': r_result['eps_shift_max'],
        }
        print(f"  r={r:.2f}: disc={r_result['discrepancy']:.6f}, "
              f"weight_ratio={r_result['spectral_weight_ratio']:.6f}, "
              f"max|dC_local|={r_result['max_delta_C_local']:.6e}, "
              f"max|dC_full|={r_result['max_delta_C_full']:.6e}")

    return results


# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    all_results = {}

    # ---- Part A: Coherent State ----
    part_a = {}
    for N in [50, 100, 200]:
        part_a[str(N)] = run_coherent_test(N, alpha=1.0, mode_frac=0.25, tau_max=20.0, n_tau=1000)
    all_results['part_a'] = part_a

    # ---- Part B: Squeezed State ----
    part_b = {}
    for N in [50, 100, 200]:
        part_b[str(N)] = run_squeezed_test(N, r=0.5, mode_idx=None, tau_max=20.0, n_tau=1000)
    all_results['part_b'] = part_b

    # ---- Part C: Convergence ----
    part_c = run_convergence_study([50, 100, 200], target_omega=0.3, r=0.5, tau_max=20.0, n_tau=1000)
    all_results['part_c'] = part_c

    # ---- Part D: Squeeze Sweep ----
    part_d = run_squeeze_sweep(N=100, r_values=[0.1, 0.3, 0.5, 0.7, 1.0], tau_max=20.0, n_tau=1000)
    all_results['part_d'] = part_d

    # ---- Summary ----
    print(f"\n\n{'='*70}")
    print("FINAL SUMMARY")
    print(f"{'='*70}")

    print("\nPart A: Coherent State")
    print(f"  {'N':>5} | {'mu_k^2':>12} | {'dC_local std':>12} | {'err_local':>10} | {'err_full':>10}")
    print(f"  {'-'*60}")
    for N_str in ['50', '100', '200']:
        r = part_a[N_str]
        print(f"  {r['N']:>5} | {r['mu_k_sq']:>12.6e} | {r['delta_C_local_std']:>12.6e} | {r['err_local']:>10.2e} | {r['err_full']:>10.2e}")

    print("\nPart B: Squeezed State")
    print(f"  {'N':>5} | {'disc':>12} | {'weight_ratio':>14} | {'max|dCl|':>12} | {'max|dCf|':>12} | {'recon':>10}")
    print(f"  {'-'*75}")
    for N_str in ['50', '100', '200']:
        r = part_b[N_str]
        print(f"  {r['N']:>5} | {r['discrepancy']:>12.6f} | {r['spectral_weight_ratio']:>14.6f} | "
              f"{r['max_delta_C_local']:>12.6e} | {r['max_delta_C_full']:>12.6e} | {r['recon_sq']:>10.2e}")

    print("\nPart C: Convergence (fixed omega ≈ 0.3)")
    print(f"  {'N':>5} | {'omega_m':>8} | {'disc':>12} | {'weight_ratio':>14}")
    print(f"  {'-'*50}")
    for N_str in [str(N) for N in [50, 100, 200]]:
        r = part_c[N_str]
        print(f"  {r['N']:>5} | {r['omega_m']:>8.4f} | {r['discrepancy']:>12.6f} | {r['spectral_weight_ratio']:>14.6f}")
    if 'power_law_exponent' in part_c and part_c['power_law_exponent'] is not None:
        print(f"  Power law: disc ~ N^{part_c['power_law_exponent']:.3f}")

    print("\nPart D: Squeeze Sweep (N=100)")
    print(f"  {'r':>5} | {'disc':>12} | {'weight_ratio':>14} | {'max|dCl|':>12}")
    print(f"  {'-'*50}")
    for key in sorted(part_d.keys()):
        r = part_d[key]
        print(f"  {r['r']:>5.2f} | {r['discrepancy']:>12.6f} | {r['spectral_weight_ratio']:>14.6f} | {r['max_delta_C_local']:>12.6e}")

    # Save results
    # Strip large arrays for summary save
    save_results = {
        'part_a': part_a,
        'part_b': {k: {kk: vv for kk, vv in v.items()
                       if kk not in ('delta_C_local', 'delta_C_full', 'tau_array',
                                     'eps_vac', 'eps_sq', 'nu_vac', 'nu_sq')}
                   for k, v in part_b.items()},
        'part_c': part_c,
        'part_d': part_d,
    }
    with open('results_summary.json', 'w') as f:
        json.dump(save_results, f, indent=2)

    # Save full Part B data separately
    for N_str in ['50', '100', '200']:
        fname = f'part_b_N{N_str}_data.json'
        with open(fname, 'w') as f:
            json.dump({
                'delta_C_local': part_b[N_str]['delta_C_local'],
                'delta_C_full': part_b[N_str]['delta_C_full'],
                'tau_array': part_b[N_str]['tau_array'],
                'eps_vac': part_b[N_str]['eps_vac'],
                'eps_sq': part_b[N_str]['eps_sq'],
            }, f)

    print(f"\nResults saved to code/results_summary.json")
    print("DONE")
