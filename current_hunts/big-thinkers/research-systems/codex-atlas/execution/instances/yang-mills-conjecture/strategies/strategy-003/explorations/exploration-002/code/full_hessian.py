"""
Build the full Hessian matrix of the Wilson action on a small lattice.
Use analytical formula, verify against finite differences, compute eigenvalues.

Lattice: L^d periodic hypercubic lattice.
Convention: edges labeled by (site, direction μ), μ = 0,...,d-1.
Each edge carries Q_e ∈ SU(2), tangent v_e ∈ su(2) ≅ ℝ³.

Plaquettes: for each site x and pair μ<ν,
  □ = (x,μ), (x+μ̂,ν), (x+ν̂,μ), (x,ν)
  U_□ = Q_{x,μ} Q_{x+μ̂,ν} Q_{x+ν̂,μ}^{-1} Q_{x,ν}^{-1}

The Hessian is a (3|E|) × (3|E|) real symmetric matrix.
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

# ============================================================
# Lattice setup
# ============================================================
class Lattice:
    def __init__(self, L, d):
        self.L = L
        self.d = d
        self.sites = list(iterprod(*[range(L)]*d))
        self.n_sites = L**d
        self.n_edges = self.n_sites * d
        self.n_plaq = self.n_sites * d * (d-1) // 2

        # Edge index: edge (x, mu) -> integer
        self.edge_idx = {}
        for i, x in enumerate(self.sites):
            for mu in range(d):
                self.edge_idx[(x, mu)] = i * d + mu

        # Plaquettes: list of (e1, e2, e3, e4, sign3, sign4)
        # where e1,e2 are forward edges and e3,e4 are backward (inverted)
        self.plaquettes = []
        for x in self.sites:
            for mu in range(d):
                for nu in range(mu+1, d):
                    x_mu = list(x); x_mu[mu] = (x_mu[mu]+1)%L; x_mu = tuple(x_mu)
                    x_nu = list(x); x_nu[nu] = (x_nu[nu]+1)%L; x_nu = tuple(x_nu)

                    e1 = self.edge_idx[(x, mu)]
                    e2 = self.edge_idx[(x_mu, nu)]
                    e3 = self.edge_idx[(x_nu, mu)]  # traversed backward
                    e4 = self.edge_idx[(x, nu)]       # traversed backward
                    self.plaquettes.append((e1, e2, e3, e4))

    def wilson_action(self, Q, beta=1.0, N=2):
        """Compute S = -(β/N) Σ_□ Re Tr(U_□)"""
        S = 0.0
        for (e1, e2, e3, e4) in self.plaquettes:
            U = Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T
            S += -(beta/N) * np.trace(U).real
        return S

def hessian_fd(lat, Q, beta=1.0, N=2, eps=1e-5):
    """Full Hessian by finite differences."""
    n = 3 * lat.n_edges
    H = np.zeros((n, n))

    for i in range(n):
        edge_i = i // 3
        color_i = i % 3

        for j in range(i, n):
            edge_j = j // 3
            color_j = j % 3

            # Perturb Q[edge_i] by eps*basis[color_i] and Q[edge_j] by eps*basis[color_j]
            # Use central difference: H_ij = (S(+,+) - S(+,-) - S(-,+) + S(-,-))/4eps²
            vals = []
            for si in [+1, -1]:
                for sj in [+1, -1]:
                    Qp = [q.copy() for q in Q]
                    Qp[edge_i] = Q[edge_i] @ expm_su2(si*eps*basis[color_i])
                    if edge_i == edge_j:
                        Qp[edge_j] = Qp[edge_j] @ expm_su2(sj*eps*basis[color_j])
                    else:
                        Qp[edge_j] = Q[edge_j] @ expm_su2(sj*eps*basis[color_j])
                    vals.append(lat.wilson_action(Qp, beta, N))

            H[i, j] = (vals[0] - vals[1] - vals[2] + vals[3]) / (4*eps**2)
            H[j, i] = H[i, j]

    return H

def hessian_analytical(lat, Q, beta=1.0, N=2):
    """
    Full Hessian matrix using analytical formula.

    For each plaquette □ with edges (e1, e2, e3, e4):
    U_□(ε) = Q1 e^{εv1} Q2 e^{εv2} e^{-εv3} Q3^{-1} e^{-εv4} Q4^{-1}

    The bilinear form HessS(v,w) for one plaquette involves:
    - Self terms: d²/dε² at a single edge
    - Cross terms: d²/dεdδ between two edges

    For the full 3|E| × 3|E| matrix, entry (i,j) corresponds to
    the Hessian in direction (edge_i, color_a) and (edge_j, color_b).
    """
    n = 3 * lat.n_edges
    H = np.zeros((n, n))

    for (e1_idx, e2_idx, e3_idx, e4_idx) in lat.plaquettes:
        Q1, Q2, Q3, Q4 = Q[e1_idx], Q[e2_idx], Q[e3_idx], Q[e4_idx]
        Q3inv = Q3.conj().T
        Q4inv = Q4.conj().T

        # Partial products
        L1 = Q1
        L12 = Q1 @ Q2
        L123 = L12 @ Q3inv
        R1 = Q2 @ Q3inv @ Q4inv
        R2 = Q3inv @ Q4inv
        R3 = Q4inv

        # Edge list with signed perturbation info:
        # (edge_index, sign, left_context, right_context, position)
        # position: determines which left/right context to use for cross terms
        #
        # The 4 perturbation slots:
        # slot 0: w1=+v_{e1}, inserted at pos between Q1 and Q2
        # slot 1: w2=+v_{e2}, inserted at pos between Q2 and Q3^{-1}
        # slot 2: w3=-v_{e3}, inserted at pos between Q2 and Q3^{-1} (same as slot 1!)
        # slot 3: w4=-v_{e4}, inserted at pos between Q3^{-1} and Q4^{-1}

        # For the bilinear form H(va, wb) where va is basis[a] on edge e_i
        # and wb is basis[b] on edge e_j:
        #
        # We need to compute -(β/N) × d²/dεdδ Re Tr(U(ε,δ)) where
        # edge e_i is perturbed by ε*va and edge e_j by δ*wb.
        #
        # For self-term (same slot, same edge):
        #   -(β/N) Re Tr(L · va·vb · R) where L,R are the context
        #
        # For cross-term (different slots i<j):
        #   -(β/N) Re Tr(L_i · va · middle · wb · R_j) [with appropriate signs]
        #   Plus the reverse: -(β/N) Re Tr(L_j · wb · middle_rev · va · R_i)
        #   But since we want d²/dεdδ with ε for slot i and δ for slot j,
        #   we get just ONE cross term (not symmetrized), times 2? No...
        #
        # Let me think again. For the quadratic form v^T H v:
        # d²/dε² S(Q exp(εv))|_0 has coefficient 1 for self and 2 for cross.
        # For the bilinear form (the matrix): H_ij = d²S/dvi dvj
        # This means for each cross-term pair (slot_p, slot_q):
        #   H_{ea,fb} += -(β/N) × sign_p × sign_q × Re Tr(L_p basis[a] middle_{pq} basis[b] R_q)

        # Let me define the slots more carefully.
        # slot 0: edge e1, sign +1, left = Q1, right = Q2 Q3^{-1} Q4^{-1}
        # slot 1: edge e2, sign +1, left = Q1Q2, right = Q3^{-1} Q4^{-1}
        # slot 2: edge e3, sign -1, left = Q1Q2, right = Q3^{-1} Q4^{-1}
        # slot 3: edge e4, sign -1, left = Q1Q2Q3^{-1}, right = Q4^{-1}

        slots = [
            (e1_idx, +1, L1, R1),   # slot 0
            (e2_idx, +1, L12, R2),   # slot 1
            (e3_idx, -1, L12, R2),   # slot 2
            (e4_idx, -1, L123, R3),  # slot 3
        ]

        # Middle matrices between slots p and q (p < q):
        # middle_{0,1} = Q2 (between slot0's insertion point and slot1's)
        # middle_{0,2} = Q2 (same, since slots 1,2 are at same point)
        # middle_{0,3} = Q2 Q3^{-1}
        # middle_{1,2} = I (slots 1,2 are at same point)
        # middle_{1,3} = Q3^{-1}
        # middle_{2,3} = Q3^{-1}

        middles = {
            (0,1): Q2,
            (0,2): Q2,
            (0,3): Q2 @ Q3inv,
            (1,2): I2,
            (1,3): Q3inv,
            (2,3): Q3inv,
        }

        # Self-terms: for each slot p, each color pair (a,b):
        # d²/dvi_a dvi_b [from this slot] = -(β/N) × sign_p² × Re Tr(L_p basis[a] basis[b] R_p)
        # Note sign_p² = 1 always.
        for p in range(4):
            ep, sp, Lp, Rp = slots[p]
            for a in range(3):
                for b in range(3):
                    val = -(beta/N) * (np.trace(Lp @ basis[a] @ basis[b] @ Rp)).real
                    H[3*ep + a, 3*ep + b] += val

        # Cross-terms: for each pair of slots (p, q) with p < q:
        # The mixed partial d²S/dv_{ep,a} dv_{eq,b}:
        # From the expansion, the ε² coefficient for cross (p,q) contributes to
        # d²/dε² when both are perturbed by ε. For the bilinear H_ij:
        # H_{ep_a, eq_b} += -(β/N) × sp × sq × Re Tr(Lp basis[a] middle_{pq} basis[b] Rq)
        # PLUS the transpose contribution:
        # H_{eq_b, ep_a} += same value
        # Because the Hessian is symmetric.

        for (p, q), mid in middles.items():
            ep, sp, Lp, Rp = slots[p]
            eq, sq, Lq, Rq = slots[q]
            for a in range(3):
                for b in range(3):
                    val = -(beta/N) * sp * sq * (np.trace(Lp @ basis[a] @ mid @ basis[b] @ Rq)).real
                    H[3*ep + a, 3*eq + b] += val
                    H[3*eq + b, 3*ep + a] += val

    return H

# ============================================================
# TEST on 2^4 lattice
# ============================================================
L = 2
d = 4
lat = Lattice(L, d)
print(f"Lattice: {L}^{d}, {lat.n_sites} sites, {lat.n_edges} edges, {lat.n_plaq} plaquettes")
print(f"Hessian size: {3*lat.n_edges} × {3*lat.n_edges}")

# ---- Q = I ----
print("\n" + "="*70)
print("Q = I (all links identity)")
print("="*70)

Q_I = [I2.copy() for _ in range(lat.n_edges)]
H_an = hessian_analytical(lat, Q_I)
H_fd = hessian_fd(lat, Q_I)

err = np.abs(H_an - H_fd).max()
print(f"Max element-wise error (analytical vs FD): {err:.2e}")

evals_an = np.linalg.eigvalsh(H_an)
print(f"Eigenvalue range: [{evals_an.min():.6f}, {evals_an.max():.6f}]")
print(f"Max eigenvalue / (β/2N): {evals_an.max() / 0.25:.6f}")
# Should be 4d = 16 if M convention matches

# ---- Q = iσ₃ ----
print("\n" + "="*70)
print("Q = iσ₃ (all links)")
print("="*70)

Q_is3 = [1j * sigma[2] for _ in range(lat.n_edges)]
H_an2 = hessian_analytical(lat, Q_is3)
H_fd2 = hessian_fd(lat, Q_is3)

err2 = np.abs(H_an2 - H_fd2).max()
print(f"Max element-wise error (analytical vs FD): {err2:.2e}")

evals_an2 = np.linalg.eigvalsh(H_an2)
print(f"Eigenvalue range: [{evals_an2.min():.6f}, {evals_an2.max():.6f}]")
print(f"Max eigenvalue / (β/2N): {evals_an2.max() / 0.25:.6f}")

# ---- Compare with M(Q) ----
print("\n" + "="*70)
print("Building M(Q) operator for comparison")
print("="*70)

def build_M(lat, Q):
    """Build M(Q) matrix: v^T M v = Σ_□ |B_□|²_Kill where |X|²_Kill = -2Tr(X²)."""
    n = 3 * lat.n_edges
    M = np.zeros((n, n))

    for (e1, e2, e3, e4) in lat.plaquettes:
        Q1, Q2, Q3, Q4 = Q[e1], Q[e2], Q[e3], Q[e4]
        Q3inv = Q3.conj().T
        Q4inv = Q4.conj().T

        # B_□ = v_{e1} + Ad_{Q1}(v_{e2}) - Ad_{Q1 Q2 Q3^{-1}}(v_{e3}) - Ad_{U_□}(v_{e4})
        # In the Killing norm: |B|²_Kill = -2Tr(B²)
        #
        # B = Σ_a c_{e1,a} basis[a]
        #   + Σ_a c_{e2,a} Ad_{Q1}(basis[a])
        #   - Σ_a c_{e3,a} Ad_{Q1Q2Q3^{-1}}(basis[a])
        #   - Σ_a c_{e4,a} Ad_{U_□}(basis[a])
        #
        # Ad_Q(X) = QXQ†
        # |B|²_Kill = -2Tr(B²)

        U_plaq = Q1 @ Q2 @ Q3inv @ Q4inv

        # Transport matrices
        T1 = I2.copy()           # identity (no transport for e1)
        T2 = Q1.copy()           # transport for e2
        T3 = Q1 @ Q2 @ Q3inv    # transport for e3 (negative sign)
        T4 = U_plaq              # transport for e4 (negative sign)

        # B = Σ_{edge,a} sign_edge * c_{edge,a} * T_edge basis[a] T_edge†
        # |B|²_Kill = Σ_{(edge_i,a),(edge_j,b)} s_i s_j c_{i,a} c_{j,b} × (-2)Tr(T_i basis[a] T_i† T_j basis[b] T_j†)

        transports = [(e1, +1, T1), (e2, +1, T2), (e3, -1, T3), (e4, -1, T4)]

        for (ei, si, Ti) in transports:
            for (ej, sj, Tj) in transports:
                Tidg = Ti.conj().T
                Tjdg = Tj.conj().T
                for a in range(3):
                    for b in range(3):
                        # -2 Tr(Ti basis[a] Ti† Tj basis[b] Tj†) × si × sj
                        val = -2 * si * sj * (np.trace(Ti @ basis[a] @ Tidg @ Tj @ basis[b] @ Tjdg)).real
                        M[3*ei + a, 3*ej + b] += val

    return M

M_I = build_M(lat, Q_I)
M_is3 = build_M(lat, Q_is3)

evals_M_I = np.linalg.eigvalsh(M_I)
evals_M_is3 = np.linalg.eigvalsh(M_is3)

print(f"M(I) eigenvalue range: [{evals_M_I.min():.4f}, {evals_M_I.max():.4f}]")
print(f"M(iσ₃) eigenvalue range: [{evals_M_is3.min():.4f}, {evals_M_is3.max():.4f}]")

# Check: HessS = (β/2N) M at Q=I?
ratio_I = H_an / (0.25 * M_I + 1e-30)
# Filter where M is nonzero
mask = np.abs(M_I) > 1e-8
if mask.any():
    print(f"\nH/(β/2N·M) at Q=I (nonzero entries): min={ratio_I[mask].min():.4f}, max={ratio_I[mask].max():.4f}")

# At iσ₃
ratio_is3 = H_an2 / (0.25 * M_is3 + 1e-30)
mask2 = np.abs(M_is3) > 1e-8
if mask2.any():
    print(f"H/(β/2N·M) at Q=iσ₃ (nonzero entries): min={ratio_is3[mask2].min():.4f}, max={ratio_is3[mask2].max():.4f}")

# Correction C = M - (2N/β) HessS
C_I = M_I - 4.0 * H_an
C_is3 = M_is3 - 4.0 * H_an2

evals_C_I = np.linalg.eigvalsh(C_I)
evals_C_is3 = np.linalg.eigvalsh(C_is3)

print(f"\nCorrection C(I) eigenvalues: [{evals_C_I.min():.6f}, {evals_C_I.max():.6f}]")
print(f"Correction C(iσ₃) eigenvalues: [{evals_C_is3.min():.6f}, {evals_C_is3.max():.6f}]")

print(f"\n(β/2N)×max_eig(M(I)) = {0.25*evals_M_I.max():.4f}")
print(f"max_eig(HessS(I)) = {evals_an.max():.4f}")
print(f"(β/2N)×max_eig(M(iσ₃)) = {0.25*evals_M_is3.max():.4f}")
print(f"max_eig(HessS(iσ₃)) = {evals_an2.max():.4f}")
