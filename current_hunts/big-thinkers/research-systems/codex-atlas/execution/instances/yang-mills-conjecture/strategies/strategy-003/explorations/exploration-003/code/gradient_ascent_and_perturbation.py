"""
Gradient ascent on lambda_max(HessS(Q)) and perturbation analysis.

1. Gradient ascent on lambda_max w.r.t. Q to find the global max
2. Perturbation of lambda_max at flat connections
3. Analysis of cross-term operator norms
4. Study of lambda_min (most negative eigenvalue)
"""

import numpy as np
import sys
sys.path.insert(0, '.')
from hessian_core import *

def su2_exp(w_vec):
    """Matrix exponential of w = Σ w_a iσ_a ∈ su(2).
    exp(w) = cos(θ)I + sin(θ)/θ * w where θ = |w_vec|.
    """
    theta = np.linalg.norm(w_vec)
    if theta < 1e-12:
        return np.eye(2, dtype=complex)
    w = sum(w_vec[a] * isigma[a] for a in range(3))
    return np.cos(theta) * np.eye(2, dtype=complex) + (np.sin(theta) / theta) * w

def expm(M):
    """General 2x2 matrix exp for su(2) elements."""
    # M should be traceless anti-hermitian for su(2)
    # Extract coefficients: M = Σ c_a iσ_a
    c = np.zeros(3)
    for a in range(3):
        c[a] = np.real(np.trace(M @ isigma[a].conj().T)) / (-2)  # Tr(iσ_a iσ_b) = -2δ
    # Actually for iσ_a: Tr((iσ_a)†(iσ_b)) = Tr(-iσ_a iσ_b) = 2δ_ab
    c = np.zeros(3)
    for a in range(3):
        c[a] = np.real(np.trace(-isigma[a] @ M)) / 2  # -Tr(iσ_a M)/2 should give c_a if M = Σ c_b iσ_b
    # Actually: Tr(iσ_a × iσ_b) = -2δ_ab, so Tr(iσ_a × M) = Σ c_b Tr(iσ_a iσ_b) = -2c_a
    # So c_a = -Tr(iσ_a × M)/2
    c = np.array([-np.real(np.trace(isigma[a] @ M)) / 2 for a in range(3)])
    return su2_exp(c)

def perturb_config(Q, eps, directions):
    """Perturb Q_e -> Q_e exp(eps * w_e) where w_e = Σ d_a iσ_a."""
    Q_new = []
    ne = len(Q)
    for e in range(ne):
        Q_new.append(Q[e] @ su2_exp(eps * directions[e]))
    return Q_new

def gradient_of_lambda_max(lat, Q, beta=1.0, N=2):
    """Compute gradient of lambda_max(HessS(Q)) w.r.t. Q.

    Uses finite differences: perturb each Q_e in each iσ_a direction.
    Returns gradient as (nedges, 3) array.
    """
    ne = lat.nedges
    H0 = compute_hessian(lat, Q, beta, N)
    lmax0 = np.linalg.eigvalsh(H0)[-1]

    eps = 1e-5
    grad = np.zeros((ne, 3))

    for e in range(ne):
        for a in range(3):
            Q_pert = [Qi.copy() for Qi in Q]
            Q_pert[e] = Q[e] @ su2_exp(eps * np.array([1 if b==a else 0 for b in range(3)]))
            H_pert = compute_hessian(lat, Q_pert, beta, N)
            lmax_pert = np.linalg.eigvalsh(H_pert)[-1]
            grad[e, a] = (lmax_pert - lmax0) / eps

    return grad, lmax0

