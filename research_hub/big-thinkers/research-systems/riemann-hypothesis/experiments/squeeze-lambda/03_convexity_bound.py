"""
Investigation 5: Using the proved convexity of I_pert(sigma) at sigma=1/2
to constrain zero migration and bound Lambda.

The proved result (Theorem 1) says:
   d^2 I_pert / d sigma^2 |_{sigma=1/2} = 4[(beta-1)^2 + 4t^2] / beta^3

This is the curvature of the perturbative Fisher information at the critical line.

Key insight: Under backward heat flow (t decreasing from 0), zeros can move off
sigma = 1/2. The rate of change of Fisher information as a zero moves off the
critical line is governed by this curvature.

If we can bound the RATE at which zeros move off sigma=1/2 (from the Coulomb ODE),
and use the curvature to bound the change in Fisher information, we might get
a constraint on how far t can go negative before the system reaches an inconsistency.

Approach:
1. For the Coulomb ODE in the s-variable (where s = sigma + i*gamma),
   the zero motion under backwards heat flow gives ds_k/dt = sum_{j!=k} 1/(s_k - s_j).

2. On the critical line, s_k = 1/2 + i*gamma_k. The real part motion:
   d(sigma_k)/dt = Re[sum_{j!=k} 1/(s_k - s_j)]

3. For zeros on the critical line:
   1/(s_k - s_j) = 1/(i(gamma_k - gamma_j)) = -i/(gamma_k - gamma_j)
   So d(sigma_k)/dt = Re[-i * sum_{j!=k} 1/(gamma_k - gamma_j)] = 0 !!

   This means zeros DO NOT move off the critical line under the heat flow
   if they start on it. The motion is purely along the imaginary axis.

4. This is consistent with the de Bruijn-Newman picture: for t >= Lambda,
   all zeros of H_t are real (in the z-variable). Since they're on the critical
   line in the s-variable for all t >= 0 (under the assumption that Lambda <= 0),
   the perturbative Fisher information at sigma=1/2 doesn't change its
   structural properties.

5. The ACTUAL mechanism by which Lambda > 0 would work:
   - The zeros of H_t are NOT simply the zeros of zeta moved along the critical line.
   - For H_t with t > 0, the zeros are real in z but have shifted positions.
   - The key is whether, as we decrease t toward 0, some pair of real zeros
     collides and goes complex.

Let me reframe this more carefully. In the z-variable:
- H_0(z) = Xi(1/2 + iz) has zeros at z = gamma_n (all real, assuming RH)
- H_t(z) for t > 0 also has only real zeros (since Lambda <= 0.2)
- H_t(z) for t < Lambda has some complex zeros

The zeros z_k(t) satisfy the Coulomb ODE (for real zeros):
   dz_k/dt = -sum_{j!=k} 1/(z_k - z_j)

For t >= Lambda, all z_k(t) are real. As t decreases to Lambda, some pair
z_k, z_{k+1} collides, and for t < Lambda they become a complex conjugate pair.

Now, the Fisher information of the zero distribution:
I_zeros(t) = integral [rho_t'(x)]^2 / rho_t(x) dx

where rho_t is the density of zeros of H_t.

Question: Can we prove I_zeros(t) is monotonically decreasing for t > 0,
and use this to characterize Lambda?

Alternative approach: The total electrostatic energy.
E(t) = -sum_{k<j} log|z_k(t) - z_j(t)|

Under the Coulomb ODE, dE/dt = sum_k (dz_k/dt)^2 >= 0.
So E(t) is monotonically INCREASING for t > 0 (zeros repel, energy increases).
And E(t) is monotonically DECREASING for t < 0 (zeros attract, approach collision).

At a collision (t = Lambda), E -> -infinity (log singularity).

Can we use this to bound Lambda?
"""

import numpy as np
from scipy.integrate import solve_ivp
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


def coulomb_rhs(t_param, x):
    """Vectorized Coulomb ODE including mirror zeros."""
    n = len(x)
    X = x.reshape(1, -1)
    diff = x.reshape(-1, 1) - X
    np.fill_diagonal(diff, np.inf)
    sum_pos = np.sum(-1.0 / diff, axis=1)
    sum_neg = np.sum(-1.0 / (x.reshape(-1, 1) + X), axis=1)
    return sum_pos + sum_neg


def compute_electrostatic_energy(zeros):
    """
    Coulomb energy: E = -sum_{k<j} log|z_k - z_j|
    Including mirror contributions: E_mirror = -sum_{k<=j} log|z_k + z_j|
    """
    n = len(zeros)
    E_direct = 0.0
    E_mirror = 0.0
    for k in range(n):
        for j in range(k+1, n):
            E_direct -= np.log(abs(zeros[k] - zeros[j]))
            E_mirror -= np.log(abs(zeros[k] + zeros[j]))
        # Self-mirror: k=j term
        E_mirror -= np.log(abs(2 * zeros[k]))
    return E_direct, E_mirror, E_direct + E_mirror


