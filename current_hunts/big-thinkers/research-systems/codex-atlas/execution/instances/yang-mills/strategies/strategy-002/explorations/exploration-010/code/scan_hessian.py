"""
scan_hessian.py — Full Hessian eigenvalue scan for SU(2) Wilson gauge theory
L=2, d=4, beta=1.0. Tests H_norm <= 1/12 conjecture for 100+ configurations.

Analytical Hessian computation for general Q in SU(2)^64.
Convention: S = -beta * sum_P Re Tr(U_P), generators tau_a = i*sigma_a/2

Author: Math Explorer (E010)
"""

import numpy as np
import json
import time
import sys

# ============================================================
# Constants
# ============================================================
L = 2
d = 4
N_SU = 2  # SU(2)
beta = 1.0

n_sites = L**d        # 16
n_links = n_sites * d  # 64
n_gen = 3              # dim su(2)
n_dof = n_links * n_gen  # 192

# Threshold values
HNORM_CONJ = 1.0 / 12  # 0.08333...
HNORM_TRIANG = 1.0 / 8  # 0.125
LAMBDA_CONJ = 4.0 * beta  # 4.0
LAMBDA_TRIANG = 6.0 * beta  # 6.0

# ============================================================
# Pauli matrices and generators
# ============================================================
sigma = np.zeros((3, 2, 2), dtype=complex)
sigma[0] = [[0, 1], [1, 0]]
sigma[1] = [[0, -1j], [1j, 0]]
sigma[2] = [[1, 0], [0, -1]]

tau = 1j * sigma / 2  # su(2) generators: tau_a = i*sigma_a/2
# Properties: Tr(tau_a tau_b) = -delta_{ab}/2
#             {tau_a, tau_b} = -delta_{ab} I / 2

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

# Build plaquettes: each = [(l0,s0), (l1,s1), (l2,s2), (l3,s3)]
# Order: (x,mu) -> (x+mu,nu) -> (x+nu,mu)^{-1} -> (x,nu)^{-1}
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
assert n_plaq == 96, f"Expected 96 plaquettes, got {n_plaq}"

# Precompute: for each link, which plaquettes contain it (and at which position)
link_to_plaqs = [[] for _ in range(n_links)]
for p_idx, plaq in enumerate(plaquettes):
    for pos, (l, s) in enumerate(plaq):
        link_to_plaqs[l].append((p_idx, pos))

# Verify: each link in 6 plaquettes
for l in range(n_links):
    assert len(link_to_plaqs[l]) == 2 * (d - 1), \
        f"Link {l} in {len(link_to_plaqs[l])} plaquettes, expected {2*(d-1)}"

# ============================================================
# SU(2) utilities
# ============================================================
def random_su2():
    """Random SU(2) element from Haar measure (unit quaternion)."""
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    return q[0] * I2 + 1j * (q[1] * sigma[0] + q[2] * sigma[1] + q[3] * sigma[2])

def su2_dagger(U):
    """Hermitian conjugate = inverse for SU(2)."""
    return U.conj().T

def su2_exp(coeffs):
    """Exponential map: coeffs = (c1,c2,c3) -> exp(sum c_a tau_a)."""
    A = coeffs[0] * tau[0] + coeffs[1] * tau[1] + coeffs[2] * tau[2]
    # A is anti-Hermitian 2x2. Eigenvalues +-i*theta/2.
    # theta^2 = -2*Tr(A^2) = sum c_a^2 / 2 ... wait
    # Tr(A^2) = sum c_a c_b Tr(tau_a tau_b) = -sum c_a^2 / 2
    # theta = sqrt(-2 Tr(A^2)) = sqrt(sum c_a^2)
    # No wait: A = sum c_a tau_a, Tr(A^2) = sum c_a^2 Tr(tau_a^2) = -sum c_a^2 / 2
    # theta/2 eigenvalue: theta = sqrt(sum c_a^2)... let me just use:
    c_sq = coeffs[0]**2 + coeffs[1]**2 + coeffs[2]**2
    if c_sq < 1e-30:
        return I2 + A
    theta = np.sqrt(c_sq)
    return np.cos(theta / 2) * I2 + (np.sin(theta / 2) / (theta / 2)) * A

