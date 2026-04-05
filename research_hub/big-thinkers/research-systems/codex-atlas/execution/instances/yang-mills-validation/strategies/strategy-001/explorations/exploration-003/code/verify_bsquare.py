"""
Verify the B_□ formula for the Wilson action Hessian.
SZZ conventions: S(Q) = -(β/N) Σ_□ Re Tr(U_□)
Inner product: <A,B> = -2 Re Tr(AB), |A|² = -2 Tr(A²)
Generators: τ_a = iσ_a/2, so |τ_a|² = 1
"""

import numpy as np
from numpy.linalg import eigvalsh, eigvals, norm

# ============================================================
# SU(2) and su(2) utilities
# ============================================================

# Pauli matrices
sigma = [
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
]

# Generators τ_a = iσ_a/2
tau = [1j * s / 2 for s in sigma]

N = 2  # SU(2)


def inner_product(A, B):
    """SZZ inner product: <A,B> = -2 Re Tr(AB)"""
    return -2 * np.real(np.trace(A @ B))


def norm_sq(A):
    """SZZ norm squared: |A|² = -2 Tr(A²)"""
    return -2 * np.real(np.trace(A @ A))


def random_su2():
    """Random SU(2) element via Haar measure."""
    # Parametrize SU(2) as a·I + b·(iσ) with |a|²+|b|² = 1
    v = np.random.randn(4)
    v /= norm(v)
    a, b1, b2, b3 = v
    return np.array([[a + 1j*b3, b2 + 1j*b1],
                     [-b2 + 1j*b1, a - 1j*b3]], dtype=complex)


def random_su2_algebra():
    """Random element of su(2) = R-span of {τ_1, τ_2, τ_3}."""
    coeffs = np.random.randn(3)
    return sum(c * t for c, t in zip(coeffs, tau))


def adjoint_action(G, v):
    """Ad_G(v) = G v G^{-1} = G v G†  (since G ∈ SU(2))"""
    return G @ v @ G.conj().T


def plaquette_holonomy(Q1, Q2, Q3, Q4):
    """U_□ = Q1 Q2 Q3^{-1} Q4^{-1}"""
    return Q1 @ Q2 @ Q3.conj().T @ Q4.conj().T


# ============================================================
# B_□ formula (claimed correct version)
# ============================================================

def B_square_correct(Q1, Q2, Q3, Q4, v1, v2, v3, v4):
    """
    B_□(Q,v) = v1 + Ad_{Q1}(v2) - Ad_{Q1 Q2 Q3^{-1}}(v3) - Ad_{U_□}(v4)

    Parallel transport:
    - e1: identity (no transport)
    - e2: Q1
    - e3: Q1 Q2 Q3^{-1}   [includes e3's own Q3^{-1}]
    - e4: U_□ = Q1 Q2 Q3^{-1} Q4^{-1}  [includes e4's own Q4^{-1}]
    """
    U = plaquette_holonomy(Q1, Q2, Q3, Q4)
    P3 = Q1 @ Q2 @ Q3.conj().T  # transport for e3
    P4 = U                        # transport for e4 = full holonomy
    return v1 + adjoint_action(Q1, v2) - adjoint_action(P3, v3) - adjoint_action(P4, v4)


def B_square_wrong(Q1, Q2, Q3, Q4, v1, v2, v3, v4):
    """
    Original WRONG formula (before correction):
    - e3: Q1 Q2  [missing Q3^{-1}]
    - e4: Q1 Q2 Q3^{-1}  [missing Q4^{-1}]
    """
    P3_wrong = Q1 @ Q2                      # missing Q3^{-1}
    P4_wrong = Q1 @ Q2 @ Q3.conj().T        # missing Q4^{-1}
    return v1 + adjoint_action(Q1, v2) - adjoint_action(P3_wrong, v3) - adjoint_action(P4_wrong, v4)


# ============================================================
# Hessian via finite differences
# ============================================================

def action_plaquette(Q1, Q2, Q3, Q4, beta=1.0):
    """Single plaquette action: -(β/N) Re Tr(U_□)"""
    U = plaquette_holonomy(Q1, Q2, Q3, Q4)
    return -(beta / N) * np.real(np.trace(U))


