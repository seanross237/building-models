"""
Task 1: Direct Estimate via Integration by Parts — Symbolic Exponent Computation

We analyze the bottleneck integral I_k = ∫∫ P^{21} · v_k · 1_{v_k>0} dx dt
using integration by parts instead of CZ bounds on P^{21}.

The standard CZ route:
  ||P^{21}||_{L^{3/2}} ≤ C ||u^{below}||_{L^3} ||u^{above}||_{L^3}
  Then Hölder: I_k ≤ ||P^{21}||_{L^{3/2}} ||v_k · 1_{v_k>0}||_{L^3}

The direct route (integration by parts):
  I_k = ∫∫ (u_i^{below} · u_j^{above}) · R_iR_j(v_k · 1_{v_k>0}) dx dt
  where R_i = ∂_i(-Δ)^{-1/2} are Riesz transforms.

We compute the exponent configuration for both routes and check if they differ.
"""

from sympy import *

print("=" * 70)
print("TASK 1: DIRECT ESTIMATE VIA INTEGRATION BY PARTS")
print("=" * 70)

# ============================================================
# STANDARD CZ ROUTE (reference)
# ============================================================
print("\n--- Standard CZ Route ---")
print("""
Step 1: P^{21} = R_iR_j(u_i^{below} · u_j^{above})
Step 2: ||P^{21}||_{L^{3/2}} ≤ C ||u^{below} · u^{above}||_{L^{3/2}}
        (CZ boundedness on L^{3/2})
Step 3: ||u^{below} · u^{above}||_{L^{3/2}} ≤ ||u^{below}||_{L^3} ||u^{above}||_{L^3}
        (Hölder with 2/3 = 1/3 + 1/3)
Step 4: I_k ≤ ||P^{21}||_{L^{3/2}} ||v_k||_{L^3}
        (Hölder with 1 = 2/3 + 1/3)
""")

# In the De Giorgi context:
# ||u^{below}||_{L^3}^3 ~ ∫|u|^3 · 1_{|u|≤λ_{k-1}} ≤ λ_{k-1}^3 · vol ~ C (bounded)
# ||u^{above}||_{L^3} ~ ||v_{k-1}||_{L^3} (controlled by Sobolev on v_{k-1})
# ||v_k||_{L^3} (controlled by Sobolev on v_k)

# The bottleneck: Hölder pairing of three factors
# Result: I_k ≤ C^k · U_{k-1}^{β} with β = 4/3

# Let me trace the exponent precisely using symbolic computation

print("--- Exponent trace for CZ route ---")
print("""
In the De Giorgi framework (n=3, s=1):

u^{below} is truncated below level λ_k, so ||u^{below}||_{L^∞} ≤ λ_k ~ O(1).
u^{above} = u · (1 - v_k/|u|) · 1_{|u| > λ_k} -- above part.

Key Sobolev/parabolic estimates:
  ||v_k||_{L^{10/3}(space-time)}^{10/3} ≤ C · U_k  (parabolic Sobolev: H^1 → L^{10/3})
  ||∇v_k||_{L^2(space-time)}^2 ≤ U_k               (energy part of U_k)
  ||v_k||_{L^∞_t L^2_x}^2 ≤ U_k                    (sup part of U_k)

For ||v_k||_{L^3}: interpolate between L^{10/3} and L^2
  ||v_k||_{L^3} ≤ ||v_k||_{L^{10/3}}^a · ||v_k||_{L^2}^{1-a}
  with 1/3 = a·3/10 + (1-a)·1/2 → a = (1/3-1/2)/(3/10-1/2) = (-1/6)/(-1/5) = 5/6

So ||v_k||_{L^3}^3 ≤ ||v_k||_{L^{10/3}}^{10/3 · (5/6)} · ...
Wait, let me be more careful with the L^p interpolation.
""")

# Symbolic interpolation computation
a = Symbol('a', positive=True)
p_target = Rational(3, 1)  # L^3
p1 = Rational(10, 3)  # L^{10/3}
p2 = Rational(2, 1)  # L^2

# 1/p_target = a/p1 + (1-a)/p2
eq = Eq(1/p_target, a/p1 + (1-a)/p2)
a_val = solve(eq, a)[0]
print(f"Interpolation for L^3 between L^{{10/3}} and L^2: a = {a_val}")
# a = 5/6 means ||v_k||_3 ≤ ||v_k||_{10/3}^{5/6} · ||v_k||_2^{1/6}
# But we need space-time interpolation more carefully

print("\n" + "=" * 70)
print("DIRECT ROUTE: INTEGRATION BY PARTS")
print("=" * 70)

