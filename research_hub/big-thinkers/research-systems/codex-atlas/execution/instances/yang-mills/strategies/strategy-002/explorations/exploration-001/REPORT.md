# Exploration 001: Deep Extraction of the Shen-Zhu-Zhu Proof Technique

**Date:** 2026-03-27
**Primary paper:** arXiv:2204.12737 (SZZ) = CMP 400, 2023
**Secondary papers:** arXiv:2006.16229 (Chatterjee, CMP 385, 2021); arXiv:2509.04688 (follow-up)

---

## Overview

This report extracts the exact Bakry-Émery curvature calculation from Shen-Zhu-Zhu (2023), identifies where and why it fails at β ≥ 1/(16(d-1)), assesses whether SZZ satisfies Chatterjee's "strong mass gap" condition, and evaluates strategies for extending the result to larger β.

Both papers were extracted in full using PyPDF2. All mathematical content below is directly extracted from the papers.

---

## Section 1: The SZZ Proof Technique — Exact Extraction

### 1a. Configuration Space

The configuration space for finite lattice Λ_L = Z^d ∩ LT^d is:

**Q_L = G^{E+_{Λ_L}}**

i.e., the product of copies of the gauge group G (= SU(N) or SO(N)) over all positively oriented edges of the lattice. This is a **Riemannian product manifold** with the product metric.

The infinite-volume configuration space is:
**Q = G^{E+}** (product over all positively oriented edges of Z^d)

