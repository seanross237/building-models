---
topic: cross-cutting
confidence: verified
date: 2026-03-25
source: exploration-004-cost-function-ghost-freedom (quantum-gravity-2 strategy-001)
---

# Cost Function Constraints Cannot Select Ghost-Free Gravity (QG+F)

## Summary

Can cost function constraints in the Pedraza et al. spacetime complexity framework select ghost-free higher-derivative gravity — specifically QG+F (quadratic gravity with fakeon quantization)? **No.** The investigation reveals a clear negative result with four precise reasons. This directly addresses the SCG program's "most promising next direction" and finds it blocked at a fundamental level.

## The Pedraza et al. Spacetime Complexity Framework

**Key paper:** Carrasco, Pedraza, Svesko, Weller-Davies, "Gravitation from optimized computation: Einstein and beyond," JHEP 09 (2023) 167 (arXiv: 2306.08503).

**Core claim:** Gravitational physics emerges from spacetime seeking to optimize the computational cost of its quantum dynamics. Einstein's equations are equivalent to requiring that CV (Complexity=Volume) complexity responds consistently to state perturbations.

**The CV complexity functional:**

    C_gen = (1/(G_N L)) ∫_Σ d^{D-1}σ √h F₁(g_μν, Φ, X^μ)

where Σ is a codimension-one extremal hypersurface, h is the induced metric, and F₁ is the **cost function** — a scalar depending on the bulk metric, dilaton, and embedding coordinates.

**How Einstein equations emerge:** Via the covariant phase space formalism — defining W[g_μν, Φ] as the complexity on the extremal slice, the symplectic form relates bulk and boundary variations. Requiring δW to satisfy the first law of complexity for ALL variations imposes the linearized Einstein equations around pure AdS. Proven fully in 2D dilaton gravity (JT gravity).

### Cost Function → Higher-Derivative Gravity Mapping

Modified cost functions with curvature-dependent terms yield higher-derivative gravitational equations:

    F₁(r) = 1 + λ L⁴ × (curvature scalar)

The mapping:
- F₁ ∝ 1 + λ R_μν R^μν → gravity with Ricci-squared correction
- F₁ ∝ 1 + λ C_μνρσ² → gravity with Weyl-squared correction (→ spin-2 sector/ghost)
- F₁ ∝ 1 + λ R_μνρσ² → gravity with Gauss-Bonnet-type correction

This maps directly to QG+F particle content: **C² controls the massive spin-2 fakeon, R² controls the massive spin-0.**

## The "Complexity = Anything" Framework

The Belin et al. (2021) and Jorstad-Myers-Ruan (arXiv: 2503.20943, March 2025) "complexity = anything" framework establishes:

- **Infinite class of equally viable complexity functionals** — different F₁ correspond to different "gate sets" in the dual quantum circuit
- **Complexity is scheme-dependent** — depends on choice of basis and gate costs
- F₁ need not equal the extremizing functional F₂

**Constraints on valid complexity measures** (all IR/macroscopic):
1. Linear growth at late times (effective potential has interior maximum)
2. Switchback effect (additive for shockwaves)
3. Diffeomorphism invariance (F must be a scalar)
4. Physical well-definedness (finite at horizons)
5. Positivity (effective potential not globally negative)

## The Negative Result: Four Reasons

### Reason 1: Too Much Freedom

The "complexity = anything" framework demonstrates an infinite class of valid complexity functionals. The constraints (linear growth, switchback, diffeomorphism invariance, positivity) are necessary but far from sufficient to select a unique gravitational theory. Different cost functions correspond to different gate sets, not different gravitational theories.

### Reason 2: Wrong Direction of Inference

The framework maps FROM bulk gravity TO complexity: given a gravitational theory, find the matching complexity functional. The reverse mapping is **degenerate** — many cost functions are compatible with many theories. The cost function ENCODES the gravitational theory rather than SELECTING it.

### Reason 3: Classical vs. Quantum (Most Fundamental)

The cost function is a **classical geometric object**. The fakeon prescription is a **quantum mechanical choice** about how to handle propagator poles. The QG+F Lagrangian is IDENTICAL to Stelle's Lagrangian: L = R + αC² + βR². The difference is purely in quantization (Feynman contour vs. fakeon contour). No classical cost function can distinguish between Stelle gravity and QG+F because their classical geometries are the same.