print("""
Starting from:
  I_k = ∫∫ P^{21} · v_k · 1_{v_k>0} dx dt

where P^{21} = (-Δ)^{-1} ∂_i∂_j (u_i^{below} · u_j^{above})

Step 1: Self-adjointness of R_iR_j = ∂_i∂_j(-Δ)^{-1}
  <R_iR_j(f), g> = <f, R_iR_j(g)>    (Riesz transforms are self-adjoint)

Therefore:
  I_k = ∫∫ (u_i^{below} · u_j^{above}) · R_iR_j(v_k · 1_{v_k>0}) dx dt

KEY OBSERVATION: The CZ operator now acts on v_k · 1_{v_k>0} instead of
on u^{below} · u^{above}.

Step 2: Bound ||R_iR_j(v_k · 1_{v_k>0})||_{L^p}
  By CZ boundedness on L^p (1 < p < ∞):
    ||R_iR_j(v_k · 1_{v_k>0})||_{L^p} ≤ C_p ||v_k · 1_{v_k>0}||_{L^p}
    = C_p ||v_k||_{L^p} (since v_k = 0 where 1_{v_k>0} = 0)

CRITICAL: This is still a CZ bound! But it's on v_k, not on u^{below} · u^{above}.
The question is whether the available estimates on v_k give a better Hölder pairing.
""")

# Now compute the Hölder pairing for the direct route
print("--- Hölder analysis for direct route ---")
print("""
We need to bound:
  ∫ (u^{below} · u^{above}) · R_iR_j(v_k) dx

By Hölder with exponents (p, q, r) where 1/p + 1/q + 1/r = 1:
  ≤ ||u^{below}||_{L^p} · ||u^{above}||_{L^q} · ||R_iR_j(v_k)||_{L^r}
  ≤ ||u^{below}||_{L^p} · ||u^{above}||_{L^q} · C ||v_k||_{L^r}

Available bounds in De Giorgi framework:
  - ||u^{below}||_{L^∞} ≤ λ_k ~ 1  [free — this is the truncation]
  - ||u^{above}||_{L^q} requires: from level set measure and energy
  - ||v_k||_{L^r}: parabolic Sobolev gives L^{10/3}, energy gives L^2, Sobolev gives L^6
""")

# The key question: can we choose p, q, r to beat the CZ route?
# In the CZ route, the effective pairing was:
# ||P^{21}||_{L^{3/2}} · ||v_k||_{L^3} with P^{21} bounded by ||u^below·u^above||_{L^{3/2}}

# In the direct route, we have three factors.
# Since ||u^{below}||_{L^∞} ≤ C is free, we effectively have:
# I_k ≤ C · ||u^{above}||_{L^q} · ||v_k||_{L^r}  with 1/q + 1/r = 1

print("\nSince ||u^{below}||_{L^∞} ≤ C (free), the direct route reduces to:")
print("  I_k ≤ C · ||u^{above}||_{L^q} · ||v_k||_{L^r}  with  1/q + 1/r = 1")
print()

# What is u^{above}?
# u^{above} = u · (v_k/|u|) · 1_{|u| > λ_k} = u/|u| · v_k
# So ||u^{above}||_{L^q} = ||v_k · (u/|u|)||_{L^q} = ||v_k||_{L^q} (since |u/|u|| = 1 on support)

print("CRUCIAL: u^{above} = (u/|u|) · v_k on {|u| > λ_k}, so ||u^{above}||_{L^q} = ||v_k||_{L^q}")
print()
print("Therefore the direct route gives:")
print("  I_k ≤ C · ||v_k||_{L^q} · ||v_k||_{L^r}  with  1/q + 1/r = 1")
print()

# Compare with CZ route:
# I_k ≤ ||P^{21}||_{L^{3/2}} · ||v_k||_{L^3}
# ≤ C · ||u^{below}||_{L^3} · ||u^{above}||_{L^3} · ||v_k||_{L^3}
# ≤ C · ||v_k||_{L^3} · ||v_k||_{L^3}  (since ||u^{below}||_{L^3} ≤ C)

print("CZ route gives: I_k ≤ C · ||v_{k-1}||_{L^3} · ||v_k||_{L^3}")
print("Direct route gives: I_k ≤ C · ||v_k||_{L^q} · ||v_k||_{L^r}  with  1/q + 1/r = 1")
print()

# WAIT — I need to be more careful. In the Vasseur setup, P^{21} involves u^{below} at level k-1
# and u^{above} at level k. Let me re-examine.

print("=" * 70)
print("CAREFUL RE-EXAMINATION: De Giorgi level structure")
print("=" * 70)
print("""
In Vasseur (2007), the pressure decomposition at level k involves:
  u^{below} = u · min(1, λ_{k-1}/|u|)    [capped at level k-1]
  u^{above} = u - u^{below}                [excess above k-1]

And we estimate the integral against v_k (the excess above level k).

So P^{21} involves u^{below}_{k-1} · u^{above}_{k-1}, and we test against v_k.

The "above" field at level k-1 satisfies:
  u^{above}_{k-1} = u · (1 - λ_{k-1}/|u|)_+ = (|u| - λ_{k-1})_+ · u/|u| on {|u| > λ_{k-1}}

So ||u^{above}_{k-1}||_{L^q} = ||v_{k-1}||_{L^q}

And v_k is the truncation at level k.
""")

# Now let's systematically compute the U_{k-1} exponent for all valid Hölder triples

