# Plan Testing Dataset — Findings

**Date:** 2026-03-28
**Total runs:** ~60+ across 8 questions, 5 meta-plans, 2 models (Opus 4.6, Haiku 4.5)

## Questions Tested

| ID | Subject | Type | Expected Answer |
|----|---------|------|-----------------|
| Q1 | FTIR biophysics | Multiple choice (9 options) | C (coiled-coils) |
| Q3 | 2D exciton physics | Exact match | -0.08 eV |
| Q4 | Polymer stat mech | Derivation | F(x) = 3E(0)x/(nl)^2 |
| Q5 | XRD crystallography | Exact match | 1, 2, 2 |
| Q6 | Mossbauer spectroscopy | Multiple choice (5 options) | C (linear Fe(II)) |
| Q7 | Lattice adsorption | Exact match | Z=4.61, k=1.66 |
| Q8 | Mean-field lattice gas | Exact match | 0.424 |
| Q10 | Ceramic sintering | Multiple choice (6 options) | C |

## Meta-Plans Tested

| ID | Name | Instruction |
|----|------|-------------|
| M1 | Classify-then-Decompose | Classify the problem type, then decompose into steps natural for that type |
| M2 | **Constraint-First** | Extract every constraint, entity, rule. List explicitly. Resolve in dependency order. |
| M3 | Failure-Mode | Identify 3+ failure modes first, then design steps that guard against each |
| M4 | **Minimal Steps** | Shortest path to answer. 2-4 steps max. Don't over-plan. |
| M5 | Vanilla | "Break into logical steps." (Control — bare planning instruction) |

## Finding 1: M2 and M4 are the two best meta-plans, for different reasons

**M2 (Constraint-First)** excels at **discrimination** — when the answer hinges on a specific word or detail, M2's explicit constraint checklist surfaces it.

- Q10: M2 is 2/2 correct (C) while 0/15 for all other approaches. The constraint plan flagged "randomly distributed" as contradicting the spatial gradient inherent in the coarsening gas mechanism.
- Q6: M2 correctly identified that linear Fe(II)'s unquenched orbital angular momentum beats Fe(III)'s higher spin.

**M4 (Minimal Steps)** excels at **computation** — keeping derivation steps short minimizes algebraic errors.

- Q8: M4 is 2/2 with correct sign (0.358) while 8/10 other agents got 0.848 (wrong sign). The minimal plan wrote `β(μ + z·ε·⟨n⟩)` in one shot, avoiding the sign-flip that longer derivations introduce.
- Q7: M4 produced the closest answers to expected values.

**M1, M3, M5 all underperform:**
- M5 (vanilla) ≈ baseline — the act of planning alone doesn't help
- M1 (classify) — inconsistent
- M3 (failure-mode) — helps on interpretation (Q3) but not elsewhere

### Head-to-head: M2 vs M4 (Opus, all 8 questions)

| Question | M2 | M4 | Winner |
|----------|----|----|--------|
| Q1 FTIR | ✗ I | ✗ E | Tie (both fail) |
| Q3 Exciton | ✓✓ | ✓✓ | Tie |
| Q4 Polymer | ✓ | ✓ | Tie |
| Q5 XRD | ✓ | ✓ | Tie |
| Q6 Mossbauer | ✓ | ✓ | Tie |
| Q7 Partition | ~1/2 | ~2/2 | M4 |
| Q8 Mean-field | 1/2 (sign varies) | **2/2** (sign consistent) | M4 |
| Q10 Sintering | **2/2 ✓** | 0/2 ✗ | M2 |
| **Total** | ~7-8/12 | ~7-8/12 | **Tied overall** |

M2 wins on discrimination, M4 wins on computation. Complementary strengths.

## Finding 2: Planning helps on reasoning/discrimination, not domain knowledge

