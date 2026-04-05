"""
BSD Conjecture ML Analysis Pipeline
====================================
Phase 1: Exploratory data analysis - look for correlations and patterns
Phase 2: Symbolic regression to find closed-form relationships
Phase 3: Focus on rank >= 2 and Sha prediction

Run with: python3 analyze_bsd.py
"""

import json
import numpy as np
import pandas as pd
from scipy import stats
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# LOAD DATA
# ============================================================
DATA_PATH = "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/bsd-conjecture/approach-1-ml/data/bsd_invariants.json"

with open(DATA_PATH) as f:
    raw_data = json.load(f)

print(f"Loaded {len(raw_data)} elliptic curves")

# Build DataFrame
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
    # Add a_p values as separate columns
    for p_str, ap_val in curve['a_p'].items():
        rec[f'a_{p_str}'] = ap_val
    # Add ainvs
    for i, a in enumerate(curve['ainvs']):
        rec[f'a{i+1}'] = a
    records.append(rec)

df = pd.DataFrame(records)

# Derived features
df['abs_disc'] = df['discriminant'].abs()
df['log_abs_disc'] = np.log(df['abs_disc'].replace(0, 1).astype(float))
df['disc_sign'] = np.sign(df['discriminant'])
df['log_tamagawa'] = np.log(df['tamagawa_product'].astype(float))
df['log_torsion'] = np.log(df['torsion_order'].astype(float))
df['log_omega'] = np.log(np.abs(df['real_period']).replace(0, 1e-20))
df['log_regulator'] = np.where(df['regulator'] > 0, np.log(df['regulator']), np.nan)
df['log_mod_deg'] = np.where(df['modular_degree'] > 0, np.log(df['modular_degree'].astype(float)), np.nan)

# BSD leading coefficient components (for rank 0)
# L(E,1) = (Sha * Omega * Reg * prod(c_p)) / |E_tors|^2
# For rank 0: L(E,1) = (Sha * Omega * prod(c_p)) / torsion_order^2
df['bsd_rhs_no_sha'] = (df['real_period'] * df['tamagawa_product'] * df['regulator']) / (df['torsion_order']**2)

# ============================================================
# PHASE 1: EXPLORATORY ANALYSIS
# ============================================================
print("\n" + "="*70)
print("PHASE 1: EXPLORATORY DATA ANALYSIS")
print("="*70)

print(f"\nRank distribution:")
for r, count in sorted(Counter(df['rank']).items()):
    print(f"  Rank {r}: {count} curves")

print(f"\nBasic statistics by rank:")
for r in sorted(df['rank'].unique()):
    sub = df[df['rank'] == r]
    print(f"\n  Rank {r} ({len(sub)} curves):")
    print(f"    Conductor: mean={sub['conductor'].mean():.1f}, median={sub['conductor'].median():.1f}")
    print(f"    |Discriminant|: mean={sub['abs_disc'].mean():.1f}, median={sub['abs_disc'].median():.1f}")
    print(f"    Torsion order: {dict(Counter(sub['torsion_order']))}")
    print(f"    Tamagawa product: mean={sub['tamagawa_product'].mean():.2f}, median={sub['tamagawa_product'].median():.2f}")
    print(f"    Real period: mean={sub['real_period'].mean():.4f}, median={sub['real_period'].median():.4f}")
    if r > 0:
        reg_data = sub['regulator'].dropna()
        if len(reg_data) > 0:
            print(f"    Regulator: mean={reg_data.mean():.4f}, median={reg_data.median():.4f}")
    sha_data = sub['analytic_sha'].dropna()
    if len(sha_data) > 0:
        print(f"    Analytic Sha: {dict(Counter(sha_data.round(2)))}")
    print(f"    Num bad primes: mean={sub['num_bad_primes'].mean():.2f}")
    moddeg = sub['modular_degree'].dropna()
    if len(moddeg) > 0:
        print(f"    Modular degree: mean={moddeg.mean():.1f}, median={moddeg.median():.1f}")

