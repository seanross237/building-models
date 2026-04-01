"""
Analytical verification: Tr(M(Q)) = Tr(M(I)) for all Q.

Proof: Tr(M(Q)) = ∑_□ ∑_{e∈□} Tr(R_e^T R_e)
     = ∑_□ ∑_{e∈□} Tr(I_3)   [because each R_e ∈ O(3) is orthogonal]
     = ∑_□ × 4 × 3 = 12 × n_plaq

Each R_e is ±Ad_P for some P ∈ SU(2), so R_e^T R_e = Ad_P^T Ad_P = I_3 (orthogonal).

This means Tr(R(Q)) = Tr(M(Q)) - Tr(M(I)) = 0 for all Q.

Also verify: higher traces. Is Tr(M(Q)²) independent of Q? (This would give
a stronger constraint on eigenvalue redistribution.)
"""

import numpy as np

def random_su2():
    v = np.random.randn(4); v /= np.linalg.norm(v)
    a,b,c,d = v
    return np.array([[a+1j*b, c+1j*d],[-c+1j*d, a-1j*b]])

def su2_exp(A_vec):
    theta = np.linalg.norm(A_vec)
    if theta < 1e-15: return np.eye(2, dtype=complex)
    n = A_vec/theta; ct,st = np.cos(theta/2),np.sin(theta/2)
    return np.array([[ct+1j*st*n[2], st*(1j*n[0]+n[1])],[st*(1j*n[0]-n[1]), ct-1j*st*n[2]]])

def su2_near_identity(eps):
    c = np.random.randn(3); c = c/np.linalg.norm(c)*eps; return su2_exp(c)

def adjoint_action(U, A): return U@A@np.conj(U).T

def su2_basis():
    s1 = np.array([[0,1],[1,0]], dtype=complex)
    s2 = np.array([[0,-1j],[1j,0]], dtype=complex)
    s3 = np.array([[1,0],[0,-1]], dtype=complex)
    return [1j*s1/2, 1j*s2/2, 1j*s3/2]

def su2_to_vec(A, basis):
    return np.array([-2*np.trace(b@A).real for b in basis])

def ad_matrix_fn(U, basis):
    R = np.zeros((3,3))
    for j in range(3): R[:,j] = su2_to_vec(adjoint_action(U, basis[j]), basis)
    return R

class Lattice:
    def __init__(self, L, d):
        self.L, self.d = L, d
        self.n_sites = L**d
        self.n_edges = d*self.n_sites
        self.n_plaq = d*(d-1)//2*self.n_sites
        self.dim = 3*self.n_edges

    def site_index(self, coords):
        idx = 0
        for i in range(self.d): idx = idx*self.L + (coords[i]%self.L)
        return idx

    def site_coords(self, idx):
        coords = []
        for i in range(self.d-1,-1,-1): coords.append(idx%self.L); idx//=self.L
        return list(reversed(coords))

    def edge_index(self, x, mu): return x*self.d + mu

    def shifted_site(self, x, mu, s=+1):
        c = self.site_coords(x); c[mu] = (c[mu]+s)%self.L
        return self.site_index(c)

    def plaquettes(self):
        P = []
        for x in range(self.n_sites):
            for mu in range(self.d):
                for nu in range(mu+1, self.d):
                    xm = self.shifted_site(x, mu); xn = self.shifted_site(x, nu)
                    P.append((self.edge_index(x,mu), self.edge_index(xm,nu),
                              self.edge_index(xn,mu), self.edge_index(x,nu), x, mu, nu))
        return P

