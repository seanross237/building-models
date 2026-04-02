# Step 006 Results

## Completion Status

- Kill condition fired: **yes**
- Kill condition reason:
  no frozen candidate has a concrete NS-versus-averaged discriminator that
  produces a smaller effective coefficient on the fixed bad term
  `I_flux[φ] = ∬_{Q_r} (|u|^2 + 2p) u · ∇φ`.
- Step status: **complete**

## 1. Candidate-By-Candidate Tao-Screen Memo

### Candidate: `divergence / stress form`

- Claimed NS-specific feature:
  [INFERRED] use incompressibility to rewrite
  `(u · ∇)u = ∇ · (u ⊗ u)`,
  so the quadratic interaction is packaged as stress divergence and the
  derivative can be moved onto the cutoff.
- Tao-screen verdict:
  [INFERRED] `preserved`, but only as identity-level packaging.
  Tao-style averaging preserves this level of divergence-free algebra; the
  local record does not identify any additional estimate-level feature that the
  averaged setting would destroy.
- Exact place where it could matter:
  [INFERRED] only in the transport-side portion of the fixed LEI cutoff-flux
  bundle, by trying to lower the coefficient after integrating by parts
  against `∇φ`.
  The same stress-against-`∇φ` burden returns, so no credible gain is created.
- Step-2 verdict:
  [INFERRED] `reject as Tao-insufficient`

Sources:
- `missions/beyond-de-giorgi/steps/step-005/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-005/explorations/exploration-003/REPORT.md`
- `library/factual/exact-rewrite-architecture-screening/the-localized-lei-cutoff-flux-bundle-is-the-fixed-bad-term-for-the-audit.md`
- `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`
- `library/factual/far-field-pressure-obstruction/algebraic-rewrites-and-local-geometry-fail-the-tao-gate.md`
- `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`

### Candidate: `Lamb-vector / Helmholtz-projected form`

- Claimed NS-specific feature:
  [INFERRED] isolate the gradient part in
  `(u · ∇)u = ∇(|u|^2/2) - u × ω`,
  then use Helmholtz projection to expose the Lamb-vector side of the
  nonlinearity; exact Beltrami alignment is the favorable anchor case.
- Tao-screen verdict:
  [INFERRED] `weakens`.
  The exact gradient/Lamb decomposition survives algebraically, but its
  supposed leverage is washed out once localization restores projection,
  pressure, Calderon-Zygmund, and commutator debt.
- Exact place where it could matter:
  [INFERRED] only if the projected Lamb-vector form lowered the same
  cutoff-flux coefficient inside `I_flux[φ]`.
  No such coefficient improvement is supported locally; the gradient piece
  simply reappears inside pressure/projection bookkeeping.
- Step-2 verdict:
  [INFERRED] `reject as Tao-insufficient`

Sources:
- `missions/beyond-de-giorgi/MISSION.md`
- `missions/beyond-de-giorgi/steps/step-005/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-005/explorations/exploration-003/REPORT.md`
- `library/factual/exact-rewrite-obstruction-audit/projected-and-vorticity-rewrites-must-pay-localization-debt.md`
- `library/factual/exact-rewrite-architecture-screening/the-localized-lei-cutoff-flux-bundle-is-the-fixed-bad-term-for-the-audit.md`
- `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`
- `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`

### Candidate: `vorticity transport / Biot-Savart form`

- Claimed NS-specific feature:
  [INFERRED] relocate the same quadratic interaction to the vorticity side and
  recover `u` from `ω` by Biot-Savart, so the nonlinearity is expressed in a
  more explicitly Navier-Stokes-looking vorticity language.
- Tao-screen verdict:
  [INFERRED] `preserved`, but only as a representation-level restatement.
  The local record does not identify a separate estimate-level feature that
  Tao-style averaging would destroy here; the same nonlocal debt is repaid once
  Biot-Savart reinsertion is charged honestly.
- Exact place where it could matter:
  [INFERRED] only by rewriting factors inside the same `I_flux[φ]` estimate and
  hoping the effective coefficient shrinks.
  The fixed protocol instead records the opposite: Biot-Savart reinsertion and
  cutoff commutation repay the same nonlocal cost.
- Step-2 verdict:
  [INFERRED] `reject as Tao-insufficient`

