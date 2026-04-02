"""
Fixed gradient ascent: remove SVD re-unitarization that breaks SU(2) constraint.

The product of SU(2) matrices IS in SU(2), so no re-unitarization needed.
The SVD in the original code was projecting to U(2) (det could be -1),
which breaks the adjoint representation (SO(3) vs O(3)).
"""

import numpy as np

def random_su2():
    v = np.random.randn(4); v /= np.linalg.norm(v)
    a, b, c, d = v
    return np.array([[a+1j*b, c+1j*d], [-c+1j*d, a-1j*b]])

def su2_exp(A_vec):
    theta = np.linalg.norm(A_vec)
    if theta < 1e-15: return np.eye(2, dtype=complex)
    n = A_vec / theta
    ct, st = np.cos(theta/2), np.sin(theta/2)
    return np.array([[ct+1j*st*n[2], st*(1j*n[0]+n[1])],
                      [st*(1j*n[0]-n[1]), ct-1j*st*n[2]]])

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
    R = np.zeros((3, 3))
    for j in range(3):
        transformed = adjoint_action(U, basis[j])
        R[:, j] = su2_to_vec(transformed, basis)
    return R

basis = su2_basis()

class Lattice:
    def __init__(self, L, d):
        self.L, self.d = L, d
        self.n_sites = L**d
        self.n_edges = d * self.n_sites
    def site_index(self, coords):
        idx = 0
        for i in range(self.d): idx = idx * self.L + (coords[i] % self.L)
        return idx
    def site_coords(self, idx):
        coords = []
        for i in range(self.d-1, -1, -1): coords.append(idx % self.L); idx //= self.L
        return list(reversed(coords))
    def edge_index(self, site_idx, mu): return site_idx * self.d + mu
    def shifted_site(self, site_idx, mu, sign=+1):
        coords = self.site_coords(site_idx)
        coords[mu] = (coords[mu] + sign) % self.L
        return self.site_index(coords)
    def plaquettes(self):
        plaq_list = []
        for x in range(self.n_sites):
            for mu in range(self.d):
                for nu in range(mu+1, self.d):
                    x_mu = self.shifted_site(x, mu); x_nu = self.shifted_site(x, nu)
                    plaq_list.append((self.edge_index(x, mu), self.edge_index(x_mu, nu),
                                     self.edge_index(x_nu, mu), self.edge_index(x, nu)))
        return plaq_list

def build_M(lat, Q):
    dim = 3 * lat.n_edges; M = np.zeros((dim, dim))
    for (e1, e2, e3, e4) in lat.plaquettes():
        Q1 = Q[e1]; Q12 = Q1@Q[e2]; Q123inv = Q12@np.conj(Q[e3]).T
        U_plaq = Q123inv@np.conj(Q[e4]).T
        R1 = np.eye(3); R2 = ad_matrix(Q1, basis)
        R3 = -ad_matrix(Q123inv, basis); R4 = -ad_matrix(U_plaq, basis)
        for (ei, Ri) in [(e1,R1),(e2,R2),(e3,R3),(e4,R4)]:
            for (ej, Rj) in [(e1,R1),(e2,R2),(e3,R3),(e4,R4)]:
                M[3*ei:3*ei+3, 3*ej:3*ej+3] += Ri.T @ Rj
    return M

def compute_lambda_max(Q, lat):
    return np.linalg.eigvalsh(build_M(lat, Q))[-1]

L, d = 2, 4
lat = Lattice(L, d)
bound = 4 * d

# First: verify the bug
print("=== Bug verification: SVD breaks SU(2) ===")
Q_su2 = random_su2()
print(f"Original det: {np.linalg.det(Q_su2):.6f}")
delta = su2_exp(0.1 * np.random.randn(3))
print(f"Perturbation det: {np.linalg.det(delta):.6f}")
product = delta @ Q_su2
print(f"Product det (should be 1): {np.linalg.det(product):.6f}")
u, s, vh = np.linalg.svd(product)
svd_result = u @ vh
print(f"After SVD re-unitarize det: {np.linalg.det(svd_result):.6f}")
print(f"SVD BREAKS SU(2)? det={np.linalg.det(svd_result):.6f} ≠ 1")
print()

# Fixed gradient ascent: NO SVD re-unitarization
def gradient_ascent_fixed(Q_init, lat, n_steps=1000, step_size=0.05):
    Q = Q_init.copy()
    lam = compute_lambda_max(Q, lat)

    for step in range(n_steps):
        e = np.random.randint(lat.n_edges)
        delta = step_size * np.random.randn(3)
        Q_new = Q.copy()
        Q_new[e] = su2_exp(delta) @ Q[e]  # NO SVD — product is already SU(2)

        lam_new = compute_lambda_max(Q_new, lat)
        if lam_new > lam:
            Q = Q_new; lam = lam_new

    return Q, lam

print("=== Fixed Gradient Ascent (no SVD, proper SU(2)) ===")
print(f"L={L}, d={d}, bound={bound}\n")

# From random starts
print("From random Haar starts:")
for trial in range(10):
    np.random.seed(1000 + trial)
    Q_init = np.array([random_su2() for _ in range(lat.n_edges)])
    Q_f, lam_f = gradient_ascent_fixed(Q_init, lat, n_steps=500, step_size=0.1)
    Q_f2, lam_f2 = gradient_ascent_fixed(Q_f, lat, n_steps=500, step_size=0.02)
    print(f"  Trial {trial}: {compute_lambda_max(Q_init,lat):.4f} → {lam_f2:.8f}  "
          f"{'VIOLATION!' if lam_f2 > bound + 1e-6 else 'OK'}")

# From near-identity starts
print(f"\nFrom near-identity starts:")
for trial in range(8):
    np.random.seed(2000 + trial)
    eps = 0.01 * (trial + 1)
    Q_init = np.array([su2_exp(eps * np.random.randn(3)) for _ in range(lat.n_edges)])

    # Verify all links are SU(2)
    max_det_err = max(abs(np.linalg.det(Q_init[e]) - 1) for e in range(lat.n_edges))

    Q_f, lam_f = gradient_ascent_fixed(Q_init, lat, n_steps=1000, step_size=eps)
    Q_f2, lam_f2 = gradient_ascent_fixed(Q_f, lat, n_steps=500, step_size=eps/5)

    # Verify final config is SU(2)
    max_det_err_f = max(abs(np.linalg.det(Q_f2[e]) - 1) for e in range(lat.n_edges))

    print(f"  ε={eps:.2f}: init λ={compute_lambda_max(Q_init,lat):.6f} → final={lam_f2:.8f}, "
          f"det_err={max_det_err_f:.1e}  {'VIOLATION!' if lam_f2 > bound + 1e-6 else 'OK'}")

# From Q=I with small perturbation
print(f"\nFrom Q=I with aggressive ascent:")
np.random.seed(42)
Q_init = np.array([su2_exp(0.001 * np.random.randn(3)) for _ in range(lat.n_edges)])
Q_f, lam_f = gradient_ascent_fixed(Q_init, lat, n_steps=5000, step_size=0.01)
Q_f2, lam_f2 = gradient_ascent_fixed(Q_f, lat, n_steps=2000, step_size=0.002)
max_det_err = max(abs(np.linalg.det(Q_f2[e]) - 1) for e in range(lat.n_edges))
print(f"  5000+2000 steps: final λ_max = {lam_f2:.10f}, det_err = {max_det_err:.1e}")
print(f"  Exceeds bound? {'YES — VIOLATION' if lam_f2 > bound + 1e-8 else 'NO — bound holds'}")
