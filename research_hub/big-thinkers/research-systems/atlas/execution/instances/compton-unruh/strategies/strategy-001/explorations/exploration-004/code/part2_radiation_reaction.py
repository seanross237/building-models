"""
Part 2: Vacuum Fluctuation Force (Radiation Reaction) in de Sitter

We compute the radiation reaction force experienced by an accelerating
particle in the de Sitter vacuum, and determine whether the crossover
at a ~ cH0 modifies the force law.

The key physics:
1. An accelerating charge/detector in vacuum experiences a radiation reaction
   force (Abraham-Lorentz-Dirac force in flat space: F_ALD = mu_0*q^2*a_dot/(6*pi*c))
2. In a thermal bath at temperature T, there is an additional fluctuation-
   dissipation contribution
3. In de Sitter, the effective temperature is T_dS(a) = (hbar/(2*pi*c*kB))*sqrt(a^2+c^2*H^2)
4. The question: does the T_dS dependence modify the relationship between
   force and acceleration?

APPROACH: We use the fluctuation-dissipation framework, NOT the ALD force directly.
The ALD force is about radiation emission; we need the FULL balance including
vacuum fluctuation absorption.

Following Sciama, Candelas & Deutsch (1981), and Parentani (1995):
The net force on an accelerating detector in a thermal state includes
contributions from both radiation reaction and vacuum fluctuations.
In the Unruh state, these cancel exactly — the detector is in thermal
equilibrium at T_U. But in de Sitter, the equilibrium is at T_dS.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import integrate
import os

OUTDIR = os.path.dirname(os.path.abspath(__file__))

# Physical constants
hbar = 1.054571817e-34   # J*s
c = 2.99792458e8         # m/s
kB = 1.380649e-23        # J/K
G_N = 6.67430e-11        # m^3/(kg*s^2)
H0 = 2.2e-18             # 1/s
a0_MOND = 1.2e-10        # m/s^2
cH0 = c * H0
T_GH = hbar * H0 / (2 * np.pi * kB)
M_sun = 1.989e30

# Temperatures
T_U = lambda a: hbar * a / (2 * np.pi * c * kB)
T_dS = lambda a: hbar * np.sqrt(a**2/c**2 + H0**2) / (2 * np.pi * kB)

print("=" * 70)
print("Part 2: Radiation Reaction Force in de Sitter")
print("=" * 70)

# ======================================================================
# SECTION 2.1: Detector Response Function R(E, a)
# ======================================================================
print("\n" + "=" * 70)
print("Section 2.1: Detector Response Function R(E, a)")
print("=" * 70)

print("""
The Unruh-DeWitt detector transition rate for a massless scalar field
in a KMS (thermal) state at temperature T is:

  R(E, T) = (E/(2*pi*hbar)) * n_BE(E, T)

where n_BE(E, T) = 1/(exp(E/(kB*T)) - 1) is the Bose-Einstein distribution.

For Rindler (flat space): T = T_U(a) = hbar*a/(2*pi*c*kB)
  => R(E, a) = (E/(2*pi*hbar)) / (exp(2*pi*c*E/(hbar*a)) - 1)

For de Sitter: T = T_dS(a) = (hbar/(2*pi*c*kB))*sqrt(a^2 + c^2*H^2)
  => R(E, a) = (E/(2*pi*hbar)) / (exp(E/(kB*T_dS)) - 1)
  = (E/(2*pi*hbar)) / (exp(2*pi*c*E/(hbar*sqrt(a^2+c^2*H^2))) - 1)

The RATIO R_dS/R_Rindler measures the modification:
  R_dS/R_Rindler = [exp(E/kB*T_U) - 1] / [exp(E/kB*T_dS) - 1]
