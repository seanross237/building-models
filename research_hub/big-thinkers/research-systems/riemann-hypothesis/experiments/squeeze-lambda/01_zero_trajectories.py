"""
Investigation 4: Zero trajectories under the de Bruijn-Newman heat flow.

The zeros of H_t satisfy an ODE system (electrostatic/Coulomb analogy):
    dz_k/dt = -sum_{j != k} 1/(z_k - z_j)

Starting from the known zeta zeros on the critical line (z_k = gamma_k for the
upper-half zeros, where rho_k = 1/2 + i*gamma_k), we integrate forward in t.

Key questions:
- At what t do first zeros collide (merge onto the real axis)?
- Can we extract an upper bound on Lambda from the dynamics?
- What is the structure of the zero flow?

NOTE: For zeros on the critical line, by symmetry the motion is purely vertical
(along the imaginary axis) initially. Zeros can only move off the line through
collisions. The actual mechanism for Lambda > 0 would be zeros of H_t that
start complex and migrate to become real as t increases.

For H_t, the zeros at t=0 are at z = gamma_n (the imaginary parts of the zeta
zeros; the Xi function zeros are at z = gamma_n on the real line in the z-variable).
Wait -- let me be more careful about conventions.

The Riemann Xi function: Xi(s) = Xi(1/2 + iz) = H_0(z)
So the zeros of H_0 are at z = gamma_n (real!) where rho_n = 1/2 + i*gamma_n.

Under the heat flow, for t > 0, zeros of H_t remain real (since Lambda <= 0.2
and we're going positive t). For t < 0, some zeros become complex.

So the interesting direction for bounding Lambda is:
- For t < 0, track when zeros first leave the real axis (become complex pairs)
- Lambda is the supremum of |t| for which H_t still has only real zeros
  when approaching from positive t.

Actually, the correct statement: Lambda = inf{t : H_s has only real zeros for all s >= t}.
So for t >= Lambda, H_t has only real zeros.
For t < Lambda, H_t has at least one non-real zero.

Since Lambda >= 0 (Rodgers-Tao) and Lambda <= 0.2 (Platt-Trudgian),
the zeros of H_0 = Xi ARE all real (this IS the RH, which is not proved but
consistent with Lambda >= 0 -- actually Lambda >= 0 does NOT prove RH!
Lambda >= 0 means the zeros of H_0 could still be complex.)

Wait, let me reconsider. Lambda >= 0 means:
- For all t >= 0, H_t has only real zeros (since t >= Lambda >= 0... no, Lambda >= 0
  means Lambda could be 0 or positive).
- Lambda >= 0 means: for t >= Lambda (which is >= 0), H_t has real zeros.
- RH is Lambda = 0, meaning H_0 has all real zeros.
- If Lambda > 0, then H_0 could have complex zeros.

For the ODE approach:
Starting from t large enough (say t = 0.2 >= Lambda), all zeros of H_t are real.
As we decrease t toward 0, at t = Lambda, the first pair of zeros collides and
would go complex for t < Lambda.

But we can also approach this differently: start from the known (numerically)
real zeros of H_0 (the zeta zeros on the critical line) and track the ODE
forward and backward.

Let me focus on the Coulomb ODE for the zeros. If x_1, x_2, ..., x_N are the
N real zeros of H_t (in the z variable), then:

    dx_k/dt = -sum_{j != k} 1/(x_k - x_j)

This is for real zeros. When two zeros x_k and x_{k+1} collide, they form a
complex conjugate pair for t slightly less than the collision time.

Strategy: Start from the first 50 zeta zeros (gamma_1, ..., gamma_50) as initial
conditions at t = 0. Integrate the ODE BACKWARD in t (toward negative t).
As t decreases from 0, the zeros will approach each other, and at some t_c < 0,
the first pair will collide. This means H_{t_c} has a double real zero, and for
t < t_c it splits into a complex pair.

Actually -- for bounding Lambda from above, we should go FORWARD from t=0.
The zeros should spread out (repel each other), becoming "more real" in some sense.

For bounding Lambda, the key insight is different. Lambda = inf{t : all zeros real
for s >= t}. If we can show that starting from some configuration at t = t_0,
the ODE ensures all zeros remain real for all t >= t_0, then Lambda <= t_0.

The standard approach (used by e.g., Polymath 15) is:
1. Verify that the first N zeros of H_{t_0} are real for some t_0.
2. Show that the remaining zeros (beyond the first N) are also real at t_0.
3. By de Bruijn monotonicity, Lambda <= t_0.

Let me implement the Coulomb ODE and study the dynamics.
"""

import numpy as np
from scipy.integrate import solve_ivp
import json
import time

