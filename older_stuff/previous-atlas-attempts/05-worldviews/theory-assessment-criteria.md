# Theory Assessment Criteria

A structured framework for evaluating alternative theories and interpretations (e.g., quantum mechanics interpretations, cosmological models, consciousness theories).

## Purpose

When multiple theories explain the same observations, we need principled criteria to compare them. This framework scores theories across dimensions drawn from philosophy of science, enabling structured (and eventually automated) assessment.

**Related:** `tenet_stability_assessment.md` applies a similar lens to the 20 core tenets themselves — rating each tenet's stability and reinterpretation potential. This criteria doc is for evaluating *new theories* against those tenets.

---

## Evaluation Criteria

### 1. Empirical Adequacy (Hard Filter)

**Question:** Does this theory reproduce all known experimental results?

- This is pass/fail. If the theory contradicts established experimental data, it's out.
- For QM interpretations specifically: double-slit, Bell inequality violations, EPR correlations, Stern-Gerlach, quantum eraser, delayed choice, etc.
- Score: **Pass / Fail / Partial** (partial = explains most but has known gaps)

### 2. Internal Consistency

**Question:** Is the theory free of logical contradictions?

- Are the axioms mutually compatible?
- Do the mathematical formulations produce consistent results across different applications?
- Does it avoid paradoxes, or does it introduce new ones?
- Score: **1-5** (1 = known contradictions, 5 = formally proven consistent)

### 3. Parsimony (Occam's Razor)

**Question:** How much new stuff does this theory require?

Count and evaluate:
- Number of new axioms or postulates beyond standard theory
- Number of new entities (hidden variables, parallel universes, consciousness fields, etc.)
- Number of free parameters that must be tuned
- New fundamental forces or interactions

- Score: **1-5** (1 = extremely bloated, 5 = minimal additions)

### 4. Mathematical Precision

**Question:** Is the theory formalized enough to actually compute with?

- Is there a clear mathematical framework?
- Can you derive quantitative predictions from it (not just qualitative stories)?
- Are the equations well-defined, or do they rely on vague/undefined operations?
- Could it be implemented in a simulation or theorem prover?

- Score: **1-5** (1 = purely verbal/conceptual, 5 = fully formalized and computable)

### 5. Explanatory Scope

**Question:** Does this theory explain things the standard theory struggles with?

- Does it address known open problems? (measurement problem, wavefunction collapse, quantum gravity, etc.)
- Does it provide satisfying answers to "why" questions the standard theory leaves unanswered?
- Does it reduce the number of things we have to accept as brute facts?

- Score: **1-5** (1 = explains nothing new, 5 = resolves major open problems)

### 6. Novel Predictions

**Question:** Does it predict anything different that could be tested?

- Are there any observable differences from the standard theory, even in principle?
- Could a future experiment distinguish this theory from alternatives?
- Has it predicted anything that was later confirmed?

- Score: **1-5** (1 = identical predictions to standard, 5 = clear testable differences with feasible experiments)

### 7. Unification

**Question:** Does it connect previously separate phenomena?

- Does it bridge domains that are currently described by separate theories? (e.g., quantum + gravity, consciousness + physics)
- Does it reveal deeper structure underlying known relationships?
- Does it reduce the number of independent theories we need?

- Score: **1-5** (1 = siloed to one domain, 5 = major unification across domains)

### 8. Compatibility

**Question:** Does it play well with other established theories?

- Is it consistent with general relativity in the appropriate limits?
- Does it reduce to classical mechanics for macroscopic objects?
- Does it respect established symmetries (Lorentz invariance, CPT, gauge symmetries)?
- Is it compatible with thermodynamics (second law, etc.)?

- Score: **1-5** (1 = conflicts with established physics, 5 = seamlessly compatible)

---

## Scorecard Template

| Criterion | Score | Notes |
|---|---|---|
| Empirical Adequacy | Pass/Fail/Partial | |
| Internal Consistency | /5 | |
| Parsimony | /5 | |
| Mathematical Precision | /5 | |
| Explanatory Scope | /5 | |
| Novel Predictions | /5 | |
| Unification | /5 | |
| Compatibility | /5 | |
| **Total** | **/35** | |

---

## Automation Notes

**Automatable now:**
- Internal consistency → theorem provers (Lean, Coq, Isabelle) if formalized
- Empirical adequacy → test suite of canonical experimental results
- Parsimony → structured axiom/entity counting
- Compatibility → limit-checking (classical limit, relativistic limit)

**Partially automatable (LLM-assisted):**
- Explanatory scope → rubric-based evaluation with chain-of-thought
- Novel predictions → diff prediction sets against standard theory
- Formalization assistance → translate verbal theories into mathematical frameworks

**Requires human judgment:**
- Weighting criteria relative to each other
- Assessing "interestingness" — a theory can be wrong but point at real problems
- Evaluating whether a claimed novel prediction is genuinely distinct or just reframing
