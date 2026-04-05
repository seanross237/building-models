# Exploration 001: Line-by-Line Decomposition Audit of the β = 4/3 Barrier

## Goal
Perform a line-by-line reading of Vasseur (2007) Proposition 3, extract the precise chain of inequalities producing β < 4/3, identify where each sub-exponent (1/2 and 5/6) originates, classify each step as sharp or potentially loose, and cross-compare with the Vasseur-Yang (2021) vorticity formulation.

---

## 1. Complete Chain of Inequalities in Proposition 3

The proof of Proposition 3 occupies Section 4 of Vasseur (2007), pages 14–24. It is organized into 6 explicit steps. Below I trace every inequality step, the tools used, the exponents produced, and their sharpness.

### Setup and Definitions (Section 2, page 4)

**Decreasing domains:**
- B_k = B(1/2(1+2^{-3k})), T_k = 1/2(-1-2^{-k}), Q_k = [T_k,1] × B_k
- B_{k-1/3} = B_{1/2(1+2·2^{-3k})}, B_{k-2/3} = B_{1/2(1+4·2^{-3k})}

**Truncated velocity (level-set energy):**
- v_k = [|u| - (1 - 2^{-k})]_+

**Energy quantity (no pressure term!):**
- U_k = sup_{t∈[T_k,1]} (∫_{B_k} |v_k(t,x)|² dx) + ∫_{Q_k} |d_k(t,x)|² dx dt

**Gradient surrogate:**
- d_k² = ((1-2^{-k}) · 1_{|u|≥1-2^{-k}} / |u|) · |∇|u||² + (v_k/|u|) · |∇u|²

**Cutoff functions:** η_k ∈ C^∞(ℝ³): η_k = 1 in B_k, η_k = 0 in B_{k-1/3}^C, |∇η_k| ≤ C2^{3k}, |∇²η_k| ≤ C2^{6k}.

**Proposition 3 statement:** For every p > 1, there exist universal constants C_p, β_p > 1 such that if U_0 ≤ 1:
> U_k ≤ C_p^k (1 + ||P||_{L^p(0,1;L¹(B_0))}) U_{k-1}^{β_p}    — equation (5)

The critical fact: **β_p < 4/3** for all p, and this is what prevents proving full regularity (which would require β_p > 3/2).

---

### Step 1: Evolution of v_k² (Lemma 11, page 14)

**What is derived:** The PDE satisfied by the level-set energy v_k²:

> ∂_t(v_k²/2) + div(u · v_k²/2) + d_k² - Δ(v_k²/2) + div(uP) + (v_k/|u| - 1) u·∇P ≤ 0    — equation (11)

**Mathematical tool:** Direct computation — multiply NS equation (1) by u(v_k/|u|) and the energy inequality (2) by the complementary factor. The key identity is:
- v_k² = |u|² + (v_k² - |u|²), where the first part uses (2) and the second uses (1)

**NS properties used:**
- div u = 0 (divergence-free velocity)
- Energy inequality (2): ∂_t(|u|²/2) + div(u|u|²/2) + div(uP) + |∇u|² - Δ(|u|²/2) ≤ 0

**Exponents:** None yet — this is an identity step.

**Sharpness:** **EXACT** — this is an identity/inequality derivation, not an estimate. The dissipation term d_k² appears as an exact remainder from the chain rule applied to the truncation. The inequality comes from the energy inequality (2), which is a structural property of suitable weak solutions.

**Key structural observation:** The pressure appears in TWO terms:
1. div(uP) — a divergence form (can be integrated away against test functions)
2. (v_k/|u| - 1) u·∇P — **NOT** in divergence form (this is the problem term)

The factor (v_k/|u| - 1) is bounded by Lemma 10: |u(v_k/|u| - 1)| ≤ 1 - 2^{-k} ≤ 1.

---

### Step 2: Bound on U_k (Energy estimate, equation (13), page 16)

**What is derived:** Multiply equation (11) by η_k(x) and integrate over [σ,τ] × ℝ³ for T_{k-1} ≤ σ ≤ T_k ≤ τ ≤ 1. Taking sup over τ and inf over σ:

> U_k ≤ C2^{6k} ∫_{Q_{k-1}} |v_k|² dx ds + C2^{3k} ∫_{Q_{k-1}} |v_k|³ dx ds + 2 ∫_{T_{k-1}}^1 |∫ η_k {div(uP) + (v_k/|u| - 1)u∇P} dx| dt    — equation (13)

**Mathematical tools:**
- Integration by parts (for the Laplacian term: -Δ(v_k²/2) tested with η_k)
- Triangle inequality
- Bounds on η_k derivatives: |∇η_k| ≤ C2^{3k}, |Δη_k| ≤ C2^{6k}

**How the terms arise:**
- C2^{6k}∫|v_k|² comes from |Δη_k| ≤ C2^{6k} times v_k²/2
- C2^{3k}∫|v_k|³ comes from |∇η_k| ≤ C2^{3k} times |u|·v_k²/2 (using u·v_k²/2 decomposition from Lemma 10, with |u(v_k/|u|)| · v_k²/2 ≤ v_k³/2)
- The pressure integral remains untouched

