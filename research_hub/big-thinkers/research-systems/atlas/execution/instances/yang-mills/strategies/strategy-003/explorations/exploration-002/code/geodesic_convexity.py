"""
Geodesic Convexity Analysis for M(Q) = Σ_□ B_□ B_□^T

Tests whether F(t) = λ_max(M(exp(tW))) has F'(0)=0 and F''(0)≤0 for all W.
This would prove Q=I is a local maximum of λ_max(M(Q)).

Setup: L=2, d=4, SU(2), n_alg=3, dim_v = 64*3 = 192
"""

import numpy as np
from numpy.linalg import eigh, eigvalsh, norm
import itertools
from scipy.linalg import expm

# ===== Lattice Setup =====
L = 2
d = 4
n_alg = 3  # dim su(2)

sites = list(itertools.product(range(L), repeat=d))
n_sites = len(sites)  # 16

def site_idx(x):
    return sum(x[i] * L**(d-1-i) for i in range(d))

n_edges = n_sites * d  # 64
dim_v = n_edges * n_alg  # 192

def edge_idx(x, mu):
    return site_idx(x) * d + mu

def full_idx(x, mu, a):
    return edge_idx(x, mu) * n_alg + a

def nbr(x, mu, sign=1):
    x = list(x)
    x[mu] = (x[mu] + sign) % L
    return tuple(x)

# SU(2) generators: τ_a = -iσ_a/2 (anti-Hermitian, satisfy [τ_a,τ_b] = ε_{abc} τ_c)
sigma = [
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex)
]
tau = [-0.5j * s for s in sigma]

# Verify: [τ₀, τ₁] = τ₂
comm01 = tau[0] @ tau[1] - tau[1] @ tau[0]
assert np.allclose(comm01, tau[2]), f"[τ0,τ1]≠τ2: {comm01} vs {tau[2]}"

# Inner product: <A,B> = -2 Re Tr(AB)
def ip(A, B):
    return -2.0 * np.real(np.trace(A @ B))

# Verify: <τ_a, τ_b> = δ_{ab}
for a in range(3):
    for b in range(3):
        expected = 1.0 if a == b else 0.0
        got = ip(tau[a], tau[b])
        assert abs(got - expected) < 1e-12, f"<τ{a},τ{b}> = {got} ≠ {expected}"
print("Inner product verified: <τ_a, τ_b> = δ_{ab} ✓")

# ad_a matrix: [τ_a, τ_b] = Σ_c ad_a[c,b] τ_c
# Structure constants: f_{abc} s.t. [τ_a, τ_b] = f_{abc} τ_c
# For su(2): f_{abc} = ε_{abc}
f_struct = np.zeros((3, 3, 3))
for a in range(3):
    for b in range(3):
        comm = tau[a] @ tau[b] - tau[b] @ tau[a]
        for c in range(3):
            f_struct[a, b, c] = ip(comm, tau[c])
print(f"Structure constants f_012 = {f_struct[0,1,2]:.4f} (should be 1.0)")

# Plaquettes
plaquettes = [(x, mu, nu) for x in sites for mu in range(d) for nu in range(mu+1, d)]
n_plaq = len(plaquettes)
print(f"\nLattice: L={L}, d={d}, sites={n_sites}, edges={n_edges}, plaq={n_plaq}")
print(f"Tangent space dimension: {dim_v}")

def plaq_edges(x, mu, nu):
    """Returns [(site, direction, sign), ...] for the 4 edges"""
    a1 = (x, mu, +1)
    a2 = (nbr(x, mu), nu, +1)
    a3 = (nbr(x, nu), mu, -1)  # backward
    a4 = (x, nu, -1)            # backward
    return [a1, a2, a3, a4]

# ===== Build M(0) = K_curl =====
print("\n--- Building M(0) = K_curl ---")

