#!/usr/bin/env python3
"""
Phase 3: Run heavy statistical analysis on Modal cloud compute.
"""

import sys
sys.path.insert(0, "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/modal")
from run_remote import remote_heavy
import json
import os

SYNTH_DIR = "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/bsd-conjecture/synthesis-ml-statmech"
ML_DATA = "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/bsd-conjecture/approach-1-ml/data/bsd_invariants.json"


def load_data():
    ext_path = os.path.join(SYNTH_DIR, 'extended_dataset.json')
    if os.path.exists(ext_path):
        with open(ext_path) as f:
            data = json.load(f)
        if len(data) > 100:
            return data, 'extended'
    with open(ML_DATA) as f:
        return json.load(f), 'original'


def run_prediction_tests():
    data, source = load_data()
    print(f"Loaded {len(data)} curves from {source} dataset")
    data_json = json.dumps(data)

    script = '''
import numpy as np
from scipy import stats
import json
import math

data = json.loads(ARGS["data_json"])
print(f"Loaded {len(data)} curves")

by_rank = {}
for c in data:
    r = c['rank']
    if r not in by_rank:
        by_rank[r] = []
    by_rank[r].append(c)

for r in sorted(by_rank.keys()):
    print(f"  Rank {r}: {len(by_rank[r])} curves")

sample_curve = data[0]
primes_available = sorted([int(p) for p in sample_curve['a_p'].keys()])
print(f"Primes: {len(primes_available)} (max {max(primes_available)})")

# =================================================================
# TEST 1: beta_p power law
# =================================================================
print("\\n" + "=" * 60)
print("TEST 1: beta_p Power Law")
print("=" * 60)

rank1 = by_rank.get(1, [])
beta_p_fitted = {}
if rank1:
    n = len(rank1)
    y_vals = []
    X_vals = []
    for c in rank1:
        bsd = c['real_period'] * c['regulator'] * c['tamagawa_product'] / c['torsion_order']**2
        if bsd <= 0:
            continue
        y_vals.append(math.log(bsd) - 0.5 * math.log(c['conductor']))
        row = [c['a_p'].get(str(p), 0) for p in primes_available]
        X_vals.append(row)

    y = np.array(y_vals)
    X = np.array(X_vals)
    X = np.column_stack([X, np.ones(len(y))])
    beta_hat, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    beta_p_fitted = {p: float(beta_hat[i]) for i, p in enumerate(primes_available)}
    intercept = float(beta_hat[-1])

    y_pred = X @ beta_hat
    ss_res = float(np.sum((y - y_pred)**2))
    ss_tot = float(np.sum((y - np.mean(y))**2))
    r2 = 1 - ss_res/ss_tot
    print(f"  R^2 = {r2:.6f}, intercept C_1 = {intercept:.6f}")

    print("\\n  Fitted beta_p:")
    for p in primes_available[:30]:
        print(f"    p={p:>3d}: beta={beta_p_fitted[p]:>10.6f}, 1/p={1/p:>10.6f}, 1/(p+1)={1/(p+1):>10.6f}")

    # Power law fit: |delta_p| = |beta_p - 1/p| ~ A / p^B
    delta_p = {p: beta_p_fitted[p] - 1/p for p in primes_available}
    fit_p = [p for p in primes_available if p >= 3]
    fit_d = [abs(delta_p[p]) for p in fit_p]
    log_p = np.log(np.array(fit_p, dtype=float))
    log_d = np.log(np.array(fit_d))
    mask = np.isfinite(log_d)
    if mask.sum() > 3:
        sl, it, rv, pv, se = stats.linregress(log_p[mask], log_d[mask])
        print(f"\\n  |delta_p| ~ {math.exp(it):.4f} / p^{-sl:.4f}  (R^2={rv**2:.4f})")
        print(f"  Original: ~0.61 / p^0.80")

    # Direct beta_p fit
    fit_p2 = [p for p in primes_available if p >= 2]
    fit_b2 = [abs(beta_p_fitted[p]) for p in fit_p2]
    log_p2 = np.log(np.array(fit_p2, dtype=float))
    log_b2 = np.log(np.array(fit_b2))
    mask2 = np.isfinite(log_b2)
    if mask2.sum() > 3:
        sl2, it2, rv2, _, _ = stats.linregress(log_p2[mask2], log_b2[mask2])
        print(f"  |beta_p| ~ {math.exp(it2):.4f} / p^{-sl2:.4f}  (R^2={rv2**2:.4f})")
        print(f"  Original: ~3.6 / p^4.2")

    # KEY: Compare with 1/(p+1)
    print("\\n  Comparison with 1/(p+1):")
    for p in primes_available[:15]:
        print(f"    p={p:>3d}: beta_BSD={beta_p_fitted[p]:>10.6f}, 1/(p+1)={1/(p+1):>10.6f}, "
              f"diff={beta_p_fitted[p]-1/(p+1):>10.6f}")

# =================================================================
# TEST 2: C_r values
# =================================================================
print("\\n" + "=" * 60)
print("TEST 2: C_r")
print("=" * 60)
Cr = {}
for rv in sorted(by_rank.keys()):
    curves = by_rank[rv]
    vals = []
    for c in curves:
        bsd = c['real_period'] * c['regulator'] * c['tamagawa_product'] / c['torsion_order']**2
        if bsd > 0:
            vals.append(math.log(bsd) - 0.5 * math.log(c['conductor']))
    if vals:
        Cr[rv] = float(np.mean(vals))
        print(f"  Rank {rv}: C_r = {np.mean(vals):.4f} +/- {np.std(vals):.4f} (n={len(vals)})")

if len(Cr) >= 2:
    rr = np.array(list(Cr.keys()), dtype=float)
    cc = np.array(list(Cr.values()))
    sl, it, rv, _, _ = stats.linregress(rr, cc)
    print(f"\\n  C_r = {it:.4f} + {sl:.4f}*r  (R^2={rv**2:.4f})")
    print(f"  per-rank factor: exp({sl:.4f}) = {math.exp(sl):.4f}")
    print(f"  Original: C_r = -2.21 - 0.39*r, factor=0.68")

# =================================================================
# TEST 3: Murmuration sum
# =================================================================
print("\\n" + "=" * 60)
print("TEST 3: Murmuration S(E)")
print("=" * 60)

primes_25 = primes_available[:25]
S_by_rank = {}
for c in data:
    r = c['rank']
    N = c['conductor']
    S = sum(c['a_p'].get(str(p), 0) * p**(-0.84) for p in primes_25 if N % p != 0)
    S_by_rank.setdefault(r, []).append(S)

for r in sorted(S_by_rank.keys()):
    v = S_by_rank[r]
    print(f"  Rank {r}: mean={np.mean(v):.4f}, std={np.std(v):.4f}, n={len(v)}")

# Binary classification
r0S = S_by_rank.get(0, [])
r1S = []
for r in S_by_rank:
    if r >= 1:
        r1S.extend(S_by_rank[r])

best_acc = 0
best_thresh = 0
if r0S and r1S:
    all_S = [(s, 0) for s in r0S] + [(s, 1) for s in r1S]
    all_S.sort()
    for i in range(len(all_S)-1):
        t = (all_S[i][0] + all_S[i+1][0]) / 2
        corr = sum(1 for s, r in all_S if (s >= t and r == 0) or (s < t and r >= 1))
        a = corr / len(all_S)
        if a > best_acc:
            best_acc = a
            best_thresh = t

    acc_orig = sum(1 for s, r in all_S if (s >= -0.80 and r == 0) or (s < -0.80 and r >= 1)) / len(all_S)
    print(f"\\n  Binary (0 vs >=1): best={best_acc:.4f} at t={best_thresh:.4f}, orig(-0.80)={acc_orig:.4f}")

    rg = [np.array(S_by_rank[r]) for r in sorted(S_by_rank.keys()) if len(S_by_rank[r]) > 1]
    if len(rg) >= 2:
        H, pv = stats.kruskal(*rg)
        print(f"  Kruskal-Wallis H={H:.1f}, p={pv:.2e}")

# =================================================================
# TEST 4: Running coupling
# =================================================================
print("\\n" + "=" * 60)
print("TEST 4: Running Coupling")
print("=" * 60)

# Compute from a_p data (partial L-function up to p=97)
primes_97 = [p for p in primes_available if p <= 97]
Lambda_test = 97

g_by_rank = {}
for c in data:
    r = c['rank']
    N = c['conductor']
    log_L = 0.0
    for p in primes_97:
        ap = c['a_p'].get(str(p), 0)
        is_bad = (N % p == 0)
        if is_bad:
            denom = 1 - float(ap)/p
        else:
            denom = 1 - float(ap)/p + 1.0/p
        if abs(denom) > 1e-50:
            log_L += -math.log(abs(denom))
    g = log_L / math.log(Lambda_test)
    g_by_rank.setdefault(r, []).append(g)

print(f"  g(Lambda={Lambda_test}) statistics:")
for r in sorted(g_by_rank.keys()):
    v = g_by_rank[r]
    print(f"    Rank {r}: mean={np.mean(v):.6f}, std={np.std(v):.6f}, n={len(v)}")

for r1, r2 in [(0, 1), (0, 2), (1, 2)]:
    if r1 in g_by_rank and r2 in g_by_rank:
        m1, m2 = np.mean(g_by_rank[r1]), np.mean(g_by_rank[r2])
        s1, s2 = np.std(g_by_rank[r1], ddof=1), np.std(g_by_rank[r2], ddof=1)
        pooled = math.sqrt((s1**2 + s2**2) / 2)
        d = abs(m1 - m2) / pooled if pooled > 0 else float('inf')
        print(f"    Rank {r1} vs {r2}: Cohen d = {d:.2f}")

# Also with Lambda = max available prime
if max(primes_available) > 97:
    Lambda_ext = max(primes_available)
    g_by_rank_ext = {}
    for c in data:
        r = c['rank']
        N = c['conductor']
        log_L = 0.0
        for p in primes_available:
            ap = c['a_p'].get(str(p), 0)
            is_bad = (N % p == 0)
            if is_bad:
                denom = 1 - float(ap)/p
            else:
                denom = 1 - float(ap)/p + 1.0/p
            if abs(denom) > 1e-50:
                log_L += -math.log(abs(denom))
        g = log_L / math.log(Lambda_ext)
        g_by_rank_ext.setdefault(r, []).append(g)

    print(f"\\n  g(Lambda={Lambda_ext}) statistics:")
    for r in sorted(g_by_rank_ext.keys()):
        v = g_by_rank_ext[r]
        print(f"    Rank {r}: mean={np.mean(v):.6f}, std={np.std(v):.6f}, n={len(v)}")

    for r1, r2 in [(0, 1), (0, 2), (1, 2)]:
        if r1 in g_by_rank_ext and r2 in g_by_rank_ext:
            m1, m2 = np.mean(g_by_rank_ext[r1]), np.mean(g_by_rank_ext[r2])
            s1, s2 = np.std(g_by_rank_ext[r1], ddof=1), np.std(g_by_rank_ext[r2], ddof=1)
            pooled = math.sqrt((s1**2 + s2**2) / 2)
            d = abs(m1 - m2) / pooled if pooled > 0 else float('inf')
            print(f"    Rank {r1} vs {r2}: Cohen d = {d:.2f}")

# =================================================================
# TEST 5: Sha > 1
# =================================================================
print("\\n" + "=" * 60)
print("TEST 5: Sha > 1")
print("=" * 60)
sha_gt1 = [c for c in data if abs(c['analytic_sha'] - 1) > 0.01]
print(f"  Sha > 1 curves: {len(sha_gt1)}")
for c in sha_gt1[:15]:
    bsd = c['real_period'] * c['regulator'] * c['tamagawa_product'] / c['torsion_order']**2
    print(f"    {c['label']}: r={c['rank']}, N={c['conductor']}, Sha={c['analytic_sha']:.2f}, BSD={bsd:.6f}")

# =================================================================
# TEST 6: 5-Fold CV
# =================================================================
print("\\n" + "=" * 60)
print("TEST 6: 5-Fold CV")
print("=" * 60)

for rv in [0, 1, 2]:
    curves = by_rank.get(rv, [])
    if len(curves) < 20:
        continue
    y = []
    X = []
    for c in curves:
        bsd = c['real_period'] * c['regulator'] * c['tamagawa_product'] / c['torsion_order']**2
        if bsd <= 0:
            continue
        y.append(math.log(bsd) - 0.5 * math.log(c['conductor']))
        X.append([c['a_p'].get(str(p), 0) for p in primes_available])
    y = np.array(y)
    X = np.column_stack([np.array(X), np.ones(len(y))])
    n = len(y)
    indices = np.arange(n)
    np.random.seed(42)
    np.random.shuffle(indices)
    folds = np.array_split(indices, 5)
    r2s = []
    for f in range(5):
        test = folds[f]
        train = np.concatenate([folds[j] for j in range(5) if j != f])
        b, _, _, _ = np.linalg.lstsq(X[train], y[train], rcond=None)
        yp = X[test] @ b
        ss_r = float(np.sum((y[test] - yp)**2))
        ss_t = float(np.sum((y[test] - np.mean(y[test]))**2))
        r2s.append(1 - ss_r/ss_t if ss_t > 0 else 0)
    print(f"  Rank {rv}: CV R^2 = {np.mean(r2s):.4f} +/- {np.std(r2s):.4f}")

# =================================================================
# TEST 7: Euler beta comparison
# =================================================================
print("\\n" + "=" * 60)
print("TEST 7: Euler 1/(p+1) Test")
print("=" * 60)
if rank1:
    for p in primes_available[:15]:
        ap_v = []
        le_v = []
        for c in rank1:
            ap = c['a_p'].get(str(p), 0)
            N = c['conductor']
            is_bad = (N % p == 0)
            denom = (1 - float(ap)/p) if is_bad else (1 - float(ap)/p + 1.0/p)
            if abs(denom) > 1e-50:
                ap_v.append(float(ap))
                le_v.append(-math.log(abs(denom)))
        a = np.array(ap_v)
        l = np.array(le_v)
        if len(a) > 10 and np.var(a) > 0:
            be = float(np.cov(a, l)[0,1] / np.var(a))
            print(f"  p={p:>3d}: beta_Euler={be:.6f}, 1/(p+1)={1/(p+1):.6f}, ratio={be*(p+1):.4f}")

# Return only plain Python types (no numpy!)
RESULTS["status"] = "complete"
RESULTS["n_curves"] = len(data)
RESULTS["r2_rank1"] = float(r2) if 'r2' in dir() else 0
print("\\nDone.")
'''

    print("Sending analysis to Modal...")
    result = remote_heavy(script, args={"data_json": data_json})

    if result.get("error"):
        print(f"MODAL ERROR:\n{result['error']}")
    if result.get("stdout"):
        print("\n=== MODAL OUTPUT ===")
        print(result["stdout"])

    # Save stdout
    output_path = os.path.join(SYNTH_DIR, 'modal_output.txt')
    with open(output_path, 'w') as f:
        f.write(result.get("stdout", ""))
        if result.get("error"):
            f.write(f"\n\nERROR:\n{result['error']}")
    print(f"\nOutput saved to {output_path}")

    return result


if __name__ == '__main__':
    run_prediction_tests()
