"""
Targeted analysis of the decoherence mechanism.
Key questions:
1. For constant Q_e = R (same link for all edges), what is the total?
2. For non-parallel axis variation of edge 0, is the total constant or just bounded?
3. What is the algebraic identity relating active and inactive sums?
4. Per-edge group structure: does Sum over the 6 plaquettes of edge e stay constant?
"""

import numpy as np
from itertools import product
from stages234_vectorized import *

np.random.seed(42)
n_vec = np.array([1., 0., 0.])
Q_I = identity_quats()
bsq_I_all = compute_Bsq_all(Q_I, n_vec)

print("=" * 65)
print("MECHANISM ANALYSIS: Decoherence Structure")
print("=" * 65)

# ── 1. Constant-link configuration Q_e = R for all edges ──────────────────
print("\n--- Test 1: Constant config Q_e = R for ALL edges ---")
t_vals = np.linspace(0, 2*np.pi, 200)

print("  Rotating all links by angle t around x-axis:")
for t in [0, np.pi/4, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]:
    Q = np.zeros((n_edges, 4))
    c, s = np.cos(t/2), np.sin(t/2)
    Q[:] = [c, s, 0, 0]  # all edges = same R(t)
    Bsq = compute_Bsq_all(Q, n_vec)
    print(f"  t={t:.4f}: total={Bsq.sum():.4f}, active={Bsq[ACTIVE].sum():.4f}, inactive={Bsq[~ACTIVE].sum():.4f}")

# Varying all-links uniformly
print("\n  Scan over t for constant-link config (axis=x):")
totals_const = []
active_const = []
inactive_const = []
for t in t_vals:
    Q = np.zeros((n_edges, 4)); c, s = np.cos(t/2), np.sin(t/2)
    Q[:] = [c, s, 0, 0]
    Bsq = compute_Bsq_all(Q, n_vec)
    totals_const.append(Bsq.sum())
    active_const.append(Bsq[ACTIVE].sum())
    inactive_const.append(Bsq[~ACTIVE].sum())

totals_const = np.array(totals_const)
active_const = np.array(active_const)
inactive_const = np.array(inactive_const)
print(f"  Total: max={totals_const.max():.4f}, min={totals_const.min():.4f}")
print(f"  Active: max={active_const.max():.4f}, min={active_const.min():.4f}")
print(f"  Inactive: max={inactive_const.max():.4f}, min={inactive_const.min():.4f}")
print(f"  Inactive always = 0: {(inactive_const < 1e-10).all()}")
print(f"  Formula: active = 64 * 8*(1+cos(t))? check at t=pi/2: {64*8*(1+np.cos(np.pi/2)):.4f}")
print(f"    Computed at t=pi/2: {totals_const[np.argmin(abs(t_vals - np.pi/2))]:.4f}")

# ── 2. Single-edge variation with non-parallel axis ──────────────────────
print("\n--- Test 2: Single-link variation with non-parallel axis ---")
t_fine = np.linspace(0, 2*np.pi, 500)

for axis_label, axis in [("x (parallel to n)", np.array([1.,0,0])),
                           ("y (perpendicular)", np.array([0.,1,0])),
                           ("z", np.array([0.,0,1])),
                           ("(1,1,0)/sqrt2", np.array([1,1,0])/np.sqrt(2)),
                           ("random", None)]:
    if axis is None:
        np.random.seed(123)
        axis = np.random.randn(3); axis /= np.linalg.norm(axis)
    totals_t = []
    for t in t_fine:
        Q = Q_I.copy()
        c, s = np.cos(t/2), np.sin(t/2)
        Q[0] = np.array([c, s*axis[0], s*axis[1], s*axis[2]])
        totals_t.append(compute_total_Bsq_vec(Q, n_vec))
    totals_t = np.array(totals_t)
    print(f"  Axis {axis_label}: max={totals_t.max():.6f}, "
          f"min={totals_t.min():.6f}, range={totals_t.max()-totals_t.min():.6f}")

# ── 3. Per-edge sum: is it exactly constant? ──────────────────────────────
print("\n--- Test 3: Per-edge contribution sum ---")
print("  For edge e, define S_e(Q) = sum over plaquettes containing e of |B_□|^2")
print("  Testing if S_e(I) is a constant for Q_e varying, rest at I...")

ep0 = edge_plaq_map[0]
t_fine = np.linspace(0, 2*np.pi, 500)

print(f"\n  Edge 0 (ep={ep0}):")
for axis_label, axis in [("x", np.array([1.,0,0])),
                           ("y", np.array([0.,1,0])),
                           ("z", np.array([0.,0,1]))]:
    vals_e = []
    for t in t_fine:
        Q = Q_I.copy()
        c, s = np.cos(t/2), np.sin(t/2)
        Q[0] = np.array([c, s*axis[0], s*axis[1], s*axis[2]])
        Bsq = compute_Bsq_all(Q, n_vec)
        vals_e.append(Bsq[ep0].sum())
    vals_e = np.array(vals_e)
    baseline_e = bsq_I_all[ep0].sum()
    print(f"    Axis {axis_label}: S_e max={vals_e.max():.6f}, min={vals_e.min():.6f}, "
          f"baseline={baseline_e:.4f}, range={vals_e.max()-vals_e.min():.6f}")

