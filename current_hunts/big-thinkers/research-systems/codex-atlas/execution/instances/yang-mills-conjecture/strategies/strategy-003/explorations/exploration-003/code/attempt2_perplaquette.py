"""
Attempt 2: Per-plaquette quadratic form bound.

For any unit vector v, HessS(v,v) = sum_plaq h_plaq(v; Q).

We try to show: h_plaq(v; Q) <= (4*beta/N) * sum_{e in plaq} |c_e|^2
where c_e = (c_{e,1}, c_{e,2}, c_{e,3}).

If this holds, then summing over plaquettes:
  HessS(v,v) <= (4*beta/N) * sum_plaq sum_{e in plaq} |c_e|^2
             = (4*beta/N) * sum_e 2(d-1) |c_e|^2
             = (4*beta/N) * 2(d-1) * |v|^2

Wait, but 4*2(d-1)/N = 4*2(d-1)/2 = 4(d-1), not 4d.
Actually the target bound is 4d*(beta/N). Let me check:
  At flat, self-term per edge = (beta/N) * 2(d-1) * Re Tr(I) = (beta/N) * 2(d-1) * 2 = 4(d-1)*beta/N.
  But E002 says max eigenvalue = 4d * (beta/N) = 16 for d=4, N=2, beta=1.

So the cross-terms at flat add an extra 4*beta/N to the eigenvalue.
  4(d-1) + 4 = 4d. OK so at flat, the cross-terms contribute exactly +4*beta/N extra.

But actually, the per-plaquette bound approach: if we bound each plaquette's contribution
to the quadratic form, we need to handle cross-terms within the plaquette.

Let me compute the per-plaquette Hessian and its max eigenvalue.
"""

import numpy as np
import sys
sys.path.insert(0, '.')
from hessian_core import *

def per_plaquette_hessian(lat, Q, pidx, beta=1.0, N=2):
    """Compute the Hessian contribution from a single plaquette.
    Returns a 12x12 matrix (4 edges * 3 colors)."""
    plaq = lat.plaquettes[pidx]
    edges = [e for (e,s) in plaq]
    signs = [s for (e,s) in plaq]

    U_plaq = plaquette_holonomy(Q, plaq)
    re_tr = np.real(np.trace(U_plaq))

    # 12x12 matrix for the 4 edges of this plaquette
    H_plaq = np.zeros((12, 12))

    # Self-terms
    for idx, (e, s) in enumerate(plaq):
        for a in range(3):
            H_plaq[3*idx+a, 3*idx+a] = (beta/N) * re_tr

    # Cross-terms
    edges_list = list(plaq)
    for p_idx in range(4):
        for q_idx in range(p_idx+1, 4):
            ep, sp = edges_list[p_idx]
            eq, sq = edges_list[q_idx]

            L = np.eye(2, dtype=complex)
            for k in range(p_idx + 1):
                ek, sk = edges_list[k]
                L = L @ (Q[ek] if sk == +1 else su2_inv(Q[ek]))

            mid = np.eye(2, dtype=complex)
            for k in range(p_idx + 1, q_idx):
                ek, sk = edges_list[k]
                mid = mid @ (Q[ek] if sk == +1 else su2_inv(Q[ek]))

            R = np.eye(2, dtype=complex)
            for k in range(q_idx + 1, 4):
                ek, sk = edges_list[k]
                R = R @ (Q[ek] if sk == +1 else su2_inv(Q[ek]))

            for a in range(3):
                for b in range(3):
                    val = -(beta/N) * sp * sq * np.real(
                        np.trace(L @ isigma[a] @ mid @ isigma[b] @ R)
                    )
                    H_plaq[3*p_idx+a, 3*q_idx+b] += val
                    H_plaq[3*q_idx+b, 3*p_idx+a] += val

    return H_plaq, edges

def per_plaquette_eigenvalue_ratio(lat, Q, beta=1.0, N=2):
    """For each plaquette, compute max eigenvalue of H_plaq / (4*beta/N).
    The bound h_plaq(v) <= (4*beta/N) * sum |c_e|^2 would hold iff
    max eigenvalue <= 4*beta/N."""
    ratios = []
    target = 4 * beta / N
    for pidx in range(lat.nplaq):
        H_plaq, edges = per_plaquette_hessian(lat, Q, pidx, beta, N)
        evals = np.linalg.eigvalsh(H_plaq)
        ratios.append(evals[-1] / target)
    return ratios

print("=" * 70)
print("ATTEMPT 2: PER-PLAQUETTE QUADRATIC FORM")
print("=" * 70)