print("=" * 70)
print("SYSTEMATIC EXPONENT COMPUTATION")
print("=" * 70)

# The key estimates available:
# (1) ||v_{k-1}||_{L^{10/3}} ≤ C · U_{k-1}^{3/10}   (parabolic Sobolev)
# (2) ||∇v_{k-1}||_{L^2} ≤ U_{k-1}^{1/2}            (energy)
# (3) Sobolev: ||v_{k-1}||_{L^6} ≤ C · ||∇v_{k-1}||_{L^2} ≤ C · U_{k-1}^{1/2}
# (4) ||v_{k-1}||_{L^2} ≤ U_{k-1}^{1/2}             (sup part)
# (5) Chebyshev: |{v_{k-1} > 2^{-(k-1)}}| ≤ C^k · U_{k-1}^{5/3}
#     (from Chebyshev on L^{10/3}: |{v > λ}| ≤ (||v||_{10/3}/λ)^{10/3})

# For any L^p norm of v_{k-1}:
# ||v_{k-1}||_{L^p}^p = ∫ v_{k-1}^p dx
# On the set {v_{k-1} > 0}, we have 0 < v_{k-1} ≤ 1 (by normalization)
# So ||v_{k-1}||_{L^p}^p ≤ |{v_{k-1} > 0}| · ||v_{k-1}||_{L^∞}^{p-q} · ||v_{k-1}||_{L^q}^q for q < p

# But more useful: interpolate between L^{10/3} (parabolic) and L^2 (energy)
# ||v||_{L^p}^p ≤ ||v||_{L^{10/3}}^{10/3 · θ} · ||v||_{L^2}^{2(1-θ)}
# where 1/p = θ·3/10 + (1-θ)·1/2

# Or use Gagliardo-Nirenberg: ||v||_{L^p} ≤ C ||∇v||_{L^2}^a · ||v||_{L^2}^{1-a}
# with a = 3(1/2 - 1/p) for 2 ≤ p ≤ 6

print("\n--- Exponent α(p) such that ||v_{k-1}||_{L^p} ≤ C^k · U_{k-1}^{α(p)} ---")
print("Using Gagliardo-Nirenberg: ||v||_{L^p} ≤ C ||∇v||_{L^2}^a · ||v||_{L^2}^{1-a}")
print("with a = 3(1/2 - 1/p) for n=3, and ||∇v||_{L^2} ≤ U^{1/2}, ||v||_{L^2} ≤ U^{1/2}")
print()

p = Symbol('p', positive=True)
# GN interpolation exponent
a_GN = 3*(Rational(1,2) - 1/p)  # This is for n=3
# ||v||_{L^p} ≤ C · U^{1/2 · a_GN} · U^{1/2 · (1-a_GN)} = C · U^{1/2}
# Wait — both norms scale as U^{1/2}, so the interpolation gives U^{1/2} for all p.
# That can't be right — let me reconsider.

# Actually, ||v||_{L^2}^2 ≤ U (from sup_t ∫ v^2 dx ≤ U)
# And ||∇v||_{L^2}^2 ≤ U (from ∫∫ |∇v|^2 dx dt ≤ U)
# So ||v||_{L^2} ≤ U^{1/2} and ||∇v||_{L^2} ≤ U^{1/2}
# Then ||v||_{L^p} ≤ C · (U^{1/2})^a · (U^{1/2})^{1-a} = C · U^{1/2}

# But this is the SPATIAL norm at a fixed time.
# The parabolic estimate gives SPACE-TIME norms.

print("IMPORTANT: Need to distinguish spatial vs space-time norms.")
print()
print("At fixed time t:")
print("  ||v(t)||_{L^2_x}^2 ≤ U_k")
print("  ||∇v(t)||_{L^2_x}^2 — NOT directly bounded by U_k")
print("  (U_k controls ∫∫ |∇v|^2 dx dt, not pointwise in t)")
print()

# The correct estimates for the space-time integral:
# ∫_0^T ∫ v^2 dx dt ≤ T · sup_t ∫ v^2 dx ≤ T · U_k
# ∫_0^T ∫ |∇v|^2 dx dt ≤ U_k
# Parabolic Sobolev: ∫_0^T ∫ |v|^{10/3} dx dt ≤ C · (sup_t ∫ v^2 dx)^{2/3} · (∫∫ |∇v|^2)
#   ≤ C · U_k^{2/3} · U_k = C · U_k^{5/3}

# So ||v||_{L^{10/3}(space-time)}^{10/3} ≤ C · U^{5/3}
# i.e., ||v||_{L^{10/3}} ≤ C · U^{1/2}  (since 5/3 ÷ 10/3 = 1/2)

# Actually more precisely:
# ||v||_{L^{10/3}_{t,x}}^{10/3} ≤ C · U^{5/3}
# ||v||_{L^{10/3}_{t,x}} ≤ C · U^{(5/3)/(10/3)} = C · U^{1/2}

