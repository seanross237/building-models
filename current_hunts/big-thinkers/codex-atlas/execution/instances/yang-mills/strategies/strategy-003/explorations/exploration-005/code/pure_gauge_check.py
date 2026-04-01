"""
pure_gauge_check.py — Fix pure gauge convention and verify λ_max = 4d
Also: measure R(Q)|_P eigenvalues vs plaquette curvature
"""
import numpy as np
np.random.seed(42)

L = 2
d = 4
N_SU = 2
beta = 1.0

n_sites = L**d
n_links = n_sites * d
n_gen = 3
n_dof = n_links * n_gen

sigma = np.zeros((3, 2, 2), dtype=complex)
sigma[0] = [[0, 1], [1, 0]]
sigma[1] = [[0, -1j], [1j, 0]]
sigma[2] = [[1, 0], [0, -1]]
tau = 1j * sigma / 2
I2 = np.eye(2, dtype=complex)

def site_to_idx(x):
    idx = 0
    for i in range(d):
        idx = idx * L + x[i]
    return idx

def idx_to_site(idx):
    x = []
    r = idx
    for i in range(d):
        x.append(r % L)
        r //= L
    return tuple(reversed(x))

def link_idx_fn(site_idx, mu):
    return site_idx * d + mu

def add_dir(site, mu):
    x = list(site)
    x[mu] = (x[mu] + 1) % L
    return tuple(x)

plaquettes = []
for x_idx in range(n_sites):
    x = idx_to_site(x_idx)
    for mu in range(d):
        for nu in range(mu + 1, d):
            x_mu = add_dir(x, mu)
            x_nu = add_dir(x, nu)
            l0 = link_idx_fn(site_to_idx(x), mu)
            l1 = link_idx_fn(site_to_idx(x_mu), nu)
            l2 = link_idx_fn(site_to_idx(x_nu), mu)
            l3 = link_idx_fn(site_to_idx(x), nu)
            plaquettes.append([(l0, +1), (l1, +1), (l2, -1), (l3, -1)])

n_plaq = len(plaquettes)

def random_su2():
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    return q[0] * I2 + 1j * (q[1] * sigma[0] + q[2] * sigma[1] + q[3] * sigma[2])

def su2_dagger(U):
    return U.conj().T

def su2_exp(coeffs):
    A = coeffs[0] * tau[0] + coeffs[1] * tau[1] + coeffs[2] * tau[2]
    c_sq = float(np.real(coeffs[0]**2 + coeffs[1]**2 + coeffs[2]**2))
    if c_sq < 1e-30:
        return I2 + A
    theta = np.sqrt(c_sq)
    return np.cos(theta / 2) * I2 + (np.sin(theta / 2) / (theta / 2)) * A

def config_identity():
    return np.array([I2.copy() for _ in range(n_links)])

def config_pure_gauge_correct():
    """Q_{l(x,μ)} = g_x^{-1} g_{x+μ} = g_x^† g_{x+μ}"""
    g = np.array([random_su2() for _ in range(n_sites)])
    Q = np.zeros((n_links, 2, 2), dtype=complex)
    for x_idx in range(n_sites):
        x = idx_to_site(x_idx)
        for mu in range(d):
            x_plus = add_dir(x, mu)
            x_plus_idx = site_to_idx(x_plus)
            lk = link_idx_fn(x_idx, mu)
            Q[lk] = su2_dagger(g[x_idx]) @ g[x_plus_idx]  # g_x^{-1} g_{x+μ}
    return Q

def plaq_product(Q, plaq):
    result = I2.copy()
    for (l, s) in plaq:
        if s == +1:
            result = result @ Q[l]
        else:
            result = result @ su2_dagger(Q[l])
    return result

