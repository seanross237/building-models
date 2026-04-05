"""
Verify the Hessian by:
1. Numerical finite differences of the Wilson action
2. Checking the staggered mode eigenvalue
3. Cross-checking the K matrix structure
"""

import numpy as np
import json

# Parameters
L = 2
d = 4
beta = 1.0

def site_to_idx(x):
    idx = 0
    for i in range(d):
        idx = idx * L + x[i]
    return idx

def idx_to_site(idx):
    x = []
    tmp = idx
    for i in range(d):
        x.append(tmp % L)
        tmp //= L
    return tuple(reversed(x))

def add_dir(site, mu):
    x = list(site)
    x[mu] = (x[mu] + 1) % L
    return tuple(x)

n_sites = L**d
n_links = n_sites * d
n_generators = 3
matrix_size = n_links * n_generators

def link_to_idx(site_idx, mu):
    return site_idx * d + mu

def dof_idx(link_idx, a):
    return link_idx * n_generators + a

# SU(2) generators: tau_a = i*sigma_a/2 (antihermitian)
# Represent as 2x2 complex matrices
def get_tau(a):
    if a == 0:
        return np.array([[0, 0.5j], [0.5j, 0]])
    elif a == 1:
        return np.array([[0, 0.5], [-0.5, 0]])
    else:
        return np.array([[0.5j, 0], [0, -0.5j]])

# Matrix exponential for su(2) element v = sum_a c_a tau_a
def mat_exp_su2(coeffs):
    """exp(coeffs[0]*tau_0 + coeffs[1]*tau_1 + coeffs[2]*tau_2)"""
    M = sum(coeffs[a] * get_tau(a) for a in range(3))
    return np.linalg.matrix_power(np.eye(2, dtype=complex), 0)  # placeholder
    # Use scipy for proper matrix exp
    from scipy.linalg import expm
    return expm(M)

from scipy.linalg import expm

def mat_exp(coeffs):
    M = sum(coeffs[a] * get_tau(a) for a in range(3))
    return expm(M)

# Build link configuration: at Q=I, all links = identity
# config[link_idx] = 2x2 complex matrix (SU(2) element)
def make_identity_config():
    return [np.eye(2, dtype=complex) for _ in range(n_links)]

def make_perturbed_config(base_config, link_idx, a, t):
    """Perturb link link_idx by exp(t * tau_a)"""
    config = [U.copy() for U in base_config]
    config[link_idx] = expm(t * get_tau(a)) @ base_config[link_idx]
    return config

# Enumerate plaquettes: (x_idx, mu, nu) with mu < nu
def get_plaquettes():
    plaquettes = []
    for x_idx in range(n_sites):
        x = idx_to_site(x_idx)
        for mu in range(d):
            for nu in range(mu+1, d):
                x_mu = add_dir(x, mu)
                x_nu = add_dir(x, nu)

                l1 = link_to_idx(site_to_idx(x), mu)
                l2 = link_to_idx(site_to_idx(x_mu), nu)
                l3 = link_to_idx(site_to_idx(x_nu), mu)
                l4 = link_to_idx(site_to_idx(x), nu)

                plaquettes.append((l1, l2, l3, l4))
    return plaquettes

plaquettes = get_plaquettes()

def wilson_action(config):
    """Compute Wilson action S = -beta * sum_plaq Re Tr(U_1 U_2 U_3^dag U_4^dag)"""
    S = 0.0
    for (l1, l2, l3, l4) in plaquettes:
        plaq = config[l1] @ config[l2] @ config[l3].conj().T @ config[l4].conj().T
        S += np.real(np.trace(plaq))
    return -beta * S

# Verify at Q=I
config_I = make_identity_config()
S_I = wilson_action(config_I)
print(f"Wilson action at Q=I: {S_I:.6f}")
print(f"Expected: {-beta * len(plaquettes) * 2:.6f} (= -beta * {len(plaquettes)} plaquettes * Tr(I)=2)")