# ============================================================
# Configuration generators
# ============================================================
def config_identity():
    """Q = I (trivial vacuum)."""
    Q = np.zeros((n_links, 2, 2), dtype=complex)
    for l in range(n_links):
        Q[l] = I2.copy()
    return Q

def config_random():
    """Random Q from Haar measure on each link."""
    Q = np.zeros((n_links, 2, 2), dtype=complex)
    for l in range(n_links):
        Q[l] = random_su2()
    return Q

def config_perturbed_identity(epsilon):
    """Q_l = exp(epsilon * random su(2))."""
    Q = np.zeros((n_links, 2, 2), dtype=complex)
    for l in range(n_links):
        c = np.random.randn(3)
        c /= np.linalg.norm(c)  # unit direction
        Q[l] = su2_exp(epsilon * c)
    return Q

def config_metropolis(beta_gibbs, n_sweeps=200, n_thermalize=100):
    """Generate equilibrium config via Metropolis at given beta."""
    Q = config_identity()
    delta = 0.5  # proposal width

    for sweep in range(n_thermalize + n_sweeps):
        for l in range(n_links):
            # Propose: Q_l -> Q_l * R where R is near-identity SU(2)
            c = delta * np.random.randn(3)
            R = su2_exp(c)
            Q_new = Q[l] @ R

            # Compute change in action for plaquettes containing link l
            dS = 0.0
            for (p_idx, pos) in link_to_plaqs[l]:
                plaq = plaquettes[p_idx]
                # Old plaquette product
                U_old = plaq_product(Q, plaq)
                # New plaquette product (with Q_new at link l)
                Q_save = Q[l].copy()
                Q[l] = Q_new
                U_new = plaq_product(Q, plaq)
                Q[l] = Q_save
                dS += -(beta_gibbs / N_SU) * (np.real(np.trace(U_new)) - np.real(np.trace(U_old)))

            # Accept/reject
            if dS < 0 or np.random.rand() < np.exp(-dS):
                Q[l] = Q_new

    return Q

def plaq_product(Q, plaq):
    """Compute the plaquette product U_P = W_0 W_1 W_2 W_3."""
    result = I2.copy()
    for (l, s) in plaq:
        if s == +1:
            result = result @ Q[l]
        else:
            result = result @ su2_dagger(Q[l])
    return result

# ============================================================
# Wilson action
# ============================================================
def compute_action(Q):
    """S = -(beta/N) * sum_P Re Tr(U_P).  SZZ convention."""
    S = 0.0
    beta_N = beta / N_SU
    for plaq in plaquettes:
        U_P = plaq_product(Q, plaq)
        S += -beta_N * np.real(np.trace(U_P))
    return S

