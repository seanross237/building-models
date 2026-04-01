"""
weitzenbock_analysis.py — Analyze R(Q) = M(Q) - M(I) for Yang-Mills

Tasks:
1. Compute R(Q) = (2N/β)(H(Q) - H(I)) for various Q
2. Check ALL eigenvalues: is R(Q) ≼ 0 (NSD) or does it have mixed sign?
3. Analyze the restriction of R(Q) to the top eigenspace of M(I)
4. Single-link excitation worked example
5. Find the cos(ε) suppression structure

Convention: S = -(β/N) sum_P Re Tr(U_P), tau_a = i*sigma_a/2
H(Q) is the Hessian of S at Q.
M(Q) = (2N/β) H(Q)
R(Q) = M(Q) - M(I) = (2N/β)(H(Q) - H(I))
"""

import numpy as np
import json
import time

np.random.seed(42)

# ============================================================
# Parameters
# ============================================================
L = 2    # Small lattice for full diagonalization
d = 4
N_SU = 2
beta = 1.0

n_sites = L**d         # 16
n_links = n_sites * d  # 64
n_gen = 3              # dim su(2)
n_dof = n_links * n_gen  # 192

print(f"L={L}, d={d}, N_SU={N_SU}, beta={beta}")
print(f"n_sites={n_sites}, n_links={n_links}, n_dof={n_dof}")
print(f"4d = {4*d}")

# ============================================================
# Pauli matrices and generators
# ============================================================
sigma = np.zeros((3, 2, 2), dtype=complex)
sigma[0] = [[0, 1], [1, 0]]
sigma[1] = [[0, -1j], [1j, 0]]
sigma[2] = [[1, 0], [0, -1]]

tau = 1j * sigma / 2  # tau_a = i*sigma_a/2, Tr(tau_a tau_b) = -delta_{ab}/2
I2 = np.eye(2, dtype=complex)

# ============================================================
# Lattice geometry
# ============================================================
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

def link_idx(site_idx, mu):
    return site_idx * d + mu

def add_dir(site, mu):
    x = list(site)
    x[mu] = (x[mu] + 1) % L
    return tuple(x)

# Build plaquettes
plaquettes = []
for x_idx in range(n_sites):
    x = idx_to_site(x_idx)
    for mu in range(d):
        for nu in range(mu + 1, d):
            x_mu = add_dir(x, mu)
            x_nu = add_dir(x, nu)
            l0 = link_idx(site_to_idx(x), mu)
            l1 = link_idx(site_to_idx(x_mu), nu)
            l2 = link_idx(site_to_idx(x_nu), mu)
            l3 = link_idx(site_to_idx(x), nu)
            plaquettes.append([(l0, +1), (l1, +1), (l2, -1), (l3, -1)])

n_plaq = len(plaquettes)
print(f"n_plaquettes = {n_plaq}")

# ============================================================
# SU(2) utilities
# ============================================================
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

def config_random():
    return np.array([random_su2() for _ in range(n_links)])

def config_perturbed(epsilon):
    Q = config_identity()
    for l in range(n_links):
        c = epsilon * np.random.randn(3)
        Q[l] = su2_exp(c)
    return Q

def config_single_link(link_idx_val, coeffs):
    """Single-link excitation: one link = exp(coeffs . tau), rest = I."""
    Q = config_identity()
    Q[link_idx_val] = su2_exp(coeffs)
    return Q

def plaq_product(Q, plaq):
    result = I2.copy()
    for (l, s) in plaq:
        if s == +1:
            result = result @ Q[l]
        else:
            result = result @ su2_dagger(Q[l])
    return result

# ============================================================
# Full Hessian computation
# ============================================================
def compute_hessian(Q):
    """
    H[i,j] = d^2 S / d(eps_i) d(eps_j), i = l*3 + a
    Perturbation: Q_l -> Q_l exp(sum_a eps^a tau_a)
    """
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

        # Diagonal
        diag_val = (beta_N / 4.0) * retr_UP
        for k in range(4):
            lk = link_ids[k]
            for a in range(n_gen):
                H[lk * n_gen + a, lk * n_gen + a] += diag_val

        # Off-diagonal
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

# ============================================================
# Compute M(Q) = (2*N_SU/beta) * H(Q)
# ============================================================
def compute_M(Q):
    H = compute_hessian(Q)
    return (2.0 * N_SU / beta) * H

# ============================================================
# SECTION 1: Basic eigenvalue analysis of R(Q) = M(Q) - M(I)
# ============================================================
print("\n" + "="*60)
print("SECTION 1: Eigenvalue analysis of R(Q) = M(Q) - M(I)")
print("="*60)

