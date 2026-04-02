# Step 014 Results

## Completion Status

- Kill condition fired: **yes**
- Step outcome:
  `exchange-failure obstruction, branch should stop before anti-repackaging gate`
- Operational note:
  the receptionist wrapper was run but did not produce a result file during the
  bounded wait.
  All three explorer sessions were launched through the required wrapper, but
  none landed its sentinel during the bounded waits, so the strategizer
  completed the reports directly from the same repository-local evidence.
  The curator handoffs were launched for all three completed reports;
  the receipt for exploration 001 landed during this step window, while the
  receipts for explorations 002 and 003 were still pending at closeout.

## 1. Candidate-Slate Sheet

| slot | candidate family | why included or not promoted | status |
| --- | --- | --- | --- |
| active | `Lamb-vector / Helmholtz-projected form` | `[INFERRED]` This is the sharpest exact-rewrite-native candidate on disk: it isolates `∇(|u|^2/2)` from `u × ω`, names exact Beltrami cancellation as the favorable anchor, and gives a direct, testable route back to the frozen `I_flux[phi]` currency. | active |
| active | `vorticity transport / Biot-Savart form` | `[INFERRED]` This is the only other exact-rewrite-native family on disk with a nontrivial theorem-facing story: it relocates the same quadratic interaction to the vorticity side and makes reconstruction debt explicit. | active |
| reserve | `divergence / stress form` | `[INFERRED]` Exact and admissible, but weaker than the active pair because it localizes almost immediately back to the same stress-against-`∇phi` burden with no sharper candidate-specific structure. | reserve |
| omitted now | `strain / pressure-Hessian` and related tensor packages | `[VERIFIED]` These appear elsewhere in the repository, but as pressure-branch or geometry-adjacent materials rather than the frozen exact-rewrite shortlist for this branch. | not promoted |

## 2. Exact-Equation Packets For The Active Candidates

### Active candidate A: `Lamb-vector / Helmholtz-projected form`

- Exact package:
  `[INFERRED]` `ω = curl u`,
  `(u · ∇)u = ∇(|u|^2/2) - u × ω`.
- Full exact evolution:
  `[INFERRED]` `∂_t u - Δu - u × ω + ∇(p + |u|^2/2) = 0`,
  `div u = 0`.
- Projected form:
  `[INFERRED]` `∂_t u - Δu - P(u × ω) = 0`.
- Exact-NS structure:
  `[INFERRED]` exact gradient/Lamb split and pointwise orthogonality
  `u · (u × ω) = 0`.
- Generic packaging:
  `[INFERRED]` Helmholtz projection and the reconstitution of the gradient part
  into pressure bookkeeping are nonlocal operator packaging, not a new theorem
  mechanism.
- Pressure re-entry or reconstruction already visible:
  `[VERIFIED]` the gradient term survives as `p + |u|^2/2`.

### Active candidate B: `vorticity transport / Biot-Savart form`

- Exact package:
  `[INFERRED]` `ω = curl u`, `u = ∇ × (-Δ)^(-1)ω`.
- Full exact evolution:
  `[INFERRED]`
  `∂_t ω - Δω + (u · ∇)ω - (ω · ∇)u = 0`,
  equivalently
  `∂_t ω - Δω + (u · ∇)ω = Sω`.
- Exact-NS structure:
  `[INFERRED]` transport, stretching, and incompressible reconstruction all sit
  in one exact `(ω,u)` package.
- Generic packaging:
  `[INFERRED]` every return from `ω` to `u`, `∇u`, or `p` is via Biot-Savart /
  Calderon-Zygmund reconstruction.
- Pressure re-entry or reconstruction already visible:
  `[VERIFIED]` pressure remains quadratic in the reconstructed velocity and
  therefore re-enters by nonlocal Riesz-transform structure.

## 3. Localized-Equation And Debt-Ledger Packets

### Active candidate A: `Lamb-vector / Helmholtz-projected form`

- Localized form relevant to the frozen burden:
  `[INFERRED]` testing the exact equation against `u phi` kills the raw
  `u × ω` term pointwise, but
  `∇(p + |u|^2/2) · (u phi) = -((|u|^2/2) + p) u · ∇phi`,
  so the same localized LEI cutoff-flux bundle returns.
- Cutoff commutators:
  `[VERIFIED]` localization after projection creates projection/cutoff
  commutator debt in the candidate's own ledger.
