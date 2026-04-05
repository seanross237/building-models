#!/usr/bin/env sage
"""
Targeted dataset generation: get rank >= 2 curves with extended primes.
Uses iter_optimal for faster database scanning.
"""

from sage.all import *
import json, os, math, time

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
prime_bound = 499
primes_list = list(prime_range(2, prime_bound + 1))
print(f"Using {len(primes_list)} primes (up to {primes_list[-1]})")

start = time.time()

# Strategy: use list_optimal which is faster
db = CremonaDatabase()

# Get ALL rank-2 curves
print("Finding rank >= 2 curves...")
rank2_curves = []
rank3_curves = []

# Use the database's iter method
for E in db.iter_optimal(range(1, 10000)):
    r = int(E.rank())
    if r == 2:
        rank2_curves.append(E)
    elif r >= 3:
        rank3_curves.append(E)

print(f"Found {len(rank2_curves)} rank-2, {len(rank3_curves)} rank-3+ ({time.time()-start:.1f}s)")

# Sample rank 0 and 1
print("Finding rank 0, 1 curves...")
rank0_curves = []
rank1_curves = []
count = 0
for E in db.iter_optimal(range(1, 10000)):
    r = int(E.rank())
    count += 1
    if r == 0 and len(rank0_curves) < 300:
        rank0_curves.append(E)
    elif r == 1 and len(rank1_curves) < 300:
        rank1_curves.append(E)
    if len(rank0_curves) >= 300 and len(rank1_curves) >= 300:
        break

print(f"Sampled {len(rank0_curves)} rank-0, {len(rank1_curves)} rank-1 ({time.time()-start:.1f}s)")

# Compute invariants
dataset = []
total = 0
sha_count = 0

all_selected = [(0, rank0_curves), (1, rank1_curves), (2, rank2_curves), (3, rank3_curves)]
for rank, curve_list in all_selected:
    print(f"\nComputing rank {rank} ({len(curve_list)} curves)...")
    for E in curve_list:
        try:
            N = int(E.conductor())
            omega = float(E.real_components() * abs(E.period_lattice().basis()[0].real()))
            reg = float(E.regulator()) if rank > 0 else 1.0
            tam = int(E.tamagawa_product())
            tors = int(E.torsion_order())
            try:
                sha = float(E.sha().an_numerical())
            except:
                sha = 1.0

            if abs(sha - 1.0) > 0.01:
                sha_count += 1

            a_p = {}
            for p in primes_list:
                a_p[str(int(p))] = int(E.ap(p))

            # Partial L-values
            log_L_97 = 0.0
            log_L_499 = 0.0
            sum_ap_p = 0.0
            murm = 0.0

            for idx, p in enumerate(primes_list):
                ap = int(a_p[str(int(p))])
                is_bad = (N % int(p) == 0)
                if not is_bad:
                    sum_ap_p += float(ap) / float(p)
                if idx < 25 and not is_bad:
                    murm += float(ap) * float(p)**(-0.84)

                d = (1 - float(ap)/float(p)) if is_bad else (1 - float(ap)/float(p) + 1.0/float(p))
                if abs(d) > 1e-50:
                    lc = -math.log(abs(d))
                    log_L_499 += lc
                    if int(p) <= 97:
                        log_L_97 += lc

            entry = {
                'label': str(E.cremona_label()),
                'conductor': int(N),
                'rank': int(rank),
                'torsion_order': int(tors),
                'tamagawa_product': int(tam),
                'real_period': float(omega),
                'regulator': float(reg),
                'analytic_sha': float(sha),
                'a_p': a_p,
                'sum_ap_over_p': float(sum_ap_p),
                'murmuration_sum_084': float(murm),
                'log_L_partial_97': float(log_L_97),
                'log_L_partial_499': float(log_L_499),
                'ainvs': [int(x) for x in E.ainvs()],
            }
            dataset.append(entry)
            total += 1

            if total % 100 == 0:
                print(f"  {total} done ({time.time()-start:.1f}s)")

        except Exception as e:
            continue

print(f"\n{'='*60}")
print(f"COMPLETE: {len(dataset)} curves, Sha>1: {sha_count}")
rank_counts = {}
for c in dataset:
    r = c['rank']
    rank_counts[r] = rank_counts.get(r, 0) + 1
print(f"By rank: {rank_counts}")
print(f"Time: {time.time()-start:.1f}s")

# Save
outpath = os.path.join(OUTPUT_DIR, 'extended_dataset.json')
with open(outpath, 'w') as f:
    json.dump(dataset, f)
print(f"Saved to {outpath} ({os.path.getsize(outpath)} bytes)")

sumpath = os.path.join(OUTPUT_DIR, 'extended_dataset_summary.json')
with open(sumpath, 'w') as f:
    json.dump({
        'total_curves': len(dataset),
        'by_rank': {str(k): v for k, v in rank_counts.items()},
        'sha_gt1': sha_count,
        'conductor_range': [int(min(c['conductor'] for c in dataset)), int(max(c['conductor'] for c in dataset))],
        'primes_available': len(primes_list),
        'max_prime': int(primes_list[-1]),
    }, f, indent=2)

# Print Sha > 1 curves
sha_crvs = [c for c in dataset if abs(c['analytic_sha'] - 1.0) > 0.01]
if sha_crvs:
    print(f"\nSha > 1 curves:")
    for c in sha_crvs[:30]:
        print(f"  {c['label']}: rank={c['rank']}, N={c['conductor']}, Sha={c['analytic_sha']:.4f}")
