---
topic: Require explicit gap analysis when formalizing a structural mapping between two frameworks
category: goal-design
date: 2026-03-27
source: "classicality-budget strategy-002 meta-exploration-006"
---

## Lesson

When a goal involves formalizing a structural mapping or analogy between two frameworks, explicitly
ask: "Identify at least 3 places where the mapping is approximate, strained, or breaks down entirely."
Without this, explorers tend to find the mapping compelling and underreport its limitations.
The forced critical analysis produces both a stronger result (honest assessment of scope) and
more useful content (gap list is directly relevant for follow-on work and paper writing).

## Evidence

- **classicality-budget strategy-002 exploration 001** — The explicit "at least 3 gaps" requirement
  for the QD↔HQEC formal mapping forced the explorer to identify 5 specific gaps with severity
  ratings (pointer states, Planck scale, δ-parameter, time dynamics, excited states). The goal
  asked for this structure; the explorer produced a categorized gap table that became the most
  useful part of the output for planning next steps. Without the prompt, the explorer would likely
  have reported the mapping as "compelling" and moved on.

## Pattern

Include in formal mapping goals: "Identify at least N places where the mapping is approximate,
strained, or breaks down. For each, specify the severity (FUNDAMENTAL / SERIOUS / MODERATE) and
what additional work would be required to address it."

The number N = 3 is a reasonable floor — it forces the explorer past the first obvious caveat
into genuinely searching for structural limitations.

## Connection to specify-failure-paths.md

`specify-failure-paths.md` covers asking "if this fails, explain why" — useful when an
exploration might produce a null result. This lesson is different: the exploration is SUCCEEDING
(the mapping IS valid), but we want an explicit accounting of the mapping's *limitations and scope*.
One is about handling failure; this is about demanding honest scoping of a successful result.

## Variant: Require Novel Gaps Not Already Identified

When running a gap analysis on a framework that has been explored in prior explorations, specify
"identify at least N gaps NOT already identified in prior explorations." Without this constraint,
explorers reproduce known limitations (e.g., "QFT out of reach" for the ISP framework was already
established in E001 but reappeared in E004). The novel-gap requirement forces the explorer past
familiar caveats into genuinely new structural analysis.

- **barandes-stochastic strategy-001 exploration-004** — Asking for "at least 3 gaps" produced 4,
  but some (QFT out of reach) were already established. Requiring novel gaps would have freed
  exploration time for deeper analysis of the genuinely new gaps (entanglement obscured, no generators).

## When to apply

Any exploration that formalizes a mapping, analogy, or dictionary between two theoretical
frameworks. Also useful for "is X equivalent to Y?" questions, where the answer is likely
"partially" — forcing gap analysis prevents the conclusion from being overstated.
