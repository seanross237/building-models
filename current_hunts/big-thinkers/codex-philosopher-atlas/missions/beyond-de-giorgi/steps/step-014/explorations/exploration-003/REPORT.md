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

### 1. Fixed Step-2 rule for both active candidates

- [VERIFIED] The frozen theorem-facing burden is the full localized LEI
  cutoff-flux bundle
  `I_flux[phi] = ∬ (|u|^2 + 2p) u · ∇phi`
  under one shared CKN-style cutoff protocol on the suitable-weak / LEI floor.
- [VERIFIED] The only admissible gain currency is positive-margin shrinkage of
  the effective coefficient on that same full bundle after pressure recovery,
  projection, Calderon-Zygmund, Biot-Savart, commutator, and admissibility
  debt.
- [VERIFIED] If a candidate's apparent gain is not already stated in that
  currency, Step 2 requires an explicit transfer lemma back to that currency.
- [INFERRED] So the Step-2 question is not whether the candidate has a cleaner
  exact identity. It is whether the candidate can exchange its native-variable
  feature back into a smaller same-ledger coefficient on full localized
  `I_flux[phi]`.

### 2. Candidate packet: `Lamb-vector / Helmholtz-projected form`

#### Endpoint-exchange memo

- [INFERRED] Native-variable gain, if real:
  exact decomposition of convection into
  `(u · ∇)u = ∇(|u|^2/2) - u × ω`,
  with `u · (u × ω) = 0` and exact Beltrami cancellation as the favorable
  anchor case.
- [INFERRED] How that gain would have to cash out in the frozen currency:
  after localization, it would have to reduce the effective coefficient on the
  full localized bundle
  `((|u|^2 / 2) + p) u · ∇phi`,
  hence on the normalized full `I_flux[phi]`, not merely isolate the gradient
  algebraically.
- [INFERRED] Transfer lemma required if the gain is not already in that
  currency:
  a theorem-level localized estimate sending projected-Lamb control or a
  localized Beltrami-deficit bound to a positive-margin reduction of the full
  `I_flux[phi]` coefficient after pressure/projection debt.
- [VERIFIED] Visible losses already present before promotion:
  pressure re-entry is immediate through
  `π = p + |u|^2 / 2`;
  Helmholtz projection is nonlocal;
  localization creates projection/cutoff commutators;
  admissibility remains distributional rather than pointwise in the fixed
  suitable-weak / LEI class.
- [INFERRED] Exchange memo verdict:
  no source-backed same-currency cash-out is on the repository record, and no
  transfer lemma of the required form is presently named.

#### Nearest-prior-art packet

- [VERIFIED] Nearest prior-art comparator on the repository record:
  the mission-level Lamb/Beltrami packet in `MISSION.md`, sharpened by the
  Step-006 Tao-screen memo for `Lamb-vector / Helmholtz-projected form`.
- [VERIFIED] Exact shared structure:
  the same exact Lamb decomposition
  `(u · ∇)u = ∇(|u|^2/2) - u × ω`,
  the same projected form
  `P((u · ∇)u) = -P(u × ω)`,
  and the same Beltrami anchor where the Lamb term vanishes exactly.
- [INFERRED] Exact claimed mathematical delta at this Step-2 interface:
  not the identity itself, but a localized theorem-facing gain showing that
  the projected/Lamb formulation lowers the effective coefficient on the full
  frozen LEI bundle after debt.
- [VERIFIED] Current record does not exhibit that delta.
- [INFERRED] Appearance before formal Step-3 classification:
  `recycled`.
  The candidate still looks like the same exact identity plus the same fragile
  anchor case, without a new exchange into the frozen ledger.
- [INFERRED] Step-3 readiness statement:
  continuation into Step 3 is not earned on this packet.

### 3. Candidate packet: `vorticity transport / Biot-Savart form`

#### Endpoint-exchange memo

- [INFERRED] Native-variable gain, if real:
  relocate the quadratic interaction to exact vorticity transport / stretching
  with velocity recovered from `ω` by Biot-Savart.
- [INFERRED] How that gain would have to cash out in the frozen currency:
  after rewriting velocity-side factors through `ω`, then reconstructing both
  velocity and pressure, the route would still have to leave a smaller
  effective coefficient on the same full localized `I_flux[phi]` bundle.
- [INFERRED] Transfer lemma required if the gain is not already in that
  currency:
  a localized estimate proving that Biot-Savart substitution plus pressure
  reconstruction implies positive-margin coefficient shrinkage on full
  `I_flux[phi]`, not merely a vorticity-side surrogate improvement.
- [VERIFIED] Visible losses already present before promotion:
  full nonlocal velocity reconstruction through Biot-Savart;
  nonlocal pressure reconstruction by Riesz-transform package;
  cutoff commutators because `phi` does not commute with those operators;
  admissibility debt in the fixed suitable-weak / LEI class;
  and locality loss because the native equation does not touch the theorem
  burden until after full reconstruction.
