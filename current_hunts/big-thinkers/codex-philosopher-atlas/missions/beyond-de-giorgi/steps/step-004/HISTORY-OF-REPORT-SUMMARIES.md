# History of Report Summaries

Exploration summaries will be appended here as they land.

---

## Exploration 001

# Exploration 001 Summary

- Goal:
  test `direction coherence + tube persistence` against the fixed Step-3
  Eulerian package and decide whether it has a credible dynamic story rather
  than only a static geometric one.
- What was checked:
  - `missions/beyond-de-giorgi/steps/step-004/GOAL.md`
  - `missions/beyond-de-giorgi/steps/step-004/REASONING.md`
  - `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`
  - `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-001/REPORT.md`
  - `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-002/REPORT.md`
  - `missions/beyond-de-giorgi/MISSION.md`
  - `library/factual/geometry-route-screening/direction-coherence-plus-tube-persistence-is-the-primary-step-2-survivor.md`
  - `library/factual/geometry-route-screening/tube-persistence-remains-live-only-as-a-dynamic-or-hybrid-route.md`
  - `library/factual/geometry-route-screening/step-3-should-start-with-a-neutral-eulerian-parabolic-localization-package.md`
  - `library/factual/geometry-route-screening/geometry-candidates-must-act-on-full-stretching.md`
  - `library/meta/obstruction-screening/for-geometry-branches-only-dynamic-coherence-or-persistence-clears-the-tao-screen.md`
  - `missions/navier-stokes/library-inbox/ckn-1982-proof-architecture.md`
  - `missions/navier-stokes/library-inbox/vasseur-2007-proof-architecture.md`
- Outcome:
  `succeeded`
- One key takeaway:
  the primary hybrid remains the branch's best dynamic idea, but only as a weak
  heuristic. On the fixed Eulerian parabolic package there is no concrete
  propagation mechanism for a coherent tube family with coherent direction over
  one diffusion-scale interval; diffusion and localization-evolution costs are
  already order-one.
- Best transport / propagation story:
  an [INFERRED] vorticity transport-diffusion-stretching heuristic in which an
  intense filamentary region is advected and stretched while its direction
  field stays coherent enough for the later stretching factor `xi . S xi` to
  remain meaningful.
- Main diffusion loss:
  [INFERRED] the full `r^2`-scale window is exactly diffusion scale on length
  `r`, so the thresholded tube boundary can smear or reconnect, while the
  direction part inherits derivative-heavy diffusion terms.
- Main localization-evolution or commutator burden:
  [INFERRED] matching coherent intense components across the moving Eulerian
  superlevel sets without re-fitting a tube axis or tuning the threshold; any
  smooth localization also carries standard `1/r` and `1/r^2` cutoff costs.
- Tao discriminator status:
  [INFERRED] still live, but only weakly: joint persistence of direction
  coherence on a coherent intense tube family is the right Tao-sensitive idea,
  yet the local record does not turn it into an estimate-level propagation
  mechanism.
- First obvious dynamic failure mode:
  the route becomes viable only after hidden tube adaptation or stronger
  `nabla xi`-type control than the fixed Step-3 package contains.
- Final rating:
  `informative but dynamically weak`

---

## Exploration 002

# Exploration 002 Summary

- Goal:
  audit `vorticity-direction coherence` and `tube coherence / persistence`
  under the same fixed Step-3 Eulerian package and determine whether either
  comparator is dynamically stronger, weaker, or only clarifying.
- What was checked:
  - `missions/beyond-de-giorgi/steps/step-004/GOAL.md`
  - `missions/beyond-de-giorgi/steps/step-004/REASONING.md`
  - `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`
  - `missions/beyond-de-giorgi/steps/step-002/RESULTS.md`
  - `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-001/REPORT.md`
  - `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-002/REPORT.md`
  - `missions/beyond-de-giorgi/MISSION.md`
  - `library/factual/geometry-route-screening/direction-regularity-is-prior-art-not-a-standalone-novelty-claim.md`
  - `library/factual/geometry-route-screening/tube-persistence-remains-live-only-as-a-dynamic-or-hybrid-route.md`
  - `library/factual/geometry-route-screening/step-3-should-start-with-a-neutral-eulerian-parabolic-localization-package.md`
  - `library/factual/geometry-route-screening/geometry-candidates-must-act-on-full-stretching.md`
  - `library/meta/obstruction-screening/for-geometry-branches-only-dynamic-coherence-or-persistence-clears-the-tao-screen.md`
