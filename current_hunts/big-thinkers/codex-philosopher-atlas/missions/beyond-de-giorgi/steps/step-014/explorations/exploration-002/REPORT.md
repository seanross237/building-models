# Exploration 002 Report

## Goal

For the two active Step-2 candidates, derive the full exact evolution, the
localized packet that actually interfaces with the frozen LEI burden
`I_flux[phi]`, and the visible debt ledger.

## Method

- Fix the inherited suitable-weak / LEI setting and one shared CKN-style
  cutoff from `step-013`.
- Use the Step-001 slate:
  `Lamb-vector / projected` and `vorticity / Biot-Savart`.
- Reuse the fixed exact-rewrite debt rules already stored in the local library.
- Derive the exact equations directly from the Navier-Stokes system, then read
  the localized consequences back through the frozen LEI bundle rather than
  switching to a different bad term.

## Operational Note

- [VERIFIED] The wrapper-launched explorer session did not land its sentinel
  during a bounded wait.
- [VERIFIED] The strategizer therefore completed this report directly from the
  same repository-local evidence and exact derivations.

## Source Log

- `missions/beyond-de-giorgi/steps/step-014/explorations/exploration-002/GOAL.md`
- `missions/beyond-de-giorgi/library-inbox/step-014-exploration-001-candidate-slate.md`
- `missions/beyond-de-giorgi/steps/step-013/RESULTS.md`
- `missions/beyond-de-giorgi/library-inbox/step-005-exploration-002-compatibility-localization-protocol.md`
- `missions/beyond-de-giorgi/library-inbox/step-006-exploration-001-tao-screen-divergence-lamb.md`
- `missions/beyond-de-giorgi/library-inbox/step-006-exploration-002-tao-screen-vorticity-biot-savart.md`
- `missions/beyond-de-giorgi/steps/step-005/explorations/exploration-003/REPORT.md`
- `library/factual/exact-rewrite-obstruction-audit/projected-and-vorticity-rewrites-must-pay-localization-debt.md`
- `library/factual/exact-rewrite-obstruction-audit/every-rewrite-must-stay-inside-the-same-localized-lei-package.md`
- `library/factual/exact-rewrite-obstruction-audit/freeze-one-ckn-style-parabolic-cutoff-protocol-for-the-rewrite-audit.md`
- `library/factual/exact-rewrite-architecture-screening/the-localized-lei-cutoff-flux-bundle-is-the-fixed-bad-term-for-the-audit.md`
- `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`

## Fixed Audit Frame

- [VERIFIED] Frozen theorem-facing target:
  `I_flux[phi] = ∬_{Q_r} (|u|^2 + 2p) u · ∇phi`.
- [VERIFIED] Frozen solution class:
  suitable weak solutions in the Leray-Hopf energy class with LEI.
- [VERIFIED] Frozen localization protocol:
  one CKN-style parabolic cylinder and one smooth cutoff `phi`.
- [VERIFIED] Debt rule:
  any projection, Calderon-Zygmund, Biot-Savart, or cutoff commutator cost
  created after localization belongs to the candidate's own ledger.

## Findings

### 1. Active candidate: `Lamb-vector / Helmholtz-projected form`

#### Exact equation packet

- [INFERRED] Start from exact Navier-Stokes:
  `∂_t u - Δu + (u · ∇)u + ∇p = 0`, `div u = 0`.
- [INFERRED] Use the exact identity
  `(u · ∇)u = ∇(|u|^2 / 2) - u × ω`, `ω = curl u`.
- [INFERRED] This gives the exact reformulated velocity equation
  `∂_t u - Δu - u × ω + ∇π = 0`,
  where `π = p + |u|^2 / 2`.
- [INFERRED] Applying Helmholtz projection yields
  `∂_t u - Δu - P(u × ω) = 0`.
- [INFERRED] Exact-NS structure exposed here:
  the quadratic nonlinearity is split into
  an algebraically orthogonal Lamb-vector part and a gradient remainder.
- [INFERRED] Generic packaging already present here:
  the passage from the gradient piece to `P(u × ω)` is a nonlocal projector
  step, not new Navier-Stokes dynamics.
- [INFERRED] The exact re-entry identity is
  `(I - P)(u × ω) = ∇π`.
  This is the precise place where the apparently removed gradient survives.

