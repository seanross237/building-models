"""
Task 2: Analytical proof attempt for max lambda[P^T R(Q) P] <= 0.

Key approach: The top eigenspace P of M(I) consists of "balanced staggered modes."
For each such mode v, v^T M(Q) v = sum_plaq |B_plaq(Q, v)|^2.

For each plaquette, B_plaq(Q, v) = S_plaq * n where S_plaq is a 3x3 matrix that
sums 4 SO(3) rotations with signs. By the triangle inequality:

  |S n| <= |R_1 n| + |R_2 n| + |R_3 n| + |R_4 n| = 4|n|

So |B_plaq|^2 <= 16|n|^2 per plaquette.

But we need a GLOBAL bound. This script:
1. Verifies the top eigenspace structure (balanced staggered modes)
2. Decomposes v^T M(Q) v per plaquette to understand the bound
3. Tests the key proof ingredients numerically
"""

import numpy as np
import sys

np.random.seed(42)


# ============================================================
# Same lattice infrastructure as numerical_verification.py
# ============================================================

class Lattice:
    def __init__(self, L, d):
        self.L, self.d = L, d
        self.n_sites = L**d
        self.n_edges = d * self.n_sites
        self.n_plaq = d*(d-1)//2 * self.n_sites
        self.dim_su = 3
        self.dim = self.dim_su * self.n_edges
        self._plaq_cache = None

    def site_index(self, coords):
        idx = 0
        for i in range(self.d):
            idx = idx * self.L + (coords[i] % self.L)
        return idx

    def site_coords(self, idx):
        coords = []
        r = idx
        for i in range(self.d - 1, -1, -1):
            coords.append(r % self.L)
            r //= self.L
        return list(reversed(coords))

    def edge_index(self, site_idx, mu):
        return site_idx * self.d + mu

    def shifted_site(self, site_idx, mu, sign=+1):
        coords = self.site_coords(site_idx)
        coords[mu] = (coords[mu] + sign) % self.L
        return self.site_index(coords)

    def plaquettes(self):
        if self._plaq_cache is not None:
            return self._plaq_cache
        plaq_list = []
        for x in range(self.n_sites):
            for mu in range(self.d):
                for nu in range(mu+1, self.d):
                    x_mu = self.shifted_site(x, mu)
                    x_nu = self.shifted_site(x, nu)
                    e1 = self.edge_index(x, mu)
                    e2 = self.edge_index(x_mu, nu)
                    e3 = self.edge_index(x_nu, mu)
                    e4 = self.edge_index(x, nu)
                    plaq_list.append((e1, e2, e3, e4, x, mu, nu))
        self._plaq_cache = plaq_list
        return plaq_list


def su2_basis():
    sigma1 = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma3 = np.array([[1, 0], [0, -1]], dtype=complex)
    return [1j * sigma1 / 2, 1j * sigma2 / 2, 1j * sigma3 / 2]


def adjoint_action(U, A):
    return U @ A @ np.conj(U).T


def su2_to_vec(A, basis):
    return np.array([-2 * np.trace(b @ A).real for b in basis])


def ad_matrix(U, basis):
    dim_su = len(basis)
    R = np.zeros((dim_su, dim_su))
    for j in range(dim_su):
        transformed = adjoint_action(U, basis[j])
        R[:, j] = su2_to_vec(transformed, basis)
    return R


def random_su2():
    x = np.random.randn(4)
    x /= np.linalg.norm(x)
    a, b, c, d = x
    return np.array([
        [a + 1j*b, c + 1j*d],
        [-c + 1j*d, a - 1j*b]
    ], dtype=complex)


def expm_su2(A):
    tr_A2 = np.trace(A @ A)
    theta_sq = -tr_A2 / 2.0
    if abs(theta_sq) < 1e-30:
        return np.eye(2, dtype=complex) + A + 0.5 * A @ A
    if theta_sq.real >= 0:
        theta = np.sqrt(theta_sq.real)
        return np.cos(theta) * np.eye(2, dtype=complex) + (np.sin(theta) / theta) * A
    else:
        theta = np.sqrt(-theta_sq.real)
        return np.cosh(theta) * np.eye(2, dtype=complex) + (np.sinh(theta) / theta) * A


