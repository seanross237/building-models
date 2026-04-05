#!/usr/bin/env sage
"""
Phase 2: Generate extended dataset with SageMath.
Uses the full Cremona mini database (conductors up to 9999)
with more primes (up to p=997) and all BSD invariants.
"""

from sage.all import *
import json
import os
import sys
import time
import math
import random as pyrandom

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
pyrandom.seed(int(42))


def generate_extended_dataset():
    print("=" * 70)
    print("GENERATING EXTENDED DATASET")
    print("=" * 70)

    db = CremonaDatabase()
    max_N = int(db.largest_conductor())
    print(f"Cremona DB conductor range: {db.smallest_conductor()} - {max_N}")

    curves_by_rank = {0: [], 1: [], 2: [], 3: [], 4: []}
    start = time.time()

    # Scan ALL conductors in the database
    for N in range(1, max_N + 1):
        try:
            class_data = db.allcurves(N)
            if not class_data:
                continue
            for label_suffix, cdata in class_data.items():
                ainvs = cdata[0]
                rank = int(cdata[1])
                if rank < 0 or rank > 4:
                    continue
                full_label = str(N) + label_suffix
                curves_by_rank[rank].append((full_label, ainvs, rank))
        except Exception:
            continue

        if N % 2000 == 0:
            counts = {r: len(v) for r, v in curves_by_rank.items()}
            print(f"  N={N}: {counts} ({time.time()-start:.1f}s)")

    print(f"\nAll curves found:")
    for rank, items in curves_by_rank.items():
        print(f"  Rank {rank}: {len(items)}")

    # Subsample rank 0 to 500, rank 1 to 500, keep all rank >= 2
    for rank in [0, 1]:
        if len(curves_by_rank[rank]) > 500:
            curves_by_rank[rank] = pyrandom.sample(curves_by_rank[rank], int(500))

    print(f"\nSelected for analysis:")
    for rank, items in curves_by_rank.items():
        print(f"  Rank {rank}: {len(items)}")

    # Compute invariants with EXTENDED primes (up to 997)
    prime_bound = 997
    primes_list = list(prime_range(2, prime_bound + 1))
    print(f"\nComputing invariants (a_p for {len(primes_list)} primes, up to p={prime_bound})...")

    dataset = []
    computed = 0
    sha_gt1_count = 0

    for rank in sorted(curves_by_rank.keys()):
        for full_label, ainvs, r in curves_by_rank[rank]:
            try:
                E = EllipticCurve(ainvs)
                N = int(E.conductor())

                omega = float(E.real_components() * abs(E.period_lattice().basis()[0].real()))
                reg = float(E.regulator()) if r > 0 else 1.0
                tam = int(E.tamagawa_product())
                tors = int(E.torsion_order())

                try:
                    sha_an = float(E.sha().an_numerical())
                except:
                    sha_an = 1.0

                if abs(sha_an - 1.0) > 0.01:
                    sha_gt1_count += 1

                # a_p for ALL primes up to 997
                a_p = {}
                for p in primes_list:
                    a_p[str(p)] = int(E.ap(p))

                # Derived: sum a_p/p (all primes), murmuration, log L
                sum_ap_p = 0.0
                murm = 0.0
                log_L_97 = 0.0
                log_L_997 = 0.0

                for idx, p in enumerate(primes_list):
                    ap = a_p[str(p)]
                    is_bad = (N % p == 0)
                    if not is_bad:
                        sum_ap_p += float(ap) / p
                    if idx < 25 and not is_bad:
                        murm += float(ap) * float(p)**(-0.84)

                    denom = (1 - float(ap)/p) if is_bad else (1 - float(ap)/p + 1.0/p)
                    if abs(denom) > 1e-50:
                        log_contrib = -math.log(abs(denom))
                        log_L_997 += log_contrib
                        if p <= 97:
                            log_L_97 += log_contrib

                entry = {
                    'label': full_label,
                    'conductor': N,
                    'rank': r,
                    'torsion_order': tors,
                    'tamagawa_product': tam,
                    'real_period': omega,
                    'regulator': reg,
                    'analytic_sha': sha_an,
                    'a_p': a_p,
                    'sum_ap_over_p_997': sum_ap_p,
                    'murmuration_sum_084': murm,
                    'log_L_partial_97': log_L_97,
                    'log_L_partial_997': log_L_997,
                    'ainvs': [int(x) for x in E.ainvs()],
                }
                dataset.append(entry)
                computed += 1

                if computed % 100 == 0:
                    print(f"  Computed {computed} ({time.time()-start:.1f}s, Sha>1: {sha_gt1_count})")

            except Exception as e:
                continue

    print(f"\nDataset: {len(dataset)} curves")
    rank_counts = {}
    for c in dataset:
        r = c['rank']
        rank_counts[r] = rank_counts.get(r, 0) + 1
    print(f"By rank: {rank_counts}")
    print(f"Sha > 1: {sha_gt1_count}")

    sha_curves = [c for c in dataset if abs(c['analytic_sha'] - 1) > 0.01]
    for c in sha_curves[:20]:
        print(f"  Sha: {c['label']}, rank={c['rank']}, Sha={c['analytic_sha']:.4f}, N={c['conductor']}")

    output_path = os.path.join(OUTPUT_DIR, 'extended_dataset.json')
    with open(output_path, 'w') as f:
        json.dump(dataset, f)
    print(f"\nSaved to {output_path} ({os.path.getsize(output_path)} bytes)")

    if dataset:
        summary = {
            'total_curves': len(dataset),
            'by_rank': rank_counts,
            'sha_gt1': sha_gt1_count,
            'conductor_range': [min(c['conductor'] for c in dataset), max(c['conductor'] for c in dataset)],
            'primes_available': len(primes_list),
            'max_prime': int(primes_list[-1]),
        }
        with open(os.path.join(OUTPUT_DIR, 'extended_dataset_summary.json'), 'w') as f:
            json.dump(summary, f, indent=2)

    return dataset


if __name__ == '__main__':
    generate_extended_dataset()
