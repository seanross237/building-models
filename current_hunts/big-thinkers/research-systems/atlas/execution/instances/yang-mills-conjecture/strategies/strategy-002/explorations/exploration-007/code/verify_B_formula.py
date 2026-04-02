"""
CRITICAL: Verify whether B_p(A) as coded gives the correct linearization
of the plaquette holonomy.

Two possible formulas for the linearized curvature:

FORMULA A (code): B_p(A) = A_1 + Q_1 A_2 - Q_1 Q_2 Q_3^{-1} A_3 - U_p A_4
FORMULA B (derived): B_p(A) = A_1 + Q_1 Q_2 A_2 - Q_1 Q_2 A_3 - Q_1 Q_2 Q_3^{-1} A_4

Test: Compute dU_p/dε numerically and extract the B-field vector.
"""
import numpy as np
from scipy.linalg import expm
import itertools

np.random.seed(42)

L = 2; d = 4

def skew(v):
    return np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])

def unskew(S):
    """Extract vector from skew-symmetric matrix."""
    return np.array([S[2,1], S[0,2], S[1,0]])

VERTICES = list(itertools.product(range(L), repeat=d))

def vertex_index(x):
    idx = 0
    for i in range(d):
        idx = idx * L + (x[i] % L)
    return idx

def edge_index(x, mu):
    return vertex_index(x) * d + mu

def neighbor(x, mu):
    y = list(x)
    y[mu] = (y[mu] + 1) % L
    return tuple(y)

# Pick a specific plaquette and test the linearization
x = (0, 0, 0, 0)
mu, nu = 0, 1
xmu = neighbor(x, mu)
xnu = neighbor(x, nu)

print("=" * 70)
print("VERIFYING B-FIELD LINEARIZATION FORMULA")
print(f"Plaquette: x={x}, mu={mu}, nu={nu}")
print("=" * 70)

# Generate random gauge field
Q = {(v, m): expm(skew(np.random.randn(3) * 2))
     for v in VERTICES for m in range(d)}

Q1 = Q[(x, mu)]
Q2 = Q[(xmu, nu)]
Q3 = Q[(xnu, mu)]
Q4 = Q[(x, nu)]

# Compute U_p
U_p = Q1 @ Q2 @ Q3.T @ Q4.T

print(f"Q1 = Q({x},{mu})")
print(f"Q2 = Q({xmu},{nu})")
print(f"Q3 = Q({xnu},{mu})")
print(f"Q4 = Q({x},{nu})")
print(f"U_p = Q1 Q2 Q3^T Q4^T, Tr(U_p) = {np.trace(U_p):.4f}")

# Test each edge perturbation
eps = 1e-7