def build_M_operator(lat, Q, basis):
    dim_su = lat.dim_su
    M = np.zeros((lat.dim, lat.dim))
    for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
        Q1 = Q[e1]
        Q12 = Q1 @ Q[e2]
        Q123inv = Q12 @ np.conj(Q[e3]).T
        U_plaq = Q123inv @ np.conj(Q[e4]).T
        R1 = np.eye(dim_su)
        R2 = ad_matrix(Q1, basis)
        R3 = -ad_matrix(Q123inv, basis)
        R4 = -ad_matrix(U_plaq, basis)
        edges_and_R = [(e1, R1), (e2, R2), (e3, R3), (e4, R4)]
        for (ei, Ri) in edges_and_R:
            for (ej, Rj) in edges_and_R:
                block = Ri.T @ Rj
                M[dim_su*ei:dim_su*ei+dim_su, dim_su*ej:dim_su*ej+dim_su] += block
    return M


def build_K_curl(lat):
    dim_su = lat.dim_su
    K = np.zeros((lat.dim, lat.dim))
    for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
        signs = {e1: +1, e2: +1, e3: -1, e4: -1}
        edges = [e1, e2, e3, e4]
        for ei in edges:
            for ej in edges:
                si, sj = signs[ei], signs[ej]
                K[dim_su*ei:dim_su*ei+dim_su, dim_su*ej:dim_su*ej+dim_su] += si * sj * np.eye(dim_su)
    return K


# ============================================================
# Top eigenspace analysis
# ============================================================

def analyze_top_eigenspace(lat, K_curl):
    """Determine the structure of the 9-dim top eigenspace of M(I) = K_curl."""
    eigs, vecs = np.linalg.eigh(K_curl)
    top_mask = np.abs(eigs - 16.0) < 1e-8
    P = vecs[:, top_mask]  # 192 x 9

    print("=== TOP EIGENSPACE STRUCTURE ===")
    print(f"Dimension: {P.shape[1]}")

    # Test: are these modes "balanced staggered"?
    # A balanced staggered mode has v_{x,mu,a} = (-1)^{|x| + f(mu)} * delta_{a,alpha}
    # where f partitions {0,...,d-1} into two equal groups.

    # For d=4, balanced partitions (k=2):
    # {0,1} vs {2,3}: f = [0,0,1,1]
    # {0,2} vs {1,3}: f = [0,1,0,1]
    # {0,3} vs {1,2}: f = [0,1,1,0]

    partitions = [
        [0, 0, 1, 1],  # {0,1} vs {2,3}
        [0, 1, 0, 1],  # {0,2} vs {1,3}
        [0, 1, 1, 0],  # {0,3} vs {1,2}
    ]

    staggered_modes = []
    for f in partitions:
        for alpha in range(3):  # color direction
            v = np.zeros(lat.dim)
            for x in range(lat.n_sites):
                coords = lat.site_coords(x)
                site_parity = sum(coords) % 2
                for mu in range(lat.d):
                    e = lat.edge_index(x, mu)
                    sign = (-1) ** (site_parity + f[mu])
                    v[3*e + alpha] = sign

            # Normalize
            v = v / np.linalg.norm(v)
            staggered_modes.append(v)

    staggered_modes = np.array(staggered_modes).T  # 192 x 9

    # Check: do these modes span the same subspace as P?
    # Compute overlap matrix
    overlap = staggered_modes.T @ P  # 9 x 9
    singular_values = np.linalg.svd(overlap, compute_uv=False)

    print(f"Overlap singular values (should all be 1.0 if same subspace):")
    print(f"  {np.sort(singular_values)[::-1]}")

    spans_same = np.allclose(singular_values, 1.0, atol=1e-10)
    print(f"  Same subspace: {spans_same}")

    # Verify Rayleigh quotients
    for i in range(9):
        v = staggered_modes[:, i]
        rq = v @ K_curl @ v
        print(f"  Mode {i}: Rayleigh quotient = {rq:.10f}")

    return P, staggered_modes, partitions


# ============================================================
# Per-plaquette decomposition
# ============================================================