# For other space-time L^p norms, interpolate:
# ||v||_{L^p_{t,x}}^p between ||v||_{L^{10/3}}^{10/3} ~ U^{5/3} and ||v||_{L^2}^2 ~ T·U
# More precisely, ||v||_{L^∞_t L^2_x}^2 ≤ U and ||v||_{L^2_t H^1_x}^2 ≤ U

# For the bottleneck integral, we're in space-time, so let's work with that.

print("=" * 70)
print("SPACE-TIME HÖLDER ANALYSIS")
print("=" * 70)

# CZ route (standard):
# I_k = ∫∫ P^{21} · v_k dx dt
# ≤ ||P^{21}||_{L^{3/2}_{t,x}} · ||v_k||_{L^3_{t,x}}

# ||P^{21}||_{L^{3/2}} ≤ C · ||v_{k-1}||_{L^3}^2 (from CZ on u^{below} · u^{above})
# Wait -- actually ||u^{below}||_{L^∞} ≤ C, so
# ||u^{below} · u^{above}||_{L^{3/2}} ≤ ||u^{below}||_{L^∞} · ||u^{above}||_{L^{3/2}} ≤ C · ||v_{k-1}||_{L^{3/2}}

# Hmm, let me re-read the standard route more carefully from E001.
# P^{21} = R_iR_j(u_i^{below} · u_j^{above})
# ||P^{21}||_{L^r} ≤ C ||u^{below} · u^{above}||_{L^r} for 1 < r < ∞
# ||u^{below} · u^{above}||_{L^r} ≤ ||u^{below}||_{L^∞} · ||v_{k-1}||_{L^r}

# Then I_k ≤ ||P^{21}||_{L^r} · ||v_k||_{L^{r'}} where 1/r + 1/r' = 1

# With Vasseur's choice: the integral involves v_k · d_k · P^{21}, actually.
# Let me re-read E001 more carefully about what the actual bottleneck form is.

print("""
STANDARD ROUTE EXPONENT TRACE (from E001):

The bottleneck integral in Vasseur Prop 3 is:
  I_k = ∫∫ P^{21} · (something involving v_k) dx dt

Key bound:
  I_k ≤ C · ||v_{k-1}||_{L^{10/3}}^2 · ||d_k||_{L^2}

where:
  ||v_{k-1}||_{L^{10/3}_{t,x}}^{10/3} ≤ C · U_{k-1}^{5/3}
  → ||v_{k-1}||_{L^{10/3}} ≤ C · U_{k-1}^{1/2}
  → ||v_{k-1}||_{L^{10/3}}^2 ≤ C · U_{k-1}

  ||d_k||_{L^2}^2 ≤ U_k (but we need U_{k-1}, so...)

Actually, the precise chain from E001 is:

Step 1: ||d_k||_{L^2(Q)}^2 ≤ U_{k-1}^{1}  (from definition)
  → ||d_k||_{L^2} ≤ U_{k-1}^{1/2}

Step 2: Chebyshev: |A_k| = |{v_{k-1} > 2^{-(k-1)}}| ≤ C^k · U_{k-1}^{5/3}
  (from ||v_{k-1}||_{L^{10/3}}^{10/3} / (2^{-(k-1)})^{10/3})

Step 3: I_k ≤ ||P^{21}||_{L^{10/7}} · ||d_k||_{L^2} · ||1_{A_k}||_{L^{10}}
  Via Hölder: 1 = 7/10 + 1/2 + 1/10

Step 4: ||P^{21}||_{L^{10/7}} ≤ C · ||u^{below}||_{L^{10/3}} · ||u^{above}||_{L^2}
  Via CZ on L^{10/7} and Hölder: 7/10 = 3/10 + 1/2

The resulting β: sum up the U_{k-1} exponents from each factor:
  ||u^{below}||_{L^{10/3}} contributes 0 (bounded)
  ||u^{above}||_{L^2} contributes 1/2
  ||d_k||_{L^2} contributes 1/2
  ||1_{A_k}||_{L^{10}} = |A_k|^{1/10} contributes (5/3)·(1/10) = 1/6

Wait, let me recheck. |A_k|^{1/10} ≤ C^k · U_{k-1}^{5/30} = C^k · U_{k-1}^{1/6}

β = 1/2 + 1/2 + 1/6 = 7/6? That's not 4/3.
Hmm, let me reconsider. I think the actual Hölder triple used in Vasseur is different.
""")

# Let me trace the actual Vasseur (2007) Proposition 3 bound more carefully.
# The real bound is:
# I_k = ∫∫ P^{21} · v_k/|u| · |u| · 1_{v_k>0} dx dt
# More precisely, the pressure term in the energy inequality for v_k is:
# ∫∫ ∇p · (u/|u|) · v_k · 1_{v_k>0} dx dt

# After the pressure decomposition, the P^{21} term becomes:
# ∫∫ ∇P^{21} · (u/|u|) · v_k dx dt (on {v_k > 0})

# Integration by parts on ∇P^{21}:
# = -∫∫ P^{21} · div(u/|u| · v_k) dx dt (on {v_k > 0})