M0 = np.zeros((dim_v, dim_v))
for x, mu, nu in plaquettes:
    edges_signs = plaq_edges(x, mu, nu)
    for (x1, m1, s1) in edges_signs:
        for (x2, m2, s2) in edges_signs:
            i1 = edge_idx(x1, m1)
            i2 = edge_idx(x2, m2)
            for a in range(n_alg):
                M0[i1*n_alg + a, i2*n_alg + a] += s1 * s2

eigvals_M0, eigvecs_M0 = eigh(M0)
print(f"M(0) max eigenvalue: {eigvals_M0[-1]:.6f} (expected {4*d})")
print(f"M(0) min eigenvalue: {eigvals_M0[0]:.6f}")

# Count eigenvalues near 4d
lambda_max = 4 * d
tol = 1e-8
P_mask = np.abs(eigvals_M0 - lambda_max) < tol
P_dim = np.sum(P_mask)
print(f"Multiplicity of λ_max = {lambda_max}: {P_dim}")
print(f"Top 15 eigenvalues: {eigvals_M0[-15:]}")

# Eigenspace P
P_vecs = eigvecs_M0[:, P_mask]  # shape (dim_v, P_dim)
print(f"\nEigenspace P has dimension {P_dim}")

# ===== Build M'(0)(W) for given W =====

def build_Mprime(W_vec):
    """
    Build M'(0)(W) as a matrix on the tangent space.
    W_vec: shape (n_edges, n_alg) giving W_e = Σ_a W_vec[e,a] τ_a

    M'(0)(W) = Σ_□ [B'_□ ⊗ B_□ + B_□ ⊗ B'_□]

    At Q=I:
    B_□(I,v) = Σ_i s_i v_{a_i} (discrete curl)
    B'_□(0,W,v) = [W_{a₁}, v_{a₂}] - [W_{a₁}+W_{a₂}, v_{a₃}] - [W_{a₁}+W_{a₂}-W_{a₃}, v_{a₄}]

    Both B and B' are linear in v, so M'(0)(W) is the matrix of the bilinear form.
    """
    # Represent W_e as su(2) matrices
    W_mat = [sum(W_vec[e, a] * tau[a] for a in range(n_alg)) for e in range(n_edges)]

    Mprime = np.zeros((dim_v, dim_v))

    for x, mu, nu in plaquettes:
        edges_signs = plaq_edges(x, mu, nu)
        (x1, m1, s1), (x2, m2, s2), (x3, m3, s3), (x4, m4, s4) = edges_signs
        e1 = edge_idx(x1, m1)
        e2 = edge_idx(x2, m2)
        e3 = edge_idx(x3, m3)
        e4 = edge_idx(x4, m4)

        W1 = W_mat[e1]
        W2 = W_mat[e2]
        W3 = W_mat[e3]
        # W4 not needed (a4 has P'4 = W1+W2-W3)

        # Transports that differentiate:
        # P'2(0) = W1
        # P'3(0) = W1+W2
        # P'4(0) = W1+W2-W3 (backward traversal of a3 gives -W3)
        Wtrans2 = W1
        Wtrans3 = W1 + W2
        Wtrans4 = W1 + W2 - W3

        # B_□(I,v) = v_{e1} + v_{e2} - v_{e3} - v_{e4} (as elements of su(2) for each component)
        # B'_□(0,W,v) = [W1, v_{e2}] - [W1+W2, v_{e3}] - [W1+W2-W3, v_{e4}]
        #
        # In components: (B'_□)_c = Σ_b (ad_{Wtrans})_{cb} v_{e_i,b}
        # where ad_{X}_{cb} = f_{c?b} (structure constants)

        # ad_X[c,b] = Σ_a X_a f_{a,b,c} ... wait let me be careful
        # [X, τ_b] = Σ_c (ad_X)_{cb} τ_c
        # X = Σ_a X_a τ_a, so [X, τ_b] = Σ_a X_a [τ_a, τ_b] = Σ_a X_a Σ_c f_{abc} τ_c
        # So (ad_X)_{cb} = Σ_a X_a f_{a,b,c}

        def ad_mat(X_su2):
            """Matrix of ad_X in basis τ_a: (ad_X)_{ca} = Σ_b X_b f_{b,a,c}"""
            # X_su2 is a 2x2 matrix
            # Decompose in τ basis: X_b = <τ_b, X>
            X_coeffs = np.array([ip(tau[b], X_su2) for b in range(n_alg)])
            # (ad_X)_{c,a} = Σ_b X_b f_{b,a,c}
            mat = np.einsum('b,bac->ca', X_coeffs, f_struct)
            return mat

        ad2 = ad_mat(Wtrans2)  # acts on v_{e2}: B'_□ gets + ad2 v_{e2}
        ad3 = ad_mat(Wtrans3)  # acts on v_{e3}: B'_□ gets - ad3 v_{e3}
        ad4 = ad_mat(Wtrans4)  # acts on v_{e4}: B'_□ gets - ad4 v_{e4}

        # B'_□(W,v) is a linear map from v → su(2) component
        # Let B0: shape (n_alg_out, dim_v) be the matrix for B_□(I,v)
        # At Q=I: B_□(I,v)_c = v_{e1,c} + v_{e2,c} - v_{e3,c} - v_{e4,c}
        B0 = np.zeros((n_alg, dim_v))
        B0[:, e1*n_alg:e1*n_alg+n_alg] = np.eye(n_alg) * s1
        B0[:, e2*n_alg:e2*n_alg+n_alg] = np.eye(n_alg) * s2
        B0[:, e3*n_alg:e3*n_alg+n_alg] = np.eye(n_alg) * s3
        B0[:, e4*n_alg:e4*n_alg+n_alg] = np.eye(n_alg) * s4

        # B'_□(W,v)_c = (ad2)_{cb} v_{e2,b} - (ad3)_{cb} v_{e3,b} - (ad4)_{cb} v_{e4,b}
        Bprime = np.zeros((n_alg, dim_v))
        Bprime[:, e2*n_alg:e2*n_alg+n_alg] += ad2
        Bprime[:, e3*n_alg:e3*n_alg+n_alg] -= ad3
        Bprime[:, e4*n_alg:e4*n_alg+n_alg] -= ad4

        # M'(0)(W) += B0^T Bprime + Bprime^T B0 (symmetrized outer product)
        Mprime += B0.T @ Bprime + Bprime.T @ B0

    return Mprime

