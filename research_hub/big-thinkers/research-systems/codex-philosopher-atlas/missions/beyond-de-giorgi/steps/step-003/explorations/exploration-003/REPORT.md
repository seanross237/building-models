# Exploration 003 Report

## Goal

Define the bounded observable table for Step 3 using the fixed package:

- primary scenario: filament or tube concentration
- comparator scenario: sheet or pancake concentration
- localization protocol:
  - threshold: `|omega| >= r^{-2}`
  - scale: one dyadic ball `B_r(x_*)`
  - time window: `[t_* - r^2, t_*]`
  - type: Eulerian

The table must cover exactly these items:

- primary candidate: direction coherence + tube persistence
- secondary comparators:
  - vorticity-direction coherence
  - tube coherence / persistence
- fragility screens only:
  - local Beltrami / alignment
  - Beltrami deficit + concentration
  - Beltrami deficit + anisotropy

For each item, record:

- scaling or normalization status
- localization data dependence
- scenario addressed
- intended leverage point on the future full-stretching target
- Tao discriminator
- first obvious instability or hidden-normalization risk

## Method

- Read the required local source anchors.
- Extract the fixed Step-3 constraints from prior explorations and step records.
- Build one bounded table with `[VERIFIED]`, `[INFERRED]`, and `[PROPOSED]` labels.
- End with a Step-3 readiness recommendation without entering the dynamic plausibility screen itself.

## Findings Log

### Initial setup

- [VERIFIED] Report skeleton created before analysis so later findings can be appended incrementally.

### Fixed Step-3 package inherited before table design

- [VERIFIED] Step 2 already bounded the candidate roles:
  - primary survivor: `direction coherence + tube persistence`
  - secondary comparators: `vorticity-direction coherence`,
    `tube coherence / persistence`
  - fragility screens only: `local Beltrami / alignment`,
    `Beltrami deficit + concentration`, `Beltrami deficit + anisotropy`
  Sources:
  - `missions/beyond-de-giorgi/steps/step-002/RESULTS.md`
  - `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-002/REPORT.md`
- [VERIFIED] Exploration 001 fixed the scenario package:
  - primary: `filament or tube concentration`
  - comparator: `sheet or pancake concentration`
  Source:
  - `missions/beyond-de-giorgi/steps/step-003/explorations/exploration-001/REPORT.md`
- [VERIFIED] Exploration 002 fixed the localization package:
  - threshold: `[PROPOSED] |omega| >= r^{-2}`
  - scale: `[PROPOSED]` one dyadic ball `B_r(x_*)`
  - time window: `[PROPOSED] [t_* - r^2, t_*]`
  - type: `[INFERRED] Eulerian`
  Source:
  - `missions/beyond-de-giorgi/steps/step-003/explorations/exploration-002/REPORT.md`
