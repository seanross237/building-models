"""
Exploration 003 — Full QM vs Local TTH: The Critical Comparison

Three correlators:
  1. C_full(tau):   standard QM, evolves x_A under H_AB (full coupled Hamiltonian)
  2. C_local(tau):  local TTH, evolves x_A under K_A/beta (local modular Hamiltonian)
  3. C_global(tau): control check, should equal C_full exactly (K_AB = beta*H_AB)

Memory-efficient implementation: O(D^2 * N_tau) time, O(D^2 + D*N_tau) memory.
"""

import numpy as np
from scipy.linalg import expm
from numpy.linalg import eigh, norm
import json
import time

# ============================================================
# Parameters
# ============================================================
N = 20          # Fock truncation per mode
omega_A = 1.0
omega_B = 1.0
beta = 2.0
lambda_vals = [0.1, 0.2, 0.3, 0.5]
N_tau = 500
tau_arr = np.linspace(0, 4 * np.pi, N_tau)

print("=" * 70)
print("Exploration 003: Full QM vs Local TTH Comparison")
print(f"N={N}, beta={beta}, omega_A=omega_B={omega_A}")
print(f"lambda values: {lambda_vals}")
print(f"tau in [0, 4pi], {N_tau} points")
print("=" * 70)

# ============================================================
# Build single-mode operators (N x N)
# ============================================================
n_op  = np.diag(np.arange(N, dtype=float))
a_op  = np.diag(np.sqrt(np.arange(1, N, dtype=float)), 1)
ad_op = a_op.T
q_op  = (a_op + ad_op) / np.sqrt(2)   # (a + a†)/√2
I_N   = np.eye(N)

# Two-mode operators (N² × N²)
H_A_2mode    = np.kron(omega_A * n_op, I_N)
H_B_2mode    = np.kron(I_N, omega_B * n_op)
H_int_base   = np.kron(q_op, q_op)        # q_A ⊗ q_B
x_A_2mode    = np.kron(q_op, I_N)         # x_A ⊗ I_B  (N² × N²)
x_A_1mode    = q_op                        # x_A in A subspace (N × N)


# ============================================================
# Helpers
# ============================================================

def partial_trace_B(rho_AB, N):
    """Partial trace over B. Kron convention: A=slow index, B=fast index."""
    rho_A = np.zeros((N, N), dtype=complex)
    for k in range(N):
        rho_A += rho_AB[k::N, k::N]
    return rho_A


def compute_K_A(rho_AB, N):
    """K_A = -log(rho_A), computed via eigendecomposition with clip at 1e-300."""
    rho_A = partial_trace_B(rho_AB, N)
    rho_A = (rho_A + rho_A.conj().T) / 2   # symmetrize

    evals_A, evecs_A = eigh(rho_A)
    log_evals = -np.log(np.maximum(evals_A, 1e-300))
    K_A = (evecs_A @ np.diag(log_evals) @ evecs_A.T).real
    return K_A, rho_A.real


def compute_correlator(H_mat, rho_mat, x_op, tau_arr):
    """
    C(tau) = Tr[ rho * e^{iH tau} x e^{-iH tau} * x ]

    Memory-efficient: uses O(D^2 + D*N_tau) memory.

    Derivation:
      In H eigenbasis (evals E_k, evecs V):
        rho_eig = V† rho V   (diagonal for Gibbs state, but works generally)
        x_eig   = V† x V

      C(tau) = sum_{m,n} B[m,n] * exp(i*(E_m - E_n)*tau)
      where B[m,n] = (x_eig @ rho_eig).T[m,n] * x_eig[m,n]
                   = (x_eig @ rho_eig)[n,m]   * x_eig[m,n]

    Vectorised over tau:
      conj_phase[i,n] = exp(-i E_n tau_i)       shape (N_tau, D)
      inner = B @ conj_phase.T                   shape (D, N_tau)
      C[i]  = sum_m exp(i E_m tau_i) * inner[m,i]
    """
    evals, evecs = eigh(H_mat)

    rho_eig = evecs.conj().T @ rho_mat @ evecs
    x_eig   = evecs.conj().T @ x_op   @ evecs

    # Precompute spectral weight matrix B (D×D)
    xrho = x_eig @ rho_eig           # (D, D)
    B = x_eig * xrho.T               # element-wise: B[m,n] = x_eig[m,n] * xrho[n,m]
    # Note: xrho.T[m,n] = xrho[n,m] = (x_eig @ rho_eig)[n,m] ✓

    # Vectorised phase computation  (N_tau × D, only 3.2 MB for D=400, N_tau=500)
    conj_phase = np.exp(-1j * np.outer(tau_arr, evals))   # (N_tau, D)
    phase      = conj_phase.conj()                          # (N_tau, D)

    # inner[m, i] = sum_n B[m,n] * conj_phase[i,n]
    inner = B @ conj_phase.T     # (D, N_tau)

    # C[i] = sum_m phase[i,m] * inner[m,i]
    C = np.sum(phase * inner.T, axis=1).real   # (N_tau,)
    return C


