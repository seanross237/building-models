# Exploration 001 Report

## Goal

Run the Tao discriminator on the first two frozen exact-rewrite candidates for
step-006 of `Fixed-Protocol Obstruction Audit for Exact NS Reformulations`:

- `divergence / stress form`
- `Lamb-vector / Helmholtz-projected form`

Required outputs:

- identify the exact Navier-Stokes-specific feature claimed for each candidate
- decide whether Tao-style averaging destroys, weakens, or preserves that
  feature
- note where the distinction could matter in the fixed localized balance on
  `I_flux[phi]`, if anywhere
- classify each candidate as `admit to Step 3`,
  `reject as Tao-insufficient`, or `reject as architecture-changing`

## Method

- Use only repository-local mission and library sources.
- Keep the audit architecture fixed:
  `local-energy flux/localization`, one CKN-style parabolic cutoff, with
  projection, Calderon-Zygmund, commutator, and Biot-Savart debt charged
  explicitly.
- Label claims as `[VERIFIED]`, `[INFERRED]`, or `[PROPOSED]`.
- Record dead ends and failed attempts honestly.

## Operational Note

- [VERIFIED] The launched explorer session created the report skeleton but did
  not finish reliably in this environment. The strategizer completed the report
  directly from the anchored local source set so the exploration could close
  cleanly.

## Source Log

- `missions/beyond-de-giorgi/steps/step-006/GOAL.md`
- `missions/beyond-de-giorgi/CHAIN.md`
- `missions/beyond-de-giorgi/MISSION.md`
- `missions/beyond-de-giorgi/controller/decisions/decision-008.md`
- `missions/beyond-de-giorgi/steps/step-005/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-005/explorations/exploration-003/REPORT.md`
- `library/factual/exact-rewrite-obstruction-audit/projected-and-vorticity-rewrites-must-pay-localization-debt.md`
- `library/factual/exact-rewrite-obstruction-audit/every-rewrite-must-stay-inside-the-same-localized-lei-package.md`
- `library/factual/exact-rewrite-architecture-screening/the-localized-lei-cutoff-flux-bundle-is-the-fixed-bad-term-for-the-audit.md`
- `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`
- `library/factual/far-field-pressure-obstruction/algebraic-rewrites-and-local-geometry-fail-the-tao-gate.md`
- `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
- `runtime/results/codex-patlas-standalone-20260331T130634Z-receptionist-94037.md`

## Findings

### 1. Common Step-2 screen for both candidates

- [VERIFIED] The branch's mechanical Tao-screen rule is already fixed:
  a candidate only counts if it changes an estimate on the live obstruction and
  makes an exact term or coefficient smaller in the same frozen balance.
  Sources:
  - `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
  - `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`
- [VERIFIED] The live obstruction for this branch is the localized LEI
  cutoff-flux bundle
  `I_flux[phi] = ∬_{Q_r} (|u|^2 + 2p) u · ∇phi`.
  Sources:
  - `library/factual/exact-rewrite-architecture-screening/the-localized-lei-cutoff-flux-bundle-is-the-fixed-bad-term-for-the-audit.md`
  - `missions/beyond-de-giorgi/steps/step-005/RESULTS.md`
- [VERIFIED] Projected and related exact rewrites earn no credit before
  localization debt is repaid after the cutoff is fixed.
  Source:
  - `library/factual/exact-rewrite-obstruction-audit/projected-and-vorticity-rewrites-must-pay-localization-debt.md`
- [INFERRED] So the only honest insertion point for either candidate is:
  does the rewrite produce a smaller effective coefficient on the same
  `I_flux[phi]` term before any architecture change?

### 2. Candidate: `divergence / stress form`

- [INFERRED] Exact claimed Navier-Stokes feature:
  use incompressibility to rewrite
  `(u · ∇)u = ∇ · (u ⊗ u)`,
  so the quadratic interaction looks like a divergence of stress and the
  derivative can be placed on the cutoff in a cleaner way.
  Sources:
  - `missions/beyond-de-giorgi/steps/step-005/explorations/exploration-003/REPORT.md`
  - `missions/beyond-de-giorgi/steps/step-005/RESULTS.md`
- [INFERRED] Tao-screen verdict:
  `preserves`, but only as identity-level packaging.
  The repository does not support a separate NS-specific estimate lever here.
  The divergence-form move is a standard incompressible rewrite; Tao-style
  averaging is designed to preserve that kind of generic divergence-free /
  harmonic-analysis structure.
  Sources:
  - `library/factual/far-field-pressure-obstruction/algebraic-rewrites-and-local-geometry-fail-the-tao-gate.md`
  - `runtime/results/codex-patlas-standalone-20260331T130634Z-receptionist-94037.md`
- [INFERRED] Exact localized insertion point:
  the only possible slot is the transport part of `I_flux[phi]`, where one
  would integrate by parts and hope the stress form lowers the coefficient of
  the cutoff interaction.
  But the Step-5 table already records the first cosmetic failure:
  after integration by parts, the same stress-against-`∇phi` burden returns.
  Sources:
  - `missions/beyond-de-giorgi/steps/step-005/explorations/exploration-003/REPORT.md`
  - `missions/beyond-de-giorgi/steps/step-005/RESULTS.md`
  - `library/factual/exact-rewrite-architecture-screening/the-localized-lei-cutoff-flux-bundle-is-the-fixed-bad-term-for-the-audit.md`