for edge_label, edge_pos, Q_key in [("e1", 1, (x, mu)),
                                      ("e2", 2, (xmu, nu)),
                                      ("e3", 3, (xnu, mu)),
                                      ("e4", 4, (x, nu))]:
    print(f"\n--- Perturbing {edge_label} = Q{Q_key} ---")

    for a_idx in range(3):
        a = np.zeros(3)
        a[a_idx] = 1.0

        # Numerical: U_p(+eps) - U_p(-eps) = 2*eps * dU_p/da
        Q_plus = dict(Q)
        Q_plus[Q_key] = Q[Q_key] @ expm(eps * skew(a))
        U_plus = Q_plus[(x,mu)] @ Q_plus[(xmu,nu)] @ Q_plus[(xnu,mu)].T @ Q_plus[(x,nu)].T

        Q_minus = dict(Q)
        Q_minus[Q_key] = Q[Q_key] @ expm(-eps * skew(a))
        U_minus = Q_minus[(x,mu)] @ Q_minus[(xmu,nu)] @ Q_minus[(xnu,mu)].T @ Q_minus[(x,nu)].T

        dU_numerical = (U_plus - U_minus) / (2 * eps)

        # dU_p should be of the form [b]_× U_p for some b (the B-field vector)
        # So b_× = dU_p U_p^{-1} = dU_p U_p^T
        b_matrix = dU_numerical @ U_p.T
        # b_matrix should be skew-symmetric
        b_numerical = unskew(b_matrix)

        # Formula A (code): G_j * a
        if edge_pos == 1:
            G_A = np.eye(3)  # G1 = I
        elif edge_pos == 2:
            G_A = Q1  # G2 = Q1
        elif edge_pos == 3:
            G_A = -(Q1 @ Q2 @ Q3.T)  # G3 = -(Q1 Q2 Q3^{-1})
        elif edge_pos == 4:
            G_A = -U_p  # G4 = -U_p

        b_formula_A = G_A @ a

        # Formula B (derived): different G matrices
        if edge_pos == 1:
            G_B = np.eye(3)
        elif edge_pos == 2:
            G_B = Q1 @ Q2
        elif edge_pos == 3:
            G_B = -(Q1 @ Q2)
        elif edge_pos == 4:
            G_B = -(Q1 @ Q2 @ Q3.T)

        b_formula_B = G_B @ a

        err_A = np.linalg.norm(b_numerical - b_formula_A)
        err_B = np.linalg.norm(b_numerical - b_formula_B)

        if a_idx == 0:  # Print for first component only to keep output manageable
            print(f"  a = e_{a_idx}:")
            print(f"    Numerical b: [{b_numerical[0]:.6f}, {b_numerical[1]:.6f}, {b_numerical[2]:.6f}]")
            print(f"    Formula A:   [{b_formula_A[0]:.6f}, {b_formula_A[1]:.6f}, {b_formula_A[2]:.6f}] err={err_A:.2e}")
            print(f"    Formula B:   [{b_formula_B[0]:.6f}, {b_formula_B[1]:.6f}, {b_formula_B[2]:.6f}] err={err_B:.2e}")

        # Check which formula is correct
        if err_A < 1e-5 and err_B > 1e-5:
            if a_idx == 0:
                print(f"    => FORMULA A (code) is correct")
        elif err_B < 1e-5 and err_A > 1e-5:
            if a_idx == 0:
                print(f"    => FORMULA B (derived) is correct")
        elif err_A < 1e-5 and err_B < 1e-5:
            if a_idx == 0:
                print(f"    => Both formulas correct (agree at Q=I or special case)")
        else:
            if a_idx == 0:
                print(f"    => NEITHER formula matches! Error A={err_A:.2e}, B={err_B:.2e}")

# ============================================================
# Summary: which formula is correct?
# ============================================================
print(f"\n{'='*70}")
print("COMPREHENSIVE TEST: 100 random Q, all plaquettes, all edges")
print("="*70)

max_err_A = 0
max_err_B = 0
n_tests = 0

for trial in range(20):
    Q = {(v, m): expm(skew(np.random.randn(3) * 2))
         for v in VERTICES for m in range(d)}

    for x in VERTICES:
        for mu in range(d):
            for nu in range(mu+1, d):
                xmu = neighbor(x, mu)
                xnu = neighbor(x, nu)
                Q1 = Q[(x, mu)]
                Q2 = Q[(xmu, nu)]
                Q3 = Q[(xnu, mu)]
                Q4 = Q[(x, nu)]
                U_p = Q1 @ Q2 @ Q3.T @ Q4.T

                for edge_pos, Q_key in [(1, (x,mu)), (2, (xmu,nu)),
                                         (3, (xnu,mu)), (4, (x,nu))]:
                    for a_idx in range(3):
                        a = np.zeros(3)
                        a[a_idx] = 1.0

                        # Numerical
                        Qp = dict(Q)
                        Qp[Q_key] = Q[Q_key] @ expm(eps * skew(a))
                        Up = Qp[(x,mu)] @ Qp[(xmu,nu)] @ Qp[(xnu,mu)].T @ Qp[(x,nu)].T
                        Qm = dict(Q)
                        Qm[Q_key] = Q[Q_key] @ expm(-eps * skew(a))
                        Um = Qm[(x,mu)] @ Qm[(xmu,nu)] @ Qm[(xnu,mu)].T @ Qm[(x,nu)].T
                        dU = (Up - Um) / (2*eps)
                        b_num = unskew(dU @ U_p.T)

                        # Formula A
                        if edge_pos == 1: G_A = np.eye(3)
                        elif edge_pos == 2: G_A = Q1
                        elif edge_pos == 3: G_A = -(Q1 @ Q2 @ Q3.T)
                        elif edge_pos == 4: G_A = -U_p
                        b_A = G_A @ a

                        # Formula B
                        if edge_pos == 1: G_B = np.eye(3)
                        elif edge_pos == 2: G_B = Q1 @ Q2
                        elif edge_pos == 3: G_B = -(Q1 @ Q2)
                        elif edge_pos == 4: G_B = -(Q1 @ Q2 @ Q3.T)
                        b_B = G_B @ a

                        max_err_A = max(max_err_A, np.linalg.norm(b_num - b_A))
                        max_err_B = max(max_err_B, np.linalg.norm(b_num - b_B))
                        n_tests += 1