# ===== Test 1: F'(0) = 0 for random W =====
print("\n--- Test 1: F'(0) = 0 for random W ---")

np.random.seed(42)
F_prime_vals = []
for trial in range(20):
    W_vec = np.random.randn(n_edges, n_alg)
    Mprime = build_Mprime(W_vec)

    # Check (P,P) block
    PP_block = P_vecs.T @ Mprime @ P_vecs  # shape (P_dim, P_dim)
    PP_max_abs = np.max(np.abs(PP_block))

    # Directional derivative = max eigenvalue of PP_block
    eigs_PP = eigvalsh(PP_block)
    F_prime = eigs_PP[-1]

    F_prime_vals.append(F_prime)
    if trial < 5:
        print(f"  Trial {trial+1}: ||PP_block||_max = {PP_max_abs:.2e}, λ_max(PP) = {F_prime:.6f}")

print(f"\nF'(0) max over 20 random W: {max(F_prime_vals):.2e}")
print(f"F'(0) min over 20 random W: {min(F_prime_vals):.2e}")
print(f"F'(0) ≈ 0 for all W: {max(abs(x) for x in F_prime_vals) < 1e-10}")

# ===== Build M''(0)(W) =====
print("\n--- Building M''(0)(W) ---")

def build_Mdprime(W_vec):
    """
    Build M''(0)(W) as a matrix on the tangent space.

    d²/dt² B_□(γ(t), v)|_{t=0} = B''_□(0,W,v):
    - From a₂: [W₁,[W₁,v_{a₂}]]
    - From a₃: -([W₁,[W₁,v_{a₃}]] + 2[W₁,[W₂,v_{a₃}]] + [W₂,[W₂,v_{a₃}]])
    - From a₄: -([W₁,[W₁,v_{a₄}]] + 2[W₁,[W₂,v_{a₄}]] + [W₂,[W₂,v_{a₄}]]
                 - 2[W₁+W₂,[W₃,v_{a₄}]] + [W₃,[W₃,v_{a₄}]])

    d²/dt² ⟨v,M(t)v⟩|_{t=0} = Σ_□ 2[|B'_□|² + ⟨B_□, B''_□⟩]

    So M''(0)(W) = 2 Σ_□ [Bprime^T Bprime + B0^T Bdprime + Bdprime^T B0] / ???

    Wait: d²/dt² ⟨v,Mv⟩ = ⟨v, M'' v⟩ where M'' = d²M/dt².
    d²M/dt² = 2 Σ_□ [Bprime⊗Bprime + B0⊗Bdprime + Bdprime⊗B0]
    But since M(t) = Σ_□ B_□(t)⊗B_□(t) (symmetric outer product),
    M''(0) = Σ_□ 2[Bprime⊗Bprime + B0⊗Bdprime + Bdprime⊗B0]

    Actually: d/dt[A⊗A] = A'⊗A + A⊗A' = 2 sym(A'⊗A)
    d²/dt²[A⊗A] = 2A''⊗A + 2A⊗A'' + 2A'⊗A' + 2A'⊗A' = 2(A''⊗A + A⊗A'') + 4(A'⊗A')
    Wait: d²/dt²[A⊗A] = d/dt[2 A'⊗A] = 2A''⊗A + 2A'⊗A'
    So d²/dt² Σ[B⊗B] = Σ 2(B''⊗B + B⊗B'') + 2(B'⊗B')...

    Let me redo: d/dt[B⊗B] = B'⊗B + B⊗B' (product rule for symmetric outer product)
    d²/dt²[B⊗B] = B''⊗B + B'⊗B' + B'⊗B' + B⊗B'' = B''⊗B + 2B'⊗B' + B⊗B''

    So M''(0) = Σ_□ [B_□''(0) ⊗ B_□(0) + B_□(0) ⊗ B_□''(0) + 2 B_□'(0) ⊗ B_□'(0)]

    As a symmetric matrix: M''(0) = Σ_□ [B0^T Bdprime + Bdprime^T B0 + 2 Bprime^T Bprime]
    (where ⊗ here means the outer product as a symmetric PSD contribution to M)
    """
    W_mat = [sum(W_vec[e, a] * tau[a] for a in range(n_alg)) for e in range(n_edges)]

    def ad_mat(X_su2):
        X_coeffs = np.array([ip(tau[b], X_su2) for b in range(n_alg)])
        mat = np.einsum('b,bac->ca', X_coeffs, f_struct)
        return mat

    Mdprime = np.zeros((dim_v, dim_v))

    for x, mu, nu in plaquettes:
        edges_signs = plaq_edges(x, mu, nu)
        (x1, m1, s1), (x2, m2, s2), (x3, m3, s3), (x4, m4, s4) = edges_signs
        e1 = edge_idx(x1, m1)
        e2 = edge_idx(x2, m2)
        e3 = edge_idx(x3, m3)
        e4 = edge_idx(x4, m4)

        W1 = W_mat[e1]
        W2 = W_mat[e2]
        W3 = W_mat[e3]

        Wtrans2 = W1
        Wtrans3 = W1 + W2
        Wtrans4 = W1 + W2 - W3

        # B'_□ matrices (same as before)
        ad2 = ad_mat(Wtrans2)
        ad3 = ad_mat(Wtrans3)
        ad4 = ad_mat(Wtrans4)

        B0 = np.zeros((n_alg, dim_v))
        B0[:, e1*n_alg:e1*n_alg+n_alg] = np.eye(n_alg) * s1
        B0[:, e2*n_alg:e2*n_alg+n_alg] = np.eye(n_alg) * s2
        B0[:, e3*n_alg:e3*n_alg+n_alg] = np.eye(n_alg) * s3
        B0[:, e4*n_alg:e4*n_alg+n_alg] = np.eye(n_alg) * s4

        Bprime = np.zeros((n_alg, dim_v))
        Bprime[:, e2*n_alg:e2*n_alg+n_alg] += ad2
        Bprime[:, e3*n_alg:e3*n_alg+n_alg] -= ad3
        Bprime[:, e4*n_alg:e4*n_alg+n_alg] -= ad4

        # B''_□ matrix:
        # From a₂: ad_{W1} ∘ ad_{W1} acting on v_{e2}
        # From a₃: -(ad_{W1}² + 2 ad_{W1}ad_{W2} + ad_{W2}²) acting on v_{e3}
        # From a₄: -(ad_{W1}² + 2 ad_{W1}ad_{W2} + ad_{W2}² - 2 ad_{W1+W2}ad_{W3} + ad_{W3}²) acting on v_{e4}

        ad_W1 = ad_mat(W1)
        ad_W2 = ad_mat(W2)
        ad_W3 = ad_mat(W3)
        ad_W12 = ad_mat(W1 + W2)

        # ad² = double commutator matrix
        ad1_sq = ad_W1 @ ad_W1
        ad2_sq = ad_W2 @ ad_W2
        ad3_sq = ad_W3 @ ad_W3
        ad12_ad3 = ad_W12 @ ad_W3

        # Contribution to a₂ (sign +1 in B₀):
        Bdprime_e2 = ad1_sq  # [W1,[W1,v_{e2}]]

        # Contribution to a₃ (sign -1 in B₀):
        Bdprime_e3 = -(ad1_sq + 2 * ad_W1 @ ad_W2 + ad2_sq)

        # Contribution to a₄ (sign -1 in B₀):
        Bdprime_e4 = -(ad1_sq + 2 * ad_W1 @ ad_W2 + ad2_sq - 2 * ad12_ad3 + ad3_sq)

        Bdprime = np.zeros((n_alg, dim_v))
        Bdprime[:, e2*n_alg:e2*n_alg+n_alg] = Bdprime_e2
        Bdprime[:, e3*n_alg:e3*n_alg+n_alg] = Bdprime_e3
        Bdprime[:, e4*n_alg:e4*n_alg+n_alg] = Bdprime_e4

        # M''(0) += B0^T Bdprime + Bdprime^T B0 + 2 Bprime^T Bprime
        Mdprime += B0.T @ Bdprime + Bdprime.T @ B0 + 2 * Bprime.T @ Bprime

    return Mdprime

