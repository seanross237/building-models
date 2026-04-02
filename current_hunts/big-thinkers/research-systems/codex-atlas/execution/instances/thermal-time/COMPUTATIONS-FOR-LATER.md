# Computation Registry

Computations identified during explorations that would significantly advance the mission. Maintained by the strategizer, read by the missionary and future strategizers.

---

## Computation 1: Type III Algebra Test — Rindler Wedges with Minkowski Vacuum

**What it is:** Repeat the C_full vs C_local comparison for two adjacent Rindler wedges (left wedge and right wedge) using the Minkowski vacuum state on a 1+1D lattice scalar field. The algebras are type III₁ (Haag-Araki-Kastler), which is the regime TTH was designed for.

**Why it matters:** Strategy-001 showed that local TTH is falsified for non-relativistic coupled oscillators. But TTH was designed for type III algebras where no background Hamiltonian exists. The Rindler wedge test would check whether the local modular flow (= Rindler boost at temperature T_U = ℏa/2πck_B) agrees with the physical dynamics restricted to the wedge. Bisognano-Wichmann theorem says K_R = 2π × boost generator — so the modular flow IS the boost. If C_local = C_full in this regime, TTH is verified in its intended domain.

**What it would resolve:** Is TTH a physically correct statement about time in the generally covariant regime? Does the local modular flow agree with the restricted global dynamics when the algebra is type III?

**Which exploration identified it:** Exploration-004 (REPORT-SUMMARY.md, Computations Identified section)

**Estimated difficulty:** Moderate (100–200 lines Python, scipy-level). Requires: (a) lattice discretization of free scalar field on 1+1D, (b) Bogoliubov transformation to Rindler modes, (c) Minkowski vacuum two-point function, (d) modular Hamiltonian of Rindler restriction (numerically), (e) autocorrelation comparison.

**Key references:**
- Bisognano-Wichmann theorem: Bisognano & Wichmann (1975, 1976); review in Haag "Local Quantum Physics" Ch. V
- Modular theory for Rindler: Takesaki, "Tomita's Theory of Modular Hilbert Algebras" (1970); Borchers (1992) for half-sided modular inclusions
- Lattice implementation: Casini & Huerta (2009), arXiv:0903.5284 (CFT interval modular Hamiltonian lattice approach)

---

## Computation 2: Non-Equilibrium TTH Test

**What it is:** Compute C_full vs C_local for a NON-Gibbs state of the coupled oscillator system (e.g., a squeezed thermal state or a state after a quantum quench). For non-Gibbs states, K_AB ≠ βH_AB even globally — so the global TTH differs from QM, and the local TTH prediction is a genuine TTH-specific prediction.

**Why it matters:** Strategy-001's conclusion was that TTH ≡ QM (global) or TTH is falsified (local) for equilibrium Gibbs states. Non-equilibrium states break this dichotomy: the global modular flow generates dynamics different from H_AB, giving TTH genuine non-trivial content even in the non-relativistic regime.

**What it would resolve:** Does TTH make novel, non-trivially testable predictions for non-equilibrium non-relativistic systems? If yes, are those predictions consistent with or contradicted by the Schrödinger/Heisenberg dynamics? What is the correct physical interpretation of modular time in a non-equilibrium state?

**Which exploration identified it:** Exploration-004 (REPORT-SUMMARY.md, Computations Identified section)

**Estimated difficulty:** Low (~50 lines). Extend exploration-003's code (`comparison_results.json` infrastructure) with a non-Gibbs initial state (e.g., ρ_0 = coherent displacement of thermal state, or post-quench state from sudden coupling change).

**Key references:**
- Modular Hamiltonians for out-of-equilibrium states: Hollands & Sanders (2017), "Entanglement measures and their properties in quantum field theory," arXiv:1702.04924
- Quantum quench modular theory: Cardy & Tonni (2016), arXiv:1602.08273

---

## Computation 3: Analytic ΔK_A to O(λ²) via Duhamel Perturbation Theory

**What it is:** Derive the closed-form expression for ΔK_A = K_A − βH_A at second order in λ using the Duhamel/perturbative expansion of ρ_A = Tr_B[e^{-β(H_0 + λV)}/Z] around the uncoupled state.

**Why it matters:** Strategy-001 found numerically that Δβ = −1.36λ² and ΔK_A has squeezing structure. An analytic formula would (a) confirm the coefficient, (b) give the exact form of the squeezing term, (c) provide the full O(λ²) structure including any terms the numerical approach might miss, and (d) be a clean publishable result.

**What it would resolve:** What is the exact closed-form expression for ΔK_A to O(λ²) for bilinear coupling? Does the squeezing structure follow simply from the Bogoliubov transformation diagonalizing H_AB, or is it genuinely a modular-Hamiltonian-specific phenomenon?

**Which exploration identified it:** Exploration-002 identified the numerical structure; exploration-004 recommended the analytic follow-up.

**Estimated difficulty:** Moderate analytical. Main tool: Duhamel formula for matrix exponentials, ρ_A = ρ_A^(0) + λρ_A^(1) + λ²ρ_A^(2) + ...; then K_A = −log(ρ_A) expanded via Baker-Campbell-Hausdorff or resolvent. The O(λ¹) term vanishes (confirmed numerically), so the first non-trivial term is O(λ²). Requires standard quantum optics perturbation theory (Schrieffer-Wolff or resolvent approach).

**Key references:**
- Modular Hamiltonian perturbation theory: Lashkari (2016) "Modular Hamiltonian for excited states in conformal field theory," arXiv:1508.03506
- Perturbative expansion of reduced density matrices: Baumgratz, Cramer, Plenio (2012), arXiv:1204.0992 (for general coupled systems)
- Duhamel formula: standard operator theory; Haag "Local Quantum Physics" Appendix; Reed-Simon Vol. I

