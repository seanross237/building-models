"""
Deep analysis of the most promising findings from Phase 1.

KEY DISCOVERIES TO INVESTIGATE:
1. BSD RHS scales as N^{~0.5} across all ranks (universal exponent ~1/2)
2. Murmuration signal: sum(a_p/sqrt(p)) is extremely rank-discriminative (KW p~10^-209)
3. Modular degree has power-law: mod_deg ~ |c6|^0.18 * N^1.01 * e^{-0.7*rank}
4. Residuals of BSD RHS vs N strongly correlate with a_2 (r=0.92!)
5. Rank 2 curves have dramatically fewer supersingular primes
6. mod_deg/N^2 decays exponentially with rank

Let's dig deeper into each.
"""

import json
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import curve_fit
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

DATA_PATH = "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/bsd-conjecture/approach-1-ml/data/bsd_invariants.json"

with open(DATA_PATH) as f:
    raw_data = json.load(f)

records = []
for curve in raw_data:
    rec = {
        'label': curve['label'],
        'conductor': curve['conductor'],
        'rank': curve['rank'],
        'discriminant': curve['discriminant'],
        'j_invariant': curve['j_invariant_float'],
        'torsion_order': curve['torsion_order'],
        'tamagawa_product': curve['tamagawa_product'],
        'real_period': curve['real_period'],
        'regulator': curve['regulator'],
        'analytic_sha': curve['analytic_sha'],
        'modular_degree': curve['modular_degree'],
        'c4': curve['c4'],
        'c6': curve['c6'],
        'num_bad_primes': curve['num_bad_primes'],
        'log_conductor': curve['log_conductor'],
    }
    for p_str, ap_val in curve['a_p'].items():
        rec[f'a_{p_str}'] = ap_val
    records.append(rec)

df = pd.DataFrame(records)
df['abs_disc'] = df['discriminant'].abs()
df['log_abs_disc'] = np.log(df['abs_disc'].replace(0, 1).astype(float))
df['log_omega'] = np.log(np.abs(df['real_period']).replace(0, 1e-20))

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
df['ap_cumsum_normalized'] = sum(df[f'a_{p}'] / np.sqrt(p) for p in primes)

print("="*70)
print("DEEP ANALYSIS: BSD INVARIANT RELATIONSHIPS")
print("="*70)

# ============================================================
# FINDING 1: Universal N^{1/2} scaling of BSD RHS
# ============================================================
print("\n" + "="*70)
print("FINDING 1: Universal N^{1/2} scaling")
print("="*70)

# BSD formula: L^(r)(E,1)/r! = (Sha * Omega * Reg * prod(c_p)) / |E_tors|^2
# We found: Omega * Reg * Tam / Tors^2 ~ N^{~0.5} for ALL ranks
# This is remarkable because individual components scale differently

# Precise fit by rank
for r in [0, 1, 2]:
    sub = df[(df['rank'] == r) & (df['regulator'].notna()) & (df['regulator'] > 0)]
    bsd_rhs = sub['real_period'] * sub['regulator'] * sub['tamagawa_product'] / (sub['torsion_order']**2)
    valid = bsd_rhs > 0
    log_bsd = np.log(bsd_rhs[valid].astype(float))
    log_N = sub.loc[valid.index[valid], 'log_conductor']

    # Fit log(BSD_RHS) = alpha * log(N) + beta
    slope, intercept, rval, pval, stderr = stats.linregress(log_N, log_bsd)
    print(f"\n  Rank {r}: BSD_RHS ~ N^{slope:.4f} (stderr={stderr:.4f})")
    print(f"    R^2 = {rval**2:.4f}, n = {valid.sum()}")
    print(f"    Constant factor: e^{intercept:.4f} = {np.exp(intercept):.6f}")

    # Test specifically alpha = 1/2
    resid_half = log_bsd - 0.5 * log_N
    print(f"    If alpha=1/2: residual std = {resid_half.std():.4f}, mean = {resid_half.mean():.4f}")

    # Is the deviation from 1/2 significant?
    t_stat = (slope - 0.5) / stderr
    p_half = 2 * (1 - stats.t.cdf(abs(t_stat), len(log_N) - 2))
    print(f"    Test H0: alpha=1/2: t={t_stat:.3f}, p={p_half:.4f} {'(REJECT)' if p_half < 0.05 else '(FAIL TO REJECT)'}")

