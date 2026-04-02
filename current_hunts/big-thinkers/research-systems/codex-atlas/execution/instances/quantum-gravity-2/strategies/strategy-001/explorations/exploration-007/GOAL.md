# Exploration 007: SCG v2.0 — Rewrite with Causal Order and Honest Assessment

## Scope

This is a NARROWLY SCOPED exploration. Do ONE thing well:

**Rewrite SCG's axioms with causal order replacing the symmetric cost function, then honestly assess what the revised theory achieves and what remains broken.**

Do NOT try to:
- Survey causal set theory comprehensively
- Address all flaws from exploration 005
- Develop new predictions in detail
- Prove the continuum limit

## The Problem

SCG v1.0 has 5 axioms. Axiom 3 defines a symmetric cost function c(x,y) = c(y,x) that is non-negative and satisfies the triangle inequality. This produces a positive-definite (Riemannian) metric. Physical spacetime is Lorentzian (one negative eigenvalue). This is a FATAL structural incompatibility.

## The Repair

Replace Axiom 3 with a causal order structure:

**New Axiom 3 (Causal Cost):**
- A partial order ≺ on Ω (x ≺ y means "x causally precedes y")
- A cost function c(x,y) ≥ 0 defined for x ≺ y (directed, not symmetric)
- A volume element v(x) > 0 for each configuration

The partial order gives causal structure. The Malament-Hawking theorem says: causal structure of a Lorentzian manifold determines it up to conformal factor. The volume element v(x) provides the conformal factor. Together: full Lorentzian geometry.

## What to Produce

### 1. SCG v2.0 Axioms (rewrite all 5, noting what changed)

Write the complete revised axiom set. Only Axiom 3 needs major changes, but check whether the other axioms need minor adjustments for consistency with the causal order.

### 2. Quick check: do the derivation chains survive?

For each chain, briefly note whether the causal order repair breaks it:
- **QM emergence (Barandes lifting):** Does it work with directed (asymmetric) transitions? Brief answer only.
- **Geometry emergence (Pedraza cost optimization):** Does it work with Lorentzian geometry? Brief answer only.
- **Bridge (Jacobson thermodynamics):** Does it survive? Brief answer only.
- **Collapse (Diósi-Penrose):** Does it survive? Brief answer only.

### 3. What the repair fixes

List specifically which devil's advocate attacks (from exploration 005) are addressed by this repair.

### 4. What remains broken

List specifically which attacks still stand.

### 5. Honest overall assessment

Is SCG v2.0 a genuine improvement? Or does the causal order repair introduce new problems? One-paragraph honest verdict.

## Key Context

**Causal set theory basics (you can look up more via web search):**
- A causet is a locally finite partially ordered set (poset)
- Malament's theorem (1977): The causal order of a distinguishing Lorentzian spacetime determines the spacetime up to conformal isometry
- Random sprinklings of points into Lorentzian manifolds (Poisson process) preserve Lorentz invariance statistically
- Sorkin's cosmological constant prediction: Λ ~ 1/√N where N = number of elements
- The causet → Lorentzian manifold continuum limit is established (Bombelli-Henson-Sorkin)
- CDT also uses causal structure to get Lorentzian signature — foliation gives natural time direction

**SCG v1.0 axioms (from exploration 003):**
1. Configuration Space: Finite set Ω, |Ω| = N
2. Stochastic Dynamics: Indivisible stochastic process, parameterized by τ
3. Cost Function: c(x,y) ≥ 0, symmetric, triangle inequality [THIS IS WHAT CHANGES]
4. Optimization: Macroscopic dynamics extremizes total cost
5. Irreducible Noise: Amplitude σ > 0

**Devil's advocate attacks (exploration 005) — severity ranking:**
- FATAL: Lorentzian signature
- NEAR-FATAL: QM is reformulation (not derivation), continuum limit unproven, Pedraza only 2D
- SERIOUS: No unique predictions, self-consistency unproven, ℏ renaming, Oppenheim not derived
- MODERATE: Undefined ontology, Diósi-Penrose constrained

## Output

Write to:
- `explorations/exploration-007/REPORT.md` — the rewrite and assessment
- `explorations/exploration-007/REPORT-SUMMARY.md` — concise summary

REPORT.md first. REPORT-SUMMARY.md as your FINAL action. Keep the report focused — aim for 200-400 lines, not 800.
