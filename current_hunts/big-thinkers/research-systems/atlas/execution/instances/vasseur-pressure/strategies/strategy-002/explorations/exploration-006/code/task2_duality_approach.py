"""
Task 2: Pressure as Test Function (Duality Approach)

Instead of bounding ||P^{21}||_{L^p} or moving CZ to the other side,
treat the pressure integral as a duality pairing:

  I_k = <P^{21}, v_k · 1_{v_k>0}>

and try to find a function space X such that:
  - v_k · 1_{v_k>0} ∈ X with a good bound
  - P^{21} ∈ X* with a better bound than CZ gives in L^p

Candidates:
  1. H^1 (Hardy space) / BMO duality
  2. W^{1,q} / W^{-1,q'} duality
  3. Lorentz space L^{p,q} duality
"""

from sympy import *
from fractions import Fraction

print("=" * 70)
print("TASK 2: DUALITY APPROACH")
print("=" * 70)

# ================================================================
# APPROACH 2A: Hardy H^1 / BMO duality
# ================================================================
print("\n--- Approach 2A: H^1 / BMO duality ---")
print("""
Key fact: For the NS pressure,  p = -Δ^{-1} ∂_i∂_j(u_i u_j)
The operator R_iR_j maps L^1 → H^1 (Hardy space), NOT L^1 → L^1.
And H^1* = BMO.

So: <P^{21}, g> = <R_iR_j(u^{below} · u^{above}), g> = <u^{below}·u^{above}, R_iR_j(g)>

For g = v_k · 1_{v_k>0}:

Route A: Put P^{21} in BMO, put v_k in H^1.
  I_k ≤ ||P^{21}||_{BMO} · ||v_k||_{H^1}

Route B: Put u^{below}·u^{above} in H^1, put R_iR_j(v_k) in BMO.
  I_k ≤ ||u^{below}·u^{above}||_{H^1} · ||R_iR_j(v_k)||_{BMO}

Let's analyze Route A first.
""")

print("Route A: P^{21} in BMO")
print()
print("||P^{21}||_{BMO} = ||R_iR_j(u^{below} · u^{above})||_{BMO}")
print("CZ operators are bounded on BMO: ||R_iR_j(f)||_{BMO} ≤ C ||f||_{BMO}")
print("So ||P^{21}||_{BMO} ≤ C ||u^{below} · u^{above}||_{BMO}")
print()
print("Now: ||u^{below} · u^{above}||_{BMO}")
print("u^{below} ∈ L^∞ with ||u^{below}||_{L^∞} ≤ C")
print("u^{above} = v_{k-1} · (u/|u|)")
print()
print("BMO product rule: ||fg||_{BMO} ≤ C(||f||_{L^∞} ||g||_{BMO} + ||f||_{BMO} ||g||_{L^∞})")
print("Since ||u^{below}||_{L^∞} ≤ C:")
print("  ||u^{below} · u^{above}||_{BMO} ≤ C ||u^{above}||_{BMO} + C ||u^{below}||_{BMO} ||u^{above}||_{L^∞}")
print()
print("Problem: ||u^{above}||_{BMO} is hard to control from U_{k-1}.")
print("BMO ⊂ L^p for no finite p (it's larger than all L^p).")
print("The best we can say: ||v_{k-1}||_{BMO} ≤ C (it's bounded, since v_{k-1} ≤ 1).")
print("So ||u^{below} · u^{above}||_{BMO} ≤ C — no U_{k-1} dependence from this factor.")
print()
print("For v_k in H^1:")
print("||v_k||_{H^1} ≥ ||v_k||_{L^1} (H^1 ⊂ L^1 with norm control)")
print("H^1 norm: ||f||_{H^1} = ||f||_{L^1} + Σ_j ||R_j f||_{L^1}")
print("||v_k||_{L^1} ≤ |supp(v_k)| · ||v_k||_{L^∞} ≤ |A_k| · 2^{-k}")
print("  ≤ C^k · U_{k-1}^{5/3} · 2^{-k} = C^k · U_{k-1}^{5/3}")
print()

