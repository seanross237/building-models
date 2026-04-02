# Step 1 Results - Fix The Intrinsic Object, Equivalence Test, Search Class, And Metrics

## Completion Status

- Step complete: **yes**
- Kill condition fired: **no**
- Chain Step 2 well-posed: **yes**
- Honest summary:
  `[INFERRED]` the branch now freezes one intrinsic phase/coherence object,
  one exact search class, one recursive closure policy, and one quantitative
  metric sheet.
  The surviving intrinsic object is the coefficient-corrected exact
  triad-phase orbit measure on a closed helical support ledger.
  Scalar coherence scores remain diagnostic only.
- Operational note:
  `[VERIFIED]` the required receptionist query was attempted synchronously
  through `bin/run-role.sh`, but it did not return within a bounded wait in
  this nested environment;
  `[VERIFIED]` all three exploration sessions were launched through
  `bin/launch-role.sh`, but only skeleton or partial files landed within the
  bounded wait, so the exploration reports were completed directly from the
  anchored local record;
  `[VERIFIED]` all three curator handoffs were launched, but their receipt
  files were still pending when this result was written.

## Source Basis

Primary Step-1 outputs:

- `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-001/REPORT-SUMMARY.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-002/REPORT-SUMMARY.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-003/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-003/REPORT-SUMMARY.md`

Main inherited local sources:

- `missions/exact-ns-phase-locking-firewall/MISSION.md`
- `missions/exact-ns-phase-locking-firewall/CHAIN.md`
- `missions/exact-ns-phase-locking-firewall/CHAIN-HISTORY.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/winning-chain.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/refined/chain-01.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/refined/chain-03.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/planner-chains/chain-01.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/planner-chains/chain-04.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/attacks/chain-01.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/attacks/chain-02.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/judgments/chain-01.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-006/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/controller/decisions/decision-009.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-of-averaged-ns-blowup-firewall-FINAL-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-001-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-002-REPORT.md`
- `library/factual/navier-stokes/INDEX.md`
- `library/factual/navier-stokes/support-means-a-role-labeled-helical-packet-with-mandatory-conjugate-completion.md`
- `library/factual/navier-stokes/conjugate-completion-is-mandatory-canonicalization-not-primary-packet-identity.md`
- `library/factual/navier-stokes/helical-signs-amplitude-normalization-and-phase-anchor-belong-to-the-frozen-packet-sheet.md`
- `library/factual/navier-stokes/packet-audits-must-separate-true-symmetries-canonicalization-and-substantive-model-changes.md`
- `library/factual/tao-circuit-feature-ledger/INDEX.md`

## Intrinsic-Object Memo

Assume a finite exact helical support `S` with active helical modes
`a_m`,
where `m = (k, sigma)`,
and exact active triad orbits `tau = (k,p,q; sigma_k, sigma_p, sigma_q)` with
`p + q = k`
and exact coefficient `C_tau != 0`.

Define

```text
z_tau(a)
  := C_tau a_p a_q overline(a_k)
      / (|C_tau| |a_p| |a_q| |a_k|),
Theta_tau(a) := arg z_tau(a).
```

### Candidate 1 - Exact triad-phase orbit measure

- `[PROPOSED]` Raw definition:

  ```text
  Mu_S(a) := sum_{tau in T(S)} delta_{z_tau(a)}
  ```

  or equivalently the triad-orbit multiset
  `{ Theta_tau(a) mod 2pi }_{tau in T(S) }`.
- `[INFERRED]` Why it is delayed-transfer-facing:
  it records the exact phase combinations that enter the normalized transfer
  terms of the active triads, without prelabeling any route as desired.
- `[INFERRED]` Status:
  `intrinsic`.

### Candidate 2 - Transfer-weighted aggregate coherence score

- `[PROPOSED]` Raw definition:

  ```text
  C_S(a)
    := (sum_{tau in T(S)} w_tau(a) Re z_tau(a))
       / (sum_{tau in T(S)} w_tau(a)),
  w_tau(a) := |C_tau| |a_p| |a_q| |a_k|.
  ```

- `[INFERRED]` Why it is delayed-transfer-facing:
  it rewards simultaneous alignment of the strongest exact triad interactions
  on the support.
