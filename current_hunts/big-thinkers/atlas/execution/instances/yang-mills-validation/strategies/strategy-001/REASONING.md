# Reasoning Log

## Iteration 1 — Phase 1: Three Parallel Proof Audit Explorations

### What I'm doing
Launching all three Phase 1 explorations simultaneously as specified by STRATEGY.md:
- E001: Independent proof rederivation (Math Explorer)
- E002: CNS paper analysis (Standard Explorer)
- E003: B-square formula and convention verification (Math Explorer)

### Why this ordering
The strategy mandates all three in parallel — they're independent. E001 rederives the proof from scratch (without reading the prior mission's proof first). E002 reads the CNS papers for novelty assessment. E003 verifies the corrected B-square formula. Results from all three feed into the Phase 1 checkpoint.

### Librarian query results
Queried the librarian for: SZZ Hessian bound details, CNS paper analysis, B-square formula corrections, convention issues, meta-learning on goal design.

Key findings used in goal design:
- **Convention warning**: SZZ convention S = -(β/N) Σ Re Tr gives λ_max = 4β; raw convention gives 8β. The 1/N factor is critical. I'm including the explicit convention table in each GOAL.md.
- **B-square formula was corrected**: The original formula had wrong parallel transport for backward edges. Correct formula verified by finite differences. I'm preloading the CORRECT formula for E003 to verify.
- **CNS Sept 2025 uses vertex sigma-model**: Different from SZZ edge approach. Their threshold is β < 1/24. They use Durhuus-Frohlich slab condition. The prior mission's library says our Fourier approach is "not found in literature."
- **Meta-lessons applied**:
  - Include Q=I sanity check as Task 0 in every math exploration
  - Stage computations: sanity check → core derivation → numerical verification
  - Specify failure paths explicitly
  - Preload convention table and known structural properties

### Scope decisions
Each exploration is tightly scoped to one task. E001 does NOT read the prior proof first — it derives independently from SZZ, then compares. E002 reads actual papers via web search. E003 does numerical verification with explicit finite-difference checks.

### Risk assessment
- Convention errors are the highest-risk failure mode (confirmed by prior mission history)
- E001 might get a different number than 1/6 due to convention issues — this is actually the most valuable possible outcome
- E002 might find CNS already prove 1/6 — this kills the novelty claim
- E003 might find the B-square formula is still wrong — this would be critical

---

### Phase 1 Interim Analysis (E001 + E002 done, E003 in progress)

**E002 verdict:** β < 1/6 is genuinely novel — NOT in either CNS paper. CNS Sept 2025 is limited to β < 1/24 by their vertex σ-model (tight at staggered mode). CNS May 2025 is limited to ~1/87. All six Atlas claims absent from both papers. Clear (c) verdict.

**E001 verdict:** β < 1/6 independently confirmed. BUT E001 found a potential COUNTEREXAMPLE to Conjecture 1: U_all = iσ₃ gives H_norm = 1/8 (> 1/12). This would disprove the conjectured β < 1/4 extension while confirming β < 1/6 is exactly tight.

**Critical analysis of E001's counterexample:**
1. E001's code uses P3 = Q1·Q2 (not Q1·Q2·Q3†) and P4 = Q1·Q2·Q3† (not U_□). This is the OLD formula that the prior mission corrected.
2. However, this may correspond to a RIGHT-perturbation convention (Q → Q·exp(tv)) vs the prior mission's LEFT convention (Q → exp(tv)·Q). I derived that:
   - LEFT B_□: v₁ + Ad_{Q₁}(v₂) - Ad_{Q₁Q₂Q₃⁻¹}(v₃) - Ad_{U_□}(v₄) → matches prior mission's corrected formula
   - RIGHT B_□: v₁ + Ad_{Q₁}(v₂) - Ad_{Q₁Q₂}(v₃) - Ad_{Q₁Q₂Q₃⁻¹}(v₄) → matches E001's formula
3. The LEFT and RIGHT Hessian matrices are related by H_L = T^T H_R T where T = diag(Ad_{Q_e⁻¹}). Since T is an isometry, they have the SAME eigenvalues.
4. If this eigenvalue equivalence holds, then the corrected formula would ALSO give λ_max = 6β at U_all = iσ₃, and Conjecture 1 is false.
5. E001 only verified DIAGONAL elements by FD (not off-diagonal), so the FD check is insufficient to fully validate the formula.

**The resolution depends on E003:** E003 should compute the full Hessian at U_all = iσ₃ using the corrected formula and verify the eigenvalue. This is the single most important computation of Phase 1.

### Phase 1 Resolution (E003 computation complete)

E003's explorer session failed (stuck thinking twice), so I ran the critical computation directly.

