# Step 4 Results — Dynamic Plausibility Screen And Branch-Kill Memo

## Completion Status

Step 4 is complete.

- Kill condition fired: **yes**
- Branch status: **dynamic screen failed on the fixed Step-3 package**
- Honest summary:
  on the inherited Eulerian parabolic package, no candidate cleared the
  `dynamically plausible` bar. The primary hybrid
  `direction coherence + tube persistence` remains the best dynamic idea, but
  only as `informative but dynamically weak`. Every comparator or fragility
  screen is likewise dynamically weak or static-only. Advancing to kernel-level
  `S omega . omega` representation work on this package would be blind momentum
  rather than an earned next step.

## Source Basis

Primary step outputs:

- `missions/beyond-de-giorgi/steps/step-004/explorations/exploration-001/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-004/explorations/exploration-001/REPORT-SUMMARY.md`
- `missions/beyond-de-giorgi/steps/step-004/explorations/exploration-002/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-004/explorations/exploration-002/REPORT-SUMMARY.md`
- `missions/beyond-de-giorgi/steps/step-004/explorations/exploration-003/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-004/explorations/exploration-003/REPORT-SUMMARY.md`

Main underlying local sources:

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
- `library/factual/geometry-route-screening/direction-regularity-is-prior-art-not-a-standalone-novelty-claim.md`
- `library/factual/geometry-route-screening/tube-persistence-remains-live-only-as-a-dynamic-or-hybrid-route.md`
- `library/factual/geometry-route-screening/standalone-beltrami-alignment-collapses-to-a-fragility-screen.md`
- `library/factual/geometry-route-screening/step-3-should-start-with-a-neutral-eulerian-parabolic-localization-package.md`
- `library/factual/geometry-route-screening/geometry-candidates-must-act-on-full-stretching.md`
- `library/meta/obstruction-screening/for-geometry-branches-only-dynamic-coherence-or-persistence-clears-the-tao-screen.md`
- `library/meta/exploration-goal-design/fix-a-provisional-stretching-representation-early-in-geometry-screens.md`
- `library/meta/exploration-goal-design/when-hidden-normalization-is-a-risk-start-with-the-least-adapted-localization-that-keeps-the-scenario-visible.md`
- `missions/navier-stokes/library-inbox/ckn-1982-proof-architecture.md`
- `missions/navier-stokes/library-inbox/vasseur-2007-proof-architecture.md`
- `runtime/results/codex-patlas-standalone-20260331T113910Z-receptionist-79670.md`

## Dynamic-Screen Memo

### Fixed inherited Step-3 package

- [VERIFIED] Primary scenario:
  `filament or tube concentration`
- [VERIFIED] Comparator scenario:
  `sheet or pancake concentration`
- [VERIFIED] Localization:
  Eulerian parabolic package on
  `B_r(x_*) x [t_* - r^2, t_*]`
- [VERIFIED] Threshold:
  `|omega| >= r^{-2}`
- [VERIFIED] Candidate set entering the dynamic screen:
  - primary:
    `direction coherence + tube persistence`
  - secondary comparators:
    `vorticity-direction coherence`,
    `tube coherence / persistence`
  - fragility screens only:
    `local Beltrami / alignment`,
    `Beltrami deficit + concentration`,
    `Beltrami deficit + anisotropy`

### Why dynamic plausibility is the right gate now

- [VERIFIED] The active chain requires the branch to ask what is transported,
  approximately propagated, or rapidly lost before fixing any kernel-level
  representation of `S omega . omega`. Source:
  `missions/beyond-de-giorgi/CHAIN.md`
- [VERIFIED] Step 3 already did the honest static narrowing:
  it fixed the scenario, localization, and bounded candidate list without
  reintroducing tube-adapted coordinates. Source:
  `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`
- [INFERRED] So the only remaining question before representation work is
  persistence credibility:
  does any candidate retain a believable dynamic mechanism once diffusion,
  moving superlevel sets, and Eulerian localization are named explicitly?
