# Executive verdict

[VERIFIED] Verdict: `harmonicity does not create U-dependence`. The minimal exterior-shell model below produces a far-field component `p_far` that is harmonic on the local cylinder `Q`, generated entirely by data outside `Q`, and even constant on `Q`. Its local pairing is a fixed positive number while a local energy-scale quantity `U(A)` can be sent to `0` by varying the local field amplitude. No positive power of `U` can therefore be forced by harmonicity alone.

[CHECKED] This is stronger than a soft obstruction. In this model the harmonic oscillation on `Q` is already identically zero, so Harnack or oscillation control is maximally favorable and still does not move the coefficient off the exterior/energy scale.

# Explicit model

[VERIFIED] Let
`Q = B_1(0) x (-1,0) subset R^3 x R`,
let `G(x) = 1 / (4 pi |x|)` be the Newtonian kernel in `R^3`, and let `sigma_2` be surface measure on the sphere `|y| = 2`. Define the exterior measure
`mu = (1/2) sigma_2`
and the far-field pressure
`p_far(x,t) = integral_{|y|=2} G(x-y) dmu(y)`.

[VERIFIED] Set `p_near = 0`, so `p = p_near + p_far = p_far`. Since the source measure `mu` is supported on `|y|=2`, outside `B_1`, the potential `p_far` is harmonic on `B_1`, hence `Delta p_far = 0` on `Q`.

[VERIFIED] By Newton's shell theorem, the potential of the uniform shell is exactly constant inside the shell:
`p_far(x,t) = 1` for every `|x| < 2`.
In particular `p_far = 1` on all of `Q`.

[COMPUTED] The script [code/harmonic_shell_model.py](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/instances/far-field-pressure-harmonic-loophole/strategies/strategy-001/explorations/exploration-003/code/harmonic_shell_model.py) numerically checks the shell potential at three interior points and gets errors `1.0e-13`, `4.5e-08`, and `3.5e-08`, consistent with the exact constant value `1`.

[VERIFIED] For the local energy scale, take the divergence-free constant family
`u_A(x,t) = A e_1`,
so any local energy-type quantity built from `|u_A|^2` scales like `A^2`. Below I use the explicit weighted local energy
`U(A) = integral integral_Q |u_A|^2 psi dx dt`.

# Pairing computation

[VERIFIED] Choose the explicit nonnegative local test function
`psi(x,t) = 1_{(-1,0)}(t) (1 - |x|^2)_+^2`.
Then
`integral integral_Q p_far psi dx dt = integral integral_Q psi dx dt`
because `p_far = 1` on `Q`.

[VERIFIED] The pairing is exactly
`integral integral_Q p_far psi dx dt = 4 pi integral_0^1 (1-r^2)^2 r^2 dr = 32 pi / 105 ~= 0.957437761094`.

[VERIFIED] For `u_A = A e_1`,
`U(A) = integral integral_Q |u_A|^2 psi dx dt = A^2 (32 pi / 105)`.
Hence the pressure pairing is
`integral integral_Q p_far psi dx dt = 32 pi / 105`,
independent of `A`, while `U(A) -> 0` as `A -> 0`.

[VERIFIED] Therefore for every exponent `alpha > 0`,
`(integral integral_Q p_far psi dx dt) / U(A)^alpha = (32 pi / 105)^(1-alpha) A^(-2 alpha) -> infinity`
as `A -> 0`.
So no estimate with a coefficient depending only on the harmonic far-field data can force the pairing to carry a positive power `U(A)^alpha`.

[COMPUTED] The script prints the sample values
`U(1) = 0.9574`, `U(1/2) = 0.2394`, `U(1/4) = 0.05984`, `U(1/8) = 0.01496`,
while the pairing stays fixed at `0.9574`.

# Why harmonicity does or does not change scaling

[VERIFIED] Harmonicity improves regularity and oscillation, but in this model those gains are already saturated: `p_far` is exactly constant on `Q`, so its oscillation is `0` and every interior harmonic estimate is trivially optimal.

[CHECKED] Despite that maximal regularity, the coefficient in the pairing is still fixed entirely by the exterior shell data. The local amplitude parameter `A`, hence the local energy scale `U(A)`, enters only through the separately chosen local field, not through `p_far`.

[CHECKED] This isolates the obstruction requested in the goal:
dependence only on exterior/energy-scale data, survival of a constant harmonic mode, and harmonic regularity controlling oscillation without creating any new `U`-power.

# Consequence for the mission

[VERIFIED] The smallest explicit falsification model is already negative. A harmonic far-field component can be perfectly smooth, perfectly harmonic, and even constant on the local cylinder while its pairing against an explicit local test function remains independent of the local energy-scale quantity.

[CHECKED] Therefore an alternative near/far pressure split can only help the mission if it changes which piece is paired with the De Giorgi object. Harmonicity of `p_far` by itself does not turn the pressure coefficient into something genuinely `U_k`-dependent.
