"""
Fast survey of eigenvalue bounds. No gradient computation — just random sampling
and D/C decomposition.
"""
import numpy as np
import sys
sys.path.insert(0, '.')
from hessian_core import *

def su2_exp(w_vec):
    theta = np.linalg.norm(w_vec)
    if theta < 1e-12:
        return np.eye(2, dtype=complex)
    w = sum(w_vec[a] * isigma[a] for a in range(3))
    return np.cos(theta) * np.eye(2, dtype=complex) + (np.sin(theta)/theta) * w

print("=" * 70)
print("FAST EIGENVALUE SURVEY")
print("=" * 70)

for d in [2, 3, 4]:
    L = 2
    lat = Lattice(d, L)
    rng = np.random.default_rng(42)

    lmins = []
    lmaxs = []
    D_maxs = []
    C_lmaxs = []
    C_norms = []
    H_norms = []

    n_configs = 1000
    for trial in range(n_configs):
        Q = random_config(lat, rng)
        H = compute_hessian(lat, Q)
        evals = np.linalg.eigvalsh(H)

        D = np.diag(np.diag(H))
        C = H - D
        C_evals = np.linalg.eigvalsh(C)

        lmins.append(evals[0])
        lmaxs.append(evals[-1])
        D_maxs.append(np.max(np.diag(H)))
        C_lmaxs.append(C_evals[-1])
        C_norms.append(max(abs(C_evals[0]), abs(C_evals[-1])))
        H_norms.append(max(abs(evals[0]), abs(evals[-1])))

    print(f"\nd={d}, L={L}: {n_configs} random configs")
    print(f"  lambda_min(H):  min={min(lmins):.4f}, mean={np.mean(lmins):.4f}")
    print(f"  lambda_max(H):  max={max(lmaxs):.4f}, mean={np.mean(lmaxs):.4f}")
    print(f"  ||H||_op:       max={max(H_norms):.4f}")
    print(f"  max D_ii:       max={max(D_maxs):.4f} (flat: {2*(d-1):.1f})")
    print(f"  lambda_max(C):  max={max(C_lmaxs):.4f} (flat: {2*(d+1):.1f})")
    print(f"  ||C||_op:       max={max(C_norms):.4f} (flat: {2*(d+1):.1f})")

    # Ratios to 4d
    print(f"  lambda_max/4d:  {max(lmaxs)/(4*d):.4f}")
    print(f"  |lambda_min|/4d: {abs(min(lmins))/(4*d):.4f}")

    # KEY: is |lambda_min| bounded by lambda_max_flat = 4d?
    print(f"  |lambda_min| <= 4d = {4*d}? {abs(min(lmins)) <= 4*d + 0.01}")

    # CRITICAL: is D_max + C_lmax <= 4d for every config?
    per_config_sum = [D_maxs[i] + C_lmaxs[i] for i in range(n_configs)]
    print(f"  max(D+C_max): {max(per_config_sum):.4f} <= 4d? {max(per_config_sum) <= 4*d + 0.01}")

    # D_min + C_min for lambda_min bound
    D_mins = [min(np.diag(compute_hessian(lat, random_config(lat, rng)))) for _ in range(200)]
    print(f"  min D_ii: {min(D_mins):.4f} (bound: {-2*(d-1):.1f})")

# Also check near-flat perturbations
print("\n" + "=" * 70)
print("NEAR-FLAT PERTURBATIONS")
print("=" * 70)

d = 4
L = 2
lat = Lattice(d, L)
ne = lat.nedges
rng = np.random.default_rng(123)

epsilons = [0, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 3.0]
for eps in epsilons:
    best_lmax = 0
    worst_lmin = 0
    for trial in range(100):
        w = rng.normal(size=(ne, 3))
        Q = [su2_exp(eps * w[e]) for e in range(ne)]
        H = compute_hessian(lat, Q)
        evals = np.linalg.eigvalsh(H)
        best_lmax = max(best_lmax, evals[-1])
        worst_lmin = min(worst_lmin, evals[0])

    print(f"  eps={eps:.1f}: lambda_max={best_lmax:.4f}/{4*d}, lambda_min={worst_lmin:.4f}")

# Cross-term kernel norm: is it ALWAYS exactly 2?
print("\n" + "=" * 70)
print("CROSS-TERM KERNEL NORM DISTRIBUTION")
print("=" * 70)

rng = np.random.default_rng(77)
norms = []
for trial in range(50000):
    M = random_su2(rng)
    N = random_su2(rng)
    F = np.zeros((3, 3))
    for a in range(3):
        for b in range(3):
            F[a, b] = np.real(np.trace(isigma[a] @ M @ isigma[b] @ N))
    norms.append(np.linalg.norm(F, ord=2))

print(f"50000 random (M,N) ∈ SU(2)²:")
print(f"  min ||F||_op = {min(norms):.6f}")
print(f"  max ||F||_op = {max(norms):.6f}")
print(f"  mean ||F||_op = {np.mean(norms):.6f}")
print(f"  std ||F||_op = {np.std(norms):.6f}")
print(f"  percentiles: 1%={np.percentile(norms,1):.4f}, 50%={np.percentile(norms,50):.4f}, 99%={np.percentile(norms,99):.4f}")

# SZZ vs our bound comparison table
print("\n" + "=" * 70)
print("MASS GAP THRESHOLD COMPARISON TABLE")
print("=" * 70)
print("\nAll in our convention (S = -(beta/N) Σ Re Tr, H = ∂²S/∂c², |v|² = Σc²)")
print("Ricci per component: Ric_ij = 2 δ_ij for SU(2)")
print("B-E: 2I + H >= (K/2)×(1/2)I i.e. lambda_min(H) >= K/4 - 2")
print("Actually: Ric + Hess(V) >= K g, Ric=2δ, g=(1/2)δ")
print("So: 2δ + H >= K(1/2)δ → lambda_min(H) >= K/2 - 2")
print("K > 0 iff lambda_min > -2")
print()

for d in [2, 3, 4]:
    gersh = 4*(d-1) + 4*(d-1)  # self + cross row sum at flat... actually
    # At flat d=4: self=6, cross_row=18, total=24.
    # General: self=2(d-1), cross per neighbor edge: each plaquette contributes 2 cross-terms (in abs)
    # Actually Gershgorin at flat: 6+18=24 for d=4. Let me compute directly.
    L = 2
    lat = Lattice(d, L)
    Q_flat = flat_config(lat)
    H = compute_hessian(lat, Q_flat)
    gersh = max(H[i,i] + sum(abs(H[i,j]) for j in range(H.shape[0]) if j!=i) for i in range(H.shape[0]))
    lmax = 4*d

    print(f"d={d}:")
    print(f"  SZZ Gershgorin: {gersh:.0f} → beta < 2/{gersh:.0f} = {2/gersh:.4f}")
    print(f"  Our lambda_max: {lmax} → beta < 2/{lmax} = {2/lmax:.4f}")
    print(f"  Improvement: {gersh/lmax:.1f}x")
