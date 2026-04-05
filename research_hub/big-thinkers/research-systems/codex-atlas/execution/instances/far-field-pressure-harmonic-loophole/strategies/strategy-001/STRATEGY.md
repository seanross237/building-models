# Strategy 001: Reconstruct the Obstruction, Then Apply the Tao Filter

## Objective

Determine whether the far-field pressure harmonicity lead is a genuine escape from the De Giorgi obstruction, or whether it is Tao-compatible and therefore another closed route.

This strategy is designed as a short falsification-first arc. The intended fast path is:

1. reconstruct the exact far-field obstruction in equations
2. test whether the same harmonic far-field structure survives Tao's averaged Navier-Stokes
3. stop early with a negative result if Tao-compatibility is established

Only if the Tao filter leaves the loophole alive should the strategy spend budget on an explicit model or quantitative gain analysis.

## Methodology

### Phase 0: Obstruction Reconstruction

First reconstruct the exact mathematical object from the predecessor missions, without re-deriving already-closed frameworks from scratch.

Required outputs from this phase:

- the precise far-field pressure pairing under discussion
- the decomposition showing why the problematic coefficient is `O(E_0)` rather than `U_k`-dependent
- the specific recurrence slot where this enters
- the exponent arithmetic connecting that slot back to the `beta = 4/3` barrier
- a compact equation-level statement suitable for direct use in the Tao filter

This is a decomposition audit specialized to the surviving loophole. The strategizer should preload the relevant equations from:

- `execution/instances/vasseur-pressure/strategies/strategy-002/FINAL-REPORT.md`
- `execution/instances/vasseur-pressure/strategies/strategy-001/FINAL-REPORT.md`
- `execution/instances/navier-stokes/strategies/strategy-001/FINAL-REPORT.md`

The point is not to rediscover the whole obstruction atlas. The point is to isolate the one surviving candidate mechanism precisely enough to kill or preserve it.

### Phase 1: Tao Filter

Take the reconstructed obstruction and analyze Tao's averaged Navier-Stokes construction at the level of the pressure equation.

Core questions:

- what replaces `-Delta p = partial_i partial_j (u_i u_j)` after averaging
- whether the far-field part of that pressure remains harmonic on the local cylinder/ball where the De Giorgi step runs
- whether the harmonic-oscillation/Harnack mechanism survives averaging
- whether the "local `H^1` of `p_far` may be much smaller than global" idea survives as a structural distinction, not just a norm rewrite

The strategizer should prefer primary-source reasoning tied to Tao's actual averaged equation, not loose analogy.

Branch rule:

- If Tao-compatible: close the loophole and move directly to synthesis.
- If Tao-incompatible: proceed to Phase 2.
- If genuinely unclear: proceed to Phase 2 with the uncertainty stated sharply.

### Phase 2: Minimal Falsification Model

This phase runs only if the Tao filter does not already close the mission.

Construct the smallest explicit model that still has the claimed favorable structure:

- harmonic far-field pressure
- a local-vs-global distinction strong enough to matter
- an explicit pressure pairing that can be checked for `U_k`-dependence

The model must answer a binary question:

- does harmonicity turn the fixed `O(E_0)` coefficient into something `U_k`-dependent, or not?

Do not allow aspirational models. The model must be explicit enough that the coefficient comparison is concrete.

### Phase 3: Quantitative Gain Check

Only if Phase 2 finds a genuine structural gain:

- quantify the gain in the pressure term
- translate it into the recurrence exponent arithmetic
- compare term-by-term against the original obstruction
- decide whether anything real changed, or whether the gain is only notational

Any claimed gain must be stated as a strict improvement in either:

- coefficient structure, or
- recurrence exponent

If the result is just a repackaging of the same bound, the direction is closed.

### Phase 4: Adversarial Synthesis and Final Report

The final report must make the mission-level judgment unambiguous:

- loophole closed because Tao-compatible
- loophole closed because harmonicity does not create `U_k`-dependence
- loophole survives with a precise quantitative gain and a precise follow-up

## Cross-Phase Rules

1. Use equation-level citations. The validation guide requires exact formulas, recurrence slots, and function spaces.
2. Reuse predecessor results rather than re-running dead directions. `beta = 4/3` sharpness, tool-independence, the `W^{1,3}` wall, and epsilon-regularity universality are already established.
3. Maintain a Direction Status Tracker in `REASONING.md` with `OPEN / PROMISING / CLOSED / EXHAUSTED`.
4. Tag substantial claims in the final report as `[VERIFIED]`, `[COMPUTED]`, `[CHECKED]`, or `[CONJECTURED]`.
5. Explicitly state the strongest counterargument to the mission's conclusion and address it.
6. Do not drift into a new proof architecture. This mission is only about the far-field harmonic loophole.
7. If the Tao filter closes the route cleanly, stop early. A definitive negative result is success.

## Validation Criteria

This strategy succeeds if it produces one of the following:

- a clean Tao-compatibility argument showing the harmonic far-field structure survives averaging, closing the loophole
- a clean negative model result showing harmonicity still leaves the pressure coefficient `O(E_0)` and not `U_k`-dependent
- a real quantitative gain, compared explicitly term-by-term against the original obstruction

This strategy is exhausted if:

- the exact obstruction has been written in equations
- the Tao filter has been answered cleanly
- either the loophole is closed, or the only surviving gain is merely notational

Expected efficient path:

- 1 exploration for obstruction reconstruction
- 1 exploration for Tao compatibility
- 0-2 explorations only if the loophole survives

## Context

### Mission context

This mission begins after the De Giorgi family has already been mapped and largely closed:

- `execution/instances/vasseur-pressure/strategies/strategy-002/FINAL-REPORT.md`: `beta = 4/3` is sharp within the De Giorgi-Vasseur framework, with tool-independent obstruction and a constant divergence-free extremizer.
- `execution/instances/vasseur-pressure/strategies/strategy-001/FINAL-REPORT.md`: the Lamb-vector/Beltrami lead does not generalize, and the barrier reappears across formulations.
- `execution/instances/navier-stokes/strategies/strategy-001/FINAL-REPORT.md`: Tao-style "harmonic analysis alone" obstruction already aligns with the failure of interpolation-driven regularity routes.

### Methodological meta-learning

Carry forward these missionary lessons:

- start proof-improvement missions with a decomposition audit of the exact load-bearing step
- use a Direction Status Tracker so closed routes stay closed
- treat negative results as terminal when they are equation-level and adversarially robust
- verify upstream logic before investing in constructive attacks

### Important non-goals

- do not re-test generic `H^1` pressure routes
- do not re-derive the entire `beta = 4/3` sharpness theorem
- do not spend budget on generic De Giorgi modifications
- do not claim success from a local norm improvement unless it changes the actual recurrence term

## Budget Guidance

Target 2-4 explorations, with early stopping strongly preferred if Phase 1 closes the mission.
