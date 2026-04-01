# Strategy 002: The Operator Construction Tournament

## Objective

**Build** operators whose spectra approximate zeta zeros — do not merely test known candidates. Strategy-001 mapped the constraint landscape and proved that all published candidates fail. Strategy-002 uses that landscape as a construction blueprint. The goal is to produce at least one operator construction that (a) satisfies more of the 10-point constraint catalog than any known candidate, and (b) exhibits a property or connection that a domain expert in analytic number theory would recognize as a fresh contribution.

Secondary goal: resolve the critical open question from strategy-001 — whether the two-point trace formula (Montgomery's formula) shows that primes determine spectral correlations, contradicting the one-point formula's failure.

## Context

### What Strategy-001 Established

**10-point constraint catalog** (all computationally verified on 2000 zeros):

| # | Constraint | Value |
|---|-----------|-------|
| 1 | GUE symmetry class (β=2) | No time-reversal symmetry |
| 2 | Pair correlation matches Montgomery | 9% mean relative deviation |
| 3 | NN spacing matches GUE Wigner surmise | 4% mean absolute deviation |
| 4 | Poisson/GOE definitively ruled out | GOE 2x worse, Poisson 5x worse |
| 5 | Quadratic level repulsion | P(s) ~ s² for small s |
| 6 | Number variance saturates beyond GUE | Σ²(L) ~ 0.3-0.5 for L > 2 |
| 7 | Spectral rigidity saturates | Δ₃ = 0.156 for L > 15 |
| 8 | Form factor ramp-plateau | slope = 1.010, plateau = 1.043 |
| 9 | Super-rigidity | 30-50% more rigid than finite GUE |
| 10 | Periodic orbit structure | Saturation encodes Σ(ln p² / p) |

**What was ruled out:**
- All Berry-Keating xp regularizations (Sierra-Townsend, BBM PT-symmetric): 0/10
- One-point trace formula reconstruction: fundamentally fails (Gibbs phenomenon)
- Real symmetric arithmetic matrices (von Mangoldt Toeplitz, Hankel): Poisson or partial GOE, never GUE
- Simple encoding of primes into matrices: structure matters as much as content

**Key insight chain:**
GUE (β=2) requires a **complex** operator → primes must be encoded **non-trivially** → the operator carries MORE information than the trace formula (eigenvectors/matrix elements, not just eigenvalues) → matrix structure (how data is organized) matters as much as arithmetic content

**Critical open question:** Montgomery proved pair correlation IS determined by prime pairs (two-point formula). Strategy-001's exploration 005 crashed before computing this. Does the two-point formula succeed where the one-point fails?

### What the Mission Requires for Progress

From the validation guide: Tier 1 novelty means "a domain expert in analytic number theory would recognize a fresh contribution." Strategy-001 produced Tier 2-3 results (rigorous, evidenced) but zero Tier 1. This strategy must produce novelty.

## Methodology: Tournament → Deep Dive → Mandatory Adversarial

### Phase 1: Construction Tournament (3 explorations, CAN RUN IN PARALLEL)

Three independent attempts to construct an operator whose spectrum approximates zeta zeros. Each uses a different construction principle. Each scores its result against the 10-constraint catalog. **The constraint catalog score is the objective function — maximize it.**

**Tournament Entry A: Complex Arithmetic Matrices**
Strategy-001 proved real symmetric matrices can't reach GUE (β=2). Complex Hermitian matrices can. Construct:
- H_{jk} = Λ(|j-k|+1) · exp(2πi · θ_{jk}) where θ involves Dirichlet characters or Gauss sums
- H_{jk} = Λ(|j-k|+1) · χ(j-k) for various Dirichlet characters χ
- Explore what phase structure produces GUE statistics
- Use N = 500-2000 matrix sizes
- Score each construction against the full 10-constraint catalog
- **Key question: Does any choice of phases push β from 0.44 (real Hankel) toward 2.0 (GUE)?**

**Tournament Entry B: Optimization-Based Construction**
Reverse-engineer the operator from constraints. Start from a parameterized family of N×N Hermitian matrices and optimize to match:
- Target spacing distribution = GUE Wigner surmise
- Target pair correlation = Montgomery's formula
- Target number variance = observed zeta values (including saturation)
- Then examine the STRUCTURE of the optimized matrix — does it have arithmetic content? Toeplitz-like structure? What does the eigenvector structure look like?
- This is genuinely novel: nobody has tried to solve "what matrix produces these statistics?" as an optimization problem
- **Key question: Does the optimized matrix reveal interpretable structure?**

**Tournament Entry C: Two-Point Formula + Operator Reconstruction**
This is the retry of strategy-001's crashed exploration 005, extended with a construction step:
- Compute Montgomery's pair correlation formula explicitly from prime pairs
- Compare to numerical pair correlation from actual zeros
- If it works: use the two-point function to construct the kernel of an integral operator
- The pair correlation R₂(x,y) defines a reproducing kernel → the kernel's eigenfunctions define a Hilbert space → this IS an operator
- **Key question: Does the kernel operator constructed from the two-point formula satisfy more constraints than the one-point trace formula?**

**SCORING RULE:** Each entry reports its constraint catalog score (X/10 with partial credit) and any unexpected findings. The strategizer uses scores to allocate Phase 2.

### Phase 2: Deep Dive on Best Construction + Gap Filling (3-4 explorations)

Based on Phase 1 scores, the strategizer allocates explorations to deepen the most promising construction:

**If an entry scored ≥ 4/10:**
- Run 2-3 explorations deepening it: larger N, parameter sweeps, connections to known mathematics
- One exploration should scale to large N (use precomputed zero tables from LMFDB or Odlyzko for comparison — do NOT rely on mpmath for more than 2000 zeros)

**If no entry scored ≥ 4/10:**
- The strategizer should pivot to a different approach entirely. Options:
  - Li's criterion: RH ⟺ λₙ ≥ 0 for all n ≥ 1 where λₙ = Σ_{ρ}[1-(1-1/ρ)ⁿ]. Compute λₙ for large n. Look for patterns, asymptotics, monotonicity.
  - Nyman-Beurling criterion: RH ⟺ completeness of certain dilated functions in L²(0,1). Compute approximation quality as function of basis size.
  - Formal gap analysis in Lean 4: take the best existing proof strategy and formalize it until it breaks. Report exactly WHERE it breaks and WHAT axiom/lemma is missing.

**MANDATORY gap-filling exploration:** At least one Phase 2 exploration MUST quantitatively compare Berry's saturation prediction to the observed Δ₃ = 0.156. Berry's explicit formula predicts the saturation level in terms of specific prime sums. Compute it and report whether the observed and predicted values match. Strategy-001 identified this as "a clean, high-value computation" but never did it.

### Phase 3: Mandatory Adversarial Review + Synthesis (2-3 explorations, NON-NEGOTIABLE)

**The strategizer MUST execute Phase 3. This is not optional.** Strategy-001 skipped Phase 3 entirely and the mission suffered. Minimum allocation: 2 explorations.

**Exploration N-1 (MANDATORY): Adversarial Review**
Take the strongest claim from Phases 1-2 and try to destroy it:
- Search for the published paper that already contains this result
- Search for the computational error or artifact
- Identify the logical gap or unjustified assumption
- Test against an independent dataset (different zero range, different matrix size)
- Rate the claim: SURVIVED / WOUNDED / DESTROYED
- If DESTROYED: this is still valuable — report why it failed

**Exploration N (MANDATORY): Synthesis and Novel Claim Construction**
Survey ALL findings from this strategy and strategy-001. Ask:
- Which findings combine to produce something stronger than either alone?
- Is there a connection between the best operator construction and an equivalent formulation of RH?
- What is the single most novel, defensible finding of the entire mission so far?
- Write the finding as it would appear in a short paper: clear statement, evidence, limitations

## Validation Criteria

### This strategy succeeds if:
- At least one operator construction scores ≥ 4/10 on the constraint catalog (better than any S-001 candidate)
- At least one finding survives adversarial review (Phase 3 MUST happen)
- The two-point formula question is resolved (primes → correlations? yes or no?)
- A domain expert would recognize at least one result as non-trivial

### This strategy is exhausted if:
- All three tournament entries score ≤ 1/10 (construction approaches fundamentally don't work)
- Phase 2 deep dives don't improve scores (the construction is stuck)
- After 6 explorations, no computation has produced anything not in the published literature
- The strategizer reports that the constraint catalog is insufficient to guide construction

### What would count as a Tier 1 novel finding:
- An operator family whose spectra match ≥ 6/10 constraints (no published operator does this)
- A constructive proof that the pair correlation kernel defines a valid operator and what properties it has
- A new connection between the constraint catalog and an equivalent formulation of RH
- A computational result at scale (millions of zeros) that shows a deviation or pattern not in the published record
- A Lean 4 formalization that identifies an exact, previously uncharacterized gap in a known proof strategy

## Computation Platform Notes

**Use precomputed zero tables for large-scale statistics.** mpmath's zetazero() tops out at ~2000 zeros practically. For comparisons at scale:
- Andrew Odlyzko published tables of billions of zeros at height ~10²⁰
- LMFDB has extensive zero data
- For explorations needing > 5000 zeros, download and use these tables

**Python libraries:** mpmath (high-precision), numpy/scipy (fast numerics), sympy (symbolic), matplotlib (plotting). For optimization: scipy.optimize. For random matrix simulation: numpy.random + scipy.linalg.

**Lean 4 + Mathlib** is available for formal verification if any partial result emerges that's worth formalizing.