print("\nComputing M(I)...")
Q_I = config_identity()
H_I = compute_hessian(Q_I)
M_I = (2.0 * N_SU / beta) * H_I

eigenvalues_MI = np.linalg.eigvalsh(M_I)
print(f"M(I) eigenvalues: min={eigenvalues_MI.min():.6f}, max={eigenvalues_MI.max():.6f}")
print(f"Expected lambda_max(M(I)) = 4d = {4*d}")
print(f"Multiplicity of lambda_max: {np.sum(np.abs(eigenvalues_MI - 4*d) < 1e-6)}")

# ============================================================
# Test 5 random configs: full eigenspectrum of R(Q)
# ============================================================
results = []
n_test = 10

print(f"\nTesting {n_test} random configurations...")
for i in range(n_test):
    Q = config_random()
    M_Q = compute_M(Q)
    R_Q = M_Q - M_I

    eigs_RQ = np.linalg.eigvalsh(R_Q)
    eigs_MQ = np.linalg.eigvalsh(M_Q)

    max_eig = eigs_RQ.max()
    min_eig = eigs_RQ.min()
    max_MQ = eigs_MQ.max()
    n_positive = np.sum(eigs_RQ > 1e-8)
    n_negative = np.sum(eigs_RQ < -1e-8)
    n_zero = np.sum(np.abs(eigs_RQ) <= 1e-8)

    results.append({
        'config': f'random_{i}',
        'max_R': float(max_eig),
        'min_R': float(min_eig),
        'max_M': float(max_MQ),
        'n_positive': int(n_positive),
        'n_negative': int(n_negative),
        'n_zero': int(n_zero),
        'M_minus_MI_NSD': bool(max_eig <= 1e-8)
    })

    print(f"  Config {i}: lambda_max(M(Q))={max_MQ:.4f}, "
          f"R(Q): min={min_eig:.4f}, max={max_eig:.4f}, "
          f"pos={n_positive}, neg={n_negative}, zero={n_zero}, "
          f"NSD={max_eig <= 1e-8}")

print("\n")
n_nsd = sum(r['M_minus_MI_NSD'] for r in results)
print(f"M(Q) ≼ M(I) (operator order): {n_nsd}/{n_test} configs")
print(f"λ_max(M(Q)) ≤ 4d: {sum(r['max_M'] <= 4*d + 1e-6 for r in results)}/{n_test} configs")

# ============================================================
# SECTION 2: Top eigenspace restriction
# ============================================================
print("\n" + "="*60)
print("SECTION 2: R(Q) restricted to top eigenspace of M(I)")
print("="*60)

# Find top eigenspace of M(I) (eigenvalue ≈ 4d)
eigs_MI, vecs_MI = np.linalg.eigh(M_I)
top_idx = np.abs(eigs_MI - 4*d) < 1e-6
P_top = vecs_MI[:, top_idx]  # shape: (n_dof, n_top)
n_top = P_top.shape[1]
print(f"\nDimension of top eigenspace (λ = 4d = {4*d}): {n_top}")

print("\nR(Q) restricted to top eigenspace:")
print(f"{'Config':<15} {'max_R_restricted':<20} {'min_R_restricted':<20} {'v^T R v ≤ 0?'}")
for i in range(n_test):
    Q = config_random()
    M_Q = compute_M(Q)
    R_Q = M_Q - M_I

    # Restrict R(Q) to top eigenspace
    R_restricted = P_top.T @ R_Q @ P_top  # shape: (n_top, n_top)
    eigs_Rr = np.linalg.eigvalsh(R_restricted)

    max_Rr = eigs_Rr.max()
    min_Rr = eigs_Rr.min()
    nsd_top = max_Rr <= 1e-8

    print(f"  random_{i:<8}  {max_Rr:>+.6f}            {min_Rr:>+.6f}            {'YES ✓' if nsd_top else 'NO ✗'}")

# ============================================================
# SECTION 3: Single-link excitation worked example
# ============================================================
print("\n" + "="*60)
print("SECTION 3: Single-link excitation Q = exp(ε τ₁) on link 0")
print("="*60)

eps_values = [0.0, 0.1, 0.5, 1.0, np.pi/2, np.pi]

print(f"\n{'ε':>10} {'λ_max(M(Q))':>14} {'max(R(Q))':>12} {'min(R(Q))':>12} {'R ≼ 0?':>8} {'cos(ε)':>8}")
print("-" * 70)

