"""
hessian_l4.py — L=4, d=4, SU(2) Hessian scan with power iteration.

Tests H_norm = lambda_max / (48*beta) <= 1/12 conjecture.

Configurations tested:
  A. Q=I sanity check (lambda_max should = 4*beta)
  B. Staggered mode check
  C. 20 random Haar configs
  D. 10 Gibbs samples (beta_gibbs = 0.5, 1.0, 2.0, 3.0)
  F. Near-identity perturbations

Convention: S = -(beta/N) sum_P Re Tr(U_P), tau_a = i*sigma_a/2
"""

import numpy as np
import json
import time
import sys

# ============================================================
# Parameters
# ============================================================
L = 4
d = 4
N_SU = 2
beta = 1.0

n_sites = L**d        # 256
n_links = n_sites * d  # 1024
n_gen = 3              # dim su(2)
n_dof = n_links * n_gen  # 3072

HNORM_CONJ = 1.0 / 12  # 0.08333...
LAMBDA_CONJ = 4.0 * beta
LAMBDA_NORM = 48.0 * beta

print(f"L={L}, d={d}, N_SU={N_SU}, beta={beta}")
print(f"n_sites={n_sites}, n_links={n_links}, n_dof={n_dof}")
print(f"Conjecture: lambda_max <= {LAMBDA_CONJ:.4f}, H_norm <= {HNORM_CONJ:.6f}")
print()

# ============================================================
# Pauli matrices and generators
# ============================================================
sigma = np.zeros((3, 2, 2), dtype=complex)
sigma[0] = [[0, 1], [1, 0]]
sigma[1] = [[0, -1j], [1j, 0]]
sigma[2] = [[1, 0], [0, -1]]

tau = 1j * sigma / 2  # tau_a = i*sigma_a/2
# Tr(tau_a tau_b) = -delta_{ab}/2

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
expected_plaq = n_sites * d * (d - 1) // 2
assert n_plaq == expected_plaq, f"Expected {expected_plaq} plaquettes, got {n_plaq}"
print(f"n_plaquettes = {n_plaq}")

# Precompute: for each link, which plaquettes contain it
link_to_plaqs = [[] for _ in range(n_links)]
for p_idx, plaq in enumerate(plaquettes):
    for pos, (l, s) in enumerate(plaq):
        link_to_plaqs[l].append((p_idx, pos))

# Verify each link in 2(d-1)=6 plaquettes
for l in range(n_links):
    assert len(link_to_plaqs[l]) == 2 * (d - 1), \
        f"Link {l} in {len(link_to_plaqs[l])} plaquettes"

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
    """exp(sum_a coeffs[a] * tau_a)"""
    A = coeffs[0] * tau[0] + coeffs[1] * tau[1] + coeffs[2] * tau[2]
    c_sq = float(np.real(coeffs[0]**2 + coeffs[1]**2 + coeffs[2]**2))
    if c_sq < 1e-30:
        return I2 + A
    theta = np.sqrt(c_sq)
    return np.cos(theta / 2) * I2 + (np.sin(theta / 2) / (theta / 2)) * A

# ============================================================
# Configuration generators
# ============================================================
def config_identity():
    Q = np.zeros((n_links, 2, 2), dtype=complex)
    for l in range(n_links):
        Q[l] = I2.copy()
    return Q

def config_random():
    Q = np.zeros((n_links, 2, 2), dtype=complex)
    for l in range(n_links):
        Q[l] = random_su2()
    return Q

def config_perturbed(epsilon):
    Q = np.zeros((n_links, 2, 2), dtype=complex)
    for l in range(n_links):
        c = epsilon * np.random.randn(3)
        Q[l] = su2_exp(c)
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
# Metropolis heat-bath configuration generator
# ============================================================
def config_metropolis(beta_gibbs, n_sweeps=100, n_thermalize=50):
    Q = config_identity()
    delta = 0.5

    for sweep in range(n_thermalize + n_sweeps):
        for l in range(n_links):
            c = delta * np.random.randn(3)
            R = su2_exp(c)
            Q_new = Q[l] @ R
            Q_save = Q[l].copy()

            dS = 0.0
            for (p_idx, pos) in link_to_plaqs[l]:
                plaq = plaquettes[p_idx]
                U_old = plaq_product(Q, plaq)
                Q[l] = Q_new
                U_new = plaq_product(Q, plaq)
                Q[l] = Q_save
                dS += -(beta_gibbs / N_SU) * (np.real(np.trace(U_new)) - np.real(np.trace(U_old)))

            if dS < 0 or np.random.rand() < np.exp(-dS):
                Q[l] = Q_new

    return Q

