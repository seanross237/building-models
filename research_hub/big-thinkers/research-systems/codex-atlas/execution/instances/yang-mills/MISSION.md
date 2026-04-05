# Mission

Prove that for any compact simple gauge group G, a non-trivial quantum Yang-Mills theory exists on R^4 and has a mass gap — or make concrete, defensible progress toward such a proof.

This is the Yang-Mills Existence and Mass Gap problem, one of the seven Millennium Prize Problems. It requires two things: (1) rigorously constructing a quantum Yang-Mills theory in 4 spacetime dimensions satisfying the Wightman axioms or equivalent, and (2) proving the theory has a mass gap — the lowest energy state above the vacuum has strictly positive energy.

No interacting quantum field theory has ever been rigorously constructed in 4D. The mass gap is a non-perturbative phenomenon invisible to Feynman diagrams. These are among the deepest open problems in mathematical physics.

The most developed approaches:
- **Lattice gauge theory**: Wilson's formulation discretizes spacetime. Lattice QCD numerically confirms confinement and mass gap. The open problem is proving the continuum limit exists and preserves these properties.
- **Balaban's program**: Tadeusz Balaban developed a rigorous renormalization group analysis for lattice Yang-Mills in 4D through a series of papers in the 1980s-90s. This is the deepest existing partial result. Understanding exactly where it stops and what's needed to complete it is high priority.
- **Constructive QFT**: Glimm-Jaffe methods succeeded in lower dimensions. The 4D case requires controlling ultraviolet divergences non-perturbatively.
- **Asymptotic freedom**: Proven perturbatively (Gross-Wilczek-Politzer). Provides UV behavior but doesn't address IR/non-perturbative regime where the mass gap lives.
- **Functional integral / stochastic quantization**: Rigorous probabilistic approaches to the Yang-Mills path integral.

Concretely, pursue one or more of:
- Identify the precise technical obstruction in Balaban's program — what specific step fails or is missing in extending his results to a full continuum limit proof?
- Formalize known partial results in Lean 4 to build verified stepping stones and identify exactly where proof gaps exist
- Compute lattice Yang-Mills observables that test specific aspects of the mass gap (glueball masses, string tension, Wilson loops) and connect numerical evidence to proof strategies
- Find a novel connection between approaches (e.g., lattice + constructive QFT + stochastic quantization) that hasn't been explicitly developed
- Prove a partial result: a mass gap in a simplified setting, a rigorous bound, or a theorem that eliminates a class of pathologies
- Develop or test a new proof strategy that circumvents known obstructions

Explorers have full shell access and should compute rather than speculate. Math explorers can use Lean 4 + Mathlib for formal verification. When a partial result or lemma can be formalized, do it. When formalization fails, report exactly where the proof breaks and what's missing.
