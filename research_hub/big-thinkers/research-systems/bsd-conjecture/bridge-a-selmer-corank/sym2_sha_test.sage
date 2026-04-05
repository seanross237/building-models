"""
Test: Does L(Sym^2 E, 1) encode Sha information?

The symmetric square L-function L(Sym^2 E, s) has:
  L(Sym^2 E, s) = prod_p (1 - alpha_p^2 p^{-s})^{-1} (1 - p^{-s})^{-1} (1 - beta_p^2 p^{-s})^{-1}

where alpha_p, beta_p are the roots of X^2 - a_p X + p.

By Rankin-Selberg: L(Sym^2 E, 1) ~ <f,f> * correction_factors

The BSD formula gives: L(E,1)/Omega = |Sha| * Tam / (Reg * Tors^2)

So the RATIO L(Sym^2 E, 1) / L(E,1)^2 eliminates some common factors
and might isolate Sha-related information.

We test this on rank-0 curves where L(E,1) != 0.
"""

import json
from collections import Counter

# Load the enriched data
with open("/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/approach-1-ml/data/bsd_invariants.json") as f:
    data = json.load(f)

# Focus on rank-0 curves
rank0 = [e for e in data if e['rank'] == 0]
print(f"Rank-0 curves: {len(rank0)}")

results = []
errors = 0

for entry in rank0:
    try:
        E = EllipticCurve(entry['ainvs'])

        # L(E,1)
        L_val = float(E.lseries().L1_vanishes() == False and E.lseries()(1) or 0)
        if L_val == 0:
            L_val = float(E.lseries()(1))

        # Real period
        omega = float(E.period_lattice().omega())

        # Sha from BSD
        sha = float(E.sha().an())

        # Compute sym2 partial sum: sum (a_p^2 - p) / p^s for s=2
        ap_dict = entry['a_p']
        conductor = entry['conductor']

        # Sym^2 partial L-value
        # L(Sym^2 E, s) Euler factor at p: (1 - alpha^2/p^s)(1 - 1/p^s)(1 - beta^2/p^s)
        # where alpha + beta = a_p, alpha*beta = p
        # alpha^2 + beta^2 = a_p^2 - 2p
        # So at s=1: factor = (1 - (a_p^2 - 2p)/p)(1 - 1/p)(1 - p/something)
        # Simpler: just compute the partial Euler product directly

        log_sym2 = 0.0
        sym2_sum = 0.0
        for p_str, a in ap_dict.items():
            p = int(p_str)
            a = int(a)
            if conductor % p == 0:
                continue

            # Sym^2 Euler factor at s=1:
            # (1 - alpha^2/p)(1 - 1/p)(1 - beta^2/p)
            # alpha^2 + beta^2 = a^2 - 2p, alpha^2 * beta^2 = p^2
            # Factor = (1 - (alpha^2+beta^2)/p + alpha^2*beta^2/p^2)(1 - 1/p)
            #        = (1 - (a^2-2p)/p + p^2/p^2)(1 - 1/p)
            #        = (1 - a^2/p + 2 + 1)(1 - 1/p)
            # Hmm, let me be more careful.

            # The local factor of L(Sym^2 E, s) at good p is:
            # 1 / ((1 - alpha^2 p^{-s})(1 - p^{-s})(1 - beta^2 p^{-s}))
            # At s=1:
            alpha_sq = (a**2 - 2*p)  # = alpha^2 + beta^2 (since alpha*beta=p => alpha^2 + beta^2 = a_p^2 - 2p)
            # Wait, alpha + beta = a_p, alpha*beta = p
            # alpha^2 = (a_p + sqrt(a_p^2 - 4p))/2)^2 -- not integer in general

            # Better approach: use the fact that
            # (1-alpha^2/p)(1-beta^2/p) = 1 - (alpha^2+beta^2)/p + (alpha*beta)^2/p^2
            #                            = 1 - (a_p^2 - 2p)/p + p^2/p^2
            #                            = 1 - a_p^2/p + 2 + 1
            #                            = 4 - a_p^2/p
            # That doesn't look right... let me redo:
            # = 1 - (a^2 - 2p)/p + p^2/p^2
            # = 1 - a^2/p + 2 + 1
            # That's wrong. Let me be very careful:
            # 1 - (alpha^2 + beta^2)/p + alpha^2 * beta^2 / p^2
            # = 1 - (a^2 - 2p)/p + p^2/p^2
            # = 1 - a^2/p + 2p/p + 1
            # = 1 - a^2/p + 2 + 1
            # = 4 - a^2/p
            # Hmm, for p=2, a=2: 4 - 4/2 = 2. For p=3, a=1: 4 - 1/3 = 11/3. Seems ok.

            sym2_factor_pair = float(4 - a**2/p)  # (1 - alpha^2/p)(1 - beta^2/p)
            mid_factor = float(1 - 1.0/p)

            full_factor = sym2_factor_pair * mid_factor
            if full_factor > 0:
                log_sym2 += log(1.0 / full_factor)

            sym2_sum += float(a**2 - p) / float(p**2)

        # Also compute L(E,1) from the data
        # Actually just use the BSD formula values
        bsd_rhs = float(entry['real_period'] * entry['regulator'] * entry['tamagawa_product'] / entry['torsion_order']**2)
        # L(E,1) / Omega should equal |Sha| * Tam / (Reg * Tors^2) ... wait
        # BSD: L(E,1) = |Sha| * Omega * Reg * Tam / Tors^2
        # So L(E,1)/Omega = |Sha| * Reg * Tam / Tors^2

        results.append({
            'label': entry['label'],
            'conductor': entry['conductor'],
            'sha': round(sha),
            'torsion_order': entry['torsion_order'],
            'log_sym2': round(float(log_sym2), 6),
            'sym2_sum': round(float(sym2_sum), 6),
            'omega': round(float(omega), 6),
            'L_val': round(float(E.lseries()(1)), 8) if True else 0,
            'bsd_rhs': round(float(bsd_rhs), 6),
        })

    except Exception as e:
        errors += 1
        if errors <= 3:
            print(f"Error on {entry['label']}: {e}")

