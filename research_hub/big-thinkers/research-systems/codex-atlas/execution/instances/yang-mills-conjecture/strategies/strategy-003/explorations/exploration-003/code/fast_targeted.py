"""Fast targeted computation: just the essential numbers."""
import numpy as np
import sys, time
sys.path.insert(0, '.')
from hessian_core import *

t0 = time.time()

def su2_exp(w_vec):
    theta = np.linalg.norm(w_vec)
    if theta < 1e-12:
        return np.eye(2, dtype=complex)
    w = sum(w_vec[a] * isigma[a] for a in range(3))
    return np.cos(theta) * np.eye(2, dtype=complex) + (np.sin(theta)/theta) * w

# Use d=2 for fast tests, then d=3, d=4
for d in [2, 3, 4]:
    L = 2
    lat = Lattice(d, L)
    rng = np.random.default_rng(42)
    n_cfg = 500 if d <= 3 else 200

    lmins, lmaxs = [], []
    D_maxs, C_lmaxs, C_norms_list = [], [], []

    for trial in range(n_cfg):
        Q = random_config(lat, rng)
        H = compute_hessian(lat, Q)
        ev = np.linalg.eigvalsh(H)
        lmins.append(ev[0])
        lmaxs.append(ev[-1])

        D_diag = np.diag(H)
        D = np.diag(D_diag)
        C = H - D
        C_ev = np.linalg.eigvalsh(C)
        D_maxs.append(np.max(D_diag))
        C_lmaxs.append(C_ev[-1])
        C_norms_list.append(max(abs(C_ev[0]), abs(C_ev[-1])))

    print(f"\nd={d} L={L} ({n_cfg} configs, {time.time()-t0:.1f}s elapsed):")
    print(f"  lambda_max: max={max(lmaxs):.4f} (4d={4*d}), ratio={max(lmaxs)/(4*d):.4f}")
    print(f"  lambda_min: min={min(lmins):.4f}, |ratio|={abs(min(lmins))/(4*d):.4f}")
    print(f"  max D: {max(D_maxs):.4f} <= {2*(d-1)} (flat)")
    print(f"  max C_lmax: {max(C_lmaxs):.4f} <= {2*(d+1)} (flat)")
    print(f"  max ||C||: {max(C_norms_list):.4f} <= {2*(d+1)} (flat)")

    # Per-config D+C bound
    sums = [D_maxs[i] + C_lmaxs[i] for i in range(n_cfg)]
    print(f"  max(D+C_lmax): {max(sums):.4f} <= 4d={4*d}? {max(sums) <= 4*d + 0.01}")

    # Spectral radius
    print(f"  Spectral radius max: {max(max(lmaxs), abs(min(lmins))):.4f}")

# Perturbation from flat
print(f"\n{'='*60}")
print("PERTURBATION FROM FLAT (d=4)")
print(f"{'='*60}")
d, L = 4, 2
lat = Lattice(d, L)
ne = lat.nedges
rng = np.random.default_rng(999)

for eps in [0.0, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0]:
    best_lmax = -999
    worst_lmin = 999
    for trial in range(50):
        w = rng.normal(size=(ne, 3))
        Q = [su2_exp(eps * w[e]) for e in range(ne)]
        H = compute_hessian(lat, Q)
        ev = np.linalg.eigvalsh(H)
        best_lmax = max(best_lmax, ev[-1])
        worst_lmin = min(worst_lmin, ev[0])
    print(f"  eps={eps:.2f}: lmax={best_lmax:.4f} ({best_lmax/(4*d):.3f}×4d), lmin={worst_lmin:.4f}")

# Cross-term kernel norms
print(f"\n{'='*60}")
print("CROSS-TERM KERNEL ||F||_op")
print(f"{'='*60}")
rng = np.random.default_rng(77)
norms = []
for trial in range(20000):
    M = random_su2(rng)
    N = random_su2(rng)
    F = np.zeros((3, 3))
    for a in range(3):
        for b in range(3):
            F[a, b] = np.real(np.trace(isigma[a] @ M @ isigma[b] @ N))
    norms.append(np.linalg.norm(F, ord=2))

print(f"20000 random: min={min(norms):.6f}, max={max(norms):.6f}, mean={np.mean(norms):.6f}")
print(f"Is ||F|| always = 2? {abs(max(norms) - 2.0) < 0.001 and abs(min(norms) - 2.0) < 0.5}")
print(f"Bound ||F|| <= 2: {max(norms) <= 2.001}")

# Mass gap table
print(f"\n{'='*60}")
print("MASS GAP THRESHOLD SUMMARY")
print(f"{'='*60}")
print("(All in our convention: S=-(β/N)ΣReTr, β=β_ours)")
print("Bakry-Émery: K = N/2 + λ_min(H)/(|v|²_SZZ/|c|²) = 1 + λ_min(H)/2 for SU(2)")
print("Mass gap iff K > 0 iff λ_min(H) > -2 for all Q")
print("Since H ∝ β: need β × |λ_min(H,β=1)/β| < 2")
print()
for d in [2, 3, 4]:
    lat = Lattice(d, L)
    Q = flat_config(lat)
    H = compute_hessian(lat, Q)
    gersh = max(H[i,i] + sum(abs(H[i,j]) for j in range(H.shape[0]) if j!=i) for i in range(H.shape[0]))
    print(f"d={d}: SZZ(Gershgorin)={gersh:.0f} → β<2/{gersh:.0f}={2/gersh:.4f}; " +
          f"Our(4d)={4*d} → β<2/{4*d}={2/(4*d):.4f}; Ratio={gersh/(4*d):.1f}x")

print(f"\nTotal time: {time.time()-t0:.1f}s")
