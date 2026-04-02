"""
Step 4: Analyze the bound H_actual ≤ H_formula.

Decompose C = H_formula - H_actual into:
1. Curvature bonus: (β/4) Σ□ |w|²(1 - cos(θ/2)) — always ≥ 0
2. Commutator term: (β/4) Σ□ L⃗·b⃗ — can be either sign

Key insight: The actual Hessian for a single plaquette has the form
-(β/2) d²/dt² Re Tr(U□) = (β/4)|w|² cos(θ/2) - (β/4) L⃗·b⃗

where cos(θ/2) = Re Tr(U)/2 ≤ 1.

For the bound H_actual ≤ H_formula = (β/4) Σ |w|², we need:
C = Σ□ [|w|²(1-cos(θ/2)) + L⃗·b⃗] ≥ 0  for all v.

Can we prove this per-plaquette? i.e., does
|w|²(1-cos(θ/2)) + L⃗·b⃗ ≥ 0 for each plaquette?

Or do we need cancellations across plaquettes?

Also: alternative approach — can we prove H_actual ≤ (β/4) Σ |w|² cos(θ/2)?
This would be: -L⃗·b⃗ ≤ 0, i.e., L⃗·b⃗ ≥ 0.
This is MUCH stronger and likely false per-plaquette.

Another approach: prove the bound directly as a MATRIX inequality, not per-plaquette.
"""

import numpy as np
from scipy.linalg import expm

np.random.seed(42)

sigma = [
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
]
T_gen = [1j * s / 2 for s in sigma]
I2 = np.eye(2, dtype=complex)

def su2_from_vec(v):
    return sum(vi * ti for vi, ti in zip(v, T_gen))

def su2_to_vec(X):
    return np.array([-2.0 * np.trace(t @ X).real for t in T_gen])

def Ad(Q, v_mat):
    return Q @ v_mat @ Q.conj().T

def re_tr(M):
    return np.trace(M).real

def random_SU2():
    return expm(sum(a * t for a, t in zip(np.random.randn(3), T_gen)))

L = 2
d = 4
Nsites = L**d
Nlinks = d * Nsites
Ndof = 3 * Nlinks

def site_index(x):
    idx = 0
    for i in range(d):
        idx = idx * L + (x[i] % L)
    return idx

def site_coords(idx):
    x = []
    for i in range(d):
        x.append(idx % L)
        idx //= L
    return list(reversed(x))

def link_index(x, mu):
    return mu * Nsites + site_index(x)

def neighbor(x, mu, direction=1):
    y = list(x)
    y[mu] = (y[mu] + direction) % L
    return y

Q = np.zeros((Nlinks, 2, 2), dtype=complex)
for i in range(Nlinks):
    Q[i] = random_SU2()

plaquettes = []
for s in range(Nsites):
    x = site_coords(s)
    for mu in range(d):
        for nu in range(mu+1, d):
            e1 = link_index(x, mu)
            e2 = link_index(neighbor(x, mu), nu)
            e3 = link_index(neighbor(x, nu), mu)
            e4 = link_index(x, nu)
            plaquettes.append((e1, e2, e3, e4))

beta = 1.0

# ============================================================
# Per-plaquette analysis
# ============================================================

print("=" * 70)
print("PER-PLAQUETTE ANALYSIS")
print("=" * 70)

print("\nFor each plaquette, check if |w|²(1-cos(θ/2)) + L⃗·b⃗ ≥ 0")
print("for random perturbation directions v.\n")

per_plaq_violations = 0
total_per_plaq_tests = 0

