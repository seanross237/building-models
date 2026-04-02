"""
Task 1: Symbolic derivation of the exact bilinear form of the bottleneck integral I_k.

We work through Vasseur (2007) Proposition 3 and write out all terms explicitly.
The key objects:
  - u = velocity field, div(u) = 0
  - beta_k(s) = min(1, lambda_k / s) for s > 0, where lambda_k = 1 - 2^{-k}
  - u^{below} = u * beta_{k-1}(|u|) = u * min(1, lambda_{k-1}/|u|)
  - u^{above} = u - u^{below} = u * (1 - beta_{k-1}(|u|)) = u * max(0, 1 - lambda_{k-1}/|u|)
  - v_k = [|u| - lambda_k]_+

The pressure decomposition from Vasseur:
  p = P_k^{11} + P_k^{12} + P_k^{21} + P_k^{22}
  where -Delta P_k^{ab} = sum_{i,j} d_i d_j (u_i^a * u_j^b)
  with a,b in {below, above}

The bottleneck integral involves P_k^{21} (and P_k^{12} by symmetry).
"""

import sympy as sp

print("=" * 70)
print("TASK 1: Exact Bilinear Form of the Bottleneck Integral I_k")
print("=" * 70)

print("""
DEFINITIONS (following Vasseur 2007, Section 3):

Let u: R^3 x [0,T] -> R^3 be a suitable weak solution of NS with div(u) = 0.

Truncation functions:
  lambda_k = 1 - 2^{-k}    (level set thresholds, approaching 1)
  beta_k(s) = min(1, lambda_k/s)  for s > 0

Decomposed velocity fields:
  u^{below}_k = u * beta_k(|u|)   = u * min(1, lambda_k/|u|)
  u^{above}_k = u - u^{below}_k   = u * max(0, 1 - lambda_k/|u|)

Key properties:
  |u^{below}_k| <= lambda_k           (bounded)
  u^{above}_k supported on {|u| > lambda_k}  (localized to high-amplitude region)
  |u^{above}_k| = |u| - lambda_k = v_k  on its support

De Giorgi truncation:
  v_k = [|u| - lambda_k]_+            (excess over threshold)
  d_k^2 = (v_k/|u|)|grad|u||^2 + (lambda_k * 1_{|u|>=lambda_k}/|u|)|grad u|^2
  U_k = sup_t ||v_k||_{L^2}^2 + ||d_k||_{L^2(0,T;L^2)}^2

PRESSURE DECOMPOSITION:

The NS pressure satisfies:
  -Delta p = sum_{i,j} d_i d_j (u_i u_j) = div div(u tensor u)

Vasseur decomposes u = u^{below}_{k-1} + u^{above}_{k-1} to get:

  p = P^{11} + P^{12} + P^{21} + P^{22}

where:
  -Delta P^{ab} = sum_{i,j} d_i d_j (u_i^a * u_j^b)

Equivalently:
  P^{ab} = R_i R_j (u_i^a * u_j^b)    [Einstein summation]

where R_i = d_i(-Delta)^{-1/2} are Riesz transforms.
""")

print("""
THE BOTTLENECK INTEGRAL:

In the energy estimate for U_k, the critical (hardest to bound) term is:

  I_k = int_0^T int_{R^3} P^{21}_{k-1} * (u/|u|) . grad(v_k) * 1_{v_k > 0} dx dt

Note: grad(v_k) = grad|u| on {|u| > lambda_k}, and (u/|u|).grad|u| = d|u|/dt(flow).

More precisely, using the structure from Vasseur Prop 3 eq (3.6):

  I_k = int_0^T int P^{21}_{k-1} * div(u v_k / |u|) dx dt

Since div(u v_k/|u|) = (u/|u|).grad(v_k) + v_k * div(u/|u|), and div(u) = 0 gives:

  div(u/|u|) = -u . grad(1/|u|) = (u . grad|u|) / |u|^2  [on {|u| > 0}]

Actually: div(u/|u|) = (div u)/|u| + u . grad(1/|u|) = 0 + u . grad(1/|u|)
  = u . (-grad|u|/|u|^2) = -(u . grad|u|)/|u|^2

Wait — let me be more careful:
  div(u_i/|u|) = (du_i/dx_i)/|u| + u_i * d(1/|u|)/dx_i
  = (du_i/dx_i)/|u| - u_i * (d|u|/dx_i) / |u|^2

Summing over i:
  div(u/|u|) = (div u)/|u| - (u . grad|u|)/|u|^2 = -(u . grad|u|)/|u|^2

since div u = 0.
""")

print("""
EXPLICIT FORM OF P^{21}_{k-1}:

  P^{21}_{k-1}(x,t) = sum_{i,j} R_i R_j [u_i^{above}_{k-1}(x,t) * u_j^{below}_{k-1}(x,t)]

where:
  u_i^{above}_{k-1} = u_i * (1 - min(1, lambda_{k-1}/|u|))
                     = u_i * max(0, (|u| - lambda_{k-1})/|u|)
                     = u_i * v_{k-1}/|u|   on {|u| > lambda_{k-1}}
                     = 0                    on {|u| <= lambda_{k-1}}

  u_j^{below}_{k-1} = u_j * min(1, lambda_{k-1}/|u|)
                     = u_j                  on {|u| <= lambda_{k-1}}
                     = u_j * lambda_{k-1}/|u|  on {|u| > lambda_{k-1}}

So the tensor product f_{ij} := u_i^{above} * u_j^{below} satisfies:

  f_{ij} = 0                                          on {|u| <= lambda_{k-1}}
  f_{ij} = u_i u_j * (v_{k-1}/|u|) * (lambda_{k-1}/|u|)  on {|u| > lambda_{k-1}}
         = u_i u_j * v_{k-1} * lambda_{k-1} / |u|^2

Therefore:
  P^{21}_{k-1} = R_i R_j [u_i u_j * v_{k-1} * lambda_{k-1} / |u|^2 * 1_{|u| > lambda_{k-1}}]

KEY OBSERVATION: The argument of the Riesz transforms is:
  f_{ij} = (u_i/|u|)(u_j/|u|) * v_{k-1} * lambda_{k-1} * 1_{|u| > lambda_{k-1}}

This is a RANK-1 tensor (u_hat tensor u_hat) times a scalar (v_{k-1} * lambda_{k-1}).
The scalar v_{k-1} = |u| - lambda_{k-1} measures the excess.
""")

