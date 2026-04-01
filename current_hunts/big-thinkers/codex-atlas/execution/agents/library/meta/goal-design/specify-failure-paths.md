---
topic: Specify failure paths in goals
category: goal-design
date: 2026-03-27
source: "strategy-001 meta-004, strategy-004 meta-s4-001, strategy-004 meta-s4-002, yang-mills strategy-001 meta-exploration-006, riemann-hypothesis strategy-001 meta-exploration-006, classicality-budget strategy-002 meta-exploration-008, riemann-hypothesis strategy-002 meta-exploration-004, riemann-hypothesis s002-meta-exploration-006, riemann-hypothesis s003-meta-exploration-003, vasseur-pressure strategy-001 meta-exploration-004"
---

## Lesson

Always include an explicit failure path instruction in exploration goals: "If you find this doesn't work, explain the structural reason and propose what WOULD work." This turns negative results into positive leads instead of dead ends.

## Evidence

- **strategy-001 exploration 004** — Asked "if this fails, explain WHY NOT and what additional input is needed." The negative result (four structural obstacles) became the most valuable outcome, producing the "quantum cost function" insight and the Flory et al. penalty factor landscape.
- **strategy-004 exploration s4-001** — Including a failure path instruction produced an honest "partial success" assessment instead of inflated claims. Explorer correctly classified the prediction as "partially discriminating" rather than overselling.
- **strategy-004 exploration s4-002** — Failure path instruction surfaced the convention dependence (M_P vs M-bar_P) as a genuine systematic uncertainty that would otherwise have been glossed over.

## Related: Request Diagnostic Outputs

For computational explorations, also ask for diagnostic outputs that might reveal unexpected effects. The negative connected correlator (finite-volume sum rule) in the SU(2) lattice computation was an unexpected finding that only surfaced because the explorer reported diagnostic details rather than just final results.

- **yang-mills strategy-001 exploration 003** — The plaquette correlator's failure to yield glueball masses was expected, but the specific mechanism (signal-to-noise ~ exp(-m₀) at t=1) was informative and consistent with a large mass gap. Future goals should explicitly ask for such diagnostic outputs.

## Variant: Pessimistic Assessments as High-Value Outcomes

When the answer to "how close are we?" is "20-50+ years," the exploration is still valuable **if it precisely identifies WHY**. Ask for "honest assessment of proximity" — the negative result (far from solution) combined with structural reasons (four specific obstructions, no overlapping approaches) is more actionable than optimistic hand-waving.

- **yang-mills strategy-001 exploration 006** — The "honest assessment of proximity to proof" prompt produced an authentic 20-50+ year timeline with detailed evidence for pessimism AND cautious optimism. The structured negative assessment (every result is for wrong groups, wrong coupling, wrong dimension, or wrong limit) was the most strategically valuable output.

## Variant: Resolve Interpretation Ambiguity Before Computing Consequences

When a theoretical framework has an unresolved **interpretation** (e.g., "does this apply to subsystem A or the full system?"), **resolve the interpretation before computing its consequences.** An exploration that assumes one interpretation for ~2 explorations and then discovers the other interpretation is the intended one has wasted those turns.

- **thermal-time strategy-001 meta-exploration-003** — The local vs. global modular flow question (does TTH apply K_A for subsystem A, or K_AB for the full system?) was not explicitly resolved until exploration-003. Explorations 001 and 002 implicitly assumed the local interpretation (K_A) and computed its consequences. Exploration-003 discovered that the global interpretation (K_AB) is trivially equivalent to standard QM. The strategizer note: "The literature disambiguation question (local vs. global) should have been in exploration-002 or even exploration-001. We spent two explorations computing assuming the local interpretation without confirming it was Connes-Rovelli's intent."

**Pattern:** When writing a Phase 2 computation goal, include a section: "**Interpretation check:** Before computing, establish which of these interpretations applies: [option A] vs. [option B]. Cite the relevant passage from [key paper(s)] that resolves this. If both interpretations are viable, compute for both and compare."

**Cost of omitting:** One or more explorations computing consequences of the wrong interpretation. The cost is proportional to how long it takes to realize the error.

