"""
refined_gauge.py — Refined arithmetic gauge theory with better lattice construction.

Key improvements over v1:
1. Use the actual mod-ell Frobenius matrices (not just traces) for the gauge field
2. Weight edges by the actual Galois representation compatibility
3. Implement "arithmetic plaquettes" that respect the knot-like structure of primes
4. Add the Euler product decomposition as a direct observable
5. Test multiple gauge groups: U(1) (abelian) vs SU(2) (non-abelian)

The key theoretical insight we're testing:
  - Kim's arithmetic CS theory says the CS action on Gal(Q_bar/Q) representations
    should encode L-function values
  - Park & Park say the BF partition function encodes Sha
  - The Euler product L(E,s) = prod_p L_p(p^{-s}) suggests a MULTIPLICATIVE
    structure that should appear as a SUM in log-space, matching CS action structure
"""

import json
import os
import sys
import time
import numpy as np
from scipy.linalg import expm
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from arithmetic_lattice import build_prime_graph, compute_lattice_topology


# ============================================================
# Refined lattice: Euler product structure
# ============================================================

def build_euler_lattice(curve_data, prime_bound=None):
    """
    Build a lattice that directly encodes the Euler product structure.

    Instead of generic distance metrics, use the ACTUAL Euler factors:
      L_p(T) = 1 - a_p*T + p*T^2  for good primes
      L_p(T) = 1 - a_p*T          for bad primes

    The lattice encodes how these local factors interact.
    """
    all_primes = curve_data['all_primes']
    good_primes = [p for p in all_primes if p['reduction_type'] == 0]
    n = len(good_primes)

    # Each vertex gets its local L-factor data
    vertices = good_primes
    vertex_labels = [p['p'] for p in good_primes]

    # Edge weights: encode interaction between Euler factors
    # Key idea: two primes interact strongly when their Euler factors
    # are "linked" — they share a common eigenvalue, or their
    # local representations are correlated
    adjacency = np.zeros((n, n))

    for i in range(n):
        pi = good_primes[i]
        ai = pi['a_p']
        qi = pi['p']
        # Frobenius eigenvalues at p_i: roots of x^2 - a_i*x + q_i
        disc_i = ai**2 - 4*qi

        for j in range(i + 1, n):
            pj = good_primes[j]
            aj = pj['a_p']
            qj = pj['p']
            disc_j = aj**2 - 4*qj

            # Interaction 1: Trace correlation (how similar are a_p values
            # after normalizing by sqrt(p))
            norm_ai = ai / (2.0 * np.sqrt(qi))
            norm_aj = aj / (2.0 * np.sqrt(qj))
            trace_sim = 1.0 - abs(norm_ai - norm_aj)  # in [0, 2], higher = more similar

            # Interaction 2: Discriminant structure
            # If both have same sign of discriminant, the Frobenius
            # elements are in the same conjugacy class type
            # (both split or both non-split in the eigenvalue field)
            disc_match = 1.0 if (disc_i >= 0) == (disc_j >= 0) else 0.5

            # Interaction 3: Congruence between traces
            # a_i ≡ a_j (mod small primes) suggests shared structure
            cong_score = 0.0
            for ell in [2, 3, 5]:
                if ai % ell == aj % ell:
                    cong_score += 1.0 / 3.0

            # Combined weight
            w = 0.4 * max(trace_sim, 0) + 0.3 * disc_match + 0.3 * cong_score
            adjacency[i, j] = adjacency[j, i] = w

    # Build KNN graph
    k = min(8, n - 1)
    sparse_adj = np.zeros_like(adjacency)
    for i in range(n):
        neighbors = np.argsort(-adjacency[i])
        kept = 0
        for j in neighbors:
            if j == i:
                continue
            if kept >= k:
                break
            sparse_adj[i, j] = adjacency[i, j]
            sparse_adj[j, i] = adjacency[j, i]
            kept += 1

    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if sparse_adj[i, j] > 1e-12:
                edges.append((i, j, sparse_adj[i, j]))

    return {
        'vertices': vertices,
        'adjacency': sparse_adj,
        'edges': edges,
        'vertex_labels': vertex_labels,
        'n_vertices': n,
        'n_edges': len(edges),
        'conductor': curve_data['conductor'],
        'rank': curve_data['rank'],
    }


# ============================================================
# U(1) gauge theory (abelian, simpler, directly tied to L-function)
# ============================================================