""")

# Compute response ratio for several energies
# Use dimensionless energy: x = E/(kB*T_GH)
a_range = np.logspace(-15, 0, 500)  # m/s^2

def response_ratio(a, x_dimless):
    """Ratio R_dS/R_Rindler at dimensionless energy x = E/(kB*T_GH)."""
    T_u = T_U(a)
    T_ds = T_dS(a)
    E = x_dimless * kB * T_GH
    # Avoid overflow
    arg_u = min(E / (kB * T_u), 700)
    arg_ds = min(E / (kB * T_ds), 700)
    num = np.exp(arg_u) - 1
    den = np.exp(arg_ds) - 1
    return num / den if den > 0 else float('inf')

# For very low energies (E << kB*T), both Bose-Einstein distributions
# are in the Rayleigh-Jeans regime: n_BE ~ kB*T/E, so R ~ T.
# Therefore R_dS/R_Rindler ~ T_dS/T_U = sqrt(1 + (cH/a)^2)
# This is the low-energy limit of the response ratio.

print("Low-energy limit of response ratio = T_dS/T_U:")
for a_val in [100*cH0, 10*cH0, cH0, 0.1*cH0, 0.01*cH0]:
    ratio = T_dS(a_val) / T_U(a_val)
    formula = np.sqrt(1 + (cH0/a_val)**2)
    print(f"  a = {a_val/cH0:.2f} cH0: T_dS/T_U = {ratio:.6f}, sqrt(1+(cH/a)^2) = {formula:.6f}")

# ======================================================================
# SECTION 2.2: Total Absorbed Power
# ======================================================================
print("\n" + "=" * 70)
print("Section 2.2: Total Absorbed Power")
print("=" * 70)

print("""
The total power absorbed by a detector from the thermal bath is:

  P(T) = integral_0^inf dE * E * rho(E) * R(E, T)

For a (3+1)D massless scalar field coupled to an Unruh-DeWitt detector
(scalar coupling), the power absorbed from the thermal bath goes as T^4
(Stefan-Boltzmann law for a single scalar degree of freedom):

  P(T) = sigma_s * T^4

where sigma_s = pi^2*kB^4 / (120*hbar^3*c^2) is the scalar field
Stefan-Boltzmann constant (1/4 of the photon value, roughly, for 1 dof).

More precisely, the total transition rate (all energies) is:

  R_total(T) = integral_0^inf dE * rho_scalar(E) * n_BE(E, T)

For a massless field: rho_scalar(E) ~ E^2 / (2*pi^2*hbar^3*c^3)

The integral gives:
  R_total = [1/(2*pi^2*hbar^3*c^3)] * integral_0^inf E^2/(exp(E/kBT)-1) dE
          = [1/(2*pi^2*hbar^3*c^3)] * 2*zeta(3)*(kBT)^3

Total power (energy absorption rate):
  P = integral_0^inf E * rho(E) * n_BE(E,T) dE * E_avg
    ~ integral E^3/(exp(E/kBT)-1) dE / (2*pi^2*hbar^3*c^3)
    = (pi^2/30) * (kBT)^4 / (hbar^3*c^3) * (1/2pi^2)
    = (kBT)^4 / (60*hbar^3*c^3)

So:
  P_Rindler(a) ~ [kB*T_U(a)]^4 / (60*hbar^3*c^3)
               = [hbar*a/(2*pi*c)]^4 / (60*hbar^3*c^3*kB^0)
               ... this simplifies but the key point is P ~ T^4 ~ a^4

  P_dS(a) ~ [kB*T_dS(a)]^4 / (60*hbar^3*c^3)
           = [hbar/(2*pi*c)]^4 * (a^2 + c^2*H^2)^2 / (60*hbar^3*c^3)

  RATIO: P_dS/P_Rindler = [T_dS/T_U]^4 = [(a^2+c^2*H^2)/a^2]^2
                         = [1 + (cH/a)^2]^2
""")

# Stefan-Boltzmann constant for a single massless scalar
sigma_scalar = np.pi**2 * kB**4 / (120 * hbar**3 * c**2)
print(f"Scalar Stefan-Boltzmann constant: sigma_s = {sigma_scalar:.4e} W/(m^2 K^4)")

# Total power comparison
print("\nTotal power in thermal bath:")
print(f"  P at T_GH: P_GH = sigma_s * T_GH^4 = {sigma_scalar * T_GH**4:.4e} W/m^2")
print(f"  P at T_U(cH0) = P_GH exactly (since T_U(cH0) = T_GH)")
print(f"  P at T_dS(cH0) = sigma_s * (sqrt(2)*T_GH)^4 = {sigma_scalar * (np.sqrt(2)*T_GH)**4:.4e} = 4 * P_GH")

# ======================================================================
# SECTION 2.3: Radiation Reaction Force
# ======================================================================
print("\n" + "=" * 70)
print("Section 2.3: Radiation Reaction Force — The Core Calculation")
print("=" * 70)

print("""
THE KEY PHYSICAL ARGUMENT:

The standard Abraham-Lorentz-Dirac (ALD) radiation reaction force in
flat spacetime is:
  F_ALD = tau_0 * m * da/dt    (where tau_0 = q^2/(6*pi*eps_0*mc^3))

