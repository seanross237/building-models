# Goal

Mission: Vasseur Pressure Threshold — Can We Close the Gap?

## Background

A prior Atlas mission on Navier-Stokes regularity established the following:

1. The vortex stretching bound is 237x loose — the loosest inequality in the NS regularity proof chain.
2. The enstrophy approach (the most popular attack strategy) is a dead end — it's logically circular. Proving regularity via enstrophy requires controlling ||omega||_{L^inf}, which is equivalent to the BKM criterion, which is equivalent to regularity itself.
3. Vasseur (2007) identified the **precise obstruction** to full regularity: the local pressure term in De Giorgi iteration achieves exponent beta = 4/3, but beta > 3/2 would imply **full regularity** (Vasseur's Conjecture 14 / Appendix). The gap is 4/3 -> 3/2.
4. The Calderon-Zygmund pressure bound is the universally tightest inequality in the proof chain (7.6-17.5x slack across ALL initial conditions). This robustness is unexplained and may point to deep structural constraints.

## The Goal

Determine whether the Vasseur pressure exponent gap (beta = 4/3, need beta > 3/2) can be closed, and if so, how. The entire Millennium Prize Problem compresses to improving one exponent by 1/6.

## The Chain

Each step feeds the next. Each has a kill condition — if the step fails, the chain pivots rather than wasting resources.

### Step 1: Measure the effective pressure exponent in DNS (~40-50% survival)

- In high-resolution pseudospectral DNS on T^3 (Taylor-Green vortex, anti-parallel tubes, random IC, Re = 100-5000), compute Vasseur's De Giorgi iteration quantities at each level k.
- Measure: what effective beta does the actual pressure term achieve? Not the theoretical bound — the value realized by real NS solutions.
- Run at N=64 and N=128 with convergence checks.
- Parallel investigation: Measure why the CZ pressure bound is universally the tightest (7.6-17.5x slack, <=6x IC variation). Decompose pressure into harmonic + particular parts.
- Kill condition: If beta_effective ~ 4/3 consistently across ICs and Re -> bound is tight, pivot to Step 2B. If beta_effective > 4/3 but < 3/2 -> proceed to Step 2A. If beta_effective > 3/2 -> proceed to Step 2A with high priority.
- Output: Table of beta_effective across ICs x Re x resolution. CZ near-tightness decomposition.

### Step 2A: Identify what structural property the generic bound misses (~40% survival)

Triggered when DNS shows beta_effective > 4/3. Investigate three NS-specific properties that generic CZ ignores:
1. Divergence-free constraint
2. Quadratic structure of u tensor u
3. Poisson structure (p determined by u)

Also verify Tran-Yu (2014, AIHP) claim that Galilean invariance improves the pressure term.

### Step 2B: Map the obstruction (~20% survival)

Triggered when DNS shows beta_effective ~ 4/3. Construct/identify the extremizing configuration. Determine if it's physically realizable. Test if limitation is De Giorgi-specific or fundamental.

### Step 2C: Consider that blow-up might actually exist (~15% survival)

Triggered when Step 2B shows obstruction is fundamental. Search for near-singular events in DNS. Study Tao's averaged NS blow-up (2016). Test blow-up candidates at higher resolution.

### Step 3: Prove an improved pressure estimate (~15% survival)

Using structural property from Step 2A, prove beta' > 4/3 via div-free CZ theory, quadratic cancellation, Galilean covariance, or pressure-velocity correlation.

### Step 4: Feed improved estimate into Vasseur's framework (mechanical)

If beta' >= 3/2: full regularity. If 4/3 < beta' < 3/2: improved partial regularity with smaller singular set.

## Key references

- Vasseur (2007), "A new proof of partial regularity of solutions to Navier-Stokes equations"
- Tran-Yu (2014), AIHP — De Giorgi + Galilean invariance
- Caffarelli-Kohn-Nirenberg (1982) — baseline partial regularity
- Beale-Kato-Majda (1984) — BKM criterion
- Tao (2016) — averaged NS blow-up
- Brandolini-Chiacchio-Trombetti — div-free CZ theory

## Prior work

Prior mission's DNS code is at `../../atlas/execution/instances/navier-stokes/strategies/strategy-001/explorations/exploration-002/code/` — pseudospectral solver, slack measurement infrastructure.

---
Received: 2026-03-30
Mission ID: m001-vasseur-pressure
