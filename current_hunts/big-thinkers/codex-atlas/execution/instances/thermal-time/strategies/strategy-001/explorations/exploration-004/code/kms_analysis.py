"""
Exploration 004 — KMS Temperature Analysis

For each correlator (C_full and C_local), compute:
1. The spectral decomposition S(ω) = Σ w_{mn} δ(ω - ω_{mn})
2. The detailed balance ratio S(ω)/S(-ω) at each spectral peak
3. The effective KMS temperature β_KMS from the ratio
4. A comparison of spectral structure (# of peaks, frequencies)

Key insight: Both C_full and C_local should satisfy KMS at β=2 w.r.t. their
own dynamics. The difference is in the SPECTRAL CONTENT (2 peaks vs 1 peak).

Physics:
  C_full(τ)  = Tr[ρ_AB · e^{iH_AB τ} x_A e^{-iH_AB τ} · x_A]  (QM)
  C_local(τ) = Tr[ρ_A · e^{i(K_A/β)τ} x_A e^{-i(K_A/β)τ} · x_A]  (TTH)

The Fourier transform convention:
  G̃(ω) = ∫ G(τ) e^{iωτ} dτ

KMS at inverse temperature β:  G̃(ω)/G̃(-ω) = e^{βω}
"""

import numpy as np
from scipy.linalg import expm
from numpy.linalg import eigh, norm
import json

# ============================================================
# Parameters (same as exploration-003)
# ============================================================
N = 20
omega_A = 1.0
omega_B = 1.0
beta = 2.0
lambda_vals = [0.1, 0.3, 0.5]

# Single-mode operators
n_op = np.diag(np.arange(N, dtype=float))
a_op = np.diag(np.sqrt(np.arange(1, N, dtype=float)), 1)
ad_op = a_op.T
q_op = (a_op + ad_op) / np.sqrt(2)
I_N = np.eye(N)

# Two-mode operators
H_A_2mode = np.kron(omega_A * n_op, I_N)
H_B_2mode = np.kron(I_N, omega_B * n_op)
H_int_base = np.kron(q_op, q_op)
x_A_2mode = np.kron(q_op, I_N)
x_A_1mode = q_op

def partial_trace_B(rho_AB, N):
    rho_A = np.zeros((N, N), dtype=complex)
    for k in range(N):
        rho_A += rho_AB[k::N, k::N]
    return rho_A

def compute_K_A(rho_AB, N):
    rho_A = partial_trace_B(rho_AB, N)
    rho_A = (rho_A + rho_A.conj().T) / 2
    evals_A, evecs_A = eigh(rho_A)
    evals_A_clipped = np.maximum(evals_A, 1e-300)
    log_evals = -np.log(evals_A_clipped)
    K_A = evecs_A @ np.diag(log_evals) @ evecs_A.T
    K_A = K_A.real
    return K_A, rho_A

# ============================================================
# Spectral decomposition of a correlator
# G(τ) = Σ_{m,n} p_m |x_{mn}|² e^{i(E_m - E_n)τ}
# G̃(ω) has spectral weight at ω = E_n - E_m (note sign!)
# Weight at ω_{nm} = E_n - E_m is w_{mn} = p_m |x_{mn}|²
# ============================================================
def spectral_decomposition(H_mat, rho_mat, x_op, freq_threshold=1e-10, weight_threshold=1e-15):
    """
    Compute spectral decomposition of G(τ) = Tr[ρ x(τ) x].

    Returns:
      freqs: array of distinct frequencies ω = E_n - E_m
      weights: corresponding spectral weights (positive/negative freq separate)
      pairs: list of (E_m, E_n, p_m, |x_mn|², ω_{nm})
    """
    evals, evecs = eigh(H_mat)

    # Transform to eigenbasis
    rho_eig = evecs.conj().T @ rho_mat @ evecs
    x_eig = evecs.conj().T @ x_op @ evecs

    # Diagonal of rho gives probabilities
    p = np.diag(rho_eig).real

    # Collect spectral data
    D = len(evals)
    pairs = []
    for m in range(D):
        for n in range(D):
            w = p[m] * abs(x_eig[m, n])**2
            if w < weight_threshold:
                continue
            omega_nm = evals[n] - evals[m]  # frequency in G̃
            pairs.append({
                'E_m': evals[m],
                'E_n': evals[n],
                'p_m': p[m],
                'x_mn_sq': abs(x_eig[m, n])**2,
                'weight': w,
                'freq': omega_nm,  # E_n - E_m
            })

    return pairs

def bin_spectral_weights(pairs, freq_resolution=0.01):
    """
    Bin spectral pairs by frequency and return
    positive/negative frequency bins with total weights.
    """
    if not pairs:
        return {}, {}

    freqs = np.array([p['freq'] for p in pairs])
    weights = np.array([p['weight'] for p in pairs])

    # Round frequencies to bins
    binned_pos = {}  # freq > 0
    binned_neg = {}  # freq < 0 (store as |freq|)

    for f, w in zip(freqs, weights):
        f_rounded = round(f / freq_resolution) * freq_resolution
        if abs(f_rounded) < freq_resolution / 2:
            continue  # Skip zero frequency
        if f_rounded > 0:
            binned_pos[f_rounded] = binned_pos.get(f_rounded, 0) + w
        else:
            binned_neg[-f_rounded] = binned_neg.get(-f_rounded, 0) + w

    return binned_pos, binned_neg

