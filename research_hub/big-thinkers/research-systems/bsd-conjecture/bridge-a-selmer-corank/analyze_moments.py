"""
Core analysis: Can Frobenius moments separate Selmer CORANK from Selmer SIZE?

Key question: Given dim(Sel_2(E)) = d, can moments of {a_p} distinguish between:
  - (rank=r, dim Sha[2]=s)  where r + s + torsion_2_rank = d

This is the "size vs corank" problem.
"""

import json
import numpy as np
from collections import defaultdict, Counter
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Load data
with open("/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/bsd-conjecture/bridge-a-selmer-corank/enriched_data.json") as f:
    data = json.load(f)

print(f"Loaded {len(data)} curves")
print()

# ============================================================
# ANALYSIS 1: Moment statistics by rank and Selmer rank
# ============================================================
print("=" * 70)
print("ANALYSIS 1: Moments by (rank, sel2_rank)")
print("=" * 70)

# Build cross-tabulation
for feature_name in ['M1', 'M2', 'sym2_sum', 'mean_ap2_p_small', 'murm_sum', 'g_Lambda', 'var_normalized']:
    print(f"\n--- {feature_name} ---")
    for rank in [0, 1, 2]:
        for sel2 in sorted(set(e['sel2_rank'] for e in data)):
            subset = [e for e in data if e['rank'] == rank and e['sel2_rank'] == sel2]
            if len(subset) >= 5:
                values = [e[feature_name] for e in subset]
                print(f"  rank={rank}, sel2={sel2} (n={len(subset):4d}): "
                      f"mean={np.mean(values):+.4f}  std={np.std(values):.4f}  "
                      f"median={np.median(values):+.4f}")

# ============================================================
# ANALYSIS 2: Within fixed rank, do moments separate sel2?
# ============================================================
print("\n" + "=" * 70)
print("ANALYSIS 2: Within FIXED RANK, do moments separate Selmer rank?")
print("=" * 70)

for rank in [0, 1, 2]:
    print(f"\n--- Rank {rank} ---")
    sel2_values = sorted(set(e['sel2_rank'] for e in data if e['rank'] == rank))
    groups = {}
    for s in sel2_values:
        groups[s] = [e for e in data if e['rank'] == rank and e['sel2_rank'] == s]

    # Only keep groups with n >= 5
    groups = {s: g for s, g in groups.items() if len(g) >= 5}
    if len(groups) < 2:
        print("  Insufficient groups for comparison")
        continue

    for feature in ['M1', 'M2', 'sym2_sum', 'mean_ap2_p_small', 'murm_sum', 'g_Lambda', 'var_normalized', 'freq_ap_even']:
        # Kruskal-Wallis test across sel2 groups
        group_values = [np.array([e[feature] for e in g]) for g in groups.values()]
        if all(len(g) >= 5 for g in group_values):
            H, p_kw = stats.kruskal(*group_values)

            # Effect size: eta-squared from H
            N = sum(len(g) for g in group_values)
            k = len(group_values)
            eta_sq = (H - k + 1) / (N - k)

            # Spearman correlation with sel2_rank within this rank
            all_feat = []
            all_sel2 = []
            for s, g in groups.items():
                for e in g:
                    all_feat.append(e[feature])
                    all_sel2.append(s)
            rho, p_sp = stats.spearmanr(all_feat, all_sel2)

            sig = "***" if p_kw < 0.001 else "** " if p_kw < 0.01 else "*  " if p_kw < 0.05 else "   "
            print(f"  {feature:25s}: KW p={p_kw:.2e} {sig}  rho={rho:+.3f}  eta2={eta_sq:.4f}")

# ============================================================
# ANALYSIS 3: The key test -- within fixed sel2, do moments separate rank?
# ============================================================
print("\n" + "=" * 70)
print("ANALYSIS 3: Within FIXED SEL2, do moments separate RANK (corank)?")
print("This is the CORE test for the corank extraction problem.")
print("=" * 70)

