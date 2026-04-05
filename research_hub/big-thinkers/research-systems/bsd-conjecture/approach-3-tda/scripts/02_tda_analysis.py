"""
Step 2: TDA Analysis of Arithmetic Data

METHOD A: "Frobenius Space" — Each curve is a point in R^100 (coordinates = a_p values).
          Compute persistent homology of the point cloud.
          Test: do rank classes separate topologically?

METHOD B: "Prime Space" — For a single curve, each prime p -> (a_p, reduction_type).
          Compute persistent homology per curve.
          Test: do persistence features correlate with BSD invariants?

METHOD C: "Normalized Frobenius Space" — Each curve is a point in R^100 where
          coordinates are a_p / (2*sqrt(p)), normalizing by Hasse bound.
          This puts all coordinates in [-1, 1] and may reveal deeper structure.
"""

import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import json
import numpy as np
from ripser import ripser
from persim import plot_diagrams, wasserstein, bottleneck
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings('ignore')

BASE = "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/bsd-conjecture/approach-3-tda"
DATA_FILE = os.path.join(BASE, "data", "curves_arithmetic_data.json")
PLOT_DIR = os.path.join(BASE, "plots")
RESULTS_DIR = os.path.join(BASE, "results")

# Load data
with open(DATA_FILE) as f:
    data = json.load(f)

prime_list = np.array(data['prime_list'])
curves = data['curves']
n_primes = data['num_primes']

print(f"Loaded {len(curves)} curves, {n_primes} primes (up to {prime_list[-1]})")

# Extract arrays
labels = [c['label'] for c in curves]
ranks = np.array([c['rank'] for c in curves])
conductors = np.array([c['conductor'] for c in curves])
sha_values = np.array([c['sha_an'] if c['sha_an'] is not None else np.nan for c in curves])
torsion = np.array([c['torsion'] for c in curves])
ap_matrix = np.array([c['ap'] for c in curves])  # shape: (n_curves, n_primes)
red_matrix = np.array([c['reduction_types'] for c in curves])

print(f"ap_matrix shape: {ap_matrix.shape}")
print(f"Rank distribution: {dict(zip(*np.unique(ranks, return_counts=True)))}")

# =====================================================================
# METHOD A: Frobenius Space — curves as points in R^100
# =====================================================================
print("\n" + "="*70)
print("METHOD A: FROBENIUS SPACE")
print("="*70)

# A1: Raw a_p point cloud
print("\n--- A1: Raw Frobenius traces ---")
X_raw = ap_matrix.astype(float)

# A2: Normalized by Hasse bound: a_p / (2*sqrt(p))
print("--- A2: Hasse-normalized ---")
hasse_bounds = 2 * np.sqrt(prime_list)
X_normalized = X_raw / hasse_bounds[np.newaxis, :]

# A3: StandardScaler normalization
X_scaled = StandardScaler().fit_transform(X_raw)

# Compute PCA for visualization
pca = PCA(n_components=3)
X_pca = pca.fit_transform(X_scaled)
print(f"PCA explained variance: {pca.explained_variance_ratio_[:3].round(4)}")

# PCA visualization colored by rank
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for r in sorted(np.unique(ranks)):
    mask = ranks == r
    axes[0].scatter(X_pca[mask, 0], X_pca[mask, 1], label=f'Rank {r}', alpha=0.6, s=30)
    axes[1].scatter(X_pca[mask, 0], X_pca[mask, 2], label=f'Rank {r}', alpha=0.6, s=30)
    axes[2].scatter(X_pca[mask, 1], X_pca[mask, 2], label=f'Rank {r}', alpha=0.6, s=30)
for i, (xl, yl) in enumerate([('PC1', 'PC2'), ('PC1', 'PC3'), ('PC2', 'PC3')]):
    axes[i].set_xlabel(xl)
    axes[i].set_ylabel(yl)
    axes[i].legend()
    axes[i].set_title(f'Frobenius Space PCA: {xl} vs {yl}')
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, 'A_pca_by_rank.png'), dpi=150)
plt.close()
print("Saved PCA plot")

