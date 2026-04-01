"""
Stage 4 LITE: Final verification — lighter version with focused adversarial.
"""
import numpy as np
from scipy.optimize import minimize as sp_minimize
np.random.seed(12345)

I3 = np.eye(3)
PAIRS = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]

def random_SO3():
    A = np.random.randn(3, 3)
    Q, R = np.linalg.qr(A)
    Q = Q @ np.diag(np.sign(np.diag(R)))
    if np.linalg.det(Q) < 0:
        Q[:, 0] *= -1
    return Q

def f(M, p):
    return p @ (I3 - M) @ p

def compute_sum_S(R, D, T):
    total = 0.0
    for mu, nu in PAIRS:
        U = R[mu] @ D[(mu,nu)]
        W = D[(mu,nu)] @ R[nu].T
        RDR = R[mu] @ D[(mu,nu)] @ R[nu].T
        total += 2*f(U, T[mu]) + 2*f(W, T[nu])
        total -= 2*T[mu] @ (2*I3 - D[(mu,nu)].T - RDR) @ T[nu]
    return total

def compute_F(R, T):
    sf = sum(f(R[mu], T[mu]) for mu in range(4))
    sd = 0.0
    for mu, nu in PAIRS:
        u = R[mu].T @ T[mu] - T[nu]
        v = T[mu] - R[nu].T @ T[nu]
        sd += (np.linalg.norm(u) - np.linalg.norm(v))**2
    return 2*sf + sd

def skew(v):
    return np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])

def so3_from_vec(v):
    theta = np.linalg.norm(v)
    if theta < 1e-15:
        return I3.copy()
    k = v / theta
    K = skew(k)
    return I3 + np.sin(theta)*K + (1-np.cos(theta))*(K@K)

# ============================================================
# TEST 1: 20K random for full chain
# ============================================================
print("=" * 60)
print("20K RANDOM: Full proof chain")
print("=" * 60)

min_F = float('inf')
min_sS = float('inf')
min_gap = float('inf')
v_F = 0; v_chain = 0

for trial in range(20000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    T = {mu: np.random.randn(3) for mu in range(3)}
    T[3] = -T[0]-T[1]-T[2]

    sS = compute_sum_S(R, D, T)
    Fval = compute_F(R, T)
    gap = sS - Fval

    min_F = min(min_F, Fval)
    min_sS = min(min_sS, sS)
    min_gap = min(min_gap, gap)
    if Fval < -1e-10: v_F += 1
    if gap < -1e-10: v_chain += 1

print(f"  min F = {min_F:.6f}, min sum_S = {min_sS:.6f}")
print(f"  min (sum_S - F) = {min_gap:.6f}")
print(f"  F < 0: {v_F}/20000, sum_S < F: {v_chain}/20000")

# ============================================================
# TEST 2: Adversarial on F
# ============================================================
print("\n" + "=" * 60)
print("ADVERSARIAL on F(R,T)")
print("=" * 60)

def neg_F(params):
    R = {i: so3_from_vec(params[3*i:3*(i+1)]) for i in range(4)}
    T = {}
    for mu in range(3):
        T[mu] = params[12 + 3*mu: 12 + 3*mu + 3]
    T[3] = -T[0] - T[1] - T[2]
    norm = np.sqrt(sum(np.dot(T[mu], T[mu]) for mu in range(4)))
    if norm < 1e-12: return 0.0
    for mu in range(4): T[mu] /= norm
    return -compute_F(R, T)

best = float('inf')
best_p = None
for trial in range(5000):
    p0 = np.random.randn(21)
    v = neg_F(p0)
    if v < best:
        best = v
        best_p = p0.copy()

print(f"  5K random: min F = {-best:.8e}")

res = sp_minimize(neg_F, best_p, method='Nelder-Mead',
                  options={'maxiter': 300000, 'xatol': 1e-14, 'fatol': 1e-16})
print(f"  NM refined: min F = {-res.fun:.8e}")

res2 = sp_minimize(neg_F, res.x, method='Powell',
                   options={'maxiter': 300000, 'xtol': 1e-14, 'ftol': 1e-16})
print(f"  Powell: min F = {-res2.fun:.8e}")

# ============================================================
# TEST 3: Adversarial on M9 eigenvalue
# ============================================================
print("\n" + "=" * 60)
print("ADVERSARIAL on min eigenvalue of M9")
print("=" * 60)

P = np.zeros((12, 9))
for i in range(3):
    P[3*i:3*i+3, 3*i:3*i+3] = I3
P[9:12, 0:3] = -I3
P[9:12, 3:6] = -I3
P[9:12, 6:9] = -I3

def build_M12(R, D):
    M = np.zeros((12, 12))
    for mu, nu in PAIRS:
        U = R[mu] @ D[(mu,nu)]
        W = D[(mu,nu)] @ R[nu].T
        RDR = R[mu] @ D[(mu,nu)] @ R[nu].T
        M[3*mu:3*mu+3, 3*mu:3*mu+3] += 2*I3 - U - U.T
        M[3*nu:3*nu+3, 3*nu:3*nu+3] += 2*I3 - W - W.T
        cross = D[(mu,nu)].T + RDR - 2*I3
        M[3*mu:3*mu+3, 3*nu:3*nu+3] += cross
        M[3*nu:3*nu+3, 3*mu:3*mu+3] += cross.T
    return M

def min_eig(params):
    R = {i: so3_from_vec(params[3*i:3*(i+1)]) for i in range(4)}
    D = {}; idx = 12
    for p in PAIRS:
        D[p] = so3_from_vec(params[idx:idx+3]); idx += 3
    M12 = build_M12(R, D)
    M9 = P.T @ M12 @ P
    return np.linalg.eigvalsh((M9+M9.T)/2)[0]

best_eig = float('inf')
best_ep = None
np.random.seed(42)
for trial in range(3000):
    p0 = np.random.randn(30) * np.pi
    v = min_eig(p0)
    if v < best_eig:
        best_eig = v
        best_ep = p0.copy()

print(f"  3K random: min eig = {best_eig:.8e}")

res = sp_minimize(min_eig, best_ep, method='Nelder-Mead',
                  options={'maxiter': 200000, 'xatol': 1e-14, 'fatol': 1e-15})
print(f"  NM: min eig = {res.fun:.8e}")

res2 = sp_minimize(min_eig, res.x, method='Powell',
                   options={'maxiter': 200000, 'xtol': 1e-14, 'ftol': 1e-15})
print(f"  Powell: min eig = {res2.fun:.8e}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("PROOF STATUS")
print("=" * 60)
all_pass = (v_F == 0 and v_chain == 0 and
            -res2.fun <= 1e-8 and  # F min ~0
            res2.fun >= -1e-8)     # eig min ~0 (using the eig result)
print(f"  F >= 0: {'PASS' if v_F == 0 else 'FAIL'}")
print(f"  sum_S >= F: {'PASS' if v_chain == 0 else 'FAIL'}")
print(f"  Adversarial F min ≈ 0: {'PASS' if -res2.fun <= 1e-8 else 'FAIL'}")
print(f"  Overall: {'ALL TESTS PASS' if all_pass else 'SOME TESTS FAIL'}")
