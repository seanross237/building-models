---
topic: Structure math explorer computation goals as sequential stages where each stage verifies before building
category: methodology
date: 2026-03-27
source: "amplituhedron strategy-001 meta-exploration-006"
---

## Lesson

When designing a math explorer goal involving multiple computation steps, structure the goal explicitly as **sequential stages** where each stage must be verified before the next begins. The typical structure: Stage 1 builds the foundation (spectral model, basis functions, etc.) → Stage 2 uses Stage 1 output to compute the primary observable → Stage 3 applies Stage 2 results to a derived constraint → Stage 4 validates against an independent physical test case.

This is different from sequential computation of two methods (see `sequence-computation-approaches.md`). Here the stages are not alternative methods for the same quantity — they are a pipeline where each stage provides verified building blocks for the next.

## Evidence

- **amplituhedron strategy-001 exploration-006** — The EFT-hedron computation goal used 4 stages: (1) spectral density models (partial waves), (2) forward limit bounds g_{n,0} ≥ 0, (3) Hankel matrix bounds PSD, (4) photon-photon Euler-Heisenberg. Each stage verifies intermediate results before proceeding. The explorer completed all 4 stages in ~20 min, found an unexpected physical insight (non-monotonic saturation ratio), and confirmed analytic formulas to machine precision. Called by meta-note as the "exactly right" structure.

## Why It Works

1. **Independent debuggability**: If Stage 2 fails, the bug is isolated to Stage 2 code, not contaminated by Stage 3. The explorer doesn't spend time diagnosing cascading errors.
2. **Physics sanity checks**: Each stage has a natural physical verification target (non-negativity, normalization, ratio check). Failing one doesn't poison later results.
3. **Incremental reporting**: The explorer writes verified partial results after each stage rather than holding everything until the end.
4. **Unexpected finds emerge naturally**: Stage 3's saturation ratio scan (non-monotonic in M2/M1) was not in the goal — it emerged from having Stage 2 results already verified. With a one-shot goal, the explorer likely would have stopped at "PSD confirmed."

## How to Design Staged Goals

Include a numbered stage list in the goal:

```
Stage 1: Build [foundation component] — verify [physics check].
Stage 2: Using Stage 1 output, compute [primary observable] — verify [analytic/literature check].
Stage 3: Apply [constraint/test] to Stage 2 results — verify [comparison target].
Stage 4: [Independent physical case] — verify [known published result].
```

Make each stage's verification criterion explicit. Common checks: non-negativity of spectral density, convergence of series at small expansion parameter, ratio test against analytic formula, comparison to published numerical value.

## Relationship to Other Patterns

- `sequence-computation-approaches.md` — Sequencing two *methods* for the same quantity (never try simultaneously). Staged goals are about *pipeline stages* that build on each other.
- `specify-computation-parameters.md` — Specify exact parameters within each stage. Staged goals provide the organizational structure.
- `multi-ansatz-sweep-pattern.md` — For parameter sweeps within a stage; often Stage 3 or 4 in a staged goal.

## Extension: Staging Long Synthesis Explorations

The staging principle extends beyond computation pipelines to **long synthesis explorations** (literature survey + claim assessment). A single synthesis exploration covering both "survey all prior work" and "evaluate 4 distinct claims against it" can hit API rate limits mid-exploration, adding 60-90 minutes of delay per interruption.

**Split pattern for synthesis tasks:**
- Part A: Literature survey only — output: "What has been done, exact formulas, specific papers"
- Part B: Claim assessment + synthesis — input: Part A output pasted as context

This mirrors the staged computation structure: each part has a clear input/output boundary, and Part B uses verified Part A output rather than doing its own research.

- **stochastic-electrodynamics strategy-002 exploration-004** — E004 (synthesis exploration: literature survey + 4 claim assessments + fix verdicts + Phase 3 recommendations) hit a rate limit mid-way, requiring a restart nudge and ~90 minute delay. The meta-note recommended splitting: Part A = literature survey only, Part B = claim assessment given Part A output. Total exploration time would have been similar, but without the recovery overhead.

**Also useful:** The staging pattern allows the strategizer to review Part A results before commissioning Part B. If the literature survey finds unexpected prior art that changes the claim assessment framing, Part B can be redesigned accordingly.

## When to Apply

Any math explorer goal that involves: (1) building a model/basis first, then (2) using it to compute primary results, then (3) applying those results to a constraint or test. Common in physics computation: spectral models → dispersion relations → positivity constraints → physical test cases. **Also apply to long synthesis tasks** (survey + assessment) where rate limits are a risk — split into two explorations at the survey/assessment boundary.
