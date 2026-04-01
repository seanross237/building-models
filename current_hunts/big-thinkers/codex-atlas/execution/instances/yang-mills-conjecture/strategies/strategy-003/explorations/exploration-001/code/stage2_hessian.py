"""
Stage 2: Verify the relationship between HessS and M(Q).

The claim: HessS(v,v;Q) = (β/2N) · v^T M(Q) v
We test this numerically and characterize any curvature correction.
"""

import numpy as np
from scipy.linalg import eigh, expm
import time

np.random.seed(42)

# ============================================================
# SU(2) and Adjoint (same as stage0)
# ============================================================

SIGMA = [
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
]

def random_su2():
    v = np.random.randn(4)
    v /= np.linalg.norm(v)
    a, b, c, d = v
    return np.array([[a + 1j*b, c + 1j*d], [-c + 1j*d, a - 1j*b]])

def su2_inv(Q):
    return Q.conj().T

def adjoint_rep(Q):
    Qinv = su2_inv(Q)
    Ad = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            Ad[i, j] = 0.5 * np.real(np.trace(SIGMA[i] @ Q @ SIGMA[j] @ Qinv))
    return Ad

# ============================================================
# Lattice Setup (same as stage0)
# ============================================================

L = 2
d = 4
num_sites = L**d
num_edges = d * num_sites
DIM = 3 * num_edges

def site_index(coords):
    idx = 0
    for i in range(d):
        idx = idx * L + (coords[i] % L)
    return idx

def index_to_coords(idx):
    coords = []
    for i in range(d):
        coords.append(idx % L)
        idx //= L
    return list(reversed(coords))

def edge_index(site_idx, mu):
    return site_idx * d + mu

def neighbor(site_idx, mu, direction=1):
    coords = index_to_coords(site_idx)
    coords[mu] = (coords[mu] + direction) % L
    return site_index(coords)

def get_plaquettes():
    plaquettes = []
    for x in range(num_sites):
        for mu in range(d):
            for nu in range(mu + 1, d):
                x_mu = neighbor(x, mu)
                x_nu = neighbor(x, nu)
                e1 = edge_index(x, mu)
                e2 = edge_index(x_mu, nu)
                e3 = edge_index(x_nu, mu)
                e4 = edge_index(x, nu)
                plaquettes.append([(e1, +1), (e2, +1), (e3, -1), (e4, -1)])
    return plaquettes

PLAQUETTES = get_plaquettes()

# ============================================================
# M(Q) and Wilson action
# ============================================================

def build_M(Q):
    dim = 3 * num_edges
    M = np.zeros((dim, dim))
    for plaq in PLAQUETTES:
        (e1, o1), (e2, o2), (e3, o3), (e4, o4) = plaq
        H1 = np.eye(2, dtype=complex)
        H2 = Q[e1]
        H3 = Q[e1] @ Q[e2]
        H4 = Q[e1] @ Q[e2] @ su2_inv(Q[e3])
        edges = [e1, e2, e3, e4]
        signs = [o1, o2, o3, o4]
        Hs = [H1, H2, H3, H4]
        blocks = [signs[k] * adjoint_rep(Hs[k]) for k in range(4)]
        for i in range(4):
            for j in range(4):
                M[3*edges[i]:3*edges[i]+3, 3*edges[j]:3*edges[j]+3] += blocks[i].T @ blocks[j]
    return M

def compute_holonomy(Q, plaq):
    U = np.eye(2, dtype=complex)
    for (e, orient) in plaq:
        if orient == +1:
            U = U @ Q[e]
        else:
            U = U @ su2_inv(Q[e])
    return U

def wilson_action(Q, beta=1.0, N=2):
    S = 0.0
    for plaq in PLAQUETTES:
        U = compute_holonomy(Q, plaq)
        S -= (beta / N) * np.real(np.trace(U))
    return S

# ============================================================
# Compute full Hessian by finite differences
# ============================================================

def make_perturbed_config(Q, perturbations, epsilon):
    """
    Apply perturbations: Q_e -> exp(epsilon * sum_a v_{e,a} * i*sigma_a/2) * Q_e
    perturbations is a dict: edge_idx -> R^3 direction
    """
    Q_new = list(Q)
    for e, v in perturbations.items():
        A = np.zeros((2, 2), dtype=complex)
        for a in range(3):
            A += 1j * v[a] * SIGMA[a] / 2.0
        Q_new[e] = expm(epsilon * A) @ Q[e]
    return Q_new