- [INFERRED] If not, then the chain should stop here. Otherwise Step 4 would
  merely choose a decomposition for a route that already failed its persistence
  screen.

## Candidate-By-Candidate Transport Table

| Candidate | Best transport identity or propagation heuristic | Main diffusion loss | Main commutator / localization-evolution burden | Depends most on | Tao discriminator dynamic status | First obvious dynamic failure mode | Final rating |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `direction coherence + tube persistence` | [INFERRED] vorticity transport-diffusion-stretching heuristic plus the idea that an intense filamentary region might be advected and stretched while its direction field stays coherent enough for later `xi . S xi` control. Sources: `MISSION.md`, `CHAIN.md`, `direction-coherence-plus-tube-persistence-is-the-primary-step-2-survivor.md` | [INFERRED] order-one diffusion on scale `r` over time `r^2`; thresholded tube boundary can smear/reconnect, and the direction part inherits derivative-heavy diffusion terms | [INFERRED] matching coherent intense components across a moving Eulerian superlevel set without tube refitting; any smooth localization also carries `1/r` and `1/r^2` cutoff costs. Sources: `step-3-should-start-with-a-neutral-eulerian-parabolic-localization-package.md`, `ckn-1982-proof-architecture.md`, `vasseur-2007-proof-architecture.md` | [INFERRED] a hidden matching principle for the evolving intense set and a stronger direction-propagation principle than the fixed package contains | [INFERRED] still live conceptually, but weak in practice: joint persistence of direction coherence on a coherent tube family is Tao-sensitive, yet no estimate-level propagation mechanism is supplied | [INFERRED] route becomes viable only after hidden tube adaptation, threshold/window retuning, or stronger `nabla xi`-type control | `informative but dynamically weak` |
| `vorticity-direction coherence` | [INFERRED] normalized-vorticity direction heuristic: if `xi = omega / |omega|` stays coherent on `E_r(t)`, then `xi . S xi` remains the relevant stretching-facing quantity. Sources: `MISSION.md`, `step-003/RESULTS.md` | [INFERRED] diffusion of `xi` introduces derivative losses and pushes the route toward stronger `nabla xi` control | [INFERRED] measuring the same coherence notion on the moving Eulerian intense set without quietly upgrading to a stronger prior-art direction criterion | [INFERRED] maintaining direction coherence on `E_r(t)` without importing the stronger regularity package already associated with known criteria | [VERIFIED/INFERRED] weak; as a standalone route it mostly collapses into prior-art direction regularity unless a new localized persistence bridge is supplied. Source: `direction-regularity-is-prior-art-not-a-standalone-novelty-claim.md` | [INFERRED] hidden import of `nabla xi`-type control stronger than the Step-3 package | `informative but dynamically weak` |
| `tube coherence / persistence` | [INFERRED] vortex-structure heuristic: intense filamentary components might persist approximately because vorticity is advected and stretched | [INFERRED] tube-boundary erosion, splitting, or merging over the `r^2` window | [INFERRED] matching connected components of the thresholded Eulerian intense set across time without tube-adapted relocalization | [INFERRED] threshold and connectedness rules for the evolving intense set | [VERIFIED/INFERRED] live only if there is genuine time/scale persistence; one-time tube imagery is static. Sources: `tube-persistence-remains-live-only-as-a-dynamic-or-hybrid-route.md`, `step-002/explorations/exploration-002/REPORT.md` | [INFERRED] descriptive slippage into tube language or hidden tube-adapted tracking | `informative but dynamically weak` |
| `local Beltrami / alignment` | [INFERRED] no credible full-stretching transport story; at best a vague hope that local alignment might persist on a core | [INFERRED] local alignment is quickly degraded without stronger derivative control on both `u` and `omega` | [INFERRED] thresholding can isolate a favorable aligned core while leaving exterior strain untouched | [VERIFIED/INFERRED] local alignment on the intense set, but without a bridge from `u x omega`-style depletion to full `S omega . omega`. Sources: `MISSION.md`, `standalone-beltrami-alignment-collapses-to-a-fragility-screen.md` | [VERIFIED] collapsed; static alignment language is Tao-robust and aimed at the wrong quantity | [INFERRED] only local/self-induced depletion improves while the decisive exterior strain remains free | `static-only` |
| `Beltrami deficit + concentration` | [INFERRED] concentrated aligned core might persist long enough to make the exterior field relatively less important | [INFERRED] diffusion weakens both alignment and concentration over the same `r^2` window | [VERIFIED/INFERRED] concentration strength is hostage to the thresholded intense set; threshold choice can manufacture the favorable core. Sources: `step-003/RESULTS.md`, `step-003/explorations/exploration-003/REPORT.md` | [INFERRED] isolating an unusually aligned intense core by the fixed threshold | [INFERRED] weak at best; concentrated aligned cores can survive as descriptive pictures unless they are linked dynamically to a smaller full-stretching term | [INFERRED] threshold tuning manufactures the signal while exterior/nonlocal strain remains scale-critical | `informative but dynamically weak` |
| `Beltrami deficit + anisotropy` | [INFERRED] anisotropic aligned core might persist and later improve a kernel angular factor or exterior remainder | [INFERRED] diffusion relaxes anisotropy and blurs the shape information needed to distinguish a filamentary core | [VERIFIED/INFERRED] anisotropy can be silently imported by geometry fitting, especially via a preferred tube axis. Sources: `step-003/RESULTS.md`, `step-003/explorations/exploration-003/REPORT.md` | [INFERRED] reading anisotropy from the neutral Eulerian package without later tube fitting | [INFERRED] weak; static anisotropy is descriptive unless paired with a real propagation law | [INFERRED] route becomes plausible only after preferred-axis fitting or stronger geometric adaptation than the Step-3 package allows | `informative but dynamically weak` |

