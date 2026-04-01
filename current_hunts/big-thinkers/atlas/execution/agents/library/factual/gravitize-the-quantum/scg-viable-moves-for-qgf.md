---
topic: gravitize-the-quantum
confidence: provisional
date: 2026-03-26
source: exploration-002-scg-conceptual-moves (quantum-gravity-2 strategy-002)
---

# Viable Conceptual Moves from SCG for QG+F Theory Construction

## Summary

Systematic extraction of conceptual raw materials from SCG v2.0 that could power novel theory construction targeting QG+F's explanatory gaps — especially the fakeon interpretation cluster (#1) and non-perturbative completion (#2). Six moves assessed for viability and novelty, plus one new move from the information-theoretic direction. Five hard constraints from strategy-001 negative results limit the solution space.

## Move Catalog

### Move 1: Computational Cost as Physical Interpretation of the Fakeon

**Idea:** Pedraza et al. (2023) shows δC/δg = 0 gives Einstein equations. If gravity IS cost optimization, the fakeon reflects a computational constraint — certain modes are "computationally forbidden" because they violate the optimization. The fakeon is a "dead branch" in the computation: contributes to cost accounting (loop integrals) but never manifests as a physical process (no asymptotic state).

**Target gap:** #1 (Fakeon Interpretation) — DIRECT.
**Novelty:** 7/10. The specific "fakeon = computationally forbidden mode" connection is new.
**Key obstacle:** Classical cost functions CANNOT distinguish Stelle gravity from QG+F. A "quantum cost function" constraining propagator structure (not just Lagrangians) would be needed.
**Viability:** MODERATE-HIGH. Obstacle clear but potentially attackable.

### Move 2: Indivisibility as the Origin of the Fakeon Prescription

**Idea:** Barandes-Doukas shows QM IS the mathematical description of "indivisible" stochastic processes — processes whose multi-time correlations can't decompose into sequential steps. The fakeon also enforces indivisibility: the massive spin-2 mode can't be separated into real particle production. Perhaps the fakeon is the gravitational manifestation of stochastic indivisibility — modes requiring decomposition into real intermediate states are forbidden because the underlying process is indivisible.

**Target gaps:** #1 (Fakeon Interpretation) — DIRECT; #2 (Non-Perturbative Completion) — ghost confinement as fully indivisible stochastic gravitational process.
**Novelty:** 8/10. "Fakeon = gravitational indivisibility" is genuinely new.
**Key obstacle:** Barandes lifting is isomorphism, not derivation. If "indivisibility → fakeon" is just "QM → fakeon" with extra steps, it's not explanatory. Must pass the Aaronson test. Critical check: can indivisibility constraints PREDICT which modes must be fakeons?
**Viability:** MODERATE. Conceptually appealing but risks reformulation.
**Full development:** See [`../quadratic-gravity-fakeon/indivisibility-fakeon-interpretation.md`](../quadratic-gravity-fakeon/indivisibility-fakeon-interpretation.md) — full mechanism, analyticity sacrifice explanation, measurement problem connection, devil's advocate (primarily interpretive, no QFT extension).

### Move 3: Irreducible Noise as Microcausality Violation

**Idea:** SCG's Axiom 5 (irreducible noise σ > 0) breaks strict commutativity — events at "spacelike separation" connected through noise channels. QG+F's microcausality violation means fields don't commute below Planck scale. Stochastic spacetime fluctuations at σ ~ 1/M₂ naturally produce the commutator corrections.

**Target gap:** #1 (Fakeon Interpretation) — INDIRECT (via microcausality).
**Novelty:** 5/10. Stochastic gravity (Hu-Verdaguer) has explored noise effects for decades.
**Key obstacle:** QG+F's microcausality violation is mathematically precise (fakeon propagator); noise effects are phenomenological. Mapping requires showing identical mathematical structure.
**Viability:** LOW-MODERATE.

### Move 4: Finite Configuration Space as Non-Perturbative Regulator

**Idea:** SCG posits finite Ω with N ~ e^{10^{122}} states. If QG+F is the continuum limit of a theory on finite configuration space, this provides the non-perturbative definition the theory lacks. Ghost confinement as finite-N effect: on finite space the ghost mode is automatically bounded.

**Target gaps:** #2 (Non-Perturbative Completion) — DIRECT; #1 (Fakeon Interpretation) — fakeon as perturbative shadow of mode confined to finite regions.
**Novelty:** 6/10. Gravity on finite config spaces exists in CDT/CST; ghost confinement connection somewhat novel.
**Key obstacle:** SCG's continuum limit is unproven; generic cost functions don't give manifolds (Gromov-Hausdorff); no 4D mechanism.
**Viability:** LOW. Multi-decade research program, not a sprint target.

### Move 5: Causal Order as the Fakeon's Origin

**Idea:** SCG v2.0 replaced symmetric cost with causal partial order + directed cost + volume measure. Via Malament's theorem, causal order determines conformal geometry. The fakeon breaks time-reversal symmetry in the propagator. Perhaps the fakeon IS the gravitational manifestation of causal order — the prescription respecting the partial order structure of spacetime. The analyticity sacrifice (no analytic S-matrix) corresponds to non-analyticity of causal structure (discrete, non-smooth relation).

**Connection to Anselmi's 2026 causality essay:** Anselmi proposes ABANDONING causality; this proposes causality as the ORIGIN. Possibly complementary: fakeon violates microcausality BECAUSE it enforces macro-causality.