def hessian_element_fd(Q, e1, a1, e2, a2, eps=1e-5, beta=1.0, N=2):
    """
    Compute ∂²S / ∂v_{e1,a1} ∂v_{e2,a2} by finite differences.
    Uses mixed partial derivative formula.
    """
    d1 = np.zeros(3); d1[a1] = 1.0
    d2 = np.zeros(3); d2[a2] = 1.0

    if e1 == e2:
        # Same edge: perturbation is d1 + d2, etc.
        # f(+h, +h), f(+h, -h), f(-h, +h), f(-h, -h) with respect to two directions on same edge
        Qpp = make_perturbed_config(Q, {e1: d1 + d2}, eps)  # wrong, these are independent directions
        # Need separate: perturb along d1 by h1 and d2 by h2
        # f(h1, h2) = S(exp(h2*A2) exp(h1*A1) Q_e, ...)
        # Mixed: [f(+,+) - f(+,-) - f(-,+) + f(-,-)] / (4 eps^2)
        Qpp = list(Q)
        Qpm = list(Q)
        Qmp = list(Q)
        Qmm = list(Q)

        A1 = np.zeros((2, 2), dtype=complex)
        A2 = np.zeros((2, 2), dtype=complex)
        for a in range(3):
            A1 += 1j * d1[a] * SIGMA[a] / 2.0
            A2 += 1j * d2[a] * SIGMA[a] / 2.0

        Qpp[e1] = expm(eps * A2) @ expm(eps * A1) @ Q[e1]
        Qpm[e1] = expm(-eps * A2) @ expm(eps * A1) @ Q[e1]
        Qmp[e1] = expm(eps * A2) @ expm(-eps * A1) @ Q[e1]
        Qmm[e1] = expm(-eps * A2) @ expm(-eps * A1) @ Q[e1]
    else:
        # Different edges
        A1 = np.zeros((2, 2), dtype=complex)
        A2 = np.zeros((2, 2), dtype=complex)
        for a in range(3):
            A1 += 1j * d1[a] * SIGMA[a] / 2.0
            A2 += 1j * d2[a] * SIGMA[a] / 2.0

        Qpp = list(Q)
        Qpm = list(Q)
        Qmp = list(Q)
        Qmm = list(Q)

        Qpp[e1] = expm(eps * A1) @ Q[e1]; Qpp[e2] = expm(eps * A2) @ Q[e2]
        Qpm[e1] = expm(eps * A1) @ Q[e1]; Qpm[e2] = expm(-eps * A2) @ Q[e2]
        Qmp[e1] = expm(-eps * A1) @ Q[e1]; Qmp[e2] = expm(eps * A2) @ Q[e2]
        Qmm[e1] = expm(-eps * A1) @ Q[e1]; Qmm[e2] = expm(-eps * A2) @ Q[e2]

    Spp = wilson_action(Qpp, beta, N)
    Spm = wilson_action(Qpm, beta, N)
    Smp = wilson_action(Qmp, beta, N)
    Smm = wilson_action(Qmm, beta, N)

    return (Spp - Spm - Smp + Smm) / (4 * eps**2)

# ============================================================
# Test: Compute Hessian for a subset and compare with M(Q)
# ============================================================

print("=" * 70)
print("STAGE 2: Hessian vs (β/2N) M(Q) comparison")
print("=" * 70)

beta = 1.0
N_gauge = 2

# Test with random configuration
Q_test = [random_su2() for _ in range(num_edges)]
M_test = build_M(Q_test)
M_scaled = (beta / (2 * N_gauge)) * M_test

print("\nComputing select Hessian elements by finite differences...")
print("(Comparing H_{(e,a),(e',b)} with (β/2N) M_{3e+a, 3e'+b})")

# Test a selection of elements: some diagonal, some off-diagonal
test_pairs = []
# Diagonal elements (same edge, same color)
for e in [0, 10, 30, 50, 63]:
    for a in range(3):
        test_pairs.append((e, a, e, a))

# Same edge, different color
for e in [5, 25, 45]:
    test_pairs.append((e, 0, e, 1))
    test_pairs.append((e, 1, e, 2))

# Adjacent edges (share a plaquette)
for e1 in [0, 8, 16]:
    for e2 in [1, 5, 9]:
        if e1 != e2:
            test_pairs.append((e1, 0, e2, 0))

# Non-adjacent edges
test_pairs.append((0, 0, 32, 0))
test_pairs.append((1, 1, 60, 2))

print(f"\nTesting {len(test_pairs)} matrix elements...")
print(f"{'(e1,a1,e2,a2)':<25} {'Hess(FD)':>14} {'(β/2N)M':>14} {'Diff':>14} {'RelErr':>10}")
print("-" * 80)