def build_M(lat, Q, basis):
    dim = lat.dim
    M = np.zeros((dim, dim))
    for (e1,e2,e3,e4,x,mu,nu) in lat.plaquettes():
        Q1 = Q[e1]; Q12 = Q1@Q[e2]
        Q123i = Q12@np.conj(Q[e3]).T; Up = Q123i@np.conj(Q[e4]).T
        R1 = np.eye(3)
        R2 = ad_matrix_fn(Q1, basis)
        R3 = -ad_matrix_fn(Q123i, basis)
        R4 = -ad_matrix_fn(Up, basis)
        for ei,Ri in [(e1,R1),(e2,R2),(e3,R3),(e4,R4)]:
            for ej,Rj in [(e1,R1),(e2,R2),(e3,R3),(e4,R4)]:
                M[3*ei:3*ei+3, 3*ej:3*ej+3] += Ri.T@Rj
    return M

def main():
    np.random.seed(42)
    basis = su2_basis()
    L, d = 2, 4
    lat = Lattice(L, d)

    Q_id = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    for e in range(lat.n_edges): Q_id[e] = np.eye(2)
    M_I = build_M(lat, Q_id, basis)

    print("Trace analysis of M(Q)")
    print("="*60)
    print()

    tr_I = np.trace(M_I)
    tr2_I = np.trace(M_I @ M_I)
    eigs_I = np.sort(np.linalg.eigvalsh(M_I))
    print(f"M(I): Tr = {tr_I:.4f}, Tr(M²) = {tr2_I:.4f}")
    print(f"  sum(λ²) = {np.sum(eigs_I**2):.4f}")
    print()

    print(f"{'Config':<25s} {'Tr(M)':<12s} {'Tr(M²)':<14s} {'Tr(M³)':<14s} {'Tr(R²)':<14s}")
    print("-"*80)

    for trial in range(15):
        if trial < 5:
            name = f"Random Haar #{trial+1}"
            Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
            for e in range(lat.n_edges): Q[e] = random_su2()
        elif trial < 10:
            name = f"Near-I ε={0.1*(trial-4):.1f}"
            Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
            eps = 0.1*(trial-4)
            for e in range(lat.n_edges): Q[e] = su2_near_identity(eps)
        else:
            name = f"Pure gauge #{trial-9}"
            g = [random_su2() for _ in range(lat.n_sites)]
            Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
            for x in range(lat.n_sites):
                for mu in range(d):
                    e = lat.edge_index(x, mu)
                    y = lat.shifted_site(x, mu)
                    Q[e] = g[x]@np.conj(g[y]).T

        M_Q = build_M(lat, Q, basis)
        R_Q = M_Q - M_I

        tr_M = np.trace(M_Q)
        tr_M2 = np.trace(M_Q @ M_Q)
        tr_M3 = np.trace(M_Q @ M_Q @ M_Q)
        tr_R2 = np.trace(R_Q @ R_Q)

        print(f"{name:<25s} {tr_M:<12.4f} {tr_M2:<14.4f} {tr_M3:<14.4f} {tr_R2:<14.4f}")

    print()
    print(f"Reference M(I): Tr = {tr_I:.4f}, Tr(M²) = {tr2_I:.4f}")
    print()
    print("Key question: Is Tr(M²) Q-independent? If yes, Tr(R²) = Tr(M²) - Tr(M_I²) + 2Tr(M_I R)")
    print("  = Tr(M²) - Tr(M_I²) (since Tr(M_I R) = 0 for pure gauge, etc.)")
    print()

    # Check if Tr(M(Q)²) varies
    vals = []
    for _ in range(50):
        Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
        for e in range(lat.n_edges): Q[e] = random_su2()
        M_Q = build_M(lat, Q, basis)
        vals.append(np.trace(M_Q @ M_Q))

    print(f"Tr(M²) over 50 random Haar:")
    print(f"  Mean = {np.mean(vals):.4f}")
    print(f"  Std  = {np.std(vals):.4f}")
    print(f"  Min  = {np.min(vals):.4f}")
    print(f"  Max  = {np.max(vals):.4f}")
    print(f"  M(I): {tr2_I:.4f}")
    print()
    print("=> Tr(M²) is NOT Q-independent (varies with Q).")
    print("   This means eigenvalue redistribution is not constrained by Tr(M²).")

if __name__ == '__main__':
    main()
