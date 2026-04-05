# Strategy 002: Focused Gap Repair — Final Report

**Date:** 2026-03-29
**Explorations:** 001–003 (3 explorations, all productive)
**Status:** Phase 2 complete — definitive negative result on gap repair

---

## Executive Summary

Strategy 002 attempted to repair the single proof gap identified by Strategy 001: the formula HessS(v,v) = (β/(2N)) Σ|B□(Q,v)|² is not an identity at generic Q. Four repair paths were evaluated (A: λ_max inequality, B: flat maximizer, C: tighten SZZ, D: direct SU(2) bound). After 3 explorations:

**The gap is NOT repairable via the B² formula route.** The inequality λ_max(H_actual) ≤ λ_max(H_formula) is FALSE — it is violated by small single-link (one-hot) perturbations at d ≥ 3, verified at multiple FD step sizes. Flat connections are NOT global maximizers of λ_max(H_actual) at any d ≥ 2.

However, the excess is small (≤ 2.6% at d=2, estimated ≤ 0.5% at d=4), and the complete analytical Hessian formula was derived and verified, opening a direct bounding path that bypasses the B² formula entirely.

**Final classification of β < 1/6:** Tier 3 — numerically supported, proof has an irreparable gap in the B² formula step, but a direct proof may be possible via the analytical Hessian formula.

---

## What Was Attempted

### Exploration 001: Adversarial Stress Test (Math Explorer)

**Goal:** Test whether λ_max(H_actual(Q)) ≤ λ_max(H_formula(Q)) for all Q.

**Result:** PASS for ~300 configs, max non-flat r = 0.981, gap = 0.019.

**Key mechanism found:** v_top(H_actual)^T · C(Q) · v_top > 0 always, where C = H_formula - H_actual. C has many negative eigenvalues (up to 139/192) but the top eigenspace avoids them.

**Verdict (later revised by E003):** The test MISSED the critical regime — small single-link perturbations, which violate the inequality. E001 tested Haar-random (large perturbations) and near-identity (all-link scaled), but not one-hot small-angle.

### Exploration 002: Path D — Direct SU(2) Hessian Computation (Math Explorer)

**Goal:** Compute d²/dt² Re Tr(U□) analytically, identify all cross terms.

**Result:** PARTIAL SUCCESS — complete formula derived and verified.

**The exact SU(2) formula:**

> d²/dt² Re Tr(U□) = -(|w|²/2) cos(θ/2) + (1/2) L⃗ · b⃗

where:
- w = B□(v) = Σ sₖ Ad_{Pₖ}(vₖ) is the covariant derivative
- L⃗ = Σ_{i<j} w⃗ᵢ × w⃗ⱼ is the commutator "angular momentum"
- b⃗ is the su(2) part of U□
- cos(θ/2) = Re Tr(U□)/2

**Verified** against finite differences to O(h²) ≈ 2×10⁻⁷.

**Decomposition:** C = H_formula - H_actual = C_curv + C_comm where:
- C_curv = (β/4)(1-cos(θ/2)) BᵀB — PSD (curvature bonus)
- C_comm — indefinite (cross-product commutator terms)
- C is NOT PSD (41/192 negative eigenvalues)

**Eigenvalue-by-eigenvalue inequality holds** for all tested configs (0/192 violations), which is stronger than the λ_max inequality. This was later shown to be regime-dependent by E003.

### Exploration 003: Path B — Flat Maximizer (Math Explorer)

**Goal:** Prove flat connections maximize λ_max(H_actual(Q)).

**Result:** FAIL — definitively disproved.

**Two independent counterexample mechanisms:**

1. **One-hot perturbations (d ≥ 3):** A single link rotated by small angle θ INCREASES λ_max(H_actual) while λ_max(H_formula) stays exactly at dβ. At d=3: excess 0.2% at θ≈1 (verified at 4 FD step sizes, 9 link/color combos). At d=4: gap/θ² = 0.018 (confirmed at h=1e-4 and h=5e-5).

2. **Complex multi-link configs (d=2):** Random walk ascent found λ_max = 2.052 (2.6% above flat value 2.0), verified at 5 FD step sizes (gap = -0.0523 ± 0.0001).

**Critical finding:** λ_max(H_formula) is EXACTLY invariant under all one-hot perturbations — the B² formula completely ignores single-link rotations. This is why r = λ_max(H_actual)/λ_max(H_formula) > 1 in this regime.

**Flat connections ARE strict local maxima** for multi-link perturbations (negative definite second-order matrix at d=2,3,4). But non-flat configs with higher λ_max exist, separated by valleys.

---

## What Paths Were Eliminated

