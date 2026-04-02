---
topic: For exact-support mechanism audits, define leakage at the coefficient-weighted amplitude level before packet coarse-graining
category: methodology
date: 2026-03-31
source: "exact-ns-no-near-closed-tao-circuit strategy-001 meta-exploration-001"
---

## Lesson

When a reduced mechanism is specified by exact quadratic monomials, leakage should be measured at the same level: exact coefficients times exact amplitudes. Triad counts and packet-energy comparisons are too coarse because they erase the sign, phase, and coefficient structure that decides whether the mechanism actually survives.

If a packet formulation is still useful, it should be treated as a backup coarse-graining after the amplitude-level definition exists, not as the primary Phase 1 object.

## Evidence

- **exact-ns-no-near-closed-tao-circuit exploration-001** — The decisive step was not "mode vs packet" in the abstract. It was recognizing that Tao's gate logic is monomial-level and phase-sensitive, so the right leakage scalarization had to come from exact helical triad contributions split into desired, internal leakage, and external leakage.
- The same exploration rejected combinatorial triad counts as a primary metric because they ignore coefficient size and actual amplitudes.
- It also rejected packet-energy leakage as the primary metric because packet energies lose the phase information needed to tell whether a tiny trigger channel or a spectator channel is dynamically decisive.

## Protocol

1. Write the exact interaction law on the chosen finite support.
2. Split each target equation into desired terms and leakage terms.
3. Weight leakage by the exact coefficient-amplitude contributions, not by edge counts.
4. Only after the amplitude-level object exists, decide whether a packet coarse-graining is useful as a secondary summary.

## When to Apply

- exact-support realization problems
- toy-circuit vs exact-PDE comparisons
- helical/Fourier interaction audits
- any mission where the reduced mechanism is carried by a small number of explicit monomials

## Relationship to Other Lessons

Distinct from `toy-subsystem-isolation-inside-exact-network.md`, which says to test whether the subsystem survives at all once exact interactions are restored.

Distinct from `goal-design/require-mechanism-layer-maps.md`, which identifies the layers and role table.

This entry says how to make the leakage metric faithful once the target subsystem has been specified.
