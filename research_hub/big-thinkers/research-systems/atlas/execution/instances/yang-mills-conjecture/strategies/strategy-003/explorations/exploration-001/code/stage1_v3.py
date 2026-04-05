"""
Stage 1 v3: Two-phase approach to maximize lambda_max(M(Q)).
Phase A: Random sampling of 1000 configs -> find range of lambda_max
Phase B: Targeted refinement of best configs using analytical single-edge optimization

Key insight for speed: For fixed eigenvector v, the Rayleigh quotient
v^T M(Q) v as a function of a SINGLE link Q_e can be evaluated very cheaply
(only 6 plaquettes depend on Q_e). We can sweep Q_e over a grid on SU(2).
"""

import numpy as np
from scipy.linalg import eigh
import time, sys

np.random.seed(2026)

# ============================================================
# SU(2) utilities (vectorized)
# ============================================================

SIGMA = [
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
]

def quaternion_to_su2(q):
    a, b, c, dd = q / np.linalg.norm(q)
    return np.array([[a + 1j*b, c + 1j*dd], [-c + 1j*dd, a - 1j*b]])

def su2_to_quaternion(U):
    return np.array([np.real(U[0,0]), np.imag(U[0,0]), np.real(U[0,1]), np.imag(U[0,1])])

def random_su2():
    v = np.random.randn(4); v /= np.linalg.norm(v)
    return quaternion_to_su2(v)

def su2_inv(Q):
    return Q.conj().T

def adjoint_rep(Q):
    Qinv = su2_inv(Q)
    Ad = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            Ad[i, j] = 0.5 * np.real(np.trace(SIGMA[i] @ Q @ SIGMA[j] @ Qinv))
    return Ad

# ============================================================
# Lattice
# ============================================================
L = 2; d = 4
num_sites = L**d; num_edges = d * num_sites; DIM = 3 * num_edges

def site_index(coords):
    idx = 0
    for i in range(d): idx = idx * L + (coords[i] % L)
    return idx

def index_to_coords(idx):
    coords = []
    for i in range(d): coords.append(idx % L); idx //= L
    return list(reversed(coords))

def edge_index(s, mu): return s * d + mu

def neighbor(s, mu, direction=1):
    c = index_to_coords(s); c[mu] = (c[mu] + direction) % L; return site_index(c)

def get_plaquettes():
    P = []
    for x in range(num_sites):
        for mu in range(d):
            for nu in range(mu+1, d):
                P.append([(edge_index(x,mu),+1), (edge_index(neighbor(x,mu),nu),+1),
                           (edge_index(neighbor(x,nu),mu),-1), (edge_index(x,nu),-1)])
    return P

PLAQUETTES = get_plaquettes()
EDGE_TO_PLAQS = [[] for _ in range(num_edges)]
for pi, p in enumerate(PLAQUETTES):
    for (e,o) in p: EDGE_TO_PLAQS[e].append(pi)

# ============================================================
# Build M(Q)
# ============================================================

def build_M(Q):
    M = np.zeros((DIM, DIM))
    for plaq in PLAQUETTES:
        (e1,o1),(e2,o2),(e3,o3),(e4,o4) = plaq
        H = [np.eye(2,dtype=complex), Q[e1], Q[e1]@Q[e2], Q[e1]@Q[e2]@su2_inv(Q[e3])]
        edges = [e1,e2,e3,e4]; signs = [o1,o2,o3,o4]
        blocks = [signs[k]*adjoint_rep(H[k]) for k in range(4)]
        for i in range(4):
            for j in range(4):
                M[3*edges[i]:3*edges[i]+3, 3*edges[j]:3*edges[j]+3] += blocks[i].T @ blocks[j]
    return M

def top_eigen(Q):
    M = build_M(Q)
    vals, vecs = eigh(M)
    return vals[-1], vecs[:,-1]

# ============================================================
# Phase A: Random sampling
# ============================================================

print("=" * 70)
print("PHASE A: Random Sampling (1000 configs)")
print("=" * 70)

t0 = time.time()
lmax_values = []
best_Q = None
best_lmax = -np.inf

