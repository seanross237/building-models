"""
Step 6: Test whether TDA persistence features can detect non-trivial Sha.

This is the core BSD test: Sha measures cohomological obstructions
(literally "holes" in local-global compatibility). Persistent homology
detects topological holes. If there is ANY correlation between
persistence features and |Sha|, this constitutes a genuine connection
between computational topology and arithmetic geometry.
"""

import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import json
import numpy as np
from ripser import ripser
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
from scipy.stats import mannwhitneyu, spearmanr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

BASE = "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/bsd-conjecture/approach-3-tda"
PLOT_DIR = os.path.join(BASE, "plots")

# Load Sha data
sha_file = os.path.join(BASE, "data", "sha_detection_data.json")
with open(sha_file) as f:
    sha_data = json.load(f)

prime_list = np.array(sha_data['prime_list'])
sha_nontrivial = sha_data['sha_nontrivial']
sha_trivial = sha_data['sha_trivial']

print(f"Sha > 1 curves: {len(sha_nontrivial)}")
print(f"Sha = 1 curves: {len(sha_trivial)}")

if len(sha_nontrivial) == 0:
    print("No Sha > 1 curves found. Exiting.")
    exit()

# Show Sha distribution
sha_vals = [c['sha_an_rounded'] for c in sha_nontrivial if c['sha_an_rounded'] is not None]
from collections import Counter
print(f"Sha distribution: {Counter(sha_vals)}")

# =====================================================================
# Compute TDA features for both groups
# =====================================================================
def build_prime_space_cloud(curve, prime_list):
    ap = np.array(curve['ap'], dtype=float)
    red = np.array(curve['reduction_types'], dtype=float)
    log_p = np.log(prime_list)
    normalized_ap = ap / (2 * np.sqrt(prime_list))
    ap_over_sqrtp = ap / np.sqrt(prime_list)
    cumulative_mean = np.cumsum(ap_over_sqrtp) / np.arange(1, len(prime_list)+1)
    return np.column_stack([log_p, normalized_ap, red, cumulative_mean])

def extract_features(curve, prime_list):
    X = build_prime_space_cloud(curve, prime_list)
    X_scaled = StandardScaler().fit_transform(X)
    result = ripser(X_scaled, maxdim=2, thresh=3.0)
    dgms = result['dgms']
    features = {}
    for dim in range(3):
        dgm = dgms[dim]
        finite = dgm[dgm[:, 1] < np.inf]
        lifetimes = finite[:, 1] - finite[:, 0] if len(finite) > 0 else np.array([0])
        features[f'H{dim}_count'] = len(finite)
        features[f'H{dim}_max_life'] = float(lifetimes.max()) if len(lifetimes) > 0 else 0
        features[f'H{dim}_mean_life'] = float(lifetimes.mean()) if len(lifetimes) > 0 else 0
        features[f'H{dim}_total_life'] = float(lifetimes.sum()) if len(lifetimes) > 0 else 0
        features[f'H{dim}_std_life'] = float(lifetimes.std()) if len(lifetimes) > 1 else 0
        if len(lifetimes) > 0 and lifetimes.sum() > 0:
            probs = lifetimes / lifetimes.sum()
            probs = probs[probs > 0]
            features[f'H{dim}_entropy'] = float(-np.sum(probs * np.log(probs)))
        else:
            features[f'H{dim}_entropy'] = 0
    return features

print("\nComputing TDA features for Sha > 1 curves...")
sha_features = []
for c in sha_nontrivial:
    try:
        f = extract_features(c, prime_list)
        f['sha'] = c['sha_an_rounded']
        f['conductor'] = c['conductor']
        f['label'] = c['label']
        sha_features.append(f)
    except:
        pass

print(f"  Successful: {len(sha_features)}")

print("Computing TDA features for Sha = 1 curves...")
control_features = []
for c in sha_trivial:
    try:
        f = extract_features(c, prime_list)
        f['sha'] = 1
        f['conductor'] = c['conductor']
        f['label'] = c['label']
        control_features.append(f)
    except:
        pass

print(f"  Successful: {len(control_features)}")

# =====================================================================
# Compare TDA features: Sha > 1 vs Sha = 1
# =====================================================================
feat_names = [k for k in sha_features[0].keys() if k not in ['sha', 'conductor', 'label']]

all_feats = sha_features + control_features
X_all = np.array([[f[k] for k in feat_names] for f in all_feats])
y_sha_binary = np.array([1 if f['sha'] > 1 else 0 for f in all_feats])
conductors = np.array([f['conductor'] for f in all_feats])

print(f"\n{'='*70}")
print("SHA DETECTION: TDA FEATURES")
print(f"{'='*70}")

print(f"\nSample sizes: Sha>1={sum(y_sha_binary==1)}, Sha=1={sum(y_sha_binary==0)}")

