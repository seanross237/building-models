# Exploration 002 Report

## Goal

Fix the compatible solution class, theorem-hypothesis constraints, and one
frozen localization protocol for the architecture selected in
`exploration-001`, so later rewrite audits compare candidates inside the same
weak-solution package with the same cutoff, projection, and commutator
bookkeeping.

## Method

- Read the selected architecture memo from `exploration-001`.
- Read the CKN and Vasseur architecture files for the weak-solution package and
  cutoff bookkeeping.
- Cross-check the chain discipline and the mission-wide negative boundaries.

## Operational Note

- [VERIFIED] The launched explorer session created only a scaffold in this
  environment. The strategizer completed the compatibility memo directly from
  the anchored local materials.

## Findings

### 1. Solution class

- [VERIFIED] The local-energy architecture in CKN is built on **suitable weak
  solutions**:
  Leray-Hopf energy-class solutions together with the local energy inequality.
  Source:
  - `missions/navier-stokes/library-inbox/ckn-1982-proof-architecture.md`
- [VERIFIED] Vasseur's proof also stays in the suitable weak / Leray-Hopf world
  even though it changes the localization mechanism.
  Source:
  - `missions/navier-stokes/library-inbox/vasseur-2007-proof-architecture.md`
- [INFERRED] Correct solution class for this audit:
  `suitable weak solutions in the Leray-Hopf energy class, with the local
  energy inequality available`
- [INFERRED] Reason:
  the chosen bad term `I_flux[φ]` lives inside the local energy inequality, so
  weakening to mere distributional weak solutions would drop the architecture,
  while strengthening to mild/classical solutions would smuggle in extra
  regularity not granted by the branch.

### 2. Theorem-hypothesis compatibility constraints

- [VERIFIED] The audit must preserve:
  - divergence-free velocity,
  - the LEI package,
  - and the standard energy-class regularity
    `u ∈ L^∞_t L^2_x ∩ L^2_t H^1_x`
  with pressure available in the suitable-weak-solution sense.
  Sources:
  - `missions/navier-stokes/library-inbox/ckn-1982-proof-architecture.md`
  - `missions/navier-stokes/library-inbox/vasseur-2007-proof-architecture.md`
- [VERIFIED] The mission record forbids claiming progress by switching to a
  different phase space or by silently importing stronger regularity than the
  inherited architecture starts with.
  Sources:
  - `missions/beyond-de-giorgi/planning-runs/run-003/judgments/chain-01.md`
  - `missions/beyond-de-giorgi/planning-runs/run-003/attacks/chain-01.md`
- [INFERRED] Non-negotiable compatibility rule:
  every rewrite must still be interpretable inside the same suitable-weak
  local-energy setting before and after localization. If a candidate only
  becomes exact or useful after upgrading regularity, replacing LEI by a
  vorticity-only package, or moving to a different closure scheme, it is not a
  candidate in this branch.

### 3. First explicit circularity / package-mismatch risk

- [INFERRED] The first explicit package-mismatch risk is:
  treating projected or Lamb-vector identities as if they remain exact **after
  localization**.
- [VERIFIED] The chain judgment says the whole point of the branch is to freeze
  where projection and commutator costs land before comparing candidates.
  Source:
  - `missions/beyond-de-giorgi/planning-runs/run-003/judgments/chain-01.md`
- [VERIFIED] The planning attacks also warn that exact rewrites of the same
  quadratic term generally collapse back to the same structure once cutoff,
  projection, and commutator bookkeeping are restored.
  Source:
  - `missions/beyond-de-giorgi/planning-runs/run-003/attacks/chain-01.md`
- [INFERRED] So the branch would become circular if it counted
  `P[(u·∇)u] = -P(u×ω)` or a vorticity-form identity as a gain before paying
  the cost of commuting projection or Biot-Savart machinery past the fixed
  cutoff package.

### 4. Frozen localization protocol

- [VERIFIED] The CKN local-energy package gives the cleanest explicit cutoff
  discipline in the local record:
  one parabolic cylinder with one nonnegative smooth space-time cutoff,
  derivatives of size `1/r` and `1/r^2`, and the localized balance written
  directly against that cutoff.
  Source:
  - `missions/navier-stokes/library-inbox/ckn-1982-proof-architecture.md`
- [INFERRED] Frozen protocol:
  - region:
    one parabolic cylinder
    `Q_r(x_*, t_*) = B_r(x_*) × (t_* - r^2, t_*)`
  - cutoff:
    one standard `φ ∈ C_c^∞(Q_r)`, `0 ≤ φ ≤ 1`, `φ ≡ 1` on the inner
    half-cylinder, with
    `|∇φ| ≤ C/r` and `|∂_t φ| + |Δφ| ≤ C/r^2`
  - target estimate:
    the local-energy balance with fixed bad term
    `I_flux[φ] = ∬ (|u|^2 + 2p) u · ∇φ`
  - bookkeeping rule:
    every candidate starts from the same `I_flux[φ]` target and pays all
    resulting localization costs in that same package
  - projection / CZ rule:
    if a candidate uses Helmholtz projection or pressure reconstruction after
    localization, the resulting nonlocal and commutator costs are charged to
    that candidate rather than hidden in the baseline
  - vorticity / Biot-Savart rule:
    if a candidate rewrites through `ω`, all Biot-Savart reinsertions and
    cutoff-commutation costs are charged explicitly in the same ledger.

### 5. Why this is the fairest protocol

- [INFERRED] It is the least adapted protocol that still keeps the chosen
  architecture visible. No candidate gets to choose a different localization
  region or a more favorable operator placement.
- [INFERRED] It respects the chain's demand that "where the localization cost
  lands" be fixed before comparing candidates.
- [INFERRED] It keeps the branch inside the suitable-weak LEI setting and
  prevents a rewrite from winning only because the surrounding protocol was
  changed.

### 6. Illegitimate mid-branch protocol changes

- [INFERRED] Later work would be illegitimate if it:
  - moves the cutoff inside a projector or singular integral for only one
    candidate without charging the resulting commutator;
  - changes the region from the fixed parabolic cylinder to a candidate-adapted
    or geometry-adapted region;
  - or upgrades the solution class to make a rewrite look cleaner.

## Decision Memo

- [VERIFIED] The architecture can be stated honestly in one stable weak-solution
  package. No compatibility kill is triggered.
- [INFERRED] Fixed solution class:
  `suitable weak solutions in the Leray-Hopf energy class, with LEI`
- [INFERRED] Fixed localization protocol:
  one standard CKN-style parabolic cutoff on one cylinder, with all
  projection/CZ/Biot-Savart commutator costs charged candidate-by-candidate in
  the same localized balance.
- [INFERRED] First package-mismatch risk:
  pretending projected/Lamb-vector or vorticity identities remain exact after
  localization without paying the operator-commutator cost.

## Conclusion

- Outcome: `succeeded`
- Step implication:
  later candidate comparisons can now inherit one explicit weak-solution
  package and one frozen cutoff/projection protocol rather than changing
  assumptions midstream.
