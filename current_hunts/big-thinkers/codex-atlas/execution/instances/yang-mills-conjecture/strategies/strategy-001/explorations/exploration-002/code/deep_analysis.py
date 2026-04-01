"""
Deep analysis of the cube-face grouping:
∑_{μ<ν} f_{(x,μ,ν)}(Q) ≤ 0 for all x, Q

Goals:
1. Stress test with 10000 random configs
2. Gradient ascent targeting individual cube-face sums
3. Algebraic analysis: what combination of links enters each cube sum
4. Per-vertex, per-plane sign structure
5. Minimal grouping analysis: can we split further?
"""

import numpy as np
from itertools import product
import sys

np.random.seed(123)

# ============================================================
# Reusable infrastructure (copied from main script)
# ============================================================
sigma1 = np.array([[0, 1], [1, 0]], dtype=complex)
sigma2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma3 = np.array([[1, 0], [0, -1]], dtype=complex)
sigmas = [sigma1, sigma2, sigma3]
T = [1j/2 * s for s in sigmas]

def su2_norm_sq(A):
    return float(np.real(-2 * np.trace(A @ A)))

def adjoint(Q, A):
    return Q @ A @ Q.conj().T

L, d = 2, 4
vertices = list(product(range(L), repeat=d))
plane_types = [(mu, nu) for mu in range(d) for nu in range(d) if mu < nu]
plaquettes = [(x, mu, nu) for x in vertices for mu, nu in plane_types]
N_PLAQ = len(plaquettes)
edges = [(x, mu) for x in vertices for mu in range(d)]

def add_dir(x, mu):
    xl = list(x)
    xl[mu] = (xl[mu] + 1) % L
    return tuple(xl)

def stag_sign(x, mu):
    return (-1)**(sum(x) + mu)

def get_plaquette_links(x, mu, nu):
    x_mu = add_dir(x, mu)
    x_nu = add_dir(x, nu)
    return (x, mu), (x_mu, nu), (x_nu, mu), (x, nu)

n_fixed = T[0]

def make_identity_links():
    return {e: np.eye(2, dtype=complex) for e in edges}

I_links = make_identity_links()

def compute_B(links, x, mu, nu):
    e1, e2, e3, e4 = get_plaquette_links(x, mu, nu)
    c1 = stag_sign(*e1); c2 = stag_sign(*e2)
    c3 = stag_sign(*e3); c4 = stag_sign(*e4)
    P1, P2, P3, P4 = links[e1], links[e2], links[e3], links[e4]
    P_123 = P1 @ P2 @ P3.conj().T
    U = P_123 @ P4.conj().T
    return (c1*n_fixed + c2*adjoint(P1, n_fixed)
            - c3*adjoint(P_123, n_fixed) - c4*adjoint(U, n_fixed))

# Precompute B_I^2
B_I_sq = {(x,mu,nu): su2_norm_sq(compute_B(I_links, x, mu, nu)) for x,mu,nu in plaquettes}

def f_plaquette(links, x, mu, nu):
    return su2_norm_sq(compute_B(links, x, mu, nu)) - B_I_sq[(x,mu,nu)]

def cube_face_sum(links, x_cube):
    """Sum f_{(x,mu,nu)} over all 6 plane types at base vertex x_cube."""
    return sum(f_plaquette(links, x_cube, mu, nu) for mu, nu in plane_types)

def all_cube_sums(links):
    return {x: cube_face_sum(links, x) for x in vertices}

# Verify: cube face sums partition the plaquettes
# Each plaquette (x, mu, nu) is in exactly one cube (at x)
total_plaq_count = sum(len(plane_types) for _ in vertices)
assert total_plaq_count == N_PLAQ, f"{total_plaq_count} != {N_PLAQ}"
print(f"Partition check: each plaquette has unique base vertex. Total = {total_plaq_count} = {N_PLAQ}. OK")

def random_su2():
    q = np.random.randn(4); q /= np.linalg.norm(q)
    a, b, c, dd = q
    return np.array([[a+1j*b, c+1j*dd], [-c+1j*dd, a-1j*b]], dtype=complex)

def random_config():
    return {e: random_su2() for e in edges}

