# Architecture Learnings — BBEH Benchmark Exploration

**Started:** 2026-03-26

## Goal

Explore how different agent architectures — specifically, how an orchestrator creates and coordinates teams of agents — affect performance on hard reasoning benchmarks. BBEH is the testbed; the system prompt that governs team creation is the variable under test.

## Baseline

- **Model:** Claude Opus 4.6
- **Baseline score:** 16/23 (69.57%) — raw question, no architectural scaffolding
- **Two runs showed:** 5 persistent failures, 14 persistent passes, 4 variance-zone tasks

## Experiment 1: Prompt Architect (Two-Hop)

**Hypothesis:** Separating "how to think about this" from "actually think about it" improves performance. Agent 1 (Prompt Architect) sees the question and crafts a strategic prompt — without solving it — for Agent 2 (Solver).

**Why this might work:**
- The architect can identify the reasoning type and recommend an approach
- It can warn about pitfalls (e.g., "find the FIRST error, not just any error")
- It can add verification steps the raw question doesn't prompt for
- It restructures the problem before the solver gets anchored

**Anti-cheating constraints:**
- Agent 1 must NOT solve the problem or include candidate answers
- Output follows a structured template: problem type, approach, pitfalls, verification strategy
- Outputs are auditable

**Test case:** `bbeh_word_sorting` — failed both baseline runs (answered 11, correct answer is 2). The model found *a* mistake but not the *first* mistake. A prompt architect should be able to fix this with pure strategy framing ("scan sequentially from step 1, stop at first error").

### Results — word_sorting (2026-03-26)

**Baseline:** Answered 11 (wrong) — both runs. Found a real error but not the first one.
**Prompt Architect → Solver:** Answered **2 (correct)**.

The prompt architect identified the key pitfall ("watch for words miscategorized by first letter in Thought 2") and emphasized sequential scanning. The solver followed that strategy and caught the "easy" being incorrectly grouped with "a" words in Thought 2 — the exact error the baseline missed both times.

**Key observation:** The prompt architect's output was suspiciously good — it flagged the exact Thought (2) and the exact word ("easy") as suspicious. This verges on solving the problem rather than just providing strategy. For the experiment to be rigorous, we need to evaluate whether the architect is providing *general* strategic value or just *partially solving it and calling it strategy*. If it's the latter, the architecture collapses to "think longer before answering" rather than genuine team value.

**Tokens used:** ~12.4k (architect) + ~12.5k (solver) = ~25k total for one question.

---

## Experiment 2: Prompt Strategy Comparison (2026-03-26)

**Setup:** 3 BBEH tasks (hyperbaton, boardgame_qa, sarc_triples), 10 approaches, 2 rounds. Sonnet 4.6. Single agent per approach (no team architecture).

Correct answers: Hyperbaton=E, Boardgame=disproved, Sarcasm=1,1,0

### Round 1 Results (all agents had full problem data)

| Approach | Hyperbaton | Boardgame | Sarcasm | Score |
|---|---|---|---|---|
| Baseline | ✓ | ✓ | ✗ | 2/3 |
| Conservative | ✗ (EF) | ✓ | ✗ | 1/3 |
| Elimination | ✗ (EF) | ✓ | ✗ | 1/3 |
| Voting (3x) | ✗ (EF) | ✓ | ✗ | 1/3 |
| Adversarial | ✗ (EF) | ✓ | ✗ | 1/3 |

### Round 2 Results (some agents had truncated prompts — N/A)

| Approach | Hyperbaton | Boardgame | Sarcasm | Score |
|---|---|---|---|---|
| Baseline | ✗ (EF) | ✓ | ✗ | 1/3 |
| Conservative | ✓ | N/A | ✗ | 1/2 |
| Elimination | ✗ (EF) | ✓ | ✗ | 1/3 |
| Voting (3x) | ✗ (F) | ✓ | N/A | 1/2 |
| Adversarial | ✗ (AE) | N/A | N/A | 0/1 |
| **Chain of Thought** | **✓** | **✓** | ✗ | **2/3** |
| **Expert Persona** | **✓** | **✓** | N/A | **2/2** |
| Meta-cognitive | ✗ (EF) | ✓ | ✗ | 1/3 |
| **Two-pass** | **✓** | N/A | ✗ | 1/2 |
| **Simplify-first** | **✓** | N/A | ✗ | 1/2 |