def fft_peaks(C, tau_arr, n_peaks=5):
    """Return the top-n angular frequencies and amplitudes from FFT."""
    dt = tau_arr[1] - tau_arr[0]
    fft_vals  = np.fft.rfft(C - C.mean())
    freqs_hz  = np.fft.rfftfreq(len(C), d=dt)
    omega_arr = freqs_hz * 2 * np.pi
    amps      = np.abs(fft_vals)
    idx       = np.argsort(amps)[::-1][:n_peaks]
    return omega_arr[idx], amps[idx]


def first_zero_crossing(tau, C):
    """Time of first sign change, via linear interpolation."""
    for i in range(1, len(C)):
        if C[i-1] * C[i] < 0:
            return tau[i-1] - C[i-1] * (tau[i] - tau[i-1]) / (C[i] - C[i-1])
    return None


# ============================================================
# Main sweep
# ============================================================
all_results = {}

for lam in lambda_vals:
    print(f"\n{'='*70}")
    print(f"lambda = {lam}")
    t0 = time.time()

    # Full Hamiltonian
    H_AB = H_A_2mode + H_B_2mode + lam * H_int_base

    # Global Gibbs state
    rho_AB = expm(-beta * H_AB)
    Z      = np.trace(rho_AB).real
    rho_AB /= Z
    print(f"  rho_AB built  (Z={Z:.4f})")

    # Local modular Hamiltonian
    K_A, rho_A = compute_K_A(rho_AB, N)
    H_A_1mode  = omega_A * n_op
    delta_K    = K_A - beta * H_A_1mode
    c_offset   = np.trace(delta_K).real / N
    delta_K   -= c_offset * I_N
    frob_dK    = norm(delta_K, 'fro')
    print(f"  K_A built  ||delta_K||_F={frob_dK:.5f}")

    # Normal-mode frequencies (analytical)
    # H = p²/2 + omega²q²/2 for each + lambda*q_A*q_B
    # Normal-mode eigenvalues of potential: omega² ± lambda
    omega_plus  = np.sqrt(omega_A**2 + lam)
    omega_minus = np.sqrt(omega_A**2 - lam)
    beat_freq   = omega_plus - omega_minus
    print(f"  Predicted: omega_+={omega_plus:.4f}, omega_-={omega_minus:.4f}, beat={beat_freq:.4f}")

    # --- Computation 1: C_full (standard QM, full H_AB) ---
    print("  Computing C_full ...", end=" ", flush=True)
    t1 = time.time()
    C_full = compute_correlator(H_AB, rho_AB, x_A_2mode, tau_arr)
    print(f"done ({time.time()-t1:.1f}s)")

    # --- Computation 2: C_local (TTH, local modular flow K_A/beta) ---
    print("  Computing C_local...", end=" ", flush=True)
    t1 = time.time()
    C_local = compute_correlator(K_A / beta, rho_A, x_A_1mode, tau_arr)
    print(f"done ({time.time()-t1:.1f}s)")

    # --- Computation 3: C_global (control: K_AB/beta = H_AB, should = C_full) ---
    # K_AB = -log(rho_AB). For Gibbs state: rho_AB = exp(-beta*H_AB)/Z
    # => K_AB = beta*H_AB + log(Z)*I
    # K_AB/beta = H_AB + (log Z / beta) * I
    # The constant shift in H doesn't affect the correlator (commutes through, cancels),
    # so C_global must equal C_full up to machine precision.
    print("  Computing C_global...", end=" ", flush=True)
    t1 = time.time()
    C_global = compute_correlator(H_AB, rho_AB, x_A_2mode, tau_arr)
    # (K_AB/beta = H_AB + const*I; const shift doesn't change Heisenberg evolution)
    print(f"done ({time.time()-t1:.1f}s)")

    ctrl_max_diff = np.max(np.abs(C_global - C_full))
    print(f"  Control: max|C_global - C_full| = {ctrl_max_diff:.2e}  (target < 1e-10)")

    # --- Frequency analysis ---
    freqs_full,  amps_full  = fft_peaks(C_full,  tau_arr)
    freqs_local, amps_local = fft_peaks(C_local, tau_arr)
    print(f"  FFT C_full  top freqs: {np.round(freqs_full,4)}  amps: {np.round(amps_full,3)}")
    print(f"  FFT C_local top freqs: {np.round(freqs_local,4)}  amps: {np.round(amps_local,3)}")

    # --- Zero-crossing (effective period) ---
    t_zc_full  = first_zero_crossing(tau_arr, C_full)
    t_zc_local = first_zero_crossing(tau_arr, C_local)
    if t_zc_full and t_zc_local:
        shift_rel = (t_zc_local - t_zc_full) / t_zc_full
        print(f"  Zero crossings: full={t_zc_full:.4f}, local={t_zc_local:.4f}")
        print(f"  Relative shift (local-full)/full = {shift_rel:.4f}")
        print(f"  Predicted by 002 (0.68*lambda^2) = {0.68*lam**2:.4f}")
    else:
        shift_rel = None

    # --- Key metric ---
    rel_disc = norm(C_full - C_local) / norm(C_full)
    print(f"  ||C_full - C_local|| / ||C_full|| = {rel_disc:.6f}")

    all_results[str(lam)] = {
        "lambda": lam,
        "omega_plus": float(omega_plus),
        "omega_minus": float(omega_minus),
        "beat_freq": float(beat_freq),
        "frob_norm_delta_K": float(frob_dK),
        "C_full":   C_full.tolist(),
        "C_local":  C_local.tolist(),
        "C_global": C_global.tolist(),
        "control_max_diff": float(ctrl_max_diff),
        "top_freqs_full":   freqs_full.tolist(),
        "top_amps_full":    amps_full.tolist(),
        "top_freqs_local":  freqs_local.tolist(),
        "top_amps_local":   amps_local.tolist(),
        "t_zero_full":  float(t_zc_full)  if t_zc_full  else None,
        "t_zero_local": float(t_zc_local) if t_zc_local else None,
        "relative_shift": float(shift_rel) if shift_rel else None,
        "relative_discrepancy": float(rel_disc),
    }

    print(f"  Total elapsed: {time.time()-t0:.1f}s")


