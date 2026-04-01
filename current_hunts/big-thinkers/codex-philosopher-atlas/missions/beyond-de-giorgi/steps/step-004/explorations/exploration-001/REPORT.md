# Exploration 001 Report

## Goal

Dynamic screen for the primary Step-3 survivor:

- hybrid: `direction coherence + tube persistence`
- inherited Step-3 package: neutral Eulerian parabolic localization on
  `B_r(x_*) x [t_* - r^2, t_*]`
- threshold: `|\omega| >= r^{-2}`
- primary scenario: filament or tube concentration
- comparator retained only for context: sheet or pancake concentration

Required deliverable: decide whether the primary hybrid has a credible dynamic
story under the fixed Step-3 package, rather than only a static geometric
picture.

## Method

- Read the required mission, step, and library source anchors.
- Extract explicit statements about the inherited Step-3 package and the live
  status of the hybrid.
- Identify the best local transport identity or propagation heuristic.
- Track the main diffusion loss and the main localization-evolution burden over
  one `r^2`-scale window.
- Classify the route as `dynamically plausible`, `informative but dynamically weak`,
  or `static-only`.

## Running Notes

### Initial setup

- Created report skeleton before detailed source review.
- Operational note:
  the launched explorer produced the scaffold above but did not complete the
  analysis in time. The strategizer completed the source-based memo directly
  from the anchored local materials so the step could continue.

## Findings

### 1. Best available transport or propagation story

- [VERIFIED] The local repository already bounded the hybrid's only live
  content to a dynamic one: direction coherence keeps the route pointed at
  stretching, while tube persistence is the part most plausibly destroyed by
  Tao-style averaging. Sources:
  - `library/factual/geometry-route-screening/direction-coherence-plus-tube-persistence-is-the-primary-step-2-survivor.md`
  - `library/factual/geometry-route-screening/tube-persistence-remains-live-only-as-a-dynamic-or-hybrid-route.md`
  - `library/meta/obstruction-screening/for-geometry-branches-only-dynamic-coherence-or-persistence-clears-the-tao-screen.md`
- [VERIFIED] Step 3 fixed the scenario and localization precisely to test
  whether any such persistence can survive on a neutral Eulerian package rather
  than on tube-adapted coordinates. Sources:
  - `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`
  - `library/factual/geometry-route-screening/step-3-should-start-with-a-neutral-eulerian-parabolic-localization-package.md`
- [INFERRED] The best available dynamic story is therefore only heuristic:
  start from the Navier-Stokes vorticity transport-diffusion-stretching
  equation and the pointwise stretching identity `omega . nabla u = S omega`,
  then imagine a strong filamentary intense region that is advected and
  stretched over one parabolic time `r^2` while its vorticity direction stays
  coherent enough that the later stretching factor `xi . S xi` is still
  geometrically meaningful. Sources:
  - `missions/beyond-de-giorgi/MISSION.md`
  - `missions/beyond-de-giorgi/CHAIN.md`
  - `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`
- [INFERRED] A slightly sharper standard identity is available even though it
  is not written in the local record: on `omega != 0`,
  `(partial_t + u . nabla)|omega| = (xi . S xi)|omega| + Delta|omega| - |omega||nabla xi|^2`.
  This is the best transport-facing formula for the hybrid because it shows, in
  one place, both the hoped-for coherent stretching factor and the first
  derivative-sensitive diffusive loss.
- [INFERRED] What is missing is decisive:
  no local file gives an exact transport law or theorem-level approximate
  propagation statement for "coherent tube family inside the Eulerian intense
  set" across the full window `[t_* - r^2, t_*]`. The route survives only as a
  plausible story, not a supported propagation mechanism. Sources:
  - `library/factual/geometry-route-screening/tube-persistence-remains-live-only-as-a-dynamic-or-hybrid-route.md`
  - `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-001/REPORT.md`
  - `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-002/REPORT.md`

### 2. Main diffusion loss

- [VERIFIED] The fixed time window is exactly one diffusion-scale interval:
  `[t_* - r^2, t_*]`. Step 3 chose that window because it is the least adapted
  honest test, not because it makes persistence easy. Sources:
  - `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`
  - `missions/beyond-de-giorgi/steps/step-003/explorations/exploration-002/REPORT.md`
- [INFERRED] On that window, diffusion is not a small perturbation on length
  scale `r`; it is order-one at exactly the scale used to define the intense
  set. So even if a filamentary core is materially advected, the thresholded
  tube boundary can thicken, erode, or reconnect enough to spoil any naive
  "same tube family persists" claim.
- [INFERRED] The direction part is even more fragile. Any direction-field
  equation for `xi = omega / |omega|` inherits diffusion terms with derivatives
  of `omega` and division by `|omega|`; the threshold `|omega| >= r^{-2}`
  prevents vanishing-amplitude singularity inside the intense set, but it does
  not supply the stronger derivative control needed to keep `xi` coherent
  dynamically. This is exactly the type of stronger `nabla xi`-style package
  that the local record treats as exceeding the inherited Step-3 bounds rather
  than clarifying them. Sources:
  - `library/factual/geometry-route-screening/direction-regularity-is-prior-art-not-a-standalone-novelty-claim.md`
  - `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`
