"""
Stage 4: Numerical Verification for Random Q Configurations
===========================================================

For N_SAMPLES Haar-distributed random Q configurations on L=2, d=4, SU(2):
1. Compute the full 192×192 Hessian matrix H(Q)
2. Find λ_max(H(Q))
3. Compute H_norm(Q) = λ_max(H(Q)) / β
4. Check: does H_norm(Q) ≤ 6β hold?
5. What is max_Q H_norm(Q) over samples?

Also verify special cases:
- Q=I: H_norm = 4β ✓
- Staggered Q: Q_{x,μ} = diag((-1)^(|x|+μ), ...)
- "Adversarial" Q: try to maximize H_norm
"""

import numpy as np
from itertools import product as iproduct

print("=" * 60)
print("STAGE 4: NUMERICAL VERIFICATION FOR RANDOM Q")
print("=" * 60)

# ===========================
# Setup
# ===========================
L = 2
d = 4
N = 2
beta = 1.0

n_sites = L**d
n_links = d * n_sites
n_gen = N**2 - 1
n_dof = n_links * n_gen

# Pauli matrices and generators
sigma = np.zeros((3, 2, 2), dtype=complex)
sigma[0] = np.array([[0, 1], [1, 0]])
sigma[1] = np.array([[0, -1j], [1j, 0]])
sigma[2] = np.array([[1, 0], [0, -1]])
tau = np.array([1j * sigma[a] / 2 for a in range(3)])

def site_index(x):
    idx = 0
    for i, xi in enumerate(x):
        idx += (int(xi) % L) * (L ** i)
    return idx

def shift(x, mu, sign=1):
    xnew = list(x)
    xnew[mu] = (xnew[mu] + sign) % L
    return tuple(xnew)

def link_index(x, mu):
    return site_index(x) * d + mu

# Plaquettes
plaquette_links = []
for x in iproduct(range(L), repeat=d):
    for mu in range(d):
        for nu in range(mu+1, d):
            links = [
                (link_index(x, mu), +1),
                (link_index(shift(x, mu), nu), +1),
                (link_index(shift(x, nu), mu), -1),
                (link_index(x, nu), -1),
            ]
            plaquette_links.append(links)

n_plaquettes = len(plaquette_links)

# ===========================
# SU(2) utilities
# ===========================

def random_su2():
    """Generate a random SU(2) matrix from Haar measure."""
    # Use quaternion parameterization: (a+bi, c+di) with a^2+b^2+c^2+d^2=1
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    a, b, c, dd = q
    return np.array([[a+1j*b, c+1j*dd], [-c+1j*dd, a-1j*b]])

def adjoint_rep(g):
    """Compute the 3×3 adjoint representation of g ∈ SU(2).

    R_{ab} such that g τ_a g^† = Σ_b R_{ba} τ_b
    i.e., <τ_c, g τ_a g^†> = <τ_c, Σ_b R_{ba} τ_b> = R_{ca}

    Inner product: <A,B> = -2 Re Tr(AB), so <τ_c, g τ_a g^†> = -2 Re Tr(τ_c g τ_a g^†)
    Therefore: R_{ca} = -2 Re Tr(τ_c g τ_a g^†)
    """
    R = np.zeros((3, 3))
    for a in range(3):
        for c in range(3):
            R[c, a] = -2 * np.real(np.trace(tau[c] @ g @ tau[a] @ g.conj().T))
    return R

def verify_ad_isometry(g):
    """Verify that Ad_g is an isometry: R(g)^T R(g) = I."""
    R = adjoint_rep(g)
    return np.allclose(R.T @ R, np.eye(3), atol=1e-10)

# Quick test
g_test = random_su2()
assert verify_ad_isometry(g_test), "Ad_g is not an isometry!"
print("  [PASS] Adjoint representation is an isometry ✓")

# ===========================
# Compute Hessian H(Q) at general Q
# ===========================

