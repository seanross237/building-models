---
topic: gravitize-the-quantum
confidence: provisional
date: 2026-03-25
source: exploration-003-scg-theory-construction (quantum-gravity-2 strategy-001)
---

# Stochastic Computational Gravity (SCG): Theory Construction

## Summary

SCG is a unified axiomatic framework that derives both quantum mechanics and spacetime geometry from a single underlying entity: a stochastic computation on a finite configuration space with a cost function. Built from five axioms, it produces QM via the Barandes-Doukas lifting of indivisible stochastic processes, and produces spacetime geometry via the continuum limit of the cost function with Einstein equations from cost optimization. It extends the earlier [stochastic-spacetime-qm-synthesis](stochastic-spacetime-qm-synthesis.md) pipeline into a concrete theory with axioms, derivation chains, predictions, and gap analysis.

**Status (v1.0):** ~~Fatally flawed~~ — the symmetric cost function structurally cannot produce Lorentzian spacetime, per [adversarial assessment](scg-adversarial-assessment.md).

**Status (v2.0):** **Alive but wounded.** The [v2.0 causal order rewrite](scg-v2-causal-order-rewrite.md) replaces Axiom 3 with a causal partial order + directed cost + volume measure, directly fixing the fatal Lorentzian signature flaw. Three near-fatal problems remain (QM is reformulation, continuum limit unproven, Pedraza only 2D) plus no unique predictions. Roughly on par with other QG research programs.

## The Five Axioms

| # | Axiom | Content | Physical Motivation |
|---|-------|---------|-------------------|
| A1 | Configuration Space | Finite set Ω with \|Ω\| = N (astronomically large) | Bekenstein bound, holographic principle, dS entropy S_dS ≈ 10^122 → N ~ e^{10^{122}} |
| A2 | Stochastic Dynamics | Indivisible stochastic process {Γ(τ₂\|τ₁)} on Ω; Γ(τ₃\|τ₁) ≠ Γ(τ₃\|τ₂)·Γ(τ₂\|τ₁) | Irreducible randomness; indivisibility forces quantum description |
| A3 | Cost Function | Metric c: Ω×Ω → ℝ≥0 (non-negative, symmetric, triangle inequality) | Pre-geometric distance; nearby configs cheap, distant expensive |
| A4 | Optimization | Macroscopic dynamics extremizes total cost C[γ] = ∫c dτ | Computational analog of least action |
| A5 | Irreducible Noise | Fundamental noise amplitude σ > 0; not epistemic | Physical source of quantum randomness |

The axioms are logically independent. They do NOT assume Hilbert space, spacetime manifold, metric tensor, ℏ, G, or specific dimensionality — all emerge.

## QM Emergence (Barandes-Doukas Lifting)

**Pipeline:** Indivisible stochastic process → Barandes-Doukas lifting → Hilbert space ℂ^N, density matrices, CPTP maps, Born rule

**Key result (Barandes 2023; Doukas 2025):** Every indivisible stochastic process on N configurations lifts to quantum channels on ℂ^N. Off-diagonal density matrix elements encode the multi-time memory that makes the process indivisible. Quantum phase = compressed encoding of multi-time stochastic memory.

**Emergence of ℏ:** In the continuum limit, stochastic diffusion with coefficient D = σ² maps to Nelson's stochastic mechanics with **ℏ = 2mσ²**, where m is the "inertial cost" (cost-per-unit-displacement). Different particles have different m but same σ → same ℏ.

| QM Concept | SCG Origin |
|---|---|
| Hilbert space ℂ^N | Lifting of indivisible stochastic process |
| Wave function | Efficient encoding of multi-time correlations |
| Quantum phase | Compressed multi-time stochastic memory |
| Born rule | Diagonal elements of lifted density matrix |
| Unitary evolution | Time-reversal symmetric stochastic dynamics |
| Entanglement | Correlations between subsystem stochastic processes |
| ℏ | 2mσ² (noise amplitude × inertial cost) |
| Collapse/decoherence | Loss of multi-time memory → Markovian dynamics |

## Geometry Emergence (Cost → Metric → Einstein)

**Pipeline:** Cost function c on Ω → finite metric space → continuum limit → Riemannian manifold (M, g) → cost optimization → Einstein equations

**Continuum limit:** As N → ∞, coarse-graining groups nearby configurations into patches. Cost between patches → smooth metric tensor g_μν. Path cost C[γ] = ∫√(g_μν ẋ^μ ẋ^ν)dτ = geodesic length. Cheapest paths = geodesics.

**Two independent routes to Einstein equations:**

1. **Pedraza cost optimization:** Total computational cost ∝ spacetime volume (CV correspondence). Varying δC/δg_μν = 0 yields G_μν + Λg_μν = 8πG T_μν. Rigorously demonstrated for 2D dilaton gravity (JHEP).

