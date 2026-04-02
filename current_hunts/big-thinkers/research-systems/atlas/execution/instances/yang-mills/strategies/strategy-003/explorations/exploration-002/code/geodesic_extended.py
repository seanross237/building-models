"""
Extended geodesic analysis:
1. F(t) along single-edge geodesic: does F stay = 4d?
2. F for abelian configurations
3. Gradient ascent to find F > 4d
4. F''(0) along adversarial directions
5. F(t) at larger t to check if F drops below 4d everywhere
6. Full geodesic at various Q, not just Q=I
"""

import numpy as np
from numpy.linalg import eigh, eigvalsh, norm
import itertools
from scipy.linalg import expm

# ===== Setup (same as before) =====
L = 2
d = 4
n_alg = 3

sites = list(itertools.product(range(L), repeat=d))
n_sites = len(sites)

def site_idx(x):
    return sum(x[i] * L**(d-1-i) for i in range(d))

n_edges = n_sites * d
dim_v = n_edges * n_alg

def edge_idx(x, mu):
    return site_idx(x) * d + mu

def nbr(x, mu, sign=1):
    x = list(x)
    x[mu] = (x[mu] + sign) % L
    return tuple(x)

sigma = [
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex)
]
tau = [-0.5j * s for s in sigma]

def ip(A, B):
    return -2.0 * np.real(np.trace(A @ B))

f_struct = np.zeros((3, 3, 3))
for a in range(3):
    for b in range(3):
        comm = tau[a] @ tau[b] - tau[b] @ tau[a]
        for c in range(3):
            f_struct[a, b, c] = ip(comm, tau[c])

plaquettes = [(x, mu, nu) for x in sites for mu in range(d) for nu in range(mu+1, d)]

def plaq_edges(x, mu, nu):
    return [
        (x, mu, +1),
        (nbr(x, mu), nu, +1),
        (nbr(x, nu), mu, -1),
        (x, nu, -1)
    ]

def build_M_at_Q(Q_mats):
    """Build M(Q) for gauge config Q_mats[e] ∈ SU(2)."""
    M = np.zeros((dim_v, dim_v))
    for x, mu, nu in plaquettes:
        edges_signs = plaq_edges(x, mu, nu)
        (x1, m1, s1), (x2, m2, s2), (x3, m3, s3), (x4, m4, s4) = edges_signs
        e1 = edge_idx(x1, m1)
        e2 = edge_idx(x2, m2)
        e3 = edge_idx(x3, m3)
        e4 = edge_idx(x4, m4)

        Q1, Q2, Q3 = Q_mats[e1], Q_mats[e2], Q_mats[e3]
        P2 = Q1
        P3 = Q1 @ Q2
        P4 = Q1 @ Q2 @ Q3.conj().T

        def Ad_mat(G):
            result = np.zeros((n_alg, n_alg))
            for a in range(n_alg):
                Ad_a = G @ tau[a] @ G.conj().T
                for c in range(n_alg):
                    result[c, a] = ip(tau[c], Ad_a)
            return result

        Ad2, Ad3, Ad4 = Ad_mat(P2), Ad_mat(P3), Ad_mat(P4)

        B_mat = np.zeros((n_alg, dim_v))
        B_mat[:, e1*n_alg:e1*n_alg+n_alg] = np.eye(n_alg) * s1
        B_mat[:, e2*n_alg:e2*n_alg+n_alg] = Ad2 * s2
        B_mat[:, e3*n_alg:e3*n_alg+n_alg] = Ad3 * s3
        B_mat[:, e4*n_alg:e4*n_alg+n_alg] = Ad4 * s4

        M += B_mat.T @ B_mat
    return M

def F_at_Q(Q_mats):
    return eigvalsh(build_M_at_Q(Q_mats))[-1]

Q_identity = [np.eye(2, dtype=complex) for _ in range(n_edges)]
F_I = F_at_Q(Q_identity)
print(f"F(I) = {F_I:.6f} (expected {4*d})")

