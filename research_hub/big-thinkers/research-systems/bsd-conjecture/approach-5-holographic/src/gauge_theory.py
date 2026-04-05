"""
gauge_theory.py — Discrete arithmetic gauge theory on the prime lattice.

Implements THREE gauge theory formulations on the arithmetic lattice:

1. ARITHMETIC CHERN-SIMONS (Kim 2015-2016):
   Discrete version of CS action S_CS = sum_vertices tr(A dA + (2/3) A^3)
   where A is a gauge field (Lie-algebra valued 1-form on the lattice).

2. ARITHMETIC BF THEORY (Park & Park 2026):
   S_BF = sum_{faces} tr(B F) where F = dA + A^A is the curvature
   and B is a Lagrange multiplier field.
   KEY RESULT: The Cassels-Tate pairing on Sha IS this BF functional.
   So the partition function Z_BF should encode |Sha|.

3. WILSON LOOP OBSERVABLES:
   W_p = tr(holonomy around prime-knot p)
   These should detect the local-global obstruction and hence rank.

We use SU(2) gauge group (simplest non-abelian, captures key features)
and Monte Carlo sampling of the path integral.

PERFORMANCE: Triangles are precomputed and indexed by edge for O(1) local
action evaluation during Metropolis updates.
"""

import numpy as np
from scipy.linalg import expm
from collections import defaultdict


# ============================================================
# SU(2) utilities
# ============================================================

# Precompute Pauli matrices
_SIGMA1 = np.array([[0, 1], [1, 0]], dtype=complex)
_SIGMA2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
_SIGMA3 = np.array([[1, 0], [0, -1]], dtype=complex)
_EYE2 = np.eye(2, dtype=complex)


def random_su2():
    """Generate a random SU(2) matrix (Haar measure via quaternion)."""
    x = np.random.randn(4)
    x /= np.linalg.norm(x)
    a, b, c, d = x
    return np.array([
        [a + b*1j, c + d*1j],
        [-c + d*1j, a - b*1j]
    ])


def random_su2_near_identity(epsilon=0.1):
    """Generate SU(2) matrix near identity (for Metropolis updates)."""
    coeffs = np.random.randn(3) * epsilon
    X = 0.5j * (coeffs[0] * _SIGMA1 + coeffs[1] * _SIGMA2 + coeffs[2] * _SIGMA3)
    return expm(X)


def su2_trace(U):
    """Real part of trace of SU(2) matrix."""
    return float(np.real(U[0, 0] + U[1, 1]))


def su2_from_ap(ap, p, scale=1.0):
    """
    Construct an SU(2) element from Frobenius data (a_p, p).
    Maps the normalized Frobenius trace a_p / (2*sqrt(p)) to an SU(2) element.
    Sato-Tate: a_p/(2*sqrt(p)) = cos(theta), maps to rotation on S^3.
    """
    norm_trace = ap / (2.0 * np.sqrt(p))
    norm_trace = np.clip(norm_trace, -1.0, 1.0)
    theta = np.arccos(norm_trace) * scale

    # Axis determined by p (deterministic hash-like)
    phi = (p * 2.654321) % (2 * np.pi)
    psi = (p * 1.234567) % np.pi
    nx = np.sin(psi) * np.cos(phi)
    ny = np.sin(psi) * np.sin(phi)
    nz = np.cos(psi)

    X = 0.5j * theta * (nx * _SIGMA1 + ny * _SIGMA2 + nz * _SIGMA3)
    return expm(X)


# ============================================================
# Triangle-indexed lattice for fast local updates
# ============================================================

