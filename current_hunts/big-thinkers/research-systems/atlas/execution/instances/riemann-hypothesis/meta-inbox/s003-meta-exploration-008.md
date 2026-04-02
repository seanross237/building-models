# Meta-Learning Note: Exploration 008

**Date:** 2026-03-28
**Strategy:** strategy-003, Riemann Hypothesis
**Explorer type:** Math (Opus)
**Goal:** Validate λ_n^zeta/λ_n^GUE crossover with 5000 zeros + larger GUE

## What Worked

- **CWD check as Task 0**: Worked perfectly again. Explorer confirmed directory and loaded E002 cached data immediately.
- **Incremental writing**: With explicit "write after EACH task" instructions and CWD check first, explorer wrote 4 task sections before context pressure.
- **Error correction**: Explorer independently discovered and corrected GOAL.md's wrong reference value (λ_100^zeta = 59.72 was wrong; actual = 114.18). This is the kind of sanity check Math Explorers excel at.
- **Truncation analysis**: Explorer added a non-planned task (truncation analysis) that turned out to be the most important finding. Task scope was broader than needed for the specific question.

## What Didn't Work

- **Context pressure at ~52 minutes**: Explorer showed "Envisioning (52m 27s)" with 12.2k tokens and the context limit warning. Had to emergency-nudge to write REPORT-SUMMARY.md before running out of context.
- **K=N=5000 matched test incomplete**: The computation that would have definitively settled the question (5000×5000 GUE) was running at cutoff. Explorer prioritized replication and truncation analysis over the primary comparison goal.
- **Scope too wide**: The explorer ran 4 separate computation paths (replication, truncation analysis, N-dependence, matched K=N test) when only the last 2 were needed. Should have scoped to just: "compute ratio at K=N=500, 1000, 2000, 3000, 5000."

## Key Lesson

**For computationally intensive explorations: specify the MINIMUM computation needed.** "Compute the ratio at K=N=500, 1000, 2000, 3000, 5000 and extrapolate" is better than "validate with 5000 zeros and N=300 GUE" because the explorer will run all available approaches instead of the one diagnostic test needed.

Also: when a Math Explorer is approaching context limits (12k+ tokens), immediate emergency nudge is needed. The 7-minute polling interval should be shortened to 5 minutes for Math Explorer sessions running >45 minutes.

## Unexpected Finding

Explorer discovered that E002's GUE setup was N=2000 (not N=100 as GOAL.md stated), which completely changes the interpretation of the original finding. Always have the Math Explorer re-read and replicate from source data, not from strategizer's summaries.
