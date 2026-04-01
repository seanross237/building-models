# Computations for Later

Parking lot for computations, derivations, and technical threads that aren't immediately needed but may be valuable for future explorations.

---

## 1. DeWitt-Brehme self-force in de Sitter spacetime
**What**: Compute the full back-reaction force on a uniformly accelerating scalar charge in de Sitter. Does the effective mass correction go as T_U/T_dS?
**Why it matters**: This is the most direct route to a first-principles derivation of the ratio ansatz m_i = m × T_U/T_dS that gives the MOND interpolation function.
**What it would resolve**: Whether the T_U/T_dS identity has physical content or is just a mathematical curiosity.
**Source**: Exploration 004
**Difficulty**: Hard — requires numerical integration of the retarded Green function in de Sitter
**References**: DeWitt & Brehme (1960), Pfenning & Poisson (2002)

## 2. Verlinde's entropy displacement for specific galaxy rotation curves
**What**: Compute predicted rotation curves from Verlinde (2017) full entropic force formula (not just deep-MOND limit) for SPARC galaxies. Compare χ² fit.
**Why it matters**: Verlinde's approach IS the de Sitter crossover from a holographic perspective. Comparing its full predictions to data would validate or constrain the approach.
**Source**: Exploration 003
**Difficulty**: Moderate — ~100-line Python script; need galaxy baryonic mass profiles from SPARC
**References**: Verlinde (2016), arXiv:1611.02269; Lelli et al. (2017)

## 3. Literature search: has T_U/T_dS = μ_MOND been published?
**What**: Search for explicit prior publication of the algebraic identity T_U(a)/T_dS(a) = a/√(a²+c²H₀²) = μ_MOND(a/cH₀).
**Why it matters**: If this is known, we need to cite it. If novel, it's a concrete result from this mission.
**Source**: Exploration 004
**Difficulty**: Easy — literature search
**References**: Deser & Levin (1997), Milgrom (1983)

## 4. What "acceleration" enters the formula for freely-falling objects?
**What**: Stars in galaxies are in free fall. The standard Unruh effect applies to proper acceleration. What quantity plays the role of "a" in the modified dynamics for freely-falling objects in curved spacetime?
**Why it matters**: This is the strongest surviving objection from Exploration 003. Any viable mechanism must answer this.
**Source**: Exploration 003
**Difficulty**: Conceptual — requires careful analysis of equivalence principle in this context

## 5. Massive-field Wightman function in de Sitter along accelerating worldline
**What**: Evaluate the Wightman function for a massive scalar field in de Sitter for an accelerating detector. Does the massive density of states produce any non-trivial structure beyond the threshold?
**Source**: Exploration 001, 004
**Difficulty**: Moderate — known hypergeometric functions but numerical evaluation is nontrivial