**Sharpness:** **ESSENTIALLY SHARP** for the cutoff approach. The 2^{6k} and 2^{3k} factors are geometric consequences of the shrinking domains — they affect only the constant C^k in the recurrence, not the exponent β. Different cutoff shapes cannot improve β.

---

### Step 3: Raise of the Power Exponents (Lemma 6, Lemma 12, equation (14), pages 7–18)

This is where the De Giorgi method works its magic, raising the power of U_{k-1} above the natural scaling.

#### Sub-step 3a: Sobolev-interpolation bound (Lemma 6 → equation (10), page 13)

**Lemma 6 (parabolic Sobolev):** For F ∈ L^∞(T_k,1; L²(B_k)) with ∇F ∈ L²(Q_k):

> ||F||_{L^{10/3}(Q_k)} ≤ C (||F||_{L^∞(L²)} + ||F||_{L^∞(L²)}^{2/5} · ||∇F||_{L²}^{3/5})

**Proof structure:** Two steps:
1. **Sobolev embedding H¹ → L⁶ in 3D:** ||F||_{L²(L⁶)} ≤ C(||F||_{L^∞(L²)} + ||∇F||_{L²})
2. **Hölder interpolation:** ||F||_{L^{10/3}} ≤ ||F||_{L^∞(L²)}^{2/5} · ||F||_{L²(L⁶)}^{3/5}

The exponent 10/3 arises from interpolation: in space-time L^{10/3}_{t,x} = interpolation of L^∞_t L²_x and L²_t L⁶_x. Specifically:
- Space: 1/(10/3) = (2/5)·(1/2) + (3/5)·(1/6) = 1/5 + 1/10 = 3/10 ✓
- Time: 1/(10/3) = (2/5)·0 + (3/5)·(1/2) = 3/10 ✓ (interpreting L^∞ as "p=∞")

**Applied to v_{k-1}:** Since ||v_{k-1}||_{L^∞(L²)} ≤ U_{k-1}^{1/2} and ||∇v_{k-1}||_{L²} ≤ ||d_{k-1}||_{L²} ≤ U_{k-1}^{1/2}:

> ||v_{k-1}||_{L^{10/3}(Q_{k-1})} ≤ C · U_{k-1}^{1/2}    — equation (10)

**Sharpness:** **SHARP.**
- H¹ → L⁶ is the optimal Sobolev embedding in 3D: 1/6 = 1/2 - 1/3. Cannot be improved.
- The interpolation L^∞L² ∩ L²L⁶ → L^{10/3} is optimal for the given input norms.
- The exponent 1/2 on U_{k-1} comes directly from the definition: v_k ∈ U_k^{1/2} in L^∞L² and d_k ∈ U_k^{1/2} in L², and 10/3 is the best parabolic exponent from these two ingredients.

**Contribution to β:** This step establishes the **1/2 exponent** on U_{k-1} in the L^{10/3} bound.

#### Sub-step 3b: Chebyshev (Tchebyshev) inequality (Lemma 12, page 17)

**If v_k > 0** then |u| > 1 - 2^{-k}, hence v_{k-1} = [|u| - 1 + 2^{-k+1}]_+ > 2^{-k+1} - 2^{-k} = 2^{-k}.

**Chebyshev inequality:** |{v_k > 0} ∩ Q_{k-1}| ≤ |{v_{k-1} > 2^{-k}}| ≤ 2^{10k/3} · ||v_{k-1}||_{L^{10/3}}^{10/3}

Using equation (10): ||v_{k-1}||_{L^{10/3}}^{10/3} ≤ C · U_{k-1}^{5/3}

**Result for space-time indicator (Lemma 12, first statement):**

> ||1_{v_k>0}||_{L^q(Q_{k-1})} ≤ C · 2^{10k/(3q)} · U_{k-1}^{5/(3q)}

**Result for spatial indicator (Lemma 12, second statement):**

> ||1_{v_k>0}||_{L^∞(T_{k-1},1; L^q(B_{k-1}))} ≤ C · 2^{2k/q} · U_{k-1}^{1/q}

**Sharpness:** **SHARP** as an abstract inequality. Chebyshev/Markov is tight for worst-case functions. The key question is whether NS solutions have additional structure that would make the Chebyshev estimate non-tight — but there is no known improvement.

**Key exponent values:**
- q = 2 (space-time): ||1_{v_k>0}||_{L²} ≤ C · 2^{5k/3} · U_{k-1}^{**5/6**}
- q = 5/2: ||1_{v_k>0}||_{L^{5/2}} ≤ C · 2^{4k/3} · U_{k-1}^{2/3}
- q = 10: ||1_{v_k>0}||_{L^{10}} ≤ C · 2^{k/3} · U_{k-1}^{1/6}

**Contribution to β:** This step produces the **5/6 exponent** when q = 2 is needed for the Hölder pairing.

#### Sub-step 3c: Combined bound on transport terms (equation (14), page 18)