for sel2 in [1, 2, 3]:
    print(f"\n--- sel2_rank = {sel2} ---")
    rank_values = sorted(set(e['rank'] for e in data if e['sel2_rank'] == sel2))
    groups = {}
    for r in rank_values:
        groups[r] = [e for e in data if e['rank'] == r and e['sel2_rank'] == sel2]

    groups = {r: g for r, g in groups.items() if len(g) >= 5}
    if len(groups) < 2:
        print("  Insufficient groups for comparison")
        continue

    print(f"  Groups: {', '.join(f'rank={r} (n={len(g)})' for r, g in groups.items())}")

    for feature in ['M1', 'M2', 'sym2_sum', 'mean_ap2_p_small', 'murm_sum', 'g_Lambda', 'var_normalized', 'freq_ap_even']:
        group_values = [np.array([e[feature] for e in g]) for g in groups.values()]
        if all(len(g) >= 5 for g in group_values):
            if len(group_values) == 2:
                U, p_mw = stats.mannwhitneyu(group_values[0], group_values[1], alternative='two-sided')
                # Cohen's d
                d_cohen = (np.mean(group_values[0]) - np.mean(group_values[1])) / np.sqrt(
                    (np.var(group_values[0]) + np.var(group_values[1])) / 2)
                print(f"  {feature:25s}: MW p={p_mw:.2e}  d={d_cohen:+.3f}  "
                      f"means=[{', '.join(f'{np.mean(g):+.3f}' for g in group_values)}]")
            else:
                H, p_kw = stats.kruskal(*group_values)
                all_feat = []
                all_rank = []
                for r, g in groups.items():
                    for e in g:
                        all_feat.append(e[feature])
                        all_rank.append(r)
                rho, _ = stats.spearmanr(all_feat, all_rank)
                print(f"  {feature:25s}: KW p={p_kw:.2e}  rho={rho:+.3f}  "
                      f"means=[{', '.join(f'{np.mean([e[feature] for e in g]):+.3f}' for r, g in sorted(groups.items()))}]")

# ============================================================
# ANALYSIS 4: Torsion structure's role in the Selmer decomposition
# ============================================================
print("\n" + "=" * 70)
print("ANALYSIS 4: Torsion structure and the Selmer decomposition")
print("=" * 70)

# The 2-Selmer rank decomposes as:
# sel2_rank = rank(E) + dim_F2(Sha[2]) + dim_F2(E[2](Q))
# where E[2](Q) is the rational 2-torsion
# dim_F2(E[2](Q)) = number of factors of 2 in torsion structure

for e in data:
    tors = e['torsion_structure']
    e['torsion_2_rank'] = sum(1 for t in tors if int(t) % 2 == 0)
    # Infer dim Sha[2]
    e['sha2_dim'] = e['sel2_rank'] - e['rank'] - e['torsion_2_rank']

print("Torsion 2-rank distribution:")
print(dict(sorted(Counter(e['torsion_2_rank'] for e in data).items())))

print("\nInferred dim Sha[2] distribution:")
sha2_dist = Counter(e['sha2_dim'] for e in data)
print(dict(sorted(sha2_dist.items())))

# Cross-tabulate rank x torsion_2_rank x sha2_dim
print("\nRank x Torsion_2_rank x sha2_dim:")
for rank in [0, 1, 2]:
    for t2r in [0, 1, 2]:
        for sha2d in [0, 1, 2]:
            subset = [e for e in data if e['rank'] == rank and e['torsion_2_rank'] == t2r and e['sha2_dim'] == sha2d]
            if len(subset) >= 2:
                print(f"  rank={rank}, tors2_rk={t2r}, sha2_dim={sha2d} (n={len(subset):4d}): "
                      f"M1={np.mean([e['M1'] for e in subset]):+.4f}  "
                      f"murm={np.mean([e['murm_sum'] for e in subset]):+.3f}  "
                      f"gL={np.mean([e['g_Lambda'] for e in subset]):+.4f}")

# ============================================================
# ANALYSIS 5: Can moments separate sha2_dim from rank?
# The CRITICAL test: within fixed sel2_rank, with torsion controlled
# ============================================================
print("\n" + "=" * 70)
print("ANALYSIS 5: Moments vs sha2_dim (controlling for rank + torsion)")
print("This tests whether moments constrain the Sha contribution separately")
print("=" * 70)

