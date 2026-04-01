"""
Stage 1: Fast gradient ascent to maximize lambda_max(M(Q)).
Optimized version using:
- scipy.sparse.linalg.eigsh for top eigenvalue only
- Rayleigh quotient optimization (alternating: fix eigvec, optimize Q; then recompute eigvec)
- Vectorized adjoint rep computation
"""

import numpy as np
from scipy.linalg import eigh
from scipy.sparse.linalg import eigsh
from scipy.optimize import minimize
from scipy.linalg import expm
import time

np.random.seed(2026)

# ============================================================
# SU(2) utilities
# ============================================================

SIGMA = [
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
]

def quaternion_to_su2(q):
    a, b, c, d = q / np.linalg.norm(q)
    return np.array([[a + 1j*b, c + 1j*d], [-c + 1j*d, a - 1j*b]])

def su2_to_quaternion(U):
    return np.array([np.real(U[0,0]), np.imag(U[0,0]), np.real(U[0,1]), np.imag(U[0,1])])

def random_su2():
    v = np.random.randn(4)
    v /= np.linalg.norm(v)
    return quaternion_to_su2(v)

def su2_inv(Q):
    return Q.conj().T

def adjoint_rep(Q):
    """3x3 SO(3) adjoint representation."""
    # Fast formula using quaternion: if Q = a + bi*σ1 + ci*σ2 + di*σ3
    a = np.real(Q[0, 0])
    b = np.imag(Q[0, 0])
    c = np.real(Q[0, 1])
    dd = np.imag(Q[0, 1])

    # Rodrigues formula for quaternion rotation
    # R_{ij} = (a²-|r|²)δ_{ij} + 2r_i r_j + 2a ε_{ijk} r_k
    # where r = (b, c, d) — BUT CAREFUL: our quaternion convention maps to specific SU(2)
    # Actually for SU(2) = a*I + i*(b*σ1 + c*σ2 + d*σ3):
    # [Ad_Q]_{ij} = (a²+b²+c²+d²=1 since unit) = (2a²-1)δ_{ij} + 2(r_ir_j + a*ε_{ijk}*r_k)
    # Wait, need to be careful. Let me just use the Pauli trace formula.

    Qinv = su2_inv(Q)
    Ad = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            Ad[i, j] = 0.5 * np.real(np.trace(SIGMA[i] @ Q @ SIGMA[j] @ Qinv))
    return Ad

# ============================================================
# Lattice Setup
# ============================================================

L = 2
d = 4
num_sites = L**d  # 16
num_edges = d * num_sites  # 64
DIM = 3 * num_edges  # 192

def site_index(coords):
    idx = 0
    for i in range(d):
        idx = idx * L + (coords[i] % L)
    return idx

def index_to_coords(idx):
    coords = []
    for i in range(d):
        coords.append(idx % L)
        idx //= L
    return list(reversed(coords))

def edge_index(site_idx, mu):
    return site_idx * d + mu

def neighbor(site_idx, mu, direction=1):
    coords = index_to_coords(site_idx)
    coords[mu] = (coords[mu] + direction) % L
    return site_index(coords)

def get_plaquettes():
    plaquettes = []
    for x in range(num_sites):
        for mu in range(d):
            for nu in range(mu + 1, d):
                x_mu = neighbor(x, mu)
                x_nu = neighbor(x, nu)
                e1 = edge_index(x, mu)
                e2 = edge_index(x_mu, nu)
                e3 = edge_index(x_nu, mu)
                e4 = edge_index(x, nu)
                plaquettes.append([(e1, +1), (e2, +1), (e3, -1), (e4, -1)])
    return plaquettes

PLAQUETTES = get_plaquettes()

# Precompute: which plaquettes contain each edge?
EDGE_TO_PLAQS = [[] for _ in range(num_edges)]
for p_idx, plaq in enumerate(PLAQUETTES):
    for (e, o) in plaq:
        EDGE_TO_PLAQS[e].append(p_idx)

# ============================================================
# Build M(Q) — core routine
# ============================================================

