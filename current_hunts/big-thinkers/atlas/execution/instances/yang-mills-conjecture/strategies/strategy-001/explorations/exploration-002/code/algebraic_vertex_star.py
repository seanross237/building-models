"""
Algebraic analysis of the vertex-star structure.

For the vertex star of x = (0,0,0,0), identify which plaquettes contribute,
what the staggered coefficients are, and derive the algebraic identity
that forces the sum to be ≤ 0.
"""

import numpy as np
from itertools import product

# ============================================================
# Setup
# ============================================================
sigma1 = np.array([[0, 1], [1, 0]], dtype=complex)
sigma2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma3 = np.array([[1, 0], [0, -1]], dtype=complex)
sigmas = [sigma1, sigma2, sigma3]
T = [1j/2 * s for s in sigmas]
I2 = np.eye(2, dtype=complex)

L = 2
d = 4
vertices = list(product(range(L), repeat=d))
plane_types = [(mu, nu) for mu in range(d) for nu in range(d) if mu < nu]

def add_dir(x, mu):
    xl = list(x)
    xl[mu] = (xl[mu] + 1) % L
    return tuple(xl)

def stag_sign(x, mu):
    return (-1)**(sum(x) + mu)

def su2_norm_sq(A):
    return float(np.real(-2 * np.trace(A @ A)))

def adjoint(Q, A):
    return Q @ A @ Q.conj().T

edges = [(x, mu) for x in vertices for mu in range(d)]

# ============================================================
# Enumerate vertex star of x0 = (0,0,0,0)
# ============================================================
x0 = (0,0,0,0)

print(f"Vertex star of x0 = {x0}:")
print(f"(On L=2, each coordinate x_i ∈ {{0,1}}, x+1 = x-1 mod 2)")
print()

# A plaquette (y, mu, nu) contains x0 as a corner if:
# x0 ∈ {y, y+e_mu, y+e_nu, y+e_mu+e_nu}
# Since L=2: y+e_mu+e_nu = y - e_mu - e_nu (mod 2) for any direction

star = []
for y in vertices:
    for mu, nu in plane_types:
        corners = [y, add_dir(y, mu), add_dir(y, nu), add_dir(add_dir(y, mu), nu)]
        if x0 in corners:
            # Which corner is x0?
            corner_idx = corners.index(x0)
            star.append((y, mu, nu, corner_idx))

print(f"Vertex star size: {len(star)}")
print()

# Group by orientation
from collections import defaultdict
by_orient = defaultdict(list)
for y, mu, nu, ci in star:
    by_orient[(mu, nu)].append((y, ci))

for orient in sorted(by_orient.keys()):
    entries = by_orient[orient]
    active = "ACTIVE" if (orient[0] + orient[1]) % 2 == 1 else "INACTIVE"
    print(f"Orientation {orient} ({active}): {len(entries)} plaquettes")
    for y, ci in entries:
        corner_names = ["base", "base+mu", "base+nu", "base+mu+nu"]
        print(f"  base={y}, x0 is corner #{ci} ({corner_names[ci]})")

print()

# ============================================================
# Analyze the structure more carefully
# For each plaquette in the star, identify:
# - The 4 edges
# - The staggered coefficients
# - The partial holonomies involved
# - Which edges are "local to x0" (incident to x0)
# ============================================================

print("="*60)
print("DETAILED STRUCTURE OF EACH PLAQUETTE IN STAR")
print("="*60)