# Within rank=0, torsion_2_rank=1: curves with sel2=1 (sha2=0) vs sel2=2 (sha2=1) vs sel2=3 (sha2=2)
print("\n--- Rank=0, torsion_2_rank=1 (most cases) ---")
for sha2d in sorted(set(e['sha2_dim'] for e in data if e['rank'] == 0 and e['torsion_2_rank'] == 1)):
    subset = [e for e in data if e['rank'] == 0 and e['torsion_2_rank'] == 1 and e['sha2_dim'] == sha2d]
    if len(subset) >= 3:
        print(f"  sha2_dim={sha2d} (n={len(subset)}): "
              f"M1={np.mean([e['M1'] for e in subset]):+.4f} +/- {np.std([e['M1'] for e in subset]):.4f}  "
              f"M2={np.mean([e['M2'] for e in subset]):+.4f}  "
              f"murm={np.mean([e['murm_sum'] for e in subset]):+.3f}  "
              f"sym2={np.mean([e['sym2_sum'] for e in subset]):+.4f}  "
              f"gL={np.mean([e['g_Lambda'] for e in subset]):+.4f}")

# Within rank=0, torsion_2_rank=0
print("\n--- Rank=0, torsion_2_rank=0 ---")
for sha2d in sorted(set(e['sha2_dim'] for e in data if e['rank'] == 0 and e['torsion_2_rank'] == 0)):
    subset = [e for e in data if e['rank'] == 0 and e['torsion_2_rank'] == 0 and e['sha2_dim'] == sha2d]
    if len(subset) >= 3:
        print(f"  sha2_dim={sha2d} (n={len(subset)}): "
              f"M1={np.mean([e['M1'] for e in subset]):+.4f} +/- {np.std([e['M1'] for e in subset]):.4f}  "
              f"M2={np.mean([e['M2'] for e in subset]):+.4f}  "
              f"murm={np.mean([e['murm_sum'] for e in subset]):+.3f}")

# Within rank=1, torsion_2_rank=0
print("\n--- Rank=1, torsion_2_rank=0 ---")
for sha2d in sorted(set(e['sha2_dim'] for e in data if e['rank'] == 1 and e['torsion_2_rank'] == 0)):
    subset = [e for e in data if e['rank'] == 1 and e['torsion_2_rank'] == 0 and e['sha2_dim'] == sha2d]
    if len(subset) >= 3:
        print(f"  sha2_dim={sha2d} (n={len(subset)}): "
              f"M1={np.mean([e['M1'] for e in subset]):+.4f} +/- {np.std([e['M1'] for e in subset]):.4f}  "
              f"M2={np.mean([e['M2'] for e in subset]):+.4f}  "
              f"murm={np.mean([e['murm_sum'] for e in subset]):+.3f}")

# Within rank=1, torsion_2_rank=1
print("\n--- Rank=1, torsion_2_rank=1 ---")
for sha2d in sorted(set(e['sha2_dim'] for e in data if e['rank'] == 1 and e['torsion_2_rank'] == 1)):
    subset = [e for e in data if e['rank'] == 1 and e['torsion_2_rank'] == 1 and e['sha2_dim'] == sha2d]
    if len(subset) >= 3:
        print(f"  sha2_dim={sha2d} (n={len(subset)}): "
              f"M1={np.mean([e['M1'] for e in subset]):+.4f} +/- {np.std([e['M1'] for e in subset]):.4f}  "
              f"M2={np.mean([e['M2'] for e in subset]):+.4f}  "
              f"murm={np.mean([e['murm_sum'] for e in subset]):+.3f}")

# ============================================================
# ANALYSIS 6: Multiple regression -- predict (rank, sha2_dim) from moments
# ============================================================
print("\n" + "=" * 70)
print("ANALYSIS 6: Multiple regression of (rank, sha2_dim) on moments")
print("=" * 70)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

features = ['M1', 'M2', 'M3', 'M4', 'sym2_sum', 'murm_sum', 'g_Lambda', 'var_normalized', 'freq_ap_even']

# Prepare data
X = np.array([[e[f] for f in features] for e in data])
y_rank = np.array([e['rank'] for e in data])
y_sel2 = np.array([e['sel2_rank'] for e in data])
y_sha2 = np.array([e['sha2_dim'] for e in data])
y_tors2 = np.array([e['torsion_2_rank'] for e in data])

# Regress rank on moments
reg_rank = LinearRegression().fit(X, y_rank)
r2_rank = r2_score(y_rank, reg_rank.predict(X))
print(f"R^2(rank ~ moments):     {r2_rank:.4f}")
print(f"  Coefficients: {dict(zip(features, [f'{c:.4f}' for c in reg_rank.coef_]))}")

# Regress sel2 on moments
reg_sel2 = LinearRegression().fit(X, y_sel2)
r2_sel2 = r2_score(y_sel2, reg_sel2.predict(X))
print(f"R^2(sel2 ~ moments):     {r2_sel2:.4f}")