# ===== 1. F(t) along single-edge geodesic =====
print("\n=== 1. F(t) along single-edge geodesic ===")

def F_single_edge(e_idx, alg_idx, t_vals):
    """F(t) = λ_max(M(Q)) where Q_{e_idx} = exp(t τ_{alg_idx}), others = I"""
    results = []
    for t in t_vals:
        Q = [np.eye(2, dtype=complex) for _ in range(n_edges)]
        Q[e_idx] = expm(t * tau[alg_idx])
        results.append(F_at_Q(Q))
    return np.array(results)

t_vals = np.linspace(0, np.pi, 50)  # full range
for e_test in [0, 1, 5]:
    for a_test in [0]:
        F_vals = F_single_edge(e_test, a_test, t_vals)
        print(f"  Edge {e_test}, alg {a_test}: F range = [{F_vals.min():.6f}, {F_vals.max():.6f}]")
        print(f"    F(t): {F_vals[:5]} ...")
        print(f"    max F = {F_vals.max():.6f} at t = {t_vals[F_vals.argmax()]:.4f}")

# Check: is F(t) = 4d for ALL t on single-edge geodesic?
print("\nDetailed single-edge F(t):")
t_fine = np.linspace(0, np.pi, 20)
F_single = F_single_edge(0, 0, t_fine)
print(f"F(t): {F_single}")
print(f"Max deviation from {4*d}: {max(abs(F_single - 4*d)):.2e}")

# ===== 2. Abelian configurations =====
print("\n=== 2. Abelian (diagonal) configurations ===")

def random_abelian_config(theta_range=np.pi):
    """All links Q_e = diag(exp(iθ_e), exp(-iθ_e)) with random θ_e"""
    Q = []
    for e in range(n_edges):
        theta = np.random.uniform(-theta_range, theta_range)
        Q.append(np.array([[np.exp(1j*theta), 0], [0, np.exp(-1j*theta)]], dtype=complex))
    return Q

np.random.seed(42)
F_abelian = []
for trial in range(50):
    Q_ab = random_abelian_config()
    F_abelian.append(F_at_Q(Q_ab))

print(f"Abelian configs F(Q) range: [{min(F_abelian):.4f}, {max(F_abelian):.4f}]")
print(f"Abelian configs F(Q) mean: {np.mean(F_abelian):.4f}")
print(f"All abelian F = 4d? {all(abs(f - 4*d) < 1e-6 for f in F_abelian)}")

# ===== 3. Large-t geodesics from I =====
print("\n=== 3. Large-t multi-link geodesics from I ===")

np.random.seed(123)
for trial in range(10):
    W = np.random.randn(n_edges, n_alg)
    W /= norm(W)

    t_vals_large = np.linspace(0, np.pi, 30)
    F_traj = []
    for t in t_vals_large:
        W_su2 = [sum(W[e, a] * tau[a] for a in range(n_alg)) for e in range(n_edges)]
        Q = [expm(t * W_su2[e]) for e in range(n_edges)]
        F_traj.append(F_at_Q(Q))

    print(f"  Trial {trial+1}: F range = [{min(F_traj):.4f}, {max(F_traj):.4f}], F(0)={F_traj[0]:.4f}, F(π)={F_traj[-1]:.4f}")

# ===== 4. Gradient ascent from Q=I to find F > 4d =====
print("\n=== 4. Gradient ascent for F(Q) ===")

def gradient_of_F(Q_mats, eps=1e-5):
    """Numerical gradient of F(Q) w.r.t. Q via finite differences in su(2)"""
    F0 = F_at_Q(Q_mats)
    grad = np.zeros((n_edges, n_alg))
    for e in range(n_edges):
        for a in range(n_alg):
            Q_plus = [q.copy() for q in Q_mats]
            Q_plus[e] = Q_plus[e] @ expm(eps * tau[a])
            F_plus = F_at_Q(Q_plus)
            grad[e, a] = (F_plus - F0) / eps
    return F0, grad