**When to apply:** Whenever the goal involves a theoretical framework with:
- A subsystem vs. global system ambiguity (very common in quantum information)
- A classical vs. quantum limit ambiguity
- A perturbative vs. non-perturbative ambiguity
- Any case where "which version of this theory are we testing?" is a real question

## Variant: Pre-Specify Known Domain Constraints to Avoid Impossible Targets

When a construction task is constrained by a fundamental physical or mathematical fact, **state the constraint explicitly in the goal** rather than discovering it mid-exploration. This prevents the explorer from pursuing directions that are theoretically impossible.

The canonical example is symmetry-class constraints in random matrix theory: real symmetric matrices can only achieve GOE statistics (β=1) at best — they can never produce GUE statistics (β=2) regardless of what arithmetic content they encode. If the goal is to find a matrix operator with GUE statistics, the goal should state upfront: "Note: real symmetric matrices are capped at GOE — to reach GUE you must consider complex-valued matrices or time-reversal symmetry breaking."

- **riemann-hypothesis strategy-001 exploration 006** — The strategizer noted in retrospect: "Real symmetric matrices can only reach GOE (β=1), never GUE (β=2). This is a fundamental constraint I should have mentioned in the goal." The exploration was not wasted (it confirmed the constraints empirically), but a cleaner goal would have pre-scoped the search to complex-valued constructions from the start.

This applies broadly: any time you know a class of solutions is impossible for a known structural reason, stating that constraint upfront focuses the exploration on the viable subspace.

**Extended (strategy-002 exploration-001):** Even within the complex-matrix space, there is a further constraint: phases of the form g(j)−g(k) (factorizable) are unitarily equivalent to real symmetric matrices and are also capped at β≤1. For GUE-targeting goals, the goal should additionally state: "Phase φ(j,k) must depend jointly on j and k — phases of the form φ(|j-k|) (Toeplitz/lag-only) or g(j)−g(k) (factorizable) do not break time-reversal symmetry and will not produce GUE statistics regardless of the arithmetic content." This rules out two more classes of construction failure before the explorer begins.

## Variant: "If the Premise Is Wrong, Explain Why" for Physical Implication Explorations

For explorations that apply a framework to a physical system and check what follows, always include:
"If the premise of this question is wrong, explain why." Sometimes the most valuable finding is
that the question itself was incorrectly posed.

- **classicality-budget strategy-001 exploration 006** — The goal asked "at what BH mass does the
  Hawking entropy first exceed 1 bit (the classicality onset mass)?" This implicitly assumed
  S_Hawking increases with BH mass (hotter/smaller BHs). The failure path instruction led the
  explorer to prove this was WRONG: T_H × r_s = const means S_Hawking is mass-independent and
  ALWAYS ≈ 0.003 bits. The "no classicality onset mass" result was the correct and more interesting
  finding — the premise was false. Without the failure path instruction, the exploration might
  have searched unsuccessfully for an onset mass instead of identifying and proving the
  mass-independence.

## Variant: Rate Each Assumption's Weakness

For derivation explorations, require an "Honest Assessment" section where the explorer rates the weakness of **each assumption** on a severity scale (e.g., CRITICAL / MODERATE / LOW). This is different from reporting whether the final result works — it forces the explorer to examine the scaffolding, not just the conclusion.

- **compton-unruh strategy-001 exploration-004** — The "Honest Assessment" section with per-assumption weakness ratings was the most valuable part of the report. It caught the CRITICAL weakness: the ratio ansatz m_i = m·T_U/T_dS gives exact MOND but is "motivated by the desired result, not derived from the physics." Without this section, the algebraically elegant result could have been reported as a physical derivation rather than an ansatz. Prompt language: "Include an 'Honest Assessment' section that rates the weakness of each assumption (CRITICAL / MODERATE / LOW) and clearly states what would be required to make each step rigorous."

## Variant: Frame "No-Go Argument" as Explicit Alternative Success Criterion

For experimental prediction goals, explicitly state that "finding the budget is VIOLATED (R_max < 0) is also a successful result." Without this framing, explorers feel pressure to find a positive experimental connection; with it, they can honestly report regime violations as the stronger result.