def check_kms(pairs, beta_expected, freq_resolution=0.01):
    """
    Check the KMS condition: G̃(ω)/G̃(-ω) = e^{β_KMS ω}.

    For each frequency ω > 0 present in the spectrum:
    - Compute S(+ω) and S(-ω)
    - Extract β_KMS = ln(S(ω)/S(-ω)) / ω

    Returns a dict of {freq: β_KMS} pairs.
    """
    binned_pos, binned_neg = bin_spectral_weights(pairs, freq_resolution)

    results = {}
    for freq in sorted(binned_pos.keys()):
        w_pos = binned_pos.get(freq, 0)
        w_neg = binned_neg.get(freq, 0)

        if w_neg > 1e-20 and w_pos > 1e-20:
            ratio = w_pos / w_neg
            beta_kms = np.log(ratio) / freq
            results[freq] = {
                'freq': freq,
                'S_pos': w_pos,
                'S_neg': w_neg,
                'ratio': ratio,
                'beta_KMS': beta_kms,
                'delta_beta': beta_kms - beta_expected,
            }

    return results

# ============================================================
# Main analysis
# ============================================================
print("=" * 80)
print("KMS TEMPERATURE ANALYSIS")
print(f"N={N}, β={beta}, ω_A={omega_A}, ω_B={omega_B}")
print("=" * 80)

all_results = {}

for lam in lambda_vals:
    print(f"\n{'='*60}")
    print(f"λ = {lam}")
    print(f"{'='*60}")

    # Build Hamiltonian and thermal state
    H_AB = H_A_2mode + H_B_2mode + lam * H_int_base
    rho_AB = expm(-beta * H_AB)
    Z = np.trace(rho_AB).real
    rho_AB /= Z

    # Local modular Hamiltonian
    K_A, rho_A = compute_K_A(rho_AB, N)

    # Normal mode frequencies
    omega_plus = np.sqrt(omega_A**2 + lam)
    omega_minus = np.sqrt(omega_A**2 - lam)

    print(f"\nNormal modes: ω_+ = {omega_plus:.4f}, ω_- = {omega_minus:.4f}")

    # --------------------------------------------------------
    # Analysis 1: C_full spectral decomposition (QM)
    # H = H_AB, ρ = ρ_AB, x = x_A ⊗ I_B
    # --------------------------------------------------------
    print("\n--- C_full (QM: ρ_AB, H_AB) ---")
    pairs_full = spectral_decomposition(H_AB, rho_AB, x_A_2mode)

    # Dominant spectral peaks
    bp_full, bn_full = bin_spectral_weights(pairs_full, freq_resolution=0.005)
    print(f"  Positive freq peaks: {len(bp_full)}")
    top_pos = sorted(bp_full.items(), key=lambda x: -x[1])[:5]
    print(f"  Top 5 positive freqs (ω, weight):")
    for f, w in top_pos:
        print(f"    ω = {f:8.4f},  weight = {w:.6e}")

    top_neg = sorted(bn_full.items(), key=lambda x: -x[1])[:5]
    print(f"  Top 5 negative freqs (|ω|, weight):")
    for f, w in top_neg:
        print(f"    |ω| = {f:8.4f},  weight = {w:.6e}")

    # KMS check
    kms_full = check_kms(pairs_full, beta, freq_resolution=0.005)
    print(f"\n  KMS check (should give β_KMS = {beta:.1f}):")
    for freq in sorted(kms_full.keys()):
        r = kms_full[freq]
        if r['S_pos'] > 1e-8:  # only show significant peaks
            print(f"    ω = {freq:8.4f}: β_KMS = {r['beta_KMS']:.6f} "
                  f"(Δβ = {r['delta_beta']:.2e}), "
                  f"S(+ω)/S(-ω) = {r['ratio']:.4f}, "
                  f"expected = {np.exp(beta*freq):.4f}")

    # --------------------------------------------------------
    # Analysis 2: C_local spectral decomposition (TTH)
    # H_eff = K_A/β, ρ = ρ_A, x = x_A (single mode)
    # --------------------------------------------------------
    print(f"\n--- C_local (TTH: ρ_A, K_A/β) ---")
    H_eff = K_A / beta
    pairs_local = spectral_decomposition(H_eff, rho_A, x_A_1mode)

    bp_local, bn_local = bin_spectral_weights(pairs_local, freq_resolution=0.005)
    print(f"  Positive freq peaks: {len(bp_local)}")
    top_pos_l = sorted(bp_local.items(), key=lambda x: -x[1])[:5]
    print(f"  Top 5 positive freqs (ω, weight):")
    for f, w in top_pos_l:
        print(f"    ω = {f:8.4f},  weight = {w:.6e}")

    top_neg_l = sorted(bn_local.items(), key=lambda x: -x[1])[:5]
    print(f"  Top 5 negative freqs (|ω|, weight):")
    for f, w in top_neg_l:
        print(f"    |ω| = {f:8.4f},  weight = {w:.6e}")

    # KMS check
    kms_local = check_kms(pairs_local, beta, freq_resolution=0.005)
    print(f"\n  KMS check (should give β_KMS = {beta:.1f}):")
    for freq in sorted(kms_local.keys()):
        r = kms_local[freq]
        if r['S_pos'] > 1e-8:
            print(f"    ω = {freq:8.4f}: β_KMS = {r['beta_KMS']:.6f} "
                  f"(Δβ = {r['delta_beta']:.2e}), "
                  f"S(+ω)/S(-ω) = {r['ratio']:.4f}, "
                  f"expected = {np.exp(beta*freq):.4f}")

    # --------------------------------------------------------
    # Analysis 3: "Naive" temperature — what if we fit C_full
    # to a single-frequency model?
    # --------------------------------------------------------
    print(f"\n--- Cross-comparison ---")

    # For each dominant positive frequency in C_full, what's the KMS temperature?
    # All should give β=2 (since the global state is Gibbs at β=2)

    # More interesting: get the frequency centroid of C_full
    total_weight_pos = sum(bp_full.values())
    freq_centroid_full = sum(f * w for f, w in bp_full.items()) / total_weight_pos if total_weight_pos > 0 else 0

    total_weight_pos_local = sum(bp_local.values())
    freq_centroid_local = sum(f * w for f, w in bp_local.items()) / total_weight_pos_local if total_weight_pos_local > 0 else 0

    # Number of significant peaks (> 1% of max weight)
    max_weight_full = max(bp_full.values()) if bp_full else 0
    sig_peaks_full = sum(1 for w in bp_full.values() if w > 0.01 * max_weight_full)

    max_weight_local = max(bp_local.values()) if bp_local else 0
    sig_peaks_local = sum(1 for w in bp_local.values() if w > 0.01 * max_weight_local)

    print(f"  C_full:  {sig_peaks_full} significant spectral peaks, centroid ω = {freq_centroid_full:.4f}")
    print(f"  C_local: {sig_peaks_local} significant spectral peak(s), centroid ω = {freq_centroid_local:.4f}")
    print(f"  Normal modes: ω_+ = {omega_plus:.4f}, ω_- = {omega_minus:.4f}")
    print(f"  Frequency shift: centroid_local - centroid_full = {freq_centroid_local - freq_centroid_full:.4f}")

    # Store results
    all_results[str(lam)] = {
        'lambda': lam,
        'omega_plus': float(omega_plus),
        'omega_minus': float(omega_minus),
        'sig_peaks_full': sig_peaks_full,
        'sig_peaks_local': sig_peaks_local,
        'freq_centroid_full': float(freq_centroid_full),
        'freq_centroid_local': float(freq_centroid_local),
        'kms_full': {str(k): v for k, v in kms_full.items()},
        'kms_local': {str(k): v for k, v in kms_local.items()},
    }

