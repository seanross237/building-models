"""
Scan for the maximum eigenvalue of HessS over many configurations.
Check whether flat connections (U=I) maximize it.

Also check whether HessS is bounded by (β/N) × d(d-1)/2 × 4 or similar.
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

def random_su2():
    v = np.random.randn(4)
    v /= np.linalg.norm(v)
    return v[0]*I2 + 1j*(v[1]*sigma[0] + v[2]*sigma[1] + v[3]*sigma[2])

def random_su2_near(Q, spread=0.1):
    """Random SU(2) near Q."""
    v = spread * np.random.randn(3)
    w = sum(c * 1j * sigma[a] for a, c in enumerate(v))
    det_w = w[0,0]*w[1,1] - w[0,1]*w[1,0]
    theta = np.sqrt(np.abs((-det_w).real))
    if theta < 1e-15:
        exp_w = I2 + w + 0.5 * w @ w
    else:
        exp_w = np.cos(theta) * I2 + (np.sin(theta) / theta) * w
    return Q @ exp_w

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

# ============================================================
# Scan configurations on 2^2 lattice (d=2, fast)
# ============================================================
print("="*70)
print("SCAN FOR MAX EIGENVALUE OF HessS")
print("="*70)

for d in [2, 3, 4]:
    L = 2
    lat = Lattice(L, d)
    n_plaq = len(lat.plaquettes)
    print(f"\n--- d={d}, L={L}, edges={lat.n_edges}, plaquettes={n_plaq} ---")

    # Known flat connections
    flat_configs = {
        'Q=I': [I2.copy() for _ in range(lat.n_edges)],
        'Q=iσ₃': [1j*sigma[2] for _ in range(lat.n_edges)],
        'Q=iσ₁': [1j*sigma[0] for _ in range(lat.n_edges)],
    }

    results = []
    for name, Q in flat_configs.items():
        H = hessian_analytical(lat, Q)
        emax = np.linalg.eigvalsh(H).max()
        results.append((emax, name))

    # Random configs
    np.random.seed(42)
    for trial in range(50):
        Q = [random_su2() for _ in range(lat.n_edges)]
        H = hessian_analytical(lat, Q)
        emax = np.linalg.eigvalsh(H).max()
        results.append((emax, f'Random {trial}'))

    # Near-flat configs
    for trial in range(20):
        Q = [random_su2_near(I2, spread=0.3) for _ in range(lat.n_edges)]
        H = hessian_analytical(lat, Q)
        emax = np.linalg.eigvalsh(H).max()
        results.append((emax, f'Near-I {trial}'))

    # Near iσ₃
    for trial in range(20):
        Q = [random_su2_near(1j*sigma[2], spread=0.3) for _ in range(lat.n_edges)]
        H = hessian_analytical(lat, Q)
        emax = np.linalg.eigvalsh(H).max()
        results.append((emax, f'Near-iσ₃ {trial}'))

    results.sort(key=lambda x: -x[0])
    print(f"  Top 5 max eigenvalues:")
    for emax, name in results[:5]:
        print(f"    {emax:.6f}  ({name})")
    print(f"  Flat connection eigenvalue: {results[0][0] if 'Q=I' in results[0][1] else [r for r in results if 'Q=I' in r[1]][0][0]:.6f}")

    flat_val = [r[0] for r in results if 'Q=I' in r[1]][0]
    violations = [r for r in results if r[0] > flat_val + 1e-6]
    print(f"  Configs exceeding flat: {len(violations)}")
    if violations:
        for emax, name in violations[:3]:
            print(f"    {emax:.6f} ({name}) — exceeds flat by {emax - flat_val:.6f}")

# ============================================================
# Gradient ascent to find max eigenvalue config
# ============================================================
print("\n" + "="*70)
print("GRADIENT ASCENT ON MAX EIGENVALUE")
print("="*70)

L, d = 2, 4
lat = Lattice(L, d)

def max_eigval_and_vec(lat, Q, beta=1.0, N=2):
    H = hessian_analytical(lat, Q, beta, N)
    evals, evecs = np.linalg.eigh(H)
    idx = np.argmax(evals)
    return evals[idx], evecs[:, idx], H

def perturb_config_gradient(lat, Q, step=0.01, n_tries=5):
    """Try random perturbations and keep the one that increases max eigenvalue."""
    current_max, _, _ = max_eigval_and_vec(lat, Q)
    best_Q = Q
    best_max = current_max
    for _ in range(n_tries):
        Q_new = []
        for q in Q:
            v = step * np.random.randn(3)
            w = sum(c * 1j * sigma[a] for a, c in enumerate(v))
            det_w = w[0,0]*w[1,1] - w[0,1]*w[1,0]
            theta = np.sqrt(np.abs((-det_w).real))
            if theta < 1e-15:
                exp_w = I2 + w + 0.5 * w @ w
            else:
                exp_w = np.cos(theta) * I2 + (np.sin(theta) / theta) * w
            Q_new.append(q @ exp_w)
        new_max, _, _ = max_eigval_and_vec(lat, Q_new)
        if new_max > best_max:
            best_max = new_max
            best_Q = Q_new
    return best_Q, best_max

np.random.seed(77)
Q = [random_su2() for _ in range(lat.n_edges)]
current_max, _, _ = max_eigval_and_vec(lat, Q)
print(f"Initial max eigenvalue: {current_max:.6f}")

for iteration in range(200):
    Q, current_max = perturb_config_gradient(lat, Q, step=0.05, n_tries=10)
    if iteration % 20 == 0:
        print(f"  Iter {iteration:4d}: max eigenvalue = {current_max:.6f}")

print(f"Final max eigenvalue: {current_max:.6f}")

# Compare with flat connection
Q_flat = [I2.copy() for _ in range(lat.n_edges)]
flat_max, _, _ = max_eigval_and_vec(lat, Q_flat)
print(f"Flat connection max eigenvalue: {flat_max:.6f}")
print(f"Ratio (found/flat): {current_max / flat_max:.6f}")

# ============================================================
# Check: what is the theoretical bound?
# ============================================================
print("\n" + "="*70)
print("THEORETICAL BOUND ANALYSIS")
print("="*70)

# For one plaquette at Q=I, max eigenvalue of HessS is 4.0 (in our normalization)
# Each edge in d=4 on L=2 participates in 2(d-1) = 6 plaquettes.
# But on L=2 with periodic BC, the structure may differ.

# Let's check how many plaquettes each edge participates in
for d_test in [2, 3, 4]:
    lat_test = Lattice(2, d_test)
    edge_plaq_count = np.zeros(lat_test.n_edges, dtype=int)
    for (e1,e2,e3,e4) in lat_test.plaquettes:
        edge_plaq_count[e1] += 1
        edge_plaq_count[e2] += 1
        edge_plaq_count[e3] += 1
        edge_plaq_count[e4] += 1
    print(f"d={d_test}: edges in {edge_plaq_count[0]} plaquettes each (uniform: {len(set(edge_plaq_count))==1})")

# At Q=I, M(I) has max eigenvalue = 4 × (plaquettes_per_edge) × max_single_plaq_M_per_edge?
# Actually at Q=I, all Ad=I, B = v1+v2-v3-v4, and |B|² depends on the lattice structure.
# The max eigenvalue of the Laplacian-like M operator on the lattice...
# M acts like a discrete curl-curl operator. Its max eigenvalue on periodic L^d is
# related to the Fourier analysis of the curl operator.

# For now, just report what we find:
for d_test in [2, 3, 4]:
    lat_test = Lattice(2, d_test)
    Q_flat = [I2.copy() for _ in range(lat_test.n_edges)]
    H = hessian_analytical(lat_test, Q_flat)
    emax = np.linalg.eigvalsh(H).max()
    n_plaq_per_edge = 2*(d_test - 1)
    print(f"d={d_test}: max(HessS) at Q=I = {emax:.4f}, 4d = {4*d_test}, 2(d-1)×4 = {n_plaq_per_edge*4}, n_plaq/edge = {n_plaq_per_edge}")