2. **Jacobson thermodynamic:** Clausius relation δQ = TdS + Unruh temperature + Bekenstein-Hawking entropy → Einstein equations. Each ingredient has SCG stochastic-computational origin. Second, independent derivation = consistency check.

| Geometric Concept | SCG Origin |
|---|---|
| Metric tensor g_μν | Coarse-grained cost function |
| Geodesics | Cheapest paths through configuration space |
| Einstein equations | Cost optimization (Pedraza) OR thermodynamic (Jacobson) |
| Newton's constant G | Cost-to-volume conversion: G ∝ σ²/c_typ² |
| Cosmological constant Λ | Maximum complexity: Λ ~ πG/ln(C_max) |
| Curvature | Non-uniformity of cost function |
| Higher-derivative corrections | Higher-order terms in cost function |

**Lorentzian signature:** Cost function is positive-definite → naturally Riemannian. Lorentzian signature requires distinguishing temporal from spatial costs. Emergence of Lorentzian sign is an **open problem**.

**Dimensionality:** NOT predicted by axioms. Depends on cost function structure. Getting d = 4 is a non-trivial requirement — an **open problem**.

## The Gravity-QM Bridge

**Self-consistency condition:** QM and geometry emerge from the SAME stochastic computation. The theory is self-consistent iff the geometry produced by cost optimization is compatible with the stochastic process that lives on it. This is a fixed-point condition (analogous to Hartree-Fock, Einstein equations, AdS/CFT).

**Diósi-Penrose collapse:** Extended superpositions are unstable because cost optimization (A4) favors lower-cost branches. Collapse timescale τ_collapse ~ ℏ/E_G emerges naturally. The same noise (A5) simultaneously produces decoherence (quantum → classical) and diffusion (metric fluctuations), inheriting Oppenheim's decoherence-diffusion trade-off: D_diffusion × τ_decoherence ≥ bound.

## Predictions Differing from GR and QG+F

| # | Prediction | vs. GR | vs. QG+F | Testability |
|---|-----------|--------|----------|-------------|
| 1 | No graviton | GR has no graviton either | QG+F predicts graviton with modified propagator | GIE experiments (Bose et al., Marletto-Vedral); subtle — stochastic correlations may mimic GIE |
| 2 | Spacetime diffusion | No stochastic metric fluctuations in GR | Not present in QG+F | LIGO/LISA could constrain |
| 3 | Decoherence-diffusion trade-off | No trade-off | No trade-off | Current experiments converging — could confirm/constrain within a decade |
| 4 | Complexity plateau (singularity resolution) | GR has true singularities | QG+F singularity not resolved perturbatively | Not directly testable (t ~ e^S timescale) |
| 5 | Modified dispersion relations | Standard E² = p²c² + m²c⁴ | Modified at Planck scale but different form | Fermi gamma-ray constraints |
| 6 | Higher-derivative gravity with predicted coefficients | Only Einstein-Hilbert | Coefficients free (f₀, f₂) | **Blocked:** cost function constraints cannot select ghost-free gravity — see cross-cutting/cost-function-ghost-selection-negative.md |

**Most testable near-term:** Decoherence-diffusion trade-off (prediction 3) — already being probed by atom interferometry + GW observations.

## Internal Consistency: Circularities Addressed

**Circularity 1 — QM needed for complexity, but complexity produces QM?** Resolved: SCG defines complexity as stochastic transition cost, not quantum circuit depth. Stochastic cost is prior to and independent of QM. Circuit complexity is a derived concept that agrees in the regime where QM is valid.

**Circularity 2 — Spacetime from complexity requires time?** Resolved: Pre-geometric process time τ (computation clock, part of A2) ≠ emergent spacetime time t (coordinate on M, part of output). τ parameterizes stochastic process; t emerges from cost function.

**Circularity 3 — "Which complexity?" ambiguity:** Resolved: Fundamental quantity is cost function c (A3), not derived complexity measures. Holographic CV/CA ambiguity arises from projecting underlying cost onto boundary — different projections of same cost.

## Honest Gaps (Unresolved Issues)

1. **Why 4 dimensions?** — Not predicted; depends on cost function structure
2. ~~**Lorentzian signature** — Positive-definite cost → Riemannian~~ **RESOLVED in v2.0** — causal partial order + directed cost + volume measure; see [scg-v2-causal-order-rewrite.md](scg-v2-causal-order-rewrite.md)
3. **Continuum limit not proven** — Smooth manifold from (Ω, c) is assumed, not a theorem
4. **Value of N** — Free parameter; Bekenstein motivation uses concepts supposed to be emergent
5. **No Standard Model** — No particle content, gauge groups, or coupling constants
6. **Why indivisible?** — A2 postulated, not derived; conjecture: non-trivial topology of cost space → non-Markovian memory
7. **Quantitative ℏ-G relation** — Schematic (ℏ = 2mσ², G ∝ σ²/c_typ²); numerical verification requires knowing exact cost function