- `[INFERRED]` Status:
  `canonically representable but non-intrinsic`.

### Candidate 3 - Desired-vs-spectator coherence split

- `[PROPOSED]` Raw definition:

  ```text
  D_{A,R}(a)
    := (sum_{tau in A} w_tau(a) Re z_tau(a)) / W_A
       - (sum_{tau in R} w_tau(a) Re z_tau(a)) / W_R,
  ```

  where `A` is a predeclared desired-transfer triad set and `R` a predeclared
  spectator set.
- `[INFERRED]` Why it is delayed-transfer-facing:
  it tries to separate phase alignment on the transfer route from phase
  alignment on spectator routes.
- `[INFERRED]` Status:
  `inadmissible`.

## Equivalence And Admissibility Sheet

- `[INFERRED]` The admissibility test must quotient by:
  1. triad-orbit relabeling and coefficient-consistent permutation;
  2. real-valued conjugate completion and representative choice;
  3. helical-basis phase / sign conventions;
  4. gauge or phase-anchor conventions;
  5. uniform amplitude normalization.
- `[VERIFIED]` The raw object must not name desired channels, packet roles, or
  frozen transfer itinerary labels; that requirement is explicit in
  `MISSION.md`, `GOAL.md`, `CHAIN.md`, and `winning-chain.md`.
- `[INFERRED]` Candidate statuses and decisive reasons:
  1. `Mu_S(a)`:
     `intrinsic`,
     because the coefficient-corrected triad phase survives the allowed
     quotient operations and uses only exact interaction data.
  2. `C_S(a)`:
     `canonically representable but non-intrinsic`,
     because its scalar aggregation law and weighting are not symmetry-forced
     even though the underlying triad-phase data are.
  3. `D_{A,R}(a)`:
     `inadmissible`,
     because its raw formula already imports the desired-vs-spectator split by
     hand.

## Exact Search-Class Memo

- `[INFERRED]` Exact search object:
  finite helical mode supports

  ```text
  S subset { (k, sigma) : k in Z^3 \ {0}, sigma in {+, -} }
  ```

  modulo exact symmetries, with mandatory conjugate completion.
- `[INFERRED]` Why helical supports:
  helical sign data enters the exact coefficient law and phase bookkeeping, so
  bare Fourier supports would erase load-bearing structure too early.
- `[VERIFIED]` Why not packet objects:
  the current mission explicitly defaults to finite Fourier/helical supports
  unless a sharper alternative is justified, and it forbids importing
  packet-role annotation into the raw object layer.

### Closure Convention

- `[VERIFIED]` Recursive exact closure is mandatory.
- `[INFERRED]` Frozen closure rule for a seed ledger `S_0`:
  1. add all forced conjugates required by real-valuedness;
  2. whenever two current modes participate in an exact helical triad with
     nonzero projected coefficient, add the third mode and its conjugate;
  3. include every helical sign sector forced by the exact interaction law;
  4. iterate until a fixed point `cl(S_0)` is reached or the current budget is
     exceeded.

### Spectator Inclusion

- `[VERIFIED]` Spectators belong in the closure audit from the start.
- `[INFERRED]` Every mode in `cl(S_0) \ S_0` enters immediately as a
  closure-forced spectator or companion mode.
  The label is descriptive only; it does not permit pruning the mode out.

### Admissible Enlargements

- `[INFERRED]` Enlargement rule 1:
  add one complete wavevector-helicity orbit
  (with its conjugate representative)
  to the seed ledger and rerun closure.
- `[INFERRED]` Enlargement rule 2:
  add one complete exact triad orbit sharing at least one mode with the
  current closed support, together with all symmetry partners required by
  conjugation and triad relabeling, and rerun closure.

### Smallest-First Ordering

- `[INFERRED]` Enumerate seeds lexicographically by:
  1. number of independent seed wavevector-helicity orbits up to conjugation;
  2. shell span / geometric scale ratio;
  3. dimension of the free geometric parameter family.
- `[INFERRED]` Compare fixed points within one seed budget by:
  1. closed-support size after recursive closure;
  2. number of exact active triad orbits;
  3. size of the closure-forced spectator ledger.

### Escalation Ladder

