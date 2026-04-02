#!/usr/bin/env python3
"""
Rindler Wedge Verification of the Thermal Time Hypothesis.

Verification strategy:
1. BW PROFILE: Check modular Hamiltonian matches 2π × boost generator near entangling surface
2. KMS: Verify occupation numbers satisfy Bose-Einstein at β=1 (modular) = 2π (physical)
3. BOOST CORRELATOR: Compare modular-flow correlator to Wightman function at boosted spacetime
   points (the CORRECT BW comparison), NOT to full-H time-evolution correlator
4. FULL-H COMPARISON: Show C_local ≠ C_full and explain WHY (boost ≠ time translation)
5. ENTANGLEMENT ENTROPY: Verify against Calabrese-Cardy (c/3)log(N)
6. CONVERGENCE: All checks at N = 50, 100, 200

Key physics: The BW theorem says the modular flow of the vacuum restricted to the right
half-space IS the Lorentz boost. The boost is NOT time translation. So the modular flow
correlator should match the BOOST correlator, not the time-evolution correlator.
"""

import numpy as np
from scipy.linalg import expm, eigh
import json, os, sys


# ============================================================================
# Stage 1: Lattice scalar field (Dirichlet BC)
# ============================================================================

def build_lattice(N):
    """
    Free massless scalar on N sites with Dirichlet BC.
    Sites: 1-indexed positions x = 1,...,N. Boundary: φ(0) = φ(N+1) = 0.

    Coupling matrix K (tridiagonal, positive definite — no zero mode).
    Eigenvalues: ω_k² = 4 sin²(πk/(2(N+1))), k = 1,...,N
    Eigenvectors: U_{j,k} = √(2/(N+1)) sin(πjk/(N+1)), j,k = 1,...,N
    """
    k_modes = np.arange(1, N+1)
    omega = 2.0 * np.abs(np.sin(np.pi * k_modes / (2*(N+1))))

    j_sites = np.arange(1, N+1)
    U = np.sqrt(2.0/(N+1)) * np.sin(np.pi * np.outer(j_sites, k_modes) / (N+1))

    # Coupling matrix (for reference in BW check)
    K = np.zeros((N, N))
    for i in range(N):
        K[i, i] = 2.0
        if i > 0: K[i, i-1] = -1.0
        if i < N-1: K[i, i+1] = -1.0

    return omega, U, K


# ============================================================================
# Stage 2: Vacuum correlation matrices
# ============================================================================

def compute_vacuum_correlators(omega, U):
    """X_ij = <φ_i φ_j> = Σ_k U_{ik} U_{jk}/(2ω_k), P_ij = <π_i π_j> = Σ_k U_{ik} U_{jk} ω_k/2"""
    X = U @ np.diag(1.0/(2.0*omega)) @ U.T
    P = U @ np.diag(omega/2.0) @ U.T
    return X, P


def restrict_to_right_half(M, N):
    """Restrict matrix M to the right half: sites N//2 ... N-1 (0-indexed)."""
    s = N // 2
    return M[s:, s:]


# ============================================================================
# Stage 3: Modular Hamiltonian (Williamson decomposition)
# ============================================================================

def mat_sqrt(A):
    """Matrix sqrt of symmetric positive semidefinite A."""
    eigvals, V = eigh(A)
    return V @ np.diag(np.sqrt(np.maximum(eigvals, 0))) @ V.T


