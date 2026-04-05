"""
Add 2-Selmer rank to the existing 1201-curve dataset.
Also compute more Frobenius moments using the available a_p data.
"""
import json
from collections import Counter

# Load existing data
with open("/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/approach-1-ml/data/bsd_invariants.json") as f:
    data = json.load(f)

print(f"Loaded {len(data)} curves")

enriched = []
errors = 0

for i, entry in enumerate(data):
    ainvs = entry['ainvs']
    try:
        E = EllipticCurve(ainvs)

        # 2-Selmer rank
        sel2 = E.selmer_rank()  # dim_F2(Sel_2(E))

        # 3-Selmer rank (if feasible)
        try:
            sel3 = E.three_selmer_rank()
        except Exception:
            sel3 = -1

        # Compute moments from existing a_p data
        ap_dict = entry['a_p']
        conductor = entry['conductor']

        # Filter good primes
        good_ap = [(int(p), int(a)) for p, a in ap_dict.items() if int(conductor) % int(p) != 0]
        good_ap.sort()

        if len(good_ap) < 10:
            continue

        # First moment: sum a_p/p
        M1 = sum(a/float(p) for p, a in good_ap)
        # Second moment: sum a_p^2/p^2
        M2 = sum(a**2/float(p)**2 for p, a in good_ap)
        # Third moment: sum a_p^3/p^3
        M3 = sum(a**3/float(p)**3 for p, a in good_ap)
        # Fourth moment: sum a_p^4/p^4
        M4 = sum(a**4/float(p)**4 for p, a in good_ap)

        # Symmetric square sum: sum (a_p^2 - p)/p^2
        sym2 = sum((a**2 - float(p))/float(p)**2 for p, a in good_ap)

        # Mean a_p^2/p for small primes (p <= 23)
        small = [(p, a) for p, a in good_ap if p <= 23]
        mean_ap2_p_small = sum(a**2/float(p) for p, a in small)/len(small) if small else 0

        # Variance of a_p/(2*sqrt(p))
        normalized = [a/(2*float(p)**0.5) for p, a in good_ap]
        mean_norm = sum(normalized)/len(normalized)
        var_norm = sum((x - mean_norm)**2 for x in normalized)/len(normalized)

        # Murmuration sum
        murm = sum(a * float(p)**(-0.84) for p, a in good_ap)

        # Running coupling (partial Euler product)
        log_L = 0.0
        for p, a in good_ap:
            ef = 1.0 - float(a)/float(p) + 1.0/float(p)
            if ef > 0:
                log_L -= log(ef)
            else:
                log_L -= log(abs(ef))
        Lambda = good_ap[-1][0]
        g_Lambda = log_L / log(float(Lambda))

        # Frequency of a_p even
        freq_even = sum(1 for p, a in good_ap if a % 2 == 0) / len(good_ap)

        enriched_entry = dict(entry)
        enriched_entry['sel2_rank'] = int(sel2)
        enriched_entry['sel3_rank'] = int(sel3)
        enriched_entry['M1'] = round(float(M1), 8)
        enriched_entry['M2'] = round(float(M2), 8)
        enriched_entry['M3'] = round(float(M3), 8)
        enriched_entry['M4'] = round(float(M4), 8)
        enriched_entry['sym2_sum'] = round(float(sym2), 8)
        enriched_entry['mean_ap2_p_small'] = round(float(mean_ap2_p_small), 6)
        enriched_entry['var_normalized'] = round(float(var_norm), 8)
        enriched_entry['murm_sum'] = round(float(murm), 6)
        enriched_entry['g_Lambda'] = round(float(g_Lambda), 8)
        enriched_entry['freq_ap_even'] = round(float(freq_even), 6)
        enriched_entry['n_good_primes'] = len(good_ap)
        enriched.append(enriched_entry)

    except Exception as e:
        errors += 1
        if errors <= 5:
            print(f"  Error on {entry['label']}: {e}")

    if (i+1) % 200 == 0:
        print(f"  Processed {i+1}/{len(data)}")

print(f"\nDone: {len(enriched)} curves enriched, {errors} errors")
print(f"Rank distribution: {dict(sorted(Counter(e['rank'] for e in enriched).items()))}")
print(f"Sel2 rank distribution: {dict(sorted(Counter(e['sel2_rank'] for e in enriched).items()))}")
print(f"Sel3 rank distribution: {dict(sorted(Counter(e['sel3_rank'] for e in enriched).items()))}")

# Cross-tabulate rank x sel2
print("\nRank x Sel2 cross-tabulation:")
for r in sorted(set(e['rank'] for e in enriched)):
    subset = [e for e in enriched if e['rank'] == r]
    sel2_dist = Counter(e['sel2_rank'] for e in subset)
    print(f"  rank={r}: {dict(sorted(sel2_dist.items()))}")

# Sha distribution by rank x sel2
print("\nSha distribution by rank x sel2:")
for r in sorted(set(e['rank'] for e in enriched)):
    for s in sorted(set(e['sel2_rank'] for e in enriched)):
        subset = [e for e in enriched if e['rank'] == r and e['sel2_rank'] == s]
        if subset:
            sha_dist = Counter(round(e['analytic_sha']) for e in subset)
            if len(sha_dist) > 1 or list(sha_dist.keys()) != [1]:
                print(f"  rank={r}, sel2={s}: {dict(sorted(sha_dist.items()))}")

# Convert Sage types to Python native for JSON
def sage_to_python(obj):
    if isinstance(obj, dict):
        return {str(k): sage_to_python(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [sage_to_python(v) for v in obj]
    elif hasattr(obj, 'parent') and hasattr(obj, '__float__'):
        return float(obj)
    elif hasattr(obj, 'parent') and hasattr(obj, '__int__'):
        return int(obj)
    else:
        return obj

# Save
output_path = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/bridge-a-selmer-corank/enriched_data.json"
clean = [sage_to_python(e) for e in enriched]
with open(output_path, 'w') as f:
    json.dump(clean, f, indent=1)
print(f"\nSaved to {output_path}")
