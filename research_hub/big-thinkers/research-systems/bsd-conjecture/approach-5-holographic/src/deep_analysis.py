"""
deep_analysis.py — Deeper statistical analysis of simulation results.

Addresses key questions:
1. Which observables best discriminate rank?
2. Does the BF partition function encode |Sha|?
3. What is the optimal distance metric?
4. Phase transition structure via beta scans.
5. Calibration: can we BUILD a rank/Sha predictor?
"""

import json
import os
import sys
import numpy as np
from collections import defaultdict

def load_results(results_dir):
    path = os.path.join(results_dir, 'focused_all.json')
    with open(path) as f:
        return json.load(f)


def rank_analysis(results):
    """Deep rank discrimination analysis."""
    print("\n" + "="*80)
    print("RANK ANALYSIS")
    print("="*80)

    # Collect all observables across all metrics
    rank_test = [r for r in results if r['sha_analytic'] <= 1.5]  # Sha=1 curves only
    ranks = np.array([r['rank'] for r in rank_test])

    print(f"\nAnalyzing {len(rank_test)} curves with |Sha|=1")
    print(f"Rank distribution: {dict(zip(*np.unique(ranks, return_counts=True)))}")

    best_corrs = []

    for metric in ['galois', 'frobenius_angle', 'mixed']:
        print(f"\n--- Metric: {metric} ---")

        # Extract all observables
        obs = {}
        obs['S_CS'] = np.array([r[f'{metric}_cs']['mean_action'] for r in rank_test])
        obs['S_BF'] = np.array([r[f'{metric}_bf']['mean_action'] for r in rank_test])
        obs['logZ_CS'] = np.array([r[f'{metric}_cs']['log_partition_function'] for r in rank_test])
        obs['logZ_BF'] = np.array([r[f'{metric}_bf']['log_partition_function'] for r in rank_test])
        obs['Z_CS'] = np.array([r[f'{metric}_cs']['partition_function'] for r in rank_test])
        obs['Z_BF'] = np.array([r[f'{metric}_bf']['partition_function'] for r in rank_test])
        obs['W_mean'] = np.array([r[f'{metric}_wilson']['wilson_mean'] for r in rank_test])
        obs['W_var'] = np.array([r[f'{metric}_wilson']['wilson_var'] for r in rank_test])
        obs['S_action'] = np.array([r[f'{metric}_wilson']['action_mean'] for r in rank_test])
        obs['S_action_var'] = np.array([r[f'{metric}_wilson']['action_var'] for r in rank_test])
        obs['spec_gap'] = np.array([r[f'{metric}_topology']['spectral_gap'] for r in rank_test])
        obs['mean_degree'] = np.array([r[f'{metric}_topology']['mean_degree'] for r in rank_test])

        # Derived observables
        obs['W_susceptibility'] = obs['W_var'] / (obs['W_mean']**2 + 1e-10)
        obs['S_susceptibility'] = obs['S_action_var'] / (obs['S_action']**2 + 1e-10)
        obs['CS_BF_ratio'] = obs['S_CS'] / (obs['S_BF'] + 1e-10)
        obs['W_CS_product'] = obs['W_mean'] * obs['S_CS']

        for name, vals in sorted(obs.items()):
            if np.std(vals) < 1e-12:
                continue
            corr = np.corrcoef(ranks, vals)[0, 1]
            flag = " ***" if abs(corr) > 0.7 else " **" if abs(corr) > 0.5 else ""
            if abs(corr) > 0.3:
                print(f"  corr(rank, {name:<20}) = {corr:+.4f}{flag}")
                best_corrs.append((abs(corr), metric, name, corr))

    # Best overall correlators
    best_corrs.sort(reverse=True)
    print(f"\n--- TOP 10 RANK CORRELATORS ---")
    for i, (ac, metric, name, corr) in enumerate(best_corrs[:10]):
        print(f"  {i+1}. [{metric:<16}] {name:<20} r={corr:+.4f}")


