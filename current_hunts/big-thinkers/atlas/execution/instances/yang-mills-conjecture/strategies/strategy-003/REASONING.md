# Reasoning Log

## Exploration 001: Phase 0 — Counterexample Verification + SZZ Framework Clarification

### What I considered

This is a mandatory Phase 0 exploration per the strategy. The strategy is explicit: verify E007's counterexample (λ_max ≈ 16.08) and clarify the SZZ framework before doing anything else.

### Library query results

Queried the librarian about E007 counterexample, SZZ framework, and math explorer goal design. Key findings:

1. **E007 formula likely wrong**: Meta-inbox (s002-meta-exploration-007.md) directly flags that E007 may have used fundamental representation (Q·v) instead of adjoint (QvQ⁻¹). The explorer built M(Q) from scratch without cross-checking against MISSION.md formula.

2. **SZZ uses HessS(v,v) = (β/2N) · v^T M(Q) v**: The Hessian IS proportional to M(Q), not structurally different. This means Scenario B (SZZ uses full Hessian H(Q) = M(Q) - C(Q)) is likely wrong — there's no separate curvature correction C(Q) that matters. Bounding λ_max(M(Q)) ≤ 16 IS equivalent to H_norm ≤ 1/12.

3. **Meta-learning for goal design**: Stage computations sequentially (Q=I sanity check first), specify exact parameters (L=2, d=4, SU(2)), require finite-difference verification of the B-field formula, use 10+ independent adversarial optimization starts.

4. **Non-staggered eigenvalue data**: For random Q, non-staggered max reaches 14.6 (from base 12 at Q=I). Full eigenspace adversarial search found max 15.997 across 110K+ tests. The gap between 14.6 and 16 is significant.

### What I chose and why

Following the strategy exactly — Phase 0 Math Explorer with three parts:
- Part A: Verify E007's counterexample with correct adjoint formula
- Part B: Clarify SZZ framework (may be simpler than expected given library findings)
- Part C: Determine the correct proof target

The library findings suggest this exploration will likely resolve as Scenario A (Conjecture 1 is TRUE, E007 used wrong formula). But I need computational verification, not just reasoning.

### Goal design decisions

- Using Math Explorer (computation-heavy verification task)
- Including Q=I sanity check as Stage 0 (per meta-learning)
- Providing the exact B-field formula and adjoint representation definition
- Requesting 20+ independent gradient ascent trials
- Including the library's finding about HessS proportionality to pre-answer Part B
- Capping at 5 stages per meta-learning on scope

### Post-exploration reflection

**Did the explorer deliver what I asked?** YES — exceeded expectations. Not only verified the counterexample but found a much cleaner one (Q=iσ₃ giving λ_max=24 exactly) and resolved the HessS vs M(Q) question definitively.

**Was the scope right?** Perfect. Five stages, all completed, no bloat. The staged design was critical — Stage 0 validation caught nothing (formula was correct), but Stage 2's Hessian check was the breakthrough.

**Key surprise:** The library claimed HessS = (β/2N)M, which was WRONG. This changes everything. Two full strategies were optimizing the wrong quantity.

**What I'd do differently:** Nothing significant. The goal was well-scoped. If anything, I'd have asked the explorer to also derive C(Q) analytically, but that's a natural next exploration.

**Direction resolution:** We're in Scenario B. Conjecture 1 (on M) is false. The revised conjecture (on HessS) is the correct target. This is the most important finding so far in the mission.

### Planning Exploration 002

**Scenario B confirmed.** The strategy says Phase 2B:
- E003: Compute H(Q) = M(Q) - C(Q) for 500+ configs
- E004: If λ_max(H(Q)) < 16 numerically — attempt proof
- E005: Adversarial review

But I'm deviating from the numbered strategy plan. The strategy's Phase 1 (E002: synthesis and direction setting) is unnecessary — E001 already definitively established Scenario B. Skipping Phase 1 saves an exploration.

**My next exploration (E002):** The most critical gap is analytical. I need to know:
1. What IS the curvature correction C(Q)? Derive it from the Wilson action.
2. Why does the Hessian bound hold at Q=iσ₃ when M's bound doesn't?
3. What is the explicit formula for HessS in terms of link variables?

This is a MATH EXPLORER task — deriving the Hessian of the Wilson action analytically and computing C(Q) = M(Q) - (2N/β)HessS.

In parallel, I should run a broad numerical survey of λ_max(HessS) — but that might be better as a separate exploration to keep scope tight. Let me combine them: E002 derives C(Q) analytically AND verifies numerically.

### Post-E002 reflection

**Did the explorer deliver?** YES — excellent. Derived the full Hessian formula, verified it at Q=I and Q=iσ₃, cross-checked against finite differences (12 configs, max rel err < 1.4e-6), and characterized the correction.

**Key structural insight:** Self-terms are (β/N) δ_{ab} Σ_{□∋e} Re Tr(U_□). Since Re Tr(U_□) ≤ 2 for SU(2), self-terms are maximized at flat connections. The self-term correction C_self ≥ 0 always. Cross-terms can partially compensate but have bounded operator norm.