print(f"Computed {len(results)} curves, {errors} errors")

# Compare Sha=1 vs Sha=4 curves
sha1 = [r for r in results if r['sha'] == 1]
sha4 = [r for r in results if r['sha'] == 4]
print(f"\nSha=1: n={len(sha1)}")
print(f"Sha=4: n={len(sha4)}")

if sha4:
    print(f"\nlog_sym2: Sha=1: {sum(r['log_sym2'] for r in sha1)/len(sha1):.4f}, Sha=4: {sum(r['log_sym2'] for r in sha4)/len(sha4):.4f}")
    print(f"sym2_sum: Sha=1: {sum(r['sym2_sum'] for r in sha1)/len(sha1):.4f}, Sha=4: {sum(r['sym2_sum'] for r in sha4)/len(sha4):.4f}")
    print(f"omega:    Sha=1: {sum(r['omega'] for r in sha1)/len(sha1):.4f}, Sha=4: {sum(r['omega'] for r in sha4)/len(sha4):.4f}")
    print(f"L_val:    Sha=1: {sum(r['L_val'] for r in sha1)/len(sha1):.6f}, Sha=4: {sum(r['L_val'] for r in sha4)/len(sha4):.6f}")

# Check if L(Sym^2 E, 1) / omega^2 correlates with Sha
print("\n\nlog_sym2 / omega^2 by Sha:")
for sha_val in [1, 4]:
    subset = [r for r in results if r['sha'] == sha_val]
    if subset:
        ratio = [r['log_sym2'] / max(r['omega']**2, 1e-10) for r in subset]
        print(f"  Sha={sha_val} (n={len(subset)}): mean ratio={sum(ratio)/len(ratio):.4f}")

# L(E,1) / omega should = |Sha| * correction
print("\nL(E,1)/omega by Sha:")
for sha_val in [1, 4]:
    subset = [r for r in results if r['sha'] == sha_val]
    if subset:
        ratio = [r['L_val'] / max(r['omega'], 1e-10) for r in subset]
        print(f"  Sha={sha_val} (n={len(subset)}): mean={sum(ratio)/len(ratio):.6f}")

# Key test: can log_sym2 predict sha BEYOND what omega alone predicts?
# Since omega varies enormously, let's look at the RESIDUAL
print("\n\nCorrelation analysis:")
import math
sha_vals = [r['sha'] for r in results]
log_sha = [math.log(r['sha']) if r['sha'] > 0 else 0 for r in results]
sym2_vals = [r['log_sym2'] for r in results]
omega_vals = [r['omega'] for r in results]
cond_vals = [r['conductor'] for r in results]

# Spearman correlations
from itertools import combinations
pairs = [('log_sym2', sym2_vals), ('omega', omega_vals), ('conductor', cond_vals)]
for name, vals in pairs:
    # Compute rank correlation
    n = len(vals)
    # Sort by vals and by sha_vals
    rank_v = [0]*n
    rank_s = [0]*n
    sorted_v = sorted(range(n), key=lambda i: vals[i])
    sorted_s = sorted(range(n), key=lambda i: sha_vals[i])
    for i, idx in enumerate(sorted_v):
        rank_v[idx] = i
    for i, idx in enumerate(sorted_s):
        rank_s[idx] = i
    rho = 1 - 6*sum((rank_v[i] - rank_s[i])**2 for i in range(n)) / (n*(n**2-1))
    print(f"  Spearman({name}, sha): rho={rho:+.4f}")