**Bound the first two terms of (13):**

C2^{6k} ∫_{Q_{k-1}} |v_k|² + C2^{3k} ∫_{Q_{k-1}} |v_k|³

Apply Hölder to each term:
- ∫|v_k|² ≤ ||v_k²||_{L^{5/3}} · ||1_{v_k>0}||_{L^{5/2}} = ||v_k||²_{L^{10/3}} · ||1||_{L^{5/2}}
  - ||v_k||_{L^{10/3}} ≤ ||v_{k-1}||_{L^{10/3}} ≤ C U_{k-1}^{1/2} (since v_k ≤ v_{k-1})
  - ||1||_{L^{5/2}} ≤ C 2^{4k/3} U_{k-1}^{2/3}
  - Total: U_{k-1}^{1} · U_{k-1}^{2/3} = U_{k-1}^{**5/3**}

- ∫|v_k|³ ≤ ||v_k||³_{L^{10/3}} · ||1_{v_k>0}||_{L^{10}}
  - ||v_k||³_{L^{10/3}} ≤ C U_{k-1}^{3/2}
  - ||1||_{L^{10}} ≤ C 2^{k/3} U_{k-1}^{1/6}
  - Total: U_{k-1}^{3/2} · U_{k-1}^{1/6} = U_{k-1}^{**5/3**}

**Result:**

> C2^{6k} ∫|v_k|² + C2^{3k} ∫|v_k|³ ≤ C · 2^{αk} · U_{k-1}^{5/3}    — equation (14)

**Exponent 5/3 > 3/2 = scaling exponent.** The De Giorgi method has succeeded in raising the power above criticality for these terms.

**Sharpness:** **SHARP** given the input norms. The Hölder pairings are optimized: both the L² and L³ terms give the same exponent 5/3, confirming the balance is optimal.

---

### Step 4: Bound of the Pressure Term Involving P_{k1} (Non-local Term) — pages 19–20

The pressure integral in (13) is split using Corollary 8:
P|_{B_{k-2/3}} = P_{k1} + P_{k2}

where P_{k1} is harmonic in [T_{k-1},1] × B_{k-2/3} (non-local part) and P_{k2} satisfies -ΔP_{k2} = Σ ∂_i∂_j(φ_k u_j u_i) (local part).

**The pressure integral (13) splits into:**
- (15): ∫ η_k (v_k u/|u|) · ∇P_{k1} dx dt  (non-local, involving ∇P_{k1})
- (16): ∫ η_k {div(u(P_{k22}+P_{k23})) + (v_k/|u|-1)u∇(P_{k22}+P_{k23})} dx dt  (local)

**Corollary 8 bounds on P_{k1}:**
> ||∇P_{k1}||_{L^p(L^∞(B_{k-1/3}))} + ||P_{k1}||_{L^p(L^∞(B_{k-1/3}))} ≤ C2^{12k} (||P||_{L^p(L¹(B_{k-1}))} + ||u||²_{L^∞(L²(B_{k-1}))})

#### Case p > 10 (equation on page 19, first bound):

Hölder triple: L^{10} × L^p × L^q where 1/q = 7/10 - 1/p.

> C · ||v_k||_{L^{10/q}(Q_{k-1})} · ||∇P_{k1}||_{L^p(L^∞)} · ||1_{v_k>0}||_{L^q}

Using (10) and Lemma 12: exponent = **5/3(1-1/p) > 3/2** for p > 10.

**Sharpness:** The exponent exceeds 3/2, so this is **NOT the bottleneck**.

#### Case 2 ≤ p ≤ 10 (page 19, second calculation):

> C · ||v_k||_{L^∞(L²)} · ||∇P_{k1}||_{L^p(L^∞(B_{k-1/3}))} · ||1_{v_k>0}||_{L²(Q_{k-1})}
> ≤ C · 2^{5k/3} · ||∇P_{k1}|| · U_{k-1}^{**4/3**}

**The 4/3 = 1/2 + 5/6 decomposition appears explicitly:**
- **1/2** from ||v_k||_{L^∞(L²)} ≤ U_{k-1}^{1/2} (energy definition)
- **5/6** from ||1_{v_k>0}||_{L²(Q_{k-1})} ≤ C · 2^{5k/3} · U_{k-1}^{5/6} (Lemma 12 with q=2)

**Sharpness:** The Hölder triple (L^∞, L^p, L²) is **constrained by the L² indicator**. The choice q=2 for the indicator forces the 5/6 exponent. Could one use a different Hölder pairing? If we use L^{10/3} for v_k instead:
- 1/(10/3) + 1/p + 1/q = 1, so q depends on p
- For small p, q must be large, giving smaller exponent 5/(3q)
- The sum 1/2 + 5/(3q) increases as q decreases, but is bounded by optimization constraints
- For the L² pairing: 1/2 + 5/6 = 4/3 = **1.333...**
- For the L^∞ pairing (Step 4a): 5/3(1-1/p) → 5/3 as p → ∞

The non-local pressure can ultimately be controlled (β_p > 1 for all p > 1, and > 3/2 for p > 10). **Vasseur explicitly notes this is not the bottleneck.**

