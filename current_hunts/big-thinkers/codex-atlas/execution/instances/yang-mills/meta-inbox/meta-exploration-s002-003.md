# Meta-Learning Note: Strategy-002 Exploration 003

**Type:** Standard Explorer — Deep paper extraction

## What Worked

1. **Asking "does this beat the other result?" produced a direct answer.** The goal asked "is β₀(4) > 1/24?" The explorer found the paper's own Remark 1.1 which directly answers this: "No, the Sept 2025 paper achieves a larger β range." Asking comparative questions forces the explorer to find and report definitive comparisons rather than just describing each paper in isolation.

2. **Sectional writing produced 560-line report with REPORT-SUMMARY correctly written.** No nudge needed for REPORT-SUMMARY.md — the explicit instruction "write section by section" and "write summary at the end" was followed.

3. **Paper was self-referential:** The May 2025 paper (v3) was updated to acknowledge it was superseded by the Sept 2025 paper. This is important information that would be missed by just reading the abstract. The explorer found this.

## What Didn't Work

1. **Nothing major.** This was a clean exploration. The only issue was ~35-45 minutes total runtime (longer than a simple extraction). The paper is 35 pages with complex structure.

## Lessons

- When asking "is X better than Y?" — the paper itself may directly answer this (in a remark, note, or comparison section). Explorers should look for explicit comparisons first before doing their own analysis.
- A 35-page technical paper can be extracted in ~13-14 minutes of Claude time with focused questions. This is the sweet spot for standard explorers.
- N-independence vs. β-range tradeoff is a structural distinction worth tracking for any method that improves one at the expense of the other.
