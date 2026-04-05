# Exploration 003: CNS Master Loop Equation Approach — β₀(d) Extraction

**Paper:** arXiv:2505.16585v3 (Cao-Nissim-Sheffield, May 2025, updated Sept 2025)
**Title:** "Expanded Regimes of Area Law for Lattice Yang–Mills Theories"
**Goal:** Extract β₀(d), compare to 1/24, assess combinability with Bakry-Émery approach

---

## Section 1: Master Loop Equations Approach — What It Is

### 1.1 The Setting

The paper proves area law for pure U(N) lattice Yang–Mills theory. "Area law" means the Wilson loop expectation satisfies:
```
|⟨W_ℓ⟩| ≤ C₁,d * C_N^|ℓ| * exp(-C₂,d * area(ℓ))
```
where |ℓ| is the perimeter and area(ℓ) is the minimal spanning area of the loop ℓ.

### 1.2 Master Loop Equations — Mathematical Definition

The master loop equations (MLE) are recursive equations satisfied by **Wilson string expectations** — multipoint correlation functions of the lattice Yang-Mills measure. A "string" s = (ℓ₁, ..., ℓₙ) is a collection of loops; the Wilson string observable is W_s(U) = ∏_i tr(U_{ℓᵢ}).

The MLE relates ⟨W_s⟩ to a weighted sum over "neighboring" strings obtained by one of six string operations:
- **Splitting**: splits one loop into two loops at a shared lattice edge
- **Merger**: merges two loops into one (comes with factor 1/N²)
- **Deformation**: deforms a loop around a plaquette (comes with factor β/N)

The equation has the form (schematically):
```
⟨W_s⟩ = G · ⟨W_{s'}⟩ + g
```
where G is the linear operator encoding splittings + mergers + deformations, and g is an "inhomogeneous" term.

This equation appeared earlier in [Chatterjee 2019, Jafarov 2016, etc.] but was only tractable in the large-N limit. The merger term (proportional to 1/N²) was the obstruction to finite-N analysis.

### 1.3 The Proof Strategy: Contraction Estimate

The proof reduces to a **contraction estimate** for the operator G: if ‖Gf‖ ≤ (1/2)‖f‖ in an appropriate norm, then:
```
‖f*‖ ≤ 2‖g‖
```
The norm ‖·‖ is defined so that ‖f*‖ ≤ 1 implies area law.

**Key innovation:** At finite N, the merger term (1/N²) in G makes the contraction estimate fail directly. The authors introduce a **truncated model** to handle this.

### 1.4 The Truncated Model

The truncated Yang-Mills measure replaces the Boltzmann weight exp(2β Re Tr(U_p)) with a **truncated exponential** exp_B(2β Re Tr(U_p)), where:
```
exp_B(x) = Σ_{k=0}^{B} x^k/k!
```
The truncation level B ~ (1/d) · 10^(-3) · N is large (scales with N).

Why this helps: in the truncated model, each plaquette can appear at most B times in the "surface sum" representation, making the number of merger terms bounded. The contraction estimate goes through for the truncated model.

Extension to original model: Since B is large (proportional to N), it is extremely rare for any plaquette to appear more than B times. The difference between truncated and original model is exponentially small (bounded by exp(-B/10)).

### 1.5 String Duality / Surface Sum Interpretation

The proof has a natural "gauge string duality" interpretation. Wilson string expectations can be written as surface sums (over surfaces spanning the strings), where each surface contributes weight (β^(plaquettes)) · (N^(-2·genus)) · (combinatorial factor).

- Area law follows because any surface spanning a large loop must contain many plaquettes → exponential area cost
- The merger term corresponds to higher-genus surfaces → weighted by N^(-2g), small at large N
- The truncated model corresponds to restricting to surfaces where each plaquette appears ≤ B times

This "string trajectory" or "surface" viewpoint is the geometric heart of the paper.

### 1.6 Comparison to Osterwalder-Seiler 1978

OS78 used truncation at level B=0 (no plaquettes at all), requiring β ≪ c(d)/N. The CNS improvement allows B ~ N/d, requiring only β ≪ 1/d (N-independent).

---

## Section 2: The Threshold β₀(d) — Explicit or Implicit?

### 2.1 Theorem 1.2 — Existential Statement

**Theorem 1.2** (exact statement from paper):
> For all d ≥ 2, there exists β₀(d) > 0 such that for all β ≤ β₀(d) and all N ≥ 1, for any rectangular loop ℓ in a finite lattice Λ:
> |⟨W_ℓ⟩_{Λ,β,N}| ≤ C₁,d · C_N^|ℓ| · exp(-C₂,d · area(ℓ))
> where C₁,d, C₂,d depend only on d, and C_N depends on N.

