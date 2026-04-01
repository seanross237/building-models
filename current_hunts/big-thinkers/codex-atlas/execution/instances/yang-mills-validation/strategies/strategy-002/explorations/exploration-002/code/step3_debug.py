"""
Debug: Compare one-parameter d²S/dt² along random directions v
between FD and analytical formula.

This tests the formula WITHOUT needing to build the full Hessian matrix.
"""

import numpy as np
from scipy.linalg import expm

np.random.seed(42)

# SU(2) utilities
sigma = [
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
]
T_gen = [1j * s / 2 for s in sigma]
I2 = np.eye(2, dtype=complex)

def su2_from_vec(v):
    return sum(vi * ti for vi, ti in zip(v, T_gen))

def su2_to_vec(X):
    return np.array([-2.0 * np.trace(t @ X).real for t in T_gen])

def Ad(Q, v_mat):
    return Q @ v_mat @ Q.conj().T

def re_tr(M):
    return np.trace(M).real

def random_SU2():
    return expm(sum(a * t for a, t in zip(np.random.randn(3), T_gen)))

# Lattice
L = 2
d = 4
Nsites = L**d
Nlinks = d * Nsites
Ndof = 3 * Nlinks

def site_index(x):
    idx = 0
    for i in range(d):
        idx = idx * L + (x[i] % L)
    return idx

def site_coords(idx):
    x = []
    for i in range(d):
        x.append(idx % L)
        idx //= L
    return list(reversed(x))

def link_index(x, mu):
    return mu * Nsites + site_index(x)

def neighbor(x, mu, direction=1):
    y = list(x)
    y[mu] = (y[mu] + direction) % L
    return y

Q = np.zeros((Nlinks, 2, 2), dtype=complex)
for i in range(Nlinks):
    Q[i] = random_SU2()

# Enumerate plaquettes
plaquettes = []
for s in range(Nsites):
    x = site_coords(s)
    for mu in range(d):
        for nu in range(mu+1, d):
            e1 = link_index(x, mu)
            e2 = link_index(neighbor(x, mu), nu)
            e3 = link_index(neighbor(x, nu), mu)
            e4 = link_index(x, nu)
            plaquettes.append((e1, e2, e3, e4))

beta = 1.0

def wilson_action():
    S = 0.0
    for (e1, e2, e3, e4) in plaquettes:
        U = Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T
        S -= (beta / 2) * re_tr(U)
    return S

def perturb_config(v_vec, t):
    """Apply Q_e → exp(t v_e) Q_e for all links."""
    Q_new = Q.copy()
    for e in range(Nlinks):
        v_mat = su2_from_vec(v_vec[3*e:3*e+3])
        Q_new[e] = expm(t * v_mat) @ Q[e]
    return Q_new

def wilson_action_with_config(Q_cfg):
    S = 0.0
    for (e1, e2, e3, e4) in plaquettes:
        U = Q_cfg[e1] @ Q_cfg[e2] @ Q_cfg[e3].conj().T @ Q_cfg[e4].conj().T
        S -= (beta / 2) * re_tr(U)
    return S

def fd_second_deriv(v_vec, h=1e-4):
    """d²S/dt² along direction v by central FD."""
    Qp = perturb_config(v_vec, h)
    Q0 = perturb_config(v_vec, 0)
    Qm = perturb_config(v_vec, -h)
    Sp = wilson_action_with_config(Qp)
    S0 = wilson_action_with_config(Q0)
    Sm = wilson_action_with_config(Qm)
    return (Sp - 2 * S0 + Sm) / h**2

def analytical_second_deriv(v_vec):
    """
    d²S/dt² = -(β/2) Σ□ [Re Tr(w²U) + Σ_{i<j} Re Tr([wᵢ,wⱼ]U)]

    where for each plaquette:
    w = Σ sₖ Ad_{Pₖ}(v_{eₖ}), wₖ = sₖ Ad_{Pₖ}(v_{eₖ})
    """
    result = 0.0
    for (e1, e2, e3, e4) in plaquettes:
        U = Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T

        # Partial holonomies
        P2 = Q[e1].copy()
        P3 = Q[e1] @ Q[e2] @ Q[e3].conj().T

        # Perturbation vectors (as su(2) matrices)
        v1 = su2_from_vec(v_vec[3*e1:3*e1+3])
        v2 = su2_from_vec(v_vec[3*e2:3*e2+3])
        v3 = su2_from_vec(v_vec[3*e3:3*e3+3])
        v4 = su2_from_vec(v_vec[3*e4:3*e4+3])

        # Rotated perturbations
        w1 = v1
        w2 = Ad(P2, v2)
        w3 = -Ad(P3, v3)
        w4 = -Ad(U, v4)

        w = w1 + w2 + w3 + w4
        ws = [w1, w2, w3, w4]

        # w² term
        w2_term = re_tr(w @ w @ U)

        # Commutator terms
        comm_term = 0.0
        for i in range(4):
            for j in range(i+1, 4):
                comm = ws[i] @ ws[j] - ws[j] @ ws[i]
                comm_term += re_tr(comm @ U)

        result += -(beta / 2) * (w2_term + comm_term)

    return result

