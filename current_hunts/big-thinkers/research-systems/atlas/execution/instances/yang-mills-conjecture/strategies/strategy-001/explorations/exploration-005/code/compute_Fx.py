"""
Exploration 005: Cube-face inequality F_x <= 64 for general Q.

L=2, d=4 torus. SU(2) links in adjoint (SO(3)) representation.
Staggered mode: v_{x,mu} = (-1)^{|x|+mu} * n, n = (1,0,0).

B formula (SZZ conventions):
  B_{x,mu,nu}(Q,v) = v_{e1} + Ad(Q_{e1})(v_{e2})
                   - Ad(Q_{e1} Q_{e2} Q_{e3}^{-1})(v_{e3})
                   - Ad(U_sq)(v_{e4})

where for plaquette (x,mu,nu):
  e1 = (x, mu),          link = Q_{x,mu}
  e2 = (x+e_mu, nu),     link = Q_{x+e_mu, nu}
  e3 = (x+e_nu, mu),     link = Q_{x+e_nu, mu}   [backward edge]
  e4 = (x, nu),          link = Q_{x, nu}          [backward edge]
  U_sq = Q_{e1} Q_{e2} Q_{e3}^{-1} Q_{e4}^{-1}
"""

import numpy as np
from itertools import combinations

# ────────────────────────────────────────────────────────────────
# Lattice setup: L=2, d=4
# ────────────────────────────────────────────────────────────────
L = 2
d = 4
N_VERTICES = L**d   # 16
N_LINKS = d * L**d  # 64

def vertex_index(x):
    """Convert 4-tuple to integer index 0..15."""
    return x[0]*8 + x[1]*4 + x[2]*2 + x[3]

def index_to_vertex(idx):
    return ((idx >> 3) & 1, (idx >> 2) & 1, (idx >> 1) & 1, idx & 1)

def shift(x, mu, steps=1):
    """Shift vertex x by steps in direction mu (mod L=2)."""
    x = list(x)
    x[mu] = (x[mu] + steps) % L
    return tuple(x)

def edge_idx(x, mu):
    """Global index for edge (x, mu)."""
    return vertex_index(x) * d + mu

def staggered_sign(x, mu):
    """(-1)^{|x|+mu} where |x| = sum of coordinates."""
    parity = sum(x) + mu
    return 1 if parity % 2 == 0 else -1

# ────────────────────────────────────────────────────────────────
# SU(2) / SO(3) utilities
# ────────────────────────────────────────────────────────────────
def quat_to_rot(q):
    """Convert unit quaternion (w,x,y,z) to 3x3 rotation matrix."""
    w, x, y, z = q / np.linalg.norm(q)
    return np.array([
        [1-2*(y*y+z*z),   2*(x*y - w*z),   2*(x*z + w*y)],
        [2*(x*y + w*z),   1-2*(x*x+z*z),   2*(y*z - w*x)],
        [2*(x*z - w*y),   2*(y*z + w*x),   1-2*(x*x+y*y)]
    ])

def random_su2():
    """Haar-random SU(2) as SO(3) rotation matrix."""
    q = np.random.randn(4)
    return quat_to_rot(q / np.linalg.norm(q))

def identity_rot():
    return np.eye(3)

def rot_inv(R):
    return R.T  # SO(3): inverse = transpose

def rot_mult(R1, R2):
    return R1 @ R2

# ────────────────────────────────────────────────────────────────
# Link storage: Q[v_idx][mu] = 3x3 rotation matrix
# ────────────────────────────────────────────────────────────────
def identity_config():
    """All links = identity."""
    return [[identity_rot() for _ in range(d)] for _ in range(N_VERTICES)]

def random_config(seed=None):
    """All links Haar-random."""
    if seed is not None:
        np.random.seed(seed)
    return [[random_su2() for _ in range(d)] for _ in range(N_VERTICES)]

def get_link(Q, x, mu):
    """Get rotation matrix for link (x, mu)."""
    return Q[vertex_index(x)][mu]

