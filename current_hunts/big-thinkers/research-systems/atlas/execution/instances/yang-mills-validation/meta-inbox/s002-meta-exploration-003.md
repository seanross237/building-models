# Meta-Learning: Strategy-002 Exploration 003

## What Worked Well
- Testing BOTH multi-link and single-link (one-hot) perturbations was crucial — multi-link supports the hypothesis, one-hot disproves it
- Multi-step-size verification (5 h values) was essential to confirm the d=2 counterexample is genuine
- Starting with d=2 (cheaper) allowed thorough testing before d=4
- The explorer correctly identified that E001 missed the one-hot regime

## What Didn't Work
- REPORT.md was written late (stuck at 75 lines for most of the exploration). "Write incrementally" needs stronger emphasis.
- The d=4 one-hot test was only preliminary (θ up to 0.2). Should have pushed to θ=1.0 to find the actual peak.

## Key Lesson
- **E001's stress test missed the critical regime.** E001 tested Haar-random (large perturbations), near-identity (all links scaled), and one-hot at θ=π (large angle). The violation is at one-hot, SMALL angle. This means stress tests need systematic coverage of perturbation types: (1) all-link random, (2) all-link scaled, (3) single-link random angle, (4) single-link parametric sweep. E001 tested (1), (2), and partially (3) at large angles, missing (4).
- **When a numerical pass depends on testing regime, always test adversarially at ALL scales.** The gap ∝ ε² near identity made small perturbations look safe, but one-hot perturbations are a different dimension of the search space.
