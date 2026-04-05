---
topic: Leave room for explorers to form synthesis insights not specified in the goal
category: goal-design
date: 2026-03-29
source: "amplituhedron strategy-001 meta-exploration-003, amplituhedron strategy-001 meta-exploration-004, riemann-hypothesis s002-meta-exploration-005, thermal-time strategy-001 meta-exploration-001, thermal-time strategy-001 meta-exploration-002, stochastic-electrodynamics strategy-003 meta-exploration-s003-001, yang-mills-conjecture strategy-002 meta-exploration-005"
---

## Lesson

Don't over-specify the conclusions you want explorers to reach. Goals should specify WHAT to investigate and WHAT FORMAT to produce, but leave the synthesis conclusions open. Explorers can identify structural patterns the strategizer didn't anticipate — these are often the most valuable outputs.

Over-specifying goal conclusions (e.g., "show that X has a two-tier structure") prevents explorers from discovering the two-tier structure themselves from evidence, which is more credible and may differ from what you expected.

## Evidence

- **amplituhedron strategy-001 exploration 003** — The goal specified an "extension map" of where positive geometry extends beyond N=4 SYM, with a structured output format (table + sections). The goal did NOT specify what structural conclusion to draw. The explorer independently synthesized a **two-tier insight** (positive geometry works broadly at tree level for any color-ordered theory, but narrowly at all-loop level only for N=4 SYM + ABJM) — not in the goal. This insight was the most valuable strategic output of the exploration.

- **amplituhedron strategy-001 exploration 004** — The goal asked to assess how locality and unitarity emerge from the amplituhedron and what physical consequences follow. The most valuable output was the explorer's **synthesis separating three genuine physical contributions from the reformulation claims**: (1) UV finiteness as selection principle, (2) EFT-hedron real-world bounds, (3) hidden zeros inter-theory structure. The goal did not specify these three categories — the explorer developed the taxonomy. Without this synthesis, the assessment would have been technically accurate but strategically unusable. Confirms: the synthesis judgment is often the output that drives decisions, and over-specifying it prevents genuine discovery.

- **riemann-hypothesis s002-meta-exploration-005** — The goal for exploration-005 asked the explorer to sweep Gauss sum phases across multiple primes and test whether β → 2 as p → ∞. The explorer computed the β values, refuted the hypothesis, and then — without being asked — identified the underlying organizing principle: the ratio N²/p ≈ 250–310 predicts the location of maximum β, with a physical interpretation (effective phase cycles). This pattern came entirely from the explorer. It turned a negative result ("β does not grow") into a mechanistic understanding ("β is maximized at a specific ratio of matrix size to prime"). The goal had not specified "find an explanatory pattern" — only "test the hypothesis." The synthesis was the most valuable output.

- **thermal-time strategy-001 exploration 001** — Goal asked for a modular Hamiltonian catalog with TTH formalization. The explorer independently identified "underexploited constraints" — a ranked list of constraint classes where TTH is under-tested — as the key strategic output for directing Phase 2. This identification was not in the goal. It was the most actionable output of the exploration.

- **thermal-time strategy-001 exploration 002** — Goal asked for normalization resolution and ΔK_A computation. The explorer additionally produced a **no-go theorem** not asked for: TTH (normalized) = QM if and only if K_A = βH_A + const·I, i.e., exactly when ρ_A is a Gibbs state. This result answered "when does TTH make new predictions?" — a question the goal didn't ask. The no-go theorem was the most theoretically significant output.

## Variant: "What Would Be a Breakthrough?" Primes Explorer for High-Value Output

Including the question "what would be a breakthrough result here?" in the goal helps the explorer prioritize its effort toward the most significant findings rather than completing tasks in arbitrary order. This is distinct from specifying conclusions (which should NOT be done); it's about directing attention to what matters strategically.

- **thermal-time strategy-001 meta-exploration-002** — Including "what would be a breakthrough" in goal helped the explorer focus on the most important findings (normalization resolution and ΔK_A no-go theorem) rather than producing a comprehensive but undifferentiated report.

**Design template:** Add to GOAL.md: "Before concluding, identify: what would constitute a genuine breakthrough result for this task? Prioritize your synthesis around that finding."

## Variant: Ask "Explain WHY This Agrees" to Elicit Novel Bonus Derivations

**Explicitly ask explorers to explain WHY a result agrees with a known prior result, not just to verify THAT it agrees.** The explanation often yields more value than the check itself — it forces the explorer to derive the underlying mechanism, which can produce novel structural insights.

- **stochastic-electrodynamics strategy-003 exploration-001** — The goal asked the explorer to check consistency of the Santos O(ħ²) framework with Pesquera-Claverie (1982). The explorer not only confirmed agreement but independently derived a symmetry argument: the O(ħ²) Moyal correction term is odd in x, so its contribution to ⟨x²⟩ integrates to zero at O(β) — explaining WHY P&C found SED and QM agree at first order in β. This symmetry argument was not in the goal, not in P&C, and not in Santos. It emerged entirely from asking "why does this agree?"

**Design template:** When you expect a result to be consistent with prior work, add to the goal: "Check consistency with [prior result]. **Explain WHY they agree or disagree at the level of mechanism — not just the fact of agreement.**" This triggers the explorer to work through the algebra and often produces a novel structural insight the strategizer didn't anticipate.

**Contrast with standard consistency checks:** A standard consistency check ("verify A agrees with B") produces a one-line confirmation. A mechanism explanation ("explain WHY A agrees with B") produces a derivation — and derivations can be wrong, surprising, or generalizable in new ways.

## When to Apply

- Survey explorations where the structure is not pre-known
- Any "map the landscape" type task
- Synthesis tasks where you want genuine discovery, not confirmation
- **Theory/derivation explorations where a result should be consistent with known prior work** — especially useful here because the WHY question produces novel structural derivations

## Variant: Don't Prescribe Proof Technique for Tight Bounds

**For proofs where the bound is tight (infimum = 0), do not prescribe a specific bounding technique.** The tightness means most standard techniques (Cauchy-Schwarz, AM-GM, spectral bounds applied directly) will be too loose. Give the explorer freedom to discover structural properties that simplify the problem.

- **yang-mills-conjecture strategy-002 exploration-005** — The GOAL prescribed a polarization approach for proving sum_S ≥ 0. The polarization bound failed immediately (37% of trials negative, correction/baseline > 10). A C-S + spectral bound was even worse (65% negative). The explorer ignored the prescribed approach, discovered that M9 is affine in D (a structural property nobody anticipated), and used this to prove the bound via an elementary contraction argument. The GOAL's approach hierarchy was counterproductive — it cost time testing a doomed technique before the explorer pivoted.

**Design principle:** For tight bounds, specify WHAT to prove and provide structural context (master identity, special-case proofs, numerical evidence), but let the explorer find HOW. Pre-screening the approach numerically before prescribing it would have caught the failure.

## When NOT to Apply

- If you need the explorer to test a specific structural hypothesis — then specify it
- Adversarial/stress-test explorations where you DO want the explorer to probe specific points

## Design Principle

Specify: domain, output format, concrete success criteria, time window, relevant references.
Leave open: what the key patterns are, what structural conclusion to draw, whether a framework succeeds or fails (let evidence drive that).
