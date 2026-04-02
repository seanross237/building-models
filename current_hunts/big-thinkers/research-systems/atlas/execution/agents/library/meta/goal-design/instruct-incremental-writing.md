---
topic: Instruct incremental writing in GOAL.md to prevent large-write stalls
category: goal-design
date: 2026-03-28
source: "amplituhedron strategy-001 meta-exploration-001, stochastic-electrodynamics strategy-001 meta-exploration-001, amplituhedron strategy-001 meta-exploration-006, yang-mills strategy-002 meta-exploration-s002-001, riemann-hypothesis s002-meta-exploration-007, riemann-hypothesis s002-meta-exploration-008, riemann-hypothesis s003-meta-exploration-002, riemann-hypothesis s003-meta-exploration-003, riemann-hypothesis s003-meta-exploration-004, riemann-hypothesis s003-meta-exploration-007, thermal-time s003-meta-exploration-002, riemann-hypothesis s003-meta-exploration-009"
---

## Lesson

Include explicit instruction to write section by section in GOAL.md. Without it, explorers attempt to compose the entire report in a single large write operation and stall for several minutes before the write succeeds (or times out). Saying "write section by section, not all at once" prevents this.

## Evidence

- **amplituhedron strategy-001 exploration-001** — Explorer got stuck for ~5 minutes attempting to write the entire report in one large write operation. The REPORT.md sat at 33 lines (skeleton) for a long time. Nudge to "write incrementally, section by section" immediately unstuck it. The explorer then wrote full content section by section without further stalls.
- **stochastic-electrodynamics strategy-001 exploration-001** — Same pattern observed independently: explorer got stuck for ~5 minutes trying to write the entire report in one large write operation; initial REPORT.md was a 33-line skeleton. The nudge to write incrementally immediately unstuck it. This is a second independent confirmation across a different domain and mission.

## Relationship to Stalling Pattern

The existing stalling pattern (see system-behavior/explorer-stalling-and-nudge-pattern.md) documents the nudge as the reliable reactive fix. This entry is the **preventive** version: include the instruction in the goal so the stall doesn't happen in the first place.

The two approaches are complementary:
- **GOAL.md instruction**: "Write section by section. After completing each major section, write what you have to the report before continuing."
- **Runtime nudge**: Fallback when the explorer stalls despite the instruction.

## Recommended Instruction Text

Add to GOAL.md (e.g., in a "Format" or "Instructions" section):

> Write the report incrementally — complete each section and write it to the file before moving on to the next. Do not attempt to write the entire report in one pass.

## When to Apply

Any exploration expected to produce a structured multi-section report (150+ lines). Especially important for catalog/survey tasks (where the explorer naturally tries to gather all material first, then write it all at once) and for computation-heavy explorations (where results pile up before writing).

## Third Confirmation

- **amplituhedron strategy-001 exploration-006** — Despite having the incremental writing instruction in the goal, the explorer still wrote the report at the end: REPORT.md sat at 81 lines (initial skeleton) and then jumped to 433 lines at completion. No intermediate writes. Suggests the instruction alone is insufficient for computation-heavy tasks where the natural workflow is: run all stages → write everything at end. **Recommendation**: for staged computation goals, explicitly tie each write to its stage: "After completing Stage 2, write the Stage 2 section to the report before proceeding to Stage 3."

## Fourth Confirmation

- **yang-mills strategy-002 exploration-001** — Explorer composed a ~500-line report in one large Write call. This took approximately 17 minutes (62-second high-effort thinking phase followed by a single massive write). The goal did not include an incremental writing instruction. Adding "write each section as you complete it" to the goal would have distributed the write time across the exploration and prevented this terminal stall pattern.

## Fifth Confirmation — Tie Writes to Computation Sections Explicitly

- **riemann-hypothesis strategy-002 exploration-007** — Adversarial exploration with three distinct tests (null matrix comparison, 20-realization stability, severity table). The explorer ran all three tests, saved results to `results.npz`, then entered a 30-minute thinking loop without writing any section. REPORT.md was stuck in all-placeholder state. Required manual intervention to complete.

**New specificity:** For multi-test or multi-stage goals, the instruction must be section-specific, not just general. The effective form is:

> "WRITE RESULTS INCREMENTALLY. After running Test 1, append the Test 1 results table to REPORT.md Test 1 section before proceeding to Test 2. After running Test 2, fill in the Test 2 section before proceeding to Test 3. Do NOT buffer all results for the end."

