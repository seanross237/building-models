# Strategy 003: Verify, Recalibrate, and Close

## Objective

Resolve the three critical unknowns left by Strategy 002, then either complete the proof or declare the conjecture false/modify it:

1. **Is E007's counterexample valid?** (λ_max(M(Q)) ≈ 16.08 via gradient ascent — but may use wrong B-field formula)
2. **What does SZZ actually need?** (M(Q) = Σ B^T B vs the Hessian H(Q) = M(Q) - C(Q) — which appears in the Bakry-Émery condition?)
3. **What is the correct proof target?** (Based on answers to 1 and 2)

This is a VERIFICATION + RECALIBRATION strategy, not a proof construction strategy. Phase 1 resolves the unknowns. Phase 2 acts on the resolution. Do NOT begin proof construction until Phase 1 is complete.

## What's Already Proved (carry forward, DO NOT REDERIVE)

### From Strategy 001 + 002 (15 explorations, adversarial-verified):

**Per-vertex staggered bound (PROVED):**
F_x(Q, T) ≤ 16 ||T||² for all T with Σ T_μ = 0, all Q ∈ SU(2)^E, even L, d=4.

Proof chain: Budget identity → per-plaquette expansion → sum-to-zero extraction → D=I base case → affine-in-D + Cauchy-Schwarz contraction → cancellation.

Key tools: Combined Bound Lemma (scalar), Vector CBL, affine-in-D structure.

This bounds the staggered Rayleigh quotient v^T M(Q) v / |v|² ≤ 16 for all v in the 9D staggered eigenspace.

### What's NOT proved:
- Non-staggered eigenvalues ≤ 16 (max observed: 14.6 random, 16.08 adversarial)
- Full λ_max(M(Q)) ≤ 16

### Dead ends (DO NOT REVISIT):
All from Strategy 001 + 002 dead-end lists, plus:
- Trace identity for general T patterns (FAILS)
- Rank-1 reduction for maximizing T (FAILS — maximizers not always rank-1)
- LEMMA_D and LEMMA_RDR separately (both individually FALSE)

## Methodology: Verify-First Pipeline

### Phase 0: Mandatory Upstream Verification (1 exploration, MUST RUN FIRST)

**THIS EXPLORATION MUST COMPLETE BEFORE ANYTHING ELSE LAUNCHES.**

**Exploration 1: Counterexample Verification + SZZ Framework Clarification**

This is a MATH EXPLORER. It must:

**Part A — Verify E007's counterexample:**
1. Build M(Q) = Σ_□ B_□^T B_□ using EXACTLY the MISSION.md formula:
   B_□(Q,v) = v_{e₁} + Ad_{Q_{e₁}}(v_{e₂}) − Ad_{Q_{e₁}Q_{e₂}Q_{e₃}⁻¹}(v_{e₃}) − Ad_{U_□}(v_{e₄})
   where Ad_Q(v) = QvQ⁻¹ (adjoint representation of SU(2) on su(2) ≅ R³, i.e. the spin-1 SO(3) rotation).
