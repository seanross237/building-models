# Exploration 002 Report

## Goal

Evaluate the third frozen exact-rewrite candidate for Step 006:
`vorticity transport / Biot-Savart form`.

Required audit frame:

- architecture: `local-energy flux/localization`
- bad term: `I_flux[phi] = \iint_{Q_r} (|u|^2 + 2p) u \cdot \nabla \phi`
- solution class: suitable weak solutions in the Leray-Hopf energy class with LEI
- localization: one CKN-style parabolic cutoff with all Biot-Savart, projection,
  Calderon-Zygmund, and commutator debt charged explicitly
- gain currency: coefficient shrinkage in the fixed localized LEI balance

## Method

- Read the Step 006 goal and the mission-level chain / controller constraints.
- Read the Step 005 freeze record and the prior vorticity-candidate discussion.
- Read the fixed-audit factual files on the bad term, success criterion, cutoff
  protocol, and localization debt.
- Search the local repository for any sharper vorticity-side Tao discriminator
  than "rewrite through `omega` and repay Biot-Savart cost."

## Source Log

- `missions/beyond-de-giorgi/steps/step-006/GOAL.md`
- `missions/beyond-de-giorgi/CHAIN.md`
- `missions/beyond-de-giorgi/MISSION.md`
- `missions/beyond-de-giorgi/controller/decisions/decision-008.md`
- `missions/beyond-de-giorgi/steps/step-005/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-005/explorations/exploration-003/REPORT.md`
- `library/factual/exact-rewrite-obstruction-audit/projected-and-vorticity-rewrites-must-pay-localization-debt.md`
- `library/factual/exact-rewrite-obstruction-audit/freeze-one-ckn-style-parabolic-cutoff-protocol-for-the-rewrite-audit.md`
- `library/factual/exact-rewrite-obstruction-audit/step-1-exact-rewrite-family-is-bounded-to-three-candidates.md`
- `library/factual/exact-rewrite-architecture-screening/the-localized-lei-cutoff-flux-bundle-is-the-fixed-bad-term-for-the-audit.md`
- `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`
- `library/factual/exact-rewrite-architecture-screening/local-energy-flux-localization-is-the-right-inherited-architecture-for-the-exact-rewrite-audit.md`
- `library/factual/exact-rewrite-architecture-screening/stretching-localization-mismatches-the-rewrite-audit-and-reopens-a-killed-branch.md`
- `library/factual/far-field-pressure-obstruction/generic-harmonic-regularity-fails-the-tao-gate.md`
- `library/factual/far-field-pressure-obstruction/algebraic-rewrites-and-local-geometry-fail-the-tao-gate.md`
- `runtime/results/codex-patlas-standalone-20260331T130634Z-receptionist-94037.md`

## Findings

### 1. Fixed audit standard

- [VERIFIED] The audit only counts progress if the candidate lowers the
  effective estimate on the same localized LEI cutoff-flux bundle
  `I_flux[phi] = \iint (|u|^2 + 2p) u . \nabla phi`, under the same cutoff
  protocol, after all projection, Calderon-Zygmund, commutator, and
  Biot-Savart costs are paid.
  Sources:
  - `library/factual/exact-rewrite-architecture-screening/the-localized-lei-cutoff-flux-bundle-is-the-fixed-bad-term-for-the-audit.md`
  - `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`
  - `missions/beyond-de-giorgi/steps/step-005/RESULTS.md`
- [VERIFIED] Rewriting through `omega` is admissible only if every
  Biot-Savart reinsertion and localization cost is charged back in the same
  ledger.
  Sources:
  - `library/factual/exact-rewrite-obstruction-audit/freeze-one-ckn-style-parabolic-cutoff-protocol-for-the-rewrite-audit.md`
  - `library/factual/exact-rewrite-obstruction-audit/projected-and-vorticity-rewrites-must-pay-localization-debt.md`
  - `library/factual/exact-rewrite-obstruction-audit/step-1-exact-rewrite-family-is-bounded-to-three-candidates.md`

### 2. What exact NS feature is the candidate claiming to exploit?

