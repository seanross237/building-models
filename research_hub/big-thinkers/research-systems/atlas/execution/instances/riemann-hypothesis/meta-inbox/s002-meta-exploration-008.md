# Meta-Learning Note — S002 Exploration 008

**What worked:**
- The GOAL.md was well-structured: three explicit tasks with clear paper-format writeup template.
- Having exact claim language written out in the goal (numbers, construction, literature context pointers) gave the explorer everything it needed.
- The instruction to search specific reviewers (Schumayer-Hutchinson, Sierra-Rodriguez-Laguna) was more efficient than open-ended keyword searches.

**What didn't work:**
- Same pattern as E006, E007: explorer wrote a full skeleton with [SEARCHING...] placeholders, ran multiple web searches, but never wrote results into the skeleton. After ~30 minutes REPORT.md had 0 actual search results in it despite the explorer completing all the searches.
- The explorer ran 8+ web search iterations but none of the content made it into the file. It was apparently buffering everything for a final write that never happened.
- This is now the THIRD consecutive exploration with this pattern. It's not explorer-specific — it's a systematic failure mode for explorations involving iterative research + final writeup.

**Lessons:**
- **The incremental writing instruction doesn't prevent buffering.** Even with "WRITE INCREMENTALLY — fill in each section as you finish it" in the goal, the explorer still buffered. The problem may be that LLM explorers naturally want to complete all research before synthesizing, and that delay + the context size by end makes writing fail.
- **The correct pattern is: kill after 30 min stagnation, extract results from conversation history, manually write.** For E008, the strategizer used the Agent tool to do the literature searches directly, then manually wrote REPORT.md and REPORT-SUMMARY.md. This took ~15 minutes total and was more reliable than waiting for the explorer.
- **For pure literature synthesis tasks**: Consider having the standard explorer only write REPORT-SUMMARY.md (not the full REPORT.md). The summary is the thing that's actually needed; the full report is just detail capture.
- **Alternative strategy**: Split literature synthesis into two explorations: (1) run the searches and produce a raw data dump, (2) synthesize the dump into a structured report. The first task is mechanical (just write what you find), the second is writing-only (no new searches). This might prevent the buffering problem.

**Science lesson:**
- Neither N²/p scaling nor Dirichlet impossibility has prior literature. The searches were genuinely productive — the gap is real. This gives the two claims SUPPORTED status.
- The adversarial review pattern (E007) was the right call — it correctly downgraded the pair correlation claim before E008 finalized verdicts.

**Scope:**
- One exploration for final synthesis + 2 literature searches + 3 claim writeups was the right scope. All three tasks are tightly coupled (literature context directly feeds the claim writeup).

**One thing to try next time:**
- In the goal for a synthesis exploration, add: "At the END of EVERY section, write a [SECTION COMPLETE] marker to REPORT.md before starting the next section. If you cannot write the section, write [SECTION FAILED: reason]. Do NOT buffer sections for a final write."
