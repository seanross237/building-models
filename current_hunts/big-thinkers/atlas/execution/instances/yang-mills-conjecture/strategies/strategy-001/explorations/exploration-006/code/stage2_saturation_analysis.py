"""
Stage 2: Deep analysis of the saturation manifold and algebraic structure.

Key question: WHY is lambda_max <= 64? What algebraic identity forces this?

Key finding from Stage 1: At all maxima, R_mu n = n for all mu, and the
per-plaquette contributions are: active=16, inactive=0.

Strategy:
1. Verify the cross-link condition (D n = n) at maxima
2. Prove that when ALL rotations fix n, F_x(n) = 64
3. Prove that when some rotation doesn't fix n, F_x(n) < 64

The proof approach: Decompose M_total into cross-term structure and show
the maximum eigenvalue is bounded by the structure of shared rotations.
"""

import numpy as np

np.random.seed(42)

# ============================================================
# SO(3) utilities (same as Stage 1)
# ============================================================

def random_so3():
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    w, x, y, z = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])

def so3_exp(omega):
    angle = np.linalg.norm(omega)
    if angle < 1e-14:
        return np.eye(3)
    axis = omega / angle
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(angle)*K + (1-np.cos(angle))*(K @ K)

def so3_log(R):
    tr = np.clip((np.trace(R) - 1) / 2, -1, 1)
    angle = np.arccos(tr)
    if angle < 1e-10:
        return np.zeros(3)
    axis = np.array([R[2,1]-R[1,2], R[0,2]-R[2,0], R[1,0]-R[0,1]]) / (2*np.sin(angle))
    return angle * axis

def rotation_angle(R):
    """Get the rotation angle of R in SO(3)."""
    tr = np.clip((np.trace(R) - 1) / 2, -1, 1)
    return np.arccos(tr)

def rotation_axis(R):
    """Get the rotation axis of R."""
    angle = rotation_angle(R)
    if angle < 1e-10:
        return np.array([0, 0, 1])  # arbitrary for identity
    axis = np.array([R[2,1]-R[1,2], R[0,2]-R[2,0], R[1,0]-R[0,1]]) / (2*np.sin(angle))
    return axis / np.linalg.norm(axis)

PLANES = [(mu, nu) for mu in range(4) for nu in range(mu+1, 4)]

def compute_A(mu, nu, R, D):
    a = (-1)**mu
    b = (-1)**(nu+1)
    S = np.eye(3) + R[mu] @ D[(mu,nu)]
    T = R[mu] + R[mu] @ D[(mu,nu)] @ R[nu].T
    return a * S + b * T

def compute_M_total(R, D):
    M = np.zeros((3, 3))
    for mu, nu in PLANES:
        A = compute_A(mu, nu, R, D)
        M += A.T @ A
    return M

def flatten(R, D):
    params = []
    for mu in range(4):
        params.extend(so3_log(R[mu]))
    for p in PLANES:
        params.extend(so3_log(D[p]))
    return np.array(params)

def unflatten(params):
    R = [so3_exp(params[3*i:3*i+3]) for i in range(4)]
    D = {p: so3_exp(params[12+3*i:12+3*i+3]) for i, p in enumerate(PLANES)}
    return R, D

def gradient_lmax(params, eps=1e-6):
    R, D = unflatten(params)
    M0 = compute_M_total(R, D)
    lam0 = np.linalg.eigvalsh(M0)[2]
    grad = np.zeros_like(params)
    for i in range(len(params)):
        p_plus = params.copy()
        p_plus[i] += eps
        R_p, D_p = unflatten(p_plus)
        M_p = compute_M_total(R_p, D_p)
        grad[i] = (np.linalg.eigvalsh(M_p)[2] - lam0) / eps
    return grad

# ============================================================
# Part 2a: Run adversarial and check ALL rotation conditions
# ============================================================

print("=" * 70)
print("PART 2a: Full rotation analysis at adversarial maxima")
print("=" * 70)

