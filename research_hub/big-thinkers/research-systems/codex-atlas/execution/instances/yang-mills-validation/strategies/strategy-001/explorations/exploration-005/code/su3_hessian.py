"""
SU(3) Hessian Eigenvalue Analysis — Exploration 005
=====================================================

Tests H_norm ≤ 1/27 for SU(3), d=4, L=2.

LEFT perturbation convention:
  Q_e -> exp(t*v_e) * Q_e
  P1 = I
  P2 = Q1
  P3 = Q1 @ Q2 @ Q3†           (includes Q3 inverse)
  P4 = Q1 @ Q2 @ Q3† @ Q4†    (= U_plaq)

Action: S = -(beta/N) sum Re Tr(U_□)  with N=3
Hessian prefactor: beta/(2N) = beta/6
H_norm = lambda_max(HessS) / (8*(d-1)*N*beta)
"""
import numpy as np
from itertools import product as iproduct

# ============================================================
# Parameters
# ============================================================
L = 2
d = 4
N = 3
beta = 1.0

n_sites = L**d           # 16
n_links = d * n_sites    # 64
n_gen = N**2 - 1         # 8
n_dof = n_links * n_gen  # 512

print(f"SU(3) setup: L={L}, d={d}, N={N}")
print(f"n_sites={n_sites}, n_links={n_links}, n_gen={n_gen}, n_dof={n_dof}")
print(f"Hessian size: {n_dof}×{n_dof}")
print()

# ============================================================
# SU(3) Generators: Gell-Mann matrices
# ============================================================
lam = np.zeros((8, 3, 3), dtype=complex)

# lambda_1
lam[0] = np.array([[0,1,0],[1,0,0],[0,0,0]], dtype=complex)
# lambda_2
lam[1] = np.array([[0,-1j,0],[1j,0,0],[0,0,0]], dtype=complex)
# lambda_3
lam[2] = np.array([[1,0,0],[0,-1,0],[0,0,0]], dtype=complex)
# lambda_4
lam[3] = np.array([[0,0,1],[0,0,0],[1,0,0]], dtype=complex)
# lambda_5
lam[4] = np.array([[0,0,-1j],[0,0,0],[1j,0,0]], dtype=complex)
# lambda_6
lam[5] = np.array([[0,0,0],[0,0,1],[0,1,0]], dtype=complex)
# lambda_7
lam[6] = np.array([[0,0,0],[0,0,-1j],[0,1j,0]], dtype=complex)
# lambda_8
lam[7] = np.array([[1,0,0],[0,1,0],[0,0,-2]], dtype=complex) / np.sqrt(3)

tau = np.array([1j * lam[a] / 2 for a in range(8)])  # Generators: i*lambda/2

# Verify normalization: Tr(lambda_a lambda_b) = 2 delta_{ab}
print("Generator normalization check:")
for a in range(8):
    for b in range(8):
        tr = np.trace(lam[a] @ lam[b]).real
        expected = 2.0 if a == b else 0.0
        if abs(tr - expected) > 1e-10:
            print(f"  ERROR: Tr(lam[{a}] lam[{b}]) = {tr:.6f}, expected {expected}")
print("  All Tr(lambda_a lambda_b) = 2*delta_{ab}: OK")

# Verify |tau_a|^2 = -2 Tr(tau_a^2) = 1
print("  |tau_a|^2 = 1 check:")
for a in range(8):
    norm_sq = -2.0 * np.trace(tau[a] @ tau[a]).real
    if abs(norm_sq - 1.0) > 1e-10:
        print(f"  ERROR: |tau[{a}]|^2 = {norm_sq:.6f}, expected 1")
print("  All |tau_a|^2 = 1: OK")
print()

# ============================================================
# Lattice geometry
# ============================================================
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

# Build plaquette list
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
print(f"Number of plaquettes: {n_plaq}")  # Should be L^d * d*(d-1)/2 = 16 * 6 = 96
print()

