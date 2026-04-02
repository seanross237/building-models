# Meta-Learning: Exploration 003b — Novelty Search

## What Worked Well
- **Specific search targets:** Listing authors (Griffiths, Gell-Mann, Hartle, Kent, Brun) and search terms gave the explorer concrete places to look. The Brun (2000) partial prior was found this way.
- **Three levels of prior discovery:** Defining "direct," "indirect," and "adjacent" priors helped the explorer calibrate its verdict. The final assessment used this framework effectively.
- **Running in parallel with the computation:** The novelty search finished much faster (~40 min vs ~2.5 hours for the math explorer) and didn't block the pipeline.

## What Could Be Improved
- **Could have been even more specific about what "the claim" is.** The explorer had to reconstruct the exact claim from the goal description. A one-sentence formal statement of the claim at the top would have been cleaner.

## Lessons for Future Goal Design
- For novelty searches, state the exact claim being checked as a single formal sentence at the top of the goal. Everything else is search guidance.
- Parallel novelty search + computation is an efficient pattern. The novelty search informs how to interpret the computation results.