def adversarial_ascent(n_steps=600, lr=0.05):
    R, D = [random_so3() for _ in range(4)], {p: random_so3() for p in PLANES}
    params = flatten(R, D)
    for step in range(n_steps):
        grad = gradient_lmax(params)
        if step < 200:
            params += lr * grad
        elif step < 400:
            params += 0.02 * grad
        else:
            params += 0.005 * grad
    R, D = unflatten(params)
    return R, D

for trial in range(5):
    print(f"\n--- Trial {trial} ---")
    R, D = adversarial_ascent()
    M = compute_M_total(R, D)
    eigs = np.linalg.eigvalsh(M)
    eigvecs = np.linalg.eigh(M)[1]
    n_max = eigvecs[:, 2]

    print(f"Eigenvalues: [{eigs[0]:.4f}, {eigs[1]:.4f}, {eigs[2]:.6f}]")
    print(f"n_max = {n_max}")

    # Check if R_mu fixes n_max
    print(f"\nBase link alignment (R_mu n = n iff |R_mu n - n| = 0):")
    for mu in range(4):
        Rn = R[mu] @ n_max
        err = np.linalg.norm(Rn - n_max)
        angle = rotation_angle(R[mu]) * 180 / np.pi
        axis = rotation_axis(R[mu])
        align = abs(np.dot(axis, n_max))
        print(f"  R_{mu}: |Rn-n| = {err:.6f}, angle = {angle:.1f}°, |axis·n| = {align:.6f}")

    # Check if D fixes n_max
    print(f"\nCross-link alignment (D n = n iff |D n - n| = 0):")
    active_planes = [(mu,nu) for mu,nu in PLANES if (mu+nu)%2 == 1]
    inactive_planes = [(mu,nu) for mu,nu in PLANES if (mu+nu)%2 == 0]

    for mu, nu in active_planes:
        Dn = D[(mu,nu)] @ n_max
        err = np.linalg.norm(Dn - n_max)
        angle = rotation_angle(D[(mu,nu)]) * 180 / np.pi
        axis = rotation_axis(D[(mu,nu)])
        align = abs(np.dot(axis, n_max))
        print(f"  D_({mu},{nu}) [active]:   |Dn-n| = {err:.6f}, angle = {angle:.1f}°, |axis·n| = {align:.6f}")

    for mu, nu in inactive_planes:
        Dn = D[(mu,nu)] @ n_max
        err = np.linalg.norm(Dn - n_max)
        angle = rotation_angle(D[(mu,nu)]) * 180 / np.pi
        print(f"  D_({mu},{nu}) [inactive]: |Dn-n| = {err:.6f}, angle = {angle:.1f}°")

# ============================================================
# Part 2b: Algebraic proof of F_x(n) = 64 when R_mu n = n and D n = n
# ============================================================

print("\n" + "=" * 70)
print("PART 2b: Verify F_x = 64 when rotations fix n (analytical)")
print("=" * 70)

# If R_mu is a rotation about axis n with angle theta_mu:
# R_mu n = n exactly.
# Similarly D rotates about n.

# Test: for n = e_3, create R_mu as rotations about e_3 with various angles
n = np.array([0, 0, 1.0])

for trial in range(20):
    thetas = np.random.uniform(0, 2*np.pi, 4)  # base link angles
    phi_active = np.random.uniform(0, 2*np.pi, 4)  # cross-link angles for active
    phi_inactive = np.random.uniform(0, 2*np.pi, 2)  # cross-link angles for inactive

    # Create rotations about e_3
    R = [so3_exp(thetas[mu] * n) for mu in range(4)]
    D = {}
    active_idx = 0
    inactive_idx = 0
    for mu, nu in PLANES:
        if (mu + nu) % 2 == 1:  # active
            D[(mu,nu)] = so3_exp(phi_active[active_idx] * n)
            active_idx += 1
        else:  # inactive
            D[(mu,nu)] = so3_exp(phi_inactive[inactive_idx] * n)
            inactive_idx += 1

    M = compute_M_total(R, D)
    Fn = n @ M @ n

    if trial < 5:
        print(f"  Trial {trial}: F(n) = {Fn:.6f}, eigs = {np.linalg.eigvalsh(M)}")