# Single-link excitation: link 0, direction τ₁
for eps in eps_values:
    Q = config_single_link(0, [eps, 0, 0])
    M_Q = compute_M(Q)
    R_Q = M_Q - M_I

    eigs_MQ = np.linalg.eigvalsh(M_Q)
    eigs_RQ = np.linalg.eigvalsh(R_Q)

    lam_max_MQ = eigs_MQ.max()
    max_R = eigs_RQ.max()
    min_R = eigs_RQ.min()
    nsd = max_R <= 1e-8
    cos_e = np.cos(eps)

    print(f"{eps:>10.4f} {lam_max_MQ:>14.6f} {max_R:>12.6f} {min_R:>12.6f} {'YES' if nsd else 'NO ':>8} {cos_e:>8.4f}")

print()

# ============================================================
# SECTION 4: Detailed analysis of single-link excitation at ε=0.5
# ============================================================
print("\n" + "="*60)
print("SECTION 4: Detailed structure at ε=0.5")
print("="*60)

eps = 0.5
Q = config_single_link(0, [eps, 0, 0])
M_Q = compute_M(Q)
R_Q = M_Q - M_I

eigs_RQ = np.linalg.eigvalsh(R_Q)
eigs_MQ, vecs_MQ = np.linalg.eigh(M_Q)

print(f"\nAt ε = {eps:.2f}, link 0 = exp({eps:.2f} τ₁):")
print(f"cos(ε) = {np.cos(eps):.4f}")
print(f"λ_max(M(Q)) = {eigs_MQ[-1]:.6f}  (expected ≤ {4*d})")
print(f"λ_max(M(I)) = {eigs_MI[-1]:.6f} = 4d = {4*d}")
print()
print(f"R(Q) eigenvalue statistics:")
print(f"  max = {eigs_RQ.max():.6f}")
print(f"  min = {eigs_RQ.min():.6f}")
print(f"  n_positive = {np.sum(eigs_RQ > 1e-8)}")
print(f"  n_negative = {np.sum(eigs_RQ < -1e-8)}")
print(f"  n_zero = {np.sum(np.abs(eigs_RQ) <= 1e-8)}")
print()

# Find the maximum eigenvalue of M(Q) and how it compares to M(I)
# The maximum eigenvector of M(Q) — is it close to the staggered mode?
v_max_MQ = vecs_MQ[:, -1]  # top eigenvector of M(Q)
top_M_I_space = P_top  # top eigenspace of M(I)
overlap = np.sum((P_top.T @ v_max_MQ)**2)
print(f"Overlap of M(Q) top eigenvector with M(I) top eigenspace: {overlap:.6f}")

# R(Q) restricted to top eigenspace
R_restricted = P_top.T @ R_Q @ P_top
eigs_Rr = np.linalg.eigvalsh(R_restricted)
print(f"\nR(Q) restricted to M(I) top eigenspace ({n_top}-dim):")
print(f"  max = {eigs_Rr.max():.6f}")
print(f"  min = {eigs_Rr.min():.6f}")
print(f"  all ≤ 0: {eigs_Rr.max() <= 1e-8}")

# ============================================================
# SECTION 5: Is M(Q) ≼ M(I) in operator order?
# ============================================================
print("\n" + "="*60)
print("SECTION 5: Systematic test — M(Q) ≼ M(I) operator order?")
print("="*60)

print("\nTesting 20 configs: full eigenspectrum analysis")
full_results = []
for i in range(20):
    if i < 10:
        Q = config_random()
        label = f'random_{i}'
    elif i < 15:
        eps_val = (i - 9) * 0.3
        Q = config_perturbed(eps_val)
        label = f'perturb_{eps_val:.1f}'
    else:
        Q = config_single_link(i % n_links, [(i-14)*0.5, 0, 0])
        label = f'single_link_{i-14}'

    M_Q = compute_M(Q)
    R_Q = M_Q - M_I
    eigs_RQ = np.linalg.eigvalsh(R_Q)
    max_R = eigs_RQ.max()

    # Restricted to top eigenspace
    R_restricted = P_top.T @ R_Q @ P_top
    eigs_Rr = np.linalg.eigvalsh(R_restricted)
    max_Rr = eigs_Rr.max()

    full_results.append({
        'label': label,
        'max_R': float(max_R),
        'min_R': float(eigs_RQ.min()),
        'NSD_full': bool(max_R <= 1e-8),
        'max_Rr': float(max_Rr),
        'NSD_top': bool(max_Rr <= 1e-8),
    })

print(f"\n{'Config':<20} {'max R(Q)':>12} {'NSD?':>8} {'max R|_top':>12} {'NSD|_top?':>10}")
print("-" * 65)
for r in full_results:
    print(f"{r['label']:<20} {r['max_R']:>12.6f} {('YES' if r['NSD_full'] else 'NO '):>8} "
          f"{r['max_Rr']:>12.6f} {('YES' if r['NSD_top'] else 'NO '):>10}")

