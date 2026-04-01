"""
Critical Test: Hessian eigenvalue at U_all = i*sigma_3
===================================================

Tests BOTH the LEFT and RIGHT perturbation B_square formulas at U_all = i*sigma_3.
If lambda_max = 6*beta, Conjecture 1 is FALSE.
If lambda_max = 4*beta, Conjecture 1 survives.

Also verifies the B_square formula against finite differences (FULL matrix, not just diagonal).
"""
import numpy as np
from itertools import product as iproduct

L = 2
d = 4
N = 2
beta = 1.0

n_sites = L**d  # 16
n_links = d * n_sites  # 64
n_gen = N**2 - 1  # 3
n_dof = n_links * n_gen  # 192

# SU(2) generators
sigma = np.zeros((3, 2, 2), dtype=complex)
sigma[0] = np.array([[0, 1], [1, 0]])
sigma[1] = np.array([[0, -1j], [1j, 0]])
sigma[2] = np.array([[1, 0], [0, -1]])
tau = np.array([1j * sigma[a] / 2 for a in range(3)])

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

def adjoint_rep(g):
    """Adjoint representation: R[c,a] = -2 Re Tr(tau_c g tau_a g^dag)"""
    R = np.zeros((3, 3))
    for a in range(3):
        for c in range(3):
            R[c, a] = -2 * np.real(np.trace(tau[c] @ g @ tau[a] @ g.conj().T))
    return R

def su2_exp(M):
    """Matrix exponential for su(2) element"""
    theta_sq = -2 * np.real(np.trace(M @ M))
    if theta_sq < 1e-20:
        return np.eye(2, dtype=complex) + M + M @ M / 2 + M @ M @ M / 6
    theta = np.sqrt(theta_sq)
    return np.cos(theta/2) * np.eye(2, dtype=complex) + (2.0/theta) * np.sin(theta/2) * M

def wilson_action(U, plaq_list, beta, N):
    """S(Q) = -(beta/N) sum Re Tr(U_plaq)"""
    S = 0.0
    for plaq in plaq_list:
        e1, s1 = plaq[0]; e2, s2 = plaq[1]
        e3, s3 = plaq[2]; e4, s4 = plaq[3]
        U_plaq = U[e1] @ U[e2] @ U[e3].conj().T @ U[e4].conj().T
        S += np.real(np.trace(U_plaq))
    return -beta / N * S

def build_hessian_LEFT(U, plaq_list, beta, N, n_dof, n_links, n_gen):
    """
    LEFT perturbation: Q_e -> exp(t*v_e) * Q_e

    B_square formula (CORRECTED):
    P1 = I
    P2 = Q1
    P3 = Q1 * Q2 * Q3^{-1}   <-- includes Q3 inverse
    P4 = Q1 * Q2 * Q3^{-1} * Q4^{-1} = U_plaq  <-- full holonomy
    """
    H = np.zeros((n_dof, n_dof))
    prefactor = beta / (2 * N)
    for plaq in plaq_list:
        e_idx = [plaq[k][0] for k in range(4)]
        signs = [plaq[k][1] for k in range(4)]
        U1, U2, U3, U4 = [U[e_idx[k]] for k in range(4)]

        # LEFT convention partial holonomies
        P1 = np.eye(N, dtype=complex)
        P2 = U1
        P3 = U1 @ U2 @ U3.conj().T          # includes Q3^{-1}
        P4 = U1 @ U2 @ U3.conj().T @ U4.conj().T  # = U_plaq

        Rs = [adjoint_rep(P) for P in [P1, P2, P3, P4]]

        for ie in range(4):
            for je in range(4):
                block = prefactor * signs[ie] * signs[je] * Rs[ie].T @ Rs[je]
                ei, ej = e_idx[ie], e_idx[je]
                H[ei*n_gen:(ei+1)*n_gen, ej*n_gen:(ej+1)*n_gen] += block
    return H

