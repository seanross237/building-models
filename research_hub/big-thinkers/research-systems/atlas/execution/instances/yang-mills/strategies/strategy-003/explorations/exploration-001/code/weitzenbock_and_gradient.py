"""
Two new analyses:

1. Explicit Weitzenböck curvature R(Q) = M(Q) - M(I): compute its spectrum,
   verify R(Q) ≼ 0 (all eigenvalues ≤ 0).

2. Gradient ascent on λ_max(M(Q)) w.r.t. Q to find the true global maximum.
   If gradient ascent from random initializations always converges to Q=I (or
   gauge-equivalent), this is strong evidence the bound holds globally.
"""

import numpy as np
import time

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
        self.n_plaq = d*(d-1)//2 * self.n_sites
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
    dim = 3 * lat.n_edges
    M = np.zeros((dim, dim))
    for (e1, e2, e3, e4) in lat.plaquettes():
        Q1 = Q[e1]; Q12 = Q1@Q[e2]; Q123inv = Q12@np.conj(Q[e3]).T
        U_plaq = Q123inv@np.conj(Q[e4]).T
        R1 = np.eye(3); R2 = ad_matrix(Q1, basis)
        R3 = -ad_matrix(Q123inv, basis); R4 = -ad_matrix(U_plaq, basis)
        for (ei, Ri) in [(e1,R1),(e2,R2),(e3,R3),(e4,R4)]:
            for (ej, Rj) in [(e1,R1),(e2,R2),(e3,R3),(e4,R4)]:
                M[3*ei:3*ei+3, 3*ej:3*ej+3] += Ri.T @ Rj
    return M

# ======================================================
# PART 1: Weitzenböck curvature R(Q) = M(Q) - M(I)
# ======================================================
print("=" * 70)
print("PART 1: Weitzenböck Curvature R(Q) = M(Q) - M(I)")
print("=" * 70)

L, d = 2, 4
lat = Lattice(L, d)
dim = 3 * lat.n_edges
bound = 4 * d

Q_id = np.zeros((lat.n_edges, 2, 2), dtype=complex)
for e in range(lat.n_edges): Q_id[e] = np.eye(2)
M_id = build_M(lat, Q_id)

np.random.seed(42)
configs = [
    ('Random Haar', lambda: np.array([random_su2() for _ in range(lat.n_edges)])),
    ('Near-I ε=0.1', lambda: np.array([su2_exp(0.1*np.random.randn(3)) for _ in range(lat.n_edges)])),
    ('Near-I ε=0.5', lambda: np.array([su2_exp(0.5*np.random.randn(3)) for _ in range(lat.n_edges)])),
]

for name, gen_Q in configs:
    Q = gen_Q()
    M_Q = build_M(lat, Q)
    R = M_Q - M_id  # Weitzenböck curvature correction

    R_eigs = np.linalg.eigvalsh(R)
    M_Q_eigs = np.linalg.eigvalsh(M_Q)

    print(f"\n{name}:")
    print(f"  R(Q) eigenvalues: min={R_eigs[0]:.6f}, max={R_eigs[-1]:.6f}")
    print(f"  R(Q) ≼ 0? {'YES' if R_eigs[-1] <= 1e-8 else 'NO (max=' + f'{R_eigs[-1]:.6f})'}")
    print(f"  M(Q) λ_max = {M_Q_eigs[-1]:.6f} (bound: {bound})")
    print(f"  Tr(R) = {np.trace(R):.6f} (should be 0: {abs(np.trace(R)) < 1e-6})")
    print(f"  ||R||_F = {np.linalg.norm(R, 'fro'):.4f}")

    # Count positive eigenvalues of R
    n_pos = np.sum(R_eigs > 1e-8)
    n_neg = np.sum(R_eigs < -1e-8)
    n_zero = dim - n_pos - n_neg
    print(f"  R eigenvalue counts: {n_pos} positive, {n_zero} zero, {n_neg} negative")

# ======================================================
# PART 2: Gradient Ascent on λ_max(M(Q))
# ======================================================
print("\n" + "=" * 70)
print("PART 2: Gradient Ascent on λ_max(M(Q))")
print("=" * 70)

def compute_lambda_max(Q, lat):
    M = build_M(lat, Q)
    return np.linalg.eigvalsh(M)[-1]

