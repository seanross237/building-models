"""
Stage 2: Investigate the ratio f_sq / Sum(1-cos theta_sq) for various configs.
Single-edge gives -13/3 exactly. Does this generalize?
"""

import numpy as np
from itertools import product

# =====================================================
# SU(2) utilities (same as before)
# =====================================================

def quat_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ])

def quat_inv(q):
    return np.array([q[0], -q[1], -q[2], -q[3]])

def quat_to_rot(q):
    q = q / np.linalg.norm(q)
    w, x, y, z = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])

def random_quat():
    q = np.random.randn(4)
    return q / np.linalg.norm(q)

# =====================================================
# Lattice setup
# =====================================================

L = 2
d = 4
coords = list(product(range(L), repeat=d))

def add_mod(x, mu):
    y = list(x)
    y[mu] = (y[mu] + 1) % L
    return tuple(y)

def staggered_sign(x, mu):
    return (-1) ** (sum(x) + mu)

def edge_index(x, mu):
    idx = 0
    for i in range(d):
        idx = idx * L + x[i]
    return idx * d + mu

plaquettes = []
for x in coords:
    for mu in range(d):
        for nu in range(mu+1, d):
            e1 = (x, mu)
            e2 = (add_mod(x, mu), nu)
            e3 = (add_mod(x, nu), mu)
            e4 = (x, nu)

            s1 = staggered_sign(*e1)
            s2 = staggered_sign(*e2)
            s3 = staggered_sign(*e3)
            s4 = staggered_sign(*e4)

            eff = (s1, s2, -s3, -s4)
            active = (mu + nu) % 2 == 1

            plaquettes.append({
                'x': x, 'mu': mu, 'nu': nu,
                'e1_idx': edge_index(*e1), 'e2_idx': edge_index(*e2),
                'e3_idx': edge_index(*e3), 'e4_idx': edge_index(*e4),
                'eff': eff, 'active': active
            })

def compute_fsq_and_wilson(Q, n):
    """Compute f_sq = Sum |B_sq|^2 - 1024 and Wilson = Sum(1-cos theta)."""
    total_bsq = 0.0
    total_wilson = 0.0
    for p in plaquettes:
        q1 = Q[p['e1_idx']]
        q2 = Q[p['e2_idx']]
        q3 = Q[p['e3_idx']]
        q4 = Q[p['e4_idx']]

        R1 = quat_to_rot(q1)
        partial = quat_mult(quat_mult(q1, q2), quat_inv(q3))
        R2 = quat_to_rot(partial)
        usq = quat_mult(partial, quat_inv(q4))
        R3 = quat_to_rot(usq)

        c1, c2, c3, c4 = p['eff']
        B = c1 * n + c2 * (R1 @ n) + c3 * (R2 @ n) + c4 * (R3 @ n)
        total_bsq += np.dot(B, B)

        # Wilson: 1 - cos(theta_sq) where cos(theta) = 2*usq[0]^2 - 1 for adjoint
        cos_theta = 2*usq[0]**2 - 1
        total_wilson += (1 - cos_theta)

    fsq = total_bsq - 1024.0
    return fsq, total_wilson

n = np.array([0., 0., 1.])

# =====================================================
# Test: random configs
# =====================================================

print("=" * 70)
print("RATIO f_sq / Sum(1-cos theta) for random configs")
print("=" * 70)

np.random.seed(42)
ratios = []
print(f"\n{'Trial':<8} {'f_sq':<14} {'Wilson':<14} {'Ratio':<14}")
for trial in range(50):
    Q = {i: random_quat() for i in range(64)}
    fsq, wilson = compute_fsq_and_wilson(Q, n)
    ratio = fsq / wilson if abs(wilson) > 1e-10 else float('nan')
    ratios.append(ratio)
    if trial < 30:
        print(f"{trial:<8} {fsq:<14.6f} {wilson:<14.6f} {ratio:<14.6f}")

ratios = np.array(ratios)
print(f"\nRatio statistics:")
print(f"  Mean:   {np.mean(ratios):.6f}")
print(f"  Std:    {np.std(ratios):.6f}")
print(f"  Min:    {np.min(ratios):.6f}")
print(f"  Max:    {np.max(ratios):.6f}")
print(f"  -13/3 = {-13/3:.6f}")

# =====================================================
# Test: configs near Q=I (small perturbations)
# =====================================================

print("\n" + "=" * 70)
print("SMALL PERTURBATIONS from Q=I")
print("=" * 70)

for eps in [0.01, 0.05, 0.1, 0.3, 0.5]:
    ratios_eps = []
    for trial in range(100):
        Q = {}
        for i in range(64):
            # Small random perturbation
            axis = np.random.randn(3)
            axis = axis / np.linalg.norm(axis)
            angle = np.random.exponential(eps)
            q = np.array([np.cos(angle/2), *(np.sin(angle/2) * axis)])
            Q[i] = q / np.linalg.norm(q)
        fsq, wilson = compute_fsq_and_wilson(Q, n)
        if abs(wilson) > 1e-10:
            ratios_eps.append(fsq / wilson)
    r = np.array(ratios_eps)
    print(f"  eps={eps:.2f}: ratio = {np.mean(r):.6f} ± {np.std(r):.6f} (n={len(r)}, -13/3={-13/3:.6f})")