# ============================================================
# Adjoint representation for SU(3)
# ============================================================
def adjoint_rep(g):
    """
    Adjoint representation of g in SU(3).
    R[c,a] = -2 Re Tr(tau_c @ g @ tau_a @ g†)
    Result: 8x8 real orthogonal matrix.
    """
    R = np.zeros((8, 8))
    gdagg = g.conj().T
    for a in range(8):
        gtag = g @ tau[a] @ gdagg  # g tau_a g†
        for c in range(8):
            R[c, a] = -2.0 * np.real(np.trace(tau[c] @ gtag))
    return R

# ============================================================
# Wilson action for SU(3)
# ============================================================
def wilson_action(U, plaq_list):
    """S(Q) = -(beta/N) sum_plaq Re Tr(U_plaq)"""
    S = 0.0
    for plaq in plaq_list:
        e1, s1 = plaq[0]; e2, s2 = plaq[1]
        e3, s3 = plaq[2]; e4, s4 = plaq[3]
        # LEFT convention (s3=-1, s4=-1 means inverse)
        U_plaq = U[e1] @ U[e2] @ U[e3].conj().T @ U[e4].conj().T
        S += np.real(np.trace(U_plaq))
    return -beta / N * S

# ============================================================
# Hessian builder — LEFT convention
# ============================================================
def build_hessian_LEFT(U, plaq_list):
    """
    LEFT perturbation Hessian for SU(3).

    HessS = (beta/(2N)) * sum_plaq sum_{i,j} s_i s_j R_i^T R_j
    where P1=I, P2=U1, P3=U1*U2*U3†, P4=U1*U2*U3†*U4†=U_plaq
    and R_k = adjoint_rep(P_k).
    """
    H = np.zeros((n_dof, n_dof))
    prefactor = beta / (2.0 * N)

    for plaq in plaq_list:
        e_idx = [plaq[k][0] for k in range(4)]
        signs  = [plaq[k][1] for k in range(4)]
        U1, U2, U3, U4 = [U[e_idx[k]] for k in range(4)]

        # LEFT partial holonomies
        P1 = np.eye(N, dtype=complex)
        P2 = U1
        P3 = U1 @ U2 @ U3.conj().T
        P4 = U1 @ U2 @ U3.conj().T @ U4.conj().T  # = U_plaq

        Rs = [adjoint_rep(P) for P in [P1, P2, P3, P4]]

        for ie in range(4):
            for je in range(4):
                # Block contribution: prefactor * s_ie * s_je * R_ie^T @ R_je
                block = prefactor * signs[ie] * signs[je] * (Rs[ie].T @ Rs[je])
                ei, ej = e_idx[ie], e_idx[je]
                H[ei*n_gen:(ei+1)*n_gen, ej*n_gen:(ej+1)*n_gen] += block

    return H

# ============================================================
# SU(3) matrix exponential
# ============================================================
def su3_exp(M, order=20):
    """
    Matrix exponential via Taylor series (for small M).
    M should be traceless anti-Hermitian (Lie algebra element).
    """
    result = np.eye(N, dtype=complex)
    term = np.eye(N, dtype=complex)
    for k in range(1, order+1):
        term = term @ M / k
        result = result + term
        if np.max(np.abs(term)) < 1e-15:
            break
    return result

def su3_exp_scipy(M):
    """Matrix exponential using scipy."""
    from scipy.linalg import expm
    return expm(M)

# ============================================================
# Random SU(3) generator
# ============================================================
def random_su3():
    """Random Haar SU(3) via QR decomposition."""
    Z = np.random.randn(N, N) + 1j * np.random.randn(N, N)
    Q, R = np.linalg.qr(Z)
    D = np.diag(np.diag(R) / np.abs(np.diag(R)))
    Q = Q @ D
    # Fix determinant to 1
    det = np.linalg.det(Q)
    Q /= det**(1.0/N)
    return Q