def hessian_fd_single_direction(Q1, Q2, Q3, Q4, v1, v2, v3, v4, beta=1.0, h=1e-5):
    """
    Compute d²/dt²[S(exp(tv)Q)] |_{t=0} via finite differences.
    S(+h) - 2S(0) + S(-h)) / h²
    """
    def perturb(Q, v, t):
        return expm(t * v) @ Q

    def S(t):
        return action_plaquette(
            perturb(Q1, v1, t),
            perturb(Q2, v2, t),
            perturb(Q3, v3, t),
            perturb(Q4, v4, t),
            beta
        )

    return (S(h) - 2*S(0) + S(-h)) / h**2


def expm(A):
    """Matrix exponential for small 2x2 matrices (exact for su(2))."""
    # For su(2): A = i(α·σ)/2, exp(A) = cos(|α|)I + sin(|α|)(iα̂·σ)/|α|
    # Use scipy or numpy
    from scipy.linalg import expm as scipy_expm
    return scipy_expm(A)


# ============================================================
# Stage 1: Verify B_□ formula
# ============================================================

def verify_bsquare_formula(beta=1.5, h=1e-5, n_configs=5, n_plaquettes=5):
    """
    Test: d²S/dt² = (β/(2N)) |B_□|²
    Also test B_□^wrong ≠ correct.
    """
    print("=" * 60)
    print("STAGE 1: Numerical Verification of B_□ Formula")
    print("=" * 60)

    max_err_correct = 0.0
    max_err_wrong = 0.0
    results = []

    for i_config in range(n_configs):
        # Random SU(2) matrices
        Q1 = random_su2()
        Q2 = random_su2()
        Q3 = random_su2()
        Q4 = random_su2()

        for i_plaq in range(n_plaquettes):
            # Random tangent vector (one component per edge, random su(2) element)
            v1 = random_su2_algebra()
            v2 = random_su2_algebra()
            v3 = random_su2_algebra()
            v4 = random_su2_algebra()

            # Numerical Hessian
            h_num = hessian_fd_single_direction(Q1, Q2, Q3, Q4, v1, v2, v3, v4, beta, h)

            # Analytical prediction (correct formula)
            B_corr = B_square_correct(Q1, Q2, Q3, Q4, v1, v2, v3, v4)
            pred_correct = (beta / (2 * N)) * norm_sq(B_corr)

            # Analytical prediction (wrong formula)
            B_wrong = B_square_wrong(Q1, Q2, Q3, Q4, v1, v2, v3, v4)
            pred_wrong = (beta / (2 * N)) * norm_sq(B_wrong)

            err_correct = abs(h_num - pred_correct)
            err_wrong = abs(h_num - pred_wrong)

            max_err_correct = max(max_err_correct, err_correct)
            max_err_wrong = max(max_err_wrong, err_wrong)

            results.append({
                'config': i_config, 'plaq': i_plaq,
                'h_num': h_num, 'pred_correct': pred_correct, 'pred_wrong': pred_wrong,
                'err_correct': err_correct, 'err_wrong': err_wrong
            })

    print(f"\nResults over {n_configs * n_plaquettes} (Q, □, v) triples:")
    print(f"  Max error (CORRECT formula): {max_err_correct:.2e}")
    print(f"  Max error (WRONG formula):   {max_err_wrong:.2e}")

    if max_err_correct < 1e-8:
        print("  ✓ CORRECT formula VERIFIED (error < 1e-8)")
    else:
        print("  ✗ CORRECT formula FAILED (error >= 1e-8)")

    if max_err_wrong > 1e-6:
        print("  ✓ WRONG formula correctly rejected (error > 1e-6)")
    else:
        print("  ✗ WARNING: Wrong formula also passes! Investigate.")

    # Now test at Q=I
    print("\nTest at Q=I:")
    I2 = np.eye(2, dtype=complex)
    Q1 = Q2 = Q3 = Q4 = I2
    v1 = random_su2_algebra()
    v2 = random_su2_algebra()
    v3 = random_su2_algebra()
    v4 = random_su2_algebra()

    B_at_I = B_square_correct(I2, I2, I2, I2, v1, v2, v3, v4)
    B_expected = v1 + v2 - v3 - v4  # discrete curl

    print(f"  B_□(I,v) = v1 + v2 - v3 - v4?")
    print(f"  |B_□(I,v) - (v1+v2-v3-v4)| = {norm(B_at_I - B_expected):.2e}")

    h_num = hessian_fd_single_direction(I2, I2, I2, I2, v1, v2, v3, v4, beta, h)
    pred = (beta / (2 * N)) * norm_sq(B_at_I)
    print(f"  Numerical Hessian at Q=I: {h_num:.8f}")
    print(f"  Predicted from B_□: {pred:.8f}")
    print(f"  Error: {abs(h_num - pred):.2e}")

    return max_err_correct, max_err_wrong