# ============================================================
# CORRELATION ANALYSIS
# ============================================================
print("\n" + "="*70)
print("CORRELATION ANALYSIS")
print("="*70)

# Key correlations with rank
numeric_cols = ['conductor', 'log_conductor', 'abs_disc', 'log_abs_disc',
                'torsion_order', 'tamagawa_product', 'real_period',
                'num_bad_primes', 'c4', 'c6', 'log_omega',
                'log_tamagawa', 'log_torsion']

# Add a_p columns
ap_cols = [c for c in df.columns if c.startswith('a_')]
numeric_cols.extend(ap_cols)

print("\nCorrelation with rank (Spearman):")
correlations = []
for col in numeric_cols:
    valid = df[['rank', col]].dropna()
    if len(valid) > 10:
        corr, pval = stats.spearmanr(valid['rank'], valid[col])
        correlations.append((col, corr, pval))

correlations.sort(key=lambda x: abs(x[1]), reverse=True)
for col, corr, pval in correlations[:25]:
    sig = "***" if pval < 0.001 else "**" if pval < 0.01 else "*" if pval < 0.05 else ""
    print(f"  {col:25s}: r={corr:+.4f}  p={pval:.2e} {sig}")

# ============================================================
# RANK DISCRIMINATION: What features best separate ranks?
# ============================================================
print("\n" + "="*70)
print("RANK DISCRIMINATION ANALYSIS")
print("="*70)

# Compare rank 0 vs rank 1 vs rank 2
for feature in ['log_conductor', 'log_abs_disc', 'torsion_order', 'tamagawa_product',
                'real_period', 'num_bad_primes', 'log_omega']:
    vals_by_rank = {}
    for r in [0, 1, 2]:
        sub = df[df['rank'] == r][feature].dropna()
        vals_by_rank[r] = sub

    if all(len(v) > 5 for v in vals_by_rank.values()):
        # KW test (non-parametric ANOVA)
        stat, p = stats.kruskal(*vals_by_rank.values())
        print(f"\n  {feature}:")
        for r in [0, 1, 2]:
            v = vals_by_rank[r]
            print(f"    Rank {r}: mean={v.mean():.4f}, std={v.std():.4f}, n={len(v)}")
        print(f"    Kruskal-Wallis H={stat:.2f}, p={p:.2e}")

# ============================================================
# a_p PATTERN ANALYSIS (Murmuration-related)
# ============================================================
print("\n" + "="*70)
print("FROBENIUS TRACE (a_p) ANALYSIS")
print("="*70)

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

print("\nMean a_p by rank:")
print(f"  {'p':>5s}", end="")
for r in [0, 1, 2]:
    print(f"  rank_{r:d}", end="")
print(f"  r0-r1_diff  r0-r2_diff")

for p in primes:
    col = f'a_{p}'
    means = {}
    for r in [0, 1, 2]:
        sub = df[df['rank'] == r][col].dropna()
        means[r] = sub.mean()
    diff01 = means[0] - means[1]
    diff02 = means[0] - means[2]
    print(f"  {p:5d}  {means[0]:+7.3f}  {means[1]:+7.3f}  {means[2]:+7.3f}  {diff01:+8.3f}    {diff02:+8.3f}")

# Normalized a_p: a_p / (2*sqrt(p)) -- Sato-Tate normalized
print("\nNormalized a_p / (2*sqrt(p)) mean by rank:")
for p in primes[:10]:
    col = f'a_{p}'
    norm = 2 * np.sqrt(p)
    for r in [0, 1, 2]:
        sub = df[df['rank'] == r][col].dropna()
        mean_norm = (sub / norm).mean()
    # Check if a_p = 0 frequency varies by rank (related to supersingular reduction)
    for r in [0, 1, 2]:
        sub = df[df['rank'] == r][col]
        frac_zero = (sub == 0).mean()

