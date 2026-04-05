# Meta-Learning: Exploration 001 (Strategy 003)

## What worked well
- The staged computation design (Stage 0 sanity check → Stage 1 counterexample → Stage 2 Hessian → Stage 3 decomposition → Stage 4 verdict) was perfect for this verification task. Each stage built on the previous.
- Including the Q=I sanity check as a mandatory first step ensured the implementation was correct before looking for counterexamples.
- The finite-difference verification of HessS vs (β/2N)M was the critical computation — it revealed that the library's claim about their proportionality was WRONG, and this completely changed the direction of the investigation.

## What didn't work
- The library entry claiming HessS = (β/2N)M was misleading. It appears this was an assumption, not a verified fact. Lesson: library entries about operator relationships should always be tagged with how they were verified (analytically, numerically, or assumed).
- The exploration ran long (~70 minutes) partly because the gradient ascent was expensive. Could have been faster if the goal specified starting from known high-eigenvalue configs (like iσ₃).

## Lessons for future explorations
1. **Always verify operator identities numerically before building proof strategies around them.** The HessS ≠ (β/2N)M discovery invalidates 2 full strategies' worth of M(Q)-focused work.
2. **Flat connections with non-trivial holonomy are the stress test for lattice Yang-Mills conjectures.** The Z₂ center element iσ₃ is the simplest and most dangerous.
3. **Finite-difference Hessian computation is expensive (43.7s for 192×192) but essential for verification.** Budget 10 minutes for this in goals.
4. **The real proof target was hiding behind a proportionality assumption.** When the first exploration reveals the assumed equality is wrong, that's the most important finding.
