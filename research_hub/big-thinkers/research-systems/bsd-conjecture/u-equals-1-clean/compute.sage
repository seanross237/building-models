# Full verification for 11a1 at p=7 clean example
print("=" * 70)
print("VERIFICATION: 11a1 at p = 7 (clean MCS hypotheses)")
print("=" * 70)
E = EllipticCurve('11a1')
p = 7

print(f"Conductor: {E.conductor()}")
print(f"Rank: {E.rank()}")
print(f"Torsion order: {E.torsion_subgroup().order()}")
print(f"Tamagawa product: {E.tamagawa_product()}")
print(f"Semistable: {E.is_semistable()}")
print(f"Optimal (self): {E.optimal_curve() == E}")
print(f"Manin constant: {E.manin_constant()}")
print(f"Good reduction at p={p}: {E.has_good_reduction(p)}")
print(f"a_p: {E.ap(p)}")

Ebar = E.change_ring(GF(p))
order_Ep = Ebar.cardinality()
print(f"|E(F_p)|: {order_Ep}")
print(f"Non-anomalous (p does not divide |E(F_p)|): {order_Ep % p != 0}")
print(f"Ordinary (p does not divide a_p): {E.ap(p) % p != 0}")

rp = E.galois_representation().reducible_primes()
print(f"Reducible primes for rho_bar: {rp}")
print(f"rho_bar irreducible at p={p}: {p not in rp}")
print(f"rho_bar surjective at p={p}: {E.galois_representation().is_surjective(p)}")

tors = E.torsion_subgroup().order()
tam = E.tamagawa_product()
product = tors * tam * order_Ep
print(f"tors * Tam * |E(F_p)| = {tors}*{tam}*{order_Ep} = {product}")
print(f"p divides product? {product % p == 0}")

print(f"L(E,1)/Omega: {E.lseries().L_ratio()}")
print(f"Analytic order of Sha: {E.sha().an()}")

print()
print("=" * 70)
print("p-ADIC L-FUNCTION at p=7")
print("=" * 70)
Lp = E.padic_lseries(p)
print(f"Lp: {Lp}")
# Get the first few terms
try:
    series = Lp.series(prec=6, n=4)
    print(f"Lp series (n=4, prec=6): {series}")
except Exception as e:
    print(f"Series computation: {e}")

# Evaluate at T=0
try:
    val0 = Lp.series(prec=3, n=5)
    print(f"Lp series: {val0}")
    # Extract constant term
    T = val0.parent().gen()
    const = val0.constant_coefficient()
    print(f"Lp(0) (constant term): {const}")
    print(f"v_7(Lp(0)): {const.valuation()}")
except Exception as e:
    print(f"Lp(0) computation: {e}")

# Compute the interpolation formula directly
print()
print("=" * 70)
print("INTERPOLATION FORMULA CHECK")
print("=" * 70)
print("Formula: Lp(E, 0) = (1 - 1/alpha_p)^2 * L(E,1)/Omega")

# a_p = -2, so x^2 + 2x + 7 = 0 gives alpha_7 (unit root mod 7)
# Unit root: we want the root with alpha_7 not divisible by 7
# x^2 + 2x + 7 = 0 => x = -1 +/- sqrt(1-7) = -1 +/- sqrt(-6)
# In Q_7: -6 = 1 mod 7, so sqrt(-6) is a unit
# alpha_7 = -1 + sqrt(-6), beta_7 = -1 - sqrt(-6)
# Product alpha * beta = 7, sum = -2

# Compute in Q_7
Zp7 = Zp(7, prec=20)
R7 = PolynomialRing(Zp7, 'x')
f = R7.gen()**2 + 2*R7.gen() + 7
print(f"Char poly of Frobenius: {f}")
roots = f.roots()
print(f"Roots: {roots}")
for r, mult in roots:
    print(f"  root = {r}, valuation = {r.valuation()}")
# Find unit root
unit_root = None
for r, mult in roots:
    if r.valuation() == 0:
        unit_root = r
        break
if unit_root is not None:
    alpha = unit_root
    print(f"alpha_7 (unit root) = {alpha}")
    print(f"v_7(alpha) = {alpha.valuation()}")
    euler_factor = (1 - 1/alpha)**2
    print(f"(1 - 1/alpha)^2 = {euler_factor}")
    print(f"v_7((1-1/alpha)^2) = {euler_factor.valuation()}")
    L_over_Omega = Zp7(1)/Zp7(5)
    print(f"L(E,1)/Omega = 1/5 in Q_7 = {L_over_Omega}")
    interpolation_value = euler_factor * L_over_Omega
    print(f"Interpolation Lp(E,0) = (1-1/alpha)^2 * (1/5) = {interpolation_value}")
    print(f"v_7(interpolation) = {interpolation_value.valuation()}")
else:
    print("No unit root found")