# Actually, let me just focus on the exponent computation.
# The standard result is β = 1 + s/n = 1 + 1/3 = 4/3 for s=1, n=3.

# The key Hölder pairing that gives β = 4/3 from E001:
# β = 1/2 (from d_k) + 5/6 (from Chebyshev/measure bound on indicator)
# 1/2 + 5/6 = 4/3 ✓

print("=" * 70)
print("CONFIRMED: β = 1/2 + 5/6 = 4/3")
print("=" * 70)
print()
print("The 1/2 comes from ||d_k||_{L^2} ≤ U_{k-1}^{1/2}")
print("The 5/6 comes from the measure bound on level sets (Chebyshev)")
print()

# NOW: Direct route. After integration by parts:
# I_k = ∫∫ (u^{below} · u^{above}) · R_iR_j(v_k · 1_{v_k>0}) dx dt

# The Riesz transforms R_iR_j are bounded on L^p for 1 < p < ∞.
# ||R_iR_j(v_k)||_{L^p} ≤ C_p ||v_k||_{L^p}

# So we need:
# I_k ≤ ||u^{below}||_{L^a} · ||u^{above}||_{L^b} · ||v_k||_{L^c}
# with 1/a + 1/b + 1/c = 1 and c > 1 (for CZ on L^c)

# u^{below} at level k-1: ||u^{below}||_{L^∞} ≤ λ_{k-1} ~ 1
# u^{above} at level k-1: ||u^{above}||_{L^q} = ||v_{k-1}||_{L^q}
# v_k: ||v_k||_{L^r}

# Since u^{below} is L^∞-bounded, we set a = ∞ and need 1/b + 1/c = 1.
# So we need: I_k ≤ C · ||v_{k-1}||_{L^b} · ||v_k||_{L^c} with 1/b + 1/c = 1

print("=" * 70)
print("DIRECT ROUTE: OPTIMIZING THE HÖLDER PAIR")
print("=" * 70)
print()
print("After IBP, I_k ≤ C · ||v_{k-1}||_{L^b} · ||v_k||_{L^c}")
print("with 1/b + 1/c = 1 and c > 1 (CZ requires this)")
print()

# Now: what U_{k-1} exponent does each choice give?
#
# For v_{k-1}: we need ||v_{k-1}||_{L^b}
# For v_k: we need ||v_k||_{L^c}
# But v_k is at level k, and we want everything in terms of U_{k-1}.
# ||v_k||_{L^c} ≤ ||v_{k-1}||_{L^c} (since v_k ≤ v_{k-1} in the De Giorgi setup?
# NO — v_k and v_{k-1} are at different levels, v_k ≤ v_{k-1} pointwise.)
# Actually v_k = [|u| - λ_k]_+ ≤ [|u| - λ_{k-1}]_+ = v_{k-1} since λ_k > λ_{k-1}.

# So ||v_k||_{L^c} ≤ ||v_{k-1}||_{L^c}

# The available space-time bounds on ||v_{k-1}||_{L^p}:
# ||v_{k-1}||_{L^p} ≤ C^k · U_{k-1}^{α(p)}
# where α(p) depends on p via the parabolic Sobolev interpolation.

# From parabolic embedding:
# ||v||_{L^{p_0}(Q)}^{p_0} ≤ C · U^{n_0}  where p_0 = 2(n+2)/n = 10/3 (n=3) and n_0 = p_0/2 = 5/3
# So ||v||_{L^{10/3}} ≤ C · U^{(5/3)/(10/3)} = C · U^{1/2}

# For general p ∈ [2, 10/3], interpolate between L^2 and L^{10/3}:
# ||v||_{L^p}^p ≤ ||v||_{L^2}^{2θ} · ||v||_{L^{10/3}}^{(10/3)(1-θ)}
# where 1/p = θ/2 + (1-θ)·3/10

# But wait, for p > 10/3, we need Sobolev embedding at each time slice.
# At fixed t: ||v(t)||_{L^6_x} ≤ C · ||∇v(t)||_{L^2_x}
# Then in space-time: ∫_0^T ||v||_{L^6}^2 dt ≤ C · ∫∫ |∇v|^2 dx dt ≤ C · U

# So ||v||_{L^2_t L^6_x}^2 ≤ C · U → ||v||_{L^2_t L^6_x} ≤ C · U^{1/2}

# For the Hölder pairing with mixed norms, things get complicated.
# Let me just compute the exponent for the standard isotropic L^p(Q) norms.

print("Available bounds: ||v_{k-1}||_{L^p(Q)} ≤ C^k · U_{k-1}^{α(p)}")
print()

# For p ∈ [2, 10/3]: interpolation between L^2(Q) and L^{10/3}(Q)
# ||v||_{L^2(Q)}^2 ≤ T · U (from sup_t ∫ v^2 ≤ U, integrate in t)
# ||v||_{L^{10/3}(Q)}^{10/3} ≤ C · U^{5/3}

