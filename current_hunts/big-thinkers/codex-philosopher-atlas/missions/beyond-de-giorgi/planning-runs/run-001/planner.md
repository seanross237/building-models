# Planner Portfolio - beyond-de-giorgi / run-001

## Preserved Context

- `beta = 4/3` is already sharp for the De Giorgi-Vasseur route. This portfolio does not spend budget on more strong-type pressure refinements, H^1/BMO relabeling, or other near-variants of the exhausted chain.
- The prior `vasseur-pressure` mission established that local pressure closes and far-field pressure is the sole obstruction. That result is treated as fixed.
- Tao's 2016 averaged-NS obstruction is the hard filter. Every chain includes an explicit step asking whether the candidate mechanism uses a property of actual Navier-Stokes that averaging destroys.
- Useful negative results count. Each chain is scoped so that an early kill still produces a reusable obstruction note, not just a failed attempt.

## Portfolio Summary

### Chain 01 - Local Harmonic Pressure Localization

Central premise: the failed H^1 route was global, while `p_far` is harmonic on the local cylinder. The question is whether truly local harmonic norms, annular energy, or Harnack decay create a usable gain that is not just `O(E_0)`.

Why it belongs: this is the cleanest direct successor to the previous mission's best surviving lead.

### Chain 02 - SQG-Type Cancellation via Lamb Vector Reformulation

Central premise: SQG wins by reformulating the drift coupling, not by beating the De Giorgi exponent. This chain asks whether an NS reformulation around the Lamb vector, vorticity transport, or Helmholtz projection exposes a first-order cancellation that the usual velocity-pressure form hides.

Why it belongs: this is the highest-novelty algebraic route and the one most directly motivated by the SQG blueprint.

### Chain 03 - Geometric Vorticity Alignment and Local Beltrami Tubes

Central premise: Tao averaging keeps harmonic analysis but destroys fine vortex geometry. Exact Beltrami annihilates the Lamb vector, so the natural question is whether local near-Beltrami structure on intense-vorticity regions can be linked to Constantin-Fefferman style control.

Why it belongs: this is the cleanest geometry-first chain and targets a property that looks genuinely absent from the averaged model.

### Chain 04 - Critical Element / Concentration-Compactness

Central premise: if blowup exists, the right object may be a minimal blowup profile, not a sharper local estimate. This chain asks whether the existing NS profile-decomposition machinery is strong enough to isolate a critical element and whether any NS-specific rigidity mechanism survives Tao's filter.

Why it belongs: this is the most globally different route and has the highest proof ceiling, even though it is the riskiest.

### Chain 05 - Strain-Pressure Eigenstructure

Central premise: the exact tensor identities linking strain, pressure Hessian, and vorticity stretching may contain NS-specific rigidity that averaged quadratic models do not retain. The target is a conditional criterion or obstruction phrased in eigenframe dynamics rather than scalar norms.

Why it belongs: this covers the tensor/algebraic middle ground between pure geometry and pure harmonic analysis without duplicating either.

## Major Differences Between Chains

- Chain 01 is local and analytic. It exploits harmonicity of the far-field pressure and the local/global mismatch exposed by the previous mission.
- Chain 02 is algebraic. It searches for a reformulation that changes the nonlinear mechanism itself, in the same spirit that separates SQG from NS.
- Chain 03 is geometric. It works on coherent structures, alignment, and high-vorticity sets rather than on norms or decompositions.
- Chain 04 is dynamical and global. It assumes blowup and tries to classify the minimal counterexample.
- Chain 05 is tensorial. It focuses on pointwise identities, eigenframes, and strain-pressure coupling rather than tube geometry or compactness.

## Portfolio Shape

- Highest floor: Chain 01 and Chain 03. Both can produce strong obstruction notes even if they fail.
- Highest novelty ceiling: Chain 02 and Chain 04. Either would change the mission's landscape if it survives first contact.
- Best bridge chain: Chain 05. It can connect the Tao filter, vorticity geometry, and pressure structure without collapsing back into De Giorgi.

## Selector Guidance

If the selector wants the widest coverage with minimal overlap, the right mix is:

1. One local analytic chain: Chain 01.
2. One structure-first chain: Chain 02 or Chain 03.
3. One global route: Chain 04 or Chain 05.

That mix covers all five candidate structural properties named in the mission context while preserving clear failure modes.
