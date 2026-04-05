# Exploration 002 Report

## Goal

Operationalize the Tao screen for the geometry route so later steps can apply
it mechanically to the candidate ingredients named in the local chain
materials.

## Source Basis

Required anchors reviewed:

- `missions/beyond-de-giorgi/steps/step-002/GOAL.md`
- `missions/beyond-de-giorgi/MISSION.md`
- `missions/beyond-de-giorgi/CHAIN.md`
- `missions/beyond-de-giorgi/planning-runs/run-002/refined/chain-02.md`
- `missions/beyond-de-giorgi/planning-runs/run-002/selected/chain-02.md`
- `missions/beyond-de-giorgi/planning-runs/run-002/attacks/chain-02.md`
- `missions/beyond-de-giorgi/planning-runs/run-002/judgments/chain-02.md`
- `missions/beyond-de-giorgi/steps/step-001/RESULTS.md`
- `library/factual/far-field-pressure-obstruction/generic-harmonic-regularity-fails-the-tao-gate.md`
- `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`

Additional local calibration sources reviewed:

- `missions/beyond-de-giorgi/planning-runs/run-001/refined/chain-03.md`
- `missions/beyond-de-giorgi/planning-runs/run-001/selected/chain-03.md`
- `missions/beyond-de-giorgi/planning-runs/run-001/judgments/chain-03.md`
- `missions/beyond-de-giorgi/steps/step-001/explorations/exploration-002/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-001/REPORT.md`
- `library/factual/far-field-pressure-obstruction/algebraic-rewrites-and-local-geometry-fail-the-tao-gate.md`

## Method

- Build the Tao screen from repository-supported rules only.
- Keep direct repository statements as `[VERIFIED]`.
- Mark route-specific extensions needed to classify the geometry candidates as
  `[INFERRED]`.
- Enforce the step-001 lesson mechanically:
  - what estimate changes?
  - what exact term or coefficient becomes smaller?

## Working Notes

### Initial skeleton

- Report initialized before final classification.

## Findings

### A. Mechanical Tao-Screen Rule For This Step

- [VERIFIED] The mission and chain fix the eventual live target as the full
  stretching mechanism `S omega . omega`, not a merely local geometric proxy.
  Step 4 and Step 5 of the chain are explicitly about fixing one
  representation of `S omega . omega` and then testing full control of that
  representation.
- [VERIFIED] Step 2 Goal and the refined run-002 chain require Step 1 to split
  the geometry route into three distinct buckets:
  - transport or propagation structure
  - exact algebraic structure
  - multiscale coherence or concentration structure
- [VERIFIED] The step-001 lesson is mechanical and branch-general:
  every candidate must answer
  - what estimate changes?
  - what exact term or coefficient becomes smaller?
- [VERIFIED] Step-001 also established a standing Tao-screen norm:
  generic harmonic-analysis upgrades do not count unless they shrink the actual
  live coefficient or term.
- [VERIFIED] The local geometry planning/judgment texts warn that
  near-Beltrami/Lamb-vector improvement is not enough because the dangerous
  object for this branch is stretching and nonlocal strain, not `u x omega`.
- [INFERRED] For the geometry route, before Step 4 fixes a kernel formula, the
  admissible estimate-level targets can only be named schematically:
  - a smaller local/self-induced stretching contribution
  - a smaller exterior or nonlocal strain contribution
  - a smaller localization/inter-scale interaction term
- [INFERRED] A candidate is `live` only if the repository materials support all
  of the following at least heuristically:
  - the averaged-model analogue would plausibly destroy the decisive feature
  - the candidate points at one of the three target classes above
  - the candidate is not already just a restatement of known static geometry
- [INFERRED] A candidate is `weak but informative` if it identifies a relevant
  stretching-facing feature or scenario discriminator but does not yet name a
  smaller full-stretching term.
- [INFERRED] A candidate is `collapsed to Tao-robust/static geometry` if it is
  only a static singular-integral or alignment description, or if its only
  clean effect is on the Lamb-vector side rather than on full stretching.

### B. Bucket-Level Tao Screen

| Bucket | Tao-style averaged or toy models plausibly preserve | Tao-style averaged or toy models plausibly destroy | Estimate-level target the bucket would need to move | Bucket verdict |
| --- | --- | --- | --- | --- |
| Transport or propagation structure | [VERIFIED] energy-class bounds, incompressibility, and generic harmonic-analysis control; [INFERRED] static snapshots of tubes or aligned regions | [INFERRED] exact NS propagation of localized direction/tube observables, especially any coherence that survives only because real vorticity is transported and stretched in a structured way | [INFERRED] must reduce localization-evolution cost or keep the exterior/inter-scale stretching contribution small enough that a full `S omega . omega` estimate can close, not merely preserve a visual tube picture | [INFERRED] `live` as a bucket, but only through explicit persistence/coherence claims rather than static tube geometry |
| Exact algebraic structure | [VERIFIED] generic quadratic / singular-integral structure and identity-level rewrites; [VERIFIED] Tao preserves standard CZ/LP/Sobolev structure | [INFERRED] only genuinely NS-specific pointwise/algebraic couplings that tie a geometric observable directly to `S omega . omega`, not merely to `u x omega` or to a repackaged norm inequality | [INFERRED] must make a defined stretching kernel factor or remainder term smaller in one fixed representation; improvement of the Lamb vector or of exact-Beltrami anchor cases is insufficient | [INFERRED] `weak but informative` at bucket level: the exact `S omega` coupling is the right target class, but the local candidate family currently lands mostly on wrong-target Beltrami language |
| Multiscale coherence or concentration structure | [INFERRED] one-scale concentration, static anisotropy, and descriptive coherent-structure snapshots | [INFERRED] coherent cross-scale direction/tube organization that depends on real NS dynamics and would be scrambled by averaging | [INFERRED] must make the nonlocal/exterior part of stretching or an inter-scale interaction term smaller; concentration by itself is not enough | [INFERRED] `weak but informative` as a bucket: pure concentration collapses, but coherence paired with persistence may survive |