# ============================================================
# Analytical Hessian for general Q (adapted from E010 scan_hessian.py)
# ============================================================
def compute_hessian(Q):
    """
    Hessian of S = -(beta/N) sum_P Re Tr(U_P).
    Perturbation: Q_l -> Q_l exp(sum_a eps^a tau_a)
    H[i,j] = d^2 S / d(eps_i) d(eps_j), i = l*3 + a
    """
    H = np.zeros((n_dof, n_dof))
    beta_N = beta / N_SU

    for plaq in plaquettes:
        # Build W matrices
        W = np.zeros((4, 2, 2), dtype=complex)
        link_ids = np.zeros(4, dtype=int)
        signs = np.zeros(4, dtype=int)
        for k, (l, s) in enumerate(plaq):
            link_ids[k] = l
            signs[k] = s
            W[k] = Q[l] if s == +1 else su2_dagger(Q[l])

        # Prefix products L[k] = W[0] @ ... @ W[k-1]
        Lpre = np.zeros((5, 2, 2), dtype=complex)
        Lpre[0] = I2
        for k in range(4):
            Lpre[k + 1] = Lpre[k] @ W[k]
        U_P = Lpre[4]
        retr_UP = np.real(np.trace(U_P))

        # Suffix products R[k] = W[k+1] @ ... @ W[3]
        Rsuf = np.zeros((4, 2, 2), dtype=complex)
        Rsuf[3] = I2
        for k in range(2, -1, -1):
            Rsuf[k] = W[k + 1] @ Rsuf[k + 1]

        # Diagonal: (beta_N / 4) * Re Tr(U_P) per link per generator
        diag_val = (beta_N / 4.0) * retr_UP
        for k in range(4):
            lk = link_ids[k]
            for a in range(n_gen):
                H[lk * n_gen + a, lk * n_gen + a] += diag_val

        # Off-diagonal: k < m
        for k in range(4):
            lk = link_ids[k]
            sk = signs[k]
            for m in range(k + 1, 4):
                lm = link_ids[m]
                sm = signs[m]

                # Middle product M_{km} = W[k+1] @ ... @ W[m-1]
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
# Power iteration for lambda_max
# ============================================================
def power_iteration(H, n_iter=200, tol=1e-8):
    """
    Compute lambda_max and v_max of symmetric matrix H via power iteration.
    Returns (lambda_max, v_max, converged, residual).
    """
    n = H.shape[0]
    w = np.random.randn(n)
    w /= np.linalg.norm(w)

    lam = 0.0
    for i in range(n_iter):
        Hw = H @ w
        lam_new = np.dot(w, Hw)
        w_new = Hw / np.linalg.norm(Hw)
        # Check convergence
        if i > 10:
            res = np.linalg.norm(Hw - lam_new * w) / (abs(lam_new) + 1e-30)
            if res < tol:
                return lam_new, w_new, True, res
        lam = lam_new
        w = w_new

    # Final residual
    Hw = H @ w
    lam = np.dot(w, Hw)
    res = np.linalg.norm(Hw - lam * w) / (abs(lam) + 1e-30)
    return lam, w, res < tol, res

# ============================================================
# H_norm computation
# ============================================================
def compute_hnorm(Q, label=""):
    """Compute H_norm = lambda_max / (48*beta) for config Q."""
    t0 = time.time()
    H = compute_hessian(Q)
    t1 = time.time()
    lam, v_max, converged, res = power_iteration(H)
    t2 = time.time()
    hnorm = lam / LAMBDA_NORM
    print(f"  {label}: lambda_max={lam:.6f}, H_norm={hnorm:.8f}, "
          f"converged={converged}, res={res:.2e}, "
          f"Hessian build={t1-t0:.1f}s, power_iter={t2-t1:.1f}s")
    return lam, hnorm, v_max, H

