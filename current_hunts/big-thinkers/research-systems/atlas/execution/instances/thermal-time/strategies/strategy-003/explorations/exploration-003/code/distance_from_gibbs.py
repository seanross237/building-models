#!/usr/bin/env python3
"""
Exploration 003: Distance-from-Gibbs Characterization

Systematically map TTH discrepancy vs. relative entropy for two families:
  Family 1: Squeezed states S(r) rho_Gibbs S(r)†, r in [0, 1.0]
  Family 2: Post-quench states rho(delta_lambda), delta_lambda in [0, 0.5]

System: Two coupled harmonic oscillators
  H_AB = omega*(n_A + n_B) + lambda * q_A * q_B
  lambda = 0.3, beta = 2.0, omega = 1.0, N = 20 (Fock truncation)
"""

import numpy as np
from scipy.linalg import expm, logm
from numpy.linalg import eigh, norm
import json
import time
import sys

# ============================================================
# Parameters
# ============================================================
N = 20          # Fock truncation per mode
omega = 1.0
beta = 2.0
lam = 0.3       # coupling
N_tau = 2000
tau_max = 16 * np.pi
tau_arr = np.linspace(0, tau_max, N_tau)

omega_plus  = np.sqrt(omega**2 + lam)   # ~ 1.1402
omega_minus = np.sqrt(omega**2 - lam)   # ~ 0.8367

print("=" * 70)
print("Exploration 003: Distance-from-Gibbs Characterization")
print(f"N={N}, beta={beta}, omega={omega}, lambda={lam}")
print(f"Normal modes: omega_+ = {omega_plus:.6f}, omega_- = {omega_minus:.6f}")
print(f"tau in [0, {tau_max:.2f}], {N_tau} points")
print("=" * 70)

# ============================================================
# Build single-mode operators (N x N)
# ============================================================
n_op  = np.diag(np.arange(N, dtype=float))
a_op  = np.diag(np.sqrt(np.arange(1, N, dtype=float)), 1)
ad_op = a_op.T
q_op  = (a_op + ad_op) / np.sqrt(2)
I_N   = np.eye(N)

# Two-mode operators (N^2 x N^2)
H_A_2mode    = np.kron(omega * n_op, I_N)
H_B_2mode    = np.kron(I_N, omega * n_op)
H_int_base   = np.kron(q_op, q_op)
H_uncoupled  = H_A_2mode + H_B_2mode
H_coupled    = H_uncoupled + lam * H_int_base
x_A_2mode    = np.kron(q_op, I_N)

dim = N**2
print(f"Hilbert space dimension: {dim}")

# ============================================================
# Reference Gibbs state
# ============================================================
rho_gibbs = expm(-beta * H_coupled)
Z_gibbs = np.trace(rho_gibbs).real
rho_gibbs /= Z_gibbs
print(f"Gibbs state: Z = {Z_gibbs:.6f}, Tr(rho) = {np.trace(rho_gibbs).real:.15f}")

evals_gibbs = np.linalg.eigvalsh(rho_gibbs)
print(f"  min eigenvalue = {evals_gibbs[0]:.2e}, max = {evals_gibbs[-1]:.6f}")

# log(rho_gibbs) for relative entropy computation
evals_g, evecs_g = eigh(rho_gibbs)
log_rho_gibbs = evecs_g @ np.diag(np.log(np.maximum(evals_g, 1e-300))) @ evecs_g.T
log_rho_gibbs = (log_rho_gibbs + log_rho_gibbs.T) / 2  # symmetrize

# ============================================================
# Helper functions
# ============================================================

def compute_relative_entropy(rho, log_rho_ref):
    """S(rho || sigma) = Tr[rho (log rho - log sigma)]"""
    evals_r, evecs_r = eigh(rho)
    # Remove near-zero eigenvalues
    mask = evals_r > 1e-300
    log_rho = evecs_r @ np.diag(np.where(mask, np.log(np.maximum(evals_r, 1e-300)), 0.0)) @ evecs_r.T
    log_rho = (log_rho + log_rho.T) / 2

    S_rel = np.trace(rho @ (log_rho - log_rho_ref)).real
    return max(S_rel, 0.0)  # Should be non-negative


def compute_modular_hamiltonian(rho):
    """K = -log(rho)"""
    evals_r, evecs_r = eigh(rho)
    log_evals = -np.log(np.maximum(evals_r, 1e-300))
    K = (evecs_r @ np.diag(log_evals) @ evecs_r.T).real
    return K


