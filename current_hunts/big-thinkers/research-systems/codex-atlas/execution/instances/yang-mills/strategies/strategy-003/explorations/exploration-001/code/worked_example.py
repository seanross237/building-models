"""
Worked Example: single non-identity link Q_{0,0} = diag(i,-i) on L=2, d=4 lattice.

Compute B_□ explicitly for all plaquettes containing this link,
verify ∑_□ |B_□(Q,v)|² ≤ 4d|v|² = 16|v|².

Also verify with the staggered eigenvector (which maximizes at Q=I).
"""
import numpy as np

def adjoint_action(U, A):
    return U @ A @ np.conj(U).T

def su2_basis():
    s1 = np.array([[0,1],[1,0]], dtype=complex)
    s2 = np.array([[0,-1j],[1j,0]], dtype=complex)
    s3 = np.array([[1,0],[0,-1]], dtype=complex)
    return [1j*s1/2, 1j*s2/2, 1j*s3/2]

def su2_to_vec(A, basis):
    return np.array([-2*np.trace(b @ A).real for b in basis])

def ad_matrix(U, basis):
    dim_su = 3
    R = np.zeros((dim_su, dim_su))
    for j in range(dim_su):
        transformed = adjoint_action(U, basis[j])
        R[:, j] = su2_to_vec(transformed, basis)
    return R

basis = su2_basis()

# Q_{0,0} = diag(i, -i)
Q_special = np.array([[1j, 0], [0, -1j]])
print("=== Worked Example ===")
print(f"Q_special = diag(i, -i) = {Q_special}")
print(f"Det = {np.linalg.det(Q_special):.4f}")

# Ad_Q for this element:
R_special = ad_matrix(Q_special, basis)
print(f"\nAd_{{Q_special}} = ")
print(R_special)
print(f"This is a rotation by π about the σ₃ axis:")
print(f"  T₁ → -T₁, T₂ → -T₂, T₃ → T₃")

# Verify
for a in range(3):
    transformed = adjoint_action(Q_special, basis[a])
    coeffs = su2_to_vec(transformed, basis)
    print(f"  Ad(T_{a+1}) = {coeffs}")

# Setup: L=2, d=4 lattice
L, d = 2, 4

class Lattice:
    def __init__(self, L, d):
        self.L, self.d = L, d
        self.n_sites = L**d
        self.n_edges = d * self.n_sites

    def site_index(self, coords):
        idx = 0
        for i in range(self.d):
            idx = idx * self.L + (coords[i] % self.L)
        return idx

    def site_coords(self, idx):
        coords = []
        for i in range(self.d - 1, -1, -1):
            coords.append(idx % self.L)
            idx //= self.L
        return list(reversed(coords))

    def edge_index(self, site_idx, mu):
        return site_idx * self.d + mu

    def shifted_site(self, site_idx, mu, sign=+1):
        coords = self.site_coords(site_idx)
        coords[mu] = (coords[mu] + sign) % self.L
        return self.site_index(coords)

    def plaquettes(self):
        plaq_list = []
        for x in range(self.n_sites):
            for mu in range(self.d):
                for nu in range(mu+1, self.d):
                    x_mu = self.shifted_site(x, mu)
                    x_nu = self.shifted_site(x, nu)
                    e1 = self.edge_index(x, mu)
                    e2 = self.edge_index(x_mu, nu)
                    e3 = self.edge_index(x_nu, mu)
                    e4 = self.edge_index(x, nu)
                    plaq_list.append((e1, e2, e3, e4, x, mu, nu))
        return plaq_list

lat = Lattice(L, d)

# Edge 0 = site 0, direction 0 = (x=0000, μ=0)
e_special = 0
site_0 = 0
mu_0 = 0

# Setup Q: all identity except edge 0
Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
for e in range(lat.n_edges):
    Q[e] = np.eye(2)
Q[e_special] = Q_special

