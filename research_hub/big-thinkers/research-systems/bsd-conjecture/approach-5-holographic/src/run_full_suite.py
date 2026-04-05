"""
run_full_suite.py — Run simulation on ALL 25+ curves for statistical validation.

Uses the fastest configuration (frobenius_angle metric with KNN graph)
since the initial analysis showed it gives the best rank correlations.
"""

import json
import os
import sys
import time
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from arithmetic_lattice import build_prime_graph, compute_lattice_topology
from gauge_theory import (
    compute_partition_function, estimate_rank_from_wilson,
    TriangleLattice
)


def run_full():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, 'data')
    results_dir = os.path.join(base_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)

    # Load all curves
    curves = []
    for fname in sorted(os.listdir(data_dir)):
        if fname.startswith('curve_') and fname.endswith('.json'):
            with open(os.path.join(data_dir, fname)) as f:
                curves.append(json.load(f))

    print(f"Running on {len(curves)} curves", flush=True)

    all_results = []

    for curve in curves:
        label = curve['label']
        t0 = time.time()
        print(f"\n{label}: rank={curve['rank']}, N={curve['conductor']}, |Sha|={curve['sha_analytic']:.0f}", flush=True)

        result = {
            'label': label,
            'rank': curve['rank'],
            'conductor': curve['conductor'],
            'sha_analytic': curve['sha_analytic'],
            'torsion_order': curve.get('torsion_order', 1),
        }

        for metric in ['frobenius_angle', 'mixed']:
            graph = build_prime_graph(curve, connectivity='knn', distance_metric=metric)
            topo = compute_lattice_topology(graph)

            # CS simulation
            cs = compute_partition_function(
                graph, action_type='cs', beta=1.0,
                n_thermalize=25, n_measure=80, epsilon=0.15, n_configs=2
            )

            # BF simulation
            bf = compute_partition_function(
                graph, action_type='bf', beta=1.0,
                n_thermalize=25, n_measure=80, epsilon=0.15, n_configs=2
            )

            # BF at beta=2 (optimal for Sha detection)
            bf2 = compute_partition_function(
                graph, action_type='bf', beta=2.0,
                n_thermalize=25, n_measure=80, epsilon=0.15, n_configs=2
            )

            # Wilson loops
            wilson = estimate_rank_from_wilson(graph, n_thermalize=15, n_measure=50)

            result[f'{metric}_topo'] = topo
            result[f'{metric}_cs'] = cs
            result[f'{metric}_bf'] = bf
            result[f'{metric}_bf2'] = bf2
            result[f'{metric}_wilson'] = wilson

        dt = time.time() - t0
        result['time'] = dt
        print(f"  {dt:.1f}s  CS={result['frobenius_angle_cs']['mean_action']:.4f}  "
              f"BF={result['frobenius_angle_bf']['mean_action']:.4f}  "
              f"W={result['frobenius_angle_wilson']['wilson_mean']:.4f}  "
              f"Wvar={result['frobenius_angle_wilson']['wilson_var']:.6f}", flush=True)

        all_results.append(result)

    # Save
    with open(os.path.join(results_dir, 'full_suite.json'), 'w') as f:
        json.dump(all_results, f, indent=2, default=str)

    # Analysis
    print(f"\n\n{'='*80}")
    print("FULL SUITE ANALYSIS")
    print(f"{'='*80}")

    ranks = np.array([r['rank'] for r in all_results])
    sha_vals = np.array([r['sha_analytic'] for r in all_results])
    conductors = np.array([r['conductor'] for r in all_results])

    for metric in ['frobenius_angle', 'mixed']:
        print(f"\n--- {metric} ---")

        obs_map = {
            'S_CS': [r[f'{metric}_cs']['mean_action'] for r in all_results],
            'S_BF': [r[f'{metric}_bf']['mean_action'] for r in all_results],
            'S_BF2': [r[f'{metric}_bf2']['mean_action'] for r in all_results],
            'logZ_CS': [r[f'{metric}_cs']['log_partition_function'] for r in all_results],
            'logZ_BF': [r[f'{metric}_bf']['log_partition_function'] for r in all_results],
            'logZ_BF2': [r[f'{metric}_bf2']['log_partition_function'] for r in all_results],
            'W': [r[f'{metric}_wilson']['wilson_mean'] for r in all_results],
            'W_var': [r[f'{metric}_wilson']['wilson_var'] for r in all_results],
            'spec_gap': [r[f'{metric}_topo']['spectral_gap'] for r in all_results],
            'mean_degree': [r[f'{metric}_topo']['mean_degree'] for r in all_results],
        }

        # Add derived
        w_arr = np.array(obs_map['W'])
        a_arr = np.array([r[f'{metric}_wilson']['action_mean'] for r in all_results])
        a_var = np.array([r[f'{metric}_wilson']['action_var'] for r in all_results])
        obs_map['S_susceptibility'] = (a_var / (a_arr**2 + 1e-10)).tolist()
        obs_map['W_susceptibility'] = (np.array(obs_map['W_var']) / (w_arr**2 + 1e-10)).tolist()

        for name, vals in sorted(obs_map.items()):
            vals = np.array(vals)
            if np.std(vals) < 1e-12:
                continue
            corr_rank = np.corrcoef(ranks, vals)[0, 1]
            flag = " ***" if abs(corr_rank) > 0.5 else " **" if abs(corr_rank) > 0.3 else ""
            print(f"  corr(rank, {name:<18}) = {corr_rank:+.4f}{flag}  "
                  f"corr(N, {name:<18}) = {np.corrcoef(conductors, vals)[0,1]:+.4f}")

    # Rank-by-rank summary
    print(f"\nMEAN BY RANK (frobenius_angle):")
    by_rank = {}
    for r in all_results:
        by_rank.setdefault(r['rank'], []).append(r)

    print(f"{'Rank':<6} {'n':<4} {'<S_CS>':<12} {'<S_BF>':<12} {'<W>':<10} {'Var(W)':<12} "
          f"{'S_susc':<12} {'spec_gap':<10}")
    for rank in sorted(by_rank.keys()):
        curves_r = by_rank[rank]
        n = len(curves_r)
        m = 'frobenius_angle'
        scs = np.mean([r[f'{m}_cs']['mean_action'] for r in curves_r])
        sbf = np.mean([r[f'{m}_bf']['mean_action'] for r in curves_r])
        wm = np.mean([r[f'{m}_wilson']['wilson_mean'] for r in curves_r])
        wv = np.mean([r[f'{m}_wilson']['wilson_var'] for r in curves_r])
        am = np.array([r[f'{m}_wilson']['action_mean'] for r in curves_r])
        av = np.array([r[f'{m}_wilson']['action_var'] for r in curves_r])
        ss = np.mean(av / (am**2 + 1e-10))
        sg = np.mean([r[f'{m}_topo']['spectral_gap'] for r in curves_r])
        print(f"{rank:<6} {n:<4} {scs:<12.6f} {sbf:<12.6f} {wm:<10.4f} {wv:<12.6f} "
              f"{ss:<12.6f} {sg:<10.4f}")

    # Sha analysis (rank 0 only)
    rank0 = [r for r in all_results if r['rank'] == 0]
    if len(rank0) > 2:
        sha_r0 = np.array([r['sha_analytic'] for r in rank0])
        log_sha = np.log(sha_r0 + 1e-10)
        print(f"\nSHA DETECTION (rank 0 only, n={len(rank0)}):")
        for metric in ['frobenius_angle', 'mixed']:
            bf_a = np.array([r[f'{metric}_bf']['mean_action'] for r in rank0])
            bf2_a = np.array([r[f'{metric}_bf2']['mean_action'] for r in rank0])
            bf_z = np.array([r[f'{metric}_bf']['log_partition_function'] for r in rank0])
            bf2_z = np.array([r[f'{metric}_bf2']['log_partition_function'] for r in rank0])
            w_mean = np.array([r[f'{metric}_wilson']['wilson_mean'] for r in rank0])

            if np.std(log_sha) > 1e-10:
                print(f"  [{metric}]")
                print(f"    corr(log|Sha|, S_BF_b1)  = {np.corrcoef(log_sha, bf_a)[0,1]:+.4f}")
                print(f"    corr(log|Sha|, S_BF_b2)  = {np.corrcoef(log_sha, bf2_a)[0,1]:+.4f}")
                print(f"    corr(log|Sha|, logZ_BF1) = {np.corrcoef(log_sha, bf_z)[0,1]:+.4f}")
                print(f"    corr(log|Sha|, logZ_BF2) = {np.corrcoef(log_sha, bf2_z)[0,1]:+.4f}")
                print(f"    corr(log|Sha|, W_mean)   = {np.corrcoef(log_sha, w_mean)[0,1]:+.4f}")


if __name__ == '__main__':
    run_full()
