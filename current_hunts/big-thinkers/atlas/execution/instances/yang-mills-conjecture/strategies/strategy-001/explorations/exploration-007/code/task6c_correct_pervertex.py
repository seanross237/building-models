"""
Task 6c: Correctly compute per-vertex F_x for different L using the ACTUAL B_sq formula.

The sign structure analysis in task6b had a formula error: it computed
c+Tr(P) incorrectly. This script verifies F_x <= 64 directly from the
actual lattice B_sq formula, with no sign simplification.

Also checks: on L=2, does the proof's simplified M_total formula match the
actual per-vertex computation?
"""

import numpy as np
from itertools import product as iprod

np.random.seed(62831)

d = 4

def random_so3():
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    w, x, y, z = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])

def build_lattice(L):
    NV = L**d
    def vi(coords):
        idx = 0
        for i in range(d): idx = idx*L + (coords[i] % L)
        return idx
    def ic(idx):
        c = []; v = idx
        for i in range(d): c.append(v%L); v //= L
        return tuple(reversed(c))

    verts = [ic(i) for i in range(NV)]
    eidx = {}; NE = NV*d
    for xi in range(NV):
        for mu in range(d):
            eidx[(xi, mu)] = xi*d + mu

    plaqs = []
    for xi in range(NV):
        x = verts[xi]
        for mu in range(d):
            for nu in range(mu+1, d):
                xm = list(x); xm[mu]=(xm[mu]+1)%L
                xn = list(x); xn[nu]=(xn[nu]+1)%L
                e1 = eidx[(xi, mu)]
                e2 = eidx[(vi(tuple(xm)), nu)]
                e3 = eidx[(vi(tuple(xn)), mu)]
                e4 = eidx[(xi, nu)]
                plaqs.append((e1,e2,e3,e4,xi,mu,nu))

    return verts, eidx, NV, NE, plaqs

def compute_vertex_F_matrix(Q, plaq_list, verts, L):
    """Compute the 3x3 matrix M_x such that F_x(n) = n^T M_x n."""
    M = np.zeros((3,3))
    for p in plaq_list:
        e1,e2,e3,e4,xi,mu,nu = p
        x = verts[xi]
        Q1,Q2,Q3,Q4 = Q[e1],Q[e2],Q[e3],Q[e4]

        # Staggered signs
        s1 = (-1)**(sum(x)+mu)
        xm = list(x); xm[mu]=(xm[mu]+1)%L
        s2 = (-1)**(sum(xm)+nu)
        xn = list(x); xn[nu]=(xn[nu]+1)%L
        s3 = (-1)**(sum(xn)+mu)
        s4 = (-1)**(sum(x)+nu)

        # B(n) = s1*n + s2*Q1*n + (-s3)*Q1Q2Q3^T*n + (-s4)*U*n
        # = [s1*I + s2*Q1 + (-s3)*Q1Q2Q3^T + (-s4)*U] * n = A_p * n
        U = Q1 @ Q2 @ Q3.T @ Q4.T
        A_p = s1*np.eye(3) + s2*Q1 + (-s3)*(Q1@Q2@Q3.T) + (-s4)*U
        M += A_p.T @ A_p

    return M

def compute_proof_M_total(R, D_dict):
    """Compute M_total using the PROOF's formula: A = a(I+R_mu D) + b(R_mu + R_mu D R_nu^T)."""
    PLANES = [(mu,nu) for mu in range(4) for nu in range(mu+1,4)]
    M = np.zeros((3,3))
    for mu,nu in PLANES:
        a = (-1)**mu
        b = (-1)**(nu+1)
        Dmn = D_dict[(mu,nu)]
        A = a*(np.eye(3) + R[mu]@Dmn) + b*(R[mu] + R[mu]@Dmn@R[nu].T)
        M += A.T @ A
    return M

# ============================================================
# Part A: Verify proof formula matches lattice computation for L=2
# ============================================================

print("=" * 70)
print("Part A: Proof formula vs lattice computation (L=2)")
print("=" * 70)

L = 2
verts, eidx, NV, NE, plaqs = build_lattice(L)

# Group plaquettes by base vertex
plaqs_by_vertex = {xi: [] for xi in range(NV)}
for p in plaqs:
    plaqs_by_vertex[p[4]].append(p)

max_err = 0
for trial in range(1000):
    Q = [random_so3() for _ in range(NE)]

    # Pick vertex 0 and extract R, D from the edge assignments
    xi = 0
    x = verts[xi]

    # Base rotations: R_mu = Q at edge (xi, mu)
    R = [Q[eidx[(xi, mu)]] for mu in range(4)]

    # Cross-link: D_{mu,nu} = Q2 * Q3^T for plaquette (mu,nu) at xi
    D_dict = {}
    for p in plaqs_by_vertex[xi]:
        e1,e2,e3,e4,_xi,mu,nu = p
        # D_{mu,nu} = Q_{e2} * Q_{e3}^T
        D_dict[(mu,nu)] = Q[e2] @ Q[e3].T

    # Compute M_total using proof formula
    M_proof = compute_proof_M_total(R, D_dict)

    # Compute M_x using actual lattice B_sq
    M_lattice = compute_vertex_F_matrix(Q, plaqs_by_vertex[xi], verts, L)

    err = np.max(np.abs(M_proof - M_lattice))
    max_err = max(max_err, err)

print(f"  Max |M_proof - M_lattice| over 1000 trials: {max_err:.2e}")
print(f"  Proof formula matches lattice: {max_err < 1e-10}")

