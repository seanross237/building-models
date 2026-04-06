"""
Maximum precision verification: 389a1 at p=5, push n_terms as high as feasible.
We want to confirm that ratio = 1 to many digits.
"""
import time

E = EllipticCurve('389a1')
print(f"E = 389a1, rank {E.rank()}", flush=True)

p = 5
PREC = 30

K = Qp(p, PREC)
R.<x> = PolynomialRing(K)
alpha = (x^2 - E.ap(p)*x + p).roots(multiplicities=False)
alpha = [r for r in alpha if r.valuation() == 0][0]
fac = (1 - 1/alpha)^2
log_g = K(1+p).log()

print(f"computing Reg_p at prec {PREC}...", flush=True)
t0 = time.time()
Reg_p = E.padic_regulator(p, PREC)
print(f"  done in {time.time()-t0:.1f}s, Reg_p = {Reg_p}", flush=True)

rhs = fac * Reg_p / log_g^2
print(f"  predicted (high-prec) RHS = {rhs}", flush=True)

# Push n higher and higher
for n in [8, 10, 12]:
    print(f"\n--- n_terms = {n} ---", flush=True)
    Lp = E.padic_lseries(p)
    t0 = time.time()
    try:
        Lps = Lp.series(n=n, prec=PREC)
        elapsed = time.time() - t0
        print(f"  series done in {elapsed:.1f}s", flush=True)
        coeffs = Lps.list()
        leading = coeffs[2]
        print(f"  L_p^(2)/2! = {leading}", flush=True)
        print(f"  abs prec = {leading.precision_absolute()}", flush=True)
        diff = leading - rhs
        print(f"  difference = {diff}", flush=True)
        ratio = leading / rhs
        print(f"  ratio = {ratio}", flush=True)
        print(f"  val(ratio - 1) = {(ratio - 1).valuation()}", flush=True)
    except Exception as e:
        print(f"  ERROR: {e}", flush=True)
        break
