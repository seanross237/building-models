"""
4-Point Tree-Level MHV Amplitude in N=4 SYM — Three Independent Methods

Computes A_4(1⁻, 2⁻, 3⁺, 4⁺) via:
  1. Parke-Taylor formula (analytic)
  2. BCFW recursion (on-shell recursion)
  3. Grassmannian / positive geometry (momentum-space localization)

All methods agree exactly.
"""

import numpy as np
import time
import sys
sys.path.insert(0, '.')
from spinor_helicity import (
    Particle, angle_bracket, square_bracket, ab, sb,
    mandelstam_sij, make_kinematics_com, make_kinematics_from_spinors,
    validate_kinematics, spinors_from_momentum, sigma, sigma_bar
)


# ============================================================
# METHOD 1: PARKE-TAYLOR FORMULA
# ============================================================

def parke_taylor_4pt(p1, p2, p3, p4):
    """Parke-Taylor formula for A_4(1⁻, 2⁻, 3⁺, 4⁺).

    A_4^MHV = ⟨12⟩⁴ / (⟨12⟩⟨23⟩⟨34⟩⟨41⟩) = ⟨12⟩³ / (⟨23⟩⟨34⟩⟨41⟩)
    """
    a12 = ab(p1, p2)
    a23 = ab(p2, p3)
    a34 = ab(p3, p4)
    a41 = ab(p4, p1)

    return a12**4 / (a12 * a23 * a34 * a41)


# ============================================================
# METHOD 2: BCFW RECURSION
# ============================================================

def bcfw_4pt(p1, p2, p3, p4, verbose=False):
    """BCFW recursion for A_4(1⁻, 2⁻, 3⁺, 4⁺) using [1,2⟩ shift.

    Shift: |1̂⟩ = |1⟩ + z|2⟩,  |2̂] = |2] - z|1]
    (|1̂] = |1], |2̂⟩ = |2⟩ unchanged)

    The shifted amplitude A₄(z) = ⟨12⟩³ / (⟨23⟩⟨34⟩(⟨41⟩+z⟨42⟩))

    This has exactly ONE pole in z (from ⟨41̂⟩ = 0), at:
        z_A = -⟨14⟩/⟨24⟩

    This pole corresponds to the color-ordered factorization channel
    {4,1̂} | {2̂,3} with propagator P = p₁+p₄.

    The factorization gives:
        A₄ = A₃^{anti-MHV}(4⁺, 1̂⁻, (-P̂)⁺) × A₃^{MHV}(P̂⁻, 2̂⁻, 3⁺) / P²₁₄

    SIGN CONVENTION: The propagator P₁₄²(z) = (⟨14⟩+z⟨24⟩)[14],
    while the amplitude's denominator has ⟨41⟩+z⟨42⟩ = -(⟨14⟩+z⟨24⟩).
    This introduces a relative (-1) between the naive sub-amplitude product
    and the correct BCFW result.

    See derivation in REPORT.md for details.
    """

    # ----- Single channel: {4,1̂} | {2̂,3} -----
    z_A = -ab(p1, p4) / ab(p2, p4)

    # Shifted spinors at z_A
    lam1_hat = p1.lam + z_A * p2.lam       # |1̂⟩
    ltilde2_hat = p2.lam_tilde - z_A * p1.lam_tilde  # |2̂]

    p1_hat = Particle(1, lam1_hat, p1.lam_tilde)  # |1̂⟩, |1]
    p2_hat = Particle(2, p2.lam, ltilde2_hat)      # |2⟩, |2̂]

    # Internal momentum K = p̂₁ + p₄ (on-shell at z_A since P̂² = 0)
    K_vec = p1_hat.four_momentum + p4.four_momentum
    K = spinors_from_momentum(K_vec, label=98)

    if verbose:
        print(f"  z_A = {z_A:.8f}")
        print(f"  K² = {K.mass_squared:.2e} (should be ~0)")
        print(f"  ⟨1̂ 4⟩ = {ab(p1_hat, p4):.2e} (should be ~0)")

    # LEFT = A₃^{anti-MHV}(4⁺, 1̂⁻, (-P̂)⁺)
    # Using A₃(1⁺,2⁺,3⁻) = [12]³/([23][31]) with 1=4, 2=(-P̂), 3=1̂:
    # After resolving signs from -P̂: [4K]³/([K1̂][1̂4])
    # where [1̂4] = [14] since |1̂] = |1].

    A_L = sb(p4, K)**3 / (sb(K, p1_hat) * sb(p1_hat, p4))

    # RIGHT = A₃^{MHV}(P̂⁻, 2̂⁻, 3⁺) = ⟨K 2̂⟩³/(⟨2̂ 3⟩⟨3 K⟩)
    # where ⟨2̂ 3⟩ = ⟨23⟩ since |2̂⟩ = |2⟩.

    A_R = ab(K, p2_hat)**3 / (ab(p2_hat, p3) * ab(p3, K))

    # Propagator denominator (unshifted s₁₄)
    P_sq = mandelstam_sij(p1, p4)

    # BCFW result: note the crucial minus sign from the relation
    # ⟨41⟩ = -⟨14⟩ in the propagator pole structure.
    # See derivation: A₄(z) = -⟨12⟩³[14]/(⟨23⟩⟨34⟩ × P₁₄²(z)),
    # so A_L × A_R must include this (-1) relative to the naive product.

    A_bcfw = -(A_L * A_R / P_sq)

    if verbose:
        print(f"  A_L = {A_L:.10f}")
        print(f"  A_R = {A_R:.10f}")
        print(f"  P² = s₁₄ = {P_sq:.10f}")
        print(f"  -A_L×A_R/P² = {A_bcfw:.10f}")

    return A_bcfw


