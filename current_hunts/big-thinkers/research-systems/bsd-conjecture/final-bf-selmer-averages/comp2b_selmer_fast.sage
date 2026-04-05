"""
Fast computation of p-Selmer averages over Cremona database.
"""
from sage.databases.cremona import CremonaDatabase
import time

DB = CremonaDatabase()

print("="*70)
print("p-SELMER AVERAGES OVER CREMONA DATABASE")
print("="*70)

# Collect curve data efficiently
max_N = 3000
curve_data = []
t0 = time.time()

for N in range(11, max_N + 1):
    try:
        curves_dict = DB.allcurves(N)
    except:
        continue
    if not curves_dict:
        continue
    for label_suffix, data in curves_dict.items():
        try:
            ainvs = data[0]
            r = data[1]  # rank stored in DB
            # tors_order = data[2]
            E = EllipticCurve(ainvs)
            sha_an = round(E.sha().an_numerical())
            tors_gens = E.torsion_subgroup().gens()
            tors_orders = [g.order() for g in tors_gens]
            curve_data.append((r, sha_an, tors_orders, N))
        except:
            continue

t1 = time.time()
print(f"Collected {len(curve_data)} curves (N <= {max_N}) in {t1-t0:.1f}s")

# Rank distribution
rank_counts = {}
for (r, sha, tors, N) in curve_data:
    rank_counts[r] = rank_counts.get(r, 0) + 1
print(f"Rank distribution: {dict(sorted(rank_counts.items()))}")

# Compute averages for each p
print(f"\n{'p':>3} | {'avg|Sel_p|':>12} | {'predicted':>10} | {'ratio':>8} | {'count':>6}")
print("-"*55)

for p in [2, 3, 5, 7, 11, 13]:
    total = 0
    count = 0
    for (r, sha_an, tors_orders, N) in curve_data:
        # p-torsion dimension
        tors_p_dim = sum(1 for o in tors_orders if o % p == 0)

        # Sha[p] part
        sha_p_part = 1
        temp = sha_an
        while temp > 0 and temp % p == 0:
            sha_p_part *= p
            temp = temp // p

        sel_size = p^(r + tors_p_dim) * sha_p_part
        total += sel_size
        count += 1

    if count > 0:
        avg = RR(total) / count
        pred = p + 1
        ratio = avg / pred
        print(f"{p:>3} | {avg:>12.6f} | {pred:>10} | {ratio:>8.6f} | {count:>6}")

# Convergence by conductor range
print(f"\nConvergence of avg|Sel_2| by conductor range:")
print(f"{'Range':>15} | {'avg|Sel_2|':>12} | {'count':>6}")
print("-"*40)

ranges = [(11, 200), (201, 500), (501, 1000), (1001, 1500), (1501, 2000), (2001, 2500), (2501, 3000)]
for lo, hi in ranges:
    total = 0
    count = 0
    for (r, sha_an, tors_orders, N) in curve_data:
        if lo <= N <= hi:
            tors_2_dim = sum(1 for o in tors_orders if o % 2 == 0)
            sha_2_part = 1
            temp = sha_an
            while temp > 0 and temp % 2 == 0:
                sha_2_part *= 2
                temp = temp // 2
            sel2 = 2^(r + tors_2_dim) * sha_2_part
            total += sel2
            count += 1
    if count > 0:
        avg = RR(total) / count
        print(f"[{lo:>5}, {hi:>5}] | {avg:>12.6f} | {count:>6}")

# Now do the same convergence for p=7 and p=11
print(f"\nConvergence of avg|Sel_7| by conductor range:")
print(f"{'Range':>15} | {'avg|Sel_7|':>12} | {'count':>6}")
print("-"*40)

for lo, hi in ranges:
    total = 0
    count = 0
    for (r, sha_an, tors_orders, N) in curve_data:
        if lo <= N <= hi:
            tors_7_dim = sum(1 for o in tors_orders if o % 7 == 0)
            sha_7_part = 1
            temp = sha_an
            while temp > 0 and temp % 7 == 0:
                sha_7_part *= 7
                temp = temp // 7
            sel7 = 7^(r + tors_7_dim) * sha_7_part
            total += sel7
            count += 1
    if count > 0:
        avg = RR(total) / count
        print(f"[{lo:>5}, {hi:>5}] | {avg:>12.6f} | {count:>6}")
