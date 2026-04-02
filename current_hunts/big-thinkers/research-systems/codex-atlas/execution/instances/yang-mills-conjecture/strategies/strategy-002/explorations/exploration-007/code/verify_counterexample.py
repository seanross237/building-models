"""
CRITICAL: Verify whether the gradient ascent found a true counterexample.
The edge-by-edge optimization reported lambda_max = 16.16.

Two possible explanations:
1. True counterexample (M(Q) has eigenvalue > 16)
2. The formula M(Q) = sum B_p^T B_p doesn't match the true Wilson action Hessian

Test: compute the Hessian of the Wilson action NUMERICALLY (by finite differences)
and compare with the B^T B formula.
"""
import numpy as np
from scipy.linalg import expm
import itertools

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

def build_full_M(Q):
    """Formula-based M(Q) = sum_p B_p^T B_p."""
    M = np.zeros((N_dim, N_dim))
    for x in VERTICES:
        for mu in range(d):
            for nu in range(mu+1, d):
                xmu = neighbor(x, mu)
                xnu = neighbor(x, nu)
                G1 = np.eye(3)
                G2 = Q[(x, mu)]
                G3 = -(Q[(x, mu)] @ Q[(xmu, nu)] @ Q[(xnu, mu)].T)
                U = Q[(x, mu)] @ Q[(xmu, nu)] @ Q[(xnu, mu)].T @ Q[(x, nu)].T
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

def plaquette_holonomy(Q, x, mu, nu):
    """Compute U_p = Q_{x,mu} Q_{x+mu,nu} Q_{x+nu,mu}^{-1} Q_{x,nu}^{-1}."""
    xmu = neighbor(x, mu)
    xnu = neighbor(x, nu)
    return Q[(x, mu)] @ Q[(xmu, nu)] @ Q[(xnu, mu)].T @ Q[(x, nu)].T

def wilson_action(Q):
    """S = sum_p Tr(I - U_p) = sum_p (3 - Tr(U_p))."""
    S = 0
    for x in VERTICES:
        for mu in range(d):
            for nu in range(mu+1, d):
                U = plaquette_holonomy(Q, x, mu, nu)
                S += 3 - np.trace(U)
    return S

def perturb_Q(Q, x, mu, a, eps):
    """Perturb Q_{x,mu} -> Q_{x,mu} exp(eps * [a]_x)."""
    Q_new = dict(Q)
    Q_new[(x, mu)] = Q[(x, mu)] @ expm(eps * skew(a))
    return Q_new

# ============================================================
# Test 1: Does M(Q) = d^2 S / dA^2 ?
# ============================================================
print("=" * 70)
print("TEST: Does formula M(Q) = sum B_p^T B_p match the Hessian of S?")
print("=" * 70)

def numerical_hessian_element(Q, x1, mu1, a1, x2, mu2, a2, eps=1e-5):
    """Compute d^2 S / (d(eps1) d(eps2)) numerically."""
    # d^2S/(deps1 deps2) = [S(+,+) - S(+,-) - S(-,+) + S(-,-)] / (4 eps^2)
    Q_pp = perturb_Q(perturb_Q(Q, x1, mu1, a1, eps), x2, mu2, a2, eps)
    Q_pm = perturb_Q(perturb_Q(Q, x1, mu1, a1, eps), x2, mu2, a2, -eps)
    Q_mp = perturb_Q(perturb_Q(Q, x1, mu1, a1, -eps), x2, mu2, a2, eps)
    Q_mm = perturb_Q(perturb_Q(Q, x1, mu1, a1, -eps), x2, mu2, a2, -eps)
    return (wilson_action(Q_pp) - wilson_action(Q_pm) - wilson_action(Q_mp) + wilson_action(Q_mm)) / (4 * eps**2)