def compute_hessian(Q):
    H = np.zeros((n_dof, n_dof))
    beta_N = beta / N_SU
    for plaq in plaquettes:
        W = np.zeros((4, 2, 2), dtype=complex)
        link_ids = np.zeros(4, dtype=int)
        signs = np.zeros(4, dtype=int)
        for k, (l, s) in enumerate(plaq):
            link_ids[k] = l
            signs[k] = s
            W[k] = Q[l] if s == +1 else su2_dagger(Q[l])
        Lpre = np.zeros((5, 2, 2), dtype=complex)
        Lpre[0] = I2
        for k in range(4):
            Lpre[k + 1] = Lpre[k] @ W[k]
        U_P = Lpre[4]
        retr_UP = np.real(np.trace(U_P))
        Rsuf = np.zeros((4, 2, 2), dtype=complex)
        Rsuf[3] = I2
        for k in range(2, -1, -1):
            Rsuf[k] = W[k + 1] @ Rsuf[k + 1]
        diag_val = (beta_N / 4.0) * retr_UP
        for k in range(4):
            lk = link_ids[k]
            for a in range(n_gen):
                H[lk * n_gen + a, lk * n_gen + a] += diag_val
        for k in range(4):
            lk = link_ids[k]
            sk = signs[k]
            for m in range(k + 1, 4):
                lm = link_ids[m]
                sm = signs[m]
                M_km = I2.copy()
                for j in range(k + 1, m):
                    M_km = M_km @ W[j]
                for a in range(n_gen):
                    Ak = (W[k] @ tau[a]) if sk == +1 else (-tau[a] @ W[k])
                    LAM = Lpre[k] @ Ak @ M_km
                    for b in range(n_gen):
                        Am = (W[m] @ tau[b]) if sm == +1 else (-tau[b] @ W[m])
                        product = LAM @ Am @ Rsuf[m]
                        val = np.real(np.trace(product))
                        i_idx = lk * n_gen + a
                        j_idx = lm * n_gen + b
                        H[i_idx, j_idx] += -beta_N * val
                        H[j_idx, i_idx] += -beta_N * val
    return H

def compute_M(Q):
    return (2.0 * N_SU / beta) * compute_hessian(Q)

# ===========================================================
# SECTION 1: Pure gauge with CORRECT convention
# ===========================================================
print("="*60)
print("SECTION 1: Pure gauge (correct convention g_x^{-1} g_{x+μ})")
print("="*60)

Q_I = config_identity()
M_I = compute_M(Q_I)
eigs_MI = np.linalg.eigvalsh(M_I)
print(f"\nM(I) max eigenvalue = {eigs_MI.max():.6f} (expect 4d = {4*d})")

print("\nVerify plaquette products = I for pure gauge:")
for trial in range(3):
    Q_pg = config_pure_gauge_correct()
    max_plaq_dev = 0.0
    for plaq in plaquettes:
        U_P = plaq_product(Q_pg, plaq)
        dev = np.max(np.abs(U_P - I2))
        max_plaq_dev = max(max_plaq_dev, dev)
    print(f"  Trial {trial}: max |U_P - I| = {max_plaq_dev:.2e}")

print("\nλ_max(M(Q)) for pure gauge configs:")
for trial in range(5):
    Q_pg = config_pure_gauge_correct()
    eigs_Mpg = np.linalg.eigvalsh(compute_M(Q_pg))
    print(f"  Pure gauge {trial}: λ_max = {eigs_Mpg.max():.6f} (expect 4d={4*d})")

# ===========================================================
# SECTION 2: R(Q)|_P eigenvalues vs plaquette curvature
# ===========================================================
print("\n" + "="*60)
print("SECTION 2: R(Q)|_P eigenvalues vs plaquette curvature sum")
print("="*60)

eigs_MI, vecs_MI = np.linalg.eigh(M_I)
top_idx = np.abs(eigs_MI - 4*d) < 1e-6
P_top = vecs_MI[:, top_idx]
n_top = P_top.shape[1]
print(f"\nTop eigenspace dim = {n_top}")

def plaquette_curvature_sum(Q):
    """∑_□ |F_□|² where F_□ = Im log(U_□) (plaquette field strength)"""
    total = 0.0
    for plaq in plaquettes:
        U_P = plaq_product(Q, plaq)
        # For SU(2): U = exp(iθ n·σ), Re Tr(U) = 2 cos(θ)
        # |F_□|² ≈ θ² ≈ (Re Tr(U) - 2)² / ... but simpler:
        # Use |U_P - I|_F² as proxy for field strength
        F_plaq = U_P - I2
        total += np.real(np.trace(F_plaq @ F_plaq.conj().T))
    return total

def plaquette_curvature_angle(Q):
    """∑_□ (1 - cos(θ_□)) where θ_□ from Re Tr(U_□) = 2 cos(θ/2)"""
    total = 0.0
    for plaq in plaquettes:
        U_P = plaq_product(Q, plaq)
        cos_half = np.real(np.trace(U_P)) / 2.0  # = cos(θ/2)
        cos_half = np.clip(cos_half, -1, 1)
        total += (1.0 - cos_half)
    return total