def gradient_ascent_lambda_max(lat, Q_init, n_steps=100, lr=0.01, beta=1.0, N=2):
    """Gradient ascent on lambda_max w.r.t. Q."""
    Q = [Qi.copy() for Qi in Q_init]
    history = []

    for step in range(n_steps):
        grad, lmax = gradient_of_lambda_max(lat, Q, beta, N)
        history.append(lmax)

        # Update: Q_e -> Q_e exp(lr * grad_e)
        for e in range(lat.nedges):
            Q[e] = Q[e] @ su2_exp(lr * grad[e])

        if step % 20 == 0:
            print(f"  Step {step}: lambda_max = {lmax:.6f}, |grad| = {np.linalg.norm(grad):.6f}")

    # Final evaluation
    H_final = compute_hessian(lat, Q, beta, N)
    lmax_final = np.linalg.eigvalsh(H_final)[-1]
    history.append(lmax_final)

    return Q, history

def cross_term_kernel_norm(X, Y, Z):
    """Compute operator norm of the 3x3 cross-term kernel
    F_{ab} = Re Tr(X iσ_a Y iσ_b Z) for SU(2) matrices X, Y, Z."""
    F = np.zeros((3, 3))
    for a in range(3):
        for b in range(3):
            F[a, b] = np.real(np.trace(X @ isigma[a] @ Y @ isigma[b] @ Z))
    return np.linalg.norm(F, ord=2), F

print("=" * 70)
print("GRADIENT ASCENT ON LAMBDA_MAX")
print("=" * 70)

for d in [2, 3, 4]:
    L = 2
    lat = Lattice(d, L)
    target = 4 * d
    rng = np.random.default_rng(42 + d)

    print(f"\nd={d}, L={L}, target=4d={target}")

    # Start from random config
    best_lmax = 0
    for trial in range(3):
        Q0 = random_config(lat, rng)
        Q_opt, hist = gradient_ascent_lambda_max(lat, Q0, n_steps=80, lr=0.02)
        final = hist[-1]
        if final > best_lmax:
            best_lmax = final
        print(f"  Trial {trial}: start={hist[0]:.4f}, end={final:.4f}, ratio={final/target:.4f}")

    # Start from flat (should stay at flat)
    Q_flat = flat_config(lat)
    Q_opt_flat, hist_flat = gradient_ascent_lambda_max(lat, Q_flat, n_steps=40, lr=0.02)
    print(f"  From flat: start={hist_flat[0]:.4f}, end={hist_flat[-1]:.4f}")

    print(f"  Best found: {best_lmax:.4f}, ratio to 4d: {best_lmax/target:.4f}")

print("\n" + "=" * 70)
print("CROSS-TERM KERNEL OPERATOR NORM")
print("=" * 70)

rng = np.random.default_rng(123)
norms = []
for trial in range(1000):
    X = random_su2(rng)
    Y = random_su2(rng)
    Z = random_su2(rng)
    norm, F = cross_term_kernel_norm(X, Y, Z)
    norms.append(norm)

print(f"\nRandom X,Y,Z ∈ SU(2): 1000 trials")
print(f"  ||F||_op: max={max(norms):.4f}, mean={np.mean(norms):.4f}, min={min(norms):.4f}")
print(f"  At flat (X=Y=Z=I): ||F||_op = ", end="")
norm_flat, F_flat = cross_term_kernel_norm(np.eye(2), np.eye(2), np.eye(2))
print(f"{norm_flat:.4f}")
print(f"  F_flat = \n{np.round(F_flat, 4)}")

# What is the theoretical max of ||F||_op?
# For SU(2): F_{ab} = Re Tr(X iσ_a Y iσ_b Z)
# The 3x3 matrix F is related to the SO(3) rotation matrices of X, Y, Z.
# At flat: F = -2 I_3, ||F||_op = 2.

print("\n" + "=" * 70)
print("LAMBDA_MIN ANALYSIS (most negative eigenvalue)")
print("=" * 70)