- **classicality-budget strategy-002 exploration 003** — The goal included "or a no-go argument" as an alternative success criterion. This prevented the explorer from inventing weak experimental connections to satisfy the goal. The explorer instead found that the ion trap at n̄ = 0.001 gives R_max = −0.315 (budget forbids copies) — a stronger result than "in principle testable." The alternative success criterion gave the explorer permission to report the negative constraint violation as positive knowledge.

This applies broadly: whenever a goal asks "is X testable?" include "if X predicts NO testability (a no-go regime), that counts as the answer." Negative regime findings are often more informative than positive borderline connections.

## Variant: Ask Whether the Formalism Can Yield the Modification in Principle

Before commissioning a derivation via a specific formalism (FDT, AdS/CFT, path integral, etc.), ask
the failure path question at the formalism level: **"Can this formalism in principle yield the desired
modification? If not, why not, and what formalism would?"**

This prevents investing a full exploration in an approach guaranteed-negative from basic principles.
The standard FDT is an example: the KMS condition (satisfied for any temperature in thermal
equilibrium) guarantees χ'' is T-independent — so any equilibrium FDT calculation cannot yield an
inertia modification by construction. Knowing this upfront would flag the exploration as needing a
non-equilibrium formulation from the start.

- **compton-unruh strategy-001 exploration-006** — A full FDT analysis was run before it became clear
  that the KMS condition guarantees χ''_dS = χ''_flat at equilibrium. The negative result was
  valuable (confirmed and computed, not just argued), but the lesson: for future derivation
  explorations, the goal should include "first check whether the formalism can in principle produce
  this class of effect, and if not, identify what modification (non-equilibrium, etc.) would be
  needed." This is a pre-screening step that takes one paragraph but can redirect the exploration to
  a more productive formulation.

## Variant: Give Explicit Skip Permission for Ambiguous Sub-Tasks

When a goal includes an open-ended sub-task that involves a formula or derivation with known normalization ambiguity (or any step where "it depends on the convention" is a real possibility), **include an explicit skip instruction**: "If the normalization of [formula X] is ambiguous, skip this sub-task and note which formula you would need to complete it." Without this permission, explorers silently drop the sub-task rather than reporting it — producing an incomplete report with no explanation of the gap.

Two acceptable forms:
1. **(a) Resolve by providing:** Give the exact formula or normalization convention in the goal, eliminating the ambiguity.
2. **(b) Resolve by scoping:** Explicitly say "skip if [condition], and state what you'd need."

Both are better than leaving the sub-task open-ended, which produces silent omission.

- **riemann-hypothesis strategy-002 exploration-004** — Part 4 of the goal (K(τ) → Δ₃ consistency check) was silently dropped due to normalization ambiguities in the K(τ) → Σ²(L) conversion. The goal should have either provided the exact integral relationship (option a) or said "skip if the K(τ) → Σ² normalization is unclear; note what formula you'd need" (option b). Instead, the explorer did neither — the check was not mentioned in the final report at all, leaving a gap.

Apply when: a sub-task requires a formula or convention that the explorer might not know; or when a goal has 4+ parts and some parts are lower-priority (give skip permission for those). Especially important for normalization-sensitive statistics (K(τ), Σ², Δ₃, R₂) where multiple formulas exist with subtle differences.

## Variant: Explicitly Request a Structural Explanation When Construction May Fail

When designing a goal that tests a construction (matrix, operator, physical model) that might fail, add the instruction: **"If the construction fails, provide a structural explanation — not just 'it doesn't work.' Identify the algebraic, topological, or physical reason that makes this class of construction impossible."** This elicits algebraic proofs and impossibility arguments rather than just negative numerical results, which are vastly more valuable.

- **riemann-hypothesis strategy-002 exploration-006** — The goal asked to test Dirichlet character matrix constructions. The explorer went beyond the numerical failure and proved algebraically that BOTH construction routes (multiplicative and factorizable) collapse to real symmetric matrices — making GUE structurally inaccessible. This proof was not required by the goal but was noted as "exactly the kind of insight to highlight." Had the goal explicitly requested a structural explanation on failure, it would have been produced more reliably. Framing: "If the construction fails, determine whether the failure is empirical (works at different parameters) or structural (algebraically impossible). If structural, provide the proof."

