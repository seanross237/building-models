"""
Task 3: Commutator with Test Function Variant

After integration by parts:
  I_k = ∫∫ u_i^{below} · u_j^{above} · R_iR_j(v_k · 1_{v_k>0}) dx dt

Write this as:
  I_k = ∫∫ u_j^{above} · [R_iR_j, u_i^{below}](v_k) dx dt
      + ∫∫ u_j^{above} · u_i^{below} · R_iR_j(v_k) dx dt

The commutator [R_iR_j, u_i^{below}] gains regularity by CRW theorem
if u^{below} ∈ BMO.

E004 checked CRW with CZ on the product side. Does moving CZ to the
test function side change the analysis?
"""

from sympy import *

print("=" * 70)
print("TASK 3: COMMUTATOR WITH TEST FUNCTION VARIANT")
print("=" * 70)

print("""
Starting point (after IBP from Task 1):
  I_k = ∫∫ (u_i^{below} · u_j^{above}) · R_iR_j(v_k) dx dt

Rewrite using commutator:
  u_i^{below} · R_iR_j(v_k) = R_iR_j(u_i^{below} · v_k) - [R_iR_j, u_i^{below}](v_k)

Wait — that's [R_iR_j, M_{u_i^{below}}] where M_f is multiplication by f.
  [R_iR_j, M_f](g) = R_iR_j(fg) - f · R_iR_j(g)

So:
  ∫ u_i^{below} · u_j^{above} · R_iR_j(v_k) dx
  = ∫ u_j^{above} · [u_i^{below} · R_iR_j(v_k)] dx
  = ∫ u_j^{above} · [R_iR_j(u_i^{below} · v_k) - [R_iR_j, u_i^{below}](v_k)] dx

The commutator term: ∫ u_j^{above} · [R_iR_j, u_i^{below}](v_k) dx

By CRW (Coifman-Rochberg-Weiss, 1976):
  ||[R_iR_j, M_f](g)||_{L^p} ≤ C ||f||_{BMO} ||g||_{L^p}  for 1 < p < ∞.

This gives:
  ||[R_iR_j, u_i^{below}](v_k)||_{L^p} ≤ C ||u^{below}||_{BMO} ||v_k||_{L^p}

Since u^{below} ∈ L^∞: ||u^{below}||_{BMO} ≤ 2||u^{below}||_{L^∞} ≤ C.
""")

print("=" * 50)
print("COMMUTATOR TERM ANALYSIS")
print("=" * 50)
print()
print("Commutator piece:")
print("  C_k = ∫∫ u_j^{above} · [R_iR_j, u_i^{below}](v_k) dx dt")
print()
print("By Hölder:")
print("  |C_k| ≤ ||u^{above}||_{L^q} · ||[R_iR_j, u^{below}](v_k)||_{L^{q'}}")
print("       ≤ ||v_{k-1}||_{L^q} · C ||u^{below}||_{BMO} · ||v_k||_{L^{q'}}")
print("       ≤ C^k · U_{k-1}^{α(q)} · C · U_{k-1}^{α(q')}")
print()
print("with 1/q + 1/q' = 1.")
print()
print("This is IDENTICAL to the direct estimate from Task 1!")
print("||u^{below}||_{BMO} ≤ C gives no improvement — the CRW bound")
print("for bounded multipliers reduces to the trivial CZ bound.")
print()

# The non-commutator term
print("=" * 50)
print("NON-COMMUTATOR (REMAINDER) TERM")
print("=" * 50)
print()
print("Remainder piece:")
print("  R_k = ∫∫ u_j^{above} · R_iR_j(u_i^{below} · v_k) dx dt")
print()
print("This is the product u_i^{below} · v_k inside R_iR_j.")
print()
print("u_i^{below} · v_k: this product has the structure")
print("  (capped velocity) × (excess above level k)")
print("Both are functions of u, but v_k is supported on {|u| > λ_k}")
print("while u^{below} = u · min(1, λ_{k-1}/|u|).")
print()
print("On {|u| > λ_k}: u^{below} = λ_{k-1} · u/|u| (the cap)")
print("So u_i^{below} · v_k = λ_{k-1} · (u_i/|u|) · v_k on the support of v_k.")
print("Since λ_{k-1} ~ 1 and |u_i/|u|| ≤ 1:")
print("  ||u^{below} · v_k||_{L^p} ≤ C · ||v_k||_{L^p}")
print()
print("Then R_k ≤ ||v_{k-1}||_{L^q} · C ||v_k||_{L^{q'}} = same as before.")
print()

