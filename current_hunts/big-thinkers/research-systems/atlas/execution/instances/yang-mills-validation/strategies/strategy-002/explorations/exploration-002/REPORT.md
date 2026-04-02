# Exploration 002: Path D — Direct SU(2) Hessian Computation

## Goal

Compute the ACTUAL second derivative d²/dt² Re Tr(U□(t))|_{t=0} analytically for SU(2) lattice gauge theory, identify ALL cross terms beyond the w²·U□ term, and verify every step numerically via finite differences on L=2, d=4.

## Conventions

- SU(2): N = 2, generators Tₐ = iσₐ/2 (a = 1,2,3)
- Inner product: ⟨X,Y⟩ = -2 Tr(XY), so |Tₐ|² = 1
- Wilson action: S(Q) = -(β/2) Σ□ Re Tr(U□)
- LEFT perturbation: Q → exp(t·v) · Q
- Plaquette: U□ = Q₁ Q₂ Q₃⁻¹ Q₄⁻¹

## Step 1: Analytical Second Derivative

### Derivation

Consider a plaquette U□ = Q₁ Q₂ Q₃⁻¹ Q₄⁻¹. Under left perturbation Qₖ → exp(t·vₖ) Qₖ:

U□(t) = exp(tv₁) Q₁ · exp(tv₂) Q₂ · Q₃⁻¹ exp(-tv₃) · Q₄⁻¹ exp(-tv₄)

**Push all exponentials to the left by conjugation:**

Define partial holonomies: P₁ = I, P₂ = Q₁, P₃ = Q₁Q₂Q₃⁻¹, P₄ = U□.

Then U□(t) = exp(tw₁) exp(tw₂) exp(tw₃) exp(tw₄) · U□

where:
- w₁ = v₁
- w₂ = Ad_{Q₁}(v₂) = Q₁ v₂ Q₁†
- w₃ = -Ad_{Q₁Q₂Q₃⁻¹}(v₃)
- w₄ = -Ad_{U□}(v₄)

**Expand the product of exponentials to O(t²):**

∏ₖ exp(twₖ) = I + tw + t²[w²/2 + (1/2)Σ_{i<j}[wᵢ,wⱼ]] + O(t³)

where w = w₁ + w₂ + w₃ + w₄ = B□(v) (the covariant derivative).

**Proof of the t² coefficient:** Multiply (I + twₖ + t²wₖ²/2 + ...) for k=1..4. The t² coefficient from the product is Σₖ wₖ²/2 + Σ_{i<j} wᵢwⱼ. Write this as w²/2 + (1/2)Σ_{i<j}[wᵢ,wⱼ] by noting that w² = Σₖwₖ² + Σ_{i≠j}wᵢwⱼ = Σₖwₖ² + Σ_{i<j}(wᵢwⱼ + wⱼwᵢ), so the "ordered" cross terms Σ_{i<j}wᵢwⱼ = w²/2 - Σₖwₖ²/2 + (1/2)Σ_{i<j}[wᵢ,wⱼ].

**Result:**

> **d²/dt² Re Tr(U□(t))|_{t=0} = Re Tr(w² U□) + Σ_{i<j} Re Tr([wᵢ,wⱼ] U□)**

The first term is the "w² U" term. The second term is the **commutator cross term**. `[VERIFIED]`

### Numerical Verification (Single Plaquette)

Tested with central finite differences (h = 10⁻⁴) on:
- **Flat (Q=I):** Cross terms = 0.000000 (traceless matrices have zero trace). Error |FD - Ana| < 6×10⁻⁸. `[VERIFIED]`
- **5 Random configs:** Cross terms are LARGE — ratio |comm/w²U| ranges from 0.07 to 6.3. Error |FD - Ana| < 2×10⁻⁷. `[VERIFIED]`
- **Large deformation (Q₁ = exp(πT₁)):** w²U = 0 (since Re Tr(U□) = 0), and the ENTIRE second derivative comes from cross terms. `[VERIFIED]`

### Key Finding: Cross Terms Are Large

Over 100 random configurations:
- Mean |comm/w²U| = 3.12
- Max |comm/w²U| = 63.6
- 37% of cases have |comm| > |w²U|
- Cross terms have **both signs** (56 positive, 44 negative)

**The commutator terms are NOT negligible — they are often the dominant contribution.**

## Step 2: SU(2) Simplification

### The w² Term

For w ∈ su(2): w² = -(|w|²/4)I where |w|² = -2Tr(w²).

Therefore: **Re Tr(w² U□) = -(|w|²/4) Re Tr(U□) = -(|w|²/2) cos(θ/2)**

where Re Tr(U□) = 2cos(θ/2) and θ is the plaquette angle.

### The Commutator Term — Cross Product Formula

For SU(2), the commutator has a beautiful cross-product structure.

**Structure constants (important sign):** For Tₐ = iσₐ/2:

[Tₐ,Tᵦ] = **-**εₐᵦ꜀T꜀

This means [T₁,T₂] = -T₃ (verified numerically). `[VERIFIED]`

Write wₖ = w⃗ₖ · T⃗ (3-component vector in the Tₐ basis). Then:

[wᵢ,wⱼ] = -(w⃗ᵢ × w⃗ⱼ) · T⃗

Write U□ = cos(θ/2)I + b where b = b⃗ · T⃗ ∈ su(2), |b⃗|² = 4sin²(θ/2).

Re Tr([wᵢ,wⱼ] U□) = Tr([wᵢ,wⱼ] b) = -(w⃗ᵢ × w⃗ⱼ)꜀ b⃗_d Tr(T꜀T_d) = -(w⃗ᵢ × w⃗ⱼ)꜀ b⃗꜀ (-1/2) = **(+1/2)(w⃗ᵢ × w⃗ⱼ) · b⃗**

**The total commutator term is:**

> Σ_{i<j} Re Tr([wᵢ,wⱼ] U□) = **(+1/2) L⃗ · b⃗**

where L⃗ = Σ_{i<j} w⃗ᵢ × w⃗ⱼ is the "angular momentum" vector.

Verified against direct matrix computation to machine precision (error < 2×10⁻¹⁵). `[VERIFIED]`

### Full Second Derivative for SU(2)

> **d²/dt² Re Tr(U□) = -(|w|²/2) cos(θ/2) + (1/2) L⃗ · b⃗**

where:
- |w|² = |B□(v)|² = -2Tr(w²) (norm of the covariant derivative)
- cos(θ/2) = Re Tr(U□)/2
- L⃗ = Σ_{i<j} w⃗ᵢ × w⃗ⱼ (ordered cross-product sum of 3-vectors)
- b⃗ = su(2) component of U□, with |b⃗|² = 4sin²(θ/2)

Verified against finite differences to O(h²) ≈ 2×10⁻⁷. `[VERIFIED]`

### Decomposition of H_formula - H_actual

The Wilson action Hessian: H_actual(v,v) = -(β/2) Σ□ d²/dt² Re Tr(U□)
= (β/4) Σ□ |w□|² cos(θ□/2) - (β/4) Σ□ L⃗□·b⃗□

The formula: H_formula(v,v) = (β/4) Σ□ |w□|²

Therefore:

> **C(v,v) = H_formula - H_actual = (β/4) Σ□ |w□|²(1 - cos(θ□/2)) + (β/4) Σ□ L⃗□·b⃗□**

The first term is **always ≥ 0** (the "curvature bonus" from non-flat plaquettes).
The second term is the **commutator correction** and can have either sign.

## Step 3: Numerical Verification (Full Hessian)

### Setup

L=2, d=4, periodic BC. 192 DOF (64 links × 3 su(2) components). 96 plaquettes. β = 1.0.

### Hessian Matrix Construction

Built the analytical Hessian from the product-of-exponentials expansion:

For each plaquette □ with edges at positions k=0,1,2,3:
- Same position (k=l): H□_{(eₖ,a),(eₖ,b)} = (1/2) Re Tr((wₖₐwₖᵦ + wₖᵦwₖₐ)U)
- Different positions (k<l): H□_{(eₖ,a),(eₗ,b)} = Re Tr(wₖₐwₗᵦU)

**Note:** Same-link, different-component entries are exactly zero by su(2) orthogonality: wₖₐwₖᵦ + wₖᵦwₖₐ = 0 for a≠b (since Ad preserves the orthonormal basis). `[VERIFIED]`

### Results

| Comparison | Max error |
|---|---|
| H_FD - H_analytical | 1.88 × 10⁻⁶ (= O(h²)) |
| H_FD - H_formula | 1.96 |
| H_analytical - H_formula | 1.96 |

**Eigenvalue comparison (top 5):**

| Rank | H_actual | H_formula |
|---|---|---|
| 1 | 2.464 | 3.576 |
| 2 | 2.334 | 3.538 |
| 3 | 2.301 | 3.501 |
| 4 | 2.275 | 3.486 |
| 5 | 2.252 | 3.438 |

- **λ_max(H_actual) / λ_max(H_formula) = 0.689** `[VERIFIED]`
- **λ_max(H_actual) ≤ λ_max(H_formula): YES** `[VERIFIED]`
- **Eigenvalue-by-eigenvalue inequality: 0 violations out of 192** `[VERIFIED]`

### Flat Configuration Check

At Q=I for all links:
- H_actual = H_formula exactly (max difference = 0)
- λ_max = 4β = 4.0 `[VERIFIED]`

### One-Parameter Quadratic Form Check

v^T H_actual v matches the analytical formula (w² + commutator terms) to 10⁻⁷ for all random directions tested. `[VERIFIED]`

## Step 4: The Bound

### Decomposition

From Step 2:

**H_actual(v,v) = (β/4) Σ□ |w□|² cos(θ□/2) - (β/4) Σ□ L⃗□·b⃗□**

**H_formula(v,v) = (β/4) Σ□ |w□|²**

So:

**C(v,v) = H_formula - H_actual = (β/4) Σ□ [|w□|²(1 - cos(θ□/2)) + L⃗□·b⃗□]**

The first term ≥ 0 always (curvature bonus). The second term can have either sign.