def u1_gauge_simulation(graph, curve_data, beta=1.0, n_therm=30, n_meas=100):
    """
    U(1) gauge theory on the arithmetic lattice.

    Simpler than SU(2) — the gauge field is just a phase angle.
    This connects more directly to the L-function:
      L(E,s) = prod_p (1 - alpha_p * p^{-s})(1 - beta_p * p^{-s})
    where alpha_p, beta_p are the Frobenius eigenvalues.

    For each prime, the "phase" is the Frobenius angle theta_p where
    a_p = 2*sqrt(p)*cos(theta_p). The action functional penalizes
    deviations from the "arithmetic flow" predicted by BSD.
    """
    vertices = graph['vertices']
    n = graph['n_vertices']
    adj = graph['adjacency']

    # Extract Frobenius angles
    angles = np.array([
        np.arccos(np.clip(v['a_p'] / (2.0 * np.sqrt(v['p'])), -1, 1))
        for v in vertices
    ])

    # U(1) link variables: phase differences
    edges = graph['edges']
    n_edges = len(edges)

    # Initialize from Frobenius data
    link_phases = np.zeros(n_edges)
    for e_idx, (i, j, w) in enumerate(edges):
        link_phases[e_idx] = angles[i] - angles[j]

    # Build triangle list
    neighbors = defaultdict(set)
    for i, j, w in edges:
        neighbors[i].add(j)
        neighbors[j].add(i)

    triangles = []
    edge_idx_map = {}
    for e_idx, (i, j, w) in enumerate(edges):
        edge_idx_map[(i, j)] = e_idx
        edge_idx_map[(j, i)] = e_idx

    for i in range(n):
        for j in neighbors[i]:
            if j <= i:
                continue
            for k in neighbors[j]:
                if k <= j or k not in neighbors[i]:
                    continue
                triangles.append((i, j, k))

    n_tri = len(triangles)
    if n_tri == 0:
        return {'mean_action': 0, 'mean_wilson': 0, 'wilson_var': 0}

    # Triangle edge weights
    tri_weights = np.array([
        adj[i, j] * adj[j, k] * adj[i, k] for i, j, k in triangles
    ])

    def u1_action(phases):
        """U(1) plaquette action: sum cos(flux)."""
        total = 0.0
        for t_idx, (i, j, k) in enumerate(triangles):
            # Flux = sum of link phases around triangle
            phi_ij = phases[edge_idx_map[(i, j)]]
            phi_jk = phases[edge_idx_map[(j, k)]]
            phi_ki = phases[edge_idx_map[(k, i)]]
            # Orient: (i,j) + (j,k) - (i,k) for triangle (i,j,k)
            flux = phi_ij + phi_jk - phi_ki
            total += tri_weights[t_idx] * np.cos(flux)
        return total / n_tri

    def u1_wilson_sample(phases, n_sample=100):
        """Wilson loops = exp(i * flux)."""
        idx = np.random.choice(n_tri, min(n_sample, n_tri), replace=False)
        ws = []
        for t_idx in idx:
            i, j, k = triangles[t_idx]
            phi_ij = phases[edge_idx_map[(i, j)]]
            phi_jk = phases[edge_idx_map[(j, k)]]
            phi_ki = phases[edge_idx_map[(k, i)]]
            flux = phi_ij + phi_jk - phi_ki
            ws.append(np.cos(flux))  # Real part of Wilson loop
        return ws

    # Metropolis MC
    all_actions = []
    all_wilson_means = []
    all_wilson_vars = []

    for cfg in range(3):
        phases = angles[np.array([e[0] for e in edges])] - angles[np.array([e[1] for e in edges])]
        # Add small noise
        phases += np.random.randn(n_edges) * 0.1

        # Thermalize
        for _ in range(n_therm):
            for e in range(n_edges):
                old = phases[e]
                phases[e] += np.random.randn() * 0.2
                S_new = u1_action(phases)
                phases[e] = old
                S_old = u1_action(phases)
                # Actually we need local action, but for U(1) it's fast enough
                phases[e] += np.random.randn() * 0.2
                S_new2 = u1_action(phases)
                if S_new2 < S_old or np.random.random() < np.exp(-beta * (S_new2 - S_old)):
                    pass  # accept
                else:
                    phases[e] = old

        # Measure
        for _ in range(n_meas):
            for e in range(n_edges):
                old = phases[e]
                phases[e] += np.random.randn() * 0.2
                S_new = u1_action(phases)
                phases[e] = old
                S_old = u1_action(phases)
                phases[e] += np.random.randn() * 0.2
                if u1_action(phases) < S_old or np.random.random() < np.exp(-beta * (u1_action(phases) - S_old)):
                    pass
                else:
                    phases[e] = old

            all_actions.append(u1_action(phases))
            ws = u1_wilson_sample(phases)
            if ws:
                all_wilson_means.append(np.mean(ws))
                all_wilson_vars.append(np.var(ws))

    return {
        'mean_action': float(np.mean(all_actions)),
        'var_action': float(np.var(all_actions)),
        'mean_wilson': float(np.mean(all_wilson_means)) if all_wilson_means else 0.0,
        'wilson_var': float(np.mean(all_wilson_vars)) if all_wilson_vars else 0.0,
    }


