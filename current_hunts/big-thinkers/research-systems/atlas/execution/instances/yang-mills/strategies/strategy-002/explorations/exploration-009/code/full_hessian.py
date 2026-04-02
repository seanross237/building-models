"""
Full Hessian matrix computation for Wilson action at Q=I
SU(2), L=2 lattice, d=4: 16 sites, 64 links, 3 generators -> 192x192 matrix

The Wilson action: S = -beta * sum_{plaquettes} Re Tr(U_x,mu U_{x+mu,nu} U_{x+nu,mu}^dag U_{x,nu}^dag)

At Q=I, the Hessian H[(x,mu,a),(y,nu,b)] = d^2 S / (dv_{x,mu}^a dv_{y,nu}^b)

For each plaquette P = U1 U2 U3 U4 (in order around the plaquette),
the second derivative wrt perturbations on links i and j:

d^2/dt ds Re Tr(... exp(t T_a) ... exp(s T_b) ...) |_{t=s=0}

where T_a = tau_a (generator).

At Q=I, each U_link = I. The plaquette = I * I * I * I = I.

For a plaquette with links in order [l1, l2, l3, l4] (l3, l4 are inverses):
S_plaq = -beta Re Tr(U_{l1} U_{l2} U_{l3}^dag U_{l4}^dag)

Let v_i be the perturbation on link i (in su(2), coefficient of tau_a).
U_{l_i}(t) = exp(t v_{l_i}) ~ I + t v_{l_i} + (t^2/2) v_{l_i}^2 + ...
For inverse links: U_{l_i}^dag(t) = exp(-t v_{l_i}) ~ I - t v_{l_i} + (t^2/2) v_{l_i}^2 + ...

Let sign_i = +1 if link i appears as U (forward), -1 if as U^dag (backward) in plaquette.

Then d^2/dt_i dt_j Re Tr(product) |_{all t=0}:

Case i=j (same link):
  d^2/dt^2 Re Tr(...(I + t*sign*v + t^2/2*(sign*v)^2 +...)*...) |_{t=0}
  = Re Tr(v_i^2) (from the single link's quadratic term, with all others = I)
  But sign^2 = 1, so = Re Tr(v_i^2)

Case i != j (different links):
  d/dt_i d/dt_j Re Tr(... (I + t_i*s_i*v_i +...) ... (I + t_j*s_j*v_j +...) ...) |_{t=0}
  = s_i * s_j * Re Tr(ordering of v_i and v_j in the product)
  where ordering means: if v_i comes before v_j in the product, we get Re Tr(v_i * v_j),
  if v_j comes before v_i, Re Tr(v_j * v_i).
  Since Re Tr is cyclic and Re Tr(AB) = Re Tr(BA) for matrices...
  actually Re Tr(v_i * [I...I] * v_j) = Re Tr(v_j * v_i) by cyclicity.

  Wait, let me be more careful. The plaquette product is P = M_1 * M_2 * M_3 * M_4
  where M_k = I + t_k * s_k * v_k + O(t^2)

  The cross term in d^2 P / dt_i dt_j = s_i * s_j * (product with v_i at position i, v_j at position j)

  So d^2 Re Tr(P) / dt_i dt_j = s_i * s_j * Re Tr(v_i inserted at pos i, v_j at pos j)

  With all other links = I, this is just:
  s_i * s_j * Re Tr( [I]^{stuff before i} * v_i * [I]^{stuff between} * v_j * [I]^{stuff after} )
  = s_i * s_j * Re Tr(v_i * v_j)

  (since identity matrices don't change anything)

  So for i < j in the plaquette ordering:
  H_contribution = -beta * s_i * s_j * Re Tr(tau_a * tau_b)

  For i = j:
  H_contribution = -beta * Re Tr(tau_a^2)  [sign^2=1]

  Wait, actually I need to be careful about Re Tr(tau_a * tau_b).
  With tau_a = i*sigma_a/2:
  tau_a * tau_b = (i sigma_a/2)(i sigma_b/2) = -sigma_a sigma_b / 4

  For a = b: sigma_a^2 = I, so tau_a^2 = -I/4
  Re Tr(tau_a^2) = Re Tr(-I/4) = -2/4 = -1/2

  For a != b: sigma_a sigma_b = i eps_{abc} sigma_c + delta_{ab} I
  = i eps_{abc} sigma_c (since a!=b)
  tau_a tau_b = -i eps_{abc} sigma_c / 4 (purely imaginary trace -> 0)
  Re Tr(tau_a tau_b) = 0 for a != b

  Wait, let me use the standard normalization: Tr(tau_a tau_b) = -delta_{ab}/2
  (this is the standard su(2) convention with tau_a = i sigma_a / 2)

  Check: Tr(tau_a^2) = Tr(-sigma_a^2/4) = Tr(-I/4) = -2/4 = -1/2. Yes.
  Tr(tau_a tau_b) for a!=b: tau_a tau_b = (i sigma_a/2)(i sigma_b/2) = -(sigma_a sigma_b)/4
  For a!=b: sigma_a sigma_b = i eps_{abc} sigma_c, Tr = 0. Correct.

So Re Tr(tau_a tau_b) = -delta_{ab}/2.

Therefore:

H[(x,mu,a),(y,nu,b)] = sum over plaquettes P containing both links (x,mu) and (y,nu):
  -beta * sign_{x,mu,P} * sign_{y,nu,P} * Re Tr(tau_a * tau_b)
  = -beta * sign_{x,mu,P} * sign_{y,nu,P} * (-delta_{ab}/2)
  = (beta/2) * sign_{x,mu,P} * sign_{y,nu,P} * delta_{ab}

Wait, but I need to be more careful about the ordering in the trace.
Re Tr(tau_a * [stuff] * tau_b * [more stuff]) where [stuff] = I (at Q=I).
This equals Re Tr(tau_a * tau_b) = -delta_{ab}/2.

And for the diagonal (same link):
H[(x,mu,a),(x,mu,a)] = sum over plaquettes P containing (x,mu):
  -beta * Re Tr(tau_a^2)
  = -beta * (-1/2)
  = beta/2

Wait, but each link appears in 2(d-1) plaquettes in d dimensions.
For d=4: each link is in 2*3=6 plaquettes.

So H[(x,mu,a),(x,mu,a)] = 6 * (beta/2) = 3*beta?

Hmm, but the staggered mode gives H_norm = 1/12, meaning lambda_max/(48*beta) = 1/12,
so lambda_max = 4*beta. Let me double-check with the off-diagonal contributions.

Actually wait - I'm being sloppy. Let me think again about the diagonal.
For i=j (same link, same generator a=b):
The plaquette P = U1 U2 U3 U4. If link i is U_k (with sign s_k):
d^2/dt^2 Re Tr(...exp(t*s_k*tau_a)...) = Re Tr([other I's] * tau_a^2 * s_k^2)
= Re Tr(tau_a^2) = -1/2

Wait, but s_k^2 = 1 always, so:
Diagonal contribution per plaquette = -beta * Re Tr(tau_a^2) = -beta*(-1/2) = beta/2

And for off-diagonal (same link but different generators a≠b):
Contribution = -beta * Re Tr(tau_a * tau_b) = -beta * 0 = 0 (a≠b)

For different links in the same plaquette (same or different generators):
Contribution = -beta * s_i * s_j * Re Tr(tau_a * tau_b) = (beta/2) * s_i * s_j * delta_{ab}

So the Hessian has the form:
H[(x,mu,a),(y,nu,b)] = delta_{ab} * K[(x,mu),(y,nu)]

where K is a (64x64 matrix of scalars) with:
- Diagonal: K[(x,mu),(x,mu)] = (number of plaquettes containing (x,mu)) * (beta/2) = 6*beta/2 = 3*beta
- Off-diagonal for (x,mu)≠(y,nu): K[(x,mu),(y,nu)] = sum over plaquettes containing both * (beta/2) * s_{x,mu,P} * s_{y,nu,P}

This structure means the 192x192 Hessian is block diagonal: 3 identical 64x64 blocks (one per generator direction), since it's proportional to delta_{ab}.

Wait, is that right? Each 64x64 block is K, and they're all the same. So eigenvalues of H are just the eigenvalues of K, each with multiplicity 3.

Let me code this up properly.
"""

