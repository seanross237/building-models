"""
Task 7: Check the full logical chain from per-vertex bound to Conjecture 1.

Key questions:
1. Is the reduction from lambda_max(full M) to staggered mode valid?
2. At identity (the tight case), what is the eigenspace structure?
3. For near-identity Q, does the full matrix approach 16?
"""

import numpy as np
from itertools import product

np.random.seed(11111)

d = 4; L = 2
NV = L**d; NE = NV*d; NDIM = NE*3

def vi(coords, L=2):
    idx = 0
    for i in range(d): idx = idx*L + (coords[i]%L)
    return idx

def ic(idx, L=2):
    c = []; v = idx
    for i in range(d): c.append(v%L); v //= L
    return tuple(reversed(c))

verts = [ic(i) for i in range(NV)]
eidx = {}
for xi in range(NV):
    for mu in range(d):
        eidx[(xi,mu)] = xi*d + mu

plaqs = []
for xi in range(NV):
    x = verts[xi]
    for mu in range(d):
        for nu in range(mu+1,d):
            xm = list(x); xm[mu]=(xm[mu]+1)%L
            xn = list(x); xn[nu]=(xn[nu]+1)%L
            plaqs.append((eidx[(xi,mu)], eidx[(vi(tuple(xm)),nu)],
                         eidx[(vi(tuple(xn)),mu)], eidx[(xi,nu)],
                         xi, mu, nu))

def random_so3():
    q = np.random.randn(4); q /= np.linalg.norm(q)
    w,x,y,z = q
    return np.array([[1-2*(y*y+z*z),2*(x*y-w*z),2*(x*z+w*y)],
                     [2*(x*y+w*z),1-2*(x*x+z*z),2*(y*z-w*x)],
                     [2*(x*z-w*y),2*(y*z+w*x),1-2*(x*x+y*y)]])

def so3_exp(omega):
    angle = np.linalg.norm(omega)
    if angle < 1e-14: return np.eye(3)
    ax = omega/angle
    K = np.array([[0,-ax[2],ax[1]],[ax[2],0,-ax[0]],[-ax[1],ax[0],0]])
    return np.eye(3) + np.sin(angle)*K + (1-np.cos(angle))*(K@K)

def build_full_M(Q):
    M = np.zeros((NDIM,NDIM))
    for p in plaqs:
        e1,e2,e3,e4,xi,mu,nu = p
        Q1,Q2,Q3,Q4 = Q[e1],Q[e2],Q[e3],Q[e4]
        U = Q1@Q2@Q3.T@Q4.T
        blocks = {e1:np.eye(3), e2:Q1.copy(), e3:-(Q1@Q2@Q3.T), e4:-U.copy()}
        edges = [e1,e2,e3,e4]
        for ei in edges:
            for ej in edges:
                M[3*ei:3*ei+3, 3*ej:3*ej+3] += blocks[ei].T @ blocks[ej]
    return M

def staggered_mode(n):
    v = np.zeros(NDIM)
    for xi in range(NV):
        x = verts[xi]
        for mu in range(d):
            e = eidx[(xi,mu)]
            sign = (-1)**(sum(x)+mu)
            v[3*e:3*e+3] = sign*n
    return v

# ============================================================
# Test 1: Eigenspace structure at identity
# ============================================================

print("=" * 70)
print("TEST 1: Full M(Q) eigenspace at identity (L=2)")
print("=" * 70)

Q_id = [np.eye(3)] * NE
M_id = build_full_M(Q_id)
eigs, vecs = np.linalg.eigh(M_id)

print("Eigenvalue spectrum:")
for ue in np.unique(np.round(eigs, 8)):
    mask = np.abs(eigs - ue) < 0.001
    mult = np.sum(mask)
    print(f"  lambda = {ue:8.4f}: multiplicity {mult}")

# Check: staggered subspace
S = np.zeros((NDIM, 3))
for i in range(3):
    e = np.zeros(3); e[i] = 1.0
    S[:,i] = staggered_mode(e)
S_orth, _ = np.linalg.qr(S)

# Project each eigenvalue-16 eigenvector onto staggered subspace
top_mask = eigs > 15.5
top_vecs = vecs[:, top_mask]
print(f"\nTop eigenspace (lambda=16): dimension {top_vecs.shape[1]}")

# Compute overlap matrix
overlap = S_orth.T @ top_vecs
sing_vals = np.linalg.svd(overlap, compute_uv=False)
print(f"  Singular values of overlap: {sing_vals}")
print(f"  (3 values of 1.0 means staggered subspace is contained in top eigenspace)")

# ============================================================
# Test 2: Near-identity perturbation — gradient analysis
# ============================================================

print("\n" + "=" * 70)
print("TEST 2: Near-identity behavior")
print("=" * 70)

# At Q=I, lambda_max=16 with multiplicity 9 (3 from staggered + 6 others).
# As Q moves away from I, does lambda_max stay at 16 or decrease?
# The conjecture says <= 16, so it should decrease (or stay at 16).

