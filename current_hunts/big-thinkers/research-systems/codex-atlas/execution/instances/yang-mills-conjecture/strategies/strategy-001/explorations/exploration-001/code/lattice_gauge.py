"""
Lattice Yang-Mills: Maximal Tree Gauge Decomposition
L=2, d=4 hypercubic torus, SU(2) gauge group

Stage 1: Implement M(Q), maximal tree gauge fixing, verify eigenvalue invariance.
Stage 2: Compute P^T R(Q) P in maximal tree gauge for random Q.
Stage 3: Identify dominant cotree degrees of freedom.
Stage 4: Attempt bound on P^T R(Q) P.

Verification: every claim tagged [COMPUTED] or [VERIFIED].
"""

import numpy as np
from scipy import linalg
import json

# ─── Constants ─────────────────────────────────────────────────────────────────
L = 2
d = 4
nV = L**d      # 16 vertices
nE = d * nV    # 64 edges
nP_count = (d*(d-1)//2) * nV  # 96 plaquettes

# ─── Pauli matrices ─────────────────────────────────────────────────────────────
sigma = [
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex)
]
# su(2) basis: T_k = i*sigma_k/2
T = [1j * s / 2 for s in sigma]


# ─── SU(2) utilities ────────────────────────────────────────────────────────────
def random_su2():
    """Sample a Haar-random SU(2) matrix."""
    a = np.random.randn(4)
    a /= np.linalg.norm(a)
    return (a[0] * np.eye(2, dtype=complex) +
            1j * (a[1] * sigma[0] + a[2] * sigma[1] + a[3] * sigma[2]))

def su2_inv(Q):
    """SU(2) inverse = conjugate transpose."""
    return Q.conj().T

def adj_matrix(Q):
    """
    Compute the 3x3 real adjoint representation matrix of Q in SU(2).
    Ad(Q)[j,k] defined by Q T_k Q^† = sum_j Ad(Q)[j,k] T_j
    Uses trace inner product: <A,B> = 2 Re Tr(A† B)
    """
    A = np.zeros((3, 3))
    for k in range(3):
        Xk = T[k]
        QXQ = Q @ Xk @ Q.conj().T
        for j in range(3):
            # <T_j, QXQ> = 2 Re Tr(T_j† QXQ) = 2 Re Tr(-i sigma_j/2 @ QXQ)
            A[j, k] = 2 * np.real(np.trace(T[j].conj().T @ QXQ))
    return A


# ─── Lattice geometry ────────────────────────────────────────────────────────────
def vidx(x):
    """Vertex index from d-tuple x in {0,1}^d."""
    return sum(int(x[i]) * (2**i) for i in range(d))

def vcoords(v):
    """Vertex coordinates as tuple."""
    return tuple((v >> i) & 1 for i in range(d))

def eidx(v, mu):
    """Edge index from source vertex v and direction mu."""
    return v * d + mu

def src_of(e):
    """Source vertex of edge e."""
    return e // d

def tgt_of(e):
    """Target vertex of edge e (with periodic boundary conditions)."""
    v = e // d
    mu = e % d
    x = list(vcoords(v))
    x[mu] = (x[mu] + 1) % L
    return vidx(x)

def edge_direction(e):
    return e % d

# Build plaquette list: each plaquette = (e1, e2, e3, e4)
# Convention: e1, e2 forward; e3, e4 backward
# Plaquette (v, mu, nu), mu < nu:
#   e1 = (v, mu)           forward: v -> v+e_mu
#   e2 = (v+e_mu, nu)      forward: v+e_mu -> v+e_mu+e_nu
#   e3 = (v+e_nu, mu)      backward traversal
#   e4 = (v, nu)           backward traversal
def build_plaquettes():
    plaquettes = []
    for v in range(nV):
        x = list(vcoords(v))
        for mu in range(d):
            for nu in range(mu+1, d):
                # e1
                e1 = eidx(v, mu)
                # e2: start at v + e_mu
                x2 = x[:]
                x2[mu] = (x2[mu] + 1) % L
                v2 = vidx(x2)
                e2 = eidx(v2, nu)
                # e3: start at v + e_nu
                x3 = x[:]
                x3[nu] = (x3[nu] + 1) % L
                v3 = vidx(x3)
                e3 = eidx(v3, mu)
                # e4
                e4 = eidx(v, nu)
                plaquettes.append((e1, e2, e3, e4))
    return plaquettes

