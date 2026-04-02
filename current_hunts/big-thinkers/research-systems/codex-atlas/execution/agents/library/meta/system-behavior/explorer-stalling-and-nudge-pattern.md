---
topic: Explorer stalling and the nudge pattern
category: system-behavior
date: 2026-03-28
source: "strategy-003 meta-s3-002, strategy-003 meta-s3-003, strategy-003 meta-s3-006, strategy-003 meta-s3-007, strategy-004 meta-s4-005, yang-mills strategy-001 meta-exploration-005, classicality-budget strategy-001 meta-exploration-004, classicality-budget strategy-001 meta-exploration-005, yang-mills strategy-002 meta-exploration-s002-002, riemann-hypothesis s002-meta-exploration-006, riemann-hypothesis s002-meta-exploration-007, yang-mills strategy-002 meta-exploration-s002-005, riemann-hypothesis s002-meta-exploration-008, riemann-hypothesis s003-meta-exploration-003, riemann-hypothesis s003-meta-exploration-004, riemann-hypothesis s003-meta-exploration-007, riemann-hypothesis s003-meta-exploration-009, yang-mills s003-meta-exploration-002, yang-mills s003-meta-exploration-003, yang-mills s003-meta-exploration-s003-006, yang-mills-conjecture meta-exploration-008"
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

## Variant: 0% Stall (No Output at All)

A distinct pattern from the mid-report stall: the explorer produces **nothing at all** for 3-5+ minutes at the start of the exploration. The report file may exist but sit at 0 lines (or just a skeleton header). This differs from the large-write stall (explorer is writing internally) — here the explorer appears stuck before producing any output.

- **classicality-budget strategy-001 exploration 003** — Stuck at 0% for 4+ minutes, needed a nudge.
- **classicality-budget strategy-001 exploration 004** — Same pattern: 0% for 4+ minutes before nudge. The goal was long and complex (5-objection stress-test format with detailed instructions).
- **classicality-budget strategy-001 exploration 005** — Also needed a nudge to start (same 0% stall pattern).
- **stochastic-electrodynamics strategy-001 exploration-002** — Math Explorer was idle for 8-10 minutes before first output on a coupled-oscillator simulation task. Consistent with the pattern that Math Explorers take longer before first output on computational/simulation goals than Standard Explorers.

**Likely cause:** Long, complex goal prompts with many instructions may cause the explorer to spend excessive time processing the goal before beginning to write. This appears to be a consistent pattern for explorations with detailed, multi-part goal specifications. Math Explorers appear particularly prone to extended initial idle time (8-10 min vs 4 min for Standard Explorers) on simulation tasks.

**Prevention:** Include "write section by section, starting immediately" in the goal (see goal-design/instruct-incremental-writing.md). **Reactive fix:** Nudge after 3 minutes if no output. The 0% stall responds to nudges just as the mid-report stall does.

## Variant: Stall from Large-Write Attempt

A specific stall trigger: the explorer accumulates findings and then attempts to write the **entire report in one large write operation**. This causes a multi-minute pause (the system processes the large write) and can look like a stall even though the explorer is "active."

- **amplituhedron strategy-001 exploration 001** — REPORT.md sat at 33 lines (skeleton) for ~5 minutes while the explorer was apparently preparing a full write. Nudge to "write incrementally, section by section" immediately produced full content.

**Prevention:** Include explicit "write section by section" instruction in GOAL.md — see goal-design/instruct-incremental-writing.md for recommended wording. The nudge remains the reliable reactive fix; the GOAL.md instruction is the preventive version.

## Caution: Nudging Can Truncate Reports

Nudging to "write now" when the explorer is mid-computation can cause it to produce a **shorter report than requested**, stopping prematurely rather than completing all sections.

- **yang-mills strategy-001 exploration 005** — Report requested at 400–600 lines. After a nudge, the explorer produced only 215 lines — stopping before fully presenting all data tables and analysis.

**Implication:** The "write section by section" instruction (see goal-design/instruct-incremental-writing.md) is preferable to reactive nudging when report completeness matters. It prevents both the large-write stall *and* the truncation that can follow a blunt nudge. Reserve the nudge for situations where any output is better than none (e.g., explorer has been processing for many minutes with nothing written at all).

## Variant: Extended Thinking Loop in Computational Debugging

When an explorer encounters a complex computational failure (e.g., BCFW implementation disagreeing between two shift choices), it can enter an extended "high effort thinking" loop — spending 35+ minutes thinking about debugging before producing any output. This is more extreme than the standard mid-report stall: the explorer is not stalled on writing, it is stuck trying to solve the problem internally.