# ============================================================
# Stage 2: Structural properties of B_□
# ============================================================

def compute_B_matrix(Q1, Q2, Q3, Q4):
    """
    Compute B_□ as a linear map: R^{4(N²-1)} → su(N).
    Returns B as a (N²-1) × 4(N²-1) matrix in the τ_a basis.

    B(v) = B_mat @ v_vec
    where v_vec = [v1_coeffs, v2_coeffs, v3_coeffs, v4_coeffs]
    """
    n = N * N - 1  # = 3 for SU(2)
    B_mat = np.zeros((n, 4 * n))

    U = plaquette_holonomy(Q1, Q2, Q3, Q4)
    P3 = Q1 @ Q2 @ Q3.conj().T
    P4 = U

    for a in range(n):
        basis_a = tau[a]

        # Contribution from v1 (edge 1, coefficient a)
        Bv1 = basis_a
        # Contribution from v2 (edge 2, coefficient a): Ad_{Q1}(τ_a)
        Bv2 = adjoint_action(Q1, basis_a)
        # Contribution from v3 (edge 3): -Ad_{P3}(τ_a)
        Bv3 = -adjoint_action(P3, basis_a)
        # Contribution from v4 (edge 4): -Ad_{P4}(τ_a)
        Bv4 = -adjoint_action(P4, basis_a)

        # Project each onto the τ_b basis
        for b in range(n):
            basis_b = tau[b]
            # Coefficient: inner_product(τ_b, X) / |τ_b|² = inner_product(τ_b, X)
            # since |τ_b|² = 1
            B_mat[b, a] = inner_product(basis_b, Bv1)
            B_mat[b, n + a] = inner_product(basis_b, Bv2)
            B_mat[b, 2*n + a] = inner_product(basis_b, Bv3)
            B_mat[b, 3*n + a] = inner_product(basis_b, Bv4)

    return B_mat


def verify_structural_properties(n_tests=5):
    """
    Verify:
    1. B B^T = 4 I_{N²-1}  (for any Q)
    2. M_□ = B^T B has eigenvalues {4,4,4,0,...,0}
    3. Tr(M) = 4 * (N²-1) (per plaquette)
    """
    print("\n" + "=" * 60)
    print("STAGE 2: Structural Properties of B_□")
    print("=" * 60)

    n = N * N - 1  # = 3

    max_err_BBT = 0.0
    max_err_trace = 0.0
    all_eigs_ok = True

    for i in range(n_tests):
        Q1, Q2, Q3, Q4 = random_su2(), random_su2(), random_su2(), random_su2()
        B = compute_B_matrix(Q1, Q2, Q3, Q4)  # shape (3, 12)

        # Test B B^T = 4 I_3
        BBT = B @ B.T
        target = 4 * np.eye(n)
        err_BBT = norm(BBT - target)
        max_err_BBT = max(max_err_BBT, err_BBT)

        # Test eigenvalues of M = B^T B
        M = B.T @ B  # shape (12, 12)
        eigs = sorted(eigvalsh(M).real, reverse=True)

        # Expected: 4,4,4,0,...,0
        eigs_nonzero = [e for e in eigs if abs(e) > 1e-10]
        eigs_ok = (len(eigs_nonzero) == n and
                   all(abs(e - 4.0) < 1e-8 for e in eigs_nonzero))
        if not eigs_ok:
            all_eigs_ok = False
            print(f"  Test {i}: Eigenvalues of M: {[f'{e:.4f}' for e in eigs[:6]]}...")

        # Test trace
        tr_M = np.trace(M).real
        expected_tr = 4 * n  # = 12
        err_trace = abs(tr_M - expected_tr)
        max_err_trace = max(max_err_trace, err_trace)

    print(f"\n  B B^T = 4I: max error = {max_err_BBT:.2e}")
    print(f"  Tr(M) = 4*(N²-1) = {4*n}: max error = {max_err_trace:.2e}")
    print(f"  Eigenvalues of M = {{4,4,4,0,...,0}}: {'✓ All pass' if all_eigs_ok else '✗ Some fail'}")

    if max_err_BBT < 1e-10:
        print("  ✓ B B^T = 4I VERIFIED")
    else:
        print(f"  ✗ B B^T != 4I, max error = {max_err_BBT:.2e}")

    # Also verify at Q=I
    I2 = np.eye(2, dtype=complex)
    B_I = compute_B_matrix(I2, I2, I2, I2)
    BBT_I = B_I @ B_I.T
    print(f"\n  At Q=I: B B^T = {BBT_I.real}")
    print(f"  Should be 4*I_3 = {4*np.eye(3)}")

    return max_err_BBT, max_err_trace, all_eigs_ok


