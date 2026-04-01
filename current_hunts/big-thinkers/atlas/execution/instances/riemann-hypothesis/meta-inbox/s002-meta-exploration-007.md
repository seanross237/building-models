# Meta-Learning Note — S002 Exploration 007

**What worked:**
- The adversarial test structure was well-designed: three independent tests (null comparison, stability, severity) gave a comprehensive attack. The specific code target (adversarial_test.py) and data format (results.npz) worked well.
- Pre-loading the scipy fallback formula directly in the GOAL.md prevented the scipy ImportError from blocking the computation.
- The instruction to compute 20 realizations for stability gave a clear, quantitative stability result.
- Providing exact pair correlation formulas prevented normalization issues.

**What didn't work:**
- Same pattern as E006: explorer computed results, saved to npz, then got stuck in an extended thinking loop without writing the report. REPORT.md was filled with placeholder sections but never updated with actual data.
- The deep thinking phase after computation appears to be a systematic pattern in this mission. The explorer writes the code skeleton, runs it, saves results, but then can't proceed from the thinking phase to the writing phase.

**Lessons:**
- **Instruct incremental writing pattern**: Tell the explorer to write each result section immediately after computing it, not at the end. Example: "After running Test 1, append results to REPORT.md Test 1 section before moving to Test 2." This prevents the report from being stuck in all-placeholder state.
- **Set explicit section-completion checkpoints**: "For each test section in REPORT.md, fill it in with numbers immediately after the code runs. Do NOT defer all writing to the end."
- **The 30-minute deep-thinking-without-writing pattern requires manual intervention.** If REPORT.md hasn't grown after >15 minutes post-computation, the strategizer should kill and manually complete.

**Science lesson:**
- The adversarial test revealed that pair correlation MRD at N=500 with 5-realization averaging is not a discriminating test — GOE-class matrices also pass. The most useful contribution of E007 was quantifying HOW much averaging is needed and what the per-realization noise looks like (15.5% mean).

**Scope:**
- Three tests was the right scope. Could have been separate explorations but they're tightly coupled (all testing the same claim).

**One thing to try next time:**
- In the goal, add: "WRITE RESULTS INCREMENTALLY. After each test, append the results table to REPORT.md immediately. Do not buffer all results for the end."
