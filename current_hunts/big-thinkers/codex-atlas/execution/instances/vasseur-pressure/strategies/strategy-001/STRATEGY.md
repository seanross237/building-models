# Strategy 001: Verify, Measure, Characterize

## Objective

Establish the computational and analytical foundation for the Vasseur pressure threshold problem. The central deliverable is a **measured value of the effective pressure exponent beta_effective** across DNS initial conditions and Reynolds numbers, plus a characterization of **which structural property of NS pressure** is responsible for any observed slack. This strategy determines whether the mission proceeds down Path A (slack exists, constructive attack) or Path B (no slack, obstruction mapping).

This is a ground-clearing strategy. It produces Tier 2-3 results (novel computational measurements + structural identification) and sets up a focused constructive Strategy 002.

## Methodology

### Three-Phase Protocol: Verify -> Measure -> Characterize

**Phase 0: Framework Verification (1-2 explorations)**

Before measuring anything, verify the target. One exploration reads Vasseur (2007) and extracts the **precise mathematical definition** of the pressure exponent beta in the De Giorgi iteration. Specifically:
- What functional does beta control? (Which term in which inequality at which iteration level?)
- What is the exact statement of Conjecture 14 / the Appendix result?
- What does beta > 3/2 give you? (Full L-infinity bound on weak solutions? Under what conditions?)
- Write beta_effective as a computable quantity: given a velocity field u on a grid, what do you evaluate?

This exploration produces: (a) a precise mathematical specification of beta, (b) a Python function skeleton `compute_beta_effective(u, p, params)` that the Phase 1 explorations will implement and run, (c) a clear statement of what beta > 3/2 implies, with equation numbers.