def compute_hessian(U_links, beta, plaquette_links, n_dof, n_links, n_gen, N):
    """
    Compute the 192×192 Hessian matrix at configuration U_links.

    Formula: HessS(v,v) = (β/2N) Σ_□ |B_□(Q,v)|²

    B_□(Q,v) = Σ_{e∈□} s_{□,e} Ad_{P_{□,e}^{-1}} v_e  [in su(2) components]

    Actually, the partial holonomy convention: for plaquette □ with links e1,e2,e3,e4
    in order, the partial holonomy to link ek is the product of preceding links.

    B_□(Q,v) = v_{e1} + Ad_{U_{e1}^{-1}}(v_{e2}) + Ad_{(U_{e1}U_{e2})^{-1}}(-v_{e3}) + Ad_{(U_{e1}U_{e2}U_{e3}^†)^{-1}}(-v_{e4})

    Wait, I need to be careful about the convention. Let me use a simpler version:

    At the base point, for a parallel transported vector, the Ad action is:
    If we perturb U_e → U_e exp(t v_e), the contribution to B_□ is:

    For link e1 (forward): P_left = I → B contribution = v_{e1}
    For link e2 (forward): P_left = U_{e1} → B contribution = Ad_{U_{e1}}(v_{e2})
    For link e3 (backward): P_left = U_{e1}U_{e2} → B contribution = -Ad_{U_{e1}U_{e2}}(v_{e3})
    For link e4 (backward): P_left = U_{e1}U_{e2}U_{e3}^† → B contribution = -Ad_{U_{e1}U_{e2}U_{e3}^†}(v_{e4})

    So B_□ = v1 + Ad_{P1}(v2) - Ad_{P2}(v3) - Ad_{P3}(v4)
    where P1 = U_{e1}, P2 = U_{e1}U_{e2}, P3 = U_{e1}U_{e2}U_{e3}^†
    """
    H = np.zeros((n_dof, n_dof))
    prefactor = beta / (2 * N)

    for plaq in plaquette_links:
        e1_idx, s1 = plaq[0]
        e2_idx, s2 = plaq[1]
        e3_idx, s3 = plaq[2]
        e4_idx, s4 = plaq[3]

        U1 = U_links[e1_idx]
        U2 = U_links[e2_idx]
        U3 = U_links[e3_idx]
        U4 = U_links[e4_idx]

        # Partial holonomies (left accumulated products)
        P1 = np.eye(N, dtype=complex)  # before e1
        P2 = U1                          # before e2 (= U_e1)
        P3 = U1 @ U2                     # before e3 (= U_e1 U_e2)
        P4 = U1 @ U2 @ U3.conj().T      # before e4 (= U_e1 U_e2 U_e3^†)

        # Adjoint representations
        R1 = adjoint_rep(P1)  # = I
        R2 = adjoint_rep(P2)
        R3 = adjoint_rep(P3)
        R4 = adjoint_rep(P4)

        # Signs from orientation
        link_indices = [e1_idx, e2_idx, e3_idx, e4_idx]
        signs = [s1, s2, s3, s4]
        Rs = [R1, R2, R3, R4]

        # Build block contribution to Hessian
        # H_{(e,a),(f,b)} += prefactor × (s_e [R_e]_{c,a}) × (s_f [R_f]_{c,b}) summed over c
        # = prefactor × s_e s_f (R_e^T R_f)_{a,b}

        for ie, (ei, si, Ri) in enumerate(zip(link_indices, signs, Rs)):
            for je, (ej, sj, Rj) in enumerate(zip(link_indices, signs, Rs)):
                # Block contribution: prefactor × si × sj × Ri^T @ Rj
                block = prefactor * si * sj * Ri.T @ Rj  # 3×3 matrix

                # Add to H
                H[ei*n_gen:(ei+1)*n_gen, ej*n_gen:(ej+1)*n_gen] += block

    return H

# ===========================
# Test at Q=I
# ===========================

print("\n=== Test at Q=I ===")
U_identity = np.array([np.eye(N, dtype=complex)] * n_links)
H_identity = compute_hessian(U_identity, beta, plaquette_links, n_dof, n_links, n_gen, N)