# Find plaquettes containing edge e_special
containing_plaq = []
all_plaq = lat.plaquettes()
for p_idx, (e1, e2, e3, e4, x, mu, nu) in enumerate(all_plaq):
    if e_special in [e1, e2, e3, e4]:
        containing_plaq.append((p_idx, e1, e2, e3, e4, x, mu, nu))

print(f"\n=== Plaquettes containing edge {e_special} ===")
print(f"Edge {e_special} = (site {site_0}, dir {mu_0})")
print(f"Number of containing plaquettes: {len(containing_plaq)} (expected: {2*(d-1)} = {2*(d-1)})")

for p_idx, e1, e2, e3, e4, x, mu, nu in containing_plaq:
    pos = 'e1' if e_special==e1 else ('e2' if e_special==e2 else ('e3' if e_special==e3 else 'e4'))
    xc = lat.site_coords(x)
    print(f"  Plaquette {p_idx}: site={xc}, plane=({mu},{nu}), edges=[{e1},{e2},{e3},{e4}], special at {pos}")

# Build M(Q) with corrected formula
dim_su = 3
dim = dim_su * lat.n_edges
M = np.zeros((dim, dim))

for (e1, e2, e3, e4, x, mu, nu) in all_plaq:
    Q1 = Q[e1]
    Q12 = Q1 @ Q[e2]
    Q123inv = Q12 @ np.conj(Q[e3]).T
    U_plaq = Q123inv @ np.conj(Q[e4]).T

    R1 = np.eye(dim_su)
    R2 = ad_matrix(Q1, basis)
    R3 = -ad_matrix(Q123inv, basis)
    R4 = -ad_matrix(U_plaq, basis)

    for (ei, Ri) in [(e1,R1),(e2,R2),(e3,R3),(e4,R4)]:
        for (ej, Rj) in [(e1,R1),(e2,R2),(e3,R3),(e4,R4)]:
            M[dim_su*ei:dim_su*ei+dim_su, dim_su*ej:dim_su*ej+dim_su] += Ri.T @ Rj

eigs = np.linalg.eigvalsh(M)
print(f"\n=== Eigenvalue analysis ===")
print(f"λ_max = {eigs[-1]:.10f} (bound: {4*d})")
print(f"Ratio: {eigs[-1]/(4*d):.10f}")
print(f"Top 5 eigenvalues: {eigs[-5:]}")

# Compare with Q=I
M_id = np.zeros((dim, dim))
for (e1, e2, e3, e4, x, mu, nu) in all_plaq:
    R1_id = np.eye(dim_su)
    R2_id = np.eye(dim_su)
    R3_id = -np.eye(dim_su)
    R4_id = -np.eye(dim_su)
    for (ei, Ri) in [(e1,R1_id),(e2,R2_id),(e3,R3_id),(e4,R4_id)]:
        for (ej, Rj) in [(e1,R1_id),(e2,R2_id),(e3,R3_id),(e4,R4_id)]:
            M_id[dim_su*ei:dim_su*ei+dim_su, dim_su*ej:dim_su*ej+dim_su] += Ri.T @ Rj

eigs_id = np.linalg.eigvalsh(M_id)
print(f"\nQ=I: λ_max = {eigs_id[-1]:.10f}")

# Staggered mode test
print(f"\n=== Staggered mode test ===")
v_stag = np.zeros(dim)
for x in range(lat.n_sites):
    coords = lat.site_coords(x)
    for mu_dir in range(d):
        e = lat.edge_index(x, mu_dir)
        sign = (-1)**(sum(coords) + mu_dir)
        v_stag[3*e] = sign  # T₁ direction

v_stag /= np.linalg.norm(v_stag)

vMv = v_stag @ M @ v_stag
vMv_id = v_stag @ M_id @ v_stag
print(f"v_stag^T M(Q_special) v_stag = {vMv:.10f}")
print(f"v_stag^T M(I) v_stag = {vMv_id:.10f}")
print(f"Ratio: {vMv/vMv_id:.10f}")