# ============================================================
# Analytical Hessian for general Q
# ============================================================
def compute_hessian(Q):
    """
    Compute the 192x192 Hessian of S = -(beta/N) sum_P Re Tr(U_P).
    SZZ convention with N=N_SU=2 for SU(2).

    Perturbation: Q_l -> Q_l exp(sum_a eps^a tau_a)
    H[i,j] = d^2 S / d(eps_i) d(eps_j) where i = l*3 + a

    For each plaquette P with W_k (k=0..3):
      Same-link: (beta/(4N)) delta_{ab} Re Tr(U_P)   [SU(2) specific]
      Cross-link (k<m): -(beta/N) Re Tr(L_k A_k^a M_{k,m} A_m^b R_m)
    """
    H = np.zeros((n_dof, n_dof))

    for plaq in plaquettes:
        # Build W matrices
        W = np.zeros((4, 2, 2), dtype=complex)
        link_ids = np.zeros(4, dtype=int)
        signs = np.zeros(4, dtype=int)
        for k, (l, s) in enumerate(plaq):
            link_ids[k] = l
            signs[k] = s
            if s == +1:
                W[k] = Q[l]
            else:
                W[k] = su2_dagger(Q[l])

        # Prefix products: L[k] = W[0] @ ... @ W[k-1]
        Lpre = np.zeros((5, 2, 2), dtype=complex)
        Lpre[0] = I2
        for k in range(4):
            Lpre[k + 1] = Lpre[k] @ W[k]
        U_P = Lpre[4]
        retr_UP = np.real(np.trace(U_P))

        # Suffix products: Rsuf[k] = W[k+1] @ ... @ W[3]
        Rsuf = np.zeros((4, 2, 2), dtype=complex)
        Rsuf[3] = I2
        for k in range(2, -1, -1):
            Rsuf[k] = W[k + 1] @ Rsuf[k + 1]

        # Diagonal contribution: (beta/(4N)) delta_{ab} Re Tr(U_P)
        beta_N = beta / N_SU  # SZZ convention: S = -(beta/N) Re Tr
        diag_val = (beta_N / 4.0) * retr_UP
        for k in range(4):
            lk = link_ids[k]
            for a in range(n_gen):
                idx = lk * n_gen + a
                H[idx, idx] += diag_val

        # Off-diagonal: k < m
        for k in range(4):
            lk = link_ids[k]
            sk = signs[k]

            for m in range(k + 1, 4):
                lm = link_ids[m]
                sm = signs[m]

                # Middle product M_{k,m} = W[k+1] @ ... @ W[m-1]
                M_km = I2.copy()
                for j in range(k + 1, m):
                    M_km = M_km @ W[j]

                for a in range(n_gen):
                    # A_k^{(a)} depends on sign
                    if sk == +1:
                        Ak = W[k] @ tau[a]
                    else:
                        Ak = -tau[a] @ W[k]

                    # Precompute L[k] @ Ak @ M_km
                    LAM = Lpre[k] @ Ak @ M_km

                    for b in range(n_gen):
                        if sm == +1:
                            Am = W[m] @ tau[b]
                        else:
                            Am = -tau[b] @ W[m]

                        product = LAM @ Am @ Rsuf[m]
                        val = np.real(np.trace(product))

                        i_idx = lk * n_gen + a
                        j_idx = lm * n_gen + b
                        H[i_idx, j_idx] += -beta_N * val
                        H[j_idx, i_idx] += -beta_N * val

    return H

# ============================================================
# Finite-difference Hessian (for verification)
# ============================================================
def compute_hessian_fd(Q, eps=1e-4):
    """Compute Hessian by central finite differences."""
    H_fd = np.zeros((n_dof, n_dof))
    S0 = compute_action(Q)

    for i in range(n_dof):
        li = i // n_gen
        ai = i % n_gen

        # Perturb +eps in direction i
        Q_plus = Q.copy()
        c_plus = np.zeros(3)
        c_plus[ai] = eps
        Q_plus[li] = Q[li] @ su2_exp(c_plus)
        S_plus = compute_action(Q_plus)

        # Perturb -eps in direction i
        Q_minus = Q.copy()
        c_minus = np.zeros(3)
        c_minus[ai] = -eps
        Q_minus[li] = Q[li] @ su2_exp(c_minus)
        S_minus = compute_action(Q_minus)

        # Diagonal
        H_fd[i, i] = (S_plus - 2 * S0 + S_minus) / eps**2

        # Off-diagonal: use 4-point formula
        for j in range(i + 1, n_dof):
            lj = j // n_gen
            aj = j % n_gen

            # (i+, j+)
            Qpp = Q.copy()
            cp = np.zeros(3); cp[ai] = eps
            Qpp[li] = Q[li] @ su2_exp(cp)
            cp2 = np.zeros(3); cp2[aj] = eps
            Qpp[lj] = Q[lj] @ su2_exp(cp2)
            Spp = compute_action(Qpp)

            # (i+, j-)
            Qpm = Q.copy()
            cp = np.zeros(3); cp[ai] = eps
            Qpm[li] = Q[li] @ su2_exp(cp)
            cm = np.zeros(3); cm[aj] = -eps
            Qpm[lj] = Q[lj] @ su2_exp(cm)
            Spm = compute_action(Qpm)

            # (i-, j+)
            Qmp = Q.copy()
            cm = np.zeros(3); cm[ai] = -eps
            Qmp[li] = Q[li] @ su2_exp(cm)
            cp = np.zeros(3); cp[aj] = eps
            Qmp[lj] = Q[lj] @ su2_exp(cp)
            Smp = compute_action(Qmp)

            # (i-, j-)
            Qmm = Q.copy()
            cm = np.zeros(3); cm[ai] = -eps
            Qmm[li] = Q[li] @ su2_exp(cm)
            cm2 = np.zeros(3); cm2[aj] = -eps
            Qmm[lj] = Q[lj] @ su2_exp(cm2)
            Smm = compute_action(Qmm)

            H_fd[i, j] = (Spp - Spm - Smp + Smm) / (4 * eps**2)
            H_fd[j, i] = H_fd[i, j]

    return H_fd

