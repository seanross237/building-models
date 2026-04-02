"""
CRITICAL: Test the upstream connection (Part C).
1. Build the full M(Q) matrix for L=2, d=4 (192x192)
2. Check lambda_max(M(Q)) <= 16 for random Q
3. Check whether max eigenvalue is achieved in staggered subspace
4. Adversarial gradient ascent on lambda_max
5. Check double-counting
"""
import numpy as np
from scipy.linalg import expm
import itertools

np.random.seed(123)

def random_so3():
    v = np.random.randn(3)
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return expm(K)

# ============================================================
# LATTICE SETUP: L=2, d=4
# ============================================================

L = 2
d = 4
N_vertices = L**d  # 16
N_edges = d * N_vertices  # 64
N_dim = 3 * N_edges  # 192

def vertex_index(x):
    """Map d-tuple to vertex index."""
    idx = 0
    for i in range(d):
        idx = idx * L + (x[i] % L)
    return idx

def all_vertices():
    return list(itertools.product(range(L), repeat=d))

def edge_index(x, mu):
    """Edge (x, mu) -> index into the edge list."""
    vi = vertex_index(x)
    return vi * d + mu

def neighbor(x, mu, direction=1):
    """Neighbor of x in direction mu (forward=+1, backward=-1)."""
    y = list(x)
    y[mu] = (y[mu] + direction) % L
    return tuple(y)

def plaquette_edges(x, mu, nu):
    """Return the 4 edges of the plaquette at (x, mu, nu).
    Order: e1=(x,mu), e2=(x+mu_hat,nu), e3=(x+nu_hat,mu), e4=(x,nu)
    e3 and e4 are traversed backward.
    """
    x_plus_mu = neighbor(x, mu)
    x_plus_nu = neighbor(x, nu)
    e1 = (x, mu)          # forward
    e2 = (x_plus_mu, nu)  # forward
    e3 = (x_plus_nu, mu)  # backward
    e4 = (x, nu)          # backward
    return e1, e2, e3, e4

def generate_random_gauge(N_edges):
    """Generate random SO(3) gauge configuration."""
    Q = {}
    for x in all_vertices():
        for mu in range(d):
            Q[(x, mu)] = random_so3()
    return Q

def holonomy(Q, x, mu, nu):
    """Compute plaquette holonomy U = Q_{x,mu} Q_{x+mu,nu} Q_{x+nu,mu}^{-1} Q_{x,nu}^{-1}."""
    x_plus_mu = neighbor(x, mu)
    x_plus_nu = neighbor(x, nu)
    U = Q[(x, mu)] @ Q[(x_plus_mu, nu)] @ Q[(x_plus_nu, mu)].T @ Q[(x, nu)].T
    return U

def Ad(g, v):
    """Adjoint action: Ad_g(v) = g v for SO(3) acting on R^3 (since so(3) ~ R^3)."""
    return g @ v

def build_full_M(Q):
    """Build the full N_dim x N_dim matrix M(Q) = sum_plaq B_plaq^T B_plaq.

    For each plaquette p, B_p is a linear map from R^{N_dim} to R^3.
    B_p(v) = v_{e1} + Ad(Q_{e1}) v_{e2} - Ad(Q_{e1}Q_{e2}Q_{e3}^{-1}) v_{e3} - Ad(U_p) v_{e4}

    where edges are: e1=(x,mu) forward, e2=(x+mu,nu) forward,
    e3=(x+nu,mu) backward, e4=(x,nu) backward.
    """
    M = np.zeros((N_dim, N_dim))

    for x in all_vertices():
        for mu in range(d):
            for nu in range(mu+1, d):
                # Plaquette at (x, mu, nu)
                e1, e2, e3, e4 = plaquette_edges(x, mu, nu)

                # Compute the adjoint matrices
                x_plus_mu = neighbor(x, mu)
                x_plus_nu = neighbor(x, nu)

                G1 = np.eye(3)                              # coefficient of v_{e1}
                G2 = Q[(x, mu)]                             # Ad(Q_{x,mu})
                G3 = -(Q[(x, mu)] @ Q[(x_plus_mu, nu)] @ Q[(x_plus_nu, mu)].T)  # -Ad(Q_{e1}Q_{e2}Q_{e3}^{-1})
                G4 = -holonomy(Q, x, mu, nu)                # -Ad(U_p)

                # Edge indices -> positions in the big vector
                idx1 = 3 * edge_index(e1[0], e1[1])
                idx2 = 3 * edge_index(e2[0], e2[1])
                idx3 = 3 * edge_index(e3[0], e3[1])
                idx4 = 3 * edge_index(e4[0], e4[1])

                # B_p = G1 v_{e1} + G2 v_{e2} + G3 v_{e3} + G4 v_{e4}
                # B_p^T B_p contribution to M:
                edges = [(idx1, G1), (idx2, G2), (idx3, G3), (idx4, G4)]

                for (ia, Ga) in edges:
                    for (ib, Gb) in edges:
                        M[ia:ia+3, ib:ib+3] += Ga.T @ Gb

    return M

