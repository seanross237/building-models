# Exploration 003 Report

## Goal

Write the endpoint-exchange memo, prior-art packet, and Step-2 verdict for the
two active exact-rewrite candidates.

## Method

- Reuse the frozen ledger from `step-013`.
- Reuse the active slate from exploration 001.
- Reuse the exact/localized equation packets from exploration 002.
- Compare each candidate against the repository's prior exact-rewrite record
  and the chain's same-currency exchange rule.

## Operational Note

- [VERIFIED] The wrapper-launched explorer session again failed to land a
  sentinel during a bounded wait.
- [VERIFIED] The strategizer completed the report directly from the same local
  sources and the new equation packets already written in this step.

## Source Log

- `missions/beyond-de-giorgi/steps/step-013/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-014/explorations/exploration-001/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-014/explorations/exploration-002/REPORT.md`
- `missions/beyond-de-giorgi/library-inbox/step-006-exploration-001-tao-screen-divergence-lamb.md`
- `missions/beyond-de-giorgi/library-inbox/step-006-exploration-002-tao-screen-vorticity-biot-savart.md`
- `missions/beyond-de-giorgi/library-inbox/step-006-exploration-003-unified-tao-verdict.md`
- `library/factual/exact-rewrite-obstruction-audit/lamb-vector-projected-form-is-tao-insufficient-once-localization-debt-returns.md`
- `library/factual/exact-rewrite-obstruction-audit/vorticity-biot-savart-form-is-tao-insufficient-on-the-fixed-lei-ledger.md`
- `library/factual/exact-rewrite-obstruction-audit/the-exact-rewrite-branch-should-stop-before-a-cosmetic-step-3.md`
- `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`
- `missions/beyond-de-giorgi/planning-runs/run-009/winning-chain.md`
- `missions/beyond-de-giorgi/planning-runs/run-009/selected/chain-01.md`
- `missions/beyond-de-giorgi/MISSION.md`

## Findings

### 1. Candidate: `Lamb-vector / Helmholtz-projected form`

#### Endpoint-exchange memo

- [INFERRED] Native-variable attraction:
  exact decomposition of convection into
  `∇(|u|^2/2) - u × ω`,
  with the Lamb-vector part orthogonal to `u` and exact Beltrami cancellation
  as the anchor case.
- [INFERRED] Same-currency cash-out requirement:
  to survive this branch, that native-variable structure would have to imply a
  smaller effective coefficient on the same full localized LEI bundle
  `I_flux[phi] = ∬ (|u|^2 + 2p) u · ∇phi`
  after pressure, projection, and cutoff debt.
- [INFERRED] Required transfer lemma:
  a theorem-level estimate converting control of the projected Lamb-vector or
  localized Beltrami deficit into a positive-margin reduction of the full
  `I_flux[phi]` coefficient in the inherited LEI package.
- [VERIFIED] Visible losses before promotion:
  pressure re-entry is immediate through
  `p + |u|^2/2`,
  projection is nonlocal,
  and localization creates commutator debt.
- [INFERRED] Exchange-path verdict:
  `absent`.
  The local record gives no source-backed transfer lemma from Lamb-vector-side
  cancellation to the frozen theorem-facing burden currency.

#### Nearest-prior-art packet

- [VERIFIED] Nearest comparator on the repository record:
  the existing exact Lamb-vector / projected-form packet already audited in
  Step 006 and the mission-level Beltrami remarks in `MISSION.md`.
- [VERIFIED] Shared exact structure:
  the same decomposition
  `(u · ∇)u = ∇(|u|^2/2) - u × ω`
  and the same favorable Beltrami anchor.
- [INFERRED] Exact claimed mathematical delta needed for survival now:
  not just the decomposition itself, but a localized same-currency gain on the
  full LEI cutoff-flux bundle after the gradient piece is repaid.
- [VERIFIED] Current packet does not exhibit that delta.
- [INFERRED] Prior-art status:
  `recycled`.
  On the repository record, this remains the same exact identity plus the same
  fragile anchor case, with no new theorem-facing cash-out.

### 2. Candidate: `vorticity transport / Biot-Savart form`

#### Endpoint-exchange memo

- [INFERRED] Native-variable attraction:
  the quadratic interaction is relocated to the exact vorticity transport /
  stretching system, with velocity recovered from `ω` by Biot-Savart.