### C. Tao-Screen Table For Concrete Candidate Families

| Candidate family | Primary bucket | What Tao-style averaged or toy models plausibly preserve | What they plausibly destroy | Estimate-level target the candidate would need to move | Verdict | Short reason |
| --- | --- | --- | --- | --- | --- | --- |
| Local Beltrami deficit or alignment | Exact algebraic structure | [VERIFIED] static local alignment language and exact-Beltrami anchor cases; [VERIFIED] generic harmonic-analysis structure; [INFERRED] local aligned snapshots can persist as descriptive data | [INFERRED] at most an exact NS-specific transport law for alignment, but no such law is identified in the local record | [VERIFIED] would need to control full stretching `S omega . omega`; [INFERRED] concretely it would have to shrink the exterior/nonlocal strain remainder, not just a local self-induced or Lamb-vector piece | `collapsed to Tao-robust/static geometry` | [VERIFIED] local texts say exact Beltrami cancellation targets the wrong quantity and that local deficit does not by itself control nonlocal strain; [INFERRED] no estimate-level full-stretching gain is named |
| Vorticity-direction coherence | Multiscale coherence or concentration structure, with transport secondary | [VERIFIED] the route already overlaps Constantin-Fefferman-style direction criteria; [INFERRED] a static direction-regularity condition can survive as a criterion statement | [INFERRED] exact persistence of direction coherence on intense regions or along coherent filaments, if such persistence depends on true NS transport/stretching | [INFERRED] must make the stretching factor `xi · S xi` smaller in a full representation, including exterior contributions, or else produce a new bridge beyond restating an existing direction criterion | `weak but informative` | [VERIFIED] this family is genuinely stretching-facing and tied to known geometry criteria, but [INFERRED] the local record gives no new term-level bridge from local coherence to a smaller full-stretching term |
| Tube coherence or persistence | Transport or propagation structure, with multiscale secondary | [INFERRED] static tube-shaped concentration or one-time coherent-structure descriptions | [INFERRED] any exact or approximate persistence of a tube family across scales and time, which is the most plausible place where Tao-style averaging would scramble the geometry | [INFERRED] must suppress the exterior/inter-scale contribution to `S omega . omega` or the localization-evolution cost; tube existence alone is not enough | `weak but informative` | [VERIFIED] chain and judgments insist persistence should matter early; [INFERRED] tube persistence is the strongest NS-specific discriminator in this family, but by itself it still does not name a smaller stretching term |
| Beltrami deficit plus concentration | Hybrid: exact algebraic + multiscale concentration | [INFERRED] localized high-`|omega|` concentration and local alignment snapshots | [INFERRED] little beyond whatever true transport of the concentrated aligned core might preserve; the local record does not supply more | [INFERRED] would need concentration to turn local alignment into control of the full stretching integral by making the exterior field negligible relative to the core | `weak but informative` | [VERIFIED] run-001 and run-002 texts warn concentration alone is descriptive and Beltrami alone misses nonlocal strain; [INFERRED] the combination helps define a scenario but still lacks a named full-stretching reduction |
| Beltrami deficit plus anisotropy | Hybrid: exact algebraic + multiscale coherence | [INFERRED] static anisotropic tube or filament geometry and local alignment descriptors | [INFERRED] any genuine NS-specific persistence of anisotropic coherent cores under transport/stretching | [INFERRED] would need the anisotropy to make a kernel-level angular factor or exterior remainder in `S omega . omega` smaller, not merely make the core look filamentary | `weak but informative` | [INFERRED] this is better aimed than Beltrami-alone because anisotropy gestures toward kernel structure, but the local repository still contains no concrete estimate or transport law that turns that gesture into control |
| Direction coherence plus tube persistence | Hybrid: transport/propagation + multiscale coherence | [INFERRED] a static snapshot of aligned directions inside a tube family | [INFERRED] the combination of directional coherence with coherent tube persistence across time and scale, which is the clearest locally suggested feature that Tao-style averaging should plausibly destroy | [INFERRED] must reduce the full stretching interaction by making `xi · S xi` small not only in the core but also after accounting for exterior/inter-scale interactions in the fixed representation chosen later | `live` | [VERIFIED] the refined chain explicitly allows hybrid observables and moves dynamics earlier; [INFERRED] this is the only locally suggested family that simultaneously names a stretching-facing quantity and a plausible NS-specific persistence discriminator, even though the actual estimate is still missing |

