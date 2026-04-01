"""
Exploration 002: Per-Plaquette Contribution Structure for Staggered Modes

Compute f_□(Q) = |B_□(Q,v_stag)|² - |B_□(I,v_stag)|² for all plaquettes
across diverse SU(2) configurations. Analyze grouping structure.

Lattice: L=2, d=4
su(2) basis: T_k = i*sigma_k/2, norm |A|^2 = -2 Re Tr(A^2)
"""

import numpy as np
from itertools import product
import json

np.random.seed(42)

# ============================================================
# su(2) setup
# ============================================================
sigma1 = np.array([[0, 1], [1, 0]], dtype=complex)
sigma2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma3 = np.array([[1, 0], [0, -1]], dtype=complex)
sigmas = [sigma1, sigma2, sigma3]
T = [1j/2 * s for s in sigmas]  # T_k = i*sigma_k/2

def su2_norm_sq(A):
    """Compute |A|^2 = -2 Re(Tr(A^2)) for A in su(2)."""
    return float(np.real(-2 * np.trace(A @ A)))

def su2_inner(A, B):
    """Compute <A,B> = -2 Re(Tr(A B)) for A, B in su(2)."""
    # Note: for anti-hermitian A, <A,B> = -2 Tr(A B)
    return float(np.real(-2 * np.trace(A @ B)))

def su2_components(A):
    """Extract components of A in su(2) basis: a_k = -2 Re Tr(T_k A)."""
    return np.array([float(np.real(-2 * np.trace(T[k] @ A))) for k in range(3)])

def adjoint(Q, A):
    """Ad_Q(A) = Q A Q^†."""
    return Q @ A @ Q.conj().T

def adjoint_matrix(Q):
    """3x3 adjoint (SO(3)) representation of Q in SU(2)."""
    R = np.zeros((3, 3))
    for j in range(3):
        AdQ_Tj = adjoint(Q, T[j])
        for i in range(3):
            R[i, j] = float(np.real(-2 * np.trace(T[i] @ AdQ_Tj)))
    return R

# Verify: |T_0|^2 should be 1
assert abs(su2_norm_sq(T[0]) - 1.0) < 1e-12, f"Expected |T_0|^2=1, got {su2_norm_sq(T[0])}"
# Verify: <T_i, T_j> = delta_ij
for i in range(3):
    for j in range(3):
        inner = su2_inner(T[i], T[j])
        expected = 1.0 if i == j else 0.0
        assert abs(inner - expected) < 1e-12, f"<T_{i}, T_{j}> = {inner}, expected {expected}"
print("su(2) inner product: OK")

# ============================================================
# Lattice setup: L=2, d=4
# ============================================================
L = 2
d = 4
N_VERTICES = L**d  # 16

# Enumerate vertices as 4-tuples
vertices = list(product(range(L), repeat=d))
vertex_to_idx = {v: i for i, v in enumerate(vertices)}

def add_dir(x, mu):
    """x + e_mu mod L."""
    xl = list(x)
    xl[mu] = (xl[mu] + 1) % L
    return tuple(xl)

# Plane types (mu < nu)
plane_types = [(mu, nu) for mu in range(d) for nu in range(d) if mu < nu]
# 6 plane types: (0,1),(0,2),(0,3),(1,2),(1,3),(2,3)

# Active planes: mu+nu odd
active_planes = [(mu, nu) for mu, nu in plane_types if (mu + nu) % 2 == 1]
inactive_planes = [(mu, nu) for mu, nu in plane_types if (mu + nu) % 2 == 0]
print(f"Active planes: {active_planes}")
print(f"Inactive planes: {inactive_planes}")

# Enumerate all plaquettes as (x, mu, nu)
plaquettes = [(x, mu, nu) for x in vertices for mu, nu in plane_types]
N_PLAQ = len(plaquettes)
print(f"N_PLAQ = {N_PLAQ}")  # Should be 96

# Edge representation: (vertex, direction)
def edge_key(x, mu):
    return (x, mu)

# Build edge list
edges = [(x, mu) for x in vertices for mu in range(d)]
N_EDGES = len(edges)
print(f"N_EDGES = {N_EDGES}")  # Should be 64

# Staggered sign for edge (x, mu)
def stag_sign(x, mu):
    return (-1)**(sum(x) + mu)

