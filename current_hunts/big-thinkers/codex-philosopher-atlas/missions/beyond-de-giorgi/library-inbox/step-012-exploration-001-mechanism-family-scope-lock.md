# Exploration 001 Report

## Goal

Freeze one honest mechanism-family-observable triple for the stochastic branch,
or say plainly that the repository leaves only a representation menu rather than
a concrete Step-1 setup.

## Method

- Read the step goal and canonical chain gate:
  `steps/step-012/GOAL.md`, `CHAIN.md`.
- Read the high-priority planning anchors:
  `planning-runs/run-007/planner-chains/chain-04.md`,
  `planning-runs/run-008/planner-chains/chain-04.md`,
  `planning-runs/run-008/selected/chain-03.md`,
  `planning-runs/run-008/refined/chain-03.md`,
  `planning-runs/run-008/attacks/chain-03.md`,
  `planning-runs/run-008/judgments/chain-03.md`,
  `planning-runs/run-008/final-decider.md`,
  `planning-runs/run-008/selector.md`.
- Extract the strongest supported answers to:
  - the first mechanism burden,
  - the single best-supported family,
  - the most concrete observable name on disk,
  - whether the record actually exits menu-level planning.

## Findings Log

### Initial anchors

- [VERIFIED] Step 12 and the canonical chain both define Step 1 as a hard
  admissibility gate: one mechanism, one family, one observable, or else stop
  before exact-identity expansion. Sources:
  - `steps/step-012/GOAL.md:11-27`
  - `steps/step-012/GOAL.md:168-186`
  - `CHAIN.md:27-46`
- [VERIFIED] The chain explicitly says local concentration exclusion is the
  default endpoint family, and continuation is allowed only if the observable
  already looks near-coercive. Sources:
  - `planning-runs/run-008/refined/chain-03.md:40-44`
  - `planning-runs/run-008/refined/chain-03.md:77-82`
  - `planning-runs/run-008/judgments/chain-03.md:73-79`

### Mechanism-family-observable table

| item | frozen choice | status | support | why this beats nearby options |
| --- | --- | --- | --- | --- |
| Mechanism burden | `local concentration of active scales` | `[INFERRED]` best-supported first burden, but not explicitly frozen as a final Step-1 choice on disk | The refined chain scope lock lists concentration among the allowed burdens and makes `local concentration exclusion first` the default endpoint family; the attack and judgment both say concentration exclusion is more realistic than continuation for stochastic transport. Sources: `planning-runs/run-008/refined/chain-03.md:29-44`, `planning-runs/run-008/attacks/chain-03.md:15-19`, `planning-runs/run-008/judgments/chain-03.md:73-79`, `CHAIN.md:29-45` | `vortex stretching growth` and `loss of control along advected filaments` remain menu entries only. Concentration is the only burden repeatedly privileged by endpoint policy rather than merely listed. |
| Primary stochastic family | `backward stochastic flow / back-to-label transport` | `[INFERRED]` favored comparator neighborhood, not canonically frozen | The run-007 stochastic chain names `a Constantin-Iyer representation term` and `a stochastic back-to-label observable` explicitly; the run-008 selected chain keeps `backward stochastic flow` in the short family menu; the final decider still names `backward-flow` as part of the branch reservoir. Sources: `planning-runs/run-007/planner-chains/chain-04.md:23-34`, `planning-runs/run-008/selected/chain-03.md:22-35`, `planning-runs/run-008/final-decider.md:16-19` | This is the only family with an explicitly named comparator neighborhood on disk. `stochastic Kelvin circulation` and generic `martingale` language remain broader and less anchored. |
| Candidate observable | `stochastic back-to-label observable` | `[INFERRED]` most concrete observable name on disk, but still formula-free | The run-007 chain names `a stochastic back-to-label observable` explicitly, alongside the Constantin-Iyer term. The refined run-008 chain later collapses back to broader labels like `backward-flow observable` and `specific stochastic observable`, without fixing a formula. Sources: `planning-runs/run-007/planner-chains/chain-04.md:26-33`, `planning-runs/run-008/refined/chain-03.md:18-19`, `planning-runs/run-008/refined/chain-03.md:51-55` | It is more concrete than `circulation` or `martingale observable` because it is named as an observable and sits in the only explicitly named comparator neighborhood. |
| Why that family is the best first test | `best match to the concentration-first endpoint, and the only option with a named prior-art neighborhood` | `[INFERRED]` | The record repeatedly says continuation is too demanding unless near-coercivity already appears, while concentration exclusion is the natural first endpoint. A transport/back-to-label object is the only family named concretely enough to test that burden without pretending generic martingale language is already a mechanism. Sources: `planning-runs/run-008/attacks/chain-03.md:15-19`, `planning-runs/run-008/judgments/chain-03.md:34-39`, `planning-runs/run-008/judgments/chain-03.md:73-79` | It beats nearby options by reducing the menu most honestly. It does not beat them by having an already-earned estimate. |
| Real mechanism-facing triple? | `No: only a provisional best-supported triple survives` | `[VERIFIED]` obstruction | Step 12 and the canonical chain both say the branch must stop if the mechanism/family/observable set cannot be fixed concretely. The attack and judgment both say the branch still delays the decisive coercive observable question. No source freezes a concrete back-to-label quantity with a theorem-facing gain. Sources: `steps/step-012/GOAL.md:16-27`, `steps/step-012/GOAL.md:173-183`, `CHAIN.md:27-46`, `planning-runs/run-008/attacks/chain-03.md:7-9`, `planning-runs/run-008/attacks/chain-03.md:37-51`, `planning-runs/run-008/judgments/chain-03.md:5-7`, `planning-runs/run-008/judgments/chain-03.md:19-24` | This beats overclaiming. A forced positive freeze here would violate the branch’s own anti-repackaging and coercivity rules. |

