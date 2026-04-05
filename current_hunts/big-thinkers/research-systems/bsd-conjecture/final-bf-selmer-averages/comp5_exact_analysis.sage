"""
Computation 5: Careful analysis of Selmer averages.

The formula |Sel_p(E)| = p^(rank + dim E(Q)[p]) * |Sha[p]| is WRONG
for computing the average.

The correct relationship:
- 0 -> E(Q)/pE(Q) -> Sel_p(E) -> Sha(E)[p] -> 0
- |Sel_p(E)| = |E(Q)/pE(Q)| * |Sha(E)[p]|

But E(Q)/pE(Q) is NOT just p^rank * E(Q)[p].
It's: |E(Q)/pE(Q)| = p^rank * |E(Q)[p]|

where rank = Mordell-Weil rank and E(Q)[p] is the p-torsion of E(Q).

HOWEVER: for the AVERAGE, we need to be careful.
The Bhargava-Shankar result is about the p-SELMER GROUP Sel_p(E),
which they define as a subgroup of H^1(Q, E[p]).

The key issue: |Sel_p(E)| includes BOTH the rank contribution AND Sha.
For the average to be p+1, we need:
    E[|Sel_p(E)|] = p + 1

Let's verify this explicitly.

For rank 0: |Sel_p| = |Sha[p]| (since E(Q)/pE(Q) has no rank contribution)
    Wait -- E(Q)/pE(Q) includes p-torsion: |E(Q)/pE(Q)| = p^0 * |E(Q)[p]| = |E(Q)[p]|
    So |Sel_p| = |E(Q)[p]| * |Sha[p]|

For rank 1: |Sel_p| = p * |E(Q)[p]| * |Sha[p]|

For rank r: |Sel_p| = p^r * |E(Q)[p]| * |Sha[p]|

The expected value:
    E[|Sel_p|] = sum_r Pr[rank=r] * E[p^r * |E(Q)[p]| * |Sha[p]| | rank=r]

For p >= 5 (where p-torsion is very rare):
    E[|Sel_p|] ~ Pr[r=0]*1 + Pr[r=1]*p + Pr[r>=2]*p^2 + ... + Sha corrections

Now, the rank distribution in our data:
    r=0: 50.2%
    r=1: 47.6%
    r=2: 2.2%

So ignoring Sha and torsion:
    E[|Sel_p|] ~ 0.502 + 0.476*p + 0.022*p^2

This is a QUADRATIC in p, not linear. For large p, it grows as 0.022*p^2.
But Bhargava predicts p+1 (LINEAR in p).

THE RESOLUTION: the rank distribution CHANGES with height.
As height -> infinity:
    Pr[r=0] -> 1/2 (conjecturally)
    Pr[r=1] -> 1/2 (conjecturally)
    Pr[r>=2] -> 0 (conjecturally, PPVW)

So in the limit:
    E[|Sel_p|] -> 1/2 * 1 + 1/2 * p + 0 * p^2 + Sha corrections
                = (1 + p)/2 + Sha corrections
                = (p+1)/2 + Sha corrections

For this to equal p+1, we need Sha corrections = (p+1)/2.

THIS IS THE KEY INSIGHT: the Sha contribution must be EXACTLY (p+1)/2
to match the Bhargava prediction.

Actually wait -- I need to reconsider. Bhargava's result is about the
ASYMPTOTIC average, and the rank distribution at finite height doesn't
converge to the asymptotic one.

The correct computation of E[|Sel_p|] requires:
    E[|Sel_p|] = E[p^{s_p(E)}]
where s_p(E) = dim_Fp Sel_p(E) is the p-Selmer rank.

Bhargava-Shankar prove: E[|Sel_p|] = p+1 (asymptotically)
where E is over all curves ordered by height.

This does NOT decompose as "rank contribution + Sha contribution" simply.
The Selmer rank s_p = rank + dim Sha[p] + correction from torsion.

For a curve with rank r and trivial Sha[p]:
    s_p = r + dim E(Q)[p]

For most curves and large p:
    s_p = r (since dim E(Q)[p] = 0 for p > torsion bound)

So |Sel_p| = p^r for most curves.

E[p^r] = Pr[r=0]*1 + Pr[r=1]*p + Pr[r=2]*p^2 + ...

The Bhargava prediction E[p^r + Sha correction] = p+1 is equivalent to:
    E[p^{s_p}] = p + 1

This means: the MOMENT GENERATING FUNCTION of s_p at log(p) equals p+1.
"""

print("="*70)
print("COMPUTATION 5: EXACT SELMER AVERAGE ANALYSIS")
print("="*70)

from sage.databases.cremona import CremonaDatabase
from collections import Counter

DB = CremonaDatabase()

# Get the rank distribution from the database
ranks = []
tors_orders = []
for N in range(11, 5001):
    try:
        curves_dict = DB.allcurves(N)
    except:
        continue
    if not curves_dict:
        continue
    for label_suffix, data in curves_dict.items():
        ranks.append(data[1])
        tors_orders.append(data[2])

n = len(ranks)
rank_dist = Counter(ranks)
print(f"Total curves: {n}")
print(f"Rank distribution: {dict(sorted(rank_dist.items()))}")

# For each prime p, compute E[p^r] (ignoring Sha and torsion)
print(f"\n--- E[p^rank] vs p+1 ---")
print(f"{'p':>4} | {'E[p^rank]':>12} | {'p+1':>6} | {'ratio':>8} | {'excess from r>=2':>18}")
print("-"*70)