# ============================================================
# Analyze a single configuration
# ============================================================
def analyze_config(Q, label=""):
    """Compute Hessian, eigenvalues, H_norm for config Q."""
    H = compute_hessian(Q)

    # Check symmetry
    sym_err = np.max(np.abs(H - H.T))

    # Eigenvalues
    eigvals = np.linalg.eigvalsh(H)
    lambda_max = eigvals[-1]
    lambda_min = eigvals[0]
    h_norm = lambda_max / (48 * beta)

    return {
        "label": label,
        "lambda_max": float(lambda_max),
        "lambda_min": float(lambda_min),
        "h_norm": float(h_norm),
        "sym_err": float(sym_err),
        "exceeds_1_12": bool(h_norm > HNORM_CONJ + 1e-10),
        "exceeds_1_8": bool(h_norm > HNORM_TRIANG + 1e-10),
    }

# ============================================================
# MAIN
# ============================================================
def main():
    results = []
    all_hnorms = []

    print("=" * 70)
    print("Exploration 010: H_norm scan for SU(2) Wilson gauge theory")
    print(f"L={L}, d={d}, beta={beta}, n_dof={n_dof}, n_plaq={n_plaq}")
    print(f"Conjecture threshold: H_norm <= 1/12 = {HNORM_CONJ:.6f}")
    print(f"Triangle bound:       H_norm <= 1/8  = {HNORM_TRIANG:.6f}")
    print("=" * 70)

    # ---- Step 0: Verify at Q=I ----
    print("\n--- Verification at Q=I ---")
    t0 = time.time()
    Q_id = config_identity()
    r = analyze_config(Q_id, "Q=I")
    t1 = time.time()
    print(f"  lambda_max = {r['lambda_max']:.6f} (expected 4.0)")
    print(f"  H_norm     = {r['h_norm']:.6f} (expected 1/12 = {1/12:.6f})")
    print(f"  sym_err    = {r['sym_err']:.2e}")
    print(f"  Time: {t1-t0:.3f}s")
    assert abs(r['lambda_max'] - 4.0) < 1e-8, f"Q=I check failed: lambda_max={r['lambda_max']}"
    print("  Q=I verification PASSED")

    # ---- Step 0b: Finite-difference verification on small random Q ----
    print("\n--- Finite-difference verification ---")
    np.random.seed(42)
    Q_test = config_random()
    t0 = time.time()
    H_anal = compute_hessian(Q_test)
    t1 = time.time()
    print(f"  Analytical Hessian: {t1-t0:.3f}s")

    # FD on a small subset of entries (full FD is too slow for 192x192)
    # For same-link different-generator pairs, must combine perturbations correctly
    print("  Running finite-difference check on subset of entries...")
    eps_fd = 1e-4
    S0 = compute_action(Q_test)
    max_err = 0.0
    n_checked = 0

    # Check 30 random entries, handling same-link case correctly
    np.random.seed(999)
    check_pairs = []
    for _ in range(40):
        i = np.random.randint(n_dof)
        j = np.random.randint(i, n_dof)
        check_pairs.append((i, j))

    for (i, j) in check_pairs:
        li, ai = i // n_gen, i % n_gen
        lj, aj = j // n_gen, j % n_gen

        if i == j:
            # Diagonal: 3-point formula
            c = np.zeros(3); c[ai] = eps_fd
            Q_p = Q_test.copy(); Q_p[li] = Q_test[li] @ su2_exp(c)
            c = np.zeros(3); c[ai] = -eps_fd
            Q_m = Q_test.copy(); Q_m[li] = Q_test[li] @ su2_exp(c)
            h_fd = (compute_action(Q_p) - 2*S0 + compute_action(Q_m)) / eps_fd**2
        elif li == lj:
            # Same link, different generators: combined perturbation
            # Q_l -> Q_l exp(eps^a tau_a + eps^b tau_b)
            c_pp = np.zeros(3); c_pp[ai] = eps_fd; c_pp[aj] += eps_fd
            c_pm = np.zeros(3); c_pm[ai] = eps_fd; c_pm[aj] -= eps_fd
            c_mp = np.zeros(3); c_mp[ai] = -eps_fd; c_mp[aj] += eps_fd
            c_mm = np.zeros(3); c_mm[ai] = -eps_fd; c_mm[aj] -= eps_fd

            Qpp = Q_test.copy(); Qpp[li] = Q_test[li] @ su2_exp(c_pp)
            Qpm = Q_test.copy(); Qpm[li] = Q_test[li] @ su2_exp(c_pm)
            Qmp = Q_test.copy(); Qmp[li] = Q_test[li] @ su2_exp(c_mp)
            Qmm = Q_test.copy(); Qmm[li] = Q_test[li] @ su2_exp(c_mm)

            h_fd = (compute_action(Qpp) - compute_action(Qpm) - compute_action(Qmp) + compute_action(Qmm)) / (4*eps_fd**2)
        else:
            # Different links: independent perturbations
            ci_p = np.zeros(3); ci_p[ai] = eps_fd
            ci_m = np.zeros(3); ci_m[ai] = -eps_fd
            cj_p = np.zeros(3); cj_p[aj] = eps_fd
            cj_m = np.zeros(3); cj_m[aj] = -eps_fd

            Qpp = Q_test.copy()
            Qpp[li] = Q_test[li] @ su2_exp(ci_p)
            Qpp[lj] = Q_test[lj] @ su2_exp(cj_p)

            Qpm = Q_test.copy()
            Qpm[li] = Q_test[li] @ su2_exp(ci_p)
            Qpm[lj] = Q_test[lj] @ su2_exp(cj_m)

            Qmp = Q_test.copy()
            Qmp[li] = Q_test[li] @ su2_exp(ci_m)
            Qmp[lj] = Q_test[lj] @ su2_exp(cj_p)

            Qmm = Q_test.copy()
            Qmm[li] = Q_test[li] @ su2_exp(ci_m)
            Qmm[lj] = Q_test[lj] @ su2_exp(cj_m)

            h_fd = (compute_action(Qpp) - compute_action(Qpm) - compute_action(Qmp) + compute_action(Qmm)) / (4*eps_fd**2)

        err = abs(H_anal[i, j] - h_fd)
        if err > max_err:
            max_err = err
        n_checked += 1

    print(f"  Max |H_anal - H_fd| over {n_checked} entries: {max_err:.2e}")
    if max_err < 1e-3:
        print("  Finite-difference verification PASSED")
    else:
        print(f"  WARNING: FD error is large: {max_err:.2e}")

    # ---- Category A: Random Q ----
    print("\n--- Category A: Random Q (30 configs, Haar measure) ---")
    np.random.seed(12345)
    cat_a = []
    for i in range(30):
        Q = config_random()
        t0 = time.time()
        r = analyze_config(Q, f"random-{i}")
        dt = time.time() - t0
        cat_a.append(r)
        all_hnorms.append(r['h_norm'])
        flag = " ***EXCEEDS 1/12***" if r['exceeds_1_12'] else ""
        print(f"  [{i+1:2d}/30] H_norm={r['h_norm']:.6f}  lam_max={r['lambda_max']:.4f}  ({dt:.2f}s){flag}")
    results.extend(cat_a)

    hnorms_a = [r['h_norm'] for r in cat_a]
    print(f"  Summary: max H_norm = {max(hnorms_a):.6f}, "
          f"mean = {np.mean(hnorms_a):.6f}, "
          f"min = {min(hnorms_a):.6f}")

    # ---- Category B: Gibbs samples ----
    print("\n--- Category B: Gibbs samples (20 configs) ---")
    cat_b = []
    for beta_g in [0.5, 1.0, 2.0, 3.0]:
        for i in range(5):
            np.random.seed(1000 * int(10*beta_g) + i)
            Q = config_metropolis(beta_g, n_sweeps=300, n_thermalize=200)
            r = analyze_config(Q, f"gibbs-beta{beta_g}-{i}")
            cat_b.append(r)
            all_hnorms.append(r['h_norm'])
            flag = " ***EXCEEDS 1/12***" if r['exceeds_1_12'] else ""
            print(f"  beta_gibbs={beta_g:.1f} [{i+1}/5] H_norm={r['h_norm']:.6f}  lam_max={r['lambda_max']:.4f}{flag}")
    results.extend(cat_b)

    hnorms_b = [r['h_norm'] for r in cat_b]
    print(f"  Summary: max H_norm = {max(hnorms_b):.6f}, "
          f"mean = {np.mean(hnorms_b):.6f}")

    # ---- Category C: Perturbations of Q=I ----
    print("\n--- Category C: Perturbations of Q=I (20 configs) ---")
    cat_c = []
    for eps in [0.01, 0.1, 0.3, 0.5, 1.0]:
        for i in range(4):
            np.random.seed(2000 + int(100*eps) + i)
            Q = config_perturbed_identity(eps)
            r = analyze_config(Q, f"perturb-eps{eps}-{i}")
            cat_c.append(r)
            all_hnorms.append(r['h_norm'])
            flag = " ***EXCEEDS 1/12***" if r['exceeds_1_12'] else ""
            print(f"  eps={eps:.2f} [{i+1}/4] H_norm={r['h_norm']:.6f}  lam_max={r['lambda_max']:.4f}{flag}")
    results.extend(cat_c)

    hnorms_c = [r['h_norm'] for r in cat_c]
    print(f"  Summary: max H_norm = {max(hnorms_c):.6f}, "
          f"mean = {np.mean(hnorms_c):.6f}")

    # ---- Category D: Adversarial search ----
    print("\n--- Category D: Adversarial stochastic ascent (30 configs) ---")
    cat_d = []
    for trial in range(30):
        np.random.seed(3000 + trial)
        Q = config_random()
        H_curr = compute_hessian(Q)
        eigvals = np.linalg.eigvalsh(H_curr)
        lmax_curr = eigvals[-1]
        hnorm_init = lmax_curr / (48 * beta)

        n_steps = 300
        n_accept = 0
        step_size = 0.3  # initial step size

        for step in range(n_steps):
            # Pick random link and random su(2) direction
            l_perturb = np.random.randint(n_links)
            c = step_size * np.random.randn(3)
            R = su2_exp(c)
            Q_new_l = Q[l_perturb] @ R

            # Compute new Hessian by updating affected plaquettes
            H_new = H_curr.copy()

            # Subtract old contributions from plaquettes containing l_perturb
            # and add new contributions
            Q_save = Q[l_perturb].copy()
            affected_plaqs = link_to_plaqs[l_perturb]

            # Remove old contributions
            for (p_idx, pos) in affected_plaqs:
                _remove_plaq_contribution(H_new, Q, plaquettes[p_idx])

            # Apply perturbation
            Q[l_perturb] = Q_new_l

            # Add new contributions
            for (p_idx, pos) in affected_plaqs:
                _add_plaq_contribution(H_new, Q, plaquettes[p_idx])

            # Check eigenvalue
            eigvals_new = np.linalg.eigvalsh(H_new)
            lmax_new = eigvals_new[-1]

            if lmax_new > lmax_curr:
                # Accept (ascending)
                lmax_curr = lmax_new
                H_curr = H_new
                n_accept += 1
            else:
                # Reject - revert
                Q[l_perturb] = Q_save
                # H_curr unchanged (we used a copy)

            # Adaptive step size
            if (step + 1) % 50 == 0:
                accept_rate = n_accept / (step + 1)
                if accept_rate > 0.3:
                    step_size *= 1.2
                elif accept_rate < 0.1:
                    step_size *= 0.7

        hnorm_final = lmax_curr / (48 * beta)
        r = {
            "label": f"adversarial-{trial}",
            "lambda_max": float(lmax_curr),
            "lambda_min": float(eigvals[-1]),  # approximate
            "h_norm": float(hnorm_final),
            "h_norm_init": float(hnorm_init),
            "n_accept": n_accept,
            "sym_err": 0.0,
            "exceeds_1_12": bool(hnorm_final > HNORM_CONJ + 1e-10),
            "exceeds_1_8": bool(hnorm_final > HNORM_TRIANG + 1e-10),
        }
        cat_d.append(r)
        all_hnorms.append(r['h_norm'])
        flag = " ***EXCEEDS 1/12***" if r['exceeds_1_12'] else ""
        print(f"  [{trial+1:2d}/30] H_norm: {hnorm_init:.6f} -> {hnorm_final:.6f}  "
              f"accept={n_accept}/{n_steps}{flag}")
    results.extend(cat_d)

    hnorms_d = [r['h_norm'] for r in cat_d]
    print(f"  Summary: max H_norm = {max(hnorms_d):.6f}, "
          f"mean = {np.mean(hnorms_d):.6f}")

    # ---- Overall Summary ----
    print("\n" + "=" * 70)
    print("OVERALL SUMMARY")
    print("=" * 70)
    print(f"Total configurations tested: {len(results)}")
    print(f"Max H_norm observed: {max(all_hnorms):.8f}")
    print(f"  At Q=I (theoretical max): {1/12:.8f}")
    print(f"  Conjecture bound (1/12):  {HNORM_CONJ:.8f}")
    print(f"  Triangle bound (1/8):     {HNORM_TRIANG:.8f}")

    n_exceed_12 = sum(1 for h in all_hnorms if h > HNORM_CONJ + 1e-10)
    n_exceed_8 = sum(1 for h in all_hnorms if h > HNORM_TRIANG + 1e-10)
    print(f"\nConfigs exceeding 1/12: {n_exceed_12}")
    print(f"Configs exceeding 1/8:  {n_exceed_8}")

    # Percentiles
    sorted_h = sorted(all_hnorms)
    print(f"\nDistribution of H_norm:")
    for p in [0, 10, 25, 50, 75, 90, 95, 99, 100]:
        idx = min(int(len(sorted_h) * p / 100), len(sorted_h) - 1)
        print(f"  {p:3d}th percentile: {sorted_h[idx]:.6f}")

    # Final verdict
    if n_exceed_12 == 0:
        print("\n>>> CONJECTURE SUPPORTED: No Q found with H_norm > 1/12 <<<")
        print(f">>> Maximum observed: {max(all_hnorms):.8f} = {max(all_hnorms)*12:.6f}/12 <<<")
    else:
        print(f"\n>>> COUNTEREXAMPLE FOUND: {n_exceed_12} configs with H_norm > 1/12 <<<")

    # Save results
    output = {
        "summary": {
            "n_configs": len(results),
            "max_hnorm": max(all_hnorms),
            "conjecture_bound": HNORM_CONJ,
            "triangle_bound": HNORM_TRIANG,
            "n_exceed_1_12": n_exceed_12,
            "n_exceed_1_8": n_exceed_8,
            "verdict": "SUPPORTED" if n_exceed_12 == 0 else "COUNTEREXAMPLE_FOUND",
        },
        "per_category": {
            "A_random": {"max": max(hnorms_a), "mean": float(np.mean(hnorms_a)), "n": len(cat_a)},
            "B_gibbs": {"max": max(hnorms_b), "mean": float(np.mean(hnorms_b)), "n": len(cat_b)},
            "C_perturb": {"max": max(hnorms_c), "mean": float(np.mean(hnorms_c)), "n": len(cat_c)},
            "D_adversarial": {"max": max(hnorms_d), "mean": float(np.mean(hnorms_d)), "n": len(cat_d)},
        },
        "results": results,
    }

    outpath = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/yang-mills/strategies/strategy-002/explorations/exploration-010/code/results.json"
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {outpath}")


