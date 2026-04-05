#!/usr/bin/env python3
"""
State-Dependent Time Analysis: Focused Comparison
===================================================

Tests whether delta_C_local (modular flow response to excitation)
matches delta_C_full (physical Hamiltonian response) across N values.

Key fix from initial run: ALWAYS use mode 0 (lowest frequency)
which gives the largest physical effect (U[k,m]^2/omega_m is maximized).

Also computes multiple probe sites and generates convergence plots.
"""

import numpy as np
from scipy.linalg import expm, eigh
import json
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ============================================================================
# Core functions (from excited_state_test.py, trimmed)
# ============================================================================

def build_lattice(N):
    K = np.zeros((N, N))
    for i in range(N):
        K[i, i] = 2.0
        if i > 0: K[i, i-1] = -1.0
        if i < N-1: K[i, i+1] = -1.0
    k_modes = np.arange(1, N+1)
    omega = np.sqrt(4.0 * np.sin(np.pi * k_modes / (2*(N+1)))**2)
    j_sites = np.arange(N)
    U = np.sqrt(2.0/(N+1)) * np.sin(np.pi * np.outer(j_sites+1, k_modes) / (N+1))
    return omega, U, K

def vacuum_correlations(omega, U):
    X = U @ np.diag(1.0 / (2.0 * omega)) @ U.T
    P = U @ np.diag(omega / 2.0) @ U.T
    return X, P

def restrict(M, start, n):
    idx = list(range(start, start + n))
    return M[np.ix_(idx, idx)]

def matrix_sqrt_sym(A):
    eigvals, V = eigh(A)
    eigvals = np.maximum(eigvals, 0.0)
    return V @ np.diag(np.sqrt(eigvals)) @ V.T

def compute_modular_hamiltonian(X_R, P_R, epsilon_max=200.0):
    n = X_R.shape[0]
    X_half = matrix_sqrt_sym(X_R)
    X_half_inv = np.linalg.inv(X_half)
    D = (X_half @ P_R @ X_half + (X_half @ P_R @ X_half).T) / 2.0
    nu_sq, V = eigh(D)
    nu = np.sqrt(np.maximum(nu_sq, 0.25))
    sort_idx = np.argsort(nu)
    nu, V = nu[sort_idx], V[:, sort_idx]
    ratio = (2*nu + 1) / np.maximum(2*nu - 1, 1e-15)
    epsilon = np.minimum(np.log(ratio), epsilon_max)
    S_phi = np.diag(np.sqrt(nu)) @ V.T @ X_half_inv
    S_pi = np.diag(1.0/np.sqrt(nu)) @ V.T @ X_half
    h_phi = (S_phi.T @ np.diag(epsilon) @ S_phi)
    h_pi = (S_pi.T @ np.diag(epsilon) @ S_pi)
    h_phi = (h_phi + h_phi.T) / 2
    h_pi = (h_pi + h_pi.T) / 2
    return h_phi, h_pi, epsilon, nu

def modular_correlator(h_phi, h_pi, X_R, probe, tau_array):
    """Symmetrized correlator: (1/2)<{sigma_tau(phi_k), phi_k}>."""
    n = X_R.shape[0]
    A = np.zeros((2*n, 2*n))
    A[:n, n:] = h_pi / (2*np.pi)
    A[n:, :n] = -h_phi / (2*np.pi)
    # Sigma = [[X, 0], [0, P]]; for k < n, (M @ Sigma)[k,k] = sum_j M[k,j] X[j,k]
    # (the P block doesn't contribute since Sigma[j>=n, k<n] = 0)
    # This gives the symmetrized correlator for k < n.
    Sigma = np.zeros((2*n, 2*n))
    Sigma[:n, :n] = X_R  # only X block needed for phi_k correlator
    # Note: P block zeros out for the (k,k) element when k < n
    C = np.zeros(len(tau_array))
    for i, tau in enumerate(tau_array):
        eAt = expm(A * tau)
        C[i] = (eAt @ Sigma)[probe, probe]
    return C

def full_correlator_vacuum(omega, U, probe_global, tau_array):
    """Symmetrized vacuum correlator: sum_m U[k,m]^2 cos(w_m tau) / (2 w_m)."""
    return np.sum(U[probe_global, :]**2 / (2*omega) * np.cos(np.outer(tau_array, omega)), axis=1)

def full_correlator_excited(omega, U, probe_global, mode_idx, tau_array):
    """Exact excited-state correlator: C_vac + U[k,m]^2 / w_m cos(w_m tau)."""
    C0 = full_correlator_vacuum(omega, U, probe_global, tau_array)
    m = mode_idx
    return C0 + U[probe_global, m]**2 / omega[m] * np.cos(omega[m] * tau_array)

