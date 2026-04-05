---
topic: Test whether a target is independently improvable before pursuing variations
date: 2026-03-30
source: "vasseur-pressure s2-exploration-003 meta"
---

## Lesson

When a decomposition audit (Phase 0) identifies a single target step as the potential weak link, the FIRST analytical exploration should test whether that target is independently improvable — i.e., whether improving it is possible without solving the entire original problem. If the target is circular with the main problem, you learn this quickly and can pivot. Do not spend 3+ explorations trying variations before testing viability.

## Evidence

Vasseur-pressure S2-E001 (sharpness audit) identified the Chebyshev step as the single potentially improvable link in the 4/3 chain. S2-E003 then tested this by analyzing six potential improvement routes:

- Support-restricted Chebyshev: RULED OUT (weaker in convergent regime)
- Holder interpolation with different q: RULED OUT (information-preserving; exponent independent of q)
- Lorentz space refinement: RULED OUT (affects constants, not exponents)
- Gradient/isoperimetric approach: RULED OUT (already exploited via Sobolev)
- L^2 Chebyshev: RULED OUT (weaker for small U_{k-1})
- PDE-based integrability beyond L^{10/3}: CIRCULAR (equivalent to proving regularity)

All six routes either fail or reduce to the original problem. The Chebyshev step is NOT independently improvable — it faithfully reflects the integrability gap between the energy space and the regularity threshold. Improving L^{10/3} to L^4 Chebyshev requires H^{5/4} regularity, which IS the Lions threshold.

This circularity was established in ONE exploration. Without the viability test, subsequent explorations might have spent weeks on Lorentz refinements, support tricks, or interpolation variations — all provably futile.

## Protocol

1. Decomposition audit identifies single target step (e.g., "Chebyshev on L^{10/3}")
2. FIRST analytical exploration: enumerate all plausible improvement routes for that step
3. For each route: determine whether the improvement is (a) impossible for structural reasons, (b) possible but insufficient, (c) circular with the original problem, or (d) genuinely open
4. If ALL routes are (a), (b), or (c): the target is NOT independently improvable — pivot to a different attack strategy (e.g., bypass the step rather than improve it)
5. If any route is (d): pursue that specific route

## Distinction from Existing Patterns

Distinct from **decomposition-audit-before-attacking-barrier** (identifies the target; this tests the target's viability). Distinct from **decisive-negative-pivot** (dimensional analysis kill; this is analytical circularity detection). Complementary to **model-pde-comparison-for-mechanism-identification** (comparison can reveal circularity by showing the barrier is universal).
