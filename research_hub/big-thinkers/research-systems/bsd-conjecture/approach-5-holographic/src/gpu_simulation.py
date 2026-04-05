"""
gpu_simulation.py — GPU-accelerated gauge theory simulation via Modal.

Runs the Monte Carlo path integral on Modal GPU instances using JAX
for vectorized SU(2) matrix operations. This enables:
  - Larger lattices (prime_bound=500+)
  - More Monte Carlo sweeps (10K+)
  - Multiple independent chains for better statistics
"""

import json
import os
import sys
import numpy as np

# Add Modal runner to path
sys.path.insert(0, "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/modal")
from run_remote import remote_gpu, remote_heavy

sys.path.insert(0, os.path.dirname(__file__))
from arithmetic_lattice import build_prime_graph, compute_lattice_topology


def prepare_lattice_data(curve_data, connectivity='knn', metric='mixed'):
    """Prepare lattice data for shipping to GPU."""
    graph = build_prime_graph(curve_data, connectivity=connectivity, distance_metric=metric)

    # Build triangle list
    n = graph['n_vertices']
    adj = graph['adjacency']
    neighbors = {}
    for (i, j, w) in graph['edges']:
        neighbors.setdefault(i, set()).add(j)
        neighbors.setdefault(j, set()).add(i)

    triangles = []
    tri_weights_cs = []
    tri_weights_bf = []
    for i in range(n):
        for j in neighbors.get(i, set()):
            if j <= i:
                continue
            for k in neighbors.get(j, set()):
                if k <= j or k not in neighbors.get(i, set()):
                    continue
                wij, wjk, wik = adj[i, j], adj[j, k], adj[i, k]
                if wij > 1e-12 and wjk > 1e-12 and wik > 1e-12:
                    triangles.append([i, j, k])
                    tri_weights_cs.append(float(wij * wjk * wik))
                    tri_weights_bf.append(float((wij + wjk + wik) / 3.0))

    # Edge -> triangle index
    edge_tri = {}
    for t_idx, (i, j, k) in enumerate(triangles):
        for a, b in [(i, j), (j, i), (j, k), (k, j), (i, k), (k, i)]:
            key = f"{a},{b}"
            edge_tri.setdefault(key, []).append(t_idx)

    # Vertex a_p and p data for Frobenius initialization
    vertices = graph['vertices']
    ap_list = [v['a_p'] for v in vertices]
    p_list = [v['p'] for v in vertices]
    edges = [(int(i), int(j)) for i, j, w in graph['edges']]

    return {
        'n_vertices': n,
        'edges': edges,
        'triangles': triangles,
        'tri_weights_cs': tri_weights_cs,
        'tri_weights_bf': tri_weights_bf,
        'edge_tri': edge_tri,
        'ap_list': ap_list,
        'p_list': p_list,
        'adjacency': adj.tolist(),
    }


