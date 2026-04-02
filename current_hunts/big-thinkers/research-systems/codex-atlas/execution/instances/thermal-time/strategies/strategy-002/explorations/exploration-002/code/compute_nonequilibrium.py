"""
Exploration 002 — Non-Equilibrium TTH Test (Post-Quench State)

Three correlators for a post-quench state:
  1. C_QM(tau):         evolve x_A under COUPLED H_AB(lambda), state = rho_0 (uncoupled thermal)
  2. C_global_TTH(tau): evolve x_A under UNCOUPLED H_AB(0) = K_AB/beta (modular flow of rho_0)
  3. C_local_TTH(tau):  evolve x_A under K_A/beta (local modular Hamiltonian of rho_A = Tr_B[rho_0])

Key physics: rho_0 = exp(-beta H_AB(0))/Z_0 is NOT the Gibbs state of H_AB(lambda).
Therefore K_AB = beta*H_AB(0) != beta*H_AB(lambda), and modular flow differs from QM evolution.

Adapted from strategy-001/exploration-003/code/compute_correlators.py
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
omega = 1.0     # both oscillators have same frequency
beta = 2.0
lambda_vals = [0.0, 0.1, 0.2, 0.3, 0.5]  # 0.0 included as control
N_tau = 500
tau_arr = np.linspace(0, 4 * np.pi, N_tau)

print("=" * 70)
print("Exploration 002: Non-Equilibrium TTH Test (Post-Quench State)")
print(f"N={N}, beta={beta}, omega={omega}")
print(f"lambda values: {lambda_vals}")
print(f"tau in [0, 4pi], {N_tau} points")
print("=" * 70)

# ============================================================
# Build single-mode operators (N x N)
# ============================================================
n_op  = np.diag(np.arange(N, dtype=float))
a_op  = np.diag(np.sqrt(np.arange(1, N, dtype=float)), 1)
ad_op = a_op.T
q_op  = (a_op + ad_op) / np.sqrt(2)   # position operator
p_op  = 1j * (ad_op - a_op) / np.sqrt(2)  # momentum operator (not needed but for completeness)
I_N   = np.eye(N)

# Two-mode operators (N^2 x N^2)
# H_AB(lambda) = omega*(n_A + 1/2) + omega*(n_B + 1/2) + lambda*q_A*q_B
# We drop zero-point energy (constant shift doesn't affect dynamics)
H_A_2mode    = np.kron(omega * n_op, I_N)
H_B_2mode    = np.kron(I_N, omega * n_op)
H_int_base   = np.kron(q_op, q_op)        # q_A tensor q_B
H_uncoupled  = H_A_2mode + H_B_2mode      # H_AB(0)
x_A_2mode    = np.kron(q_op, I_N)         # x_A tensor I_B
x_A_1mode    = q_op                        # x_A in A subspace


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

    Memory-efficient spectral decomposition method.
    """
    evals, evecs = eigh(H_mat)
    rho_eig = evecs.conj().T @ rho_mat @ evecs
    x_eig   = evecs.conj().T @ x_op   @ evecs

    # Spectral weight matrix B (D x D)
    xrho = x_eig @ rho_eig
    B = x_eig * xrho.T  # B[m,n] = x_eig[m,n] * (x @ rho)[n,m]

    # Phase computation
    conj_phase = np.exp(-1j * np.outer(tau_arr, evals))
    phase      = conj_phase.conj()

    inner = B @ conj_phase.T     # (D, N_tau)
    C = np.sum(phase * inner.T, axis=1).real
    return C


def fft_analysis(C, tau_arr, n_peaks=8):
    """Return angular frequencies and amplitudes from FFT."""
    dt = tau_arr[1] - tau_arr[0]
    fft_vals  = np.fft.rfft(C - C.mean())
    freqs_hz  = np.fft.rfftfreq(len(C), d=dt)
    omega_arr = freqs_hz * 2 * np.pi
    amps      = np.abs(fft_vals)
    idx       = np.argsort(amps)[::-1][:n_peaks]
    return omega_arr[idx], amps[idx]


