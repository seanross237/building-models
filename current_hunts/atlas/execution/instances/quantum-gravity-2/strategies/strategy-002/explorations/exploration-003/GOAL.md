# Exploration 003: Concept Sprint — Causal Order as the Physical Origin of the Fakeon

## Mission Context

QG+F (quadratic gravity + fakeon quantization) is the unique perturbative quantum gravity in 4D, but nobody understands what the fakeon IS physically. The fakeon prescription:
- Removes the massive spin-2 ghost from the physical spectrum (purely virtual)
- Violates microcausality at Planck scales (fields don't commute at spacelike separation below ~1/M₂)
- Sacrifices S-matrix analyticity (no dispersion relations, no crossing symmetry in the standard sense)
- Has no classical limit (the ghost doesn't correspond to any classical field)
- Anselmi (Jan 2026) proposes abandoning causality itself as fundamental

This exploration develops a NOVEL concept: **the fakeon prescription arises from spacetime's causal partial order.**

## The Core Concept to Develop

**Physical intuition (for a non-physicist):**
Imagine spacetime as a web of causal connections — every event is linked to its causal past and future, like a branching river. In quantum field theory, we normally allow virtual particles to "flow backwards in time" through loops. The fakeon is nature's way of enforcing the river's direction: the massive spin-2 mode is not allowed to become a real particle because doing so would violate the causal order. It contributes to the quantum accounting (loop integrals) but never materializes, because materialization would require a locally acausal process. Microcausality violation at the Planck scale is the "spray at the edges" where the strict causal flow is slightly fuzzy — but this fuzziness doesn't propagate.

**Mathematical skeleton:**
1. Spacetime has a fundamental causal partial order ≺ (as in causal set theory)
2. Via Malament's theorem, ≺ determines the conformal geometry up to a volume factor
3. The propagator of any field must be compatible with this causal order
4. For the massless graviton: compatible (it propagates causally)
5. For the massive spin-0 (from R²): compatible (it propagates causally)
6. For the massive spin-2 ghost: incompatible as a real particle. The ghost's propagator has the wrong sign residue, meaning its "flow" would reverse the causal order at the pole. The only consistent treatment is the fakeon prescription — include it in loops (virtual causal accounting) but forbid real production (which would violate ≺).
7. The analyticity sacrifice is natural: causal partial orders are discrete/non-smooth structures, so the S-matrix built from causal-order-compatible propagators is not analytic in the standard sense.

## What You Must Do

### Part 1: Novelty Check (critical — do this first)
Search the literature for:
- Has ANYONE connected causal structure/causal sets to the fakeon prescription?
- Has ANYONE derived quantization prescriptions from causal order?
- What is the relationship between causal structure and propagator prescriptions in curved spacetime?
- Is there work on "causal propagators" vs. "acausal propagators" in higher-derivative gravity?
- Search: Anselmi + causal, Sorkin + quadratic gravity, Dowker + higher-derivative, causal order + quantization prescription, Malament + quantum field theory

If this concept already exists in the literature, document it and assess whether there's ANYTHING new you can add. If it's genuinely novel, proceed to Part 2.

### Part 2: Develop the Concept
1. **Physical picture** (2-3 paragraphs a thoughtful non-physicist can follow)
2. **The mechanism:** HOW does causal order constrain propagator prescriptions? Be specific — this is the core innovation. You need a rule of the form: "Given causal order ≺, the propagator of a field with pole at p² = m² must satisfy [condition]. For positive-residue poles, this is automatically satisfied. For negative-residue poles (ghosts), this requires the fakeon prescription."
3. **One testable prediction** that differs from QG+F-without-causal-motivation. Even speculative.
4. **Self-assessment:** Rate on (a) genuine novelty 1-10, (b) internal consistency 1-10, (c) explanatory clarity 1-10, (d) viability for further development 1-10.

### Part 3: Devil's Advocate (immediately after Part 2)
Attack your own concept:
- Does the classical→quantum gap kill it? (Causal order is classical; fakeon is quantum.)
- Is this just "unitarity requires the fakeon" restated in causal language?
- Can you derive that the spin-2 ghost must be a fakeon without already knowing it's a ghost?
- Would this concept select the fakeon even if you didn't already know the answer?

## Key Constraints from Strategy-001

1. **Classical cost functions cannot select QG+F.** Causal order is classical. How does a classical structure constrain a quantum prescription? This is the CENTRAL CHALLENGE.
2. **The fakeon is inherently quantum.** The same Lagrangian gives Stelle gravity classically and QG+F quantum-mechanically.
3. **Causal structure IS mandatory for Lorentzian geometry** (Malament's theorem). This is established.

## Success Criteria
- ✅ Novelty check completed: clear answer on whether this concept exists
- ✅ Physical picture in 2-3 paragraphs a non-physicist can follow
- ✅ Specific mechanism for HOW causal order selects the fakeon
- ✅ Self-assessment scores with honest justification
- ✅ Devil's advocate identifies at least 2 serious objections

## Failure Criteria
- ❌ Concept turns out to already exist (document who did it and what's new)
- ❌ No specific mechanism — just vague analogies between causality and the fakeon
- ❌ Classical→quantum gap not addressed

## Practical Notes
- Write REPORT.md skeleton IMMEDIATELY (first tool call)
- Directory: explorations/exploration-003/
- Aim for 150-250 lines
- Write REPORT-SUMMARY.md last
- If the concept fails the novelty check or the devil's advocate, that's a valid result — document WHY it fails