# ============================================================
# B_□ computation
# ============================================================
n_fixed = T[0]  # Fixed su(2) direction: n = T_1

def get_plaquette_links(x, mu, nu):
    """
    Return (e1, e2, e3, e4) as (vertex, direction) tuples.
    e1 = (x, mu)       forward
    e2 = (x+mu, nu)    forward
    e3 = (x+nu, mu)    backward
    e4 = (x, nu)       backward
    """
    x_mu = add_dir(x, mu)
    x_nu = add_dir(x, nu)
    e1 = (x, mu)
    e2 = (x_mu, nu)
    e3 = (x_nu, mu)
    e4 = (x, nu)
    return e1, e2, e3, e4

def compute_B(links, x, mu, nu):
    """
    B_□(Q, v_stag) = c1*n + c2*Ad_{P1}(n) - c3*Ad_{P1*P2*P3^{-1}}(n) - c4*Ad_{U_□}(n)
    where partial holonomies: forward edges only include links up to them;
    backward edges include their OWN link in the partial holonomy.

    Specifically:
    - First term (e1, forward): c1 * n  [no transport yet]
    - Second term (e2, forward): c2 * Ad_{P1}(n)  [transported by P1]
    - Third term (e3, backward): -c3 * Ad_{P1 P2 P3^{-1}}(n)  [includes P3^{-1}]
    - Fourth term (e4, backward): -c4 * Ad_{U_□}(n)  [U_□ = P1 P2 P3^{-1} P4^{-1}]
    """
    e1, e2, e3, e4 = get_plaquette_links(x, mu, nu)

    c1 = stag_sign(*e1)
    c2 = stag_sign(*e2)
    c3 = stag_sign(*e3)
    c4 = stag_sign(*e4)

    P1 = links[e1]
    P2 = links[e2]
    P3 = links[e3]
    P4 = links[e4]

    P3dag = P3.conj().T
    P4dag = P4.conj().T

    P_12_3inv = P1 @ P2 @ P3dag          # P1 P2 P3^{-1}
    U_plaq = P_12_3inv @ P4dag             # U_□ = P1 P2 P3^{-1} P4^{-1}

    B = (c1 * n_fixed
         + c2 * adjoint(P1, n_fixed)
         - c3 * adjoint(P_12_3inv, n_fixed)
         - c4 * adjoint(U_plaq, n_fixed))

    return B

# ============================================================
# Precompute B at Q=I
# ============================================================
def make_identity_links():
    return {e: np.eye(2, dtype=complex) for e in edges}

I_links = make_identity_links()

B_I_sq = {}
for (x, mu, nu) in plaquettes:
    B = compute_B(I_links, x, mu, nu)
    B_I_sq[(x, mu, nu)] = su2_norm_sq(B)

# Verify: active planes should give 16, inactive should give 0
print("\nB^2 at Q=I by plane type:")
for (mu_p, nu_p) in plane_types:
    vals = [B_I_sq[(x, mu_p, nu_p)] for x in vertices]
    parity = "active (mu+nu odd)" if (mu_p + nu_p) % 2 == 1 else "inactive (mu+nu even)"
    print(f"  ({mu_p},{nu_p}) {parity}: min={min(vals):.4f}, max={max(vals):.4f}, sum={sum(vals):.4f}")

# ============================================================
# f_□(Q) computation
# ============================================================
def compute_f_plaquettes(links):
    """Compute f_□(Q) for all plaquettes. Returns array of shape (N_PLAQ,)."""
    f = np.zeros(N_PLAQ)
    for i, (x, mu, nu) in enumerate(plaquettes):
        B_Q = compute_B(links, x, mu, nu)
        B_sq_Q = su2_norm_sq(B_Q)
        f[i] = B_sq_Q - B_I_sq[(x, mu, nu)]
    return f

# ============================================================
# SU(2) random element generation
# ============================================================
def random_su2():
    """Haar-random SU(2) element."""
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    a, b, c, dd = q
    return np.array([[a + 1j*b, c + 1j*dd], [-c + 1j*dd, a - 1j*b]], dtype=complex)

