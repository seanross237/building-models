# Exploration History

## Exploration 001: Line-by-Line Decomposition Audit of β = 4/3

**Goal:** Extract the precise chain of inequalities in Vasseur (2007) Proposition 3 that produces β = 4/3, classify each step as sharp or potentially loose, build a sensitivity table, and cross-compare with Vasseur-Yang (2021) vorticity formulation.

**Outcome: SUCCESS**

The 4/3 = 1/2 + 5/6 decomposes into 5 links, of which **4 are provably sharp and 1 is potentially loose**:

- **1/2**: from ||d_k||_{L²} ≤ U_{k-1}^{1/2} — definitional, immovable
- **5/6**: chain: Sobolev H¹→L⁶ (sharp) → parabolic interpolation to L^{10/3} (sharp) → **Chebyshev at level 2^{-k} giving measure bound U^{5/3} (potentially loose for NS)** → L² norm = U^{5/6} (sharp)

**The Chebyshev inequality at the truncation level set is the SINGLE potentially improvable step.** It is sharp for arbitrary L^{10/3} functions but may not be tight for NS solutions. Improving |{v_{k-1} > 2^{-k}}| ≤ C^k U_{k-1}^{5/3} to U_{k-1}^{5/3+δ} with δ > 1/3 would break the barrier.

No free parameters help — truncation shape, Sobolev exponents, Hölder pairs, pressure decomposition are all optimized or irrelevant to β.

Cross-comparison confirms the 4/3 is **intrinsic to the NS quadratic nonlinearity** — pressure and vortex stretching are dual manifestations of the same obstruction (u⊗u cannot be put in divergence form relative to truncated variables).

**Computation identified:** Level-set distribution |{|u| > λ}| near potential blow-up scenarios. Compare with Chebyshev prediction λ^{-10/3}·(energy)^{5/3}. If actual decay is faster, there's room for improvement.

## Exploration 003: Analytical Chebyshev Improvement and Model PDE Comparison

**Goal:** Determine whether the Chebyshev estimate can be analytically improved for NS solutions, and test universality of β = 4/3 across model PDEs.

**Outcome: SUCCEEDED — All deliverables met**

**The Chebyshev step is NOT independently improvable.** Every attempted route ruled out:
- Support-restricted Chebyshev: weaker than direct in convergent regime
- Hölder interpolation with q ≠ 10/3: total U-exponent is 5/3 regardless of q (flat optimization)
- Lorentz space refinements: affect constants, not decay exponents
- Div-free constraint on |u|: no known mechanism; question OPEN but evidence strongly says NO (truncation destroys div-free)

**Universal formula discovered: β = 1 + s/n** for dissipation H^s in dimension n. Confirmed across all PDEs tested:
- 3D NS: s=1, n=3 → β = 4/3
- 1D Burgers: s=1, n=1 → β = 2 (De Giorgi works)
- 2D NS: s=1, n=2 → β = 3/2 (De Giorgi barely works)
- Critical SQG: succeeds NOT by beating this formula at Chebyshev, but because drift enters multiplicatively (no pressure)

**Key insight:** The gap β = 4/3 vs 3/2 is NOT a proof artifact — it faithfully encodes the NS regularity gap. Improving Chebyshev from L^{10/3} to L^4 is equivalent to improving regularity from H^1 to H^{5/4} (Lions threshold) — circular.

**Most promising remaining direction:** Route 3 — commutator improvement of the nonlinear estimate, following the SQG precedent. SQG succeeds because the drift enters multiplicatively without extra U_{k-1} power. Could the NS nonlinear term be reorganized similarly?

**Unexpected findings:**
- "Does div(u) = 0 improve |{|u| > λ}|?" is genuinely OPEN — no paper addresses it. Publishable either way.
- SQG in Caffarelli-Silvestre extension has β = 4/3 (same as 3D NS!) — improvement is entirely in drift coupling, not Chebyshev chain.
- Fractional NS: De Giorgi β reaches 3/2 only at α = 3/2, missing Lions threshold α = 5/4.

**Computations identified:** (1) DNS distributional sharpness test; (2) Commutator estimate for P_{k21} via Hardy space / CLMS compensated compactness.

## Exploration 004: Commutator / Compensated Compactness Analysis

**Goal:** Determine whether CLMS compensated compactness or commutator estimates can improve β = 4/3, following the SQG precedent.

**Outcome: SUCCEEDED — Route 3 definitively closed**

