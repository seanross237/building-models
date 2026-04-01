"""
Stage 2-3: Shared edge analysis and decoherence mechanism.

Key questions:
1. How many SO(3) variables are shared between adjacent plaquettes?
2. Can worst-case configs be simultaneously achieved?
3. What's the cross-term structure?

Also: compute the exact second-order expansion of f_sq around Q=I
to understand the decoherence mechanism analytically.
"""

import numpy as np
from itertools import product
from collections import defaultdict

# =====================================================
# Lattice setup
# =====================================================

L = 2
d = 4
coords = list(product(range(L), repeat=d))

def add_mod(x, mu):
    y = list(x)
    y[mu] = (y[mu] + 1) % L
    return tuple(y)

def staggered_sign(x, mu):
    return (-1) ** (sum(x) + mu)

def edge_key(x, mu):
    """Canonical edge key."""
    return (x, mu)

# Build plaquette list
plaquettes = []
for x in coords:
    for mu in range(d):
        for nu in range(mu+1, d):
            e1 = edge_key(x, mu)
            e2 = edge_key(add_mod(x, mu), nu)
            e3 = edge_key(add_mod(x, nu), mu)
            e4 = edge_key(x, nu)

            s1 = staggered_sign(*e1)
            s2 = staggered_sign(*e2)
            s3 = staggered_sign(*e3)
            s4 = staggered_sign(*e4)

            eff = (s1, s2, -s3, -s4)
            active = (mu + nu) % 2 == 1

            plaquettes.append({
                'x': x, 'mu': mu, 'nu': nu,
                'edges': [e1, e2, e3, e4],
                'eff': eff, 'active': active
            })

# =====================================================
# SHARED EDGE ANALYSIS
# =====================================================

print("=" * 70)
print("SHARED EDGE ANALYSIS")
print("=" * 70)

# Build edge-to-plaquette mapping
edge_to_plaquettes = defaultdict(list)
for idx, p in enumerate(plaquettes):
    for edge_pos, e in enumerate(p['edges']):
        edge_to_plaquettes[e].append((idx, edge_pos))

print(f"\nTotal distinct edges: {len(edge_to_plaquettes)}")
# Each edge should appear in multiple plaquettes
degree_dist = defaultdict(int)
for e, plist in edge_to_plaquettes.items():
    degree_dist[len(plist)] += 1

print(f"Edge degree distribution (how many plaquettes per edge):")
for deg, count in sorted(degree_dist.items()):
    print(f"  {deg} plaquettes: {count} edges")

# For each pair of adjacent plaquettes (sharing an edge), count shared edges
adj_pairs = set()
for e, plist in edge_to_plaquettes.items():
    for i in range(len(plist)):
        for j in range(i+1, len(plist)):
            p1_idx, _ = plist[i]
            p2_idx, _ = plist[j]
            adj_pairs.add((min(p1_idx, p2_idx), max(p1_idx, p2_idx)))

print(f"\nTotal adjacent plaquette pairs (sharing at least 1 edge): {len(adj_pairs)}")

# Count shared edges per pair
shared_count = defaultdict(int)
for p1, p2 in adj_pairs:
    edges_1 = set(map(tuple, [list(e) for e in plaquettes[p1]['edges']]))
    edges_2 = set(map(tuple, [list(e) for e in plaquettes[p2]['edges']]))
    shared = len(edges_1 & edges_2)
    shared_count[shared] += 1

print(f"Distribution of shared edges between adjacent pairs:")
for k, v in sorted(shared_count.items()):
    print(f"  {k} shared edge(s): {v} pairs")

# =====================================================
# ADJACENCY STRUCTURE: Which plaquettes share edges?
# =====================================================

print("\n" + "=" * 70)
print("ADJACENCY STRUCTURE")
print("=" * 70)