- [INFERRED] What fails precisely:
  the rewrite can rename where the derivative visibly lands, but it does not
  identify any smaller coefficient in the frozen LEI balance.
  Under the branch rule, that makes the specialness purely verbal /
  identity-level rather than estimate-level.
  Sources:
  - `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
  - `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`
- [INFERRED] Step-2 classification:
  `reject as Tao-insufficient`

### 3. Candidate: `Lamb-vector / Helmholtz-projected form`

- [INFERRED] Exact claimed Navier-Stokes feature:
  isolate the gradient piece in
  `(u · ∇)u = ∇(|u|^2/2) - u × omega`,
  then remove the gradient by Helmholtz projection so that the remaining
  nonlinearity looks like the more first-order Lamb vector.
  In the most favorable exact case, Beltrami alignment kills the Lamb-vector
  term.
  Sources:
  - `missions/beyond-de-giorgi/MISSION.md`
  - `missions/beyond-de-giorgi/steps/step-005/explorations/exploration-003/REPORT.md`
  - `missions/beyond-de-giorgi/steps/step-005/RESULTS.md`
- [INFERRED] Tao-screen verdict:
  `weakens` the purported leverage down to an identity-level remnant.
  The exact gradient/Lamb decomposition survives algebraically, but the local
  record says its apparent gain is washed out once localization restores the
  same projection, pressure, Calderon-Zygmund, and commutator debt.
  Sources:
  - `library/factual/exact-rewrite-obstruction-audit/projected-and-vorticity-rewrites-must-pay-localization-debt.md`
  - `runtime/results/codex-patlas-standalone-20260331T130634Z-receptionist-94037.md`
  - `missions/beyond-de-giorgi/steps/step-005/RESULTS.md`
- [INFERRED] Exact localized insertion point:
  the candidate could only matter where `I_flux[phi]` pays the cubic-transport
  and pressure-transport pieces against `∇phi`, namely if the projected
  Lamb-vector form produced a smaller effective coefficient after the cutoff is
  inserted.
  The repository does not supply such a coefficient improvement; it says the
  gradient part simply reappears inside pressure/projection bookkeeping.
  Sources:
  - `library/factual/exact-rewrite-architecture-screening/the-localized-lei-cutoff-flux-bundle-is-the-fixed-bad-term-for-the-audit.md`
  - `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`
  - `missions/beyond-de-giorgi/steps/step-005/explorations/exploration-003/REPORT.md`
- [VERIFIED] The mission background already treats exact Beltrami cancellation
  as fragile and insufficient as a general lever.
  Source:
  - `missions/beyond-de-giorgi/MISSION.md`
- [INFERRED] What fails precisely:
  if the candidate is kept inside the frozen LEI package, the attractive
  first-order-looking form does not shrink the fixed coefficient.
  If one tries to rescue it by leaning on special alignment beyond the fixed
  package, the route starts drifting toward the already-killed geometry branch.
  Sources:
  - `missions/beyond-de-giorgi/MISSION.md`
  - `missions/beyond-de-giorgi/steps/step-004/RESULTS.md`
- [INFERRED] Step-2 classification:
  `reject as Tao-insufficient`

### 4. Candidate table for this exploration

| Candidate | Claimed NS-specific feature | Tao-screen verdict | Credible insertion point in `I_flux[phi]` | Classification |
| --- | --- | --- | --- | --- |
| `divergence / stress form` | [INFERRED] incompressible stress-divergence rewriting of convection | `preserved` only as identity-level packaging | [INFERRED] only by trying to lower the transport-side cutoff coefficient, but IBP recreates the same stress-against-`∇phi` burden | `reject as Tao-insufficient` |
| `Lamb-vector / Helmholtz-projected form` | [INFERRED] isolate gradient part and expose projected Lamb-vector structure; exact Beltrami is the favorable anchor case | `weakens` to an identity once localization debt is repaid | [INFERRED] only if projection/Lamb rewriting lowered the same cutoff-flux coefficient, but the same pressure / CZ / commutator burden returns | `reject as Tao-insufficient` |

## Dead Ends / Rejected Paths

- [INFERRED] Rejected the temptation to count "cleaner derivative placement" as
  progress without naming a smaller coefficient on the fixed LEI balance.
- [INFERRED] Rejected any rescue by special alignment or geometry because Step 2
  is not allowed to reopen the killed geometry branch.

## Conclusion

- Outcome: `succeeded`
- [INFERRED] Neither of the first two frozen rewrites survives the Tao screen.
- [INFERRED] Both candidates fail for the same branch-specific reason:
  the exact identity remains available, but no source-backed estimate-level
  insertion point shrinks the fixed `I_flux[phi]` coefficient once the
  localized LEI bookkeeping is restored.
