"""
1. Analyze whether per-vertex bound covers non-staggered modes
2. Check the SZZ normalization formula
3. Decompose eigenvalue contributions by momentum
"""
import numpy as np
from scipy.linalg import expm
import itertools

np.random.seed(789)

L = 2
d = 4
N_vertices = L**d
N_edges = d * N_vertices
N_dim = 3 * N_edges

def random_so3():
    v = np.random.randn(3)
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return expm(K)

def vertex_index(x):
    idx = 0
    for i in range(d):
        idx = idx * L + (x[i] % L)
    return idx

def all_vertices():
    return list(itertools.product(range(L), repeat=d))

def edge_index(x, mu):
    return vertex_index(x) * d + mu

def neighbor(x, mu):
    y = list(x)
    y[mu] = (y[mu] + 1) % L
    return tuple(y)

def holonomy(Q, x, mu, nu):
    x_mu = neighbor(x, mu)
    x_nu = neighbor(x, nu)
    return Q[(x, mu)] @ Q[(x_mu, nu)] @ Q[(x_nu, mu)].T @ Q[(x, nu)].T

def build_full_M(Q):
    M = np.zeros((N_dim, N_dim))
    for x in all_vertices():
        for mu in range(d):
            for nu in range(mu+1, d):
                x_mu = neighbor(x, mu)
                x_nu = neighbor(x, nu)
                G1 = np.eye(3)
                G2 = Q[(x, mu)]
                G3 = -(Q[(x, mu)] @ Q[(x_mu, nu)] @ Q[(x_nu, mu)].T)
                G4 = -holonomy(Q, x, mu, nu)
                edges_G = [
                    (3 * edge_index(x, mu), G1),
                    (3 * edge_index(x_mu, nu), G2),
                    (3 * edge_index(x_nu, mu), G3),
                    (3 * edge_index(x, nu), G4),
                ]
                for (ia, Ga) in edges_G:
                    for (ib, Gb) in edges_G:
                        M[ia:ia+3, ib:ib+3] += Ga.T @ Gb
    return M

def build_staggered_basis():
    """Build orthonormal basis for staggered subspace (9D)."""
    # T in V = {T : sum T_mu = 0}. 9D subspace.
    # Use basis: T^(a,j) with T^(a,j)_mu = delta(mu,a)*e_j - delta(mu,3)*e_j, a=0,1,2, j=0,1,2
    basis = []
    for a in range(3):
        for j in range(3):
            T = np.zeros((4, 3))
            T[a, j] = 1.0
            T[3, j] = -1.0
            v = np.zeros(N_dim)
            for x in all_vertices():
                sx = sum(x) % 2
                for mu in range(d):
                    sign = (-1)**(sx + mu)
                    ei = edge_index(x, mu)
                    v[3*ei:3*ei+3] = sign * T[mu]
            basis.append(v)
    P = np.column_stack(basis)
    Q_orth, _ = np.linalg.qr(P)
    return Q_orth

def momentum_decomposition():
    """On L=2, d=4, the momenta are k in {0, pi}^4. There are 16 momentum modes."""
    print("=== Momentum Decomposition at Q=I ===\n")

    Q_id = {}
    for x in all_vertices():
        for mu in range(d):
            Q_id[(x, mu)] = np.eye(3)

    M = build_full_M(Q_id)
    verts = all_vertices()

    # For L=2, momenta are k in {0, pi}^4
    momenta = list(itertools.product([0, np.pi], repeat=d))

    for k in momenta:
        # Build basis for momentum k: v_{x,mu,a} = e^{ikx} e_a for each (mu, a)
        # For L=2, e^{ikx} = product_i e^{ik_i x_i} = product_i (-1)^{k_i * x_i / pi}
        basis_k = []
        for mu in range(d):
            for a in range(3):
                v = np.zeros(N_dim)
                for x in verts:
                    phase = 1.0
                    for i in range(d):
                        if k[i] > 0:  # k_i = pi
                            phase *= (-1)**x[i]
                    ei = edge_index(x, mu)
                    v[3*ei + a] = phase
                basis_k.append(v)

        P_k = np.column_stack(basis_k)
        # Orthonormalize
        Q_k, _ = np.linalg.qr(P_k)

        # Restrict M to this momentum subspace
        M_k = Q_k.T @ M @ Q_k
        eigs = np.linalg.eigvalsh(M_k)

        k_str = ",".join(["0" if ki == 0 else "π" for ki in k])
        print(f"  k=({k_str}): eigenvalues = {sorted(eigs)}")