# ===== Compute H_eff and F''(0) =====
print("\n--- Computing H_eff and F''(0) ---")

# Get eigenvalues/vectors below λ_max
below_P = ~P_mask
lambdas_below = eigvals_M0[below_P]
vecs_below = eigvecs_M0[:, below_P]

print(f"Eigenvalues below λ_max: max={lambdas_below.max():.4f}, gap={lambda_max - lambdas_below.max():.4f}")

def compute_F_double_prime(W_vec, verbose=False):
    """
    Compute F''(0) = 2 λ_max(H_eff) where
    H_eff = (1/2) P M''(0) P + Σ_j (P M'(0) |j⟩⟨j| M'(0) P) / (λ_max - λ_j)
    """
    Mprime = build_Mprime(W_vec)
    Mdprime = build_Mdprime(W_vec)

    # Check F'(0) = 0
    PP = P_vecs.T @ Mprime @ P_vecs
    F_prime_max = eigvalsh(PP)[-1] if P_dim > 1 else (P_vecs.T @ Mprime @ P_vecs)[0,0]

    # H_eff on P
    # Term 1: (1/2) P M''(0) P
    H_direct = 0.5 * P_vecs.T @ Mdprime @ P_vecs

    # Term 2: Level repulsion Σ_j P M'(0) |j⟩⟨j| M'(0) P / (λ_max - λ_j)
    # M'(0) restricted to P→below: shape (below_count, P_dim)
    M_PtoBelow = vecs_below.T @ Mprime @ P_vecs  # shape (n_below, P_dim)

    gaps = lambda_max - lambdas_below  # shape (n_below,)
    # Level repulsion = Σ_j |j⟩⟨j| ... / gap_j
    # As matrix on P: Σ_j (M_PtoBelow[j,:] outer M_PtoBelow[j,:]) / gap_j
    level_repulsion = np.einsum('ji,jk,j->ik', M_PtoBelow, M_PtoBelow, 1.0/gaps)

    H_eff = H_direct + level_repulsion

    eigs_Heff = eigvalsh(H_eff)
    F_double_prime = 2 * eigs_Heff[-1]

    if verbose:
        print(f"  F'(0) max = {F_prime_max:.2e}")
        print(f"  H_direct eigenvalues: {eigs_Heff[:3]}...{eigs_Heff[-3:]}")
        print(f"  λ_max(H_direct) = {eigvalsh(H_direct)[-1]:.6f}")
        print(f"  λ_max(level_repulsion) = {eigvalsh(level_repulsion)[-1]:.6f}")
        print(f"  λ_max(H_eff) = {eigs_Heff[-1]:.6f}")
        print(f"  F''(0) = {F_double_prime:.6f}")

    return F_double_prime, F_prime_max

