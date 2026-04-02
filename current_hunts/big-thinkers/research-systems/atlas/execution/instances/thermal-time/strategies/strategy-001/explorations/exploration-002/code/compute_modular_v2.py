"""
Exploration 002 — Part B: Entangled-State Modular Hamiltonian (CORRECTED)

Fixed: Use eigendecomposition-based logm instead of scipy logm with bad regularization.
The tiny eigenvalues (e.g., p_{19} ~ 2.7e-17 for n=19 Fock state) are physically correct
(thermal population of high energy states), not numerical noise. Do NOT add I*epsilon.

Setup:
  H_AB = omega_A * a†a ⊗ I + I ⊗ omega_B * b†b + lambda * q_A ⊗ q_B
  rho_AB = exp(-beta * H_AB) / Z
  rho_A = Tr_B[rho_AB]
  K_A = -log(rho_A)  [via eigendecomposition]
  delta_K_A = K_A - beta * H_A_red - (trace offset) * I
"""

import numpy as np
from scipy.linalg import expm
from numpy.linalg import norm, eigh
import json

# ============================================================
# Parameters
# ============================================================
N = 20        # Fock space truncation per mode
omega_A = 1.0
omega_B = 1.0
beta = 2.0
lambda_vals = np.arange(0.0, 0.55, 0.05)

# ============================================================
# Single-mode operators
# ============================================================
n_op = np.diag(np.arange(N, dtype=float))
a_op = np.diag(np.sqrt(np.arange(1, N, dtype=float)), 1)
ad_op = a_op.T
q_op = (a_op + ad_op) / np.sqrt(2)
p_op = 1j * (ad_op - a_op) / np.sqrt(2)
I_N = np.eye(N)

# ============================================================
# Two-mode operators
# ============================================================
H_A = np.kron(omega_A * n_op, I_N)
H_B = np.kron(I_N, omega_B * n_op)
H_int_base = np.kron(q_op, q_op)  # q_A ⊗ q_B
q_A_2mode = np.kron(q_op, I_N)
q_B_2mode = np.kron(I_N, q_op)

# H_A in the A subspace (N×N)
H_A_red = omega_A * n_op

# ============================================================
# Functions
# ============================================================
def partial_trace_B(rho_AB, N):
    """Partial trace over system B. A=slow index, B=fast index (numpy kron convention)."""
    rho_A = np.zeros((N, N), dtype=complex)
    for k in range(N):
        rho_A += rho_AB[k::N, k::N]
    return rho_A

def matrix_log_via_eig(M, clip_min=1e-300):
    """
    Compute -log(M) via eigendecomposition.
    M must be symmetric positive semi-definite.
    Clips very small eigenvalues to clip_min to avoid log(0).
    """
    evals, evecs = eigh(M)
    evals_clipped = np.maximum(evals, clip_min)
    log_evals = np.log(evals_clipped)
    return -evecs @ np.diag(log_evals) @ evecs.T

def modular_flow(K_A, q_A_op, t_arr):
    """
    Compute sigma_t(q_A) = e^{iK_A t} q_A e^{-iK_A t} using eigendecomposition.
    Returns <n|sigma_t(q_A)|0> as a function of t (expectation value proxy).

    More precisely: returns Tr[rho_A * sigma_t(q_A)] = Tr[e^{-iK_A t} rho_A e^{iK_A t} q_A]
    """
    evals_K, evecs_K = eigh(K_A)

    correlations = []
    for t in t_arr:
        # U(t) = exp(-i K_A t)
        phase = np.exp(-1j * evals_K * t)
        Ut = evecs_K @ np.diag(phase) @ evecs_K.T
        # sigma_t(q_A) = U(-t) q_A U(t) = Ut† q_A Ut (with Ut = e^{-iK_A t})
        sigma_t_qA = Ut.conj().T @ q_A_op @ Ut
        # rho_A = exp(-K_A) / trace
        rho_A = evecs_K @ np.diag(np.exp(-evals_K)) @ evecs_K.T
        rho_A /= np.trace(rho_A).real
        corr = np.trace(rho_A @ sigma_t_qA).real
        correlations.append(corr)
    return np.array(correlations)

