---
topic: quadratic-gravity-fakeon
confidence: provisional
date: 2026-03-26
source: exploration-005-entanglement-fakeon (quantum-gravity-2 strategy-002)
---

# Entanglement Structure Requires the Fakeon

## Summary

Novel concept: the fakeon prescription is uniquely selected by the requirement of well-defined entanglement entropy — extending the MVEH (Maximal Vacuum Entanglement Hypothesis) construction. The ghost with Feynman prescription produces pathological entanglement (negative eigenvalues, complex entropy), destroying the entanglement scaffold from which gravity emerges. The fakeon restores consistency, closing a self-consistency loop: gravity from entanglement requires fakeon, which preserves entanglement.

**Self-assessment:** Novelty 8/10, Consistency 6/10, Clarity 7/10, Viability 5/10. **Verdict:** Philosophically appealing, genuine gap between communities, but may reduce to "unitarity" with extra decoration. Main value is as a research direction and bridge concept.

## The Mechanism: Five Steps

**Step 1 — MVEH derives gravity from entanglement equilibrium.** Jacobson (2015): δS_EE = δ(A/4G) for all local causal horizons → linearized Einstein equations. Bueno et al. (2017): extended to higher-derivative gravity with Wald entropy corrections → linearized quadratic gravity field equations.

**Step 2 — MVEH requires well-defined entanglement entropy.** The derivation assumes S_EE is real, non-negative, UV-renormalizable. Guaranteed when the spectral function ρ(s) ≥ 0 for all physical modes.

**Step 3 — Feynman ghost violates this requirement.** The massive spin-2 ghost (negative residue at m² = M₂²) with Feynman prescription produces negative-norm physical states. **Jatkar & Narayan (2017, Nucl. Phys. B 922, 319)** showed explicitly: ghost-spin entanglement produces pathological reduced density matrices with negative eigenvalues; von Neumann entropy acquires negative real part and imaginary contributions. With an odd number of ghost DOF (5 polarizations for spin-2), no positive-norm subsector guarantees positive S_EE.

**Step 4 — Fakeon restores well-defined entanglement.** Fakeon prescription quantizes the ghost as purely virtual — never in physical external states. Physical Hilbert space is positive-definite (massless graviton + matter only). S_EE is real, non-negative, UV-renormalizable by standard gravitational counterterms (Cooperman & Luty, 2013). MVEH premises satisfied.

**Step 5 — Self-consistency loop closes.** Gravity emerges from entanglement (MVEH) → QG contains ghost that would destroy entanglement → fakeon preserves entanglement → gravity remains self-consistent. The fakeon is not imposed externally; it is the unique prescription compatible with the entanglement origin of gravity.

## Key Quantity: Ghost Spectral Contribution to Vacuum S_EE

For a free field of mass m and spin s, UV-divergent entanglement entropy across a planar boundary: S_EE ~ c(s) · A/ε² + ..., where c(s) depends on spin. With Feynman ghost: c(s) < 0 — subtracts from entropy, potentially making total S_EE negative or complex. With fakeon: ghost makes zero contribution to physical S_EE (no physical states). Only positive graviton contribution survives.

## Analyticity Sacrifice as Informational Area Law Manifestation

Dispersion relations (Kramers-Kronig) assume all intermediate states are physical and contribute to the spectral function with positive weight. The fakeon breaks this: the ghost is NOT a physical intermediate state. The analyticity sacrifice is the S-matrix encoding the fact that **not all kinematically allowed states contribute to the entanglement structure** — the area law has "removed" them.

## Structural Prediction

If this picture is correct, the Wald entropy corrections in QG+F should be EXACTLY the corrections maintaining MVEH with fakeon prescription. Specifically: the Wald entropy functional for S = ∫(R + αR² + βR_μνR^μν) should be the unique entanglement functional making entanglement equilibrium equivalent to fakeon-quantized field equations. **In principle checkable** by comparing Bueno et al.'s generalized MVEH with known QG+F Wald entropy.

## Research Direction: Nonlinear MVEH as Prescription Selector

The linearized MVEH (Bueno et al. 2017) cannot distinguish Feynman ghost, Lee-Wick, or fakeon — they agree at tree level. The concept predicts that any attempt to derive **nonlinear** gravitational equations from entanglement will REQUIRE specifying the quantization prescription. The nonlinear extension should uniquely select the fakeon. This is the key open problem.

## Devil's Advocate: Key Objections

1. **May reduce to unitarity + extra steps (STRONGEST):** The chain MVEH → positive S_EE → positive-definite Hilbert space → unitarity → fakeon is just "unitarity requires the fakeon" with entanglement decoration. Genuinely new only if entanglement imposes STRONGER constraints than unitarity alone.

2. **Linearization barrier:** Bueno et al. explicitly state nonlinear higher-curvature equations cannot be derived from linearized MVEH in small balls. At linearized level, all ghost prescriptions are indistinguishable. The concept NEEDS the nonlinear extension that doesn't exist yet.

3. **Partial circularity:** Fakeon defined as prescription giving unitarity; unitarity makes entanglement well-defined; saying "fakeon makes entanglement well-defined" restates the definition. Non-circular content: ghost creates SIGN problem in UV divergences (not just magnitude), violating area law positivity.

4. **No new quantitative predictions:** Concept provides interpretation, not new constraints. QG+F predictions (r, microcausality, etc.) unchanged.

5. **AdS vs. dS problem:** Rigorous entanglement-spacetime results (Ryu-Takayanagi, MVEH) are in AdS or flat space. Our universe has positive Λ. Domain of applicability uncertain.

6. **Ghost entanglement pathology unproven in QFT:** Jatkar-Narayan is for spin systems, not QFT. Whether negative spectral weight leads to complex entropy after QFT renormalization is not established.

## Cross-References

- [`../cross-cutting/entanglement-gravity-bootstrap.md`](../cross-cutting/entanglement-gravity-bootstrap.md) — The MVEH → QG+F construction this builds on (complementary: that file focuses on bootstrap; this focuses on ghost entanglement pathology)
- [`../gravitize-the-quantum/scg-viable-moves-for-qgf.md`](../gravitize-the-quantum/scg-viable-moves-for-qgf.md) — Move 7 (1-paragraph precursor)
- [`analyticity-sacrifice.md`](analyticity-sacrifice.md) — The analyticity cost this concept reinterprets informationally
- [`explanatory-debts-catalog.md`](explanatory-debts-catalog.md) — Gaps #1 and #5 that this targets
- [`causal-order-fakeon-interpretation.md`](causal-order-fakeon-interpretation.md) — Alternative interpretation (lower novelty, higher viability)
- [`indivisibility-fakeon-interpretation.md`](indivisibility-fakeon-interpretation.md) — Alternative interpretation (highest novelty, lowest viability)

Sources: Jacobson (arXiv:1505.04753, 2015); Bueno et al. (arXiv:1612.04374, Phys. Rev. D 95, 046003, 2017); Jatkar & Narayan (Nucl. Phys. B 922, 319, 2017); Cooperman & Luty (2013); Speranza (JHEP 12, 2023, 020); Faulkner et al. (arXiv:1705.03026, 2017)