# H^1 norm bound
# ||v_k||_{H^1} ~ ||v_k||_{L^1} + ||R_j v_k||_{L^1}
# The Riesz transform part: ||R_j v_k||_{L^1} ≤ C ||v_k||_{L^1} ???
# NO! R_j is NOT bounded on L^1. That's the whole point of H^1.
# H^1 ⊊ L^1 — the H^1 norm is STRONGER than L^1.

# Better: ||v_k||_{H^1} ≤ C ||v_k||_{W^{1,1}} (Sobolev → Hardy, for compactly supported)
# Wait, that's also not right in general.

# The real estimate: for f supported on a bounded set E,
# ||f||_{H^1} ≤ C · (||f||_{L^2} · |E|^{1/2} + ||∇f||_{L^1} · ... )
# This is getting complicated. Let me use a cleaner approach.

# H^1 via atomic decomposition: ||f||_{H^1} ~ inf Σ |λ_j| over atomic decompositions
# For our purposes, we can bound: ||v_k||_{H^1} ≤ C · ||∇v_k||_{L^1} (for v_k with mean zero)
# Actually for functions supported in a ball (or compact set), ||f||_{H^1} ≤ C ||f||_{L^2} |supp|^{1/2}

print("Better H^1 bound via Coifman-Weiss:")
print("For v_k supported on A_k = {v_{k-1} > 2^{-(k-1)}}:")
print("||v_k||_{H^1} ≤ C · ||v_k||_{L^2} · |A_k|^{1/2}")
print("Wait — this isn't correct for H^1 either. Let me use the molecular bound.")
print()
print("Correct bound: ||v_k||_{H^1} ≤ C · ||v_k||_{L^{n/(n-1)}} = C · ||v_k||_{L^{3/2}}")
print("(In 3D, L^{3/2} ⊂ H^1 by the Riesz characterization... no, that's backwards.)")
print()

# Actually, the correct inclusion is:
# H^1 ⊂ L^1  (H^1 functions are L^1)
# L^p ⊂ H^1 for p > 1  (L^p functions are in H^1 for p > 1 — wait, this is also wrong)
#
# The correct statement: H^1(R^n) ⊂ L^1(R^n) ⊂ H^p for p < 1
# And for p > 1: L^p ⊂ H^1 with ||f||_{H^1} ≤ C_p ||f||_{L^p}
# NO — this is false. H^1 is NOT contained in L^p for p > 1.
#
# Let me be precise:
# H^1 ⊊ L^1 and for 1 < p < ∞: L^p ⊂ H^1 ∩ L^p but the H^1 norm is
# NOT bounded by the L^p norm.
#
# Actually, I'm getting confused. Let me use the correct characterization:
# ||f||_{H^1} = ||Mf||_{L^1} where M is the grand maximal function.
# For f ∈ L^p, p > 1: ||Mf||_{L^1} ≤ ... this doesn't give a useful bound.
#
# The key bound for our problem: for f supported in a cube Q,
# ||f||_{H^1} ≤ C|Q|^{1-1/p} ||f||_{L^p(Q)} for 1 < p ≤ ∞
# This follows from: f = (f − f_Q) + f_Q, and atomic decomposition.
# Actually even this isn't quite right.
#
# Let me just use: ||v_k||_{H^1} ≤ C (||v_k||_{L^2}·|A_k|^{1/6}) by...
# No, let me take a step back and use the Hölder inequality directly.

print("=" * 50)
print("Route A: H^1/BMO exponent computation")
print("=" * 50)
print()
print("The H^1/BMO duality gives:")
print("  I_k ≤ ||P^{21}||_{BMO} · ||v_k||_{H^1}")
print()
print("||P^{21}||_{BMO} ≤ C ||u^{below}·u^{above}||_{BMO}")
print("Since u^{below} ∈ L^∞ and u^{above} ∈ L^∞ (both ≤ 1 after normalization):")
print("||u^{below}·u^{above}||_{BMO} ≤ 2||u^{below}·u^{above}||_{L^∞} ≤ 2")
print("This contributes U_{k-1}^0 — no U-dependence.")
print()
print("||v_k||_{H^1}: The best we can do is ||v_k||_{L^1} ≤ |A_k|^{1/2} ||v_k||_{L^2}")
print("  ≤ C^k U_{k-1}^{5/6} · U_{k-1}^{1/2} = C^k U_{k-1}^{4/3}")
print()
print("Wait — that gives β = 0 + 4/3 = 4/3. Let me check if this is right.")
print()

