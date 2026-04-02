# Angle 3 --- Microlocal Defect Measures on the Nonlinear Term

## Adversarial Exploration

**Date:** 2026-04-02
**Evaluator stance:** Honest exploration, early falsification preferred over advocacy.

---

## 1. Concise Statement of the Proposed Route

Take a sequence of Leray-Hopf solutions that putatively concentrate (i.e., fail to be compact in the energy space). Associate to this sequence a microlocal defect measure `mu` in the sense of Gerard (1991) and Tartar (1990), living on the cosphere bundle `S^* R^3`. This measure records the phase-space distribution of energy escaping compactness. The key structural input is the **null structure** of the Leray-projected quadratic form: because `div u = 0`, the principal symbol of the bilinear map

```
(u, v) |-> P(u . nabla v)
```

vanishes on a codimension-1 variety in frequency space --- the "resonant set" where the Leray projection annihilates the advective transport. The proposed program is:

1. Prove a **microlocal support theorem**: `mu` is supported on the resonant variety `R` inside `S^* R^3`.
2. Show that on `R`, `mu` satisfies a **transport equation** whose characteristics are the bicharacteristics of the linearized Stokes operator.
3. Argue that the **codimension of `R`** combined with the **transport constraint** forces `mu = 0`, i.e., the defect measure is trivial.
4. Conclude compactness of the solution sequence, which by standard conditional regularity results (e.g., concentration-compactness plus epsilon-regularity) gives full regularity.

---

## 2. Check Against Known Obstructions in the Status Document

### Obstructions it claims to avoid

- **Finding 9 (reformulation-only escapes closed):** The proposal claims it goes beyond reformulation because microlocal defect measures extract phase-space geometric information invisible in any single coordinate representation. This is a defensible distinction. A defect measure is not the same as rewriting the PDE; it is an additional limit object capturing concentration behavior in phase space.

- **Finding 2 (BKM circularity):** The route does not attempt to bound `||omega||_{L^infty}` directly. It instead targets compactness of the solution sequence, which is a logically different statement. This is a real bypass.

- **Findings 3-5 (De Giorgi / epsilon-regularity ceilings):** The route does not use De Giorgi iteration or epsilon-regularity bootstrap at all. It passes through concentration-compactness, which is a different proof architecture.

### Obstructions it may still hit

- **"No one-sided gain from structure" (Finding 9, broadly construed):** The deeper question is whether the null structure of the NS bilinear form actually constrains the defect measure more than generic incompressibility already does. The div-free condition is already accounted for in every classical estimate. The question is whether its *microlocal* expression gives something extra that is invisible in the standard energy framework.

- **Epsilon-regularity as endpoint:** Even if the defect measure is shown to be supported on a restricted set, converting this into regularity likely still passes through some form of epsilon-regularity or concentration-compactness argument at the final step. The route may re-encounter known ceilings when cashing in the defect measure information.

- **Scaling criticality:** The NS problem is critical in `L^3` / `dot{H}^{1/2}`. Microlocal defect measures are most powerful in semiclassical or high-frequency limits where there is a clean separation of scales. In a scale-critical problem, there is no semiclassical parameter --- the concentration can happen at all scales simultaneously. This is a fundamental mismatch between the tool and the problem.

---

## 3. Strongest Argument For Why the Route Might Work

The most compelling structural point is this: **the Leray projector is not a scalar operator in frequency space, and its interaction with the bilinear advection term creates genuine null directions that are invisible in energy-level estimates.** More specifically:

The bilinear symbol of `(u, v) |-> P_i (u_j partial_j v_i)` is, after Leray projection,

```
sigma(xi, eta) = (delta_{il} - xi_i xi_l / |xi|^2) * eta_j
```

which vanishes when `eta` is parallel to `xi` (because then the whole expression reduces to `xi . eta / |xi|^2` times a projection onto `xi^perp`, which kills the `xi`-direction component). The resonant variety is therefore the set where the "output" frequency `xi` is parallel to the "input gradient" frequency `eta`. In the cosphere bundle, this is a codimension-1 condition.

The genuine novelty would be: **if the defect measure is restricted to this resonant variety, and if the bicharacteristic flow of the Stokes operator is ergodic or dispersive on that variety, then the transport equation might force `mu` to spread out rather than concentrate.** This would be a new mechanism --- not an energy bound, not a regularity bootstrap, but a phase-space geometric rigidity coming from the interplay of the null structure with linear dispersion.

