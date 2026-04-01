# Colossus — Mission Plan

## Vision

Build the most capable AI system possible for executing arbitrary tasks, using existing foundation models without training new ones. The system improves itself through knowledge compilation, ensemble reasoning, experience accumulation, and systematic self-optimization.

## Principles

### 1. Measure First
Never optimize what you can't measure. The evaluation harness is the first thing to build and the last thing to compromise on.

### 2. Earn Complexity
Start simple. Add infrastructure only when you hit a concrete wall. The file system is your database until it isn't. A single API call is your architecture until it isn't.

### 3. Iterate on Evidence
Every decision should be informed by data. Run experiments, measure results, then decide. Intuition generates hypotheses. Data makes decisions.

### 4. Know Your Limits
You are built on LLMs. LLMs hallucinate, lose track in long contexts, can't do precise arithmetic, and are unreliable on single passes. Design every component with these limitations in mind. When you find a limitation, build a tool or procedure to compensate.

### 5. Compound Gains
Small improvements that compound are better than large improvements that don't. A 5% gain that applies to every task is worth more than a 50% gain on one task type.

---

## Phase 1: Foundation

**Goal:** Build the minimum infrastructure to run and measure experiments.

### 1.1 Evaluation Harness

Build a system that can:
- Load benchmark tasks (start with subsets of MMLU, MATH, HumanEval, GPQA)
- Run them against a model via the Anthropic API
- Score results (exact match, fuzzy match, LLM-as-judge)
- Store results in structured files
- Compare two configurations with statistical significance

**Success criteria:** Run 200+ benchmark tasks across at least 3 categories, get accuracy within 5% of published baselines.

**Deliverable:** `infrastructure/eval/` with runnable scripts and a README.

### 1.2 Baseline Measurement

Run the base model (Claude Sonnet, single pass, zero scaffolding) against the benchmark suite. This is the floor. Every future improvement is measured against it.

**Success criteria:** Baseline scores recorded in `benchmarks/baseline.md` with per-category breakdown.

### 1.3 Cost Tracking

Build a utility that logs API spend per worker, per experiment, per day. The system needs to know what things cost before it can make smart allocation decisions.

**Success criteria:** After running Phase 1 benchmarks, know exactly what they cost. Report in `benchmarks/baseline-cost.md`.

**Deliverable:** `infrastructure/cost/` with tracking utility.

---

## Phase 2: First Experiments

**Goal:** Determine which improvement axes give the biggest gains, so Phase 3 investment is data-driven.

Run these experiments in parallel once Phase 1 is complete. Each experiment should produce a report in `experiments/` with methodology, results, and conclusions.

### 2.1 Ensemble Scaling
Run the same task N times (N=1,3,5,7) with majority vote. Measure accuracy vs. N across task types.
**Question:** How much does raw repetition buy? Where does it plateau?

### 2.2 Diverse Ensemble
Run N=5 but vary system prompts, reasoning strategies, and temperature. Compare vs. homogeneous ensemble of same size.
**Question:** Does diversity beat repetition at the same cost?

### 2.3 Procedure Injection
Generate 30 task-type-specific procedures ("here's how to approach problems like this"). Inject matching procedure into prompt. Measure lift vs. no procedure.
**Question:** How much does compiled expertise help? Is it worth building the knowledge store?

### 2.4 Verify-and-Retry
For checkable tasks (math, code): generate answer, verify it (run code / check math), retry with error context if wrong. Measure lift for 1, 2, 3 retries.
**Question:** How much does self-correction buy?

### 2.5 Failure Taxonomy
Take all wrong answers from the baseline. Categorize failures: knowledge gap, reasoning error, misunderstood question, calculation error, premature conclusion, etc. Quantify each category.
**Question:** What are the biggest failure modes to target?

**After Phase 2:** The controller must update STATE.md with a summary of results and a revised plan for Phase 3 based on what the data says.

---

## Phase 3: Build What Works

**Goal:** Scale up the approaches that showed the biggest gains in Phase 2.

This phase is deliberately underspecified. The controller designs Phase 3 based on Phase 2 data. Expected activities (pursue based on evidence):

- **If procedures helped:** Launch large-scale knowledge compilation — workers building verified procedures for every identifiable task type.
- **If ensembles helped:** Build a difficulty router — cheap single-pass for easy tasks, full ensemble for hard tasks.
- **If verify-and-retry helped:** Build verification into the default pipeline.
- **If a failure mode dominates:** Build targeted countermeasures (tools, prompts, forced decomposition).

### 3.1 Experience Database
Start logging every task attempt with: task, approach used, result, verification outcome. Build retrieval so the system can find similar past tasks. This compounds over time.

### 3.2 Tool Building
For every identified weakness that can be addressed with code (arithmetic, date math, spatial reasoning, etc.), build a tool. Verify the tool actually helps by measuring before/after.

---

## Phase 4: Self-Improvement Loop

**Goal:** The system continuously identifies weaknesses and builds countermeasures without human intervention.

- Run against benchmarks on a regular schedule
- Analyze new failures, categorize, build fixes
- A/B test system changes automatically
- Red-team: generate hard/adversarial cases to find new weaknesses
- Architecture experiments: test structural changes to routing, ensemble, verification
- Prompt evolution: maintain and evolve prompting strategies per task type

This phase runs indefinitely.

---

## Overall Success Metrics

| Phase | Metric |
|-------|--------|
| 1 | Evaluation harness works. Baseline measured. |
| 2 | Clear signal on which approaches help, with numbers. |
| 3 | System outperforms baseline on every benchmark category. |
| 4 | System continues improving week-over-week without human input. |
| Ultimate | Performance approaching best published results on standard benchmarks, with generality to handle novel task types. |