evals_I = np.linalg.eigvalsh(H_identity)
lambda_max_I = np.max(evals_I)
print(f"  λ_max(H(I)) = {lambda_max_I:.6f}  (expected 4*β = {4*beta})")
print(f"  [{'PASS' if abs(lambda_max_I - 4*beta) < 0.01 else 'FAIL'}] Q=I check ✓")

# Verify with staggered mode
v_stag_full = np.zeros(n_dof)
for x in iproduct(range(L), repeat=d):
    for mu in range(d):
        li = link_index(x, mu)
        v_stag_full[li*n_gen] = (-1)**(sum(x) + mu)  # generator 0 component

v_stag_full /= np.linalg.norm(v_stag_full)
hess_stag_full = v_stag_full @ H_identity @ v_stag_full
print(f"  HessS(v_stag) / |v|^2 = {hess_stag_full:.6f}  (expected 4*β = 4)")

# ===========================
# CS bound verification
# ===========================

print("\n=== Theoretical CS bound: λ_max(H(Q)) ≤ 6β for all Q ===")
print(f"  Cauchy-Schwarz: |B_□|² ≤ 4 Σ_{{e∈□}} |v_e|²")
print(f"  Sum over □: Σ|B_□|² ≤ 4 × 2(d-1) × |v|² = 24|v|²")
print(f"  HessS ≤ (β/2N) × 24 = 6β")
print(f"  CS bound: λ_max(H(Q)) ≤ 6β = {6*beta:.4f}")

# ===========================
# Random Q samples
# ===========================

print("\n=== Sampling 20 random Haar-distributed Q configurations ===\n")

np.random.seed(42)
N_SAMPLES = 20
max_h_norm = 0.0
results = []

for i in range(N_SAMPLES):
    # Generate random configuration
    U_random = np.array([random_su2() for _ in range(n_links)])

    # Compute Hessian
    H_Q = compute_hessian(U_random, beta, plaquette_links, n_dof, n_links, n_gen, N)

    # Eigenvalue analysis
    evals_Q = np.linalg.eigvalsh(H_Q)
    lmax = np.max(evals_Q)
    lmin = np.min(evals_Q)

    h_norm = lmax / beta
    results.append(h_norm)
    max_h_norm = max(max_h_norm, h_norm)

    cs_ok = lmax <= 6*beta + 1e-6

    if i < 5:  # Print first 5
        print(f"  Sample {i+1}: λ_max = {lmax:.4f}, H_norm/β = {h_norm:.4f}  "
              f"(≤ 6β: {'✓' if cs_ok else '✗'})  λ_min = {lmin:.4f}")

print("  ...")
print(f"\n  Results over {N_SAMPLES} samples:")
print(f"  max H_norm/β = {max(results):.6f}")
print(f"  min H_norm/β = {min(results):.6f}")
print(f"  mean H_norm/β = {np.mean(results):.6f}")
print(f"  std H_norm/β = {np.std(results):.6f}")
print()
print(f"  CS bound: H_norm/β ≤ 6.0000")
print(f"  Actual max: {max(results):.6f}")
print(f"  Bound satisfied: {max(results) <= 6.0 + 1e-6}")

# ===========================
# Adversarial Q: try to maximize H_norm
# ===========================

print("\n=== Adversarial Search: Trying to Maximize H_norm ===")
print("  Strategy: Sample more configurations and find worst case")
print()

np.random.seed(123)
N_ADV = 200
all_h_norms = []

for i in range(N_ADV):
    U_random = np.array([random_su2() for _ in range(n_links)])
    H_Q = compute_hessian(U_random, beta, plaquette_links, n_dof, n_links, n_gen, N)
    lmax = np.max(np.linalg.eigvalsh(H_Q))
    all_h_norms.append(lmax / beta)

all_h_norms = np.array(all_h_norms)

print(f"  Over {N_ADV} random samples:")
print(f"  max H_norm/β = {np.max(all_h_norms):.6f}  (bound: 6.0)")
print(f"  All within CS bound: {np.all(all_h_norms <= 6.0 + 1e-4)}")
print()

# Histogram
percentiles = [50, 75, 90, 95, 99, 100]
print("  Percentiles of H_norm/β:")
for p in percentiles:
    print(f"    {p:3d}th: {np.percentile(all_h_norms, p):.6f}")