# Test for random Q
max_err = 0
n_tests = 0
for trial in range(5):
    Q = {(x, mu): expm(skew(np.random.randn(3)))
         for x in VERTICES for mu in range(d)}

    M_formula = build_full_M(Q)

    # Test random matrix elements
    for _ in range(20):
        x1 = VERTICES[np.random.randint(N_vertices)]
        mu1 = np.random.randint(d)
        x2 = VERTICES[np.random.randint(N_vertices)]
        mu2 = np.random.randint(d)
        a1 = np.random.randn(3); a1 /= np.linalg.norm(a1)
        a2 = np.random.randn(3); a2 /= np.linalg.norm(a2)

        # Formula-based result
        i1 = 3 * edge_index(x1, mu1)
        i2 = 3 * edge_index(x2, mu2)
        formula_val = a1 @ M_formula[i1:i1+3, i2:i2+3] @ a2

        # Numerical Hessian
        numerical_val = numerical_hessian_element(Q, x1, mu1, a1, x2, mu2, a2)

        err = abs(formula_val - numerical_val)
        max_err = max(max_err, err)
        n_tests += 1

        if err > 0.1:
            print(f"  LARGE ERROR: trial={trial}, edges ({x1},{mu1})-({x2},{mu2})")
            print(f"    Formula: {formula_val:.6f}")
            print(f"    Numerical: {numerical_val:.6f}")
            print(f"    Error: {err:.6f}")

print(f"  Max error over {n_tests} tests: {max_err:.6e}")
print(f"  Formula matches Hessian? {'YES' if max_err < 1e-3 else 'NO - DISCREPANCY!'}")

# ============================================================
# Test 2: Build full numerical Hessian and compare eigenvalues
# ============================================================
print(f"\n{'='*70}")
print("TEST: Full Hessian eigenvalue comparison")
print("="*70)

Q = {(x, mu): expm(skew(np.random.randn(3)))
     for x in VERTICES for mu in range(d)}

M_formula = build_full_M(Q)
eigs_formula = np.sort(np.linalg.eigvalsh(M_formula))

# Build numerical Hessian (expensive but definitive)
print("  Building numerical Hessian (192x192)...")
eps = 1e-5
M_numerical = np.zeros((N_dim, N_dim))

all_edges = []
for x in VERTICES:
    for mu in range(d):
        all_edges.append((x, mu))

S0 = wilson_action(Q)

for i, (x1, mu1) in enumerate(all_edges):
    for a_idx in range(3):
        row = 3 * i + a_idx
        a1 = np.zeros(3)
        a1[a_idx] = 1.0

        # Diagonal
        Q_p = perturb_Q(Q, x1, mu1, a1, eps)
        Q_m = perturb_Q(Q, x1, mu1, a1, -eps)
        M_numerical[row, row] = (wilson_action(Q_p) - 2*S0 + wilson_action(Q_m)) / eps**2

        # Off-diagonal (only upper triangle, for j > i)
        for j in range(i, len(all_edges)):
            x2, mu2 = all_edges[j]
            for b_idx in range(3):
                col = 3 * j + b_idx
                if col <= row:
                    continue

                a2 = np.zeros(3)
                a2[b_idx] = 1.0

                # Mixed partial
                Q_pp = perturb_Q(perturb_Q(Q, x1, mu1, a1, eps), x2, mu2, a2, eps)
                Q_pm = perturb_Q(perturb_Q(Q, x1, mu1, a1, eps), x2, mu2, a2, -eps)
                Q_mp = perturb_Q(perturb_Q(Q, x1, mu1, a1, -eps), x2, mu2, a2, eps)
                Q_mm = perturb_Q(perturb_Q(Q, x1, mu1, a1, -eps), x2, mu2, a2, -eps)

                val = (wilson_action(Q_pp) - wilson_action(Q_pm) - wilson_action(Q_mp) + wilson_action(Q_mm)) / (4 * eps**2)
                M_numerical[row, col] = val
                M_numerical[col, row] = val

eigs_numerical = np.sort(np.linalg.eigvalsh(M_numerical))

print(f"  Formula lambda_max: {eigs_formula[-1]:.6f}")
print(f"  Numerical lambda_max: {eigs_numerical[-1]:.6f}")
print(f"  Formula lambda_min: {eigs_formula[0]:.6f}")
print(f"  Numerical lambda_min: {eigs_numerical[0]:.6f}")
print(f"  Max eigenvalue difference: {np.max(np.abs(eigs_formula - eigs_numerical)):.6e}")