def gradient_ascent_lambda_max(Q_init, lat, n_steps=500, step_size=0.05):
    """
    Stochastic gradient ascent: perturb each link, keep if λ_max increases.
    """
    Q = Q_init.copy()
    lam = compute_lambda_max(Q, lat)
    history = [lam]

    for step in range(n_steps):
        # Pick a random edge and perturbation direction
        e = np.random.randint(lat.n_edges)
        delta = step_size * np.random.randn(3)

        Q_new = Q.copy()
        Q_new[e] = su2_exp(delta) @ Q[e]
        # Re-unitarize
        u, s, vh = np.linalg.svd(Q_new[e])
        Q_new[e] = u @ vh

        lam_new = compute_lambda_max(Q_new, lat)

        if lam_new > lam:
            Q = Q_new
            lam = lam_new

        history.append(lam)

    return Q, lam, history

print(f"\nL={L}, d={d}, bound={bound}")
print("Running gradient ascent from various starting points...\n")

results = []
for trial in range(10):
    np.random.seed(1000 + trial)

    # Start from random Haar
    Q_init = np.array([random_su2() for _ in range(lat.n_edges)])
    lam_init = compute_lambda_max(Q_init, lat)

    Q_final, lam_final, history = gradient_ascent_lambda_max(Q_init, lat, n_steps=500, step_size=0.1)

    # Also try refining with smaller step size
    Q_final2, lam_final2, history2 = gradient_ascent_lambda_max(Q_final, lat, n_steps=200, step_size=0.02)

    results.append(lam_final2)
    print(f"  Trial {trial}: init={lam_init:.4f} → ascent={lam_final:.6f} → refined={lam_final2:.6f}")

print(f"\n  Best λ_max found: {max(results):.8f}")
print(f"  Bound: {bound}")
print(f"  Gap: {bound - max(results):.6f}")

if max(results) > bound + 1e-6:
    print(f"  *** VIOLATION FOUND ***")
else:
    print(f"  No violation. Gradient ascent confirms bound holds.")

# ======================================================
# PART 3: Stronger gradient ascent — start from near-I
# ======================================================
print(f"\nStarting from near-identity (where λ_max is highest)...")

for trial in range(5):
    np.random.seed(2000 + trial)
    eps = 0.01 * (trial + 1)  # ε = 0.01, 0.02, 0.03, 0.04, 0.05
    Q_init = np.array([su2_exp(eps * np.random.randn(3)) for _ in range(lat.n_edges)])
    lam_init = compute_lambda_max(Q_init, lat)

    Q_final, lam_final, _ = gradient_ascent_lambda_max(Q_init, lat, n_steps=1000, step_size=0.02)
    Q_final2, lam_final2, _ = gradient_ascent_lambda_max(Q_final, lat, n_steps=500, step_size=0.005)

    print(f"  ε={eps:.2f}: init={lam_init:.6f} → final={lam_final2:.8f}, gap={bound-lam_final2:.6f}")

# ======================================================
# PART 4: Check the holonomy of the gradient-ascent maximizer
# ======================================================
print(f"\n=== Analyzing the gradient-ascent maximizer ===")

# Start from identity, try to ascend
Q_init = np.array([np.eye(2, dtype=complex) for _ in range(lat.n_edges)])
lam_init = compute_lambda_max(Q_init, lat)
print(f"Q=I: λ_max = {lam_init:.8f}")

# Perturb and ascend
np.random.seed(42)
Q_pert = np.array([su2_exp(0.001 * np.random.randn(3)) for _ in range(lat.n_edges)])
Q_final, lam_final, history = gradient_ascent_lambda_max(Q_pert, lat, n_steps=2000, step_size=0.01)

print(f"After 2000 steps of ascent from near-I: λ_max = {lam_final:.8f}")
print(f"Ascent found {'higher' if lam_final > lam_init + 1e-8 else 'equal or lower'} than Q=I")

# Check holonomy of final config
plaq_list = lat.plaquettes()
holonomy_norms = []
for (e1, e2, e3, e4) in plaq_list:
    U_plaq = Q_final[e1] @ Q_final[e2] @ np.conj(Q_final[e3]).T @ np.conj(Q_final[e4]).T
    hol_dist = np.linalg.norm(U_plaq - np.eye(2))
    holonomy_norms.append(hol_dist)

print(f"Holonomy distances from I: mean={np.mean(holonomy_norms):.6f}, max={np.max(holonomy_norms):.6f}")
print(f"(If near zero, the ascent returned to flat/gauge-trivial configuration)")