def l2_rel(a, b):
    d = np.sqrt(np.mean((a - b)**2))
    n = np.sqrt(np.mean(b**2))
    return d / n if n > 1e-15 else float('inf')

def linf_rel(a, b):
    d = np.max(np.abs(a - b))
    n = np.max(np.abs(b))
    return d / n if n > 1e-15 else float('inf')


# ============================================================================
# Main analysis
# ============================================================================

def analyze_N(N, mode_idx=0, tau_max=15.0, n_tau=800):
    """Full analysis for a given lattice size, always using specified mode."""
    start = N // 2
    n_R = N - start
    omega, U, K_mat = build_lattice(N)

    # Vacuum
    X_full, P_full = vacuum_correlations(omega, U)
    X_R_vac = restrict(X_full, start, n_R)
    P_R_vac = restrict(P_full, start, n_R)
    h_phi_vac, h_pi_vac, eps_vac, nu_vac = compute_modular_hamiltonian(X_R_vac, P_R_vac)

    # Excited state correlations (exact two-point functions)
    u_m = U[:, mode_idx]
    X1_full = X_full + np.outer(u_m, u_m) / omega[mode_idx]
    P1_full = P_full + np.outer(u_m, u_m) * omega[mode_idx]
    X_R_exc = restrict(X1_full, start, n_R)
    P_R_exc = restrict(P1_full, start, n_R)
    h_phi_exc, h_pi_exc, eps_exc, nu_exc = compute_modular_hamiltonian(X_R_exc, P_R_exc)

    # Perturbation size
    dh_phi_norm = np.linalg.norm(h_phi_exc - h_phi_vac) / np.linalg.norm(h_phi_vac)
    dh_pi_norm = np.linalg.norm(h_pi_exc - h_pi_vac) / np.linalg.norm(h_pi_vac)

    tau_array = np.linspace(0, tau_max, n_tau)

    # Test multiple probe positions
    probe_positions = [1, 2, max(3, n_R//4), n_R//2]
    probe_positions = sorted(set([min(p, n_R-1) for p in probe_positions]))

    results = {
        'N': N, 'n_R': n_R, 'mode_idx': mode_idx,
        'omega_m': float(omega[mode_idx]),
        'p_R': float(np.sum(U[start:, mode_idx]**2)),
        'dh_phi_norm': dh_phi_norm,
        'dh_pi_norm': dh_pi_norm,
        'probes': {},
    }

    for p_local in probe_positions:
        p_global = start + p_local

        C_loc_vac = modular_correlator(h_phi_vac, h_pi_vac, X_R_vac, p_local, tau_array)
        C_full_vac = full_correlator_vacuum(omega, U, p_global, tau_array)
        C_loc_exc = modular_correlator(h_phi_exc, h_pi_exc, X_R_exc, p_local, tau_array)
        C_full_exc = full_correlator_excited(omega, U, p_global, mode_idx, tau_array)

        dC_loc = C_loc_exc - C_loc_vac
        dC_full = C_full_exc - C_full_vac

        results['probes'][p_local] = {
            'disc_vac_l2': l2_rel(C_loc_vac, C_full_vac),
            'disc_exc_l2': l2_rel(C_loc_exc, C_full_exc),
            'delta_disc_l2': l2_rel(dC_loc, dC_full),
            'delta_disc_linf': linf_rel(dC_loc, dC_full),
            'max_dC_loc': float(np.max(np.abs(dC_loc))),
            'max_dC_full': float(np.max(np.abs(dC_full))),
            'C_loc_vac': C_loc_vac,
            'C_full_vac': C_full_vac,
            'C_loc_exc': C_loc_exc,
            'C_full_exc': C_full_exc,
            'dC_loc': dC_loc,
            'dC_full': dC_full,
            'tau': tau_array,
        }

    return results


def run_convergence_study():
    """Run the analysis for multiple N values with mode 0."""
    N_values = [20, 30, 50, 80, 100, 150, 200]
    all_results = {}

    for N in N_values:
        print(f"\n  N = {N} ...", end='', flush=True)
        r = analyze_N(N, mode_idx=0)
        all_results[N] = r
        # Print summary for one probe
        p_local = sorted(r['probes'].keys())[1]  # second probe
        p = r['probes'][p_local]
        print(f"  omega_m={r['omega_m']:.4f}, probe={p_local}, "
              f"disc_vac={p['disc_vac_l2']:.3f}, disc_exc={p['disc_exc_l2']:.3f}, "
              f"delta_disc={p['delta_disc_l2']:.3f}, "
              f"max|dC_full|={p['max_dC_full']:.4f}")

    return all_results


def make_convergence_plots(all_results, output_dir):
    """Generate convergence and comparison plots."""

    # --- Plot 1: Convergence of delta_disc with N ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    N_vals = sorted(all_results.keys())

    # For each probe position (relative), track delta_disc
    probe_styles = {1: ('o', 'Near boundary (d=1)'),
                    2: ('s', 'Near boundary (d=2)'),
                    'quarter': ('^', 'Quarter'),
                    'mid': ('D', 'Middle')}

    ax = axes[0]
    for i, p_label in enumerate(['d=1', 'd=2', 'quarter', 'mid']):
        delta_disc_vals = []
        N_plot = []
        for N in N_vals:
            probes = sorted(all_results[N]['probes'].keys())
            if i < len(probes):
                p = all_results[N]['probes'][probes[i]]
                delta_disc_vals.append(p['delta_disc_l2'])
                N_plot.append(N)
        if N_plot:
            ax.loglog(N_plot, delta_disc_vals, 'o-', label=p_label, markersize=5)

    ax.set_xlabel('N (lattice size)')
    ax.set_ylabel('||delta_C_local - delta_C_full|| / ||delta_C_full||')
    ax.set_title('State-Dependence Discrepancy vs N')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Power law fit on d=2 probe
    ax = axes[1]
    for i, p_label in enumerate(['d=1', 'd=2', 'quarter', 'mid']):
        disc_vac_vals = []
        disc_exc_vals = []
        N_plot = []
        for N in N_vals:
            probes = sorted(all_results[N]['probes'].keys())
            if i < len(probes):
                p = all_results[N]['probes'][probes[i]]
                disc_vac_vals.append(p['disc_vac_l2'])
                disc_exc_vals.append(p['disc_exc_l2'])
                N_plot.append(N)
        if N_plot:
            ax.semilogx(N_plot, disc_vac_vals, 's--', label=f'Vacuum ({p_label})', alpha=0.5, markersize=4)
            ax.semilogx(N_plot, disc_exc_vals, 'o-', label=f'Excited ({p_label})', markersize=5)

    ax.set_xlabel('N (lattice size)')
    ax.set_ylabel('L2 relative discrepancy')
    ax.set_title('Vacuum vs Excited Discrepancy')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/convergence.png', dpi=150)
    plt.close()

    # --- Plot 2: Correlator comparison for largest N ---
    N_best = max(N_vals)
    r = all_results[N_best]
    probes = sorted(r['probes'].keys())
    p_idx = min(1, len(probes)-1)  # second probe
    p_local = probes[p_idx]
    p = r['probes'][p_local]
    tau = p['tau']

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle(f'N={N_best}, mode=0 (omega={r["omega_m"]:.4f}), probe=d={p_local}', fontsize=14)

    # Row 1: Vacuum
    ax = axes[0, 0]
    ax.plot(tau, p['C_loc_vac'], 'b-', label='C_local (modular)', alpha=0.7)
    ax.plot(tau, p['C_full_vac'], 'r--', label='C_full (physical)', alpha=0.7)
    ax.set_xlabel('tau'); ax.set_ylabel('C(tau)')
    ax.set_title('Vacuum correlators')
    ax.legend(); ax.grid(True, alpha=0.3)

    ax = axes[0, 1]
    ax.plot(tau, p['C_loc_exc'], 'b-', label='C_local (modular)', alpha=0.7)
    ax.plot(tau, p['C_full_exc'], 'r--', label='C_full (physical)', alpha=0.7)
    ax.set_xlabel('tau'); ax.set_ylabel('C(tau)')
    ax.set_title('Excited-state correlators')
    ax.legend(); ax.grid(True, alpha=0.3)

    ax = axes[0, 2]
    ax.plot(tau, np.abs(p['C_loc_vac'] - p['C_full_vac']), 'k-', label='Vacuum', alpha=0.5)
    ax.plot(tau, np.abs(p['C_loc_exc'] - p['C_full_exc']), 'r-', label='Excited')
    ax.set_xlabel('tau'); ax.set_ylabel('|C_local - C_full|')
    ax.set_title('Discrepancies')
    ax.legend(); ax.grid(True, alpha=0.3)

    # Row 2: State dependence
    ax = axes[1, 0]
    ax.plot(tau, p['dC_loc'], 'b-', label='delta_C_local (modular)', linewidth=2)
    ax.plot(tau, p['dC_full'], 'r--', label='delta_C_full (physical)', linewidth=2)
    ax.set_xlabel('tau'); ax.set_ylabel('delta_C(tau)')
    ax.set_title('State-dependence: C^(1) - C^(0)')
    ax.legend(); ax.grid(True, alpha=0.3)

    ax = axes[1, 1]
    ax.plot(tau, np.abs(p['dC_loc'] - p['dC_full']), 'k-')
    ax.set_xlabel('tau'); ax.set_ylabel('|delta_C_local - delta_C_full|')
    ax.set_title('State-dependence discrepancy')
    ax.grid(True, alpha=0.3)

    # FFT comparison
    ax = axes[1, 2]
    dt = tau[1] - tau[0]
    freqs = np.fft.rfftfreq(len(tau), dt)
    fft_dC_loc = np.abs(np.fft.rfft(p['dC_loc']))
    fft_dC_full = np.abs(np.fft.rfft(p['dC_full']))
    mask = freqs > 0
    ax.plot(freqs[mask], fft_dC_loc[mask], 'b-', label='delta_C_local FFT', alpha=0.7)
    ax.plot(freqs[mask], fft_dC_full[mask], 'r--', label='delta_C_full FFT', alpha=0.7)
    ax.axvline(r['omega_m']/(2*np.pi), color='g', linestyle=':', label=f'omega_m/(2pi)={r["omega_m"]/(2*np.pi):.4f}')
    ax.set_xlabel('Frequency'); ax.set_ylabel('|FFT|')
    ax.set_title('Spectral comparison of delta_C')
    ax.legend(); ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 0.5)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/state_dependence_N{N_best}.png', dpi=150)
    plt.close()

    # --- Plot 3: Correlator comparison for N=50 ---
    if 50 in all_results:
        r50 = all_results[50]
        probes50 = sorted(r50['probes'].keys())
        p_idx50 = min(1, len(probes50)-1)
        p50 = r50['probes'][probes50[p_idx50]]
        tau50 = p50['tau']

        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        fig.suptitle(f'N=50, mode=0 (omega={r50["omega_m"]:.4f}), probe=d={probes50[p_idx50]}', fontsize=14)

        ax = axes[0]
        ax.plot(tau50, p50['dC_loc'], 'b-', label='delta_C_local', linewidth=2)
        ax.plot(tau50, p50['dC_full'], 'r--', label='delta_C_full', linewidth=2)
        ax.set_xlabel('tau'); ax.set_ylabel('delta_C')
        ax.set_title('State-dependence: C^(1) - C^(0)')
        ax.legend(); ax.grid(True, alpha=0.3)

        ax = axes[1]
        # Normalize for shape comparison
        dC_loc_max = np.max(np.abs(p50['dC_loc']))
        dC_full_max = np.max(np.abs(p50['dC_full']))
        if dC_loc_max > 1e-15 and dC_full_max > 1e-15:
            ax.plot(tau50, p50['dC_loc']/dC_loc_max, 'b-', label='delta_C_local (normalized)', linewidth=2)
            ax.plot(tau50, p50['dC_full']/dC_full_max, 'r--', label='delta_C_full (normalized)', linewidth=2)
        ax.set_xlabel('tau'); ax.set_ylabel('Normalized delta_C')
        ax.set_title('Shape comparison (normalized)')
        ax.legend(); ax.grid(True, alpha=0.3)

        ax = axes[2]
        freqs50 = np.fft.rfftfreq(len(tau50), tau50[1]-tau50[0])
        fft50_loc = np.abs(np.fft.rfft(p50['dC_loc']))
        fft50_full = np.abs(np.fft.rfft(p50['dC_full']))
        mask50 = freqs50 > 0
        ax.plot(freqs50[mask50], fft50_loc[mask50], 'b-', label='delta_C_local FFT', alpha=0.7)
        ax.plot(freqs50[mask50], fft50_full[mask50], 'r--', label='delta_C_full FFT', alpha=0.7)
        ax.axvline(r50['omega_m']/(2*np.pi), color='g', linestyle=':', label=f'omega_m/(2pi)')
        ax.set_xlabel('Frequency'); ax.set_ylabel('|FFT|')
        ax.set_title('Spectral comparison')
        ax.legend(); ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 0.5)

        plt.tight_layout()
        plt.savefig(f'{output_dir}/state_dependence_N50.png', dpi=150)
        plt.close()

    # --- Plot 4: Entanglement spectrum comparison ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for N in [50, 100, 200]:
        if N not in all_results:
            continue
        r = all_results[N]
        # Recompute nu_vac and nu_exc (not stored in results dict)
        omega, U, _ = build_lattice(N)
        X_f, P_f = vacuum_correlations(omega, U)
        st = N // 2; nR = N - st
        X_R_v = restrict(X_f, st, nR)
        P_R_v = restrict(P_f, st, nR)
        _, _, _, nu_v = compute_modular_hamiltonian(X_R_v, P_R_v)

        u_m = U[:, 0]
        X_R_e = restrict(X_f + np.outer(u_m, u_m)/omega[0], st, nR)
        P_R_e = restrict(P_f + np.outer(u_m, u_m)*omega[0], st, nR)
        _, _, _, nu_e = compute_modular_hamiltonian(X_R_e, P_R_e)

        axes[0].plot(nu_v, 'o-', label=f'N={N} vacuum', markersize=3, alpha=0.7)
        axes[0].plot(nu_e, 's--', label=f'N={N} excited', markersize=3, alpha=0.7)

        delta_nu = nu_e - nu_v
        axes[1].plot(delta_nu, 'o-', label=f'N={N}', markersize=3)

    axes[0].set_xlabel('Mode index')
    axes[0].set_ylabel('Symplectic eigenvalue nu')
    axes[0].set_title('Entanglement Spectrum')
    axes[0].legend(fontsize=8)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_yscale('log')

    axes[1].set_xlabel('Mode index')
    axes[1].set_ylabel('delta_nu = nu_exc - nu_vac')
    axes[1].set_title('Spectrum Change from Excitation')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/entanglement_spectrum.png', dpi=150)
    plt.close()

    print(f"\nPlots saved to {output_dir}/")