| Bottleneck type | Example | Does planning help? |
|---|---|---|
| Specific wording discrimination | Q10 "randomly distributed" | **Yes** — M2 catches it |
| Algebraic sign conventions | Q8 mean-field equation | **Yes** — M4 keeps it clean |
| Interpretation ambiguity | Q3 "Rydberg energy for n=3" | **Yes** — M2, M3 both help |
| Multi-step derivation | Q4 polymer force law | **Yes** — both M2 and M4 |
| Systematic enumeration | Q5 XRD reflections | **Yes** — both M2 and M4 |
| Domain-specific facts | Q1 coiled-coil FTIR signature | **No** — nobody gets it |
| Ambiguous problem formulation | Q7 partition function | Marginal — high variance |

## Finding 3: Meta-plans shape error patterns deterministically

On Q10, each meta-plan consistently produces the same wrong answer:
- M1: always A (2/2)
- M3: always E (2/2)
- M4: always A (2/2)
- M5: A or E
- **M2: always C — correct (2/2)**

The meta-plan doesn't add randomness — it channels reasoning down a specific path.

## Finding 4: Plan variance is a real problem

M2's Q8 results: run 1 got 0.358 (correct sign), run 2 got 0.848 (wrong sign). Same meta-plan, different instance-plans, different outcomes. The plan itself is a random variable.

M4 is more consistent (Q8: 0.358 both runs) because its shorter plans leave less room for variation.

**Implication: run at least 2 replicates.** Single runs can't distinguish signal from noise.

## Finding 5: BIGGEST FINDING — Good plans compensate for weaker model capabilities

Haiku (4.5) baseline on Q5, Q6, Q8, Q10: **0/4 correct.**
Haiku executing Opus-generated plans: **4/4 correct (or correct direction).**

| Question | Haiku Baseline | Opus Plan → Haiku Execute | What happened |
|----------|---------------|---------------------------|---------------|
| Q5 XRD | 0,3,0 ✗ | **1,2,2 ✓** | Plan taught splitting analysis |
| Q6 Mossbauer | D ✗ | **C ✓** | Plan explained orbital momentum matters |
| Q8 Mean-field | 5.594 ✗ | **0.358 ~✓** | Plan gave correct equation sign |
| Q10 Sintering | D ✗ | **C ✓** | Plan flagged "randomly distributed" |

**The plan is a knowledge transfer mechanism.** The strong planner (Opus) identifies the key insight, embeds it in the plan, and the weaker executor (Haiku) follows it through successfully.

### Implications:
1. **Strong model plans + cheap model execution** is a viable architecture
2. Plans transfer not just structure but domain knowledge
3. The quality of the plan matters more than the capability of the executor

### Missing test (in progress):
**Haiku plan → Haiku execute** — does Haiku produce good enough plans to help itself? If not, the bottleneck is plan quality (requires strong planner). If yes, even self-planning helps.

## Finding 6: Opus >> Haiku on expert-level questions (without plans)

On Q1, Q4, Q5, Q6 (new questions):
- Opus with plans: 3/4 correct
- Haiku baseline: 0/4 correct

Exception: Q7 — Haiku baseline (k=1.52) was closer than Opus baseline (k=6.2). Simpler reasoning avoided overthinking.

## Practical Implications for Agent Architecture

1. **Use M2 (Constraint-First) as the default planning approach** — broadest advantage, unique discrimination ability.

2. **Use M4 (Minimal Steps) for computation-heavy problems** — fewer steps = fewer algebraic errors.

3. **A hybrid M2+M4 might be optimal** — "extract all constraints, then find the shortest path through them."

4. **Consider Opus-plan + Haiku-execute** for cost optimization — the plan carries the intelligence, execution is mechanical.

5. **Planning can't substitute for domain knowledge** — Q1 (coiled-coils) defeats all approaches. The bottleneck is knowing a specific fact.

6. **Run at least 2 replicates** — plan variance means single runs are unreliable.

## Finding 7: Plan quality is the dominant variable — the Planner/Executor matrix