print("=" * 50)
print("KEY INSIGHT FROM E004")
print("=" * 50)
print()
print("E004 already showed that for BOUNDED multipliers (||u^{below}||_{BMO} ≤ C·||u^{below}||_{L^∞}):")
print("  CRW commutator bounds give NO improvement over direct CZ.")
print()
print("The reason: CRW gains are measured in the BMO norm of the multiplier.")
print("When the multiplier is L^∞-bounded, its BMO norm is O(||f||_{L^∞}) — no better.")
print("The commutator improvement only helps when the multiplier has small BMO norm")
print("but large L^∞ norm (i.e., oscillatory functions).")
print()
print("u^{below} = u · min(1, λ/|u|) has ||u^{below}||_{L^∞} ≤ λ ~ 1.")
print("Its BMO norm is at best O(1). No room for improvement.")
print()

print("=" * 50)
print("DOES MOVING CZ TO THE OTHER SIDE CHANGE ANYTHING?")
print("=" * 50)
print()
print("In the standard approach (E004):")
print("  P^{21} = R_iR_j(u^{below} · u^{above})")
print("  [R_iR_j, u^{below}](u^{above}) = R_iR_j(u^{below} · u^{above}) - u^{below} · R_iR_j(u^{above})")
print("  The commutator acts on u^{above} = v_{k-1} · (u/|u|)")
print()
print("In the IBP approach (this task):")
print("  I_k = ∫ (u^{below} · u^{above}) · R_iR_j(v_k) dx")
print("  [R_iR_j, u^{below}](v_k) = R_iR_j(u^{below} · v_k) - u^{below} · R_iR_j(v_k)")
print("  The commutator acts on v_k")
print()
print("DIFFERENCE: The commutator now acts on v_k (level k) instead of u^{above} (level k-1).")
print("But the CRW bound depends on:")
print("  ||[T, M_f](g)||_{L^p} ≤ C ||f||_{BMO} ||g||_{L^p}")
print("The bound on ||g||_{L^p} is the SAME for v_k and u^{above}_{k-1} = v_{k-1}·(u/|u|):")
print("  ||v_k||_{L^p} ≤ ||v_{k-1}||_{L^p}  (since v_k ≤ v_{k-1} pointwise)")
print("  ||u^{above}_{k-1}||_{L^p} = ||v_{k-1}||_{L^p}")
print()
print("So the commutator acts on a SMALLER function (v_k ≤ v_{k-1}),")
print("but this doesn't help because the Hölder pairing is with u^{above}_{k-1}")
print("(or v_{k-1}), which has the SAME bounds as before.")
print()
print("NET EFFECT: Moving CZ to the test function side does NOT change the")
print("commutator analysis. The exponent remains the same.")
print()

print("=" * 50)
print("HIGHER-ORDER COMMUTATOR POSSIBILITY")
print("=" * 50)
print()
print("One might try iterated commutators:")
print("  [R_iR_j, [R_kR_l, M_f]](g) — double commutator")
print("This could gain extra regularity: ~||f||_{BMO}^2 instead of ||f||_{BMO}.")
print("But the structure of P^{21} doesn't support this — there's only one")
print("CZ operator (R_iR_j), so we can form at most one commutator.")
print()
print("Alternatively, write P^{21} = R_iR_j(f_{ij}) where f_{ij} = u_i^{below} · u_j^{above}.")
print("The tensor structure: summing over i,j. Could we exploit cancellations")
print("between the (i,j) components?")
print()
print("For the commutator: Σ_{i,j} [R_iR_j, u_i^{below}](v_k) · u_j^{above}")
print("The sum over i involves: Σ_i u_i^{below} · R_i(...) — this is u^{below} · R(...)")
print("(dot product of vector with Riesz transform vector).")
print("div(u^{below}) appears if we can extract ∂_i from R_i.")
print("But R_i = ∂_i(-Δ)^{-1/2}, not ∂_i(-Δ)^{-1}.")
print()
print("No additional cancellation from the tensor structure.")
print()

print("=" * 70)
print("TASK 3 SUMMARY")
print("=" * 70)
print()
print("The commutator variant on the test-function side gives:")
print("  I_k = (commutator term) + (remainder term)")
print()
print("Both terms give the same bound as the direct estimate (Task 1): β = 1.")
print()
print("CRW commutator bounds for bounded multipliers (||u^{below}||_{BMO} ≤ C)")
print("provide no improvement, regardless of which side of the pairing the CZ")
print("operator acts on. This is consistent with E004's finding.")
print()
print("Moving CZ from the product side (standard) to the test-function side")
print("(IBP) does NOT change the commutator analysis because:")
print("1. The multiplier u^{below} has the same BMO norm on both sides")
print("2. The function being commutated (v_k vs u^{above}) has comparable L^p bounds")
print("3. The Hölder pairing exponents are identical")
print()
print("VERDICT: Commutator variant gives β ≤ 1 (direct) or β = 4/3 (via CZ on product).")
print("No improvement beyond standard CZ.")