- Pressure re-entry:
  `[VERIFIED]` immediate through `p + |u|^2/2`.
- Vector reconstruction debt:
  `[INFERRED]` the package depends on `ω = curl u` and on the nonlocal
  projector `P`.
- Admissibility debt:
  `[INFERRED]` the projected identity is not a free pointwise replacement in
  the suitable-weak / LEI class; it must be justified distributionally.
- Locality loss:
  `[INFERRED]` the clean global decomposition becomes nonlocal once `phi` is
  inserted.
- Full burden or surrogate:
  `[INFERRED]` full burden, but only by restoring the same bundle rather than
  lowering it.

### Active candidate B: `vorticity transport / Biot-Savart form`

- Localized form relevant to the frozen burden:
  `[INFERRED]` the native vorticity equation does not itself produce
  `I_flux[phi]`; to touch the theorem-facing target one must rewrite
  `u = BS[ω]` and `p = R_i R_j(u_i u_j)` inside the same localized LEI bundle.
- Cutoff commutators:
  `[VERIFIED]` `phi` does not commute with Biot-Savart or pressure
  reconstruction, so interior/exterior and commutator debt appears
  immediately.
- Pressure re-entry:
  `[VERIFIED]` through the same quadratic pressure reconstruction after `u` is
  recovered from `ω`.
- Vector reconstruction debt:
  `[VERIFIED]` every velocity-side factor in `I_flux[phi]` must be rebuilt from
  `ω`.
- Admissibility debt:
  `[INFERRED]` the suitable-weak / LEI floor does not provide a separate
  vorticity-side closure that could replace the inherited local-energy package.
- Locality loss:
  `[INFERRED]` the route is intrinsically nonlocal once one insists on acting
  on the full `I_flux[phi]` object.
- Full burden or surrogate:
  `[INFERRED]` the native equation acts on a surrogate object until full
  reconstruction is paid; only then does it speak the full frozen burden.

## 4. Endpoint-Exchange Memos

### Active candidate A: `Lamb-vector / Helmholtz-projected form`

- Native-variable gain that would have to cash out:
  `[INFERRED]` localized Lamb-vector cancellation or Beltrami-deficit control.
- Required transfer lemma:
  `[INFERRED]` one same-protocol estimate converting that native-variable
  control into a positive-margin reduction of the full `I_flux[phi]`
  coefficient after pressure, projection, and cutoff debt.
- Visible losses before promotion:
  `[VERIFIED]` pressure re-entry, nonlocal projection, cutoff commutators,
  admissibility debt.
- Exchange-path verdict:
  `[INFERRED]` absent.

### Active candidate B: `vorticity transport / Biot-Savart form`

- Native-variable gain that would have to cash out:
  `[INFERRED]` vorticity-side relocation of the quadratic interaction together
  with any hoped-for vorticity-side structure.
- Required transfer lemma:
  `[INFERRED]` one localized estimate proving that Biot-Savart substitution and
  pressure reconstruction still leave a smaller full `I_flux[phi]` coefficient
  after full debt.
- Visible losses before promotion:
  `[VERIFIED]` Biot-Savart reconstruction, pressure reconstruction, cutoff
  commutators, admissibility debt, locality loss.
- Exchange-path verdict:
  `[INFERRED]` absent.

## 5. Nearest-Prior-Art Packets

### Active candidate A: `Lamb-vector / Helmholtz-projected form`

- Nearest comparator on the repository record:
  `[VERIFIED]`
  `missions/beyond-de-giorgi/library-inbox/step-006-exploration-001-tao-screen-divergence-lamb.md`
  together with the Beltrami remarks in `missions/beyond-de-giorgi/MISSION.md`.
- Shared exact structure:
  `[VERIFIED]` the same decomposition
  `(u · ∇)u = ∇(|u|^2/2) - u × ω`
  and the same exact Beltrami anchor.
- Exact claimed mathematical delta that would be needed now:
  `[INFERRED]` a localized same-currency gain on the full LEI cutoff-flux
  bundle after the gradient part is repaid.
- Prior-art verdict:
  `[INFERRED]` recycled.
  The current packet adds no new theorem-facing mathematical delta beyond the
  same identity and fragile anchor case.

### Active candidate B: `vorticity transport / Biot-Savart form`

- Nearest comparator on the repository record:
  `[VERIFIED]`
  `missions/beyond-de-giorgi/library-inbox/step-006-exploration-002-tao-screen-vorticity-biot-savart.md`
  together with the vorticity-form remarks in `missions/beyond-de-giorgi/MISSION.md`.
