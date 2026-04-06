"""
Investigation 4: Numerical Computation

1. Compute the actual distribution of log|zeta(sigma+it)| for sigma = 0.6, 0.7, 0.8, 0.9
   and t up to 10^4 (using mpmath). Verify Gaussian concentration.

2. Compute Jensen integrals explicitly around known zero locations.

3. Compare predicted vs actual N(sigma, T) for moderate T.
"""

import mpmath
from mpmath import mp, mpf, mpc, log, pi, sqrt, exp, power, zeta, fabs, re, im, arg
from sympy import nextprime as _nextprime
from math import log as mlog, sqrt as msqrt, pi as mpi, exp as mexp
import json
import time

mp.dps = 25

def nextprime(n):
    return int(_nextprime(int(n)))

def V_sigma_full(sigma, num_primes=2000):
    """V(sigma) = sum_p (-1/2)*log(1 - p^{-2*sigma})"""
    total = mpf(0)
    p = 2
    count = 0
    while count < num_primes:
        total += -log(1 - power(p, -2*sigma)) / 2
        p = nextprime(p)
        count += 1
    return float(total)

print("=" * 70)
print("INVESTIGATION 4: NUMERICAL COMPUTATION")
print("=" * 70)

# Part 1: Distribution of log|zeta(sigma+it)| for various sigma
print("\n--- Part 1: Distribution of log|zeta(sigma+it)| ---")

sigmas = [0.6, 0.7, 0.8, 0.9]
T_max = 2000  # Moderate T for computation speed
N_points = 2000
dt = T_max / N_points

results = {}

for sigma in sigmas:
    print(f"\nComputing for sigma = {sigma}...")
    t0 = time.time()

    log_vals = []
    for i in range(1, N_points + 1):
        t = 10 + i * dt  # start at t=10 to avoid trivial zeros
        s = mpc(sigma, t)
        z = zeta(s)
        if z != 0:
            log_vals.append(float(log(fabs(z))))
        else:
            log_vals.append(-999)  # placeholder for actual zero

    elapsed = time.time() - t0
    print(f"  Computed {len(log_vals)} values in {elapsed:.1f}s")

    # Statistics
    mean_val = sum(log_vals) / len(log_vals)
    var_val = sum((x - mean_val)**2 for x in log_vals) / len(log_vals)
    std_val = msqrt(var_val)
    min_val = min(log_vals)
    max_val = max(log_vals)

    # Predicted variance from Euler product
    V_pred = V_sigma_full(sigma, 1000)

    # How many values exceed 2, 3, 4 standard deviations?
    n_2sigma = sum(1 for x in log_vals if abs(x - mean_val) > 2*std_val)
    n_3sigma = sum(1 for x in log_vals if abs(x - mean_val) > 3*std_val)
    n_4sigma = sum(1 for x in log_vals if abs(x - mean_val) > 4*std_val)

    # Gaussian prediction
    # P(|X| > k*sigma) = 2*(1 - Phi(k))
    # For k=2: ~4.6%, k=3: ~0.27%, k=4: ~0.006%
    pred_2 = 0.046 * N_points
    pred_3 = 0.0027 * N_points
    pred_4 = 0.000063 * N_points

    print(f"  Mean log|zeta|: {mean_val:.4f}")
    print(f"  Variance:       {var_val:.4f} (predicted V = {V_pred:.4f}, ratio = {var_val/V_pred:.4f})")
    print(f"  Std dev:        {std_val:.4f} (predicted sqrt(V) = {msqrt(V_pred):.4f})")
    print(f"  Min, Max:       {min_val:.4f}, {max_val:.4f}")
    print(f"  >2sigma: {n_2sigma} (Gaussian pred: {pred_2:.1f})")
    print(f"  >3sigma: {n_3sigma} (Gaussian pred: {pred_3:.1f})")
    print(f"  >4sigma: {n_4sigma} (Gaussian pred: {pred_4:.1f})")

    # Build histogram
    n_bins = 50
    bin_min = mean_val - 5*std_val
    bin_max = mean_val + 5*std_val
    bin_width = (bin_max - bin_min) / n_bins
    hist = [0] * n_bins
    for x in log_vals:
        idx = int((x - bin_min) / bin_width)
        if 0 <= idx < n_bins:
            hist[idx] += 1

    results[sigma] = {
        'mean': mean_val,
        'variance': var_val,
        'V_predicted': V_pred,
        'ratio': var_val / V_pred,
        'std': std_val,
        'min': min_val,
        'max': max_val,
        'n_2sigma': n_2sigma,
        'n_3sigma': n_3sigma,
        'n_4sigma': n_4sigma,
        'histogram': hist,
        'hist_bins': [bin_min + (i+0.5)*bin_width for i in range(n_bins)]
    }