# Regress sha2_dim on moments
reg_sha2 = LinearRegression().fit(X, y_sha2)
r2_sha2 = r2_score(y_sha2, reg_sha2.predict(X))
print(f"R^2(sha2_dim ~ moments): {r2_sha2:.4f}")

# Regress torsion_2_rank on moments
reg_tors2 = LinearRegression().fit(X, y_tors2)
r2_tors2 = r2_score(y_tors2, reg_tors2.predict(X))
print(f"R^2(tors2_rk ~ moments): {r2_tors2:.4f}")

# CRITICAL: After controlling for rank (residual analysis)
# Regress sha2_dim on moments, controlling for rank
y_sha2_resid = y_sha2 - LinearRegression().fit(y_rank.reshape(-1,1), y_sha2).predict(y_rank.reshape(-1,1))
X_resid = X - LinearRegression().fit(y_rank.reshape(-1,1), X).predict(y_rank.reshape(-1,1))
reg_sha2_resid = LinearRegression().fit(X_resid, y_sha2_resid)
r2_sha2_resid = r2_score(y_sha2_resid, reg_sha2_resid.predict(X_resid))
print(f"\nR^2(sha2_dim ~ moments | controlling rank): {r2_sha2_resid:.4f}")

# After controlling for both rank AND torsion
controls = np.column_stack([y_rank, y_tors2])
y_sha2_resid2 = y_sha2 - LinearRegression().fit(controls, y_sha2).predict(controls)
X_resid2 = X - LinearRegression().fit(controls, X).predict(controls)
reg_sha2_resid2 = LinearRegression().fit(X_resid2, y_sha2_resid2)
r2_sha2_resid2 = r2_score(y_sha2_resid2, reg_sha2_resid2.predict(X_resid2))
print(f"R^2(sha2_dim ~ moments | controlling rank+torsion): {r2_sha2_resid2:.4f}")

# ============================================================
# ANALYSIS 7: The symmetric square L-function connection
# ============================================================
print("\n" + "=" * 70)
print("ANALYSIS 7: The sym^2 sum and its relation to Sha")
print("The symmetric square sum S2 = sum (a_p^2 - p)/p^2 is related to")
print("L(Sym^2 E, 1) via the Rankin-Selberg method.")
print("=" * 70)

# Group by rank and check if sym2_sum separates Sha
for rank in [0, 1]:
    subset = [e for e in data if e['rank'] == rank]
    sha_trivial = [e for e in subset if round(e['analytic_sha']) == 1]
    sha_nontrivial = [e for e in subset if round(e['analytic_sha']) > 1]

    print(f"\nRank {rank}: {len(sha_trivial)} trivial Sha, {len(sha_nontrivial)} nontrivial Sha")
    if sha_nontrivial:
        print(f"  sym2_sum: trivial={np.mean([e['sym2_sum'] for e in sha_trivial]):.4f}, "
              f"nontrivial={np.mean([e['sym2_sum'] for e in sha_nontrivial]):.4f}")
        print(f"  M2:       trivial={np.mean([e['M2'] for e in sha_trivial]):.4f}, "
              f"nontrivial={np.mean([e['M2'] for e in sha_nontrivial]):.4f}")

# Correlation of sym2_sum with sha2_dim across all curves
rho_sym2_sha2, p_sym2_sha2 = stats.spearmanr(
    [e['sym2_sum'] for e in data],
    [e['sha2_dim'] for e in data]
)
print(f"\nSpearman(sym2_sum, sha2_dim): rho={rho_sym2_sha2:.4f}, p={p_sym2_sha2:.2e}")

# Within fixed rank
for rank in [0, 1, 2]:
    subset = [e for e in data if e['rank'] == rank]
    rho, p = stats.spearmanr(
        [e['sym2_sum'] for e in subset],
        [e['sha2_dim'] for e in subset]
    )
    print(f"  rank={rank}: Spearman(sym2_sum, sha2_dim): rho={rho:.4f}, p={p:.2e}")

# ============================================================
# ANALYSIS 8: Minimal moment set for joint (rank, sha2_dim) prediction
# ============================================================
print("\n" + "=" * 70)
print("ANALYSIS 8: Minimal moment set for joint rank+sha prediction")
print("=" * 70)

from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

# Create joint target: (rank, sha2_dim)
y_joint = np.array([e['rank'] * 10 + e['sha2_dim'] for e in data])

