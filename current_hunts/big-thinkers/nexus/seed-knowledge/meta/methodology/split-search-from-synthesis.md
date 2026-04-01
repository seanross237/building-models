---
topic: Split iterative literature search and synthesis into two separate explorations
category: methodology
date: 2026-03-27
source: "riemann-hypothesis s002-meta-exploration-008"
---

## Lesson

For explorations that require both (1) iterative literature searches and (2) a structured, synthesized writeup, split into two explorations:

1. **Search exploration** — Mechanical task: run all the searches, write raw results to a dump file as you go. No synthesis required. Just: search → paste what you found → repeat.
2. **Synthesis exploration** — Writing-only task: read the dump file, organize into the required structure, produce REPORT.md. No new searches.

## Why This Works

The failure mode (see `system-behavior/explorer-stalling-and-nudge-pattern.md` — Research-Buffering Stall variant) is systematic: explorers want to complete all research before synthesizing, and by the time they're done with research, writing fails. Splitting the tasks prevents this by:

- Making Task 1 purely mechanical: "search and paste, no synthesis" — there is nothing to buffer
- Making Task 2 purely compositional: "read and write, no searching" — no research phase to complete first

## Evidence

- **riemann-hypothesis S002-E008** — Third consecutive exploration (E006, E007, E008) where the combined search + synthesis pattern produced 0 actual content in REPORT.md after 30 minutes. The meta-note from E008 identified the split as the architectural fix. (Not yet tested — proposed, not confirmed.)

## Contrast with Standard Two-Phase Structure

This is different from the standard Phase 1 / Phase 2 strategy split:
- Phase 1 / Phase 2 = two full explorations tackling different scientific questions
- Search / Synthesis split = two explorations for ONE task that was too long in one pass

## When to Apply

Use this pattern when:
- The goal requires searching ≥3 distinct literature sources/questions
- AND requires synthesizing the results into a structured narrative or verdict table
- AND those two tasks are sequential (search first, then write)

Do NOT use for:
- Single focused literature searches (one topic, one-pass write) — those work fine in one exploration
- Computational goals — use the staged computation pattern (see `staged-computation-goals.md`) instead
- Goals where synthesis requires judgment that depends on what the search finds — splitting may work but the synthesis goal needs to reference the dump file explicitly

## Recommended Structure

**Exploration 1 goal (search):**
> "Run the following literature searches: [list searches]. For each search, write the raw results (title, authors, abstract excerpt, relevance assessment) to `raw-search-results.md`. Write after each search — do not buffer. Target: 150–300 lines."

**Exploration 2 goal (synthesis):**
> "Read `raw-search-results.md`. Synthesize the results into REPORT.md with this structure: [structure]. No new searches needed — all evidence is in the raw results file. Target: 200–400 lines."

## Related Entries

- `system-behavior/explorer-stalling-and-nudge-pattern.md` — the failure mode this pattern avoids
- `goal-design/instruct-incremental-writing.md` — complementary preventive instruction (use in Task 1)
- `methodology/staged-computation-goals.md` — analogous pattern for computation goals