- **amplituhedron strategy-001 exploration 002** — Explorer spent 35+ minutes in thinking phases debugging BCFW sign/helicity bugs before producing the report. A nudge to "write your findings now" broke the loop and produced the 208-line report. Without the nudge, the explorer would have continued debugging indefinitely.

**Prevention:** The root cause is usually that the problem genuinely cannot be resolved without an independent ground truth (see also goal-design/require-independent-verification-baseline.md). Include in the goal: "if your two implementations disagree, document the disagreement and your diagnosis — do not continue debugging." This gives the explorer explicit permission to stop and report rather than loop.

**Reactive fix:** Nudge after 10 minutes if no output on a computational debugging task. The nudge should be explicit: "Stop debugging. Write up exactly what you found, what disagrees, and why you think it disagrees."

## Variant: Pre-Computation Coding Stall

A distinct stall type: the explorer has the goal and is in the thinking/planning phase but has NOT started writing code or producing output after 5-6 minutes. The report file may not even exist yet, or exists only as a short header. This differs from the 0% stall (where the report exists but is empty) — here the explorer hasn't even reached the point of creating its output files.

**Key feature:** A direct, structured nudge is more effective than a gentle "write now." The nudge should include: **(a) explicit code NOW instruction, (b) the output file path, (c) the starting code file path.**

- **yang-mills strategy-002 exploration-005** — Explorer was thinking for 6 minutes without coding. One nudge ("Stop thinking and start coding NOW. Write to [output file]. Start with [code file].") got it coding in 30 seconds. The structured format (output path + code path) was key — it gave the explorer two concrete anchors to start from.

**Template nudge for pre-computation coding stall:**
> "Stop thinking and start coding NOW. Write your code to `[absolute/path/to/code.py]`. Write results to `[absolute/path/to/REPORT.md]`. Implement the [measurement/simulation/computation] first, then analyze."

**Timing:** Nudge after 5-6 minutes of no output on a pure computation goal. For complex multi-part goals (5+ sections), allow up to 8 minutes before the first code nudge.

## Variant: Post-Computation Thinking Stall

After a long background computation completes (exit code 0), the explorer may enter an extended thinking phase (~10 minutes) before writing the report — apparently reviewing and organizing results before writing. This is distinct from the mid-report stall: the explorer is "thinking" not "writing."

**Reactive fix:** After a long computation completes, **paste the results directly into the nudge message** rather than just saying "write the report." This saves the explorer from having to re-read the output files and immediately unblocks the writing phase.

**Caution — multiple simultaneous background scripts [YM s003-E006]:** Don't start multiple long-running background computations at once. When two background shells run simultaneously, one finishes and the explorer processes it, but the second causes a delay — the explorer stalls at "Forming" for 30+ minutes without writing remaining sections. Nudge: "Write the results from the completed script to REPORT.md now."

- **yang-mills strategy-002 exploration-002** — After the 64-minute background scan completed, the explorer thought for ~10 minutes before writing. Nudge with explicit results ("The computation is done. Here are the results: [paste all 8 β values with τ_int]. Write the report NOW.") immediately produced the full report. Without pasting results, the explorer would have had to re-read files and think further.
- **riemann-hypothesis strategy-002 exploration-007** — Explorer ran all three adversarial tests, saved to `results.npz`, then entered a ~30-minute thinking loop without writing any section. REPORT.md remained in all-placeholder state. The post-computation thinking stall can last much longer than the earlier ~10-minute estimate — allow up to 15 minutes before concluding the stall is structural.

**Template nudge:** "The computation is done. Here are all results: [paste raw output data]. Now write the REPORT.md immediately. You have all the numbers above — no need to re-read any files."

**Time guidance:** Yang-mills s002 E002 stall was ~10 min; RH s002 E007 stall was ~30 min. For adversarial/multi-test explorations, budget up to 15 minutes before intervening.

## Variant: Computation-Done-But-Still-Debugging Stall

A distinct stall type: the explorer has **successfully computed and saved output** (data file exists, e.g., a .npz file with all results), but remains stuck in a debugging loop — trying to fix a non-critical tool failure (e.g., scipy.optimize ImportError) when the actual data is already there. The report never gets written because the explorer is still "trying to get the analysis code working."

- **riemann-hypothesis strategy-002 exploration-006** — The explorer computed all Part B results (N=500 matrix eigenvalues, β estimates, KS statistics) and saved them to `part_b_results.npz`. But scipy.optimize failed with an ImportError (`numpy.Inf` removed in newer numpy), so the explorer kept iterating on beta-fitting code instead of writing up the already-computed results. The REPORT.md stopped at 108 lines (Part B setup only, no results). Required multiple nudges.

**Distinguishing feature:** The computation IS done (output file exists with correct data); only the analysis/visualization code has an error. The explorer doesn't realize it already has what it needs.