This is a DISSIPATIVE force — it describes energy loss due to radiation.

However, in the Unruh framework, there is a deeper picture:
  1. The accelerating charge emits radiation (dissipation)
  2. The accelerating charge absorbs Unruh quanta (fluctuation)
  3. These balance via the fluctuation-dissipation theorem

The NET force is zero in equilibrium (the detector reaches the Unruh
temperature and stays there). The radiation reaction force is exactly
canceled by the vacuum fluctuation force in steady-state acceleration.

NOW THE CRITICAL QUESTION: In de Sitter, is there a RESIDUAL force?

ANSWER: NO, for the following reason.

An observer with constant proper acceleration a in de Sitter spacetime
is in a stationary state. The KMS condition guarantees that the detector
is in thermal equilibrium at temperature T_dS(a). The fluctuation-
dissipation theorem holds. There is NO net energy exchange between
the detector and the field in steady state.

The radiation reaction force and the vacuum fluctuation force STILL
cancel each other. The only difference is that they cancel at T_dS
instead of T_U.

But wait — this doesn't mean there's no modification to the dynamics!
The issue is more subtle.
""")

print("""
SUBTLETY: THE INERTIA ARGUMENT

The standard argument connecting vacuum fluctuations to inertia
(Haisch, Rueda, Puthoff 1994; modified by Milgrom, Verlinde) goes:

1. A particle moving through the vacuum (or beginning to accelerate)
   experiences a drag force from the vacuum fluctuations.

2. This drag force is proportional to acceleration:
     F_vacuum = -f(a) * a

3. If f(a) is constant, this just adds to the inertial mass.
   The particle's effective inertial mass becomes m_eff = m_bare + f.

4. If f(a) has a non-trivial dependence on a, then the effective
   inertial mass is acceleration-dependent: m_eff(a) = m_bare + f(a).

5. The de Sitter modification could change f(a) because the vacuum
   fluctuation spectrum changes across the crossover.

Let's compute this more carefully.

The "stochastic electrodynamics" (SED) approach gives the vacuum
fluctuation force as an integral over the spectral density:

  F_vacuum(a) = C * integral_0^{omega_max} omega^3 * n_eff(omega, a) d_omega

where C is a coupling constant and n_eff includes both the zero-point
contribution and the thermal contribution.

For flat space (Unruh):
  n_eff(omega, a) = 1/2 + n_BE(omega, T_U(a))
                  = 1/2 * coth(pi*c*omega/a)

For de Sitter:
  n_eff(omega, a) = 1/2 + n_BE(omega, T_dS(a))
                  = 1/2 * coth(hbar*omega/(2*kB*T_dS(a)))
                  = 1/2 * coth(pi*c*omega/sqrt(a^2 + c^2*H^2))

THE VACUUM CONTRIBUTION (1/2) IS THE SAME. It does not depend on a or H.
This is the Lorentz-invariant zero-point energy.

THE THERMAL CONTRIBUTION depends on T_dS(a) instead of T_U(a).
""")

# ======================================================================
# SECTION 2.4: Computing the effective drag coefficient
# ======================================================================
print("\n" + "=" * 70)
print("Section 2.4: The Effective Drag Coefficient")
print("=" * 70)

print("""
Following Boyer (1980) and Haisch & Rueda (1998), the contribution of
vacuum + thermal fluctuations to the equation of motion of a particle
with charge q (or coupling g) accelerating through the vacuum is:

For a scalar field, the drag force due to the thermal part is:

  F_drag(a) = -C_coupling * integral d^3k/(2*pi)^3 * partial/partial(a)
              [omega_k * n_BE(omega_k, T_eff(a))]

This is enormously complex in full generality. Let's extract the
ACCELERATION DEPENDENCE analytically.

SIMPLIFICATION: Since the spectrum is purely thermal, the total thermal
energy density depends only on T_eff:

  u_thermal(a) = (pi^2/30) * (kB*T_eff(a))^4 / (hbar*c)^3

For the drag force, we need the derivative with respect to velocity
(or acceleration) of the momentum flux of the thermal radiation
in the detector's frame. For the Unruh effect, this gives the
Abraham-Lorentz force.

The key quantity is how u_thermal depends on a:

  u_flat(a) = alpha_u * a^4     where alpha_u = pi^2*kB^4/(30*(2*pi*c)^4*hbar^3*c^3)
  u_dS(a) = alpha_u * (a^2 + c^2*H^2)^2

