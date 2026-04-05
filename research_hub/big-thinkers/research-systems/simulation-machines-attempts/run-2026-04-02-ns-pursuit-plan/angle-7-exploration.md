# Angle 7 Exploration: Nonlinear Spectral Gap via Optimal Transport on the Vorticity Measure

**Date:** 2026-04-02
**Evaluator stance:** Adversarial honest exploration

---

## 1. Concise Statement of the Proposed Route

Normalize the enstrophy density `rho_omega(t) = |omega(x,t)|^2 / ||omega(t)||_2^2` into a probability measure on `T^3`. Track its Wasserstein-2 distance from the uniform measure:

```
E(t) = W_2(rho_omega(t), uniform)^2.
```

The route claims two competing effects on `E(t)`:

- **Contraction (viscous).** The Laplacian in the vorticity equation drives `rho_omega` toward uniformity. The mechanism is Bakry-Emery-type: the heat semigroup contracts in `W_2` with rate proportional to a spectral gap, and the viscous enstrophy dissipation `nu ||nabla omega||_2^2` controls that rate.
- **Dilation (nonlinear).** The stretching term `omega . nabla u` can concentrate `rho_omega`. But `div u = 0` imposes a volume-preservation constraint on the transport, limiting the dilation rate in Wasserstein distance.

The proposed theorem-object is a contraction-dominance lemma:

```
d/dt W_2(rho_omega(t), uniform) <= -lambda nu ||nabla omega||_2^2 / ||omega||_2^2 + mu ||omega||_infty
```

with `lambda > mu`, so that dissipation beats stretching-driven concentration.

The conclusion would be: `rho_omega` cannot concentrate to a point in finite time, which (via known criteria) gives regularity.

---

## 2. Check Against Known Obstructions

### Obstruction 1: BKM circularity (Finding 2)

**Status: NOT bypassed --- the circularity reappears inside the proposed lemma.**

The proposed bound has `||omega||_infty` on the right-hand side as the dilation term. The claim is that this avoids BKM because `||omega||_infty` appears "in competition with dissipation in a Wasserstein balance, not as a standalone requirement." But this is misleading. To close the argument, you need the contraction term to dominate the dilation term, i.e.,

```
lambda nu ||nabla omega||_2^2 / ||omega||_2^2 >= mu ||omega||_infty.
```

This requires controlling `||omega||_infty` in terms of `||nabla omega||_2^2 / ||omega||_2^2`. But `||nabla omega||_2^2 / ||omega||_2^2` is a Rayleigh-type quotient bounded below only by the first Laplacian eigenvalue (a constant independent of the solution). Meanwhile, `||omega||_infty` can be arbitrarily large. So the contraction-dominance inequality is *exactly* a disguised bound on `||omega||_infty`, which is BKM.

More precisely: if you could prove the contraction-dominance lemma as stated, you would in particular be proving that `||omega||_infty <= C nu ||nabla omega||_2^2 / ||omega||_2^2`, which, combined with the enstrophy equation, immediately gives regularity by completely standard means --- no optimal transport needed. The Wasserstein framework is decorative here; the load-bearing content is an a priori bound on `||omega||_infty`.

### Obstruction 2: De Giorgi dimensional cap (Finding 4)

**Status: claimed bypass does not hold.**

The proposal claims that "in Wasserstein geometry, the relevant exponents are transport exponents rather than Sobolev embedding exponents." This is vague and, upon examination, incorrect in the relevant sense. The Bakry-Emery contraction theory works for *linear* diffusions or for gradient flows of *convex* functionals. The enstrophy measure `rho_omega` does not evolve by a gradient flow of a convex functional --- the vortex stretching term is the obstruction. The "transport exponents" in the Wasserstein framework do not magically avoid the dimensional scaling constraints that produce `beta = 4/3`. Those constraints are ultimately about the competition between diffusion and nonlinear amplification in 3 spatial dimensions, and changing the metric from Sobolev to Wasserstein does not alter the underlying dimensional analysis.

### Obstruction 3: The enstrophy-based regularity programs are closed (What Is Closed, item 1)

The status document lists "generic enstrophy regularity programs" as closed. This route, while dressed in optimal-transport language, is fundamentally an enstrophy regularity program: it studies the spatial distribution of `|omega|^2` and tries to prove it cannot concentrate. The novelty claim rests entirely on the Wasserstein metric being a different lens. But the equation governing `rho_omega` is derived from the same vorticity equation, and the essential difficulty --- controlling the stretching term `omega . nabla u` --- is unchanged.

### Obstruction 4: No one-sided gain from reformulation (Finding 9)

Passing from the enstrophy equation to the Wasserstein evolution of `rho_omega` is a reformulation. The proposal needs to identify a *one-sided gain* that appears in the Wasserstein formulation but not in the standard one. The only candidate is the claim that `div u = 0` provides a Wasserstein-specific bound on the dilation rate. Let us examine this.