class TriangleLattice:
    """
    Precomputed triangle structure for fast action evaluation.

    Stores:
    - All triangles in the graph
    - For each edge, which triangles contain it
    - Edge weights for each triangle
    """

    def __init__(self, graph, max_triangles=5000):
        """
        Build triangle index from the arithmetic lattice graph.

        Args:
            graph: dict from arithmetic_lattice.build_prime_graph()
            max_triangles: limit on number of triangles (use KNN if exceeded)
        """
        self.n = graph['n_vertices']
        adj = graph['adjacency']

        # Build adjacency list for fast neighbor lookup
        self.neighbors = defaultdict(set)
        for (i, j, w) in graph['edges']:
            self.neighbors[i].add(j)
            self.neighbors[j].add(i)

        # Find all triangles
        self.triangles = []  # list of (i, j, k) with i < j < k
        self.triangle_weights_cs = []  # product of edge weights
        self.triangle_weights_bf = []  # average of edge weights

        for i in range(self.n):
            for j in self.neighbors[i]:
                if j <= i:
                    continue
                for k in self.neighbors[j]:
                    if k <= j or k not in self.neighbors[i]:
                        continue
                    wij = adj[i, j]
                    wjk = adj[j, k]
                    wik = adj[i, k]
                    if wij > 1e-12 and wjk > 1e-12 and wik > 1e-12:
                        self.triangles.append((i, j, k))
                        self.triangle_weights_cs.append(wij * wjk * wik)
                        self.triangle_weights_bf.append((wij + wjk + wik) / 3.0)

        self.n_triangles = len(self.triangles)

        # Build edge -> triangle index
        # For each directed edge (i,j), store indices of triangles containing it
        self.edge_triangles = defaultdict(list)
        for t_idx, (i, j, k) in enumerate(self.triangles):
            # Each triangle involves edges (i,j), (j,k), (i,k)
            for a, b in [(i, j), (j, i), (j, k), (k, j), (i, k), (k, i)]:
                self.edge_triangles[(a, b)].append(t_idx)


# ============================================================
# Gauge field configurations on the lattice
# ============================================================

class GaugeConfig:
    """
    A gauge field configuration on the arithmetic lattice.
    Assigns an SU(2) matrix U_{ij} to each edge (i,j).
    """

    def __init__(self, graph, tri_lattice, init='frobenius'):
        self.graph = graph
        self.tri = tri_lattice
        self.n = graph['n_vertices']
        self.edges = graph['edges']
        self.adjacency = graph['adjacency']
        self.U = {}

        if init == 'frobenius':
            self._init_from_frobenius()
        elif init == 'random':
            self._init_random()
        elif init == 'identity':
            self._init_identity()

    def _init_from_frobenius(self):
        vertices = self.graph['vertices']
        for (i, j, w) in self.edges:
            Ui = su2_from_ap(vertices[i]['a_p'], vertices[i]['p'])
            Uj = su2_from_ap(vertices[j]['a_p'], vertices[j]['p'])
            self.U[(i, j)] = Ui @ Uj.conj().T
            self.U[(j, i)] = Uj @ Ui.conj().T

    def _init_random(self):
        for (i, j, w) in self.edges:
            U = random_su2()
            self.U[(i, j)] = U
            self.U[(j, i)] = U.conj().T

    def _init_identity(self):
        for (i, j, w) in self.edges:
            self.U[(i, j)] = _EYE2.copy()
            self.U[(j, i)] = _EYE2.copy()

    def get_link(self, i, j):
        return self.U.get((i, j), _EYE2)

    def set_link(self, i, j, U):
        self.U[(i, j)] = U
        self.U[(j, i)] = U.conj().T


# ============================================================
# Action functionals (optimized with precomputed triangles)
# ============================================================

def _triangle_holonomy(config, i, j, k):
    """Compute holonomy U_ij @ U_jk @ U_ki around triangle (i,j,k)."""
    return config.get_link(i, j) @ config.get_link(j, k) @ config.get_link(k, i)


def chern_simons_action(config):
    """
    Discrete arithmetic Chern-Simons action.
    S_CS = (1/N_tri) * sum_{triangles (i,j,k)} w_ijk * tr(U_ij U_jk U_ki)
    """
    tri = config.tri
    if tri.n_triangles == 0:
        return 0.0

    total = 0.0
    for t_idx in range(tri.n_triangles):
        i, j, k = tri.triangles[t_idx]
        hol = _triangle_holonomy(config, i, j, k)
        total += tri.triangle_weights_cs[t_idx] * su2_trace(hol)

    return total / tri.n_triangles


def bf_theory_action(config):
    """
    Discrete arithmetic BF theory action (Park & Park).
    S_BF = (1/N_tri) * sum_{faces} w_ijk * tr(F^dag F)
    where F = holonomy - I is the discrete curvature.
    """
    tri = config.tri
    if tri.n_triangles == 0:
        return 0.0

    total = 0.0
    for t_idx in range(tri.n_triangles):
        i, j, k = tri.triangles[t_idx]
        hol = _triangle_holonomy(config, i, j, k)
        F = hol - _EYE2
        curv_sq = float(np.real(F[0, 0].conj() * F[0, 0] + F[0, 1].conj() * F[0, 1] +
                                F[1, 0].conj() * F[1, 0] + F[1, 1].conj() * F[1, 1]))
        total += tri.triangle_weights_bf[t_idx] * curv_sq

    return total / tri.n_triangles


