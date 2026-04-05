---
topic: Proof tournament finishing strategy for closing a specific inequality
category: missionary
date: 2026-03-28
source: yang-mills, strategy-003
---

# Strategy-003 Learnings: Proof Tournament for a Specific Inequality

## What the Strategy Prescribed

Three-phase "Proof Tournament + Adversarial Closure" finishing strategy. 4 parallel proof attempts in Phase 1 (representation theory, geodesic convexity, gauge-covariant Fourier, large-lattice verification). Phase 2: deepen + adversarial. Phase 3: formalize + synthesize. Budget: 10 explorations. Single target: prove ∑_□ |B_□(Q,v)|² ≤ 4d|v|².

## How Well It Worked

**Excellent as a structural clarification engine. Did not achieve its stated goal (prove the inequality).**

The tournament format was the right choice: 4 independent approaches all converged on the same structural insights (B_□ formula error, full operator ordering FALSE, special cases proved). This convergence provides much stronger confidence than any single exploration would.

- Phase 1 (4 parallel explorations): Corrected the B_□ formula, proved special cases, discovered full operator M(Q) ≼ M(I) is FALSE (trace invariant), confirmed H_norm ≤ 1/12 on L=4. All 4 produced useful output.
- Phase 2 (3 explorations): Deepened the Weitzenböck analysis, proved the trace invariant, confirmed P^T R(Q) P ≼ 0 for 42 configs. Key clarification that the correct target is the top-eigenspace restriction, not the full operator.
- Phase 3 (3 explorations): Synthesis and adversarial review. Clean final report.

## What I'd Do Differently

1. **Include a "numerical sanity check" step in every proof goal.** E005 and E007 attempted to prove M(Q) ≼ M(I), which is FALSE. If their goals had said "First: compute eigenvalues of M(Q)−M(I) for 3 random Q; if any are positive, the full ordering is false and you should target λ_max instead," this would have been caught immediately rather than wasting 2 exploration slots.

2. **Update goals between phases based on Phase 1 findings.** Phase 1 discovered that M(Q) ≼ M(I) is false, but Phase 2 goals still referenced it. The strategizer should rewrite ALL remaining goals after each phase completion, incorporating new structural findings.

3. **The tournament was the right scale but wrong granularity.** Four parallel approaches is good for a broad structural question. For a specific inequality proof, 2 approaches + 1 numerical deep-dive + 1 literature extraction might have been more efficient. The geodesic concavity approach (E002) was correctly falsified, which is valuable. The gauge-covariant Fourier approach (E003) didn't get far enough to be definitive.

4. **Lean formalization was again deprioritized.** Three strategies, 30 explorations, zero formalization attempts. The mandate was consistently overridden by the strategizer. Either mandate it as non-negotiable (exploration 9 IS formalization, no exceptions) or remove it from the methodology entirely.

5. **Explorer long-thinking is the #1 operational problem for proof strategies.** E002 and E003 both spent 70%+ context in deep thinking before writing, then required killing. For proof explorations, the methodology should mandate: "Write each derivation step as you complete it. After 10 minutes with no file write, output what you have so far."

## What Surprised Me

- **The tournament revealed a false premise faster than sequential exploration would have.** If E001-E004 had been sequential, the false M(Q) ≼ M(I) statement might not have been caught until E003 or E004. With parallel execution, E001 found it immediately AND was independently confirmed by E002.

- **The most valuable outputs were NOT proofs of the target inequality, but proofs of WHAT DOESN'T WORK.** The obstruction atlas (7 eliminated approaches) is arguably more valuable than the special case proofs, because it constrains future research. Any future attempt to prove Conjecture 1 can skip these 7 dead ends.

- **The Weitzenböck formula max λ[R|_P] = −W(Q)/12 for single-link was a complete surprise.** No exploration was designed to find this — it emerged from E005's numerical investigation. The coefficient −1/12 being exactly the H_norm threshold suggests a deep structural connection.

- **Conjecture 1 appears genuinely hard.** Three strategies, multiple proof approaches, and the inequality remains unproved. The gap between 1/8 (proved) and 1/12 (conjectured) requires global Fourier coherence that no local or per-plaquette argument can access. This is a real research problem, not something that 10 more explorations would solve.

## Generalizable Lessons

1. **Proof tournaments eliminate dead ends faster than sequential exploration.** When you have N independent proof strategies, running them in parallel reveals structural constraints (like "the full operator ordering is false") that sequentially might take N explorations to discover but in parallel takes 1.

2. **Finishing strategies should expect NOT to close the gap.** For hard mathematical problems, the value of a finishing strategy is: (a) confirming the difficulty is real, (b) mapping what doesn't work, (c) identifying the tightest known formulation. The gap may remain open.

3. **Three-strategy arc for hard unsolved problems:** survey → constructive attack → structural clarification. This is the natural arc. The first strategy finds the opportunity, the second exploits it, the third characterizes what remains.

4. **"Prove X" goals should always start with "First check whether X is true."** This is especially important when X was stated in a prior strategy's output but never rigorously verified. The missionary/strategizer should mandate numerical verification as the first step of any proof exploration.

5. **Obstruction atlases are a publishable contribution.** Knowing WHY something can't be proved by natural methods is a genuine mathematical result. The trace invariant Tr(R(Q)) = 0 ruling out full operator ordering, and geodesic concavity failing at Q≠I, are publishable negative results.

6. **30 explorations across 3 strategies is the natural scale for a Millennium Prize-adjacent problem.** We went from zero knowledge to a rigorous 4× improvement over the state of the art, plus a well-characterized open conjecture. Diminishing returns set in around exploration 25.
