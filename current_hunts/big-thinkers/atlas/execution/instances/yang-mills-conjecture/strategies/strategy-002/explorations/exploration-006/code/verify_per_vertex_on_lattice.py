"""
Verify that the per-vertex formula F_x(R, D, T) matches the actual lattice B-field
computation for staggered modes. Also check the mapping between lattice link variables
and the per-vertex (R_mu, D_{mu,nu}).
"""
import numpy as np
from scipy.linalg import expm
import itertools

np.random.seed(2024)

L = 2
d = 4
N_vertices = L**d
N_edges = d * N_vertices
N_dim = 3 * N_edges

def random_so3():
    v = np.random.randn(3)
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return expm(K)

def vertex_index(x):
    idx = 0
    for i in range(d):
        idx = idx * L + (x[i] % L)
    return idx

def all_vertices():
    return list(itertools.product(range(L), repeat=d))

def edge_index(x, mu):
    return vertex_index(x) * d + mu

def neighbor(x, mu):
    y = list(x)
    y[mu] = (y[mu] + 1) % L
    return tuple(y)

def holonomy(Q, x, mu, nu):
    x_mu = neighbor(x, mu)
    x_nu = neighbor(x, nu)
    return Q[(x, mu)] @ Q[(x_mu, nu)] @ Q[(x_nu, mu)].T @ Q[(x, nu)].T

def compute_Fx_lattice(Q, x, T):
    """Compute F_x from the lattice B-field formula for staggered mode."""
    sx = sum(x) % 2  # parity of vertex x

    Fx = 0
    for mu in range(d):
        for nu in range(mu+1, d):
            # Plaquette (x, mu, nu)
            x_mu = neighbor(x, mu)
            x_nu = neighbor(x, nu)

            # Link variables
            U_e1 = Q[(x, mu)]          # forward link e1
            U_e2 = Q[(x_mu, nu)]       # forward link e2
            U_e3 = Q[(x_nu, mu)]       # forward link e3 (traversed backward)
            U_e4 = Q[(x, nu)]          # forward link e4 (traversed backward)

            # B-field coefficients for general v:
            # B = v_{e1} + Ad(U_{e1}) v_{e2} - Ad(U_{e1}U_{e2}U_{e3}^{-1}) v_{e3} - Ad(U_plaq) v_{e4}
            G1 = np.eye(3)
            G2 = U_e1
            G3 = -(U_e1 @ U_e2 @ U_e3.T)
            G4 = -holonomy(Q, x, mu, nu)

            # Staggered mode: v_{y,alpha} = (-1)^{|y|+alpha} T_alpha
            # Edge e1 = (x, mu): v = (-1)^{|x|+mu} T_mu
            # Edge e2 = (x+mu_hat, nu): v = (-1)^{|x|+1+nu} T_nu = (-1)^{sx+1+nu} T_nu
            # Edge e3 = (x+nu_hat, mu): v = (-1)^{|x|+1+mu} T_mu = (-1)^{sx+1+mu} T_mu
            # Edge e4 = (x, nu): v = (-1)^{|x|+nu} T_nu

            s1 = (-1)**(sx + mu)
            s2 = (-1)**(sx + 1 + nu)
            s3 = (-1)**(sx + 1 + mu)
            s4 = (-1)**(sx + nu)

            v1 = s1 * T[mu]
            v2 = s2 * T[nu]
            v3 = s3 * T[mu]
            v4 = s4 * T[nu]

            B = G1 @ v1 + G2 @ v2 + G3 @ v3 + G4 @ v4
            Fx += np.dot(B, B)

    return Fx

def compute_Fx_formula(R, D_dict, T, sign_struct):
    """Compute F_x from the per-vertex formula.
    sign_struct determines the signs for each plaquette (mu,nu):
    a = (-1)^mu, b = (-1)^{nu+1} for even parity vertex, but adjusted for vertex parity.
    """
    Fx = 0
    for mu in range(d):
        for nu in range(mu+1, d):
            D = D_dict[(mu, nu)]
            a, b = sign_struct[(mu, nu)]

            # B_{mu,nu} = (a*I + b*R_mu*D) T_mu + (-b*R_mu - a*R_mu*D*R_nu^T) T_nu
            # Wait, this depends on the exact sign convention. Let me derive it.
            #
            # The staggered signs for plaquette (x, mu, nu):
            # s1 = (-1)^(sx + mu), s2 = (-1)^(sx+1+nu), s3 = (-1)^(sx+1+mu), s4 = (-1)^(sx+nu)
            #
            # B = s1*G1*T_mu + s2*G2*T_nu + s3*G3*T_mu + s4*G4*T_nu
            #   = (s1*I + s3*G3_hat)*T_mu + (s2*G2 + s4*G4)*T_nu
            #
            # where G3_hat = -U_e1*U_e2*U_e3^T and G4 = -U_plaq
            #
            # With R_mu = U_{x,mu} and D_{mu,nu} = U_{x+mu,nu}:
            # G2 = R_mu = U_{x,mu}
            # G3_hat = -R_mu * D * R_nu^{-T}... wait, not quite.
            #
            # Actually the per-vertex formula maps:
            # R_mu = Q_{x,mu} (base link in direction mu)
            # D_{mu,nu} relates to the cross-plaquette link

            # Let me just compute both and compare.
            pass

    return Fx

