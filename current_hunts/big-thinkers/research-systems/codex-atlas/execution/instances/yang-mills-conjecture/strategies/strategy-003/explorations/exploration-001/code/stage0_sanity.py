"""
Stage 0: Sanity check for M(Q) implementation.
L=2, d=4 hypercubic torus with SU(2) gauge group.

Validates:
1. Q=I gives lambda_max = 16 (multiplicity 9), next eigenvalue = 12
2. Finite-difference check of v^T M(Q) v vs B-field formula
"""

import numpy as np
from scipy.linalg import eigh
np.set_printoptions(precision=10)

# ============================================================
# SU(2) and Adjoint Representation
# ============================================================

def random_su2():
    """Random SU(2) element as 2x2 complex matrix."""
    # Haar-random: use quaternion parameterization
    v = np.random.randn(4)
    v /= np.linalg.norm(v)
    a, b, c, d = v
    return np.array([[a + 1j*b, c + 1j*d],
                     [-c + 1j*d, a - 1j*b]])

def su2_inv(Q):
    """Inverse of SU(2) matrix = conjugate transpose."""
    return Q.conj().T

def adjoint_rep(Q):
    """
    Compute the 3x3 SO(3) adjoint representation matrix of Q in SU(2).
    [Ad_Q]_{ij} = (1/2) Tr(sigma_i Q sigma_j Q^{-1})
    Maps su(2) ~ R^3 to su(2) ~ R^3.
    """
    sigma = [
        np.array([[0, 1], [1, 0]], dtype=complex),      # sigma_1
        np.array([[0, -1j], [1j, 0]], dtype=complex),    # sigma_2
        np.array([[1, 0], [0, -1]], dtype=complex),      # sigma_3
    ]
    Qinv = su2_inv(Q)
    Ad = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            Ad[i, j] = 0.5 * np.real(np.trace(sigma[i] @ Q @ sigma[j] @ Qinv))
    return Ad

def adjoint_action(Q, v):
    """Ad_Q(v) for v in R^3, returns R^3."""
    return adjoint_rep(Q) @ v

# ============================================================
# Lattice Setup: L=2, d=4 periodic hypercubic lattice
# ============================================================

L = 2
d = 4
num_sites = L**d  # 16
num_edges = d * num_sites  # 64
num_plaquettes = d * (d - 1) // 2 * num_sites  # 6 * 16 = 96

def site_index(coords):
    """Convert d-dimensional coordinates (mod L) to linear index."""
    idx = 0
    for i in range(d):
        idx = idx * L + (coords[i] % L)
    return idx

def index_to_coords(idx):
    """Convert linear index to d-dimensional coordinates."""
    coords = []
    for i in range(d):
        coords.append(idx % L)
        idx //= L
    return list(reversed(coords))

def edge_index(site_idx, mu):
    """Edge index for the edge starting at site_idx in direction mu."""
    return site_idx * d + mu

def neighbor(site_idx, mu, direction=1):
    """Neighbor of site_idx in direction mu (+1 or -1), with periodic BC."""
    coords = index_to_coords(site_idx)
    coords[mu] = (coords[mu] + direction) % L
    return site_index(coords)

# ============================================================
# Plaquettes
# ============================================================

def get_plaquettes():
    """
    Return list of plaquettes. Each plaquette is a list of 4 (edge_idx, orientation) pairs.
    orientation = +1 means forward (use Q_e), -1 means backward (use Q_e^{-1}).

    Plaquette at site x in the (mu, nu) plane (mu < nu):
    Path: x -> x+mu -> x+mu+nu -> x+nu -> x
    Edges: (x,mu)+, (x+mu,nu)+, (x+nu,mu)-, (x,nu)-

    Wait - let me be more careful. The standard plaquette is:
    U_□ = Q_{x,mu} Q_{x+mu,nu} Q_{x+nu,mu}^{-1} Q_{x,nu}^{-1}

    So the 4 oriented edges traversed in order are:
    e1 = (x, mu) forward
    e2 = (x+mu, nu) forward
    e3 = (x+nu, mu) forward but traversed BACKWARD -> inverse
    e4 = (x, nu) forward but traversed BACKWARD -> inverse
    """
    plaquettes = []
    for x in range(num_sites):
        for mu in range(d):
            for nu in range(mu + 1, d):
                x_mu = neighbor(x, mu)
                x_nu = neighbor(x, nu)

                e1 = edge_index(x, mu)        # forward
                e2 = edge_index(x_mu, nu)     # forward
                e3 = edge_index(x_nu, mu)     # backward (traversed in -mu direction)
                e4 = edge_index(x, nu)        # backward (traversed in -nu direction)

                plaquettes.append([(e1, +1), (e2, +1), (e3, -1), (e4, -1)])
    return plaquettes

