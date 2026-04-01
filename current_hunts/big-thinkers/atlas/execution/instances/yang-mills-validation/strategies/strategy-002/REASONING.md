# Reasoning Log

## Exploration 001: Adversarial Stress Test of λ_max Inequality

### Planning

**What I considered:**
- The strategy is very clear: Phase 1 is mandatory — numerically stress-test λ_max(H_actual) ≤ λ_max(H_formula) before any proof attempts.
- This is the ONLY exploration that makes sense to start with. No proof attempts until the numerical foundation is solid.
- Explorer type: Math Explorer (computation, gradient ascent, numerical experiments).

**What I chose:** Follow the strategy exactly — launch E001 as specified in Phase 1.

**Why:** The "check before prove" methodology is sound. Strategy 001 verified this inequality for ~200 configs, but didn't do adversarial gradient ascent specifically targeting r(Q) = λ_max(H_actual)/λ_max(H_formula). That's the gap in our knowledge.

**Key context to provide:**
- The LEFT B_□ formula (P3 = Q1·Q2·Q3⁻¹, P4 = U_□) — CRITICAL, the RIGHT formula gives wrong results
- S = -(β/N) Σ Re Tr(U_□) with N=2 throughout
- At flat Q: formula is exact, λ_max = 4β (verified)
- At random Q: formula overestimates ~36%, but PSD fails (some directions have actual > formula)
- Despite PSD failure, λ_max(H_actual) ≤ λ_max(H_formula) for all ~200 tested configs

**Library query planned:** Ask about the B² formula, Hessian structure, any known results on λ_max comparisons.

### Librarian Findings

Queried the librarian for: B² formula relationship to actual Hessian, LEFT convention, FD lessons, meta-lessons for stress tests.

**Critical finding:** M(Q) ≠ H(Q). The B² formula gives M(Q) = Σ B□ᵀ B□ (the "covariant curl squared"). The actual Hessian of the Wilson action is H(Q) = M(Q) - C(Q), where C(Q) involves second derivatives of the exponential map. C(Q) is NOT PSD. At Q=I, C(I) = 0 so they coincide. Per-plaquette, the ratio H_actual/H_formula can reach 1.936× (actual EXCEEDS formula). But this is the per-plaquette/quadratic-form story — the λ_max story may differ.

**Implication:** The stress test must be precise. We know H_actual(v,v) > H_formula(v,v) for some v (PSD fails). The question is ONLY about λ_max: does max eigenvalue of (M(Q) - C(Q)) ≤ max eigenvalue of M(Q)? This is plausible if C(Q)'s positive eigenspace doesn't align with M(Q)'s top eigenvectors.

**Convention confirmed:** LEFT formula: B□ = v₁ + Ad_{Q₁}(v₂) - Ad_{Q₁Q₂Q₃⁻¹}(v₃) - Ad_{U□}(v₄). Use adjoint Ad_Q(a) = QaQ⁻¹, NOT fundamental Qa.

**Meta-lessons incorporated:** Start with Q=I sanity check (λ_max = 4β), use eigvalsh not ARPACK, test off-diagonal FD, adversarial gradient ascent (≥10 starts), stage computation sequentially.

**Assessment:** Library findings are highly relevant and change how I frame the goal. The explorer needs to understand H = M - C decomposition and test λ_max specifically.

### Reflection (Post-Exploration)

**Did the explorer deliver?** Yes — exceeded expectations. Not only confirmed the inequality holds (PASS across ~300 configs, max non-flat r = 0.981), but identified the precise mechanism: v_top(H_actual)^T · C(Q) · v_top > 0 always. This gives a concrete proof target.

**Was the scope right?** Yes. The 4-stage design worked well. The explorer was thorough with adversarial strategies. One weakness: gradient ascent was done in d=2 not d=4 (computational cost). The structured configs (one-hot π) were actually more adversarial than the optimizer.

**Key insight for Phase 2:** The proof target is now much more precise than before. Instead of "prove λ_max(H_actual) ≤ λ_max(H_formula)", we can target "prove v_top^T C v_top ≥ 0" or equivalently "prove the top eigenspace of H_actual avoids C's negative eigenspace." The gap ∝ ε² near flat connections suggests perturbative analysis could work.

**What would I change?** Specify d=4 as mandatory for gradient ascent. Include one-hot π as a starting config for optimization. Ask for explicit eigenspace decomposition of C in terms of lattice symmetry modes.

---

