# Strategy 002: Focused Gap Repair

## Objective

Repair the single proof gap identified by Strategy 001 — or prove it is irreparable. The gap is: the formula HessS(v,v) = (β/(2N)) Σ|B□(Q,v)|² is NOT an identity at generic Q. Numerically, λ_max(H_actual) ≤ λ_max(H_formula) for all 190+ tested configs, but this inequality needs a proof.

This is NOT a re-exploration. The science is settled: β < 1/6 is novel, the numerics are clean, the convention is resolved, the extensions are tested. The ONLY question is whether the proof gap can be closed. A repair would upgrade the main result from Tier 3 to Tier 1/2. A definitive obstruction characterization is equally valuable — it tells us exactly what's needed for a rigorous proof.

## Context: The Gap

### What's Broken

Step 2 of the proof chain claims: HessS(v,v) = (β/(2N)) Σ_□ |B□(Q,v)|²

This is EXACT at flat connections (U□ = I ∀□) but NOT at generic Q. At generic Q:
- The formula OVERESTIMATES λ_max (actual 2.26 vs formula 3.54 at random Q)
- But the PSD inequality FAILS: some directions have actual > formula (so it's not a pointwise upper bound on the quadratic form)
- Despite this, λ_max(H_actual(Q)) ≤ λ_max(H_formula(Q)) for all tested Q (190+)

### What Would Fix It

Four repair paths were identified (Strategy 001 FINAL-REPORT):

**Path A: Prove λ_max(H_actual(Q)) ≤ λ_max(H_formula(Q)) for all Q.**
Most direct. Numerically: ratio ≈ 0.64 for random Q, ≈ 1.0 for flat Q. For SU(2), v² = -(|v|²/4)I simplifies diagonal terms. Cross terms need work.

**Path B: Prove flat connections maximize H_norm globally.**
Then max_Q λ_max(H_actual(Q)) = λ_max(H_actual(I)) = 4β, and β < N²/(4d). This gives 1/4 for SU(2) d=4 — even stronger than 1/6.

**Path C: Tighten SZZ Lemma 4.1 directly.**
SZZ bounds HessS without B² formula. Their bound gives 8(d-1)Nβ. Need 4(d-1)β/N instead — factor of 2N² improvement in Cauchy-Schwarz step. Seems hard.

**Path D: Bound the actual Hessian directly for SU(2).**
The actual Hessian involves Re Tr((Σ s_k P_k v_k)² · U₀). Use |Re Tr(XU₀)| ≤ |Tr(X)| with X = v² = scalar for SU(2). Strategy 001 flagged this as most promising.

### Key Files

- `../strategy-001/FINAL-REPORT.md` — full validation results and gap description
- `../strategy-001/HISTORY-OF-REPORT-SUMMARIES.md` — all exploration summaries
- `../../../yang-mills/strategies/strategy-002/explorations/exploration-008/REPORT.md` — original proof
- `../../../yang-mills/strategies/strategy-003/FINAL-REPORT.md` — obstruction analysis from prior mission

### Known Obstacles from Prior Mission

The prior yang-mills mission (strategy-003) attempted to prove the conjecture M(Q) ≼ M(I) (PSD inequality) and found it is FALSE. This doesn't kill Paths A or B, but shows that the approach must work at the λ_max level, not the matrix level.

## Methodology: Check-Before-Prove Tournament

**Critical meta-lesson: "Check X numerically before proving X."** Before spending exploration budget proving any inequality, verify it numerically with adversarial search. If it fails numerically, don't waste an exploration trying to prove it.

### Phase 1: Numerical Feasibility Check (1 exploration)

**E001 — Adversarial Stress Test of λ_max Inequality (Math Explorer):**

Build the ACTUAL Hessian (by finite differences) and the FORMULA Hessian (using LEFT B□ formula) for the same Q. Compare λ_max values.

Specifically:
1. Implement actual_hessian(Q, beta) using finite differences of HessS — second derivative of S = -(β/N) Σ Re Tr(U□) with respect to link perturbations.
2. Implement formula_hessian(Q, beta) using M(Q) from the B□ formula (LEFT convention: P3 = Q1·Q2·Q3⁻¹, P4 = U□).
3. For 50+ random SU(2) configs on L=2:
   - Compute ratio r(Q) = λ_max(H_actual(Q)) / λ_max(H_formula(Q))
   - Record the maximum r(Q)
   - If any r(Q) > 1: STOP, the inequality fails, Path A is dead
4. Gradient ascent on r(Q): starting from 10 random Q, maximize r by gradient steps on Q. Run for 500+ steps.
5. If max r(Q) < 1 after all tests: report the gap (1 - max_r). This gap is the "safety margin" for a proof.
6. Also check: for each Q, is the Hessian QUADRATIC FORM H_actual(v,v) ≤ H_formula(v,v) for the top eigenvector of H_actual? (This is weaker than PSD but stronger than λ_max.)

Convention: S = -(β/(2)) Σ Re Tr(U□) with β/N = β/2 for N=2. ALL computations use N=2 throughout.

If the inequality fails: Strategy 002 pivots to obstruction characterization (see "Pivot Protocol" below).

### Phase 2: Proof Attempt Tournament (3 parallel explorations)

Launch only if Phase 1 confirms the inequality holds numerically.

**E002 — Path D: Direct SU(2) Bound (Math Explorer):**

The most promising path. For SU(2), use v² = -(|v|²/4)I to simplify the actual Hessian.

1. Write out the actual Hessian for a single plaquette □ with edges e1,e2,e3,e4. The second derivative of -Re Tr(U□) is:
   Re Tr(d²U□/dt²)|_{t=0} = Re Tr((Σ_k s_k P_k v_k)² · U□) + boundary terms
   where s_k = ±1 are the link orientations and P_k are partial holonomies.
2. For SU(2): if w = Σ s_k P_k v_k P_k⁻¹, then w ∈ su(2) and w² = -(|w|²/4)I.
   So Re Tr(w² U□) = -(|w|²/4) Re Tr(U□) = -(|w|²/4)(2 cos θ) where θ = angle of U□.
3. The key question: is |w|² ≤ Σ|v_k|²? This is where the triangle/CS step enters. For SU(2), Ad is an isometry on su(2), so |P_k v_k P_k⁻¹|² = |v_k|². Then |w|² = |Σ s_k Ad_{P_k}(v_k)|² ≤ (Σ|v_k|)² ≤ 4Σ|v_k|² by CS.
4. Combine: Re Tr(w² U□) ≥ -cos(θ) · 2 · Σ|v_k|² where cos(θ) = Re Tr(U□)/2.
5. Sum over plaquettes, multiply by β/2N, and derive the λ_max bound.
6. VERIFY every step by finite differences on L=2.

Critical question: does Re Tr(d²U□/dt²) equal Re Tr(w² · U□), or are there additional "cross terms" involving derivatives of the partial holonomies? Compute the full second derivative carefully. This is where the gap might be.

**E003 — Path B: Flat Maximizer Proof (Math Explorer):**

Prove that λ_max(H_actual(Q)) achieves its maximum over Q at flat connections.

1. Compute ∂/∂Q [λ_max(H_actual(Q))] at Q = flat using perturbation theory.
   At flat Q: the Hessian is block-diagonalized by Fourier modes. λ_max = 4β with degeneracy d(N²-1).
   A small perturbation δQ shifts λ_max by first-order perturbation: δλ ≈ <v_max|δH|v_max>.
2. If δλ ≤ 0 for all δQ, then flat connections are local maxima.
3. Compute <v_max|δH|v_max> for the staggered mode v_max at a flat connection, with δQ an arbitrary small perturbation.
4. Numerically verify: compute λ_max(H_actual) along lines Q(t) = exp(t·δQ) for 20 random δQ directions, verify λ_max decreases from t=0 (flat).
5. If flat connections are local maxima AND the numerical evidence shows they are global maxima (190+ configs), this is strong (though not rigorous) evidence.
6. For a rigorous proof: can you use a Weitzenböck-type identity? The prior mission suggested M(Q) = M(I) + R(Q) with R(Q) negative-definite. Can R(Q) be shown to decrease λ_max?

**E004 — Path A: Direct λ_max Inequality (Math Explorer):**

Prove λ_max(H_actual(Q)) ≤ λ_max(H_formula(Q)) for all Q.

1. Define: H_actual(Q) = the true Hessian matrix (FD-verified). H_formula(Q) = the B² formula Hessian.
2. Write H_actual = H_formula + E(Q) where E(Q) is the error matrix.
3. At flat Q: E(I) = 0 (formula is exact). At generic Q: E(Q) ≠ 0.
4. Compute E(Q) explicitly for a single plaquette. What is its structure? Is it negative-semidefinite? (Strategy 001 says NO — PSD fails.) What is its rank? Its spectrum?
5. Even though E(Q) is not NSD, can we show λ_max(H_actual) = λ_max(H_formula + E) ≤ λ_max(H_formula)? This requires that the top eigenvector of H_formula doesn't overlap much with the positive directions of E.
6. Compute the spectrum of E(Q) for 20 random Q. How does ||E||_op compare to λ_max(H_formula)? If ||E|| << λ_max(H_formula), a perturbative argument might work.
7. Check: is E(Q) "off-diagonal" in the Fourier basis? If E only mixes different Fourier modes while λ_max is at a single mode, the top eigenvalue might be protected.

### Pivot Protocol

If Phase 1 shows the λ_max inequality FAILS (some r(Q) > 1):

**E002-pivot — Obstruction Characterization (Standard Explorer):**
1. What is the maximum r(Q) found? How much above 1?
2. What Q configurations give r > 1? Do they share structure?
3. Does the bound β < 1/6 still hold even though the formula doesn't bound λ_max? I.e., is λ_max(H_actual(Q)) < 6β for all Q even if λ_max(H_actual) > λ_max(H_formula)?
4. What is the actual tight bound on max_Q λ_max(H_actual(Q))? Is it 4β (flat), 6β, or something else?
5. Can we prove β < 1/(2 · max_Q λ_max(H_actual(Q))/(β)) directly?

### Phase 3: Verdict (1 exploration)

**E005 — Adversarial Verdict:**
After Phases 1-2 complete, write the definitive verdict:

1. Did any path succeed in repairing the gap?
2. If yes: state the repaired proof chain precisely, step by step, with all conventions and SU(2)-specific ingredients.
3. If no: state the obstruction precisely. What inequality would need to hold? What numerical evidence exists for/against? Is this a hard problem or a gap that future work could plausibly close?
4. Update the tier classification: did β < 1/6 upgrade from Tier 3?
5. Final novel claims assessment: what survives as defensible?

## Validation Criteria

### Success
- Gap repaired → Tier 3 becomes Tier 1/2 → mission complete
- Gap proved irreparable → obstruction clearly characterized → mission complete with negative result

### Exhaustion
- All four paths tried or numerically eliminated
- The obstruction (if any) is precisely characterized

### What Would Indicate a Third Strategy Is Needed
- A near-miss: one path almost works but needs a specific technical lemma
- A new insight from Phase 2 that opens a fifth path not considered here

## Methodology Rules

1. **Check numerically before proving.** Phase 1 is mandatory. Do NOT launch proof attempts until the inequality is numerically confirmed.
2. **Computation mandatory.** Every step of every proof attempt must be accompanied by numerical verification on L=2.
3. **Write incrementally.** Write each step as you complete it. If you get stuck for more than 5 minutes, write what you have so far and explain where you're stuck.
4. **Convention: LEFT formula, S = -(β/N) Σ Re Tr.** Every exploration must use this convention. If you're not sure, compute at Q=I and verify λ_max = 4β.
5. **Report cross-terms explicitly.** The gap is in how the second derivative of the Wilson action decomposes. Any time you compute d²S/dt², explicitly identify ALL terms and classify each as "captured by B² formula" or "not captured."
6. **Budget: 5-6 explorations.** Tight budget — this is a focused repair, not a survey.
