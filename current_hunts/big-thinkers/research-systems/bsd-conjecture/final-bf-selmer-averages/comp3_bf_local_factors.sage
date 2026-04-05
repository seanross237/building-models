"""
Computation 3: BF Local Factor Analysis

In the arithmetic BF theory (Carlson-Kim, Park-Park), the partition function
Z_BF factorizes as a product of local factors:

    Z_BF(E) = prod_{v} Z_v(E)

where v ranges over all places of Q.

For an elliptic curve E/Q with good reduction at a prime q != p:
    - The local Selmer condition at q is:
      im(E(Q_q)/pE(Q_q) -> H^1(Q_q, E[p]))
    - The local BF factor Z_q involves the local Tamagawa number and
      the local Euler factor

For the p-Selmer group, the local condition at q (good reduction) is:
    H^1_f(Q_q, E[p]) = ker(H^1(Q_q, E[p]) -> H^1(Q_q^nr, E[p]))

The LOCAL contribution to |Sel_p| at q is related to:
    |H^1_f(Q_q, E[p])| / |H^0(Q_q, E[p])|

We compute these local factors for many curves and check whether
their product/average matches the Poonen-Rains prediction.
"""

print("="*70)
print("COMPUTATION 3: BF LOCAL FACTORS AND SELMER STRUCTURE")
print("="*70)

# ============================================================
# Part A: Local Selmer conditions at good primes
# ============================================================

print("\nPart A: Local Selmer conditions at primes of good reduction")
print("-"*50)

def local_selmer_data(E, q, p):
    """
    Compute local Selmer data at a prime q for the p-Selmer group.

    For good reduction at q:
    - |E(F_q)| = q + 1 - a_q
    - |E(F_q)[p]| depends on a_q mod p
    - The local condition is: image of kappa_q: E(Q_q)/pE(Q_q) -> H^1(Q_q, E[p])

    Key formula: |E(Q_q)/pE(Q_q)| = p^(dim) where
        dim = v_p(|E(F_q)|) (for good reduction)

    This is because E(Q_q) has a filtration:
        0 -> E_1(Q_q) -> E_0(Q_q) -> E(F_q) -> 0
    and E_1(Q_q) ~ Z_q (formal group), so E_1(Q_q)/p ~ 0 or Z/pZ.
    """
    if E.has_good_reduction(q):
        a_q = E.ap(q)
        e_fq = q + 1 - a_q  # |E(F_q)|

        # v_p(|E(F_q)|)
        vp = 0
        temp = e_fq
        while temp % p == 0:
            vp += 1
            temp = temp // p

        return {
            'a_q': a_q,
            '|E(F_q)|': e_fq,
            'v_p(|E(F_q)|)': vp,
            '|local_image|': p^vp,
            'reduction': 'good'
        }
    else:
        c_q = E.tamagawa_number(q)
        vp = 0
        temp = c_q
        while temp % p == 0:
            vp += 1
            temp = temp // p
        return {
            'c_q': c_q,
            'v_p(c_q)': vp,
            '|local_image|': p^vp,
            'reduction': 'bad'
        }

# Test with specific curves
test_curves = {
    '11a1': 0,
    '37a1': 1,
    '389a1': 2,
    '5077a1': 3
}

for label, expected_rank in test_curves.items():
    E = EllipticCurve(label)
    N = E.conductor()
    print(f"\n{label} (rank {expected_rank}, N={N}):")

    for p in [2, 3, 5, 7]:
        print(f"\n  p = {p}:")
        # Check local conditions at small good primes
        product = 1
        for q in primes_first_n(20):
            if q == p:
                continue
            data = local_selmer_data(E, q, p)
            if data['reduction'] == 'good' and data['v_p(|E(F_q)|)'] > 0:
                print(f"    q={q}: a_q={data['a_q']}, |E(F_q)|={data['|E(F_q)|']}, "
                      f"v_p={data['v_p(|E(F_q)|)']}, |local|={data['|local_image|']}")
                product *= data['|local_image|']

# ============================================================
# Part B: The Poonen-Rains local prediction
# ============================================================

print("\n\n" + "="*70)
print("Part B: Poonen-Rains Local Prediction")
print("-"*50)