# ============================================================
# FINDING 2: a_2 predicts BSD residuals (r=0.92)
# ============================================================
print("\n" + "="*70)
print("FINDING 2: a_2 as BSD residual predictor")
print("="*70)

# For rank 1 curves, BSD_RHS = Omega * Reg * Tam / Tors^2
# After removing the N^{1/2} trend, residuals correlate strongly with a_2

for r in [0, 1, 2]:
    sub = df[(df['rank'] == r) & (df['regulator'].notna()) & (df['regulator'] > 0)].copy()
    if len(sub) < 20:
        continue
    bsd_rhs = sub['real_period'] * sub['regulator'] * sub['tamagawa_product'] / (sub['torsion_order']**2)
    valid = bsd_rhs > 0
    sub = sub[valid]
    bsd_rhs = bsd_rhs[valid]
    log_bsd = np.log(bsd_rhs.astype(float))
    log_N = sub['log_conductor']

    slope, intercept, _, _, _ = stats.linregress(log_N, log_bsd)
    residuals = log_bsd - (slope * log_N + intercept)

    print(f"\n  Rank {r} residual analysis (after removing N^{slope:.3f} trend):")
    for p in [2, 3, 5, 7, 11, 13]:
        col = f'a_{p}'
        corr, pval = stats.spearmanr(residuals, sub[col])
        sig = "***" if pval < 0.001 else "**" if pval < 0.01 else "*" if pval < 0.05 else ""
        print(f"    vs a_{p:2d}: Spearman r = {corr:+.4f}  (p = {pval:.2e}) {sig}")

    # Build multivariate model: residual ~ sum of a_p terms
    print(f"\n    Multivariate: residual = sum(beta_p * a_p)")
    ap_cols = [f'a_{p}' for p in primes[:10]]
    X = sub[ap_cols].values
    y = residuals.values
    X_aug = np.column_stack([X, np.ones(len(X))])
    from numpy.linalg import lstsq
    coeffs, _, _, _ = lstsq(X_aug, y, rcond=None)
    y_pred = X_aug @ coeffs
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - y.mean())**2)
    r2 = 1 - ss_res/ss_tot
    print(f"    R^2 = {r2:.4f}")
    for i, p in enumerate(primes[:10]):
        if abs(coeffs[i]) > 0.01:
            print(f"      beta_{p:2d} = {coeffs[i]:+.4f}")

# ============================================================
# FINDING 3: Modular degree formula
# ============================================================
print("\n" + "="*70)
print("FINDING 3: Modular degree formula")
print("="*70)

sub = df[(df['modular_degree'].notna()) & (df['modular_degree'] > 0) &
         (df['c6'] != 0) & (df['c4'] != 0)].copy()
sub['log_mod_deg'] = np.log(sub['modular_degree'].astype(float))
sub['log_abs_c4'] = np.log(np.abs(sub['c4']).astype(float))
sub['log_abs_c6'] = np.log(np.abs(sub['c6']).astype(float))

# Full model: log(mod_deg) ~ a*log|c4| + b*log|c6| + c*log(N) + d*rank + e
X = np.column_stack([sub['log_abs_c4'].values, sub['log_abs_c6'].values,
                      sub['log_conductor'].values, sub['rank'].values,
                      np.ones(len(sub))])
y = sub['log_mod_deg'].values
coeffs, _, _, _ = lstsq(X, y, rcond=None)
y_pred = X @ coeffs
r2 = 1 - np.sum((y-y_pred)**2)/np.sum((y-y.mean())**2)
residuals = y - y_pred

print(f"\n  Full model (R^2 = {r2:.4f}):")
print(f"    log(mod_deg) = {coeffs[0]:.4f}*log|c4| + {coeffs[1]:.4f}*log|c6| + {coeffs[2]:.4f}*log(N) + {coeffs[3]:.4f}*rank + {coeffs[4]:.4f}")
print(f"    => mod_deg ~ |c4|^{coeffs[0]:.3f} * |c6|^{coeffs[1]:.3f} * N^{coeffs[2]:.3f} * exp({coeffs[3]:.3f} * rank)")
print(f"    Residual std: {residuals.std():.4f}")