# Test with specific direction W = (W_{0,0} = τ₁, all others 0)
print("\n[Test A: W = (τ₁ at edge (0,0,...,0, μ=0), others=0)]")
W_vec_A = np.zeros((n_edges, n_alg))
W_vec_A[0, 0] = 1.0  # edge 0, algebra index 0 (τ₀)
F2_A, F1_A = compute_F_double_prime(W_vec_A, verbose=True)

print(f"\n[Test B: W = (τ₁ at edge (0,0,...,0, μ=1), others=0)]")
W_vec_B = np.zeros((n_edges, n_alg))
W_vec_B[1, 1] = 1.0  # edge 1, algebra index 1 (τ₁)
F2_B, F1_B = compute_F_double_prime(W_vec_B, verbose=True)

print(f"\n[Test C: W random small, normalized]")
np.random.seed(7)
W_vec_C = np.random.randn(n_edges, n_alg)
W_vec_C /= norm(W_vec_C)
F2_C, F1_C = compute_F_double_prime(W_vec_C, verbose=True)

# ===== Scan over many random W =====
print("\n--- Scanning F''(0) over 200 random W ---")
np.random.seed(123)
F2_vals = []
F2_max = -np.inf
W_worst = None

for trial in range(200):
    W_vec = np.random.randn(n_edges, n_alg)
    W_vec /= norm(W_vec)
    F2, F1 = compute_F_double_prime(W_vec)
    F2_vals.append(F2)
    if F2 > F2_max:
        F2_max = F2
        W_worst = W_vec.copy()

