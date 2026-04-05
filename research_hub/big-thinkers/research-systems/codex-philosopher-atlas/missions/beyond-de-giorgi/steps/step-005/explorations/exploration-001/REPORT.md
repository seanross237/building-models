# Exploration 001 Report

## Goal

Choose exactly one inherited architecture and exactly one named bad term for
`step-005` of the chain
`Fixed-Protocol Obstruction Audit for Exact NS Reformulations`.

## Method

- Read the chain record and the run-003 planning/judgment materials.
- Read the strongest local architecture sources:
  - `missions/navier-stokes/library-inbox/ckn-1982-proof-architecture.md`
  - `missions/navier-stokes/library-inbox/vasseur-2007-proof-architecture.md`
- Read the already-earned branch negatives:
  - `missions/beyond-de-giorgi/steps/step-001/RESULTS.md`
  - `missions/beyond-de-giorgi/steps/step-004/RESULTS.md`
  - `missions/vasseur-pressure/steps/step-001/RESULTS.md`
  - `missions/vasseur-pressure/steps/step-002/RESULTS.md`
- Cross-check against the receptionist result for this step.

## Operational Note

- [VERIFIED] The launched explorer session created the report scaffold but did
  not complete reliably in this environment. The strategizer completed the
  source-based memo directly from the anchored local materials so the step
  could continue honestly.

## Findings

### 1. Source-supported architecture menu

- [VERIFIED] The active chain requires a single inherited estimate
  architecture chosen from:
  `De Giorgi truncation`, `local-energy flux/localization`, or
  `vorticity stretching localization`.
  Sources:
  - `missions/beyond-de-giorgi/CHAIN.md`
  - `missions/beyond-de-giorgi/planning-runs/run-003/refined/chain-01.md`
- [VERIFIED] The same chain also requires one fixed protocol, one fixed bad
  term, and one bounded rewrite family before any Tao screen or estimate
  testing.
  Sources:
  - `missions/beyond-de-giorgi/CHAIN.md`
  - `missions/beyond-de-giorgi/planning-runs/run-003/judgments/chain-01.md`

### 2. Why `De Giorgi truncation` is not the best architecture for this step

- [VERIFIED] The local record already treats the De Giorgi/Vasseur pressure
  barrier as exhausted: `beta = 4/3` is sharp across the documented pressure
  routes, the H^1/BMO, atomic, and interpolation variants all failed, and the
  far-field pressure branch was already downgraded to a narrow negative track.
  Sources:
  - `missions/beyond-de-giorgi/MISSION.md`
  - `missions/vasseur-pressure/steps/step-001/RESULTS.md`
  - `missions/vasseur-pressure/steps/step-002/RESULTS.md`
  - `missions/beyond-de-giorgi/steps/step-001/RESULTS.md`
- [VERIFIED] The mission background says not to spend budget on De Giorgi
  tuning, stronger-type pressure estimates, or renamed H^1/BMO variants.
  Source:
  - `missions/beyond-de-giorgi/planning-runs/run-003/planner.md`
- [INFERRED] Fixing the architecture directly as De Giorgi truncation would
  force the step back toward one of two already pre-closed targets:
  - the far-field pressure coefficient, already isolated negatively in
    `step-001` and the `vasseur-pressure` mission;
  - or the local pressure obstruction, already heavily benchmarked and not a
    clean new audit target for the present exact-rewrite cleanup branch.
- [INFERRED] So De Giorgi is too overdetermined by local prior negatives to be
  the fairest place to test the exact-rewrite shortlist.

### 3. Why `vorticity stretching localization` is not the best architecture

- [VERIFIED] The mission and planning record repeatedly warns that the natural
  exact-rewrite shortlist (`Lamb-vector`, projected form, vorticity transport)
  does not automatically target full stretching `S omega . omega`.
  Sources:
  - `missions/beyond-de-giorgi/MISSION.md`
  - `missions/beyond-de-giorgi/planning-runs/run-003/attacks/chain-01.md`
  - `missions/beyond-de-giorgi/planning-runs/run-001/attacks/chain-02.md`
- [VERIFIED] The geometry branch was already killed when forced to control the
  full stretching mechanism under a fixed package; local Beltrami/Lamb-vector
  improvements were explicitly ruled out as wrong-target progress.
  Sources:
  - `missions/beyond-de-giorgi/steps/step-004/RESULTS.md`
  - `library/factual/geometry-route-screening/geometry-candidates-must-act-on-full-stretching.md`