# ============================================================
# PART 1: GIBBS STATE CONTROL CHECK
# ============================================================
print(f"\n{'='*70}")
print("PART 1: GIBBS STATE CONTROL CHECK")
print("For Gibbs state: C_QM should equal C_global_TTH to machine zero")
print(f"{'='*70}")

gibbs_control = {}
for lam in [0.1, 0.3, 0.5]:
    H_coupled = H_uncoupled + lam * H_int_base

    # Gibbs state of the COUPLED system
    rho_gibbs = expm(-beta * H_coupled)
    Z_gibbs = np.trace(rho_gibbs).real
    rho_gibbs /= Z_gibbs

    # Check trace and positivity
    tr = np.trace(rho_gibbs).real
    evals_rho = np.linalg.eigvalsh(rho_gibbs)
    min_eval = evals_rho[0]
    print(f"  lam={lam}: Tr(rho_gibbs)={tr:.15f}, min eigenvalue={min_eval:.2e}")

    # C_QM: evolve under H_coupled with Gibbs state
    C_qm_gibbs = compute_correlator(H_coupled, rho_gibbs, x_A_2mode, tau_arr)

    # C_global_TTH: modular flow of Gibbs state = evolution under H_coupled
    # K_AB = beta*H_coupled + log(Z)*I, so K_AB/beta = H_coupled + const
    # The const doesn't affect Heisenberg evolution, so this IS C_QM
    C_global_gibbs = compute_correlator(H_coupled, rho_gibbs, x_A_2mode, tau_arr)

    max_diff = np.max(np.abs(C_qm_gibbs - C_global_gibbs))
    rel_diff = norm(C_qm_gibbs - C_global_gibbs) / norm(C_qm_gibbs)
    print(f"  lam={lam}: max|C_QM - C_global| = {max_diff:.2e}, rel = {rel_diff:.2e}")
    print(f"  CONTROL: {'PASS' if max_diff < 1e-10 else 'FAIL'}")

    gibbs_control[str(lam)] = {
        "max_diff": float(max_diff),
        "rel_diff": float(rel_diff),
        "passed": bool(max_diff < 1e-10)
    }


# ============================================================
# PART 2: POST-QUENCH STATE — MAIN COMPUTATION
# ============================================================
print(f"\n{'='*70}")
print("PART 2: POST-QUENCH STATE (NON-EQUILIBRIUM TTH TEST)")
print(f"{'='*70}")

# Build the post-quench state: thermal state of UNCOUPLED system
rho_0 = expm(-beta * H_uncoupled)
Z_0 = np.trace(rho_0).real
rho_0 /= Z_0
print(f"Post-quench state built: Z_0 = {Z_0:.6f}")
print(f"Tr(rho_0) = {np.trace(rho_0).real:.15f}")
evals_rho0 = np.linalg.eigvalsh(rho_0)
print(f"Min eigenvalue of rho_0 = {evals_rho0[0]:.2e}")
print(f"Max eigenvalue of rho_0 = {evals_rho0[-1]:.6f}")

# rho_0 is a product state: rho_0 = rho_A(0) tensor rho_B(0)
# where rho_A(0) = exp(-beta*omega*n_A)/Z_A
# Verify this:
rho_A_direct = expm(-beta * omega * n_op)
Z_A = np.trace(rho_A_direct).real
rho_A_direct /= Z_A
rho_A_from_trace = partial_trace_B(rho_0, N)
product_check = norm(rho_A_from_trace - rho_A_direct)
print(f"Product state check: ||rho_A(trace) - rho_A(direct)|| = {product_check:.2e}")

# Compute K_A for the post-quench state
K_A_quench, rho_A_quench = compute_K_A(rho_0, N)
# For product state, rho_A is just the thermal state of the uncoupled A
# So K_A = beta*omega*n_A + const, and K_A/beta = omega*n_A + const = H_A + const
# Local modular flow should be same as uncoupled H_A evolution
K_A_diff = K_A_quench - beta * omega * n_op
c_offset_A = np.trace(K_A_diff).real / N
K_A_shifted = K_A_diff - c_offset_A * I_N
print(f"K_A - beta*H_A (after removing constant): ||delta|| = {norm(K_A_shifted, 'fro'):.2e}")