PLAQUETTES = get_plaquettes()
assert len(PLAQUETTES) == num_plaquettes, f"Expected {num_plaquettes} plaquettes, got {len(PLAQUETTES)}"

# ============================================================
# B-field computation
# ============================================================

def compute_holonomy(Q, plaq):
    """Compute U_□ = Q_{e1} Q_{e2} Q_{e3}^{-1} Q_{e4}^{-1}."""
    U = np.eye(2, dtype=complex)
    for (e, orient) in plaq:
        if orient == +1:
            U = U @ Q[e]
        else:
            U = U @ su2_inv(Q[e])
    return U

def compute_B_plaq(Q, v, plaq):
    """
    Compute B_□(Q, v) for a single plaquette.

    B_□ = v_{e1} + Ad_{Q_{e1}}(v_{e2}) - Ad_{Q_{e1}Q_{e2}Q_{e3}^{-1}}(v_{e3}) - Ad_{U_□}(v_{e4})

    where U_□ = Q_{e1} Q_{e2} Q_{e3}^{-1} Q_{e4}^{-1}

    The partial holonomies along the path are:
    After e1: Q_{e1}
    After e2: Q_{e1} Q_{e2}
    After e3: Q_{e1} Q_{e2} Q_{e3}^{-1}
    After e4: Q_{e1} Q_{e2} Q_{e3}^{-1} Q_{e4}^{-1} = U_□

    The B-field formula with adjoint: each v_{ei} is conjugated by the partial
    holonomy UP TO (but not including?) that edge...

    Let me re-derive. The linearization of U_□ gives:
    δU_□ = Σ_i (partial holonomy before e_i) · δQ_{ei} · (partial holonomy after e_i)

    For the action S = -(β/2N) Σ_□ Tr(U_□ + U_□†), the Hessian involves B_□^T B_□ terms.

    Standard result: B_□(Q, v) for edge perturbation v_e · σ_a (in Lie algebra):

    Term for edge e_i in plaquette:
    - sign_i * Ad_{H_i}(v_{e_i})
    where H_i is the partial holonomy from the START of the plaquette to the START of edge e_i,
    and sign_i = +1 for forward edges, -1 for backward edges.

    Wait, let me think again more carefully about the standard derivation.
    """
    (e1, o1), (e2, o2), (e3, o3), (e4, o4) = plaq

    # Partial holonomies (from start of path to start of each edge)
    # Before e1: identity
    H1 = np.eye(2, dtype=complex)
    # Before e2: Q_{e1}
    H2 = Q[e1]
    # Before e3: Q_{e1} Q_{e2}
    H3 = Q[e1] @ Q[e2]
    # Before e4: Q_{e1} Q_{e2} Q_{e3}^{-1}
    H4 = Q[e1] @ Q[e2] @ su2_inv(Q[e3])

    # Ad action of partial holonomies on corresponding v vectors
    # For forward edges: +Ad_{H_i}(v_{e_i})
    # For backward edges: -Ad_{H_i}(v_{e_i})
    B = np.zeros(3)
    B += o1 * adjoint_action(H1, v[e1])  # +v_{e1} (H1 = I, o1 = +1)
    B += o2 * adjoint_action(H2, v[e2])  # +Ad_{Q_{e1}}(v_{e2})
    B += o3 * adjoint_action(H3, v[e3])  # -Ad_{Q_{e1}Q_{e2}}(v_{e3})
    B += o4 * adjoint_action(H4, v[e4])  # -Ad_{Q_{e1}Q_{e2}Q_{e3}^{-1}}(v_{e4})

    return B

def compute_vMv(Q, v):
    """Compute v^T M(Q) v = Σ_□ |B_□(Q, v)|²."""
    total = 0.0
    for plaq in PLAQUETTES:
        B = compute_B_plaq(Q, v, plaq)
        total += np.dot(B, B)
    return total