def random_su2_near_identity(epsilon):
    """SU(2) near identity: exp(epsilon * X) for random X in su(2), |X|=1."""
    # Random unit vector in su(2)
    v = np.random.randn(3)
    v /= np.linalg.norm(v)
    X = sum(v[k] * T[k] for k in range(3))
    # exp(epsilon * X) where |X|^2 = 1
    # Use: exp(theta * n_hat) = cos(theta)*I + sin(theta)*n_hat/|n_hat| * sigma
    # Actually: exp(epsilon * X) where X = i*(v . sigma)/2
    # = cos(epsilon/2)*I + i*sin(epsilon/2)*(v . sigma) ... no wait
    # X = sum_k v_k * T_k = sum_k v_k * i*sigma_k/2 = i/2 * (v.sigma)
    # exp(epsilon * X) = exp(i*epsilon/2 * (v.sigma))
    #                  = cos(epsilon/2)*I + i*sin(epsilon/2)*(v.sigma)
    theta = epsilon / 2
    v_sigma = sum(v[k] * sigmas[k] for k in range(3))
    return np.cos(theta) * np.eye(2, dtype=complex) + 1j * np.sin(theta) * v_sigma

def make_random_config():
    return {e: random_su2() for e in edges}

def make_near_identity_config(epsilon):
    return {e: random_su2_near_identity(epsilon) for e in edges}

def make_gibbs_config(beta):
    """Simple Gibbs-like sampling: each link set to random SU(2) weighted by plaquette action."""
    # Use heat bath: for each link, pick proportional to exp(-beta * Re action)
    # For simplicity, use random near-identity with temperature-dependent scale
    # (crude approximation for illustration)
    # Actually, a proper heat bath is complex. Let's use: for each link,
    # set to exp(i * theta * n_hat) where theta ~ N(0, 1/sqrt(beta))
    sigma_theta = 1.0 / np.sqrt(max(beta, 0.01))
    links = {}
    for e in edges:
        # Random rotation angle
        theta = np.random.normal(0, sigma_theta)
        v = np.random.randn(3)
        v /= np.linalg.norm(v)
        # exp(theta * X) where X = sum_k v_k T_k
        half_theta = theta / 2
        v_sigma = sum(v[k] * sigmas[k] for k in range(3))
        links[e] = np.cos(half_theta) * np.eye(2, dtype=complex) + 1j * np.sin(half_theta) * v_sigma
    return links

def make_abelian_config():
    """Abelian (U(1)-like) configuration: all links are diagonal SU(2)."""
    links = {}
    for e in edges:
        theta = np.random.uniform(0, 2*np.pi)
        links[e] = np.array([[np.exp(1j*theta), 0], [0, np.exp(-1j*theta)]], dtype=complex)
    return links

# ============================================================
# Gradient ascent to find adversarial configs
# ============================================================
def gradient_ascent_config(n_steps=500, lr=0.05):
    """
    Find Q maximizing Sum_□ f_□(Q) via gradient ascent.
    Uses finite differences on Lie algebra.
    """
    links = make_random_config()

    for step in range(n_steps):
        f = compute_f_plaquettes(links)
        total = f.sum()

        # Compute gradient for each link
        new_links = {}
        for e in edges:
            # Perturb each of the 3 su(2) generators
            grads = np.zeros(3)
            for k in range(3):
                # Perturb: Q -> exp(eps*T_k) * Q
                eps = 1e-4
                Q_orig = links[e]
                # exp(eps*T_k) ≈ I + eps*T_k
                delta_links = dict(links)
                delta_links[e] = (np.eye(2, dtype=complex) + eps * T[k]) @ Q_orig
                # Re-normalize to SU(2)
                U = delta_links[e]
                det = np.linalg.det(U)
                delta_links[e] = U / np.sqrt(det)

                f_perturbed = compute_f_plaquettes(delta_links)
                grads[k] = (f_perturbed.sum() - total) / eps

            # Update: Q -> exp(lr * grad_k T_k) * Q
            grad_vec = grads
            grad_norm = np.linalg.norm(grad_vec)
            if grad_norm > 1e-10:
                grad_vec_normalized = grad_vec / grad_norm
                X = sum(grad_vec_normalized[k] * T[k] for k in range(3))
                angle = lr * grad_norm
                angle = min(angle, 0.5)  # clip
                half_angle = angle / 2
                v_sigma = sum(grad_vec_normalized[k] * sigmas[k] for k in range(3))
                exp_X = np.cos(half_angle) * np.eye(2, dtype=complex) + 1j * np.sin(half_angle) * v_sigma
                new_links[e] = exp_X @ links[e]
            else:
                new_links[e] = links[e]

        links = new_links

        if step % 100 == 0:
            f = compute_f_plaquettes(links)
            print(f"  Gradient ascent step {step}: Sum f = {f.sum():.6f}")

    return links

