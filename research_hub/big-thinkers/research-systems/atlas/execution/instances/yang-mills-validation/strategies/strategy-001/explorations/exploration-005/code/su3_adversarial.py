"""
SU(3) Adversarial Search — Exploration 005
==========================================

Attempts to find configurations that maximize H_norm and potentially
exceed the predicted bound of 1/27.

Methods:
1. 100+ random Haar configurations
2. Gradient ascent on H_norm
3. Specific adversarial constructions
"""
import numpy as np
from scipy.linalg import expm
from itertools import product as iproduct

# ============================================================
# Parameters (same as main script)
# ============================================================
L = 2
d = 4
N = 3
beta = 1.0
n_sites = L**d
n_links = d * n_sites
n_gen = N**2 - 1
n_dof = n_links * n_gen

# Gell-Mann matrices
lam = np.zeros((8, 3, 3), dtype=complex)
lam[0] = np.array([[0,1,0],[1,0,0],[0,0,0]], dtype=complex)
lam[1] = np.array([[0,-1j,0],[1j,0,0],[0,0,0]], dtype=complex)
lam[2] = np.array([[1,0,0],[0,-1,0],[0,0,0]], dtype=complex)
lam[3] = np.array([[0,0,1],[0,0,0],[1,0,0]], dtype=complex)
lam[4] = np.array([[0,0,-1j],[0,0,0],[1j,0,0]], dtype=complex)
lam[5] = np.array([[0,0,0],[0,0,1],[0,1,0]], dtype=complex)
lam[6] = np.array([[0,0,0],[0,0,-1j],[0,1j,0]], dtype=complex)
lam[7] = np.array([[1,0,0],[0,1,0],[0,0,-2]], dtype=complex) / np.sqrt(3)
tau = np.array([1j * lam[a] / 2 for a in range(8)])

# Lattice
def site_index(x):
    idx = 0
    for i, xi in enumerate(x):
        idx += (int(xi) % L) * (L ** i)
    return idx

def shift(x, mu, sign=1):
    xnew = list(x)
    xnew[mu] = (xnew[mu] + sign) % L
    return tuple(xnew)

def link_index(x, mu):
    return site_index(x) * d + mu

plaquette_links = []
for x in iproduct(range(L), repeat=d):
    for mu in range(d):
        for nu in range(mu+1, d):
            links = [
                (link_index(x, mu), +1),
                (link_index(shift(x, mu), nu), +1),
                (link_index(shift(x, nu), mu), -1),
                (link_index(x, nu), -1),
            ]
            plaquette_links.append(links)

n_plaq = len(plaquette_links)

def adjoint_rep(g):
    R = np.zeros((8, 8))
    gdagg = g.conj().T
    for a in range(8):
        gtag = g @ tau[a] @ gdagg
        for c in range(8):
            R[c, a] = -2.0 * np.real(np.trace(tau[c] @ gtag))
    return R

def build_hessian_LEFT(U, plaq_list):
    H = np.zeros((n_dof, n_dof))
    prefactor = beta / (2.0 * N)
    for plaq in plaq_list:
        e_idx = [plaq[k][0] for k in range(4)]
        signs  = [plaq[k][1] for k in range(4)]
        U1, U2, U3, U4 = [U[e_idx[k]] for k in range(4)]
        P1 = np.eye(N, dtype=complex)
        P2 = U1
        P3 = U1 @ U2 @ U3.conj().T
        P4 = U1 @ U2 @ U3.conj().T @ U4.conj().T
        Rs = [adjoint_rep(P) for P in [P1, P2, P3, P4]]
        for ie in range(4):
            for je in range(4):
                block = prefactor * signs[ie] * signs[je] * (Rs[ie].T @ Rs[je])
                ei, ej = e_idx[ie], e_idx[je]
                H[ei*n_gen:(ei+1)*n_gen, ej*n_gen:(ej+1)*n_gen] += block
    return H

def compute_hnorm(U):
    H = build_hessian_LEFT(U, plaquette_links)
    lmax = np.max(np.linalg.eigvalsh(H))
    return lmax / (8 * (d-1) * N * beta), lmax

