"""
Build the CORRECT M(Q) = sum_p C_p^T C_p where C_p uses the correct
B-field formula (with Q_1 factor removed from norm):

C_p(a) = a_1 + Q_2 a_2 - Q_2 a_3 - Q_2 Q_3^{-1} a_4

where edges are:
e1 = (x, mu), e2 = (x+mu, nu), e3 = (x+nu, mu), e4 = (x, nu)
Q_2 = Q_{x+mu,nu}, Q_3 = Q_{x+nu,mu}

Compare with the INCORRECT formula used in previous explorations:
B_p(a) = a_1 + Q_1 a_2 - Q_1 Q_2 Q_3^{-1} a_3 - U_p a_4
"""
import numpy as np
from scipy.linalg import expm
import itertools
import time

np.random.seed(42)

L = 2; d = 4
N_vertices = L**d
N_edges = d * N_vertices
N_dim = 3 * N_edges

def vertex_index(x):
    idx = 0
    for i in range(d):
        idx = idx * L + (x[i] % L)
    return idx

VERTICES = list(itertools.product(range(L), repeat=d))

def edge_index(x, mu):
    return vertex_index(x) * d + mu

def neighbor(x, mu):
    y = list(x)
    y[mu] = (y[mu] + 1) % L
    return tuple(y)

def skew(v):
    return np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])

def build_correct_M(Q):
    """Build CORRECT M(Q) = sum_p C_p^T C_p.

    C_p(a) = a_{e1} + Q_2 a_{e2} - Q_2 a_{e3} - Q_2 Q_3^{-1} a_{e4}

    where Q_2 = Q(x+mu, nu) and Q_3 = Q(x+nu, mu).
    """
    M = np.zeros((N_dim, N_dim))
    for x in VERTICES:
        for mu in range(d):
            for nu in range(mu+1, d):
                xmu = neighbor(x, mu)
                xnu = neighbor(x, nu)
                Q2 = Q[(xmu, nu)]
                Q3 = Q[(xnu, mu)]

                G1 = np.eye(3)
                G2 = Q2
                G3 = -Q2
                G4 = -(Q2 @ Q3.T)

                idx1 = 3 * edge_index(x, mu)
                idx2 = 3 * edge_index(xmu, nu)
                idx3 = 3 * edge_index(xnu, mu)
                idx4 = 3 * edge_index(x, nu)

                edges = [(idx1, G1), (idx2, G2), (idx3, G3), (idx4, G4)]
                for (ia, Ga) in edges:
                    for (ib, Gb) in edges:
                        M[ia:ia+3, ib:ib+3] += Ga.T @ Gb
    return M

def build_old_M(Q):
    """Build OLD (incorrect) M(Q) from previous explorations."""
    M = np.zeros((N_dim, N_dim))
    for x in VERTICES:
        for mu in range(d):
            for nu in range(mu+1, d):
                xmu = neighbor(x, mu)
                xnu = neighbor(x, nu)
                Q1 = Q[(x, mu)]
                Q2 = Q[(xmu, nu)]
                Q3 = Q[(xnu, mu)]
                Q4 = Q[(x, nu)]
                U = Q1 @ Q2 @ Q3.T @ Q4.T

                G1 = np.eye(3)
                G2 = Q1
                G3 = -(Q1 @ Q2 @ Q3.T)
                G4 = -U

                idx1 = 3 * edge_index(x, mu)
                idx2 = 3 * edge_index(xmu, nu)
                idx3 = 3 * edge_index(xnu, mu)
                idx4 = 3 * edge_index(x, nu)

                edges = [(idx1, G1), (idx2, G2), (idx3, G3), (idx4, G4)]
                for (ia, Ga) in edges:
                    for (ib, Gb) in edges:
                        M[ia:ia+3, ib:ib+3] += Ga.T @ Gb
    return M

# ============================================================
# Test 1: Both formulas agree at Q=I
# ============================================================
print("=" * 70)
print("TEST 1: Agreement at Q=I")
print("=" * 70)

Q_id = {(x, mu): np.eye(3) for x in VERTICES for mu in range(d)}
M_old = build_old_M(Q_id)
M_new = build_correct_M(Q_id)

print(f"  Max |M_old(I) - M_new(I)|: {np.max(np.abs(M_old - M_new)):.2e}")
eigs_old = np.sort(np.linalg.eigvalsh(M_old))
eigs_new = np.sort(np.linalg.eigvalsh(M_new))
print(f"  Old eigenvalues at I: {[f'{e:.1f}' for e in sorted(set(np.round(eigs_old)))]}")
print(f"  New eigenvalues at I: {[f'{e:.1f}' for e in sorted(set(np.round(eigs_new)))]}")

# ============================================================
# Test 2: Compare eigenvalues for random Q
# ============================================================
print(f"\n{'='*70}")
print("TEST 2: Eigenvalue comparison for random Q")
print("="*70)