# First 50 nontrivial zeta zeros (imaginary parts)
# These are well-known to high precision
zeta_zeros = [
    14.134725141734693, 21.022039638771555, 25.010857580145688,
    30.424876125859513, 32.935061587739189, 37.586178158825671,
    40.918719012147495, 43.327073280914999, 48.005150881167159,
    49.773832477672302, 52.970321477714460, 56.446247697063394,
    59.347044002602353, 60.831778524609809, 65.112544048081606,
    67.079810529494173, 69.546401711173979, 72.067157674481907,
    75.704690699083933, 77.144840068874805, 79.337375020249367,
    82.910380854086030, 84.735492980517050, 87.425274613125229,
    88.809111207634465, 92.491899270558484, 94.651344040519838,
    95.870634228245309, 98.831194218193692, 101.31785100573139,
    103.72553804532511, 105.44662305232542, 107.16861118427640,
    111.02953554316967, 111.87465917699263, 114.32022091545271,
    116.22668032085755, 118.79078286597621, 121.37012500242066,
    122.94682929355258, 124.25681855434576, 127.51668387959649,
    129.57870419995605, 131.08768853093265, 133.49773720299758,
    134.75650975337387, 138.11604205453344, 139.73620895212138,
    141.12370740402112, 143.11184580762063,
]

N = len(zeta_zeros)
print(f"Working with {N} zeta zeros")
print(f"First zero: gamma_1 = {zeta_zeros[0]:.6f}")
print(f"Last zero: gamma_{N} = {zeta_zeros[-1]:.6f}")


def coulomb_rhs(t_param, x):
    """
    Right-hand side of the Coulomb ODE for real zeros:
    dx_k/dt = -sum_{j != k} 1/(x_k - x_j)

    We include the "mirror" zeros at -gamma_n (by symmetry of Xi).
    So the full system has zeros at +gamma_n and -gamma_n.

    For a zero at x_k > 0, the contribution from its mirror at -x_k is:
    -1/(x_k - (-x_k)) = -1/(2*x_k)

    The contribution from zero at x_j (j != k) and its mirror at -x_j:
    -1/(x_k - x_j) - 1/(x_k + x_j)
    """
    n = len(x)
    dxdt = np.zeros(n)

    for k in range(n):
        # Mirror image contribution
        s = -1.0 / (2.0 * x[k])

        for j in range(n):
            if j == k:
                continue
            diff_pos = x[k] - x[j]
            diff_neg = x[k] + x[j]

            if abs(diff_pos) < 1e-10:
                # Zeros about to collide -- use regularization
                s += -np.sign(diff_pos) * 1e10
            else:
                s += -1.0 / diff_pos

            if abs(diff_neg) < 1e-10:
                s += -np.sign(diff_neg) * 1e10
            else:
                s += -1.0 / diff_neg

        dxdt[k] = s

    return dxdt


def coulomb_rhs_vectorized(t_param, x):
    """Vectorized version for speed."""
    n = len(x)
    X = x.reshape(1, -1)  # 1 x n

    # Differences: diff[k,j] = x[k] - x[j]
    diff = x.reshape(-1, 1) - X  # n x n

    # Set diagonal to inf to avoid division by zero
    np.fill_diagonal(diff, np.inf)

    # Contributions from positive zeros
    contrib_pos = -1.0 / diff  # n x n

    # Sum over j for each k (exclude diagonal)
    sum_pos = np.sum(contrib_pos, axis=1)

    # Contributions from negative mirrors: -1/(x_k + x_j)
    sum_neg_mirrors = x.reshape(-1, 1) + X  # n x n, all positive for positive zeros
    contrib_neg = -1.0 / sum_neg_mirrors
    # Include k=j term: -1/(2*x_k), which is already in sum_neg_mirrors diagonal
    sum_neg = np.sum(contrib_neg, axis=1)

    return sum_pos + sum_neg


# Initial conditions: the zeta zeros
x0 = np.array(zeta_zeros)

print("\n=== Forward integration (t: 0 -> 0.5) ===")
print("Zeros should repel and spread out.\n")

# Forward integration
t_span_fwd = (0, 0.5)
t_eval_fwd = np.linspace(0, 0.5, 501)

start_time = time.time()
sol_fwd = solve_ivp(
    coulomb_rhs_vectorized, t_span_fwd, x0,
    method='RK45', t_eval=t_eval_fwd,
    rtol=1e-10, atol=1e-12,
    max_step=0.001
)
elapsed = time.time() - start_time

print(f"Integration completed in {elapsed:.1f}s")
print(f"Success: {sol_fwd.success}")
if not sol_fwd.success:
    print(f"Message: {sol_fwd.message}")
print(f"Number of time steps evaluated: {len(sol_fwd.t)}")