# Check if numerical Hessian has any eigenvalue > 16
print(f"\n  Numerical Hessian lambda_max: {eigs_numerical[-1]:.6f}")
print(f"  Exceeds 16? {'YES' if eigs_numerical[-1] > 16 + 1e-4 else 'NO'}")

# ============================================================
# Test 3: Reproduce the gradient ascent with verification
# ============================================================
print(f"\n{'='*70}")
print("TEST: Reproduce edge-by-edge optimization with verification")
print("="*70)

np.random.seed(2024)
best_ever = 0
best_Q = None

for trial in range(3):
    Q = {(x, mu): expm(skew(np.random.randn(3)))
         for x in VERTICES for mu in range(d)}

    for sweep in range(3):
        for x in VERTICES:
            for mu in range(d):
                M0 = build_full_M(Q)
                lmax0 = np.linalg.eigvalsh(M0)[-1]
                best_g = Q[(x, mu)].copy()
                best_lmax = lmax0

                for _ in range(20):
                    g_test = expm(skew(np.random.randn(3) * np.random.exponential(1)))
                    Q_test = dict(Q)
                    Q_test[(x, mu)] = g_test
                    M_test = build_full_M(Q_test)
                    lmax_test = np.linalg.eigvalsh(M_test)[-1]

                    if lmax_test > best_lmax:
                        best_lmax = lmax_test
                        best_g = g_test.copy()

                Q[(x, mu)] = best_g

        M_final = build_full_M(Q)
        lmax_final = np.linalg.eigvalsh(M_final)[-1]

    if lmax_final > best_ever:
        best_ever = lmax_final
        best_Q = {k: v.copy() for k, v in Q.items()}

    print(f"  Trial {trial}: lmax = {lmax_final:.8f}")

print(f"\n  Best from optimization: {best_ever:.8f}")
print(f"  Exceeds 16? {'YES' if best_ever > 16 + 1e-8 else 'NO'}")

if best_ever > 16 + 1e-8 and best_Q is not None:
    print("\n  VERIFYING with numerical Hessian...")
    # Build numerical Hessian for this specific Q
    Q = best_Q
    M_formula = build_full_M(Q)
    eigs_f = np.linalg.eigvalsh(M_formula)
    v_top = np.linalg.eigh(M_formula)[1][:, -1]

    # Direct Rayleigh quotient check
    rq = v_top @ M_formula @ v_top / (v_top @ v_top)
    print(f"  Rayleigh quotient of top eigvec: {rq:.8f}")

    # Check M is symmetric
    print(f"  M symmetric? {np.allclose(M_formula, M_formula.T)}")

    # Check M is sum of PSD terms
    print(f"  M is PSD (min eigenvalue)? {eigs_f[0]:.6f}")

    # Compute Wilson action Hessian along top eigenvector direction
    # d²S/dε² = v^T H v
    eps = 1e-4
    S0 = wilson_action(Q)

    # Perturb along top eigenvector direction
    def perturb_along_v(Q, v, eps):
        Q_new = dict(Q)
        for x in VERTICES:
            for mu in range(d):
                ei = edge_index(x, mu)
                a = v[3*ei:3*ei+3]
                Q_new[(x, mu)] = Q[(x, mu)] @ expm(eps * skew(a))
        return Q_new

    Q_plus = perturb_along_v(Q, v_top, eps)
    Q_minus = perturb_along_v(Q, v_top, -eps)
    S_plus = wilson_action(Q_plus)
    S_minus = wilson_action(Q_minus)

    hessian_along_v = (S_plus - 2*S0 + S_minus) / eps**2
    formula_along_v = v_top @ M_formula @ v_top

    print(f"\n  d²S/dε² along top eigvec (numerical): {hessian_along_v:.6f}")
    print(f"  v^T M v (formula): {formula_along_v:.6f}")
    print(f"  Difference: {abs(hessian_along_v - formula_along_v):.6f}")
    print(f"  MATCH? {'YES' if abs(hessian_along_v - formula_along_v) < 0.01 else 'NO - FORMULA IS WRONG!'}")

    # Check trace
    print(f"\n  Tr(M_formula) = {np.trace(M_formula):.4f} (should be 1152)")