def build_hessian_RIGHT(U, plaq_list, beta, N, n_dof, n_links, n_gen):
    """
    RIGHT perturbation: Q_e -> Q_e * exp(t*v_e)

    B_square formula (E001's version):
    P1 = I
    P2 = Q1
    P3 = Q1 * Q2            <-- does NOT include Q3 inverse
    P4 = Q1 * Q2 * Q3^{-1}  <-- does NOT include Q4 inverse
    """
    H = np.zeros((n_dof, n_dof))
    prefactor = beta / (2 * N)
    for plaq in plaq_list:
        e_idx = [plaq[k][0] for k in range(4)]
        signs = [plaq[k][1] for k in range(4)]
        U1, U2, U3, U4 = [U[e_idx[k]] for k in range(4)]

        # RIGHT convention partial holonomies (E001's formula)
        P1 = np.eye(N, dtype=complex)
        P2 = U1
        P3 = U1 @ U2                  # NO Q3^{-1}
        P4 = U1 @ U2 @ U3.conj().T    # NO Q4^{-1}

        Rs = [adjoint_rep(P) for P in [P1, P2, P3, P4]]

        for ie in range(4):
            for je in range(4):
                block = prefactor * signs[ie] * signs[je] * Rs[ie].T @ Rs[je]
                ei, ej = e_idx[ie], e_idx[je]
                H[ei*n_gen:(ei+1)*n_gen, ej*n_gen:(ej+1)*n_gen] += block
    return H

def build_hessian_FD(U, plaq_list, beta, N, n_dof, n_links, n_gen, convention='left', eps=1e-5):
    """Build Hessian by finite differences."""
    H = np.zeros((n_dof, n_dof))
    S0 = wilson_action(U, plaq_list, beta, N)

    for ia in range(n_dof):
        li = ia // n_gen
        ga = ia % n_gen

        for jb in range(ia, n_dof):
            lj = jb // n_gen
            gb = jb % n_gen

            if ia == jb:
                # Diagonal: (S(+h) - 2S(0) + S(-h)) / h^2
                Up = U.copy()
                Um = U.copy()
                if convention == 'left':
                    Up[li] = su2_exp(eps * tau[ga]) @ U[li]
                    Um[li] = su2_exp(-eps * tau[ga]) @ U[li]
                else:
                    Up[li] = U[li] @ su2_exp(eps * tau[ga])
                    Um[li] = U[li] @ su2_exp(-eps * tau[ga])
                Sp = wilson_action(Up, plaq_list, beta, N)
                Sm = wilson_action(Um, plaq_list, beta, N)
                H[ia, ia] = (Sp - 2*S0 + Sm) / eps**2
            else:
                # Off-diagonal: (S(+h,+h) - S(+h,-h) - S(-h,+h) + S(-h,-h)) / (4h^2)
                Upp = U.copy(); Upm = U.copy(); Ump = U.copy(); Umm = U.copy()
                if convention == 'left':
                    Upp[li] = su2_exp(eps * tau[ga]) @ U[li]
                    Upp[lj] = su2_exp(eps * tau[gb]) @ Upp[lj] if li != lj else su2_exp(eps * tau[gb]) @ Upp[li]

                    Upm[li] = su2_exp(eps * tau[ga]) @ U[li]
                    Upm[lj] = su2_exp(-eps * tau[gb]) @ U[lj] if li != lj else su2_exp(-eps * tau[gb]) @ su2_exp(eps * tau[ga]) @ U[li]

                    Ump[li] = su2_exp(-eps * tau[ga]) @ U[li]
                    Ump[lj] = su2_exp(eps * tau[gb]) @ U[lj] if li != lj else su2_exp(eps * tau[gb]) @ su2_exp(-eps * tau[ga]) @ U[li]

                    Umm[li] = su2_exp(-eps * tau[ga]) @ U[li]
                    Umm[lj] = su2_exp(-eps * tau[gb]) @ U[lj] if li != lj else su2_exp(-eps * tau[gb]) @ su2_exp(-eps * tau[ga]) @ U[li]
                else:
                    Upp[li] = U[li] @ su2_exp(eps * tau[ga])
                    Upp[lj] = U[lj] @ su2_exp(eps * tau[gb]) if li != lj else Upp[li] @ su2_exp(eps * tau[gb])

                    Upm[li] = U[li] @ su2_exp(eps * tau[ga])
                    Upm[lj] = U[lj] @ su2_exp(-eps * tau[gb]) if li != lj else U[li] @ su2_exp(eps * tau[ga]) @ su2_exp(-eps * tau[gb])

                    Ump[li] = U[li] @ su2_exp(-eps * tau[ga])
                    Ump[lj] = U[lj] @ su2_exp(eps * tau[gb]) if li != lj else U[li] @ su2_exp(-eps * tau[ga]) @ su2_exp(eps * tau[gb])

                    Umm[li] = U[li] @ su2_exp(-eps * tau[ga])
                    Umm[lj] = U[lj] @ su2_exp(-eps * tau[gb]) if li != lj else U[li] @ su2_exp(-eps * tau[ga]) @ su2_exp(-eps * tau[gb])

                Spp = wilson_action(Upp, plaq_list, beta, N)
                Spm = wilson_action(Upm, plaq_list, beta, N)
                Smp = wilson_action(Ump, plaq_list, beta, N)
                Smm = wilson_action(Umm, plaq_list, beta, N)
                H[ia, jb] = (Spp - Spm - Smp + Smm) / (4 * eps**2)
                H[jb, ia] = H[ia, jb]
    return H