# ============================================================
# STRESS TEST 1: 10000 random configs
# ============================================================
print("\n" + "="*60)
print("STRESS TEST: 10000 Random Haar Configs")
print("="*60)

N_STRESS = 10000
max_cube_sum = -np.inf
max_total_sum = -np.inf
worst_cube = None
n_violations_cube = 0
n_violations_total = 0

for i in range(N_STRESS):
    links = random_config()
    csums = all_cube_sums(links)
    total = sum(csums.values())

    for x, val in csums.items():
        if val > 1e-8:
            n_violations_cube += 1
            if val > max_cube_sum:
                max_cube_sum = val
                worst_cube = (x, val, total)
    if total > 1e-8:
        n_violations_total += 1
        max_total_sum = max(max_total_sum, total)

    if (i+1) % 1000 == 0:
        print(f"  After {i+1} configs: cube violations = {n_violations_cube}, "
              f"total violations = {n_violations_total}, "
              f"max_cube_sum = {max_cube_sum:.6f}")

print(f"\nFinal after {N_STRESS} configs:")
print(f"  Cube-face violations: {n_violations_cube}")
print(f"  Total violations: {n_violations_total}")
print(f"  Max cube-face sum: {max_cube_sum:.8f}")
if worst_cube:
    print(f"  Worst cube: vertex={worst_cube[0]}, cube_sum={worst_cube[1]:.6f}, total={worst_cube[2]:.4f}")

# ============================================================
# STRESS TEST 2: Near-identity at many epsilons
# ============================================================
print("\n" + "="*60)
print("STRESS TEST: Near-identity at large epsilon")
print("="*60)

for eps in [np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]:
    max_cube = -np.inf
    for _ in range(1000):
        v = np.random.randn(3); v /= np.linalg.norm(v)
        X = sum(v[k]*T[k] for k in range(3))
        half = eps/2
        v_sigma = sum(v[k]*sigmas[k] for k in range(3))
        links = {e: np.cos(half)*np.eye(2,dtype=complex) + 1j*np.sin(half)*v_sigma
                 for e in edges}
        csums = all_cube_sums(links)
        max_cube = max(max_cube, max(csums.values()))
    print(f"  eps={eps:.3f}: max cube sum = {max_cube:.6f}")

# ============================================================
# ADVERSARIAL: Gradient ascent targeting a single cube-face sum
# ============================================================
print("\n" + "="*60)
print("ADVERSARIAL: Maximize cube-face sum at x=(0,0,0,0)")
print("="*60)

x_target = (0, 0, 0, 0)

def grad_ascent_cube(target_vertex, n_steps=500, lr=0.01):
    links = random_config()
    for step in range(n_steps):
        val = cube_face_sum(links, target_vertex)
        new_links = {}
        for e in edges:
            grads = np.zeros(3)
            eps_finite = 1e-4
            for k in range(3):
                delta_links = dict(links)
                Q_orig = links[e]
                # Perturb: Q -> exp(eps*T_k) * Q
                U_perturb = (np.eye(2, dtype=complex) + eps_finite * T[k]) @ Q_orig
                # Normalize to SU(2)
                det = np.linalg.det(U_perturb)
                delta_links[e] = U_perturb / np.sqrt(det)
                val_p = cube_face_sum(delta_links, target_vertex)
                grads[k] = (val_p - val) / eps_finite
            grad_norm = np.linalg.norm(grads)
            if grad_norm > 1e-10:
                gn = grads / grad_norm
                X = sum(gn[k]*T[k] for k in range(3))
                angle = min(lr * grad_norm, 0.3)
                v_sigma = sum(gn[k]*sigmas[k] for k in range(3))
                half = angle/2
                exp_X = np.cos(half)*np.eye(2,dtype=complex) + 1j*np.sin(half)*v_sigma
                new_links[e] = exp_X @ links[e]
            else:
                new_links[e] = links[e]
        links = new_links
        if step % 100 == 0:
            print(f"  Step {step}: cube_sum = {val:.6f}")
    return links, cube_face_sum(links, target_vertex)

