"""
Fast gradient ascent on lambda_max(M(Q)) using eigenvector-based gradient.

Key formula: d(lambda_max)/d(theta_j) = v^T (dM/dtheta_j) v
where v is the top eigenvector.

We compute dM/dtheta_j by perturbing one edge at a time.
"""
import numpy as np
from scipy.linalg import expm
import itertools
import time

np.random.seed(2024)

L = 2; d = 4
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

VERTICES = all_vertices()

def edge_index(x, mu):
    return vertex_index(x) * d + mu

def neighbor(x, mu):
    y = list(x)
    y[mu] = (y[mu] + 1) % L
    return tuple(y)

def skew(v):
    return np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])

def build_full_M(Q):
    M = np.zeros((N_dim, N_dim))
    for x in VERTICES:
        for mu in range(d):
            for nu in range(mu+1, d):
                xmu = neighbor(x, mu)
                xnu = neighbor(x, nu)
                G1 = np.eye(3)
                G2 = Q[(x, mu)]
                G3 = -(Q[(x, mu)] @ Q[(xmu, nu)] @ Q[(xnu, mu)].T)
                U = Q[(x, mu)] @ Q[(xmu, nu)] @ Q[(xnu, mu)].T @ Q[(x, nu)].T
                G4 = -U
                idx1 = 3 * edge_index(x, mu)
                idx2 = 3 * edge_index(xmu, nu)
                idx3 = 3 * edge_index(xnu, mu)
                idx4 = 3 * edge_index(x, nu)
                edges = [(idx1, G1), (idx2, G2), (idx3, G3), (idx4, G4)]
                for (ia, Ga) in edges:
                    for (ib, Gb) in edges:
                        M[ia:ia+3, ib:ib+3] += Ga.T @ Gb
    return M

# ============================================================
# Strategy: Stochastic gradient ascent
# ============================================================

def random_direction_gradient(Q, v, n_dirs=20, delta=1e-5):
    """Estimate gradient using random directions (faster than full gradient)."""
    best_dir = None
    best_increase = -np.inf

    for _ in range(n_dirs):
        # Pick random edge and random generator
        x = VERTICES[np.random.randint(N_vertices)]
        mu = np.random.randint(d)
        gen = np.random.randn(3)
        gen /= np.linalg.norm(gen)

        # Perturb Q in this direction
        Q_plus = dict(Q)
        Q_plus[(x, mu)] = Q[(x, mu)] @ expm(delta * skew(gen))

        M_plus = build_full_M(Q_plus)
        lmax_plus = v @ M_plus @ v  # Rayleigh quotient approximation

        increase = (lmax_plus - v @ build_full_M(Q) @ v) / delta

        if increase > best_increase:
            best_increase = increase
            best_dir = (x, mu, gen)

    return best_dir, best_increase

print("=" * 70)
print("FAST GRADIENT ASCENT ON lambda_max(M(Q))")
print("=" * 70)

overall_best = 0
n_starts = 20

for start in range(n_starts):
    # Random initial Q
    Q = {(x, mu): expm(skew(np.random.randn(3)))
         for x in VERTICES for mu in range(d)}

    M = build_full_M(Q)
    eigs, vecs = np.linalg.eigh(M)
    lmax = eigs[-1]
    best_lmax = lmax

    # Gradient ascent steps
    for step in range(50):
        v = vecs[:, -1]  # top eigenvector

        # Try multiple random perturbations
        best_new_lmax = lmax
        best_Q_new = None

        for _ in range(30):
            x = VERTICES[np.random.randint(N_vertices)]
            mu = np.random.randint(d)
            gen = np.random.randn(3)

            # Try different step sizes
            for eps in [0.05, 0.1, 0.2, 0.5]:
                Q_new = dict(Q)
                Q_new[(x, mu)] = Q[(x, mu)] @ expm(eps * skew(gen))
                M_new = build_full_M(Q_new)
                eigs_new = np.linalg.eigvalsh(M_new)
                lmax_new = eigs_new[-1]

                if lmax_new > best_new_lmax:
                    best_new_lmax = lmax_new
                    best_Q_new = Q_new

        if best_Q_new is not None and best_new_lmax > lmax + 1e-12:
            Q = best_Q_new
            M = build_full_M(Q)
            eigs, vecs = np.linalg.eigh(M)
            lmax = eigs[-1]
            best_lmax = max(best_lmax, lmax)
        else:
            break  # stuck

    overall_best = max(overall_best, best_lmax)
    if start < 10 or start % 5 == 0:
        print(f"  Start {start:2d}: best lmax = {best_lmax:.8f}")

print(f"\n  Overall best: {overall_best:.10f}")
print(f"  Exceeds 16? {'YES!' if overall_best > 16 + 1e-8 else 'NO'}")

