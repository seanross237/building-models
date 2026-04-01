"""
Focused analysis: The cube-face conjecture.

Conjecture: For each vertex x, Sum_{mu<nu} f_{(x,mu,nu)}(Q) <= 0 for all Q.

If true, this directly proves the global bound since {(x,mu,nu)} partitions all plaquettes.

This script:
1. Verifies cube-face is a partition
2. Tests with 500 Haar-random configs
3. Runs gradient ascent to maximize individual cube-face sums
4. Analyzes the single-link exact formula
5. Checks two-link and multi-link patterns
"""

import numpy as np
from itertools import product
import sys

np.random.seed(777)

# ============================================================
# Infrastructure
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
N_E = len(edges)

# ALL plaquettes, ordered as (x, mu, nu) for each x, for each (mu,nu)
plaquettes = [(x, mu, nu) for x in vertices for mu, nu in plane_types]
N_P = len(plaquettes)

def random_su2():
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    a, b, c, dd = q
    return np.array([[a + 1j*b, c + 1j*dd], [-c + 1j*dd, a - 1j*b]], dtype=complex)

def make_random_config():
    return {e: random_su2() for e in edges}

# ============================================================
# B_sq computation
# ============================================================
def compute_B(links, x, mu, nu):
    x_mu = add_dir(x, mu)
    x_nu = add_dir(x, nu)
    e1, e2, e3, e4 = (x, mu), (x_mu, nu), (x_nu, mu), (x, nu)
    c1, c2, c3, c4 = stag_sign(*e1), stag_sign(*e2), stag_sign(*e3), stag_sign(*e4)
    P1, P2, P3, P4 = links[e1], links[e2], links[e3], links[e4]
    P123 = P1 @ P2 @ P3.conj().T
    U = P123 @ P4.conj().T
    return (c1 * n_fixed + c2 * adjoint(P1, n_fixed)
            - c3 * adjoint(P123, n_fixed) - c4 * adjoint(U, n_fixed))

# Precompute |B(I)|^2
I_links = {e: I2.copy() for e in edges}
B_I_sq = np.zeros(N_P)
for i, (x, mu, nu) in enumerate(plaquettes):
    B_I_sq[i] = su2_norm_sq(compute_B(I_links, x, mu, nu))

def compute_f_array(links):
    f = np.zeros(N_P)
    for i, (x, mu, nu) in enumerate(plaquettes):
        f[i] = su2_norm_sq(compute_B(links, x, mu, nu)) - B_I_sq[i]
    return f

# ============================================================
# Cube-face indices: plaquettes (x, mu, nu) grouped by base vertex x
# Since plaquettes are ordered as: for each x, then for each (mu,nu),
# plaquette i belongs to vertex vertices[i // 6]
# ============================================================
cube_indices = {}
for v_idx, x in enumerate(vertices):
    cube_indices[x] = list(range(v_idx * 6, v_idx * 6 + 6))

# Verify partition
all_indices = []
for x in vertices:
    all_indices.extend(cube_indices[x])
assert sorted(all_indices) == list(range(N_P)), "Cube-face is not a valid partition!"
print("Cube-face partition verified: each plaquette belongs to exactly one cube.")

# Verify total
links_test = make_random_config()
f_test = compute_f_array(links_test)
cube_total = sum(f_test[cube_indices[x]].sum() for x in vertices)
direct_total = f_test.sum()
print(f"Partition check: cube_total={cube_total:.10f}, direct_total={direct_total:.10f}, diff={abs(cube_total - direct_total):.2e}")

# ============================================================
# Test 1: 500 random Haar configs
# ============================================================
print("\n" + "="*60)
print("TEST 1: Cube-face sums for 500 Haar-random configs")
print("="*60)

n_configs = 500
max_cube_sum = -1e10
violations = 0
cube_sum_max_per_config = np.zeros(n_configs)

