---
topic: One task per exploration
category: goal-design
date: 2026-03-30
source: "strategy-001 meta-006, strategy-001 meta-007, strategy-001 meta-009, strategy-003 meta-s3-001, riemann-hypothesis meta-exploration-004, riemann-hypothesis s002-meta-exploration-005, riemann-hypothesis s003-meta-exploration-003, vasseur-pressure strategy-001 meta-exploration-007"
---

## Lesson

Every exploration should have exactly one primary task. Multi-task explorations either time out or produce shallow results across all tasks. "One task" means one cognitive unit — not one sentence that contains five sub-tasks.

## Evidence

- **strategy-001 exploration 006** — Goal combined "research new approach + rewrite existing theory + address 4+ flaws + new predictions." Explorer got stuck thinking and never produced output. Timed out.
- **strategy-001 exploration 007** — Same topic as 006, narrowed to ONE repair. Succeeded in under 10 minutes. This contrast is the clearest evidence.
- **strategy-001 exploration 009** — Final synthesis confirmed: the most effective explorations (001, 002, 003, 005, 007) were all single-task. The only failure (006) was multi-task.
- **strategy-003 exploration s3-001** — Goal said "state a conjecture precisely" but actually required: formulating 3 math versions, enumerating 6-8 testable implications, identifying 3-4 falsifiers, surveying literature, and assessing novelty. Explorer spent 25+ minutes doing web searches without writing anything beyond a skeleton.

## When to apply

Always. Before dispatching any exploration, count the distinct cognitive tasks. If there are more than one, split into separate explorations. A survey + deep dive + synthesis counts as one task (the survey pattern). "Research X and also rewrite Y" is two tasks.

## Corollary: Split Conceptual Mapping + Computation Across Explorer Types

When an exploration involves both (a) conceptual framework mapping (translating concepts between
two theories) and (b) numerical or algebraic computation (verifying the framework works), consider
splitting into two explorations using appropriate explorer types:
- A **standard explorer** for the conceptual mapping and derivation
- A **math explorer** for computation verification

The standard explorer is stronger at framework translation and literature synthesis; the math
explorer is stronger at tensor contractions, algebraic verification, and code execution.

- **classicality-budget strategy-001 exploration 007** — Combined holographic QD mapping with
  HaPPY code saturation computation. The report was 647 lines (above the 400-600 target) and the
  explorer acknowledged it "couldn't fully verify the HaPPY code saturation claim — would have
  benefited from a Math Explorer to run the tensor contraction computation." A split (standard
  explorer for HQEC mapping; math explorer for HaPPY verification) would have been cleaner.

## Corollary: Depth Beats Breadth for Generating Insight

A single deeply investigated approach produces more understanding than three approaches surveyed at the same total time. Focus an exploration on ONE question and follow it wherever it leads.

- **riemann-hypothesis meta-exploration-004** — Exploration-003 (three parallel approaches to the berry-keating operator testing problem) produced useful data but limited insight. Exploration-004 (one approach: trace formula reconstruction) discovered the Gibbs phenomenon, proved individual zero reconstruction is fundamentally impossible, and produced clean theoretical insight — results that led to one of the most important strategic clarifications in the mission. The lesson: if you must choose between breadth and depth, choose depth.

## Corollary: Two Genuinely Parallel Computations With Shared Setup Can Combine

Exception to one-task-per-exploration: two computationally independent investigations can share one exploration if they share setup (data, code, matrices) and do not depend on each other's results. The cognitive task remains unified (evaluate this physical system).

- **riemann-hypothesis s002-meta-exploration-005** — Exploration-005 had Part A (recompute pair correlation and Δ₃ for the C1 matrix using corrected formulas) and Part B (sweep Gauss sum phases across multiple primes). Both used the same matrix construction; neither depended on the other's result. The exploration delivered both results cleanly. Contrast: combining "build new theory + attack it" would be a cognitive multi-task and should be split.
- **vasseur-pressure strategy-001 exploration-007** — Task A (Beltrami deficit vs k) and Task B (Hessian/remainder pressure decomposition) share DNS infrastructure and are conceptually linked (each informs interpretation of the other). The explorer handled both cleanly without fragmentation.

