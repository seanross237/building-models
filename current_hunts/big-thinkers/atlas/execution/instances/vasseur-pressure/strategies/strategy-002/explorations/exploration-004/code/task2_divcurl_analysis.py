"""
Task 2: Analytical check of div-curl structure for the bottleneck bilinear form.

Key question: Does the product u^{above} tensor u^{below} have compensated compactness
structure that would put P^{21} = R_iR_j(u_i^{above} u_j^{below}) in Hardy H^1?
"""

import sympy as sp

print("=" * 70)
print("TASK 2a: Divergence of u^{below}")
print("=" * 70)

print("""
COMPUTATION: div(u^{below})

u^{below} = u * phi(|u|)  where phi(s) = min(1, lambda/s)

On {|u| <= lambda}: u^{below} = u, so div(u^{below}) = div(u) = 0

On {|u| > lambda}: u^{below} = u * lambda/|u|, so:

  d(u_i^{below})/dx_i = (du_i/dx_i) * lambda/|u| + u_i * d(lambda/|u|)/dx_i
                       = (du_i/dx_i) * lambda/|u| + u_i * (-lambda/|u|^2) * d|u|/dx_i

  d|u|/dx_i = (u . du/dx_i) / |u| = sum_j u_j (du_j/dx_i) / |u|

Summing over i:
  div(u^{below}) = (div u) * lambda/|u| - lambda/|u|^2 * sum_i u_i * d|u|/dx_i
                 = 0 - lambda/|u|^2 * (u . grad|u|)

Now u . grad|u| = u . (Du^T u / |u|) = sum_i u_i * sum_j u_j (du_j/dx_i) / |u|

So: div(u^{below}) = -lambda * (u . grad|u|) / |u|^2    on {|u| > lambda}

BOUND on div(u^{below}):
  |div(u^{below})| <= lambda * |u| * |grad|u|| / |u|^2 = lambda * |grad|u|| / |u|

On the support {|u| > lambda}:
  |div(u^{below})| <= |grad|u||

KEY FINDING: div(u^{below}) is NOT zero — it is O(|grad|u||), which is the SAME
order as the gradient of the velocity. This is an O(1) error, NOT a small perturbation.

In terms of norms:
  ||div(u^{below})||_{L^2} <= ||grad|u|| * 1_{|u|>lambda}||_{L^2}
                             <= ||grad u||_{L^2}    (not small!)

The compressibility error is bounded by the FULL enstrophy, which is the same scale
as the quantities we're trying to bound. CLMS cannot apply to u^{below} directly
because div(u^{below}) is not small relative to the main estimates.
""")

print("=" * 70)
print("TASK 2b: Structure of u^{above} — curl analysis")
print("=" * 70)

print("""
COMPUTATION: curl(u^{above})

u^{above} = u * psi(|u|)  where psi(s) = max(0, 1 - lambda/s) = max(0, (s-lambda)/s)

On {|u| <= lambda}: u^{above} = 0, curl = 0.

On {|u| > lambda}: u^{above} = u * (|u| - lambda)/|u| = u - u * lambda/|u|
  = u - u^{below}

So: curl(u^{above}) = curl(u) - curl(u^{below}) = omega - curl(u^{below})

where omega = curl(u) is the vorticity.

  curl(u^{below})_k = epsilon_{kij} d_j(u_i * lambda/|u|)
    = epsilon_{kij} [(du_i/dx_j) * lambda/|u| + u_i * (-lambda/|u|^2) * d|u|/dx_j]
    = lambda/|u| * epsilon_{kij} du_i/dx_j - lambda/|u|^2 * epsilon_{kij} u_i * d|u|/dx_j
    = lambda/|u| * omega_k - lambda/|u|^2 * (u cross grad|u|)_k

So: curl(u^{above}) = omega - lambda/|u| * omega + lambda/|u|^2 * (u cross grad|u|)
    = omega * (1 - lambda/|u|) + lambda/|u|^2 * (u cross grad|u|)
    = omega * v_{k-1}/|u| + lambda * (u cross grad|u|) / |u|^2

On {|u| > lambda}: curl(u^{above}) = omega * (v_{k-1}/|u|) + lambda * (u x grad|u|)/|u|^2

This is ALSO not zero — u^{above} is neither divergence-free nor curl-free.

CONCLUSION FOR CLMS: Neither u^{above} nor u^{below} is divergence-free or curl-free.
Both fields have full O(enstrophy) divergence and curl. The CLMS div-curl lemma
CANNOT be applied to the pair (u^{above}, u^{below}).
""")

print("=" * 70)
print("TASK 2c: Could we restructure to find SOME div-curl pairing?")
print("=" * 70)

