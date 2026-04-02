# Meta-Learning Note: Strategy-002 Exploration 005

**Type:** Math Explorer — Monte Carlo Hessian measurement

## What Worked

1. **Nudge worked perfectly.** E005 was thinking for 6 minutes without coding. One nudge ("Stop thinking and start coding NOW") got it coding in 30 seconds. The nudge should always include: (a) explicit instruction to write code NOW, (b) the output file path, and (c) the starting code file path.

2. **The finite-difference Hessian approach worked well.** ε = 1e-4 step gave stable, reproducible results. 200 samples per β (20 configs × 10 tangent vectors) was sufficient to estimate the max.

3. **The finding was unexpected and major.** The Lemma 4.1 slack factor of 12-45× was not anticipated. When a computation gives a surprising result, the explorer correctly paused to interpret it before writing the report.

## What Didn't Work

1. **Used d=3 (3D lattice) instead of d=4 (4D).** The GOAL.md said "4³ lattice (3D is fine)" which was correct for speed, but the most important case is d=4. Future explorations should run the full 4D case to get the directly applicable result.

2. **Did not search for worst-case configurations.** The measurement only covered typical Gibbs configurations. The Lemma 4.1 bound applies to ALL configurations (including non-Gibbs ones). The worst case might saturate the bound.

## Lessons

- For Hessian/curvature measurements: always include BOTH a typical-configuration scan AND a worst-case search (random or adversarial perturbations of the configuration).
- Specifying "d=3 is fine" in a goal about a 4D physics problem can mislead — the explorer used 3D throughout. Better: "run on 4³ lattice using d=4 (4-dimensional, L=4 lattice with d=4 in the Hessian formula)."
- Unexpected major results should trigger more careful validation (more configs, larger lattice, adversarial cases). Design the next exploration to stress-test the finding.
