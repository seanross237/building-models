"""
Stage 1: Comprehensive computation of M_total and its eigenvalue structure.

M_total = sum_{mu<nu} A_{mu,nu}^T A_{mu,nu}  (a 3x3 PSD matrix)

where A_{mu,nu} = a*S + b*T with:
  S = I + R_mu * D_{mu,nu}
  T = R_mu + R_mu * D_{mu,nu} * R_nu^T
  a = (-1)^mu,  b = (-1)^{nu+1}

From E005 [VERIFIED]: this matches the direct B-field computation.
"""

import numpy as np
from itertools import product as iproduct

np.random.seed(42)

# ============================================================
# SO(3) utilities
# ============================================================

def random_so3():
    """Random SO(3) matrix from Haar measure (via quaternion)."""
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    w, x, y, z = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])

def so3_exp(omega):
    """Exponential map: so(3) -> SO(3). omega is a 3-vector."""
    angle = np.linalg.norm(omega)
    if angle < 1e-14:
        return np.eye(3)
    axis = omega / angle
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(angle)*K + (1-np.cos(angle))*(K @ K)

def so3_log(R):
    """Logarithm map: SO(3) -> so(3). Returns axis-angle vector."""
    tr = np.clip((np.trace(R) - 1) / 2, -1, 1)
    angle = np.arccos(tr)
    if angle < 1e-10:
        return np.zeros(3)
    axis = np.array([R[2,1]-R[1,2], R[0,2]-R[2,0], R[1,0]-R[0,1]]) / (2*np.sin(angle))
    return angle * axis

# ============================================================
# M_total computation
# ============================================================

PLANES = [(mu, nu) for mu in range(4) for nu in range(mu+1, 4)]

def compute_A(mu, nu, R, D):
    """Compute A_{mu,nu} matrix."""
    a = (-1)**mu
    b = (-1)**(nu+1)
    S = np.eye(3) + R[mu] @ D[(mu,nu)]
    T = R[mu] + R[mu] @ D[(mu,nu)] @ R[nu].T
    return a * S + b * T

def compute_M_total(R, D):
    """Compute 3x3 PSD matrix M_total = sum A^T A."""
    M = np.zeros((3, 3))
    for mu, nu in PLANES:
        A = compute_A(mu, nu, R, D)
        M += A.T @ A
    return M

def make_identity_config():
    """Return (R, D) at identity."""
    R = [np.eye(3)] * 4
    D = {p: np.eye(3) for p in PLANES}
    return R, D

def make_random_config():
    """Return random (R, D) from Haar measure."""
    R = [random_so3() for _ in range(4)]
    D = {p: random_so3() for p in PLANES}
    return R, D

# ============================================================
# Flatten/unflatten for optimization
# ============================================================

def flatten(R, D):
    """Flatten config to parameter vector (30 params = 4*3 + 6*3)."""
    params = []
    for mu in range(4):
        params.extend(so3_log(R[mu]))
    for p in PLANES:
        params.extend(so3_log(D[p]))
    return np.array(params)

def unflatten(params):
    """Unflatten parameter vector to (R, D)."""
    R = [so3_exp(params[3*i:3*i+3]) for i in range(4)]
    D = {p: so3_exp(params[12+3*i:12+3*i+3]) for i, p in enumerate(PLANES)}
    return R, D

# ============================================================
# Test 1: Verify M_total(I) = 64*I
# ============================================================

print("=" * 70)
print("TEST 1: M_total at identity")
print("=" * 70)

R_I, D_I = make_identity_config()
M_I = compute_M_total(R_I, D_I)
print("M_total(I) =")
print(M_I)
eigs_I = np.linalg.eigvalsh(M_I)
print(f"Eigenvalues: {eigs_I}")
err = np.max(np.abs(M_I - 64*np.eye(3)))
print(f"Max |M - 64I|: {err:.2e}")
print(f"RESULT: {'PASS' if err < 1e-10 else 'FAIL'}")

# ============================================================
# Test 2: Per-plaquette contributions at Q=I
# ============================================================

