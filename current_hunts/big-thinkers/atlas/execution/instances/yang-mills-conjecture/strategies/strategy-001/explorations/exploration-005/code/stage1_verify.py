"""
Stage 1: Implement F_x(Q) on L=2, d=4 torus and verify basic properties.

Lattice: (Z/2Z)^4, 16 vertices, 64 edges, 96 plaquettes.
Staggered mode: v_{x,mu} = (-1)^{|x|+mu} * n, n = (1,0,0).

B_sq formula (SZZ conventions):
  B = v_{e1} + Ad(Q_{e1})(v_{e2}) - Ad(Q_{e1}Q_{e2}Q_{e3}^{-1})(v_{e3}) - Ad(U_sq)(v_{e4})

where U_sq = Q_{e1}Q_{e2}Q_{e3}^{-1}Q_{e4}^{-1}.
"""

import numpy as np
from itertools import product as iproduct

np.random.seed(42)

# ============================================================
# Quaternion / SO(3) utilities
# ============================================================

def random_su2(size=None):
    """Random SU(2) element(s) as unit quaternion (w,x,y,z)."""
    if size is None:
        q = np.random.randn(4)
        q /= np.linalg.norm(q)
        return q
    qs = np.random.randn(size, 4)
    qs /= np.linalg.norm(qs, axis=1, keepdims=True)
    return qs

def quat_to_so3(q):
    """Unit quaternion -> 3x3 SO(3) matrix."""
    w, x, y, z = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])

def quat_mult(q1, q2):
    """Hamilton product."""
    w1,x1,y1,z1 = q1
    w2,x2,y2,z2 = q2
    return np.array([
        w1*w2-x1*x2-y1*y2-z1*z2,
        w1*x2+x1*w2+y1*z2-z1*y2,
        w1*y2-x1*z2+y1*w2+z1*x2,
        w1*z2+x1*y2-y1*x2+z1*w2
    ])

def quat_inv(q):
    """Inverse of unit quaternion (= conjugate)."""
    return np.array([q[0], -q[1], -q[2], -q[3]])

# ============================================================
# Lattice setup: L=2, d=4
# ============================================================

d = 4
L = 2
vertices = list(iproduct(range(L), repeat=d))  # 16 vertices
vtx_idx = {v: i for i, v in enumerate(vertices)}

def neighbor(x, mu):
    """x + e_mu on (Z/2Z)^4."""
    xl = list(x)
    xl[mu] = (xl[mu] + 1) % L
    return tuple(xl)

def sum_coords(x):
    return sum(x)

# ============================================================
# Configuration management
# ============================================================

def identity_config():
    """All links = identity SU(2)."""
    config = np.zeros((16, 4, 4))
    config[:, :, 0] = 1.0
    return config

def random_config():
    """Haar-random SU(2) on all 64 links."""
    config = np.zeros((16, 4, 4))
    for i in range(16):
        for mu in range(4):
            config[i, mu] = random_su2()
    return config

def single_link_config(x, mu, epsilon):
    """Identity except edge (x, mu) = exp(epsilon * tau_1)."""
    config = identity_config()
    # exp(epsilon * i*sigma_1/2) as quaternion: (cos(eps/2), sin(eps/2), 0, 0)
    config[vtx_idx[x], mu] = np.array([np.cos(epsilon/2), np.sin(epsilon/2), 0, 0])
    return config

# ============================================================
# B_plaquette computation
# ============================================================

def compute_B(config, x, mu, nu, n):
    """
    Compute B for plaquette (x, mu, nu).

    Edges:
      e1 = (x, mu) forward
      e2 = (x+e_mu, nu) forward
      e3 = (x+e_nu, mu) backward (=> Q_{e3}^{-1})
      e4 = (x, nu) backward (=> Q_{e4}^{-1})

    B = v_{e1} + Ad(Q_{e1}) v_{e2} - Ad(Q_{e1}Q_{e2}Q_{e3}^{-1}) v_{e3} - Ad(U_sq) v_{e4}
    """
    sx = sum_coords(x)

    # Staggered signs for each edge's v component
    s1 = (-1)**(sx + mu)           # v_{(x, mu)}
    s2 = (-1)**(sx + 1 + nu)       # v_{(x+e_mu, nu)}
    s3 = (-1)**(sx + 1 + mu)       # v_{(x+e_nu, mu)}
    s4 = (-1)**(sx + nu)           # v_{(x, nu)}

    # Get quaternions
    xi = vtx_idx[x]
    q1 = config[xi, mu]

    x_mu = neighbor(x, mu)
    q2 = config[vtx_idx[x_mu], nu]

    x_nu = neighbor(x, nu)
    q3 = config[vtx_idx[x_nu], mu]

    q4 = config[xi, nu]

    # Partial holonomies (as SO(3) matrices)
    R1 = quat_to_so3(q1)

    q12 = quat_mult(q1, q2)
    q123inv = quat_mult(q12, quat_inv(q3))
    R2 = quat_to_so3(q123inv)

    Usq = quat_mult(q123inv, quat_inv(q4))
    R3 = quat_to_so3(Usq)

    # B = s1*n + s2*R1*n - s3*R2*n - s4*R3*n
    B = s1 * n + s2 * (R1 @ n) - s3 * (R2 @ n) - s4 * (R3 @ n)

    return B