# ============================================================
# Analysis functions
# ============================================================
def analyze_config(links, name=""):
    """Compute f_□ for all plaquettes and compute statistics."""
    f = compute_f_plaquettes(links)

    stats = {
        'name': name,
        'sum': float(f.sum()),
        'n_positive': int(np.sum(f > 1e-10)),
        'n_negative': int(np.sum(f < -1e-10)),
        'n_zero': int(np.sum(np.abs(f) <= 1e-10)),
        'sum_positive': float(f[f > 1e-10].sum()) if np.any(f > 1e-10) else 0.0,
        'sum_negative': float(f[f < -1e-10].sum()) if np.any(f < -1e-10) else 0.0,
        'min': float(f.min()),
        'max': float(f.max()),
    }

    # Per-plane-type sums
    plane_sums = {}
    for mu_p, nu_p in plane_types:
        indices = [i for i, (x, mu, nu) in enumerate(plaquettes) if mu == mu_p and nu == nu_p]
        plane_sums[(mu_p, nu_p)] = float(f[indices].sum())
    stats['plane_sums'] = plane_sums

    # Per-vertex-star sums (sum over all plaquettes containing vertex x as one of its 4 corners)
    vertex_sums = {}
    for x_star in vertices:
        indices = []
        for i, (x, mu, nu) in enumerate(plaquettes):
            # Plaquette (x, mu, nu) has corners: x, x+mu, x+nu, x+mu+nu
            corners = [x, add_dir(x, mu), add_dir(x, nu), add_dir(add_dir(x, mu), nu)]
            if x_star in corners:
                indices.append(i)
        vertex_sums[x_star] = float(f[indices].sum())
    stats['vertex_sums'] = vertex_sums

    # Per-edge-star sums (sum over all plaquettes containing a specific edge)
    edge_sums = {}
    for edge in edges:
        indices = []
        e_vertex, e_dir = edge
        for i, (x, mu, nu) in enumerate(plaquettes):
            e1, e2, e3, e4 = get_plaquette_links(x, mu, nu)
            if edge in [e1, e2, e3, e4]:
                indices.append(i)
        edge_sums[edge] = float(f[indices].sum())
    stats['edge_sums'] = edge_sums

    # Per-cube sums (6 face plaquettes of each elementary cube)
    # Elementary cube at vertex x: 6 plaquettes in the 6 coordinate planes through x
    # Actually on L=2, each cube corresponds to a vertex: 16 cubes, each with 6 faces
    # But on L=2, plaquettes are shared between cubes more heavily
    # The 6 faces of cube at x are: (x, mu, nu) for all 6 plane types
    cube_sums = {}
    for x_cube in vertices:
        indices = [i for i, (x, mu, nu) in enumerate(plaquettes) if x == x_cube]
        cube_sums[x_cube] = float(f[indices].sum())
    stats['cube_sums'] = cube_sums

    return stats, f

def summarize_grouping(all_stats, grouping_key, group_label):
    """Check if a grouping gives per-group sum <= 0 for all configs."""
    print(f"\n=== {group_label} ===")
    any_positive = False
    max_positive = 0.0

    for stats in all_stats:
        group_sums = stats[grouping_key]
        for key, val in group_sums.items():
            if val > 1e-8:
                any_positive = True
                max_positive = max(max_positive, val)

    if not any_positive:
        print(f"  ALL GROUP SUMS <= 0! This is a potential proof route!")
    else:
        print(f"  Some group sums are positive (max = {max_positive:.4f})")
        # Print worst violators
        violating_configs = []
        for stats in all_stats:
            group_sums = stats[grouping_key]
            pos_vals = [(key, val) for key, val in group_sums.items() if val > 1e-8]
            if pos_vals:
                violating_configs.append((stats['name'], pos_vals))
        print(f"  Violating configs: {len(violating_configs)}/{len(all_stats)}")
        if violating_configs[:2]:
            print(f"  Example: {violating_configs[0][0]}: {violating_configs[0][1][:3]}")