print("\n" + "=" * 70)
print("TEST 2: Per-plaquette contributions at Q=I")
print("=" * 70)

for mu, nu in PLANES:
    a = (-1)**mu
    b = (-1)**(nu+1)
    A = compute_A(mu, nu, R_I, D_I)
    AtA = A.T @ A
    eigs = np.linalg.eigvalsh(AtA)
    sign_type = "active" if (mu+nu) % 2 == 1 else "inactive"
    print(f"  ({mu},{nu}): a={a:+d}, b={b:+d}, a+b={a+b:+d}, "
          f"eigs={eigs}, type={sign_type}")

# ============================================================
# Test 3: Random configs - eigenvalue statistics
# ============================================================

print("\n" + "=" * 70)
print("TEST 3: Random configs - eigenvalue statistics (N=10000)")
print("=" * 70)

N = 10000
all_lmax = []
all_lmid = []
all_lmin = []
all_trace = []
all_trace2 = []
all_det = []

for trial in range(N):
    R, D = make_random_config()
    M = compute_M_total(R, D)
    eigs = np.linalg.eigvalsh(M)
    all_lmax.append(eigs[2])
    all_lmid.append(eigs[1])
    all_lmin.append(eigs[0])
    all_trace.append(np.trace(M))
    all_trace2.append(np.trace(M @ M))
    all_det.append(np.linalg.det(M))

all_lmax = np.array(all_lmax)
all_lmid = np.array(all_lmid)
all_lmin = np.array(all_lmin)
all_trace = np.array(all_trace)
all_trace2 = np.array(all_trace2)
all_det = np.array(all_det)

print(f"{'Statistic':<20} {'Min':>12} {'Mean':>12} {'Max':>12}")
print("-" * 56)
print(f"{'lambda_max':<20} {all_lmax.min():12.4f} {all_lmax.mean():12.4f} {all_lmax.max():12.4f}")
print(f"{'lambda_mid':<20} {all_lmid.min():12.4f} {all_lmid.mean():12.4f} {all_lmid.max():12.4f}")
print(f"{'lambda_min':<20} {all_lmin.min():12.4f} {all_lmin.mean():12.4f} {all_lmin.max():12.4f}")
print(f"{'Tr(M)':<20} {all_trace.min():12.4f} {all_trace.mean():12.4f} {all_trace.max():12.4f}")
print(f"{'Tr(M^2)':<20} {all_trace2.min():12.4f} {all_trace2.mean():12.4f} {all_trace2.max():12.4f}")
print(f"{'det(M)':<20} {all_det.min():12.4f} {all_det.mean():12.4f} {all_det.max():12.4f}")

violations = np.sum(all_lmax > 64 + 1e-10)
print(f"\nViolations (lambda_max > 64): {violations} / {N}")

# ============================================================
# Test 4: Adversarial gradient ascent on lambda_max
# ============================================================

print("\n" + "=" * 70)
print("TEST 4: Adversarial gradient ascent on lambda_max (30 trials)")
print("=" * 70)

def objective_neg_lmax(params):
    """Negative of lambda_max for minimization."""
    R, D = unflatten(params)
    M = compute_M_total(R, D)
    return -np.linalg.eigvalsh(M)[2]

def gradient_lmax(params, eps=1e-6):
    """Numerical gradient of lambda_max."""
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

adv_results = []
adv_configs = []

for trial in range(30):
    R, D = make_random_config()
    params = flatten(R, D)

    lr = 0.05
    best_lam = 0

    for step in range(500):
        grad = gradient_lmax(params)
        params += lr * grad
        R, D = unflatten(params)
        M = compute_M_total(R, D)
        lam = np.linalg.eigvalsh(M)[2]
        best_lam = max(best_lam, lam)

        # Reduce lr
        if step == 200:
            lr = 0.02
        if step == 350:
            lr = 0.01

    M_final = compute_M_total(R, D)
    eigs_final = np.linalg.eigvalsh(M_final)
    adv_results.append(eigs_final)
    adv_configs.append((R, D))

    if trial < 10 or best_lam > 63.99:
        print(f"  Trial {trial:2d}: lambda_max = {best_lam:.6f}, "
              f"eigs = [{eigs_final[0]:.2f}, {eigs_final[1]:.2f}, {eigs_final[2]:.4f}]")

