#!/usr/bin/env python3
"""
Refined correlation analysis focused on demonstrating the key structural
differences between sigma=0.5 and sigma>0.5.

Key improvements:
1. More samples for better statistics
2. Focus on the ratio Cov(tau)/Var to get normalized correlation
3. Theoretical comparison using the known Dirichlet series formula
4. Analysis of how quickly correlations decay (characteristic length scale)

The theoretical 2-point function:
  For sigma > 1/2, by the Euler product:
    E[log|zeta(sigma+it1)| * log|zeta(sigma+it2)|] involves
    sum_p (log p)^2 / (p^{2*sigma} - 1) * cos((t1-t2)*log(p)) / ...

  At sigma = 1/2, this series DIVERGES (the sum over primes doesn't converge),
  giving rise to the log-correlated structure.
"""

import numpy as np
from mpmath import mp, zeta, log, fabs
import time

mp.dps = 20


def log_abs_zeta(sigma, t):
    s = mp.mpc(sigma, t)
    z = zeta(s)
    if z == 0:
        return float('-inf')
    return float(log(fabs(z)))


def compute_normalized_correlation(sigma, base_t, base_vals, tau):
    """Compute normalized correlation rho(tau) = Cov(f(t), f(t+tau)) / Var(f)."""
    shifted_vals = np.array([log_abs_zeta(sigma, float(t + tau)) for t in base_t])

    mask = np.isfinite(base_vals) & np.isfinite(shifted_vals)
    b = base_vals[mask]
    s = shifted_vals[mask]

    if len(b) < 20:
        return np.nan, np.nan

    cov = np.mean(b * s) - np.mean(b) * np.mean(s)
    var_b = np.var(b)
    var_s = np.var(s)

    if var_b <= 0 or var_s <= 0:
        return np.nan, np.nan

    rho = cov / np.sqrt(var_b * var_s)
    return cov, rho


# ============================================================
# Compute base values with more samples
# ============================================================
print("=" * 70)
print("REFINED CORRELATION ANALYSIS")
print("=" * 70)

T_center = 5e3
n_samples = 300
np.random.seed(777)
base_t = np.random.uniform(T_center * 0.8, T_center * 1.2, n_samples)

tau_values = [0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]

for sigma in [0.5, 0.6, 0.75, 1.0]:
    print(f"\n{'='*50}")
    print(f"SIGMA = {sigma}")
    print(f"{'='*50}")

    start = time.time()
    base_vals = np.array([log_abs_zeta(sigma, float(t)) for t in base_t])
    base_vals_clean = base_vals[np.isfinite(base_vals)]
    base_var = np.var(base_vals_clean)
    base_mean = np.mean(base_vals_clean)
    elapsed = time.time() - start
    print(f"Base values computed in {elapsed:.1f}s")
    print(f"  Mean = {base_mean:.4f}, Var = {base_var:.4f}")

    covs = []
    rhos = []
    for tau in tau_values:
        cov, rho = compute_normalized_correlation(sigma, base_t, base_vals, tau)
        covs.append(cov)
        rhos.append(rho)
        print(f"  tau={tau:8.4f}: cov={cov:+.6f}, rho={rho:+.4f}")

    covs = np.array(covs)
    rhos = np.array(rhos)
    log_tau = np.log(np.array(tau_values))

    # Fit covariance to log model: C = a - b*log(tau)
    valid = np.isfinite(covs)
    if np.sum(valid) >= 3:
        A = np.vstack([np.ones_like(log_tau[valid]), log_tau[valid]]).T
        coeffs = np.linalg.lstsq(A, covs[valid], rcond=None)[0]
        a_fit, b_fit = coeffs
        resids = covs[valid] - (a_fit + b_fit * log_tau[valid])
        R2 = 1 - np.var(resids) / np.var(covs[valid])
        print(f"\n  Log-linear fit: C(tau) = {a_fit:.4f} + ({b_fit:.4f})*log(tau)")
        print(f"  Slope = {b_fit:.4f} (log-correlated: -0.5)")
        print(f"  R^2 = {R2:.4f}")

    # Fit to exponential decay: rho = exp(-tau / L) for comparison
    valid_pos = valid & (np.array(rhos) > 0.01)
    if np.sum(valid_pos) >= 3:
        log_rho = np.log(np.array(rhos)[valid_pos])
        tau_arr = np.array(tau_values)[valid_pos]
        A2 = np.vstack([np.ones_like(tau_arr), tau_arr]).T
        coeffs2 = np.linalg.lstsq(A2, log_rho, rcond=None)[0]
        L_char = -1.0 / coeffs2[1] if coeffs2[1] < 0 else float('inf')
        print(f"  Exponential decorrelation length: L = {L_char:.4f}")

# ============================================================
# Theoretical prime sum analysis
# ============================================================
print("\n" + "=" * 70)
print("THEORETICAL PRIME SUM ANALYSIS")
print("At sigma>1/2, the 2-point function involves:")
print("  sum_p log(p)^2 / p^(2*sigma) * p^(-|tau|*log(p)) ...")
print("This sum CONVERGES for sigma>1/2 and DIVERGES at sigma=1/2.")
print("=" * 70)

from sympy import primerange

primes = list(primerange(2, 1000))

for sigma in [0.5, 0.6, 0.75, 1.0]:
    # Partial sum of (log p)^2 / p^{2*sigma}
    partial_sums = []
    running = 0.0
    for p in primes:
        running += np.log(p)**2 / p**(2*sigma)
        partial_sums.append(running)

    n_primes_10 = min(10, len(primes))
    n_primes_50 = min(50, len(primes))
    n_primes_all = len(primes)

    print(f"\nsigma={sigma}:")
    print(f"  sum_{{p<=29}}  (log p)^2 / p^{{2*{sigma}}} = {partial_sums[n_primes_10-1]:.4f}")
    print(f"  sum_{{p<=229}} (log p)^2 / p^{{2*{sigma}}} = {partial_sums[n_primes_50-1]:.4f}")
    print(f"  sum_{{p<1000}} (log p)^2 / p^{{2*{sigma}}} = {partial_sums[-1]:.4f}")

    if sigma == 0.5:
        # At sigma=1/2: sum (log p)^2 / p ~ integral (log x) / x ~ (1/2)(log N)^2
        # This diverges as log(N)^2
        N = primes[-1]
        theory = 0.5 * np.log(N)**2
        print(f"  Divergence check: (1/2)(log {N})^2 = {theory:.4f}")
        print(f"  --> SUM DIVERGES (log-correlated)")
    else:
        # At sigma>1/2: converges
        # Rough bound: sum ~ integral (log x)^2 / x^{2*sigma} dx
        # which converges for sigma > 1/2
        print(f"  --> Sum appears to {'CONVERGE' if partial_sums[-1] < 20 else 'grow slowly'}")

print("\nDone.")
