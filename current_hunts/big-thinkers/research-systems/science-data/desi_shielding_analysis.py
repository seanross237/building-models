"""
Matter Shielding Model vs DESI DR2 Dark Energy Constraints
==========================================================

Hypothesis: The effective dark energy density is modified by matter "shielding":
    rho_DE_eff(z) = rho_Lambda_bare - alpha * rho_m(z)

where alpha is a single free parameter representing shielding efficiency.

This script:
1. Derives w_eff(z) analytically
2. Maps the model to the (w0, wa) parameterization
3. Compares against DESI DR2 constraints
4. Produces diagnostic plots
5. Makes predictions at high z

Author: Sean Ross + Claude
Date: 2026-04-02
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import minimize_scalar, minimize
import matplotlib.patches as mpatches
from matplotlib.patches import Ellipse
import os

# ============================================================
# COSMOLOGICAL PARAMETERS (Planck 2018)
# ============================================================
H0 = 67.4          # km/s/Mpc
Omega_m0 = 0.315
Omega_Lambda0 = 0.685
Omega_b0 = 0.049
c_km_s = 2.998e5   # speed of light in km/s

# Critical density ratios
# rho_m0 / rho_crit = Omega_m0
# rho_Lambda0 / rho_crit = Omega_Lambda0

# ============================================================
# SECTION 1: ANALYTICAL DERIVATION
# ============================================================
print("=" * 70)
print("SECTION 1: ANALYTICAL DERIVATION")
print("=" * 70)

print("""
MODEL:
  rho_DE_eff(z) = rho_Lambda_bare - alpha * rho_m(z)
  rho_m(z) = rho_m0 * (1+z)^3

BOUNDARY CONDITION (z=0):
  rho_DE_eff(0) = rho_Lambda_obs = rho_Lambda_bare - alpha * rho_m0
  => rho_Lambda_bare = rho_Lambda_obs + alpha * rho_m0

SUBSTITUTING:
  rho_DE_eff(z) = (rho_Lambda_obs + alpha * rho_m0) - alpha * rho_m0 * (1+z)^3
                = rho_Lambda_obs + alpha * rho_m0 * [1 - (1+z)^3]

In units of rho_crit:
  Omega_DE_eff(z) = Omega_Lambda0 + alpha * Omega_m0 * [1 - (1+z)^3]

Note: Omega_DE_eff(z) here is the density at redshift z divided by rho_crit TODAY
(not the density parameter at z). This is the standard convention for
the Friedmann equation: H^2/H0^2 = Omega_m0*(1+z)^3 + Omega_DE_eff(z)/f(z) ...

Actually, let's be more careful. In the Friedmann equation:
  H^2(z) = H0^2 [Omega_m0 (1+z)^3 + Omega_r0 (1+z)^4 + rho_DE(z)/rho_crit0]

For our model:
  rho_DE(z)/rho_crit0 = Omega_Lambda0 + alpha * Omega_m0 * [1 - (1+z)^3]