# ────────────────────────────────────────────────────────────────
# B formula for plaquette (x, mu, nu)
# ────────────────────────────────────────────────────────────────
def compute_B(Q, x, mu, nu, n):
    """
    Compute B_{x,mu,nu}(Q, v_stag) as a 3-vector.

    Plaquette edges:
      e1 = (x, mu)
      e2 = (x+e_mu, nu)
      e3 = (x+e_nu, mu)   [traversed backward]
      e4 = (x, nu)         [traversed backward]

    B = v_{e1} + Ad(Q_{e1})(v_{e2}) - Ad(Q_{e1}Q_{e2}Q_{e3}^{-1})(v_{e3}) - Ad(U_sq)(v_{e4})
    """
    x_emu = shift(x, mu)
    x_enu = shift(x, nu)

    # Staggered values (3-vectors)
    v_e1 = staggered_sign(x,       mu) * n
    v_e2 = staggered_sign(x_emu,   nu) * n
    v_e3 = staggered_sign(x_enu,   mu) * n
    v_e4 = staggered_sign(x,       nu) * n

    # Link matrices
    R1  = get_link(Q, x,     mu)   # Q_{x,mu}
    R2  = get_link(Q, x_emu, nu)   # Q_{x+e_mu, nu}
    R3  = get_link(Q, x_enu, mu)   # Q_{x+e_nu, mu}
    R4  = get_link(Q, x,     nu)   # Q_{x, nu}

    # Partial holonomies
    # After e1:         R1
    # After e1,e2:      R1 R2
    # After e1,e2,e3^{-1}: R1 R2 R3^{-1}
    # After all 4:      R1 R2 R3^{-1} R4^{-1} = U_sq

    R1R2       = rot_mult(R1, R2)
    R1R2R3inv  = rot_mult(R1R2, rot_inv(R3))
    U_sq       = rot_mult(R1R2R3inv, rot_inv(R4))

    B = (v_e1
         + R1       @ v_e2
         - R1R2R3inv @ v_e3
         - U_sq     @ v_e4)
    return B

# ────────────────────────────────────────────────────────────────
# F_x = sum_{mu<nu} |B_{x,mu,nu}|^2
# ────────────────────────────────────────────────────────────────
def compute_Fx(Q, x, n=None):
    """Compute cube-face sum for vertex x."""
    if n is None:
        n = np.array([1.0, 0.0, 0.0])
    total = 0.0
    for mu, nu in combinations(range(d), 2):
        B = compute_B(Q, x, mu, nu, n)
        total += np.dot(B, B)
    return total

def compute_all_Fx(Q, n=None):
    """Compute F_x for all 16 vertices."""
    if n is None:
        n = np.array([1.0, 0.0, 0.0])
    results = {}
    for idx in range(N_VERTICES):
        x = index_to_vertex(idx)
        results[x] = compute_Fx(Q, x, n)
    return results

# ────────────────────────────────────────────────────────────────
# Stage 1 Tests
# ────────────────────────────────────────────────────────────────
def test_identity():
    """Test 1: F_x(I) = 64 for all 16 vertices."""
    print("=" * 60)
    print("TEST 1: F_x(I) for all vertices")
    print("=" * 60)
    Q = identity_config()
    results = compute_all_Fx(Q)
    all_64 = True
    for x, val in sorted(results.items()):
        ok = abs(val - 64.0) < 1e-10
        if not ok:
            all_64 = False
        print(f"  F_{x} = {val:.6f}  {'OK' if ok else 'FAIL'}")
    print(f"\n  All F_x = 64: {all_64}")
    return all_64

