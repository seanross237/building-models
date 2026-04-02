"""
Exploration 002 — Part B: Entangled-State Modular Hamiltonian Computation

Computes K_A = -log(rho_A) for two coupled harmonic oscillators:
  H_AB = omega_A * a†a ⊗ I + I ⊗ omega_B * b†b + lambda * q_A ⊗ q_B
  rho_AB = exp(-beta * H_AB) / Z
  rho_A = Tr_B[rho_AB]
  K_A = -log(rho_A)

Then computes Delta_K_A = K_A - beta * H_A_reduced (minus scalar offset)
to see if entanglement modifies the modular Hamiltonian.
"""

import numpy as np
from scipy.linalg import expm, logm
from numpy.linalg import norm
import json

# ============================================================
# Parameters
# ============================================================
N = 20        # Fock space truncation per mode (total space = N x N = 400 x 400)
omega_A = 1.0
omega_B = 1.0
beta = 2.0
lambda_vals = np.arange(0.0, 0.55, 0.05)

# ============================================================
# Single-mode operators (N x N)
# ============================================================
n_op = np.diag(np.arange(N, dtype=float))                     # number operator
a_op = np.diag(np.sqrt(np.arange(1, N, dtype=float)), 1)      # lowering
ad_op = a_op.T                                                  # raising
q_op = (a_op + ad_op) / np.sqrt(2)                             # position = (a+a†)/√2
I_N = np.eye(N)

# ============================================================
# Two-mode operators (N^2 x N^2) via tensor products
# ============================================================
H_A = np.kron(omega_A * n_op, I_N)    # omega_A * n_A ⊗ I_B
H_B = np.kron(I_N, omega_B * n_op)    # I_A ⊗ omega_B * n_B
q_A_2mode = np.kron(q_op, I_N)        # q_A ⊗ I_B
q_B_2mode = np.kron(I_N, q_op)        # I_A ⊗ q_B
H_int_base = np.kron(q_op, q_op)      # q_A ⊗ q_B (without lambda factor)

# H_A_reduced: H_A restricted to mode A subspace
H_A_red = omega_A * n_op              # N x N

# ============================================================
# Partial trace: trace over system B (second mode)
# rho_A[i,j] = sum_k rho_AB[i*N + k, j*N + k]
# ============================================================
def partial_trace_B(rho_AB, N):
    """Trace out subsystem B (index block structure: A tensored with B)."""
    rho_A = np.zeros((N, N), dtype=complex)
    for k in range(N):
        rho_A += rho_AB[k::N, k::N]
    return rho_A

# ============================================================
# Main computation
# ============================================================
print("="*60)
print("Modular Hamiltonian Computation")
print(f"N={N}, omega_A={omega_A}, omega_B={omega_B}, beta={beta}")
print("="*60)

results = []

for lam in lambda_vals:
    # Build Hamiltonian
    H_AB = H_A + H_B + lam * H_int_base

    # Global thermal state
    rho_AB = expm(-beta * H_AB)
    Z = np.trace(rho_AB).real
    rho_AB /= Z

    # Partial trace to get rho_A
    rho_A = partial_trace_B(rho_AB, N)
    rho_A = (rho_A + rho_A.conj().T) / 2  # Symmetrize for numerical stability

    # Verify positivity and normalization
    evals_A = np.linalg.eigvalsh(rho_A)
    min_eval = evals_A.min()
    trace_A = np.trace(rho_A).real

    # Modular Hamiltonian: K_A = -log(rho_A)
    # Add small regularization if needed
    if min_eval < 1e-15:
        rho_A_reg = rho_A + 1e-15 * np.eye(N)
        rho_A_reg /= np.trace(rho_A_reg)
        K_A = -logm(rho_A_reg)
    else:
        K_A = -logm(rho_A)
    K_A = K_A.real  # Should be real and symmetric

    # Comparison: beta * H_A_red
    beta_HA = beta * H_A_red

    # Scalar offset: align K_A and beta*H_A by subtracting their means
    # delta_K = K_A - beta*H_A - c*I where c is chosen to make trace(delta_K) = 0
    diff = K_A - beta_HA
    c = np.trace(diff).real / N
    delta_K = diff - c * np.eye(N)

    # Frobenius norm of delta_K
    frob_norm = norm(delta_K, 'fro')

    # Eigenvalue spectrum of delta_K
    evals_delta = np.linalg.eigvalsh(delta_K)

    print(f"lambda={lam:.2f}: ||delta_K||_F={frob_norm:.6f}, "
          f"min_eval(rho_A)={min_eval:.2e}, Tr[rho_A]={trace_A:.6f}, "
          f"c={c:.4f}, delta_K_range=[{evals_delta.min():.4f}, {evals_delta.max():.4f}]")

    results.append({
        "lambda": float(lam),
        "frob_norm_delta_K": frob_norm,
        "scalar_offset_c": float(c),
        "min_eval_rho_A": float(min_eval),
        "trace_rho_A": float(trace_A),
        "K_A_diagonal": K_A.diagonal().tolist(),
        "beta_HA_diagonal": beta_HA.diagonal().tolist(),
        "delta_K_eigenvalues_min5": evals_delta[:5].tolist(),
        "delta_K_eigenvalues_max5": evals_delta[-5:].tolist(),
    })

# ============================================================
# Check perturbative scaling: fit ||delta_K|| ~ lambda^p
# ============================================================
print("\n" + "="*60)
print("Perturbative scaling analysis")
print("="*60)
frob_norms = np.array([r["frob_norm_delta_K"] for r in results])
lam_arr = np.array([r["lambda"] for r in results])

# Fit log-log for lambda > 0
mask = lam_arr > 0.01
if mask.sum() >= 3:
    log_lam = np.log(lam_arr[mask])
    log_frob = np.log(frob_norms[mask])
    # Linear fit: log(||delta_K||) = p * log(lambda) + const
    coeffs = np.polyfit(log_lam, log_frob, 1)
    print(f"Power law fit: ||delta_K|| ~ lambda^{coeffs[0]:.3f}")
    print(f"(Expected: 2.0 for perturbative O(lambda^2), 1.0 for O(lambda))")

# ============================================================
# Save results
# ============================================================
save_path = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/thermal-time/strategies/strategy-001/explorations/exploration-002/code/sweep_results.json"
with open(save_path, "w") as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved to {save_path}")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"At lambda=0: ||delta_K||_F = {results[0]['frob_norm_delta_K']:.2e} (should be ~0)")
if len(results) > 6:
    print(f"At lambda=0.3: ||delta_K||_F = {results[6]['frob_norm_delta_K']:.6f}")
if len(results) > 10:
    print(f"At lambda=0.5: ||delta_K||_F = {results[10]['frob_norm_delta_K']:.6f}")