# Cumulative a_p sum as rank predictor
print("\nCumulative sum of a_p / sqrt(p) by rank (key murmuration signal):")
df['ap_cumsum_normalized'] = 0
for p in primes:
    col = f'a_{p}'
    df['ap_cumsum_normalized'] += df[col] / np.sqrt(p)

for r in [0, 1, 2]:
    sub = df[df['rank'] == r]['ap_cumsum_normalized']
    print(f"  Rank {r}: mean={sub.mean():.4f}, std={sub.std():.4f}")

stat, p = stats.kruskal(
    df[df['rank'] == 0]['ap_cumsum_normalized'],
    df[df['rank'] == 1]['ap_cumsum_normalized'],
    df[df['rank'] == 2]['ap_cumsum_normalized']
)
print(f"  Kruskal-Wallis: H={stat:.2f}, p={p:.2e}")

# ============================================================
# NOVEL RELATIONSHIP SEARCH
# ============================================================
print("\n" + "="*70)
print("NOVEL RELATIONSHIP SEARCH")
print("="*70)

# Idea 1: Does Omega * Reg have a simpler relationship with conductor than BSD predicts?
print("\n--- Omega * Regulator vs Conductor ---")
for r in [0, 1, 2]:
    sub = df[(df['rank'] == r) & (df['regulator'].notna()) & (df['regulator'] > 0)]
    if len(sub) < 5:
        continue
    omega_reg = sub['real_period'] * sub['regulator']
    log_or = np.log(omega_reg)
    log_N = sub['log_conductor']
    slope, intercept, rval, pval, stderr = stats.linregress(log_N, log_or)
    print(f"  Rank {r}: log(Omega*Reg) ~ {slope:.4f} * log(N) + {intercept:.4f}  (R^2={rval**2:.4f}, n={len(sub)})")

# Idea 2: Tamagawa product as function of conductor factorization
print("\n--- Tamagawa product vs conductor structure ---")
for r in [0, 1, 2]:
    sub = df[df['rank'] == r]
    corr, pval = stats.spearmanr(sub['tamagawa_product'], sub['num_bad_primes'])
    print(f"  Rank {r}: corr(tamagawa, num_bad_primes) = {corr:.4f} (p={pval:.2e})")

# Idea 3: Modular degree scaling
print("\n--- Modular degree scaling ---")
for r in [0, 1, 2]:
    sub = df[(df['rank'] == r) & (df['modular_degree'].notna()) & (df['modular_degree'] > 0)]
    if len(sub) < 5:
        continue
    log_md = np.log(sub['modular_degree'].astype(float))
    log_N = sub['log_conductor']
    slope, intercept, rval, pval, stderr = stats.linregress(log_N, log_md)
    print(f"  Rank {r}: log(mod_deg) ~ {slope:.4f} * log(N) + {intercept:.4f}  (R^2={rval**2:.4f}, n={len(sub)})")

# Idea 4: BSD RHS (without Sha) vs conductor -- does this scale differently by rank?
print("\n--- BSD RHS (no Sha) vs conductor ---")
for r in [0, 1, 2]:
    sub = df[(df['rank'] == r) & (df['bsd_rhs_no_sha'].notna()) & (df['bsd_rhs_no_sha'] > 0)]
    if len(sub) < 5:
        continue
    log_bsd = np.log(sub['bsd_rhs_no_sha'].astype(float))
    log_N = sub['log_conductor']
    slope, intercept, rval, pval, stderr = stats.linregress(log_N, log_bsd)
    print(f"  Rank {r}: log(Omega*Reg*Tam/Tors^2) ~ {slope:.4f} * log(N) + {intercept:.4f}  (R^2={rval**2:.4f})")

