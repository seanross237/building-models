"""
Find curves with large |Sha| and compute dim Sha[p].
Key question: does dim Sha[p] ever exceed the CSS capacity bound?
"""

# Direct search using EllipticCurve from Cremona labels
print("Searching for curves with large |Sha| (rank 0)...")
print("="*60)

# Known curves with large Sha from the literature and LMFDB
# These are from various sources: Stein-Watkins, LMFDB tables
known_large_sha = [
    # |Sha| = 49
    '3364c1',
    # |Sha| = 81 
    # From Fisher's tables of curves with large Sha
    '11592h1', '12760e1',
    # |Sha| = 121
    '118006a1',
    # More candidates from literature searches
]

# Also scan a range
for N in range(5000, 20001):
    try:
        label = str(N) + 'a1'
        E = EllipticCurve(label)
        if E.analytic_rank() == 0:
            L1 = float(E.lseries()(1))
            omega_E = float(E.period_lattice().omega())
            S_primes = ZZ(N).prime_factors()
            tam = prod([E.tamagawa_number(p) for p in S_primes])
            tors_order = E.torsion_order()
            sha_an = L1 * tors_order**2 / (omega_E * tam)
            sha_int = int(round(sha_an))
            if sha_int >= 25:
                omega_N = len(S_primes)
                print(f"  {label}: |Sha|={sha_int}, omega(N)={omega_N}, N={N}")
                known_large_sha.append(label)
    except:
        pass

# Also try b1, c1 etc
for N in range(5000, 15001):
    for suffix in ['b1', 'c1', 'd1', 'e1']:
        try:
            label = str(N) + suffix
            E = EllipticCurve(label)
            if E.analytic_rank() == 0:
                L1 = float(E.lseries()(1))
                omega_E = float(E.period_lattice().omega())
                S_primes = ZZ(N).prime_factors()
                tam = prod([E.tamagawa_number(p) for p in S_primes])
                tors_order = E.torsion_order()
                sha_an = L1 * tors_order**2 / (omega_E * tam)
                sha_int = int(round(sha_an))
                if sha_int >= 25:
                    omega_N = len(S_primes)
                    print(f"  {label}: |Sha|={sha_int}, omega(N)={omega_N}, N={N}")
                    known_large_sha.append(label)
        except:
            pass

print(f"\nTotal curves with large |Sha| found: {len(known_large_sha)}")

# Now for each, analyze dim Sha[p] and CSS bound
print("\n" + "="*60)
print("DETAILED ANALYSIS: dim Sha[p] vs CSS CAPACITY BOUND")
print("="*60)

# Remove duplicates
known_large_sha = list(set(known_large_sha))

for label in sorted(known_large_sha):
    try:
        E = EllipticCurve(label)
        N = E.conductor()
        r = E.analytic_rank()
        omega_N = len(ZZ(N).prime_factors())
        S_primes = ZZ(N).prime_factors()
        tors = E.torsion_subgroup().invariants()
        
        if r == 0:
            L1 = float(E.lseries()(1))
            omega_E = float(E.period_lattice().omega())
            tam = prod([E.tamagawa_number(p) for p in S_primes])
            tors_order = E.torsion_order()
            sha_an = L1 * tors_order**2 / (omega_E * tam)
        else:
            sha_an = 1  # skip non-zero rank for now
        
        sha_int = int(round(sha_an))
        if sha_int < 4:
            continue
            
        print(f"\n{label}: N={N}, rank={r}, |Sha|={sha_int}, omega(N)={omega_N}")
        print(f"  S = {S_primes}, tors = {tors}")
        
        # 2-Selmer analysis
        try:
            sel_rank_2 = E.selmer_rank()
            dim_E2Q = len([d for d in tors if ZZ(d) % 2 == 0])
            dim_MW2 = r + dim_E2Q
            dim_sha2 = sel_rank_2 - dim_MW2
            print(f"  2-Selmer: rank={sel_rank_2}, dim Sha[2]={dim_sha2}")
        except:
            dim_sha2 = None
            print(f"  2-Selmer: computation failed")
        
        # For each prime p dividing |Sha|
        for p in ZZ(sha_int).prime_factors():
            p = ZZ(p)
            v_p = ZZ(sha_int).valuation(p)
            
            # The structure of Sha_p:
            # |Sha_p| = p^{v_p}. Since Cassels-Tate pairing is alternating,
            # Sha_p ~ (Z/p^{a_1})^2 x ... x (Z/p^{a_k})^2 with sum 2*a_i = v_p
            # So v_p is even, and dim_Fp Sha[p] = 2 * (number of cyclic factors) 
            # Minimum dim: 2 (if Sha_p ~ (Z/p^{v_p/2})^2)
            # Maximum dim: v_p (if Sha_p ~ (Z/p)^{v_p}, elementary abelian)
            
            # CSS capacity bound
            S_size = omega_N + 1
            n_est = 2 * S_size  # dim H^1(G_S, E[p]) estimate
            css_bound_val = float((1 - Integer(1)/p) * n_est)
            
            print(f"  p={p}: v_p(|Sha|)={v_p}, dim Sha[p] in [2, {v_p}]")
            print(f"    CSS bound: dim Sha[p] <= {css_bound_val:.1f}")
            
            # KEY: Is the CSS bound ever VIOLATED?
            # min dim Sha[p] = 2 (always satisfied by CSS bound for our curves)
            # max dim Sha[p] = v_p
            # Violation iff v_p > css_bound_val
            if v_p > css_bound_val:
                print(f"    *** CSS BOUND COULD BE VIOLATED if Sha is elementary abelian ***")
            elif 2 > css_bound_val:
                print(f"    *** CSS BOUND VIOLATED even for minimal dim ***")
            else:
                print(f"    CSS bound NOT violated (max possible {v_p} <= {css_bound_val:.1f})")
    except Exception as ex:
        print(f"\n{label}: ERROR - {type(ex).__name__}: {ex}")