def build_staggered_subspace():
    """Build a basis for the staggered subspace.
    v_{x,mu} = (-1)^{|x|+mu} T_mu where T is 4x3 with sum T_mu = 0.

    Returns a N_dim x 9 matrix whose columns span the staggered subspace.
    """
    # Basis for V = {T : sum T_mu = 0}: 9 basis vectors
    # T_0 = e_j, T_1 = -e_j, T_2 = 0, T_3 = 0  (j=0,1,2)
    # T_0 = 0, T_1 = e_j, T_2 = -e_j, T_3 = 0  (j=0,1,2)
    # T_0 = 0, T_1 = 0, T_2 = e_j, T_3 = -e_j  (j=0,1,2)

    basis = []
    for pair_idx, (a, b) in enumerate([(0,1), (1,2), (2,3)]):
        for j in range(3):
            T = np.zeros((4, 3))
            T[a, j] = 1.0
            T[b, j] = -1.0
            # Build the full vector
            v = np.zeros(N_dim)
            for x in all_vertices():
                sx = sum(x) % 2  # |x| mod 2
                for mu in range(d):
                    sign = (-1)**(sx + mu)
                    ei = edge_index(x, mu)
                    v[3*ei:3*ei+3] = sign * T[mu]
            basis.append(v)

    P = np.column_stack(basis)
    # Orthonormalize
    Q, R = np.linalg.qr(P)
    return Q

def test_eigenvalues_at_identity():
    """Check M(I) eigenvalue structure."""
    print("=== Full Matrix at Q=I ===")
    Q_identity = {}
    for x in all_vertices():
        for mu in range(d):
            Q_identity[(x, mu)] = np.eye(3)

    M = build_full_M(Q_identity)

    eigvals = np.linalg.eigvalsh(M)
    eigvals_sorted = np.sort(eigvals)

    print(f"  Eigenvalue range: [{eigvals_sorted[0]:.4f}, {eigvals_sorted[-1]:.4f}]")
    print(f"  lambda_max = {eigvals_sorted[-1]:.6f} (should be 16)")

    # Count eigenvalue multiplicities
    unique_eigs = []
    for ev in eigvals_sorted:
        found = False
        for ue in unique_eigs:
            if abs(ev - ue[0]) < 0.1:
                ue[1] += 1
                found = True
                break
        if not found:
            unique_eigs.append([ev, 1])

    print("  Distinct eigenvalues and multiplicities:")
    for ev, mult in sorted(unique_eigs):
        print(f"    {ev:.2f} (x{mult})")

    ok = abs(eigvals_sorted[-1] - 16.0) < 1e-10
    print(f"  Status: {'VERIFIED' if ok else 'FAILED'}")

    # Check staggered subspace
    P_stag = build_staggered_subspace()
    M_stag = P_stag.T @ M @ P_stag
    stag_eigs = np.linalg.eigvalsh(M_stag)
    print(f"  Staggered eigenvalues: {sorted(stag_eigs)[-3:]}")

    return ok

def test_lambda_max_random(n_configs=300):
    """Test lambda_max(M(Q)) <= 16 for random Q."""
    print(f"\n=== Full Matrix Random Test ({n_configs} configs) ===")

    P_stag = build_staggered_subspace()
    max_lmax = 0
    max_lmax_outside_stag = 0
    violations = 0

    for trial in range(n_configs):
        Q = generate_random_gauge(N_edges)
        M = build_full_M(Q)

        eigvals, eigvecs = np.linalg.eigh(M)
        lmax = eigvals[-1]
        top_vec = eigvecs[:, -1]

        if lmax > 16 + 1e-10:
            violations += 1

        max_lmax = max(max_lmax, lmax)

        # Check if top eigenvector is in staggered subspace
        proj = P_stag @ (P_stag.T @ top_vec)
        proj_norm = np.linalg.norm(proj)
        outside_norm = np.sqrt(max(1 - proj_norm**2, 0))

        # Also check max eigenvalue in complement of staggered subspace
        I_perp = np.eye(N_dim) - P_stag @ P_stag.T
        M_perp = I_perp @ M @ I_perp.T
        # Actually, restrict M to complement
        # Use the complement projector
        eigvals_perp = np.linalg.eigvalsh(M_perp)
        # Filter out near-zero eigenvalues (from the projection)
        non_stag_max = max(ev for ev in eigvals_perp if ev > 0.1)
        max_lmax_outside_stag = max(max_lmax_outside_stag, non_stag_max)

        if trial < 5 or trial == n_configs - 1:
            print(f"  Config {trial}: lmax={lmax:.4f}, stag_proj={proj_norm:.4f}, non-stag max={non_stag_max:.4f}")

    print(f"\n  Max lambda_max: {max_lmax:.6f} (should be <= 16)")
    print(f"  Max non-staggered eigenvalue: {max_lmax_outside_stag:.6f}")
    print(f"  Violations (>16): {violations}/{n_configs}")
    print(f"  Status: {'VERIFIED' if violations == 0 and max_lmax <= 16 + 1e-10 else 'FAILED'}")
    return violations == 0