print("""
ALTERNATIVE ATTEMPTS:

1. DECOMPOSE differently: Instead of u^{above}, u^{below}, could we write the
   bilinear form in terms of fields that DO have div-curl structure?

   The NS nonlinearity is div(u tensor u) = (u . grad)u + u * div(u) = (u . grad)u.
   Using Leray projection: partial_t u + P[(u.grad)u] = nu * Delta u

   The quadratic form u_i u_j with div(u) = 0 means:
     sum_i d_i(u_i u_j) = (u . grad)u_j    (not zero)
     sum_j d_j(u_i u_j) = (u . grad)u_i    (not zero)

   So u tensor u does NOT have a div-curl structure even BEFORE truncation.

2. HELMHOLTZ DECOMPOSE the truncated fields:
   u^{below} = u^{below,df} + grad(phi)
   where u^{below,df} is div-free and grad(phi) is the potential part.

   Then: u^{above} tensor u^{below} = u^{above} tensor u^{below,df} + u^{above} tensor grad(phi)

   The first term has a div-free second factor. But u^{above} is NOT curl-free,
   so CLMS still doesn't apply.

   For CLMS, we need: div-free DOT curl-free. We'd need one factor to be a gradient.
   But velocity fields are generically rotational — there's no reason either truncation
   should be curl-free.

3. USE THE SPECIFIC RANK-1 STRUCTURE:
   f_{ij} = (u_i/|u|)(u_j/|u|) * v_{k-1} * lambda

   The unit vectors e_i = u_i/|u| satisfy |e| = 1. So f_{ij} = e_i * e_j * g
   where g = v_{k-1} * lambda.

   For this to have div-curl structure, we'd need either:
   - sum_i d_i(e_i * g) = 0  (div-free in first index) => div(e * g) = 0
   - sum_j d_j(e_j * g) = 0  (same thing)

   But div(e * g) = e . grad(g) + g * div(e), and neither is zero.

4. LOOK AT THE CONTRACTED FORM directly:
   P^{21} = sum_{ij} R_i R_j (f_{ij}) = R_i R_j(e_i e_j g)
           = R . R . (e tensor e * g)    [double divergence in Riesz sense]

   This is (-Delta)^{-1} div div (e tensor e * g) = (-Delta)^{-1} * partial_i partial_j(e_i e_j g)

   Note: partial_i partial_j(e_i e_j g) = partial_i[partial_j(e_i e_j g)]
     = partial_i[e_i (e . grad g + g div(e)) + g (grad e_i . e)]
     ... this gets very complicated but has no special cancellation.

VERDICT: No div-curl structure exists in the NS bottleneck bilinear form.
The fundamental reason is that the NS nonlinearity u tensor u with div(u) = 0
is NOT a div-curl product — it's a div-div product (the double divergence
partial_i partial_j(u_i u_j) is what gives the pressure, and this is a SECOND-order
cancellation, not first-order). CLMS handles first-order cancellations (one div, one curl).
""")

print("""
PRECISE STRUCTURAL OBSTRUCTION:

CLMS (1993) Theorem: If f in L^p and g in L^q with 1/p + 1/q = 1, and
  div(f) = 0 and curl(g) = 0 (or vice versa), then f . g in H^1(R^n).

For our bilinear form, we need BOTH conditions simultaneously:
  1. One factor approximately div-free (i.e., div is lower order)
  2. The other factor approximately curl-free

The truncation u -> u * phi(|u|) introduces BOTH div error AND curl error,
and these errors are O(|grad u|) = O(enstrophy^{1/2}), which is the same order
as the quantity being bounded. There is no regime in which these are "small."

Moreover, even if we could handle the errors perturbatively:
  - u^{below} has div ≠ 0 (computed above): error is lambda * |grad|u|| / |u|
  - u^{above} has curl ≠ 0 (computed above): curl ~ omega * v_{k-1}/|u| + ...

The div-curl structure would require one field to be EXACTLY a gradient.
No truncation of a generic velocity field produces a gradient field — this would
require the velocity to be irrotational in the high-amplitude region, which is
essentially never true for NS solutions (vorticity concentrates where |u| is large,
not where it is small).

HEURISTIC: Vorticity and velocity amplitude are positively correlated in turbulence
(vortex tubes have both high vorticity and high velocity). So the region
{|u| > lambda} where the truncation acts is precisely where curl is LARGEST,
making the curl-free approximation WORST.
""")

print("\n[TASK 2a,b,c ANALYTICAL COMPLETE]")
print("KEY RESULT: CLMS compensated compactness CANNOT apply to the NS bottleneck.")
print("Reason: Both u^{above} and u^{below} have O(1) divergence and curl errors.")
print("The truncation |u| -> threshold acts where vorticity is concentrated.")