# Numerical Hessian via finite differences
# H_num[i,j] = (S(t_i=eps, t_j=eps) - S(t_i=eps, t_j=-eps) - S(t_i=-eps, t_j=eps) + S(t_i=-eps, t_j=-eps)) / (4*eps^2)
print("\nComputing numerical Hessian (this takes a few seconds)...")
eps = 1e-4

H_num = np.zeros((matrix_size, matrix_size))

for i in range(matrix_size):
    li, a = i // n_generators, i % n_generators
    for j in range(i, matrix_size):
        lj, b = j // n_generators, j % n_generators

        if i == j:
            # Diagonal: (S(+eps) - 2*S(0) + S(-eps)) / eps^2
            c_pp = make_perturbed_config(config_I, li, a, eps)
            c_mm = make_perturbed_config(config_I, li, a, -eps)
            H_ij = (wilson_action(c_pp) - 2*S_I + wilson_action(c_mm)) / eps**2
        else:
            # Use separate perturbations for i and j
            # Need to perturb two links simultaneously
            config_pp = [U.copy() for U in config_I]
            config_pm = [U.copy() for U in config_I]
            config_mp = [U.copy() for U in config_I]
            config_mm = [U.copy() for U in config_I]

            config_pp[li] = expm(eps * get_tau(a)) @ config_I[li]
            config_pp[lj] = expm(eps * get_tau(b)) @ config_I[lj]

            config_pm[li] = expm(eps * get_tau(a)) @ config_I[li]
            config_pm[lj] = expm(-eps * get_tau(b)) @ config_I[lj]

            config_mp[li] = expm(-eps * get_tau(a)) @ config_I[li]
            config_mp[lj] = expm(eps * get_tau(b)) @ config_I[lj]

            config_mm[li] = expm(-eps * get_tau(a)) @ config_I[li]
            config_mm[lj] = expm(-eps * get_tau(b)) @ config_I[lj]

            H_ij = (wilson_action(config_pp) - wilson_action(config_pm)
                    - wilson_action(config_mp) + wilson_action(config_mm)) / (4*eps**2)

        H_num[i, j] = H_ij
        H_num[j, i] = H_ij

    if i % 20 == 0:
        print(f"  Row {i}/{matrix_size}...")

print("Numerical Hessian computed.")

# Load analytical Hessian from previous computation
# (rebuild it inline)
def build_analytical_K():
    K = np.zeros((n_links, n_links))
    for x_idx in range(n_sites):
        x = idx_to_site(x_idx)
        for mu in range(d):
            for nu in range(mu+1, d):
                x_mu = add_dir(x, mu)
                x_nu = add_dir(x, nu)

                links_signs = [
                    (link_to_idx(site_to_idx(x), mu), +1),
                    (link_to_idx(site_to_idx(x_mu), nu), +1),
                    (link_to_idx(site_to_idx(x_nu), mu), -1),
                    (link_to_idx(site_to_idx(x), nu), -1),
                ]

                for (li, si) in links_signs:
                    for (lj, sj) in links_signs:
                        K[li, lj] += (beta / 2) * si * sj
    return K

K_analytical = build_analytical_K()

# Build analytical H
H_analytical = np.zeros((matrix_size, matrix_size))
for li in range(n_links):
    for lj in range(n_links):
        for a in range(n_generators):
            H_analytical[dof_idx(li, a), dof_idx(lj, a)] = K_analytical[li, lj]

print(f"\nAnalytical H diagonal range: [{H_analytical.diagonal().min():.4f}, {H_analytical.diagonal().max():.4f}]")
print(f"Numerical H diagonal range: [{H_num.diagonal().min():.4f}, {H_num.diagonal().max():.4f}]")

max_diff = np.max(np.abs(H_num - H_analytical))
print(f"\nMax |H_num - H_analytical|: {max_diff:.2e}")
print(f"Are they close? {np.allclose(H_num, H_analytical, atol=1e-6)}")

# Check eigenvalues of numerical Hessian
eigs_num = np.linalg.eigvalsh(H_num)
print(f"\nNumerical Hessian eigenvalues:")
print(f"  Min: {eigs_num.min():.6f}")
print(f"  Max: {eigs_num.max():.6f}")
print(f"  Max/beta: {eigs_num.max()/beta:.6f}")
print(f"  Max/(48*beta): {eigs_num.max()/(48*beta):.6f}")