def compute_correlator(H_mat, rho_mat, x_op, tau_arr):
    """
    C(tau) = Tr[rho * e^{iH tau} x e^{-iH tau} * x]
    Spectral decomposition method.
    """
    evals, evecs = eigh(H_mat)
    rho_eig = evecs.conj().T @ rho_mat @ evecs
    x_eig   = evecs.conj().T @ x_op   @ evecs

    xrho = x_eig @ rho_eig
    B = x_eig * xrho.T

    conj_phase = np.exp(-1j * np.outer(tau_arr, evals))
    phase      = conj_phase.conj()

    inner = B @ conj_phase.T
    C = np.sum(phase * inner.T, axis=1).real
    return C


def fft_classify(C_qm, C_tth, tau_arr, omega_plus, omega_minus, tol=0.08):
    """
    FFT both correlators and classify:
    - QUANTITATIVE: C_tth has peaks at omega_+/- (correct frequencies)
    - STRUCTURAL: C_tth has peaks at wrong frequencies

    Returns: classification, peak_freqs_qm, peak_freqs_tth, fft details
    """
    dt = tau_arr[1] - tau_arr[0]
    N_pad = len(tau_arr) * 4  # zero-pad for resolution
    freq_axis = np.fft.rfftfreq(N_pad, d=dt) * 2 * np.pi

    fft_qm  = np.abs(np.fft.rfft(C_qm - C_qm.mean(), n=N_pad))
    fft_tth = np.abs(np.fft.rfft(C_tth - C_tth.mean(), n=N_pad))

    def find_peaks(fft_data, freq_axis, threshold_frac=0.05, n_peaks=8):
        threshold = threshold_frac * fft_data.max()
        peaks = []
        for i in range(1, len(fft_data)-1):
            if (fft_data[i] > threshold and
                fft_data[i] > fft_data[i-1] and
                fft_data[i] > fft_data[i+1]):
                peaks.append((freq_axis[i], fft_data[i]))
        peaks.sort(key=lambda x: -x[1])
        return peaks[:n_peaks]

    peaks_qm  = find_peaks(fft_qm, freq_axis)
    peaks_tth = find_peaks(fft_tth, freq_axis)

    # Check if TTH peaks match normal mode frequencies
    expected_freqs = [omega_plus, omega_minus]
    tth_peak_freqs = [p[0] for p in peaks_tth[:4]]  # top 4 peaks

    matched = 0
    for exp_f in expected_freqs:
        for peak_f in tth_peak_freqs:
            if abs(peak_f - exp_f) < tol:
                matched += 1
                break

    # If both normal mode frequencies are matched in TTH peaks -> QUANTITATIVE
    if matched == 2:
        classification = "QUANTITATIVE"
    elif matched == 1:
        classification = "MIXED"
    else:
        classification = "STRUCTURAL"

    return classification, peaks_qm, peaks_tth


def compute_beta_eff(K, rho, H_coupled, beta):
    """
    Estimate effective inverse temperature.
    For Gibbs: K = beta*H + const, so beta_eff = beta.
    For non-Gibbs: fit K ~ beta_eff * H + const using Tr[K*H]/Tr[H^2].
    """
    K_centered = K - np.trace(K @ rho).real * np.eye(K.shape[0])
    H_centered = H_coupled - np.trace(H_coupled @ rho).real * np.eye(K.shape[0])

    # beta_eff = Tr[rho K H] / Tr[rho H^2] approximately
    num = np.trace(K @ H_coupled).real
    den = np.trace(H_coupled @ H_coupled).real
    if den > 0:
        return num / den
    return beta


# ============================================================
# CONTROL CHECK: Gibbs state (r=0 / delta_lambda=0)
# ============================================================
print(f"\n{'='*70}")
print("CONTROL CHECK: Gibbs state")
print(f"{'='*70}")

K_gibbs = compute_modular_hamiltonian(rho_gibbs)
S_rel_gibbs = compute_relative_entropy(rho_gibbs, log_rho_gibbs)

C_QM_gibbs = compute_correlator(H_coupled, rho_gibbs, x_A_2mode, tau_arr)
C_TTH_gibbs = compute_correlator(K_gibbs / beta, rho_gibbs, x_A_2mode, tau_arr)

disc_gibbs = norm(C_QM_gibbs - C_TTH_gibbs) / norm(C_QM_gibbs)

print(f"S(rho_gibbs || rho_gibbs) = {S_rel_gibbs:.2e}  (should be ~0)")
print(f"||C_QM - C_TTH|| / ||C_QM|| = {disc_gibbs:.2e}  (should be ~0)")
print(f"CONTROL: {'PASS' if disc_gibbs < 1e-8 else 'FAIL'}")