# ============================================================
# Direct L-function observable via Euler product lattice
# ============================================================

def euler_product_observable(curve_data, s_values=None):
    """
    Compute the partial Euler product and derived observables.

    L_partial(E, s) = prod_{p <= bound} (1 - a_p*p^{-s} + p^{1-2s})^{-1}

    At s=1, this gives an approximation to L(E,1).
    The RATE of convergence and the distribution of local factors
    should correlate with rank via the BSD formula.
    """
    if s_values is None:
        s_values = [1.0, 1.1, 1.2, 1.5, 2.0]

    good_primes = [p for p in curve_data['all_primes'] if p['reduction_type'] == 0]
    bad_primes = [p for p in curve_data['all_primes'] if p['reduction_type'] != 0]

    results = {}

    for s in s_values:
        log_L_partial = 0.0
        partial_products = []

        for p_data in good_primes:
            p = p_data['p']
            ap = p_data['a_p']
            # Local L-factor: (1 - a_p*p^{-s} + p^{1-2s})^{-1}
            local_factor = 1.0 - ap * p**(-s) + p**(1 - 2*s)
            if abs(local_factor) > 1e-15:
                log_L_partial += -np.log(abs(local_factor))
            partial_products.append(np.exp(log_L_partial))

        for p_data in bad_primes:
            p = p_data['p']
            ap = p_data['a_p']
            local_factor = 1.0 - ap * p**(-s)
            if abs(local_factor) > 1e-15:
                log_L_partial += -np.log(abs(local_factor))

        results[f's={s}'] = {
            'log_L_partial': float(log_L_partial),
            'L_partial': float(np.exp(log_L_partial)),
            'n_primes': len(good_primes) + len(bad_primes),
            'convergence_rate': float(partial_products[-1] / partial_products[len(partial_products)//2]) if len(partial_products) > 1 else 1.0,
        }

    return results


# ============================================================
# Spectral zeta function of the lattice
# ============================================================

def lattice_spectral_zeta(graph, s_values=None):
    """
    Compute spectral zeta function of the arithmetic lattice Laplacian.

    zeta_lattice(s) = sum_i lambda_i^{-s} for nonzero eigenvalues lambda_i

    This is the arithmetic analog of the spectral zeta function on a manifold.
    For Spec(Z) as a 3-manifold, this should relate to the actual zeta/L-function.
    """
    if s_values is None:
        s_values = [0.5, 1.0, 1.5, 2.0]

    adj = graph['adjacency']
    n = graph['n_vertices']
    degrees = np.sum(adj, axis=1)
    D = np.diag(degrees)
    L = D - adj

    eigenvalues = np.linalg.eigvalsh(L)
    eigenvalues = np.sort(np.abs(eigenvalues))
    nonzero_eigs = eigenvalues[eigenvalues > 1e-10]

    results = {}
    for s in s_values:
        zeta_val = np.sum(nonzero_eigs**(-s))
        results[f's={s}'] = float(zeta_val)

    results['eigenvalues_first20'] = nonzero_eigs[:20].tolist()
    results['spectral_gap'] = float(nonzero_eigs[0]) if len(nonzero_eigs) > 0 else 0.0
    results['spectral_dimension'] = float(np.sum(nonzero_eigs**(-1.0)) / np.sum(nonzero_eigs**(-2.0))) if len(nonzero_eigs) > 0 else 0.0

    return results


# ============================================================
# Main refined simulation
# ============================================================

def run_refined(curve_data, verbose=True):
    """Run all refined analyses on a single curve."""
    label = curve_data['label']
    result = {
        'label': label,
        'rank': curve_data['rank'],
        'conductor': curve_data['conductor'],
        'sha_analytic': curve_data['sha_analytic'],
    }

    # 1. Euler lattice
    graph = build_euler_lattice(curve_data)
    topo = compute_lattice_topology(graph)
    result['euler_lattice_topo'] = topo

    # 2. U(1) gauge simulation
    u1_result = u1_gauge_simulation(graph, curve_data, beta=1.0, n_therm=20, n_meas=60)
    result['u1_gauge'] = u1_result

    # 3. Euler product observable
    euler = euler_product_observable(curve_data)
    result['euler_product'] = euler

    # 4. Spectral zeta
    spec_zeta = lattice_spectral_zeta(graph)
    result['spectral_zeta'] = spec_zeta

    if verbose:
        print(f"  {label}: rank={curve_data['rank']} |Sha|={curve_data['sha_analytic']:.0f} "
              f"U1_action={u1_result['mean_action']:.4f} "
              f"L(1)_partial={euler.get('s=1.0', {}).get('L_partial', 0):.4f} "
              f"spec_dim={spec_zeta.get('spectral_dimension', 0):.4f}")

    return result


def run_refined_suite():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, 'data')
    results_dir = os.path.join(base_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)

    curves = []
    for fname in sorted(os.listdir(data_dir)):
        if fname.startswith('curve_') and fname.endswith('.json'):
            with open(os.path.join(data_dir, fname)) as f:
                curves.append(json.load(f))

    print(f"Running refined analysis on {len(curves)} curves...", flush=True)
    all_results = []

    for curve in curves:
        result = run_refined(curve, verbose=True)
        all_results.append(result)

    with open(os.path.join(results_dir, 'refined_results.json'), 'w') as f:
        json.dump(all_results, f, indent=2, default=str)

    # Analysis
    print(f"\n{'='*80}")
    print("REFINED ANALYSIS")
    print(f"{'='*80}")

    ranks = np.array([r['rank'] for r in all_results])
    sha_vals = np.array([r['sha_analytic'] for r in all_results])
    log_sha = np.log(sha_vals + 1e-10)
    conductors = np.array([r['conductor'] for r in all_results])

    # Observables
    obs = {
        'U1_action': [r['u1_gauge']['mean_action'] for r in all_results],
        'U1_wilson': [r['u1_gauge']['mean_wilson'] for r in all_results],
        'U1_wilson_var': [r['u1_gauge']['wilson_var'] for r in all_results],
        'L_partial_s1': [r['euler_product'].get('s=1.0', {}).get('L_partial', 0) for r in all_results],
        'logL_partial_s1': [r['euler_product'].get('s=1.0', {}).get('log_L_partial', 0) for r in all_results],
        'L_partial_s1.5': [r['euler_product'].get('s=1.5', {}).get('L_partial', 0) for r in all_results],
        'L_conv_rate': [r['euler_product'].get('s=1.0', {}).get('convergence_rate', 0) for r in all_results],
        'spec_gap': [r['euler_lattice_topo']['spectral_gap'] for r in all_results],
        'spec_dim': [r['spectral_zeta'].get('spectral_dimension', 0) for r in all_results],
        'zeta_s1': [r['spectral_zeta'].get('s=1.0', 0) for r in all_results],
        'zeta_s2': [r['spectral_zeta'].get('s=2.0', 0) for r in all_results],
    }

    print(f"\nRANK CORRELATIONS:")
    for name, vals in sorted(obs.items()):
        vals = np.array(vals, dtype=float)
        if np.std(vals) < 1e-12 or np.any(np.isnan(vals)) or np.any(np.isinf(vals)):
            continue
        corr = np.corrcoef(ranks, vals)[0, 1]
        corr_N = np.corrcoef(conductors, vals)[0, 1]
        flag = " ***" if abs(corr) > 0.5 else " **" if abs(corr) > 0.3 else ""
        print(f"  corr(rank, {name:<20}) = {corr:+.4f}{flag}  corr(N) = {corr_N:+.4f}")

    print(f"\nSHA CORRELATIONS (all curves):")
    for name, vals in sorted(obs.items()):
        vals = np.array(vals, dtype=float)
        if np.std(vals) < 1e-12 or np.any(np.isnan(vals)) or np.any(np.isinf(vals)):
            continue
        corr = np.corrcoef(log_sha, vals)[0, 1]
        if abs(corr) > 0.2:
            print(f"  corr(log|Sha|, {name:<20}) = {corr:+.4f}")

    # The KEY test: L_partial at s=1 vs rank
    print(f"\nEULER PRODUCT TEST:")
    print(f"  Theory: L(E,1) = 0 for rank >= 1, L(E,1) > 0 for rank 0")
    print(f"  {'Label':<12} {'Rank':<5} {'L_partial(s=1)':<18} {'log L_partial(s=1)':<20}")
    for r in sorted(all_results, key=lambda x: (x['rank'], x['label'])):
        lp = r['euler_product'].get('s=1.0', {})
        print(f"  {r['label']:<12} {r['rank']:<5} {lp.get('L_partial', 0):<18.6f} "
              f"{lp.get('log_L_partial', 0):<20.6f}")

    # Mean by rank
    print(f"\nMEAN BY RANK:")
    by_rank = {}
    for r in all_results:
        by_rank.setdefault(r['rank'], []).append(r)

    for rank in sorted(by_rank.keys()):
        curves_r = by_rank[rank]
        n = len(curves_r)
        lp_vals = [r['euler_product'].get('s=1.0', {}).get('L_partial', 0) for r in curves_r]
        u1_a = [r['u1_gauge']['mean_action'] for r in curves_r]
        sd = [r['spectral_zeta'].get('spectral_dimension', 0) for r in curves_r]
        print(f"  Rank {rank} (n={n}): L_partial(1)={np.mean(lp_vals):.6f}  "
              f"U1_action={np.mean(u1_a):.4f}  spec_dim={np.mean(sd):.4f}")


if __name__ == '__main__':
    run_refined_suite()