# Idea 5: Sha distribution
print("\n--- Sha distribution by rank ---")
for r in [0, 1, 2]:
    sub = df[(df['rank'] == r) & (df['analytic_sha'].notna())]
    if len(sub) == 0:
        continue
    sha_vals = sub['analytic_sha'].round(1)
    sha_dist = Counter(sha_vals)
    print(f"  Rank {r}: Sha values = {dict(sorted(sha_dist.items())[:10])}")
    sha_gt1 = (sub['analytic_sha'] > 1.5).sum()
    print(f"    Sha > 1: {sha_gt1}/{len(sub)} ({100*sha_gt1/len(sub):.1f}%)")

# Idea 6: Can we predict Sha from other invariants?
print("\n--- Sha prediction from other invariants ---")
sub = df[(df['analytic_sha'].notna()) & (df['analytic_sha'] > 0)]
sha = sub['analytic_sha']
for feature in ['conductor', 'log_conductor', 'torsion_order', 'tamagawa_product',
                'real_period', 'num_bad_primes', 'c4', 'c6']:
    vals = sub[feature].dropna()
    common_idx = sha.index.intersection(vals.index)
    if len(common_idx) > 10:
        corr, pval = stats.spearmanr(sha.loc[common_idx], vals.loc[common_idx])
        sig = "***" if pval < 0.001 else "**" if pval < 0.01 else "*" if pval < 0.05 else ""
        print(f"  Sha vs {feature:20s}: r={corr:+.4f}  p={pval:.2e} {sig}")

# Idea 7: Composite score for rank classification
print("\n--- Composite rank discriminator ---")
# Build: sign * sum(a_p / sqrt(p)) + alpha * log(torsion) + beta * log(conductor)
# This combines the murmuration signal with torsion and conductor info
for r in [0, 1, 2]:
    sub = df[df['rank'] == r]
    score = sub['ap_cumsum_normalized'] + 0.5 * sub['log_torsion'] - 0.3 * sub['log_conductor']
    print(f"  Rank {r}: composite score mean={score.mean():.4f}, std={score.std():.4f}")

# ============================================================
# PHASE 2: DEEPER PATTERN MINING
# ============================================================
print("\n" + "="*70)
print("PHASE 2: DEEPER PATTERN MINING")
print("="*70)

# Look at ratios and products of BSD invariants
print("\n--- Interesting ratios ---")

# Omega * Tamagawa / Torsion^2 -- this is the "easy" part of BSD
df['easy_bsd'] = df['real_period'] * df['tamagawa_product'] / (df['torsion_order']**2)
for r in [0, 1, 2]:
    sub = df[df['rank'] == r]['easy_bsd'].dropna()
    print(f"  Rank {r}: Omega*Tam/Tors^2: mean={sub.mean():.6f}, median={sub.median():.6f}")

# Regulator * Omega for rank >= 1
print("\n--- Regulator * Omega product ---")
for r in [1, 2]:
    sub = df[(df['rank'] == r) & (df['regulator'].notna()) & (df['regulator'] > 0)]
    if len(sub) > 0:
        prod = sub['real_period'] * sub['regulator']
        print(f"  Rank {r}: Omega*Reg: mean={prod.mean():.6f}, median={prod.median():.6f}")
        # Check scaling with N
        log_prod = np.log(prod)
        corr, pval = stats.spearmanr(sub['log_conductor'], log_prod)
        print(f"    vs log(N): Spearman r={corr:.4f}, p={pval:.2e}")

# Modular degree / conductor ratio
print("\n--- Modular degree / conductor ---")
sub = df[(df['modular_degree'].notna()) & (df['modular_degree'] > 0)]
sub_ratio = sub['modular_degree'] / sub['conductor']
for r in [0, 1, 2]:
    rsub = sub[sub['rank'] == r]
    if len(rsub) > 0:
        ratio = rsub['modular_degree'] / rsub['conductor']
        print(f"  Rank {r}: mod_deg/N: mean={ratio.mean():.6f}, median={ratio.median():.6f}")

# ============================================================
# PHASE 3: LOOK FOR CLOSED-FORM RELATIONSHIPS
# ============================================================
print("\n" + "="*70)
print("PHASE 3: CLOSED-FORM RELATIONSHIP SEARCH")
print("="*70)

