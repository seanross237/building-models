# Strategy 001 — Derive or Falsify the Compton-Unruh Resonance

## Objective

Establish the mathematical framework for a Compton-Unruh resonance at low accelerations, carry the calculation as far as possible, and determine whether the resonance exists, modifies inertia, and is physically distinct from existing proposals (MOND, McCulloch QI). This strategy prioritizes reaching a decisive result — either a derived prediction or a rigorous no-go — over comprehensiveness.

## Methodology: Adversarial Derivation Protocol

The core principle: **derive, then immediately try to kill what you derived.** Every constructive exploration is followed (or accompanied) by an adversarial one that stress-tests the result. This prevents the common failure mode of building an elaborate theoretical structure on a flawed foundation.

### Phase 1: Framework & Feasibility (explorations 1–3)

**Goal:** Set up the QFT-in-curved-spacetime framework correctly, write down the key equations, and perform a feasibility check before investing in heavy computation.

The Strategizer should design explorations that:
1. **Derive, don't quote.** Start from a scalar field in a de Sitter background with an Unruh-DeWitt detector. Derive the detector response function. Identify how the Compton frequency enters (field mass → oscillation frequency of the mode functions). Write down the explicit integral or equation whose evaluation would reveal whether a resonance exists at a ~ cH₀.
2. **Dimensional analysis first.** Before any detailed calculation, verify that a resonance at a ~ cH₀ is dimensionally possible. What are the relevant energy/length/time scales? Do they actually coincide, or is this a numerological coincidence?
3. **Hunt for no-go theorems early.** Before investing in the full calculation, search for existing arguments that would rule out Unruh-effect-based inertia modification at low accelerations. Check: Does the Unruh effect even apply to bound systems (stars in galaxies)? Is the Unruh temperature at a ~ cH₀ so low (≈ 10⁻³⁰ K) that no physical effect is possible? Are there thermodynamic or quantum-coherence arguments against this?

**Checkpoint to advance:** The key integral/equation is written down explicitly. The regime of interest is physically characterized. Any obvious no-go has been found or ruled out. If a fatal no-go is found here, skip to documenting the null result — that's a valid mission outcome.

### Phase 2: Calculation & Prediction (explorations 4–6)

**Goal:** Evaluate the key integral/equation. If a resonance exists, derive the modified inertia law. Compute predicted rotation curves.

The Strategizer should design explorations that:
1. **Compute, don't argue.** Explorers have full shell access — use scipy, sympy, numpy. The key integral should be evaluated numerically if analytic methods fail. Try series expansions, saddle-point approximations, numerical quadrature. Don't reason about what the answer "should" be — calculate it.
2. **Cross-check against known limits.** The flat-spacetime limit must recover standard Unruh. The large-acceleration limit must recover standard inertia. Any modified inertia law must reduce to m_i = m_g in the Newtonian regime.
3. **Generate numbers, not just formulas.** If a modified inertia law is derived, compute actual rotation curves for NGC 3198 and NGC 2403 (well-studied benchmark galaxies). Look up their observed baryonic mass distributions and compute v(r). Compare against SPARC data or published fits. Report χ² or equivalent fit quality.

**Checkpoint to advance:** Either the calculation is complete (resonance confirmed or denied with explicit math), or the point of intractability is precisely identified. If predictions exist, they include actual numbers for at least one galaxy.

### Phase 3: Distinctness & Stress Testing (explorations 7–8)

**Goal:** Determine whether this is genuinely new physics or a rediscovery of existing proposals. Stress-test against known constraints.

The Strategizer should design explorations that:
1. **Compare equations, not narratives.** Write down the modified dynamics from this approach, from MOND (Milgrom 1983), and from McCulloch QI side-by-side. Are the transition functions identical? Is there a regime where predictions differ? If they're equivalent, prove it algebraically.
2. **Check the hardest constraints.** Solar system dynamics (Pioneer anomaly bounds). Bullet cluster. Gravitational lensing without dark matter. CMB third peak. These are the observations that kill most modified-gravity proposals. If the Compton-Unruh approach can't address at least the strongest one, identify that clearly.

### Exploration Budget & Pacing

- Target 6–8 explorations total. The Strategizer may use fewer if a decisive result arrives early.
- Explorations should be tightly scoped — 1 clear question, 1 clear deliverable. A 90-minute exploration that answers one question well is better than a 3-hour exploration that surveys vaguely.
- If Phase 1 produces a no-go theorem, the strategy can complete early. Document the no-go rigorously — a well-characterized impossibility result is a valid and valuable mission outcome.
- If the calculation in Phase 2 is genuinely intractable, document exactly where it breaks down and what tools/techniques would be needed. This is also a valid outcome.

### Novel Claims Tracking

From exploration 3 onward, each exploration report should include a "Novel Claims" section identifying any claim that goes beyond established literature. The Strategizer should accumulate these and stress-test the strongest ones in later explorations.

## Validation Criteria

This strategy succeeds if it reaches at least Tier 2 of the mission validation guide:
- The QFT framework is correctly set up (Tier 1)
- The key integral/equation is identified and at least partially evaluated (Tier 2)
- Progress toward Tier 3–5 is a bonus, not a requirement for strategy-001

This strategy is **exhausted** when:
- The key calculation is either complete or blocked (with the obstruction characterized)
- The no-go search has been conducted
- The Strategizer has used 8 explorations or determined that further explorations within this methodology won't produce new results

## Context

- This is the first strategy. No prior exploration has been done. The library is empty.
- The meta library has no entries from previous missionaries.
- The mission explicitly values partial results — framework setup, key integral identification, no-go theorems, and mechanism comparison all count as progress.
- Explorers have computational tools (Python, scipy, sympy, numpy). Design explorations that use them. Don't rely on purely verbal physics reasoning when a calculation can settle the question.