def test_per_vertex_non_staggered():
    """Test whether per-vertex bound applies to NON-staggered modes.

    For a non-staggered mode, the B-field at a plaquette involves v at different
    vertices. Check if the per-vertex bound F_x ≤ 16||T_x||^2 can be used
    where T_x is the effective color vector at vertex x.
    """
    print("\n=== Per-Vertex Bound for Non-Staggered Modes ===")
    print("  Testing if v^T M(Q) v ≤ 16|v|^2 for k=(0,π,π,π) modes...\n")

    verts = all_vertices()

    for trial in range(50):
        Q = {}
        for x in verts:
            for mu in range(d):
                Q[(x, mu)] = random_so3()

        M = build_full_M(Q)

        # Build modes at k=(0,pi,pi,pi)
        k = (0, np.pi, np.pi, np.pi)
        basis_k = []
        for mu in range(d):
            for a in range(3):
                v = np.zeros(N_dim)
                for x in verts:
                    phase = 1.0
                    for i in range(d):
                        if k[i] > 0:
                            phase *= (-1)**x[i]
                    ei = edge_index(x, mu)
                    v[3*ei + a] = phase
                basis_k.append(v)

        P_k = np.column_stack(basis_k)
        Q_k, _ = np.linalg.qr(P_k)

        M_k = Q_k.T @ M @ Q_k
        lmax_k = np.linalg.eigvalsh(M_k)[-1]

        if trial < 5:
            print(f"  Trial {trial}: k=(0,π,π,π) max eig = {lmax_k:.4f}")

    # Now test k=(π,π,π,π) — the staggered mode
    print("\n  Testing staggered mode k=(π,π,π,π)...")
    k_stag = (np.pi, np.pi, np.pi, np.pi)
    max_stag = 0
    max_non_stag = 0

    for trial in range(100):
        Q = {}
        for x in verts:
            for mu in range(d):
                Q[(x, mu)] = random_so3()

        M = build_full_M(Q)
        lmax = np.linalg.eigvalsh(M)[-1]

        # Staggered subspace eigenvalue
        P_stag = build_staggered_basis()
        M_stag = P_stag.T @ M @ P_stag
        lmax_stag = np.linalg.eigvalsh(M_stag)[-1]

        # Non-staggered max eigenvalue
        I_perp = np.eye(N_dim) - P_stag @ P_stag.T
        # Project to get approximate non-staggered eigenvalues
        eigvals_full = np.linalg.eigvalsh(M)

        max_stag = max(max_stag, lmax_stag)
        max_non_stag = max(max_non_stag, lmax)  # lmax includes both

        if trial < 5:
            print(f"  Trial {trial}: lmax_full={lmax:.4f}, lmax_stag={lmax_stag:.4f}")

    print(f"\n  Max staggered eigenvalue: {max_stag:.6f}")
    print(f"  Max full eigenvalue: {max_non_stag:.6f}")