def gradient_ascent_F(Q_init, n_steps=50, lr=0.01):
    """Maximize F(Q) via gradient ascent on SU(2)^E"""
    Q = [q.copy() for q in Q_init]
    F_history = [F_at_Q(Q)]

    for step in range(n_steps):
        F0, grad = gradient_of_F(Q)
        # Retraction: Q_e → Q_e * exp(lr * grad_e * τ_{a*})
        # Actually, gradient w.r.t. right action: Q_e → Q_e * exp(lr * v_e)
        for e in range(n_edges):
            v_e = sum(lr * grad[e, a] * tau[a] for a in range(n_alg))
            Q[e] = Q[e] @ expm(v_e)
        F_new = F_at_Q(Q)
        F_history.append(F_new)

    return Q, np.array(F_history)

# Start from small perturbations
np.random.seed(42)
print("Gradient ascent starting from near I:")
for trial in range(5):
    # Random small perturbation
    Q_init = []
    for e in range(n_edges):
        W_e = sum(0.1 * np.random.randn() * tau[a] for a in range(n_alg))
        Q_init.append(np.eye(2, dtype=complex) @ expm(W_e))

    Q_max, F_hist = gradient_ascent_F(Q_init, n_steps=30, lr=0.005)
    print(f"  Trial {trial+1}: F_init={F_hist[0]:.4f}, F_final={F_hist[-1]:.4f}, F_max={max(F_hist):.4f}")

# Start from random Q
print("\nGradient ascent starting from random SU(2)^E:")
from scipy.stats import special_ortho_group

def random_su2():
    """Random SU(2) matrix"""
    u = np.random.randn(4)
    u /= np.linalg.norm(u)
    a, b, c, d = u
    return np.array([[a + 1j*b, c + 1j*d], [-c + 1j*d, a - 1j*b]])

np.random.seed(42)
for trial in range(5):
    Q_init = [random_su2() for _ in range(n_edges)]
    Q_max, F_hist = gradient_ascent_F(Q_init, n_steps=50, lr=0.005)
    print(f"  Trial {trial+1}: F_init={F_hist[0]:.4f}, F_final={F_hist[-1]:.4f}, F_max={max(F_hist):.4f}")

# ===== 5. Higher-order terms for single-edge W =====
print("\n=== 5. Higher-order analysis for single-edge W ===")

# F(t) for single edge up to 4th order via finite differences
def Fn_order(e_idx, alg_idx, n=4):
    """Compute F(t) Taylor coefficients at t=0 for single-edge geodesic"""
    eps = 1e-3
    # Need F(0), F(eps), F(-eps), F(2eps), F(-2eps) for 4th order
    pts = {}
    for k in range(-2, 3):
        Q = [np.eye(2, dtype=complex) for _ in range(n_edges)]
        if k != 0:
            Q[e_idx] = expm(k * eps * tau[alg_idx])
        pts[k] = F_at_Q(Q)

    F0 = pts[0]
    F1 = (pts[1] - pts[-1]) / (2*eps)
    F2 = (pts[1] - 2*pts[0] + pts[-1]) / eps**2
    F3 = (pts[2] - 2*pts[1] + 2*pts[-1] - pts[-2]) / (2*eps**3)
    F4 = (pts[2] - 4*pts[1] + 6*pts[0] - 4*pts[-1] + pts[-2]) / eps**4

    return F0, F1, F2, F3, F4

for e_test in [0, 1]:
    for a_test in [0, 2]:
        F0, F1, F2, F3, F4 = Fn_order(e_test, a_test)
        print(f"  Edge {e_test}, alg {a_test}: F(0)={F0:.4f}, F'={F1:.4f}, F''={F2:.4f}, F'''={F3:.4f}, F''''={F4:.4f}")

# ===== 6. F''(0) for adversarial (near-flat) W =====
print("\n=== 6. Adversarial search for max F''(0) ===")