plaquettes = build_plaquettes()
assert len(plaquettes) == nP_count, f"Expected {nP_count} plaquettes, got {len(plaquettes)}"


# ─── B-field and M(Q) operator ───────────────────────────────────────────────────
def compute_holonomies(Q_list, e1, e2, e3, e4):
    """
    Compute the partial holonomies for the B-field formula.
    Returns (Q1, Q2, Q3, Q4, P2, P3, U_plaq) where
    P2 = Q1, P3 = Q1 Q2 Q3^{-1}, U_plaq = Q1 Q2 Q3^{-1} Q4^{-1}
    """
    Q1 = Q_list[e1]
    Q2 = Q_list[e2]
    Q3 = Q_list[e3]
    Q4 = Q_list[e4]
    P2 = Q1
    P3 = Q1 @ su2_inv(Q3) @ su2_inv(Q2) if False else Q1 @ Q2 @ su2_inv(Q3)
    # Double-check: P3 = Q1 Q2 Q3^{-1} as stated in goal
    U_plaq = P3 @ su2_inv(Q4)
    return Q1, Q2, Q3, Q4, P2, P3, U_plaq

def make_M(Q_list):
    """
    Build the 192x192 operator M(Q).
    v^T M(Q) v = sum_□ |B_□(Q,v)|^2
    where B_□ = v_e1 + Ad(Q1) v_e2 - Ad(P3) v_e3 - Ad(U) v_e4

    Index convention: row/col = e*3 + a where e=edge, a=color 0,1,2.
    """
    M = np.zeros((nE * 3, nE * 3))
    for (e1, e2, e3, e4) in plaquettes:
        Q1, Q2, Q3, Q4, P2, P3, U_plaq = compute_holonomies(Q_list, e1, e2, e3, e4)
        # signs and Ad matrices for each edge
        signs   = [+1, +1, -1, -1]
        edges   = [e1, e2, e3, e4]
        Ad_list = [np.eye(3),
                   adj_matrix(P2),
                   adj_matrix(P3),
                   adj_matrix(U_plaq)]
        # Contribution: sum_{k,l} s_k s_l Ad_k^T Ad_l  (3x3 block at (edges[k], edges[l]))
        for ki in range(4):
            for kj in range(4):
                block = signs[ki] * signs[kj] * (Ad_list[ki].T @ Ad_list[kj])
                ei_ = edges[ki]
                ej_ = edges[kj]
                M[ei_*3:(ei_+1)*3, ej_*3:(ej_+1)*3] += block
    return M

def identity_config():
    """Return the identity configuration: Q_e = I for all e."""
    return [np.eye(2, dtype=complex)] * nE

def random_config():
    """Return a random SU(2) configuration."""
    return [random_su2() for _ in range(nE)]


# ─── Verify B-field formula against finite differences ──────────────────────────
def plaquette_holonomy(Q_list, e1, e2, e3, e4):
    """Compute the plaquette holonomy U_□ = Q1 Q2 Q3^{-1} Q4^{-1}."""
    Q1 = Q_list[e1]
    Q2 = Q_list[e2]
    Q3 = Q_list[e3]
    Q4 = Q_list[e4]
    return Q1 @ Q2 @ su2_inv(Q3) @ su2_inv(Q4)