# t-SNE visualization
try:
    tsne = TSNE(n_components=2, random_state=42, perplexity=30)
    X_tsne = tsne.fit_transform(X_scaled)
    fig, ax = plt.subplots(figsize=(8, 6))
    for r in sorted(np.unique(ranks)):
        mask = ranks == r
        ax.scatter(X_tsne[mask, 0], X_tsne[mask, 1], label=f'Rank {r}', alpha=0.6, s=30)
    ax.legend()
    ax.set_title('t-SNE of Frobenius Space (colored by rank)')
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, 'A_tsne_by_rank.png'), dpi=150)
    plt.close()
    print("Saved t-SNE plot")
except Exception as e:
    print(f"t-SNE failed (non-critical): {e}")

# =====================================================================
# Persistent Homology on Frobenius Space subsets
# =====================================================================
print("\n--- Computing persistent homology on Frobenius space ---")

def compute_persistence(X, maxdim=2, thresh=None):
    """Compute Vietoris-Rips persistence."""
    if thresh is None:
        # Use a reasonable threshold
        from scipy.spatial.distance import pdist
        dists = pdist(X)
        thresh = np.percentile(dists, 30)
    result = ripser(X, maxdim=maxdim, thresh=thresh)
    return result

# Full point cloud persistence (all curves)
print("Computing persistence for all curves in Frobenius space...")
result_all = compute_persistence(X_scaled, maxdim=2)
dgms_all = result_all['dgms']

fig, ax = plt.subplots(figsize=(8, 6))
plot_diagrams(dgms_all, ax=ax, show=False)
ax.set_title('Persistence Diagram: All Curves in Frobenius Space')
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, 'A_persistence_all.png'), dpi=150)
plt.close()
print("Saved persistence diagram for all curves")

for dim in range(3):
    dgm = dgms_all[dim]
    finite = dgm[dgm[:, 1] < np.inf]
    if len(finite) > 0:
        lifetimes = finite[:, 1] - finite[:, 0]
        print(f"  H_{dim}: {len(dgm)} features, {len(finite)} finite, "
              f"max lifetime={lifetimes.max():.3f}, mean={lifetimes.mean():.3f}")
    else:
        print(f"  H_{dim}: {len(dgm)} features (all infinite)")

# Per-rank subcloud persistence
print("\nComputing persistence by rank class...")
rank_persistence = {}
for r in sorted(np.unique(ranks)):
    mask = ranks == r
    X_r = X_scaled[mask]
    if len(X_r) < 5:
        print(f"  Rank {r}: only {len(X_r)} points, skipping")
        continue
    result_r = compute_persistence(X_r, maxdim=2)
    rank_persistence[r] = result_r['dgms']

    fig, ax = plt.subplots(figsize=(8, 6))
    plot_diagrams(result_r['dgms'], ax=ax, show=False)
    ax.set_title(f'Persistence Diagram: Rank {r} Curves')
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, f'A_persistence_rank{r}.png'), dpi=150)
    plt.close()

    for dim in range(3):
        dgm = result_r['dgms'][dim]
        finite = dgm[dgm[:, 1] < np.inf]
        if len(finite) > 0:
            lifetimes = finite[:, 1] - finite[:, 0]
            print(f"  Rank {r}, H_{dim}: {len(finite)} finite features, "
                  f"max lifetime={lifetimes.max():.3f}")

# =====================================================================
# Wasserstein distances between rank classes
# =====================================================================
print("\n--- Wasserstein distances between rank-class persistence diagrams ---")
rank_keys = sorted(rank_persistence.keys())
for dim in range(2):  # H_0 and H_1
    print(f"\n  H_{dim} Wasserstein distances:")
    for i, r1 in enumerate(rank_keys):
        for r2 in rank_keys[i+1:]:
            d1 = rank_persistence[r1][dim]
            d2 = rank_persistence[r2][dim]
            # Filter to finite features
            d1_fin = d1[d1[:, 1] < np.inf]
            d2_fin = d2[d2[:, 1] < np.inf]
            if len(d1_fin) > 0 and len(d2_fin) > 0:
                try:
                    wd = wasserstein(d1_fin, d2_fin)
                    bd = bottleneck(d1_fin, d2_fin)
                    print(f"    Rank {r1} vs Rank {r2}: Wasserstein={wd:.4f}, Bottleneck={bd:.4f}")
                except Exception as e:
                    print(f"    Rank {r1} vs Rank {r2}: error - {e}")