print("""
The Poonen-Rains model predicts:
  For random E over Q_q with good reduction at q:
    Pr[|E(F_q)| = 0 mod p] = 1/p + 1/p^2 - 1/p^3 + ...  (for large q)

  More precisely, the distribution of a_q mod p for random curves gives:
    Pr[p | |E(F_q)|] = Pr[a_q = q+1 mod p]

  For large q, by Hasse-Weil, a_q is roughly uniformly distributed mod p
  (by Chebotarev/Sato-Tate), so:
    Pr[p | |E(F_q)|] ~ 1/p

  The BF local factor at q for the p-Selmer group is:
    Z_q^{BF} ~ E[|local Selmer at q|] = 1 + (1/p - 1/p^2) + ...
""")

# Verify: for random curves, what fraction have p | |E(F_q)|?
print("Verification: fraction of curves with p | |E(F_q)| for various q")
print(f"{'q':>5} | {'p=2':>8} | {'p=3':>8} | {'p=5':>8} | {'p=7':>8} | {'p=11':>8}")
print("-"*55)

for q in [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 97]:
    fracs = []
    for p in [2, 3, 5, 7, 11]:
        if p == q:
            fracs.append("  ---  ")
            continue
        # Count curves over F_q with |E(F_q)| = 0 mod p
        # Parameterize by (a4, a6) in F_q
        count_div = 0
        count_total = 0
        Fq = GF(q)
        for a4 in Fq:
            for a6 in Fq:
                try:
                    E_fq = EllipticCurve(Fq, [a4, a6])
                    n = E_fq.order()
                    count_total += 1
                    if n % p == 0:
                        count_div += 1
                except:
                    continue
        if count_total > 0:
            frac = RR(count_div) / count_total
            fracs.append(f"{frac:.4f}")
        else:
            fracs.append("  err  ")

    print(f"{q:>5} | " + " | ".join(fracs))

print(f"\nPredicted (1/p):   | {'0.5000':>8} | {'0.3333':>8} | {'0.2000':>8} | {'0.1429':>8} | {'0.0909':>8}")

# ============================================================
# Part C: The product of local factors
# ============================================================

print("\n\n" + "="*70)
print("Part C: Product of Local Factors and Global Selmer Size")
print("-"*50)

print("""
In BF theory, the partition function factorizes:
    Z_BF = prod_v Z_v

For the p-Selmer group, each local factor Z_q contributes:
    Z_q = |H^1_f(Q_q, E[p])| / |H^0(Q_q, E[p])|

The GLOBAL Selmer group size is:
    |Sel_p(E)| = |H^1_f(Q, E[p])| = some subset of prod_v |H^1_f(Q_v, E[p])|

The BF theory says: Z_BF = |Sel_p(E)| * |Sel_p(E^dual)| / correction

For self-dual E (which all elliptic curves are):
    Z_BF = |Sel_p(E)|^2 / |E[p](Q)| (roughly)

Actually, the precise formula involves the Cassels-Tate pairing:
    Z_BF = |Sel_p(E)| * (product of local terms)

The key insight for averaging:
    E[Z_BF] = E[|Sel_p(E)|] * E[product of local terms]

If the local terms are "independent" across primes (the Poonen-Rains
independence hypothesis), then:
    E[Z_BF] = product_v E[Z_v]
""")

# Compute the product of local E[Z_q] for the p-Selmer problem
# E[Z_q] = sum_E Z_q(E) / #curves ~ 1 + correction terms

# For good reduction at q:
# E[|Sel_p condition at q|] = E[p^(v_p(|E(F_q)|))]
# = sum_{k>=0} p^k * Pr[v_p(|E(F_q)|) >= k]

print("Average local Selmer factor at q for p-Selmer:")
print(f"{'q':>5} | {'p=2':>10} | {'p=3':>10} | {'p=5':>10} | {'p=7':>10}")
print("-"*50)

for q in [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
    avgs = []
    for p in [2, 3, 5, 7]:
        if p == q:
            avgs.append("   ---   ")
            continue
        # Average of p^(v_p(|E(F_q)|)) over all curves E/F_q
        total_factor = 0
        count = 0
        Fq = GF(q)
        for a4 in Fq:
            for a6 in Fq:
                try:
                    E_fq = EllipticCurve(Fq, [a4, a6])
                    n = E_fq.order()
                    vp = 0
                    temp = n
                    while temp % p == 0:
                        vp += 1
                        temp = temp // p
                    total_factor += p^vp
                    count += 1
                except:
                    continue
        if count > 0:
            avg_factor = RR(total_factor) / count
            avgs.append(f"{avg_factor:.5f}")
        else:
            avgs.append("   err   ")
    print(f"{q:>5} | " + " | ".join(avgs))

print(f"\nNote: if these converge to 1 as q -> inf, the product converges.")
print(f"The rate of convergence determines the global average.")
