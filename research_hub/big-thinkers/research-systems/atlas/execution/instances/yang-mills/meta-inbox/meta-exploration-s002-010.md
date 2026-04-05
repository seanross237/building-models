# Meta-Learning Note: Strategy-002 Exploration 010

**Type:** Math Explorer — Large numerical scan + proof attempt + convention audit

## What Worked

1. **Large numerical scan was decisive.** 100 configs spanning 4 categories (random, Gibbs, perturbations of Q=I, adversarial ascent) with zero counterexamples. The adversarial ascent category is especially valuable — it explicitly searched for the maximum and found 0.063 << 1/12 = 0.083. This is much stronger than random sampling alone.

2. **Convention issue found and corrected.** The explorer caught that E009's code had a missing 1/N factor (giving λ=8β instead of 4β). Building in a convention check against Q=I (where the expected eigenvalue is known) is an excellent self-test strategy.

3. **The "saturation" finding was a bonus.** The B_P intermediate bound (∑|B_P|²=16|v|² exactly at Q=I) was observed to be exactly saturated. This is additional evidence that Q=I is genuinely the worst case.

4. **The B_P bound = 4d|v|² numerically confirmed.** The key conjectured inequality ∑_□ |B_P|² ≤ 4d|v|² was computed for all 100 configs — always satisfied, saturated only at Q=I. This is the key missing piece for the full proof.

## What Didn't Work

1. **Initial convention error cost 20 minutes.** The explorer had to debug the 8β vs 4β discrepancy before running the main scan. A GOAL.md instruction like "Before running any scan, verify λ_max = 4β at Q=I as a sanity check" would have caught this faster.

2. **Temporal gauge proof failed.** The attempt to prove ∑_□ |B_P|² ≤ 4d|v|² in temporal gauge was inconclusive. This suggests the proof may require a different approach (representation theory or convexity argument rather than direct gauge fixing).

3. **Adversarial ascent used stochastic hill climbing, not analytical gradient.** The REPORT-SUMMARY notes that "gradient ascent with analytical gradient" would be stronger. For the final max at 0.063, we don't know if it's a true local max or just a stopping point.

## Key Lessons

- **Always include a sanity check at Q=I before running a scan.** λ_max should equal 4β under SZZ convention. If it's 8β, you have the wrong convention.
- **Adversarial strategies should include both stochastic and analytical gradient ascent.** Stochastic hill climbing may miss true local maxima.
- **B_P intermediate bound saturation is a useful diagnostic.** If ∑|B_P|² = 16|v|² at some Q, that Q is Q=I or close to it. Can use this to identify the worst-case configuration without computing eigenvalues.
- **100 configs spanning 4 categories is the right scale for a conjecture check.** Fewer is anecdotal; this level gives genuine confidence.