def compute_Fx(config, x, n):
    """F_x = sum_{mu<nu} |B_{(x,mu,nu)}|^2"""
    Fx = 0.0
    for mu in range(d):
        for nu in range(mu+1, d):
            B = compute_B(config, x, mu, nu, n)
            Fx += np.dot(B, B)
    return Fx

def compute_all_Fx(config, n):
    """Compute F_x for all 16 vertices."""
    return {x: compute_Fx(config, x, n) for x in vertices}

# ============================================================
# Stage 1 Tests
# ============================================================

n = np.array([1.0, 0.0, 0.0])

print("=" * 70)
print("STAGE 1.2: Verify F_x(I) = 64 for all 16 vertices")
print("=" * 70)

config_I = identity_config()
Fx_I = compute_all_Fx(config_I, n)

print(f"{'Vertex':<20} {'F_x':>12} {'Error from 64':>15}")
print("-" * 50)
max_err = 0.0
for x in vertices:
    err = abs(Fx_I[x] - 64.0)
    max_err = max(max_err, err)
    print(f"{str(x):<20} {Fx_I[x]:>12.6f} {err:>15.2e}")
print(f"\nMax error from 64: {max_err:.2e}")
print(f"RESULT: {'PASS' if max_err < 1e-10 else 'FAIL'}")

# Also check total sum
total = sum(Fx_I.values())
print(f"\nTotal sum over all vertices: {total:.6f} (expected 1024)")
print(f"Error: {abs(total - 1024):.2e}")

print("\n" + "=" * 70)
print("STAGE 1.3: Random Q tests (10 configs, all 16 vertices)")
print("=" * 70)

max_Fx_all = 0.0
violations = 0
n_configs = 10

for trial in range(n_configs):
    config = random_config()
    Fx_vals = compute_all_Fx(config, n)
    max_Fx = max(Fx_vals.values())
    max_Fx_all = max(max_Fx_all, max_Fx)

    # Check for violations
    for x, val in Fx_vals.items():
        if val > 64.0 + 1e-10:
            violations += 1
            print(f"  VIOLATION: trial={trial}, vertex={x}, F_x={val:.6f}")

    total = sum(Fx_vals.values())
    print(f"  Trial {trial:2d}: max F_x = {max_Fx:8.4f}, total = {total:8.4f}")

print(f"\nMax F_x over all trials: {max_Fx_all:.6f}")
print(f"Violations: {violations}")
print(f"RESULT: {'PASS' if violations == 0 else 'FAIL'}")

print("\n" + "=" * 70)
print("STAGE 1.4: Single-link perturbation Q_{(0,0)} = exp(eps*tau_1)")
print("=" * 70)

x0 = (0,0,0,0)
for eps in [0.01, 0.1, 0.5, 1.0, np.pi/2, np.pi]:
    config = single_link_config(x0, 0, eps)
    print(f"\n  epsilon = {eps:.4f}:")
    Fx_vals = compute_all_Fx(config, n)
    for x in vertices:
        Fx_val = Fx_vals[x]
        if abs(Fx_val - 64.0) < 0.01:
            print(f"    vertex {x}: F_x = {Fx_val:.6f}  <-- near 64")
        elif Fx_val > 63.0:
            print(f"    vertex {x}: F_x = {Fx_val:.6f}  <-- high")
    max_v = max(Fx_vals.values())
    print(f"    Max F_x = {max_v:.6f}")

print("\n" + "=" * 70)
print("STAGE 1.5: Larger random test (1000 configs)")
print("=" * 70)

max_Fx_large = 0.0
violations_large = 0

for trial in range(1000):
    config = random_config()
    Fx_vals = compute_all_Fx(config, n)
    for x, val in Fx_vals.items():
        if val > max_Fx_large:
            max_Fx_large = val
        if val > 64.0 + 1e-10:
            violations_large += 1

print(f"Max F_x over 1000 trials x 16 vertices = 16000 tests: {max_Fx_large:.6f}")
print(f"Violations: {violations_large}")
print(f"RESULT: {'PASS' if violations_large == 0 else 'FAIL'}")

# Also test with different n vectors
print("\n" + "=" * 70)
print("STAGE 1.6: Different n vectors (100 configs each)")
print("=" * 70)

for n_test in [np.array([0,1,0.]), np.array([0,0,1.]), np.array([1,1,0.])/np.sqrt(2),
               np.array([1,1,1.])/np.sqrt(3)]:
    max_val = 0.0
    for _ in range(100):
        config = random_config()
        for x in vertices:
            val = compute_Fx(config, x, n_test)
            max_val = max(max_val, val)
    nn = np.dot(n_test, n_test)
    print(f"  n = {n_test}, |n|^2 = {nn:.4f}: max F_x = {max_val:.6f}, max F_x/|n|^2 = {max_val/nn:.6f}")

print("\nDone with Stage 1.")