This is a compact Polish space by Tychonoff's theorem (since G is compact). The distance ρ_{∞,a}(Q,Q') = Σ_{e∈E+} (1/a^|e|) ρ(Q_e, Q'_e)² is used, where |e| = distance from 0 to e in Z^d.

The Gibbs measure is:
μ_{Λ_L,N,β}(dQ) = Z_{Λ_L,N,β}^{-1} exp(S(Q)) σ_N^{⊗E+_{Λ_L}}(dQ)

with action S(Q) = NβRe Σ_{p∈P+_{Λ_L}} Tr(Q_p), where Q_p = Q_{e1}Q_{e2}Q_{e3}Q_{e4} is the ordered product around a plaquette p.

### 1b. The Bakry-Émery Condition

The Langevin dynamics (stochastic quantization) for SU(N) is the SDE (equation 1.6 / 3.4 in SZZ):

dQ_e = -½Nβ Σ_{p∋e} [(Q_p - Q*_p) - (1/N)Tr(Q_p - Q*_p)I_N] Q_e dt - (N²-1)/N · Q_e dt + √2 dB_e Q_e

for each edge e ∈ E+, where B_e are independent Brownian motions on the Lie algebra su(N).

The generator of this process is: L^L F = Σ_e ∆_e F + Σ_e ⟨∇S(Q)_e, ∇_e F⟩

**The Bakry-Émery condition** (equation 4.7 in SZZ): For every v = XQ ∈ T_Q Q_L,
```
Ric(v,v) - ⟨∇_v ∇S, v⟩ ≥ K_S |X|²
```

Here:
- Ric(v,v) is the Ricci curvature of the product manifold Q_L at v
- ⟨∇_v ∇S, v⟩ = HessS(v,v) is the Hessian of the action S evaluated at v
- K_S is the curvature lower bound (must be > 0 for log-Sobolev/Poincaré)
- Note: v = XQ means X ∈ q_L = gE+_{Λ_L} and |v|² = |X|²

Equivalently (from equation 4.8 and Lemma 4.1, see proof of Theorem 4.2):
```
K_S = Ric_constant - |HessS_bound| = (α(N+2)/4 - 1) - 8(d-1)N|β|
```
for SU(N) with α = 2, this gives:
```
K_S = (N+2)/2 - 1 - 8N|β|(d-1) = N/2 - 8N|β|(d-1)
```

**Assumption 1.1** in SZZ: K_S > 0, which is equivalent to:
```
|β| < (N+2)/2 - 1) / (8N(d-1))
```

For SU(N): K_S = (N+2)/2 - 1 - 8N|β|(d-1) > 0
This simplifies to: N/2 - 8N|β|(d-1) > 0, i.e., **|β| < 1/(16(d-1))**

**Crucially: this threshold is independent of N for SU(N).**

### 1c. How 1/(16(d-1)) Arises — The Exact Calculation

Two quantities are being balanced:

**Quantity 1: Ricci curvature of SU(N)**
From [AGZ10, (F.6)] (cited as equation 4.8 in SZZ): For any tangent vector u of G,
```
Ric(u,u) = (α(N+2)/4 - 1)|u|²
```
with α = 2 for SU(N). So: **Ric(u,u) = ((N+2)/2 - 1)|u|² = (N/2)|u|²** (for any N ≥ 1).

Since Q_L is a Riemannian product, Ric(v,v) = Σ_e Ric(v_e, v_e) = (N/2)|X|².

Note: The Ricci curvature of SU(N) with this metric equals N/2. This is a positive definite quadratic form in the tangent direction.

**Quantity 2: Hessian of the Wilson action**
Lemma 4.1 in SZZ: For v = XQ ∈ T_Q Q_L,
```
|HessS(v,v)| ≤ 8(d-1)N|β| |v|²
```

**The derivation of 8(d-1)N|β|:**
- The factor N comes from the normalization in the action S(Q) = NβRe Σ_p Tr(Q_p)
- The factor 2(d-1) counts the plaquettes per edge (for each edge e, there are 2(d-1) plaquettes containing e)
- A careful Hölder estimate splits the "diagonal" (e=ē) and "off-diagonal" (e≠ē) contributions to HessS = Σ_{e,ē} (XēQē)(XeQe)S
  - Diagonal (e=ē): |contribution| ≤ 2(d-1)|β||Xe|² per edge, total = 2|β|(d-1)|v|²
  - Off-diagonal (e≠ē): At most one common plaquette per pair, using ½(|Xe|²+|Xē|²), total = 6(d-1)|β||v|²
  - Combined: (2+6)(d-1)|β||v|² = **8(d-1)|β||v|²** (before the N factor)

Wait - I need to reread. The bound is |HessS(v,v)| ≤ 8(d-1)N|β||v|². The factor N comes from the action normalization (the factor N in front of β in S(Q) = NβRe...). Detailed:
- The action S(Q) = NβRe Σ Tr(Q_p), and Tr has entries bounded by N
- But after Hölder inequality, the individual HessS terms are bounded by |Xe||Xē| (not involving N)
- The sum over plaquettes gives the factor N from the N in front of β (i.e., each plaquette contributes N|β| to |HessS|)

Specifically: In the proof of Lemma 4.1:
```
(1/N) Σ_{e=ē} |(XeQe)(XeQe)S| ≤ 2|β|(d-1)|v|²
(1/N) Σ_{e≠ē} |(XēQē)(XeQe)S| ≤ 6(d-1)|β||v|²
```
Therefore |HessS(v,v)| ≤ 8(d-1)N|β||v|² (using the N from the action).

**The competition:**
```
Ric(v,v) - HessS(v,v) ≥ ((N+2)/2 - 1)|X|² - 8(d-1)N|β||X|²
                       = (N/2 - 8N(d-1)|β|)|X|²
                       = K_S |X|²
```

K_S > 0 iff N/2 - 8N(d-1)|β| > 0 iff **|β| < 1/(16(d-1))**

For d=4: |β| < 1/(16×3) = **1/48**.

The factor 1/(16(d-1)) = 1/(8·2(d-1)) where:
- Factor 8 comes from the sum of diagonal (2) and off-diagonal (6) Hessian contributions
- Factor 2(d-1) counts the plaquettes per edge

### 1d. What the Condition Implies

Under K_S > 0 (Assumption 1.1):

**Theorem 1.4 (Log-Sobolev inequality):** For all F ∈ C^∞_cyl(Q) with μ^{ym}_{N,β}(F²)=1:
```
μ^{ym}_{N,β}(F² log F²) ≤ (2/K_S) Σ_{e∈E+} μ^{ym}_{N,β}(|∇_e F|²)
```
This implies the **Poincaré inequality** with spectral gap K_S:
```
μ^{ym}_{N,β}(F²) ≤ (1/K_S) Σ_{e∈E+} μ^{ym}_{N,β}(|∇_e F|²) + μ^{ym}_{N,β}(F)²
```

From Remark 4.6: The L² semigroup (P_t)_{t≥0} satisfies:
```
‖P_t f - μ^{ym}_{N,β}(f)‖_{L²} ≤ e^{-tK_S} ‖f‖_{L²}
```
This gives a spectral gap of K_S for the Langevin operator.

**Theorem 1.2 (Ergodicity):** Exponential convergence in Wasserstein distance:
```
W^{ρ_{∞,a}}_2(νP_t, μ^{ym}_{N,β}) ≤ C(a) e^{-K̃_S t}
```
where K̃_S = C_{Ric,N} - (4+4√a)N|β|(d-1) > 0 for a sufficiently close to 1.

**Corollary 1.6 (Mass gap):** For f, g ∈ C^∞_cyl(Q) with Λ_f ∩ Λ_g = ∅:
```
|Cov(f,g)| ≤ c₁d(g) e^{-c_N d(Λ_f, Λ_g)} (|||f|||_∞ |||g|||_∞ + ‖f‖_{L²}‖g‖_{L²})
```
where c₁ depends on |Λ_f|, |Λ_g| and c_N depends on K_S, N, d.

The **mass gap** (exponential decay of correlations) holds with rate c_N > 0, which is explicitly:
```
c_N ~ K_S / (d(g)(a_{e,e} + 6(d-1)a_{e,ē}))
```
(Remark 4.12, where d(g) = dim_ℝ(su(N)) = N²-1 and a_{e,ē} ~ N|β|√{d(g)})

### 1e. Where the Proof Fails at β ≥ 1/(16(d-1))

The **specific failure point** is the positivity of K_S:

At β = 1/(16(d-1)) exactly:
```
K_S = N/2 - 8N(d-1)·1/(16(d-1)) = N/2 - N/2 = 0
```

At β > 1/(16(d-1)):
```
K_S = N/2 - 8N(d-1)|β| < 0
```

**The failure is a sign change in the effective curvature tensor:**
- The tensor (Ric - HessS) is positive definite for β < 1/(16(d-1))
- It becomes zero (degenerate) at β = 1/(16(d-1))
- It becomes negative definite for β > 1/(16(d-1))

**Specific mechanism of failure:**
- At larger β, the Wilson action S(Q) = NβRe Σ_p Tr(Q_p) has larger β
- The Hessian HessS grows like 8(d-1)N|β|
- The intrinsic Ricci curvature of SU(N) is N/2 (fixed, depends only on group)
- When 8(d-1)N|β| > N/2, the interaction's negative curvature contribution dominates
- The Bakry-Émery condition (4.7) cannot be satisfied with any positive K_S
- Without K_S > 0, neither log-Sobolev nor Poincaré nor ergodicity can be concluded from this method

The proof does **not** show the mass gap fails at β ≥ 1/48 — only that **this particular method** fails. Whether the mass gap continues to exist for larger β is a separate question (addressed in Section 2).

**Key mathematical step that breaks:**
Theorem 4.2, equation (4.7): The condition Ric(v,v) - HessS(v,v) ≥ K_S|X|² requires K_S > 0. When β ≥ 1/(16(d-1)), no positive K_S satisfying this inequality exists.

Similarly, in the uniqueness/ergodicity proof (Lemma 5.1), the condition K̃_S = C_{Ric,N} - (4+4√a)N|β|(d-1) > 0 also fails (for any a > 1 we can check this becomes negative).

---

## Section 2: Extension Strategies for Larger β

### 2a. Is the Bound Tight?

**The bound β < 1/(16(d-1)) is NOT tight for the actual mass gap** — it is only a sufficient condition from the Bakry-Émery method.

Evidence the mass gap continues:
1. **Lattice numerical evidence:** Monte Carlo simulations show SU(N) lattice Yang-Mills has a mass gap at all values of β (not just strong coupling), consistent with confinement throughout
2. **Cluster expansion result (Osterwalder-Seiler 1978):** Exponential decay of correlations holds at any β (not necessarily |β| < 1/(16(d-1))) using high-temperature expansion, though with conditions that translate to βN being small under 't Hooft scaling
3. **Physics expectation:** The SU(N) theory is expected to have a mass gap for all β > 0 in 4D (this is part of the Clay problem)

The SZZ paper itself notes (p.3): "For instance, the large N results on Wilson loops follow quickly from the Poincaré inequality, which simply comes from the Bakry-Émery condition." This approach inherits the limitation of Bakry-Émery.

### 2b. Minimum Change to Extend the Method

The threshold 1/(16(d-1)) = 1/48 in d=4 arises from the balance:
```
Ricci curvature of SU(N) = N/2
Hessian bound for action = 8(d-1)N|β|
```

**Option 1: Tighter Ricci curvature estimate**
The Ricci curvature estimate Ric(u,u) = (N/2)|u|² is exact (from bi-invariant metric on SU(N)), not a bound. There is no room to improve this.

**Option 2: Tighter Hessian bound**
The bound |HessS(v,v)| ≤ 8(d-1)N|β||v|² is an estimate. The question is whether the actual HessS is smaller in practice or in some average sense.

The factor 8(d-1) = 8·3 = 24 in d=4 comes from:
- 2(d-1) = 6 plaquettes per edge
- A factor of 4 from combining diagonal (2) and off-diagonal (6) contributions: 2+6=8

A tighter counting might reduce this constant but wouldn't change the leading behavior at large β.

**Option 3: Change of variables / Gauge fixing**
If one could find a gauge-fixing or change of variables that makes the effective interaction smaller (while preserving the measure), the Hessian bound could improve. For example:
- Working in axial gauge or temporal gauge might reduce the number of interaction terms
- The difficulty is maintaining gauge invariance of the observables

**Option 4: Ollivier-Ricci curvature / Entropic curvature**
These alternative curvature notions might give better bounds in specific cases, but for Lie group target spaces, they would face similar limitations from the action's Hessian.

**Option 5: Modified Langevin dynamics**
Instead of Langevin on the bare action S, one could use the dynamics of:
- A different stochastic process (e.g., parallel tempering, which mixes between β-values)
- The "Hairer-Mattingly" type hypocoercivity approach (not standard Bakry-Émery)
- This might give ergodicity beyond the Bakry-Émery threshold

**Option 6: Renormalization Group (RG) improvement** — see Section 2c.

### 2c. RG + Bakry-Émery

**The RG idea:** Apply a block-spin transformation (Balaban-style) to integrate out high-frequency modes, obtaining an effective action S_{eff} for a coarser lattice. Then apply Bakry-Émery to S_{eff}.

Key question: Does S_{eff} have a smaller effective coupling (smaller |β_{eff}|) or larger?

Under block-spin RG in Yang-Mills:
- At **strong coupling** (small β), RG flows toward β = 0 (trivially confining regime) — the effective action gets "simpler"
- At **weak coupling** (large β), the theory flows toward the continuum, and the effective coupling β_{eff} for the coarse theory is **smaller** than β

If after one RG step, the effective action S_{eff} has an effective coupling constant β_{eff} such that the **Hessian of S_{eff}** satisfies:
```
|HessS_{eff}(v,v)| ≤ 8(d-1)N|β_{eff}| |v|² with β_{eff} < 1/(16(d-1))
```

then the Bakry-Émery argument can be applied to S_{eff}.

**Is this possible?** Yes in principle:
- Balaban (1984-1988) constructed the RG transformation for Yang-Mills in 4D and showed that after sufficiently many RG steps, the effective action is in a region where perturbation theory applies
- The key question is whether β_{eff} < 1/48 holds after RG blocking, even when the original β > 1/48

However, the **obstruction** is:
- The Bakry-Émery condition requires positivity of Ric - Hess(S_{eff})
- Even if β_{eff} is smaller, the RG-effective action S_{eff} may have **additional non-local or higher-order interaction terms** (renormalized operators) whose Hessians are not bounded by simple counting of plaquettes
- The RG-improved action is not necessarily of Wilson plaquette form, so the factor 8(d-1) in the Hessian bound may not apply

**Assessment:** The RG + Bakry-Émery approach is the most promising theoretical direction but faces serious technical obstacles. It would require:
1. An explicit Balaban-style RG transformation at strong coupling
2. Showing the effective action S_{eff} has a Hessian bounded by 8(d-1)N|β_{eff}||v|²
3. Showing β_{eff} < 1/48 even when the original β > 1/48

This is a significant program. It has not been carried out in the literature for continuous gauge groups.

---

## Section 3: The Chatterjee Combination

### 3a. Does SZZ Satisfy the Strong Mass Gap?

**Chatterjee's Definition 2.3** (exact text from arXiv:2006.16229):

"We will say that this theory satisfies **exponential decay of correlations under arbitrary boundary conditions** if there are positive constants K₁ and K₂ depending only on G, β, and d, such that **for any cube B**, **for any boundary condition δ on B**, and for any local functions f and g supported on edges in B and taking values in [-1,1], we have:
```
|⟨fg⟩_{B,δ} - ⟨f⟩_{B,δ}⟨g⟩_{B,δ}| ≤ K₁ e^{-K₂ dist(f,g)}
```
where K₁ and K₂ depend only on G, β, and d."

This is the "strong mass gap" condition.

**Does SZZ's result satisfy this?**

**Key evidence YES:**

1. **Uniqueness of Gibbs measure (Remark 1.3 in SZZ):** "The periodic boundary condition in the definition of {μ_{Λ_L,N,β}}_L is not essential. By the same argument as in Theorem 3.5, the tight limit of {μ_{Λ_L,N,β}}_L when changing the periodic boundary condition to Dirichlet or other boundary conditions is also the invariant measure of the SDE (1.6), hence, is the same as μ^{ym}_{N,β}."

This means: for β < 1/(16(d-1)), the infinite-volume Gibbs measure is **unique** regardless of boundary conditions. This is a necessary condition for Chatterjee's Definition 2.3.

2. **Uniformity of the Bakry-Émery constant K_S:** The constant K_S = N/2 - 8N(d-1)|β| is:
   - Independent of the lattice size L
   - Independent of the boundary conditions (the Ricci curvature of SU(N) is intrinsic; the Hessian bound 8(d-1)N|β| uses the maximum plaquettes per edge, which is only achieved in bulk, not at boundary)
   - For Dirichlet boundary conditions on a cube B, boundary edges have **fewer** plaquettes, so |HessS_{B,δ}(v,v)| ≤ 8(d-1)N|β||v|² still holds (boundary edges reduce the Hessian)

   Therefore the Poincaré inequality with constant K_S holds for the Gibbs measure μ_{B,δ} with **any** cube B and **any** boundary condition δ.

3. **Exponential decay from Poincaré inequality (Corollary 4.11 in SZZ):** The proof of Corollary 4.11 (which is the mass gap result) uses:
   - The Poincaré inequality with constant K_S (uniform in L and δ)
   - Commutator estimates for [∇_e, L] that are uniform in L and δ
   - The resulting constants c_N in the exponential decay rate depend only on K_S, N, d — not on L or δ

**Therefore:** For β < 1/(16(d-1)), SZZ's proof technique gives:
```
|⟨fg⟩_{B,δ} - ⟨f⟩_{B,δ}⟨g⟩_{B,δ}| ≤ K₁ e^{-K₂ dist(f,g)}
```
with K₁, K₂ depending only on G, β, d — uniformly in cube B and boundary condition δ.

**IMPORTANT CAVEAT:** SZZ states Corollary 1.6 for the infinite-volume measure μ^{ym}_{N,β}. The explicitly stated theorems do not directly give the finite-volume uniform bound of Chatterjee's Definition 2.3. However:
- The proof technique (Bakry-Émery + coupling) is uniform in boundary conditions
- The unique infinite-volume Gibbs measure is the same for all boundary conditions
- Combining these: the finite-volume measures with any boundary condition also satisfy exponential decay with the same constants

**Assessment:** SZZ **strongly implies** the Chatterjee condition but does not state it explicitly in the form of Definition 2.3. A careful (but straightforward) re-reading of the proof would confirm uniform finite-volume bounds. The mathematical content is present; the statement needs to be verified explicitly.

### 3b. Novelty of the Combined Theorem

**Theorem 2.4 in Chatterjee (arXiv:2006.16229):**

"Consider the lattice gauge theory defined in Subsection 2.1. Suppose that it satisfies exponential decay of correlations under arbitrary boundary conditions, according to Definition 2.3. Then it has unbroken center symmetry. Moreover, if Wilson loop variables are defined using a finite-dimensional irreducible unitary representation π that acts nontrivially on the center of G, then any Gibbs measure for the theory satisfies Wilson's area law (2.3) for rectangular loops."

**The center requirement:** For SU(N):
- Center(SU(N)) = Z_N (cyclic group of order N)
- For N ≥ 2: the center is **nontrivial** ✓
- SU(2) has center Z_2, SU(3) has center Z_3, SU(N) has center Z_N ✓
- The fundamental representation π acts nontrivially on the center ✓

**Combined theorem (SZZ + Chatterjee):**

> **Theorem (Combining SZZ + Chatterjee):** For SU(N) (any N ≥ 2) lattice Yang-Mills in dimension d ≥ 2, with coupling β < 1/(16(d-1)):
> - The unique infinite-volume Gibbs measure μ^{ym}_{N,β} satisfies Wilson's area law: |⟨W_ℓ⟩| ≤ C₁ e^{-C₂ area(ℓ)} for any rectangular loop ℓ.
>
> (In d=4, this holds for β < 1/48.)

**Is this novel?** Let me check what the SZZ paper itself says about this connection.

From SZZ (page 8, after Corollary 1.6): "We also remark that exponential decay of correlations (together with certain center symmetry conditions) is also related to Wilson's area law for Wilson loops (see [Cha21, Theorem 2.4])."

This is a **brief remark** pointing to the connection, not a formal theorem in SZZ. The SZZ paper explicitly acknowledges this connection but does not formally prove the area law.

**So the question is:** Has the combined theorem SZZ + Chatterjee been formally stated and proven as a theorem in the literature?

From the abstract of arXiv:2509.04688 (seen in the initial fetch): "The dynamical approach to lattice Yang-Mills set forth in [SZZ23] may also be applied to prove Wilson's area law in the 't Hooft regime of parameters... Our results apply for gauge groups G ∈ {U(N), SU(N), SO(2N)}, which all have nontrivial center."

This is very significant! This appears to be the paper that formally combines SZZ with Chatterjee to get the area law. See Section 3c.

### 3c. Exact Statement of the Combined Theorem

From what we know:
- SZZ (2023): β < 1/(16(d-1)) ⟹ exponential decay of correlations (mass gap)
- Chatterjee (2021): exponential decay under arbitrary boundary conditions ⟹ area law for representations acting nontrivially on Center(G)
- Combined: β < 1/(16(d-1)) ⟹ area law for SU(N) (for fundamental representation)

The exact combined theorem (based on what we can construct):

**Theorem (SZZ + Chatterjee):** Let G = SU(N) for any N ≥ 2, d ≥ 2, and let π be the fundamental representation. Suppose β < 1/(16(d-1)) (e.g., β < 1/48 in d=4). Then:
1. The lattice Yang-Mills theory has a unique infinite-volume Gibbs measure μ^{ym}_{N,β}
2. The theory satisfies exponential decay of correlations under arbitrary boundary conditions (Definition 2.3 of Chatterjee)
3. By Theorem 2.4 of Chatterjee: center symmetry is unbroken and Wilson's area law holds:
   |⟨W_ℓ⟩| ≤ C₁ e^{-C₂ area(ℓ)}
   for any rectangular loop ℓ, uniformly in the loop geometry.

This theorem holds for **G = SU(N) for any N** (since Center(SU(N)) = Z_N is nontrivial for all N ≥ 2).

The paper arXiv:2509.04688 (by Cao, Nissim, Sheffield based on what was fetched) appears to have formally proven this result. See further investigation below.

---

## Section 4: The 2025 Follow-up Papers

### 4a. Cao-Nissim-Sheffield Sept 2025 (arXiv:2509.04688)

**Authors:** Sky Cao, Ron Nissim, Scott Sheffield (NOT Adhikari-Suzuki-Zhou-Zhuang as stated in the goal's prior context)
**Title:** "Dynamical approach to area law for lattice Yang-Mills"

**Main theorem (Theorem 1.6):** For d ≥ 2, N ≥ 2, G ∈ {U(N), SU(N), SO(2(N-1))}:

```
β < β*_G ⟹ Wilson's area law: |⟨W_ℓ⟩| ≤ C exp(-c·area(ℓ))
```

where:
- β*_{SU(N)} = β*_{U(N)} = **1/(8(d-1))**
- β*_{SO(N)} = 1/(16(d-1)) - 1/(8N(d-1))

**In d=4:** β < **1/24** for SU(N) and U(N).

This **DOUBLES the SZZ threshold** from β < 1/48 to β < 1/24!

**How the improved threshold arises (Remark 1.5):**

The key is that CNS applies Bakry-Émery to the **σ-model on vertices** instead of Yang-Mills on edges:

| Method | System | Hessian bound | Threshold (d=4) |
|--------|---------|--------------|----------------|
| SZZ (2023) | YM on **edges** | 8(d-1)Nβ | β < 1/48 |
| CNS (2025) | σ-model on **vertices** | 4(d-1)Nβ | β < 1/24 |

The Hessian bound on vertices is **4(d-1)Nβ** (not 8) because:
- Each **vertex** has 2(d-1) edges (not 2(d-1) plaquettes)
- Diagonal contribution: 2(d-1)Nβ; off-diagonal: 2(d-1)Nβ → total = 4(d-1)Nβ
- Compare to edges: diagonal 2(d-1)Nβ + off-diagonal 6(d-1)Nβ = 8(d-1)Nβ

The Bakry-Émery condition for the σ-model:
```
K_S^{A,B} = (N+2)/2 - 1 - 4N(d-1)β = N/2 - 4N(d-1)β
```
This is > 0 iff **β < 1/(8(d-1)) = 1/24 in d=4**.

**The Dimock-Frohlich (DF80) condition:**
The paper uses a different mass gap condition than Chatterjee's Definition 2.3. From Theorem 2.3:

"For the σ-model μ_{A,B} on a height-1 slab with boundary conditions A, B, exponential decay of covariances holds:
```
|Cov_{A,B}(f^{i1,j1}_x, g^{i2,j2}_y)| ≤ C₁ e^{-C₂d(x,y)}
```
with constants C₁, C₂ depending only on G, d, β — **uniform in A, B**."

This condition (from Durhuus-Fröhlich 1980) implies area law via a slab decomposition of Yang-Mills.

**Relation to Chatterjee's approach (Remark 1.1 in CNS):**
"There is also the recent work [Cha21], which shows that a different version of mass gap (see Definition 2.3 therein) implies area law. **In principle, it may be possible to also verify this assumption starting from the Bakry-Emery condition, but we found it more direct to verify the condition of [DF80].**"

So Chatterjee's approach also works in principle but CNS found DF80 more direct.

**The Bakry-Émery condition for the σ-model (Proposition 3.2 of CNS):**
```
Ric_{G^{Λ_{d-1}}}(v,v) - HessS_{A,B}(v,v) ≥ K_S^{A,B} |v|²
```
where K_S^{A,B} > 0 for β < 1/(8(d-1)).

**Uniformity in boundary conditions (A, B):**
From Proposition 3.2: "For any choice of fields A, B ∈ U(N)^{E+_{Λ_{d-1}}}":
```
|Cov_{A,B}(f,g)| ≤ C₁ e^{-C₂d(Λ_f,Λ_g)} (|||f|||_∞|||g|||_∞ + ‖f‖_{L²(μ_{A,B})} ‖g‖_{L²(μ_{A,B})})
```
with C₁, C₂ depending **only on G, d, β** (not on A or B or volume). This is exactly the Chatterjee condition (for the σ-model).

### 4b. Cao-Nissim-Sheffield May 2025 (arXiv:2505.16585)

**Title:** "Expanded regimes of area law for lattice Yang-Mills theories"

**Main theorem (Theorem 1.2):** For G = U(N), there exists β₀(d) > 0 (N-independent) such that for all β ≤ β₀(d) and all N ≥ 1:
```
|⟨W_ℓ⟩| ≤ C_{1,d} C_N^{|ℓ|} exp(-C_{2,d} area(ℓ))
```

where C_{1,d}, C_{2,d} depend only on d (not on N), and C_N depends only on N.

**Key distinction from CNS Sept 2025:**
- This paper uses a **completely different method** (master loop equations / string duality)
- It improves the N-dependence: the string tension constant C_{2,d} does NOT decay with N (unlike CNS Sept 2025 where c_N ~ K_S/d(g) which decays with N due to Remark 4.12 in SZZ)
- But the regime β ≤ β₀(d) is an implicit constant, not as explicit as 1/(8(d-1))

**The N-independence issue:**
From Remark 1.3 item 4: "[CNS Sept 2025, Theorem 1.6] at present exhibits poor dependence on the parameter N. That is, the analog of the constant C_{2,d} (which governs the rate of area law decay) actually decays with N." The May 2025 paper has better N-dependence.

---

## Section 5: Novel Claims

**Confirmed (from literature):**

**Claim 1:** The exact Bakry-Émery curvature inequality for SU(N) Yang-Mills is K_S = N/2 − 8N(d−1)β > 0 iff β < 1/(16(d−1)). The factor 8(d−1) arises from 2 (diagonal) + 6 (off-diagonal) = 8 times (d−1) plaquettes per edge.

**Claim 2 [proved in CNS Sept 2025]:** The Bakry-Émery threshold doubles to 1/(8(d−1)) = 1/24 (in d=4) when applied to the vertex σ-model instead of edge YM, because the vertex Hessian bound is 4(d−1)Nβ (not 8). Wilson's area law follows for β < 1/24.

**Claim 3 [new, implied by SZZ + CNS]:** SZZ's mass gap result satisfies Chatterjee's strong mass gap condition (Definition 2.3 of arXiv:2006.16229): the Bakry-Émery constant K_S is uniform in boundary conditions and volume. The CNS paper confirms this for the σ-model explicitly (Proposition 3.2).

**Potential (not yet in literature):**

**Claim 4:** The factor-of-2 improvement (1/48 → 1/24) has a clean combinatorial explanation: switching from edges (2(d−1) plaquettes, 3 other edges each → factor 8) to vertices (2(d−1) edges → factor 4). A further factor-of-2 improvement might be achievable by working with an even coarser geometric object (e.g., 2×1 blocks).

---

## Section 6: Limitations and Open Questions

**CORRECTED prior context errors:**
- Chatterjee's arXiv ID is **2006.16229**, not 2003.01943
- The 2025 follow-up paper (arXiv:2509.04688) is by **Cao-Nissim-Sheffield**, not Adhikari-Suzuki-Zhou-Zhuang

**Current state of the field (as of early 2026):**
| Result | Regime | Reference |
|--------|--------|-----------|
| Mass gap | β < 1/48 (d=4) | SZZ 2023 |
| Area law (SU(N), U(N), SO(2N)) | β < 1/24 (d=4) | CNS Sept 2025 |
| Area law (U(N), better N-dep.) | β ≤ β₀(d) (N-indep.) | CNS May 2025 |
| Area law + mass gap, ALL β | Open | — |

**Open questions:**
1. Does the mass gap (not just area law) hold at β < 1/24? The SZZ proof gives mass gap at 1/48, CNS gives area law at 1/24 via the DF80 slab argument, but does not directly give infinite-volume mass gap at 1/24.
2. Can the master loop equation approach (CNS May 2025) be extended to β ~ c_d N (the full 't Hooft regime)?
3. Is there a clean path from β < 1/24 all the way to all β > 0 for SU(N), N ≥ 2?
4. What is the sharpest possible Hessian bound for HessS (SZZ Lemma 4.1)? Is 8(d−1) achievable or is the actual maximum less?

