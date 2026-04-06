# Final check: does Sage's Lp(E,0) agree with interpolation (1-1/alpha)^2 * L(E,1)/Omega?
E = EllipticCurve('11a1')
p = 7
Lp = E.padic_lseries(p)

# Get the constant term of the series in a robust way
series = Lp.series(prec=8, n=5)
print(f"Lp series: {series}")

# Parse out the constant term T^0 coefficient
# The coefficient is itself a p-adic number
zero_coeff = series[0]
print(f"Lp(E, T=0) (constant coefficient of series) = {zero_coeff}")
print(f"  valuation = {zero_coeff.valuation()}")

# Compute the interpolation value in Q_p
Zp_7 = Zp(7, prec=25)
R = PolynomialRing(Zp_7, 'x')
f = R.gen()**2 + 2*R.gen() + 7
roots = f.roots()
alpha = None
for r, _ in roots:
    if r.valuation() == 0:
        alpha = r
        break

euler = (1 - 1/alpha)**2
L_ov_Om = Zp_7(1) / Zp_7(5)
interp = euler * L_ov_Om
print(f"\nInterpolation formula (1-1/alpha_7)^2 * (1/5) = {interp}")
print(f"  valuation = {interp.valuation()}")

# Are they equal?
print(f"\nFirst 8 digits of series constant: {str(zero_coeff)[:100]}")
print(f"First 8 digits of interp value:    {str(interp)[:100]}")

# Compare digit by digit
diff = zero_coeff - interp
print(f"\nDifference (series - interp): {diff}")
print(f"Valuation of difference: {diff.valuation()}")
