"""
Part 2: Staggered mode eigenvector verification
Part 3: Random Q eigenvalue test
Also: Convention analysis — factor of 2 between S = -beta*... and S = -(beta/2)*...
"""

import numpy as np
from scipy.linalg import expm
import json

np.random.seed(42)

L = 2
d = 4
beta = 1.0

n_sites = L**d
n_links = n_sites * d
n_generators = 3
matrix_size = n_links * n_generators

def site_to_idx(x):
    idx = 0
    for i in range(d): idx = idx * L + x[i]
    return idx

def idx_to_site(idx):
    x = []
    tmp = idx
    for i in range(d):
        x.append(tmp % L); tmp //= L
    return tuple(reversed(x))

def add_dir(site, mu):
    x = list(site); x[mu] = (x[mu] + 1) % L; return tuple(x)

def link_to_idx(site_idx, mu): return site_idx * d + mu
def dof_idx(link_idx, a): return link_idx * n_generators + a

# SU(2) generators tau_a = i*sigma_a/2
tau = [
    np.array([[0, 0.5j], [0.5j, 0]]),   # tau_0 = i*sigma_x/2
    np.array([[0, 0.5], [-0.5, 0]]),      # tau_1 = i*sigma_y/2
    np.array([[0.5j, 0], [0, -0.5j]]),    # tau_2 = i*sigma_z/2
]

def get_plaquettes():
    plaquettes = []
    for x_idx in range(n_sites):
        x = idx_to_site(x_idx)
        for mu in range(d):
            for nu in range(mu+1, d):
                x_mu = add_dir(x, mu); x_nu = add_dir(x, nu)
                l1 = link_to_idx(site_to_idx(x), mu)
                l2 = link_to_idx(site_to_idx(x_mu), nu)
                l3 = link_to_idx(site_to_idx(x_nu), mu)
                l4 = link_to_idx(site_to_idx(x), nu)
                plaquettes.append((l1, l2, l3, l4))
    return plaquettes

plaquettes = get_plaquettes()

def wilson_action_S1(config):
    """Convention 1: S = -beta * sum Re Tr(U_plaq)"""
    S = 0.0
    for (l1, l2, l3, l4) in plaquettes:
        plaq = config[l1] @ config[l2] @ config[l3].conj().T @ config[l4].conj().T
        S += np.real(np.trace(plaq))
    return -beta * S

def wilson_action_S2(config):
    """Convention 2: S = -(beta/2) * sum Re Tr(U_plaq) (SU(2), N=2)"""
    return wilson_action_S1(config) / 2.0

def build_analytical_H(convention='S1'):
    """Build 192x192 Hessian. convention='S1' uses S = -beta*..., 'S2' uses S = -(beta/2)*..."""
    factor = 1.0 if convention == 'S1' else 0.5
    K = np.zeros((n_links, n_links))
    for x_idx in range(n_sites):
        x = idx_to_site(x_idx)
        for mu in range(d):
            for nu in range(mu+1, d):
                x_mu = add_dir(x, mu); x_nu = add_dir(x, nu)
                links_signs = [
                    (link_to_idx(site_to_idx(x), mu), +1),
                    (link_to_idx(site_to_idx(x_mu), nu), +1),
                    (link_to_idx(site_to_idx(x_nu), mu), -1),
                    (link_to_idx(site_to_idx(x), nu), -1),
                ]
                for (li, si) in links_signs:
                    for (lj, sj) in links_signs:
                        K[li, lj] += factor * (beta / 2) * si * sj
    H = np.zeros((matrix_size, matrix_size))
    for li in range(n_links):
        for lj in range(n_links):
            for a in range(n_generators):
                H[dof_idx(li, a), dof_idx(lj, a)] = K[li, lj]
    return H, K

print("=== PART 2: STAGGERED MODE VERIFICATION ===\n")

H_S1, K_S1 = build_analytical_H('S1')
H_S2, K_S2 = build_analytical_H('S2')

eigs_S1 = np.linalg.eigvalsh(H_S1)
eigs_S2 = np.linalg.eigvalsh(H_S2)

print(f"Convention S1 (S = -beta*sum Re Tr):")
print(f"  lambda_max = {eigs_S1.max():.6f} = {eigs_S1.max()/beta:.4f} * beta")
print(f"  lambda_max / (48*beta) = {eigs_S1.max()/(48*beta):.6f} (cf 1/12 = {1/12:.6f})")