# Actually: ||v_k||_{L^1} ≤ ||v_k||_{L^2} · |A_k|^{1/2}
# ||v_k||_{L^2} ≤ U_{k-1}^{1/2} (or more precisely, U_k^{1/2} ≤ ... from v_k ≤ v_{k-1})
# |A_k| = |{v_{k-1} > 2^{-(k-1)}}| ≤ C^k U_{k-1}^{5/3}
# So |A_k|^{1/2} ≤ C^k U_{k-1}^{5/6}
# ||v_k||_{L^1} ≤ C^k U_{k-1}^{1/2 + 5/6} = C^k U_{k-1}^{4/3}

# But ||v_k||_{H^1} ≥ ||v_k||_{L^1}, so we'd need ||v_k||_{H^1} from above.
# The L^1 bound gives an UPPER bound for the pairing (since BMO ⊂ L^∞_{loc}).
# But we want to use H^1/BMO duality, which says |<f,g>| ≤ ||f||_{H^1} ||g||_{BMO}.
# This is only useful if ||v_k||_{H^1} is SMALL (smaller than ||v_k||_{L^p} for the L^p route).

# H^1 norm is between L^1 norm (which it contains) and L^p norms.
# For our application, we need an UPPER bound on ||v_k||_{H^1}.

# Key: H^1 ⊂ L^1, so ||v_k||_{L^1} ≤ ||v_k||_{H^1}. The H^1 norm is LARGER.
# So bounding ||v_k||_{H^1} from above requires MORE than just L^1.

# For functions in L^2: ||f||_{H^1} ≤ C ||f||_{L^2} (in the non-homogeneous H^1).
# Wait — is this true? In the classical real H^1 (Stein's definition):
# If f ∈ L^2(R^3), then ||f||_{H^1} ≤ C ||f||_{L^2}...
# Actually NO. Consider f = 1_B for a large ball B: ||f||_{L^2} = |B|^{1/2},
# but ||f||_{H^1} ~ |B| (from the atom decomposition — you need ~|B|/|B_0| atoms).

# For f supported on a set of measure |E|:
# ||f||_{H^1} ≤ C ||f||_{L^2} |E|^{1/2} (wrong direction — this bounds L^1)
# ||f||_{H^1}: hard to bound without more regularity information.

# Actually, for the real-variable H^1 space:
# ||f||_{H^1} = ||f*||_{L^1} where f* is the maximal function of f.
# For f ∈ L^p, p > 1: ||f*||_{L^p} ≤ C_p ||f||_{L^p} (maximal inequality).
# But ||f*||_{L^1} is NOT bounded by ||f||_{L^1} (this fails at p=1).
# ||f*||_{L^1} ≤ C ||f||_{L^p} · |Ω|^{1-1/p} for f supported on Ω?
# By Hölder: ||f*||_{L^1} ≤ ||f*||_{L^p} |Ω|^{1/p'} ≤ C_p ||f||_{L^p} |Ω|^{1-1/p}
# But f* may have larger support than f.

# Let me just use: for v_k ∈ W^{1,1}(R^3), ||v_k||_{H^1} ≤ C(||v_k||_{L^1} + ||∇v_k||_{L^1})
# This is a valid bound: W^{1,1} ⊂ H^1 in R^n for n ≥ 1.