#### Case p < 2 (page 20):

Exponent = 5/3 - 2/(3p) > 1 for all p > 1. **Not the bottleneck.**

**Step 4 conclusion (equation (18)):** For any p > 1, there exist α_p, β_p > 1 such that term (15) is bounded by:

> C · 2^{kα_p} · U_{k-1}^{β_p} · (||P||_{L^p(L¹)} + 1)

with β_p > 3/2 for p > 10.

---

### Step 5: Bound of the Pressure Term Involving P_{k2} (Local Term) — THE BOTTLENECK — pages 20–24

This is where the fatal 4/3 exponent is locked in.

#### Sub-step 5a: Three-way split of P_{k2}

Using the identity 1 = (1 - v_k/|u|) + v_k/|u| applied to u_j and u_i in -ΔP_{k2} = Σ ∂_i∂_j(φ_k u_j u_i):

> P_{k2} = P_{k21} + P_{k22} + P_{k23}

- **P_{k21}**: -ΔP_{k21} = Σ ∂_i∂_j{φ_k u_j(1-v_k/|u|) u_i(1-v_k/|u|)}
  - Source involves (1-v_k/|u|)² terms, which are **bounded** (≤ 1)
  - By Riesz theorem: ||P_{k21}||_{L^q} ≤ C_q for all 1 < q < ∞

- **P_{k22}**: -ΔP_{k22} = Σ ∂_i∂_j{2φ_k u_j(1-v_k/|u|) u_i(v_k/|u|)}
  - Cross term, controllable by CZ theory

- **P_{k23}**: -ΔP_{k23} = Σ ∂_i∂_j{φ_k u_j(v_k/|u|) u_i(v_k/|u|)}
  - Pure truncated-velocity term, controllable by CZ theory

#### Sub-step 5b: P_{k21} bound — THE CRITICAL STEP (equation (20), page 21)

The pressure-velocity interaction involves:
> ∫∫ η_k {div(uP_{k21}) + (v_k/|u| - 1)u∇P_{k21}} dx dt    — equation (19)

Using equation (19) and Lemma 10, this splits into:
1. **Divergence part:** div(v_k(u/|u|) P_{k21}) — can be integrated by parts → good terms
2. **Non-divergence part:** -P_{k21} · div(uv_k/|u|) — **CANNOT be integrated by parts**

The non-divergence part is bounded (for q > 2) by:

> C_q · ||P_{k21}||_{L^q} · ||d_k||_{L²} · ||1_{|u|≥1-2^{-k}}||_{L^{2q/(q-2)}}    — second term of (20)

As q → ∞:
- ||d_k||_{L²(Q_{k-1})} ≤ U_{k-1}^{**1/2**} (directly from definition of U_k)
- ||1_{|u|≥1-2^{-k}}||_{L²(Q_{k-1})} ≤ U_{k-1}^{**5/6**} (Lemma 12 with q = 2)

**Result:** exponent = 4/3 - 5/(3q) → **4/3** as q → ∞

Combined with the divergence part: equation (20) gives

> ≤ C_q · 2^{kα_q} · (U_{k-1}^{5/3(1-1/q)} + U_{k-1}^{**4/3-5/(3q)**})

The first term has exponent > 5/3·(1/2) = 5/6 > 4/3 for moderate q. The **second term has exponent → 4/3 as q → ∞**, and this is the global bottleneck.

**Vasseur's commentary (page 21):** "Notice that the second term (with the exponent smaller than 3/2) comes from the second term of the right hand side of (19), namely the pressure term which is not in a divergence form."

#### Sub-step 5c: P_{k22} + P_{k23} bound (page 24)

Using Lemma 13's gradient decomposition:
- ∇P_{k22} = G_{221} + G_{222} + G_{223}
- ∇P_{k23} = G_{231} + G_{232}

with bounds:
- ||G_{221}||_{L^{10/3}} ≤ C2^{3k} ||v_k||_{L^{10/3}}
- ||G_{222}||_{L²} ≤ C ||d_k||_{L²}
- ||G_{223}||_{L^{5/4}} ≤ C ||v_k||_{L^{10/3}} ||d_k||_{L²}
- ||G_{231}||_{L^{5/3}} ≤ C2^{3k} ||v_k||²_{L^{10/3}}
- ||G_{232}||_{L^{5/4}} ≤ C ||v_k||_{L^{10/3}} ||d_k||_{L²}

After extensive Hölder pairings (full page 24), the final bound is:

> ≤ C · 2^{αk} · U_{k-1}^{5/3} + C · U_{k-1}^{**4/3**}

**Vasseur's commentary (page 24):** "Again the exponent 4/3 < 3/2 comes from the pressure term which is not in a divergence form."

The 4/3 here comes from the same mechanism: a term involving ||d_k||_{L²} ≤ U_{k-1}^{1/2} paired with ||1_{v_k>0}||_{L²} ≤ U_{k-1}^{5/6} through an intermediate involving the G_{222} component (which carries the d_k/gradient factor).

