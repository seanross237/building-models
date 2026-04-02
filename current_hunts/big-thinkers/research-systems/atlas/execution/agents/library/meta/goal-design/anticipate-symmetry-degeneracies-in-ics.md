---
topic: Anticipate symmetry degeneracies when specifying initial conditions
category: goal-design
date: 2026-03-30
source: "navier-stokes strategy-001 meta-exploration-003"
---

## Lesson

When specifying initial conditions for numerical explorations involving directional or alignment-dependent quantities (vortex stretching, strain-vorticity correlation, etc.), anticipate symmetry degeneracies that cause the quantity of interest to vanish identically. Either exclude degenerate ICs from the test set, or flag them as known edge cases with the expected behavior stated.

## Evidence

- **navier-stokes strategy-001 exploration-003** — The goal specified vortex tube and anti-parallel tube ICs without z-perturbation. Z-invariant vortex tubes have exactly zero vortex stretching (strain tensor acts in x-y plane while vorticity is in z, giving integral(S*omega*omega) = 0). ABC flow also has VS = 0 (Beltrami property: omega = u implies integral vanishes by incompressibility). The explorer discovered these degeneracies and added z-modulation as a fix, but this wasted time. The goal should have either (a) specified z-perturbed ICs upfront, or (b) flagged "z-invariant flows have zero VS — ensure z-symmetry breaking."

## When to Apply

- When the quantity being measured depends on alignment between two vector/tensor fields (vortex stretching = strain-vorticity alignment)
- When ICs have high symmetry (z-invariance, isotropy, Beltrami property)
- When the quantity can be shown to vanish by a simple integration-by-parts or orthogonality argument

## Relationship to Other Entries

Distinct from `require-matrix-sanity-checks.md` (which is about checking matrix construction is non-degenerate). This is about anticipating that the *physics* of certain symmetric configurations makes the measured quantity zero — a symmetry analysis step before writing the goal, not a runtime sanity check.

Complements `specify-computation-parameters.md`: parameter specification covers "what values to use"; this covers "which configurations to avoid or modify."