F2_arr = np.array(F2_vals)
print(f"F''(0) statistics over 200 random W:")
print(f"  max: {F2_arr.max():.6f}")
print(f"  min: {F2_arr.min():.6f}")
print(f"  mean: {F2_arr.mean():.6f}")
print(f"  std: {F2_arr.std():.6f}")
print(f"  All F''(0) ≤ 0: {F2_arr.max() <= 1e-8}")

if F2_arr.max() > 1e-8:
    print(f"\nWARNING: Found F''(0) > 0! Maximum = {F2_arr.max():.6f}")
    print("  This means Q=I is NOT a local max of λ_max(M(Q))")
    # Check worst case
    F2_worst, _ = compute_F_double_prime(W_worst, verbose=True)
else:
    print(f"\nAll F''(0) ≤ 0: Q=I appears to be a LOCAL MAXIMUM ✓")

# ===== Direct numerical verification: F(t) by finite differences =====
print("\n--- Direct numerical F(t) verification ---")

def build_M_at_Q(Q_mats):
    """
    Build M(Q) for given gauge configuration Q_mats[e] ∈ SU(2).
    Returns M as a (dim_v, dim_v) matrix.
    """
    M = np.zeros((dim_v, dim_v))

    for x, mu, nu in plaquettes:
        edges_signs = plaq_edges(x, mu, nu)
        (x1, m1, s1), (x2, m2, s2), (x3, m3, s3), (x4, m4, s4) = edges_signs
        e1 = edge_idx(x1, m1)
        e2 = edge_idx(x2, m2)
        e3 = edge_idx(x3, m3)
        e4 = edge_idx(x4, m4)

        Q1 = Q_mats[e1]
        Q2 = Q_mats[e2]
        Q3 = Q_mats[e3]

        # Holonomies
        P2 = Q1
        P3 = Q1 @ Q2
        P4 = Q1 @ Q2 @ Q3.conj().T

        # B_□ as a matrix: B[c, (e,a)] = contribution to algebra component c
        # B_□(v)_c = v_{e1,c} + (Ad_{P2} v_{e2})_c - (Ad_{P3} v_{e3})_c - (Ad_{P4} v_{e4})_c

        def Ad_mat(G):
            """Matrix of Ad_G in τ basis: (Ad_G)_{ca} = <τ_c, G τ_a G†>"""
            result = np.zeros((n_alg, n_alg))
            for a in range(n_alg):
                Ad_a = G @ tau[a] @ G.conj().T
                for c in range(n_alg):
                    result[c, a] = ip(tau[c], Ad_a)
            return result

        Ad2 = Ad_mat(P2)  # (3,3) matrix
        Ad3 = Ad_mat(P3)
        Ad4 = Ad_mat(P4)

        # Build B_□ as a (n_alg, dim_v) matrix
        B_mat = np.zeros((n_alg, dim_v))
        B_mat[:, e1*n_alg:e1*n_alg+n_alg] = np.eye(n_alg) * s1
        B_mat[:, e2*n_alg:e2*n_alg+n_alg] = Ad2 * s2
        B_mat[:, e3*n_alg:e3*n_alg+n_alg] = Ad3 * s3
        B_mat[:, e4*n_alg:e4*n_alg+n_alg] = Ad4 * s4

        # M += B^T B (outer product contribution)
        M += B_mat.T @ B_mat

    return M

