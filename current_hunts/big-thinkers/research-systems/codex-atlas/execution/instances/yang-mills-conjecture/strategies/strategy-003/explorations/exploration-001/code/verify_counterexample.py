"""
Verify the Q = iσ₃ counterexample analytically and numerically.
λ_max(M(Q)) = 24 at Q_e = iσ₃ for all edges on L=2, d=4 lattice.
"""

import numpy as np
from scipy.linalg import eigh, expm

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
# 1. Verify Q = iσ₃ properties
# ============================================================

print("=" * 70)
print("VERIFICATION OF Q = iσ₃ COUNTEREXAMPLE")
print("=" * 70)

Q_s3 = [1j * SIGMA[2] for _ in range(num_edges)]

print("\n1. Adjoint representation of iσ₃:")
Ad_s3 = adjoint_rep(1j * SIGMA[2])
print(f"   Ad_{{iσ₃}} = diag({Ad_s3[0,0]:.0f}, {Ad_s3[1,1]:.0f}, {Ad_s3[2,2]:.0f})")
print(f"   This is a 180° rotation around z-axis in color space.")

print("\n2. Plaquette holonomies:")
all_trivial = True
for i, plaq in enumerate(PLAQUETTES):
    U = compute_holonomy(Q_s3, plaq)
    if np.max(np.abs(U - np.eye(2))) > 1e-10:
        all_trivial = False
        print(f"   Plaq {i}: U = {U} (NOT identity!)")
if all_trivial:
    print(f"   All {len(PLAQUETTES)} plaquettes have U_□ = I (flat connection)")

print("\n3. Non-contractible holonomies (L=2 torus):")
for mu in range(d):
    # Holonomy = product of links along direction mu from site 0
    hol = np.eye(2, dtype=complex)
    x = 0
    for step in range(L):
        e = edge_index(x, mu)
        hol = hol @ Q_s3[e]
        x = neighbor(x, mu)
    print(f"   Direction {mu}: Hol = {np.array2string(hol, precision=2)}")
    # Check if Hol = -I
    if np.max(np.abs(hol - (-np.eye(2)))) < 1e-10:
        print(f"              = -I (Z₂ center element, topologically nontrivial)")

print("\n4. Partial holonomies in B-field (for any plaquette):")
Q_e = 1j * SIGMA[2]
H1 = np.eye(2, dtype=complex)
H2 = Q_e
H3 = Q_e @ Q_e  # = -I
H4 = Q_e @ Q_e @ su2_inv(Q_e)  # = -I × (-iσ₃) = iσ₃

print(f"   H₁ = I")
print(f"   H₂ = iσ₃ → Ad = diag(-1,-1,+1)")
print(f"   H₃ = (iσ₃)² = -I → Ad = diag(+1,+1,+1) = I")
print(f"   H₄ = -I × (-iσ₃) = iσ₃ → Ad = diag(-1,-1,+1)")

Ad_H = [adjoint_rep(H) for H in [H1, H2, H3, H4]]
for k, A in enumerate(Ad_H):
    print(f"   Ad_H{k+1} = diag({A[0,0]:.0f}, {A[1,1]:.0f}, {A[2,2]:.0f})")

print("\n5. B-field sign pattern per color:")
signs = [+1, +1, -1, -1]
for color in range(3):
    eff_signs = [signs[k] * Ad_H[k][color, color] for k in range(4)]
    print(f"   Color {color+1}: ({eff_signs[0]:+.0f}, {eff_signs[1]:+.0f}, {eff_signs[2]:+.0f}, {eff_signs[3]:+.0f})")

# ============================================================
# 2. Build M and compute spectrum
# ============================================================

print("\n6. M(Q) spectrum at Q = iσ₃:")
M_s3 = build_M(Q_s3)
eigvals = np.sort(eigh(M_s3, eigvals_only=True))[::-1]

print(f"   λ_max = {eigvals[0]:.10f}")
print(f"   Top 15 eigenvalues:")
for i in range(min(15, len(eigvals))):
    print(f"     λ_{i+1} = {eigvals[i]:.6f}")

