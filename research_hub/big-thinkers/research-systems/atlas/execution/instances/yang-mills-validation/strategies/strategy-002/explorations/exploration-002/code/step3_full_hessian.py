"""
Step 3: Build the full 192×192 Hessian for L=2, d=4 lattice.

Compare:
1. H_actual (finite differences)
2. H_analytical (our formula: w² + commutator terms)
3. H_formula (B² formula: (β/4) Σ |w|²)
4. H_w2only (w² terms only, no commutator)

Lattice: L=2, d=4, periodic boundary conditions.
Links: 4 directions × 2⁴ sites = 64 links.
Each link has 3 su(2) components.
Total DOF: 192.

Plaquettes: (d choose 2) × L^d = 6 × 16 = 96 plaquettes.
"""

import numpy as np
from scipy.linalg import expm

np.random.seed(42)

# ============================================================
# SU(2) utilities
# ============================================================

sigma = [
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
]
T_gen = [1j * s / 2 for s in sigma]
I2 = np.eye(2, dtype=complex)

def random_su2_vec():
    return np.random.randn(3)

def random_SU2():
    alpha = np.random.randn(3)
    X = sum(a * t for a, t in zip(alpha, T_gen))
    return expm(X)

def su2_from_vec(v):
    return sum(vi * ti for vi, ti in zip(v, T_gen))

def su2_to_vec(X):
    return np.array([-2.0 * np.trace(t @ X).real for t in T_gen])

def Ad(Q, v_mat):
    return Q @ v_mat @ Q.conj().T

def Ad_vec(Q, v):
    """Ad_Q(v) in vector form."""
    v_mat = su2_from_vec(v)
    result_mat = Q @ v_mat @ Q.conj().T
    return su2_to_vec(result_mat)

def re_tr(M):
    return np.trace(M).real

# ============================================================
# Lattice setup: L=2, d=4, periodic BC
# ============================================================

L = 2
d = 4
Nsites = L**d  # 16
Nlinks = d * Nsites  # 64
Ndof = 3 * Nlinks  # 192

def site_index(x):
    """Convert d-dimensional coordinate (mod L) to linear index."""
    idx = 0
    for i in range(d):
        idx = idx * L + (x[i] % L)
    return idx

def site_coords(idx):
    """Convert linear index to d-dimensional coordinate."""
    x = []
    for i in range(d):
        x.append(idx % L)
        idx //= L
    return list(reversed(x))

def link_index(x, mu):
    """Index of the link at site x in direction mu."""
    return mu * Nsites + site_index(x)

def neighbor(x, mu, direction=1):
    """Neighbor of x in direction mu (forward if direction=1, backward if -1)."""
    y = list(x)
    y[mu] = (y[mu] + direction) % L
    return y

# Generate random configuration
Q = np.zeros((Nlinks, 2, 2), dtype=complex)
for i in range(Nlinks):
    Q[i] = random_SU2()

# ============================================================
# Enumerate plaquettes
# Each plaquette is (site, mu, nu) with mu < nu
# Edges: e1 = (x, mu), e2 = (x+mu, nu), e3 = (x+nu, mu), e4 = (x, nu)
# U□ = Q_{e1} Q_{e2} Q_{e3}^{-1} Q_{e4}^{-1}
# ============================================================

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

Nplaq = len(plaquettes)
print(f"Lattice: L={L}, d={d}")
print(f"Sites: {Nsites}, Links: {Nlinks}, DOF: {Ndof}, Plaquettes: {Nplaq}")

def compute_plaquette_holonomy(e1, e2, e3, e4):
    """U□ = Q_{e1} Q_{e2} Q_{e3}^{-1} Q_{e4}^{-1}"""
    return Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T

# ============================================================
# Wilson action
# ============================================================

beta = 1.0

def wilson_action():
    """S = -(β/2) Σ□ Re Tr(U□)"""
    S = 0.0
    for (e1, e2, e3, e4) in plaquettes:
        U = compute_plaquette_holonomy(e1, e2, e3, e4)
        S -= (beta / 2) * re_tr(U)
    return S

# ============================================================
# Method 1: Finite-difference Hessian
# ============================================================

def perturb_link(link_idx, component, epsilon):
    """Perturb Q[link_idx] → exp(ε T_a) Q[link_idx]"""
    old = Q[link_idx].copy()
    Q[link_idx] = expm(epsilon * T_gen[component]) @ old
    return old

def restore_link(link_idx, old_val):
    Q[link_idx] = old_val

def build_hessian_fd(h=1e-4):
    """Build full Hessian by central finite differences."""
    H = np.zeros((Ndof, Ndof))
    S0 = wilson_action()

    for i in range(Ndof):
        li, ci = divmod(i, 3)  # link index, component
        # Diagonal: (S(+h) - 2S(0) + S(-h)) / h²
        old = perturb_link(li, ci, h)
        Sp = wilson_action()
        restore_link(li, old)

        old = perturb_link(li, ci, -h)
        Sm = wilson_action()
        restore_link(li, old)

        H[i, i] = (Sp - 2 * S0 + Sm) / h**2

    # Off-diagonal (only upper triangle, then symmetrize)
    for i in range(Ndof):
        li, ci = divmod(i, 3)
        for j in range(i+1, Ndof):
            lj, cj = divmod(j, 3)
            # (S(+h,+h) - S(+h,-h) - S(-h,+h) + S(-h,-h)) / (4h²)
            old_i = perturb_link(li, ci, h)
            old_j = perturb_link(lj, cj, h)
            Spp = wilson_action()
            restore_link(lj, old_j)
            old_j = perturb_link(lj, cj, -h)
            Spm = wilson_action()
            restore_link(lj, old_j)
            restore_link(li, old_i)

            old_i = perturb_link(li, ci, -h)
            old_j = perturb_link(lj, cj, h)
            Smp = wilson_action()
            restore_link(lj, old_j)
            old_j = perturb_link(lj, cj, -h)
            Smm = wilson_action()
            restore_link(lj, old_j)
            restore_link(li, old_i)

            H[i, j] = (Spp - Spm - Smp + Smm) / (4 * h**2)
            H[j, i] = H[i, j]

    return H

# ============================================================
# Method 2: Analytical Hessian from our formula
# ============================================================

