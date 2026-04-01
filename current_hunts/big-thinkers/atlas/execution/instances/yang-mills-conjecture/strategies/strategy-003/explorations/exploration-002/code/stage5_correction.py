"""
Stage 5: Structure of the correction C(Q) = M(Q) - (2N/β)HessS(Q)
using the CORRECT Hessian formula.
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

def hessian_correct(lat, Q, beta=1.0, N=2):
    n = 3 * lat.n_edges
    H = np.zeros((n, n))
    for (e1_idx, e2_idx, e3_idx, e4_idx) in lat.plaquettes:
        Q1, Q2, Q3, Q4 = Q[e1_idx], Q[e2_idx], Q[e3_idx], Q[e4_idx]
        Q3i = Q3.conj().T; Q4i = Q4.conj().T
        U = Q1 @ Q2 @ Q3i @ Q4i
        reTrU = np.trace(U).real
        for e in [e1_idx, e2_idx, e3_idx, e4_idx]:
            for a in range(3):
                H[3*e+a, 3*e+a] += (beta/N) * reTrU
        Ls = [Q1, Q1@Q2, Q1@Q2, Q1@Q2@Q3i]
        Rs = [Q2@Q3i@Q4i, Q3i@Q4i, Q3i@Q4i, Q4i]
        sn = [+1,+1,-1,-1]; es = [e1_idx, e2_idx, e3_idx, e4_idx]
        mids = {(0,1):Q2,(0,2):Q2,(0,3):Q2@Q3i,(1,2):I2,(1,3):Q3i,(2,3):Q3i}
        for (p,q),middle in mids.items():
            sp,sq = sn[p],sn[q]
            for a in range(3):
                for b in range(3):
                    val = -(beta/N)*sp*sq*(np.trace(Ls[p]@basis[a]@middle@basis[b]@Rs[q])).real
                    H[3*es[p]+a, 3*es[q]+b] += val
                    H[3*es[q]+b, 3*es[p]+a] += val
    return H

def build_M(lat, Q):
    n = 3 * lat.n_edges
    M = np.zeros((n, n))
    for (e1, e2, e3, e4) in lat.plaquettes:
        Q1, Q2, Q3, Q4 = Q[e1], Q[e2], Q[e3], Q[e4]
        Q3i = Q3.conj().T; Q4i = Q4.conj().T
        U = Q1 @ Q2 @ Q3i @ Q4i
        Ts = [I2, Q1.copy(), Q1 @ Q2 @ Q3i, U]
        sn = [+1, +1, -1, -1]; es = [e1, e2, e3, e4]
        for i_slot in range(4):
            for j_slot in range(4):
                si, sj = sn[i_slot], sn[j_slot]
                Ti, Tj = Ts[i_slot], Ts[j_slot]
                ei, ej = es[i_slot], es[j_slot]
                for a in range(3):
                    for b in range(3):
                        val = -2*si*sj*(np.trace(Ti@basis[a]@Ti.conj().T @ Tj@basis[b]@Tj.conj().T)).real
                        M[3*ei+a, 3*ej+b] += val
    return M

# ============================================================
# Correction analysis
# ============================================================
print("="*70)
print("CORRECTION C(Q) = M(Q) - (2N/β) HessS(Q)")
print("="*70)

for d in [2, 4]:
    lat = Lattice(2, d)
    print(f"\n--- d={d}, {lat.n_edges} edges ---")

    # Q = I
    Q_I = [I2.copy() for _ in range(lat.n_edges)]
    H_I = hessian_correct(lat, Q_I)
    M_I = build_M(lat, Q_I)
    C_I = M_I - 4.0 * H_I  # 2N/β = 4 with N=2, β=1
    eC_I = np.linalg.eigvalsh(C_I)
    print(f"  Q=I: C eigenvalues [{eC_I.min():.6f}, {eC_I.max():.6f}], HessS={np.linalg.eigvalsh(H_I).max():.4f}")

    # Q = iσ₃
    Q_is3 = [1j*sigma[2] for _ in range(lat.n_edges)]
    H_is3 = hessian_correct(lat, Q_is3)
    M_is3 = build_M(lat, Q_is3)
    C_is3 = M_is3 - 4.0 * H_is3
    eC_is3 = np.linalg.eigvalsh(C_is3)
    print(f"  Q=iσ₃: C eigenvalues [{eC_is3.min():.6f}, {eC_is3.max():.6f}], HessS={np.linalg.eigvalsh(H_is3).max():.4f}")

    # Random configs
    np.random.seed(42)
    print(f"\n  Random configs:")
    print(f"  {'trial':>5} | {'max(H)':>8} | {'(β/2N)max(M)':>14} | {'min(C_eig)':>12} | {'max(C_eig)':>12} | {'C≥0?':>5}")
    print(f"  " + "-"*75)
    for trial in range(10):
        Q_r = [random_su2() for _ in range(lat.n_edges)]
        H_r = hessian_correct(lat, Q_r)
        M_r = build_M(lat, Q_r)
        C_r = M_r - 4.0 * H_r
        eH = np.linalg.eigvalsh(H_r)
        eM = np.linalg.eigvalsh(M_r)
        eC = np.linalg.eigvalsh(C_r)
        psd = eC.min() > -1e-8
        print(f"  {trial:5d} | {eH.max():8.4f} | {0.25*eM.max():14.4f} | {eC.min():12.4f} | {eC.max():12.4f} | {'Y' if psd else 'N':>5}")

# ============================================================
# Decompose C into self and cross contributions
# ============================================================
print("\n" + "="*70)
print("DECOMPOSITION OF C INTO SELF AND CROSS PARTS")
print("="*70)

lat = Lattice(2, 2)
np.random.seed(42)
Q_r = [random_su2() for _ in range(lat.n_edges)]

# Build H and M separately for self and cross terms
n = 3 * lat.n_edges
H_self = np.zeros((n,n)); H_cross = np.zeros((n,n))
M_self = np.zeros((n,n)); M_cross = np.zeros((n,n))

for (e1_idx, e2_idx, e3_idx, e4_idx) in lat.plaquettes:
    Q1,Q2,Q3,Q4 = Q_r[e1_idx],Q_r[e2_idx],Q_r[e3_idx],Q_r[e4_idx]
    Q3i = Q3.conj().T; Q4i = Q4.conj().T
    U = Q1@Q2@Q3i@Q4i
    reTrU = np.trace(U).real
    Ts = [I2, Q1.copy(), Q1@Q2@Q3i, U]
    sn = [+1,+1,-1,-1]; es = [e1_idx,e2_idx,e3_idx,e4_idx]

    # Self-terms
    for p in range(4):
        for a in range(3):
            H_self[3*es[p]+a, 3*es[p]+a] += 0.5 * reTrU  # (β/N)=(1/2) with β=1,N=2
            M_self[3*es[p]+a, 3*es[p]+a] += -2*(np.trace(basis[a]@basis[a])).real  # = 4

    # Cross-terms for M
    for i_s in range(4):
        for j_s in range(4):
            if i_s == j_s: continue
            si,sj = sn[i_s],sn[j_s]
            Ti,Tj = Ts[i_s],Ts[j_s]
            ei,ej = es[i_s],es[j_s]
            for a in range(3):
                for b in range(3):
                    val = -2*si*sj*(np.trace(Ti@basis[a]@Ti.conj().T @ Tj@basis[b]@Tj.conj().T)).real
                    M_cross[3*ei+a, 3*ej+b] += val

    # Cross-terms for H
    Ls = [Q1, Q1@Q2, Q1@Q2, Q1@Q2@Q3i]
    Rs = [Q2@Q3i@Q4i, Q3i@Q4i, Q3i@Q4i, Q4i]
    mids = {(0,1):Q2,(0,2):Q2,(0,3):Q2@Q3i,(1,2):I2,(1,3):Q3i,(2,3):Q3i}
    for (p,q),middle in mids.items():
        sp,sq = sn[p],sn[q]
        for a in range(3):
            for b in range(3):
                val = -0.5*sp*sq*(np.trace(Ls[p]@basis[a]@middle@basis[b]@Rs[q])).real
                H_cross[3*es[p]+a, 3*es[q]+b] += val
                H_cross[3*es[q]+b, 3*es[p]+a] += val

C_self = M_self - 4.0 * H_self
C_cross = M_cross - 4.0 * H_cross

eC_self = np.linalg.eigvalsh(C_self)
eC_cross = np.linalg.eigvalsh(C_cross)

print(f"\nFor random Q on 2^2 lattice:")
print(f"  C_self eigenvalues: [{eC_self.min():.4f}, {eC_self.max():.4f}]")
print(f"  C_cross eigenvalues: [{eC_cross.min():.4f}, {eC_cross.max():.4f}]")
print(f"  C_self PSD? {eC_self.min() > -1e-8}")
print(f"  C_cross PSD? {eC_cross.min() > -1e-8}")

# Self-correction analysis
print(f"\n  Self-correction structure:")
print(f"  H_self diag values (per edge, per color):")
reTrUs = []
for (e1,e2,e3,e4) in lat.plaquettes:
    U_p = Q_r[e1]@Q_r[e2]@Q_r[e3].conj().T@Q_r[e4].conj().T
    reTrUs.append(np.trace(U_p).real)

print(f"  Re Tr(U_□) for each plaquette: {[f'{x:.4f}' for x in reTrUs]}")
print(f"  M_self diagonal: 4 × (# plaquettes per edge) = {M_self[0,0]:.4f}")
print(f"  H_self diagonal: (β/N) × Σ Re Tr(U_□ containing edge) = {H_self[0,0]:.4f}")
print(f"  C_self = M_self - 4H_self = 4 × [# plaq/edge × 1 - Σ Re Tr(U)/2]")
print(f"  Since Re Tr(U) ≤ 2, each plaquette contributes ≥ 0 to C_self ⟹ C_self ≥ 0!")
print(f"  C_self PSD confirmed: {eC_self.min() > -1e-8}")

# ============================================================
# Key structural result
# ============================================================
print("\n" + "="*70)
print("KEY STRUCTURAL RESULT")
print("="*70)
print("""
The Hessian decomposes as:

  HessS(v,v;Q) = (β/N) Σ_{□∋e} Re Tr(U_□) × |v_e|²     [self-terms]
                + cross-terms from adjacent edges

