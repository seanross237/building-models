"""
Stage 4 (fixed): Cross-check analytical Hessian against finite differences.

BUG FIX: When computing d²S/(dc_{e,a} dc_{e,b}) for the SAME edge e,
we must use Q_e exp(ε_a iσ_a + ε_b iσ_b) as a SINGLE exponential,
NOT Q_e exp(ε_a iσ_a) exp(ε_b iσ_b), because the latter differs
at O(ε²) due to the Baker-Campbell-Hausdorff formula.
"""

import numpy as np
from itertools import product as iterprod

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
        for (e1, e2, e3, e4) in self.plaquettes:
            U = Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T
            S += -(beta/N) * np.trace(U).real
        return S

def hessian_analytical(lat, Q, beta=1.0, N=2):
    n = 3 * lat.n_edges
    H = np.zeros((n,n))
    for (e1,e2,e3,e4) in lat.plaquettes:
        Q1,Q2,Q3,Q4 = Q[e1],Q[e2],Q[e3],Q[e4]
        Q3i = Q3.conj().T; Q4i = Q4.conj().T
        Ls = [Q1, Q1@Q2, Q1@Q2, Q1@Q2@Q3i]
        Rs = [Q2@Q3i@Q4i, Q3i@Q4i, Q3i@Q4i, Q4i]
        sn = [+1,+1,-1,-1]; es = [e1,e2,e3,e4]
        mids = {(0,1):Q2,(0,2):Q2,(0,3):Q2@Q3i,(1,2):I2,(1,3):Q3i,(2,3):Q3i}
        for p in range(4):
            for a in range(3):
                for b in range(3):
                    H[3*es[p]+a, 3*es[p]+b] += -(beta/N)*(np.trace(Ls[p]@basis[a]@basis[b]@Rs[p])).real
        for (p,q),middle in mids.items():
            for a in range(3):
                for b in range(3):
                    val = -(beta/N)*sn[p]*sn[q]*(np.trace(Ls[p]@basis[a]@middle@basis[b]@Rs[q])).real
                    H[3*es[p]+a, 3*es[q]+b] += val
                    H[3*es[q]+b, 3*es[p]+a] += val
    return H

def hessian_fd_full(lat, Q, beta=1.0, N=2, eps=1e-5):
    """Full Hessian by central finite differences.
    FIXED: uses single combined exponential for same-edge perturbations.
    """
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
                        # FIXED: combine into single exponential
                        Qp[ei] = Q[ei] @ expm_su2(si*eps*basis[ai] + sj*eps*basis[aj])
                    else:
                        Qp[ei] = Q[ei] @ expm_su2(si*eps*basis[ai])
                        Qp[ej] = Q[ej] @ expm_su2(sj*eps*basis[aj])
                    vals.append(lat.wilson_action(Qp, beta, N))
            H[i, j] = (vals[0] - vals[1] - vals[2] + vals[3]) / (4*eps**2)
            H[j, i] = H[i, j]
    return H

# Cross-check
lat = Lattice(2, 2)
n = 3 * lat.n_edges
print(f"Lattice: 2^2, {lat.n_edges} edges, matrix {n}×{n}")
print(f"\n{'Config':>8} | {'max|H_an|':>10} | {'max|H_fd|':>10} | {'max|diff|':>10} | {'max rel err':>12} | {'eig_an_max':>11} | {'eig_fd_max':>11}")
print("-"*90)

np.random.seed(12345)
all_max_rel_err = 0

configs = [
    ("Q=I", [I2.copy() for _ in range(lat.n_edges)]),
    ("Q=iσ₃", [1j*sigma[2] for _ in range(lat.n_edges)]),
]
for trial in range(10):
    configs.append((f"Rand {trial}", [random_su2() for _ in range(lat.n_edges)]))

for name, Q in configs:
    H_an = hessian_analytical(lat, Q)
    H_fd = hessian_fd_full(lat, Q)

    diff = np.abs(H_an - H_fd)
    max_diff = diff.max()
    max_H = max(np.abs(H_an).max(), np.abs(H_fd).max(), 1e-15)
    max_rel = max_diff / max_H

    eigs_an = np.linalg.eigvalsh(H_an)
    eigs_fd = np.linalg.eigvalsh(H_fd)

    all_max_rel_err = max(all_max_rel_err, max_rel)
    print(f"{name:>8} | {np.abs(H_an).max():10.4f} | {np.abs(H_fd).max():10.4f} | {max_diff:10.2e} | {max_rel:12.2e} | {eigs_an.max():11.6f} | {eigs_fd.max():11.6f}")

print(f"\nOverall max relative error: {all_max_rel_err:.2e}")
print(f"Criterion: < 10⁻⁴ => {'PASS' if all_max_rel_err < 1e-4 else 'FAIL'}")

# Also verify symmetry of analytical Hessian
print("\nSymmetry check:")
for name, Q in configs[:3]:
    H = hessian_analytical(lat, Q)
    asym = np.abs(H - H.T).max()
    print(f"  {name}: max|H - H^T| = {asym:.2e}")