import numpy as np
import itertools
import json

# Parameters
L = 2
d = 4
N = 2  # SU(2)
beta = 1.0  # Will factor out at the end

# Sites: labeled by d-tuples in Z_L^d
def site_to_idx(x):
    """Convert site tuple to index."""
    idx = 0
    for i in range(d):
        idx = idx * L + x[i]
    return idx

def idx_to_site(idx):
    """Convert index to site tuple."""
    x = []
    for i in range(d):
        x.append(idx % L)
        idx //= L
    return tuple(reversed(x))

n_sites = L**d  # 16
n_links = n_sites * d  # 64
n_generators = 3  # su(2)
matrix_size = n_links * n_generators  # 192

print(f"L={L}, d={d}, n_sites={n_sites}, n_links={n_links}, matrix_size={matrix_size}")

# Link indexing: (site_idx, mu) -> link_idx
def link_to_idx(site_idx, mu):
    return site_idx * d + mu

def idx_to_link(link_idx):
    return link_idx // d, link_idx % d

# DOF indexing: (link_idx, a) -> dof_idx
def dof_idx(link_idx, a):
    return link_idx * n_generators + a

# Enumerate all plaquettes
# A plaquette is identified by (x, mu, nu) with mu < nu
# It consists of 4 links:
#   Forward:  (x, mu), (x+mu_hat, nu)
#   Backward: (x+nu_hat, mu), (x, nu)  [these appear as U^dag]
# So signs: +1 for forward, -1 for backward