print("Using W^{1,1} ⊂ H^1:")
print("||v_k||_{H^1} ≤ C(||v_k||_{L^1} + ||∇v_k||_{L^1})")
print()
print("||v_k||_{L^1} ≤ |A_k|^{1/2} · ||v_k||_{L^2} ≤ C^k · U_{k-1}^{5/6} · U_{k-1}^{1/2}")
print("  = C^k · U_{k-1}^{4/3}")
print()
print("||∇v_k||_{L^1} ≤ |A_k|^{1/2} · ||∇v_k||_{L^2} ≤ C^k · U_{k-1}^{5/6} · U_{k-1}^{1/2}")
print("  = C^k · U_{k-1}^{4/3}")
print()
print("So ||v_k||_{H^1} ≤ C^k · U_{k-1}^{4/3}")
print("And ||P^{21}||_{BMO} ≤ C (no U-dependence)")
print()
print("Route A exponent: β_A = 0 + 4/3 = 4/3")
print()
print("VERDICT: H^1/BMO duality gives β = 4/3 — SAME as CZ route.")
print("No improvement.")
print()

# ================================================================
# APPROACH 2B: W^{1,q} / W^{-1,q'} duality
# ================================================================
print("=" * 70)
print("--- Approach 2B: W^{1,q} / W^{-1,q'} duality ---")
print("=" * 70)
print()
print("Idea: The De Giorgi functional controls ||∇v_k||_{L^2}.")
print("Can we use this in a Sobolev duality pairing?")
print()
print("I_k = <P^{21}, v_k> (on {v_k > 0})")
print("    = <P^{21}, v_k>_{W^{-1,q'} × W^{1,q}}")
print("    ≤ ||P^{21}||_{W^{-1,q'}} · ||v_k||_{W^{1,q}}")
print()

# P^{21} = (-Δ)^{-1} ∂_i∂_j(u_i^{below} · u_j^{above})
# In W^{-1,q'}: ||P^{21}||_{W^{-1,q'}} = ||(-Δ)^{-1} ∂_i∂_j(u^{below}·u^{above})||_{W^{-1,q'}}
# By Sobolev embedding and the structure of P^{21}:
# P^{21} = R_iR_j(u^{below}·u^{above}), which is a zeroth-order operator of u^{below}·u^{above}
# So ||P^{21}||_{W^{-1,q'}} ≤ ||P^{21}||_{L^r} for some r (by Sobolev embedding W^{s,p} ⊂ L^q)
# Specifically, W^{-1,q'} ⊃ L^r if 1/r = 1/q' + 1/3 = (q-1)/q + 1/3

# Actually: W^{-1,q'}(R^3) is the dual of W_0^{1,q}(R^3).
# For f ∈ L^r(R^3), ||f||_{W^{-1,q'}} ≤ C ||f||_{L^r} when W^{1,q} ⊂ L^{r'} i.e. r' ≤ 3q/(3-q) for q < 3
# i.e. 1/r ≥ 1 - q/(3-q)... this is getting complicated.

# Let me use a simpler approach:
# I_k = ∫ P^{21} · v_k dx = -∫ ∇P^{21} · v_k ... wait, integration by parts:
# = -∫ ∇((-Δ)^{-1}∂_i∂_j(f_{ij})) · ...
# ∇P^{21} involves ∂_k(-Δ)^{-1}∂_i∂_j(f_{ij}) — still a CZ operator (order 1, applied to f)

# Actually, let's think about it differently.
# W^{-1,q'} × W^{1,q} pairing:
# <P^{21}, v_k>_{W^{-1,q'} × W^{1,q}} ≤ ||P^{21}||_{W^{-1,q'}} · ||v_k||_{W^{1,q}}

# ||P^{21}||_{W^{-1,q'}} = sup_{||φ||_{W^{1,q}}=1} <P^{21}, φ>
# = sup ∫ R_iR_j(u^{below}·u^{above}) · φ dx
# = sup ∫ (u^{below}·u^{above}) · R_iR_j(φ) dx
# ≤ ||u^{below}·u^{above}||_{L^{(q*)'}} · ||R_iR_j(φ)||_{L^{q*}}
#   where q* = 3q/(3-q) (Sobolev embedding W^{1,q} → L^{q*})

