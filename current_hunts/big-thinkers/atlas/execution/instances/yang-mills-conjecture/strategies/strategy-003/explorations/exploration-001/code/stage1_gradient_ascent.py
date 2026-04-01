"""
Stage 1: Edge-by-edge gradient ascent to maximize lambda_max(M(Q)).
L=2, d=4 hypercubic torus with SU(2) gauge group.

Strategy: For each edge, find Q_e that maximizes lambda_max while all others are fixed.
Since SU(2) is 3-dimensional, we parameterize Q_e and optimize using scipy.
"""

import numpy as np
from scipy.linalg import eigh
from scipy.optimize import minimize
import time

np.random.seed(2026)

# ============================================================
# SU(2) and Adjoint Representation (same as stage0)
# ============================================================

SIGMA = [
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
]

def quaternion_to_su2(q):
    """Convert unit quaternion (a,b,c,d) to SU(2) matrix."""
    a, b, c, d = q
    return np.array([[a + 1j*b, c + 1j*d],
                     [-c + 1j*d, a - 1j*b]])

def su2_to_quaternion(U):
    """Extract unit quaternion from SU(2) matrix."""
    a = np.real(U[0, 0])
    b = np.imag(U[0, 0])
    c = np.real(U[0, 1])
    d = np.imag(U[0, 1])
    return np.array([a, b, c, d])

def random_su2():
    """Random Haar-distributed SU(2) element."""
    v = np.random.randn(4)
    v /= np.linalg.norm(v)
    return quaternion_to_su2(v)

def su2_inv(Q):
    return Q.conj().T

def adjoint_rep(Q):
    """3x3 SO(3) adjoint representation."""
    Qinv = su2_inv(Q)
    Ad = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            Ad[i, j] = 0.5 * np.real(np.trace(SIGMA[i] @ Q @ SIGMA[j] @ Qinv))
    return Ad

# Precompute adjoint reps with caching
_ad_cache = {}
def adjoint_rep_cached(Q_tuple):
    if Q_tuple not in _ad_cache:
        Q = np.array([[Q_tuple[0], Q_tuple[1]], [Q_tuple[2], Q_tuple[3]]])
        _ad_cache[Q_tuple] = adjoint_rep(Q)
    return _ad_cache[Q_tuple]

# ============================================================
# Lattice Setup
# ============================================================

L = 2
d = 4
num_sites = L**d
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

# For each edge, which plaquettes contain it?
EDGE_PLAQUETTES = [[] for _ in range(num_edges)]
for p_idx, plaq in enumerate(PLAQUETTES):
    for (e, o) in plaq:
        EDGE_PLAQUETTES[e].append(p_idx)

# ============================================================
# Build M(Q) — optimized version
# ============================================================

def build_M(Q):
    """Build the full M(Q) matrix."""
    dim = 3 * num_edges
    M = np.zeros((dim, dim))

    for plaq in PLAQUETTES:
        (e1, o1), (e2, o2), (e3, o3), (e4, o4) = plaq

        H1 = np.eye(2, dtype=complex)
        H2 = Q[e1]
        H3 = Q[e1] @ Q[e2]
        H4 = Q[e1] @ Q[e2] @ su2_inv(Q[e3])

        edges = [e1, e2, e3, e4]
        signs = [o1, o2, o3, o4]
        Hs = [H1, H2, H3, H4]

        blocks = []
        for k in range(4):
            blocks.append(signs[k] * adjoint_rep(Hs[k]))

        for i in range(4):
            for j in range(4):
                ei = edges[i]
                ej = edges[j]
                M[3*ei:3*ei+3, 3*ej:3*ej+3] += blocks[i].T @ blocks[j]

    return M

def compute_lambda_max(Q):
    """Compute maximum eigenvalue of M(Q)."""
    M = build_M(Q)
    eigvals = eigh(M, eigvals_only=True)
    return np.max(eigvals)

# ============================================================
# Edge-by-edge optimization
# ============================================================

def optimize_single_edge(Q, edge_idx):
    """
    Optimize Q[edge_idx] to maximize lambda_max(M(Q)).
    Uses quaternion parameterization of SU(2).
    """
    best_lmax = -np.inf
    best_q = su2_to_quaternion(Q[edge_idx])

    def neg_lambda_max(params):
        """Negative of lambda_max as function of quaternion params."""
        q = params / np.linalg.norm(params)  # project to unit quaternion
        Q[edge_idx] = quaternion_to_su2(q)
        M = build_M(Q)
        eigvals = eigh(M, eigvals_only=True)
        return -np.max(eigvals)

    # Start from current quaternion
    q0 = su2_to_quaternion(Q[edge_idx])

    result = minimize(neg_lambda_max, q0, method='Nelder-Mead',
                     options={'maxiter': 200, 'xatol': 1e-10, 'fatol': 1e-10})

    # Restore best
    q_opt = result.x / np.linalg.norm(result.x)
    Q[edge_idx] = quaternion_to_su2(q_opt)
    return -result.fun

def gradient_ascent_cycle(Q, verbose=False):
    """One full cycle through all edges."""
    lmax_before = compute_lambda_max(Q)
    for e in range(num_edges):
        optimize_single_edge(Q, e)
    lmax_after = compute_lambda_max(Q)
    if verbose:
        print(f"  Cycle: {lmax_before:.10f} -> {lmax_after:.10f} (delta = {lmax_after - lmax_before:.2e})")
    return lmax_after, abs(lmax_after - lmax_before)