def add_dir(site, mu):
    """Move site one step in direction mu (mod L)."""
    x = list(site)
    x[mu] = (x[mu] + 1) % L
    return tuple(x)

plaquettes = []  # Each: list of (link_idx, sign)

for x_idx in range(n_sites):
    x = idx_to_site(x_idx)
    for mu in range(d):
        for nu in range(mu+1, d):
            # Plaquette links in order: (x,mu), (x+mu,nu), (x+nu,mu)^{-1}, (x,nu)^{-1}
            x_mu = add_dir(x, mu)
            x_nu = add_dir(x, nu)

            l1 = link_to_idx(site_to_idx(x), mu)       # sign +1
            l2 = link_to_idx(site_to_idx(x_mu), nu)    # sign +1
            l3 = link_to_idx(site_to_idx(x_nu), mu)    # sign -1 (appears as U^dag)
            l4 = link_to_idx(site_to_idx(x), nu)       # sign -1 (appears as U^dag)

            plaquettes.append([(l1, +1), (l2, +1), (l3, -1), (l4, -1)])

n_plaquettes = len(plaquettes)
print(f"Number of plaquettes: {n_plaquettes}")
# Expected: n_sites * d*(d-1)/2 = 16 * 6 = 96

# Build the Hessian
# H is (matrix_size x matrix_size) = 192x192
# H[(li, a), (lj, b)] = delta_{ab} * K[li, lj]
# K[li, lj] = sum over plaquettes containing both li and lj of:
#   (beta/2) * sign_li * sign_lj
# Diagonal (li=lj): K[li,li] = (number of plaquettes containing li) * (beta/2)

# First build K (64x64)
K = np.zeros((n_links, n_links))

