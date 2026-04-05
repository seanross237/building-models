"""
Stage 2b: Matrix formulation of F_x.

KEY INSIGHT: F_x = n^T M_total n where M_total is a 3x3 PSD matrix independent of n.
The bound F_x <= 64 for all unit n is equivalent to lambda_max(M_total) <= 64.

At Q=I: M_total = 64*I (all eigenvalues equal 64).
Conjecture: lambda_max(M_total) <= 64 for ALL Q.

This script computes M_total for many configs and checks its eigenvalues.
"""

import numpy as np
from itertools import product as iproduct

np.random.seed(777)

# SO(3) utilities
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
    """Exponential map: so(3) -> SO(3). omega is a 3-vector."""
    angle = np.linalg.norm(omega)
    if angle < 1e-14:
        return np.eye(3)
    axis = omega / angle
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(angle)*K + (1-np.cos(angle))*(K @ K)

# Plaquette structure
planes = [(mu, nu) for mu in range(4) for nu in range(mu+1, 4)]
sigmas = {(mu,nu): (-1)**(mu+nu+1) for mu,nu in planes}

def compute_M_total(R, D):
    """
    Compute M_total = sum_{mu<nu} (a S + b T)^T (a S + b T)

    where S = I + R_mu D, T = R_mu + R_mu D R_nu^T
    a = (-1)^mu, b = (-1)^{nu+1} (for vertex with |x|=0)
    """
    M = np.zeros((3, 3))
    for mu, nu in planes:
        a = (-1)**mu
        b = (-1)**(nu+1)
        S = np.eye(3) + R[mu] @ D[(mu,nu)]
        T = R[mu] + R[mu] @ D[(mu,nu)] @ R[nu].T
        A = a * S + b * T  # 3x3 matrix
        M += A.T @ A
    return M

def compute_Fx(R, D, n):
    """Direct computation of F_x."""
    M = compute_M_total(R, D)
    return n @ M @ n

# ============================================================
# Verify M_total formulation
# ============================================================

print("=" * 70)
print("VERIFY: M_total formulation matches direct computation")
print("=" * 70)

n_test = np.array([1.0, 0.0, 0.0])
max_err = 0.0

for _ in range(100):
    R = [random_so3() for _ in range(4)]
    D = {(mu,nu): random_so3() for mu,nu in planes}

    Fx_M = n_test @ compute_M_total(R, D) @ n_test

    # Direct computation
    Fx_direct = 0.0
    for mu, nu in planes:
        a = (-1)**mu
        b = (-1)**(nu+1)
        p = R[mu] @ D[(mu,nu)] @ n_test
        q = D[(mu,nu)] @ R[nu].T @ n_test
        u = n_test + p
        v = n_test + q
        sigma = sigmas[(mu,nu)]
        Fx_direct += np.dot(u,u) + np.dot(v,v) + 2*sigma*np.dot(u, R[mu] @ v)

    err = abs(Fx_M - Fx_direct)
    max_err = max(max_err, err)

print(f"Max error: {max_err:.2e}")
print(f"RESULT: {'PASS' if max_err < 1e-10 else 'FAIL'}")

# ============================================================
# Check M_total at Q = I
# ============================================================

print("\n" + "=" * 70)
print("CHECK: M_total at Q=I")
print("=" * 70)

R_I = [np.eye(3)] * 4
D_I = {(mu,nu): np.eye(3) for mu,nu in planes}
M_I = compute_M_total(R_I, D_I)
print("M_total at Q=I:")
print(M_I)
eigs_I = np.linalg.eigvalsh(M_I)
print(f"Eigenvalues: {eigs_I}")
print(f"Expected: [64, 64, 64]")

# ============================================================
# Main test: eigenvalues of M_total for random configs
# ============================================================

print("\n" + "=" * 70)
print("MAIN TEST: lambda_max(M_total) for random configs")
print("=" * 70)

n_trials = 10000
max_eig_all = 0.0
trace_at_max = 0.0
max_eig_vals = []

for trial in range(n_trials):
    R = [random_so3() for _ in range(4)]
    D = {(mu,nu): random_so3() for mu,nu in planes}
    M = compute_M_total(R, D)
    eigs = np.linalg.eigvalsh(M)
    max_eig = eigs[2]
    max_eig_vals.append(max_eig)

    if max_eig > max_eig_all:
        max_eig_all = max_eig
        trace_at_max = np.trace(M)
        eigs_at_max = eigs.copy()
        R_best = [r.copy() for r in R]
        D_best = {k: v.copy() for k, v in D.items()}

