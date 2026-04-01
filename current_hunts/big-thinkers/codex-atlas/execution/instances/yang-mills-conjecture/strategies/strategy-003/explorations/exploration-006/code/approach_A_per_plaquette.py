"""
Approach A: Per-Plaquette Full Hessian Bound
Test whether ||H_□||_op ≤ 4 for all plaquettes and all Q.

H = Σ_□ H_□ where each H_□ includes both self-terms and cross-terms from plaquette □.
If ||H_□|| ≤ 4, then ||H|| ≤ Σ_□ max_{e in □} (overlap factor) × 4.

Each edge appears in 2(d-1) plaquettes. But the per-plaquette matrices overlap on
the same rows/columns, so the aggregation is NOT simply Σ ||H_□||.

The correct bound: v^T H v = Σ_□ v^T H_□ v, so λ_max(H) ≤ Σ_□ λ_max(H_□).
But H_□ acts on ALL edge-color indices (not just the 4×3=12 of the plaquette).
"""

import numpy as np
import sys, os, time
sys.path.insert(0, os.path.dirname(__file__))
from hessian_core import (
    Lattice, random_su2, su2_inv, su2_exp, project_su2,
    flat_config, random_config, anti_instanton_config,
    compute_hessian, compute_per_plaquette_hessian,
    plaquette_holonomy, isigma, get_link
)

def per_plaquette_norms(lat, Q, beta=1.0, N=2):
    """Compute ||H_□||_op for each plaquette."""
    norms = []
    for pidx in range(lat.nplaq):
        H_p = compute_per_plaquette_hessian(lat, Q, pidx, beta, N)
        # This is a full-dim matrix but sparse — only 12 rows/cols are nonzero
        ev = np.linalg.eigvalsh(H_p)
        norms.append(max(abs(ev[0]), abs(ev[-1])))
    return norms

def per_plaquette_restricted_norm(lat, Q, pidx, beta=1.0, N=2):
    """Compute norm of H_□ restricted to the 12-dim subspace of its edges."""
    plaq = lat.plaquettes[pidx]
    edges = [e for (e, s) in plaq]
    # Unique edges (may repeat if lattice wraps)
    edges_unique = list(dict.fromkeys(edges))

    # Build index mapping
    idx_map = []
    for e in edges_unique:
        for a in range(3):
            idx_map.append(3*e + a)

    H_p = compute_per_plaquette_hessian(lat, Q, pidx, beta, N)

    # Extract submatrix
    n = len(idx_map)
    H_sub = np.zeros((n, n))
    for i, ri in enumerate(idx_map):
        for j, rj in enumerate(idx_map):
            H_sub[i, j] = H_p[ri, rj]

    ev = np.linalg.eigvalsh(H_sub)
    return max(abs(ev[0]), abs(ev[-1])), ev

