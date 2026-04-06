"""
High-precision verification of the BD-Reg lemma identity for 389a1.
Goal: confirm to 6+ digits that the unit u in the lemma is 1.
"""

E = EllipticCurve('389a1')
print(f"E = 389a1, rank {E.rank()}")
r = 2

for p in [5, 7, 11]:
    if E.has_bad_reduction(p):
        print(f"Skip p={p} (bad reduction)")
        continue
    a_p = E.ap(p)
    if a_p % p == 0:
        print(f"Skip p={p} (supersingular)")
        continue
    print(f"\n=== p = {p}, a_p = {a_p} ===", flush=True)

    # Higher precision Sage settings
    PREC = 25
    print(f"  ambient prec = {PREC}", flush=True)

    K = Qp(p, PREC)
    R.<x> = PolynomialRing(K)
    f = x^2 - a_p*x + p
    roots = f.roots(multiplicities=False)
    alpha = [rt for rt in roots if rt.valuation() == 0][0]
    fac = (1 - 1/alpha)^2

    log_g = K(1+p).log()

    # p-adic regulator at high precision
    print(f"  computing Reg_p at prec {PREC}...", flush=True)
    Reg_p = E.padic_regulator(p, PREC)
    print(f"  val(Reg_p) = {Reg_p.valuation()}, prec = {Reg_p.precision_absolute()}", flush=True)

    # p-adic L-series — try to get more terms
    print(f"  computing p-adic L-series...", flush=True)
    Lp = E.padic_lseries(p)
    # Try larger n_max for more series precision; this is the tight constraint
    Lps = Lp.series(n=5, prec=PREC)
    coeffs = Lps.list()
    print(f"  num coeffs = {len(coeffs)}", flush=True)
    leading_coef = coeffs[r]
    print(f"  L_p^(2)/2! = {leading_coef}", flush=True)
    print(f"    abs prec = {leading_coef.precision_absolute()}", flush=True)

    # Predicted
    rhs = fac * Reg_p / log_g^r
    print(f"  predicted = {rhs}", flush=True)
    print(f"    abs prec = {rhs.precision_absolute()}", flush=True)

    # Both sides should be in O(p^N) for max common N
    common_prec = min(leading_coef.precision_absolute(), rhs.precision_absolute())
    print(f"  common prec = {common_prec}", flush=True)

    diff = leading_coef - rhs
    print(f"  difference = {diff}", flush=True)
    print(f"    val = {diff.valuation()}", flush=True)

    # Ratio
    ratio = leading_coef / rhs
    print(f"  ratio = {ratio}", flush=True)
    print(f"  val(ratio - 1) = {(ratio - 1).valuation()}", flush=True)

print("\n=== higher precision attempt: explicit n loop ===")

# Try Lp.series(n) for several n to see how far we can push
for n in [3, 4, 5, 6, 7]:
    p = 5
    print(f"\n--- p = {p}, n_terms = {n} ---", flush=True)
    Lp = E.padic_lseries(p)
    try:
        Lps = Lp.series(n=n, prec=10)
        coeffs = Lps.list()
        leading = coeffs[2] if len(coeffs) > 2 else None
        print(f"  L_p^(2)/2! = {leading}", flush=True)
        print(f"    abs prec = {leading.precision_absolute() if leading is not None else 'NA'}", flush=True)
    except Exception as e:
        print(f"  ERROR: {e}", flush=True)
