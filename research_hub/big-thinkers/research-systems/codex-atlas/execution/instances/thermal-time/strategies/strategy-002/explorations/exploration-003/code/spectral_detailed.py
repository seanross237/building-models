#!/usr/bin/env python3
"""
High-resolution spectral analysis with properly-resolved frequencies.
Tests both mode 0 (with long tau window) and a mid-frequency mode.
"""

import numpy as np
from scipy.linalg import expm, eigh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

from state_dependence_analysis import (
    build_lattice, vacuum_correlations, restrict, compute_modular_hamiltonian,
    modular_correlator, full_correlator_vacuum, full_correlator_excited
)


def run_resolved_analysis(N, mode_idx, tau_max, n_tau, label=""):
    """Run spectral analysis with parameters chosen to resolve the mode frequency."""
    start = N // 2
    n_R = N - start
    omega, U, K_mat = build_lattice(N)

    X_full, P_full = vacuum_correlations(omega, U)
    X_R_vac = restrict(X_full, start, n_R)
    P_R_vac = restrict(P_full, start, n_R)
    h_phi_vac, h_pi_vac, eps_vac, nu_vac = compute_modular_hamiltonian(X_R_vac, P_R_vac)

    u_m = U[:, mode_idx]
    X_R_exc = restrict(X_full + np.outer(u_m, u_m)/omega[mode_idx], start, n_R)
    P_R_exc = restrict(P_full + np.outer(u_m, u_m)*omega[mode_idx], start, n_R)
    h_phi_exc, h_pi_exc, eps_exc, nu_exc = compute_modular_hamiltonian(X_R_exc, P_R_exc)

    tau = np.linspace(0, tau_max, n_tau)
    target_freq = omega[mode_idx] / (2 * np.pi)
    freq_res = 1.0 / tau_max
    n_cycles = target_freq * tau_max

    print(f"\n{'='*70}")
    print(f"  {label}: N={N}, mode={mode_idx}, omega_m={omega[mode_idx]:.4f}")
    print(f"  target f = {target_freq:.6f}, freq resolution = {freq_res:.6f}")
    print(f"  # cycles in window = {n_cycles:.1f}")
    print(f"{'='*70}")

    # Modular energies (non-trivial ones)
    active = eps_vac < 35
    print(f"  Active modular energies (vacuum): {eps_vac[active].round(3)}")
    print(f"  Active modular energies (excited): {eps_exc[active | (eps_exc < 35)].round(3)}")
    # The modular flow oscillation frequencies are eps_k / (2pi)
    print(f"  Modular frequencies (vac, first active): {(eps_vac[active]/(2*np.pi)).round(4)}")
    print(f"  Modular frequencies (exc, first active): {(eps_exc[active | (eps_exc < 35)]/(2*np.pi)).round(4)}")

    probe = 2  # near-boundary probe
    p_global = start + probe

    C_loc_vac = modular_correlator(h_phi_vac, h_pi_vac, X_R_vac, probe, tau)
    C_full_vac = full_correlator_vacuum(omega, U, p_global, tau)
    C_loc_exc = modular_correlator(h_phi_exc, h_pi_exc, X_R_exc, probe, tau)
    C_full_exc = full_correlator_excited(omega, U, p_global, mode_idx, tau)

    dC_loc = C_loc_exc - C_loc_vac
    dC_full = C_full_exc - C_full_vac

    # FFT with zero-padding
    n_pad = n_tau * 4
    dt = tau[1] - tau[0]
    window = np.hanning(n_tau)

    fft_dC_loc = np.fft.rfft(dC_loc * window, n=n_pad)
    fft_dC_full = np.fft.rfft(dC_full * window, n=n_pad)
    freqs = np.fft.rfftfreq(n_pad, dt)
    amp_loc = 2.0 * np.abs(fft_dC_loc) / np.sum(window)
    amp_full = 2.0 * np.abs(fft_dC_full) / np.sum(window)

    # Find peaks
    def peaks(amps, freqs, n=5, min_f=0.0005):
        a = amps.copy()
        a[freqs < min_f] = 0
        result = []
        for _ in range(n):
            idx = np.argmax(a)
            if a[idx] < 1e-10:
                break
            result.append((freqs[idx], a[idx]))
            lo, hi = max(0, idx-10), min(len(a), idx+11)
            a[lo:hi] = 0
        return result

    peaks_full = peaks(amp_full, freqs)
    peaks_loc = peaks(amp_loc, freqs)

    print(f"\n  delta_C_full peaks:")
    for f, a in peaks_full:
        print(f"    f={f:.6f}  amp={a:.4f}  ratio_to_target={f/target_freq:.2f}")
    print(f"  delta_C_local peaks:")
    for f, a in peaks_loc:
        print(f"    f={f:.6f}  amp={a:.4f}  ratio_to_target={f/target_freq:.2f}")

    # Amplitude at target frequency
    idx_t = np.argmin(np.abs(freqs - target_freq))
    print(f"\n  At target freq ({target_freq:.6f}):")
    print(f"    amp_full = {amp_full[idx_t]:.6f}")
    print(f"    amp_loc  = {amp_loc[idx_t]:.6f}")
    if amp_full[idx_t] > 1e-10:
        print(f"    ratio    = {amp_loc[idx_t]/amp_full[idx_t]:.4f}")

    # Check if ANY of the delta_C_local peaks are near the target
    near_target = any(abs(f - target_freq)/target_freq < 0.15 for f, a in peaks_loc)
    print(f"\n  Target frequency in delta_C_local top peaks? {'YES' if near_target else 'NO'}")

    return {
        'tau': tau, 'dC_loc': dC_loc, 'dC_full': dC_full,
        'freqs': freqs, 'amp_loc': amp_loc, 'amp_full': amp_full,
        'target_freq': target_freq, 'peaks_loc': peaks_loc, 'peaks_full': peaks_full,
        'eps_vac': eps_vac, 'eps_exc': eps_exc,
        'C_loc_vac': C_loc_vac, 'C_full_vac': C_full_vac,
        'label': label, 'omega_m': omega[mode_idx],
    }


