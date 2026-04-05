# Exploration 002 Report - Exact Interaction Templates And Downstream Gates

## Goal

Attach one exact Fourier/helical interaction template and one honest downstream
gate to each promoted Step-2 candidate, then decide whether Chain Step 3 is
now well-posed.

## Required Context Reviewed

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-001/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/explorations/exploration-001/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/explorations/exploration-001/REPORT-SUMMARY.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-001-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-002-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-of-averaged-ns-blowup-firewall-FINAL-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/final-decider.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/winning-chain.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/planner-chains/chain-02.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/judgments/chain-01.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/judgments/chain-03.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/attacks/chain-01.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/refined/chain-03.md`
- `missions/exact-ns-no-near-closed-tao-circuit/controller/decisions/decision-002.md`
- `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
- `library/factual/navier-stokes/support-means-a-role-labeled-helical-packet-with-mandatory-conjugate-completion.md`
- `library/factual/navier-stokes/conjugate-completion-is-mandatory-canonicalization-not-primary-packet-identity.md`
- `library/factual/navier-stokes/helical-signs-amplitude-normalization-and-phase-anchor-belong-to-the-frozen-packet-sheet.md`
- `library/factual/tao-circuit-feature-ledger/tao-likeness-requires-a-five-part-canonicalization-screen.md`
- `library/factual/tao-circuit-feature-ledger/admissible-leakage-must-be-declared-but-is-a-branch-level-policy-choice.md`
- `runtime/logs/codex-patlas-exact-ns-no-near-closed-tao-circuit-step-002-receptionist-search-attempt-003.md`

## Working Notes

### Skeleton Initialized

- `[VERIFIED]` `REPORT.md` and `REPORT-SUMMARY.md` were created before the
  investigation.

### Exploration 001 Recovery Problem

- `[VERIFIED]` The sibling Exploration 001 artifacts in
  `steps/step-002/explorations/exploration-001/` are still skeletons and do
  not contain an actual promoted shortlist.
- `[INFERRED]` I therefore recovered the intended promoted family from the
  Step-1 freezes, the winning-chain/judgment packet, the firewall final report,
  and the receptionist search log.
- `[INFERRED]` The best-supported promoted set is:
  `Role-Coupling Sheet`,
  `Spectator-Leakage Screen`,
  and
  `Delayed-Threshold Behavior Screen`.
- `[INFERRED]` A pure graph-closure notion should not be promoted. The attack
  packet explicitly says graph closure alone is too combinatorial and too poor
  in phase/helical/amplitude data to be the real object.

## Shared Exact Packet Sheet

- `[VERIFIED]` Every promoted candidate must live on a finite role-labeled
  helical packet with mandatory conjugate completion, not on a bare mode and
  not on a bare conjugate pair.
- `[VERIFIED]` Every promoted candidate inherits one fixed canonical sheet:
  one role ordering,
  one conjugate-representative convention,
  one helical sign sheet,
  one amplitude normalization anchor,
  and one phase anchor or equivalent gauge.
- `[VERIFIED]` The exact Fourier/Leray law every candidate is tracking is

  ```text
  ∂t û(k) + |k|^2 û(k)
    = -i ∑_{p+q=k} (q · û(p)) P_k û(q),
  P_k = I - (k ⊗ k)/|k|^2,
  û(-k) = overline{û(k)}.
  ```

- `[INFERRED]` On a canonical helical sheet

  ```text
  û(k) = ∑_{σ=±} a_σ(k) h_σ(k),
  ```

  each desired channel is an exact triad family
  `(p, q, k; σ_p, σ_q, σ_k)` with one geometry-fixed coefficient
  `C_{k,p,q}^{σ_k,σ_p,σ_q}`. This exploration does not compute those
  coefficients; it identifies which coefficient families later steps must audit.
- `[INFERRED]` I use the Tao-role labels
  `A_n` = carrier,
  `B_n` = delay clock,
  `C_n` = tiny trigger,
  `D_n` = transfer conduit / rotor leg,
  `A_{n+1}` = next-shell carrier.

## Candidate Sheets