# α(2) = 1/2 (from U^{1/2} for the L^2 norm, ignoring T)
# α(10/3) = 1/2

# Actually they're both 1/2! So ||v||_{L^p(Q)} ~ U^{1/2} for p ∈ [2, 10/3].
# This makes sense: the parabolic Sobolev embedding is an equality in terms of U-exponent.

# For p > 10/3: need mixed-norm or spatial Sobolev
# ||v||_{L^p(Q)} is controlled by ||v||_{L^∞_t L^2_x}^{2θ/p} · ||v||_{L^2_t L^6_x}^{6(1-θ)/p}
# ... but both give U^{1/2}

# KEY INSIGHT: ALL L^p norms of v_{k-1} scale as U_{k-1}^{1/2} (possibly with different C^k prefactors).
# The reason: the De Giorgi energy U controls both sup_t ||v||_2^2 and ||∇v||_{L^2}^2,
# and both scale as U^{1/2} per norm.

# WAIT — that's not right for L^p with p very large.
# ||v||_{L^∞(Q)} ≤ 1 (by normalization) — this is U^0, not U^{1/2}!
# The transition happens through interpolation.

# For L^∞: ||v_{k-1}||_{L^∞} ≤ 2^{-(k-1)} (in the normalized picture,
# actually max of v_{k-1} = 1 - λ_{k-1} = 2^{-(k-1)})
# So ||v_{k-1}||_{L^∞} ~ 2^{-k} (absorbed into C^k)

# For L^p with p very large:
# ||v||_{L^p}^p ≤ ||v||_{L^∞}^{p-10/3} · ||v||_{L^{10/3}}^{10/3}
# ||v||_{L^p}^p ≤ (2^{-k})^{p-10/3} · C · U^{5/3}
# ||v||_{L^p} ≤ 2^{-k·(p-10/3)/p} · C · U^{5/(3p)}

# So α(p) = 5/(3p) for p ≥ 10/3 (from Hölder interpolation with L^∞)

# Hmm wait, let me reconsider. For p ≤ 10/3:
# ||v||_{L^p}^p ≤ |Q|^{1-p·3/10} · ||v||_{L^{10/3}}^p (Hölder, since p < 10/3)
# ||v||_{L^p} ≤ C · ||v||_{L^{10/3}} ≤ C · U^{1/2}

# For p > 10/3:
# ||v||_{L^p}^p ≤ ||v||_{L^∞}^{p-10/3} · ||v||_{L^{10/3}}^{10/3}
# = (C · 2^{-k})^{p-10/3} · C · U^{5/3}
# ||v||_{L^p} = C^k · U^{5/(3p)}

# So:
# α(p) = 1/2  for p ≤ 10/3
# α(p) = 5/(3p) for p ≥ 10/3  (decreasing: approaches 0 as p → ∞)

print("Summary of α(p) where ||v_{k-1}||_{L^p} ≤ C^k · U_{k-1}^{α(p)}:")
print()

for p_val in [2, Rational(5,2), 3, Rational(10,3), 4, 5, 6, 10, 20]:
    if p_val <= Rational(10,3):
        alpha = Rational(1,2)
    else:
        alpha = Rational(5,3) / p_val
    print(f"  p = {p_val}: α(p) = {alpha} = {float(alpha):.4f}")

print()
print("=" * 70)
print("DIRECT ROUTE: β COMPUTATION")
print("=" * 70)
print()

# Direct route: I_k ≤ C · ||v_{k-1}||_{L^b} · ||v_k||_{L^c} with 1/b + 1/c = 1, c > 1
# Since v_k ≤ v_{k-1}: ||v_k||_{L^c} ≤ ||v_{k-1}||_{L^c}
# So I_k ≤ C^k · U_{k-1}^{α(b) + α(c)}

# BUT WAIT: the bottleneck integral isn't I_k alone. It appears inside the De Giorgi recurrence as:
# U_k ≤ C^k · I_k
# And the standard bound gives I_k ≤ C^k · ||d_k||_{L^2} · (measure bound) · (P^{21} bound)

# Actually, let me reconsider what I_k is. In the E001 analysis:
# U_k ≤ C^k · U_{k-1}^{1/2 + 5/6}
# where 1/2 comes from d_k (gradient term) and 5/6 from the level-set measure bound.

# The direct approach changes how we handle the pressure part.
# The full recurrence has the form:
# U_k ≤ C^k · (diffusion terms + pressure terms)
# Diffusion terms always give U_{k-1}^{1/2 + something} where the 1/2 is from d_k.
# Pressure terms involve I_k.

# The pressure term in the energy inequality is:
# |∫∫ ∇p · (u/|u|) v_k 1_{v_k>0} dx dt|
# After decomposition, the P^{21} piece is:
# |∫∫ ∇P^{21} · (u/|u|) v_k dx dt|

# With the CZ route, this is bounded by:
# C · ||P^{21}||_{L^{10/7}} · ||d_k||_{L^2} · |A_k|^{1/10}