### Answers to the required questions

#### 1. Which burden is the sharpest honest first target on the local record?

- [INFERRED] The sharpest honest first target is `local concentration of active
  scales`, not because the repository derives a concentration mechanism, but
  because the run-008 record repeatedly privileges `local concentration
  exclusion` as the default endpoint while treating continuation as too
  coercive for early admission.
- [VERIFIED] The chain documents do not comparably privilege `vortex stretching
  growth` or `loss of control along advected filaments`; those remain entries in
  a burden menu. Sources:
  - `planning-runs/run-008/refined/chain-03.md:29-44`
  - `planning-runs/run-008/refined/chain-03.md:77-90`
  - `planning-runs/run-008/judgments/chain-03.md:73-79`
  - `CHAIN.md:29-45`

#### 2. Which stochastic family is best supported as a first test?

- [INFERRED] `backward stochastic flow / back-to-label transport` is the best
  supported first family.
- [VERIFIED] The reason is not that the repository proves it works. The reason
  is narrower: it is the only family with an explicitly named comparator
  neighborhood (`Constantin-Iyer`) and an explicitly named observable
  (`stochastic back-to-label observable`), while Kelvin/circulation/martingale
  remain mostly family labels. Sources:
  - `planning-runs/run-007/planner-chains/chain-04.md:23-34`
  - `planning-runs/run-008/selected/chain-03.md:25-29`
  - `planning-runs/run-008/final-decider.md:16-19`

#### 3. What exact candidate observable is the most concrete on the repository record?

- [INFERRED] The most concrete candidate observable on disk is the named
  `stochastic back-to-label observable`.
- [VERIFIED] The record does not freeze its exact formula, insertion point, or
  blowup-facing gain. So the repository gives a name, not a working observable
  packet. Sources:
  - `planning-runs/run-007/planner-chains/chain-04.md:26-33`
  - `planning-runs/run-008/refined/chain-03.md:51-55`
  - `planning-runs/run-008/attacks/chain-03.md:37-51`

#### 4. Does the evidence support a real mechanism-facing triple, or only planning language that never exits representational variety?

- [VERIFIED] The evidence supports only a provisional menu-trim, not a real
  frozen Step-1 triple.
- [VERIFIED] The branch certainly narrows the admissibility rules: one
  mechanism, one family, one observable, concentration-first endpoint,
  expectation-only failure bucket, and early coercivity demand.
- [VERIFIED] But the planning archive still never fixes the actual back-to-label
  quantity tightly enough to clear its own Step-1 bar. The attack and judgment
  both say the decisive problem remains: no concrete coercive observable is
  frozen early enough. Sources:
  - `steps/step-012/GOAL.md:16-27`
  - `CHAIN.md:27-46`
  - `planning-runs/run-008/attacks/chain-03.md:7-19`
  - `planning-runs/run-008/attacks/chain-03.md:37-51`
  - `planning-runs/run-008/judgments/chain-03.md:5-7`
  - `planning-runs/run-008/judgments/chain-03.md:16-25`

