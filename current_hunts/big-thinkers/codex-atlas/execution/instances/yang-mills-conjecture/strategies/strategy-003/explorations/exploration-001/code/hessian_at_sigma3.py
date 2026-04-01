"""
Compute the full Hessian of S at Q = iσ₃ via finite differences.
Compare spectrum with (β/2N) M(Q).
"""

import numpy as np
from scipy.linalg import eigh, expm
import time

SIGMA = [
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
]

def su2_inv(Q): return Q.conj().T

def adjoint_rep(Q):
    Qinv = su2_inv(Q)
    Ad = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            Ad[i, j] = 0.5 * np.real(np.trace(SIGMA[i] @ Q @ SIGMA[j] @ Qinv))
    return Ad

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
def neighbor(s, mu, dir=1):
    c = index_to_coords(s); c[mu] = (c[mu] + dir) % L; return site_index(c)
def get_plaquettes():
    P = []
    for x in range(num_sites):
        for mu in range(d):
            for nu in range(mu+1, d):
                P.append([(edge_index(x,mu),+1), (edge_index(neighbor(x,mu),nu),+1),
                           (edge_index(neighbor(x,nu),mu),-1), (edge_index(x,nu),-1)])
    return P
PLAQUETTES = get_plaquettes()

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

def compute_holonomy(Q, plaq):
    U = np.eye(2, dtype=complex)
    for (e, o) in plaq:
        if o == +1: U = U @ Q[e]
        else: U = U @ su2_inv(Q[e])
    return U

def wilson_action(Q, beta=1.0, N=2):
    S = 0.0
    for plaq in PLAQUETTES:
        U = compute_holonomy(Q, plaq)
        S -= (beta / N) * np.real(np.trace(U))
    return S

# ============================================================
# Compute gradient of S at Q via finite differences
# ============================================================

def gradient_S(Q, eps=1e-6, beta=1.0, N=2):
    """Compute ∂S/∂v_{e,a} for all e,a by finite differences."""
    grad = np.zeros(DIM)
    for e in range(num_edges):
        for a in range(3):
            d_vec = np.zeros(3); d_vec[a] = 1.0
            A = np.zeros((2,2), dtype=complex)
            for b in range(3):
                A += 1j * d_vec[b] * SIGMA[b] / 2.0

            Q_plus = list(Q)
            Q_minus = list(Q)
            Q_plus[e] = expm(eps * A) @ Q[e]
            Q_minus[e] = expm(-eps * A) @ Q[e]

            Sp = wilson_action(Q_plus, beta, N)
            Sm = wilson_action(Q_minus, beta, N)
            grad[3*e + a] = (Sp - Sm) / (2 * eps)
    return grad

# ============================================================
# Compute Hessian-vector product via finite-difference of gradient
# ============================================================

def hessian_vec_product(Q, v, eps=1e-5, beta=1.0, N=2):
    """Compute H @ v where H is the Hessian, via finite-diff of gradients."""
    # Perturb Q along v
    Q_plus = list(Q); Q_minus = list(Q)
    for e in range(num_edges):
        ve = v[3*e:3*e+3]
        if np.linalg.norm(ve) < 1e-15: continue
        A = np.zeros((2,2), dtype=complex)
        for a in range(3):
            A += 1j * ve[a] * SIGMA[a] / 2.0
        Q_plus[e] = expm(eps * A) @ Q[e]
        Q_minus[e] = expm(-eps * A) @ Q[e]

    g_plus = gradient_S(Q_plus, eps=1e-6, beta=beta, N=N)
    g_minus = gradient_S(Q_minus, eps=1e-6, beta=beta, N=N)

    return (g_plus - g_minus) / (2 * eps)

# ============================================================
# Build full Hessian at Q = iσ₃ by column-by-column Hessian-vec products
# ============================================================

Q_s3 = [1j * SIGMA[2] for _ in range(num_edges)]
beta = 1.0; N = 2

print("=" * 70)
print("Full Hessian computation at Q = iσ₃")
print("=" * 70)

# Method: Use d²S/dε_i dε_j formula directly
# H_{ij} = [S(+i,+j) - S(+i,-j) - S(-i,+j) + S(-i,-j)] / (4 eps^2)
# This requires DIM² evaluations of S, too many.

