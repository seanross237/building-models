"""
Deep analysis of the phase transition structure of F(t) and attempts to
bound Lambda using information-theoretic methods.

This script focuses on:

1. The BACKWARD heat flow with very fine resolution near t=0 to detect
   the onset of zero collisions.

2. Computing the "collision time" for each consecutive pair of zeros,
   treating them as a 2-body problem (ignoring other zeros).

3. Understanding whether the information-theoretic quantities have
   singular behavior at t = Lambda.

4. A careful analysis of why information-theoretic methods cannot
   improve on the Platt-Trudgian bound Lambda <= 0.2.
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import json

# First 50 zeta zeros
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

# ================================================================
# Analysis 1: Two-body collision times
# ================================================================

print("=== Two-body collision time analysis ===\n")
print("For each consecutive pair (gamma_k, gamma_{k+1}), compute the time")
print("at which they would collide under the 2-body Coulomb repulsion.\n")
print("The 2-body ODE: dx_1/dt = -1/(x_1-x_2) - 1/(x_1+x_2)")
print("                dx_2/dt = -1/(x_2-x_1) - 1/(x_2+x_1)\n")
print("For the RELATIVE coordinate r = x_2 - x_1 (with x_2 > x_1):")
print("  dr/dt = dx_2/dt - dx_1/dt = 2/(x_2-x_1) - [1/(x_2+x_1) - 1/(x_1+x_2)]")
print("        = 2/r + 0 = 2/r")
print("\nBut wait -- the mirror zero contributions don't exactly cancel.")
print("Actually: dx_k/dt = -1/(x_k - x_j) - 1/(x_k + x_j) for the 2-body problem")
print("(including only the mirror of the other zero, not one's own mirror).")
print("\nLet me redo this carefully with ALL mirror contributions.\n")

print("For zeros at x_1 and x_2 (with mirrors at -x_1 and -x_2):")
print("dx_1/dt = -1/(x_1-x_2) - 1/(x_1+x_2) - 1/(2*x_1)")
print("dx_2/dt = -1/(x_2-x_1) - 1/(x_2+x_1) - 1/(2*x_2)")
print()

# For the relative coordinate r = x_2 - x_1 and center c = (x_1 + x_2)/2:
# dr/dt = dx_2/dt - dx_1/dt = 2/r - [1/(2x_2) - 1/(2x_1)]
#       = 2/r - (x_1 - x_2)/(4*x_1*x_2)
#       = 2/r + r/(4*x_1*x_2)
# dc/dt = -(1/(2x_1) + 1/(2x_2))/2 = -(x_1+x_2)/(4x_1*x_2)

# For large x_1, x_2 >> r, the dominant term is 2/r (repulsion).
# For backward evolution (t going negative), dr/dt < 0 means r shrinks
# (but 2/r > 0 means repulsion pushes them apart for forward t).

# In the BACKWARD direction, we reverse time: dt -> -dt
# dr/d(-t) = -2/r - r/(4*x_1*x_2)
# Both terms are negative (for backward time), so r DECREASES.

# For the pure 2-body problem (r decreasing from r_0 at rate -2/r):
# r * dr = -2 dt => r^2/2 = -2t + C => r(t) = sqrt(r_0^2 - 4t)
# Collision at t = r_0^2 / 4 (measuring backward from t=0).

print("Pure 2-body collision times (ignoring other zeros and mirrors):")
print("For gap r_0, collision occurs at t_c = -r_0^2/4 (backward from t=0).\n")

print(f"{'pair':>8s}  {'gamma_k':>12s}  {'gamma_{k+1}':>12s}  {'gap r_0':>10s}  {'t_c = -r^2/4':>14s}")
print("-" * 70)

collision_times_2body = []
for k in range(N-1):
    r0 = zeta_zeros[k+1] - zeta_zeros[k]
    tc = -r0**2 / 4.0
    collision_times_2body.append({
        "pair": (k+1, k+2),
        "gamma_k": zeta_zeros[k],
        "gamma_kp1": zeta_zeros[k+1],
        "gap": r0,
        "tc_2body": tc,
    })
    print(f"({k+1:2d},{k+2:2d})  {zeta_zeros[k]:12.6f}  {zeta_zeros[k+1]:12.6f}  {r0:10.6f}  {tc:14.8f}")

# Find the LATEST collision time (closest to 0, i.e., first to collide going backward)
collision_times_2body.sort(key=lambda x: x["tc_2body"], reverse=True)
print(f"\nFirst pair to collide (backward): ({collision_times_2body[0]['pair'][0]}, "
      f"{collision_times_2body[0]['pair'][1]})")
print(f"Gap: {collision_times_2body[0]['gap']:.6f}")
print(f"Collision time (2-body): t_c = {collision_times_2body[0]['tc_2body']:.8f}")
print(f"\nNote: This is an UNDERESTIMATE of |t_c| because the mirror zero")
print(f"contributions and other-zero contributions provide additional repulsion.")

# ================================================================
# Analysis 2: Including mirror effects in 2-body estimate
# ================================================================

print("\n\n=== Improved 2-body estimates with mirror zeros ===\n")

# For zeros at x_1, x_2 with x_1 approx = x_2 approx = gamma (midpoint):
# The mirror contribution to dr/dt is r/(4*x_1*x_2) ~ r/(4*gamma^2)
# So dr/dt = 2/r + r/(4*gamma^2) (forward time)
# In backward time: dr/dt = -2/r - r/(4*gamma^2)

# Solving: r * dr / (2 + r^2/(4*gamma^2)) = -dt
# Let u = r^2: du/(2*(2 + u/(4*gamma^2))) = -dt
# du / (4 + u/(2*gamma^2)) = -dt
# (2*gamma^2) * du / (8*gamma^2 + u) = -dt
# 2*gamma^2 * log(8*gamma^2 + u) = -t + C

# At t=0: 2*gamma^2 * log(8*gamma^2 + r_0^2) = C
# At t_c (r=0): 2*gamma^2 * log(8*gamma^2) = -t_c + C
# t_c = -2*gamma^2 * [log(8*gamma^2 + r_0^2) - log(8*gamma^2)]
#      = -2*gamma^2 * log(1 + r_0^2/(8*gamma^2))

# For r_0 << gamma (which is typical): t_c ~ -2*gamma^2 * r_0^2/(8*gamma^2) = -r_0^2/4
# The correction is second order in r_0/gamma.

print("Improved collision times (with mirror correction):")
print(f"{'pair':>8s}  {'gap':>10s}  {'gamma_mid':>10s}  {'tc_pure':>14s}  {'tc_improved':>14s}  {'correction':>10s}")

for item in collision_times_2body[:10]:
    k = item["pair"][0] - 1
    gamma_mid = (zeta_zeros[k] + zeta_zeros[k+1]) / 2
    r0 = item["gap"]
    tc_pure = -r0**2 / 4.0
    tc_improved = -2 * gamma_mid**2 * np.log(1 + r0**2 / (8 * gamma_mid**2))
    correction = (tc_improved - tc_pure) / abs(tc_pure) * 100
    print(f"({item['pair'][0]:2d},{item['pair'][1]:2d})  {r0:10.6f}  {gamma_mid:10.4f}  "
          f"{tc_pure:14.8f}  {tc_improved:14.8f}  {correction:+9.4f}%")


# ================================================================
# Analysis 3: Full N-body backward integration with collision tracking
# ================================================================

print("\n\n=== Full N-body backward integration ===\n")
print("Integrating the full Coulomb ODE backward from t=0.\n")

def coulomb_rhs_full(t_param, x):
    """Full N-body Coulomb ODE with mirrors."""
    n = len(x)
    X = x.reshape(1, -1)
    diff = x.reshape(-1, 1) - X
    np.fill_diagonal(diff, np.inf)
    sum_pos = np.sum(-1.0 / diff, axis=1)
    sum_neg = np.sum(-1.0 / (x.reshape(-1, 1) + X), axis=1)
    return sum_pos + sum_neg

x0 = np.array(zeta_zeros)

# Track all consecutive gaps during backward evolution
def track_gaps(t_param, x):
    """Return minimum gap minus threshold."""
    x_sorted = np.sort(x)
    gaps = np.diff(x_sorted)
    return np.min(gaps) - 0.001

track_gaps.terminal = True
track_gaps.direction = -1

# Very fine backward integration
print("Starting backward integration with fine stepping...")
t_bwd = np.linspace(0, -0.5, 5001)
sol = solve_ivp(
    coulomb_rhs_full, (0, -0.5), x0,
    method='RK45', t_eval=t_bwd,
    rtol=1e-11, atol=1e-13,
    max_step=0.0001,
    events=track_gaps,
)

print(f"Integration: success={sol.success}, reached t={sol.t[-1]:.6f}")
if sol.t_events and len(sol.t_events[0]) > 0:
    print(f"COLLISION at t = {sol.t_events[0][0]:.10f}")

# Track the minimum gap and which pair it corresponds to
print(f"\n{'t':>10s}  {'min_gap':>12s}  {'pair':>8s}  {'2nd_min_gap':>12s}  {'pair2':>8s}")
step = max(1, len(sol.t) // 30)
min_gap_history = []
for idx in range(0, len(sol.t), step):
    t_val = sol.t[idx]
    z = np.sort(sol.y[:, idx])
    gaps = np.diff(z)
    sorted_gap_indices = np.argsort(gaps)

    min_i = sorted_gap_indices[0]
    min_gap = gaps[min_i]
    sec_i = sorted_gap_indices[1]
    sec_gap = gaps[sec_i]

    min_gap_history.append((float(t_val), float(min_gap), int(min_i)+1))

    if idx % (step * 3) == 0 or t_val < -0.3:
        print(f"{t_val:10.6f}  {min_gap:12.8f}  ({min_i+1:2d},{min_i+2:2d})  "
              f"{sec_gap:12.8f}  ({sec_i+1:2d},{sec_i+2:2d})")


# ================================================================
# Analysis 4: Extrapolate collision time from N-body dynamics
# ================================================================

print("\n\n=== Extrapolating collision time from N-body dynamics ===\n")

# Use the min_gap data to extrapolate
t_data = np.array([x[0] for x in min_gap_history])
gap_data = np.array([x[1] for x in min_gap_history])

# For Coulomb repulsion, gap ~ sqrt(t_c - t), so gap^2 ~ -(t - t_c)
# Fit gap^2 vs t linearly
mask = t_data < -0.01
if np.sum(mask) > 5:
    t_fit = t_data[mask]
    gap2_fit = gap_data[mask]**2

    # Linear fit: gap^2 = a*t + b, collision at t_c = -b/a
    coeffs = np.polyfit(t_fit, gap2_fit, 1)
    tc_linear = -coeffs[1] / coeffs[0]
    print(f"Linear fit of gap^2 vs t: gap^2 = {coeffs[0]:.6f}*t + {coeffs[1]:.6f}")
    print(f"Extrapolated collision: t_c = {tc_linear:.8f}")

    # Quadratic fit
    coeffs2 = np.polyfit(t_fit, gap2_fit, 2)
    # Solve quadratic
    disc = coeffs2[1]**2 - 4*coeffs2[0]*coeffs2[2]
    if disc >= 0:
        t1 = (-coeffs2[1] + np.sqrt(disc)) / (2*coeffs2[0])
        t2 = (-coeffs2[1] - np.sqrt(disc)) / (2*coeffs2[0])
        tc_candidates = [t for t in [t1, t2] if t < 0]
        if tc_candidates:
            tc_quad = max(tc_candidates)
            print(f"Quadratic fit: t_c = {tc_quad:.8f}")

    # Gap^2 vs t plot data
    print(f"\n{'t':>10s}  {'gap^2':>14s}  {'gap':>12s}")
    for i in range(len(t_fit)):
        print(f"{t_fit[i]:10.4f}  {gap2_fit[i]:14.8f}  {gap_data[mask][i]:12.8f}")


# ================================================================
# Analysis 5: Connection to Lambda bounds
# ================================================================

print("\n\n=== Connection to Lambda bounds ===\n")

# The key question: if the first 50 zeros have collision time t_c (from the
# N-body ODE), does this give us Lambda?

# Answer: NO, because:
# 1. Lambda is defined for the FULL system (infinitely many zeros)
# 2. The truncated system misses the contributions from the infinitely many
#    zeros beyond the 50th
# 3. Additional zeros INCREASE repulsion (more particles pushing), which
#    DELAYS collisions (makes t_c more negative)

# So the truncated collision time is an OVERESTIMATE of Lambda:
# Lambda <= t_c(N) + truncation_error

# But we can estimate the truncation error:
# The extra zeros beyond N contribute a force on the k-th zero:
# F_extra = sum_{j>N} [1/(gamma_k - gamma_j) + 1/(gamma_k + gamma_j)]
# For the closest pair (around gamma ~ 30-60), this force is:
# F ~ sum_{j>50} 2*gamma_k / (gamma_j^2 - gamma_k^2) (for gamma_j >> gamma_k)
# ~ integral from gamma_50 to infinity of 2*gamma_k / (gamma^2 - gamma_k^2) d(N(gamma))
# where N(gamma) ~ gamma/(2*pi) * log(gamma/(2*pi)) is the zero counting function.

# This is a small correction because the distant zeros provide a nearly
# uniform background force.

print("The truncated zero model (first 50 zeros) provides a qualitative")
print("picture of the zero dynamics but CANNOT give a rigorous bound on Lambda.")
print()
print("Reasons:")
print("1. Lambda is defined for the full (infinite) system")
print("2. Truncation introduces boundary effects")
print("3. The missing zeros change the collective dynamics")
print("4. The Coulomb ODE is derived heuristically; the rigorous connection")
print("   between the ODE and the de Bruijn-Newman family requires careful")
print("   estimates on the remainder terms")
print()
print("What WOULD be needed for a rigorous bound:")
print("- Verify that the first M zeros of H_t are real at t = t_0 (direct computation)")
print("- Bound the remaining zeros using analytic estimates (zero-free region arguments)")
print("- This is exactly the Platt-Trudgian approach (their Lambda <= 0.2 uses")
print("  verified zeros up to height T ~ 3 * 10^10 combined with analytic bounds)")
print()
print("Information-theoretic methods CANNOT bypass this because:")
print("- Fisher information and entropy are GLOBAL statistical quantities")
print("- They average over the zero distribution")
print("- Lambda depends on the LOCAL behavior of individual zero pairs")
print("- A single close pair can dominate Lambda while having negligible")
print("  effect on global statistics")


# ================================================================
# Save results
# ================================================================

results = {
    "two_body_collision_times": collision_times_2body[:20],
    "n_body_collision_tracking": min_gap_history,
    "n_body_final_t": float(sol.t[-1]),
}

if sol.t_events and len(sol.t_events[0]) > 0:
    results["n_body_collision_t"] = float(sol.t_events[0][0])

with open("/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/riemann-hypothesis/experiments/squeeze-lambda/phase_transition_results.json", "w") as f:
    json.dump(results, f, indent=2, default=str)

print("\nResults saved to phase_transition_results.json")
