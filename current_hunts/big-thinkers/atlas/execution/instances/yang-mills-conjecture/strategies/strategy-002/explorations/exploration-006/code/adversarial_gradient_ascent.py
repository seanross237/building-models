"""
Adversarial gradient ascent on lambda_max of full M(Q) for L=2, d=4.
Goal: try to push lambda_max above 16.
"""
import numpy as np
from scipy.linalg import expm
import itertools

np.random.seed(456)

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

def neighbor(x, mu, direction=1):
    y = list(x)
    y[mu] = (y[mu] + direction) % L
    return tuple(y)

def holonomy(Q, x, mu, nu):
    x_plus_mu = neighbor(x, mu)
    x_plus_nu = neighbor(x, nu)
    return Q[(x, mu)] @ Q[(x_plus_mu, nu)] @ Q[(x_plus_nu, mu)].T @ Q[(x, nu)].T

def build_full_M(Q):
    M = np.zeros((N_dim, N_dim))
    for x in all_vertices():
        for mu in range(d):
            for nu in range(mu+1, d):
                x_plus_mu = neighbor(x, mu)
                x_plus_nu = neighbor(x, nu)

                G1 = np.eye(3)
                G2 = Q[(x, mu)]
                G3 = -(Q[(x, mu)] @ Q[(x_plus_mu, nu)] @ Q[(x_plus_nu, mu)].T)
                G4 = -holonomy(Q, x, mu, nu)

                edges_G = [
                    (3 * edge_index(x, mu), G1),
                    (3 * edge_index(x_plus_mu, nu), G2),
                    (3 * edge_index(x_plus_nu, mu), G3),
                    (3 * edge_index(x, nu), G4),
                ]
                for (ia, Ga) in edges_G:
                    for (ib, Gb) in edges_G:
                        M[ia:ia+3, ib:ib+3] += Ga.T @ Gb
    return M

def Q_to_vec(Q):
    """Flatten Q dict to a vector (for gradient computation)."""
    verts = all_vertices()
    vec = []
    for x in verts:
        for mu in range(d):
            vec.append(Q[(x, mu)].flatten())
    return np.concatenate(vec)

def gradient_ascent_lambda_max(n_starts=30, n_steps=150, lr=0.005, eps=1e-5):
    """Riemannian gradient ascent on SO(3)^E to maximize lambda_max(M(Q))."""
    print(f"=== Adversarial Gradient Ascent ({n_starts} starts × {n_steps} steps) ===")

    best_lmax = 0
    best_Q = None
    verts = all_vertices()

    for start in range(n_starts):
        # Initialize with random Q
        Q = {}
        for x in verts:
            for mu in range(d):
                Q[(x, mu)] = random_so3()

        M = build_full_M(Q)
        eigvals, eigvecs = np.linalg.eigh(M)
        lmax = eigvals[-1]

        for step in range(n_steps):
            top_vec = eigvecs[:, -1]

            # Gradient: d(lmax)/d(Q_{x,mu}) via finite differences
            for x in verts:
                for mu in range(d):
                    # Try 3 random skew-symmetric directions
                    for _ in range(1):
                        v = np.random.randn(3) * eps
                        K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
                        Q_orig = Q[(x, mu)].copy()

                        Q[(x, mu)] = expm(K) @ Q_orig
                        M_new = build_full_M(Q)
                        lmax_new = np.linalg.eigvalsh(M_new)[-1]

                        grad = (lmax_new - lmax) / eps

                        if grad > 0:
                            # Accept the step with reduced lr
                            K_step = K * (lr / eps)
                            Q[(x, mu)] = expm(K_step) @ Q_orig
                        else:
                            Q[(x, mu)] = Q_orig

            M = build_full_M(Q)
            eigvals, eigvecs = np.linalg.eigh(M)
            lmax = eigvals[-1]

        if lmax > best_lmax:
            best_lmax = lmax
            best_Q = {k: v.copy() for k, v in Q.items()}

        if start < 5 or lmax > 15:
            print(f"  Start {start}: lmax = {lmax:.6f}")

    print(f"\n  BEST lambda_max found: {best_lmax:.6f}")
    print(f"  Bound: 16.000000")
    print(f"  Gap: {16.0 - best_lmax:.6f}")
    print(f"  Status: {'BOUND VIOLATED!' if best_lmax > 16 + 1e-8 else 'No violation found'}")

    # For the best config, analyze the eigenvalue structure
    if best_Q is not None:
        M_best = build_full_M(best_Q)
        eigvals_best = np.linalg.eigvalsh(M_best)
        print(f"\n  Best config top 10 eigenvalues:")
        for i, ev in enumerate(sorted(eigvals_best)[-10:]):
            print(f"    {i}: {ev:.6f}")

    return best_lmax