The FORCE is related to the derivative of the thermal energy with
respect to position (via the equivalence principle and the Tolman
relation):

  F ~ -d(u_thermal)/d(a) * (characteristic length)

Wait — this is getting circular. Let me take a different, more
rigorous approach.
""")

print("""
RIGOROUS APPROACH: Self-force from the de Sitter Wightman function

The self-force on a scalar charge q coupled to a massless scalar field
in a curved background is computed from the retarded Green function
via the DeWitt-Brehme equation. For a uniformly accelerating charge
in de Sitter, the self-force has been computed by several authors
(e.g., Akhmedov, Burda, 2013).

The result for a SCALAR charge in (3+1)D de Sitter with acceleration a:

  F_self = (q^2/(12*pi*c^3)) * [a_dot + correction terms involving H^2]

The H^2 correction terms come from the spacetime curvature and are of
the form:
  F_curvature ~ (q^2*H^2/(12*pi*c)) * a * [functions of a/(cH)]

For our purposes, the critical question is: DOES THE ACCELERATION
DEPENDENCE OF F_self BECOME NONLINEAR AT a ~ cH?

Let me compute this numerically by evaluating the self-force integral
directly.

The regularized self-force for a scalar charge in de Sitter can be
written as:

  F_self(a) = (q^2/(6*pi)) * d/d(tau) [alpha_eff(a)]
            = (q^2/(6*pi)) * (a * a_dot/c^2) / sqrt(a^2/c^2 + H^2)

For CONSTANT acceleration (a_dot = 0), F_self = 0 — just as in flat space.
The Abraham-Lorentz-Dirac force vanishes for uniform acceleration.

This means the direct self-force approach does NOT produce a steady-state
modification to F = ma. The ALD force is about radiation reaction to
CHANGING acceleration, not to steady acceleration.
""")

# ======================================================================
# SECTION 2.5: The entropic/thermodynamic approach
# ======================================================================
print("\n" + "=" * 70)
print("Section 2.5: Thermodynamic/Entropic Approach")
print("=" * 70)

print("""
Since the direct self-force vanishes for uniform acceleration, let me
try the THERMODYNAMIC approach (following Verlinde 2010, Jacobson 1995).

The idea: connect the entropy associated with the de Sitter horizon
to an entropic force.

For an accelerating observer in de Sitter, the relevant horizon has
area A and entropy S = A/(4*G*hbar/c^3) = A*c^3/(4*G*hbar).

The temperature is T_dS(a) = (hbar/(2*pi*c*kB)) * sqrt(a^2 + c^2*H^2).

An entropic force arises when a particle at the horizon changes the
entropy:
  F = T * dS/dx

This is Verlinde's framework. The standard Newtonian result F = ma
comes from:
  F = T_U(a) * 2*pi*kB*mc / hbar = [hbar*a/(2*pi*c*kB)] * [2*pi*kB*mc/hbar] = ma

Now replace T_U with T_dS:
  F_dS = T_dS(a) * 2*pi*kB*mc/hbar
       = [hbar*sqrt(a^2+c^2*H^2)/(2*pi*c*kB)] * [2*pi*kB*mc/hbar]
       = m * sqrt(a^2 + c^2*H^2)

This gives:
  F_dS = m * sqrt(a^2 + c^2*H^2)

The equation of motion becomes:
  F_Newton = m * sqrt(a^2 + c^2*H^2)

Solving for a:
  a = sqrt(F_N^2/m^2 - c^2*H^2)    for F_N/m > cH
  a = 0                               for F_N/m < cH

THIS IS PROBLEMATIC — it predicts a MINIMUM force below which no
acceleration is possible, not MOND-like behavior.

Let me try the other direction: the force needed to produce acceleration a.
""")

print("""
ALTERNATIVE ENTROPIC FORMULATION:

If the effective temperature experienced by a particle with acceleration a
in de Sitter is T_dS(a), and if inertia arises from the Unruh effect
(F = T * dS/dx), then:

  F_inertia(a) = T_dS(a) * (2*pi*kB*m*c/hbar)

Standard (flat): F = T_U(a) * (2*pi*kB*m*c/hbar) = m*a
De Sitter:       F = T_dS(a) * (2*pi*kB*m*c/hbar) = m*sqrt(a^2 + c^2*H^2)

So the inertial force is:
  F = m * sqrt(a^2 + c^2*H^2)

Newton's second law becomes:
  g_N = F_grav/m = sqrt(a^2 + c^2*H^2)