def per_plaquette_decomposition(lat, Q, basis, staggered_modes, partitions):
    """
    For each staggered mode and each plaquette, compute:
    - |B_plaq(Q, v)|^2
    - |B_plaq(I, v)|^2
    - The difference (should be <= 0 when summed appropriately)

    Also verifies the key proof ingredient:
    B_plaq(Q, v) = sigma * S_plaq * n where S is sum of +-rotations,
    and |S n| <= 4|n| by triangle inequality.
    """
    results = []

    for mode_idx in range(9):
        v = staggered_modes[:, mode_idx]
        partition_idx = mode_idx // 3
        color_idx = mode_idx % 3
        f = partitions[partition_idx]

        total_Q = 0.0  # v^T M(Q) v
        total_I = 0.0  # v^T M(I) v
        contributing_Q = 0.0
        contributing_I = 0.0
        noncontributing_Q = 0.0
        noncontributing_I = 0.0

        max_per_plaq_ratio = 0.0

        for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
            # Determine if this plaquette is "contributing" for this mode
            is_contributing = (f[mu] != f[nu])

            # Get edge values
            v1 = v[3*e1:3*e1+3]
            v2 = v[3*e2:3*e2+3]
            v3 = v[3*e3:3*e3+3]
            v4 = v[3*e4:3*e4+3]

            # B_plaq(I, v) = v1 + v2 - v3 - v4
            B_I = v1 + v2 - v3 - v4
            sq_I = np.dot(B_I, B_I)

            # B_plaq(Q, v) = R1*v1 + R2*v2 + R3*v3 + R4*v4
            Q1 = Q[e1]
            Q12 = Q1 @ Q[e2]
            Q123inv = Q12 @ np.conj(Q[e3]).T
            U_plaq = Q123inv @ np.conj(Q[e4]).T

            R1 = np.eye(3)
            R2 = ad_matrix(Q1, basis)
            R3 = -ad_matrix(Q123inv, basis)
            R4 = -ad_matrix(U_plaq, basis)

            B_Q = R1 @ v1 + R2 @ v2 + R3 @ v3 + R4 @ v4
            sq_Q = np.dot(B_Q, B_Q)

            total_Q += sq_Q
            total_I += sq_I

            if is_contributing:
                contributing_Q += sq_Q
                contributing_I += sq_I
            else:
                noncontributing_Q += sq_Q
                noncontributing_I += sq_I

            # Triangle inequality check: |B_Q| <= sum of individual norms = 4*|n|
            # Each R_i v_i has norm |v_i| = |n| (since R_i is orthogonal)
            n_norm = np.linalg.norm(v1)  # all equal for staggered
            tri_bound = (4 * n_norm) ** 2  # = 16 |n|^2

            if sq_Q > tri_bound + 1e-12:
                print(f"  WARNING: Triangle inequality violated! |B|^2 = {sq_Q:.8f} > {tri_bound:.8f}")

        norm_v_sq = np.dot(v, v)

        results.append({
            'mode': mode_idx,
            'partition': partition_idx,
            'color': color_idx,
            'total_Q': total_Q,
            'total_I': total_I,
            'RQ_diag': total_Q - total_I,  # v^T R(Q) v
            'contributing_Q': contributing_Q,
            'contributing_I': contributing_I,
            'noncontributing_Q': noncontributing_Q,
            'noncontributing_I': noncontributing_I,
            'norm_v_sq': norm_v_sq,
        })

    return results