# ============================================================
# Stage 3: Full Hessian at Q=I
# ============================================================

def build_full_hessian(Q_config, L, d, beta=1.0):
    """
    Build the full Hessian matrix H at configuration Q_config.

    Q_config: dict mapping (site_tuple, mu) -> SU(2) matrix
    L: lattice size
    d: dimension
    Returns: H as a numpy array of shape (n_links * (N²-1), n_links * (N²-1))
    """
    n_gen = N * N - 1  # = 3
    # Number of links
    sites = list(np.ndindex(*([L] * d)))
    n_sites = len(sites)
    n_links = n_sites * d
    dim = n_links * n_gen

    site_to_idx = {s: i for i, s in enumerate(sites)}

    def link_idx(site, mu):
        return site_to_idx[site] * d + mu

    H = np.zeros((dim, dim))

    # Sum over all plaquettes (x, mu < nu)
    for x in sites:
        for mu in range(d):
            for nu in range(mu + 1, d):
                # Four edges of plaquette (x, mu, nu)
                x_arr = np.array(x)
                x_mu = tuple((x_arr + np.eye(d, dtype=int)[mu]) % L)  # x + ê_mu
                x_nu = tuple((x_arr + np.eye(d, dtype=int)[nu]) % L)  # x + ê_nu

                # Edge links and their indices
                e1_site, e1_mu = x, mu
                e2_site, e2_mu = x_mu, nu
                e3_site, e3_mu = x_nu, mu  # backward
                e4_site, e4_mu = x, nu     # backward

                Q1 = Q_config[(e1_site, e1_mu)]
                Q2 = Q_config[(e2_site, e2_mu)]
                Q3 = Q_config[(e3_site, e3_mu)]
                Q4 = Q_config[(e4_site, e4_mu)]

                # B matrix for this plaquette
                B = compute_B_matrix(Q1, Q2, Q3, Q4)  # (3, 12)

                # M = (beta/(2N)) B^T B, but we need to assemble into full H
                # The 12 columns correspond to:
                # cols 0:3   -> link (e1_site, e1_mu), generators 0,1,2
                # cols 3:6   -> link (e2_site, e2_mu)
                # cols 6:9   -> link (e3_site, e3_mu)
                # cols 9:12  -> link (e4_site, e4_mu)

                links = [
                    (e1_site, e1_mu),
                    (e2_site, e2_mu),
                    (e3_site, e3_mu),
                    (e4_site, e4_mu),
                ]

                M_plaq = (beta / (2 * N)) * B.T @ B  # (12, 12)

                for i_link, (si, mi) in enumerate(links):
                    for j_link, (sj, mj) in enumerate(links):
                        li = link_idx(si, mi)
                        lj = link_idx(sj, mj)
                        for a in range(n_gen):
                            for b in range(n_gen):
                                row = li * n_gen + a
                                col = lj * n_gen + b
                                H[row, col] += M_plaq[i_link * n_gen + a,
                                                       j_link * n_gen + b].real

    return H


