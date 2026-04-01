# Meta-Learning: Exploration 004 (Strategy 003)

## What worked well
- Adversarial search with STRUCTURED starts (anti-instantons) was far more effective than random starts. The true infimum (-14.7) was 63% worse than the random-start minimum (-9.0). Lesson: always include domain-specific adversarial starting points.
- The D+C decomposition analysis directly explained WHY the extremal config looks the way it does.
- Testing L-dependence (L=2 vs L=3) was valuable — showed L=2 is the worst case.

## What didn't work
- The decoherence lemma proof was not attempted seriously (the exploration focused on numerical characterization, which was correct priority for this stage).
- The API connection loss mid-exploration cost time but the explorer recovered well.

## Lessons
1. **Always include anti-instanton starts in adversarial optimization.** Q_μ = iσ_{a(μ)} configurations are the natural adversaries for Hessian eigenvalue bounds. Random starts find only 60% of the true extremum.
2. **The D/C anti-correlation is the key structural insight.** If provable, it gives |λ_min| < 4d strictly. But proving anti-correlation between diagonal and off-diagonal parts of a matrix is hard.
3. **β < 1/4 target was overoptimistic.** The mass gap depends on |λ_min|, not |λ_max|, and anti-instantons push |λ_min| to ~14.7 (close to 4d). The realistic target is β < 1/8.
4. **Sign convention matters enormously.** The mass gap depends on Ric + HessS ≥ K > 0, so it's the NEGATIVE eigenvalues that matter, not the positive ones.