def sha_analysis(results):
    """Deep Sha detection analysis."""
    print("\n" + "="*80)
    print("SHA ANALYSIS (BF Theory Partition Function)")
    print("="*80)

    # All rank-0 curves with varying Sha
    sha_curves = [r for r in results if r['rank'] == 0]
    sha_vals = np.array([r['sha_analytic'] for r in sha_curves])
    log_sha = np.log(sha_vals + 1e-10)

    print(f"\nAnalyzing {len(sha_curves)} rank-0 curves")
    print(f"|Sha| values: {sha_vals.tolist()}")

    best_corrs = []

    for metric in ['galois', 'frobenius_angle', 'mixed']:
        print(f"\n--- Metric: {metric} ---")

        obs = {}
        obs['S_BF'] = np.array([r[f'{metric}_bf']['mean_action'] for r in sha_curves])
        obs['logZ_BF'] = np.array([r[f'{metric}_bf']['log_partition_function'] for r in sha_curves])
        obs['Z_BF'] = np.array([r[f'{metric}_bf']['partition_function'] for r in sha_curves])
        obs['S_CS'] = np.array([r[f'{metric}_cs']['mean_action'] for r in sha_curves])
        obs['logZ_CS'] = np.array([r[f'{metric}_cs']['log_partition_function'] for r in sha_curves])
        obs['W_mean'] = np.array([r[f'{metric}_wilson']['wilson_mean'] for r in sha_curves])
        obs['W_var'] = np.array([r[f'{metric}_wilson']['wilson_var'] for r in sha_curves])
        obs['spec_gap'] = np.array([r[f'{metric}_topology']['spectral_gap'] for r in sha_curves])

        for name, vals in sorted(obs.items()):
            if np.std(vals) < 1e-12:
                continue
            corr_log = np.corrcoef(log_sha, vals)[0, 1]
            corr_lin = np.corrcoef(sha_vals, vals)[0, 1]
            flag = " ***" if abs(corr_log) > 0.5 else ""
            if abs(corr_log) > 0.2 or abs(corr_lin) > 0.2:
                print(f"  corr(log|Sha|, {name:<15}) = {corr_log:+.4f}  "
                      f"corr(|Sha|, {name:<15}) = {corr_lin:+.4f}{flag}")
                best_corrs.append((abs(corr_log), metric, name, corr_log))

    # Beta scan analysis for Sha
    print(f"\n--- BF BETA SCAN vs |Sha| ---")
    betas = [0.1, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0]

    for beta_idx, beta in enumerate(betas):
        bf_actions = []
        bf_logZ = []
        for r in sha_curves:
            scan = r.get('bf_beta_scan', [])
            if beta_idx < len(scan):
                bf_actions.append(scan[beta_idx]['mean_action'])
                bf_logZ.append(scan[beta_idx]['log_partition_function'])

        if len(bf_actions) == len(sha_curves):
            bf_actions = np.array(bf_actions)
            bf_logZ = np.array(bf_logZ)
            corr_action = np.corrcoef(log_sha, bf_actions)[0, 1]
            corr_logZ = np.corrcoef(log_sha, bf_logZ)[0, 1]
            flag = " ***" if abs(corr_action) > 0.4 or abs(corr_logZ) > 0.4 else ""
            print(f"  beta={beta:<6.1f}  corr(log|Sha|, <S_BF>)={corr_action:+.4f}  "
                  f"corr(log|Sha|, logZ_BF)={corr_logZ:+.4f}{flag}")

    best_corrs.sort(reverse=True)
    print(f"\n--- TOP 5 SHA CORRELATORS ---")
    for i, (ac, metric, name, corr) in enumerate(best_corrs[:5]):
        print(f"  {i+1}. [{metric:<16}] {name:<20} r={corr:+.4f}")