def get_plaquette_info(y, mu, nu):
    """Get full info about plaquette (y, mu, nu)."""
    y_mu = add_dir(y, mu)
    y_nu = add_dir(y, nu)
    y_mu_nu = add_dir(y_mu, nu)

    e1 = (y, mu)      # forward from y in direction mu
    e2 = (y_mu, nu)    # forward from y+mu in direction nu
    e3 = (y_nu, mu)    # backward from y+nu in direction mu
    e4 = (y, nu)       # backward from y in direction nu

    c1 = stag_sign(*e1)
    c2 = stag_sign(*e2)
    c3 = stag_sign(*e3)
    c4 = stag_sign(*e4)

    return {
        'base': y,
        'mu': mu, 'nu': nu,
        'corners': [y, y_mu, y_nu, y_mu_nu],
        'edges': [e1, e2, e3, e4],
        'signs': [c1, c2, c3, c4],
        'edge_labels': ['(y,mu)', '(y+mu,nu)', '(y+nu,mu)', '(y,nu)'],
        'B_direction': ['+', '+Ad(P1)', '-Ad(P12*P3inv)', '-Ad(U)'],
    }

# For each plaquette in the star, list which edges are incident to x0
edges_incident_to_x0 = [(x0, mu) for mu in range(d)]  # 4 outgoing edges from x0
# On L=2, these are also the incoming edges (since x0 + e_mu ≡ x0 - e_mu mod 2)

print(f"\nEdges incident to x0: {edges_incident_to_x0}")

for y, mu, nu, ci in star[:12]:  # Show first 12
    info = get_plaquette_info(y, mu, nu)
    active = "ACT" if (mu + nu) % 2 == 1 else "INA"

    # Which edges of this plaquette are incident to x0?
    incident = []
    for i, e in enumerate(info['edges']):
        if e[0] == x0 or add_dir(e[0], e[1]) == x0:
            incident.append(i)

    print(f"\n  [{active}] ({y},{mu},{nu}), x0 = corner#{ci}")
    print(f"    Edges: {info['edges']}")
    print(f"    Signs: {info['signs']}")
    print(f"    Edges incident to x0: indices {incident}")

# ============================================================
# KEY QUESTION: On L=2, x0 + e_mu = x0 - e_mu for all mu.
# So the vertex star of x0 has high symmetry.
# ============================================================

print("\n\n" + "="*60)
print("SYMMETRY ANALYSIS ON L=2")
print("="*60)

print(f"\nOn L=2, every vertex has the same local geometry (translation invariance).")
print(f"The vertex star of x0 = (0,...,0) has {len(star)} plaquettes.")
print(f"Each plaquette has 4 corners; each of 96 plaquettes contributes to 4 vertex stars.")
print(f"Total plaquette-vertex pairs: 96 × 4 = {96*4}")
print(f"Spread across 16 vertices: {96*4/16} = 24 per vertex (matches {len(star)}).")
print(f"\nSo each vertex star has 24 plaquettes, and the 16 vertex-star sums partition the")
print(f"total sum (with each plaquette counted 4 times).")
print(f"\nSum_x star(x) = 4 * Sum_□ f_□")
print()

# Verify this numerically
np.random.seed(99)

def compute_f_array(links):
    plaq_list = [(x, mu, nu) for x in vertices for mu, nu in plane_types]
    n_fixed = T[0]
    I_links = {e: I2.copy() for e in edges}
    f = np.zeros(len(plaq_list))
    for i, (x, mu, nu) in enumerate(plaq_list):
        def compute_B_for(lnk, x, mu, nu):
            y_mu = add_dir(x, mu)
            y_nu = add_dir(x, nu)
            e1, e2, e3, e4 = (x, mu), (y_mu, nu), (y_nu, mu), (x, nu)
            c1, c2, c3, c4 = stag_sign(*e1), stag_sign(*e2), stag_sign(*e3), stag_sign(*e4)
            P1, P2, P3, P4 = lnk[e1], lnk[e2], lnk[e3], lnk[e4]
            P123 = P1 @ P2 @ P3.conj().T
            U = P123 @ P4.conj().T
            return (c1 * n_fixed + c2 * adjoint(P1, n_fixed)
                    - c3 * adjoint(P123, n_fixed) - c4 * adjoint(U, n_fixed))
        B_Q = compute_B_for(links, x, mu, nu)
        B_I = compute_B_for(I_links, x, mu, nu)
        f[i] = su2_norm_sq(B_Q) - su2_norm_sq(B_I)
    return f