Sources:
- `missions/beyond-de-giorgi/MISSION.md`
- `missions/beyond-de-giorgi/steps/step-005/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-005/explorations/exploration-003/REPORT.md`
- `library/factual/exact-rewrite-obstruction-audit/projected-and-vorticity-rewrites-must-pay-localization-debt.md`
- `library/factual/exact-rewrite-obstruction-audit/every-rewrite-must-stay-inside-the-same-localized-lei-package.md`
- `library/factual/exact-rewrite-architecture-screening/the-localized-lei-cutoff-flux-bundle-is-the-fixed-bad-term-for-the-audit.md`
- `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`
- `runtime/results/codex-patlas-standalone-20260331T130634Z-receptionist-94037.md`

## 2. Localized Insertion-Point Note

- [VERIFIED] The fixed insertion target for every candidate is the localized
  LEI cutoff-flux bundle
  `I_flux[φ] = ∬_{Q_r} (|u|^2 + 2p) u · ∇φ`.
- [INFERRED] No candidate earns a more specific estimate-level insertion point
  before Step 3:
  - `divergence / stress` returns the same stress-against-`∇φ` burden
  - `Lamb-vector / projected` returns the same pressure / projection /
    commutator ledger
  - `vorticity / Biot-Savart` returns the same nonlocal reinsertion debt
- [INFERRED] Therefore every discrimination attempt in this step collapses at
  the static rewrite level rather than altering the fixed localized balance.

Sources:
- `library/factual/exact-rewrite-architecture-screening/the-localized-lei-cutoff-flux-bundle-is-the-fixed-bad-term-for-the-audit.md`
- `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`
- `library/factual/exact-rewrite-obstruction-audit/projected-and-vorticity-rewrites-must-pay-localization-debt.md`
- `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`

## 3. Admission / Rejection Table

| Candidate | Classification | One-line reason tied to the frozen branch |
| --- | --- | --- |
| `divergence / stress form` | `reject as Tao-insufficient` | The divergence rewrite only repackages the transport term; after IBP it leaves the same cutoff-flux burden on `∇φ`. |
| `Lamb-vector / Helmholtz-projected form` | `reject as Tao-insufficient` | The attractive projected/Lamb decomposition does not shrink the same LEI coefficient once localization restores pressure / CZ / commutator debt. |
| `vorticity transport / Biot-Savart form` | `reject as Tao-insufficient` | Rewriting through `ω` does not identify a smaller coefficient on `I_flux[φ]`; Biot-Savart reinsertion repays the same nonlocal cost. |

## 4. Branch Verdict Memo

- [INFERRED] The branch is **dead after the Tao screen**.
- [INFERRED] Survivors admitted to Step 3:
  none.
- [INFERRED] Step-3 estimate question:
  none should be opened for this branch, because the candidate family has
  already failed the prerequisite Tao discriminator.
- [INFERRED] Recommendation:
  invalidate the fixed-protocol exact-rewrite audit now rather than continue to
  a cosmetic Step 3 loss ledger.

## 5. Prior-Art Calibration Note

- [VERIFIED] Relative to the De Giorgi sharpness record:
  this step did **not** retest `beta = 4/3` or the `W^{1,3}` wall.
  It asked the narrower question whether exact reformulations of the same
  quadratic interaction improve one frozen localized LEI cutoff-flux
  coefficient before any architecture change.
- [VERIFIED] Relative to the pressure-route negatives:
  this step did **not** revisit the far-field harmonic-tail coefficient or the
  H^1 pressure route.
  It instead tested whether standard algebraic rewrites survive Tao screening
  inside the fixed local-energy flux architecture.
- [VERIFIED] Relative to the killed geometry branch:
  this step did **not** evaluate tube persistence, direction coherence, or full
  stretching control.
  It explicitly rejected any attempt to rescue the rewrite family by drifting
  back into stretching/geometry language.
- [INFERRED] So the new result earned here is a bounded obstruction memo:
  within one frozen localized LEI protocol, the standard exact-rewrite family
  does not provide a Tao-sensitive estimate lever on `I_flux[φ]`.

Sources:
- `missions/vasseur-pressure/steps/step-001/RESULTS.md`
- `missions/vasseur-pressure/steps/step-002/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-001/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-002/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-004/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-005/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-006/explorations/exploration-003/REPORT.md`