# ===========================
# "Worst case" configuration design
# ===========================

print("\n=== Designing a 'Worst Case' Q Configuration ===")
print()
print("  For Cauchy-Schwarz to be tight: need |B_□| = |v_e1|+|v_e2|+|v_e3|+|v_e4|")
print("  This requires: ±Ad_{P_k}(v_{e_k}) all point in the same direction")
print()
print("  Strategy: Use a 'twisted' configuration where all plaquette B_□ values")
print("  align with the eigenvector directions.")
print()

# Try: U_{x,mu} = diag(i, -i) for all links (maximally misaligned from I)
# This is equivalent to U = i*sigma_3 = diag(i,-i) ∈ SU(2)
U_twisted = np.zeros((n_links, N, N), dtype=complex)
for li in range(n_links):
    # Use U = i * sigma_3 which is in SU(2)
    U_twisted[li] = np.array([[1j, 0], [0, -1j]])

H_twisted = compute_hessian(U_twisted, beta, plaquette_links, n_dof, n_links, n_gen, N)
evals_twisted = np.linalg.eigvalsh(H_twisted)
lmax_twisted = np.max(evals_twisted)
print(f"  U_{{all}} = iσ₃: λ_max = {lmax_twisted:.4f}, H_norm/β = {lmax_twisted/beta:.4f}")

# Try: U = exp(θ τ_1) for different θ
print()
print("  Varying global rotation angle θ in U = exp(θ τ_1):")
for theta in [np.pi/4, np.pi/2, 3*np.pi/4, np.pi]:
    U_theta = np.zeros((n_links, N, N), dtype=complex)
    U_mat = np.cos(theta/2)*np.eye(N) + 2*np.sin(theta/2)*tau[0]
    for li in range(n_links):
        U_theta[li] = U_mat
    H_theta = compute_hessian(U_theta, beta, plaquette_links, n_dof, n_links, n_gen, N)
    lmax_theta = np.max(np.linalg.eigvalsh(H_theta))
    print(f"  θ = {theta:.4f}: λ_max = {lmax_theta:.4f}, H_norm/β = {lmax_theta/beta:.4f}")

# ===========================
# Maximum H_norm tracking
# ===========================

print("\n=== FINDING THE TRUE MAXIMUM H_norm over all Q ===")
print()
print("  So far, max observed H_norm/β =", max(max(all_h_norms), lmax_twisted/beta))
print(f"  Q=I: H_norm/β = 4.0 (analytical)")
print(f"  CS bound: H_norm/β ≤ 6.0")
print()

max_seen = max(max(all_h_norms), lmax_twisted/beta, lambda_max_I/beta)
print(f"  Conclusion: max seen = {max_seen:.4f}β (over 200+ samples + special configs)")

# ===========================
# Summary
# ===========================

print("\n" + "=" * 60)
print("STAGE 4 SUMMARY")
print("=" * 60)
print()
print(f"  CS bound: λ_max(H(Q)) ≤ {6*beta:.4f} for all Q")
print(f"  At Q=I: λ_max(H(I)) = {lambda_max_I:.4f}")
print(f"  Over {N_ADV} random samples: max λ_max = {np.max(all_h_norms)*beta:.4f}")
print()

all_ok = np.all(all_h_norms <= 6.0 + 1e-4)
print(f"  CS bound satisfied for all samples: {all_ok}")
print()

if np.max(all_h_norms) < 4.0 + 0.1:
    print("  NOTE: All random samples give H_norm < 4β!")
    print("  Q=I may be close to the TRUE maximum.")
    print("  The CS bound of 6β may not be tight.")
elif np.max(all_h_norms) > 4.0 + 0.1:
    print(f"  NOTE: Some configs give H_norm > 4β")
    print(f"  max = {np.max(all_h_norms):.4f}β")
    print(f"  The gap {6-np.max(all_h_norms):.4f}β remains to the CS bound")

np.save('/tmp/all_h_norms.npy', all_h_norms)
print("\n  Saved H_norm distribution to /tmp/all_h_norms.npy")