**The dividing line:** Can both tasks run simultaneously without the output of one informing the other? If yes, combine. If either task depends on the other's result, split into sequential explorations.

## Corollary: Separate Literature/Convention Questions from Computation

When an exploration involves both (a) a convention or normalization question (requiring careful paper-reading to resolve) and (b) numerical computation that depends on that convention, **put the convention question in its own exploration first.** Paper-reading competes with computation time: an explorer that spends ~1/3 of its context resolving a normalization question has proportionally less context for the computation, and vice versa.

- **thermal-time strategy-001 meta-exploration-001** — Exploration-001 combined a modular Hamiltonian catalog (paper-reading + formalization) with a Fock-space computation. The normalization question (τ=t vs. τ=β·t) arose mid-exploration and was correctly flagged as open rather than resolved — which required a dedicated follow-up exploration (E002). The strategizer note: "When the key question is normalization (a convention question), put it in its own exploration — it requires careful paper-reading that competes with computation time."
- **thermal-time strategy-001 meta-exploration-002** — Confirmed: the normalization literature survey (reading Connes-Rovelli 1994, Martinetti-Rovelli 2003, Haggard-Rovelli 2013) took approximately 1/3 of E002's context. This was manageable because E002's computation was also well-defined. If the computation had been more complex, the paper-reading would have crowded it out.

**The dividing line:** Is the convention/normalization question resolvable by finding the right equation in a specific paper? If yes, it's a literature task — separate it. If it can be resolved from dimensional analysis or known physics in a paragraph, leave it in.

## Corollary: Mark Optional Tasks as Explicitly Skippable

When a goal contains both essential and exploratory tasks, **explicitly mark which tasks are optional and can be skipped under time pressure.** Without this, the explorer must guess priorities. With it, the explorer can correctly focus on the critical path and skip secondary tasks when time-pressured — which is usually the right call.

- **riemann-hypothesis strategy-003 exploration-003** — Goal combined 5 tasks: (0) setup, (1) empirical R₂, (2) K(τ) from R₂, (3) prime orbit K(τ), (4) Δ₃ from K(τ), (5) Hardy-Littlewood enhancement. The explorer correctly skipped Tasks 3 and 5 (the most scientifically interesting but non-essential tasks) to focus on the critical Δ₃ verification (Task 4). This was the right prioritization — but should have been an explicit instruction in the goal, not an implicit decision by the explorer. The meta-note: "prime orbit K(τ) deserves its own dedicated exploration — the goal was too broad."

**Template:** In multi-part goals, add priority labels:
> **Required:** Tasks 0, 1, 2, 4 (core verification)
> **Optional (skip if time-pressured):** Tasks 3, 5 (exploratory; will be dedicated explorations later)

**Relationship to one-task-per-exploration:** This corollary is the pragmatic fallback for when the strategizer nevertheless includes multiple tasks. The ideal is one task; the next best is explicit skip permissions.

## Corollary: Trust a Well-Scoped Comprehensive Survey

If a single comprehensive survey exploration is designed to cover all relevant sub-categories (e.g.,
"catalog all constraints: structural, recovery, and precision bounds"), it typically DOES cover them
all — you don't need a separate follow-up exploration for each sub-category. Over-splitting a
well-scoped catalog into multiple narrow explorations wastes turns.

- **stochastic-electrodynamics strategy-001 meta-exploration-001** — One comprehensive numerical
  survey exploration (SED HO ground state: ZPF PSD, variance, Gaussianity, UV structure, parameter
  sensitivity) was sufficient. No separate follow-up was needed to fill specific sub-categories.
- **thermal-time strategy-001 meta-exploration-001** — One comprehensive constraint catalog exploration (TTH modular Hamiltonian catalog: 4 systems, Rindler through CFT interval) was sufficient; no separate exploration was needed for precision bounds or individual system classes. The well-scoped goal with explicit categories (A/B/C/D structure) meant the explorer covered all subcategories in one pass.