def build_hessian_analytical():
    """
    H_actual(i,j) = -(β/2) Σ□ d²/dt_i dt_j Re Tr(U□)

    For each plaquette, perturbation of link eₖ in component a
    contributes to d²/dt_i dt_j.

    We compute the full bilinear form.
    """
    H = np.zeros((Ndof, Ndof))

    for (e1, e2, e3, e4) in plaquettes:
        U = compute_plaquette_holonomy(e1, e2, e3, e4)
        a_scalar = re_tr(U) / 2  # cos(θ/2)
        b_mat = U - a_scalar * I2
        b_vec = su2_to_vec(b_mat)

        # Partial holonomies
        P2 = Q[e1].copy()
        P3 = Q[e1] @ Q[e2] @ Q[e3].conj().T

        # Signs and Ad operators for each edge
        # w₁ = v₁ (identity Ad)
        # w₂ = Ad_{Q₁}(v₂)
        # w₃ = -Ad_{P₃}(v₃)
        # w₄ = -Ad_{U}(v₄)

        edges = [e1, e2, e3, e4]
        signs = [1, 1, -1, -1]
        Ad_mats = [I2, P2, P3, U]  # Q for the Ad action

        # For each pair of DOFs (i, j) in this plaquette:
        # d²/(dv_i dv_j) Re Tr(U□) = contribution from w² and commutator

        # Build 12×12 block (4 edges × 3 components each)
        # Then scatter into the full 192×192 matrix

        # For a general bilinear form, we need:
        # d²/(dα_i dα_j) [Re Tr(w²U) + Σ_{k<l} Re Tr([wₖ,wₗ]U)]
        # where α_i parametrize the perturbations

        # The w² U term: Re Tr(w²U) where w = Σ sₖ Ad_{Pₖ}(v_{eₖ})
        # d²/dα_i dα_j Re Tr(w²U) where w depends linearly on all α:
        #   = Re Tr((∂w/∂α_i)(∂w/∂α_j) U + (∂w/∂α_j)(∂w/∂α_i) U)
        # Wait no. w²U is quadratic in w, and w is linear in α.
        # d²/dα² Re Tr(w²U) = 2 Re Tr(w_i w_j U)... hmm let me think.

        # Actually, for the bilinear form H(v,v), we compute
        # d²/dt² with v = (v_{e1}, ..., v_{e4}) fixed.
        # But for the MATRIX, we need to take second mixed partials.

        # For the second derivative d²/dα_i dα_j where α_i is the
        # a-th component of link e, we need the (i,j) entry of the
        # Hessian matrix.

        # From our formula:
        # f(t) = Re Tr([∏ exp(t s_k Ad_{P_k}(v_k))] U)
        # d²f/dt² = Re Tr(w²U) + Σ_{k<l} Re Tr([w_k,w_l]U)

        # For the matrix element, we perturb link e in direction T_a
        # (component a) and link f in direction T_b.
        # The second derivative is the (3*e+a, 3*f+b) entry.

        # If both perturbations are on the same plaquette:
        # There are at most 4 links per plaquette.

        # For each edge k of the plaquette, the contribution to w is:
        # w += s_k * Ad_{P_k}(v_{e_k})
        # If we perturb link e_k in direction T_a, then:
        # ∂w/∂α_{k,a} = s_k * Ad_{P_k}(T_a)

        # So ∂w/∂α_{k,a} is a specific su(2) element.

        # The w² contribution to d²f:
        # Re Tr((∂w/∂α_i · ∂w/∂α_j + ∂w/∂α_j · ∂w/∂α_i) U) / 2
        # NO! The second derivative of Re Tr(w²U) where w = Σ cₖ wₖ
        # and we differentiate w.r.t. c_i and c_j is:
        # Re Tr((w_i w_j + w_j w_i) U)

        # Wait, let me redo this properly. We have a quadratic form
        # Q(t) = Re Tr(W(t)²U) where W(t) = Σ t_k w_k.
        # d²Q/dt_i dt_j = Re Tr((w_i w_j + w_j w_i) U)
        #                = 2 Re Tr(w_i w_j U) (if U commutes, no...)
        # Actually Re Tr((w_i w_j + w_j w_i) U) is the answer.

        # For the commutator term: Σ_{k<l} Re Tr([w_k, w_l] U)
        # where w_k = t_k * (specific su2 element)
        # d²/dt_i dt_j of t_k t_l Re Tr([w_k/t_k, w_l/t_l] U)?
        # No, the commutator arises from the product of exponentials.

        # Let me think about this differently. The full second-order
        # expansion is:
        # Re Tr(U□(t)) = Re Tr(U) + t · Re Tr(wU) +
        #   t²/2 · [Re Tr(w²U) + Σ_{k<l} Re Tr([w_k,w_l]U)] + O(t³)

        # But this is for a one-parameter perturbation with w = Σ s_k Ad(v_k).

        # For the Hessian MATRIX, I need to consider independent
        # perturbation parameters for each link-component.
        # Let me write U□(t) where t = (t_{e,a}) for each link e, comp a.

        # Q_e → exp(Σ_a t_{e,a} T_a) Q_e for each e

        # For the plaquette, only edges e₁,...,e₄ matter.
        # U□(t) = exp(Σ_a t₁ₐ T_a) Q₁ · exp(Σ_a t₂ₐ T_a) Q₂ ·
        #          Q₃⁻¹ exp(-Σ_a t₃ₐ T_a) · Q₄⁻¹ exp(-Σ_a t₄ₐ T_a)

        # Following the same push-to-left procedure:
        # = exp(Σ t₁ₐ w¹ₐ) exp(Σ t₂ₐ w²ₐ) exp(Σ t₃ₐ w³ₐ) exp(Σ t₄ₐ w⁴ₐ) · U

        # where wᵏₐ = sₖ Ad_{Pₖ}(Tₐ) are the rotated generators.

        # OK so w¹ₐ = T_a for edge 1 (s=+1, P₁=I)
        #    w²ₐ = Ad_{Q₁}(T_a)
        #    w³ₐ = -Ad_{P₃}(T_a)
        #    w⁴ₐ = -Ad_{U}(T_a)

        # Now, the product of exponentials to second order:
        # ∏ₖ exp(Σₐ tₖₐ wₖₐ)
        # = I + Σ_{k,a} tₖₐ wₖₐ + (1/2)[Σ_{k,a} tₖₐ wₖₐ]² +
        #   (1/2) Σ_{k<l} [Σₐ tₖₐ wₖₐ, Σᵦ tₗᵦ wₗᵦ] + O(t³)

        # The t² terms in Re Tr(... U):
        # d²/dt_{ka} dt_{lb} Re Tr(U□) = Re Tr(wₖₐ wₗᵦ U + wₗᵦ wₖₐ U) / ... hmm

        # Actually, the second-order coefficient is:
        # (1/2) w² + (1/2) Σ_{k<l} [wₖ, wₗ]
        # where w = Σ tₖₐ wₖₐ.

        # So Re Tr(U□(t)) = Re Tr(U) + Σ tₖₐ Re Tr(wₖₐ U) +
        #   (1/2) Σ_{k,a,l,b} tₖₐ tₗᵦ Re Tr(wₖₐ wₗᵦ U) +
        #   (1/2) Σ_{k<l} Σ_{a,b} tₖₐ tₗᵦ Re Tr([wₖₐ, wₗᵦ] U)

        # Wait, I need to be more careful. The w² + commutator decomposition:

        # The t² coefficient in ∏ exp(Σₐ tₖₐ wₖₐ) is:
        # Σ_{k,a} tₖₐ² wₖₐ²/2 + Σ_{(k,a)<(l,b)} tₖₐ tₗᵦ wₖₐ wₗᵦ
        #
        # where the ordering is first by k, then by a within k.
        # But the wₖₐ for the same k are in the SAME exponential:
        # exp(Σₐ tₖₐ wₖₐ) = exp(tₖ · wₖ) where tₖ = (tₖ₁,tₖ₂,tₖ₃)
        # and wₖ = Σₐ tₖₐ wₖₐ.

        # Hmm, this is getting messy. Let me just compute it directly.

        # The 12 "generators" for this plaquette are:
        # wₖₐ = sₖ Ad_{Pₖ}(Tₐ) for k=1..4, a=1..3
        # where sₖ = (+1, +1, -1, -1) and Pₖ are partial holonomies.

        # The second derivative d²/dt_{ka} dt_{lb} Re Tr(U□) needs to
        # account for the ordering of exponentials.

        # For same-link (k = l): both perturbations are in the SAME exponential.
        # exp(Σ tₖₐ wₖₐ) - the second-order term is (Σ tₖₐ wₖₐ)²/2
        # which gives d²/dtₖₐ dtₖᵦ = Re Tr((wₖₐ wₖᵦ + wₖᵦ wₖₐ)/2 · [rest] · U)

        # Hmm, but the "rest" is the product of OTHER exponentials.
        # At t=0, those are all I. So:
        # d²/dtₖₐ dtₖᵦ Re Tr(U□)|_{t=0} = Re Tr(wₖₐ wₖᵦ U) + Re Tr(wₖᵦ wₖₐ U)
        #   ... no, the second-order coefficient of exp is X²/2, so
        # d²/dtₖₐ dtₖᵦ [Tr(exp(·)U)] = Tr(wₖₐ wₖᵦ U) if a≠b (from the cross terms)
        # ... plus higher-order corrections from the BCH.

        # Actually wait. Let me reconsider. For the FULL product of 4 exponentials
        # at t=0, the second-order Taylor expansion gives us the formula we verified.

        # For the Hessian MATRIX element H_{(e,a),(f,b)}:
        # If e=f (same link): only one exponential is involved.
        #   wₖ = sₖ (t_a T_a + t_b T_b + ...) (for the link that matches e=f)
        #   d²/dt_a dt_b [Re Tr(wₖ²/2 · U)] = Re Tr(wₖₐ wₖᵦ · U)
        #   where wₖₐ = sₖ Ad_{Pₖ}(T_a), wₖᵦ = sₖ Ad_{Pₖ}(T_b)
        #   The commutator contribution is zero (same exponential).

        # If e≠f (different links in same plaquette):
        #   The w² contribution: for w = Σ sₖ Ad tₖₐ wₖₐ,
        #   d²/dt_{ka} dt_{lb} |w|²/something...
        #   The commutator contribution: [wₖₐ, wₗᵦ] (for k<l).

        # OK I think the cleanest approach is:
        # d²/dt_{ka} dt_{lb} Re Tr(U□)|_{t=0}
        # = Re Tr(wₖₐ wₗᵦ U) + Re Tr(wₗᵦ wₖₐ U)  [from w² expansion]
        #     (factor: 1 for k=l, 1 for k≠l)
        # + Re Tr([wₖₐ, wₗᵦ] U) · sgn(k - l)
        #     (factor: +1 if k<l, -1 if k>l, 0 if k=l)
        #     NO, this isn't right either.

        # Let me think step by step. The product ∏ exp(εₖ) where
        # εₖ = Σₐ tₖₐ wₖₐ. At second order:
        #
        # ∏ exp(εₖ) = I + Σₖ εₖ + Σₖ εₖ²/2 + Σ_{k<l} εₖ εₗ + O(ε³)
        #
        # The t²-coefficient matrix is:
        # Σₖ (Σₐ tₖₐ wₖₐ)²/2 + Σ_{k<l} (Σₐ tₖₐ wₖₐ)(Σᵦ tₗᵦ wₗᵦ)
        #
        # = (1/2) Σₖ Σₐᵦ tₖₐ tₖᵦ wₖₐ wₖᵦ + Σ_{k<l} Σₐᵦ tₖₐ tₗᵦ wₖₐ wₗᵦ
        #
        # So d²/dtₖₐ dtₗᵦ = Re Tr([coefficient] U) where coefficient is:
        #   k=l: wₖₐ wₖᵦ (from the εₖ²/2 term, factor 2 from d²/dt² gives 1)
        #
        #   Wait: d²/dtₖₐ dtₖᵦ of (1/2) tₖₐ tₖᵦ wₖₐ wₖᵦ (no sum on repeated indices)
        #   If a≠b: (1/2)(wₖₐ wₖᵦ + wₖᵦ wₖₐ) (from both orderings in the sum)
        #   If a=b: wₖₐ² (from the single term)

        # Hmm wait, (Σₐ tₖₐ wₖₐ)² = Σₐᵦ tₖₐ tₖᵦ wₖₐ wₖᵦ
        # d²/dtₖₐ dtₖᵦ [(1/2)Σ_{a',b'} tₖₐ' tₖᵦ' wₖₐ' wₖᵦ']
        # = (1/2)(wₖₐ wₖᵦ + wₖᵦ wₖₐ) if a≠b (from a'=a,b'=b and a'=b,b'=a)
        # = wₖₐ wₖₐ if a=b (from a'=a,b'=a, factor 2 from d²/dt²×1/2)
        # Wait no: d²/dtₖₐ² [(1/2)(tₖₐ)² wₖₐ²] = wₖₐ². And there might be
        # cross terms from (1/2) 2 tₖₐ tₖᵦ wₖₐ wₖᵦ for a≠b.
        # d²/dtₖₐ dtₖᵦ [(1/2)Σ tₖₐ' tₖᵦ' wₖₐ' wₖᵦ']
        # The terms that survive: a'=a,b'=b gives wₖₐ wₖᵦ
        #                         a'=b,b'=a gives wₖᵦ wₖₐ
        # So: (1/2)(wₖₐ wₖᵦ + wₖᵦ wₖₐ) for all a,b (including a=b, giving wₖₐ²)

        # For k<l:
        # d²/dtₖₐ dtₗᵦ [Σ_{k'<l'} (Σₐ' tₖ'ₐ' wₖ'ₐ')(Σᵦ' tₗ'ᵦ' wₗ'ᵦ')]
        # From the term k'=k, l'=l: wₖₐ wₗᵦ

        # So the FULL Hessian element is:
        # d²/dtₖₐ dtₗᵦ Re Tr(U□) =
        #   Re Tr(wₖₐ wₗᵦ U) if k < l (from the cross term in ∏ exp)
        #   (1/2) Re Tr((wₖₐ wₖᵦ + wₖᵦ wₖₐ) U) if k = l
        #   Re Tr(wₗᵦ wₖₐ U) if k > l (from the cross term with reversed order)

        # But wait — the cross term for k>l should not appear since we sum k<l.
        # By symmetry of the Hessian: H_{(k,a),(l,b)} = H_{(l,b),(k,a)}.
        # So for k>l: d²/dtₖₐ dtₗᵦ = Re Tr(wₗᵦ wₖₐ U) by symmetry? No...

        # Actually the Hessian is symmetric, and:
        # d²/dtₖₐ dtₗᵦ = d²/dtₗᵦ dtₖₐ
        # So for k<l: both give Re Tr(wₖₐ wₗᵦ U)?
        # But Re Tr(wₖₐ wₗᵦ U) ≠ Re Tr(wₗᵦ wₖₐ U) in general.

        # The resolution: the second derivative should be computed as:
        # d²/dtₖₐ dtₗᵦ [Re Tr(∏ₘ exp(εₘ) · U)]|_{t=0}

        # For k=l: from (1/2)εₖ² contribution:
        #   = (1/2) Re Tr((wₖₐ wₖᵦ + wₖᵦ wₖₐ) U) ✓ (symmetric in a,b)

        # For k≠l: Both come from the product expansion.
        # If k<l, the contribution is εₖ εₗ → tₖₐ wₖₐ · tₗᵦ wₗᵦ → wₖₐ wₗᵦ
        # If k>l, the contribution is εₗ εₖ → tₗᵦ wₗᵦ · tₖₐ wₖₐ → wₗᵦ wₖₐ

        # Wait, both k<l and k>l contribute if we look at ALL pairs.
        # The expansion is: Σ_{k<l} εₖ εₗ.
        # d²/dtₖₐ dtₗᵦ for k<l gives: wₖₐ wₗᵦ
        # d²/dtₗᵦ dtₖₐ for k<l also gives: wₖₐ wₗᵦ (same thing)

        # So d²/dtₖₐ dtₗᵦ = Re Tr(wₖₐ wₗᵦ U) for k<l.

        # But wait, this isn't symmetric in (k,a) ↔ (l,b):
        # d²/dtₖₐ dtₗᵦ = Re Tr(wₖₐ wₗᵦ U) (for k<l)
        # d²/dtₗᵦ dtₖₐ should equal this (symmetry of mixed partials)
        # But if I computed it as d²/dtₗᵦ dtₖₐ by SWAPPING roles:
        # Now l<k is false, so... hmm.

        # Actually, the Hessian must be symmetric since Re Tr(U□(t)) is a
        # smooth function of the parameters. Let me verify:
        # H_{(k,a),(l,b)} = Re Tr(wₖₐ wₗᵦ U) for k<l
        # H_{(l,b),(k,a)} = Re Tr(wₗᵦ wₖₐ U) for l>k... but l>k means l<k is
        # handled as k'=l, l'=k with k'>l'... this is getting confusing.

        # Let me just compute it correctly. The second derivative is:
        # d²/dt_i dt_j f(t) where f = Re Tr(∏ exp(tₖ εₖ) U)
        # (using tₖ as shorthand for the specific component of that link)

        # OK I think the issue is that the expansion ∏ exp(εₖ) at t=0 gives:
        # I + Σₖ εₖ + (1/2)(Σₖ εₖ)² + (1/2)Σ_{k<l}[εₖ,εₗ] + O(ε³)
        # where I used the identity from step 1.

        # So the t² coefficient is:
        # (1/2)(Σ εₖ)² + (1/2)Σ_{k<l}[εₖ,εₗ]
        # = (1/2) Σ_{k,l} εₖ εₗ + (1/2)Σ_{k<l}[εₖ,εₗ]
        # = (1/2) Σ_{k,l} εₖ εₗ + (1/2)Σ_{k<l}(εₖ εₗ - εₗ εₖ)
        # = (1/2) Σₖ εₖ² + (1/2) Σ_{k≠l} εₖ εₗ + (1/2) Σ_{k<l} εₖ εₗ - (1/2)Σ_{k<l} εₗ εₖ
        # = (1/2) Σₖ εₖ² + Σ_{k<l} εₖ εₗ
        # (as expected: the product of exponentials)

        # So Re Tr([t² coeff] U) = (1/2)Σₖ Re Tr(εₖ²U) + Σ_{k<l} Re Tr(εₖ εₗ U)

        # Now εₖ = Σₐ tₖₐ wₖₐ. So εₖ² = Σₐᵦ tₖₐ tₖᵦ wₖₐ wₖᵦ.
        # And εₖ εₗ = Σₐᵦ tₖₐ tₗᵦ wₖₐ wₗᵦ.

        # The Hessian is d²/dtₖₐ dtₗᵦ [2 × t²_coefficient_multiplied_by_U]:
        # (Factor of 2 because d²/dt² of t² f = 2f)

        # For k=l:
        #   From (1/2)εₖ²: d²/dtₖₐ dtₖᵦ [(1/2)Σ tₖₐ' tₖᵦ' wₖₐ' wₖᵦ']
        #     = (1/2)(wₖₐ wₖᵦ + wₖᵦ wₖₐ) (as computed above)
        #   Factor of 2: gives Re Tr((wₖₐ wₖᵦ + wₖᵦ wₖₐ) U)

        # Hmm wait, I need to be more careful. Re Tr(U□(t)) has the expansion:
        # Re Tr(U) + Σ tₖₐ Re Tr(wₖₐ U) +
        #   [(1/2) Σₖ Re Tr(εₖ² U) + Σ_{k<l} Re Tr(εₖ εₗ U)] + O(t³)

        # where the last term is already the full t² coefficient including the 1/2.

        # The HESSIAN of Re Tr(U□(t)) w.r.t. the t parameters is:
        # ∂²/∂tₖₐ ∂tₗᵦ Re Tr(U□)

        # For k=l: ∂²/∂tₖₐ ∂tₖᵦ of [(1/2) Re Tr(εₖ² U)]
        #   = (1/2) Re Tr((wₖₐ wₖᵦ + wₖᵦ wₖₐ) U) ← symmetric ✓

        # For k<l: ∂²/∂tₖₐ ∂tₗᵦ of [Re Tr(εₖ εₗ U)]
        #   = Re Tr(wₖₐ wₗᵦ U) ← NOT obviously symmetric in (k,a)↔(l,b)

        # But by equality of mixed partials, we need:
        #   Re Tr(wₖₐ wₗᵦ U) = Re Tr(wₗᵦ wₖₐ U)

        # Is this true? In general NO for matrices. But Re Tr(AB U) where
        # A,B are anti-Hermitian and U is unitary... let me check.

        # Hmm, Re Tr(AB U) = Re Tr(BUA) (cyclic) ≠ Re Tr(BAU) in general.

        # So there might be an error in my approach. Let me reconsider.

        # Actually, the issue is that the perturbation exp(tₖₐ wₖₐ) only
        # affects ONE exponential. The Hessian should come from expanding
        # EACH exponential separately.

        # Let me redo this more carefully for 2 exponentials first.
        # f(s,t) = Re Tr(exp(sA) exp(tB) U) where A,B ∈ su(2), U ∈ SU(2).
        # df/ds = Re Tr(A exp(sA) exp(tB) U)
        # d²f/dsdt = Re Tr(A exp(sA) B exp(tB) U)
        # At s=t=0: d²f/dsdt = Re Tr(A B U)
        # Similarly: d²f/dtds = Re Tr(A B U) (it IS symmetric because
        # partial derivatives commute for smooth functions)

        # But: d²f/dtds at s=t=0:
        # df/dt = Re Tr(exp(sA) B exp(tB) U)
        # d²f/dtds = Re Tr(A exp(sA) B exp(tB) U)
        # At s=t=0: Re Tr(A B U) ✓ same

        # OK so for k<l: H_{(k,a),(l,b)} = Re Tr(wₖₐ wₗᵦ U)
        # And H_{(l,b),(k,a)} should equal this by symmetry.

        # But if I computed H_{(l,b),(k,a)} with l>k, I would get...
        # I'd need to find wₗᵦ and wₖₐ in the reversed order.
        # Since exp(εₗ) comes AFTER exp(εₖ) in the product:
        # ∏ = ... exp(εₖ) ... exp(εₗ) ...
        # d/dtₗᵦ gives exp(εₖ) (at t=0 = I) ... wₗᵦ ... U
        # d²/dtₖₐ dtₗᵦ at t=0: wₖₐ ... wₗᵦ ... U

        # But at t=0, ALL exponentials are I, so:
        # d²/dtₖₐ dtₗᵦ = Re Tr(wₖₐ · I · wₗᵦ · I · U) = Re Tr(wₖₐ wₗᵦ U)

        # Wait, that's only true if the two exponentials are adjacent.
        # If there are other exponentials between them, at t=0 they contribute I.
        # So at t=0: d²/dtₖₐ dtₗᵦ = Re Tr(wₖₐ wₗᵦ U) regardless of position.

        # Similarly: d²/dtₗᵦ dtₖₐ = Re Tr(wₗᵦ wₖₐ U)

        # For the Hessian to be symmetric, we need:
        # Re Tr(wₖₐ wₗᵦ U) = Re Tr(wₗᵦ wₖₐ U)

        # Let me check numerically...

        # Actually, for Hermitian matrix H = -d²S where S is the action,
        # the Hessian IS symmetric because S is a real-valued smooth function.
        # So d²S/dtₖₐ dtₗᵦ = d²S/dtₗᵦ dtₖₐ.

        # But this means Re Tr(wₖₐ wₗᵦ U) = Re Tr(wₗᵦ wₖₐ U)!

        # Let me verify: Re Tr(ABU) = Re Tr(BUAU⁻¹ U²)... hmm, not obviously.
        # Actually, for A,B ∈ su(2) (anti-Hermitian, traceless) and U ∈ SU(2):
        # We need Re Tr(ABU) = Re Tr(BAU).
        # Re Tr(ABU) - Re Tr(BAU) = Re Tr([A,B]U)
        # And [A,B] ∈ su(2) (traceless, anti-Hermitian).
        # Re Tr([A,B]U) = Re Tr([A,B](aI+b)) = a·Re Tr([A,B]) + Re Tr([A,B]b) = Tr([A,B]b)
        # So Re Tr(ABU) ≠ Re Tr(BAU) in general!

        # This means the Hessian computed from my formula ISN'T symmetric??
        # That can't be right... Let me recheck.

        # Hmm, I think the issue is that my "push to left" formula is correct
        # for the ONE-PARAMETER case (perturbation along v = (v₁,...,v₄) with
        # common parameter t), but for INDEPENDENT parameters for each link,
        # the expansion is different.

        # Wait, let me reconsider. For independent perturbations:
        # Q₁ → exp(s₁ v₁) Q₁, Q₂ → exp(s₂ v₂) Q₂, etc.
        # U□(s) = exp(s₁ v₁) Q₁ exp(s₂ v₂) Q₂ Q₃⁻¹ exp(-s₃ v₃) Q₄⁻¹ exp(-s₄ v₄)

        # Push everything to the left:
        # = exp(s₁ w₁) exp(s₂ w₂) exp(s₃ w₃) exp(s₄ w₄) U

        # where wₖ are the same as before (INDEPENDENT of sₖ).

        # Expand to second order in s:
        # f(s) = Re Tr(∏ exp(sₖ wₖ) U)
        # = Re Tr(U) + Σ sₖ Re Tr(wₖ U) +
        #   Σₖ sₖ²/2 Re Tr(wₖ² U) + Σ_{k<l} sₖ sₗ Re Tr(wₖ wₗ U) + O(s³)

        # So ∂²f/∂sₖ ∂sₗ|_{s=0} =
        #   Re Tr(wₖ² U) if k=l
        #   Re Tr(wₖ wₗ U) if k<l

        # And by symmetry of second derivatives: Re Tr(wₖ wₗ U) = Re Tr(wₗ wₖ U) for k<l??

        # No! The issue is that the parameterization matters. Let me redo.
        # With independent parameters s₁,...,s₄:
        # ∂f/∂s₁ = Re Tr(w₁ exp(s₁w₁) exp(s₂w₂) exp(s₃w₃) exp(s₄w₄) U)
        # ∂²f/∂s₂∂s₁|_{s=0} = Re Tr(w₁ w₂ U)
        # ∂²f/∂s₁∂s₂|_{s=0}:
        # ∂f/∂s₂ = Re Tr(exp(s₁w₁) w₂ exp(s₂w₂) exp(s₃w₃) exp(s₄w₄) U)
        # ∂²f/∂s₁∂s₂|_{s=0} = Re Tr(w₁ w₂ U) ← YES, same!

        # Because at s=0, ∂/∂s₁ of exp(s₁w₁) = w₁ and exp(s₁w₁)|_{s=0} = I.
        # So ∂²f/∂s₁∂s₂ = Re Tr(w₁ w₂ exp(s₂w₂)..U) → at s=0: Re Tr(w₁ w₂ U) ✓

        # So the result IS Re Tr(wₖ wₗ U) for k<l.
        # But this is NOT equal to Re Tr(wₗ wₖ U) in general.

        # But f(s) is smooth and real-valued, so ∂²f/∂sₖ∂sₗ = ∂²f/∂sₗ∂sₖ.
        # This means the result IS symmetric, which contradicts...

        # Let me just verify numerically. If Re Tr(w₁w₂U) = Re Tr(w₂w₁U), I'm wrong
        # about them being different.

        # Actually wait. I was computing ∂²f/∂sₖ∂sₗ as the second derivative of
        # f(s₁,...,s₄) = Re Tr(∏ exp(sₖwₖ) U).
        # If both orders give Re Tr(w₁w₂U), then it IS symmetric. Let me check the
        # other order:
        # ∂f/∂s₁ = Re Tr(w₁ ∏_{k≥2} exp(sₖwₖ) U)  (since d/ds₁ only hits exp(s₁w₁))
        # ∂²f/∂s₂∂s₁ = Re Tr(w₁ · d/ds₂[∏_{k≥2} exp(sₖwₖ)] · U)
        # d/ds₂ hits exp(s₂w₂): = Re Tr(w₁ w₂ ∏_{k≥3} exp(sₖwₖ) U)
        # At s=0: Re Tr(w₁ w₂ U) ✓

        # Now the other order:
        # ∂f/∂s₂ = Re Tr(exp(s₁w₁) · w₂ · ∏_{k≥3} exp(sₖwₖ) · U)
        # ∂²f/∂s₁∂s₂ = Re Tr(d/ds₁[exp(s₁w₁)] · w₂ · ∏_{k≥3} exp(sₖwₖ) · U)
        # = Re Tr(w₁ exp(s₁w₁) w₂ ∏_{k≥3} exp(sₖwₖ) U)
        # At s=0: Re Tr(w₁ w₂ U) ✓

        # So BOTH ORDERS give Re Tr(w₁ w₂ U). The function IS smooth and
        # the mixed partials ARE equal. But that means Re Tr(w₁w₂U) is the
        # Hessian entry for BOTH (1,2) and (2,1). The Hessian matrix has
        # H₁₂ = H₂₁ = Re Tr(w₁w₂U), not H₁₂ = Re Tr(w₁w₂U), H₂₁ = Re Tr(w₂w₁U).

        # So the formula for the ordered product IS correct and automatically
        # gives a symmetric Hessian, even though Re Tr(w₁w₂U) ≠ Re Tr(w₂w₁U).
        # The ordering of w₁, w₂ comes from the PHYSICAL ordering of
        # exponentials in the product, and both orderings of differentiation
        # give the SAME result.

        # Great. So:
        # H_{(k,a),(l,b)} = Re Tr(wₖₐ wₗᵦ U) for k ≤ l (where k<l uses the
        # ordered product, and k=l uses Re Tr(wₖₐ wₖᵦ U) = Re Tr(wₖₐ² U) for a=b)
        # Wait, for k=l: (1/2) Re Tr((wₖₐ wₖᵦ + wₖᵦ wₖₐ) U)?

        # Hmm, no. Let me redo the k=l case.
        # For k=l, both perturbations are in the SAME exponential:
        # exp(sₖ,ₐ wₖₐ + sₖ,ᵦ wₖᵦ)
        # = I + sₖₐ wₖₐ + sₖᵦ wₖᵦ + (1/2)(sₖₐ wₖₐ + sₖᵦ wₖᵦ)² + ...
        # d²/dsₖₐ dsₖᵦ [(1/2)(sₖₐ wₖₐ + sₖᵦ wₖᵦ)²]
        # = (1/2)(wₖₐ wₖᵦ + wₖᵦ wₖₐ)

        # So for k=l: ∂²f/∂sₖₐ ∂sₖᵦ = Re Tr((1/2)(wₖₐ wₖᵦ + wₖᵦ wₖₐ) U)
        # This IS symmetric in a,b ✓

        # For k<l: ∂²f/∂sₖₐ ∂sₗᵦ = Re Tr(wₖₐ wₗᵦ U)
        # And by symmetry of mixed partials: = ∂²f/∂sₗᵦ ∂sₖₐ

        # So the Hessian element is:
        # H_{(k,a),(l,b)} = H_{(l,b),(k,a)} = Re Tr(wₖₐ wₗᵦ U)  for k < l
        # H_{(k,a),(k,b)} = (1/2) Re Tr((wₖₐ wₖᵦ + wₖᵦ wₖₐ) U)

        # BUT WAIT: the formula for the one-parameter case gave:
        # d²/dt² Re Tr(U□) = Re Tr(w²U) + Σ_{i<j} Re Tr([wᵢ,wⱼ]U)
        # where w = Σ sₖ wₖ with all sₖ = t.
        # This equals Σₖ Re Tr(wₖ² U) + 2 Σ_{k<l} Re Tr(wₖ wₗ U) +
        #             Σ_{k<l} Re Tr([wₖ,wₗ]U)
        # = Σₖ Re Tr(wₖ² U) + 2 Σ_{k<l} Re Tr(wₖ wₗ U) +
        #   Σ_{k<l} Re Tr(wₖ wₗ U) - Re Tr(wₗ wₖ U)
        # Hmm that doesn't simplify nicely.

        # Actually, Re Tr(w²U) = Σ Re Tr(wₖ² U) + Σ_{k≠l} Re Tr(wₖ wₗ U)
        # = Σ Re Tr(wₖ² U) + Σ_{k<l} Re Tr(wₖ wₗ U) + Σ_{k>l} Re Tr(wₖ wₗ U)
        # = Σ Re Tr(wₖ² U) + Σ_{k<l} Re Tr(wₖ wₗ U) + Σ_{k<l} Re Tr(wₗ wₖ U)
        # = Σ Re Tr(wₖ² U) + Σ_{k<l} Re Tr((wₖ wₗ + wₗ wₖ) U)

        # And the one-parameter second derivative is:
        # Σₖ Re Tr(wₖ² U) + 2 Σ_{k<l} Re Tr(wₖ wₗ U)
        # = Re Tr(w² U) + Σ_{k<l} Re Tr([wₖ, wₗ] U)  ✓ (matches our formula)

        # Because:
        # Σ_{k<l} [Re Tr((wₖwₗ + wₗwₖ)U) + Re Tr([wₖ,wₗ]U)]
        # = Σ_{k<l} [Re Tr((wₖwₗ + wₗwₖ)U) + Re Tr(wₖwₗU) - Re Tr(wₗwₖU)]
        # = Σ_{k<l} 2 Re Tr(wₖ wₗ U) ✓

        # OK so the matrix-level Hessian for Re Tr(U□(t)):
        # For a single plaquette with 4 edges, the 12×12 block is:
        # H^□_{(k,a),(l,b)} (k,l ∈ {1,2,3,4}, a,b ∈ {1,2,3})
        #
        # k=l: (1/2) Re Tr((wₖₐ wₖᵦ + wₖᵦ wₖₐ) U)
        # k<l: Re Tr(wₖₐ wₗᵦ U)
        # k>l: Re Tr(wₗᵦ wₖₐ U) [= H_{(l,b),(k,a)}]

        # Let me simplify. For ALL (k,l), (a,b):
        # if k <= l: H = Re Tr(wₖₐ wₗᵦ U) for k<l, or
        #            H = (1/2) Re Tr((wₖₐ wₖᵦ + wₖᵦ wₖₐ) U) for k=l

        # Actually, I realize the simpler expression for k=l:
        # (1/2) Re Tr((wₖₐ wₖᵦ + wₖᵦ wₖₐ) U) = Re Tr(wₖₐ wₖᵦ U)
        # IFF Re Tr(wₖₐ wₖᵦ U) = Re Tr(wₖᵦ wₖₐ U).
        # This is true because both perturbations are in the same exponential,
        # and the Hessian is symmetric.
        # But Re Tr(ABU) ≠ Re Tr(BAU) in general...

        # Let me just numerically verify by comparing to FD.

        # DECISION: I'll compute the full analytical Hessian using the formula
        # from the expansion, and check it against FD. Let me use:
        # H_{(k,a),(l,b)} for k<l: Re Tr(wₖₐ wₗᵦ U)
        # H_{(k,a),(k,b)}: Re Tr(wₖₐ wₖᵦ U)
        # then symmetrize: H = (H + H^T) / 2

        # Wait, but the expansion gives non-symmetric entries for k<l.
        # The actual Hessian IS symmetric, and equals Re Tr(wₖₐ wₗᵦ U) for k<l
        # (both orderings of differentiation give this). So:
        # H_{(k,a),(l,b)} = Re Tr(wₖₐ wₗᵦ U) for k<l
        # H_{(l,b),(k,a)} = Re Tr(wₖₐ wₗᵦ U)  (same value, by symmetry of partials)
        # NOT Re Tr(wₗᵦ wₖₐ U)!

        # This is confusing. Let me just verify numerically.

        # Build the 12×12 "raw" Hessian for each plaquette
        # and scatter into 192×192.

        pass

    # I'll use a simpler approach: build the full Hessian directly by
    # computing d²/dt² for each pair of basis directions.

    # For the analytical formula, I'll use the one-parameter expansion and
    # construct the bilinear form directly.

    # OK, actually, let me take the simplest correct approach.
    # The Hessian H is a symmetric bilinear form.
    # For basis vectors eᵢ (unit vector in direction i of R^{192}):
    # H_{ij} = d²S/dt_i dt_j = (1/2)(d²S/dt² along eᵢ+eⱼ - d²S/dt² along eᵢ - d²S/dt² along eⱼ)
    # This is the polarization identity.

    # But that's expensive (192² evaluations). Instead, I'll build H_ij
    # by summing over plaquettes containing both links i and j.

    # For each plaquette, the contribution to H is:
    # H^□_{ij} = -(β/2) × [partial Hessian of Re Tr(U□)]

    # The partial Hessian comes from our expansion.
    # I'll use the direct approach: for each plaquette, compute the 12×12
    # sub-matrix and scatter.

    pass

