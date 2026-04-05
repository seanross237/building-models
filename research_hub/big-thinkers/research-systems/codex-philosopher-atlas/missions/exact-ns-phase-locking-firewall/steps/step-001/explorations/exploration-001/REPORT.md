# Exploration 001 Report - Intrinsic Candidate Family And Admissibility Screen

## Goal

Identify a very small candidate family of exact phase/coherence objects built
from exact Fourier or helical interaction data, and classify each candidate as
`intrinsic`,
`canonically representable but non-intrinsic`,
or
`inadmissible`
under an explicit equivalence and admissibility test.

## Sources Used

- `missions/exact-ns-phase-locking-firewall/steps/step-001/GOAL.md`
- `missions/exact-ns-phase-locking-firewall/MISSION.md`
- `missions/exact-ns-phase-locking-firewall/CHAIN.md`
- `missions/exact-ns-phase-locking-firewall/CHAIN-HISTORY.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/winning-chain.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/refined/chain-03.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/planner-chains/chain-01.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/planner-chains/chain-04.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/mission-context.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-006/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/controller/decisions/decision-009.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-of-averaged-ns-blowup-firewall-FINAL-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-001-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-002-REPORT.md`
- `library/factual/navier-stokes/INDEX.md`
- `library/factual/navier-stokes/conjugate-completion-is-mandatory-canonicalization-not-primary-packet-identity.md`
- `library/factual/navier-stokes/helical-signs-amplitude-normalization-and-phase-anchor-belong-to-the-frozen-packet-sheet.md`
- `library/factual/navier-stokes/packet-audits-must-separate-true-symmetries-canonicalization-and-substantive-model-changes.md`

## Operational Note

- `[VERIFIED]` The strategist launched
  `codex-patlas-exact-ns-phase-locking-firewall-step-001-explorer-001`
  through `bin/launch-role.sh` with sentinel
  `explorations/exploration-001/REPORT-SUMMARY.md`.
- `[VERIFIED]` The session produced only a report skeleton plus placeholder
  summary fields within the bounded wait.
- `[INFERRED]` This report is therefore completed directly from the anchored
  local record, using the same fallback style already present in earlier
  mission steps when launched sessions did not finish their sentinel outputs.

## Equivalence And Admissibility Test

- `[VERIFIED]` The mission requires raw candidate formulas to use exact
  Fourier/helical interaction data with no desired-channel labels,
  packet sheets,
  or frozen transfer annotations in the raw definition.
  Source basis:
  `missions/exact-ns-phase-locking-firewall/MISSION.md`,
  `missions/exact-ns-phase-locking-firewall/steps/step-001/GOAL.md`,
  `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/winning-chain.md`,
  `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/refined/chain-03.md`.
- `[VERIFIED]` The local Atlas record already insists that one must separate
  true symmetries,
  canonicalization choices,
  and substantive model changes,
  and that conjugate completion is mandatory bookkeeping rather than primary
  object identity.
  Source basis:
  `library/factual/navier-stokes/conjugate-completion-is-mandatory-canonicalization-not-primary-packet-identity.md`,
  `library/factual/navier-stokes/packet-audits-must-separate-true-symmetries-canonicalization-and-substantive-model-changes.md`.

### Ambient exact interaction scalar

- `[INFERRED]` Before any packet or support aggregation, the cleanest exact
  interaction datum attached to one Fourier triad `k = p + q` is

  ```text
  Gamma_{k,p,q}(u)
    := -i * overline{u^(k)} · [ (q · u^(p)) P_k u^(q) ].
  ```

  This is the exact triad contribution coming from the Leray-projected
  quadratic Navier-Stokes interaction.
- `[INFERRED]` In any helical decomposition

  ```text
  u^(m) = sum_s a_s(m) h_s(m),
  ```

  the same scalar expands as

  ```text
  Gamma_{k,p,q}(u)
    = sum_(s_k,s_p,s_q) C_{k,p,q}^{s_k,s_p,s_q}
      a_{s_p}(p) a_{s_q}(q) overline{a_{s_k}(k)}.
  ```

  So a candidate built from `Gamma_{k,p,q}` is already compatible with
  Fourier/helical representation changes rather than tied to one frozen helical
  sheet.

### Explicit quotient relation `E`

- `[PROPOSED]` A candidate is tested against the following equivalences.
  1. Conjugation:

     ```text
     (k,p,q) ~ (-k,-p,-q),
     Gamma_{-k,-p,-q}(u) = overline{Gamma_{k,p,q}(u)}.
     ```

  2. Real-valued conjugate completion:
     forcing the mirror modes required by
     `u^(-m) = overline{u^(m)}`
     must not create a new object.
  3. Helical-sign relabeling:
     rewriting the same field in another helical sign naming must only relabel
     coordinates, not alter the physical object.
  4. Gauge conventions:
     helical basis rephasing or other phase-anchor conventions must transport
     the object tautologically rather than demand a new sign/phase sheet.
  5. Normalization changes:
     replacing amplitudes by another positive normalization
     `b^(m) = lambda_m u^(m)`
     should not change an intrinsic candidate.
  6. Representation changes:
     Fourier and helical presentations of the same exact interaction should be
     identified.
  7. Annotation test:
     any extra data in the raw formula
     such as a chosen finite interaction family,
     window,
     threshold set,
     desired-transfer label,
     or packet/sheet name
     must itself be forced by the equivalence class of the field plus one exact
     interaction class.
     If not, the candidate is not intrinsic.

