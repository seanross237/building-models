"""
Task 2: Per-vertex decomposition for GENERAL modes in the 9D eigenspace.

For a general mode w in P: w_{x,mu} = (-1)^{|x|} T_mu where T_mu is a 3-vector
(color direction that depends on lattice direction mu).

The constraint Sum_mu T_mu = 0 ensures w is in the eigenspace.

The per-vertex B-field for plaquette (x, mu, nu) is:
  B = S_{mu,nu} T_mu - T_{mu,nu} T_nu
where:
  S_{mu,nu} = I + R_mu D_{mu,nu}
  T_{mu,nu} = R_mu + R_mu D_{mu,nu} R_nu^T

(D_{mu,nu} is the combined cross-link D_{mu,nu} D_{nu,mu}^T)

The per-vertex contribution F_x(T) = Sum_{mu<nu} |B_{mu,nu}|^2 is a quadratic form
in the 12 entries of T (or 9 with constraint).

BUILD: the 12x12 per-vertex matrix M_12 and check its eigenvalue on the 9D constrained space.
"""

import numpy as np

np.random.seed(42)

d = 4

def random_so3():
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    w, x, y, z = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])

PLANES = [(mu, nu) for mu in range(d) for nu in range(mu+1, d)]

def compute_M12(R, D):
    """
    Build the 12x12 per-vertex matrix M_12 such that
    F_x = T_vec^T M_12 T_vec where T_vec = (T_0, T_1, T_2, T_3) in R^12.

    R = [R_0, R_1, R_2, R_3] - base link rotations
    D = {(mu,nu): D_{mu,nu}} - cross-link rotations
    """
    M12 = np.zeros((12, 12))

    for mu, nu in PLANES:
        S = np.eye(3) + R[mu] @ D[(mu,nu)]
        T = R[mu] + R[mu] @ D[(mu,nu)] @ R[nu].T

        # C is 3 x 12: C T_vec = S * T_mu - T * T_nu
        # C[:, 3*mu:3*(mu+1)] = S
        # C[:, 3*nu:3*(nu+1)] = -T

        # M12 += C^T C
        # Only nonzero blocks: (mu,mu), (nu,nu), (mu,nu), (nu,mu)
        M12[3*mu:3*(mu+1), 3*mu:3*(mu+1)] += S.T @ S
        M12[3*nu:3*(nu+1), 3*nu:3*(nu+1)] += T.T @ T
        M12[3*mu:3*(mu+1), 3*nu:3*(nu+1)] -= S.T @ T
        M12[3*nu:3*(nu+1), 3*mu:3*(mu+1)] -= T.T @ S

    return M12

def compute_M12_constrained_eigs(R, D):
    """
    Compute eigenvalues of M_12 restricted to the 9D space {T : Sum_mu T_mu = 0}.
    """
    M12 = compute_M12(R, D)

    # Projector onto constraint space
    # Constraint: Sum_mu T_mu = 0, i.e., (I_3 I_3 I_3 I_3) T_vec = 0
    # Build orthonormal basis for the 9D null space

    # The constraint kills 3D: T_3 = -(T_0 + T_1 + T_2)
    # Basis: T_mu = delta_{mu,i} e_a - delta_{mu,3} e_a for i=0,1,2 and a=0,1,2
    # That's 9 vectors

    V = np.zeros((12, 9))
    idx = 0
    for i in range(3):  # spatial directions 0,1,2 (3 is eliminated)
        for a in range(3):  # color directions
            v = np.zeros(12)
            v[3*i + a] = 1.0
            v[3*3 + a] = -1.0
            V[:, idx] = v
            idx += 1

    # Orthonormalize
    Q_orth, _ = np.linalg.qr(V)
    V_orth = Q_orth[:, :9]

    # Restricted matrix
    M_restricted = V_orth.T @ M12 @ V_orth
    eigs = np.linalg.eigvalsh(M_restricted)
    return eigs, M12

# ============================================================
# Part A: Check at Q=I
# ============================================================
print("=" * 70)
print("PART A: Per-vertex M_12 at Q=I")
print("=" * 70)

