---
topic: Adversarial reviews of parallel explorations need context on ALL completed work
category: goal-design
date: 2026-03-30
source: "vasseur-pressure strategy-002 meta-exploration-s2-007"
---

## Lesson

When launching an adversarial review in parallel with constructive explorations, the reviewer may lack findings from those parallel explorations. This creates a context gap: the adversarial review evaluates an incomplete picture, potentially flagging issues already resolved by parallel work.

## Evidence

**vasseur-pressure S2-E007:** The adversarial reviewer flagged "non-CZ pressure handling incomplete" as a gap in the obstruction result. However, S2-E006 had already been completed in parallel and showed beta = 4/3 is tool-independent (three non-CZ routes tested, all <= 4/3). The adversarial review was launched without E006's findings because both explorations ran simultaneously.

## Protocol

Two mitigation strategies:

1. **Sequential launch (preferred):** Launch adversarial reviews AFTER all constructive explorations in the batch complete. This ensures the reviewer has the full picture. Cost: wall-clock delay of one exploration cycle.

2. **Supplementary context (if parallel is necessary):** Include summaries of parallel work-in-progress as context in the adversarial review GOAL.md. Even partial results ("E006 is testing non-CZ routes; preliminary: IBP gives beta=1, H^1/BMO gives beta=4/3") prevent the reviewer from flagging known-open directions as gaps.

## When to Apply

Any time a strategizer launches an adversarial review alongside constructive explorations in the same batch. Especially important when the adversarial review's scope ("evaluate the COMPLETE picture") overlaps with what the parallel explorations are contributing.

## Distinction from Related Entries

- **adversarial-check-between-phases.md** — Timing of adversarial checks (WHEN to run them); this entry is about CONTEXT when running them in parallel.
- **preload-context-from-prior-work.md** — General context loading; this entry is specifically about parallel-exploration context gaps.
- **adversarial-synthesis-goal-structure.md** — Output format for adversarial reviews; this entry is about input completeness.