# =====================================================================
# METHOD B: Prime Space — per-curve persistence
# =====================================================================
print("\n" + "="*70)
print("METHOD B: PRIME SPACE (per-curve)")
print("="*70)

def build_prime_space_cloud(curve, prime_list):
    """
    Build a point cloud for a single curve where each prime p
    maps to a vector (log(p), a_p/2sqrt(p), reduction_type_encoded).
    """
    ap = np.array(curve['ap'], dtype=float)
    red = np.array(curve['reduction_types'], dtype=float)

    # Coordinates for each prime
    log_p = np.log(prime_list)
    normalized_ap = ap / (2 * np.sqrt(prime_list))

    # 3D point cloud: (log(p), a_p/2sqrt(p), reduction_type)
    # Also add: cumulative average of a_p/sqrt(p) (Sato-Tate statistic)
    ap_over_sqrtp = ap / np.sqrt(prime_list)
    cumulative_mean = np.cumsum(ap_over_sqrtp) / np.arange(1, len(prime_list)+1)

    X = np.column_stack([log_p, normalized_ap, red, cumulative_mean])
    return X

# Compute per-curve persistence features
print("Computing per-curve persistence in prime space...")

curve_features = []
for i, curve in enumerate(curves):
    X_prime = build_prime_space_cloud(curve, prime_list)
    X_prime_scaled = StandardScaler().fit_transform(X_prime)

    try:
        result = ripser(X_prime_scaled, maxdim=2, thresh=3.0)
        dgms = result['dgms']

        features = {
            'label': curve['label'],
            'rank': curve['rank'],
            'sha_an': curve['sha_an'],
            'conductor': curve['conductor'],
        }

        for dim in range(3):
            dgm = dgms[dim]
            finite = dgm[dgm[:, 1] < np.inf]
            lifetimes = finite[:, 1] - finite[:, 0] if len(finite) > 0 else np.array([0])

            features[f'H{dim}_count'] = len(finite)
            features[f'H{dim}_max_life'] = float(lifetimes.max()) if len(lifetimes) > 0 else 0
            features[f'H{dim}_mean_life'] = float(lifetimes.mean()) if len(lifetimes) > 0 else 0
            features[f'H{dim}_total_life'] = float(lifetimes.sum()) if len(lifetimes) > 0 else 0
            features[f'H{dim}_std_life'] = float(lifetimes.std()) if len(lifetimes) > 1 else 0
            # Persistence entropy
            if len(lifetimes) > 0 and lifetimes.sum() > 0:
                probs = lifetimes / lifetimes.sum()
                probs = probs[probs > 0]
                features[f'H{dim}_entropy'] = float(-np.sum(probs * np.log(probs)))
            else:
                features[f'H{dim}_entropy'] = 0

        curve_features.append(features)
    except Exception as e:
        print(f"  FAILED for {curve['label']}: {e}")

print(f"Computed features for {len(curve_features)} curves")

# Build feature matrix from per-curve persistence
feat_names = [k for k in curve_features[0].keys() if k not in ['label', 'rank', 'sha_an', 'conductor']]
X_tda = np.array([[cf[fn] for fn in feat_names] for cf in curve_features])
y_rank = np.array([cf['rank'] for cf in curve_features])
y_sha = np.array([cf['sha_an'] if cf['sha_an'] is not None else np.nan for cf in curve_features])

print(f"\nTDA feature matrix: {X_tda.shape}")
print(f"Feature names: {feat_names}")