def action(Q_list):
    """Compute the Wilson action S = sum_□ (1 - (1/2) Re Tr U_□)."""
    S = 0.0
    for (e1, e2, e3, e4) in plaquettes:
        U = plaquette_holonomy(Q_list, e1, e2, e3, e4)
        S += 1 - 0.5 * np.real(np.trace(U))
    return S

def perturbed_config(Q_list, edge, color, eps):
    """Perturb edge 'edge' in color direction 'color' by eps."""
    Q_new = list(Q_list)
    # Q_e -> Q_e * exp(eps * T[color])
    dQ = linalg.expm(eps * T[color])
    Q_new[edge] = Q_list[edge] @ dQ
    return Q_new

def numerical_hessian_entry(Q_list, e1, a1, e2, a2, eps=1e-5):
    """
    Compute d²S / (d v_{e1,a1} d v_{e2,a2}) by finite differences.
    """
    if e1 == e2 and a1 == a2:
        S_plus = action(perturbed_config(Q_list, e1, a1, eps))
        S_0    = action(Q_list)
        S_minus = action(perturbed_config(Q_list, e1, a1, -eps))
        return (S_plus - 2*S_0 + S_minus) / (eps**2)
    else:
        S_pp = action(perturbed_config(perturbed_config(Q_list, e1, a1, eps), e2, a2, eps))
        S_pm = action(perturbed_config(perturbed_config(Q_list, e1, a1, eps), e2, a2, -eps))
        S_mp = action(perturbed_config(perturbed_config(Q_list, e1, a1, -eps), e2, a2, eps))
        S_mm = action(perturbed_config(perturbed_config(Q_list, e1, a1, -eps), e2, a2, -eps))
        return (S_pp - S_pm - S_mp + S_mm) / (4 * eps**2)


# ─── Maximal spanning tree ────────────────────────────────────────────────────────
def build_bfs_spanning_tree():
    """
    BFS spanning tree rooted at vertex 0.
    Returns list of edge indices (|V|-1 = 15 edges).
    """
    tree_edges = []
    visited = [False] * nV
    visited[0] = True
    queue = [0]
    while queue:
        v = queue.pop(0)
        for mu in range(d):
            e = eidx(v, mu)
            w = tgt_of(e)
            if not visited[w]:
                visited[w] = True
                tree_edges.append(e)
                queue.append(w)
    assert len(tree_edges) == nV - 1, f"Expected {nV-1} tree edges, got {len(tree_edges)}"
    return tree_edges

def gauge_fix_tree(Q_list, tree_edges):
    """
    Fix gauge so Q_e = I for all tree edges.
    Uses propagation: h(tgt(e)) = Q_e^{-1} h(src(e)) if e goes src->tgt in tree.

    Returns (h, Q_new) where h[v] is the gauge transformation at v,
    and Q_new[e] = h(src)^{-1} Q_e h(tgt) is the gauge-fixed configuration.
    """
    tree_set = set(tree_edges)

    # Build tree adjacency
    tree_adj = {v: [] for v in range(nV)}
    for e in tree_edges:
        v = src_of(e)
        w = tgt_of(e)
        tree_adj[v].append((e, w, 'fwd'))
        tree_adj[w].append((e, v, 'bwd'))

    h = [None] * nV
    h[0] = np.eye(2, dtype=complex)
    visited = [False] * nV
    visited[0] = True
    queue = [0]

    while queue:
        v = queue.pop(0)
        for (e, w, direction) in tree_adj[v]:
            if not visited[w]:
                visited[w] = True
                if direction == 'fwd':
                    # e: v -> w; want h(v)^{-1} Q_e h(w) = I => h(w) = Q_e^{-1} h(v)
                    h[w] = su2_inv(Q_list[e]) @ h[v]
                else:
                    # e: w -> v (original); traversing from v to w (backward)
                    # want h(w)^{-1} Q_e h(v) = I => h(w) = Q_e h(v)
                    # But wait: src(e)=w, tgt(e)=v in original orientation.
                    # So Q_e^{new} = h(w)^{-1} Q_e h(v) = I => h(w) = Q_e h(v)
                    # But actually, this tree edge should be traversed in its natural direction.
                    # Let me use the natural direction only:
                    # Tree edge e has src=w (original), so we go w->v in the tree, which means
                    # we found w via v traversing backward. The constraint is:
                    # h(w)^{-1} Q_e h(v) = I => h(w) = Q_e h(v)
                    h[w] = Q_list[e] @ h[v]
                queue.append(w)

    assert all(h[v] is not None for v in range(nV)), "Some vertices unreachable in tree!"

    # Apply gauge transformation
    Q_new = []
    for e in range(nE):
        v = src_of(e)
        w = tgt_of(e)
        Q_new.append(su2_inv(h[v]) @ Q_list[e] @ h[w])

    return h, Q_new

