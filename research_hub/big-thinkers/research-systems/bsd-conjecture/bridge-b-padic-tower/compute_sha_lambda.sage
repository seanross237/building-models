#!/usr/bin/env sage
"""
Test the critical connection: lambda_p = rank iff Sha[p^infty] is finite.

For curves with known nontrivial Sha, check whether lambda_p > rank
(which would indicate Sha[p^infty] contributes to the lambda invariant).

Key theory:
- lambda >= rank always (Kato, Skinner-Urban)
- lambda = rank + dim(Sha[p^infty]) in many cases
- More precisely: lambda = corank_Zp(Sel_p^infty) = rank + corank_Zp(Sha[p^infty])
- Sha[p^infty] finite iff corank_Zp(Sha[p^infty]) = 0 iff lambda = rank

For KNOWN curves with nontrivial Sha:
- Sha is always finite (no known counterexamples)
- So Sha[p^infty] should be finite for all p
- Hence lambda_p should equal rank for all ordinary p
"""

print("=" * 80)
print("SHA-LAMBDA CONNECTION TEST")
print("=" * 80)
print()
print("Theory: lambda_p = rank(E) + corank(Sha[p^infty])")
print("        Sha[p^infty] finite <==> lambda_p = rank(E)")
print()

# Curves with nontrivial Sha from the Cremona database
sha_curves = [
    # (label, rank, |Sha|, Sha_structure)
    ("571a1", 0, 4, "C2 x C2"),
    ("681b1", 0, 9, "C3 x C3"),
    ("960d1", 0, 4, "C2 x C2"),
    ("1058d1", 0, 4, "C2 x C2"),
    ("1073a1", 0, 4, "C2 x C2"),
    ("1246b1", 0, 9, "C3 x C3"),
    ("1483a1", 0, 9, "C3 x C3"),
    ("1613a1", 0, 4, "C2 x C2"),
    ("2006e1", 0, 9, "C3 x C3"),
    ("2366d1", 0, 9, "C3 x C3"),
    ("2834d1", 0, 9, "C3 x C3"),
    ("3054a1", 0, 4, "C2 x C2"),
    ("3364c1", 0, 9, "C3 x C3"),
    ("4229a1", 0, 25, "C5 x C5"),
    # Rank 1 curves with Sha (rare but exist)
    # Actually for rank <=1, Sha finiteness is proved by Kolyvagin.
    # The interesting case would be rank >=2 with nontrivial Sha, but these are rare.
]

test_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

print("{:<12} {:<5} {:<8} {:<12} {:<6} {:<8} {:<12}".format(
    "Curve", "Rank", "|Sha|", "Sha_struct", "p", "lambda", "lambda=rank?"
))
print("-" * 70)

all_results = []

for label, exp_rank, sha_order, sha_struct in sha_curves:
    try:
        E = EllipticCurve(label)
        rank = E.rank()
    except Exception:
        continue

    for p in test_primes:
        if E.conductor() % p == 0:
            continue
        if not E.is_ordinary(p):
            continue

        try:
            Lp = E.padic_lseries(p)
            n_terms = 6
            series = Lp.series(n=n_terms)

            lam = None
            for i in range(n_terms):
                coeff = series[i]
                if coeff.valuation() < coeff.precision_absolute():
                    lam = i
                    break

            if lam is not None:
                match = "YES" if lam == rank else "NO (lambda={})".format(lam)
                all_results.append((label, rank, sha_order, p, lam, lam == rank))
                print("{:<12} {:<5} {:<8} {:<12} {:<6} {:<8} {}".format(
                    label, rank, sha_order, sha_struct, p, lam, match
                ))
        except Exception:
            pass

print()
print("=" * 80)
print("SUMMARY FOR CURVES WITH NONTRIVIAL SHA")
print("=" * 80)

total = len(all_results)
matches = sum(1 for r in all_results if r[5])
print("Total (curve, prime) pairs tested: {}".format(total))
print("lambda = rank (Sha[p^infty] appears finite): {} ({:.1f}%)".format(
    matches, 100.0 * matches / total if total > 0 else 0))
mismatches = [(r[0], r[2], r[3], r[4]) for r in all_results if not r[5]]
if mismatches:
    print()
    print("MISMATCHES (lambda != rank):")
    for label, sha, p, lam in mismatches:
        print("  {} (|Sha|={}): p={}, lambda={}".format(label, sha, p, lam))
        # Check if p divides |Sha|
        if sha % p == 0:
            print("    NOTE: p | |Sha| -- this is expected! Sha[p] nontrivial.")
            print("    BUT lambda should still = rank if Sha[p^infty] is FINITE.")
else:
    print()
    print("ALL MATCH: lambda_p = rank for every ordinary prime tested.")
    print("This is consistent with Sha[p^infty] being finite for all p.")
    print()
    print("KEY IMPLICATION: For these curves, the tower growth rate of Z_BF")
    print("determines rank(E(Q)) WITHOUT assuming Sha finiteness --")
    print("because the growth rate IS the lambda invariant, and lambda = rank")
    print("is a COMPUTATIONAL FACT for these curves, not an assumption.")

# Special analysis: primes dividing |Sha|
print()
print("=" * 80)
print("SPECIAL: Primes p dividing |Sha|")
print("=" * 80)
print()
print("When p | |Sha|, the p-part of Sha is nontrivial: Sha[p] != 0.")
print("But Sha[p^infty] can still be finite (just = Sha[p] = (Z/pZ)^2).")
print("So we should still have lambda = rank.")
print()

for label, exp_rank, sha_order, sha_struct in sha_curves:
    E = EllipticCurve(label)
    rank = E.rank()

    # Find primes dividing Sha
    sha_primes = [p for p in prime_divisors(sha_order)]

    for p in sha_primes:
        if E.conductor() % p == 0:
            print("{}: p={} divides |Sha|={} but also divides conductor -- skip".format(
                label, p, sha_order))
            continue
        if not E.is_ordinary(p):
            print("{}: p={} divides |Sha|={} but is supersingular -- skip".format(
                label, p, sha_order))
            continue

        try:
            Lp = E.padic_lseries(p)
            series = Lp.series(n=6)

            lam = None
            for i in range(6):
                coeff = series[i]
                if coeff.valuation() < coeff.precision_absolute():
                    lam = i
                    break

            print("{}: p={} divides |Sha|={}, lambda={}, rank={}, match={}".format(
                label, p, sha_order, lam, rank, lam == rank))

            # Also check: does the constant term have valuation > 0?
            # If Sha[p] is nontrivial, then |Sel_p| is larger, which affects
            # the p-adic valuation of g_E(0)
            if rank == 0 and lam == 0:
                v0 = series[0].valuation()
                print("  v_p(g_E(0)) = {} (nonzero iff p | |Sel_p| = {} * torsion * |Sha[p]|)".format(
                    v0, sha_order))

        except Exception as e:
            print("{}: p={} error: {}".format(label, p, e))
