# Strategy 001: Constraint-Driven Theory Construction

## Objective

Build a novel quantum gravity theory by first extracting the tightest empirical and theoretical constraints from what is already known, then systematically constructing theories that satisfy those constraints by design rather than by accident. The aim is to discover theories or mathematical structures that existing programs have not explored — particularly in the space between known approaches where hybrid or constraint-forced frameworks may live.

## Methodology

The Strategizer should follow a three-phase cycle, iterating within each phase as needed:

### Phase 1: Constraint Mapping (explorations 1–4)

Survey and extract the hardest constraints that any viable quantum gravity theory must satisfy. Organize them by type:

- **Structural constraints**: unitarity, ghost freedom, correct degrees of freedom (2 for massless graviton in 4D), diffeomorphism invariance
- **Recovery constraints**: Newton's law, linearized GR, equivalence principle, correct graviton propagator
- **Precision constraints**: graviton mass bound, GW speed, post-Newtonian parameters, Bekenstein-Hawking entropy
- **Cross-cutting convergences**: spectral dimension d_s → 2 in UV (appears across CDT, asymptotic safety, strings, LQG, Horava-Lifshitz — why?), entanglement area law, holographic entropy bounds

For each constraint, determine: (a) how restrictive it actually is (does it rule out large classes of theories, or is it easy to satisfy?), and (b) whether multiple approaches converge on it for the same or different reasons. Convergent results across independent frameworks are especially valuable — they may point to model-independent truths.

### Phase 2: Theory Construction (explorations 5–14)

Use the constraint map to build theories. The key insight: instead of starting from a physical picture (strings, loops, discrete sets) and checking whether constraints hold, start from the constraints themselves and ask what theories they force.

Specific construction methods to try:
- **Action-level construction**: Write the most general action consistent with the structural constraints, then impose recovery and precision constraints to fix coefficients and eliminate terms. What survives?
- **Convergence exploitation**: Take results that appear across multiple programs (spectral dimension running, area-law entropy, UV finiteness) and ask: what is the minimal theoretical structure that produces all of them simultaneously?
- **Gap-filling**: Identify the space between known approaches. What theories satisfy the LQG constraints but use continuous rather than discrete geometry? What theories have the UV behavior of asymptotic safety but the background independence of LQG?
- **Hybrid construction**: Take successful elements from different programs (e.g., the Reuter fixed point from asymptotic safety, the causal structure from causal sets, the entanglement structure from emergent gravity) and attempt rigorous synthesis.

For each constructed theory, immediately run it against the Tier 1 validation checks. If it fails, diagnose why and iterate. Theories that pass Tier 1 advance to Phase 3.

### Phase 3: Validation and Prediction (explorations 15–20)

Take the most promising theory(ies) from Phase 2 and push them through Tiers 2–4:

- Compute the graviton propagator and verify GR recovery
- Check quantitative bounds (graviton mass, GW speed, post-Newtonian parameters)
- Compute black hole entropy and check Bekenstein-Hawking
- Look for novel predictions — observable consequences that differ from standard GR and from existing quantum gravity approaches
- Assess testability: can any prediction be checked with current or near-future experiments?

If a theory fails at a specific tier, diagnose whether the failure is fixable (modify parameters, add terms) or fundamental (structural incompatibility). Feed fixable failures back into Phase 2 for iteration.

## Validation Criteria

Progress is measured by the mission validation guide's tiers. Specifically:

- **Minimum success**: At least one theory passes Tier 2 (recovers known physics) with a clear path toward Tier 3
- **Good success**: A theory passes Tier 3 (matches quantitative data) and produces at least one candidate novel prediction
- **Breakthrough**: A theory passes Tier 4 — a genuine, quantitative, testable prediction distinguishable from GR and from existing quantum gravity approaches

The strategy is **exhausted** when:
- Multiple independent construction attempts all converge on known theories (no novelty being produced)
- The constraint map has been fully exploited without producing viable Tier-2+ theories
- Repeated Phase 2–3 iterations are stuck at the same validation failure with no new ideas for resolution

## Context

This is the first strategy. The factual library contains 67 findings across 6 categories (string theory, LQG, asymptotic safety, causal set theory, emergent gravity, cross-cutting themes). Key things the Strategizer should be aware of:

- **Spectral dimension running** (d_s = 4 → 2 in UV) appears across CDT, asymptotic safety, strings, LQG, Horava-Lifshitz, and causal sets. This convergence is remarkable and underexploited.
- **Bekenstein-Hawking entropy** has been derived from at least 4 independent frameworks. Understanding *why* may be more revealing than any single derivation.
- **Jacobson's result** (Einstein equations from entanglement equilibrium) suggests gravity may be thermodynamic/entropic rather than fundamental. This is a strong constraint on the form any theory can take.
- **The cosmological constant problem** remains the hardest quantitative challenge — 120 orders of magnitude discrepancy. Causal set theory's "everpresent lambda" is the only approach that predicted the right order of magnitude.
- **Experimental landscape** is rapidly evolving: GQuEST tabletop detector, LIGO spacetime fluctuation searches (2026), gravity-induced entanglement experiments. Novel predictions targeting these experiments would be especially valuable.
- No prior strategies have been run. This is a fresh start.