def random_su3():
    Z = np.random.randn(N, N) + 1j * np.random.randn(N, N)
    Q, R = np.linalg.qr(Z)
    D = np.diag(np.diag(R) / np.abs(np.diag(R)))
    Q = Q @ D
    det = np.linalg.det(Q)
    Q /= det**(1.0/N)
    return Q

# ============================================================
# TEST 1: 100 random Haar configurations
# ============================================================
print("=" * 60)
print("TEST 1: 100 RANDOM SU(3) CONFIGURATIONS")
print("=" * 60)

np.random.seed(123)
max_hnorm = 0.0
max_lmax = 0.0
violations = []

for trial in range(100):
    U_rand = np.array([random_su3() for _ in range(n_links)])
    hnorm, lmax = compute_hnorm(U_rand)
    if hnorm > max_hnorm:
        max_hnorm = hnorm
        max_lmax = lmax
        best_U = U_rand.copy()
    if hnorm > 1/27 + 1e-6:
        violations.append((trial, hnorm, lmax))
        print(f"  VIOLATION at trial {trial}: H_norm = {hnorm:.8f} > 1/27 = {1/27:.8f}")

print(f"  Max H_norm over 100 configs: {max_hnorm:.8f}")
print(f"  Bound 1/27:                  {1/27:.8f}")
print(f"  Violations:                  {len(violations)}")
print(f"  Max is at Q=I? {abs(max_hnorm - 1/27) < 1e-6}")

# ============================================================
# TEST 2: Gradient ascent to maximize H_norm
# ============================================================
print("\n" + "=" * 60)
print("TEST 2: GRADIENT ASCENT TO MAXIMIZE H_norm")
print("=" * 60)

def hnorm_with_grad(U, eps=1e-5):
    """Compute H_norm and numerical gradient w.r.t. link variables."""
    hnorm0, _ = compute_hnorm(U)
    grad = np.zeros((n_links, n_gen))
    for li in range(n_links):
        for ga in range(n_gen):
            U_plus = U.copy()
            U_plus[li] = expm(eps * tau[ga]) @ U[li]
            # Project back to SU(3)
            hnorm_p, _ = compute_hnorm(U_plus)
            grad[li, ga] = (hnorm_p - hnorm0) / eps
    return hnorm0, grad

def gradient_ascent(U_init, n_steps=30, step_size=0.02):
    """Ascent to maximize H_norm."""
    U = U_init.copy()
    hnorm_history = []

    for step in range(n_steps):
        hnorm, grad = hnorm_with_grad(U, eps=1e-5)
        hnorm_history.append(hnorm)

        # Update each link
        for li in range(n_links):
            delta = step_size * grad[li]
            dM = sum(delta[ga] * tau[ga] for ga in range(n_gen))
            U[li] = expm(dM) @ U[li]
            # Normalize to SU(3)
            det = np.linalg.det(U[li])
            U[li] /= det**(1.0/N)

        if step % 5 == 0:
            print(f"  Step {step:3d}: H_norm = {hnorm:.8f}")

    hnorm_final, _ = compute_hnorm(U)
    print(f"  Final: H_norm = {hnorm_final:.8f}")
    return U, hnorm_final, hnorm_history

print("\n  Starting gradient ascent from Q=I ...")
U_I = np.array([np.eye(N, dtype=complex) for _ in range(n_links)])
# Use a perturbation of Q=I as starting point
np.random.seed(0)
U_start = np.array([expm(0.3 * sum(np.random.randn() * tau[a] for a in range(n_gen))) for _ in range(n_links)])
for li in range(n_links):
    det = np.linalg.det(U_start[li])
    U_start[li] /= det**(1.0/N)

U_opt, hnorm_opt, history = gradient_ascent(U_start, n_steps=20, step_size=0.01)
print(f"\n  Gradient ascent result: H_norm = {hnorm_opt:.8f}")
print(f"  Bound 1/27 = {1/27:.8f}")
print(f"  Exceeded bound? {'YES' if hnorm_opt > 1/27 + 1e-6 else 'NO'}")

# ============================================================
# TEST 3: More adversarial SU(3) constructions
# ============================================================
print("\n" + "=" * 60)
print("TEST 3: ADVERSARIAL CONSTRUCTIONS")
print("=" * 60)

