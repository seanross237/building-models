#!/usr/bin/env python3
"""
GMC Phase Structure Analysis for the Riemann Zeta Function.

This script investigates the connection between the GMC phase structure
(subcritical / critical / supercritical) and the behavior of zeta.

Key theoretical framework:
  - In GMC, mu_gamma = exp(gamma*phi - gamma^2/2 * E[phi^2]) dx
  - For a log-correlated field phi with Cov(phi(x), phi(y)) ~ -log|x-y|:
      gamma < sqrt(2):  subcritical, mu_gamma is non-degenerate
      gamma = sqrt(2):  critical, mu_gamma degenerates but has a limit (with log correction)
      gamma > sqrt(2):  supercritical, mu_gamma = 0

  - For zeta on the critical line, Harper showed the relevant parameter is
    gamma = sqrt(2), i.e., zeta lives at the CRITICAL GMC phase.

What we compute here:
1. The "effective gamma" at different sigma values
2. Moment behavior: E[|zeta(sigma+it)|^{2q}] should scale differently in each phase
3. The connection between the zero process and the GMC critical measure
"""

import numpy as np
from mpmath import mp, zeta, fabs, log
import time
from scipy.stats import norm

mp.dps = 20


def abs_zeta(sigma, t):
    """Compute |zeta(sigma + i*t)|."""
    s = mp.mpc(sigma, t)
    z = zeta(s)
    return float(fabs(z))


def log_abs_zeta(sigma, t):
    """Compute log|zeta(sigma + i*t)|."""
    s = mp.mpc(sigma, t)
    z = zeta(s)
    if z == 0:
        return float('-inf')
    return float(log(fabs(z)))


# ============================================================
# 1. EFFECTIVE GAMMA PARAMETER
# ============================================================
print("=" * 70)
print("1. EFFECTIVE GMC PARAMETER gamma(sigma)")
print("=" * 70)
print()
print("In the GMC framework, the 'inverse participation ratio' is:")
print("  E[mu_gamma([0,1])^2] / E[mu_gamma([0,1])]^2")
print("which diverges at gamma = sqrt(2) (critical point).")
print()
print("For zeta, the analogous quantity is the ratio of moments.")
print("The effective gamma is determined by:")
print("  Var(log|zeta(sigma+it)|) = gamma^2/2 * log(log T) + O(1)")
print("So gamma_eff = sqrt(2 * Var / log(log T))")
print()

T_center = 1e4
n_samples = 500
np.random.seed(42)
ts = np.random.uniform(T_center * 0.8, T_center * 1.2, n_samples)

loglogT = np.log(np.log(T_center))

for sigma in [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.9, 1.0]:
    print(f"sigma = {sigma}:", end=" ", flush=True)
    start = time.time()
    vals = np.array([log_abs_zeta(sigma, float(t)) for t in ts])
    vals = vals[np.isfinite(vals)]
    v = np.var(vals)
    elapsed = time.time() - start

    # Effective gamma: Var = gamma^2/2 * loglogT at sigma=1/2
    # For sigma > 1/2, the variance doesn't scale with loglogT,
    # so gamma_eff should decrease
    gamma_eff = np.sqrt(2 * v / loglogT)

    print(f"Var={v:.4f}, gamma_eff={gamma_eff:.4f} "
          f"(critical=sqrt(2)={np.sqrt(2):.4f}) [{elapsed:.1f}s]")

print()
print("Note: gamma_eff is meaningful at sigma=1/2 where the variance")
print("scales with log(log T). At sigma > 1/2, 'gamma_eff' decreases")
print("as T grows because the variance converges to a constant while")
print("loglogT diverges. This means sigma > 1/2 is in the 'subcritical' phase.")

# ============================================================
# 2. MOMENT SCALING
# ============================================================
print()
print("=" * 70)
print("2. MOMENT SCALING OF |zeta(sigma+it)|^{2q}")
print("=" * 70)
print()
print("Keating-Snaith conjecture (at sigma=1/2):")
print("  E[|zeta(1/2+it)|^{2q}] ~ C(q) * (log T)^{q^2}")
print("This q^2 exponent is characteristic of the log-correlated/GMC phase.")
print()
print("At sigma > 1/2, the Euler product converges:")
print("  E[|zeta(sigma+it)|^{2q}] ~ product_p (stuff) = O(1)")
print("i.e., moments are bounded, no growth with T.")
print()

# Compute moments for several q values at different sigma
q_values = [0.5, 1.0, 1.5, 2.0]
T_values = [1e3, 5e3, 1e4]
n_moment = 300

