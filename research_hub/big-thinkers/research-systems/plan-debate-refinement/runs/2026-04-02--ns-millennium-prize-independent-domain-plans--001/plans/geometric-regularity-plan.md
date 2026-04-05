# Geometric Regularity Plan

## Core judgment

There is no honest prize-facing mainline here at present.

Within the geometric depletion / strain-vorticity / vorticity-direction lens, the status file closes the naive headline route: `e_2`-alignment by itself will not yield regularity, and GMT on the dangerous superlevel set is dead. The live frontier is narrower and more specific:

- either derive a Constantin-Fefferman / Deng-Hou-Yu type regularity criterion from actual high-vorticity tube geometry, with a genuine gain over the borderline `|D_xi S| ~ |omega|^{3/2} / nu^{1/2}` core-scale tube-crossing scenario;
- or prove a serious no-go theorem showing that the remaining geometric depletion family cannot beat that borderline without a new PDE-level ingredient.

So my judgment is:

- `e_2`-alignment is now a mechanistic clue, not a main theorem route;
- the real question is spatial coherence of the vorticity direction in high-vorticity tube encounters;
- the central barrier is not single-tube dynamics, but nonparallel tube-tube interaction at core scale;
- if this lens contributes something decisive, it will be either a CF/DHY-type upgrade from tube geometry, or a theorem proving that such an upgrade is impossible under the currently available mechanisms.

## Main theorem target

Prove a quantitative reduction theorem from high-vorticity tube geometry to a CF/DHY-type regularity criterion.

Concretely, target a theorem of the following form:

> For a smooth 3D Navier-Stokes solution on `[0,T)`, assume that on each sufficiently high-vorticity region `{|omega| > M}` the flow admits a finite-overlap tube decomposition whose single-tube pieces have uniformly bounded vortex-line curvature, and whose nonparallel core-scale tube encounters satisfy a quantitative sparsity/coherence bound strong enough to force a logarithmically subcritical estimate for `D_xi S` along vortex lines. Then the Constantin-Fefferman / Deng-Hou-Yu direction-regularity criterion holds, hence no blowup occurs on `[0,T)`.

This is the best serious target because the status file already says:

- single-tube geometry is safe;
- the obstruction is localized to core-scale nonparallel encounters;
- any unconditional route must beat the exact borderline `delta = 1/2` forced by Biot-Savart geometry;
- a logarithmic gain would already matter.

I do not expect to prove this full theorem quickly. But this is the correct main target.

## Fallback theorem target

Prove a no-go theorem for the remaining alignment/depletion family:

> Any regularity program that uses only `e_2`-alignment, the Rayleigh quotient `Q`, pointwise/ODE curvature control, single-tube filament structure, pairwise antisymmetry at closest approach, circulation conservation, and energy/enstrophy budgets cannot improve the borderline `|D_xi S| <= C |omega|^{3/2} / nu^{1/2}` scaling in the dangerous nonparallel core-scale tube-crossing regime.

This would not solve Navier-Stokes, but it would be a valuable theorem-level closure result. It would turn the current informal picture into a real frontier statement: any viable geometric regularity route must use genuinely PDE-level spatial structure beyond the currently exhausted local mechanisms.

## Route structure

### Route 1: tube geometry to CF/DHY regularity

This is the only remotely prize-facing route in this lens.

The objective is to replace vague "coherent vortex tube" language with a theorem object that controls the vorticity-direction field strongly enough to trigger a known geometric regularity criterion.

Subgoals:

- isolate the bad contribution to `D_xi S` to a precisely defined encounter set of nonparallel core-scale tube interactions;
- show that outside that set, the flow is safely subcritical because single-tube dynamics give `|D_xi S| ~ kappa |omega|`;
- prove a logarithmic improvement, sparsity law, or integrable encounter budget on the bad set strong enough to imply CF/DHY.

### Route 2: geometric reduction theorem before any regularity claim

If Route 1 is too ambitious, the next serious theorem is a sharp reduction theorem:

- every high-vorticity configuration splits into safe single-tube regions plus a bad encounter set;
- every known dangerous contribution to `D_xi S` comes from that set and nowhere else;
- all other geometric mechanisms are provably subcritical.

This would be a real advance because it would collapse the geometric regularity problem to one explicit scenario instead of a cloud of heuristics.

### Route 3: no-go theorem for alignment-only depletion programs