def bcfw_4pt_direct(p1, p2, p3, p4):
    """BCFW via direct Cauchy residue on A₄(z) — cross-check.

    A₄(z) = ⟨12⟩³ / (⟨23⟩⟨34⟩(⟨41⟩+z⟨42⟩))

    Single pole at z* = -⟨41⟩/⟨42⟩. Residue via Cauchy:
    A₄(0) = -Res[A₄(z)/z, z*] = ⟨12⟩³/(⟨23⟩⟨34⟩⟨41⟩) = PT.
    """
    a12 = ab(p1, p2)
    a23 = ab(p2, p3)
    a34 = ab(p3, p4)
    a41 = ab(p4, p1)
    a42 = ab(p4, p2)

    z_star = -a41 / a42

    # Residue of A₄(z)/z at z = z*
    # A₄(z) = a12³ / (a23 × a34 × (a41 + z × a42))
    # Near z*: a41 + z × a42 = (z - z*) × a42
    # Res[A₄(z), z*] = a12³ / (a23 × a34 × a42)
    # Res[A₄(z)/z, z*] = Res[A₄(z)] / z*

    residue = a12**3 / (a23 * a34 * a42)
    A4 = -residue / z_star  # Cauchy: A(0) = -Σ Res[A(z)/z]

    return A4


# ============================================================
# METHOD 3: GRASSMANNIAN / POSITIVE GEOMETRY
# ============================================================

def grassmannian_4pt_mhv(p1, p2, p3, p4, verbose=False):
    """Grassmannian computation of A_4(1⁻, 2⁻, 3⁺, 4⁺).

    The Grassmannian integral for G(2,4):

    L_{4,2} = ∫ d^{2×4}C / (vol(GL(2)) × M₁M₂M₃M₄) × δ⁴(C·λ̃) × δ⁴(C⊥·λ)

    Gauge fix C = (I₂ | C'), solve C·Λ̃ = 0 for the free parameters.
    The integral fully localizes to a single point. Result:

        A₄ = 1/(M₁ M₂ M₃ M₄)

    evaluated at the solution C*.

    KEY RESULT: This equals the Parke-Taylor formula exactly.

    The minors in terms of square brackets are:
        M₁ = 1 (gauge), M₂ = [14]/[34], M₃ = [12]/[34], M₄ = -[23]/[34]

    So 1/(M₁M₂M₃M₄) = -[34]³/([12][14][23])
    and this equals ⟨12⟩³/(⟨23⟩⟨34⟩⟨41⟩) by a non-trivial algebraic identity
    that follows from Schouten + momentum conservation.
    """
    particles = [p1, p2, p3, p4]

    # Build λ̃ matrix: 4×2
    Lambda_tilde = np.array([p.lam_tilde for p in particles])
    Lambda = np.array([p.lam for p in particles])

    # Gauge fix: C = (I₂ | C'), solve C·Λ̃ = 0
    lt3, lt4 = Lambda_tilde[2], Lambda_tilde[3]
    M = np.column_stack([lt3, lt4])

    coeffs1 = np.linalg.solve(M, -Lambda_tilde[0])
    coeffs2 = np.linalg.solve(M, -Lambda_tilde[1])

    C = np.zeros((2, 4), dtype=complex)
    C[0, 0] = 1;  C[0, 1] = 0;  C[0, 2] = coeffs1[0];  C[0, 3] = coeffs1[1]
    C[1, 0] = 0;  C[1, 1] = 1;  C[1, 2] = coeffs2[0];  C[1, 3] = coeffs2[1]

    # Verify constraints
    check1 = np.max(np.abs(C @ Lambda_tilde))
    C_perp = np.zeros((2, 4), dtype=complex)
    C_perp[0, :] = [-C[0,2], -C[1,2], 1, 0]
    C_perp[1, :] = [-C[0,3], -C[1,3], 0, 1]
    check2 = np.max(np.abs(C_perp @ Lambda))

    if verbose:
        print(f"  Constraint check: |C·Λ̃| = {check1:.2e}, |C⊥·Λ| = {check2:.2e}")

    # Consecutive 2×2 minors
    def minor(i, j):
        return C[0, i] * C[1, j] - C[0, j] * C[1, i]

    M1 = minor(0, 1)  # (12)
    M2 = minor(1, 2)  # (23)
    M3 = minor(2, 3)  # (34)
    M4 = minor(3, 0)  # (41)

    if verbose:
        s34 = sb(p3, p4)
        print(f"  Minors: M1={M1:.6f}, M2={M2:.6f}, M3={M3:.6f}, M4={M4:.6f}")
        print(f"  Analytic: M1=1, M2=[14]/[34]={sb(p1,p4)/s34:.6f}, "
              f"M3=[12]/[34]={sb(p1,p2)/s34:.6f}, M4=-[23]/[34]={-sb(p2,p3)/s34:.6f}")

    A_grass = 1.0 / (M1 * M2 * M3 * M4)
    return A_grass, C, (M1, M2, M3, M4)


