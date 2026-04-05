"""
Quick gradient ascent on λ_max(M(Q)) — fewer steps, just to confirm convergence.

Uses coordinate ascent: for each edge, find the best su(2) direction and take a step.
"""

import numpy as np
import time

# ====================== SU(2) Utilities ======================

def random_su2():
    v = np.random.randn(4)
    v /= np.linalg.norm(v)
    a, b, c, d = v
    return np.array([[a + 1j*b, c + 1j*d], [-c + 1j*d, a - 1j*b]])

def su2_exp(A_vec):
    theta = np.linalg.norm(A_vec)
    if theta < 1e-15:
        return np.eye(2, dtype=complex)
    n = A_vec / theta
    ct, st = np.cos(theta/2), np.sin(theta/2)
    return np.array([[ct + 1j*st*n[2], st*(1j*n[0] + n[1])], [st*(1j*n[0] - n[1]), ct - 1j*st*n[2]]])

def su2_near_identity(eps):
    c = np.random.randn(3); c = c/np.linalg.norm(c)*eps
    return su2_exp(c)

def adjoint_action(U, A):
    return U @ A @ np.conj(U).T

def su2_basis():
    s1 = np.array([[0,1],[1,0]], dtype=complex)
    s2 = np.array([[0,-1j],[1j,0]], dtype=complex)
    s3 = np.array([[1,0],[0,-1]], dtype=complex)
    return [1j*s1/2, 1j*s2/2, 1j*s3/2]

def su2_to_vec(A, basis):
    return np.array([-2*np.trace(b@A).real for b in basis])

def ad_matrix_fn(U, basis):
    R = np.zeros((3,3))
    for j in range(3):
        R[:,j] = su2_to_vec(adjoint_action(U, basis[j]), basis)
    return R

class Lattice:
    def __init__(self, L, d):
        self.L, self.d = L, d
        self.n_sites = L**d
        self.n_edges = d * self.n_sites
        self.n_plaq = d*(d-1)//2 * self.n_sites
        self.dim_su = 3
        self.dim = 3 * self.n_edges

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
                    xm = self.shifted_site(x, mu)
                    xn = self.shifted_site(x, nu)
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
    bound = 4*d

    print(f"Quick gradient ascent on λ_max(M(Q)), L={L}, d={d}")
    print(f"Target: 4d = {bound}")
    print()

    for trial in range(10):
        Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
        for e in range(lat.n_edges):
            Q[e] = su2_near_identity(2.0)  # Start far from identity

        t0 = time.time()
        lam_history = []

        for step in range(15):
            M_Q = build_M(lat, Q, basis)
            eigs, vecs = np.linalg.eigh(M_Q)
            lam = eigs[-1]
            v = vecs[:, -1]
            lam_history.append(float(lam))

            # Coordinate ascent: for each edge, find best perturbation
            delta = 1e-4
            for e in range(lat.n_edges):
                best_grad = np.zeros(3)
                for a in range(3):
                    Av = np.zeros(3); Av[a] = delta
                    Qp = Q.copy(); Qp[e] = su2_exp(Av)@Q[e]
                    Mp = build_M(lat, Qp, basis)
                    best_grad[a] = (v@Mp@v - lam)/delta

                if np.linalg.norm(best_grad) > 1e-10:
                    Q[e] = su2_exp(0.03*best_grad)@Q[e]
                    u,s,vh = np.linalg.svd(Q[e]); Q[e] = u@vh

        elapsed = time.time() - t0

        # Final check
        M_final = build_M(lat, Q, basis)
        lam_final = np.linalg.eigvalsh(M_final)[-1]
        lam_history.append(float(lam_final))

        # Plaq holonomy
        max_hol = 0.0
        for (e1,e2,e3,e4,x,mu,nu) in lat.plaquettes():
            Up = Q[e1]@Q[e2]@np.conj(Q[e3]).T@np.conj(Q[e4]).T
            max_hol = max(max_hol, np.linalg.norm(Up - np.eye(2)))

        print(f"  Trial {trial+1}: start={lam_history[0]:.4f} → final={lam_final:.8f}, "
              f"gap={bound-lam_final:.8f}, max_hol={max_hol:.4f}, time={elapsed:.1f}s")

    print()
    print("Summary: All trials should plateau at or below 4d = 16.")
    print("If any trial reaches > 16, that would be a counterexample to λ_max ≤ 4d.")

if __name__ == '__main__':
    main()
