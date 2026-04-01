# Architecture Automated Exploration — Plan

**Goal:** Discover the best problem categorization (multi-dimensional taxonomy) and the best agent architecture for each problem type. Build a playbook that takes any new problem and outputs the optimal pipeline.

**Location:** All work lives in this folder.

## Phase 1: Question Bank (Round 0)

Collect 50-60 diverse questions across domains. Sources:
- **Science**: Our 14 HLE questions + GPQA Diamond
- **Math**: MATH benchmark hard tier, AMC/AIME competition problems
- **Logic/Reasoning**: BBEH questions (already in repo, minus tennis), BIG-Bench Hard
- **Coding**: Algorithmic problems with deterministic answers

Questions and answers stored separately to prevent agent contamination.

## Phase 2: Baseline Filter (Round 1)

Run Sonnet baseline (no planning, just "solve this") on all questions.
- Passes → tag "easy", record, move on
- Fails → our exploration set for architecture testing

This tells us which questions actually need better architecture.

## Phase 3: Taxonomy Building (Rounds 2-4)

Categorize the hard questions along empirically-validated dimensions. Start with what we already know (discrimination vs computation, knowledge dependency), add dimensions only when data shows they predict different optimal architectures.

Test the router + specialist planner approach across categories.

## Phase 4: Component Testing (Rounds 5-8)

Test architecture components individually and in combination:
- Planning prompts (D2, C1, others)
- Critic / verification loops
- Multi-agent majority vote (separate agents)
- Retrieval-augmented hints
- Model selection (Opus vs Sonnet vs Haiku per step)

Track tokens, speed, and accuracy for every run. Build the cost model alongside the accuracy model.

## Phase 5: Playbook (Rounds 9+)

Synthesize into a decision algorithm:
- Given a new problem → classify → select architecture → execute
- Include model selection (when Haiku is enough, when you need Opus)
- Include cost estimates per pipeline
- Validate on held-out questions

## Principles

- **Use cheap models by default.** Haiku for routing/collection, Sonnet for most experiments, Opus only when testing if it changes outcomes.
- **Baseline filter first.** Don't spend architecture time on problems a single agent solves.
- **Expand questions when helpful,** not upfront. Start moderate and diverse.
- **Track everything.** Every agent run logged with: model, tokens, time, question, architecture, result.
- **Dimensions need evidence.** Don't add taxonomy dimensions without data showing they predict different optimal architectures.
- **Check in every round.** Brief summary of findings, files written, and next steps.

## Prior Work

Findings 1-15 in FINDINGS.md document extensive experiments on 10 HLE questions covering:
- 5 meta-plan strategies (M1-M5) + 4 prompt variants (D1, D2, C1, C2)
- Hybrid vs specialist approaches
- Router architecture
- Plan critique
- Cross-model transfer (Opus plan → Haiku execute)
- Difficulty-adaptive pipelines
- Majority vote (within-agent)

Key prior findings carried forward:
- Specialist prompts beat generalist hybrids
- D2 (adversarial elimination) best for discrimination
- C1 (sign-explicit) best for computation
- Plan variance is the #1 problem
- Plans transfer knowledge across models
- Within-agent majority vote is useless (need separate agents)
- Critique catches ~17% of errors