def build_M(Q):
    """Build the full M(Q) matrix."""
    M = np.zeros((DIM, DIM))
    for plaq in PLAQUETTES:
        (e1, o1), (e2, o2), (e3, o3), (e4, o4) = plaq
        H1 = np.eye(2, dtype=complex)
        H2 = Q[e1]
        H3 = Q[e1] @ Q[e2]
        H4 = Q[e1] @ Q[e2] @ su2_inv(Q[e3])
        edges = [e1, e2, e3, e4]
        signs = [o1, o2, o3, o4]
        Hs = [H1, H2, H3, H4]
        blocks = [signs[k] * adjoint_rep(Hs[k]) for k in range(4)]
        for i in range(4):
            for j in range(4):
                M[3*edges[i]:3*edges[i]+3, 3*edges[j]:3*edges[j]+3] += blocks[i].T @ blocks[j]
    return M

def lambda_max_full(Q):
    """Top eigenvalue + eigenvector using full eigendecomposition."""
    M = build_M(Q)
    eigvals, eigvecs = eigh(M)
    idx = np.argmax(eigvals)
    return eigvals[idx], eigvecs[:, idx]

def lambda_max_top(Q):
    """Top eigenvalue only."""
    M = build_M(Q)
    return np.max(eigh(M, eigvals_only=True))

# ============================================================
# Rayleigh quotient: v^T M(Q) v for fixed v
# ============================================================

def compute_B_plaq(Q, v, plaq):
    """Compute B_□(Q, v) for one plaquette."""
    (e1, o1), (e2, o2), (e3, o3), (e4, o4) = plaq
    H1 = np.eye(2, dtype=complex)
    H2 = Q[e1]
    H3 = Q[e1] @ Q[e2]
    H4 = Q[e1] @ Q[e2] @ su2_inv(Q[e3])
    B = np.zeros(3)
    for (e, o, H) in [(e1,o1,H1), (e2,o2,H2), (e3,o3,H3), (e4,o4,H4)]:
        B += o * adjoint_rep(H) @ v[3*e:3*e+3]
    return B

def rayleigh_quotient(Q, v):
    """v^T M(Q) v = Σ_□ |B_□|²."""
    total = 0.0
    for plaq in PLAQUETTES:
        B = compute_B_plaq(Q, v, plaq)
        total += np.dot(B, B)
    return total

# ============================================================
# Edge-by-edge optimization (fast: optimize Rayleigh quotient)
# ============================================================

def optimize_edge_rayleigh(Q, edge, v):
    """
    Optimize Q[edge] to maximize v^T M(Q) v (Rayleigh quotient with fixed v).
    Only plaquettes containing this edge are affected.
    Much faster than full eigenvalue optimization.
    """
    affected_plaqs = [PLAQUETTES[p] for p in EDGE_TO_PLAQS[edge]]
    Q_orig = Q[edge].copy()

    def neg_rayleigh(params):
        q = params / np.linalg.norm(params)
        Q[edge] = quaternion_to_su2(q)
        total = 0.0
        for plaq in affected_plaqs:
            B = compute_B_plaq(Q, v, plaq)
            total += np.dot(B, B)
        return -total

    q0 = su2_to_quaternion(Q[edge])
    result = minimize(neg_rayleigh, q0, method='Nelder-Mead',
                     options={'maxiter': 100, 'xatol': 1e-10, 'fatol': 1e-10})
    q_opt = result.x / np.linalg.norm(result.x)
    Q[edge] = quaternion_to_su2(q_opt)
    return -result.fun

def alternating_optimization(Q, max_outer=20, max_inner_cycles=3, tol=1e-8, verbose=True):
    """
    Alternating optimization:
    1. Compute top eigenvector v
    2. For each edge, optimize Q_e to maximize v^T M v (Rayleigh quotient)
    3. Repeat
    """
    lmax, v = lambda_max_full(Q)
    if verbose:
        print(f"  Initial λ_max = {lmax:.10f}")

    for outer in range(max_outer):
        # Fix v, optimize Q edge-by-edge
        for inner in range(max_inner_cycles):
            rq_before = rayleigh_quotient(Q, v)
            for e in range(num_edges):
                optimize_edge_rayleigh(Q, e, v)
            rq_after = rayleigh_quotient(Q, v)
            if abs(rq_after - rq_before) < tol:
                break

        # Fix Q, recompute top eigenvector
        lmax_new, v_new = lambda_max_full(Q)

        if verbose and (outer < 3 or outer % 5 == 0):
            print(f"  Outer {outer+1}: λ_max = {lmax_new:.10f} (delta = {lmax_new - lmax:.2e})")

        if abs(lmax_new - lmax) < tol:
            if verbose:
                print(f"  Converged at outer iteration {outer+1}")
            lmax = lmax_new
            v = v_new
            break
        lmax = lmax_new
        v = v_new

    return lmax, v

