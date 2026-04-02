"""
Squeezed thermal state test: apply S(r) to thermal state of H_AB(lambda=0.3).

S(r) = exp[r(a_A^2 - a_A†^2)/2] applied to mode A only.
The resulting state is NOT a Gibbs state of H_AB(lambda).
"""

import numpy as np
from scipy.linalg import expm
from numpy.linalg import eigh, norm
import json

# ============================================================
# Parameters
# ============================================================
N = 20
omega = 1.0
beta = 2.0
lam = 0.3
r_squeeze = 0.3  # squeezing parameter
N_tau = 2000
tau_max = 16 * np.pi
tau_arr = np.linspace(0, tau_max, N_tau)

print("=" * 70)
print("Squeezed Thermal State Test")
print(f"N={N}, beta={beta}, omega={omega}, lambda={lam}, r={r_squeeze}")
print("=" * 70)

# Build operators
n_op  = np.diag(np.arange(N, dtype=float))
a_op  = np.diag(np.sqrt(np.arange(1, N, dtype=float)), 1)
ad_op = a_op.T
q_op  = (a_op + ad_op) / np.sqrt(2)
I_N   = np.eye(N)

H_A_2mode  = np.kron(omega * n_op, I_N)
H_B_2mode  = np.kron(I_N, omega * n_op)
H_int_base = np.kron(q_op, q_op)
H_uncoupled = H_A_2mode + H_B_2mode
H_coupled   = H_uncoupled + lam * H_int_base
x_A_2mode   = np.kron(q_op, I_N)
x_A_1mode   = q_op

# Squeezing operator: S(r) = exp[r(a^2 - a†^2)/2]
# Generator: (a^2 - a†^2)/2
gen_squeeze = (a_op @ a_op - ad_op @ ad_op) / 2.0
S_r = expm(r_squeeze * gen_squeeze)  # N x N unitary for mode A

# Two-mode squeezing operator: S_A tensor I_B
S_AB = np.kron(S_r, I_N)

# Start with thermal state of COUPLED system at lambda=0.3
rho_gibbs = expm(-beta * H_coupled)
rho_gibbs /= np.trace(rho_gibbs).real

# Apply squeezing: rho_squeezed = S rho_gibbs S†
rho_squeezed = S_AB @ rho_gibbs @ S_AB.conj().T

# Sanity checks
tr_sq = np.trace(rho_squeezed).real
evals_sq = np.linalg.eigvalsh(rho_squeezed)
print(f"Tr(rho_squeezed) = {tr_sq:.15f}")
print(f"Min eigenvalue = {evals_sq[0]:.2e}")
print(f"Max eigenvalue = {evals_sq[-1]:.6f}")

# Modular Hamiltonian of squeezed state
# K_sq = -log(rho_squeezed)
# This is NOT beta*H_coupled (that would be the Gibbs state)
evals_rho_sq, evecs_rho_sq = eigh(rho_squeezed)
log_evals_sq = -np.log(np.maximum(evals_rho_sq, 1e-300))
K_sq = (evecs_rho_sq @ np.diag(log_evals_sq) @ evecs_rho_sq.T).real

# Check how different K_sq is from beta*H_coupled
K_gibbs = beta * H_coupled + np.log(np.trace(expm(-beta * H_coupled)).real) * np.eye(N**2)
diff_K = K_sq - K_gibbs
diff_K_norm = norm(diff_K, 'fro') / norm(K_gibbs, 'fro')
print(f"||K_squeezed - K_gibbs|| / ||K_gibbs|| = {diff_K_norm:.6f}")

# Also compare to S†(beta H)S + const
K_expected = S_AB @ (beta * H_coupled) @ S_AB.conj().T
# K_sq should be S K_gibbs S† = S (beta*H + logZ*I) S† = beta * S H S† + logZ*I
K_transformed = S_AB @ K_gibbs @ S_AB.conj().T
diff_K_trans = norm(K_sq - K_transformed, 'fro')
print(f"||K_sq - S K_gibbs S†|| = {diff_K_trans:.2e}  (should be ~0)")

# Local modular Hamiltonian
def partial_trace_B(rho_AB, N):
    rho_A = np.zeros((N, N), dtype=complex)
    for k in range(N):
        rho_A += rho_AB[k::N, k::N]
    return rho_A