def test_double_counting():
    """Verify sum_x F_x = v^T M(Q) v for staggered v (no double counting)."""
    print("\n=== Double-Counting Test ===")
    max_err = 0

    for trial in range(100):
        Q = generate_random_gauge(N_edges)
        M = build_full_M(Q)

        T = np.random.randn(4, 3)
        T -= T.mean(axis=0)  # sum = 0

        # Build staggered vector
        v = np.zeros(N_dim)
        for x in all_vertices():
            sx = sum(x) % 2
            for mu in range(d):
                sign = (-1)**(sx + mu)
                ei = edge_index(x, mu)
                v[3*ei:3*ei+3] = sign * T[mu]

        # Global Rayleigh quotient
        global_val = v @ M @ v

        # Sum of per-vertex F_x
        sum_Fx = 0
        for x in all_vertices():
            # Compute F_x: sum over 6 plaquettes at x
            sx = sum(x) % 2
            Fx = 0
            for mu in range(d):
                for nu in range(mu+1, d):
                    # Get gauge variables for plaquette at (x, mu, nu)
                    e1, e2, e3, e4 = plaquette_edges(x, mu, nu)

                    # B_plaq = G1 v_{e1} + G2 v_{e2} + G3 v_{e3} + G4 v_{e4}
                    x_plus_mu = neighbor(x, mu)
                    x_plus_nu = neighbor(x, nu)

                    G1 = np.eye(3)
                    G2 = Q[(x, mu)]
                    G3 = -(Q[(x, mu)] @ Q[(x_plus_mu, nu)] @ Q[(x_plus_nu, mu)].T)
                    G4 = -holonomy(Q, x, mu, nu)

                    # Get v components
                    v1 = v[3*edge_index(e1[0], e1[1]):3*edge_index(e1[0], e1[1])+3]
                    v2 = v[3*edge_index(e2[0], e2[1]):3*edge_index(e2[0], e2[1])+3]
                    v3 = v[3*edge_index(e3[0], e3[1]):3*edge_index(e3[0], e3[1])+3]
                    v4 = v[3*edge_index(e4[0], e4[1]):3*edge_index(e4[0], e4[1])+3]

                    B_vec = G1 @ v1 + G2 @ v2 + G3 @ v3 + G4 @ v4
                    Fx += np.dot(B_vec, B_vec)

            sum_Fx += Fx

        err = abs(global_val - sum_Fx)
        max_err = max(max_err, err)

    print(f"  Max |global - sum_Fx|: {max_err:.2e} (should be < 1e-10)")
    print(f"  Status: {'VERIFIED (no double counting)' if max_err < 1e-10 else 'FAILED (double counting!)'}")
    return max_err < 1e-10