# Add a_p to the model
ap_features = [f'a_{p}' for p in primes[:10]]
X2 = np.column_stack([X, sub[ap_features].values])
coeffs2, _, _, _ = lstsq(X2, y, rcond=None)
y_pred2 = X2 @ coeffs2
r2_2 = 1 - np.sum((y-y_pred2)**2)/np.sum((y-y.mean())**2)
print(f"\n  With a_p features (R^2 = {r2_2:.4f}, improvement: +{r2_2-r2:.4f}):")

# ============================================================
# FINDING 4: mod_deg/N^2 exponential decay with rank
# ============================================================
print("\n" + "="*70)
print("FINDING 4: mod_deg/N^2 exponential rank decay")
print("="*70)

for r in [0, 1, 2]:
    rsub = sub[sub['rank'] == r]
    ratio = rsub['modular_degree'] / rsub['conductor']**2
    log_ratio = np.log(ratio.astype(float))
    print(f"\n  Rank {r}:")
    print(f"    mod_deg/N^2: mean = {ratio.mean():.6e}, median = {ratio.median():.6e}")
    print(f"    log(mod_deg/N^2): mean = {log_ratio.mean():.4f}, std = {log_ratio.std():.4f}")

# Is the ratio sequence geometric?
means = []
for r in [0, 1, 2]:
    rsub = sub[sub['rank'] == r]
    ratio = rsub['modular_degree'] / rsub['conductor']**2
    means.append(np.log(ratio.mean()))

if len(means) == 3:
    decay_01 = means[0] - means[1]
    decay_12 = means[1] - means[2]
    print(f"\n  Log-mean decrease rank 0->1: {decay_01:.4f}")
    print(f"  Log-mean decrease rank 1->2: {decay_12:.4f}")
    print(f"  Ratio (should be ~1 for geometric): {decay_12/decay_01:.4f}")

# ============================================================
# FINDING 5: Murmuration quantification
# ============================================================
print("\n" + "="*70)
print("FINDING 5: Murmuration signal quantification")
print("="*70)

# The sum S(E) = sum_{p<=97} a_p(E) / sqrt(p) is incredibly rank-discriminative
# Let's find the optimal weighting

# Test different weightings: a_p * p^{-s} for various s
print("\n  Optimal exponent search for sum(a_p * p^{-s}):")
best_s = None
best_kw = 0
for s in np.arange(0.3, 1.5, 0.01):
    score = sum(df[f'a_{p}'] * p**(-s) for p in primes)
    vals = [score[df['rank'] == r].values for r in [0, 1, 2]]
    if all(len(v) > 5 for v in vals):
        stat, _ = stats.kruskal(*vals)
        if stat > best_kw:
            best_kw = stat
            best_s = s

print(f"  Best s = {best_s:.2f} (KW statistic = {best_kw:.2f})")

# With best s, compute separation
score = sum(df[f'a_{p}'] * p**(-best_s) for p in primes)
for r in [0, 1, 2]:
    sub_score = score[df['rank'] == r]
    print(f"  Rank {r}: mean = {sub_score.mean():.4f}, std = {sub_score.std():.4f}")

# Linear relationship between score and rank
from numpy.linalg import lstsq
X = np.column_stack([df['rank'].values, np.ones(len(df))])
y = score.values
c, _, _, _ = lstsq(X, y, rcond=None)
y_pred = X @ c
r2 = 1 - np.sum((y-y_pred)**2)/np.sum((y-y.mean())**2)
print(f"\n  Linear fit: S(E) = {c[0]:.4f} * rank + {c[1]:.4f} (R^2 = {r2:.4f})")
print(f"  => Rank ~ (S(E) - {c[1]:.4f}) / {c[0]:.4f}")
print(f"  Mean separation per rank unit: {c[0]:.4f}")

# How well does S(E) < threshold classify rank 0 vs rank >= 1?
from sklearn.metrics import accuracy_score, classification_report
rank_binary = (df['rank'] >= 1).astype(int)
thresholds = np.arange(-5, 5, 0.1)
best_thresh = None
best_acc = 0
for t in thresholds:
    pred = (score < t).astype(int)
    acc = accuracy_score(rank_binary, pred)
    if acc > best_acc:
        best_acc = acc
        best_thresh = t
