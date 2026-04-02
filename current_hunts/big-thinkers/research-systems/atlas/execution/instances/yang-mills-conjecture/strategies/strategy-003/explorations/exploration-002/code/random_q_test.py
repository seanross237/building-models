"""
Test HessS vs (β/2N)M at random Q configurations.
E001 claimed a large curvature correction. Let's check.
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
    theta_sq = -det_v
    theta = np.sqrt(np.abs(theta_sq.real))
    if theta < 1e-15:
        return I2 + v + 0.5 * v @ v
    return np.cos(theta) * I2 + (np.sin(theta) / theta) * v

def random_su2():
    v = np.random.randn(4)
    v /= np.linalg.norm(v)
    return v[0]*I2 + 1j*(v[1]*sigma[0] + v[2]*sigma[1] + v[3]*sigma[2])

def su2_basis():
    return [1j * sigma[a] for a in range(3)]

basis = su2_basis()

class Lattice:
    def __init__(self, L, d):
        self.L = L
        self.d = d
        self.sites = list(iterprod(*[range(L)]*d))
        self.n_sites = L**d
        self.n_edges = self.n_sites * d
        self.plaquettes = []
        for x in self.sites:
            for mu in range(d):
                for nu in range(mu+1, d):
                    x_mu = list(x); x_mu[mu] = (x_mu[mu]+1)%L; x_mu = tuple(x_mu)
                    x_nu = list(x); x_nu[nu] = (x_nu[nu]+1)%L; x_nu = tuple(x_nu)
                    e1 = self._eidx(x, mu)
                    e2 = self._eidx(x_mu, nu)
                    e3 = self._eidx(x_nu, mu)
                    e4 = self._eidx(x, nu)
                    self.plaquettes.append((e1, e2, e3, e4))

    def _eidx(self, x, mu):
        idx = 0
        for i, xi in enumerate(x):
            idx = idx * self.L + xi
        return idx * self.d + mu

def hessian_analytical(lat, Q, beta=1.0, N=2):
    n = 3 * lat.n_edges
    H = np.zeros((n, n))
    for (e1_idx, e2_idx, e3_idx, e4_idx) in lat.plaquettes:
        Q1, Q2, Q3, Q4 = Q[e1_idx], Q[e2_idx], Q[e3_idx], Q[e4_idx]
        Q3inv = Q3.conj().T
        Q4inv = Q4.conj().T
        L1 = Q1; L12 = Q1 @ Q2; L123 = L12 @ Q3inv
        R1 = Q2 @ Q3inv @ Q4inv; R2 = Q3inv @ Q4inv; R3 = Q4inv
        slots = [(e1_idx, +1, L1, R1), (e2_idx, +1, L12, R2),
                 (e3_idx, -1, L12, R2), (e4_idx, -1, L123, R3)]
        middles = {(0,1): Q2, (0,2): Q2, (0,3): Q2 @ Q3inv,
                   (1,2): I2, (1,3): Q3inv, (2,3): Q3inv}
        for p in range(4):
            ep, sp, Lp, Rp = slots[p]
            for a in range(3):
                for b in range(3):
                    val = -(beta/N) * (np.trace(Lp @ basis[a] @ basis[b] @ Rp)).real
                    H[3*ep + a, 3*ep + b] += val
        for (p, q), mid in middles.items():
            ep, sp, Lp, Rp = slots[p]
            eq, sq, Lq, Rq = slots[q]
            for a in range(3):
                for b in range(3):
                    val = -(beta/N) * sp * sq * (np.trace(Lp @ basis[a] @ mid @ basis[b] @ Rq)).real
                    H[3*ep + a, 3*eq + b] += val
                    H[3*eq + b, 3*ep + a] += val
    return H

def build_M(lat, Q):
    n = 3 * lat.n_edges
    M = np.zeros((n, n))
    for (e1, e2, e3, e4) in lat.plaquettes:
        Q1, Q2, Q3, Q4 = Q[e1], Q[e2], Q[e3], Q[e4]
        Q3inv = Q3.conj().T; Q4inv = Q4.conj().T
        U_plaq = Q1 @ Q2 @ Q3inv @ Q4inv
        T1 = I2; T2 = Q1; T3 = Q1 @ Q2 @ Q3inv; T4 = U_plaq
        transports = [(e1, +1, T1), (e2, +1, T2), (e3, -1, T3), (e4, -1, T4)]
        for (ei, si, Ti) in transports:
            for (ej, sj, Tj) in transports:
                Tidg = Ti.conj().T; Tjdg = Tj.conj().T
                for a in range(3):
                    for b in range(3):
                        val = -2 * si * sj * (np.trace(Ti @ basis[a] @ Tidg @ Tj @ basis[b] @ Tjdg)).real
                        M[3*ei + a, 3*ej + b] += val
    return M

# Use small lattice for speed: L=2, d=2 first
L, d = 2, 2
lat = Lattice(L, d)
print(f"Lattice: {L}^{d}, edges={lat.n_edges}, plaq={len(lat.plaquettes)}")
print(f"Matrix size: {3*lat.n_edges}")

np.random.seed(123)
print("\nRandom Q tests:")
print(f"{'Config':>8} | {'max(H)':>10} | {'max(M)':>10} | {'β/2N·max(M)':>12} | {'max(C)':>10} | {'min(C)':>10} | {'H=β/2N·M?':>10}")
print("-"*90)

for trial in range(5):
    Q = [random_su2() for _ in range(lat.n_edges)]
    H = hessian_analytical(lat, Q)
    M = build_M(lat, Q)
    C = M - 4.0 * H  # C = M - (2N/β)H
    eH = np.linalg.eigvalsh(H)
    eM = np.linalg.eigvalsh(M)
    eC = np.linalg.eigvalsh(C)
    match = np.allclose(H, 0.25 * M, atol=1e-10)
    print(f"Trial {trial:2d} | {eH.max():10.4f} | {eM.max():10.4f} | {0.25*eM.max():12.4f} | {eC.max():10.6f} | {eC.min():10.6f} | {'YES' if match else 'NO'}")

# Now d=4
print("\n\nNow testing d=4:")
L, d = 2, 4
lat = Lattice(L, d)
print(f"Lattice: {L}^{d}, edges={lat.n_edges}, plaq={len(lat.plaquettes)}")

np.random.seed(456)
for trial in range(3):
    Q = [random_su2() for _ in range(lat.n_edges)]
    H = hessian_analytical(lat, Q)
    M = build_M(lat, Q)
    C = M - 4.0 * H
    eH = np.linalg.eigvalsh(H)
    eM = np.linalg.eigvalsh(M)
    eC = np.linalg.eigvalsh(C)
    match = np.allclose(H, 0.25 * M, atol=1e-10)
    print(f"Trial {trial:2d}: max(H)={eH.max():.4f}, max(M)={eM.max():.4f}, β/2N·max(M)={0.25*eM.max():.4f}, C range=[{eC.min():.6f}, {eC.max():.6f}], match={match}")

# Explicit trace-based derivation showing HessS = (β/2N)M
print("\n\n" + "="*70)
print("ALGEBRAIC ANALYSIS: Why HessS = (β/2N)M")
print("="*70)
print("""
For a single plaquette U = Q1 Q2 Q3^{-1} Q4^{-1}, with perturbation
Q_i → Q_i exp(ε w_i) where w1=v1, w2=v2, w3=-v3, w4=-v4:

d²/dε² Re Tr(U(ε))|_0 = self_sum + 2*cross_sum

where self_sum = Σ_p Re Tr(L_p w_p² R_p)
and cross_sum = Σ_{p<q} Re Tr(L_p w_p M_{pq} w_q R_q)

Now, B_□ = v1 + Q1 v2 Q1† - (Q1Q2Q3⁻¹)v3(Q1Q2Q3⁻¹)† - U v4 U†

|B|²_Kill = -2 Tr(B²)

Let me expand this with transported w's:
Define ŵ_p = T_p w_p T_p† (transported perturbation) with signs absorbed.
T1 = I, T2 = Q1, T3 = Q1Q2Q3⁻¹, T4 = U

Then B = ŵ1 + ŵ2 + ŵ3 + ŵ4 (signs already in w).

|B|²_Kill = -2Tr(B²) = -2Tr[(ŵ1+ŵ2+ŵ3+ŵ4)²]
= -2[Σ_p Tr(ŵ_p²) + 2Σ_{p<q} Tr(ŵ_p ŵ_q)]
= -2Σ_p Tr(T_p w_p² T_p†) - 4Σ_{p<q} Tr(T_p w_p T_p† T_q w_q T_q†)

Using cyclicity: Tr(T_p w_p² T_p†) = Tr(w_p² T_p† T_p) = Tr(w_p²) [since T_p ∈ SU(2)]

So the self terms in |B|²: -2 Σ_p Tr(w_p²)
The self terms in d²ReTr: Σ_p Re Tr(L_p w_p² R_p)

At Q=I: Re Tr(w_p²) = Tr(w_p²) (real since w_p antiherm), and -Tr(w_p²) = -Tr(w_p²).
So -(β/N) × d²ReTr = -(β/N) Σ Tr(w_p²) and (β/2N)|B|²_Kill = (β/2N)(-2)ΣTr(w_p²) = -(β/N)ΣTr(w_p²). Match!

But for general Q, Re Tr(L_p w_p² R_p) ≠ Tr(w_p²) since L_p R_p ≠ I in general.
Actually: L_p R_p = ?
For p=0: L1 R1 = Q1 Q2 Q3⁻¹ Q4⁻¹ = U_□
For p=1: L12 R2 = Q1Q2 Q3⁻¹Q4⁻¹ = U_□
For p=2: L12 R2 = Q1Q2 Q3⁻¹Q4⁻¹ = U_□  (same as p=1!)
For p=3: L123 R3 = Q1Q2Q3⁻¹ Q4⁻¹ = U_□

SO ALL SELF TERMS HAVE THE SAME PRODUCT L_p R_p = U_□!

