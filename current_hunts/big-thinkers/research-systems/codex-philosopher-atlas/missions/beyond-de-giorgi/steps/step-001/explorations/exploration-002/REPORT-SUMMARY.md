# Exploration 002 Summary

## Goal

Test the short list of pressure-relevant NS-specific ingredients against the Tao 2016 averaged-Navier-Stokes filter and decide whether any nontrivial version of the harmonic-tail pressure branch survives.

## What Was Tested

- Reconstructed the live far-field pressure pairing from the copied `vasseur-pressure` materials:
  `I_p^far = -∬ p_far div(v_k φ_k^2 ê)`, with main live term `-2 ∬ p_far v_k φ_k (ê·∇φ_k)`.
- Checked which pressure modes the test structure already kills:
  constants are annihilated, affine modes generally survive.
- Screened only the allowed candidates:
  - exact algebraic form of `u · ∇u`
  - pressure-Hessian / tensor structure tied to `∂_i∂_j p = R_i R_j(u_i u_j)`
  - vorticity or strain geometry only if it directly affects the surviving far-field pairing

## Outcome

`failed` as a live harmonic-tail continuation, in the sense required by the chain.

Candidate verdicts:

- exact algebraic form of `u · ∇u`: `fails Tao gate`
- pressure-Hessian / tensor structure: `unclear but testable`
- vorticity / strain geometry for this pressure pairing: `fails Tao gate`

No candidate earned `survives Tao gate`.

## One Key Takeaway

The pressure-side loophole is coefficient-side, not regularity-side: the only thing that would matter is a mechanism shrinking the surviving affine-or-higher harmonic moments behind

`C_far ~ ||u||_{L^2}^2 / r_k^3`,

and none of the screened candidates currently does that at estimate level.

## Leads Worth Pursuing

- Preserve one narrow follow-up question only:
  can the exact pressure-tensor structure force cancellation in the remote-shell moments that generate the affine-or-higher harmonic tail on `Q_k`?
- If pursued, that question fits better in a tensor/eigenstructure branch than in continued harmonic-tail norm-shopping.

## Unexpected Findings

- The pressure test structure automatically kills constant modes, so the surviving far-field issue is already a moment problem for affine-or-higher harmonic content.
- This makes generic harmonic smoothing even less relevant than it first appears: it cannot touch the live coefficient unless it is paired with a genuinely NS-specific moment cancellation.

## Computations Worth Doing Later

- An explicit remote-shell model or multipole-style calculation for the pressure-tensor candidate, testing whether exact NS tensor structure can cancel the surviving affine moment on the inner cylinder.

## Step Decision

Step 2 should be downgraded, not green-lit as a broad harmonic-tail continuation. The honest Step 1 output is a negative-result memo with, at most, one narrow tensor-side follow-up question.
