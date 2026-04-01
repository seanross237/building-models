# Meta-Learning: Exploration 005

## What worked well
- **Explicit novelty search protocol** worked. Searching for the specific identity, then searching for closest prior work (Milgrom 1999), gave a clear novelty verdict.
- **Equation-level Verlinde comparison** was exactly right. Comparing interpolation functions algebraically (not just narratively) showed the distinction clearly.
- **Including the free-fall objection** as part of the literature task was efficient — it fits naturally since the objection has a 25-year literature trail.

## What didn't work
- The explorer couldn't access all papers directly (some timeouts). This limited the depth on some sources.

## Lessons
1. **Ask for closest prior work explicitly.** "Find the paper that comes closest to this result" is a sharper question than "has this been published?"
2. **The free-fall objection is structural, not accidental.** It was flagged by Milgrom himself in 1999 and remains unresolved. Any future exploration attempting to resolve it should be aware this is a 25-year-old problem — easy resolutions have presumably been tried.
3. **Verlinde's actual predictions are weaker than his reputation.** He gets only the deep-MOND limit, not the full interpolation function, and fails the RAR. This was not obvious from the original exploration 003 survey — the detailed comparison in 005 was necessary to reveal this.
