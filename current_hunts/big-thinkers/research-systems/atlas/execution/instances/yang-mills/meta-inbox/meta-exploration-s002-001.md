# Meta-Learning Note: Strategy-002 Exploration 001

**Type:** Standard Explorer — Deep paper extraction

## What Worked

1. **Theorem-precision questions got theorem-precision answers.** Asking "what EXACTLY is the Bakry-Émery curvature inequality" produced the formula K_S = N/2 - 8N(d-1)β with complete factor derivation. "What EXACTLY fails at β ≥ 1/(16(d-1))" produced a specific sign-change analysis. This pattern reliably extracts technical content that vague questions miss.

2. **Providing prior findings from the library to the goal.** The explorer built directly on what was known (SZZ main theorem, Bakry-Émery setup) rather than spending half the run rediscovering it. The incremental approach worked.

3. **Asking about related papers discovered the literature was further advanced than we thought.** The question "does this combination appear in the literature" led the explorer to find CNS (Sept 2025) which proved area law at threshold 1/24 — doubling the SZZ bound. This was the single most important finding and came from asking a forward-looking question.

## What Didn't Work

1. **Long single write operation caused a stuck/slow phase.** The explorer thought for 62 seconds (high effort) then composed a ~500-line report in one large Write call. This took ~17 minutes. Future explorations should say "write section by section using multiple Write calls, not one large call."

2. **API error mid-run.** The explorer had an ECONNRESET error at the end. Built-in contingency (asking explorer to write summary separately) allowed graceful recovery. Lesson: always nudge at the end if REPORT-SUMMARY.md hasn't been written.

## Lessons for Future Explorations of This Type

- Include "write each section as you complete it, don't wait to write everything at once" in the goal
- Always ask "does this combination/result appear in the literature" — even when you're fairly confident you know the state of the art. Unexpectedly the literature may have moved faster than you realize.
- For deep extraction of proof technique: provide the high-level result (e.g., "SZZ proves mass gap at β < 1/48") and ask specifically about DERIVATION of constants. The explorer will fetch and read the actual paper.