# ============================================================
# Build analytical Hessian using the expansion coefficients
# ============================================================

def build_hessian_analytical():
    """
    Build the 192×192 Hessian analytically.

    For each plaquette with edges e₁,...,e₄:
    - Compute wₖₐ = sₖ Ad_{Pₖ}(Tₐ) for k=1..4, a=1..3
    - The Hessian contribution is:
      H^□_{(eₖ,a),(eₗ,b)} += -(β/2) × C_{(k,a),(l,b)}
      where C is the second-order expansion coefficient.

    For k<l: C_{(k,a),(l,b)} = Re Tr(wₖₐ wₗᵦ U)
    For k=l: C_{(k,a),(k,b)} = (1/2) Re Tr((wₖₐ wₖᵦ + wₖᵦ wₖₐ) U)
    """
    H = np.zeros((Ndof, Ndof))

    for (e1, e2, e3, e4) in plaquettes:
        U = compute_plaquette_holonomy(e1, e2, e3, e4)
        Q3inv = Q[e3].conj().T
        P2 = Q[e1].copy()
        P3 = Q[e1] @ Q[e2] @ Q3inv

        edges = [e1, e2, e3, e4]
        signs_arr = [1, 1, -1, -1]
        Ad_ops = [I2, P2, P3, U]

        # Compute wₖₐ for k=0..3, a=0..2
        wka = np.zeros((4, 3, 2, 2), dtype=complex)
        for k in range(4):
            for a in range(3):
                wka[k, a] = signs_arr[k] * Ad(Ad_ops[k], T_gen[a])

        # Build the 12×12 sub-Hessian
        for k in range(4):
            for a in range(3):
                i_global = 3 * edges[k] + a
                for l in range(4):
                    for b in range(3):
                        j_global = 3 * edges[l] + b
                        if k < l:
                            val = re_tr(wka[k, a] @ wka[l, b] @ U)
                        elif k == l:
                            val = 0.5 * re_tr((wka[k, a] @ wka[k, b] +
                                               wka[k, b] @ wka[k, a]) @ U)
                        else:  # k > l
                            # Use symmetry: same as (l,b),(k,a) with l<k
                            val = re_tr(wka[l, b] @ wka[k, a] @ U)

                        H[i_global, j_global] += -(beta / 2) * val

    # Symmetrize (should already be symmetric, but numerics)
    H = (H + H.T) / 2
    return H