print(f"  {n_tests} tests completed")
print(f"  Formula A (code): max error = {max_err_A:.2e}")
print(f"  Formula B (derived): max error = {max_err_B:.2e}")

if max_err_A < 1e-4 and max_err_B > 0.01:
    print(f"\n  RESULT: Formula A (code) is CORRECT. Formula B is WRONG.")
    print(f"  The code's M(Q) correctly computes the B-field norm squared.")
elif max_err_B < 1e-4 and max_err_A > 0.01:
    print(f"\n  RESULT: Formula B (derived) is CORRECT. Formula A (code) is WRONG.")
    print(f"  The code's M(Q) uses incorrect G matrices!")
elif max_err_A < 1e-4 and max_err_B < 1e-4:
    print(f"\n  RESULT: Both formulas are correct (they agree).")
else:
    print(f"\n  RESULT: NEITHER formula is correct!")

# ============================================================
# If code is correct, then the Hessian test discrepancy needs explanation
# ============================================================
print(f"\n{'='*70}")
print("EXPLAINING HESSIAN DISCREPANCY")
print("="*70)
print("""
The Wilson action Hessian d²S/dA² has TWO contributions:
1. The "B-field squared" part: sum_p B_p^T B_p (what the code computes)
2. The "curvature correction": -sum_p (Tr(U_p) terms from d²exp/dε²)

The full Hessian is:
  H(Q) = M_BtB(Q) + M_curvature(Q)

where M_BtB = sum B_p^T B_p (always PSD) and M_curvature involves
the second derivative of the exponential map.

At Q=I: U_p = I, and the curvature correction is:
  M_curv(I) = sum_p [3I - R_p] (per diagonal block, where R_p involves
  the cyclic reordering of the plaquette)

This explains why M_BtB(I) ≠ H(I) in general, but the eigenvalue
structure might still match after accounting for both terms.
""")

# Compute the curvature correction numerically
Q_test = {(v, m): expm(skew(np.random.randn(3)))
          for v in VERTICES for m in range(d)}

# Build M_BtB
N_dim = 3 * d * len(VERTICES)
M_BtB = np.zeros((N_dim, N_dim))
for x in VERTICES:
    for mu in range(d):
        for nu in range(mu+1, d):
            xmu = neighbor(x, mu)
            xnu = neighbor(x, nu)
            Q1 = Q_test[(x, mu)]
            Q2 = Q_test[(xmu, nu)]
            Q3 = Q_test[(xnu, mu)]
            Q4 = Q_test[(x, nu)]
            U_p = Q1 @ Q2 @ Q3.T @ Q4.T
            G1 = np.eye(3)
            G2 = Q1
            G3 = -(Q1 @ Q2 @ Q3.T)
            G4 = -U_p
            idx1 = 3 * edge_index(x, mu)
            idx2 = 3 * edge_index(xmu, nu)
            idx3 = 3 * edge_index(xnu, mu)
            idx4 = 3 * edge_index(x, nu)
            edges = [(idx1, G1), (idx2, G2), (idx3, G3), (idx4, G4)]
            for (ia, Ga) in edges:
                for (ib, Gb) in edges:
                    M_BtB[ia:ia+3, ib:ib+3] += Ga.T @ Gb

