"""
Phase 2: Compute Sha[p] dimensions and code parameters.
Use analytic_sha() which doesn't need generators.
"""

# Use curves from previous approach-4-qec analysis (known to work)
test_curves = [
    # (label, rank, sha_an, omega_N) -- from prior findings
    ('571b1', 0, 4, None),      # Note: might be 571a1 
    ('960d1', 0, 4, None),
    ('681b1', 0, 9, None),
    ('1913b1', 0, 9, None),
    ('2366d1', 0, 9, None),
    ('2534e1', 0, 9, None),
    ('2534f1', 0, 9, None),
    ('2849a1', 0, 9, None),
    ('3054a1', 0, 9, None),
    ('3364c1', 0, 49, None),
    ('3712j1', 0, 9, None),
    ('4229a1', 0, 9, None),
    ('1058d1', 0, 25, None),
    ('1246b1', 0, 25, None),
]

print("="*80)
print("PART 1: VERIFYING SHA[p] DIMENSIONS FROM PRIOR WORK")
print("="*80)

results = []
for label, expected_rank, expected_sha, _ in test_curves:
    try:
        E = EllipticCurve(label)
        N = E.conductor()
        omega_N = len(ZZ(N).prime_factors())
        S_primes = ZZ(N).prime_factors()
        
        # Use analytic rank and analytic sha
        r_an = E.analytic_rank()
        
        # For rank 0 curves, sha can be computed without generators
        if r_an == 0:
            L_val = E.lseries().L1_vanishes()  # check L(1) != 0
            # sha = L(E,1) * |E_tors|^2 / (Omega * prod c_p)
            L1 = float(E.lseries()(1))
            omega_E = float(E.period_lattice().omega())
            tam = prod([E.tamagawa_number(p) for p in S_primes])
            tors_order = E.torsion_order()
            sha_an = float(L1 * tors_order^2 / (omega_E * tam))
        else:
            sha_an = expected_sha  # trust the prior computation
        
        sha_int = int(round(sha_an))
        
        # Selmer rank computation (2-Selmer)
        try:
            sel_rank_2 = E.selmer_rank()
        except:
            sel_rank_2 = None
        
        # Torsion structure
        tors_invs = E.torsion_subgroup().invariants()
        
        print(f"\n{label}: N={N}, r_an={r_an}, |Sha|={sha_int}, omega(N)={omega_N}")
        print(f"  S = {S_primes}, tors = {tors_invs}")
        
        if sel_rank_2 is not None:
            dim_E2Q = len([d for d in tors_invs if ZZ(d) % 2 == 0])
            dim_MW2 = r_an + dim_E2Q
            dim_sha2 = sel_rank_2 - dim_MW2
            print(f"  2-Selmer rank = {sel_rank_2}, dim E(Q)/2E(Q) = {dim_MW2}, dim Sha[2] = {dim_sha2}")
        
        # For each p | |Sha|
        if sha_int > 1:
            for p in ZZ(sha_int).prime_factors():
                p = ZZ(p)
                # v_p(|Sha|)
                v_p = ZZ(sha_int).valuation(p)
                # dim Sha[p] is between 2 (cyclic^2) and v_p (elementary abelian)
                # For rank 0, we know from Cassels that Sha has a non-degenerate alternating pairing,
                # so dim_Fp Sha[p] is EVEN
                print(f"  p={p}: v_p(|Sha|) = {v_p}")
                print(f"    dim Sha[p] in {{2, 4, ..., {v_p}}} (even, >= 2 if v_p >= 2)")
                
                # CSS bound
                S_size = omega_N + 1  # bad primes + p
                n_est = 2 * S_size
                css_bound = float((1 - Integer(1)/p) * n_est)
                print(f"    CSS bound: dim Sha[p] <= (1-1/{p}) * {n_est} = {css_bound:.1f}")
                print(f"    Is CSS bound useful? dim Sha[p] <= {css_bound:.1f} vs max possible {v_p}")
        
        results.append((label, N, r_an, sha_int, omega_N, sel_rank_2))
        
    except Exception as ex:
        print(f"\n{label}: ERROR - {ex}")

print("\n" + "="*80)
print("PART 2: SYSTEMATIC SEARCH FOR LARGE |Sha|")
print("="*80)

# Search Cremona database
large_sha_curves = []
print("\nScanning Cremona database for curves with large |Sha|...")

# Use cremona_optimal_curves which iterates by conductor
from sage.databases.cremona import CremonaDatabase
C = CremonaDatabase()

for N in range(1, 30001):
    try:
        data = C.allcurves(N)
        for iso_label, curve_data in data.items():
            # curve_data is a dict with keys like 'ainvs', 'rank', etc.
            if isinstance(curve_data, dict):
                r = curve_data.get('rank', None)
                if r is not None and r == 0:
                    # For rank 0 curves, compute sha analytically
                    ainvs = curve_data.get('ainvs', None)
                    if ainvs:
                        E = EllipticCurve(list(ainvs))
                        try:
                            L1 = float(E.lseries()(1))
                            omega_E = float(E.period_lattice().omega())
                            S_primes_N = ZZ(N).prime_factors()
                            tam = prod([E.tamagawa_number(p) for p in S_primes_N])
                            tors_order = E.torsion_order()
                            sha_an = L1 * tors_order**2 / (omega_E * tam)
                            sha_int = int(round(sha_an))
                            if sha_int >= 36:
                                omega_N = len(S_primes_N)
                                label_full = str(N) + iso_label
                                large_sha_curves.append((label_full, N, 0, omega_N, sha_int))
                        except:
                            pass
    except:
        pass

large_sha_curves.sort(key=lambda x: -x[4])
print(f"\nFound {len(large_sha_curves)} rank-0 curves with |Sha| >= 36:")
for label, N, r, omega, sha_int in large_sha_curves[:30]:
    print(f"  {label}: N={N}, omega(N)={omega}, |Sha|={sha_int}")
