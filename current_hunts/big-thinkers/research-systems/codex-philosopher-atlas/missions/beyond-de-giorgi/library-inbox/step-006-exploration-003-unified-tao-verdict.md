# Exploration 003 Report

## Goal

Synthesize the unified Step-2 Tao-screen verdict for the three frozen exact
rewrite candidates in the fixed localized LEI audit:

- `divergence / stress form`
- `Lamb-vector / Helmholtz-projected form`
- `vorticity transport / Biot-Savart form`

## Method

- Read the completed reports for `exploration-001` and `exploration-002`.
- Read the fixed Step-5 branch setup in `missions/beyond-de-giorgi/steps/step-005/RESULTS.md`.
- Read the prior negative calibrators:
  `missions/beyond-de-giorgi/steps/step-001/RESULTS.md`,
  `missions/beyond-de-giorgi/steps/step-002/RESULTS.md`,
  `missions/beyond-de-giorgi/steps/step-004/RESULTS.md`,
  `missions/vasseur-pressure/steps/step-001/RESULTS.md`,
  and `missions/vasseur-pressure/steps/step-002/RESULTS.md`.
- Reapply the branch rule:
  a candidate only survives if it makes an exact term or coefficient smaller in
  the fixed localized balance on `I_flux[phi]`.

## Operational Note

- [VERIFIED] As with the first two explorations, the synthesis explorer was
  launched through the wrapper, but this report was completed directly by the
  strategizer to avoid waiting on another idle session.

## Findings

### 1. Unified Step-2 standard

- [VERIFIED] The branch is frozen to:
  - architecture:
    `local-energy flux/localization`
  - bad term:
    `I_flux[phi] = ∬_{Q_r} (|u|^2 + 2p) u · ∇phi`
  - solution class:
    suitable weak solutions in the Leray-Hopf energy class with LEI
  - gain currency:
    `coefficient shrinkage in the fixed localized LEI balance`
  Sources:
  - `missions/beyond-de-giorgi/steps/step-005/RESULTS.md`
  - `library/factual/exact-rewrite-architecture-screening/the-localized-lei-cutoff-flux-bundle-is-the-fixed-bad-term-for-the-audit.md`
  - `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`
- [VERIFIED] The Tao screen for this step is therefore mechanical rather than
  rhetorical:
  what exact NS-specific feature is claimed, what does Tao-style averaging do
  to that feature, and what coefficient on `I_flux[phi]` becomes smaller?
  Sources:
  - `missions/beyond-de-giorgi/steps/step-006/GOAL.md`
  - `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`

### 2. Candidate-by-candidate verdict table

| Candidate | Claimed NS-specific feature | Tao-screen verdict | Localized insertion point on `I_flux[phi]` | Admission status |
| --- | --- | --- | --- | --- |
| `divergence / stress form` | [INFERRED] incompressible divergence rewriting of convection into stress form | `preserved` only as identity-level packaging | [INFERRED] formal transport-side IBP slot only; same stress-against-`∇phi` burden reappears | `reject as Tao-insufficient` |
| `Lamb-vector / Helmholtz-projected form` | [INFERRED] exact gradient isolation and projected Lamb-vector form, with exact Beltrami as the favorable anchor case | `weakens`; the identity survives but its leverage is washed out once projection / pressure / CZ / commutator debt is restored | [INFERRED] only if the projected Lamb form lowered the same cutoff-flux coefficient; the record gives no such gain | `reject as Tao-insufficient` |
| `vorticity transport / Biot-Savart form` | [INFERRED] vorticity-side relocation of the same quadratic interaction, coupled back by Biot-Savart | `preserved` only as a representation-level restatement inside the fixed audit | [INFERRED] no credible slot beyond formal substitution inside the same `I_flux[phi]` estimate, after which the same nonlocal debt is repaid | `reject as Tao-insufficient` |

### 3. Insertion-point memo

- [INFERRED] For all three candidates, the only honest insertion point before
  Step 3 is a smaller effective coefficient on the same localized LEI
  cutoff-flux bundle.
- [INFERRED] No candidate earns a more specific insertion point:
  - `divergence / stress` returns the same cutoff-stress interaction after IBP
  - `Lamb-vector / projected` returns the same pressure / projection /
    commutator ledger after localization
  - `vorticity / Biot-Savart` returns the same nonlocal debt after reinsertion
- [INFERRED] So every candidate's supposed specialness remains either
  identity-level, verbal, or contingent on leaving the frozen architecture.

### 4. Branch verdict

- [INFERRED] The branch does **not** remain alive after the Tao screen.
- [INFERRED] No candidate survives to Step 3.
- [INFERRED] The kill condition is met in the exact form Step 006 was designed
  to test:
  no frozen candidate has a concrete NS-versus-averaged discriminator tied to
  the fixed bad term `I_flux[phi]`.
- [INFERRED] Therefore the correct Step-2 output is:
  invalidate the branch now rather than opening a cosmetic Step 3 estimate
  ledger for candidates that have already failed the Tao gate.

### 5. What this newly tests relative to prior negatives

- [VERIFIED] This is distinct from the De Giorgi sharpness record.
  The De Giorgi / Vasseur negatives say the classical pressure-side framework
  hits `beta = 4/3` and the `W^{1,3}` wall.
  This step instead asks a narrower question:
  can exact Navier-Stokes rewrites of the same quadratic interaction improve
  one fixed localized LEI cutoff-flux coefficient before any new architecture
  is introduced?
  Sources:
  - `missions/vasseur-pressure/steps/step-001/RESULTS.md`
  - `missions/vasseur-pressure/steps/step-002/RESULTS.md`
- [VERIFIED] This is distinct from the pressure-route negatives.
  Step 1 killed the harmonic-tail branch by showing that generic harmonic
  regularity and algebraic rewrites do not shrink the live far-field pressure
  coefficient.
  Step 6 instead tests the same algebraic optimism inside the local-energy
  cutoff-flux architecture, with the bad term fixed at `I_flux[phi]`.
  Source:
  - `missions/beyond-de-giorgi/steps/step-001/RESULTS.md`
- [VERIFIED] This is distinct from the killed geometry branch.
  Step 2 and Step 4 screened geometry / persistence candidates against full
  stretching and dynamic plausibility.
  Step 6 asks whether the non-geometry exact rewrite family itself survives a
  Tao screen on the fixed LEI target, without allowing geometry or stretching
  rescue language to smuggle the branch back in.
  Sources:
  - `missions/beyond-de-giorgi/steps/step-002/RESULTS.md`
  - `missions/beyond-de-giorgi/steps/step-004/RESULTS.md`
- [INFERRED] The new obstruction diagnosis earned here is therefore narrow and
  clean:
  within one frozen localized LEI protocol, the standard exact reformulation
  family does not supply a Tao-sensitive estimate lever on the cutoff-flux
  bundle.

## Conclusion

- Outcome: `succeeded`
- [INFERRED] Unified Step-2 verdict:
  all three frozen candidates are rejected as Tao-insufficient.
- [INFERRED] Branch recommendation:
  stop the exact-rewrite audit here and invalidate the branch rather than
  continuing to a cosmetic Step 3.