links_adv, adv_sum = grad_ascent_cube(x_target, n_steps=500, lr=0.02)
print(f"  Final cube sum at {x_target}: {adv_sum:.6f}")
print(f"  Total sum: {sum(all_cube_sums(links_adv).values()):.4f}")

# ============================================================
# ALGEBRAIC ANALYSIS: Cube-face sum formula
# ============================================================
print("\n" + "="*60)
print("ALGEBRAIC ANALYSIS: cube-face sum at fixed vertex")
print("="*60)

# At Q=I: cube_face sum = sum_{mu<nu} [(c1+c2-c3-c4)^2 - (c1+c2-c3-c4)^2] = 0
# The S(x) = sum_{mu<nu} |B_{x,mu,nu}(Q)|^2 - 64
# where the 64 comes from 4 active planes × 16

# What are the B_I^2 values per vertex?
print("\nB_I^2 values per plane type per vertex (confirming 16 for active, 0 for inactive):")
for mu_p, nu_p in plane_types:
    vals_per_vertex = {x: B_I_sq[(x, mu_p, nu_p)] for x in vertices}
    unique_vals = sorted(set(round(v, 6) for v in vals_per_vertex.values()))
    print(f"  ({mu_p},{nu_p}): {unique_vals}")

# The cube-face sum at x:
# S(x) = sum_{mu<nu} |B_{x,mu,nu}(Q)|^2 - sum_{mu<nu} |B_{x,mu,nu}(I)|^2
# = sum_{mu<nu} |B_{x,mu,nu}(Q)|^2 - 64  (for any x)

# Let's examine B_{x,mu,nu}(Q) for all plane types at x=0000
x0 = (0,0,0,0)
links_test = random_config()
print(f"\nFor random config at x=(0,0,0,0):")
total_Bsq = 0
for mu_p, nu_p in plane_types:
    B = compute_B(links_test, x0, mu_p, nu_p)
    Bsq = su2_norm_sq(B)
    fval = f_plaquette(links_test, x0, mu_p, nu_p)
    total_Bsq += Bsq
    print(f"  Plane ({mu_p},{nu_p}): |B|^2 = {Bsq:.4f}, f = {fval:.4f}")
print(f"  Sum |B|^2 = {total_Bsq:.4f}, should be <= 64")
print(f"  cube_face_sum = {cube_face_sum(links_test, x0):.4f}")

# ============================================================
# KEY QUESTION: What are the links in the cube-face sum?
# The cube at x involves links at x, x+e0, x+e1, x+e2, x+e3
# and cross-links between them
# ============================================================
print("\n" + "="*60)
print("LINK STRUCTURE OF CUBE-FACE SUM")
print("="*60)

x0 = (0,0,0,0)
all_links_in_cube = set()
for mu_p, nu_p in plane_types:
    e1, e2, e3, e4 = get_plaquette_links(x0, mu_p, nu_p)
    all_links_in_cube.update([e1, e2, e3, e4])

print(f"Cube at x={x0} involves {len(all_links_in_cube)} distinct links:")
for e in sorted(all_links_in_cube, key=lambda e: (sum(e[0]), e[0], e[1])):
    print(f"  {e}")

# Group links by vertex
by_vertex = {}
for (xv, mu) in all_links_in_cube:
    by_vertex.setdefault(xv, []).append(mu)
print(f"\nLinks grouped by vertex:")
for xv, dirs in sorted(by_vertex.items()):
    print(f"  vertex {xv}: directions {sorted(dirs)}")

# ============================================================
# FINER GROUPING: Can we do better than cube?
# Test: separate active and inactive planes per vertex
# ============================================================
print("\n" + "="*60)
print("FINER GROUPING: Active vs Inactive planes per vertex")
print("="*60)

N_TEST = 5000
max_active_sum = -np.inf
max_inactive_sum = -np.inf
n_active_viol = 0
n_inactive_viol = 0

active_planes = [(mu, nu) for mu, nu in plane_types if (mu+nu) % 2 == 1]
inactive_planes = [(mu, nu) for mu, nu in plane_types if (mu+nu) % 2 == 0]