print(f"\n  (All should give F(n) = 64.0000)")

# Now test: rotations about n for base, but ARBITRARY rotations for inactive cross-links
print("\nNow: base rotations about n, inactive cross-links ARBITRARY:")
for trial in range(20):
    thetas = np.random.uniform(0, 2*np.pi, 4)
    R = [so3_exp(thetas[mu] * n) for mu in range(4)]

    D = {}
    for mu, nu in PLANES:
        if (mu + nu) % 2 == 1:  # active - rotate about n
            D[(mu,nu)] = so3_exp(np.random.uniform(0, 2*np.pi) * n)
        else:  # inactive - RANDOM rotation
            D[(mu,nu)] = random_so3()

    M = compute_M_total(R, D)
    Fn = n @ M @ n
    if trial < 5:
        print(f"  Trial {trial}: F(n) = {Fn:.6f}")

print(f"\n  (All should STILL give F(n) = 64.0000)")

# Why? Because for inactive planes, (I - R_mu) n = 0, so cross-links don't matter
# Verify this analytically: A n for inactive plane
print("\nVerification: A_p n for inactive planes when R_mu n = n")
for trial in range(5):
    theta0 = np.random.uniform(0, 2*np.pi)
    theta2 = np.random.uniform(0, 2*np.pi)
    R0 = so3_exp(theta0 * n)
    R2 = so3_exp(theta2 * n)
    D02 = random_so3()  # completely random cross-link

    # For plane (0,2): a=1, b=-1
    A = compute_A(0, 2, [R0, None, R2, None], {(0,2): D02})
    An = A @ n
    print(f"  |A_(0,2) n| = {np.linalg.norm(An):.6f} (should be 0)")

# ============================================================
# Part 2c: What happens when base rotations DON'T all fix n?
# ============================================================

print("\n" + "=" * 70)
print("PART 2c: F_x when R_mu n ≠ n (misalignment analysis)")
print("=" * 70)

# Parameterize: R_0 is rotation by angle alpha about axis at angle epsilon from n
# Keep R_1 = R_2 = R_3 = I, D = I

n = np.array([0, 0, 1.0])

print("Test: R_0 = rotation by pi/2 about tilted axis, R_1=R_2=R_3=I, D=I")
print(f"{'eps (deg)':<12} {'F_x(n)':<12} {'lambda_max':<12} {'active_sum':<12} {'inactive_sum':<12}")

for eps_deg in [0, 5, 10, 20, 30, 45, 60, 90]:
    eps = eps_deg * np.pi / 180
    # Axis in xz plane, tilted eps from z
    axis = np.array([np.sin(eps), 0, np.cos(eps)])
    R0 = so3_exp(np.pi/2 * axis)
    R = [R0, np.eye(3), np.eye(3), np.eye(3)]
    D = {p: np.eye(3) for p in PLANES}

    M = compute_M_total(R, D)
    Fn = n @ M @ n
    lmax = np.linalg.eigvalsh(M)[2]

    active_sum = 0
    inactive_sum = 0
    for mu, nu in PLANES:
        A = compute_A(mu, nu, R, D)
        bsq = np.dot(A @ n, A @ n)
        if (mu+nu) % 2 == 1:
            active_sum += bsq
        else:
            inactive_sum += bsq

    print(f"{eps_deg:<12} {Fn:<12.4f} {lmax:<12.4f} {active_sum:<12.4f} {inactive_sum:<12.4f}")

# ============================================================
# Part 2d: Key identity - Expand F_x into cross-term structure
# ============================================================

print("\n" + "=" * 70)
print("PART 2d: Cross-term structure analysis")
print("=" * 70)

# For each plaquette, the 4 SO(3) rotations acting on n are:
# Q_{p,1} = I
# Q_{p,2} = R_mu D_{mu,nu}
# Q_{p,3} = R_mu
# Q_{p,4} = R_mu D_{mu,nu} R_nu^T
#
# |B_p|^2 = |sum_i s_i Q_i n|^2 = sum_{ij} s_i s_j (Q_i n).(Q_j n) = sum_{ij} s_i s_j n^T Q_i^T Q_j n
#
# Cross-term rotations O_k = Q_i^T Q_j:
# (1,2): R_mu D        (1,3): R_mu        (1,4): R_mu D R_nu^T
# (2,3): D^T            (2,4): R_nu^T      (3,4): D R_nu^T