for cfg in range(n_configs):
    links = make_random_config()
    f = compute_f_array(links)

    for x in vertices:
        cs = f[cube_indices[x]].sum()
        if cs > cube_sum_max_per_config[cfg]:
            cube_sum_max_per_config[cfg] = cs
        if cs > 1e-10:
            violations += 1
            if cs > max_cube_sum:
                max_cube_sum = cs

    if cfg % 100 == 0:
        print(f"  Config {cfg}: total={f.sum():.4f}, worst_cube={cube_sum_max_per_config[cfg]:.6f}")

print(f"\nResults:")
print(f"  Violations: {violations}/{n_configs * N_V}")
print(f"  Max cube-face sum: {max(max_cube_sum, cube_sum_max_per_config.max()):.6f}")
print(f"  Worst per-config cube-face max: {cube_sum_max_per_config.max():.6f}")

# ============================================================
# Test 2: Gradient ascent to maximize cube-face sum at x0
# ============================================================
print("\n" + "="*60)
print("TEST 2: Gradient ascent on cube-face sum at (0,0,0,0)")
print("="*60)

x0 = (0,0,0,0)
target_idxs = np.array(cube_indices[x0])

def cube_objective(links):
    f = compute_f_array(links)
    return f[target_idxs].sum()

def gradient_ascent_cube(n_steps=500, lr=0.03):
    links = make_random_config()
    best_val = -1e10
    best_links = None

    for step in range(n_steps):
        f = compute_f_array(links)
        current = f[target_idxs].sum()

        new_links = {}
        for e in edges:
            grads = np.zeros(3)
            for k in range(3):
                eps = 1e-4
                dl = dict(links)
                dl[e] = (I2 + eps * T[k]) @ links[e]
                det = np.linalg.det(dl[e])
                dl[e] = dl[e] / np.sqrt(det)
                f_p = compute_f_array(dl)
                grads[k] = (f_p[target_idxs].sum() - current) / eps

            gn = np.linalg.norm(grads)
            if gn > 1e-10:
                gnorm = grads / gn
                angle = min(lr * gn, 0.5)
                half = angle / 2
                vs = sum(gnorm[k] * sigmas[k] for k in range(3))
                exp_X = np.cos(half) * I2 + 1j * np.sin(half) * vs
                new_links[e] = exp_X @ links[e]
            else:
                new_links[e] = links[e]

        links = new_links

        if current > best_val:
            best_val = current
            best_links = {k: v.copy() for k, v in links.items()}

        if step % 100 == 0:
            f_now = compute_f_array(links)
            total = f_now.sum()
            cube_val = f_now[target_idxs].sum()
            print(f"  Step {step}: cube_sum={cube_val:.6f}, total={total:.4f}")

        # Decay LR
        if step == 200:
            lr *= 0.5
        if step == 350:
            lr *= 0.5

    return best_links, best_val

print("\nRunning 5 gradient ascent trials...")
ga_results = []
for trial in range(5):
    print(f"\n--- Trial {trial+1} ---")
    lr = 0.03
    best_links, best_val = gradient_ascent_cube(n_steps=500, lr=lr)
    ga_results.append(best_val)
    print(f"  Best cube-face sum: {best_val:.6f}")

    # Analyze the optimum
    f_opt = compute_f_array(best_links)
    print(f"  Per-plaquette at optimum:")
    for idx in target_idxs:
        x, mu, nu = plaquettes[idx]
        active = "ACT" if (mu + nu) % 2 == 1 else "INA"
        print(f"    ({x},{mu},{nu}) [{active}]: f={f_opt[idx]:.6f}")
    print(f"  Total sum: {f_opt.sum():.4f}")

    # Check ALL cubes at optimum
    all_cubes = [f_opt[cube_indices[x]].sum() for x in vertices]
    print(f"  All cube sums: min={min(all_cubes):.4f}, max={max(all_cubes):.6f}")
    n_pos = sum(1 for c in all_cubes if c > 1e-10)
    print(f"  Positive cubes: {n_pos}/{N_V}")

