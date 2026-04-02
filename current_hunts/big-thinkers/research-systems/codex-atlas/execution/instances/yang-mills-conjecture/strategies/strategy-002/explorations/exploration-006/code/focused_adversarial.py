"""
Focused adversarial: try to maximize the NON-staggered eigenvalue of M(Q).
Also check odd L (L=3).
"""
import numpy as np
from scipy.linalg import expm
import itertools

np.random.seed(999)

def random_so3():
    v = np.random.randn(3)
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return expm(K)

def build_lattice(L, d):
    N_vertices = L**d
    N_edges = d * N_vertices
    N_dim = 3 * N_edges

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

    return N_vertices, N_edges, N_dim, vertex_index, all_vertices, edge_index, neighbor

def build_full_M(Q, L, d):
    N_v, N_e, N_dim, vi, all_v, ei, nb = build_lattice(L, d)
    M = np.zeros((N_dim, N_dim))
    verts = all_v()

    for x in verts:
        for mu in range(d):
            for nu in range(mu+1, d):
                x_mu = nb(x, mu)
                x_nu = nb(x, nu)

                G1 = np.eye(3)
                G2 = Q[(x, mu)]
                G3 = -(Q[(x, mu)] @ Q[(x_mu, nu)] @ Q[(x_nu, mu)].T)
                U = Q[(x, mu)] @ Q[(x_mu, nu)] @ Q[(x_nu, mu)].T @ Q[(x, nu)].T
                G4 = -U

                edges_G = [
                    (3 * ei(x, mu), G1),
                    (3 * ei(x_mu, nu), G2),
                    (3 * ei(x_nu, mu), G3),
                    (3 * ei(x, nu), G4),
                ]
                for (ia, Ga) in edges_G:
                    for (ib, Gb) in edges_G:
                        M[ia:ia+3, ib:ib+3] += Ga.T @ Gb
    return M

def test_odd_L():
    """Test lambda_max(M(Q)) for L=3, d=4."""
    L_val = 3
    d_val = 4
    print(f"=== Odd L Test: L={L_val}, d={d_val} ===")
    N_v, N_e, N_dim, vi, all_v, ei, nb = build_lattice(L_val, d_val)
    print(f"  Vertices: {N_v}, Edges: {N_e}, Dim: {N_dim}")
    verts = all_v()

    # Test at Q=I
    Q_id = {}
    for x in verts:
        for mu in range(d_val):
            Q_id[(x, mu)] = np.eye(3)

    M_id = build_full_M(Q_id, L_val, d_val)
    eigs_id = np.linalg.eigvalsh(M_id)
    print(f"  Q=I: lambda_max = {eigs_id[-1]:.6f}")
    print(f"  Q=I: top 5 eigenvalues = {sorted(eigs_id)[-5:]}")

    # Count distinct eigenvalues
    unique = {}
    for ev in eigs_id:
        rounded = round(ev, 1)
        unique[rounded] = unique.get(rounded, 0) + 1
    print(f"  Q=I eigenvalue multiplicities: {dict(sorted(unique.items()))}")

    # Random Q tests
    max_lmax = 0
    violations = 0
    for trial in range(30):
        Q = {}
        for x in verts:
            for mu in range(d_val):
                Q[(x, mu)] = random_so3()
        M = build_full_M(Q, L_val, d_val)
        lmax = np.linalg.eigvalsh(M)[-1]
        max_lmax = max(max_lmax, lmax)
        if lmax > 16 + 1e-8:
            violations += 1
        if trial < 5:
            print(f"  Trial {trial}: lmax = {lmax:.6f}")

    print(f"\n  Max lambda_max (L={L_val}): {max_lmax:.6f}")
    print(f"  Violations (>16): {violations}/30")
    print(f"  Status: {'VERIFIED' if violations == 0 else 'FAILED'}")

    return violations == 0