**Compensated compactness / commutator methods CANNOT improve β = 4/3 for NS.** Three independent obstruction layers:
1. No div-curl structure in truncated fields (both div(u^below) ≠ 0 and curl(u^above) ≠ 0)
2. Non-commutator remainder from div(u^above) ≠ 0 dominates P^{21} at high frequencies (61% of L², 18× at high k)
3. CRW commutator bounds give no improvement for bounded multipliers (||u^below||_{BMO} ≤ 2||u^below||_{L^∞})

**SQG-NS gap is structural:** scalar vs vector (R^⊥ preserves div-free for scalars; no amplitude truncation preserves div-free for vectors), linear vs quadratic coupling, first-order vs second-order cancellation.

**Key takeaway:** β = 4/3 is sharp within the class of techniques using energy inequality + Sobolev + CZ pressure estimates + Chebyshev. To beat 4/3, one must use structural information about NS solutions BEYOND these four ingredients.

**Unexpected findings:**
- Commutator part of P^{21} actually HAS better high-frequency regularity (spectral ratio drops 0.67→0.09 at k=20). But divergence-error remainder completely negates this.
- IF a div-free-preserving truncation existed, commutator improvement COULD work. But no amplitude truncation on vector fields can preserve div-free (topological obstruction).

**New directions identified:**
1. **Frequency-localized De Giorgi:** Littlewood-Paley decomposition with different estimates on low (commutator-amenable) vs high (standard) modes. Div error concentrates at high frequencies.
2. **Div-free truncation existence question:** Likely impossible; rigorous proof would close a loophole.

**Proof gap:** The "β = 4/3 is sharp within energy+Sobolev+CZ+Chebyshev" is informal. A rigorous optimality result would require constructing an adversarial example.

## Exploration 002: DNS Level-Set Distribution vs Chebyshev Bound

**Goal:** Measure whether NS solutions have faster tail decay than Chebyshev μ(λ) ~ λ^{-10/3}, and quantify De Giorgi tightness ratios.

**Outcome: Mixed — Significant constant slack exists but CANNOT improve β**

**μ(λ) tail exponents are IC-dependent:**
- Taylor-Green: p ≈ 10 (3× the Chebyshev 10/3)
- Random Gaussian: p ≈ 8-9 (2.5×)
- ABC Beltrami: p ≈ 2.1 — BELOW 10/3, Chebyshev is tight here

**De Giorgi tightness ratios are ~3-5×, constant in k and flow type.** This constant slack does NOT improve β — it only changes C in U_k ≤ C^k U_{k-1}^β. To improve β, one needs slack scaling as U_{k-1}^{-δ}, which is NOT observed.

**Key takeaway:** The Chebyshev step has moderate constant slack but the slack doesn't accumulate to improve β. ABC shows Chebyshev can be tight for global distributions (p < 10/3). **The β = 4/3 barrier is structural, not distributional.**

**Verification:** 5 computed, 1 checked (resolution convergence), 3 conjectured.

## Exploration 005: Frequency-Localized De Giorgi via LP Decomposition

**Goal:** Determine whether Littlewood-Paley decomposition of P^{21} with commutator estimates on low modes can bypass β = 4/3.

**Outcome: NEGATIVE — LP decomposition cannot improve β**

Four independent lines of evidence:
1. **Spectral peak shift:** Peak LP block of P^{21} shifts to higher j with increasing k. High-frequency content GROWS with De Giorgi level.
2. **Growing I_hi/I_total:** High-frequency bottleneck fraction grows from ~1% (k=1) to ~20% (k=6).
3. **Bernstein penalty:** LP route gives L^{10/3} bounds 5-10× worse than direct CZ.
4. **Analytical chain:** All three LP approaches (Bernstein+L², commutator+Bernstein, paraproduct) introduce irreducible growing factor 2^{αJ}.

**Key takeaway:** CZ already IS the optimal frequency-by-frequency estimate. LP reveals frequency structure that CZ handles implicitly, but cannot improve it. Bernstein exchange rate between regularity and integrability is fixed by dimensional analysis — structural, not technical.

**Unexpected findings:**
- Paraproduct transition: resonance R(u^below, u^above) dominates at low k (~98%), paraproduct T_{u^below}u^above dominates at high k (~99%). Same-frequency interactions control early De Giorgi levels.
- Bernstein verdict flips with k: LP viable at k=1 (inflated sequence decreasing) but fails at k≥4 (increasing) — exactly where it matters.

**Computations identified:** Time-frequency analysis (modulation spaces), non-CZ pressure handling (bypass CZ entirely).

## Exploration 006: Non-CZ Pressure Handling — Direct Energy Estimates

**Goal:** Test whether bypassing CZ bounds on P^{21} via IBP, H¹/BMO duality, or CRW commutators can improve β.

**Outcome: NEGATIVE — No non-CZ route improves β**