def test_S_matrix_bound(lat, Q, basis, staggered_modes, partitions):
    """
    For each plaquette and staggered mode, compute S = sum(sigma_i R_i)
    and check ||S||_op <= 4 (operator norm bound from triangle inequality).

    Also compute S^T S and check its eigenvalues.
    """
    n_plaq = len(lat.plaquettes())

    # For a fixed mode (say mode 0)
    v = staggered_modes[:, 0]
    f = partitions[0]  # [0,0,1,1]

    S_matrices_contrib = []
    S_matrices_noncontrib = []

    for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
        is_contributing = (f[mu] != f[nu])

        Q1 = Q[e1]
        Q12 = Q1 @ Q[e2]
        Q123inv = Q12 @ np.conj(Q[e3]).T
        U_plaq = Q123inv @ np.conj(Q[e4]).T

        R1 = np.eye(3)
        R2 = ad_matrix(Q1, basis)
        R3_raw = ad_matrix(Q123inv, basis)
        R4_raw = ad_matrix(U_plaq, basis)

        # Get the sign of each edge in the staggered mode
        coords_x = lat.site_coords(x)
        parity_x = sum(coords_x) % 2

        # v_{e1} = (-1)^{|x|+f(mu)} * n
        # v_{e2} = (-1)^{|x+mu|+f(nu)} * n = (-1)^{|x|+1+f(nu)} * n
        # v_{e3} = (-1)^{|x+nu|+f(mu)} * n = (-1)^{|x|+1+f(mu)} * n
        # v_{e4} = (-1)^{|x|+f(nu)} * n

        s1 = (-1)**(parity_x + f[mu])
        s2 = (-1)**(parity_x + 1 + f[nu])
        s3 = (-1)**(parity_x + 1 + f[mu])
        s4 = (-1)**(parity_x + f[nu])

        # B_plaq(Q, v) = R1*(s1*n) + R2*(s2*n) - R3_raw*(s3*n) - R4_raw*(s4*n)
        # = [s1*R1 + s2*R2 - s3*R3_raw - s4*R4_raw] * n
        # = S * n (where S is a 3x3 matrix)

        S = s1 * R1 + s2 * R2 - s3 * R3_raw - s4 * R4_raw

        # Check: S*n should give the same as B_plaq(Q, v) up to sign
        # (the overall (-1)^{|x|} factor cancels when we take |B|^2)

        # Eigenvalues of S^T S
        eigs_STS = np.linalg.eigvalsh(S.T @ S)
        op_norm_sq = eigs_STS[-1]

        if is_contributing:
            S_matrices_contrib.append((S, op_norm_sq, eigs_STS))
        else:
            S_matrices_noncontrib.append((S, op_norm_sq, eigs_STS))

    print("\n=== S MATRIX ANALYSIS ===")
    print(f"Contributing plaquettes: {len(S_matrices_contrib)}")
    print(f"Non-contributing plaquettes: {len(S_matrices_noncontrib)}")

    contrib_opnorms = [x[1] for x in S_matrices_contrib]
    noncontrib_opnorms = [x[1] for x in S_matrices_noncontrib]

    print(f"\nContributing ||S||^2: min={min(contrib_opnorms):.6f}, max={max(contrib_opnorms):.6f}")
    print(f"  (Should be <= 16 by triangle inequality)")

    if noncontrib_opnorms:
        print(f"Non-contributing ||S||^2: min={min(noncontrib_opnorms):.6f}, max={max(noncontrib_opnorms):.6f}")

    # For Q=I, contributing should have ||S||^2 = 16, non-contributing = 0

    # Key: sum over ALL plaquettes of lambda_max(S^T S) / n_plaq gives avg bound
    all_opnorms = contrib_opnorms + noncontrib_opnorms
    print(f"\nSum of all ||S||^2_op = {sum(all_opnorms):.4f}")
    print(f"  Need: sum * |n|^2 <= 16 * |v|^2 = 16")
    print(f"  Actual max v^T M(Q) v / |v|^2 uses directional S*n, not ||S||_op*|n|")

    return S_matrices_contrib, S_matrices_noncontrib


