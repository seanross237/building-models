# Meta-Learning Note: Strategy-002 Exploration 002

**Type:** Math Explorer — Computational spectral gap measurement

## What Worked

1. **Explorer self-diagnosed and fixed a serious bug.** The initial parallel heat bath implementation gave wrong results (⟨P⟩ ≈ 0 at all β including β=3.0). The explorer identified this as "parallel updates violate detailed balance" and rewrote with a checkerboard decomposition. This produced correct results. Lesson: math explorers are capable of debugging their own code if given enough context about what the correct output should look like.

2. **Providing E003 SU(2) code as a starting point.** The explorer adapted the existing heat bath code rather than writing from scratch, which saved time and gave a known-good foundation.

3. **Print-first discipline.** Instructing "print results as you go" meant we got data even when individual runs took longer than expected. Each β value was reported immediately when computed.

## What Didn't Work

1. **Sequential SU(2) heat bath is slow.** Each β value on a 4⁴ lattice with 2000 sweeps took ~8 minutes. 8 values × 8 min = 64 min total. This is at the edge of explorer feasibility. For larger lattices (6⁴, 8⁴), this would be completely infeasible in one run. **Lesson:** For spectral gap scans, either (a) use fewer sweeps (500 instead of 2000), (b) use fewer β values (5 instead of 8), or (c) use a smaller lattice (4⁴ is minimum anyway).

2. **Long thinking phase after computation.** After the background scan completed (exit code 0), the explorer thought for ~10 minutes before writing the report. Had to be nudged with explicit result data. **Lesson:** After a long computation, explicitly say "The computation is done. Here are the results: [paste results]. Write the report NOW."

3. **First implementation (parallel updates) was wrong and wasted ~15 minutes.** The initial code ran quickly (gave results in seconds) but all data was garbage. The fast completion should have been a red flag (8 minutes per β should not become 2 seconds per β). **Lesson:** Always cross-check at least one data point against a known analytic or literature value before accepting fast results as correct.

## Lessons for Future Explorations of This Type

- For β-scan computations: Specify "cross-check your first data point against a known value (e.g., strong-coupling expansion ⟨P⟩ ≈ β/4 for β << 1) before running the full scan."
- Reduce default sweep count to 500-1000 for exploratory scans (enough for autocorrelation measurement on 4⁴)
- Add "if computation finishes quickly (< 30 seconds per data point), something is wrong — check against known results"
- After long background computations: paste the results directly into the nudge message so the explorer doesn't have to re-read files