for plaq_idx, (e1, e2, e3, e4) in enumerate(plaquettes[:10]):  # first 10
    U = Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T
    a_val = re_tr(U) / 2
    b_mat = U - a_val * I2
    b_vec = su2_to_vec(b_mat)
    theta_half = np.arccos(np.clip(a_val, -1, 1))

    P2 = Q[e1].copy()
    P3 = Q[e1] @ Q[e2] @ Q[e3].conj().T

    edges = [e1, e2, e3, e4]
    signs = [1, 1, -1, -1]
    Ad_ops = [I2, P2, P3, U]

    violations_this = 0
    min_C = np.inf

    for trial in range(1000):
        # Random perturbation for the 4 edges of this plaquette
        v_vec = np.random.randn(12)  # 4 edges × 3 components

        ws = []
        w_vecs = []
        for k in range(4):
            v_e = su2_from_vec(v_vec[3*k:3*k+3])
            wk = signs[k] * Ad(Ad_ops[k], v_e)
            ws.append(wk)
            w_vecs.append(su2_to_vec(wk))

        w = ws[0] + ws[1] + ws[2] + ws[3]
        w_norm_sq = -2.0 * np.trace(w @ w).real

        # L⃗ = Σ_{i<j} w⃗ᵢ × w⃗ⱼ
        L_vec = np.zeros(3)
        for i in range(4):
            for j in range(i+1, 4):
                L_vec += np.cross(w_vecs[i], w_vecs[j])

        curv_bonus = w_norm_sq * (1 - a_val)  # |w|²(1 - cos(θ/2))
        comm_term = np.dot(L_vec, b_vec)        # L⃗·b⃗
        C_val = curv_bonus + comm_term

        if C_val < -1e-10:
            violations_this += 1
        min_C = min(min_C, C_val)
        total_per_plaq_tests += 1

    if violations_this > 0:
        per_plaq_violations += violations_this
        print(f"  Plaq {plaq_idx}: θ/2={theta_half:.3f}, VIOLATIONS={violations_this}/1000, "
              f"min C = {min_C:.6f}")
    else:
        print(f"  Plaq {plaq_idx}: θ/2={theta_half:.3f}, OK (min C = {min_C:.6f})")

print(f"\nTotal per-plaquette violations: {per_plaq_violations}/{total_per_plaq_tests}")

# ============================================================
# Can the per-plaquette quantity be negative?
# Maximize -C / |v|² over perturbation directions
# ============================================================

print("\n\n" + "=" * 70)
print("ADVERSARIAL PER-PLAQUETTE SEARCH")
print("=" * 70)

print("\nFor each plaquette, maximize -(C_value) / |v|² by gradient ascent.\n")

worst_ratio = -np.inf

for plaq_idx, (e1, e2, e3, e4) in enumerate(plaquettes):
    U = Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T
    a_val = re_tr(U) / 2
    b_mat = U - a_val * I2
    b_vec = su2_to_vec(b_mat)

    P2 = Q[e1].copy()
    P3 = Q[e1] @ Q[e2] @ Q[e3].conj().T

    edges = [e1, e2, e3, e4]
    signs_arr = [1, 1, -1, -1]
    Ad_ops = [I2, P2, P3, U]

    # Precompute the Ad-rotated generators (3×12 matrix)
    # Each column wₖₐ is a 3-vector
    W_matrix = np.zeros((3, 12))
    for k in range(4):
        for c in range(3):
            wkc = signs_arr[k] * Ad(Ad_ops[k], T_gen[c])
            W_matrix[:, 3*k+c] = su2_to_vec(wkc)

    def compute_C_value(v12):
        """Compute C = |w|²(1-cos(θ/2)) + L⃗·b⃗ for a 12-vector v."""
        # w = W_matrix @ v12 (3-vector)
        w_vec = W_matrix @ v12
        w_norm_sq = np.dot(w_vec, w_vec)

        # Compute L⃗ from the 4 individual w-vectors
        ws = [W_matrix[:, 3*k:3*k+3] @ v12[3*k:3*k+3] for k in range(4)]
        L_vec = np.zeros(3)
        for i in range(4):
            for j in range(i+1, 4):
                L_vec += np.cross(ws[i], ws[j])

        curv_bonus = w_norm_sq * (1 - a_val)
        comm_term = np.dot(L_vec, b_vec)
        return curv_bonus + comm_term

    # Try many random directions
    min_C_normed = np.inf
    for _ in range(50):
        v = np.random.randn(12)
        v /= np.linalg.norm(v)
        C_val = compute_C_value(v)
        if C_val < min_C_normed:
            min_C_normed = C_val

    if min_C_normed < 0:
        ratio = -min_C_normed
        if ratio > worst_ratio:
            worst_ratio = ratio

