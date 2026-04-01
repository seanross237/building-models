# Meta-Learning Note: Strategy-003 Exploration 006

**Strategy:** 003, Phase 2
**Explorer type:** Math Explorer
**Task:** Full operator M(Q) - M(I) eigenvalue verification + pure gauge isometry

## What Worked Well

- The math explorer correctly prioritized computation over thinking — ran Python scripts immediately.
- The trace analysis (Tr(M(Q)) = Tr(M(I))) was a key structural insight that wasn't in the goal. The explorer discovered it as a byproduct of setting up the computation.
- Gradient ascent on P^T R P (not just on λ_max(M)) was a good choice — directly tested the correct target.
- The [VERIFIED]/[COMPUTED] tags correctly distinguished rigorously verified facts from numerical computations.

## What Didn't Work

- The explorer ran a 10-minute background script early on, then stalled at "Forming" for 30+ minutes without writing sections 5 and 6. Required a nudge to wrap up.
- Two background shells were running simultaneously — one finished and the explorer processed it, but the other caused a delay. Lesson: don't start multiple long-running background computations at once.

## Lessons

1. **Nudge math explorers when background scripts complete**: After a long background script finishes, send "Write the results from the completed script to REPORT.md now." The explorer may be waiting for a second script that's slow.

2. **The trace constraint is a powerful tool**: Tr(M(Q)) = constant (proved from orthogonality of transport) immediately implies R(Q) is trace-free. Any proof of λ_max reduction MUST work around this — you can't bound all eigenvalues, only the top ones.

3. **Gradient ascent on the PROJECTION (P^T R P) is more informative than on M directly**: Since we care about the top eigenspace, gradient ascent on the 9×9 projected matrix directly tests the correct target. Future explorations should always include this.

## Key Findings for Future Strategizers

1. **Tr(M(Q)) = Tr(M(I)) for ALL Q** — proved from orthogonality of adjoint transport. This is a theorem, not a conjecture. It means R(Q) is TRACE-FREE, so R(Q) ≼ 0 globally is impossible (trace-free NSD = zero). The correct target is the TOP EIGENSPACE projection.

2. **P^T R(Q) P ≼ 0 for 42 tested configs** — gradient ascent plateaus at -8 to -11, never near 0. This strongly suggests the inequality is true.

3. **Gradient ascent on P^T R P** didn't find a counterexample. The margin is huge (min eigenvalue -8 to -11, would need to increase by 8-11 units to violate).

4. For the analytical proof: staggered modes have structure v = f_{stag}(x,μ) ⊗ n (spatial pattern × fixed color direction n). The B_□(Q, v) involves Ad_P(n) for partial holonomies P. Bounding ∑_□ |Ad_P(n)|_contribution ≤ |ω_□(v)|² requires controlling how much adjoint rotations can coherently reinforce vs. destructively interfere.
