"""
Stress-test the vertex-star and cube-face grouping conjectures with:
1. 500 random Haar configs
2. Gradient ascent to maximize individual vertex-star sums
3. Gradient ascent to maximize individual cube-face sums
"""

import numpy as np
from itertools import product

np.random.seed(123)

# ============================================================
# Minimal infrastructure (self-contained)
# ============================================================
sigma1 = np.array([[0, 1], [1, 0]], dtype=complex)
sigma2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma3 = np.array([[1, 0], [0, -1]], dtype=complex)
sigmas = [sigma1, sigma2, sigma3]
T = [1j/2 * s for s in sigmas]
I2 = np.eye(2, dtype=complex)

def su2_norm_sq(A):
    return float(np.real(-2 * np.trace(A @ A)))

def adjoint(Q, A):
    return Q @ A @ Q.conj().T

L = 2
d = 4
vertices = list(product(range(L), repeat=d))
N_V = L**d
plane_types = [(mu, nu) for mu in range(d) for nu in range(d) if mu < nu]
n_fixed = T[0]

def add_dir(x, mu):
    xl = list(x)
    xl[mu] = (xl[mu] + 1) % L
    return tuple(xl)

def stag_sign(x, mu):
    return (-1)**(sum(x) + mu)

edges = [(x, mu) for x in vertices for mu in range(d)]
plaquettes = [(x, mu, nu) for x in vertices for mu, nu in plane_types]
N_PLAQ = len(plaquettes)

def random_su2():
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    a, b, c, dd = q
    return np.array([[a + 1j*b, c + 1j*dd], [-c + 1j*dd, a - 1j*b]], dtype=complex)

def make_random_config():
    return {e: random_su2() for e in edges}

def make_identity_config():
    return {e: I2.copy() for e in edges}

def get_plaquette_links(x, mu, nu):
    x_mu = add_dir(x, mu)
    x_nu = add_dir(x, nu)
    return (x, mu), (x_mu, nu), (x_nu, mu), (x, nu)

def compute_B(links, x, mu, nu):
    e1, e2, e3, e4 = get_plaquette_links(x, mu, nu)
    c1 = stag_sign(*e1)
    c2 = stag_sign(*e2)
    c3 = stag_sign(*e3)
    c4 = stag_sign(*e4)
    P1, P2, P3, P4 = links[e1], links[e2], links[e3], links[e4]
    P_12_3inv = P1 @ P2 @ P3.conj().T
    U_plaq = P_12_3inv @ P4.conj().T
    B = (c1 * n_fixed + c2 * adjoint(P1, n_fixed)
         - c3 * adjoint(P_12_3inv, n_fixed) - c4 * adjoint(U_plaq, n_fixed))
    return B

# Precompute B at I
I_links = make_identity_config()
B_I_sq = {}
for (x, mu, nu) in plaquettes:
    B = compute_B(I_links, x, mu, nu)
    B_I_sq[(x, mu, nu)] = su2_norm_sq(B)

def compute_f_array(links):
    """Returns f_□ for all plaquettes as numpy array."""
    f = np.zeros(N_PLAQ)
    for i, (x, mu, nu) in enumerate(plaquettes):
        B_Q = compute_B(links, x, mu, nu)
        f[i] = su2_norm_sq(B_Q) - B_I_sq[(x, mu, nu)]
    return f

# ============================================================
# Build vertex-star and cube-face index maps
# ============================================================

# Vertex-star: all plaquettes with x as one of their 4 corners
vertex_star_indices = {x: [] for x in vertices}
for i, (x, mu, nu) in enumerate(plaquettes):
    corners = [x, add_dir(x, mu), add_dir(x, nu), add_dir(add_dir(x, mu), nu)]
    for c in corners:
        vertex_star_indices[c].append(i)