def _local_action_cs(config, edge_i, edge_j):
    """Compute CS action contribution from triangles containing edge (i,j)."""
    tri = config.tri
    tri_indices = tri.edge_triangles.get((edge_i, edge_j), [])
    if not tri_indices:
        return 0.0

    total = 0.0
    for t_idx in tri_indices:
        i, j, k = tri.triangles[t_idx]
        hol = _triangle_holonomy(config, i, j, k)
        total += tri.triangle_weights_cs[t_idx] * su2_trace(hol)

    return total / tri.n_triangles


def _local_action_bf(config, edge_i, edge_j):
    """Compute BF action contribution from triangles containing edge (i,j)."""
    tri = config.tri
    tri_indices = tri.edge_triangles.get((edge_i, edge_j), [])
    if not tri_indices:
        return 0.0

    total = 0.0
    for t_idx in tri_indices:
        i, j, k = tri.triangles[t_idx]
        hol = _triangle_holonomy(config, i, j, k)
        F = hol - _EYE2
        curv_sq = float(np.real(F[0, 0].conj() * F[0, 0] + F[0, 1].conj() * F[0, 1] +
                                F[1, 0].conj() * F[1, 0] + F[1, 1].conj() * F[1, 1]))
        total += tri.triangle_weights_bf[t_idx] * curv_sq

    return total / tri.n_triangles


def wilson_loop(config, loop_vertices):
    """Compute Wilson loop around a sequence of vertices."""
    if len(loop_vertices) < 2:
        return 2.0
    holonomy = _EYE2.copy()
    for idx in range(len(loop_vertices)):
        i = loop_vertices[idx]
        j = loop_vertices[(idx + 1) % len(loop_vertices)]
        holonomy = holonomy @ config.get_link(i, j)
    return su2_trace(holonomy)


def wilson_loops_sample(config, n_sample=200):
    """Sample Wilson loops from random triangles (faster than all)."""
    tri = config.tri
    if tri.n_triangles == 0:
        return []
    n = min(n_sample, tri.n_triangles)
    indices = np.random.choice(tri.n_triangles, n, replace=False)
    loops = []
    for t_idx in indices:
        i, j, k = tri.triangles[t_idx]
        w = wilson_loop(config, [i, j, k])
        loops.append(w)
    return loops


# ============================================================
# Monte Carlo simulation with LOCAL updates (fast)
# ============================================================

def metropolis_sweep(config, action_type='cs', beta=1.0, epsilon=0.1):
    """
    One Metropolis sweep with LOCAL action evaluation.
    Only recomputes action for triangles touching the updated edge.
    """
    n_edges = len(config.edges)
    if n_edges == 0:
        return 0.0

    local_action_fn = _local_action_cs if action_type == 'cs' else _local_action_bf
    accepted = 0

    for edge_idx in range(n_edges):
        i, j, w = config.edges[edge_idx]
        old_U = config.U[(i, j)].copy()

        # Compute local action before
        S_local_old = local_action_fn(config, i, j)

        # Propose update
        delta = random_su2_near_identity(epsilon)
        new_U = delta @ old_U
        config.set_link(i, j, new_U)

        # Compute local action after
        S_local_new = local_action_fn(config, i, j)

        # Metropolis accept/reject
        dS = S_local_new - S_local_old
        if action_type == 'cs':
            # For CS, we MAXIMIZE tr(holonomy), so flip sign
            dS = -dS

        if dS < 0 or np.random.random() < np.exp(-beta * dS):
            accepted += 1
        else:
            config.set_link(i, j, old_U)

    return accepted / n_edges