Re Tr(L_p w_p² R_p) = Re Tr(w_p² U_□)  (by cyclicity: Tr(L w² R) = Tr(w² R L))
Wait: Tr(L_p w² R_p) = Tr(w² R_p L_p). And R_p L_p:
p=0: R1 L1 = Q2Q3⁻¹Q4⁻¹Q1 (cyclic perm of U)
p=1: R2 L12 = Q3⁻¹Q4⁻¹Q1Q2 (another cyclic perm)
p=2: R2 L12 = same as p=1
p=3: R3 L123 = Q4⁻¹Q1Q2Q3⁻¹ (another cyclic perm)

All are cyclic permutations of U_□. But Tr(w² × cyclic_perm_of_U) = Tr(w² U)
since Tr(ABCD) = Tr(BCDA). YES! All cyclic perms give the same trace.

So Re Tr(L_p w_p² R_p) = Re Tr(w_p² U_□) for all p.

Meanwhile |B|²_Kill self-term = -2Tr(w_p²) = -2Tr(w_p²) independent of Q.

These are NOT equal unless U_□ = I!

...Wait but our numerical test shows they ARE equal for random Q. Let me check...
""")

# Verify: is Re Tr(w² U) = -2Tr(w²)/(-2) = Tr(w²) for all U?
print("Checking Re Tr(w² U) vs Tr(w²) for random U, w:")
np.random.seed(789)
for _ in range(5):
    U = random_su2()
    coeffs = np.random.randn(3)
    w = sum(c*b for c, b in zip(coeffs, basis))
    t1 = np.trace(w @ w @ U).real  # Re Tr(w² U)
    t2 = np.trace(w @ w).real       # Tr(w²) — always real since w antiherm
    print(f"  Re Tr(w²U) = {t1:.8f},  Tr(w²) = {t2:.8f},  ratio = {t1/t2:.8f}")

# INTERESTING! For SU(2), we need to check if Re Tr(X·U) = Tr(X) for hermitian X = w²
# w ∈ su(2) => w² = -|w|²_Eucl · I (for SU(2)!) since (iσ_a)² = -I
# Wait: (Σ c_a iσ_a)² = - Σ c_a² I + Σ_{a≠b} c_a c_b iσ_a iσ_b
# For su(2): (iσ_a)(iσ_b) = -σ_aσ_b = -(δ_{ab}I + iε_{abc}σ_c) = -δ_{ab}I - iε_{abc}σ_c
# So (Σ c_a iσ_a)² = -|c|²I - i Σ_{a≠b} c_a c_b ε_{abc} σ_c
# Hmm, actually: Σ_{a,b} c_a c_b (-δ_{ab}I - iε_{abc}σ_c)
# = -|c|²I - i Σ_c (Σ_{a,b} ε_{abc} c_a c_b) σ_c
# = -|c|²I - i Σ_c 0 · σ_c  (since ε_{abc}c_ac_b is antisymmetric in a,b but c_ac_b symmetric)
# = -|c|²I

# SO w² = -|c|² I for any w ∈ su(2)! This is the KEY IDENTITY.
print("\nKEY: For w = Σ c_a (iσ_a), w² = -|c|² I (scalar matrix)")
for _ in range(3):
    coeffs = np.random.randn(3)
    w = sum(c*b for c, b in zip(coeffs, basis))
    wsq = w @ w
    expected = -np.sum(coeffs**2) * I2
    print(f"  c={coeffs}, w² =? -|c|²I: {np.allclose(wsq, expected)}")

print("\nConsequence: Tr(w²U) = -|c|² Tr(U), and Re Tr(w²U) = -|c|² Re Tr(U)")
print("At flat conn (U=I): Re Tr(w²U) = -2|c|² = Tr(w²). ✓")
print("At curved conn: Re Tr(w²U) = -|c|² Re Tr(U) ≠ Tr(w²) = -2|c|²")
print("Unless Re Tr(U) = 2, i.e., U = I.")

# Wait but numerically C=0 for random Q. Let me recheck...
print("\n\nRe-checking C for random Q (d=2 lattice):")
L, d = 2, 2
lat = Lattice(L, d)
np.random.seed(42)
Q = [random_su2() for _ in range(lat.n_edges)]
H = hessian_analytical(lat, Q)
M = build_M(lat, Q)
C = M - 4.0 * H
print(f"max|C| = {np.abs(C).max():.2e}")
print(f"max|H| = {np.abs(H).max():.2e}")
print(f"max|M| = {np.abs(M).max():.2e}")

# Check one plaquette contribution in detail
e1, e2, e3, e4 = lat.plaquettes[0]
Q1, Q2, Q3, Q4 = Q[e1], Q[e2], Q[e3], Q[e4]
U_plaq = Q1 @ Q2 @ Q3.conj().T @ Q4.conj().T
print(f"\nPlaquette 0: Re Tr(U) = {np.trace(U_plaq).real:.6f}")
print(f"Is U=I? {np.allclose(U_plaq, I2)}")