# ============================================================
# Main computation: lambda sweep
# ============================================================
print("="*65)
print("Modular Hamiltonian Computation (CORRECTED)")
print(f"N={N}, omega_A={omega_A}, omega_B={omega_B}, beta={beta}")
print("="*65)
print(f"{'lambda':>8} {'||dK||_F':>12} {'power':>8} {'c (offset)':>12} {'K_A[0,0]':>10} {'K_A[1,1]':>10}")
print("-"*65)

results = []

for lam in lambda_vals:
    # Hamiltonian
    H_AB = H_A + H_B + lam * H_int_base

    # Global thermal state
    rho_AB = expm(-beta * H_AB)
    Z = np.trace(rho_AB).real
    rho_AB /= Z

    # Partial trace
    rho_A = partial_trace_B(rho_AB, N)
    rho_A = (rho_A + rho_A.conj().T) / 2  # Symmetrize

    # Modular Hamiltonian via eigendecomposition (no spurious regularization)
    evals_A, evecs_A = eigh(rho_A)
    min_eval_A = evals_A.min()

    # K_A = -log(rho_A), clip at 1e-300 to avoid log(0) for machine-precision zeros
    log_evals = -np.log(np.maximum(evals_A, 1e-300))
    K_A = evecs_A @ np.diag(log_evals) @ evecs_A.T
    K_A = K_A.real  # Should be real

    # delta_K = K_A - beta*H_A_red - c*I (c chosen to zero trace)
    diff = K_A - beta * H_A_red
    c = np.trace(diff).real / N
    delta_K = diff - c * np.eye(N)

    frob = norm(delta_K, 'fro')

    print(f"{lam:8.2f} {frob:12.6f} {'':>8} {c:12.4f} {K_A[0,0]:10.4f} {K_A[1,1]:10.4f}")

    results.append({
        "lambda": float(lam),
        "frob_norm_delta_K": frob,
        "scalar_offset_c": float(c),
        "min_eval_rho_A": float(min_eval_A),
        "K_A_diagonal": K_A.diagonal().real.tolist(),
        "delta_K_diagonal": delta_K.diagonal().real.tolist(),
        "delta_K_matrix": delta_K.real.tolist(),  # Save full matrix for analysis
        "rho_A_eigenvalues": evals_A.tolist(),
    })

# ============================================================
# Perturbative scaling
# ============================================================
print("\n" + "="*65)
print("Perturbative scaling (fit ||dK|| ~ lambda^p)")
print("="*65)

frob_arr = np.array([r["frob_norm_delta_K"] for r in results])
lam_arr = np.array([r["lambda"] for r in results])

# Fit using lambda > 0.01
mask = lam_arr > 0.01
if mask.sum() >= 3:
    log_lam = np.log(lam_arr[mask])
    log_frob = np.log(frob_arr[mask])
    p, const = np.polyfit(log_lam, log_frob, 1)
    print(f"  Best fit: ||dK|| ≈ exp({const:.3f}) * lambda^{p:.3f}")
    print(f"  (O(λ¹) → p=1.0, O(λ²) → p=2.0)")

    # Check first few points for order
    for i in range(1, min(5, mask.sum())):
        lam_i = lam_arr[mask][i]
        if i > 0:
            ratio = frob_arr[mask][i] / frob_arr[mask][i-1]
            lam_ratio = lam_arr[mask][i] / lam_arr[mask][i-1]
            print(f"  lambda={lam_i:.2f}: frob={frob_arr[mask][i]:.6f}, "
                  f"||dK||/||dK||-prev = {ratio:.3f} (lam ratio = {lam_ratio:.2f})")