for i in range(1000):
    Q = [random_su2() for _ in range(num_edges)]
    M = build_M(Q)
    lmax = np.max(eigh(M, eigvals_only=True))
    lmax_values.append(lmax)
    if lmax > best_lmax:
        best_lmax = lmax
        best_Q = [q.copy() for q in Q]
    if (i+1) % 100 == 0:
        print(f"  {i+1}/1000: max so far = {best_lmax:.6f}, current = {lmax:.6f}")
        sys.stdout.flush()

elapsed = time.time() - t0
lmax_arr = np.array(lmax_values)
print(f"\nPhase A complete in {elapsed:.1f}s")
print(f"  Max: {lmax_arr.max():.10f}")
print(f"  Min: {lmax_arr.min():.10f}")
print(f"  Mean: {lmax_arr.mean():.6f} ± {lmax_arr.std():.6f}")
print(f"  Median: {np.median(lmax_arr):.6f}")
print(f"  95th percentile: {np.percentile(lmax_arr, 95):.6f}")
print(f"  99th percentile: {np.percentile(lmax_arr, 99):.6f}")
print(f"  Count > 15: {np.sum(lmax_arr > 15)}")
print(f"  Count > 15.5: {np.sum(lmax_arr > 15.5)}")
print(f"  Count > 16: {np.sum(lmax_arr > 16)}")

# ============================================================
# Phase B: Refine top configs using grid search on SU(2) per edge
# ============================================================

print("\n" + "=" * 70)
print("PHASE B: Targeted Refinement of Best Config")
print("=" * 70)

# SU(2) grid: Fibonacci sphere on S³ (unit quaternions)
def su2_grid(n_points):
    """Generate approximately uniform points on SU(2) ≅ S³."""
    points = []
    golden = (1 + np.sqrt(5)) / 2
    for i in range(n_points):
        # Use spherical Fibonacci for S³
        t1 = np.arccos(1 - 2*(i+0.5)/n_points)
        t2 = 2 * np.pi * i / golden
        t3 = 2 * np.pi * i / (golden**2)
        q = np.array([
            np.cos(t1/2) * np.cos(t2/2),
            np.cos(t1/2) * np.sin(t2/2),
            np.sin(t1/2) * np.cos(t3/2),
            np.sin(t1/2) * np.sin(t3/2),
        ])
        q /= np.linalg.norm(q)
        points.append(q)
    return points

GRID = su2_grid(200)  # 200 points on SU(2)

def refine_config(Q, max_cycles=20, verbose=True):
    """
    Refine Q by cycling through edges, trying grid points on SU(2) for each edge.
    """
    lmax, v = top_eigen(Q)
    if verbose: print(f"  Start: λ_max = {lmax:.10f}")

    for cycle in range(max_cycles):
        improved = False
        for e in range(num_edges):
            # Current Rayleigh quotient contribution from plaquettes containing e
            current_rq = 0
            for pi in EDGE_TO_PLAQS[e]:
                plaq = PLAQUETTES[pi]
                (e1,o1),(e2,o2),(e3,o3),(e4,o4) = plaq
                H = [np.eye(2,dtype=complex), Q[e1], Q[e1]@Q[e2], Q[e1]@Q[e2]@su2_inv(Q[e3])]
                edges = [e1,e2,e3,e4]; signs = [o1,o2,o3,o4]
                B = np.zeros(3)
                for k in range(4):
                    B += signs[k] * adjoint_rep(H[k]) @ v[3*edges[k]:3*edges[k]+3]
                current_rq += np.dot(B, B)

            # Try grid points
            Q_orig = Q[e].copy()
            best_rq = current_rq
            best_Qe = Q_orig

            for q in GRID:
                Q[e] = quaternion_to_su2(q)
                rq = 0
                for pi in EDGE_TO_PLAQS[e]:
                    plaq = PLAQUETTES[pi]
                    (e1,o1),(e2,o2),(e3,o3),(e4,o4) = plaq
                    H = [np.eye(2,dtype=complex), Q[e1], Q[e1]@Q[e2], Q[e1]@Q[e2]@su2_inv(Q[e3])]
                    edges = [e1,e2,e3,e4]; signs = [o1,o2,o3,o4]
                    B = np.zeros(3)
                    for k in range(4):
                        B += signs[k] * adjoint_rep(H[k]) @ v[3*edges[k]:3*edges[k]+3]
                    rq += np.dot(B, B)
                if rq > best_rq + 1e-12:
                    best_rq = rq
                    best_Qe = Q[e].copy()
                    improved = True

            Q[e] = best_Qe

        # Recompute eigenvector
        lmax_new, v_new = top_eigen(Q)
        delta = lmax_new - lmax
        if verbose and (cycle < 3 or cycle % 5 == 0 or abs(delta) < 1e-8):
            print(f"  Cycle {cycle+1}: λ_max = {lmax_new:.10f} (delta = {delta:.2e})")

        if abs(delta) < 1e-8 and not improved:
            if verbose: print(f"  Converged at cycle {cycle+1}")
            lmax = lmax_new; v = v_new
            break
        lmax = lmax_new; v = v_new

    return lmax, v, Q

