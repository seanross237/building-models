# Exploration 001 Report - Recover The Inherited Fixed Ledger And Remaining Freedoms

## Goal

Recover the exact one-bridge ledger that Step 9 must inherit unchanged, and
separate it from:

- witness-local conclusions tied only to the old `F_SS(1/12)` branch;
- classwise exact-closure burden that Step 8 earned but did not make
  support-level explicit; and
- open freedoms that still must be frozen before any honest exact audited
  realization exists.

## Sources Used

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-009/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-008/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-008/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-008/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-007/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-007/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-007/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-003/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-003/winning-chain.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-003/judgments/chain-02.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-003/attacks/chain-01.md`
- `library/factual/navier-stokes/support-means-a-role-labeled-helical-packet-with-mandatory-conjugate-completion.md`
- `library/factual/navier-stokes/helical-signs-amplitude-normalization-and-phase-anchor-belong-to-the-frozen-packet-sheet.md`
- `library/factual/navier-stokes/conjugate-completion-is-mandatory-canonicalization-not-primary-packet-identity.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/all-promoted-step-2-candidates-share-the-same-forced-exact-ns-extras-around-the-core.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/step-8-stops-at-exact-non-isolability-before-step-3-dynamics-on-the-frozen-ledger.md`

## Operational Note

- `[VERIFIED]` The strategizer attempted a direct launch through
  `CODEX_PATLAS_FORCE_DIRECT=1 bin/launch-role.sh`, but the sandbox blocked
  `tmux` access with
  `error connecting to /private/tmp/tmux-501/default (Operation not permitted)`.
- `[VERIFIED]` The strategizer then re-issued the exploration through
  `bin/launch-role.sh` in nested/request mode under session
  `codex-patlas-exact-ns-no-near-closed-tao-circuit-step-009-explorer-001`.
- `[VERIFIED]` The exploration status file remains `active`, no
  `REPORT-SUMMARY.md` landed within the bounded wait, and only the present
  `REPORT.md` skeleton landed.
- `[INFERRED]` This report is therefore completed directly from the anchored
  local record, following the same fallback pattern already used in earlier
  mission steps when launched role work stalled before its sentinel output.

## Findings Log

### 0. Source hygiene and local-record handling

- `[VERIFIED]` The goal's relative-path block is not directly relative to this
  exploration directory. The usable local step paths resolve under
  `../../../step-*` from here, with library and planning files taken from the
  repository root.
- `[VERIFIED]` `step-008/explorations/exploration-002/REPORT.md` contains a
  stale note claiming the sibling raw-closure report is absent, but
  `step-008/explorations/exploration-001/REPORT.md` is present in the current
  repository and is also cited by `step-008/RESULTS.md`.
- `[INFERRED]` For the inherited-ledger memo, the higher local authority is
  therefore `step-008/RESULTS.md` plus the landed
  `step-008/explorations/exploration-001/REPORT.md`, not the stale absence note
  inside the sibling report.

### 1. The inherited canonical packet ledger is already frozen at packet level

- `[VERIFIED]` The inherited exact object is the canonical one-bridge
  role-labeled helical packet

  ```text
  P_n = (A_n, B_n, C_n, D_n, E_n)
  ```

  with role meanings
  `A_n = active carrier`,
  `B_n = slow clock`,
  `C_n = tiny trigger`,
  `D_n = transfer conduit / rotor leg`,
  `E_n = next carrier = A_{n+1}`.
- `[VERIFIED]` Packet identity stays at the packet level.
  Mandatory conjugate completion is frozen as real-valuedness bookkeeping, not
  as a second primary support notion.
- `[VERIFIED]` The packet-sheet conventions are also already frozen:
  one role order,
  one conjugate-representative convention,
  one helical basis choice,
  one sign sheet,
  one amplitude anchor,
  and one phase anchor.
- `[VERIFIED]` The normalization sheet already frozen on the carried ledger is

  ```text
  |A_n(0)| = 1,
  arg A_n(0) = 0,
  I = [0, 1],
  int_I D_on(t) dt = 1.
  ```

- `[VERIFIED]` The desired Tao-like interaction core already inherited by Step
  9 is

  ```text
  A -> B,
  A -> C,
  B,C -> C,
  C,A <-> D,
  D,D -> E.
  ```

- `[VERIFIED]` The classwise forced-extra categories already earned on disk are
  exactly:
  `mirror`,
  `companion`,
  `feedback`,
  and
  `cross`.
  These are frozen as exact-NS burden classes, not as optional bookkeeping.
- `[INFERRED]` This is the true inherited Step-9 ledger:
  canonical packet semantics,
  role labels,
  mandatory conjugate completion,
  normalization anchors,
  desired core,
  and forced-extra taxonomy.
  None of that needs new proof in this step.

### 2. Witness-local carried data are narrower than canonical packet semantics

- `[VERIFIED]` The old branch carried the **single witness**
  `F_SS(1/12)`,
  not the whole family
  `F_SS(mu)`.
- `[VERIFIED]` The witness-local screening record freezes the sparse-triad
  family support conventions
  of one primary mode per role,
  mandatory conjugates,
  and only closure-forced companions,
  together with the family labels
  `sigma_SS`,
  `phi_SS`,
  the initial tiny-trigger value
  `|C_n(0)| = 1/128`,
  and the classwise desired/spectator totals at
  `mu = 1/12`.
- `[VERIFIED]` The carried sign realization on `sigma_SS` is Tao-ordered:
  `Q_clk`,
  `Q_seed`,
  `Q_amp`,
  and
  `Q_next`
  feed positively,
  while
  `Q_rot^D` feeds `D_n`
  and
  `Q_rot^A` drains `A_n`.
- `[INFERRED]` Step 9 may inherit that as old-branch sign-sheet data, but it is
  still not a newly promoted wavevector/helicity realization for the general
  audited exact-closure object.
- `[VERIFIED]` The witness-local desired-channel totals recorded on disk are

  ```text
  int_I |Q_clk|   = 1/6
  int_I |Q_seed|  = 1/12
  int_I |Q_amp|   = 1/4
  int_I |Q_rot^D| = 1/4
  int_I |Q_rot^A| = 1/12
  int_I |Q_next|  = 1/6
  ```

  and the witness-local classwise spectator totals are

  ```text
  L_tot       = 1/4
  L_mirror    = 1/12
  L_companion = 1/12
  L_feedback  = 1/24
  L_cross     = 1/24.
  ```

- `[INFERRED]` Those data are **not** the same thing as canonical packet
  semantics.
  They belong to the sparse-triad witness branch and its repaired screening
  ledger, not to the full one-bridge class.
- `[INFERRED]` Repaired `G_tmpl` and repaired `G_leak` likewise belong to the
  inherited screening scorecard, not to the packet definition itself.

### 3. Step 8 earned only classwise exact-closure burden, not support-level explicit closure

- `[VERIFIED]` Step 8’s sharp constructive verdict is

  ```text
  exact non-isolability / arbitrary-truncation requirement
  ```

  on the frozen ledger.
- `[VERIFIED]` The local record makes representative exact forced channels
  explicit, including same-scale reciprocal updates such as

  ```text
  (A_n, B_n) -> A_n
  (A_n, C_n) -> C_n
  (B_n, C_n) -> B_n
  (D_n, A_{n+1}) -> D_n
  ```

  and mirror companions such as

  ```text
  (overline{A_n}, overline{A_n}) -> overline{B_n}
  (overline{A_n}, overline{A_n}) -> overline{C_n}
  (overline{B_n}, overline{C_n}) -> overline{C_n}
  (overline{A_n}, overline{C_n}) -> overline{D_n}
  (overline{D_n}, overline{D_n}) -> overline{A_{n+1}}.
  ```

- `[VERIFIED]` But Step 8 also states that the repository still does **not**
  pin:
  one explicit wavevector family,
  one exact helical coefficient ledger,
  or one finite packet-closure convention for the carried witness.
- `[INFERRED]` So the inherited closure information is classwise and
  interaction-level only.
  It does not yet identify one finite exact support list, one reduced ODE, or
  one audited realization protocol that later steps could inherit unchanged.

### 4. Remaining freedoms that Step 9 still has to freeze

- `[VERIFIED]` Step-2 and Step-8 records explicitly leave open:
  one explicit wavevector family for the five roles,
  one fixed helicity assignment / wavevector-level sign ledger,
  one exact coefficient ledger for desired and forced triads,
  and one finite packet-closure convention.
- `[INFERRED]` The carried amplitude and phase anchors are frozen, but the
  remaining amplitude / phase freedoms of any later exact realization are not
  yet exhausted by those anchors.
  Step 9 would still need to say what is fixed, what remains free, and what is
  constrained by conjugation.
- `[INFERRED]` Coefficient-zero or degeneracy subvarieties also remain open.
  The Step-4 adverse family dossier and the run-003 judgment both show that
  degenerate geometry, cancellation, and exceptional algebraic regimes matter,
  but no explicit theorem-facing exceptional-set sheet is yet frozen for the
  audited ledger.

### 5. Strongest local authority path by major item

- `[VERIFIED]` **Canonical one-bridge packet and role labels:**
  `step-007/RESULTS.md:67-83`.
- `[VERIFIED]` **Packet-level support semantics:**
  `library/factual/navier-stokes/support-means-a-role-labeled-helical-packet-with-mandatory-conjugate-completion.md:5-14`.
- `[VERIFIED]` **Mandatory conjugate completion without identity drift:**
  `library/factual/navier-stokes/conjugate-completion-is-mandatory-canonicalization-not-primary-packet-identity.md:5-12`
  plus
  `step-007/RESULTS.md:96-105`.
- `[VERIFIED]` **Frozen sign / amplitude / phase packet-sheet rule:**
  `step-007/RESULTS.md:99-105`
  plus
  `library/factual/navier-stokes/helical-signs-amplitude-normalization-and-phase-anchor-belong-to-the-frozen-packet-sheet.md:5-15`.
- `[VERIFIED]` **Frozen normalization:**
  `step-007/RESULTS.md:106-113`.
- `[VERIFIED]` **Desired Tao-like core:**
  `step-007/RESULTS.md:84-95`.
- `[VERIFIED]` **Forced-extra class taxonomy:**
  `step-002/RESULTS.md:72-76`
  plus
  `library/factual/exact-ns-tao-circuit-near-closure-screening/all-promoted-step-2-candidates-share-the-same-forced-exact-ns-extras-around-the-core.md:5-12`.
- `[VERIFIED]` **Witness-local `F_SS(1/12)` sheet and numeric burden data:**
  `step-007/explorations/exploration-001/REPORT.md:117-155`
  with family origin in
  `step-004/RESULTS.md:265-283`.
- `[VERIFIED]` **Step-8 classwise-only closure verdict and stop:**
  `step-008/RESULTS.md:5-15,151-179`
  plus
  `library/factual/exact-ns-tao-circuit-near-closure-screening/step-8-stops-at-exact-non-isolability-before-step-3-dynamics-on-the-frozen-ledger.md:5-20`.
- `[VERIFIED]` **Still-open Step-9 realization freedoms:**
  `step-002/explorations/exploration-002/REPORT.md:187-197,273-281,369-377`,
  `planning-runs/run-003/judgments/chain-02.md:53-82`,
  and
  `planning-runs/run-003/attacks/chain-01.md:76-89`.

## Dead Ends / Failed Attempts

- `[VERIFIED]` The required receptionist query was attempted by the strategizer
  first and failed at the local Codex runtime layer before producing a usable
  result or search log.
- `[VERIFIED]` The goal's raw relative-path list initially mispointed from this
  exploration directory.
  I corrected the paths against the actual `steps/` layout rather than treating
  those misses as substantive evidence.
- `[VERIFIED]` The Step-8 report packet contains a stale internal inconsistency
  about whether the raw closure report landed.
  I resolved that by privileging the current landed files and
  `step-008/RESULTS.md`, not by speculating about historical absence.
- `[VERIFIED]` I searched the repository for explicit sign-sheet assignments or
  wavevector tuples using `rg` around
  `sigma_SS`,
  `phi_SS`,
  `wavevector`,
  `k_A`,
  `k_B`,
  `k_C`,
  `k_D`,
  `k_E`,
  and
  `exact coefficient ledger`.
  I found symbolic sign-sheet references for `sigma_BM` and `sigma_DT`, but no
  explicit `sigma_SS` / `phi_SS` role tuple and no carried-witness wavevector
  realization.

## Outcome

- `[INFERRED]` Exploration succeeded.
  The inherited fixed ledger is sharp enough to freeze what Step 9 may reuse
  without new proof.
- `[INFERRED]` The same exploration also makes the open-freedom boundary
  explicit:
  Step 9 still lacks an explicit wavevector/helicity realization, a promoted
  exact coefficient ledger, explicit exceptional-set tracking, and a finite
  closure convention.
- `[INFERRED]` So this exploration supports the Step-9 split cleanly:
  the next question is no longer "what is inherited?"
  It is whether any honest audited realization-and-provenance packet actually
  exists on disk.
