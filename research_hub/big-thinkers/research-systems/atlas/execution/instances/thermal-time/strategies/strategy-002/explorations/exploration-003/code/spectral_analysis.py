#!/usr/bin/env python3
"""
Detailed Spectral Analysis of delta_C
======================================

Compares the frequency content of delta_C_local (modular) vs delta_C_full (physical)
to determine if the discrepancy is structural (wrong frequencies) or quantitative
(right frequencies, wrong amplitudes).

Key diagnostic: delta_C_full is EXACTLY cos(omega_m * tau) * U[k,m]^2/omega_m,
so it has a single peak at f = omega_m/(2pi). Does delta_C_local have this peak?
"""

import numpy as np
from scipy.linalg import expm, eigh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# Import core functions
from state_dependence_analysis import (
    build_lattice, vacuum_correlations, restrict, compute_modular_hamiltonian,
    modular_correlator, full_correlator_vacuum, full_correlator_excited
)


def spectral_decomposition(signal, tau_array, zero_pad_factor=8):
    """High-resolution FFT with zero-padding."""
    n = len(signal)
    n_padded = n * zero_pad_factor
    dt = tau_array[1] - tau_array[0]

    # Window to reduce spectral leakage
    window = np.hanning(n)
    windowed = signal * window

    fft = np.fft.rfft(windowed, n=n_padded)
    freqs = np.fft.rfftfreq(n_padded, dt)
    amplitudes = 2.0 * np.abs(fft) / np.sum(window)  # normalize by window

    return freqs, amplitudes


def find_peaks(freqs, amps, n_peaks=5, min_freq=0.001):
    """Find the top n_peaks frequency peaks."""
    mask = freqs > min_freq
    f_masked = freqs[mask]
    a_masked = amps[mask]

    peaks = []
    for _ in range(n_peaks):
        if len(a_masked) == 0:
            break
        idx = np.argmax(a_masked)
        peaks.append((f_masked[idx], a_masked[idx]))
        # Zero out a neighborhood around the peak
        lo = max(0, idx - 5)
        hi = min(len(a_masked), idx + 6)
        a_masked[lo:hi] = 0
    return peaks