# Test specific functional forms between BSD invariants
# These are candidate conjectures we can test

print("\n--- Testing candidate conjectural relationships ---")

# Candidate 1: Does log(mod_deg) ~ rank * log(N) + const?
print("\nCandidate 1: log(mod_deg) = alpha * rank + beta * log(N) + gamma")
sub = df[(df['modular_degree'].notna()) & (df['modular_degree'] > 0)].copy()
from numpy.linalg import lstsq
X = np.column_stack([sub['rank'].values, sub['log_conductor'].values, np.ones(len(sub))])
y = np.log(sub['modular_degree'].astype(float).values)
coeffs, residuals, _, _ = lstsq(X, y, rcond=None)
y_pred = X @ coeffs
ss_res = np.sum((y - y_pred)**2)
ss_tot = np.sum((y - y.mean())**2)
r2 = 1 - ss_res/ss_tot
print(f"  log(mod_deg) = {coeffs[0]:.4f}*rank + {coeffs[1]:.4f}*log(N) + {coeffs[2]:.4f}")
print(f"  R^2 = {r2:.4f}")

# Candidate 2: Omega * Tamagawa * Reg / Torsion^2 ~ N^alpha (by rank)
print("\nCandidate 2: Omega*Tam*Reg/Tors^2 ~ N^alpha (rank-dependent scaling)")
for r in [0, 1, 2]:
    sub = df[(df['rank'] == r) & (df['regulator'].notna()) & (df['regulator'] > 0)]
    if len(sub) < 10:
        continue
    bsd_val = sub['real_period'] * sub['tamagawa_product'] * sub['regulator'] / (sub['torsion_order']**2)
    valid = bsd_val > 0
    if valid.sum() < 10:
        continue
    log_bsd = np.log(bsd_val[valid].astype(float))
    log_N = sub.loc[valid.index[valid], 'log_conductor']
    slope, intercept, rval, _, _ = stats.linregress(log_N, log_bsd)
    print(f"  Rank {r}: exponent alpha = {slope:.4f}, R^2 = {rval**2:.4f}")

# Candidate 3: a_p pattern - does sum(a_p * p^{-s}) for specific s values predict rank?
print("\nCandidate 3: Partial Euler product evaluation at various s")
for s_val in [0.5, 0.75, 1.0, 1.25, 1.5]:
    df[f'partial_L_{s_val}'] = 0
    for p in primes:
        col = f'a_{p}'
        df[f'partial_L_{s_val}'] += df[col] * p**(-s_val)

    vals_by_rank = {}
    for r in [0, 1, 2]:
        vals_by_rank[r] = df[df['rank'] == r][f'partial_L_{s_val}'].dropna()

    if all(len(v) > 5 for v in vals_by_rank.values()):
        stat, p_kw = stats.kruskal(*vals_by_rank.values())
        means = [vals_by_rank[r].mean() for r in [0, 1, 2]]
        print(f"  s={s_val}: rank means = [{means[0]:.4f}, {means[1]:.4f}, {means[2]:.4f}], KW p={p_kw:.2e}")

# Candidate 4: Discriminant-conductor relationship
print("\nCandidate 4: |disc| vs N^k relationship")
for r in [0, 1, 2]:
    sub = df[df['rank'] == r]
    valid = sub['abs_disc'] > 0
    if valid.sum() < 10:
        continue
    log_disc = np.log(sub.loc[valid, 'abs_disc'].astype(float))
    log_N = sub.loc[valid, 'log_conductor']
    slope, intercept, rval, _, _ = stats.linregress(log_N, log_disc)
    print(f"  Rank {r}: log|disc| ~ {slope:.4f} * log(N) + {intercept:.4f}  (R^2={rval**2:.4f})")