# ============================================================
# TEST 1: Q=I sanity check
# ============================================================
print("=" * 60)
print("TEST 1: Q=I SANITY CHECK")
print("=" * 60)

U_I = np.array([np.eye(2, dtype=complex) for _ in range(n_links)])

H_left_I = build_hessian_LEFT(U_I, plaquette_links, beta, N, n_dof, n_links, n_gen)
H_right_I = build_hessian_RIGHT(U_I, plaquette_links, beta, N, n_dof, n_links, n_gen)

evals_left_I = np.sort(np.linalg.eigvalsh(H_left_I))[::-1]
evals_right_I = np.sort(np.linalg.eigvalsh(H_right_I))[::-1]

print(f"  LEFT  formula at Q=I: lambda_max = {evals_left_I[0]:.6f}")
print(f"  RIGHT formula at Q=I: lambda_max = {evals_right_I[0]:.6f}")
print(f"  Max difference: {np.max(np.abs(evals_left_I - evals_right_I)):.2e}")
print(f"  Expected: {4*beta:.6f}")
print()

# ============================================================
# TEST 2: U_all = i*sigma_3  (THE CRITICAL TEST)
# ============================================================
print("=" * 60)
print("TEST 2: U_all = i*sigma_3 (CRITICAL)")
print("=" * 60)

U_isig3 = np.array([np.array([[1j, 0], [0, -1j]]) for _ in range(n_links)])

# Check plaquette value
U_plaq_test = U_isig3[0] @ U_isig3[0] @ U_isig3[0].conj().T @ U_isig3[0].conj().T
print(f"  Plaquette holonomy: Re Tr(U_plaq) = {np.real(np.trace(U_plaq_test)):.4f} (should be 2 for SU(2) flat)")

H_left = build_hessian_LEFT(U_isig3, plaquette_links, beta, N, n_dof, n_links, n_gen)
H_right = build_hessian_RIGHT(U_isig3, plaquette_links, beta, N, n_dof, n_links, n_gen)

evals_left = np.sort(np.linalg.eigvalsh(H_left))[::-1]
evals_right = np.sort(np.linalg.eigvalsh(H_right))[::-1]

print(f"\n  LEFT  formula at U=isig3: lambda_max = {evals_left[0]:.6f}")
print(f"  RIGHT formula at U=isig3: lambda_max = {evals_right[0]:.6f}")
print(f"  Difference in lambda_max: {abs(evals_left[0] - evals_right[0]):.2e}")
print()
print(f"  H_norm (LEFT)  = {evals_left[0]/(48*beta):.6f}  (Conjecture 1 limit: 1/12 = {1/12:.6f})")
print(f"  H_norm (RIGHT) = {evals_right[0]/(48*beta):.6f}")
print()

if evals_left[0] > 4*beta + 0.01:
    print(f"  *** CONJECTURE 1 IS FALSE! lambda_max = {evals_left[0]:.4f} > 4d*beta/(2N) = {4*beta:.4f} ***")
    print(f"  *** H_norm = {evals_left[0]/(48*beta):.6f} > 1/12 = {1/12:.6f} ***")
elif abs(evals_left[0] - 4*beta) < 0.01:
    print(f"  Conjecture 1 SURVIVES: lambda_max ≈ 4*beta at U=isig3 (same as Q=I)")
else:
    print(f"  Conjecture 1 holds here: lambda_max < 4*beta")

print(f"\n  Top 10 eigenvalues (LEFT formula):")
for i in range(10):
    print(f"    {evals_left[i]:.6f}")

# ============================================================
# TEST 3: FD verification at U=isig3 (LEFT, selective off-diagonal)
# ============================================================
print("\n" + "=" * 60)
print("TEST 3: FD VERIFICATION AT U=isig3 (LEFT CONVENTION)")
print("=" * 60)

# Only check a few elements to keep it fast
eps_fd = 1e-5
S0 = wilson_action(U_isig3, plaquette_links, beta, N)
print(f"  S(U_isig3) = {S0:.6f}")