Moreover, there is precedent: microlocal defect measures have been used to prove compactness in other critical/borderline settings --- notably in homogenization theory (Tartar), and in the study of wave equations with critical nonlinearities (Gerard, Bahouri-Gerard). The technique has a genuine track record of extracting compactness from structural information that is invisible in standard function space estimates.

---

## 4. Strongest Argument For Why It Probably Fails

There are several serious reasons to expect failure, ranked by severity:

### 4a. The Stokes operator has no dispersion in 3D

This is the most damaging point. The bicharacteristics of the Stokes (or even linearized NS) operator are **not dispersive**: the Stokes semigroup `e^{t nu Delta}` is purely dissipative, not oscillatory. Its symbol is `e^{-nu |xi|^2 t}`, which has no phase. Consequently, the "transport equation" for the defect measure along bicharacteristics is actually a **dissipation/damping equation**, not a dispersive transport equation.

In the dispersive case (e.g., Schrodinger or wave equations), bicharacteristic transport can spread the defect measure and prevent concentration. But for a purely parabolic operator, the bicharacteristics are trivial --- they just sit at fixed spatial points while the frequency component decays. The defect measure `mu` restricted to the resonant variety is not transported anywhere useful. It simply decays, and the question reduces to whether the nonlinear self-interaction can regenerate it faster than dissipation kills it --- which is exactly the standard regularity question, repackaged.

**This is a critical structural mismatch.** The microlocal defect measure technique is fundamentally a tool for oscillation, not concentration. It works best when the linear part of the equation has nontrivial oscillatory characteristics (wave, Schrodinger, Dirac). For parabolic equations, the high-frequency behavior is dominated by dissipation, and the defect measure formalism adds little beyond what standard compactness arguments already capture.

### 4b. The "null structure" may not be strong enough

The null structure of the NS bilinear form --- the vanishing of the symbol when `eta || xi` --- is well known. It is essentially the statement that the pressure term cancels the longitudinal part of the advective nonlinearity. This is the same div-free structure that is already exploited in every regularity estimate via the Leray projection. The question is whether its microlocal expression gives strictly more.

