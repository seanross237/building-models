# Meta-Learning Note — Exploration 001

## What Worked Well
- **Math Explorer was the right choice** for a computation-heavy task. The explorer wrote 628 lines of working code and produced 10 verified numerical results.
- **Providing explicit formulas in the goal** (Parke-Taylor, BCFW shift, Grassmannian integral) gave the explorer clear targets. It didn't have to derive the formulas — just implement and evaluate them.
- **Three-way comparison** was an excellent structure. Having Parke-Taylor as the baseline made debugging BCFW and Grassmannian straightforward.

## What Didn't Work Well
- **The explorer went into a 10+ minute thinking loop** after the computation timed out at 30s. It tried to write a 900-line all-in-one script that was too complex. Lesson: specify in the goal that scripts should be modular and broken into stages.
- **Report writing was delayed** — the explorer didn't update REPORT.md incrementally until nudged. Despite the system prompt saying to write incrementally, the explorer preferred to compute everything first. The nudge at ~26 minutes was necessary and effective.
- **The initial prompt may have been too long** — there was a ~10 minute period at the start where the explorer appeared stuck at 0%. Shorter, more focused prompts might start faster.

## Lessons for Future Explorations
1. **Tell math explorers to break computation into stages explicitly** — "Run each method as a separate script, verify, then combine." Don't let them write mega-scripts.
2. **The 30s timeout for bash commands is aggressive for computation** — but the explorer adapted by breaking up the script after the nudge.
3. **Goal length matters** — this goal was ~80 lines. Could probably be more effective at 40-50 lines with just the key formulas and success criteria. The explorer will look up details on its own.
4. **Nudging works** — the explorer responded well to the mid-run nudge. The queued message pattern (message sent while thinking, processed after) works fine.
