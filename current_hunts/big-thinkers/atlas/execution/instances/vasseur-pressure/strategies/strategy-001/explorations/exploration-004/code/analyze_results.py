"""Analyze the pressure decomposition results and produce formatted tables."""

import json
import os

OUTDIR = '/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/atlas/execution/instances/vasseur-pressure/strategies/strategy-001/explorations/exploration-004'

with open(os.path.join(OUTDIR, 'code', 'results.json'), 'r') as f:
    data = json.load(f)

print("=" * 80)
print("DECOMPOSITION VERIFICATION")
print("=" * 80)

for case in data['cases']:
    print(f"\nIC={case['ic']}, Re={case['Re']}, N={case['N']}")
    print(f"  max_speed={case['max_speed']:.4f}, energy={case['energy']:.6f}")
    if 'renorm_factor' in case:
        print(f"  renorm_factor={case['renorm_factor']:.4f}, renormed_max={case['renormed_max_speed']:.4f}")
    for kr in case['k_results']:
        print(f"  k={kr['k_level']}: decomp_err_rel={kr['decomp_error_rel']:.2e}, "
              f"frac_above={kr['frac_above_threshold']:.4f}")

print("\n")
print("=" * 80)
print("TABLE A: CZ TIGHTNESS BY PRESSURE PIECE (k=4, mid-range)")
print("=" * 80)

# Pick k=4 as representative
target_k = 4
q_vals = [2, 3, 4, 6, 8]

print(f"\n{'IC':<16} {'Re':<6} {'Piece':<8}", end="")
for q in q_vals:
    print(f" {'q='+str(q):<8}", end="")
print()
print("-" * 80)

for case in data['cases']:
    # Find k=4 result
    kr = None
    for r in case['k_results']:
        if r['k_level'] == target_k:
            kr = r
            break
    if kr is None:
        continue

    for piece in ['full', 'P21', 'P22', 'P23']:
        print(f"{case['ic']:<16} {case['Re']:<6} {piece:<8}", end="")
        for q in q_vals:
            key = str(q) if str(q) in kr['tightness'] else q
            t = kr['tightness'].get(str(q), kr['tightness'].get(q, {}))
            val = t.get(piece, 0)
            print(f" {val:<8.4f}", end="")
        print()
    print()


print("\n")
print("=" * 80)
print("TABLE B: P_k^{21} TIGHTNESS vs k (THE CRITICAL MEASUREMENT)")
print("=" * 80)

for q in [2, 4, 6, 8]:
    print(f"\n--- q = {q} ---")
    print(f"{'IC':<16} {'Re':<6}", end="")
    for k in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        print(f" {'k='+str(k):<7}", end="")
    print(" Trend")
    print("-" * 120)

    for case in data['cases']:
        print(f"{case['ic']:<16} {case['Re']:<6}", end="")
        vals = []
        for k in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            kr = None
            for r in case['k_results']:
                if r['k_level'] == k:
                    kr = r
                    break
            if kr:
                t = kr['tightness'].get(str(q), kr['tightness'].get(q, {}))
                val = t.get('P21', 0)
                vals.append(val)
                print(f" {val:<7.4f}", end="")
            else:
                vals.append(None)
                print(f" {'N/A':<7}", end="")

        # Trend analysis (skip k=0 which is always 0)
        valid = [v for v in vals[1:] if v is not None and v > 0]
        if len(valid) >= 2:
            first = valid[0]
            last = valid[-1]
            change = (last - first) / first * 100
            if abs(change) < 5:
                trend = f"FLAT ({change:+.1f}%)"
            elif change > 0:
                trend = f"UP ({change:+.1f}%)"
            else:
                trend = f"DOWN ({change:+.1f}%)"
        else:
            trend = "N/A"
        print(f" {trend}")


print("\n")
print("=" * 80)
print("TABLE C: P_k^{21} ABSOLUTE L^q NORMS vs k")
print("=" * 80)

for q in [2, 4]:
    print(f"\n--- q = {q} ---")
    print(f"{'IC':<16} {'Re':<6}", end="")
    for k in [0, 1, 2, 4, 6, 8]:
        print(f" {'k='+str(k):<10}", end="")
    print()
    print("-" * 100)

    for case in data['cases']:
        print(f"{case['ic']:<16} {case['Re']:<6}", end="")
        for k in [0, 1, 2, 4, 6, 8]:
            kr = None
            for r in case['k_results']:
                if r['k_level'] == k:
                    kr = r
                    break
            if kr:
                t = kr['tightness'].get(str(q), kr['tightness'].get(q, {}))
                val = t.get('p21_Lq', 0)
                print(f" {val:<10.4e}", end="")
            else:
                print(f" {'N/A':<10}", end="")
        print()