# Cube-face: the 6 plaquettes based at vertex x
cube_face_indices = {x: [] for x in vertices}
for i, (x, mu, nu) in enumerate(plaquettes):
    cube_face_indices[x].append(i)

# Verify sizes
vstar_sizes = set(len(vertex_star_indices[x]) for x in vertices)
cube_sizes = set(len(cube_face_indices[x]) for x in vertices)
print(f"Vertex-star sizes: {vstar_sizes}")
print(f"Cube-face sizes: {cube_sizes}")

# ============================================================
# Test 1: 500 random Haar configs
# ============================================================
print("\n" + "="*60)
print("TEST 1: 500 random Haar configs")
print("="*60)

n_configs = 500
vstar_max_per_config = np.zeros(n_configs)
cube_max_per_config = np.zeros(n_configs)
total_sum_per_config = np.zeros(n_configs)

vstar_violations = 0
cube_violations = 0

for cfg in range(n_configs):
    links = make_random_config()
    f = compute_f_array(links)
    total_sum_per_config[cfg] = f.sum()

    for x in vertices:
        vs = f[vertex_star_indices[x]].sum()
        if vs > vstar_max_per_config[cfg]:
            vstar_max_per_config[cfg] = vs
        if vs > 1e-10:
            vstar_violations += 1

        cs = f[cube_face_indices[x]].sum()
        if cs > cube_max_per_config[cfg]:
            cube_max_per_config[cfg] = cs
        if cs > 1e-10:
            cube_violations += 1

    if cfg % 100 == 0:
        print(f"  Config {cfg}: total_sum={f.sum():.4f}, vstar_max={vstar_max_per_config[cfg]:.6f}, cube_max={cube_max_per_config[cfg]:.6f}")

print(f"\nResults over {n_configs} configs:")
print(f"  Total sum: min={total_sum_per_config.min():.4f}, max={total_sum_per_config.max():.4f}")
print(f"  Vertex-star max: min={vstar_max_per_config.min():.6f}, max={vstar_max_per_config.max():.6f}")
print(f"  Cube-face max: min={cube_max_per_config.min():.6f}, max={cube_max_per_config.max():.6f}")
print(f"  Vertex-star violations: {vstar_violations}/{n_configs * N_V}")
print(f"  Cube-face violations: {cube_violations}/{n_configs * N_V}")

# ============================================================
# Test 2: Gradient ascent to maximize a specific vertex-star sum
# ============================================================
print("\n" + "="*60)
print("TEST 2: Gradient ascent on vertex-star sum for vertex (0,0,0,0)")
print("="*60)

target_vertex = (0,0,0,0)
target_indices = vertex_star_indices[target_vertex]
print(f"Vertex star of {target_vertex} has {len(target_indices)} plaquettes")

def compute_vertex_star_sum(links, v_idx_list):
    """Compute sum of f_□ over plaquettes in the vertex star."""
    f = compute_f_array(links)
    return f[v_idx_list].sum()

def gradient_ascent_vertex_star(target_idxs, n_steps=500, lr=0.02):
    links = make_random_config()

    for step in range(n_steps):
        f = compute_f_array(links)
        current = f[target_idxs].sum()

        new_links = {}
        for e in edges:
            grads = np.zeros(3)
            for k in range(3):
                eps = 1e-4
                delta_links = dict(links)
                delta_links[e] = (I2 + eps * T[k]) @ links[e]
                det = np.linalg.det(delta_links[e])
                delta_links[e] = delta_links[e] / np.sqrt(det)
                f_pert = compute_f_array(delta_links)
                grads[k] = (f_pert[target_idxs].sum() - current) / eps

            grad_norm = np.linalg.norm(grads)
            if grad_norm > 1e-10:
                gn = grads / grad_norm
                angle = min(lr * grad_norm, 0.5)
                half = angle / 2
                v_sigma = sum(gn[k] * sigmas[k] for k in range(3))
                exp_X = np.cos(half) * I2 + 1j * np.sin(half) * v_sigma
                new_links[e] = exp_X @ links[e]
            else:
                new_links[e] = links[e]

        links = new_links

        if step % 100 == 0:
            f = compute_f_array(links)
            vs_sum = f[target_idxs].sum()
            total = f.sum()
            print(f"  Step {step}: vstar_sum={vs_sum:.6f}, total_sum={total:.4f}")

    return links

