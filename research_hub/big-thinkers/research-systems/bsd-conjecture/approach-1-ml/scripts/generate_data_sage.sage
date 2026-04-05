"""
Generate BSD invariant dataset using SageMath's Cremona database.
Uses MiniCremonaDatabase (conductors up to 10000) + direct computation for higher conductors.
"""
import json
import sys
from collections import Counter

results = []
rank_counts = Counter()
target_by_rank = {0: 500, 1: 500, 2: 150, 3: 30}

print("Generating elliptic curve BSD invariant dataset via SageMath...")

# Phase 1: Use Cremona database for conductors up to 10000
db = CremonaDatabase()
max_N = 10000

for N in range(1, max_N + 1):
    try:
        curves = db.allcurves(N)
    except Exception:
        continue

    if not curves:
        continue

    for label_suffix, data in curves.items():
        ainvs_raw, stored_rank, stored_torsion = data
        r = int(stored_rank)

        # Skip if we have enough of this rank
        if rank_counts.get(r, 0) >= target_by_rank.get(r, 1000):
            continue

        try:
            full_label = str(N) + label_suffix
            E = EllipticCurve(ainvs_raw)

            # Compute BSD invariants
            disc = E.discriminant()
            j = E.j_invariant()
            tors_order = int(E.torsion_order())
            tors_structure = [int(x) for x in E.torsion_subgroup().invariants()]

            # Tamagawa numbers
            tam_product = int(E.tamagawa_product())
            tam_numbers = {}
            for p in Integer(N).prime_factors():
                tam_numbers[str(p)] = int(E.tamagawa_number(p))

            # Real period
            omega = float(E.period_lattice().omega())

            # Regulator
            if r > 0:
                try:
                    reg = float(E.regulator())
                except Exception:
                    reg = None
            else:
                reg = 1.0

            # Analytic order of Sha
            try:
                sha_an = float(E.sha().an_numerical())
            except Exception:
                sha_an = None

            # Frobenius traces a_p for small primes
            small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                           53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
            a_p = {}
            for p in small_primes:
                a_p[str(p)] = int(E.ap(p))

            # Weierstrass coefficients
            ainvs_list = [int(a) for a in E.ainvs()]

            # Additional invariants
            c4 = int(E.c4())
            c6 = int(E.c6())

            # Reduction types at bad primes
            reduction_types = {}
            for p in Integer(N).prime_factors():
                if E.has_split_multiplicative_reduction(p):
                    reduction_types[str(p)] = "split_mult"
                elif E.has_nonsplit_multiplicative_reduction(p):
                    reduction_types[str(p)] = "nonsplit_mult"
                elif E.has_additive_reduction(p):
                    reduction_types[str(p)] = "additive"
                else:
                    reduction_types[str(p)] = "good"

            # L-function special value at s=1
            try:
                Lval = float(E.lseries().L1_vanishing()[1])
            except Exception:
                Lval = None

            # Modular degree
            try:
                mod_deg = int(E.modular_degree())
            except Exception:
                mod_deg = None

            # Isogeny class size
            try:
                isog_size = len(E.isogeny_class().curves)
            except Exception:
                isog_size = None

            entry = {
                'label': full_label,
                'conductor': int(N),
                'rank': r,
                'discriminant': int(disc),
                'j_invariant': str(j),
                'j_invariant_float': float(j) if j in QQ else None,
                'torsion_order': tors_order,
                'torsion_structure': tors_structure,
                'tamagawa_product': tam_product,
                'tamagawa_numbers': tam_numbers,
                'real_period': omega,
                'regulator': reg,
                'analytic_sha': sha_an,
                'L_value': Lval,
                'modular_degree': mod_deg,
                'isogeny_class_size': isog_size,
                'a_p': a_p,
                'ainvs': ainvs_list,
                'c4': c4,
                'c6': c6,
                'reduction_types': reduction_types,
                'num_bad_primes': len(Integer(N).prime_factors()),
                'conductor_factored': [[int(p), int(e)] for p, e in Integer(N).factor()],
                'log_conductor': float(log(N)),
            }
            results.append(entry)
            rank_counts[r] += 1

        except Exception as e:
            pass

    if N % 500 == 0:
        print(f"  Conductor {N}: {dict(sorted(rank_counts.items()))} ({len(results)} total)")

