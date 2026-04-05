"""
arithmetic_lattice.py — Build the arithmetic lattice for gauge theory simulation.

Core idea from Morishita's arithmetic topology:
  - Spec(Z) behaves like a 3-manifold
  - Primes p behave like knots K_p embedded in this 3-manifold
  - The Galois group Gal(Q_bar/Q) plays the role of pi_1

For an elliptic curve E/Q with Galois representation rho: Gal(Q_bar/Q) -> GL(2, Z_ell),
we build a lattice where:
  - Vertices = primes p up to a bound (the "knots" in the arithmetic 3-manifold)
  - Edges connect primes based on how the Galois representation interacts at each
  - Edge weights encode the arithmetic gauge field data

The lattice structure implements a DISCRETE version of the arithmetic 3-manifold.
We can then define gauge theory actions on it.
"""

import numpy as np
from collections import defaultdict


def build_prime_graph(curve_data, connectivity='full', distance_metric='galois'):
    """
    Build the arithmetic lattice graph from curve data.

    Args:
        curve_data: dict from curve_data.extract_curve_data()
        connectivity: 'full', 'knn', or 'threshold'
        distance_metric: how to compute edge weights
            'galois' — based on mod-ell Frobenius conjugacy
            'frobenius_angle' — based on Sato-Tate angle distance
            'mixed' — combination of multiple metrics

    Returns:
        dict with:
            'vertices': list of prime data
            'adjacency': numpy matrix of edge weights
            'edges': list of (i, j, weight) tuples
            'vertex_labels': list of prime values
    """
    all_primes = curve_data['all_primes']
    good_primes = [p for p in all_primes if p['reduction_type'] == 0]
    bad_primes = [p for p in all_primes if p['reduction_type'] != 0]

    # For the lattice, use good primes as vertices (bad primes are "boundary" / "defects")
    n = len(good_primes)
    adjacency = np.zeros((n, n))
    vertex_labels = [p['p'] for p in good_primes]

    if distance_metric == 'galois':
        adjacency = _galois_distance_matrix(good_primes, curve_data['mod_ell'])
    elif distance_metric == 'frobenius_angle':
        adjacency = _frobenius_angle_distance(good_primes)
    elif distance_metric == 'mixed':
        # Combine multiple distance metrics
        d_galois = _galois_distance_matrix(good_primes, curve_data['mod_ell'])
        d_angle = _frobenius_angle_distance(good_primes)
        d_arith = _arithmetic_distance(good_primes)
        # Weighted combination
        adjacency = 0.4 * d_galois + 0.3 * d_angle + 0.3 * d_arith
    else:
        raise ValueError(f"Unknown distance metric: {distance_metric}")

    # Apply connectivity filter
    if connectivity == 'knn':
        adjacency = _knn_filter(adjacency, k=min(8, n - 1))
    elif connectivity == 'threshold':
        threshold = np.median(adjacency[adjacency > 0]) if np.any(adjacency > 0) else 0.5
        adjacency[adjacency > threshold] = 0

    # Build edge list
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if adjacency[i, j] > 0:
                edges.append((i, j, adjacency[i, j]))

    return {
        'vertices': good_primes,
        'bad_primes': bad_primes,
        'adjacency': adjacency,
        'edges': edges,
        'vertex_labels': vertex_labels,
        'n_vertices': n,
        'n_edges': len(edges),
        'conductor': curve_data['conductor'],
        'rank': curve_data['rank'],
    }


def _galois_distance_matrix(primes_data, ell):
    """
    Distance based on mod-ell Galois representation.

    Two primes p, q are "close" if their Frobenius elements in GL(2, F_ell)
    are conjugate or nearly so. This is the core arithmetic gauge theory distance.

    We use: d(p,q) = 1 - |tr(Frob_p * Frob_q^{-1})|^2 / (det(Frob_p)*det(Frob_q))
    normalized to [0, 1].
    """
    n = len(primes_data)
    D = np.zeros((n, n))

    traces = np.array([p.get('frob_trace_mod_ell', 0) for p in primes_data], dtype=float)
    dets = np.array([p.get('frob_det_mod_ell', 1) for p in primes_data], dtype=float)
    # Replace zero determinants
    dets[dets == 0] = 1.0

    for i in range(n):
        for j in range(i + 1, n):
            # Product trace: tr(A)*tr(B) - this is related to tr(AB) in GL(2)
            # For GL(2, F_ell): tr(AB^{-1}) = tr(A)*tr(B^{-1}) - tr(A * adj(B))/det(B)
            # Simplified: use trace-based similarity
            ti, tj = traces[i], traces[j]
            di, dj = dets[i], dets[j]

            # Chebychev-style distance based on traces
            # Two Frobenius are conjugate iff they have same trace and determinant mod ell
            trace_match = 1.0 if (int(ti) % ell == int(tj) % ell) else 0.0
            det_match = 1.0 if (int(di) % ell == int(dj) % ell) else 0.0

            # Continuous version: how close are the normalized traces
            norm_ti = ti / max(abs(di)**0.5, 1e-10)
            norm_tj = tj / max(abs(dj)**0.5, 1e-10)
            trace_distance = abs(norm_ti - norm_tj) / (abs(norm_ti) + abs(norm_tj) + 1e-10)

            # Combined: exact conjugacy class match + continuous trace distance
            similarity = 0.5 * (trace_match + det_match) + 0.5 * (1.0 - trace_distance)
            D[i, j] = D[j, i] = similarity

    return D