# 3a: Center elements of SU(3) — group {I, omega*I, omega^2*I} with omega = e^{2pi*i/3}
omega = np.exp(2j * np.pi / 3)
U_center1 = np.array([omega * np.eye(N, dtype=complex) for _ in range(n_links)])
hnorm_c1, lmax_c1 = compute_hnorm(U_center1)
print(f"\n  3a: All links = omega*I (omega = e^{{2pi*i/3}})")
print(f"  lambda_max = {lmax_c1:.6f}, H_norm = {hnorm_c1:.8f}")

# 3b: Mix of center elements
U_center2 = []
for k in range(n_links):
    if k % 3 == 0:
        U_center2.append(np.eye(N, dtype=complex))
    elif k % 3 == 1:
        U_center2.append(omega * np.eye(N, dtype=complex))
    else:
        U_center2.append(omega**2 * np.eye(N, dtype=complex))
U_center2 = np.array(U_center2)
hnorm_c2, lmax_c2 = compute_hnorm(U_center2)
print(f"\n  3b: Mixed center elements")
print(f"  lambda_max = {lmax_c2:.6f}, H_norm = {hnorm_c2:.8f}")

# 3c: All links = exp(i*pi/3 * lambda_3)
angle = np.pi / 3
U_phase = np.array([expm(1j * angle * lam[2] / 2) for _ in range(n_links)])
hnorm_p, lmax_p = compute_hnorm(U_phase)
print(f"\n  3c: All links = exp(i*pi/3 * lambda_3)")
print(f"  lambda_max = {lmax_p:.6f}, H_norm = {hnorm_p:.8f}")

# 3d: Links that maximize the plaquette value being maximally non-trivial
# Try all links = exp(i*pi/2 * lambda_8) (maximal lambda_8 phase)
angle2 = np.pi / 2
U_l8 = np.array([expm(1j * angle2 * lam[7]) for _ in range(n_links)])
for li in range(n_links):
    det = np.linalg.det(U_l8[li])
    U_l8[li] /= det**(1.0/N)
hnorm_l8, lmax_l8 = compute_hnorm(U_l8)
print(f"\n  3d: All links = exp(i*pi/2 * lambda_8)")
print(f"  lambda_max = {lmax_l8:.6f}, H_norm = {hnorm_l8:.8f}")

# 3e: Staggered by direction (different configs for x and y direction links)
U_stagger_dir = []
for x in iproduct(range(L), repeat=d):
    for mu in range(d):
        if mu % 2 == 0:
            U_stagger_dir.append(expm(np.pi/2 * tau[2]))
        else:
            U_stagger_dir.append(expm(-np.pi/2 * tau[2]))
U_stagger_dir = np.array(U_stagger_dir)
for li in range(n_links):
    det = np.linalg.det(U_stagger_dir[li])
    U_stagger_dir[li] /= det**(1.0/N)
hnorm_sd, lmax_sd = compute_hnorm(U_stagger_dir)
print(f"\n  3e: Direction-staggered config")
print(f"  lambda_max = {lmax_sd:.6f}, H_norm = {hnorm_sd:.8f}")

# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("FINAL SUMMARY")
print("=" * 60)

all_results = [
    ("100 random (max)", max_hnorm),
    ("Gradient ascent", hnorm_opt),
    ("Center omega*I", hnorm_c1),
    ("Mixed center", hnorm_c2),
    ("exp(i*pi/3*lambda3)", hnorm_p),
    ("exp(i*pi/2*lambda8)", hnorm_l8),
    ("Direction-staggered", hnorm_sd),
]

print(f"\n{'Config':>25} {'H_norm':>14} {'<=1/27':>10}")
print("-" * 55)
for name, hn in all_results:
    ok = hn <= 1/27 + 1e-6
    print(f"  {name:>23}   {hn:.8f}   {'YES' if ok else 'VIOLATION!'}")

print(f"\n  Analytical value Q=I:  1/27 = {1/27:.8f}")
total_max = max(hn for _, hn in all_results)
print(f"  Maximum found:         {total_max:.8f}")
print(f"  Any violations?        {'YES' if total_max > 1/27 + 1e-6 else 'NO'}")
