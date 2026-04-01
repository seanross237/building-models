---
topic: Math Explorer for dimensional analysis
category: methodology
date: 2026-03-27
source: "compton-unruh strategy-001 meta-exploration-001"
---

## Lesson

The Math Explorer agent type is an excellent match for dimensional analysis tasks — "is this dimensionally possible?" questions. The combination of scale computation, formula evaluation, and plot generation in a single exploration produces decisive verdicts with clear numerical evidence.

## Evidence

- **compton-unruh strategy-001 exploration 001** — Math Explorer computed all relevant physical scales, performed the matching condition analysis, produced 5 diagnostic plots, and delivered an unambiguous 43-order-of-magnitude discrepancy verdict. The tight scope (four closely related subtasks all serving the same question) kept the exploration focused and productive.

## When to apply

Any exploration where the primary question is whether a proposed physical relationship is dimensionally consistent, whether two quantities can match at a particular scale, or whether a hypothesized effect is numerically plausible. The Math Explorer's ability to compute and plot makes it far superior to a standard explorer for these quantitative assessments.

## Design notes

- Frame the goal as a sequence of related quantitative questions rather than one open-ended analysis
- Ask for explicit numerical tables and comparison ratios
- Request plots that visualize the key discrepancies
- The tight scope guideline (one cognitive task per exploration) is satisfied when all subtasks serve a single quantitative question
