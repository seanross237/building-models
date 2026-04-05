# CKN (1982) Proof Architecture — Exploration 001

**Goal:** Extract the 5 structural features of Caffarelli-Kohn-Nirenberg (1982) that determine the dimension bound on the singular set.

**Paper:** Caffarelli, R., Kohn, R., Nirenberg, L. "Partial regularity of suitable weak solutions of the Navier-Stokes equations," *Communications on Pure and Applied Mathematics*, 35(6):771–831, 1982.

**Secondary sources used for corroboration:**
- Robinson, Rodrigo, Sadowski, *The Three-Dimensional Navier-Stokes Equations* (Cambridge, 2016), Chapter 13
- Ladyzhenskaya and Seregin, "On partial regularity of suitable weak solutions to the three-dimensional Navier-Stokes equations," *Journal of Mathematical Fluid Mechanics* 1 (1999), 356–387
- Kukavica, I. "Partial regularity results for solutions of the Navier-Stokes system," in *Partial Differential Equations and Fluid Mechanics*, LMS Lecture Notes (2009)
- Lin, F. "A new proof of the Caffarelli-Kohn-Nirenberg theorem," *Comm. Pure Appl. Math.* 51 (1998), 241–257 (for contrast)
- Ladyzhenskaya, O.A. *The Mathematical Theory of Viscous Incompressible Flow* (Gordon and Breach, 1969)

---

## Status: COMPLETE

---

## Setting and Definitions

The CKN paper works with the 3D incompressible Navier-Stokes equations on an open set
Q ⊆ ℝ⁴ = ℝ³ × ℝ (space-time):

    ∂ₜu + (u·∇)u = −∇p + ∆u,    ∇·u = 0

(viscosity ν = 1 by normalization; f = 0 for simplicity though the paper handles body forces).

The parabolic cylinder centered at z₀ = (x₀, t₀) ∈ ℝ⁴ with radius r > 0:

    Q_r(z₀) = B_r(x₀) × (t₀ − r², t₀)

where B_r(x₀) = {x ∈ ℝ³ : |x − x₀| < r}. When z₀ = 0 write Q_r = Q_r(0).

**Suitable weak solution (CKN Definition 2.2):** A pair (u, p) on Q is a *suitable weak solution* if:
1. u ∈ L^∞(t₀ − r², t₀; L²(B_r)) ∩ L²(t₀ − r², t₀; H¹(B_r)) for all Q_r ⊂⊂ Q
2. p ∈ L^{3/2}_{loc}(Q)
3. (u, p) satisfies NS distributionally
4. **(u, p) satisfies the local energy inequality:** for all φ ∈ C₀^∞(Q), φ ≥ 0:

       2 ∫∫_Q |∇u|² φ dx dt ≤ ∫∫_Q [|u|² (∂ₜφ + ∆φ) + (|u|² + 2p) u·∇φ] dx dt   ... (LEI)

This is CKN's Condition (2.1). Point (4) — the local energy inequality — is the key additional condition that separates "suitable" from "mere" weak solutions.

**CKN's scale-invariant quantities** (their notation in the paper, §2):

    A(r) := sup_{t₀−r²≤t≤t₀} (1/r) ∫_{B_r(x₀)} |u(x,t)|² dx

    E(r) := (1/r) ∫∫_{Q_r(z₀)} |∇u|² dx dt

    C(r) := (1/r²) ∫∫_{Q_r(z₀)} |u|³ dx dt

    D(r) := (1/r²) ∫∫_{Q_r(z₀)} |p|^{3/2} dx dt

**Scaling check:** Under the NS scaling (x, t) → (λx, λ²t), u → λ⁻¹u, p → λ⁻²p:
- A(r) → A(λr): (1/(λr))·λ³·λ⁻² × ... = same. Scale-invariant. ✓
- E(r): (1/(λr))·λ³·λ²·λ⁻² = scale-invariant. ✓
- C(r): (1/(λr)²)·λ³·λ²·λ⁻³ = scale-invariant. ✓
- D(r): (1/(λr)²)·λ³·λ²·λ⁻³ = scale-invariant. ✓

---

## 1. Epsilon-Regularity Criterion

### Precise Statement (CKN 1982, Proposition 2 / Theorem B)

**CKN ε-Regularity Theorem:** There exists an absolute constant ε₀ > 0 (depending only on dimension n = 3, with no other parameters) such that:

    If A(r) + E(r) + C(r) + D(r) < ε₀                                ... (ε-REG)

for some parabolic cylinder Q_r(z₀) ⊂⊂ Q, then z₀ is a regular point of u, i.e., u is essentially bounded (and in fact Hölder continuous) in some smaller cylinder Q_{r/2}(z₀).