def compute_modular_hamiltonian(X_R, P_R, eps_max=200.0):
    """
    Williamson decomposition → modular Hamiltonian.

    Returns: h_phi, h_pi (position blocks of modular H), epsilon (modular energies),
             nu (symplectic eigenvalues), recon_err, S_phi, S_pi (Williamson matrices)
    """
    n = X_R.shape[0]
    Xh = mat_sqrt(X_R)
    Xhi = np.linalg.inv(Xh)

    D = Xh @ P_R @ Xh
    D = (D + D.T) / 2.0  # symmetrize

    nu_sq, V = eigh(D)
    nu = np.sqrt(np.maximum(nu_sq, 0.25))
    idx = np.argsort(nu)
    nu, V = nu[idx], V[:, idx]

    eps = np.minimum(np.log((2*nu+1)/np.maximum(2*nu-1, 1e-15)), eps_max)

    S_phi = np.diag(np.sqrt(nu)) @ V.T @ Xhi
    S_pi  = np.diag(1.0/np.sqrt(nu)) @ V.T @ Xh

    h_phi = S_phi.T @ np.diag(eps) @ S_phi
    h_pi  = S_pi.T  @ np.diag(eps) @ S_pi

    # Verify reconstruction
    X_recon = np.linalg.inv(S_phi) @ np.diag(nu) @ np.linalg.inv(S_phi.T)
    recon_err = np.linalg.norm(X_R - X_recon) / np.linalg.norm(X_R)

    return h_phi, h_pi, eps, nu, recon_err


# ============================================================================
# Stage 4: Correlator computations
# ============================================================================

def modular_flow_correlator(h_phi, h_pi, X_R, P_R, tau_arr, probe):
    """
    C_local(τ) = <φ_k(τ) φ_k(0)> under modular flow with generator K/(2π).

    Evolution: dφ/dτ = h_π/(2π) · π,  dπ/dτ = -h_φ/(2π) · φ
    """
    n = h_phi.shape[0]
    k = probe

    A = np.zeros((2*n, 2*n))
    A[:n, n:] = h_pi / (2*np.pi)
    A[n:, :n] = -h_phi / (2*np.pi)

    Sigma = np.zeros((2*n, 2*n))
    Sigma[:n, :n] = X_R
    Sigma[n:, n:] = P_R

    C = np.zeros(len(tau_arr))
    for i, tau in enumerate(tau_arr):
        C[i] = np.real((expm(A * tau) @ Sigma)[k, k])
    return C


def full_H_correlator(omega, U, tau_arr, probe_global_0idx):
    """C_full(τ) = <0|φ_k(τ) φ_k(0)|0> = Σ_m |U_{k,m}|² cos(ω_m τ)/(2ω_m)"""
    k = probe_global_0idx  # 0-indexed in U (which is 1-indexed internally but stored 0-based)
    weights = U[k, :]**2 / (2.0 * omega)
    return np.array([np.sum(weights * np.cos(omega * t)) for t in tau_arr])


def boost_correlator(omega, U, N, tau_arr, probe_sublattice_idx):
    """
    Compute the Wightman function at the BOOSTED spacetime point.

    BW says: modular flow ≡ Lorentz boost. So C_local(τ) should equal
    the vacuum Wightman function evaluated at the boosted spacetime point:

    W(x_boost, t_boost; x_probe, 0)

    where x_boost = x_cut + d·cosh(τ), t_boost = d·sinh(τ), d = probe distance from cut.

    The mode functions f_m(x) = √(2/(N+1)) sin(πmx/(N+1)) are defined for continuous x.
    """
    n_sub = N - N//2
    # Distance from cut (in lattice units)
    d_probe = probe_sublattice_idx + 0.5
    # 1-indexed position on full lattice
    x_cut = N//2 + 0.5  # position of the entangling cut
    x_probe = x_cut + d_probe

    k_modes = np.arange(1, N+1)
    f_probe = np.sqrt(2.0/(N+1)) * np.sin(np.pi * k_modes * x_probe / (N+1))

    C = np.zeros(len(tau_arr))
    for i, tau in enumerate(tau_arr):
        x_boost = x_cut + d_probe * np.cosh(tau)
        t_boost = d_probe * np.sinh(tau)

        # Check if boosted position is within the lattice
        if x_boost > N + 0.5 or x_boost < 0.5:
            C[i] = np.nan
            continue

        f_boost = np.sqrt(2.0/(N+1)) * np.sin(np.pi * k_modes * x_boost / (N+1))
        C[i] = np.sum(f_boost * f_probe * np.cos(omega * t_boost) / (2.0 * omega))

    return C


# ============================================================================
# Stage 5: BW Profile Check
# ============================================================================