rho_A_sq = partial_trace_B(rho_squeezed, N)
rho_A_sq = (rho_A_sq + rho_A_sq.conj().T) / 2
evals_A_sq, evecs_A_sq = eigh(rho_A_sq)
log_evals_A = -np.log(np.maximum(evals_A_sq, 1e-300))
K_A_sq = (evecs_A_sq @ np.diag(log_evals_A) @ evecs_A_sq.T).real

# Compute correlators
def compute_correlator(H_mat, rho_mat, x_op, tau_arr):
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

# C_QM: evolve under H_coupled
print("\nComputing C_QM (squeezed)...", end=" ", flush=True)
C_QM_sq = compute_correlator(H_coupled, rho_squeezed, x_A_2mode, tau_arr)
print("done")

# C_global_TTH: evolve under K_sq/beta (modular flow of squeezed state)
# Note: K_sq/beta is NOT H_coupled (it's a "squeezed" version of it)
print("Computing C_global_TTH (squeezed)...", end=" ", flush=True)
# We need to normalize: modular parameter s maps to physical time tau via tau = beta*s
# The modular Hamiltonian K generates flow at rate 1: sigma_s(A) = e^{iKs} A e^{-iKs}
# Physical time identification: tau = beta*s, so sigma_tau(A) = e^{iK tau/beta} A e^{-iK tau/beta}
C_global_sq = compute_correlator(K_sq / beta, rho_squeezed, x_A_2mode, tau_arr)
print("done")

# C_local_TTH: evolve under K_A_sq/beta
print("Computing C_local_TTH (squeezed)...", end=" ", flush=True)
C_local_sq = compute_correlator(K_A_sq / beta, rho_A_sq.real, x_A_1mode, tau_arr)
print("done")

# Also compute Gibbs-state correlators for comparison
C_QM_gibbs   = compute_correlator(H_coupled, rho_gibbs, x_A_2mode, tau_arr)
C_global_gibbs = compute_correlator(H_coupled, rho_gibbs, x_A_2mode, tau_arr)  # should equal C_QM

# Discrepancies
disc_global_sq = norm(C_QM_sq - C_global_sq) / norm(C_QM_sq)
disc_local_sq  = norm(C_QM_sq - C_local_sq)  / norm(C_QM_sq)
disc_gl_lo_sq  = norm(C_global_sq - C_local_sq) / norm(C_global_sq)
max_diff_global_sq = np.max(np.abs(C_QM_sq - C_global_sq))
max_diff_local_sq  = np.max(np.abs(C_QM_sq - C_local_sq))

print(f"\n{'='*70}")
print("SQUEEZED STATE RESULTS (lambda={lam}, r={r_squeeze})")
print(f"{'='*70}")
print(f"||C_QM - C_global_TTH|| / ||C_QM|| = {disc_global_sq:.8f}")
print(f"||C_QM - C_local_TTH||  / ||C_QM|| = {disc_local_sq:.8f}")
print(f"||C_global - C_local||  / ||C_global|| = {disc_gl_lo_sq:.8f}")
print(f"max|C_QM - C_global| = {max_diff_global_sq:.6e}")
print(f"max|C_QM - C_local|  = {max_diff_local_sq:.6e}")

# FFT analysis
dt = tau_arr[1] - tau_arr[0]
N_pad = N_tau * 8
freq_axis = np.fft.rfftfreq(N_pad, d=dt) * 2 * np.pi

omega_plus  = np.sqrt(omega**2 + lam)
omega_minus = np.sqrt(omega**2 - lam)

def find_peaks(fft_data, freq_axis, threshold_frac=0.02, n_peaks=8):
    threshold = threshold_frac * fft_data.max()
    peaks = []
    for i in range(1, len(fft_data)-1):
        if fft_data[i] > threshold and fft_data[i] > fft_data[i-1] and fft_data[i] > fft_data[i+1]:
            peaks.append((freq_axis[i], fft_data[i]))
    peaks.sort(key=lambda x: -x[1])
    return peaks[:n_peaks]

fft_qm_sq  = np.abs(np.fft.rfft(C_QM_sq - C_QM_sq.mean(), n=N_pad))
fft_gl_sq  = np.abs(np.fft.rfft(C_global_sq - C_global_sq.mean(), n=N_pad))
fft_lo_sq  = np.abs(np.fft.rfft(C_local_sq - C_local_sq.mean(), n=N_pad))