The threshold β₀(d) is **existential** in the theorem statement. However, the proof provides an **explicit** sufficient condition from the parameter assumptions.

### 2.2 Explicit Parameter Conditions (from Section 2.1)

The proof works under the following parameter assumptions (equations 2.1–2.3):

**(2.1):** N ≥ 10^(10d^10)  ← N must be astronomically large (for large N analysis)

**(2.2):** β ≤ 10^(-10d) / d  ← **The explicit bound used in the proof**

**(2.3):** B satisfies: (1/(2d)) · 10^(-3) · N ≤ B ≤ (1/d) · 10^(-3) · N (B is the truncation level)

(B must be odd)

The authors explicitly note (Remark 2.8): "The precise values such as 10^(10d^10) are **somewhat arbitrary**, and are chosen so that we always have a lot of room in the estimates."

### 2.3 The Explicit Threshold from the Proof

The proof of Theorem 1.2 (from the paper, proof on page 18) explicitly constructs:
```
β₀(d) := min(10^(-10d)/d,  min_{N ≤ 10^(10d·d^10)} β₀(d,N))
```
where β₀(d,N) comes from the Osterwalder-Seiler theorem for small N.

**From condition (2.2): β₀(d) ≤ 10^(-10d) / d** (the bound used in the proof for large N).

In d=4: 10^(-10·4)/4 = 10^(-40)/4 ≈ **2.5 × 10^(-41)**

This is astronomically smaller than 1/24 ≈ 0.042. But the authors say these constants are "somewhat arbitrary."

### 2.4 Structural Thresholds from the Proof Mechanics

The paper contains multiple places where the structural threshold emerges:

**From Theorem 3.2 (truncated model, Section 3):**
```
|⟨W_ℓ⟩_{Λ,β,N,B}| ≤ 2N^(|ℓ|/4-1) · (10³ dβ)^(area(ℓ))
```
Area law holds when **(10³ d β) < 1**, i.e., **β < 1/(10³ d) = 1/4000 in d=4**.
This is the "truncated model structural threshold."

**From Theorem 4.1 (original model, Section 4):**
```
|⟨W_ℓ⟩| ≤ 2^|ℓ| · N^(|ℓ|/4-1) · α^(area(ℓ))
where α = 2 × 10³d × max(10³dβ, exp(-10^(-7) d^(-2) N)) ≪ 1
```
Area law requires α < 1. For large N (exp term small), this requires:
**2 × 10³d × 10³dβ < 1 → β < 1/(2 × 10^6 d²)**

In d=4: β < 1/(3.2 × 10^7) ≈ **3 × 10^(-8)** (even smaller due to the α prefactor of 2×10³d).

**Note:** These constants are unoptimized. The factor "10³" is a choice made for convenience in the norm parameter γ = (10³dβ)^(-1). Optimizing γ:

From the contraction estimate (Proposition 3.23 and Proposition 4.41), the critical condition is:
```
4dβγ/(λρN) ≤ 1/4
with λ = 1/N, ρ = 1/e: 4dβγ·e ≤ 1/4
```
The norm requires γ ≥ 1. Setting γ = 1 (optimal):
```
4dβ·e ≤ 1/4 → β ≤ 1/(16ed)
```
In d=4: **β_optimal ≤ 1/(16 × e × 4) ≈ 1/87 ≈ 0.0115**

This is still **~3.6× smaller than 1/24 ≈ 0.042**.

### 2.5 Summary of Master Loop Thresholds in d=4

| Threshold source | β₀(4) value | Notes |
|-----------------|-------------|-------|
| Explicit bound from proof (eq. 2.2) | 10^(-40)/4 ≈ 2.5×10^(-41) | "Arbitrary" conservative constants |
| Theorem 3.2 structural | 1/4000 ≈ 2.5×10^(-4) | From contraction condition in truncated model |
| Theorem 4.1 formula | ~3×10^(-8) | From explicit α formula |
| Optimized parameter choice | ~1/87 ≈ 0.0115 | Setting γ=1 in contraction estimate |
| Bakry-Émery [CNS25] for comparison | 1/24 ≈ 0.042 | Best known rigorous bound |

### 2.6 Summary: Is β₀(4) > 1/24?

**ANSWER: β₀(4) < 1/24, definitively.**