At Q=I (all U_□=I, Re Tr=2):
  Self = (β/N) × 2 × (#plaq/edge) × |v_e|² = (2β/N) × 2(d-1) × |v_e|²
  This matches (β/2N) × M_self = (β/2N) × 4 × 2(d-1) = (2β/N) × 2(d-1)

The self-term correction C_self is ALWAYS ≥ 0 because:
  C_self = 4 × Σ_{□∋e} [1 - Re Tr(U_□)/2] × |v_e|²
  and Re Tr(U)/2 ≤ 1 for SU(2).

The cross-term correction C_cross is NOT PSD in general.
The total C = C_self + C_cross may have negative eigenvalues.

However, the max eigenvalue of HessS appears bounded by the flat-connection value:
  λ_max(HessS(Q)) ≤ λ_max(HessS(Q_flat)) = 4d  [in iσ_a normalization]

This is because:
1. Self-terms are suppressed by Re Tr(U_□)/2 ≤ 1 when U_□ ≠ I
2. Cross-terms partially compensate but not enough to exceed the flat bound
""")

# Verify the bound conjecture more rigorously with gradient ascent
print("="*70)
print("GRADIENT ASCENT VERIFICATION (d=4)")
print("="*70)

def expm_su2(v):
    det_v = v[0,0]*v[1,1] - v[0,1]*v[1,0]
    theta = np.sqrt(np.abs((-det_v).real))
    if theta < 1e-15:
        return I2 + v + 0.5 * v @ v
    return np.cos(theta) * I2 + (np.sin(theta) / theta) * v

lat4 = Lattice(2, 4)
np.random.seed(999)

# Start from many random initial configs
best_overall = 0
for start in range(5):
    Q = [random_su2() for _ in range(lat4.n_edges)]
    current_max = np.linalg.eigvalsh(hessian_correct(lat4, Q)).max()

    for it in range(100):
        best_max = current_max
        for _ in range(20):
            Q_new = []
            for q in Q:
                v = 0.05 * np.random.randn(3)
                w = sum(c * basis[a] for a, c in enumerate(v))
                Q_new.append(q @ expm_su2(w))
            new_max = np.linalg.eigvalsh(hessian_correct(lat4, Q_new)).max()
            if new_max > best_max:
                best_max = new_max
                Q_best = Q_new
        if best_max > current_max:
            Q = Q_best
            current_max = best_max

    best_overall = max(best_overall, current_max)
    print(f"  Start {start}: converged to max eigenvalue = {current_max:.6f}")

flat_max = np.linalg.eigvalsh(hessian_correct(lat4, [I2.copy() for _ in range(lat4.n_edges)])).max()
print(f"\n  Best found: {best_overall:.6f}")
print(f"  Flat bound: {flat_max:.6f}")
print(f"  Ratio: {best_overall/flat_max:.6f}")
print(f"  Bound holds: {best_overall <= flat_max + 1e-6}")