# Candidate 5: Torsion and conductor interaction with Sha
print("\nCandidate 5: Sha prediction model")
sub = df[(df['analytic_sha'].notna()) & (df['analytic_sha'] > 0)].copy()
if len(sub) > 20:
    # Try to predict log(Sha) from other invariants
    features = ['rank', 'log_conductor', 'torsion_order', 'tamagawa_product',
                'num_bad_primes', 'log_omega']
    feature_cols = [c for c in features if c in sub.columns]
    X = sub[feature_cols].values
    y = np.log(sub['analytic_sha'].values + 1e-10)  # log(Sha)

    # Remove any rows with NaN
    valid = ~np.any(np.isnan(X), axis=1) & ~np.isnan(y)
    X = X[valid]
    y = y[valid]

    if len(X) > 10:
        X_aug = np.column_stack([X, np.ones(len(X))])
        coeffs, residuals, _, _ = lstsq(X_aug, y, rcond=None)
        y_pred = X_aug @ coeffs
        ss_res = np.sum((y - y_pred)**2)
        ss_tot = np.sum((y - y.mean())**2)
        r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0
        print(f"  Linear model R^2 = {r2:.4f}")
        for i, col in enumerate(feature_cols):
            print(f"    {col}: {coeffs[i]:.4f}")
        print(f"    intercept: {coeffs[-1]:.4f}")

# ============================================================
# PHASE 4: PRODUCT FORMULA TESTING
# ============================================================
print("\n" + "="*70)
print("PHASE 4: PRODUCT FORMULA EXPLORATION")
print("="*70)

# The BSD formula says: L^(r)(E,1)/r! = (Sha * Omega * Reg * prod(c_p)) / |E_tors|^2
# Can we find other product formulas?

# Test: Does c4^a * c6^b * N^c approximate any BSD quantity?
print("\n--- Power-law combinations of c4, c6, N ---")
sub = df[(df['c4'] != 0) & (df['c6'] != 0)].copy()
sub['log_abs_c4'] = np.log(np.abs(sub['c4']).astype(float))
sub['log_abs_c6'] = np.log(np.abs(sub['c6']).astype(float))

# Target: log(Omega)
X = np.column_stack([sub['log_abs_c4'].values, sub['log_abs_c6'].values,
                      sub['log_conductor'].values, np.ones(len(sub))])
y = sub['log_omega'].values
valid = ~np.any(np.isnan(X), axis=1) & ~np.isnan(y)
X, y = X[valid], y[valid]
if len(X) > 10:
    coeffs, _, _, _ = lstsq(X, y, rcond=None)
    y_pred = X @ coeffs
    r2 = 1 - np.sum((y-y_pred)**2)/np.sum((y-y.mean())**2)
    print(f"  log(Omega) ~ {coeffs[0]:.4f}*log|c4| + {coeffs[1]:.4f}*log|c6| + {coeffs[2]:.4f}*log(N) + {coeffs[3]:.4f}")
    print(f"  R^2 = {r2:.4f}")
    # Translate: Omega ~ |c4|^a * |c6|^b * N^c
    print(f"  => Omega ~ |c4|^{coeffs[0]:.3f} * |c6|^{coeffs[1]:.3f} * N^{coeffs[2]:.3f}")

# Target: log(mod_deg)
sub2 = sub[sub['modular_degree'].notna() & (sub['modular_degree'] > 0)].copy()
if len(sub2) > 10:
    X = np.column_stack([sub2['log_abs_c4'].values, sub2['log_abs_c6'].values,
                          sub2['log_conductor'].values, sub2['rank'].values, np.ones(len(sub2))])
    y = np.log(sub2['modular_degree'].astype(float).values)
    valid = ~np.any(np.isnan(X), axis=1) & ~np.isnan(y)
    X, y = X[valid], y[valid]
    if len(X) > 10:
        coeffs, _, _, _ = lstsq(X, y, rcond=None)
        y_pred = X @ coeffs
        r2 = 1 - np.sum((y-y_pred)**2)/np.sum((y-y.mean())**2)
        print(f"\n  log(mod_deg) ~ {coeffs[0]:.4f}*log|c4| + {coeffs[1]:.4f}*log|c6| + {coeffs[2]:.4f}*log(N) + {coeffs[3]:.4f}*rank + {coeffs[4]:.4f}")
        print(f"  R^2 = {r2:.4f}")

