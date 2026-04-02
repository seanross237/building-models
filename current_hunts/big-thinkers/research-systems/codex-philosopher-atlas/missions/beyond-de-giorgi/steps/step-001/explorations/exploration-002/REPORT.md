# Exploration 002 Report

## Goal

Test the short list of pressure-relevant candidate NS-specific ingredients against the Tao 2016 averaged-Navier-Stokes filter and determine whether any nontrivial version of the harmonic-tail branch survives.

Allowed candidates only:

- exact algebraic form of `u · ∇u`
- pressure-Hessian / tensor structure tied to `∂_i∂_j p = R_i R_j(u_i u_j)`
- vorticity or strain geometry only if it directly affects the surviving far-field pairing

## Required Anchors Consulted

- `missions/beyond-de-giorgi/MISSION.md`
- `missions/beyond-de-giorgi/CHAIN.md`
- `missions/beyond-de-giorgi/planning-runs/run-001/mission-context.md`
- `missions/beyond-de-giorgi/planning-runs/run-001/attacks/chain-01.md`
- `missions/vasseur-pressure/steps/step-001/RESULTS.md`
- `missions/vasseur-pressure/steps/step-002/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-001/explorations/exploration-002/GOAL.md`

## Working Standard

Only count a candidate as surviving if it can plausibly act on the actual far-field coefficient problem

`I_p^far <= C_far 2^{12k/5} U_k^{6/5},  C_far ~ ||u||_{L^2}^2 / r_k^3`

rather than merely restating generic harmonic regularity of `p_far`.

## Findings

### A. Exact Obstruction To Screen

[VERIFIED] From the copied `vasseur-pressure` material, the live pressure contribution is

`I_p = -∬ p div(v_k φ_k^2 ê)`

with expansion

`div(v_k φ_k^2 ê) = (ê·∇v_k) φ_k^2 + 2 v_k φ_k (ê·∇φ_k) + v_k φ_k^2 div ê`

and the main error term

`I_p^far,main = - 2 ∬ p_far v_k φ_k (ê·∇φ_k)`.

Source trail inside the repo:

- `missions/vasseur-pressure/library-inbox/exploration-002-pressure-dissection-de-giorgi.md`
- `missions/vasseur-pressure/steps/step-001/RESULTS.md`
- `missions/beyond-de-giorgi/planning-runs/run-001/attacks/chain-01.md`

[VERIFIED] The earlier pressure mission already isolated the quantitative obstruction:

`I_p^far <= C_far 2^{12k/5} U_k^{6/5}`

with

`C_far ~ ||p_far||_{L^∞(Q_k)} ~ ||u||_{L^2}^2 / r_k^3`.

The `U_k` power is already superlinear. The failure is coefficient-side, not exponent-side. Any real gain must make the operative coefficient smaller than the fixed energy-class scale, or otherwise make the full far-field contribution summably smaller than `O(E_0)`.

[INFERRED] The test structure already kills constant pressure modes but not affine ones.

- If `p_far = c`, then
  `I_p^far = -c ∬ div(v_k φ_k^2 ê) = 0`
  by spatial integration by parts, since `φ_k` gives compact spatial support.
- If `p_far = a·x + c`, then
  `I_p^far = - ∬ (a·x) div(v_k φ_k^2 ê) = ∬ a·(v_k φ_k^2 ê)`,
  which is generically nonzero.

So the branch is not asking for better control of constants already annihilated by the test. It is asking whether NS-specific structure can shrink the surviving affine-or-higher harmonic moments that couple to `v_k φ_k^2 ê`, equivalently the actual coefficient behind `I_p^far`.

[VERIFIED] This is exactly the chain standard in `missions/beyond-de-giorgi/CHAIN.md`: do not count nicer harmonicity as progress unless it acts on the surviving pairing itself and reduces the actual bad coefficient.

### B. Tao-Gate Screen By Candidate

[VERIFIED] The mission files state the Tao filter as follows: averaged NS preserves the energy identity, divergence-free structure, and standard Calderon-Zygmund / Littlewood-Paley / Sobolev / harmonic-analysis estimates. Therefore generic harmonic-tail regularity is disqualified at the start.

#### Candidate 1. Exact algebraic form of `u · ∇u`

Verdict: `fails Tao gate`

Reasoning:

- [VERIFIED] The pressure-side obstruction no longer appears as a raw transport term. After decomposition it is the harmonic tail pairing `I_p^far`, controlled through `p_far`.
- [VERIFIED] Local planning notes for Chain 02 say Lamb-vector, vorticity, and Helmholtz-projected rewrites are mostly equivalent repackagings of the same quadratic interaction before truncation/localization, while the real loss appears after truncation/localization.
- [INFERRED] For this branch, merely rewriting `u·∇u` does not by itself act on the surviving affine moments of `p_far`. Once the tail is encoded through the harmonic pressure field, the coefficient problem is still a remote-source moment problem of size `O(||u||_2^2 / r_k^3)`.
- [INFERRED] Tao's averaged model is designed to preserve exactly this harmonic-analysis-level quadratic control. Without a new estimate showing that the exact NS algebra shrinks the surviving pressure moment, the algebraic form is not a live coefficient lever.