for plaq in plaquettes:
    # plaq = [(l1,s1), (l2,s2), (l3,s3), (l4,s4)]
    links_in_plaq = plaq  # list of (link_idx, sign)

    for i, (li, si) in enumerate(links_in_plaq):
        for j, (lj, sj) in enumerate(links_in_plaq):
            # The contribution to K[li, lj]
            # For i==j: contribution is (beta/2) * si^2 = beta/2
            # For i!=j: contribution is (beta/2) * si * sj
            # But wait - I need Re Tr(tau_a * tau_b) = -delta_{ab}/2
            # So H contribution = -beta * si * sj * (-1/2) * delta_{ab}
            #                    = (beta/2) * si * sj * delta_{ab}
            # This applies to both diagonal and off-diagonal in link space
            K[li, lj] += (beta / 2) * si * sj

print(f"\nK matrix built. Shape: {K.shape}")
print(f"K diagonal range: [{K.diagonal().min():.4f}, {K.diagonal().max():.4f}]")
print(f"K expected diagonal: {6 * beta/2:.4f} = 6*beta/2")

# Build full 192x192 Hessian H = K ⊗ I_3
# H[(li,a),(lj,b)] = K[li,lj] * delta_{ab}
H = np.zeros((matrix_size, matrix_size))
for li in range(n_links):
    for lj in range(n_links):
        for a in range(n_generators):
            H[dof_idx(li, a), dof_idx(lj, a)] = K[li, lj]

print(f"\nH matrix built. Shape: {H.shape}")
print(f"H is symmetric: {np.allclose(H, H.T)}")

# Compute eigenvalues
print("\nComputing eigenvalues of H...")
eigenvalues = np.linalg.eigvalsh(H)
print(f"Min eigenvalue: {eigenvalues.min():.6f}")
print(f"Max eigenvalue: {eigenvalues.max():.6f}")
print(f"Max eigenvalue / beta: {eigenvalues.max()/beta:.6f}")
print(f"4*beta = {4*beta:.6f}")
print(f"Max eigenvalue / (48*beta) = {eigenvalues.max()/(48*beta):.6f}")
print(f"1/12 = {1/12:.6f}")
print(f"Max == 4*beta? {np.isclose(eigenvalues.max(), 4*beta)}")

# Also look at unique eigenvalues
unique_eigs = np.unique(np.round(eigenvalues, 8))
print(f"\nUnique eigenvalues (rounded to 8 decimal places):")
for ev in unique_eigs:
    count = np.sum(np.isclose(eigenvalues, ev, atol=1e-6))
    print(f"  {ev:.6f} (multiplicity {count}, ratio to beta: {ev/beta:.4f})")

# Save results
results = {
    "L": L, "d": d, "N": N, "beta": beta,
    "n_sites": n_sites, "n_links": n_links, "matrix_size": matrix_size,
    "n_plaquettes": n_plaquettes,
    "lambda_max": float(eigenvalues.max()),
    "lambda_min": float(eigenvalues.min()),
    "lambda_max_over_beta": float(eigenvalues.max()/beta),
    "lambda_max_over_48beta": float(eigenvalues.max()/(48*beta)),
    "expected_4beta": 4*beta,
    "is_lambda_max_eq_4beta": bool(np.isclose(eigenvalues.max(), 4*beta)),
    "unique_eigenvalues": [float(e) for e in unique_eigs],
}

# Save K and eigenvalues for later use
np.save("/tmp/K_matrix.npy", K)
np.save("/tmp/H_eigenvalues.npy", eigenvalues)

# Also compute full eigenvectors (needed for staggered mode check)
print("\nComputing full eigenvectors...")
eigenvalues_full, eigenvectors = np.linalg.eigh(H)
# eigenvectors[:,i] is the i-th eigenvector
max_idx = np.argmax(eigenvalues_full)
print(f"Maximum eigenvalue: {eigenvalues_full[max_idx]:.6f}")
print(f"Corresponding eigenvector (first 12 components): {eigenvectors[:12, max_idx]}")
np.save("/tmp/H_eigenvectors.npy", eigenvectors)
np.save("/tmp/H_eigenvalues_full.npy", eigenvalues_full)

with open("/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/yang-mills/strategies/strategy-002/explorations/exploration-009/code/results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nResults saved to results.json")
print("Done with Part 1.")