if worst_ratio > 0:
    print(f"\n  PER-PLAQUETTE BOUND FAILS: worst C/|v|² = {-worst_ratio:.6f}")
else:
    print(f"\n  Per-plaquette bound HOLDS for all 96 plaquettes")

# ============================================================
# Now check the FULL (summed over plaquettes) bound
# ============================================================

print("\n\n" + "=" * 70)
print("FULL LATTICE BOUND ANALYSIS")
print("=" * 70)

def build_C_matrix():
    """Build C = H_formula - H_actual (192×192)."""
    H_form = np.zeros((Ndof, Ndof))
    H_act = np.zeros((Ndof, Ndof))

    for (e1, e2, e3, e4) in plaquettes:
        U = Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T
        P2 = Q[e1].copy()
        P3 = Q[e1] @ Q[e2] @ Q[e3].conj().T
        a_val = re_tr(U) / 2

        edges = [e1, e2, e3, e4]
        signs_arr = [1, 1, -1, -1]
        Ad_ops = [I2, P2, P3, U]

        wka = np.zeros((4, 3, 2, 2), dtype=complex)
        for k in range(4):
            for a in range(3):
                wka[k, a] = signs_arr[k] * Ad(Ad_ops[k], T_gen[a])

        # B² formula
        B_cols = np.zeros((3, 12))
        for k in range(4):
            for c in range(3):
                B_cols[:, 3*k+c] = su2_to_vec(wka[k, c])

        block_form = (beta / 4) * B_cols.T @ B_cols

        for i_loc in range(12):
            ki, ai = divmod(i_loc, 3)
            ig = 3 * edges[ki] + ai
            for j_loc in range(12):
                kj, aj = divmod(j_loc, 3)
                jg = 3 * edges[kj] + aj
                H_form[ig, jg] += block_form[i_loc, j_loc]

        # Actual Hessian
        for k in range(4):
            for a in range(3):
                ig = 3 * edges[k] + a
                for l in range(4):
                    for b in range(3):
                        jg = 3 * edges[l] + b
                        if k == l:
                            val = 0.5 * (re_tr(wka[k,a] @ wka[k,b] @ U) +
                                         re_tr(wka[k,b] @ wka[k,a] @ U))
                        elif k < l:
                            val = re_tr(wka[k,a] @ wka[l,b] @ U)
                        else:
                            val = re_tr(wka[l,b] @ wka[k,a] @ U)
                        H_act[ig, jg] += -(beta / 2) * val

    return H_form, H_act

H_form, H_act = build_C_matrix()
C_mat = H_form - H_act

# Eigenvalues of C
eig_C = np.sort(np.linalg.eigvalsh(C_mat))
print(f"\nSpectrum of C = H_formula - H_actual:")
print(f"  Min eigenvalue: {eig_C[0]:.8f}")
print(f"  Max eigenvalue: {eig_C[-1]:.8f}")
print(f"  # negative: {np.sum(eig_C < -1e-10)}")
print(f"  # positive: {np.sum(eig_C > 1e-10)}")
print(f"  # zero: {np.sum(np.abs(eig_C) < 1e-10)}")

if eig_C[0] >= -1e-10:
    print(f"\n  C IS PSD: The inequality H_actual ≤ H_formula holds as a MATRIX inequality!")
else:
    print(f"\n  C is NOT PSD (has {np.sum(eig_C < -1e-10)} negative eigenvalues)")
    print(f"  But λ_max(H_actual) ≤ λ_max(H_formula) still holds because the")
    print(f"  negative eigenspace of C is not aligned with the top eigenspace of H_actual.")

# ============================================================
# Decompose C into curvature and commutator parts
# ============================================================

print("\n\n" + "=" * 70)
print("DECOMPOSITION OF C = C_curv + C_comm")
print("=" * 70)

