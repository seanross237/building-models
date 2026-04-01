# Exploration 001 Summary

- goal:
  test the primary Step-3 survivor `direction coherence + tube persistence`
  against the fixed Step-3 Eulerian package on
  `B_r(x_*) x [t_* - r^2, t_*]` with threshold `|omega| >= r^{-2}`, and decide
  whether it has a credible dynamic story rather than only a static geometric
  picture.
- what was checked:
  - `missions/beyond-de-giorgi/steps/step-004/GOAL.md`
  - `missions/beyond-de-giorgi/steps/step-004/REASONING.md`
  - `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`
  - `missions/beyond-de-giorgi/steps/step-003/HISTORY-OF-REPORT-SUMMARIES.md`
  - `missions/beyond-de-giorgi/steps/step-002/RESULTS.md`
  - `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-001/REPORT.md`
  - `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-002/REPORT.md`
  - `missions/beyond-de-giorgi/CHAIN.md`
  - `missions/beyond-de-giorgi/MISSION.md`
  - `library/factual/geometry-route-screening/direction-coherence-plus-tube-persistence-is-the-primary-step-2-survivor.md`
  - `library/factual/geometry-route-screening/tube-persistence-remains-live-only-as-a-dynamic-or-hybrid-route.md`
  - `library/factual/geometry-route-screening/filament-or-tube-concentration-is-the-primary-step-3-scenario-for-the-live-hybrid.md`
  - `library/factual/geometry-route-screening/step-3-should-start-with-a-neutral-eulerian-parabolic-localization-package.md`
  - `library/factual/geometry-route-screening/geometry-candidates-must-act-on-full-stretching.md`
  - `library/factual/geometry-route-screening/direction-regularity-is-prior-art-not-a-standalone-novelty-claim.md`
  - `library/meta/obstruction-screening/for-geometry-branches-only-dynamic-coherence-or-persistence-clears-the-tao-screen.md`
  - `library/meta/exploration-goal-design/fix-a-provisional-stretching-representation-early-in-geometry-screens.md`
  - `library/meta/exploration-goal-design/when-hidden-normalization-is-a-risk-start-with-the-least-adapted-localization-that-keeps-the-scenario-visible.md`
  - `runtime/results/codex-patlas-standalone-20260331T113910Z-receptionist-79670.md`
- outcome:
  `succeeded`
- one key takeaway:
  the primary hybrid is still the only route with a genuinely dynamic Tao
  discriminator, but under the inherited Eulerian thresholded package its
  transport story is only heuristic and breaks first on diffusion-driven motion
  of the intense set plus implicit `nabla xi`-type demands.
- best transport / propagation story:
  - [VERIFIED] repo-level story:
    persistence of direction coherence along a coherent intense tube family is
    the only remaining dynamic ingredient that could reduce an
    exterior/inter-scale stretching term or a localization-evolution cost.
  - [INFERRED] best available identity:
    the standard vorticity transport-diffusion equation together with the
    standard magnitude identity
    `(partial_t + u . nabla)|omega| = (xi . S xi)|omega| + Delta|omega| - |omega||nabla xi|^2`.
  - [INFERRED] limitation:
    the local repository gives no theorem-level propagation law for a coherent
    tube family inside the fixed Eulerian superlevel-set package.
- main diffusion loss:
  - [INFERRED] on a time window of length `r^2`, diffusion acts at the same
    spatial scale `r` used to define the package, so tube cross-sections and
    thresholded components can change by order one.
  - [INFERRED] the coherence-specific loss is the derivative-sensitive term
    `-|omega||nabla xi|^2`, which points directly beyond the inherited Step-3
    package.
- main localization-evolution or commutator burden:
  - [INFERRED] the thresholded Eulerian intense set
    `E_r(t) = {x in B_r(x_*) : |omega| >= r^{-2}}`
    has no transport law in the local record.
  - [INFERRED] the first burden is therefore matching coherent components across
    time without re-centering, tube-fitting, or retuning the threshold/window;
    smooth cutoffs would also introduce standard `1/r` and `1/r^2` localization
    errors.
- Tao discriminator status:
  - [VERIFIED/INFERRED] still live, but only narrowly:
    what averaging would destroy is not static tube imagery but joint
    persistence of direction coherence and coherent intense-component structure
    across one `r^2` window.
  - [INFERRED] under the fixed package it remains dynamically weak because the
    repo cannot supply a concrete propagation mechanism that survives diffusion
    and Eulerian relocalization burdens.
- first obvious dynamic failure mode:
  - [INFERRED] the tube-like Eulerian intense component seen at one time cannot
    be matched cleanly across the whole `r^2` window because diffusion and
    advection move the superlevel-set boundary, causing threshold crossings,
    splits, or mergers before coherence is propagated.
  - [INFERRED] the first dishonest rescue after that is hidden tube adaptation
    or stronger derivative control.
- final rating:
  `informative but dynamically weak`
- leads worth pursuing:
  - make the later Step-4 representation explicitly isolate whether the hybrid
    would need to reduce an exterior/inter-scale term or only a
    localization-evolution term.
  - test whether any smoothed version of the Eulerian intense-set indicator can
    be evolved without immediately importing tube-adapted tracking.
- unexpected findings:
  - the local record is stronger on the earliest honest kill condition than on a
    positive transport mechanism.
  - the first true failure is not "tube geometry is false" but "the honest
    Eulerian package gives no canonical way to propagate the relevant tube
    component across time."
- computations worth doing later if they are outside scope:
  - write one explicit localized evolution identity with a smooth cutoff for a
    candidate coherence quantity on `Q_r(x_*, t_*)` to see whether the dominant
    remainder is genuinely a cutoff term or the moving-threshold/component
    matching burden.