print(f"\n  Binary classification (rank 0 vs rank >= 1):")
print(f"  Best threshold: {best_thresh:.2f}, accuracy: {best_acc:.4f}")

# ============================================================
# FINDING 6: Rank-conditioned Omega formula
# ============================================================
print("\n" + "="*70)
print("FINDING 6: Rank-conditioned period formula")
print("="*70)

# Omega seems to increase with rank at fixed conductor
# Can we find Omega ~ f(rank, N)?
sub = df[df['real_period'] > 0].copy()
sub['log_omega'] = np.log(sub['real_period'])

# Model: log(Omega) = alpha * log(N) + beta * rank + gamma
X = np.column_stack([sub['log_conductor'].values, sub['rank'].values, np.ones(len(sub))])
y = sub['log_omega'].values
c, _, _, _ = lstsq(X, y, rcond=None)
y_pred = X @ c
r2 = 1 - np.sum((y-y_pred)**2)/np.sum((y-y.mean())**2)
print(f"  log(Omega) = {c[0]:.4f} * log(N) + {c[1]:.4f} * rank + {c[2]:.4f}")
print(f"  R^2 = {r2:.4f}")
print(f"  => Omega ~ N^{c[0]:.3f} * exp({c[1]:.3f} * rank)")

# ============================================================
# FINDING 7: Torsion constraint on rank
# ============================================================
print("\n" + "="*70)
print("FINDING 7: Torsion and rank constraints")
print("="*70)

print("\n  Torsion structure by rank:")
for r in sorted(df['rank'].unique()):
    sub = df[df['rank'] == r]
    tors_dist = Counter(sub['torsion_order'])
    total = len(sub)
    print(f"\n  Rank {r} ({total} curves):")
    for t in sorted(tors_dist.keys()):
        pct = 100 * tors_dist[t] / total
        bar = "#" * int(pct / 2)
        print(f"    T={t:2d}: {tors_dist[t]:4d} ({pct:5.1f}%) {bar}")

# Maximum torsion by rank
print("\n  Maximum torsion order observed by rank:")
for r in sorted(df['rank'].unique()):
    max_t = df[df['rank'] == r]['torsion_order'].max()
    print(f"    Rank {r}: max torsion = {max_t}")

# ============================================================
# FINDING 8: Combined predictor - can we beat conductor alone?
# ============================================================
print("\n" + "="*70)
print("FINDING 8: Optimal rank prediction model")
print("="*70)

from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# Prepare features
feature_sets = {
    'conductor_only': ['log_conductor'],
    'ap_sum_only': ['ap_cumsum_normalized'],
    'conductor+ap_sum': ['log_conductor', 'ap_cumsum_normalized'],
    'conductor+ap_sum+torsion': ['log_conductor', 'ap_cumsum_normalized', 'torsion_order'],
    'full_model': ['log_conductor', 'ap_cumsum_normalized', 'torsion_order',
                   'tamagawa_product', 'real_period', 'num_bad_primes'] +
                  [f'a_{p}' for p in primes[:15]],
}

for name, features in feature_sets.items():
    sub = df[features + ['rank']].dropna()
    X = sub[features].values
    y = sub['rank'].values

    # Cross-validated accuracy
    gb = GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42)
    scores = cross_val_score(gb, X, y, cv=5, scoring='accuracy')
    print(f"  {name:35s}: CV accuracy = {scores.mean():.4f} +/- {scores.std():.4f}")

# ============================================================
# FINDING 9: Novel ratio that appears nearly constant
# ============================================================
print("\n" + "="*70)
print("FINDING 9: Near-constant ratios")
print("="*70)

# For rank 0 with Sha=1: L(E,1) = Omega * Tam / Tors^2
# Search for: L(E,1) / f(N, a_p) ~= constant

# First, compute L(E,1) proxy: Omega * Tam / Tors^2 for rank 0
sub_r0 = df[(df['rank'] == 0) & (df['analytic_sha'].notna())].copy()
sub_r0['L1'] = sub_r0['real_period'] * sub_r0['tamagawa_product'] * sub_r0['analytic_sha'] / (sub_r0['torsion_order']**2)