**Phase 0 gate:** If the exploration reveals that beta_effective CANNOT be meaningfully computed from DNS (e.g., it requires infinite-resolution limit-set operations that don't discretize), the strategy pivots immediately to analytical-only assessment. This is unlikely but must be checked.

**Phase 1: Parallel Computational Measurement (3-4 explorations, run concurrently)**

All Phase 1 explorations receive the beta_effective specification from Phase 0. They run independently.

Exploration types for Phase 1:
1. **DNS beta_effective measurement.** Pseudospectral DNS on T^3. Compute beta_effective across: Taylor-Green vortex, anti-parallel tubes, random IC, Kida vortex, Arnold-Beltrami-Childress flow. Reynolds numbers: Re = 100, 500, 1000, 2000, 5000. Two resolutions: N=64 and N=128 with convergence checks. Output: table of beta_effective(IC, Re, N) with error bars and convergence rates.

2. **CZ pressure decomposition.** For the same DNS runs, decompose pressure into harmonic and particular parts. Measure the CZ bound-vs-actual ratio for each component separately. Identify which component drives the universal 7.6-17.5x near-tightness found in the prior mission. Output: decomposition table with per-component slack ratios.

3. **Tran-Yu (2014) assessment.** Read Tran-Yu (2014, AIHP) carefully. Extract their specific claim about Galilean invariance improving the pressure term. Determine: (a) does their approach actually improve beta? (b) If so, to what value? (c) What exactly does Galilean invariance contribute — a better constant, a better exponent, or a structural improvement? (d) Is their result correct? Check their key estimates. Output: precise assessment with equation numbers.

4. **Structural property isolation.** Using DNS data, compare beta_effective for: (a) actual NS solutions, (b) synthetic fields with same energy spectrum but broken div-free constraint, (c) random div-free fields with same statistics but no quadratic structure. This isolates the contribution of each structural property (div-free, quadratic, Poisson). Output: table of beta_effective by property present/absent.

**Phase 2: Adversarial Review + Branch Determination (2-3 explorations)**

After Phase 1 results are in:
1. **Math adversarial recomputation.** An independent exploration re-derives beta_effective from Vasseur's paper and recomputes it on at least 2 ICs at the most important Reynolds number. Checks whether Phase 1's implementation matches the mathematical definition. This is mandatory — the prior NS mission showed numerical claims need independent recomputation.

2. **Synthesis + branch determination.** Reads all Phase 1 results. Produces: (a) the measured beta_effective landscape, (b) which structural property is most responsible for slack (if any), (c) clear determination of Path A vs Path B, (d) what the constructive Strategy 002 should target.

3. **(If needed) Standard adversarial review.** Novelty search + logical consistency check on the synthesis. Mandatory if the synthesis claims beta_effective > 4/3.

## Cross-Phase Rules (mandatory for every exploration)

1. **Compute, don't argue.** Every quantitative claim must come from running code, not from reasoning about what the answer "should" be. If an exploration says "beta_effective is approximately X," it must include the code that produced X and the numerical output.

2. **Computable function pairs.** Every bound or estimate discussed must be written as a Python function pair: `theoretical_bound(params)` and `actual_value(u, p, params)`. These accumulate across explorations and form the mission's computational infrastructure.

3. **Multi-IC validation.** No key finding may rest on a single initial condition. Minimum 3 ICs for any claimed result. The prior NS mission's single-IC dependence was a blind spot.

4. **Prescribed computation scale.** DNS runs require: >= 5 Reynolds numbers, >= 3 initial conditions, two-resolution convergence (N=64 and N=128 minimum). Any result without convergence checks is flagged [UNVERIFIED].

5. **Cite equations, not just papers.** "Vasseur (2007)" is insufficient. "Vasseur (2007), Theorem 3.1, equation (3.14)" is required. The validation guide demands this.

6. **Distinguish beta from CZ slack.** The CZ pressure bound measures bound-vs-actual for pressure values. Beta measures how pressure behaves under level-set iteration. These CAN decouple. Never conflate them. Every claim must state which quantity it refers to.

7. **Prior code available.** DNS infrastructure from the prior NS mission is at `execution/instances/navier-stokes/strategies/strategy-001/explorations/exploration-002/code/`. Reuse or rewrite, but don't start from scratch without reason.

## Validation Criteria

**Strategy succeeds if:**
- beta_effective is measured with convergence-checked values across >= 5 ICs and >= 5 Reynolds numbers
- The branch determination (Path A: slack exists vs Path B: no slack) is clear and adversarially reviewed
- At least one structural property (div-free, quadratic, Poisson) is quantitatively characterized for its contribution to beta_effective
- Tran-Yu (2014) is assessed with specific equation-level analysis
- CZ near-tightness decomposition is completed

**Strategy is exhausted if:**
- Phase 0 reveals beta_effective is not computable from DNS (pivot to analytical-only)
- Phase 1 measurements are consistent and adversarially verified — no further measurement will change the branch determination
- All prescribed computations are complete

**Success tiers for this strategy:**
- Tier 2-3: Measured beta_effective landscape + structural property identification + Tran-Yu assessment + CZ decomposition (the realistic target)
- Tier 4: Unexpected finding — beta_effective >> 4/3, or a structural property that clearly explains the gap, or Tran-Yu's approach gives a concrete path to improvement (possible but not expected from a ground-clearing strategy)

## Context

**From the prior NS mission (Strategy 001-002):**
- Vortex stretching bound is 237x loose (loosest in the chain)
- CZ pressure bound is universally 7.6-17.5x tight (tightest, unexplained)
- Enstrophy approach is a dead end (logical circle: BKM criterion == regularity)
- Vasseur (2007) Conjecture 14 / Appendix: beta > 3/2 => full regularity
- Current beta = 4/3. Gap to close: 1/6.
- Prior DNS code exists (pseudospectral solver, slack measurement infrastructure)

**From meta-learnings:**
- Cross-phase computable function pairs are the highest-value design decision for bound/estimate missions
- Phase 0 gates save entire strategies — the prior NS mission's Phase 0 gate exceeded threshold by 10^6
- Ground-clearing -> constructive is the natural two-strategy arc for Millennium-adjacent problems
- ONE task per exploration (never three approaches in one goal)
- Math adversarial recomputation catches errors that standard review misses
- "Modest but genuine" novelty is the realistic ceiling — a clean beta_effective measurement is a result even if it confirms beta = 4/3

## Budget Guidance

Target: 8-12 explorations. Phase 0: 1-2. Phase 1: 3-4 (parallel). Phase 2: 2-3. Early stopping is appropriate if branch determination is clear after Phase 1 + one adversarial review. Do not spend explorations on tightening or proving anything — that's Strategy 002's job.