def bw_profile_analysis(h_phi, h_pi, K_matrix, N):
    """
    Compare modular Hamiltonian to BW prediction:
    K_BW = 2π ∫ x T_{00} dx  →  h_π^BW = 2π·diag(d_i)  (φ eq of motion)

    On the lattice:
    - h_π should be approximately 2π × diag(d_0, d_1, ...) near the cut
    - h_φ should be approximately 2π × (distance-weighted Laplacian) near the cut
    """
    n = h_phi.shape[0]
    s = N // 2  # start index of sublattice (0-indexed in full lattice)

    distances = np.arange(n) + 0.5  # distance from cut

    # BW prediction for h_π: diagonal, 2π × distance
    h_pi_bw_diag = 2 * np.pi * distances

    # BW prediction for h_φ: distance-weighted Laplacian
    # K_BW_φ comes from 2π × ∫ x (∂φ)² dx
    # On lattice: 2π × Σ_links d_link × (Δφ)² where d_link = position of link
    # Link between sublattice sites i and i+1 is at distance i+1 from cut
    h_phi_bw = np.zeros((n, n))
    for i in range(n-1):
        d_link = i + 1.0  # distance of link (i, i+1) from cut
        h_phi_bw[i, i]     += 2*np.pi * d_link
        h_phi_bw[i+1, i+1] += 2*np.pi * d_link
        h_phi_bw[i, i+1]   -= 2*np.pi * d_link
        h_phi_bw[i+1, i]   -= 2*np.pi * d_link
    # The link from cut to site 0 is at distance d_link = 0, so no contribution.
    # But actually there IS a boundary coupling: site 0 connects to the cut.
    # The link between the last left-sublattice site and first right site
    # is at the cut position (distance 0). Weight = 0, so no contribution. ✓

    # Compute ratios (diagonal comparison)
    ratio_pi = np.diag(h_pi) / h_pi_bw_diag
    ratio_phi = np.where(np.abs(np.diag(h_phi_bw)) > 1e-10,
                         np.diag(h_phi) / np.diag(h_phi_bw),
                         np.nan)

    # Off-diagonal comparison for h_φ (first few off-diagonals)
    offdiag_actual = np.array([h_phi[i, i+1] for i in range(min(n-1, 20))])
    offdiag_bw     = np.array([h_phi_bw[i, i+1] for i in range(min(n-1, 20))])
    ratio_offdiag = np.where(np.abs(offdiag_bw) > 1e-10, offdiag_actual / offdiag_bw, np.nan)

    # Frobenius norm comparison in a window near the cut
    for w in [3, 5, 8, 12]:
        if w > n: continue
        actual_block = h_phi[:w, :w]
        bw_block = h_phi_bw[:w, :w]
        frob_err = np.linalg.norm(actual_block - bw_block) / np.linalg.norm(bw_block)

    return {
        'distances': distances.tolist(),
        'h_pi_diag': np.diag(h_pi).tolist(),
        'h_pi_bw_diag': h_pi_bw_diag.tolist(),
        'ratio_pi': ratio_pi.tolist(),
        'h_phi_diag': np.diag(h_phi).tolist(),
        'h_phi_bw_diag': np.diag(h_phi_bw).tolist(),
        'ratio_phi': ratio_phi.tolist(),
        'offdiag_actual': offdiag_actual.tolist(),
        'offdiag_bw': offdiag_bw.tolist(),
        'ratio_offdiag': ratio_offdiag.tolist(),
        'h_phi_bw': h_phi_bw,
    }


# ============================================================================
# Entanglement entropy
# ============================================================================

def entanglement_entropy(nu):
    """S = Σ_k [(ν+1/2)log(ν+1/2) - (ν-1/2)log(ν-1/2)]"""
    S = 0.0
    for v in nu:
        vp = v + 0.5
        vm = v - 0.5
        if vm > 1e-15:
            S += vp * np.log(vp) - vm * np.log(vm)
        elif vp > 1e-15:
            S += vp * np.log(vp)  # vm ≈ 0 term → 0
    return S


# ============================================================================
# KMS check
# ============================================================================

