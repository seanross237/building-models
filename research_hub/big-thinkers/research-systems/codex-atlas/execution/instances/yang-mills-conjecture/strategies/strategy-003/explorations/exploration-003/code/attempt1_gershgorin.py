"""
Attempt 1: Gershgorin-type bound for lambda_max(HessS).

For symmetric H, lambda_max(H) <= max_i (H_{ii} + sum_{j!=i} |H_{ij}|).

We compute:
- Gershgorin bound at flat connections
- Gershgorin bound at 50 random configs
- Analyze whether the bound is tight enough (i.e., <= 4d)
"""

import numpy as np
import sys
sys.path.insert(0, '.')
from hessian_core import *

def gershgorin_analysis(lat, Q, beta=1.0, N=2):
    """Compute Gershgorin bounds and compare to actual max eigenvalue."""
    H = compute_hessian(lat, Q, beta, N)
    evals = np.linalg.eigvalsh(H)
    lmax = evals[-1]

    n = H.shape[0]
    gersh_bounds = np.zeros(n)
    diag_vals = np.zeros(n)
    offdiag_sums = np.zeros(n)
    for i in range(n):
        diag_vals[i] = H[i,i]
        offdiag_sums[i] = np.sum(np.abs(H[i,:])) - np.abs(H[i,i])
        gersh_bounds[i] = diag_vals[i] + offdiag_sums[i]

    gersh_max = np.max(gersh_bounds)

    return {
        'lmax': lmax,
        'gersh_max': gersh_max,
        'max_diag': np.max(diag_vals),
        'max_offdiag_sum': np.max(offdiag_sums),
        'ratio': gersh_max / (4*lat.d) if 4*lat.d > 0 else 0,
        'gersh_bounds': gersh_bounds,
        'diag_vals': diag_vals,
        'offdiag_sums': offdiag_sums,
    }

def analyze_gershgorin_structure(lat, Q, beta=1.0, N=2):
    """Detailed analysis: break down self/cross contributions to Gershgorin rows."""
    ne = lat.nedges
    # Self-term diagonal: (beta/N) * sum_{box containing e} Re Tr(U_box)
    self_diag = np.zeros(ne)
    for pidx, plaq in enumerate(lat.plaquettes):
        U_plaq = plaquette_holonomy(Q, plaq)
        re_tr = np.real(np.trace(U_plaq))
        for (e, s) in plaq:
            self_diag[e] += (beta/N) * re_tr

    # Cross-term absolute row sums per edge
    H = compute_hessian(lat, Q, beta, N)
    cross_rowsum = np.zeros(ne)
    for e in range(ne):
        for a in range(3):
            i = 3*e + a
            for f in range(ne):
                if f == e:
                    continue
                for b in range(3):
                    j = 3*f + b
                    cross_rowsum[e] += abs(H[i,j])
            # Also add off-diagonal in same edge block (a != b)
            # Actually those are zero since self-terms are proportional to delta_ab
            pass
    cross_rowsum /= 3  # average over color indices

    return self_diag, cross_rowsum

print("=" * 70)
print("ATTEMPT 1: GERSHGORIN BOUND ANALYSIS")
print("=" * 70)

for d in [2, 3, 4]:
    L = 2
    lat = Lattice(d, L)
    rng = np.random.default_rng(42)
    bound_4d = 4 * d

    print(f"\n{'='*60}")
    print(f"d={d}, L={L}, target bound = 4d = {bound_4d}")
    print(f"{'='*60}")

    # Flat config
    Q_flat = flat_config(lat)
    res_flat = gershgorin_analysis(lat, Q_flat)
    print(f"\nFlat (Q=I):")
    print(f"  lambda_max = {res_flat['lmax']:.4f}")
    print(f"  Gershgorin max = {res_flat['gersh_max']:.4f}")
    print(f"  Gersh/4d = {res_flat['ratio']:.4f}")
    print(f"  Max diagonal = {res_flat['max_diag']:.4f}")
    print(f"  Max off-diag row sum = {res_flat['max_offdiag_sum']:.4f}")

    # Z2 flat config
    Q_z2 = flat_config_z2(lat)
    res_z2 = gershgorin_analysis(lat, Q_z2)
    print(f"\nZ2 flat (Q=isigma3):")
    print(f"  lambda_max = {res_z2['lmax']:.4f}")
    print(f"  Gershgorin max = {res_z2['gersh_max']:.4f}")
    print(f"  Gersh/4d = {res_z2['ratio']:.4f}")

    # Random configs
    gersh_ratios = []
    lmax_ratios = []
    for trial in range(50):
        Q_rand = random_config(lat, rng)
        res = gershgorin_analysis(lat, Q_rand)
        gersh_ratios.append(res['ratio'])
        lmax_ratios.append(res['lmax'] / bound_4d)

    print(f"\n50 random configs:")
    print(f"  lambda_max / 4d: max={max(lmax_ratios):.4f}, mean={np.mean(lmax_ratios):.4f}")
    print(f"  Gershgorin / 4d: max={max(gersh_ratios):.4f}, mean={np.mean(gersh_ratios):.4f}")
    print(f"  Gershgorin <= 4d? {all(r <= 1.001 for r in gersh_ratios)}")

    if max(gersh_ratios) > 1.001:
        print(f"  *** GERSHGORIN EXCEEDS 4d! Max ratio = {max(gersh_ratios):.4f} ***")
        print(f"  This means the Gershgorin approach CANNOT directly prove the bound.")

# Detailed structure at flat for d=4
print(f"\n{'='*60}")
print("DETAILED STRUCTURE AT FLAT CONFIG (d=4, L=2)")
print(f"{'='*60}")
lat4 = Lattice(4, 2)
Q_flat4 = flat_config(lat4)
H4 = compute_hessian(lat4, Q_flat4)
n4 = H4.shape[0]

# For each row, decompose into same-edge and cross-edge contributions
ne4 = lat4.nedges
for e in range(min(3, ne4)):
    print(f"\nEdge {e}:")
    for a in range(3):
        i = 3*e + a
        same_edge_offdiag = sum(abs(H4[i, 3*e+b]) for b in range(3) if b != a)
        cross_edge = sum(abs(H4[i, j]) for j in range(n4) if j // 3 != e)
        print(f"  color {a}: diag={H4[i,i]:.4f}, same_edge_off={same_edge_offdiag:.6f}, cross_edge={cross_edge:.4f}")
        print(f"    Gershgorin = {H4[i,i] + same_edge_offdiag + cross_edge:.4f}")