def F_at_t(W_vec_nm, t):
    """Compute F(t) = λ_max(M(exp(tW))) using finite su(2) matrices."""
    W_su2 = [sum(W_vec_nm[e, a] * tau[a] for a in range(n_alg)) for e in range(n_edges)]
    Q_mats = [expm(t * W_su2[e]) for e in range(n_edges)]
    Mt = build_M_at_Q(Q_mats)
    return eigvalsh(Mt)[-1]

# Test finite difference against analytical F''(0)
print("\nFinite difference check for F''(0):")
for label, W_test in [("W_A", W_vec_A), ("W_C (random)", W_vec_C)]:
    F2_ana, _ = compute_F_double_prime(W_test)

    eps = 1e-4
    F_plus = F_at_t(W_test, eps)
    F_zero = F_at_t(W_test, 0.0)
    F_minus = F_at_t(W_test, -eps)

    F2_fd = (F_plus - 2*F_zero + F_minus) / eps**2
    print(f"  {label}: F''(0) analytical={F2_ana:.6f}, finite-diff={F2_fd:.6f}")

# ===== The worst-case direction =====
if W_worst is not None:
    print("\n--- Worst case W analysis ---")
    F2_worst, _ = compute_F_double_prime(W_worst, verbose=True)

    # Verify with finite differences
    eps = 1e-4
    F_plus = F_at_t(W_worst, eps)
    F_zero = F_at_t(W_worst, 0.0)
    F_minus = F_at_t(W_worst, -eps)
    F2_fd_worst = (F_plus - 2*F_zero + F_minus) / eps**2
    print(f"  Worst W: F''(0) analytical={F2_worst:.6f}, finite-diff={F2_fd_worst:.6f}")

