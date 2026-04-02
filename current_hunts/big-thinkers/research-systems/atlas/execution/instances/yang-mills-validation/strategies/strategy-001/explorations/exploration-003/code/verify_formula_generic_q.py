"""
CRITICAL VERIFICATION: Does HessS = (β/(2N)) v^T M(Q) v hold for generic Q?

E007 claims the formula is only exact at flat connections.
This test compares the ACTUAL Hessian (via finite differences of S)
against the B²-FORMULA Hessian ((β/(2N)) Σ B^T B) at RANDOM Q.

If they disagree, the entire β < 1/6 proof chain needs re-examination.
"""
import numpy as np
from itertools import product as iproduct

L = 2
d = 4
N = 2
beta = 1.0

n_sites = L**d
n_links = d * n_sites
n_gen = N**2 - 1
n_dof = n_links * n_gen

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

def adjoint_rep(g):
    R = np.zeros((3, 3))
    for a in range(3):
        for c in range(3):
            R[c, a] = -2 * np.real(np.trace(tau[c] @ g @ tau[a] @ g.conj().T))
    return R

def su2_exp(M):
    theta_sq = -2 * np.real(np.trace(M @ M))
    if theta_sq < 1e-20:
        return np.eye(2, dtype=complex) + M + M @ M / 2 + M @ M @ M / 6
    theta = np.sqrt(theta_sq)
    return np.cos(theta/2) * np.eye(2, dtype=complex) + (2.0/theta) * np.sin(theta/2) * M

def random_su2():
    a = np.random.randn(4)
    a /= np.linalg.norm(a)
    return a[0] * np.eye(2, dtype=complex) + 1j * sum(a[k+1] * sigma[k] for k in range(3))

def wilson_action(U, plaq_list, beta, N):
    S = 0.0
    for plaq in plaq_list:
        e1, s1 = plaq[0]; e2, s2 = plaq[1]
        e3, s3 = plaq[2]; e4, s4 = plaq[3]
        U_plaq = U[e1] @ U[e2] @ U[e3].conj().T @ U[e4].conj().T
        S += np.real(np.trace(U_plaq))
    return -beta / N * S

def build_hessian_LEFT_formula(U, plaq_list, beta, N, n_dof, n_links, n_gen):
    """Build Hessian from B_square formula (β/(2N)) Σ B^T B"""
    H = np.zeros((n_dof, n_dof))
    prefactor = beta / (2 * N)
    for plaq in plaq_list:
        e_idx = [plaq[k][0] for k in range(4)]
        signs = [plaq[k][1] for k in range(4)]
        U1, U2, U3, U4 = [U[e_idx[k]] for k in range(4)]
        P1 = np.eye(N, dtype=complex)
        P2 = U1
        P3 = U1 @ U2 @ U3.conj().T
        P4 = U1 @ U2 @ U3.conj().T @ U4.conj().T
        Rs = [adjoint_rep(P) for P in [P1, P2, P3, P4]]
        for ie in range(4):
            for je in range(4):
                block = prefactor * signs[ie] * signs[je] * Rs[ie].T @ Rs[je]
                ei, ej = e_idx[ie], e_idx[je]
                H[ei*n_gen:(ei+1)*n_gen, ej*n_gen:(ej+1)*n_gen] += block
    return H