where g_N = GM/r^2 is the Newtonian gravitational field.

Solving for a:
  a^2 = g_N^2 - c^2*H^2
  a = sqrt(g_N^2 - c^2*H^2)    for g_N > cH
  a = 0                          for g_N < cH

This gives LESS acceleration than Newton, not MORE.
The de Sitter correction REDUCES the observed acceleration.

COMPARISON WITH MOND:
MOND says: mu(a/a0)*a = g_N, where mu(x) -> 1 for x >> 1 and mu(x) -> x for x << 1
=> a = g_N for large a, a = sqrt(a0*g_N) for small a
=> MORE acceleration than Newton at low g_N (flat rotation curves)

Our result: a = sqrt(g_N^2 - c^2*H^2)
=> LESS acceleration (or none) at low g_N

THIS IS THE OPPOSITE OF MOND.
""")

# ======================================================================
# SECTION 2.6: Numerical computation
# ======================================================================
print("\n" + "=" * 70)
print("Section 2.6: Numerical Verification and Plotting")
print("=" * 70)

# Compute the three force laws
g_N_range = np.logspace(-15, 0, 1000)  # m/s^2

# Newton: a = g_N
a_newton = g_N_range

# Our naive de Sitter: a = sqrt(g_N^2 - (cH)^2)
a_dS_naive = np.where(g_N_range > cH0, np.sqrt(g_N_range**2 - cH0**2), 0)

# MOND (simple interpolation): mu(a/a0)*a = g_N => a*(a/a0)/sqrt(1+(a/a0)^2) = g_N
# Solve for a given g_N using the standard MOND formula
# a = (g_N + sqrt(g_N^2 + 4*a0^2*g_N^2)) / (2) ... no, this is more complex.
# Use: a*mu(a/a0) = g_N where mu(x) = x/sqrt(1+x^2)
# => a^2/(a0*sqrt(1+(a/a0)^2)) = g_N
# Actually mu(x) = x/sqrt(1+x^2) gives:
# (a/a0)*a / sqrt(1+(a/a0)^2) = g_N
# a^2 / (a0*sqrt(1+(a/a0)^2)) = g_N ...

# Simpler: In MOND deep regime (a << a0): mu ~ a/a0, so a*a/a0 = g_N => a = sqrt(a0*g_N)
# In Newton regime (a >> a0): mu ~ 1, so a = g_N
# Full solution: solve a^2/sqrt(a0^2 + a^2) = g_N for a

from scipy.optimize import brentq

def mond_a_from_gN(g_N, a0=a0_MOND):
    """Solve mu(a/a0)*a = g_N for the standard interpolation function mu(x) = x/sqrt(1+x^2)."""
    if g_N <= 0:
        return 0
    # mu(x)*a = g_N where x = a/a0
    # (a/a0)/sqrt(1+(a/a0)^2) * a = g_N
    # a^2/(a0*sqrt(1+(a/a0)^2)) = g_N
    def residual(a):
        x = a / a0
        return a * x / np.sqrt(1 + x**2) - g_N
    # a must be > 0, and for large g_N, a ~ g_N
    a_max = g_N * 10  # generous upper bound
    try:
        return brentq(residual, 1e-30, a_max)
    except:
        return g_N  # fallback to Newtonian

a_mond = np.array([mond_a_from_gN(g) for g in g_N_range])

# Plot comparison
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Top: a vs g_N
ax1.loglog(g_N_range, a_newton, 'k-', label='Newton: a = gN', linewidth=2)
ax1.loglog(g_N_range, a_mond, 'b-', label=r'MOND: $\mu(a/a_0) \cdot a = g_N$', linewidth=2)
ax1.loglog(g_N_range[a_dS_naive > 0], a_dS_naive[a_dS_naive > 0], 'r--',
           label=r'Naive dS: $a = \sqrt{g_N^2 - c^2H^2}$', linewidth=2)
ax1.axvline(cH0, color='gray', linestyle=':', alpha=0.5)
ax1.axvline(a0_MOND, color='orange', linestyle=':', alpha=0.5)
ax1.text(cH0*1.5, 1e-14, 'cH0', fontsize=10, color='gray')
ax1.text(a0_MOND*0.1, 1e-14, 'a0', fontsize=10, color='orange')
ax1.set_xlabel(r'$g_N$ (m/s$^2$)', fontsize=12)
ax1.set_ylabel(r'$a$ (m/s$^2$)', fontsize=12)
ax1.set_title('Observed acceleration vs Newtonian gravity', fontsize=14)
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(1e-15, 1e0)
ax1.set_ylim(1e-15, 1e0)

# Bottom: ratio a/g_N
ax2.semilogx(g_N_range, a_newton/g_N_range, 'k-', label='Newton', linewidth=2)
ax2.semilogx(g_N_range, a_mond/g_N_range, 'b-', label='MOND', linewidth=2)
a_dS_ratio = np.where(a_dS_naive > 0, a_dS_naive/g_N_range, 0)
ax2.semilogx(g_N_range, a_dS_ratio, 'r--', label='Naive dS', linewidth=2)
ax2.axvline(cH0, color='gray', linestyle=':', alpha=0.5)
ax2.axvline(a0_MOND, color='orange', linestyle=':', alpha=0.5)
ax2.set_xlabel(r'$g_N$ (m/s$^2$)', fontsize=12)
ax2.set_ylabel(r'$a / g_N$', fontsize=12)
ax2.set_title('Ratio a/gN (deviation from Newton)', fontsize=14)
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(1e-15, 1e0)
ax2.set_ylim(-0.1, 3.5)

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, 'plot4_force_law_comparison.png'), dpi=150)
plt.close()
print("Plot 4 saved: plot4_force_law_comparison.png")

# ======================================================================
# SECTION 2.7: Can we get MOND-LIKE behavior?
# ======================================================================
print("\n" + "=" * 70)
print("Section 2.7: Can We Get MOND-Like Behavior?")
print("=" * 70)

print("""
ANALYSIS: Why the naive de Sitter approach gives the WRONG sign