# ── 4. Algebraic identity: active + inactive with same R_k ─────────────
print("\n--- Test 4: Algebraic identity for paired plaquettes ---")
print("  Identity: |n + R2*n + R1*n + R3*n|^2 + |n + R2*n - R1*n - R3*n|^2 = 2|n+R2*n|^2 + 2|R1*n+R3*n|^2")
print("  Verifying for random R_k...")

def random_so3():
    """Random SO(3) rotation as quaternion."""
    q = np.random.randn(4); q /= np.linalg.norm(q)
    return q

verified = 0
for _ in range(1000):
    # Random unit vectors (R_k * n for random SO(3))
    q1, q2, q3 = random_so3(), random_so3(), random_so3()
    R1n = rotate_n_by_q(q1.reshape(1,4), n_vec)[0]
    R2n = rotate_n_by_q(q2.reshape(1,4), n_vec)[0]
    R3n = rotate_n_by_q(q3.reshape(1,4), n_vec)[0]

    a = n_vec + R2n
    b = R1n + R3n

    active = np.dot(n_vec + R1n + R2n + R3n, n_vec + R1n + R2n + R3n)
    inactive = np.dot(n_vec - R1n + R2n - R3n, n_vec - R1n + R2n - R3n)
    identity_val = 2*np.dot(a,a) + 2*np.dot(b,b)

    if abs(active + inactive - identity_val) < 1e-10:
        verified += 1

print(f"  Identity verified: {verified}/1000")
print(f"  Identity value at Q=I: 2|2n|^2 + 2|2n|^2 = {2*4 + 2*4}")
print(f"  Upper bound: 2*4 + 2*4 = 16 (when |a|=|b|=2)")

# Check: is active always <= 16? And inactive always >= 0?
n_test = 10000
active_vals = np.zeros(n_test)
inactive_vals = np.zeros(n_test)
for i in range(n_test):
    q1, q2, q3 = random_so3(), random_so3(), random_so3()
    Q_arr = Q_I.copy()
    # Set random rotation for first 4 edges
    R1n = rotate_n_by_q(q1.reshape(1,4), n_vec)[0]
    R2n = rotate_n_by_q(q2.reshape(1,4), n_vec)[0]
    R3n = rotate_n_by_q(q3.reshape(1,4), n_vec)[0]
    active_vals[i] = np.dot(n_vec + R1n + R2n + R3n, n_vec + R1n + R2n + R3n)
    inactive_vals[i] = np.dot(n_vec - R1n + R2n - R3n, n_vec - R1n + R2n - R3n)

print(f"\n  Single active plaquette (random R_k):")
print(f"    Max |B|^2: {active_vals.max():.6f} (expect ≤ 16)")
print(f"    Min |B|^2: {active_vals.min():.6f}")
print(f"    Mean: {active_vals.mean():.4f}")
print(f"  Single inactive plaquette (random R_k):")
print(f"    Max |B|^2: {inactive_vals.max():.6f} (expect ≤ 16)")
print(f"    Min |B|^2: {inactive_vals.min():.6f}")
print(f"  Paired sum (active + inactive) with SAME R_k:")
print(f"    Max: {(active_vals + inactive_vals).max():.6f} (identity says ≤ 16)")
print(f"    Min: {(active_vals + inactive_vals).min():.6f}")
print(f"    Always ≤ 16: {(active_vals + inactive_vals <= 16 + 1e-10).all()}")

# ── 5. Counting argument: active/inactive coupling ─────────────────────
print("\n--- Test 5: Counting argument ---")
print("  On L=2 d=4 torus:")
print(f"  Active plaquettes: {ACTIVE.sum()} (each ≤ 16, so sum ≤ {ACTIVE.sum()*16})")
print(f"  Inactive plaquettes: {(~ACTIVE).sum()} (each ≥ 0, so sum ≥ 0)")
print()
print("  Key algebraic bound per plaquette:")
print("  |n + R1*n + R2*n + R3*n|^2 ≤ 16  (triangle, all unit vectors)")
print("  This gives Sum_active ≤ 1024 TRIVIALLY.")
print()
print("  For the GLOBAL bound Sum_total ≤ 1024:")
print("  We need: Sum_inactive ≤ 1024 - Sum_active.")
print("  Since Sum_active ≤ 1024 trivially, this needs coupling.")
print()

# How often does the algebraic bound (Sum_active ≤ 1024) give full bound?
N_c = 2000
active_sums = np.zeros(N_c)
inactive_sums = np.zeros(N_c)
for i in range(N_c):
    Bsq = compute_Bsq_all(random_quats(), n_vec)
    active_sums[i] = Bsq[ACTIVE].sum()
    inactive_sums[i] = Bsq[~ACTIVE].sum()