---

### Step 6: Conclusion (page 24)

Combining equations (13), (14), (18), and the Step 5 bound:

> **U_k ≤ C_p^k (1 + ||P||_{L^p(0,1;L¹(B_0))}) U_{k-1}^{β_p}**

with β_p > 1 for all p > 1, and β_p > 3/2 for p > 10 (ignoring the local pressure).

**The bottleneck:** For any p > 1, the local pressure term (Step 5) contributes an exponent of 4/3, which is less than 3/2. This prevents using Lemma 4 to conclude full regularity (which requires β > 3/2).

**The exponent 4/3 = 1/2 + 5/6 arises from the product of exactly two factors:**
1. **||d_k||_{L²} ≤ U_{k-1}^{1/2}** — the gradient/dissipation bound (from the energy definition)
2. **||1_{v_k>0}||_{L²} ≤ U_{k-1}^{5/6}** — the measure/indicator bound (from Chebyshev on L^{10/3})

These two factors are forced together by the non-divergence-form pressure interaction -P_{k21}·div(uv_k/|u|), which produces a term requiring a gradient factor (from div) and a measure factor (from the support restriction).

---

## 2. Sensitivity Table

### How β depends on each sub-exponent

| Step | Tool | Exponent contribution to β | Sensitivity dβ/dδ | Sharp? | Notes |
|------|------|--------------------------|-------------------|--------|-------|
| **3a** | Sobolev H¹→L⁶ (3D) | Determines L^{10/3} norm → feeds into 5/6 via Chebyshev | ~1/6 (indirect) | **YES** | H¹→L^{6+δ} would give β = 4/3 + δ/6. But Sobolev exponent 6 is provably optimal in 3D. |
| **3a** | L^∞L² ∩ L²L⁶ interpolation | Determines L^{10/3} exponent | N/A | **YES** | 10/3 is the unique interpolation exponent. Cannot be changed. |
| **3a** | Energy definition U_k^{1/2} | 1/2 in ||v_{k-1}||_{L^{10/3}} ≤ U_{k-1}^{1/2} | Direct (enters 5/6 chain) | **YES** (by definition) | This 1/2 is definitional. |
| **3b** | Chebyshev on L^{10/3} | 5/3 = (10/3)·(1/2) in measure bound | 1/2 (half goes to β via L² norm) | **YES** (abstract) | Chebyshev is tight for arbitrary functions. NS structure unused. |
| **3b→5b** | L² norm of indicator | **5/6 = (5/3)·(1/2)** | **dβ/dδ = 1** (direct additive) | **YES** (given 5/3 input) | q=2 is forced by Hölder pairing in Step 5b. |
| **5b** | Gradient factor ||d_k||_{L²} | **1/2** | **dβ/dδ = 1** (direct additive) | **YES** (by definition) | d_k² is part of U_k. Cannot be improved without changing U_k. |
| **5b** | Non-divergence pressure | Forces Hölder pairing → 1/2 + 5/6 | N/A (structural) | **UNKNOWN** | This is the only step not provably sharp. Could a different decomposition avoid it? |
| **4** | Non-local pressure P_{k1} | β_p > 3/2 for p > 10 | N/A | **YES** | Not the bottleneck for large p. |

### Bottleneck analysis

The sensitivity table reveals:

**β = 1/2 + 5/6 = 4/3, where:**
- The **1/2 is immovable** (definitional — ||d_k||_{L²} ≤ U_{k-1}^{1/2} by construction)
- The **5/6 is locked by the Sobolev+Chebyshev chain**: H¹→L⁶ → L^{10/3} interpolation → Chebyshev gives 5/3 → L² norm gives 5/6

**If the Sobolev exponent improved by δ** (H¹→L^{6+δ}, impossible in 3D):
- L^{10/3} → L^{(10+2δ)/3} (approximately)
- Chebyshev: 5/3 → (5+δ)/3
- L² indicator: 5/6 → (5+δ)/6
- β → 1/2 + (5+δ)/6 = 4/3 + δ/6
- Need δ > 1 to reach 3/2. But Sobolev is sharp in 3D.

**If we could bypass the L² Hölder constraint** (use L^q with q < 2):
- 5/(3q) > 5/6 for q < 2 (better!)
- But then the Hölder conjugate for the gradient factor becomes > 2
- ||d_k||_{L^r} for r > 2 is NOT controlled by U_{k-1}^{1/2} (it requires more regularity)
- **Trade-off: improving one factor worsens the other**

**If NS solutions had additional structure** making Chebyshev non-tight:
- Suppose |{v_k > 0}| ≤ C^k U_{k-1}^{5/3+δ} for some δ > 0
- Then β = 1/2 + (5/3+δ)/2 = 4/3 + δ/2
- Need δ > 1/3 to reach 3/2
- **This is the most promising direction**, but no such structural improvement is known

---

## 3. Free Parameters

### Parameter 1: Truncation function

**Choice:** v_k = [|u| - (1-2^{-k})]_+

**Assessment: CONVENTIONAL but effectively optimal.**