for d in [2, 3, 4]:
    L = 2
    lat = Lattice(d, L)
    rng = np.random.default_rng(42)

    print(f"\n{'='*60}")
    print(f"d={d}, L={L}")
    print(f"{'='*60}")

    # Flat config
    Q_flat = flat_config(lat)
    ratios = per_plaquette_eigenvalue_ratio(lat, Q_flat)
    print(f"\nFlat (Q=I):")
    print(f"  Per-plaquette max_eval / (4*beta/N): max={max(ratios):.6f}, min={min(ratios):.6f}")
    print(f"  All <= 1? {all(r <= 1.001 for r in ratios)}")

    # Get actual eigenvalues of one plaquette Hessian
    H_plaq, edges = per_plaquette_hessian(lat, Q_flat, 0)
    evals = np.linalg.eigvalsh(H_plaq)
    print(f"  Plaquette 0 eigenvalues: {np.sort(evals)}")

    # Random configs
    all_max_ratios = []
    for trial in range(50):
        Q_rand = random_config(lat, rng)
        ratios = per_plaquette_eigenvalue_ratio(lat, Q_rand)
        all_max_ratios.append(max(ratios))

    print(f"\n50 random configs:")
    print(f"  Max of per-plaquette ratios: max={max(all_max_ratios):.4f}, mean={np.mean(all_max_ratios):.4f}")
    print(f"  All plaqs have max_eval <= 4*beta/N? {all(r <= 1.001 for r in all_max_ratios)}")

    if max(all_max_ratios) > 1.001:
        print(f"  *** PER-PLAQUETTE BOUND FAILS! Max ratio = {max(all_max_ratios):.4f} ***")

# More detailed analysis for d=4
print(f"\n{'='*60}")
print("DETAILED PER-PLAQUETTE ANALYSIS (d=4, L=2)")
print(f"{'='*60}")

lat4 = Lattice(4, 2)
Q_flat4 = flat_config(lat4)

# Eigenvalues of one plaquette's Hessian at flat
H_p0, edges0 = per_plaquette_hessian(lat4, Q_flat4, 0)
evals0 = np.linalg.eigvalsh(H_p0)
print(f"\nPlaquette 0 at flat (d=4):")
print(f"  Eigenvalues: {np.round(evals0, 6)}")
print(f"  Max eigenvalue: {evals0[-1]:.6f}")
print(f"  4*beta/N = {4*1.0/2:.6f}")

# What is the right per-plaquette bound?
# Let's try: h_plaq(v) <= C_plaq * sum_{e in plaq} |c_e|^2
# where C_plaq = max eigenvalue of H_plaq.
# Then summing: HessS(v,v) <= sum_plaq C_plaq * sum_{e in plaq} |c_e|^2
# At flat: C_plaq is the same for all plaquettes.
# Each edge appears in 2(d-1) plaquettes.
# So HessS(v,v) <= C_plaq * 2(d-1) * |v|^2
# For this to give 4d: C_plaq * 2(d-1) = 4d => C_plaq = 4d / (2(d-1)) = 2d/(d-1)

target_Cplaq = 2 * 4 / (4 - 1)  # for d=4
print(f"\nTarget C_plaq for d=4: 2d/(d-1) = {target_Cplaq:.4f}")
print(f"Actual max eigenvalue: {evals0[-1]:.4f}")
print(f"Ratio actual/target: {evals0[-1] / target_Cplaq:.4f}")

# Actually, let's count: each edge appears in 2(d-1) plaquettes, so
# sum_plaq sum_{e in plaq} |c_e|^2 = sum_e 2(d-1) |c_e|^2 = 2(d-1) |v|^2
# Need: max_plaq C_plaq * 2(d-1) <= 4d
# So: C_plaq <= 4d / (2(d-1)) = 2d/(d-1)

# For d=2: 2*2/1 = 4 = 4*beta/N (target per plaquette)
# For d=3: 2*3/2 = 3
# For d=4: 2*4/3 = 8/3 ≈ 2.667

print(f"\n--- Checking per-plaquette bound C_plaq <= 2d/(d-1) ---")
for d in [2, 3, 4]:
    L = 2
    lat = Lattice(d, L)
    target = 2 * d / (d - 1)

    Q_flat = flat_config(lat)
    H_p, _ = per_plaquette_hessian(lat, Q_flat, 0)
    evals = np.linalg.eigvalsh(H_p)

    print(f"\nd={d}: target C_plaq = 2d/(d-1) = {target:.4f}")
    print(f"  Flat plaquette max eigenvalue: {evals[-1]:.6f}")
    print(f"  Bound holds? {evals[-1] <= target + 0.001}")

    rng = np.random.default_rng(123)
    worst = 0
    for trial in range(50):
        Q_rand = random_config(lat, rng)
        for pidx in range(lat.nplaq):
            H_p, _ = per_plaquette_hessian(lat, Q_rand, pidx)
            ev = np.linalg.eigvalsh(H_p)
            worst = max(worst, ev[-1])

    print(f"  Worst across 50 random configs: {worst:.6f}")
    print(f"  Bound holds for random? {worst <= target + 0.001}")