max_adv = max(e[2] for e in adv_results)
print(f"\nMax adversarial lambda_max: {max_adv:.6f}")
print(f"Gap to 64: {64 - max_adv:.6f}")

# ============================================================
# Test 5: Saturation analysis - structure at lambda_max = 64
# ============================================================

print("\n" + "=" * 70)
print("TEST 5: Structure at adversarial maxima (lambda_max ≈ 64)")
print("=" * 70)

for trial_idx in range(min(10, len(adv_configs))):
    R, D = adv_configs[trial_idx]
    M = compute_M_total(R, D)
    eigs = np.linalg.eigvalsh(M)

    if eigs[2] > 63.9:
        print(f"\n--- Trial {trial_idx}: eigs = [{eigs[0]:.4f}, {eigs[1]:.4f}, {eigs[2]:.6f}]")

        # Find the eigenvector for lambda_max
        eigvals, eigvecs = np.linalg.eigh(M)
        n_max = eigvecs[:, 2]  # eigenvector for largest eigenvalue
        print(f"  n_max = [{n_max[0]:.4f}, {n_max[1]:.4f}, {n_max[2]:.4f}]")

        # Check: does n_max align with any rotation axis?
        for mu in range(4):
            axis = so3_log(R[mu])
            if np.linalg.norm(axis) > 0.01:
                axis_norm = axis / np.linalg.norm(axis)
                alignment = abs(np.dot(n_max, axis_norm))
                angle = np.linalg.norm(axis) * 180 / np.pi
                print(f"  R_{mu}: angle = {angle:.1f}°, |n·axis| = {alignment:.4f}")

        # Per-plaquette contributions at this config and n_max
        print(f"  Per-plaquette |B|^2 at n_max:")
        total = 0
        for mu, nu in PLANES:
            A = compute_A(mu, nu, R, D)
            b_sq = np.dot(A @ n_max, A @ n_max)
            total += b_sq
            sign_type = "active" if (mu+nu)%2==1 else "inactive"
            print(f"    ({mu},{nu}) [{sign_type}]: {b_sq:.4f}")
        print(f"    Total: {total:.4f}")

        # Trace and other invariants
        print(f"  Tr(M) = {np.trace(M):.4f}")
        print(f"  Tr(M^2) = {np.trace(M@M):.4f}")
        print(f"  det(M) = {np.linalg.det(M):.4f}")

# ============================================================
# Test 6: Decomposition M = 24I + C (diagonal + cross terms)
# ============================================================

print("\n" + "=" * 70)
print("TEST 6: Decomposition M = 24I + C")
print("=" * 70)
print("Each |B_p|^2 = |sum_i s_i R_i n|^2 has diagonal terms = 4")
print("So diagonal contribution = 6*4 = 24 per component => 24*I")
print("Cross terms C = M - 24I")

# Verify at Q=I
C_I = M_I - 24*np.eye(3)
print(f"\nAt Q=I: C = M - 24I =")
print(C_I)
print(f"C eigenvalues: {np.linalg.eigvalsh(C_I)}")
print(f"Expected: [40, 40, 40]")

# Random configs
c_lmax_list = []
for _ in range(5000):
    R, D = make_random_config()
    M = compute_M_total(R, D)
    C = M - 24*np.eye(3)
    c_eigs = np.linalg.eigvalsh(C)
    c_lmax_list.append(c_eigs[2])

print(f"\nC = M - 24I eigenvalue stats (5000 random):")
print(f"  lambda_max(C) range: [{min(c_lmax_list):.4f}, {max(c_lmax_list):.4f}]")
print(f"  Need lambda_max(C) <= 40")
print(f"  Bound holds: {max(c_lmax_list) <= 40 + 1e-10}")

print("\nDone with Stage 1.")
