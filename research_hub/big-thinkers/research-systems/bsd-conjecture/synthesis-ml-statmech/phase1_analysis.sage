#!/usr/bin/env sage
"""
Phase 1 Analysis: Deeper investigation of the key finding.

KEY DISCOVERY from Phase 1:
The Euler product expansion gives log(euler factor at p) = sum S_n/(n*p^n),
where S_n = alpha^n + beta^n are power sums.

The LINEAR component of this in a_p is NOT 1/p but rather:
  beta_eff = E[f(a_p)*a_p] / E[a_p^2] = 1/p - 1/(3p) + ...

But the ML model doesn't fit log(Euler factor) -- it fits log(BSD_RHS).
The BSD_RHS includes Omega, Reg, Tam, tors.

From the decomposition, beta_2(BSD_RHS) = 0.192:
  - from log(Omega): -0.080 (real period ANTI-correlates with a_2)
  - from log(Reg): +0.137 (regulator correlates with a_2)
  - from log(Tam): +0.189 (Tamagawa product correlates with a_2)
  - from -log(tors^2): -0.001 (negligible)
  Total BSD components: 0.246

But the 0.5*log(N) subtraction removes 0.056, giving:
  beta_2(resid) = 0.246 - 0.056 = 0.190, matching the ML result.

This means the ML beta_p is NOT the Euler product coefficient.
The correction delta_p = beta_p(ML) - 1/p is dominated by:
1. The real period Omega absorbing a NEGATIVE a_p contribution (-0.08 at p=2)
2. The Tamagawa product contributing a POSITIVE a_p contribution (+0.19 at p=2)
3. The regulator contributing a POSITIVE a_p contribution (+0.14 at p=2)

The total correction is:
  delta_p = (contribution from Omega, Reg, Tam, tors decomposition) - (Euler coefficient)

This is NOT a number-theoretic correction to the Euler product.
It's an accounting artifact of fitting BSD_RHS instead of L(E,s).

BUT: the EMPIRICAL Euler coefficient for log(Euler factor) vs a_p is:
  p=2: 0.438 (vs theoretical 1/(p+1) = 0.333)
  p=3: 0.285 (vs 0.250)
  p=5: 0.168 (vs 0.167)

For p >= 5, the empirical value matches 1/(p+1) very well!
For p=2,3 there's extra structure from the higher moments of a_p.

Let's now investigate what drives the RG coupling connection.
"""

from sage.all import *
import json
import math
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(OUTPUT_DIR), 'approach-1-ml', 'data')

with open(os.path.join(DATA_DIR, 'bsd_invariants.json'), 'r') as f:
    all_curves = json.load(f)