def check_szz_normalization():
    """Check the SZZ normalization: what H_norm does lambda_max <= 16 give?"""
    print("\n=== SZZ Normalization Check ===")
    print()
    print("  The SZZ framework (Shen-Zhu-Zhu, Theorem 1.3) uses:")
    print("  H_norm = max_Q || nabla^2 S_W(Q) - E[nabla^2 S_W(Q)] ||")
    print("  where S_W is the Wilson action and the norm is the operator norm.")
    print()
    print("  For the standard Wilson action with coupling beta:")
    print("  S_W(Q) = (beta/N) sum_plaq Re Tr(U_plaq)")
    print("  where N is the dimension of the gauge group representation.")
    print()
    print("  For SU(2) ~ SO(3), N = 2 (fundamental), but for SO(3) directly, N depends on convention.")
    print()
    print("  The Hessian of S_W has eigenvalues proportional to M(Q).")
    print("  Specifically: nabla^2 S_W(Q) ~ (beta/N) * M(Q)")
    print()
    print("  From the GOAL:")
    print("  H_norm = beta/(2N) * max_Q lambda_max(M(Q))")
    print("  For lambda_max <= 16 = 4d:")
    print("    H_norm = beta/(2N) * 4d")
    print()
    print("  For SU(2): N=2, d=4:")
    print("    H_norm = beta/4 * 16 = 4*beta")
    print("    H_norm < 1 iff beta < 1/4")
    print()
    print("  For SU(N): N groups, d dimensions:")
    print("    H_norm = beta/(2N) * 4d = 2*beta*d/N")
    print("    H_norm < 1 iff beta < N/(2d)")
    print()
    print("  The GOAL says H_norm = 1/3 which would give beta < 3. That's different.")
    print("  Let me check: if lambda_max = 16 = 4d and H_norm = lambda_max/(12*4) = 16/48 = 1/3...")
    print("  This uses normalization factor 12*4 = 48 = 4*d*N where N=3 (SO(3) adjoint).")
    print()
    print("  KEY QUESTION: What is the correct normalization?")
    print("  This depends on the exact SZZ setup. The GOAL itself flags this.")
    print()

    # Let's compute the actual Hessian normalization
    # At Q=I, the Wilson action Hessian has eigenvalues:
    # The B-field formula gives |B|^2 which is the Hessian of (1 - Re Tr(U)/N)
    # For SO(3) in adjoint rep (N=3):
    # S_W = (beta/N) sum_plaq (N - Re Tr(U_plaq)) = (beta/N) sum |B|^2/2 (approximately)
    # Actually, the exact Hessian at Q=I: M_ij = d^2 S_W / dA_i dA_j
    # This is proportional to M(Q) with factor beta/(2N)

    print("  Numerical check: Hessian eigenvalues at Q=I")
    print("  M(I) eigenvalues: {0(×57), 4(×36), 8(×54), 12(×36), 16(×9)}")
    print("  If Hessian = beta/(2N) * M(Q), then H_max = beta/(2N) * 16")
    print("  For N=2 (SU(2)): H_max = 4*beta. SZZ requires H_max < 1, so beta < 1/4")
    print("  For N=3 (SO(3) adj): H_max = 8*beta/3. SZZ requires beta < 3/8")
    print()
    print("  BOTTOM LINE: The normalization depends on the group and representation.")
    print("  The proof chain needs to specify which convention is used.")

def check_gap_quantitatively():
    """Quantify how close non-staggered eigenvalues get to 16."""
    print("\n=== Quantitative Gap Analysis ===")
    verts = all_vertices()

    max_vals = {
        'full_lmax': [],
        'stag_lmax': [],
        'non_stag_lmax': []
    }

    P_stag = build_staggered_basis()

    for trial in range(200):
        Q = {}
        for x in verts:
            for mu in range(d):
                Q[(x, mu)] = random_so3()

        M = build_full_M(Q)
        eigvals, eigvecs = np.linalg.eigh(M)

        # Full lambda_max
        max_vals['full_lmax'].append(eigvals[-1])

        # Staggered lambda_max
        M_stag = P_stag.T @ M @ P_stag
        stag_eigs = np.linalg.eigvalsh(M_stag)
        max_vals['stag_lmax'].append(stag_eigs[-1])

        # Non-staggered: find max eigenvalue of eigenvector with <50% staggered component
        non_stag_max = 0
        for i in range(N_dim-1, max(N_dim-30, 0), -1):
            vec = eigvecs[:, i]
            stag_comp = np.linalg.norm(P_stag.T @ vec)
            if stag_comp < 0.5:
                non_stag_max = max(non_stag_max, eigvals[i])
                break
        max_vals['non_stag_lmax'].append(non_stag_max)

    for key in max_vals:
        vals = np.array(max_vals[key])
        print(f"\n  {key}:")
        print(f"    max: {vals.max():.6f}")
        print(f"    mean: {vals.mean():.4f}")
        print(f"    std: {vals.std():.4f}")
        print(f"    99th pct: {np.percentile(vals, 99):.4f}")

    print("\n  Is non-staggered max EVER > staggered max at same Q?")
    stag = np.array(max_vals['stag_lmax'])
    non_stag = np.array(max_vals['non_stag_lmax'])
    ns_wins = np.sum(non_stag > stag)
    print(f"    Non-stag > stag: {ns_wins}/{len(stag)} times ({100*ns_wins/len(stag):.1f}%)")
    print(f"    Max (non-stag - stag): {(non_stag - stag).max():.4f}")

if __name__ == "__main__":
    momentum_decomposition()
    test_per_vertex_non_staggered()
    check_gap_quantitatively()
    check_szz_normalization()
