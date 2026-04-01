#!/usr/bin/env python3
"""
Convergence with FIXED physical frequency.

Previous convergence used mode 0 (omega → 0 as N → ∞), which made
delta_C_full approach a constant, artificially reducing the L2 discrepancy.

This test uses a mode with omega ≈ 0.3 for all N values, keeping the
physical frequency fixed as we take N → ∞.
"""

import numpy as np
from scipy.linalg import expm, eigh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

from state_dependence_analysis import (
    build_lattice, vacuum_correlations, restrict, compute_modular_hamiltonian,
    modular_correlator, full_correlator_vacuum, full_correlator_excited, l2_rel
)


def find_mode_near_freq(omega, target_omega):
    """Find the mode index closest to the target frequency."""
    return int(np.argmin(np.abs(omega - target_omega)))


def run_fixed_freq_convergence(target_omega=0.3, tau_max=50.0, n_tau=2000):
    """Run convergence study with a fixed physical frequency."""

    N_values = [30, 50, 80, 100, 150, 200]
    probe_offset = 2  # near-boundary

    results = []

    print(f"\n{'='*80}")
    print(f"  FIXED-FREQUENCY CONVERGENCE: target omega = {target_omega}")
    print(f"{'='*80}")
    print(f"{'N':>5} | {'mode':>5} | {'omega':>8} | {'disc_vac':>10} | {'disc_exc':>10} | {'delta_disc':>11} | {'delta_linf':>11} | {'max|dC_l|':>10} | {'max|dC_f|':>10}")
    print(f"{'-'*95}")

    tau_array = np.linspace(0, tau_max, n_tau)

    for N in N_values:
        start = N // 2
        n_R = N - start
        omega, U, K_mat = build_lattice(N)

        mode_idx = find_mode_near_freq(omega, target_omega)
        actual_omega = omega[mode_idx]

        # Vacuum
        X_full, P_full = vacuum_correlations(omega, U)
        X_R_vac = restrict(X_full, start, n_R)
        P_R_vac = restrict(P_full, start, n_R)
        h_phi_vac, h_pi_vac, _, _ = compute_modular_hamiltonian(X_R_vac, P_R_vac)

        # Excited
        u_m = U[:, mode_idx]
        X_R_exc = restrict(X_full + np.outer(u_m, u_m)/actual_omega, start, n_R)
        P_R_exc = restrict(P_full + np.outer(u_m, u_m)*actual_omega, start, n_R)
        h_phi_exc, h_pi_exc, _, _ = compute_modular_hamiltonian(X_R_exc, P_R_exc)

        probe = min(probe_offset, n_R - 1)
        p_global = start + probe

        C_loc_vac = modular_correlator(h_phi_vac, h_pi_vac, X_R_vac, probe, tau_array)
        C_full_vac = full_correlator_vacuum(omega, U, p_global, tau_array)
        C_loc_exc = modular_correlator(h_phi_exc, h_pi_exc, X_R_exc, probe, tau_array)
        C_full_exc = full_correlator_excited(omega, U, p_global, mode_idx, tau_array)

        dC_loc = C_loc_exc - C_loc_vac
        dC_full = C_full_exc - C_full_vac

        disc_vac = l2_rel(C_loc_vac, C_full_vac)
        disc_exc = l2_rel(C_loc_exc, C_full_exc)
        dd_l2 = l2_rel(dC_loc, dC_full)

        # Linf relative
        dd_linf = np.max(np.abs(dC_loc - dC_full)) / np.max(np.abs(dC_full)) if np.max(np.abs(dC_full)) > 1e-15 else float('inf')

        max_dC_loc = np.max(np.abs(dC_loc))
        max_dC_full = np.max(np.abs(dC_full))

        results.append({
            'N': N, 'mode_idx': mode_idx, 'omega': actual_omega,
            'disc_vac': disc_vac, 'disc_exc': disc_exc,
            'dd_l2': dd_l2, 'dd_linf': dd_linf,
            'max_dC_loc': max_dC_loc, 'max_dC_full': max_dC_full,
            'dC_loc': dC_loc, 'dC_full': dC_full,
            'tau': tau_array,
        })

        print(f"{N:>5} | {mode_idx:>5} | {actual_omega:>8.4f} | {disc_vac:>10.4f} | {disc_exc:>10.4f} | {dd_l2:>11.4f} | {dd_linf:>11.4f} | {max_dC_loc:>10.4f} | {max_dC_full:>10.4f}")

    # Power law fit
    N_arr = np.array([r['N'] for r in results])
    dd_arr = np.array([r['dd_l2'] for r in results])
    valid = (dd_arr > 0) & np.isfinite(dd_arr)
    if np.sum(valid) >= 3:
        b, log_a = np.polyfit(np.log(N_arr[valid]), np.log(dd_arr[valid]), 1)
        print(f"\nPower law fit: delta_disc ~ {np.exp(log_a):.3f} * N^({b:.3f})")

    # Also check if delta_disc is converging to 0 or to a constant
    if len(results) >= 3:
        last3 = [r['dd_l2'] for r in results[-3:]]
        print(f"Last 3 values: {[f'{v:.4f}' for v in last3]}")
        variation = (max(last3) - min(last3)) / np.mean(last3)
        print(f"Variation in last 3: {variation:.2%}")
        if variation < 0.1:
            print("  -> PLATEAU: delta_disc appears to converge to a NONZERO value")
        else:
            print("  -> STILL CHANGING: delta_disc may converge to 0 or to a nonzero value")

    return results