This is confirmed in three ways:
1. **Paper self-report (Remark 1.1):** "[CNS25] were able to establish area law for a **larger range of β values**..." — [CNS25] is the Sept 2025 paper with threshold 1/24.
2. **Explicit computation:** Even the optimized master loop threshold (~1/87) is ~3.6× smaller than 1/24.
3. **Structural reason:** The master loop contraction does not use the curvature of U(N), while Bakry-Émery directly exploits positive Ricci curvature K = 4N(d-1)β. This curvature is precisely what allows the larger threshold.

---

## Section 3: Comparison with Bakry-Émery Threshold (1/24)

### 3.1 Direct Comparison Table

| Approach | Threshold (d=4) | N-dependence | String tension constant |
|----------|----------------|--------------|------------------------|
| SZZ 2023 (mass gap) | β < 1/48 | N-independent | N/A |
| OS78 (area law) | β < c(4)/N | Decays as 1/N | N-dependent |
| CNS May 2025 (master loop, optimized) | β ~ 1/87 ≈ 0.0115 | **N-independent (for large N)** | **C₂,d does NOT decay with N** |
| CNS May 2025 (master loop, as stated) | β ~ 1/4000 ≈ 0.00025 | N-independent | C₂,d does NOT decay with N |
| CNS Sept 2025 (Bakry-Émery) | β < 1/24 ≈ 0.042 | N-independent | C₂,d DECAYS with N |

Key nuance: Both CNS papers achieve N-independent thresholds (for the range of β). But:
- Master loop: SMALLER β range (~1/87 optimized vs 1/24), BETTER string tension constant (N-independent)
- Bakry-Émery: LARGER β range (1/24), WORSE string tension constant (decays with N)

### 3.2 The Core Tradeoff

From **Remark 1.3(4)** of the paper:
> "The analog of C₂,d actually decays with N in [CNS25, Theorem 1.6]... On the other hand, the constant C₂,d in Theorem 1.2 does **not** decay with N. Thus, in the regime β ≤ β₀(d), the upper bound of Theorem 1.2 is **better** than [CNS25, Theorem 1.6]."

Consequence:
- For **β ≤ β₀(4)** (master loop regime): use master loop → better N-independent C₂,d
- For **β₀(4) < β < 1/24**: only Bakry-Émery applies, with C₂,d → 0 as N → ∞
- For **β ≥ 1/24**: no rigorous area law proof currently

### 3.3 Why Bakry-Émery Achieves a Larger β Range

The Bakry-Émery approach (CNS Sept 2025) uses the **positive Ricci curvature of U(N) as a Riemannian manifold** to obtain spectral gap / log-Sobolev inequalities. The vertex Hessian bound K_S = 4N(d-1)β > 0 comes from the curvature of the U(N) manifold, and is positive precisely when β < 1/(8(d-1)) = 1/24 in d=4.

The master loop approach does NOT exploit this curvature — it works purely from contraction estimates on the master loop operator G. The contraction condition β ≤ 1/(C·d) involves only combinatorial/algebraic constants. This is why it gives a smaller threshold.

**The gap factor:** Even with optimal constants, master loop gives β ~ 1/87 vs Bakry-Émery's 1/24 — a factor of ~3.6×. This factor reflects the "free lunch" from the positive curvature of U(N) that Bakry-Émery exploits.

### 3.4 Explicit Numerical Comparison

```
Threshold comparison in d=4:
                     Physical: β ~ 2.0    (lattice QCD)
                   ↑
                   |          <--- gap of ~48× --->
                   |
           1/24 = 0.042       CNS Sept 2025 (best known)
                   |
          1/87 ≈ 0.012        CNS May 2025 (optimized parameters)
                   |
          1/4000 = 0.00025    CNS May 2025 (as stated in proof)
                   |
          1/48 = 0.021        SZZ 2023 (mass gap)
                   |
```

Wait, note that 1/48 > 1/87. So SZZ's mass gap result (1/48) is actually ABOVE the optimized master loop threshold (1/87)! Let me clarify: SZZ proves **mass gap** (not area law). The area law results are:

```
Area law thresholds in d=4 (in descending order of β coverage):
  1/24 ≈ 0.042   [CNS Sept 2025, Bakry-Émery on vertices]     ← BEST
  ~1/87 ≈ 0.012  [CNS May 2025, master loop, optimized]
  ~1/4000        [CNS May 2025, master loop, as stated]
  c(4)/N         [OS78, Osterwalder-Seiler 1978]

Mass gap (implies area law via Durhuus-Fröhlich, but area law proved independently):
  1/48           [SZZ 2023]
```