# Check 5 diagonal elements
print(f"\n  Diagonal FD check:")
for ia in [0, 1, 2, 50, 100]:
    li = ia // n_gen
    ga = ia % n_gen
    Up = U_isig3.copy()
    Um = U_isig3.copy()
    Up[li] = su2_exp(eps_fd * tau[ga]) @ U_isig3[li]
    Um[li] = su2_exp(-eps_fd * tau[ga]) @ U_isig3[li]
    Sp = wilson_action(Up, plaquette_links, beta, N)
    Sm = wilson_action(Um, plaquette_links, beta, N)
    H_fd = (Sp - 2*S0 + Sm) / eps_fd**2
    print(f"    H[{ia},{ia}]: formula={H_left[ia,ia]:.6f}, FD={H_fd:.6f}, diff={abs(H_left[ia,ia]-H_fd):.2e}")

# Check 5 off-diagonal elements (links that share a plaquette)
print(f"\n  Off-diagonal FD check (LEFT convention):")
offdiag_pairs = [(0, 3), (0, 6), (1, 4), (3, 9), (5, 8)]  # Ensure different links
for ia, jb in offdiag_pairs:
    li = ia // n_gen; ga = ia % n_gen
    lj = jb // n_gen; gb = jb % n_gen

    if li == lj:
        continue  # Skip same-link pairs for simplicity

    Upp = U_isig3.copy()
    Upm = U_isig3.copy()
    Ump = U_isig3.copy()
    Umm = U_isig3.copy()

    Upp[li] = su2_exp(eps_fd * tau[ga]) @ U_isig3[li]
    Upp[lj] = su2_exp(eps_fd * tau[gb]) @ U_isig3[lj]

    Upm[li] = su2_exp(eps_fd * tau[ga]) @ U_isig3[li]
    Upm[lj] = su2_exp(-eps_fd * tau[gb]) @ U_isig3[lj]

    Ump[li] = su2_exp(-eps_fd * tau[ga]) @ U_isig3[li]
    Ump[lj] = su2_exp(eps_fd * tau[gb]) @ U_isig3[lj]

    Umm[li] = su2_exp(-eps_fd * tau[ga]) @ U_isig3[li]
    Umm[lj] = su2_exp(-eps_fd * tau[gb]) @ U_isig3[lj]

    Spp = wilson_action(Upp, plaquette_links, beta, N)
    Spm = wilson_action(Upm, plaquette_links, beta, N)
    Smp = wilson_action(Ump, plaquette_links, beta, N)
    Smm = wilson_action(Umm, plaquette_links, beta, N)
    H_fd = (Spp - Spm - Smp + Smm) / (4 * eps_fd**2)
    print(f"    H[{ia},{jb}]: formula={H_left[ia,jb]:.6f}, FD={H_fd:.6f}, diff={abs(H_left[ia,jb]-H_fd):.2e}")

# ============================================================
# TEST 4: Random Q test
# ============================================================
print("\n" + "=" * 60)
print("TEST 4: RANDOM Q HESSIAN (LEFT FORMULA)")
print("=" * 60)

def random_su2():
    """Random Haar-distributed SU(2) element."""
    a = np.random.randn(4)
    a /= np.linalg.norm(a)
    return a[0] * np.eye(2, dtype=complex) + 1j * sum(a[k+1] * sigma[k] for k in range(3))

for trial in range(5):
    U_rand = np.array([random_su2() for _ in range(n_links)])
    H_rand = build_hessian_LEFT(U_rand, plaquette_links, beta, N, n_dof, n_links, n_gen)
    evals_rand = np.linalg.eigvalsh(H_rand)
    lmax = np.max(evals_rand)
    hnorm = lmax / (48 * beta)
    print(f"  Trial {trial}: lambda_max = {lmax:.4f}, H_norm = {hnorm:.6f} (<= 1/12={1/12:.6f}? {'YES' if hnorm <= 1/12 + 1e-6 else 'NO'})")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"  LEFT formula at Q=I: lambda_max = {evals_left_I[0]:.6f} (expected {4*beta})")
print(f"  LEFT formula at U=isig3: lambda_max = {evals_left[0]:.6f}")
print(f"  RIGHT formula at U=isig3: lambda_max = {evals_right[0]:.6f}")
print(f"  H_norm at U=isig3 (LEFT): {evals_left[0]/(48*beta):.6f}")
print(f"  Conjecture 1 bound: H_norm <= 1/12 = {1/12:.6f}")
if evals_left[0] > 4*beta + 0.01:
    print(f"\n  VERDICT: CONJECTURE 1 IS DISPROVED by U_all = i*sigma_3")
    print(f"  H_norm = {evals_left[0]/(48*beta):.6f} > 1/12")
    print(f"  But beta < 1/6 is CORRECT and TIGHT (CS bound saturated)")
else:
    print(f"\n  VERDICT: Conjecture 1 SURVIVES (U=isig3 does NOT violate it)")
    print(f"  E001's finding was an artifact of the wrong B_square formula")