# ============================================================
# PHASE 5: SUPERSINGULAR PRIMES AND RANK
# ============================================================
print("\n" + "="*70)
print("PHASE 5: SUPERSINGULAR REDUCTION AND RANK")
print("="*70)

# For each prime p, a_p = 0 means supersingular reduction
# Question: Is the pattern of supersingular primes related to rank?
print("\nFraction of curves with a_p = 0, by rank and prime:")
print(f"  {'p':>5s}  {'rank_0':>8s}  {'rank_1':>8s}  {'rank_2':>8s}  {'r0-r2_diff':>10s}")
for p in primes:
    col = f'a_{p}'
    fracs = {}
    for r in [0, 1, 2]:
        sub = df[df['rank'] == r][col]
        fracs[r] = (sub == 0).mean()
    diff = fracs[0] - fracs[2]
    print(f"  {p:5d}  {fracs[0]:8.4f}  {fracs[1]:8.4f}  {fracs[2]:8.4f}  {diff:+10.4f}")

# Count of supersingular primes as rank predictor
df['num_supersingular'] = sum((df[f'a_{p}'] == 0).astype(int) for p in primes)
print("\nMean number of supersingular primes (out of 25) by rank:")
for r in [0, 1, 2]:
    sub = df[df['rank'] == r]['num_supersingular']
    print(f"  Rank {r}: {sub.mean():.3f} +/- {sub.std():.3f}")

stat, p_val = stats.kruskal(
    df[df['rank'] == 0]['num_supersingular'],
    df[df['rank'] == 1]['num_supersingular'],
    df[df['rank'] == 2]['num_supersingular']
)
print(f"  Kruskal-Wallis: H={stat:.2f}, p={p_val:.2e}")

# ============================================================
# PHASE 6: INFORMATION-THEORETIC ANALYSIS
# ============================================================
print("\n" + "="*70)
print("PHASE 6: MUTUAL INFORMATION AND FEATURE IMPORTANCE")
print("="*70)

# Use sklearn for mutual information
try:
    from sklearn.feature_selection import mutual_info_classif, mutual_info_regression
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

    # Prepare features for rank classification
    feature_names = ['conductor', 'log_conductor', 'torsion_order', 'tamagawa_product',
                     'real_period', 'num_bad_primes', 'c4', 'c6', 'log_omega',
                     'ap_cumsum_normalized', 'num_supersingular']
    feature_names.extend([f'a_{p}' for p in primes[:15]])

    feature_names = [f for f in feature_names if f in df.columns]

    sub = df[feature_names + ['rank']].dropna()
    X = sub[feature_names].values
    y = sub['rank'].values

    # Mutual information
    mi = mutual_info_classif(X, y, random_state=42)
    mi_ranking = sorted(zip(feature_names, mi), key=lambda x: x[1], reverse=True)

    print("\nMutual information with rank (bits):")
    for name, mi_val in mi_ranking[:15]:
        bar = "#" * int(mi_val * 50)
        print(f"  {name:25s}: {mi_val:.4f} {bar}")

    # Random Forest feature importance
    rf = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
    rf.fit(X, y)
    rf_importance = rf.feature_importances_
    rf_ranking = sorted(zip(feature_names, rf_importance), key=lambda x: x[1], reverse=True)

    print("\nRandom Forest feature importance for rank prediction:")
    print(f"  RF accuracy: {rf.score(X, y):.4f}")
    for name, imp in rf_ranking[:15]:
        bar = "#" * int(imp * 100)
        print(f"  {name:25s}: {imp:.4f} {bar}")

    # Gradient Boosting
    gb = GradientBoostingClassifier(n_estimators=200, max_depth=5, random_state=42)
    gb.fit(X, y)
    print(f"\n  GradientBoosting accuracy: {gb.score(X, y):.4f}")

