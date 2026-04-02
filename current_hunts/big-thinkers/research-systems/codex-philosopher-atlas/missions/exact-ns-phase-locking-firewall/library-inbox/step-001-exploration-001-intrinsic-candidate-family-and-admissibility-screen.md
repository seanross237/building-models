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

- `[VERIFIED]` The local mission record requires any admissible object to be
  built from exact Fourier/helical interaction data and to avoid desired-channel
  or packet-role labels in the raw definition. That requirement is explicit in
  `MISSION.md`, `GOAL.md`, `winning-chain.md`, and `refined/chain-03.md`.
- `[INFERRED]` The honest quotient relation for this step has five layers:
  1. triad-orbit relabeling:
     cyclic permutation of `(k,p,q)` and equivalent helical-orbit
     representatives, with the matching exact coefficient change;
  2. real-valued conjugate completion:
     replacing a mode by its forced conjugate representative must not change
     the object except by the obvious conjugation action;
  3. helical-basis phase and sign conventions:
     changing the helical basis representative or sign sheet is allowed only if
     the object transforms covariantly and the physically meaningful value is
     unchanged;
  4. gauge / anchor conventions:
     phase-anchor choices, translation-gauge choices, and representative
     choices are canonicalization data, not new objects;
  5. amplitude normalization:
     uniform rescaling or a different normalization anchor must not change the
     object's status, except where the candidate is explicitly only a
     canonically normalized summary.
- `[INFERRED]` Status rules for this exploration:
  `intrinsic` means invariant under all five layers above and definable without
  desired-channel annotation;
  `canonically representable but non-intrinsic` means the object can be written
  honestly after fixing a canonical aggregation or normalization sheet, but the
  scalar object itself is not forced by the exact symmetry class;
  `inadmissible` means the raw definition already imports desired channels,
  packet roles, frozen itinerary content, or another forbidden annotation.

## Candidate Family

Assume a finite exact helical support `S` with active helical modes
`a_m`,
where `m = (k, sigma)`,
and exact active triad orbits `tau = (k,p,q; sigma_k, sigma_p, sigma_q)` with
`p + q = k`
and exact coefficient `C_tau != 0`.

Define the coefficient-corrected interaction phase

```text
z_tau(a)
  := C_tau a_p a_q overline(a_k)
      / (|C_tau| |a_p| |a_q| |a_k|),
Theta_tau(a) := arg z_tau(a).
```

This is the exact phase combination that enters the normalized transfer term

```text
Re(C_tau a_p a_q overline(a_k))
  = |C_tau| |a_p| |a_q| |a_k| cos Theta_tau.
```

### Candidate 1 - Exact triad-phase orbit measure

- `[PROPOSED]` Raw definition:

  ```text
  Mu_S(a) := sum_{tau in T(S)} delta_{z_tau(a)}
  ```

  or equivalently the triad-orbit multiset
  `{ Theta_tau(a) mod 2pi }_{tau in T(S) }`.
- `[INFERRED]` Why this is delayed-transfer-facing:
  it records the exact phase combinations that directly determine the sign and
  strength of each normalized triad transfer contribution, without prelabeling
  which triads are "good" or "bad".
- `[INFERRED]` Status:
  `intrinsic`.
- `[INFERRED]` Decisive reason:
  the coefficient-corrected phase `z_tau` is invariant under conjugate
  completion, triad relabeling, helical-basis rephasing, and uniform amplitude
  normalization, and its raw formula names only exact interaction data.

### Candidate 2 - Transfer-weighted aggregate coherence score

- `[PROPOSED]` Raw definition:

  ```text
  C_S(a)
    := (sum_{tau in T(S)} w_tau(a) Re z_tau(a))
       / (sum_{tau in T(S)} w_tau(a)),
  w_tau(a) := |C_tau| |a_p| |a_q| |a_k|.
  ```

- `[INFERRED]` Why this is delayed-transfer-facing:
  it compresses the whole active support into one scalar that rewards strong
  simultaneous alignment of the triads carrying the largest instantaneous exact
  interaction weight.
- `[INFERRED]` Status:
  `canonically representable but non-intrinsic`.
- `[INFERRED]` Decisive reason:
  the underlying `z_tau` data are intrinsic, but the decision to collapse them
  to one scalar and the choice of weights are not forced by exact symmetry.
  Other equally natural summaries
  (unweighted average,
  phase entropy,
  median phase defect,
  sign-only counts)
  are canonically available on the same support.

### Candidate 3 - Desired-vs-spectator coherence split

- `[PROPOSED]` Raw definition:

  ```text
  D_{A,R}(a)
    := (sum_{tau in A} w_tau(a) Re z_tau(a)) / W_A
       - (sum_{tau in R} w_tau(a) Re z_tau(a)) / W_R,
  ```

  where `A` is a predeclared desired-transfer triad set and `R` is a
  predeclared spectator set.
- `[INFERRED]` Why this is delayed-transfer-facing:
  it tries to separate phase alignment on the transfer route from phase
  alignment on the spectator burden.
- `[INFERRED]` Status:
  `inadmissible`.
- `[INFERRED]` Decisive reason:
  the raw definition already names desired and spectator subsets, so the object
  has meaning only after importing the target transfer direction by hand.
  That is exactly the definition-level failure warned against in `MISSION.md`
  and `GOAL.md`.

## Audit Matrix

| Candidate | Conjugate / relabel invariance | Gauge / normalization status | Depends on desired labels? | Status |
| --- | --- | --- | --- | --- |
| `Mu_S(a)` | `[INFERRED]` yes, after quotienting by triad orbit and coefficient phase | `[INFERRED]` yes | `[VERIFIED]` no | `intrinsic` |
| `C_S(a)` | `[INFERRED]` yes on a fixed support | `[INFERRED]` only after fixing one aggregation convention | `[VERIFIED]` no | `canonically representable but non-intrinsic` |
| `D_{A,R}(a)` | `[INFERRED]` can be made canonical on a fixed sheet | `[INFERRED]` yes after normalization | `[VERIFIED]` yes | `inadmissible` |

## Exploration Verdict

- `[INFERRED]` The best surviving intrinsic object for this branch is not a
  desired-channel phase score. It is the exact triad-phase orbit measure
  `Mu_S(a)` or an equivalent coefficient-corrected triad-phase ledger.
- `[INFERRED]` Scalar coherence summaries are still useful, but only as later
  diagnostics built on top of the intrinsic triad-phase ledger rather than as
  the intrinsic object itself.
- `[VERIFIED]` Any raw object that pre-splits desired channels from spectators
  fails the mission's admissibility test immediately.

## Dead Ends / Rejections

- `[VERIFIED]` Reusing packet-role or Step-6 gate labels from the predecessor
  mission as part of the raw phase object is rejected by the mission brief.
- `[INFERRED]` A bare "phase-locking window" object without an underlying exact
  triad ledger was also rejected at this stage because the window and
  threshold choices are policy data rather than intrinsic exact interaction
  data.