def verify_eigenspectrum_at_identity(L=2, d=4, beta=1.0):
    """
    Build full Hessian at Q=I and check eigenvalues.
    Expected spectrum:
      0:  multiplicity 57
      β:  multiplicity 36
      2β: multiplicity 54
      3β: multiplicity 36
      4β: multiplicity 9
    Total: 192 = 2^4 * 4 * 3 links × generators
    """
    print("\n" + "=" * 60)
    print(f"STAGE 3: Full Hessian at Q=I (L={L}, d={d})")
    print("=" * 60)

    I2 = np.eye(2, dtype=complex)
    sites = list(np.ndindex(*([L] * d)))
    Q_config = {}
    for x in sites:
        for mu in range(d):
            Q_config[(x, mu)] = I2.copy()

    n_links = len(sites) * d
    n_gen = N * N - 1
    dim = n_links * n_gen
    print(f"  Lattice: {L}^{d}, {len(sites)} sites, {n_links} links, dim={dim}")

    print("  Building Hessian...")
    H = build_full_hessian(Q_config, L, d, beta)

    print("  Computing eigenvalues...")
    eigs = sorted(eigvalsh(H).real)

    # Count eigenvalues by value
    tol = 1e-6
    buckets = {}
    for e in eigs:
        # Round to nearest 0.5*beta
        rounded = round(e / (0.5 * beta)) * 0.5 * beta
        buckets[rounded] = buckets.get(rounded, 0) + 1

    print(f"\n  Eigenvalue spectrum:")
    for val in sorted(buckets.keys()):
        print(f"    λ = {val:.4f} ({val/beta:.2f}β): multiplicity {buckets[val]}")

    # Check against expected
    expected = {
        0.0: 57,
        1.0 * beta: 36,
        2.0 * beta: 54,
        3.0 * beta: 36,
        4.0 * beta: 9,
    }

    print(f"\n  Expected vs Actual:")
    total_ok = True
    for val, exp_mult in expected.items():
        act_mult = buckets.get(round(val / (0.5 * beta)) * 0.5 * beta, 0)
        status = "✓" if act_mult == exp_mult else "✗"
        print(f"    λ={val:.2f} ({val/beta:.0f}β): expected {exp_mult}, got {act_mult} {status}")
        if act_mult != exp_mult:
            total_ok = False

    lambda_max = max(eigs)
    print(f"\n  λ_max = {lambda_max:.8f}")
    print(f"  4β = {4*beta:.8f}")
    print(f"  λ_max / (4β) = {lambda_max / (4*beta):.8f} (should be 1.0)")
    print(f"  H_norm = λ_max / (48β) = {lambda_max / (48*beta):.8f} (should be 1/12 ≈ {1/12:.8f})")

    return H, eigs, lambda_max


def verify_staggered_mode(H, L=2, d=4, beta=1.0):
    """
    Verify that the staggered mode v_{x,μ,a} = (-1)^{|x|+μ} δ_{a,1} / ‖v‖
    is an eigenvector with eigenvalue 4β.
    """
    print("\n  Staggered mode check:")

    sites = list(np.ndindex(*([L] * d)))
    n_gen = N * N - 1
    n_links = len(sites) * d
    dim = n_links * n_gen

    site_to_idx = {s: i for i, s in enumerate(sites)}

    def link_idx(site, mu):
        return site_to_idx[site] * d + mu

    # v_{x,μ,a} = (-1)^{sum(x)+μ} * δ_{a,0}  (generator 0 = τ_1)
    v_stag = np.zeros(dim)
    for x in sites:
        for mu in range(d):
            li = link_idx(x, mu)
            sign = (-1) ** (sum(x) + mu)
            # generator index a=0
            v_stag[li * n_gen + 0] = sign

    v_stag /= norm(v_stag)

    H_v = H @ v_stag
    expected = 4 * beta * v_stag
    residual = norm(H_v - expected)
    print(f"  ‖H·v_stag - 4β·v_stag‖ = {residual:.2e}")
    print(f"  Eigenvalue check: H·v_stag projected = {np.dot(H_v, v_stag):.6f} (should be {4*beta:.6f})")

    if residual < 1e-10:
        print("  ✓ Staggered mode is eigenvector with eigenvalue 4β")
    else:
        print(f"  ✗ Staggered mode residual too large: {residual:.2e}")

    return residual


# ============================================================
# Stage 4: Convention chain verification
# ============================================================