# ============================================================
# PART A: Q=I sanity check
# ============================================================
print("="*60)
print("PART A: Q=I sanity check")
print("="*60)

np.random.seed(42)
Q_I = config_identity()
lam_I, hnorm_I, v_I, H_I = compute_hnorm(Q_I, "Q=I")

# Check lambda_max = 4*beta
assert abs(lam_I - 4.0 * beta) < 0.01, f"SANITY FAIL: lambda_max={lam_I}, expected={4*beta}"
assert abs(hnorm_I - 1.0/12) < 0.01, f"SANITY FAIL: H_norm={hnorm_I}, expected={1/12}"
print(f"  SANITY CHECK PASSED: lambda_max = {lam_I:.6f} ≈ 4*beta = {4*beta:.6f}")
print(f"  H_norm = {hnorm_I:.8f} ≈ 1/12 = {1/12:.8f}")
print()

# ============================================================
# PART B: Staggered mode check
# ============================================================
print("="*60)
print("PART B: Staggered mode verification")
print("="*60)

# Staggered mode: v[x,mu,a] = (-1)^(x0+x1+x2+x3) * delta_{a,0} (for direction mu=0 only)
# Actually the staggered mode at Q=I has v_{x,mu,a} = (-1)^|x| * delta_{a,1}
# where |x| = x0+x1+...+x_{d-1}

# Build staggered vector
v_stag = np.zeros(n_dof)
for l in range(n_links):
    site_idx = l // d
    mu = l % d
    x = idx_to_site(site_idx)
    parity = sum(x) % 2
    sign = (-1)**parity
    # Use generator a=0 (tau_1)
    v_stag[l * n_gen + 0] = sign

# Normalize
v_stag /= np.linalg.norm(v_stag)

# Compute H_I @ v_stag and check if it's an eigenvector with lambda=4*beta
Hv = H_I @ v_stag
lam_stag = np.dot(v_stag, Hv)
res_stag = np.linalg.norm(Hv - lam_stag * v_stag) / (abs(lam_stag) + 1e-30)

print(f"  Staggered mode: Rayleigh quotient = {lam_stag:.6f}")
print(f"  Expected: {4*beta:.6f}")
print(f"  Residual as eigenvector: {res_stag:.2e}")
print(f"  Is eigenvector (res<1e-4)? {res_stag < 1e-4}")
print()

# ============================================================
# PART C: 20 Random Haar configs
# ============================================================
print("="*60)
print("PART C: 20 random Haar configurations")
print("="*60)

results_random = []
max_hnorm_random = 0.0
for i in range(20):
    Q = config_random()
    lam, hnorm, v_max, H = compute_hnorm(Q, f"Random {i+1:02d}")
    results_random.append({"lam": float(lam), "hnorm": float(hnorm)})
    if hnorm > max_hnorm_random:
        max_hnorm_random = hnorm
    if hnorm > HNORM_CONJ:
        print(f"  *** COUNTEREXAMPLE CANDIDATE: H_norm={hnorm:.8f} > 1/12={HNORM_CONJ:.8f} ***")

print(f"\nRandom configs: max H_norm = {max_hnorm_random:.8f} (bound = {HNORM_CONJ:.8f})")
print()

# ============================================================
# PART D: 10 Gibbs samples
# ============================================================
print("="*60)
print("PART D: Gibbs samples")
print("="*60)

beta_gibbs_list = [0.5, 0.5, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 4.0, 4.0]
results_gibbs = []
max_hnorm_gibbs = 0.0

for i, bg in enumerate(beta_gibbs_list):
    print(f"  Generating Gibbs sample {i+1}/10 at beta_gibbs={bg}...")
    Q = config_metropolis(bg, n_sweeps=50, n_thermalize=30)
    lam, hnorm, v_max, H = compute_hnorm(Q, f"Gibbs beta={bg}")
    results_gibbs.append({"beta_gibbs": float(bg), "lam": float(lam), "hnorm": float(hnorm)})
    if hnorm > max_hnorm_gibbs:
        max_hnorm_gibbs = hnorm
    if hnorm > HNORM_CONJ:
        print(f"  *** COUNTEREXAMPLE CANDIDATE: H_norm={hnorm:.8f} > 1/12={HNORM_CONJ:.8f} ***")