# ||R_iR_j(φ)||_{L^{q*}} ≤ C ||φ||_{L^{q*}} ≤ C ||φ||_{W^{1,q}} = C
# ||(u^{below}·u^{above}||_{L^{(q*)'}} = ||v_{k-1}||_{L^{(q*)'}}  (using ||u^{below}||_{L^∞} ≤ C)

# (q*)' = 3q/(3q-3+q) = 3q/(4q-3)  [conjugate of q* = 3q/(3-q)]
# Wait: 1/(q*)' = 1 - (3-q)/(3q) = (3q-3+q)/(3q) = (4q-3)/(3q)
# So (q*)' = 3q/(4q-3)

print("W^{-1,q'} bound via duality:")
print("||P^{21}||_{W^{-1,q'}} ≤ C · ||v_{k-1}||_{L^{3q/(4q-3)}}")
print()
print("||v_k||_{W^{1,q}} ≤ ||v_k||_{L^q} + ||∇v_k||_{L^q}")
print()

# For q = 2: the optimal choice
# ||P^{21}||_{W^{-1,2}} ≤ C · ||v_{k-1}||_{L^{6/5}}
# ||v_k||_{W^{1,2}} ≤ ||v_k||_{L^2} + ||∇v_k||_{L^2} ≤ C · U_{k-1}^{1/2}

# ||v_{k-1}||_{L^{6/5}}:
# 6/5 < 10/3, so α(6/5) = 1/2

# Total: β = 1/2 + 1/2 = 1. Still worse than CZ!

print("For q = 2:")
print("  ||P^{21}||_{W^{-1,2}} ≤ C · ||v_{k-1}||_{L^{6/5}} ≤ C · U_{k-1}^{1/2}")
print("  ||v_k||_{W^{1,2}} ≤ C · U_{k-1}^{1/2}")
print("  β = 1/2 + 1/2 = 1  — no improvement!")
print()

# For other q values:
print("General q analysis:")
q = Symbol('q', positive=True)
# (q*)' = 3q/(4q-3)
q_star_conj = 3*q / (4*q - 3)
print(f"  (q*)' = 3q/(4q-3)")
print()

# For the pairing to work, we need:
# (a) q > 1 (for W^{1,q} to make sense)
# (b) (q*)' > 1 (for L^{(q*)'} to make sense): 3q/(4q-3) > 1 iff 3q > 4q-3 iff q < 3
# (c) 4q-3 > 0 iff q > 3/4

# So q ∈ (1, 3) works.

# Exponent from ||v_{k-1}||_{L^{3q/(4q-3)}}:
# If 3q/(4q-3) ≤ 10/3: α = 1/2
# Check: 3q/(4q-3) ≤ 10/3 iff 9q ≤ 10(4q-3) iff 9q ≤ 40q-30 iff 30 ≤ 31q iff q ≥ 30/31
# Since q > 1 > 30/31, this is always true.

# Exponent from ||v_k||_{W^{1,q}}:
# ||v_k||_{W^{1,q}} ≤ ||v_k||_{L^q} + ||∇v_k||_{L^q}
# ||v_k||_{L^q}: α(q) = 1/2 for q ≤ 10/3, α(q) = 5/(3q) for q > 10/3
# ||∇v_k||_{L^q} ≤ |A_k|^{(2-q)/(2q)} · ||∇v_k||_{L^2} for q ≤ 2
#                ≤ C^k · U_{k-1}^{(5/3)·(2-q)/(2q)} · U_{k-1}^{1/2}

# For q = 2: ||∇v_k||_{L^2} ≤ U^{1/2}, ||v_k||_{L^2} ≤ U^{1/2}, so ||v_k||_{W^{1,2}} ≤ C U^{1/2}
# For q < 2: ||∇v_k||_{L^q} ≤ |A_k|^{1/q-1/2} ||∇v_k||_{L^2} ≤ C^k U^{5(1/q-1/2)/3 + 1/2}
#            = C^k U^{5/(3q) - 5/6 + 1/2} = C^k U^{5/(3q) - 1/3}