# ============================================================
# Detailed analysis at lambda=0.3
# ============================================================
print("\n" + "="*65)
print("Detailed analysis at lambda=0.3")
print("="*65)
idx_03 = list(lambda_vals).index(0.3) if 0.3 in lambda_vals else None
if idx_03 is not None:
    r = results[idx_03]
    print(f"||delta_K||_F = {r['frob_norm_delta_K']:.6f}")
    print(f"K_A diagonal: {[f'{x:.4f}' for x in r['K_A_diagonal'][:8]]}")
    c_val = r["scalar_offset_c"]
    print(f"Expected (beta*n + c): {[round(beta*n + c_val, 4) for n in range(8)]}")
    print(f"delta_K diagonal: {[f'{x:.4f}' for x in r['delta_K_diagonal'][:8]]}")

    # Structure of delta_K
    dK = np.array(r['delta_K_matrix'])
    print(f"\ndelta_K Frobenius norm: {r['frob_norm_delta_K']:.4f}")
    print(f"delta_K max off-diagonal: {np.max(np.abs(dK - np.diag(dK.diagonal()))):.4f}")
    print(f"delta_K diagonal range: [{np.min(dK.diagonal()):.4f}, {np.max(dK.diagonal()):.4f}]")

    # Is delta_K proportional to n^2 or n or something else?
    n_arr = np.arange(N)
    dK_diag = dK.diagonal()
    # Try fit: delta_K[n,n] = A*n^2 + B*n
    A_quad = np.polyfit(n_arr, dK_diag, 2)
    print(f"Fit delta_K[n,n] ≈ {A_quad[0]:.4f}*n^2 + {A_quad[1]:.4f}*n + {A_quad[2]:.4f}")

# ============================================================
# Modular flow comparison at lambda=0.3
# ============================================================
print("\n" + "="*65)
print("Modular flow comparison: TTH vs Heisenberg at lambda=0.3")
print("="*65)

lam_test = 0.30
H_AB_test = H_A + H_B + lam_test * H_int_base
rho_AB_test = expm(-beta * H_AB_test)
rho_AB_test /= np.trace(rho_AB_test).real
rho_A_test = partial_trace_B(rho_AB_test, N)
rho_A_test = (rho_A_test + rho_A_test.conj().T) / 2

evals_test, evecs_test = eigh(rho_A_test)
log_evals_test = -np.log(np.maximum(evals_test, 1e-300))
K_A_test = evecs_test @ np.diag(log_evals_test) @ evecs_test.T
K_A_test = K_A_test.real

t_arr = np.linspace(0, np.pi, 100)

# TTH modular flow: sigma_t(q_A) under K_A
evals_Ka, evecs_Ka = eigh(K_A_test)
rho_A_from_K = evecs_Ka @ np.diag(np.exp(-evals_Ka)) @ evecs_Ka.T
rho_A_from_K /= np.trace(rho_A_from_K).real

C_TTH = []
C_QM = []
C_TTH_normalized = []

for t in t_arr:
    # TTH: C(t) = Tr[rho_A * sigma_t(q_A) * q_A]  where sigma_t = e^{iK_A t} q_A e^{-iK_A t}
    phase_K = np.exp(1j * evals_Ka * t)
    Ut_K = evecs_Ka @ np.diag(phase_K) @ evecs_Ka.T  # e^{iK_A t}
    sigma_t = Ut_K @ q_op @ Ut_K.conj().T
    C_TTH.append(np.trace(rho_A_from_K @ q_op @ sigma_t).real)

    # Standard QM (Heisenberg under H_A_red)
    evals_HA, evecs_HA = eigh(H_A_red)
    phase_H = np.exp(1j * evals_HA * t)
    Ut_H = evecs_HA @ np.diag(phase_H) @ evecs_HA.T  # e^{iH_A t}
    q_t_QM = Ut_H @ q_op @ Ut_H.conj().T
    C_QM.append(np.trace(rho_A_from_K @ q_op @ q_t_QM).real)

    # TTH with normalization τ = β*t (i.e., modular time runs at t=τ/β)
    t_phys = t / beta  # If τ = β * t_modular, then at physical time t, modular param = t/β
    phase_K_norm = np.exp(1j * evals_Ka * t_phys)
    Ut_K_norm = evecs_Ka @ np.diag(phase_K_norm) @ evecs_Ka.T
    sigma_t_norm = Ut_K_norm @ q_op @ Ut_K_norm.conj().T
    C_TTH_normalized.append(np.trace(rho_A_from_K @ q_op @ sigma_t_norm).real)