# ============================================================
# Targeted search: systematic edge-by-edge optimization
# ============================================================
print(f"\n{'='*70}")
print("SYSTEMATIC EDGE-BY-EDGE OPTIMIZATION")
print("="*70)

for trial in range(10):
    Q = {(x, mu): expm(skew(np.random.randn(3)))
         for x in VERTICES for mu in range(d)}

    for sweep in range(5):
        improved = False
        for x in VERTICES:
            for mu in range(d):
                # Find best rotation for this edge
                M0 = build_full_M(Q)
                lmax0 = np.linalg.eigvalsh(M0)[-1]

                best_lmax_edge = lmax0
                best_g = Q[(x, mu)]

                # Search over rotations
                for _ in range(20):
                    g_test = expm(skew(np.random.randn(3) * np.random.exponential(1)))
                    Q_test = dict(Q)
                    Q_test[(x, mu)] = g_test
                    M_test = build_full_M(Q_test)
                    lmax_test = np.linalg.eigvalsh(M_test)[-1]

                    if lmax_test > best_lmax_edge:
                        best_lmax_edge = lmax_test
                        best_g = g_test.copy()
                        improved = True

                Q[(x, mu)] = best_g

        M_final = build_full_M(Q)
        lmax_final = np.linalg.eigvalsh(M_final)[-1]

    overall_best = max(overall_best, lmax_final)
    print(f"  Trial {trial}: lmax = {lmax_final:.8f}")

print(f"\n  Overall best after systematic: {overall_best:.10f}")
print(f"  Exceeds 16? {'YES!' if overall_best > 16 + 1e-8 else 'NO'}")

# ============================================================
# Large-scale random search (fast to compute)
# ============================================================
print(f"\n{'='*70}")
print("LARGE-SCALE RANDOM SEARCH (2000 configs)")
print("="*70)

max_random = 0
t0 = time.time()
for trial in range(2000):
    Q = {(x, mu): expm(skew(np.random.randn(3)))
         for x in VERTICES for mu in range(d)}
    M = build_full_M(Q)
    lmax = np.linalg.eigvalsh(M)[-1]
    max_random = max(max_random, lmax)

dt = time.time() - t0
print(f"  Time: {dt:.1f}s")
print(f"  Max lambda_max over 2000 random: {max_random:.8f}")
print(f"  Exceeds 16? {'YES!' if max_random > 16 + 1e-8 else 'NO'}")

overall_best = max(overall_best, max_random)

# ============================================================
# Adversarial: try configs that maximize curvature
# ============================================================
print(f"\n{'='*70}")
print("ADVERSARIAL: HIGH-CURVATURE CONFIGS")
print("="*70)

max_curv = 0
for trial in range(200):
    # Create configs with large curvature (non-trivial holonomies)
    Q = {}
    for x in VERTICES:
        for mu in range(d):
            # Random rotation by angle near π (max curvature)
            angle = np.pi * (0.5 + 0.5 * np.random.rand())
            axis = np.random.randn(3)
            axis /= np.linalg.norm(axis)
            Q[(x, mu)] = expm(angle * skew(axis))

    M = build_full_M(Q)
    lmax = np.linalg.eigvalsh(M)[-1]
    max_curv = max(max_curv, lmax)

print(f"  Max lambda_max (high curv): {max_curv:.8f}")
overall_best = max(overall_best, max_curv)

# Also: configs with one link very different from others
max_spike = 0
for trial in range(200):
    # All links near identity except one
    Q = {(x, mu): expm(skew(np.random.randn(3) * 0.01))
         for x in VERTICES for mu in range(d)}
    # One link at a random extreme rotation
    x_spike = VERTICES[np.random.randint(N_vertices)]
    mu_spike = np.random.randint(d)
    Q[(x_spike, mu_spike)] = expm(np.pi * skew(np.random.randn(3) / np.linalg.norm(np.random.randn(3))))

    M = build_full_M(Q)
    lmax = np.linalg.eigvalsh(M)[-1]
    max_spike = max(max_spike, lmax)

print(f"  Max lambda_max (single spike): {max_spike:.8f}")
overall_best = max(overall_best, max_spike)

print(f"\n{'='*70}")
print(f"GRAND TOTAL: overall best lambda_max = {overall_best:.10f}")
print(f"Exceeds 16? {'YES - COUNTEREXAMPLE FOUND!' if overall_best > 16 + 1e-8 else 'NO - bound holds across all tests'}")
print(f"Gap: {16 - overall_best:.10f}")
print(f"Total configs tested: ~{n_starts * 50 * 30 + 10 * 5 * 16 * 20 + 2000 + 400}")
print("="*70)
