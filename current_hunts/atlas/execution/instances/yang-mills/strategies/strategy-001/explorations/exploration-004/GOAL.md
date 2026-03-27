# Exploration 004: Lattice-to-Continuum Limit — Bridging Numerical Evidence and Rigorous Proof

## Mission Context

This is a YANG-MILLS mission investigating the Millennium Prize Problem. Prior explorations established:
- Balaban's program achieves UV stability of 4D lattice YM on T⁴ but not observables, uniqueness, mass gap, or OS axioms
- The UV problem for 4D YM is solved (MRS 1993); the difficulty is entirely IR
- Constructive QFT toolkit breaks at d=4 (3 specific failure modes: cluster expansion divergence, large field problem, infinite RG convergence)
- φ⁴₄ is provably trivial (Aizenman-Duminil-Copin 2021); YM₄ expected to escape via asymptotic freedom but unproven

## Your Task

Produce a **precision technical map** of the lattice-to-continuum limit for Yang-Mills: what lattice practitioners and rigorous mathematical physicists know, what the gap is between numerical evidence and proof, and where specific proof strategies might succeed.

## Specific Deliverables

### 1. What lattice simulations have established numerically (but not rigorously)
- Confinement: area law for Wilson loops, string tension measurements
- Mass gap: glueball spectrum measurements (what are the best numbers? SU(2) and SU(3))
- Asymptotic scaling: how well do lattice results agree with perturbative asymptotic freedom predictions?
- Continuum limit: how lattice practitioners take a → 0 in practice, and what controls they use
- Universality: results from different lattice actions (Wilson, Symanzik-improved, etc.) agreeing in the continuum limit

### 2. The precise gap between lattice evidence and rigorous proof
For each major numerical result, identify:
- What exactly has been shown numerically
- What would need to be proved rigorously (what theorem is needed?)
- What specific mathematical obstacles prevent the proof
- Classification: NUMERICAL ONLY / PARTIALLY RIGOROUS / RIGOROUS

### 3. Rigorous lattice gauge theory results
What has been proved rigorously about lattice gauge theories? Include:
- Strong coupling results (Osterwalder-Seiler, Wilson, etc.): confinement at large coupling
- Brydges-Fröhlich-Seiler results on lattice gauge theories
- Chatterjee's recent results on Wilson loops and lattice YM
- Any rigorous continuum limit results (even partial)
- What does Chatterjee (2020) actually prove about the scaling limit? (His result gives a Gaussian limit — what does this mean?)

### 4. The continuum limit problem specifically
- What does "taking the continuum limit" mean rigorously? (Osterwalder-Schrader, Wightman, etc.)
- What is the relationship between lattice spacing a → 0 and bare coupling β → ∞?
- What does the renormalization group predict about this limit?
- Where exactly does the rigorous argument break down?

### 5. Most promising proof strategies
From the lattice perspective, what are the most promising strategies for a rigorous proof? Consider:
- Extending Balaban's program to control observables and prove uniqueness
- Stochastic quantization route (Chandra-Hairer et al.)
- Probabilistic approaches (Chatterjee's framework)
- Direct infinite-volume limit arguments
- Any novel strategies proposed in recent papers

For each, assess: what's the bottleneck? How close is it? What would a breakthrough look like?

## Success Criteria
- At least 5 specific numerical lattice results cataloged with their rigorous status
- The gap between numerical and rigorous clearly articulated for at least 3 major results
- At least 3 proof strategies assessed with specific bottlenecks identified
- References to actual papers (authors, years, arXiv IDs where available)

## Failure Criteria
- Only narrative descriptions without specific results
- No distinction between what's numerical vs. rigorous
- No assessment of proof strategies

## Output
Write results to:
- `REPORT.md` in this directory (target 400-600 lines)
- `REPORT-SUMMARY.md` — concise summary (50-100 lines)

Write REPORT-SUMMARY.md as your FINAL action.