**Reactive fix:** Direct and unambiguous nudge: *"Your computation is DONE. The data is in [filename]. Stop debugging [tool X]. Read the data from [filename] and write the report now."* The key is explicitly stating that the computation is done and naming the file — this short-circuits the debugging loop.

**Distinction from Post-Computation Thinking Stall:** In the post-computation stall, the computation completed and the explorer needs to write; in the computation-done-but-debugging stall, the explorer is actively trying to fix code that doesn't need to be fixed.

**Preventive fix:** In multi-part goals where some analysis might use fragile libraries, specify a fallback: "If [library X] fails, use [manual formula / alternative method] instead." See also goal-design/specify-computation-parameters.md for the startup diagnostics variant.

## Variant: Research-Buffering Stall (Iterative Search + Writeup)

A distinct and **systematically unpreventable** stall type for explorations that involve (1) iterative web research and (2) a structured final writeup. The explorer runs all searches but buffers all results for a final write that never happens. REPORT.md has a skeleton with placeholder sections; the content never materializes despite the explorer completing all the research.

**Key feature:** This is NOT prevented by the incremental writing instruction ("fill in each section as you finish it"). The LLM explorer naturally wants to complete all research before synthesizing. By the time it's done, context size and complexity make writing fail. This is a structural failure mode, not a stall that responds to nudging.

**Evidence:**
- **riemann-hypothesis strategy-002 E006** — First instance
- **riemann-hypothesis strategy-002 E007** — Second consecutive instance
- **riemann-hypothesis strategy-002 E008** — Third consecutive instance; goal included explicit "WRITE INCREMENTALLY" instruction; explorer ran 8+ web searches but 0 content reached REPORT.md after ~30 minutes