def verify_gauge_fix(Q_new, tree_edges, tol=1e-10):
    """Check that all tree edges have Q_e = I after gauge fixing."""
    errors = []
    for e in tree_edges:
        diff = np.max(np.abs(Q_new[e] - np.eye(2, dtype=complex)))
        if diff > tol:
            errors.append((e, diff))
    return errors


# ─── Eigenvalue and projection utilities ─────────────────────────────────────────
def compute_eigenvalues(M):
    """Compute eigenvalues of M, sorted descending."""
    evals = np.linalg.eigvalsh(M)
    return evals[::-1]

def get_top_eigenspace(M, eigenvalue_target, tol=1e-8):
    """
    Get the eigenspace of M corresponding to eigenvalues near eigenvalue_target.
    Returns matrix P whose columns span the eigenspace.
    """
    evals, evecs = np.linalg.eigh(M)
    mask = np.abs(evals - eigenvalue_target) < tol
    return evecs[:, mask]

def project_matrix(M, P):
    """Compute P^T M P (restriction of M to eigenspace spanned by P's columns)."""
    return P.T @ M @ P


# ─── Per-cotree-link perturbation analysis ────────────────────────────────────────
def cotree_edges(tree_edges):
    """Return list of cotree edge indices."""
    tree_set = set(tree_edges)
    return [e for e in range(nE) if e not in tree_set]