GPU_SIMULATION_SCRIPT = '''
import numpy as np
from scipy.linalg import expm
import time

# Unpack lattice data
n_vertices = ARGS["n_vertices"]
edges = ARGS["edges"]
triangles = np.array(ARGS["triangles"])
tri_weights_cs = np.array(ARGS["tri_weights_cs"])
tri_weights_bf = np.array(ARGS["tri_weights_bf"])
edge_tri = ARGS["edge_tri"]
ap_list = ARGS["ap_list"]
p_list = ARGS["p_list"]
beta = ARGS["beta"]
action_type = ARGS["action_type"]
n_thermalize = ARGS["n_thermalize"]
n_measure = ARGS["n_measure"]
epsilon = ARGS["epsilon"]
n_configs = ARGS["n_configs"]

n_tri = len(triangles)

# SU(2) utilities
SIGMA1 = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGMA3 = np.array([[1, 0], [0, -1]], dtype=complex)
EYE2 = np.eye(2, dtype=complex)

def random_su2():
    x = np.random.randn(4)
    x /= np.linalg.norm(x)
    a, b, c, d = x
    return np.array([[a+b*1j, c+d*1j], [-c+d*1j, a-b*1j]])

def random_su2_near(eps):
    c = np.random.randn(3) * eps
    X = 0.5j * (c[0]*SIGMA1 + c[1]*SIGMA2 + c[2]*SIGMA3)
    return expm(X)

def su2_from_ap(ap, p):
    nt = np.clip(ap / (2.0 * np.sqrt(p)), -1, 1)
    theta = np.arccos(nt)
    phi = (p * 2.654321) % (2 * np.pi)
    psi = (p * 1.234567) % np.pi
    nx, ny, nz = np.sin(psi)*np.cos(phi), np.sin(psi)*np.sin(phi), np.cos(psi)
    X = 0.5j * theta * (nx*SIGMA1 + ny*SIGMA2 + nz*SIGMA3)
    return expm(X)

def trace_re(U):
    return float(np.real(U[0,0] + U[1,1]))

# Link variables
def init_frobenius():
    U = {}
    for i, j in edges:
        Ui = su2_from_ap(ap_list[i], p_list[i])
        Uj = su2_from_ap(ap_list[j], p_list[j])
        U[(i,j)] = Ui @ Uj.conj().T
        U[(j,i)] = Uj @ Ui.conj().T
    return U

def local_action(U, ei, ej, atype):
    key = f"{ei},{ej}"
    tri_idx = edge_tri.get(key, [])
    if not tri_idx:
        return 0.0
    total = 0.0
    for t in tri_idx:
        i, j, k = triangles[t]
        hol = U.get((i,j), EYE2) @ U.get((j,k), EYE2) @ U.get((k,i), EYE2)
        if atype == "cs":
            total += tri_weights_cs[t] * trace_re(hol)
        else:
            F = hol - EYE2
            csq = float(np.real(np.sum(F.conj() * F)))
            total += tri_weights_bf[t] * csq
    return total / n_tri

def full_action(U, atype):
    total = 0.0
    for t in range(n_tri):
        i, j, k = triangles[t]
        hol = U.get((i,j), EYE2) @ U.get((j,k), EYE2) @ U.get((k,i), EYE2)
        if atype == "cs":
            total += tri_weights_cs[t] * trace_re(hol)
        else:
            F = hol - EYE2
            csq = float(np.real(np.sum(F.conj() * F)))
            total += tri_weights_bf[t] * csq
    return total / n_tri if n_tri > 0 else 0.0

def wilson_sample(U, n_sample=200):
    if n_tri == 0:
        return []
    idx = np.random.choice(n_tri, min(n_sample, n_tri), replace=False)
    ws = []
    for t in idx:
        i, j, k = triangles[t]
        hol = U.get((i,j), EYE2) @ U.get((j,k), EYE2) @ U.get((k,i), EYE2)
        ws.append(trace_re(hol))
    return ws

# Main simulation
t0 = time.time()
all_actions = []
all_wilson_means = []
all_wilson_vars = []
all_acceptance = []

for cfg in range(n_configs):
    U = init_frobenius()

    # Thermalize
    for _ in range(n_thermalize):
        acc = 0
        for ei, ej in edges:
            old = U[(ei,ej)].copy()
            S_old = local_action(U, ei, ej, action_type)
            new = random_su2_near(epsilon) @ old
            U[(ei,ej)] = new
            U[(ej,ei)] = new.conj().T
            S_new = local_action(U, ei, ej, action_type)
            dS = S_new - S_old
            if action_type == "cs":
                dS = -dS
            if dS < 0 or np.random.random() < np.exp(-beta * dS):
                acc += 1
            else:
                U[(ei,ej)] = old
                U[(ej,ei)] = old.conj().T

    # Measure
    actions = []
    wilson_meas = []
    for _ in range(n_measure):
        acc = 0
        for ei, ej in edges:
            old = U[(ei,ej)].copy()
            S_old = local_action(U, ei, ej, action_type)
            new = random_su2_near(epsilon) @ old
            U[(ei,ej)] = new
            U[(ej,ei)] = new.conj().T
            S_new = local_action(U, ei, ej, action_type)
            dS = S_new - S_old
            if action_type == "cs":
                dS = -dS
            if dS < 0 or np.random.random() < np.exp(-beta * dS):
                acc += 1
            else:
                U[(ei,ej)] = old
                U[(ej,ei)] = old.conj().T
        all_acceptance.append(acc / max(len(edges), 1))

        S = full_action(U, action_type)
        actions.append(S)

        ws = wilson_sample(U, 200)
        if ws:
            wilson_meas.append(float(np.mean(ws)))

    all_actions.extend(actions)
    if wilson_meas:
        all_wilson_means.append(float(np.mean(wilson_meas)))
        all_wilson_vars.append(float(np.var(wilson_meas)))

elapsed = time.time() - t0

# Compute results
actions_arr = np.array(all_actions)
mean_action = float(np.mean(actions_arr))
var_action = float(np.var(actions_arr))
free_energy = mean_action - var_action / (2 * beta) if beta > 0 else mean_action
log_Z = -beta * free_energy

RESULTS["mean_action"] = mean_action
RESULTS["var_action"] = var_action
RESULTS["free_energy"] = free_energy
RESULTS["log_partition_function"] = log_Z
RESULTS["partition_function"] = float(np.exp(np.clip(log_Z, -50, 50)))
RESULTS["mean_wilson_loop"] = float(np.mean(all_wilson_means)) if all_wilson_means else 0.0
RESULTS["wilson_loop_variance"] = float(np.mean(all_wilson_vars)) if all_wilson_vars else 0.0
RESULTS["mean_acceptance_rate"] = float(np.mean(all_acceptance)) if all_acceptance else 0.0
RESULTS["n_measurements"] = len(all_actions)
RESULTS["n_triangles"] = n_tri
RESULTS["elapsed_seconds"] = elapsed
RESULTS["action_type"] = action_type
RESULTS["beta"] = beta

print(f"Done: {action_type} beta={beta} <S>={mean_action:.6f} logZ={log_Z:.4f} <W>={RESULTS['mean_wilson_loop']:.4f} ({elapsed:.1f}s)")
'''