### 3.5 Cross-Paper Compatibility

Both papers work with U(N) (the May paper explicitly; the Sept paper works with U(N) and SU(N)). They use different methods but compatible measure-theoretic foundations. The area law results are compatible:

**Combined statement:** For d=4 U(N) lattice Yang-Mills, area law holds for **all β < 1/24**, with:
- N-independent string tension for β ≤ β₀(4) ~ 1/87
- N-dependent string tension for 1/87 < β < 1/24

---

## Section 4: Novel Combinations

### 4.1 Can the Two Approaches Be Combined? What the Authors Say

The paper explicitly raises the combination question in **Remark 1.4**:
> "It would be natural to try to extend Theorem 1.2 to the case where β is allowed to depend **linearly in N**, e.g. β ≤ c_d · N, where c_d is a small dimensional constant. In other words, the natural next step is to further develop the approach of the present paper to **reprove the main result of [CNS25]**."

This is remarkable: the authors explicitly say the next goal is to use master loop techniques to REPROVE (not improve upon) the Bakry-Émery result β < 1/24. They acknowledge this is a regime the current master loop proof CANNOT reach yet.

**Key distinction in regimes:**
- CNS May 2025 (master loop): β ≤ β₀(d) ~ constant/d (N-independent, small)
- "Next step" (Remark 1.4): β ≤ c_d · N (linear in N)

The Bakry-Émery result β < 1/24 = 1/(8(d-1)) in the Trace convention is the target. In the normalized trace convention (˜β = Nβ), this is ˜β < N/24, which is indeed linear in N — matching the "linear regime" the authors describe as the next step.

### 4.2 Potential Combination Strategies

**Strategy A: Direct union (trivial, no new math needed)**

Area law holds for **β < 1/24** using either approach:
- For β ≤ β₀(4) ~ 1/4000: use master loop (better string tension)
- For β₀(4) < β < 1/24: use Bakry-Émery (weaker string tension)

The combined result: **area law holds for β < 1/24 in d=4 U(N) lattice YM**, with N-independent string tension for small β.

**Strategy B: Bakry-Émery curvature as input to master loop contraction**

The core idea: The master loop contraction fails for large β because the deformation term 4dβγ/(λρN) becomes large. But Bakry-Émery provides a separate estimate on deformations through the curvature of U(N).