print(f"\nGibbs configs: max H_norm = {max_hnorm_gibbs:.8f} (bound = {HNORM_CONJ:.8f})")
print()

# ============================================================
# PART F: Near-identity perturbations (L=4 specific)
# ============================================================
print("="*60)
print("PART F: Near-identity perturbations")
print("="*60)

results_perturb = []
max_hnorm_perturb = 0.0
for eps in [0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0]:
    Q = config_perturbed(eps)
    lam, hnorm, v_max, H = compute_hnorm(Q, f"eps={eps:.2f}")
    results_perturb.append({"epsilon": float(eps), "lam": float(lam), "hnorm": float(hnorm)})
    if hnorm > max_hnorm_perturb:
        max_hnorm_perturb = hnorm

print(f"\nPerturbed configs: max H_norm = {max_hnorm_perturb:.8f}")
print()

# ============================================================
# PART F2: Wavelength-4 staggered mode test
# ============================================================
print("="*60)
print("PART F2: Wavelength-4 mode at L=4")
print("="*60)

# Test v = {(-1)^(x0/2)} * v0  (wavelength-4 in x0 direction)
# This only makes sense at L=4; at L=2 it would give |x0/2| always 0.
v_wave4 = np.zeros(n_dof)
for l in range(n_links):
    site_idx = l // d
    x = idx_to_site(site_idx)
    # Half-integer checkerboard: sign = (-1)^floor(x0/2)
    sign = (-1)**(x[0] // 2)
    v_wave4[l * n_gen + 0] = sign

v_wave4 /= np.linalg.norm(v_wave4)
Hv4 = H_I @ v_wave4
lam_wave4 = np.dot(v_wave4, Hv4)
print(f"  Wavelength-4 mode Rayleigh quotient: {lam_wave4:.6f}")
print(f"  H_norm = {lam_wave4 / LAMBDA_NORM:.8f}")
print(f"  Compare staggered: {lam_stag:.6f} vs wavelength-4: {lam_wave4:.6f}")
print()

# ============================================================
# Save results
# ============================================================
results = {
    "L": L, "d": d, "N_SU": N_SU, "beta": beta,
    "n_sites": n_sites, "n_links": n_links, "n_dof": n_dof, "n_plaq": n_plaq,
    "PART_A": {
        "lambda_max_QI": float(lam_I),
        "hnorm_QI": float(hnorm_I),
        "sanity_passed": abs(lam_I - 4.0*beta) < 0.01,
    },
    "PART_B": {
        "staggered_rayleigh": float(lam_stag),
        "staggered_residual": float(res_stag),
        "is_eigenvector": bool(res_stag < 1e-4),
    },
    "PART_C_random": results_random,
    "PART_C_max_hnorm": float(max_hnorm_random),
    "PART_D_gibbs": results_gibbs,
    "PART_D_max_hnorm": float(max_hnorm_gibbs),
    "PART_F_perturbed": results_perturb,
    "PART_F_max_hnorm": float(max_hnorm_perturb),
    "wavelength4_rayleigh": float(lam_wave4),
    "wavelength4_hnorm": float(lam_wave4 / LAMBDA_NORM),
    "overall_max_hnorm": float(max(hnorm_I, max_hnorm_random, max_hnorm_gibbs, max_hnorm_perturb)),
    "conjecture_violated": bool(max(hnorm_I, max_hnorm_random, max_hnorm_gibbs, max_hnorm_perturb) > HNORM_CONJ),
}

out_path = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/yang-mills/strategies/strategy-003/explorations/exploration-004/code/results.json"
with open(out_path, "w") as f:
    json.dump(results, f, indent=2)

print("="*60)
print("SUMMARY")
print("="*60)
print(f"Q=I: H_norm = {hnorm_I:.8f}")
print(f"Max random:   H_norm = {max_hnorm_random:.8f}")
print(f"Max Gibbs:    H_norm = {max_hnorm_gibbs:.8f}")
print(f"Max perturbed: H_norm = {max_hnorm_perturb:.8f}")
print(f"Overall max:  H_norm = {results['overall_max_hnorm']:.8f}")
print(f"Conjecture violated: {results['conjecture_violated']}")
print(f"Results saved to {out_path}")
print("hessian_l4.py DONE")
