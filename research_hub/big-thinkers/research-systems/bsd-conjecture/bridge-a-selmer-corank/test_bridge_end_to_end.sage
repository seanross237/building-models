"""
End-to-end test of the corank bridge on a fresh set of curves.

The bridge chain:
  1. Compute a_p for primes up to X
  2. M1 = sum a_p/p -> rank (via explicit formula rounding)
  3. freq_ap_even -> tors2_rk
  4. sel2_rank (algebraic) -> sha2_dim = sel2 - rank - tors2_rk

Test: how accurately does this chain recover rank and sha2_dim?
"""

import json
from collections import Counter, defaultdict
from math import log

db = CremonaDatabase()

# Test curves: conductor 5001-8000 (NOT in training set)
correct_rank = 0
correct_sha2 = 0
total = 0
rank_errors_by_true_rank = defaultdict(int)
rank_correct_by_true_rank = defaultdict(int)

NUM_PRIMES = 50
primes_list = list(primes(300))[:NUM_PRIMES]
X = int(primes_list[-1])
log_log_X = log(log(X))

# Calibration from training data:
# M1_mean(rank=0) ≈ +0.55 (50 primes), M1_mean(rank=1) ≈ -1.1
# Spacing ≈ 1.65 per rank unit
# Threshold: rank = round((-M1 + C_base) / spacing)
# where C_base ≈ 0.55 (mean C(E) at rank 0)
C_base = 0.55
spacing = 1.65  # slightly larger than log_log_X due to the 15% excess

tested = 0
for N in range(5001, 8001):
    try:
        curves = db.allcurves(N)
    except:
        continue
    for label_suffix, data_raw in curves.items():
        label = f"{N}{label_suffix}"
        try:
            ainvs = data_raw[0] if isinstance(data_raw, (list, tuple)) else data_raw
            E = EllipticCurve(ainvs)

            true_rank = E.rank()
            true_sel2 = E.selmer_rank()
            true_sha = round(float(E.sha().an()))
            tors = [int(x) for x in E.torsion_subgroup().invariants()]
            true_tors2 = sum(1 for t in tors if t % 2 == 0)
            true_sha2_dim = true_sel2 - true_rank - true_tors2

            # Compute a_p
            good_ap = []
            for p in primes_list:
                if N % int(p) != 0:
                    good_ap.append((int(p), int(E.ap(p))))

            if len(good_ap) < 30:
                continue

            # Step 1: Compute M1
            M1 = sum(a/float(p) for p, a in good_ap)

            # Step 2: Infer rank from M1
            rank_est = max(0, round((-M1 + C_base) / spacing))
            rank_est = min(rank_est, 4)  # cap at 4

            # Step 3: Infer tors2_rk from freq_ap_even
            freq_even = sum(1 for p, a in good_ap if p > 2 and a % 2 == 0) / sum(1 for p, _ in good_ap if p > 2)
            tors2_est = 0 if freq_even < 0.9 else 1
            # Distinguish tors2=1 from tors2=2
            if freq_even > 0.99:
                # Could be tors2=2, but need more info
                # For now, use torsion order if available from a_p data
                # Actually, can detect Z/2 x Z/2 vs Z/2 from the a_p pattern
                # Z/2 x Z/2 means all a_p ≡ 0 mod 4 for good p ≡ 1 mod 4? No.
                # Just use freq > 0.99 as indicator of 2-rank >= 1
                tors2_est = 1

            # Step 4: Compute sha2_dim
            sha2_est = max(0, true_sel2 - rank_est - tors2_est)

            if true_rank == rank_est:
                correct_rank += 1
                rank_correct_by_true_rank[true_rank] += 1
            else:
                rank_errors_by_true_rank[true_rank] += 1

            if true_sha2_dim == sha2_est:
                correct_sha2 += 1

            total += 1

        except Exception:
            pass

    if N % 500 == 0:
        if total > 0:
            print(f"N<={N}: {total} curves, rank acc={correct_rank/total:.3f}, sha2 acc={correct_sha2/total:.3f}")

print(f"\n{'='*60}")
print(f"END-TO-END BRIDGE TEST (conductor 5001-8000)")
print(f"{'='*60}")
print(f"Total curves: {total}")
print(f"Rank accuracy: {correct_rank}/{total} = {correct_rank/total:.3f}" if total else "No curves")
print(f"sha2_dim accuracy: {correct_sha2}/{total} = {correct_sha2/total:.3f}" if total else "No curves")

print(f"\nRank accuracy by true rank:")
for r in sorted(set(list(rank_correct_by_true_rank.keys()) + list(rank_errors_by_true_rank.keys()))):
    correct = rank_correct_by_true_rank[r]
    errors = rank_errors_by_true_rank[r]
    total_r = correct + errors
    print(f"  rank={r}: {correct}/{total_r} = {correct/total_r:.3f}" if total_r > 0 else f"  rank={r}: 0/0")