control_results = {
    "S_rel": float(S_rel_gibbs),
    "discrepancy": float(disc_gibbs),
    "passed": bool(disc_gibbs < 1e-8)
}

# ============================================================
# FAMILY 1: SQUEEZED STATES
# ============================================================
print(f"\n{'='*70}")
print("FAMILY 1: SQUEEZED STATES")
print(f"S(r) rho_Gibbs S(r)†, two-mode squeezing")
print(f"{'='*70}")

# Two-mode squeezing operator: S(r) = exp[r(a_A a_B - a_A† a_B†)]
# Generator: a_A tensor a_B - a_A† tensor a_B†
gen_two_mode = np.kron(a_op, a_op) - np.kron(ad_op, ad_op)

r_values = np.arange(0, 1.05, 0.1)  # 0.0, 0.1, ..., 1.0
squeezed_results = []

for r_sq in r_values:
    t0 = time.time()
    print(f"\n  r = {r_sq:.1f} ...", end=" ", flush=True)

    if r_sq == 0.0:
        rho_sq = rho_gibbs.copy()
    else:
        S_r = expm(r_sq * gen_two_mode)
        rho_sq = S_r @ rho_gibbs @ S_r.conj().T
        # Symmetrize and normalize
        rho_sq = (rho_sq + rho_sq.conj().T) / 2
        rho_sq /= np.trace(rho_sq).real

    # Check positivity
    evals_sq = np.linalg.eigvalsh(rho_sq)
    min_eval = evals_sq[0]

    # Relative entropy
    S_rel = compute_relative_entropy(rho_sq, log_rho_gibbs)

    # Modular Hamiltonian
    K_sq = compute_modular_hamiltonian(rho_sq)

    # Effective beta: for TTH, we evolve under K/beta_eff
    # For the squeezed Gibbs state: K_sq = S K_gibbs S†
    # The natural beta_eff is still beta (from the original Gibbs state)
    beta_eff = beta

    # Correlators
    C_QM = compute_correlator(H_coupled, rho_sq, x_A_2mode, tau_arr)
    C_TTH = compute_correlator(K_sq / beta_eff, rho_sq, x_A_2mode, tau_arr)

    # Discrepancy
    disc = norm(C_QM - C_TTH) / norm(C_QM)
    max_diff = np.max(np.abs(C_QM - C_TTH))

    # FFT classification
    classification, peaks_qm, peaks_tth = fft_classify(
        C_QM, C_TTH, tau_arr, omega_plus, omega_minus
    )

    elapsed = time.time() - t0
    print(f"S_rel={S_rel:.4f}, disc={disc:.4f} ({disc*100:.1f}%), "
          f"class={classification}, min_eval={min_eval:.2e}, t={elapsed:.1f}s")

    squeezed_results.append({
        "family": "squeezed",
        "parameter": float(r_sq),
        "param_name": "r",
        "S_rel": float(S_rel),
        "discrepancy": float(disc),
        "max_diff": float(max_diff),
        "classification": classification,
        "min_eigenvalue": float(min_eval),
        "beta_eff": float(beta_eff),
        "peaks_qm": [(float(f), float(a)) for f, a in peaks_qm[:6]],
        "peaks_tth": [(float(f), float(a)) for f, a in peaks_tth[:6]],
    })

# Print summary table
print(f"\n{'='*70}")
print("SQUEEZED STATE SUMMARY")
print(f"{'='*70}")
print(f"{'r':>5} | {'S_rel':>10} | {'disc':>10} | {'disc%':>8} | {'class':>14} | {'min_eval':>10}")
print("-" * 75)
for r in squeezed_results:
    print(f"{r['parameter']:5.1f} | {r['S_rel']:10.4f} | {r['discrepancy']:10.6f} | "
          f"{r['discrepancy']*100:7.1f}% | {r['classification']:>14} | {r['min_eigenvalue']:10.2e}")


# ============================================================
# FAMILY 2: POST-QUENCH STATES
# ============================================================
print(f"\n{'='*70}")
print("FAMILY 2: POST-QUENCH STATES")
print(f"rho(delta_lam) = exp(-beta H(lam - delta_lam))/Z, dynamics under H(lam)")
print(f"{'='*70}")

dlam_values = np.arange(0, 0.525, 0.05)  # 0.0, 0.05, ..., 0.5
quench_results = []