### SU(2) Product Identity

For the matrix-level Hessian decomposition, we use:

> **TₐTᵦ = -(δₐᵦ/4)I - (1/2)εₐᵦ꜀T꜀** `[VERIFIED]`

Consequence: For X = x⃗·T⃗, Y = y⃗·T⃗:
- XY = -(x⃗·y⃗/4)I - (1/2)(x⃗×y⃗)·T⃗
- Re Tr(XY · U) = -(x⃗·y⃗/2)cos(θ/2) + (1/4)(x⃗×y⃗)·b⃗

This gives the exact matrix decomposition:

For k < l: **C□_{(eₖ,a),(eₗ,b)} = (β/4)(1-cos(θ/2))(w⃗ₖₐ·w⃗ₗᵦ) + (β/8)(w⃗ₖₐ×w⃗ₗᵦ)·b⃗**

For k = l: **C□_{(eₖ,a),(eₖ,b)} = (β/4)(1-cos(θ/2))(w⃗ₖₐ·w⃗ₖᵦ)** (no cross-product, by su(2) orthogonality)

### Matrix Decomposition: C = C_curv + C_comm

**C_curv = (β/4)(1-cos(θ/2)) × BᵀB** (curvature bonus)
**C_comm: off-diagonal blocks with coefficient (β/8)(w⃗ₖₐ × w⃗ₗᵦ)·b⃗**

Verified: |C - (C_curv + C_comm)| = 6.7 × 10⁻¹⁶ `[VERIFIED]`

### Spectral Analysis of the Correction

| Matrix | Min eigenvalue | Max eigenvalue | PSD? |
|---|---|---|---|
| C | -0.765 | 4.340 | **NO** (41 negative) |
| C_curv | +0.018 | 3.850 | **YES** |
| C_comm | -1.555 | +1.624 | **NO** (indefinite) |

**Key finding: C is NOT positive semi-definite.** The inequality H_actual ≤ H_formula does NOT hold as a matrix inequality. `[VERIFIED]`

### Why λ_max(H_actual) ≤ λ_max(H_formula) Still Holds

At the top eigenvector v_top of H_actual:
- v_top^T C v_top = **+0.103** (positive!)
- v_top^T C_curv v_top = 1.163
- v_top^T C_comm v_top = -1.060
- Ratio C_curv/|C_comm| = **1.10** (barely compensates)

The curvature bonus compensates the commutator correction in the top eigenspace, but the margin is slim. Over 20 random configurations, the inequality λ_max(H_actual) ≤ λ_max(H_formula) holds with ratio 0.61-0.74. `[COMPUTED]`

### Per-Plaquette Bound Fails

For a SINGLE plaquette, the quantity |w|²(1-cos(θ/2)) + L⃗·b⃗ can be negative (violations in ~10-28% of random directions). The worst case has min C/|v|² = -1.05. So **the proof cannot work per-plaquette**. `[COMPUTED]`

### Proof Status

**What is established:**

1. Complete analytical formula for H_actual with all cross terms `[VERIFIED]`
2. H_actual = (β/4)cos(θ/2) × BᵀB + H_comm (exact decomposition) `[VERIFIED]`
3. C = C_curv + C_comm with C_curv PSD, C_comm indefinite `[VERIFIED]`
4. λ_max(H_actual) ≤ λ_max(H_formula) for all 50+ tested configs `[COMPUTED]`
5. λ_max(H_actual) < 2(d-1)β for all 50 tested configs `[COMPUTED]`

**What remains to prove:**

The inequality λ_max(H_actual) ≤ λ_max(H_formula) requires a structural argument. The three approaches below have been analyzed:

| Approach | Status |
|---|---|
| C ≥ 0 (PSD matrix inequality) | **FAILS** — C has 41 negative eigenvalues |
| Per-plaquette bound | **FAILS** — negative per-plaquette |
| v_top^T C v_top ≥ 0 | **HOLDS numerically** — needs proof |

**The gap is precisely:** Prove that the top eigenspace of H_actual always sees non-negative C. The mechanism is that C_curv compensates C_comm in the top eigenspace (ratio ≈ 1.10), even though it fails in other directions.

### Possible Proof Strategies

**Strategy A (Direct |v|² bound):** Bound H_actual ≤ c|v|² directly, without using the B² formula. Since cos(θ/2) ≤ 1 and the commutator terms are bounded by Cauchy-Schwarz, this gives c ≤ 2(d-1)β. Combined with the trivial bound |w|² ≤ 4Σ|vₖ|², this yields the spectral gap for β < 1/(d-1) = 1/3. This is weaker than β < 1/6 but doesn't need the B² inequality. `[CONJECTURED]`

**Strategy B (Eigenspace orthogonality):** From E001's finding that v_top(H_actual) and v_top(H_formula) are nearly orthogonal, prove that the commutator term projects onto a complementary space to the top eigenspace. `[CONJECTURED]`

**Strategy C (Lattice cancellation):** The per-plaquette bound fails, but on the full lattice, commutator terms from different plaquettes sharing the same link may partially cancel. Analyze this cancellation structure. `[CONJECTURED]`