def focused_non_stag_attack():
    """Try to maximize non-staggered eigenvalue for L=2."""
    L_val = 2
    d_val = 4
    print(f"\n=== Focused Non-Staggered Attack: L={L_val} ===")
    N_v, N_e, N_dim, vi, all_v, ei, nb = build_lattice(L_val, d_val)
    verts = all_v()

    # Strategy: parametrize Q to be "bad" for non-staggered modes
    # Key insight: at Q=I, non-stag max = 12. We want to push this above 16.

    # Build staggered projector
    basis = []
    for a in range(3):
        for j in range(3):
            T = np.zeros((4, 3))
            T[a, j] = 1.0
            T[3, j] = -1.0
            v = np.zeros(N_dim)
            for x in verts:
                sx = sum(x) % 2
                for mu in range(d_val):
                    sign = (-1)**(sx + mu)
                    idx = ei(x, mu)
                    v[3*idx:3*idx+3] = sign * T[mu]
            basis.append(v)
    P_stag = np.column_stack(basis)
    P_stag, _ = np.linalg.qr(P_stag)
    P_perp = np.eye(N_dim) - P_stag @ P_stag.T

    best_non_stag = 0
    best_full = 0

    for trial in range(100):
        Q = {}
        for x in verts:
            for mu in range(d_val):
                Q[(x, mu)] = random_so3()

        M = build_full_M(Q, L_val, d_val)
        eigvals, eigvecs = np.linalg.eigh(M)

        # Non-staggered eigenvalue: project out staggered component
        M_ns = P_perp @ M @ P_perp
        ns_eigs = np.linalg.eigvalsh(M_ns)
        ns_max = max(e for e in ns_eigs if e > 0.1)

        best_non_stag = max(best_non_stag, ns_max)
        best_full = max(best_full, eigvals[-1])

    print(f"  Best non-staggered eigenvalue: {best_non_stag:.6f}")
    print(f"  Best full lambda_max: {best_full:.6f}")
    print(f"  Gap to 16: {16 - best_non_stag:.4f}")

    # Now do gradient ascent specifically on non-staggered eigenvalue
    print("\n  Gradient ascent on non-stag eigenvalue...")
    best_ns_grad = 0

    for start in range(10):
        Q = {}
        for x in verts:
            for mu in range(d_val):
                Q[(x, mu)] = random_so3()

        for step in range(60):
            M = build_full_M(Q, L_val, d_val)
            M_ns = P_perp @ M @ P_perp
            ns_eigs = np.linalg.eigvalsh(M_ns)
            ns_max = max(e for e in ns_eigs if e > 0.1)

            # Random perturbation gradient
            improved = False
            for _ in range(5):
                x = verts[np.random.randint(N_v)]
                mu = np.random.randint(d_val)
                eps = 0.01
                v = np.random.randn(3) * eps
                K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])

                Q_orig = Q[(x, mu)].copy()
                Q[(x, mu)] = expm(K) @ Q_orig

                M_new = build_full_M(Q, L_val, d_val)
                M_ns_new = P_perp @ M_new @ P_perp
                ns_new = max(e for e in np.linalg.eigvalsh(M_ns_new) if e > 0.1)

                if ns_new > ns_max:
                    improved = True
                    break
                else:
                    Q[(x, mu)] = Q_orig

        M_final = build_full_M(Q, L_val, d_val)
        M_ns_final = P_perp @ M_final @ P_perp
        ns_final = max(e for e in np.linalg.eigvalsh(M_ns_final) if e > 0.1)
        best_ns_grad = max(best_ns_grad, ns_final)

        if start < 5:
            print(f"    Start {start}: non-stag max = {ns_final:.6f}")

    print(f"\n  Best non-stag via gradient ascent: {best_ns_grad:.6f}")
    print(f"  16 - best = {16 - best_ns_grad:.4f}")
    print(f"  Status: {'DANGEROUS' if best_ns_grad > 15.5 else 'SAFE (gap > 0.5)'}")

    return best_ns_grad

if __name__ == "__main__":
    ns_max = focused_non_stag_attack()
    odd_L_ok = test_odd_L()

    print("\n" + "="*60)
    print("FINAL ADVERSARIAL RESULTS")
    print("="*60)
    print(f"  Max non-staggered eigenvalue (L=2): {ns_max:.6f}")
    print(f"  Odd L (L=3) bound holds: {odd_L_ok}")
    print(f"  Non-staggered gap to 16: {16 - ns_max:.4f}")