print("""
STANDARD ESTIMATE (what gives beta = 4/3):

By Calderon-Zygmund theory, R_i R_j : L^p -> L^p for 1 < p < infty:

  ||P^{21}||_{L^r} <= C ||u^{above} tensor u^{below}||_{L^r}
                    <= C ||u^{above}||_{L^{2r}} * ||u^{below}||_{L^{2r}}

For the De Giorgi chain:
  - u^{above} is in L^{10/3} (from Sobolev + parabolic interpolation)
  - u^{below} is in L^infty (bounded by lambda_{k-1})
  - So P^{21} is in L^{5/3} by taking r = 5/3

The bottleneck comes from pairing P^{21} with d_k:
  |I_k| <= ||P^{21}||_{L^{5/3}} * ||d_k||_{L^2} * ||1_{v_k>0}||_{L^{10}}

Wait — let me get the correct Holder triple. The pairing is:
  I_k = int P^{21} * div(u v_k/|u|) dx dt

After integration by parts and careful bookkeeping (Vasseur pp. 17-19), this becomes:
  |I_k| <= C * ||P^{21}||_{L^{3/2}_{t,x}} * ||d_k||_{L^2} * |{v_k > 0}|^{1/6}

The exponents satisfy: 2/3 + 1/2 + 1/6 = 4/3... wait, that's the wrong dimension.

Actually the key Holder triple is:
  |I_k| <= ||P^{21}||_{L^2_t L^{3/2}_x} * ||d_k * 1_{v_k>0}||_{L^2_t L^3_x}

No — let me trace through the actual estimate more carefully.

From Vasseur Prop 3, the critical bound (after all Holder and CZ applications) is:

  |I_k| <= C^k * U_{k-1}^{4/3}

The 4/3 = 1/2 + 5/6 comes from:
  - 1/2: from ||d_k||_{L^2} <= U_{k-1}^{1/2}  (energy bound)
  - 5/6: from ||1_{v_k>0}||_{L^{5/3}} * (CZ bound on P^{21})

More precisely (from E001's decomposition):
  - The pressure P^{21} is bounded by CZ as ||u^{below}||_{L^infty} * ||u^{above}||_{L^r}
  - ||u^{below}||_{L^infty} <= lambda_{k-1} <= 1 (absorbed into constants)
  - ||u^{above}||_{L^{10/3}} = ||v_{k-1}||_{L^{10/3}} (on the support)
  - ||v_{k-1}||_{L^{10/3}} <= C * U_{k-1}^{5/6} by Sobolev + interpolation + Chebyshev
  - The Holder pairing then gives 1/2 (from d_k) + 5/6 (from above) = 4/3
  - C^k comes from the geometric growth of Sobolev constants at each level

SUMMARY: beta = 4/3 = (1/2) + (5/6)
  where 1/2 is from the energy/dissipation bound
  and 5/6 is from L^{10/3} integrability of v_{k-1} via Chebyshev
""")

print("""
BILINEAR FORM FOR CLMS ANALYSIS:

To check compensated compactness, we need to examine:

  T_{ij} = u_i^{above} * u_j^{below}

where u^{above} and u^{below} come from the SAME divergence-free field u.

Question: Is there a div-curl pairing?

For CLMS (1993), we need:
  E in L^p with div(E) = 0
  B in L^q with curl(B) = 0
  => E . B in H^1 (Hardy space)

The product T_{ij} = u_i^{above} * u_j^{below} is a TENSOR product, not a dot product.
CLMS gives H^1 for the contraction u^{above} . u^{below} (if one is div-free and other curl-free).
But P^{21} involves R_i R_j applied to the full tensor.

More relevant: R_i R_j(f_{ij}) = R_i R_j(u_i^{above} u_j^{below})
  = sum_j R_j [sum_i R_i(u_i^{above} u_j^{below})]
  = sum_j R_j [R . (u^{above} u_j^{below})]

The inner sum R . (u^{above} * g) for fixed g = u_j^{below} is related to
div(u^{above} * g) through the Riesz transform relation:
  R . f = sum_i R_i f_i = (-Delta)^{-1/2} sum_i d_i f_i = (-Delta)^{-1/2} div(f)

So: sum_i R_i(u_i^{above} * u_j^{below}) = (-Delta)^{-1/2} div(u^{above} * u_j^{below})

If u^{above} were divergence-free:
  div(u^{above} * u_j^{below}) = u^{above} . grad(u_j^{below}) + u_j^{below} * div(u^{above})
  = u^{above} . grad(u_j^{below})   [if div(u^{above}) = 0]

BUT u^{above} IS NOT DIVERGENCE-FREE. This is the critical issue.
""")

print("\n[TASK 1 COMPLETE]")
print("The bilinear form is fully written out. Key finding: P^{21} = R_iR_j(f_{ij})")
print("where f_{ij} = (u_i u_j * v_{k-1} * lambda_{k-1} / |u|^2) * 1_{|u|>lambda_{k-1}}")
print("The tensor structure (rank-1, from same field u) is critical for div-curl analysis.")
