# Step 2 Results — Prior-Art Benchmark And Tao Screen For The Geometry Route

## Completion Status

Step 2 is complete.

- Kill condition fired: **no**
- Branch status: **survives only in a narrowed form**
- Honest summary: the geometry route is not dead, but Step 1 eliminates all
  broad standalone geometry claims and leaves only one primary survivor:
  `direction coherence + tube persistence`

## Source Basis

Primary step outputs:

- `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-001/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-001/REPORT-SUMMARY.md`
- `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-002/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-002/REPORT-SUMMARY.md`

Main underlying local sources:

- `missions/beyond-de-giorgi/steps/step-002/GOAL.md`
- `missions/beyond-de-giorgi/MISSION.md`
- `missions/beyond-de-giorgi/CHAIN.md`
- `missions/beyond-de-giorgi/planning-runs/run-002/refined/chain-02.md`
- `missions/beyond-de-giorgi/planning-runs/run-002/selected/chain-02.md`
- `missions/beyond-de-giorgi/planning-runs/run-002/attacks/chain-02.md`
- `missions/beyond-de-giorgi/planning-runs/run-002/judgments/chain-02.md`
- `missions/beyond-de-giorgi/planning-runs/run-001/refined/chain-03.md`
- `missions/beyond-de-giorgi/planning-runs/run-001/selected/chain-03.md`
- `missions/beyond-de-giorgi/planning-runs/run-001/attacks/chain-03.md`
- `missions/beyond-de-giorgi/planning-runs/run-001/judgments/chain-03.md`
- `missions/beyond-de-giorgi/steps/step-001/RESULTS.md`
- `library/factual/far-field-pressure-obstruction/INDEX.md`
- `library/factual/far-field-pressure-obstruction/generic-harmonic-regularity-fails-the-tao-gate.md`
- `library/factual/far-field-pressure-obstruction/algebraic-rewrites-and-local-geometry-fail-the-tao-gate.md`
- `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`

## Prior-Art Benchmark Memo

### 1. Vorticity-direction coherence / direction regularity

- [VERIFIED] The local record already places this family inside existing
  geometry criteria: `missions/beyond-de-giorgi/MISSION.md` names the
  Constantin-Fefferman route directly, and
  `missions/beyond-de-giorgi/planning-runs/run-002/refined/chain-02.md`
  explicitly requires benchmarking against Constantin-Fefferman-Majda style
  direction coherence and later vorticity-direction coherence work.
- [VERIFIED] The run-001 and run-002 chain materials treat
  `vorticity-direction regularity` as a known candidate criterion family, not
  as an unexplored object.
- [INFERRED] Claim boundary:
  a Step 2 route that merely says "regularity follows from sufficiently regular
  vorticity direction," or that reaches such a statement only by importing
  `nabla xi`-type control, is a relabeling of prior-art structure.
- [INFERRED] Benchmark verdict:
  not live as a standalone novelty claim.
  It remains useful only as a benchmark target or as one half of a later
  dynamic hybrid.

### 2. Geometric depletion / local Beltrami or alignment

- [VERIFIED] `missions/beyond-de-giorgi/MISSION.md` already records the main
  prior-art boundary: exact Beltrami kills the Lamb-vector / pressure-side
  Calderon-Zygmund loss, but the effect is extremely fragile and does not
  survive even small perturbation from exact alignment.
- [VERIFIED] The geometry-chain attacks and judgments say Beltrami language is
  not enough because the real target is full stretching `S omega . omega`,
  not `u x omega` or another local-looking piece.
- [VERIFIED] `missions/beyond-de-giorgi/steps/step-001/RESULTS.md` and the
  curated far-field obstruction notes already forbid treating local geometry or
  static singular-integral repackaging as mission-live progress.
- [INFERRED] Claim boundary:
  a Step 2 claim is not new if it rests only on local alignment, Lamb-vector
  depletion, or near-Beltrami language without controlling full stretching,
  including nonlocal/exterior contributions.
- [INFERRED] Benchmark verdict:
  standalone Beltrami/alignment is collapsed as a primary route.
  Only hybridized versions, such as Beltrami deficit plus concentration or
  anisotropy, remain worth carrying as weak probes.

### 3. Tube coherence or persistence

- [VERIFIED] The local chain materials consistently separate tube coherence or
  persistence from both direction regularity and Beltrami deficit:
  `missions/beyond-de-giorgi/planning-runs/run-002/selected/chain-02.md` and
  `missions/beyond-de-giorgi/planning-runs/run-001/refined/chain-03.md`.