EFFECTIVE EQUATION OF STATE:
  w_eff(z) is defined by: rho_DE(z) = rho_DE(0) * exp(3 * integral_0^z [1+w(z')]/(1+z') dz')

  Equivalently: w_eff(z) = -1 + (1+z)/(3*rho_DE(z)) * d(rho_DE)/dz

  d(rho_DE)/dz = -alpha * rho_m0 * 3*(1+z)^2
               = -3 * alpha * Omega_m0 * rho_crit0 * (1+z)^2

  So: w_eff(z) = -1 + (1+z) * [-3*alpha*Omega_m0*(1+z)^2] / [3 * rho_DE_eff(z)/rho_crit0]
              = -1 - alpha*Omega_m0*(1+z)^3 / [Omega_Lambda0 + alpha*Omega_m0*(1 - (1+z)^3)]

Let's define:
  r(z) = alpha * Omega_m0 / Omega_Lambda0  (ratio of shielding term to Lambda at z=0)
  x = (1+z)^3

Then:
  w_eff(z) = -1 - r*x / [1 + r*(1 - x)]
           = -1 - r*x / [1 + r - r*x]

CHECK at z=0 (x=1):
  w_eff(0) = -1 - r / [1 + r - r] = -1 - r = -1 - alpha*Omega_m0/Omega_Lambda0

This is the w0 of the model: w0 = -1 - alpha * Omega_m0 / Omega_Lambda0

For alpha > 0: w0 < -1 (phantom!)
For alpha < 0: w0 > -1 (quintessence-like)

DESI finds w0 ~ -0.7 to -0.8, so w0 > -1, meaning we need alpha < 0.

WAIT — let's reconsider the sign convention.
If matter SHIELDS (reduces) the expansion, the shielding term should REDUCE
the effective dark energy. So:
  rho_DE_eff = rho_bare - alpha * rho_m    with alpha > 0

At z=0 this means rho_bare > rho_Lambda_obs.
At high z, rho_m is larger, so more shielding, so rho_DE_eff is SMALLER
(could even go negative).

The w_eff at z=0 = -1 - alpha*Omega_m0/Omega_Lambda0 < -1 for alpha > 0.

But DESI wants w0 > -1. So we need the OPPOSITE sign:
  rho_DE_eff = rho_bare + alpha * rho_m  (matter ENHANCES effective DE)

OR we keep the model but flip: what looks like dark energy includes a
contribution that scales like matter but is counted in the DE sector.

Let me reconsider: maybe the shielding model naturally gives w0 < -1.
Let me check what DESI actually says more carefully.

DESI DR2 results (March 2025):
  - w0 = -0.75 +/- 0.07 (CMB+DESI)  [w0 > -1]
  - wa = -0.88 +/- 0.27             [wa < 0]

  The w0-wa parameterization: w(a) = w0 + wa*(1-a)
  At high z (a->0): w -> w0 + wa ~ -0.75 - 0.88 = -1.63
  At z=0 (a=1): w -> w0 = -0.75

So w(z) starts below -1 at high z and rises ABOVE -1 at z=0.
This means w CROSSES -1 during cosmic evolution.

For the shielding model with alpha > 0:
  w_eff(z=0) = -1 - r < -1
  w_eff(z>>0) -> -1 - r*x / (1+r-r*x)

  As x grows, denominator (1+r-r*x) can go to zero or negative.
  That's when rho_DE_eff -> 0 (all dark energy is shielded).

This does NOT match DESI. The shielding model gives w < -1 at z=0
and even more negative at high z. DESI wants w > -1 at z=0.

Let me try the OPPOSITE: matter ADDS to the effective dark energy
(an "anti-shielding" or "matter-induced" dark energy):
  rho_DE_eff(z) = rho_bare + alpha * rho_m(z)   [alpha > 0]

Then rho_bare = rho_Lambda_obs - alpha * rho_m0
And rho_DE_eff(z) = rho_Lambda_obs - alpha*Omega_m0*rho_crit*(1 - (1+z)^3)
                   = rho_Lambda_obs + alpha*Omega_m0*rho_crit*((1+z)^3 - 1)

d(rho_DE)/dz = 3*alpha*Omega_m0*rho_crit*(1+z)^2 > 0
(DE density increases with z — it was bigger in the past)

w_eff(z) = -1 + (1+z)/(3*rho_DE) * d(rho_DE)/dz
         = -1 + alpha*Omega_m0*(1+z)^3 / [Omega_Lambda0 + alpha*Omega_m0*((1+z)^3-1)]

At z=0: w0 = -1 + alpha*Omega_m0/Omega_Lambda0 = -1 + r
For alpha > 0: w0 > -1. YES! This matches the DESI direction.

Actually, let me re-examine. The original hypothesis says matter SHIELDS
(blocks) the expansion. If matter blocks expansion, then at high z there's
more matter and MORE blocking, so LESS effective dark energy. That means
rho_DE is SMALLER at high z. But for the w0-wa parameterization to give
w0 > -1, we need rho_DE that DECREASES toward the present (or increases
toward the past more slowly than constant).

Hmm, actually: a CONSTANT rho gives w = -1. If rho INCREASES toward the past
(like in the anti-shielding case), that means the DE dilutes as we go forward
in time, which gives w > -1 (quintessence-like). This is because if
d(rho_DE)/dz > 0 (density was larger in past), then the DE is "diluting"
and behaves like it has w > -1.

The shielding model (rho_DE DECREASES toward past because matter eats it):
  d(rho_DE)/dz < 0 => w < -1 (phantom). Opposite of DESI.

SO: The ORIGINAL shielding hypothesis (matter blocks dark energy) predicts
PHANTOM dark energy (w < -1), which is the OPPOSITE of what DESI sees.

But wait — there's a more physical version. What if:
  - Bare dark energy is the TRUE cosmological constant
  - Matter doesn't shield DE, but rather, matter GRAVITATIONALLY
    contributes something that looks like extra DE at high density
  - As matter dilutes, this extra contribution goes away
  - So effective DE was LARGER in the past → w > -1 ✓

This is actually the "matter-dark energy coupling" or "interacting DE" model.
Let me proceed with BOTH signs and see which matches DESI.
""")


# ============================================================
# SECTION 2: MODEL IMPLEMENTATION
# ============================================================

def rho_DE_eff(z, alpha, Omega_m=Omega_m0, Omega_L=Omega_Lambda0):
    """
    Effective DE density (in units of rho_crit0).

    Model: rho_DE_eff(z) = rho_bare + alpha * rho_m(z)
    with rho_bare = Omega_L - alpha * Omega_m  (so that rho_DE_eff(0) = Omega_L)

    Result: rho_DE_eff(z) / rho_crit0 = Omega_L + alpha * Omega_m * [(1+z)^3 - 1]

    alpha > 0: matter contributes extra effective DE (quintessence-like, w > -1)
    alpha < 0: matter reduces effective DE (phantom-like, w < -1)
    """
    return Omega_L + alpha * Omega_m * ((1 + z)**3 - 1)


def w_eff(z, alpha, Omega_m=Omega_m0, Omega_L=Omega_Lambda0):
    """
    Effective equation of state.

    w(z) = -1 + alpha * Omega_m * (1+z)^3 / rho_DE_eff(z)
    """
    rho = rho_DE_eff(z, alpha, Omega_m, Omega_L)
    if np.isscalar(z):
        if rho <= 0:
            return np.nan
    else:
        rho = np.where(rho > 0, rho, np.nan)

    return -1.0 + alpha * Omega_m * (1 + z)**3 / rho


def w_w0wa(z, w0, wa):
    """Standard w0-wa parameterization: w(a) = w0 + wa*(1-a), a = 1/(1+z)"""
    a = 1.0 / (1 + z)
    return w0 + wa * (1 - a)


def map_to_w0wa(alpha, Omega_m=Omega_m0, Omega_L=Omega_Lambda0):
    """
    Map shielding parameter alpha to (w0, wa).

    w0 = w_eff(z=0) = -1 + alpha * Omega_m / Omega_L

    wa: we match the derivative dw/da at a=1 (z=0).
    In the w0-wa param: dw/da = -wa, so wa = -dw/da|_{a=1}

    dw/dz = d/dz [-1 + alpha*Omega_m*(1+z)^3 / rho_DE_eff(z)]

    Let f(z) = alpha*Omega_m*(1+z)^3, g(z) = rho_DE_eff(z)
    dw/dz = (f'g - fg') / g^2

    f' = 3*alpha*Omega_m*(1+z)^2
    g' = 3*alpha*Omega_m*(1+z)^2  (same!)

    So dw/dz = [3*alpha*Omega_m*(1+z)^2 * g - f * 3*alpha*Omega_m*(1+z)^2] / g^2
             = 3*alpha*Omega_m*(1+z)^2 * (g - f) / g^2

    At z=0: g(0) = Omega_L, f(0) = alpha*Omega_m
    dw/dz|_{z=0} = 3*alpha*Omega_m * (Omega_L - alpha*Omega_m) / Omega_L^2

    And dw/da = dw/dz * dz/da = dw/dz * (-(1+z)^2) = -dw/dz at z=0
    So wa = -dw/da = dw/dz|_{z=0}

    wa = 3*alpha*Omega_m * (Omega_L - alpha*Omega_m) / Omega_L^2
    """
    r = alpha * Omega_m / Omega_L
    w0 = -1.0 + r
    wa = 3.0 * r * (1.0 - r)
    return w0, wa


def map_to_w0wa_numerical(alpha, Omega_m=Omega_m0, Omega_L=Omega_Lambda0):
    """
    Numerical mapping: fit w0, wa to minimize mismatch over z=[0, 2].
    """
    z_fit = np.linspace(0, 2, 200)
    w_model = np.array([w_eff(zi, alpha, Omega_m, Omega_L) for zi in z_fit])

    # Remove NaN
    mask = np.isfinite(w_model)
    z_fit = z_fit[mask]
    w_model = w_model[mask]

    if len(z_fit) < 10:
        return np.nan, np.nan

    def cost(params):
        w0, wa = params
        w_approx = w_w0wa(z_fit, w0, wa)
        return np.sum((w_model - w_approx)**2)

    # Initial guess from analytical
    r = alpha * Omega_m / Omega_L
    res = minimize(cost, [-1 + r, 3*r*(1-r)], method='Nelder-Mead')
    return res.x[0], res.x[1]


# ============================================================
# SECTION 3: DESI DR2 CONSTRAINTS
# ============================================================
print("\n" + "=" * 70)
print("SECTION 2: DESI DR2 CONSTRAINTS")
print("=" * 70)

# DESI DR2 (March 2025) combined with CMB (Planck + ACT)
# From DESI collaboration papers
# w0-wa parameterization: w(a) = w0 + wa(1-a)
#
# Best fit values (DESI BAO + CMB + PantheonPlus):
#   w0 = -0.752 +/- 0.063
#   wa = -0.86  +0.28/-0.25
#
# Best fit (DESI BAO + CMB + DESY5):
#   w0 = -0.758 +/- 0.058
#   wa = -0.82  +0.26/-0.23
#
# Rejection of LCDM (w0=-1, wa=0): 2.8 - 4.2 sigma depending on dataset combo

# We'll use the DESI+CMB+PantheonPlus values as reference
w0_DESI = -0.752
w0_DESI_err = 0.063
wa_DESI = -0.86
wa_DESI_err = 0.27  # average of asymmetric errors

# Correlation coefficient between w0 and wa (approximate, from contour shape)
# They are strongly anti-correlated
rho_w0wa = -0.85

print(f"DESI DR2 + CMB + PantheonPlus best fit:")
print(f"  w0 = {w0_DESI} +/- {w0_DESI_err}")
print(f"  wa = {wa_DESI} +/- {wa_DESI_err}")
print(f"  Correlation: {rho_w0wa}")
print(f"  LCDM point (w0=-1, wa=0) rejected at ~3.5 sigma")


# ============================================================
# SECTION 4: MAPPING ALPHA TO (w0, wa) SPACE
# ============================================================
print("\n" + "=" * 70)
print("SECTION 3: MAPPING ALPHA TO (w0, wa)")
print("=" * 70)

# Analytical mapping
print("\nAnalytical formulas:")
print("  w0 = -1 + alpha * Omega_m / Omega_Lambda")
print(f"     = -1 + alpha * {Omega_m0}/{Omega_Lambda0}")
print(f"     = -1 + {Omega_m0/Omega_Lambda0:.4f} * alpha")
print()
print("  wa = 3 * alpha * Omega_m / Omega_Lambda * (1 - alpha*Omega_m/Omega_Lambda)")
print(f"     = 3 * {Omega_m0/Omega_Lambda0:.4f} * alpha * (1 - {Omega_m0/Omega_Lambda0:.4f}*alpha)")

# What alpha gives w0 = -0.752?
alpha_target_w0 = (w0_DESI + 1) * Omega_Lambda0 / Omega_m0
print(f"\nTo match w0 = {w0_DESI}:")
print(f"  alpha = (w0 + 1) * Omega_L / Omega_m = {alpha_target_w0:.4f}")

w0_pred, wa_pred = map_to_w0wa(alpha_target_w0)
print(f"  Predicted (w0, wa) = ({w0_pred:.4f}, {wa_pred:.4f})")
print(f"  DESI target (w0, wa) = ({w0_DESI}, {wa_DESI})")
print(f"  wa residual = {wa_pred - wa_DESI:.4f}")

# Numerical mapping
w0_num, wa_num = map_to_w0wa_numerical(alpha_target_w0)
print(f"\nNumerical fit over z=[0,2]:")
print(f"  (w0, wa) = ({w0_num:.4f}, {wa_num:.4f})")

# Scan alpha values
alphas = np.linspace(-2.0, 2.0, 1000)
w0_arr = np.zeros_like(alphas)
wa_arr = np.zeros_like(alphas)
w0_num_arr = np.zeros_like(alphas)
wa_num_arr = np.zeros_like(alphas)

for i, a in enumerate(alphas):
    w0_arr[i], wa_arr[i] = map_to_w0wa(a)
    w0_num_arr[i], wa_num_arr[i] = map_to_w0wa_numerical(a)

print("\n\nSample alpha -> (w0, wa) mapping:")
print(f"{'alpha':>8s}  {'w0 (anal)':>10s}  {'wa (anal)':>10s}  {'w0 (num)':>10s}  {'wa (num)':>10s}")
for a_test in [-0.5, -0.3, -0.1, 0.0, 0.1, 0.3, 0.5, 0.54, 0.6, 0.8, 1.0]:
    w0a, waa = map_to_w0wa(a_test)
    w0n, wan = map_to_w0wa_numerical(a_test)
    print(f"{a_test:8.2f}  {w0a:10.4f}  {waa:10.4f}  {w0n:10.4f}  {wan:10.4f}")


# ============================================================
# SECTION 5: FIND BEST-FIT ALPHA
# ============================================================
print("\n" + "=" * 70)
print("SECTION 4: BEST-FIT ALPHA")
print("=" * 70)

# Chi-squared in (w0, wa) space with correlation
def chi2_w0wa(alpha, use_numerical=False):
    if use_numerical:
        w0, wa = map_to_w0wa_numerical(alpha)
    else:
        w0, wa = map_to_w0wa(alpha)

    if np.isnan(w0) or np.isnan(wa):
        return 1e10

    dw0 = w0 - w0_DESI
    dwa = wa - wa_DESI
    s0 = w0_DESI_err
    sa = wa_DESI_err
    r = rho_w0wa

    # Bivariate Gaussian chi2
    chi2 = (1/(1-r**2)) * ((dw0/s0)**2 + (dwa/sa)**2 - 2*r*dw0*dwa/(s0*sa))
    return chi2

# Scan
chi2_anal = np.array([chi2_w0wa(a, False) for a in alphas])
chi2_num = np.array([chi2_w0wa(a, True) for a in alphas])

# Find minimum
idx_best_anal = np.argmin(chi2_anal)
idx_best_num = np.argmin(chi2_num)

alpha_best_anal = alphas[idx_best_anal]
alpha_best_num = alphas[idx_best_num]

print(f"\nBest-fit alpha (analytical w0-wa): {alpha_best_anal:.4f}")
print(f"  chi2 = {chi2_anal[idx_best_anal]:.4f}")
w0b, wab = map_to_w0wa(alpha_best_anal)
print(f"  (w0, wa) = ({w0b:.4f}, {wab:.4f})")

print(f"\nBest-fit alpha (numerical w0-wa): {alpha_best_num:.4f}")
print(f"  chi2 = {chi2_num[idx_best_num]:.4f}")
w0bn, wabn = map_to_w0wa_numerical(alpha_best_num)
print(f"  (w0, wa) = ({w0bn:.4f}, {wabn:.4f})")

# Refine with scipy
res_anal = minimize_scalar(lambda a: chi2_w0wa(a, False), bounds=(-1, 2), method='bounded')
res_num = minimize_scalar(lambda a: chi2_w0wa(a, True), bounds=(-1, 2), method='bounded')

alpha_best = res_num.x
chi2_best = res_num.fun
w0_best, wa_best = map_to_w0wa_numerical(alpha_best)

print(f"\nRefined best-fit alpha (numerical): {alpha_best:.6f}")
print(f"  chi2_min = {chi2_best:.4f}")
print(f"  (w0, wa) = ({w0_best:.4f}, {wa_best:.4f})")
print(f"  DESI target: ({w0_DESI}, {wa_DESI})")
print(f"  Delta w0 = {w0_best - w0_DESI:.4f}")
print(f"  Delta wa = {wa_best - wa_DESI:.4f}")

# Sigma equivalent
from scipy.stats import chi2 as chi2_dist
p_value = 1 - chi2_dist.cdf(chi2_best, df=1)  # 1 dof (1 param model in 2d space)
sigma_equiv = np.sqrt(chi2_best)  # approximate
print(f"\n  chi2 with 1 dof: p-value = {p_value:.4f}")
print(f"  Approximate sigma tension: {sigma_equiv:.2f}")


# ============================================================
# SECTION 6: THE KEY QUESTION — DOES THE CURVE SHAPE MATCH?
# ============================================================
print("\n" + "=" * 70)
print("SECTION 5: CURVE SHAPE COMPARISON")
print("=" * 70)

# The w0-wa parameterization is LINEAR in a.
# Our model's w(z) is NOT linear in a. So the real question is whether
# the full w(z) curve matches, not just the w0-wa projection.

z_arr = np.linspace(0, 3, 500)
a_arr = 1.0 / (1 + z_arr)

w_shielding = np.array([w_eff(z, alpha_best) for z in z_arr])
w_DESI_curve = w_w0wa(z_arr, w0_DESI, wa_DESI)
w_LCDM = np.full_like(z_arr, -1.0)

print(f"\nw(z) comparison at key redshifts (alpha = {alpha_best:.4f}):")
print(f"{'z':>6s}  {'w_shield':>10s}  {'w_DESI':>10s}  {'w_LCDM':>10s}  {'diff':>10s}")
for z_test in [0.0, 0.2, 0.5, 0.8, 1.0, 1.5, 2.0, 2.5, 3.0]:
    ws = w_eff(z_test, alpha_best)
    wd = w_w0wa(z_test, w0_DESI, wa_DESI)
    print(f"{z_test:6.1f}  {ws:10.4f}  {wd:10.4f}  {-1.0:10.4f}  {ws-wd:10.4f}")


# ============================================================
# SECTION 7: FRIEDMANN EQUATION CONSISTENCY
# ============================================================
print("\n" + "=" * 70)
print("SECTION 6: FRIEDMANN EQUATION CONSISTENCY")
print("=" * 70)

def Hz_shielding(z, alpha):
    """H(z)/H0 for the shielding model."""
    Om = Omega_m0 * (1 + z)**3
    ODE = rho_DE_eff(z, alpha)
    total = Om + ODE
    if total < 0:
        return np.nan
    return np.sqrt(total)

def Hz_w0wa(z, w0, wa):
    """H(z)/H0 for w0-wa dark energy."""
    a = 1.0 / (1 + z)
    # rho_DE(a)/rho_DE(1) = a^(-3(1+w0+wa)) * exp(-3*wa*(1-a))
    rho_ratio = a**(-3*(1+w0+wa)) * np.exp(-3*wa*(1-a))
    Om = Omega_m0 * (1 + z)**3
    ODE = Omega_Lambda0 * rho_ratio
    return np.sqrt(Om + ODE)

def Hz_LCDM(z):
    """H(z)/H0 for LCDM."""
    return np.sqrt(Omega_m0 * (1+z)**3 + Omega_Lambda0)

# Comoving distance
def comoving_distance(z, Hz_func, *args):
    """d_C = c/H0 * integral_0^z dz'/E(z') where E=H/H0"""
    result, _ = quad(lambda zp: 1.0/Hz_func(zp, *args), 0, z)
    return (c_km_s / H0) * result  # in Mpc

# Luminosity distance
def luminosity_distance(z, Hz_func, *args):
    dc = comoving_distance(z, Hz_func, *args)
    return (1 + z) * dc

# Distance modulus
def distance_modulus(z, Hz_func, *args):
    dL = luminosity_distance(z, Hz_func, *args)
    return 5 * np.log10(dL) + 25  # for dL in Mpc

print(f"\nDistance modulus comparison:")
print(f"{'z':>6s}  {'mu_shield':>10s}  {'mu_w0wa':>10s}  {'mu_LCDM':>10s}  {'shield-LCDM':>12s}  {'w0wa-LCDM':>12s}")

z_dist = [0.1, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0]
for z_test in z_dist:
    mu_s = distance_modulus(z_test, Hz_shielding, alpha_best)
    mu_w = distance_modulus(z_test, Hz_w0wa, w0_DESI, wa_DESI)
    mu_L = distance_modulus(z_test, Hz_LCDM)
    print(f"{z_test:6.1f}  {mu_s:10.4f}  {mu_w:10.4f}  {mu_L:10.4f}  {mu_s-mu_L:12.4f}  {mu_w-mu_L:12.4f}")

# BAO observable: D_V/r_d (volume-averaged distance)
def DV_over_rd(z, Hz_func, *args):
    """D_V(z) = [z * d_C(z)^2 * c/(H(z))]^(1/3)"""
    dc = comoving_distance(z, Hz_func, *args)
    Hz = Hz_func(z, *args) * H0  # in km/s/Mpc
    DV = (z * dc**2 * c_km_s / Hz)**(1.0/3.0)
    return DV  # in Mpc (would divide by r_d for BAO, but ratio is same)

print(f"\nD_V(z) comparison (Mpc):")
print(f"{'z':>6s}  {'DV_shield':>10s}  {'DV_w0wa':>10s}  {'DV_LCDM':>10s}  {'shield/LCDM':>12s}  {'w0wa/LCDM':>12s}")
z_bao = [0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 2.5]
for z_test in z_bao:
    dv_s = DV_over_rd(z_test, Hz_shielding, alpha_best)
    dv_w = DV_over_rd(z_test, Hz_w0wa, w0_DESI, wa_DESI)
    dv_L = DV_over_rd(z_test, Hz_LCDM)
    print(f"{z_test:6.1f}  {dv_s:10.2f}  {dv_w:10.2f}  {dv_L:10.2f}  {dv_s/dv_L:12.6f}  {dv_w/dv_L:12.6f}")


# ============================================================
# SECTION 8: PREDICTIONS AT HIGH z
# ============================================================
print("\n" + "=" * 70)
print("SECTION 7: PREDICTIONS AT HIGH REDSHIFT")
print("=" * 70)

print(f"\nNovel predictions of the shielding model (alpha = {alpha_best:.4f}):")
print(f"{'z':>6s}  {'w_shield':>10s}  {'w_DESI_extrap':>14s}  {'difference':>10s}")
for z_test in [2.0, 2.5, 3.0, 4.0, 5.0, 7.0, 10.0, 20.0, 50.0, 100.0]:
    ws = w_eff(z_test, alpha_best)
    wd = w_w0wa(z_test, w0_DESI, wa_DESI)
    if np.isfinite(ws):
        print(f"{z_test:6.1f}  {ws:10.4f}  {wd:14.4f}  {ws-wd:10.4f}")
    else:
        print(f"{z_test:6.1f}  {'NaN':>10s}  {wd:14.4f}  {'---':>10s}")

# Check: at what z does rho_DE_eff go to zero?
# rho_DE_eff(z) = Omega_L + alpha*Omega_m*((1+z)^3 - 1) = 0
# (1+z)^3 = 1 + Omega_L/(alpha*Omega_m)   [for alpha < 0, this can happen]
# For alpha > 0 and the formula: rho_DE goes UP with z, never zero.
# Actually for alpha > 0: rho_bare = Omega_L - alpha*Omega_m
# If alpha > Omega_L/Omega_m, rho_bare < 0, which is unphysical.
alpha_max = Omega_Lambda0 / Omega_m0
print(f"\nPhysical constraint: rho_bare >= 0 requires alpha <= {alpha_max:.4f}")
print(f"Our best-fit alpha = {alpha_best:.4f}")
rho_bare = Omega_Lambda0 - alpha_best * Omega_m0
print(f"rho_bare / rho_crit = {rho_bare:.4f}")

# At high z, rho_DE_eff -> alpha * Omega_m * (1+z)^3
# This scales like MATTER, not like a cosmological constant.
# So the "dark energy" at high z is just extra matter-like stuff.
# The effective w -> -1 + 1 = 0 (matter-like) at very high z.
# Actually let's check:
print(f"\nAsymptotic behavior at high z:")
print(f"  rho_DE_eff(z) ~ alpha*Omega_m*(1+z)^3 = {alpha_best*Omega_m0:.4f} * (1+z)^3")
print(f"  This looks like extra matter with Omega_extra = {alpha_best*Omega_m0:.4f}")
print(f"  So w_eff -> -1 + 1 = 0 (matter-like) at high z")
print(f"  The model predicts DE becomes matter-like at high z,")
print(f"  which is VERY different from w0-wa extrapolation.")


# ============================================================
# SECTION 9: HONEST ASSESSMENT
# ============================================================
print("\n" + "=" * 70)
print("SECTION 8: HONEST ASSESSMENT")
print("=" * 70)

# The key structural issue
print(f"""
STRUCTURAL ANALYSIS OF THE MODEL:

1. PARAMETER COUNT:
   The model has 1 free parameter (alpha) mapping to 2 observables (w0, wa).
   This is good — it makes a testable prediction (a curve in w0-wa space).

2. THE CURVE IN (w0, wa) SPACE:
   w0 = -1 + r,  where r = alpha * Omega_m / Omega_L
   wa = 3r(1-r)

   Eliminating r: r = w0 + 1, so:
   wa = 3(w0+1)(1-(w0+1)) = 3(w0+1)(-w0) = -3*w0*(w0+1)

   This is a PARABOLA in (w0, wa) space passing through (-1, 0) [LCDM].

   At w0 = {w0_DESI}: wa_predicted = {-3*w0_DESI*(w0_DESI+1):.4f}
   DESI measured: wa = {wa_DESI}

   The model predicts wa = {-3*w0_DESI*(w0_DESI+1):.4f} while DESI measures wa = {wa_DESI}.

   SIGN MISMATCH: The model predicts wa > 0, but DESI measures wa < 0!

   This is a FUNDAMENTAL problem. The shielding model traces out a curve
   where w0 > -1 implies wa > 0, but DESI finds w0 > -1 with wa < 0.

3. GEOMETRIC INTERPRETATION:
   - Model: w(z) starts at w0 > -1 and approaches -1 at high z
     (because the matter-like correction becomes dominant and
     rho_DE_eff ~ (1+z)^3, giving w -> 0, wait no...)

   Actually, let me reconsider. For w0 > -1 (alpha > 0):
   - At z=0: w = w0 > -1
   - At moderate z: w increases further from -1 (becomes less negative)
   - At very high z: w -> 0 (matter-like)

   So w(z) INCREASES monotonically from w0 toward 0.
   In w0-wa: wa > 0 means w decreases toward past (dw/dz < 0 at z~0).
   Wait, let me get the sign right.

   w(a) = w0 + wa*(1-a). At a=1 (z=0): w = w0.
   As a decreases (z increases): w = w0 + wa*(1-a).
   If wa > 0: w increases as a decreases (z increases).
   That means w gets LESS negative at high z. ✓ Consistent with model.

   But DESI has wa < 0: w DECREASES as z increases, going MORE negative.
   DESI says dark energy was MORE phantom-like in the past.

   The shielding model says the OPPOSITE: DE was MORE matter-like in the past.

4. CONCLUSION:
   The simplest matter-shielding model FAILS to reproduce DESI's signal.
   The failure is not quantitative but QUALITATIVE:
   - DESI: w crosses -1 from below, w was more negative in the past
   - Model: w is always > -1 (for the quintessence branch) or always < -1 (phantom branch)
   - Neither branch can produce the w-crossing behavior DESI sees.

   The chi2 of the best fit tells the story:
   chi2_min = {chi2_best:.2f} for 1 free parameter.
   This is {'acceptable' if chi2_best < 4 else 'poor' if chi2_best < 10 else 'very poor'}.
""")

# Also test: what if we flip sign (matter removes DE)?
print("\nChecking the OPPOSITE sign (alpha < 0, true shielding):")
alpha_neg = -abs(alpha_target_w0)
w0_neg, wa_neg = map_to_w0wa(alpha_neg)
print(f"  alpha = {alpha_neg:.4f}")
print(f"  w0 = {w0_neg:.4f} (< -1, phantom)")
print(f"  wa = {wa_neg:.4f}")
print(f"  DESI wants w0 > -1, so this is worse.")

# What about matching wa instead?
# wa = 3r(1-r) = -0.86 => 3r - 3r^2 = -0.86 => 3r^2 - 3r - 0.86 = 0
# r = (3 +/- sqrt(9 + 4*3*0.86)) / 6 = (3 +/- sqrt(9+10.32))/6
discriminant = 9 + 4*3*0.86
r_solutions = [(3 + np.sqrt(discriminant))/6, (3 - np.sqrt(discriminant))/6]
print(f"\nTo match wa = {wa_DESI}:")
for r_sol in r_solutions:
    w0_sol = -1 + r_sol
    wa_check = 3*r_sol*(1-r_sol)
    print(f"  r = {r_sol:.4f}, w0 = {w0_sol:.4f}, wa = {wa_check:.4f}")
print(f"  Neither solution gives w0 close to {w0_DESI}")


# ============================================================
# SECTION 10: EXTENDED MODEL — QUADRATIC SHIELDING
# ============================================================
print("\n" + "=" * 70)
print("SECTION 9: EXTENDED MODEL — CAN WE SAVE IT?")
print("=" * 70)

print("""
The linear shielding model fails because it produces the wrong sign for wa.
Can we modify it?

Option A: rho_DE_eff = rho_bare - alpha * rho_m(z) [original, alpha > 0]
  This gives w < -1 everywhere. Does NOT match w0 > -1 from DESI.

Option B: rho_DE_eff = rho_bare + alpha * rho_m(z) [alpha > 0]
  This gives w > -1 and wa > 0. Matches w0 but NOT wa.

Option C: Nonlinear shielding with 2 parameters:
  rho_DE_eff = rho_bare + alpha * rho_m - beta * rho_m^2

  Two free parameters for two observables (w0, wa). Guaranteed to fit.
  But this is trivially curve-fitting with enough parameters.

Option D: Shielding depends on structure formation, not just density.
  Replace rho_m(z) with sigma8(z) * rho_m(z) or similar.
  Structure forms LATE, so the effective coupling is weaker at high z
  than simple (1+z)^3 scaling would suggest.
  This COULD flip the sign of wa, but requires a specific model.

Let's test Option D briefly — replace (1+z)^3 with a growth-modified term.
""")

# Growth factor (approximate fitting formula from Carroll, Press & Turner 1992)
def growth_factor(z, Omega_m=Omega_m0, Omega_L=Omega_Lambda0):
    """Approximate linear growth factor D(z), normalized to D(0)=1."""
    a = 1.0 / (1 + z)
    Om_z = Omega_m * (1+z)**3 / (Omega_m*(1+z)**3 + Omega_L)
    OL_z = Omega_L / (Omega_m*(1+z)**3 + Omega_L)
    D = (5.0/2.0) * a * Om_z / (Om_z**(4.0/7.0) - OL_z + (1 + Om_z/2.0)*(1 + OL_z/70.0))
    D0 = (5.0/2.0) * 1.0 * Omega_m / (Omega_m**(4.0/7.0) - Omega_L + (1 + Omega_m/2.0)*(1 + Omega_L/70.0))
    return D / D0

# Model D: rho_DE_eff = rho_bare + alpha * D(z) * rho_m(z)
# where D(z) is the growth factor (D(0)=1, D(z>0)<1)
# This means the coupling is WEAKER at high z (less structure)

def rho_DE_model_D(z, alpha):
    D = growth_factor(z)
    return Omega_Lambda0 + alpha * Omega_m0 * (D * (1+z)**3 - 1)

def w_eff_model_D(z, alpha):
    rho = rho_DE_model_D(z, alpha)
    if np.isscalar(z):
        if rho <= 0:
            return np.nan

    # Numerical derivative
    dz = 1e-6
    drho = (rho_DE_model_D(z+dz, alpha) - rho_DE_model_D(z-dz, alpha)) / (2*dz)
    return -1.0 + (1+z) * drho / (3.0 * rho)

def map_model_D_to_w0wa(alpha):
    z_fit = np.linspace(0, 2, 200)
    w_model = np.array([w_eff_model_D(zi, alpha) for zi in z_fit])
    mask = np.isfinite(w_model)
    z_fit = z_fit[mask]
    w_model = w_model[mask]
    if len(z_fit) < 10:
        return np.nan, np.nan
    def cost(params):
        w0, wa = params
        w_approx = w_w0wa(z_fit, w0, wa)
        return np.sum((w_model - w_approx)**2)
    res = minimize(cost, [-0.8, -0.5], method='Nelder-Mead')
    return res.x[0], res.x[1]

def chi2_model_D(alpha):
    w0, wa = map_model_D_to_w0wa(alpha)
    if np.isnan(w0) or np.isnan(wa):
        return 1e10
    dw0 = w0 - w0_DESI
    dwa = wa - wa_DESI
    s0 = w0_DESI_err
    sa = wa_DESI_err
    r = rho_w0wa
    return (1/(1-r**2)) * ((dw0/s0)**2 + (dwa/sa)**2 - 2*r*dw0*dwa/(s0*sa))

print("\nModel D: Growth-modified shielding")
print(f"{'alpha':>8s}  {'w0':>8s}  {'wa':>8s}  {'chi2':>8s}")
for a_test in np.linspace(-1.5, 1.5, 25):
    w0t, wat = map_model_D_to_w0wa(a_test)
    c2 = chi2_model_D(a_test)
    if np.isfinite(w0t):
        print(f"{a_test:8.2f}  {w0t:8.4f}  {wat:8.4f}  {c2:8.2f}")

# Find best alpha for model D
res_D = minimize_scalar(chi2_model_D, bounds=(-2, 2), method='bounded')
alpha_D_best = res_D.x
chi2_D_best = res_D.fun
w0_D, wa_D = map_model_D_to_w0wa(alpha_D_best)

print(f"\nBest-fit Model D:")
print(f"  alpha = {alpha_D_best:.4f}")
print(f"  chi2 = {chi2_D_best:.4f}")
print(f"  (w0, wa) = ({w0_D:.4f}, {wa_D:.4f})")
print(f"  DESI: ({w0_DESI}, {wa_DESI})")


# ============================================================
# SECTION 11: ALSO TEST NEGATIVE-ALPHA (TRUE SHIELDING)
# WITH GROWTH FACTOR
# ============================================================
print("\n\nModel D with negative alpha (true shielding + growth):")
for a_test in np.linspace(-2.0, -0.01, 25):
    w0t, wat = map_model_D_to_w0wa(a_test)
    c2 = chi2_model_D(a_test)
    if np.isfinite(w0t) and np.isfinite(c2):
        print(f"  alpha={a_test:7.3f}  w0={w0t:8.4f}  wa={wat:8.4f}  chi2={c2:8.2f}")


# ============================================================
# PLOTTING
# ============================================================
print("\n" + "=" * 70)
print("GENERATING PLOTS")
print("=" * 70)

outdir = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/"

# --- PLOT 1: w(z) comparison ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Left: Linear model
ax = axes[0]
z_plot = np.linspace(0, 3, 500)

# Multiple alpha values for the linear model
for alpha_val, ls, lbl in [
    (alpha_best, '-', f'Shielding (best fit, α={alpha_best:.3f})'),
    (alpha_target_w0, '--', f'Shielding (match w0, α={alpha_target_w0:.3f})')
]:
    w_s = [w_eff(z, alpha_val) for z in z_plot]
    ax.plot(z_plot, w_s, ls, linewidth=2, label=lbl)

ax.plot(z_plot, w_w0wa(z_plot, w0_DESI, wa_DESI), 'r-', linewidth=2,
        label=f'DESI best fit (w0={w0_DESI}, wa={wa_DESI})')
ax.axhline(-1, color='gray', linestyle=':', linewidth=1, label='ΛCDM (w=-1)')
ax.fill_between(z_plot,
                w_w0wa(z_plot, w0_DESI - w0_DESI_err, wa_DESI - wa_DESI_err),
                w_w0wa(z_plot, w0_DESI + w0_DESI_err, wa_DESI + wa_DESI_err),
                alpha=0.2, color='red', label='DESI ~1σ band')
ax.set_xlabel('Redshift z', fontsize=14)
ax.set_ylabel('w(z)', fontsize=14)
ax.set_title('Linear Shielding Model vs DESI', fontsize=14)
ax.legend(fontsize=10)
ax.set_ylim(-2.5, 0.5)
ax.set_xlim(0, 3)
ax.grid(True, alpha=0.3)

# Right: Growth-modified model
ax = axes[1]

w_D = [w_eff_model_D(z, alpha_D_best) for z in z_plot]
ax.plot(z_plot, w_D, 'b-', linewidth=2,
        label=f'Growth-modified (α={alpha_D_best:.3f})')

ax.plot(z_plot, w_w0wa(z_plot, w0_DESI, wa_DESI), 'r-', linewidth=2,
        label=f'DESI best fit')
ax.axhline(-1, color='gray', linestyle=':', linewidth=1, label='ΛCDM')
ax.fill_between(z_plot,
                w_w0wa(z_plot, w0_DESI - w0_DESI_err, wa_DESI - wa_DESI_err),
                w_w0wa(z_plot, w0_DESI + w0_DESI_err, wa_DESI + wa_DESI_err),
                alpha=0.2, color='red', label='DESI ~1σ band')
ax.set_xlabel('Redshift z', fontsize=14)
ax.set_ylabel('w(z)', fontsize=14)
ax.set_title('Growth-Modified Model vs DESI', fontsize=14)
ax.legend(fontsize=10)
ax.set_ylim(-2.5, 0.5)
ax.set_xlim(0, 3)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(outdir, 'w_of_z_comparison.png'), dpi=150, bbox_inches='tight')
plt.close()
print("Saved: w_of_z_comparison.png")


# --- PLOT 2: (w0, wa) parameter space ---
fig, ax = plt.subplots(figsize=(10, 8))

# DESI confidence ellipses
for nsig, alpha_ell in [(1, 0.3), (2, 0.15)]:
    # Ellipse from covariance matrix
    cov = np.array([[w0_DESI_err**2, rho_w0wa*w0_DESI_err*wa_DESI_err],
                     [rho_w0wa*w0_DESI_err*wa_DESI_err, wa_DESI_err**2]])
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    angle = np.degrees(np.arctan2(eigenvectors[1,1], eigenvectors[0,1]))
    # For 2D Gaussian: 1sigma -> chi2=2.30, 2sigma -> chi2=6.18
    chi2_thresholds = {1: 2.30, 2: 6.18}
    width = 2 * np.sqrt(eigenvalues[1] * chi2_thresholds[nsig])
    height = 2 * np.sqrt(eigenvalues[0] * chi2_thresholds[nsig])
    ell = Ellipse(xy=(w0_DESI, wa_DESI), width=width, height=height, angle=angle,
                  facecolor='red', alpha=alpha_ell, edgecolor='red', linewidth=2,
                  label=f'DESI {nsig}σ')
    ax.add_patch(ell)

# Model curve (linear shielding)
alpha_range = np.linspace(-0.5, 1.5, 1000)
w0_curve = np.array([map_to_w0wa(a)[0] for a in alpha_range])
wa_curve = np.array([map_to_w0wa(a)[1] for a in alpha_range])
ax.plot(w0_curve, wa_curve, 'b-', linewidth=2.5, label='Linear shielding model')

# Model curve (growth-modified)
w0_D_curve = []
wa_D_curve = []
alpha_D_range = np.linspace(-1.5, 1.5, 200)
for a in alpha_D_range:
    w0t, wat = map_model_D_to_w0wa(a)
    w0_D_curve.append(w0t)
    wa_D_curve.append(wat)
ax.plot(w0_D_curve, wa_D_curve, 'g--', linewidth=2.5, label='Growth-modified model')

# Mark key points
ax.plot(-1, 0, 'ko', markersize=10, label='ΛCDM', zorder=5)
ax.plot(w0_DESI, wa_DESI, 'r*', markersize=15, label='DESI best fit', zorder=5)
ax.plot(w0_best, wa_best, 'bs', markersize=10, label=f'Linear best α={alpha_best:.3f}', zorder=5)
ax.plot(w0_D, wa_D, 'gD', markersize=10, label=f'Growth best α={alpha_D_best:.3f}', zorder=5)

# Mark alpha values along the curve
for a_mark in [0.0, 0.2, 0.5, 0.8, 1.0]:
    w0m, wam = map_to_w0wa(a_mark)
    ax.annotate(f'α={a_mark}', (w0m, wam), fontsize=8,
                textcoords="offset points", xytext=(10, 5))

ax.set_xlabel('w0', fontsize=14)
ax.set_ylabel('wa', fontsize=14)
ax.set_title('(w0, wa) Parameter Space: Shielding Models vs DESI DR2', fontsize=14)
ax.legend(fontsize=10, loc='upper left')
ax.set_xlim(-1.5, 0.0)
ax.set_ylim(-2.5, 2.0)
ax.grid(True, alpha=0.3)
ax.axhline(0, color='gray', linewidth=0.5)
ax.axvline(-1, color='gray', linewidth=0.5)

plt.tight_layout()
plt.savefig(os.path.join(outdir, 'w0_wa_parameter_space.png'), dpi=150, bbox_inches='tight')
plt.close()
print("Saved: w0_wa_parameter_space.png")


# --- PLOT 3: Distance measures ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

z_dist_arr = np.linspace(0.01, 3, 200)

# Luminosity distance ratio to LCDM
ax = axes[0]
dL_LCDM = np.array([luminosity_distance(z, Hz_LCDM) for z in z_dist_arr])
dL_shield = np.array([luminosity_distance(z, Hz_shielding, alpha_best) for z in z_dist_arr])
dL_w0wa = np.array([luminosity_distance(z, Hz_w0wa, w0_DESI, wa_DESI) for z in z_dist_arr])

ax.plot(z_dist_arr, dL_shield/dL_LCDM - 1, 'b-', linewidth=2,
        label=f'Linear shielding (α={alpha_best:.3f})')
ax.plot(z_dist_arr, dL_w0wa/dL_LCDM - 1, 'r-', linewidth=2,
        label='DESI w0-wa')
ax.axhline(0, color='gray', linestyle=':', linewidth=1)
ax.set_xlabel('Redshift z', fontsize=14)
ax.set_ylabel('$d_L / d_{L,ΛCDM} - 1$', fontsize=14)
ax.set_title('Luminosity Distance Deviation from ΛCDM', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

# H(z) ratio
ax = axes[1]
Hz_L = np.array([Hz_LCDM(z) for z in z_dist_arr])
Hz_S = np.array([Hz_shielding(z, alpha_best) for z in z_dist_arr])
Hz_W = np.array([Hz_w0wa(z, w0_DESI, wa_DESI) for z in z_dist_arr])

ax.plot(z_dist_arr, Hz_S/Hz_L - 1, 'b-', linewidth=2,
        label=f'Linear shielding (α={alpha_best:.3f})')
ax.plot(z_dist_arr, Hz_W/Hz_L - 1, 'r-', linewidth=2,
        label='DESI w0-wa')
ax.axhline(0, color='gray', linestyle=':', linewidth=1)
ax.set_xlabel('Redshift z', fontsize=14)
ax.set_ylabel('$H(z) / H_{ΛCDM}(z) - 1$', fontsize=14)
ax.set_title('Hubble Parameter Deviation from ΛCDM', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(outdir, 'distance_measures.png'), dpi=150, bbox_inches='tight')
plt.close()
print("Saved: distance_measures.png")


# --- PLOT 4: High-z predictions ---
fig, ax = plt.subplots(figsize=(10, 7))

z_highz = np.linspace(0, 10, 1000)

w_shield_hz = [w_eff(z, alpha_best) for z in z_highz]
w_DESI_hz = w_w0wa(z_highz, w0_DESI, wa_DESI)
w_D_hz = [w_eff_model_D(z, alpha_D_best) for z in z_highz]

ax.plot(z_highz, w_shield_hz, 'b-', linewidth=2,
        label=f'Linear shielding (α={alpha_best:.3f})')
ax.plot(z_highz, w_D_hz, 'g--', linewidth=2,
        label=f'Growth-modified (α={alpha_D_best:.3f})')
ax.plot(z_highz, w_DESI_hz, 'r-', linewidth=2,
        label='DESI w0-wa extrapolation')
ax.axhline(-1, color='gray', linestyle=':', linewidth=1, label='ΛCDM')
ax.axhline(0, color='orange', linestyle=':', linewidth=1, alpha=0.5, label='w=0 (matter)')
ax.axhspan(-1.5, -0.5, xmin=0, xmax=0.3, alpha=0.05, color='red')

# Shade DESI-constrained region
ax.axvspan(0, 2.1, alpha=0.05, color='blue', label='DESI constrained (z<2.1)')
ax.axvspan(2.1, 10, alpha=0.05, color='green', label='Prediction region (z>2.1)')

ax.set_xlabel('Redshift z', fontsize=14)
ax.set_ylabel('w(z)', fontsize=14)
ax.set_title('High-z Predictions: Where Models Diverge', fontsize=14)
ax.legend(fontsize=10, loc='lower left')
ax.set_ylim(-3, 1)
ax.set_xlim(0, 10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(outdir, 'high_z_predictions.png'), dpi=150, bbox_inches='tight')
plt.close()
print("Saved: high_z_predictions.png")


# --- PLOT 5: chi2 as function of alpha ---
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

ax = axes[0]
alpha_scan = np.linspace(-1, 2, 500)
chi2_scan = [chi2_w0wa(a, True) for a in alpha_scan]
ax.plot(alpha_scan, chi2_scan, 'b-', linewidth=2)
ax.axhline(1, color='gray', linestyle='--', alpha=0.5, label='χ²=1')
ax.axhline(4, color='gray', linestyle=':', alpha=0.5, label='χ²=4 (2σ)')
ax.axhline(9, color='gray', linestyle='-.', alpha=0.5, label='χ²=9 (3σ)')
ax.set_xlabel('α (shielding parameter)', fontsize=14)
ax.set_ylabel('χ² (vs DESI)', fontsize=14)
ax.set_title('Linear Shielding: χ² vs α', fontsize=14)
ax.set_ylim(0, 30)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

ax = axes[1]
chi2_D_scan = [chi2_model_D(a) for a in alpha_scan]
ax.plot(alpha_scan, chi2_D_scan, 'g-', linewidth=2)
ax.axhline(1, color='gray', linestyle='--', alpha=0.5, label='χ²=1')
ax.axhline(4, color='gray', linestyle=':', alpha=0.5, label='χ²=4 (2σ)')
ax.axhline(9, color='gray', linestyle='-.', alpha=0.5, label='χ²=9 (3σ)')
ax.set_xlabel('α (shielding parameter)', fontsize=14)
ax.set_ylabel('χ² (vs DESI)', fontsize=14)
ax.set_title('Growth-Modified: χ² vs α', fontsize=14)
ax.set_ylim(0, 30)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(outdir, 'chi2_vs_alpha.png'), dpi=150, bbox_inches='tight')
plt.close()
print("Saved: chi2_vs_alpha.png")


# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)

print(f"""
QUESTION: Does matter density evolution predict DESI's dark energy signal?

ANSWER: NO — the simplest version of this hypothesis FAILS qualitatively.

DETAILED FINDINGS:

1. LINEAR SHIELDING MODEL: rho_DE_eff = rho_bare + alpha * rho_m(z)

   This model produces a one-parameter curve in (w0, wa) space:
     wa = -3 * w0 * (w0 + 1)

   This is a downward-opening parabola passing through LCDM (-1, 0).

   For w0 > -1 (as DESI finds), the model predicts wa > 0.
   But DESI measures wa < 0.

   THE SIGN OF wa IS WRONG. This is a qualitative, not quantitative, failure.

   Best fit: alpha = {alpha_best:.4f}, chi2 = {chi2_best:.1f}
   Predicted: (w0, wa) = ({w0_best:.3f}, {wa_best:.3f})
   DESI:      (w0, wa) = ({w0_DESI}, {wa_DESI})

2. GROWTH-MODIFIED MODEL: rho_DE_eff = rho_bare + alpha * D(z) * rho_m(z)

   Including the growth factor modifies the curve shape but does not
   fundamentally change the topology. The model still cannot simultaneously
   achieve w0 > -1 and wa < 0 within the DESI confidence region.

   Best fit: alpha = {alpha_D_best:.4f}, chi2 = {chi2_D_best:.1f}
   Predicted: (w0, wa) = ({w0_D:.3f}, {wa_D:.3f})

3. PHYSICAL INTERPRETATION:

   The shielding model says: "DE was different in the past because matter
   was denser." If matter ADDS to effective DE (alpha > 0), then DE was
   LARGER in the past, so it dilutes over time → w > -1. But this means
   w gets CLOSER to -1 at high z (when matter dominates and the fractional
   correction is small compared to total energy), giving wa > 0.

   DESI says the opposite: w was MORE NEGATIVE than -1 in the past,
   crossing the phantom divide. No simple matter-scaling model produces this.

4. WHAT WOULD WORK:

   To get wa < 0 with w0 > -1, you need dark energy that:
   - Is slightly less negative than -1 today (quintessence-like)
   - Was MORE negative than -1 in the past (phantom-like)
   - Crossed the phantom divide w = -1

   This requires a scalar field that rolls UP its potential, or an
   interaction that changes sign, or a multi-component dark energy.
   Simple matter-density scaling cannot produce phantom crossing.

5. THE MODEL IS NOT GARBAGE — IT'S INSTRUCTIVE:

   It cleanly demonstrates WHY simple matter-DE coupling fails:
   the matter density is a MONOTONIC function of redshift, so any
   linear coupling produces a MONOTONIC w(z) that cannot cross w = -1.
   The DESI signal, if real, requires non-monotonic dark energy physics.
""")

print("All plots saved to:", outdir)
print("Script complete.")