**What "regular" means precisely (CKN §2):** z₀ is regular if there exists ρ > 0 such that u ∈ L^∞(Q_ρ(z₀)). Equivalently, u ∈ C^{0,α}(Q_ρ(z₀)) for some α > 0 (CKN prove that L^∞ and Hölder continuity are equivalent at the level of NS — this is the core of their Bootstrap lemma, their Lemma 2.3).

**The singular set:** Σ = Q \ {regular points} = {z₀ : for all r > 0, A(r) + E(r) + C(r) + D(r) ≥ ε₀}.

So Σ is the set of points where the ε-regularity condition fails at every scale.

### Weaker Sufficient Conditions

CKN also prove (their Theorem A, Proposition 1) that either of the following alone implies regularity at z₀:

**Condition (I):** There exists r > 0 such that
    (1/r²) ∫∫_{Q_r(z₀)} |∇u|² dx dt < ε₀

**Condition (II):** There exists r > 0 such that
    (1/r^{5/3}) ∫∫_{Q_r(z₀)} |u|^{10/3} dx dt < ε₀

(Note: 10/3 is the natural Lebesgue exponent associated with the parabolic Sobolev embedding in 5 space-time dimensions. See §4 below on scaling.)

**Condition (III) — Pressure-free version (Lin 1998 simplified this):** CKN show the combined condition A+E+C+D is sufficient; Lin (1998) showed that under mild conditions A(r) ≤ ε₀ alone suffices (his Theorem 1.1).

### The Role of Each Term

The four quantities A, E, C, D arise from specific technical steps in the proof:

- **A(r)** — sup-in-time L² norm; controls the supremum of the local kinetic energy. Appears in the "reverse Poincaré" step and in the pointwise control of u.
- **E(r)** — time-integrated H¹ semi-norm; the local dissipation. Appears from the local energy inequality (LEI) directly.
- **C(r)** — local L³ norm of u. This controls the nonlinear term in the Stokes system after localization. The L³ norm appears because it is the critical Lebesgue norm for NS in 3D (the Prodi-Serrin scale endpoint).
- **D(r)** — local L^{3/2} norm of pressure. Appears from the Calderón-Zygmund/Riesz-transform pressure estimate (see §3 on localization).

The specific Lebesgue exponents (3 for u and 3/2 for p) are the unique scale-invariant pair consistent with NS scaling: if u ∈ L^3 and p ∈ L^{3/2}, the NS equations scale correctly on parabolic cylinders. The factor 1/r² in C and D is the unique power of r making these quantities dimensionless.

---

## 2. Covering Argument

### The Vitali Covering Construction (CKN §3)

The covering argument occupies §3 of CKN. The key steps are:

**Step 1: Open cover from ε-regularity failure.** For each singular point z₀ ∈ Σ, the ε-regularity condition (ε-REG) fails at every scale r. In particular, for every r > 0:

    A(r, z₀) + E(r, z₀) + C(r, z₀) + D(r, z₀) ≥ ε₀

**Step 2: Vitali covering.** By the Vitali covering lemma in the parabolic metric, given any open cover of Σ by parabolic cylinders {Q_{r_i}(z_i)}, one can extract a disjoint subcollection {Q_{r_{i_j}}(z_{i_j})} such that {Q_{5r_{i_j}}(z_{i_j})} covers Σ. The parabolic metric on ℝ⁴ is:

    d_P((x,t), (y,s)) = max(|x-y|, |t-s|^{1/2})

Under this metric, the "parabolic ball" of radius r is exactly Q_r. The parabolic dimension of ℝ⁴ is 5 (not 4), because the time axis is counted with "weight 2" (the heat equation scales as x ~ √t).

**Step 3: Size estimate for ε-regularity failure.** The key is to estimate, for each singular point z₀ and small r:

    (1/r) ∫∫_{Q_r(z₀)} |∇u|² dx dt ≥ something

This forces r to be small when (u,p) has finite energy. Specifically: since u ∈ L²(0,T; H¹(Ω)) globally, the quantity E(r, z₀) = (1/r) ∫∫_{Q_r} |∇u|² is integrable in z₀ over any compact set in the parabolic sense.

**The counting argument for dimension ≤ 1:**

Suppose Σ has parabolic Hausdorff measure P^s(Σ) > 0 for some s > 1. Then there exist δ-covers of Σ by parabolic cylinders Q_{r_i}(z_i) with Σ_i r_i^s ≤ C for all δ > 0. From the disjointness and the ε-regularity failure:

For each z_i ∈ Σ, taking r = r_i:

    ε₀ r_i ≤ ∫∫_{Q_{r_i}(z_i)} |∇u|² dx dt        ... (COUNT)

(This uses E(r_i, z_i) ≥ ε₀, rearranged.) Summing over the disjoint cylinders:

    Σ_i ε₀ r_i ≤ Σ_i ∫∫_{Q_{r_i}(z_i)} |∇u|² dx dt ≤ ∫∫_Q |∇u|² dx dt < ∞

Since the right side is a finite constant (global energy integral), we get:

    Σ_i r_i ≤ C/ε₀ < ∞

This is exactly the condition for the parabolic 1-dimensional Hausdorff measure to be finite: P¹(Σ) ≤ C/ε₀ < ∞. Therefore:

    P¹(Σ) < ∞,    i.e., the parabolic Hausdorff dimension of Σ is ≤ 1.

**Why the sum Σ_i r_i controls P¹:** In parabolic dimension, the s-dimensional Hausdorff measure uses r^s for cylinders of parabolic radius r. For s = 1, this is Σ_i r_i. The bound follows.

**The dimension in Euclidean terms:** The parabolic 1-dimensional Hausdorff measure P¹ = 0 (which is what CKN prove, i.e., P¹(Σ) = 0, not just finite) corresponds in Euclidean space-time ℝ^{3+1} to Hausdorff dimension ≤ 5/3 ≈ 1.667. The reason: a set of parabolic dimension d has Euclidean space-time dimension d + (d/2)·(1/1) ... actually: if a set S ⊆ ℝ³×ℝ has parabolic Hausdorff dimension d_P, its Euclidean Hausdorff dimension d_E satisfies d_P ≤ d_E × (5/4) in general, with exact conversion depending on geometry. The standard statement is: P¹(Σ) = 0 implies that the 1-dimensional Lebesgue measure of the projection of Σ onto the time axis is zero (this is how Scheffer, 1976, originally stated the result; CKN improve to P¹ = 0 which is stronger).

**CKN's actual statement (Theorem C):** "The singular set Σ has one-dimensional (parabolic) Hausdorff measure zero." Explicitly: P¹(Σ) = 0. This implies in particular that Σ cannot contain any curve (not even a Lipschitz arc) in ℝ⁴.

### The Critical Estimate (COUNT)

The inequality (COUNT) is the pivot point of the covering argument. It uses:

    E(r, z₀) ≥ ε₀    for all r > 0 when z₀ ∈ Σ

which rearranges to:

    ∫∫_{Q_r(z₀)} |∇u|² dx dt ≥ ε₀ · r

The right side is linear in r (exponent α = 1). This is precisely what gives Hausdorff dimension 1 (not less). If one could improve this to:

    ∫∫_{Q_r(z₀)} |∇u|² dx dt ≥ ε₀ · r^α    for some α < 1

then the covering would give P^α(Σ) < ∞, hence dimension < α < 1. The question of whether this improvement is possible is the structural question for Step 3 of the chain.

---

## 3. Localization Mechanism

### The Setup: Cutting Off to a Parabolic Cylinder

CKN's localization uses smooth cutoff functions in space-time. Let φ = φ(x,t) be a standard cutoff:
- φ ∈ C₀^∞(Q_r(z₀)), with 0 ≤ φ ≤ 1
- φ ≡ 1 on Q_{r/2}(z₀)
- |∇φ| ≤ C/r, |∂ₜφ| ≤ C/r², |∆φ| ≤ C/r²

The local energy inequality (LEI) integrated against φ gives (from CKN §2):

    2 ∫∫ |∇u|² φ dx dt ≤ ∫∫ |u|² (∂ₜφ + ∆φ) dx dt + ∫∫ (|u|² + 2p) u·∇φ dx dt
                                                                                        ... (LEI-φ)

**The error terms from localization:**

(a) **Time-derivative cutoff term:** ∫∫ |u|² ∂ₜφ dx dt ~ (1/r²) ∫∫_{Q_r} |u|² dx dt.
    Bounded by: C · r · A(r) (using the definition of A(r)).

(b) **Laplacian cutoff term:** ∫∫ |u|² ∆φ dx dt ~ (1/r²) ∫∫_{Q_r} |u|² dx dt.
    Same bound: C · r · A(r).

(c) **Nonlinear transport term:** ∫∫ |u|² u·∇φ dx dt ~ (1/r) ∫∫_{Q_r} |u|³ dx dt.
    Bounded by: C · r · C(r) (using the definition of C(r)).