#### Localized equation and debt ledger

- [INFERRED] Test the exact equation against `u phi` inside the frozen CKN
  cutoff protocol.
- [INFERRED] The pointwise orthogonality
  `u · (u × ω) = 0`
  removes the Lamb-vector piece from the raw energy pairing.
- [INFERRED] But the remaining gradient term becomes
  `∇π · (u phi) = - π u · ∇phi`
  because `div u = 0`.
- [INFERRED] Since `π = p + |u|^2 / 2`, the localized flux is exactly
  `((|u|^2 / 2) + p) u · ∇phi`,
  which is the same frozen LEI cutoff-flux bundle up to the standard factor-2
  normalization.
- [INFERRED] If one insists on localizing the projected equation instead of the
  unprojected equation, the same burden reappears as a projector commutator:
  `∬ phi u · P(u × ω)
   = ∬ P(phi u) · (u × ω)`.
  Since
  `P(phi u) = phi u - ∇Δ^{-1} div(phi u)
            = phi u - ∇Δ^{-1}(u · ∇phi)`,
  the first term still vanishes by `u · (u × ω) = 0`, leaving
  `∬ phi u · P(u × ω)
   = - ∬ ∇Δ^{-1}(u · ∇phi) · (u × ω)`.
- [INFERRED] Comparing the projected and unprojected calculations shows the
  exact re-entry mechanism:
  `- ∬ ∇Δ^{-1}(u · ∇phi) · (u × ω)
   = ∬ π u · ∇phi`.
- [INFERRED] So the localized packet does act on the full frozen burden, but it
  does so only by restoring the same transport-plus-pressure bundle rather than
  replacing it with a smaller object.

#### Visible debt

- [INFERRED] Pressure re-entry debt:
  the apparently removed gradient returns immediately through
  `π = p + |u|^2 / 2`.
- [INFERRED] Cutoff commutator debt:
  localizing after projection creates `phi`-projection commutators and the
  usual diffusion/cutoff terms.
- [INFERRED] Vector reconstruction debt:
  the candidate uses `ω = curl u`, and the projected package depends on the
  nonlocal Helmholtz projector.
- [INFERRED] Admissibility debt:
  in the suitable-weak / LEI class, the projected form must be interpreted
  through distributional or mollified arguments; it is not a free pointwise
  replacement inside the localized inequality.
- [INFERRED] Locality loss:
  `P` is nonlocal, so the clean global decomposition is not a clean local
  decomposition once `phi` is inserted.
- [INFERRED] Full burden or surrogate:
  the raw projected Lamb packet acts only on the surrogate object
  `P(u x omega)`.
  It reaches the full frozen burden only after exact pressure/projection
  re-entry restores `pi u . ∇phi`.

### 2. Active candidate: `vorticity transport / Biot-Savart form`

#### Exact equation packet

- [INFERRED] Define `ω = curl u`.
- [INFERRED] Taking curl of Navier-Stokes gives the exact vorticity equation
  `∂_t ω - Δω + (u · ∇)ω - (ω · ∇)u = 0`.
- [INFERRED] Equivalently,
  `∂_t ω - Δω + (u · ∇)ω = Sω`,
  where `S = (∇u + ∇u^T)/2`.
- [INFERRED] Velocity reconstruction is exact:
  `u = ∇ × (-Δ)^(-1) ω`,
  and `∇u` is a Calderon-Zygmund image of `ω`.
- [INFERRED] Exact-NS structure exposed here:
  transport, diffusion, stretching, and incompressible reconstruction are all
  explicit in the `(ω, u)` package.
- [INFERRED] Generic packaging already present here:
  passing from `ω` back to `u` or `∇u` is entirely singular-integral
  reconstruction.

#### Localized equation and debt ledger

- [INFERRED] The native vorticity equation does not itself produce the frozen
  LEI flux bundle.
  To touch the Step-013 theorem-facing burden, one must reinsert
  `u = BS[ω]` into the same localized LEI packet.
- [INFERRED] Formally, the candidate rewrites
  `I_flux[phi]` as
  `∬ (|BS[ω]|^2 + 2 p[ω]) BS[ω] · ∇phi`,
  with pressure still determined by
  `-Δp = ∂_i ∂_j (u_i u_j)`,
  hence by a double Riesz transform of quadratic expressions in `BS[ω]`.
