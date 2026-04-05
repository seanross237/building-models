"""
Compute Frobenius moment statistics and Selmer group data for elliptic curves.

Goal: Test whether the first k moments of {a_p/p} jointly determine (rank, dim Sha[p]).

For each curve we compute:
  - Mordell-Weil rank
  - 2-Selmer rank (dim_F2 Sel_2(E))
  - Analytic Sha (from BSD formula)
  - Frobenius trace moments: M_k = sum_{p<=X} a_p^k / p^k for k=1,2,3,4
  - Weighted moments: W_k = sum_{p<=X} a_p^k / p^{k/2+1} (Sato-Tate normalized)
  - The symmetric square partial sum: sum_{p<=X} (a_p^2 - p) / p^2
  - Murmuration sum: sum a_p * p^{-0.84}
"""

import json
import sys
from collections import defaultdict

# Parameters
MAX_CONDUCTOR = 5000
PRIME_BOUND = 500
NUM_PRIMES = 100  # first 100 primes

# Get primes
primes_list = list(primes(PRIME_BOUND + 1))[:NUM_PRIMES]
print(f"Using {len(primes_list)} primes up to {primes_list[-1]}")

# Collect data
results = []
db = CremonaDatabase()

conductors = range(1, MAX_CONDUCTOR + 1)
count = 0
errors = 0

for N in conductors:
    try:
        curves = db.allcurves(N)
    except Exception:
        continue

    for label_suffix, data in curves.items():
        label = f"{N}{label_suffix}"
        try:
            ainvs = data[0] if isinstance(data, (list, tuple)) else data
            E = EllipticCurve(ainvs)

            # Basic invariants
            rank = E.rank()
            conductor = E.conductor()
            torsion_order = E.torsion_order()
            torsion_struct = [int(x) for x in E.torsion_subgroup().invariants()]

            # 2-Selmer group
            try:
                sel2 = E.selmer_rank()  # This is dim_F2(Sel_2)
            except Exception:
                sel2 = -1

            # Analytic Sha
            try:
                sha_an = E.sha().an()
                sha_val = float(sha_an)
            except Exception:
                sha_val = -1.0

            # Frobenius traces at good primes
            ap_list = []
            good_primes = []
            for p in primes_list:
                if conductor % p != 0:
                    ap = int(E.ap(p))
                    ap_list.append(ap)
                    good_primes.append(int(p))

            if len(ap_list) < 50:
                continue

            # Compute moments
            # M_k = sum a_p^k / p^k (the raw moments)
            M1 = sum(a / float(p) for a, p in zip(ap_list, good_primes))
            M2 = sum(a**2 / float(p)**2 for a, p in zip(ap_list, good_primes))
            M3 = sum(a**3 / float(p)**3 for a, p in zip(ap_list, good_primes))
            M4 = sum(a**4 / float(p)**4 for a, p in zip(ap_list, good_primes))

            # Sato-Tate normalized moments: a_p / (2*sqrt(p))
            # W_k = sum (a_p/(2*sqrt(p)))^k / p  (normalized by 1/p for convergence)
            W1 = sum(a / (2 * float(p)**0.5) / float(p) for a, p in zip(ap_list, good_primes))
            W2 = sum((a / (2 * float(p)**0.5))**2 / float(p) for a, p in zip(ap_list, good_primes))
            W3 = sum((a / (2 * float(p)**0.5))**3 / float(p) for a, p in zip(ap_list, good_primes))
            W4 = sum((a / (2 * float(p)**0.5))**4 / float(p) for a, p in zip(ap_list, good_primes))

            # Second moment deviation: sum (a_p^2 - p) / p^2
            sym2_sum = sum((a**2 - float(p)) / float(p)**2 for a, p in zip(ap_list, good_primes))

            # E[a_p^2]/p for small primes (p <= 23)
            small_primes_ap2 = []
            for a, p in zip(ap_list, good_primes):
                if p <= 23:
                    small_primes_ap2.append(a**2 / float(p))
            mean_ap2_over_p_small = sum(small_primes_ap2) / len(small_primes_ap2) if small_primes_ap2 else 0

            # Murmuration sum: sum a_p * p^{-0.84}
            murm_sum = sum(a * float(p)**(-0.84) for a, p in zip(ap_list, good_primes))

            # Running coupling at Lambda
            # g(Lambda) = log|L_Lambda(E,1)| / log(Lambda)
            # L_Lambda = prod (1 - a_p/p + 1/p)^{-1}
            log_L = 0.0
            for a, p in zip(ap_list, good_primes):
                euler_factor = 1.0 - float(a)/float(p) + 1.0/float(p)
                if euler_factor > 0:
                    log_L -= log(euler_factor)
                else:
                    log_L -= log(abs(euler_factor))

            Lambda = good_primes[-1]
            g_Lambda = log_L / log(float(Lambda))

            # Local data: frequency of a_p ≡ 0 mod 2
            freq_ap_even = sum(1 for a in ap_list if a % 2 == 0) / len(ap_list)

            # Average |a_p|/sqrt(p) (Sato-Tate scale)
            mean_normalized_ap = sum(abs(a) / float(p)**0.5 for a, p in zip(ap_list, good_primes)) / len(ap_list)

            entry = {
                'label': label,
                'conductor': int(conductor),
                'rank': int(rank),
                'sel2_rank': int(sel2),  # dim_F2(Sel_2(E))
                'sha_an': round(sha_val, 6),
                'torsion_order': int(torsion_order),
                'torsion_struct': torsion_struct,
                'M1': round(M1, 8),
                'M2': round(M2, 8),
                'M3': round(M3, 8),
                'M4': round(M4, 8),
                'W1': round(W1, 8),
                'W2': round(W2, 8),
                'W3': round(W3, 8),
                'W4': round(W4, 8),
                'sym2_sum': round(sym2_sum, 8),
                'mean_ap2_over_p_small': round(mean_ap2_over_p_small, 6),
                'murm_sum': round(murm_sum, 6),
                'g_Lambda': round(g_Lambda, 8),
                'freq_ap_even': round(freq_ap_even, 6),
                'mean_normalized_ap': round(mean_normalized_ap, 6),
                'n_good_primes': len(ap_list),
            }
            results.append(entry)
            count += 1

            if count % 500 == 0:
                print(f"  Processed {count} curves (conductor <= {N})")

        except Exception as e:
            errors += 1
            if errors <= 10:
                print(f"  Error on {label}: {e}")

print(f"\nDone: {count} curves processed, {errors} errors")
print(f"Rank distribution: {dict(sorted(defaultdict(int, {r: sum(1 for e in results if e['rank']==r) for r in set(e['rank'] for e in results)}).items()))}")
print(f"Sel2 distribution: {dict(sorted(defaultdict(int, {s: sum(1 for e in results if e['sel2_rank']==s) for s in set(e['sel2_rank'] for e in results)}).items()))}")

# Count curves with non-trivial Sha
sha_nontrivial = [e for e in results if e['sha_an'] > 1.5]
print(f"Curves with |Sha| > 1: {len(sha_nontrivial)}")
sha_counts = defaultdict(int)
for e in sha_nontrivial:
    sha_counts[round(e['sha_an'])] += 1
print(f"  Sha value distribution: {dict(sorted(sha_counts.items()))}")

# Save
output_path = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/bridge-a-selmer-corank/moment_selmer_data.json"
with open(output_path, 'w') as f:
    json.dump(results, f, indent=1)
print(f"Saved to {output_path}")
