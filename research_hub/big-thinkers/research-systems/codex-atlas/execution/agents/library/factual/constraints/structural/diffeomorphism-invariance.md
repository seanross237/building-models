---
topic: constraints/structural
confidence: verified
date: 2026-03-24
source: exploration-001-structural-recovery-constraints
---

# Diffeomorphism Invariance (Constraint A4)

**Statement:** The theory must be invariant under general coordinate transformations (diffeomorphisms), or deformations thereof that reduce to diffeomorphism invariance in the classical limit. This is the gauge symmetry of gravity.

**Mathematical form:**
Under x^μ → x^μ + ξ^μ(x):
- δg_μν = ∇_μ ξ_ν + ∇_ν ξ_μ (at linearized level)
- Physical observables must be diffeomorphism-invariant (or at least BRST-invariant)

**Restrictiveness: MAXIMALLY RESTRICTIVE**

This is one of the most powerful constraints because:
- Combined with Weinberg's soft graviton theorem, it forces the massless spin-2 particle to couple universally to the stress-energy tensor → **uniquely selects Einstein gravity at leading order**
- Horava-Lifshitz gravity explicitly breaks full diffeomorphism invariance (keeping only foliation-preserving diffeomorphisms), which generically introduces a problematic extra scalar mode
- Any discretization of spacetime (lattice, causal sets, spin foams) must show how diffeomorphism invariance emerges in the continuum limit

## Correct Degrees of Freedom (Derived Constraint A3)

In 4D, a massless spin-2 graviton has exactly 2 physical polarizations (helicity ±2):
- Total components: 10 (symmetric 4×4 tensor)
- Remove gauge: -4 (diffeomorphisms) × 2 = -8
- Physical DOF: 10 - 8 = 2

This is automatically satisfied by any theory that correctly implements diffeomorphism invariance. Constrains massive gravity (vDVZ discontinuity, Boulware-Deser ghost), bimetric theories, and higher-spin theories.

## Status Across Approaches

- **String theory:** Realized through worldsheet diffeomorphism invariance + target space gauge invariance
- **LQG:** Built in by construction (background-independent quantization preserves spatial diffeomorphisms), though Hamiltonian constraint status (time diffeomorphisms) remains contentious
- **Asymptotic Safety:** Maintained as a Ward identity constraint on the effective action

## Dependency

Diffeomorphism invariance is genuinely independent. Correct DOF (A3) follows from diffeomorphism invariance (A4) + unitarity (A1).