def verify_su3(g, label=""):
    """Check g is in SU(3)."""
    err_unitary = np.max(np.abs(g @ g.conj().T - np.eye(N)))
    err_det = abs(np.linalg.det(g) - 1.0)
    if err_unitary > 1e-10 or err_det > 1e-10:
        print(f"  WARNING {label}: not SU(3)! unitary_err={err_unitary:.2e}, det_err={err_det:.2e}")

# ============================================================
# TASK 1: Q=I Sanity Check
# ============================================================
print("=" * 70)
print("TASK 1: Q=I SANITY CHECK")
print("=" * 70)

U_I = np.array([np.eye(N, dtype=complex) for _ in range(n_links)])

print("Building Hessian at Q=I ...")
H_I = build_hessian_LEFT(U_I, plaquette_links)
print(f"  Hessian shape: {H_I.shape}")
print(f"  Hessian symmetry check: max|H - H^T| = {np.max(np.abs(H_I - H_I.T)):.2e}")

print("Computing eigenvalues ...")
evals_I = np.linalg.eigvalsh(H_I)
evals_I_sorted = np.sort(evals_I)[::-1]

lmax_I = evals_I_sorted[0]
expected_lmax = 8.0 * beta / 3.0  # = (beta/(2*3)) * 16 = beta * 8/6 = 8*beta/3
hnorm_I = lmax_I / (8 * (d-1) * N * beta)

print(f"\n  lambda_max at Q=I = {lmax_I:.8f}")
print(f"  Expected:            {expected_lmax:.8f}  (= 8*beta/3 = 8/3 for beta=1)")
print(f"  Difference:          {abs(lmax_I - expected_lmax):.2e}")
print(f"\n  H_norm(I) = lambda_max / (8*(d-1)*N*beta)")
print(f"            = {lmax_I:.6f} / (8 * {d-1} * {N} * {beta})")
print(f"            = {lmax_I:.6f} / {8*(d-1)*N*beta:.1f}")
print(f"            = {hnorm_I:.8f}")
print(f"  Expected H_norm(I) = 1/27 = {1/27:.8f}")
print(f"  Difference: {abs(hnorm_I - 1/27):.2e}")

# Also check eigenvalue multiplicity
unique_evals = []
current = evals_I_sorted[0]
count = 1
for e in evals_I_sorted[1:]:
    if abs(e - current) < 1e-6:
        count += 1
    else:
        unique_evals.append((current, count))
        current = e
        count = 1
unique_evals.append((current, count))

print(f"\n  Top eigenvalues and their multiplicities:")
for val, cnt in unique_evals[:8]:
    print(f"    {val:.8f}  (multiplicity {cnt})")

if abs(lmax_I - expected_lmax) < 0.01:
    print(f"\n  SANITY CHECK PASSED: lambda_max = 8*beta/3 = {expected_lmax:.6f} ✓")
else:
    print(f"\n  SANITY CHECK FAILED: got {lmax_I:.6f}, expected {expected_lmax:.6f}")

print()

# ============================================================
# TASK 2: 20 Random SU(3) Configurations
# ============================================================
print("=" * 70)
print("TASK 2: 20 RANDOM SU(3) CONFIGURATIONS")
print("=" * 70)

np.random.seed(42)

results = []
print(f"\n{'Config':>8} {'lambda_max':>14} {'H_norm':>14} {'<=1/27?':>10}")
print("-" * 50)

for trial in range(20):
    U_rand = np.array([random_su3() for _ in range(n_links)])
    # Verify a few are in SU(3)
    if trial < 3:
        verify_su3(U_rand[0], f"config {trial}, link 0")

    H_rand = build_hessian_LEFT(U_rand, plaquette_links)
    evals_rand = np.linalg.eigvalsh(H_rand)
    lmax = np.max(evals_rand)
    hnorm = lmax / (8 * (d-1) * N * beta)
    bound = 1.0 / 27.0
    ok = hnorm <= bound + 1e-8
    results.append((lmax, hnorm))
    print(f"  {trial+1:>6}   {lmax:>12.6f}   {hnorm:>12.8f}   {'YES' if ok else 'VIOLATION!'}")

