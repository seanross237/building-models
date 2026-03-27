---
topic: gravitize-the-quantum
confidence: provisional
date: 2026-03-26
source: exploration-007-scg-v2-causal-order (quantum-gravity-2 strategy-001)
---

# SCG v2.0: Causal Order Rewrite

## Summary

Major rewrite of SCG's axioms to fix the **fatal Lorentzian signature problem** identified by the [adversarial assessment](scg-adversarial-assessment.md). The symmetric cost function (Axiom 3) is replaced with a causal partial order + directed cost + volume measure, drawing on causal set theory's "Order + Number = Geometry" principle and the Malament-Hawking-King-McCarthy theorem. The repair eliminates the fatal flaw and strengthens the Jacobson bridge, but leaves four near-fatal/serious problems untouched and introduces two new moderate gaps.

**Verdict:** SCG moves from "dead on arrival" (v1.0) to "alive but wounded" (v2.0) — roughly on par with other QG research programs (causal sets, CDT). This is genuine progress: "structurally broken" → "ambitious but unproven."

## v2.0 Axiom Changes

| Axiom | v1.0 | v2.0 | Change |
|---|---|---|---|
| A1. Configuration Space | Finite set Ω | Same | None |
| A2. Stochastic Dynamics | Indivisible process | Same (directedness emphasized) | Cosmetic |
| A3. Cost → **Causal Structure** | Symmetric metric c(x,y) | **Partial order ≺ + directed cost c(x,y) for x≺y + volume measure v(x)** | **Major rewrite** |
| A4. Optimization | Extremize total cost | Extremize cost along **causal paths** | Adjusted |
| A5. Irreducible Noise | Noise amplitude σ | Same | None |

### New Axiom 3 (Causal Structure) — Three Components

**(a) Partial order ≺** (reflexive, antisymmetric, transitive): represents causal precedence. Locally finite: causal intervals {z : x ≺ z ≺ y} are finite. Discrete analog of the causal relation J⁺ on a Lorentzian manifold.

**(b) Directed cost c(x,y) ≥ 0**, defined **only** when x ≺ y:
- c(x,x) = 0
- c(x,z) ≤ c(x,y) + c(y,z) when x ≺ y ≺ z (directed triangle inequality)
- NOT symmetric: c(x,y) defined when x ≺ y, but c(y,x) need not exist at all

**(c) Volume measure v: Ω → ℝ₊**: positive volume per configuration.

### What the Triple (≺, c, v) Encodes

| Component | Continuum Analog | Determines |
|---|---|---|
| Partial order ≺ | Causal relation J⁺ | Conformal geometry (light cones) |
| Directed cost c(x,y) | Proper time along timelike curves | Temporal separation |
| Volume measure v(x) | √(-det g) d⁴x | Conformal factor |

**Mathematical basis:** The Malament-Hawking-King-McCarthy theorem (Hawking et al. 1976, Malament 1977) proves that the causal order of a future-and-past-distinguishing spacetime determines its conformal geometry. The volume measure supplies the conformal factor via Sorkin's "Order + Number = Geometry."

### Axiom 4 Adjustment

Optimization restricted to **causal chains** x₁ ≺ x₂ ≺ ... ≺ xₖ. Cost functional: C[γ] = Σ c(xᵢ, xᵢ₊₁). In the continuum limit: extremizing directed cost along causal paths → **maximizing proper time** (timelike geodesics in Lorentzian geometry). This is the correct variational principle — physical trajectories maximize proper time (twin paradox). The sign flip from v1.0 (minimizing symmetric distance → maximizing directed proper time) is structurally natural.

## Derivation Chain Survival

| Chain | Status | Notes |
|---|---|---|
| QM Emergence (Barandes) | **Survives** | Directed transitions compatible by construction; lifting requires only indivisible stochastic process on finite set |
| Geometry (Pedraza) | **Improved but still gapped** | Signature mismatch eliminated; Lorentzian threads (Pedraza 2022) naturally compatible; Pedraza still only proven in 2D, CV ambiguity persists |
| Bridge (Jacobson) | **Strengthened** | Jacobson's derivation requires causal horizons, Unruh temperature, null surfaces — all require Lorentzian causal structure, now provided by Axiom 3 |
| Collapse (Diósi-Penrose) | **Unaffected** | Depends on weak-field gravitational potential, independent of signature |