# For a specific plaquette, list all neighbors
sample_plaq = plaquettes[0]
print(f"\nSample plaquette: x={sample_plaq['x']}, mu={sample_plaq['mu']}, nu={sample_plaq['nu']}")
print(f"  Edges: {sample_plaq['edges']}")
print(f"  Active: {sample_plaq['active']}")
print(f"  Eff: {sample_plaq['eff']}")

neighbors = set()
for e in sample_plaq['edges']:
    for pidx, epos in edge_to_plaquettes[e]:
        if pidx != 0:
            neighbors.add(pidx)

print(f"  Neighbors: {len(neighbors)} plaquettes")
for pidx in sorted(neighbors):
    p = plaquettes[pidx]
    shared = set(map(str, sample_plaq['edges'])) & set(map(str, p['edges']))
    print(f"    Plaq {pidx}: x={p['x']}, ({p['mu']},{p['nu']}), active={p['active']}, "
          f"eff={p['eff']}, shared_edges={len(shared)}")

# =====================================================
# How many edge rotations (Ad(Q_e)) affect each plaquette?
# =====================================================

print("\n" + "=" * 70)
print("EDGE ROTATION ANALYSIS")
print("=" * 70)

# For each plaquette, the B_sq involves R1 = Ad(Q_{e1}), R2, R3 which are
# composed from Q_{e1}, Q_{e2}, Q_{e3}, Q_{e4}. So each plaquette depends
# on 4 edge quaternions.

# The key SO(3) rotations are:
# R1 = Ad(Q_{e1}), R2 = Ad(Q_{e1}*Q_{e2}*Q_{e3}^{-1}), R3 = R2 * Ad(Q_{e4}^{-1})
# So R1 depends on e1, R2 on (e1,e2,e3), R3 on (e1,e2,e3,e4).

# Two plaquettes sharing edge e1 would share the R1 rotation.
# But if they share e2 or e3, R2 still depends on other edges too.

# Let's quantify: for each pair of adjacent plaquettes, how constrained are
# their B_sq by the shared edges?

# =====================================================
# SECOND-ORDER EXPANSION around Q=I
# =====================================================

print("\n" + "=" * 70)
print("SECOND-ORDER EXPANSION of f_sq around Q=I")
print("=" * 70)

# At Q=I, parameterize Q_e = exp(epsilon * A_e) for A_e in su(2).
# In quaternion form: q_e ≈ (1, epsilon/2 * a_e) where a_e is the Lie algebra element.
#
# The adjoint rotation: Ad(exp(epsilon*A)) ≈ I + epsilon * [A, .] + O(epsilon^2).
# In SO(3) form: R_e ≈ I + epsilon * hat(a_e) where hat(a) is the 3x3 skew matrix.
#
# Let's compute f_sq to second order in epsilon.