def make_spectral_plots(results_list, output_dir):
    """Make comparison plots for all analyses."""
    n = len(results_list)
    fig, axes = plt.subplots(n, 3, figsize=(20, 6*n))
    if n == 1:
        axes = axes[np.newaxis, :]

    for i, r in enumerate(results_list):
        tau = r['tau']
        tf = r['target_freq']

        # Time domain
        ax = axes[i, 0]
        ax.plot(tau, r['dC_loc'], 'b-', label='delta_C_local', linewidth=1.5, alpha=0.8)
        ax.plot(tau, r['dC_full'], 'r--', label='delta_C_full', linewidth=1.5, alpha=0.8)
        ax.set_xlabel('tau')
        ax.set_ylabel('delta_C')
        ax.set_title(f'{r["label"]}: Time domain (first 2T)')
        # Show first 2 full periods
        T = 1.0 / tf if tf > 0 else len(tau)
        ax.set_xlim(0, min(2.5*T, tau[-1]))
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Spectral: narrow band around target
        ax = axes[i, 1]
        mask = (r['freqs'] > 0) & (r['freqs'] < max(15*tf, 0.05))
        ax.plot(r['freqs'][mask], r['amp_loc'][mask], 'b-', label='delta_C_local', linewidth=1.5, alpha=0.8)
        ax.plot(r['freqs'][mask], r['amp_full'][mask], 'r--', label='delta_C_full', linewidth=1.5, alpha=0.8)
        ax.axvline(tf, color='g', linestyle=':', linewidth=2, label=f'omega_m/(2pi)={tf:.4f}')
        # Mark modular frequencies
        for k, e in enumerate(r['eps_exc'][:5]):
            mf = e / (2*np.pi)
            if mf < 15*tf:
                ax.axvline(mf, color='purple', linestyle='--', alpha=0.4, linewidth=0.8)
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Spectral amplitude')
        ax.set_title(f'{r["label"]}: Low-f spectrum')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

        # Spectral: wide band
        ax = axes[i, 2]
        mask_w = (r['freqs'] > 0) & (r['freqs'] < 0.5)
        ax.plot(r['freqs'][mask_w], r['amp_loc'][mask_w], 'b-', label='delta_C_local', alpha=0.7)
        ax.plot(r['freqs'][mask_w], r['amp_full'][mask_w], 'r--', label='delta_C_full', alpha=0.7)
        ax.axvline(tf, color='g', linestyle=':', linewidth=2, label='omega_m/(2pi)')
        for k, e in enumerate(r['eps_exc'][:5]):
            mf = e / (2*np.pi)
            if mf < 0.5:
                ax.axvline(mf, color='purple', linestyle='--', alpha=0.4)
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Spectral amplitude')
        ax.set_title(f'{r["label"]}: Wide-band spectrum')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/spectral_detailed.png', dpi=150)
    plt.close()
    print(f"\nDetailed spectral plot saved to {output_dir}/spectral_detailed.png")


if __name__ == '__main__':
    output_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(output_dir)

    results_list = []

    # Test 1: N=50, mode 0 with LONG tau window (need ~10 periods)
    # omega_0 ≈ 0.062, T ≈ 102. tau_max = 500 gives ~5 periods.
    r1 = run_resolved_analysis(N=50, mode_idx=0, tau_max=500, n_tau=5000,
                                label="N=50, mode 0 (IR)")
    results_list.append(r1)

    # Test 2: N=50, mode 5 (mid-frequency)
    # omega_5 ≈ 0.55, T ≈ 11. tau_max = 100 gives ~9 periods.
    r2 = run_resolved_analysis(N=50, mode_idx=5, tau_max=100, n_tau=2000,
                                label="N=50, mode 5 (mid-f)")
    results_list.append(r2)

    # Test 3: N=100, mode 0 with LONG tau window
    # omega_0 ≈ 0.031, T ≈ 202. tau_max = 1000 gives ~5 periods.
    r3 = run_resolved_analysis(N=100, mode_idx=0, tau_max=1000, n_tau=5000,
                                label="N=100, mode 0 (IR)")
    results_list.append(r3)

    # Test 4: N=100, mode 5 (mid-frequency)
    r4 = run_resolved_analysis(N=100, mode_idx=5, tau_max=100, n_tau=2000,
                                label="N=100, mode 5 (mid-f)")
    results_list.append(r4)

    make_spectral_plots(results_list, output_dir)