# Print feature statistics by rank
print("\n--- Per-curve persistence features by rank ---")
for fn in feat_names:
    fidx = feat_names.index(fn)
    print(f"\n  {fn}:")
    for r in sorted(np.unique(y_rank)):
        mask = y_rank == r
        vals = X_tda[mask, fidx]
        print(f"    Rank {r}: mean={vals.mean():.4f}, std={vals.std():.4f}, "
              f"min={vals.min():.4f}, max={vals.max():.4f}")

# =====================================================================
# CLASSIFICATION: Can TDA features predict rank?
# =====================================================================
print("\n" + "="*70)
print("CLASSIFICATION: TDA FEATURES -> RANK")
print("="*70)

# Binary: rank 0 vs rank >= 1
y_binary = (y_rank >= 1).astype(int)
print(f"\nBinary classification (rank 0 vs rank>=1): {np.bincount(y_binary)}")

X_tda_scaled = StandardScaler().fit_transform(X_tda)

# Also build baseline features: just raw a_p statistics
X_baseline = np.column_stack([
    ap_matrix[:len(curve_features)].mean(axis=1),
    ap_matrix[:len(curve_features)].std(axis=1),
    np.abs(ap_matrix[:len(curve_features)]).mean(axis=1),
])
X_baseline_scaled = StandardScaler().fit_transform(X_baseline)

# Combined: TDA + baseline
X_combined = np.column_stack([X_tda_scaled, X_baseline_scaled])

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for name, X_feat in [("TDA features only", X_tda_scaled),
                      ("Baseline a_p stats", X_baseline_scaled),
                      ("TDA + baseline", X_combined)]:
    for clf_name, clf in [("SVM-RBF", SVC(kernel='rbf', C=10, gamma='scale')),
                          ("Random Forest", RandomForestClassifier(n_estimators=100, random_state=42))]:
        # Binary
        scores = cross_val_score(clf, X_feat, y_binary, cv=cv, scoring='accuracy')
        print(f"  {name} | {clf_name} | Rank 0 vs >=1: {scores.mean():.3f} +/- {scores.std():.3f}")

# Multi-class: rank 0 vs 1 vs 2
# Filter to ranks 0, 1, 2 (enough samples)
mask_012 = y_rank <= 2
X_012 = X_tda_scaled[mask_012]
y_012 = y_rank[mask_012]
X_base_012 = X_baseline_scaled[mask_012]
X_comb_012 = X_combined[mask_012]

print(f"\nMulti-class (rank 0 vs 1 vs 2): {dict(zip(*np.unique(y_012, return_counts=True)))}")

for name, X_feat in [("TDA features", X_012),
                      ("Baseline", X_base_012),
                      ("TDA + baseline", X_comb_012)]:
    for clf_name, clf in [("SVM-RBF", SVC(kernel='rbf', C=10, gamma='scale')),
                          ("RF", RandomForestClassifier(n_estimators=100, random_state=42))]:
        scores = cross_val_score(clf, X_feat, y_012, cv=cv, scoring='accuracy')
        print(f"  {name} | {clf_name} | 3-class: {scores.mean():.3f} +/- {scores.std():.3f}")

# The hardest test: rank 0 vs rank 2
mask_02 = np.isin(y_rank, [0, 2])
X_02 = X_tda_scaled[mask_02]
y_02 = y_rank[mask_02]
X_base_02 = X_baseline_scaled[mask_02]
X_comb_02 = X_combined[mask_02]

print(f"\nHardest test — Rank 0 vs Rank 2: {dict(zip(*np.unique(y_02, return_counts=True)))}")

for name, X_feat in [("TDA features", X_02),
                      ("Baseline", X_base_02),
                      ("TDA + baseline", X_comb_02)]:
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    scores = cross_val_score(clf, X_feat, y_02, cv=cv, scoring='accuracy')
    print(f"  {name} | RF | Rank 0 vs 2: {scores.mean():.3f} +/- {scores.std():.3f}")