def compute_kinetic_energy(zeros):
    """
    Kinetic energy: K = sum_k (dz_k/dt)^2 = |coulomb_rhs|^2
    This equals dE/dt, the rate of energy dissipation.
    """
    v = coulomb_rhs(0, zeros)
    return np.sum(v**2)


def compute_perturbative_fisher_curvature(zeros, beta=2.0):
    """
    For each zero at 1/2 + i*gamma_n, the curvature of I_pert at sigma=1/2 is:
    d^2I/dsigma^2 = 4[(beta-1)^2 + 4*gamma_n^2] / beta^3

    Sum over all zeros for total curvature.
    """
    curvature_total = 0.0
    curvatures = []
    for gamma_n in zeros:
        c = 4.0 * ((beta - 1)**2 + 4 * gamma_n**2) / beta**3
        curvatures.append(c)
        curvature_total += c
    return curvature_total, curvatures


# ================================================================
# Compute electrostatic energy and kinetic energy along the heat flow
# ================================================================

print("=== Electrostatic energy along the heat flow ===\n")

x0 = np.array(zeta_zeros)

# Forward integration
t_values_fwd = np.linspace(0, 0.3, 301)
sol_fwd = solve_ivp(
    coulomb_rhs, (0, 0.3), x0,
    method='RK45', t_eval=t_values_fwd,
    rtol=1e-10, atol=1e-12,
    max_step=0.001
)
print(f"Forward: success={sol_fwd.success}, reached t={sol_fwd.t[-1]:.4f}")

# Backward integration
t_values_bwd = np.linspace(0, -0.2, 2001)
sol_bwd = solve_ivp(
    coulomb_rhs, (0, -0.2), x0,
    method='RK45', t_eval=t_values_bwd,
    rtol=1e-10, atol=1e-12,
    max_step=0.0002
)
print(f"Backward: success={sol_bwd.success}, reached t={sol_bwd.t[-1]:.4f}")

# Compute energy at sampled times
print(f"\n{'t':>10s}  {'E_direct':>14s}  {'E_total':>14s}  {'K(t)=dE/dt':>14s}  {'min_gap':>10s}")

energy_data = {"t": [], "E_direct": [], "E_total": [], "kinetic": [], "min_gap": []}

