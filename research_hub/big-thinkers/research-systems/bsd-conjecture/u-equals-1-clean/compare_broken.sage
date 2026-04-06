# Compare the BROKEN p=5 example with the CLEAN p=7 example for 11a1
print("=" * 70)
print("COMPARISON: 11a1 at p=5 (BROKEN) vs p=7 (CLEAN)")
print("=" * 70)
E = EllipticCurve('11a1')

for p in [5, 7]:
    print(f"\n--- p = {p} ---")
    print(f"a_p = {E.ap(p)}")
    order_Ep = E.change_ring(GF(p)).cardinality()
    print(f"|E(F_p)| = {order_Ep}")
    anomalous = order_Ep % p == 0
    print(f"Anomalous (p divides |E(F_p)|): {anomalous}  [{'FAIL Hyp 2.11(iii)' if anomalous else 'OK'}]")
    reducible = p in E.galois_representation().reducible_primes()
    print(f"rho_bar reducible at p: {reducible}  [{'FAIL Hyp 2.17' if reducible else 'OK'}]")
    surj = E.galois_representation().is_surjective(p)
    print(f"rho_bar surjective at p: {surj}")
    # Compute interpolation value
    Zp = pAdicField(p, prec=20)
    R = PolynomialRing(Zp, 'x')
    f = R.gen()**2 - E.ap(p)*R.gen() + p
    roots = f.roots()
    unit_root = None
    for r, _ in roots:
        if r.valuation() == 0:
            unit_root = r
            break
    if unit_root is not None:
        alpha = unit_root
        euler = (1 - 1/alpha)**2
        print(f"v_p(alpha) = {alpha.valuation()}, v_p((1-1/alpha)^2) = {euler.valuation()}")
        L_Om = Zp(1)/Zp(5)
        print(f"v_p(L(E,1)/Omega) = {L_Om.valuation()}")
        interp = euler * L_Om
        print(f"v_p(interpolation value) = {interp.valuation()}")
        if anomalous:
            print("  ==> interpolation valuation is POSITIVE because (1-1/alpha)^2 has v_p >= 2 in anomalous case")
    # What is the MCS verdict?
    verdict = "APPLIES" if (not anomalous and not reducible and surj) else "FAILS"
    print(f"MCS Theorem 3.4 verdict for (11a1, p={p}): {verdict}")

print()
print("=" * 70)
print("SHARP STATEMENT of the p=5 failure:")
print("=" * 70)
print("  11a1/p=5: Hypothesis 2.11(iii) FAILS (5 | |E(F_5)| = 5)")
print("            AND Hypothesis 2.17 FAILS (rho_bar REDUCIBLE at 5)")
print("            MCS Theorem 3.4 does not apply.")
print("  11a1/p=7: All hypotheses hold.")
print("            MCS Theorem 3.4 applies.")