**Surprise correction to E001:** E001 claimed HessS ≠ (β/2N)M at Q=iσ₃. E002 shows this was WRONG — both Q=I and Q=iσ₃ are flat connections where the equality is exact. E001 had a normalization/basis issue. This is important: it means the "curvature correction" story from E001 was partially wrong. At flat connections, there IS no correction. Away from flat, the self-terms decrease (C_self ≥ 0), and the question is just about cross-terms.

**Was the scope right?** Almost perfect. Could have pushed further on the proof direction, but derivation + verification was the right first step.

**What E001 got RIGHT:** Conjecture 1 IS false (M can exceed 4d). The revised conjecture on HessS IS the right target. The Hessian IS bounded by 4d at flat connections.

**What E001 got WRONG:** The claim that HessS differs from (β/2N)M at flat connections (iσ₃). This was a normalization error between the ℝ³ basis and the iσ_a basis.

## Planning Exploration 003: Proof of the Hessian Bound

### Options considered

A. **Large-scale numerical survey** of λ_max(HessS) — more evidence but no proof.
B. **Focused proof attempt** using the self-term dominance mechanism.
C. **Resolve E001/E002 normalization discrepancy** — secondary, Hessian is what matters.

### Decision: B — Proof attempt

The key structural insight from E002 is:
1. At flat connections, HessS = (β/2N)M and λ_max = 4d.
2. Self-terms decrease monotonically away from flat (C_self ≥ 0).
3. Cross-terms can increase but have bounded operator norm.

A proof could work by:
- Decomposing HessS = H_self + H_cross
- Showing H_self ≤ 4d·(avg Re Tr/2) where avg Re Tr ≤ 2
- Showing H_cross operator norm ≤ some bound < (self-term reduction)
- Or: showing the full Hessian has a Fourier block-diagonal structure at flat connections that persists perturbatively

I'll design a Math Explorer goal that attempts the proof using two approaches: (1) self-term dominance + cross-term bound, (2) Fourier/spectral analysis.

But I also need to be careful about normalization. I'll pin the basis explicitly in the goal.

### Post-E003 reflection

**Did the explorer deliver?** YES — excellent work. Produced a conditional proof of λ_max ≤ 4d, identified the one missing lemma ("decoherence"), and — most importantly — discovered that the mass gap depends on |λ_min|, not λ_max.

