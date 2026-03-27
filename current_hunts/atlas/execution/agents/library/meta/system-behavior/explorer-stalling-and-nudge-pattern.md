---
topic: Explorer stalling and the nudge pattern
category: system-behavior
date: 2026-03-27
source: "strategy-003 meta-s3-002, strategy-003 meta-s3-003, strategy-003 meta-s3-006, strategy-003 meta-s3-007, strategy-004 meta-s4-005"
---

## Lesson

Explorers consistently stall after writing an initial skeleton or partial report (typically 46-107 lines). They enter a "thinking" or "transmuting" phase where they process findings internally without writing. A nudge ("write your findings now") reliably breaks the stall. This pattern appears unavoidable -- it's how the explorer processes complex information.

## Evidence

- **strategy-003 exploration s3-002** — Stalled at 56 lines for ~3 minutes. Nudge got it writing again.
- **strategy-003 exploration s3-003** — Same pattern: 56 lines then ~3 minutes of "transmuting." Better than s3-001 (never writing) but still batch-writes rather than appends.
- **strategy-003 exploration s3-006** — Stalled at 107 lines for ~9 minutes while "thinking with high effort." Nudge resolved it.
- **strategy-003 exploration s3-007** — Stalled at 46 lines (skeleton) for ~4 minutes. Construction tasks may need more patience since the explorer may be genuinely thinking, not just stalled.
- **strategy-004 exploration s4-005** — Explorer printed findings to terminal instead of writing files, requiring a nudge.

- **yang-mills strategy-001 exploration 001** — The report started as a 32-line scaffold and didn't grow for a long time. The explorer was doing web research (not stalling) but this was indistinguishable from stalling by monitoring line count alone. For technical mapping explorations requiring web search, the explorer needs research time before it can write anything meaningful.

## When to apply

Monitor every exploration for the stall pattern. If the report file hasn't grown in 3-5 minutes, nudge. For construction tasks, allow up to 5 minutes before nudging since the explorer may be doing genuine reasoning. **For technical mapping explorations requiring web research, allow extra time (5-10 minutes) — check the tmux pane for search activity rather than relying solely on line count.** Consider adding "write every 3 minutes" instructions to goals, though the nudge-based pattern may be more reliable.