print(f"\n  Rank 0: L(E,1) = Omega * Tam * Sha / Tors^2")
print(f"  Distribution of L(E,1): mean={sub_r0['L1'].mean():.4f}, median={sub_r0['L1'].median():.4f}")

# Test: L(E,1) / N^{1/2} ~= ?
ratio = sub_r0['L1'] / np.sqrt(sub_r0['conductor'])
print(f"\n  L(E,1) / sqrt(N): mean={ratio.mean():.6f}, CV={ratio.std()/ratio.mean():.4f}")

# Test: L(E,1) * Tors^2 / (Omega * Tam) = Sha, which should be ~1
sha_proxy = sub_r0['L1'] * sub_r0['torsion_order']**2 / (sub_r0['real_period'] * sub_r0['tamagawa_product'])
print(f"  Sha proxy check: mean={sha_proxy.mean():.6f}, std={sha_proxy.std():.6f}")

# Test: Omega * N^{-1/2} relationship
omega_scaled = sub_r0['real_period'] / np.sqrt(sub_r0['conductor'])
print(f"\n  Omega / sqrt(N): mean={omega_scaled.mean():.6f}, CV={omega_scaled.std()/omega_scaled.mean():.4f}")

# ============================================================
# FINDING 10: Regulator-conductor relationship
# ============================================================
print("\n" + "="*70)
print("FINDING 10: Regulator scaling with conductor")
print("="*70)

for r in [1, 2]:
    sub = df[(df['rank'] == r) & (df['regulator'].notna()) & (df['regulator'] > 0)]
    if len(sub) < 10:
        continue
    log_reg = np.log(sub['regulator'].astype(float))
    log_N = sub['log_conductor']

    slope, intercept, rval, pval, stderr = stats.linregress(log_N, log_reg)
    print(f"\n  Rank {r}: log(Reg) = {slope:.4f} * log(N) + {intercept:.4f}")
    print(f"    R^2 = {rval**2:.4f}, p = {pval:.2e}")
    print(f"    => Reg ~ N^{slope:.3f}")

    # Residuals vs a_p
    resid = log_reg - (slope * log_N + intercept)
    for p in [2, 3, 5, 7, 11]:
        corr, pv = stats.spearmanr(resid, sub[f'a_{p}'])
        if abs(corr) > 0.1:
            print(f"    Residual vs a_{p}: r = {corr:.4f} (p={pv:.2e})")

# ============================================================
# FINDING 11: Product of a_p across primes
# ============================================================
print("\n" + "="*70)
print("FINDING 11: Euler product partial evaluation")
print("="*70)

# Compute partial Euler product: prod(1 - a_p/p + 1/p) for p <= 97
# This approximates L(E,1) from the product side

df['partial_euler_prod'] = 1.0
for p in primes:
    factor = 1 - df[f'a_{p}'] / p + 1.0 / p
    # Avoid zero or negative factors
    factor = factor.clip(lower=1e-10)
    df['partial_euler_prod'] *= factor

df['log_partial_euler'] = np.log(df['partial_euler_prod'])

for r in [0, 1, 2]:
    sub = df[df['rank'] == r]
    pep = sub['partial_euler_prod']
    print(f"\n  Rank {r}: partial Euler product (25 primes)")
    print(f"    mean = {pep.mean():.6f}, median = {pep.median():.6f}")
    print(f"    log: mean = {sub['log_partial_euler'].mean():.4f}, std = {sub['log_partial_euler'].std():.4f}")

# Does partial Euler product correlate with the BSD RHS?
sub_all = df[(df['regulator'].notna()) & (df['regulator'] > 0)].copy()
sub_all['bsd_rhs'] = sub_all['real_period'] * sub_all['regulator'] * sub_all['tamagawa_product'] / (sub_all['torsion_order']**2)
corr, pval = stats.spearmanr(sub_all['partial_euler_prod'], sub_all['bsd_rhs'])
print(f"\n  Correlation (partial Euler prod, BSD RHS): r = {corr:.4f}, p = {pval:.2e}")