def build_hessian_FD(U, plaq_list, beta, N, n_dof, n_links, n_gen, eps=1e-5):
    """Build ACTUAL Hessian from finite differences of S (left perturbation)."""
    H = np.zeros((n_dof, n_dof))
    S0 = wilson_action(U, plaq_list, beta, N)

    for ia in range(n_dof):
        li = ia // n_gen
        ga = ia % n_gen

        for jb in range(ia, n_dof):
            lj = jb // n_gen
            gb = jb % n_gen

            if ia == jb:
                Up = U.copy(); Um = U.copy()
                Up[li] = su2_exp(eps * tau[ga]) @ U[li]
                Um[li] = su2_exp(-eps * tau[ga]) @ U[li]
                Sp = wilson_action(Up, plaq_list, beta, N)
                Sm = wilson_action(Um, plaq_list, beta, N)
                H[ia, ia] = (Sp - 2*S0 + Sm) / eps**2
            else:
                if li == lj:
                    # Same link, different generators
                    Upp = U.copy()
                    Upp[li] = su2_exp(eps * tau[gb]) @ su2_exp(eps * tau[ga]) @ U[li]
                    Upm = U.copy()
                    Upm[li] = su2_exp(-eps * tau[gb]) @ su2_exp(eps * tau[ga]) @ U[li]
                    Ump = U.copy()
                    Ump[li] = su2_exp(eps * tau[gb]) @ su2_exp(-eps * tau[ga]) @ U[li]
                    Umm = U.copy()
                    Umm[li] = su2_exp(-eps * tau[gb]) @ su2_exp(-eps * tau[ga]) @ U[li]
                else:
                    # Different links
                    Upp = U.copy()
                    Upp[li] = su2_exp(eps * tau[ga]) @ U[li]
                    Upp[lj] = su2_exp(eps * tau[gb]) @ U[lj]
                    Upm = U.copy()
                    Upm[li] = su2_exp(eps * tau[ga]) @ U[li]
                    Upm[lj] = su2_exp(-eps * tau[gb]) @ U[lj]
                    Ump = U.copy()
                    Ump[li] = su2_exp(-eps * tau[ga]) @ U[li]
                    Ump[lj] = su2_exp(eps * tau[gb]) @ U[lj]
                    Umm = U.copy()
                    Umm[li] = su2_exp(-eps * tau[ga]) @ U[li]
                    Umm[lj] = su2_exp(-eps * tau[gb]) @ U[lj]

                Spp = wilson_action(Upp, plaq_list, beta, N)
                Spm = wilson_action(Upm, plaq_list, beta, N)
                Smp = wilson_action(Ump, plaq_list, beta, N)
                Smm = wilson_action(Umm, plaq_list, beta, N)
                H[ia, jb] = (Spp - Spm - Smp + Smm) / (4 * eps**2)
                H[jb, ia] = H[ia, jb]
    return H

# ============================================================
# TEST: Compare B²-formula vs FD at RANDOM Q
# ============================================================
print("=" * 60)
print("CRITICAL TEST: B² formula vs actual Hessian at random Q")
print("=" * 60)

np.random.seed(42)

# Test 1: Q=I (should agree perfectly)
print("\n--- Q=I (flat, should agree) ---")
U_I = np.array([np.eye(2, dtype=complex) for _ in range(n_links)])
H_formula_I = build_hessian_LEFT_formula(U_I, plaquette_links, beta, N, n_dof, n_links, n_gen)
# Only check a few FD elements at Q=I
eps = 1e-5
S0 = wilson_action(U_I, plaquette_links, beta, N)
for ia in [0, 1, 50, 100]:
    Up = U_I.copy(); Um = U_I.copy()
    li, ga = ia // n_gen, ia % n_gen
    Up[li] = su2_exp(eps * tau[ga]) @ U_I[li]
    Um[li] = su2_exp(-eps * tau[ga]) @ U_I[li]
    Sp = wilson_action(Up, plaquette_links, beta, N)
    Sm = wilson_action(Um, plaquette_links, beta, N)
    H_fd = (Sp - 2*S0 + Sm) / eps**2
    print(f"  H[{ia},{ia}]: formula={H_formula_I[ia,ia]:.8f}, FD={H_fd:.8f}, diff={abs(H_formula_I[ia,ia]-H_fd):.2e}")

# Test 2: RANDOM Q (this is the critical test)
print("\n--- RANDOM Q (non-flat, critical test) ---")
U_rand = np.array([random_su2() for _ in range(n_links)])

