# Exploration 002: Scrutinize Bianconi's Entropic Action Quantum Gravity (2025)

## Mission Context

We are developing a novel theory of quantum gravity. Our survey (exploration 001) identified Bianconi's 2025 "entropic action" proposal as the most concrete candidate from Route 5 (alternative constructive axioms). This paper claims to derive gravity from quantum relative entropy, with predictions including emergent cosmological constant and a G-field candidate for dark matter.

Before spending multiple explorations constructing new theories from abstract axioms, we need to determine whether this existing concrete proposal is viable.

## Your Specific Goal

Provide a thorough critical assessment of Bianconi's entropic action quantum gravity. Specifically:

### Task 1: Reconstruct the Proposal
- Find and read Bianconi's 2025 paper (Phys. Rev. D) on gravity from quantum relative entropy / entropic action
- Reconstruct the key claim: gravity's action IS the quantum relative entropy S(ρ_metric || ρ_matter)
- What are the specific mathematical ingredients? What fields, what action, what equations of motion?
- What predictions does the paper make?

### Task 2: Novelty Assessment
- Is this genuinely new, or a reformulation of Jacobson (1995/2015), Verlinde (2010), Padmanabhan, or Sakharov?
- How does it differ from each of these existing programs?
- Has it been cited? Any follow-up work or critiques?

### Task 3: Tier 1 Validation (Structural Sanity)
Run the proposal through structural sanity checks:
- **Correct degrees of freedom**: Does it reproduce the massless spin-2 graviton?
- **Unitarity**: Is there a well-defined Hilbert space with positive-definite norm?
- **Ghost freedom**: Are there ghost modes?
- **UV completion**: Does it actually address the UV problem, or is it only an IR/classical reformulation?
- **Diffeomorphism invariance**: Is the theory generally covariant?
- **Weinberg-Witten theorem**: The graviton cannot be composite in a Lorentz-covariant theory with a conserved, gauge-invariant energy-momentum tensor. Does this proposal evade this? (Known escapes: holography, broken LI, or using GR's pseudo-tensor nature)

### Task 4: Tier 2 Validation (Known Physics Recovery)
If the proposal passes Tier 1, check:
- Does it recover Newton's law?
- Does it reduce to GR in the appropriate limit?
- Are the PPN parameters correct?
- Is the gravitational wave speed c?

### Task 5: Assessment of Predictive Claims
- The paper claims emergent Λ (cosmological constant) — is this a genuine prediction or does it depend on tunable parameters?
- The paper claims a "G-field" dark matter candidate — what is this? Is it testable?
- Are there any other predictions?
- Compare predictions to QG+F (quadratic gravity with fakeon): r ∈ [0.0004, 0.0035], n_s ≈ 0.967

### Task 6: Overall Verdict
- Is this a viable quantum gravity theory? (Yes / No / Partially — explain)
- What specifically does it get right that other approaches don't?
- What are its fatal flaws (if any)?
- Is it worth pursuing further, or should we move on to other candidates?
- If it fails, what lessons does the failure teach about information-theoretic approaches to QG?

## Success Criteria
- A clear reconstruction of the mathematical proposal
- Unambiguous verdicts on Tier 1 and Tier 2 checks
- Assessment of whether this is genuinely novel or a reformulation
- A recommended decision: pursue further or move on

## Failure Criteria
- Unable to find the paper
- Vague assessment without specific mathematical checks
- No comparison to existing entropic gravity programs

## Relevant Context

**Existing entropic gravity programs (from the library):**
- **Jacobson 1995**: δQ = TdS at local Rindler horizons → Einstein equations. Not a UV completion — it's a reformulation of GR as thermodynamics.
- **Jacobson 2015**: Maximal vacuum entanglement hypothesis → Einstein equations from entanglement equilibrium. Still only recovers Einstein equations (not a UV completion).
- **Verlinde 2010**: Gravity as entropic force. Derives Newton's law from Bekenstein entropy + Unruh temperature. Predicts MOND-scale acceleration a_0 = cH_0/6. Fails at cluster scales, can't predict CMB.
- **Padmanabhan**: Field equations = TdS = dE + PdV on any horizon. Natural CC perspective via shift invariance.
- **Sakharov 1967**: One-loop effective action → induced Einstein-Hilbert term. But generates Λ ~100 orders too large.

**Known criticisms of entropic gravity:**
- Kobakhidze: Neutron interference experiments show quantum coherence in gravitational fields, inconsistent with fundamentally thermal/entropic gravity.
- Carlip: Gauge symmetry problem (how does diffeomorphism invariance emerge?), Weinberg-Witten constraints.

**Tier 1-2 validation criteria:**
- 32 constraints, 15 independent. Top 5: UV completion, unitarity+ghost freedom, diffeo invariance, LIV bounds, BH entropy.
- Weinberg-Witten theorem: graviton cannot be composite in Lorentz-covariant theory with conserved T^{μν}. Escapes: holography, broken LI, GR's pseudo-tensor nature.

**The QG+F benchmark (what any new theory must beat):**
- Passes all Tier 1-3 checks
- Prediction: r ∈ [0.0004, 0.0035], n_s ≈ 0.967
- Cost: microcausality violation at Planck scale
- Open problem: cosmological constant (the "new CC problem")

## Instructions
- Write your report to `explorations/exploration-002/REPORT.md`
- Write your summary to `explorations/exploration-002/REPORT-SUMMARY.md`
- **IMPORTANT: Write incrementally, section by section.** Write the skeleton first, then fill in as you work.
- Use web search to find the actual paper and any citations/critiques
- Be ruthlessly honest in the assessment — a clear "this doesn't work because X" is more valuable than a diplomatic hedge