If the encounter set still saturates the borderline after honest analysis, stop trying to rescue alignment-only or depletion-only arguments and prove the impossibility theorem cleanly.

That theorem should explicitly cover:

- `e_2`-alignment-only regularity claims;
- `Q`-only depletion claims;
- curvature ODE bootstraps without new PDE structure;
- antisymmetry/circulation/energy arguments in isolation.

This route is not prize-facing, but it is mathematically clean and would prevent further wasted effort.

## First 2-3 concrete theorem steps

### Step 1: self/interaction decomposition for `D_xi S`

Prove a decomposition theorem for `D_xi S` on `{|omega| > M}`:

- a self-induced single-tube term with bound `|D_xi S| <= C kappa |omega|`;
- a pairwise interaction term coming from neighboring tube cores;
- a remainder term controlled by lower-vorticity or farther-field contributions.

The point is to formalize, at theorem level, the status-file claim that the only dangerous scaling comes from nonparallel core-scale tube-tube interaction.

### Step 2: reduction from geometric encounter control to CF/DHY

Define an encounter functional on the bad set, built from:

- tube-axis curvature;
- inter-tube angle;
- core-scale separation;
- encounter duration along vortex lines.

Then prove: if this functional has an integrable logarithmic gain over the borderline scaling, the CF or DHY direction-regularity criterion follows. This converts "beat `delta = 1/2`" into one explicit theorem statement.

### Step 3: either prove encounter sparsity/coherence, or prove it cannot hold from existing ingredients

Try to show that nonparallel core-scale encounters cannot cascade densely enough along a high-vorticity vortex line to saturate blowup. If that fails, convert the failure into the fallback no-go theorem instead of continuing heuristic work.

This is the main decision point of the program.

## Hard stop conditions

I would stop this line quickly if any of the following happens:

- the tube decomposition itself cannot be made canonical enough for theorem use on high-vorticity sets;
- Step 1 does not produce a clean localization of the bad scaling to a sharply defined encounter term;
- the encounter term still saturates the exact borderline after all available spatial-coherence identities, with no plausible source of logarithmic gain;
- the argument starts relying again on `s_2 <= 0`, GMT dimension reduction, pressure-Hessian self-damping, or epsilon-regularity at the `nabla^2 u` level;
- the only remaining claims are DNS-style geometric plausibility statements rather than PDE theorem objects.

Any of those means this lens is not producing a prize-facing route and should be demoted to no-go cleanup only.

## What counts as genuine progress

The following would count as real progress:

- a theorem reducing the vorticity-direction regularity problem to one explicit encounter functional;
- a theorem showing all single-tube high-vorticity geometry is safely subcritical in the required sense;
- a CF/DHY implication derived from a concrete tube-encounter hypothesis rather than an abstract Lipschitz assumption on `xi`;
- a logarithmic improvement over the `delta = 1/2` borderline in the actual bad interaction geometry;
- failing that, a broad no-go theorem proving that alignment/depletion-only arguments cannot cross the borderline.

By contrast, better pictures, more simulations, or more examples of `e_2`-alignment do not count as meaningful progress anymore.

## What I refuse to spend time on because the status file closes it

I would not spend time on:

- proving regularity from `e_2`-alignment alone;
- GMT dimension-reduction arguments on `{|omega| > M, Q > epsilon}`;
- trying to force `s_2 <= 0` in high-vorticity regions;
- pressure-Hessian `Q` self-damping stories based on the nonexistent autonomous `-|omega|^2 / 6` mechanism;
- pointwise curvature ODE bootstraps that do not introduce new PDE-level spatial structure;
- finite-build-up / moving-source parabolic smoothing as the missing logarithmic gain in the dangerous `Theta = O(1)` crossing regime;
- epsilon-regularity at the `D_xi S` or `nabla^2 u` level;
- vague "coherent vortex tubes probably regularize" narratives without a theorem object tied to CF/DHY.

## Bottom line

The honest geometric plan is not "push harder on alignment." That door is closed.

The only serious path in this lens is:

1. localize the bad scaling entirely to nonparallel core-scale tube encounters,
2. try to upgrade encounter geometry into a CF/DHY-type criterion with a real logarithmic gain,
3. if that gain does not materialize, prove a no-go theorem and stop treating geometric depletion as a prize-facing mainline.

That is narrow, but it is the right narrow target.