- [INFERRED] The first exact cutoff decomposition already exposes the
  nonlocality:
  `phi u = phi BS[ω] = BS[phi ω] + [phi, BS]ω`.
  Likewise,
  `phi p = phi R_i R_j(u_i u_j)
         = R_i R_j(phi u_i u_j) + [phi, R_i R_j](u_i u_j)`.
- [INFERRED] So the localized packet touches the full frozen burden only after
  full velocity and pressure reconstruction.
  Before that, the vorticity equation acts on a surrogate object, not on the
  theorem-facing LEI bundle itself.
- [INFERRED] This is why the native localized vorticity identity is not the
  right packet for this branch: it naturally produces transport/stretching
  terms for `ω`, whereas the frozen burden is still a velocity-pressure flux
  against `∇phi`.

#### Visible debt

- [INFERRED] Pressure re-entry debt:
  pressure remains quadratic in the reconstructed velocity and re-enters by a
  nonlocal Riesz-transform package.
- [INFERRED] Cutoff commutator debt:
  `phi` does not commute with Biot-Savart or the pressure reconstruction
  operators, so localization produces interior/exterior splits and
  commutators.
- [INFERRED] Vector reconstruction debt:
  every velocity-side factor in the frozen LEI bundle must be recovered from
  `ω` through Biot-Savart.
- [INFERRED] Admissibility debt:
  the suitable-weak / LEI class does not grant a standalone vorticity closure
  strong enough to replace the inherited local-energy architecture.
- [INFERRED] Locality loss:
  the route is intrinsically nonlocal once one insists on acting on the full
  `I_flux[phi]` object.

### 3. Dead-end control

- [INFERRED] I did not promote a localized vorticity-energy or stretching test
  to the main packet, because that would switch the branch target away from the
  frozen LEI flux bundle.
- [INFERRED] I also did not treat the global projected Lamb identity as already
  localized. The exact point of this audit is that projection and
  singular-integral bookkeeping must be restored after the cutoff is fixed.

### 4. Shared equation-level conclusion

- [INFERRED] Both active candidates admit exact full equations precise enough
  for Step 2.
- [INFERRED] Both localized packets still meet the same frozen burden.
- [INFERRED] Neither localized packet isolates a new theorem-facing bad term;
  both return to the full `I_flux[phi]` ledger after their own nonlocal and
  commutator costs are charged.
- [INFERRED] The crucial distinction is how quickly the debt appears:
  for the Lamb/projected route, pressure re-entry is immediate;
  for the vorticity/Biot-Savart route, reconstruction and nonlocality dominate
  before the candidate can even speak the frozen burden currency.

## Localized Debt Table

| candidate | full exact evolution | localized interface with `I_flux[phi]` | visible debt | acts on full burden or surrogate? |
| --- | --- | --- | --- | --- |
| `Lamb-vector / projected` | `[INFERRED]` `∂_t u - Δu - u × ω + ∇(p + |u|^2/2) = 0`, or projected `∂_t u - Δu - P(u × ω) = 0` | `[INFERRED]` dot with `u phi`; orthogonality kills `u × ω`, but `∇(p + |u|^2/2)` returns the same localized flux bundle | `[INFERRED]` pressure re-entry, projection/cutoff commutators, projector nonlocality, admissibility | `[INFERRED]` full frozen burden, but only by restoring the same bundle |
| `vorticity / Biot-Savart` | `[INFERRED]` `∂_t ω - Δω + (u · ∇)ω - (ω · ∇)u = 0`, with `u = BS[ω]` | `[INFERRED]` rewrite velocity and pressure factors inside the same LEI flux through singular-integral reconstruction | `[INFERRED]` Biot-Savart reconstruction, pressure reconstruction, cutoff commutators, admissibility, locality loss | `[INFERRED]` only reaches the full burden after full reconstruction; native equation alone acts on a surrogate |

## Conclusion

- Outcome: `succeeded`
- [INFERRED] Each active candidate now has an exact equation sheet and a
  localized debt ledger.
- [INFERRED] The equations already expose the likely obstruction:
  neither candidate stays cleaner than the inherited LEI bundle once the
  localized bookkeeping is restored.