def random_su2():
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    a, b, c, dd = q
    return np.array([[a + 1j*b, c + 1j*dd], [-c + 1j*dd, a - 1j*b]], dtype=complex)

links = {e: random_su2() for e in edges}
f = compute_f_array(links)

total = f.sum()

# Compute vertex star sums
plaq_list = [(x, mu, nu) for x in vertices for mu, nu in plane_types]
vstar_sum_total = 0
for xv in vertices:
    vs = 0
    for i, (y, mu, nu) in enumerate(plaq_list):
        corners = [y, add_dir(y, mu), add_dir(y, nu), add_dir(add_dir(y, mu), nu)]
        if xv in corners:
            vs += f[i]
    vstar_sum_total += vs

print(f"Total f = {total:.6f}")
print(f"Sum of vertex-star sums = {vstar_sum_total:.6f}")
print(f"Ratio = {vstar_sum_total/total:.6f} (should be 4)")
print(f"4 × total = {4*total:.6f}")

# ============================================================
# If vertex-star sum ≤ 0 for each vertex, then:
# Sum_x star(x) = 4 * Sum_□ f_□ ≤ 0
# This is STRONGER than Sum_□ f_□ ≤ 0.
# ============================================================

print(f"\n\nCRITICAL INSIGHT:")
print(f"If star(x) ≤ 0 for all x, then Sum_x star(x) = 4 * Sum_□ f_□ ≤ 0.")
print(f"The vertex-star inequality is a REFINEMENT of the global inequality.")
print(f"It distributes the negativity across all vertices.")

# ============================================================
# Check: is vertex-star sum proportional to total for each vertex?
# (Translation invariance on L=2 might make all vertex stars equal)
# ============================================================
print(f"\n\n" + "="*60)
print(f"ARE ALL VERTEX-STAR SUMS EQUAL? (Translation invariance)")
print(f"="*60)

links = {e: random_su2() for e in edges}
f = compute_f_array(links)

vstar_sums = {}
for xv in vertices:
    vs = 0
    for i, (y, mu, nu) in enumerate(plaq_list):
        corners = [y, add_dir(y, mu), add_dir(y, nu), add_dir(add_dir(y, mu), nu)]
        if xv in corners:
            vs += f[i]
    vstar_sums[xv] = vs

print(f"Vertex-star sums:")
for xv in sorted(vstar_sums.keys()):
    print(f"  {xv}: {vstar_sums[xv]:.6f}")

vals = list(vstar_sums.values())
print(f"\nMin = {min(vals):.6f}, Max = {max(vals):.6f}")
print(f"All equal? {max(vals) - min(vals) < 1e-10}")
print(f"Std dev = {np.std(vals):.6f}")

# ============================================================
# For the cube-face grouping: decomposition check
# ============================================================
print(f"\n\n" + "="*60)
print(f"CUBE-FACE GROUPING: DECOMPOSITION CHECK")
print(f"="*60)

# Cube-face at x: the 6 plaquettes (x, mu, nu) for all 6 plane types
cube_sum_total = 0
for xv in vertices:
    cs = 0
    for i, (y, mu, nu) in enumerate(plaq_list):
        if y == xv:
            cs += f[i]
    cube_sum_total += cs

print(f"Sum of cube-face sums = {cube_sum_total:.6f}")
print(f"Total f = {total:.6f}")
print(f"Ratio = {cube_sum_total/total:.6f} (should be 1, since each plaq counted once)")

cube_sums = {}
for xv in vertices:
    cs = 0
    for i, (y, mu, nu) in enumerate(plaq_list):
        if y == xv:
            cs += f[i]
    cube_sums[xv] = cs

print(f"\nCube-face sums:")
for xv in sorted(cube_sums.keys()):
    print(f"  {xv}: {cube_sums[xv]:.6f}")