Conclusion:

This candidate may matter for a different reformulation branch, but for the harmonic-tail pressure branch it does not survive Step 1. It is an identity-level repackaging, not a demonstrated mechanism on `C_far`.

#### Candidate 2. Pressure-Hessian / tensor structure tied to `∂_i∂_j p = R_i R_j(u_i u_j)`

Verdict: `unclear but testable`

Reasoning:

- [VERIFIED] This is the only candidate on the short list that is naturally attached to the pressure-side object itself rather than to a parallel formulation.
- [VERIFIED] The mission and planning notes explicitly single out the exact pressure-tensor relation as a plausible thing averaging may destroy.
- [INFERRED] In principle, an exact tensor statement could matter if it forced cancellations in the remote-shell moments generating the affine-or-higher harmonic part of `p_far` on `Q_k`.
- [VERIFIED] But the current chain-01 attack memo already warns that `∂_i∂_j p = R_i R_j(u_i u_j)` is not progress by itself. If it stays only a representation formula or Calderon-Zygmund repackaging, then it remains inside Tao-preserved structure.
- [INFERRED] No local repository result currently identifies a concrete estimate-level mechanism by which this tensor identity shrinks the actual bad coefficient rather than restating nonlocal pressure generation.

Conclusion:

This candidate is not dead in the abstract, but it does not currently keep the harmonic-tail branch alive. What survives is only a testable possibility: one would have to build an explicit remote-shell or moment-cancellation computation showing tensor structure reduces the surviving affine-or-higher harmonic coefficients. Without that, it is not a green light.

#### Candidate 3. Vorticity or strain geometry, only if it directly affects the surviving far-field pairing

Verdict: `fails Tao gate`

Reasoning:

- [VERIFIED] The mission treats vorticity geometry as a genuinely NS-specific axis in general.
- [VERIFIED] But the pressure-side goal is narrower: the candidate only counts if it directly changes the surviving far-field pressure pairing.
- [VERIFIED] Local planning notes for the geometry branch say local Beltrami alignment controls the Lamb vector, while the dangerous objects for geometry are vortex stretching and nonlocal strain; exterior contributions remain unresolved.
- [INFERRED] That same nonlocality is fatal here. A local geometry statement does not directly control the remote-shell contribution that fixes `C_far`, and can at best touch a local subpiece while leaving the exteriorly generated harmonic tail unchanged.

Conclusion:

Geometry may belong to a separate beyond-De-Giorgi route, but for this pressure-side harmonic-tail branch it does not provide a direct handle on the actual surviving coefficient. It therefore fails the gate for the present branch.

### C. Dead Ends / Failed Routes

[VERIFIED] Generic harmonic regularity is a dead end here. Harnack, local `H^1`, Campanato, derivative decay, harmonic polynomial approximation, and related elliptic regularity are exactly the kind of tools Tao's averaged model preserves. The chain-01 attack memo says these should be presumed guilty immediately unless attached to an NS-specific identity that acts on `C_far`.

[VERIFIED] The earlier `vasseur-pressure` mission already killed the main pressure upgrades inside the De Giorgi architecture:

- H^1-BMO duality fails.
- Atomic decomposition fails.
- Interpolation fails.
- Bogovskii/localization worsens the problem.

[INFERRED] For the present exploration, this means there is no residual credit for merely restating the harmonic tail in a nicer norm. Any surviving candidate must modify the remote moment structure of `p_far` itself. None currently does so at estimate level.

Dead end encountered in this exploration:

- I searched the repository for a more explicit local note on Tao's averaged model beyond the mission summaries and found none inside the mission materials. I therefore used the mission's preserved-structure list as the operative Tao filter. That is adequate for this branch because the question is not a literature reconstruction; it is whether the proposed mechanism is generic harmonic analysis or an NS-specific coefficient lever.

### D. Step Recommendation

Recommendation: trigger the negative-result track for Chain 01 Step 1.

Reason:

- No candidate earned `survives Tao gate`.
- The exact-bilinear candidate fails because it does not act on the surviving pressure coefficient.
- The geometry candidate fails because it does not directly control the nonlocal far-field pairing.
- The pressure-tensor candidate remains only `unclear but testable`, but not in a way that justifies continuing the harmonic-tail branch as currently framed.

Operational consequence:

- Do not green-light a broad Step 2 harmonic-tail program.
- At most, preserve one narrow follow-up question for a different tensor-focused branch:
  can the exact pressure-tensor structure force cancellation in the remote-shell moments that generate the affine-or-higher harmonic tail on `Q_k`?
- Absent such a moment-level mechanism, the honest conclusion is that the harmonic-tail loophole is Tao-compatible and should be downgraded.
