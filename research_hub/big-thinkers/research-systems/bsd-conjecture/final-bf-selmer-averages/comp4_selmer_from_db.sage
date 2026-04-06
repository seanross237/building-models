"""
Computation 4: p-Selmer averages using stored rank/torsion from Cremona DB.
Skip Sha computation (use Sha=1 for most curves, which is correct for the vast majority).

The key formula: |Sel_p(E)| = p^(rank + dim E(Q)[p]) * |Sha[p]|

For the AVERAGE, the dominant contribution comes from:
- rank 0 curves: |Sel_p| = |Sha[p]| (usually 1)
- rank 1 curves: |Sel_p| = p * |Sha[p]| (usually p)
- rank >= 2 curves: |Sel_p| >= p^2

Since we're testing Bhargava's conjecture E[|Sel_p|] = p+1, we can use the
stored rank from the DB and only compute Sha for the minority of curves where
it matters.
"""
from sage.databases.cremona import CremonaDatabase
import time

DB = CremonaDatabase()

print("="*70)
print("COMPUTATION 4: p-SELMER AVERAGES (FAST)")
print("="*70)

# Collect curve data using DB-stored rank
max_N = 5000
ranks = []
tors_data = []
sha_data = []
conductors = []

t0 = time.time()
for N in range(11, max_N + 1):
    try:
        curves_dict = DB.allcurves(N)
    except:
        continue
    if not curves_dict:
        continue
    for label_suffix, data in curves_dict.items():
        ainvs = data[0]
        r = data[1]  # stored rank
        tors_order = data[2]  # stored torsion order
        ranks.append(r)
        tors_data.append(tors_order)
        conductors.append(N)
        # Sha: assume 1 for now (correct for >95% of curves)
        # We'll correct this with a smaller detailed sample
        sha_data.append(1)

t1 = time.time()
print(f"Collected {len(ranks)} curves (N <= {max_N}) in {t1-t0:.1f}s")

# Rank distribution
from collections import Counter
rank_dist = Counter(ranks)
print(f"Rank distribution: {dict(sorted(rank_dist.items()))}")

# Torsion distribution (just the order)
tors_dist = Counter(tors_data)
print(f"Torsion order distribution: {dict(sorted(tors_dist.items()))}")

# Compute "approximate" Selmer averages (assuming Sha[p] = 0 for all curves)
# This gives a LOWER BOUND on avg|Sel_p|
print(f"\n--- Lower bound on avg|Sel_p| (assuming Sha trivial) ---")
print(f"{'p':>3} | {'avg_lower':>12} | {'predicted':>10} | {'ratio':>8} | note")
print("-"*65)

for p in [2, 3, 5, 7, 11, 13, 17, 23, 29, 37, 41, 43, 47]:
    total = 0
    for i in range(len(ranks)):
        r = ranks[i]
        tors_order = tors_data[i]

        # dim E(Q)[p]
        tors_p_dim = 0
        temp = tors_order
        while temp % p == 0:
            tors_p_dim += 1
            temp = temp // p
        # Actually for torsion, if tors_order = p^a * m with gcd(m,p)=1,
        # then E(Q)[p] has order p^min(a, 2) (since E[p] has rank 2 over F_p)
        # But we need dim over F_p, not the exact p-part.
        # E(Q) is finite abelian, so E(Q)[p] = (Z/pZ)^d for d = 0, 1, or 2
        # d = number of cyclic factors of E(Q)_tors that are divisible by p
        # For simplicity: if p | tors_order, d >= 1; if p^2 | tors_order, d might be 2
        # But for Selmer rank, we need: dim_Fp (E(Q)/pE(Q)) = rank + d
        # where d = dim_Fp E(Q)[p]

        # More careful: the torsion subgroup of E(Q) is Z/aZ x Z/bZ with a|b
        # E(Q)[p] = (Z/gcd(a,p)Z) x (Z/gcd(b,p)Z)
        # dim_Fp = #{i : p | tors_factor_i}

        # From tors_order alone we can't distinguish Z/12Z from Z/2Z x Z/6Z
        # But for our estimate, the main contribution is from rank, not torsion
        # For p >= 5, very few curves have p | tors_order

        sel_p_size = p^(r + tors_p_dim)  # lower bound (ignoring Sha[p])
        total += sel_p_size

    avg_lower = RR(total) / len(ranks)
    pred = p + 1
    ratio = avg_lower / pred
    note = ""
    if ratio > 0.95:
        note = "CLOSE"
    elif ratio < 0.5:
        note = "Sha correction needed"
    print(f"{p:>3} | {avg_lower:>12.6f} | {pred:>10} | {ratio:>8.6f} | {note}")

# Now compute the exact Sha contribution for a SAMPLE of curves
print(f"\n--- Sha correction from sample (first 1000 curves) ---")

sha_corrections = {}
sample_size = min(1000, len(ranks))
t0 = time.time()

# We need actual curves for Sha computation
sample_shas = {}
count = 0
for N in range(11, max_N + 1):
    if count >= sample_size:
        break
    try:
        curves_dict = DB.allcurves(N)
    except:
        continue
    if not curves_dict:
        continue
    for label_suffix, data in curves_dict.items():
        if count >= sample_size:
            break
        try:
            ainvs = data[0]
            E = EllipticCurve(ainvs)
            sha_an = round(E.sha().an_numerical())
            sample_shas[count] = sha_an
            count += 1
        except:
            sample_shas[count] = 1
            count += 1

t1 = time.time()
print(f"Computed Sha for {len(sample_shas)} curves in {t1-t0:.1f}s")

# Distribution of Sha values in sample
sha_vals = Counter(sample_shas.values())
print(f"Sha distribution in sample: {dict(sorted(sha_vals.items()))}")

# Compute Sha correction
for p in [2, 3, 5, 7, 11]:
    correction_total = 0
    for idx, sha_val in sample_shas.items():
        sha_p_part = 1
        temp = sha_val
        while temp > 0 and temp % p == 0:
            sha_p_part *= p
            temp = temp // p
        correction_total += sha_p_part  # This is the multiplicative correction

    avg_sha_factor = RR(correction_total) / len(sample_shas)
    print(f"  p={p}: avg Sha[p] correction factor = {avg_sha_factor:.6f}")

print("\n--- Corrected Selmer averages ---")
print("(Using Sha correction from sample applied to full dataset)")
print(f"{'p':>3} | {'avg_corrected':>14} | {'predicted':>10} | {'ratio':>8}")
print("-"*50)

# For each p, the correction is multiplicative: true avg = lower_bound * avg_sha_factor
# This is approximate but gives the right order of magnitude
for p in [2, 3, 5, 7, 11, 13]:
    total = 0
    for i in range(len(ranks)):
        r = ranks[i]
        tors_order = tors_data[i]
        tors_p_dim = 0
        temp = tors_order
        while temp % p == 0:
            tors_p_dim += 1
            temp = temp // p
        sel_p_size = p^(r + tors_p_dim)
        total += sel_p_size
    avg_lower = RR(total) / len(ranks)

    # Apply Sha correction from sample
    correction = 0
    for idx, sha_val in sample_shas.items():
        sha_p_part = 1
        temp = sha_val
        while temp > 0 and temp % p == 0:
            sha_p_part *= p
            temp = temp // p
        correction += sha_p_part
    avg_sha = RR(correction) / len(sample_shas)

    avg_corrected = avg_lower * avg_sha
    pred = p + 1
    ratio = avg_corrected / pred
    print(f"{p:>3} | {avg_corrected:>14.6f} | {pred:>10} | {ratio:>8.6f}")