def build_C_decomposed():
    """Build C_curv and C_comm separately."""
    C_curv = np.zeros((Ndof, Ndof))
    C_comm = np.zeros((Ndof, Ndof))

    for (e1, e2, e3, e4) in plaquettes:
        U = Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T
        P2 = Q[e1].copy()
        P3 = Q[e1] @ Q[e2] @ Q[e3].conj().T
        a_val = re_tr(U) / 2
        b_mat = U - a_val * I2
        b_vec = su2_to_vec(b_mat)

        edges = [e1, e2, e3, e4]
        signs_arr = [1, 1, -1, -1]
        Ad_ops = [I2, P2, P3, U]

        wka = np.zeros((4, 3, 2, 2), dtype=complex)
        wka_vec = np.zeros((4, 3, 3))
        for k in range(4):
            for a in range(3):
                wka[k, a] = signs_arr[k] * Ad(Ad_ops[k], T_gen[a])
                wka_vec[k, a] = su2_to_vec(wka[k, a])

        # C_curv = (β/4) Σ |w|²(1-cos(θ/2))
        # This comes from H_formula - H_w2 where H_w2 is the w²·cos(θ/2) part.
        # H_formula_{ij} = (β/4) Σ⟨∂w/∂vᵢ, ∂w/∂vⱼ⟩
        # H_w2_{ij} = (β/4) cos(θ/2) Σ⟨∂w/∂vᵢ, ∂w/∂vⱼ⟩
        # C_curv_{ij} = (β/4)(1-cos(θ/2)) Σ⟨∂w/∂vᵢ, ∂w/∂vⱼ⟩

        # For this plaquette:
        # ⟨∂w/∂v_{eₖ,a}, ∂w/∂v_{eₗ,b}⟩ = ⟨wₖₐ, wₗᵦ⟩ = -2 Tr(wₖₐ wₗᵦ)
        # But this is the INNER PRODUCT, not the ordered product.
        # For the B² formula: H_form contribution = (β/4) Σ⟨wₖₐ, wₗᵦ⟩
        #                                         = (β/4) w⃗ₖₐ · w⃗ₗᵦ

        B_cols = np.zeros((3, 12))
        for k in range(4):
            for c in range(3):
                B_cols[:, 3*k+c] = wka_vec[k, c]

        BtB = B_cols.T @ B_cols  # 12×12, (BtB)_{ij} = ⟨wᵢ, wⱼ⟩

        # C_curv contribution from this plaquette
        block_curv = (beta / 4) * (1 - a_val) * BtB

        for i_loc in range(12):
            ki, ai = divmod(i_loc, 3)
            ig = 3 * edges[ki] + ai
            for j_loc in range(12):
                kj, aj = divmod(j_loc, 3)
                jg = 3 * edges[kj] + aj
                C_curv[ig, jg] += block_curv[i_loc, j_loc]

        # C_comm contribution: from the commutator terms
        # The commutator part of H_actual is:
        # H_comm_{ij} = -(β/2) × [commutator contribution to d²Re Tr]
        #
        # From the expansion: for k<l, the commutator gives Re Tr([wₖₐ,wₗᵦ]U)
        # and the w² gives Re Tr((wₖₐwₗᵦ + wₗᵦwₖₐ)U)/2 (anticommutator×U + comm×U)
        #
        # Actually, let me think about this differently.
        # H_actual = H_w2 + H_comm where:
        # H_w2(v,v) = (β/4) cos(θ/2) |w|² (= (β/4) cos(θ/2) BᵀB)
        # H_comm(v,v) = -(β/4) L⃗·b⃗
        # C = H_form - H_actual = (H_form - H_w2) + (-H_comm) = C_curv + (-H_comm)
        #
        # So C_comm = -H_comm = (β/4) L⃗·b⃗ contribution to the bilinear form.
        #
        # For the MATRIX form of H_comm:
        # H_comm(v,v) = -(β/4) Σ_{i<j} (w⃗ᵢ × w⃗ⱼ) · b⃗ (summed over plaquette positions)
        # But wᵢ depends linearly on v, so this is a bilinear form.
        #
        # L⃗ = Σ_{k<l} (Σₐ v_{eₖ,a} w⃗ₖₐ) × (Σᵦ v_{eₗ,b} w⃗ₗᵦ)
        #    = Σ_{k<l} Σₐᵦ v_{eₖ,a} v_{eₗ,b} (w⃗ₖₐ × w⃗ₗᵦ)
        #
        # So L⃗·b⃗ = Σ_{k<l} Σₐᵦ v_{eₖ,a} v_{eₗ,b} (w⃗ₖₐ × w⃗ₗᵦ)·b⃗
        #
        # This means: H_comm matrix element for (eₖ,a),(eₗ,b) with k<l is:
        # -(β/4) × (w⃗ₖₐ × w⃗ₗᵦ)·b⃗

        # Build C_comm as a matrix
        for k in range(4):
            for a in range(3):
                ig = 3 * edges[k] + a
                for l in range(4):
                    for b in range(3):
                        jg = 3 * edges[l] + b
                        if k < l:
                            cross = np.cross(wka_vec[k, a], wka_vec[l, b])
                            val = np.dot(cross, b_vec)
                            # C_comm = -H_comm, and H_comm_{ij} = -(β/4)(w⃗ₖₐ×w⃗ₗᵦ)·b⃗
                            # So C_comm_{ij} = (β/4)(w⃗ₖₐ×w⃗ₗᵦ)·b⃗
                            C_comm[ig, jg] += (beta / 4) * val
                            C_comm[jg, ig] += (beta / 4) * val  # symmetrize for k>l

    return C_curv, C_comm