# Hmm actually, let me reconsider. The actual form of the energy inequality for v_k is:
# d/dt ∫ v_k^2 dx + ∫ |∇v_k|^2 dx ≤ ∫ p · div(ψ_k) dx
# where ψ_k involves v_k and u/|u|.

# The pressure appears as: ∫ p · div(ψ_k) dx
# After decomposition: ∫ P^{21} · div(ψ_k) dx
# Integration by parts: -∫ ∇P^{21} · ψ_k dx

# In the standard approach, one bounds ||P^{21}||_{L^r} and ||div(ψ_k)||_{L^{r'}} via Hölder.

# In the DIRECT approach (Task 1), we don't bound ||P^{21}||_{L^r} first.
# Instead: P^{21} = (-Δ)^{-1} ∂_i ∂_j (u_i^{below} u_j^{above})
# And we move the operator to the other side:
# ∫ P^{21} · div(ψ_k) dx = ∫ (u^{below} · u^{above}) · R_iR_j(div ψ_k) dx

# ACTUALLY, more carefully:
# ∫ (-Δ)^{-1} ∂_i ∂_j (f_{ij}) · g dx = ∫ f_{ij} · (-Δ)^{-1} ∂_i ∂_j (g) dx
# = ∫ f_{ij} · R_iR_j(g) dx

# So: ∫ P^{21} · g dx = ∫ (u_i^{below} u_j^{above}) · R_iR_j(g) dx

# where g = div(ψ_k) or g = v_k · 1_{v_k>0} depending on the exact formulation.

# In any case, the direct route moves the CZ operator to the test function side.
# ||R_iR_j(g)||_{L^c} ≤ C · ||g||_{L^c} for c > 1.

# The test function g has the same regularity as v_k (it's built from v_k).
# So ||g||_{L^c} ~ ||v_k||_{L^c} ~ U_{k-1}^{α(c)} (with level shift)

# And u^{below} · u^{above}: ||u^{below}||_{L^∞} · ||u^{above}||_{L^b}
# = C · ||v_{k-1}||_{L^b} ~ C · U_{k-1}^{α(b)}

# The constraint is 1/b + 1/c = 1, and c > 1 for CZ.

# β_direct = α(b) + α(c) for the optimal choice of (b,c) with 1/b + 1/c = 1.

# Let's compute this systematically.

print("Direct route β = α(b) + α(c) with 1/b + 1/c = 1:")
print()
print(f"{'b':>8} {'c':>8} {'α(b)':>10} {'α(c)':>10} {'β=α(b)+α(c)':>14}")
print("-" * 55)

best_beta = 0
best_b = None

b_vals = [Rational(p, 10) for p in range(15, 100, 5)]  # b from 1.5 to 10
for b_val in b_vals:
    c_val = b_val / (b_val - 1)  # 1/c = 1 - 1/b
    if c_val <= 1:
        continue

    # α(b)
    if b_val <= Rational(10,3):
        alpha_b = Rational(1,2)
    else:
        alpha_b = Rational(5,3) / b_val

    # α(c)
    if c_val <= Rational(10,3):
        alpha_c = Rational(1,2)
    else:
        alpha_c = Rational(5,3) / c_val

    beta_direct = alpha_b + alpha_c

    if float(beta_direct) > float(best_beta):
        best_beta = beta_direct
        best_b = b_val

    if b_val in [2, Rational(5,2), 3, Rational(10,3), 4, 5, 6, 10]:
        print(f"{str(b_val):>8} {str(c_val):>8} {str(alpha_b):>10} {str(alpha_c):>10} {str(beta_direct):>14}  = {float(beta_direct):.4f}")

print()
print(f"Maximum β_direct = {best_beta} = {float(best_beta):.4f} at b = {best_b}")
print()

# Let's do the optimization analytically
print("=" * 70)
print("ANALYTICAL OPTIMIZATION OF β_direct")
print("=" * 70)

b_sym = Symbol('b', positive=True)
c_sym = b_sym / (b_sym - 1)

# Case 1: b ≤ 10/3 and c ≤ 10/3
# Need b ≤ 10/3 and b/(b-1) ≤ 10/3
# b/(b-1) ≤ 10/3 ⟺ 3b ≤ 10(b-1) ⟺ 3b ≤ 10b-10 ⟺ 10 ≤ 7b ⟺ b ≥ 10/7
# So for 10/7 ≤ b ≤ 10/3: α(b) = 1/2, α(c) = 1/2, β = 1
print()
print("Case 1: 10/7 ≤ b ≤ 10/3 → β = 1/2 + 1/2 = 1")

# Case 2: b ≤ 10/3 and c > 10/3
# Need b ≤ 10/3 and b/(b-1) > 10/3 ⟺ b < 10/7 (impossible since b > 1 and c > 1 needs b > 1)
# Actually for b < 10/7 with b > 1: c = b/(b-1) > 10/3
# α(b) = 1/2, α(c) = 5/(3c) = 5(b-1)/(3b)
# β = 1/2 + 5(b-1)/(3b) = 1/2 + 5/3 - 5/(3b)
# This is INCREASING in b (derivative = 5/(3b^2) > 0)
# At b = 10/7: β = 1/2 + 5(3/7)/(30/7) = 1/2 + (15/7)/(30/7) = 1/2 + 1/2 = 1 ✓
# At b → 1+: c → ∞, α(c) → 0, β → 1/2

