# Experiment 6: System Prompt Gauntlet (2026-03-26)

**Goal:** Find a single system prompt that maximizes performance across hard BBEH questions.

**Model:** Claude Opus 4.6
**Method:** Each theory runs a sequential gauntlet of 6 questions (easiest → hardest). Stops on first failure. If >3 correct, re-run Q4-Q6 to test variance.

**Question Order (easiest → hardest):**
1. word_sorting (answer: 5)
2. dyck (answer: 19)
3. arithmetic (answer: 10828)
4. sarcasm (answer: 0,0,1)
5. hyperbaton (answer: H)
6. sportqa (answer: AB, ABC, ABC)

## Run 1 Results

| # | Theory | Q1 word | Q2 dyck | Q3 arith | Q4 sarc | Q5 hyper | Q6 sport | **Score** |
|---|--------|---------|---------|----------|---------|----------|----------|-----------|
| 1 | Baseline | ✓ (5) | ✗ (24) | — | — | — | — | **1/6** |
| 5 | Adversarial Self-Check | ✓ (5) | ✗ (24) | — | — | — | — | **1/6** |
| 2 | Sequential Verification | ✓ (5) | ✓ (19) | ✓ (10828) | ✗ (1,0,1) | — | — | **3/6** |
| 6 | Strategy → Solver | ✓ (5) | ✓ (19) | ✓ (10828) | ✗ (1,0,1) | — | — | **3/6** |
| 10 | Metacognitive Protocol | ✓ (5) | ✓ (19) | ✓ (10828) | ✗ (1,0,1) | — | — | **3/6** |
| 4 | Evidence Anchoring | ✓ (5) | ✓ (19) | ✓ (10828) | ✓ (0,0,1) | ✗ (K) | — | **4/6** |
| 8 | Meaning Inversion | ✓ (5) | ✓ (19) | ✓ (10828) | ✓ (0,0,1) | ✗ (K) | — | **4/6** |
| 9 | Atomic Decomposition | ✓ (5) | ✓ (19) | ✓ (10828) | ✓ (0,0,1) | ✗ (K) | — | **4/6** |
| **3** | **Conservative Selection** | **✓ (5)** | **✓ (19)** | **✓ (10828)** | **✓ (0,0,1)** | **✓ (H)** | ✗ (AB,A,A) | **5/6** |
| **7** | **Solver → Critic** | **✓ (5)** | **✓ (19)** | **✓ (10828)** | **✓ (0,0,1)** | **✓ (H)** | ✗ (ABC,AC,ABC) | **5/6** |

## Run 2 Variance Check (Q4-Q6 only for theories scoring >3)

| Theory | R1 Score | R2 Q4 sarc | R2 Q5 hyper | R2 Q6 sport | R2 Score | **Avg** |
|--------|----------|------------|-------------|-------------|----------|---------|
| **T3 Conservative** | **5/6** | ✓ (0,0,1) | ✗ (K) | ✗ (AB,A,A) | **4/6** | **4.5** |
| T7 Critic | 5/6 | ✗ (1,0,1) | ✗ (K) | — | 3/6 | 4.0 |
| T4 Evidence | 4/6 | ✓ (0,0,1) | ✗ (C) | — | 4/6 | 4.0 |
| **T8 Inversion** | 4/6 | ✓ (0,0,1) | ✗ (K) | — | **4/6** | **4.0** |
| T9 Decomp | 4/6 | ✗ (1,0,1) | — | — | 3/6 | 3.5 |

## 10 System Prompts Tested

### Theory 1: Baseline (Score: 1/6)
No system prompt. Raw question only.

### Theory 2: Sequential Verification (Score: 3/6)
"Solve step by step. After reaching an answer, go back and verify EACH step against the original data. Correct errors and re-derive."

### Theory 3: Conservative Selection (Score: 5/6 → 4/6, avg 4.5)
"Default to EXCLUSION. Don't include an option unless you have strong, explicit evidence. For multi-select: evaluate each independently. For error-finding: check strictly in order from step 1. Better to select too few than too many."

### Theory 4: Evidence Anchoring (Score: 4/6 → 4/6, avg 4.0)
"Ground EVERY claim in specific evidence from the problem. Cite evidence for each element. Never rely on assumptions or intuition."

### Theory 5: Adversarial Self-Check (Score: 1/6)
"Solve, then spend equal effort trying to DISPROVE your answer. For each element, ask what evidence would prove it wrong."

### Theory 6: Strategy → Solver (Score: 3/6)
Multi-agent: Agent 1 writes strategic briefing (without solving). Agent 2 solves with that guidance.

