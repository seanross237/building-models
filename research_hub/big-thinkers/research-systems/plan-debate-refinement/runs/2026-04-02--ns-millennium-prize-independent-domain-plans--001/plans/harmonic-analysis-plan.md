# Harmonic Analysis / Pressure / Nonlinear Estimates Plan

## Core judgment

There is **no honest prize-facing mainline currently available** from the pure harmonic-analysis / pressure lane.

The status file closes the classical versions of this program:

- De Giorgi / Vasseur pressure improvement is capped sharply at `beta = 4/3`.
- Standard epsilon-regularity inherits the same ceiling.
- The `H^1` pressure route dies at the `W^{1,3}` wall.
- Harmonic far-field pressure does not touch the real bad term.
- Constant-factor Calderon-Zygmund improvements do not change the scaling obstruction.

So I would not spend time pretending there is still a generic pressure-improvement path to the prize. The only live frontier in this domain is much narrower:

> determine whether the borderline Calderon-Zygmund debt in the anisotropic pressure/strain derivative term driving curvature, schematically `P_perp((D_xi S) xi)`, is a true exact-NS saturation mechanism, or whether incompressibility plus geometric localization force a logarithmic or otherwise subcritical gain.

If that borderline can be beaten, this lens becomes relevant again. If it cannot, the right output is a sharp no-go theorem that closes the lane cleanly.

## Main theorem target

Prove a **borderline-breaking local estimate** for the dangerous anisotropic pressure/strain term in high-vorticity regions:

```text
|D_xi S| <= C |omega|^(3/2) / (nu^(1/2) L(|omega|))
```

with `L(M) -> infinity` at least logarithmically on the dangerous high-vorticity set, or any equivalent local Morrey/Carleson formulation for the anisotropic pressure Hessian that is strong enough to push the existing coupled `(|omega|, kappa)` bootstrap past the critical `delta = 1/2` threshold.

This is the only harmonic-analysis theorem target here that would count as plausible prize-relevant forward motion.

## Fallback theorem target

Prove a **sharp pressure/CZ no-go theorem**:

any argument based only on

- Calderon-Zygmund representation of `S` or `nabla^2 p`,
- standard Littlewood-Paley / paraproduct decompositions,
- local pressure splits,
- Hardy-BMO / commutator technology,
- and pointwise tube geometry hypotheses short of genuinely new PDE structure,

cannot improve the critical `delta = 1/2` scaling in the nonparallel core-scale two-tube interaction regime.

That would be a good theorem. It would close a misleading route instead of letting it absorb more time.

## Route structure

### Route 1. Anisotropic pressure-Hessian decomposition

Main line.

Work directly on the exact tensor object behind the curvature source, not on scalar pressure slogans. The goal is to split

```text
P_perp((D_xi S) xi)
```

into pieces that are:

- genuinely null by incompressibility / symmetry,
- lower order after localization,
- or truly bad and carrying the full CZ debt.

If the bad piece survives unchanged, that is already a serious negative result.

### Route 2. Angular-frequency attack on the CZ debt

Support line for Route 1.

Use dyadic and angular decomposition near the dangerous nonparallel tube-crossing geometry to test whether the bad term really occupies all sectors or only a thin set that gives a logarithmic summation gain.

The only thing worth finding here is a gain in exponent or a rigorous proof that no such gain exists.

### Route 3. Nonlinear conversion step

If Route 1 or 2 produces a real gain, convert it immediately into a theorem through the existing coupled `(|omega|, kappa)` bootstrap or an equivalent pressure-side regularity criterion. Do not leave the gain as an isolated estimate.

### Route 4. Honest closure if the gain is not there

If Routes 1-3 fail, write the sharpness theorem. The correct end state is not “more heuristics”; it is a clean statement that the pressure/CZ lane is structurally saturated at the borderline.

## First 2-3 concrete theorem steps

### Step 1. Exact localized decomposition lemma

Prove an exact formula on a parabolic cylinder in the high-vorticity regime:

```text
P_perp((D_xi S) xi) = T_bad + T_null + T_comm
```

with:

- `T_null` vanishing by algebraic/divergence-free structure,
- `T_comm` controlled strictly below the dangerous scaling after cutoff insertion,
- `T_bad` isolated as the only surviving term with critical homogeneity.

This must be done at the tensor level. Scalar reformulations are too lossy.

### Step 2. Sharp dyadic model theorem for `T_bad`

Run the smallest honest harmonic-analysis test on `T_bad`:

- either prove a logarithmic improvement in the nonparallel high-vorticity regime,
- or prove that core-scale two-tube interactions saturate the full `|omega|^(3/2) / nu^(1/2)` size even after all available tensor cancellations are used.

The result of this step decides whether the lane is alive or dead.

### Step 3. Immediate conversion

- If Step 2 gives the gain, close the coupled bootstrap and state the regularity consequence.
- If Step 2 gives saturation, formalize it as a no-go theorem for the full pressure/CZ strategy class.

No long intermediate program should exist between Step 2 and the final theorem object.

## Hard stop conditions

- If every exact decomposition collapses back to one sign-indefinite critical CZ term with unchanged homogeneity.
- If the best gain is only an `O(1)` constant factor.
- If the argument requires assumptions that are effectively as strong as known regularity criteria.
- If the core-scale nonparallel two-tube regime can be shown to saturate every candidate cancellation mechanism in the planned toolkit.

Any one of these is enough to stop the mainline and switch to the no-go theorem.

## What counts as genuine progress

- A theorem with any explicit logarithmic or power improvement over the critical `delta = 1/2` bound on `D_xi S` or the equivalent anisotropic pressure Hessian term.
- A rigorous conversion of that gain into a regularity criterion that is not just a renamed BKM / De Giorgi statement.
- Or a sharp theorem proving that the borderline CZ debt is structurally saturated in exact NS geometry, at least for the current pressure/decomposition technology class.

What does **not** count:

- constant improvements,
- cleaner pressure splitting with unchanged scaling,
- rephrasing the same bad term in a different exact formulation,
- or heuristic numerology about tube interactions.

## What I refuse to spend time on because the status file closes it

- Any retry of De Giorgi / Vasseur pressure improvement toward `beta > 3/2`.
- Standard epsilon-regularity bootstraps dressed up with new notation.
- `H^1` / Hardy-BMO / compensated-compactness pressure repair aimed at the `W^{1,3}` wall.
- Harmonic far-field pressure refinements by themselves.
- Direct `Q`-equation self-damping arguments based on the nonexistent `-|omega|^2 / 6` autonomous term.
- Generic host-space or exact-reformulation restarts with no new one-sided gain.
- Any campaign whose best possible outcome is only a better constant in a Calderon-Zygmund estimate.

## Bottom line

For this domain lens, the honest plan is:

1. attack the single remaining borderline pressure/CZ debt at the tensor level;
2. either break it by a real logarithmic/subcritical gain;
3. or prove that it is sharp and close the lane.

Anything broader than that is not serious at the current project state.