In the regularity theory of semilinear wave equations, null forms (Klainerman's null condition) genuinely improve estimates by a full derivative. But in that setting, the null structure interacts with *oscillation* to produce cancellation. For NS, the analogue would need the null structure to interact with *dissipation*, and there is no known mechanism by which this produces a gain beyond what energy estimates already capture.

Furthermore, the resonant variety (where `eta || xi`) is codimension 1 in the cosphere bundle, which is `S^* R^3 = R^3 x S^2`, a 5-dimensional manifold. A codimension-1 submanifold is 4-dimensional. This is not particularly restrictive --- the defect measure on a 4-dimensional set inside a 5-dimensional space can still carry substantial mass. For the argument to work, one would need the effective dimension to be much lower, likely codimension >= 2 or higher. But the actual resonant set is exactly codimension 1, which is unlikely to suffice.

### 4c. Microlocal defect measures lose information at critical regularity

Microlocal defect measures are defined as weak-* limits of Wigner distributions, and they capture the leading-order concentration behavior. But at critical regularity (which is where NS lives), the defect measure may be trivially zero even for sequences that fail to be compact, because the concentration happens at a rate that is invisible to the leading-order Wigner distribution. This is a well-known limitation: at critical scaling, one needs **refined microlocal objects** (profile decompositions a la Bahouri-Gerard, or concentration-compactness on the full profile tree) rather than a single defect measure.

In fact, the Bahouri-Gerard profile decomposition for critical wave equations already shows that the defect measure alone is not enough --- one needs to track individual concentration profiles and their interactions. For NS, the analogous structure would be concentration-compactness in the Kenig-Koch `L^3` or `dot{H}^{1/2}` framework, which is already part of the standard machinery and has not produced a regularity proof.

### 4d. The route has an implicit circularity risk

The final step --- converting `mu = 0` into regularity --- likely requires showing that compactness of a concentrating sequence implies the limit is a strong solution. This typically requires epsilon-regularity or a suitable bootstrap. The status document records that epsilon-regularity is structurally capped (Finding 5). If the defect-measure argument reduces at the endpoint to "compactness + epsilon-regularity = regularity," it may inherit the same structural ceiling.

---

## 5. First Concrete Subproblems

### Subproblem 1: Compute the exact resonant variety

Compute explicitly the variety `R` in `S^* R^3` where the principal symbol of the Leray-projected bilinear form vanishes. Determine its codimension in the full cosphere bundle. Specifically: is it codimension 1 (as expected from the `eta || xi` condition) or does the full tensorial structure of the Leray projection impose additional constraints that raise the codimension?

**Prediction:** Codimension 1, because the constraint is `xi x eta = 0` (i.e., `eta` parallel to `xi`) which removes one degree of freedom from the 2-sphere of directions. This is the most likely outcome and it would already weaken the argument significantly.

### Subproblem 2: Determine whether parabolic bicharacteristics carry any useful transport

Write down the exact transport equation for the defect measure restricted to `R`, using the bicharacteristics of the Stokes semigroup. Determine whether the transport is trivial (fixed spatial point, decaying frequency) or whether the nonlinear coupling introduces nontrivial effective transport. If the transport is trivial (as expected for a purely dissipative linear part), assess honestly whether the formalism adds anything beyond standard parabolic compactness.

**Prediction:** The transport is trivial in the sense that Stokes bicharacteristics do not move in the spatial variable. The defect measure "sits" at each spatial point and decays. The only nontrivial dynamics come from the nonlinear source term, which is what one is trying to control in the first place.

### Subproblem 3: Test the argument on a model problem with genuine null structure

The cleanest test case would be incompressible MHD in 2D or a simplified 3D model where the null structure is similar but regularity is known by other means. If the microlocal defect measure argument cannot recover known regularity results in the model problem, it has no chance on full 3D NS.

**Prediction:** In 2D NS (where regularity is known), the argument should go through trivially because the defect measure is zero for other reasons (energy controls everything in 2D). This makes 2D NS a useless test case. A more informative test would be 3D NS with hyperdissipation `(-Delta)^s` for `s > 5/4`, where regularity is known but the proof uses energy methods, not microlocal methods.

### Subproblem 4: Determine the relationship to Bahouri-Gerard profiles

Clarify whether the microlocal defect measure is strictly weaker than, equivalent to, or complementary to the Bahouri-Gerard profile decomposition at critical regularity. If it is strictly weaker (as expected), the route needs to be upgraded to a profile-level argument, at which point it becomes part of the existing concentration-compactness machinery rather than a new route.

### Subproblem 5: Assess the codimension-mass threshold

Even assuming the defect measure is supported on `R` and satisfies a transport equation, determine the minimal codimension of the support needed to force `mu = 0`. Is codimension 1 sufficient, or does one need codimension 2 or higher? Compare with known results on the Hausdorff dimension of singular sets from partial regularity (Caffarelli-Kohn-Nirenberg gives a 1-dimensional singular set in spacetime).

---

## 6. Route Classification

**Mechanism-facing, leaning speculative.**

The route proposes a real structural observation (the null structure of the Leray-projected bilinear form creates a restricted defect-measure support) and a real proof architecture (transport equation on the restricted support forces triviality). However:

- The key mechanism (bicharacteristic transport forcing dispersive spreading) fundamentally relies on oscillatory behavior that the Stokes operator does not have.
- The null structure is codimension 1, which is likely insufficient.
- At critical regularity, defect measures may be too coarse an object.

These are not mere technical gaps; they are structural mismatches between the proposed tool and the problem. The route has a clear mechanism idea but is not yet theorem-facing because the core mechanism (dispersive transport on the resonant variety) appears absent for parabolic equations.

---

## 7. Final Verdict

**`weakly promising`** --- with a strong lean toward `unclear`.

**Rationale:**

*In favor:* The route introduces a genuinely different proof architecture (phase-space geometry of concentration) that is logically independent of the closed routes. The null structure of the NS bilinear form is a real algebraic feature that has not been fully exploited in the regularity problem. Microlocal defect measures have a successful track record in other critical PDE settings.

*Against:* The core mechanism --- bicharacteristic transport spreading the defect measure --- is designed for dispersive/oscillatory equations and does not transfer cleanly to the parabolic setting. The Stokes operator has trivial bicharacteristics. The resonant variety is codimension 1, which is weak. At critical regularity, a single defect measure is likely too coarse; one needs profile decompositions, which are already part of the standard toolkit. The argument risks reducing to known concentration-compactness machinery at the endpoint.

The route is not dead --- there is a logically coherent path from null structure to support restriction to triviality. But the most important structural ingredient (nontrivial bicharacteristic transport) is absent, and without it the argument does not have a clear mechanism for forcing `mu = 0`. The route would need a genuinely new idea about how parabolic dissipation (rather than dispersive oscillation) interacts with null-structure support restrictions to produce compactness. No such idea is currently visible.

**If forced to bet:** the route closes negatively at Subproblem 2, when the triviality of Stokes bicharacteristics is confronted honestly. The defect measure framework would then add no structural information beyond what standard parabolic compactness already provides, and the remaining argument would collapse into known machinery.