# ============================================================
# Main: Run gradient ascent from multiple random starts
# ============================================================

print("=" * 70)
print("STAGE 1: Gradient Ascent to Maximize lambda_max(M(Q))")
print("=" * 70)

num_trials = 20
max_cycles = 30
conv_threshold = 1e-8

results = []

for trial in range(num_trials):
    t0 = time.time()
    Q = [random_su2() for _ in range(num_edges)]

    lmax_init = compute_lambda_max(Q)
    print(f"\nTrial {trial+1}/{num_trials}: initial lambda_max = {lmax_init:.6f}")

    for cycle in range(max_cycles):
        lmax, delta = gradient_ascent_cycle(Q, verbose=(cycle < 3 or cycle % 5 == 0))
        if delta < conv_threshold:
            print(f"  Converged at cycle {cycle+1}, lambda_max = {lmax:.10f}")
            break
    else:
        print(f"  Max cycles reached, lambda_max = {lmax:.10f}")

    elapsed = time.time() - t0
    print(f"  Time: {elapsed:.1f}s")

    # Save configuration if lambda_max > 16
    config_data = None
    if lmax > 16.0 + 1e-6:
        config_data = [su2_to_quaternion(Q[e]) for e in range(num_edges)]

    results.append({
        'trial': trial + 1,
        'lmax_init': lmax_init,
        'lmax_final': lmax,
        'converged': delta < conv_threshold,
        'config': config_data
    })

# ============================================================
# Additional trials from near-identity and adversarial starts
# ============================================================

print("\n" + "=" * 70)
print("Additional trials: near-identity starts (eps=0.3)")
print("=" * 70)

for trial in range(5):
    t0 = time.time()
    Q = []
    for _ in range(num_edges):
        v = np.random.randn(3) * 0.3
        A = np.zeros((2, 2), dtype=complex)
        for a in range(3):
            A += 1j * v[a] * SIGMA[a] / 2.0
        from scipy.linalg import expm
        Q.append(expm(A))

    lmax_init = compute_lambda_max(Q)
    print(f"\nNear-ID Trial {trial+1}: initial lambda_max = {lmax_init:.6f}")

    for cycle in range(max_cycles):
        lmax, delta = gradient_ascent_cycle(Q, verbose=(cycle < 2))
        if delta < conv_threshold:
            print(f"  Converged at cycle {cycle+1}, lambda_max = {lmax:.10f}")
            break

    elapsed = time.time() - t0
    config_data = None
    if lmax > 16.0 + 1e-6:
        config_data = [su2_to_quaternion(Q[e]) for e in range(num_edges)]
    results.append({
        'trial': f'near-id-{trial+1}',
        'lmax_init': lmax_init,
        'lmax_final': lmax,
        'converged': delta < conv_threshold,
        'config': config_data
    })

print("\n" + "=" * 70)
print("Additional trials: adversarial starts (half links random)")
print("=" * 70)

for trial in range(5):
    t0 = time.time()
    Q = []
    for e in range(num_edges):
        if e < num_edges // 2:
            Q.append(random_su2())
        else:
            Q.append(np.eye(2, dtype=complex))

    lmax_init = compute_lambda_max(Q)
    print(f"\nAdversarial Trial {trial+1}: initial lambda_max = {lmax_init:.6f}")

    for cycle in range(max_cycles):
        lmax, delta = gradient_ascent_cycle(Q, verbose=(cycle < 2))
        if delta < conv_threshold:
            print(f"  Converged at cycle {cycle+1}, lambda_max = {lmax:.10f}")
            break

    elapsed = time.time() - t0
    config_data = None
    if lmax > 16.0 + 1e-6:
        config_data = [su2_to_quaternion(Q[e]) for e in range(num_edges)]
    results.append({
        'trial': f'adversarial-{trial+1}',
        'lmax_init': lmax_init,
        'lmax_final': lmax,
        'converged': delta < conv_threshold,
        'config': config_data
    })

# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 70)
print("RESULTS SUMMARY")
print("=" * 70)
print(f"{'Trial':<20} {'Init λ_max':>12} {'Final λ_max':>14} {'Conv':>6}")
print("-" * 55)
all_final = []
for r in results:
    print(f"{str(r['trial']):<20} {r['lmax_init']:>12.6f} {r['lmax_final']:>14.10f} {'Y' if r['converged'] else 'N':>6}")
    all_final.append(r['lmax_final'])

print(f"\nMaximum λ_max found: {max(all_final):.10f}")
print(f"Minimum λ_max found: {min(all_final):.10f}")
print(f"Mean λ_max found:    {np.mean(all_final):.10f}")
print(f"\nExceeds 16? {max(all_final) > 16.0 + 1e-6}")

# Save any counterexamples
for r in results:
    if r['config'] is not None:
        fname = f"counterexample_trial_{r['trial']}.npy"
        np.save(fname, r['config'])
        print(f"\nCounterexample saved: {fname}")
        print(f"  lambda_max = {r['lmax_final']:.10f}")