2. CRITICAL: The adjoint representation maps Q ∈ SU(2) to a 3×3 SO(3) matrix via [Ad_Q]_{ij} = (1/2)Tr(σ_i Q σ_j Q⁻¹). Verify this is what you're computing, NOT the fundamental representation Q·v.
3. Verify against known cases: At Q = I, M(I) must have eigenvalue 4d = 16 with multiplicity 9 (staggered modes). At uniform Q with angle θ, check against the Fourier block analysis from E007.
4. Run edge-by-edge gradient ascent (E007's method) on L=2, d=4 with the VERIFIED formula. 20 independent trials. Report max λ_max.
5. If λ_max > 16 is found: save the exact configuration Q* (all link matrices) and DOUBLE-CHECK by computing B_□(Q*, v*) term by term for the maximizing eigenvector v*.

**Part B — SZZ Framework clarification:**
1. Read arXiv:2204.12737 (SZZ) Lemma 4.1. What operator appears in the Bakry-Émery condition? Is it Σ B^T B (our M(Q)), or the full Hessian of the Wilson action (which includes curvature corrections)?
2. Read the specific passage where SZZ define the "Hessian" they bound. Quote the exact formula.
3. If SZZ use the full Hessian H(Q) = M(Q) - C(Q): what is C(Q)? Compute C(Q) explicitly for L=2 random configurations. What is λ_max(H(Q))?
4. If SZZ use M(Q) directly: confirm this and move on.

**Part C — Problem statement resolution:**
Based on A + B, state precisely:
- Is Conjecture 1 (λ_max(M(Q)) ≤ 16) true or false?
- If false, what IS the correct inequality for the mass gap argument?
- What is the new proof target?

### Phase 1: Direction Decision (1 exploration, standard explorer)

**Exploration 2: Synthesis and Direction Setting**

Read E001's report. Based on its findings, decide which of these scenarios we're in:

**Scenario A — Conjecture 1 is TRUE** (E007 used wrong formula):
→ The non-staggered eigenvalues satisfy λ ≤ 16 under the correct formula.
→ Design a focused proof of the non-staggered bound. The staggered proof is already done.
→ Proceed to Phase 2A.

**Scenario B — M(Q) can exceed 16, but SZZ uses the Hessian H(Q)**:
→ Conjecture 1 (as stated) is false, but the mass gap argument uses H(Q) = M(Q) - C(Q).
→ The correction C(Q) may push λ_max(H(Q)) below 16 even when λ_max(M(Q)) > 16.
→ Reformulate the conjecture: λ_max(H(Q)) ≤ 16.
→ Proceed to Phase 2B.

**Scenario C — Both M(Q) and H(Q) exceed 16**:
→ The conjecture is false in all forms.
→ Characterize the true supremum. What mass gap beta does the actual supremum give?
→ Proceed to Phase 2C.

**Scenario D — Something unexpected**:
→ Phase 2D: Investigate further.

E002 must produce a CLEAR recommendation for which Phase 2 to execute.

### Phase 2A: Prove Non-Staggered Bound (3-4 explorations)

If Conjecture 1 is true and the non-staggered eigenvalues are the remaining gap:

- E003: Numerical characterization of non-staggered eigenvalue behavior. How does λ_max grow from 12 (at Q=I) to approach 16? What is the maximizing mode structure? Is there a spectral gap argument?
- E004: Proof attempt using the trace constraint: Tr(R(Q)|_stag) ≤ 0 (proved) ⟹ Tr(R(Q)|_non-stag) ≥ 0. Can this plus the 12→16 gap plus structural constraints close the bound?
- E005: Adversarial review of proof from E004.
- E006 (if needed): Repair or alternative.

### Phase 2B: Reformulated Conjecture (Hessian bound) (3-4 explorations)

If SZZ uses the Hessian and the Hessian bound may hold:

- E003: Compute H(Q) = M(Q) - C(Q) for 500+ configs. What is sup λ_max(H(Q))? Where does it concentrate? What's the top eigenspace?
- E004: If λ_max(H(Q)) < 16 numerically — attempt proof. The curvature correction C(Q) may help (large negative trace).
- E005: Adversarial review.

### Phase 2C: Conjecture False — Characterization (2-3 explorations)

If both M(Q) and H(Q) exceed 16:

- E003: What is the true supremum? Extensive gradient ascent (1000+ trials). Does the supremum scale with L? What mass gap beta does it give?
- E004: Can the SZZ framework be modified? E.g., weaker Bakry-Émery condition, different norm, perturbative correction.
- E005: Final synthesis — what IS the best achievable beta?

### Phase 3: Final Consolidation (1 exploration)

**E007 (or last exploration): Mission Synthesis**

Combine ALL three strategies into a final proof document or obstruction report:
- What was proved (staggered bound, special cases)
- What was falsified (if applicable)
- What the best achievable mass gap bound is
- Novel claims with evidence and adversarial status
- Precise statement of what remains open

## Cross-Phase Rules

1. **Phase 0 MUST complete before Phase 1 begins.** No exceptions.
2. **Compute first.** Every exploration starts with numerical computation.
3. **ONE approach per exploration.** Never present multiple alternatives.
4. **Cross-check ALL formulas against MISSION.md.** The adjoint representation is Ad_Q(v) = QvQ⁻¹, NOT the fundamental Q·v.
5. **Incremental writing.** Write to REPORT.md after every computation. 5-minute rule.
6. **Pre-load the proved staggered bound.** Every goal must include the Strategy 001+002 result as context.
7. **4-5 stages max per goal.**
8. **Report cap: 250 lines.**

## Validation Criteria

**Full success:** Proof of Conjecture 1 (or its correct reformulation), adversarial-verified.

**Strong partial:** Conjecture 1 falsified with verified counterexample + correct reformulation identified + numerical evidence for the reformulation.

**Partial:** Counterexample verified OR SZZ framework clarified, but proof/reformulation incomplete.

**Strategy exhausted:** Phase 0 produces ambiguous results AND Phase 1 cannot resolve the direction.

## Budget

7 explorations maximum. Phase 0 (1) + Phase 1 (1) + Phase 2 (3-4) + Phase 3 (1) = 6-7.

The most likely scenario: Phase 0 resolves the formula question in 1 exploration, Phase 1 sets direction in 1, and the remaining 5 are used for proof/characterization.