# Direct B_□ computation for the staggered mode
B_sum_sq = 0.0
B_sum_sq_id = 0.0
for (e1, e2, e3, e4, x, mu, nu) in all_plaq:
    # With Q_special
    Q1 = Q[e1]; Q12 = Q1@Q[e2]; Q123inv = Q12@np.conj(Q[e3]).T; U_plaq = Q123inv@np.conj(Q[e4]).T

    v1 = sum(v_stag[3*e1+a]*basis[a] for a in range(3))
    v2 = sum(v_stag[3*e2+a]*basis[a] for a in range(3))
    v3 = sum(v_stag[3*e3+a]*basis[a] for a in range(3))
    v4 = sum(v_stag[3*e4+a]*basis[a] for a in range(3))

    B = v1 + adjoint_action(Q1, v2) - adjoint_action(Q123inv, v3) - adjoint_action(U_plaq, v4)
    B_sq = -2*np.trace(B@B).real
    B_sum_sq += B_sq

    # With Q=I
    B_id = v1 + v2 - v3 - v4
    B_sq_id = -2*np.trace(B_id@B_id).real
    B_sum_sq_id += B_sq_id

print(f"\nDirect: ∑|B_□(Q_special)|² = {B_sum_sq:.10f}")
print(f"Direct: ∑|B_□(I)|²        = {B_sum_sq_id:.10f}")
print(f"Ratio: {B_sum_sq/B_sum_sq_id:.10f}")
print(f"Bound check: {B_sum_sq:.6f} ≤ {4*d:.1f} × |v|² = {4*d:.1f} : {'OK' if B_sum_sq <= 4*d + 1e-8 else 'VIOLATION'}")

# Detailed per-plaquette analysis for containing plaquettes
print(f"\n=== Per-plaquette B_□ analysis (affected plaquettes only) ===")
for p_idx, e1, e2, e3, e4, x, mu, nu in containing_plaq:
    Q1 = Q[e1]; Q12 = Q1@Q[e2]; Q123inv = Q12@np.conj(Q[e3]).T; U_plaq = Q123inv@np.conj(Q[e4]).T

    v1 = sum(v_stag[3*e1+a]*basis[a] for a in range(3))
    v2 = sum(v_stag[3*e2+a]*basis[a] for a in range(3))
    v3 = sum(v_stag[3*e3+a]*basis[a] for a in range(3))
    v4 = sum(v_stag[3*e4+a]*basis[a] for a in range(3))

    B = v1 + adjoint_action(Q1, v2) - adjoint_action(Q123inv, v3) - adjoint_action(U_plaq, v4)
    B_sq = -2*np.trace(B@B).real

    B_id = v1 + v2 - v3 - v4
    B_sq_id = -2*np.trace(B_id@B_id).real

    hol = -2*np.trace(U_plaq @ U_plaq).real  # should be 0 since U is unitary

    pos = 'e1' if e_special==e1 else ('e2' if e_special==e2 else ('e3' if e_special==e3 else 'e4'))
    xc = lat.site_coords(x)
    print(f"  Plaq {p_idx} ({mu},{nu}), special={pos}: |B|²={B_sq:.6f}, |B_id|²={B_sq_id:.6f}, ratio={B_sq/max(B_sq_id,1e-15):.4f}")

# Try to find the worst-case v (top eigenvector)
eig_vals, eig_vecs = np.linalg.eigh(M)
v_top = eig_vecs[:, -1]
vMv_top = v_top @ M @ v_top
print(f"\n=== Worst-case v (top eigenvector) ===")
print(f"λ_max = v_top^T M v_top = {vMv_top:.10f}")
print(f"Bound check: {vMv_top:.6f} ≤ {4*d:.1f} : {'OK' if vMv_top <= 4*d + 1e-8 else 'VIOLATION'}")