# Backward
step_bwd = max(1, len(sol_bwd.t) // 20)
for idx in range(len(sol_bwd.t)-1, -1, -step_bwd):
    t_val = sol_bwd.t[idx]
    z = sol_bwd.y[:, idx]
    E_d, E_m, E_tot = compute_electrostatic_energy(z)
    K = compute_kinetic_energy(z)
    gaps = np.diff(np.sort(z))
    min_gap = np.min(gaps)

    energy_data["t"].append(float(t_val))
    energy_data["E_direct"].append(float(E_d))
    energy_data["E_total"].append(float(E_tot))
    energy_data["kinetic"].append(float(K))
    energy_data["min_gap"].append(float(min_gap))

    print(f"{t_val:10.4f}  {E_d:14.6f}  {E_tot:14.6f}  {K:14.6f}  {min_gap:10.6f}")

# Forward (skip t=0 to avoid duplication)
step_fwd = max(1, len(sol_fwd.t) // 20)
for idx in range(step_fwd, len(sol_fwd.t), step_fwd):
    t_val = sol_fwd.t[idx]
    z = sol_fwd.y[:, idx]
    E_d, E_m, E_tot = compute_electrostatic_energy(z)
    K = compute_kinetic_energy(z)
    gaps = np.diff(np.sort(z))
    min_gap = np.min(gaps)

    energy_data["t"].append(float(t_val))
    energy_data["E_direct"].append(float(E_d))
    energy_data["E_total"].append(float(E_tot))
    energy_data["kinetic"].append(float(K))
    energy_data["min_gap"].append(float(min_gap))

    print(f"{t_val:10.4f}  {E_d:14.6f}  {E_tot:14.6f}  {K:14.6f}  {min_gap:10.6f}")


# ================================================================
# Fisher info curvature analysis
# ================================================================

print("\n\n=== Perturbative Fisher information curvature ===\n")

beta_values = [1.5, 2.0, 3.0, 5.0, 10.0]
for beta in beta_values:
    C_total, curvatures = compute_perturbative_fisher_curvature(zeta_zeros, beta)
    print(f"beta={beta}: total curvature = {C_total:.4f}")
    print(f"  First 5 individual curvatures: {[f'{c:.4f}' for c in curvatures[:5]]}")
    print(f"  Min curvature: {min(curvatures):.4f} (zero #{curvatures.index(min(curvatures))+1})")
    print(f"  Max curvature: {max(curvatures):.4f} (zero #{curvatures.index(max(curvatures))+1})")


# ================================================================
# Analysis: Can the energy or kinetic energy bound Lambda?
# ================================================================

print("\n\n=== Attempting to bound Lambda from energy considerations ===\n")

# Sort energy data by t
sorted_indices = np.argsort(energy_data["t"])
t_sorted = np.array(energy_data["t"])[sorted_indices]
E_sorted = np.array(energy_data["E_direct"])[sorted_indices]
K_sorted = np.array(energy_data["kinetic"])[sorted_indices]
gap_sorted = np.array(energy_data["min_gap"])[sorted_indices]

# Check monotonicity of energy
E_mono_inc = all(E_sorted[i] <= E_sorted[i+1] for i in range(len(E_sorted)-1))
print(f"E_direct monotonically increasing with t? {E_mono_inc}")

# Check monotonicity of kinetic energy
K_mono = all(K_sorted[i] >= K_sorted[i+1] for i in range(len(K_sorted)-1))
print(f"K = dE/dt monotonically decreasing with t? {K_mono}")

# The key question: does the minimum gap extrapolate to zero at some t < 0?
# If so, that gives an estimate of when the first collision occurs.
# Linear extrapolation of min_gap from the backward data:
bwd_mask = t_sorted < -0.01
if np.sum(bwd_mask) > 2:
    t_bwd = t_sorted[bwd_mask]
    gap_bwd = gap_sorted[bwd_mask]

    # Linear fit to min_gap vs t
    coeffs = np.polyfit(t_bwd, gap_bwd, 1)
    t_collision_linear = -coeffs[1] / coeffs[0]
    print(f"\nLinear extrapolation of min_gap to zero: t_collision ~ {t_collision_linear:.6f}")

    # Quadratic fit
    if len(t_bwd) > 3:
        coeffs2 = np.polyfit(t_bwd, gap_bwd, 2)
        # Solve quadratic: c2*t^2 + c1*t + c0 = 0
        disc = coeffs2[1]**2 - 4*coeffs2[0]*coeffs2[2]
        if disc >= 0:
            t1 = (-coeffs2[1] + np.sqrt(disc)) / (2*coeffs2[0])
            t2 = (-coeffs2[1] - np.sqrt(disc)) / (2*coeffs2[0])
            t_collision_quad = min(t for t in [t1, t2] if t < 0)
            print(f"Quadratic extrapolation: t_collision ~ {t_collision_quad:.6f}")


# ================================================================
# Analysis: Energy divergence rate near collision
# ================================================================

print("\n\n=== Energy behavior analysis ===\n")

# dE/dt = K(t) = sum of squared velocities
# Near a collision at t_c: gap ~ (t - t_c)^{1/2} (diffusive scaling)
# So K ~ 1/(t - t_c), and E ~ log(t - t_c) near collision

# Check: does K(t) grow as t -> t_c from above?
print(f"Kinetic energy at key backward times:")
for idx in sorted_indices:
    if energy_data["t"][idx] < 0:
        print(f"  t = {energy_data['t'][idx]:.4f}: K = {energy_data['kinetic'][idx]:.6f}, "
              f"min_gap = {energy_data['min_gap'][idx]:.6f}")


# ================================================================
# The convexity bound argument
# ================================================================

print("\n\n=== Convexity bound argument (Investigation 5) ===\n")

print("""
ANALYSIS: Can the proved convexity of I_pert(sigma) at sigma=1/2 bound Lambda?

The proved theorem states:
  d^2 I_pert / dsigma^2 |_{sigma=1/2} = 4[(beta-1)^2 + 4*gamma_n^2] / beta^3 > 0

This means the perturbative Fisher information has a STRICT minimum at sigma=1/2
for each zero pair.

However, for the heat flow, the relevant variable is NOT sigma (the real part
of the zero in the s-plane) but rather t (the heat flow parameter).

Key observation: On the critical line, all zeros have sigma = 1/2, and they
stay on the critical line under the heat flow (because the Coulomb force is
purely imaginary between zeros on a vertical line). So the curvature in sigma
is ORTHOGONAL to the heat flow direction.

The convexity in sigma tells us about stability of the critical line:
- Moving a zero off sigma = 1/2 increases I_pert
- This is an energy barrier against leaving the critical line

But this energy barrier is infinite-dimensional (all zeros must simultaneously
be considered), and the heat flow moves zeros along the line, not off it.

CONCLUSION: The proved convexity theorem characterizes the critical line as
an information-theoretic optimum (minimum Fisher information configuration)
but does NOT directly constrain the heat flow parameter t.

The connection to Lambda is indirect:
- Lambda = 0 means the zeros of H_0 are on the critical line
- The convexity theorem says this configuration is Fisher-optimal
- But Fisher optimality does not IMPLY real-rootedness

The fundamental limitation: Fisher information is a SECOND-ORDER quantity
(involving derivatives). The condition for all zeros to be real is a GLOBAL
topological constraint. No amount of local curvature analysis can capture
the global topology of the zero set.
""")


# Save results
output = {
    "energy_data": energy_data,
    "curvature_at_sigma_half": {},
}

for beta in beta_values:
    C, _ = compute_perturbative_fisher_curvature(zeta_zeros, beta)
    output["curvature_at_sigma_half"][str(beta)] = C

with open("/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/riemann-hypothesis/experiments/squeeze-lambda/convexity_bound_results.json", "w") as f:
    json.dump(output, f, indent=2)

print("Results saved to convexity_bound_results.json")