print(f"\n{'Config':<18} {'max R|_P':>10} {'min R|_P':>10} {'|F|^2':>10} {'Σ(1-cosθ)':>12}")
print("-"*65)

# Single-link excitation at various ε
for eps_val in [0.0, 0.1, 0.3, 0.5, 1.0, 2.0, np.pi]:
    Q = config_identity()
    Q[0] = su2_exp([eps_val, 0, 0])
    M_Q = compute_M(Q)
    R_Q = M_Q - M_I
    R_restricted = P_top.T @ R_Q @ P_top
    eigs_Rr = np.linalg.eigvalsh(R_restricted)
    F2 = plaquette_curvature_sum(Q)
    F_angle = plaquette_curvature_angle(Q)
    print(f"  link0 ε={eps_val:.3f}   {eigs_Rr.max():>10.5f} {eigs_Rr.min():>10.5f} "
          f"{F2:>10.4f} {F_angle:>12.4f}")

print()
# Random configs
for i in range(5):
    Q = np.array([random_su2() for _ in range(n_links)])
    M_Q = compute_M(Q)
    R_Q = M_Q - M_I
    R_restricted = P_top.T @ R_Q @ P_top
    eigs_Rr = np.linalg.eigvalsh(R_restricted)
    F2 = plaquette_curvature_sum(Q)
    F_angle = plaquette_curvature_angle(Q)
    print(f"  random_{i:<8}    {eigs_Rr.max():>10.5f} {eigs_Rr.min():>10.5f} "
          f"{F2:>10.4f} {F_angle:>12.4f}")

# ===========================================================
# SECTION 3: Cos(ε/2) vs cos(ε) — which suppression factor?
# ===========================================================
print("\n" + "="*60)
print("SECTION 3: Cos(ε/2) vs cos(ε) for single-link plaquettes")
print("="*60)
print(f"\n{'ε':>8} {'Re Tr(U_P)':>12} {'2cos(ε/2)':>12} {'2cos(ε)':>10}")
print("-"*45)
for eps_val in [0.0, 0.1, 0.5, 1.0, np.pi/2, np.pi]:
    Q = config_identity()
    Q[0] = su2_exp([eps_val, 0, 0])
    # Plaquettes containing link 0 (6 of them, all same by symmetry)
    link0_plaq = [p for p in plaquettes if any(l == 0 for (l, s) in p)]
    U_P = plaq_product(Q, link0_plaq[0])
    retr = np.real(np.trace(U_P))
    print(f"{eps_val:>8.4f} {retr:>12.6f} {2*np.cos(eps_val/2):>12.6f} {2*np.cos(eps_val):>10.6f}")

# ===========================================================
# SECTION 4: Correlation between max R|_P and plaquette angle
# ===========================================================
print("\n" + "="*60)
print("SECTION 4: Linear fit — max R(Q)|_P vs Σ(1-cosθ_□)")
print("="*60)

xs = []  # Σ(1-cosθ)
ys = []  # max R(Q)|_P

for i in range(30):
    eps_val = i * 0.15
    Q = config_identity()
    Q[0] = su2_exp([eps_val, 0, 0])
    M_Q = compute_M(Q)
    R_Q = M_Q - M_I
    R_restricted = P_top.T @ R_Q @ P_top
    eigs_Rr = np.linalg.eigvalsh(R_restricted)
    F_angle = plaquette_curvature_angle(Q)
    xs.append(F_angle)
    ys.append(eigs_Rr.max())

xs = np.array(xs)
ys = np.array(ys)

# Linear regression y = a*x + b
A_mat = np.vstack([xs, np.ones(len(xs))]).T
coeffs, residuals, rank, sv = np.linalg.lstsq(A_mat, ys, rcond=None)
a, b = coeffs
print(f"\nLinear fit: max R(Q)|_P = {a:.4f} × Σ(1-cosθ_□) + {b:.4f}")
print(f"Residuals: max = {np.max(np.abs(ys - (a*xs + b))):.4f}")
print(f"R² = {1 - np.sum((ys - (a*xs+b))**2)/np.sum((ys - ys.mean())**2):.6f}")

print(f"\nConclusion: max R(Q)|_P ≈ {a:.2f} × Σ(1-cosθ_□)")
print(f"Since 1-cosθ ≥ 0, we get max R(Q)|_P ≤ {b:.4f} (should be ≈ 0)")

print("\nDone!")
