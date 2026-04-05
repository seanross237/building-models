#!/usr/bin/env sage
"""
Systematic computation of Iwasawa lambda invariants vs algebraic rank.
Tests the key hypothesis: ord_{T=0} L_p(E,T) = rank(E(Q)) for ordinary primes p.
"""

# Test curves spanning ranks 0-3, plus some with nontrivial Sha
test_curves = [
    # (label, expected_rank, expected_sha_order)
    # Rank 0
    ("11a1", 0, 1),
    ("14a1", 0, 1),
    ("15a1", 0, 1),
    ("17a1", 0, 1),
    ("19a1", 0, 1),
    ("20a1", 0, 1),
    ("21a1", 0, 1),
    ("24a1", 0, 1),
    ("26a1", 0, 1),
    ("27a1", 0, 1),
    # Rank 0 with Sha
    ("571a1", 0, 4),
    ("681b1", 0, 9),
    # Rank 1
    ("37a1", 1, 1),
    ("43a1", 1, 1),
    ("53a1", 1, 1),
    ("57a1", 1, 1),
    ("58a1", 1, 1),
    ("61a1", 1, 1),
    ("77a1", 1, 1),
    ("79a1", 1, 1),
    ("83a1", 1, 1),
    ("89a1", 1, 1),
    # Rank 2
    ("389a1", 2, 1),
    ("433a1", 2, 1),
    # Rank 3
    ("5077a1", 3, 1),
]

primes_test = [3, 5, 7, 11, 13]

results = []
header = "{:<10} {:<5} {:<6} {:<4} {:<10} {:<12}".format(
    "Curve", "Rank", "|Sha|", "p", "ord_T Lp", "lambda=rank?"
)
print("=" * 60)
print("ord_{{T=0}} L_p(E,T) vs rank(E(Q))")
print("=" * 60)
print(header)
print("-" * 60)

for label, exp_rank, exp_sha in test_curves:
    try:
        E = EllipticCurve(label)
        rank = E.rank()
    except Exception:
        continue

    for p in primes_test:
        if E.conductor() % p == 0:
            continue
        if not E.is_ordinary(p):
            continue

        try:
            Lp = E.padic_lseries(p)
            n_terms = max(rank + 3, 6)
            series = Lp.series(n=n_terms)

            # Extract order of vanishing
            ord_van = None
            for i in range(n_terms):
                try:
                    coeff = series[i]
                    if coeff.valuation() < coeff.precision_absolute():
                        ord_van = i
                        break
                except Exception:
                    pass

            if ord_van is None:
                ord_str = ">=" + str(n_terms)
                match = "MAYBE"
            else:
                ord_str = str(ord_van)
                match = "YES" if ord_van == rank else "NO"

            results.append((label, rank, exp_sha, p, ord_van, match))
            line = "{:<10} {:<5} {:<6} {:<4} {:<10} {:<12}".format(
                label, rank, exp_sha, p, ord_str, match
            )
            print(line)

        except Exception as e:
            pass

# Summary
print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)
yes_count = sum(1 for r in results if r[5] == "YES")
no_count = sum(1 for r in results if r[5] == "NO")
maybe_count = sum(1 for r in results if r[5] == "MAYBE")
total = len(results)
print("Total tests: {}".format(total))
if total > 0:
    print("lambda = rank: {} ({:.1f}%)".format(yes_count, 100.0 * yes_count / total))
    print("lambda != rank: {} ({:.1f}%)".format(no_count, 100.0 * no_count / total))
    print("inconclusive: {} ({:.1f}%)".format(maybe_count, 100.0 * maybe_count / total))

# Check the no cases
if no_count > 0:
    print()
    print("Cases where lambda != rank:")
    for r in results:
        if r[5] == "NO":
            print("  {}: rank={}, |Sha|={}, p={}, ord={}".format(r[0], r[1], r[2], r[3], r[4]))

# Analyze by rank
print()
print("=" * 60)
print("ANALYSIS BY RANK")
print("=" * 60)
for rk in range(4):
    rk_results = [r for r in results if r[1] == rk]
    if not rk_results:
        continue
    rk_yes = sum(1 for r in rk_results if r[5] == "YES")
    rk_total = len(rk_results)
    print("Rank {}: {}/{} match ({:.1f}%)".format(rk, rk_yes, rk_total, 100.0 * rk_yes / rk_total))

# Analyze Sha cases specifically
print()
print("=" * 60)
print("SHA ANALYSIS")
print("=" * 60)
sha_results = [r for r in results if r[2] > 1]
if sha_results:
    for r in sha_results:
        print("  {}: rank={}, |Sha|={}, p={}, ord={}, match={}".format(
            r[0], r[1], r[2], r[3], r[4], r[5]))
    sha_yes = sum(1 for r in sha_results if r[5] == "YES")
    print("Curves with nontrivial Sha: {}/{} match".format(sha_yes, len(sha_results)))
else:
    print("No curves with nontrivial Sha had ordinary primes in test set")