C_TTH = np.array(C_TTH)
C_QM = np.array(C_QM)
C_TTH_normalized = np.array(C_TTH_normalized)

print(f"At t=0: C_TTH={C_TTH[0]:.4f}, C_QM={C_QM[0]:.4f}, C_TTH_norm={C_TTH_normalized[0]:.4f}")
print(f"At t=pi: C_TTH={C_TTH[-1]:.4f}, C_QM={C_QM[-1]:.4f}, C_TTH_norm={C_TTH_normalized[-1]:.4f}")

# First zero crossing (oscillation frequency)
def first_zero_crossing(t, C):
    for i in range(1, len(C)):
        if C[i-1] * C[i] < 0:
            t_cross = t[i-1] - C[i-1] * (t[i] - t[i-1]) / (C[i] - C[i-1])
            return t_cross
    return None

t_TTH = first_zero_crossing(t_arr, C_TTH)
t_QM = first_zero_crossing(t_arr, C_QM)
t_TTH_norm = first_zero_crossing(t_arr, C_TTH_normalized)

print(f"\nFirst zero crossing (quarter-period):")
print(f"  TTH modular flow: t = {t_TTH}")
print(f"  QM Heisenberg:    t = {t_QM}")
print(f"  TTH normalized (tau=beta*t): t = {t_TTH_norm}")
print(f"  Ratio TTH/QM: {t_TTH/t_QM if (t_TTH and t_QM) else 'N/A':.4f}")
print(f"  Expected if TTH oscillates at beta*omega: ratio = {1.0/beta:.4f}")

# ============================================================
# Save results
# ============================================================
save_dir = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/thermal-time/strategies/strategy-001/explorations/exploration-002/code/"

# Main results (without huge matrix, just key quantities)
results_summary = [{
    "lambda": r["lambda"],
    "frob_norm_delta_K": r["frob_norm_delta_K"],
    "scalar_offset_c": r["scalar_offset_c"],
    "min_eval_rho_A": r["min_eval_rho_A"],
    "K_A_first4_diag": r["K_A_diagonal"][:4],
    "delta_K_first4_diag": r["delta_K_diagonal"][:4],
} for r in results]

with open(save_dir + "sweep_results_v2.json", "w") as f:
    json.dump(results_summary, f, indent=2)

# Save flow comparison
flow_data = {
    "t_arr": t_arr.tolist(),
    "C_TTH": C_TTH.tolist(),
    "C_QM": C_QM.tolist(),
    "C_TTH_normalized": C_TTH_normalized.tolist(),
    "lambda_test": lam_test,
    "beta": beta,
    "omega_A": omega_A
}
with open(save_dir + "flow_comparison.json", "w") as f:
    json.dump(flow_data, f, indent=2)

print(f"\nResults saved to {save_dir}")

# Also print a summary table
print("\n" + "="*65)
print("FINAL SUMMARY TABLE")
print("="*65)
print(f"{'lambda':>8} {'||dK||_F':>12} {'dK[0,0]':>10} {'dK[1,1]':>10} {'dK[2,2]':>10}")
print("-"*65)
for r in results:
    dK_d = r["delta_K_diagonal"]
    print(f"{r['lambda']:8.2f} {r['frob_norm_delta_K']:12.6f} "
          f"{dK_d[0]:10.4f} {dK_d[1]:10.4f} {dK_d[2]:10.4f}")