## Exploration 002 + 003: Phase 2 Proof Attempts (Parallel)

### Planning

**What I considered:**
- Strategy specifies 3 parallel proof paths (D, B, A). Budget is tight (5-6 total, 1 used).
- E001 produced a critical insight: the proof target is v_top^T C v_top ≥ 0, and the gap scales as ε² near flat connections.
- Path D (direct SU(2) bound using v² = -(|v|²/4)I) — most promising per strategy. Addresses the mechanism directly: compute the actual Hessian analytically, identify cross terms, bound using SU(2) identity.
- Path B (flat maximizer) — prove flat connections maximize λ_max(H_actual). E001's gap ∝ ε² result strongly supports this. Perturbation theory at Q=I could prove flat is a local max.
- Path A (direct λ_max inequality via E(Q) structure) — less promising. E001 showed C is messy (not PSD, many negative eigs). Would need eigenspace orthogonality argument which is hard to make rigorous.

**What I chose:** Launch E002 (Path D) and E003 (Path B) in parallel. Skip Path A — its insights are subsumed by Path D (which also computes the actual Hessian structure). Reserve E004-005 for verdict/followup.

**Why:** Path D directly addresses the cross-term structure (the gap's root cause). Path B leverages the strongest E001 finding (gap ∝ ε²). Together they attack from two angles: "bound the Hessian at all Q" vs "prove the max is at flat Q". If either succeeds, the proof is repaired.

**Deviation from strategy:** Launching 2 instead of 3 parallel explorations. Path A is the weakest — E001 already characterized E(Q)'s spectrum extensively. Better to invest that exploration in a targeted followup after seeing Phase 2 results.

### Reflection on E002 (Path D)

**Did the explorer deliver?** Yes — exceeded expectations. Derived the complete analytical formula with all cross terms identified and verified. The formula d²/dt² Re Tr(U□) = -(|w|²/2)cos(θ/2) + (1/2)L⃗·b⃗ is clean and verified.

**Key insight:** The cross terms have cross-product structure (L⃗ = Σ w⃗ᵢ × w⃗ⱼ). These are large (up to 63× the w² term!) and make C indefinite. But C_curv (PSD part) barely compensates C_comm in the top eigenspace (ratio 1.10). This is too slim a margin for a clean algebraic proof.

**New proof direction identified:** The explorer suggested "Strategy A" — bound H_actual directly by c|v|² without going through the B² formula, potentially giving β < 1/3. This is weaker than 1/6 but could be rigorously provable. Worth exploring in E004.

**Also notable:** The eigenvalue-by-eigenvalue inequality holds (0/192 violations). This is MUCH stronger than just λ_max and suggests there might be a deeper structural reason.

**What would I change?** Ask the explorer to compute the direct bound coefficient explicitly. Ask about the eigenvalue-by-eigenvalue ordering — this stronger result might have a simpler proof.

### Reflection on E003 (Path B)

**Did the explorer deliver?** YES — this is the most important result of the strategy. It disproved a key assumption (flat connections maximize λ_max) that was implicitly relied upon by the entire proof chain. It also revealed that E001's "PASS" was incomplete — the λ_max inequality IS violated in the one-hot small-angle regime.

**Impact:** This changes the entire picture:
- Path A (λ_max inequality) is DISPROVED — r > 1 for one-hot at d≥3
- Path B (flat maximizer) is DISPROVED — confirmed
- Path D (direct bound) found the formula but the algebraic bound fails
- The proof gap is WIDER than we thought — the B² formula is not a valid upper bound

**But the excess is small (≤2.6%).** The result β < 1/6 is "approximately correct" but not provable via the B² formula route. A direct bound bypassing the B² formula might still work.

**Key meta-lesson:** E001's 300-config stress test gave a false sense of security. The violation is in a specific regime (single-link, small angle) that wasn't tested. Adversarial stress tests need systematic coverage of perturbation TYPES, not just quantity.

---

## Strategy Synthesis

With E001-E003 complete, the picture is clear:
- The B² formula route (λ_max(H_actual) ≤ λ_max(H_formula)) is definitively BROKEN
- The flat maximizer route (max_Q λ_max = dβ) is definitively BROKEN
- But the excess is tiny (~0.4% at d=4), so β < 1/6 is very close to correct
- The complete analytical Hessian formula is now known (E002)
- A direct bounding approach bypassing the B² formula is the remaining viable path

Proceeding to write FINAL-REPORT.md per instructions.