for dlam in dlam_values:
    t0 = time.time()
    print(f"\n  delta_lambda = {dlam:.2f} ...", end=" ", flush=True)

    lam_state = lam - dlam  # coupling for the state preparation

    if abs(dlam) < 1e-10:
        # delta_lambda = 0: state IS the Gibbs state of H(lambda)
        rho_q = rho_gibbs.copy()
    else:
        H_state = H_uncoupled + lam_state * H_int_base
        rho_q = expm(-beta * H_state)
        rho_q /= np.trace(rho_q).real

    # Symmetrize
    rho_q = (rho_q + rho_q.conj().T) / 2
    rho_q /= np.trace(rho_q).real

    # Check positivity
    evals_q = np.linalg.eigvalsh(rho_q)
    min_eval = evals_q[0]

    # Relative entropy S(rho_q || rho_gibbs)
    S_rel = compute_relative_entropy(rho_q, log_rho_gibbs)

    # Modular Hamiltonian of the quench state
    K_q = compute_modular_hamiltonian(rho_q)

    # For the quench state: K_q = beta * H(lam - dlam) + const
    # beta_eff is the beta of the state (which is beta, since we constructed it at temperature beta)
    beta_eff = beta

    # Correlators
    # C_QM: dynamics under H(lambda) (the actual Hamiltonian)
    C_QM = compute_correlator(H_coupled, rho_q, x_A_2mode, tau_arr)
    # C_TTH: modular flow under K_q / beta_eff
    C_TTH = compute_correlator(K_q / beta_eff, rho_q, x_A_2mode, tau_arr)

    # Discrepancy
    disc = norm(C_QM - C_TTH) / norm(C_QM)
    max_diff = np.max(np.abs(C_QM - C_TTH))

    # FFT classification
    classification, peaks_qm, peaks_tth = fft_classify(
        C_QM, C_TTH, tau_arr, omega_plus, omega_minus
    )

    # Also compute what frequencies the TTH SHOULD have
    # K_q = beta * H(lam - dlam), so modular flow under H(lam - dlam)
    # Normal modes of H(lam - dlam): omega_pm_state = sqrt(omega^2 +/- (lam - dlam))
    lam_eff = lam - dlam
    if omega**2 + lam_eff > 0:
        omega_plus_state = np.sqrt(omega**2 + lam_eff)
    else:
        omega_plus_state = 0.0
    if omega**2 - lam_eff > 0:
        omega_minus_state = np.sqrt(omega**2 - lam_eff)
    else:
        omega_minus_state = 0.0

    elapsed = time.time() - t0
    print(f"S_rel={S_rel:.4f}, disc={disc:.4f} ({disc*100:.1f}%), "
          f"class={classification}, min_eval={min_eval:.2e}, t={elapsed:.1f}s")

    quench_results.append({
        "family": "quench",
        "parameter": float(dlam),
        "param_name": "delta_lambda",
        "S_rel": float(S_rel),
        "discrepancy": float(disc),
        "max_diff": float(max_diff),
        "classification": classification,
        "min_eigenvalue": float(min_eval),
        "beta_eff": float(beta_eff),
        "lam_state": float(lam_state),
        "omega_plus_state": float(omega_plus_state),
        "omega_minus_state": float(omega_minus_state),
        "peaks_qm": [(float(f), float(a)) for f, a in peaks_qm[:6]],
        "peaks_tth": [(float(f), float(a)) for f, a in peaks_tth[:6]],
    })

# Print summary table
print(f"\n{'='*70}")
print("POST-QUENCH STATE SUMMARY")
print(f"{'='*70}")
print(f"{'dlam':>6} | {'lam_eff':>8} | {'S_rel':>10} | {'disc':>10} | {'disc%':>8} | {'class':>14} | {'omega+_s':>8} | {'omega-_s':>8}")
print("-" * 100)
for r in quench_results:
    print(f"{r['parameter']:6.2f} | {r['lam_state']:8.3f} | {r['S_rel']:10.4f} | "
          f"{r['discrepancy']:10.6f} | {r['discrepancy']*100:7.1f}% | "
          f"{r['classification']:>14} | {r['omega_plus_state']:8.4f} | {r['omega_minus_state']:8.4f}")


# ============================================================
# COMBINED ANALYSIS
# ============================================================
print(f"\n{'='*70}")
print("COMBINED ANALYSIS")
print(f"{'='*70}")

all_results = squeezed_results + quench_results

# Sort by relative entropy
all_sorted = sorted(all_results, key=lambda x: x['S_rel'])