| Path | Method | Verdict | Evidence |
|------|--------|---------|----------|
| A | λ_max(H_actual) ≤ λ_max(H_formula) | **DISPROVED** | r > 1 for one-hot at d≥3 (E003) |
| B | Flat connections maximize λ_max(H_actual) | **DISPROVED** | d=2: 2.6% excess; d=3,4: one-hot excess (E003) |
| C | Tighten SZZ Lemma 4.1 | Not attempted | Factor 2N² improvement needed; seemed impossible |
| D | Direct SU(2) bound via v² = -(|v|²/4)I | **FORMULA FOUND, BOUND INCOMPLETE** | Cross terms (commutators) prevent algebraic bound (E002) |

---

## What Remains Viable

### Direct Bound (Bypassing B² Formula)

From E002's analytical formula:

H_actual(v,v) = (β/4) Σ□ [|w□|² cos(θ□/2) - L⃗□ · b⃗□]

A direct bound on H_actual would bypass the B² formula entirely:

**Approach 1 — Triangle inequality on cross terms:**
- |L⃗□ · b⃗□| ≤ |L⃗□| · |b⃗□| ≤ |L⃗□| · 2 (since |b⃗| ≤ 2)
- |L⃗□| = |Σ_{i<j} w⃗ᵢ × w⃗ⱼ| ≤ Σ_{i<j} |w⃗ᵢ||w⃗ⱼ|
- Since Ad is isometry: |w⃗ₖ| = |vₖ|
- Combined: a direct bound might give β < 1/(d-1) = 1/3 for d=4 (still 16× improvement over SZZ)

**Approach 2 — Exploit cos(θ/2) ≤ 1:**
- The w² term is bounded by (β/4) Σ|w|² ≤ (β/4)·4·2(d-1)|v|² = 2(d-1)β|v|²
- The cross term adds at most some fraction
- Net bound: H_actual ≤ c·β|v|² where c is between d and 2(d-1)

**Approach 3 — Numerical characterization of true max:**
- E003 found max_Q λ_max(H_actual(Q)) ≈ (d + δ)β where δ is small
- At d=4: δ ≈ 0.018 (from one-hot parametric), giving max ≈ 4.018β
- If one could PROVE max ≤ 4.1β, the threshold would be β < N/(2·4.1) ≈ 0.244 (still 12× SZZ)

### Key Observation: Direct Bound Is Stronger Than B² Route

The B² formula route, even if it worked, would give β < N²/(8(d-1)) = 1/6 through Cauchy-Schwarz + link counting. A direct bound on max_Q λ_max(H_actual) gives β < N/(2·max_ratio), which could be as good as β < 1/4 if max_ratio ≈ d. The B² + CS chain was always lossy — it inflates d=4 to 6 unnecessarily.

---

## Tier Classification Update

**Tier 1 — RIGOROUS (unchanged from Strategy 001):**
1. SZZ Bakry-Émery applies (Corollary 1.6)
2. CS bound |B□|² ≤ 4Σ|v_e|²
3. Link counting: 2(d-1) plaquettes/link
4. λ_max(H) = dβ at Q=I for all d
5. Convention: LEFT formula correct for covariant Hessian
6. Complete analytical Hessian formula (NEW — E002)

**Tier 2 — RIGOROUS WITH CITATION (unchanged):**
7. SZZ original threshold β < 1/48

**Tier 3 — NUMERICALLY VERIFIED, PROOF GAP IS IRREPARABLE VIA B² ROUTE:**
8. β < 1/6 mass gap threshold — B² formula step is false (λ_max(H_actual) > λ_max(H_formula) for one-hot perturbations), but the conclusion is approximately correct (excess ≤ 0.5% at d=4)
9. H_norm ≤ d/(4(d-1)N²) for all Q — 190+ configs from S001, but flat connections do NOT maximize H_actual

**Tier 4 — DISPROVED:**
10. ~~λ_max(H_actual(Q)) ≤ λ_max(H_formula(Q)) for all Q~~ — FALSE for one-hot at d≥3
11. ~~Flat connections maximize λ_max(H_actual)~~ — FALSE at all d≥2

---

## Novel Claims

### Claim 1: Complete Analytical SU(2) Wilson Hessian Formula
- **Claim:** d²/dt² Re Tr(U□) = -(|w|²/2)cos(θ/2) + (1/2)L⃗·b⃗ where L⃗ = Σ_{i<j} w⃗ᵢ × w⃗ⱼ
- **Evidence:** Derived analytically (E002), verified against finite differences to O(h²) ≈ 2×10⁻⁷ for 50+ configurations
- **Novelty search:** The decomposition into w²·U term + commutator term with explicit cross-product structure appears new. SZZ uses a crude bound (Lemma 4.1); CNS uses vertex framework; neither writes the exact formula.
- **Strongest counterargument:** The second derivative of Re Tr(U□) is a standard calculation in lattice gauge theory. The product-of-exponentials expansion may appear in textbooks. However, the specific decomposition C = C_curv + C_comm and the observation that C_curv is PSD while C_comm is indefinite appears to be new.
- **Status:** VERIFIED (formula + decomposition + spectral analysis all FD-checked)