# ============================================================
# Summary table
# ============================================================
print(f"\n{'='*80}")
print("SUMMARY TABLE")
print(f"{'='*80}")
print(f"{'λ':>6} {'peaks_QM':>10} {'peaks_TTH':>10} {'ω_cent_QM':>12} {'ω_cent_TTH':>12} {'β_KMS_QM':>10} {'β_KMS_TTH':>10}")
print("-" * 80)

for lam in lambda_vals:
    r = all_results[str(lam)]
    # Get the β_KMS from the dominant peak for each
    kms_f = r['kms_full']
    kms_l = r['kms_local']

    # Dominant positive freq β_KMS
    if kms_f:
        dom_full = max(kms_f.values(), key=lambda x: x['S_pos'])
        beta_qm = dom_full['beta_KMS']
    else:
        beta_qm = float('nan')

    if kms_l:
        dom_local = max(kms_l.values(), key=lambda x: x['S_pos'])
        beta_tth = dom_local['beta_KMS']
    else:
        beta_tth = float('nan')

    print(f"{lam:6.1f} {r['sig_peaks_full']:10d} {r['sig_peaks_local']:10d} "
          f"{r['freq_centroid_full']:12.4f} {r['freq_centroid_local']:12.4f} "
          f"{beta_qm:10.4f} {beta_tth:10.4f}")

print(f"\nExpected β_KMS = {beta:.1f} for both (since both use their own consistent state+dynamics)")
print("\nThe PHYSICAL difference is in the spectral structure:")
print("  QM:  Two peaks at ω_± (normal mode splitting) → beating in time domain")
print("  TTH: One peak at ω_eff (local modular frequency) → single oscillation")

# Save results
save_path = "/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/thermal-time/strategies/strategy-001/explorations/exploration-004/code/"
with open(save_path + "kms_results.json", "w") as f:
    json.dump(all_results, f, indent=2, default=str)

print(f"\nResults saved to {save_path}kms_results.json")
print("DONE")
