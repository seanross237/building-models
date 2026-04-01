---
topic: Ask forward-looking literature questions even when confident about state of the art
category: goal-design
date: 2026-03-27
source: "yang-mills strategy-002 meta-exploration-s002-001"
---

## Lesson

Always include "does this combination/result appear in the literature?" as an explicit question in deep extraction explorations — even when you believe you already know the state of the art. Literature in active research areas can advance faster than the library's knowledge, and a forward-looking question is the cheapest way to discover this.

## Evidence

- **yang-mills strategy-002 exploration-001** — The goal asked the standard extraction questions about the SZZ proof technique, but also included a forward-looking question: "does this combination [SZZ + Chatterjee] appear in the literature?" The explorer found arXiv:2509.04688 (Cao-Nissim-Sheffield, Sept 2025), which doubled the SZZ threshold from β < 1/48 to β < 1/24. This was the **single most important finding of the exploration** and came entirely from the forward-looking question. Without it, the library would have continued believing the state of the art was β < 1/48.

## Why It Matters

The strategizer's context about the literature is always frozen at some past date. Explorers can search the web in real time. A single forward-looking question can reveal months of progress in an active field.

## Recommended Phrasing

In deep extraction explorations, add a question like:

> "Does this technique appear in the literature in combination with [related result]? Search for recent (2025–2026) papers that extend or combine these approaches. Has anyone proved [X] using [technique Y] beyond the range we already know about?"

Or more simply:

> "Search for any papers from the past 12 months that extend or build on [SZZ / key result]. What is the most recent bound in the literature?"

## Distinction from Existing Patterns

- **name-specific-authors-and-papers.md** — Targets known papers and authors. This pattern is for discovering *unknown* papers in a rapidly evolving field.
- **specify-temporal-recency.md** — Specifies a time window for the search. This pattern is about the *type* of question (forward-looking combination question), not just the recency filter.
- **prioritize-novelty-assessment.md** — Asks "is our result novel?" after construction. This pattern asks "has someone else already reached our next step?" *before* we assume we're at the frontier.

## When to Apply

Any deep extraction exploration in an active research field where:
- Several groups are working simultaneously
- Results build on each other quickly (months between papers)
- The strategizer suspects "the literature may have advanced since our last survey"

In slower-moving fields or areas where the frontier is well-established, this question is lower-priority. For rapidly progressing fronts (constructive YM, RH, SED), it should be standard.