# Staggered mode check
print("\n--- STAGGERED MODE CHECK ---")
# v_{x,mu} = (-1)^{|x| + mu} where |x| = sum of coordinates
staggered_v = np.zeros(n_links)
for x_idx in range(n_sites):
    x = idx_to_site(x_idx)
    site_parity = sum(x)
    for mu in range(d):
        link_idx = link_to_idx(x_idx, mu)
        staggered_v[link_idx] = (-1)**(site_parity + mu)

# Normalize
staggered_v = staggered_v / np.linalg.norm(staggered_v)
print(f"Staggered vector norm: {np.linalg.norm(staggered_v):.6f}")
print(f"First 8 components: {staggered_v[:8]}")

# Rayleigh quotient for K
Kv = K_analytical @ staggered_v
rayleigh_K = staggered_v @ Kv
print(f"\nRayleigh quotient of K for staggered mode: {rayleigh_K:.6f}")
print(f"Is staggered mode an eigenvector of K? Residual = {np.linalg.norm(Kv - rayleigh_K * staggered_v):.2e}")

# Also try just site parity (no mu dependence)
print("\n--- SITE PARITY MODE ---")
site_parity_v = np.zeros(n_links)
for x_idx in range(n_sites):
    x = idx_to_site(x_idx)
    site_parity = sum(x)
    for mu in range(d):
        link_idx = link_to_idx(x_idx, mu)
        site_parity_v[link_idx] = (-1)**site_parity

site_parity_v = site_parity_v / np.linalg.norm(site_parity_v)
Kv2 = K_analytical @ site_parity_v
rayleigh_K2 = site_parity_v @ Kv2
print(f"Rayleigh quotient of K for site-parity-only mode: {rayleigh_K2:.6f}")
print(f"Is it eigenvector? Residual = {np.linalg.norm(Kv2 - rayleigh_K2 * site_parity_v):.2e}")

# Find what eigenvectors achieve lambda = 8
eigs_K, vecs_K = np.linalg.eigh(K_analytical)
print(f"\nK eigenvalues (unique):")
unique_K = np.unique(np.round(eigs_K, 6))
for ev in unique_K:
    count = np.sum(np.isclose(eigs_K, ev, atol=1e-5))
    print(f"  {ev:.6f} (mult {count})")

# Find eigenvectors with eigenvalue 8
max_eig_idx = np.where(np.isclose(eigs_K, eigs_K.max(), atol=1e-5))[0]
print(f"\nNumber of eigenvectors with lambda_max={eigs_K.max():.4f}: {len(max_eig_idx)}")
print(f"First max eigenvector:\n{vecs_K[:, max_eig_idx[0]]}")

# Check: what is the staggered mode's eigenvalue?
print(f"\nStaggered mode Rayleigh quotient (K): {rayleigh_K:.6f}")
print(f"This corresponds to H_norm = {rayleigh_K/(48*beta):.6f}")
print(f"Compare to 1/12 = {1/12:.6f}")

results_verify = {
    "max_diff_analytical_vs_numerical": float(max_diff),
    "are_close": bool(np.allclose(H_num, H_analytical, atol=1e-6)),
    "numerical_lambda_max": float(eigs_num.max()),
    "analytical_lambda_max": float(np.linalg.eigvalsh(H_analytical).max()),
    "staggered_mode_rayleigh_K": float(rayleigh_K),
    "staggered_mode_rayleigh_Hnorm": float(rayleigh_K / (48 * beta)),
    "K_unique_eigenvalues": [float(e) for e in unique_K],
}

# Load existing results.json and update
try:
    with open("/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/yang-mills/strategies/strategy-002/explorations/exploration-009/code/results.json", "r") as f:
        results = json.load(f)
except:
    results = {}

results.update(results_verify)
with open("/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/yang-mills/strategies/strategy-002/explorations/exploration-009/code/results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nVerification complete. Results updated in results.json")