**Key distinction:**
- Empirical failure: "β = 0.28 instead of 2.0" — suggests trying different parameters
- Structural failure: "Both construction routes provably collapse to real matrices via Re(χ(j)χ(k)) = cos(g_j+g_k)" — closes the entire construction class

**Combined with "Pre-Specify Known Domain Constraints" variant:** If you know some subclasses of a construction are impossible, state that upfront. For the remaining untested subclasses, ask for structural explanation on failure. Together, these frame the exploration to produce both targeted tests AND mathematical closure.

**When to apply:** Any goal testing a parametric family of constructions (matrix phases, operator ansatze, effective field theories, physical models) where failure is possible. Especially valuable when the construction has algebraic structure that might produce a general impossibility result.

## Variant: Include Brute-Force Fallback Alongside Elegant Indirect Methods

When a goal's primary computation method is an indirect/analytical chain (e.g., R₂ → Σ₂ → Δ₃ integral chain), **always include a direct/brute-force fallback method in the goal.** Elegant chains can fail quantitatively due to noise amplification, truncation, or intermediate-step instability — while the brute-force method (e.g., direct sliding-window Δ₃ computation) often succeeds trivially.

- **riemann-hypothesis strategy-003 exploration-003** — The goal provided two methods: Method A (R₂ → Σ₂ → Δ₃ integral chain) and Method B (direct sliding-window Δ₃). Method A overestimated by 43% due to R₂ noise amplification through double integration. Method B gave the correct 0.1545 trivially. Having both methods in the goal meant the explorer had a fallback and produced reliable results despite the primary method's failure.

**Template:** "Compute X by [elegant method]. As a cross-check, also compute X by [direct/brute-force method]. If the two disagree, trust the direct method and diagnose why the indirect chain fails."

**When to apply:** Any exploration where the primary computation involves chaining multiple transformations (Fourier transforms, double integrals, iterative inversions). The chain's error propagation may not be obvious in advance; the brute-force backup costs little but saves the exploration.

## Variant: State Quantitative Falsification Criterion for Hypothesis-Testing Computations

When designing a computation to test a hypothesis, **state the falsification criterion explicitly and quantitatively in the goal**: "If the ratio is constant with k, the hypothesis is falsified." This makes the explorer's job unambiguous even when the result is negative. Combined with a multi-dimensional sweep (IC x Re x k x q), a clean negative result becomes decisive.

- **vasseur-pressure strategy-001 exploration-004** — The goal stated that if CZ tightness ratio for P_k^{21} is k-independent, the hypothesis is falsified. The explorer ran a comprehensive grid (3 ICs x 3 Re x 8 k-levels x 4 q-values), found convergence to a constant by k~3-4, and cleanly declared falsification. Having the criterion upfront made the negative result unambiguous and saved the mission from pursuing a dead-end.

**Template:** "Measure X as a function of Y. If X converges to a constant as Y increases, the hypothesis that X improves with Y is falsified. Include the convergence rate."

**Extension:** Also seed "what does this NOT rule out" into the goal. In E004, the explorer independently identified 4 alternative paths not eliminated by the negative result. Including these as prompts in the goal would have been helpful: "If the hypothesis is falsified, identify which alternative approaches remain viable."

## When to apply

Every technical investigation or verification exploration. Especially important for construction tasks where the hypothesis might be wrong, derivation explorations where assumption-by-assumption honesty is needed, and prediction extraction where the prediction might not exist. For computational explorations, include "report any unexpected or diagnostic findings." For proximity-to-solution assessments, ask for honest timelines with structural reasons. For construction explorations with known symmetry or structural constraints, state those constraints explicitly so the explorer targets the viable subspace. For derivation explorations, add a pre-screening step: "Can this formalism in principle produce the desired effect?" Less relevant for pure surveys where there's no hypothesis to fail.