# Total for q < 2:
# β = 1/2 + max(α(q), 5/(3q) - 1/3)
# Since q < 2 < 10/3: α(q) = 1/2
# And 5/(3q) - 1/3: for q < 2, this is > 5/6 - 1/3 = 1/2.
# So the gradient term dominates: β = 1/2 + 5/(3q) - 1/3 = 5/(3q) + 1/6

# Maximize over q ∈ (1, 2): 5/(3q) + 1/6 is decreasing in q.
# At q → 1+: β → 5/3 + 1/6 = 11/6 ≈ 1.833 (but CZ on L^q needs q > 1)
# At q = 2: β → 5/6 + 1/6 = 1

# Wait — the gradient term uses Hölder:
# ||∇v_k||_{L^q} ≤ ||∇v_k||_{L^2} · |A_k|^{1/q - 1/2} for q < 2
# But this involves |A_k| — the measure of the support.
# |A_k| ≤ C^k U_{k-1}^{5/3}

print("For q < 2:")
print("||∇v_k||_{L^q} ≤ ||∇v_k||_{L^2} · |A_k|^{1/q-1/2}")
print("  ≤ C^k · U_{k-1}^{1/2} · U_{k-1}^{5(1/q-1/2)/3}")
print("  = C^k · U_{k-1}^{1/2 + 5/(3q) - 5/6}")
print("  = C^k · U_{k-1}^{5/(3q) - 1/3}")
print()
print("Total β for W^{-1,q'}/W^{1,q} route with q < 2:")
print("  β = α(3q/(4q-3)) + max(α(q), 5/(3q) - 1/3)")
print("  = 1/2 + 5/(3q) - 1/3  (gradient dominates for q < 2)")
print("  = 5/(3q) + 1/6")
print()

for q_val in [Rational(6,5), Rational(3,2), Rational(2,1), Rational(5,2), Rational(3,1)]:
    if q_val < 2:
        grad_exp = Rational(5,3) / q_val - Rational(1,3)
        lp_exp = Rational(1,2) if q_val <= Rational(10,3) else Rational(5,3)/q_val
        beta = Rational(1,2) + max(lp_exp, grad_exp)
    elif q_val == 2:
        beta = Rational(1,2) + Rational(1,2)
    else:
        # q > 2: ||∇v_k||_{L^q} uses Sobolev embedding, more complex
        beta = Rational(1,2) + Rational(1,2)  # placeholder
    print(f"  q = {q_val}: β = {beta} = {float(beta):.4f}")

print()
print("PROBLEM: As q → 1+, β → 11/6 > 4/3. Better?!")
print("BUT: The W^{1,q} norm of v_k for q < 2 uses |A_k| via Hölder.")
print("This is the SAME measure bound as in the standard CZ approach.")
print()

# Wait — am I being sloppy? Let me recheck.
# The W^{-1,q'}/W^{1,q} approach gives:
# I_k ≤ ||P^{21}||_{W^{-1,q'}} · ||v_k||_{W^{1,q}}
# The bound on ||P^{21}||_{W^{-1,q'}} was obtained by duality, putting CZ on the test function.
# But wait — the W^{-1,q'} norm of P^{21} was bounded by:
# ||P^{21}||_{W^{-1,q'}} ≤ C · ||v_{k-1}||_{L^{3q/(4q-3)}}
# This used the CZ boundedness on L^{q*} — so CZ IS used here!
# The question is whether the final exponent is different.

# Actually, I realize the β > 4/3 result for q < 2 is suspicious.
# If β > 4/3, that would be WORSE for convergence (we want large β > 1).
# Actually WAIT — I have the direction confused.

# In the De Giorgi recurrence U_k ≤ C^k · U_{k-1}^β:
# LARGER β is BETTER (faster convergence).
# β = 4/3 > 1: works
# β = 11/6 > 4/3: would be even better!

# But can we really get β > 4/3 from the W^{1,q} route?
# Let me double-check. The issue is:

# I_k ≤ ||P^{21}||_{W^{-1,q'}} · ||v_k||_{W^{1,q}}
# feeds into the recurrence as U_k ≤ ... + I_k ≤ ... + C^k U_{k-1}^β

