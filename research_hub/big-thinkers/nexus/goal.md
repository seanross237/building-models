---
type: hybrid
priority: quality
max_budget_tokens: none
max_time_hours: none
---

# Goal

Close the Vasseur pressure exponent gap: β = 4/3 → β > 3/2.

Vasseur (2007) showed that full Navier-Stokes regularity follows if the local pressure term in De Giorgi iteration achieves exponent β > 3/2. Current proofs only reach β = 4/3. The entire Millennium Prize Problem compresses to improving one exponent by 1/6.

This mission is a structured chain of investigation with kill conditions at each step. Each step feeds the next. If a step fails, the chain pivots rather than wasting resources.

## Prior Results (from Atlas NS mission)

A completed Atlas mission established:
1. The vortex stretching bound is 237× loose — the loosest inequality in the NS regularity proof chain.
2. The enstrophy approach is a dead end — it's logically circular (proving regularity via enstrophy requires controlling ||ω||_{L^∞}, which is equivalent to the BKM criterion, which is equivalent to regularity itself).
3. Vasseur (2007) identified the precise obstruction: De Giorgi iteration achieves β = 4/3, but β > 3/2 would imply full regularity (Vasseur's Conjecture 14 / Appendix).
4. The Calderón-Zygmund pressure bound is universally the tightest inequality in the proof chain (7.6–17.5× slack across ALL initial conditions). This robustness is unexplained and may point to deep structural constraints.

Prior mission DNS code: ~/nexus/knowledge/facts/prior-dns-code-location.md (reference to atlas codebase). Reuse or rewrite as needed.

## The Chain

### Step 1: Measure the effective pressure exponent in DNS

**What to do:**
- In high-resolution pseudospectral DNS on T³ (Taylor-Green vortex, anti-parallel tubes, random IC, Re = 100–5000), compute Vasseur's De Giorgi iteration quantities at each level k.
- Measure: what effective β does the actual pressure term achieve? Not the theoretical bound — the value realized by real NS solutions.
- Run at N=64 and N=128 with convergence checks.

**Parallel investigation:** Measure why the CZ pressure bound is universally the tightest (7.6–17.5× slack, ≤6× IC variation). Decompose pressure into harmonic + particular parts. Determine which component is responsible for the near-tightness. This may reveal the same structural insight that Step 2 needs, approached from a different angle.

**Kill conditions and branching:**
- If β_effective ≈ 4/3 consistently across ICs and Re → bound is tight against real solutions. The De Giorgi pressure limitation is fundamental, not a proof artifact. **Pivot to Step 2B.**
- If β_effective > 4/3 but < 3/2 → there's slack but not enough to solve the problem directly. **Proceed to Step 2A** — understand the structural source of the slack.
- If β_effective > 3/2 → bound is very loose. Strong signal that improvement is possible. **Proceed to Step 2A with high priority.**

**Why this might fail:** CZ pressure having 7.6–17.5× slack does NOT directly imply the De Giorgi pressure exponent has slack. CZ measures bound-vs-actual for pressure values; β measures how pressure behaves under level-set iteration. These could decouple.

**Output:** Table of β_effective across ICs × Re × resolution. CZ near-tightness decomposition.

### Step 2A: Identify what structural property the generic bound misses

**Triggered when:** DNS shows β_effective > 4/3 (slack exists).

**What to do:**
The pressure satisfies −Δp = ∂ᵢ∂ⱼ(uᵢuⱼ) with div(u) = 0. Generic Calderón-Zygmund theory treats the source as an arbitrary L^q function. It ignores three specific properties of NS pressure:

1. **Divergence-free constraint.** Only certain Fourier modes contribute. The source ∂ᵢ∂ⱼ(uᵢuⱼ) is really a divergence of a divergence because ∇·u = 0 — this is stronger than arbitrary L^q.
2. **Quadratic structure.** The source is u⊗u, not an arbitrary tensor. This has specific cancellation properties (e.g., trace condition from incompressibility).
3. **Poisson structure.** p is determined by u — it's not an independent field. Bounds that treat p and u as separate variables are inherently loose.

Computationally isolate which property creates the improvement:
- Compute β_effective for actual NS solutions vs. synthetic fields with the same energy spectrum but broken div-free constraint.
- Compute β_effective for NS solutions vs. random div-free fields (same statistics but no quadratic structure).
- This isolates the contribution of each property.

Also: **verify Tran-Yu (2014, AIHP).** They claim Galilean invariance improves the pressure term. Read the paper carefully — does their approach actually improve β? If so, to what value? What specifically does Galilean invariance contribute?

**Kill condition:** If the structural property exists but only improves β by a small amount (e.g., β' = 1.38 instead of 1.33), the gap to 3/2 is still too large for this approach alone. Note the improvement, publish it, but pivot to looking for additional independent improvements that could stack.

**Output:** Identification of which structural property (div-free, quadratic, Poisson) is responsible for the slack, with quantitative contribution of each. Tran-Yu assessment.

### Step 2B: Map the obstruction

**Triggered when:** DNS shows β_effective ≈ 4/3 (bound is tight).

**What to do:**
The bound is tight against real solutions — the limitation is in the NS equations themselves, not just the proof.

- Construct or identify the extremizing configuration — what flow geometry makes the pressure term as bad as β = 4/3? Is it a vortex tube? A shear layer? Something else?
- Determine if the extremizer is physically realizable or is a mathematical pathology that real turbulence avoids.
- Ask: is the limitation specific to De Giorgi iteration, or fundamental to any local regularity approach? Test by measuring the same quantity in CKN's and Lin's frameworks.

**Kill condition:** If the extremizer is physically realizable AND the limitation is fundamental to all local approaches → this chain is dead for the pressure path. Write up the negative result (valuable). **Pivot to Step 2C.**

**Output:** Characterization of the extremizing flow. Assessment of whether the limitation is De-Giorgi-specific or universal.

### Step 2C: Investigate whether blow-up might actually exist

**Triggered when:** Step 2B shows the obstruction is fundamental.

**What to do:**
- Search for near-singular events in DNS. Look for spacetime regions where scale-invariant dissipation E(r) grows fastest as r → 0.
- Study Tao's averaged NS blow-up (2016). What EXACTLY does the real NS nonlinearity have that Tao's averaged version doesn't? Identify a conserved quantity or cancellation that prevents blow-up.
- Test blow-up candidates: if DNS reveals near-singular configurations, extract as initial data for higher-resolution runs.
- Convex integration barriers (Buckmaster-Vicol, 2019): does this constrain what kind of regularity proof is possible?

**Kill condition:** If DNS at all accessible resolutions shows smooth behavior with E(r) bounded → blow-up is not computationally accessible. Write up findings with precise resolution/Re thresholds tested.

**Output:** Either evidence pointing toward blow-up candidates, or a characterization of what Tao's averaged NS is missing (which IS a roadmap for a regularity proof).

### Step 3: Prove an improved pressure estimate

**Triggered when:** Step 2A identified a usable structural property.

**What to do:**
Using the structural property from Step 2A, prove: for div-free u solving NS, the local pressure term satisfies a bound with exponent β' > 4/3.

Analytical routes (in order of promise):
1. **Div-free Calderón-Zygmund theory.** Brandolini-Chiacchio-Trombetti and related work.
2. **Quadratic cancellation.** In Fourier space, P(u·∇u) has cancellations that generic quadratic forms don't.
3. **Galilean covariance.** If Tran-Yu checks out, extend it.
4. **Pressure-velocity correlation from turbulence theory.** If empirical constraints can be made rigorous for individual realizations.

Even β' > 4/3 by any amount is novel and publishable.

**Kill condition:** If β' cannot exceed ~1.4 → write up whatever was achieved. The remaining gap characterizes exactly what mathematical insight is still needed.

**Output:** Proved bound with β' > 4/3, or clear characterization of why each route fails.

### Step 4: Feed improved estimate into Vasseur's framework

**Triggered when:** Step 3 achieves β' > 4/3.

**What to do:**
- If β' ≥ 3/2: Vasseur's Appendix (Conjecture 14) gives full regularity directly. Standard bootstrap → global regularity.
- If 4/3 < β' < 3/2: partial improvement — smaller singular set, or regularity for a restricted class. Characterize exactly how much improvement β' → dimension gives.

**Output:** If β' ≥ 3/2: proof of NS global regularity. If β' < 3/2: improved partial regularity result.

## Success Criteria

1. **Nobel-tier (0.1%):** β' ≥ 3/2 proved → NS global regularity → Millennium Prize
2. **Excellent (2.5%):** β' > 4/3 proved for any amount → first improvement to Vasseur's exponent since 2007
3. **Good (16%):** DNS measurement of β_effective + identification of the structural property responsible → novel computational result + clear roadmap
4. **Acceptable (40%):** β_effective measured across ICs/Re + CZ near-tightness explained + Tran-Yu assessed → solid synthesis with new data
5. **Minimum (90%):** Honest characterization of why the chain fails at whichever step → negative result that saves future researchers time

Partial credit matters. A clean β' = 1.4 with a proved theorem is better than a hand-wavy claim about β' = 3/2.

## Constraints

- Every claim tagged: [VERIFIED], [COMPUTED], [CHECKED], or [CONJECTURED]
- Function spaces specified precisely (Sobolev, Lebesgue, Besov)
- Domain stated for every result (T³ vs R³ vs bounded)
- Citations accurate (paper, authors, theorem/equation numbers)
- Computations reproducible with code provided
- Numerical claims distinguish "observed in simulation" from "proved"
- DNS must be validated against known benchmarks before measuring bound tightness
- The strongest counterargument against each finding has been identified and addressed

## Context

This builds on a completed Atlas NS regularity mission that identified the Vasseur pressure gap as the critical bottleneck. The prior mission found that the CZ pressure bound is universally the tightest (7.6–17.5× slack, ≤6× IC variation) — this robustness is unexplained and may reveal structure exploitable for proving β' > 4/3.

Seed knowledge from Yang-Mills and prior NS work is in ~/nexus/knowledge/. Operational meta-lessons from 10+ prior agent missions are in ~/nexus/knowledge/meta/.

## Key References

- Vasseur (2007), "A new proof of partial regularity of solutions to Navier-Stokes equations" — THE framework. Appendix / Conjecture 14 is the target.
- Tran-Yu (2014), AIHP — De Giorgi + Galilean invariance. Verify their claim.
- Caffarelli-Kohn-Nirenberg (1982) — baseline partial regularity
- Beale-Kato-Majda (1984) — BKM criterion
- Tao (2016) — averaged NS blow-up
- Vasseur-Yu, Cheskidov-Dai, Colombo-De Lellis-De Rosa — post-2007 De Giorgi approaches
- Brandolini-Chiacchio-Trombetti — div-free CZ theory
- Buckmaster-Vicol (2019) — convex integration / non-uniqueness barriers
- Protas et al. (JFM 2020) — adjoint optimization for enstrophy growth

## Available Tools

- Python (numpy 2.0.2, scipy 1.7.3, sympy 1.10.1, mpmath 1.2.1)
- SageMath 10.8
- Lean 4 + Mathlib
- pip install anything needed (dedalus spectral PDE solver available)
- Web search for papers
- Prior mission DNS code available (pseudospectral solver, slack measurement infrastructure)

## Expected Outputs

- artifacts/beta-effective-measurements.md — Table of β_effective across ICs × Re × resolution
- artifacts/cz-tightness-decomposition.md — Why CZ pressure is universally tight
- artifacts/structural-property-isolation.md — Which NS property (div-free, quadratic, Poisson) creates slack
- artifacts/tran-yu-assessment.md — Verification of Tran-Yu (2014) claims
- artifacts/improved-bound.md — Any proved β' > 4/3, or characterization of why routes fail
- artifacts/final-report.md — Complete writeup of the chain: what was tried, what worked, what failed, and why
