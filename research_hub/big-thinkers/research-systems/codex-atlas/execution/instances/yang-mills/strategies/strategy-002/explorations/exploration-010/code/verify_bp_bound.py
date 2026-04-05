"""
verify_bp_bound.py — Verify the intermediate B_P bound:
  sum_P |B_P(Q,v)|^2 <= 4d |v|^2
for the max eigenvector v at various Q configurations.

If this bound holds, combined with H_P <= (beta/(2N))|B_P|^2,
it gives lambda_max <= 2d*beta/N = 4*beta.
"""
import numpy as np
import sys
sys.path.insert(0, '.')
from scan_hessian import (
    plaquettes, n_links, n_gen, n_dof, n_plaq, tau, I2,
    su2_dagger, random_su2, config_identity, config_random,
    config_perturbed_identity, compute_hessian, d, beta, N_SU
)

def compute_BP(Q, plaq, v_vec):
    """
    Compute B_P = Ã_0 + Ã_1 + Ã_2 + Ã_3 for plaquette P.

    v_vec: shape (n_dof,) — tangent vector, reshaped as (n_links, n_gen)
    Returns B_P as a 2x2 matrix in su(2).
    """
    links = [plaq[k][0] for k in range(4)]
    signs = [plaq[k][1] for k in range(4)]

    # Extract v_l as su(2) elements
    def get_v(l):
        """Get tangent vector at link l as 2x2 su(2) matrix."""
        return sum(v_vec[l * n_gen + a] * tau[a] for a in range(n_gen))

    # Build the transport matrices: G_k = W_0 W_1 ... W_{k-1}
    # For the B_P formula:
    #   Ã_0 = v_{l_0}
    #   Ã_1 = G_1 v_{l_1} G_1^{-1}  where G_1 = Q_{l_0}
    #   Ã_2 = -G_2 v_{l_2} G_2^{-1}  where G_2 = Q_{l_0} Q_{l_1}
    #   Ã_3 = -G_3 v_{l_3} G_3^{-1}  where G_3 = Q_{l_0} Q_{l_1} Q_{l_2}^{-1}

    # Transport matrices (accumulated products)
    G = [I2.copy()]
    # G[k] = product of first k "link matrices" in plaquette order
    for k in range(4):
        l, s = plaq[k]
        if s == +1:
            G.append(G[-1] @ Q[l])
        else:
            G.append(G[-1] @ su2_dagger(Q[l]))
    # G[0] = I, G[1] = W_0, G[2] = W_0 W_1, G[3] = W_0 W_1 W_2, G[4] = U_P

    # Compute Ã_k
    def adjoint(G_k, v):
        """Compute Ad_{G_k}(v) = G_k v G_k^{-1}."""
        return G_k @ v @ su2_dagger(G_k)

    B_P = np.zeros((2, 2), dtype=complex)
    for k in range(4):
        v_k = get_v(links[k])
        Atilde_k = adjoint(G[k], v_k)
        if signs[k] == +1:
            B_P += Atilde_k
        else:
            B_P -= Atilde_k

    return B_P

def su2_norm_sq(A):
    """Compute |A|^2 = -2 Tr(A^2) for A in su(2)."""
    return -2.0 * np.real(np.trace(A @ A))

def compute_BP_sum(Q, v_vec):
    """Compute sum_P |B_P(Q,v)|^2."""
    total = 0.0
    for plaq in plaquettes:
        B = compute_BP(Q, plaq, v_vec)
        total += su2_norm_sq(B)
    return total

def compute_v_norm_sq(v_vec):
    """Compute |v|^2 = sum_l |v_l|^2 where |v_l|^2 = sum_a (v_l^a)^2 * |tau_a|^2."""
    # |tau_a|^2 = -2 Tr(tau_a^2) = -2*(-1/2) = 1
    # So |v_l|^2 = sum_a (v_l^a)^2 * 1 = sum_a (v_l^a)^2
    return np.sum(v_vec**2)

# ============================================================
# Main verification
# ============================================================
print("=" * 60)
print("B_P Bound Verification")
print(f"Bound: sum_P |B_P|^2 <= 4d |v|^2 = {4*d} |v|^2")
print("=" * 60)

configs = [
    ("Q=I", config_identity()),
]

np.random.seed(42)
for i in range(5):
    configs.append((f"random-{i}", config_random()))

for eps in [0.01, 0.1, 0.5, 1.0]:
    configs.append((f"perturb-eps={eps}", config_perturbed_identity(eps)))

print(f"\n{'Config':<20} {'lambda_max':>10} {'BP_ratio':>10} {'4d':>5} {'Saturated?':>12}")
print("-" * 60)

for label, Q in configs:
    H = compute_hessian(Q)
    eigvals, eigvecs = np.linalg.eigh(H)
    lam_max = eigvals[-1]
    v_max = eigvecs[:, -1]  # Max eigenvector

    BP_sum = compute_BP_sum(Q, v_max)
    v_nsq = compute_v_norm_sq(v_max)
    BP_ratio = BP_sum / v_nsq

    saturated = "YES" if abs(BP_ratio - 4*d) < 0.1 else "no"
    exceeds = " ***EXCEEDS***" if BP_ratio > 4*d + 1e-6 else ""

    print(f"{label:<20} {lam_max:10.4f} {BP_ratio:10.4f} {4*d:5d} {saturated:>12}{exceeds}")

# Also test with random v (not just the eigenvector)
print("\n--- Testing with random v vectors at various Q ---")
max_ratio = 0.0
for trial in range(100):
    Q = config_random() if trial < 50 else config_perturbed_identity(np.random.uniform(0.01, 2.0))
    v = np.random.randn(n_dof)
    v /= np.linalg.norm(v)

    BP_sum = compute_BP_sum(Q, v)
    v_nsq = compute_v_norm_sq(v)
    ratio = BP_sum / v_nsq

    if ratio > max_ratio:
        max_ratio = ratio

print(f"Max BP_ratio over 100 random (Q, v) pairs: {max_ratio:.4f} (bound: {4*d})")
if max_ratio > 4*d:
    print("*** B_P BOUND VIOLATED! ***")
else:
    print(f"B_P bound holds. Gap: {4*d - max_ratio:.4f}")

print("\nDone.")