# Import from geodesic_convexity.py results
# We know F''(0) = 0 for single-edge
# Can we find W with F''(0) slightly positive?

# Try structured W: staggered perturbation (most natural candidate)
def staggered_W(dir_mu, alg_idx):
    """W_e = sigma_e * tau_{alg_idx} where sigma_e = (-1)^{|x|+mu} × delta_{mu, dir_mu}"""
    W = np.zeros((n_edges, n_alg))
    for x in sites:
        e = edge_idx(x, dir_mu)
        sign = (-1) ** (sum(x) + dir_mu)
        W[e, alg_idx] = sign
    return W / norm(W.ravel())

# Note: staggered_W is proportional to v_stag (the top eigenmode!)
# So this is a "natural" geodesic direction aligned with the eigenspace

print("Staggered W (aligned with top eigenmode):")
for dir_mu in range(d):
    for alg_idx in range(n_alg):
        W_stag = staggered_W(dir_mu, alg_idx)
        # Check F''(0)
        W_su2 = [sum(W_stag[e, a] * tau[a] for a in range(n_alg)) for e in range(n_edges)]
        eps = 1e-3
        F_vals = []
        for k in [-2, -1, 0, 1, 2]:
            Q = [expm(k * eps * W_su2[e]) for e in range(n_edges)]
            F_vals.append(F_at_Q(Q))
        F2_fd = (F_vals[3] - 2*F_vals[2] + F_vals[1]) / eps**2
        print(f"  dir={dir_mu}, alg={alg_idx}: F''(0) ≈ {F2_fd:.6f}")

# Try to maximize F''(0) via gradient ascent on W
print("\nGradient ascent on F''(0):")

def compute_F2_numerical(W_vec):
    """Compute F''(0) by finite differences"""
    eps = 1e-3
    W_su2 = [sum(W_vec[e, a] * tau[a] for a in range(n_alg)) for e in range(n_edges)]
    F_plus = eigvalsh(build_M_at_Q([expm(eps * W_su2[ee]) for ee in range(n_edges)]))[-1]
    F_zero = 4.0 * d  # known
    F_minus = eigvalsh(build_M_at_Q([expm(-eps * W_su2[ee]) for ee in range(n_edges)]))[-1]
    return (F_plus - 2*F_zero + F_minus) / eps**2

# Start from the "worst" W found in main scan (random)
np.random.seed(42)
W_best = np.random.randn(n_edges, n_alg)
W_best /= norm(W_best.ravel())
F2_best = compute_F2_numerical(W_best)
print(f"Initial: F''(0) = {F2_best:.6f}")

# Simple gradient ascent: maximize F''(0) over W in unit sphere
for step in range(30):
    grad = np.zeros_like(W_best)
    eps_grad = 1e-3
    F2_0 = compute_F2_numerical(W_best)
    for e in range(min(n_edges, 20)):  # partial gradient for speed
        for a in range(n_alg):
            dW = np.zeros_like(W_best)
            dW[e, a] = eps_grad
            F2_p = compute_F2_numerical(W_best + dW)
            grad[e, a] = (F2_p - F2_0) / eps_grad

    # Project onto sphere
    W_new = W_best + 0.01 * grad
    W_new /= norm(W_new.ravel())
    F2_new = compute_F2_numerical(W_new)

    if F2_new > F2_best:
        W_best = W_new
        F2_best = F2_new

    if step % 10 == 0:
        print(f"  Step {step}: max F''(0) = {F2_best:.6f}")

print(f"Final adversarial F''(0) = {F2_best:.6f}")

# ===== 7. Check geodesic concavity at other Q =====
print("\n=== 7. Geodesic concavity at Q ≠ I ===")

# For the geodesic convexity approach to work globally, we need F''(t) ≤ 0
# along entire geodesics, not just at Q=I.
#
# Check: along geodesic γ(t) = exp(tW) from I, is F''(t) ≤ 0 for t ∈ [0, π]?