#### 5. If one triple is still honest, what would count as a real gain, and what would already fail as expectation-only or rhetorical packaging?

- [PROPOSED] The only honest provisional triple is:
  `local concentration of active scales`
  + `backward stochastic flow / back-to-label transport`
  + `stochastic back-to-label observable`.
- [VERIFIED] A real gain on that burden would have to be a local or pathwise
  concentration-exclusion consequence that survives localization, stopping, and
  solution-class pressure, rather than a global expectation identity. That is
  exactly the branch’s own admissibility rule. Sources:
  - `planning-runs/run-008/refined/chain-03.md:5-12`
  - `planning-runs/run-008/refined/chain-03.md:59-64`
  - `CHAIN.md:5-12`
  - `CHAIN.md:61-66`
- [VERIFIED] What already fails:
  - expectation-only control with no local/pathwise consequence;
  - exact stochastic rewriting that adds no endpoint-facing estimate;
  - a martingale or transport identity whose usable content is only the
    deterministic burden rewritten through expectation, filtration, or imported
    machinery. Sources:
    - `steps/step-012/GOAL.md:16-27`
    - `steps/step-012/GOAL.md:173-183`
    - `CHAIN.md:38-45`
    - `planning-runs/run-008/judgments/chain-03.md:24-39`

## Mechanism memo

- [VERIFIED] The local record wants a mechanism-first branch, not a stochastic
  portfolio. Sources:
  - `planning-runs/run-008/judgments/chain-03.md:41-45`
  - `steps/step-012/GOAL.md:33-43`
- [INFERRED] The only burden clearly favored enough to freeze first is local
  concentration of active scales, because concentration exclusion is the branch
  default endpoint and continuation is demoted unless near-coercive control
  already exists.
- [INFERRED] The best first-test family is back-to-label / backward-flow
  transport, not because the record proves it gives control, but because it is
  the only neighborhood named concretely enough to compare against prior art.
- [VERIFIED] The repository does not yet state the missing one-sentence claim in
  a concrete enough form, namely why this observable should constrain that
  burden beyond expectation-level rewriting. That missing sentence is exactly
  why the setup still fails Step 1.

## Dead Ends / Failed Attempts

- A first `rg` loop used malformed shell quoting and failed with `command not
  found`; reran the search with separate commands.
- [VERIFIED] I looked for any file that actually promoted a fully specified
  stochastic observable beyond menu-level names. I did not find one in the
  required anchors. The strongest hits were still:
  - `a Constantin-Iyer representation term`
  - `a stochastic back-to-label observable`
  - `backward stochastic flow`
  - `specific stochastic observable`

## Source map

### Planning-run evidence

- `planning-runs/run-007/planner-chains/chain-04.md`
- `planning-runs/run-008/planner-chains/chain-04.md`
- `planning-runs/run-008/selected/chain-03.md`
- `planning-runs/run-008/refined/chain-03.md`
- `planning-runs/run-008/attacks/chain-03.md`
- `planning-runs/run-008/judgments/chain-03.md`
- `planning-runs/run-008/final-decider.md`
- `planning-runs/run-008/selector.md`

### Step-level mission evidence

- `steps/step-012/GOAL.md`
- `CHAIN.md`

### New synthesis in this report

- The best-supported provisional triple is:
  `local concentration of active scales`
  + `backward stochastic flow / back-to-label transport`
  + `stochastic back-to-label observable`.
- That triple is still not concretely frozen enough to count as a passed Step-1
  setup, because the observable never exits name-level planning.

## Conclusion

`scope lock remains menu-level`

- [VERIFIED] The repository narrows the branch honestly toward one likely
  corridor: concentration-first endpoint discipline and a back-to-label /
  backward-flow comparator neighborhood.
- [VERIFIED] It does **not** yet freeze a real mechanism-family-observable
  triple with a concrete, theorem-facing observable and a non-rhetorical claim
  of leverage.
- [VERIFIED] The correct Step-1 reading from the local record is therefore a
  setup obstruction, not a genuine frozen entry point for Step 2.