R_id = [np.eye(3)] * d
D_id = {p: np.eye(3) for p in PLANES}

eigs_id, M12_id = compute_M12_constrained_eigs(R_id, D_id)
print(f"Constrained eigenvalues at Q=I: {np.sort(eigs_id)}")
print(f"Max eigenvalue: {np.max(eigs_id):.6f} (should be 16)")

# Also check full 12x12 eigenvalues
eigs_full_id = np.linalg.eigvalsh(M12_id)
print(f"Full 12x12 eigenvalues at Q=I: {np.sort(eigs_full_id)}")

# ============================================================
# Part B: Random configs — check constrained max eigenvalue
# ============================================================
print("\n" + "=" * 70)
print("PART B: Max eigenvalue of constrained M_12 for random configs")
print("=" * 70)

N_tests = 10000
max_constrained = 0
max_unconstrained = 0

for trial in range(N_tests):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}

    eigs, M12 = compute_M12_constrained_eigs(R, D)
    max_constrained = max(max_constrained, eigs[-1])

    eigs_full = np.linalg.eigvalsh(M12)
    max_unconstrained = max(max_unconstrained, eigs_full[-1])

    if trial < 5:
        print(f"  Trial {trial}: constrained max = {eigs[-1]:.6f}, "
              f"unconstrained max = {eigs_full[-1]:.6f}")

    if eigs[-1] > 16 + 1e-10:
        print(f"  *** VIOLATION at trial {trial}: constrained max = {eigs[-1]:.6f} > 16!")

print(f"\nResults over {N_tests} random configs:")
print(f"  Max constrained eigenvalue: {max_constrained:.6f} (need <= 16)")
print(f"  Max unconstrained eigenvalue: {max_unconstrained:.6f}")
print(f"  Constrained bound holds: {max_constrained <= 16 + 1e-10}")

# ============================================================
# Part C: Adversarial gradient ascent on constrained max eigenvalue
# ============================================================
print("\n" + "=" * 70)
print("PART C: Adversarial gradient ascent on constrained max eigenvalue")
print("=" * 70)

def so3_exp(omega):
    angle = np.linalg.norm(omega)
    if angle < 1e-14:
        return np.eye(3)
    axis = omega / angle
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(angle)*K + (1-np.cos(angle))*(K @ K)

N_adversarial = 100
best_constrained = 0
best_unconstrained = 0
convergence_values = []

for trial in range(N_adversarial):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}

    step_size = 0.02
    for iteration in range(300):
        eigs, M12 = compute_M12_constrained_eigs(R, D)
        current = eigs[-1]

        eigs_full = np.linalg.eigvalsh(M12)

        # Gradient via finite differences
        eps = 1e-5

        # Gradient w.r.t. base links R
        grad_R = [np.zeros(3) for _ in range(d)]
        for mu in range(d):
            for k in range(3):
                omega = np.zeros(3); omega[k] = eps
                R_pert = R.copy()
                R_pert[mu] = so3_exp(omega) @ R[mu]
                eigs_pert, _ = compute_M12_constrained_eigs(R_pert, D)
                grad_R[mu][k] = (eigs_pert[-1] - current) / eps

        # Gradient w.r.t. cross links D
        grad_D = {p: np.zeros(3) for p in PLANES}
        for p in PLANES:
            for k in range(3):
                omega = np.zeros(3); omega[k] = eps
                D_pert = dict(D)
                D_pert[p] = so3_exp(omega) @ D[p]
                eigs_pert, _ = compute_M12_constrained_eigs(R, D_pert)
                grad_D[p][k] = (eigs_pert[-1] - current) / eps

        # Update
        for mu in range(d):
            R[mu] = so3_exp(step_size * grad_R[mu]) @ R[mu]
        for p in PLANES:
            D[p] = so3_exp(step_size * grad_D[p]) @ D[p]

        if iteration % 100 == 0:
            grad_norm = np.sqrt(sum(np.dot(g, g) for g in grad_R) +
                               sum(np.dot(g, g) for g in grad_D.values()))
            if trial < 5:
                print(f"  Trial {trial}, iter {iteration}: constrained_max = {current:.6f}, "
                      f"full_max = {eigs_full[-1]:.6f}, grad_norm = {grad_norm:.6f}")

        if iteration > 0 and iteration % 100 == 0:
            step_size *= 0.5

    final_constrained = eigs[-1]
    best_constrained = max(best_constrained, final_constrained)
    best_unconstrained = max(best_unconstrained, eigs_full[-1])
    convergence_values.append(final_constrained)

    if trial < 10 or final_constrained > 16 - 0.01:
        print(f"  Trial {trial} final: constrained = {final_constrained:.6f}, "
              f"full = {eigs_full[-1]:.6f}")

