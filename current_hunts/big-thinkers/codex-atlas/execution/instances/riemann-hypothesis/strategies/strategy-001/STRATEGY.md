# Strategy 001: Computational Constraint Cartography

## Objective

Map the landscape of *computable* constraints on the hypothetical Riemann operator — the undiscovered self-adjoint operator whose eigenvalues would be the non-trivial zeros of the Riemann zeta function — and use numerical computation to test, tighten, or falsify specific candidates. The goal is not a survey of the literature but a catalog of **numerically verified constraints** with code that reproduces every claimed result, and at least one finding that a domain expert would consider a fresh contribution.

## Context

This is strategy-001. No prior strategies exist. The problem space is vast — 160+ years of work on RH across analytic number theory, random matrix theory, operator theory, and quantum chaos. Rather than trying to survey everything, this strategy takes a specific angle: treat the Riemann zeros as empirical data and the operator question as an engineering problem. What must the operator look like? What can computation tell us that pure analysis cannot?

The mission identifies the spectral approach as the most promising avenue. Key threads:
- **Montgomery-Odlyzko**: pair correlation of zeta zeros matches GUE (Gaussian Unitary Ensemble) statistics from random matrix theory
- **Berry-Keating conjecture**: the Riemann operator is a quantization of the classical Hamiltonian H = xp
- **Hilbert-Polya conjecture**: zeros are eigenvalues of a self-adjoint operator
- **Selberg trace formula**: connects spectral data to geometric data on hyperbolic surfaces
- **De Bruijn-Newman constant**: Rodgers-Tao (2020) proved Lambda >= 0, consistent with RH (Lambda = 0)

## Methodology

### Phase 1: Constraint Extraction and Numerical Verification (3 explorations)

**Goal:** Extract precise mathematical constraints from three independent domains and verify each computationally.

Each exploration targets ONE domain and must produce:
1. A list of explicit mathematical conditions the Riemann operator must satisfy (not vague statements — equations)
2. Code that numerically verifies each condition against known zeros (use mpmath for high-precision zeta zeros)
3. A quantitative measure: how constraining is this condition? How much of "operator space" does it eliminate?

Suggested domains (Strategizer should choose based on what looks most promising):
- **Random matrix theory**: GUE statistics (pair correlation, nearest-neighbor spacing, number variance, form factor). Compute these for the first N zeros at various heights and compare to GUE predictions. Look for deviations or sub-leading corrections that are under-studied.
- **Explicit formulas / trace formulas**: Weil's explicit formula, Guinand's formula. These give exact relationships between zeros and primes. Implement them numerically and extract what they imply about operator structure.
- **Quantum chaos / semiclassical methods**: Berry's semiclassical analysis of the Riemann zeros, periodic orbit theory, connections to the Gutzwiller trace formula. What does semiclassical quantization predict about the operator?
- **Moment conjectures**: Keating-Snaith moment conjectures and their implications for operator statistics. Compute high moments of zeta on the critical line and compare.

**Critical rule for this phase:** Every constraint must be accompanied by a computation. "The pair correlation matches GUE" is not enough — the explorer must compute the pair correlation function for zeros at height T, compare to GUE prediction to precision X, and report any deviations. A computed number with error bars is worth infinitely more than a qualitative statement.

### Phase 2: Operator Candidate Testing (4 explorations)

**Goal:** Take the constraint catalog from Phase 1 and computationally test specific operator candidates against it.

Each exploration should:
1. Pick a specific operator candidate (or class of candidates)
2. Compute its spectrum numerically
3. Check how many Phase 1 constraints it satisfies
4. Identify exactly which constraints it fails and by how much
5. If it fails, determine whether the failure is fundamental or could be fixed with modifications

Candidate families to consider (Strategizer should prioritize based on Phase 1 results):
- **Berry-Keating xp variants**: H = xp and its regularizations (e.g., Sierra-Townsend regularization, Bender-Brody-Mueller PT-symmetric variant). Compute spectra and compare to zeta zeros.
- **Laplacians on specific manifolds**: Does any known manifold's Laplacian have a spectrum that resembles zeta zeros? Numerical spectral computations on hyperbolic surfaces.
- **Random matrix realizations**: Construct explicit random matrices from GUE and compare individual eigenvalue statistics to zeta zeros — are there systematic differences?
- **Toeplitz/Hankel operators**: Operators constructed from arithmetic functions whose spectral properties might encode zeta zeros.
- **Novel combinations**: If Phase 1 reveals that constraints from different domains are unusually compatible, try to reverse-engineer an operator from the constraints themselves.

**The highest-value outcome from this phase** would be: discovering that a specific operator candidate satisfies constraints from multiple independent domains better than previously documented, OR discovering that a widely-cited candidate fails a constraint that hasn't been checked before.

### Phase 3: Synthesis and Novel Claim Construction (3 explorations)

**Goal:** Synthesize findings into defensible claims. Each exploration in this phase should either:
- Strengthen a promising finding from Phase 2 with additional computation
- Run an adversarial check on the strongest claim (try to break it)
- Attempt a synthesis across domains — are two "separate" constraints actually the same constraint in disguise?

At least one exploration should be an adversarial review: take the best finding and try to demolish it. Find the published paper that already said it. Find the computation error. Find the logical gap. If the finding survives, it's worth reporting. If it doesn't, that's just as valuable.

## Validation Criteria

### Success indicators (this strategy is working if):
- Explorations are producing computations with actual numbers, error bars, and code
- The constraint catalog is growing with each exploration — new conditions the operator must satisfy
- At least one operator candidate is being tested against multiple constraints from different domains
- Something unexpected appears — a constraint fails where it shouldn't, or two constraints turn out to be equivalent

### Exhaustion indicators (time to stop or pivot if):
- Explorations are producing literature reviews instead of computations
- All constraints extracted are well-known and already in the literature with the exact numerical values we compute
- Operator candidates are failing all constraints trivially (the approach isn't discriminating)
- After 5 explorations, no computational result has produced anything surprising

### What would count as a novel finding:
- A numerical deviation from GUE statistics at specific zero heights that hasn't been published
- An operator candidate that satisfies a constraint it wasn't designed for
- A proof that two independently-motivated constraints are mathematically equivalent
- A computational falsification of a candidate that was considered viable
- A new tighter bound derived by combining constraints from different domains