### Claim 2: λ_max(H_formula) Exactly Invariant Under One-Hot Perturbations
- **Claim:** λ_max(H_formula(Q)) = dβ whenever Q differs from flat by rotation of a single link
- **Evidence:** Verified numerically at d=2,3,4 for all angles θ ∈ [0, π] (E003)
- **Novelty search:** Not stated in SZZ, CNS, or Jiang. This is a structural property of the B² Gram operator.
- **Strongest counterargument:** May be a straightforward consequence of the B□ formula structure — one changed link doesn't affect enough plaquettes to change the maximum eigenvalue. But the FACT that H_actual IS affected while H_formula isn't is a fundamental obstruction to the B² approach.
- **Status:** COMPUTED (not proved analytically)

### Claim 3: Flat Connections Are Local But Not Global Maximizers of λ_max(H_actual)
- **Claim:** At d ≥ 2, ∃Q non-flat with λ_max(H_actual(Q)) > λ_max(H_actual(I)) = dβ
- **Evidence:** d=2: λ_max = 2.052 (2.6% above, verified at 5 FD step sizes); d=3: 0.2% one-hot excess; d=4: 0.018·θ² excess coefficient (E003)
- **Novelty search:** Prior work (Strategy 001, 190+ configs) consistently found flat maximizes. The violation is in a narrow regime (small one-hot) that was systematically missed. This finding contradicts E001 and changes the proof landscape.
- **Strongest counterargument:** The excess is tiny (≤ 2.6%) and might be a finite-lattice effect (L=2). Need verification on larger lattices.
- **Status:** CHECKED (verified at multiple step sizes and perturbation types)

### Claim 4: Same-Link Different-Component Hessian Entries Vanish by su(2) Orthogonality
- **Claim:** H_actual[(e,a),(e,b)] = 0 for a ≠ b (block-diagonal in color at each link)
- **Evidence:** Follows from TₐTᵦ + TᵦTₐ = -(δₐᵦ/2)I for su(2) generators (E002)
- **Novelty search:** Standard SU(2) representation theory. Not novel as a fact, but useful as a structural constraint.
- **Status:** VERIFIED

---

## Recommendations for Next Strategy (if any)

1. **Direct bound on H_actual bypassing B² formula (highest priority).** E002's formula gives the exact Hessian. A triangle inequality on the commutator terms (using |L⃗·b⃗| ≤ |L⃗||b⃗| ≤ 2|L⃗|) combined with CS on |L⃗| could give a direct bound. Even β < 1/3 (instead of 1/6) would be a 16× improvement over SZZ and rigorously provable.

2. **Characterize max_Q λ_max(H_actual(Q)) precisely at d=4.** E003 found the one-hot coefficient (0.018·θ²) but not the true maximum via random walk at d=4 (too expensive). Knowing the true max would set the tightest possible Bakry-Émery threshold.

3. **Investigate whether the one-hot excess persists at large L.** All tests were on L=2. If the excess vanishes as L→∞, the proof might still work in the thermodynamic limit.

4. **Consider probabilistic/concentration approaches.** Since the high-λ_max configs have low Wilson action weight (exponentially suppressed at small β), a probabilistic version of Bakry-Émery might avoid needing the worst-case bound.

5. **Do NOT pursue the B² formula route further.** It is definitively broken: H_actual > H_formula in the one-hot regime. Any future proof must bound H_actual directly.

---

## Exploration Summary

| # | Type | Goal | Outcome |
|---|------|------|---------|
| E001 | Math | Adversarial λ_max stress test | PASS for ~300 configs but missed one-hot regime |
| E002 | Math | Path D: Analytical Hessian | Complete formula derived; cross terms identified |
| E003 | Math | Path B: Flat maximizer | DISPROVED — flat not global max at any d ≥ 2 |

**Total explorations used: 3 (of 5-6 budget)**
**Budget saved: 2-3 explorations — strategy conclusive after 3**

---

## Key Lesson for the Mission

The "check numerically before proving" methodology was correct in principle but E001's stress test had a coverage gap. **A stress test that finds no violations is only as strong as its coverage of perturbation types.** E001 tested ~300 configs across multiple adversarial strategies but missed the one-hot small-angle regime that E003 found. The lesson: adversarial tests need systematic parameter-space coverage (all-link vs single-link × large-angle vs small-angle), not just volume (number of configs).

The positive outcome is that the analytical Hessian formula from E002 is a permanent result that opens a direct bounding path. The B² formula was always a convenience — the actual Hessian has a clean cross-product structure that may support a direct proof.
