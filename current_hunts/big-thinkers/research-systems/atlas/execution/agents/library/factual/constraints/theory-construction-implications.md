---
topic: constraints/analysis
confidence: verified
date: 2026-03-24
source: exploration-001-structural-recovery-constraints
---

# Implications of the Constraint Catalog for Novel Theory Construction

## The Constraint Funnel

Working top-down through the most restrictive constraints:

1. **UV completion** forces a non-perturbative mechanism (rules out naive QFT of gravity)
2. **Unitarity + ghost freedom** creates tension with higher-derivative approaches (must be resolved by string-like UV completion, asymptotic safety, fundamental discreteness, or infinite-derivative mechanism)
3. **Diffeomorphism invariance** uniquely fixes the low-energy structure of graviton interactions
4. **Lorentz invariance** rules out O(1) Planck-scale violations — the theory must be Lorentz-invariant or violations must be extraordinarily suppressed
5. **Bekenstein-Hawking entropy** requires the theory to have the right microscopic degrees of freedom to account for horizon entropy as area/4G
6. **GW speed = c** eliminates many modified gravity alternatives
7. **Spectral dimension running** provides a UV target: the theory should become effectively 2-dimensional at short distances

## The Narrowest Bottleneck

The **unitarity-renormalizability tension** remains the single tightest bottleneck. The known escape routes define the major programs:
- **String theory:** UV-finite amplitudes, no higher-derivative ghosts
- **Asymptotic safety:** Non-perturbative fixed point, possible fictitious ghosts
- **LQG:** Fundamentally discrete, sidesteps continuum divergences
- **IDG:** Entire functions in the propagator, no new poles

Any novel approach must identify its own escape route through this bottleneck.

## Underexploited Constraints (Potential Starting Axioms)

The following constraints are powerful but underused in theory construction — they are typically checked after the fact rather than used as starting axioms:

1. **Spectral dimension d_s → 2** — **has been explored as a constructive axiom** (exploration-002): starting from d_s = 2 + Lorentz invariance + diffeomorphism invariance + renormalizability uniquely selects Stelle quadratic gravity with fakeon quantization, with only 2 free parameters beyond GR. See `quadratic-gravity-fakeon/core-idea.md` and `constraints/structural/ghost-spectral-dimension-no-go.md`. The systematic escape routes from this selection have been mapped — see `constraints/escape-routes-from-no-go.md`.
2. **Jacobson's derivation** — the fact that Einstein equations follow from thermodynamics of local horizons is rarely used as a constructive principle for building new theories. The maximal vacuum entanglement hypothesis (Jacobson 2015) could be extended to the UV by specifying a particular Planck-scale entanglement structure, generating modified gravitational equations.
3. **Entanglement area law** — the Ryu-Takayanagi connection between entanglement and geometry could be promoted from a result to an axiom
4. **Holographic Swampland unification** — the 2025 result that all Swampland conjectures derive from a single geometric condition on holographic effective action convexity is a potentially powerful organizing principle
5. **Information-theoretic axioms** — four specific axioms have been identified as the most promising alternative foundations for novel QG theory construction: positivity of relative entropy, maximal vacuum entanglement, quantum focusing condition, and the entropic action principle. None has been used to construct a UV-complete theory. See `cross-cutting/information-theoretic-constructive-axioms.md`.

## Implication for Research Strategy

The constraint funnel suggests a concrete approach for evaluating novel constructions: check the independent constraints first (unitarity, diffeomorphism invariance, UV completion, Lorentz invariance, BH entropy), since failure on any of these is fatal. Derived constraints can be checked afterward as consistency checks.