# Count distinct eigenvalues
unique_eigs = []
for ev in eigvals:
    if not any(abs(ev - u) < 1e-4 for u in unique_eigs):
        unique_eigs.append(ev)
print(f"\n   Distinct eigenvalues: {[f'{e:.2f}' for e in sorted(unique_eigs, reverse=True)]}")
for ue in sorted(unique_eigs, reverse=True):
    mult = np.sum(np.abs(eigvals - ue) < 1e-4)
    print(f"     {ue:8.4f} with multiplicity {mult}")

# ============================================================
# 3. Construct the eigenvector explicitly
# ============================================================

print("\n7. Constructing the λ=24 eigenvector analytically:")
print("   Mode: v_{x,μ,color} = (-1)^{Σx_i} for transverse color (1 or 2), all μ")

v_24 = np.zeros(DIM)
for x in range(num_sites):
    coords = index_to_coords(x)
    stag_sign = (-1)**sum(coords)
    for mu in range(d):
        e = edge_index(x, mu)
        v_24[3*e + 0] = stag_sign  # color 1 (transverse)

v_24 /= np.linalg.norm(v_24)

rq = v_24 @ M_s3 @ v_24
print(f"   Rayleigh quotient v^T M v / |v|² = {rq:.10f}")
print(f"   Expected: 24.0")
print(f"   Match: {abs(rq - 24.0) < 1e-8}")

# ============================================================
# 4. Verify this is NOT a gauge mode at Q = iσ₃
# ============================================================

print("\n8. Gauge mode check:")
print("   Gauge modes at Q = iσ₃ have v_{x,μ} = λ_x - Ad_{Q_{x,μ}}(λ_{x+μ̂})")
print("   = λ_x - diag(-1,-1,+1) λ_{x+μ̂}")

# Build gauge mode subspace
gauge_vecs = []
for x in range(num_sites):
    for a in range(3):
        # Gauge parameter: λ_y = δ_{y,x} e_a
        v_gauge = np.zeros(DIM)
        for mu in range(d):
            e = edge_index(x, mu)
            v_gauge[3*e + a] = 1.0  # λ_x contribution

            # -Ad_{Q_{x,μ}}(λ_{x+μ̂}) contribution: only if x+μ̂ = x (not the case for distinct sites)
            # Actually, need to handle x+μ̂ = x case (only on L=2 if step wraps around)

        # Also: sites y where y + μ̂ = x (i.e., y = x - μ̂) contribute to v_{y,μ}
        for mu in range(d):
            y = neighbor(x, mu, -1)  # y + μ̂ = x
            e_y = edge_index(y, mu)
            # v_{y,μ} gets -Ad_{Q_{y,μ}}(λ_x) = -Ad_{iσ₃}(e_a) contribution
            for b in range(3):
                v_gauge[3*e_y + b] -= Ad_s3[b, a]

        if np.linalg.norm(v_gauge) > 1e-10:
            gauge_vecs.append(v_gauge / np.linalg.norm(v_gauge))

# Orthogonalize gauge vectors
from numpy.linalg import qr
if gauge_vecs:
    G = np.column_stack(gauge_vecs)
    Q_orth, R = qr(G, mode='reduced')
    # Remove near-zero columns
    norms = np.abs(np.diag(R))
    keep = norms > 1e-8
    Q_gauge = Q_orth[:, keep]
    print(f"   Gauge subspace dimension: {Q_gauge.shape[1]}")

    # Project v_24 onto gauge subspace
    proj = Q_gauge @ (Q_gauge.T @ v_24)
    gauge_overlap = np.linalg.norm(proj)
    print(f"   |projection of λ=24 mode onto gauge subspace| = {gauge_overlap:.10f}")
    print(f"   Is gauge mode? {'YES' if gauge_overlap > 0.9 else 'NO'}")
else:
    print("   No gauge modes found (unexpected)")

# ============================================================
# 5. Hessian verification at Q = iσ₃
# ============================================================

print("\n9. Hessian verification at Q = iσ₃ (flat connection):")
beta = 1.0; N = 2

# v^T H v by finite difference
v_test = v_24 * np.linalg.norm(v_24)  # already normalized, scale doesn't matter