# Let's verify this decomposition numerically
print("\nVerifying cross-term decomposition:")
for trial in range(10):
    R = [random_so3() for _ in range(4)]
    D = {p: random_so3() for p in PLANES}
    n = np.random.randn(3)
    n /= np.linalg.norm(n)

    # Direct computation
    Fx_direct = 0
    for mu, nu in PLANES:
        A = compute_A(mu, nu, R, D)
        Fx_direct += np.dot(A @ n, A @ n)

    # Cross-term computation
    Fx_cross = 24  # diagonal contribution (24 unit vectors)
    for mu, nu in PLANES:
        a = (-1)**mu
        b = (-1)**(nu+1)
        signs = [a, a, b, b]

        Q = [np.eye(3),
             R[mu] @ D[(mu,nu)],
             R[mu],
             R[mu] @ D[(mu,nu)] @ R[nu].T]

        for i in range(4):
            for j in range(i+1, 4):
                sigma = signs[i] * signs[j]
                Ok = Q[i].T @ Q[j]
                Fx_cross += 2 * sigma * (n @ Ok @ n)

    err = abs(Fx_direct - Fx_cross)
    if trial < 3:
        print(f"  Trial {trial}: F_direct = {Fx_direct:.6f}, F_cross = {Fx_cross:.6f}, error = {err:.2e}")

print("  (All errors should be < 1e-10)")

# ============================================================
# Part 2e: Collect cross-terms by rotation type
# ============================================================

print("\n" + "=" * 70)
print("PART 2e: Cross-terms grouped by rotation type")
print("=" * 70)

# The 6 cross-term types per plaquette:
# Type A: (1,3) gives R_mu          — base link only
# Type B: (2,4) gives R_nu^T        — base link only
# Type C: (1,2) gives R_mu D        — base + cross
# Type D: (2,3) gives D^T           — cross only
# Type E: (1,4) gives R_mu D R_nu^T — base + cross + base
# Type F: (3,4) gives D R_nu^T      — cross + base

# Signs for active (a=b): all +1
# Signs for inactive (a=-b):
#   Type A (1,3): s_1 s_3 = a*b = -1
#   Type B (2,4): s_2 s_4 = a*b = -1
#   Type C (1,2): s_1 s_2 = a^2 = +1
#   Type D (2,3): s_2 s_3 = a*b = -1
#   Type E (1,4): s_1 s_4 = a*b = -1
#   Type F (3,4): s_3 s_4 = b^2 = +1

print("\nSign structure for each plaquette type:")
for mu, nu in PLANES:
    a = (-1)**mu
    b = (-1)**(nu+1)
    signs = [a, a, b, b]
    ptype = "active" if (mu+nu)%2==1 else "inactive"

    type_labels = ['A(R_mu)', 'B(R_nu^T)', 'C(R_mu D)', 'D(D^T)', 'E(R_mu D R_nu^T)', 'F(D R_nu^T)']
    pairs = [(0,2), (1,3), (0,1), (1,2), (0,3), (2,3)]

    sigs = []
    for (i,j) in pairs:
        sigs.append(signs[i]*signs[j])

    sig_str = " ".join(f"{l}:{s:+d}" for l, s in zip(type_labels, sigs))
    print(f"  ({mu},{nu}) [{ptype:8s}]: {sig_str}")

# ============================================================
# Part 2f: Compute M_total in the c*I + P decomposition
# ============================================================

print("\n" + "=" * 70)
print("PART 2f: M_total = c*I + P decomposition")
print("=" * 70)