- [INFERRED] The first honest diffusion lesson is therefore:
  the hybrid's dynamic burden is not just preserving large `|omega|`; it is
  preserving coherent direction on a superlevel-set tube family while
  diffusion acts at full strength on the chosen parabolic window.

### 3. Main localization-evolution and commutator burden

- [VERIFIED] Step 3 deliberately chose a neutral Eulerian superlevel-set
  protocol so tube persistence would have to emerge from the data, not from a
  transported coordinate system or tube-fitted axis. Sources:
  - `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`
  - `library/factual/geometry-route-screening/step-3-should-start-with-a-neutral-eulerian-parabolic-localization-package.md`
  - `library/meta/exploration-goal-design/when-hidden-normalization-is-a-risk-start-with-the-least-adapted-localization-that-keeps-the-scenario-visible.md`
- [INFERRED] That creates the central dynamic burden:
  one must match coherent intense components across time inside a moving
  thresholded set `E_r(t)` without re-centering, re-fitting a tube axis, or
  redefining the threshold. Component splitting/merging is therefore a genuine
  burden, not a bookkeeping detail.
- [INFERRED] Any smooth Eulerian localization of the parabolic package also
  carries the usual cutoff costs:
  spatial derivatives scale like `1/r` and time/Laplacian derivatives like
  `1/r^2`, so localization-evolution errors arrive at the same scale as the
  transport-diffusion balance. Sources:
  - `missions/navier-stokes/library-inbox/ckn-1982-proof-architecture.md`
  - `missions/navier-stokes/library-inbox/vasseur-2007-proof-architecture.md`
- [VERIFIED] The local geometry rule is that a candidate only survives if it
  can make some full-stretching term smaller, schematically a local piece, an
  exterior/nonlocal piece, or a localization/inter-scale interaction term.
  Sources:
  - `library/factual/geometry-route-screening/geometry-candidates-must-act-on-full-stretching.md`
  - `library/meta/exploration-goal-design/fix-a-provisional-stretching-representation-early-in-geometry-screens.md`
- [INFERRED] For the hybrid, the only plausible target at Step 4 level is the
  exterior/inter-scale stretching contribution or the localization-evolution
  cost. But the present local record supplies no estimate showing that the
  Eulerian matching problem gets easier rather than harder under the hybrid.

### 4. What the hybrid depends on most

- [INFERRED] The route depends most on a hidden matching principle for the
  evolving intense set:
  that the thresholded Eulerian components really do identify a coherent tube
  family across the full window without later axis-fitting or threshold tuning.
- [INFERRED] It also depends on a direction-propagation principle stronger than
  the present Step-3 package contains. The hybrid remains live only if one can
  talk about `xi`-coherence dynamically without importing the stronger
  derivative-control package that would already place the route close to known
  direction-regularity criteria.

### 5. Tao discriminator status

- [VERIFIED] The Tao discriminator stays live only in a narrow dynamic sense:
  joint persistence of direction coherence along an intense coherent tube family
  across times/scales is the one feature the local record repeatedly marks as
  plausibly destroyed by averaging. Sources:
  - `library/factual/geometry-route-screening/direction-coherence-plus-tube-persistence-is-the-primary-step-2-survivor.md`
  - `library/meta/obstruction-screening/for-geometry-branches-only-dynamic-coherence-or-persistence-clears-the-tao-screen.md`
- [INFERRED] But once the story is forced onto the fixed Eulerian package, the
  discriminator becomes dynamically weak rather than robust:
  the repository can explain why averaged models should scramble this kind of
  coherence, but it cannot name a concrete propagation mechanism that survives
  diffusion and Eulerian relocalization costs.

### 6. First obvious dynamic failure mode

- [INFERRED] The first obvious failure mode inside the fixed package is that the
  thresholded Eulerian component that looked tube-like near one time cannot be
  matched cleanly across the full `r^2` window: diffusion and advection move the
  superlevel-set boundary, so components can split, merge, or fall below
  `r^{-2}` before any coherence statement is propagated.
- [INFERRED] The first rescue move after that failure would be hidden tube
  adaptation:
  re-fit a tube axis, track a preferred component, or retune the
  threshold/window after the geometry is seen.
- [INFERRED] The second rescue move is hidden derivative control:
  turning the direction part into a real dynamic estimate appears to demand a
  stronger `nabla xi`-type package than the bounded Step-3 data contains.
- [INFERRED] Either move triggers the step's honest kill condition, because the
  branch would then survive only by exceeding the fixed audited package.

## Dead Ends / Failed Attempts

- [VERIFIED] No theorem-level local source was found that propagates a coherent
  tube family inside a fixed Eulerian superlevel-set package across one
  diffusion-scale time interval.
- [VERIFIED] No local source was found that upgrades the direction part into a
  dynamic estimate without effectively importing a stronger direction-regularity
  package.

## Provisional Verdict

- [INFERRED] Final rating:
  `informative but dynamically weak`
- [INFERRED] Reason:
  the hybrid is still the strongest candidate in the branch because it is the
  only one whose Tao discriminator remains genuinely dynamic, but under the
  fixed Eulerian package the best transport story is still only heuristic while
  the diffusion and localization-evolution burdens are already order-one.