print(f"\nOverall best cube-face sum across all trials: {max(ga_results):.6f}")
print(f"Cube-face conjecture holds? {max(ga_results) <= 1e-6}")

# ============================================================
# Test 3: Single-link exact analysis
# ============================================================
print("\n" + "="*60)
print("TEST 3: Single-link exact formulas")
print("="*60)

# When only one link (x0, alpha) differs from I by rotation angle theta,
# compute the cube-face sum at x0 exactly.

x0 = (0,0,0,0)

for alpha in range(d):
    print(f"\n  Perturbed edge: ({x0}, {alpha})")
    thetas = np.linspace(0, np.pi, 50)
    cube_sums_theta = []

    for theta in thetas:
        links = {e: I2.copy() for e in edges}
        # Rotate around T_2 axis
        v = np.array([0, 1, 0])
        half = theta / 2
        vs = sum(v[k] * sigmas[k] for k in range(3))
        links[(x0, alpha)] = np.cos(half) * I2 + 1j * np.sin(half) * vs

        f = compute_f_array(links)
        cube_sums_theta.append(f[cube_indices[x0]].sum())

    cube_sums_theta = np.array(cube_sums_theta)
    print(f"    min cube_sum = {cube_sums_theta.min():.6f} at theta = {thetas[np.argmin(cube_sums_theta)]:.4f}")
    print(f"    max cube_sum = {cube_sums_theta.max():.6f} at theta = {thetas[np.argmax(cube_sums_theta)]:.4f}")
    print(f"    At theta=pi: cube_sum = {cube_sums_theta[-1]:.6f}")

    # Also check cube at x0 + e_alpha (the other affected vertex)
    x0_alpha = add_dir(x0, alpha)
    cube_sums_other = []
    for theta in thetas:
        links = {e: I2.copy() for e in edges}
        v = np.array([0, 1, 0])
        half = theta / 2
        vs = sum(v[k] * sigmas[k] for k in range(3))
        links[(x0, alpha)] = np.cos(half) * I2 + 1j * np.sin(half) * vs

        f = compute_f_array(links)
        cube_sums_other.append(f[cube_indices[x0_alpha]].sum())

    cube_sums_other = np.array(cube_sums_other)
    print(f"    Neighbor cube ({x0_alpha}): max = {cube_sums_other.max():.6f}")

# ============================================================
# Test 4: Two-link analysis
# ============================================================
print("\n" + "="*60)
print("TEST 4: Two-link adversarial search")
print("="*60)

# Perturb two links sharing a vertex, search for positive cube-face sum
x0 = (0,0,0,0)
n_trials_2link = 10000

max_cube_2link = -1e10
for trial in range(n_trials_2link):
    # Pick two random edges from x0
    alpha = np.random.randint(d)
    beta = np.random.randint(d)
    theta1 = np.random.uniform(0, 2*np.pi)
    theta2 = np.random.uniform(0, 2*np.pi)

    links = {e: I2.copy() for e in edges}

    v1 = np.random.randn(3); v1 /= np.linalg.norm(v1)
    half1 = theta1 / 2
    vs1 = sum(v1[k] * sigmas[k] for k in range(3))
    links[(x0, alpha)] = np.cos(half1) * I2 + 1j * np.sin(half1) * vs1

    v2 = np.random.randn(3); v2 /= np.linalg.norm(v2)
    half2 = theta2 / 2
    vs2 = sum(v2[k] * sigmas[k] for k in range(3))
    links[(x0, beta)] = np.cos(half2) * I2 + 1j * np.sin(half2) * vs2

    f = compute_f_array(links)
    cs = f[cube_indices[x0]].sum()
    if cs > max_cube_2link:
        max_cube_2link = cs

print(f"Two-link search (10000 trials): max cube-face sum = {max_cube_2link:.6f}")
print(f"Cube-face conjecture holds? {max_cube_2link <= 1e-6}")