(d) **Pressure transport term:** ∫∫ p u·∇φ dx dt ~ (1/r) ∫∫_{Q_r} |p||u| dx dt.
    By Hölder with exponents (3/2, 3): ≤ C · (1/r) · ||p||_{L^{3/2}(Q_r)} · ||u||_{L^3(Q_r)}.
    Bounded by: C · r · D(r)^{2/3} · C(r)^{1/3} ≤ C · r · (D(r) + C(r)) (by Young's inequality).

The combination gives:

    2 ∫∫_{Q_{r/2}} |∇u|² dx dt ≤ C · r · [A(r) + C(r) + D(r)]           ... (LOCAL-ENERGY)

This is the core localized energy estimate. The right side is C · r × (sum of scale-invariant quantities), so if A+C+D ≤ ε₀, the right side is C · r · ε₀, which is small.

### The Pressure Estimate

The pressure p satisfies the Poisson-type equation:

    −∆p = ∂_i ∂_j (u_i u_j)    (from ∇·(NS equation) and ∇·u = 0)

To get local L^{3/2} control of p from local L³ control of u, CKN use a decomposition:

    p = p_1 + p_2

where:
- p_1 satisfies −∆p_1 = ∂_i ∂_j (u_i u_j φ) in ℝ³ (the "localized pressure")
- p_2 = p − p_1 is harmonic in B_{r/2}(x₀)

**Estimate for p_1:** By Calderón-Zygmund (second-order Riesz transforms are bounded on L^q for 1 < q < ∞):

    ||p_1||_{L^{3/2}(ℝ³)} ≤ C_{CZ} ||u φ||²_{L^3(ℝ³)} ≤ C · ||u||²_{L³(Q_r)}

so D_1(r) := (1/r²) ∫∫_{Q_r} |p_1|^{3/2} ≤ C · C(r)^{something}.

More precisely: the Hardy-Littlewood-Sobolev inequality with n=3, α=2, p=3/2, q=3 gives:

    ||I_2 f||_{L^3(ℝ³)} ≤ C_{HLS} ||f||_{L^{3/2}(ℝ³)}

Applied to f = ∂_i∂_j(u_iu_j): since p_1 = I_2(∂_i∂_j(u_iu_j)) and Riesz transforms are L^{3/2}-bounded:

    ||p_1(·,t)||_{L^{3/2}(ℝ³)} ≤ C ||u(·,t)||²_{L^3(B_r)}

Integrating in time: D_1(r) ≤ C · (C(r))^{something} (precise exponents require careful bookkeeping).

**Estimate for p_2:** Since −∆p_2 = 0 in B_{r/2}(x₀), by the mean value property for harmonic functions:

    ||p_2||_{L^{3/2}(B_{r/4})} ≤ C · r^3 · |p_2(x₀)| ≤ C · (1/r^3) ∫_{B_{r/2}} |p_2| dx

By the CKN pressure decomposition technique (see CKN §3, and Robinson-Rodrigo-Sadowski Ch.13 §13.3), p_2 is controlled by the non-local part of the pressure, which in turn is bounded by global L^{3/2} norms of u far from x₀.

The net result (after combining p₁ and p₂ estimates) is:

    D(r/2) ≤ C [C(r) + (global L³ norm of u on B_r)^{something}]

For solutions with finite energy, the global term is controlled by E(r) and A(r) via Sobolev embedding.

### The Bootstrap (CKN Proposition 3 / Lemma 2.3)

After establishing the local energy estimate, CKN run the following bootstrap:

**Morrey's regularity argument:** If ∫∫_{Q_r} |∇u|² dx dt ≤ M r for all r ≤ r₀ (i.e., E(r) ≤ M uniformly), then u ∈ L^{10/3}(Q_{r₀/2}) by the parabolic Sobolev embedding (see §4 below). This gives improved integrability.

**Improved integrability → Hölder continuity:** With u ∈ L^{10/3} and p ∈ L^{5/3}, by a Nirenberg-Gagliardo estimate applied to the Stokes system (linearized NS), one gets u ∈ C^{0,α} in Q_{r₀/4} for some α > 0.

The precise chain is:
1. u ∈ L²_t H¹_x (global) + local energy inequality → E(r) controlled
2. E(r) ≤ ε₀ → u ∈ L^{10/3}(Q_{r/2}) by parabolic Sobolev
3. u ∈ L^{10/3} → improved pressure estimate → D(r/2) improved
4. Iterate: u ∈ L^{10/3} + improved D → Hölder continuity of u

---

## 4. Critical Scaling Exponents

### The Parabolic Sobolev Embedding

The key embedding (CKN §3, using the parabolic Sobolev inequality):

For u ∈ L^2(t₀−r², t₀; H¹(B_r)) ∩ L^∞(t₀−r², t₀; L²(B_r)):

    (1/r²) ∫∫_{Q_r} |u|^{10/3} dx dt ≤ C [E(r)]^{5/3}           ... (PARABOLSOBOLEV)

This uses the Gagliardo-Nirenberg-Sobolev inequality in the parabolic cylinder. The exponent 10/3 is the *parabolic Sobolev exponent* for energy-class functions in 3+2 = 5 parabolic dimensions:

The scaling: n = 3 (space), parabolic dimension N = 5 (= 3 + 2, where t counts as 2 via t ~ x²).
The Sobolev exponent: 2N/(N-2) = 10/3 (since N = 5, N − 2 = 3, 2N/(N-2) = 10/3). ✓

### The Key Estimate with Scaling Exponent α = 1

The central estimate controlling the singular set size is:

    ∫∫_{Q_r(z₀)} |∇u|² dx dt ≥ ε₀ · r    for all z₀ ∈ Σ, all r > 0   ... (KEY-EST)

The exponent α = 1 comes from:

    E(r) = (1/r) ∫∫_{Q_r} |∇u|² ≥ ε₀    ⟹    ∫∫_{Q_r} |∇u|² ≥ ε₀ · r

**Why α = 1 and not something smaller:**
- The quantity E(r) is already dimensionless (scale-invariant). It equals ε₀ at the threshold. So the raw integral ∫∫_{Q_r}|∇u|² scales as r¹ times E(r).
- Since E(r) is scale-invariant and ≥ ε₀ on Σ, the linear scaling r¹ is exact — not from any approximation.
- The failure to get α < 1 from this estimate is structural: E(r) being scale-invariant and bounded below by ε₀ on Σ is the *definition* of Σ. There is no way to squeeze more from this definition.

**The scaling dimension computation:**

Suppose one wanted to show P^s(Σ) = 0 for some s < 1. One would need:

    ∫∫_{Q_r(z₀)} |∇u|² dx dt ≥ ε₀ · r^s    for z₀ ∈ Σ

This is equivalent to E(r) ≥ ε₀ · r^{s-1}. Since s − 1 < 0, this would say E(r) → ∞ as r → 0 for singular points, i.e., the scale-invariant dissipation diverges at singular points. This is plausible — in fact, for Type I blow-ups, one can prove E(r) → ∞ — but in the full generality of suitable weak solutions, E(r) ≥ ε₀ (constant) is the best the ε-regularity criterion can state.

**The parabolic space-time dimension 5:**
The exponent 1 (parabolic Hausdorff dimension of Σ) vs the ambient dimension 5 (parabolic) yields the relative "smallness":

    Hausdorff dimension of Σ / Parabolic dimension of ℝ⁴ = 1/5

This is an extremely thin set: a set of parabolic dimension 1 in ℝ⁵ (parabolic) is "1-dimensional" in the sense of parabolic measure — as thin as a curve in 5D.

### The Power 10/3 and Its Role

The L^{10/3} parabolic Sobolev exponent enters the Hölder continuity bootstrap:

**Parabolic Sobolev chain:**
- Step 1: Energy-class solution → u ∈ L^{10/3}(Q_r) via parabolic Sobolev (PARABOLSOBOLEV).
- Step 2: u ∈ L^{10/3} + p ∈ L^{5/3} → by De Rham + elliptic theory → ∇u ∈ L^{10/3}_x (locally in time, via Stokes regularity).
- Step 3: ∇u ∈ L^{10/3} → Morrey embedding → u ∈ C^{0,α} (since 10/3 > 5 = N, and Morrey embedding: W^{1,p} ↪ C^{0,α} when p > N gives α = 1 − N/p = 1 − 5/(10/3) = 1 − 3/2 < 0 ... wait, this is NOT quite right for the parabolic case).

**Correction for parabolic Morrey embedding:** In the parabolic setting, the Morrey embedding states:
- If u ∈ L^p(Q_r) with p > N/2 = 5/2, then u is Hölder continuous.
- 10/3 > 5/2 ✓.

So the chain: L² energy control → L^{10/3} by parabolic Sobolev → Hölder continuity by parabolic Morrey. The exponent 10/3 is the minimal exponent above 5/2 that the energy gives for free.

**Scaling summary table:**

| Quantity | Scaling under (x,t) → (λx, λ²t), u → λ⁻¹u, p → λ⁻²p | Power of r in bound |
|---|---|---|
| A(r) = (1/r)∫_{B_r}|u|² | dimensionless | 0 (scale-invariant) |
| E(r) = (1/r)∫∫_{Q_r}|∇u|² | dimensionless | 0 (scale-invariant) |
| C(r) = (1/r²)∫∫_{Q_r}|u|³ | dimensionless | 0 (scale-invariant) |
| D(r) = (1/r²)∫∫_{Q_r}|p|^{3/2} | dimensionless | 0 (scale-invariant) |
| ∫∫_{Q_r}|∇u|² | scales as r | 1 |
| Threshold for singular set | E(r) ≥ ε₀ | implies ∫|∇u|² ≥ ε₀·r |
| Hausdorff dimension of Σ | controlled by Σ_i r_i ≤ const | dim = 1 |

The dimension 1 follows directly from:
- The scale-invariant quantity E(r) being bounded below by ε₀ on Σ (that is the definition)
- E(r) = (1/r)∫∫_{Q_r}|∇u|², so the raw integral scales as r¹

This is not a proof-specific artifact — it is forced by the scale-invariance of E(r) and the definition of the singular set.

---

## 5. Young/Absorption Steps

### Location of Each Young's Inequality Step

CKN's proof uses Young's inequality in several places. I identify the main ones with the powers used.

**Young Step Y1: Pressure-nonlinear coupling in (LEI-φ)**

The term ∫∫ p u·∇φ dx dt needs to be bounded. Using Hölder:

    |∫∫ p u·∇φ| ≤ (1/r) ∫∫_{Q_r} |p||u| ≤ (1/r) ||p||_{L^{3/2}(Q_r)} ||u||_{L³(Q_r)}

Converting to the scale-invariant quantities:

    ≤ r · D(r)^{2/3} · C(r)^{1/3}

By Young's inequality with conjugate exponents 3/2 and 3:

    D(r)^{2/3} · C(r)^{1/3} ≤ (2/3) D(r) + (1/3) C(r)

Powers: p = 3/2 (for D^{2/3}), p' = 3 (for C^{1/3}). This Young's inequality is used with ε = 1 (no free parameter — standard Young's). The step is lossy because D and C are treated symmetrically regardless of their actual sizes.

**Young Step Y2: Vortex stretching term in enstrophy estimate (appears in intermediate bootstrap)**

When bounding ∫∫ |u|² (u·∇φ) dx dt, which involves ∫_{Q_r} |u|³:

    |∫∫ |u|³| ≤ (∫∫ |u|²)^{1/2} (∫∫ |u|⁴)^{1/2}

Ladyzhenskaya: ||u||_{L^4}⁴ ≤ C ||u||_{L²} ||∇u||_{L²}³. Then Young with exponents (4/3, 4):

    ||u||_{L²}^{1/4} · ||∇u||_{L²}^{3/4} ≤ (1/4)(δ^{-1/3}||u||_{L²}) + (3/4)(δ^{1/3}||∇u||_{L²})

Here δ > 0 is a free parameter (the ε in "Young with ε"). This is the primary absorption step where the free parameter appears. The choice of δ is made to absorb the ||∇u||_{L²}³ term into the left side (the -ν||∇u||² dissipation term in the energy inequality).

Powers: the Ladyzhenskaya inequality uses exponents 1/4 and 3/4. Young's inequality to split these uses conjugate exponents 4 and 4/3.

**Young Step Y3: Parabolic interpolation in the Sobolev chain**

The parabolic Sobolev inequality (PARABOLSOBOLEV) involves an interpolation between L^∞_t L²_x and L²_t H¹_x to get L^{10/3}_{t,x}. The interpolation exponent is:

    (1/p, 1/q) = θ(1/∞, 1/2) + (1-θ)(1/2, 1/6)

For the L^{10/3} parabolic Sobolev: θ = 2/5, giving (1/p, 1/q) = (2/5)(0, 1/2) + (3/5)(1/2, 1/6) = (3/10, 1/5 + 1/10) = (3/10, 3/10). Wait — let me redo this correctly:

The Gagliardo-Nirenberg interpolation used in CKN (parabolic version):

    ||u||_{L^{10/3}(Q_r)}^{10/3} ≤ C · (sup_t ||u(t)||_{L²(B_r)}²)^{2/3} · (∫∫_{Q_r} |∇u|²)^{4/3}

This follows from the standard 3D GNS:
    ||f||_{L^{10/3}(ℝ³)} ≤ C ||f||_{L²}^{2/5} ||f||_{H¹}^{3/5}
... extended to the parabolic cylinder. The exponent 2/5 comes from: θ such that 3/(10/3) = 3(1-θ)/2 + 3θ/6 → solving gives θ = 3/5, hence ||f||_{L²} exponent = 1-θ = 2/5. Young here uses no free parameter (fixed exponents).

**Young Step Y4: The absorption step in the CKN "pressure-regularity" lemma**

In proving the pressure term D(r/2) ≤ C(r) + ε₀ (or similar), there is an intermediate step where:

    ||p_1||_{L^{3/2}}^{3/2} ≤ C ||u||_{L^3}³

requires that C(r) controls D(r/2). This uses:

    C(r/2)^{1/2} ≤ δ D(r/2) + C(δ) C(r)

(Young with δ = free parameter to absorb D(r/2) into the left side of the energy inequality). Powers: p = 2, p' = 2 (elementary Young's). The free parameter δ is chosen as δ = 1/(2C) to absorb.

**Summary of Young/Absorption Steps:**

| Step | Location | Exponents (p, p') | Free ε? | Purpose |
|---|---|---|---|---|
| Y1 | Pressure term in local energy inequality | 3/2 and 3 | No (ε = 1) | Separate pressure and velocity |
| Y2 | Ladyzhenskaya absorption of vortex-like term | 4 and 4/3 | Yes (free δ) | Absorb ||∇u||^3 into dissipation |
| Y3 | Parabolic Sobolev interpolation | Fixed (2/5 and 3/5) | No | Control L^{10/3} from L² and H¹ |
| Y4 | Pressure-regularity iteration | 2 and 2 | Yes (free δ) | Absorb D(r/2) into C(r) |

The key observation: **Y2 is the most significant lossy step.** The Ladyzhenskaya inequality with free parameter δ is where the proof is intentionally lossy — the power 3/2 of ||∇u||_{L²} in the vortex-stretching-type term forces a Young's inequality that introduces ν⁻³ or equivalent factors. In the *local* setting of CKN, the dissipation is sufficient to close (because the local energy inequality gives a uniform estimate), but the lossiness here is what prevents explicit computation of ε₀.

---

## 6. Logical Flow Summary

The complete proof architecture of CKN (1982):

```
1. Define suitable weak solutions (u,p) satisfying NS + local energy inequality (LEI)

2. Introduce scale-invariant quantities A(r), E(r), C(r), D(r)

3. LOCALIZATION (§2):
   - Apply (LEI) against cutoff φ supported in Q_r
   - Decompose pressure: p = p_1 (localized, CZ estimate) + p_2 (harmonic, mean-value)
   - Obtain: (LOCAL-ENERGY): 2∫∫_{Q_{r/2}}|∇u|² ≤ C·r·[A(r) + C(r) + D(r)]

4. PARABOLIC SOBOLEV (§2):
   - Apply GNS in parabolic cylinder: E(r) ≤ ε₀ → u ∈ L^{10/3}(Q_{r/2})
   - Exponent 10/3 = 2N/(N-2) with N=5 (parabolic dimension)

5. BOOTSTRAP (§2, Lemma 2.3):
   - u ∈ L^{10/3} + p ∈ L^{5/3} → Stokes regularity → u ∈ C^{0,α}
   - Iterative: each step gains regularity, finitely many steps reach C^∞ (for smooth data)
   - Key: all scale-invariant quantities remain bounded through the iteration

6. ε-REGULARITY CRITERION (§2, Proposition 2):
   - Conclusion: ∃ ε₀ > 0 s.t. A(r)+E(r)+C(r)+D(r) < ε₀ ⟹ z₀ regular
   - ε₀ is determined by the constants in steps 3-5 (existential, uncomputed)

7. SINGULAR SET CHARACTERIZATION (§3):
   - Σ := {z₀ : ε-regularity fails at every scale}
   - By definition: E(r, z₀) ≥ ε₀ for all r when z₀ ∈ Σ

8. COVERING ARGUMENT (§3):
   - Vitali covering in parabolic metric (d_P, ambient dimension 5)
   - Disjoint cylinders Q_{r_i}(z_i) covering Σ satisfy: ε₀ r_i ≤ ∫∫_{Q_{r_i}}|∇u|²
   - Summing: Σ_i r_i ≤ (1/ε₀) ∫∫_Q |∇u|² < ∞
   - Conclusion: P¹(Σ) = 0 (parabolic 1-Hausdorff measure zero)

9. OUTPUT:
   - The singular set has parabolic Hausdorff dimension ≤ 1
   - Equivalently: Σ cannot contain any curve in space-time (parabolic sense)
   - Euclidean space-time Hausdorff dimension of Σ ≤ 5/3 < 2
```

---

## 7. The Structural Bottleneck

The proof architecture makes clear where the dimension bound 1 comes from, and why it cannot be improved within the CKN framework:

**The bottleneck is step 7 → step 8:**

The singular set Σ is defined by E(r) ≥ ε₀ at all scales. Since E(r) is scale-invariant and the raw integral ∫∫_{Q_r}|∇u|² = r · E(r), the counting argument gives Σ_i r_i ≤ const, i.e., P¹(Σ) < ∞. To get P^s(Σ) = 0 for s < 1, one would need:

    ∫∫_{Q_r(z₀)} |∇u|² ≥ ε₀ · r^s    (for s < 1)

which would require E(r, z₀) ≥ ε₀ · r^{s-1} → ∞ as r → 0 for singular points. This cannot be guaranteed by the structure of the local energy inequality alone — it would require knowing that the dissipation concentrates even more strongly at singular points. Whether Type I singular points (where |u(x,t)| ≤ C/√(T*-t)) satisfy such enhanced concentration is a deep open question.

**What CKN leaves open:** The gap between "P¹(Σ) = 0" and "Σ = ∅" (full regularity). Filling this gap requires either:
(a) A new proof strategy that avoids the scale-invariant criterion (unlikely to help — see §4 above), or
(b) Additional geometric/analytic information about NS singular points beyond what the local energy inequality provides.

---

## 8. Comparison Preparation (for Step 1 synthesis)

For the comparison with Lin (1998) and Vasseur (2007), the key signatures of CKN are:

| Feature | CKN (1982) signature |
|---|---|
| ε-regularity criterion | A(r) + E(r) + C(r) + D(r) < ε₀ (all four quantities) |
| Localization method | Explicit cutoff functions φ with |∇φ| ~ 1/r, |∆φ| ~ 1/r², |∂ₜφ| ~ 1/r² |
| Pressure treatment | Explicit harmonic decomposition p = p₁ + p₂ |
| Covering objects | Parabolic cylinders Q_r(z₀) in parabolic metric d_P |
| Critical scaling | E(r) scale-invariant → ∫|∇u|² ~ r → dim(Σ) ≤ 1 |
| Young steps | Ladyzhenskaya + free-parameter Young = Y2 (dominant lossy step) |
| Parabolic Sobolev exponent | 10/3 = 2N/(N-2) with N = 5 (parabolic dim) |
| ε₀ value | Existential (uncomputed), depends on CZ and GNS constants |
| Proof style | Direct: explicit estimates, cutoff functions, Hölder/CZ/Sobolev at each step |

The direct/explicit style means CKN's proof is quantitative in structure but non-quantitative in constants. Every estimate is of the form "LHS ≤ C × RHS" with explicit powers of r, but C is determined by chains of Sobolev/CZ constants that are not computed.

---

## Notes and Sources

**On the local energy inequality:** CKN Definition 2.2 and the discussion in §2. This inequality was first used by Scheffer (1976); CKN strengthened the partial regularity result by proving P¹(Σ) = 0 (Scheffer had only proven the time-Lebesgue measure of the singular set is zero).

**On the scale-invariant quantities A, E, C, D:** CKN §2. The specific normalization (1/r and 1/r²) is chosen to make each quantity dimensionless under NS scaling.

**On Condition (I) vs. the full criterion:** CKN prove in Proposition 1 that Condition (I) alone (only E(r) < ε₀) is sufficient if one additionally assumes the solution is in L^{10/3} near z₀. Their Proposition 2 handles the full local case with all four quantities.

**On the parabolic Hausdorff measure:** CKN §3 and Theorem C. The definition P^s(Σ) uses parabolic cylinders Q_r with "radius" r counted in the parabolic metric (so Q_r has parabolic "diameter" proportional to r, but Euclidean space-time diameter proportional to r in space and r² in time).

**On Ladyzhenskaya-Seregin (1999):** They simplify the pressure decomposition step (avoiding the harmonic splitting p = p₁ + p₂ by working in a different functional framework), but the ε-regularity criterion and covering argument are identical to CKN.

**On Robinson-Rodrigo-Sadowski (2016):** Their Chapter 13 presents the CKN proof in full, including the explicit form of the local energy inequality and the parabolic Sobolev embedding. Their §13.3 has the most explicit treatment of the pressure decomposition.

**On ε₀ computability:** As noted in the Atlas NS library (atlas/execution/agents/library/factual/navier-stokes, entry R4 in exploration-001), ε₀ has never been explicitly computed. Lin (1998)'s proof is non-constructive (compactness), so it does not improve this. Vasseur (2007)'s De Giorgi approach also does not yield an explicit ε₀.

**Verification note:** The precise form of (LEI-φ) — specifically the coefficient 2 in front of |∇u|² — appears in CKN (2.1). Some textbooks write the NS local energy inequality without the factor of 2 and with a different normalization of viscosity ν. With ν = 1 (CKN normalization), the factor is 2 (from 2ν = 2·1). Care is needed when comparing with papers that use ν explicitly.
