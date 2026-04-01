"""
Task 1: L=4, d=4 Hessian verification with 20 configurations.
Uses DENSE Hessian (3072x3072 = 75MB, tractable).

Configurations tested:
- 5 Haar random
- 5 Gibbs at beta=0.1
- 5 near-identity (epsilon=0.1)
- 5 adversarial gradient ascent (Rayleigh quotient maximization)
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import scipy.linalg as la
import time
from utils import (
    build_plaquette_list, adjoint_rep, su2_exp, random_su2, h_norm,
    build_hessian_LEFT, lambda_max_and_vec_dense, gibbs_sample, tau, sigma,
    compute_partial_holonomies, wilson_action
)

np.random.seed(42)

L = 4
d = 4
N = 2
beta = 1.0

n_sites = L**d       # 256
n_links = d * n_sites  # 1024
n_gen = N**2 - 1     # 3
n_dof = n_links * n_gen  # 3072

print(f"L={L}, d={d}, N={N}, beta={beta}")
print(f"n_sites={n_sites}, n_links={n_links}, n_dof={n_dof}")
print(f"Matrix size: {n_dof}x{n_dof} = {n_dof**2 * 8 / 1e6:.1f} MB")

plaq_list = build_plaquette_list(L, d)
n_plaq = len(plaq_list)
print(f"n_plaq={n_plaq} (expected {d*(d-1)//2 * n_sites} = {d*(d-1)//2 * n_sites})")
print()

results = []

# ==============================================================
# SANITY CHECK: Q=I
# ==============================================================
print("=" * 60)
print("SANITY CHECK: Q = I (identity)")
print("=" * 60)

U_I = np.array([np.eye(2, dtype=complex) for _ in range(n_links)])
t0 = time.time()
H_I = build_hessian_LEFT(U_I, plaq_list, beta, N, n_dof, n_links, n_gen)
t1 = time.time()
print(f"  Hessian build time: {t1-t0:.2f}s")

evals_I = la.eigvalsh(H_I)
lmax_I = np.max(evals_I)
hn_I = h_norm(lmax_I, beta)
print(f"  lambda_max = {lmax_I:.8f}")
print(f"  Expected:   {4*beta:.8f}")
print(f"  Difference: {abs(lmax_I - 4*beta):.2e}")
print(f"  H_norm = {hn_I:.8f} (bound: 1/12 = {1/12:.8f})")

sanity_ok = abs(lmax_I - 4*beta) < 1e-4
print(f"  SANITY CHECK: {'PASSED' if sanity_ok else 'FAILED'}")

if not sanity_ok:
    print("  CRITICAL: SANITY CHECK FAILED — stopping.")
    sys.exit(1)
print()

# Record sanity check result
results.append({'type': 'identity', 'config': 'Q=I', 'lmax': lmax_I, 'hnorm': hn_I, 'violates': hn_I > 1/12 + 1e-6})

# ==============================================================
# 5 HAAR RANDOM CONFIGURATIONS
# ==============================================================
print("=" * 60)
print("5 HAAR RANDOM CONFIGURATIONS")
print("=" * 60)

for trial in range(5):
    U = np.array([random_su2() for _ in range(n_links)])
    lmax, _ = lambda_max_and_vec_dense(U, plaq_list, beta, N, n_dof, n_links, n_gen)
    hn = h_norm(lmax, beta)
    violates = hn > 1/12 + 1e-6
    results.append({'type': 'haar', 'config': f'haar_{trial}', 'lmax': lmax, 'hnorm': hn, 'violates': violates})
    status = "VIOLATION!" if violates else "ok"
    print(f"  Haar {trial}: lambda_max = {lmax:.6f}, H_norm = {hn:.6f} [{status}]")
    if violates:
        print(f"  *** H_norm = {hn:.6f} > 1/12 = {1/12:.6f} ***")
        print(f"  *** CONJECTURE 1 VIOLATED — STOPPING ***")
        sys.exit(2)
print()

# ==============================================================
# 5 GIBBS CONFIGURATIONS AT beta=0.1
# ==============================================================
print("=" * 60)
print("5 GIBBS CONFIGURATIONS AT beta=0.1")
print("=" * 60)

beta_gibbs = 0.1
for trial in range(5):
    # Start from random, run Metropolis
    U = np.array([random_su2() for _ in range(n_links)])
    U, acc_rate = gibbs_sample(U, plaq_list, beta_gibbs, N, n_links, n_steps=5000)
    lmax, _ = lambda_max_and_vec_dense(U, plaq_list, beta, N, n_dof, n_links, n_gen)
    hn = h_norm(lmax, beta)
    violates = hn > 1/12 + 1e-6
    results.append({'type': 'gibbs', 'config': f'gibbs_{trial}', 'lmax': lmax, 'hnorm': hn, 'violates': violates})
    status = "VIOLATION!" if violates else "ok"
    print(f"  Gibbs {trial}: lambda_max = {lmax:.6f}, H_norm = {hn:.6f}, acc_rate={acc_rate:.2f} [{status}]")
    if violates:
        print(f"  *** CONJECTURE 1 VIOLATED ***")
        sys.exit(2)
print()

# ==============================================================
# 5 NEAR-IDENTITY CONFIGURATIONS (epsilon=0.1)
# ==============================================================
print("=" * 60)
print("5 NEAR-IDENTITY CONFIGURATIONS (eps=0.1)")
print("=" * 60)

eps_near = 0.1
for trial in range(5):
    U = np.array([su2_exp(eps_near * sum(np.random.randn() * tau[a] for a in range(3)))
                  for _ in range(n_links)])
    lmax, _ = lambda_max_and_vec_dense(U, plaq_list, beta, N, n_dof, n_links, n_gen)
    hn = h_norm(lmax, beta)
    violates = hn > 1/12 + 1e-6
    results.append({'type': 'near_id', 'config': f'near_id_{trial}', 'lmax': lmax, 'hnorm': hn, 'violates': violates})
    status = "VIOLATION!" if violates else "ok"
    print(f"  Near-I {trial}: lambda_max = {lmax:.6f}, H_norm = {hn:.6f} [{status}]")
    if violates:
        print(f"  *** CONJECTURE 1 VIOLATED ***")
        sys.exit(2)
print()

# ==============================================================
# 5 ADVERSARIAL GRADIENT ASCENT ON lambda_max
# ==============================================================
print("=" * 60)
print("5 ADVERSARIAL GRADIENT ASCENT (500 steps)")
print("=" * 60)

def compute_gradient_rayleigh(U, v, plaq_list, beta, N, n_links, n_gen, eps=1e-4):
    """
    Compute gradient of Rayleigh quotient w.r.t. LEFT perturbations.
    Uses finite differences, but only recomputes the affected plaquettes per link.

    For link e, generator a:
    grad[e,a] = (RQ(Q_e + eps*tau_a Q_e) - RQ(Q_e - eps*tau_a Q_e)) / (2*eps)
    where RQ = v^T H v evaluated on affected plaquettes only.
    """
    n_dof = n_links * n_gen
    prefactor = beta / (2.0 * N)
    v_mat = v.reshape(n_links, n_gen)
    grad = np.zeros((n_links, n_gen))

    # Precompute plaquettes by link
    plaq_by_link = [[] for _ in range(n_links)]
    for pi, plaq in enumerate(plaq_list):
        for pos, (link_idx, sign) in enumerate(plaq):
            plaq_by_link[link_idx].append(plaq)

    def rayleigh_contribution_plaqs(U_local, plaqs):
        """Compute sum_{p in plaqs} v^T H_p v"""
        total = 0.0
        for plaq in plaqs:
            e_idx = [plaq[k][0] for k in range(4)]
            signs = [plaq[k][1] for k in range(4)]
            Us = [U_local[e_idx[k]] for k in range(4)]
            P1, P2, P3, P4 = compute_partial_holonomies(Us[0], Us[1], Us[2], Us[3], N)
            Rs = [adjoint_rep(P) for P in [P1, P2, P3, P4]]

            for ie in range(4):
                for je in range(4):
                    block = prefactor * signs[ie] * signs[je] * Rs[ie].T @ Rs[je]
                    total += float(v_mat[e_idx[ie]] @ (block @ v_mat[e_idx[je]]))
        return total

    for e in range(n_links):
        plaqs_e = plaq_by_link[e]
        if not plaqs_e:
            continue
        for a in range(n_gen):
            U_plus = U.copy()
            U_plus[e] = su2_exp(eps * tau[a]) @ U[e]
            U_minus = U.copy()
            U_minus[e] = su2_exp(-eps * tau[a]) @ U[e]

            rq_plus = rayleigh_contribution_plaqs(U_plus, plaqs_e)
            rq_minus = rayleigh_contribution_plaqs(U_minus, plaqs_e)
            grad[e, a] = (rq_plus - rq_minus) / (2.0 * eps)

    return grad.flatten()


def normalize_su2(U):
    """Project each 2x2 matrix back onto SU(2)."""
    result = np.zeros_like(U)
    for i in range(len(U)):
        g = U[i]
        # Polar decomposition: g = U_unitary * P_positive
        # For 2x2: normalize by det
        det = np.linalg.det(g)
        if abs(det) > 1e-10:
            result[i] = g / np.sqrt(det)
        else:
            result[i] = np.eye(2, dtype=complex)
    return result


# Run 5 gradient ascent trials from different starts
grad_starts = [
    ('random', None),
    ('aligned_tau3', 'exp(eps*tau3)'),
    ('alternating', 'alternating_UV'),
    ('random_axis', 'random_axis'),
    ('near_center', 'near_minus_I'),
]

for trial, (start_name, start_desc) in enumerate(grad_starts):
    print(f"\n  Adversarial {trial} ({start_name}):")

    # Initialize configuration
    if start_name == 'random':
        U = np.array([random_su2() for _ in range(n_links)])
    elif start_name == 'aligned_tau3':
        # All links = exp(0.5 * tau_3)
        eps_start = 0.5
        U = np.array([su2_exp(eps_start * tau[2]) for _ in range(n_links)])
    elif start_name == 'alternating':
        # Alternating: even links get U, odd get V
        U_mat = su2_exp(0.8 * tau[0])
        V_mat = su2_exp(0.8 * tau[1])
        U = np.array([U_mat if i % 2 == 0 else V_mat for i in range(n_links)])
    elif start_name == 'random_axis':
        # All links = rotation around fixed random axis
        axis = np.random.randn(3)
        axis /= np.linalg.norm(axis)
        angle = np.pi / 3
        M = angle * sum(axis[a] * tau[a] for a in range(3))
        U = np.array([su2_exp(M) for _ in range(n_links)])
    elif start_name == 'near_center':
        # Near -I: all links = exp(pi*tau_3 + small noise)
        M = np.pi * tau[2]
        U = np.array([su2_exp(M + 0.1 * sum(np.random.randn() * tau[a] for a in range(3)))
                      for _ in range(n_links)])

    # Gradient ascent
    n_steps = 500
    step_size = 0.01
    best_lmax = -np.inf
    best_hnorm = -np.inf

    lmax_prev = lambda_max_and_vec_dense(U, plaq_list, beta, N, n_dof, n_links, n_gen)[0]
    history = [lmax_prev]

    for step in range(n_steps):
        lmax, v = lambda_max_and_vec_dense(U, plaq_list, beta, N, n_dof, n_links, n_gen)
        v /= np.linalg.norm(v)

        grad = compute_gradient_rayleigh(U, v, plaq_list, beta, N, n_links, n_gen)
        grad_mat = grad.reshape(n_links, n_gen)
        grad_norm = np.linalg.norm(grad)

        if grad_norm < 1e-10:
            print(f"    Step {step}: gradient vanished")
            break

        # Update: Q_e -> exp(step_size * grad_e^a * tau_a / |grad|) @ Q_e
        # Adaptive step size: reduce if lmax decreases
        for e in range(n_links):
            g_e = grad_mat[e]  # shape (3,)
            M_e = sum(g_e[a] * tau[a] for a in range(3))
            U[e] = su2_exp(step_size * M_e / (np.linalg.norm(g_e) + 1e-12)) @ U[e]

        # Re-normalize to SU(2)
        U = normalize_su2(U)

        if lmax > best_lmax:
            best_lmax = lmax
            best_hnorm = h_norm(lmax, beta)

        if step % 100 == 0:
            print(f"    Step {step}: lmax={lmax:.6f}, H_norm={h_norm(lmax, beta):.6f}")
        history.append(lmax)

    final_lmax, _ = lambda_max_and_vec_dense(U, plaq_list, beta, N, n_dof, n_links, n_gen)
    final_hnorm = h_norm(final_lmax, beta)
    violates = final_hnorm > 1/12 + 1e-6

    results.append({'type': 'adversarial', 'config': f'adv_{start_name}',
                    'lmax': final_lmax, 'hnorm': final_hnorm, 'violates': violates})

    print(f"    Final: lmax={final_lmax:.6f}, H_norm={final_hnorm:.6f}")
    print(f"    Max H_norm over trajectory: {best_hnorm:.6f} (bound: {1/12:.6f})")
    print(f"    Status: {'VIOLATION!' if violates else 'ok'}")

    if violates:
        print(f"    *** CONJECTURE 1 VIOLATED AT L=4 ***")
        sys.exit(2)

    # Sanity check: did gradient ascent actually maximize?
    print(f"    Trajectory range: [{min(history):.4f}, {max(history):.4f}]")

print()

# ==============================================================
# SUMMARY TABLE
# ==============================================================
print("=" * 60)
print("SUMMARY: L=4 RESULTS")
print("=" * 60)
print(f"{'Config':<20} {'Type':<12} {'lambda_max':<14} {'H_norm':<10} {'≤1/12?'}")
print("-" * 65)

max_hnorm = 0.0
max_config = None
for r in results:
    ok_str = "YES" if not r['violates'] else "NO - VIOLATION"
    print(f"  {r['config']:<18} {r['type']:<12} {r['lmax']:>12.6f}   {r['hnorm']:>8.6f}   {ok_str}")
    if r['hnorm'] > max_hnorm:
        max_hnorm = r['hnorm']
        max_config = r['config']

print("-" * 65)
print(f"  Max H_norm: {max_hnorm:.6f} (at {max_config})")
print(f"  Bound:      {1/12:.6f}")
print(f"  All OK:     {all(not r['violates'] for r in results)}")
print()
print(f"  Sanity check (Q=I): lambda_max = {results[0]['lmax']:.6f}, expected {4*beta}")
print(f"  Convention PASSED" if abs(results[0]['lmax'] - 4*beta) < 1e-4 else "  Convention FAILED!")

# Save results for later processing
import json
out_file = os.path.join(os.path.dirname(__file__), 'task1_results.json')
with open(out_file, 'w') as f:
    json.dump({'L': L, 'd': d, 'beta': beta, 'results': results, 'max_hnorm': max_hnorm}, f, indent=2)
print(f"\n  Results saved to task1_results.json")