The divergence-free condition means the velocity field preserves the Lebesgue measure. But `rho_omega` does not evolve by pure transport along `u` --- it also has source/sink terms from the stretching `omega . nabla u` and dissipation `nu Delta omega`. The volume-preservation constraint on `u` does constrain the *transport* component of the evolution, but the dominant concentrating effect comes from the *source* term (stretching amplifies `|omega|^2` locally), not from the transport term. So the divergence-free constraint, while real, is applied to the wrong piece of the dynamics. The concentrating mechanism is not transport-driven concentration but production-driven concentration.

---

## 3. Strongest Argument for Why the Route Might Work

The one genuinely interesting structural observation is this: the competition between dissipation and concentration *can* sometimes be analyzed more sharply in Wasserstein geometry than in Sobolev geometry, because the Wasserstein distance is sensitive to mass displacement rather than pointwise amplitude.

Specifically, consider the scenario where `|omega|^2` is concentrating toward a delta function. In Sobolev norms, the relevant quantity is `||omega||_infty`, which grows without bound. In Wasserstein distance from uniform, the relevant quantity is how far the mass has moved, which is a *geometric* quantity insensitive to the amplitude of the peak. It is conceivable (though far from established) that the viscous dissipation `||nabla omega||_2^2` controls Wasserstein concentration more efficiently than it controls `L^infty` concentration, precisely because `||nabla omega||_2^2` measures the roughness of the profile (which correlates with mass displacement) rather than the height of the peak.

If this were true, the route would produce a bound on the Wasserstein concentration rate that does *not* reduce to a bound on `||omega||_infty`, but rather to a bound on the spatial extent of the vorticity support --- which is a strictly weaker object. The question would then be whether prevention of Wasserstein concentration alone suffices for regularity, which is nontrivial: concentration of `rho_omega` to a point implies `||omega||_infty -> infty` (by mass conservation and normalization), but the converse is false.

This is the one potentially non-circular path: if you could show that the Wasserstein distance `E(t)` stays bounded *without* controlling `||omega||_infty`, and then separately show that bounded Wasserstein distance implies a regularity-class bound, the route would bypass BKM. But neither step has been demonstrated even at the level of a plausible mechanism.

---

## 4. Strongest Argument for Why It Probably Fails

**The proposed lemma is almost certainly false as stated, and any repair reintroduces BKM circularity.**

Here is the concrete reason. Consider a family of smooth solutions on `T^3` where the vorticity concentrates into a thin tube of radius `epsilon` and length `O(1)` with `||omega||_infty ~ epsilon^{-2}` and `||omega||_2 ~ epsilon^{-1}` (consistent with enstrophy conservation). This is exactly the kind of near-singular configuration one must handle.

For such a configuration:

- `||nabla omega||_2^2 / ||omega||_2^2 ~ epsilon^{-2}` (the gradient is of order `epsilon^{-3}` on a volume `epsilon^2`, so `||nabla omega||_2^2 ~ epsilon^{-4}`, divided by `||omega||_2^2 ~ epsilon^{-2}`).
- `||omega||_infty ~ epsilon^{-2}`.
- The Wasserstein distance `W_2(rho_omega, uniform)` is `O(1)` (the mass is displaced by `O(1)` but concentrated in a tube).

So the proposed inequality reads roughly:

```
d/dt W_2 <= -lambda nu epsilon^{-2} + mu epsilon^{-2}.
```

The two terms are the *same order* in `epsilon`. There is no reason to expect `lambda > mu` universally --- the constants depend on the geometry of the concentration, and for a thin vortex tube, the stretching term is comparable to the dissipation term. This is precisely the criticality of 3D NS: dissipation and stretching scale the same way.

This is not an accident. It is a manifestation of the same dimensional balance that produces `beta = 4/3` in the De Giorgi framework and the BKM circularity in the enstrophy framework. Rewriting the balance in Wasserstein language does not change the exponents.

Furthermore, even if one could somehow prove a favorable balance for the Wasserstein evolution, the conclusion "enstrophy distribution cannot concentrate to a point" is *insufficient for regularity*. The enstrophy distribution could spread out over a 1D filament while `||omega||_infty` still blows up. Prevention of Wasserstein concentration (from uniform) prevents only the most extreme form of concentration (to a delta), not the less extreme but still fatal forms of singularity.

---

## 5. First Concrete Subproblems

If one wanted to pursue this route despite the above, these are the subproblems that would need honest resolution:

### Subproblem 1: Derive the exact evolution equation for `W_2(rho_omega(t), uniform)`.