for trial in range(10):
    Q = {(x, mu): expm(skew(np.random.randn(3)))
         for x in VERTICES for mu in range(d)}
    M_old = build_old_M(Q)
    M_new = build_correct_M(Q)
    eigs_old = np.linalg.eigvalsh(M_old)
    eigs_new = np.linalg.eigvalsh(M_new)
    print(f"  Trial {trial}: old_max={max(eigs_old):.4f}, new_max={max(eigs_new):.4f}, "
          f"Tr_old={np.trace(M_old):.1f}, Tr_new={np.trace(M_new):.1f}")

# ============================================================
# Test 3: Large-scale test of CORRECT M(Q) ≤ 16
# ============================================================
print(f"\n{'='*70}")
print("TEST 3: Is lambda_max(CORRECT M(Q)) ≤ 16?")
print("="*70)

max_correct = 0
max_old = 0
t0 = time.time()

for trial in range(1000):
    Q = {(x, mu): expm(skew(np.random.randn(3)))
         for x in VERTICES for mu in range(d)}
    M_new = build_correct_M(Q)
    eigs = np.linalg.eigvalsh(M_new)
    max_correct = max(max_correct, eigs[-1])

dt = time.time() - t0
print(f"  1000 random configs ({dt:.1f}s):")
print(f"  Max lambda_max (correct): {max_correct:.6f}")
print(f"  Exceeds 16? {'YES' if max_correct > 16 + 1e-8 else 'NO'}")

# ============================================================
# Test 4: Gradient ascent on CORRECT M(Q)
# ============================================================
print(f"\n{'='*70}")
print("TEST 4: Edge-by-edge optimization on CORRECT M(Q)")
print("="*70)

np.random.seed(2024)
best_ever = 0

for trial in range(5):
    Q = {(x, mu): expm(skew(np.random.randn(3)))
         for x in VERTICES for mu in range(d)}

    for sweep in range(3):
        for x in VERTICES:
            for mu in range(d):
                M0 = build_correct_M(Q)
                lmax0 = np.linalg.eigvalsh(M0)[-1]
                best_g = Q[(x, mu)].copy()
                best_lmax = lmax0

                for _ in range(20):
                    g_test = expm(skew(np.random.randn(3) * np.random.exponential(1)))
                    Q_test = dict(Q)
                    Q_test[(x, mu)] = g_test
                    M_test = build_correct_M(Q_test)
                    lmax_test = np.linalg.eigvalsh(M_test)[-1]
                    if lmax_test > best_lmax:
                        best_lmax = lmax_test
                        best_g = g_test.copy()

                Q[(x, mu)] = best_g

        lmax_final = np.linalg.eigvalsh(build_correct_M(Q))[-1]

    best_ever = max(best_ever, lmax_final)
    print(f"  Trial {trial}: lmax = {lmax_final:.8f}")

print(f"\n  Best from optimization: {best_ever:.8f}")
print(f"  Exceeds 16? {'YES!' if best_ever > 16 + 1e-8 else 'NO'}")

# ============================================================
# Test 5: Verify correct M matches Hessian
# ============================================================
print(f"\n{'='*70}")
print("TEST 5: Does correct M(Q) = Hessian of Wilson action?")
print("="*70)

def wilson_action(Q):
    S = 0
    for x in VERTICES:
        for mu in range(d):
            for nu in range(mu+1, d):
                xmu = neighbor(x, mu)
                xnu = neighbor(x, nu)
                U = Q[(x,mu)] @ Q[(xmu,nu)] @ Q[(xnu,mu)].T @ Q[(x,nu)].T
                S += 3 - np.trace(U)
    return S

Q_test = {(x, mu): expm(skew(np.random.randn(3)))
          for x in VERTICES for mu in range(d)}

M_correct = build_correct_M(Q_test)
v = np.linalg.eigh(M_correct)[1][:, -1]

# Hessian along top eigenvector
eps = 1e-4
S0 = wilson_action(Q_test)

def perturb_along(Q, v, eps):
    Q_new = dict(Q)
    for x in VERTICES:
        for mu in range(d):
            ei = edge_index(x, mu)
            a = v[3*ei:3*ei+3]
            Q_new[(x, mu)] = Q[(x, mu)] @ expm(eps * skew(a))
    return Q_new

Qp = perturb_along(Q_test, v, eps)
Qm = perturb_along(Q_test, v, -eps)

hessian_val = (wilson_action(Qp) - 2*S0 + wilson_action(Qm)) / eps**2
formula_val = v @ M_correct @ v

print(f"  d²S/dε² (numerical): {hessian_val:.6f}")
print(f"  v^T M_correct v:     {formula_val:.6f}")
print(f"  Difference: {abs(hessian_val - formula_val):.6f}")
print(f"  M_correct = Hessian? {'YES' if abs(hessian_val - formula_val) < 0.01 else 'NO'}")
print(f"  Tr(M_correct) = {np.trace(M_correct):.2f}")

# ============================================================
# Summary
# ============================================================
print(f"\n{'='*70}")
print("SUMMARY")
print("="*70)
print(f"  Old formula (code): eigenvalues range up to 16+ (WRONG operator)")
print(f"  New formula (correct): max eigenvalue = {max(max_correct, best_ever):.6f}")
print(f"  The correct operator is {'bounded' if max(max_correct, best_ever) <= 16 + 1e-8 else 'NOT bounded'} by 16")