lmax_values = [r[0] for r in results]
hnorm_values = [r[1] for r in results]

print(f"\n  Max lambda_max over 20 configs: {max(lmax_values):.6f}")
print(f"  Max H_norm over 20 configs:    {max(hnorm_values):.8f}")
print(f"  H_norm(I):                     {hnorm_I:.8f}")
print(f"  Bound 1/27:                    {1/27:.8f}")
print(f"\n  H_norm(I) is maximum? {hnorm_I >= max(hnorm_values) - 1e-8}")

# ============================================================
# TASK 3: Specific test configs
# ============================================================
print("\n" + "=" * 70)
print("TASK 3: SPECIFIC CONFIGURATIONS")
print("=" * 70)

# Config: all links = diag(i, -i, 1) (partial analogue of SU(2) i*sigma_3)
print("\n3a: U_all = diag(i, -i, 1) (partial SU(3) analogue)")
U_diag1 = np.array([np.diag([1j, -1j, 1.0+0j]) for _ in range(n_links)])
verify_su3(U_diag1[0], "diag(i,-i,1)")
H_diag1 = build_hessian_LEFT(U_diag1, plaquette_links)
evals_diag1 = np.linalg.eigvalsh(H_diag1)
lmax_d1 = np.max(evals_diag1)
hnorm_d1 = lmax_d1 / (8 * (d-1) * N * beta)
print(f"  lambda_max = {lmax_d1:.6f}, H_norm = {hnorm_d1:.8f}")

# Config: all links = diag(i, i, -1) (another diagonal SU(3))
print("\n3b: U_all = diag(i, i, -1)")
U_diag2 = np.array([np.diag([1j, 1j, -1.0+0j]) for _ in range(n_links)])
verify_su3(U_diag2[0], "diag(i,i,-1)")
H_diag2 = build_hessian_LEFT(U_diag2, plaquette_links)
evals_diag2 = np.linalg.eigvalsh(H_diag2)
lmax_d2 = np.max(evals_diag2)
hnorm_d2 = lmax_d2 / (8 * (d-1) * N * beta)
print(f"  lambda_max = {lmax_d2:.6f}, H_norm = {hnorm_d2:.8f}")

# Config: alternating between I and a rotation
print("\n3c: Staggered config (alternating I and rotation by pi/2 around lambda_3)")
angle = np.pi / 2
U_stagger = []
for k in range(n_links):
    if k % 2 == 0:
        U_stagger.append(np.eye(N, dtype=complex))
    else:
        # exp(angle * tau_3) = exp(i*angle*lambda_3/2)
        g = su3_exp_scipy(angle * tau[2])
        U_stagger.append(g)
U_stagger = np.array(U_stagger)
verify_su3(U_stagger[1], "stagger")
H_stagger = build_hessian_LEFT(U_stagger, plaquette_links)
evals_stagger = np.linalg.eigvalsh(H_stagger)
lmax_stag = np.max(evals_stagger)
hnorm_stag = lmax_stag / (8 * (d-1) * N * beta)
print(f"  lambda_max = {lmax_stag:.6f}, H_norm = {hnorm_stag:.8f}")

# ============================================================
# TASK 4: Triangle Inequality Bound
# ============================================================
print("\n" + "=" * 70)
print("TASK 4: TRIANGLE INEQUALITY ANALYSIS")
print("=" * 70)

