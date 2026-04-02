"""
CORRECT Hessian of the Wilson action for SU(2) lattice gauge theory.

KEY INSIGHT: The Hessian MATRIX H_{(e,a),(f,b)} = ∂²S/∂c_{e,a} ∂c_{f,b}
requires symmetrization of the second-order Taylor expansion.

For the self-terms (same edge, same slot in a plaquette):
  ∂²/∂c_a ∂c_b exp(Σ c_m iσ_m)|_0 = {iσ_a, iσ_b}/2 = -δ_{ab} I

NOT the product (iσ_a)(iσ_b), which is the coefficient in the quadratic form
d²/dε² but not the mixed partial.

This simplifies the self-term to:
  H_self[(e,a),(e,b)] = -(β/N) × (-δ_{ab}) × Σ_{□∋e} Re Tr(U_□)
                       = (β/N) δ_{ab} Σ_{□∋e} Re Tr(U_□)

The self-term diagonal blocks are PROPORTIONAL TO IDENTITY in color space,
with coefficient (β/N) × Σ_{□∋e} Re Tr(U_□).

For the cross-terms (different edges from different slots in a plaquette):
  H[(ep,a),(eq,b)] = -(β/N) s_p s_q Re Tr(L_p (iσ_a) mid_{pq} (iσ_b) R_q)
  (already the correct mixed partial — no symmetrization needed)
"""

import numpy as np
from itertools import product as iterprod
np.set_printoptions(precision=8, linewidth=140)

sigma = np.array([
    [[0, 1], [1, 0]],
    [[0, -1j], [1j, 0]],
    [[1, 0], [0, -1]],
], dtype=complex)
I2 = np.eye(2, dtype=complex)

def expm_su2(v):
    det_v = v[0,0]*v[1,1] - v[0,1]*v[1,0]
    theta = np.sqrt(np.abs((-det_v).real))
    if theta < 1e-15:
        return I2 + v + 0.5 * v @ v
    return np.cos(theta) * I2 + (np.sin(theta) / theta) * v

def random_su2():
    v = np.random.randn(4)
    v /= np.linalg.norm(v)
    return v[0]*I2 + 1j*(v[1]*sigma[0] + v[2]*sigma[1] + v[3]*sigma[2])

basis = [1j * sigma[a] for a in range(3)]

class Lattice:
    def __init__(self, L, d):
        self.L = L; self.d = d
        self.sites = list(iterprod(*[range(L)]*d))
        self.n_sites = L**d; self.n_edges = self.n_sites * d
        self.plaquettes = []
        for x in self.sites:
            for mu in range(d):
                for nu in range(mu+1, d):
                    x_mu = list(x); x_mu[mu] = (x_mu[mu]+1)%L; x_mu = tuple(x_mu)
                    x_nu = list(x); x_nu[nu] = (x_nu[nu]+1)%L; x_nu = tuple(x_nu)
                    e1 = (sum(x[i]*L**(d-1-i) for i in range(d)))*d + mu
                    e2 = (sum(x_mu[i]*L**(d-1-i) for i in range(d)))*d + nu
                    e3 = (sum(x_nu[i]*L**(d-1-i) for i in range(d)))*d + mu
                    e4 = (sum(x[i]*L**(d-1-i) for i in range(d)))*d + nu
                    self.plaquettes.append((e1, e2, e3, e4))

    def wilson_action(self, Q, beta=1.0, N=2):
        S = 0.0
        for (e1,e2,e3,e4) in self.plaquettes:
            U = Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T
            S += -(beta/N) * np.trace(U).real
        return S

def hessian_correct(lat, Q, beta=1.0, N=2):
    """
    Correct Hessian matrix of the Wilson action.

    Self-terms: H[(e,a),(e,b)] = (β/N) δ_{ab} Σ_{□∋e} Re Tr(U_□)
    Cross-terms: H[(ep,a),(eq,b)] = -(β/N) sp sq Re Tr(Lp iσa mid iσb Rq)
    """
    n = 3 * lat.n_edges
    H = np.zeros((n, n))

    for (e1_idx, e2_idx, e3_idx, e4_idx) in lat.plaquettes:
        Q1, Q2, Q3, Q4 = Q[e1_idx], Q[e2_idx], Q[e3_idx], Q[e4_idx]
        Q3i = Q3.conj().T
        Q4i = Q4.conj().T
        U = Q1 @ Q2 @ Q3i @ Q4i
        reTrU = np.trace(U).real

        # Self-terms: (β/N) δ_{ab} Re Tr(U_□) for each edge in this plaquette
        edges = [e1_idx, e2_idx, e3_idx, e4_idx]
        for e in edges:
            for a in range(3):
                H[3*e + a, 3*e + a] += (beta/N) * reTrU

        # Cross-terms: need the slot structure
        Ls = [Q1, Q1 @ Q2, Q1 @ Q2, Q1 @ Q2 @ Q3i]
        Rs = [Q2 @ Q3i @ Q4i, Q3i @ Q4i, Q3i @ Q4i, Q4i]
        sn = [+1, +1, -1, -1]
        es = [e1_idx, e2_idx, e3_idx, e4_idx]
        mids = {(0,1): Q2, (0,2): Q2, (0,3): Q2 @ Q3i,
                (1,2): I2, (1,3): Q3i, (2,3): Q3i}

        for (p, q), middle in mids.items():
            sp, sq = sn[p], sn[q]
            ep, eq_idx = es[p], es[q]
            for a in range(3):
                for b in range(3):
                    val = -(beta/N) * sp * sq * (np.trace(Ls[p] @ basis[a] @ middle @ basis[b] @ Rs[q])).real
                    H[3*ep + a, 3*eq_idx + b] += val
                    H[3*eq_idx + b, 3*ep + a] += val

    return H