## Comparison to Existing Programs

SCG is the **union** of multiple programs connected by common axioms:

| Program | What it does | What SCG adds |
|---|---|---|
| Barandes stochastic QM | Derives QM from stochastic processes | Geometry emergence from cost function |
| Oppenheim postquantum | Classical gravity + stochastic QM coupling | Geometry derivation from optimization |
| Pedraza complexity → gravity | Einstein eqns from complexity | QM derivation from same stochastic source |
| Nelson stochastic mechanics | QM ↔ diffusion | Physical source for the diffusion |
| Diósi-Penrose | Gravitational collapse | Collapse from cost optimization |
| Jacobson thermodynamic | Einstein eqns from entropy | Microscopic stochastic basis |

**Most promising next direction (BLOCKED):** Identifying cost functions that produce ghost-free higher-derivative gravity was the obvious next step, but exploration-004 showed this is fundamentally blocked: the cost function is a classical geometric object that cannot distinguish Stelle gravity from QG+F (identical Lagrangians, different quantization prescriptions). See [`cross-cutting/cost-function-ghost-selection-negative.md`](../cross-cutting/cost-function-ghost-selection-negative.md). The most promising remaining direction is developing a **quantum cost function** that constrains propagator structure, or connecting SCG to QG+F via the entanglement-gravity bootstrap route instead.

## Adversarial Assessment

A systematic devil's advocate attack (7 vectors, 11 ranked weaknesses) found SCG **does NOT survive** in its current form. See [`scg-adversarial-assessment.md`](scg-adversarial-assessment.md) for the full analysis. Key findings:

- **FATAL:** Lorentzian signature cannot emerge from positive-definite cost function (Axiom 3). This is a structural incompatibility, not a gap.
- **NEAR-FATAL:** QM emergence (Attack 1) is reformulation not derivation — Barandes-Doukas is an isomorphism, Born rule is definitional, phases undetermined, indivisibility may smuggle in QM.
- **NEAR-FATAL:** Continuum limit (Attack 2) unproven — generic cost functions don't give manifolds (Gromov-Hausdorff); no mechanism for 4D.
- **NEAR-FATAL:** Pedraza derivation (Attack 4) only proven in 2D dilaton gravity; depends on unproven CV conjecture and AdS/CFT.
- **SERIOUS:** No unique predictions — every prediction inherited from component programs.
- **SERIOUS:** Self-consistency fixed point asserted, not proven; may have no solution.

**What would elevate SCG:** (1) Solve Lorentzian signature, (2) prove continuum limit with dimension selection, (3) prove self-consistency exists, (4) make a unique prediction, (5) derive Oppenheim's equations from axioms.

## Cross-References

- [scg-adversarial-assessment.md](scg-adversarial-assessment.md) — **Comprehensive adversarial attack on v1.0; verdict: does not survive current form**
- [scg-v2-causal-order-rewrite.md](scg-v2-causal-order-rewrite.md) — **v2.0 rewrite fixing fatal Lorentzian flaw; verdict: alive but wounded**
- [scg-viable-moves-for-qgf.md](scg-viable-moves-for-qgf.md) — **Conceptual moves extracted from SCG for QG+F theory construction: 7 moves ranked by novelty/viability; top: causal order → fakeon, indivisibility → fakeon, entanglement-theoretic fakeon**
- [stochastic-spacetime-qm-synthesis.md](stochastic-spacetime-qm-synthesis.md) — Precursor synthesis pipeline that SCG axiomatizes
- [barandes-verlinde-stochastic-emergence.md](barandes-verlinde-stochastic-emergence.md) — Barandes-Doukas lifting theorem used in QM emergence
- [oppenheim-postquantum-classical-gravity.md](oppenheim-postquantum-classical-gravity.md) — Decoherence-diffusion trade-off inherited by SCG
- [diosi-penrose-gravitational-collapse.md](diosi-penrose-gravitational-collapse.md) — Collapse mechanism derived from cost optimization
- [nelson-stochastic-mechanics.md](nelson-stochastic-mechanics.md) — Diffusion-QM bridge; SCG provides physical source
- [../cross-cutting/spectral-dimension-running.md](../cross-cutting/spectral-dimension-running.md) — SCG predicts d_s → 2 at short distances, consistent with universal result
- [../cross-cutting/cost-function-ghost-selection-negative.md](../cross-cutting/cost-function-ghost-selection-negative.md) — Cost function constraints cannot select ghost-free gravity; blocks prediction #6 route