except ImportError as e:
    print(f"  sklearn not available: {e}")

# ============================================================
# PHASE 7: NOVEL CONJECTURE SEARCH - Ratio Analysis
# ============================================================
print("\n" + "="*70)
print("PHASE 7: NOVEL CONJECTURE CANDIDATES")
print("="*70)

# Look for invariant ratios that are constant or simple by rank
print("\n--- Searching for rank-invariant ratios ---")

# For rank 0 curves with Sha = 1: L(E,1) = Omega * Tam / Tors^2
# What is the distribution of Omega * Tam / (Tors^2 * N^alpha)?
for alpha in np.arange(-0.5, 0.5, 0.05):
    sub = df[(df['rank'] == 0) & (df['analytic_sha'].notna()) & (df['analytic_sha'].round() == 1)]
    ratio = sub['real_period'] * sub['tamagawa_product'] / (sub['torsion_order']**2 * sub['conductor']**alpha)
    cv = ratio.std() / ratio.mean() if ratio.mean() != 0 else float('inf')
    if cv < 0.5:  # coefficient of variation < 50%
        print(f"  alpha={alpha:.2f}: Omega*Tam/(Tors^2 * N^alpha) CV = {cv:.4f}, mean = {ratio.mean():.6f}")

# For rank 1 curves: L'(E,1) = Sha * Omega * Reg * Tam / Tors^2
# Test: Omega * Reg * Tam / Tors^2 ~ N^beta
sub_r1 = df[(df['rank'] == 1) & (df['regulator'].notna()) & (df['regulator'] > 0)]
if len(sub_r1) > 10:
    bsd_r1 = sub_r1['real_period'] * sub_r1['regulator'] * sub_r1['tamagawa_product'] / (sub_r1['torsion_order']**2)
    log_bsd = np.log(bsd_r1.astype(float))
    log_N = sub_r1['log_conductor']
    slope, intercept, rval, _, _ = stats.linregress(log_N, log_bsd)
    print(f"\n  Rank 1: log(Omega*Reg*Tam/Tors^2) ~ {slope:.4f}*log(N) + {intercept:.4f}, R^2={rval**2:.4f}")

    # Residuals -- are they structured?
    residuals = log_bsd - (slope * log_N + intercept)
    # Do residuals correlate with a_p?
    for p in [2, 3, 5, 7, 11]:
        col = f'a_{p}'
        corr, pval = stats.spearmanr(residuals, sub_r1[col])
        if abs(corr) > 0.1:
            print(f"    Residual corr with a_{p}: {corr:.4f} (p={pval:.2e})")

# Check mod_deg / (N * Omega * Tam) ratio
print("\n--- Modular degree ratio exploration ---")
sub_md = df[(df['modular_degree'].notna()) & (df['modular_degree'] > 0)].copy()
if len(sub_md) > 10:
    # Test: mod_deg / N^2
    for r in [0, 1, 2]:
        rsub = sub_md[sub_md['rank'] == r]
        if len(rsub) > 5:
            ratio = rsub['modular_degree'] / rsub['conductor']**2
            print(f"  Rank {r}: mod_deg/N^2: mean={ratio.mean():.6e}, std={ratio.std():.6e}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "="*70)
print("SUMMARY OF KEY FINDINGS")
print("="*70)
print("""
Analysis complete. Key findings logged. See findings.md for detailed writeup.
Dataset: {n} curves (rank 0: {r0}, rank 1: {r1}, rank 2: {r2}, rank 3: {r3})
""".format(n=len(df), r0=len(df[df['rank']==0]), r1=len(df[df['rank']==1]),
           r2=len(df[df['rank']==2]), r3=len(df[df['rank']==3])))