feature_sets = {
    'M1 only': ['M1'],
    'M1+M2': ['M1', 'M2'],
    'M1+M2+M3': ['M1', 'M2', 'M3'],
    'M1+M2+M3+M4': ['M1', 'M2', 'M3', 'M4'],
    'M1+sym2': ['M1', 'sym2_sum'],
    'M1+murm': ['M1', 'murm_sum'],
    'M1+gL': ['M1', 'g_Lambda'],
    'murm+sym2': ['murm_sum', 'sym2_sum'],
    'all moments': features,
    'all moments + freq_even': features + ['freq_ap_even'],
}

# Predict rank
print("\nRank prediction (5-fold CV, GBM):")
for name, feats in feature_sets.items():
    Xi = np.array([[e[f] for f in feats] for e in data])
    scores = cross_val_score(GradientBoostingClassifier(n_estimators=100, random_state=42),
                             Xi, y_rank, cv=5, scoring='accuracy')
    print(f"  {name:30s}: {scores.mean():.3f} +/- {scores.std():.3f}")

# Predict sha2_dim
print("\nsha2_dim prediction (5-fold CV, GBM):")
for name, feats in feature_sets.items():
    Xi = np.array([[e[f] for f in feats] for e in data])
    scores = cross_val_score(GradientBoostingClassifier(n_estimators=100, random_state=42),
                             Xi, y_sha2, cv=5, scoring='accuracy')
    print(f"  {name:30s}: {scores.mean():.3f} +/- {scores.std():.3f}")

# Predict joint (rank, sha2_dim)
print("\nJoint (rank, sha2_dim) prediction (5-fold CV, GBM):")
for name, feats in feature_sets.items():
    Xi = np.array([[e[f] for f in feats] for e in data])
    scores = cross_val_score(GradientBoostingClassifier(n_estimators=100, random_state=42),
                             Xi, y_joint, cv=5, scoring='accuracy')
    print(f"  {name:30s}: {scores.mean():.3f} +/- {scores.std():.3f}")

# ============================================================
# ANALYSIS 9: Feature importance for sha2_dim prediction
# ============================================================
print("\n" + "=" * 70)
print("ANALYSIS 9: Feature importance for sha2_dim prediction")
print("=" * 70)

Xi = np.array([[e[f] for f in features] for e in data])
rf = RandomForestClassifier(n_estimators=200, random_state=42).fit(Xi, y_sha2)
importances = dict(zip(features, rf.feature_importances_))
for feat, imp in sorted(importances.items(), key=lambda x: -x[1]):
    print(f"  {feat:25s}: {imp:.4f}")

# ============================================================
# ANALYSIS 10: The conductor confound check
# ============================================================
print("\n" + "=" * 70)
print("ANALYSIS 10: Conductor confound check")
print("Does sha2_dim correlate with conductor? If so, the moment-sha")
print("connection might be mediated by conductor.")
print("=" * 70)

conductors = np.array([e['conductor'] for e in data])
rho_cond_sha2, p_cond_sha2 = stats.spearmanr(conductors, y_sha2)
print(f"Spearman(conductor, sha2_dim): rho={rho_cond_sha2:.4f}, p={p_cond_sha2:.2e}")

rho_cond_rank, p_cond_rank = stats.spearmanr(conductors, y_rank)
print(f"Spearman(conductor, rank):     rho={rho_cond_rank:.4f}, p={p_cond_rank:.2e}")

# Partial correlation of moments with sha2_dim controlling for conductor
print("\nPartial correlations of moments with sha2_dim (controlling conductor):")
for feat in features:
    feat_vals = np.array([e[feat] for e in data])
    # Partial correlation = correlation of residuals
    resid_feat = feat_vals - np.polyval(np.polyfit(conductors, feat_vals, 1), conductors)
    resid_sha2 = y_sha2 - np.polyval(np.polyfit(conductors, y_sha2, 1), conductors)
    rho, p = stats.spearmanr(resid_feat, resid_sha2)
    sig = "***" if p < 0.001 else "** " if p < 0.01 else "*  " if p < 0.05 else "   "
    print(f"  {feat:25s}: rho={rho:+.4f}, p={p:.2e} {sig}")

print("\n\n=== SUMMARY ===")
print("The key result is whether moments can determine sha2_dim AFTER controlling")
print("for rank and torsion. This is the bridge between Selmer SIZE and CORANK.")