# ============================================================
# Build B² formula Hessian
# ============================================================

def build_hessian_formula():
    """
    H_formula_{ij} = (β/(2N)) Σ□ [B□]ᵢ [B□]ⱼ = (β/4) Σ□ B□ᵢ B□ⱼ

    where B□ is the 192→3 linear map: B□(v) = Σₖ sₖ Ad_{Pₖ}(v_{eₖ})
    and B□ᵢ means the i-th column of B□ (in the 3D su(2) output space).
    """
    H = np.zeros((Ndof, Ndof))

    for (e1, e2, e3, e4) in plaquettes:
        Q3inv = Q[e3].conj().T
        P2 = Q[e1].copy()
        P3 = Q[e1] @ Q[e2] @ Q3inv
        U = compute_plaquette_holonomy(e1, e2, e3, e4)

        edges = [e1, e2, e3, e4]
        signs_arr = [1, 1, -1, -1]
        Ad_ops = [I2, P2, P3, U]

        # B□ is a 3×192 matrix (maps 192-vector to 3-vector in su(2))
        # B□ₐᵢ = component a of sₖ Ad_{Pₖ}(T_c) where i = 3*eₖ + c
        # Build the 3×12 sub-block
        B_cols = np.zeros((3, 12))
        for k in range(4):
            for c in range(3):
                w = signs_arr[k] * Ad(Ad_ops[k], T_gen[c])
                w_vec = su2_to_vec(w)
                B_cols[:, 3*k + c] = w_vec

        # H_formula contribution: (β/4) Bᵀ B (12×12 block)
        block = (beta / 4) * B_cols.T @ B_cols

        # Scatter into full matrix
        local_to_global = []
        for k in range(4):
            for c in range(3):
                local_to_global.append(3 * edges[k] + c)

        for i_loc in range(12):
            for j_loc in range(12):
                H[local_to_global[i_loc], local_to_global[j_loc]] += block[i_loc, j_loc]

    return H

