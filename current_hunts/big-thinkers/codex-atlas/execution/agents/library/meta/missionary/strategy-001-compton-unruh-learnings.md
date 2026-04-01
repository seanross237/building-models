---
topic: Adversarial Derivation Protocol for hypothesis-testing missions
category: missionary
date: 2026-03-27
source: compton-unruh, strategy-001
---

# Strategy-001 Learnings: Compton-Unruh Resonance

## Methodology: Adversarial Derivation Protocol

Prescribed a three-phase protocol: (1) Framework & Feasibility — dimensional analysis + no-go search, (2) Calculation & Prediction — compute key equations + generate numbers, (3) Distinctness & Stress Testing — compare with prior work + adversarial test. Core principle: "derive, then immediately try to kill what you derived."

## What Worked

### Dimensional analysis as Phase 1 gatekeeper was the best decision

The very first exploration killed the original hypothesis by 43 orders of magnitude. Without this, the strategy would have spent 7 explorations building on a dimensionally impossible foundation. **Lesson: For any hypothesis-testing mission, mandate dimensional analysis / feasibility check as exploration 001.** This is cheap (one math exploration) and can save the entire budget if the hypothesis is dead.

### Math explorers for computation were 4/4

Every math exploration succeeded and delivered clean, verifiable results (symbolic verification with Sympy, numerical checks with Python). The strategy's emphasis on "compute, don't argue" worked: the FDT closure (χ''_dS = χ''_flat exactly) and the free-fall resolution (Λ cancels identically) were both decisive because they were calculated, not argued.

### Parallel exploration pairs were efficient

The strategizer effectively paired explorations: (001 dimensional analysis + 002 literature survey), (005 novelty search + 006 FDT mechanism), (007 free-fall + 008 adversarial). This doubled throughput when tasks were independent. **Lesson: Parallel pairs work well when the two tasks are genuinely independent — don't pair things where one result should inform the other.**

### The pivot was handled well

When exploration 001 killed the original hypothesis, the strategizer pivoted to the de Sitter crossover — the one feature at the right scale. This was a natural pivot (identified by the same exploration) and led to the most interesting finding (T_U/T_dS identity). **Lesson: Design explorations that identify their own successor directions. Ask "what IS at the right scale?" not just "is THIS at the right scale?"**

## What I'd Change

### Run the adversarial test MUCH earlier

The adversarial stress test (exploration 008) found a fatal flaw — Bullet Cluster lensing — that was a *standard test*. This should have been exploration 003 or 004, not 008. Seven constructive explorations built on the T_U/T_dS identity before discovering it was falsified. The modified-inertia-doesn't-modify-lensing objection is well-known in the field. **Lesson: In the methodology, mandate an adversarial/falsification exploration no later than the third or fourth slot. Don't wait until Phase 3. Phrase it as: "What is the single strongest observational test that could kill this? Run it now."**

### The 1/(2π) investigation was predictable wasted time

The strategizer sent exploration 007 to derive the factor of 1/(2π) from the T_U/T_dS ratio. This was algebraically doomed: 2π appears identically in both T_U and T_dS and cancels in the ratio. A 30-second algebra check would have caught this. **Lesson: In the methodology, add a pre-launch algebra/dimensional check: "Before launching an exploration, verify that the question isn't trivially answerable. If the answer follows from the formula's structure in 5 minutes of algebra, don't spend an exploration on it."**

### Context contamination in parallel launches

Exploration 002 worked on the wrong mission (classicality-budget). The explorer picked up context from another mission's files. The strategizer fixed this by being more explicit in subsequent prompts. **Lesson: When launching parallel explorers, include the mission name, topic, and working directory explicitly in the prompt. Don't rely on implicit context from directory structure alone.**

## Surprising Observations

### The most interesting finding was a side-effect of the pivot

The T_U/T_dS = μ_MOND identity was not what the mission was looking for. It emerged from investigating the de Sitter crossover as a salvage route after the original hypothesis died. **Lesson: Don't design strategies that only succeed if the original hypothesis is confirmed. The most interesting findings often emerge from exploring why something DOESN'T work.**

### The strategizer self-corrected well

After exploration 002 failed, the strategizer diagnosed the cause (context contamination) and fixed it. After the adversarial test, it honestly noted "should have run this earlier." The REASONING.md log shows genuine adaptation. **Lesson: The "Adversarial Derivation Protocol" name might have influenced the strategizer to take adversarial testing seriously — naming the methodology matters.**

### One strategy was sufficient for this mission

8 explorations (6 successful, 1 failed, 1 adversarial) reached all 5 validation tiers. The mission asked a yes/no question (does the resonance modify inertia?) and got a decisive no. **Lesson: For hypothesis-testing missions with clear falsification criteria, one well-designed strategy can be enough. Don't plan for multiple strategies if the question has a binary answer.**

## Generalizable Lessons

1. **Dimensional analysis first.** Always. For any quantitative hypothesis.
2. **Adversarial tests early, not late.** Run the strongest falsification test as soon as there's something to falsify. Don't build for 7 explorations before stress-testing.
3. **Pre-launch algebra check.** If the question is trivially answerable from the formula's structure, answer it before spending an exploration.
4. **"Compute, don't argue" works.** Math explorers with symbolic+numerical verification produce the cleanest results.
5. **Side-effects of failures are valuable.** Design the methodology to capture and follow up on unexpected findings from failed hypotheses.
6. **Name the methodology.** "Adversarial Derivation Protocol" may have influenced the strategizer to actually be adversarial.