print(f"Over {n_trials} random (R, D) configs:")
print(f"  Max lambda_max: {max_eig_all:.6f}")
print(f"  Eigenvalues at max: {eigs_at_max}")
print(f"  Trace at max: {trace_at_max:.4f} (expected <= 192)")
print(f"  Mean lambda_max: {np.mean(max_eig_vals):.4f}")
print(f"  Violation count (> 64): {sum(1 for e in max_eig_vals if e > 64 + 1e-10)}")

# ============================================================
# Trace analysis
# ============================================================

print("\n" + "=" * 70)
print("TRACE ANALYSIS: Tr(M_total) distribution")
print("=" * 70)

traces = []
for _ in range(5000):
    R = [random_so3() for _ in range(4)]
    D = {(mu,nu): random_so3() for mu,nu in planes}
    M = compute_M_total(R, D)
    traces.append(np.trace(M))

print(f"Tr(M_total) stats:")
print(f"  Min: {min(traces):.4f}")
print(f"  Max: {max(traces):.4f}")
print(f"  Mean: {np.mean(traces):.4f}")
print(f"  At Q=I: 192.0000")
print(f"  Tr > 192 count: {sum(1 for t in traces if t > 192 + 1e-10)}")

# ============================================================
# Adversarial gradient ascent on lambda_max(M_total)
# ============================================================

print("\n" + "=" * 70)
print("ADVERSARIAL: Gradient ascent on lambda_max(M_total)")
print("=" * 70)

def max_eigenvalue_gradient(R, D, eps=1e-6):
    """
    Compute gradient of lambda_max(M_total) w.r.t.
    the axis-angle parameters of R and D.

    R parameterized by 4 * 3 = 12 params
    D parameterized by 6 * 3 = 18 params
    Total: 30 params
    """
    M0 = compute_M_total(R, D)
    lam0 = np.linalg.eigvalsh(M0)[2]

    grad_R = np.zeros((4, 3))
    grad_D = np.zeros((6, 3))

    for mu in range(4):
        for j in range(3):
            omega = np.zeros(3)
            omega[j] = eps
            R_p = [r.copy() for r in R]
            R_p[mu] = R[mu] @ so3_exp(omega)
            M_p = compute_M_total(R_p, D)
            grad_R[mu, j] = (np.linalg.eigvalsh(M_p)[2] - lam0) / eps

    for i, (mu, nu) in enumerate(planes):
        for j in range(3):
            omega = np.zeros(3)
            omega[j] = eps
            D_p = {k: v.copy() for k, v in D.items()}
            D_p[(mu,nu)] = D[(mu,nu)] @ so3_exp(omega)
            M_p = compute_M_total(R, D_p)
            grad_D[i, j] = (np.linalg.eigvalsh(M_p)[2] - lam0) / eps

    return grad_R, grad_D, lam0

def adversarial_ascent(n_steps=300, lr=0.02):
    """Gradient ascent on lambda_max from random start."""
    R = [random_so3() for _ in range(4)]
    D = {(mu,nu): random_so3() for mu,nu in planes}

    best_lam = 0.0

    for step in range(n_steps):
        gR, gD, lam = max_eigenvalue_gradient(R, D)
        best_lam = max(best_lam, lam)

        # Gradient step on R
        for mu in range(4):
            R[mu] = R[mu] @ so3_exp(lr * gR[mu])

        # Gradient step on D
        for i, (mu, nu) in enumerate(planes):
            D[(mu,nu)] = D[(mu,nu)] @ so3_exp(lr * gD[i])

    return best_lam, R, D

print("Running 30 adversarial trials...")
max_adv = 0.0
for trial in range(30):
    lam, R, D = adversarial_ascent(n_steps=300, lr=0.02)
    max_adv = max(max_adv, lam)
    if trial < 5 or lam > 60:
        M = compute_M_total(R, D)
        eigs = np.linalg.eigvalsh(M)
        print(f"  Trial {trial:2d}: lambda_max = {lam:.6f}, eigs = {eigs}")

print(f"\nMax adversarial lambda_max: {max_adv:.6f}")
print(f"Gap to 64: {64 - max_adv:.6f}")

# ============================================================
# Start from identity and perturb
# ============================================================

print("\n" + "=" * 70)
print("IDENTITY PERTURBATION: Starting from Q=I")
print("=" * 70)

