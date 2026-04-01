# Mission: Beyond De Giorgi — What Structural Property Could Break the NS Regularity Barrier?

## Background

Two independent systems (Atlas and Philosopher Atlas) have conclusively established that the De Giorgi-Vasseur framework is exhausted for 3D Navier-Stokes regularity:

**Atlas findings (18 explorations, 2 strategies):**
- β = 4/3 is rigorously sharp. All four De Giorgi proof steps (energy definition → Sobolev H^1→L^6 → parabolic interpolation to L^{10/3} → Chebyshev level-set) are individually tight under NS constraints.
- Tool-independent: CZ, IBP, H^1/BMO duality, CRW commutators all give β ≤ 4/3.
- Universal formula: β = 1 + s/n. For 3D NS: s/n = 1/3, need s/n ≥ 1/2. The gap is 1/6.
- The Lamb vector L = ω × u generates the CZ-lossy pressure piece. For Beltrami flows (L = 0), CZ loss vanishes — but mechanism doesn't survive even 1% perturbation from Beltrami alignment.
- Vorticity formulation (Vasseur-Yang 2021) also gives 4/3 — the barrier is the quadratic nonlinearity, not the pressure formulation.
- Constant field u = (c,0,0) simultaneously extremizes 3 of 4 De Giorgi chain steps. One-line sharpness proof.

**Philosopher Atlas findings (4 explorations):**
- Three H^1 pressure routes tested (H^1-BMO duality, atomic decomposition, interpolation) — all failed.
- Universal obstruction: W^{1,3} wall. W^{1,2} (what Leray-Hopf gives) does not embed in BMO (needs W^{1,3}).
- Local pressure closes (σ = 3/5 > 0). Far-field pressure is the sole obstruction.
- Even with hypothetical W^{1,3} regularity, H^1-BMO is structurally WORSE than Hölder (loses U_k^{1/2} factor). Wrong tool entirely.
- Bogovskii corrector introduces 2^{2k} compound growth — eliminates all localization strategies.

**The Tao constraint (2016):**
Tao proved that any method based solely on energy identity + harmonic analysis CANNOT resolve NS regularity. He showed blowup exists for an averaged version of NS that preserves energy identity and all standard harmonic analysis structure. Therefore, the proof (if NS is regular) MUST use some specific property of the actual NS nonlinearity that the averaged version lacks.

Our β = 4/3 sharpness is a concrete quantitative instance of Tao's general obstruction.

## The Goal

**Primary question:** What specific structural property of the 3D Navier-Stokes equations — not captured by energy identity + harmonic analysis — could bypass the De Giorgi β = 4/3 barrier and provide a path toward regularity?

This is NOT "try random approaches and hope." The Tao constraint gives us a precise filter: the property must distinguish the actual NS nonlinearity from the averaged version. The SQG success gives us a concrete example of what "using the right structural property" looks like.

**What success looks like:**
- Identify 1-2 structural properties of NS that (a) are absent from Tao's averaged equations, (b) are present in SQG-like equations where regularity is proven, and (c) could plausibly feed into a non-De-Giorgi regularity proof.
- For each candidate property, assess whether it can be operationalized into a concrete mathematical attack.
- Produce an obstruction map of the non-De-Giorgi landscape: what approaches exist, which ones could exploit the identified properties, which ones have been tried and failed.

**What failure looks like:**
- All identified structural properties are either already exploited (and insufficient) or cannot be operationalized.
- Even failure is valuable: a comprehensive map of "what NS has that averaged NS doesn't, and why none of it helps" would be a publishable result.

## Key Context for the Planner

### The SQG Blueprint (most concrete lead)

SQG (surface quasi-geostrophic equation) is the closest structural analog to NS where De Giorgi regularity was proved (Caffarelli-Vasseur 2010). Atlas identified three specific structural gaps:

1. **Scalar vs vector.** SQG truncates a scalar θ. Div-free of the drift R⊥θ is preserved under scalar truncation. NS truncates a vector u — no amplitude truncation preserves div-free (topological obstruction).
2. **Linear vs quadratic coupling.** SQG drift is linear in θ. NS pressure is quadratic in u.
3. **First-order vs second-order cancellation.** SQG gains a power via commutator [(-Δ)^{1/2}, u·]θ. NS loses a power through CZ.

SQG in the Caffarelli-Silvestre extension has β = 4/3 (same as NS) at the Chebyshev level. The improvement is entirely in the drift coupling structure, not in beating Chebyshev. This means the question is NOT "how to get β > 4/3" but "how to reformulate the nonlinear interaction so that a different mechanism (commutator-type) handles it."

### Concrete Leads (untested)

1. **Harmonic structure of far-field pressure.** p_far is harmonic on Q_k with oscillation decaying exponentially (Harnack). A LOCAL H^1 norm of p_far could be much smaller than the global H^1 norm. This was identified by patlas but never tested — and it works OUTSIDE De Giorgi by exploiting harmonicity.

2. **Profile decomposition / concentration-compactness.** Kenig-Merle type approach: assume blowup, extract critical element, derive contradiction. Works for energy-critical NLS. For NS: supercriticality makes critical element extraction harder. Gallagher-Koch-Planchon (2016) have partial results.

3. **Geometric vorticity criteria.** Constantin-Fefferman (1993): regularity holds if vorticity direction is sufficiently regular. Doesn't require De Giorgi at all. Question: can NS dynamics be shown to produce the required vorticity regularity?

4. **Lorentz-space De Giorgi.** The L^{3/2,∞} weak-type estimate is available but unexploited. A De Giorgi framework using weak-type norms directly might sidestep the strong-type CZ ceiling. (This is technically still within De Giorgi, but using a qualitatively different norm structure.)

5. **Local Beltrami structure near vortex tubes.** Exact Beltrami kills CZ loss entirely (β_eff → 1.0). The mechanism requires >98% global alignment. But vortex tube cores are locally near-Beltrami. A conditional result using LOCAL Beltrami deficit (restricted to high-|ω| regions) might work — connecting to Constantin-Fefferman geometric criteria.

### What must be avoided

- Do NOT attempt further modifications to the De Giorgi iteration. β = 4/3 is sharp — this has been proven, not just observed.
- Do NOT approach this as "find a better bound for the pressure term." The barrier is universal — it's not about pressure specifically.
- Do NOT confuse H^1 structure with better L^p integrability (this error was caught by the wide funnel last mission).

### What the Tao filter requires

Any proposed approach must be checked against Tao's 2016 construction. His averaged NS preserves:
- Energy identity (||u(t)||_{L^2} ≤ ||u_0||_{L^2})
- Div-free condition
- All standard Calderón-Zygmund / Littlewood-Paley / Sobolev estimates
- The quadratic nonlinearity structure at the harmonic analysis level

But blowup CAN occur. So the proof must use something that the averaging destroys. The leading candidates for "what averaging destroys":
- The specific algebraic form of u · ∇u (not just "some quadratic term")
- Geometric properties of the vorticity field (stretching alignment, tube structure)
- The pointwise identity ω · ∇u = S · ω (strain-vorticity alignment)
- The specific structure of the pressure Hessian (∂_i∂_j p relates to u_i u_j, not just any quadratic)

## Budget

6-10 explorations total across all steps. This is a landscape + feasibility mission, not a proof construction.

## Connection to Prior Work

This is the natural successor to:
- patlas `vasseur-pressure` (H^1 pressure route → dead end)
- Atlas `vasseur-pressure` (full De Giorgi framework → exhausted)
- Atlas `navier-stokes` (proof architecture comparison: CKN/Lin/Vasseur)

All findings from those missions should be treated as established. Do not re-derive them.
