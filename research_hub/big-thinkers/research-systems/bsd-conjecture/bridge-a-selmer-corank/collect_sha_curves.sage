"""
Collect elliptic curves with non-trivial Sha from the Cremona database.
These are critical for testing whether moments distinguish Sha from rank.
"""
import json
from collections import Counter

# We need curves with Sha > 1
# These are relatively rare: most rank-0 curves have Sha=1
# Strategy: scan larger conductor range, only keep curves with Sha > 1 or interesting Selmer

results = []
db = CremonaDatabase()

sha_counts = Counter()
count = 0
sha_target = 100  # we want at least 100 nontrivial Sha curves

# Also collect matched controls
controls = []

for N in range(1, 200001):
    try:
        curves = db.allcurves(N)
    except Exception:
        continue

    for label_suffix, data_raw in curves.items():
        label = f"{N}{label_suffix}"
        try:
            ainvs = data_raw[0] if isinstance(data_raw, (list, tuple)) else data_raw
            E = EllipticCurve(ainvs)

            rank = E.rank()

            # Only check Sha for rank 0 curves (where Sha is most often nontrivial)
            # and a few rank 1/2 curves
            if rank > 2:
                continue

            sha_an = float(E.sha().an())
            sha_rounded = round(sha_an)

            if sha_rounded > 1:
                # This is a nontrivial Sha curve!
                sel2 = E.selmer_rank()
                tors = [int(x) for x in E.torsion_subgroup().invariants()]
                tors2_rk = sum(1 for t in tors if t % 2 == 0)

                # Compute a_p for 50 primes
                primes_list = list(primes(300))[:50]
                ap_data = {}
                for p in primes_list:
                    if N % int(p) != 0:
                        ap_data[str(int(p))] = int(E.ap(p))

                M1 = sum(a / float(int(p)) for p, a in ap_data.items() for a in [int(ap_data[p])] for p in [int(p)])
                # Fix: compute properly
                good_ap = [(int(p), int(a)) for p, a in ap_data.items()]
                M1 = sum(a/float(p) for p, a in good_ap)
                M2 = sum(a**2/float(p)**2 for p, a in good_ap)
                murm = sum(a * float(p)**(-0.84) for p, a in good_ap)

                entry = {
                    'label': label,
                    'conductor': int(N),
                    'rank': int(rank),
                    'sel2_rank': int(sel2),
                    'sha_an': sha_rounded,
                    'torsion_order': int(E.torsion_order()),
                    'torsion_2_rank': tors2_rk,
                    'sha2_dim': int(sel2) - int(rank) - tors2_rk,
                    'M1': round(float(M1), 8),
                    'M2': round(float(M2), 8),
                    'murm_sum': round(float(murm), 6),
                    'n_good_primes': len(good_ap),
                }
                results.append(entry)
                sha_counts[sha_rounded] += 1
                count += 1

                if count % 20 == 0:
                    print(f"  Found {count} nontrivial Sha curves (N<={N})")
                    print(f"  Distribution: {dict(sorted(sha_counts.items()))}")

        except Exception as e:
            pass

    if count >= sha_target:
        break

print(f"\nDone: {count} nontrivial Sha curves found")
print(f"Sha distribution: {dict(sorted(sha_counts.items()))}")

# Distribution by rank
rank_dist = Counter(e['rank'] for e in results)
print(f"Rank distribution: {dict(sorted(rank_dist.items()))}")

# Cross-tabulate
for r in sorted(set(e['rank'] for e in results)):
    subset = [e for e in results if e['rank'] == r]
    sha_d = Counter(e['sha_an'] for e in subset)
    sel2_d = Counter(e['sel2_rank'] for e in subset)
    print(f"\n  rank={r} (n={len(subset)}):")
    print(f"    Sha: {dict(sorted(sha_d.items()))}")
    print(f"    sel2: {dict(sorted(sel2_d.items()))}")

# Key test: within same sel2 and tors2_rk, do moments differ by sha value?
print("\n\nMoment comparison by Sha value (within rank=0):")
for sha in sorted(sha_counts.keys()):
    subset = [e for e in results if e['rank'] == 0 and e['sha_an'] == sha]
    if subset:
        print(f"  Sha={sha} (n={len(subset)}): M1={sum(e['M1'] for e in subset)/len(subset):+.4f} "
              f"M2={sum(e['M2'] for e in subset)/len(subset):.4f} "
              f"murm={sum(e['murm_sum'] for e in subset)/len(subset):+.3f}")

# Save
output_path = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/bridge-a-selmer-corank/sha_curves.json"
with open(output_path, 'w') as f:
    json.dump(results, f, indent=1)
print(f"\nSaved to {output_path}")