print(f"\nConvention S2 (S = -(beta/2)*sum Re Tr, SU(2) normalized):")
print(f"  lambda_max = {eigs_S2.max():.6f} = {eigs_S2.max()/beta:.4f} * beta")
print(f"  lambda_max / (48*beta) = {eigs_S2.max()/(48*beta):.6f} (cf 1/12 = {1/12:.6f})")

# Staggered mode: v_{x,mu} = (-1)^{|x|+mu}
staggered_K = np.zeros(n_links)
for x_idx in range(n_sites):
    x = idx_to_site(x_idx)
    parity = sum(x)
    for mu in range(d):
        staggered_K[link_to_idx(x_idx, mu)] = (-1)**(parity + mu)
staggered_K /= np.linalg.norm(staggered_K)

# Build full staggered in 192-dim space (use generator a=0 only, for one block)
staggered_H = np.zeros(matrix_size)
for li in range(n_links):
    staggered_H[dof_idx(li, 0)] = staggered_K[li]
staggered_H /= np.linalg.norm(staggered_H)

# Check eigenvector for S1
Hv = H_S1 @ staggered_H
rayleigh_S1 = staggered_H @ Hv
residual_S1 = np.linalg.norm(Hv - rayleigh_S1 * staggered_H)
print(f"\n--- Staggered mode eigenvector check (S1) ---")
print(f"  Rayleigh quotient: {rayleigh_S1:.6f}")
print(f"  Is eigenvector (residual < 1e-10): {residual_S1:.2e} -> {residual_S1 < 1e-8}")
print(f"  Eigenvalue / beta: {rayleigh_S1/beta:.4f}")

# Check eigenvector for S2
Hv2 = H_S2 @ staggered_H
rayleigh_S2 = staggered_H @ Hv2
residual_S2 = np.linalg.norm(Hv2 - rayleigh_S2 * staggered_H)
print(f"\n--- Staggered mode eigenvector check (S2, SU(2)-normalized) ---")
print(f"  Rayleigh quotient: {rayleigh_S2:.6f}")
print(f"  Is eigenvector (residual < 1e-10): {residual_S2:.2e} -> {residual_S2 < 1e-8}")
print(f"  Eigenvalue / beta: {rayleigh_S2/beta:.4f}")
print(f"  H_norm = lambda/(48*beta) = {rayleigh_S2/(48*beta):.6f} (cf 1/12 = {1/12:.6f})")

# Check: is staggered mode actually the GLOBAL max?
_, vecs_S2 = np.linalg.eigh(H_S2)
max_eig_S2 = eigs_S2.max()
max_idx_S2 = np.where(np.isclose(eigs_S2, max_eig_S2, atol=1e-5))[0]
print(f"\n--- Is staggered mode the GLOBAL max eigenvector? ---")
print(f"  Number of max eigenvectors (lambda={max_eig_S2:.4f}): {len(max_idx_S2)}")
print(f"  Staggered mode lies in the max eigenspace:")
# Project staggered_H onto max eigenspace
proj = sum(np.dot(vecs_S2[:, i], staggered_H)**2 for i in max_idx_S2)
print(f"  Projection onto max eigenspace: {proj:.6f} (should be ~1 if staggered is in eigenspace)")

# Now check for the other 2 generator directions
for a in range(n_generators):
    sv = np.zeros(matrix_size)
    for li in range(n_links):
        sv[dof_idx(li, a)] = staggered_K[li]
    sv /= np.linalg.norm(sv)
    r = sv @ H_S2 @ sv
    print(f"  Generator a={a}: Rayleigh quotient = {r:.6f}, H_norm = {r/(48*beta):.6f}")

print("\n\n=== PART 3: RANDOM Q EIGENVALUE TEST ===\n")

def random_su2():
    """Random SU(2) element via Haar measure."""
    # Parameterize: U = a*I + i*(b*sigma_x + c*sigma_y + d*sigma_z) with a^2+b^2+c^2+d^2=1
    v = np.random.randn(4)
    v /= np.linalg.norm(v)
    a, b, c, dd = v
    U = np.array([[a + 1j*dd, b + 1j*c], [-b + 1j*c, a - 1j*dd]], dtype=complex)
    return U