# ============================================================
# Main computation
# ============================================================
print("\n" + "="*60)
print("MAIN COMPUTATION: f_□(Q) for diverse configs")
print("="*60)

all_stats = []
all_f_arrays = []

# 1. Identity config (trivial check)
stats, f = analyze_config(I_links, "identity")
all_stats.append(stats)
all_f_arrays.append(f)
print(f"\nIdentity: Sum f = {stats['sum']:.6f} (should be 0)")

# 2. Random Haar configs (10)
print("\nRandom Haar configs:")
for i in range(10):
    links = make_random_config()
    stats, f = analyze_config(links, f"random_haar_{i+1}")
    all_stats.append(stats)
    all_f_arrays.append(f)
    print(f"  random_{i+1}: Sum f = {stats['sum']:.6f}, #pos={stats['n_positive']}, max={stats['max']:.4f}")

# 3. Near-identity configs
print("\nNear-identity configs:")
epsilons = [0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, np.pi]
for eps in epsilons:
    links = make_near_identity_config(eps)
    stats, f = analyze_config(links, f"near_identity_eps{eps:.2f}")
    all_stats.append(stats)
    all_f_arrays.append(f)
    print(f"  eps={eps:.2f}: Sum f = {stats['sum']:.6f}, #pos={stats['n_positive']}, max={stats['max']:.4f}")

# 4. Gibbs-like configs (5 beta values)
print("\nGibbs-like configs:")
betas = [0.5, 1.0, 2.0, 3.0, 4.0]
for beta in betas:
    links = make_gibbs_config(beta)
    stats, f = analyze_config(links, f"gibbs_beta{beta:.1f}")
    all_stats.append(stats)
    all_f_arrays.append(f)
    print(f"  beta={beta}: Sum f = {stats['sum']:.6f}, #pos={stats['n_positive']}, max={stats['max']:.4f}")

# 5. Abelian configs (5)
print("\nAbelian configs:")
for i in range(5):
    links = make_abelian_config()
    stats, f = analyze_config(links, f"abelian_{i+1}")
    all_stats.append(stats)
    all_f_arrays.append(f)
    print(f"  abelian_{i+1}: Sum f = {stats['sum']:.6f}, #pos={stats['n_positive']}, max={stats['max']:.4f}")

# 6. Adversarial configs (gradient ascent)
print("\nAdversarial configs (gradient ascent to maximize Sum f):")
for i in range(5):
    print(f"\n  Adversarial config {i+1}:")
    links = gradient_ascent_config(n_steps=300, lr=0.02)
    stats, f = analyze_config(links, f"adversarial_{i+1}")
    all_stats.append(stats)
    all_f_arrays.append(f)
    print(f"  adversarial_{i+1}: Sum f = {stats['sum']:.6f}, #pos={stats['n_positive']}, max={stats['max']:.4f}")

print(f"\n\nTotal configs computed: {len(all_stats)}")

# ============================================================
# GROUPING ANALYSIS
# ============================================================
print("\n" + "="*60)
print("GROUPING ANALYSIS")
print("="*60)

# 1. Plane-type grouping
summarize_grouping(all_stats, 'plane_sums', "PLANE-TYPE GROUPING")
for stats in all_stats[:5]:
    psums = stats['plane_sums']
    vals = {str(k): f"{v:.4f}" for k, v in psums.items()}
    print(f"  {stats['name']}: {vals}")

# 2. Vertex-star grouping
summarize_grouping(all_stats, 'vertex_sums', "VERTEX-STAR GROUPING")

# 3. Edge-star grouping
summarize_grouping(all_stats, 'edge_sums', "EDGE-STAR GROUPING")

# 4. Cube-face grouping
summarize_grouping(all_stats, 'cube_sums', "CUBE-FACE GROUPING")

# ============================================================
# DETAILED PLANE-TYPE ANALYSIS
# ============================================================
print("\n" + "="*60)
print("DETAILED PLANE-TYPE ANALYSIS")
print("="*60)

print("\nPer-plane-type sums for all configs:")
header = f"{'Config':<35} " + " ".join(f"({m},{n})" for m,n in plane_types) + "  Total"
print(header)
print("-"*len(header))
for stats in all_stats:
    psums = [stats['plane_sums'][(m,n)] for m,n in plane_types]
    total = stats['sum']
    row = f"{stats['name']:<35} " + " ".join(f"{v:7.3f}" for v in psums) + f"  {total:7.3f}"
    print(row)