def momentum_twistors_and_geometry(p1, p2, p3, p4, verbose=False):
    """Compute momentum twistors and amplituhedron geometry data."""
    particles = [p1, p2, p3, p4]
    n = len(particles)

    # Dual coordinates x_i: x_{i+1} = x_i - |i⟩[i|, x_1 = 0
    x = [np.zeros((2, 2), dtype=complex)]
    for i in range(n):
        x.append(x[i] - np.outer(particles[i].lam, particles[i].lam_tilde))

    closure = np.max(np.abs(x[n]))

    # Momentum twistors Z_i = (λ_i, μ_i) where μ_i = x_i · λ_i
    Z = []
    for i in range(n):
        mu_i = x[i] @ particles[i].lam
        Z.append(np.concatenate([particles[i].lam, mu_i]))

    # 4-bracket
    def four_bracket(i, j, k, l):
        return np.linalg.det(np.column_stack([Z[i], Z[j], Z[k], Z[l]]))

    Z1234 = four_bracket(0, 1, 2, 3)

    if verbose:
        print(f"  Momentum twistor closure: {closure:.2e}")
        print(f"  ⟨1234⟩ = {Z1234:.6f}")
        for i in range(4):
            print(f"    Z_{i+1} = [{Z[i][0]:.4f}, {Z[i][1]:.4f}, {Z[i][2]:.4f}, {Z[i][3]:.4f}]")

    return Z, Z1234


# ============================================================
# MAIN: Compare all three methods
# ============================================================

def compare_methods(particles, label="", verbose=False):
    """Run all three methods on the same kinematics and compare."""
    p1, p2, p3, p4 = particles

    print(f"\n{'='*70}")
    print(f" {label}")
    print(f"{'='*70}")

    info = validate_kinematics(particles, verbose=verbose)

    # Method 1: Parke-Taylor
    t0 = time.perf_counter()
    A_PT = parke_taylor_4pt(p1, p2, p3, p4)
    t_PT = time.perf_counter() - t0

    # Method 2: BCFW (sub-amplitude factorization)
    t0 = time.perf_counter()
    A_BCFW = bcfw_4pt(p1, p2, p3, p4, verbose=verbose)
    t_BCFW = time.perf_counter() - t0

    # Method 2b: BCFW (direct Cauchy)
    A_BCFW_direct = bcfw_4pt_direct(p1, p2, p3, p4)

    # Method 3: Grassmannian
    t0 = time.perf_counter()
    A_grass, C, minors = grassmannian_4pt_mhv(p1, p2, p3, p4, verbose=verbose)
    t_grass = time.perf_counter() - t0

    if verbose:
        momentum_twistors_and_geometry(p1, p2, p3, p4, verbose=True)

    # Results
    print(f"\n  A_PT           = {A_PT:.12f}")
    print(f"  A_BCFW(sub)    = {A_BCFW:.12f}")
    print(f"  A_BCFW(Cauchy) = {A_BCFW_direct:.12f}")
    print(f"  A_Grass        = {A_grass:.12f}")

    # Ratios
    if abs(A_PT) > 1e-15:
        r_bcfw = A_BCFW / A_PT
        r_bcfw_d = A_BCFW_direct / A_PT
        r_grass = A_grass / A_PT
        err_bcfw = abs(r_bcfw - 1)
        err_bcfw_d = abs(r_bcfw_d - 1)
        err_grass = abs(r_grass - 1)
        print(f"\n  |BCFW(sub)/PT - 1|    = {err_bcfw:.2e}")
        print(f"  |BCFW(Cauchy)/PT - 1| = {err_bcfw_d:.2e}")
        print(f"  |Grass/PT - 1|        = {err_grass:.2e}")

        all_agree = err_bcfw < 1e-8 and err_grass < 1e-8
        print(f"  All agree: {'✓ YES' if all_agree else '✗ NO'}")
    else:
        all_agree = False

    print(f"  Time: PT={t_PT*1e6:.0f}μs, BCFW={t_BCFW*1e6:.0f}μs, Grass={t_grass*1e6:.0f}μs")

    return A_PT, A_BCFW, A_grass, (t_PT, t_BCFW, t_grass), all_agree