# Check plaquette values
plaq_vals = []
for plaq in plaquette_links[:3]:
    e1 = plaq[0][0]; e2 = plaq[1][0]; e3 = plaq[2][0]; e4 = plaq[3][0]
    U_plaq = U_rand[e1] @ U_rand[e2] @ U_rand[e3].conj().T @ U_rand[e4].conj().T
    plaq_vals.append(np.real(np.trace(U_plaq)))
print(f"  Sample plaquette values: {[f'{v:.4f}' for v in plaq_vals]}")
print(f"  (Should be near 0 for random Q, near 2 for flat Q)")

# Build BOTH Hessians at random Q
print("\n  Building B²-formula Hessian...")
H_formula = build_hessian_LEFT_formula(U_rand, plaquette_links, beta, N, n_dof, n_links, n_gen)

print("  Building FD Hessian (this takes a while, 192x192 = ~18K FD evaluations)...")
H_fd_full = build_hessian_FD(U_rand, plaquette_links, beta, N, n_dof, n_links, n_gen, eps=1e-5)

# Compare
evals_formula = np.sort(np.linalg.eigvalsh(H_formula))[::-1]
evals_fd = np.sort(np.linalg.eigvalsh(H_fd_full))[::-1]

print(f"\n  B²-formula λ_max: {evals_formula[0]:.6f}")
print(f"  FD (actual) λ_max: {evals_fd[0]:.6f}")
print(f"  Difference: {abs(evals_formula[0] - evals_fd[0]):.6f}")
print(f"  Ratio actual/formula: {evals_fd[0] / evals_formula[0]:.6f}")

print(f"\n  B²-formula H_norm: {evals_formula[0]/(48*beta):.6f}")
print(f"  FD (actual) H_norm: {evals_fd[0]/(48*beta):.6f}")

# Check element-by-element
max_diff = np.max(np.abs(H_formula - H_fd_full))
frobenius_diff = np.linalg.norm(H_formula - H_fd_full)
frobenius_formula = np.linalg.norm(H_formula)
print(f"\n  Max element-wise difference: {max_diff:.6f}")
print(f"  Frobenius norm of difference: {frobenius_diff:.6f}")
print(f"  Frobenius norm of H_formula: {frobenius_formula:.6f}")
print(f"  Relative Frobenius: {frobenius_diff/frobenius_formula:.6f}")

# Check a few diagonal elements
print(f"\n  Diagonal element comparison:")
for ia in [0, 1, 2, 50, 100, 150]:
    print(f"    H[{ia},{ia}]: formula={H_formula[ia,ia]:.6f}, FD={H_fd_full[ia,ia]:.6f}, diff={abs(H_formula[ia,ia]-H_fd_full[ia,ia]):.4f}")

# Check if formula systematically over/underestimates
diag_formula = np.diag(H_formula)
diag_fd = np.diag(H_fd_full)
n_overestimate = np.sum(diag_formula > diag_fd + 1e-4)
n_underestimate = np.sum(diag_formula < diag_fd - 1e-4)
print(f"\n  Diagonal: formula overestimates {n_overestimate} elements, underestimates {n_underestimate}")

print("\n" + "=" * 60)
if max_diff < 0.01:
    print("VERDICT: Formula AGREES with FD at random Q")
    print("E007's claim of a critical flaw appears to be WRONG")
    print("The B² formula IS the correct covariant Hessian")
else:
    print("VERDICT: Formula DISAGREES with FD at random Q")
    print(f"Max difference: {max_diff:.6f}")
    if evals_fd[0] > evals_formula[0] + 0.01:
        print("Actual Hessian LARGER than formula → proof may be invalid")
        print(f"Actual λ_max = {evals_fd[0]:.6f} > formula λ_max = {evals_formula[0]:.6f}")
    elif evals_fd[0] < evals_formula[0] - 0.01:
        print("Actual Hessian SMALLER than formula → formula is an upper bound → proof is still valid")
        print(f"Actual λ_max = {evals_fd[0]:.6f} < formula λ_max = {evals_formula[0]:.6f}")
    else:
        print(f"λ_max similar but matrix elements differ — needs more investigation")
print("=" * 60)