Three routes computed:
- **Direct IBP:** β = 1 (WORSE — loses the CZ consolidation gain of 1/3)
- **H¹/BMO duality:** β = 4/3 (SAME — exponent invariant under CZ↔BMO exchange)
- **CRW commutator variant:** β ≤ 1 (SAME as direct — bounded multiplier blocks improvement)

DNS confirms CZ bound is 2-3× tighter than direct bound at low k. Both overestimate I_k by 5-20×. Effective β_eff ≈ 2-3 in practice.

Literature survey (12 published approaches): NO published work achieves β > 4/3 by any method.

**Key takeaway: β = 4/3 is TOOL-INDEPENDENT.** The CZ consolidation gain maps the bilinear product to a single L^p function, extracting exactly 1/3 from the Chebyshev level-set. H¹/BMO reproduces the same 1/3 through different mechanism (BMO absorbs P^{21}, H¹ of v_k carries full 4/3). The exponent is locked to the NS quadratic structure.

**Unexpected:** CZ becomes loose at high k — ratio ||P^{21}||_{L^{3/2}}/||v_{k-1}||_{L^2}^2 grows from 0.2 (k=2) to 92 (k=5). CZ most effective at low De Giorgi levels.

**Computations identified:** Wolf's local harmonic+particular pressure decomposition (genuinely CZ-free, untested for β).

## Exploration 007: Adversarial Review of β = 4/3 Obstruction and Novel Claims

**Goal:** Stress-test the comprehensive obstruction result and evaluate five novel claims.

**Outcome: The obstruction SURVIVES adversarial review.**

Literature search (15 papers) confirms no published β improvement in 18 years. Vasseur himself confirmed in March 2025 survey (arXiv:2503.02575). All seven closure arguments withstand attack. Three combination attacks (commutator+LP, modified functional+embedding, truncation+compensated compactness) all fail for structural reasons.

**Novel claim assessment (ranked by publishability):**
1. **Claim 3 (informal sharpness — seven-route obstruction):** Most significant. Genuinely new work. Needs formalization; SDP approach could provide rigor.
2. **Claim 2 (SQG-NS gap):** Correct and useful. 3-dimensional structural comparison not consolidated elsewhere.
3. **Claim 4 (div-free level-set question):** Genuinely open per literature search. Likely negative for pure div-free (toroidal counterexample), but NS-specific version is the harder, interesting question.
4. **Claim 1 (β = 1+s/n):** Correct but elementary. Formula implicit/unstated in literature — novelty is in tabulation.
5. **Claim 5 (paraproduct transition):** Computational observation, low significance.

**Combined publishability:** Claims 1-4 together form a publishable paper.

**Missing directions identified:**
1. SDP/computer-assisted proof of Chebyshev sharpness — most actionable, could formalize Claim 3
2. Non-CZ pressure handling — NOTE: already completed in E006 with negative result
3. Probabilistic regularization by noise

**Unexpected finding:** Tao (2016) independently explains the obstruction: any method based only on energy identity + harmonic analysis cannot resolve NS regularity. This is exactly what β = 4/3 reflects.

**Computation identified:** SDP relaxation to rigorously bound |{|u|>λ}| under NS constraints (div-free, energy, Sobolev). Feasible ~100-line Python/CVXPY. Would upgrade Claim 3 from informal to rigorous.

## Exploration 008: SDP Formalization of Chebyshev Sharpness Under NS Constraints

**Goal:** Determine whether Chebyshev can be improved under NS constraints (div-free, energy, enstrophy). If tight, completes proof that β = 4/3 is optimal.

**Outcome: SUCCESS — Chebyshev is provably tight under all NS constraints**

The core result is elementary: **the constant vector field u(x) = (c, 0, 0) is divergence-free, lies in H¹(T³), and achieves Chebyshev ratio → 1 as λ → c⁻.** One-line construction proves no NS structural constraint can improve the Chebyshev exponent.

**Verification:** 7 verified, 6 computed, 1 checked, 1 conjectured.

**All four steps of the De Giorgi chain are individually tight under NS constraints:**
- Energy definition: tight (by construction)
- Sobolev H¹→L⁶: tight (known, checked)
- Parabolic interpolation: tight (verified)
- Chebyshev: tight (constant field extremizer — verified)

The constant div-free field simultaneously extremizes three of four steps.

**Key takeaway: β = 4/3 is SHARP for the De Giorgi–Vasseur framework.** Combined with the seven-route obstruction (E001-E007), this provides a rigorous computational formalization of the sharpness claim.

**Unexpected:** L² norm constraint improves level-set bound by constant factor 10-200× via pointwise dual, but never changes the exponent. Kato inequality gap (ratio ≈ 0.36) for multi-component div-free fields.

