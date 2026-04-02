# Step 3 Results — Scenario Class, Localization, And Bounded Observable Table

## Completion Status

Step 3 is complete.

- Kill condition fired: **no**
- Branch status: **survives only in a narrowed Step-3 package**
- Honest summary:
  after fixing scenario and localization, the branch still has one honest
  primary candidate, `direction coherence + tube persistence`, but only on a
  tightly bounded package:
  - primary scenario: `filament or tube concentration`
  - comparator scenario: `sheet or pancake concentration`
  - localization: Eulerian parabolic package on a dyadic ball with threshold
    `|omega| >= r^{-2}` over `[t_* - r^2, t_*]`

## Source Basis

Primary step outputs:

- `missions/beyond-de-giorgi/steps/step-003/explorations/exploration-001/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-003/explorations/exploration-001/REPORT-SUMMARY.md`
- `missions/beyond-de-giorgi/steps/step-003/explorations/exploration-002/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-003/explorations/exploration-002/REPORT-SUMMARY.md`
- `missions/beyond-de-giorgi/steps/step-003/explorations/exploration-003/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-003/explorations/exploration-003/REPORT-SUMMARY.md`

Main underlying local sources:

- `missions/beyond-de-giorgi/steps/step-003/GOAL.md`
- `missions/beyond-de-giorgi/CHAIN.md`
- `missions/beyond-de-giorgi/planning-runs/run-002/refined/chain-02.md`
- `missions/beyond-de-giorgi/planning-runs/run-002/attacks/chain-02.md`
- `missions/beyond-de-giorgi/planning-runs/run-002/judgments/chain-02.md`
- `missions/beyond-de-giorgi/steps/step-002/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-001/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-002/REPORT.md`
- `library/factual/geometry-route-screening/direction-coherence-plus-tube-persistence-is-the-primary-step-2-survivor.md`
- `library/factual/geometry-route-screening/tube-persistence-remains-live-only-as-a-dynamic-or-hybrid-route.md`
- `library/factual/geometry-route-screening/direction-regularity-is-prior-art-not-a-standalone-novelty-claim.md`
- `library/factual/geometry-route-screening/standalone-beltrami-alignment-collapses-to-a-fragility-screen.md`
- `library/factual/geometry-route-screening/geometry-candidates-must-act-on-full-stretching.md`
- `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
- `library/meta/obstruction-screening/for-geometry-branches-only-dynamic-coherence-or-persistence-clears-the-tao-screen.md`
- `library/meta/exploration-goal-design/fix-a-provisional-stretching-representation-early-in-geometry-screens.md`
- `library/meta/exploration-goal-design/state-nonlocal-moment-dependence-in-the-goal.md`

## Scenario-Class Decision Memo

- [VERIFIED] The active chain and its judgment record require a concrete
  singular-scenario class before any persistence claim can be tested.
- [VERIFIED] The only scenario classes explicitly supported in the local record
  at this stage are `filament concentration` and `sheet/pancake
  concentration`.
- [VERIFIED] Step 2 narrowed the live branch to the hybrid
  `direction coherence + tube persistence`.

### Decision

- [INFERRED] Primary scenario class:
  `filament or tube concentration`
- [INFERRED] Secondary comparator:
  `sheet or pancake concentration`

### Why this is the right bounded choice

- [INFERRED] `filament or tube concentration` is the fairest primary test bed
  because the only surviving Step-2 question is already tube-family specific:
  whether direction coherence can persist along a coherent tube family strongly
  enough to matter for full stretching, including the exterior/inter-scale
  part.
- [INFERRED] `sheet or pancake concentration` is worth retaining only as a
  comparator because it prevents the branch from equating "geometric scenario"
  with "tube-looking scenario," but the local record does not tie the surviving
  hybrid to a comparably concrete sheet-based persistence mechanism.

### Why rejected alternatives are inferior

- [INFERRED] More specific variants such as `axial tube collapse` or
  `filament reconnection-type concentration` are too weakly supported in the
  local corpus to count as official Step-3 scenario classes.

### Failure mode for each chosen scenario

- [INFERRED] `filament or tube concentration` failure mode:
  the hybrid may improve only tube-core or self-induced geometry while the
  decisive exterior/inter-scale stretching contribution or
  localization-evolution cost stays large, leaving only descriptive tube
  language.
- [INFERRED] `sheet or pancake concentration` failure mode:
  the hybrid may cease to function as tube persistence at all and collapse into
  generic direction regularity or bare concentration, exposing scenario misfit
  rather than new leverage.

## Localization Protocol Specification

### Fixed protocol

- [PROPOSED] Intensity threshold:
  `|omega(x,t)| >= r^{-2}`
- [PROPOSED] Spatial scale:
  one dyadic ball `B_r(x_*)`
- [PROPOSED] Time window:
  `[t_* - r^2, t_*]`
- [INFERRED] Localization type:
  `Eulerian`

Equivalent package:

- [PROPOSED] Work on the Eulerian intense set
  `E_r(t) = {x in B_r(x_*) : |omega(x,t)| >= r^{-2}}`
  inside the parabolic cylinder
  `Q_r(x_*, t_*) = B_r(x_*) x [t_* - r^2, t_*]`.

### Why this protocol fits the chosen scenario

- [INFERRED] It is the least adapted package that still keeps the
  filament/tube scenario visible.
- [INFERRED] It does not preselect a tube axis or follow a pre-fitted tube
  family, so any tube coherence or persistence has to emerge from the data
  rather than from the coordinates.
- [INFERRED] It is also portable to the `sheet or pancake concentration`
  comparator, which is important for overfitting control.
- [INFERRED] Its intended leverage point is not merely to isolate a core.
  It is meant to expose whether any candidate can later shrink:
  - the exterior/inter-scale stretching contribution
  - or the localization-evolution cost
  in a fixed full-stretching representation.

### Why this does not quietly bake in the hoped-for conclusion

- [INFERRED] `Eulerian` was chosen over `tube-adapted` precisely to avoid
  installing the hoped-for tube geometry into the localization.
- [INFERRED] The threshold uses the simplest scale-matched vorticity level
  rather than a local-maximum or quantile normalization, which would be more
  data-adaptive and easier to tune.

### Stability check

- [INFERRED] Threshold perturbation:
  replacing `|omega| >= r^{-2}` by `|omega| >= (1/2)r^{-2}` or
  `|omega| >= 2r^{-2}` should only thicken or thin the intense set. If the
  primary hybrid survives only at one tuned threshold, it is localization
  overfit.
- [INFERRED] Time-window perturbation:
  replacing `[t_* - r^2, t_*]` by `[t_* - (1/2)r^2, t_*]` or
  `[t_* - 2r^2, t_*]` should change persistence burden gradually. If the hybrid
  survives only on an extremely short window, it is likely a static snapshot
  rather than a persistence mechanism.
- [INFERRED] Residual risk:
  the choice of center `(x_*, t_*)` and dyadic scale `r` can still be tuned
  after seeing favorable filament geometry. Later steps must keep that choice
  rule fixed.

## Bounded Observable Table

| Candidate | Role | Scaling / normalization status | Localization data dependence | Scenario addressed | Intended leverage point on future full-stretching target | Tao discriminator | First obvious instability / hidden-normalization risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `direction coherence + tube persistence` | primary | [INFERRED] mixed but bounded: direction coherence is dimensionless; persistence is only scale-credible when tied to the shared dyadic Eulerian package | [VERIFIED/INFERRED] needs `E_r(t)` on `B_r(x_*) x [t_*-r^2,t_*]` and a fixed rule for matching coherent intense components across the window | [INFERRED] primary `filament or tube concentration`; only a comparator misfit test on `sheet or pancake concentration` | [INFERRED] best chance to shrink the exterior/inter-scale stretching contribution or localization-evolution cost | [VERIFIED/INFERRED] joint persistence of direction coherence along a coherent tube family across scales/times is the main ingredient plausibly destroyed by Tao-style averaging | [INFERRED] collapses if coherence appears only after tube-adapted relocalization or tuned threshold/window choices |
| `vorticity-direction coherence` | secondary comparator | [VERIFIED/INFERRED] dimensionless, but operational force is limited by how coherence is measured on `E_r(t)` | [INFERRED] direction field on the same Eulerian intense set and parabolic window | [INFERRED] comparator in both primary and secondary scenarios | [INFERRED] could at best make `xi . S xi` or a localized exterior contribution smaller if coherence persists under the fixed package | [VERIFIED] prior-art direction-regularity statements are Tao-robust benchmark material; only a new localized persistence effect would clear the screen | [VERIFIED/INFERRED] easily collapses back into known criteria or smuggles in stronger `nabla xi` control |
| `tube coherence / persistence` | secondary comparator | [INFERRED] not clearly scale-invariant by itself; inherits any scale credibility only from the fixed threshold/scale package | [INFERRED] connectedness/coherence of intense components inside the Eulerian thresholded set across the parabolic window | [INFERRED] mainly `filament or tube concentration`; only a misfit detector on `sheet or pancake concentration` | [INFERRED] could matter only by suppressing exterior/inter-scale stretching or localization-evolution cost | [VERIFIED/INFERRED] one-time tube-shaped concentration is Tao-robust; only persistence across scales/time is plausibly destroyed by averaging | [VERIFIED/INFERRED] very prone to descriptive slippage if it never names a smaller full-stretching term |
| `local Beltrami / alignment` | fragility screen only | [VERIFIED] dimensionless alignment-type quantity, but not enough for operational control | [INFERRED] local `u` and `omega` data on the same intense set | [INFERRED] diagnostic in either scenario | [VERIFIED/INFERRED] at most tests local/self-induced depletion, not the full exterior/nonlocal stretching burden | [VERIFIED] static alignment language is Tao-robust and already benchmark-collapsed unless it reaches full stretching | [VERIFIED] controls the wrong object too easily, drifting toward `u x omega` or local depletion rather than full `S omega . omega` |
| `Beltrami deficit + concentration` | fragility screen only | [INFERRED] normalization is fragile because concentration strength depends explicitly on the thresholded intense set | [INFERRED] alignment plus the Eulerian thresholded concentration profile in `E_r(t)` | [INFERRED] mostly `filament or tube concentration`, but diagnostic only | [INFERRED] hoped-for gain is a more favorable core-versus-exterior split, but no full-stretching bridge is present on the local record | [INFERRED] only a dynamic coupling between concentrated aligned cores and a smaller full-stretching term would beat Tao-style robustness | [INFERRED] easiest place for hidden normalization, since the threshold can isolate unusually aligned cores by construction |
| `Beltrami deficit + anisotropy` | fragility screen only | [INFERRED] normalization depends on how anisotropy is extracted from the thresholded set | [INFERRED] alignment plus shape data of `E_r(t)` inside the Eulerian ball | [INFERRED] mainly `filament or tube concentration` | [INFERRED] hoped-for gain is a smaller kernel angular factor or exterior remainder in a later stretching representation | [INFERRED] only a genuinely NS-specific persistence of anisotropic coherent cores would clear the Tao screen | [INFERRED] anisotropy can be silently imported by geometry-fitting choices, especially if later steps align coordinates with a preferred tube axis |

## Step-3 Readiness Recommendation

- [INFERRED] The branch should advance to the dynamic plausibility screen.
- [INFERRED] It should advance only on the fixed Step-3 package above.
- [INFERRED] Candidate ranking after scenario/localization fixing:
  - primary:
    `direction coherence + tube persistence`
  - secondary:
    `vorticity-direction coherence`,
    `tube coherence / persistence`
  - effectively dead as promoted routes, retained only as fragility screens:
    `local Beltrami / alignment`,
    `Beltrami deficit + concentration`,
    `Beltrami deficit + anisotropy`

### Why advancement is still justified

- [INFERRED] The primary hybrid remains concrete under an honest,
  non-tube-adapted localization and still names a plausible Tao discriminator.
- [INFERRED] It has not yet collapsed into either:
  - a prior-art direction criterion
  - or purely descriptive tube language
  under the fixed Step-3 package.

### Early invalidation trigger for the next step

- [INFERRED] If the primary hybrid survives only after reintroducing
  tube-adapted localization, tuned threshold/window choices, or stronger
  derivative control than the bounded package contains, the branch should be
  invalidated or replanned rather than drift forward.