print("\nRunning 3 gradient ascent trials on vertex-star sum...")
ga_vstar_results = []
for trial in range(3):
    print(f"\n  Trial {trial+1}:")
    links_opt = gradient_ascent_vertex_star(target_indices, n_steps=500, lr=0.02)
    f_opt = compute_f_array(links_opt)
    vs_sum = f_opt[target_indices].sum()
    total = f_opt.sum()
    ga_vstar_results.append((vs_sum, total))
    print(f"  Final: vstar_sum={vs_sum:.6f}, total={total:.4f}")

    # Check ALL vertex stars at this optimum
    print(f"  All vertex-star sums at optimum:")
    for x in vertices:
        s = f_opt[vertex_star_indices[x]].sum()
        if s > 1e-10:
            print(f"    {x}: {s:.6f} POSITIVE!")
        elif abs(s) < 0.01:
            print(f"    {x}: {s:.6f} (near zero)")

# ============================================================
# Test 3: Gradient ascent to maximize a specific cube-face sum
# ============================================================
print("\n" + "="*60)
print("TEST 3: Gradient ascent on cube-face sum for vertex (0,0,0,0)")
print("="*60)

target_cube_indices = cube_face_indices[target_vertex]
print(f"Cube-face at {target_vertex} has {len(target_cube_indices)} plaquettes")

def gradient_ascent_cube_face(target_idxs, n_steps=500, lr=0.02):
    links = make_random_config()

    for step in range(n_steps):
        f = compute_f_array(links)
        current = f[target_idxs].sum()

        new_links = {}
        for e in edges:
            grads = np.zeros(3)
            for k in range(3):
                eps = 1e-4
                delta_links = dict(links)
                delta_links[e] = (I2 + eps * T[k]) @ links[e]
                det = np.linalg.det(delta_links[e])
                delta_links[e] = delta_links[e] / np.sqrt(det)
                f_pert = compute_f_array(delta_links)
                grads[k] = (f_pert[target_idxs].sum() - current) / eps

            grad_norm = np.linalg.norm(grads)
            if grad_norm > 1e-10:
                gn = grads / grad_norm
                angle = min(lr * grad_norm, 0.5)
                half = angle / 2
                v_sigma = sum(gn[k] * sigmas[k] for k in range(3))
                exp_X = np.cos(half) * I2 + 1j * np.sin(half) * v_sigma
                new_links[e] = exp_X @ links[e]
            else:
                new_links[e] = links[e]

        links = new_links

        if step % 100 == 0:
            f = compute_f_array(links)
            cf_sum = f[target_idxs].sum()
            total = f.sum()
            print(f"  Step {step}: cube_sum={cf_sum:.6f}, total_sum={total:.4f}")

    return links

print("\nRunning 3 gradient ascent trials on cube-face sum...")
ga_cube_results = []
for trial in range(3):
    print(f"\n  Trial {trial+1}:")
    links_opt = gradient_ascent_cube_face(target_cube_indices, n_steps=500, lr=0.02)
    f_opt = compute_f_array(links_opt)
    cf_sum = f_opt[target_cube_indices].sum()
    total = f_opt.sum()
    ga_cube_results.append((cf_sum, total))
    print(f"  Final: cube_sum={cf_sum:.6f}, total={total:.4f}")

    # Show per-plaquette breakdown of the optimized cube
    print(f"  Per-plaquette at optimum:")
    for idx in target_cube_indices:
        x, mu, nu = plaquettes[idx]
        print(f"    ({x},{mu},{nu}): f={f_opt[idx]:.6f}")

    # Check ALL cube-face sums at this optimum
    worst_cube = max(f_opt[cube_face_indices[x]].sum() for x in vertices)
    print(f"  Worst cube-face sum across all vertices: {worst_cube:.6f}")

