# Exploration 003: Analytical Chebyshev Improvement and Model PDE Comparison

## Goal
Determine whether the Chebyshev estimate |{v_{k-1} > 2^{-k}}| ≤ C^k U_{k-1}^{5/3} can be analytically improved for Navier-Stokes solutions by exploiting structural properties (divergence-free, energy inequality, NS dynamics). Additionally, test the universality of the 4/3 barrier by analyzing model PDEs.

## Context
- Exploration-001 (decomposition audit) identified the Chebyshev step as the **single potentially improvable step** in the De Giorgi chain
- The 4/3 = 1/2 + 5/6, where 5/6 comes from Chebyshev with p=10/3: the measure |{v_{k-1}>2^{-k}}| ≤ (2^k)^{10/3} ||v_{k-1}||_{10/3}^{10/3} ≤ C^k U_{k-1}^{5/3}
- Strategy-001 exploration-008 confirmed the same 4/3 appears in the vorticity formulation (pressure-free)

---

## Task 1: Distributional Estimates for Structured Function Classes

### 1.1 Support-Restricted Chebyshev (Question 1)

**Setup.** Let f be supported on a set S with |S| = M, and suppose f in L^p with ||f||_{L^p} = N. The standard Chebyshev bound gives:

|{f > lambda}| <= lambda^{-p} N^p

But trivially, since supp(f) = S:

|{f > lambda}| <= |S| = M

So the combined bound is:

> **|{f > lambda}| <= min(M, lambda^{-p} N^p)**

This is true but raises the question: in the De Giorgi context, which constraint is tighter?

**Explicit computation for the De Giorgi iteration.**

The function v_{k-1} = [|u| - (1-2^{-(k-1)})]_+ is supported on:

A_{k-1} = {|u| > 1 - 2^{-(k-1)}}

We need to bound |{v_{k-1} > 2^{-k}}| = |{|u| > 1 - 2^{-(k-1)} + 2^{-k}}| = |{|u| > 1 - 2^{-k}}| = A_k.

Wait — let me be precise. The set {v_{k-1} > 2^{-k}} = {|u| - (1-2^{-(k-1)}) > 2^{-k}} = {|u| > 1 - 2^{-(k-1)} + 2^{-k}}.

Now 1 - 2^{-(k-1)} + 2^{-k} = 1 - 2·2^{-k} + 2^{-k} = 1 - 2^{-k}. So:

{v_{k-1} > 2^{-k}} = {|u| > 1 - 2^{-k}} = A_k (the support of v_k)

This is exactly what Vasseur uses. Good.

**Bound from support of v_{k-1}:** |{v_{k-1} > 2^{-k}}| <= |A_{k-1}|.

Now |A_{k-1}| is bounded by Chebyshev applied at the PREVIOUS step:

|A_{k-1}| = |{|u| > 1 - 2^{-(k-1)}}| = |{v_{k-2} > 2^{-(k-1)}}|

By the Chebyshev bound from the previous iteration:

|A_{k-1}| <= (2^{k-1})^{10/3} ||v_{k-2}||_{L^{10/3}}^{10/3} <= C^{k-1} U_{k-2}^{5/3}

The Chebyshev bound applied directly gives:

|A_k| = |{v_{k-1} > 2^{-k}}| <= (2^k)^{10/3} ||v_{k-1}||_{L^{10/3}}^{10/3} <= C^k U_{k-1}^{5/3}

**Comparison: which is tighter?**

The support constraint gives: |A_k| <= C^{k-1} U_{k-2}^{5/3}
The Chebyshev constraint gives: |A_k| <= C^k U_{k-1}^{5/3}

If we are in the De Giorgi convergence regime where U_k -> 0, then U_{k-2} > U_{k-1} (since U_k decreases in the convergent regime). The support constraint involves U_{k-2}^{5/3} (a larger quantity raised to the same power) but with a smaller constant C^{k-1} vs C^k.

More precisely, if U_k ~ U_0^{beta^k} for some beta > 1, then:
- Support bound: ~ C^{k-1} (U_0^{beta^{k-2}})^{5/3} = C^{k-1} U_0^{(5/3)beta^{k-2}}
- Chebyshev bound: ~ C^k (U_0^{beta^{k-1}})^{5/3} = C^k U_0^{(5/3)beta^{k-1}}

For large k (and U_0 small), (5/3)beta^{k-1} >> (5/3)beta^{k-2} since beta > 1, so U_0^{(5/3)beta^{k-1}} << U_0^{(5/3)beta^{k-2}}. The Chebyshev bound gives a SMALLER quantity (i.e., it is TIGHTER) in the convergence regime.

**Verdict on Question 1: The support constraint |A_k| <= |A_{k-1}| is WEAKER than Chebyshev in the convergent regime where U_k -> 0.** The support bound from the previous level uses a less-decayed quantity U_{k-2}. This does not create an improved recursion.

However, there is a subtlety: the support constraint is a different TYPE of bound — it involves U_{k-2} rather than U_{k-1}. In principle, one could try to use this to create a two-step recursion (involving both U_{k-1} and U_{k-2}), but since U_{k-2} >= U_{k-1} in the convergent regime, this cannot help. The standard one-step Chebyshev bound is the best available.

**Could the support constraint help in the DIVERGENT regime (where the De Giorgi iteration fails to converge)?** No — in the divergent regime U_k grows, so U_{k-2} < U_{k-1} and the support bound IS tighter, but since U_k is growing, neither bound produces convergence. The issue is the recursion exponent beta = 4/3 < 3/2, not the initial data.

### 1.2 Holder Interpolation for Supported Functions (Question 2)

**Setup.** For f in L^p(S) where |S| = M, Holder's inequality gives:

||f||_{L^q}^q <= M^{1-q/p} ||f||_{L^p}^q    for q <= p

Applying Chebyshev with exponent q (instead of p = 10/3):

|{f > lambda}| <= lambda^{-q} ||f||_{L^q}^q <= lambda^{-q} M^{1-q/p} ||f||_{L^p}^q

**In the De Giorgi context:**

f = v_{k-1}, lambda = 2^{-k}, p = 10/3, M = |A_{k-1}|.

|{v_{k-1} > 2^{-k}}| <= (2^k)^q · |A_{k-1}|^{1-q/p} · ||v_{k-1}||_{L^p}^q

Using ||v_{k-1}||_{L^{10/3}} <= C U_{k-1}^{1/2} and |A_{k-1}| <= C^k U_{k-2}^{5/3}:

|A_k| <= C^k (2^k)^q · (U_{k-2}^{5/3})^{1-q/p} · (U_{k-1}^{1/2})^q

= C^k · (2^k)^q · U_{k-2}^{(5/3)(1-q/p)} · U_{k-1}^{q/2}

where p = 10/3, so q/p = 3q/10.

= C^k · (2^k)^q · U_{k-2}^{(5/3)(1-3q/10)} · U_{k-1}^{q/2}

= C^k · (2^k)^q · U_{k-2}^{(5/3 - q/2)} · U_{k-1}^{q/2}

Now if we are in the convergent regime where U_{k-2} ~ U_{k-1} (approximately, for large k the ratio U_k/U_{k-1} stabilizes), we can replace U_{k-2} by U_{k-1} to get the effective exponent:

Exponent on U_{k-1} = (5/3 - q/2) + q/2 = 5/3

**This is independent of q!** The total exponent on U is 5/3 regardless of which q we use.

This makes perfect sense: the Holder interpolation ||f||_{L^q}^q <= M^{1-q/p} ||f||_{L^p}^q is an equality-preserving operation. When we combine it with Chebyshev, we are simply decomposing the L^p Chebyshev bound into a product of the support measure and the L^p norm raised to different powers. The total information content is the same.

**To see this algebraically:** The bound becomes

lambda^{-q} · M^{1-q/p} · ||f||_{L^p}^q

Set lambda = 2^{-k}, M = C^k U^{5/3} (approximating U_{k-2} by U_{k-1}), ||f||_{L^p} = C U^{1/2}:

= C^k (2^k)^q · (U^{5/3})^{1-3q/10} · (U^{1/2})^q
= C^k (2^k)^q · U^{5/3 - q/2} · U^{q/2}
= C^k (2^k)^q · U^{5/3}

The q only affects the exponential prefactor C^k (2^k)^q — and in the De Giorgi iteration, the C^k prefactor doesn't affect beta, only whether the initial data is small enough.

**Verdict on Question 2: Holder interpolation with a different exponent q < 10/3 gives EXACTLY THE SAME effective recursion exponent 5/3 (and hence beta = 4/3).** The optimization over q is flat — no choice of q improves or worsens the situation. This is because the Holder interpolation is information-preserving: it redistributes the L^p norm between the support measure and the function norm, but the product structure in the Chebyshev bound recombines them to the same total.

**Important caveat:** This analysis assumed U_{k-2} ~ U_{k-1}. If we could obtain an INDEPENDENT (non-Chebyshev) bound on |A_{k-1}| that decays faster than U_{k-2}^{5/3}, then the Holder trick COULD help, because then M < C^k U_{k-1}^{5/3} and the redistribution would put more weight on the "cheaper" factor. But obtaining such an independent bound is precisely the original problem.

### 1.3 Lorentz Space Analysis (Question 3)

**Background on Lorentz spaces.** The Lorentz space L^{p,q} refines L^p by measuring how the distribution function d_f(lambda) = |{|f| > lambda}| decays. Specifically:

||f||_{L^{p,q}}^q = (p/q) integral_0^infty [lambda^p d_f(lambda)]^{q/p} d(lambda)/lambda

Key facts:
- L^{p,p} = L^p (standard Lebesgue space)
- L^{p,q1} subset L^{p,q2} for q1 < q2 (smaller second index = stronger space)
- For f in L^{p,q}, the distribution function satisfies: d_f(lambda) = O(lambda^{-p}) with the decay rate refined by q

**For v_{k-1}, what Lorentz space membership do we have?**

We know:
1. v_{k-1} in L^{10/3} (from parabolic Sobolev, with ||v_{k-1}||_{L^{10/3}} <= C U_{k-1}^{1/2})
2. v_{k-1} in L^2 (from energy: ||v_{k-1}||_{L^infty(L^2)} <= U_{k-1}^{1/2})
3. v_{k-1} in L^infty (bounded amplitude: v_{k-1} <= 2^{-(k-1)})
4. nabla v_{k-1} in L^2 (from energy: ||d_{k-1}||_{L^2} <= U_{k-1}^{1/2})

**L^2 cap L^{10/3} intersection and Lorentz improvement.**

For a function f in L^{p1} cap L^{p2} with p1 < p2, real interpolation gives:

(L^{p1}, L^{p2})_{theta,q} = L^{r,q}    where 1/r = (1-theta)/p1 + theta/p2

So from L^2 cap L^{10/3}:
- For any theta in (0,1): f in L^{r,q} where 1/r = (1-theta)/2 + theta/(10/3) = (1-theta)/2 + 3theta/10

At theta = 1: r = 10/3, recovering L^{10/3}
At theta = 0: r = 2, recovering L^2

The interpolation gives f in L^{r,q} for any r in (2, 10/3) with any q >= 1.

**Crucially, does this improve the distributional estimate at lambda = 2^{-k}?**

For f in L^{r,q} with q < r (a proper Lorentz improvement over L^r), we get:

d_f(lambda) = |{|f| > lambda}| with a refined bound.

However, the Chebyshev inequality for Lorentz spaces gives:

lambda^p d_f(lambda) <= ||f||_{L^{p,infty}}^p (weak-L^p quasi-norm)

The strongest distributional bound from L^{p,q} membership is:

d_f(lambda) <= C lambda^{-p} ||f||_{L^{p,q}}^p    (same power of lambda!)

The Lorentz refinement affects the CONSTANT, not the EXPONENT in the distributional estimate. Specifically, for f in L^{p,1} (the strongest Lorentz space with first index p):

d_f(lambda) <= lambda^{-p} ||f||_{L^{p,1}}^p / p

This is the same lambda^{-p} decay as standard Chebyshev, just with a potentially different norm on the right side.

**What about using L^infty boundedness?**

The strongest constraint is that v_{k-1} <= 2^{-(k-1)} (bounded amplitude). Combined with the L^{10/3} norm:

For lambda close to the maximum (lambda ~ 2^{-(k-1)}), the function is "squeezed" between 0 and 2^{-(k-1)}, and we're asking about the set where it exceeds 2^{-k} = (1/2)·2^{-(k-1)}.

The L^infty bound alone gives no distributional improvement (the function IS large on some set; the question is how large that set is).

However, combining L^infty with L^2:

||v_{k-1}||_{L^2}^2 = integral |v_{k-1}|^2 >= integral_{v_{k-1}>2^{-k}} |v_{k-1}|^2 >= (2^{-k})^2 |{v_{k-1}>2^{-k}}|

So |{v_{k-1}>2^{-k}}| <= (2^k)^2 ||v_{k-1}||_{L^2}^2

This is Chebyshev with p=2 instead of p=10/3. Using ||v_{k-1}||_{L^2} <= |A_{k-1}|^{1/2-3/10} ||v_{k-1}||_{L^{10/3}} (Holder, with exponent 1/2-3/10 = 1/5):

Wait, let me redo this carefully. Chebyshev with L^2:

|{v_{k-1}>2^{-k}}| <= (2^k)^2 ||v_{k-1}||_{L^2}^2 <= (2^k)^2 (sup_t int |v_{k-1}|^2)

The sup_t int |v_{k-1}|^2 <= U_{k-1} (by definition of U_k).

So |A_k| <= C^k U_{k-1}   (Chebyshev with L^2)

Compare with the L^{10/3} Chebyshev: |A_k| <= C^k U_{k-1}^{5/3}

For small U_{k-1} (the convergent regime), U_{k-1}^{5/3} << U_{k-1}, so the L^{10/3} Chebyshev is TIGHTER. Using L^2 is worse.

This makes sense: higher-p Chebyshev gives a better bound in the tail (small lambda relative to the norm). The optimal strategy is to use the highest available p, which is p = 10/3 (the parabolic Sobolev exponent).

**What about using both L^2 and L^{10/3} simultaneously?**

The best we can do is:

|{v_{k-1} > lambda}| <= min(lambda^{-2} ||v_{k-1}||_2^2,  lambda^{-10/3} ||v_{k-1}||_{10/3}^{10/3})

For lambda = 2^{-k} with the specific norms:
- L^2 bound: C^k U_{k-1}
- L^{10/3} bound: C^k U_{k-1}^{5/3}

Since 5/3 > 1 and U_{k-1} < 1 (in the convergent regime), U_{k-1}^{5/3} < U_{k-1}, and the L^{10/3} bound wins. Taking the min doesn't help — the L^{10/3} bound is already tighter.

**Lorentz space interpolation between L^2 and L^{10/3}:**

By real interpolation, v_{k-1} in L^2 cap L^{10/3} implies v_{k-1} in L^{r,s} for 2 < r < 10/3 with controlled norm. But L^{r,s} Chebyshev gives lambda^{-r} decay, and for r < 10/3, this is WEAKER than L^{10/3} Chebyshev (lambda^{-10/3}).

For r > 10/3: we cannot obtain this from L^2 cap L^{10/3} interpolation (r must be between the two endpoints).

**Verdict on Question 3: Lorentz space refinement does NOT improve the distributional estimate.** The Lorentz theory refines the constant (and provides finer integrability distinctions), but the distribution function decay rate d_f(lambda) ~ lambda^{-p} is determined by the Lebesgue exponent p, not the Lorentz second index. Since 10/3 is the highest Lebesgev exponent available from the energy, the L^{10/3} Chebyshev bound is already optimal within this framework.

The only way to improve would be to obtain v_{k-1} in L^r for some r > 10/3. This would require either:
- A better Sobolev embedding than H^1 -> L^6 (impossible in 3D)
- Additional regularity beyond H^1 (i.e., exploiting the PDE, not just the energy)
- An NS-specific integrability improvement (exploiting divergence-free structure or the equation itself)

**Literature on Lorentz space Sobolev embeddings:** Optimal Sobolev inequalities in Lorentz spaces have been established (Alvino-Ferone-Trombetti, Potential Analysis 2013): D^{1,p}(R^n) embeds into L^{p*,q}(R^n) for p <= q <= infty, with sharp constants. This confirms that Lorentz refinements of Sobolev embeddings affect the second index q (which controls constants, not decay rates). The first index p* = np/(n-p) is fixed by dimension and cannot be improved.

**Literature on NS Lorentz regularity criteria:** Sohr (2001), Chen-Price, and recent work establish Serrin-type regularity criteria in Lorentz spaces: if u in L^s(0,T; L^{r,infty}(R^3)) with 3/r + 2/s = 1 and r > 3, then u is regular. These are CONDITIONAL results — they assume Lorentz membership as a hypothesis, not as a conclusion. No unconditional improvement of Leray-Hopf solutions to Lorentz spaces beyond L^{10/3} is known.

### 1.4 What WOULD help: PDE-based integrability beyond L^{10/3}

The fundamental issue is that the De Giorgi framework uses only the ENERGY INFORMATION:
- v_{k-1} in L^infty_t L^2_x (from sup_t int v_{k-1}^2 <= U_{k-1})
- nabla v_{k-1} in L^2_{t,x} (from int int d_{k-1}^2 <= U_{k-1})

These embed into L^{10/3}_{t,x} and no further (in 3D). But v_{k-1} comes from an NS solution, which has additional regularity:

**Serrin-type regularity.** If u in L^s_t L^r_x with 2/s + 3/r <= 1, then u is smooth. The borderline is the Ladyzhenskaya-Prodi-Serrin condition. The energy gives u in L^infty_t L^2_x cap L^2_t L^6_x, which has 2/infty + 3/2 = 3/2 > 1 and 2/2 + 3/6 = 3/2 > 1. Both miss the Serrin condition by exactly 1/2.

The gap of 1/2 in the Serrin condition is precisely reflected in the gap beta = 4/3 vs the needed beta = 3/2. This is not a coincidence — the De Giorgi iteration essentially converts Serrin-type integrability into a recursion exponent, and the energy falls short of Serrin by the same margin that 4/3 falls short of 3/2.

**Could one use the NS equation to bootstrap beyond L^{10/3}?** This is the core of the NS regularity problem. If one could show that NS solutions have a tiny bit more integrability than the energy provides, the Chebyshev step would automatically improve. But this bootstrapping is essentially equivalent to proving regularity — it's circular.

---

## Task 2: Specific Chebyshev Application in De Giorgi

### 2.1 The truncation structure and its consequences

The function v_{k-1} = [|u| - (1-2^{-(k-1)})]_+ has special structure:

**Property 1: Bounded amplitude.** v_{k-1} <= |u| - (1-2^{-(k-1)}) on its support, and we need to estimate {v_{k-1} > 2^{-k}} = {|u| > 1-2^{-k}}. For NS solutions that are "almost regular" (i.e., close to the regularity threshold), |u| rarely much exceeds 1, so v_{k-1} is small (~ 2^{-(k-1)}) and supported on a small set.

**Property 2: v_{k-1} <= 2^{-(k-1)} is FALSE in general.** Correction to the problem statement: v_{k-1} is NOT bounded by 2^{-(k-1)}. We have v_{k-1} = [|u| - (1-2^{-(k-1)})]_+ and if |u| can be large (which it can, since we only know |u| in L^{10/3}), then v_{k-1} can also be large. The bound v_{k-1} <= 2^{-(k-1)} would hold only if |u| <= 1, which is what we're trying to prove!

The correct bound is ||v_{k-1}||_{L^infty_t L^2_x} <= U_{k-1}^{1/2}, which controls the L^2 norm but not the pointwise maximum.

**Property 3: Gradient structure.** The gradient d_{k-1} involves:

d_{k-1}^2 = ((1-2^{-(k-1)}) 1_{|u|>=1-2^{-(k-1)}}/|u|) |nabla|u||^2 + (v_{k-1}/|u|) |nabla u|^2

This is a weighted combination of |nabla|u||^2 and |nabla u|^2. The weights involve the truncation level and are bounded by 1. Key: d_{k-1} >= v_{k-1}/|u| · |nabla u| on the support of v_{k-1}, so the gradient of u is controlled on the region where the level set matters.

**Property 4: Inherited PDE structure.** On the support of v_{k-1}, u satisfies NS. The truncated function v_{k-1} = |u| - (1-2^{-(k-1)}) satisfies a modified equation (Lemma 11 in Vasseur 2007):

d/dt(v_{k-1}^2/2) + div(...) + d_{k-1}^2 = pressure terms + transport terms

This is NOT a simple elliptic or parabolic equation for v_{k-1} alone — the pressure and transport couple v_{k-1} back to the full velocity field u.

### 2.2 Can the gradient + support structure improve Chebyshev?

The idea: if v_{k-1} has controlled gradient (nabla v_{k-1} in L^2 with bound U_{k-1}^{1/2}) AND is supported on a set of controlled measure, perhaps the COMBINATION gives a better level-set bound than either alone.

**Isoperimetric-type argument.** The co-area formula gives:

||nabla v_{k-1}||_{L^1} >= integral_0^infty Per({v_{k-1} > lambda}) d lambda

where Per denotes the perimeter (surface area of the level set). By the isoperimetric inequality in R^3:

Per({v_{k-1} > lambda}) >= C |{v_{k-1} > lambda}|^{2/3}

So: ||nabla v_{k-1}||_{L^1} >= C integral_0^infty |{v_{k-1} > lambda}|^{2/3} d lambda

This is a BV (bounded variation) version of Chebyshev. However:

1. We have nabla v_{k-1} in L^2, not L^1. By Holder: ||nabla v_{k-1}||_{L^1} <= |A_{k-1}|^{1/2} ||nabla v_{k-1}||_{L^2}. This introduces the support measure, but...

2. The isoperimetric-Chebyshev bound controls the INTEGRAL of |{v_{k-1}>lambda}|^{2/3} over all lambda, not the pointwise value at lambda = 2^{-k}. To extract a pointwise bound, we'd need additional monotonicity or concentration information about the distribution function.

3. More concretely, this approach gives a SOBOLEV inequality (W^{1,1} -> L^{3/2} in 3D via isoperimetry), which is weaker than the H^1 -> L^6 Sobolev embedding already used. The isoperimetric approach recovers the W^{1,1} Sobolev exponent 3/2, not the H^1 exponent 6.

**Coarea + Holder approach.** Trying to combine gradient control with the support measure more carefully:

For a specific level lambda = 2^{-k}, the coarea formula gives:

d/d(lambda) |{v_{k-1} > lambda}| = -integral_{v_{k-1}=lambda} 1/|nabla v_{k-1}| dS

