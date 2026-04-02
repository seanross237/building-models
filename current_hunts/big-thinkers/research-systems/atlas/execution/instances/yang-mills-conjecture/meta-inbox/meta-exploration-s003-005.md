# Meta-Learning: Exploration 005 (Strategy 003)

## What worked well
- Testing the lemma adversarially BEFORE trying to prove it was the right strategy. Found the counterexample (||C|| = 11.68) within the first 30 minutes, which redirected the entire exploration toward understanding WHY it fails.
- The per-plaquette proof (||C_□|| ≤ 3) and d=2 proof are genuine positive results that came from the failed attempt.
- The closed-form SVD of the color kernel (SVs = (2, 2, 2|β₀|)) is a beautiful structural result.

## What didn't work
- The E004 survey (2000+ configs, all below 10) was misleading because it used random configs + specific anti-instanton starts, not gradient ascent ON ||C||. Gradient ascent on ||C|| finds very different configs (near saddle points where D ≈ 0). Lesson: when testing a bound numerically, always use gradient ascent on the EXACT quantity being bounded.
- The 6 proof approaches from the GOAL were mostly dead ends (approaches 1-4 all gave bounds too loose by 50%+). Approach 5 (variational/perturbation) correctly identified flat as a local max but couldn't prove global. Only the per-plaquette approach gave anything useful.

## Lessons
1. **Always adversarial-test a lemma before trying to prove it.** This exploration would have been wasted if all 70 minutes went to proof attempts for a false lemma.
2. **Gradient ascent on the EXACT quantity matters.** E004 tested ||C|| with random starts and found max 7.9. E005 tested with gradient ascent specifically targeting ||C|| and found 11.68. The 48% gap means E004's numerical "evidence" for decoherence was wrong.
3. **Per-plaquette bounds aggregate poorly in high dimensions.** The ratio ||A_struct||/||A_total|| = 1.8 for d=4 means any per-plaquette approach loses 80% of the sign structure. This is a fundamental dimensional obstacle.
4. **D/C anti-correlation is the key physics.** The proof cannot separate self-terms from cross-terms. Must bound the full Hessian directly.
