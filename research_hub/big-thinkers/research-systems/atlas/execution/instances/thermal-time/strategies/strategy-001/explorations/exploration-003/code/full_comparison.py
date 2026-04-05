"""
Exploration 003 — Full QM vs Local TTH: The Critical Comparison

Three correlators:
  1. C_full(tau):   standard QM, evolves x_A under H_AB (full coupled Hamiltonian)
  2. C_local(tau):  local TTH, evolves x_A under K_A/beta (local modular Hamiltonian)
  3. C_global(tau): control check, should equal C_full exactly (K_AB = beta*H_AB)

Physical parameters:
  omega_A = omega_B = 1.0, beta = 2.0
  lambda in {0.1, 0.2, 0.3, 0.5}
  N_trunc = 20 per mode (400x400 full space)
  tau in [0, 4*pi], 500 points
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
print(f"N={N}, omega_A={omega_A}, omega_B={omega_B}, beta={beta}")
print(f"lambda values: {lambda_vals}")
print(f"tau in [0, 4*pi], {N_tau} points")
print("=" * 70)

# ============================================================
# Single-mode operators (N x N)
# ============================================================
n_op = np.diag(np.arange(N, dtype=float))
a_op = np.diag(np.sqrt(np.arange(1, N, dtype=float)), 1)
ad_op = a_op.T
q_op = (a_op + ad_op) / np.sqrt(2)   # position-like: (a + a†)/sqrt(2)
I_N = np.eye(N)

# ============================================================
# Two-mode operators (N^2 x N^2)
# ============================================================
H_A_2mode = np.kron(omega_A * n_op, I_N)
H_B_2mode = np.kron(I_N, omega_B * n_op)
H_int_base = np.kron(q_op, q_op)     # q_A ⊗ q_B
x_A_2mode = np.kron(q_op, I_N)       # x_A = q_A ⊗ I_B
x_A_1mode = q_op                      # x_A in A subspace (N x N)

# ============================================================
# Helper: Partial trace over B (trace out fast index)
# ============================================================
def partial_trace_B(rho_AB, N):
    """Partial trace over B. Kron convention: A=slow, B=fast."""
    rho_A = np.zeros((N, N), dtype=complex)
    for k in range(N):
        rho_A += rho_AB[k::N, k::N]
    return rho_A

# ============================================================
# Helper: Compute correlator C(tau) via eigendecomposition
# Given H (or K), rho, x_op, all in the same Hilbert space,
# C(tau) = Tr[rho * e^{iH tau} x_op e^{-iH tau} * x_op]
# ============================================================
def compute_correlator(H_mat, rho_mat, x_op, tau_arr):
    """
    Compute C(tau) = Tr[rho * (e^{iH tau} x_op e^{-iH tau}) * x_op]
    using eigendecomposition for efficiency.

    H_mat: generator of time evolution (N x N or N^2 x N^2)
    rho_mat: density matrix
    x_op: observable (same size as H_mat)
    tau_arr: array of times
    """
    # Diagonalize H
    evals, evecs = eigh(H_mat)

    # Transform rho and x_op to eigenbasis
    # rho_tilde = evecs.T @ rho @ evecs (but evecs is unitary, so evecs.conj().T @ rho @ evecs)
    rho_eig = evecs.conj().T @ rho_mat @ evecs
    x_eig   = evecs.conj().T @ x_op  @ evecs

    # C(tau) = sum_{mnp} rho_{mn} * x_{np} * x_{pm} * e^{i(E_m - E_n)tau} ... wait
    # Let me do it properly.
    # x_A(tau) = e^{iH tau} x_A e^{-iH tau}
    # In eigenbasis: [x_A(tau)]_{mn} = x_{mn} * e^{i(E_m - E_n) tau}
    # C(tau) = Tr[rho x_A(tau) x_A]
    #        = sum_{mnp} rho_{mp} [x_A(tau)]_{pn} [x_A]_{nm}
    # Wait - let me be careful about operator ordering.
    # C(tau) = Tr[rho * A(tau) * B] where A=B=x_A
    # = Tr[rho * e^{iH tau} x_A e^{-iH tau} * x_A]
    # In eigenbasis (using tilde notation for eigenbasis):
    # = sum_{m} [rho e^{iH tau} x_A e^{-iH tau} x_A]_{mm}
    # Let phi_k be eigenvectors, E_k eigenvalues.
    # [e^{iH tau}]_{mn} = delta_{mn} e^{i E_m tau} in eigenbasis
    # [x_A(tau)]_{mn} = e^{i E_m tau} [x_A]_{mn} e^{-i E_n tau} (in eigenbasis)
    # C(tau) = sum_{m,n,p} rho_{mp} * [x_A(tau)]_{pn} * [x_A]_{nm}
    #        = sum_{m,n,p} rho_{mp} * x_{pn} * e^{i(E_p - E_n) tau} * x_{nm}

    # So: C(tau) = sum_{m,n,p} rho_{mp} * x_{pn} * x_{nm} * exp(i*(E_p - E_n)*tau)

    # Precompute coefficient array: A_{mn,p} = rho_{mp} * x_{pn} * x_{nm}
    # Group by frequency omega_k = E_p - E_n:
    # C(tau) = sum_{p,n} [sum_m rho_{mp} * x_{nm}] * x_{pn} * exp(i*(E_p - E_n)*tau)

    # Define M_{pn} = sum_m rho_{mp} * x_{nm} = (rho @ x_eig.T)_{pn} = (rho.T @ x_eig)...
    # Wait: sum_m rho_{mp} * x_{nm} = [rho^T]_{pm} x_{mn}^T ... let me just compute directly.

    # M = x_eig.T @ rho_eig  (shape: [N, N] or [N^2, N^2])
    # M_{pn} = sum_m [x_eig.T]_{pm} rho_{mn} ... hmm.

    # Actually: sum_m rho_{mp} * x_{nm} = sum_m rho_{mp} x_{nm}
    # = (rho^T x)_{pn} ... no.
    # Let me define Z_{pn} = sum_m x_{nm} rho_{mp} = (x rho)_{np} ... so Z = x_eig @ rho_eig, Z_{np} = sum_m x_{nm} rho_{mp}
    # Then sum_m rho_{mp} x_{nm} = Z_{np} = (x_eig @ rho_eig)_{np}

    # So C(tau) = sum_{p,n} Z_{np} * x_{pn} * exp(i*(E_p-E_n)*tau)
    #           = sum_{p,n} (x_eig @ rho_eig)_{np} * x_{pn} * exp(i*(E_p-E_n)*tau)

    # Note: x_{pn} = x_eig[p,n], (x_eig @ rho_eig)_{np} = xrho[n,p]
    # C(tau) = sum_{p,n} xrho[n,p] * x_eig[p,n] * exp(i*(E_p-E_n)*tau)
    #        = sum_{p,n} (xrho * x_eig.T)[n,p]... let me define coeff[n,p] = xrho[n,p]*x_eig[p,n]
    # Actually the element-wise: coeff_{np} = xrho[n,p] * x_eig[p,n]
    # This doesn't simplify to a simple product of matrices (one index is transposed).

    # Simpler: use matrix trace formula.
    # C(tau) = Tr[rho * e^{iH tau} x e^{-iH tau} x]
    # In eigenbasis:
    # = Tr[rho_eig * e^{iD tau} x_eig e^{-iD tau} x_eig]
    # where D = diag(evals).
    # [e^{iD tau} x_eig e^{-iD tau}]_{mn} = x_eig[m,n] * exp(i*(evals[m]-evals[n])*tau)

    # So C(tau) = sum_{m,n} [rho_eig * (e^{iD tau} x_eig e^{-iD tau})]_{nm} * x_eig[m,n]
    # Hmm, let me just loop over tau. For large matrices this is slow, but let's do it smart.

    # C(tau) = Tr[rho_eig @ (x_eig * phase_matrix(tau)) @ x_eig]
    # where phase_matrix[m,n] = exp(i*(evals[m]-evals[n])*tau)

    # = sum_{m,n,k} rho_eig[m,k] * [x_eig*phase]_{k,n} * x_eig[n,m]
    # Actually: Tr[A @ B @ C] = sum_{m,n,k} A[m,k] B[k,n] C[n,m]
    # = Tr[(rho_eig @ (x_eig * phase)) @ x_eig]

    # Let's precompute: coeff[m,n] = (rho_eig @ x_eig)[m,n] * x_eig[n,m]
    # because Tr[A @ B @ C] = sum_{m} [A @ B @ C]_{mm}
    # = sum_{m,n} [A @ B]_{mn} C_{nm}
    # So C(tau) = sum_{m,n} [rho_eig @ (x_eig * phase)]_{mn} * x_eig[n,m]
    #           = sum_{m,n} sum_k rho_eig[m,k] * x_eig[k,n] * phase[k,n] * x_eig[n,m]

    # Define G[k,n] = x_eig[k,n] * x_eig[n,...] summed over n with rho...
    # This is getting complex. Let me precompute:
    # For each (k,n) pair, the coefficient is:
    # amp[k,n] = sum_m rho_eig[m,k] * x_eig[n,m] = (rho_eig.T)[k,m] x_eig[n,m]
    #           = x_eig[n,:] @ rho_eig[:,k] = x_eig[n,:] @ rho_eig[:,k]
    # So amp = x_eig @ rho_eig  (shape DxD), amp[n,k] = sum_m x_eig[n,m]*rho_eig[m,k]
    # Then C(tau) = sum_{k,n} x_eig[k,n] * amp[n,k] * phase[k,n]
    # = sum_{k,n} x_eig[k,n] * (x_eig @ rho_eig)[n,k] * exp(i*(evals[k]-evals[n])*tau)

    # Let coeff_mat[k,n] = x_eig[k,n] * (x_eig @ rho_eig)[n,k]
    # = x_eig[k,n] * (x_eig @ rho_eig)[n,k]
    # = (x_eig * (x_eig @ rho_eig).T)[k,n]  -- element-wise multiply

    # C(tau) = sum_{k,n} coeff_mat[k,n] * exp(i*(evals[k]-evals[n])*tau)

    # This can be computed as: C(tau) = flatten(coeff_mat) . flatten(exp(i * outer(evals, -evals) * tau))
    # But we can speed up by grouping by frequency difference.

    # Precompute coeff_mat (independent of tau)
    amp = x_eig @ rho_eig   # amp[n,k] = sum_m x_eig[n,m] * rho_eig[m,k]
    coeff_mat = x_eig * amp.T  # element-wise: [k,n] = x_eig[k,n] * amp[n,k] = x_eig[k,n] * amp.T[k,n]
    # Wait: amp.T[k,n] = amp[n,k] - yes that's right.

    # Frequency differences matrix: freq[k,n] = evals[k] - evals[n]
    # C(tau) = sum_{k,n} coeff_mat[k,n] * exp(i * freq[k,n] * tau)

    # Vectorized over tau:
    freq_mat = evals[:, None] - evals[None, :]   # shape (D, D)

    # For each tau: C(tau) = sum_{k,n} coeff_mat[k,n] * exp(i * freq[k,n] * tau)
    # = Re[trace-like sum]

    # Vectorize: flatten coeff and freq, then use np.dot for each tau
    coeff_flat = coeff_mat.flatten()
    freq_flat = freq_mat.flatten()

    # C[tau_i] = Re[sum_j coeff_flat[j] * exp(i * freq_flat[j] * tau_i)]
    # = Re[coeff_flat @ exp(i * freq_flat * tau_i)]
    # Vectorized: exp_mat[j, i] = exp(i * freq_flat[j] * tau_arr[i])
    # C = Re[coeff_flat @ exp_mat]  --> shape (N_tau,)

    exp_mat = np.exp(1j * np.outer(freq_flat, tau_arr))  # shape (D^2, N_tau)
    C = (coeff_flat @ exp_mat).real  # shape (N_tau,)

    return C

# ============================================================
# Helper: Compute local modular Hamiltonian K_A
# ============================================================
def compute_K_A(rho_AB, N):
    """
    Compute K_A = -log(rho_A) where rho_A = partial_trace_B(rho_AB).
    Uses eigendecomposition, clips eigenvalues at 1e-300.
    """
    rho_A = partial_trace_B(rho_AB, N)
    rho_A = (rho_A + rho_A.conj().T) / 2  # Symmetrize

    evals_A, evecs_A = eigh(rho_A)
    evals_A_clipped = np.maximum(evals_A, 1e-300)
    log_evals = -np.log(evals_A_clipped)
    K_A = evecs_A @ np.diag(log_evals) @ evecs_A.T
    K_A = K_A.real
    return K_A, rho_A

# ============================================================
# Helper: FFT frequency analysis
# ============================================================
def fft_analysis(C_tau, tau_arr):
    """
    Return dominant frequencies and their amplitudes from FFT of C(tau).
    Returns sorted (freq, amp) pairs.
    """
    dt = tau_arr[1] - tau_arr[0]
    N = len(C_tau)
    fft_vals = np.fft.rfft(C_tau - C_tau.mean())
    freqs = np.fft.rfftfreq(N, d=dt) * 2 * np.pi  # Angular frequency (rad/unit)
    amplitudes = np.abs(fft_vals)

    # Sort by amplitude descending
    idx_sort = np.argsort(amplitudes)[::-1]
    return freqs[idx_sort], amplitudes[idx_sort]

# ============================================================
# Helper: First zero crossing
# ============================================================
def first_zero_crossing(tau, C):
    """Find time of first zero crossing via linear interpolation."""
    for i in range(1, len(C)):
        if C[i-1] * C[i] < 0:
            t_cross = tau[i-1] - C[i-1] * (tau[i] - tau[i-1]) / (C[i] - C[i-1])
            return t_cross
    return None

# ============================================================
# Main: Compute three correlators for each lambda
# ============================================================
all_results = {}

for lam in lambda_vals:
    print(f"\n{'='*70}")
    print(f"lambda = {lam}")
    print(f"{'='*70}")
    t0 = time.time()

    # --- Build full Hamiltonian ---
    H_AB = H_A_2mode + H_B_2mode + lam * H_int_base

    # --- Global thermal state ---
    print("  Computing rho_AB...", end=" ", flush=True)
    rho_AB = expm(-beta * H_AB)
    Z = np.trace(rho_AB).real
    rho_AB /= Z
    print(f"done (Z={Z:.4f})")

    # --- Local modular Hamiltonian K_A ---
    print("  Computing K_A...", end=" ", flush=True)
    K_A, rho_A = compute_K_A(rho_AB, N)
    print(f"done (K_A range: [{K_A.min():.3f}, {K_A.max():.3f}])")

    # Check K_A vs beta*H_A_1mode
    H_A_1mode = omega_A * n_op
    diff_KA = K_A - beta * H_A_1mode
    c_offset = np.trace(diff_KA).real / N
    delta_K = diff_KA - c_offset * I_N
    frob_dK = norm(delta_K, 'fro')
    print(f"  ||delta_K_A||_F = {frob_dK:.6f}, offset c = {c_offset:.4f}")

    # --- Normal mode analysis ---
    # For small lambda, eigenvalues of H_AB should split around omega
    # Normal mode frequencies: omega_pm = sqrt(omega^2 +/- lambda)
    omega_plus  = np.sqrt(omega_A**2 + lam)   # coupling shifts omega^2 by +/- lambda
    omega_minus = np.sqrt(omega_A**2 - lam)
    # Wait: H_AB = omega a†a + omega b†b + lambda q_A q_B
    # q_A q_B = (a+a†)/sqrt(2) * (b+b†)/sqrt(2) = (ab + a†b† + a†b + ab†)/2
    # Normal modes: A± = (a ± b)/sqrt(2), with frequencies
    # H_+ = omega_+ A+†A+, omega_+ = sqrt(omega^2 + lambda/2) ... actually let's just
    # use the relation from classical mechanics:
    # omega_± = sqrt(omega^2 ± lambda/2) ... the coupling in q_A q_B gives lambda/2 in freq^2
    # Actually: H_int = lambda * q_A * q_B
    # The q_A q_B coupling in the position representation:
    # V(q_A, q_B) = lambda * q_A * q_B
    # Mass matrix M = I, spring matrix K = diag(omega^2, omega^2) + lambda * offdiag
    # K = [[omega^2, lambda/2],[lambda/2, omega^2]]  ? No...
    # In harmonic oscillator: H = p^2/2 + omega^2 q^2/2 for each + lambda q_A q_B
    # So total: H = (p_A^2 + omega^2 q_A^2)/2 + (p_B^2 + omega^2 q_B^2)/2 + lambda q_A q_B
    # Normal modes: omega_± = sqrt(omega^2 ± lambda)
    # since the potential matrix is [[omega^2, lambda],[lambda, omega^2]]
    # eigenvalues: omega^2 ± lambda
    # So omega_± = sqrt(omega^2 ± lambda)
    print(f"  Normal mode frequencies: omega_+ = {omega_plus:.4f}, omega_- = {omega_minus:.4f}")
    print(f"  Beat frequency: delta_omega = {omega_plus - omega_minus:.4f}")

    # --- Computation 1: C_full_QM(tau) ---
    print("  Computing C_full_QM...", end=" ", flush=True)
    t1 = time.time()
    C_full = compute_correlator(H_AB, rho_AB, x_A_2mode, tau_arr)
    print(f"done ({time.time()-t1:.1f}s)")

    # --- Computation 2: C_local_TTH(tau) ---
    # Uses K_A/beta as generator (so physical time tau maps to modular time tau/beta)
    # C_local(tau) = Tr[rho_A * e^{i K_A tau/beta} x_A e^{-i K_A tau/beta} * x_A]
    # Equivalently: use K_A/beta as the "Hamiltonian"
    print("  Computing C_local_TTH...", end=" ", flush=True)
    t1 = time.time()
    C_local = compute_correlator(K_A / beta, rho_A, x_A_1mode, tau_arr)
    print(f"done ({time.time()-t1:.1f}s)")

    # --- Computation 3: C_global_TTH(tau) (control check) ---
    # K_AB = beta * H_AB for Gibbs state
    # C_global = Tr[rho_AB e^{i K_AB tau/beta} x_A e^{-i K_AB tau/beta} x_A]
    #          = Tr[rho_AB e^{i H_AB tau} x_A e^{-i H_AB tau} x_A]
    #          = C_full by construction
    # We compute this explicitly to verify consistency.
    K_AB = beta * H_AB  # This is -log(rho_AB) up to a constant (partition function)
    # Note: K_AB/beta = H_AB, so C_global = C_full. We compute anyway as cross-check.
    print("  Computing C_global_TTH (control)...", end=" ", flush=True)
    t1 = time.time()
    C_global = compute_correlator(K_AB / beta, rho_AB, x_A_2mode, tau_arr)
    print(f"done ({time.time()-t1:.1f}s)")

    # --- Verification: C_global should = C_full ---
    max_diff_global = np.max(np.abs(C_global - C_full))
    print(f"  Control check: max|C_global - C_full| = {max_diff_global:.2e} (should be < 1e-6)")

    # --- Frequency analysis ---
    freqs_full, amps_full = fft_analysis(C_full, tau_arr)
    freqs_local, amps_local = fft_analysis(C_local, tau_arr)

    top_freqs_full = freqs_full[:5]
    top_amps_full = amps_full[:5]
    top_freqs_local = freqs_local[:5]
    top_amps_local = amps_local[:5]

    print(f"  C_full top frequencies: {top_freqs_full.round(4)} (amps: {top_amps_full.round(3)})")
    print(f"  C_local top frequencies: {top_freqs_local.round(4)} (amps: {top_amps_local.round(3)})")

    # --- Period shift analysis ---
    t_zero_full  = first_zero_crossing(tau_arr, C_full)
    t_zero_local = first_zero_crossing(tau_arr, C_local)

    if t_zero_full and t_zero_local:
        shift = (t_zero_local - t_zero_full) / t_zero_full
        print(f"  First zero crossing: C_full={t_zero_full:.4f}, C_local={t_zero_local:.4f}")
        print(f"  Period shift (local-full)/full = {shift:.4f}")
        print(f"  Exploration-002 prediction: 0.68*lambda^2 = {0.68*lam**2:.4f}")

    # --- Key metric: relative discrepancy ---
    norm_diff = norm(C_full - C_local) / norm(C_full)
    print(f"  ||C_full - C_local||_2 / ||C_full||_2 = {norm_diff:.6f}")

    # Store results
    all_results[lam] = {
        "lambda": lam,
        "omega_plus": float(omega_plus),
        "omega_minus": float(omega_minus),
        "beat_freq": float(omega_plus - omega_minus),
        "frob_norm_delta_K": float(frob_dK),
        "C_full": C_full.tolist(),
        "C_local": C_local.tolist(),
        "C_global": C_global.tolist(),
        "control_check_max_diff": float(max_diff_global),
        "top_freqs_full": top_freqs_full.tolist(),
        "top_amps_full": top_amps_full.tolist(),
        "top_freqs_local": top_freqs_local.tolist(),
        "top_amps_local": top_amps_local.tolist(),
        "t_zero_full": float(t_zero_full) if t_zero_full else None,
        "t_zero_local": float(t_zero_local) if t_zero_local else None,
        "norm_diff_full_local": float(norm_diff),
    }

    print(f"  Elapsed: {time.time()-t0:.1f}s")

# Save results
save_path = "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/thermal-time/strategies/strategy-001/explorations/exploration-003/code/"

with open(save_path + "comparison_results.json", "w") as f:
    # Convert to JSON-serializable (tau_arr is np.array)
    out = {
        "tau_arr": tau_arr.tolist(),
        "N": N,
        "beta": beta,
        "omega_A": omega_A,
        "omega_B": omega_B,
        "results": all_results
    }
    json.dump(out, f, indent=2)

print(f"\n{'='*70}")
print("SUMMARY TABLE")
print(f"{'='*70}")
print(f"{'lambda':>8} {'omega_+':>10} {'omega_-':>10} {'beat_freq':>12} {'||dK||_F':>10} {'||dC||/||Cf||':>15}")
print("-" * 70)
for lam in lambda_vals:
    r = all_results[lam]
    print(f"{lam:8.2f} {r['omega_plus']:10.4f} {r['omega_minus']:10.4f} "
          f"{r['beat_freq']:12.4f} {r['frob_norm_delta_K']:10.4f} {r['norm_diff_full_local']:15.8f}")

print(f"\nResults saved to {save_path}comparison_results.json")
print("DONE")