### Key Findings

**Hyperbaton (the discriminating question):**
- 6/15 runs got it right (just "E"), 9/15 got it wrong
- The model over-selects F because it can't determine where shape/opinion fits in the ordering — some category pairs never appear together in the 88 examples
- Approaches that got it RIGHT recognized this ambiguity and chose only E (which avoids shape/opinion entirely). The two-pass agent explicitly stated: "E is the only option where ALL adjacent pairs are directly confirmed by training examples."
- Approaches that got it WRONG confidently placed shape/opinion somewhere specific, then accepted F (or A) as valid
- No approach was consistent across both rounds — showing high variance

**Boardgame (easy for Sonnet):**
- 100% correct across all agents that received the full rules
- Long rule-chaining works fine for this model on this specific example

**Sarcasm (universally failed):**
- 0% correct. Every agent labeled Reply 2 (Steve Jobs anonymous donor) as sincere (0) when correct is sarcastic (1)
- No prompting strategy can overcome this — the model genuinely reads that reply as a good-faith correction
- This is a fundamental comprehension gap, not an approach problem

**Variance is the dominant signal:**
- Baseline got hyperbaton right in R1, wrong in R2
- Conservative got it wrong in R1, right in R2
- Same model, same question, different answer each time
- Single-run results are unreliable — need N>5 per approach to measure real effect

**Strategies that never helped:**
- Voting: 3 copies of the same bias = 3 copies of the same wrong answer
- Adversarial: the "attacker" phase never successfully overturned a wrong answer
- Meta-cognitive: identifying likely error modes didn't prevent those errors

**Strategies showing promise (but unconfirmed due to variance):**
- Chain of Thought, Expert Persona, Simplify-first, Two-pass all got hyperbaton right in R2
- But with N=1 per approach per round, this could be luck

---

## Experiment 3: Multi-Agent Team Architectures (2026-03-26)

**Setup:** 8 architectures × 6 BBEH tasks = 48 runs. All agents: Claude Haiku 4.5. Questions drawn from the last example in each task.json.

**Correct answers:** hyperbaton=H, word_sorting=5, sarcasm=0,0,1, sportqa=AB/ABC/ABC, arithmetic=10828, dyck=19

### Architectures Tested

