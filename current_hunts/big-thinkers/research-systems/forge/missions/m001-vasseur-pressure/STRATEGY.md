# Strategy

## Mission
Determine whether the Vasseur pressure exponent gap (beta = 4/3, need beta > 3/2) can be closed by measuring the effective exponent in DNS, identifying structural properties the generic bound misses, and attempting to prove an improved estimate.

## Architecture
Depth 2: Planner + Workers. Single serial workstream with branching. Code, Math, Research, Analysis, and Adversarial workers as needed per phase.

## Approach

Follow the 4-step chain from the mission goal. Each step has explicit kill conditions — evaluate them honestly and pivot when triggered. Do not proceed past a failed kill condition.

**Critical first step:** Set up a pseudospectral DNS solver on T^3 and validate it before ANY measurement. Prior Atlas code exists at `../../atlas/execution/instances/navier-stokes/strategies/strategy-001/explorations/exploration-002/code/` — evaluate whether to reuse or rewrite. Validation target: Taylor-Green vortex enstrophy evolution against published results.

**The measurement that determines everything:** Compute Vasseur's De Giorgi iteration quantities from DNS data. Extract the effective pressure exponent beta_effective. This measurement must be:
- Converged across resolution (N=64 vs N=128)
- Tested across multiple ICs (Taylor-Green, anti-parallel tubes, random)
- Tested across multiple Re (100-5000)
- Clearly distinguishable from beta = 4/3 if there is slack

## Phases

### Phase 1: DNS Infrastructure (Tasks 1-3)
- **Objective:** Working, validated pseudospectral NS solver on T^3 with De Giorgi quantity extraction
- **Task budget:** 2-3 tasks
- **Success criteria:** Solver reproduces Taylor-Green vortex benchmark. De Giorgi iteration quantities computable from output.
- **Depends on:** Nothing

### Phase 2: Measurement (Tasks 4-6)
- **Objective:** Table of beta_effective across ICs x Re x resolution. Also CZ pressure decomposition.
- **Task budget:** 2-3 tasks
- **Success criteria:** beta_effective measured with convergence checks. Clear determination of whether beta_effective > 4/3.
- **Depends on:** Phase 1 (validated solver)
- **Branch point:** Result determines Phase 3.

### Phase 3: Investigation (Tasks 7-9)
- **Objective:** Depends on Phase 2 result.
  - If beta_effective > 4/3: Step 2A — identify which structural property (div-free, quadratic, Poisson) creates slack. Verify Tran-Yu.
  - If beta_effective ~ 4/3: Step 2B — map the extremizing configuration. Test if limitation is De Giorgi-specific.
  - If 2B shows fundamental obstruction: Step 2C — investigate blow-up, study Tao (2016).
- **Task budget:** 2-3 tasks
- **Success criteria:** Identified structural property (2A), or characterized obstruction (2B), or blow-up investigation results (2C).
- **Depends on:** Phase 2 measurement

### Phase 4: Proof Attempt (Tasks 10-12, if reached)
- **Objective:** Prove beta' > 4/3 using structural property from Phase 3.
- **Task budget:** 2-3 tasks
- **Success criteria:** Proved bound with beta' > 4/3, or clear characterization of why each analytical route fails.
- **Depends on:** Phase 3 (Step 2A success)

## Validation Criteria

Mission is "done" when one of:
1. beta' >= 3/2 proved and fed into Vasseur framework (Nobel-tier — extremely unlikely)
2. beta' > 4/3 proved for any amount (Excellent — first improvement since 2007)
3. beta_effective measured + structural property identified (Good — publishable computational result)
4. beta_effective measured + obstruction characterized (Acceptable — maps the boundary)
5. All steps fail with honest characterization of why (Minimum — negative result, still valuable)

Quality bar: every claim tagged [VERIFIED], [COMPUTED], [CHECKED], or [CONJECTURED]. Numerical claims distinguish simulation from proof. Partial results valued — don't overstate.

## Context from Library
No prior Forge context available (first mission). Prior Atlas NS mission results referenced in GOAL.md.

## Risk and Mitigation

| Risk | Mitigation |
|---|---|
| DNS solver bugs → wrong beta_effective | Validate against Taylor-Green benchmark BEFORE measurement |
| Resolution too low for convergence | Run N=64 and N=128, check convergence. If insufficient, note the gap. |
| beta_effective measurement is ambiguous (close to 4/3 but uncertain) | Use multiple ICs and Re values. Statistical analysis of spread. |
| Step 2A identifies structural property but it's not exploitable analytically | Quantify the improvement precisely. Even beta' = 1.35 is a result. |
| Proof attempt in Step 3 fails | Document exactly where and why each route fails. This maps what insight is still needed. |
| Context window exhaustion on long computation tasks | Workers handle single tasks. Planner resets between tasks via stop hook. |