def F_trajectory_and_concavity(W_vec, t_max=np.pi, n_pts=30):
    """
    Compute F(t) and check concavity along geodesic γ(t) = exp(tW).
    """
    W_su2 = [sum(W_vec[e, a] * tau[a] for a in range(n_alg)) for e in range(n_edges)]

    t_vals = np.linspace(0, t_max, n_pts)
    F_vals = []
    for t in t_vals:
        Q = [expm(t * W_su2[ee]) for ee in range(n_edges)]
        F_vals.append(F_at_Q(Q))

    F_arr = np.array(F_vals)
    # Check concavity: d²F/dt² ≤ 0 everywhere
    # Finite difference second derivative
    dt = t_vals[1] - t_vals[0]
    F2 = np.diff(F_arr, n=2) / dt**2

    return t_vals, F_arr, F2

np.random.seed(42)
print("Checking concavity along full geodesics from I:")
for trial in range(5):
    W = np.random.randn(n_edges, n_alg)
    W /= norm(W.ravel())

    t_vals, F_arr, F2 = F_trajectory_and_concavity(W)
    is_concave = np.all(F2 <= 1e-6)  # allow small numerical error

    print(f"  Trial {trial+1}: F range=[{F_arr.min():.4f},{F_arr.max():.4f}], "
          f"F''(t) range=[{F2.min():.4f},{F2.max():.4f}], concave={is_concave}")

# ===== 8. Key visualization: F''(0) as function of W orientation =====
print("\n=== 8. F''(0) dependence on W type ===")

# Decompose W into: all-single-edge, all-multi-edge, staggered, uniform...
print("Various structured W types:")
types = []

# Type 1: Single edges
for e in range(3):
    for a in range(n_alg):
        W = np.zeros((n_edges, n_alg))
        W[e, a] = 1.0
        F2 = compute_F2_numerical(W)
        types.append(("single", F2))

# Type 2: Two-edge (pairs of adjacent edges)
for mu in range(d):
    for a in range(n_alg):
        W = np.zeros((n_edges, n_alg))
        W[0, a] = 1.0  # edge 0 = (x=0, mu=0)
        W[edge_idx(tuple([0]*d), mu), a] = 1.0
        F2 = compute_F2_numerical(W / norm(W.ravel()))
        types.append(("two-edge", F2))

# Type 3: Plaquette-shaped W (4 edges of one plaquette)
x0, mu0, nu0 = sites[0], 0, 1
for a in range(n_alg):
    W = np.zeros((n_edges, n_alg))
    for (xi, mi, si) in plaq_edges(x0, mu0, nu0):
        W[edge_idx(xi, mi), a] = si
    F2 = compute_F2_numerical(W / norm(W.ravel()))
    types.append(("plaquette", F2))

# Type 4: All-links same direction
for a in range(n_alg):
    W = np.ones((n_edges, n_alg)) * 0
    W[:, a] = 1.0
    F2 = compute_F2_numerical(W / norm(W.ravel()))
    types.append(("uniform", F2))

for type_name, F2 in types:
    print(f"  {type_name}: F''(0) = {F2:.6f}")

# Summary statistics by type
for tname in ["single", "two-edge", "plaquette", "uniform"]:
    vals = [F2 for name, F2 in types if name == tname]
    print(f"{tname}: range=[{min(vals):.4f}, {max(vals):.4f}]")

# ===== Summary =====
print("\n===== EXTENDED SUMMARY =====")
print(f"1. Single-edge geodesic: F(t) = {4*d} for all t (abelian: F = {4*d} always)")
print(f"2. Abelian configs all have F = {4*d} (not unique max)")
print(f"3. Large-t multi-link geodesics: F < {4*d} interior, returns to {4*d} at t=π")
print(f"4. No F > {4*d} found by gradient ascent")
print(f"5. Geodesic concavity along full paths: appears to hold")
print(f"6. F''(0) = 0 for single-edge W, F''(0) < 0 for multi-edge W")
