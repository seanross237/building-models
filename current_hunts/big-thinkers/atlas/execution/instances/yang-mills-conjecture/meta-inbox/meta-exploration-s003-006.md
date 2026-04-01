# Meta-Learning: Exploration 006 (Strategy 003)

## What worked well
- Testing the combined bound |D|+||C|| ≤ 4d adversarially before attempting to prove it. Found the counterexample quickly (uniform θ=2π/3).
- Structured configs (uniform rotations) found violations that random configs (500) completely missed.

## What didn't work
- Only 1 of 3 approaches was completed (B). Approaches C and A were coded but not run. The exploration should have been more focused — either run all three shallowly or commit to the most promising one deeply.
- The GOAL described all three approaches equally but should have weighted by promise. Approach C (concavity) was probably the most promising and should have been tried first.

## Lessons
1. **Norm-additive bounds are fundamentally limited.** |λ(D+C)| ≤ |D|+||C|| loses eigenvector cancellation information. Any proof through this route is doomed for d≥3.
2. **Uniform rotations are a critical test class.** They have D_min = -2(d-1) exactly (all edges equivalent) while allowing ||C|| > 2(d+1). Random and anti-instanton starts don't find these.
3. **When time is limited, focus the exploration.** With 3 approaches and limited compute, better to deeply investigate 1 than shallowly touch 3.