The naive entropic argument gives:
  F_inertia = m * sqrt(a^2 + c^2*H^2)

This means the "inertial resistance" is LARGER than ma at low a:
  F_inertia > ma  for all a

So it takes MORE force to accelerate the particle, not less.
The particle appears HEAVIER, not lighter.

For MOND, we need the particle to appear LIGHTER (less inertia)
at low accelerations: the same gravitational force produces MORE
acceleration than Newton predicts.

THE FUNDAMENTAL ISSUE: The de Sitter correction to the Unruh
temperature goes in the WRONG DIRECTION for MOND.

  T_dS > T_U  (always, for H > 0)

A higher effective temperature means MORE thermal inertia,
not less. If F = T * (2*pi*kB*mc/hbar) and T increases, then
F increases for the same a, meaning more force is needed.

IS THERE A WAY TO REVERSE THE SIGN?

Option 1: Modified inertia as m_i(a) = m * [T_U(a)/T_dS(a)]
  = m * a / sqrt(a^2 + c^2*H^2)

This would give:
  F = m_i(a) * a = m * a^2 / sqrt(a^2 + c^2*H^2)

This IS MOND-like! It gives:
  - a >> cH0: F ~ m*a (Newton)
  - a << cH0: F ~ m*a^2/(cH0) (deep MOND)

And the MOND interpolation function would be:
  mu(x) = x / sqrt(x^2 + (cH0/a0)^2)

Wait, let me work this out more carefully.
""")

print("""
THE MODIFIED INERTIA HYPOTHESIS:

If inertia arises from the flat-space Unruh effect (F = T_U * entropy_gradient),
and the de Sitter background REDUCES the available Unruh radiation by
providing a "background bath" that effectively screens the acceleration-
dependent part, then:

  The "excess" thermal energy due to acceleration =
    T_eff - T_background = T_dS(a) - T_GH
    = (hbar/(2*pi*c*kB))[sqrt(a^2+c^2*H^2) - cH]

  For a >> cH: excess ~ (hbar*a/(2*pi*c*kB))[1 - cH/a + ...] ~ T_U
  For a ~ cH: excess ~ T_GH*(sqrt(2) - 1) ~ 0.414*T_GH
  For a << cH: excess ~ T_GH*(1 + a^2/(2c^2H^2) - 1) ~ hbar*a^2/(4*pi*c^3*kB*H)

This gives a QUADRATIC dependence on a at low acceleration!

If inertia is proportional to this excess:
  m_i(a) = m * (T_dS(a) - T_GH) / T_U(a)
         = m * [sqrt(a^2+c^2*H^2) - cH] / a

For a >> cH: m_i -> m (Newton recovered)
For a << cH: m_i -> m * a/(2*cH) (inertia drops linearly with a)

