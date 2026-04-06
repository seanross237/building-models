#!/usr/bin/env python3
"""
Comprehensive correlation analysis of log|zeta(sigma+it)|.

Computes:
1. Variance scaling with T at sigma=0.5, 0.75, 1.0
2. Two-point correlation function at sigma=0.5, 0.6, 0.75, 1.0
3. Log-linearity test (slope of C vs log tau)
4. Prime sum divergence analysis

This is the main numerical script for the GMC-repulsion experiment.
"""

import numpy as np
from mpmath import mp, zeta, log, fabs
from sympy import primerange
import time

mp.dps = 20


def log_abs_zeta(sigma, t):
    """Compute log|zeta(sigma + i*t)| using mpmath."""
    s = mp.mpc(sigma, t)
    z = zeta(s)
    if z == 0:
        return float('-inf')
    return float(log(fabs(z)))


def batch_eval(sigma, t_array):
    """Evaluate log|zeta| for array of t values."""
    return np.array([log_abs_zeta(sigma, float(t)) for t in t_array])


# ============================================================
# PART 1: VARIANCE SCALING
# ============================================================
print("=" * 70)
print("PART 1: VARIANCE SCALING WITH HEIGHT T")
print("Selberg CLT: Var(log|zeta(1/2+it)|) ~ (1/2)*log(log(T))")
print("=" * 70)

T_centers = [1e3, 5e3, 1e4, 5e4]
n_var = 200

for sigma in [0.5, 0.75, 1.0]:
    print(f"\nsigma = {sigma}:")
    for Tc in T_centers:
        np.random.seed(42)
        ts = np.random.uniform(Tc * 0.9, Tc * 1.1, n_var)
        vals = batch_eval(sigma, ts)
        vals = vals[np.isfinite(vals)]
        v = np.var(vals)
        selberg = 0.5 * np.log(np.log(Tc))
        print(f"  T~{Tc:.0e}: Var={v:.4f}, (1/2)loglogT={selberg:.4f}, "
              f"ratio={v/selberg:.3f}")

# ============================================================
# PART 2: TWO-POINT CORRELATION
# ============================================================
print("\n" + "=" * 70)
print("PART 2: TWO-POINT CORRELATION C(sigma; tau)")
print("=" * 70)

T_center = 5e3
n_corr = 300
np.random.seed(777)
base_t = np.random.uniform(T_center * 0.8, T_center * 1.2, n_corr)

tau_values = [0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]

for sigma in [0.5, 0.6, 0.75, 1.0]:
    print(f"\nsigma = {sigma}:")
    base_vals = batch_eval(sigma, base_t)
    base_var = np.var(base_vals[np.isfinite(base_vals)])
    print(f"  Var = {base_var:.4f}")

    covs = []
    for tau in tau_values:
        shifted_vals = batch_eval(sigma, base_t + tau)
        mask = np.isfinite(base_vals) & np.isfinite(shifted_vals)
        b, s = base_vals[mask], shifted_vals[mask]
        cov = np.mean(b * s) - np.mean(b) * np.mean(s)
        rho = cov / np.sqrt(np.var(b) * np.var(s)) if np.var(b) > 0 and np.var(s) > 0 else 0
        covs.append(cov)
        print(f"  tau={tau:8.4f}: cov={cov:+.6f}, rho={rho:+.4f}")

    # Fit C = a + b*log(tau)
    log_tau = np.log(np.array(tau_values))
    covs = np.array(covs)
    valid = np.isfinite(covs)
    A = np.vstack([np.ones_like(log_tau[valid]), log_tau[valid]]).T
    coeffs = np.linalg.lstsq(A, covs[valid], rcond=None)[0]
    a, b = coeffs
    resids = covs[valid] - (a + b * log_tau[valid])
    R2 = 1 - np.var(resids) / np.var(covs[valid])
    print(f"  Fit: C = {a:.4f} + ({b:.4f})*log(tau), R^2={R2:.4f}")
    print(f"  Slope = {b:.4f} (log-correlated: -0.500)")

# ============================================================
# PART 3: PRIME SUM DIVERGENCE
# ============================================================
print("\n" + "=" * 70)
print("PART 3: PRIME SUM DIVERGENCE")
print("S(sigma) = sum_p (log p)^2 / p^{2*sigma}")
print("Diverges at sigma=1/2, converges for sigma>1/2")
print("=" * 70)

primes = list(primerange(2, 10000))

for sigma in [0.5, 0.6, 0.75, 1.0]:
    running = 0.0
    for p in primes:
        running += np.log(p)**2 / p**(2*sigma)
    print(f"  sigma={sigma}: S(primes < 10000) = {running:.4f}", end="")
    if sigma == 0.5:
        theory = 0.5 * np.log(primes[-1])**2
        print(f"  [(1/2)(log N)^2 = {theory:.4f}, DIVERGES]")
    else:
        print(f"  [CONVERGES]")

print("\nDone.")