- [INFERRED] The strongest exact feature the local record lets this candidate
  claim is narrow:
  the actual NS nonlinearity can be relocated to the vorticity side, with the
  velocity recovered from `omega` by the incompressible Biot-Savart relation,
  so the same quadratic interaction is viewed as a vorticity-transport /
  Biot-Savart interaction rather than directly as `u . nabla u`.
  Sources:
  - `missions/beyond-de-giorgi/steps/step-005/explorations/exploration-003/REPORT.md`
  - `library/factual/exact-rewrite-obstruction-audit/step-1-exact-rewrite-family-is-bounded-to-three-candidates.md`
  - `missions/beyond-de-giorgi/steps/step-005/RESULTS.md`
- [VERIFIED] The repository does **not** support a stronger fixed-architecture
  claim such as:
  "the vorticity rewrite already controls stretching," or
  "the vorticity rewrite already produces a smaller LEI coefficient before the
  debt ledger is run."
  Sources:
  - `missions/beyond-de-giorgi/steps/step-005/RESULTS.md`
  - `missions/beyond-de-giorgi/steps/step-005/explorations/exploration-003/REPORT.md`
  - `library/factual/exact-rewrite-architecture-screening/stretching-localization-mismatches-the-rewrite-audit-and-reopens-a-killed-branch.md`
- [INFERRED] So the candidate's real Step-2 claim is not a new estimate-level
  mechanism. It is only a more Navier-Stokes-looking exact representation of
  the same quadratic interaction.

### 3. Tao discriminator: destroyed, weakened, or preserved?

- [VERIFIED] Tao's averaged-model constraint, as recorded in the mission, is
  that any route resting only on energy identity plus standard harmonic
  analysis is insufficient; the averaged model preserves that structure.
  Sources:
  - `missions/beyond-de-giorgi/MISSION.md`
  - `library/factual/far-field-pressure-obstruction/generic-harmonic-regularity-fails-the-tao-gate.md`
- [INFERRED] Under the fixed LEI audit, the vorticity/Biot-Savart candidate's
  claimed feature is best classified as:
  `preserves`.
- [INFERRED] Reason:
  the local record does not isolate any extra NS-specific content that Tao-style
  averaging would destroy. What remains admissible is a restatement of the same
  quadratic interaction together with Biot-Savart / singular-integral
  reconstruction, and the repository repeatedly treats such material as part of
  the same harmonic-analysis / localization bookkeeping that must be repaid.
  Sources:
  - `missions/beyond-de-giorgi/planning-runs/run-003/judgments/chain-01.md`
  - `missions/beyond-de-giorgi/planning-runs/run-003/attacks/chain-01.md`
  - `library/factual/exact-rewrite-obstruction-audit/projected-and-vorticity-rewrites-must-pay-localization-debt.md`
  - `runtime/results/codex-patlas-standalone-20260331T130634Z-receptionist-94037.md`
- [VERIFIED] The mission background already says the vorticity formulation also
  lands at the same `beta = 4/3` barrier and that the quadratic obstruction is
  not removed merely by moving to `omega`.
  Source:
  - `missions/beyond-de-giorgi/MISSION.md`
- [INFERRED] A weaker verdict such as `weakens` is not supported by the local
  sources unless one silently promotes the candidate into a stretching or
  geometry route. Inside the frozen LEI architecture, no distinct destroyed
  feature is actually named.

### 4. Where could the distinction matter inside the fixed localized estimate?

- [VERIFIED] The only legitimate target is still the same localized cutoff-flux
  bundle `I_flux[phi]`; no other bad term is allowed at Step 2.
  Sources:
  - `missions/beyond-de-giorgi/steps/step-006/GOAL.md`
  - `library/factual/exact-rewrite-architecture-screening/the-localized-lei-cutoff-flux-bundle-is-the-fixed-bad-term-for-the-audit.md`
- [INFERRED] The only candidate-specific insertion point is formal:
  inside the fixed estimate on `I_flux[phi]`, one could try to re-express one
  or more velocity-side factors through `omega` and Biot-Savart after
  localization and hope this shrinks the effective coefficient.
- [INFERRED] But the repository supports no live insertion point beyond that
  formal substitution. Once the cutoff is fixed, Biot-Savart reinsertion and
  cutoff commutation create the very nonlocal debt the protocol says must be
  charged back to the candidate.
  Sources:
  - `library/factual/exact-rewrite-obstruction-audit/freeze-one-ckn-style-parabolic-cutoff-protocol-for-the-rewrite-audit.md`
  - `library/factual/exact-rewrite-obstruction-audit/projected-and-vorticity-rewrites-must-pay-localization-debt.md`
  - `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`