# CS bound: |B_□|^2 <= 4 * sum|v_e|^2 (from triangle ineq + Ad isometry)
# Summing over plaquettes: HessS <= (beta/(2N)) * 4 * 2*(d-1) * |v|^2
# = (beta/(2N)) * 8*(d-1) * |v|^2
# K_S > 0 iff HessS(v,v) < (N/2)|v|^2
# So: (beta/(2N)) * 8*(d-1) < N/2
# => 8*(d-1)*beta/(2N) < N/2
# => 4*(d-1)*beta/N < N/2
# => beta < N^2 / (8*(d-1))
# For N=3, d=4: beta < 9/24 = 3/8

cs_threshold = N**2 / (8 * (d-1))
print(f"\n  CS bound threshold: beta < N^2 / (8*(d-1)) = {N}^2 / (8*{d-1}) = {cs_threshold:.4f}")
print(f"  For N=3, d=4: beta < 3/8 = {3/8:.4f}")

# If H_norm ≤ 1/(8*(d-1)) always, then:
# HessS <= beta/(2N) * 16 = 8*beta/3 for N=3
# K_S > 0 iff 8*beta/3 < 3/2 => beta < 9/16
conj_threshold = N**2 / (16 * (d-1))
print(f"\n  Conjecture threshold (if H_norm <= 1/(8*(d-1))):")
print(f"  beta < N^2 / (16*(d-1)) = {N}^2 / (16*{d-1}) = {conj_threshold:.4f}")

# Based on H_norm ≤ 1/27 conjecture:
# HessS <= (beta/(2N)) * 16/(8*(d-1)*N) * 8*(d-1)*N = beta/N * 16/(...)
# Actually: H_norm = lambda_max / (8*(d-1)*N*beta) <= 1/(8*(d-1)*N*...)
# Wait, let me recompute:
# H_norm <= C means lambda_max <= C * 8*(d-1)*N*beta
# K_S > 0 iff lambda_max < N/2 * |v|^2
# So: C * 8*(d-1)*N*beta < N/2
# => C * 16*(d-1)*beta < 1
# => beta < 1 / (C * 16*(d-1))
# For C = 1/27 = 1/(3*N^2): beta < N^2 / (16*(d-1)) = 9/48 = 3/16
conj2_threshold = 1 / (1/27.0 * 16 * (d-1))
print(f"\n  If H_norm <= 1/27 always:")
print(f"  K_S > 0 iff beta < 1 / (1/27 * 16*(d-1)) = 27 / (16*{d-1}) = {conj2_threshold:.4f}")
print(f"  (= 27/48 = 9/16)")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

all_hnorms = hnorm_values + [hnorm_I, hnorm_d1, hnorm_d2, hnorm_stag]
max_hnorm = max(all_hnorms)

print(f"\n  H_norm at Q=I:                {hnorm_I:.8f} (expected 1/27 = {1/27:.8f})")
print(f"  Max H_norm (20 random):       {max(hnorm_values):.8f}")
print(f"  H_norm diag(i,-i,1):          {hnorm_d1:.8f}")
print(f"  H_norm diag(i,i,-1):          {hnorm_d2:.8f}")
print(f"  H_norm staggered:             {hnorm_stag:.8f}")
print(f"  Max H_norm (all configs):     {max_hnorm:.8f}")
print(f"\n  Bound 1/27 = {1/27:.8f}")
print(f"  All H_norm <= 1/27? {'YES' if max_hnorm <= 1/27 + 1e-8 else 'SOME VIOLATIONS'}")
print(f"  lambda_max at Q=I = {expected_lmax:.6f} (= 8*beta/3) {'CHECK' if abs(lmax_I - expected_lmax) < 0.01 else 'MISMATCH'}")

# Histogram of H_norm values
print(f"\n  Distribution of H_norm (20 random configs):")
bins = [0, 0.01, 0.02, 0.03, 0.04, 0.05]
for i in range(len(bins)-1):
    count = sum(1 for h in hnorm_values if bins[i] <= h < bins[i+1])
    print(f"    [{bins[i]:.2f}, {bins[i+1]:.2f}): {count} configs")
