"""
Step 3: Full 192×192 Hessian comparison — clean version.

Strategy: Build H_analytical from the one-parameter formula using
the bilinear form identity:

H_{ij} = (f(eᵢ+eⱼ) - f(eᵢ-eⱼ)) / 4

where f(v) = v^T H v is the analytical one-parameter formula.

Then compare eigenvalues of H_analytical, H_formula, and H_FD.
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

# ============================================================
# Analytical formula for d²S/dt² along direction v
# ============================================================

def analytical_quadratic_form(v_vec):
    """
    Compute v^T H_actual v = d²S/dt²|_{t=0} analytically.

    f□ = -(β/2) Re Tr(U□(t))

    U□(t) = ∏ exp(t sₖ Ad_{Pₖ}(v_{eₖ})) U□

    d²Re Tr(U□)/dt² = Σₖ Re Tr(wₖ² U) + 2Σ_{k<l} Re Tr(wₖ wₗ U)
    """
    result = 0.0
    for (e1, e2, e3, e4) in plaquettes:
        U = Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T
        P2 = Q[e1].copy()
        P3 = Q[e1] @ Q[e2] @ Q[e3].conj().T

        edges = [e1, e2, e3, e4]
        signs = [1, 1, -1, -1]
        Ad_ops = [I2, P2, P3, U]

        # Compute wₖ = sₖ Ad_{Pₖ}(v_{eₖ}) for each edge
        ws = []
        for k in range(4):
            v_e = su2_from_vec(v_vec[3*edges[k]:3*edges[k]+3])
            wk = signs[k] * Ad(Ad_ops[k], v_e)
            ws.append(wk)

        # Second derivative: Σₖ Re Tr(wₖ² U) + 2 Σ_{k<l} Re Tr(wₖ wₗ U)
        d2 = 0.0
        for k in range(4):
            d2 += re_tr(ws[k] @ ws[k] @ U)
        for k in range(4):
            for l in range(k+1, 4):
                d2 += 2 * re_tr(ws[k] @ ws[l] @ U)

        result += -(beta / 2) * d2

    return result

def formula_quadratic_form(v_vec):
    """H_formula(v,v) = (β/4) Σ□ |w□|²"""
    result = 0.0
    for (e1, e2, e3, e4) in plaquettes:
        U = Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T
        P2 = Q[e1].copy()
        P3 = Q[e1] @ Q[e2] @ Q[e3].conj().T

        edges = [e1, e2, e3, e4]
        signs = [1, 1, -1, -1]
        Ad_ops = [I2, P2, P3, U]

        w = np.zeros((2, 2), dtype=complex)
        for k in range(4):
            v_e = su2_from_vec(v_vec[3*edges[k]:3*edges[k]+3])
            w += signs[k] * Ad(Ad_ops[k], v_e)

        w_norm_sq = -2.0 * np.trace(w @ w).real
        result += (beta / 4) * w_norm_sq

    return result

# ============================================================
# Build analytical Hessian via per-plaquette bilinear form
# ============================================================

def build_hessian_analytical_v2():
    """
    Build H_actual from the product-of-exponentials expansion.

    For each plaquette with edges at positions k=0,1,2,3:

    The second-order expansion of Re Tr(∏ exp(εₖ) U):
    Σₖ (1/2) Re Tr(εₖ² U) + Σ_{k<l} Re Tr(εₖ εₗ U)

    where εₖ = Σₐ v_{eₖ,a} wₖₐ.

    The Hessian contributions are:
    Same position (k=l): ∂²/∂v_{eₖ,a}∂v_{eₖ,b} = (1/2)(Re Tr(wₖₐwₖᵦU) + Re Tr(wₖᵦwₖₐU))
    Different positions (k<l): ∂²/∂v_{eₖ,a}∂v_{eₗ,b} = Re Tr(wₖₐwₗᵦU)
    """
    H = np.zeros((Ndof, Ndof))

    for (e1, e2, e3, e4) in plaquettes:
        U = Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T
        P2 = Q[e1].copy()
        P3 = Q[e1] @ Q[e2] @ Q[e3].conj().T

        edges = [e1, e2, e3, e4]
        signs = [1, 1, -1, -1]
        Ad_ops = [I2, P2, P3, U]

        # Compute all wₖₐ
        wka = np.zeros((4, 3, 2, 2), dtype=complex)
        for k in range(4):
            for a in range(3):
                wka[k, a] = signs[k] * Ad(Ad_ops[k], T_gen[a])

        # Build contributions
        for k in range(4):
            for a in range(3):
                i = 3 * edges[k] + a
                for l in range(4):
                    for b in range(3):
                        j = 3 * edges[l] + b

                        if k == l:
                            # Same exponential: symmetric in a,b
                            val = 0.5 * (re_tr(wka[k,a] @ wka[k,b] @ U) +
                                         re_tr(wka[k,b] @ wka[k,a] @ U))
                        elif k < l:
                            # Earlier × Later
                            val = re_tr(wka[k,a] @ wka[l,b] @ U)
                        else:
                            # k > l: this entry is H[3*eₖ+a, 3*eₗ+b]
                            # = ∂²f/∂v_{eₖ,a} ∂v_{eₗ,b}
                            # From the (l,k) term (l<k):
                            # ∂²/∂v_{eₖ,a} ∂v_{eₗ,b} [Σ v_{eₗ,a'} v_{eₖ,b'} Tr(wₗₐ' wₖᵦ' U)]
                            # = Re Tr(wₗᵦ wₖₐ U)
                            val = re_tr(wka[l,b] @ wka[k,a] @ U)

                        H[i, j] += -(beta / 2) * val

    return H

# ============================================================
# Build B² formula Hessian
# ============================================================

def build_hessian_formula():
    H = np.zeros((Ndof, Ndof))
    for (e1, e2, e3, e4) in plaquettes:
        U = Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T
        P2 = Q[e1].copy()
        P3 = Q[e1] @ Q[e2] @ Q[e3].conj().T

        edges = [e1, e2, e3, e4]
        signs = [1, 1, -1, -1]
        Ad_ops = [I2, P2, P3, U]

        B_cols = np.zeros((3, 12))
        for k in range(4):
            for c in range(3):
                w = signs[k] * Ad(Ad_ops[k], T_gen[c])
                B_cols[:, 3*k + c] = su2_to_vec(w)

        block = (beta / 4) * B_cols.T @ B_cols

        for i_loc in range(12):
            k_i, a_i = divmod(i_loc, 3)
            i_glob = 3 * edges[k_i] + a_i
            for j_loc in range(12):
                k_j, a_j = divmod(j_loc, 3)
                j_glob = 3 * edges[k_j] + a_j
                H[i_glob, j_glob] += block[i_loc, j_loc]

    return H

# ============================================================
# Build FD Hessian
# ============================================================

def wilson_action():
    S = 0.0
    for (e1, e2, e3, e4) in plaquettes:
        U = Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T
        S -= (beta / 2) * re_tr(U)
    return S

def build_hessian_fd(h=1e-4):
    H = np.zeros((Ndof, Ndof))
    S0 = wilson_action()

    for i in range(Ndof):
        li, ci = divmod(i, 3)
        old = Q[li].copy()
        Q[li] = expm(h * T_gen[ci]) @ old
        Sp = wilson_action()
        Q[li] = old.copy()
        Q[li] = expm(-h * T_gen[ci]) @ old
        Sm = wilson_action()
        Q[li] = old
        H[i, i] = (Sp - 2 * S0 + Sm) / h**2

    for i in range(Ndof):
        li, ci = divmod(i, 3)
        for j in range(i+1, Ndof):
            lj, cj = divmod(j, 3)

            # Check if links share any plaquette
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

            H[i, j] = (Spp - Spm - Smp + Smm) / (4 * h**2)
            H[j, i] = H[i, j]

    return H

# ============================================================
# Run
# ============================================================

print(f"Lattice: L={L}, d={d}, DOF={Ndof}, Plaquettes={len(plaquettes)}")

print("\nBuilding H_FD...")
H_fd = build_hessian_fd()
print(f"  |H_fd - H_fd^T| = {np.max(np.abs(H_fd - H_fd.T)):.2e}")

print("\nBuilding H_analytical (v2)...")
H_ana = build_hessian_analytical_v2()
print(f"  |H_ana - H_ana^T| = {np.max(np.abs(H_ana - H_ana.T)):.2e}")

# Symmetrize
H_ana_sym = (H_ana + H_ana.T) / 2

print("\nBuilding H_formula...")
H_form = build_hessian_formula()

# First check: does the quadratic form match for random directions?
print("\n" + "=" * 70)
print("QUADRATIC FORM VERIFICATION (v^T H v)")
print("=" * 70)
for trial in range(5):
    v = np.random.randn(Ndof)
    v /= np.linalg.norm(v)

    qf_fd = v @ H_fd @ v
    qf_ana = analytical_quadratic_form(v)
    qf_mat = v @ H_ana_sym @ v
    qf_form = v @ H_form @ v
    qf_form2 = formula_quadratic_form(v)

    print(f"\n  Trial {trial+1}:")
    print(f"    v^T H_fd v      = {qf_fd:+.8f}")
    print(f"    analytical_qf   = {qf_ana:+.8f}")
    print(f"    v^T H_ana_sym v = {qf_mat:+.8f}")
    print(f"    v^T H_form v    = {qf_form:+.8f}")
    print(f"    formula_qf      = {qf_form2:+.8f}")
    print(f"    |FD - ana_qf|   = {abs(qf_fd - qf_ana):.2e}")
    print(f"    |FD - mat|      = {abs(qf_fd - qf_mat):.2e}")

# Element-wise comparison
print("\n" + "=" * 70)
print("ELEMENT-WISE COMPARISON")
print("=" * 70)

diff_raw = np.max(np.abs(H_fd - H_ana))
diff_sym = np.max(np.abs(H_fd - H_ana_sym))
print(f"  |H_fd - H_ana (raw)|     = {diff_raw:.6e}")
print(f"  |H_fd - H_ana_sym|       = {diff_sym:.6e}")
print(f"  |H_fd - H_form|          = {np.max(np.abs(H_fd - H_form)):.6e}")
print(f"  |H_ana_sym - H_form|     = {np.max(np.abs(H_ana_sym - H_form)):.6e}")

# Check: is H_ana already symmetric?
asym = H_ana - H_ana.T
print(f"\n  H_ana asymmetry: max = {np.max(np.abs(asym)):.6e}")
if np.max(np.abs(asym)) > 1e-10:
    # Find worst asymmetric entry
    idx = np.unravel_index(np.argmax(np.abs(asym)), asym.shape)
    i, j = idx
    print(f"  Worst asymmetry at ({i},{j}): H[i,j]={H_ana[i,j]:.8f}, H[j,i]={H_ana[j,i]:.8f}")
    print(f"  Difference: {H_ana[i,j]-H_ana[j,i]:.8e}")

    # What links are these?
    li, ci = divmod(i, 3)
    lj, cj = divmod(j, 3)
    print(f"  Link {li} comp {ci}, Link {lj} comp {cj}")

    # Find plaquettes containing both links
    for pidx, (e1, e2, e3, e4) in enumerate(plaquettes):
        es = [e1, e2, e3, e4]
        if li in es and lj in es:
            ki = es.index(li)
            kj = es.index(lj)
            print(f"  Plaquette {pidx}: edges={es}, link {li} at pos {ki}, link {lj} at pos {kj}")

# Eigenvalues
print("\n" + "=" * 70)
print("EIGENVALUE COMPARISON")
print("=" * 70)

eig_fd = np.sort(np.linalg.eigvalsh(H_fd))[::-1]
eig_ana = np.sort(np.linalg.eigvalsh(H_ana_sym))[::-1]
eig_form = np.sort(np.linalg.eigvalsh(H_form))[::-1]

print(f"\n  {'i':>4s} {'FD':>12s} {'Analytical':>12s} {'Formula':>12s}")
for i in range(10):
    print(f"  {i:4d} {eig_fd[i]:12.6f} {eig_ana[i]:12.6f} {eig_form[i]:12.6f}")

print(f"\n  λ_max ratio (FD/formula): {eig_fd[0]/eig_form[0]:.6f}")
print(f"  λ_max(FD) ≤ λ_max(formula)? {eig_fd[0] <= eig_form[0] + 1e-6}")

# Check ALL eigenvalue inequalities
violations = np.sum(eig_fd > eig_form + 1e-6)
print(f"\n  Eigenvalue-by-eigenvalue: {violations} violations out of {Ndof}")
# Note: the inequality λ_max(H_actual) ≤ λ_max(H_formula) is what we need,
# not eigenvalue-by-eigenvalue (which is stronger and may not hold).

print("\nDone.")