**Key reframing:** The mass gap threshold is β < 2/sup|λ_min|. Our λ_max bound gives only β < 1/8 (because we'd use λ_max as a proxy for spectral radius). But if |λ_min| ≤ 2d (numerically observed), β < 1/4 — the original target from MISSION.md!

**What's remaining (budget: 4 more explorations):**
1. Prove the decoherence lemma (completes λ_max proof, gives β < 1/8)
2. Characterize and prove |λ_min| ≤ 2d (gives β < 1/4)
3. Adversarial review
4. Final synthesis

**Reframing the direction:** The original conjecture (λ_max(M) ≤ 16) was wrong. But the correct conjecture may be even better than expected: if |λ_min(HessS)| ≤ 2d, we get the full β < 1/4 from the Bakry-Émery framework directly.

## Planning Exploration 004: Two parallel tasks

I'll run TWO parallel explorations to maximize efficiency:

**E004a (Math Explorer): Decoherence Lemma + λ_min Bound**
The decoherence lemma and the λ_min bound are related — both involve understanding how the cross-term C(Q) behaves away from flat connections. A single Math Explorer can tackle both:
- Prove ||C(Q)|| ≤ ||C_flat|| (decoherence)
- Characterize sup |λ_min(HessS)| and attempt proof |λ_min| ≥ -2d

Wait, should I split or combine? The decoherence lemma is about the cross-term operator norm, while the λ_min bound is about the whole Hessian's minimum eigenvalue. They're related but different.

Let me think... The D+C decomposition gives:
- λ_max(H) ≤ D_max + C_max ≤ 2(d-1) + C_max
- λ_min(H) ≥ D_min + C_min ≥ -2(d-1) + C_min

At flat: D = 2(d-1), C has eigenvalues in [-2(d-1), 2(d+1)].
λ_max = 2(d-1) + 2(d+1) = 4d
λ_min = 2(d-1) + (-2(d-1)) = 0

For the mass gap, the question is: how negative can λ_min get?
λ_min(H) ≥ D_min + λ_min(C)
The D_min = -2(d-1) is achievable when Re Tr(U_□) = -2 (anti-instanton).
C_min at that config: depends on the cross-terms with Re Tr = -2.

Numerically, λ_min ≈ -8.5 for d=4. Is this -2d or -(2d+1) or what?

I think the best approach is a single Math Explorer that:
1. Does gradient DESCENT to find the most negative λ_min(HessS) across many configs
2. Characterizes the extremal configs (what makes λ_min most negative?)
3. Attempts to prove the decoherence lemma
4. If possible, derives a bound on |λ_min|

This is one coherent exploration. Let me do it.

Actually, I'm now at 4 explorations remaining (of 7 total budget). Let me allocate:
- E004: λ_min characterization + decoherence lemma proof attempt (Math Explorer)
- E005: Adversarial review of conditional proof (Standard Explorer)
- E006: Final synthesis (Standard Explorer)
- E007: Reserve for repair/additional investigation

The decoherence lemma is likely the harder of the two. But the λ_min bound is more impactful for the mass gap. Let me prioritize λ_min.

### Post-E004 reflection

**Did the explorer deliver?** YES — thorough adversarial search. Found inf λ_min ≈ -14.734 (determined to ±0.05). Tested structured anti-instanton starts, which were far more effective than random. Key discovery: D/C anti-correlation.

**β < 1/4 is ruled out.** The most negative eigenvalue is ~14.7, well above 2d = 8. The Bakry-Émery route gives at best β < 2/14.7 ≈ 0.136 empirically, or β < 1/8 = 0.125 if we prove |λ_min| ≤ 4d = 16 via decoherence.

**The decoherence lemma is THE remaining proof target.** If proved: ||C(Q)|| ≤ 2(d+1) → |λ_min| ≤ 4d → β < 1/8 (1.5× over SZZ). This is a clean, provable statement with strong numerical support (0/2000+ violations).

## Planning Exploration 005: Prove the Decoherence Lemma

### Options
A. Math Explorer to prove the decoherence lemma directly
B. Standard Explorer to do adversarial review of the full proof chain
C. Final synthesis

### Decision: A — Prove decoherence, then review + synthesize

With 3 explorations left, the best allocation is:
- E005: Math Explorer — focused proof of the decoherence lemma
- E006: Standard Explorer — adversarial review of entire proof chain (Hessian formula → D+C → decoherence → mass gap)
- E007: Final synthesis

The decoherence lemma: ||C(Q)||_op ≤ ||C_flat||_op = 2(d+1).

Key proof strategies to try:
1. **Tensor product norm bound**: C = Σ (spatial) ⊗ (color). At flat, color = -2I₃ for all terms → spatial part determines ||C||. Away from flat, color factors misalign → destructive interference.
2. **Matrix-valued Cauchy-Schwarz**: ||Σ A_i ⊗ B_i|| ≤ ||Σ A_i ⊗ A_i||^{1/2} · ||Σ B_i ⊗ B_i||^{1/2} or similar.
3. **Direct bounding**: Bound each plaquette pair's cross-term contribution using ||F|| ≤ 2, then sum.
4. **SO(3) averaging**: Average over gauge transformations and show the average equals the flat value.

### Post-E005 reflection

**Outcome:** The decoherence lemma is FALSE for d≥3. This is a critical negative result that invalidates the D+C proof approach.

**But positive results emerged:**
- Per-plaquette decoherence PROVED: ||C_□|| ≤ 3
- Full decoherence PROVED for d=2
- Color kernel SVD: exact singular values (2, 2, 2|β₀|)
- D/C anti-correlation is confirmed structural

**Key lesson from E004→E005 discrepancy:** E004 tested 2000+ configs for ||C|| ≤ 10 and found 0 violations. E005 found ||C|| = 11.68 by gradient ascent specifically targeting ||C||. The 48% gap shows that random sampling + specific structured starts are NOT sufficient — must always gradient-ascend on the exact quantity being bounded.

**Remaining budget: 2 explorations.** The D+C approach failed for d≥3. Options:

A. **Try per-plaquette bound on H directly** (not D/C separately). Each plaquette contributes |h_□| ≤ some bound to H. If this bound × (lattice aggregation) ≤ 4d, done.

B. **Prove |λ(H)| ≤ 4d using the Weitzenböck/Bochner structure**. The Hessian of the Wilson action has geometric meaning — it's related to the lattice curvature. There may be a natural decomposition H = Lap + Curv where both are bounded.

C. **Accept the gap and write final synthesis.** We have β < 1/8 rigorously for d=2 (decoherence proved). For d≥3, we have strong numerical evidence but no proof.

D. **Prove the D/C anti-correlation directly.** Show: if |D| ≥ 2(d-1) - δ, then ||C|| ≤ 2(d+1) - f(δ), with (2(d-1)-δ) + (2(d+1)-f(δ)) ≤ 4d.

### Decision: E006 = Final proof attempt (Math Explorer), E007 = Final synthesis

E006 will be a Math Explorer trying approach D (D/C anti-correlation) and approach A (per-plaquette H bound). These are the most promising given the structural insights.

Wait — actually I should save the last exploration for the final synthesis/report. So E006 is my LAST proof attempt. Let me make it count.

E006 priorities:
1. Attempt to prove D/C anti-correlation (most promising given E005's structural insights)
2. If that fails, try per-plaquette H bound
3. If all fail, characterize the obstruction precisely for the final report

E007 = Final synthesis and FINAL-REPORT.md
