#!/usr/bin/env python3
"""
Generate FFT comparison plots for the Gaussian caveat resolution.
"""

import numpy as np
import json
import os
import sys

# Check for matplotlib
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("matplotlib not available — generating text-based summary only")

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def load_data(N):
    """Load Part B data for a given N."""
    with open(f'part_b_N{N}_data.json', 'r') as f:
        return json.load(f)


def fft_with_freq(signal, tau_arr, pad=8):
    dt = tau_arr[1] - tau_arr[0]
    n_pad = len(signal) * pad
    sig = np.array(signal) - np.mean(signal)
    fft_vals = np.abs(np.fft.rfft(sig, n=n_pad))
    freqs = np.fft.rfftfreq(n_pad, d=dt) * 2 * np.pi
    return freqs, fft_vals


if HAS_MPL:
    # ---- Figure 1: Time-domain comparison for N=100 ----
    data = load_data(100)
    tau = np.array(data['tau_array'])
    dCl = np.array(data['delta_C_local'])
    dCf = np.array(data['delta_C_full'])
    eps_sq = np.array(data['eps_sq'])

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Squeezed State Modular Flow: N=100, r=0.5, mode=25', fontsize=14)

    # Panel 1: Time domain
    ax = axes[0, 0]
    ax.plot(tau, dCl, 'b-', linewidth=0.8, label=r'$\delta C_{\rm local}(\tau)$ (modular flow)')
    ax.plot(tau, dCf, 'r-', linewidth=1.2, label=r'$\delta C_{\rm full}(\tau)$ (Hamiltonian)')
    ax.set_xlabel(r'$\tau$')
    ax.set_ylabel(r'$\delta C(\tau)$')
    ax.set_title('Time domain: modular vs physical evolution')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # Panel 2: Time domain (zoom to see delta_C_full)
    ax = axes[0, 1]
    ax.plot(tau, dCf, 'r-', linewidth=1.2, label=r'$\delta C_{\rm full}(\tau)$ (physical)')
    ax.set_xlabel(r'$\tau$')
    ax.set_ylabel(r'$\delta C_{\rm full}(\tau)$')
    ax.set_title(r'Physical response: $\mu_k^2 \cos(\omega_m \tau)$')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # Panel 3: FFT comparison
    ax = axes[1, 0]
    freqs_l, fft_l = fft_with_freq(dCl, tau)
    freqs_f, fft_f = fft_with_freq(dCf, tau)

    omega_m = 0.786867  # for N=100, mode 25
    mask = freqs_l < 8.0
    ax.semilogy(freqs_l[mask], fft_l[mask], 'b-', linewidth=0.8, alpha=0.8, label=r'$\delta C_{\rm local}$ FFT')
    ax.semilogy(freqs_f[mask], fft_f[mask], 'r-', linewidth=1.2, alpha=0.8, label=r'$\delta C_{\rm full}$ FFT')
    ax.axvline(omega_m, color='green', linestyle='--', linewidth=1.5, alpha=0.7, label=f'$\\omega_m = {omega_m:.3f}$')

    # Mark some modular frequencies
    for i in range(min(5, len(eps_sq))):
        mod_freq = eps_sq[i] / (2 * np.pi)
        if mod_freq < 8.0:
            ax.axvline(mod_freq, color='gray', linestyle=':', linewidth=0.8, alpha=0.5)
            if i == 0:
                ax.axvline(mod_freq, color='gray', linestyle=':', linewidth=0.8, alpha=0.5, label='modular freqs $\\epsilon_k/(2\\pi)$')

    ax.set_xlabel(r'$\omega$ (angular frequency)')
    ax.set_ylabel('FFT amplitude')
    ax.set_title('FFT spectra: modular flow peaks at WRONG frequencies')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Panel 4: Modular energy shift
    ax = axes[1, 1]
    eps_vac = np.array(data['eps_vac'])
    ax.plot(range(len(eps_vac)), eps_vac, 'ko-', markersize=4, label='vacuum $\\epsilon_k$')
    ax.plot(range(len(eps_sq)), eps_sq, 'rs-', markersize=3, label='squeezed $\\epsilon_k$')
    ax.set_xlabel('Mode index k')
    ax.set_ylabel('Modular energy $\\epsilon_k$')
    ax.set_title('Modular energy spectrum: vacuum vs squeezed')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 40)

    plt.tight_layout()
    plt.savefig('fft_comparison_N100.png', dpi=150, bbox_inches='tight')
    print("Saved fft_comparison_N100.png")

    # ---- Figure 2: Convergence across N ----
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Squeezed State Test: Convergence Across Lattice Sizes', fontsize=14)

    for idx, N in enumerate([50, 100, 200]):
        data = load_data(N)
        tau = np.array(data['tau_array'])
        dCl = np.array(data['delta_C_local'])
        dCf = np.array(data['delta_C_full'])

        ax = axes[idx]
        ax.plot(tau[:300], dCl[:300], 'b-', linewidth=0.8, label=r'$\delta C_{\rm local}$')
        # Scale delta_C_full to be visible
        scale = max(np.max(np.abs(dCl[:300])), 1e-10) / max(np.max(np.abs(dCf[:300])), 1e-10)
        ax.plot(tau[:300], dCf[:300] * scale, 'r-', linewidth=1.0, alpha=0.7,
                label=f'$\\delta C_{{\\rm full}} \\times {scale:.0f}$')

        omega_m_val = np.array(data['eps_sq'])[0] / (2 * np.pi)  # not omega_m, just for labeling
        ax.set_xlabel(r'$\tau$')
        ax.set_ylabel(r'$\delta C(\tau)$')
        ax.set_title(f'N = {N} (mode = {N//4})')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('convergence_time_domain.png', dpi=150, bbox_inches='tight')
    print("Saved convergence_time_domain.png")

    # ---- Figure 3: FFT comparison across N ----
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('FFT Spectra: Squeezed State Modular Flow vs Physical Evolution', fontsize=14)

    omega_m_vals = {50: 0.779572, 100: 0.786867, 200: 0.776184}

    for idx, N in enumerate([50, 100, 200]):
        data = load_data(N)
        tau = np.array(data['tau_array'])
        dCl = np.array(data['delta_C_local'])
        dCf = np.array(data['delta_C_full'])

        freqs_l, fft_l = fft_with_freq(dCl, tau)
        freqs_f, fft_f = fft_with_freq(dCf, tau)

        ax = axes[idx]
        mask = freqs_l < 8.0
        ax.semilogy(freqs_l[mask], fft_l[mask], 'b-', linewidth=0.8, alpha=0.8, label='modular flow')
        ax.semilogy(freqs_f[mask], fft_f[mask], 'r-', linewidth=1.2, alpha=0.8, label='physical')
        ax.axvline(omega_m_vals[N], color='green', linestyle='--', linewidth=1.5, alpha=0.7,
                   label=f'$\\omega_m$={omega_m_vals[N]:.3f}')

        ax.set_xlabel(r'$\omega$')
        ax.set_ylabel('FFT amplitude')
        ax.set_title(f'N = {N}')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('fft_comparison_all_N.png', dpi=150, bbox_inches='tight')
    print("Saved fft_comparison_all_N.png")

    # ---- Figure 4: Squeezing parameter sweep ----
    with open('results_summary.json', 'r') as f:
        summary = json.load(f)

    r_vals = []
    disc_vals = []
    for key in sorted(summary['part_d'].keys()):
        r_vals.append(summary['part_d'][key]['r'])
        disc_vals.append(summary['part_d'][key]['discrepancy'])

    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    ax.plot(r_vals, disc_vals, 'bo-', markersize=8, linewidth=2)
    ax.set_xlabel('Squeezing parameter r', fontsize=12)
    ax.set_ylabel(r'$\|\delta C_{\rm local} - \delta C_{\rm full}\| / \|\delta C_{\rm full}\|$', fontsize=12)
    ax.set_title('Discrepancy vs Squeezing Parameter (N=100, mode=25)', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(bottom=0)
    plt.tight_layout()
    plt.savefig('squeeze_sweep.png', dpi=150, bbox_inches='tight')
    print("Saved squeeze_sweep.png")

    print("\nAll plots saved successfully.")

else:
    # Text-based summary
    print("\n=== TEXT SUMMARY (no matplotlib) ===")
    with open('results_summary.json', 'r') as f:
        summary = json.load(f)

    print("\nPart B key result: delta_C_local oscillates at modular frequencies,")
    print("NOT at physical frequency omega_m. Discrepancy > 15x for all N.")

    for N_str in ['50', '100', '200']:
        if N_str in summary.get('part_b', {}):
            r = summary['part_b'][N_str]
            print(f"\n  N={N_str}: disc={r['discrepancy']:.2f}, "
                  f"top peaks (local): {[f'{p[0]:.3f}' for p in r['peaks_local'][:3]]}")