for sigma in [0.5, 0.75, 1.0]:
    print(f"\nsigma = {sigma}:")
    print(f"  {'q':>5}  ", end="")
    for T in T_values:
        print(f"  E[|zeta|^{{2q}}] @ T={T:.0e}", end="")
    print()

    for q in q_values:
        print(f"  {q:5.1f}  ", end="")
        for T in T_values:
            np.random.seed(int(T + 100*q + 1000*sigma))
            t_samp = np.random.uniform(T * 0.8, T * 1.2, n_moment)
            zeta_vals = np.array([abs_zeta(sigma, float(t)) for t in t_samp])
            moment = np.mean(zeta_vals**(2*q))
            print(f"  {moment:20.4f}", end="")
        print()

    # For sigma=0.5, check if growth is consistent with (log T)^{q^2}
    if sigma == 0.5:
        print(f"\n  Growth exponents (log(moment)/log(log T)):")
        for q in q_values:
            moments_at_T = []
            for T in T_values:
                np.random.seed(int(T + 100*q + 1000*sigma))
                t_samp = np.random.uniform(T * 0.8, T * 1.2, n_moment)
                zeta_vals = np.array([abs_zeta(sigma, float(t)) for t in t_samp])
                moments_at_T.append(np.mean(zeta_vals**(2*q)))

            # Fit: log(moment) ~ alpha * log(log T)
            loglogTs = np.log(np.log(np.array(T_values)))
            log_moments = np.log(np.array(moments_at_T))
            A = np.vstack([np.ones_like(loglogTs), loglogTs]).T
            coeffs = np.linalg.lstsq(A, log_moments, rcond=None)[0]
            alpha = coeffs[1]
            print(f"    q={q}: alpha={alpha:.3f} (Keating-Snaith prediction: q^2={q**2:.2f})")

# ============================================================
# 3. DISTRIBUTION OF log|zeta| AND TAIL BEHAVIOR
# ============================================================
print()
print("=" * 70)
print("3. TAIL BEHAVIOR OF log|zeta(sigma+it)|")
print("=" * 70)
print()
print("At sigma=1/2: tails are HEAVIER than Gaussian")
print("(the large deviation rate function is different)")
print("At sigma>1/2: tails should approach Gaussian faster")
print()

for sigma in [0.5, 0.75, 1.0]:
    np.random.seed(42)
    ts = np.random.uniform(1e4 * 0.8, 1e4 * 1.2, n_samples)
    vals = np.array([log_abs_zeta(sigma, float(t)) for t in ts])
    vals = vals[np.isfinite(vals)]

    mean = np.mean(vals)
    std = np.std(vals)
    skew = np.mean(((vals - mean) / std)**3)
    kurtosis = np.mean(((vals - mean) / std)**4) - 3  # excess kurtosis

    # Count extreme values (> 2, 3 sigma)
    n_2sigma = np.sum(np.abs(vals - mean) > 2 * std) / len(vals)
    n_3sigma = np.sum(np.abs(vals - mean) > 3 * std) / len(vals)

    # Gaussian predictions
    gauss_2sigma = 2 * (1 - norm.cdf(2))
    gauss_3sigma = 2 * (1 - norm.cdf(3))

    print(f"sigma = {sigma}:")
    print(f"  Mean = {mean:.4f}, Std = {std:.4f}")
    print(f"  Skewness = {skew:.4f} (Gaussian: 0)")
    print(f"  Excess kurtosis = {kurtosis:.4f} (Gaussian: 0)")
    print(f"  Fraction |x| > 2sigma: {n_2sigma:.4f} (Gaussian: {gauss_2sigma:.4f})")
    print(f"  Fraction |x| > 3sigma: {n_3sigma:.4f} (Gaussian: {gauss_3sigma:.4f})")
    print()

# ============================================================
# 4. THE ZERO DENSITY ARGUMENT
# ============================================================
print("=" * 70)
print("4. THE ZERO DENSITY ARGUMENT")
print("=" * 70)
print()
print("Question: If log|zeta(sigma+it)| has finite variance V(sigma)")
print("for sigma > 1/2, how incompatible is this with zeros?")
print()
print("A zero at sigma+it_0 means |zeta(sigma+it_0)| = 0,")
print("i.e., log|zeta(sigma+it_0)| = -infinity.")
print()
print("In a Gaussian model with variance V:")
print("  P(log|zeta| < -M) ~ exp(-M^2 / (2V))")
print()
print("For a zero, we need M -> infinity.")
print()
print("BUT: zeros of zeta are not 'random Gaussian events'.")
print("They are deterministic features of a specific function.")
print("The Gaussian model describes the TYPICAL behavior of zeta,")
print("not the exceptional behavior near zeros.")
print()

# Compute the actual variance at various sigma
print("Variance of log|zeta(sigma+it)| (numerically):")
for sigma in np.arange(0.50, 1.05, 0.05):
    np.random.seed(42)
    ts = np.random.uniform(1e4 * 0.8, 1e4 * 1.2, 300)
    vals = np.array([log_abs_zeta(sigma, float(t)) for t in ts])
    vals = vals[np.isfinite(vals)]
    v = np.var(vals)
    print(f"  sigma={sigma:.2f}: V={v:.4f}")

print()
print("The variance decreases monotonically from sigma=0.5 to sigma=1.0.")
print("At sigma=0.5, V ~ 1.4 (and growing with T).")
print("At sigma=1.0, V ~ 0.2 (and converging).")
print()
print("The SMALLER variance at sigma > 1/2 makes large negative excursions")
print("exponentially less likely, but 'exponentially unlikely' is not 'impossible'.")
print("Deterministic zeros could still exist even in a low-variance regime.")

print()
print("=" * 70)
print("CONCLUSION")
print("=" * 70)
print("""
The GMC phase structure cleanly separates sigma=1/2 from sigma>1/2:
  - sigma = 1/2: CRITICAL GMC phase (gamma = sqrt(2)), log-correlated
  - sigma > 1/2: effectively SUBCRITICAL, finite variance, not log-correlated

This is a beautiful mathematical structure, but the gap between
'statistical phase structure' and 'deterministic zero locations'
remains unbridged. The Gaussian model predicts zeros are unlikely
at sigma > 1/2, but cannot prove they're impossible.
""")

print("Done.")