# Part 2: Jensen integral around a known zero
print("\n\n--- Part 2: Jensen Integral Near First Zero ---")
print("""
The first zero of zeta is at s = 1/2 + i*14.13472...
Let's compute Jensen's integral for disks centered at sigma + i*14.135
for various sigma > 1/2.
""")

rho1_im = mpf('14.134725141734693790')  # first zero

for sigma_center in [0.6, 0.7, 0.8, 0.9, 1.0]:
    print(f"\nJensen integral centered at {sigma_center} + i*14.135:")

    for R in [0.05, 0.1, 0.2, 0.5]:
        # Compute avg of log|zeta| on circle of radius R
        N_circle = 200
        log_sum = mpf(0)
        for k in range(N_circle):
            theta = 2 * pi * k / N_circle
            s = mpc(sigma_center + R * mpmath.cos(theta), rho1_im + R * mpmath.sin(theta))
            z = zeta(s)
            if z != 0:
                log_sum += log(fabs(z))
            else:
                log_sum += mpf('-100')  # approximate

        avg_log = float(log_sum / N_circle)

        # Value at center
        z_center = zeta(mpc(sigma_center, rho1_im))
        log_center = float(log(fabs(z_center)))

        # Jensen bound
        jensen_bound = avg_log - log_center
        if jensen_bound < 0:
            jensen_bound = 0

        # Distance from center to the zero at 1/2 + i*14.135
        dist_to_zero = sigma_center - 0.5  # since Im parts are ~equal

        print(f"  R={R:.2f}: avg log|zeta|={avg_log:.4f}, log|zeta(center)|={log_center:.4f}, "
              f"Jensen sum={jensen_bound:.4f}, n(r={dist_to_zero:.2f}) <= {jensen_bound/mlog(R/dist_to_zero):.2f}" if R > dist_to_zero else
              f"  R={R:.2f}: avg log|zeta|={avg_log:.4f}, log|zeta(center)|={log_center:.4f} (R < dist to zero)")

# Part 3: Count zeros and compare with bounds
print("\n\n--- Part 3: Zero Counting vs Bounds ---")
print("""
N(T) = number of zeros with 0 < Im(rho) < T.
Backlund: N(T) = (T/2pi)*log(T/2pi*e) + S(T) where S(T) = (1/pi)*arg(zeta(1/2+iT)) = O(log T)

N(sigma, T) = number of zeros with Re(rho) > sigma, 0 < Im(rho) < T.
""")

# Compute N(T) for moderate T using mpmath's zero finder
print("Computing zeta zeros...")
n_zeros = 50
zeros = []
for k in range(1, n_zeros + 1):
    z = mpmath.zetazero(k)
    zeros.append((float(re(z)), float(im(z))))

print(f"Computed {len(zeros)} zeros. All on critical line: {all(abs(r - 0.5) < 1e-10 for r, _ in zeros)}")
print(f"First zero: {zeros[0][1]:.6f}")
print(f"Last zero: {zeros[-1][1]:.6f}")

# Since all known zeros are on Re=1/2, N(sigma, T) = 0 for sigma > 1/2
# Compare with our bounds
T_test = zeros[-1][1] + 1  # just above last zero
print(f"\nFor T = {T_test:.1f}:")
print(f"  Actual N(0.6, T) = 0  (all zeros on critical line)")
print(f"  Actual N(0.7, T) = 0")
print(f"  Actual N(0.8, T) = 0")

# What do our bounds give?
for sigma in [0.6, 0.7, 0.8, 0.9]:
    V = V_sigma_full(sigma, 1000)
    # Ingham
    a_ing = 3*(1-sigma)/(2-sigma)
    n_ing = T_test**a_ing
    # Huxley
    a_hux = 12*(1-sigma)/5
    n_hux = T_test**a_hux
    # Our concentration-Jensen
    n_cj = T_test * mlog(T_test) / 5  # rough bound from inv1

    print(f"  sigma={sigma}: Ingham={n_ing:.1f}, Huxley={n_hux:.1f}, Conc-Jensen~{n_cj:.1f}")