- [VERIFIED] The refined chain treats a persistence mechanism for coherent
  structures across scales as a plausible NS-specific ingredient that would be
  distinct from static singular-integral geometry.
- [VERIFIED] The attack/judgment record also makes clear that descriptive tube
  language alone earns nothing; persistence has to be an explicit organizing
  mechanism, not a late embellishment.
- [INFERRED] Claim boundary:
  no novelty claim is earned by "tube-like intense regions" or "coherent tube
  snapshots" unless a propagated quantity, fixed scenario/localization, and a
  concrete effect on full stretching are specified.
- [INFERRED] Benchmark verdict:
  this is the least pre-killed family in the local record, but only as a
  dynamic or hybrid route rather than as a ready-made criterion.

### Prior-Art Bottom Line

- [INFERRED] Standalone `vorticity-direction coherence` is prior-art calibrated.
- [INFERRED] Standalone `local Beltrami / alignment` is pre-killed as a primary
  operational route.
- [INFERRED] `tube coherence / persistence` remains the only family with real
  Step-2 value, and even then only in a narrow dynamic form.

## Tao-Screen Table

| Candidate | Bucket | Tao-style averaging plausibly preserves | Tao-style averaging plausibly destroys | Classification |
| --- | --- | --- | --- | --- |
| Local Beltrami deficit or alignment | algebraic | static alignment language, exact-Beltrami anchor cases, generic CZ/LP/Sobolev structure | any exact NS transport/stretching leverage tied to persistent alignment | `collapsed to Tao-robust/static geometry` |
| Vorticity-direction coherence | transport + coherence | criterion-level direction regularity and static coherence statements | dynamic persistence of localized direction coherence under exact NS transport/stretching | `weak but informative` |
| Tube coherence or persistence | transport + multiscale coherence | one-time coherent-tube snapshots and descriptive intense-set geometry | coherent persistence across scales and times that Tao-style averaging would wash out | `weak but informative` |
| Beltrami deficit plus concentration | algebraic + concentration | local alignment plus intensity localization as static data | any true dynamic coupling between concentrated aligned cores and full stretching reduction | `weak but informative` |
| Beltrami deficit plus anisotropy | algebraic + coherence | static anisotropic filament geometry plus alignment descriptors | any NS-specific persistence or kernel-facing anisotropic reduction of stretching | `weak but informative` |
| Direction coherence plus tube persistence | transport + multiscale coherence | static aligned tube snapshots | joint persistence of coherent directions along a tube family across scales/time | `live` |

### Tao-Screen Reading

- [VERIFIED] The branch-wide mechanical rule from
  `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
  still controls this step:
  every candidate must say what estimate changes and what exact term becomes
  smaller.
- [INFERRED] For this geometry step, the only candidates that survive are those
  whose essential content is dynamic coherence or persistence, not static
  geometry.
- [INFERRED] `direction coherence + tube persistence` is the only primary
  survivor because it is the sole candidate family that is both
  stretching-facing and plausibly destroyed by Tao-style averaging.

## Step-2 Readiness Recommendation

- [INFERRED] Step 2 should proceed.
- [INFERRED] It should proceed only on a bounded survivor list:
  - primary survivor: `direction coherence + tube persistence`
  - secondary comparators: `vorticity-direction coherence`, `tube coherence / persistence`
  - downgraded fragility screens: `local Beltrami / alignment`,
    `Beltrami deficit + concentration`, `Beltrami deficit + anisotropy`
- [INFERRED] Step 2 must still fix, before any stronger claim:
  - one or two concrete singular-scenario classes
  - one localization protocol
  - one fixed kernel-level representation of `S omega . omega`
- [PROPOSED] The first Step-2 test should ask:
  can direction coherence persist along a coherent tube family strongly enough
  to make a full stretching contribution, including exterior/inter-scale
  interactions, smaller in one fixed representation?

## Honest Bottom Line

- [VERIFIED] This step did the required prior-art benchmark and Tao screen.
- [VERIFIED] It forbids novelty claims based on static singular-integral
  geometry, criterion restatement, or standalone Beltrami rhetoric.
- [INFERRED] The branch remains mission-live, but only barely:
  the survivor set has narrowed to one transport-plus-coherence hybrid.
- [INFERRED] That narrowing is a valid success state for this step.