# ============================================================
# CORRELATION ANALYSIS: f_□ vs plaquette holonomy
# ============================================================
print("\n" + "="*60)
print("CORRELATION: f_□ vs. PLAQUETTE HOLONOMY")
print("="*60)

def compute_plaquette_holonomy_action(links):
    """Compute W_□ = 1 - Re Tr(U_□)/2 for each plaquette."""
    W = np.zeros(N_PLAQ)
    for i, (x, mu, nu) in enumerate(plaquettes):
        e1, e2, e3, e4 = get_plaquette_links(x, mu, nu)
        P1, P2, P3, P4 = links[e1], links[e2], links[e3], links[e4]
        U = P1 @ P2 @ P3.conj().T @ P4.conj().T
        W[i] = 1.0 - float(np.real(np.trace(U))) / 2.0
    return W

# Check correlation for one representative config
links_repr = make_random_config()
f_repr = compute_f_plaquettes(links_repr)
W_repr = compute_plaquette_holonomy_action(links_repr)
corr = np.corrcoef(W_repr, f_repr)[0, 1]
print(f"Correlation(W_□, f_□) for random config: {corr:.4f}")
print(f"  W_□ range: [{W_repr.min():.4f}, {W_repr.max():.4f}]")
print(f"  f_□ range: [{f_repr.min():.4f}, {f_repr.max():.4f}]")

# ============================================================
# COMBINED GROUPING: PLANE TYPE + VERTEX STAR
# ============================================================
print("\n" + "="*60)
print("COMBINED GROUPING ANALYSIS")
print("="*60)

# Check if any pairs of plane types always have negative sum together
for i, pt1 in enumerate(plane_types):
    for pt2 in plane_types[i+1:]:
        all_neg = True
        max_val = 0.0
        for stats in all_stats:
            val = stats['plane_sums'][pt1] + stats['plane_sums'][pt2]
            if val > 1e-8:
                all_neg = False
                max_val = max(max_val, val)
        if all_neg:
            print(f"  Planes {pt1}+{pt2}: ALWAYS <= 0")
        else:
            pass  # Don't print non-results to keep output clean

# ============================================================
# SIGN STRUCTURE AT Q=I
# ============================================================
print("\n" + "="*60)
print("STAGGERED SIGN STRUCTURE")
print("="*60)

print("\nc1+c2-c3-c4 values for each plaquette at Q=I:")
for mu_p, nu_p in plane_types:
    sums = []
    for x in vertices:
        e1, e2, e3, e4 = get_plaquette_links(x, mu_p, nu_p)
        c1 = stag_sign(*e1)
        c2 = stag_sign(*e2)
        c3 = stag_sign(*e3)
        c4 = stag_sign(*e4)
        S = c1 + c2 - c3 - c4
        sums.append(S)
    unique_sums = sorted(set(sums))
    count_pos = sum(1 for s in sums if s > 0)
    count_neg = sum(1 for s in sums if s < 0)
    count_zero = sum(1 for s in sums if s == 0)
    print(f"  Plane ({mu_p},{nu_p}): values = {unique_sums}, pos={count_pos}, neg={count_neg}, zero={count_zero}")
    print(f"    |B_I|^2 values: {sorted(set([round(v,4) for v in [B_I_sq[(x, mu_p, nu_p)] for x in vertices]]))}")

# ============================================================
# EXTREMAL CONFIGS ANALYSIS
# ============================================================
print("\n" + "="*60)
print("SUMMARY: MOST NEGATIVE Sum f_□")
print("="*60)

sorted_by_sum = sorted(all_stats, key=lambda s: s['sum'])
print("\nTop 10 most negative Sum f_□:")
for stats in sorted_by_sum[:10]:
    print(f"  {stats['name']:<35} Sum={stats['sum']:.4f}, max_f={stats['max']:.4f}, #pos={stats['n_positive']}")

print("\nAre any Sum f_□ > 0?")
positives = [s for s in all_stats if s['sum'] > 1e-8]
if positives:
    print(f"  YES! {len(positives)} configs have Sum f_□ > 0:")
    for s in positives:
        print(f"    {s['name']}: Sum = {s['sum']:.6f}")
else:
    print("  No, all Sum f_□ <= 0. Conjecture holds for all tested configs.")

print("\nAll done.")