print("\nMann-Whitney U tests (Sha>1 vs Sha=1):")
for i, fn in enumerate(feat_names):
    vals_sha = X_all[y_sha_binary == 1, i]
    vals_ctrl = X_all[y_sha_binary == 0, i]
    u, p = mannwhitneyu(vals_sha, vals_ctrl, alternative='two-sided')
    effect = abs(vals_sha.mean() - vals_ctrl.mean()) / max(vals_sha.std(), vals_ctrl.std(), 0.001)
    marker = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
    if p < 0.1:  # Show marginally significant too
        print(f"  {fn}: p={p:.6f} {marker} effect={effect:.3f} "
              f"(sha>1: {vals_sha.mean():.4f}, sha=1: {vals_ctrl.mean():.4f})")

# Control for conductor
print("\nPartial correlation (TDA vs Sha | log(conductor)):")
from numpy.linalg import lstsq

log_cond = np.log(conductors)
for i, fn in enumerate(feat_names):
    # Full correlation
    r_full, p_full = spearmanr(X_all[:, i], y_sha_binary)
    # Partial correlation
    A = np.column_stack([log_cond, np.ones(len(log_cond))])
    coef_x = lstsq(A, X_all[:, i], rcond=None)[0]
    coef_y = lstsq(A, y_sha_binary.astype(float), rcond=None)[0]
    res_x = X_all[:, i] - A @ coef_x
    res_y = y_sha_binary.astype(float) - A @ coef_y
    from scipy.stats import pearsonr
    r_part, p_part = pearsonr(res_x, res_y)

    if abs(r_full) > 0.1 or p_full < 0.1:
        print(f"  {fn}: full rho={r_full:.4f} (p={p_full:.4f}), "
              f"partial r={r_part:.4f} (p={p_part:.4f})")

# Classification
print("\nClassification: Sha > 1 vs Sha = 1:")
X_scaled = StandardScaler().fit_transform(X_all)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Also build baseline features
ap_all = np.array([c['ap'] for c in sha_nontrivial + sha_trivial], dtype=float)
X_baseline = np.column_stack([
    ap_all.mean(axis=1),
    ap_all.std(axis=1),
    np.abs(ap_all).mean(axis=1),
    np.log(conductors),
])
X_base_s = StandardScaler().fit_transform(X_baseline)

for name, X_feat in [("TDA features", X_scaled),
                      ("Baseline", X_base_s),
                      ("TDA + Baseline", np.column_stack([X_scaled, X_base_s]))]:
    clf = GradientBoostingClassifier(n_estimators=100, random_state=42)
    try:
        scores = cross_val_score(clf, X_feat, y_sha_binary, cv=cv, scoring='accuracy')
        print(f"  {name}: {scores.mean():.3f} +/- {scores.std():.3f}")
    except Exception as e:
        print(f"  {name}: failed - {e}")

# =====================================================================
# Sha value analysis (if enough Sha=4 vs Sha=9 curves)
# =====================================================================
sha_values = np.array([f['sha'] for f in all_feats])
unique_sha = sorted(np.unique(sha_values[sha_values > 1]))
if len(unique_sha) > 1:
    print(f"\nTDA features by Sha value:")
    for fn_idx, fn in enumerate(feat_names):
        print(f"\n  {fn}:")
        for sv in [1] + list(unique_sha):
            mask = sha_values == sv
            if mask.sum() > 0:
                vals = X_all[mask, fn_idx]
                print(f"    Sha={sv}: mean={vals.mean():.4f} +/- {vals.std():.4f} (n={mask.sum()})")

# Visualization
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
top_features = ['H0_total_life', 'H1_total_life', 'H1_count',
                'H2_count', 'H0_mean_life', 'H1_entropy']

for ax, fn in zip(axes.flat, top_features):
    if fn in feat_names:
        idx = feat_names.index(fn)
        vals_sha = X_all[y_sha_binary == 1, idx]
        vals_ctrl = X_all[y_sha_binary == 0, idx]

        ax.boxplot([vals_ctrl, vals_sha], labels=['Sha=1', 'Sha>1'])
        u, p = mannwhitneyu(vals_sha, vals_ctrl, alternative='two-sided')
        ax.set_title(f'{fn}\n(p={p:.4f})')
        ax.set_ylabel(fn)

plt.suptitle('TDA Features: Sha=1 vs Sha>1 Curves', fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, 'E_sha_detection.png'), dpi=150)
plt.close()
print("\nSaved Sha detection plot")

print("\n" + "="*70)
print("SHA DETECTION SUMMARY")
print("="*70)
print("""
The key question: does persistent homology detect the Tate-Shafarevich group?

Sha is the CENTRAL object in BSD:
  - Sha is conjectured to be finite (Birch-Swinnerton-Dyer conjecture)
  - |Sha| appears in the BSD leading coefficient formula
  - Sha measures cohomological obstructions to Hasse principle

If TDA features correlate with |Sha| after controlling for conductor,
this would establish a genuine connection between:
  COMPUTATIONAL TOPOLOGY <-> ARITHMETIC COHOMOLOGY
""")

print("\nDone!")