print(f"\nResults over {N_adversarial} adversarial trials:")
print(f"  Best constrained eigenvalue: {best_constrained:.6f} (need <= 16)")
print(f"  Best unconstrained eigenvalue: {best_unconstrained:.6f}")
print(f"  Mean convergence value: {np.mean(convergence_values):.6f}")
print(f"  Constrained bound holds: {best_constrained <= 16 + 1e-10}")

# ============================================================
# Part D: Check structure of maximizer — is it always uniform-color?
# ============================================================
print("\n" + "=" * 70)
print("PART D: Is the constrained maximizer always uniform-color?")
print("=" * 70)

# At the adversarial maximum, extract the top eigenvector T*
# Check if it's rank-1: T_mu = s_mu * n for some s, n

# Build constraint basis
V = np.zeros((12, 9))
idx = 0
for i in range(3):
    for a in range(3):
        v = np.zeros(12)
        v[3*i + a] = 1.0
        v[3*3 + a] = -1.0
        V[:, idx] = v
        idx += 1
Q_orth, _ = np.linalg.qr(V)
V_orth = Q_orth[:, :9]

rank1_fracs = []
for trial in range(50):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}

    # Adversarial ascent
    step_size = 0.02
    for iteration in range(300):
        eigs, M12 = compute_M12_constrained_eigs(R, D)
        current = eigs[-1]

        eps = 1e-5
        grad_R = [np.zeros(3) for _ in range(d)]
        for mu in range(d):
            for k in range(3):
                omega = np.zeros(3); omega[k] = eps
                R_pert = R.copy()
                R_pert[mu] = so3_exp(omega) @ R[mu]
                eigs_pert, _ = compute_M12_constrained_eigs(R_pert, D)
                grad_R[mu][k] = (eigs_pert[-1] - current) / eps

        grad_D = {p: np.zeros(3) for p in PLANES}
        for p in PLANES:
            for k in range(3):
                omega = np.zeros(3); omega[k] = eps
                D_pert = dict(D)
                D_pert[p] = so3_exp(omega) @ D[p]
                eigs_pert, _ = compute_M12_constrained_eigs(R, D_pert)
                grad_D[p][k] = (eigs_pert[-1] - current) / eps

        for mu in range(d):
            R[mu] = so3_exp(step_size * grad_R[mu]) @ R[mu]
        for p in PLANES:
            D[p] = so3_exp(step_size * grad_D[p]) @ D[p]

        if iteration > 0 and iteration % 100 == 0:
            step_size *= 0.5

    # Extract top eigenvector in 12D
    M_r = V_orth.T @ compute_M12(R, D) @ V_orth
    eigs_r, vecs_r = np.linalg.eigh(M_r)
    top_9d = vecs_r[:, -1]
    top_12d = V_orth @ top_9d

    # Reshape to 4x3 matrix T
    T = top_12d.reshape(4, 3)

    # Check rank: singular values of T
    sv = np.linalg.svd(T, compute_uv=False)
    rank1_frac = sv[0]**2 / np.sum(sv**2) if np.sum(sv**2) > 0 else 0
    rank1_fracs.append(rank1_frac)

    if trial < 10:
        print(f"  Trial {trial}: max_eig = {eigs_r[-1]:.6f}, "
              f"T singular values = [{sv[0]:.4f}, {sv[1]:.4f}, {sv[2]:.4f}], "
              f"rank-1 fraction = {rank1_frac:.4f}")

