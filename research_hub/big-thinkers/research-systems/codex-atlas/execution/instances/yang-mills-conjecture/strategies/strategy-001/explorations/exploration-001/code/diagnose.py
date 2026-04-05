"""
Diagnostic: Why does P^T R(Q) P = 0 for single-link perturbations?
Also: understand staggered eigenvectors, and check multi-link behavior.
"""

import numpy as np
import sys
sys.path.insert(0, '.')
from lattice_gauge import (
    L, d, nV, nE, nP_count, plaquettes, T, sigma,
    random_su2, su2_inv, adj_matrix, vidx, vcoords, eidx,
    src_of, tgt_of, edge_direction,
    identity_config, random_config, make_M,
    build_bfs_spanning_tree, gauge_fix_tree, cotree_edges,
    get_top_eigenspace, action
)

np.random.seed(123)

# ─── 1. Staggered eigenvectors ────────────────────────────────────────────────
print("=" * 60)
print("1. Structure of staggered eigenvectors")
print("=" * 60)

Q_I = identity_config()
M_I = make_M(Q_I)

evals, evecs = np.linalg.eigh(M_I)
lambda_max = evals[-1]
mask = np.abs(evals - lambda_max) < 1e-8
P = evecs[:, mask]
print(f"P shape: {P.shape}")

# P[e*3+a, col] = amplitude of color-a component of edge e in eigenvector col
# For each column, look at the spatial pattern (ignoring color)
print("\nColumn norms per edge (summed over 3 colors), first eigenvector:")
col0 = P[:, 0]
edge_norms = np.array([np.linalg.norm(col0[e*3:(e+1)*3]) for e in range(nE)])
print(f"  Min: {edge_norms.min():.6f}, Max: {edge_norms.max():.6f}")
print(f"  All equal? {np.allclose(edge_norms, edge_norms[0])}")

# Signs of first color component per edge
signs_edge = np.sign(col0[0::3])  # color-0 component of each edge
print(f"\nSign pattern of first eigenvector (color-0), by edge index:")
for mu in range(d):
    row = []
    for v in range(nV):
        e = eidx(v, mu)
        idx = e * 3 + 0
        row.append(f"{col0[idx]:+.4f}")
    print(f"  dir={mu}: {' '.join(row)}")

# Check staggered pattern: (-1)^{sum of source coordinates}
print("\nCheck staggered pattern v_e = (-1)^{|src(e)|+mu_e}:")
for mu in range(d):
    for v in range(nV):
        e = eidx(v, mu)
        x = vcoords(v)
        stagger = (-1)**(sum(x) + mu)
        amplitude = col0[e*3 + 0] * np.sqrt(nE)  # normalize
        print(f"  e={e:3d} (src={v:2d}, dir={mu}): stagger={stagger:+d}, amplitude={amplitude:+.4f}")
    print()

# Check which P vectors correspond to which color directions
print("P columns: color structure")
for col_idx in range(P.shape[1]):
    v = P[:, col_idx]
    # For each color a, compute sum of |v[e*3+a]|^2
    color_weight = np.array([sum(v[e*3+a]**2 for e in range(nE)) for a in range(3)])
    print(f"  Col {col_idx}: color weights = {color_weight}")

# ─── 2. Single-link P^T R P analysis with higher precision ────────────────────
print("\n" + "=" * 60)
print("2. Single-link perturbation: precise values")
print("=" * 60)

tree_edges = build_bfs_spanning_tree()
cotree = cotree_edges(tree_edges)

# Pick first 10 cotree edges and show precise P^T R P values
print("\nFirst 10 cotree edges, P^T R P eigenvalues (setting one link = random SU(2)):")
for ct_e in cotree[:10]:
    Q_test = list(Q_I)
    Q_test[ct_e] = random_su2()
    M_test = make_M(Q_test)
    R_test = M_test - M_I
    RR = P.T @ R_test @ P
    evals_RR = np.linalg.eigvalsh(RR)
    print(f"  Edge {ct_e:3d}: max_ev = {evals_RR[-1]:.2e}, "
          f"min_ev = {evals_RR[0]:.2e}, "
          f"Tr = {np.trace(RR):.2e}, "
          f"||RR|| = {np.linalg.norm(RR):.2e}")