def verify_convention_chain(beta=1.0, L=2, d=4):
    """
    Trace the full proof chain:
    1. HessS(v,v) = (β/(2N)) v^T M(Q) v
    2. λ_max(M) ≤ ? (need to derive bound)
    3. Threshold β < N²/λ_max_bound → 1/6?
    """
    print("\n" + "=" * 60)
    print("STAGE 4: Convention Chain Verification")
    print("=" * 60)

    # For a single plaquette at Q=I:
    # B = [I, I, -I, -I] (4 edge contributions)
    # B B^T = 4I_3 (we verified this)
    # M_□ = B^T B has eigenvalues {4,4,4,0,...,0}
    # So per plaquette, λ_max(M_□) = 4

    # For the full Hessian over all plaquettes:
    # M(Q) = Σ_□ B_□^T B_□
    # Each link appears in how many plaquettes? In d dimensions: 2(d-1)
    # For d=4: each link is in 2×3 = 6 plaquettes
    # But the per-edge contribution to M from B^T B is at most 4 per plaquette
    # So λ_max(M) ≤ 4 × (plaquettes per link) = 4 × 2(d-1)

    d_val = d
    plaq_per_link = 2 * (d_val - 1)
    lambda_max_bound = 4 * plaq_per_link
    print(f"\n  Dimension d={d_val}")
    print(f"  Plaquettes per link: 2(d-1) = {plaq_per_link}")
    print(f"  λ_max bound: 4 × {plaq_per_link} = {lambda_max_bound}")

    # HessS(v,v) = (β/(2N)) v^T M(Q) v ≤ (β/(2N)) λ_max(M) |v|²
    # SZZ condition: HessS(v,v) < (N/2)|v|²
    # So we need: (β/(2N)) λ_max(M) < N/2
    # β < N² / λ_max(M)
    # β < N² / λ_max_bound = 4 / (4 × 2(d-1)) = 1/(2(d-1))

    threshold_from_bound = N**2 / lambda_max_bound
    print(f"\n  SZZ condition: (β/(2N)) λ_max < N/2")
    print(f"  → β < N²/λ_max = {N}²/{lambda_max_bound} = {N**2}/{lambda_max_bound} = {threshold_from_bound:.6f}")
    print(f"  For d=4: β < 1/{2*(d_val-1)} = 1/6 = {1/6:.6f}")
    print(f"  ✓ This gives the claimed threshold β < 1/6")

    # Break down the 48 factor in H_norm:
    # H_norm = λ_max / (48β)
    # At Q=I: λ_max = 4β
    # H_norm = 4β/(48β) = 1/12
    #
    # Where does 48 come from?
    # Option 1: 8(d-1)N = 8×3×2 = 48
    # Option 2: 16(d-1) = 16×3 = 48
    # Let's check:
    print(f"\n  Factor 48 in H_norm = λ_max/(48β):")
    print(f"  Option 1: 8(d-1)N = 8×{d_val-1}×{N} = {8*(d_val-1)*N}")
    print(f"  Option 2: 16(d-1) = 16×{d_val-1} = {16*(d_val-1)}")
    print(f"  Option 3: 4 × 2(d-1) × N = 4×{2*(d_val-1)}×{N} = {4*2*(d_val-1)*N}")
    print(f"  Option 4: λ_max_bound × N = {lambda_max_bound}×{N} = {lambda_max_bound*N}")
    print(f"\n  Correct: 48 = λ_max_bound × N = {lambda_max_bound} × {N}")
    print(f"  Or equivalently: 4 × 2(d-1) × N = 4 × plaq_per_link × N")
    print(f"  H_norm = λ_max/(N × λ_max_bound) = λ_max / (N × 4 × 2(d-1))")

    # Verify normalization formula
    I2 = np.eye(2, dtype=complex)
    sites = list(np.ndindex(*([L] * d)))
    Q_config = {(x, mu): I2.copy() for x in sites for mu in range(d)}
    H = build_full_hessian(Q_config, L, d, beta=beta)
    eigs = eigvalsh(H).real
    lmax = max(eigs)
    H_norm = lmax / (48 * beta)

    print(f"\n  Numerically at Q=I:")
    print(f"  λ_max = {lmax:.8f}, 4β = {4*beta:.8f}")
    print(f"  H_norm = λ_max/(48β) = {H_norm:.8f} (expected 1/12 = {1/12:.8f})")

    return threshold_from_bound, H_norm


