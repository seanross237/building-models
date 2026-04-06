"""
Numerical verification of the BD-Reg lemma:
    Reg_p(E)  =  Reg_{p,der}^cyc(E)  *  log_p(gamma)^r           (in some normalization)
or equivalently
    Reg_{p,der}^cyc(E)  =  Reg_p(E) / log_p(gamma)^r              (in the BD/e_grp normalization)

Strategy:
For E of rank r and prime p of good ordinary reduction, compute:
  - Reg_p(E): determinant of Schneider's p-adic height matrix (SAGE: E.padic_height(p))
  - log_p(gamma) where gamma = 1+p (the standard choice of topological generator of Z_p^x)
  - L_p^(r)(E,0)/r!: leading coefficient of the cyclotomic p-adic L-function
  - The campaign-verified formula:
        L_p^(r)/r!  =  (1-1/alpha)^2 * Reg_p / log_p(gamma)^r * (Sha * Tam / |E_tors|^2)

The lemma claim is:
    L_p^(r)/r!  =  (1-1/alpha)^2 * Reg_{p,der}^cyc * (Sha * Tam / |E_tors|^2)   [Bertolini-Darmon Thm 2.23]

These two are CONSISTENT (i.e. equivalent at the level of equality, not just valuations) iff
    Reg_{p,der}^cyc  =  Reg_p / log_p(gamma)^r

We do NOT have direct SAGE access to Reg_{p,der}^cyc — it's defined in I^r/I^(r+1) tensor Q,
not Q_p. But we can verify the EQUALITY (not just valuation match) of the two sides of the
campaign formula. If they agree as p-adic numbers (not just as valuations), then the unit u in
the lemma identification

    Reg_{p,der}^cyc  =  Reg_p / log_p(gamma)^r  *  u

is exactly 1 (under the e_grp identification), confirming the lemma.
"""

import sys

def compute_for(curve_label, p, prec=20):
    print(f"\n--- {curve_label}, p = {p}, prec = {prec} ---", flush=True)
    E = EllipticCurve(curve_label)
    r = E.rank()
    print(f"  rank r = {r}", flush=True)
    print(f"  cond N = {E.conductor()}", flush=True)

    # Check ordinary good reduction
    if E.has_bad_reduction(p):
        print(f"  SKIP: E has bad reduction at p = {p}")
        return None
    a_p = E.ap(p)
    if a_p % p == 0:
        print(f"  SKIP: E is supersingular at p = {p} (a_p = {a_p})")
        return None
    print(f"  a_p = {a_p}", flush=True)

    # Compute alpha (unit root of x^2 - a_p x + p) in Z_p
    K = Qp(p, prec)
    R.<x> = PolynomialRing(K)
    f = x^2 - a_p*x + p
    roots = f.roots(multiplicities=False)
    alpha = None
    for rt in roots:
        if rt.valuation() == 0:
            alpha = rt
            break
    if alpha is None:
        print(f"  ERROR: no unit root")
        return None
    print(f"  alpha = {alpha} (val 0)", flush=True)
    one_minus_inv_alpha = 1 - 1/alpha
    print(f"  (1 - 1/alpha) = {one_minus_inv_alpha}", flush=True)
    print(f"  (1 - 1/alpha)^2 = {one_minus_inv_alpha^2}", flush=True)

    # log_p(gamma) where gamma = 1+p
    # In SAGE, log of (1+p) in Z_p is computed by .log()
    gamma = K(1 + p)
    log_gamma = gamma.log()
    print(f"  log_p(1+p) = {log_gamma}", flush=True)
    print(f"  val(log_p(1+p)) = {log_gamma.valuation()}", flush=True)

    # Standard p-adic regulator via Schneider's pairing
    print(f"  computing p-adic height pairing...", flush=True)
    try:
        # E.padic_regulator(p, prec) returns det of Schneider height matrix in Q_p
        Reg_p = E.padic_regulator(p, prec)
    except Exception as e:
        print(f"  ERROR computing padic_regulator: {e}")
        return None
    print(f"  Reg_p = {Reg_p}", flush=True)
    print(f"  val(Reg_p) = {Reg_p.valuation()}", flush=True)

    # Compute leading coefficient of L_p(E, T) at T=0
    print(f"  computing p-adic L-function...", flush=True)
    try:
        Lp = E.padic_lseries(p)
        # Series expansion in T: get a power series of length sufficient
        Lps = Lp.series(n=4, prec=prec)
    except Exception as e:
        print(f"  ERROR computing padic_lseries: {e}")
        return None
    print(f"  L_p(E, T) series (first few terms): {Lps}", flush=True)

    # Extract the leading coefficient = L_p^(r)(0) / r!
    # The series is in T, with center at T=0 (which corresponds to s=1)
    coeffs = Lps.list()
    print(f"  coefficient valuations: {[c.valuation() if c != 0 else 'inf' for c in coeffs]}", flush=True)

    # Find the first nonzero coefficient
    leading_idx = None
    for i, c in enumerate(coeffs):
        if c != 0 and c.valuation() < prec:
            leading_idx = i
            break
    if leading_idx is None:
        print(f"  Could not find leading coefficient (precision insufficient?)")
        return None
    print(f"  leading index = {leading_idx} (expected = r = {r})", flush=True)
    if leading_idx != r:
        print(f"  WARNING: leading index {leading_idx} != rank {r}!")
    leading_coef = coeffs[leading_idx]
    print(f"  L_p^({leading_idx})(0) / {leading_idx}! = {leading_coef}", flush=True)

    # Compute the predicted RHS:
    #   (1 - 1/alpha)^2 * Reg_p / log(gamma)^r * (Sha * Tam / |E_tors|^2)
    Sha = 1   # for 389a1, 433a1, etc, the Sha is 1 (BSD known up to Sha)
    Tam = prod(E.tamagawa_numbers())
    tors = E.torsion_order()
    print(f"  Tam = {Tam}, tors = {tors}", flush=True)
    Q = Sha * Tam / tors^2
    print(f"  Q = Sha * Tam / tors^2 = {Q}", flush=True)

    rhs = one_minus_inv_alpha^2 * Reg_p / log_gamma^r * K(Q)
    print(f"  predicted RHS = {rhs}", flush=True)

    # The ratio
    ratio = leading_coef / rhs
    print(f"  ratio L_p^(r)/RHS = {ratio}", flush=True)
    print(f"  val(ratio - 1) = {(ratio - 1).valuation()}", flush=True)

    return {
        "curve": curve_label,
        "p": p,
        "rank": r,
        "Reg_p": Reg_p,
        "log_gamma": log_gamma,
        "leading_coef": leading_coef,
        "rhs": rhs,
        "ratio": ratio,
        "ratio_minus_1_val": (ratio - 1).valuation(),
    }


# Run on rank-2 curves at small primes (good ordinary)
results = []

# 389a1: rank 2, p=5 ordinary (a_5 = -3)
results.append(compute_for('389a1', 5, prec=15))

# 389a1, p=7
results.append(compute_for('389a1', 7, prec=15))

# Rank 2 curves
for label in ['389a1', '433a1', '563a1']:
    for p in [5, 7]:
        try:
            r = compute_for(label, p, prec=12)
            if r is not None:
                results.append(r)
        except Exception as e:
            print(f"  EXCEPTION for {label}, p={p}: {e}", flush=True)

print("\n=== SUMMARY ===")
for r in results:
    if r is not None:
        print(f"  {r['curve']:8s} p={r['p']:2d} rank={r['rank']} val(ratio-1)={r['ratio_minus_1_val']}")