# =====================================================================
# Feature importance for rank discrimination
# =====================================================================
print("\n--- Feature importance (Random Forest, binary task) ---")
rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_tda_scaled, y_binary)
importances = rf.feature_importances_
sorted_idx = np.argsort(importances)[::-1]
for i in sorted_idx[:10]:
    print(f"  {feat_names[i]}: {importances[i]:.4f}")

# Plot feature importances
fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(range(len(feat_names)), importances[sorted_idx])
ax.set_xticks(range(len(feat_names)))
ax.set_xticklabels([feat_names[i] for i in sorted_idx], rotation=45, ha='right')
ax.set_title('TDA Feature Importance for Rank Prediction')
ax.set_ylabel('Importance')
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, 'B_feature_importance.png'), dpi=150)
plt.close()

# =====================================================================
# METHOD C: Hasse-Normalized Frobenius Space with sliding windows
# =====================================================================
print("\n" + "="*70)
print("METHOD C: HASSE-NORMALIZED + SLIDING WINDOW")
print("="*70)

# Use sliding windows of a_p values to build delay embeddings
# This is inspired by Takens' embedding theorem
def delay_embedding(series, dim=5, delay=1):
    """Create delay embedding of a time series."""
    n = len(series) - (dim - 1) * delay
    if n < 1:
        return np.array([])
    result = np.zeros((n, dim))
    for i in range(dim):
        result[:, i] = series[i*delay : i*delay + n]
    return result

print("Computing delay embeddings of normalized Frobenius sequences...")

delay_features = []
for i, curve in enumerate(curves):
    ap_seq = np.array(curve['ap'], dtype=float) / (2 * np.sqrt(prime_list))

    # Delay embedding: window=7, delay=1
    embedded = delay_embedding(ap_seq, dim=7, delay=1)
    if len(embedded) < 10:
        continue

    # Compute persistence on the delay embedding
    try:
        result = ripser(embedded, maxdim=1, thresh=2.0)
        dgms = result['dgms']

        features = {'rank': curve['rank'], 'label': curve['label']}
        for dim in range(2):
            dgm = dgms[dim]
            finite = dgm[dgm[:, 1] < np.inf]
            lifetimes = finite[:, 1] - finite[:, 0] if len(finite) > 0 else np.array([0])
            features[f'delay_H{dim}_count'] = len(finite)
            features[f'delay_H{dim}_max'] = float(lifetimes.max()) if len(lifetimes) > 0 else 0
            features[f'delay_H{dim}_mean'] = float(lifetimes.mean()) if len(lifetimes) > 0 else 0
            features[f'delay_H{dim}_total'] = float(lifetimes.sum()) if len(lifetimes) > 0 else 0
            if len(lifetimes) > 0 and lifetimes.sum() > 0:
                probs = lifetimes / lifetimes.sum()
                probs = probs[probs > 0]
                features[f'delay_H{dim}_entropy'] = float(-np.sum(probs * np.log(probs)))
            else:
                features[f'delay_H{dim}_entropy'] = 0

        delay_features.append(features)
    except:
        pass

print(f"Computed delay embedding features for {len(delay_features)} curves")

# Analyze delay features
delay_feat_names = [k for k in delay_features[0].keys() if k not in ['rank', 'label']]
X_delay = np.array([[df[fn] for fn in delay_feat_names] for df in delay_features])
y_delay = np.array([df['rank'] for df in delay_features])

print("\n--- Delay embedding persistence features by rank ---")
for fn in delay_feat_names:
    fidx = delay_feat_names.index(fn)
    vals_by_rank = {}
    for r in sorted(np.unique(y_delay)):
        mask = y_delay == r
        vals = X_delay[mask, fidx]
        vals_by_rank[r] = (vals.mean(), vals.std())

    # Check if feature discriminates
    means = [vals_by_rank[r][0] for r in sorted(vals_by_rank.keys()) if r in [0, 1, 2]]
    if len(means) >= 2 and max(means) - min(means) > 0.01:
        print(f"  {fn}: ", end="")
        for r in sorted(vals_by_rank.keys()):
            m, s = vals_by_rank[r]
            print(f"rank{r}={m:.3f}+/-{s:.3f}  ", end="")
        print()

