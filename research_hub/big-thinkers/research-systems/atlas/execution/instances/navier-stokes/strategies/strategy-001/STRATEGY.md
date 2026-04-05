# Strategy-001: Catalog-Measure-Tighten

## Objective

Map the load-bearing inequalities in 3D Navier-Stokes regularity theory, computationally measure the slack in each one, rank them by looseness, and attempt to prove a tighter version of the loosest. This is a ground-clearing + computational attack strategy — it should produce a ranked "slack atlas" of key estimates and, ideally, one tightened bound as a novel contribution.

## Methodology

Three-phase protocol: **Catalog → Measure → Tighten**. Every phase requires computation — no phase is purely conceptual.

### Phase 1: Catalog the Estimates (2-3 explorations)

**Goal:** Identify and precisely state every load-bearing inequality in the major regularity results. For each estimate, extract:
- The exact mathematical statement (function spaces, norms, constants)
- Where it enters the proof (which theorem, which step)
- What it bounds (energy, enstrophy, vorticity, etc.)
- Its scaling behavior (how the bound and actual value scale with Reynolds number)
- Whether the constant is explicit or existential

**Targets (at minimum):**
- Caffarelli-Kohn-Nirenberg (1982): the local energy inequality, the "suitable weak solution" estimates, the covering argument
- Prodi-Serrin-Ladyzhenskaya criteria: the interpolation inequalities that connect L^p_t L^q_x regularity to energy bounds
- Escauriaza-Seregin-Šverák (2003): the backward uniqueness estimates, Carleman inequalities
- Ladyzhenskaya inequality itself: ||u||_4 ≤ C ||u||^{1/4}_{L²} ||∇u||^{3/4}_{L²} (3D)
- Sobolev embedding and interpolation bounds used throughout
- Any Gronwall-based estimates that control growth rates

**Explorer type:** One standard explorer for the literature survey (extract exact statements from papers), one math explorer to verify the dimensional analysis and write down each inequality in computable form (as Python functions that take flow fields and return bound vs. actual).

**Cross-phase rule:** Every identified estimate must be written as a pair of Python functions: `bound(u, params) → float` and `actual(u, params) → float`, where the ratio `bound/actual` is the slack factor. These functions are the deliverable of Phase 1 — Phase 2 will call them on simulated flows.

### Phase 2: Computational Measurement (5-7 explorations)

**Goal:** Run 3D Navier-Stokes simulations and measure the slack factor for each cataloged estimate across a range of flows.

**Simulation infrastructure:**
- Pseudospectral solver on the 3D periodic torus T³ (dealiased with 2/3 rule or phase-shift)
- Resolution: at minimum N=64³, with convergence checks at N=128³ for key results
- Reynolds numbers: Re = 100, 500, 1000, 5000 (at minimum 4 values spanning 2 orders of magnitude)
- Time evolution: run to statistical steady state, then sample over at least 10 large-eddy turnover times
- Viscosity tracked explicitly in all results

**Initial conditions to test (each exploration picks a subset):**
1. **Taylor-Green vortex** — standard benchmark, known to develop strong vorticity growth
2. **Random-phase Gaussian** — typical turbulent initial data at specified energy spectrum
3. **Kida vortex** — high-symmetry flow, computationally cheaper
4. **Concentrated vortex tubes** — adversarial: thin vortex tubes designed to stress Sobolev embeddings
5. **Vortex sheets** — adversarial: high-gradient structures
6. **Near-singular data** — adversarial: initial data with ||∇u||_{L²} as large as resolution allows

**Measurement protocol for each estimate:**
- Compute `bound(u(t), params)` and `actual(u(t), params)` at each timestep
- Record the time-averaged slack ratio, the minimum slack ratio (worst case), and the trend as Re increases
- For minimum 5 Reynolds numbers per estimate per initial condition
- Report: which estimate, which initial condition, Re range, slack ratio (mean ± std), trend with Re

**Mandatory adversarial exploration:** At least one exploration (slot 5-6) must specifically search for initial conditions that MINIMIZE the slack ratio. Use gradient-based optimization or parametric sweeps over vortex tube configurations (radius, aspect ratio, circulation) to find the tightest approach to each bound.

**Computation scale requirements:**
- Minimum 5 Reynolds numbers per slack measurement
- Minimum 3 independent initial conditions per estimate category (typical, adversarial)
- Resolution convergence: every slack ratio must be reported at two resolutions
- Error bars: statistical uncertainty from time-averaging must be quantified

### Phase 3: Tighten and Verify (3-4 explorations)

**Goal:** Take the loosest estimate (largest, most robust slack factor) and attempt a tighter version. Then adversarially review.

**Tightening approaches (Strategizer chooses based on Phase 2 results):**
- If the slack is in a multiplicative constant: compute the sharp constant or a tighter one
- If the slack is in the exponent: check whether a different interpolation path gives a tighter power
- If the slack is structural (e.g., Gronwall exponential vs. actual polynomial growth): prove the actual growth rate
- If the slack is in a covering/geometric argument: tighten the covering

**Mandatory adversarial review:** The final exploration (or second-to-last) must be an adversarial review of the strategy's best claimed result. The reviewer must:
- Check if the tightened bound has been published before (search arXiv, MathSciNet terms)
- Verify the computation independently (rerun key simulations from scratch)
- Try to construct a counterexample to the tightened bound
- State the strongest reason the result might be wrong or not novel

## Validation Criteria

**Strategy succeeds if:**
- A ranked slack atlas of ≥5 estimates is produced, with quantified slack factors across ≥3 Reynolds numbers and ≥2 initial condition types (Tier 2: Rigor)
- At least one estimate is identified as having slack factor >10× across all tested conditions (Tier 3: Novelty if not previously quantified)
- A tightened version of the loosest estimate is proposed with analytical or computational evidence (Tier 4: Significance)
- The best result survives adversarial review (Tier 5: Defensibility)

**Strategy is exhausted if:**
- All major estimates turn out to be tight (slack <2× for all, approaching 1 as Re increases) — this would itself be a surprising finding worth documenting
- Phase 2 reveals that the estimates are too loose to be load-bearing (they were always loose and nobody uses them tightly) — pivot to finding which estimates ARE tight
- Computational resources are insufficient for the required resolution

## Context

- **No prior strategies.** This is strategy-001 for the Navier-Stokes mission.
- **No existing library entries** on Navier-Stokes. All knowledge must be built from scratch.
- **Lessons from other missions:**
  - "Computation mandatory" is the single most important rule (SED, Yang-Mills missions)
  - Survey explorations at the start pay for themselves (SED, Yang-Mills)
  - Adversarial review should come at exploration 6-7 or at most second-to-last, not final (Yang-Mills, Riemann)
  - Prescribe computation scale (minimum data points, resolution, Re range), not just "compute" (Yang-Mills)
  - Pre-load all verified results from earlier explorations into later goals (SED: 2× speedup)
  - First strategy = ground-clearing. Don't expect Tier 5 novelty from strategy-001. A quantified slack atlas is the realistic target.
- **Tao's 2016 obstruction** is the key theoretical constraint: any regularity proof must use specific structural properties of the NS nonlinearity. Slack in estimates that DON'T depend on the nonlinearity structure may be real slack; slack in estimates that DO depend on it may be where the real proof barrier lives.
