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

### 3. Pump / amplifier / rotor / next-shell role hierarchy

- Classification: `essential`
- Status: `[VERIFIED]`
- Justification:
  Tao's circuit depends on distinct roles with distinct causal jobs:
  slow clock, tiny trigger, strong amplifier, rotor-mediated exchange, and
  one-way next-shell transfer. Exploration 002 treats exact-NS coefficient
  rigidity precisely as the threat to reproducing this hierarchy. The role
  hierarchy is therefore part of the object, not merely a later theorem lens.

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

### 6. Time-scale separation

- Classification: `essential`
- Status: `[VERIFIED]`
- Justification:
  the shell transfer times must shrink summably while amplitudes remain
  comparable enough for the delayed-abrupt transfer to repeat. Both the
  mechanism reconstruction and the firewall final report mark this as part of
  the load-bearing mechanism. A packet family with no honest time-scale
  separation is not Tao-like, even if it has a suggestive interaction graph.

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

### 9. Support semantics

- Classification: `essential`
- Status: `[INFERRED]`
- Justification:
  Step 1 exists partly to decide what `support` means. The exact object cannot
  be stable if support is left ambiguous between single modes, conjugate pairs,
  and packets. The specific object choice is handled in Exploration 002, but
  fixing support semantics itself is clearly essential rather than optional.

### 10. Tiny-trigger role

- Classification: `essential`
- Status: `[VERIFIED]`
- Justification:
  both the mechanism reconstruction and the final report single out the tiny
  trigger `X3,n` as the most decisive variable. The trigger is dynamically
  central while energetically negligible before threshold. A candidate that
  lacks this role is at most a sparse cascade analogue, not a Tao-like circuit.

## What Is Dispensable

- `[INFERRED]` The literal five-scalar ODE coordinates `(a,b,c,d,ã)` are
  dispensable. The branch must preserve the roles, not those names.
- `[INFERRED]` Tao's exact numerical coefficient formulas are dispensable as
  formulas, though their hierarchy is not.
- `[INFERRED]` A polished shell-cascade presentation is dispensable. The branch
  may work with finite Fourier/helical packets instead, provided the role
  ledger survives.

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

Negative test:

- `[INFERRED]` A family that is only sparse, multiscale, or triad-engineered
  but has no delayed-threshold trigger logic, no role hierarchy, or no honest
  near-isolation screen should not count as Tao-like.

## Outcome

- `[VERIFIED]` The feature ledger can be made sharp enough for Step 1.
- `[INFERRED]` No kill condition fires at the feature-ledger level.
- `[INFERRED]` The remaining ambiguity is not whether a Tao-likeness ledger
  exists, but how to freeze packet/support semantics and canonical
  representation policy for later exact audits.