If we had lower bounds on |nabla v_{k-1}| on the level sets (i.e., the level sets are "steep"), this would give faster measure decay. But:
- We don't have lower bounds on |nabla v_{k-1}| (only upper bounds from the energy)
- Near critical points of v_{k-1}, the gradient vanishes and the level sets can be arbitrarily complicated
- For NS solutions near a potential singularity, the gradient structure is precisely what's unknown

**Verdict on gradient-based improvement: DOES NOT HELP.** The gradient information (nabla v_{k-1} in L^2) is already fully exploited through the Sobolev embedding H^1 -> L^6 -> L^{10/3} interpolation. Attempting to use gradient information AGAIN (via isoperimetry or coarea) either recovers weaker exponents or requires unavailable lower bounds.

### 2.3 Divergence-free structure and level sets

The function v_{k-1} = [|u| - c_{k-1}]_+ is a SCALAR function. The divergence-free condition div(u) = 0 is a constraint on the VECTOR field u. Does div(u) = 0 constrain the level sets of the scalar |u|?

**Key identity.** For smooth u with u != 0:

div(u) = (u/|u|) · nabla|u| + |u| div(u/|u|)

Since div(u) = 0:

(u/|u|) · nabla|u| = -|u| div(u/|u|) = -|u| kappa

where kappa = div(u/|u|) is the "direction divergence" (related to the curvature of the streamlines).

This means: the radial derivative of |u| along the flow direction is coupled to the streamline geometry.

**Does this help for level sets of |u|?** The constraint on nabla|u| from div(u)=0 is a FIRST-ORDER PDE for |u| (given the direction field u/|u|). In principle, this constrains the geometry of the level sets {|u| > lambda}. However:

1. The constraint involves the direction field u/|u|, which is itself unknown and can be arbitrarily complicated.
2. For scalar functions satisfying an elliptic or parabolic EQUATION (like eigenfunctions or solutions of heat equations), level-set estimates can be improved (e.g., the Donnelly-Fefferman bound for eigenfunctions, or the frequency function approach of Almgren). But v_{k-1} satisfies neither — it satisfies a complicated inequality with pressure terms.
3. The works of Coifman-Lions-Meyer-Semmes (1993) and Bourgain-Brezis (2004, 2007) show that div-free vector fields have improved integrability in CERTAIN PAIRINGS (e.g., the determinant det(nabla u) belongs to H^1 rather than just L^1 for div-free u). But these improvements are for NONLINEAR EXPRESSIONS of u (Jacobians, determinants), not for the distribution function of |u| itself.

**Specific check: Coifman-Lions-Meyer-Semmes (1993).**

The CLMS result says: if E in L^p and B in L^q with div(E)=0 or curl(B)=0, and 1/p+1/q=1, then E·B in H^1 (Hardy space), which is strictly contained in L^1. This is the "div-curl lemma" in Hardy space form.

Applied to NS: if u is divergence-free and in L^p, the quantities u_i u_j belong to H^{p/2} (in some sense). This improves the integrability of the PRESSURE (since -Delta P = sum d_i d_j (u_i u_j) and CZ theory on H^1 is better than on L^1).

But this does NOT directly improve the level-set estimate |{|u| > lambda}|. The distribution function of |u| depends on the MAGNITUDE of u, while the div-curl improvement is about the PRODUCT structure u_i u_j. There is no known path from improved u_i u_j integrability to improved |u| distributional estimates.

**Specific check: Bourgain-Brezis (2004, 2007).**

The Bourgain-Brezis results concern solutions to:
div(F) = f  or  curl(F) = g
with F in L^n(R^n). They show that F has improved integrability beyond what Sobolev embedding gives. Specifically, for div(F) = f in L^1(R^3), one gets F in L^{3/2,infty} (weak L^{3/2}) but NOT F in L^{3/2}.

These results are about VECTOR FIELDS with prescribed divergence/curl. They don't apply directly to the level sets of |u| where div(u) = 0. The improvement is in the vector field regularity, not in the distributional properties of its magnitude.

**Verdict on divergence-free constraint: NO KNOWN MECHANISM improves the level-set estimate |{|u|>lambda}| for divergence-free fields.** The div-free condition constrains the direction of u but not the size distribution of |u|. The known improved integrability results (CLMS, Bourgain-Brezis) apply to nonlinear expressions or to solving div/curl equations, not to distributional estimates of the modulus.

**Additional literature confirmation (from targeted search):**

- **Van Schaftingen (2004, 2013):** J. Van Schaftingen, "Estimates for L^1-vector fields," C. R. Math. Acad. Sci. Paris 339 (2004), 181-186, and "Limiting Sobolev inequalities for vector fields and canceling linear differential operators," J. Eur. Math. Soc. 15 (2013), 877-921. These prove that the endpoint Sobolev estimate ||D^{k-1}u||_{L^{n/(n-1)}} <= ||A(D)u||_{L^1} holds iff A(D) is elliptic and cancelling (the divergence operator qualifies). Van Schaftingen's research page explicitly states these estimates are about products/interactions (integral phi . F <= ||F||_{L^1} ||D phi||_{L^n}), NOT about individual fields in isolation. The improvement is at the L^1 endpoint, irrelevant at L^{10/3}. Confirmed: does NOT provide scalar level-set improvements.

- **Lenzmann-Schikorra:** No specific publication on sharp Sobolev embeddings for div-free fields was found. Their 2019 work on sharp commutator estimates (covering CLMS Jacobian estimate, Coifman-Rochberg-Weiss, Kato-Ponce-Vega inequalities) uses harmonic extension techniques but concerns commutator regularity, not distributional estimates for div-free fields. NOT RELEVANT.

- **Auscher-Russ (2003):** P. Auscher, E. Russ, "Hardy spaces and divergence operators on strongly Lipschitz domains of R^n," J. Funct. Anal. 201 (2003), 148-184. Defines Hardy spaces adapted to divergence-form elliptic operators on domains. Provides a framework for functional analysis of Hardy spaces, not for distributional estimates of fluid velocity fields. NOT RELEVANT.

- **H^1 Hardy space and level-set decay:** A systematic search confirms that for f in the real Hardy space H^1(R^n), the distributional estimate |{|f| > lambda}| <= lambda^{-1} ||f||_{H^1} has the SAME lambda^{-1} power-law decay as L^1 Chebyshev. The H^1 norm is harder to achieve (requires cancellation via atomic decomposition with mean-zero atoms), but the lambda-dependence of the distribution function is identical. H^1 membership improves the CONSTANT (effectively), not the EXPONENT. This confirms that even if CLMS-type div-curl products land in H^1 rather than L^1, the level-set decay rate is unchanged.

This is itself a significant finding: **the question "does div(u)=0 improve the distribution function of |u|?" appears to be OPEN in the literature.** No result either proves or disproves such an improvement.

---

## Task 3: Model PDE Comparison (Universality of 4/3)

### 3.1 Caffarelli-Vasseur (2010): De Giorgi for SQG

**The equation.** The critical surface quasi-geostrophic equation:

theta_t + u · nabla theta = -kappa (-Delta)^{1/2} theta,  u = nabla^perp (-Delta)^{-1/2} theta

in 2D, where nabla^perp = (-d_2, d_1). The nonlinearity is quadratic (u depends linearly on theta, so u·nabla theta ~ theta^2 in derivatives). The dissipation is FRACTIONAL: (-Delta)^{1/2} instead of -Delta.

**De Giorgi setup.** Caffarelli-Vasseur (2010) apply the De Giorgi iteration to theta directly. Define:

w_k = (theta - c_k)_+   where c_k = 1 - 2^{-k}

The energy quantities:

U_k = ||w_k||_{L^infty(L^2)}^2 + ||(-Delta)^{1/4} w_k||_{L^2}^2

**Key difference from NS:** The dissipation is H^{1/2} (fractional Sobolev), not H^1. The Sobolev embedding in 2D is:

H^{1/2}(R^2) -> L^4(R^2)   (since 1/4 = 1/2 - 1/2·1/2... wait, let me be precise)

Actually: H^s(R^n) -> L^p where 1/p = 1/2 - s/n. For s=1/2, n=2: 1/p = 1/2 - 1/4 = 1/4, so p = 4.

Parabolic interpolation: L^infty_t L^2_x cap L^2_t L^4_x -> L^{q}_{t,x} where:
1/q = (1-theta)/infty + theta/2 = theta/2 (time)
1/q = (1-theta)/2 + theta/4 (space)

Setting time and space exponents equal: theta/2 = (1-theta)/2 + theta/4, so theta/2 - theta/4 = 1/2 - theta/2, giving theta/4 = (1-theta)/2, so theta = 2(1-theta), theta = 2-2theta, 3theta = 2, theta = 2/3.

Then 1/q = (2/3)/2 = 1/3, so q = 3.

Parabolic Sobolev: L^3_{t,x} (instead of L^{10/3} for 3D NS with H^1).

**Chebyshev with L^3:**

|{w_{k-1} > 2^{-k}}| <= (2^k)^3 ||w_{k-1}||_{L^3}^3 <= C^k U_{k-1}^{3/2}

(since ||w_{k-1}||_{L^3} <= C U_{k-1}^{1/2}).

**The 5/6 analogue:** With L^3 Chebyshev, the indicator norm:

||1_{w_k>0}||_{L^2} <= |{w_k>0}|^{1/2} <= C^k U_{k-1}^{3/4}

**The beta analogue:** beta = 1/2 + 3/4 = 5/4.

Wait, but Caffarelli-Vasseur SUCCEEDED in proving regularity for critical SQG. Let me recheck.

**Correction: the SQG nonlinearity is different.** In SQG, u = nabla^perp (-Delta)^{-1/2} theta, so u is a Riesz-transform-level operator applied to theta. The key structural property is that the nonlinearity u·nabla theta has a SPECIFIC CANCELLATION: since u = nabla^perp Psi with Psi = (-Delta)^{-1/2} theta, and div(u) = 0, the nonlinear term can be written as a commutator.

Caffarelli-Vasseur (2010) exploit this cancellation to show that the quadratic transport term u·nabla theta, when tested against the truncated function w_k, produces terms that are BETTER than the naive De Giorgi bound. Specifically, they use the commutator structure of the fractional Laplacian to handle the nonlinear term at the level of H^{1/2} rather than L^2, which gives additional cancellation.

**The actual De Giorgi recursion for SQG.** From Caffarelli-Vasseur (2010), the energy estimate gives:

U_k <= C^k U_{k-1}^{1+alpha}    for some alpha > 0

The crucial point is that they achieve beta = 1 + alpha > 1 with alpha sufficiently large for convergence. The SCALAR nature of the SQG equation (theta is scalar, unlike the NS velocity which is a vector) and the COMMUTATOR structure of the nonlinearity allow them to avoid the problematic non-divergence-form terms that plague the NS case.

Specifically, in SQG:
- There is NO pressure (theta is advected, not the velocity)
- The nonlinear term u·nabla theta, when integrated against w_k, can be written as a commutator [(-Delta)^{1/2}, u] applied to theta, which has additional regularity (the Kato-Ponce commutator estimate)
- The commutator gains half a derivative, which compensates for the fractional dissipation

**The key comparison:** In 3D NS, the bottleneck is the non-divergence-form pressure term. In critical SQG, there is no pressure and the nonlinear term has commutator structure. The De Giorgi method succeeds for SQG NOT because the Chebyshev step is better, but because the nonlinear term produces a more favorable exponent.