# Perturb: Q_e = exp(epsilon * omega_e) for small epsilon
for epsilon in [0.001, 0.01, 0.1, 0.5, 1.0]:
    max_lam = 0
    max_stag = 0
    for trial in range(50):
        omegas = [np.random.randn(3) for _ in range(NE)]
        Q = [so3_exp(epsilon * om) for om in omegas]
        M = build_full_M(Q)
        eigs_pert = np.linalg.eigvalsh(M)
        lam_max = eigs_pert[-1]
        max_lam = max(max_lam, lam_max)

        # Staggered quotient
        n = np.random.randn(3); n /= np.linalg.norm(n)
        v = staggered_mode(n)
        sq = v @ M @ v / np.dot(v, v)
        max_stag = max(max_stag, sq)

    print(f"  epsilon={epsilon:.3f}: max lambda_full={max_lam:.6f}, max stag={max_stag:.6f}")

# ============================================================
# Test 3: Does the staggered mode ever give a HIGHER Rayleigh
#          quotient than the full matrix maximum?
# ============================================================

print("\n" + "=" * 70)
print("TEST 3: Staggered vs full matrix maximum")
print("=" * 70)

stag_exceeds = 0
for trial in range(500):
    Q = [random_so3() for _ in range(NE)]
    M = build_full_M(Q)
    lam_full = np.linalg.eigvalsh(M)[-1]

    # Staggered maximum = max eigenvalue of 3x3 restriction
    M_stag = S_orth.T @ M @ S_orth  # 3x3
    lam_stag = np.linalg.eigvalsh(M_stag)[-1]

    if lam_stag > lam_full + 1e-10:
        stag_exceeds += 1
        print(f"  ANOMALY: stag={lam_stag:.6f} > full={lam_full:.6f}")

print(f"\n  Cases where staggered exceeds full: {stag_exceeds} / 500")
print(f"  (Should always be 0 since staggered is a subspace of full)")

# ============================================================
# Test 4: What is the nature of the OTHER 6 modes at eigenvalue 16?
# ============================================================

print("\n" + "=" * 70)
print("TEST 4: Characterize the full eigenvalue-16 subspace at identity")
print("=" * 70)

top_space = vecs[:, eigs > 15.5]  # 9-dimensional
print(f"  Eigenspace dimension: {top_space.shape[1]}")

# Project onto staggered subspace and its complement
proj_stag = S_orth @ S_orth.T @ top_space  # projection onto staggered
proj_comp = top_space - proj_stag  # complement

# Check: are the complement modes "constant modes" v_e = const for each direction?
# On L=2, constant modes have v_{(x,mu)} = c_mu for all x (same in each direction)
C = np.zeros((NDIM, 12))  # 4 directions * 3 components
for mu in range(4):
    for i in range(3):
        col = mu*3 + i
        for xi in range(NV):
            e = eidx[(xi, mu)]
            C[3*e+i, col] = 1.0 / np.sqrt(NV)

C_orth, _ = np.linalg.qr(C)
overlap_const = np.linalg.svd(C_orth.T @ top_space, compute_uv=False)
print(f"\n  Singular values of overlap with constant modes: {np.round(overlap_const, 4)}")

# Check "alternating" modes: v_{(x,mu)} = (-1)^{x_nu} c_mu for various nu
# These are Fourier modes with momentum (0,...,pi,...,0)
print("\n  Checking Fourier modes at momentum pi:")
for nu_mom in range(d):
    F = np.zeros((NDIM, 12))
    for mu in range(4):
        for i in range(3):
            col = mu*3 + i
            for xi in range(NV):
                x = verts[xi]
                e = eidx[(xi, mu)]
                F[3*e+i, col] = (-1)**x[nu_mom] / np.sqrt(NV)
    F_orth, _ = np.linalg.qr(F)
    overlap_fourier = np.linalg.svd(F_orth.T @ top_space, compute_uv=False)
    n_overlap = np.sum(overlap_fourier > 0.5)
    print(f"    Momentum pi in direction {nu_mom}: {n_overlap} overlapping modes "
          f"(svals: {np.round(overlap_fourier[:5], 3)})")

# Also check the staggered mode specifically
stag_check = np.zeros((NDIM, 3))
for i in range(3):
    en = np.zeros(3); en[i] = 1.0
    for xi in range(NV):
        x = verts[xi]
        for mu in range(d):
            e = eidx[(xi, mu)]
            sign = (-1)**(sum(x)+mu)
            stag_check[3*e+i, i] += sign / np.sqrt(NE)

stag_orth, _ = np.linalg.qr(stag_check)
overlap_stag = np.linalg.svd(stag_orth.T @ top_space, compute_uv=False)
print(f"\n  Staggered mode overlap: {np.round(overlap_stag, 4)}")
print(f"  (3 values of 1.0 means staggered is fully contained)")

print("\nDone.")
