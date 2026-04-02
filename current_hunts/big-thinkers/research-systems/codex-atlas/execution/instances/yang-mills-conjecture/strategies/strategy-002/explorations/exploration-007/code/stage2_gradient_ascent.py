"""
Stage 2: Gradient ascent on lambda_max(M(Q)) to find configurations
that maximize the top eigenvalue. If the max is always ≤ 16, this provides
strong computational evidence.

Also: verify that uniform Q always gives lambda_max = 16 exactly (1-parameter family).
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

def random_so3():
    return expm(skew(np.random.randn(3)))

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
# Part 1: Verify uniform Q always gives lambda_max = 16
# ============================================================
print("=" * 70)
print("UNIFORM Q: VERIFY lambda_max = 16 FOR ALL ANGLES")
print("=" * 70)

angles = np.linspace(0.01, np.pi, 100)
uniform_lmax = []

for theta in angles:
    axis = np.array([1, 0, 0])  # fixed axis for simplicity
    g = expm(theta * skew(axis))
    Q = {(x, mu): g.copy() for x in VERTICES for mu in range(d)}
    M = build_full_M(Q)
    eigs = np.linalg.eigvalsh(M)
    uniform_lmax.append(eigs[-1])

uniform_lmax = np.array(uniform_lmax)
print(f"  Min lambda_max over angles: {uniform_lmax.min():.8f}")
print(f"  Max lambda_max over angles: {uniform_lmax.max():.8f}")
print(f"  All = 16? {np.allclose(uniform_lmax, 16.0, atol=1e-10)}")

# Try random axes too
print("\n  Random axes:")
max_dev = 0
for trial in range(200):
    theta = np.random.uniform(0.01, np.pi)
    axis = np.random.randn(3)
    axis /= np.linalg.norm(axis)
    g = expm(theta * skew(axis))
    Q = {(x, mu): g.copy() for x in VERTICES for mu in range(d)}
    M = build_full_M(Q)
    eigs = np.linalg.eigvalsh(M)
    dev = abs(eigs[-1] - 16.0)
    max_dev = max(max_dev, dev)

print(f"  Max |lambda_max - 16| over 200 random uniform Q: {max_dev:.2e}")
print(f"  Result: lambda_max(uniform Q) = 16 ALWAYS [{'VERIFIED' if max_dev < 1e-10 else 'PARTIAL'}]")

# ============================================================
# Part 2: Gradient ascent on lambda_max(M(Q))
# ============================================================
print(f"\n{'='*70}")
print("GRADIENT ASCENT ON lambda_max(M(Q))")
print("="*70)

def Q_to_params(Q):
    """Convert gauge config to parameter vector (3 params per edge)."""
    params = np.zeros(3 * N_edges)
    for x in VERTICES:
        for mu in range(d):
            ei = edge_index(x, mu)
            g = Q[(x, mu)]
            # Extract axis-angle from rotation matrix
            theta = np.arccos(np.clip((np.trace(g) - 1) / 2, -1, 1))
            if theta < 1e-12:
                params[3*ei:3*ei+3] = np.zeros(3)
            else:
                # Rotation axis from skew-symmetric part
                w = np.array([g[2,1]-g[1,2], g[0,2]-g[2,0], g[1,0]-g[0,1]]) / (2*np.sin(theta))
                params[3*ei:3*ei+3] = theta * w
    return params

def params_to_Q(params):
    """Convert parameter vector to gauge config."""
    Q = {}
    for x in VERTICES:
        for mu in range(d):
            ei = edge_index(x, mu)
            v = params[3*ei:3*ei+3]
            Q[(x, mu)] = expm(skew(v))
    return Q

def lambda_max_from_params(params):
    Q = params_to_Q(params)
    M = build_full_M(Q)
    return np.linalg.eigvalsh(M)[-1]

def gradient_ascent(params0, n_steps=200, eps=0.01, delta=1e-4):
    """Finite-difference gradient ascent on lambda_max."""
    params = params0.copy()
    best_lmax = lambda_max_from_params(params)
    best_params = params.copy()

    for step in range(n_steps):
        # Compute gradient by finite differences
        lmax0 = lambda_max_from_params(params)
        grad = np.zeros_like(params)

        for i in range(len(params)):
            params[i] += delta
            lmax_plus = lambda_max_from_params(params)
            params[i] -= delta
            grad[i] = (lmax_plus - lmax0) / delta

        # Ascent step
        params += eps * grad / (np.linalg.norm(grad) + 1e-12)

        lmax_new = lambda_max_from_params(params)
        if lmax_new > best_lmax:
            best_lmax = lmax_new
            best_params = params.copy()

        if step < 5 or step % 20 == 19:
            print(f"  Step {step:3d}: lmax = {lmax_new:.8f}, |grad| = {np.linalg.norm(grad):.4f}")

        # Reduce step size
        if step > 50:
            eps *= 0.99

    return best_params, best_lmax

# Multiple random starts
print("\nGradient ascent from random initial configs:")
overall_best = 0

for start in range(10):
    print(f"\n--- Start {start} ---")
    Q0 = {(x, mu): random_so3() for x in VERTICES for mu in range(d)}
    params0 = Q_to_params(Q0)
    init_lmax = lambda_max_from_params(params0)
    print(f"  Initial: lmax = {init_lmax:.6f}")

    best_params, best_lmax = gradient_ascent(params0, n_steps=100, eps=0.02)
    print(f"  Best: lmax = {best_lmax:.8f}")
    overall_best = max(overall_best, best_lmax)

print(f"\n  Overall best lambda_max from gradient ascent: {overall_best:.10f}")
print(f"  Exceeds 16? {'YES - COUNTEREXAMPLE!' if overall_best > 16 + 1e-8 else 'NO'}")
print(f"  Gap to 16: {16 - overall_best:.8f}")

# ============================================================
# Part 3: Start from near-identity with adversarial perturbations
# ============================================================
print(f"\n{'='*70}")
print("GRADIENT ASCENT FROM NEAR-IDENTITY (where lambda_max = 16)")
print("="*70)

for start in range(5):
    print(f"\n--- Start {start} ---")
    # Small perturbation from identity
    params0 = np.random.randn(3 * N_edges) * 0.1
    init_lmax = lambda_max_from_params(params0)
    print(f"  Initial (near I): lmax = {init_lmax:.6f}")

    best_params, best_lmax = gradient_ascent(params0, n_steps=100, eps=0.01)
    print(f"  Best: lmax = {best_lmax:.8f}")
    overall_best = max(overall_best, best_lmax)

print(f"\n  Overall best (including near-identity): {overall_best:.10f}")
print(f"  Exceeds 16? {'YES' if overall_best > 16 + 1e-8 else 'NO'}")

# ============================================================
# Part 4: Start from uniform Q (where lambda_max = 16 exactly)
# and perturb
# ============================================================
print(f"\n{'='*70}")
print("PERTURBATIONS FROM UNIFORM Q (lambda_max = 16 exactly)")
print("="*70)

for start in range(5):
    theta = np.random.uniform(0.5, 2.5)
    axis = np.random.randn(3); axis /= np.linalg.norm(axis)
    g = expm(theta * skew(axis))

    # Start at uniform Q, then perturb
    params0 = np.zeros(3 * N_edges)
    for x in VERTICES:
        for mu in range(d):
            ei = edge_index(x, mu)
            params0[3*ei:3*ei+3] = theta * axis

    init_lmax = lambda_max_from_params(params0)
    print(f"  Start {start}: uniform theta={theta:.3f}, lmax = {init_lmax:.8f}")

    # Gradient ascent
    best_params, best_lmax = gradient_ascent(params0, n_steps=100, eps=0.01)
    print(f"  Best after ascent: lmax = {best_lmax:.8f}")
    overall_best = max(overall_best, best_lmax)

print(f"\n{'='*70}")
print(f"FINAL VERDICT: Overall best lambda_max = {overall_best:.10f}")
print(f"Exceeds 16? {'YES - BOUND FAILS!' if overall_best > 16 + 1e-8 else 'NO - bound holds'}")
print(f"Gap: {16 - overall_best:.10f}")
print("="*70)