eigs_BtB = np.sort(np.linalg.eigvalsh(M_BtB))

# Build numerical Hessian for comparison
def wilson_action_q(Q):
    S = 0
    for x in VERTICES:
        for mu in range(d):
            for nu in range(mu+1, d):
                xmu = neighbor(x, mu)
                xnu = neighbor(x, nu)
                U = Q[(x,mu)] @ Q[(xmu,nu)] @ Q[(xnu,mu)].T @ Q[(x,nu)].T
                S += 3 - np.trace(U)
    return S

print("Building numerical Hessian (this takes a minute)...")
eps_h = 1e-5
H_num = np.zeros((N_dim, N_dim))
S0 = wilson_action_q(Q_test)

all_edges = [(x, mu) for x in VERTICES for mu in range(d)]

for i, (x1, mu1) in enumerate(all_edges):
    for a in range(3):
        row = 3*i + a
        avec = np.zeros(3); avec[a] = 1.0

        Qp = dict(Q_test); Qp[(x1,mu1)] = Q_test[(x1,mu1)] @ expm(eps_h * skew(avec))
        Qm = dict(Q_test); Qm[(x1,mu1)] = Q_test[(x1,mu1)] @ expm(-eps_h * skew(avec))
        H_num[row, row] = (wilson_action_q(Qp) - 2*S0 + wilson_action_q(Qm)) / eps_h**2

        for j in range(i, len(all_edges)):
            x2, mu2 = all_edges[j]
            for b in range(3):
                col = 3*j + b
                if col <= row: continue
                bvec = np.zeros(3); bvec[b] = 1.0

                Qpp = dict(Q_test)
                Qpp[(x1,mu1)] = Q_test[(x1,mu1)] @ expm(eps_h * skew(avec))
                Qpp[(x2,mu2)] = Qpp[(x2,mu2)] @ expm(eps_h * skew(bvec))
                Qpm = dict(Q_test)
                Qpm[(x1,mu1)] = Q_test[(x1,mu1)] @ expm(eps_h * skew(avec))
                Qpm[(x2,mu2)] = Qpm[(x2,mu2)] @ expm(-eps_h * skew(bvec))
                Qmp = dict(Q_test)
                Qmp[(x1,mu1)] = Q_test[(x1,mu1)] @ expm(-eps_h * skew(avec))
                Qmp[(x2,mu2)] = Qmp[(x2,mu2)] @ expm(eps_h * skew(bvec))
                Qmm = dict(Q_test)
                Qmm[(x1,mu1)] = Q_test[(x1,mu1)] @ expm(-eps_h * skew(avec))
                Qmm[(x2,mu2)] = Qmm[(x2,mu2)] @ expm(-eps_h * skew(bvec))

                val = (wilson_action_q(Qpp) - wilson_action_q(Qpm) - wilson_action_q(Qmp) + wilson_action_q(Qmm)) / (4*eps_h**2)
                H_num[row, col] = val
                H_num[col, row] = val

eigs_H = np.sort(np.linalg.eigvalsh(H_num))

# Curvature correction = H - M_BtB
M_curv = H_num - M_BtB
eigs_curv = np.sort(np.linalg.eigvalsh(M_curv))

print(f"\n  M_BtB eigenvalues: [{eigs_BtB[0]:.4f}, ..., {eigs_BtB[-1]:.4f}]")
print(f"  Hessian eigenvalues: [{eigs_H[0]:.4f}, ..., {eigs_H[-1]:.4f}]")
print(f"  Curvature correction eigenvalues: [{eigs_curv[0]:.4f}, ..., {eigs_curv[-1]:.4f}]")
print(f"  Tr(M_BtB) = {np.trace(M_BtB):.2f}")
print(f"  Tr(H) = {np.trace(H_num):.2f}")
print(f"  Tr(M_curv) = {np.trace(M_curv):.2f}")
