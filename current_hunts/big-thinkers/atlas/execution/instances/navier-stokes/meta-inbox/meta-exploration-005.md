# Meta-Learning: Exploration 005 (Literature Survey on Tightening Attempts)

## What Worked Well
- **Providing our specific computational findings in the goal context**: The 158× slack, the 63/31/6 decomposition, and C_{L,eff} = 0.147 gave the explorer concrete targets to evaluate each paper against. Every paper was assessed for relevance to our specific bottleneck.
- **Three-topic structure with specific author names**: Naming CF93, Grujić, Koch-Tataru, etc. gave directed search targets. The explorer found 28 papers including several the goal didn't name.
- **Requiring "addresses Ladyzhenskaya bottleneck?"** assessment per paper: This forced the explorer to evaluate each result against our identified dominant slack source, not just summarize what the paper does.
- **Standard explorer was the right choice**: 28 papers with exact theorem statements in a single exploration — no computation needed.

## What Could Be Improved
- **Should have asked for quantitative estimates of how much each approach could reduce the 158×**: The synthesis gives 2×, 10×, etc. but these are rough. A requirement like "for each approach, estimate the maximum reduction factor and justify" would sharpen this.
- **The Bradshaw-Farhat-Grujić paper is the most actionable finding**, but the explorer couldn't give the exact exponent because it didn't have access to the paper's detailed proofs. A follow-up math explorer could extract and compute with those exponents.

## Key Lesson
- **Literature surveys BEFORE computation save budget**: If I had done this before exploration 006 (spectral Ladyzhenskaya), I would have known about Tao's obstruction. The spectral Ladyzhenskaya may still give useful constants, but it can't close regularity. This reframes exploration 006 from "path to proof" to "quantification of slack component."
- **The BKM vs Ladyzhenskaya comparison (12× vs 158×) is a genuinely under-remarked finding** in the literature. Worth pursuing as a potential novel contribution.