# Alternative: compute column by column using gradient finite difference
# H[:,j] = [grad_S(Q + eps*e_j) - grad_S(Q - eps*e_j)] / (2*eps)
# Each gradient requires 2*DIM action evaluations.
# Total: DIM columns × 2*DIM per gradient × 2 perturbations = 4*DIM² ≈ 150K
# Each action evaluation is fast (~0.1ms), total ~15s. Feasible!

# But actually, we can use the symmetry of Q=iσ₃ to speed things up.
# The configuration has translational symmetry AND the action of the lattice symmetry group.
# For now, let's just compute the Hessian column by column.

# Even faster: use the quadratic form approach.
# H_ij = (S(+i,+j) - S(+i,-j) - S(-i,+j) + S(-i,-j)) / (4 eps²)
# For S evaluations: each takes ~0.1ms, we need 4*DIM² = 4*192² ≈ 150K evals → ~15s

# Let's use the mixed partial derivative approach

print("Computing full 192x192 Hessian by finite differences...")
print("(Using mixed partial derivatives)")
t0 = time.time()

eps = 1e-4
Hess = np.zeros((DIM, DIM))
S0 = wilson_action(Q_s3, beta, N)

# Precompute all single-perturbation configs
Q_plus_single = []
Q_minus_single = []
S_plus = np.zeros(DIM)
S_minus = np.zeros(DIM)

for i in range(DIM):
    e = i // 3
    a = i % 3
    d_vec = np.zeros(3); d_vec[a] = 1.0
    A = np.zeros((2,2), dtype=complex)
    for b in range(3):
        A += 1j * d_vec[b] * SIGMA[b] / 2.0

    Qp = list(Q_s3); Qm = list(Q_s3)
    Qp[e] = expm(eps * A) @ Q_s3[e]
    Qm[e] = expm(-eps * A) @ Q_s3[e]
    Q_plus_single.append(Qp)
    Q_minus_single.append(Qm)
    S_plus[i] = wilson_action(Qp, beta, N)
    S_minus[i] = wilson_action(Qm, beta, N)

print(f"  Single perturbations computed: {time.time()-t0:.1f}s")

# Diagonal elements: H_ii = (S(+i) - 2*S0 + S(-i)) / eps²
for i in range(DIM):
    Hess[i,i] = (S_plus[i] - 2*S0 + S_minus[i]) / eps**2

# Off-diagonal elements: H_ij = (S(+i,+j) - S(+i,-j) - S(-i,+j) + S(-i,-j)) / (4*eps²)
# But computing S(+i, +j) requires perturbing BOTH coordinates i and j simultaneously
# For coordinates on DIFFERENT edges, this is straightforward
# For coordinates on the SAME edge, we need special handling

print("  Computing off-diagonal elements...")
count = 0
for i in range(DIM):
    ei = i // 3
    ai = i % 3
    for j in range(i+1, DIM):
        ej = j // 3
        aj = j % 3

        d_i = np.zeros(3); d_i[ai] = 1.0
        d_j = np.zeros(3); d_j[aj] = 1.0

        A_i = np.zeros((2,2), dtype=complex)
        A_j = np.zeros((2,2), dtype=complex)
        for b in range(3):
            A_i += 1j * d_i[b] * SIGMA[b] / 2.0
            A_j += 1j * d_j[b] * SIGMA[b] / 2.0

        if ei == ej:
            # Same edge: need to compose perturbations
            Qpp = list(Q_s3); Qpp[ei] = expm(eps*A_j) @ expm(eps*A_i) @ Q_s3[ei]
            Qpm = list(Q_s3); Qpm[ei] = expm(-eps*A_j) @ expm(eps*A_i) @ Q_s3[ei]
            Qmp = list(Q_s3); Qmp[ei] = expm(eps*A_j) @ expm(-eps*A_i) @ Q_s3[ei]
            Qmm = list(Q_s3); Qmm[ei] = expm(-eps*A_j) @ expm(-eps*A_i) @ Q_s3[ei]
        else:
            # Different edges
            Qpp = list(Q_s3); Qpp[ei] = expm(eps*A_i) @ Q_s3[ei]; Qpp[ej] = expm(eps*A_j) @ Q_s3[ej]
            Qpm = list(Q_s3); Qpm[ei] = expm(eps*A_i) @ Q_s3[ei]; Qpm[ej] = expm(-eps*A_j) @ Q_s3[ej]
            Qmp = list(Q_s3); Qmp[ei] = expm(-eps*A_i) @ Q_s3[ei]; Qmp[ej] = expm(eps*A_j) @ Q_s3[ej]
            Qmm = list(Q_s3); Qmm[ei] = expm(-eps*A_i) @ Q_s3[ei]; Qmm[ej] = expm(-eps*A_j) @ Q_s3[ej]

        Spp = wilson_action(Qpp, beta, N)
        Spm = wilson_action(Qpm, beta, N)
        Smp = wilson_action(Qmp, beta, N)
        Smm = wilson_action(Qmm, beta, N)

        Hess[i,j] = (Spp - Spm - Smp + Smm) / (4 * eps**2)
        Hess[j,i] = Hess[i,j]

        count += 1
        if count % 5000 == 0:
            print(f"    {count}/{DIM*(DIM-1)//2} off-diagonal elements ({time.time()-t0:.1f}s)")