print(f"\nPhase 1 complete: {len(results)} curves from Cremona DB")
print(f"Rank distribution: {dict(sorted(rank_counts.items()))}")

# Phase 2: Generate specific high-rank curves manually
# Known rank 2 curves
print("\nPhase 2: Adding known higher-rank curves...")

high_rank_curves = [
    # rank 2
    '389a1', '433a1', '446d1', '563a1', '571b1', '643a1', '655a1',
    '664a1', '681c1', '707a1', '709a1', '718b1',
    '794a1', '817a1', '916c1', '944e1', '997b1', '997c1',
    # rank 3
    '5077a1',
    # More rank 2
    '1058d1', '1077a1', '1082a1', '1094a1', '1102a1', '1134e1',
    '1147a1', '1171a1', '1187a1', '1190b1', '1206e1', '1229a1',
    '1246b1', '1283a1', '1291a1', '1309a1', '1325a1', '1339a1',
    '1342a1', '1346a1', '1355a1', '1357c1', '1363a1', '1373a1',
    '1399a1', '1423a1', '1429a1', '1439a1', '1446a1', '1451a1',
]

for label in high_rank_curves:
    try:
        E = EllipticCurve(label)
        r = E.rank()
        N = int(E.conductor())

        if rank_counts.get(r, 0) >= target_by_rank.get(r, 1000):
            continue

        # Check if already in dataset
        if any(e['label'] == label for e in results):
            continue

        disc = E.discriminant()
        j = E.j_invariant()
        tors_order = int(E.torsion_order())
        tors_structure = [int(x) for x in E.torsion_subgroup().invariants()]
        tam_product = int(E.tamagawa_product())
        tam_numbers = {}
        for p in Integer(N).prime_factors():
            tam_numbers[str(p)] = int(E.tamagawa_number(p))
        omega = float(E.period_lattice().omega())
        reg = float(E.regulator()) if r > 0 else 1.0
        try:
            sha_an = float(E.sha().an_numerical())
        except:
            sha_an = None
        small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                       53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        a_p = {}
        for p in small_primes:
            a_p[str(p)] = int(E.ap(p))
        ainvs_list = [int(a) for a in E.ainvs()]
        c4 = int(E.c4())
        c6 = int(E.c6())
        reduction_types = {}
        for p in Integer(N).prime_factors():
            if E.has_split_multiplicative_reduction(p):
                reduction_types[str(p)] = "split_mult"
            elif E.has_nonsplit_multiplicative_reduction(p):
                reduction_types[str(p)] = "nonsplit_mult"
            elif E.has_additive_reduction(p):
                reduction_types[str(p)] = "additive"
            else:
                reduction_types[str(p)] = "good"
        try:
            Lval = float(E.lseries().L1_vanishing()[1])
        except:
            Lval = None
        try:
            mod_deg = int(E.modular_degree())
        except:
            mod_deg = None
        try:
            isog_size = len(E.isogeny_class().curves)
        except:
            isog_size = None

        entry = {
            'label': label,
            'conductor': int(N),
            'rank': r,
            'discriminant': int(disc),
            'j_invariant': str(j),
            'j_invariant_float': float(j) if j in QQ else None,
            'torsion_order': tors_order,
            'torsion_structure': tors_structure,
            'tamagawa_product': tam_product,
            'tamagawa_numbers': tam_numbers,
            'real_period': omega,
            'regulator': reg,
            'analytic_sha': sha_an,
            'L_value': Lval,
            'modular_degree': mod_deg,
            'isogeny_class_size': isog_size,
            'a_p': a_p,
            'ainvs': ainvs_list,
            'c4': c4,
            'c6': c6,
            'reduction_types': reduction_types,
            'num_bad_primes': len(Integer(N).prime_factors()),
            'conductor_factored': [[int(p), int(e)] for p, e in Integer(N).factor()],
            'log_conductor': float(log(N)),
        }
        results.append(entry)
        rank_counts[r] += 1
        print(f"  Added {label} (rank {r})")
    except Exception as e:
        print(f"  Failed {label}: {e}")

print(f"\nFinal dataset: {len(results)} curves")
print(f"Rank distribution: {dict(sorted(rank_counts.items()))}")

# Save
outpath = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/approach-1-ml/data/bsd_invariants.json"
with open(outpath, 'w') as f:
    json.dump(results, f, indent=2)
print(f"Saved to {outpath}")