print(f"\nRank-1 fraction statistics:")
print(f"  Mean: {np.mean(rank1_fracs):.4f}")
print(f"  Min:  {np.min(rank1_fracs):.4f}")
print(f"  Max:  {np.max(rank1_fracs):.4f}")
print(f"  Always rank-1 (>0.99): {np.all(np.array(rank1_fracs) > 0.99)}")

# ============================================================
# Part E: Trace identity for general s
# ============================================================
print("\n" + "=" * 70)
print("PART E: Trace identity for general s (uniform-color modes)")
print("=" * 70)

# For uniform-color mode T_mu = s_mu n: F_x = n^T M_total(s) n
# Check: Tr(M_total(s)) = ? for various s perp (1,1,1,1)

def compute_M_total_s(R, D, s):
    """Per-vertex 3x3 matrix for spatial pattern s."""
    M = np.zeros((3, 3))
    for mu_idx, (mu, nu) in enumerate(PLANES):
        S = np.eye(3) + R[mu] @ D[(mu,nu)]
        T = R[mu] + R[mu] @ D[(mu,nu)] @ R[nu].T
        A = s[mu] * S - s[nu] * T
        M += A.T @ A
    return M

# Original staggered pattern
s_stag = np.array([1, -1, 1, -1], dtype=float)
# Alternative patterns perpendicular to (1,1,1,1)
s_alt1 = np.array([1, -1, 0, 0], dtype=float)
s_alt2 = np.array([1, 1, -2, 0], dtype=float)
s_alt3 = np.array([1, 1, 1, -3], dtype=float)
# Random unit vectors perp (1,1,1,1)
s_patterns = [s_stag, s_alt1, s_alt2, s_alt3]
s_names = ['staggered (1,-1,1,-1)', '(1,-1,0,0)', '(1,1,-2,0)', '(1,1,1,-3)']

for s, name in zip(s_patterns, s_names):
    traces = []
    max_eigs = []
    for _ in range(1000):
        R = [random_so3() for _ in range(d)]
        D = {p: random_so3() for p in PLANES}
        M = compute_M_total_s(R, D, s)
        traces.append(np.trace(M))
        max_eigs.append(np.linalg.eigvalsh(M)[-1])

    print(f"\n  s = {name}:")
    print(f"    |s|^2 = {np.dot(s, s):.1f}")
    print(f"    Tr(M_total(s)) range: [{min(traces):.4f}, {max(traces):.4f}]")
    print(f"    Tr/|s|^2 range: [{min(traces)/np.dot(s,s):.4f}, {max(traces)/np.dot(s,s):.4f}]")
    print(f"    Is Tr constant? {max(traces) - min(traces) < 0.01}")
    print(f"    max lambda_max(M_total): {max(max_eigs):.4f}")
    print(f"    max lambda_max / |s|^2: {max(max_eigs)/np.dot(s,s):.4f} (need <= 16)")

# ============================================================
# Part F: Is the per-vertex bound F_x / ||T||^2 <= 16 for general T?
# ============================================================
print("\n" + "=" * 70)
print("PART F: Direct check of F_x / ||T||^2 <= 16 for rank > 1 modes")
print("=" * 70)

max_ratio = 0
for trial in range(5000):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}

    # Random T with Sum_mu T_mu = 0
    T = np.random.randn(4, 3)
    T[3] = -(T[0] + T[1] + T[2])  # enforce constraint
    T_norm2 = np.sum(T**2)

    # Compute F_x
    F = 0
    for mu, nu in PLANES:
        S = np.eye(3) + R[mu] @ D[(mu,nu)]
        Tm = R[mu] + R[mu] @ D[(mu,nu)] @ R[nu].T
        B = S @ T[mu] - Tm @ T[nu]
        F += np.dot(B, B)

    ratio = F / T_norm2
    max_ratio = max(max_ratio, ratio)

    if trial < 5:
        print(f"  Trial {trial}: F_x = {F:.4f}, ||T||^2 = {T_norm2:.4f}, "
              f"ratio = {ratio:.4f}")

print(f"\nMax F_x / ||T||^2 over {5000} random trials: {max_ratio:.6f} (need <= 16)")
print(f"Bound holds: {max_ratio <= 16 + 1e-10}")

print("\nDone with Task 2.")