- Shared exact structure:
  `[VERIFIED]` exact vorticity transport with Biot-Savart reconstruction and
  the already recorded warning that moving to `ω` does not remove the
  quadratic obstruction.
- Exact claimed mathematical delta that would be needed now:
  `[INFERRED]` a same-ledger gain on the full localized `I_flux[phi]` bundle,
  not merely a vorticity-side restatement.
- Prior-art verdict:
  `[INFERRED]` recycled.
  The current packet adds no new theorem-facing mathematical delta beyond the
  same representation change.

## 6. Step Verdict

- `[VERDICT]`
  `exchange-failure obstruction, branch should stop before anti-repackaging gate`
- `[INFERRED]` Reason:
  every active candidate lacks a credible route from its native-variable
  structure back to a smaller effective coefficient on the full frozen
  `I_flux[phi]` bundle once visible debt is charged.
- `[VERIFIED]` This step therefore does **not** earn continuation into the
  formal anti-repackaging screen.
- `[INFERRED]` The reserve `divergence / stress form` is weaker still and does
  not rescue the branch.

## 7. Source Map

### Planning-run evidence

- `missions/beyond-de-giorgi/CHAIN.md`
- `missions/beyond-de-giorgi/planning-runs/run-009/winning-chain.md`
- `missions/beyond-de-giorgi/planning-runs/run-009/selected/chain-01.md`
- `missions/beyond-de-giorgi/controller/decisions/decision-021.md`

### Prior mission evidence

- Candidate-family choice:
  `missions/beyond-de-giorgi/library-inbox/step-005-exploration-003-gain-currency-candidate-family.md`
- Localization and debt rules:
  `missions/beyond-de-giorgi/library-inbox/step-005-exploration-002-compatibility-localization-protocol.md`
- Prior exact-rewrite comparator and negative screen:
  `missions/beyond-de-giorgi/library-inbox/step-006-exploration-001-tao-screen-divergence-lamb.md`
- Prior exact-rewrite comparator and negative screen:
  `missions/beyond-de-giorgi/library-inbox/step-006-exploration-002-tao-screen-vorticity-biot-savart.md`
- Unified prior exact-rewrite verdict:
  `missions/beyond-de-giorgi/library-inbox/step-006-exploration-003-unified-tao-verdict.md`
- Mission-level exact-rewrite context:
  `missions/beyond-de-giorgi/MISSION.md`
- Fixed branch rules:
  `library/factual/exact-rewrite-obstruction-audit/step-1-exact-rewrite-family-is-bounded-to-three-candidates.md`
- Fixed branch rules:
  `library/factual/exact-rewrite-obstruction-audit/projected-and-vorticity-rewrites-must-pay-localization-debt.md`
- Fixed branch rules:
  `library/factual/exact-rewrite-obstruction-audit/every-rewrite-must-stay-inside-the-same-localized-lei-package.md`
- Fixed branch rules:
  `library/factual/exact-rewrite-obstruction-audit/freeze-one-ckn-style-parabolic-cutoff-protocol-for-the-rewrite-audit.md`
- Fixed theorem-facing target:
  `library/factual/exact-rewrite-architecture-screening/the-localized-lei-cutoff-flux-bundle-is-the-fixed-bad-term-for-the-audit.md`
- Fixed success criterion:
  `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`
- Early-stop calibrator:
  `library/factual/exact-rewrite-obstruction-audit/the-exact-rewrite-branch-should-stop-before-a-cosmetic-step-3.md`

### New synthesis created in this step

- `missions/beyond-de-giorgi/steps/step-014/explorations/exploration-001/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-014/explorations/exploration-002/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-014/explorations/exploration-003/REPORT.md`
- `missions/beyond-de-giorgi/library-inbox/step-014-exploration-001-candidate-slate.md`
- `missions/beyond-de-giorgi/library-inbox/step-014-exploration-002-exact-and-localized-equations.md`
- `missions/beyond-de-giorgi/library-inbox/step-014-exploration-003-exchange-prior-art-and-verdict.md`
- `missions/beyond-de-giorgi/meta-inbox/meta-step-014-exploration-001.md`
- `missions/beyond-de-giorgi/meta-inbox/meta-step-014-exploration-002.md`
- `missions/beyond-de-giorgi/meta-inbox/meta-step-014-exploration-003.md`
