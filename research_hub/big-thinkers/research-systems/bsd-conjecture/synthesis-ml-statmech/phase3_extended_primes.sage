#!/usr/bin/env sage
"""
Compute a_p for extended primes (up to p=997) for a subset of curves.
This lets us test whether beta_p ~ 1/p - 1/(3p^2) continues to hold.
"""

from sage.all import *
import json
import math
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Use 50 rank-1 curves with known labels
rank1_labels = [
    '37a1', '43a1', '53a1', '57a1', '58a1', '61a1', '65a1', '67a1', '73a1', '77a1',
    '79a1', '82a1', '83a1', '88a1', '89a1', '91a1', '92a1', '99a1', '101a1', '102a1',
    '106a1', '109a1', '110a1', '113a1', '115a1', '116a1', '118a1', '121a1', '123a1', '124a1',
    '127a1', '129a1', '131a1', '133a1', '134a1', '137a1', '139a1', '141a1', '142a1', '143a1',
    '145a1', '147a1', '148a1', '149a1', '150a1', '151a1', '152a1', '153a1', '155a1', '157a1',
]

# Extended primes
primes_ext = list(prime_range(2, 998))
print(f"Computing a_p for {len(primes_ext)} primes, up to p={primes_ext[-1]}")

# Compute BSD RHS and a_p for each curve
data = []
for label in rank1_labels:
    try:
        E = EllipticCurve(label)
        N = int(E.conductor())
        r = int(E.rank())
        if r != 1:
            continue

        omega = float(E.real_components() * abs(E.period_lattice().basis()[0].real()))
        reg = float(E.regulator())
        tam = int(E.tamagawa_product())
        tors = int(E.torsion_order())

        bsd_rhs = omega * reg * tam / tors**2
        if bsd_rhs <= 0:
            continue

        a_p = {}
        for p in primes_ext:
            a_p[int(p)] = int(E.ap(p))

        data.append({
            'label': label,
            'N': N,
            'rank': r,
            'bsd_rhs': bsd_rhs,
            'log_bsd_resid': math.log(bsd_rhs) - 0.5 * math.log(N),
            'a_p': a_p,
        })
        print(f"  {label}: N={N}, BSD_RHS={bsd_rhs:.6f}")

    except Exception as e:
        print(f"  {label}: Error - {e}")

print(f"\n{len(data)} rank-1 curves computed")

# Now compute beta_p for ALL primes
print(f"\nComputing regression coefficients beta_p for each prime:")
print(f"{'p':>5s}  {'beta_BSD':>12s}  {'1/p':>10s}  {'1/p-1/(3p^2)':>14s}  {'beta_Euler':>12s}")

n = len(data)
y = [d['log_bsd_resid'] for d in data]
mean_y = sum(y) / n

results = []
for p in primes_ext:
    # Get a_p values
    ap_vals = [d['a_p'][p] for d in data]

    # Check if this prime is bad for any curve (skip if so for > 50% of curves)
    good_count = sum(1 for d in data if d['N'] % p != 0)
    if good_count < n * 0.5:
        continue

    mean_ap = sum(ap_vals) / n
    var_ap = sum((v - mean_ap)**2 for v in ap_vals) / n
    if var_ap < 1e-10:
        continue

    # Regression of log(BSD_RHS/sqrt(N)) on a_p
    cov = sum((y[i] - mean_y) * (ap_vals[i] - mean_ap) for i in range(n)) / n
    beta_bsd = cov / var_ap

    # Regression of log(Euler factor) on a_p
    euler_vals = []
    ap_good = []
    for d in data:
        N_d = d['N']
        ap = d['a_p'][p]
        is_bad = (N_d % p == 0)
        if is_bad:
            denom = 1 - float(ap)/p
        else:
            denom = 1 - float(ap)/p + 1.0/p
        if abs(denom) > 1e-50:
            euler_vals.append(-math.log(abs(denom)))
            ap_good.append(float(ap))

    if len(ap_good) > 5:
        mean_ap_g = sum(ap_good) / len(ap_good)
        mean_euler = sum(euler_vals) / len(euler_vals)
        var_ap_g = sum((v-mean_ap_g)**2 for v in ap_good) / len(ap_good)
        cov_euler = sum((ap_good[i]-mean_ap_g)*(euler_vals[i]-mean_euler) for i in range(len(ap_good))) / len(ap_good)
        beta_euler = cov_euler / var_ap_g if var_ap_g > 0 else 0
    else:
        beta_euler = 0

    theory = 1.0/p - 1.0/(3*p**2)

    results.append({
        'p': int(p),
        'beta_bsd': float(beta_bsd),
        'beta_euler': float(beta_euler),
        'theory': float(theory),
        'one_over_p': 1.0/p,
    })

    if p <= 97 or p in [101, 127, 197, 293, 401, 503, 599, 701, 809, 907, 997]:
        print(f"{p:>5d}  {beta_bsd:>12.8f}  {1.0/p:>10.8f}  {theory:>14.8f}  {beta_euler:>12.8f}")

# Save
with open(os.path.join(OUTPUT_DIR, 'extended_prime_results.json'), 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nSaved {len(results)} results")

# Summary: fit power law to |beta_bsd| for p > 97
print("\nPower law fit for |delta_p| = |beta_bsd - 1/p| at p > 97:")
import math
large_p = [r for r in results if r['p'] > 97 and abs(r['beta_bsd']) > 1e-12]
if len(large_p) > 10:
    log_p = [math.log(r['p']) for r in large_p]
    log_delta = [math.log(abs(r['beta_bsd'] - 1.0/r['p'])) for r in large_p if abs(r['beta_bsd'] - 1.0/r['p']) > 1e-15]

    # Linear regression in log space
    if len(log_delta) > 5:
        n_fit = min(len(log_p), len(log_delta))
        log_p = log_p[:n_fit]
        log_delta = log_delta[:n_fit]
        mean_lp = sum(log_p) / n_fit
        mean_ld = sum(log_delta) / n_fit
        sxx = sum((lp - mean_lp)**2 for lp in log_p)
        sxy = sum((log_p[i] - mean_lp)*(log_delta[i] - mean_ld) for i in range(n_fit))
        if sxx > 0:
            slope = sxy / sxx
            intercept = mean_ld - slope * mean_lp
            print(f"  |delta_p| ~ {math.exp(intercept):.4f} * p^{slope:.4f}")
            # R^2
            ss_res = sum((log_delta[i] - (slope*log_p[i]+intercept))**2 for i in range(n_fit))
            ss_tot = sum((log_delta[i] - mean_ld)**2 for i in range(n_fit))
            r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0
            print(f"  R^2 = {r2:.4f}")

# Also test: beta_euler vs theory for p > 97
print("\nEuler coefficient test for p > 97:")
large_euler = [r for r in results if r['p'] > 97 and r['beta_euler'] != 0]
if large_euler:
    ratios = [r['beta_euler'] / r['theory'] for r in large_euler if r['theory'] != 0]
    print(f"  Mean ratio beta_euler / (1/p - 1/(3p^2)): {sum(ratios)/len(ratios):.6f}")
    print(f"  Std: {(sum((r - sum(ratios)/len(ratios))**2 for r in ratios)/len(ratios))**0.5:.6f}")
    print(f"  n = {len(ratios)}")