def compute_partition_function(graph, action_type='cs', beta=1.0,
                                n_thermalize=50, n_measure=200,
                                epsilon=0.1, n_configs=5):
    """
    Compute the partition function via Monte Carlo sampling.

    Z = integral exp(-beta * S[A]) d[A]

    Returns dict with partition function estimates and observables.
    """
    action_fn = chern_simons_action if action_type == 'cs' else bf_theory_action

    # Build triangle lattice (once per graph)
    tri = TriangleLattice(graph)

    all_actions = []
    all_wilson_avgs = []
    all_wilson_vars = []
    all_acceptance_rates = []

    for config_idx in range(n_configs):
        config = GaugeConfig(graph, tri, init='frobenius')

        # Thermalize
        for t in range(n_thermalize):
            ar = metropolis_sweep(config, action_type, beta, epsilon)

        # Measure
        actions = []
        wilson_measurements = []

        for m in range(n_measure):
            ar = metropolis_sweep(config, action_type, beta, epsilon)
            all_acceptance_rates.append(ar)

            S = action_fn(config)
            actions.append(S)

            # Sample Wilson loops
            wloops = wilson_loops_sample(config, n_sample=100)
            if wloops:
                wilson_measurements.append(np.mean(wloops))

        all_actions.extend(actions)
        if wilson_measurements:
            all_wilson_avgs.append(np.mean(wilson_measurements))
            all_wilson_vars.append(np.var(wilson_measurements))

    actions_arr = np.array(all_actions)
    mean_action = float(np.mean(actions_arr))
    var_action = float(np.var(actions_arr))
    free_energy = mean_action - var_action / (2 * beta) if beta > 0 else mean_action
    log_Z = -beta * free_energy

    mean_wilson = float(np.mean(all_wilson_avgs)) if all_wilson_avgs else 0.0
    var_wilson = float(np.mean(all_wilson_vars)) if all_wilson_vars else 0.0

    return {
        'action_type': action_type,
        'beta': beta,
        'mean_action': mean_action,
        'var_action': var_action,
        'free_energy': free_energy,
        'log_partition_function': log_Z,
        'partition_function': float(np.exp(np.clip(log_Z, -50, 50))),
        'mean_wilson_loop': mean_wilson,
        'wilson_loop_variance': var_wilson,
        'mean_acceptance_rate': float(np.mean(all_acceptance_rates)) if all_acceptance_rates else 0.0,
        'n_measurements': len(all_actions),
        'n_configs': n_configs,
        'n_triangles': tri.n_triangles,
    }


def scan_beta(graph, action_type='cs', betas=None,
              n_thermalize=30, n_measure=100, epsilon=0.1):
    """Scan over coupling constants to find phase transitions."""
    if betas is None:
        betas = np.logspace(-1, 2, 20)
    results = []
    for beta in betas:
        result = compute_partition_function(
            graph, action_type=action_type, beta=beta,
            n_thermalize=n_thermalize, n_measure=n_measure,
            epsilon=epsilon, n_configs=2
        )
        results.append(result)
    return results


def estimate_rank_from_wilson(graph, n_thermalize=30, n_measure=150):
    """
    Estimate the analytic rank from Wilson loop behavior.

    Hypothesis: <W> and Var(W) in the Chern-Simons theory
    correlate with rank via the local-global obstruction.
    """
    tri = TriangleLattice(graph)
    config = GaugeConfig(graph, tri, init='frobenius')

    for t in range(n_thermalize):
        metropolis_sweep(config, 'cs', beta=1.0, epsilon=0.1)

    wilson_measurements = []
    action_measurements = []

    for m in range(n_measure):
        metropolis_sweep(config, 'cs', beta=1.0, epsilon=0.1)
        wloops = wilson_loops_sample(config, n_sample=100)
        if wloops:
            wilson_measurements.append(np.mean(wloops))
        action_measurements.append(chern_simons_action(config))

    if not wilson_measurements:
        return {'wilson_mean': 0, 'wilson_var': 0, 'action_mean': 0, 'action_var': 0, 'n_measurements': 0}

    w_arr = np.array(wilson_measurements)
    a_arr = np.array(action_measurements)

    return {
        'wilson_mean': float(np.mean(w_arr)),
        'wilson_var': float(np.var(w_arr)),
        'wilson_autocorrelation': float(np.corrcoef(w_arr[:-1], w_arr[1:])[0, 1]) if len(w_arr) > 2 else 0.0,
        'action_mean': float(np.mean(a_arr)),
        'action_var': float(np.var(a_arr)),
        'n_measurements': len(wilson_measurements),
    }