# ============================================================
# Run comparison
# ============================================================

print("Building H_actual (finite differences)...")
H_fd = build_hessian_fd(h=1e-4)
print(f"  Done. Symmetry check: |H - H^T|_max = {np.max(np.abs(H_fd - H_fd.T)):.2e}")

print("Building H_analytical...")
H_ana = build_hessian_analytical()
print(f"  Done. Symmetry check: |H - H^T|_max = {np.max(np.abs(H_ana - H_ana.T)):.2e}")

print("Building H_formula (B²)...")
H_form = build_hessian_formula()
print(f"  Done. Symmetry check: |H - H^T|_max = {np.max(np.abs(H_form - H_form.T)):.2e}")

# Compare
print("\n" + "=" * 70)
print("COMPARISONS")
print("=" * 70)

diff_fd_ana = np.max(np.abs(H_fd - H_ana))
diff_fd_form = np.max(np.abs(H_fd - H_form))
diff_ana_form = np.max(np.abs(H_ana - H_form))

print(f"\n  |H_FD - H_analytical|_max  = {diff_fd_ana:.6e}")
print(f"  |H_FD - H_formula|_max     = {diff_fd_form:.6e}")
print(f"  |H_analytical - H_formula|_max = {diff_ana_form:.6e}")

# Eigenvalues
eig_fd = np.sort(np.linalg.eigvalsh(H_fd))[::-1]
eig_ana = np.sort(np.linalg.eigvalsh(H_ana))[::-1]
eig_form = np.sort(np.linalg.eigvalsh(H_form))[::-1]