def prove_per_plaquette_bound(lat, Q, basis, staggered_modes, partitions):
    """
    KEY PROOF ATTEMPT: For each staggered mode v and plaquette plaq:

    B_plaq(Q, v) = S_plaq * n where S = s1*I + s2*Ad(Q1) - s3*Ad(P2) - s4*Ad(U)

    For contributing plaquettes (f(mu) != f(nu)):
      s1=s4=(+1)^{|x|+f(mu)}, s2=s3=(-1)^{|x|+1+f(nu)}
      Actually need to track signs more carefully.

    The CRITICAL identity:
      S^T S = 4I + sum_{i!=j} sigma_ij R_i^T R_j

    where sigma_ij are products of the edge signs and transport signs.

    We need: max_n n^T (sum_plaq S_plaq^T S_plaq) n <= 16 * |n|^2 * n_edges

    This is equivalent to: sum_plaq S_plaq^T S_plaq is bounded by 16 * n_edges / 3 * I_3
    (since |v|^2 = n_edges * |n|^2 and we optimize over unit n).

    Actually: v^T M(Q) v = sum_plaq |S_plaq n|^2 = n^T (sum_plaq S_plaq^T S_plaq) n

    And we need this <= 16 * n_edges * |n|^2 = 16 (for unit v with |n|^2 = 1/n_edges)

    So: n^T (sum_plaq S_plaq^T S_plaq) n <= 16 * n_edges * |n|^2 = 16

    i.e.: sum_plaq S_plaq^T S_plaq <= 16 * n_edges * I_3 ??

    No wait, |n|^2 = 1/n_edges for unit v. So:
    v^T M(Q) v = |n|^2 * n^hat^T (sum_plaq S_plaq^T S_plaq) n^hat
    where n^hat = n/|n|.

    So v^T M(Q) v = (1/n_edges) * n^hat^T (sum_plaq S_plaq^T S_plaq) n^hat

    We need this <= 16, so: lambda_max(sum_plaq S_plaq^T S_plaq) <= 16 * n_edges
    """

    print("\n=== PER-PLAQUETTE SUM BOUND ===")

    # For each partition + color, compute sum of S^T S
    for part_idx, f in enumerate(partitions):
        total_STS = np.zeros((3, 3))

        for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
            Q1 = Q[e1]
            Q12 = Q1 @ Q[e2]
            Q123inv = Q12 @ np.conj(Q[e3]).T
            U_plaq = Q123inv @ np.conj(Q[e4]).T

            R1 = np.eye(3)
            R2 = ad_matrix(Q1, basis)
            R3_raw = ad_matrix(Q123inv, basis)
            R4_raw = ad_matrix(U_plaq, basis)

            coords_x = lat.site_coords(x)
            parity_x = sum(coords_x) % 2

            s1 = (-1)**(parity_x + f[mu])
            s2 = (-1)**(parity_x + 1 + f[nu])
            s3 = (-1)**(parity_x + 1 + f[mu])
            s4 = (-1)**(parity_x + f[nu])

            S = s1 * R1 + s2 * R2 - s3 * R3_raw - s4 * R4_raw
            total_STS += S.T @ S

        eigs_total = np.linalg.eigvalsh(total_STS)
        bound = 16 * lat.n_edges  # = 16 * 64 = 1024

        print(f"  Partition {part_idx} (f={f}):")
        print(f"    Eigenvalues of sum S^T S: {eigs_total}")
        print(f"    Max eigenvalue: {eigs_total[-1]:.6f}")
        print(f"    Bound (16*n_edges): {bound}")
        print(f"    Satisfies bound: {eigs_total[-1] <= bound + 1e-8}")
        print(f"    Rayleigh quotient: {eigs_total[-1] / lat.n_edges:.6f} (need <= 16)")


def verify_B_BBT_identity(lat, Q, basis):
    """Verify B_plaq B_plaq^T = 4*I_3 for all plaquettes."""
    max_err = 0.0
    for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
        Q1 = Q[e1]
        Q12 = Q1 @ Q[e2]
        Q123inv = Q12 @ np.conj(Q[e3]).T
        U_plaq = Q123inv @ np.conj(Q[e4]).T

        R1 = np.eye(3)
        R2 = ad_matrix(Q1, basis)
        R3 = -ad_matrix(Q123inv, basis)
        R4 = -ad_matrix(U_plaq, basis)

        # B_plaq as 3x12 matrix
        B = np.zeros((3, 12))
        B[:, 0:3] = R1
        B[:, 3:6] = R2
        B[:, 6:9] = R3
        B[:, 9:12] = R4

        BBT = B @ B.T
        err = np.max(np.abs(BBT - 4*np.eye(3)))
        max_err = max(max_err, err)

    print(f"\n=== B B^T = 4I CHECK ===")
    print(f"Max error: {max_err:.2e}")
    return max_err < 1e-10