# For each plaquette, the adjoint rotations are:
# R1 = Ad(Q_{e1}) ≈ I + hat(a1) + (1/2)*hat(a1)^2
# P23 = Q_{e1}*Q_{e2}*Q_{e3}^{-1} ≈ I + (a1+a2-a3) + (1/2)(a1+a2-a3)^2 + commutator terms
# U_sq = P23 * Q_{e4}^{-1} ≈ I + (a1+a2-a3-a4) + ...
#
# Actually for SU(2) products at first order:
# Q_{e1}*Q_{e2} ≈ I + epsilon*(a1+a2) + O(epsilon^2)
# Q_{e1}*Q_{e2}*Q_{e3}^{-1} ≈ I + epsilon*(a1+a2-a3) + O(epsilon^2)
# U_sq ≈ I + epsilon*(a1+a2-a3-a4) + O(epsilon^2)
#
# So:
# R1 ≈ I + epsilon * hat(a1)
# R2 ≈ I + epsilon * hat(a1+a2-a3)
# R3 ≈ I + epsilon * hat(a1+a2-a3-a4)
#
# B_sq = c1*n + c2*(I + epsilon*hat(a1))*n + c3*(I + epsilon*hat(a1+a2-a3))*n
#        + c4*(I + epsilon*hat(a1+a2-a3-a4))*n
#      = (c1+c2+c3+c4)*n + epsilon * [c2*hat(a1)*n + c3*hat(a1+a2-a3)*n + c4*hat(a1+a2-a3-a4)*n]
#
# For active plaquettes: (c1,c2,c3,c4) = (a,a,a,a), sum = 4a.
# B_sq_active ≈ 4a*n + epsilon*a*[hat(a1) + hat(a1+a2-a3) + hat(a1+a2-a3-a4)]*n
#
# |B_sq|^2 ≈ 16|n|^2 + 2*epsilon*4a * a * n^T [hat(a1) + hat(a1+a2-a3) + hat(a1+a2-a3-a4)] n + O(epsilon^2)
#           = 16|n|^2 + 8*epsilon * n^T [hat(a1) + hat(a1+a2-a3) + hat(a1+a2-a3-a4)] n
#
# But hat(a)*n = a × n (cross product), which is perpendicular to n.
# So n^T * hat(a)*n = n · (a × n) = 0.
# Therefore the first-order term VANISHES and we need the second order.
#
# At second order:
# R ≈ I + epsilon*hat(a) + (epsilon^2/2)*hat(a)^2
# hat(a)^2 = a*a^T - |a|^2*I (from standard formula)
# R*n ≈ n + epsilon*(a×n) + (epsilon^2/2)*(a*a^T - |a|^2*I)*n
#      = n + epsilon*(a×n) + (epsilon^2/2)*((a·n)*a - |a|^2*n)
#
# Let's define the perturbation for each rotation:
# delta1 = a1 (from R1)
# delta2 = a1+a2-a3 (from R2)
# delta3 = a1+a2-a3-a4 (from R3)

# For active plaquettes:
# B_sq = a*(n + (n + eps*d1×n + eps^2/2*Q1*n) + (n + eps*d2×n + eps^2/2*Q2*n)
#          + (n + eps*d3×n + eps^2/2*Q3*n))
# where Qi*n = (di·n)*di - |di|^2*n and di are delta1,delta2,delta3.
# B_sq = a*(4n + eps*(d1+d2+d3)×n + eps^2/2*(Q1+Q2+Q3)*n)
#
# |B_sq|^2 = |4n + eps*(d1+d2+d3)×n + eps^2/2*(Q1+Q2+Q3)*n|^2
# = 16 + 8*eps*n·((d1+d2+d3)×n) + eps^2*(|(d1+d2+d3)×n|^2 + 4*n·(Q1+Q2+Q3)*n) + O(eps^3)
# First term: n·((d1+d2+d3)×n) = 0 ✓
# Second order:
# = 16 + eps^2 * [|(d1+d2+d3)×n|^2 + 4*n·(Q1+Q2+Q3)*n]
# = 16 + eps^2 * [|D×n|^2 + 4*sum_i ((di·n)^2 - |di|^2)]  where D = d1+d2+d3
# = 16 + eps^2 * [|D|^2 - (D·n)^2 + 4*sum_i ((di·n)^2 - |di|^2)]
# (using |v×n|^2 = |v|^2 - (v·n)^2)
#
# f_sq_active = eps^2 * [|D|^2 - (D·n)^2 - 4*(|d1|^2 + |d2|^2 + |d3|^2) + 4*(d1·n)^2 + 4*(d2·n)^2 + 4*(d3·n)^2]
#             = eps^2 * [|D|^2 - (D·n)^2 - 4*sum|di|^2 + 4*sum(di·n)^2]
#
# Let's use the shorthand: for 3D vectors, |v×n|^2 = |v|^2(1 - cos^2 α) where α is angle to n.

# For inactive plaquettes: (c1,c2,c3,c4) = (a,-a,a,-a), sum=0.
# B_sq = a*(n - R1*n + R2*n - R3*n) + O(eps)
# At zeroth order: a*(n-n+n-n) = 0.
# First order: a*eps*(-d1×n + d2×n - d3×n)
# |B_sq|^2 = eps^2 * |((-d1+d2-d3)×n|^2 = eps^2 * |D'×n|^2
# where D' = -d1+d2-d3 = -(a1) + (a1+a2-a3) - (a1+a2-a3-a4) = -a1+a4 = a4-a1
#
# So f_sq_inactive = eps^2 * |(a4-a1)×n|^2