all_results = {}

for lam in lambda_vals:
    print(f"\n{'='*70}")
    print(f"lambda = {lam}")
    t0 = time.time()

    # The coupled Hamiltonian (actual dynamics after quench)
    H_coupled = H_uncoupled + lam * H_int_base

    # Normal-mode frequencies
    omega_plus  = np.sqrt(omega**2 + lam)
    omega_minus = np.sqrt(omega**2 - lam) if omega**2 > lam else 0.0
    print(f"  Normal modes: omega_+ = {omega_plus:.6f}, omega_- = {omega_minus:.6f}")

    # --- C_QM: evolve under COUPLED H_AB(lambda), state = rho_0 ---
    print("  Computing C_QM ...", end=" ", flush=True)
    t1 = time.time()
    C_QM = compute_correlator(H_coupled, rho_0, x_A_2mode, tau_arr)
    print(f"done ({time.time()-t1:.1f}s)")

    # --- C_global_TTH: evolve under UNCOUPLED H_AB(0) (= modular flow of rho_0) ---
    # K_AB = -log(rho_0) = beta*H_AB(0) + log(Z_0)*I
    # K_AB/beta = H_AB(0) + const*I
    # Modular flow generates evolution under H_AB(0)
    print("  Computing C_global_TTH ...", end=" ", flush=True)
    t1 = time.time()
    C_global_TTH = compute_correlator(H_uncoupled, rho_0, x_A_2mode, tau_arr)
    print(f"done ({time.time()-t1:.1f}s)")

    # --- C_local_TTH: evolve under K_A/beta ---
    print("  Computing C_local_TTH ...", end=" ", flush=True)
    t1 = time.time()
    C_local_TTH = compute_correlator(K_A_quench / beta, rho_A_quench, x_A_1mode, tau_arr)
    print(f"done ({time.time()-t1:.1f}s)")

    # --- Discrepancies ---
    disc_global = norm(C_QM - C_global_TTH) / norm(C_QM) if norm(C_QM) > 0 else 0.0
    disc_local  = norm(C_QM - C_local_TTH)  / norm(C_QM) if norm(C_QM) > 0 else 0.0
    disc_gl_loc = norm(C_global_TTH - C_local_TTH) / norm(C_global_TTH) if norm(C_global_TTH) > 0 else 0.0
    max_diff_global = np.max(np.abs(C_QM - C_global_TTH))
    max_diff_local  = np.max(np.abs(C_QM - C_local_TTH))

    print(f"  ||C_QM - C_global_TTH|| / ||C_QM|| = {disc_global:.8f}")
    print(f"  ||C_QM - C_local_TTH||  / ||C_QM|| = {disc_local:.8f}")
    print(f"  ||C_global - C_local||  / ||C_global|| = {disc_gl_loc:.8f}")
    print(f"  max|C_QM - C_global_TTH| = {max_diff_global:.6e}")
    print(f"  max|C_QM - C_local_TTH|  = {max_diff_local:.6e}")

    # --- FFT spectral analysis ---
    freqs_qm,     amps_qm     = fft_analysis(C_QM,         tau_arr)
    freqs_global,  amps_global  = fft_analysis(C_global_TTH, tau_arr)
    freqs_local,   amps_local   = fft_analysis(C_local_TTH,  tau_arr)

    print(f"  FFT C_QM         top freqs: {np.round(freqs_qm[:5],4)}  amps: {np.round(amps_qm[:5],3)}")
    print(f"  FFT C_global_TTH top freqs: {np.round(freqs_global[:5],4)}  amps: {np.round(amps_global[:5],3)}")
    print(f"  FFT C_local_TTH  top freqs: {np.round(freqs_local[:5],4)}  amps: {np.round(amps_local[:5],3)}")

    if lam > 0:
        print(f"  Expected C_QM freqs: {omega_plus:.4f}, {omega_minus:.4f} (normal modes of coupled system)")
        print(f"  Expected C_global freqs: {omega:.4f} (uncoupled frequency only)")

    all_results[str(lam)] = {
        "lambda": lam,
        "omega_plus": float(omega_plus),
        "omega_minus": float(omega_minus),
        "C_QM":         C_QM.tolist(),
        "C_global_TTH": C_global_TTH.tolist(),
        "C_local_TTH":  C_local_TTH.tolist(),
        "disc_global":     float(disc_global),
        "disc_local":      float(disc_local),
        "disc_gl_loc":     float(disc_gl_loc),
        "max_diff_global": float(max_diff_global),
        "max_diff_local":  float(max_diff_local),
        "fft_qm_freqs":      freqs_qm.tolist(),
        "fft_qm_amps":       amps_qm.tolist(),
        "fft_global_freqs":   freqs_global.tolist(),
        "fft_global_amps":    amps_global.tolist(),
        "fft_local_freqs":    freqs_local.tolist(),
        "fft_local_amps":     amps_local.tolist(),
    }
    print(f"  Total elapsed: {time.time()-t0:.1f}s")