## Dynamic Ranking And Kill Memo

### Ranking

- [INFERRED] `direction coherence + tube persistence`:
  `informative but dynamically weak`
- [INFERRED] `vorticity-direction coherence`:
  `informative but dynamically weak`
- [INFERRED] `tube coherence / persistence`:
  `informative but dynamically weak`
- [INFERRED] `local Beltrami / alignment`:
  `static-only`
- [INFERRED] `Beltrami deficit + concentration`:
  `informative but dynamically weak`
- [INFERRED] `Beltrami deficit + anisotropy`:
  `informative but dynamically weak`

### Kill memo

- [INFERRED] No candidate is `dynamically plausible` on the audited package.
- [INFERRED] The primary hybrid remains the best route descriptively and
  conceptually, but not strongly enough to justify Step 4 representation work.
- [INFERRED] The step's early kill condition is met in two convergent ways:
  - every surviving candidate is dynamically weak or static-only, so further
    work would be blind momentum;
  - the only visible rescues for the primary hybrid are the forbidden ones:
    tube-adapted relocalization, tuned threshold/window choices, or stronger
    derivative control than the bounded Step-3 package contains.
- [INFERRED] Therefore the current geometry branch should be invalidated or
  replanned rather than allowed to drift into kernel-level analysis anyway.

## Step-4 Readiness Recommendation

- [INFERRED] No route survives honestly enough to justify fixing a primary
  kernel-level representation of `S omega . omega` on the present package.
- [INFERRED] The current chain should stop here and hand the controller a
  calibrated obstruction result:
  the geometry branch fails at the dynamic screen because neutral Eulerian
  localization plus a diffusion-scale time window makes every candidate either
  too weak dynamically, too dependent on hidden normalization, or too close to
  static prior-art geometry.
- [INFERRED] If later work wants to revisit geometry, it should do so only by
  openly changing the package and admitting that the current Step-3 audit did
  not earn continuation.
