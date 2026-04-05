"""
Practical combined analysis: zero trajectories, Fisher information,
entropy production, and monotone functionals.

Key insight from the phase transition script: under the BACKWARD heat flow,
the minimum gap INCREASES (zeros spread apart). This is correct because:
- Forward t: zeros REPEL (spread out)
- Backward t: with the ODE dx/dt = -sum 1/(x_k - x_j), going backward
  means the effective force is ATTRACTIVE... but wait, the results showed
  gaps INCREASING going backward. Let me understand this.

Actually, re-reading the N-body result more carefully:
t = 0.000: min_gap = 0.845 (pair 34,35)
t = -0.050: min_gap = 0.940
t = -0.100: min_gap = 1.023
...
t = -0.500: min_gap = 1.469

The gap INCREASES as t goes negative. This seems counterintuitive for
"backward heat flow" where we expect collisions.

The resolution: the Coulomb ODE dx_k/dt = -sum 1/(x_k - x_j) gives
REPULSIVE dynamics in FORWARD time. Going BACKWARD in t means we're
UNDOING the repulsion, so zeros should COME TOGETHER.

But the numerical result shows they SPREAD. Something is off with the sign.

Let me reconsider. The de Bruijn-Newman heat flow:
H_t(z) = integral e^{tu^2} Phi(u) cos(zu) du

The parameter t acts as a Gaussian smoothing parameter. Increasing t
smooths the function more, which makes zeros of H_t move APART (repel).
So forward t = repulsion.

The Coulomb ODE for zeros of H_t:
dz_k/dt = -sum_{j!=k} 1/(z_k - z_j)

For z_{k+1} > z_k (consecutive zeros):
dz_{k+1}/dt has a term -1/(z_{k+1} - z_k) < 0 (pulls DOWN)
dz_k/dt has a term -1/(z_k - z_{k+1}) = +1/(z_{k+1} - z_k) > 0 (pushes UP)

So the gap d(z_{k+1} - z_k)/dt = ... let's compute:
d(gap)/dt = dz_{k+1}/dt - dz_k/dt
          = [-1/(z_{k+1}-z_k) - sum_{j!=k+1} 1/(z_{k+1}-z_j)]
            - [+1/(z_{k+1}-z_k) - sum_{j!=k} 1/(z_k - z_j)]
          = -2/(z_{k+1}-z_k) + [other terms]

The -2/(gap) term makes the gap DECREASE in forward time... that's ATTRACTION,
not repulsion!

Wait -- I think I have the sign wrong in the ODE. Let me check the literature.

The standard result (e.g., Csordas, Norfolk, Varga 1986):
If z_k(t) are the real zeros of H_t, they satisfy:
    dz_k/dt = sum_{j!=k} 1/(z_k - z_j)  [POSITIVE sign!]

NOT the negative sign I used! The positive sign gives REPULSION:
dz_{k+1}/dt - dz_k/dt = sum terms, with the dominant pairwise contribution
being 1/(z_{k+1}-z_k) - (-1/(z_{k+1}-z_k)) = 2/(z_{k+1}-z_k) > 0.

So the gap INCREASES in forward time. That's repulsion. Good.

With the WRONG sign (negative, as I coded), the dynamics is reversed:
forward t has attraction, backward t has repulsion. That explains why
in my simulation, going backward showed gaps increasing.

Let me redo everything with the CORRECT sign.
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.stats import gaussian_kde
import json
import time

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
x0 = np.array(zeta_zeros)


def coulomb_rhs_correct(t_param, x):
    """
    CORRECT Coulomb ODE for de Bruijn-Newman zeros:
    dz_k/dt = +sum_{j!=k} 1/(z_k - z_j)   [REPULSIVE in forward t]

    Including mirror zeros at -z_k (from symmetry of Xi):
    dz_k/dt = sum_{j!=k} 1/(z_k - z_j) + sum_{j} 1/(z_k + z_j)
    (The mirror at -z_j contributes 1/(z_k - (-z_j)) = 1/(z_k + z_j))
    Including the self-mirror: 1/(z_k + z_k) = 1/(2*z_k)
    """
    n = len(x)
    X = x.reshape(1, -1)

    # Direct interactions
    diff = x.reshape(-1, 1) - X
    np.fill_diagonal(diff, np.inf)
    sum_direct = np.sum(1.0 / diff, axis=1)  # POSITIVE sign = repulsion

    # Mirror interactions (including self-mirror)
    sum_mirrors = np.sum(1.0 / (x.reshape(-1, 1) + X), axis=1)

    return sum_direct + sum_mirrors


# ================================================================
# Test: verify the correct sign gives repulsion forward, attraction backward
# ================================================================

print("=== Sign verification ===\n")
v = coulomb_rhs_correct(0, x0)
print(f"First few velocities at t=0:")
for i in range(5):
    print(f"  v[{i}] = {v[i]:.6f}  (zero at {x0[i]:.6f})")

# The smallest zero should be pushed DOWN (toward its mirror) and the
# largest zero pushed UP (away from the cluster). Actually, all zeros
# should be repelled outward from the cluster center.
print(f"\nSign check: first zero velocity = {v[0]:.6f} (should be < 0, pushed toward lower end)")
print(f"Last zero velocity = {v[-1]:.6f} (should be > 0, pushed toward upper end)")
print(f"Middle zero velocity (#{N//2}) = {v[N//2]:.6f}")

# ================================================================
# Forward integration: zeros repel, gaps grow
# ================================================================

print("\n\n=== Forward integration (t: 0 -> 0.5) ===")
print("With CORRECT sign: zeros should repel.\n")

sol_fwd = solve_ivp(
    coulomb_rhs_correct, (0, 0.5), x0,
    method='DOP853', t_eval=np.linspace(0, 0.5, 101),
    rtol=1e-10, atol=1e-12,
)
print(f"Forward: success={sol_fwd.success}, reached t={sol_fwd.t[-1]:.4f}")

# Track gaps
print(f"\n{'t':>8s}  {'min_gap':>10s}  {'mean_gap':>10s}  {'pair':>8s}")
for idx in range(0, len(sol_fwd.t), 10):
    t_val = sol_fwd.t[idx]
    z = np.sort(sol_fwd.y[:, idx])
    gaps = np.diff(z)
    min_i = np.argmin(gaps)
    print(f"{t_val:8.3f}  {gaps[min_i]:10.6f}  {np.mean(gaps):10.6f}  ({min_i+1},{min_i+2})")


# ================================================================
# Backward integration: zeros attract, gaps shrink, collisions happen
# ================================================================

print("\n\n=== Backward integration (t: 0 -> -0.3) ===")
print("With CORRECT sign: zeros should attract and collide.\n")

def min_gap_event(t_param, x):
    """Detect when min gap approaches zero."""
    gaps = np.diff(np.sort(x))
    return np.min(gaps) - 0.005
min_gap_event.terminal = True
min_gap_event.direction = -1

sol_bwd = solve_ivp(
    coulomb_rhs_correct, (0, -0.3), x0,
    method='DOP853', t_eval=np.linspace(0, -0.3, 3001),
    rtol=1e-10, atol=1e-12,
    events=min_gap_event,
)

print(f"Backward: success={sol_bwd.success}, reached t={sol_bwd.t[-1]:.6f}")
if sol_bwd.t_events and len(sol_bwd.t_events[0]) > 0:
    tc = sol_bwd.t_events[0][0]
    print(f"\n*** COLLISION EVENT at t = {tc:.10f} ***")
    z_coll = np.sort(sol_bwd.y_events[0][0])
    gaps = np.diff(z_coll)
    min_i = np.argmin(gaps)
    print(f"Colliding pair: ({min_i+1}, {min_i+2})")
    print(f"Positions: z_{min_i+1} = {z_coll[min_i]:.10f}, z_{min_i+2} = {z_coll[min_i+1]:.10f}")
    print(f"Gap at collision: {gaps[min_i]:.10f}")

# Track gaps during backward evolution
print(f"\n{'t':>10s}  {'min_gap':>10s}  {'pair':>8s}  {'2nd_gap':>10s}  {'pair2':>8s}")
step = max(1, len(sol_bwd.t) // 40)
for idx in range(0, len(sol_bwd.t), step):
    t_val = sol_bwd.t[idx]
    z = np.sort(sol_bwd.y[:, idx])
    gaps = np.diff(z)
    si = np.argsort(gaps)
    print(f"{t_val:10.6f}  {gaps[si[0]]:10.6f}  ({si[0]+1},{si[0]+2})  "
          f"{gaps[si[1]]:10.6f}  ({si[1]+1},{si[1]+2})")


# ================================================================
# Fisher information and entropy along the heat flow
# ================================================================

print("\n\n=== Fisher information and entropy vs t ===\n")

def compute_fisher_entropy(zeros, bw=2.0, x_lo=5, x_hi=155, n_pts=2000):
    """KDE-based Fisher information and entropy."""
    x = np.linspace(x_lo, x_hi, n_pts)
    dx = x[1] - x[0]

    rho = np.zeros(n_pts)
    drho = np.zeros(n_pts)
    for z in zeros:
        u = (x - z) / bw
        g = np.exp(-0.5 * u**2) / (bw * np.sqrt(2*np.pi))
        rho += g
        drho += g * (-u / bw)

    rho /= len(zeros)
    drho /= len(zeros)

    # Normalize
    norm = np.sum(rho) * dx
    rho /= norm
    drho /= norm

    mask = rho > 1e-30
    fisher = np.sum(drho[mask]**2 / rho[mask]) * dx
    entropy = -np.sum(rho[mask] * np.log(rho[mask])) * dx

    return fisher, entropy


def compute_perturbative_fisher(zeros, beta=2.0):
    """Perturbative Fisher info with all sigma=1/2."""
    return sum(2 * (g**2 + 0.25) / beta for g in zeros)


# Combine forward and backward solutions
print("Computing statistics along the full t range...\n")

all_data = {"t": [], "fisher_kde": [], "entropy": [], "fisher_pert": [],
            "min_gap": [], "mean_gap": [], "electrostatic_energy": []}

# Backward data
for idx in range(len(sol_bwd.t)-1, 0, -max(1, len(sol_bwd.t)//25)):
    t_val = sol_bwd.t[idx]
    z = sol_bwd.y[:, idx]
    F, S = compute_fisher_entropy(z)
    Fp = compute_perturbative_fisher(z)
    gaps = np.diff(np.sort(z))

    # Electrostatic energy
    z_s = np.sort(z)
    E = 0
    for k in range(len(z_s)):
        for j in range(k+1, len(z_s)):
            E -= np.log(z_s[j] - z_s[k])

    all_data["t"].append(float(t_val))
    all_data["fisher_kde"].append(float(F))
    all_data["entropy"].append(float(S))
    all_data["fisher_pert"].append(float(Fp))
    all_data["min_gap"].append(float(np.min(gaps)))
    all_data["mean_gap"].append(float(np.mean(gaps)))
    all_data["electrostatic_energy"].append(float(E))

# Forward data
for idx in range(0, len(sol_fwd.t), max(1, len(sol_fwd.t)//25)):
    t_val = sol_fwd.t[idx]
    z = sol_fwd.y[:, idx]
    F, S = compute_fisher_entropy(z)
    Fp = compute_perturbative_fisher(z)
    gaps = np.diff(np.sort(z))

    z_s = np.sort(z)
    E = 0
    for k in range(len(z_s)):
        for j in range(k+1, len(z_s)):
            E -= np.log(z_s[j] - z_s[k])

    all_data["t"].append(float(t_val))
    all_data["fisher_kde"].append(float(F))
    all_data["entropy"].append(float(S))
    all_data["fisher_pert"].append(float(Fp))
    all_data["min_gap"].append(float(np.min(gaps)))
    all_data["mean_gap"].append(float(np.mean(gaps)))
    all_data["electrostatic_energy"].append(float(E))

# Sort by t
sort_idx = np.argsort(all_data["t"])
for key in all_data:
    all_data[key] = [all_data[key][i] for i in sort_idx]

print(f"{'t':>8s}  {'F_kde':>10s}  {'entropy':>10s}  {'F_pert':>12s}  {'min_gap':>10s}  {'E_elec':>12s}")
for i in range(len(all_data["t"])):
    print(f"{all_data['t'][i]:8.4f}  {all_data['fisher_kde'][i]:10.6f}  "
          f"{all_data['entropy'][i]:10.6f}  {all_data['fisher_pert'][i]:12.2f}  "
          f"{all_data['min_gap'][i]:10.6f}  {all_data['electrostatic_energy'][i]:12.4f}")


# ================================================================
# de Bruijn's identity check: dS/dt = (1/2)*I(t)
# ================================================================

print("\n\n=== de Bruijn's identity check ===\n")
print("dS/dt should equal (1/2)*I(t) if the zero density evolution")
print("follows the heat equation. For the Coulomb ODE, this is approximate.\n")

t_arr = np.array(all_data["t"])
S_arr = np.array(all_data["entropy"])
F_arr = np.array(all_data["fisher_kde"])

# Numerical derivative
dSdt = np.gradient(S_arr, t_arr)
half_I = 0.5 * F_arr

print(f"{'t':>8s}  {'dS/dt':>12s}  {'I/2':>12s}  {'ratio':>10s}")
for i in range(len(t_arr)):
    ratio = dSdt[i] / half_I[i] if abs(half_I[i]) > 1e-10 else float('nan')
    print(f"{t_arr[i]:8.4f}  {dSdt[i]:12.6f}  {half_I[i]:12.6f}  {ratio:10.4f}")


# ================================================================
# Monotone functional check
# ================================================================

print("\n\n=== Monotone functional analysis ===\n")

# Check various candidates for monotonicity
F_arr = np.array(all_data["fisher_kde"])
S_arr = np.array(all_data["entropy"])
E_arr = np.array(all_data["electrostatic_energy"])
gap_arr = np.array(all_data["min_gap"])

candidates = {
    "Fisher (KDE)": F_arr,
    "Entropy": S_arr,
    "Electrostatic E": E_arr,
    "Min gap": gap_arr,
    "Mean gap": np.array(all_data["mean_gap"]),
    "F_pert": np.array(all_data["fisher_pert"]),
}

for name, arr in candidates.items():
    mono_inc = all(arr[i] <= arr[i+1] + 1e-10 for i in range(len(arr)-1))
    mono_dec = all(arr[i] >= arr[i+1] - 1e-10 for i in range(len(arr)-1))
    status = "INCREASING" if mono_inc else ("DECREASING" if mono_dec else "NON-MONOTONE")
    print(f"{name:20s}: {status}  [{arr[0]:.6f} -> {arr[-1]:.6f}]")


# ================================================================
# Summary: can we bound Lambda?
# ================================================================

print("\n\n" + "="*70)
print("SUMMARY: BACKWARD COLLISION ANALYSIS")
print("="*70 + "\n")

if sol_bwd.t_events and len(sol_bwd.t_events[0]) > 0:
    tc = sol_bwd.t_events[0][0]
    print(f"First collision detected at t = {tc:.10f}")
    print(f"This means: for the truncated 50-zero system,")
    print(f"all zeros are real for t >= {tc:.6f}")
    print(f"\nThe absolute value |t_c| = {abs(tc):.6f}")
    print(f"\nInterpretation:")
    print(f"- Lambda(50-zero system) = {tc:.6f}")
    print(f"- This is NOT a bound on the true Lambda (full system)")
    print(f"- The full system has additional zeros that modify the dynamics")
    print(f"- But it gives a QUALITATIVE picture of the scale of Lambda")

    # Compare with 2-body estimate
    closest_pair = sorted(
        [(i, zeta_zeros[i+1]-zeta_zeros[i]) for i in range(N-1)],
        key=lambda x: x[1]
    )[0]
    tc_2body = -closest_pair[1]**2 / 4
    print(f"\n2-body estimate for closest pair ({closest_pair[0]+1},{closest_pair[0]+2}):")
    print(f"  gap = {closest_pair[1]:.6f}, t_c(2-body) = {tc_2body:.6f}")
    print(f"  N-body t_c / 2-body t_c = {tc / tc_2body:.4f}")
else:
    print(f"No collision detected down to t = {sol_bwd.t[-1]:.6f}")
    print(f"The closest pair at that time:")
    z_final = np.sort(sol_bwd.y[:, -1])
    gaps = np.diff(z_final)
    min_i = np.argmin(gaps)
    print(f"  Pair ({min_i+1},{min_i+2}): gap = {gaps[min_i]:.8f}")

    # Extrapolate
    # Collect min_gap at several backward times
    t_bwd_arr = []
    gap_bwd_arr = []
    for idx in range(0, len(sol_bwd.t), max(1, len(sol_bwd.t)//50)):
        t_bwd_arr.append(sol_bwd.t[idx])
        z = np.sort(sol_bwd.y[:, idx])
        gap_bwd_arr.append(np.min(np.diff(z)))

    t_bwd_arr = np.array(t_bwd_arr)
    gap_bwd_arr = np.array(gap_bwd_arr)

    # Fit gap^2 vs t (Coulomb scaling)
    mask = t_bwd_arr < -0.01
    if np.sum(mask) > 3:
        coeffs = np.polyfit(t_bwd_arr[mask], gap_bwd_arr[mask]**2, 1)
        tc_est = -coeffs[1] / coeffs[0]
        print(f"\nLinear fit of gap^2 vs t: gap^2 = {coeffs[0]:.6f}*t + {coeffs[1]:.6f}")
        print(f"Extrapolated collision time: t_c ~ {tc_est:.6f}")


# Save all results
with open("/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/riemann-hypothesis/experiments/squeeze-lambda/practical_results.json", "w") as f:
    json.dump({
        "forward_reached": float(sol_fwd.t[-1]),
        "backward_reached": float(sol_bwd.t[-1]),
        "collision_detected": bool(sol_bwd.t_events and len(sol_bwd.t_events[0]) > 0),
        "collision_t": float(sol_bwd.t_events[0][0]) if sol_bwd.t_events and len(sol_bwd.t_events[0]) > 0 else None,
        "time_series": all_data,
    }, f, indent=2, default=str)

print("\nResults saved.")