for _ in range(N_TEST):
    links = random_config()
    for x in vertices:
        active_sum = sum(f_plaquette(links, x, mu, nu) for mu, nu in active_planes)
        inactive_sum = sum(f_plaquette(links, x, mu, nu) for mu, nu in inactive_planes)
        if active_sum > 1e-8:
            n_active_viol += 1
            max_active_sum = max(max_active_sum, active_sum)
        if inactive_sum > 1e-8:
            n_inactive_viol += 1
            max_inactive_sum = max(max_inactive_sum, inactive_sum)

print(f"After {N_TEST} configs × 16 vertices = {N_TEST*16} tests:")
print(f"  Active planes per vertex (4 plaquettes): violations = {n_active_viol}, max = {max_active_sum:.4f}")
print(f"  Inactive planes per vertex (2 plaquettes): violations = {n_inactive_viol}, max = {max_inactive_sum:.4f}")

# ============================================================
# FINER GROUPING: Single plane type per vertex
# ============================================================
print("\n" + "="*60)
print("FINER GROUPING: Single plane type per vertex")
print("="*60)

N_TEST2 = 2000
violations_per_plane = {pt: 0 for pt in plane_types}
max_per_plane = {pt: -np.inf for pt in plane_types}

for _ in range(N_TEST2):
    links = random_config()
    for x in vertices:
        for mu, nu in plane_types:
            val = f_plaquette(links, x, mu, nu)
            if val > 1e-8:
                violations_per_plane[(mu, nu)] += 1
            max_per_plane[(mu, nu)] = max(max_per_plane[(mu, nu)], val)

total_tests = N_TEST2 * 16
print(f"After {N_TEST2} configs × 16 vertices = {total_tests} tests per plane type:")
for pt in plane_types:
    viol = violations_per_plane[pt]
    mx = max_per_plane[pt]
    parity = "active" if (pt[0]+pt[1])%2==1 else "inactive"
    print(f"  Plane {pt} ({parity}): violations = {viol}/{total_tests}, max f = {mx:.4f}")

# ============================================================
# CHECK: Does the cube-face sum depend on staggered sign?
# Analyze f_{x,mu,nu} for individual plaquettes
# ============================================================
print("\n" + "="*60)
print("INDIVIDUAL PLAQUETTE SIGN ANALYSIS")
print("="*60)

N_TEST3 = 2000
max_pos_active = -np.inf
max_pos_inactive = -np.inf
for _ in range(N_TEST3):
    links = random_config()
    for x, mu, nu in plaquettes:
        val = f_plaquette(links, x, mu, nu)
        if (mu+nu)%2==1 and val > max_pos_active:
            max_pos_active = val
        if (mu+nu)%2==0 and val > max_pos_inactive:
            max_pos_inactive = val

print(f"Max individual f_□ for active plaquettes: {max_pos_active:.4f}")
print(f"Max individual f_□ for inactive plaquettes: {max_pos_inactive:.4f}")
print("(Confirming individual plaquettes can be positive)")

# ============================================================
# GROUPING: 3-plaquette groups (adjacent plane types)
# For d=4: can we pair active planes or mix active/inactive?
# ============================================================
print("\n" + "="*60)
print("3-PLAQUETTE GROUPING ANALYSIS (plane subsets per vertex)")
print("="*60)

from itertools import combinations
subsets_of_interest = [
    [(0,1),(0,2),(0,3)],  # all planes containing direction 0
    [(0,1),(1,2),(1,3)],  # all planes containing direction 1
    [(0,2),(1,2),(2,3)],  # all planes containing direction 2
    [(0,3),(1,3),(2,3)],  # all planes containing direction 3
]

N_TEST4 = 3000
for subset in subsets_of_interest:
    max_val = -np.inf
    n_viol = 0
    for _ in range(N_TEST4):
        links = random_config()
        for x in vertices:
            val = sum(f_plaquette(links, x, mu, nu) for mu, nu in subset)
            if val > 1e-8:
                n_viol += 1
            max_val = max(max_val, val)
    label = "+".join(f"({m},{n})" for m,n in subset)
    print(f"  Planes {label}: violations={n_viol}/{N_TEST4*16}, max={max_val:.4f}")

print("\nAll analyses complete.")