The key properties needed:
1. v_k ≤ v_{k-1} (monotone decreasing in k)
2. {v_k > 0} ⊂ {v_{k-1} > 2^{-k}} (level gap for Chebyshev)
3. v_k ~ |u| - c_k for |u| >> c_k (captures energy above level c_k)

Any truncation satisfying these three properties produces the same exponents. The specific shape [|u| - c_k]_+ = max(|u| - c_k, 0) is the simplest. Smooth truncations (e.g., using mollified max) don't change β, only constants.

**Potential for improvement: NONE** via truncation shape.

### Parameter 2: Sobolev target exponent (L^{10/3})

**Choice:** Parabolic embedding L^∞(L²) ∩ L²(H¹) → L^{10/3}

**Assessment: OPTIMIZED — this is the unique natural exponent.**

The 10/3 is determined by:
- Input: L^∞_t L²_x (energy) and L²_t L⁶_x (Sobolev in 3D)
- Output: L^{10/3}_{t,x} (interpolation)

There are no free parameters here. The only input choice is the Sobolev exponent 6 (from H¹ → L⁶ in 3D), which is sharp.

**Could one use a different parabolic norm?** The De Giorgi iteration requires L^r with r > 10/3 to exceed the scaling. The natural energy gives exactly L^{10/3}. Getting higher r requires additional regularity assumptions, which is circular.

**Potential for improvement: NONE** within the standard energy framework.

### Parameter 3: Hölder conjugate pairs in pressure bound

**Choice in Step 4 (non-local):** For 2 ≤ p ≤ 10, uses (L^∞(L²), L^p(L^∞), L²) triple.

**Assessment: CONSTRAINED but not necessarily optimal for p close to 2.**

The Hölder pairings in Step 4 are **optimized for large p** (the exponent exceeds 3/2 for p > 10). For small p, the exponent is 4/3, but this matches the bottleneck from Step 5 anyway, so optimizing the non-local term cannot help.

**Choice in Step 5 (local):** Multiple Hölder pairings appear. The worst one forces d_k in L² paired with indicator in L², giving 1/2 + 5/6.

**Potential for improvement: EXPLORED** by Vasseur. The Hölder exponents are optimized given the available norms. Different pairings trade off between the two factors but cannot improve the sum.

### Parameter 4: Pressure decomposition P = P_{k1} + P_{k2}

**Choice:** Split into harmonic (non-local) P_{k1} and Calderón-Zygmund (local) P_{k2} using smooth cutoff φ_k.

**Assessment: NOVEL to this paper, but not the source of the limitation.**

This decomposition is Vasseur's key innovation. It isolates the problematic local pressure from the controllable non-local pressure. The further split P_{k2} = P_{k21} + P_{k22} + P_{k23} using 1 = (1-v_k/|u|) + v_k/|u| is also novel and optimal for its purpose.