def build_M(Q):
    """Build the full M(Q) matrix (3*num_edges x 3*num_edges)."""
    dim = 3 * num_edges
    M = np.zeros((dim, dim))

    for plaq in PLAQUETTES:
        # For each plaquette, compute contribution to M
        # B_□(Q, v) = Σ_i sign_i * Ad_{H_i} @ v_{e_i}
        # |B_□|² = B^T B, which gives a contribution to M

        (e1, o1), (e2, o2), (e3, o3), (e4, o4) = plaq

        H1 = np.eye(2, dtype=complex)
        H2 = Q[e1]
        H3 = Q[e1] @ Q[e2]
        H4 = Q[e1] @ Q[e2] @ su2_inv(Q[e3])

        # The 3x3 blocks: sign_i * Ad_{H_i}
        edges = [e1, e2, e3, e4]
        signs = [o1, o2, o3, o4]
        Hs = [H1, H2, H3, H4]

        blocks = []
        for k in range(4):
            blocks.append(signs[k] * adjoint_rep(Hs[k]))

        # M contribution: for each pair (i,j),
        # M[3*e_i:3*e_i+3, 3*e_j:3*e_j+3] += blocks[i]^T @ blocks[j]
        for i in range(4):
            for j in range(4):
                ei = edges[i]
                ej = edges[j]
                M[3*ei:3*ei+3, 3*ej:3*ej+3] += blocks[i].T @ blocks[j]

    return M

# ============================================================
# Stage 0a: Q = I validation
# ============================================================

print("=" * 60)
print("STAGE 0a: Q = Identity validation")
print("=" * 60)

Q_identity = [np.eye(2, dtype=complex) for _ in range(num_edges)]
M_id = build_M(Q_identity)

# Check symmetry
asym = np.max(np.abs(M_id - M_id.T))
print(f"Asymmetry of M(I): {asym:.2e}")

# Eigenvalues
eigvals = np.sort(eigh(M_id, eigvals_only=True))[::-1]

print(f"\nTop 20 eigenvalues of M(I):")
for i in range(min(20, len(eigvals))):
    print(f"  λ_{i+1} = {eigvals[i]:.10f}")

print(f"\nλ_max = {eigvals[0]:.10f}")
print(f"Expected: 16.0")
print(f"Match: {abs(eigvals[0] - 16.0) < 1e-8}")

# Count multiplicity of top eigenvalue
mult_16 = np.sum(np.abs(eigvals - 16.0) < 1e-6)
print(f"\nMultiplicity of λ=16: {mult_16}")
print(f"Expected: 9")

# Next distinct eigenvalue
next_eig = eigvals[np.abs(eigvals - 16.0) > 1e-6][0] if mult_16 < len(eigvals) else None
print(f"\nNext eigenvalue: {next_eig:.10f}")
print(f"Expected: 12.0")

# ============================================================
# Stage 0b: Finite-difference validation of v^T M(Q) v
# ============================================================

print("\n" + "=" * 60)
print("STAGE 0b: Finite-difference validation")
print("=" * 60)

def wilson_action(Q, beta=1.0, N=2):
    """S(Q) = -(beta/N) Σ_□ Re Tr(U_□)."""
    S = 0.0
    for plaq in PLAQUETTES:
        U = compute_holonomy(Q, plaq)
        S -= (beta / N) * np.real(np.trace(U))
    return S

def perturb_link(Q, edge, direction_vec, epsilon):
    """Perturb Q[edge] -> exp(epsilon * A) Q[edge] where A = i*Σ direction_vec[a]*sigma_a/2."""
    sigma = [
        np.array([[0, 1], [1, 0]], dtype=complex),
        np.array([[0, -1j], [1j, 0]], dtype=complex),
        np.array([[1, 0], [0, -1]], dtype=complex),
    ]
    # A = i * Σ_a v_a * sigma_a / 2  (element of su(2))
    A = np.zeros((2, 2), dtype=complex)
    for a in range(3):
        A += 1j * direction_vec[a] * sigma[a] / 2.0

    from scipy.linalg import expm
    expA = expm(epsilon * A)

    Q_new = list(Q)
    Q_new[edge] = expA @ Q[edge]
    return Q_new

np.random.seed(42)