max_err = 0
max_abs_diff = 0
for (e1, a1, e2, a2) in test_pairs:
    h_fd = hessian_element_fd(Q_test, e1, a1, e2, a2, eps=1e-5)
    m_val = M_scaled[3*e1+a1, 3*e2+a2]
    diff = h_fd - m_val
    denom = max(abs(h_fd), abs(m_val), 1e-15)
    rel_err = abs(diff) / denom
    max_err = max(max_err, rel_err)
    max_abs_diff = max(max_abs_diff, abs(diff))
    print(f"({e1:2d},{a1},{e2:2d},{a2})          {h_fd:>14.8f} {m_val:>14.8f} {diff:>14.8f} {rel_err:>10.2e}")

print(f"\nMax relative error: {max_err:.2e}")
print(f"Max absolute diff:  {max_abs_diff:.2e}")

# ============================================================
# Full comparison: compute full Hessian for a smaller test
# ============================================================

print("\n" + "=" * 70)
print("Full Hessian computation (sampling rows)")
print("=" * 70)

# Compute a few full rows of the Hessian to get eigenvalue comparison
# Too expensive for full 192x192, but we can compare for specific tangent vectors

# Test 1: Full quadratic form v^T H v via 1D finite difference
print("\nQuadratic form comparison: v^T H v vs (β/2N) v^T M v")
print(f"{'Direction':<20} {'v^T H v (FD)':>14} {'(β/2N)v^T Mv':>14} {'Ratio':>10}")
print("-" * 60)

for trial in range(10):
    # Random tangent vector
    v = np.random.randn(DIM)
    v /= np.linalg.norm(v)

    # (β/2N) v^T M v
    vMv = v @ M_scaled @ v

    # v^T H v by finite difference: d²S/dε² where Q_e(ε) = exp(ε V_e) Q_e for all edges
    eps = 1e-5
    Q_plus = list(Q_test)
    Q_minus = list(Q_test)
    for e in range(num_edges):
        ve = v[3*e:3*e+3]
        A = np.zeros((2, 2), dtype=complex)
        for a in range(3):
            A += 1j * ve[a] * SIGMA[a] / 2.0
        Q_plus[e] = expm(eps * A) @ Q_test[e]
        Q_minus[e] = expm(-eps * A) @ Q_test[e]

    S0 = wilson_action(Q_test, beta, N_gauge)
    Sp = wilson_action(Q_plus, beta, N_gauge)
    Sm = wilson_action(Q_minus, beta, N_gauge)
    d2S = (Sp - 2*S0 + Sm) / eps**2

    vHv = d2S  # v^T (Hess S) v = d²S/dε²

    ratio = vHv / vMv if abs(vMv) > 1e-15 else float('nan')
    label = f"random-{trial+1}"
    print(f"{label:<20} {vHv:>14.8f} {vMv:>14.8f} {ratio:>10.6f}")

# Test 2: Staggered mode (should be extremal for M)
print("\nStaggered mode test:")
# Staggered mode: v_{x,mu,a} = (-1)^{sum(x)} * delta_{a,0}
v_stag = np.zeros(DIM)
for x in range(num_sites):
    coords = index_to_coords(x)
    sign = (-1)**sum(coords)
    for mu in range(d):
        e = edge_index(x, mu)
        v_stag[3*e] = sign  # color direction 0

v_stag /= np.linalg.norm(v_stag)
vMv_stag = v_stag @ M_scaled @ v_stag

eps = 1e-5
Q_plus = list(Q_test)
Q_minus = list(Q_test)
for e in range(num_edges):
    ve = v_stag[3*e:3*e+3]
    if np.linalg.norm(ve) < 1e-15:
        continue
    A = np.zeros((2, 2), dtype=complex)
    for a in range(3):
        A += 1j * ve[a] * SIGMA[a] / 2.0
    Q_plus[e] = expm(eps * A) @ Q_test[e]
    Q_minus[e] = expm(-eps * A) @ Q_test[e]

S0 = wilson_action(Q_test, beta, N_gauge)
Sp = wilson_action(Q_plus, beta, N_gauge)
Sm = wilson_action(Q_minus, beta, N_gauge)
d2S_stag = (Sp - 2*S0 + Sm) / eps**2

ratio_stag = d2S_stag / vMv_stag if abs(vMv_stag) > 1e-15 else float('nan')
print(f"{'staggered':<20} {d2S_stag:>14.8f} {vMv_stag:>14.8f} {ratio_stag:>10.6f}")

# ============================================================
# Characterize the correction
# ============================================================