peaks_qm   = find_peaks(fft_qm_sq, freq_axis)
peaks_gl   = find_peaks(fft_gl_sq, freq_axis)
peaks_lo   = find_peaks(fft_lo_sq, freq_axis)

print(f"\nExpected coupled normal modes: omega_+ = {omega_plus:.4f}, omega_- = {omega_minus:.4f}")

print(f"\nC_QM (squeezed) peaks:")
for freq, amp in peaks_qm[:6]:
    match = ""
    if abs(freq - omega_plus) < 0.05: match = " <-- omega_+"
    elif abs(freq - omega_minus) < 0.05: match = " <-- omega_-"
    elif abs(freq - omega) < 0.05: match = " <-- omega"
    print(f"  omega = {freq:.4f}  amp = {amp:.3f}{match}")

print(f"\nC_global_TTH (squeezed) peaks:")
for freq, amp in peaks_gl[:6]:
    match = ""
    if abs(freq - omega_plus) < 0.05: match = " <-- omega_+"
    elif abs(freq - omega_minus) < 0.05: match = " <-- omega_-"
    elif abs(freq - omega) < 0.05: match = " <-- omega"
    print(f"  omega = {freq:.4f}  amp = {amp:.3f}{match}")

print(f"\nC_local_TTH (squeezed) peaks:")
for freq, amp in peaks_lo[:6]:
    match = ""
    if abs(freq - omega_plus) < 0.05: match = " <-- omega_+"
    elif abs(freq - omega_minus) < 0.05: match = " <-- omega_-"
    elif abs(freq - omega) < 0.05: match = " <-- omega"
    print(f"  omega = {freq:.4f}  amp = {amp:.3f}{match}")

# Physical interpretation: squeezed state vs post-quench
# The squeezed state K = S†(beta H + logZ)S / beta ≠ H
# The modular flow generates evolution under K/beta = S†HS (up to const)
# So the modular Hamiltonian is the Hamiltonian conjugated by the squeezing operator

print(f"\n{'='*70}")
print("PHYSICAL INTERPRETATION")
print(f"{'='*70}")
print(f"For the squeezed state rho = S rho_gibbs S†:")
print(f"  K_squeezed = S K_gibbs S† = S (beta H) S† (up to const)")
print(f"  K_squeezed/beta = S† H S (modular flow Hamiltonian)")
print(f"  This is the Hamiltonian in a 'squeezed frame'")
print(f"  The modular time does NOT correspond to actual Hamiltonian evolution")

# How different are the dynamics? Compare C_QM with Gibbs C_QM
disc_sq_gibbs = norm(C_QM_sq - C_QM_gibbs) / norm(C_QM_gibbs)
print(f"\n||C_QM(squeezed) - C_QM(gibbs)|| / ||C_QM(gibbs)|| = {disc_sq_gibbs:.6f}")
print(f"(How different the squeezed state's QM correlator is from the equilibrium one)")

# Compare: for the post-quench case at same lambda
n_bar = 1.0 / (np.exp(beta * omega) - 1)
C_QM_quench = compute_correlator(H_coupled,
    expm(-beta * H_uncoupled) / np.trace(expm(-beta * H_uncoupled)).real,
    x_A_2mode, tau_arr)
disc_quench = norm(C_QM_quench - C_QM_gibbs) / norm(C_QM_gibbs)
print(f"||C_QM(quench) - C_QM(gibbs)|| / ||C_QM(gibbs)|| = {disc_quench:.6f}")
print(f"(For comparison: post-quench discrepancy at same lambda)")

# Save
save_dir = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/thermal-time/strategies/strategy-002/explorations/exploration-002/code/"
results_sq = {
    "lambda": lam, "r_squeeze": r_squeeze, "beta": beta,
    "disc_global": float(disc_global_sq),
    "disc_local": float(disc_local_sq),
    "disc_gl_lo": float(disc_gl_lo_sq),
    "peaks_qm": [(float(f), float(a)) for f,a in peaks_qm],
    "peaks_global": [(float(f), float(a)) for f,a in peaks_gl],
    "peaks_local": [(float(f), float(a)) for f,a in peaks_lo],
    "K_diff_from_gibbs": float(diff_K_norm),
}
with open(save_dir + "squeezed_results.json", "w") as f:
    json.dump(results_sq, f, indent=2)

print(f"\nResults saved. DONE — squeezed state test")
