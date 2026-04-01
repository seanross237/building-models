"""
Closed-form Hessian of the Wilson action for SU(2).

KEY IDENTITY (specific to SU(2)): For w = Σ c_a (iσ_a) ∈ su(2), w² = -|c|² I.
This makes the self-terms of the Hessian proportional to Re Tr(U_□).

FORMULA (derived here and verified):

For one plaquette □ with U_□ = Q1 Q2 Q3⁻¹ Q4⁻¹:

d²/dε² Re Tr(U_□(ε))|_0 = SELF_TERMS + 2 × CROSS_TERMS

SELF_TERMS:
  Σ_p Re Tr(w_p² U_□) = -Re Tr(U_□) × Σ_p |c_p|²   [using w²=-|c|²I]

CROSS_TERMS:
  Σ_{p<q} Re Tr(L_p w_p mid_{pq} w_q R_q)

  These can be expressed as bilinear forms:
  Re Tr(L_p w_p mid_{pq} w_q R_q) = Σ_{a,b} c_{p,a} c_{q,b} K^{pq}_{ab}
  where K^{pq}_{ab} = Re Tr(L_p (iσ_a) mid_{pq} (iσ_b) R_q)

HessS_□ = -(β/N) [-Re Tr(U_□) Σ_p |c_p|² + 2 Σ_{p<q} Σ_{ab} c_{p,a} c_{q,b} K^{pq}_{ab}]

(β/2N) × v^T M_□ v = (β/2N) × [-2Tr(B²)]
  where B = Σ_p T_p w_p T_p† and T's are transport matrices.

This script:
1. Derives and verifies the formula element by element
2. Decomposes HessS and M into self and cross parts
3. Characterizes the correction C = M - (2N/β)HessS
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

def adjoint_3x3(Q):
    """3x3 adjoint matrix: Ad_Q(iσ_a) = Q(iσ_a)Q† = Σ_b R_{ba}(iσ_b)"""
    Qd = Q.conj().T
    R = np.zeros((3,3))
    for a in range(3):
        rot = Q @ basis[a] @ Qd
        for b in range(3):
            R[b,a] = (np.trace(basis[b].conj().T @ rot) / 2.0).real
    return R

# ============================================================
# Single plaquette: decompose HessS into self + cross parts
# ============================================================
def analyze_single_plaquette(Q1, Q2, Q3, Q4, beta=1.0, N=2):
    """Decompose single-plaquette Hessian into self and cross terms."""
    Q3inv = Q3.conj().T
    Q4inv = Q4.conj().T
    U = Q1 @ Q2 @ Q3inv @ Q4inv
    reTrU = np.trace(U).real

    # Transport matrices for M
    T = [I2.copy(), Q1.copy(), Q1 @ Q2 @ Q3inv, U.copy()]
    signs = [+1, +1, -1, -1]
    # Note: the signed w's are w1=v1, w2=v2, w3=-v3, w4=-v4

    # Left/Right contexts for HessS
    L = [Q1, Q1 @ Q2, Q1 @ Q2, Q1 @ Q2 @ Q3inv]
    R = [Q2 @ Q3inv @ Q4inv, Q3inv @ Q4inv, Q3inv @ Q4inv, Q4inv]

    # Middles for cross terms
    mid = {(0,1): Q2, (0,2): Q2, (0,3): Q2 @ Q3inv,
           (1,2): I2, (1,3): Q3inv, (2,3): Q3inv}

    # Build 12×12 Hessian matrix (4 edges × 3 colors)
    H_self = np.zeros((12, 12))
    H_cross = np.zeros((12, 12))
    M_self = np.zeros((12, 12))
    M_cross = np.zeros((12, 12))

    # Self-terms
    for p in range(4):
        for a in range(3):
            for b in range(3):
                # HessS self: -(β/N) Re Tr(L_p basis[a] basis[b] R_p)
                h_val = -(beta/N) * (np.trace(L[p] @ basis[a] @ basis[b] @ R[p])).real
                H_self[3*p+a, 3*p+b] += h_val

                # M self: -2 Tr(T_p basis[a] T_p† T_p basis[b] T_p†) = -2 Tr(basis[a] basis[b])
                # (since T_p†T_p = I)
                m_val = -2 * (np.trace(T[p] @ basis[a] @ T[p].conj().T @ T[p] @ basis[b] @ T[p].conj().T)).real
                M_self[3*p+a, 3*p+b] += m_val

    # Cross-terms
    for (p,q), middle in mid.items():
        sp, sq = signs[p], signs[q]
        for a in range(3):
            for b in range(3):
                # HessS cross: -(β/N) sp sq Re Tr(L_p basis[a] middle basis[b] R_q) (both ways)
                h_val = -(beta/N) * sp * sq * (np.trace(L[p] @ basis[a] @ middle @ basis[b] @ R[q])).real
                H_cross[3*p+a, 3*q+b] += h_val
                H_cross[3*q+b, 3*p+a] += h_val

                # M cross: -2 sp sq [Tr(T_p basis[a] T_p† T_q basis[b] T_q†) + Tr(T_q basis[b] T_q† T_p basis[a] T_p†)]
                # = -4 sp sq Re Tr(T_p basis[a] T_p† T_q basis[b] T_q†)
                # But we add symmetrically:
                m_val = -2 * sp * sq * (np.trace(T[p] @ basis[a] @ T[p].conj().T @ T[q] @ basis[b] @ T[q].conj().T)).real
                M_cross[3*p+a, 3*q+b] += m_val
                m_val2 = -2 * sq * sp * (np.trace(T[q] @ basis[b] @ T[q].conj().T @ T[p] @ basis[a] @ T[p].conj().T)).real
                M_cross[3*q+b, 3*p+a] += m_val2

    H_total = H_self + H_cross
    M_total = M_self + M_cross
    C_total = M_total - (2*N/beta) * H_total

    return {
        'U': U, 'reTrU': reTrU,
        'H_self': H_self, 'H_cross': H_cross, 'H_total': H_total,
        'M_self': M_self, 'M_cross': M_cross, 'M_total': M_total,
        'C_total': C_total,
    }

# ============================================================
# Analysis at key configurations
# ============================================================
print("="*70)
print("SINGLE PLAQUETTE DECOMPOSITION")
print("="*70)

configs = {
    'Q=I': (I2, I2, I2, I2),
    'Q=iσ₃': (1j*sigma[2], 1j*sigma[2], 1j*sigma[2], 1j*sigma[2]),
}

np.random.seed(42)
for i in range(3):
    Qs = tuple(random_su2() for _ in range(4))
    configs[f'Random {i}'] = Qs

for name, (Q1, Q2, Q3, Q4) in configs.items():
    r = analyze_single_plaquette(Q1, Q2, Q3, Q4)
    eH = np.linalg.eigvalsh(r['H_total'])
    eM = np.linalg.eigvalsh(r['M_total'])
    eC = np.linalg.eigvalsh(r['C_total'])

    # Self-term structure: should be -Re Tr(U)/2 × δ_{ab} for each block (using w²=-|c|²I)
    # Actually: -(1/2) Re Tr(L_p basis[a] basis[b] R_p) = -(1/2) Re Tr(basis[a] basis[b] U)
    # basis[a]basis[b] = (iσ_a)(iσ_b) = -(δ_{ab}I + iε_{abc}σ_c)
    # Tr(basis[a]basis[b] U) = -(δ_{ab} Tr(U) + iε_{abc} Tr(σ_c U))
    # Re Tr = -(δ_{ab} Re Tr(U) - ε_{abc} Im Tr(σ_c U))
    # So H_self block at (p,p): +(1/2)(δ_{ab} Re Tr(U) - ε_{abc} Im Tr(σ_c U))
    # Wait, but U depends on cyclic permutation... Actually Tr(L_p X R_p) = Tr(X R_p L_p) = Tr(X U^{cyc_p}) = Tr(X U) (same trace)

    print(f"\n--- {name} ---")
    print(f"  Re Tr(U_□) = {r['reTrU']:.6f}")
    print(f"  H eigs: [{eH.min():.4f}, {eH.max():.4f}]")
    print(f"  M eigs: [{eM.min():.4f}, {eM.max():.4f}]")
    print(f"  C eigs: [{eC.min():.4f}, {eC.max():.4f}]")
    print(f"  H = (β/2N)M? {np.allclose(r['H_total'], 0.25 * r['M_total'], atol=1e-10)}")

    # Check self-term structure
    # H_self for block (p,p) should be:
    # -(β/N) Re Tr(basis[a] basis[b] U) = -(β/N)[-(δ_{ab} Re Tr(U) + something)]
    # Let's check diagonal blocks
    for p in range(4):
        block = r['H_self'][3*p:3*p+3, 3*p:3*p+3]
        diag_val = block[0,0]  # should be related to Re Tr(U)
        expected_diag = (1/2) * r['reTrU']  # -(β/N) × (-(Re Tr(U))) = (1/2)Re Tr(U) when β/N=1/2
        if p == 0:
            print(f"  H_self diag block p=0: diag={block[0,0]:.6f}, expected {expected_diag:.6f}, match={abs(block[0,0]-expected_diag)<1e-10}")

    # M_self block: -2 Tr(basis[a] basis[b]) = -2 × (-2δ_{ab}) = 4δ_{ab}
    block_M = r['M_self'][0:3, 0:3]
    print(f"  M_self block (0,0): diag={block_M[0,0]:.4f}, expected 4.0")

# ============================================================
# Verify the self-term formula explicitly
# ============================================================
print("\n" + "="*70)
print("SELF-TERM FORMULA VERIFICATION")
print("="*70)

print("""
For SU(2), the self-terms simplify completely:
  w² = -|c|² I  (the key su(2) identity)