print(f"\n  Top 5 eigenvalues:")
print(f"  {'FD':>12s} {'Analytical':>12s} {'Formula':>12s}")
for i in range(5):
    print(f"  {eig_fd[i]:12.6f} {eig_ana[i]:12.6f} {eig_form[i]:12.6f}")

print(f"\n  λ_max: FD = {eig_fd[0]:.8f}, Ana = {eig_ana[0]:.8f}, Form = {eig_form[0]:.8f}")
print(f"  Ratio λ_max(actual)/λ_max(formula) = {eig_fd[0]/eig_form[0]:.8f}")

# Check inequality: λ_max(H_actual) ≤ λ_max(H_formula)?
print(f"\n  λ_max(H_actual) ≤ λ_max(H_formula)? {eig_fd[0] <= eig_form[0]}")

# Correction matrix C = H_formula - H_actual
C = H_form - H_ana
eig_C = np.sort(np.linalg.eigvalsh(C))[::-1]
print(f"\n  Correction C = H_formula - H_actual:")
print(f"  Top eigenvalue:    {eig_C[0]:.8f}")
print(f"  Bottom eigenvalue: {eig_C[-1]:.8f}")
print(f"  Is C ≥ 0 (PSD)?   {eig_C[-1] >= -1e-10}")

# Check at flat configuration
print("\n\n" + "=" * 70)
print("FLAT CONFIGURATION CHECK (Q = I for all links)")
print("=" * 70)

Q_backup = Q.copy()
Q[:] = I2[np.newaxis, :, :]

H_ana_flat = build_hessian_analytical()
H_form_flat = build_hessian_formula()

eig_flat_ana = np.sort(np.linalg.eigvalsh(H_ana_flat))[::-1]
eig_flat_form = np.sort(np.linalg.eigvalsh(H_form_flat))[::-1]

print(f"  λ_max (analytical): {eig_flat_ana[0]:.8f}")
print(f"  λ_max (formula):    {eig_flat_form[0]:.8f}")
print(f"  Expected (4β):      {4*beta:.8f}")
print(f"  |H_ana - H_form|_max = {np.max(np.abs(H_ana_flat - H_form_flat)):.2e}")

Q[:] = Q_backup

print("\nDone.")