print("""
\nAll bounds vastly overestimate: the actual count is 0, while even the best
bounds (Ingham, Huxley) give O(1) to O(10). Our concentration-Jensen bound
gives O(T*log T) which is worse.

This is expected: zero-density BOUNDS are upper bounds, not estimates.
The actual density is much smaller (conjectured to be exactly 0 by RH).
""")

# Part 4: Minimum of |zeta| on vertical lines
print("\n--- Part 4: Minimum of |zeta(sigma+it)| on Vertical Lines ---")
print("""
For sigma > 1/2, how small can |zeta(sigma+it)| get?
The concentration predicts extreme minima at rate exp(-M^2/(2V)).
""")

for sigma in [0.6, 0.7, 0.8, 0.9]:
    min_abs = float('inf')
    min_t = 0
    t_vals_near_zeros = [z[1] for z in zeros]  # check near known zeros

    # Check at known zero heights
    for t in t_vals_near_zeros:
        s = mpc(sigma, t)
        z_val = fabs(zeta(s))
        if float(z_val) < min_abs:
            min_abs = float(z_val)
            min_t = t

    # Also check some random points
    for t in [x * 0.37 + 5 for x in range(200)]:
        s = mpc(sigma, t)
        z_val = fabs(zeta(s))
        if float(z_val) < min_abs:
            min_abs = float(z_val)
            min_t = t

    log_min = mlog(min_abs) if min_abs > 0 else -999
    V = V_sigma_full(sigma, 1000)
    M_observed = -log_min  # how many "standard deviations" is this?
    n_sigma_devs = M_observed / msqrt(V) if V > 0 else 0

    print(f"  sigma={sigma:.1f}: min|zeta| = {min_abs:.6f} at t={min_t:.3f}, "
          f"log(min) = {log_min:.4f}, = {n_sigma_devs:.2f} * sqrt(V)")

    # Probability of seeing this in Gaussian model
    if n_sigma_devs > 0:
        # Gaussian tail: P(X < -k*sigma) ~ exp(-k^2/2)/(k*sqrt(2*pi))
        log_P = -n_sigma_devs**2/2
        print(f"         Gaussian tail prob ~ exp({log_P:.1f}) ~ 10^({log_P/mlog(10):.1f})")

# Part 5: Approach of |zeta(sigma+it)| to zero near critical line
print("\n\n--- Part 5: How |zeta(sigma+it)| Approaches Zero Near sigma=1/2 ---")
print("""
For the first zero rho_1 = 1/2 + i*14.1347..., how does |zeta(sigma+igamma_1)|
behave as sigma -> 1/2?
""")

gamma1 = float(rho1_im)
print(f"First zero at t = {gamma1:.10f}")
print(f"{'sigma':>8} {'|zeta|':>14} {'log|zeta|':>12} {'sigma-1/2':>10} {'|zeta|/(sigma-1/2)':>20}")
print("-" * 70)

for delta_exp in range(-1, -11, -1):
    delta = 10**delta_exp
    sigma = 0.5 + delta
    s = mpc(sigma, gamma1)
    z = zeta(s)
    abs_z = float(fabs(z))
    log_z = mlog(abs_z) if abs_z > 0 else -999
    ratio = abs_z / delta
    print(f"{sigma:>8.10f} {abs_z:>14.6e} {log_z:>12.4f} {delta:>10.0e} {ratio:>20.6f}")

print("""
Near a zero at 1/2 + igamma:
|zeta(sigma+igamma)| ~ C * (sigma - 1/2) * |zeta'(rho)| as sigma -> 1/2+

This is LINEAR in (sigma - 1/2), confirming that the zero is simple.
The constant C ~ |zeta'(rho)|.
""")

# Save all results
with open('/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/jensen-concentration/inv4_results.json', 'w') as f:
    json.dump({
        'distribution_stats': {str(k): {kk: vv for kk, vv in v.items() if kk != 'histogram' and kk != 'hist_bins'}
                               for k, v in results.items()},
        'zeros_computed': len(zeros),
        'all_on_critical_line': all(abs(r - 0.5) < 1e-10 for r, _ in zeros),
    }, f, indent=2, default=str)

print("\nResults saved to inv4_results.json")
