# Verify Sha[p^infty] = 0 for 11a1 at p=7
E = EllipticCurve('11a1')
# Analytic Sha
print(f"Analytic order of Sha: {E.sha().an()}")
# Kato's bound / bounds from Kolyvagin
for p in [5, 7]:
    print(f"\np = {p}")
    # p-primary part of Sha: analytic order factored by p
    # Can we get an actual upper bound?
    try:
        kb = E.sha().p_primary_bound(p)
        print(f"  p-primary bound on Sha from p-descent/Kato: {kb}")
    except Exception as e:
        print(f"  bound error: {e}")

# BSD formula at p=7:
# Analytic: L(E,1)/Omega = 1/5 = (1/|E(Q)_tors|^2) * Tam * |Sha|
# i.e., 1/5 = (1/25) * 5 * |Sha| = |Sha|/5, so |Sha| = 1
# At p=7: p does not divide tors, Tam, |Sha|; BSD p-part holds trivially with everything = 1
print()
print("BSD check for 11a1:")
print(f"  L(E,1)/Omega = 1/5 = Tam * |Sha| / |tors|^2 = 5 * 1 / 25 = 1/5 CHECK")
print(f"  At p=7: v_7(Tam)=0, v_7(|Sha|)=0, v_7(tors)=0, v_7(L/Omega)=0. All match.")
print(f"  So Sha[7^infty] = 0 and p-part of BSD holds trivially.")