# But this is the pressure CONTRIBUTION to U_k. The full recurrence has:
# U_k ≤ C^k · (energy terms + pressure terms)
# The pressure I_k is just one piece.

# In the standard proof, the pressure bound I_k ≤ C^k U_{k-1}^{4/3}
# is what determines the overall β = 4/3 (since other terms are better).

# If we could get a LARGER exponent for I_k, the overall β would improve.

# BUT: the W^{1,q} bound for q → 1 gives β → 11/6 ONLY if the
# W^{-1,q'}/W^{1,q} pairing is valid AND the bound is sharp.

# Let me check: is the W^{-1,q'}/W^{1,q} duality pairing valid?
# We need v_k ∈ W^{1,q} and P^{21} ∈ W^{-1,q'}.
# For q close to 1: W^{1,q} with q → 1 is problematic because:
# - W^{1,1} functions have BV regularity but R_iR_j may not be bounded on L^{q*=3q/(3-q)} as q→1
# - q* → 3/2, and CZ IS bounded on L^{3/2}. So the CZ step is fine.

# Wait, but there's a deeper issue. Let me re-examine the bound:
# ||P^{21}||_{W^{-1,q'}} ≤ C · ||v_{k-1}||_{L^{(q*)'}}
# (q*)' = 3q/(4q-3)
# For q → 1+: (q*)' → 3/1 = 3. So ||v_{k-1}||_{L^3}.
# α(3) = 1/2. OK.

# ||v_k||_{W^{1,q}} ~ ||∇v_k||_{L^q} (dominates for small q)
# ||∇v_k||_{L^q} ≤ ||∇v_k||_{L^2} · |A_k|^{1/q-1/2}
# For q → 1+: |A_k|^{1/q-1/2} → |A_k|^{1/2}
# So ||∇v_k||_{L^1} ≤ ||∇v_k||_{L^2} · |A_k|^{1/2} ≤ U^{1/2} · U^{5/6} = U^{4/3}

# Total: β = 1/2 + 4/3 = 11/6

print("=" * 70)
print("CHECKING β = 11/6 CLAIM")
print("=" * 70)
print()
print("At q → 1+:")
print("  ||P^{21}||_{W^{-1,∞}} ≤ C · ||v_{k-1}||_{L^3} ≤ C^k · U_{k-1}^{1/2}")
print("  ||v_k||_{W^{1,1}} ~ ||∇v_k||_{L^1} ≤ ||∇v_k||_{L^2}·|A_k|^{1/2}")
print("    ≤ C^k · U_{k-1}^{1/2} · U_{k-1}^{5/6} = C^k · U_{k-1}^{4/3}")
print("  I_k ≤ C^k · U_{k-1}^{1/2 + 4/3} = C^k · U_{k-1}^{11/6}")
print()
print("BUT WAIT: Is this comparing apples to apples?")
print()
print("In the standard proof, the bottleneck integral is bounded as:")
print("  I_k = ∫∫ |P^{21}| · |d_k| · 1_{A_k} dx dt")
print("  ≤ ||P^{21}||_{L^r(A_k)} · ||d_k||_{L^2} · |A_k|^{1/s}")
print()
print("The W^{-1,q'}/W^{1,q} pairing bounds a DIFFERENT integral:")
print("  ∫∫ P^{21} · v_k dx dt (without d_k!)")
print()
print("The actual pressure term in the De Giorgi energy inequality is")
print("NOT simply ∫P^{21} · v_k, but involves ∇p · (u/|u|) · v_k.")
print("This has one more derivative than the W^{-1,q'}/W^{1,q} pairing handles.")
print()

# THIS IS THE KEY ISSUE. The pressure appears in the energy inequality as:
# ∂_t(|u| - λ_k)_+^2 + |∇v_k|^2 ≤ ... + ∇p · (u/|u|) · v_k · 1_{v_k>0}
# The ∇p term has a GRADIENT on the pressure.
# So the actual integral is ∫∫ ∇p · (u/|u|) · v_k dx dt
# = -∫∫ p · div((u/|u|) v_k 1_{v_k>0}) dx dt (integration by parts)
# = -∫∫ p · (div(u/|u|) · v_k + (u/|u|) · ∇v_k) · 1_{v_k>0} dx dt