# ─── Main computation ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    np.random.seed(42)
    results = {}

    print("=" * 60)
    print("STAGE 1: Setup and Verification")
    print("=" * 60)

    # 1a. Build M(I) and check top eigenvalue
    print("\n[1a] Building M(I)...")
    Q_I = identity_config()
    M_I = make_M(Q_I)
    print(f"  M(I) shape: {M_I.shape}")
    print(f"  M(I) symmetric: {np.allclose(M_I, M_I.T)}")

    evals_I = np.linalg.eigvalsh(M_I)
    evals_I_sorted = evals_I[::-1]
    print(f"  Top 15 eigenvalues of M(I):")
    for i, ev in enumerate(evals_I_sorted[:15]):
        print(f"    {i}: {ev:.6f}")

    lambda_max_I = evals_I_sorted[0]
    results['lambda_max_I'] = float(lambda_max_I)
    print(f"\n  lambda_max(M(I)) = {lambda_max_I:.6f}  [expected: 16.0]")

    # Count multiplicity of top eigenvalue
    top_mult = np.sum(np.abs(evals_I_sorted - lambda_max_I) < 1e-8)
    print(f"  Multiplicity of top eigenvalue: {top_mult}  [expected: 9]")
    results['top_eigenvalue_multiplicity'] = int(top_mult)

    # 1b. Verify M(I) eigenvalue against finite differences
    print("\n[1b] Spot-checking M(I) against finite differences...")
    Q0 = Q_I
    check_edges = [(0, 0), (0, 1), (1, 2), (5, 0)]
    for (e1, a1) in check_edges[:2]:
        for (e2, a2) in check_edges[:2]:
            fd = numerical_hessian_entry(Q0, e1, a1, e2, a2, eps=1e-5)
            exact = M_I[e1*3+a1, e2*3+a2]
            print(f"  M[({e1},{a1}),({e2},{a2})]: exact={exact:.6f}, FD={fd:.6f}, err={abs(exact-fd):.2e}")

    # 1c. Build the BFS spanning tree
    print("\n[1c] Building maximal spanning tree (BFS)...")
    tree_edges = build_bfs_spanning_tree()
    print(f"  Tree has {len(tree_edges)} edges: {tree_edges}")
    cotree = cotree_edges(tree_edges)
    print(f"  Cotree has {len(cotree)} edges")
    results['tree_edges'] = tree_edges
    results['cotree_edges'] = cotree

    # 1d. Gauge-fix a random config and verify eigenvalue invariance
    print("\n[1d] Gauge fixing verification...")
    Q_rand = random_config()
    M_rand_before = make_M(Q_rand)
    evals_before = np.linalg.eigvalsh(M_rand_before)[::-1]

    h, Q_rand_fixed = gauge_fix_tree(Q_rand, tree_edges)
    M_rand_after = make_M(Q_rand_fixed)
    evals_after = np.linalg.eigvalsh(M_rand_after)[::-1]

    errors = verify_gauge_fix(Q_rand_fixed, tree_edges)
    print(f"  Tree edges gauge-fixed to I: {'YES' if not errors else 'NO, errors: ' + str(errors)}")

    eval_diff = np.max(np.abs(evals_before - evals_after))
    print(f"  Eigenvalue max difference before/after gauge fix: {eval_diff:.2e}")
    print(f"  lambda_max before: {evals_before[0]:.6f}")
    print(f"  lambda_max after:  {evals_after[0]:.6f}")
    results['gauge_fix_eigenvalue_invariance'] = float(eval_diff)

    # 1e. Verify at Q=I: gauge-fixed config equals I on all edges
    print("\n[1e] Gauge-fix of Q=I: should give Q=I everywhere...")
    h_I, Q_I_fixed = gauge_fix_tree(Q_I, tree_edges)
    max_err_I = max(np.max(np.abs(Q_I_fixed[e] - np.eye(2, dtype=complex))) for e in range(nE))
    print(f"  Max deviation from I: {max_err_I:.2e}")
    results['identity_gauge_fix_error'] = float(max_err_I)

    print("\n" + "=" * 60)
    print("STAGE 2: P^T R(Q) P in maximal tree gauge")
    print("=" * 60)

    # Get the top eigenspace P of M(I)
    print("\n[2a] Computing top eigenspace P of M(I)...")
    evals_full, evecs_full = np.linalg.eigh(M_I)
    mask_top = np.abs(evals_full - lambda_max_I) < 1e-8
    P = evecs_full[:, mask_top]
    print(f"  P shape: {P.shape}  (should be 192 x 9)")
    print(f"  P^T P = I: {np.allclose(P.T @ P, np.eye(P.shape[1]))}")
    results['P_shape'] = list(P.shape)

    # Check P^T M(I) P = 16 * I
    check = P.T @ M_I @ P
    print(f"  P^T M(I) P = 16*I: {np.allclose(check, lambda_max_I * np.eye(P.shape[1]))}")

    # Compute P^T R(Q) P for 25 random configurations
    print("\n[2b] Computing P^T R(Q) P for 25 random configs (gauge-fixed)...")
    R_proj_values = []
    lambda_max_values = []

    for i in range(25):
        Q_r = random_config()
        _, Q_rf = gauge_fix_tree(Q_r, tree_edges)
        M_r = make_M(Q_rf)
        R_r = M_r - M_I

        # lambda_max of M(Q)
        lmax = np.linalg.eigvalsh(M_r)[-1]
        lambda_max_values.append(float(lmax))

        # P^T R(Q) P
        RR = P.T @ R_r @ P
        eigvals_RR = np.linalg.eigvalsh(RR)[::-1]
        R_proj_values.append({
            'lambda_max_M': float(lmax),
            'max_eval_R_proj': float(eigvals_RR[0]),
            'min_eval_R_proj': float(eigvals_RR[-1]),
            'trace_R_proj': float(np.trace(RR))
        })

        if i < 5:
            print(f"  Config {i+1}: lambda_max(M)={lmax:.4f}, "
                  f"max_eval(P^T R P)={eigvals_RR[0]:.4f}, "
                  f"min_eval(P^T R P)={eigvals_RR[-1]:.4f}, "
                  f"Tr(P^T R P)={np.trace(RR):.4f}")

    results['R_proj_values'] = R_proj_values

    max_proj_eval = max(v['max_eval_R_proj'] for v in R_proj_values)
    max_lambda_max = max(v['lambda_max_M'] for v in R_proj_values)
    print(f"\n  Over 25 configs:")
    print(f"  max lambda_max(M(Q))       = {max_lambda_max:.6f}  (bound = 16)")
    print(f"  max eigenval of P^T R(Q) P = {max_proj_eval:.6f}  (must be <= 0 for proof)")
    results['max_proj_eval_25'] = float(max_proj_eval)
    results['max_lambda_max_25'] = float(max_lambda_max)

    print("\n" + "=" * 60)
    print("STAGE 3: Cotree link analysis")
    print("=" * 60)

    # 3a. Per-cotree-link perturbation analysis
    print("\n[3a] Perturbing each cotree link individually from Q=I...")

    # For each cotree link, perturb it by a small random SU(2) element
    # and measure change in lambda_max
    cotree_impacts = []
    eps_perturb = 0.3  # moderately large perturbation

    Q_I2 = identity_config()
    lmax_I = np.linalg.eigvalsh(M_I)[-1]

    for ct_e in cotree:
        impacts = []
        for trial in range(5):
            Q_pert = list(Q_I2)
            Q_pert[ct_e] = random_su2()
            M_pert = make_M(Q_pert)
            lmax_pert = np.linalg.eigvalsh(M_pert)[-1]

            R_pert = M_pert - M_I
            RR = P.T @ R_pert @ P
            max_ev = np.linalg.eigvalsh(RR)[-1]
            impacts.append((float(lmax_pert - lmax_I), float(max_ev)))

        avg_delta_lmax = np.mean([x[0] for x in impacts])
        avg_max_ev = np.mean([x[1] for x in impacts])
        cotree_impacts.append({
            'edge': ct_e,
            'direction': int(edge_direction(ct_e)),
            'src': int(src_of(ct_e)),
            'avg_delta_lmax': float(avg_delta_lmax),
            'avg_max_ev_proj': float(avg_max_ev)
        })

    # Sort by impact
    cotree_impacts_sorted = sorted(cotree_impacts, key=lambda x: -abs(x['avg_delta_lmax']))

    print(f"  Top 10 cotree links by |delta lambda_max|:")
    for item in cotree_impacts_sorted[:10]:
        print(f"  Edge {item['edge']:3d} (dir={item['direction']}, src={item['src']:2d}): "
              f"avg_delta_lmax={item['avg_delta_lmax']:+.4f}, "
              f"avg_max_ev_proj={item['avg_max_ev_proj']:+.4f}")

    results['cotree_impacts'] = cotree_impacts

    # 3b. Analyze by direction
    print("\n[3b] Impact by direction...")
    for mu in range(d):
        mu_edges = [x for x in cotree_impacts if x['direction'] == mu]
        avg_impact = np.mean([abs(x['avg_delta_lmax']) for x in mu_edges])
        avg_proj = np.mean([x['avg_max_ev_proj'] for x in mu_edges])
        print(f"  Direction {mu}: {len(mu_edges)} cotree links, "
              f"avg |delta lmax|={avg_impact:.4f}, avg max_ev_proj={avg_proj:.4f}")

    print("\n" + "=" * 60)
    print("STAGE 4: Bound analysis")
    print("=" * 60)

    # 4a. Decompose P^T R(Q) P as sum over plaquettes
    print("\n[4a] Plaquette decomposition of P^T R(Q) P...")

    # For each plaquette, compute its contribution to M(Q)
    # M(Q) = sum_□ M_□(Q), so R(Q) = M(Q) - M(I) = sum_□ (M_□(Q) - M_□(I))
    # P^T R(Q) P = sum_□ P^T (M_□(Q) - M_□(I)) P

    def make_M_single_plaquette(Q_list, plaq_idx):
        """Build the contribution of a single plaquette to M(Q)."""
        (e1, e2, e3, e4) = plaquettes[plaq_idx]
        M_p = np.zeros((nE * 3, nE * 3))
        Q1, Q2, Q3, Q4, P2, P3, U_plaq = compute_holonomies(Q_list, e1, e2, e3, e4)
        signs   = [+1, +1, -1, -1]
        edges   = [e1, e2, e3, e4]
        Ad_list = [np.eye(3), adj_matrix(P2), adj_matrix(P3), adj_matrix(U_plaq)]
        for ki in range(4):
            for kj in range(4):
                block = signs[ki] * signs[kj] * (Ad_list[ki].T @ Ad_list[kj])
                ei_ = edges[ki]
                ej_ = edges[kj]
                M_p[ei_*3:(ei_+1)*3, ej_*3:(ej_+1)*3] += block
        return M_p

    # Verify decomposition: M = sum_□ M_□
    print("  Verifying M(I) = sum_□ M_□(I)...")
    M_I_check = np.zeros_like(M_I)
    for pidx in range(nP_count):
        M_I_check += make_M_single_plaquette(Q_I, pidx)
    print(f"  Max error: {np.max(np.abs(M_I_check - M_I)):.2e}")

    # For a sample random config, compute per-plaquette contributions to P^T R P
    print("\n[4b] Per-plaquette contributions to P^T R(Q) P (for 3 random configs)...")

    for sample_idx in range(3):
        Q_r = random_config()
        _, Q_rf = gauge_fix_tree(Q_r, tree_edges)
        M_r = make_M(Q_rf)
        R_r = M_r - M_I

        plaq_contribs = []
        for pidx in range(nP_count):
            M_plaq_Q = make_M_single_plaquette(Q_rf, pidx)
            M_plaq_I = make_M_single_plaquette(Q_I, pidx)
            R_plaq = M_plaq_Q - M_plaq_I
            RR_plaq = P.T @ R_plaq @ P
            ev_max = np.linalg.eigvalsh(RR_plaq)[-1]
            plaq_contribs.append(float(np.trace(RR_plaq)))  # trace contribution

        total_trace = sum(plaq_contribs)
        pos_count = sum(1 for x in plaq_contribs if x > 1e-10)
        neg_count = sum(1 for x in plaq_contribs if x < -1e-10)

        # lambda_max of total R projected
        RR_total = P.T @ R_r @ P
        lmax_RR = np.linalg.eigvalsh(RR_total)[-1]

        print(f"\n  Sample {sample_idx+1}:")
        print(f"    lambda_max(M(Q)) = {np.linalg.eigvalsh(M_r)[-1]:.4f}")
        print(f"    max_eval(P^T R P) = {lmax_RR:.4f}")
        print(f"    Tr(P^T R P) = {np.trace(RR_total):.4f}")
        print(f"    Per-plaquette contributions (trace): "
              f"pos={pos_count}, neg={neg_count}, total={total_trace:.4f}")
        print(f"    Max single-plaquette trace contrib: {max(plaq_contribs):.4f}")
        print(f"    Min single-plaquette trace contrib: {min(plaq_contribs):.4f}")

    # 4c. Gradient ascent on P^T R(Q) P (looking for violations)
    print("\n[4c] Gradient ascent on max eigenvalue of P^T R(Q) P...")
    print("  (Trying to find Q where P^T R(Q) P has a positive eigenvalue)")

    def compute_proj_max_eval(Q_list):
        """Compute max eigenvalue of P^T R(Q) P."""
        M_r = make_M(Q_list)
        R_r = M_r - M_I
        RR = P.T @ R_r @ P
        return np.linalg.eigvalsh(RR)[-1]

    # Start from random Q and perturb to maximize
    best_max_eval = -np.inf
    best_Q = None

    for trial in range(5):
        Q_curr = random_config()
        _, Q_curr = gauge_fix_tree(Q_curr, tree_edges)
        curr_eval = compute_proj_max_eval(Q_curr)

        # Simple random hill-climbing on cotree links
        for step in range(50):
            # Perturb a random cotree link
            ct_e = cotree[np.random.randint(len(cotree))]
            Q_try = list(Q_curr)
            # Small random SU(2) rotation
            v_rand = np.random.randn(3)
            v_rand /= np.linalg.norm(v_rand)
            angle = np.random.uniform(0, np.pi/4)
            dQ = linalg.expm(angle * sum(v_rand[i] * T[i] for i in range(3)))
            Q_try[ct_e] = Q_curr[ct_e] @ dQ
            new_eval = compute_proj_max_eval(Q_try)
            if new_eval > curr_eval:
                Q_curr = Q_try
                curr_eval = new_eval

        if curr_eval > best_max_eval:
            best_max_eval = curr_eval
            best_Q = Q_curr
        print(f"  Trial {trial+1}: best max_eval = {curr_eval:.6f}")

    print(f"\n  Best max_eval of P^T R(Q) P over gradient ascent: {best_max_eval:.6f}")
    print(f"  (Must be <= 0 for the conjecture; negative = holds)")
    results['gradient_ascent_best'] = float(best_max_eval)

    # 4d. Cotree-link-by-link bound analysis
    print("\n[4d] Maximum contribution of each cotree link to P^T R(Q) P...")
    print("  (Setting all links = I except one cotree link)")

    max_single_link_contrib = {}
    for ct_e in cotree:
        max_ev = -np.inf
        for trial in range(20):
            Q_try = list(Q_I)
            Q_try[ct_e] = random_su2()
            M_try = make_M(Q_try)
            R_try = M_try - M_I
            RR = P.T @ R_try @ P
            ev = np.linalg.eigvalsh(RR)[-1]
            if ev > max_ev:
                max_ev = ev
        max_single_link_contrib[ct_e] = float(max_ev)

    # Sort by max contribution
    sorted_single = sorted(max_single_link_contrib.items(), key=lambda x: -x[1])

    print(f"  Top 10 cotree links by max single-link P^T R P eigenvalue:")
    for e, v in sorted_single[:10]:
        print(f"  Edge {e:3d} (dir={edge_direction(e)}, src={src_of(e):2d}): max_ev = {v:+.6f}")

    print(f"\n  Bottom 10 cotree links (most negative):")
    for e, v in sorted_single[-10:]:
        print(f"  Edge {e:3d} (dir={edge_direction(e)}, src={src_of(e):2d}): max_ev = {v:+.6f}")

    positive_links = [(e,v) for e,v in sorted_single if v > 1e-6]
    print(f"\n  Links with positive single-link max contribution: {len(positive_links)}")

    results['max_single_link_contrib'] = {str(k): v for k,v in max_single_link_contrib.items()}

    # Save results
    with open('/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/yang-mills-conjecture/strategies/strategy-001/explorations/exploration-001/code/results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\n\nResults saved to code/results.json")
    print("\nDONE")