print("\n")
print("=" * 80)
print("TABLE D: RHS TENSOR NORMS ||f^{21}||_q vs k")
print("=" * 80)

for q in [2, 4]:
    print(f"\n--- q = {q} ---")
    print(f"{'IC':<16} {'Re':<6}", end="")
    for k in [0, 1, 2, 4, 6, 8]:
        print(f" {'k='+str(k):<10}", end="")
    print()
    print("-" * 100)

    for case in data['cases']:
        print(f"{case['ic']:<16} {case['Re']:<6}", end="")
        for k in [0, 1, 2, 4, 6, 8]:
            kr = None
            for r in case['k_results']:
                if r['k_level'] == k:
                    kr = r
                    break
            if kr:
                t = kr['tightness'].get(str(q), kr['tightness'].get(q, {}))
                val = t.get('f21_Lq', 0)
                print(f" {val:<10.4e}", end="")
            else:
                print(f" {'N/A':<10}", end="")
        print()


print("\n")
print("=" * 80)
print("CONVERGENCE CHECK: N=64 vs N=128")
print("=" * 80)

# Find TG Re=500 at N=64
n64_case = None
for case in data['cases']:
    if case['ic'] == 'taylor_green' and case['Re'] == 500 and case['N'] == 64:
        n64_case = case
        break

n128_case = data.get('convergence_check')

if n64_case and n128_case:
    print(f"\n{'k':<6}", end="")
    for q in [2, 4, 6, 8]:
        print(f" {'P21_N64(q='+str(q)+')':<16} {'P21_N128(q='+str(q)+')':<16} {'diff%':<8}", end="")
    print()
    print("-" * 140)

    for k in [1, 2, 4, 6, 8]:
        print(f"{k:<6}", end="")
        kr64 = None
        kr128 = None
        for r in n64_case['k_results']:
            if r['k_level'] == k:
                kr64 = r
                break
        for r in n128_case['k_results']:
            if r['k_level'] == k:
                kr128 = r
                break

        if kr64 and kr128:
            for q in [2, 4, 6, 8]:
                t64 = kr64['tightness'].get(str(q), kr64['tightness'].get(q, {}))
                t128 = kr128['tightness'].get(str(q), kr128['tightness'].get(q, {}))
                v64 = t64.get('P21', 0)
                v128 = t128.get('P21', 0)
                diff = (v128 - v64) / v64 * 100 if v64 > 0 else 0
                print(f" {v64:<16.4f} {v128:<16.4f} {diff:<8.2f}", end="")
        print()


# Summary statistics
print("\n")
print("=" * 80)
print("SUMMARY: P21 TIGHTNESS RATIO RANGES")
print("=" * 80)

for q in [2, 4, 6, 8]:
    all_tight = []
    for case in data['cases']:
        for kr in case['k_results']:
            if kr['k_level'] >= 1:  # skip k=0 (trivially 0)
                t = kr['tightness'].get(str(q), kr['tightness'].get(q, {}))
                val = t.get('P21', 0)
                if val > 0:
                    all_tight.append(val)

    if all_tight:
        print(f"  q={q}: min={min(all_tight):.4f}, max={max(all_tight):.4f}, "
              f"mean={sum(all_tight)/len(all_tight):.4f}, "
              f"slack=1/ratio: {1/min(all_tight):.1f}x - {1/max(all_tight):.1f}x")

# Check: does tightness depend on k or on IC?
print("\n\nVariation analysis:")
for case in data['cases']:
    for q in [2, 4]:
        vals = []
        for kr in case['k_results']:
            if kr['k_level'] >= 1:
                t = kr['tightness'].get(str(q), kr['tightness'].get(q, {}))
                val = t.get('P21', 0)
                if val > 0:
                    vals.append(val)
        if vals:
            spread = (max(vals) - min(vals)) / min(vals) * 100
            print(f"  {case['ic']:<16} Re={case['Re']:<6} q={q}: "
                  f"range [{min(vals):.4f}, {max(vals):.4f}], spread={spread:.1f}%")