This is more effective than "write section by section" because it explicitly chains each write event to a computation checkpoint, leaving no ambiguity about when writing should occur.

**Threshold:** If REPORT.md hasn't grown after >15 minutes post-computation (all data saved), the explorer is in a deep thinking loop that will not self-resolve. At that point, manual intervention (kill + complete) is more reliable than a nudge.

## Sixth Confirmation — Research Buffering Is Systematically Unpreventable

- **riemann-hypothesis strategy-002 exploration-008** — Third consecutive exploration (E006, E007, E008) with the same pattern: explorer wrote a full skeleton with [SEARCHING...] placeholders, ran 8+ web search iterations, but none of the content made it into the file. The goal included "WRITE INCREMENTALLY — fill in each section as you finish it." Despite this, the explorer buffered all results for a final write that never happened. REPORT.md had 0 actual search results after ~30 minutes of searching.

**Key new observation:** This is NOT explorer-specific and NOT prevented by the incremental writing instruction. The pattern is **systematic for iterative research + final writeup explorations**. The LLM explorer naturally wants to complete all research before synthesizing, and by the time it's done, context size + complexity makes writing fail.

**Most reliable fix for this pattern:** Kill the exploration after ~30 minutes of stagnation, extract results from conversation history, and write the report manually. For E008, this took ~15 minutes total — faster than waiting for the explorer.

**New variant — Section Completion Markers:** Adding a [SECTION COMPLETE] marker instruction may help. Try:
> "At the END of every section, write `[SECTION COMPLETE]` to REPORT.md before starting the next section. If you cannot complete the section, write `[SECTION FAILED: reason]`. Do NOT buffer sections for a final write."

The explicit marker creates a binary checkpoint that's harder for the explorer to skip than a general "write incrementally" instruction.

**New mitigation — Reduce scope for pure synthesis:** For pure literature synthesis tasks (search + writeup, no computation), consider requiring only REPORT-SUMMARY.md rather than full REPORT.md. The summary is the actionable output; the full report is detail capture that may never materialize. This avoids the failure mode entirely by reducing the writing commitment.

**See also:** `meta/methodology/split-search-from-synthesis.md` — the architectural fix: split search (produce raw dump) and synthesis (structured report) into two separate explorations.

## Seventh Confirmation — Literature Search Deadline Nudge with [INCOMPLETE] Markers

- **riemann-hypothesis strategy-003 exploration-007** — Adversarial novelty review with multiple literature searches. The explorer stalled for ~45 minutes doing web research without writing anything. The goal included [SECTION COMPLETE] markers but the explorer ignored them, buffering all results. A "STOP RESEARCHING. Write your findings NOW" nudge broke the stall and produced 141 lines. A second, very specific nudge ("5-8 bullet points, YES/NO/UNCLEAR, write REPORT-SUMMARY.md immediately") was needed to produce the final summary. **Planning assumption for web research explorations: first write will happen after ~45 minutes, not 5 minutes.**

**New preventive instruction for literature search goals:** Add an explicit deadline nudge directly into GOAL.md:

> "If you have been searching for more than 20 minutes without writing, STOP and write a partial section with [INCOMPLETE] markers. Do not run 10 web searches in a row without writing. After each major search batch (2-3 searches), write what you found so far."

This combines the [SECTION COMPLETE] markers with a time-based trigger and the [INCOMPLETE] permission — telling the explorer it's OK to write partial results rather than waiting for completeness. The key is giving explicit permission to write incomplete sections; without this, the explorer's natural instinct is to complete all research first.

**Distinction from research-buffering architectural fix:** The split-search-from-synthesis pattern (see `meta/methodology/split-search-from-synthesis.md`) is the stronger fix but requires two explorations. This deadline-nudge instruction is a lighter-weight alternative for goals where splitting is overkill (e.g., 2-3 literature searches, not 8+).

## Eighth Confirmation — [SECTION COMPLETE] Markers Insufficient for Computation-Heavy Explorations

- **riemann-hypothesis strategy-003 exploration-002** — The goal included [SECTION COMPLETE] markers and the explorer did use them, but the REPORT.md stayed at 33 lines (skeleton) for ~20 minutes while the explorer ran multiple analyses (FFT, GUE comparison, spectral rigidity). The report was written almost entirely at the end in one pass, not section-by-section. Despite computation completing quickly (~80s for all 500 Li coefficients after zero pre-computation), the explorer ran additional analyses before updating the report.