def _frobenius_angle_distance(primes_data):
    """
    Distance based on Frobenius angles (Sato-Tate distribution).

    a_p / (2*sqrt(p)) = cos(theta_p) where theta_p is the Frobenius angle.
    Primes with similar angles reduce "similarly" — they're close in the
    arithmetic manifold.
    """
    n = len(primes_data)
    D = np.zeros((n, n))

    angles = np.array([p.get('frobenius_angle', 0.0) for p in primes_data])

    for i in range(n):
        for j in range(i + 1, n):
            # Angular distance, normalized to [0, 1]
            d = abs(angles[i] - angles[j]) / 2.0  # max possible diff is 2
            similarity = 1.0 - d
            D[i, j] = D[j, i] = similarity

    return D


def _arithmetic_distance(primes_data):
    """
    Arithmetic distance based on number-theoretic relations between primes.

    Uses: p-adic distance, quadratic residue relation, size ratio.
    """
    n = len(primes_data)
    D = np.zeros((n, n))

    primes_list = [p['p'] for p in primes_data]

    for i in range(n):
        for j in range(i + 1, n):
            pi, pj = primes_list[i], primes_list[j]

            # Quadratic residue reciprocity: is p_i a QR mod p_j and vice versa?
            # Legendre symbols
            leg_ij = _legendre(pi, pj)
            leg_ji = _legendre(pj, pi)

            # QR reciprocity gives a "linking number" flavor
            qr_similarity = 0.5 * (1 + 0.5 * (leg_ij + leg_ji))

            # Log-ratio of primes (nearby primes are arithmetically closer)
            log_ratio = abs(np.log(pi) - np.log(pj)) / np.log(max(pi, pj))
            size_similarity = 1.0 - log_ratio

            # p-adic inspired: gcd structure
            diff = abs(pi - pj)
            # 2-adic valuation of the difference
            v2 = 0
            d = diff
            while d > 0 and d % 2 == 0:
                v2 += 1
                d //= 2
            padic_similarity = v2 / (np.log2(max(pi, pj)) + 1)

            D[i, j] = D[j, i] = 0.4 * qr_similarity + 0.3 * size_similarity + 0.3 * padic_similarity

    return D


def _legendre(a, p):
    """Compute Legendre symbol (a/p) for odd prime p."""
    if p == 2:
        return 1
    a = a % p
    if a == 0:
        return 0
    result = pow(a, (p - 1) // 2, p)
    return 1 if result == 1 else -1


def _knn_filter(adjacency, k=6):
    """Keep only k nearest neighbors for each vertex."""
    n = adjacency.shape[0]
    filtered = np.zeros_like(adjacency)
    for i in range(n):
        # Get indices sorted by weight (descending, since higher = closer)
        neighbors = np.argsort(-adjacency[i])
        # Keep top k (excluding self)
        kept = 0
        for j in neighbors:
            if j == i:
                continue
            if kept >= k:
                break
            filtered[i, j] = adjacency[i, j]
            filtered[j, i] = adjacency[j, i]
            kept += 1
    return filtered


def compute_lattice_topology(graph):
    """
    Compute topological invariants of the arithmetic lattice.

    These should relate to the arithmetic topology of Spec(Z) w.r.t. the curve.
    Key quantities:
      - Betti numbers of the lattice
      - Spectral gap of the graph Laplacian
      - Cheeger constant
    """
    adj = graph['adjacency']
    n = graph['n_vertices']

    if n == 0:
        return {'betti_0': 0, 'spectral_gap': 0, 'cheeger_constant': 0}

    # Degree matrix
    degrees = np.sum(adj, axis=1)
    D = np.diag(degrees)

    # Graph Laplacian L = D - A
    L = D - adj

    # Eigenvalues
    eigenvalues = np.linalg.eigvalsh(L)
    eigenvalues = np.sort(np.abs(eigenvalues))

    # Betti_0 = number of connected components = multiplicity of 0 eigenvalue
    betti_0 = np.sum(eigenvalues < 1e-10)

    # Spectral gap = smallest nonzero eigenvalue (Fiedler value)
    nonzero = eigenvalues[eigenvalues > 1e-10]
    spectral_gap = float(nonzero[0]) if len(nonzero) > 0 else 0.0

    # Normalized Laplacian eigenvalues
    D_inv_sqrt = np.diag(1.0 / np.sqrt(np.maximum(degrees, 1e-10)))
    L_norm = D_inv_sqrt @ L @ D_inv_sqrt
    norm_eigenvalues = np.sort(np.linalg.eigvalsh(L_norm))

    # Cheeger constant estimate (from spectral gap via Cheeger inequality)
    lambda_1 = float(norm_eigenvalues[1]) if len(norm_eigenvalues) > 1 else 0.0
    cheeger_lower = lambda_1 / 2.0
    cheeger_upper = np.sqrt(2 * lambda_1)

    return {
        'betti_0': int(betti_0),
        'spectral_gap': spectral_gap,
        'fiedler_value': spectral_gap,
        'cheeger_lower': cheeger_lower,
        'cheeger_upper': float(cheeger_upper),
        'laplacian_eigenvalues': eigenvalues.tolist()[:20],  # first 20
        'normalized_eigenvalues': norm_eigenvalues.tolist()[:20],
        'total_edge_weight': float(np.sum(adj) / 2),
        'mean_degree': float(np.mean(degrees)),
    }