print(f"\nMin = {min(cube_sums.values()):.6f}, Max = {max(cube_sums.values()):.6f}")

# ============================================================
# The cube-face grouping is a PARTITION of all plaquettes.
# If each cube sum ≤ 0, this directly implies Sum_□ f_□ ≤ 0.
# This is the STRONGEST natural grouping.
# ============================================================
print(f"\nCRITICAL: Cube-face is a PARTITION (each plaquette belongs to exactly one cube).")
print(f"So cube_sum(x) ≤ 0 for all x directly implies Sum_□ f_□ ≤ 0.")
print(f"This is the TIGHTEST grouping — it's a per-vertex local inequality.")

# ============================================================
# Analysis: What makes cube-face work?
# The 6 plaquettes at vertex x are (x,0,1), (x,0,2), (x,0,3), (x,1,2), (x,1,3), (x,2,3)
# 4 active + 2 inactive
# The inactive ones contribute positively, active ones negatively, but sum ≤ 0
# ============================================================
print(f"\n\n" + "="*60)
print(f"CUBE-FACE BREAKDOWN BY ORIENTATION")
print(f"="*60)

for xv in [(0,0,0,0), (1,0,0,0), (0,1,0,0), (1,1,0,0)]:
    print(f"\nVertex {xv}:")
    for mu, nu in plane_types:
        i = plaq_list.index((xv, mu, nu))
        active = "ACT" if (mu + nu) % 2 == 1 else "INA"
        print(f"  ({mu},{nu}) [{active}]: f = {f[i]:.6f}")
    cs = cube_sums[xv]
    print(f"  TOTAL: {cs:.6f}")

# ============================================================
# Single-link analysis: what happens when only one link differs from I?
# ============================================================
print(f"\n\n" + "="*60)
print(f"SINGLE-LINK ANALYSIS")
print(f"="*60)

n_fixed = T[0]

# Perturb one link: edge (x0, 0) by angle theta
for theta in [0.1, 0.5, 1.0, 2.0, np.pi]:
    links_sl = {e: I2.copy() for e in edges}
    # Rotation by theta around T_2 axis
    v = np.array([0, 1, 0])
    half = theta / 2
    v_sigma = sum(v[k] * sigmas[k] for k in range(3))
    links_sl[(x0, 0)] = np.cos(half) * I2 + 1j * np.sin(half) * v_sigma

    f_sl = compute_f_array(links_sl)
    total_sl = f_sl.sum()

    # Count affected plaquettes (those sharing edge (x0, 0))
    affected = []
    for i, (y, mu, nu) in enumerate(plaq_list):
        y_mu = add_dir(y, mu)
        y_nu = add_dir(y, nu)
        plaq_edges = [(y, mu), (y_mu, nu), (y_nu, mu), (y, nu)]
        if (x0, 0) in plaq_edges:
            affected.append(i)

    print(f"\n  theta = {theta:.2f}:")
    print(f"    Total f = {total_sl:.6f}")
    print(f"    Affected plaquettes: {len(affected)}")
    for i in affected:
        y, mu, nu = plaq_list[i]
        active = "ACT" if (mu + nu) % 2 == 1 else "INA"
        print(f"      ({y},{mu},{nu}) [{active}]: f = {f_sl[i]:.6f}")

    non_affected = [i for i in range(len(plaq_list)) if i not in affected and abs(f_sl[i]) > 1e-10]
    if non_affected:
        print(f"    Non-affected with f≠0: {len(non_affected)} UNEXPECTED!")
    else:
        print(f"    All non-affected have f=0: OK")

    # Cube-face sums
    for xv in vertices:
        cs = sum(f_sl[i] for i, (y, mu, nu) in enumerate(plaq_list) if y == xv)
        if abs(cs) > 1e-10:
            print(f"    Cube-face {xv}: {cs:.6f}")

print("\nAlgebraic analysis complete.")