def _remove_plaq_contribution(H, Q, plaq):
    """Remove this plaquette's contribution from H."""
    _update_plaq_contribution(H, Q, plaq, sign=-1)

def _add_plaq_contribution(H, Q, plaq):
    """Add this plaquette's contribution to H."""
    _update_plaq_contribution(H, Q, plaq, sign=+1)

def _update_plaq_contribution(H, Q, plaq, sign=+1):
    """Add (sign=+1) or subtract (sign=-1) a plaquette's Hessian contribution."""
    W = np.zeros((4, 2, 2), dtype=complex)
    link_ids = []
    signs_p = []
    for k, (l, s) in enumerate(plaq):
        link_ids.append(l)
        signs_p.append(s)
        if s == +1:
            W[k] = Q[l]
        else:
            W[k] = su2_dagger(Q[l])

    # Prefix
    Lpre = np.zeros((5, 2, 2), dtype=complex)
    Lpre[0] = I2
    for k in range(4):
        Lpre[k + 1] = Lpre[k] @ W[k]
    retr_UP = np.real(np.trace(Lpre[4]))

    # Suffix
    Rsuf = np.zeros((4, 2, 2), dtype=complex)
    Rsuf[3] = I2
    for k in range(2, -1, -1):
        Rsuf[k] = W[k + 1] @ Rsuf[k + 1]

    # Diagonal (SZZ convention: beta/N)
    beta_N = beta / N_SU
    diag_val = sign * (beta_N / 4.0) * retr_UP
    for k in range(4):
        lk = link_ids[k]
        for a in range(n_gen):
            idx = lk * n_gen + a
            H[idx, idx] += diag_val

    # Off-diagonal
    for k in range(4):
        lk = link_ids[k]
        sk = signs_p[k]
        for m in range(k + 1, 4):
            lm = link_ids[m]
            sm = signs_p[m]
            M_km = I2.copy()
            for j in range(k + 1, m):
                M_km = M_km @ W[j]
            for a in range(n_gen):
                if sk == +1:
                    Ak = W[k] @ tau[a]
                else:
                    Ak = -tau[a] @ W[k]
                LAM = Lpre[k] @ Ak @ M_km
                for b in range(n_gen):
                    if sm == +1:
                        Am = W[m] @ tau[b]
                    else:
                        Am = -tau[b] @ W[m]
                    product = LAM @ Am @ Rsuf[m]
                    val = np.real(np.trace(product))
                    i_idx = lk * n_gen + a
                    j_idx = lm * n_gen + b
                    H[i_idx, j_idx] += sign * (-beta_N) * val
                    H[j_idx, i_idx] += sign * (-beta_N) * val


if __name__ == "__main__":
    main()