def main():
    d = 4
    L = 2
    lat = Lattice(d, L)
    ne = lat.nedges
    bound = 4 * d

    print(f"{'='*70}")
    print(f"APPROACH A: PER-PLAQUETTE FULL HESSIAN BOUND")
    print(f"d={d}, L={L}, nedges={ne}, nplaq={lat.nplaq}")
    print(f"{'='*70}")

    # ==================================================================
    # PHASE 1: PER-PLAQUETTE NORMS AT FLAT
    # ==================================================================
    print(f"\n{'='*60}")
    print("PHASE 1: FLAT CONFIG — per-plaquette norms")
    print(f"{'='*60}")

    Q = flat_config(lat)
    norms = per_plaquette_norms(lat, Q)
    print(f"||H_□|| at flat: min={min(norms):.6f}, max={max(norms):.6f}, mean={np.mean(norms):.4f}")
    print(f"Expected: 4 (each plaquette contributes self-term=2 and cross-term≤2)")

    # Restricted norm (just the 12 plaquette indices)
    for pidx in range(min(3, lat.nplaq)):
        rn, ev = per_plaquette_restricted_norm(lat, Q, pidx)
        print(f"  Plaq {pidx}: restricted ||H_□|| = {rn:.6f}, eigenvalues = "
              f"[{ev[0]:.4f}, ..., {ev[-1]:.4f}]")

    # Verify sum of per-plaquette = full Hessian
    H_full = compute_hessian(lat, Q)
    H_sum = sum(compute_per_plaquette_hessian(lat, Q, pidx) for pidx in range(lat.nplaq))
    err = np.max(np.abs(H_full - H_sum))
    print(f"\n||H_full - Σ H_□|| = {err:.2e} (should be ~0)")

    # ==================================================================
    # PHASE 2: RANDOM SURVEY
    # ==================================================================
    print(f"\n{'='*60}")
    print("PHASE 2: RANDOM SURVEY — per-plaquette norms (500 configs)")
    print(f"{'='*60}")

    rng = np.random.default_rng(42)
    max_plaq_norm = 0
    all_max_norms = []
    all_sum_norms = []
    violations_4 = 0
    t0 = time.time()

    for trial in range(500):
        Q = random_config(lat, rng)
        norms = per_plaquette_norms(lat, Q)
        max_n = max(norms)
        sum_n = sum(norms)
        all_max_norms.append(max_n)
        all_sum_norms.append(sum_n)
        if max_n > 4.001:
            violations_4 += 1
        max_plaq_norm = max(max_plaq_norm, max_n)

    elapsed = time.time() - t0
    print(f"Completed in {elapsed:.1f}s")
    print(f"\nmax ||H_□|| across all configs and plaquettes: {max_plaq_norm:.6f}")
    print(f"||H_□|| > 4: {violations_4}/500 configs have at least one plaquette exceeding 4")
    print(f"mean of max ||H_□||: {np.mean(all_max_norms):.4f}")
    print(f"\nSum of norms Σ||H_□||:")
    print(f"  max = {max(all_sum_norms):.4f}")
    print(f"  mean = {np.mean(all_sum_norms):.4f}")
    print(f"  This is an UPPER bound on ||H|| (triangle inequality)")

    # ==================================================================
    # PHASE 3: STRUCTURED + ADVERSARIAL
    # ==================================================================
    print(f"\n{'='*60}")
    print("PHASE 3: STRUCTURED CONFIGS")
    print(f"{'='*60}")

    configs = [
        ('flat', flat_config(lat)),
        ('anti-instanton', anti_instanton_config(lat)),
    ]

    # Uniform rotations
    for theta in [np.pi/4, np.pi/2, np.pi]:
        w = np.zeros(3); w[2] = theta
        Q_e = su2_exp(w)
        configs.append((f'uniform-θ={theta:.3f}', [Q_e.copy() for _ in range(ne)]))

    # Checkerboard I/iσ
    for ax in range(3):
        Q = []
        for mu in range(d):
            for site in lat.sites:
                if sum(site) % 2 == 0:
                    Q.append(np.eye(2, dtype=complex))
                else:
                    Q.append(isigma[ax].copy())
        configs.append((f'checker-I/iσ{ax}', Q))

    print(f"{'config':30s} {'max||H_□||':>12s} {'mean||H_□||':>12s} {'Σ||H_□||':>12s} {'||H||':>10s}")
    print("-" * 80)

    for name, Q in configs:
        norms = per_plaquette_norms(lat, Q)
        H = compute_hessian(lat, Q)
        ev = np.linalg.eigvalsh(H)
        H_norm = max(abs(ev[0]), abs(ev[-1]))
        print(f"{name:30s} {max(norms):12.6f} {np.mean(norms):12.6f} "
              f"{sum(norms):12.4f} {H_norm:10.4f}")

    # ==================================================================
    # PHASE 4: GRADIENT ASCENT on max ||H_□||
    # ==================================================================
    print(f"\n{'='*60}")
    print("PHASE 4: GRADIENT ASCENT on max_{□} ||H_□||")
    print(f"{'='*60}")

    rng2 = np.random.default_rng(777)

    for start_idx in range(5):
        Q = random_config(lat, rng2)
        best_max_norm = 0

        for it in range(100):
            norms = per_plaquette_norms(lat, Q)
            worst_pidx = np.argmax(norms)
            current_max = norms[worst_pidx]

            if current_max > best_max_norm:
                best_max_norm = current_max
                best_Q = [q.copy() for q in Q]

            # Finite-difference gradient of ||H_{worst}||
            eps = 1e-4
            grad = np.zeros((ne, 3))
            plaq_edges = set(e for (e, s) in lat.plaquettes[worst_pidx])

            # Only perturb edges in/near the worst plaquette
            affected_edges = set()
            for pidx_adj in lat.edge_plaquettes.get(list(plaq_edges)[0], []):
                for (e, s) in lat.plaquettes[pidx_adj]:
                    affected_edges.add(e)

            for e in affected_edges:
                for a in range(3):
                    w = np.zeros(3); w[a] = eps
                    Q_plus = [q.copy() for q in Q]
                    Q_plus[e] = su2_exp(w) @ Q[e]
                    norms_plus = per_plaquette_norms(lat, Q_plus)
                    grad[e, a] = (max(norms_plus) - current_max) / eps

            gnorm = np.linalg.norm(grad)
            if gnorm < 1e-8:
                break

            lr = min(0.02, 0.5 / gnorm)
            for e in range(ne):
                Q[e] = su2_exp(lr * grad[e]) @ Q[e]
                Q[e] = project_su2(Q[e])

            if it % 25 == 0:
                print(f"    start {start_idx}, iter {it}: max||H_□||={current_max:.6f}, |grad|={gnorm:.2e}")

        print(f"  Start {start_idx}: best max||H_□|| = {best_max_norm:.6f}")

    # ==================================================================
    # PHASE 5: AGGREGATION ANALYSIS
    # ==================================================================
    print(f"\n{'='*60}")
    print("PHASE 5: AGGREGATION — can per-plaquette bounds give ||H|| ≤ 4d?")
    print(f"{'='*60}")

    # At flat: each plaquette has ||H_□|| = 4.
    # Number of plaquettes = d(d-1)/2 * L^d. For d=4, L=2: 6*16=96.
    # Each edge is in 2(d-1)=6 plaquettes.
    # Triangle inequality: ||H|| ≤ Σ ||H_□|| = 96 * 4 = 384 >> 4d = 16. Terrible!
    #
    # Better: for quadratic form v^T H v = Σ_□ v^T H_□ v.
    # Each H_□ has support on 4 edges (12 indices).
    # If v is spread over all edges, v^T H_□ v is small.
    # The key: Σ_□ H_□ = H, and for a single edge, the sum of its plaquette
    # contributions gives the self-term.
    print(f"nplaquettes = {lat.nplaq}")
    print(f"plaquettes per edge = 2(d-1) = {2*(d-1)}")
    print(f"Triangle bound: Σ||H_□|| ≤ {lat.nplaq} × 4 = {lat.nplaq * 4} >> 4d = {bound}")
    print(f"This is way too loose — the per-plaquette approach needs structure.")

    # Better approach: partition plaquettes into groups that share no edges,
    # then bound each group separately.
    # Plaquettes sharing no edges can be bounded independently.
    # Maximum independent set in the plaquette-edge incidence graph.

    # For now, count: how many plaquettes share an edge with a given plaquette?
    plaq_adjacency_count = []
    for pidx in range(lat.nplaq):
        edges_p = set(e for (e, s) in lat.plaquettes[pidx])
        neighbors = set()
        for e in edges_p:
            for pidx2 in lat.edge_plaquettes[e]:
                if pidx2 != pidx:
                    neighbors.add(pidx2)
        plaq_adjacency_count.append(len(neighbors))

    print(f"\nPlaquette adjacency (sharing an edge):")
    print(f"  min neighbors = {min(plaq_adjacency_count)}")
    print(f"  max neighbors = {max(plaq_adjacency_count)}")
    print(f"  mean = {np.mean(plaq_adjacency_count):.1f}")

    # Chromatic number bound: if we can color plaquettes with k colors
    # such that same-color plaquettes share no edges, then ||H|| ≤ k × 4.
    # We need k ≤ d. For d=4, k ≤ 4 gives ||H|| ≤ 16 = 4d. Exactly!
    # But can we achieve k=d? Let's try greedy coloring.
    colors = [-1] * lat.nplaq
    n_colors = 0
    for pidx in range(lat.nplaq):
        edges_p = set(e for (e, s) in lat.plaquettes[pidx])
        neighbor_colors = set()
        for e in edges_p:
            for pidx2 in lat.edge_plaquettes[e]:
                if pidx2 != pidx and colors[pidx2] >= 0:
                    neighbor_colors.add(colors[pidx2])
        c = 0
        while c in neighbor_colors:
            c += 1
        colors[pidx] = c
        n_colors = max(n_colors, c + 1)

    print(f"\nGreedy coloring: {n_colors} colors needed")
    print(f"  If ||H_□|| ≤ 4 for all □, then ||H|| ≤ {n_colors} × 4 = {n_colors * 4}")
    print(f"  Target: 4d = {bound}")
    print(f"  Achieves target? {n_colors * 4 <= bound}")

    # Check: within each color class, do plaquettes share edges?
    for c in range(n_colors):
        class_pidxs = [i for i in range(lat.nplaq) if colors[i] == c]
        all_edges_in_class = []
        for pidx in class_pidxs:
            edges_p = [e for (e, s) in lat.plaquettes[pidx]]
            all_edges_in_class.extend(edges_p)
        from collections import Counter
        edge_counts = Counter(all_edges_in_class)
        max_count = max(edge_counts.values()) if edge_counts else 0
        print(f"  Color {c}: {len(class_pidxs)} plaquettes, max edge overlap = {max_count}")

    # ==================================================================
    # SUMMARY
    # ==================================================================
    print(f"\n{'='*70}")
    print("APPROACH A SUMMARY")
    print(f"{'='*70}")

    print(f"Per-plaquette bound ||H_□|| ≤ 4:")
    print(f"  Violations in random survey: {violations_4}/500")
    print(f"  Max ||H_□|| found: {max_plaq_norm:.6f}")
    print(f"\nAggregation via graph coloring: {n_colors} colors")
    if violations_4 == 0 and n_colors <= d:
        print(f"  => ||H|| ≤ {n_colors} × 4 = {n_colors*4} ≤ 4d = {bound} ✓")
    elif violations_4 > 0:
        print(f"  => Per-plaquette bound ||H_□|| ≤ 4 FAILS — need different approach")
    else:
        print(f"  => Coloring needs {n_colors} > d={d} colors — bound too loose")


if __name__ == "__main__":
    main()