- [INFERRED] So there is no credible localized insertion point before Step 3
  other than the generic hope of a smaller coefficient on the same `I_flux[phi]`
  term, and the local record provides no evidence that the vorticity rewrite
  achieves even that.

### 5. Does keeping the candidate alive require architecture drift?

- [VERIFIED] The repository already warns that shifting this route toward
  vorticity stretching localization is a mismatch for the rewrite audit and
  effectively reopens the killed geometry branch.
  Source:
  - `library/factual/exact-rewrite-architecture-screening/stretching-localization-mismatches-the-rewrite-audit-and-reopens-a-killed-branch.md`
- [INFERRED] Yes. Any attempt to make the vorticity-side rewrite look genuinely
  Tao-sensitive seems to require leaving the fixed `I_flux[phi]` audit and
  appealing instead to stretching-facing or geometry-facing material:
  `S omega . omega`, local Beltrami / alignment, tube structure, or related
  hybrid observables.
  Sources:
  - `missions/beyond-de-giorgi/steps/step-004/RESULTS.md`
  - `library/factual/exact-rewrite-architecture-screening/stretching-localization-mismatches-the-rewrite-audit-and-reopens-a-killed-branch.md`
  - `missions/beyond-de-giorgi/steps/step-005/RESULTS.md`
- [INFERRED] That rescue is outside this candidate's admissible Step-2 role.
  Under the frozen architecture, the route must act on `I_flux[phi]`; once it
  instead depends on stretching or geometry localization, it is no longer the
  same branch.

### 6. Does Biot-Savart reinsertion merely repay the same nonlocal cost?

- [VERIFIED] Yes, that is exactly how the fixed protocol tells us to charge the
  candidate:
  all Biot-Savart reinsertions and cutoff-commutation debt must be paid in the
  same ledger.
  Sources:
  - `library/factual/exact-rewrite-obstruction-audit/freeze-one-ckn-style-parabolic-cutoff-protocol-for-the-rewrite-audit.md`
  - `library/factual/exact-rewrite-obstruction-audit/projected-and-vorticity-rewrites-must-pay-localization-debt.md`
- [INFERRED] The local Step-005 freeze already anticipated the consequence:
  this candidate's first obvious cosmetic risk is that it "drifts toward a
  different architecture" and that "Biot-Savart reinsertion repays the same
  nonlocal cost."
  Sources:
  - `missions/beyond-de-giorgi/steps/step-005/RESULTS.md`
  - `missions/beyond-de-giorgi/steps/step-005/explorations/exploration-003/REPORT.md`
- [INFERRED] Therefore, as long as the branch is kept honest about the fixed
  LEI ledger, the vorticity-side rewrite does not buy a Step-2 survivor. It
  only repackages the same nonlocal burden in a different vocabulary.

## Dead Ends / Failed Attempts

- [VERIFIED] A broad repository search for a sharper vorticity-side Tao
  discriminator found no stronger local claim than:
  "exact vorticity-side structure of the same quadratic interaction, with full
  Biot-Savart debt repaid."
- [VERIFIED] I also checked for a neighboring Step-006 exploration report to
  compare classification style; `exploration-003` had no `REPORT.md`, so there
  was no extra local precedent to extract.

## Conclusion

- [INFERRED] Tao-screen verdict for `vorticity transport / Biot-Savart form`:
  `preserves`
- [INFERRED] Exact claimed NS-specific feature:
  only the vorticity-side relocation of the same quadratic interaction, coupled
  back to velocity by Biot-Savart
- [INFERRED] Honest localized insertion point:
  none beyond the formal attempt to rewrite factors inside the fixed
  `I_flux[phi]` estimate, which immediately repays the same nonlocal debt
- [INFERRED] Step-2 classification:
  `reject as Tao-insufficient`
- [INFERRED] Reason:
  within the frozen LEI architecture, the repository supports no destroyed
  Tao-sensitive feature and no smaller effective coefficient on `I_flux[phi]`;
  the only way to keep the route alive is to drift into stretching/geometry
  work, which would be a different branch rather than a survivor of this one.

## Outcome

- Outcome: `succeeded`
- Hypothesis test:
  confirmed and sharpened. The local record supports the negative version of
  the strategizer's hypothesis:
  within the fixed LEI audit the vorticity/Biot-Savart candidate is only a
  repackaging of the same quadratic interaction, and any stronger-looking
  effect would require forbidden architecture drift.