for p in [2, 3, 5, 7, 11, 13, 17, 23, 29, 37, 41, 43, 47, 53, 97]:
    total = sum(p^r * count for r, count in rank_dist.items())
    avg = RR(total) / n

    # Contribution from rank >= 2
    excess = sum(p^r * count for r, count in rank_dist.items() if r >= 2)
    excess_avg = RR(excess) / n

    pred = p + 1
    ratio = avg / pred
    print(f"{p:>4} | {avg:>12.4f} | {pred:>6} | {ratio:>8.4f} | {excess_avg:>18.4f}")

# The excess from rank >= 2 grows as p^2 * Pr[r>=2]
pr_r2 = RR(sum(count for r, count in rank_dist.items() if r >= 2)) / n
print(f"\nPr[rank >= 2] in this dataset: {pr_r2:.6f}")
print(f"For large p: excess ~ {pr_r2:.4f} * p^2")
print(f"E[p^rank] ~ 0.50 + 0.476*p + {pr_r2:.4f}*p^2")
print(f"Target:     ~ p + 1")

# What the Sha correction needs to be
print(f"\n--- Required Sha correction for E[|Sel_p|] = p+1 ---")
print(f"{'p':>4} | {'E[p^rank]':>12} | {'p+1':>6} | {'needed Sha':>12} | {'as fraction of p+1':>20}")
print("-"*70)

for p in [2, 3, 5, 7, 11, 13, 17, 23, 29]:
    total = sum(p^r * count for r, count in rank_dist.items())
    avg_p_r = RR(total) / n
    needed = (p + 1) - avg_p_r
    # But this is wrong -- the Sha correction is multiplicative, not additive
    # |Sel_p| = p^rank * |Sha[p]| (for most curves, ignoring torsion)
    # E[|Sel_p|] = E[p^rank * |Sha[p]|]
    # This is NOT E[p^rank] * E[|Sha[p]|] unless rank and Sha[p] are independent

    # For rank 0 curves: E[|Sha[p]| | rank=0] is the expected p-part of Sha for rank 0
    # For rank 1 curves: E[|Sha[p]| | rank=1] is the expected p-part for rank 1
    # For rank >= 2: similarly

    # The needed total correction is:
    # p+1 = sum_r Pr[r] * E[p^r * |Sha[p]| | rank = r]
    #      = Pr[0]*E[|Sha[p]||r=0] + Pr[1]*p*E[|Sha[p]||r=1] + Pr[2]*p^2*E[|Sha[p]||r=2] + ...

    # For this to equal p+1:
    # If we assume E[|Sha[p]||r] = 1 + delta_r for small delta_r, then
    # p+1 ~ sum_r Pr[r] * p^r * (1 + delta_r)
    #      = E[p^r] + sum_r Pr[r] * p^r * delta_r

    if avg_p_r > p + 1:
        needed_sign = "NEGATIVE"
        deficit = avg_p_r - (p + 1)
    else:
        needed_sign = "positive"
        deficit = (p + 1) - avg_p_r

    frac = deficit / (p + 1)
    print(f"{p:>4} | {avg_p_r:>12.4f} | {p+1:>6} | {needed_sign:>12} | {frac:>20.4f}")

# The key realization:
print("""
KEY REALIZATION:
For p >= 29, E[p^rank] > p+1 at this finite conductor range.
This means the "Sha correction" would need to be NEGATIVE,
which is impossible (|Sha[p]| >= 1 always).

RESOLUTION: The Bhargava average is ASYMPTOTIC in the height.
At finite height, the rank distribution has too many rank >= 2 curves.
As height -> infinity, Pr[rank >= 2] -> 0 (conjecturally), and then:
    E[p^rank] -> Pr[r=0] + Pr[r=1]*p = 1/2 + p/2 = (p+1)/2

So in the asymptotic limit:
    E[|Sel_p|] = E[p^rank] * E[|Sha[p]| correction]
              = (p+1)/2 * (Sha correction)

For this to equal p+1: Sha correction = 2.

This means: E[|Sha[p]|] = 2 (averaged over all rank 0 and rank 1 curves).
But E[|Sha[p]|] = 1 + Pr[Sha[p] != 0] * (average size when nontrivial)
So Pr[Sha[p] != 0] * (avg nontrivial size - 1) = 1.

For the Poonen-Rains model:
    Pr[Sha[p] = p^2] ~ C/p^3 (for large p)
    E[|Sha[p]|] ~ 1 + sum_{k=1}^inf (p^{2k} - 1) * Pr[|Sha[p]| = p^{2k}]
    This converges to a value ~ 1 + O(1/p) for large p.

Wait -- this doesn't add up. Let me reconsider.

Actually, the Bhargava average is:
    E[|Sel_p|] = sum_E p^{s_p(E)} / #curves

where s_p(E) = dim_Fp Sel_p(E).

The Selmer rank s_p is NOT simply rank + dim Sha[p].
It's: s_p = dim_Fp Sel_p(E), and the relationship is:
    s_p >= rank (since the Mordell-Weil generators give independent Selmer classes)

The DIFFERENCE s_p - rank is the "Sha contribution" (really the kernel of Sel -> Sha).

For rank 0, s_p = dim Sha[p]_{surviving} (the part detected by Selmer)
For rank 1, s_p = 1 + dim Sha[p]_{surviving}
Etc.

The average E[p^{s_p}] = p+1 is a JOINT statement about rank AND Sha.

In the Poonen-Rains model:
    s_p ~ dim(U cap W) where U, W are random maximal isotropic subspaces
    rank ~ some function of the intersection (related to the kernel of the pairing)
    Sha[p] ~ the cokernel

The distribution of dim(U cap W) gives:
    E[p^dim] = p + 1 directly from the random matrix computation.
""")