# Is RR exactly zero? Let's try a non-random U
print("\nTrying specific SU(2) elements (not random):")
test_Us = [
    ('pi/4 around T0', np.array([[np.cos(np.pi/8), 1j*np.sin(np.pi/8)],
                                   [1j*np.sin(np.pi/8), np.cos(np.pi/8)]], dtype=complex)),
    ('pi/2 around T0', np.array([[0, 1j], [1j, 0]], dtype=complex)),
    ('-I (center)', -np.eye(2, dtype=complex)),
]
for name, U in test_Us:
    Q_test = list(Q_I)
    Q_test[cotree[0]] = U
    M_test = make_M(Q_test)
    R_test = M_test - M_I
    RR = P.T @ R_test @ P
    print(f"  U = {name}: Tr(P^T R P) = {np.trace(RR):.6e}, ||P^T R P|| = {np.linalg.norm(RR):.6e}")

# ─── 3. Per-plaquette P^T R_□ P for a single perturbed link ─────────────────
print("\n" + "=" * 60)
print("3. Per-plaquette structure with one perturbed link")
print("=" * 60)

def make_M_plaq(Q_list, e1, e2, e3, e4):
    """M contribution from single plaquette."""
    M_p = np.zeros((nE * 3, nE * 3))
    from lattice_gauge import compute_holonomies
    Q1, Q2, Q3, Q4, P2, P3, U_plaq = compute_holonomies(Q_list, e1, e2, e3, e4)
    signs   = [+1, +1, -1, -1]
    edges   = [e1, e2, e3, e4]
    Ad_list = [np.eye(3), adj_matrix(P2), adj_matrix(P3), adj_matrix(U_plaq)]
    for ki in range(4):
        for kj in range(4):
            block = signs[ki] * signs[kj] * (Ad_list[ki].T @ Ad_list[kj])
            M_p[edges[ki]*3:(edges[ki]+1)*3, edges[kj]*3:(edges[kj]+1)*3] += block
    return M_p

# Perturb cotree[0] = first cotree edge
ct_e = cotree[0]
U = random_su2()
Q_test = list(Q_I)
Q_test[ct_e] = U

# Find all plaquettes containing ct_e
affected_plaquettes = [(i, plaq) for i, plaq in enumerate(plaquettes) if ct_e in plaq]
print(f"\nCotree edge {ct_e} (dir={edge_direction(ct_e)}, src={src_of(ct_e)}) appears in {len(affected_plaquettes)} plaquettes")

for pidx, (e1, e2, e3, e4) in affected_plaquettes:
    M_plaq_Q = make_M_plaq(Q_test, e1, e2, e3, e4)
    M_plaq_I = make_M_plaq(Q_I, e1, e2, e3, e4)
    dM_plaq = M_plaq_Q - M_plaq_I
    dRR = P.T @ dM_plaq @ P
    print(f"  Plaquette {pidx} ({e1},{e2},{e3},{e4}): "
          f"role={['e1','e2','e3','e4'][[e1,e2,e3,e4].index(ct_e)]}, "
          f"Tr(P^T dM P) = {np.trace(dRR):.6e}, "
          f"max_ev = {np.linalg.eigvalsh(dRR)[-1]:.6e}")

# Sum of plaquette contributions
total_RR = sum(P.T @ (make_M_plaq(Q_test, *plaq) - make_M_plaq(Q_I, *plaq)) @ P
               for pidx, plaq in affected_plaquettes)
print(f"\nSum over affected plaquettes: Tr = {np.trace(total_RR):.6e}, "
      f"max_ev = {np.linalg.eigvalsh(total_RR)[-1]:.6e}")

# ─── 4. Two-link perturbation ─────────────────────────────────────────────────
print("\n" + "=" * 60)
print("4. Two-link perturbation")
print("=" * 60)

print("P^T R P for two cotree links perturbed simultaneously:")
for i in range(5):
    ct_e1, ct_e2 = cotree[i], cotree[i+5]
    Q_test = list(Q_I)
    Q_test[ct_e1] = random_su2()
    Q_test[ct_e2] = random_su2()
    M_test = make_M(Q_test)
    R_test = M_test - M_I
    RR = P.T @ R_test @ P
    evals_RR = np.linalg.eigvalsh(RR)
    print(f"  Edges {ct_e1},{ct_e2}: max_ev = {evals_RR[-1]:.6f}, "
          f"Tr = {np.trace(RR):.6f}")