**Target gap:** #1 (Fakeon Interpretation) — DIRECT.
**Novelty:** 7/10. "Causal order → fakeon" not proposed explicitly.
**Key obstacle:** Same classical → quantum gap. How does classical causal order constrain quantum propagator? But: both are GLOBAL constraints (causal order is global; fakeon modifies integration contour for all momenta). Global ↔ global matching may be tractable.
**Viability:** MODERATE-HIGH. Conceptually strongest of all moves.
**Full development:** See [`../quadratic-gravity-fakeon/causal-order-fakeon-interpretation.md`](../quadratic-gravity-fakeon/causal-order-fakeon-interpretation.md) — Wheeler propagator = fakeon connection, Belenchia et al. causal set bridge, SJ vacuum mechanism, loop-level gap analysis, devil's advocate.

### Move 6: Complexity Plateau as Singularity Resolution

**Idea:** Spacetime complexity saturates at maximum value, replacing classical singularity with "complexity wall." In QG+F, the fakeon selects Schwarzschild but stays silent about the singularity. Extended Pedraza cost optimization would saturate at extreme curvatures.

**Target gap:** #4 (Black Hole Interior) — DIRECT but off-target from primary Gap #1.
**Novelty:** 4/10. Complexity saturation discussed by Susskind, Brown-Susskind.
**Key obstacle:** Pedraza only 2D; targets wrong gap.
**Viability:** LOW for primary targets.

### Move 7 (New): Information-Theoretic Fakeon from Entanglement Structure

**Idea:** The fakeon is REQUIRED for consistent entanglement structure across horizons. The MVEH construction (maximal vacuum entanglement → QG+F) already hints: modular flow unitarity demands the fakeon. Push further: the fakeon prevents entanglement entropy from diverging in the UV. The analyticity sacrifice IS the entanglement area law — the non-analyticity of the S-matrix reflects finite entanglement capacity of spacetime regions.

**Target gaps:** #1 (Fakeon Interpretation) + #5 (Gravitational Thermodynamics).
**Novelty:** HIGH — extends the most rigorous existing MVEH → QG+F result.
**Key obstacle:** MVEH only gives linearized results (Bueno et al. 2017). Extension to nonlinear may hit barriers.
**Viability:** MODERATE-HIGH. Directly builds on established mathematical results.
**Full development:** See [`../quadratic-gravity-fakeon/entanglement-structure-fakeon-interpretation.md`](../quadratic-gravity-fakeon/entanglement-structure-fakeon-interpretation.md) — ghost entanglement pathology (Jatkar-Narayan), MVEH self-consistency loop, analyticity as informational area law, structural prediction, devil's advocate.

## Viability Rankings

| Move | Target | Novelty | Viability | Best For |
|------|--------|---------|-----------|----------|
| 5. Causal Order | Gap #1 | 7/10 | MODERATE-HIGH | Conceptually cleanest, global-global matching |
| 7. Entanglement | Gap #1 + #5 | HIGH | MODERATE-HIGH | Extends rigorous MVEH result |
| 2. Indivisibility | Gap #1 + #2 | 8/10 | MODERATE | Highest novelty, addresses two gaps |
| 1. Computational Cost | Gap #1 | 7/10 | MODERATE-HIGH | Clearest technical path, deepest obstacle |
| 3. Noise | Gap #1 | 5/10 | LOW-MODERATE | Well-trodden framework |
| 4. Finite Config | Gap #2 | 6/10 | LOW | Too hard for sprint |
| 6. Complexity | Gap #4 | 4/10 | LOW | Off-target |

## Critical Constraint: The Classical → Quantum Gap

The deepest obstruction shared by Moves 1, 4, 5, and 6: classical structures (cost functions, variational principles, causal orders) cannot distinguish Stelle gravity from QG+F because the Lagrangian is IDENTICAL. The fakeon is a quantization choice. Any theory built on Move 1-6 must bridge from classical to quantum — the novel mechanism must be quantum from the start.

Move 2 (indivisibility) and Move 7 (entanglement) are the only moves that start quantum. This may make them structurally favored despite other obstacles.

## Cross-References

- [scg-theory-construction.md](scg-theory-construction.md) — Source: SCG axioms and derivation chains
- [scg-adversarial-assessment.md](scg-adversarial-assessment.md) — Source: weaknesses informing obstacle analysis
- [scg-v2-causal-order-rewrite.md](scg-v2-causal-order-rewrite.md) — Source: causal order innovation powering Move 5
- [barandes-verlinde-stochastic-emergence.md](barandes-verlinde-stochastic-emergence.md) — Source: indivisibility concept powering Move 2
- [../quadratic-gravity-fakeon/explanatory-debts-catalog.md](../quadratic-gravity-fakeon/explanatory-debts-catalog.md) — Target: the gaps these moves address
- [../cross-cutting/cost-function-ghost-selection-negative.md](../cross-cutting/cost-function-ghost-selection-negative.md) — Constraint: classical costs can't select QG+F
- [../cross-cutting/entanglement-gravity-bootstrap.md](../cross-cutting/entanglement-gravity-bootstrap.md) — Foundation for Move 7 (MVEH → QG+F)
- [../quadratic-gravity-fakeon/analyticity-sacrifice.md](../quadratic-gravity-fakeon/analyticity-sacrifice.md) — Context: the analyticity sacrifice Moves 5 and 7 interpret
