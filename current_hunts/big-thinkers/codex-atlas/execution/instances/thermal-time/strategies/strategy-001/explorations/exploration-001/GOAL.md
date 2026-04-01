# Exploration 001 — Modular Hamiltonians: Catalog, Formalization, and TTH Prediction

## Mission Context

We are investigating the Connes-Rovelli thermal time hypothesis (TTH): that physical time is the modular flow of the quantum state of the universe. The TTH makes a concrete claim — that the flow of time experienced by an observer is determined by the modular automorphism group σ_t^ω associated with their local state ω via the Tomita-Takesaki theorem.

The mission's goal is to find a concrete, quantitative prediction where TTH and standard QM diverge — or to rigorously characterize why they agree.

**Your working directory is the thermal-time mission. Write ALL output to `explorations/exploration-001/` within this directory.**

## Your Task

This is Phase 1 of the strategy: establish the mathematical toolkit by cataloging explicit modular Hamiltonians, then formalize what TTH actually predicts for a concrete system.

### Part 1: Modular Hamiltonian Catalog

For each of the following systems, write down explicitly:
- The algebra M (or M_A for a subsystem)
- The state ω (or ρ_A the reduced density matrix)
- The modular operator Δ = e^{-K}
- The modular Hamiltonian K = -log Δ
- The modular flow σ_t(A) = Δ^{it} A Δ^{-it}

**System 1: Rindler wedge (Bisognano-Wichmann)**
The modular Hamiltonian for the Rindler wedge is K = 2π * boost generator. Write this explicitly. What is the modular flow? What does it mean physically (Unruh effect)?

**System 2: Finite-dimensional — two-qubit system**
Take ρ_AB = |Φ+⟩⟨Φ+| (Bell state). Compute ρ_A = Tr_B[ρ_AB] = I/2. Write K_A = -log ρ_A. What is the modular flow on the algebra of subsystem A? Is it trivial (it will be — this is instructive)?

**System 3: Thermal state of a harmonic oscillator**
ρ = e^{-βH}/Z where H = ω a†a. Compute K = βH (up to constant). Write the modular flow explicitly. Verify it satisfies the KMS condition.

**System 4: CFT vacuum reduced to an interval [0, L] in 1+1d**
The Casini-Huerta result: K = 2π ∫_0^L dx ((L-x)x/L) T_{00}(x). Write this and describe what the modular flow looks like geometrically (it's a conformal transformation of the interval).

### Part 2: Formalizing the TTH Prediction

The TTH says: the physical time flow experienced by a system in state ω IS the modular flow σ_t^ω.

Now consider the following concrete setup — a bipartite system A+B in a global state ω, where:
- Subsystem A is in a KMS state at inverse temperature β_A (local equilibrium)
- Subsystem B is in a KMS state at inverse temperature β_B ≠ β_A
- A and B are then weakly coupled

**What does TTH predict?**
- The modular flow of the global state ω_{AB} does NOT factor into σ_t^A ⊗ σ_t^B when β_A ≠ β_B
- There will be "modular flow mismatch" at the boundary
- TTH must predict something about what an observer near the boundary experiences

Derive (or at least formally write down) what TTH predicts for the time experienced by a local observer at the A-B boundary. Is the time flow well-defined? Does it depend on β_A, β_B, and the coupling strength?

**Standard QM prediction for the same setup:**
For the same bipartite system with temperature gradient, standard quantum thermodynamics predicts thermalization via a Lindblad master equation. Write down the Lindblad equation for this system (two coupled harmonic oscillators at different temperatures is the simplest case). What does the decoherence rate depend on? Does it involve the modular Hamiltonian?

### Part 3: Identifying the Discriminating Observable

Based on Parts 1 and 2, identify the most promising observable where TTH and standard QM might give numerically different predictions. Candidates:
- Decoherence rate at the boundary between two temperature zones
- Correlation function decay C(t) = ⟨A(t)B(0)⟩ — TTH predicts decay along modular flow, standard QM predicts decay along physical time
- Thermalization timescale for the coupled system

For your top candidate: write down both the TTH prediction and the standard QM prediction in equation form. What is the parameter regime where they might differ?

### Part 4: Computation

Pick the simplest system from Part 3 where both predictions can be computed explicitly. This is likely the two coupled harmonic oscillators at different temperatures (β_A ≠ β_B).

Using Python (numpy/scipy/sympy), compute:
1. The modular Hamiltonian K for the coupled system
2. The modular flow σ_t for at least one observable
3. The Lindblad decoherence rate for the same system
4. Plot: modular flow trajectory vs standard QM trajectory for the same observable

Save all code to `explorations/exploration-001/code/`.

## Success Criteria

- Modular Hamiltonians written down explicitly for at least 2 systems (Part 1)
- TTH prediction formalized for the bipartite temperature-gradient setup (Part 2)
- At least one discriminating observable identified with both predictions in equation form (Part 3)
- At least a partial computation in Python (Part 4)

## Deliverables

Write your findings to:
- `explorations/exploration-001/REPORT.md` — full detailed report (target 200-400 lines), written incrementally as you work
- `explorations/exploration-001/REPORT-SUMMARY.md` — concise summary (20-40 lines), written LAST as your completion signal

## Important Notes

- **Your working directory is the thermal-time mission directory.** All file paths in your output should be relative to `instances/thermal-time/strategies/strategy-001/`.
- Write to REPORT.md incrementally — do not wait until the end to write everything.
- Cite papers where relevant (Connes & Rovelli 1994, Bisognano & Wichmann 1975-76, Casini & Huerta).
- If a computation is intractable, say exactly why and what would be needed to proceed.