n_nsd_full = sum(r['NSD_full'] for r in full_results)
n_nsd_top = sum(r['NSD_top'] for r in full_results)
print(f"\nSummary: M(Q) ≼ M(I) full order: {n_nsd_full}/20")
print(f"Summary: R(Q) ≼ 0 on top eigenspace: {n_nsd_top}/20")

# ============================================================
# SECTION 6: Decompose R(Q) structure
# ============================================================
print("\n" + "="*60)
print("SECTION 6: Decompose M(Q) at Q=I vs Q=exp(ε τ₁)")
print("="*60)

eps = 0.5
Q_sl = config_single_link(0, [eps, 0, 0])

H_I_mat = compute_hessian(Q_I)
H_Q_mat = compute_hessian(Q_sl)
DH = H_Q_mat - H_I_mat  # difference in Hessians

eigs_DH = np.linalg.eigvalsh(DH)
print(f"\nH(Q) - H(I) eigenvalue range at ε={eps}:")
print(f"  max = {eigs_DH.max():.6f}  (×2N/β={2*N_SU/beta:.1f} → max R(Q) = {eigs_DH.max()*2*N_SU/beta:.6f})")
print(f"  min = {eigs_DH.min():.6f}  (×2N/β={2*N_SU/beta:.1f} → min R(Q) = {eigs_DH.min()*2*N_SU/beta:.6f})")
print(f"  n_positive: {np.sum(eigs_DH > 1e-8)}")
print(f"  n_negative: {np.sum(eigs_DH < -1e-8)}")

# Separate diagonal vs off-diagonal contributions
print("\nDiagonal correction contribution (Re Tr(U_P) factor):")
# Diagonal of H(Q) - H(I) comes from changes in Re Tr(U_P)
diag_diff = np.diag(H_Q_mat) - np.diag(H_I_mat)
print(f"  max diagonal change = {diag_diff.max():.6f}")
print(f"  min diagonal change = {diag_diff.min():.6f}")
print(f"  mean diagonal change = {diag_diff.mean():.6f}")

# Plaquettes containing link 0:
link0_plaq_idx = []
for p_idx, plaq in enumerate(plaquettes):
    if any(l == 0 for (l, s) in plaq):
        link0_plaq_idx.append(p_idx)
print(f"\nPlaquettes containing link 0: {len(link0_plaq_idx)} (expected 2(d-1)={2*(d-1)})")

# Re Tr(U_P) for affected plaquettes
print(f"Re Tr(U_P) for affected plaquettes at ε={eps}:")
for p_idx in link0_plaq_idx[:3]:  # show first 3
    U_P = plaq_product(Q_sl, plaquettes[p_idx])
    retrU = np.real(np.trace(U_P))
    print(f"  Plaq {p_idx}: Re Tr(U_P) = {retrU:.4f} (expected ~ cos(ε)={np.cos(eps):.4f} × 2)")

# ============================================================
# SECTION 7: Is F(Q) = λ_max(M(Q)) = 4d iff Q pure gauge?
# ============================================================
print("\n" + "="*60)
print("SECTION 7: F(Q) = λ_max(M(Q)) characterization")
print("="*60)

# Pure gauge: Q_l = g_{x+μ}^{-1} g_x (gauge transform of I)
# For L=2, a gauge transform is: for each site x, choose g_x ∈ SU(2)
# Q_l(x,μ) = g_{x+μ}^{-1} g_x

def config_pure_gauge():
    """Random pure gauge configuration."""
    g = np.array([random_su2() for _ in range(n_sites)])
    Q = np.zeros((n_links, 2, 2), dtype=complex)
    for x_idx in range(n_sites):
        x = idx_to_site(x_idx)
        for mu in range(d):
            x_plus = add_dir(x, mu)
            x_plus_idx = site_to_idx(x_plus)
            lk = link_idx(x_idx, mu)
            Q[lk] = su2_dagger(g[x_plus_idx]) @ g[x_idx]
    return Q

print("\nTesting pure gauge configs: expect λ_max = 4d")
for i in range(5):
    Q_pg = config_pure_gauge()
    eigs_Mpg = np.linalg.eigvalsh(compute_M(Q_pg))
    lmax = eigs_Mpg.max()
    print(f"  Pure gauge {i}: λ_max = {lmax:.6f}  (4d = {4*d})")

print("\nTesting random configs: expect λ_max < 4d")
for i in range(5):
    Q_rand = config_random()
    eigs_Mrand = np.linalg.eigvalsh(compute_M(Q_rand))
    lmax = eigs_Mrand.max()
    print(f"  Random {i}: λ_max = {lmax:.6f}  (< {4*d}? {'YES' if lmax < 4*d else 'NO'})")

print()
print("Done!")
