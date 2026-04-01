# Exploration 006: Repair SCG — Causal Structure, Lorentzian Signature, and Honest Reframing

## Mission Context

We built "Stochastic Computational Gravity" (SCG) — a theory where QM and spacetime emerge from a stochastic computation on a finite configuration space with a cost function. A devil's advocate exploration (005) found a FATAL flaw: the positive-definite cost function (Axiom 3) structurally cannot produce Lorentzian spacetime. Additional serious flaws: QM emergence is reformulation not derivation, continuum limit unproven, no unique predictions.

Your job: REPAIR SCG. Address the fatal flaw and the most serious weaknesses. Produce SCG v2.0.

## The Fatal Flaw: Lorentzian Signature

**The problem:** SCG's cost function c(x,y) satisfies: non-negative, symmetric, triangle inequality. This gives a positive-definite metric → Riemannian (Euclidean) geometry with elliptic operators. Physical spacetime requires Lorentzian geometry with hyperbolic operators (light cones, finite propagation speed, causality).

**Why this is fatal:** You cannot get causal structure from a positive-definite metric. Elliptic operators have global support — no light cones, no finite-speed propagation. This is not a gap; it's a structural impossibility.

## The Repair Strategy: Causal Order

**Key insight from causal set theory:** The Malament-Hawking-King-McCarthy theorem proves that the causal structure of a Lorentzian manifold determines the manifold up to a conformal factor. Causal structure → Lorentzian geometry (up to a scale).

**Proposed repair:** Replace the symmetric cost function with a DIRECTED structure:
- Replace Axiom 3 (symmetric cost c(x,y) = c(y,x)) with a partial order ≺ on Ω (causal order) PLUS a volume measure (conformal factor)
- The partial order gives causal structure → Lorentzian signature naturally
- The volume measure determines the conformal factor → full Lorentzian geometry

This is essentially incorporating the core insight of causal set theory into SCG's framework.

## Specific Tasks

### 1. Design SCG v2.0 Axioms

Rewrite the five axioms to fix the Lorentzian problem. Proposed modifications:
- **Axiom 1 (Configuration Space):** Keep — finite set Ω of N configurations
- **Axiom 2 (Stochastic Dynamics):** Keep — indivisible stochastic process
- **Axiom 3 (MODIFIED — Causal Cost Structure):** Replace symmetric cost with:
  - A partial order ≺ on Ω (x ≺ y means x is "before" y — the causal order)
  - A directed cost function c(x,y) defined only when x ≺ y (cost of transitioning from past to future)
  - A volume element v(x) for each configuration (determines the conformal factor)
  - The partial order + volume element → full Lorentzian geometry in the continuum limit
- **Axiom 4 (Optimization):** Modify to respect causal ordering
- **Axiom 5 (Noise):** Keep — irreducible noise amplitude

### 2. Check That the Repair Preserves What Worked

The original SCG had two derivation chains. Does the repair break them?
- **QM emergence:** Does the Barandes-Doukas lifting still work with directed transitions?
- **Geometry emergence:** Does the Pedraza cost optimization work with a causal order structure?
- **Bridge:** Does the Jacobson thermodynamic derivation survive?

### 3. Address the Other Serious Flaws

**QM emergence as reformulation:** Research whether anyone has proposed a physical (not just mathematical) argument for why stochastic processes are more fundamental than quantum mechanics. Is there an asymmetry in the correspondence? If not, honestly reframe SCG's QM emergence as "a reformulation with specific physical advantages" rather than "a derivation."

**Continuum limit:** Does the causal set literature provide mechanisms for continuum limits that produce Lorentzian manifolds? (Yes — Bombelli-Henson-Sorkin theorem shows random sprinklings converge to the manifold). Can SCG v2.0 import this?

**4D selection:** Does the causal order provide any mechanism for dimension selection? Causal set theory has some results on this (Myrheim-Meyer dimension estimator). Can SCG v2.0 use them?

**Unique predictions:** Can the causal version of SCG make at least ONE prediction that neither the component programs nor QG+F make? For example: a specific relationship between spacetime discreteness, decoherence rates, and complexity growth that only SCG predicts?

### 4. Write the Revised Theory

Present SCG v2.0 clearly:
- Revised axioms (with the causal order repair)
- Revised derivation chains (showing what changes)
- Revised predictions (noting any new ones)
- Revised gap list (which old gaps are fixed, which remain, any new gaps)
- Honest assessment: is this now a viable research program or still broken?

## Success Criteria

- **Success:** SCG v2.0 with repaired Lorentzian signature, preserved QM and geometry emergence, at least one honestly new prediction, and clear gap list.
- **Partial success:** Lorentzian signature repaired but other flaws remain unaddressed.
- **Failure:** The causal order repair breaks the QM or geometry emergence chains, making SCG v2.0 worse than v1.0.

## Relevant Context

**Causal set theory:** The causal set program (Bombelli, Lee, Meyer, Sorkin 1987) replaces spacetime with a locally finite partially ordered set (causet). Key results:
- Malament theorem: the causal order determines Lorentzian geometry up to conformal factor
- Hauptvermutung: a faithful embedding of a causet in a Lorentzian manifold is unique
- Sorkin's cosmological constant prediction: Λ ~ 1/√N (the only correct advance prediction in QG)
- Random sprinklings (Poisson process on manifold) preserve Lorentz invariance statistically

**CDT (Causal Dynamical Triangulations):** Gets 4D from causality conditions. Foliation structure produces Lorentzian signature by construction.

**Devil's advocate findings (exploration 005):**
- FATAL: Lorentzian signature (this exploration's primary target)
- NEAR-FATAL: QM emergence is reformulation; continuum limit unproven; Pedraza only in 2D
- SERIOUS: No unique predictions; self-consistency unproven; ℏ = 2mσ² is renaming
- MODERATE: Undefined ontology; Diósi-Penrose experimentally constrained

## Output

Write findings to:
- `explorations/exploration-006/REPORT.md` — detailed theory revision
- `explorations/exploration-006/REPORT-SUMMARY.md` — concise summary

REPORT.md first, progressively. REPORT-SUMMARY.md last.