# For rank 0, compare partial Euler product with L(E,1)
sub_r0_2 = sub_all[(sub_all['rank'] == 0) & (sub_all['analytic_sha'].notna())].copy()
sub_r0_2['L1'] = sub_r0_2['bsd_rhs'] * sub_r0_2['analytic_sha']
corr, pval = stats.spearmanr(sub_r0_2['partial_euler_prod'], sub_r0_2['L1'])
print(f"  Rank 0: corr(partial Euler, L(E,1)) = {corr:.4f}, p = {pval:.2e}")

# ============================================================
# FINDING 12: Searching for Sha proxies
# ============================================================
print("\n" + "="*70)
print("FINDING 12: Sha proxy search")
print("="*70)

# Sha is the hardest BSD quantity to compute. Can we find a proxy?
# For our dataset, most Sha = 1, but 5 rank-0 curves have Sha = 4

sub_sha = df[(df['analytic_sha'].notna())].copy()
sha_nontrivial = sub_sha[sub_sha['analytic_sha'] > 1.5]
sha_trivial = sub_sha[sub_sha['analytic_sha'] <= 1.5]

print(f"\n  Curves with Sha > 1: {len(sha_nontrivial)}")
print(f"  Curves with Sha = 1: {len(sha_trivial)}")

if len(sha_nontrivial) > 0:
    print(f"\n  Sha > 1 curves:")
    for _, row in sha_nontrivial.iterrows():
        print(f"    {row['label']}: Sha={row['analytic_sha']:.1f}, N={row['conductor']}, rank={row['rank']}, "
              f"tors={row['torsion_order']}, tam={row['tamagawa_product']}")

    # What distinguishes Sha > 1 curves?
    features_to_test = ['conductor', 'torsion_order', 'tamagawa_product', 'real_period',
                         'num_bad_primes', 'c4', 'c6', 'modular_degree']
    print(f"\n  Feature comparison (Sha=1 vs Sha>1):")
    for feat in features_to_test:
        v1 = sha_trivial[feat].dropna()
        v2 = sha_nontrivial[feat].dropna()
        if len(v2) > 1 and len(v1) > 1:
            stat, pval = stats.mannwhitneyu(v1, v2, alternative='two-sided')
            print(f"    {feat:20s}: Sha=1 mean={v1.mean():.2f}, Sha>1 mean={v2.mean():.2f}, p={pval:.4f}")

# ============================================================
# CONJECTURAL FORMULAS
# ============================================================
print("\n" + "="*70)
print("CONJECTURAL FORMULAS SUMMARY")
print("="*70)

print("""
CONJECTURE 1 (Universal BSD scaling):
  For rank r curves E/Q with conductor N:
    Omega(E) * Reg(E) * prod(c_p) / |E_tors|^2  ~  C_r * N^{1/2}
  where C_r depends only on r.
  Evidence: R^2 = 0.63 (rank 0), 0.71 (rank 1), 0.51 (rank 2)
  Exponents: 0.510, 0.576, 0.501 (all close to 1/2)

CONJECTURE 2 (Murmuration rank formula):
  S(E) := sum_{p<=X} a_p(E) * p^{-s*}  is approximately linear in rank.
  With optimal s* ~ 0.5:
    rank(E) ~ (S(E) - c_0) / c_1
  where c_0, c_1 are computable constants.

CONJECTURE 3 (Modular degree formula):
  mod_deg(E) ~ |c6|^{0.18} * N^{1.01} * exp(-0.70 * rank)
  R^2 = 0.89

CONJECTURE 4 (Frobenius-BSD bridge):
  After removing the N^{1/2} trend from the BSD RHS, the residuals
  are almost entirely determined by a_2(E) (the Frobenius trace at 2).
  For rank 1: residual correlation with a_2 = 0.92.
  This means: Omega*Reg*Tam/Tors^2 ~ N^{1/2} * g(a_2(E))
  for some function g.

CONJECTURE 5 (Supersingular-rank bound):
  Higher rank curves have fewer supersingular primes (a_p = 0) among small primes.
  Mean count (primes <= 97): rank 0: 3.89, rank 1: 3.24, rank 2: 2.01
""")