# ─── 5. Understand why single-link gives zero ─────────────────────────────────
print("\n" + "=" * 60)
print("5. Algebraic analysis: why does P^T R P = 0 for single link?")
print("=" * 60)

# Key: compute P^T M_□(Q) P for a single plaquette with one perturbed link
# and check analytically

# For plaquette (e1, e2, e3, e4) with Q_{e1} = U, rest = I:
# B = v_{e1} + Ad(U) v_{e2} - Ad(U) v_{e3} - Ad(U) v_{e4}
# M^{diff}(e1,e1) = 0
# M^{diff}(e1,e2) = Ad(U) - I   [off-diagonal]
# M^{diff}(e2,e2) = Ad(U)^T Ad(U) - I = I - I = 0   [since Ad is orthogonal]
# etc.

# So the change in M_□ when Q_{e1} = U involves only Ad(U) - I factors.
# Let A = Ad(U) - I (3x3 matrix, zero when U = I)
# The relevant blocks of M_□(Q) - M_□(I):
# Case e0 = e1:
#   (e1, e2): +1*+1 * (I^T @ Ad(U) - I) = A
#   (e2, e1): A^T
#   (e1, e3): +1*-1 * (I^T @ Ad(U) - I) = -A
#   (e3, e1): -A^T
#   (e1, e4): +1*-1 * (I^T @ Ad(U) - I) = -A
#   (e4, e1): -A^T
#   (e2, e3): +1*-1 * (Ad(U)^T @ Ad(U) - I) = 0
#   ... all (e2,e2), (e2,e3), etc = 0 since Ad(U)^T Ad(U) = I
# So: dM = [e1-row/col only non-zero parts involving A]

# More precisely, dM_{(e1,b),(f,c)} = A_{bc} for f=e2, -A_{bc} for f=e3,e4
# dM_{(f,b),(e1,c)} = A^T_{bc} for f=e2, etc.
# dM at (e2,e2), (e2,e3), etc. = 0

# Therefore: P^T dM P has entries:
# (P^T dM P)_{ij} = sum_{f,g,b,c} P[f*3+b, i] * dM[(f,b),(g,c)] * P[g*3+c, j]
# = sum_{b,c} [sum_f P[f*3+b, i] dM[(f,b),(g,c)]] * P[g*3+c, j]

# For dM concentrated on edge e1:
# = sum_{b,c} P[e1*3+b, i] * [sum_g sum_{c} dM[(e1,b),(g,c)] * P[g*3+c, j]] +
#             [sum_f sum_b dM[(f,b),(e1,c)] * P[f*3+b, i]] * P[e1*3+c, j]

# Let p_{e1} = 3-vector (P[e1*3+a, col] for a=0,1,2) (component of P at edge e1)
# Then P^T dM P = (p_{e1} ⊗ q_{e1,other}^T) + ...

# Let me just compute this numerically for a specific case
ct_e = cotree[0]
U_specific = random_su2()
Q_test = list(Q_I)
Q_test[ct_e] = U_specific
M_test = make_M(Q_test)
dM = M_test - M_I

# Non-zero block structure of dM
nonzero_blocks = []
for e1 in range(nE):
    for e2 in range(nE):
        block = dM[e1*3:(e1+1)*3, e2*3:(e2+1)*3]
        if np.max(np.abs(block)) > 1e-12:
            nonzero_blocks.append((e1, e2, np.linalg.norm(block)))

print(f"\nNon-zero blocks of dM (single link {ct_e} perturbed):")
for e1, e2, norm in sorted(nonzero_blocks, key=lambda x: -x[2]):
    print(f"  ({e1:3d}, {e2:3d}): norm = {norm:.6f}")

# Compute p_e = P[e*3:(e+1)*3, :] for each edge
P_edge = [P[e*3:(e+1)*3, :] for e in range(nE)]  # list of (3, 9) matrices

# P^T dM P = sum_{e1,e2} P_edge[e1]^T @ dM_block[e1,e2] @ P_edge[e2]
result = np.zeros((P.shape[1], P.shape[1]))
for e1 in range(nE):
    for e2 in range(nE):
        block = dM[e1*3:(e1+1)*3, e2*3:(e2+1)*3]
        if np.max(np.abs(block)) > 1e-12:
            result += P_edge[e1].T @ block @ P_edge[e2]