# =====================================================
# Test: abelian configs (all quaternions in same U(1))
# =====================================================

print("\n" + "=" * 70)
print("ABELIAN CONFIGS (all q in same U(1) subgroup)")
print("=" * 70)

for trial in range(20):
    Q = {}
    for i in range(64):
        angle = np.random.uniform(0, 2*np.pi)
        Q[i] = np.array([np.cos(angle/2), np.sin(angle/2), 0., 0.])
    fsq, wilson = compute_fsq_and_wilson(Q, n)
    ratio = fsq / wilson if abs(wilson) > 1e-10 else float('nan')
    if trial < 10:
        print(f"  Trial {trial}: f_sq={fsq:.6f}, Wilson={wilson:.6f}, ratio={ratio:.6f}")

# =====================================================
# Multi-edge perturbation: 2 edges
# =====================================================

print("\n" + "=" * 70)
print("TWO-EDGE PERTURBATION from Q=I")
print("=" * 70)

for edge1, edge2 in [(0, 1), (0, 4), (0, 8), (0, 32), (0, 63)]:
    for angle1, angle2 in [(1.0, 1.0), (0.5, 1.5), (np.pi, np.pi)]:
        Q = {i: np.array([1., 0., 0., 0.]) for i in range(64)}
        Q[edge1] = np.array([np.cos(angle1/2), np.sin(angle1/2), 0., 0.])
        Q[edge2] = np.array([np.cos(angle2/2), np.sin(angle2/2), 0., 0.])
        fsq, wilson = compute_fsq_and_wilson(Q, n)
        ratio = fsq / wilson if abs(wilson) > 1e-10 else float('nan')
        print(f"  edges ({edge1},{edge2}), angles ({angle1:.2f},{angle2:.2f}): ratio={ratio:.6f}")

# =====================================================
# Multi-edge: all edges perturbed by same angle (same axis)
# =====================================================

print("\n" + "=" * 70)
print("ALL EDGES SAME PERTURBATION")
print("=" * 70)

for angle in [0.01, 0.1, 0.3, 0.5, 1.0, np.pi/2, np.pi]:
    Q = {}
    for i in range(64):
        Q[i] = np.array([np.cos(angle/2), np.sin(angle/2), 0., 0.])
    fsq, wilson = compute_fsq_and_wilson(Q, n)
    ratio = fsq / wilson if abs(wilson) > 1e-10 else float('nan')
    print(f"  angle={angle:.4f}: f_sq={fsq:.6f}, Wilson={wilson:.6f}, ratio={ratio:.6f}")

# =====================================================
# Try different n directions
# =====================================================

print("\n" + "=" * 70)
print("DIFFERENT n DIRECTIONS for random configs")
print("=" * 70)

np.random.seed(999)
for n_dir in [np.array([1,0,0.]), np.array([0,1,0.]), np.array([0,0,1.]),
              np.array([1,1,0.])/np.sqrt(2), np.array([1,1,1.])/np.sqrt(3)]:
    ratios_n = []
    for trial in range(100):
        Q = {i: random_quat() for i in range(64)}
        fsq, wilson = compute_fsq_and_wilson(Q, n_dir)
        if abs(wilson) > 1e-10:
            ratios_n.append(fsq / wilson)
    r = np.array(ratios_n)
    print(f"  n = {n_dir}: ratio = {np.mean(r):.6f} ± {np.std(r):.6f}")

# =====================================================
# Scan for the WORST (least negative) ratio
# =====================================================

print("\n" + "=" * 70)
print("SEARCH FOR WORST RATIO (closest to 0)")
print("=" * 70)

np.random.seed(2024)
worst_ratio = -np.inf
best_config_info = None

for trial in range(5000):
    Q = {i: random_quat() for i in range(64)}
    fsq, wilson = compute_fsq_and_wilson(Q, n)
    if abs(wilson) > 1e-10:
        ratio = fsq / wilson
        if ratio > worst_ratio:
            worst_ratio = ratio
            best_config_info = (fsq, wilson, ratio, trial)

print(f"  Worst ratio over 5000 trials: {worst_ratio:.6f}")
print(f"  At trial {best_config_info[3]}: f_sq={best_config_info[0]:.6f}, Wilson={best_config_info[1]:.6f}")
print(f"  -13/3 = {-13/3:.6f}")

# Check: is the ratio always MORE negative than -13/3?
# If so, the single-edge is the worst case, and the bound f_sq <= -(13/3)*Wilson holds.
# Wilson ≥ 0 always, so this would give f_sq ≤ 0, proving the conjecture!