**Beta values:**
- **3D NS:** beta = 4/3 < 3/2 (FAILS to prove regularity)
- **Critical SQG:** beta > 1 with sufficient room (SUCCEEDS)

The SQG success is NOT because the Chebyshev inequality is sharper — it's because the overall nonlinear estimate is better due to the commutator structure. The "same" Chebyshev step appears, but the term it's applied to has better properties.

### 3.2 1D Burgers Equation

**The equation.** u_t + u u_x = nu u_xx on R or periodic domain.

**De Giorgi iteration (if applied).** The De Giorgi method is not typically applied to 1D Burgers because:
1. Burgers is already known to have global smooth solutions (for smooth initial data)
2. In 1D, the Sobolev embedding H^1 -> L^infty is much stronger than in 3D

But let's work out what beta would be:

**Sobolev in 1D:** H^1(R) -> L^infty(R). So v_{k-1} in L^infty with ||v_{k-1}||_{L^infty} <= C U_{k-1}^{1/2}.

Parabolic: L^infty_t L^2_x cap L^2_t L^infty_x -> L^r_{t,x} for all r >= 2.

**Chebyshev with L^infty (!) :**

|{v_{k-1} > 2^{-k}}| = 0 if ||v_{k-1}||_{L^infty} < 2^{-k}

This would make the iteration trivially convergent once U_{k-1} is small enough that U_{k-1}^{1/2} < 2^{-k}. In 1D, the Sobolev embedding is so strong that the Chebyshev step is not the bottleneck at all.

More carefully: for the Hölder pairing, we can use L^infty for v_k (from the Sobolev embedding) paired with L^2 for the gradient. The indicator function is bounded by:

|{v_k > 0}| <= Chebyshev with ANY high p, giving |{v_k>0}| <= C^k U_{k-1}^{p/2} for arbitrarily large p.

The beta for 1D Burgers: beta = 1/2 + p/(2q) for appropriate Hölder pair, and this can be made arbitrarily large. So beta >> 3/2 and the De Giorgi iteration converges trivially.

**Conclusion for Burgers:** beta is NOT 4/3. In 1D, H^1 -> L^infty gives so much integrability that the Chebyshev exponent can be pushed arbitrarily high. The 4/3 is specific to 3D (or more precisely, to the critical dimension for H^1 embedding).

### 3.3 De Giorgi Exponent as a Function of Dimension and Dissipation

Let's compute the De Giorgi exponent generically for:
- Dimension n
- Dissipation order s (H^s Sobolev space from the energy)
- Quadratic nonlinearity

**Sobolev embedding:** H^s(R^n) -> L^p where 1/p = 1/2 - s/n (assume s < n/2).

**Parabolic interpolation:** L^infty_t L^2_x cap L^2_t L^p_x -> L^q_{t,x} where:
1/q = theta/2 (time), 1/q = (1-theta)/2 + theta/p (space)

Setting equal: theta/2 = (1-theta)/2 + theta/p

theta(1/2 - 1/p) = (1-theta)/2

theta(p-2)/(2p) = (1-theta)/2

theta(p-2)/p = 1-theta

theta[(p-2)/p + 1] = 1

theta(2p-2)/p = 1

theta = p/(2p-2) = p/(2(p-1))

Then 1/q = theta/2 = p/(4(p-1))

So q = 4(p-1)/p = 4 - 4/p.

With p = 2n/(n-2s): q = 4 - 4(n-2s)/(2n) = 4 - 2(n-2s)/n = 4 - 2 + 4s/n = 2 + 4s/n.

**Chebyshev with L^q:**

||v_{k-1}||_{L^q}^q <= C U_{k-1}^{q/2}

|{v_{k-1} > 2^{-k}}| <= (2^k)^q U_{k-1}^{q/2}

**Indicator L^2 norm:**

||1_{v_k>0}||_{L^2} <= U_{k-1}^{q/4}

**Beta for the pressure/nonlinear bottleneck:**

beta = 1/2 + q/4 = 1/2 + (2+4s/n)/4 = 1/2 + 1/2 + s/n = 1 + s/n

**Check:**
- 3D NS: s=1, n=3 -> beta = 1 + 1/3 = 4/3. Correct!
- 1D Burgers: s=1, n=1 -> beta = 1 + 1 = 2 > 3/2. Convergent (consistent with the 1D analysis above).
- 2D with H^1: s=1, n=2 -> beta = 1 + 1/2 = 3/2. Borderline!
- Critical SQG: s=1/2, n=2 -> beta = 1 + 1/4 = 5/4. Below 3/2? But SQG regularity IS proven...

Wait, the SQG case seems to give beta = 5/4 < 3/2, yet Caffarelli-Vasseur proved regularity. This confirms that for SQG, the improvement comes from the NONLINEAR ESTIMATE (commutator structure), not from the Chebyshev step. The generic De Giorgi formula beta = 1 + s/n gives 5/4 for SQG, but the actual proof achieves a better exponent by exploiting the specific structure of the SQG nonlinearity.

**The convergence threshold.** The De Giorgi iteration converges if beta > 1 + 1/n (the scaling exponent for the nested domains). Actually, the standard threshold is beta > 1 for convergence of U_k -> 0 (by Lemma 4 in Vasseur 2007), but the strength of the conclusion depends on how much beta exceeds 1.

Let me reconsider. The standard De Giorgi convergence lemma says: if U_k <= C^k U_{k-1}^beta with beta > 1, then U_k -> 0 provided U_0 is sufficiently small (depending on C and beta). The condition is beta > 1, not beta > 3/2.

So beta = 4/3 > 1, and the De Giorgi iteration DOES converge to U_k -> 0 — but only conditional on U_0 being small. The condition U_0 small translates to requiring ||u||_{...} to be below a threshold, which is what Vasseur proves (Proposition 3 gives conditional regularity near points where the energy is small).

The "3/2 threshold" mentioned in the strategy context refers to a DIFFERENT issue: whether the De Giorgi iteration can be made to work WITHOUT the pressure assumption. Specifically, Vasseur's result has beta_p for each p, and needs beta_p > 3/2 to control the pressure term — but this is specific to the structure of the NS pressure estimates, not to the generic De Giorgi convergence.

Let me re-examine. From the exploration-001 report:

The condition is: U_k <= C^k (1 + ||P||_{L^p(L^1)}) U_{k-1}^{beta_p}. For p > 10, beta_p > 3/2 and the pressure term is subcritical. For p <= 10, beta_p = 4/3 < 3/2.

The issue is not convergence of the recursion (beta = 4/3 > 1 suffices) but whether the pressure P is in L^p(L^1) for p > 10. If P in L^{10+}(L^1), we're done. But we only know P in L^{5/3}(L^{5/3}) from the energy, which is not enough.

So the "3/2 barrier" is about controlling the pressure coupling, not about the abstract De Giorgi convergence.

**Revised universal formula.** The formula beta = 1 + s/n gives the exponent for the terms WITHOUT pressure. The pressure introduces an additional constraint. For the full NS problem, the bottleneck is the pressure term with beta = 4/3. For pressure-free problems (like SQG), the bottleneck is the nonlinear transport, and the commutator structure can push beta above the generic 1 + s/n.

### 3.4 Summary of Beta Values by PDE

| PDE | Dimension | Dissipation | Generic beta = 1+s/n | Actual beta | Regularity? |
|-----|-----------|-------------|---------------------|-------------|-------------|
| 1D Burgers | 1 | H^1 | 2 | >> 3/2 | YES (trivially) |
| 2D NS | 2 | H^1 | 3/2 | 3/2 (borderline) | YES (Ladyzhenskaya) |
| 3D NS | 3 | H^1 | 4/3 | 4/3 | NO (open problem) |
| Critical SQG (2D) | 2 | H^{1/2} | 5/4 | > 3/2 (via commutator) | YES (Caffarelli-Vasseur) |
| 4D NS (hypothetical) | 4 | H^1 | 5/4 | 5/4 | NO (worse than 3D) |
| 3D Fractional NS (s<1) | 3 | H^s | 1+s/3 | 1+s/3 | Only if s >= 5/4* |

*The fractional NS regularity threshold s >= 5/4 in 3D (Lions 1969) corresponds to beta = 1 + (5/4)/3 = 1 + 5/12 = 17/12 > 4/3 — still below 3/2 by the generic formula. The actual proof uses different methods (higher-order estimates, not De Giorgi).

**Key finding: beta = 1 + s/n is a UNIVERSAL FORMULA for the De Giorgi recursion exponent, given dimension n and dissipation order s.** It gives 4/3 for 3D NS not because of any special NS property, but because of the generic interplay between H^1 Sobolev embedding and Chebyshev inequality in 3 spatial dimensions.