print(f"\nP^T dM P (via manual block sum): max abs = {np.max(np.abs(result)):.2e}")
print(f"P^T dM P (direct): max abs = {np.max(np.abs(P.T @ dM @ P)):.2e}")

# Examine p_e vectors for edges involved in dM
involved_edges = list(set([e1 for e1,e2,_ in nonzero_blocks] + [e2 for e1,e2,_ in nonzero_blocks]))
print(f"\nP_edge vectors for edges involved in dM:")
for e in sorted(involved_edges):
    pe = P_edge[e]  # shape (3, 9)
    print(f"  Edge {e:3d} (dir={edge_direction(e)}, src={src_of(e):2d}): "
          f"P_edge norm = {np.linalg.norm(pe):.4f}, "
          f"nonzero pattern: {np.linalg.matrix_rank(pe)} rank")

# ─── 6. Test with many more single-link perturbations ────────────────────────
print("\n" + "=" * 60)
print("6. Systematic single-link test: all cotree edges")
print("=" * 60)

max_abs_RR_single = 0.0
for ct_e in cotree:
    for trial in range(10):
        Q_test = list(Q_I)
        Q_test[ct_e] = random_su2()
        M_test = make_M(Q_test)
        dM = M_test - M_I
        RR = P.T @ dM @ P
        v = np.max(np.abs(RR))
        if v > max_abs_RR_single:
            max_abs_RR_single = v

print(f"Max |P^T R(Q) P[i,j]| over all single-link perturbations (all cotree): {max_abs_RR_single:.2e}")

# Tree edges too
max_abs_RR_tree = 0.0
for tr_e in tree_edges:
    for trial in range(10):
        Q_test = list(Q_I)
        Q_test[tr_e] = random_su2()  # perturb tree edge (NOT gauge-fixed)
        M_test = make_M(Q_test)
        dM = M_test - M_I
        RR = P.T @ dM @ P
        v = np.max(np.abs(RR))
        if v > max_abs_RR_tree:
            max_abs_RR_tree = v

print(f"Max |P^T R(Q) P[i,j]| over all single-link perturbations (tree edges): {max_abs_RR_tree:.2e}")

# ─── 7. Second-order analysis ─────────────────────────────────────────────────
print("\n" + "=" * 60)
print("7. Second-order (two-link) cotree analysis via Taylor expansion")
print("=" * 60)

# For Q = exp(t * v_{e0}) on edge e0 (small t), compute P^T R P to order t^2
# We expect P^T R P ~ t^2 * (some symmetric form in v)

def R_proj_at_angle(ct_e, v3, t):
    """Q_e = exp(t * sum v3[i] T[i]), rest = I. Return max eval of P^T R P."""
    Q_test = list(Q_I)
    dQ = np.eye(2, dtype=complex)
    for i in range(3):
        # Use first-order: exp(t*X) ≈ I + t*X for small t
        pass
    from scipy.linalg import expm
    X = sum(v3[i] * T[i] for i in range(3))
    Q_test[ct_e] = expm(t * X)
    M_test = make_M(Q_test)
    RR = P.T @ (M_test - M_I) @ P
    return RR

ct_e = cotree[0]
v3 = np.array([1.0, 0.0, 0.0])  # direction in su(2)
print(f"\nP^T R P as function of angle t for cotree edge {ct_e}, direction T0:")
for t in [0.01, 0.05, 0.1, 0.3, 0.5, 1.0, np.pi/2, np.pi]:
    RR = R_proj_at_angle(ct_e, v3, t)
    max_ev = np.linalg.eigvalsh(RR)[-1]
    tr_RR = np.trace(RR)
    print(f"  t = {t:.3f}: max_ev = {max_ev:+.8f}, Tr = {tr_RR:+.8f}")

# Check t^2 scaling
print("\nScaling of max_ev with t^2:")
base_t = 0.1
RR0 = R_proj_at_angle(ct_e, v3, base_t)
max_ev0 = np.linalg.eigvalsh(RR0)[-1]
for t in [0.01, 0.05, 0.1, 0.2, 0.3]:
    RR = R_proj_at_angle(ct_e, v3, t)
    max_ev = np.linalg.eigvalsh(RR)[-1]
    ratio = max_ev / (t**2) if t > 0 else 0
    print(f"  t = {t:.3f}: max_ev/t^2 = {ratio:.6f}")

print("\nDONE")
