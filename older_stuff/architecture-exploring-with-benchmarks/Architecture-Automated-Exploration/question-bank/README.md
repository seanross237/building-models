# Question Bank

## Structure

```
question-bank/
  questions/           — Question files, NO answers
    science-hle.md     — 14 expert-level science (HLE)
    logic-bbeh.md      — 22 hard reasoning (BBEH, excl. tennis)
    math.md            — Competition/research math
    coding.md          — Algorithmic reasoning
  answers/
    answer-key.md      — All answers, NEVER give to agents
  baseline-results.md  — Round 1 Sonnet baseline scores
```

## Anti-Contamination Protocol

Questions and answers are in SEPARATE files. When running agent experiments:
- Only pass question files to agents
- NEVER include answer-key.md in agent context
- Validate answers by reading the key yourself, not by asking the agent

## Question ID Format

- `SCI-NN` — Science (HLE)
- `LOGIC-NN` — Logic/Reasoning (BBEH)
- `MATH-NN` — Math (competition/research)
- `CODE-NN` — Coding/Algorithms

## Difficulty Target

All questions should be hard enough to stump frontier models with a naive single-shot approach. The point is to find problems where architecture (planning, critics, multi-agent, retrieval) makes a measurable difference.

## Flagged Questions

- LOGIC-02 (boardgame): Answer listed as "unknown" — needs manual verification
- LOGIC-18 (time_arithmetic): Answer is empty list [] — verify correctness