# Analyze the forward solution
if sol_fwd.success or len(sol_fwd.t) > 10:
    t_max = sol_fwd.t[-1]
    print(f"\nReached t = {t_max:.6f}")

    # Track zero spacings
    print("\nZero spacings (first 10 consecutive pairs):")
    print(f"{'t':>8s}  {'gap_1':>10s}  {'gap_2':>10s}  {'gap_3':>10s}  {'gap_4':>10s}  {'gap_5':>10s}")

    for idx in [0, len(sol_fwd.t)//4, len(sol_fwd.t)//2, 3*len(sol_fwd.t)//4, -1]:
        t_val = sol_fwd.t[idx]
        zeros_at_t = sol_fwd.y[:, idx]
        gaps = np.diff(sorted(zeros_at_t))[:5]
        gap_str = "  ".join(f"{g:10.6f}" for g in gaps)
        print(f"{t_val:8.4f}  {gap_str}")

    # Check if any zeros crossed
    print("\n\nZero positions at key times:")
    for idx in [0, -1]:
        t_val = sol_fwd.t[idx]
        zeros_at_t = sorted(sol_fwd.y[:, idx])
        print(f"\nt = {t_val:.4f}:")
        for i in range(min(10, N)):
            print(f"  z_{i+1} = {zeros_at_t[i]:.10f}  (started at {zeta_zeros[i]:.10f})")


print("\n\n=== Backward integration (t: 0 -> -0.3) ===")
print("Zeros should attract and some may collide.\n")

# Backward integration -- this is where we look for collisions
t_span_bwd = (0, -0.3)
t_eval_bwd = np.linspace(0, -0.3, 3001)

# Use event detection for collisions
def collision_event(t_param, x):
    """Detect when minimum gap between consecutive zeros approaches zero."""
    x_sorted = np.sort(x)
    gaps = np.diff(x_sorted)
    return np.min(gaps) - 0.01  # Trigger when gap < 0.01

collision_event.terminal = True
collision_event.direction = -1

start_time = time.time()
sol_bwd = solve_ivp(
    coulomb_rhs_vectorized, t_span_bwd, x0,
    method='RK45', t_eval=t_eval_bwd,
    rtol=1e-10, atol=1e-12,
    max_step=0.0005,
    events=collision_event
)
elapsed = time.time() - start_time

print(f"Integration completed in {elapsed:.1f}s")
print(f"Success: {sol_bwd.success}")
if not sol_bwd.success:
    print(f"Message: {sol_bwd.message}")
print(f"Number of time steps evaluated: {len(sol_bwd.t)}")

if hasattr(sol_bwd, 't_events') and sol_bwd.t_events and len(sol_bwd.t_events[0]) > 0:
    t_collision = sol_bwd.t_events[0][0]
    print(f"\n*** COLLISION DETECTED at t = {t_collision:.8f} ***")

    # Find which pair is colliding
    x_at_collision = sol_bwd.y_events[0][0]
    x_sorted = np.sort(x_at_collision)
    gaps = np.diff(x_sorted)
    min_gap_idx = np.argmin(gaps)
    print(f"Colliding zeros: z_{min_gap_idx+1} = {x_sorted[min_gap_idx]:.8f}, z_{min_gap_idx+2} = {x_sorted[min_gap_idx+1]:.8f}")
    print(f"Gap at collision: {gaps[min_gap_idx]:.10f}")

# Track minimum gap over time
if len(sol_bwd.t) > 10:
    print("\nMinimum consecutive gap vs t (backward):")
    print(f"{'t':>10s}  {'min_gap':>12s}  {'pair':>6s}")

    step = max(1, len(sol_bwd.t) // 20)
    for idx in range(0, len(sol_bwd.t), step):
        t_val = sol_bwd.t[idx]
        zeros_at_t = np.sort(sol_bwd.y[:, idx])
        gaps = np.diff(zeros_at_t)
        min_idx = np.argmin(gaps)
        min_gap = gaps[min_idx]
        print(f"{t_val:10.6f}  {min_gap:12.8f}  ({min_idx+1},{min_idx+2})")


# Save results
results = {
    "n_zeros": N,
    "zeta_zeros": zeta_zeros,
    "forward": {
        "t_range": [0, float(sol_fwd.t[-1])],
        "success": bool(sol_fwd.success),
    },
    "backward": {
        "t_range": [0, float(sol_bwd.t[-1])],
        "success": bool(sol_bwd.success),
    }
}

# Add collision info if found
if hasattr(sol_bwd, 't_events') and sol_bwd.t_events and len(sol_bwd.t_events[0]) > 0:
    results["backward"]["collision_t"] = float(sol_bwd.t_events[0][0])

with open("/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/riemann-hypothesis/experiments/squeeze-lambda/zero_trajectories_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nResults saved.")