if __name__ == '__main__':
    output_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(output_dir)

    print("=" * 70)
    print("  STATE-DEPENDENT TIME ANALYSIS")
    print("  Mode: 0 (lowest frequency) across all N")
    print("=" * 70)

    all_results = run_convergence_study()

    # Print convergence table
    N_vals = sorted(all_results.keys())
    print(f"\n{'='*100}")
    print("CONVERGENCE TABLE (mode 0, all probes)")
    print(f"{'='*100}")
    print(f"{'N':>5} | {'omega_m':>8} | {'probe':>5} | {'disc_vac':>10} | {'disc_exc':>10} | {'delta_disc':>11} | {'max|dC_loc|':>12} | {'max|dC_full|':>12}")
    print(f"{'-'*100}")
    for N in N_vals:
        r = all_results[N]
        for p_local in sorted(r['probes'].keys()):
            p = r['probes'][p_local]
            print(f"{N:>5} | {r['omega_m']:>8.4f} | {p_local:>5} | {p['disc_vac_l2']:>10.4f} | {p['disc_exc_l2']:>10.4f} | {p['delta_disc_l2']:>11.4f} | {p['max_dC_loc']:>12.6f} | {p['max_dC_full']:>12.6f}")

    # Power law fit for delta_disc convergence
    print(f"\n{'='*70}")
    print("POWER LAW FIT: delta_disc ~ a * N^b")
    print(f"{'='*70}")
    for probe_offset in [0, 1]:  # first and second probe
        N_fit = []
        dd_fit = []
        for N in N_vals:
            probes = sorted(all_results[N]['probes'].keys())
            if probe_offset < len(probes):
                dd = all_results[N]['probes'][probes[probe_offset]]['delta_disc_l2']
                if dd > 0 and np.isfinite(dd):
                    N_fit.append(N)
                    dd_fit.append(dd)
        if len(N_fit) >= 3:
            log_N = np.log(np.array(N_fit))
            log_dd = np.log(np.array(dd_fit))
            b, log_a = np.polyfit(log_N, log_dd, 1)
            a = np.exp(log_a)
            print(f"  Probe offset {probe_offset}: delta_disc ~ {a:.3f} * N^({b:.3f})")
            print(f"    Data: {list(zip(N_fit, [f'{d:.4f}' for d in dd_fit]))}")

    # Generate plots
    make_convergence_plots(all_results, output_dir)

    # Save summary
    summary = {}
    for N in N_vals:
        r = all_results[N]
        summary[str(N)] = {
            'omega_m': r['omega_m'],
            'p_R': r['p_R'],
            'dh_phi_norm': r['dh_phi_norm'],
            'dh_pi_norm': r['dh_pi_norm'],
            'probes': {
                str(k): {kk: vv for kk, vv in v.items()
                         if kk not in ('C_loc_vac', 'C_full_vac', 'C_loc_exc',
                                       'C_full_exc', 'dC_loc', 'dC_full', 'tau')}
                for k, v in r['probes'].items()
            }
        }

    with open('convergence_results.json', 'w') as f:
        json.dump(summary, f, indent=2)
    print("\nResults saved to convergence_results.json")