for d in [2, 3, 4]:
    L = 2
    lat = Lattice(d, L)
    rng = np.random.default_rng(77 + d)

    print(f"\nd={d}, L={L}")

    lmins = []
    lmaxs = []
    for trial in range(200):
        Q = random_config(lat, rng)
        H = compute_hessian(lat, Q)
        evals = np.linalg.eigvalsh(H)
        lmins.append(evals[0])
        lmaxs.append(evals[-1])

    print(f"  200 random configs:")
    print(f"    lambda_min: min={min(lmins):.4f}, mean={np.mean(lmins):.4f}")
    print(f"    lambda_max: max={max(lmaxs):.4f}, mean={np.mean(lmaxs):.4f}")
    print(f"    lambda_max/4d: max={max(lmaxs)/(4*d):.4f}")

    # Anti-flat: all Q = exp(pi/2 * isigma_a) for various a
    Q_anti = [su2_exp(np.array([np.pi/2, 0, 0])) for _ in range(lat.nedges)]
    H_anti = compute_hessian(lat, Q_anti)
    evals_anti = np.linalg.eigvalsh(H_anti)
    print(f"  Anti-flat (Q=exp(iπσ₁/2)):")
    print(f"    lambda_min={evals_anti[0]:.4f}, lambda_max={evals_anti[-1]:.4f}")

    # Worst case for negative eigenvalue: gradient descent on lambda_min
    Q0 = random_config(lat, rng)
    H0 = compute_hessian(lat, Q0)
    print(f"  (Gradient descent on lambda_min skipped — use random survey)")

print("\n" + "=" * 70)
print("PERTURBATION FROM FLAT: EIGENVALUE RESPONSE")
print("=" * 70)

d = 4
L = 2
lat = Lattice(d, L)
rng = np.random.default_rng(999)

# Generate random perturbation direction
ne = lat.nedges
w = rng.normal(size=(ne, 3))
w /= np.linalg.norm(w)

epsilons = np.linspace(0, 2.0, 50)
Q_flat = flat_config(lat)

lmax_vs_eps = []
lmin_vs_eps = []

for eps in epsilons:
    Q_pert = [np.eye(2, dtype=complex) for _ in range(ne)]
    for e in range(ne):
        Q_pert[e] = su2_exp(eps * w[e])
    H = compute_hessian(lat, Q_pert)
    evals = np.linalg.eigvalsh(H)
    lmax_vs_eps.append(evals[-1])
    lmin_vs_eps.append(evals[0])

print(f"\nd={d}, L={L}: lambda_max along random perturbation from flat")
print(f"  eps=0: lambda_max={lmax_vs_eps[0]:.4f} (=4d={4*d})")

max_lmax = max(lmax_vs_eps)
max_eps = epsilons[np.argmax(lmax_vs_eps)]
print(f"  max lambda_max: {max_lmax:.4f} at eps={max_eps:.4f}")
print(f"  ratio to 4d: {max_lmax / (4*d):.6f}")

# Try 20 random directions
print(f"\n20 random perturbation directions:")
max_overall = 0
for trial in range(20):
    w = rng.normal(size=(ne, 3))
    w /= np.linalg.norm(w)

    best_this = 0
    for eps in np.linspace(0, 3.0, 60):
        Q_pert = [np.eye(2, dtype=complex) for _ in range(ne)]
        for e in range(ne):
            wmat = sum(w[e, a] * isigma[a] for a in range(3))
            Q_pert[e] = expm(eps * wmat)
        H = compute_hessian(lat, Q_pert)
        lmax = np.linalg.eigvalsh(H)[-1]
        best_this = max(best_this, lmax)

    max_overall = max(max_overall, best_this)
    if trial < 5 or best_this > 0.95 * 4 * d:
        print(f"  Dir {trial}: max lambda_max = {best_this:.4f} ({best_this/(4*d):.4f} of 4d)")

print(f"\n  Overall max across all directions: {max_overall:.4f} ({max_overall/(4*d):.4f} of 4d)")
print(f"  BOUND HOLDS: {max_overall <= 4*d + 0.01}")