### Candidate 1 - Role-Coupling Sheet

- Classification:
  `dual-use`
- Promotion basis:
  `[INFERRED]` This is the recovered pro-near-circuit-friendly candidate. It
  asks directly whether exact Fourier/helical geometry can realize the desired
  Tao role hierarchy without collapsing the question first into a leakage-only
  or behavior-only language.
- Supporting local files:
  `steps/step-001/RESULTS.md`
  `atlas-anatomy-exploration-001-REPORT.md`
  `atlas-anatomy-exploration-002-REPORT.md`
  `atlas-anatomy-of-averaged-ns-blowup-firewall-FINAL-REPORT.md`
  `planning-runs/run-001/judgments/chain-01.md`
  `controller/decisions/decision-002.md`
- Step-1 freezes used:
  `stage order`
  `tiny-trigger centrality`
  `amplitude hierarchy`
  `packet-level helical support`
  `canonical conjugate completion`
  `declared helical sign sheet`
  `declared phase anchor`
  `one downstream gate`
- Recovered criterion:
  `[INFERRED]` A packet family counts as near-closed in this language only if
  its exact helical coefficient sheet exhibits one Tao-like on-template role
  hierarchy together with one predeclared spectator upper-bound sheet on the
  same canonical normalization.
- Packet class:
  `[INFERRED]` One-shell-bridge exact helical packet families of the form

  ```text
  𝒫_n = P(A_n) ∪ P(B_n) ∪ P(C_n) ∪ P(D_n) ∪ P(A_{n+1}) ∪ overline{𝒫_n},
  ```

  where each role packet is finite and carries a fixed sign / amplitude / phase
  sheet.
- Exact interaction template:
  `[INFERRED]` Desired role couplings are the Tao channels written now as exact
  helical triad families:

  ```text
  T_pump : (A_n, A_n) -> B_n
  T_seed : (A_n, A_n) -> C_n
  T_amp  : (B_n, C_n) -> C_n
  T_rot  : (A_n, C_n) -> D_n
           (D_n, C_n) -> A_n
  T_next : (D_n, D_n) -> A_{n+1}
  ```

  `[INFERRED]` The point of the candidate is not merely that these channels
  exist. It is that their exact helical coefficient sheet should realize one
  Tao-like relative order:
  seed much smaller than pump,
  and pump much smaller than the amplifier / rotor / next-shell transfer
  channels, all on one fixed normalization.
- Forced same-scale spectators:
  `[VERIFIED]` Exact NS never gives only a target channel. Once the desired
  triads above are active, the same triads also force reciprocal updates on the
  other legs, for example

  ```text
  (A_n, B_n) -> A_n
  (A_n, C_n) -> C_n
  (B_n, C_n) -> B_n
  (D_n, A_{n+1}) -> D_n
  ```

  with exact sizes and signs fixed by the same helical coefficient sheet.
- Forced conjugate spectators:
  `[VERIFIED]` Real-valuedness forces the mirror packet and therefore mirror
  triads for every desired channel:

  ```text
  (overline{A_n}, overline{A_n}) -> overline{B_n}
  (overline{A_n}, overline{A_n}) -> overline{C_n}
  (overline{B_n}, overline{C_n}) -> overline{C_n}
  (overline{A_n}, overline{C_n}) -> overline{D_n}
  (overline{D_n}, overline{D_n}) -> overline{A_{n+1}}
  ```

  together with any mixed mirror companions admitted by the exact closure rule.
- Forced cross-scale spectators:
  `[INFERRED]` Once `A_{n+1}` is present, the next-shell pump cannot be treated
  as one-way. Later steps must track back-reaction channels involving
  `A_{n+1}` and `D_n`, and any shell-`n` / shell-`n+1` companions forced by the
  chosen geometry.
- Exact data later steps still need:
  `[VERIFIED]`
  one explicit wavevector family for the five roles;
  one helical sign assignment;
  one exact coefficient ledger
  `C_{k,p,q}^{σ_k,σ_p,σ_q}` for all desired and forced triads;
  one amplitude normalization anchor;
  one phase anchor;
  one coefficient-ratio threshold sheet naming exactly which ratios must be
  small or large;
  and one finite packet-closure convention.