def compare_convergence_modes(output_dir):
    """Compare convergence for mode 0 (omega→0) vs fixed omega."""

    # Mode 0 convergence
    print("\n\n=== MODE 0 (omega → 0 as N → ∞) ===")
    from state_dependence_analysis import analyze_N
    mode0_results = {}
    for N in [30, 50, 80, 100, 150, 200]:
        r = analyze_N(N, mode_idx=0, tau_max=15.0)
        p = r['probes'][sorted(r['probes'].keys())[1]]
        mode0_results[N] = p['delta_disc_l2']
        print(f"  N={N}: delta_disc = {p['delta_disc_l2']:.4f}, omega_m = {r['omega_m']:.4f}")

    # Fixed omega convergence (already computed above)
    print("\n=== FIXED OMEGA ≈ 0.3 ===")
    fixed_results = run_fixed_freq_convergence(target_omega=0.3)

    # Also test omega ≈ 0.6
    print("\n=== FIXED OMEGA ≈ 0.6 ===")
    fixed_results_06 = run_fixed_freq_convergence(target_omega=0.6)

    # Plot comparison
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Panel 1: delta_disc vs N
    ax = axes[0]
    N_m0 = sorted(mode0_results.keys())
    ax.loglog(N_m0, [mode0_results[n] for n in N_m0], 'bo-', label='mode 0 (omega→0)', markersize=6)
    N_f = [r['N'] for r in fixed_results]
    ax.loglog(N_f, [r['dd_l2'] for r in fixed_results], 'rs-', label='fixed omega≈0.3', markersize=6)
    N_f2 = [r['N'] for r in fixed_results_06]
    ax.loglog(N_f2, [r['dd_l2'] for r in fixed_results_06], 'g^-', label='fixed omega≈0.6', markersize=6)
    ax.set_xlabel('N (lattice size)', fontsize=12)
    ax.set_ylabel('delta_disc (L2 relative)', fontsize=12)
    ax.set_title('Convergence: mode 0 vs fixed frequency', fontsize=13)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    # Reference lines
    N_ref = np.array([30, 200])
    ax.loglog(N_ref, 5.0*N_ref**(-0.5), 'k--', alpha=0.3, label='~N^{-1/2}')
    ax.legend(fontsize=10)

    # Panel 2: amplitude ratio
    ax = axes[1]
    ratios_f = [r['max_dC_loc']/r['max_dC_full'] for r in fixed_results if r['max_dC_full'] > 1e-10]
    ratios_f2 = [r['max_dC_loc']/r['max_dC_full'] for r in fixed_results_06 if r['max_dC_full'] > 1e-10]
    ax.plot(N_f[:len(ratios_f)], ratios_f, 'rs-', label='omega≈0.3', markersize=6)
    ax.plot(N_f2[:len(ratios_f2)], ratios_f2, 'g^-', label='omega≈0.6', markersize=6)
    ax.axhline(1.0, color='k', linestyle=':', alpha=0.5)
    ax.set_xlabel('N (lattice size)', fontsize=12)
    ax.set_ylabel('max|dC_local| / max|dC_full|', fontsize=12)
    ax.set_title('Amplitude amplification by modular flow', fontsize=13)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/fixed_freq_convergence.png', dpi=150)
    plt.close()
    print(f"\nPlot saved to {output_dir}/fixed_freq_convergence.png")


if __name__ == '__main__':
    output_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(output_dir)
    compare_convergence_modes(output_dir)