# M_total = 24*I + sum over all 36 cross terms: 2 * sigma_k * sym(O_k)
# where sym(O) = (O + O^T)/2
#
# For O = rotation by theta about axis u:
# sym(O) = cos(theta) * I + (1-cos(theta)) * u u^T
#
# So M_total = [24 + 2*sum sigma_k cos(theta_k)] * I + 2*sum sigma_k (1-cos(theta_k)) * u_k u_k^T
#            = c * I + P
#
# where c = 24 + 2*sum sigma_k cos(theta_k)
#       P = 2*sum sigma_k (1-cos(theta_k)) * u_k u_k^T

def compute_cI_P_decomposition(R, D):
    """Compute M_total = c*I + P."""
    c = 24.0
    P = np.zeros((3, 3))

    for mu, nu in PLANES:
        a = (-1)**mu
        b = (-1)**(nu+1)
        signs = [a, a, b, b]

        Q = [np.eye(3),
             R[mu] @ D[(mu,nu)],
             R[mu],
             R[mu] @ D[(mu,nu)] @ R[nu].T]

        for i in range(4):
            for j in range(i+1, 4):
                sigma = signs[i] * signs[j]
                Ok = Q[i].T @ Q[j]

                # Extract angle and axis
                theta = rotation_angle(Ok)
                if theta < 1e-10:
                    c += 2 * sigma  # cos(0) = 1, (1-cos(0))*uu^T = 0
                else:
                    u = rotation_axis(Ok)
                    c += 2 * sigma * np.cos(theta)
                    P += 2 * sigma * (1 - np.cos(theta)) * np.outer(u, u)

    return c, P

# Verify decomposition
print("Verifying c*I + P = M_total:")
for trial in range(10):
    R = [random_so3() for _ in range(4)]
    D = {p: random_so3() for p in PLANES}

    M = compute_M_total(R, D)
    c, P = compute_cI_P_decomposition(R, D)
    M_reconstructed = c * np.eye(3) + P

    err = np.max(np.abs(M - M_reconstructed))
    if trial < 3:
        eigs_M = np.linalg.eigvalsh(M)
        eigs_P = np.linalg.eigvalsh(P)
        print(f"  Trial {trial}: c = {c:.4f}, eigs(P) = [{eigs_P[0]:.4f}, {eigs_P[1]:.4f}, {eigs_P[2]:.4f}]")
        print(f"    eigs(M) = [{eigs_M[0]:.4f}, {eigs_M[1]:.4f}, {eigs_M[2]:.4f}]")
        print(f"    c + max(eigs_P) = {c + eigs_P[2]:.4f}")
        print(f"    Reconstruction error: {err:.2e}")

# ============================================================
# Part 2g: The KEY relationship: c + lambda_max(P) <= 64?
# ============================================================

print("\n" + "=" * 70)
print("PART 2g: Testing c + lambda_max(P) <= 64")
print("=" * 70)

c_vals = []
p_lmax_vals = []
sum_vals = []

for _ in range(10000):
    R = [random_so3() for _ in range(4)]
    D = {p: random_so3() for p in PLANES}

    c, P = compute_cI_P_decomposition(R, D)
    p_lmax = np.linalg.eigvalsh(P)[2]

    c_vals.append(c)
    p_lmax_vals.append(p_lmax)
    sum_vals.append(c + p_lmax)

c_vals = np.array(c_vals)
p_lmax_vals = np.array(p_lmax_vals)
sum_vals = np.array(sum_vals)

print(f"{'Quantity':<25} {'Min':>10} {'Mean':>10} {'Max':>10}")
print("-" * 55)
print(f"{'c':<25} {c_vals.min():10.4f} {c_vals.mean():10.4f} {c_vals.max():10.4f}")
print(f"{'lambda_max(P)':<25} {p_lmax_vals.min():10.4f} {p_lmax_vals.mean():10.4f} {p_lmax_vals.max():10.4f}")
print(f"{'c + lambda_max(P)':<25} {sum_vals.min():10.4f} {sum_vals.mean():10.4f} {sum_vals.max():10.4f}")
print(f"\nc + lambda_max(P) > 64: {np.sum(sum_vals > 64 + 1e-10)} / {len(sum_vals)}")
print(f"(Since M_total = cI + P, lambda_max(M) = c + lambda_max(P))")

# ============================================================
# Part 2h: Correlation between c and lambda_max(P)
# ============================================================

