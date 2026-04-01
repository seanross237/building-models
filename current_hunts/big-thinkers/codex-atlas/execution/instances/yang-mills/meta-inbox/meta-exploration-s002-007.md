# Meta-Learning Note: Strategy-002 Exploration 007

**Type:** Standard Explorer — Adversarial review with computation

## What Worked

1. **Adversarial review found the actual tight bound.** The adversarial reviewer was told to be "genuinely adversarial" and to "look for where the claim could fail." This produced the most important finding of the strategy: the staggered mode at identity gives H_norm = 1/12 exactly. The structured adversarial prompting works.

2. **The explorer computed the analytical maximum, not just searched.** Rather than only doing gradient ascent (like E006 did), E007 reasoned from first principles: "what configuration maximizes the Hessian?" and derived the staggered mode analytically. This is more powerful than blind gradient ascent.

3. **Rate limit recovery worked.** The explorer hit its rate limit, recovered, re-read REPORT.md, and continued writing. The incremental writing strategy (write as you go) made recovery possible.

## What Didn't Work

1. **Long thinking without writing (25+ minutes at 48%).** E007 spent 25 minutes computing before writing anything. Had to be nudged twice. The instruction "write section by section" should also say "write after each attack, not after all attacks."

2. **E007 is a hybrid (literature + computation), which took longer.** Standard explorers are supposed to be for literature only. When they also need to run code, they take 2× longer. Either give computation to math explorers or explicitly budget more time for hybrid explorations.

## Key Lessons

- **Adversarial review should ALWAYS include a "what is the analytical worst case?" attack.** Random and gradient-ascent adversarial searches are weak compared to structured analysis. E007 demonstrated this: the structured staggered mode is 14× worse than what random search found.
- **The adversarial reviewer found the tighter bound (1/12) better than the forward explorers (E005, E006).** This suggests adversarial review should be run EARLIER in the strategy, not as a later step. The 1/12 bound could have been found in E005 if an adversarial angle had been included there.
- **An adversarial explorer that runs code should be given the math-explorer system prompt.** The standard explorer is limited in computation depth. E007 ran code successfully but had to fight for time to do it.