- [INFERRED] Exchange memo verdict:
  the only source-backed move is formal substitution inside the unchanged
  `I_flux[phi]` estimate, after which the same nonlocal debt is repaid.
  No same-currency cash-out or required transfer lemma is on disk.

#### Nearest-prior-art packet

- [VERIFIED] Nearest prior-art comparator on the repository record:
  the mission-level vorticity-formulation note in `MISSION.md`, sharpened by
  the Step-006 Tao-screen memo for `vorticity transport / Biot-Savart form`.
- [VERIFIED] Exact shared structure:
  the same exact vorticity transport equation with velocity reconstructed from
  `ω`, together with the already-recorded warning that moving to `ω` does not
  remove the quadratic obstruction or beat the `beta = 4/3` barrier by itself.
- [INFERRED] Exact claimed mathematical delta at this Step-2 interface:
  not the vorticity representation itself, but a theorem-facing gain showing
  that this representation shrinks the effective coefficient on the same full
  localized LEI bundle after Biot-Savart, pressure, and commutator debt.
- [VERIFIED] Current record does not exhibit that delta.
- [INFERRED] Appearance before formal Step-3 classification:
  `recycled`.
  On the repository record this is still a representation-level relocation of
  the same interaction, not a new same-ledger estimate.
- [INFERRED] Step-3 readiness statement:
  continuation into Step 3 is not earned on this packet.

### 4. Reserve memo: `divergence / stress form`

- [INFERRED] The reserve route would need the simplest exchange memo of all:
  integration by parts in conservative form would have to lower the same
  transport-side coefficient instead of recreating the same stress-against-
  `∇phi` burden.
- [VERIFIED] The Step-006 record already says that does not happen.
- [INFERRED] So the reserve does not rescue the branch once both active
  candidates fail to produce same-currency exchange.

### 5. Step-level recommendation

- [VERIFIED] The chain's Step-2 kill condition is explicit:
  stop if every candidate is either a recycled prior-art package, only an
  identity-level rewrite, or has no credible exchange path back to the frozen
  burden currency.
- [INFERRED] That condition is met on the current repository-local record.
  Both active candidates look recycled, but more importantly both fail the
  Step-2 exchange burden first:
  neither names a credible same-currency route from its native-variable gain
  to a smaller effective coefficient on the full localized LEI bundle after
  visible debt.
- [INFERRED] Because the stop signal is already triggered at exchange, the
  branch should not be advanced into the formal Step-3 anti-repackaging gate.

## Exchange And Prior-Art Table

| candidate | native-variable gain would have to cash out as | required transfer lemma | visible losses before promotion | nearest local comparator | exact shared structure | exact claimed mathematical delta | appearance before Step 3 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Lamb-vector / projected` | `[INFERRED]` smaller effective coefficient on full localized `I_flux[phi]` after pressure/projection debt | `[INFERRED]` convert projected-Lamb or Beltrami-deficit control into same-ledger coefficient shrinkage on full `I_flux[phi]` | `[VERIFIED]` pressure re-entry, projector nonlocality, cutoff commutators, admissibility debt | `MISSION.md` Lamb/Beltrami packet, sharpened by Step-006 Lamb Tao screen | `[VERIFIED]` same Lamb decomposition, same projected form, same exact Beltrami anchor | `[INFERRED]` a localized theorem-facing coefficient reduction on full `I_flux[phi]` after debt | `recycled` |
| `vorticity / Biot-Savart` | `[INFERRED]` smaller effective coefficient on full localized `I_flux[phi]` after Biot-Savart and pressure reconstruction | `[INFERRED]` prove vorticity-side substitution plus reconstruction yields same-ledger coefficient shrinkage on full `I_flux[phi]` | `[VERIFIED]` Biot-Savart debt, pressure reconstruction, cutoff commutators, admissibility debt, locality loss | `MISSION.md` vorticity-formulation packet, sharpened by Step-006 vorticity Tao screen | `[VERIFIED]` same exact vorticity transport plus velocity reconstruction from `ω` | `[INFERRED]` a localized theorem-facing coefficient reduction on full `I_flux[phi]` after reconstruction debt | `recycled` |

## Failed Attempts / Dead Ends

- [VERIFIED] I found no repository-local transfer lemma converting projected
  Lamb structure, Beltrami deficit, or vorticity-side substitution into a
  smaller effective coefficient on full localized `I_flux[phi]`.
- [VERIFIED] I found no local source naming a new mathematical delta beyond
  the already recorded exact identities and anchor cases for either active
  candidate.
- [INFERRED] Because the exchange packet is already missing, running the formal
  Step-3 anti-repackaging classifier here would outrun the Step-2 record.

## Conclusion

- Outcome: `succeeded`
- [VERDICT]
  `exchange-failure obstruction, branch should stop before anti-repackaging gate`
- [INFERRED] Step-3 continuation is not earned.
- [INFERRED] The honest bounded negative result is:
  the active exact-rewrite pair never reaches a smaller same-currency LEI
  coefficient once visible debt is charged, and the reserve is weaker still.