# Check for ALL vertices
print("\n  Checking all vertices...")
max_err_all = 0
for trial in range(100):
    Q = [random_so3() for _ in range(NE)]
    for xi in range(NV):
        x = verts[xi]
        R = [Q[eidx[(xi, mu)]] for mu in range(4)]
        D_dict = {}
        for p in plaqs_by_vertex[xi]:
            e1,e2,e3,e4,_xi,mu,nu = p
            D_dict[(mu,nu)] = Q[e2] @ Q[e3].T
        M_proof = compute_proof_M_total(R, D_dict)
        M_lattice = compute_vertex_F_matrix(Q, plaqs_by_vertex[xi], verts, L)
        err = np.max(np.abs(M_proof - M_lattice))
        max_err_all = max(max_err_all, err)

print(f"  Max error over all vertices: {max_err_all:.2e}")
print(f"  Proof formula matches for ALL L=2 vertices: {max_err_all < 1e-10}")

# ============================================================
# Part B: Check if proof formula works for L=3
# ============================================================

print("\n" + "=" * 70)
print("Part B: Proof formula vs lattice (L=3)")
print("=" * 70)

L = 3
verts3, eidx3, NV3, NE3, plaqs3 = build_lattice(L)
plaqs3_by_vertex = {xi: [] for xi in range(NV3)}
for p in plaqs3:
    plaqs3_by_vertex[p[4]].append(p)

# Check vertex (0,0,0,0) — should match
max_err_v0 = 0
max_err_other = 0
worst_vertex = None

for trial in range(100):
    Q = [random_so3() for _ in range(NE3)]
    for xi in range(NV3):
        x = verts3[xi]
        R = [Q[eidx3[(xi, mu)]] for mu in range(4)]
        D_dict = {}
        for p in plaqs3_by_vertex[xi]:
            e1,e2,e3,e4,_xi,mu,nu = p
            D_dict[(mu,nu)] = Q[e2] @ Q[e3].T
        M_proof = compute_proof_M_total(R, D_dict)
        M_lattice = compute_vertex_F_matrix(Q, plaqs3_by_vertex[xi], verts3, L)
        err = np.max(np.abs(M_proof - M_lattice))

        if all(c < L-1 for c in x):
            max_err_v0 = max(max_err_v0, err)
        else:
            if err > max_err_other:
                max_err_other = err
                worst_vertex = x

print(f"  Vertices with all coords < {L-1}: max error = {max_err_v0:.2e}")
print(f"  Vertices with some coord = {L-1}: max error = {max_err_other:.2e}")
print(f"  Worst vertex: {worst_vertex}")
print(f"  Proof formula matches for L=3: {max_err_other < 1e-10}")

if max_err_other > 1e-10:
    print(f"\n  *** PROOF FORMULA DOES NOT MATCH LATTICE FOR L=3! ***")
    print(f"  *** The proof's M_total = a(I+RD)+b(R+RDR^T) is L=2-specific. ***")
    print(f"  *** For L=3 vertices with coord = {L-1}, a different formula applies. ***")

# ============================================================
# Part C: Direct per-vertex bound check on actual lattice (L=3)
# ============================================================

print("\n" + "=" * 70)
print("Part C: Per-vertex lambda_max bound (actual lattice, L=3)")
print("=" * 70)

max_lam_by_type = {}
for trial in range(500):
    Q = [random_so3() for _ in range(NE3)]
    for xi in range(NV3):
        x = verts3[xi]
        M_x = compute_vertex_F_matrix(Q, plaqs3_by_vertex[xi], verts3, L)
        lam = np.max(np.linalg.eigvalsh(M_x))

        # Classify vertex
        has_max_coord = any(c == L-1 for c in x)
        key = "boundary" if has_max_coord else "interior"
        if key not in max_lam_by_type:
            max_lam_by_type[key] = 0
        max_lam_by_type[key] = max(max_lam_by_type[key], lam)

for key, val in max_lam_by_type.items():
    print(f"  {key} vertices: max lambda = {val:.4f} (bound: 64)")

# ============================================================
# Part D: Check L=4 proof formula
# ============================================================

print("\n" + "=" * 70)
print("Part D: Proof formula vs lattice (L=4)")
print("=" * 70)

L = 4
verts4, eidx4, NV4, NE4, plaqs4 = build_lattice(L)
plaqs4_by_vertex = {xi: [] for xi in range(NV4)}
for p in plaqs4:
    plaqs4_by_vertex[p[4]].append(p)

max_err_L4 = 0
for trial in range(50):
    Q = [random_so3() for _ in range(NE4)]
    for xi in range(min(NV4, 32)):  # Check subset of vertices
        x = verts4[xi]
        R = [Q[eidx4[(xi, mu)]] for mu in range(4)]
        D_dict = {}
        for p in plaqs4_by_vertex[xi]:
            e1,e2,e3,e4,_xi,mu,nu = p
            D_dict[(mu,nu)] = Q[e2] @ Q[e3].T
        M_proof = compute_proof_M_total(R, D_dict)
        M_lattice = compute_vertex_F_matrix(Q, plaqs4_by_vertex[xi], verts4, L)
        err = np.max(np.abs(M_proof - M_lattice))
        max_err_L4 = max(max_err_L4, err)

print(f"  Max |M_proof - M_lattice| over L=4: {max_err_L4:.2e}")
print(f"  Proof formula matches for L=4: {max_err_L4 < 1e-10}")

print("\nDone.")