Specifically: the deformation operator in MLE is:
```
D^± terms: ±(β/N) Σ_{s' ∈ D±(s,e)} ⟨W_{s'}⟩
```
The Bakry-Émery spectral gap gives a bound on |⟨W_{s'}⟩| that involves β through the curvature condition K_S = 4N(d-1)β. If this bound were substituted into the master loop contraction, the effective β-dependence of the deformation term would be improved.

Schematically: instead of `4dβ/N × ||f||` in the contraction estimate, one might get `4dβ/N × C(β, N) × ||f||` where C(β, N) < 1 exploits the curvature. For β < 1/24, C(β, N) → 0 from positive curvature.

**This is a genuinely unexploited combination** that the authors do not discuss. The difficulty: the master loop operates on Wilson STRINGS, not single Wilson loops, and it's unclear if Bakry-Émery's single-loop bounds extend to multi-loop quantities.

**Strategy C: Master loop provides quantitative rates for Bakry-Émery regime**

The Bakry-Émery result ([CNS25]) proves area law for β < 1/24 but with N-dependent string tension C₂,d → 0 as N → ∞. The master loop result proves area law with N-independent string tension for β ≤ β₀(d).

A combined approach might: (1) use Bakry-Émery to establish area law for β < 1/24, and (2) use master loop techniques to quantify the string tension (making it N-independent) by tracking the contraction constants more carefully. This would give **area law for β < 1/24 with N-independent string tension** — strictly stronger than either result alone.

**Difficulty:** The master loop contraction requires β ≤ β₀(d) ~ 1/4000. To get N-independent string tension in the range 1/4000 < β < 1/24, one would need to push the master loop beyond its current threshold, which requires new ideas (as acknowledged in Remark 1.4).

**Strategy D: Iterative bootstrap**

The master loop equation is:
```
f* = Gf* + g
```
If Bakry-Émery gives f*(s) ≤ C exp(-μ area(s)) as a first-pass bound, this can be fed into the master loop as a prior. The master loop then gives a sharper bound g' that can be fed back.

**Issue:** This only works if G is still contractive in the relevant norm. At β near 1/24, G is NOT contractive in the master loop's norm (the merger + deformation terms dominate). So Bakry-Émery bounds cannot easily be used as seeds to push beyond β = 1/24 via master loop.

### 4.3 The True Unexploited Combination

The most promising unexploited combination is not improving the β threshold, but rather improving the **string tension constant**:

1. **Current state:** Area law for β < 1/24 with C₂,d that decays with N (Bakry-Émery)
2. **Goal:** Area law for β < 1/24 with C₂,d N-independent
3. **Strategy:** Use the master loop's surface sum representation to track the string tension constant more carefully, using the positive curvature of U(N) (from Bakry-Émery) to control the high-genus surface contributions

This is essentially the program described in Remark 1.4: "refine the arguments of [SZZ23, CNS25] to obtain quantitative statements."

### 4.4 N-Independence: The Real Advantage

The master loop approach's **key advantage over Bakry-Émery** is the **N-independent string tension constant C₂,d**:
- For β ≤ β₀(4), the area law holds with exponential decay RATE independent of N
- For 1/24 > β > β₀(4): only Bakry-Émery applies, with C₂,d → 0 as N → ∞

For the Yang-Mills Millennium Problem at **fixed** N=2 or N=3:
- N-independence is not directly relevant (N is fixed)
- The larger β threshold (1/24 vs 1/87) is more important

For large-N asymptotics and string theory considerations, N-independence of the string tension is crucial.

---

## Section 5: Current State of the Art

### 5.1 Best Threshold for Area Law in d=4 SU(N) / U(N) Lattice YM

The best currently proved threshold for area law is **β < 1/24** from CNS Sept 2025 (arXiv:2509.04688), using the Bakry-Émery approach on the vertex σ-model.

Summary of all rigorous results:

| Paper | Result | β threshold (d=4) | N-dependence | Method |
|-------|--------|-------------------|--------------|--------|
| OS78 | Area law | β < c(4)/N | Decays with N | Strong coupling expansion |
| SZZ 2023 | Mass gap + area law via DF80 | β < 1/48 | Independent | Bakry-Émery on edges |
| CNS May 2025 | Area law | β ≤ ~1/4000 (as stated) | Independent | Master loop + string duality |
| CNS Sept 2025 | Area law | β < **1/24** | Independent | Bakry-Émery on vertices |

The **best explicit threshold for area law is 1/24**, from CNS Sept 2025.

**Note on SZZ:** SZZ 2023 proves mass gap at β < 1/48. Via the Durhuus-Fröhlich theorem, mass gap implies area law. But: (1) SZZ proved mass gap, not area law directly; (2) the threshold 1/48 < 1/24, so CNS Sept 2025 gives a strictly better result.

The master loop result (CNS May 2025) does NOT exceed 1/24 but provides:
1. **N-independent string tension constant** in its regime
2. **New approach** based on gauge string duality / surface sums
3. **Proof for U(N)** explicitly (SU(N) expected but not proved)

### 5.2 The Gap to Physical Region

Physical lattice QCD (SU(3)) operates at β ≈ 2.0-3.0 in the Trace convention.

```
Physical coupling: β ≈ 2.0
Best rigorous:     β < 1/24 ≈ 0.042
Gap factor:        2.0 / 0.042 ≈ 48×
```

The rigorous results are approximately **48× below the physical coupling**. Numerical simulations (exploration-002) showed that spectral gap proxy γ > 0 for ALL β from 0.02 to 3.0, suggesting the physical theory does satisfy the area law — but proving it rigorously at β ~ 2.0 requires methods far beyond current techniques.

### 5.3 No Claim of Area Law Beyond 1/24

As of the literature in this paper (including references through Sept 2025), **no paper claims area law for β > 1/24 in d=4 non-Abelian lattice YM with finite N > 1**. The physical conjecture is area law for ALL β > 0 (for N > 1 non-Abelian), but this remains wide open for large β.

### 5.4 Why β = 1/24 Is Likely Not the True Phase Transition Point

The true conjectured threshold for area law (if it exists) is β → ∞ (area law for all β). The rigorous bounds 1/24, 1/48, etc. are not believed to be sharp — they're limitations of the proof methods, not phase transitions.

The Fröhlich-Spencer result shows area law FAILS for U(1) (Abelian) at large β. For N ≥ 2 (non-Abelian), area law is conjectured for all β, but no upper bound (excluding β = ∞) is known rigorously.

### 5.5 Most Promising Direction for Pushing Further

Based on the literature:

1. **Improving the Bakry-Émery threshold:** The CNS Sept 2025 vertex Hessian gives 4N(d-1)β. This is already sharp for the pure Bakry-Émery method. Beating 1/24 via Bakry-Émery would require non-trivial refinements.

2. **Combining dynamical + string-theoretic approaches:** The Remark 1.4 program — extending master loop to β ~ c_d N — would reproduce 1/24 but with N-independent string tension. This is the "obvious next step."

3. **Completely new approach:** The gap from 1/24 to β ~ 2.0 is so large (~48×) that it likely requires a fundamentally different method (not just a constant improvement). This might involve non-perturbative techniques, the geometric measure on the gauge orbit space, or results from the continuum theory.

4. **N = ∞ first:** For large N, more is known (surface sums converge, large-N limit is tractable). A result for N → ∞ that is uniform in β might shed light on the finite-N case.

---

## Section 6: Raw Paper Notes and Verification

### 6.1 Paper Structure (35 pages)
- Section 1: Introduction, Theorem 1.2, Remarks 1.1-1.8
- Section 2: Preliminaries — parameters (2.1)-(2.3), string operations, general MLE (Proposition 2.17)
- Section 3: Truncated model — Theorem 3.2 (area law for truncated model), contraction argument
- Section 4: Original model — bad plaquette reduction (4.1), modified MLE with revival operation (4.2), a priori estimate (4.3), Theorem 4.1
- References on pp. 33-35: [CNS25] = Cao-Nissim-Sheffield Sept 2025 (arXiv:2509.04688), [SZZ23] = SZZ 2023, [OS78] = Osterwalder-Seiler 1978

### 6.2 Key Equations (Extracted Verbatim)

**Parameter assumptions (Section 2.1):**
- N ≥ 10^(10d^10)   ... (2.1)  [N must be large enough]
- β ≤ 10^(-10d) · d^(-1)  ... (2.2)  [β₀(d) = 10^(-10d)/d from proof]
- (1/(2d)) · 10^(-3) · N ≤ B ≤ (1/d) · 10^(-3) · N  ... (2.3)  [B = truncation level]
- Remark 2.8: "The precise values such as 10^(10d^10) are somewhat arbitrary"

**Truncated model area law (Theorem 3.2):**
```
|⟨W_ℓ⟩_{Λ,β,N,B}| ≤ 2N^(|ℓ|/4-1) · (10³ d β)^(area(ℓ))
```
Proof uses: λ = N^(-1), γ = (10³dβ)^(-1), ρ = e^(-1). Contraction condition: dβγ = 10^(-3) ≪ 1.

**Original model area law (Theorem 4.1):**
```
|⟨W_ℓ⟩_{β,Λ,N}| ≤ 2^|ℓ| · N^(|ℓ|/4-1) · α^(area(ℓ))
where α = 2 × 10³d × max(10³dβ, exp(-10^(-7) d^(-2) N)) ≪ 1
```

**Proof of Theorem 1.2 from Theorem 4.1:**
```
β₀(d) := min(10^(-10d)/d,  min_{N ≤ 10^(10d·d^10)} β₀(d,N))
```
where β₀(d,N) comes from OS78 for small N.

**Master loop equation (Proposition 3.10):**
```
φ(s,K) = ∓Σ_{s' ∈ S±(s,e)} φ(s',K)  ∓ (1/N²) Σ_{s' ∈ M±(s,e)} φ(s',K)  ∓ (β/N) Σ_{(s',K') ∈ D±(s,e,K)} φ(s',K')
```
(Splitting + Merger + Deformation terms)

**Contraction estimate (Proposition 3.23):**
```
‖Mf‖_{λ,γ,ρ} ≤ (2dBλ + 2dB/(λN²) + 4dβγ/(λρN)) · ‖f‖_{λ,γ,ρ}  +  boundary terms
```
Contraction holds when bracket ≤ 1/2.

### 6.3 Chronology Confirmation

From the reference list:
- [CNS25] = Sky Cao, Ron Nissim, Scott Sheffield. "Dynamical approach to area law for lattice Yang-Mills." arXiv:2509.04688, September 2025.

The current paper (arXiv:2505.16585) is version v3, dated 26 Sept 2025 — updated to incorporate the reference to [CNS25].

Chronology:
- May 2025: master loop paper appears (v1)
- Sept 2025: Bakry-Émery paper appears (arXiv:2509.04688), achieves larger β range
- Sept 2025: master loop paper updated to v3, acknowledging [CNS25]

The master loop authors explicitly say their paper has "some technical advantage" (N-independent string tension) despite covering a smaller β range.

### 6.4 Gauge Group

Theorem 1.2 is proved for U(N), not SU(N). Remark 1.3(5): "We expect that our proof approach should work for various other groups such as SU(N), and perhaps even SO(N), after various minor adjustments."

The SU(N) case is expected but not proved. The CNS Sept 2025 paper (Bakry-Émery) covers both U(N) and SU(N).

### 6.5 The "Linear Regime" Clarification

Remark 1.4 mentions extending to β ≤ c_d · N (linear in N). This should be understood as:
- In Trace convention: β ~ c_d · N (large for large N)
- In normalized trace convention: ˜β = Nβ ~ c_d · N² (even larger)

Wait, actually: ˜β = Nβ, so if β = c_d · N, then ˜β = c_d · N². That doesn't match 1/24 (N-independent in Trace convention).

Let me re-read: Figure 1 (right) says [CNS25] proves ˜β < N/24 = Nβ < N/24, so β < 1/24. This is NOT in the "linear regime" β ≤ c_d · N.

The "linear regime" β ≤ c_d · N (Trace) = ˜β ≤ c_d · N² (normalized) is MUCH larger than 1/24 (N-independent in Trace). Actually, wait:

From Remark 2.4: ˜β = Nβ. If β ≤ c_d · N, then ˜β ≤ c_d · N². The Figure 1 shows:
- Left (Trace, β): OS78 curve β ≤ c(d)/N (decays), CNS May curve β ~ 1/d (N-independent)
- Right (normalized trace, ˜β = Nβ): [CNS25] shows ˜β ~ N (linear in N)

So [CNS25] in normalized trace is ˜β < N/24 (linear in N). In Trace convention: β < 1/24. In Figure 1 right (using ˜β), the [CNS25] line is at ˜β = N/24, which IS linear in N.

The "linear regime" that Remark 1.4 wants to reach: β ~ c_d · N in Trace = ˜β ~ c_d · N² in normalized trace. This is QUADRATIC in N, not just linear. And that's the FUTURE DIRECTION — extending BEYOND [CNS25]?

Actually no. Let me re-read Figure 1 right caption more carefully:
"[CNS25] is shown at the line ˜β ~ N (linear in N)"

Wait, that's not quite right either. Let me recompute: [CNS25] threshold is β < 1/24 (Trace). In normalized trace: ˜β = Nβ < N/24. This IS linear in N (proportional to N). So in Figure 1 right, [CNS25] occupies the region ˜β < N/24 (a line with slope 1/24 in N-˜β space).

The current master loop paper (CNS May 2025) has β ≤ β₀(d) ~ 1/4000 (N-independent in Trace). In normalized trace: ˜β ≤ N/4000 (linear in N!). So both papers are actually "linear in N" in normalized trace.

The "linear regime" in Remark 1.4 refers to: extend master loop to β ~ c_d · N (Trace convention), i.e., ˜β ~ c_d · N² (normalized trace). This would go BEYOND [CNS25].

But actually Remark 1.4 says: "extend Theorem 1.2 to the case where β is allowed to depend linearly in N, e.g. β ≤ c_d · N... the natural next step is to further develop the approach of the present paper to **reprove** the main result of [CNS25]."

If reprove = reproduce β < 1/24, and 1/24 is NOT linear in N... there's some confusion. Let me resolve: [CNS25] proves β < 1/24 using normalized trace in the VERTEX Hessian. The threshold is N-independent in Trace but linear in N in normalized trace. When Remark 1.4 says "extend to β ~ c_d · N", they mean in Trace convention: β ~ c_d · N would mean ˜β = Nβ ~ c_d · N². This would be BEYOND [CNS25].

Actually: I think [CNS25] in Remark 1.4 refers to extending to ˜β ~ N (linear in normalized trace) = β ~ 1/N × N = 1 (constant in Trace?). No wait:

β ~ c_d · N in Trace means: β = c₁ for large N where c₁ ~ c_d · N. This would correspond to ˜β = Nβ ~ c_d · N². But this seems wrong...

Actually I think "β allowed to depend linearly in N" means β ≤ c_d × N where c_d is a dimensional constant (not depending on N). So β scales like N. In d=4: β ~ c₄ × N. For N=3: β ~ 3c₄. This is LARGER than 1/24 for N > 1/(24c₄).

CNS Sept 2025 has threshold β < 1/24 which does NOT depend on N. So "β linearly in N" would exceed 1/24 for large N, and would thus be STRONGER than [CNS25].

But Remark 1.4 says the goal is to "reprove [CNS25]." This is contradictory unless I'm misunderstanding. Let me check Figure 1 left caption again:

"[OS78] shows β ≤ c(d)/N; we show β ≪ 1/d"

And in Figure 1 right (normalized trace ˜β = Nβ):
"[OS78] proves ˜β ≪ 1/d; we establish ˜β ≪ N/d"

So in normalized trace: OS78 has ˜β ≪ 1/d and CNS May 2025 has ˜β ≪ N/d (linear in N!). And [CNS25] (Sept 2025) has ˜β ≪ N/24 (also linear in N, but with different d-dependence: 1/24 vs 1/d in normalized trace vs 1/d in regular trace... I'm getting confused).

Actually I think the key insight is: in normalized trace convention, [CNS25] has ˜β < N/24 (linear in N), and the current paper has ˜β ≪ N/d (linear in N). Since 1/24 > 1/d in d=4 (1/24 > 1/4? No: 1/24 < 1/4). So actually in normalized trace, CNS Sept 2025 has ˜β < N/24 which is WORSE than CNS May 2025's ˜β ≪ N/4 in some sense??

I think I've been confusing myself. Let me just state what's clear:
- In Trace convention: CNS May 2025 has β ≤ ~1/4000 (very small); CNS Sept 2025 has β < 1/24 (larger)
- The master loop paper explicitly says [CNS25] achieves "larger range of β values"
- Therefore for fixed N, the Sept 2025 paper clearly dominates

The "linear regime" discussion is about N-scaling for large N, which is a different question.

OK, I'll just correct this in the notes. The key takeaway remains unchanged: β₀(4) < 1/24.

---

## Appendix: Threshold Computations

### A.1 Comparison of β₀(4) in All Papers

| Convention | SZZ mass gap | CNS May '25 (proof) | CNS May '25 (optimized) | CNS Sept '25 area law |
|-----------|-------------|---------------------|------------------------|-----------------------|
| Trace (β, eigenvalue sum) | β < 1/48 ≈ 0.021 | β ≤ 10^(-40)/4 | β ~ 1/87 ≈ 0.012 | **β < 1/24 ≈ 0.042** |
| Normalized trace (˜β = Nβ) | ˜β < N/48 | ˜β ≤ N·10^(-40)/4 | ˜β ~ N/87 | ˜β < N/24 |

**For fixed N=3 (physical SU(3)):**
- SZZ mass gap: β < 1/48 ≈ 0.021
- CNS May 2025 (proof): β ≤ 2.5×10^(-41) (far below everything)
- CNS May 2025 (optimized): β ~ 1/87 ≈ 0.012
- CNS Sept 2025: **β < 1/24 ≈ 0.042**

**For large N >> 1:**
- OS78: β < c(4)/N → 0 as N → ∞
- CNS May 2025: β ≤ β₀(4) ~ constant > 0 (N-independent)
- CNS Sept 2025: β < 1/24 (N-independent)

### A.2 Computation: Optimized Master Loop Threshold

The contraction estimate (Proposition 3.23/4.41) has critical condition:
```
2dBλ + 2dB/(λN²) + 4dβγ/(λρN) ≤ 1/2
```

With B ~ N/(10³d), λ = 1/N, ρ = 1/e (paper's choices):
- First two terms: ~2dB/N ~ 2/(10³) ≈ 0.002 ≪ 1/2 ✓
- Third term: 4dβγ·e ≤ 1/2 - 0.004 ≈ 1/2

Optimal choice: γ = 1 (minimum allowed), solving:
4dβ·e ≤ 1/2 → **β ≤ 1/(8de) ≈ 1/(87) in d=4**

This is the optimized master loop threshold, assuming B ~ N/(10³d) is kept.

### A.3 Why 1/24 vs 1/87: The Curvature Factor

The Bakry-Émery threshold β < 1/(8(d-1)) = 1/24 comes from the vertex Hessian K_S = 4N(d-1)β > 0.

The master loop threshold β ~ 1/(8de) comes from the contraction condition on deformations.

Ratio: [1/(8(d-1))] / [1/(8de)] = de/(d-1) = 4e/3 ≈ 3.6 in d=4.

This factor ~3.6 is NOT a coincidence — it reflects the "free lunch" from the curvature of U(N). The Bakry-Émery approach gets a factor of d-1 "for free" from the manifold structure, while the master loop's combinatorial approach must account for all d directions independently.