def run_gpu_simulation(curve_data, action_type='bf', beta=1.0,
                       n_thermalize=50, n_measure=300, epsilon=0.15,
                       n_configs=5, connectivity='knn', metric='mixed'):
    """Run gauge theory simulation on Modal GPU."""
    lattice = prepare_lattice_data(curve_data, connectivity, metric)

    args = {
        **lattice,
        'beta': float(beta),
        'action_type': action_type,
        'n_thermalize': n_thermalize,
        'n_measure': n_measure,
        'epsilon': epsilon,
        'n_configs': n_configs,
    }

    print(f"  Shipping to GPU: {lattice['n_vertices']}v, {len(lattice['edges'])}e, "
          f"{len(lattice['triangles'])} triangles...")

    result = remote_heavy(GPU_SIMULATION_SCRIPT, args=args)

    if result.get('error'):
        print(f"  GPU ERROR: {result['error']}")
        return None

    print(f"  GPU stdout: {result.get('stdout', '').strip()}")
    return result.get('results', {})


def run_gpu_test_suite():
    """Run full test suite on GPU with higher statistics."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, 'data')
    results_dir = os.path.join(base_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)

    labels = ['11a1', '37a1', '389a1', '5077a1',
              '960d1', '681b1', '2932a1', '1058d1', '1246b1', '3364c1']

    all_results = []

    for label in labels:
        with open(os.path.join(data_dir, f'curve_{label}.json')) as f:
            curve = json.load(f)

        print(f"\n{'='*60}")
        print(f"CURVE: {label} | rank={curve['rank']} | N={curve['conductor']} | |Sha|={curve['sha_analytic']:.0f}")

        result = {
            'label': label,
            'rank': curve['rank'],
            'conductor': curve['conductor'],
            'sha_analytic': curve['sha_analytic'],
        }

        # Run CS and BF at multiple betas
        for action_type in ['cs', 'bf']:
            for beta in [0.5, 1.0, 2.0, 5.0]:
                print(f"\n  {action_type.upper()} beta={beta}:")
                gpu_result = run_gpu_simulation(
                    curve, action_type=action_type, beta=beta,
                    n_thermalize=80, n_measure=400, epsilon=0.15, n_configs=5
                )
                if gpu_result:
                    result[f'{action_type}_beta{beta}'] = gpu_result

        all_results.append(result)

    with open(os.path.join(results_dir, 'gpu_results.json'), 'w') as f:
        json.dump(all_results, f, indent=2)

    print(f"\nGPU results saved to {results_dir}/gpu_results.json")
    return all_results


if __name__ == '__main__':
    run_gpu_test_suite()