def test_per_vertex_bound_on_full_lattice():
    """Test per-vertex F_x <= 16||T||^2 on the FULL lattice."""
    print("\n=== Per-Vertex Bound on Full Lattice ===")
    max_ratio = 0
    violations = 0
    n_tests = 0

    for trial in range(50):
        Q = generate_random_gauge(N_edges)
        T = np.random.randn(4, 3)
        T -= T.mean(axis=0)
        T_norm_sq = np.sum(T**2)

        for x in all_vertices():
            # Compute F_x using the full B-field formula
            v = np.zeros(N_dim)
            sx = sum(x) % 2
            for mu in range(d):
                sign = (-1)**(sx + mu)
                ei = edge_index(x, mu)
                v[3*ei:3*ei+3] = sign * T[mu]

            Fx = 0
            for mu in range(d):
                for nu in range(mu+1, d):
                    e1, e2, e3, e4 = plaquette_edges(x, mu, nu)
                    x_plus_mu = neighbor(x, mu)
                    x_plus_nu = neighbor(x, nu)

                    G1 = np.eye(3)
                    G2 = Q[(x, mu)]
                    G3 = -(Q[(x, mu)] @ Q[(x_plus_mu, nu)] @ Q[(x_plus_nu, mu)].T)
                    G4 = -holonomy(Q, x, mu, nu)

                    v1 = v[3*edge_index(e1[0], e1[1]):3*edge_index(e1[0], e1[1])+3]
                    v2 = v[3*edge_index(e2[0], e2[1]):3*edge_index(e2[0], e2[1])+3]
                    v3 = v[3*edge_index(e3[0], e3[1]):3*edge_index(e3[0], e3[1])+3]
                    v4 = v[3*edge_index(e4[0], e4[1]):3*edge_index(e4[0], e4[1])+3]

                    B_vec = G1 @ v1 + G2 @ v2 + G3 @ v3 + G4 @ v4
                    Fx += np.dot(B_vec, B_vec)

            ratio = Fx / (16 * T_norm_sq)
            max_ratio = max(max_ratio, ratio)
            if Fx > 16 * T_norm_sq + 1e-10:
                violations += 1
            n_tests += 1

    print(f"  Max F_x / (16||T||^2): {max_ratio:.6f} (should be <= 1)")
    print(f"  Violations: {violations}/{n_tests}")
    print(f"  Status: {'VERIFIED' if violations == 0 else 'FAILED'}")
    return violations == 0

def test_staggered_vs_global_gap():
    """KEY TEST: Can non-staggered modes have Rayleigh quotient > 16?
    At Q=I, non-staggered max eigenvalue = 12. Can this grow above 16?
    """
    print("\n=== CRITICAL: Non-Staggered Eigenvalue Can Exceed 16? ===")

    P_stag = build_staggered_subspace()
    max_non_stag_eig = 0

    for trial in range(200):
        Q = generate_random_gauge(N_edges)
        M = build_full_M(Q)

        eigvals, eigvecs = np.linalg.eigh(M)

        # Find eigenvalues of M restricted to complement of staggered subspace
        # Project out staggered components from eigenvectors
        for i in range(N_dim):
            ev = eigvals[i]
            vec = eigvecs[:, i]
            proj = P_stag.T @ vec
            stag_component = np.linalg.norm(proj)

            # If mostly non-staggered and eigenvalue is high
            if stag_component < 0.5 and ev > max_non_stag_eig:
                max_non_stag_eig = ev

        if trial < 5:
            print(f"  Config {trial}: lmax={eigvals[-1]:.4f}")

    print(f"\n  Max eigenvalue of mostly non-staggered eigenvectors: {max_non_stag_eig:.6f}")
    print(f"  If > 16: PROOF HAS A GAP (non-staggered modes not bounded)")
    print(f"  If <= 12 + epsilon: gap is not a practical problem")
    print(f"  Status: {'SAFE (< 14)' if max_non_stag_eig < 14 else 'CONCERNING' if max_non_stag_eig < 16 else 'COUNTEREXAMPLE!'}")
    return max_non_stag_eig

if __name__ == "__main__":
    print("Building lattice: L=2, d=4, N_dim=192")
    print(f"Vertices: {N_vertices}, Edges: {N_edges}, Plaquettes: {6*N_vertices}\n")

    test_eigenvalues_at_identity()
    no_double_counting = test_double_counting()
    per_vertex_ok = test_per_vertex_bound_on_full_lattice()
    no_violations = test_lambda_max_random(n_configs=200)
    max_non_stag = test_staggered_vs_global_gap()

    print("\n" + "="*60)
    print("UPSTREAM CONNECTION SUMMARY")
    print("="*60)
    print(f"  Double counting: {'No (verified)' if no_double_counting else 'YES (ERROR!)'}")
    print(f"  Per-vertex bound: {'Verified' if per_vertex_ok else 'FAILED'}")
    print(f"  lambda_max(M(Q)) <= 16: {'Verified (200 configs)' if no_violations else 'FAILED'}")
    print(f"  Max non-staggered eigenvalue: {max_non_stag:.4f}")
    if max_non_stag > 16:
        print(f"  *** CRITICAL: Non-staggered modes CAN exceed 16! Proof gap is REAL. ***")
    elif max_non_stag > 14:
        print(f"  *** WARNING: Non-staggered eigenvalues approach 16. Proof gap is concerning. ***")
    else:
        print(f"  Non-staggered eigenvalues well below 16. Proof gap exists but bound likely holds.")
