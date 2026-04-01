# Exploration 001 Report

## Goal

Build the bounded Step-2 candidate slate for the active exact-rewrite audit.

## Method

- Read the frozen ledger from `step-013`.
- Reuse the repository-native exact-rewrite shortlist from Step 005.
- Reuse the Step-006 candidate screens to judge which packages are at least
  specific enough to audit as active candidates under the frozen LEI burden.
- Keep the slate bounded to two active candidates and one reserve.

## Operational Note

- [VERIFIED] The wrapper-launched explorer session did not land
  `REPORT-SUMMARY.md` during a bounded wait.
- [VERIFIED] As in `step-013`, the strategizer completed the report directly
  from the same repository-local source set so the step could continue.

## Source Log

- `missions/beyond-de-giorgi/steps/step-013/RESULTS.md`
- `missions/beyond-de-giorgi/library-inbox/step-005-exploration-003-gain-currency-candidate-family.md`
- `missions/beyond-de-giorgi/library-inbox/step-006-exploration-001-tao-screen-divergence-lamb.md`
- `missions/beyond-de-giorgi/library-inbox/step-006-exploration-002-tao-screen-vorticity-biot-savart.md`
- `missions/beyond-de-giorgi/library-inbox/step-006-exploration-003-unified-tao-verdict.md`
- `library/factual/exact-rewrite-obstruction-audit/step-1-exact-rewrite-family-is-bounded-to-three-candidates.md`
- `library/factual/exact-rewrite-obstruction-audit/lamb-vector-projected-form-is-tao-insufficient-once-localization-debt-returns.md`
- `library/factual/exact-rewrite-obstruction-audit/vorticity-biot-savart-form-is-tao-insufficient-on-the-fixed-lei-ledger.md`
- `missions/beyond-de-giorgi/MISSION.md`

## Findings

### 1. The admissible slate is already bounded on the repository record

- [VERIFIED] The exact-rewrite branch already froze a three-family shortlist:
  `divergence / stress form`,
  `Lamb-vector / Helmholtz-projected form`,
  `vorticity transport / Biot-Savart form`.
  Sources:
  - `missions/beyond-de-giorgi/library-inbox/step-005-exploration-003-gain-currency-candidate-family.md`
  - `library/factual/exact-rewrite-obstruction-audit/step-1-exact-rewrite-family-is-bounded-to-three-candidates.md`
- [VERIFIED] The Step-013 ledger now fixes the theorem-facing target as the
  full localized LEI cutoff-flux bundle
  `I_flux[phi] = ∬ (|u|^2 + 2p) u · ∇phi`
  on the inherited suitable-weak / LEI floor with one shared CKN-style cutoff.
  Source:
  - `missions/beyond-de-giorgi/steps/step-013/RESULTS.md`
- [INFERRED] That means the Step-2 slate should be chosen from the existing
  exact-rewrite-native shortlist rather than importing pressure-Hessian or
  geometry-facing families from older branches.

### 2. Active candidate 1: `Lamb-vector / Helmholtz-projected form`

- [VERIFIED] Exact package:
  velocity equation rewritten as
  `(u · ∇)u = ∇(|u|^2/2) - u × ω`,
  with projected form
  `P((u · ∇)u) = -P(u × ω)`.
- [INFERRED] Why it earns active status:
  among the repository-native exact rewrites, this is the clearest candidate
  that claims a specific nonlinear structural delta rather than mere placement
  of derivatives.
  The package isolates a gradient piece, exposes the Lamb vector explicitly,
  and names exact Beltrami cancellation as its most favorable anchor case.
- [INFERRED] Named route back to the frozen burden currency:
  if the projected Lamb-vector form were live, it would have to reduce the
  effective coefficient on the same `I_flux[phi]` bundle after the gradient
  piece is repaid through pressure/projection bookkeeping.
- [INFERRED] Why it is still only Step-2 active, not promoted:
  the local record already warns that this route may collapse once
  localization, pressure re-entry, Calderon-Zygmund debt, and commutators
  return.

### 3. Active candidate 2: `vorticity transport / Biot-Savart form`

- [VERIFIED] Exact package:
  vorticity transport-diffusion with velocity reconstructed from vorticity by
  Biot-Savart.
- [INFERRED] Why it earns active status:
  this is the only other exact-rewrite-native family on disk with a concrete
  theorem-facing promise beyond pure conservative-form packaging.
  It relocates the same quadratic interaction to the vorticity side and makes
  the reconstruction debt explicit.
- [INFERRED] Named route back to the frozen burden currency:
  any gain would have to appear when one rewrites velocity factors inside the
  same localized `I_flux[phi]` bundle through `ω`, then proves that the full
  Biot-Savart and localization debt still leaves a smaller effective
  coefficient.
- [INFERRED] Why it is still only Step-2 active, not promoted:
  the branch record already warns that this apparent gain may be only a
  repackaging unless the same-currency exchange can be shown.

### 4. Reserve candidate: `divergence / stress form`

- [VERIFIED] Exact package:
  `(u · ∇)u = ∇ · (u ⊗ u)` when `div u = 0`.
- [INFERRED] Why it stays reserve:
  it is exact-rewrite-native and admissible, but it offers the weakest
  candidate-specific delta under the fixed LEI ledger.
  The current record already shows its likely insertion point is just
  integration by parts back to the same stress-against-`∇phi` burden.
- [INFERRED] So it is useful as a control comparator but not the best use of
  one of the two active slots.

### 5. Omitted family memo

- [VERIFIED] `strain / pressure-Hessian` language does appear elsewhere in the
  repository, but in pressure-branch and geometry-adjacent materials rather
  than in the frozen exact-rewrite shortlist for this branch.
- [INFERRED] It should therefore not be promoted into this Step-2 exact-rewrite
  slate without reopening a different branch architecture.

## Candidate Slate Sheet

| slot | candidate family | exact unknown or package | inclusion verdict |
| --- | --- | --- | --- |
| active | `Lamb-vector / Helmholtz-projected form` | velocity package `u`, `ω = curl u`, with `P((u · ∇)u) = -P(u × ω)` | `[INFERRED]` keep active because it names the sharpest exact algebraic delta on the record and a direct, testable route back to `I_flux[phi]` |
| active | `vorticity transport / Biot-Savart form` | package `(ω, u = BS[ω])` with vorticity transport and explicit reconstruction | `[INFERRED]` keep active because it is the only other exact-rewrite-native family with a nontrivial candidate-specific theorem-facing story |
| reserve | `divergence / stress form` | velocity package `u` with conservative stress divergence | `[INFERRED]` keep only as reserve because it localizes back to the same burden with even less candidate-specific structure |

## Decision Memo

- [INFERRED] Frozen Step-2 active candidates:
  `Lamb-vector / Helmholtz-projected form`,
  `vorticity transport / Biot-Savart form`.
- [INFERRED] Frozen Step-2 reserve:
  `divergence / stress form`.
- [INFERRED] Omitted for now:
  `strain / pressure-Hessian` or other branch-adjacent families, because the
  current exact-rewrite branch never froze them as admissible Step-2 native
  candidates.

## Conclusion

- Outcome: `succeeded`
- [INFERRED] The step now has a bounded slate rather than a soft portfolio.
- [INFERRED] The active pair is strong enough to force the equation and
  exchange audit, while the reserve keeps one exact-rewrite-native comparator
  alive without reopening another branch.