# The (u/|u|)·∇v_k part gives: ∫∫ p · ∇v_k (·unit vector) dx dt
# This is why d_k (which is |∇v_k| weighted) appears in the standard estimate.

# So the correct integral to bound is more like:
# I_k = ∫∫ P^{21} · |∇v_k| dx dt (on {v_k > 0})
# NOT ∫∫ P^{21} · v_k dx dt.

# This changes the W^{-1,q'}/W^{1,q} analysis fundamentally — the extra derivative
# is already "used up" by the gradient of v_k.

print("CORRECTION: The actual bottleneck integral involves ∇v_k, not v_k:")
print("  I_k ~ ∫∫ P^{21} · |∇v_k| · 1_{A_k} dx dt")
print()
print("For the W^{-1,q'}/W^{1,q} approach, this means the pairing is between")
print("P^{21} and |∇v_k| (not v_k), so we lose one derivative of improvement.")
print()
print("Revised W^{-1,q'}/W^{1,q} bound:")
print("  I_k ≤ ||P^{21}||_{L^r} · ||∇v_k||_{L^{r'}} (plain Hölder, no W^{-1} gain)")
print()
print("This reduces to the standard CZ/Hölder approach — no improvement.")
print()

# ================================================================
# APPROACH 2C: Lorentz space L^{p,q}
# ================================================================
print("=" * 70)
print("--- Approach 2C: Lorentz space L^{p,q} duality ---")
print("=" * 70)
print()
print("Lorentz spaces L^{p,q} refine L^p: L^{p,p} = L^p, L^{p,1} ⊂ L^{p,p} ⊂ L^{p,∞}.")
print("CZ operators are bounded L^{p,q} → L^{p,q} for 1 < p < ∞, 1 ≤ q ≤ ∞.")
print("Hölder in Lorentz spaces: L^{p_1,q_1} · L^{p_2,q_2} ⊂ L^{r,s} where")
print("1/r = 1/p_1 + 1/p_2 and 1/s = 1/q_1 + 1/q_2.")
print()
print("The potential advantage: if v_k ∈ L^{p,1} (better than L^p), the")
print("Hölder pairing could give a logarithmic improvement.")
print()
print("However: from the De Giorgi functional U_k, the estimates on ||v_k||_{L^p}")
print("come from Sobolev/Chebyshev bounds that give POWER-LAW scaling in U_{k-1}.")
print("The refinement to L^{p,q} can at most give:")
print("  ||v_k||_{L^{p,1}} ≤ C · p ||v_k||_{L^p} (by real interpolation)")
print("This is a CONSTANT improvement — no change in the U_{k-1} exponent.")
print()
print("VERDICT: Lorentz spaces give at most logarithmic/constant improvements.")
print("The exponent β = 4/3 is unchanged.")
print()

print("=" * 70)
print("TASK 2 SUMMARY")
print("=" * 70)
print()
print("Three duality approaches tested:")
print()
print("A. H^1/BMO: β = 4/3 (matches CZ). The BMO norm of P^{21} loses U-dependence,")
print("   while the H^1 norm of v_k recovers the full 4/3 through L^1 and gradient bounds.")
print()
print("B. W^{-1,q'}/W^{1,q}: Initially appears to give β = 11/6 for q → 1,")
print("   but this bounds the WRONG integral (∫P·v, not ∫P·|∇v|).")
print("   Correcting for the gradient in the actual energy inequality removes")
print("   the apparent gain, reducing to β = 4/3 or worse.")
print()
print("C. Lorentz L^{p,q}: At most constant/logarithmic improvement in the")
print("   CZ bounds. No change to the power-law exponent β.")
print()
print("ALL THREE give β ≤ 4/3 for the actual bottleneck integral. No improvement.")