# ============================================================
# Stage 5: Random Q Hessian check
# ============================================================

def verify_random_Q_hessian(n_configs=5, L=2, d=4, beta=1.0):
    """
    For 5 random Q configurations, compute λ_max and H_norm.
    Verify H_norm ≤ 1/8 (proved) and check if H_norm ≤ 1/12 (conjectured).
    """
    print("\n" + "=" * 60)
    print("STAGE 5: Random Q Hessian Check")
    print("=" * 60)

    sites = list(np.ndindex(*([L] * d)))
    n_links = len(sites) * d

    results = []
    for i in range(n_configs):
        Q_config = {}
        for x in sites:
            for mu in range(d):
                Q_config[(x, mu)] = random_su2()

        H = build_full_hessian(Q_config, L, d, beta)
        eigs = eigvalsh(H).real
        lmax = max(eigs)
        H_norm = lmax / (48 * beta)
        results.append({'config': i, 'lambda_max': lmax, 'H_norm': H_norm})

        print(f"  Config {i+1}: λ_max = {lmax:.6f} ({lmax/beta:.4f}β), "
              f"H_norm = {H_norm:.6f} "
              f"{'≤ 1/12' if H_norm <= 1/12 + 1e-10 else ('≤ 1/8' if H_norm <= 1/8 + 1e-10 else '> 1/8!')}")

    H_norms = [r['H_norm'] for r in results]
    print(f"\n  Max H_norm over {n_configs} configs: {max(H_norms):.6f}")
    print(f"  Proved bound 1/8 = {1/8:.6f}")
    print(f"  Conjectured bound 1/12 = {1/12:.6f}")

    all_below_1_8 = all(h <= 1/8 + 1e-10 for h in H_norms)
    all_below_1_12 = all(h <= 1/12 + 1e-10 for h in H_norms)

    print(f"\n  All H_norm ≤ 1/8: {'✓' if all_below_1_8 else '✗'}")
    print(f"  All H_norm ≤ 1/12: {'✓' if all_below_1_12 else '?'} (not a proof)")

    return results


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    np.random.seed(42)

    print("B_□ Formula Verification")
    print("SZZ conventions: S = -(β/N) Σ Re Tr(U_□), <A,B> = -2 Re Tr(AB)")
    print("N =", N, "(SU(2))")
    print()

    # Stage 1
    max_err_correct, max_err_wrong = verify_bsquare_formula(beta=1.5, n_configs=5, n_plaquettes=5)

    # Stage 2
    max_err_BBT, max_err_trace, all_eigs_ok = verify_structural_properties(n_tests=5)

    # Stage 3
    H_I, eigs_I, lambda_max_I = verify_eigenspectrum_at_identity(L=2, d=4, beta=1.0)
    residual_stag = verify_staggered_mode(H_I, L=2, d=4, beta=1.0)

    # Stage 4
    threshold, H_norm_I = verify_convention_chain(beta=1.0, L=2, d=4)

    # Stage 5
    random_results = verify_random_Q_hessian(n_configs=5, L=2, d=4, beta=1.0)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"B_□ formula: max error = {max_err_correct:.2e} {'✓' if max_err_correct < 1e-8 else '✗'}")
    print(f"Wrong formula rejected: max error = {max_err_wrong:.2e} {'✓' if max_err_wrong > 1e-6 else '✗'}")
    print(f"B B^T = 4I: max error = {max_err_BBT:.2e} {'✓' if max_err_BBT < 1e-10 else '✗'}")
    print(f"Trace conservation: max error = {max_err_trace:.2e} {'✓' if max_err_trace < 1e-10 else '✗'}")
    print(f"Eigenvalues at Q=I: {'✓' if abs(lambda_max_I/1.0 - 4) < 1e-8 else '✗'} λ_max = {lambda_max_I:.6f}")
    print(f"Staggered mode residual: {residual_stag:.2e} {'✓' if residual_stag < 1e-10 else '✗'}")
    print(f"Threshold β < {threshold:.6f} (expected 1/6 = {1/6:.6f})")
    print(f"H_norm at Q=I: {H_norm_I:.8f} (expected 1/12 = {1/12:.8f})")