# Classification with delay features
X_delay_scaled = StandardScaler().fit_transform(X_delay)
y_binary_delay = (y_delay >= 1).astype(int)

print(f"\nDelay embedding classification (rank 0 vs >=1):")
for clf_name, clf in [("SVM-RBF", SVC(kernel='rbf', C=10, gamma='scale')),
                      ("RF", RandomForestClassifier(n_estimators=100, random_state=42))]:
    scores = cross_val_score(clf, X_delay_scaled, y_binary_delay, cv=cv, scoring='accuracy')
    print(f"  {clf_name}: {scores.mean():.3f} +/- {scores.std():.3f}")

# =====================================================================
# COMBINED: All TDA features together
# =====================================================================
print("\n" + "="*70)
print("COMBINED ANALYSIS: All TDA features")
print("="*70)

# Merge prime-space and delay features (aligned by curve index)
# Build combined feature matrix
n_common = min(len(curve_features), len(delay_features))
X_all_tda = np.column_stack([
    X_tda_scaled[:n_common],
    X_delay_scaled[:n_common],
])
y_all = y_rank[:n_common]
y_all_binary = (y_all >= 1).astype(int)

print(f"Combined TDA feature matrix: {X_all_tda.shape}")

print(f"\nCombined TDA — Binary (rank 0 vs >=1):")
for clf_name, clf in [("SVM-RBF", SVC(kernel='rbf', C=10, gamma='scale')),
                      ("RF", RandomForestClassifier(n_estimators=200, random_state=42))]:
    scores = cross_val_score(clf, X_all_tda, y_all_binary, cv=cv, scoring='accuracy')
    print(f"  {clf_name}: {scores.mean():.3f} +/- {scores.std():.3f}")

# Multi-class
mask_012_c = y_all <= 2
print(f"\nCombined TDA — 3-class (rank 0 vs 1 vs 2):")
for clf_name, clf in [("RF", RandomForestClassifier(n_estimators=200, random_state=42))]:
    scores = cross_val_score(clf, X_all_tda[mask_012_c], y_all[mask_012_c], cv=cv, scoring='accuracy')
    print(f"  {clf_name}: {scores.mean():.3f} +/- {scores.std():.3f}")

# =====================================================================
# DEEP DIVE: H_1 features and Sha
# =====================================================================
print("\n" + "="*70)
print("DEEP DIVE: H_1 loops and Sha(E)")
print("="*70)

# For curves with Sha > 1 (if any) or non-trivial Sha, check H_1 correlation
# Since all our Sha=1, let's check if H_1 features vary with other BSD invariants
print("Checking H_1 correlation with BSD invariants...")

tda_feats_array = np.array([[cf['H1_count'], cf['H1_max_life'], cf['H1_total_life'], cf['H1_entropy']]
                             for cf in curve_features])
conductors_cf = np.array([cf['conductor'] for cf in curve_features])

from scipy.stats import pearsonr, spearmanr

print("\n  Correlation of H_1 features with log(conductor):")
log_cond = np.log(conductors_cf)
for i, name in enumerate(['H1_count', 'H1_max_life', 'H1_total_life', 'H1_entropy']):
    r_p, p_p = pearsonr(tda_feats_array[:, i], log_cond)
    r_s, p_s = spearmanr(tda_feats_array[:, i], log_cond)
    print(f"    {name}: Pearson r={r_p:.4f} (p={p_p:.4f}), Spearman rho={r_s:.4f} (p={p_s:.4f})")

print("\n  Correlation of H_1 features with rank:")
for i, name in enumerate(['H1_count', 'H1_max_life', 'H1_total_life', 'H1_entropy']):
    r_p, p_p = pearsonr(tda_feats_array[:, i], y_rank[:len(curve_features)])
    r_s, p_s = spearmanr(tda_feats_array[:, i], y_rank[:len(curve_features)])
    print(f"    {name}: Pearson r={r_p:.4f} (p={p_p:.4f}), Spearman rho={r_s:.4f} (p={p_s:.4f})")