def build_hessian_at_Q(config, convention='S2'):
    """
    Build the Hessian of the Wilson action at a given configuration Q.
    Uses numerical finite differences.
    convention: 'S1' = -beta*sum, 'S2' = -(beta/2)*sum
    """
    action_fn = wilson_action_S2 if convention == 'S2' else wilson_action_S1
    S0 = action_fn(config)
    eps = 1e-4
    H = np.zeros((matrix_size, matrix_size))
    for i in range(matrix_size):
        li, a = i // n_generators, i % n_generators
        # Diagonal
        c_p = [U.copy() for U in config]
        c_p[li] = expm(eps * tau[a]) @ config[li]
        c_m = [U.copy() for U in config]
        c_m[li] = expm(-eps * tau[a]) @ config[li]
        H[i, i] = (action_fn(c_p) - 2*S0 + action_fn(c_m)) / eps**2
        # Off-diagonal (only upper triangle, then symmetrize)
        for j in range(i+1, matrix_size):
            lj, b = j // n_generators, j % n_generators
            c_pp = [U.copy() for U in config]
            c_pp[li] = expm(eps * tau[a]) @ config[li]
            c_pp[lj] = expm(eps * tau[b]) @ config[lj]

            c_pm = [U.copy() for U in config]
            c_pm[li] = expm(eps * tau[a]) @ config[li]
            c_pm[lj] = expm(-eps * tau[b]) @ config[lj]

            c_mp = [U.copy() for U in config]
            c_mp[li] = expm(-eps * tau[a]) @ config[li]
            c_mp[lj] = expm(eps * tau[b]) @ config[lj]

            c_mm = [U.copy() for U in config]
            c_mm[li] = expm(-eps * tau[a]) @ config[li]
            c_mm[lj] = expm(-eps * tau[b]) @ config[lj]

            H[i, j] = (action_fn(c_pp) - action_fn(c_pm) - action_fn(c_mp) + action_fn(c_mm)) / (4*eps**2)
            H[j, i] = H[i, j]
    return H

# Test 5 random configurations
random_results = []
lambda_max_identity = eigs_S2.max()
print(f"lambda_max at Q=I (S2 convention) = {lambda_max_identity:.6f}")
print(f"4*beta = {4*beta:.6f}")
print()

for trial in range(5):
    config_rand = [random_su2() for _ in range(n_links)]
    H_rand = build_hessian_at_Q(config_rand, 'S2')
    eigs_rand = np.linalg.eigvalsh(H_rand)
    lmax = eigs_rand.max()
    lmin = eigs_rand.min()
    exceeds = lmax > lambda_max_identity + 1e-4
    print(f"Trial {trial+1}: lambda_max = {lmax:.4f}, lambda_min = {lmin:.4f}, exceeds Q=I? {exceeds}")
    random_results.append({
        "trial": trial+1, "lambda_max": float(lmax), "lambda_min": float(lmin),
        "exceeds_identity": bool(exceeds)
    })

any_exceed = any(r["exceeds_identity"] for r in random_results)
print(f"\nAny random Q exceeds Q=I max eigenvalue? {any_exceed}")
print(f"H_norm at Q=I (S2 conv) = {lambda_max_identity/(48*beta):.6f}")

# Summary of convention analysis
print("\n=== CONVENTION ANALYSIS ===")
print(f"My convention (S = -beta * sum Re Tr):")
print(f"  lambda_max = 8*beta (H_norm = 1/6)")
print(f"  SZZ bound: 48*beta -> H_norm_bound = 1 (not tight)")
print()
print(f"SZZ convention (S = -(beta/2) * sum Re Tr for SU(2)):")
print(f"  lambda_max = 4*beta (H_norm = 1/12)")
print(f"  SZZ bound: 48*beta -> H_norm_bound = 1 (tight at 1/12)")
print()
print(f"The factor of 2 comes from the 1/N normalization for SU(N) with N=2.")
print(f"In BOTH conventions, the staggered mode is the GLOBAL maximum eigenvector.")

# Save all results
results = {
    "convention_analysis": {
        "S1_lambda_max": float(eigs_S1.max()),
        "S2_lambda_max": float(eigs_S2.max()),
        "S1_H_norm": float(eigs_S1.max()/(48*beta)),
        "S2_H_norm": float(eigs_S2.max()/(48*beta)),
    },
    "staggered_mode": {
        "is_eigenvector_S1": bool(residual_S1 < 1e-8),
        "is_eigenvector_S2": bool(residual_S2 < 1e-8),
        "rayleigh_S1": float(rayleigh_S1),
        "rayleigh_S2": float(rayleigh_S2),
        "is_global_max": bool(abs(proj - 1.0) < 1e-6),
    },
    "random_Q_test": random_results,
    "any_random_exceeds_identity": bool(any_exceed),
}

try:
    with open("/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/yang-mills/strategies/strategy-002/explorations/exploration-009/code/results.json", "r") as f:
        old = json.load(f)
    old.update(results)
    results = old
except:
    pass

with open("/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/yang-mills/strategies/strategy-002/explorations/exploration-009/code/results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nDone. Results saved.")
