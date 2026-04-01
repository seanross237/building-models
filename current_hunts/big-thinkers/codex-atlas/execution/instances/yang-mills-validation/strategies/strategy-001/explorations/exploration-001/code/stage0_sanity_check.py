"""
Stage 0: Convention Setup and Sanity Check for SZZ Yang-Mills
=============================================================

SZZ convention (S2):
- Wilson action: S(Q) = -(beta/N) * sum_{plaquettes} Re Tr(U_plaquette)
- Inner product: <A,B> = -2 Re Tr(AB), |A|^2 = -2 Tr(A^2)
- SU(2) generators: tau_a = i*sigma_a/2, |tau_a|^2 = 1
- N=2, d=4, L=2

At Q=I, the Hessian has an analytical formula:
  Hess_S(v,v) = (beta/2N) * sum_□ |B_□(I,v)|^2
where B_□(I,v) = v_{e1} + v_{e2} - v_{e3} - v_{e4} (sum with orientation)

This gives a block-diagonal Hessian (decoupled by generator index):
  H_{(e1,a),(e2,b)} = delta_{a,b} * (beta/2N) * sum_□ sign(□,e1)*sign(□,e2)

So lambda_max(H) = (beta/2N) * lambda_max(M) where M is the oriented plaquette adjacency matrix.

Sanity checks:
1. Hessian at Q=I is 192x192 (64 links x 3 generators)
2. lambda_max = 4*beta exactly  (SZZ convention)
3. Hessian is positive semi-definite
"""

import numpy as np
from itertools import product as iproduct

# ===========================
# SU(2) Setup
# ===========================

# Pauli matrices
sigma = np.zeros((3, 2, 2), dtype=complex)
sigma[0] = np.array([[0, 1], [1, 0]])
sigma[1] = np.array([[0, -1j], [1j, 0]])
sigma[2] = np.array([[1, 0], [0, -1]])

# Generators tau_a = i*sigma_a/2  (anti-Hermitian)
tau = np.array([1j * sigma[a] / 2 for a in range(3)])

print("=== SU(2) Generator Check ===")
for a in range(3):
    norm_sq = -2 * np.real(np.trace(tau[a] @ tau[a]))
    print(f"  |tau_{a+1}|^2 = -2 Re Tr(tau_{a+1}^2) = {norm_sq:.6f}  (should be 1.0)")

# Check inner product structure: <tau_a, tau_b> = -2 Re Tr(tau_a @ tau_b)
print("\n  Inner products <tau_a, tau_b>:")
for a in range(3):
    for b in range(3):
        ip = -2 * np.real(np.trace(tau[a] @ tau[b]))
        if a == b:
            assert abs(ip - 1.0) < 1e-12, f"Diagonal element wrong: {ip}"
        else:
            assert abs(ip) < 1e-12, f"Off-diagonal element wrong: {ip}"
print("  [PASS] tau_a form an orthonormal basis ✓")
print()

# ===========================
# Lattice Setup L=2, d=4
# ===========================

L = 2
d = 4
N = 2  # SU(2)
beta = 1.0  # unit coupling for analysis

n_sites = L**d    # 16
n_links = d * n_sites  # 64
n_gen = N**2 - 1   # 3
n_dof = n_links * n_gen  # 192

print(f"=== Lattice Setup: L={L}, d={d}, N={N} ===")
print(f"  Sites: {n_sites}")
print(f"  Links: {n_links}")
print(f"  Generators per link: {n_gen}")
print(f"  Total DOF: {n_dof}  (should be 192)")
assert n_dof == 192, f"DOF count wrong: {n_dof}"
print(f"  [PASS] DOF = 192 ✓")
print()

def site_index(x):
    """Convert d-dimensional coordinate to index. x is a tuple."""
    idx = 0
    for i, xi in enumerate(x):
        idx += (int(xi) % L) * (L ** i)
    return idx

def shift(x, mu, sign=1):
    """Shift site x in direction mu by sign."""
    xnew = list(x)
    xnew[mu] = (xnew[mu] + sign) % L
    return tuple(xnew)

def link_index(x, mu):
    """Link index for site x, direction mu."""
    return site_index(x) * d + mu

def dof_index(link_idx, gen_a):
    """DOF index for (link, generator)."""
    return link_idx * n_gen + gen_a

# ===========================
# Build plaquette list
# ===========================

# For each plaquette, store the 4 links with orientations (+1 forward, -1 backward)
# Plaquette at site x, plane (mu,nu): U_mu(x) U_nu(x+mu) U_mu^dag(x+nu) U_nu^dag(x)
# = link(x,mu,+1) * link(x+mu,nu,+1) * link(x+nu,mu,-1) * link(x,nu,-1)

plaquette_links = []  # List of [(link_idx, orientation), ...]