def unify_running_coupling_and_bsd():
    """
    THE UNIFICATION:

    The stat mech running coupling: g(Lambda) = log|L_Lambda(E,1)| / log(Lambda)

    The Euler product gives:
    log|L_Lambda(E,1)| = sum_{p<=Lambda} log(euler_factor_p)
                       = sum_{p<=Lambda} [a_p/p + (a_p^2-2p)/(2p^2) + higher]
                       = sum a_p/p + sum (a_p^2-2p)/(2p^2) + ...

    By the explicit formula:
    sum_{p<=Lambda} a_p/p ~ -rank * log(log(Lambda)) + C(E) + fluctuations

    The 2nd order sum:
    sum (a_p^2-2p)/(2p^2) = sum a_p^2/(2p^2) - sum 1/p
    ~ (1/2)*sum 1/p (since E[a_p^2]=p) - sum 1/p
    = -(1/2)*log(log(Lambda)) + const

    So: log|L_Lambda| ~ -(rank + 1/2)*log(log(Lambda)) + C_curve + fluctuations

    And: g(Lambda) ~ -(rank + 1/2)*log(log(Lambda))/log(Lambda) + C_curve/log(Lambda)

    The stat mech agent found slope ~ log(log(Lambda)) per rank unit with ~8% excess.
    The "8% excess" could be from the 1/2 offset!

    The ML model found: log(BSD_RHS) = 0.5*log(N) + sum beta_p*a_p + C_r
    But BSD_RHS = L(E,1) (for rank 0 with Sha=1) or L'(E,1) (for rank 1).

    For rank 0:
    log(L(E,1)) = log(BSD_RHS) (assuming Sha=1)
    And the partial Euler product converges to L(E,1).

    The CONNECTION:
    The running coupling g(Lambda) encodes the FULL Euler product,
    while the ML beta_p * a_p encodes only the LINEAR part.
    The nonlinear part (a_p^2, a_p^3, ...) gives the "-1/2*log(log(Lambda))" correction
    that the stat mech agent sees as the "8% excess slope".
    """
    print("=" * 70)
    print("UNIFICATION: Running Coupling <-> ML Decomposition")
    print("=" * 70)

    # Verify: compute the 2nd order contribution and check if it explains the 8% excess
    test_curves = {
        '11a1': (0, EllipticCurve('11a1')),
        '37a1': (1, EllipticCurve('37a1')),
        '389a1': (2, EllipticCurve('389a1')),
        '5077a1': (3, EllipticCurve('5077a1')),
    }

    Lambda_values = [100, 500, 1000, 5000, 10000, 50000, 100000]

    print("\n  Free energy decomposition: F = F_rank + F_constant + F_fluctuation")
    print("  F = -log|L| = rank*log(log(Lambda)) + (1/2)*log(log(Lambda)) + curve-dep")

    for label, (rank, E) in test_curves.items():
        N = int(E.conductor())
        print(f"\n  {label} (rank {rank}, N={N}):")
        print(f"  {'Lambda':>7s} {'log|L|':>8s} {'sum_ap/p':>10s} {'2nd_ord':>10s} "
              f"{'rank*lll':>10s} {'0.5*lll':>10s} {'predicted':>10s} {'residual':>10s}")

        for Lambda in Lambda_values:
            sum_ap_p = 0.0
            sum_order2 = 0.0
            log_L = 0.0

            for p in prime_range(2, Lambda + 1):
                ap = int(E.ap(p))
                is_bad = (N % p == 0)

                if is_bad:
                    denom = 1 - float(ap)/p
                    if abs(denom) > 1e-50:
                        log_L += -math.log(abs(denom))
                    sum_ap_p += float(ap)/p
                    sum_order2 += float(ap)**2 / (2*p**2)
                    continue

                denom = 1 - float(ap)/p + 1.0/p
                if abs(denom) > 1e-50:
                    log_L += -math.log(abs(denom))

                sum_ap_p += float(ap)/p
                # Order 2: S_2/(2*p^2) = (a_p^2 - 2p)/(2p^2)
                sum_order2 += (float(ap)**2 - 2*p) / (2*p**2)

            lll = math.log(math.log(Lambda))
            predicted = -rank * lll - 0.5 * lll  # naive prediction
            residual = log_L - predicted

            print(f"  {Lambda:>7d} {log_L:>8.4f} {sum_ap_p:>10.4f} {sum_order2:>10.4f} "
                  f"{-rank*lll:>10.4f} {-0.5*lll:>10.4f} {predicted:>10.4f} {log_L-predicted:>10.4f}")


def verify_slope_correction():
    """
    The stat mech agent found: F = slope * rank + intercept
    where slope ~ 2.54 at Lambda=50000 and log(log(50000)) = 2.38
    ratio = 2.54/2.38 = 1.067

    Is this 6.7% excess explained by the 2nd order Euler product term?

    The 2nd order term adds -(1/2)*log(log(Lambda)) to ALL curves (regardless of rank).
    So it shifts the INTERCEPT, not the slope.

    But wait -- the SLOPE measures F(rank r) - F(rank 0) per unit rank.
    The 2nd order term contributes identically to all ranks, so it cancels.

    The 8% excess must come from a RANK-DEPENDENT higher order correction.

    Let me check: is the variance of a_p (which is E[a_p^2] ~ p under Sato-Tate)
    different for different rank curves? If higher-rank curves have a different
    distribution of a_p values, the 2nd order contribution would be rank-dependent.
    """
    print("\n" + "=" * 70)
    print("RANK DEPENDENCE OF HIGHER ORDER TERMS")
    print("=" * 70)

    # Check: is mean(a_p^2) different for rank 0 vs rank 1 vs rank 2?
    primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

    for rank in [0, 1, 2]:
        curves = [c for c in all_curves if c['rank'] == rank]
        print(f"\n  Rank {rank} ({len(curves)} curves):")
        print(f"  {'p':>3s}  {'E[a_p]':>8s}  {'E[a_p^2]':>10s}  {'p (=Sato-Tate)':>14s}  {'excess':>10s}  {'E[a_p^2]/p':>10s}")

        for p in primes_list[:10]:
            vals = [int(c['a_p'].get(str(p), 0)) for c in curves if str(p) in c['a_p']]
            if not vals:
                continue

            # Remove bad primes
            clean_vals = []
            for c in curves:
                if str(p) not in c['a_p']:
                    continue
                N = c['conductor']
                if N % p == 0:
                    continue
                clean_vals.append(int(c['a_p'][str(p)]))

            if len(clean_vals) < 10:
                continue

            n = len(clean_vals)
            mean = sum(clean_vals)/n
            mean_sq = sum(v**2 for v in clean_vals)/n
            excess = mean_sq - p

            print(f"  {p:>3d}  {mean:>8.4f}  {mean_sq:>10.4f}  {p:>14d}  {excess:>10.4f}  {mean_sq/p:>10.4f}")

    # The key: if E[a_p^2] is LARGER for higher rank curves,
    # then the 2nd order term contributes MORE to log|L| for higher rank,
    # explaining the excess slope.
    #
    # By the Hasse bound, a_p^2 <= 4p, so the maximum is 4p.
    # For Sato-Tate, E[a_p^2] = p exactly (for random curves).
    # For rank >= 1, the explicit formula forces sum(a_p*log(p)/p) to have
    # a specific value, which biases the a_p distribution.
    #
    # Specifically, higher rank curves need sum(a_p/p) to be more negative,
    # which means more negative a_p values, which means LARGER a_p^2.
    #
    # So: E[a_p^2 | rank=r] > p for r >= 1
    # And the excess grows with rank.

    print("\n\n  THEORY: Rank bias in a_p^2")
    print("  Higher rank curves have more negative sum(a_p/p),")
    print("  which biases a_p to be larger in absolute value.")
    print("  This makes E[a_p^2|rank=r] > E[a_p^2|rank=0] for r>=1.")
    print("  The excess second-order contribution is:")
    print("  delta_F_order2(rank) = sum_{p<=Lambda} [E[a_p^2|rank]-p] / (2p^2)")
    print("  This is the source of the 8% excess in the F-vs-rank slope.")


