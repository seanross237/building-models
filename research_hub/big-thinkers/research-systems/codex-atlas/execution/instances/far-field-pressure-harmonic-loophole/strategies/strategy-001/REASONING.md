# Strategy Reasoning

## Missionary setup notes

This strategy is intentionally short. The mission brief already predicts that the likely outcome is negative and likely reachable after the Tao filter. The strategy therefore front-loads:

- exact obstruction reconstruction
- Tao compatibility analysis
- early stopping if the loophole closes cleanly

## Direction Status Tracker

| Direction | Status | Evidence | Exploration |
|---|---|---|---|
| Exact far-field obstruction reconstruction | CLOSED | Exploration 001 succeeded. It reconstructed the exact `P_k21` recurrence slot and showed the mission loophole is not the literal Vasseur harmonic term `P_k1`, but an alternative harmonic far-field decomposition question. | Exploration 001 |
| Tao compatibility of far-field harmonic structure | CLOSED | Exploration 002 concluded the loophole is Tao-incompatible. Tao's averaged model preserves only an averaged projected bilinear operator, not the local Poisson pressure structure or a clean harmonic far-field split. | Exploration 002 |
| Minimal falsification model | CLOSED | Exploration 003 gave an explicit countermodel: harmonic far-field pieces can carry fixed constant or affine modes set by exterior data, so the pairing need not have any positive power of `U`. | Exploration 003 |
| Quantitative gain check | EXHAUSTED | No structural gain survived the model stage, so there is no quantity to translate into improved recurrence arithmetic. | Not needed |

## Iteration 1 decision

The first move should stay narrow: reconstruct the exact obstruction in equations before testing Tao compatibility. The predecessor missions already closed generic De Giorgi improvement routes and identified the surviving loophole as a far-field pressure harmonicity idea. What is still missing is an equation-level statement precise enough to pass the validation guide and precise enough to compare against Tao's averaged equation.

This means exploration 001 should not be another general survey. It should extract:

- the precise far-field pressure decomposition and pairing
- the exact recurrence slot where the coefficient enters
- the arithmetic showing why the contribution remains fixed at `O(E_0)` and therefore does not improve the `beta = 4/3` obstruction unless harmonicity changes that coefficient structure

I queried the Receptionist before launch, as required, to surface any relevant factual-library holdings and meta-guidance for an equation-first reconstruction brief.

## Iteration 1 result

Exploration 001 produced the equation-level clarification the mission needed. The exact `beta = 4/3` bottleneck in Vasseur is

- the local pressure term `P_k21`,
- specifically its non-divergence pairing `-P_k21 div(u v_k / |u|)`,
- with exponent `0 + 1/2 + 5/6 = 4/3`.

The harmonic/nonlocal term `P_k1` is already favorable and is not the bottleneck when `p > 10`.

The surviving loophole is therefore narrower than the mission wording initially suggests. It is not "maybe Vasseur forgot that his bottleneck term is harmonic." He did not; the harmonic term is already separated and controlled. The only live version is:

- choose a different pressure decomposition, with a far-field harmonic piece on `Q_k`,
- show that this decomposition captures part of what Vasseur isolated as the dangerous local term,
- then show that harmonicity changes the coefficient structure rather than merely the constant.

That is the right target for the Tao filter.

## Iteration 2 decision

The Tao filter is now the critical path. The local library already says:

- Tao (2016) is a barrier-level obstruction to generic energy/harmonic-analysis methods.
- The library does not yet contain the exact averaged pressure law.
- Wolf-style harmonic+particular pressure splitting is present only as an untested lead.

So exploration 002 should answer one sharp question from the primary source: after averaging, what pressure object exists, and does it preserve the specific harmonic far-field structure that the loophole would need?

## Iteration 2 result

Exploration 002 did not kill the loophole. The Tao filter result is:

- Tao's averaged equation is written as `∂_t u = Δu + \tilde B(u,u)`.
- The ordinary NS pressure identity `-Δp = ∂i∂j(u_i u_j)` is not preserved as a clean local law for the averaged equation.
- The nonlocal Fourier-multiplier part of the averaging destroys the local harmonicity structure that the loophole needs.

So the loophole is Tao-incompatible. That means it could still be exploiting genuinely NS-specific local elliptic structure. The strategy therefore has to continue to the minimal falsification model.

## Iteration 3 result

The minimal model closes the route. Take a local ball and let `p_far` be the harmonic extension of constant boundary data from a larger enclosing ball. Then `p_far` is constant on the local ball, and its pairing against any nonnegative local test function is fixed by the test function and exterior data, not by the local De Giorgi quantity `U`.

Subtracting the constant mode does not save the mechanism: affine harmonic modes still produce pairings independent of `U`. So harmonicity can improve oscillation and regularity control, but it does not force the scaling change the loophole needed.

That is enough to end the strategy negatively. The loophole is closed because harmonicity does not create `U`-dependence.