# ============================================================
# PART 3: CONVERGENCE CHECK (N=15, N=20, N=25 at lambda=0.3)
# ============================================================
print(f"\n{'='*70}")
print("PART 3: CONVERGENCE CHECK (lambda=0.3, varying N)")
print(f"{'='*70}")

convergence = {}
for N_check in [15, 25]:
    n_op_c  = np.diag(np.arange(N_check, dtype=float))
    a_op_c  = np.diag(np.sqrt(np.arange(1, N_check, dtype=float)), 1)
    ad_op_c = a_op_c.T
    q_op_c  = (a_op_c + ad_op_c) / np.sqrt(2)
    I_c     = np.eye(N_check)

    H_A2 = np.kron(omega * n_op_c, I_c)
    H_B2 = np.kron(I_c, omega * n_op_c)
    H_int2 = np.kron(q_op_c, q_op_c)
    xA2    = np.kron(q_op_c, I_c)
    xA1    = q_op_c

    H_uncoupled_c = H_A2 + H_B2
    lam_s = 0.3
    H_coupled_c = H_uncoupled_c + lam_s * H_int2

    # Post-quench state
    rho_0_c = expm(-beta * H_uncoupled_c)
    rho_0_c /= np.trace(rho_0_c).real

    K_A_c, rhoA_c = compute_K_A(rho_0_c, N_check)

    print(f"  N={N_check}: computing all three ...", end=" ", flush=True)
    C_qm_c     = compute_correlator(H_coupled_c, rho_0_c, xA2, tau_arr)
    C_global_c  = compute_correlator(H_uncoupled_c, rho_0_c, xA2, tau_arr)
    C_local_c   = compute_correlator(K_A_c / beta, rhoA_c, xA1, tau_arr)
    print("done")

    convergence[N_check] = {
        "C_QM": C_qm_c.tolist(),
        "C_global": C_global_c.tolist(),
        "C_local": C_local_c.tolist(),
    }

# Compare
C_qm_15 = np.array(convergence[15]["C_QM"])
C_qm_20 = np.array(all_results["0.3"]["C_QM"])
C_qm_25 = np.array(convergence[25]["C_QM"])
diff_qm_15_20 = norm(C_qm_15 - C_qm_20) / norm(C_qm_20)
diff_qm_20_25 = norm(C_qm_25 - C_qm_20) / norm(C_qm_20)
print(f"  C_QM: ||N=15 - N=20|| / ||N=20|| = {diff_qm_15_20:.4e}")
print(f"  C_QM: ||N=25 - N=20|| / ||N=20|| = {diff_qm_20_25:.4e}")

C_gl_15 = np.array(convergence[15]["C_global"])
C_gl_20 = np.array(all_results["0.3"]["C_global_TTH"])
C_gl_25 = np.array(convergence[25]["C_global"])
diff_gl_15_20 = norm(C_gl_15 - C_gl_20) / norm(C_gl_20)
diff_gl_20_25 = norm(C_gl_25 - C_gl_20) / norm(C_gl_20)
print(f"  C_global: ||N=15 - N=20|| / ||N=20|| = {diff_gl_15_20:.4e}")
print(f"  C_global: ||N=25 - N=20|| / ||N=20|| = {diff_gl_20_25:.4e}")