# ===== Summary of the H_eff decomposition =====
print("\n--- H_eff decomposition analysis ---")
print("For W = W_C (random):")
Mprime_C = build_Mprime(W_vec_C)
Mdprime_C = build_Mdprime(W_vec_C)

H_direct = 0.5 * P_vecs.T @ Mdprime_C @ P_vecs
M_PtoBelow_C = vecs_below.T @ Mprime_C @ P_vecs
gaps = lambda_max - lambdas_below
level_repulsion_C = np.einsum('ji,jk,j->ik', M_PtoBelow_C, M_PtoBelow_C, 1.0/gaps)
H_eff_C = H_direct + level_repulsion_C

print(f"  λ_max(H_direct) = {eigvalsh(H_direct)[-1]:.6f} (decoherence)")
print(f"  λ_max(level_repulsion) = {eigvalsh(level_repulsion_C)[-1]:.6f} (level repulsion)")
print(f"  λ_max(H_eff) = {eigvalsh(H_eff_C)[-1]:.6f}")
print(f"  Ratio (decoherence/repulsion at max eigvec): ?")

# E001 reported decoherence dominates repulsion by 2-3x. Check here.
evals_direct = eigvalsh(H_direct)
evals_repulsion = eigvalsh(level_repulsion_C)
print(f"  H_direct eigenvalues: {evals_direct}")
print(f"  Level repulsion eigenvalues: {evals_repulsion}")

# ===== Broader analysis: single-edge vs multi-edge =====
print("\n--- Single-edge vs multi-edge W comparison ---")
F2_single_edge = []
F2_multi_edge = []

# Single edge perturbations
for e in range(min(n_edges, 20)):
    for a in range(n_alg):
        W_se = np.zeros((n_edges, n_alg))
        W_se[e, a] = 1.0
        F2, _ = compute_F_double_prime(W_se)
        F2_single_edge.append(F2)

print(f"Single-edge W:")
print(f"  max F''(0) = {max(F2_single_edge):.6f}")
print(f"  min F''(0) = {min(F2_single_edge):.6f}")
print(f"  mean F''(0) = {np.mean(F2_single_edge):.6f}")

# Multi-edge (random)
np.random.seed(999)
for trial in range(50):
    W_me = np.random.randn(n_edges, n_alg)
    W_me /= norm(W_me)
    F2, _ = compute_F_double_prime(W_me)
    F2_multi_edge.append(F2)

print(f"Multi-edge (random) W:")
print(f"  max F''(0) = {max(F2_multi_edge):.6f}")
print(f"  min F''(0) = {min(F2_multi_edge):.6f}")

# ===== Final summary =====
print("\n===== SUMMARY =====")
print(f"Multiplicity of λ_max={lambda_max}: {P_dim}")
print(f"F'(0) = 0 for all tested W: {max(abs(x) for x in F_prime_vals) < 1e-8}")
print(f"F''(0) range: [{F2_arr.min():.4f}, {F2_arr.max():.4f}]")
print(f"Q=I is a local max of λ_max(M(Q)): {F2_arr.max() < 0}")
if F2_arr.max() < 0:
    print("  → Geodesic concavity at Q=I CONFIRMED")
else:
    print(f"  → WARNING: F''(0) = {F2_arr.max():.4f} > 0 for some W!")