def key_identity_check(lat, Q, basis, staggered_modes, partitions):
    """
    Check the CRUCIAL per-plaquette identity for the proof:

    For a staggered mode v with partition f and color n:
      B_plaq(Q, v) = sigma * S_plaq * n

    where S_plaq depends on the transport matrices and signs.

    Key fact: S = s1*I + s2*R2 - s3*R3 - s4*R4 where:
    - s1, s2, s3, s4 are staggering signs
    - R2, R3, R4 are SO(3) transport matrices

    For CONTRIBUTING plaquettes (f(mu) != f(nu)):
      Signs simplify to: s1 = sigma, s2 = sigma, s3 = -sigma, s4 = -sigma
      (where sigma = (-1)^{|x|+f(mu)})

      Wait, need to check this.
    """
    print("\n=== SIGN PATTERN ANALYSIS ===")

    f = partitions[0]  # [0, 0, 1, 1]

    for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes()[:6]:  # first few
        coords_x = lat.site_coords(x)
        parity_x = sum(coords_x) % 2
        is_contributing = (f[mu] != f[nu])

        # Edge values for staggered mode
        s1 = (-1)**(parity_x + f[mu])
        s2 = (-1)**(parity_x + 1 + f[nu])
        s3_mode = (-1)**(parity_x + 1 + f[mu])  # edge value sign
        s4_mode = (-1)**(parity_x + f[nu])

        # In B_plaq: R3 has the - sign built in, R4 has - sign built in
        # B = R1*v1 + R2*v2 + R3*v3 + R4*v4
        # = I*(s1*n) + Ad(Q1)*(s2*n) + (-Ad(P2))*(s3_mode*n) + (-Ad(U))*(s4_mode*n)
        # = s1*I*n + s2*Ad(Q1)*n - s3_mode*Ad(P2)*n - s4_mode*Ad(U)*n

        # Effective signs in S: s1, s2, -s3_mode, -s4_mode
        eff1 = s1
        eff2 = s2
        eff3 = -s3_mode
        eff4 = -s4_mode

        print(f"  Plaq ({x},{mu},{nu}): contrib={is_contributing}, "
              f"signs=[{s1},{s2},{s3_mode},{s4_mode}], "
              f"eff=[{eff1},{eff2},{eff3},{eff4}]")

        if is_contributing:
            # For contributing: f[mu] != f[nu]
            # s1 = (-1)^{p+f(mu)}, s2 = (-1)^{p+1+f(nu)}
            # Since f(mu) != f(nu): one is 0 and other is 1
            # s1 = (-1)^{p+f(mu)}, s2 = (-1)^{p+1+f(nu)} = (-1)^{p+1+(1-f(mu))} = (-1)^{p+f(mu)}
            # Wait: f(nu) = 1-f(mu) only for balanced partition? Not quite.
            # Let me just check: are all 4 effective signs the same?
            print(f"    All eff same: {eff1==eff2==eff3==eff4}")
        else:
            # For non-contributing: f[mu] = f[nu]
            print(f"    Pattern: eff signs should alternate")


def parallelogram_test(lat, Q, basis, staggered_modes, partitions):
    """
    Test the parallelogram law approach for paired plaquettes.

    For contributing plaq: B(Q,v) ~ [I + A + B + C]*n where A,B,C in SO(3)
    For non-contributing plaq: B(Q,v) ~ [I - A + B - C]*n (DIFFERENT signs)

    Parallelogram law: |u+w|^2 + |u-w|^2 = 2|u|^2 + 2|w|^2

    With u = (I+B)n, w = (A+C)n:
    |(I+A+B+C)n|^2 + |(I-A+B-C)n|^2 = 2|(I+B)n|^2 + 2|(A+C)n|^2

    Each: |(I+B)n|^2 = 2+2n.Bn <= 4, |(A+C)n|^2 = 2+2An.Cn <= 4

    So paired sum <= 16. But pairing doesn't work 1-to-1!

    For d=4, partition {0,1}|{2,3}: 4 contributing, 2 non-contributing orientations.
    Ratio: 2:1, not 1:1.
    """
    print("\n=== PARALLELOGRAM LAW TEST ===")

    f = partitions[0]  # [0, 0, 1, 1]

    # Count contributing vs non-contributing
    n_contrib = 0
    n_noncontrib = 0
    for mu in range(lat.d):
        for nu in range(mu+1, lat.d):
            if f[mu] != f[nu]:
                n_contrib += 1
            else:
                n_noncontrib += 1

    print(f"Partition {f}: {n_contrib} contributing orientations, {n_noncontrib} non-contributing")
    print(f"Ratio: {n_contrib}:{n_noncontrib}")

    # Per site x: compute the sum for one specific x
    x = 0
    coords_x = lat.site_coords(x)
    parity_x = sum(coords_x) % 2

    sum_STS = np.zeros((3, 3))

    for mu in range(lat.d):
        for nu in range(mu+1, lat.d):
            e1 = lat.edge_index(x, mu)
            x_mu = lat.shifted_site(x, mu)
            e2 = lat.edge_index(x_mu, nu)
            x_nu = lat.shifted_site(x, nu)
            e3 = lat.edge_index(x_nu, mu)
            e4 = lat.edge_index(x, nu)

            Q1 = Q[e1]
            Q12 = Q1 @ Q[e2]
            Q123inv = Q12 @ np.conj(Q[e3]).T
            U_plaq = Q123inv @ np.conj(Q[e4]).T

            # Transport SO(3) matrices
            A = ad_matrix(Q1, basis)          # Ad(Q1)
            B_mat = ad_matrix(Q123inv, basis)  # Ad(Q1 Q2 Q3^{-1})
            C = ad_matrix(U_plaq, basis)       # Ad(U_plaq)

            is_contributing = (f[mu] != f[nu])

            s1 = (-1)**(parity_x + f[mu])
            s2 = (-1)**(parity_x + 1 + f[nu])
            s3_mode = (-1)**(parity_x + 1 + f[mu])
            s4_mode = (-1)**(parity_x + f[nu])

            S = s1 * np.eye(3) + s2 * A - s3_mode * B_mat - s4_mode * C

            sum_STS += S.T @ S

            sq_S = np.linalg.eigvalsh(S.T @ S)

            label = "CONTRIB" if is_contributing else "NON-CONTRIB"
            print(f"  ({mu},{nu}) {label}: ||S||^2_op = {sq_S[-1]:.6f}, "
                  f"tr(S^T S) = {np.trace(S.T@S):.6f}")

    eigs_sum = np.linalg.eigvalsh(sum_STS)
    print(f"\n  Sum over all 6 orientations at site {x}:")
    print(f"  Eigenvalues of sum S^T S: {eigs_sum}")
    print(f"  Max eigenvalue per site: {eigs_sum[-1]:.6f}")
    print(f"  Total bound (per site): {eigs_sum[-1] / lat.n_edges:.6f} * n_edges")