# ============================================================
# Main: Run from multiple random starts
# ============================================================

print("=" * 70)
print("STAGE 1: Fast Gradient Ascent to Maximize lambda_max(M(Q))")
print("=" * 70)

all_results = []

# 20 random starts
print("\n--- Random SU(2) starts ---")
for trial in range(20):
    t0 = time.time()
    Q = [random_su2() for _ in range(num_edges)]
    lmax_init = lambda_max_top(Q)

    lmax_final, v_final = alternating_optimization(Q, max_outer=15, verbose=False)
    elapsed = time.time() - t0

    exceeds = lmax_final > 16.0 + 1e-6
    marker = " *** EXCEEDS 16 ***" if exceeds else ""
    print(f"Trial {trial+1:2d}: init={lmax_init:.4f} -> final={lmax_final:.10f}  ({elapsed:.1f}s){marker}")

    all_results.append({
        'trial': f'random-{trial+1}',
        'init': lmax_init,
        'final': lmax_final,
        'Q': [su2_to_quaternion(Q[e]) for e in range(num_edges)] if exceeds else None,
        'v': v_final if exceeds else None,
    })

# 5 near-identity starts
print("\n--- Near-identity starts (eps=0.3) ---")
for trial in range(5):
    t0 = time.time()
    Q = []
    for _ in range(num_edges):
        v = np.random.randn(3) * 0.3
        A = np.zeros((2, 2), dtype=complex)
        for a in range(3):
            A += 1j * v[a] * SIGMA[a] / 2.0
        Q.append(expm(A))
    lmax_init = lambda_max_top(Q)

    lmax_final, v_final = alternating_optimization(Q, max_outer=15, verbose=False)
    elapsed = time.time() - t0

    exceeds = lmax_final > 16.0 + 1e-6
    marker = " *** EXCEEDS 16 ***" if exceeds else ""
    print(f"Trial {trial+1:2d}: init={lmax_init:.4f} -> final={lmax_final:.10f}  ({elapsed:.1f}s){marker}")

    all_results.append({
        'trial': f'nearid-{trial+1}',
        'init': lmax_init,
        'final': lmax_final,
        'Q': [su2_to_quaternion(Q[e]) for e in range(num_edges)] if exceeds else None,
        'v': v_final if exceeds else None,
    })

# 5 adversarial starts (half random, half identity)
print("\n--- Adversarial starts (half random) ---")
for trial in range(5):
    t0 = time.time()
    Q = []
    for e in range(num_edges):
        if e < num_edges // 2:
            Q.append(random_su2())
        else:
            Q.append(np.eye(2, dtype=complex))
    lmax_init = lambda_max_top(Q)

    lmax_final, v_final = alternating_optimization(Q, max_outer=15, verbose=False)
    elapsed = time.time() - t0

    exceeds = lmax_final > 16.0 + 1e-6
    marker = " *** EXCEEDS 16 ***" if exceeds else ""
    print(f"Trial {trial+1:2d}: init={lmax_init:.4f} -> final={lmax_final:.10f}  ({elapsed:.1f}s){marker}")

    all_results.append({
        'trial': f'advers-{trial+1}',
        'init': lmax_init,
        'final': lmax_final,
        'Q': [su2_to_quaternion(Q[e]) for e in range(num_edges)] if exceeds else None,
        'v': v_final if exceeds else None,
    })

# ============================================================
# Summary
# ============================================================

finals = [r['final'] for r in all_results]
print("\n" + "=" * 70)
print("RESULTS SUMMARY")
print("=" * 70)
print(f"Total trials: {len(all_results)}")
print(f"Maximum λ_max: {max(finals):.10f}")
print(f"Minimum λ_max: {min(finals):.10f}")
print(f"Mean λ_max:    {np.mean(finals):.10f}")
print(f"Std λ_max:     {np.std(finals):.10f}")
print(f"\nExceeds 16? {max(finals) > 16.0 + 1e-6}")