Equation of motion: g_N = m_i(a)*a/m = a * [sqrt(a^2+c^2*H^2) - cH] / a
Actually wait:
  F = m_i(a) * a
  g_N = F/m = a * [sqrt(a^2+c^2*H^2) - cH] / a = sqrt(a^2+c^2*H^2) - cH

So: g_N = sqrt(a^2 + c^2*H^2) - cH
=> sqrt(a^2 + c^2*H^2) = g_N + cH
=> a^2 = (g_N + cH)^2 - c^2*H^2 = g_N^2 + 2*g_N*cH

=> a = sqrt(g_N^2 + 2*cH*g_N) = sqrt(g_N*(g_N + 2*cH))

For g_N >> cH: a ~ g_N (Newton)
For g_N << cH: a ~ sqrt(2*cH*g_N) ~ sqrt(2*cH_0*g_N)

THIS IS MOND-LIKE! The deep-MOND regime gives a ~ sqrt(a_0*g_N)
with a_0 = 2*cH_0.
""")

# Compute this version
a_modified = np.sqrt(g_N_range**2 + 2*cH0*g_N_range)
a0_predicted = 2*cH0
print(f"\nPredicted a0 from this model: a0 = 2*cH0 = {a0_predicted:.4e} m/s^2")
print(f"Observed MOND a0: {a0_MOND:.4e} m/s^2")
print(f"Ratio: a0_predicted/a0_MOND = {a0_predicted/a0_MOND:.2f}")
print(f"  (Factor of ~{a0_predicted/a0_MOND:.1f} too large)")

# MOND-like version with exact same functional form
a_deep_mond = np.sqrt(a0_predicted * g_N_range)

# Also compute with a = sqrt(g_N*(g_N + 2*cH0))
print(f"\nComparison at g_N = a0_MOND:")
print(f"  Newton:   a = {a0_MOND:.4e}")
print(f"  MOND:     a = {mond_a_from_gN(a0_MOND):.4e}")
print(f"  Modified: a = {np.sqrt(a0_MOND**2 + 2*cH0*a0_MOND):.4e}")

# ======================================================================
# SECTION 2.8: Alternative — Direct ratio approach
# ======================================================================
print("\n" + "=" * 70)
print("Section 2.8: Alternative Ratio Approach")
print("=" * 70)

print("""
ALTERNATIVE DERIVATION: T_U/T_dS as interpolation function

If the effective inertial mass is:
  m_i(a) = m * T_U(a) / T_dS(a) = m * a / sqrt(a^2 + c^2*H^2)

Then:
  mu(a) = m_i(a)/m = a / sqrt(a^2 + c^2*H^2)

The equation of motion becomes:
  mu(a) * a = g_N
  a^2 / sqrt(a^2 + c^2*H^2) = g_N

Let x = a/cH0:
  (cH0)^2 * x^2 / (cH0 * sqrt(x^2 + 1)) = g_N
  cH0 * x^2 / sqrt(x^2 + 1) = g_N

This is EXACTLY the MOND equation with:
  mu(x) = x / sqrt(1 + x^2)    (standard interpolation function)
  a_0 = cH_0                    (the critical acceleration)