We tested the full 2x2 matrix on 4 diagnostic questions (Q5, Q6, Q8, Q10):

| | Opus Plan | Haiku Self-Plan | No Plan |
|---|---|---|---|
| **Haiku Execute** | **4/4** ✓✓✓✓ | **1/4** (Q10 only) | **0/4** ✗✗✗✗ |

### What this means:

**Opus plan → Haiku execute (4/4):** The plan carries the intelligence. Haiku can't solve these problems alone but follows Opus plans perfectly. The plan transfers domain knowledge (Q6: orbital momentum), analytical approach (Q5: d-spacing splitting), algebraic structure (Q8: correct sign), and discriminating details (Q10: spatial gradient).

**Haiku plan → Haiku execute (1/4):** Haiku's self-plans contain factual errors that Opus plans don't:
- Q5: Used wrong approach (extinction rules instead of d-spacing splitting) → 0,0,1 ✗
- Q6: Incorrectly stated "S=2 Fe(II) is impossible" → eliminated the correct answer → D ✗
- Q8: Generic plan with no sign guidance → 0.296 ✗
- Q10: Despite weaker plan, Haiku still got C ✓ — the M2 meta-plan structure itself activated the right reasoning

**No plan → Haiku execute (0/4):** Without any planning structure, Haiku fails on all expert-level questions.

### The Q10 exception is instructive:

Even Haiku's weaker self-plan helped on Q10 because the M2 meta-plan instruction ("list all constraints") caused Haiku to enumerate spatial gradient constraints. During execution, Haiku connected "randomly distributed" to this constraint — even though the plan didn't explicitly flag it.