Therefore:
  Re Tr(L_p w_p² R_p) = Re Tr(-|c_p|² I × U_□) = -|c_p|² Re Tr(U_□)

So HessS_□ self-part = -(β/N) × [-Re Tr(U_□) Σ_p |c_p|²]
                      = (β/N) Re Tr(U_□) Σ_p |c_p|²

And (β/2N) M_□ self-part = (β/2N) × [4 Σ_p |c_p|²]
                          = (2β/N) Σ_p |c_p|²

Self-term correction ratio: HessS_self / [(β/2N)M_self] = Re Tr(U_□) / 2

Since |Re Tr(U)| ≤ Tr(I) = 2 for SU(2), this ratio is in [-1, 1].
The self-terms are SUPPRESSED when U_□ ≠ I.
""")

# ============================================================
# Now analyze the cross-terms
# ============================================================
print("="*70)
print("CROSS-TERM ANALYSIS")
print("="*70)

# For the M operator, cross-term between slots (p,q):
# -4 sp sq Tr(T_p w_p T_p† T_q w_q T_q†)
# = -4 sp sq Σ_{a,b} c_{p,a} c_{q,b} Tr(T_p (iσ_a) T_p† T_q (iσ_b) T_q†)
# = -4 sp sq Σ_{a,b} c_{p,a} c_{q,b} Tr(Ad_{T_p}(iσ_a) Ad_{T_q}(iσ_b))
# = -4 sp sq Σ_{a,b} c_{p,a} c_{q,b} Σ_{c,d} [Ad_{T_p}]_{ca} [Ad_{T_q}]_{db} Tr(iσ_c · iσ_d)
# = -4 sp sq Σ_{a,b} c_{p,a} c_{q,b} Σ_c [Ad_{T_p}]_{ca} [Ad_{T_q}]_{cb} × (-2)
# = 8 sp sq Σ_{a,b} c_{p,a} c_{q,b} [Ad_{T_p}^T Ad_{T_q}]_{ab}
#
# So the M cross-term kernel is: 8 sp sq [Ad_{T_p}^T Ad_{T_q}]_{ab}
# = 8 sp sq [R_p^T R_q]_{ab}  where R_p = Ad_{T_p} ∈ SO(3)
# = 8 sp sq [cos(angle between transported frames)]

# For the HessS cross-term (p,q):
# -(β/N) sp sq Re Tr(L_p (iσ_a) mid_{pq} (iσ_b) R_q)
# This kernel K^{pq}_{ab} depends on the full path structure.

print("Cross-term kernels for random configuration:")
np.random.seed(42)
Q1, Q2, Q3, Q4 = [random_su2() for _ in range(4)]
Q3inv = Q3.conj().T; Q4inv = Q4.conj().T
U = Q1 @ Q2 @ Q3inv @ Q4inv

# Transport matrices
T = [I2.copy(), Q1.copy(), Q1 @ Q2 @ Q3inv, U.copy()]
signs = [+1, +1, -1, -1]
L = [Q1, Q1 @ Q2, Q1 @ Q2, Q1 @ Q2 @ Q3inv]
R_ctx = [Q2 @ Q3inv @ Q4inv, Q3inv @ Q4inv, Q3inv @ Q4inv, Q4inv]
mid = {(0,1): Q2, (0,2): Q2, (0,3): Q2 @ Q3inv,
       (1,2): I2, (1,3): Q3inv, (2,3): Q3inv}

print(f"\nRe Tr(U_□) = {np.trace(U).real:.6f}")

for (p,q), middle in mid.items():
    sp, sq = signs[p], signs[q]

    # HessS kernel
    K_H = np.zeros((3,3))
    for a in range(3):
        for b in range(3):
            K_H[a,b] = -(1/2) * sp * sq * (np.trace(L[p] @ basis[a] @ middle @ basis[b] @ R_ctx[q])).real

    # M kernel
    K_M = np.zeros((3,3))
    Rp = adjoint_3x3(T[p])
    Rq = adjoint_3x3(T[q])
    K_M_mat = 8 * sp * sq * (Rp.T @ Rq)
    # Actually this gives M cross kernel per pair (factor 2 for symmetry included differently)
    # Let me recompute more carefully
    for a in range(3):
        for b in range(3):
            K_M[a,b] = -2 * sp * sq * (np.trace(T[p] @ basis[a] @ T[p].conj().T @ T[q] @ basis[b] @ T[q].conj().T)).real

    print(f"\n  Slots ({p},{q}): sp={sp:+d}, sq={sq:+d}")
    print(f"    K_H (HessS cross kernel, 3x3):\n    {K_H}")
    print(f"    K_M (M cross kernel, 3x3):\n    {K_M}")
    diff = K_M - (2*2/1) * K_H  # C = M - (2N/β)H for cross terms
    print(f"    K_C = K_M - 4K_H (correction kernel):\n    {diff}")

# ============================================================
# Full correction analysis
# ============================================================
print("\n" + "="*70)
print("CORRECTION C(Q) = M(Q) - (2N/β)HessS(Q)")
print("="*70)

# On full lattice
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

def build_H_and_M(lat, Q, beta=1.0, N=2):
    n = 3 * lat.n_edges
    H = np.zeros((n,n)); M_mat = np.zeros((n,n))
    for (e1,e2,e3,e4) in lat.plaquettes:
        Q1,Q2,Q3,Q4 = Q[e1],Q[e2],Q[e3],Q[e4]
        Q3i = Q3.conj().T; Q4i = Q4.conj().T
        U = Q1@Q2@Q3i@Q4i
        Ls = [Q1, Q1@Q2, Q1@Q2, Q1@Q2@Q3i]
        Rs = [Q2@Q3i@Q4i, Q3i@Q4i, Q3i@Q4i, Q4i]
        Ts = [I2, Q1.copy(), Q1@Q2@Q3i, U]
        sn = [+1,+1,-1,-1]
        es = [e1,e2,e3,e4]
        mids = {(0,1):Q2,(0,2):Q2,(0,3):Q2@Q3i,(1,2):I2,(1,3):Q3i,(2,3):Q3i}

        for p in range(4):
            for a in range(3):
                for b in range(3):
                    hv = -(beta/N)*(np.trace(Ls[p]@basis[a]@basis[b]@Rs[p])).real
                    H[3*es[p]+a, 3*es[p]+b] += hv
                    mv = -2*(np.trace(Ts[p]@basis[a]@Ts[p].conj().T@Ts[p]@basis[b]@Ts[p].conj().T)).real
                    M_mat[3*es[p]+a, 3*es[p]+b] += mv

        for (p,q),middle in mids.items():
            sp,sq = sn[p],sn[q]
            for a in range(3):
                for b in range(3):
                    hv = -(beta/N)*sp*sq*(np.trace(Ls[p]@basis[a]@middle@basis[b]@Rs[q])).real
                    H[3*es[p]+a, 3*es[q]+b] += hv
                    H[3*es[q]+b, 3*es[p]+a] += hv
                    mv = -2*sp*sq*(np.trace(Ts[p]@basis[a]@Ts[p].conj().T@Ts[q]@basis[b]@Ts[q].conj().T)).real
                    M_mat[3*es[p]+a, 3*es[q]+b] += mv
                    mv2 = -2*sq*sp*(np.trace(Ts[q]@basis[b]@Ts[q].conj().T@Ts[p]@basis[a]@Ts[p].conj().T)).real
                    M_mat[3*es[q]+b, 3*es[p]+a] += mv2
    return H, M_mat

# Test on 2^2 lattice
lat22 = Lattice(2, 2)
print(f"\nLattice 2^2: {lat22.n_edges} edges, {len(lat22.plaquettes)} plaquettes")

np.random.seed(100)
print(f"\n{'Trial':>6} | {'Re Tr(U) range':>16} | {'max(H)':>8} | {'(β/2N)max(M)':>14} | {'C psd?':>6} | {'min(C_eig)':>12} | {'max(C_eig)':>12}")
print("-"*95)

for trial in range(8):
    Q_rand = [random_su2() for _ in range(lat22.n_edges)]
    H, M_mat = build_H_and_M(lat22, Q_rand)
    C = M_mat - 4.0 * H
    eH = np.linalg.eigvalsh(H)
    eM = np.linalg.eigvalsh(M_mat)
    eC = np.linalg.eigvalsh(C)

    # Compute Re Tr(U) for all plaquettes
    reTrUs = []
    for (e1,e2,e3,e4) in lat22.plaquettes:
        U = Q_rand[e1] @ Q_rand[e2] @ Q_rand[e3].conj().T @ Q_rand[e4].conj().T
        reTrUs.append(np.trace(U).real)

    psd = eC.min() > -1e-8
    print(f"  {trial:4d} | [{min(reTrUs):+.3f},{max(reTrUs):+.3f}] | {eH.max():8.4f} | {0.25*eM.max():14.4f} | {'YES' if psd else 'NO':>6} | {eC.min():12.6f} | {eC.max():12.6f}")

# Test on 2^4 lattice (d=4)
print(f"\nLattice 2^4:")
lat24 = Lattice(2, 4)
print(f"  {lat24.n_edges} edges, {len(lat24.plaquettes)} plaquettes, matrix {3*lat24.n_edges}x{3*lat24.n_edges}")

for trial in range(3):
    Q_rand = [random_su2() for _ in range(lat24.n_edges)]
    H, M_mat = build_H_and_M(lat24, Q_rand)
    C = M_mat - 4.0 * H
    eH = np.linalg.eigvalsh(H)
    eM = np.linalg.eigvalsh(M_mat)
    eC = np.linalg.eigvalsh(C)
    psd = eC.min() > -1e-8
    print(f"  Trial {trial}: max(H)={eH.max():.4f}, (β/2N)max(M)={0.25*eM.max():.4f}, C psd? {psd}, C eigs=[{eC.min():.4f}, {eC.max():.4f}]")

print("\n" + "="*70)
print("KEY FINDING: Is C(Q) always PSD?")
print("="*70)
print("If C = M - (2N/β)HessS ≥ 0, then HessS ≤ (β/2N)M,")
print("and any bound on M gives a bound on HessS.")
print("But if C has negative eigenvalues, then HessS can exceed (β/2N)M.")