def compare_lattice_vs_formula(n_trials=200):
    """Compare F_x from lattice B-field vs the per-vertex formula.
    Key: identify the mapping from lattice links to per-vertex (R, D).
    """
    print("=== Lattice F_x vs Per-Vertex Formula ===")

    verts = all_vertices()
    max_err = 0

    for trial in range(n_trials):
        Q = {}
        for x in verts:
            for mu in range(d):
                Q[(x, mu)] = random_so3()

        T = np.random.randn(4, 3)
        T -= T.mean(axis=0)
        T_norm_sq = np.sum(T**2)

        # Pick a vertex x
        x = verts[trial % N_vertices]
        sx = sum(x) % 2

        # Compute F_x from lattice
        Fx_lattice = compute_Fx_lattice(Q, x, T)

        # Compute F_x from per-vertex formula
        # Map: R_mu = Q_{x,mu}, D_{mu,nu} = holonomy of plaquette at x without base links
        # Actually, the per-vertex formula uses:
        # For plaquette (x, mu, nu):
        # B = (s1*I)*T_mu + (s2*R_mu)*T_nu + (s3*(-R_mu*D_mn*U3^T))*T_mu + (s4*(-U_plaq))*T_nu
        # where D_mn = Q_{x+mu, nu} and U3 = Q_{x+nu, mu}
        # and U_plaq = Q_{x,mu}*Q_{x+mu,nu}*Q_{x+nu,mu}^T*Q_{x,nu}^T

        # The per-vertex formula from E001:
        # F_x = sum_{mu<nu} ||(I + R_mu D) T_mu - (R_mu + R_mu D R_nu^T) T_nu||^2
        # But with SIGNS from the staggered pattern!

        # The signs are: s1 = (-1)^(sx+mu), s2 = (-1)^(sx+1+nu), s3 = (-1)^(sx+1+mu) = -s1, s4 = (-1)^(sx+nu) = -s2

        # B = s1*T_mu + s2*R_mu*T_nu - s1*(R_mu*D_mn*U3^T)*T_mu - s2*U_plaq*T_nu
        # = s1*(I - R_mu*D_mn*U3^T)*T_mu + s2*(R_mu - U_plaq)*T_nu

        # Now, U_plaq = R_mu * D_mn * U3^T * R_nu^T... wait, holonomy is:
        # U = Q_{x,mu} Q_{x+mu,nu} Q_{x+nu,mu}^T Q_{x,nu}^T = R_mu * D_mn * U3^T * R_nu^T
        # So U_plaq = R_mu * D_mn * U3^T * R_nu^T... no:
        # U3 = Q_{x+nu,mu}, so Q_{x+nu,mu}^T = U3^T
        # R_nu = Q_{x,nu}
        # U = R_mu * D_mn * U3^T * R_nu^T

        # G3 = -(R_mu * D_mn * U3^T)   =>  B contribution from e3: s3*G3*T_mu = -s1*(-R_mu*D_mn*U3^T)*T_mu = s1*R_mu*D_mn*U3^T*T_mu
        # Wait, I had G3 = -(U_e1 @ U_e2 @ U_e3.T) = -(R_mu * D_mn * U3^T)
        # and s3 = -s1
        # So s3*G3 = (-s1)*(-(R_mu*D_mn*U3^T)) = s1*R_mu*D_mn*U3^T

        # Similarly, G4 = -U_plaq = -(R_mu*D_mn*U3^T*R_nu^T)
        # s4 = -s2
        # s4*G4 = (-s2)*(-(R_mu*D_mn*U3^T*R_nu^T)) = s2*R_mu*D_mn*U3^T*R_nu^T

        # B = s1*T_mu + s2*R_mu*T_nu + s1*R_mu*D_mn*U3^T*T_mu + s2*R_mu*D_mn*U3^T*R_nu^T*T_nu
        # = s1*(I + R_mu*D_mn*U3^T)*T_mu + s2*(R_mu + R_mu*D_mn*U3^T*R_nu^T)*T_nu
        # = s1*(I + R_mu*D_mn*U3^T)*T_mu + s2*R_mu*(I + D_mn*U3^T*R_nu^T)*T_nu

        # Now, the per-vertex formula uses D = D_mn * U3^T... that's the "cross-link" D!
        # So D_{mu,nu} = Q_{x+mu,nu} * Q_{x+nu,mu}^T
        # And the formula becomes:
        # B = s1*(I + R_mu*D)*T_mu + s2*R_mu*(I + D*R_nu^T)*T_nu

        # |B|^2 = [s1*(I+R_mu D)*T_mu + s2*R_mu*(I+D R_nu^T)*T_nu]^2
        # Since s1, s2 are just ±1, |B|^2 is the same as
        # |(I+R_mu D)*T_mu|^2 + |R_mu*(I+D R_nu^T)*T_nu|^2 + 2*s1*s2*cross
        # = |(I+R_mu D)*T_mu|^2 + |(I+D R_nu^T)*T_nu|^2 + 2*s1*s2*T_mu^T*(I+R_mu D)^T*R_mu*(I+D R_nu^T)*T_nu

        Fx_formula = 0
        for mu in range(d):
            for nu in range(mu+1, d):
                x_mu = neighbor(x, mu)
                x_nu = neighbor(x, nu)

                R_mu_val = Q[(x, mu)]
                R_nu_val = Q[(x, nu)]
                D_mn = Q[(x_mu, nu)] @ Q[(x_nu, mu)].T  # cross-link

                s1 = (-1)**(sx + mu)
                s2 = (-1)**(sx + 1 + nu)

                A = np.eye(3) + R_mu_val @ D_mn
                C = R_mu_val @ (np.eye(3) + D_mn @ R_nu_val.T)

                B_vec = s1 * A @ T[mu] + s2 * C @ T[nu]
                Fx_formula += np.dot(B_vec, B_vec)

        err = abs(Fx_lattice - Fx_formula)
        max_err = max(max_err, err)

        if trial < 5:
            print(f"  Trial {trial} (vertex {x}): Fx_lattice={Fx_lattice:.6f}, Fx_formula={Fx_formula:.6f}, err={err:.2e}")

    print(f"\n  Max |lattice - formula|: {max_err:.2e}")
    print(f"  Status: {'VERIFIED' if max_err < 1e-10 else 'FAILED'}")

    # Now check: the per-vertex formula from the proof uses specific sign conventions.
    # The proof's formula is:
    # F_x = sum_{mu<nu} ||(I + R_mu D) T_mu - (R_mu + R_mu D R_nu^T) T_nu||^2
    # Let's check if this matches (ignoring sign structure).

    print("\n  Checking sign structure consistency...")
    max_err2 = 0
    for trial in range(200):
        Q = {}
        for x in verts:
            for mu in range(d):
                Q[(x, mu)] = random_so3()

        T = np.random.randn(4, 3)
        T -= T.mean(axis=0)

        x = verts[0]  # Even parity vertex (0,0,0,0)
        sx = sum(x) % 2  # = 0

        Fx_lattice = compute_Fx_lattice(Q, x, T)

        # The proof's per-vertex formula (from E001):
        # For even parity vertex, s1 = (-1)^mu, s2 = (-1)^{nu+1}
        # The combination s1*s2 = (-1)^{mu+nu+1} determines active/inactive
        Fx_proof = 0
        for mu in range(d):
            for nu in range(mu+1, d):
                x_mu = neighbor(x, mu)
                x_nu = neighbor(x, nu)

                R_mu_val = Q[(x, mu)]
                R_nu_val = Q[(x, nu)]
                D_mn = Q[(x_mu, nu)] @ Q[(x_nu, mu)].T

                # For even vertex: s1 = (-1)^mu, s2 = (-1)^{1+nu}
                s1 = (-1)**mu
                s2 = (-1)**(1 + nu)

                A = np.eye(3) + R_mu_val @ D_mn
                C = R_mu_val @ (np.eye(3) + D_mn @ R_nu_val.T)

                B_vec = s1 * A @ T[mu] + s2 * C @ T[nu]
                Fx_proof += np.dot(B_vec, B_vec)

        err2 = abs(Fx_lattice - Fx_proof)
        max_err2 = max(max_err2, err2)

    print(f"  Max error (even vertex, proof signs): {max_err2:.2e}")
    print(f"  Status: {'VERIFIED' if max_err2 < 1e-10 else 'MISMATCH'}")

    return max_err < 1e-10

if __name__ == "__main__":
    compare_lattice_vs_formula()