**This is the deepest obstruction:** the cost function determines classical geometry; the fakeon prescription determines how to quantize excitations around that geometry. These are distinct layers of structure.

### Reason 4: IR vs. UV Mismatch

The known complexity constraints (linear growth, switchback) are **infrared/macroscopic** properties. Ghost-freedom is an **ultraviolet/microscopic** property. There is no established mapping between the two regimes.

## The Positive-Definiteness Lead (Incomplete)

The most promising potential route comes from the **landscape/swampland structure of complexity penalty factors** (Flory et al. 2026, JHEP 02):

- In the Nielsen complexity framework, the penalty factor matrix I_IJ defines the cost: F² = Y^I I_IJ Y^J
- Only **positive-definite** penalty matrices give viable complexity measures
- Indefinite penalty factors → physically meaningless complexity ("swampland")
- This is **structurally analogous** to ghost-freedom: ghosts (negative-residue poles) ↔ indefinite complexity metrics

**Why the analogy fails (currently):**
1. **Level mismatch:** Nielsen complexity geometry lives on the boundary (CFT); ghost question is about the bulk propagator. No established mapping between boundary complexity metric signature and bulk propagator pole residues.
2. **Object mismatch:** Cost function F₁ ≠ gravitational Lagrangian L_grav. "F₁ well-defined" ≠ "L_grav ghost-free."
3. **Freedom absorbs it:** Even with positive-definiteness, "complexity = anything" gives infinitely many valid choices corresponding to gate sets, not gravitational theories.

## What Would Be Needed

To make cost function constraints select QG+F, four gaps must be bridged:

1. **UV-sensitive complexity constraint** — probing short-distance structure, not just long-distance growth
2. **Holographic propagator-complexity dictionary** — mapping bulk propagator pole residues to boundary complexity metric properties (does not currently exist)
3. **Quantization-sensitive boundary observable** — distinguishing Feynman from fakeon quantization in the bulk (most holographic observables are determined by classical bulk geometry, which is identical for both)
4. **Positive-definiteness theorem** — proving that bulk ghosts induce indefinite boundary complexity metrics

A "quantum cost function" that directly constrains propagator structure (not just classical geometry) would be a significant extension of the current framework.

## Alternative Holographic Mechanisms (Partial Constraints)

While cost functions don't work, other holographic mechanisms DO constrain bulk higher-derivative gravity:

- **Conformal collider bounds** (Hofman-Maldacena 2008, Buchel et al. 2010): Positivity of energy flux in CFT constrains a/c ratio, bounding Weyl-squared and Gauss-Bonnet couplings
- **Causality constraints:** Bulk causality ↔ boundary causality bounds higher-derivative couplings
- **Conformal bootstrap / swampland conditions** (Caron-Huot et al. 2022): Positivity, monotonicity, log-convexity of higher-derivative couplings from bootstrap axioms

These provide **sign and magnitude bounds** on couplings α and β, but:
- Give ranges, not unique values
- Do NOT distinguish Feynman from fakeon quantization (constrain classical Lagrangian only)
- Apply only in the holographic (large-N) regime with higher-derivative terms perturbatively small

## Cross-References

- [../../gravitize-the-quantum/scg-theory-construction.md](../../gravitize-the-quantum/scg-theory-construction.md) — SCG uses Pedraza cost optimization as one route to Einstein equations; this negative result blocks the "most promising next direction" identified there
- [entanglement-gravity-bootstrap.md](entanglement-gravity-bootstrap.md) — Alternative information-theoretic route that DOES uniquely produce QG+F (via MVEH + renormalizability + unitarity)
- [information-theoretic-constructive-axioms.md](information-theoretic-constructive-axioms.md) — Broader landscape of info-theoretic axioms for QG construction

## Key References

- Carrasco, Pedraza, Svesko, Weller-Davies, JHEP 09 (2023) 167. arXiv: 2306.08503.
- Jorstad, Myers, Ruan, arXiv: 2503.20943 (2025).
- Flory et al., JHEP 02 (2026) 247. arXiv: 2507.22118.
- Hofman, Maldacena, JHEP 05 (2008) 012.
- Caron-Huot et al., JHEP 01 (2022) 176.