def run_spectral_analysis(N=100, mode_idx=0):
    """Detailed spectral comparison for given N."""
    start = N // 2
    n_R = N - start
    omega, U, K_mat = build_lattice(N)

    # Use high-resolution parameters
    tau_max = 50.0  # longer window for better frequency resolution
    n_tau = 2000

    X_full, P_full = vacuum_correlations(omega, U)
    X_R_vac = restrict(X_full, start, n_R)
    P_R_vac = restrict(P_full, start, n_R)
    h_phi_vac, h_pi_vac, eps_vac, nu_vac = compute_modular_hamiltonian(X_R_vac, P_R_vac)

    u_m = U[:, mode_idx]
    X_R_exc = restrict(X_full + np.outer(u_m, u_m)/omega[mode_idx], start, n_R)
    P_R_exc = restrict(P_full + np.outer(u_m, u_m)*omega[mode_idx], start, n_R)
    h_phi_exc, h_pi_exc, eps_exc, nu_exc = compute_modular_hamiltonian(X_R_exc, P_R_exc)

    tau_array = np.linspace(0, tau_max, n_tau)

    # Test probes at d=2 and d=n_R//4
    probes = [2, max(3, n_R // 4)]

    target_freq = omega[mode_idx] / (2 * np.pi)

    print(f"\n{'='*70}")
    print(f"SPECTRAL ANALYSIS: N={N}, mode={mode_idx}, omega_m={omega[mode_idx]:.6f}")
    print(f"Target frequency (omega_m / 2pi) = {target_freq:.6f}")
    print(f"Modular energies: eps_vac = [{eps_vac.min():.3f}, {eps_vac.max():.3f}]")
    print(f"                  eps_exc = [{eps_exc.min():.3f}, {eps_exc.max():.3f}]")
    print(f"{'='*70}")

    # Also print the modular energies for reference
    # The modular flow frequencies are eps_k / (2pi)
    mod_freqs_vac = eps_vac / (2 * np.pi)
    mod_freqs_exc = eps_exc / (2 * np.pi)
    print(f"\nModular flow frequencies (eps/(2pi)):")
    print(f"  Vacuum (first 5): {mod_freqs_vac[:5].round(4)}")
    print(f"  Excited (first 5): {mod_freqs_exc[:5].round(4)}")

    fig, axes = plt.subplots(len(probes), 3, figsize=(20, 6*len(probes)))
    if len(probes) == 1:
        axes = axes[np.newaxis, :]

    for pi, p_local in enumerate(probes):
        p_global = start + p_local

        # Compute correlators
        C_loc_vac = modular_correlator(h_phi_vac, h_pi_vac, X_R_vac, p_local, tau_array)
        C_full_vac = full_correlator_vacuum(omega, U, p_global, tau_array)
        C_loc_exc = modular_correlator(h_phi_exc, h_pi_exc, X_R_exc, p_local, tau_array)
        C_full_exc = full_correlator_excited(omega, U, p_global, mode_idx, tau_array)

        dC_loc = C_loc_exc - C_loc_vac
        dC_full = C_full_exc - C_full_vac

        # Spectral decomposition
        freqs_loc, amps_loc = spectral_decomposition(dC_loc, tau_array)
        freqs_full, amps_full = spectral_decomposition(dC_full, tau_array)

        # Find peaks
        peaks_loc = find_peaks(freqs_loc, amps_loc.copy(), n_peaks=5)
        peaks_full = find_peaks(freqs_full, amps_full.copy(), n_peaks=5)

        print(f"\n--- Probe d={p_local} ---")
        print(f"  delta_C_full peaks:")
        for f, a in peaks_full:
            print(f"    f={f:.6f} (ratio to target: {f/target_freq:.3f}), amp={a:.6f}")
        print(f"  delta_C_local peaks:")
        for f, a in peaks_loc:
            print(f"    f={f:.6f} (ratio to target: {f/target_freq:.3f}), amp={a:.6f}")

        # Check if target frequency is present in delta_C_local
        # Find amplitude at target frequency
        idx_target = np.argmin(np.abs(freqs_loc - target_freq))
        amp_loc_at_target = amps_loc[idx_target]
        idx_target_full = np.argmin(np.abs(freqs_full - target_freq))
        amp_full_at_target = amps_full[idx_target_full]

        print(f"  Amplitude at target freq:")
        print(f"    delta_C_full:  {amp_full_at_target:.6f}")
        print(f"    delta_C_local: {amp_loc_at_target:.6f}")
        print(f"    Ratio (local/full): {amp_loc_at_target/amp_full_at_target:.4f}" if amp_full_at_target > 1e-10 else "")

        # Is the dominant frequency of delta_C_local the target?
        if peaks_loc:
            dominant_loc = peaks_loc[0][0]
            print(f"  Dominant freq of delta_C_local: {dominant_loc:.6f} (ratio to target: {dominant_loc/target_freq:.3f})")
            if abs(dominant_loc - target_freq) / target_freq < 0.1:
                print(f"  -> MATCH: dominant frequency matches target (within 10%)")
            else:
                print(f"  -> MISMATCH: dominant frequency differs from target by {abs(dominant_loc - target_freq) / target_freq * 100:.1f}%")

        # Plot time-domain comparison
        ax = axes[pi, 0]
        ax.plot(tau_array[:500], dC_loc[:500], 'b-', label='delta_C_local', linewidth=1.5)
        ax.plot(tau_array[:500], dC_full[:500], 'r--', label='delta_C_full', linewidth=1.5)
        ax.set_xlabel('tau')
        ax.set_ylabel('delta_C(tau)')
        ax.set_title(f'Probe d={p_local}: Time domain')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Plot spectral comparison
        ax = axes[pi, 1]
        freq_max = min(0.3, 5 * target_freq) if target_freq > 0 else 0.3
        mask = (freqs_loc > 0) & (freqs_loc < freq_max)
        ax.plot(freqs_loc[mask], amps_loc[mask], 'b-', label='delta_C_local', alpha=0.7)
        mask_f = (freqs_full > 0) & (freqs_full < freq_max)
        ax.plot(freqs_full[mask_f], amps_full[mask_f], 'r--', label='delta_C_full', alpha=0.7)
        ax.axvline(target_freq, color='g', linestyle=':', linewidth=2, label=f'omega_m/(2pi)={target_freq:.4f}')
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Spectral amplitude')
        ax.set_title(f'Probe d={p_local}: Low-frequency spectrum')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Plot wide-band spectral comparison
        ax = axes[pi, 2]
        freq_wide = 1.0
        mask_w = (freqs_loc > 0) & (freqs_loc < freq_wide)
        ax.plot(freqs_loc[mask_w], amps_loc[mask_w], 'b-', label='delta_C_local', alpha=0.7)
        mask_wf = (freqs_full > 0) & (freqs_full < freq_wide)
        ax.plot(freqs_full[mask_wf], amps_full[mask_wf], 'r--', label='delta_C_full', alpha=0.7)
        ax.axvline(target_freq, color='g', linestyle=':', linewidth=2, label=f'omega_m/(2pi)')
        # Also mark modular frequencies
        for k, mf in enumerate(mod_freqs_exc[:5]):
            if mf < freq_wide:
                ax.axvline(mf, color='purple', linestyle='--', alpha=0.3, linewidth=0.5)
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Spectral amplitude')
        ax.set_title(f'Probe d={p_local}: Wide-band spectrum')
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    output_dir = os.path.dirname(os.path.abspath(__file__))
    plt.savefig(f'{output_dir}/spectral_analysis_N{N}.png', dpi=150)
    plt.close()
    print(f"\nPlot saved to {output_dir}/spectral_analysis_N{N}.png")


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Run for N=100 (good resolution, manageable size)
    run_spectral_analysis(N=100, mode_idx=0)

    # Also run for N=50 for comparison
    run_spectral_analysis(N=50, mode_idx=0)
