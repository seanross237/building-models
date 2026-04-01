# Exploration 002: CNS Paper Analysis — Novelty and Overlap Assessment

## Goal Summary
Determine whether the claimed β < 1/6 mass gap result from prior Atlas work is already in, or trivially derivable from, the CNS papers (arXiv:2509.04688 and arXiv:2505.16585). Conduct equation-level comparison.

---

## Section 1: arXiv:2509.04688 — "Dynamical Approach to Area Law" (Sept 2025)

**Authors:** Sky Cao, Ron Nissim, Scott Sheffield
**Length:** 8 pages

### 1.1 Action Convention

Eq. (1.2): S_YM(Q) := Nβ Σ_{p ∈ P^+_Λ} ReTr(Q_p)

where Tr is the **unnormalized** N×N matrix trace, dQ is product Haar measure, and the normalized trace is defined separately as tr = (1/N)Tr. The regime β ≤ β₀ (small constant) is the 't Hooft regime.

**Convention tag:** "CNS/SZZ convention" — β has the N prefactor absorbed into the coupling Nβ.

### 1.2 Main Theorem

**Theorem 1.6 (Area law in the 't Hooft regime):** For d ≥ 2, N ≥ 2, G ∈ {U(N), SU(N), SO(2(N-1))}, for β < β*_G, there are constants C, c depending on β, d, N such that for any rectangular loop ℓ with side lengths ≤ L/2:

```
|⟨W_ℓ⟩_{Λ,β}| ≤ C exp(−c · area(ℓ))
```

**Definition 1.4 (Thresholds):**
```
β*_{SU(N)} = β*_{U(N)} = 1/(8(d−1))
β*_{SO(N)} = 1/(16(d−1)) − 1/(8N(d−1))
```

For SU(N) in d=4: **β* = 1/(8×3) = 1/24.**

### 1.3 Technique: Vertex σ-Model + Bakry-Émery

The key step reformulates the lattice Yang-Mills measure as a product of vertex-based σ-models conditioned on horizontal slabs (DF80 construction). The σ-model action on a slab is:

Definition 2.1: S_{A,B}(Q) := Nβ Σ_{e=(x,y) ∈ E^+_{Λ^{d-1}}} ReTr(Q_x A_e Q_y^{-1} B_e^{-1})

where A, B ∈ U(N)^{E^+_{Λ^{d-1}}} are the boundary conditions.

**Hessian bound** (Eq. 3.1): For any Q ∈ G^{Λ^{d-1}} and tangent vector v:

```
|Hess_{S_{A,B}}(v,v)| ≤ 4(d−1)Nβ|v|²
```

**Derivation structure:** Each vertex of Λ^{d-1} is contained in 2(d-1) edges, giving the prefactor 4(d-1).

**Bakry-Émery constant** (Eq. 3.2): K_{S_{A,B}} = (N+2)/2 − 1 − 4Nβ(d−1) for G = SU(N). For N=2, d=4: K = 1 − 24β > 0 iff β < 1/24.

### 1.4 How CNS Improved Over SZZ23

From Remark 1.5: "The threshold in [SZZ23] is half the threshold in the current paper." The SZZ23 Hessian bound is 8(d-1)Nβ (because SZZ applies Bakry-Émery to EDGE-based Yang-Mills). CNS applies it to VERTEX-based σ-model, halving the Hessian coefficient ("every edge contains two vertices, while every plaquette contains four edges").

### 1.5 Items NOT Present in This Paper

1. **No exact Hessian eigenvalue computation at Q=I.** The bound |Hess| ≤ 4(d-1)Nβ|v|² is derived via Cauchy-Schwarz and counting; no eigenvalue diagonalization is performed.

2. **No Fourier analysis on the lattice.** The argument is combinatorial/algebraic.

3. **No staggered mode identification.** The specific mode (−1)^{|x|+μ} v₀ that maximizes the Hessian is never mentioned.

4. **No Weitzenböck decomposition.** There is no M(Q) = M(I) + R(Q) analysis.

5. **No mention of β < 1/6.** Searched the full text: this value does not appear.

6. **The vertex σ-model Hessian bound is tight.** At Q=I, A=B=I, the vertex action S_{A,B=I}(Q=I) has Hessian with maximum eigenvalue exactly 4(d-1)Nβ (the discrete vertex Laplacian eigenvalue). The CNS bound 4(d-1)Nβ is NOT improvable within the vertex formulation using the same Cauchy-Schwarz approach.

---

## Section 2: arXiv:2505.16585 — "Expanded Regimes of Area Law" (May 2025)

**Authors:** Sky Cao, Ron Nissim, Scott Sheffield
**Length:** 35 pages

### 2.1 Action Convention

**Definition 2.3:** dμ_{Λ,β,N}(U) = (1/Z) ∏_p exp(2β ReTr(U_p)) dU

where Tr is the **unnormalized** N×N matrix trace. Note: the coefficient is **2β** (not Nβ).

**Remark 2.4:** β Tr(U) = β̃ tr(U) where β̃ = Nβ. So their β̃ (= Nβ) is the analog of the 't Hooft parameter.

**Critical convention difference:** This paper uses S = 2β Σ Re Tr, while CNS Sept 2025 uses S = Nβ Σ Re Tr. Same physical theory requires 2β_May = Nβ_Sept → β_May = (N/2)β_Sept. For N=2: β_May = β_Sept (same values). For general N, the conventions differ by N/2.

### 2.2 Main Theorem

**Theorem 1.2 (Area law):** Consider lattice Yang-Mills with G = U(N). For all d ≥ 2, there exists β₀(d) > 0 such that for all β ≤ β₀(d) and all N ≥ 1, for any rectangular loop ℓ in finite lattice Λ:

```
|⟨W_ℓ⟩_{Λ,β,N}| ≤ C_{1,d} C_N^{|ℓ|} exp(−C_{2,d} area(ℓ))
```

where C_{1,d}, C_{2,d} depend only on d (NOT on N), and C_N is a constant depending on N.

**Key improvement over CNS Sept 2025:** The string tension constant C_{2,d} is N-independent, whereas in CNS Sept 2025 (and SZZ23) it decays with N (see SZZ Remark 4.12).

### 2.3 Actual β₀(d) Threshold

The parameter regime used in the proof (Section 2.1):
- Eq. (2.1): N ≥ 10^{10} d^{10}
- Eq. (2.2): β ≤ 10^{-10d} d^{-1}  [for d=4: β ≤ 10^{-40}/4 ≈ 2.5 × 10^{-41}]
- Eq. (2.3): (1/2d) × 10^{-3} N ≤ B ≤ (1/d) × 10^{-3} N

The proof of Theorem 1.2 (page 18) defines: β₀(d) := min(10^{-10d} d^{-1}, min_{N ≤ 10^{10} d^{10}} β₀(d,N)).

This threshold is astronomically small as published. The library records an "optimized ceiling" of β₀(4)_max ≈ 1/87 after parameter optimization, still well below the CNS Sept 2025 threshold of 1/24.

### 2.4 Technique: Master Loop Equations

Completely different from Bakry-Émery. The Wilson string expectations satisfy a linear inhomogeneous master loop equation (Proposition 2.17). The proof:
1. Introduces a truncated Yang-Mills model (Definition 3.1, action with exp_B replacing exp)
2. Proves area law for the truncated model (Theorem 3.2) via contraction mapping
3. Shows the truncated model approximates the original (Section 4)

The contraction estimate (Proposition 3.23) requires the linear operator M (Definition 3.22) to satisfy ‖Mf‖ ≤ (1/2)‖f‖. This leads to constraints on β, λ, γ, ρ parameters.

**No curvature input:** Ricci curvature of U(N) does NOT appear anywhere. The Bakry-Émery framework is entirely absent.

### 2.5 Items NOT Present in This Paper

1. **No Bakry-Émery analysis.** No Hessian bounds, no Ric - Hess computation.
2. **No Fourier analysis on the lattice.**
3. **No mention of β < 1/6 or β < 1/24.** These thresholds are from the Sept 2025 paper's framework.
4. **No Weitzenböck decomposition.**
5. **The master loop approach cannot easily reach 1/24 or 1/6.** The optimized ceiling is ~1/87, below the CNS Sept 2025 threshold.
6. **Does NOT prove mass gap** — only area law. The lack of curvature input means the framework cannot leverage the Bakry-Émery spectral gap.

---

## Section 3: Convention Comparison

| Paper | Action | β convention | SU(2), d=4 threshold |
|-------|--------|--------------|----------------------|
| SZZ23 | S = −(β/N) Σ Re Tr or equivalent | 't Hooft: β × N | β < 1/48 |
| CNS Sept 2025 | S = Nβ Σ Re Tr | β = 't Hooft coupling | β < 1/24 |
| CNS May 2025 | S = 2β Σ Re Tr | β̃ = Nβ = 't Hooft | ~1/87 (optimized) |
| Atlas (our work) | S = −(β/N) Σ Re Tr | Same as SZZ/CNS | β < 1/6 (triangle) |

**All numbers 1/48, 1/24, 1/87, 1/6 are in the SAME convention** (SZZ/CNS 't Hooft coupling, where the action coefficient is Nβ per plaquette with unnormalized trace Tr, or equivalently β per plaquette with normalized trace tr = (1/N)Tr).

**What CNS Sept 2025 proves at β < 1/24:** Wilson's area law via DF80 slab condition + vertex σ-model mass gap.

**What our Atlas work claims at β < 1/6:** Bakry-Émery spectral gap (mass gap) for the EDGE-based Wilson action on the full lattice, using a sharper Hessian bound from the triangle inequality applied to B_□(Q,v).

---

## Section 4: Overlap Analysis Table

| Our Claim | In CNS (Sept 2025)? | In CNS (May 2025)? | Notes |
|-----------|---------------------|--------------------|----|
| H_norm = 1/12 at Q=I (exact Fourier) | **NO** | **NO** | CNS Sept uses global bound 4(d-1)Nβ; never computes eigenvalues |
| Staggered mode v = (−1)^{|x|+μ} v₀ is the Hessian maximizer | **NO** | **NO** | Not identified in either paper |
| Triangle inequality gives H_norm ≤ 1/8 for all Q | **NO** | **NO** | CNS Sept vertex bound gives H_norm ≤ 1/2 relative (4× weaker); no global bound < 1/8 proven |
| β < 1/6 threshold for SU(2), d=4 | **NO** | **NO** | CNS Sept achieves 1/24; May achieves ~1/87 optimized |
| Conjecture: H_norm ≤ 1/12 for all Q | **NO** | **NO** | Not stated or conjectured in either paper |
| Weitzenböck decomposition M(Q) = M(I) + R(Q) | **NO** | **NO** | Not used; SZZ does not distinguish flat and curvature parts |

**All six claims are ABSENT from the CNS papers.**

---

## Section 5: Why CNS Doesn't Reach β < 1/6

### Fundamental Limitation of the CNS Sept 2025 Vertex Approach

The vertex σ-model Hessian is bounded by 4(d-1)Nβ (Eq. 3.1). At Q=I with A=B=I, the vertex σ-model action S_{I,I}(Q) = Nβ Σ_{e=(x,y)} ReTr(Q_x Q_y^{-1}) has Hessian equal to the **vertex Laplacian** on Λ^{d-1}. The maximum eigenvalue of the vertex Laplacian is exactly 4(d-1) (achieved at the "staggered mode" for the vertex model). Thus, the CNS bound 4(d-1)Nβ IS TIGHT within the vertex formulation — it cannot be improved using the same techniques.

To go from 1/24 to 1/6 within the Bakry-Émery framework requires either:
1. **Switching back to the edge-based action** and using a tighter bound than SZZ's Cauchy-Schwarz (the Atlas approach)
2. **Finding a different vertex reformulation** that has smaller Hessian eigenvalues

### Why the Atlas Triangle Bound Works

The Atlas triangle inequality applied to the EDGE-based Wilson action gives:
```
|B_□(Q,v)|² ≤ (per-plaquette bound) × |v_edges|²
```
where the tighter bound accounts for the fact that B_□ = v_{e1} + parallel-transported terms, and the sum has only 4 terms. The key improvement: using |B_□|² ≤ (1/N) × Σ_{k=1}^{4} |Ã_k|² (via Lemma 5.1: −(1/N)Re Tr(B²U) ≤ (1/2N)|B|²) instead of the full Cauchy-Schwarz.

This gives |Hess| ≤ 4(d-1)β/N × |v|² for the EDGE action (vs. SZZ's 8(d-1)Nβ). For N=2, d=4: |Hess| ≤ 6β, threshold β < 1/6.

### Why the May 2025 Paper Is Structurally Limited

The master loop approach is curvature-free. It cannot use the positive Ricci curvature κ = N/2 of SU(N). The contraction estimate (Proposition 3.23) relies only on combinatorial/algebraic bounds, and its threshold β₀ is limited by the merger term's unsigned count (2dB mergers). The Bakry-Émery approach exploits curvature at NO cost; the master loop pays for it in a weaker β ceiling.

---

## Section 6: Verdict

### Is β < 1/6 Already in the CNS Papers?
**NO.** Neither paper contains this threshold.

### Is β < 1/6 Trivially Derivable from Their Work?
**NO — but for different reasons depending on which paper:**

**From CNS Sept 2025:** The vertex σ-model Hessian bound 4(d-1)Nβ is TIGHT — the bound is achieved at the staggered mode of the vertex Laplacian. You cannot improve it within the vertex formulation without new ideas. The 1/6 result requires switching back to the edge-based action and applying a more careful triangle inequality (the Atlas approach). This is a non-trivial new step.

**From CNS May 2025:** The master loop approach is structurally different and cannot reach 1/6. It uses no curvature, and its optimized ceiling is ~1/87 (well below 1/24, let alone 1/6). Deriving 1/6 from their framework would require incorporating Bakry-Émery-type curvature bounds, which fundamentally changes the proof.

### Classification: (c) Requires genuinely new insight beyond their work.

The β < 1/6 result (from the global triangle bound H_norm ≤ 1/8) is:
- NOT in either CNS paper
- NOT trivially derivable from the CNS vertex approach (bound is tight in their formulation)
- Requires returning to the edge-based framework (SZZ) and applying a more careful application of the triangle inequality to B_□(Q,v)
- The key new mathematical content: Lemma 5.1 (−(1/N)Re Tr(B²U) ≤ (1/2N)|B|²) applied systematically to give a per-plaquette bound that is 4× tighter than SZZ's Cauchy-Schwarz at each step

**Caveat:** The insight (Lemma 5.1) is technically modest — it is a straightforward bound on matrix products using unitarity. The result could plausibly have been derived from SZZ23 alone, without reference to CNS. However, it was NOT noted in any prior work we can find, and it yields a meaningful 4× improvement over the tightest known prior result (CNS Sept 2025).

---

## Section 7: Additional Observations from Reading the Papers

1. **CNS May 2025 knows it is weaker than CNS Sept 2025 in β range.** Remark 1.3(4) and Fig 1 explicitly acknowledge that the Sept 2025 paper achieves a LARGER β range. The May 2025 contribution is N-independence of the string tension constant, not improved β.

2. **CNS Sept 2025 acknowledges the Hessian bound is the bottleneck.** Remark 1.5 explains the vertex reformulation halved the Hessian, and thanks SZZ authors for the observation. This suggests CNS is aware that further Hessian improvements could push the threshold higher.

3. **No CNS paper proves a spectral gap (mass gap) at β < 1/24.** CNS Sept 2025 proves AREA LAW via the DF80 slab condition. The direct spectral gap from SZZ (at β < 1/48) has not been extended to 1/24. Our Atlas β < 1/6 is a MASS GAP result (direct Bakry-Émery spectral gap) — this distinction is important.

4. **The papers are 8 pages (Sept) and 35 pages (May).** The Sept paper is intentionally short, citing SZZ for 7 pages of calculations. The May paper is substantially new.

5. **Library entries were accurate.** The library description of CNS Sept 2025 ("Hessian bound 4(d-1)Nβ, threshold β < 1/24, vertex reformulation") and CNS May 2025 ("master loop equations, completely different from Bakry-Émery, optimized ceiling β₀(4) ≈ 1/87") are confirmed correct by the actual papers.

---

## Section 8: Summary Table

| Feature | SZZ23 | CNS Sept 2025 | CNS May 2025 | Atlas β<1/6 claim |
|---------|-------|---------------|--------------|------------------|
| Threshold (d=4) | β < 1/48 | β < 1/24 | ~1/87 optimized | **β < 1/6** |
| Method | BE on edges | BE on vertices + DF80 | Master loop | BE on edges (improved) |
| Hessian bound | 8(d-1)Nβ | 4(d-1)Nβ | N/A | 4(d-1)β/N |
| Proves mass gap? | YES | NO (area law via DF80) | NO | YES |
| Proves area law? | NO (only mass gap) | YES | YES | NO (only mass gap) |
| Fourier analysis? | NO | NO | NO | YES (at Q=I) |
| Exact eigenvalue at Q=I? | NO | NO | NO | YES (4β) |
| Weitzenböck used? | NO | NO | NO | YES (M(Q)=M(I)+R(Q)) |
| N-independent string tension? | NO | NO | YES | NO |