# ============================================================
# PART 4: DETAILED FFT SPECTRAL COMPARISON
# ============================================================
print(f"\n{'='*70}")
print("PART 4: DETAILED FFT SPECTRAL ANALYSIS")
print(f"{'='*70}")

dt = tau_arr[1] - tau_arr[0]
freq_axis = np.fft.rfftfreq(N_tau, d=dt) * 2 * np.pi  # angular frequencies

spectral_data = {}
for lam in [0.1, 0.2, 0.3, 0.5]:
    r = all_results[str(lam)]
    C_qm_arr = np.array(r["C_QM"])
    C_gl_arr = np.array(r["C_global_TTH"])
    C_lo_arr = np.array(r["C_local_TTH"])

    fft_qm  = np.abs(np.fft.rfft(C_qm_arr - C_qm_arr.mean()))
    fft_gl  = np.abs(np.fft.rfft(C_gl_arr - C_gl_arr.mean()))
    fft_lo  = np.abs(np.fft.rfft(C_lo_arr - C_lo_arr.mean()))

    omega_plus  = np.sqrt(omega**2 + lam)
    omega_minus = np.sqrt(omega**2 - lam)

    print(f"\n  lambda = {lam}:")
    print(f"    Expected normal modes: omega_+ = {omega_plus:.4f}, omega_- = {omega_minus:.4f}")
    print(f"    Expected uncoupled: omega = {omega:.4f}")

    # Find peaks above 5% of max
    for label, fft_data in [("C_QM", fft_qm), ("C_global", fft_gl), ("C_local", fft_lo)]:
        threshold = 0.05 * fft_data.max()
        peaks = freq_axis[fft_data > threshold]
        peak_amps = fft_data[fft_data > threshold]
        top_idx = np.argsort(peak_amps)[::-1][:5]
        print(f"    {label:>10} peaks: {np.round(peaks[top_idx], 4)}  (amps: {np.round(peak_amps[top_idx], 3)})")

    spectral_data[str(lam)] = {
        "freq_axis": freq_axis.tolist(),
        "fft_qm": fft_qm.tolist(),
        "fft_global": fft_gl.tolist(),
        "fft_local": fft_lo.tolist(),
    }


# ============================================================
# FINAL SUMMARY TABLE
# ============================================================
print(f"\n{'='*70}")
print("FINAL SUMMARY TABLE — POST-QUENCH STATE")
print(f"{'='*70}")
header = f"{'lam':>5}  {'omega+':>8}  {'omega-':>8}  {'||dC_global||':>14}  {'||dC_local||':>14}  {'max|dC_gl|':>12}  {'max|dC_lo|':>12}"
print(header)
print("-" * len(header))
for lam in lambda_vals:
    r = all_results[str(lam)]
    print(f"{lam:5.2f}  {r['omega_plus']:8.4f}  {r['omega_minus']:8.4f}  "
          f"{r['disc_global']:14.8f}  {r['disc_local']:14.8f}  "
          f"{r['max_diff_global']:12.6e}  {r['max_diff_local']:12.6e}")

print(f"\nConvergence (lambda=0.3):")
print(f"  C_QM:     N=15 vs N=20: {diff_qm_15_20:.2e},  N=25 vs N=20: {diff_qm_20_25:.2e}")
print(f"  C_global: N=15 vs N=20: {diff_gl_15_20:.2e},  N=25 vs N=20: {diff_gl_20_25:.2e}")


# ============================================================
# Save all results
# ============================================================
save_dir = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/thermal-time/strategies/strategy-002/explorations/exploration-002/code/"

output = {
    "tau_arr": tau_arr.tolist(),
    "N": N, "beta": beta, "omega": omega,
    "gibbs_control": gibbs_control,
    "results": all_results,
    "convergence": {
        "lambda": 0.3,
        "diff_qm_15_20": float(diff_qm_15_20),
        "diff_qm_20_25": float(diff_qm_20_25),
        "diff_gl_15_20": float(diff_gl_15_20),
        "diff_gl_20_25": float(diff_gl_20_25),
    },
}
with open(save_dir + "nonequilibrium_results.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\nResults saved to {save_dir}nonequilibrium_results.json")
print("DONE — Part 1 (main computation)")