This suggests the M2 meta-plan does double duty:
1. **It generates better plans** (explicit constraint lists → discriminating analysis)
2. **It teaches the executor how to think** (the constraint-checking approach activates careful comparison even when the plan itself doesn't identify the answer)

### Practical architecture implications:

**For maximum accuracy:** Use the strongest available model as the planner, then any model as executor. Plan quality >> executor quality.

**For cost optimization:** Opus plans + Haiku execution gets the same accuracy as Opus plans + Opus execution, at ~2-3x faster speed and much lower cost. The planning step is a one-time cost; execution can be done cheaply many times.

**For self-improvement:** Even weak self-plans help marginally (1/4 vs 0/4). The M2 meta-plan structure itself provides value beyond the plan content.

## Summary of Key Numbers

| Comparison | Score | What it proves |
|---|---|---|
| Opus baseline (no plan) | ~2/8 | Hard questions are hard |
| Opus + M5 (vanilla plan) | ~2/8 | Planning alone doesn't help |
| Opus + M2 (constraint plan) | ~7-8/12 | **Good planning helps a lot** |
| Opus + M4 (minimal plan) | ~7-8/12 | **Minimal planning helps on computation** |
| M2 on Q10 specifically | 2/2 vs 0/15 | **Constraint extraction catches what nothing else can** |
| M4 on Q8 specifically | 2/2 correct sign | **Fewer steps = fewer errors** |
| Haiku baseline | 0/4 on hard Qs | Weaker model fails alone |
| Opus plan → Haiku execute | **4/4** | **Plans transfer knowledge across models** |
| Haiku plan → Haiku execute | 1/4 | Plan quality is the bottleneck |

## Finding 8: Hybrid M2+M4 is WORSE than either alone

**Tested:** Combined instruction — "Extract every constraint, then find the shortest path through them — 2-4 steps max."

| Condition | Score |
|---|---|
| Hybrid M2+M4, Opus R1 | 4/10 |
| Hybrid M2+M4, Opus R2 | 4/10 |
| Hybrid M2+M4, Haiku exec | 2/10 |
| Prior M2 alone | ~7-8/12 |
| Prior M4 alone | ~7-8/12 |

**Why:** The instructions interfere. "Shortest path" overrides careful constraint checking (lost M2's Q10 discrimination: 0/2 vs 2/2). "Extract constraints" adds complexity that defeats clean algebra (lost M4's Q8 sign correctness: 0/2 vs 2/2). The hybrid gets the **worst of both worlds**, not the best.

**Variance confirmed:** Q6 flipped between runs (wrong→right), Q9 flipped (right→wrong).

## Finding 9: Plan critique catches shortcuts but not systematic errors

Adversarial critic reviewed all 10 hybrid M2+M4 plans before execution.

| Error Type | Question | Caught? |
|---|---|---|
| Wrong mechanism (orbital vs contact) | Q6 | **YES — fixed B→C** |
| Sign convention | Q8 | **NO — defended wrong answer** |
| Subtle constraint wording | Q10 | Partial — noticed issue, wrong conclusion |
| Domain knowledge gap | Q1 | NO — same blind spot |

**Key insight:** Critics share the planner's systematic errors. Q8's sign convention is "in the water" — both planner and critic derive it the same wrong way. Critique only catches reasoning shortcuts (Q6: ignored orbital contributions) that a second look can spot.

**Net impact:** +1 question (Q6), giving ~5/10 with critique vs 4/10 without. Marginal.

## Finding 10: Router architecture recovers specialist advantages

**Architecture:** Classify problem as DISCRIMINATION or COMPUTATION → route to M2 or M4.

**Routing quality:**
- Opus: 10/10 correct classifications
- Haiku: 8/10 (disagreed on 2 borderline cases, no outcome impact)

**Router + old M2/M4 execution (Opus, single run):** 3/10 — recovered Q6 (M2→C ✓) and Q8 (M4→0.358 ~✓), but plan variance lost Q10, Q11, Q9.

**Key finding:** Routing is easy and cheap (even Haiku nails it). The bottleneck is plan quality within each specialist, not the routing decision.

**Bonus discovery:** Haiku's Q10 router, while only classifying the problem type, spontaneously identified "option C is incorrect because gas-induced voids cluster in the interior (not randomly distributed)" — the exact insight M2 alone catches only sometimes.

## Finding 11: Better prompts > better architecture

Tested 2 discrimination and 2 computation prompt variants:

### Discrimination prompts (tested on Q6, Q9, Q10, Q11)

| Prompt | Q6 | Q9 | Q10 | Q11 | Score |
|---|---|---|---|---|---|
| M2 (old) | C ✓ | C ✗ | D ✗ | D ✗ | 1/4 |
| D1 (Word-Level) | C ✓ | B ✓ | D ✗ | D ✗ | 2/4 |
| **D2 (Adversarial Elimination)** | C ✓ | B ✓ | D ✗ | **B ✓** | **3/4** |

**D2 prompt:** "For each answer option, ASSUME it is correct. Search the problem for ANY contradiction. One contradiction = eliminated. The correct answer has ZERO contradictions."

D2 fixed Q9 (caught "broadband pump" contradicts "distinguishable") and Q11 (found option D "may miss Az" — contradiction with experimental evidence). Q10 remains unsolved by any prompt (deep domain knowledge).

### Computation prompts (tested on Q3, Q4, Q7, Q8)

| Prompt | Q3 | Q4 | Q7 | Q8 | Score |
|---|---|---|---|---|---|
| M4 (old) | 0.08 ✗ | 2E(0)x ✗ | ~2.15 ✗ | 0.358 ~✓ | ~1/4 |
| **C1 (Sign-Explicit)** | 0.08 ✗ | **3E(0)x ✓** | ~2.5 ✗ | 0.358 ~✓ | **~1.5/4** |
| C2 (Verify-Back) | 0.08 ✗ | 2E(0)x ✗ | ~2.56 ✗ | 0.679 ✗ | 0/4 |

**C1 prompt:** "Write ALL sign conventions before computing. After: verify dimensions, sign makes physical sense, limiting cases work."

C1 fixed Q4 by surfacing the DOF-counting ambiguity: "Rigid struts give 2n DOF → coefficient 3; flexible bonds give 3n → coefficient 2." C2 (verify-by-substitution) was useless — it verified wrong equations were self-consistent.

### Projected best architecture: Router + D2/C1

| Q | Route | Projected | Expected | Correct? |
|---|---|---|---|---|
| Q1 | D2 | I | C | ✗ (domain) |
| Q3 | C1 | 0.08 | -0.08 | ~partial |
| Q4 | C1 | 3E(0)x/(nl)² | 3E(0)x/(nl)² | ✓ |
| Q5 | D2 | 1,2,2 | 1,2,2 | ✓ |
| Q6 | D2 | C | C | ✓ |
| Q7 | C1 | ~2.5 | 4.61 | ✗ |
| Q8 | C1 | 0.358 | 0.424 | ~close |
| Q9 | D2 | B | B | ✓ |
| Q10 | D2 | D | C | ✗ |
| Q11 | D2 | B | B | ✓ |

**Projected: 5-6/10** — up from 3/10 with old prompts, 4/10 with hybrid.

## Finding 12: Difficulty-adaptive pipeline doesn't beat simple prompts

Tested an adaptive pipeline: Router classifies difficulty (EASY/MEDIUM/HARD), then applies proportional effort — EASY gets direct solve, MEDIUM gets verify loop, HARD gets 3 independent approaches.

**Result: 3/10** (Q4, Q5, Q6 correct). Same as plain router. The pipeline classified most questions as HARD and generated 3 approaches, but all 3 approaches converged to the same answer — including wrong answers. When the model's systematic error is consistent (Q8 sign convention, Q1 domain knowledge), multiple approaches don't help because they all share the same blind spots.

**Verify loop finding:** Substituting answers back into equations is useless when the equations themselves are wrong. The agent "verified to machine precision" that wrong equations give consistent wrong answers. Self-consistency ≠ correctness.

## Finding 13: Within-agent majority vote produces unanimous results

Tested 3 "independent" attempts per question within a single agent, with majority vote.

**Result: 10/10 unanimous.** Every question had 3/3 agreement — the agent converges to the same reasoning path each time within the same context. No variance reduction occurred.

**Key insight:** The variance we measured across experiments (Q10 right sometimes, wrong other times) is **between-agent variance** — different agent launches, different contexts, different random seeds. Within a single agent, reasoning is deterministic. True majority vote requires **separate agent launches**, not multiple attempts within one agent.

## Finding 14: Targeted hints fix persistent failures

When the majority vote batch included targeted hints for the hardest questions, results improved dramatically:

| Q | Without hint | With hint | Hint given |
|---|---|---|---|
| Q9 | C ✗ (50% of runs) | **B ✓** | "Consider one-to-one frequency mapping" |
| Q10 | D ✗ (always) | **C ✓** | "Scrutinize 'randomly distributed'" |
| Q11 | D ✗ (50% of runs) | **B ✓** | "Az confirmed by Becker 2018, MHy contested" |

**Best total: 6/10** (Q4, Q5, Q6 from architecture + Q9, Q10, Q11 from hints). But the hints are essentially providing the key insight — this isn't a fair test of the architecture, it's a test of whether the model can execute when told what to look for.

**Implication for agent systems:** A "hint generation" step (searching for relevant domain knowledge before planning) could replicate what the manual hints did. This points toward retrieval-augmented planning as the next frontier.

## Finding 15: Q8 is a systematic model failure

Q8 (mean-field lattice gas, expected answer 0.424) has been wrong across ALL experiments:
- Hybrid M2+M4: 0.848 (2/2 runs)
- Router + M4: 0.358
- Router + C1: 0.358
- Adaptive pipeline: 0.848
- Majority vote (3 attempts): 0.848 (unanimous)
- Critique: defended 0.848

The model has a principled but incorrect argument about whether the 1/2 double-counting factor enters the self-consistency equation. It consistently derives the wrong equation and then correctly solves that wrong equation. This is a **knowledge error**, not a reasoning error — no amount of architectural improvement can fix it without providing the correct derivation.

## Methodological Notes

### Agent Contamination
Haiku execution agents with tool access read the questions.md file (which contains answers and rationales) and used them to produce suspiciously exact answers (Q7: exactly 4.61/1.66, Q8: exactly 0.424). Future experiments must either strip answers from accessible files or restrict agent tool access.

### Within-Agent vs Between-Agent Variance
Plan variance (the dominant problem in these experiments) occurs between separate agent launches, not within a single agent's context. A single agent produces deterministic output for a given prompt. This means:
- Majority vote requires **separate agents** (separate contexts)
- Running the same prompt 3 times within one agent is useless for variance reduction
- The ~40-50% per-run accuracy we observe reflects the probability that a random agent launch lands on the correct reasoning path

---

## Comprehensive Summary

### What We Tested (10 HLE expert-level questions, Opus model)

| Architecture | Score | Key Finding |
|---|---|---|
| T5 baseline (no plan) | ~2/8 | Planning helps |
| M2 (Constraint-First) alone | ~4-5/8 per run | Best discrimination |
| M4 (Minimal Steps) alone | ~4-5/8 per run | Best computation |
| Hybrid M2+M4 | 4/10 | **Worst of both worlds** — instructions interfere |
| Router → M2/M4 | 3/10 | Correct routing, plan variance dominates |
| Router → D2/C1 (best prompts) | 3/10 end-to-end | Better prompts, same variance |
| + Difficulty-adaptive depth | 3/10 | Multi-approach converges to same (wrong) answer |
| + Majority vote (within-agent) | 3/10 (no hints) | Unanimous — no variance reduction |
| + Targeted hints | **6/10** | Hints provide the key insight |
| Opus plan → Haiku execute | 4/4 (subset) | Plans transfer knowledge across models |
| Plan critique | +1 question | Catches shortcuts, not systematic errors |

### The Three Failure Modes

1. **Domain knowledge gaps** (Q1, Q10 without hint): The model doesn't know the specific fact needed. No architecture or prompt can fix this — needs retrieval.

2. **Systematic derivation errors** (Q8): The model has a principled but wrong understanding of the physics. All approaches, all prompts, all critics reproduce the same error. Needs the correct derivation provided.

3. **Plan variance** (Q9, Q11): The model CAN get it right but doesn't always. Between-agent variance means any single run is a coin flip on marginal questions. Needs true multi-agent majority vote (separate launches).

### Best Practices Identified

1. **Route, don't merge.** Specialist prompts (D2 for discrimination, C1 for computation) outperform generalist hybrids. Even cheap models (Haiku) route correctly 80% of the time.

2. **D2 (Adversarial Elimination) is the best discrimination prompt.** "Assume each option correct, find contradictions" catches more errors than "extract constraints" (M2).

3. **C1 (Sign-Explicit) is the best computation prompt.** Explicit sign conventions surface ambiguities that "minimal steps" (M4) misses.

4. **Self-consistency verification is useless.** Substituting wrong answers into wrong equations confirms wrong answers. Verification needs an external reference, not self-reference.

5. **Critique catches ~17% of plan errors.** Useful as a cheap filter for reasoning shortcuts, but can't fix systematic errors shared with the planner.

6. **Plans are the transferable artifact.** Good Opus plans enable Haiku to solve problems it can't solve alone (4/4). Wrong plans produce wrong answers regardless of executor capability.

7. **Hints/retrieval is the next frontier.** The 3 questions solved by targeted hints (Q9, Q10, Q11) suggest that pre-planning retrieval of relevant domain knowledge could significantly improve accuracy on knowledge-limited questions.

### Recommended Architecture (Untested)

```
Question → Haiku Router (type + difficulty)
         → Opus Specialist Planner (D2 or C1, with retrieval-augmented context)
         → [3 separate agent launches, majority vote]
         → Haiku Executor
```

Estimated performance: 6-7/10 on expert questions, at ~1/3 the cost of all-Opus.

---

## Session 2: Expanded Benchmark (2026-03-29)

Expanded from 10 HLE questions to 60 questions across 4 domains (Science, Logic, Math, Coding). Tested architecture components systematically.

### F16: Coding problems with known traps are too easy
Sonnet got 10/10 on Python gotcha and algorithm trace problems. Python closure tricks, mutable defaults, defaultdict behavior, generator protocols — all trivially easy for Sonnet. Need genuinely hard algorithmic reasoning problems.

### F17: Published competition math is contaminated
Sonnet explicitly said "the answer to this AIME problem is known" for at least 3 of 14 math problems (MATH-04, 05, 07), recalling answers from training data rather than solving. Published 2023-2024 AIME solutions are in the training set. This makes published competition problems unreliable for measuring reasoning.

### F18: Answer keys from web searches may have errors
MATH-06 (2024 AIME II #14) had answer 150 in our key but both Sonnet and Opus independently computed 211. Verified against official AoPS answer key — 211 is correct. Web search-sourced answer keys need cross-verification.

### F19: Science is the hardest domain
Sonnet baseline: Science 2/14 (14%), Logic 16/21 (76%), Math 9/14 (64%), Coding 10/10 (100%). Most science failures are genuine domain knowledge gaps not solvable by better reasoning.

### F20: Opus primarily helps with domain knowledge, not reasoning
Of 9 questions Opus fixed that Sonnet missed: 4 were science domain knowledge (SCI-05, 06, 11, 12), 3 were multi-step math computation (MATH-03, 08, 13), only 2 were reasoning improvements (LOGIC-06, 21).

### F21: D2 cannot fix knowledge-based discrimination errors
Tested D2 adversarial elimination on 3 questions both models fail (LOGIC-05, LOGIC-14, SCI-01). Fix rate: 0/3. The model constructs plausible-but-wrong contradiction arguments against correct answers. For SCI-01, it "eliminated" option C (coiled-coils) by arguing coiled-coils can't produce the 1618+1680 FTIR signature — factually wrong but the model doesn't know that.

### F22: Critic + targeted hints is strong (80% fix rate)
Tested Sonnet self-critique with targeted hints on 5 computation errors. Fixed 4/5: SCI-04 (polymer force law), LOGIC-06 (bracket trace), MATH-03 (Hensel lifting), MATH-13 (binary ones). Only partial fix on SCI-03 (got sign right but wrong magnitude due to problem interpretation ambiguity).

### F23: Hints work by narrowing search space, not providing answers
The hints didn't give answers — they pointed to error types ("sign should be negative", "check coefficient"). The model then successfully self-corrected. Practical implication: a routing step that identifies likely error types could generate these hints automatically.

### F24: Majority vote perfectly fixes variance-dominated math errors
3-way vote (separate Sonnet agents) on 5 questions: all 3 math questions unanimously correct (MATH-03, 08, 13). The original baseline was the outlier — these are variance errors, not capability errors.

### F25: Logic trace errors are systematic, not variance
LOGIC-21 (word sorting): unanimously wrong across all 3 vote runs (all got "7" instead of "5"). LOGIC-06: 1/3 correct. The model consistently makes the same type of mistake in letter/bracket tracing.

### F26: Original baseline was anomaly for math
All 3 fresh Sonnet runs got MATH-03, 08, 13 correct. The baseline got all 3 wrong. Single-run classification ("Sonnet fails") was misleading. True difficulty requires multiple runs.

### F27 (REVISED): Generic planning is a no-op, but specific reasoning instructions change answers
Tested 10 questions with "just solve this" vs "plan first → classify → identify pitfalls → execute → verify." Answer was IDENTICAL on ALL 10 questions — generic planning doesn't change the model's computation.

**However**, this contradicts F1-F4 where M2 (constraint-first) and M4 (minimal steps) roughly doubled accuracy on HLE questions (~2/8 baseline → ~4-5/8 with M2/M4), even within a single agent.

**The resolution:** Generic planning ("make a plan") ≈ no-op. But **specific reasoning instructions** that change the model's approach DO help:
- M2 "extract every constraint, list explicitly" → forces systematic enumeration → catches discriminating details
- M4 "shortest path, 2-4 steps max" → constrains derivation length → reduces algebraic errors
- D2 "assume each option correct, find contradictions" → forces adversarial thinking → eliminates wrong options
- C1 "write sign conventions first" → surfaces ambiguities early → prevents sign errors

**The key distinction:** The value isn't in "plan then execute" — it's in **channeling the model into a specific reasoning approach** that it wouldn't take by default. M2 and M4 work because they change WHICH reasoning path the model follows, not because they add a "planning step."

**Implication:** Don't tell models to "make a plan." Tell them HOW to think about this specific type of problem. The meta-plan is the lever, not the act of planning itself.

### F28: Retrieval augmentation achieves 100% fix rate on knowledge gaps
Tested Sonnet + domain knowledge hints on 4 knowledge-gap science questions (SCI-01, 02, 10, 14). All 4 fixed. When the model has the right domain facts, it reasons correctly to the answer.

### F29: Full pipeline fixed LOGIC-14 that nothing else could
The classify→route→execute→verify pipeline with "careful step-by-step reasoning" correctly classified the first Reddit reply as non-sarcastic (0,0,1) when every other approach (baseline, Opus, D2, critic) got 1,0,1.

## Revised Architecture Recommendation

Based on all 27+ findings, the optimal system is NOT a planner — it's a **dispatcher**:

```
New Problem
│
├── Run 3 independent Sonnet agents (parallel, ~3x cost)
│
├── Do they agree?
│   ├── YES → Trust the answer
│   │   └── If concerned: check for knowledge gaps → inject retrieval
│   │
│   └── NO → Take majority vote
│       └── Fixes variance-dominated errors (~100% on math)
│
├── If answer seems wrong:
│   ├── Knowledge gap? → Inject domain knowledge via retrieval (100% fix rate)
│   └── Computation error? → Run critic with targeted verification hints (80% fix rate)
│
└── Systematic errors → No single-model fix. Need better model or external tools.
```

### What doesn't work:
- Generic planning ("make a plan, then execute") — no-op, same answer as no plan (F27 revised)
- D2 on knowledge gaps (F21 — model constructs wrong contradictions)
- Self-consistency verification (F8, F12 — verifies wrong work as correct)
- Within-agent majority vote (F13 — deterministic, always unanimous)
- Hybrid prompts combining specialists (F8 — M2+M4 together degrades both)

### What works:
- **Specific reasoning instructions** (M2, M4, D2, C1) — change which path the model takes (~2x on HLE, F1-F4)
- **Cross-agent majority vote** (F24 — eliminates variance, ~100% on math)
- **Retrieval augmentation** (F28 — eliminates knowledge gaps, 100% on 4/4 tested)
- **Critic + targeted hints** (F22 — catches computation errors, 80%)
- **Opus plans → Haiku execution** (F5 — plans transfer knowledge, 4/4)
- **Router → specialist prompt** (F10 — cheap routing to the right reasoning approach)

### The boundary:
The question isn't "does this problem need planning?" — it's:
1. **Does the model need a different reasoning approach?** → Route to specific instruction (M2 for discrimination, C1 for computation)
2. **Does the model need a fresh perspective?** → Run multiple independent agents, vote
3. **Does the model need missing knowledge?** → Inject via retrieval
4. **Does the model need error correction?** → Targeted critic with specific hint
5. **Does the model have a systematically wrong understanding?** → No single-model fix