AMAZING: This reproduces the STANDARD MOND interpolation function
with a0 = cH0!
""")

# Compute this version
def modified_inertia_a_from_gN(g_N, a0=cH0):
    """Solve mu(a/a0)*a = g_N with mu(x) = x/sqrt(1+x^2)."""
    if g_N <= 0:
        return 0
    def residual(a):
        x = a / a0
        return a * x / np.sqrt(1 + x**2) - g_N
    a_max = g_N * 100
    try:
        return brentq(residual, 1e-40, a_max)
    except:
        return g_N

a_mod_inertia = np.array([modified_inertia_a_from_gN(g) for g in g_N_range])

print(f"\nWith mu(x) = x/sqrt(1+x^2) and a0 = cH0 = {cH0:.4e} m/s^2:")
print(f"  Observed MOND a0 = {a0_MOND:.4e} m/s^2")
print(f"  Ratio cH0/a0_MOND = {cH0/a0_MOND:.2f}")
print(f"  So cH0 is {cH0/a0_MOND:.1f}x larger than a0_MOND")
print(f"  Verlinde (2016) gets a0 = cH0/6 which gives {cH0/6:.4e}")
print(f"  Ratio (cH0/6)/a0_MOND = {cH0/(6*a0_MOND):.2f}")

# ======================================================================
# PLOT 5: All force laws compared
# ======================================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Re-solve MOND with a0 = a0_MOND
a_mond_std = np.array([mond_a_from_gN(g, a0=a0_MOND) for g in g_N_range])
# And with a0 = cH0
a_mond_cH0 = np.array([mond_a_from_gN(g, a0=cH0) for g in g_N_range])

ax1.loglog(g_N_range, g_N_range, 'k-', label='Newton', linewidth=2)
ax1.loglog(g_N_range, a_mond_std, 'b-', label=f'MOND (a0={a0_MOND:.1e})', linewidth=2)
ax1.loglog(g_N_range, a_mod_inertia, 'r--',
           label=r'Modified inertia: $\mu = a/\sqrt{a^2+c^2H^2}$ ($a_0=cH_0$)', linewidth=2)
ax1.loglog(g_N_range, a_mond_cH0, 'g:',
           label=f'MOND (a0=cH0={cH0:.1e})', linewidth=2, alpha=0.7)
ax1.axvline(cH0, color='gray', linestyle=':', alpha=0.5)
ax1.axvline(a0_MOND, color='orange', linestyle=':', alpha=0.5)
ax1.set_xlabel(r'$g_N$ (m/s$^2$)', fontsize=12)
ax1.set_ylabel(r'Observed $a$ (m/s$^2$)', fontsize=12)
ax1.set_title('Modified Inertia Force Law vs MOND', fontsize=14)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(1e-15, 1e0)
ax1.set_ylim(1e-12, 1e0)

# Ratio a/g_N
ax2.semilogx(g_N_range, a_mond_std/g_N_range, 'b-',
             label=f'MOND (a0={a0_MOND:.1e})', linewidth=2)
ax2.semilogx(g_N_range, a_mod_inertia/g_N_range, 'r--',
             label=r'Modified inertia ($a_0=cH_0$)', linewidth=2)
ax2.semilogx(g_N_range, a_mond_cH0/g_N_range, 'g:',
             label=f'MOND (a0=cH0)', linewidth=2, alpha=0.7)
ax2.axhline(1, color='k', linestyle='-', linewidth=1, alpha=0.5)
ax2.axvline(cH0, color='gray', linestyle=':', alpha=0.5)
ax2.axvline(a0_MOND, color='orange', linestyle=':', alpha=0.5)
ax2.set_xlabel(r'$g_N$ (m/s$^2$)', fontsize=12)
ax2.set_ylabel(r'$a / g_N$', fontsize=12)
ax2.set_title('Boost factor a/gN', fontsize=14)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(1e-15, 1e0)
ax2.set_ylim(0.5, 15)

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, 'plot5_all_force_laws.png'), dpi=150)
plt.close()
print("\nPlot 5 saved: plot5_all_force_laws.png")

# ======================================================================
# SUMMARY
# ======================================================================
print("\n" + "=" * 70)
print("PART 2 SUMMARY")
print("=" * 70)
print("""
RESULT: Three approaches were tried:

1. NAIVE ENTROPIC (F = T_dS * entropy_gradient):
   Gives F = m*sqrt(a^2 + c^2*H^2) > ma
   WRONG SIGN — predicts less acceleration than Newton, not more.
   Opposite of MOND.

2. EXCESS TEMPERATURE (inertia from T_dS - T_GH):
   Gives a = sqrt(g_N^2 + 2*cH*g_N)
   For small g_N: a ~ sqrt(2*cH*g_N) — MOND-like with a0 = 2*cH0
   Correct qualitative behavior but derivation is ad hoc.

3. RATIO APPROACH (m_i = m * T_U/T_dS):
   Gives mu(a) = a/sqrt(a^2 + c^2*H^2) — EXACTLY the standard MOND
   interpolation function with a0 = cH0!
   But the derivation requires assuming inertia is proportional to T_U
   and the de Sitter correction is in the denominator, not numerator.

KEY INSIGHT: The functional form mu(x) = x/sqrt(1+x^2) with x = a/(cH0)
emerges NATURALLY from the ratio T_U(a)/T_dS(a). This is mathematically
exact — NOT an approximation.

HOWEVER: The PHYSICAL JUSTIFICATION for why inertia should be proportional
to T_U/T_dS rather than to T_dS is NOT established. This is the weakest
link in the argument.

The predicted a0 = cH0 = 6.6e-10 m/s^2, which is 5.5x larger than the
observed a0 = 1.2e-10 m/s^2. This factor could be absorbed into the
model (e.g., Verlinde gets a0 = cH0/6 from a more careful analysis).
""")
