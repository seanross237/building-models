# Exploration 003 Summary

## Goal

Determine whether a harmonic far-field pressure component on a local cylinder can make the bad local pressure pairing genuinely `U_k`-dependent, or whether harmonicity only improves constants/oscillation while leaving the coefficient fixed at energy scale.

## What Was Tried

- Built the smallest explicit near/far model on `Q = B_1 x (-1,0)`.
- Took `p_near = 0` and defined `p_far` as the Newtonian potential of the exterior shell measure `(1/2) sigma_2` on `|y|=2`.
- Paired `p_far` against the explicit local test function `psi(x,t) = 1_{(-1,0)}(t) (1-|x|^2)_+^2`.
- Introduced a local amplitude family `u_A = A e_1` so the local energy-scale quantity satisfies `U(A) = A^2 (32 pi / 105)`.
- Verified the shell model numerically with [code/harmonic_shell_model.py](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/instances/far-field-pressure-harmonic-loophole/strategies/strategy-001/explorations/exploration-003/code/harmonic_shell_model.py).

## Outcome

[VERIFIED] The model is decisively negative: `harmonicity does not create U-dependence`.

[VERIFIED] The exterior shell gives `p_far = 1` exactly on `B_1`, so `Delta p_far = 0` on `Q` and the pairing is
`integral integral_Q p_far psi = 32 pi / 105`.

[VERIFIED] That pairing is independent of the local amplitude parameter `A`, while `U(A) -> 0` as `A -> 0`. For every `alpha > 0`,
`(integral integral_Q p_far psi) / U(A)^alpha -> infinity`,
so no positive `U`-power can be forced by harmonicity alone.

## Verification Scorecard

- `[VERIFIED]` 11
- `[COMPUTED]` 2
- `[CHECKED]` 4
- `[CONJECTURED]` 0

## Key Takeaway

[CHECKED] The exact obstruction is already visible in the constant harmonic mode: the coefficient is determined by exterior data, not by the local De Giorgi scale. Harmonic regularity can reduce oscillation, but even zero oscillation does not manufacture a `U_k` factor.

## Proof Gaps Or Computation Gaps

- No gap remains for the main verdict in this model.
- I did not build a more elaborate affine-mode or Wolf-style variant because the constant shell mode already settles the coefficient question cleanly.
- The pairing tested is an explicit local test-function pairing, not the full literal Vasseur `P_{k21}` expression; that extra complexity is unnecessary once the constant harmonic countermodel is available.

## Unexpected Findings

- The strongest possible harmonic improvement, namely `osc_Q p_far = 0`, still gives no `U`-dependence at all.
- This means any surviving near/far loophole would have to come from changing which pressure piece is paired with the De Giorgi object, not from harmonicity of `p_far` itself.