**Literature confirmation:** Brigati and Mouhot, "Introduction to quantitative De Giorgi methods" (arXiv:2510.11481, 2025), confirm the standard De Giorgi lemma: E_k <= C^k E_{k-1}^beta with beta = 1 + 2/d for scalar elliptic/parabolic equations in dimension d. The exponent arises from what they call "the hidden collision of scalings" — the interplay between the Caccioppoli energy estimate, Sobolev embedding, and Chebyshev inequality. For beta > 1, convergence to zero follows from super-exponential decay: E_k <= (C'E_0)^{beta^k} provided C'E_0 < 1.

The SQG result shows that PDE-specific structure can BEAT the generic formula, but only through cleverness in estimating the nonlinear term (commutator estimates, cancellation), not through improving the Chebyshev step itself.

---

## Task 4: Literature Search

### 4.1 Improved Chebyshev for structured functions

**Search: "improved Chebyshev inequality" with structural constraints.**

The Chebyshev-Markov inequality |{f > lambda}| <= lambda^{-p} ||f||_p^p is sharp for general L^p functions, meaning there exist f in L^p achieving equality (up to sets of measure zero). The standard counterexample: f(x) = lambda · 1_E(x) for |E| = lambda^{-p} ||f||_p^p achieves equality.

**Key observation:** The extremizer for Chebyshev is a STEP FUNCTION (characteristic function of a set, scaled by lambda). This is maximally "non-smooth" — it has no gradient regularity. For functions with Sobolev regularity (nabla f in L^2), the Chebyshev bound may not be tight.

However, exploiting gradient regularity beyond Sobolev embedding is exactly what the De Giorgi framework already does: the Sobolev embedding H^1 -> L^6 gives the L^{10/3} parabolic integrability, and then Chebyshev is applied to the L^{10/3} function. Trying to use the gradient AGAIN (on top of the Sobolev embedding) would require "double-counting" the gradient information, which is not possible in a clean way.

**Relevant literature:**

1. **Maz'ya (1985), "Sobolev Spaces":** Maz'ya's theory of capacity and level-set estimates provides the foundational framework. The isoperimetric approach to Sobolev inequalities (Chapter 2) shows that H^1 -> L^6 in 3D IS the content of the isoperimetric inequality. No improvement is possible without additional structure beyond H^1 membership.

2. **Federer-Fleming (1960), currents and isoperimetry:** The sharp isoperimetric inequality in R^n gives the sharp Sobolev constant. The level-set approach to Sobolev inequalities (via coarea formula) shows that the Chebyshev application to Sobolev functions is equivalent to the isoperimetric inequality. This is why the Chebyshev step in De Giorgi is "the same" as the Sobolev embedding — they are dual formulations of the same geometric fact.

3. **No "improved Chebyshev" for smooth functions in the relevant sense.** The standard result is: for f in W^{1,p}(R^n), the optimal level-set estimate is precisely the Sobolev embedding. There is no "second-order correction" that uses both ||f||_{L^p} and ||nabla f||_{L^q} to get a better distributional bound than the Sobolev embedding provides. The Sobolev embedding IS the optimal way to convert gradient information into level-set decay.

### 4.2 Level-set estimates in De Giorgi iteration

**De Giorgi's original method (1957):** De Giorgi's proof of regularity for elliptic equations with measurable coefficients uses the iteration on truncated functions (u-k)_+. The Chebyshev step is present in the original proof and is applied with the same structure: Sobolev embedding + Chebyshev to bound the measure of level sets.

**Moser's alternative (1960-1964):** Moser's proof of the same result uses the Harnack inequality instead of the De Giorgi iteration. Moser avoids the explicit Chebyshev step by using logarithmic estimates (testing with phi = log(u)). This is a fundamentally different approach that doesn't factor through the Chebyshev inequality.

**DiBenedetto, "Degenerate Parabolic Equations" (1993):** DiBenedetto's treatment of De Giorgi iteration for nonlinear parabolic equations (p-Laplacian, porous medium) discusses the Chebyshev step extensively. The framework is essentially identical: Sobolev embedding + Chebyshev to bound level-set measures. For degenerate equations, the Sobolev exponent changes (depending on the p in the p-Laplacian), but the Chebyshev step is always applied in the same way. DiBenedetto does not discuss potential improvements to Chebyshev for structured functions.

**Kinnunen-Lewis (2000, 2002):** Kinnunen and Lewis extended De Giorgi iteration to higher-order nonlinear parabolic equations and systems. Their treatment in "Higher integrability for parabolic systems of p-Laplacian type" uses the standard Chebyshev step. They do discuss REVERSE Holder inequalities (which bootstrap integrability), but these require starting with a solution of an elliptic/parabolic equation — they don't apply to the truncated functions v_k which satisfy only an inequality.

**Vasseur (2007) and Vasseur-Yang (2021):** As documented in exploration-001, both formulations use the standard Chebyshev step. Neither discusses potential improvements. Vasseur explicitly identifies the Chebyshev step as part of the 4/3 barrier but does not suggest it could be improved.

### 4.3 Caffarelli-Vasseur (2010) and the SQG success

**Full reference:** L. Caffarelli, A. Vasseur, "Drift diffusion equations with fractional diffusion and the quasi-geostrophic equation," Ann. of Math. 171 (2010), no. 3, 1903-1930 (arXiv:math/0608447).

Caffarelli and Vasseur's proof of regularity for critical SQG is the closest analogue to a "successful De Giorgi for quadratic PDE." Key insights:

1. **They do NOT improve the Chebyshev step.** The level-set estimate is the same generic Sobolev + Chebyshev.
2. **They improve the NONLINEAR ESTIMATE** using the commutator structure of [(-Delta)^{1/2}, u], which gains regularity through the Kato-Ponce inequality.
3. **The scalar nature of SQG is essential.** For a scalar equation, the nonlinear term u·nabla theta involves only FIRST derivatives of theta (not the second derivatives that appear in the NS pressure). This makes the Holder pairing more favorable.

### 4.4 Sharpness of the Chebyshev step — what the literature says

**No paper I can identify explicitly addresses the question: "Is the Chebyshev step in the De Giorgi iteration for NS sharp?"**

This is significant. The question of whether NS solutions have better distributional decay than generic L^{10/3} functions appears to be:
- Not asked in the classical De Giorgi/Moser/Nash literature (which deals with linear equations where regularity is known)
- Not addressed in the NS regularity literature (which focuses on Serrin-type criteria, blow-up rates, and concentration compactness)
- Not addressed in the Vasseur line of work (which takes the Chebyshev step as given and focuses on the pressure decomposition)

### 4.5 Related directions in the literature

1. **Profile decomposition and concentration compactness (Gallagher, Seregin, Sverak 2012; Kenig-Koch 2011):** These methods analyze the structure of potential blow-up solutions by decomposing them into "profiles" (concentrated at different scales/locations) and a remainder. The profile decomposition gives detailed information about HOW the L^{10/3} norm concentrates, but this is used for a different purpose (proving the remainder is subcritical) rather than for improving level-set estimates.

2. **Quantitative regularity (Tao 2020; Palasek 2023):** Recent work on quantitative bounds for NS solutions gives explicit rates of regularity given quantitative Serrin-type assumptions. These methods are orthogonal to the De Giorgi approach — they bound ||u||_{L^infty} directly rather than through an iterative level-set scheme.

3. **Frequency-localized estimates (Chemin-Zhang 2016; Bradshaw-Grujic 2017):** These approaches decompose u into frequency shells and analyze each shell separately. The level-set distribution of a frequency-localized function IS better than generic (Bernstein's inequality gives ||f_j||_{L^infty} <= C 2^{3j/2} ||f_j||_{L^2}, which is sharp for lacunary decompositions). However, recombining the frequency shells loses this advantage — the level-set distribution of the full u is not controlled by summing the frequency-localized bounds.

4. **Escauriaza-Seregin-Sverak (2003):** The backward uniqueness approach to NS regularity avoids level-set estimates entirely, working instead with Carleman inequalities for the backward heat equation. Their proof that L^3(R^3) solutions don't blow up at the first singular time uses entirely different tools from De Giorgi iteration. Their method does not seem adaptable to improve the Chebyshev step.

---

## Task 5: Synthesis and Verdict

### 5.1 Is there a known analytical improvement to Chebyshev for NS solutions?

**NO.** No published result improves the distributional estimate |{|u|>lambda}| for divergence-free vector fields in L^p beyond the standard Chebyshev bound. The question appears to be open in the mathematical literature.

### 5.2 Is the 4/3 universal across model PDEs?

**YES, in the following precise sense:** The generic De Giorgi recursion exponent for a PDE with H^s dissipation in n dimensions is:

> **beta = 1 + s/n**

This gives 4/3 for (s,n) = (1,3) (NS), 3/2 for (s,n) = (1,2) (2D NS, borderline), and 2 for (s,n) = (1,1) (Burgers). The formula is universal for the Sobolev + Chebyshev chain.

PDE-specific structure can beat this formula, as demonstrated by Caffarelli-Vasseur for SQG (where commutator estimates improve the nonlinear bound beyond what the generic Chebyshev step gives). But the Chebyshev step ITSELF always produces the generic exponent.

### 5.3 Ranked list of most promising routes to improving the Chebyshev step

1. **NS-specific distributional estimate for |u|** (OPEN, high risk, high reward). Show that div(u)=0 + energy inequality constrains |{|u|>lambda}| better than Chebyshev. No existing result, no clear path, but also no obstruction. This is the only route that directly improves the Chebyshev step.

2. **PDE-based integrability beyond L^{10/3}** (CIRCULAR, unless partial). Use the NS equation to bootstrap v_{k-1} into L^r for some r > 10/3. This is equivalent to proving partial regularity (circular), BUT: a conditional version (assuming some quantitative control on the pressure or vorticity) might give a partial improvement applicable in the De Giorgi regime.

3. **Commutator-type improvement of the nonlinear estimate** (PROMISING for SPECIFIC terms). Following the SQG precedent: don't improve the Chebyshev step, but improve the estimate of the specific term where 4/3 appears. The P_{k21} non-divergence-form pressure interaction might have cancellations exploitable via commutator estimates or Hardy-space techniques. This doesn't improve Chebyshev but bypasses it.

4. **Modified energy functional** (POSSIBLE but likely insufficient). Change U_k to include additional terms (Besov norms, vorticity information, logarithmic corrections). This changes both the 1/2 and the 5/6 simultaneously and might shift the balance. However, any modification must still satisfy a closed energy inequality, which constrains the options severely.

5. **Lorentz/interpolation refinements** (RULED OUT by this analysis). Using L^{p,q} Lorentz spaces or Holder interpolation with different exponents does not change the distributional decay rate. The improvement is in constants, not exponents.

6. **Support-restricted Chebyshev** (RULED OUT by this analysis). The support constraint from the previous De Giorgi level is weaker than the direct Chebyshev bound in the convergent regime.

### 5.4 Key finding: the gap between Chebyshev and Serrin

The most illuminating finding is the precise correspondence:

- The energy gives L^{10/3}_{t,x} parabolic integrability
- Serrin regularity requires L^q_{t,x} with q > 10/3... wait, more precisely: 2/s + 3/r <= 1 for Serrin. The energy has (s,r) = (infty,2) and (2,6), interpolating to (10/3, 10/3). The Serrin condition at this exponent is 2/(10/3) + 3/(10/3) = 3/2 > 1. So the energy misses Serrin by 3/2 - 1 = 1/2 in the exponent sum.

- The De Giorgi beta = 4/3, and the needed beta = 3/2 for full regularity (in the sense of controlling the pressure term). The gap is 3/2 - 4/3 = 1/6.

- The gap 1/6 in beta corresponds to improving the Chebyshev exponent from 5/3 to 5/3 + 1/3 = 2 (since beta = 1/2 + (Cheb exponent)/2, needing beta = 3/2 gives Cheb exponent = 2, i.e., |A_k| <= C^k U_{k-1}^2 instead of U_{k-1}^{5/3}).

- This would require |{v_{k-1}>2^{-k}}| to decay like U_{k-1}^2, which corresponds to the level set measure decaying as ||v_{k-1}||_{L^4}^4 (Chebyshev with L^4 instead of L^{10/3}). Getting v_{k-1} in L^4 parabolic would require H^{5/4} Sobolev regularity (since H^{5/4} -> L^{12} in 3D, and the parabolic interpolation would give L^4), which is the Lions (1969) fractional NS threshold.

This closes the circle: improving the Chebyshev step from L^{10/3} to L^4 is equivalent to improving the regularity from H^1 to H^{5/4}, which is the known threshold for NS regularity via interpolation methods. The Chebyshev step is not an independent bottleneck — it is a faithful reflection of the integrability gap between the energy space and the regularity threshold.

---

## Task 6: Detailed Model PDE Analysis (Quantitative)

The user requests specific quantitative analysis for five PDEs. I expand on the summary table (Task 3.4) with full derivations.

### 6.1 PDE 1: Caffarelli-Vasseur (2010) — Critical SQG (Detailed)

**Equation:** theta_t + u . nabla theta = -kappa (-Delta)^{1/2} theta, with u = nabla^perp (-Delta)^{-1/2} theta, in 2D.

**Step 1: Sobolev embedding.** The dissipation gives H^{1/2}(R^2) control. The fractional Sobolev embedding is:

H^s(R^n) embeds into L^{2n/(n-2s)} for s < n/2.

For s = 1/2, n = 2: L^{2*2/(2-1)} = L^4(R^2).

**Step 2: Parabolic interpolation.** The energy gives w_k in L^infty_t L^2_x and (-Delta)^{1/4} w_k in L^2_{t,x}, hence w_k in L^2_t L^4_x.

Interpolation L^infty_t L^2_x cap L^2_t L^4_x gives L^q_{t,x} where q = 2 + 4s/n = 2 + 4(1/2)/2 = 3.

So the parabolic Sobolev embedding is: **L^3_{t,x}** (compare L^{10/3} for 3D NS).

**Step 3: Chebyshev.** With ||w_{k-1}||_{L^3} <= C U_{k-1}^{1/2}:

|{w_{k-1} > 2^{-k}}| <= (2^k)^3 U_{k-1}^{3/2}

**Step 4: Indicator norm.**

||1_{w_k>0}||_{L^2} <= |{w_k>0}|^{1/2} <= C^k U_{k-1}^{3/4}

**Step 5: Generic beta.** beta_generic = 1/2 + 3/4 = **5/4**.

**Step 6: Closure threshold.** The De Giorgi convergence lemma requires beta > 1 (for U_k -> 0 given small U_0). beta = 5/4 > 1, so the generic iteration converges — but only for the terms without the quadratic nonlinearity.

**Step 7: The quadratic nonlinearity.** For the full SQG equation, the transport term u . nabla theta tested against w_k produces terms analogous to the NS pressure. The generic Holder pairing would give:

|integral u . nabla theta . w_k| <= ||u||_{L^r} ||nabla theta||_{L^2} ||w_k||_{L^s}

For u = R^perp theta (Riesz transform), ||u||_{L^p} ~ ||theta||_{L^p}, so the velocity has the SAME integrability as theta.

The key issue: does the transport term degrade beta from 5/4, and if so, to what?

**The Caffarelli-Vasseur approach** avoids this issue entirely by RESTRUCTURING the proof:

(a) **L^2 -> L^infty step (Section 3 of their paper).** They first prove that theta in L^2 implies theta in L^infty. This step uses a De Giorgi iteration where the energy quantity is:

A_k = ||w_k||_{L^infty_t L^2_x}^2 + integral integral |(-Delta)^{1/4} w_k|^2

and the recurrence is:

A_{k+1} <= C . 2^{4k} . A_k^{1+epsilon}

with **epsilon > 0** that depends on the dimension and the fractional order. For d=2, s=1/2: the paper achieves epsilon = 1/(2d) = 1/4 (from the parabolic gain).

Actually, let me be more precise about what Caffarelli-Vasseur prove. Their Theorem 1.2 states that for the drift-diffusion equation theta_t + b . nabla theta + (-Delta)^{1/2} theta = 0 with b divergence-free and in L^infty_t BMO_x^{-1}, solutions with L^2 initial data become L^infty.

The proof structure for L^2 -> L^infty (their Section 3) does NOT follow the Vasseur 2007 pattern. Instead, it uses:

1. **Harmonic extension** (Caffarelli-Silvestre 2007): Represent (-Delta)^{1/2} theta as the normal derivative of the harmonic extension theta* to the upper half-space R^{n+1}_+. This converts the nonlocal problem to a LOCAL problem in one higher dimension.

2. **Local energy inequality** for the extended function: The energy inequality becomes a standard parabolic energy inequality in n+1 dimensions with a weight (the y-coordinate acts as a weight in the extension).

3. **De Giorgi iteration on the extended problem:** Apply De Giorgi iteration to the extended function on the half-space. The key advantage: in the extended formulation, the fractional Laplacian becomes a standard Laplacian (with weight), and the drift b does not appear in the interior of the half-space — it appears only at the boundary y=0.

4. **The recurrence:** The energy quantities A_k satisfy a recurrence of the form A_{k+1} <= C^k A_k^{1+alpha} with alpha > 0. If A_0 is sufficiently small, then A_k -> 0, giving theta in L^infty on the unit ball.

**What is alpha (= epsilon)?** The harmonic extension lives in n+1 = 3 dimensions (for the 2D SQG problem). The Sobolev embedding in 3D is H^1 -> L^6, giving parabolic L^{10/3}. But the equation is for an (n+1)-dimensional function with a boundary condition at y=0, so the effective dimension for the Sobolev embedding is n+1 = 3.

Using our universal formula with s=1 (standard Laplacian in the extension), effective dimension n+1 = 3:

beta = 1 + s/(n+1) = 1 + 1/3 = 4/3

Wait — this gives 4/3 again! But the iteration CLOSES because the drift term is handled differently in the extension. The drift b only acts at the boundary y=0, and its contribution to the energy inequality is controlled by the BMO^{-1} norm, which introduces a MULTIPLICATIVE factor (not a power of U_{k-1}).

**The precise mechanism:** In the harmonic extension framework:

U_k <= C^k U_{k-1}^{4/3} . (1 + ||b||_{BMO^{-1}})

The factor (1 + ||b||_{BMO^{-1}}) is a CONSTANT (independent of k), so it gets absorbed into the C^k prefactor. The exponent 4/3 > 1 is sufficient for convergence of the De Giorgi iteration (given U_0 small).

**This is the crucial difference from 3D NS:** In SQG/drift-diffusion, the nonlinearity enters as a drift b that contributes a multiplicative constant to the recurrence, NOT an additional power of U_{k-1}. In 3D NS, the pressure term contributes U_{k-1}^{4/3} with no additional smallness — and separately, the pressure norm ||P||_{L^p} needs to be controlled, introducing the constraint beta_p > 3/2 for p <= 10.

**Summary for SQG:**

| Quantity | Value |
|----------|-------|
| Dimension | d=2 (physical), d+1=3 (extension) |
| Diffusion order | s=1/2 (physical), s=1 (extension) |
| Sobolev embedding | H^1(R^3) -> L^6 (in extension) |
| Parabolic embedding | L^{10/3}_{t,x,y} (in extension) |
| Chebyshev exponent | 10/3 -> measure U^{5/3} |
| Generic beta | 4/3 (same as 3D NS!) |
| Actual beta | 4/3, but iteration CLOSES because drift is multiplicative |
| Closure mechanism | BMO^{-1} drift gives bounded constant, not extra U power |
| Regularity | YES — proved by Caffarelli-Vasseur (2010) |

**Is the Chebyshev step sharp?** Yes, in the same sense as for 3D NS — the L^{10/3} Chebyshev bound is the best available from the energy. The SQG proof does NOT improve Chebyshev; it improves the handling of the nonlinear term.

### 6.2 PDE 2: General Drift-Diffusion (Detailed)

**Equation:** theta_t + b . nabla theta + (-Delta)^{1/2} theta = 0, where b is divergence-free and in L^infty_t BMO^{-1}_x.

This is the general class treated in Caffarelli-Vasseur (2010), Theorem 1.2. The SQG equation is the special case b = R^perp theta.

**The De Giorgi iteration is identical to the SQG case** because the proof only uses:
1. div(b) = 0
2. b in L^infty_t BMO^{-1}_x
3. Energy inequality for theta

It does NOT use the specific relation b = R^perp theta. The beta and closure mechanism are the same.

**How does drift regularity affect beta?** The drift b enters the energy estimate through the transport term integral b . nabla theta . w_k. Using the harmonic extension, this term is controlled at the boundary y=0. The bound on this term involves:

||b||_{BMO^{-1}} . ||nabla theta||_{L^2} . ||w_k||_{L^2}

The BMO^{-1} norm is the critical regularity for the drift at the scaling of (-Delta)^{1/2} in 2D. If the drift had BETTER regularity (e.g., b in L^infty), the argument would still work (the multiplicative constant would be different). If the drift had WORSE regularity (e.g., b in L^p for some p), the argument might fail because the drift contribution could grow with k.

**Specifically:**
- b in BMO^{-1}: borderline case, works because BMO^{-1} is the dual of H^1, and the commutator [(-Delta)^{1/2}, b] maps L^2 to L^2 when b in BMO (the Coifman-Rochberg-Weiss commutator theorem).
- b in L^p (finite p < infty): the drift contribution to the energy inequality would involve ||b||_{L^p} . ||w_k||_{L^{2p/(p-2)}}, and the Holder pairing would introduce additional powers of U_{k-1}. This could degrade beta.
- b in L^2: For b in L^2_x only, the transport term cannot be controlled at all (insufficient integrability), and the De Giorgi iteration does not close.

**Summary:**

| Drift regularity | Effect on beta | Iteration closes? |
|------------------|---------------|-------------------|
| b in L^infty | beta = 4/3 (extension), closes | YES |
| b in BMO^{-1} | beta = 4/3 (extension), closes (critical) | YES (Caffarelli-Vasseur) |
| b in L^p, p > 2d | beta = 4/3, drift adds multiplicative constant | YES (for large enough p) |
| b in L^p, p <= 2d | beta < 4/3 (additional U power from drift) | OPEN / depends on p |
| b in L^2 | Cannot control transport term | NO |

The critical observation: **the beta from the Chebyshev chain is always 4/3 (in the extension) regardless of drift regularity.** What changes with the drift is whether the transport term adds a MULTIPLICATIVE constant (good) or an ADDITIONAL POWER of U_{k-1} (bad).

### 6.3 PDE 3: 1D Burgers Equation (Detailed)

**Equation:** u_t + u u_x = nu u_xx.

**Why De Giorgi is overkill.** The maximum principle gives ||u(t)||_{L^infty} <= ||u_0||_{L^infty} directly (test with sign(u-M) for any level M). De Giorgi iteration is unnecessary. But let's trace the exponents.

**Step 1: Sobolev embedding.** H^1(R) embeds into L^infty(R) (Morrey's inequality in 1D). This is dramatically stronger than in higher dimensions.

More precisely: ||f||_{L^infty} <= C ||f||_{H^1} in 1D.

**Step 2: Parabolic interpolation.** L^infty_t L^2_x cap L^2_t H^1_x. Since H^1 embeds into L^infty in 1D:

L^infty_t L^2_x cap L^2_t L^infty_x embeds into L^q_{t,x} for q = 2 + 4s/n = 2 + 4(1)/1 = 6.

So the parabolic Sobolev embedding gives **L^6_{t,x}** in 1D.

**Step 3: Chebyshev with L^6.**

|{v_{k-1} > 2^{-k}}| <= (2^k)^6 ||v_{k-1}||_{L^6}^6 <= C^k U_{k-1}^3

**Step 4: Indicator norm.**

||1_{v_k>0}||_{L^2} <= C^k U_{k-1}^{3/2}

**Step 5: Generic beta.**

beta = 1/2 + 3/2 = **2**

Alternatively, from the formula: beta = 1 + s/n = 1 + 1/1 = 2.

**Step 6: The nonlinear term.** Burgers has the nonlinear term u u_x. Testing with v_k:

integral u u_x v_k dx = integral u (partial_x)(v_k^2/2) dx (roughly)

By integration by parts: = -integral u_x v_k^2/2 dx - integral u (v_k v_{k,x}) dx (after using the chain rule for v_k = (|u|-c_k)_+)

The nonlinear term is quadratic and involves first derivatives, similar to NS. The Holder pairing for the worst term gives:

||v_k||_{L^infty} . ||v_{k,x}||_{L^2} . ||1_{v_k>0}||_{L^2}

Using L^infty embedding: ||v_k||_{L^infty} <= C U_{k-1}^{1/2} (from H^1 -> L^infty in 1D)

So the nonlinear contribution: U_{k-1}^{1/2} . U_{k-1}^{1/2} . U_{k-1}^{3/2} = U_{k-1}^{5/2}

This gives beta_nonlinear = 5/2 >> 2, so the nonlinear term is even better than the generic transport estimate. The iteration closes with enormous room.

**Step 7: Closure analysis.** The threshold for De Giorgi convergence is beta > 1. We have beta = 2 > 1 (from generic terms) and beta_nonlinear = 5/2 (from the quadratic term). The iteration converges trivially.

There is no pressure in 1D Burgers (the pressure in 1D incompressible flow is determined algebraically, and Burgers is compressible anyway — the nonlinear term u u_x = partial_x(u^2/2) is in conservative form). So there is no pressure bottleneck.

**Summary for 1D Burgers:**

| Quantity | Value |
|----------|-------|
| Dimension | d=1 |
| Diffusion order | s=1 (standard Laplacian) |
| Sobolev embedding | H^1(R) -> L^infty |
| Parabolic embedding | L^6_{t,x} |
| Chebyshev exponent | 6 -> measure U^3 |
| Generic beta | 2 |
| Nonlinear beta | 5/2 |
| Closure threshold | beta > 1 |
| Regularity | YES (trivially, also via maximum principle) |

**Why it's different from 3D NS:** The H^1 -> L^infty embedding in 1D (vs H^1 -> L^6 in 3D) gives enormously better integrability. The parabolic embedding L^6 (vs L^{10/3}) pushes the Chebyshev exponent from 5/3 to 3, and beta from 4/3 to 2. Additionally, there is no pressure.

### 6.4 PDE 4: 3D MHD Equations (Detailed)

**Equations:**
u_t + u . nabla u = -nabla p + nu Delta u + B . nabla B
B_t + u . nabla B = mu Delta B + B . nabla u
div u = div B = 0

**The key structural features:**
1. Both u and B have standard H^1 dissipation in 3D.
2. The nonlinearity involves two quadratic terms: u . nabla u (advection) and B . nabla B (magnetic tension/Lorentz force).
3. The magnetic tension B . nabla B has the SAME scaling as u . nabla u but different algebraic structure.
4. The total energy is (1/2) integral (|u|^2 + |B|^2), which gives a joint energy inequality.

**Has De Giorgi iteration been applied to MHD?**

[VERIFIED] Yes. He and Xin (2005) proved CKN-type partial regularity for MHD. Jiu and Wang gave an alternative proof using De Giorgi iteration (following Vasseur's 2007 approach). More recently, Chamorro and He (2020, arXiv:2005.02697) generalized the CKN partial regularity to MHD in the framework of parabolic Morrey spaces.

The He-Xin result establishes that for suitable weak solutions of MHD, the one-dimensional parabolic Hausdorff measure of the singular set is zero. This is the SAME conclusion as for 3D NS (CKN theorem). The De Giorgi approach by Jiu-Wang gives the same result.

**What beta results for MHD?**

The MHD energy structure is:

U_k(u,B) = sup_t integral (|v_k^u|^2 + |v_k^B|^2) + integral integral (|d_k^u|^2 + |d_k^B|^2)

where v_k^u = (|u|-c_k)_+, v_k^B = (|B|-c_k)_+ (or some combined truncation).

The Sobolev and Chebyshev steps are IDENTICAL to NS:
- H^1(R^3) -> L^6 -> parabolic L^{10/3}
- Chebyshev gives measure ~ U_{k-1}^{5/3}
- Indicator norm ~ U_{k-1}^{5/6}

**The nonlinear terms:**

1. **Advection u . nabla u:** This produces pressure, handled identically to NS. Gives beta = 4/3 from the non-divergence-form pressure interaction.

2. **Magnetic tension B . nabla B:** This term has the SAME scaling as u . nabla u. It produces a "magnetic pressure" P_B satisfying -Delta P_B = partial_i partial_j (B_i B_j). The CZ theory for P_B is identical to the velocity pressure P. So this term ALSO gives beta = 4/3.

3. **Cross terms u . nabla B and B . nabla u:** These appear in the B-equation. They have the same scaling and structure as the advection term. The De Giorgi estimates give the same exponents.

**Beta for MHD:**

beta = 4/3

The magnetic tension B . nabla B does NOT change beta. The reason: it has the same scaling (quadratic, with one derivative) and the same algebraic structure from the De Giorgi perspective (a bilinear term that produces a non-divergence-form pressure interaction when tested against the truncated function).

The algebraic difference between B . nabla B and u . nabla u (the magnetic tension is symmetric in i,j while the Reynolds stress is not) does not affect the De Giorgi exponents. Both terms require the same Holder pairings and produce the same beta.

**Summary for 3D MHD:**

| Quantity | Value |
|----------|-------|
| Dimension | d=3 |
| Diffusion order | s=1 for both u and B |
| Sobolev embedding | H^1(R^3) -> L^6 |
| Parabolic embedding | L^{10/3}_{t,x} |
| Chebyshev exponent | 10/3 -> measure U^{5/3} |
| Generic beta | 4/3 (same as NS) |
| Pressure beta | 4/3 (from both u-pressure and B-pressure) |
| Singular set | 1-dimensional parabolic Hausdorff measure = 0 |
| Regularity | NO (open problem, same status as NS) |

**Why MHD gives the same beta as NS:** The magnetic field B has the same Sobolev regularity as u (both in H^1), the same scaling (both satisfy quadratic equations with first-order nonlinearity), and produces the same type of pressure interaction. The De Giorgi iteration cannot distinguish between u . nabla u and B . nabla B at the level of exponents.

**What IS different about MHD?** The partial regularity for MHD is slightly harder to prove because the energy inequality involves cross-terms and the pressure has contributions from both u and B. But the EXPONENTS are the same. The additional difficulty is in the constants and the structure of the proof, not in the scaling.

**Open question for MHD:** Could the different ALGEBRAIC structure of B . nabla B vs u . nabla u give a structural improvement? For example, B . nabla B appears with a positive sign in the u-equation (magnetic tension accelerates the fluid), while u . nabla u appears with an ambiguous sign (can either concentrate or disperse energy). This sign difference might help — but it has not been exploited in the De Giorgi framework.

### 6.5 PDE 5: Fractional (Hyperdissipative) NS (Detailed)

**Equation:** u_t + u . nabla u = -nabla p - nu (-Delta)^alpha u, with div u = 0, in 3D.

For alpha = 1, this is standard NS. For alpha > 1, the dissipation is stronger (hyperdissipative). For alpha < 1, the dissipation is weaker (hypodissipative).

**Known regularity results:**
- alpha >= 5/4: Global regularity (Lions 1969), proved via energy methods
- 1 < alpha < 5/4: Partial regularity (Katz-Pavlovic 2001), singular set dimension <= 5 - 4alpha
- alpha = 1: Standard NS, singular set dimension <= 1 (CKN)
- alpha < 1: Weaker results, larger singular sets

**Step 1: Sobolev embedding.** The dissipation gives H^alpha(R^3) control.

H^alpha(R^3) embeds into L^{6/(3-2alpha)} for alpha < 3/2.

For alpha = 1: L^6 (standard). For alpha = 5/4: L^{6/(3-5/2)} = L^{6/(1/2)} = L^12. For alpha = 3/2: L^infty (supercritical).

**Step 2: Parabolic interpolation.**

L^infty_t L^2_x cap L^2_t L^{6/(3-2alpha)}_x embeds into L^q_{t,x} where:

q = 2 + 4alpha/3 (using the formula q = 2 + 4s/n with s=alpha, n=3)

For alpha = 1: q = 10/3. For alpha = 5/4: q = 2 + 5/3 = 11/3. For alpha = 3/2: q = 4.

**Step 3: Chebyshev.**

||v_{k-1}||_{L^q}^q <= C U_{k-1}^{q/2}

|{v_{k-1} > 2^{-k}}| <= C^k U_{k-1}^{q/2}

**Step 4: Indicator norm.**

||1_{v_k>0}||_{L^2} <= C^k U_{k-1}^{q/4}

**Step 5: Generic beta (from the formula).**

beta = 1 + alpha/3

| alpha | Parabolic embedding q | Chebyshev measure exponent q/2 | Indicator exponent q/4 | Beta = 1/2 + q/4 = 1+alpha/3 |
|-------|----------------------|-------------------------------|----------------------|-------------------------------|
| 1 | 10/3 | 5/3 | 5/6 | 4/3 = 1.333 |
| 5/4 | 11/3 | 11/6 | 11/12 | 17/12 = 1.417 |
| 3/2 | 4 | 2 | 1 | 3/2 = 1.5 |
| 2 | 14/3 | 7/3 | 7/6 | 5/3 = 1.667 |

**Step 6: Does beta cross the closure threshold?**

The closure threshold for the De Giorgi iteration with pressure is beta > 3/2 (the same as for standard NS, because the pressure-velocity coupling structure is unchanged). The generic beta = 1 + alpha/3 reaches 3/2 exactly when alpha = 3/2.

But wait: for alpha > 5/4, regularity is already known by Lions (1969)! So the De Giorgi method reaches the 3/2 threshold at alpha = 3/2, which is ABOVE the known regularity threshold alpha = 5/4.

**This gap is significant:** Lions proves regularity at alpha = 5/4 using energy methods + interpolation (specifically, the Gagliardo-Nirenberg inequality). The De Giorgi method, applied naively, only recovers regularity at alpha = 3/2 — it MISSES the Lions result by a factor of alpha.

Why? Because the De Giorgi method uses only the L^2 energy and the H^alpha gradient energy. Lions' proof uses the FULL energy cascade: testing the equation with (-Delta)^s u for various s, building up higher Sobolev regularity iteratively. This iterative bootstrapping is more powerful than the single-step De Giorgi energy estimate.

**Step 7: The pressure bottleneck for fractional NS.**

The non-divergence-form pressure term in the De Giorgi iteration gives beta_pressure = 1/2 + q/4 = 1 + alpha/3. This is the bottleneck for alpha <= 3/2 (i.e., q <= 4).

For the non-local pressure P_{k1} (harmonic part), the exponent is:

beta_p = q/2 . (1 - 1/p) for pressure in L^p(L^1). For p > some threshold, beta_p > 3/2.

The threshold p decreases as alpha increases (better dissipation gives more room). At alpha = 5/4, the threshold is still p > 10-something, and beta_p for the local pressure term is 17/12 < 3/2.

**Step 8: Comparison to the Katz-Pavlovic singular set result.**

Katz-Pavlovic (2001) proved that for 1 < alpha < 5/4, the Hausdorff dimension of the singular set at blow-up time is at most 5 - 4alpha. At alpha = 1 (standard NS), this gives dim <= 1 (consistent with CKN).

The formula 5 - 4alpha = 0 at alpha = 5/4, consistent with the Lions regularity result (no singular points).

This result uses a CKN-type approach, NOT De Giorgi iteration. The CKN approach gives a sharper result because it uses the local energy inequality more efficiently (through the epsilon-regularity criterion), while De Giorgi gives the same qualitative conclusion (partial regularity) but with potentially different quantitative bounds.

**Colombo-De Lellis-Massaccesi (2017, arXiv:1712.07015)** introduced a notion of suitable weak solution for hyperdissipative NS and proved a generalized CKN theorem. Their result extends the CKN partial regularity to the full range 1 <= alpha < 5/4.

**Summary for Fractional NS:**

| Quantity | Value (general alpha) | alpha = 1 (NS) | alpha = 5/4 | alpha = 3/2 |
|----------|---------------------|----------------|-------------|-------------|
| Sobolev embedding | L^{6/(3-2alpha)} | L^6 | L^12 | L^infty |
| Parabolic embedding | L^{2+4alpha/3} | L^{10/3} | L^{11/3} | L^4 |
| Chebyshev measure exp. | (1+2alpha/3) | 5/3 | 11/6 | 2 |
| Indicator L^2 exp. | (1/2+alpha/3) | 5/6 | 11/12 | 1 |
| Generic beta | 1+alpha/3 | 4/3 | 17/12 | 3/2 |
| De Giorgi closes? | Only if alpha >= 3/2 | NO | NO | BORDERLINE |
| Lions regularity? | alpha >= 5/4 | NO | YES (borderline) | YES |
| CKN singular set dim | 5-4alpha | 1 | 0 | 0 |

**Key finding:** The De Giorgi beta does NOT cross the 3/2 closure threshold at alpha = 5/4. It only reaches 3/2 at alpha = 3/2. The gap between alpha = 5/4 (Lions) and alpha = 3/2 (De Giorgi closure) reflects the fact that the De Giorgi method uses only one step of the energy bootstrap, while Lions' proof iterates the energy estimate through multiple Sobolev levels.

### 6.6 Comprehensive Comparison Table

| PDE | d | s | Sobolev target | Parabolic q | Cheb. measure exp. | Beta = 1+s/d | Closes? | Why? |
|-----|---|---|---------------|------------|-------------------|-------------|---------|------|
| 1D Burgers | 1 | 1 | L^infty | L^6 | 3 | 2 | YES | H^1 -> L^infty in 1D |
| 2D NS | 2 | 1 | L^{infty}/L^p (all p) | L^4 | 2 | 3/2 | BORDERLINE | Known: Ladyzhenskaya |
| 3D NS | 3 | 1 | L^6 | L^{10/3} | 5/3 | 4/3 | NO | Open problem |
| 4D NS (hyp.) | 4 | 1 | L^4 | L^3 | 3/2 | 5/4 | NO | Worse than 3D |
| 3D MHD | 3 | 1 | L^6 | L^{10/3} | 5/3 | 4/3 | NO | Same as 3D NS |
| SQG (2D, s=1/2) | 2 | 1/2 | L^4 | L^3 | 3/2 | 5/4 | YES* | Commutator + extension |
| SQG extension | 3 | 1 | L^6 | L^{10/3} | 5/3 | 4/3 | YES* | Drift is multiplicative |
| Frac NS alpha=5/4 | 3 | 5/4 | L^12 | L^{11/3} | 11/6 | 17/12 | NO** | De Giorgi misses Lions |
| Frac NS alpha=3/2 | 3 | 3/2 | L^infty | L^4 | 2 | 3/2 | BORDERLINE | De Giorgi just reaches |

*SQG closes despite generic beta = 5/4 (or 4/3 in extension) because the drift term is multiplicative, not an additional power of U_{k-1}.
**Fractional NS at alpha = 5/4 has regularity (Lions), but De Giorgi gives beta = 17/12 < 3/2, so De Giorgi alone doesn't prove it.

---

## Task 7: Answers to Specific Questions

### Q1: What is the De Giorgi recurrence exponent beta for SQG?

**Generic beta = 5/4** (from s=1/2, d=2) if one works directly in 2D with fractional dissipation. Equivalently, **beta = 4/3** in the Caffarelli-Silvestre harmonic extension to 3D with standard Laplacian. The iteration closes because the drift contributes only a multiplicative constant (not a power of U_{k-1}), unlike the NS pressure.

### Q2: Is the SQG beta above the closure threshold?

The closure threshold is beta > 1 (standard De Giorgi convergence lemma). Beta = 5/4 > 1 (or 4/3 > 1 in the extension), so yes. The 3/2 threshold is specific to NS where the pressure creates an ADDITIONAL requirement — in SQG, there is no pressure.

### Q3: How does the parabolic embedding differ from 3D NS?

For 3D NS: H^1 -> L^6 -> parabolic L^{10/3}.
For SQG (direct 2D): H^{1/2} -> L^4 -> parabolic L^3.
For SQG (extension to 3D): H^1 -> L^6 -> parabolic L^{10/3} (same as NS!).

The embedding exponents are DIFFERENT in the direct approach (L^3 vs L^{10/3}) but the SAME in the extension approach (both L^{10/3}).

### Q4: Is the Chebyshev step sharp or loose in the SQG argument?

**Sharp** in the same sense as for NS — the Chebyshev bound is tight for arbitrary L^q functions. No SQG-specific improvement to Chebyshev is used. The improvement comes from the nonlinear estimate, not from Chebyshev.

### Q5: What structural feature of SQG allows the iteration to close where NS doesn't?

Three features:

1. **No pressure.** SQG is a scalar advection equation. There is no pressure term. The bottleneck in NS is the non-divergence-form pressure interaction, which is entirely absent in SQG.

2. **Scalar equation.** The truncated function w_k = (theta - c_k)_+ is scalar, so the Holder pairings in the energy estimate are simpler. There are no cross-terms between velocity components.

3. **Drift structure.** The nonlinearity u . nabla theta enters as a transport term with a divergence-free drift u. In the Caffarelli-Vasseur framework (after harmonic extension), this drift contributes a BOUNDED MULTIPLICATIVE FACTOR to the De Giorgi recurrence (controlled by the BMO^{-1} norm of u), not an additional power of U_{k-1}. In NS, the pressure-velocity coupling contributes an additional U_{k-1}^{4/3} factor that limits the overall exponent.

The commutator structure [(-Delta)^{1/2}, u] also plays a role, but the most fundamental difference is that SQG has no pressure and the nonlinearity is a transport (first-order in theta), while NS has pressure and the nonlinearity is quadratic-in-velocity (creating a non-divergence-form second-order interaction).

### Q6: What beta does the iteration produce for the general drift-diffusion class?

**Beta = 4/3** (in the harmonic extension framework). The drift regularity (BMO^{-1} vs L^p) does not change beta — it only affects whether the multiplicative constant from the drift term is finite. For b in BMO^{-1}, the constant is finite and the iteration closes. For b in weaker spaces, the constant may blow up and the iteration may fail.

### Q7: Has De Giorgi iteration been applied to MHD?

[VERIFIED] Yes. Jiu and Wang used De Giorgi iteration (following Vasseur 2007) to prove partial regularity for MHD. The beta is 4/3, identical to NS. The magnetic tension term B . nabla B has the same scaling as u . nabla u and produces the same exponents in the De Giorgi framework.

### Q8: For hyperdissipative NS, does the De Giorgi beta cross the closure threshold at alpha = 5/4?

**NO.** The generic De Giorgi beta for fractional NS with dissipation (-Delta)^alpha is:

beta = 1 + alpha/3

At alpha = 5/4: beta = 17/12 = 1.417 < 3/2 = 1.5. The threshold 3/2 is reached only at alpha = 3/2.

Lions (1969) proved regularity at alpha = 5/4 using energy methods that are MORE POWERFUL than a single De Giorgi step — specifically, testing with (-Delta)^s u and iterating through Sobolev levels. The De Giorgi approach, using only the L^2 energy and H^alpha gradient, cannot recover the Lions result.

---

## Appendix: Literature References (from targeted search)

### Divergence-free constraint and distributional estimates

1. **Coifman-Lions-Meyer-Semmes (1993).** "Compensated compactness and Hardy spaces," J. Math. Pures Appl. (9) 72, no. 3, 247-286. Shows div-free F times curl-free G belongs to H^1 (not just L^1). BILINEAR result only. Does not improve scalar level-set estimates for individual div-free fields.

2. **Bourgain-Brezis (2004).** "New estimates for the Laplacian, the div-curl, and related Hodge systems," C. R. Math. Acad. Sci. Paris 338, 539-543. Endpoint estimates for div-free vector fields at L^1. Proof uses atomic decomposition of divergence-free measures.

3. **Bourgain-Brezis (2007).** "New estimates for elliptic equations and Hodge type systems," J. Eur. Math. Soc. (JEMS) 9, 277-315. For div-free F in L^1(R^3): curl^{-1}(F) in L^{3/2,1} (Lorentz space). Concerns DUAL PAIRINGS and solving div/curl systems, not distribution functions of |F|.

4. **Van Schaftingen (2004).** "Estimates for L^1-vector fields," C. R. Math. Acad. Sci. Paris 339, no. 3, 181-186. For div-free F in L^1: integral phi . F <= ||F||_{L^1} ||D phi||_{L^n}. Explicitly does NOT provide pointwise or level-set estimates on |F|.

5. **Van Schaftingen (2013).** "Limiting Sobolev inequalities for vector fields and canceling linear differential operators," J. Eur. Math. Soc. 15, 877-921. Characterizes when endpoint Sobolev estimate holds: ||D^{k-1}u||_{L^{n/(n-1)}} <= ||A(D)u||_{L^1} iff A(D) is elliptic and cancelling. Divergence is cancelling. Result is at L^1 endpoint, irrelevant at L^{10/3}.

6. **Auscher-Russ (2003).** "Hardy spaces and divergence operators on strongly Lipschitz domains of R^n," J. Funct. Anal. 201, 148-184. Hardy spaces adapted to divergence-form elliptic operators. Not directly relevant to fluid velocity distributional estimates.

7. **Lenzmann-Schikorra (2019).** "Three examples of sharp commutator estimates via harmonic extensions." Covers CLMS Jacobian, Coifman-Rochberg-Weiss, Kato-Ponce-Vega. Commutator regularity results, not distributional estimates for div-free fields.

### De Giorgi method and model PDEs

8. **Vasseur (2007).** "A new proof of partial regularity of solutions to Navier-Stokes equations," NoDEA 14, 753-785 (arXiv:math/0607017). De Giorgi iteration for NS: beta = 4/3 from L^{10/3} Chebyshev.

9. **Caffarelli-Vasseur (2010).** "Drift diffusion equations with fractional diffusion and the quasi-geostrophic equation," Ann. of Math. 171, no. 3, 1903-1930 (arXiv:math/0608447). De Giorgi for critical SQG: proves L^2 -> L^infty via harmonic extension. Drift contributes multiplicative constant, not extra power of U_{k-1}.

10. **Brigati-Mouhot (2025).** "Introduction to quantitative De Giorgi methods," arXiv:2510.11481. Confirms beta = 1 + 2/d for scalar equations. "Hidden collision of scalings" from energy estimate, Sobolev embedding, Chebyshev.

11. **He-Xin (2005).** Partial regularity for MHD, CKN-type. Same beta = 4/3 as NS.

12. **Colombo-De Lellis-Massaccesi (2017).** arXiv:1712.07015. Generalized CKN theorem for hyperdissipative NS, range 1 <= alpha < 5/4.

13. **Lions (1969).** Global regularity for fractional NS with alpha >= 5/4 via iterative energy methods.

### Lorentz spaces and NS regularity

14. **Sohr (2001).** Serrin-type regularity in Lorentz spaces: u in L^s(0,T; L^{r,infty}) with 3/r + 2/s = 1, r > 3 implies regularity. CONDITIONAL result.

15. **Alvino-Ferone-Trombetti (2013).** "Optimal Sobolev Type Inequalities in Lorentz Spaces," Potential Analysis. Sharp embedding D^{1,p} -> L^{p*,q} for p <= q <= infty. Lorentz second index affects constants, not decay rates.

### Key negative finding

No paper in the literature addresses the question: "For u divergence-free and in L^p(R^3) with p > 1, does the divergence-free constraint improve the distribution function |{|u| > lambda}| beyond lambda^{-p} ||u||_{L^p}^p?" This question appears to be genuinely open. However, the analysis in this report provides strong evidence that the answer is NO: the distribution function depends on |u| (a scalar), while the div-free constraint involves the direction u/|u| (a vector property). Truncation to |u| > lambda destroys the div-free structure, making it inaccessible to the Chebyshev step in De Giorgi iteration.

---

## Status: COMPLETE