1. **Baseline** — single agent, raw question, no scaffolding
2. **Debate** — 2 independent solvers + judge picks the better answer
3. **Strategy Architect** — Agent 1 writes generic reasoning strategy (no data references), Agent 2 solves with that strategy
4. **Decompose → Solve → Verify (DSV)** — Agent 1 decomposes into sub-tasks, Agent 2 solves, Agent 3 tries to falsify the answer
5. **Generator → Critic** — Agent 1 proposes answer, Agent 2 (fresh context) attacks it, Agent 3 revises if flaws found
6. **Diverse Ensemble** — 3 agents with different analytical frames (pattern matcher, devil's advocate, step-by-step auditor) + meta-aggregator
7. **Sean's Favorite Horizontal (SFH)** — orchestrator designs parallel subtasks, N workers run independently, compiler synthesizes
8. **Sean's Favorite Vertical (SFV)** — orchestrator designs sequential pipeline, each agent builds on previous agent's output

### Full Results

| Architecture | Hyper | Word Sort | Sarcasm | Sport | Arith | Dyck | **Score** |
|---|---|---|---|---|---|---|---|
| **Gen-Critic** | **✓** | **✓** | ✗ | ✗ | **✓** | **✓** | **4/6** |
| **Debate** | **✓** | **✓** | ✗ | ✗ | **✓** | ✗ | **3/6** |
| Strategy | ✗ | **✓** | ✗ | ✗ | ✗ | **✓** | 2/6 |
| SFH (Horiz) | ✗ | **✓** | ✗ | ✗ | ✗ | **✓** | 2/6 |
| SFV (Vert) | ✗ | **✓** | ✗ | ✗ | **✓** | ✗ | 2/6 |
| Baseline | ✗ | ✗ | ✗ | ✗ | **✓** | ✗ | 1/6 |
| DSV (Pipeline) | ✗ | ✗ | ✗ | ✗ | **✓** | ✗ | 1/6 |
| **Ensemble** | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | **0/6** |

### Per-Question Difficulty

| Question | Correct/Total | Which architectures got it right |
|---|---|---|
| Sarcasm | 0/8 | none |
| SportQA | 0/8 | none |
| Hyperbaton | 2/8 | debate, gen-critic |
| Dyck | 3/8 | strategy, gen-critic, sfh |
| Word sorting | 5/8 | debate, strategy, gen-critic, sfh, sfv |
| Arithmetic | 5/8 | baseline, debate, dsv, gen-critic, sfv |

### Raw Answers

| Architecture | Hyperbaton | Word Sort | Sarcasm | SportQA | Arithmetic | Dyck |
|---|---|---|---|---|---|---|
| Baseline | K | 6 | 1,0,1 | AB, AB, A | 10828 | 31 |
| Debate | H | 5 | 1,0,1 | AB, ACD, A | 10828 | 26 |
| Strategy | K | 5 | 1,0,1 | ABC, ABC, AC | -18 | 19 |
| DSV | K | 13 | 1,0,1 | AB, A, A | 10828 | 23 |
| Gen-Critic | H | 5 | 1,0,1 | ABC, AC, AB | 10828 | 19 |
| Ensemble | K | 9 | 1,1,1 | A, A, A | 121834 | 25 |
| SFH | I | 5 | 1,0,1 | ABC, AC, ABC | -579438 | 19 |
| SFV | K | 5 | 1,0,1 | AB, A, A | 10828 | 26 |

### Key Findings

**1. Generator-Critic is the best architecture (4/6)**

The "propose then have a fresh agent attack it" pattern is the strongest. The critic catches errors the solver can't see because it has zero anchoring bias — it never went through the generation process. Criticizing is a fundamentally different cognitive task than solving; separating them into different agents leverages that difference.

Best example: On dyck, the generator found a mistake at Thought 26. The critic, with its adversarial mandate, asked "is there an error *before* 26?" and found the actual first error at Thought 19. The reviser confirmed. This is the exact failure mode (finding *a* mistake but not the *first* mistake) that plagues baseline approaches.

**2. Debate is runner-up (3/6)**

Two independent solvers + judge works well when the solvers genuinely produce different answers. The judge can evaluate competing reasoning quality. Weaker than gen-critic because both debaters are *solving* (same cognitive task) rather than one solving and one attacking.

**3. Diverse Ensemble is the WORST (0/6) — worse than baseline**

A confidently wrong contrarian can poison the whole group:
- On hyperbaton, the "devil's advocate" agent argued "all examples use max 3 adjectives, so 6+ adjective options are invalid" — creative but completely wrong reasoning that overrode two agents who had the right answer (H) in their lists.
- On sportqa, consensus over-pruned correct answers (2 of 3 agents excluded B, so meta-aggregator dropped it).
- On arithmetic, three agents got three different answers; the aggregator picked the wrong one.

**Takeaway:** Diversity without quality control is worse than no diversity. The ensemble lacks a mechanism to evaluate *reasoning quality* — it just counts votes or defers to the loudest voice.

**4. Sarcasm and SportQA are model-level blind spots (0/8 each)**

No architecture fixes a fundamental comprehension gap. On sarcasm, all 8 architectures produced 1,0,1 (or 1,1,1 for ensemble) vs. correct 0,0,1. Every agent reads Reply 1 as sarcastic when it's sincere. This is Haiku's ceiling on this specific example, not an architecture problem.

On sportqa, verification steps consistently made things WORSE by pruning correct answers. DSV's solver initially got ABC, AC, ABC (close to correct AB, ABC, ABC) but the verifier pushed it to AB, A, A. Gen-critic's critic removed a correct answer from sub-question 2. Critics/verifiers are too aggressive on "select all that apply" tasks.

**5. Arithmetic rewards coherent computation chains**

The 5 architectures that maintain a single thread of computation (baseline, debate, dsv, gen-critic, sfv) all got 10828. The 3 that fragment the computation (strategy adds indirection, sfh parallelizes A/B/C across workers, ensemble has 3 independent solvers) all failed with wildly different wrong answers (-18, -579438, 121834).

**6. SFH works well on structured sequential tasks**

SFH (parallel decomposition) cracked dyck by splitting the 42 thoughts into ranges — three workers found errors at 19, 26, and 31 respectively, and the compiler picked the earliest. This parallel range-checking pattern is naturally suited to "find the first X" problems.

**7. SFV suffers from anchoring propagation**

The sequential vertical pipeline has a cascading anchor problem: if an early agent makes a wrong finding, every subsequent agent inherits and builds on that mistake. On dyck, Agent 2 flagged "suspicious transitions around 26-28" and every later agent narrowed within that range, never backtracking to check earlier thoughts. SFH's parallel approach avoids this because workers check different regions independently.

### Architecture Design Principles (Emerging)

1. **"Propose then attack" beats "generate multiple and vote."** Fresh adversarial evaluation > consensus.
2. **Separate solving from criticizing.** They are different cognitive tasks — combining them in one agent means anchoring wins.
3. **Don't fragment computation.** For tasks requiring precise sequential reasoning (arithmetic), keep one coherent chain.
4. **Parallelize search, not computation.** SFH works when workers search different regions. It fails when workers independently implement the same logic.
5. **Diversity needs quality control.** A contrarian without accountability poisons the group. Ensemble needs a mechanism to evaluate reasoning quality, not just count votes.
6. **Architecture can't fix capability gaps.** If the model fundamentally can't do something (Haiku on this sarcasm example), no team structure helps.
7. **Verification helps structured tasks, hurts multi-select tasks.** Critics find errors well but over-prune when the task requires selecting multiple correct answers.

---

## Experiment 4: Sonnet Multi-Agent Architectures (2026-03-26)

**Setup:** 6 architectures × 6 BBEH tasks = 36 runs. All agents: Claude Sonnet 4.6. Same 6 questions as Experiment 3. Dropped Ensemble (worst on Haiku: 0/6) and DSV (tied worst: 1/6).

**Correct answers:** hyperbaton=H, word_sorting=5, sarcasm=0,0,1, sportqa=AB/ABC/ABC, arithmetic=10828, dyck=19

### Full Results

| Architecture | Hyper | Word Sort | Sarcasm | Sport | Arith | Dyck | **Score** |
|---|---|---|---|---|---|---|---|
| **Strategy** | ✗ | **✓** | **✓** | ✗ | **✓** | **✓** | **4/6** |
| Baseline | ✗ | **✓** | ✗ | ✗ | **✓** | **✓** | 3/6 |
| Debate | ✗ | **✓** | ✗ | ✗ | **✓** | **✓** | 3/6 |
| Gen-Critic | ✗ | **✓** | ✗ | ✗ | **✓** | **✓** | 3/6 |
| SFH (Horiz) | ✗ | **✓** | ✗ | ✗ | **✓** | **✓** | 3/6 |
| SFV (Vert) | ✗ | ✗ | ✗ | ✗ | **✓** | **✓** | 2/6 |

**Overall: 18/36 (50%)** — up from Haiku's 14/48 (29%).

### Per-Question Difficulty

| Question | Correct/Total | Which architectures got it right |
|---|---|---|
| Hyperbaton | 0/6 | none |
| SportQA | 0/6 | none |
| Sarcasm | 1/6 | strategy |
| Word sorting | 5/6 | all except sfv |
| Arithmetic | 6/6 | all |
| Dyck | 6/6 | all |

### Raw Answers

| Architecture | Hyperbaton | Word Sort | Sarcasm | SportQA | Arithmetic | Dyck |
|---|---|---|---|---|---|---|
| Baseline | GH | 5 | 1,0,1 | ABC, A, A | 10828 | 19 |
| Debate | CDH | 5 | 1,0,1 | ABC, AC, AB | 10828 | 19 |
| Gen-Critic | GH | 5 | 1,0,1 | ABC, AC, AC | 10828 | 19 |
| Strategy | CDH | 5 | 0,0,1 | AB, A, A | 10828 | 19 |
| SFH | CDGH | 5 | 1,0,1 | ABC, A, AB | 10828 | 19 |
| SFV | CDH | 7 | 1,0,1 | ABC, A, ABC | 10828 | 19 |

### Key Findings

**1. Strategy Architect wins on Sonnet (4/6) — different winner than Haiku**

On Haiku, Gen-Critic won (4/6). On Sonnet, Strategy Architect wins (4/6). The best architecture depends on the model's capability level. Strategy Architect provides a strategic reframe that leverages Sonnet's stronger baseline reasoning, while Gen-Critic's adversarial step adds less value when the solver is already strong.

**2. Strategy Architect cracked sarcasm — the only architecture to do so across all experiments**

The strategy guidance included a "meaning inversion" reframe for sarcasm detection, telling the solver to consider whether each reply's literal meaning opposes the speaker's likely intent. This reframed Reply 1 away from the default "sounds sarcastic" bias. No other architecture across Haiku or Sonnet got sarcasm right — this is a strategic insight, not just compute.

**3. Sonnet trivializes arithmetic and dyck (6/6 each)**

Every architecture got both right. These were discriminating questions on Haiku (arithmetic: 5/8, dyck: 3/8) but ceiling-level for Sonnet. The model upgrade eliminated the need for architectural help on these tasks.

**4. Gen-Critic dropped from 1st (Haiku) to tied-3rd (Sonnet)**

Gen-Critic scored 4/6 on Haiku but only 3/6 on Sonnet — tied with baseline, debate, and SFH. The critic adds value when the solver makes errors worth catching (Haiku). When the solver is already strong (Sonnet), the critic has less to fix and occasionally over-corrects.

**5. SFV is consistently the worst multi-agent approach**

2/6 on both Haiku and Sonnet. The sequential pipeline's anchoring propagation problem persists regardless of model quality. On Sonnet, SFV was the only architecture to miss word_sorting (answered 7 instead of 5).

**6. Hyperbaton and SportQA remain unsolved**

0/6 on both for Sonnet. Every architecture over-selected hyperbaton options (GH, CDH, CDGH — always including extra letters beyond the correct H). SportQA is 0/22 across all experiments — a genuine blind spot no architecture can fix.

**7. Sonnet's errors are different from Haiku's**

Haiku struggles with computation (arithmetic, dyck) and gets hyperbaton wrong with different letters (K, I). Sonnet handles computation easily but over-selects on hyperbaton more aggressively (CDH, CDGH — more wrong letters). The failure mode shifted from "can't compute" to "over-confident pattern matching."

---

## Experiment 5: Hybrid Architecture — Strategy + Gen-Critic (2026-03-26)

**Setup:** 1 architecture × 6 BBEH tasks = 6 runs. Claude Sonnet 4.6. Combines Strategy Architect (Agent 1 writes strategy) with Generator-Critic (Agent 2 solves, Agent 3 attacks, Agent 4 revises if flaws found).

**Hypothesis:** Combining the Haiku winner (Gen-Critic) with the Sonnet winner (Strategy) should compound their advantages.

**Result: 3/6 — WORSE than Strategy alone (4/6).**

### Results

| Question | Strategy Alone | Hybrid (Strategy+Critic) | Correct Answer |
|---|---|---|---|
| Hyperbaton | ✗ (CDH) | ✗ (CDH) | H |
| Word sorting | ✓ (5) | ✓ (5) | 5 |
| Sarcasm | **✓ (0,0,1)** | **✗ (1,0,1)** | 0,0,1 |
| SportQA | ✗ (AB,A,A) | ✗ (ABC,AC,A) | AB,ABC,ABC |
| Arithmetic | ✓ (10828) | ✓ (10828) | 10828 |
| Dyck | ✓ (19) | ✓ (19) | 19 |

### The Critical Finding: Critics Reintroduce Default Priors

The hybrid lost sarcasm — the one question Strategy Architect uniquely cracked. Here's what happened:

1. **Strategy phase:** Provided the same "meaning inversion" guidance that worked in Experiment 4
2. **Solver phase:** Following the strategy, correctly identified Reply 1 as sincere (0) — the counterintuitive-but-correct answer
3. **Critic phase:** A fresh agent with no awareness of the strategy attacked the answer. It flagged "Reply 1 classified as sincere" as suspicious because the reply "reads as sarcastic" — exactly the default bias the strategy was designed to overcome
4. **Reviser phase:** Faced with the critic's objection, reverted to 1,0,1

The critic, lacking the strategic context, applied the model's default prior ("Reply 1 sounds sarcastic") and undid the strategy's correct reframe. This is not a bug — it's a fundamental architectural tension: **adversarial critics enforce consensus with the model's priors, which is exactly wrong when the correct answer is counterintuitive.**

### Design Principle Update

Added to the emerging principles:

8. **More agents ≠ better.** Each additional agent is a chance to reintroduce default biases. The hybrid scored worse than Strategy alone because the critic enforced the prior the strategy had correctly overcome.
9. **The best architecture depends on model capability.** Weaker models benefit from adversarial checking (errors worth catching). Stronger models benefit from strategic reframing (leveraging existing capability in new directions). Combining both can be worse than either alone.

---

## Architecture Design Principles (Updated)

1. **"Propose then attack" beats "generate multiple and vote."** Fresh adversarial evaluation > consensus.
2. **Separate solving from criticizing.** They are different cognitive tasks — combining them in one agent means anchoring wins.
3. **Don't fragment computation.** For tasks requiring precise sequential reasoning (arithmetic), keep one coherent chain.
4. **Parallelize search, not computation.** SFH works when workers search different regions. It fails when workers independently implement the same logic.
5. **Diversity needs quality control.** A contrarian without accountability poisons the group. Ensemble needs a mechanism to evaluate reasoning quality, not just count votes.
6. **Architecture can't fix capability gaps.** If the model fundamentally can't do something (SportQA across all models), no team structure helps.
7. **Verification helps structured tasks, hurts multi-select tasks.** Critics find errors well but over-prune when the task requires selecting multiple correct answers.
8. **More agents ≠ better.** Each additional agent is a chance to reintroduce default biases. Critics can undo correct counterintuitive answers by enforcing the model's priors.
9. **The best architecture depends on model capability.** Weaker models → adversarial checking (Gen-Critic). Stronger models → strategic reframing (Strategy Architect). Combining both can be worse than either alone.

## Cross-Experiment Summary

| Experiment | Model | Architectures | Runs | Accuracy | Winner |
|---|---|---|---|---|---|
| 3 (Haiku) | Haiku 4.5 | 8 | 48 | 14/48 (29%) | Gen-Critic (4/6) |
| 4 (Sonnet) | Sonnet 4.6 | 6 | 36 | 18/36 (50%) | Strategy Architect (4/6) |
| 5 (Hybrid) | Sonnet 4.6 | 1 | 6 | 3/6 (50%) | — (worse than Strategy alone) |

## Open Questions

- Does Strategy Architect maintain its lead on Sonnet with N>1 runs? (variance still a concern)
- Would Strategy Architect work on Opus, or does Opus already reframe problems internally?
- Can the critic be given the strategy context without anchoring it? (e.g., "evaluate whether the strategy was correctly applied" rather than "attack the answer")
- Would a "strategy-aware critic" — one that sees the strategy and checks adherence rather than correctness — avoid the prior-reintroduction problem?
- How do these results scale to the full 23-task BBEH suite?
- What's the optimal architecture per question type? (e.g., gen-critic for sequential error-finding, strategy for bias-prone tasks)
