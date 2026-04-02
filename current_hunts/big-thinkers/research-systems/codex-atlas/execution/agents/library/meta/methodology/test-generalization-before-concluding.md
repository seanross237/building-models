---
topic: Always test generalization of a positive finding before treating it as a strategy conclusion
category: methodology
date: 2026-03-30
source: "vasseur-pressure meta-exploration-010"
---

## Lesson

When a mechanism or property is demonstrated for an exact special case (exact eigenstate, exact symmetry, exact solution), **always test whether it extends to perturbations before including it as a strategy conclusion.** Eigenvalue/eigenfunction properties can be structurally fragile: the property may hold exactly on a measure-zero set and fail immediately in any neighborhood.

"Mechanism works for exact X" does NOT imply "mechanism works for near-X."

## Evidence

**vasseur-pressure explorations E006-E007-E010** — The Beltrami-De Giorgi mechanism was the strongest positive result in Strategy-001:
- E006: Exact Beltrami flows have L=0, zero CZ loss, p = -|u|^2/2 (analytically derived)
- E007: The De Giorgi truncation u_below preserves Beltrami structure: B_k = O(2^{-k}) (computed)
- E010: Perturbed-ABC (eps=0.01 to 0.50) shows B_k decay is **destroyed for any eps > 0**. Even 1% perturbation creates a floor in B_k. beta_eff drops below 1 for eps >= 0.05.

Without E010, the final report would have overclaimed the Beltrami connection as a promising regularity mechanism. With E010, the connection is correctly scoped as analytically novel but practically limited to a measure-zero set.

## Physical Mechanism of Fragility

The curl eigenvalue equation curl(u) = lambda*u defines a measure-zero set. The property that truncation-level quantities decay geometrically depends on the non-eigenstate component existing ONLY at the clipping boundary (which vanishes as the clipping level increases). For any perturbation, the non-eigenstate component exists at ALL magnitudes and cannot be removed by truncation. This is a generic fragility pattern for eigenfunction properties.

## The Check

Before treating a positive finding as a strategy conclusion:

1. **Identify whether the finding was demonstrated on a special case** (exact eigenstate, exact symmetry, exact solution, measure-zero set)
2. **If yes, design a perturbation sweep** (eps = 0.01, 0.05, 0.1, 0.2, 0.5) testing the same property
3. **Look for:** continuous degradation (suggests fragility), threshold behavior (suggests robustness), or plateau (suggests partial survival)
4. **Report the mechanism as "exact-case specific" or "robust" based on the sweep results**

Cost: one additional exploration. Payoff: prevents overclaiming in the final report.

## Distinction from Related Entries

- **`verify-identity-generalization-before-extending.md`** — That entry is about testing whether algebraic identities generalize to larger spaces before attempting a proof extension. This entry is about testing whether empirical/computational mechanisms generalize to perturbed initial conditions before drawing strategy conclusions. Different triggers (proof extension vs. strategy conclusion), different checks (identity test vs. perturbation sweep).
- **`adversarial-check-between-phases.md`** — The adversarial review IDENTIFIED the need for this test (E009 flagged Claim 5 as weakest). This entry is about the FOLLOW-UP test itself. The adversarial review is the diagnostic; this perturbation sweep is the treatment.
- **`distinguish-typical-vs-worst-case-bounds.md`** — Related in spirit (correctly classifying what a result actually shows) but that entry is about bounds vs. values; this is about exact-case vs. generic-case mechanisms.