C_curv, C_comm = build_C_decomposed()

eig_curv = np.sort(np.linalg.eigvalsh(C_curv))
eig_comm = np.sort(np.linalg.eigvalsh(C_comm))

print(f"\nC_curv (curvature bonus):")
print(f"  Min eigenvalue: {eig_curv[0]:.8f}")
print(f"  Max eigenvalue: {eig_curv[-1]:.8f}")
print(f"  Is PSD? {eig_curv[0] >= -1e-10}")

print(f"\nC_comm (commutator):")
print(f"  Min eigenvalue: {eig_comm[0]:.8f}")
print(f"  Max eigenvalue: {eig_comm[-1]:.8f}")
print(f"  Is PSD? {eig_comm[0] >= -1e-10}")

# Check: C = C_curv + C_comm?
C_sum = C_curv + C_comm
print(f"\n|C - (C_curv + C_comm)| = {np.max(np.abs(C_mat - C_sum)):.2e}")

# ============================================================
# Key question: Does C_curv dominate C_comm's negative part?
# ============================================================

print("\n\n" + "=" * 70)
print("SPECTRAL DOMINANCE ANALYSIS")
print("=" * 70)

# Find the most negative direction of C_comm
eig_comm_vals, eig_comm_vecs = np.linalg.eigh(C_comm)
v_worst = eig_comm_vecs[:, 0]  # most negative eigenvector

# Evaluate C_curv and C_comm in this direction
c_curv_at_worst = v_worst @ C_curv @ v_worst
c_comm_at_worst = v_worst @ C_comm @ v_worst  # = eig_comm[0]
c_total_at_worst = v_worst @ C_mat @ v_worst

print(f"\nAt the most negative C_comm direction:")
print(f"  C_curv(v,v) = {c_curv_at_worst:.8f}")
print(f"  C_comm(v,v) = {c_comm_at_worst:.8f}")
print(f"  C_total(v,v) = {c_total_at_worst:.8f}")
print(f"  Ratio C_curv/|C_comm| = {c_curv_at_worst / abs(c_comm_at_worst):.4f}")

if c_total_at_worst >= -1e-10:
    print("  C_curv DOES compensate: C ≥ 0 even in worst C_comm direction!")
else:
    print("  C_curv does NOT compensate in this direction.")

# ============================================================
# Systematic check: ratio C_curv / |C_comm| for random directions
# ============================================================

print("\n\nRatio analysis: C_curv(v,v) / |C_comm(v,v)| for 1000 random v:")