def hessian_fd(lat, Q, beta=1.0, N=2, eps=1e-5):
    """Hessian by central finite differences with correct same-edge handling."""
    n = 3 * lat.n_edges
    H = np.zeros((n, n))
    for i in range(n):
        ei, ai = i // 3, i % 3
        for j in range(i, n):
            ej, aj = j // 3, j % 3
            vals = []
            for si in [+1, -1]:
                for sj in [+1, -1]:
                    Qp = [q.copy() for q in Q]
                    if ei == ej:
                        Qp[ei] = Q[ei] @ expm_su2(si*eps*basis[ai] + sj*eps*basis[aj])
                    else:
                        Qp[ei] = Q[ei] @ expm_su2(si*eps*basis[ai])
                        Qp[ej] = Q[ej] @ expm_su2(sj*eps*basis[aj])
                    vals.append(lat.wilson_action(Qp, beta, N))
            H[i, j] = (vals[0] - vals[1] - vals[2] + vals[3]) / (4*eps**2)
            H[j, i] = H[i, j]
    return H

# ============================================================
# CROSS-CHECK
# ============================================================
lat = Lattice(2, 2)
n = 3 * lat.n_edges
print(f"Lattice: 2^2, {lat.n_edges} edges, matrix {n}×{n}")
print(f"\n{'Config':>8} | {'max|diff|':>10} | {'max rel err':>12} | {'symm err':>10} | {'eig_an':>12} | {'eig_fd':>12}")
print("-"*80)

np.random.seed(12345)
all_max_rel = 0

configs = [
    ("Q=I", [I2.copy() for _ in range(lat.n_edges)]),
    ("Q=iσ₃", [1j*sigma[2] for _ in range(lat.n_edges)]),
]
for trial in range(10):
    configs.append((f"Rand {trial}", [random_su2() for _ in range(lat.n_edges)]))

for name, Q in configs:
    H_an = hessian_correct(lat, Q)
    H_fd = hessian_fd(lat, Q)

    diff = np.abs(H_an - H_fd).max()
    denom = max(np.abs(H_an).max(), np.abs(H_fd).max(), 1e-15)
    rel = diff / denom
    symm = np.abs(H_an - H_an.T).max()
    emax_an = np.linalg.eigvalsh(H_an).max()
    emax_fd = np.linalg.eigvalsh(H_fd).max()

    all_max_rel = max(all_max_rel, rel)
    print(f"{name:>8} | {diff:10.2e} | {rel:12.2e} | {symm:10.2e} | {emax_an:12.6f} | {emax_fd:12.6f}")

print(f"\nOverall max relative error: {all_max_rel:.2e}")
print(f"Criterion: < 10⁻⁴ => {'PASS' if all_max_rel < 1e-4 else 'FAIL'}")

# ============================================================
# Now test on larger lattice and check eigenvalue bound
# ============================================================
print("\n" + "="*70)
print("EIGENVALUE BOUND CHECK (d=2,3,4)")
print("="*70)

for d in [2, 3, 4]:
    lat_d = Lattice(2, d)
    print(f"\nd={d}: {lat_d.n_edges} edges, {len(lat_d.plaquettes)} plaquettes")

    # Flat connection
    Q_flat = [I2.copy() for _ in range(lat_d.n_edges)]
    H_flat = hessian_correct(lat_d, Q_flat)
    emax_flat = np.linalg.eigvalsh(H_flat).max()
    print(f"  Q=I: max eigenvalue = {emax_flat:.4f}")

    # iσ₃ connection
    Q_is3 = [1j*sigma[2] for _ in range(lat_d.n_edges)]
    H_is3 = hessian_correct(lat_d, Q_is3)
    emax_is3 = np.linalg.eigvalsh(H_is3).max()
    print(f"  Q=iσ₃: max eigenvalue = {emax_is3:.4f}")

    # Random configs
    np.random.seed(42)
    max_rand = 0
    for trial in range(30):
        Q_r = [random_su2() for _ in range(lat_d.n_edges)]
        H_r = hessian_correct(lat_d, Q_r)
        em = np.linalg.eigvalsh(H_r).max()
        max_rand = max(max_rand, em)
    print(f"  Random (30 configs): max eigenvalue = {max_rand:.4f}")
    print(f"  Flat exceeds random: {emax_flat > max_rand + 1e-8}")