def kms_check(eps, nu):
    """Verify <n_k> = 1/(e^{ε_k} - 1) for modes with ν > 0.501."""
    mask = nu > 0.501
    if not np.any(mask):
        return {'satisfied': True, 'max_rel_err': 0.0, 'n_checked': 0, 'n_total': len(nu)}

    safe_eps = np.minimum(eps[mask], 100.0)
    n_kms = 1.0 / (np.exp(safe_eps) - 1.0)
    n_actual = nu[mask] - 0.5

    rel_err = np.abs(n_kms - n_actual) / np.maximum(n_actual, 1e-15)
    return {
        'satisfied': bool(np.max(rel_err) < 1e-6),
        'max_rel_err': float(np.max(rel_err)),
        'mean_rel_err': float(np.mean(rel_err)),
        'n_checked': int(np.sum(mask)),
        'n_total': len(nu),
    }


# ============================================================================
# Main
# ============================================================================

def run(N, tau_max=5.0, n_tau=300, verbose=True):
    pr = lambda *a, **kw: print(*a, **kw) if verbose else None

    pr(f"\n{'='*70}")
    pr(f"  N = {N}")
    pr(f"{'='*70}")

    # Stage 1
    omega, U, K_mat = build_lattice(N)
    pr(f"  Lattice: ω ∈ [{omega.min():.5f}, {omega.max():.5f}], all > 0: {np.all(omega > 0)}")

    # Stage 2
    X, P = compute_vacuum_correlators(omega, U)
    n_sub = N - N//2
    X_R = restrict_to_right_half(X, N)
    P_R = restrict_to_right_half(P, N)

    # Uncertainty check
    M_eig = np.sort(np.real(np.linalg.eigvals(X_R @ P_R)))
    pr(f"  Sublattice: {n_sub} sites. XP eigenvalues: [{M_eig.min():.6f}, {M_eig.max():.6f}]")

    # Stage 3: Modular Hamiltonian
    h_phi, h_pi, eps, nu, recon_err = compute_modular_hamiltonian(X_R, P_R)
    n_entangled = int(np.sum(nu > 0.501))
    pr(f"  Modular H: ν ∈ [{nu.min():.6f}, {nu.max():.6f}], {n_entangled}/{n_sub} entangled modes")
    pr(f"  ε ∈ [{eps.min():.4f}, {eps.max():.4f}], recon err = {recon_err:.2e}")

    # Entanglement entropy
    S_ent = entanglement_entropy(nu)
    S_cc = (1.0/3.0) * np.log(N)  # Calabrese-Cardy (leading term)
    pr(f"  Entanglement entropy: S = {S_ent:.4f}, Calabrese-Cardy ≈ (1/3)ln(N) = {S_cc:.4f}")

    # Stage 4: BW profile
    bw = bw_profile_analysis(h_phi, h_pi, K_mat, N)
    pr(f"\n  BW Profile (h_π diagonal / (2π·distance)):")
    pr(f"  {'d':>5} {'h_π':>8} {'BW':>8} {'ratio':>7} | {'h_φ':>8} {'BW_φ':>8} {'ratio':>7}")
    pr(f"  {'-'*60}")
    for i in range(min(n_sub, 12)):
        pr(f"  {bw['distances'][i]:>5.1f} {bw['h_pi_diag'][i]:>8.3f} {bw['h_pi_bw_diag'][i]:>8.3f} {bw['ratio_pi'][i]:>7.4f}"
           f" | {bw['h_phi_diag'][i]:>8.3f} {bw['h_phi_bw_diag'][i]:>8.3f} {bw['ratio_phi'][i]:>7.4f}")

    # Off-diagonal comparison
    pr(f"\n  BW Profile (h_φ off-diagonal):")
    pr(f"  {'link':>5} {'actual':>10} {'BW':>10} {'ratio':>7}")
    for i in range(min(len(bw['offdiag_actual']), 8)):
        pr(f"  {i}-{i+1}:  {bw['offdiag_actual'][i]:>10.3f} {bw['offdiag_bw'][i]:>10.3f} {bw['ratio_offdiag'][i]:>7.4f}")

    # Stage 5: Correlators
    tau_arr = np.linspace(0, tau_max, n_tau)

    # Multiple probe sites at different distances from cut
    probes = {}
    for name, idx in [('d=0.5', 0), ('d=1.5', 1), ('d=2.5', 2), ('d=5.5', 5), ('bulk', n_sub//2)]:
        if idx >= n_sub:
            continue
        d = idx + 0.5
        global_0idx = N//2 + idx

        C_mod = modular_flow_correlator(h_phi, h_pi, X_R, P_R, tau_arr, idx)
        C_full = full_H_correlator(omega, U, tau_arr, global_0idx)
        C_boost = boost_correlator(omega, U, N, tau_arr, idx)

        # L2 discrepancies (excluding NaN values from boost)
        mask_valid = ~np.isnan(C_boost)

        def l2r(a, b, m=None):
            if m is None: m = np.ones(len(a), dtype=bool)
            return np.sqrt(np.mean((a[m]-b[m])**2)) / np.sqrt(np.mean(b[m]**2)) if np.any(m) else np.nan

        disc_mod_full = l2r(C_mod, C_full)
        disc_mod_boost = l2r(C_mod, C_boost, mask_valid)
        disc_boost_full = l2r(C_boost, C_full, mask_valid)
        vac_cons = abs(C_mod[0] - C_full[0]) / abs(C_full[0]) if abs(C_full[0]) > 0 else 0

        probes[name] = {
            'idx': idx, 'd': d, 'global': global_0idx,
            'C_mod': C_mod.tolist(),
            'C_full': C_full.tolist(),
            'C_boost': C_boost.tolist(),
            'disc_mod_full': disc_mod_full,
            'disc_mod_boost': disc_mod_boost,
            'disc_boost_full': disc_boost_full,
            'vac_consistency': vac_cons,
            'n_valid_boost': int(np.sum(mask_valid)),
        }

        pr(f"\n  Probe {name} (global={global_0idx}):")
        pr(f"    Vacuum consistency: {vac_cons:.2e}")
        pr(f"    L2 discrepancy: mod vs full = {disc_mod_full:.4f}, mod vs boost = {disc_mod_boost:.4f}, boost vs full = {disc_boost_full:.4f}")
        pr(f"    Boost valid points: {np.sum(mask_valid)}/{len(tau_arr)}")

    # KMS
    kms = kms_check(eps, nu)
    pr(f"\n  KMS: satisfied={kms['satisfied']}, max_err={kms['max_rel_err']:.2e}, checked={kms['n_checked']}/{kms['n_total']}")

    return {
        'N': N, 'n_sub': n_sub,
        'modular_spectrum': {'eps': eps.tolist(), 'nu': nu.tolist(), 'n_entangled': n_entangled},
        'entropy': {'S': S_ent, 'S_cc': S_cc},
        'bw_profile': {k: v for k, v in bw.items() if k != 'h_phi_bw'},  # skip numpy matrix
        'probes': probes,
        'tau': tau_arr.tolist(),
        'kms': kms,
        'recon_err': recon_err,
    }


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    results = {}
    for N in [50, 100, 200]:
        results[str(N)] = run(N, tau_max=5.0, n_tau=300)

    # Convergence summary
    print(f"\n{'='*90}")
    print("CONVERGENCE SUMMARY")
    print(f"{'='*90}")
    print(f"{'N':>5} | {'S_ent':>6} | {'S_CC':>6} | {'mod-boost (d=0.5)':>18} | {'mod-boost (d=1.5)':>18} | {'mod-full (d=0.5)':>17} | KMS")
    print(f"{'-'*90}")
    for Ns in ['50', '100', '200']:
        r = results[Ns]
        mb05 = r['probes'].get('d=0.5', {}).get('disc_mod_boost', float('nan'))
        mb15 = r['probes'].get('d=1.5', {}).get('disc_mod_boost', float('nan'))
        mf05 = r['probes'].get('d=0.5', {}).get('disc_mod_full', float('nan'))
        print(f"{r['N']:>5} | {r['entropy']['S']:>6.3f} | {r['entropy']['S_cc']:>6.3f} | {mb05:>18.6f} | {mb15:>18.6f} | {mf05:>17.6f} | {r['kms']['satisfied']}")

    with open('results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print("\nSaved to results.json")
