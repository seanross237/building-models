# Strategy 001 — Ground the Math, Find the Crack

## Objective

Establish the rigorous mathematical foundation needed to compare the thermal time hypothesis against standard quantum mechanics, then systematically search for a concrete system where their predictions diverge. This strategy prioritizes *calculation over conceptual argumentation* — every claim must be backed by an explicit computation on a well-defined system.

The deliverable is either: (a) a quantitative prediction where thermal time differs from standard QM, with the magnitude and parameter dependence computed, or (b) a clear map of which systems have been checked and why they yield equivalence, setting up the next strategy to look elsewhere.

## Methodology

### Phase 1: Foundation and Survey (explorations 1–3)

The first phase establishes the mathematical toolkit and identifies which concrete systems are tractable. The Strategizer should run explorations that:

1. **Extract the known modular Hamiltonians.** For which systems can the modular Hamiltonian be written down explicitly? The key cases from the literature are:
   - Rindler wedge in Minkowski spacetime (Bisognano-Wichmann theorem gives the modular Hamiltonian as the boost generator)
   - Half-space reduced states of free field theories (Casini-Huerta results)
   - Finite-dimensional systems (e.g., two coupled harmonic oscillators, spin chains with thermal states)
   - CFT vacuum reduced to an interval (known results in 1+1d)

   For each, write down: the algebra, the state, the modular operator Δ, the modular Hamiltonian K = -log Δ, and the modular flow σ_t.

2. **Formalize the thermal time hypothesis prediction.** What does the TTH actually say happens physically when two subsystems with different KMS states are coupled? The standard story is that time IS modular flow. But modular flow is state-dependent. So when two subsystems at different temperatures (different KMS states) are entangled across a boundary, their modular flows don't agree. The TTH must predict something specific about this mismatch. Derive what it predicts — not narratively, but from the formalism.

3. **Formalize the standard QM prediction.** For the exact same physical setup, derive what standard quantum thermodynamics predicts. This is the control. The standard approach would use partial trace, reduced density matrices, and Lindblad master equations for decoherence. Get this computation done for at least one concrete system so we have a comparison target.

**Phase 1 is complete when:** We have explicit modular Hamiltonians for at least 2 concrete systems, the TTH prediction is formalized for at least 1 system, and the standard QM prediction is computed for comparison.

### Phase 2: Calculate and Compare (explorations 4–7)

With the foundation laid, the second phase does the actual head-to-head comparison. The methodology here is:

**For each candidate system:**
1. Define the bipartite setup: subsystem A and B with their respective algebras M_A, M_B, and a global state ω
2. Compute the reduced states ω_A, ω_B and their modular Hamiltonians K_A, K_B
3. Compute the modular flow for the global state vs. the local modular flows
4. Identify the specific observable where TTH and standard QM might differ — decoherence rate is the mission's suggested starting point, but the Strategizer should also consider:
   - Entanglement entropy dynamics
   - Correlation function decay across the boundary
   - Thermalization rates
   - Berry phase or geometric phase from modular flow mismatch
5. **Compute both predictions numerically** — write code to evaluate the integrals, solve the differential equations, do parameter sweeps. Do not hand-wave.
6. Compare. Is there a parameter regime where the two predictions diverge?

**Key computational targets the Strategizer should assign to explorers:**
- For the Rindler wedge: compute the Unruh decoherence as seen by an accelerated observer using modular flow vs. using standard QFT in curved spacetime. This is the most concrete system because Bisognano-Wichmann gives us the exact modular Hamiltonian.
- For coupled harmonic oscillators at different temperatures: this is the simplest finite-dimensional test bed. Compute everything exactly.
- For a 1+1d CFT interval: use the known conformal results for modular Hamiltonians to check if boundary effects from modular flow mismatch produce observable signatures.

**Phase 2 is complete when:** At least 2 systems have been fully computed (both TTH and standard QM predictions) and compared quantitatively.

### Phase 3: Sharpen or Pivot (explorations 8–10)

Based on what Phase 2 finds:

**If a difference was found:**
- Verify it's not an artifact by checking in a second system
- Characterize the magnitude and parameter dependence
- Identify the experimental regime (Unruh temperature, required accelerations, etc.)
- Do the prior art search: has anyone derived this specific prediction before?
- Stress-test: what's the strongest objection and how does the result hold up?

**If no difference was found:**
- Understand *why* they agree — is there a structural reason (e.g., does the TTH reduce to standard QM for all type III factors)?
- Search for alternative observables beyond decoherence
- Consider whether the agreement itself is a publishable result if it can be made rigorous and general
- Look for loopholes: are there exotic states or non-equilibrium scenarios where the two frameworks must diverge?

### Cross-cutting rules

- **Explorers must compute.** Every exploration should include explicit calculations — symbolic (SymPy) or numerical (NumPy/SciPy). An exploration that reasons about what the answer "should be" without computing it has failed.
- **Verify against known results.** Before trusting any new calculation, verify the computational pipeline reproduces known results (e.g., Unruh temperature from Bisognano-Wichmann, KMS condition from modular flow).
- **Track the comparison table.** The Strategizer should maintain a running comparison: for each system and observable, what does TTH predict vs. standard QM? This table IS the deliverable.

## Validation Criteria

**Strategy is succeeding when:**
- Tier 1 (Formalization) is reached by end of Phase 1
- Tier 2 (Derivation) is reached by mid-Phase 2
- Tier 3 (Discrimination) is reached by end of Phase 2

**Strategy is exhausted when:**
- Phase 2 is complete for 2+ systems with no divergence found, and no promising alternative observables remain
- OR a divergence is found and Phase 3 has verified and characterized it

**Red flags to pivot on:**
- If Phase 1 reveals that explicit modular Hamiltonians can only be computed for trivially simple systems where TTH and standard QM obviously agree, the Strategizer should immediately pivot to algebraic/structural arguments rather than brute-force computation
- If the TTH formalization turns out to be ambiguous (multiple reasonable interpretations that give different predictions), this is itself a finding — document the interpretive options and compute predictions for each

## Context

This is strategy-001. No prior work exists in this mission. The missionary meta library is empty.

Key literature entry points:
- Connes & Rovelli (1994) — "Von Neumann algebra automorphisms and time-thermodynamics relation in generally covariant quantum theories"
- Bisognano & Wichmann (1975, 1976) — modular theory in Wightman QFT, the boost-modular connection
- Haggard & Rovelli (2013) — thermal time and Tolman-Ehrenfest effect
- Martinetti & Rovelli (2003) — diamonds, temperatures, and thermal time
- Casini & Huerta — modular Hamiltonians for free fields
- Witten (2018) — "APS medal lecture: notes on some entanglement properties of quantum field theory" (excellent modern review of modular theory in QFT)

The mission specifically calls out the Unruh effect and Rindler wedge as testing grounds. This is well-motivated: the Bisognano-Wichmann theorem gives us the exact modular Hamiltonian for Rindler wedges, making it one of the few systems where TTH predictions can be computed exactly.