for x in iproduct(range(L), repeat=d):
    for mu in range(d):
        for nu in range(mu+1, d):
            links_in_plaquette = [
                (link_index(x, mu), +1),              # forward in mu
                (link_index(shift(x, mu), nu), +1),   # forward in nu
                (link_index(shift(x, nu), mu), -1),   # backward in mu
                (link_index(x, nu), -1),              # backward in nu
            ]
            plaquette_links.append(links_in_plaquette)

n_plaquettes = len(plaquette_links)
expected_plaquettes = (d*(d-1)//2) * n_sites
print(f"=== Plaquette Count ===")
print(f"  Plaquettes: {n_plaquettes}  (expected: {expected_plaquettes})")
assert n_plaquettes == expected_plaquettes, f"Plaquette count wrong"
print(f"  [PASS] Plaquette count = {n_plaquettes} ✓")
print()

# ===========================
# Build the oriented plaquette adjacency matrix M at Q=I
# ===========================
#
# At Q=I:
#   Hess_S(v,v) = (beta/2N) * sum_□ |B_□|^2
#   B_□ = sum_{e in □} sign(□,e) * v_e  (in su(2))
#
# In components (v_e = sum_a c_{e,a} tau_a):
#   |B_□|^2 = sum_a (sum_{e in □} sign(□,e) * c_{e,a})^2
#
# Hessian matrix:
#   H_{(e1,a1),(e2,a2)} = (beta/2N) * delta_{a1,a2} * sum_□ sign(□,e1)*sign(□,e2)
#
# So H = (beta/2N) * M ⊗ I_{3x3}
# where M_{e1,e2} = sum_□ sign(□,e1)*sign(□,e2)

M = np.zeros((n_links, n_links))
for plaq in plaquette_links:
    for (e1, s1) in plaq:
        for (e2, s2) in plaq:
            M[e1, e2] += s1 * s2

print("=== Oriented Plaquette Adjacency Matrix M ===")
print(f"  M is {M.shape[0]}x{M.shape[1]}")

# Eigenvalues of M
evals_M = np.linalg.eigvalsh(M)
lambda_max_M = np.max(evals_M)
lambda_min_M = np.min(evals_M)

print(f"  lambda_max(M) = {lambda_max_M:.6f}")
print(f"  lambda_min(M) = {lambda_min_M:.6f}")
print()

# ===========================
# Build full Hessian H = (beta/2N) * M ⊗ I_3
# ===========================

# At Q=I, Hessian decouples by generator: H = (beta/2N) * M ⊗ I
# So eigenvalues of H are (beta/2N) * evals_M, each with multiplicity 3

prefactor = beta / (2 * N)
evals_H = prefactor * evals_M  # eigenvalues (each x3 multiplicity)
lambda_max_H = np.max(evals_H)
lambda_min_H = np.min(evals_H)

print("=== Hessian at Q=I (Analytical) ===")
print(f"  H = (beta/2N) * M ⊗ I_3")
print(f"  Prefactor beta/2N = {prefactor:.6f}  (beta={beta}, N={N})")
print(f"  lambda_max(H) = {prefactor:.4f} * {lambda_max_M:.4f} = {lambda_max_H:.6f}")
print(f"  lambda_min(H) = {prefactor:.4f} * {lambda_min_M:.4f} = {lambda_min_H:.6f}")
print()

# ===========================
# Convention Check
# ===========================

expected_lambda_max = 4 * beta  # Should be 4*beta for SZZ convention (S2)

print("=== CONVENTION CHECK ===")
print(f"  lambda_max(H) = {lambda_max_H:.6f}")
print(f"  Expected (SZZ/S2): {expected_lambda_max:.6f} = 4*beta")
print(f"  Expected (S1, wrong): {8*beta:.6f} = 8*beta")

ratio = lambda_max_H / beta
print(f"  lambda_max / beta = {ratio:.6f}")

if abs(ratio - 4.0) < 0.1:
    print("  [PASS] lambda_max = 4*beta  ✓  (S2 / SZZ convention confirmed)")
    convention_ok = True
elif abs(ratio - 8.0) < 0.1:
    print("  [FAIL] lambda_max = 8*beta  ✗  (S1 convention error!)")
    convention_ok = False
else:
    print(f"  [WARN] Unexpected: lambda_max = {ratio:.4f}*beta")
    convention_ok = False

print()

# ===========================
# PSD Check
# ===========================

n_pos = np.sum(evals_H > 1e-8 * lambda_max_H)
n_zero_modes = np.sum(np.abs(evals_H) <= 1e-8 * lambda_max_H)
n_neg = np.sum(evals_H < -1e-8 * lambda_max_H)

print("=== PSD CHECK ===")
print(f"  Positive eigenvalues: {n_pos}")
print(f"  Near-zero eigenvalues: {n_zero_modes}")
print(f"  Negative eigenvalues: {n_neg}")

# Expected zero modes: gauge symmetry gives n_sites * n_gen zero modes
# Actually, for lattice gauge theory, the gauge zero modes are:
# Local gauge transformations: n_sites * (N^2-1) = 16 * 3 = 48 modes
expected_zero_modes = n_sites * n_gen * 3  # rough estimate (may overcorrect)

print(f"  Expected gauge zero modes ~ {n_sites * n_gen}")
print()

if n_neg == 0:
    print("  [PASS] Hessian is positive semi-definite ✓")
else:
    print(f"  [FAIL] {n_neg} negative eigenvalues — not PSD!")

# ===========================
# H_norm and mass gap threshold
# ===========================

print()
print("=== H_NORM ANALYSIS AT Q=I ===")
print()
print("  The Bakry-Émery condition K_S > 0 requires:")
print("  Hess_S(v,v) < (N/2)|v|^2 = 1 * |v|^2  for all v  (N=2)")
print()
print("  H_norm = max_v Hess_S(v,v)/|v|^2 = lambda_max(H)")
print(f"  H_norm at Q=I = lambda_max(H) = {lambda_max_H:.6f}")
print(f"  (as a function of beta: H_norm = {lambda_max_H/beta:.6f} * beta)")
print()
print(f"  Mass gap condition: H_norm * beta < N/2 = 1")
print(f"  i.e., {lambda_max_H/beta:.4f} * beta < 1")
print(f"  i.e., beta < {1/(lambda_max_H/beta):.6f}")
print()

# ===========================
# Identify the maximizing vector at Q=I (staggered mode)
# ===========================

print("=== EIGENVECTOR ANALYSIS ===")
print()
print("  Finding the eigenvector achieving lambda_max(M)...")

evals_M_full, evecs_M = np.linalg.eigh(M)
max_idx = np.argmax(evals_M_full)
v_max = evecs_M[:, max_idx]

print(f"  lambda_max(M) = {evals_M_full[max_idx]:.6f}")
print(f"  Eigenvector norm: {np.linalg.norm(v_max):.6f}")

# Check if it's a staggered mode: v_x = (-1)^(|x|) in link direction mu
# For link (x, mu): (-1)^(sum(x) + mu)
print()
print("  Testing staggered mode v_{x,mu} = (-1)^(|x|+mu):")
v_stag = np.zeros(n_links)
for x in iproduct(range(L), repeat=d):
    for mu in range(d):
        li = link_index(x, mu)
        phase = (-1) ** (sum(x) + mu)
        v_stag[li] = phase
v_stag /= np.linalg.norm(v_stag)

# Rayleigh quotient
rayleigh_stag = v_stag @ M @ v_stag
print(f"  Rayleigh quotient of staggered mode: {rayleigh_stag:.6f}")
print(f"  lambda_max(M) = {lambda_max_M:.6f}")
print(f"  Ratio: {rayleigh_stag/lambda_max_M:.6f}  (1.0 means staggered mode IS the max eigenvector)")

# Also try purely spatial staggered modes
print()
print("  Testing spatial staggered mode v_{x,mu} = (-1)^(|x|):")
v_stag2 = np.zeros(n_links)
for x in iproduct(range(L), repeat=d):
    for mu in range(d):
        li = link_index(x, mu)
        phase = (-1) ** sum(x)
        v_stag2[li] = phase
v_stag2 /= np.linalg.norm(v_stag2)

rayleigh_stag2 = v_stag2 @ M @ v_stag2
print(f"  Rayleigh quotient: {rayleigh_stag2:.6f}")

# ===========================
# Summary
# ===========================

print()
print("=" * 60)
print("STAGE 0 SUMMARY")
print("=" * 60)
print(f"  DOF count: {n_dof} (192) ✓" if n_dof == 192 else f"  DOF count: {n_dof} WRONG")
print(f"  lambda_max(H) = {lambda_max_H:.6f} (expected 4*beta = {4*beta})")
print(f"  Convention: {'S2/SZZ ✓' if convention_ok else 'ERROR ✗'}")
print(f"  PSD: {'✓' if n_neg == 0 else '✗ FAIL'}")
print()
print(f"  Mass gap threshold from Q=I analysis: beta < {1/(lambda_max_H/beta):.6f}")
print()

# Save results
np.save('/tmp/M_matrix.npy', M)
np.save('/tmp/evals_M.npy', evals_M_full)
print("  Saved M matrix and eigenvalues to /tmp/")

# ===========================
# Verify with plaquette count per link
# ===========================

print()
print("=== DIAGONAL OF M ===")
print("  M_{e,e} = number of plaquettes containing link e")
print(f"  Each link should appear in 2*(d-1) = {2*(d-1)} plaquettes")
diag_vals = np.diag(M)
print(f"  M_{{e,e}} values: min={diag_vals.min():.1f}, max={diag_vals.max():.1f}")
print(f"  Expected: {2*(d-1)}")
assert np.allclose(diag_vals, 2*(d-1)), f"Diagonal wrong: {diag_vals[:4]}"
print("  [PASS] All diagonal entries = 2*(d-1) = 6 ✓")