- `[INFERRED]` Start with:
  1. one exact triad orbit;
  2. two-triad shared-mode clusters;
  3. three-triad clusters with one repeated wavevector across two scales;
  4. then increase the seed orbit count by one and repeat.
- `[VERIFIED]` Any negative conclusion before final mission comparison is
  class-limited to the current ladder level and budget.

## Quantitative Metric Sheet

Assume later steps fix a recursively closed support `S`, a source set `A`,
target set `B`, spectator set
`R := S \ (A union B)`,
and one exact trajectory.
The partition `A / B / R` must be declared before any trajectory is scored.

### Exact inflow observable

- `[PROPOSED]` For any `X subset S`, define

  ```text
  E_X(t) := sum_{m in X} |a_m(t)|^2,
  D_X(t) := sum_{m in X} |k_m|^2 |a_m(t)|^2,
  J_X(t) := E_X(t) - E_X(0) + 2 nu int_0^t D_X(s) ds.
  ```

- `[INFERRED]` `J_X(t)` is the exact cumulative nonlinear inflow to `X`
  after removing viscous loss on the same set.

### Intrinsic clocks

- `[PROPOSED]` Define support activity and clocks by

  ```text
  Q_S(t) := sum_{tau in T(S)} |C_tau| |a_p(t)| |a_q(t)| |a_k(t)|,
  E_S(t) := sum_{m in S} |a_m(t)|^2,
  tau_turn(t) := inf_{0 <= s <= t} E_S(s) / Q_S(s),
  tau_nu(S) := 1 / (nu max_{m in S} |k_m|^2).
  ```

- `[INFERRED]` `tau_turn` is the branch's intrinsic nonlinear clock and
  `tau_nu` the strictest viscous deadline on the support.

### Delayed-transfer event

- `[PROPOSED]` Let `t_*` be the first time such that

  ```text
  J_B(t_*) >= (1/4) E_A(0).
  ```

- `[PROPOSED]` Count this as delayed transfer only if

  ```text
  t_* >= 3 tau_turn(t_*),
  t_* <= (1/4) tau_nu(S).
  ```

- `[INFERRED]` This excludes ordinary turnover-scale exchange and also excludes
  events that occur only after viscosity has already had time to erase the
  support.

### Spectator-burden threshold

- `[PROPOSED]` Require, at the same event time,

  ```text
  J_R(t_*) <= (1/4) J_B(t_*).
  ```

- `[INFERRED]` If more than one quarter of the supporting exact nonlinear
  inflow is absorbed by spectators before the event lands, the candidate fails.

### Robustness standard

- `[PROPOSED]` A single favorable trajectory never counts.
- `[PROPOSED]` The delayed-transfer and spectator-burden inequalities must hold
  either on an open set of reduced initial data after quotienting exact
  symmetries, or on an exact invariant family / normally hyperbolic manifold
  with at least one non-symmetry parameter.

## Step Verdict

- `[INFERRED]` Chain Step 2 is now well-posed.
- `[INFERRED]` Why yes:
  1. one intrinsic phase/coherence object survives the admissibility screen;
  2. one exact support class and recursive closure rule are now frozen;
  3. one enlargement policy, smallest-first ordering, and escalation ladder are
     explicit;
  4. delayed transfer, spectator burden, and robustness are now quantitative.

## Frozen Commitments For Chain Step 2

- `[INFERRED]` Enumerate finite helical support ledgers, not packet-role
  objects.
- `[INFERRED]` Use recursive exact closure with mandatory conjugates and
  immediate spectator inclusion.
- `[INFERRED]` Carry the intrinsic object forward as the exact triad-phase orbit
  measure `Mu_S`; any scalar coherence score is diagnostic only.
- `[INFERRED]` Apply at least one admissible enlargement test to every apparent
  survivor.
- `[INFERRED]` Keep all negative claims class-limited to the current ladder
  level and budget.
- `[INFERRED]` When later steps score trajectories, freeze `A / B / R` before
  evaluation and use the exact formulas for `J_X`, `tau_turn`, `tau_nu`, the
  `1/4` target-transfer threshold, the `1/4` spectator-burden threshold, and
  the non-single-trajectory robustness rule.