if __name__ == "__main__":
    np.set_printoptions(precision=8)

    # ========================================
    # Detailed test (verbose)
    # ========================================
    print("*" * 70)
    print("* DETAILED DIAGNOSTIC TEST")
    print("*" * 70)
    p_detail = make_kinematics_com(E=1.0, theta=np.pi/3)
    compare_methods(p_detail, "DETAILED: COM E=1 θ=π/3", verbose=True)

    # ========================================
    # Full test suite
    # ========================================
    test_cases = [
        ("COM E=1.0 θ=π/3", make_kinematics_com(1.0, np.pi/3)),
        ("COM E=1.0 θ=π/4", make_kinematics_com(1.0, np.pi/4)),
        ("COM E=1.0 θ=π/6", make_kinematics_com(1.0, np.pi/6)),
        ("COM E=1.0 θ=1.0", make_kinematics_com(1.0, 1.0)),
        ("COM E=2.0 θ=2.1", make_kinematics_com(2.0, 2.1)),
        ("COM E=5.0 θ=0.5", make_kinematics_com(5.0, 0.5)),
        ("Random seed=42",  make_kinematics_from_spinors(42)),
        ("Random seed=137", make_kinematics_from_spinors(137)),
        ("Random seed=999", make_kinematics_from_spinors(999)),
        ("Random seed=7",   make_kinematics_from_spinors(7)),
    ]

    results = []
    for name, parts in test_cases:
        A_PT, A_BCFW, A_grass, times, ok = compare_methods(parts, name)
        results.append((name, A_PT, A_BCFW, A_grass, times, ok))

    # ========================================
    # Summary table
    # ========================================
    print(f"\n\n{'='*100}")
    print(f" FINAL SUMMARY TABLE")
    print(f"{'='*100}")
    hdr = f"{'Test':<22} {'A_PT (real part)':<18} {'|BCFW/PT-1|':<14} {'|Grass/PT-1|':<14} {'t_PT':<8} {'t_BCFW':<8} {'t_Grass':<8} {'OK?'}"
    print(hdr)
    print("-" * len(hdr))

    all_ok = True
    for name, apt, abcfw, agrass, times, ok in results:
        err_b = abs(abcfw/apt - 1) if abs(apt) > 1e-15 else float('nan')
        err_g = abs(agrass/apt - 1) if abs(apt) > 1e-15 else float('nan')
        if not ok: all_ok = False
        print(f"{name:<22} {apt.real:<18.10f} {err_b:<14.2e} {err_g:<14.2e} "
              f"{times[0]*1e6:<8.0f} {times[1]*1e6:<8.0f} {times[2]*1e6:<8.0f} {'✓' if ok else '✗'}")

    print(f"\n{'='*100}")
    print(f" ALL THREE METHODS AGREE ACROSS ALL TESTS: {'✓ YES' if all_ok else '✗ NO'}")
    print(f"{'='*100}")

    # ========================================
    # Timing benchmark (1000 evaluations)
    # ========================================
    print(f"\n--- Timing Benchmark (1000 evaluations each) ---")
    parts = make_kinematics_com(1.0, np.pi/3)
    p1, p2, p3, p4 = parts

    N = 1000
    t0 = time.perf_counter()
    for _ in range(N):
        parke_taylor_4pt(p1, p2, p3, p4)
    t_pt = (time.perf_counter() - t0) / N

    t0 = time.perf_counter()
    for _ in range(N):
        bcfw_4pt(p1, p2, p3, p4)
    t_bcfw = (time.perf_counter() - t0) / N

    t0 = time.perf_counter()
    for _ in range(N):
        grassmannian_4pt_mhv(p1, p2, p3, p4)
    t_grass = (time.perf_counter() - t0) / N

    print(f"  Parke-Taylor:  {t_pt*1e6:.1f} μs/eval")
    print(f"  BCFW:          {t_bcfw*1e6:.1f} μs/eval")
    print(f"  Grassmannian:  {t_grass*1e6:.1f} μs/eval")
    print(f"  Ratio BCFW/PT:  {t_bcfw/t_pt:.1f}x")
    print(f"  Ratio Grass/PT: {t_grass/t_pt:.1f}x")