- `[PROPOSED]` Status rule used in this report:
  `intrinsic`
  means the formula descends under all seven items above;
  `canonically representable but non-intrinsic`
  means the formula is exact but fails the quotient only through frozen
  representational choices such as normalization;
  `inadmissible`
  means the raw formula already imports substantive external annotation.

## Candidate Family

### Candidate 1 - Exact triad interaction phase class

- `[PROPOSED]` Raw definition:

  ```text
  P_[k,p,q](u)
    := Gamma_{k,p,q}(u) / |Gamma_{k,p,q}(u)|
  ```

  when `Gamma_{k,p,q}(u) != 0`,
  and `0` otherwise,
  viewed on the mirror class
  `[k,p,q] = {(k,p,q),(-k,-p,-q)}`.
- `[INFERRED]` Why this is delayed-transfer-facing:
  it isolates the exact phase/coherence direction of one NS interaction
  contribution before any desired transfer route is chosen.
- `[INFERRED]` Why it survives the quotient:
  - conjugation only sends `P` to its tautological complex conjugate on the
    mirror representative;
  - conjugate completion adds no new information beyond that mirror class;
  - helical-sign relabelings and gauge changes only alter how `Gamma` is
    expanded, not the scalar itself;
  - normalization drops out after dividing by `|Gamma|`;
  - Fourier/helical rewrites preserve the same object.
- `[PROPOSED]` Status:
  `intrinsic`.

### Candidate 2 - Exact triad interaction scalar

- `[PROPOSED]` Raw definition:

  ```text
  Gamma_[k,p,q](u)
    := -i * overline{u^(k)} · [ (q · u^(p)) P_k u^(q) ].
  ```

- `[INFERRED]` Why this is delayed-transfer-facing:
  it is the exact cubic interaction currency whose argument drives `Candidate 1`
  and whose magnitude measures instantaneous interaction strength.
- `[INFERRED]` Why it fails intrinsicity:
  under an admissible normalization change

  ```text
  b^(m) = lambda_m u^(m),
  ```

  one gets

  ```text
  Gamma^b_{k,p,q} = lambda_k lambda_p lambda_q Gamma^u_{k,p,q}.
  ```

  So the raw scalar magnitude is not invariant under the quotient relation even
  though the scalar is exact and representation-clean.
- `[PROPOSED]` Status:
  `canonically representable but non-intrinsic`.

### Candidate 3 - Windowed family phase-lock occupancy

- `[PROPOSED]` Raw definition:

  ```text
  L_(S,I,Omega)(u)
    := (1/|I|) ∫_I 1_{ {arg Gamma_tau(t) in Omega for all tau in S} } dt.
  ```

- `[INFERRED]` Why this is delayed-transfer-facing:
  it directly tries to measure whether a chosen interaction family stays in a
  coherent phase window for long enough to support a delayed-transfer story.
- `[INFERRED]` Why it is inadmissible here:
  the object is not forced by
  `field + one exact interaction class`.
  It additionally requires an externally chosen family `S`,
  a window `I`,
  and a phase band `Omega`.
  Those are precisely the kinds of frozen transfer annotations that Step 1 is
  supposed to avoid.
- `[PROPOSED]` Status:
  `inadmissible`.

## Audit Matrix

| Candidate | Conjugation / completion | Helical relabeling / gauge | Normalization | Extra annotation | Status |
| --- | --- | --- | --- | --- | --- |
| `P_[k,p,q](u)` | `[INFERRED]` survives on mirror class | `[INFERRED]` survives | `[INFERRED]` survives | `[VERIFIED]` none | `intrinsic` |
| `Gamma_[k,p,q](u)` | `[INFERRED]` survives | `[INFERRED]` survives | `[INFERRED]` fails | `[VERIFIED]` none | `canonically representable but non-intrinsic` |
| `L_(S,I,Omega)(u)` | `[INFERRED]` can be transported | `[INFERRED]` can be transported | `[INFERRED]` depends on conventions for comparison thresholds | `[VERIFIED]` yes | `inadmissible` |

## Exploration Verdict

- `[PROPOSED]` Best intrinsic survivor:
  `Candidate 1`,
  the exact triad interaction phase class `P_[k,p,q](u)`.
- `[PROPOSED]` Why this is the branch's best Step-2 object:
  it is already smaller than any support-level or window-level summary,
  but still lives directly on exact NS interaction data.
  Step 2 can therefore test closed exact supports by asking what finite set of
  active triad classes appears and what exact compatibility relations among the
  corresponding `P_[k,p,q]` are forced.
- `[PROPOSED]` Immediate Step-2 rejection rule:
  do not promote any object whose raw formula
  already depends on an absolute cubic magnitude
  without freezing normalization,
  or on a chosen family/window of triads.

## Dead Ends / Rejections

- `[VERIFIED]` Reusing packet-role or Step-6 gate labels from the predecessor
  mission as part of the raw phase object is rejected by the current mission
  brief.
- `[INFERRED]` I considered promoting a bare helical relative phase

  ```text
  phi_bare
    := arg a_{s_p}(p) + arg a_{s_q}(q) - arg a_{s_k}(k).
  ```

  I rejected it before the final candidate table because it is not invariant
  under helical gauge rephasing.
  The coefficient phase carried by `Gamma_{k,p,q}` is needed to cancel that
  dependence.
- `[INFERRED]` I also considered treating the support-level multiset of all
  active triad phases as the primary intrinsic survivor.
  I demoted that idea because it is larger than necessary:
  the triad-local phase class already survives the admissibility quotient and
  support-level aggregates can be reconstructed later if needed.