def formula_second_deriv(v_vec):
    """
    H_formula(v,v) = (β/4) Σ□ |w□|²
    """
    result = 0.0
    for (e1, e2, e3, e4) in plaquettes:
        U = Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T
        P2 = Q[e1].copy()
        P3 = Q[e1] @ Q[e2] @ Q[e3].conj().T

        v1 = su2_from_vec(v_vec[3*e1:3*e1+3])
        v2 = su2_from_vec(v_vec[3*e2:3*e2+3])
        v3 = su2_from_vec(v_vec[3*e3:3*e3+3])
        v4 = su2_from_vec(v_vec[3*e4:3*e4+3])

        w1 = v1
        w2 = Ad(P2, v2)
        w3 = -Ad(P3, v3)
        w4 = -Ad(U, v4)

        w = w1 + w2 + w3 + w4
        w_norm_sq = -2.0 * np.trace(w @ w).real

        result += (beta / 4) * w_norm_sq

    return result

# ============================================================
# Test: Compare d²S/dt² along random directions
# ============================================================

print("=" * 70)
print("ONE-PARAMETER SECOND DERIVATIVE COMPARISON")
print("=" * 70)

for trial in range(10):
    v = np.random.randn(Ndof)
    v /= np.linalg.norm(v)  # normalize

    fd = fd_second_deriv(v)
    ana = analytical_second_deriv(v)
    form = formula_second_deriv(v)

    print(f"\nTrial {trial+1}:")
    print(f"  FD       = {fd:+.8f}")
    print(f"  Analyt.  = {ana:+.8f}")
    print(f"  Formula  = {form:+.8f}")
    print(f"  |FD-Ana| = {abs(fd-ana):.2e}")
    print(f"  |FD-Form|= {abs(fd-form):.2e}")

# ============================================================
# Test: Build Hessian from one-parameter formula and compare
# ============================================================

print("\n\n" + "=" * 70)
print("HESSIAN FROM QUADRATIC FORM (using polarization identity)")
print("=" * 70)

# Build Hessian by computing v^T H v for basis vectors
# H_{ij} = (1/2)(f(eᵢ+eⱼ) - f(eᵢ) - f(eⱼ)) where f(v) = v^T H v = d²S/dt²

# Only build a 10×10 subblock for speed
N_test = 10

H_polar = np.zeros((N_test, N_test))
H_fd_sub = np.zeros((N_test, N_test))

# First compute f(eᵢ) for each basis vector
f_ei = np.zeros(N_test)
for i in range(N_test):
    ei = np.zeros(Ndof)
    ei[i] = 1.0
    f_ei[i] = analytical_second_deriv(ei)

# Then compute f(eᵢ + eⱼ) for pairs
for i in range(N_test):
    H_polar[i, i] = f_ei[i]
    for j in range(i+1, N_test):
        eij = np.zeros(Ndof)
        eij[i] = 1.0
        eij[j] = 1.0
        f_eij = analytical_second_deriv(eij)
        H_polar[i, j] = 0.5 * (f_eij - f_ei[i] - f_ei[j])
        H_polar[j, i] = H_polar[i, j]

# Build FD Hessian for same subblock
S0 = wilson_action()
h = 1e-4

for i in range(N_test):
    li, ci = divmod(i, 3)
    old = Q[li].copy()
    Q[li] = expm(h * T_gen[ci]) @ Q[li]
    Sp = wilson_action()
    Q[li] = old
    Q[li] = expm(-h * T_gen[ci]) @ Q[li]
    Sm = wilson_action()
    Q[li] = old
    H_fd_sub[i, i] = (Sp - 2 * S0 + Sm) / h**2

for i in range(N_test):
    li, ci = divmod(i, 3)
    for j in range(i+1, N_test):
        lj, cj = divmod(j, 3)

        old_i, old_j = Q[li].copy(), Q[lj].copy()

        Q[li] = expm(h*T_gen[ci]) @ old_i
        Q[lj] = expm(h*T_gen[cj]) @ old_j
        Spp = wilson_action()

        Q[lj] = expm(-h*T_gen[cj]) @ old_j
        Spm = wilson_action()
        Q[lj] = old_j
        Q[li] = old_i

        Q[li] = expm(-h*T_gen[ci]) @ old_i
        Q[lj] = expm(h*T_gen[cj]) @ old_j
        Smp = wilson_action()

        Q[lj] = expm(-h*T_gen[cj]) @ old_j
        Smm = wilson_action()
        Q[lj] = old_j
        Q[li] = old_i

        H_fd_sub[i, j] = (Spp - Spm - Smp + Smm) / (4 * h**2)
        H_fd_sub[j, i] = H_fd_sub[i, j]

print("\nComparison of 10×10 subblock:")
print(f"  |H_polar - H_fd|_max = {np.max(np.abs(H_polar - H_fd_sub)):.6e}")
print(f"  |H_polar - H_fd|_mean = {np.mean(np.abs(H_polar - H_fd_sub)):.6e}")

print("\nDiagonal comparison:")
for i in range(min(5, N_test)):
    print(f"  H[{i},{i}]: FD = {H_fd_sub[i,i]:+.6f}, Polar = {H_polar[i,i]:+.6f}, "
          f"err = {abs(H_fd_sub[i,i]-H_polar[i,i]):.2e}")

print("\nOff-diagonal comparison (first 5):")
count = 0
for i in range(N_test):
    for j in range(i+1, N_test):
        if count >= 5:
            break
        print(f"  H[{i},{j}]: FD = {H_fd_sub[i,j]:+.6f}, Polar = {H_polar[i,j]:+.6f}, "
              f"err = {abs(H_fd_sub[i,j]-H_polar[i,j]):.2e}")
        count += 1
    if count >= 5:
        break

print("\nDone.")
