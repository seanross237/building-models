# Exploration 001: Structural and Recovery Constraints for Quantum Gravity

## Mission Context

We are developing a novel theory of quantum gravity using a constraint-driven construction approach. Rather than starting from a physical picture (strings, loops, discrete sets) and checking constraints afterward, we start from the constraints themselves and ask what theories they force.

This is the first exploration in a constraint-mapping phase. We need a rigorous, ranked catalog of every constraint a viable quantum gravity theory must satisfy.

## Your Goal

Produce a comprehensive, ranked constraint map for quantum gravity theories. For each constraint, determine:

1. **What the constraint says** — precise statement
2. **How restrictive it is** — does it rule out large classes of theories, or is most anything consistent with it?
3. **Which known approaches satisfy it** — and which struggle
4. **Whether it's a hard requirement or soft preference** — e.g., unitarity is non-negotiable; background independence is debated
5. **The mathematical form** — what equation or inequality must be satisfied

Organize constraints into these categories:

### A. Structural Constraints (non-negotiable mathematical consistency)
- Unitarity (S-matrix unitarity)
- Ghost freedom (no negative-norm states in physical spectrum)
- Correct degrees of freedom (2 polarizations for massless graviton in 4D)
- Gauge symmetry consistent with diffeomorphism invariance
- Renormalizability or UV completion (theory makes sense at all energies)
- Causality preservation

### B. Recovery Constraints (must reproduce known physics in appropriate limits)
- Newton's law: V(r) = -GM/r at large distances
- Linearized GR: correct linearized Einstein equations
- Graviton propagator matching GR in IR
- Three-graviton vertex matching GR (or deviations within bounds)
- Equivalence principle
- Lorentz invariance (or violations below experimental bounds)
- Post-Newtonian corrections matching solar system tests

### C. Cross-Framework Convergences (results that appear across multiple independent approaches)
- Spectral dimension running d_s = 4 -> 2 in UV (appears in CDT, asymptotic safety, strings, LQG, Horava-Lifshitz, causal sets)
- Bekenstein-Hawking entropy S = A/(4G) from at least 4 independent frameworks
- Entanglement area law
- Jacobson's result: Einstein equations from entanglement equilibrium
- Holographic entropy bounds

For each convergence, assess: Is this a genuine constraint (any viable theory MUST reproduce it) or merely a common feature that could be an artifact?

### D. Precision Constraints (quantitative bounds from experiment)
- Graviton mass: m_g < 1.2 x 10^-22 eV
- GW speed: |c_gw/c - 1| < 5 x 10^-16
- Post-Newtonian parameter: |gamma - 1| < 2.3 x 10^-5
- Lorentz violation bounds from Standard Model Extension (SME)
- Any other precision tests from recent experiments (2024-2026)

## Success Criteria

- Comprehensive catalog with at least 20 distinct constraints across all four categories
- Each constraint has a clear restrictiveness ranking (high/medium/low)
- Mathematical form given where applicable
- At least 5 constraints identified as "maximally restrictive" — ones that eliminate the most candidate theories
- Clear identification of which constraints are genuinely independent vs. which follow from others

## Failure Criteria

- Fewer than 15 constraints cataloged
- No ranking of restrictiveness
- Only vague statements without mathematical precision

## Output

Write your full findings to:
- `explorations/exploration-001/REPORT.md` (detailed report — write incrementally!)
- `explorations/exploration-001/REPORT-SUMMARY.md` (concise summary — write last)