**New nuance:** The [SECTION COMPLETE] marker works as a *progress tracking* mechanism (sections get marked), but does not force *intermediate report writes*. Even when sections are initially placeholders, the explorer fills them all in one final pass. The effective instruction must be stronger: "After EACH task completes its computation, write results to REPORT.md BEFORE starting the next task." The emphasis on temporal ordering (write, then proceed) is critical — the marker only labels completion, it doesn't force the write-first pattern.

## Eighth Confirmation — Incremental Writing Works When Explorer Follows It

- **riemann-hypothesis strategy-003 exploration-003** — Positive example: Tasks 0, 1, 2, and 4 each got their own REPORT.md section with results tables. The explorer wrote each section before moving to the next computation. This is the write-then-proceed temporal ordering working as intended. However, the explorer still stalled for 3.5 hours between Tasks 1 and 2 (see system-behavior/explorer-stalling-and-nudge-pattern.md) — the incremental writing instruction prevents the *write* stall but does not prevent the *computation initiation* stall. When the explorer DID start each task, results were written correctly and incrementally.

## Ninth Confirmation — Row-Level Writing for Parameter Sweeps

- **riemann-hypothesis strategy-003 exploration-004** — The explorer ran N=250 and N=1000 prime sweeps (26 and 19 primes respectively). Computation happened — tmux pane showed results like "N=250 p=211 N2/p=296.2 beta_W=1.1124" — but REPORT.md was not updated during computation. The explorer computed all results, buffered them, then deferred writing until post-computation thinking. This is the computation-buffering stall in its extreme form: the explorer has all results but doesn't write them.

**New granularity requirement for parameter sweeps:** Section-level incremental writing is insufficient when each section involves a sweep across many parameter values. The instruction must go to **row level**: "After EACH prime p is tested, write one row to the results table in REPORT.md immediately. Do not wait until the sweep is complete." This prevents the buffer-then-think pattern for sweep explorations.

**Template for sweep goals:**
> "After computing β for each prime p, immediately append one row `| p | N²/p | β_W | β_B |` to the results table in REPORT.md. Do not accumulate results in memory — write each row as you compute it."

## Tenth Confirmation — Adversarial Per-Claim Checkpoint for Multi-Claim Reviews

- **thermal-time strategy-003 exploration-002** — Adversarial review of 5 TTH claims with prior art search, 3 conceptual attacks, and null hypothesis tests. The explorer fetched ~20 papers before writing anything; the report stayed at 69 lines for over an hour. A nudge was needed to trigger writing. Despite the GOAL saying "write incrementally," the explorer accumulated all research first.

**New variant for adversarial explorations:** Mandate a per-claim checkpoint: "After completing the prior art search for each claim, write that claim's section to REPORT.md before moving to the next claim." This prevents the accumulation problem specifically for adversarial reviews, where the natural workflow is: search all → organize all → write all. The per-claim checkpoint forces: search Claim 1 → write Claim 1 → search Claim 2 → write Claim 2 → ...

**Template for adversarial per-claim checkpoints:**
> "For each claim: (1) complete prior art search, (2) write that claim's prior art assessment to REPORT.md including verdict and novelty rating, (3) move to the next claim. Do NOT accumulate all prior art searches before writing."

## Eleventh Confirmation — Write-During-Long-Computation Pattern

- **riemann-hypothesis strategy-003 exploration-009** — The K=N=5000 GUE computation (15 trials of 5000×5000 matrices) took ~20 minutes. The explorer wrote REPORT.md up to "K=N=5000 running..." and then stopped adding content until the computation finished. By then, context pressure hit (7.4k tokens at 33 min) and the explorer could not complete the report without an emergency nudge.

**New instruction for computations >15 minutes:** Include in GOAL.md:

> "If any computation will take more than 15 minutes, submit it as a background job. While it runs, write the REPORT.md with all results you already have. Note which results are pending. When the background job completes, append those results."

The key insight: **decouple writing from computation**. The explorer's natural behavior is to block on the computation and then write — but if the computation is long, context pressure may prevent the write from ever happening. Writing intermediate results first preserves them regardless of what happens to the computation.

**Distinct from row-level/section-level variants:** Those address the sequencing of write vs. compute for *serial* tasks. This addresses the *concurrent* case: a single very long computation where the explorer has partial results from earlier (shorter) computations and should write those while the long one runs.
