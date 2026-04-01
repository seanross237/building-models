"""
Part 4: Test d=5 on 2^5 lattice. Expected H_norm_max = 3/40 = 0.075
SZZ bound for d=5: 8*(d-1)*N*beta = 8*4*2*beta = 64*beta
Tight claim: lambda_max = 3/40 * 64*beta = 4.8*beta

Convention: S = -(beta/(2N)) * sum Re Tr = -(beta/2) * sum Re Tr for SU(2)
"""

import numpy as np
import json

np.random.seed(42)

L = 2
d = 5
beta = 1.0
N_group = 2  # SU(2)

n_sites = L**d   # 32
n_links = n_sites * d   # 160
n_generators = 3
matrix_size = n_links * n_generators  # 480

print(f"d={d}, L={L}, n_sites={n_sites}, n_links={n_links}, matrix_size={matrix_size}")

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

# Build K matrix with SZZ convention (factor = 1/(2N) = 1/4)
# K[li, lj] = (beta/(2N)) / 2 * si * sj summed over plaquettes
# = (beta/4) * (1/2) * si * sj = (beta/8) * si * sj... wait

# Let me be careful:
# S = -(beta/N) * sum_{mu<nu, x} Re Tr(U_plaq)   <- SZZ convention
# For SU(2), N=2, so S = -(beta/2) * sum Re Tr(U_plaq)
# The Hessian: H[(li,a),(lj,b)] = d^2 S / (dv_i^a dv_j^b)
#   = -(beta/2) * si * sj * Re Tr(tau_a * tau_b)
#   = -(beta/2) * si * sj * (-delta_{ab}/2)
#   = (beta/4) * si * sj * delta_{ab}
# So K[li, lj] = (beta/4) * sum_{plaq containing li and lj} si * sj
# Compare to d=4 case where K[li,lj] = (beta/2) * si * sj (with S1 convention, factor=1/2)
# With S2 convention (factor=1/2 * 1/2 = 1/4): K[li,lj] = (beta/4) * si * sj

n_plaquettes = n_sites * d * (d-1) // 2
print(f"Number of plaquettes: {n_plaquettes}")  # 32 * 10 = 320

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
                    K[li, lj] += (beta / 4) * si * sj   # SZZ convention, SU(2)

print(f"K diagonal value: {K[0,0]:.4f}")
# Expected: each link in 2*(d-1) = 8 plaquettes, diagonal = 8 * (beta/4) = 2*beta

# Build full H = K tensor I_3
H = np.zeros((matrix_size, matrix_size))
for li in range(n_links):
    for lj in range(n_links):
        for a in range(n_generators):
            H[dof_idx(li, a), dof_idx(lj, a)] = K[li, lj]

print("Computing eigenvalues...")
eigs = np.linalg.eigvalsh(H)
lambda_max = eigs.max()
print(f"lambda_max = {lambda_max:.6f}")
print(f"lambda_max / beta = {lambda_max/beta:.4f}")
print(f"lambda_max / (64*beta) = {lambda_max/(64*beta):.6f}")
print(f"3/40 = {3/40:.6f}")
print(f"H_norm_max = lambda_max / (8*(d-1)*N*beta) = {lambda_max/(8*(d-1)*N_group*beta):.6f}")
print(f"Matches 3/40? {np.isclose(lambda_max/(8*(d-1)*N_group*beta), 3/40)}")

# Unique eigenvalues
unique_eigs = np.unique(np.round(eigs, 6))
print(f"\nUnique eigenvalues:")
for ev in unique_eigs:
    count = np.sum(np.isclose(eigs, ev, atol=1e-5))
    print(f"  {ev:.4f} (mult {count})")

# Check staggered mode
staggered_K = np.zeros(n_links)
for x_idx in range(n_sites):
    x = idx_to_site(x_idx)
    parity = sum(x)
    for mu in range(d):
        staggered_K[link_to_idx(x_idx, mu)] = (-1)**(parity + mu)
staggered_K /= np.linalg.norm(staggered_K)

Kv = K @ staggered_K
rayleigh = staggered_K @ Kv
residual = np.linalg.norm(Kv - rayleigh * staggered_K)
print(f"\nStaggered mode Rayleigh quotient (K): {rayleigh:.6f}")
print(f"Is eigenvector (residual): {residual:.2e}")
print(f"H_norm = {rayleigh/(8*(d-1)*N_group*beta):.6f} (cf 3/40 = {3/40:.6f})")

results_d5 = {
    "d5_test": {
        "d": d, "L": L, "n_sites": n_sites, "n_links": n_links,
        "lambda_max": float(lambda_max),
        "H_norm_max": float(lambda_max/(8*(d-1)*N_group*beta)),
        "expected_H_norm": 3/40,
        "matches_3_40": bool(np.isclose(lambda_max/(8*(d-1)*N_group*beta), 3/40)),
        "staggered_rayleigh": float(rayleigh),
        "staggered_residual": float(residual),
        "unique_eigenvalues": [float(e) for e in unique_eigs],
    }
}

try:
    with open("/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/yang-mills/strategies/strategy-002/explorations/exploration-009/code/results.json", "r") as f:
        old = json.load(f)
    old.update(results_d5)
except:
    old = results_d5

with open("/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/yang-mills/strategies/strategy-002/explorations/exploration-009/code/results.json", "w") as f:
    json.dump(old, f, indent=2)

print("\nDone.")