ratios = []
n_neg_C = 0
for _ in range(1000):
    v = np.random.randn(Ndof)
    v /= np.linalg.norm(v)
    cc = v @ C_curv @ v
    cm = v @ C_comm @ v
    ct = v @ C_mat @ v
    if cm < -1e-10:
        ratios.append(cc / abs(cm))
    if ct < -1e-10:
        n_neg_C += 1

if ratios:
    ratios = np.array(ratios)
    print(f"  (only when C_comm < 0: {len(ratios)} cases)")
    print(f"  Min ratio: {ratios.min():.6f}")
    print(f"  Mean ratio: {ratios.mean():.6f}")
    print(f"  Max ratio: {ratios.max():.6f}")
    print(f"  All ratios > 1? {(ratios > 1.0 - 1e-6).all()}")
else:
    print("  C_comm is never negative!")

print(f"\n  C_total < 0 for {n_neg_C}/1000 random directions")

# ============================================================
# Check multiple configurations
# ============================================================

print("\n\n" + "=" * 70)
print("MULTI-CONFIGURATION ANALYSIS")
print("=" * 70)

configs_tested = 0
total_violations = 0

for config_trial in range(20):
    # Generate new random config
    for i in range(Nlinks):
        Q[i] = random_SU2()

    # Rebuild the lists
    H_form_local = np.zeros((Ndof, Ndof))
    H_act_local = np.zeros((Ndof, Ndof))

    for (e1, e2, e3, e4) in plaquettes:
        U = Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T
        P2 = Q[e1].copy()
        P3 = Q[e1] @ Q[e2] @ Q[e3].conj().T
        a_val = re_tr(U) / 2

        edges = [e1, e2, e3, e4]
        signs_arr = [1, 1, -1, -1]
        Ad_ops = [I2, P2, P3, U]

        wka = np.zeros((4, 3, 2, 2), dtype=complex)
        for k in range(4):
            for a_idx in range(3):
                wka[k, a_idx] = signs_arr[k] * Ad(Ad_ops[k], T_gen[a_idx])

        B_cols = np.zeros((3, 12))
        for k in range(4):
            for c in range(3):
                B_cols[:, 3*k+c] = su2_to_vec(wka[k, c])

        block_form = (beta / 4) * B_cols.T @ B_cols
        for i_loc in range(12):
            ki, ai = divmod(i_loc, 3)
            ig = 3 * edges[ki] + ai
            for j_loc in range(12):
                kj, aj = divmod(j_loc, 3)
                jg = 3 * edges[kj] + aj
                H_form_local[ig, jg] += block_form[i_loc, j_loc]

        for k in range(4):
            for a_idx in range(3):
                ig = 3 * edges[k] + a_idx
                for l in range(4):
                    for b_idx in range(3):
                        jg = 3 * edges[l] + b_idx
                        if k == l:
                            val = 0.5 * (re_tr(wka[k,a_idx] @ wka[k,b_idx] @ U) +
                                         re_tr(wka[k,b_idx] @ wka[k,a_idx] @ U))
                        elif k < l:
                            val = re_tr(wka[k,a_idx] @ wka[l,b_idx] @ U)
                        else:
                            val = re_tr(wka[l,b_idx] @ wka[k,a_idx] @ U)
                        H_act_local[ig, jg] += -(beta / 2) * val

    eig_act = np.sort(np.linalg.eigvalsh(H_act_local))[::-1]
    eig_form = np.sort(np.linalg.eigvalsh(H_form_local))[::-1]

    C_local = H_form_local - H_act_local
    eig_C_local = np.sort(np.linalg.eigvalsh(C_local))

    violation = eig_act[0] > eig_form[0] + 1e-8
    configs_tested += 1
    if violation:
        total_violations += 1

    ratio = eig_act[0] / eig_form[0]
    min_C_eig = eig_C_local[0]
    n_neg_C_eig = np.sum(eig_C_local < -1e-10)

    print(f"  Config {config_trial+1}: λ_max ratio = {ratio:.4f}, "
          f"C min eig = {min_C_eig:.4f}, "
          f"C neg eigs = {n_neg_C_eig}, "
          f"violation = {violation}")

print(f"\n  Total violations: {total_violations}/{configs_tested}")

print("\nDone.")