**Potential for improvement: LIMITED.** The decomposition successfully identifies that the bottleneck is the non-divergence-form interaction of P_{k21} with div(uv_k/|u|). Alternative decompositions (e.g., Choi-Vasseur's approach) redistribute the difficulty but don't eliminate it.

### Parameter 5: Cutoff functions η_k, φ_k

**Choice:** Standard smooth cutoffs with |∇η_k| ≤ C2^{3k}, |∇²η_k| ≤ C2^{6k}.

**Assessment: CONVENTIONAL — only affects C^k constant, not β.**

The cutoff derivatives produce the 2^{6k} and 2^{3k} prefactors in (13). These factors are absorbed into the C^k of the recurrence and do not affect β.

**Potential for improvement: NONE** for β.

---

## 4. Cross-Comparison with Vorticity Formulation (Vasseur-Yang 2021)

### The vorticity approach

Vasseur-Yang (2021) apply De Giorgi iteration to a **localized velocity** v = -curl φ^♯ Δ^{-1} φω, which captures local information from the vorticity ω = curl u. The key advantage: **the pressure disappears entirely** when working with vorticity, since curl(∇P) = 0.

**Equation for v (equation 4.3):**
> ∂_t v + P_curl(φω × u) = **B** + **L** + Δv

where **B**, **L** are commutator terms (lower order) involving cutoff derivatives.

**Key property:** This equation has no pressure! The nonlinearity is purely from the vortex stretching ω·∇u, which manifests as the trilinear P_curl(φω × u) term.

### De Giorgi iteration in the vorticity formulation (Section 5)

**Energy quantities (page 19):** Same structure as Vasseur 2007:
- c_k = 1 - 2^{-k}, v_k = (|v| - c_k)_+, β_k = v_k/|v|, α_k = 1 - β_k
- d_k² = 1_k(α_k|∇|v||² + β_k|∇v|²)
- U_k = ||v_k||²_{L^∞(L²)} + ||d_k||²_{L²}

**Truncation estimates (Lemma 5.2):** Same as Vasseur 2007:
- ||β_k v||_{L^∞L² ∩ L²L⁶ ∩ L²H¹} ≤ 9U_{k-1}^{1/2}  (→ L^{10/3} by interpolation)
- ||1_k||² ≤ C^k U_{k-1}  (Chebyshev)

**Energy estimate (equation 5.4):** After testing the evolution equation with cutoffs:

> U_k ≤ C^k ∫v_k² + {trilinear terms from R(u⊗v)} + {**B**, **L**, **W** terms}

**The quadratic term (equation 5.5):** Same as Vasseur 2007:
> ∫_{Q_k} v_k² ≤ ∫_{Q_{k-1}} |β_k v|² ≤ U_{k-1}^{**5/3**}

This is the same Sobolev + Chebyshev chain: L^{10/3} bound → Chebyshev → Hölder pairing.

### Where the 4/3 appears in the vorticity version

**Trilinear term (equation 5.6, page 23):** The highest-order nonlinearity involves trilinear forms T_∇, T_○, T_div acting on combinations of α_k v, β_k v, and the velocity field. After extensive algebraic manipulation:

> |∬ ρ_k α_k v · ∇R(u⊗v) - ∬ ρ_k div(vR(u⊗v)) - ∬ ρ_k β_k v · W₂| ≤ C^k U_{k-1}^{min{**4/3**, 5/3 - 2/(3p₃)}}

**The 4/3 appears from the trilinear terms that cannot be written in divergence form.** Specifically, terms like T_∇[α_k v, ρ_k^♯ β_k v, β_k v] involve:
- A gradient factor (∇ in T_∇) contributing U_{k-1}^{1/2}
- A Chebyshev indicator factor contributing U_{k-1}^{5/6}

The 5/3 - 2/(3p₃) terms (with p₃ > 1) come from bilinear and lower-order terms (**B**, **L** in equations 5.7-5.8) and always exceed 1.

**Final recurrence (page 26, Proof of Proposition 5.1):**

> U_k ≤ C^k U_{k-1}^{min{5/3 - 2/(3p₃), **4/3**}}

Since p₃ > 1 ensures 5/3 - 2/(3p₃) > 1, and since the 4/3 < 5/3 - 2/(3p₃) for p₃ large enough, **the bottleneck is again 4/3**.

### Comparison of the two formulations

| Aspect | Velocity (Vasseur 2007) | Vorticity (Vasseur-Yang 2021) |
|--------|------------------------|------------------------------|
| **Equation** | NS for u | Vorticity eq for ω = curl u |
| **Pressure** | Present, decomposed as P_{k1}+P_{k2} | **Absent** (curl eliminates ∇P) |
| **Energy quantity U_k** | sup∫|v_k|² + ∫|d_k|² | sup∫|v_k|² + ∫|d_k|² (same structure) |
| **Sobolev bound** | ||v_{k-1}||_{L^{10/3}} ≤ CU_{k-1}^{1/2} | ||β_k v||_{L^{10/3}} ≤ CU_{k-1}^{1/2} (same) |
| **Chebyshev bound** | ||1_{v_k>0}||_{L²} ≤ CU_{k-1}^{5/6} | ||1_k||_{L²} ≤ CU_{k-1}^{5/6} (same) |
| **Source of 4/3** | Local pressure P_{k2} not in div form | Trilinear R(u⊗v) not in div form |
| **1/2 origin** | ||d_k||_{L²} (gradient of truncated vel.) | ||d_k||_{L²} (gradient of truncated vel.) |
| **5/6 origin** | Chebyshev on L^{10/3} | Chebyshev on L^{10/3} |
| **Final exponent** | β < 4/3 | β < 4/3 |
| **Steps with slack** | Same: non-div form interaction | Same: non-div form trilinear |

### Key insight from cross-comparison

**The pressure and the vortex stretching are dual manifestations of the same quadratic nonlinearity.** Taking curl u to get ω converts -∇P (which satisfies -ΔP = Σ∂_i∂_j(u_iu_j)) into ω·∇u (vortex stretching). Both produce a bilinear/trilinear term that **cannot be written in divergence form** when projected onto the truncated variables.

The 4/3 barrier is not an artifact of how the pressure is handled — it is a fundamental constraint of the De Giorgi iteration applied to any formulation of 3D Navier-Stokes with its natural quadratic nonlinearity. The SAME two factors (gradient U^{1/2} and Chebyshev indicator U^{5/6}) combine in the SAME way, regardless of whether one works with velocity+pressure or vorticity alone.

**The improvable steps are the SAME in both formulations:** the only path to improving β would be:
1. A structural improvement to the Chebyshev estimate (exploiting NS-specific properties), or
2. A fundamentally different way to handle the non-divergence-form quadratic interaction, or
3. Working in a different function space where the Sobolev/energy exponents change

---

## 5. Detailed Decomposition of the 5/6 Exponent

The 5/6 is the more promising target for improvement. Here is its complete genealogy:

### Chain producing 5/6:

```
H¹(ℝ³) ↪ L⁶(ℝ³)              [Sobolev embedding, dimension n=3: 1/6 = 1/2 - 1/3]
     ↓
L²_t L⁶_x ∩ L^∞_t L²_x       [available norms from energy]
     ↓ (interpolation)
L^{10/3}_{t,x}                 [parabolic Sobolev: 3/(10/3) = 3/10]
     ↓
||v_{k-1}||_{L^{10/3}} ≤ C U_{k-1}^{1/2}    [equation (10)]
     ↓ (Chebyshev at level 2^{-k})
|{v_k > 0}| ≤ 2^{10k/3} ||v_{k-1}||_{L^{10/3}}^{10/3} ≤ C^k U_{k-1}^{5/3}
     ↓ (L² norm = square root of measure)
||1_{v_k>0}||_{L²} ≤ C^{k/2} U_{k-1}^{5/6}   [5/6 = (5/3)/2]
```

### Step-by-step sharpness assessment of the 5/6 chain:

1. **H¹ → L⁶ (Sobolev):** SHARP in 3D. The exponent 6 = 2n/(n-2) for n=3 is the critical Sobolev exponent. No improvement possible without additional regularity.

2. **L^∞L² ∩ L²L⁶ → L^{10/3} (interpolation):** SHARP. This is a consequence of bilinear interpolation and cannot be improved.

3. **||v_{k-1}||_{L^{10/3}} ≤ U_{k-1}^{1/2}:** SHARP by definition of U_k. The 1/2 comes from square root of the energy.

4. **Chebyshev: |{v_{k-1} > 2^{-k}}| ≤ 2^{10k/3} U_{k-1}^{5/3}:** SHARP as an abstract inequality for arbitrary L^{10/3} functions. **POTENTIALLY LOOSE for NS solutions.** This is the only step in the chain where NS-specific structure (divergence-free, pressure equation, energy cascade) could potentially help. If NS solutions have additional integrability or concentration properties near level sets, the Chebyshev estimate could be non-tight.

5. **L² norm of indicator: ||1||_{L²} ≤ |support|^{1/2} ≤ U_{k-1}^{5/6}:** SHARP given the measure bound. The L² norm is forced by the Hölder pairing in Step 5b.

### The single potentially improvable link:

**Step 4 of the 5/6 chain (Chebyshev)** is the ONLY step that is sharp for general functions but potentially loose for NS solutions specifically. All other steps are either definitional (U_k definition), algebraically optimal (Sobolev, interpolation), or structurally forced (Hölder pairing).

The question is: **do NS solutions near a potential singularity have a controlled distribution function for v_{k-1}?** That is, does the measure |{v_{k-1} > λ}| decay faster than λ^{-10/3} for NS solutions? This is related to:
- Regularity of the level sets of |u|
- Concentration phenomena near singular points
- The Kolmogorov scaling structure of turbulence

No such structural improvement is currently known.

---

## 6. Conclusions

### Summary of findings

1. **The 4/3 = 1/2 + 5/6 decomposition is precise and traceable.** The 1/2 comes from the energy/gradient definition (||d_k||_{L²} ≤ U_{k-1}^{1/2}), and the 5/6 comes from Sobolev embedding H¹→L⁶ → parabolic interpolation to L^{10/3} → Chebyshev at the truncation level → L² norm of the indicator function.

2. **Every step except one is provably sharp.** The Sobolev exponent, interpolation, energy definition, and L² norm extraction are all optimal. The only potentially loose step is the **Chebyshev inequality applied to NS solutions**, which is tight for arbitrary L^{10/3} functions but may not be tight for functions satisfying the Navier-Stokes structure.

3. **The bottleneck is the non-divergence-form pressure interaction**, specifically -P_{k21} · div(uv_k/|u|) in the velocity formulation, or the non-divergence trilinear form in the vorticity formulation. This term requires pairing a gradient factor (1/2) with a measure factor (5/6).

4. **The vorticity formulation (Vasseur-Yang 2021) produces the same 4/3 from the same chain.** The pressure disappears but is replaced by the vortex stretching term ω·∇u, which creates identical non-divergence-form interactions. This confirms the 4/3 is intrinsic to the NS nonlinearity, not an artifact of pressure handling.

5. **There are no free parameters that can improve β.** The truncation shape, Sobolev target, Hölder pairs, and cutoff functions are all either optimized or irrelevant to the exponent.

### The 5/6 is the more interesting target

The 1/2 is definitional and cannot be changed within the De Giorgi framework. The 5/6 is a chain of five steps, of which four are provably sharp and one (Chebyshev for NS) is potentially loose. Any improvement to β must come from:

(a) **Structural Chebyshev improvement:** showing |{v_{k-1} > 2^{-k}}| ≤ C^k U_{k-1}^{5/3+δ} for NS solutions
(b) **Alternative to the Hölder pairing in Step 5b:** finding a way to estimate the non-divergence pressure term that doesn't require d_k ∈ L² paired with 1_{v_k>0} ∈ L²
(c) **Different energy quantities U_k:** modifying the definition to change the 1/2 and/or 5/6 contributions (but this would need a different equation for the level-set energy)

Option (a) requires deep insight into NS level-set structure. Option (b) requires a fundamentally new pressure decomposition. Option (c) requires abandoning the De Giorgi framework.