## What the Repair Fixes

1. **FATAL → Resolved: Lorentzian signature.** Partial order encodes light cone structure; directed cost gives proper time; volume measure gives conformal factor. Signature built into causal order, not emergent from metric space. Same strategy as CST and CDT (both successfully produce Lorentzian geometry).

2. **SERIOUS → Resolved: Hyperbolic vs. elliptic operators.** Causal order gives hyperbolic structure: information propagates only along the partial order, not across spacelike gaps. Finite propagation speed by construction.

3. **MODERATE → Resolved: Jacobson mismatch.** Jacobson's thermodynamic derivation requires causal horizons. v1.0 awkwardly grafted onto Riemannian substrate; v2.0 provides exactly the structure Jacobson needs.

4. **CDT-like dimension selection becomes possible.** CDT shows imposing causality (global time foliation) makes 4D emerge dynamically. v2.0's causal structure opens this door, though dimension selection remains unproven.

## What Remains Broken

| Issue | v1.0 Severity | v2.0 Severity | Change |
|---|---|---|---|
| Lorentzian signature | FATAL | **Resolved** | ✓ Fixed |
| QM reformulation, not derivation | NEAR-FATAL | NEAR-FATAL | Unchanged |
| Continuum limit unproven | NEAR-FATAL | NEAR-FATAL | Type changed (Riemannian → Lorentzian) |
| Pedraza only 2D | NEAR-FATAL | NEAR-FATAL | Slightly improved (signature alignment) |
| No unique predictions | SERIOUS | SERIOUS | Unchanged (arguably worsened — more similar to CST now) |
| Self-consistency unproven | SERIOUS | SERIOUS | Slightly improved in plausibility |
| Oppenheim not derived | SERIOUS | SERIOUS | Unchanged |
| ℏ renaming | MODERATE | MODERATE | Unchanged |
| Ontology issues | MODERATE | MODERATE | Slightly improved (Ω now a causet) |
| **Volume measure origin (NEW)** | — | MODERATE | New free function with no specified origin |
| **Partial order origin (NEW)** | — | MODERATE | Postulating causal order on pre-geometric space may put spacetime in by hand |

### New Problem: Volume Measure

v(x) is an additional input v1.0 didn't need. In CST, volume comes from sprinkling density (one element per Planck volume). In SCG, the configuration space is a given finite set with no sprinkling — volume measure is a free function with no specified origin.

### New Problem: Partial Order Origin

Why should Ω have a partial order? In CST, the partial order IS the fundamental structure. In SCG, Ω is supposed to be pre-geometric. Postulating causal order on the pre-geometric space may put spacetime structure in by hand rather than deriving it. Conflates causal order with dynamical constraint (similar to prescriptive/descriptive ambiguity of adversarial Attack 7.5).

## Largest Remaining Risk

**QM emergence (Attack 1).** The causal order repair doesn't touch this at all. If the Barandes-Doukas lifting is truly just a reformulation, SCG doesn't derive QM — it assumes it under a different name. This may be the deepest problem in the framework.

## Cross-References

- [scg-theory-construction.md](scg-theory-construction.md) — v1.0 axioms and full theory description
- [scg-adversarial-assessment.md](scg-adversarial-assessment.md) — The attack that identified the fatal Lorentzian flaw
- [../causal-set-theory/core-idea.md](../causal-set-theory/core-idea.md) — "Order + Number = Geometry" principle borrowed for v2.0
- [../causal-set-theory/lorentz-invariance.md](../causal-set-theory/lorentz-invariance.md) — Bombelli-Henson-Sorkin theorem preserving Lorentz invariance
- [barandes-verlinde-stochastic-emergence.md](barandes-verlinde-stochastic-emergence.md) — QM emergence chain (survives v2.0)