def adversarial_from_identity(n_steps=500, lr=0.01):
    """Start at Q=I, gradient ascent."""
    R = [np.eye(3) for _ in range(4)]
    D = {(mu,nu): np.eye(3) for mu,nu in planes}

    best_lam = 64.0
    best_step = 0

    for step in range(n_steps):
        gR, gD, lam = max_eigenvalue_gradient(R, D)
        if lam > best_lam:
            best_lam = lam
            best_step = step

        for mu in range(4):
            R[mu] = R[mu] @ so3_exp(lr * gR[mu])
        for i, (mu, nu) in enumerate(planes):
            D[(mu,nu)] = D[(mu,nu)] @ so3_exp(lr * gD[i])

    return best_lam, best_step

print("Running 10 trials starting from identity...")
for trial in range(10):
    lam, step = adversarial_from_identity(n_steps=500, lr=0.005 + 0.005*trial)
    print(f"  Trial {trial}: lr={0.005+0.005*trial:.4f}, max lambda = {lam:.6f} at step {step}")

# ============================================================
# Eigenvalue structure: how anisotropic is M_total?
# ============================================================

print("\n" + "=" * 70)
print("EIGENVALUE STRUCTURE: Anisotropy of M_total")
print("=" * 70)

# Define anisotropy = lambda_max / (Tr/3)
anisotropies = []
for _ in range(3000):
    R = [random_so3() for _ in range(4)]
    D = {(mu,nu): random_so3() for mu,nu in planes}
    M = compute_M_total(R, D)
    eigs = sorted(np.linalg.eigvalsh(M))
    tr = sum(eigs)
    if tr > 1e-10:
        anisotropies.append(eigs[2] / (tr/3))

print(f"Anisotropy ratio (lambda_max / (Tr/3)):")
print(f"  Min: {min(anisotropies):.4f}")
print(f"  Max: {max(anisotropies):.4f}")
print(f"  Mean: {np.mean(anisotropies):.4f}")
print(f"  At Q=I: 1.0000")

# If anisotropy is bounded, say <= alpha, then lambda_max <= alpha * Tr/3.
# Combined with Tr <= 192: lambda_max <= 64 * alpha.
# If alpha <= 1, done!

print(f"\nImplied bound: lambda_max <= {max(anisotropies):.4f} * Tr/3 <= {max(anisotropies)*192/3:.4f}")
print(f"Need <= 64.0")

# ============================================================
# Trace bound: is Tr(M_total) <= 192?
# ============================================================

print("\n" + "=" * 70)
print("TRACE BOUND TEST")
print("=" * 70)

# Check if Tr(M_total) is ALWAYS <= 192
max_trace = 0.0
for _ in range(10000):
    R = [random_so3() for _ in range(4)]
    D = {(mu,nu): random_so3() for mu,nu in planes}
    M = compute_M_total(R, D)
    tr = np.trace(M)
    max_trace = max(max_trace, tr)

print(f"Max Tr(M_total) over 10000 trials: {max_trace:.6f}")
print(f"Tr <= 192?: {'YES' if max_trace < 192 + 1e-10 else 'NO'}")

# Adversarial ascent on trace
print("\nAdversarial gradient ascent on Tr(M_total)...")
for trial in range(5):
    R = [random_so3() for _ in range(4)]
    D = {(mu,nu): random_so3() for mu,nu in planes}

    for step in range(200):
        eps = 1e-5
        tr0 = np.trace(compute_M_total(R, D))

        for mu in range(4):
            for j in range(3):
                omega = np.zeros(3)
                omega[j] = eps
                R_p = [r.copy() for r in R]
                R_p[mu] = R[mu] @ so3_exp(omega)
                dtr = (np.trace(compute_M_total(R_p, D)) - tr0) / eps
                R[mu] = R[mu] @ so3_exp(0.01 * dtr * np.eye(3)[j])

        for i, (mu, nu) in enumerate(planes):
            for j in range(3):
                omega = np.zeros(3)
                omega[j] = eps
                D_p = {k: v.copy() for k, v in D.items()}
                D_p[(mu,nu)] = D[(mu,nu)] @ so3_exp(omega)
                dtr = (np.trace(compute_M_total(R, D_p)) - tr0) / eps
                D[(mu,nu)] = D[(mu,nu)] @ so3_exp(0.01 * dtr * np.eye(3)[j])

    tr_final = np.trace(compute_M_total(R, D))
    print(f"  Trial {trial}: Tr = {tr_final:.4f}")

print("\nDone with Stage 2b.")
