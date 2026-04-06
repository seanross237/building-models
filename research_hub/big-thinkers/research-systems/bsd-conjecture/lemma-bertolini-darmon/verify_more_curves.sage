"""
Broader verification: rank-2 and rank-3 curves at small primes.

For each (E, p), we compute:
  - Reg_p (Schneider p-adic regulator)
  - log_p(1+p)^r
  - L_p^(r)(0)/r! from the SAGE p-adic L-series
  - The predicted RHS = (1-1/alpha)^2 * Reg_p / log(g)^r
  - Verify: ratio = 1 to as many digits as possible

This tests whether Reg_p / log(g)^r matches the leading coefficient
(modulo the (1-1/alpha)^2 Euler factor) — i.e. whether the lemma
identification R_der = Reg_p / log(g)^r holds with unit u = 1.
"""
import time

def verify(label, p, n_terms=6):
    print(f"\n=== {label} at p={p}, n_terms={n_terms} ===", flush=True)
    E = EllipticCurve(label)
    r = E.rank()
    print(f"  rank = {r}", flush=True)
    if E.has_bad_reduction(p):
        print(f"  bad reduction; skip")
        return
    a_p = E.ap(p)
    if a_p % p == 0:
        print(f"  supersingular (a_p={a_p}); skip")
        return
    print(f"  a_p = {a_p}", flush=True)

    PREC = 20
    K = Qp(p, PREC)
    R.<x> = PolynomialRing(K)
    alpha = [rt for rt in (x^2 - a_p*x + p).roots(multiplicities=False) if rt.valuation() == 0][0]
    fac = (1 - 1/alpha)^2
    log_g = K(1+p).log()

    t0 = time.time()
    Reg_p = E.padic_regulator(p, PREC)
    print(f"  Reg_p computed in {time.time()-t0:.1f}s, val = {Reg_p.valuation()}", flush=True)

    Tam = prod(E.tamagawa_numbers())
    tors = E.torsion_order()
    Q = K(Tam) / K(tors^2)  # Sha = 1 typically
    rhs = fac * Reg_p / log_g^r * Q
    print(f"  RHS = {rhs}", flush=True)

    t0 = time.time()
    Lps = E.padic_lseries(p).series(n=n_terms, prec=PREC)
    print(f"  L-series computed in {time.time()-t0:.1f}s", flush=True)
    coeffs = Lps.list()
    if len(coeffs) <= r:
        print(f"  not enough coeffs ({len(coeffs)})")
        return
    leading = coeffs[r]
    print(f"  L_p^({r})/{r}! = {leading}", flush=True)
    if leading.precision_absolute() < 1:
        print(f"  precision too low")
        return
    diff = leading - rhs
    val_diff = diff.valuation()
    print(f"  difference val = {val_diff}", flush=True)
    print(f"  ratio = {leading / rhs}", flush=True)
    print(f"  val(ratio - 1) = {(leading/rhs - 1).valuation()}", flush=True)
    return val_diff

# Rank-2 curves at p=5,7
results = []
for label in ['389a1', '433a1', '563a1', '643a1', '709a1', '997b1']:
    for p in [5, 7]:
        v = verify(label, p, n_terms=6)
        if v is not None:
            results.append((label, p, v))

# A rank-3 curve
print("\n\n*** Rank-3 test ***", flush=True)
for label in ['5077a1']:
    for p in [5, 7]:
        v = verify(label, p, n_terms=6)
        if v is not None:
            results.append((label, p, v))

print("\n\n=== SUMMARY ===")
for label, p, v in results:
    print(f"  {label:8s} p={p:2d}: val(L_p^(r) - RHS) = {v}")