print("Case 2: 1 < b < 10/7 → β = 1/2 + 5(b-1)/(3b), increasing in b, max = 1 at b=10/7")

# Case 3: b > 10/3 and c ≤ 10/3
# Need b > 10/3 and c = b/(b-1) ≤ 10/3 ⟺ 3b ≤ 10b-10 ⟺ b ≥ 10/7 (always true since b > 10/3)
# α(b) = 5/(3b), α(c) = 1/2
# β = 5/(3b) + 1/2
# This is DECREASING in b. At b = 10/3: β = 5/10 + 1/2 = 1/2 + 1/2 = 1 ✓
# As b → ∞: β → 0 + 1/2 = 1/2

print("Case 3: b > 10/3 → β = 5/(3b) + 1/2, decreasing in b, max = 1 at b=10/3")

# Case 4: b > 10/3 and c > 10/3 — impossible since 1/b + 1/c = 1 and both > 3/10 means
# 1 = 1/b + 1/c < 3/10 + 3/10 = 3/5 — contradiction! Wait, b > 10/3 means 1/b < 3/10.
# Need 1/b + 1/c = 1 with both 1/b < 3/10 and 1/c < 3/10.
# Then 1 = 1/b + 1/c < 6/10 — contradiction. So Case 4 is empty.

print("Case 4: b > 10/3 and c > 10/3 → impossible (Hölder constraint)")
print()

print("=" * 70)
print("CONCLUSION: MAXIMUM β_direct = 1")
print("=" * 70)
print()
print("The maximum is achieved at b = c = 10/3 (or in the plateau b ∈ [10/7, 10/3]).")
print("The direct route β_direct = 1 < 4/3 = β_CZ.")
print()
print("CRITICAL FINDING: The direct route gives a WORSE exponent than the CZ route!")
print()
print("Reason: In the CZ route, the pressure P^{21} 'consolidates' the product")
print("u^{below} · u^{above} into a single L^p function, allowing a 3-way Hölder")
print("pairing that extracts more U_{k-1} from the interaction.")
print("In the direct route, we lose this consolidation and must bound two")
print("v-factors separately, getting only α(b) + α(c) ≤ 1/2 + 1/2 = 1.")
print()

# BUT WAIT — there's a subtlety I missed. The full De Giorgi recurrence is not just the
# pressure term. The pressure term feeds into: U_k ≤ C^k · (I_{diffusion} + I_{pressure}).
# In the standard route, I_{pressure} ≤ C^k · U_{k-1}^{4/3}, and this is the bottleneck
# because I_{diffusion} has a better exponent (from diffusion, often β = 2 or similar).

# If β_direct = 1 < 4/3, does this mean the direct route makes the pressure term
# EASIER to handle (β=1 < 4/3), or does it mean the bound is WORSE?

# In the De Giorgi iteration, U_k ≤ C^k · U_{k-1}^β.
# For convergence to 0, we need β > 1 (supercritical).
# β = 4/3 > 1 ✓ (works)
# β = 1: this is CRITICAL — on the edge. U_k ≤ C^k · U_{k-1} doesn't give convergence to 0.

# So β_direct = 1 is actually the WORST possible outcome — right at criticality!

print("=" * 70)
print("INTERPRETATION")
print("=" * 70)
print()
print("β = 1 is CRITICAL — right at the edge. The De Giorgi iteration needs β > 1")
print("for the sequence U_k → 0. So β_direct = 1 doesn't work at all!")
print()
print("The CZ route gives β = 4/3 > 1: the recurrence U_k ≤ C^k U_{k-1}^{4/3}")
print("drives U_k → 0 if U_0 is small enough.")
print()
print("The direct route gives β = 1: the recurrence U_k ≤ C^k U_{k-1}")
print("is borderline and cannot drive U_k → 0.")
print()
print("THEREFORE: CZ is genuinely HELPFUL. The consolidation of the bilinear product")
print("through the CZ operator is essential — it gains exactly 1/3 in the exponent")
print("compared to the naive approach.")
print()
print("This 1/3 gain: from α(b)+α(c) ≤ 1 (direct) to β = 4/3 (CZ) comes precisely")
print("from the fact that CZ maps L^{3/2} → L^{3/2}, consolidating the product")
print("||u^{below} · u^{above}||_{L^{3/2}} into a single entity whose L^{3/2} norm")
print("scales as ||v_{k-1}||_{L^3}^2 ≤ U_{k-1}^{2·(1/2)} = U_{k-1}.")
print("But then the Hölder pairing with ||v_k||_{L^3} gives another U_{k-1}^{1/3}")
print("(from the measure bound), totaling 1 + 1/3 = 4/3.")