torsion_cf = np.array([curves[i]['torsion'] for i in range(len(curve_features))])
print("\n  Correlation of H_1 features with torsion order:")
for i, name in enumerate(['H1_count', 'H1_max_life', 'H1_total_life', 'H1_entropy']):
    r_s, p_s = spearmanr(tda_feats_array[:, i], torsion_cf)
    print(f"    {name}: Spearman rho={r_s:.4f} (p={p_s:.4f})")

# =====================================================================
# Persistence Landscapes comparison
# =====================================================================
print("\n" + "="*70)
print("PERSISTENCE LANDSCAPES BY RANK")
print("="*70)

def persistence_landscape(dgm, num_points=100, num_landscapes=5):
    """Compute persistence landscapes from a persistence diagram."""
    finite = dgm[dgm[:, 1] < np.inf]
    if len(finite) == 0:
        return np.zeros((num_landscapes, num_points))

    births = finite[:, 0]
    deaths = finite[:, 1]

    t_min = births.min()
    t_max = deaths.max()
    t_vals = np.linspace(t_min, t_max, num_points)

    # For each t, compute all tent function values
    landscapes = np.zeros((num_landscapes, num_points))

    for ti, t in enumerate(t_vals):
        tent_values = []
        for b, d in zip(births, deaths):
            mid = (b + d) / 2
            half_life = (d - b) / 2
            if b <= t <= d:
                tent_values.append(half_life - abs(t - mid))
            else:
                tent_values.append(0)

        tent_values.sort(reverse=True)
        for k in range(min(num_landscapes, len(tent_values))):
            landscapes[k, ti] = tent_values[k]

    return landscapes

# Compute average persistence landscapes by rank for H_1
print("Computing persistence landscapes by rank...")

rank_landscapes = {}
for r in [0, 1, 2]:
    landscapes_list = []
    mask = y_rank[:len(curve_features)] == r
    indices = np.where(mask)[0]

    for idx in indices:
        curve = curves[idx]
        X_prime = build_prime_space_cloud(curve, prime_list)
        X_prime_scaled = StandardScaler().fit_transform(X_prime)

        try:
            result = ripser(X_prime_scaled, maxdim=1, thresh=3.0)
            dgms = result['dgms']
            ls = persistence_landscape(dgms[1], num_points=50, num_landscapes=3)
            landscapes_list.append(ls)
        except:
            pass

    if len(landscapes_list) > 0:
        rank_landscapes[r] = np.mean(landscapes_list, axis=0)
        print(f"  Rank {r}: averaged {len(landscapes_list)} landscapes")

# Plot persistence landscapes
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for k in range(3):
    ax = axes[k]
    for r in sorted(rank_landscapes.keys()):
        ax.plot(rank_landscapes[r][k], label=f'Rank {r}', linewidth=2)
    ax.set_title(f'Landscape λ_{k+1} (H_1)')
    ax.legend()
    ax.set_xlabel('t')
    ax.set_ylabel(f'λ_{k+1}(t)')
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, 'C_persistence_landscapes_H1.png'), dpi=150)
plt.close()
print("Saved persistence landscapes plot")

# =====================================================================
# SUMMARY STATISTICS
# =====================================================================
print("\n" + "="*70)
print("SUMMARY OF ALL RESULTS")
print("="*70)

# Save all results
results = {
    'num_curves': len(curves),
    'rank_distribution': dict(zip(*[x.tolist() for x in np.unique(ranks, return_counts=True)])),
    'pca_variance_explained': pca.explained_variance_ratio_[:3].tolist(),
    'feature_names': feat_names,
    'delay_feature_names': delay_feat_names,
}

with open(os.path.join(RESULTS_DIR, 'tda_summary.json'), 'w') as f:
    json.dump(results, f, indent=2)

print("Results saved to results/tda_summary.json")
print("\nDone!")