print("\n" + "=" * 70)
print("Curvature correction analysis")
print("=" * 70)

# The diagonal correction is: HessS_{ee} = (β/4N) Σ_{□∋e} Re Tr(U_□) I_3
# while (β/2N) M_{ee} = (β/2N) × 6 × I_3

# Compute the per-edge curvature correction
for e in [0, 10, 30, 50]:
    # Sum of Re Tr(U_□) for plaquettes containing this edge
    re_tr_sum = 0
    for p_idx, plaq in enumerate(PLAQUETTES):
        edges_in_plaq = [ep[0] for ep in plaq]
        if e in edges_in_plaq:
            U = compute_holonomy(Q_test, plaq)
            re_tr_sum += np.real(np.trace(U))

    diag_hess = (beta / (4 * N_gauge)) * re_tr_sum
    diag_M = (beta / (2 * N_gauge)) * 6  # 6 plaquettes per edge, each contributes 1 to M diagonal
    print(f"Edge {e:2d}: Σ Re Tr(U_□) = {re_tr_sum:8.4f}, HessS_diag = {diag_hess:8.4f}, (β/2N)M_diag = {diag_M:8.4f}, ratio = {diag_hess/diag_M:.6f}")

print("\nConclusion: The Hessian HessS and (β/2N)M differ by a curvature correction")
print("that depends on Re Tr(U_□) for plaquettes around each edge.")
print("At Q=I (all U_□ = I, Re Tr = 2), they agree. Otherwise they differ.")

# ============================================================
# Derive the exact formula
# ============================================================

print("\n" + "=" * 70)
print("Exact Hessian formula derivation (numerical)")
print("=" * 70)
print("""
The full Hessian of S = -(β/N) Σ_□ Re Tr(U_□) is:

    HessS(v,v;Q) = (β/2N) [Σ_□ (|v|²_□ / 2) Re Tr(U_□) + cross terms]

The "cross terms" involve B-field-like objects but coupled to the holonomy.
The key decomposition is:

    HessS = -(β/2N) × Σ_□ [Re Tr(B̃_□ · B̃_□ · U_□)]

where B̃_□ is the matrix-valued B-field (in the fundamental representation).

This can be rewritten as:
    HessS = (β/2N) × [v^T C(Q) v]

where C(Q) involves BOTH |B|² terms AND Re Tr(U_□) diagonal terms.

The critical insight: M(Q) = Σ_□ B_□^T B_□ captures ONLY the |B|² part.
The Hessian also has curvature-dependent terms from the A² expansion.
""")

# Compute the actual Hessian matrix for a small set of edges to verify the formula
# Compare element-by-element

# Let me compute both the Hessian diagonal block for edge 0 and the M diagonal block
e_test = 0
H_block = np.zeros((3, 3))
M_block = M_scaled[0:3, 0:3]

for a1 in range(3):
    for a2 in range(3):
        H_block[a1, a2] = hessian_element_fd(Q_test, e_test, a1, e_test, a2, eps=1e-5)

print(f"\nEdge {e_test} diagonal block comparison:")
print(f"Hessian (FD):\n{H_block}")
print(f"\n(β/2N) M:\n{M_block}")
print(f"\nDifference (H - M_scaled):\n{H_block - M_block}")
print(f"\nDifference eigenvalues: {np.linalg.eigvalsh(H_block - M_block)}")

# The difference should be proportional to identity
diff_block = H_block - M_block
off_diag = np.max(np.abs(diff_block - np.diag(np.diag(diff_block))))
diag_spread = np.max(np.diag(diff_block)) - np.min(np.diag(diff_block))
print(f"\nOff-diagonal magnitude: {off_diag:.2e}")
print(f"Diagonal spread: {diag_spread:.2e}")
print(f"Mean diagonal: {np.mean(np.diag(diff_block)):.8f}")

# Predicted correction: (β/4N) Σ_{□∋e} Re Tr(U_□) - (β/2N) × 6
re_tr_sum = 0
for plaq in PLAQUETTES:
    edges_in_plaq = [ep[0] for ep in plaq]
    if e_test in edges_in_plaq:
        U = compute_holonomy(Q_test, plaq)
        re_tr_sum += np.real(np.trace(U))

predicted_correction = (beta / (4 * N_gauge)) * re_tr_sum - (beta / (2 * N_gauge)) * 6
print(f"\nPredicted correction per diagonal: {predicted_correction:.8f}")
print(f"Actual mean diagonal correction:   {np.mean(np.diag(diff_block)):.8f}")

print("\n" + "=" * 70)
print("STAGE 2 COMPLETE")
print("=" * 70)