- [INFERRED] Choosing stretching localization here would therefore mismatch the
  rewrite family the chain itself expects and would risk reopening the killed
  geometry branch under a new label.

### 4. Why `local-energy flux/localization` is the right architecture

- [VERIFIED] The selected and refined chain versions describe this branch as a
  local estimate-level audit of exact nonlinear rewrites, not as a new
  pressure-only or geometry-only program.
  Sources:
  - `missions/beyond-de-giorgi/planning-runs/run-003/selected/chain-01.md`
  - `missions/beyond-de-giorgi/planning-runs/run-003/refined/chain-01.md`
- [VERIFIED] The CKN architecture gives the cleanest explicit localized balance
  in the local record:
  \[
  2 \iint |\nabla u|^2 \phi
  \le
  \iint |u|^2 (\partial_t \phi + \Delta \phi)
  + \iint (|u|^2 + 2p)\,u \cdot \nabla \phi.
  \]
  Source:
  - `missions/navier-stokes/library-inbox/ckn-1982-proof-architecture.md`
- [VERIFIED] This architecture is already written in the exact language the
  chain wants to audit later: one fixed cutoff, one fixed localized balance,
  and explicit places where projection/CZ/localization costs enter.
  Sources:
  - `missions/navier-stokes/library-inbox/ckn-1982-proof-architecture.md`
  - `missions/beyond-de-giorgi/planning-runs/run-003/judgments/chain-01.md`
- [INFERRED] This is the fairest architecture for the rewrite family because
  the natural exact rewrites all start from the same quadratic interaction
  before localization, and the local-energy balance is exactly where one can
  see whether the rewrite changes the operative cutoff cost or merely moves it.

### 5. Chosen bad term

- [INFERRED] Chosen architecture:
  `local-energy flux/localization`
- [INFERRED] Chosen bad term:
  the **localized LEI cutoff-flux bundle**
  \[
  I_{\mathrm{flux}}[\phi]
  :=
  \iint_{Q_r} (|u|^2 + 2p)\,u \cdot \nabla \phi.
  \]
- [VERIFIED] This term is explicit in the CKN local energy inequality and is
  the unique place where the localized nonlinear transport and pressure
  transport costs are paid against the same cutoff.
  Source:
  - `missions/navier-stokes/library-inbox/ckn-1982-proof-architecture.md`
- [INFERRED] This is the right bad term for the present branch because:
  - it is not the already-killed far-field pressure coefficient;
  - it is not the full stretching target that killed the geometry branch;
  - and it is exactly the localized interaction on which the standard exact
    rewrite family can be compared without changing architecture.
- [INFERRED] Later steps should treat this entire cutoff-flux bundle as the
  fixed target. A rewrite does **not** count as progress if it merely shifts
  cost between the cubic `|u|^2 u · \nabla \phi` piece and the pressure
  transport `p\,u \cdot \nabla \phi` piece while leaving the same effective LEI
  closure cost.

### 6. What later success would mean

- [INFERRED] Later success in this fixed setup would mean:
  one of the bounded exact rewrites produces a smaller effective estimate on
  `I_flux[φ]` in the same cutoff protocol and same solution class, after all
  projection, Calderon-Zygmund, and commutator costs are paid.
- [INFERRED] It would **not** mean:
  - a prettier identity before localization,
  - a gain only on the Lamb-vector side with no LEI closure improvement,
  - or a shift to a vorticity/stretching architecture.

## Decision Memo

- [VERIFIED] The architecture can be fixed concretely; the step does **not**
  trigger the under-specification kill.
- [INFERRED] Final architecture choice:
  `local-energy flux/localization`
- [INFERRED] Final bad term:
  `I_flux[φ] = ∬ (|u|^2 + 2p) u · ∇φ`
- [INFERRED] Rejected architectures:
  - `De Giorgi truncation`:
    too entangled with already-earned pressure negatives
  - `vorticity stretching localization`:
    mismatched to the rewrite shortlist and too close to the killed geometry
    branch

## Conclusion

- Outcome: `succeeded`
- Step implication:
  the branch now has one source-supported architecture and one named bad term
  concrete enough for a frozen protocol and bounded rewrite-family audit.
