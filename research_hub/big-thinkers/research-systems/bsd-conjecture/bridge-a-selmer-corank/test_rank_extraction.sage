"""
Fast test: rank extraction from M1 only (skip selmer_rank computation).
Tests on 2000 curves from conductor 3001-5000.
"""
from collections import Counter, defaultdict
from math import log

db = CremonaDatabase()

correct_rank = 0
total = 0
rank_by_true = defaultdict(list)

NUM_PRIMES = 50
primes_list = list(primes(300))[:NUM_PRIMES]
X = int(primes_list[-1])
log_log_X = log(log(X))

# From earlier analysis: spacing ~ 1.65, C_base ~ 0.55
C_base = 0.55
spacing = 1.65

for N in range(3001, 5001):
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

            # Compute a_p
            good_ap = []
            for p in primes_list:
                if N % int(p) != 0:
                    good_ap.append((int(p), int(E.ap(p))))

            if len(good_ap) < 30:
                continue

            M1 = sum(a/float(p) for p, a in good_ap)
            rank_est = max(0, round((-M1 + C_base) / spacing))
            rank_est = min(rank_est, 4)

            rank_by_true[true_rank].append((M1, rank_est == true_rank))

            if true_rank == rank_est:
                correct_rank += 1
            total += 1

        except Exception:
            pass

    if N % 500 == 0:
        if total > 0:
            print(f"N<={N}: {total} curves, rank acc={float(correct_rank)/float(total):.3f}")

print(f"\n{'='*60}")
print(f"RANK EXTRACTION TEST (conductor 3001-5000, 50 primes)")
print(f"{'='*60}")
print(f"Total curves: {total}")
print(f"Overall rank accuracy: {correct_rank}/{total} = {float(correct_rank)/float(total):.3f}")

for r in sorted(rank_by_true.keys()):
    entries = rank_by_true[r]
    n = len(entries)
    correct = sum(1 for _, c in entries if c)
    m1_vals = [float(m) for m, _ in entries]
    mean_m1 = sum(m1_vals) / n
    std_m1 = (sum((x - mean_m1)**2 for x in m1_vals) / n)**0.5
    print(f"  rank={r}: n={n}, acc={correct}/{n}={float(correct)/float(n):.3f}, M1={mean_m1:+.4f}+/-{std_m1:.4f}")

# Also test g_Lambda
print(f"\nWith running coupling (g_Lambda thresholds):")
correct_gL = 0
for N in range(3001, 5001):
    try:
        curves = db.allcurves(N)
    except:
        continue
    for label_suffix, data_raw in curves.items():
        try:
            ainvs = data_raw[0] if isinstance(data_raw, (list, tuple)) else data_raw
            E = EllipticCurve(ainvs)
            true_rank = E.rank()

            good_ap = []
            for p in primes_list:
                if N % int(p) != 0:
                    good_ap.append((int(p), int(E.ap(p))))
            if len(good_ap) < 30:
                continue

            log_L = 0.0
            for p, a in good_ap:
                ef = 1.0 - float(a)/float(p) + 1.0/float(p)
                if ef > 0:
                    log_L -= log(ef)
                else:
                    log_L -= log(abs(ef))
            gL = log_L / log(float(good_ap[-1][0]))

            if gL > -0.27:
                rank_est = 0
            elif gL > -0.62:
                rank_est = 1
            elif gL > -0.95:
                rank_est = 2
            else:
                rank_est = 3

            if true_rank == rank_est:
                correct_gL += 1
        except:
            pass

print(f"  g_Lambda accuracy: {correct_gL}/{total} = {float(correct_gL)/float(total):.3f}")