# ============================================================
# Main
# ============================================================

def main():
    L, d = 2, 4
    lat = Lattice(L, d)
    basis = su2_basis()

    print(f"Lattice: L={L}, d={d}")
    print(f"Sites: {lat.n_sites}, Edges: {lat.n_edges}, Plaquettes: {lat.n_plaq}")
    print()

    # Build K_curl
    K_curl = build_K_curl(lat)

    # Analyze top eigenspace
    P, staggered_modes, partitions = analyze_top_eigenspace(lat, K_curl)

    # Test with various Q
    configs = [
        ("Identity", np.array([np.eye(2, dtype=complex) for _ in range(lat.n_edges)])),
        ("Random Haar", np.array([random_su2() for _ in range(lat.n_edges)])),
    ]

    # Add a near-identity config
    Q_near = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    for e in range(lat.n_edges):
        vec = np.random.randn(3) * 0.5
        A = sum(v * b for v, b in zip(vec, basis))
        Q_near[e] = expm_su2(A)
    configs.append(("Near-I eps=0.5", Q_near))

    for name, Q in configs:
        print(f"\n{'='*60}")
        print(f"CONFIG: {name}")
        print(f"{'='*60}")

        # Verify B B^T = 4I
        verify_B_BBT_identity(lat, Q, basis)

        # Per-plaquette decomposition
        results = per_plaquette_decomposition(lat, Q, basis, staggered_modes, partitions)

        print("\n  Per-plaquette decomposition:")
        print(f"  {'Mode':>6} {'v^T M(Q) v':>14} {'v^T M(I) v':>14} {'Diff':>14} {'Contrib Q':>14} {'NonContrib Q':>14}")
        for r in results:
            print(f"  {r['mode']:>6} {r['total_Q']:>14.6f} {r['total_I']:>14.6f} "
                  f"{r['RQ_diag']:>14.6f} {r['contributing_Q']:>14.6f} {r['noncontributing_Q']:>14.6f}")

        # Check: is the total always <= 16?
        max_rq = max(r['total_Q'] / r['norm_v_sq'] for r in results)
        print(f"\n  Max Rayleigh quotient: {max_rq:.10f} (need <= 16)")

        # S matrix analysis
        test_S_matrix_bound(lat, Q, basis, staggered_modes, partitions)

        # Per-plaquette sum bound
        prove_per_plaquette_bound(lat, Q, basis, staggered_modes, partitions)

        # Sign pattern
        key_identity_check(lat, Q, basis, staggered_modes, partitions)

        # Parallelogram test
        parallelogram_test(lat, Q, basis, staggered_modes, partitions)


if __name__ == "__main__":
    main()