# Also try all-links at x0 perturbed
print("\n  All 4 links at x0 perturbed (10000 trials):")
max_cube_4link = -1e10
for trial in range(n_trials_2link):
    links = {e: I2.copy() for e in edges}
    for alpha in range(d):
        theta = np.random.uniform(0, 2*np.pi)
        v = np.random.randn(3); v /= np.linalg.norm(v)
        half = theta / 2
        vs = sum(v[k] * sigmas[k] for k in range(3))
        links[(x0, alpha)] = np.cos(half) * I2 + 1j * np.sin(half) * vs

    f = compute_f_array(links)
    cs = f[cube_indices[x0]].sum()
    if cs > max_cube_4link:
        max_cube_4link = cs

print(f"  Max cube-face sum = {max_cube_4link:.6f}")
print(f"  Cube-face conjecture holds? {max_cube_4link <= 1e-6}")

# Also perturb all links incident to the plaquettes at x0
print("\n  All edges touching cube at x0 perturbed (5000 trials):")
# The edges of plaquettes at x0 include: (x0, mu) for all mu, plus neighbors
cube_edges = set()
for mu, nu in plane_types:
    x_mu = add_dir(x0, mu)
    x_nu = add_dir(x0, nu)
    cube_edges.add((x0, mu))
    cube_edges.add((x_mu, nu))
    cube_edges.add((x_nu, mu))
    cube_edges.add((x0, nu))
print(f"  Edges in cube: {len(cube_edges)}")

max_cube_full = -1e10
for trial in range(5000):
    links = {e: I2.copy() for e in edges}
    for e in cube_edges:
        theta = np.random.uniform(0, 2*np.pi)
        v = np.random.randn(3); v /= np.linalg.norm(v)
        half = theta / 2
        vs = sum(v[k] * sigmas[k] for k in range(3))
        links[e] = np.cos(half) * I2 + 1j * np.sin(half) * vs

    f = compute_f_array(links)
    cs = f[cube_indices[x0]].sum()
    if cs > max_cube_full:
        max_cube_full = cs

print(f"  Max cube-face sum = {max_cube_full:.6f}")
print(f"  Cube-face conjecture holds? {max_cube_full <= 1e-6}")

# ============================================================
# Test 5: Check H_norm for cube-face
# ============================================================
print("\n" + "="*60)
print("TEST 5: Cube-face H_norm")
print("="*60)

# At Q=I, each cube contributes |B_I|^2 = 4 * 16 + 2 * 0 = 64 (4 active + 2 inactive)
# Total = 16 * 64 = 1024 = 4d * |v|^2

# Conjecture: for each x, Sum_{mu<nu} |B_{(x,mu,nu)}(Q,v)|^2 <= 64 for all Q
# Equivalently: cube-face H_norm = Sum_{mu<nu} |B_{(x,mu,nu)}|^2 / (4d * |v|^2 / N_V) <= 1

print(f"At Q=I:")
for x in vertices[:4]:
    total_B_at_I = sum(B_I_sq[cube_indices[x]])
    print(f"  Cube {x}: Sum |B_I|^2 = {total_B_at_I:.4f}")

print(f"\nAt random Q (5 configs):")
for cfg in range(5):
    links = make_random_config()
    f = compute_f_array(links)
    for x in [x0]:
        cube_B_sq = sum(su2_norm_sq(compute_B(links, *plaquettes[i])) for i in cube_indices[x])
        cube_f = f[cube_indices[x]].sum()
        cube_B_at_I = sum(B_I_sq[cube_indices[x]])
        print(f"  Config {cfg}, Cube {x}: |B_Q|^2={cube_B_sq:.4f}, |B_I|^2={cube_B_at_I:.4f}, f={cube_f:.4f}, ratio={cube_B_sq/cube_B_at_I:.6f}")

print("\n--- Analysis complete ---")