- Honest downstream gate:
  `[PROPOSED]` `Invariant admissibility sheet for adversarial exact search.`
  On the normalized one-shell-bridge packet family, the gate should require:
  presence of all five desired channel families,
  one fixed sign pattern,
  one declared coefficient-ratio hierarchy,
  and one fixed upper-bound screen for same-scale / conjugate / cross-scale
  companion coefficients in the same normalization.
- Why this is the right gate:
  `[INFERRED]` This candidate is algebraic before it is dynamical. The next
  honest audit is therefore not simulation first; it is whether the coefficient
  sheet survives canonicalization and whether any exact packet family passes the
  hard admissibility screen at all.

### Candidate 2 - Spectator-Leakage Screen

- Classification:
  `obstruction-oriented`
- Promotion basis:
  `[VERIFIED]` The winning-chain packet and Chain 02 both treat unavoidable
  spectator leakage as the strongest non-coefficient route once exact closure,
  Leray projection, and conjugate completion are enforced.
- Supporting local files:
  `steps/step-001/RESULTS.md`
  `atlas-anatomy-exploration-002-REPORT.md`
  `planning-runs/run-001/planner-chains/chain-02.md`
  `planning-runs/run-001/winning-chain.md`
  `library/factual/tao-circuit-feature-ledger/admissible-leakage-must-be-declared-but-is-a-branch-level-policy-choice.md`
  `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
- Step-1 freezes used:
  `packet-level helical support`
  `canonical conjugate completion`
  `admissible leakage on one fixed window`
  `tiny-trigger centrality`
  `ordered Tao-role template`
  `one downstream gate`
- Recovered criterion:
  `[INFERRED]` A packet family counts as near-closed in this language only if
  the off-template transfer generated by exact closure stays below one
  predeclared fraction of on-template transfer on one fixed normalized window.
- Packet class:
  `[INFERRED]` Exact closed one-shell-bridge packets carrying the five Tao roles
  together with all finitely forced same-scale, conjugate, and cross-scale
  companions under the chosen closure convention.
- Exact interaction template:
  `[INFERRED]` Desired on-template channels are the same Tao-role families as
  in Candidate 1, but now grouped into one `on-template` ledger:

  ```text
  𝒯_on = {
    (A_n, A_n) -> B_n,
    (A_n, A_n) -> C_n,
    (B_n, C_n) -> C_n,
    (A_n, C_n) -> D_n,
    (D_n, C_n) -> A_n,
    (D_n, D_n) -> A_{n+1}
  }.
  ```

  `[INFERRED]` The candidate tracks whether the exact packet can keep the
  complementary interaction set `𝒯_spec` small in one fixed normalization.
- Forced same-scale spectators:
  `[VERIFIED]` The exact ledger must include role-preserving or role-damaging
  companion channels inside the same scale block, including feedback into
  `A_n`, `B_n`, `C_n`, and `D_n` from the very triads meant to realize the Tao
  roles.
- Forced conjugate spectators:
  `[VERIFIED]` The mirror packet creates a second spectator class
  automatically. These are part of the exact closed packet and must enter the
  leakage functional on the same footing as the canonical packet.
- Forced cross-scale spectators:
  `[VERIFIED]` The local atlas packet already says exact NS forces extra
  cross-scale couplings once a desired shell-bridge triad is active. The gate
  must therefore separate shell-`n` / shell-`n+1` desired transfer from other
  shell-bridge companions and long-leg feedback.
- Exact data later steps still need:
  `[VERIFIED]`
  one exact partition of the closed interaction ledger into
  `on-template` and `spectator` classes;
  one fixed norm or projected interaction-strength functional;
  one normalized finite window `I_leak`;
  one initial-data family on the canonical packet sheet;
  and one proof-grade reason why the chosen observable is invariant enough to
  compare packet realizations honestly.
- Honest downstream gate:
  `[PROPOSED]` `One invariant dynamical observable on one stated packet family
  and finite window.`
  The most natural gate is the normalized leakage ratio

  ```text
  L_spec/on(I_leak)
    = ( ∫_{I_leak} Σ_{r in spectator classes}
          ||Π_r B(u,u)||_2^2 dt )
      /
      ( ∫_{I_leak} Σ_{r in on-template classes}
          ||Π_r B(u,u)||_2^2 dt ).
  ```

  The packet family is the canonically normalized exact closed one-shell-bridge
  family above. The window `I_leak` must be fixed before testing.
- Why this is the right gate:
  `[VERIFIED]` This is precisely the Chain-02 downstream question:
  does exact NS force a positive amount of off-template production, or can
  adversarial families drive it to zero while preserving the Tao-role logic?

### Candidate 3 - Delayed-Threshold Behavior Screen

- Classification:
  `dual-use`
- Promotion basis:
  `[VERIFIED]` The Step-1 discriminator and the winning-chain judgment both say
  Tao-likeness is not just a graph or coefficient sheet. It includes ordered
  delayed-threshold behavior, tiny-trigger centrality, amplitude hierarchy, and
  finite-window spectator control.
- Supporting local files:
  `steps/step-001/RESULTS.md`
  `steps/step-001/explorations/exploration-001/REPORT-SUMMARY.md`
  `atlas-anatomy-exploration-001-REPORT.md`
  `planning-runs/run-001/judgments/chain-01.md`
  `planning-runs/run-001/judgments/chain-03.md`
  `planning-runs/run-001/refined/chain-03.md`
- Step-1 freezes used:
  `stage order`
  `delayed-threshold behavior`
  `tiny-trigger centrality`
  `amplitude hierarchy`
  `time-scale separation`
  `packet-level helical support`
  `declared sign / phase / normalization sheet`
  `admissible leakage on one fixed window`
- Recovered criterion:
  `[INFERRED]` A packet family counts as near-closed in this language only if,
  on one fixed finite window, the exact closed dynamics exhibit Tao's ordered
  activation logic with the trigger initially tiny but dynamically decisive, and
  with spectators remaining under one predeclared screen long enough for the
  next-shell transfer attempt to occur.
- Packet class:
  `[INFERRED]` Exact closed canonical packet families containing the same five
  role packets as above, now equipped with explicit initial amplitude ratios and
  a finite time window `I_beh`.
- Exact interaction template:
  `[INFERRED]` The desired channels are still

  ```text
  (A_n, A_n) -> B_n
  (A_n, A_n) -> C_n
  (B_n, C_n) -> C_n
  (A_n, C_n) -> D_n
  (D_n, C_n) -> A_n
  (D_n, D_n) -> A_{n+1}
  ```

  but the candidate tracks them as one ordered temporal script:
  early clock pump,
  tiny seed remains negligible,
  post-threshold amplifier turns on,
  rotor exchange activates,
  delayed next-shell transfer begins.
- Forced same-scale spectators:
  `[VERIFIED]` The same desired triads also push on the carrier, clock, trigger,
  and conduit variables in directions that can destroy delay or threshold order.
  Step 4 will need the exact closed evolution, not a reduced subsystem with
  those companions dropped.
- Forced conjugate spectators:
  `[VERIFIED]` Mirror packet evolution is part of the exact behavior. Delayed
  activation claims are not honest unless the conjugate companions obey the same
  canonicalization rule throughout the window.
- Forced cross-scale spectators:
  `[INFERRED]` Any shell-`n+1` feedback that activates too early is exactly the
  kind of failure mode this candidate must count, so the template must record
  early back-reaction and other cross-scale spill channels explicitly.
- Exact data later steps still need:
  `[VERIFIED]`
  one exact closed amplitude system for the projected packet variables;
  one declared initial amplitude hierarchy;
  one declared phase anchor and helical sign sheet;
  one fixed threshold sheet
  `(θ_B, θ_C, θ_D, θ_{A_{n+1}})`;
  one fixed finite time window `I_beh`;
  and one fixed spectator ceiling on the same window.
- Honest downstream gate:
  `[PROPOSED]` `Invariant admissibility sheet for adversarial exact search on a
  fixed packet family and window.`
  The sheet should require:
  threshold crossing in the order
  `B_n` then `C_n` then `D_n` then `A_{n+1}`,
  the trigger remaining below its seed ceiling before declared activation,
  and spectator channels staying below the declared ceiling on `I_beh`.
- Why this is the right gate:
  `[INFERRED]` The refined Chain 03 packet explicitly rejects a scalar
  Tao-likeness score and replaces it with hard admissibility filters plus a
  diagnostic vector. This candidate should therefore feed Step 4 as a hard
  admissibility sheet, not as one soft score.

## Downstream Gate Ledger

- `[INFERRED]` `Role-Coupling Sheet`
  -> gate type:
  `invariant admissibility sheet for adversarial exact search`
  on canonically normalized one-shell-bridge helical packets.
- `[INFERRED]` `Spectator-Leakage Screen`
  -> gate type:
  `invariant dynamical observable`
  given by the exact off-template / on-template leakage ratio on one fixed
  finite window.
- `[INFERRED]` `Delayed-Threshold Behavior Screen`
  -> gate type:
  `invariant admissibility sheet for adversarial exact search`
  on exact closed packets over one fixed finite activation window.

## Candidate-Family Verdict

- `[INFERRED]` The recovered promoted family is now sharp enough for Chain Step
  3. Each candidate has:
  one exact packet class,
  one exact Tao-role interaction template,
  one explicit same-scale / conjugate / cross-scale spectator ledger,
  one exact list of still-missing data,
  and one honest downstream gate.
- `[INFERRED]` No candidate collapses here into a pure mechanism memo. The
  `Role-Coupling Sheet` is algebraic, the `Spectator-Leakage Screen` is
  observable-based, and the `Delayed-Threshold Behavior Screen` is
  admissibility-based.
- `[INFERRED]` The most vulnerable candidate remains the behavioral one,
  because it is the closest to threshold-gerrymandering if the threshold sheet
  is not frozen before testing. That is now an ordinary Step-3 robustness
  question, not a Step-2 object-missing failure.

## Step 3 Readiness Verdict

- `[INFERRED]` `Chain Step 3 is now well-posed.`
- `[INFERRED]` Why:
  the Step-2 failure conditions named in the brief do not fire on the recovered
  promoted family. No promoted candidate is missing an exact interaction object,
  and no promoted candidate is missing one honest downstream gate.
- `[INFERRED]` What Step 3 should audit next:
  whether the `Role-Coupling Sheet` survives canonicalization without its ratio
  hierarchy drifting under sign-sheet or phase-sheet choices;
  whether the `Spectator-Leakage Screen` uses an invariant-enough observable and
  closure convention;
  and whether the `Delayed-Threshold Behavior Screen` is stable under the frozen
  canonical packet sheet rather than tuned to one representation or one
  cherry-picked window.
- `[INFERRED]` What Step 4 will still need after Step 3:
  explicit wavevector/helicity parameterizations,
  exact coefficient tables,
  exact closed packet ledgers,
  fixed threshold values,
  and one normalized packet family or parameter family per surviving candidate.
- `[INFERRED]` Surviving candidates for Chain Step 3:
  `Role-Coupling Sheet`
  `Spectator-Leakage Screen`
  `Delayed-Threshold Behavior Screen`

## Dead Ends / Failed Attempts

- `[VERIFIED]` The direct Exploration 001 report path was a dead end for
  candidate recovery because both `REPORT.md` and `REPORT-SUMMARY.md` there are
  still skeletons.
- `[INFERRED]` I therefore did not treat those empty files as the promoted
  shortlist. I reconstructed the shortlist from the planning/judgment packet,
  the firewall final report, the Step-1 freezes, and the receptionist log.
- `[INFERRED]` I did not write a fully explicit helical coefficient formula
  `C_{k,p,q}^{σ_k,σ_p,σ_q}` here, because the local record supports only the
  exact Fourier/Leray law and the fact that these coefficients are geometry- and
  helicity-fixed. Writing a formula from memory would have been a source guess,
  not a repository-grounded finding.