- Outcome:
  `succeeded`
- One key takeaway:
  neither comparator is dynamically stronger than the primary hybrid. Direction
  coherence is the cleaner stretching-facing object but collapses toward known
  criteria once stronger derivative control appears; tube persistence carries
  the sharper Tao-sensitive intuition but lacks a concrete transport law on the
  fixed Eulerian package.
- Best transport / propagation story for `vorticity-direction coherence`:
  [INFERRED] a normalized-vorticity-direction heuristic in which coherence of
  `xi = omega / |omega|` keeps `xi . S xi` meaningful on the intense set.
- Main diffusion loss for `vorticity-direction coherence`:
  [INFERRED] diffusion of the normalized field introduces derivative-heavy
  terms and pushes the route toward stronger `nabla xi` control.
- Main localization-evolution or commutator burden for `vorticity-direction coherence`:
  [INFERRED] measuring the same coherence notion on a moving Eulerian
  superlevel set without quietly upgrading to a stronger regularity criterion.
- Tao discriminator status for `vorticity-direction coherence`:
  [INFERRED] weak; as a standalone route it mostly collapses into prior-art
  direction-regularity unless a new persistence bridge is supplied.
- First obvious failure mode for `vorticity-direction coherence`:
  importing stronger `nabla xi`-type control than the fixed Step-3 package
  contains.
- Final rating for `vorticity-direction coherence`:
  `informative but dynamically weak`
- Best transport / propagation story for `tube coherence / persistence`:
  [INFERRED] a vortex-structure heuristic in which intense filamentary
  components persist approximately because vorticity is advected and stretched.
- Main diffusion loss for `tube coherence / persistence`:
  [INFERRED] order-one tube-boundary erosion, splitting, or merging over the
  `r^2` diffusion-scale window.
- Main localization-evolution or commutator burden for `tube coherence / persistence`:
  [INFERRED] matching connected components of the moving Eulerian superlevel
  sets without re-centering or tube-adapted relocalization.
- Tao discriminator status for `tube coherence / persistence`:
  [INFERRED] live only if there is genuine time/scale persistence; one-time
  tube imagery is static-only.
- First obvious failure mode for `tube coherence / persistence`:
  descriptive slippage into tube language or hidden tube-adapted localization.
- Final rating for `tube coherence / persistence`:
  `informative but dynamically weak`

---

## Exploration 003

# Exploration 003 Summary

- Goal:
  confirm that the Beltrami-family quantities remain fragility screens after
  dynamic considerations are added, and state the earliest honest branch-kill
  condition if the primary hybrid fails.
- What was checked:
  - `missions/beyond-de-giorgi/steps/step-004/GOAL.md`
  - `missions/beyond-de-giorgi/steps/step-004/REASONING.md`
  - `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`
  - `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-001/REPORT.md`
  - `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-002/REPORT.md`
  - `missions/beyond-de-giorgi/MISSION.md`
  - `library/factual/geometry-route-screening/standalone-beltrami-alignment-collapses-to-a-fragility-screen.md`
  - `library/factual/geometry-route-screening/geometry-candidates-must-act-on-full-stretching.md`
  - `library/meta/obstruction-screening/for-geometry-branches-only-dynamic-coherence-or-persistence-clears-the-tao-screen.md`
  - `missions/beyond-de-giorgi/steps/step-004/explorations/exploration-001/REPORT.md`
  - `missions/beyond-de-giorgi/steps/step-004/explorations/exploration-002/REPORT.md`
- Outcome:
  `succeeded`
- One key takeaway:
  the fragility screens stay fragility screens dynamically. No Beltrami-family
  route becomes plausible on the fixed Eulerian package, and once the primary
  hybrid is only `informative but dynamically weak`, the branch has already hit
  the honest stop condition for this step.
- Final rating for `local Beltrami / alignment`:
  `static-only`
- Final rating for `Beltrami deficit + concentration`:
  `informative but dynamically weak`
- Final rating for `Beltrami deficit + anisotropy`:
  `informative but dynamically weak`
- Earliest honest branch-kill condition:
  every surviving candidate on the audited Step-3 package is dynamically weak
  or static-only, so continuing to kernel-level representation work would be
  blind momentum; the only apparent rescues require hidden tube adaptation,
  threshold/window tuning, or stronger derivative control than the fixed
  package contains.
- Final continuation or invalidation recommendation:
  invalidate or replan the branch now rather than advancing directly to Step 4.