elapsed = time.time() - t0
print(f"  Full Hessian computed in {elapsed:.1f}s")

# ============================================================
# Compare spectra
# ============================================================

print("\n" + "=" * 70)
print("Spectral comparison: Hessian vs (β/2N) M")
print("=" * 70)

M_s3 = build_M(Q_s3)
M_scaled = (beta / (2*N)) * M_s3

eigvals_H = np.sort(eigh(Hess, eigvals_only=True))[::-1]
eigvals_M = np.sort(eigh(M_scaled, eigvals_only=True))[::-1]

print(f"\n{'Rank':<6} {'Hessian':>12} {'(β/2N)M':>12} {'Diff':>12}")
print("-" * 45)
for i in range(min(25, DIM)):
    diff = eigvals_H[i] - eigvals_M[i]
    print(f"{i+1:<6} {eigvals_H[i]:>12.6f} {eigvals_M[i]:>12.6f} {diff:>12.6f}")

print(f"\n...")
# Show bottom eigenvalues too
for i in range(max(0, DIM-10), DIM):
    diff = eigvals_H[i] - eigvals_M[i]
    print(f"{i+1:<6} {eigvals_H[i]:>12.6f} {eigvals_M[i]:>12.6f} {diff:>12.6f}")

# Check symmetry and PSD
print(f"\nHessian symmetry error: {np.max(np.abs(Hess - Hess.T)):.2e}")
print(f"Hessian min eigenvalue: {eigvals_H[-1]:.8f}")
print(f"Hessian max eigenvalue: {eigvals_H[0]:.8f}")
print(f"(β/2N)M min eigenvalue: {eigvals_M[-1]:.8f}")
print(f"(β/2N)M max eigenvalue: {eigvals_M[0]:.8f}")

# Check how many zero eigenvalues in Hessian
zero_count_H = np.sum(np.abs(eigvals_H) < 1e-4)
zero_count_M = np.sum(np.abs(eigvals_M) < 1e-4)
print(f"\nZero eigenvalues (|λ| < 1e-4): Hessian = {zero_count_H}, (β/2N)M = {zero_count_M}")

# Key: does the Hessian have the λ=24/(2N/β) = 6 eigenvalue?
print(f"\nHessian eigenvalue near 6.0: {eigvals_H[0]:.8f} (expected if Hess = M_scaled)")
print(f"Hessian eigenvalue near 4.0: {eigvals_H[np.argmin(np.abs(eigvals_H - 4.0))]:.8f}")

# Non-zero Hessian eigenvalues
nz_H = eigvals_H[np.abs(eigvals_H) > 1e-4]
nz_M = eigvals_M[np.abs(eigvals_M) > 1e-4]
print(f"\nNon-zero eigenvalue count: Hessian = {len(nz_H)}, (β/2N)M = {len(nz_M)}")
if len(nz_H) > 0:
    print(f"Max non-zero Hessian eigenvalue: {nz_H[0]:.8f}")

print("\nDONE")
