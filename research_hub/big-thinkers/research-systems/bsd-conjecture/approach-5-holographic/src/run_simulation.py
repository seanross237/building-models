"""
run_simulation.py — Main simulation driver.

Runs the full arithmetic gauge theory pipeline:
1. Load curve data (from JSON files extracted by curve_data.py)
2. Build arithmetic lattice
3. Run Chern-Simons gauge theory simulation
4. Run BF theory simulation
5. Extract observables and compare to known BSD invariants
6. Output results

Can be run with standard Python (does not require SageMath).
"""

import json
import os
import sys
import time
import numpy as np
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from arithmetic_lattice import build_prime_graph, compute_lattice_topology
from gauge_theory import (
    compute_partition_function, estimate_sha_from_bf,
    estimate_rank_from_wilson, scan_beta, GaugeConfig,
    chern_simons_action, bf_theory_action, wilson_loops_all_triangles
)


def load_curve_data(data_dir, label):
    """Load a single curve's data from JSON."""
    path = os.path.join(data_dir, f"curve_{label}.json")
    with open(path) as f:
        return json.load(f)


def load_all_curves(data_dir):
    """Load all curve data files."""
    curves = []
    for fname in sorted(os.listdir(data_dir)):
        if fname.startswith('curve_') and fname.endswith('.json'):
            with open(os.path.join(data_dir, fname)) as f:
                curves.append(json.load(f))
    return curves


def run_single_curve(curve_data, verbose=True):
    """
    Run full simulation pipeline for a single curve.

    Returns a results dict with all observables and comparisons.
    """
    label = curve_data['label']
    if verbose:
        print(f"\n{'='*60}")
        print(f"CURVE: {label}  |  rank={curve_data['rank']}  |  N={curve_data['conductor']}  |  |Sha|={curve_data['sha_analytic']:.2f}")
        print(f"{'='*60}")

    results = {
        'label': label,
        'rank': curve_data['rank'],
        'conductor': curve_data['conductor'],
        'sha_analytic': curve_data['sha_analytic'],
        'bsd_leading_coefficient': curve_data.get('bsd_leading_coefficient', None),
        'torsion_order': curve_data.get('torsion_order', 1),
    }

    # Step 1: Build arithmetic lattice with mixed distance metric
    t0 = time.time()
    graph = build_prime_graph(curve_data, connectivity='full', distance_metric='mixed')
    t_lattice = time.time() - t0

    if verbose:
        print(f"\n  Lattice: {graph['n_vertices']} vertices, {graph['n_edges']} edges "
              f"({t_lattice:.2f}s)")

    results['n_vertices'] = graph['n_vertices']
    results['n_edges'] = graph['n_edges']

    # Step 2: Lattice topology
    topo = compute_lattice_topology(graph)
    results['lattice_topology'] = topo
    if verbose:
        print(f"  Topology: betti_0={topo['betti_0']}, spectral_gap={topo['spectral_gap']:.4f}, "
              f"mean_degree={topo['mean_degree']:.2f}")

    # Step 3: Chern-Simons simulation
    if verbose:
        print(f"\n  Running Chern-Simons simulation...")
    t0 = time.time()
    cs_result = compute_partition_function(
        graph, action_type='cs', beta=1.0,
        n_thermalize=40, n_measure=150, epsilon=0.15, n_configs=3
    )
    t_cs = time.time() - t0
    results['chern_simons'] = cs_result
    if verbose:
        print(f"    <S_CS>={cs_result['mean_action']:.6f}, "
              f"log(Z_CS)={cs_result['log_partition_function']:.4f}, "
              f"<W>={cs_result['mean_wilson_loop']:.4f} ({t_cs:.1f}s)")

    # Step 4: BF theory simulation
    if verbose:
        print(f"\n  Running BF theory simulation (Sha detector)...")
    t0 = time.time()
    bf_result = compute_partition_function(
        graph, action_type='bf', beta=1.0,
        n_thermalize=40, n_measure=150, epsilon=0.15, n_configs=3
    )
    t_bf = time.time() - t0
    results['bf_theory'] = bf_result
    if verbose:
        print(f"    <S_BF>={bf_result['mean_action']:.6f}, "
              f"log(Z_BF)={bf_result['log_partition_function']:.4f}, "
              f"<W_BF>={bf_result['mean_wilson_loop']:.4f} ({t_bf:.1f}s)")

    # Step 5: Wilson loop rank estimator
    if verbose:
        print(f"\n  Running Wilson loop rank estimation...")
    t0 = time.time()
    wilson_result = estimate_rank_from_wilson(graph, n_thermalize=30, n_measure=100)
    t_wilson = time.time() - t0
    results['wilson_rank'] = wilson_result
    if verbose:
        print(f"    <W>={wilson_result['wilson_mean']:.4f}, "
              f"Var(W)={wilson_result['wilson_var']:.6f}, "
              f"<S>={wilson_result['action_mean']:.6f} ({t_wilson:.1f}s)")

    # Step 6: Beta scan for phase transitions
    if verbose:
        print(f"\n  Running beta scan (phase structure)...")
    t0 = time.time()
    betas = np.logspace(-0.5, 1.5, 10)
    beta_scan = scan_beta(
        graph, action_type='cs', betas=betas,
        n_thermalize=20, n_measure=60, epsilon=0.15
    )
    t_scan = time.time() - t0
    results['beta_scan'] = beta_scan
    if verbose:
        print(f"    Scanned {len(betas)} beta values ({t_scan:.1f}s)")

    results['timing'] = {
        'lattice': t_lattice,
        'chern_simons': t_cs,
        'bf_theory': t_bf,
        'wilson': t_wilson,
        'beta_scan': t_scan,
        'total': t_lattice + t_cs + t_bf + t_wilson + t_scan,
    }

    return results