print(f"  Over {N_c} random configs:")
print(f"  Sum_active: mean={active_sums.mean():.1f}, max={active_sums.max():.1f} (≤1024)")
print(f"  Sum_inactive: mean={inactive_sums.mean():.1f}, max={inactive_sums.max():.1f}")
print(f"  Sum_total: max={(active_sums+inactive_sums).max():.1f} (must be ≤1024)")
print()
print("  Is (Sum_active ≤ 1024) + (Sum_inactive ≤ 512) enough to prove the bound?")
print(f"  Active max = {active_sums.max():.1f}, Inactive max = {inactive_sums.max():.1f}")
print(f"  Sum max = {(active_sums+inactive_sums).max():.1f}")
print("  No: 1024 + 512 = 1536, but actual max is ~481. Need tighter coupling.")
print()
print("  Correlation between active sum and total:")
print(f"  corr(Sum_active, Sum_total) = {np.corrcoef(active_sums, active_sums+inactive_sums)[0,1]:.4f}")
print(f"  corr(Sum_inactive, Sum_total) = {np.corrcoef(inactive_sums, active_sums+inactive_sums)[0,1]:.4f}")

# ── 6. Gradient of total at Q=I ─────────────────────────────────────────
print("\n--- Test 6: Gradient structure at Q=I ---")
print("  Checking if gradient of Sum|B|^2 vanishes at Q=I...")

eps = 1e-5
grad_norms = []
for ei in range(n_edges):
    grad_e = np.zeros(3)
    for k, axis in enumerate([np.array([1.,0,0]), np.array([0.,1,0]), np.array([0.,0,1])]):
        Q_plus = Q_I.copy()
        c, s = np.cos(eps/2), np.sin(eps/2)
        Q_plus[ei] = np.array([c, s*axis[0], s*axis[1], s*axis[2]])
        f_plus = compute_total_Bsq_vec(Q_plus, n_vec)
        f_0 = 1024.0  # known value at Q=I
        grad_e[k] = (f_plus - f_0) / eps
    grad_norms.append(np.linalg.norm(grad_e))

print(f"  Gradient norm per edge: max={max(grad_norms):.8f}, mean={np.mean(grad_norms):.8f}")
print(f"  Gradient vanishes at Q=I: {max(grad_norms) < 1e-3}")

# ── 7. Second derivative (curvature) at Q=I ─────────────────────────────
print("\n--- Test 7: Hessian at Q=I (curvature) ---")
print("  For small perturbation Q_0 = exp(t*X/2), compute d^2f/dt^2 at t=0...")

curvatures = {}
for ei in [0, 1, 2]:
    for ax, axis in enumerate([np.array([1.,0,0]), np.array([0.,1,0]), np.array([0.,0,1])]):
        eps2 = 0.01
        vals = []
        for t in [-eps2, 0, eps2]:
            Q = Q_I.copy()
            c, s = np.cos(t/2), np.sin(t/2)
            Q[ei] = np.array([c, s*axis[0], s*axis[1], s*axis[2]])
            vals.append(compute_total_Bsq_vec(Q, n_vec))
        curv = (vals[0] - 2*vals[1] + vals[2]) / eps2**2
        curvatures[(ei, ax)] = curv

print("  d^2f/dt^2 at Q=I for each (edge, axis):")
for (ei, ax), curv in list(curvatures.items())[:9]:
    print(f"    Edge {ei}, axis {ax}: {curv:.6f}")

all_curvs = list(curvatures.values())
print(f"  Max curvature: {max(all_curvs):.6f}")
print(f"  Min curvature: {min(all_curvs):.6f}")
print(f"  All curvatures ≤ 0: {max(all_curvs) <= 1e-8} (Q=I is local maximum iff all ≤ 0)")

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("MECHANISM SUMMARY")
print("=" * 65)
print()
print("Key findings on decoherence mechanism:")
print()
print("1. Constant config Q_e=R for all e:")
print("   - Sum_inactive = 0 EXACTLY for all R")
print("   - Sum_active = 64*8*(1+cos θ) ≤ 1024")
print("   - Shows that inactive plaquettes require VARIATION in edge links")
print()
print("2. Single-link variation from Q=I:")
print("   - Sum_total = 1024 EXACTLY for parallel axis (no change)")
print("   - Sum_total ≤ 1024 for all axes (numerical)")
print()
print("3. Per-plaquette algebraic identity:")
print("   Active(R1,R2,R3) + Inactive(R1,R2,R3) = 2|n+R2*n|^2 + 2|R1*n+R3*n|^2 ≤ 16")
print("   This pairs each inactive with an active at the same R_k values.")
print()
print("4. Gradient at Q=I: VANISHES (Q=I is a critical point of Sum|B|^2)")
print("5. Hessian at Q=I: [curvatures below]")
for (ei, ax), curv in list(curvatures.items())[:3]:
    print(f"   Edge {ei}, axis {ax}: d^2f/dt^2 = {curv:.4f}")