# ============================================================
# Stability check: N=15 and N=25 at lambda=0.3
# ============================================================
print(f"\n{'='*70}")
print("Stability / convergence check at lambda=0.3")
print("Running N=15 and N=25 ...")

stability = {}
for N_check in [15, 25]:
    n_op_c  = np.diag(np.arange(N_check, dtype=float))
    a_op_c  = np.diag(np.sqrt(np.arange(1, N_check, dtype=float)), 1)
    ad_op_c = a_op_c.T
    q_op_c  = (a_op_c + ad_op_c) / np.sqrt(2)
    I_c     = np.eye(N_check)

    H_A2 = np.kron(omega_A * n_op_c, I_c)
    H_B2 = np.kron(I_c, omega_B * n_op_c)
    H_int2 = np.kron(q_op_c, q_op_c)
    xA2    = np.kron(q_op_c, I_c)
    xA1    = q_op_c

    lam_s  = 0.3
    H_s    = H_A2 + H_B2 + lam_s * H_int2
    rho_s  = expm(-beta * H_s); rho_s /= np.trace(rho_s).real
    K_s, rhoA_s = compute_K_A(rho_s, N_check)

    print(f"  N={N_check}: computing C_local ...", end=" ", flush=True)
    C_loc_s = compute_correlator(K_s / beta, rhoA_s, xA1, tau_arr)
    print("done")
    stability[N_check] = C_loc_s.tolist()

# Compare N=15 vs N=20 vs N=25
C_loc_15 = np.array(stability[15])
C_loc_20 = np.array(all_results["0.3"]["C_local"])
C_loc_25 = np.array(stability[25])

diff_15_20 = norm(C_loc_15 - C_loc_20) / norm(C_loc_20)
diff_20_25 = norm(C_loc_25 - C_loc_20) / norm(C_loc_20)
print(f"  ||C_local(N=15) - C_local(N=20)|| / ||N=20|| = {diff_15_20:.4e}")
print(f"  ||C_local(N=25) - C_local(N=20)|| / ||N=20|| = {diff_20_25:.4e}")


# ============================================================
# Save
# ============================================================
save_dir = "/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/thermal-time/strategies/strategy-001/explorations/exploration-003/code/"

output = {
    "tau_arr": tau_arr.tolist(),
    "N": N, "beta": beta, "omega_A": omega_A, "omega_B": omega_B,
    "results": all_results,
    "stability": {
        "lambda": 0.3,
        "N_values": [15, 20, 25],
        "diff_15_20": float(diff_15_20),
        "diff_20_25": float(diff_20_25),
    }
}
with open(save_dir + "comparison_results.json", "w") as f:
    json.dump(output, f, indent=2)


# ============================================================
# Print final summary table
# ============================================================
print(f"\n{'='*70}")
print("FINAL SUMMARY TABLE")
print(f"{'='*70}")
header = f"{'lam':>5}  {'omega+':>8}  {'omega-':>8}  {'beat':>8}  {'||dK||':>8}  {'||dC||/||Cf||':>14}"
print(header)
print("-" * len(header))
for lam in lambda_vals:
    r = all_results[str(lam)]
    print(f"{lam:5.2f}  {r['omega_plus']:8.4f}  {r['omega_minus']:8.4f}  "
          f"{r['beat_freq']:8.4f}  {r['frob_norm_delta_K']:8.4f}  "
          f"{r['relative_discrepancy']:14.8f}")

print(f"\nStability (lambda=0.3):")
print(f"  N=15 vs N=20 : {diff_15_20:.2e}")
print(f"  N=25 vs N=20 : {diff_20_25:.2e}")

print(f"\nResults saved to {save_dir}comparison_results.json")
print("DONE")
