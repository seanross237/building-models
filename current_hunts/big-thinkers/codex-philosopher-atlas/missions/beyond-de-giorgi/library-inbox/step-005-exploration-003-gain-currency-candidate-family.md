# Exploration 003 Report

## Goal

Choose one bookkeeping currency of gain, define the bounded exact-rewrite
family, and state the novelty / Step-2-readiness memo for `step-005`.

## Method

- Inherit the architecture and bad-term choice from `exploration-001`.
- Inherit the weak-solution and localization protocol from `exploration-002`.
- Read the chain-01 planning, attack, and judgment files together with the
  mission background and the prior negative branches.

## Findings

### 1. Gain currency

- [VERIFIED] The chain allows only one gain currency chosen in advance:
  derivative count, integrability improvement, coefficient shrinkage, or a
  strictly weaker hypothesis in the same closure scheme.
  Sources:
  - `missions/beyond-de-giorgi/CHAIN.md`
  - `missions/beyond-de-giorgi/planning-runs/run-003/refined/chain-01.md`
- [INFERRED] The honest choice for this branch is:
  `coefficient shrinkage in the fixed localized LEI balance`
- [INFERRED] More explicitly:
  a candidate only counts as a gain if it shrinks the effective cost of the
  frozen bad term
  `I_flux[φ] = ∬ (|u|^2 + 2p) u · ∇φ`
  in the same cutoff protocol and same weak-solution package.
- [INFERRED] Reason:
  derivative-count and exponent-improvement language is too easy to game at the
  identity level. The chain judgment already warns that progress must be
  defined at the localized estimate level, not by a prettier formula.

### 2. Bounded candidate family

- [VERIFIED] The local chain materials repeatedly identify the natural exact
  rewrite shortlist for this branch as:
  `Lamb-vector or projected form`, `vorticity transport form`, and one
  additional tightly justified exact rewrite.
  Sources:
  - `missions/beyond-de-giorgi/planning-runs/run-003/selected/chain-01.md`
  - `missions/beyond-de-giorgi/planning-runs/run-003/attacks/chain-01.md`
  - `missions/beyond-de-giorgi/planning-runs/run-001/selected/chain-02.md`
- [INFERRED] Final bounded exact-rewrite family:
  1. `divergence / stress form`
     \[
     (u \cdot \nabla)u = \nabla \cdot (u \otimes u)
     \quad \text{when } \nabla \cdot u = 0
     \]
  2. `Lamb-vector / Helmholtz-projected form`
     \[
     (u \cdot \nabla)u
     =
     \nabla(|u|^2/2) - u \times \omega,
     \qquad
     \mathbb{P}((u \cdot \nabla)u) = -\mathbb{P}(u \times \omega)
     \]
  3. `vorticity transport / Biot-Savart form`
     use the exact vorticity-side rewriting of the same quadratic interaction,
     with `u` re-expressed through `ω` only if the full Biot-Savart cost is
     paid back in the same localized ledger.

### 3. Intended leverage point and first cosmetic risk

#### Candidate 1. Divergence / stress form

- [INFERRED] Intended leverage point:
  put the quadratic interaction into divergence form before testing against the
  fixed cutoff, hoping to relocate the derivative onto `φ` in a cleaner way.
- [INFERRED] First obvious cosmetic risk:
  after integration by parts the same cutoff-flux burden reappears as a stress
  interaction against `∇φ`, so nothing improves except presentation.

#### Candidate 2. Lamb-vector / Helmholtz-projected form

- [INFERRED] Intended leverage point:
  isolate the gradient component and expose a potentially more first-order
  looking nonlinear piece.
- [VERIFIED] The mission background already records that exact Beltrami kills
  the Lamb-vector side but that this cancellation is highly fragile.
  Source:
  - `missions/beyond-de-giorgi/MISSION.md`
- [INFERRED] First obvious cosmetic risk:
  the gradient part simply reappears inside pressure / projection bookkeeping,
  while localization and projection commutators recreate the same CZ-type cost.

#### Candidate 3. Vorticity transport / Biot-Savart form

- [INFERRED] Intended leverage point:
  expose the exact vorticity-side structure of the same quadratic interaction
  and see whether the localized balance gains from that relocation.
- [VERIFIED] The mission background already warns that the vorticity
  formulation also lands at the same `beta = 4/3` barrier and that the
  quadratic obstruction is not removed merely by moving to `ω`.
  Source:
  - `missions/beyond-de-giorgi/MISSION.md`
- [INFERRED] First obvious cosmetic risk:
  the rewrite drifts into a different architecture or repays the same cost via
  Biot-Savart nonlocality and stronger regularity demands.

### 4. Hybrid route decision

- [INFERRED] No same-target hybrid route should be admitted at Step 1.
- [INFERRED] Reason:
  the obvious hybrids in the local record are pressure-tensor or geometry-side
  routes, and the chain judgments explicitly warn against letting hybrid
  material silently change branches. At this step, admitting a hybrid would
  blur the fixed architecture more than it would clarify the candidate family.

### 5. Novelty claim

- [VERIFIED] Relative to the De Giorgi sharpness record, the novelty here is
  not "beat `beta = 4/3`." The novelty is a bounded audit of whether exact NS
  rewrites change a fixed localized LEI balance before any De Giorgi recursion
  or Tao optimism is allowed.
  Sources:
  - `missions/beyond-de-giorgi/MISSION.md`
  - `missions/beyond-de-giorgi/planning-runs/run-003/refined/chain-01.md`
- [VERIFIED] Relative to the pressure-route negatives, this branch is no longer
  chasing the far-field coefficient or H^1 pressure upgrades.
  Sources:
  - `missions/beyond-de-giorgi/steps/step-001/RESULTS.md`
  - `missions/vasseur-pressure/steps/step-002/RESULTS.md`
- [VERIFIED] Relative to the killed geometry branch, this branch does not rely
  on tube persistence, direction coherence, or control of full stretching
  `S omega . omega`.
  Source:
  - `missions/beyond-de-giorgi/steps/step-004/RESULTS.md`
- [INFERRED] So the genuinely new claim earned here is narrow:
  the repository now fixes one local-energy architecture, one cutoff-flux bad
  term, one weak-solution package, one localization protocol, and one bounded
  exact-rewrite family for a later Tao screen. That bounded setup did not exist
  in the local record before this step.

### 6. Step-2 readiness

- [INFERRED] The candidate family is concrete enough for Step 2's Tao
  discriminator screen.
- [INFERRED] Reason:
  the architecture, bad term, solution class, localization protocol, gain
  currency, and candidate family are now all explicit and bounded.
- [INFERRED] Important caution:
  the expected baseline is still negative. The planning attacks already make it
  likely that these rewrites collapse once localization/projection bookkeeping
  is paid. But that is now a testable later claim rather than an unstated
  assumption.

## Decision Memo

- [INFERRED] Chosen gain currency:
  `coefficient shrinkage in the fixed localized LEI balance`
- [INFERRED] Final candidate family:
  - divergence / stress form
  - Lamb-vector / Helmholtz-projected form
  - vorticity transport / Biot-Savart form
- [INFERRED] Hybrid route:
  none admitted at Step 1
- [INFERRED] Step-2 readiness:
  `yes, with narrow-claim discipline`

## Conclusion

- Outcome: `succeeded`
- Step implication:
  the branch is now concrete enough to run the Tao screen on a bounded
  candidate table without silently changing architecture or protocol.