for trial in range(3):
    print(f"\n--- Trial {trial+1} ---")
    # Random configuration
    Q_rand = [random_su2() for _ in range(num_edges)]

    # Random tangent vector v (3 components per edge)
    v_rand = [np.random.randn(3) for _ in range(num_edges)]

    # Method 1: v^T M(Q) v via B-field formula
    vMv_direct = compute_vMv(Q_rand, v_rand)

    # Method 2: v^T M(Q) v via matrix
    M_rand = build_M(Q_rand)
    v_flat = np.concatenate(v_rand)
    vMv_matrix = v_flat @ M_rand @ v_flat

    # Method 3: Finite differences of the action
    # S(Q + εv) ≈ S(Q) + ε·dS + (ε²/2)·d²S
    # d²S/dε² = Hess S(v,v)
    # From GOAL.md: HessS(v,v;Q) = (β/2N) · v^T M(Q) v
    # So v^T M(Q) v = (2N/β) · d²S/dε²

    eps_vals = [1e-4]
    for eps in eps_vals:
        # Perturb ALL edges simultaneously along v
        Q_plus = list(Q_rand)
        Q_minus = list(Q_rand)
        for e in range(num_edges):
            Q_plus = perturb_link(Q_plus, e, v_rand[e], eps)
        for e in range(num_edges):
            Q_minus = perturb_link(Q_minus, e, v_rand[e], -eps)

        # Wait - this doesn't work for simultaneous perturbation.
        # The Hessian is the second derivative of S along a curve.
        # Need to perturb: Q_e(ε) = exp(ε · v_e · σ) · Q_e for ALL edges simultaneously.

        # Actually for non-commuting perturbations, we need to be more careful.
        # Let's do this edge-by-edge for diagonal terms, and verify v^T M v
        # for a single edge perturbation first.

    # Simpler approach: verify for a single-edge perturbation
    e_test = np.random.randint(num_edges)
    dir_test = np.random.randn(3)

    # Make v that's nonzero only at edge e_test
    v_single = [np.zeros(3) for _ in range(num_edges)]
    v_single[e_test] = dir_test.copy()

    vMv_single = compute_vMv(Q_rand, v_single)

    # Finite difference: d²S/dε² where Q_e -> exp(ε·A)·Q_e
    from scipy.linalg import expm
    eps = 1e-5

    Q_p = list(Q_rand)
    Q_m = list(Q_rand)
    sigma = [
        np.array([[0, 1], [1, 0]], dtype=complex),
        np.array([[0, -1j], [1j, 0]], dtype=complex),
        np.array([[1, 0], [0, -1]], dtype=complex),
    ]
    A = np.zeros((2, 2), dtype=complex)
    for a in range(3):
        A += 1j * dir_test[a] * sigma[a] / 2.0

    Q_p[e_test] = expm(eps * A) @ Q_rand[e_test]
    Q_m[e_test] = expm(-eps * A) @ Q_rand[e_test]

    S0 = wilson_action(Q_rand, beta=1.0, N=2)
    Sp = wilson_action(Q_p, beta=1.0, N=2)
    Sm = wilson_action(Q_m, beta=1.0, N=2)

    d2S = (Sp - 2*S0 + Sm) / eps**2

    # HessS(v,v) = (β/2N) * v^T M v
    # So v^T M v = (2N/β) * d²S/dε²
    beta, N = 1.0, 2
    vMv_fd = (2 * N / beta) * d2S

    rel_err = abs(vMv_single - vMv_fd) / max(abs(vMv_single), 1e-15)
    print(f"  Edge {e_test}: vMv_direct = {vMv_single:.10f}, vMv_fd = {vMv_fd:.10f}, rel_err = {rel_err:.2e}")

    # Also verify matrix computation matches direct B-field
    v_single_flat = np.concatenate(v_single)
    vMv_mat = v_single_flat @ M_rand @ v_single_flat
    rel_err2 = abs(vMv_single - vMv_mat) / max(abs(vMv_single), 1e-15)
    print(f"  B-field vs matrix: rel_err = {rel_err2:.2e}")

    # Multi-edge finite difference (do edges one at a time for cross terms)
    # Actually let's just verify the full v^T M v vs direct B-field computation
    rel_err3 = abs(vMv_direct - vMv_matrix) / max(abs(vMv_direct), 1e-15)
    print(f"  Full v: B-field_direct = {vMv_direct:.10f}, matrix = {vMv_matrix:.10f}, rel_err = {rel_err3:.2e}")

print("\n" + "=" * 60)
print("STAGE 0 COMPLETE")
print("=" * 60)