**RESULT: The eigenvalue equivalence argument was WRONG.** The LEFT and RIGHT B_□ formulas give DIFFERENT eigenvalues at Q ≠ I:
- LEFT (corrected, P3 = Q1·Q2·Q3⁻¹): λ_max = 4β at U=iσ₃ → Conjecture 1 SURVIVES
- RIGHT (E001's, P3 = Q1·Q2): λ_max = 6β at U=iσ₃ → ARTIFACT

The LEFT formula was verified by finite differences (diagonal AND off-diagonal). The key insight is that the LEFT and RIGHT formulas are NOT related by a simple block-diagonal isometry — the partial holonomies themselves change under the convention swap, so the abstract "same eigenvalues" argument doesn't apply to these specific matrix implementations.

**Phase 1 checkpoint:** No proof errors found. β < 1/6 confirmed correct and novel. Conjecture 1 survives (not refuted). Proceed to Phase 2.

### Reflection on Phase 1
- E001 delivered the core verification (β < 1/6 confirmed) but the "counterexample" was a red herring caused by the wrong B_□ formula
- E002 delivered clean novelty assessment — well-scoped task
- E003's explorer failed but the direct computation resolved the critical question
- The most valuable finding was the convention analysis: understanding WHY left and right give different eigenvalues deepens understanding of the B_□ formula
- Meta-lesson: "independent rederivation" can independently reproduce known errors. Need to specify LEFT perturbation convention explicitly.

---

## Iteration 4 — Phase 2: Numerical Extension

### Phase 2 Planning

Per STRATEGY.md, Phase 2 has three parallel explorations:
- E004: Large lattice verification (L=8+, Math Explorer)
- E005: SU(3) extension (Math Explorer)
- E006: d=5 anomaly resolution (Math Explorer)

**Important corrections from Phase 1:**
All math explorations in Phase 2 MUST use the LEFT B_□ formula (P3 = Q1·Q2·Q3⁻¹, P4 = U_□). Must explicitly specify this in every GOAL.md, with the convention table and the warning about the wrong RIGHT formula.

**Budget consideration:** I've used 3 explorations (Phase 1). Strategy says 8-10 total. Phase 2 would use 3 more (6 total). That leaves 4 for Phase 3 adversarial. But E003 didn't produce a deep analysis — just the critical test. I might want to roll some E003 tasks (structural properties, full eigenvalue verification) into Phase 2.

**Decision:** Proceed with all three Phase 2 explorations in parallel. The large lattice test (E004) is the highest priority — it's the strongest evidence for/against Conjecture 1. SU(3) (E005) and d=5 (E006) are important for understanding the conjecture's scope.

### Phase 2 Results

**E004 (Large lattice):** L=4 and L=6 verified. 71 configs total, zero violations. Flat connections uniquely saturate at 1/12. Pattern is L-independent. ARPACK artifact caught and resolved. Explorer timed out on gradient ascent (stuck in 2.5-hour thinking loop).

**E005 (SU(3)):** Corrected the conjecture to H_norm ≤ d/(4(d-1)N²) (N² not N). SU(3) gives H_norm(I) = 1/27. 120+ configs tested, all within bound.

**E006 (d=5):** λ_max = dβ for ALL d (universal). Staggered mode saturates only for even d. Odd d uses "half-staggered" modes with traceless direction vectors. The prior mission's H_norm formula for odd d was wrong.

### Phase 2 Reflections
- The numerical evidence is now very strong: 190+ configs across L=2,4,6, SU(2), SU(3), d=3,4,5,6 — zero violations
- Two corrections to prior mission: (1) N² not N in conjecture, (2) formula wrong for odd d
- The L-independence of H_norm values is a strong indicator that the bound is a LOCAL property
- Flat connections being the unique maximizers is consistent with the Weitzenböck decomposition M(Q) = M(I) + R(Q) with R(Q) negative

---

## Iteration 7 — Phase 3: Adversarial Review + Final Synthesis

### Planning

I have 4 explorations left (budget 10, used 6). Strategy calls for:
- E007: Adversarial proof review (Standard Explorer) — try to find gaps in the proof
- E008: Final synthesis with novel claims assessment (Standard Explorer)
- E009-010: Reserve for deeper investigation of any issues found

### What I considered
1. **Full adversarial review of the proof chain** — Standard Explorer reads the prior mission's proof (E008 from yang-mills strategy-002) and tries to find errors, with special focus on: (a) the triangle inequality step, (b) the CS bound saturation question, (c) the Bakry-Émery → mass gap step
2. **Final synthesis** — collate all validation findings into a coherent assessment
3. **Deeper gradient ascent** — more aggressive search for H_norm > 1/12 counterexamples
4. **Formal gap analysis** — what would be needed for a rigorous paper?

### Decision
Run E007 (adversarial review) and E008 (formal gap analysis) in parallel.

### CRITICAL FINDING: E007 Adversarial Review

E007 found a GENUINE GAP: HessS(v,v) ≠ (β/(2N)) v^T M(Q) v at generic Q.

**Verified by direct computation (verify_formula_generic_q.py):**
- Random Q (seed 42): formula λ_max = 3.54, actual λ_max (FD) = 2.26
- Formula overestimates ALL diagonal elements but PSD inequality FAILS
- Some directions have actual HessS > formula value

**Key nuance:** The formula bounds λ_max but NOT the full Hessian matrix. The proof chain needs repair:
- λ_max(H_actual(Q)) ≤ λ_max(H_formula(Q)) holds numerically for all tested Q
- λ_max(H_formula(Q)) ≤ 6β (by CS)
- So β < 1/6 appears correct but requires proving λ_max(H_actual) ≤ λ_max(H_formula)

**Status:** β < 1/6 is Tier 3 (numerically verified, proof has a gap that needs repair). NOT Tier 1/2.

---

