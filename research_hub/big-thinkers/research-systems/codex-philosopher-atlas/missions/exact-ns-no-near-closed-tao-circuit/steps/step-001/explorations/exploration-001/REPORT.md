# Exploration 001 Report — Essential Tao-Circuit Feature Ledger

## Goal

Separate Tao-circuit features that are genuinely load-bearing for this mission
branch from features that are merely convenient packaging, while keeping clear
boundaries between Tao's internal mechanism, exact-NS mismatch claims, and
Step-1 scope-lock commitments.

## Sources Used

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-001/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/CHAIN.md`
- `missions/exact-ns-no-near-closed-tao-circuit/CHAIN-HISTORY.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-001-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-002-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-of-averaged-ns-blowup-firewall-FINAL-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-exact-ns-no-near-closed-tao-circuit-MISSION.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/winning-chain.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/judgments/chain-01.md`
- `runtime/results/codex-patlas-exact-ns-no-near-closed-tao-circuit-step-001-receptionist.md`

## Boundary Rule

- `[VERIFIED]` Tao's internal mechanism comes from the reconstructed
  delayed-threshold circuit and shell cascade in the anatomy reports.
- `[VERIFIED]` Leakage thresholds, packet semantics, canonicalization, and
  downstream-gate requirements come from the Step-1 brief, mission brief, and
  winning-chain scope lock, not from Tao's toy circuit itself.
- `[INFERRED]` The ledger below therefore classifies each feature while also
  noting whether it is inherited from Tao's mechanism or frozen here as branch
  policy.

## Ledger

### 1. Stage order

- Classification: `essential`
- Status: `[VERIFIED]`
- Justification:
  the inherited Atlas reconstruction does not present Tao's mechanism as a
  generic five-node graph. It presents an ordered delayed-abrupt-transfer
  sequence:
  weak pump `X1,n -> X2,n`, tiny seed into `X3,n`, amplification of `X3,n`,
  rotor exchange `X1,n <-> X4,n`, and final transfer `X4,n -> X1,n+1`.
  The final report explicitly calls this the load-bearing mechanism rather than
  a decorative packaging choice. A packet family that scrambles this order is
  no longer Tao-like in the sense the mission inherited.
- Sources:
  `atlas-anatomy-exploration-001-REPORT.md:241-286`
  `atlas-anatomy-exploration-001-REPORT.md:487-492`
  `atlas-anatomy-of-averaged-ns-blowup-firewall-FINAL-REPORT.md:21-31`

### 2. Delayed-threshold behavior

- Classification: `essential`
- Status: `[VERIFIED]`
- Justification:
  the decisive Tao feature is not merely multistage transfer but delayed
  activation created by exponential amplification of an exponentially tiny
  trigger. The final report names delayed threshold activation as the
  load-bearing mechanism, and the exploration-001 reconstruction makes the
  threshold time `t_c` explicit. Removing the delayed-threshold logic collapses
  the mechanism into an ordinary sparse cascade.
- Sources:
  `atlas-anatomy-exploration-001-REPORT.md:274-302`
  `atlas-anatomy-of-averaged-ns-blowup-firewall-FINAL-REPORT.md:25-30`

### 3. Pump / amplifier / rotor / next-shell role hierarchy

- Classification: `essential`
- Status: `[VERIFIED]`
- Justification:
  Tao's circuit depends on distinct roles with distinct causal jobs:
  slow clock, tiny trigger, strong amplifier, rotor-mediated exchange, and
  one-way next-shell transfer. Exploration 002 treats exact-NS coefficient
  rigidity precisely as the threat to reproducing this hierarchy. The role
  hierarchy is therefore part of the object, not merely a later theorem lens.
- Sources:
  `atlas-anatomy-exploration-001-REPORT.md:264-286`
  `atlas-anatomy-exploration-002-REPORT.md:5-15`
  `atlas-anatomy-exploration-002-REPORT.md:37-54`

### 4. Amplitude hierarchy

- Classification: `essential`
- Status: `[INFERRED]`
- Justification:
  the exact numerical constants `ε`, `ε^2 exp(-K^10)`, `ε^(-1) K^10`,
  `ε^(-2)`, and `K` belong to Tao's engineered realization, so those literal
  formulas are not themselves the Step-1 object. But the hierarchy they encode
  is load-bearing:
  one channel must be exponentially weaker than the amplifier channel,
  the amplifier and rotor must dominate after threshold,
  and the final pump must become macroscopic only after the rotor stage.
  Step 2 cannot test Tao-likeness honestly without preserving that ordered size
  hierarchy.
- Sources:
  `atlas-anatomy-exploration-001-REPORT.md:356-416`
  `atlas-anatomy-exploration-002-REPORT.md:40-44`
  `atlas-anatomy-of-averaged-ns-blowup-firewall-FINAL-REPORT.md:62-65`

### 5. Admissible leakage

- Classification: `open but load-bearing`
- Status: `[VERIFIED]` for the need, `[INFERRED]` for the classification
- Justification:
  Tao's averaged mechanism wants unusual isolation, but the inherited mission
  did not yet freeze a single leakage functional or bound. The new mission and
  winning chain explicitly require quantitative leakage language, but they do
  so as a Step-1 scope lock rather than an inherited theorem fact. So leakage
  is not dispensable, but the exact admissibility rule remains to be fixed at
  the branch level.
- Boundary note:
  `[VERIFIED]` This is primarily a branch-policy item, not a literal Tao
  mechanism item.
- Sources:
  `atlas-anatomy-exploration-001-REPORT.md:410-416`
  `atlas-exact-ns-no-near-closed-tao-circuit-MISSION.md:71-121`
  `CHAIN.md:45-67`
  `runtime/results/codex-patlas-exact-ns-no-near-closed-tao-circuit-step-001-receptionist.md:11-18`

### 6. Time-scale separation

- Classification: `essential`
- Status: `[VERIFIED]`
- Justification:
  the shell transfer times must shrink summably while amplitudes remain
  comparable enough for the delayed-abrupt transfer to repeat. Both the
  mechanism reconstruction and the firewall final report mark this as part of
  the load-bearing mechanism. A packet family with no honest time-scale
  separation is not Tao-like, even if it has a suggestive interaction graph.
- Sources:
  `atlas-anatomy-exploration-001-REPORT.md:274-302`
  `atlas-anatomy-exploration-001-REPORT.md:376-396`
  `atlas-anatomy-exploration-002-REPORT.md:44-45`

### 7. Phase sensitivity

- Classification: `open but load-bearing`
- Status: `[INFERRED]`
- Justification:
  the attack on Chain 01 flags phase information as omitted but mathematically
  relevant, and exploration 002 treats sign/size hierarchy as constrained by
  exact triadic geometry rather than freely assigned. The local record does not
  yet give a final canonical phase convention, so phase sensitivity is not yet
  fully frozen. But Step 2 must preserve phase data well enough to distinguish
  true delayed-threshold behavior from a bookkeeping artifact.
- Sources:
  `atlas-anatomy-exploration-001-REPORT.md:471-481`
  `judgments/chain-01.md:21-23`
  `steps/step-001/GOAL.md:24-33`

### 8. Helical-sign sensitivity

- Classification: `open but load-bearing`
- Status: `[INFERRED]`
- Justification:
  the local record repeatedly frames the exact setting as Fourier/helical, and
  the surviving exact-NS candidate mismatch is tied to geometry-fixed
  coefficients and helicity signs. Yet the inherited packet does not fix one
  final helical sign sheet. So helical signs are load-bearing for later exact
  testing, but Step 1 can only freeze the requirement that they be named and
  tracked canonically.
- Sources:
  `atlas-anatomy-exploration-001-REPORT.md:463-469`
  `atlas-anatomy-exploration-002-REPORT.md:29-30`
  `atlas-anatomy-exploration-002-REPORT.md:52-54`

### 9. Support semantics

- Classification: `open but load-bearing`
- Status: `[INFERRED]`
- Justification:
  Step 1 exists partly to decide what `support` means. The exact object cannot
  be stable if support is left ambiguous between single modes, conjugate pairs,
  and packets. The inherited record does not itself settle the object choice;
  it only makes clear that later robustness work cannot proceed without one.
- Boundary note:
  `[PROPOSED]` This is frozen here as branch policy rather than inherited
  directly from Tao's shell mechanism.
- Sources:
  `steps/step-001/GOAL.md:24-44`
  `CHAIN.md:49-88`
  `atlas-exact-ns-no-near-closed-tao-circuit-MISSION.md:71-102`
  `runtime/results/codex-patlas-exact-ns-no-near-closed-tao-circuit-step-001-receptionist.md:15-23`

### 10. Tiny-trigger role

- Classification: `essential`
- Status: `[VERIFIED]`
- Justification:
  both the mechanism reconstruction and the final report single out the tiny
  trigger `X3,n` as the most decisive variable. The trigger is dynamically
  central while energetically negligible before threshold. A candidate that
  lacks this role is at most a sparse cascade analogue, not a Tao-like circuit.
- Sources:
  `atlas-anatomy-exploration-001-REPORT.md:281-302`
  `atlas-anatomy-exploration-001-REPORT.md:370-405`
  `atlas-anatomy-of-averaged-ns-blowup-firewall-FINAL-REPORT.md:62-64`

## What Is Dispensable

- `[INFERRED]` The literal five-scalar ODE coordinates `(a,b,c,d,ã)` are
  dispensable. The branch must preserve the roles, not those names.
- `[INFERRED]` Tao's exact numerical coefficient formulas are dispensable as
  formulas, though their hierarchy is not.
- `[INFERRED]` A polished shell-cascade presentation is dispensable. The branch
  may work with finite Fourier/helical packets instead, provided the role
  ledger survives.

## Canonical Packet-Language Memo

- `[PROPOSED]` Packet object:
  a finite packet-level/helical object rather than a single bare Fourier mode.
- `[PROPOSED]` Real-valuedness rule:
  exact evaluation is always done on the canonically conjugate-completed
  realization; conjugate completion is mandatory bookkeeping, not an alternate
  replacement for packet identity.
- `[PROPOSED]` Canonicalization rule:
  later audits must distinguish true symmetries from fixed canonicalization
  choices from substantive modeling changes, exactly as the winning chain and
  judgment require.
- `[PROPOSED]` Non-cosmetic changes:
  packet regrouping, helical basis changes after the fact, threshold retuning,
  and time-window cherry-picking are substantive.
- Sources:
  `CHAIN.md:111-120`
  `judgments/chain-01.md:25-36`
  `attacks/chain-01.md:11-25`
  `runtime/results/codex-patlas-exact-ns-no-near-closed-tao-circuit-step-001-receptionist.md:15-23`

## Scope-Lock Sheet

- `[PROPOSED]` Freeze packet semantics at the packet/helical-object level.
- `[PROPOSED]` Freeze support bookkeeping to canonical conjugate-completed
  realizations with forced spectator modes recorded explicitly.
- `[PROPOSED]` Freeze leakage language to a predeclared admissibility sheet on
  a predeclared packet family and time window.
- `[PROPOSED]` Freeze the downstream-gate rule:
  every promoted notion must name one invariant observable or one invariant
  admissibility sheet.
- `[PROPOSED]` Freeze the negative buckets:
  `not well-defined`,
  `not robust after canonicalization`,
  `not useful for the target theorem or counterexample question`.
- Sources:
  `steps/step-001/GOAL.md:33-44`
  `CHAIN.md:45-67`
  `winning-chain.md:45-67`
  `CHAIN-HISTORY.md:18-44`

## Tao-Likeness Discriminator

Later steps should treat a packet family as Tao-like only if all of the
following survive after canonicalization:

1. `[VERIFIED]` It contains identifiable carrier, delay-clock, tiny-trigger,
   transfer-conduit, and next-stage carrier roles.
2. `[VERIFIED]` Those roles interact in the ordered delayed-threshold sequence
   inherited from Tao's mechanism, not merely in an arbitrary sparse network.
3. `[INFERRED]` The dominant channels exhibit a real hierarchy:
   weak clock pump,
   much smaller seed,
   larger post-threshold amplifier/rotor response,
   and delayed next-stage transfer.
4. `[INFERRED]` The packet family predeclares phase/helical-sign bookkeeping
   tightly enough that the claimed role hierarchy is not representation drift.
5. `[INFERRED]` Spectator couplings remain bounded by a predeclared admissible
   leakage rule on a predeclared finite time window.
6. `[PROPOSED]` The packet object and its conjugate/helical bookkeeping are
   fixed before testing, not re-chosen after seeing exact interactions.
7. `[PROPOSED]` The notion names one downstream gate for Step 2 and later.

Negative test:

- `[INFERRED]` A family that is only sparse, multiscale, or triad-engineered
  but has no delayed-threshold trigger logic, no role hierarchy, or no honest
  near-isolation screen should not count as Tao-like.

Kill-condition warning:

- `[PROPOSED]` If Step 2 cannot turn role hierarchy, sign/phase/helicity data,
  and admissible leakage into a fixed exact interaction template plus a fixed
  admissibility sheet, the branch should stop in the `not well-defined` bucket
  rather than softening Tao-likeness into rhetoric.

## Outcome

- `[VERIFIED]` The feature ledger can be made sharp enough for Step 1.
- `[INFERRED]` No kill condition fires at the feature-ledger level.
- `[INFERRED]` The remaining ambiguity is not whether a Tao-likeness ledger
  exists, but how to freeze packet/support semantics and canonical
  representation policy for later exact audits.

## Step Verdict

- `[INFERRED]` Step 2 is now well-posed.
- `[PROPOSED]` Frozen commitments for Step 2:
  preserve stage order, delayed threshold, role hierarchy, amplitude hierarchy,
  and time-scale separation as essential;
  require explicit treatment of phase, helical sign, support semantics, and
  leakage;
  use packet-level/helical objects with canonical conjugate-completed
  realizations;
  reject any candidate that survives only by threshold gerrymandering,
  packet-regrouping drift, or re-importing Tao's averaged construction by hand.
