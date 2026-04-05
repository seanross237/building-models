"""
run_focused.py — Run focused simulation on key test curves.

Selects curves that maximize diagnostic power:
- Rank 0 with varying Sha (1, 4, 9, 25, 49) to test BF theory
- Ranks 0, 1, 2, 3 with Sha=1 to test rank detection
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
    scan_beta, TriangleLattice
)


def load_curve(data_dir, label):
    with open(os.path.join(data_dir, f"curve_{label}.json")) as f:
        return json.load(f)


def run_focused_suite():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, 'data')
    results_dir = os.path.join(base_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)

    # Key curves for diagnostics
    rank_test_curves = ['11a1', '37a1', '389a1', '5077a1']  # ranks 0,1,2,3
    sha_test_curves = ['11a1', '960d1', '681b1', '2932a1', '1058d1', '1246b1', '3364c1']

    all_labels = list(dict.fromkeys(rank_test_curves + sha_test_curves))

    all_results = []

    for label in all_labels:
        print(f"\n{'='*70}", flush=True)
        curve = load_curve(data_dir, label)
        print(f"CURVE: {label}  |  rank={curve['rank']}  |  N={curve['conductor']}  |  |Sha|={curve['sha_analytic']:.0f}", flush=True)
        print(f"{'='*70}", flush=True)

        t_total = time.time()

        results = {
            'label': label,
            'rank': curve['rank'],
            'conductor': curve['conductor'],
            'sha_analytic': curve['sha_analytic'],
            'torsion_order': curve.get('torsion_order', 1),
            'bsd_leading_coefficient': curve.get('bsd_leading_coefficient', None),
        }

        for metric in ['galois', 'frobenius_angle', 'mixed']:
            print(f"\n  --- Distance metric: {metric} ---", flush=True)
            # Use KNN=8 for sparse graph (manageable triangles)
            graph = build_prime_graph(curve, connectivity='knn', distance_metric=metric)
            topo = compute_lattice_topology(graph)
            tri = TriangleLattice(graph)
            print(f"  Lattice: {graph['n_vertices']}v, {graph['n_edges']}e, "
                  f"{tri.n_triangles} triangles, spectral_gap={topo['spectral_gap']:.4f}", flush=True)

            # Chern-Simons
            t0 = time.time()
            cs = compute_partition_function(
                graph, action_type='cs', beta=1.0,
                n_thermalize=30, n_measure=100, epsilon=0.15, n_configs=3
            )
            dt = time.time() - t0
            print(f"  CS:  <S>={cs['mean_action']:.6f}  log(Z)={cs['log_partition_function']:.4f}  "
                  f"<W>={cs['mean_wilson_loop']:.4f}  ({dt:.1f}s)", flush=True)

            # BF theory
            t0 = time.time()
            bf = compute_partition_function(
                graph, action_type='bf', beta=1.0,
                n_thermalize=30, n_measure=100, epsilon=0.15, n_configs=3
            )
            dt = time.time() - t0
            print(f"  BF:  <S>={bf['mean_action']:.6f}  log(Z)={bf['log_partition_function']:.4f}  "
                  f"<W>={bf['mean_wilson_loop']:.4f}  ({dt:.1f}s)", flush=True)

            # Wilson rank estimation
            t0 = time.time()
            wilson = estimate_rank_from_wilson(graph, n_thermalize=20, n_measure=60)
            dt = time.time() - t0
            print(f"  Wilson: <W>={wilson['wilson_mean']:.4f}  Var(W)={wilson['wilson_var']:.6f}  ({dt:.1f}s)", flush=True)

            results[f'{metric}_topology'] = topo
            results[f'{metric}_cs'] = cs
            results[f'{metric}_bf'] = bf
            results[f'{metric}_wilson'] = wilson

        # Multi-beta BF scan for Sha estimation (mixed metric only)
        print(f"\n  --- BF beta scan for Sha estimation ---", flush=True)
        graph = build_prime_graph(curve, connectivity='knn', distance_metric='mixed')
        betas = np.array([0.1, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0])
        bf_scan = []
        for beta in betas:
            bf_beta = compute_partition_function(
                graph, action_type='bf', beta=beta,
                n_thermalize=15, n_measure=60, epsilon=0.15, n_configs=2
            )
            bf_scan.append(bf_beta)
            print(f"    beta={beta:<6.1f} <S_BF>={bf_beta['mean_action']:.6f}  "
                  f"log(Z)={bf_beta['log_partition_function']:.4f}", flush=True)
        results['bf_beta_scan'] = bf_scan

        t_elapsed = time.time() - t_total
        results['total_time'] = t_elapsed
        print(f"\n  Total time: {t_elapsed:.1f}s", flush=True)

        all_results.append(results)

        # Save individual
        with open(os.path.join(results_dir, f'focused_{label}.json'), 'w') as f:
            json.dump(results, f, indent=2, default=str)

    # Save combined
    with open(os.path.join(results_dir, 'focused_all.json'), 'w') as f:
        json.dump(all_results, f, indent=2, default=str)

    # Analysis
    analyze_results(all_results, rank_test_curves, sha_test_curves)

    return all_results


def analyze_results(all_results, rank_test_curves, sha_test_curves):
    print(f"\n\n{'='*80}")
    print("ANALYSIS")
    print(f"{'='*80}")

    print(f"\nRANK DISCRIMINATION (mixed metric)")
    print(f"{'Label':<12} {'Rank':<5} {'|Sha|':<6} {'<S_CS>':<12} {'<S_BF>':<12} "
          f"{'<W>':<10} {'Var(W)':<12} {'spec_gap':<10}")
    print("-" * 85)
    for r in sorted(all_results, key=lambda x: (x['rank'], x['sha_analytic'])):
        cs = r.get('mixed_cs', {})
        bf = r.get('mixed_bf', {})
        wl = r.get('mixed_wilson', {})
        topo = r.get('mixed_topology', {})
        print(f"{r['label']:<12} {r['rank']:<5} {r['sha_analytic']:<6.0f} "
              f"{cs.get('mean_action', 0):<12.6f} {bf.get('mean_action', 0):<12.6f} "
              f"{wl.get('wilson_mean', 0):<10.4f} {wl.get('wilson_var', 0):<12.6f} "
              f"{topo.get('spectral_gap', 0):<10.4f}")

    # Sha correlation
    print(f"\nSHA CORRELATION (BF theory, mixed metric)")
    sha_curves = [r for r in all_results if r['label'] in sha_test_curves]
    sha_vals = np.array([r['sha_analytic'] for r in sha_curves])
    log_sha = np.log(sha_vals + 1e-10)

    for metric in ['galois', 'frobenius_angle', 'mixed']:
        bf_actions = np.array([r.get(f'{metric}_bf', {}).get('mean_action', 0) for r in sha_curves])
        bf_logZ = np.array([r.get(f'{metric}_bf', {}).get('log_partition_function', 0) for r in sha_curves])
        if np.std(bf_actions) > 1e-12 and np.std(log_sha) > 1e-12:
            corr_action = np.corrcoef(log_sha, bf_actions)[0, 1]
            corr_logZ = np.corrcoef(log_sha, bf_logZ)[0, 1]
            print(f"  [{metric}] corr(log|Sha|, <S_BF>)={corr_action:+.4f}  "
                  f"corr(log|Sha|, logZ_BF)={corr_logZ:+.4f}")

    # Rank correlations
    print(f"\nRANK CORRELATIONS (all metrics)")
    rank_curves = [r for r in all_results if r['label'] in rank_test_curves]
    ranks = np.array([r['rank'] for r in rank_curves])
    for metric in ['galois', 'frobenius_angle', 'mixed']:
        for obs_name, key1, key2 in [
            ('<S_CS>', f'{metric}_cs', 'mean_action'),
            ('<S_BF>', f'{metric}_bf', 'mean_action'),
            ('logZ_CS', f'{metric}_cs', 'log_partition_function'),
            ('logZ_BF', f'{metric}_bf', 'log_partition_function'),
            ('<W>', f'{metric}_wilson', 'wilson_mean'),
            ('Var(W)', f'{metric}_wilson', 'wilson_var'),
            ('spec_gap', f'{metric}_topology', 'spectral_gap'),
        ]:
            vals = np.array([r.get(key1, {}).get(key2, 0) for r in rank_curves])
            if np.std(vals) > 1e-12:
                corr = np.corrcoef(ranks, vals)[0, 1]
                if abs(corr) > 0.5:
                    flag = " ***"
                elif abs(corr) > 0.3:
                    flag = " **"
                else:
                    flag = ""
                print(f"  [{metric:<16}] corr(rank, {obs_name:<10}) = {corr:+.4f}{flag}")

    # Detailed rank-by-rank means
    print(f"\nMEAN OBSERVABLES BY RANK (mixed metric)")
    by_rank = {}
    for r in all_results:
        rank = r['rank']
        if rank not in by_rank:
            by_rank[rank] = []
        by_rank[rank].append(r)

    for rank in sorted(by_rank.keys()):
        curves_r = by_rank[rank]
        n = len(curves_r)
        cs_actions = [r.get('mixed_cs', {}).get('mean_action', 0) for r in curves_r]
        bf_actions = [r.get('mixed_bf', {}).get('mean_action', 0) for r in curves_r]
        wilsons = [r.get('mixed_wilson', {}).get('wilson_mean', 0) for r in curves_r]
        wilson_vars = [r.get('mixed_wilson', {}).get('wilson_var', 0) for r in curves_r]
        print(f"  Rank {rank} (n={n}): <S_CS>={np.mean(cs_actions):.6f}  <S_BF>={np.mean(bf_actions):.6f}  "
              f"<W>={np.mean(wilsons):.4f}  Var(W)={np.mean(wilson_vars):.6f}")


if __name__ == '__main__':
    run_focused_suite()
