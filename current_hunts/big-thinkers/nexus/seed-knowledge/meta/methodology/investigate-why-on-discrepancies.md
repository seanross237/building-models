---
topic: Investigate WHY results disagree with predictions, not just that they do
category: methodology
date: 2026-03-27
source: "stochastic-electrodynamics strategy-001 meta-exploration-004"
---

## Lesson

When simulation results disagree with theoretical predictions, **investigate WHY** rather than just reporting the disagreement. The explanation for the discrepancy often becomes the most interesting finding.

## Evidence

**SED strategy-001 exploration-004:** E003 showed SED Langevin simulation failing at O(β) — one order earlier than Pesquera & Claverie (1982) predicted for the full ALD equation. The original strategy plan only intended to numerically confirm the P-C result. But the strategizer asked: *why does Langevin fail at O(β) instead of O(β²)?*

Following the "why" led directly to the Langevin vs. ALD distinction — **the main finding of the entire SED investigation.** The ALD equation (with Landau-Lifshitz order reduction) eliminates the O(β) failure entirely, confirming P-C's prediction and showing that the O(β) failure was an approximation artifact, not a fundamental SED limitation.

If the team had just reported "Langevin fails at O(β), P-C predicted O(β²), discrepancy noted," they would have missed the central physics.

## Application

- When you have a discrepancy between simulation and theory, make "why does this discrepancy exist?" a priority question, not a note in the limitations section.
- The answer to "why" typically requires understanding the physical mechanism, which is often deeper and more actionable than the discrepancy itself.
- Format as: **state the discrepancy explicitly, then make the mechanism investigation a dedicated exploration** (not a one-sentence remark).

## Related

- `comparison-exploration-pattern.md` — comparing two related approaches is productive; this entry is about following discrepancies within a single approach
- `decisive-negative-pivot.md` — when a result is decisively negative, pivot; this entry is about following the *cause* of a negative result before pivoting