- [INFERRED] Same-currency cash-out requirement:
  this package would have to imply a smaller effective coefficient on the same
  full localized LEI bundle after every Biot-Savart, pressure-recovery, and
  cutoff-commutator cost is charged.
- [INFERRED] Required transfer lemma:
  a localized estimate proving that rewriting one or more velocity factors
  through `ω` and reconstructing pressure still yields positive-margin
  coefficient shrinkage on the full `I_flux[phi]` term.
- [VERIFIED] Visible losses before promotion:
  full nonlocal velocity reconstruction,
  nonlocal pressure reconstruction,
  cutoff commutators,
  and admissibility debt all appear before any same-currency gain is named.
- [INFERRED] Exchange-path verdict:
  `absent`.
  The record explicitly says the only honest move is formal substitution inside
  the same `I_flux[phi]` estimate, after which the same nonlocal cost is
  repaid.

#### Nearest-prior-art packet

- [VERIFIED] Nearest comparator on the repository record:
  the vorticity-form mission background and the Step-006
  `vorticity / Biot-Savart` Tao-screen packet.
- [VERIFIED] Shared exact structure:
  exact vorticity transport with Biot-Savart reconstruction of velocity and
  the already known warning that moving to `ω` does not by itself beat the
  quadratic obstruction.
- [INFERRED] Exact claimed mathematical delta needed for survival now:
  a theorem-facing same-ledger gain on `I_flux[phi]`, not merely a vorticity
  representation of the same interaction.
- [VERIFIED] Current packet does not exhibit that delta.
- [INFERRED] Prior-art status:
  `recycled`.
  On the local record, the route remains a representation-level restatement
  unless it produces the missing same-currency exchange, which it does not.

### 3. Reserve memo: `divergence / stress form`

- [INFERRED] The reserve route would need an even simpler transfer lemma:
  integration by parts in stress form would have to lower the same transport
  coefficient instead of recreating the same stress-against-`∇phi` burden.
- [VERIFIED] The Step-006 record already says that does not happen.
- [INFERRED] So the reserve cannot rescue the slate once both active exchange
  paths are absent.

### 4. Step-level verdict

- [VERIFIED] The chain's own Step-2 kill condition is already explicit:
  stop if every candidate is either a recycled prior-art package, only an
  identity-level rewrite, or has no credible exchange path back to the frozen
  burden currency.
- [INFERRED] That condition is met here.
  Both active candidates fail first on endpoint exchange:
  neither produces a credible same-currency route from its native-variable
  structure back to a smaller coefficient on the full localized LEI bundle
  after visible debt.
- [INFERRED] Prior-art overlap strengthens the negative verdict, but the first
  live failure is exchange failure rather than the formal Step-3
  anti-repackaging classification.

## Exchange And Prior-Art Table

| candidate | required cash-out into frozen currency | required transfer lemma | visible losses before promotion | nearest local comparator | prior-art delta status | Step-2 standing |
| --- | --- | --- | --- | --- | --- | --- |
| `Lamb-vector / projected` | `[INFERRED]` smaller effective coefficient on full `I_flux[phi]` after pressure/projection debt | `[INFERRED]` convert Lamb-vector or Beltrami-deficit control into same-ledger coefficient shrinkage | `[VERIFIED]` pressure re-entry, projector nonlocality, cutoff commutators, admissibility | `step-006-exploration-001-tao-screen-divergence-lamb` plus `MISSION.md` Beltrami note | `[INFERRED]` no new mathematical delta beyond the same identity and anchor case | `exchange path absent; recycled risk already high` |
| `vorticity / Biot-Savart` | `[INFERRED]` smaller effective coefficient on full `I_flux[phi]` after BS and pressure reconstruction | `[INFERRED]` localized estimate turning vorticity-side substitution into same-ledger coefficient shrinkage | `[VERIFIED]` Biot-Savart debt, pressure reconstruction, cutoff commutators, admissibility, locality loss | `step-006-exploration-002-tao-screen-vorticity-biot-savart` plus `MISSION.md` vorticity note | `[INFERRED]` no new mathematical delta beyond the same representation change | `exchange path absent; recycled risk already high` |

## Conclusion

- Outcome: `succeeded`
- [VERDICT]
  `exchange-failure obstruction, branch should stop before anti-repackaging gate`
- [INFERRED] Step-3 continuation is not earned.
- [INFERRED] The honest bounded negative result is:
  the active exact-rewrite pair never reaches a smaller same-currency LEI
  coefficient once visible debt is charged, and the reserve is weaker still.