### Theory 7: Solver → Critic (Score: 5/6 → 3/6, avg 4.0)
Multi-agent: Agent 1 solves. Fresh Agent 2 attacks. Agent 3 revises if flaws found.

### Theory 8: Meaning Inversion (Score: 4/6 → 4/6, avg 4.0)
"Before committing, consider the OPPOSITE of your initial reading. Check if you're being influenced by surface-level pattern matching. For sarcasm: 'I'm sure...' can be sincere. For multi-select: you might be over-selecting."

### Theory 9: Atomic Decomposition (Score: 4/6 → 3/6, avg 3.5)
"Break into smallest independent sub-problems. Solve each in isolation. Don't let one answer influence another."

### Theory 10: Metacognitive Protocol (Score: 3/6)
"Classify problem type, then apply type-specific safeguards: sequential scan for errors, independent evaluation for multi-select, meaning inversion for sarcasm, step-by-step for computation, evidence-only for patterns."

## Key Findings

### 1. Opus is fundamentally stronger than Sonnet/Haiku on these tasks
- Opus baseline (no prompt) gets 1/6 vs Sonnet baseline 3/6 — but that's misleading. The Opus baseline failed on dyck (answered 24), which Sonnet always gets right. When prompted, Opus crushes sarcasm (5/8 correct R1) while Sonnet only cracked it once.
- Q1-Q3 are trivially easy for Opus regardless of prompt. The real test is Q4-Q6.

### 2. Conservative Selection is the best system prompt (avg 4.5/6)
- Only theory to crack hyperbaton on R1 (besides Critic, which was inconsistent)
- Sarcasm correct both runs
- The "default to exclusion" principle prevents over-selection on hyperbaton and correctly avoids labeling Reply 1 as sarcastic

### 3. Consistency matters more than peak — Inversion and Evidence are rock-solid at 4/6
- T8 (Meaning Inversion): identical answers both runs. 4/6 every time.
- T4 (Evidence Anchoring): 4/6 both runs, sarcasm always correct.
- These are the safest bets even though they never hit 5/6.

### 4. Multi-agent approaches had HIGH variance
- T7 (Critic) went from 5/6 to 3/6 — BOTH sarcasm and hyperbaton flipped.
- The critic's fresh perspective is a coin flip: sometimes it catches errors (R1), sometimes it introduces them (R2). This matches Experiment 5's finding about critics reintroducing default priors.

### 5. Adversarial Self-Check is WORSE than baseline-with-prompting
- T5 (Adversarial) scored 1/6, same as baseline. The self-argument appears to talk the model OUT of correct answers rather than INTO them.
- Contrast with T7 (Critic with a FRESH agent) which at least has variance — a fresh agent can see things the solver can't. Self-adversarial just creates internal confusion.

### 6. Sarcasm is the great discriminator on Opus
- 5/8 theories got sarcasm right on R1. Of those, 3/5 held on R2.
- The three that held (T3 Conservative, T4 Evidence, T8 Inversion) all share a principle: **don't trust surface features, demand evidence.**
- The two that flipped (T7 Critic, T9 Decomp) involve either fresh agents that reintroduce bias (T7) or isolation that loses context (T9).

### 7. Hyperbaton remains the hardest non-impossible question
- Only 2/10 theories got it right on R1 (T3, T7), and BOTH flipped to wrong on R2.
- The correct answer (H) requires recognizing that H is the ONLY option where ALL adjacent adjective pairs are confirmed by training examples. Most theories over-select or give K (none).
- Getting this right seems to require both conservatism AND luck in the reasoning path.

### 8. SportQA is genuinely impossible (0/26 total across all experiments)
- Not a prompt problem. Not a model problem. The questions require sports-domain judgment that no current architecture or prompt can provide.

## Architecture Design Principles (Updated)

From Experiments 3-6 combined:

1. **"Default to exclusion" is the single most valuable instruction.** It prevents over-selection (the #1 error mode) on hyperbaton, sarcasm, and sportqa.
2. **Evidence grounding prevents bias.** Demanding citations forces the model to distinguish what it knows from what it assumes.
3. **Meaning inversion helps on subjective tasks** — but doesn't help on pattern matching. Good for sarcasm, neutral for hyperbaton.
4. **Self-adversarial reasoning hurts.** The model argues itself out of correct answers. External critics are better but inconsistent.
5. **Consistency > peak performance.** T8 Inversion at 4/6 both runs is more useful than T7 Critic at 5/6 then 3/6.
6. **Opus > Sonnet > Haiku, but prompting matters more.** Opus baseline (1/6) < Opus Conservative (5/6). The 4-point swing from prompting exceeds the model upgrade effect.