- [VERIFIED] The live term-level rule remains mechanical:
  every candidate must answer what estimate changes and what full-stretching
  term becomes smaller. Sources:
  - `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
  - `library/factual/geometry-route-screening/geometry-candidates-must-act-on-full-stretching.md`
- [PROPOSED] For this bounded table, the shared localization data package is
  the Eulerian intense set
  `E_r(t) = {x in B_r(x_*) : |omega(x,t)| >= r^{-2}}`
  on
  `Q_r(x_*, t_*) = B_r(x_*) x [t_* - r^2, t_*]`.
  This packages the Step-3 localization without adding tube-adapted coordinates
  or local-max/quantile normalizations.

## Bounded Observable Table

| Candidate | Role | Scaling / normalization status | Localization data dependence | Scenario addressed | Intended leverage point on future full-stretching target | Tao discriminator | First obvious instability / hidden-normalization risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `direction coherence + tube persistence` | primary | [INFERRED] mixed but still bounded: direction coherence is dimensionless, while persistence is only scale-credible when computed on the fixed dyadic Eulerian package rather than on tube-fitted coordinates | [PROPOSED] uses the Step-3 intense set `E_r(t)` on `Q_r(x_*, t_*)`; [INFERRED] it also needs a rule for matching coherent intense components across the same window without re-centering or re-fitting a tube axis | [INFERRED] primary filament/tube scenario; it is only a stress-tested comparator on sheet/pancake concentration | [INFERRED] best chance to shrink the exterior/inter-scale stretching contribution or the localization-evolution cost by preserving coherent direction structure on an intense tube family | [INFERRED] static tube snapshots survive Tao-style averaging, but joint persistence of direction coherence along a coherent tube family across scale/time is the feature most plausibly destroyed by averaging | [INFERRED] collapses if coherence only appears after tube-adapted relocalization or tuned threshold/window choices; it also fails if no smaller full-stretching term can be named |
| `vorticity-direction coherence` | secondary comparator | [INFERRED] dimensionless as a direction-field observable, but its force under this package depends on how coherence is measured on `E_r(t)` | [PROPOSED] depends on the vorticity-direction field on the Eulerian intense set and on the same parabolic window | [INFERRED] addresses both filament/tube and sheet/pancake scenarios as a cross-scenario comparator | [INFERRED] could at best make the stretching factor `xi . S xi` or a localized exterior contribution smaller, if coherence persists under the fixed localization | [INFERRED] prior-art direction-regularity statements are Tao-robust benchmark material; only a genuinely localized persistence effect beyond that criterion family would clear the Tao screen | [INFERRED] can collapse back into existing direction-regularity criteria or secretly require stronger `nabla xi` control than the bounded package contains |
| `tube coherence / persistence` | secondary comparator | [INFERRED] not clearly scale-invariant by itself; it inherits any scale-credibility only from the fixed `r^{-2}` threshold and dyadic-scale package | [PROPOSED] depends on connectedness or coherence of intense components inside the Eulerian thresholded set across the parabolic window | [INFERRED] mainly filament/tube primary scenario; useful only as a misfit detector on the sheet/pancake comparator | [INFERRED] could only matter by suppressing exterior/inter-scale stretching or localization-evolution cost; tube existence alone does not point to a smaller term | [INFERRED] one-time tube-shaped concentration is Tao-robust; only persistence across scales/time is plausibly destroyed by averaging | [INFERRED] very prone to descriptive slippage: if the table cannot say what full-stretching term becomes smaller, tube language is dead even if coherent structures look vivid |
| `local Beltrami / alignment` | fragility screen only | [VERIFIED] dimensionless alignment-type quantity, but not enough for operational control under this package | [INFERRED] uses local `u` and `omega` data on the same intense set; does not require a special scenario to be stated | [INFERRED] diagnostic in either scenario, not a promoted route | [INFERRED] at most tests whether local/self-induced depletion is unusually strong; it does not directly target the full exterior/nonlocal stretching burden | [VERIFIED] static alignment language is largely Tao-robust and already benchmark-collapsed unless it reaches full stretching | [VERIFIED] controls the wrong object too easily, drifting toward `u x omega` or local depletion rather than full `S omega . omega` |
| `Beltrami deficit + concentration` | fragility screen only | [INFERRED] normalization is fragile because concentration strength depends explicitly on the thresholded intense set; any advantage is hostage to threshold choice | [INFERRED] depends on alignment plus the Eulerian thresholded concentration profile in `E_r(t)` | [INFERRED] mostly filament/tube primary scenario, but only as a diagnostic hybrid | [INFERRED] hoped leverage would be a more favorable core-versus-exterior split, but the local record contains no full-stretching bridge under the fixed package | [INFERRED] only a dynamic coupling between concentrated aligned cores and a smaller full-stretching term would beat Tao-style robustness | [INFERRED] easiest place for hidden normalization: if the hybrid looks good only because the threshold isolates unusually aligned cores, the route is manufactured by localization |
| `Beltrami deficit + anisotropy` | fragility screen only | [INFERRED] normalization depends on how anisotropy is extracted from the thresholded set; not stable enough to promote under the current package | [INFERRED] depends on alignment plus shape data of `E_r(t)` inside the Eulerian ball | [INFERRED] mainly filament/tube primary scenario, since anisotropy is supposed to gesture toward tube-like geometry | [INFERRED] hoped leverage is a smaller kernel angular factor or exterior remainder in a later stretching representation | [INFERRED] only a genuinely NS-specific persistence of anisotropic coherent cores would survive Tao-style averaging | [INFERRED] anisotropy can be silently imported by geometry-fitting choices, especially if later steps start aligning the coordinates with a preferred tube axis |

### Table reading

- [INFERRED] The fixed Step-3 package preserves one honest primary candidate:
  `direction coherence + tube persistence`.
- [INFERRED] `vorticity-direction coherence` and `tube coherence / persistence`
  remain worth carrying only as secondary comparators:
  - direction coherence tests whether the hybrid is adding anything beyond
    prior-art benchmark material
  - tube persistence tests whether there is any stretching-facing content left
    after removing the direction part
- [INFERRED] Beltrami-alignment candidates remain effectively dead as
  operational routes:
  the fixed Eulerian localization does not rescue them, and the full-stretching
  rule still exposes that they do not name a reliable smaller term.

## Ranking And Readiness

### Candidate ranking

- [INFERRED] Primary:
  `direction coherence + tube persistence`
- [INFERRED] Secondary:
  - `vorticity-direction coherence`
  - `tube coherence / persistence`
- [INFERRED] Effectively dead as promoted routes, retained only as fragility
  screens:
  - `local Beltrami / alignment`
  - `Beltrami deficit + concentration`
  - `Beltrami deficit + anisotropy`

### Step-3 readiness recommendation

- [INFERRED] The branch should advance to the dynamic plausibility screen, but
  only narrowly.
- [INFERRED] Reason:
  after fixing both the scenario class and a non-overfitted localization
  package, the primary hybrid is still concrete enough to test without
  collapsing into pure imagery or prior-art restatement.
- [INFERRED] Boundary on that advancement:
  the next step should immediately ask what quantity is actually propagated on
  the Eulerian intense set over `[t_* - r^2, t_*]`, and whether that
  propagation can plausibly shrink the exterior/inter-scale stretching burden
  or the localization-evolution cost.
- [INFERRED] Early invalidation trigger for the next step:
  if the primary hybrid survives only after reintroducing tube-adapted
  localization, tuned threshold/window choices, or stronger direction
  derivatives than the bounded package contains, the branch should be
  invalidated or replanned rather than carried forward.

## Dead Ends And Failed Attempts

- [VERIFIED] The local record does not supply a canonical formula-level
  observable for any of the six entries once the Step-3 package is fixed.
  Trying to extract one directly from the repository would have forced a new
  hidden normalization choice, so the table stays at the bounded schematic
  level required by the step.
- [INFERRED] Re-promoting Beltrami-based hybrids as live candidates was ruled
  out again under the fixed Step-3 package. The scenario/localization choices
  did not repair their core target mismatch.

## Conclusion

- Outcome: `succeeded`
- Compact ranking:
  - primary: `direction coherence + tube persistence`
  - secondary: `vorticity-direction coherence`,
    `tube coherence / persistence`
  - fragility only / effectively dead operationally:
    `local Beltrami / alignment`,
    `Beltrami deficit + concentration`,
    `Beltrami deficit + anisotropy`
- Step-3 recommendation:
  advance to the dynamic plausibility screen, but only with the fixed
  scenario/localization package and with an explicit willingness to kill the
  hybrid if no real propagation mechanism appears immediately.