print(f"\n{'Family':>10} | {'Param':>8} | {'S_rel':>10} | {'disc%':>8} | {'Classification':>14}")
print("-" * 65)
for r in all_sorted:
    pname = f"r={r['parameter']:.1f}" if r['family'] == 'squeezed' else f"dl={r['parameter']:.2f}"
    print(f"{r['family']:>10} | {pname:>8} | {r['S_rel']:10.4f} | "
          f"{r['discrepancy']*100:7.1f}% | {r['classification']:>14}")

# Check for transition
print(f"\n--- Transition Analysis ---")
for family_name, family_data in [("squeezed", squeezed_results), ("quench", quench_results)]:
    classifications = [r['classification'] for r in family_data]
    transitions = []
    for i in range(len(classifications)-1):
        if classifications[i] != classifications[i+1]:
            transitions.append((i, family_data[i]['parameter'], family_data[i+1]['parameter'],
                              classifications[i], classifications[i+1],
                              family_data[i]['S_rel'], family_data[i+1]['S_rel']))

    if transitions:
        print(f"\n  {family_name}: transitions found:")
        for t in transitions:
            print(f"    {t[3]} -> {t[4]} between param={t[1]:.2f} and {t[2]:.2f}, "
                  f"S_rel in [{t[5]:.4f}, {t[6]:.4f}]")
    else:
        print(f"\n  {family_name}: NO transitions (all {classifications[0]})")

# Check universality: do both families fall on same curve?
print(f"\n--- Universality Check ---")
sq_srels = np.array([r['S_rel'] for r in squeezed_results])
sq_discs = np.array([r['discrepancy'] for r in squeezed_results])
qu_srels = np.array([r['S_rel'] for r in quench_results])
qu_discs = np.array([r['discrepancy'] for r in quench_results])

# Check if there's overlap in S_rel ranges
sq_range = (sq_srels.min(), sq_srels.max())
qu_range = (qu_srels.min(), qu_srels.max())
print(f"  Squeezed S_rel range: [{sq_range[0]:.4f}, {sq_range[1]:.4f}]")
print(f"  Quench S_rel range: [{qu_range[0]:.4f}, {qu_range[1]:.4f}]")

# Interpolation comparison in overlap region
overlap_min = max(sq_range[0], qu_range[0])
overlap_max = min(sq_range[1], qu_range[1])
if overlap_max > overlap_min:
    print(f"  Overlap region: [{overlap_min:.4f}, {overlap_max:.4f}]")
    # Find points from each family in the overlap
    sq_in = [(r['S_rel'], r['discrepancy']) for r in squeezed_results
             if overlap_min <= r['S_rel'] <= overlap_max]
    qu_in = [(r['S_rel'], r['discrepancy']) for r in quench_results
             if overlap_min <= r['S_rel'] <= overlap_max]
    if sq_in and qu_in:
        print(f"  Squeezed points in overlap: {len(sq_in)}")
        print(f"  Quench points in overlap: {len(qu_in)}")
        for s, d in sq_in:
            print(f"    Squeezed: S_rel={s:.4f}, disc={d*100:.1f}%")
        for s, d in qu_in:
            print(f"    Quench: S_rel={s:.4f}, disc={d*100:.1f}%")
else:
    print(f"  No overlap in S_rel ranges!")

# Correlation analysis
print(f"\n--- Correlation: disc vs S_rel ---")
for name, srels, discs in [("Squeezed", sq_srels, sq_discs), ("Quench", qu_srels, qu_discs)]:
    if len(srels) > 2:
        # Linear correlation
        corr = np.corrcoef(srels, discs)[0, 1]
        print(f"  {name}: Pearson r = {corr:.4f}")
        # Log-log if possible
        mask = (srels > 0) & (discs > 0)
        if mask.sum() > 2:
            log_corr = np.corrcoef(np.log(srels[mask]), np.log(discs[mask]))[0, 1]
            # Power law fit: disc ~ S_rel^alpha
            coeffs = np.polyfit(np.log(srels[mask]), np.log(discs[mask]), 1)
            print(f"  {name}: log-log Pearson r = {log_corr:.4f}, power law disc ~ S_rel^{coeffs[0]:.3f}")


# ============================================================
# SAVE RESULTS
# ============================================================
save_path = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/thermal-time/strategies/strategy-003/explorations/exploration-003/code/"

output = {
    "parameters": {
        "N": N, "beta": beta, "omega": omega, "lambda": lam,
        "omega_plus": float(omega_plus), "omega_minus": float(omega_minus),
        "N_tau": N_tau, "tau_max": float(tau_max),
    },
    "control": control_results,
    "squeezed_results": squeezed_results,
    "quench_results": quench_results,
}

with open(save_path + "results.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\nResults saved to {save_path}results.json")
print("DONE")