def phase_structure_analysis(results):
    """Analyze phase transition structure from beta scans."""
    print("\n" + "="*80)
    print("PHASE STRUCTURE ANALYSIS")
    print("="*80)

    betas = [0.1, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0]

    for r in results:
        scan = r.get('bf_beta_scan', [])
        if not scan:
            continue

        actions = [s['mean_action'] for s in scan[:len(betas)]]
        logZ_values = [s['log_partition_function'] for s in scan[:len(betas)]]

        # Look for specific heat (variance peak)
        if len(actions) >= 3:
            # Numerical derivative of <S> w.r.t. beta (specific heat)
            d_action = np.diff(actions) / np.diff(betas[:len(actions)])

            # Find beta where action changes most rapidly
            max_change_idx = np.argmax(np.abs(d_action))
            critical_beta = betas[max_change_idx]

            print(f"  {r['label']:<12} rank={r['rank']}  |Sha|={r['sha_analytic']:.0f}  "
                  f"critical_beta~{critical_beta:.1f}  "
                  f"d<S>/dbeta_max={d_action[max_change_idx]:+.4f}")


def combined_predictor(results):
    """Build a combined observable for rank prediction."""
    print("\n" + "="*80)
    print("COMBINED RANK PREDICTOR")
    print("="*80)

    # Use all curves
    n = len(results)
    ranks = np.array([r['rank'] for r in results])

    # Feature matrix
    features = []
    feature_names = []

    for metric in ['galois', 'frobenius_angle', 'mixed']:
        for key1, key2, name in [
            (f'{metric}_cs', 'mean_action', f'{metric}_S_CS'),
            (f'{metric}_bf', 'mean_action', f'{metric}_S_BF'),
            (f'{metric}_cs', 'log_partition_function', f'{metric}_logZ_CS'),
            (f'{metric}_bf', 'log_partition_function', f'{metric}_logZ_BF'),
            (f'{metric}_wilson', 'wilson_mean', f'{metric}_W'),
            (f'{metric}_wilson', 'wilson_var', f'{metric}_W_var'),
            (f'{metric}_topology', 'spectral_gap', f'{metric}_spec_gap'),
        ]:
            vals = np.array([r.get(key1, {}).get(key2, 0) for r in results])
            features.append(vals)
            feature_names.append(name)

    X = np.array(features).T  # (n_curves, n_features)

    # Standardize
    means = X.mean(axis=0)
    stds = X.std(axis=0)
    stds[stds < 1e-10] = 1.0
    X_std = (X - means) / stds

    # Simple least squares regression for rank prediction
    # rank ~ w^T x + b
    X_aug = np.column_stack([X_std, np.ones(n)])
    w, residuals, _, _ = np.linalg.lstsq(X_aug, ranks, rcond=None)

    predicted = X_aug @ w
    r2 = 1 - np.sum((ranks - predicted)**2) / np.sum((ranks - np.mean(ranks))**2)

    print(f"\nLinear model: R^2 = {r2:.4f}")
    print(f"\nPredictions:")
    print(f"{'Label':<12} {'True Rank':<12} {'Predicted':<12} {'Error':<10}")
    for i, r in enumerate(results):
        print(f"{r['label']:<12} {ranks[i]:<12} {predicted[i]:<12.3f} {abs(ranks[i]-predicted[i]):<10.3f}")

    # Top contributing features
    weights = w[:-1]  # exclude bias
    top_features = sorted(zip(np.abs(weights), weights, feature_names), reverse=True)
    print(f"\nTop contributing features:")
    for i, (aw, w_val, name) in enumerate(top_features[:10]):
        print(f"  {i+1}. {name:<30} weight={w_val:+.4f}")


def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    results_dir = os.path.join(base_dir, 'results')
    results = load_results(results_dir)

    rank_analysis(results)
    sha_analysis(results)
    phase_structure_analysis(results)
    combined_predictor(results)


if __name__ == '__main__':
    main()