### D. Bucket-By-Bucket Reading

#### 1. Transport or propagation structure

- [VERIFIED] The local chain attack/judgment record says persistence was placed
  too late and should constrain observable choice early.
- [INFERRED] That makes propagation the one bucket that remains clearly
  Tao-sensitive after the static geometry is discounted.
- [INFERRED] But transport is only mission-live when attached to a stretching
  target. Tube persistence alone is therefore not enough; it survives mainly as
  one half of `direction coherence plus tube persistence`.

#### 2. Exact algebraic structure

- [VERIFIED] Step-001 already killed identity-level algebraic repackaging on
  the pressure branch, and the geometry judgments separately say Beltrami
  cancellation aims at the wrong object.
- [INFERRED] The exact-algebraic bucket is not empty in principle, because an
  exact link from a geometric observable to `S omega . omega` would be the
  right kind of mechanism.
- [INFERRED] But none of the locally named concrete candidates currently
  supplies that link. The Beltrami family therefore collapses as an operational
  route, while Beltrami hybrids remain only diagnostic.

#### 3. Multiscale coherence or concentration structure

- [VERIFIED] The local judgment texts explicitly say concentration alone is
  descriptive, not a depletion mechanism.
- [INFERRED] Static coherence facts are too close to Tao-robust geometry unless
  they are paired with a dynamic persistence claim.
- [INFERRED] This bucket therefore contributes only through hybrids, with
  `direction coherence plus tube persistence` the sole candidate that stays
  above the collapse line.

### E. Prior-Art Calibration Memo

- [VERIFIED] `vorticity-direction coherence` already sits in the orbit of
  Constantin-Fefferman-style criteria and later direction-coherence work, as
  explicitly acknowledged in the mission and run-002 materials.
- [VERIFIED] `local Beltrami deficit or alignment` already sits inside the
  mission's known exact-Beltrami / near-Beltrami discussion, and the local
  planning/judgment record already treats Beltrami as fragile and often aimed
  at the wrong object.
- [INFERRED] `tube coherence or persistence` is less sharply benchmarked in the
  repository as a theorem family, but the chain repeatedly treats it as the
  natural transport-heavy complement to direction coherence.
- [INFERRED] The main redundancy risk is therefore:
  - Beltrami language that only redescribes local depletion
  - direction-coherence language that only restates known conditional criteria
  - concentration language that only redescribes intense-set geometry
- [INFERRED] The only local escape from that redundancy is a hybrid where
  dynamic persistence is not decorative but is the reason a full stretching
  term should become smaller.

## Dead Ends / Limits

### Dead Ends

- [VERIFIED] Pure local Beltrami alignment is a dead end as a standalone Step-2
  route. The local record repeatedly says it improves the wrong object unless
  it is upgraded to control the full stretching mechanism.
- [VERIFIED] Pure concentration of high-`|omega|` regions is a dead end as a
  control claim. The run-001 judgment explicitly treats concentration alone as
  descriptive rather than depleting.
- [INFERRED] Static tube imagery without a persistence or stretching link is a
  dead end for the Tao screen. It may help choose a scenario later, but it does
  not by itself move an estimate.

### Limits

- [VERIFIED] The repository materials for this step do not yet fix the
  scenario class, localization protocol, or kernel-level representation of
  `S omega . omega`.
- [INFERRED] Because of that, the estimate targets in the table are necessarily
  schematic rather than formula-level.
- [VERIFIED] The repo also does not include a full literature dossier on the
  geometric regularity papers themselves. Prior-art calibration here is
  therefore limited to what the mission and chain materials explicitly encode.

## Recommendation

### Step-2 Readiness Recommendation

- [INFERRED] Step 2 should proceed, but only in a narrowed form.
- [INFERRED] Promote exactly one primary survivor:
  - `direction coherence plus tube persistence`
- [INFERRED] Keep two secondary inputs only as diagnostic comparators, not as
  standalone control routes:
  - `vorticity-direction coherence`
  - `tube coherence or persistence`
- [INFERRED] Downgrade the Beltrami family to non-live status for this chain
  step:
  - `local Beltrami deficit or alignment` is collapsed
  - `Beltrami deficit plus concentration` is only weakly informative
  - `Beltrami deficit plus anisotropy` is only weakly informative
- [INFERRED] Operational instruction for Step 2:
  choose scenario class and localization in a way that tests one specific
  question only:
  does direction coherence persist along a coherent tube family strongly enough
  to make a full stretching contribution, including the exterior/inter-scale
  part, smaller in a fixed representation?

### Bottom Line

- [INFERRED] The geometry route is not killed at Step 1.
- [INFERRED] But it survives only after a severe narrowing:
  static Beltrami-style geometry is screened out, and the live content is
  almost entirely the transport-plus-coherence hybrid rather than any single
  static observable.