# TOTAL:
# f_sq = Sum_active eps^2*[|D|^2 - (D·n)^2 - 4*sum|di|^2 + 4*sum(di·n)^2]
#       + Sum_inactive eps^2*|(a4-a1)×n|^2

# Let me compute this numerically for random perturbations to verify.

def quat_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ])

def quat_inv(q):
    return np.array([q[0], -q[1], -q[2], -q[3]])

def quat_to_rot(q):
    q = q / np.linalg.norm(q)
    w, x, y, z = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])

def edge_index(x, mu):
    idx = 0
    for i in range(d):
        idx = idx * L + x[i]
    return idx * d + mu

# Rebuild plaquettes with edge indices
plaq_data = []
for p in plaquettes:
    e_indices = [edge_index(*e) for e in p['edges']]
    plaq_data.append({
        'e_idx': e_indices,
        'eff': p['eff'],
        'active': p['active'],
        'mu': p['mu'],
        'nu': p['nu'],
        'x': p['x']
    })

def compute_fsq_exact(Q_dict, n):
    """Exact f_sq computation."""
    total = 0.0
    for p in plaq_data:
        q1 = Q_dict[p['e_idx'][0]]
        q2 = Q_dict[p['e_idx'][1]]
        q3 = Q_dict[p['e_idx'][2]]
        q4 = Q_dict[p['e_idx'][3]]

        R1 = quat_to_rot(q1)
        partial = quat_mult(quat_mult(q1, q2), quat_inv(q3))
        R2 = quat_to_rot(partial)
        usq = quat_mult(partial, quat_inv(q4))
        R3 = quat_to_rot(usq)

        c1, c2, c3, c4 = p['eff']
        B = c1 * n + c2 * (R1 @ n) + c3 * (R2 @ n) + c4 * (R3 @ n)
        total += np.dot(B, B)
    return total - 1024.0

def compute_fsq_second_order(A_dict, n):
    """
    Second-order approximation.
    A_dict: edge_index -> 3D Lie algebra element (rotation vector).
    Returns f_sq to second order in A.
    """
    f_active = 0.0
    f_inactive = 0.0

    for p in plaq_data:
        a1 = A_dict[p['e_idx'][0]]  # Lie algebra for edge e1
        a2 = A_dict[p['e_idx'][1]]  # for e2
        a3 = A_dict[p['e_idx'][2]]  # for e3
        a4 = A_dict[p['e_idx'][3]]  # for e4

        d1 = a1                    # delta for R1
        d2 = a1 + a2 - a3         # delta for R2
        d3 = a1 + a2 - a3 - a4   # delta for R3 (= holonomy)

        if p['active']:
            # f_active_sq = |D×n|^2 - 4*sum|di|^2 + 4*sum(di·n)^2 + (D·n)^2 - (D·n)^2
            # Wait, let me redo: f = |D×n|^2 + 4*n·(Q1+Q2+Q3)*n
            # where Qi*n = (di·n)*di - |di|^2*n
            # n·Qi*n = (di·n)^2 - |di|^2
            D = d1 + d2 + d3
            DxN = np.cross(D, n)
            f_plaq = np.dot(DxN, DxN) + 4 * sum(np.dot(di, n)**2 - np.dot(di, di) for di in [d1, d2, d3])
            f_active += f_plaq
        else:
            # f_inactive_sq = |D'×n|^2 where D' = -d1+d2-d3
            Dp = -d1 + d2 - d3
            DpxN = np.cross(Dp, n)
            f_plaq = np.dot(DpxN, DpxN)
            f_inactive += f_plaq

    return f_active + f_inactive, f_active, f_inactive