def test_random_configs(n_trials=50, seed=42):
    """Test 2: F_x <= 64 for random Q configs."""
    print("\n" + "=" * 60)
    print(f"TEST 2: F_x <= 64 for {n_trials} random configs (all 16 vertices each)")
    print("=" * 60)
    np.random.seed(seed)
    max_observed = 0.0
    violations = 0
    total_checks = 0
    for trial in range(n_trials):
        Q = random_config()
        for idx in range(N_VERTICES):
            x = index_to_vertex(idx)
            val = compute_Fx(Q, x)
            total_checks += 1
            if val > max_observed:
                max_observed = val
            if val > 64.0 + 1e-8:
                violations += 1
                print(f"  VIOLATION: trial={trial}, x={x}, F_x={val:.6f}")
    print(f"  Total checks: {total_checks}")
    print(f"  Violations (F_x > 64): {violations}")
    print(f"  Max F_x observed: {max_observed:.6f}")
    return violations == 0, max_observed

def test_single_link_perturbation():
    """Test 3: Single-link perturbation — which vertices achieve F_x=64?"""
    print("\n" + "=" * 60)
    print("TEST 3: Single-link perturbation Q_{e0} = exp(eps * tau_1)")
    print("=" * 60)

    # tau_1 = (-i/2) sigma_1, adjoint action = rotation about x-axis
    # exp(eps * tau_1) as SU(2): cos(eps/2) I + sin(eps/2) i sigma_1
    # Adjoint: rotation by eps about x-axis
    def rot_x(eps):
        c, s = np.cos(eps), np.sin(eps)
        return np.array([[1,0,0],[0,c,-s],[0,s,c]])

    # Perturb edge (x0=(0,0,0,0), mu=0)
    eps = 0.5
    x0 = (0,0,0,0)
    mu0 = 0
    Q = identity_config()
    Q[vertex_index(x0)][mu0] = rot_x(eps)

    print(f"  Perturbed edge: ({x0}, mu={mu0}), eps={eps}")
    print(f"  Rotation: Rx(eps={eps:.2f})")
    results = compute_all_Fx(Q)

    at_64 = []
    for x, val in sorted(results.items()):
        at_boundary = abs(val - 64.0) < 0.01
        print(f"  F_{x} = {val:.6f}  {'<- at 64!' if at_boundary else ''}")
        if at_boundary:
            at_64.append(x)

    print(f"\n  Vertices with F_x ~= 64: {at_64}")
    print(f"  Max F_x: {max(results.values()):.6f}")
    return results

def test_large_random(n_trials=1000, seed=0):
    """Test 4: Larger random test, report distribution."""
    print("\n" + "=" * 60)
    print(f"TEST 4: Large random test ({n_trials} configs)")
    print("=" * 60)
    np.random.seed(seed)
    all_vals = []
    violations = 0
    for trial in range(n_trials):
        Q = random_config()
        for idx in range(N_VERTICES):
            x = index_to_vertex(idx)
            val = compute_Fx(Q, x)
            all_vals.append(val)
            if val > 64.0 + 1e-8:
                violations += 1
    all_vals = np.array(all_vals)
    print(f"  Total vertex checks: {len(all_vals)}")
    print(f"  Violations: {violations}")
    print(f"  Max F_x: {all_vals.max():.6f}")
    print(f"  Mean F_x: {all_vals.mean():.6f}")
    print(f"  Std F_x: {all_vals.std():.6f}")
    print(f"  Percentiles [50,75,90,95,99,99.9]: "
          f"{np.percentile(all_vals, [50,75,90,95,99,99.9])}")
    return violations == 0, all_vals.max()


if __name__ == "__main__":
    # Run all stage 1 tests
    ok1 = test_identity()
    ok2, max2 = test_random_configs(n_trials=50)
    results3 = test_single_link_perturbation()
    ok4, max4 = test_large_random(n_trials=1000)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  F_x(I) = 64 for all vertices: {ok1}")
    print(f"  No violations in 50 random configs: {ok2}")
    print(f"  Max observed (50 configs): {max2:.6f}")
    print(f"  No violations in 1000 random configs: {ok4}")
    print(f"  Max observed (1000 configs): {max4:.6f}")