counterexamples = [r for r in all_results if r['Q'] is not None]
if counterexamples:
    print(f"\n*** {len(counterexamples)} COUNTEREXAMPLE(S) FOUND ***")
    for ce in counterexamples:
        print(f"  {ce['trial']}: λ_max = {ce['final']:.10f}")
        np.savez(f"counterexample_{ce['trial']}.npz",
                 Q=ce['Q'], v=ce['v'], lmax=ce['final'])
else:
    print("\nNo counterexamples found. Conjecture λ_max(M(Q)) ≤ 16 is consistent.")

# ============================================================
# Staggered decomposition of top eigenvectors
# ============================================================

print("\n" + "=" * 70)
print("STAGE 3: Eigenvector Decomposition")
print("=" * 70)

# Rerun a few trials and save eigenvector info
print(f"\n{'Trial':<15} {'λ_max':>12} {'stag_frac':>10} {'nonstag_frac':>12}")
print("-" * 52)

# Build staggered projector
# Staggered modes: v_{x,mu,a} = (-1)^{Σ x_i} * c_{mu,a}
# There are d*3 = 12 staggered modes (choosing mu, a), but with constraint Σ_mu c_{mu,a} = 0
# giving (d-1)*3 = 9 modes.
# For simplicity, project onto the staggered subspace.

# Staggered basis vectors: for each (mu, a), define s_{mu,a} with
# s_{mu,a}[x, nu, b] = (-1)^{Σ x_i} * δ_{nu,mu} * δ_{b,a}
def staggered_sign(x):
    coords = index_to_coords(x)
    return (-1)**sum(coords)

staggered_vecs = []
for mu in range(d):
    for a in range(3):
        v = np.zeros(DIM)
        for x in range(num_sites):
            e = edge_index(x, mu)
            v[3*e + a] = staggered_sign(x)
        v /= np.linalg.norm(v)
        staggered_vecs.append(v)

# Orthonormalize (they should already be orthonormal)
S = np.column_stack(staggered_vecs)  # 192 x 12

# The constrained staggered subspace (Σ_mu = 0 per color) removes 3 modes
# For now, just project onto the full staggered span

for r in all_results[:10]:
    # Recompute the configuration and eigenvector
    if r['Q'] is not None:
        Q = [quaternion_to_su2(q) for q in r['Q']]
    else:
        # Regenerate (won't exactly match due to seed issues, but close enough)
        continue

    lmax, v = lambda_max_full(Q)
    v /= np.linalg.norm(v)

    # Project onto staggered subspace
    stag_comp = S.T @ v  # 12-vector of coefficients
    stag_frac = np.dot(stag_comp, stag_comp)
    nonstag_frac = 1.0 - stag_frac

    print(f"{r['trial']:<15} {lmax:>12.6f} {stag_frac:>10.4f} {nonstag_frac:>12.4f}")

# Do some fresh trials with decomposition
for trial in range(10):
    Q = [random_su2() for _ in range(num_edges)]
    lmax_final, v_final = alternating_optimization(Q, max_outer=10, verbose=False)
    v_final /= np.linalg.norm(v_final)

    stag_comp = S.T @ v_final
    stag_frac = np.dot(stag_comp, stag_comp)
    nonstag_frac = 1.0 - stag_frac

    print(f"{'fresh-'+str(trial+1):<15} {lmax_final:>12.6f} {stag_frac:>10.4f} {nonstag_frac:>12.4f}")

# Max non-staggered eigenvalue
print("\nMax eigenvalue in non-staggered subspace:")
for trial in range(5):
    Q = [random_su2() for _ in range(num_edges)]
    lmax_final, _ = alternating_optimization(Q, max_outer=10, verbose=False)

    M = build_M(Q)
    # Project M onto non-staggered subspace
    # P_nonstag = I - S (S^T S)^{-1} S^T = I - S S^T (since S columns are orthonormal)
    P = np.eye(DIM) - S @ S.T
    M_nonstag = P @ M @ P
    eigvals_ns = eigh(M_nonstag, eigvals_only=True)
    lmax_ns = np.max(eigvals_ns)

    print(f"  Trial {trial+1}: full λ_max = {lmax_final:.6f}, non-stag λ_max = {lmax_ns:.6f}")

print("\n" + "=" * 70)
print("STAGES 1+3 COMPLETE")
print("=" * 70)