The measure `rho_omega` does not evolve by a continuity equation (it has source terms from stretching and dissipation). The Benamou-Brenier formulation of `W_2` requires a continuity equation structure. One must either:
- decompose the evolution into a transport part (for which Wasserstein tools apply) and a source part (which must be estimated separately), or
- work with an unbalanced optimal transport distance (Liero-Mielke-Savare or Chizat-Peyre-Schmitzer-Vialard) that handles mass creation/destruction.

Either way, the evolution equation for the Wasserstein functional will be substantially more complicated than the proposal suggests, and the source terms from stretching will dominate the transport terms in near-singular regimes.

### Subproblem 2: Quantify the Wasserstein dilation rate of the stretching term.

The claim that `div u = 0` bounds the dilation rate needs to be made precise. Divergence-free transport preserves Lebesgue measure, but the stretching term `omega . nabla u . omega` is a *source*, not transport. The relevant question is: what is the Wasserstein-2 cost of the mass creation/destruction pattern induced by `omega . nabla u`? This must be computed for near-singular vorticity configurations (thin tubes, sheets, pancakes) and compared to the contraction rate from `nu Delta omega`.

### Subproblem 3: Determine whether Wasserstein non-concentration implies regularity.

This is the most critical gap. Even if `W_2(rho_omega, uniform) <= C < infty` for all time, this does not obviously imply regularity. One needs a quantitative implication of the form: if the enstrophy distribution stays within Wasserstein distance `R` of uniform, then `||omega||_{L^p}` is bounded for some `p` in a regularity class. Such an implication would itself likely require Sobolev embedding, reintroducing the classical exponent constraints.

### Subproblem 4: Handle the normalization instability.

The measure `rho_omega = |omega|^2 / ||omega||_2^2` depends on the total enstrophy `||omega||_2^2` in the denominator. Near a potential blowup, the total enstrophy is growing (potentially rapidly). The time derivative of `rho_omega` therefore has a term proportional to `-(d/dt ||omega||_2^2) / ||omega||_2^2 * rho_omega`, which couples the Wasserstein evolution to the total enstrophy growth rate. This coupling means the Wasserstein analysis is not independent of the enstrophy analysis --- it is *layered on top of it*, adding complexity without obviously adding power.

### Subproblem 5: Check whether the Bakry-Emery analogy is valid.

The Bakry-Emery criterion gives Wasserstein contraction for diffusions that are gradient flows of convex potentials on manifolds with Ricci curvature bounded below. The viscous term in the vorticity equation is a Laplacian, but the vorticity equation as a whole is not a gradient flow of any known convex functional. The Bakry-Emery analogy is suggestive but may be entirely formal --- one would need to verify that the contraction estimate survives the presence of the stretching term, which is exactly the hard problem.

---

## 6. Classification

**Mostly speculative.**

The route does not have a concrete theorem-object that survives scrutiny. The proposed contraction-dominance lemma, as stated, either encodes BKM circularity in disguise or requires terms that balance at the same scaling exponent in near-singular configurations. The Wasserstein framework is a real mathematical tool, but its application here has not been developed past the level of analogy with the Bakry-Emery theory for linear diffusions. No intermediate technical step has been identified that would constitute progress even if the full program fails.

The route is not "mechanism-facing" because it does not illuminate the mechanism of potential blowup or non-blowup in a new way --- it rephrases the same dissipation-versus-stretching competition in a different metric. It is not "theorem-facing" because the proposed lemma appears to be either false or circular.

---

## 7. Verdict: `weakly promising`

Despite the serious objections above, I stop short of `dead` for two narrow reasons:

1. **The Wasserstein-to-regularity implication (Subproblem 3) has not been fully explored.** It is conceivable, though unlikely, that control of the enstrophy distribution in a Wasserstein-type metric gives regularity information that is genuinely different from `L^p` control of `omega`. If there exists a Wasserstein-type regularity criterion that is strictly weaker than BKM, the route would have a non-circular path. No one has investigated this question carefully.

2. **Unbalanced optimal transport is a relatively new tool.** The Liero-Mielke-Savare / Chizat et al. framework for measures with varying mass is less than a decade old and has not been applied to vorticity dynamics. It is possible (though I would not bet on it) that this framework reveals structure in the competition between stretching and dissipation that is invisible in both the Sobolev and classical Wasserstein settings.

However, the probability that this route leads to a regularity proof is very low. The dimensional scaling argument in Section 4 (both terms are `O(epsilon^{-2})` for a concentrating tube) is essentially a no-go at the level of scaling, and any resolution would require a mechanism that defeats scaling --- which is the whole problem. The route should be treated as a low-priority exploratory direction, not as a serious proof candidate.

**Rating: `weakly promising` --- the framework is not logically dead, but the first concrete lemma is almost certainly false as stated, the BKM circularity reappears in every formulation examined so far, and the dimensional scaling balance offers no margin.**