# Refine the best config from Phase A
print("\nRefining best random config:")
lmax_refined, v_refined, Q_refined = refine_config([q.copy() for q in best_Q], verbose=True)

# Also try from identity (known optimum)
print("\nRefining from identity:")
Q_id = [np.eye(2, dtype=complex) for _ in range(num_edges)]
lmax_id, v_id, Q_id_ref = refine_config(Q_id, max_cycles=10, verbose=True)

# Also try from "anti-aligned" configs: Q = diag(i, -i) = i*σ3
print("\nRefining from σ3 (maximally non-trivial):")
Q_s3 = [1j * SIGMA[2] for _ in range(num_edges)]
lmax_s3, v_s3, Q_s3_ref = refine_config(Q_s3, max_cycles=10, verbose=True)

# Try from -I (center of SU(2))
print("\nRefining from -I:")
Q_mI = [-np.eye(2, dtype=complex) for _ in range(num_edges)]
lmax_mI, v_mI, Q_mI_ref = refine_config(Q_mI, max_cycles=10, verbose=True)

# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 70)
print("STAGE 1 FINAL RESULTS")
print("=" * 70)
all_refined = [lmax_refined, lmax_id, lmax_s3, lmax_mI]
labels = ['best-random-refined', 'identity-refined', 'sigma3-refined', '-I-refined']
for lab, val in zip(labels, all_refined):
    print(f"  {lab}: λ_max = {val:.10f}")

print(f"\nOverall maximum: {max(all_refined):.10f}")
print(f"Exceeds 16? {max(all_refined) > 16.0 + 1e-6}")
print(f"\nFrom 1000 random samples: max = {lmax_arr.max():.10f}")
print(f"After refinement: max = {max(all_refined):.10f}")

# Staggered decomposition
print("\n" + "=" * 70)
print("STAGE 3: Eigenvector Decomposition")
print("=" * 70)

def staggered_sign(x):
    coords = index_to_coords(x)
    return (-1)**sum(coords)

stag_vecs = []
for mu in range(d):
    for a in range(3):
        v = np.zeros(DIM)
        for x in range(num_sites):
            e = edge_index(x, mu)
            v[3*e + a] = staggered_sign(x)
        v /= np.linalg.norm(v)
        stag_vecs.append(v)
S_proj = np.column_stack(stag_vecs)

for lab, v in [('best-random', v_refined), ('identity', v_id), ('sigma3', v_s3), ('-I', v_mI)]:
    v_n = v / np.linalg.norm(v)
    stag_coeffs = S_proj.T @ v_n
    stag_frac = np.dot(stag_coeffs, stag_coeffs)
    print(f"  {lab}: staggered fraction = {stag_frac:.6f}, non-staggered = {1-stag_frac:.6f}")

# Non-staggered eigenvalue
print("\nNon-staggered eigenvalues:")
for lab, Q in [('best-random', Q_refined), ('identity', Q_id_ref), ('sigma3', Q_s3_ref)]:
    M = build_M(Q)
    P = np.eye(DIM) - S_proj @ S_proj.T
    M_ns = P @ M @ P
    vals_ns = eigh(M_ns, eigvals_only=True)
    M_full_vals = eigh(M, eigvals_only=True)
    print(f"  {lab}: full λ_max = {M_full_vals[-1]:.6f}, non-stag λ_max = {vals_ns[-1]:.6f}")

print("\nDONE")