def adversarial_near_identity(n_trials=50, eps_range=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0]):
    """Try configs near Q=I at various perturbation scales."""
    print("\n=== Near-Identity Adversarial ===")
    verts = all_vertices()

    for eps in eps_range:
        max_lmax = 0
        for _ in range(n_trials):
            Q = {}
            for x in verts:
                for mu in range(d):
                    v = np.random.randn(3) * eps
                    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
                    Q[(x, mu)] = expm(K)
            M = build_full_M(Q)
            lmax = np.linalg.eigvalsh(M)[-1]
            max_lmax = max(max_lmax, lmax)

        print(f"  eps={eps:.2f}: max lmax = {max_lmax:.6f}")

def adversarial_extreme_configs():
    """Try extreme configurations: all links = 180-degree rotations, etc."""
    print("\n=== Extreme Configuration Tests ===")
    verts = all_vertices()

    configs = []

    # Config 1: All links = 180-degree rotation about x-axis
    Q1 = {}
    R180x = np.diag([1, -1, -1]).astype(float)
    for x in verts:
        for mu in range(d):
            Q1[(x, mu)] = R180x
    configs.append(("All R=180x", Q1))

    # Config 2: All links = 180-degree rotation about z-axis
    Q2 = {}
    R180z = np.diag([-1, -1, 1]).astype(float)
    for x in verts:
        for mu in range(d):
            Q2[(x, mu)] = R180z
    configs.append(("All R=180z", Q2))

    # Config 3: Alternating 90 and -90 degree rotations
    Q3 = {}
    R90 = np.array([[1,0,0],[0,0,-1],[0,1,0]], dtype=float)
    Rm90 = R90.T
    for x in verts:
        for mu in range(d):
            if (sum(x) + mu) % 2 == 0:
                Q3[(x, mu)] = R90
            else:
                Q3[(x, mu)] = Rm90
    configs.append(("Alternating ±90", Q3))

    # Config 4: Random per-direction (same R for all x in a given mu)
    Q4 = {}
    Rs = [random_so3() for _ in range(d)]
    for x in verts:
        for mu in range(d):
            Q4[(x, mu)] = Rs[mu]
    configs.append(("Uniform per-direction", Q4))

    # Config 5: -I everywhere (det=-1, not SO(3), but test anyway)
    Q5 = {}
    for x in verts:
        for mu in range(d):
            Q5[(x, mu)] = -np.eye(3)
    configs.append(("All R=-I", Q5))

    for name, Q in configs:
        M = build_full_M(Q)
        eigvals = np.linalg.eigvalsh(M)
        lmax = eigvals[-1]
        print(f"  {name}: lmax = {lmax:.6f} {'VIOLATION!' if lmax > 16 + 1e-8 else ''}")

if __name__ == "__main__":
    adversarial_extreme_configs()
    adversarial_near_identity()
    best = gradient_ascent_lambda_max(n_starts=20, n_steps=80)

    print("\n" + "="*60)
    print(f"ADVERSARIAL SUMMARY: Best lambda_max = {best:.6f}")
    print(f"Bound 16 {'VIOLATED' if best > 16 else 'NOT violated'}")
    print("="*60)