# ============================================================
# Test 4: Edge-sharing pair analysis for active plaquettes
# ============================================================
print("\n" + "="*60)
print("TEST 4: Edge-sharing pair analysis (active plaquettes only)")
print("="*60)

# Build pairs of active plaquettes sharing an edge
active_mask = np.array([(mu + nu) % 2 == 1 for (x, mu, nu) in plaquettes])
active_indices = np.where(active_mask)[0]

edge_to_active = {}
for idx in active_indices:
    x, mu, nu = plaquettes[idx]
    for e in get_plaquette_links(x, mu, nu):
        if e not in edge_to_active:
            edge_to_active[e] = []
        edge_to_active[e].append(idx)

pairs = set()
for e, plaqs in edge_to_active.items():
    for i in range(len(plaqs)):
        for j in range(i+1, len(plaqs)):
            pairs.add((min(plaqs[i], plaqs[j]), max(plaqs[i], plaqs[j])))

print(f"Total edge-sharing active pairs: {len(pairs)}")

# Test with 200 configs
n_test = 200
pair_max = {}
for pair in pairs:
    pair_max[pair] = -1e10

for cfg in range(n_test):
    links = make_random_config()
    f = compute_f_array(links)
    for pair in pairs:
        s = f[pair[0]] + f[pair[1]]
        if s > pair_max[pair]:
            pair_max[pair] = s

n_always_neg = sum(1 for v in pair_max.values() if v <= 1e-10)
n_sometimes_pos = sum(1 for v in pair_max.values() if v > 1e-10)
print(f"Pairs always ≤ 0: {n_always_neg}/{len(pairs)}")
print(f"Pairs sometimes > 0: {n_sometimes_pos}/{len(pairs)}")

worst_pairs = sorted(pair_max.items(), key=lambda t: -t[1])[:10]
print(f"\nWorst 10 edge-sharing pairs:")
for pair, mx in worst_pairs:
    x1, m1, n1 = plaquettes[pair[0]]
    x2, m2, n2 = plaquettes[pair[1]]
    print(f"  ({x1},{m1},{n1}) + ({x2},{m2},{n2}): max_sum = {mx:.4f}")

# ============================================================
# Test 5: Link-star analysis (per-link sum)
# ============================================================
print("\n" + "="*60)
print("TEST 5: Link-star stress test (500 configs)")
print("="*60)

edge_star_indices = {e: [] for e in edges}
for i, (x, mu, nu) in enumerate(plaquettes):
    for e in get_plaquette_links(x, mu, nu):
        edge_star_indices[e].append(i)

lstar_max = {e: -1e10 for e in edges}
lstar_violations = 0

for cfg in range(n_configs):
    links = make_random_config()
    f = compute_f_array(links)
    for e in edges:
        s = f[edge_star_indices[e]].sum()
        if s > lstar_max[e]:
            lstar_max[e] = s
        if s > 1e-10:
            lstar_violations += 1

n_always_neg_e = sum(1 for v in lstar_max.values() if v <= 1e-10)
max_lstar = max(lstar_max.values())
print(f"Link-star violations: {lstar_violations}/{n_configs * len(edges)}")
print(f"Links with star always ≤ 0: {n_always_neg_e}/{len(edges)}")
print(f"Max link-star sum seen: {max_lstar:.6f}")

# Show worst links
worst_links = sorted(lstar_max.items(), key=lambda t: -t[1])[:10]
print(f"\nWorst 10 link stars:")
for e, mx in worst_links:
    print(f"  edge {e}: max_sum = {mx:.6f}")

print("\nAll stress tests complete.")