**Most reliable fix:** Kill after ~30 minutes of stagnation (REPORT.md not growing beyond the skeleton). **Extract results from the conversation history** (the searches ARE there, the explorer just didn't write them) and **manually write** the REPORT.md and REPORT-SUMMARY.md. For E008, manual writing took ~15 minutes — faster than waiting.

**Architectural fix:** Split into two explorations — (1) search-only task produces a raw dump file, (2) synthesis task reads the dump and produces the structured report. See `meta/methodology/split-search-from-synthesis.md`.

**Distinguishing features:**
- REPORT.md is a full skeleton with [SEARCHING...] or placeholder text in every section
- The explorer IS actively working (many tool calls, web searches visible in tmux)
- After 20–30 min, still 0 actual research content in the file
- Nudges do not reliably fix this (unlike other stall variants); the architecture is the problem

**Partial exception — highly specific nudges CAN work (RH s003-E007):**
- **riemann-hypothesis strategy-003 exploration-007** — Adversarial novelty review stalled for ~45 minutes with web searches but no writing (despite [SECTION COMPLETE] markers in goal). A blunt nudge ("STOP RESEARCHING. Write your findings NOW.") broke the stall and produced 141 lines. A second, very specific nudge ("5-8 bullet points, YES/NO/UNCLEAR, write REPORT-SUMMARY.md immediately") produced the final summary. **Planning assumption for web research: first write will happen after ~45 min, not 5 min.** The 42-line skeleton is misleading — it suggests more progress than actually occurred.
- **Revised guidance:** Nudges CAN work for research-buffering stalls if (a) the nudge is highly specific about format and scope, and (b) the research is mostly complete. For stalls where the explorer has done extensive research but not written, try a specific nudge first before killing. If the nudge doesn't produce output within 5 minutes, kill and extract manually.

## Variant: Extended Between-Task Computation Stall (3.5 Hours)

When an exploration involves multiple sequential computation tasks, the explorer can stall for **hours** between tasks — far longer than the typical mid-report or post-computation stalls. The explorer completes one computation task, saves results, but then enters an extended processing loop instead of starting the next task.

- **riemann-hypothesis strategy-003 exploration-003** — Explorer completed Tasks 0 (setup) and 1 (empirical R₂) successfully, saving results to .npz files. Then stalled for **3.5 hours** before Tasks 2 and 4 (K(τ) computation and Δ₃ cross-check). A direct nudge — "STOP thinking. You have R₂(r) from Task 1 saved. IMMEDIATELY write and run a Python script to complete Tasks 2 and 4" — produced results within ~15 minutes. The nudge was effective because it: (a) named the specific saved data file, (b) instructed to skip optional tasks (3 and 5), (c) gave an explicit "write and run" action.
- **riemann-hypothesis strategy-003 exploration-004** — Same multi-hour stall pattern. The explorer was actively computing (tmux pane showed results: "N=250 p=211 N2/p=296.2 beta_W=1.1124") but REPORT.md was not updated during computation. The explorer computed all results then deferred writing — a computation-buffering variant of this stall. Nudge "STOP thinking, run N=250 sweep NOW with specific prime list" was effective. **New detail:** providing a specific prime list in the nudge eliminated parameter-selection overhead and got the explorer moving immediately.

**Key features distinguishing from other stalls:**
- Duration: 3.5 hours (vs. 3-30 min for other stall types)
- The explorer HAS completed work and saved output — it's stuck between tasks, not stuck on a task
- The nudge must reference the saved data and specify which tasks to prioritize

**Timing guidance:** For multi-task computation explorations where the explorer has completed a task and saved data but is not progressing to the next task, nudge after **15 minutes** of no line-count change. Do not wait 30+ minutes — the stall will not self-resolve and can extend to hours.

## Variant: Context Pressure Emergency at 50+ Minutes (Math Explorer)

Math Explorer sessions running >45 minutes approach context limits (~12k tokens remaining). At this point, the explorer may show "Envisioning" status with the context limit warning. An immediate emergency nudge is required to extract whatever results exist before the session terminates.

- **riemann-hypothesis strategy-003 exploration-008** — Math Explorer showed "Envisioning (52m 27s)" with 12.2k tokens and context limit warning. Emergency nudge to write REPORT-SUMMARY.md succeeded, but the primary computation (K=N=5000 matched GUE test) was still running and could not be completed.
- **riemann-hypothesis strategy-003 exploration-009** — Context pressure at **33 minutes** (7.4k tokens remaining, "Tip: Use /clear" warning). Earlier than E008 (52 min) — likely because K=N=5000 GUE computation (15 trials of 5000×5000 matrices) consumed ~20 min of execution time. Emergency nudge "STOP, write REPORT-SUMMARY.md NOW" with **key numerical results pre-supplied** ("ratio = 0.888, 0.898, 0.952, 1.004, 1.090") produced the summary within 90 seconds. **Key technique: providing actual numbers in the emergency nudge eliminates the need for the explorer to recompute or re-read data — it can write immediately.**
- **yang-mills-conjecture exploration-008** — 75+ minutes of computation with report stuck at 119 lines. Needed nudge to write up. Consistent with the 50+ minute context pressure pattern for Math Explorers on heavy computation explorations.

**Timing guidance for Math Explorers:** Shorten the polling interval from 7 minutes to **5 minutes** for sessions running >45 minutes. At 50+ minutes, issue an emergency nudge regardless of apparent progress — context exhaustion can happen without warning. **For computations that include very large matrix operations (N≥5000), context pressure can arrive as early as 33 minutes** — monitor more aggressively. When issuing the emergency nudge, **pre-supply all key numerical results** in the nudge text itself.

## Variant: Math-Heavy Standard Explorer Context Exhaustion

Standard explorers (not Math Explorers) assigned long mathematical derivation tasks will spend 70%+ of context before writing. This triggers compaction, which may leave the explorer in a "queued messages" state that does NOT recover from nudges — the session must be killed and relaunched.

- **yang-mills strategy-003 exploration-002** — Standard explorer on geodesic convexity proofs spent 70%+ of context in deep thinking, compacted twice, required killing and relaunching. Produced 168 lines total.
- **yang-mills strategy-003 exploration-003** — Same pattern: after compaction, needed re-launch with updated context. The "queued messages" state is a dead end.

**Distinguishing feature:** The "queued messages" indicator in tmux. Nudges do not submit when the session is in this state.

**Reactive fix:** Kill the session and relaunch with current context (any partial results already written + the original goal). Do not wait for nudge delivery.

**Preventive fix:** For math-heavy goals given to standard explorers, send nudges MUCH earlier — at 40% context, not 80%. By the time compaction happens, writing is extremely unlikely.

## When to apply

Monitor every exploration for the stall pattern. If the report file hasn't grown in 3-5 minutes, nudge. For construction tasks, allow up to 5 minutes before nudging since the explorer may be doing genuine reasoning. **For technical mapping explorations requiring web research, allow extra time (5-10 minutes) — check the tmux pane for search activity rather than relying solely on line count.** For multi-section catalog tasks, include incremental writing instructions in the goal to prevent the large-write stall. **For computational implementation tasks (writing and running Monte Carlo code, multi-group simulations), the planning/coding phase alone can take 10–15 minutes before any output appears; if nothing is produced after 15 minutes, consider relaunching rather than nudging, as nudging at this stage may produce truncated output.** **For computational debugging tasks where two results disagree, allow 10 minutes before nudging; at that point give an explicit stop-and-report nudge.** When completeness of output matters, prefer the proactive "write section by section" instruction over reactive nudges.
