# Exploration 002 Report — Packet Language And Canonical Representation Policy

## Goal

Freeze the packet-language policy for this branch using only the local
repository record.

## Sources Used

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-001/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/CHAIN.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-002-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-exact-ns-no-near-closed-tao-circuit-MISSION.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/winning-chain.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/judgments/chain-01.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/judgments/chain-03.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/final-decider.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/planner.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/planner-chains/chain-02.md`
- `runtime/results/codex-patlas-exact-ns-no-near-closed-tao-circuit-step-001-receptionist.md`

## Packet-Language Recommendation

### Recommended object

- Recommendation: `packet-level helical packet object`
- Status: `[INFERRED]`
- Reason:
  the local record repeatedly frames the exact setting as Fourier/helical and
  warns that exact bookkeeping depends on more than a support graph. The
  receptionist synthesis also notes that the corpus leans away from single-mode
  support toward packet-level or helical-packet language. A single Fourier mode
  is too small to carry Tao's role ledger honestly, while a bare
  conjugate-complete pair is still only bookkeeping, not packet identity.

### What support means

- `[INFERRED]` Support should mean:
  a finite role-labeled set of helical modes together with the exact forced
  conjugate completion required to represent a real-valued velocity field.
- `[INFERRED]` The primary identity of the object is the role-labeled positive
  packet, not the doubled real-valued bookkeeping copy.
- `[VERIFIED]` This matches the branch-wide emphasis on exact closure,
  conjugate bookkeeping, and packet semantics in the winning chain and the
  planning stack.

## Conjugacy, Helicity, And Phase Policy

### Conjugate completion

- Recommendation:
  conjugate completion is mandatory in canonical representation, but it should
  be treated as bookkeeping/canonicalization rather than as the primary notion
  of packet identity.
- Status: `[INFERRED]`
- Reason:
  the attack on Chain 01 correctly says conjugate completion is not merely
  decorative for real-valued fields. At the same time, the planning stack
  discusses packet families and helical supports, not bare conjugate pairs as
  the main object. So the clean Step-1 policy is:
  object identity is a role-labeled packet;
  canonical realization enforces the conjugate mirror packet.

### Helical signs

- Recommendation:
  helical signs are part of the object sheet and must be declared explicitly for
  every promoted packet family.
- Status: `[VERIFIED]` for relevance, `[INFERRED]` for policy
- Reason:
  the inherited exact-NS mismatch is written precisely in terms of
  geometry-fixed coefficients and helicity signs, and the winning chain
  requires sign data to be frozen before robustness work.

### Phase data

- Recommendation:
  later Step-2 candidates must declare a canonical phase convention relative to
  one chosen carrier mode or one equivalent canonical anchor.
- Status: `[INFERRED]`
- Reason:
  the local record does not supply a single inherited phase gauge, but it does
  say phase information is part of the missing object discipline. So Step 1
  should not overclaim a fully invariant phase-free ontology; it should require
  predeclared phase bookkeeping.

## Canonical Representation Policy

The local record supports a three-way separation.

### A. True exact symmetries

- `[VERIFIED]` These should be the transformations later candidates must treat
  as genuine invariances.
- `[INFERRED]` For this branch, keep the list narrow and honest:
  only transformations already justified as exact NS symmetries for the chosen
  packet presentation should count here.

### B. Canonicalization choices

- `[VERIFIED]` The winning chain and Chain-01 judgment explicitly require a
  separate canonicalization tier.
- `[INFERRED]` The branch should fix in advance:
  - one half-space or equivalent convention for conjugate representatives;
  - one helical basis convention;
  - one role-label ordering for the packet;
  - one amplitude normalization anchor;
  - one phase anchor or equivalent canonical gauge.
- `[INFERRED]` Dependence on these choices is not automatically fatal if the
  choice was fixed up front and later audits test stability there.

### C. Substantive modeling changes

- `[VERIFIED]` The attack on Chain 01 identifies these explicitly:
  packet regrouping,
  treating conjugate completion as optional,
  retuning thresholds,
  changing time windows,
  changing support semantics,
  or using a different helical sign sheet.
- `[INFERRED]` Later robustness work should treat these as different packet
  models, not as cosmetic rewrites.

## Cosmetic Vs Substantive Table

| Change | Classification | Reason |
| --- | --- | --- |
| reordering role labels after a fixed canonical packet order | cosmetic | bookkeeping only once the order is fixed up front |
| displaying the mandatory conjugate packet explicitly versus implicitly | cosmetic after canonicalization | same real-valued packet if the canonical completion rule is fixed |
| changing the chosen half-space representative for conjugate pairs without changing the completed packet | cosmetic after canonicalization | representative change only |
| changing helical basis convention without a fixed canonical rule | substantive until canonicalized | can alter how interactions are recorded |
| regrouping modes into different packets | substantive | changes nonlinear bookkeeping and may change the audited object |
| changing support from single modes to packet objects or vice versa | substantive | changes the object itself |
| retuning leakage thresholds or time windows | substantive | can gerrymander the object |
| changing helical sign assignments or relative phase sheet | substantive | changes the exact interaction template |

## Step-2 Inheritance Verdict

- `[INFERRED]` Step 2 can inherit one fixed packet semantics without
  representation cherry-picking.
- Recommended inherited object:
  a finite role-labeled helical packet, canonically completed to a real-valued
  packet by mandatory conjugate mirrors.
- Recommended inheritance rules:
  - every candidate must declare its helical sign sheet;
  - every candidate must use the same canonical conjugate-completion rule;
  - every candidate must state one amplitude normalization and one phase anchor;
  - later robustness work may vary true symmetries and canonical
    representatives, but not support semantics, regrouping, time windows, or
    thresholds by convenience.

## Outcome

- `[VERIFIED]` The local record is strong enough to reject support ambiguity as
  a harmless detail.
- `[INFERRED]` The best Step-1 freeze is a packet-level helical object with
  conjugate completion treated as mandatory canonical bookkeeping.
- `[INFERRED]` No third exploration is needed solely to decide packet semantics;
  the remaining work is step-level synthesis into the scope-lock sheet.