def run_test_suite(data_dir, results_dir, max_curves=None, verbose=True):
    """Run simulation on all curves in the test suite."""
    curves = load_all_curves(data_dir)
    if max_curves:
        curves = curves[:max_curves]

    if verbose:
        print(f"Running simulation on {len(curves)} curves...")
        print(f"Data dir: {data_dir}")
        print(f"Results dir: {results_dir}")

    os.makedirs(results_dir, exist_ok=True)
    all_results = []

    for curve in curves:
        try:
            result = run_single_curve(curve, verbose=verbose)
            all_results.append(result)

            # Save individual result
            fname = os.path.join(results_dir, f"result_{curve['label']}.json")
            with open(fname, 'w') as f:
                json.dump(result, f, indent=2, default=str)

        except Exception as e:
            print(f"  ERROR on {curve['label']}: {e}")
            import traceback
            traceback.print_exc()

    # Save combined results
    combined_path = os.path.join(results_dir, 'all_results.json')
    with open(combined_path, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)

    if verbose:
        print(f"\n{'='*60}")
        print(f"SUITE COMPLETE: {len(all_results)} curves processed")
        print(f"Results saved to {results_dir}")

    return all_results


def quick_analysis(all_results):
    """Quick comparative analysis of simulation results."""
    print(f"\n{'='*70}")
    print("COMPARATIVE ANALYSIS")
    print(f"{'='*70}")

    # Group by rank
    by_rank = {}
    for r in all_results:
        rank = r['rank']
        if rank not in by_rank:
            by_rank[rank] = []
        by_rank[rank].append(r)

    print(f"\n{'Label':<12} {'Rank':<5} {'|Sha|':<8} {'<S_CS>':<12} {'<S_BF>':<12} "
          f"{'log(Z_CS)':<12} {'log(Z_BF)':<12} {'<W>':<10}")
    print("-" * 85)

    for rank in sorted(by_rank.keys()):
        for r in by_rank[rank]:
            cs = r.get('chern_simons', {})
            bf = r.get('bf_theory', {})
            wl = r.get('wilson_rank', {})
            print(f"{r['label']:<12} {r['rank']:<5} {r['sha_analytic']:<8.2f} "
                  f"{cs.get('mean_action', 0):<12.6f} {bf.get('mean_action', 0):<12.6f} "
                  f"{cs.get('log_partition_function', 0):<12.4f} "
                  f"{bf.get('log_partition_function', 0):<12.4f} "
                  f"{wl.get('wilson_mean', 0):<10.4f}")
        print()

    # Correlation analysis
    print("\nCORRELATION: Observables vs. Known Invariants")
    print("-" * 50)

    ranks = np.array([r['rank'] for r in all_results])
    sha_values = np.array([r['sha_analytic'] for r in all_results])
    conductors = np.array([r['conductor'] for r in all_results])

    observables = {
        '<S_CS>': np.array([r.get('chern_simons', {}).get('mean_action', 0) for r in all_results]),
        '<S_BF>': np.array([r.get('bf_theory', {}).get('mean_action', 0) for r in all_results]),
        'log(Z_CS)': np.array([r.get('chern_simons', {}).get('log_partition_function', 0) for r in all_results]),
        'log(Z_BF)': np.array([r.get('bf_theory', {}).get('log_partition_function', 0) for r in all_results]),
        '<W_CS>': np.array([r.get('wilson_rank', {}).get('wilson_mean', 0) for r in all_results]),
        'Var(W)': np.array([r.get('wilson_rank', {}).get('wilson_var', 0) for r in all_results]),
        'spectral_gap': np.array([r.get('lattice_topology', {}).get('spectral_gap', 0) for r in all_results]),
    }

    for name, values in observables.items():
        if len(values) > 2 and np.std(values) > 1e-12:
            corr_rank = np.corrcoef(ranks, values)[0, 1]
            corr_sha = np.corrcoef(sha_values, values)[0, 1] if np.std(sha_values) > 1e-12 else 0
            corr_cond = np.corrcoef(conductors, values)[0, 1]
            print(f"  {name:<15} | corr(rank)={corr_rank:+.4f} | "
                  f"corr(|Sha|)={corr_sha:+.4f} | corr(N)={corr_cond:+.4f}")

    # Rank discrimination
    print("\nRANK DISCRIMINATION (mean observable by rank)")
    print("-" * 60)
    for rank in sorted(by_rank.keys()):
        indices = [i for i, r in enumerate(all_results) if r['rank'] == rank]
        print(f"  Rank {rank} (n={len(indices)}):")
        for name, values in observables.items():
            mean_val = np.mean(values[indices])
            std_val = np.std(values[indices])
            print(f"    {name:<15}: {mean_val:+.6f} +/- {std_val:.6f}")

    return observables


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, 'data')
    results_dir = os.path.join(base_dir, 'results')

    if not os.path.exists(data_dir) or not os.listdir(data_dir):
        print("No curve data found. Run curve_data.py first under sage -python.")
        print(f"Expected data in: {data_dir}")
        sys.exit(1)

    all_results = run_test_suite(data_dir, results_dir, verbose=True)
    quick_analysis(all_results)