# Verify second-order expansion
print("Verification of second-order expansion:")
n = np.array([0., 0., 1.])
np.random.seed(77)

for eps in [0.001, 0.01, 0.05, 0.1]:
    # Random Lie algebra elements
    A_dict = {}
    Q_dict = {}
    for i in range(64):
        a = np.random.randn(3)
        A_dict[i] = eps * a
        # Convert to quaternion: q ≈ (1, eps*a/2) normalized
        angle = np.linalg.norm(eps * a)
        if angle < 1e-15:
            Q_dict[i] = np.array([1., 0., 0., 0.])
        else:
            axis = (eps * a) / angle
            Q_dict[i] = np.array([np.cos(angle/2), *(np.sin(angle/2) * axis)])
            Q_dict[i] /= np.linalg.norm(Q_dict[i])

    f_exact = compute_fsq_exact(Q_dict, n)
    f_approx, f_act, f_inact = compute_fsq_second_order(A_dict, n)

    print(f"  eps={eps:.4f}: exact={f_exact:.8f}, approx={f_approx:.8f}, "
          f"ratio={f_exact/f_approx:.6f}, act={f_act:.6f}, inact={f_inact:.6f}")

# =====================================================
# SIMPLIFY: For inactive plaquettes, D' = a4 - a1
# =====================================================

print("\n" + "=" * 70)
print("INACTIVE PLAQUETTE D' ANALYSIS")
print("=" * 70)

# Verify D' = a4 - a1 for inactive plaquettes
# d1 = a1, d2 = a1+a2-a3, d3 = a1+a2-a3-a4
# D' = -d1 + d2 - d3 = -a1 + (a1+a2-a3) - (a1+a2-a3-a4) = -a1 + a4 = a4 - a1
print("D' = -d1 + d2 - d3 = -(a1) + (a1+a2-a3) - (a1+a2-a3-a4) = a4 - a1")
print("So f_inactive_sq = |(a4-a1)×n|^2")
print("This depends ONLY on edges e1 and e4!")

# For active plaquettes:
# D = d1 + d2 + d3 = a1 + (a1+a2-a3) + (a1+a2-a3-a4) = 3*a1 + 2*a2 - 2*a3 - a4
print("\nActive plaquette D = d1 + d2 + d3:")
print("D = a1 + (a1+a2-a3) + (a1+a2-a3-a4) = 3*a1 + 2*a2 - 2*a3 - a4")

# Sum of |di|^2 for active:
# |d1|^2 = |a1|^2
# |d2|^2 = |a1+a2-a3|^2
# |d3|^2 = |a1+a2-a3-a4|^2

# =====================================================
# COMPACT FORM: f_sq to second order
# =====================================================

print("\n" + "=" * 70)
print("COMPACT SECOND-ORDER FORMULA")
print("=" * 70)

# Let's write f_sq = Sum_e,e' A_e^T M_{ee'} A_{e'} where M is a matrix
# acting on the 64*3 = 192 dimensional Lie algebra.
#
# From the plaquette sums, we can read off M as a quadratic form.
# Let's compute it numerically.

dim = 192  # 64 edges * 3 components
M = np.zeros((dim, dim))