eps = 1e-5
Q_plus = list(Q_s3); Q_minus = list(Q_s3)
for e in range(num_edges):
    ve = v_24[3*e:3*e+3]
    if np.linalg.norm(ve) < 1e-15: continue
    A = np.zeros((2,2), dtype=complex)
    for a in range(3):
        A += 1j * ve[a] * SIGMA[a] / 2.0
    Q_plus[e] = expm(eps * A) @ Q_s3[e]
    Q_minus[e] = expm(-eps * A) @ Q_s3[e]

S0 = wilson_action(Q_s3, beta, N)
Sp = wilson_action(Q_plus, beta, N)
Sm = wilson_action(Q_minus, beta, N)
d2S = (Sp - 2*S0 + Sm) / eps**2

vMv_scaled = (beta / (2*N)) * (v_24 @ M_s3 @ v_24)

print(f"   d²S/dε² (FD) = {d2S:.10f}")
print(f"   (β/2N) v^T M v = {vMv_scaled:.10f}")
print(f"   Ratio = {d2S / vMv_scaled:.10f}")
print(f"   At flat connection, these should match (ratio ≈ 1.0)")

# Also check a random tangent vector
v_rand = np.random.randn(DIM); v_rand /= np.linalg.norm(v_rand)

Q_plus2 = list(Q_s3); Q_minus2 = list(Q_s3)
for e in range(num_edges):
    ve = v_rand[3*e:3*e+3]
    A = np.zeros((2,2), dtype=complex)
    for a in range(3):
        A += 1j * ve[a] * SIGMA[a] / 2.0
    Q_plus2[e] = expm(eps * A) @ Q_s3[e]
    Q_minus2[e] = expm(-eps * A) @ Q_s3[e]

Sp2 = wilson_action(Q_plus2, beta, N)
Sm2 = wilson_action(Q_minus2, beta, N)
d2S2 = (Sp2 - 2*S0 + Sm2) / eps**2
vMv2 = (beta / (2*N)) * (v_rand @ M_s3 @ v_rand)
print(f"\n   Random v: d²S/dε² = {d2S2:.10f}, (β/2N)v^T Mv = {vMv2:.10f}, ratio = {d2S2/vMv2:.10f}")

# ============================================================
# 6. Other flat connections
# ============================================================

print("\n10. Survey of flat connections with center holonomies:")
# Configurations where Q_e picks up phases from center elements
# Q = exp(i π n · σ₃/(L)) gives holonomy along L links = exp(i π n σ₃)

configs = {
    'all I': np.eye(2, dtype=complex),
    'all -I': -np.eye(2, dtype=complex),
    'all iσ₃': 1j * SIGMA[2],
    'all iσ₁': 1j * SIGMA[0],
    'all iσ₂': 1j * SIGMA[1],
    'all -iσ₃': -1j * SIGMA[2],
}

for name, Q_e in configs.items():
    Q = [Q_e.copy() for _ in range(num_edges)]
    M = build_M(Q)
    lmax = np.max(eigh(M, eigvals_only=True))
    # Check flatness
    is_flat = all(np.max(np.abs(compute_holonomy(Q, p) - np.eye(2))) < 1e-10 for p in PLAQUETTES)
    print(f"   {name:15s}: λ_max = {lmax:8.4f}, flat = {is_flat}")

# General SU(2) element
print("\n   Random single-element configs (Q_e = same for all e):")
for trial in range(10):
    v = np.random.randn(4); v /= np.linalg.norm(v)
    Q_e = np.array([[v[0]+1j*v[1], v[2]+1j*v[3]], [-v[2]+1j*v[3], v[0]-1j*v[1]]])
    Q = [Q_e.copy() for _ in range(num_edges)]
    M = build_M(Q)
    lmax = np.max(eigh(M, eigvals_only=True))
    U = compute_holonomy(Q, PLAQUETTES[0])
    re_tr = np.real(np.trace(U))
    print(f"   trial {trial+1}: λ_max = {lmax:8.4f}, Re Tr(U_□) = {re_tr:6.3f}")

print("\nDONE")