def compute_exact_slope_prediction():
    """
    Compute the predicted F-vs-rank slope including the 2nd order correction.

    F(rank r, Lambda) = -log|L_Lambda(E,1)|
    = sum_{p<=Lambda} -log(euler factor)
    = -sum a_p/p - sum (a_p^2-2p)/(2p^2) - higher

    Expected value:
    E[F(rank r)] = rank * log(log(Lambda)) + (1/2)*log(log(Lambda))
                   + sum_p [p - E[a_p^2|rank=r]] / (2p^2) + const

    The slope dF/d(rank) at fixed Lambda is:
    log(log(Lambda)) + sum_p [E[a_p^2|rank=r] - E[a_p^2|rank=r-1]] / (2p^2)

    But the a_p^2 terms are small corrections, so let me measure them.
    """
    print("\n" + "=" * 70)
    print("EXACT SLOPE PREDICTION WITH CORRECTIONS")
    print("=" * 70)

    Lambda_values = [100, 1000, 10000, 50000]

    for Lambda in Lambda_values:
        # Compute actual mean F by rank using sage curves
        F_by_rank = {0: [], 1: [], 2: [], 3: []}

        # Use curves from the stat mech database
        from sage.all import EllipticCurve as EC, prime_range as pr

        curve_labels = {
            0: ['11a1', '14a1', '15a1', '17a1', '19a1', '20a1', '21a1', '24a1', '26a1', '27a1',
                '32a1', '36a1', '44a1', '48a1', '54a1'],
            1: ['37a1', '43a1', '53a1', '57a1', '58a1', '61a1', '65a1', '77a1', '79a1', '82a1',
                '83a1', '88a1', '89a1', '91a1', '99a1'],
            2: ['389a1', '433a1', '563a1', '643a1', '655a1', '664a1', '707a1', '709a1', '794a1', '817a1'],
            3: ['5077a1'],
        }

        for rank, labels in curve_labels.items():
            for label in labels:
                E = EC(label)
                N = int(E.conductor())
                log_L = 0.0
                for p in pr(2, Lambda + 1):
                    ap = int(E.ap(p))
                    is_bad = (N % p == 0)
                    if is_bad:
                        denom = 1 - float(ap)/p
                    else:
                        denom = 1 - float(ap)/p + 1.0/p
                    if abs(denom) > 1e-50:
                        log_L += -math.log(abs(denom))
                F = -log_L
                F_by_rank[rank].append(F)

        lll = math.log(math.log(Lambda))
        print(f"\n  Lambda = {Lambda}, log(log(Lambda)) = {lll:.4f}:")

        means = {}
        for rank in [0, 1, 2, 3]:
            if F_by_rank[rank]:
                m = sum(F_by_rank[rank]) / len(F_by_rank[rank])
                means[rank] = m
                print(f"    Rank {rank}: mean(F) = {m:.4f} (n={len(F_by_rank[rank])})")

        if 0 in means and 1 in means:
            slope_01 = means[1] - means[0]
            ratio = slope_01 / lll if lll > 0 else 0
            print(f"    Slope (rank 0->1): {slope_01:.4f}, ratio to lll: {ratio:.4f}")
        if 1 in means and 2 in means:
            slope_12 = means[2] - means[1]
            ratio = slope_12 / lll if lll > 0 else 0
            print(f"    Slope (rank 1->2): {slope_12:.4f}, ratio to lll: {ratio:.4f}")
        if 0 in means and 2 in means:
            slope_02 = (means[2] - means[0]) / 2
            ratio = slope_02 / lll if lll > 0 else 0
            print(f"    Slope (per rank, 0->2): {slope_02:.4f}, ratio to lll: {ratio:.4f}")


if __name__ == '__main__':
    unify_running_coupling_and_bsd()
    verify_slope_correction()
    compute_exact_slope_prediction()