print("\n" + "=" * 70)
print("PART 2h: Trade-off between c and lambda_max(P)")
print("=" * 70)

# Key insight: as c decreases from 64 (rotations move away from I),
# P can develop positive eigenvalues. But c + lambda_max(P) stays <= 64.

# Group by c value
for c_low, c_high in [(-20, 0), (0, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 65)]:
    mask = (c_vals >= c_low) & (c_vals < c_high)
    if mask.sum() > 0:
        p_in_range = p_lmax_vals[mask]
        s_in_range = sum_vals[mask]
        print(f"  c in [{c_low:3d},{c_high:3d}): count={mask.sum():5d}, "
              f"max(P_lmax)={p_in_range.max():.4f}, max(c+P_lmax)={s_in_range.max():.4f}, "
              f"64-c_max={64-c_low:.0f}")

# ============================================================
# Part 2i: Tr(P) and the trace constraint
# ============================================================

print("\n" + "=" * 70)
print("PART 2i: Trace of P")
print("=" * 70)

# Tr(M) = 3c + Tr(P) <= 192
# Tr(P) <= 192 - 3c
# If P has rank at most r, then lambda_max(P) <= Tr(P)_+ <= Tr(P) (when P >= 0)
# But P can have negative eigenvalues.

# For the bound: lambda_max(P) <= ?

tr_P_vals = []
for _ in range(5000):
    R = [random_so3() for _ in range(4)]
    D = {p: random_so3() for p in PLANES}
    c, P = compute_cI_P_decomposition(R, D)
    tr_P_vals.append(np.trace(P))

tr_P_vals = np.array(tr_P_vals)

# Also check: Tr(M) = 3c + Tr(P) relationship
print(f"Tr(P) stats: min={tr_P_vals.min():.4f}, mean={tr_P_vals.mean():.4f}, max={tr_P_vals.max():.4f}")
print(f"Note: Tr(M) = 3c + Tr(P)")

# Check: is Tr(P) always <= 192 - 3c? (Should be since Tr(M) <= 192)
# Actually, is Tr(M) always <= 192?
all_tr = []
for _ in range(5000):
    R = [random_so3() for _ in range(4)]
    D = {p: random_so3() for p in PLANES}
    M = compute_M_total(R, D)
    all_tr.append(np.trace(M))

print(f"Tr(M) max: {max(all_tr):.4f} (is <= 192? {max(all_tr) <= 192 + 1e-10})")

# ============================================================
# Part 2j: Is Tr(M) <= 192 always true? PROVE IT.
# ============================================================

print("\n" + "=" * 70)
print("PART 2j: Adversarial ascent on Tr(M_total)")
print("=" * 70)

def gradient_trace(params, eps=1e-6):
    R, D = unflatten(params)
    M0 = compute_M_total(R, D)
    tr0 = np.trace(M0)
    grad = np.zeros_like(params)
    for i in range(len(params)):
        p_plus = params.copy()
        p_plus[i] += eps
        R_p, D_p = unflatten(p_plus)
        M_p = compute_M_total(R_p, D_p)
        grad[i] = (np.trace(M_p) - tr0) / eps
    return grad

print("Adversarial ascent on Tr(M_total):")
max_tr = 0
for trial in range(10):
    R = [random_so3() for _ in range(4)]
    D = {p: random_so3() for p in PLANES}
    params = flatten(R, D)

    for step in range(300):
        grad = gradient_trace(params)
        lr = 0.03 if step < 150 else 0.01
        params += lr * grad

    R, D = unflatten(params)
    M = compute_M_total(R, D)
    tr = np.trace(M)
    max_tr = max(max_tr, tr)
    eigs = np.linalg.eigvalsh(M)
    print(f"  Trial {trial}: Tr = {tr:.4f}, eigs = [{eigs[0]:.2f}, {eigs[1]:.2f}, {eigs[2]:.2f}]")

print(f"\nMax Tr achieved: {max_tr:.4f}")
print(f"Gap to 192: {192 - max_tr:.4f}")

print("\nDone with Stage 2.")
