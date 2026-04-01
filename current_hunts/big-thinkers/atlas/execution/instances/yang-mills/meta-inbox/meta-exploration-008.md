# Meta-Learning: Exploration 008

## What worked well
- The code was well-written and produced correct results immediately when run
- The spectral gap + Adhikari-Cao analysis produced the strongest quantitative result of the entire strategy
- Having the code saved in code/ allowed recovery after the explorer timed out

## What didn't work
- Explorer timed out at 43% after ~25 minutes. It wrote code and a report skeleton but never populated the results.
- The report template was filled with "(Populated after running code)" placeholders
- The nudge to write was queued but never processed

## Lessons
- Math Explorers can get stuck in long thinking loops between code execution and report writing. This seems to happen when there are multiple computational results to synthesize.
- Always save code to files (not inline) — this enables recovery when the explorer times out
- The spectral gap computation is trivial (< 1 second) — the explorer spent 25 minutes thinking, not computing. Goal should have been "compute this specific thing and report the numbers immediately"
- For simple computations (eigenvalue problems), a single focused script with results printed directly is better than a complex multi-file setup