for p in plaq_data:
    ei = p['e_idx']
    # Indices into the 192-dim space
    idx1 = ei[0]*3  # 3D block for edge e1
    idx2 = ei[1]*3
    idx3 = ei[2]*3
    idx4 = ei[3]*3

    # delta1 = a_{e1}
    # delta2 = a_{e1} + a_{e2} - a_{e3}
    # delta3 = a_{e1} + a_{e2} - a_{e3} - a_{e4}

    # For active: f = |D×n|^2 + 4*sum_i((di·n)^2 - |di|^2)
    # For inactive: f = |D'×n|^2

    if p['active']:
        # D = d1+d2+d3 = 3*a1 + 2*a2 - 2*a3 - a4
        # Contribution from |D×n|^2:
        # |D×n|^2 = D^T (I - nn^T) D (since |v×n|^2 = |v|^2 - (v·n)^2 = v^T(I-nn^T)v)
        P_perp = np.eye(3) - np.outer(n, n)  # projector onto plane perp to n

        # D = c1*a1 + c2*a2 + c3*a3 + c4*a4 where c = (3, 2, -2, -1)
        coeffs_D = {0: 3, 1: 2, 2: -2, 3: -1}

        # |D×n|^2 = D^T P_perp D = sum_{j,k} c_j c_k a_j^T P_perp a_k
        for j in range(4):
            for k in range(4):
                block = coeffs_D[j] * coeffs_D[k] * P_perp
                M[ei[j]*3:ei[j]*3+3, ei[k]*3:ei[k]*3+3] += block

        # 4*sum_i ((di·n)^2 - |di|^2) = 4*sum_i di^T (nn^T - I) di
        P_neg = np.outer(n, n) - np.eye(3)
        # di for i=0,1,2 (d1, d2, d3)
        # d1 = a1: coeffs = {0: 1}
        # d2 = a1+a2-a3: coeffs = {0: 1, 1: 1, 2: -1}
        # d3 = a1+a2-a3-a4: coeffs = {0: 1, 1: 1, 2: -1, 3: -1}
        d_coeffs = [
            {0: 1},
            {0: 1, 1: 1, 2: -1},
            {0: 1, 1: 1, 2: -1, 3: -1}
        ]
        for di_c in d_coeffs:
            for j_local, cj in di_c.items():
                for k_local, ck in di_c.items():
                    block = 4 * cj * ck * P_neg
                    M[ei[j_local]*3:ei[j_local]*3+3, ei[k_local]*3:ei[k_local]*3+3] += block
    else:
        # Inactive: f = |D'×n|^2 where D' = a4 - a1
        P_perp = np.eye(3) - np.outer(n, n)
        coeffs_Dp = {0: -1, 3: 1}
        for j in coeffs_Dp:
            for k in coeffs_Dp:
                block = coeffs_Dp[j] * coeffs_Dp[k] * P_perp
                M[ei[j]*3:ei[j]*3+3, ei[k]*3:ei[k]*3+3] += block

# Check symmetry
print(f"M matrix size: {M.shape}")
print(f"Symmetric? {np.allclose(M, M.T)}")

# Eigenvalue analysis
eigs = np.linalg.eigvalsh(M)
print(f"\nEigenvalues of M (quadratic form for f_sq):")
print(f"  Min: {eigs[0]:.6f}")
print(f"  Max: {eigs[-1]:.6f}")
print(f"  # positive: {np.sum(eigs > 1e-10)}")
print(f"  # negative: {np.sum(eigs < -1e-10)}")
print(f"  # zero: {np.sum(np.abs(eigs) < 1e-10)}")

print(f"\nIf max eigenvalue < 0: f_sq <= 0 for ALL small perturbations => CONJECTURE TRUE near Q=I")
print(f"Max eigenvalue = {eigs[-1]:.10f}")

# Print eigenvalue spectrum
print("\nFull eigenvalue spectrum (sorted):")
for i, e in enumerate(eigs):
    if abs(e) > 1e-8 or i < 5 or i > len(eigs)-5:
        print(f"  [{i:3d}] {e:+.8f}")
    elif i == 5:
        print(f"  ...")

# Verify with random perturbation
print("\nVerification: random A, f_sq via M vs direct computation")
np.random.seed(42)
A_vec = np.random.randn(192)
f_M = A_vec @ M @ A_vec

# Reconstruct A_dict
A_dict = {}
for i in range(64):
    A_dict[i] = A_vec[i*3:(i+1)*3]
f_direct, _, _ = compute_fsq_second_order(A_dict, n)
print(f"  f_sq via M: {f_M:.8f}")
print(f"  f_sq via direct: {f_direct:.8f}")
print(f"  Match: {abs(f_M - f_direct) < 1e-6}")
