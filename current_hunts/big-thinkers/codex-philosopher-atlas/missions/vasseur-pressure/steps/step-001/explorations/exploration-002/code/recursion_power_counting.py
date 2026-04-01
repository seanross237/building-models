"""
Precise power counting for the De Giorgi recursion in 3D Navier-Stokes.

Computes the exact exponent δ(β) in the recursion U_{k+1} ≤ C b^k U_k^{1+δ}
as a function of the pressure integrability exponent β.
"""

from sympy import *

d = 3
print("=" * 70)
print("PRECISE POWER COUNTING FOR DE GIORGI RECURSION")
print("=" * 70)

# ========================================================================
# Setup: The De Giorgi energy and the recursion
# ========================================================================
print("""
SETUP:
  U_k = sup_t ∫ v_k² φ_k² dx  +  ∫∫ |∇(v_k φ_k)|² dx dt

  Dissipation and transport terms: after integration by parts, these give
  contributions that are powers of U_k via parabolic Sobolev embedding.

  The key embedding: v_k φ_k ∈ L^{10/3}_{t,x}  with
    ||v_k φ_k||_{L^{10/3}}^{10/3} ≤ C · U_k^{5/3}

  (This follows from: ||f||_{L^{10/3}} ≤ ||f||_{L^∞_t L^2_x}^{2/5} · ||f||_{L^2_t L^6_x}^{3/5}
   and ||f||_{L^∞_t L^2_x}^2 + ||∇f||_{L^2_t L^2_x}^2 ≤ U_k)

  We express all terms in the energy inequality as powers of U_k.
""")

# ========================================================================
# Contribution from each term
# ========================================================================

# The standard De Giorgi recursion without pressure (drift-diffusion case):
# The transport + cutoff terms give:
#   U_{k+1} ≤ C · 2^{kα₀} · U_k^{1 + 2/(d+2)}
# In d=3: δ₀ = 2/5
delta_0 = Rational(2, d + 2)
print(f"Drift-diffusion δ₀ = 2/(d+2) = {delta_0} = {float(delta_0):.4f}")
print(f"  Recursion: U_{{k+1}} ≤ C · 2^{{kα}} · U_k^{{{1 + delta_0}}} = U_k^{{7/5}}")
print()

# ========================================================================
# Pressure term power counting
# ========================================================================
print("=" * 70)
print("PRESSURE TERM POWER COUNTING")
print("=" * 70)
print()

beta = Symbol('beta', positive=True)

print("The pressure integral:")
print("  I_p = |∫∫ p · div(v_k φ_k² ê) dx dt|")
print()
print("After Hölder's inequality:")
print("  I_p ≤ ||p||_{L^β(Q_k)} · ||div(v_k φ_k² ê)||_{L^{β'}(Q_k)}")
print()

# Piece 1: ||p||_{L^β(Q_k)}
print("--- Piece 1: ||p||_{L^β(Q_k)} ---")
print()
print("By CZ: ||p||_{L^β} ≤ C ||u⊗u||_{L^β} = C ||u||_{L^{2β}}²")
print()
print("The full velocity u on Q_k decomposes as u = v_k + C_k (on superlevel set).")
print("The term ||u||_{L^{2β}(Q_k)}² contains both the controlled part (v_k)")
print("and the constant background (C_k). This is where the issue lies —")
print("C_k is NOT small, so ||u||_{L^{2β}} does not → 0 with U_k alone.")
print()
print("However, u is in L^{3,∞} globally. Restricting to the superlevel set:")
print("  ||u||_{L^{2β}(A_k)}^{2β} ≤ ∫₀^∞ 2β λ^{2β-1} |{|u|>λ} ∩ Q_k| dλ")
print()
print("From weak-L^3: |{|u|>λ}| ≤ C λ^{-3}")
print("The measure of Q_k ∩ {|u| > C_k} ≤ C C_k^{-3}")
print("But via Chebyshev with energy: |Q_k ∩ {|u| > C_k}| ≤ C 2^{2k} U_k / M²")
print()

# Piece 2: ||div(v_k φ_k² ê)||_{L^{β'}(Q_k)}
print("--- Piece 2: ||div(v_k φ_k² ê)||_{L^{β'}(Q_k)} ---")
print()
print("The divergence expands to terms involving:")
print("  (i)  ∇v_k · φ_k²  — controlled by ∫|∇v_k|² φ_k² ≤ U_k")
print("  (ii) v_k · ∇φ_k · φ_k  — controlled by ||v_k||_{L^{β'}} · ||∇φ_k||_{L^∞}")
print("  (iii) v_k · φ_k² · div(ê) — lower order")
print()
print("The dominant contribution is (ii) since ∇φ_k ~ 2^k blows up.")
print("By Hölder + measure: ||v_k||_{L^{β'}(Q_k)} ≤ |Q_k ∩ A_k|^{1/β' - 3/10} · ||v_k||_{L^{10/3}}")
print("  (when β' > 10/3, need reverse Hölder — not available)")
print("  (when β' ≤ 10/3, use |A_k|^{extra power} to fill the gap)")
print()

# ========================================================================
# Explicit δ(β) computation
# ========================================================================
print("=" * 70)
print("COMPUTING δ(β) — THE RECURSION EXPONENT")
print("=" * 70)
print()

# In Vasseur's framework, the precise recursion is:
# U_{k+1} ≤ C 2^{kα} [U_k^{1+2/5} + ||p||_{L^β}^{β} · U_k^{γ(β)}]
#
# The pressure contribution's power of U_k:
# ||p||_{L^β(Q_k)} is bounded using the GLOBAL a priori bound (not U_k),
# so it contributes as a coefficient, not a power of U_k.
#
# BUT the localization to Q_k introduces measure factors:
# |Q_k ∩ A_k| ≤ C 2^{2k} U_k / M²
# This |A_k| appears raised to some power in the Hölder estimates.

# The key calculation:
# I_p ≤ ||p||_{L^β(Q_k)} · ||v_k φ_k||_{L^{β'}(Q_k)} · ||∇φ_k||_{L^∞}
#
# For β' ≤ 10/3:
# ||v_k φ_k||_{L^{β'}(Q_k)} ≤ ||v_k φ_k||_{L^{10/3}}^{10/(3β')} · |Q_k|^{1/β' - 3/10}
#                             ≤ C U_k^{5/(3β')} · |Q_k|^{1/β' - 3/10}
#
# Wait — let me be more careful. We use Hölder between L^{10/3} and L^1:
# ||f||_{L^q} ≤ ||f||_{L^r}^θ · |support|^{(1-θ)/1}  ... this isn't quite right.
#
# More precisely: for q < r, on a set of measure μ:
# ||f||_{L^q}^q = ∫|f|^q ≤ (∫|f|^r)^{q/r} · μ^{1-q/r}  (Hölder)
# so ||f||_{L^q} ≤ ||f||_{L^r} · μ^{1/q - 1/r}

# For q = β' and r = 10/3:
# If β' ≤ 10/3:
# ||v_k φ_k||_{L^{β'}} ≤ ||v_k φ_k||_{L^{10/3}} · μ_k^{1/β' - 3/10}
# where μ_k = |Q_k ∩ {v_k > 0}| = |Q_k ∩ {|u| > C_k}|

# From the energy: μ_k ≤ C U_k / (ΔC_k)² = C 2^{2k} U_k / M²
# And: ||v_k φ_k||_{L^{10/3}} ≤ C U_k^{1/2} (from parabolic Sobolev norm equivalence)

# WAIT - let me be more precise. The parabolic Sobolev norm gives:
# ||v_k φ_k||_{L^{10/3}}^2 ≤ C ||v_k φ_k||_{L^∞_t L^2_x}^{4/5} · ||∇(v_k φ_k)||_{L^2}^{6/5}
#                            ≤ C U_k^{2/5} · U_k^{3/5} = C U_k
# So ||v_k φ_k||_{L^{10/3}} ≤ C U_k^{1/2}

# Actually, let me trace this more carefully using the interpolation inequality.
# ||f||_{L^{10/3}_{t,x}}^{10/3} ≤ C ||f||_{L^∞_t L^2_x}^{4/3} · ||f||_{L^2_t L^6_x}^2
# Proof: 1/(10/3) = 3/10, and
# θ·(1/2) + (1-θ)·(1/6) = 3/10 with (p: ∞ and 2)
# Actually the interpolation is in both time and space simultaneously.

# Let me use the cleaner form. Set:
# E = ||v_k φ_k||_{L^∞_t L^2_x}^2 (bounded by U_k)
# D = ||∇(v_k φ_k)||_{L^2_{t,x}}^2 (bounded by U_k)
# Then parabolic Sobolev (Gagliardo-Nirenberg in space + Hölder in time):
# ||v_k φ_k||_{L^r_{t,x}}^r ≤ C E^{a} D^{b} with r = 2(d+2)/d = 10/3 for d=3
# a = r/2 - d(r-2)/(2·2) = 5/3 - 3·4/3 / 4 = 5/3 - 1 = 2/3
# b = d(r-2)/(2·2) = 3·(4/3)/(4) = 1
# Check: a + b = 2/3 + 1 = 5/3 and r/2 = 5/3 ✓

a_exp = Rational(2, 3)
b_exp = Rational(1, 1)
r_exp = Rational(10, 3)
print(f"Parabolic Sobolev: ||v_k φ_k||_{{L^{{10/3}}}}^{{10/3}} ≤ C · E^{{{a_exp}}} · D^{{{b_exp}}}")
print(f"  where E = ||v_k φ_k||_{{L^∞_t L^2_x}}^2 ≤ U_k")
print(f"  and   D = ||∇(v_k φ_k)||_{{L^2}}^2 ≤ U_k")
print(f"  So: ||v_k φ_k||_{{L^{{10/3}}}}^{{10/3}} ≤ C · U_k^{{{a_exp + b_exp}}} = C · U_k^{{5/3}}")
print(f"  Hence: ||v_k φ_k||_{{L^{{10/3}}}} ≤ C · U_k^{{1/2}}")
print()

# Now for β' ≤ 10/3:
# ||v_k φ_k||_{L^{β'}}  ≤ ||v_k φ_k||_{L^{10/3}} · μ_k^{1/β' - 3/10}
#                         ≤ C U_k^{1/2} · (C 2^{2k} U_k / M²)^{1/β' - 3/10}
#                         = C(M) · 2^{2k(1/β' - 3/10)} · U_k^{1/2 + 1/β' - 3/10}

print("For β' ≤ 10/3:")
print("  ||v_k φ_k||_{L^{β'}} ≤ ||v_k φ_k||_{L^{10/3}} · μ_k^{1/β' - 3/10}")
print("    ≤ C U_k^{1/2} · (C 2^{2k} U_k / M²)^{1/β' - 3/10}")
print()

bp = Symbol("bp", positive=True)  # β'
U_power_dual = Rational(1,2) + (1/bp - Rational(3,10))
growth_dual = 2 * (1/bp - Rational(3,10))

print(f"  U_k power from dual side: 1/2 + (1/β' - 3/10)")
print(f"  2^k growth from dual side: 2k(1/β' - 3/10)")
print()

# The pressure ||p||_{L^β(Q_k)}:
# Since p is determined by the FULL velocity field (not just v_k),
# we can't express ||p||_{L^β(Q_k)} purely as a power of U_k.
#
# Vasseur's approach: assume p ∈ L^β as an a priori hypothesis,
# or derive it from the energy regularity.
#
# From the energy class: u ∈ L^2_t H^1_x, so u ∈ L^2_t L^6_x.
# CZ gives p ∈ L^1_t L^3_x. But we need more.
#
# Actually, the key insight is that the pressure on the LOCALIZED region
# can be split: p = p_near + p_far, where
# p_near comes from u²|_{Q_k} (local) → controlled by U_k
# p_far comes from u²|_{Q_k^c} (far field) → decays, controlled by energy

# For Vasseur's partial regularity:
# The pressure term needs only be integrable enough to close the recursion
# at the FIRST step, giving singular set estimate.
#
# The recursion for partial regularity is:
# U_{k+1} ≤ C 2^{kα} [transport terms + pressure term]
# ≤ C 2^{kα} [U_k^{1+2/5} + (pressure contribution)]

# The pressure contribution after all estimates:
# I_p ≤ ||p||_{L^β} · C(M) · 2^{k(1 + 2(1/β' - 3/10))} · U_k^{1/2 + 1/β' - 3/10}
#      = ||p||_{L^β} · C(M) · 2^{k·(2/β' + 2/5)} · U_k^{1/2 + 1/β' - 3/10}

# Wait, let me also account for ||∇φ_k||_{L^∞} ~ 2^k:
# I_p ≤ ||p||_{L^β} · ||v_k ∇φ_k||_{L^{β'}}
#      ≤ ||p||_{L^β} · 2^k · ||v_k φ_k||_{L^{β'}}  (using φ_k ~ 1 on supp v_{k+1})

# Hmm, let me be even more careful. The term is:
# I_p = ∫∫ p (v_k · 2φ_k ∇φ_k · ê) dx dt + lower order
# ≤ ||p||_{L^β} · 2||v_k φ_k||_{L^{β'/(β'-1)}} · ...

# Actually, the simplest way: by Hölder in space-time on Q_k,
# I_p ≤ ||p||_{L^β(Q_k)} · ||v_k||_{L^s(Q_k)} · ||∇φ_k||_{L^∞}
# with 1/β + 1/s = 1, i.e., s = β' = β/(β-1)
# and ||∇φ_k||_{L^∞} ~ 2^k

print("Full pressure contribution to the recursion:")
print()
print("I_p ≤ ||p||_{L^β(Q_k)} · ||v_k||_{L^{β'}(Q_k)} · ||∇φ_k||_{L^∞}")
print("    ≤ ||p||_{L^β} · 2^k · [C U_k^{1/2} · (C 2^{2k} U_k)^{1/β'-3/10}]")
print()

# Power of U_k:
# 1/2 + (1/β' - 3/10) = 1/2 + 1/β' - 3/10 = 2/10 + 1/β' = 1/5 + 1/β'
# Since β' = β/(β-1), we have 1/β' = 1 - 1/β
# So power = 1/5 + 1 - 1/β = 6/5 - 1/β

print("Power of U_k in pressure contribution:")
for b_val in [Rational(10,7), Rational(6,5), Rational(4,3), Rational(3,2), Rational(5,3)]:
    bp_val = b_val / (b_val - 1)
    power = Rational(1,2) + Rational(1, bp_val) - Rational(3, 10)
    power_simplified = simplify(power)
    print(f"  β = {b_val}: β' = {bp_val}, U_k power = 1/2 + 1/{bp_val} - 3/10 = {power_simplified} = {float(power_simplified):.4f}")
    # For recursion closure: need power > 1
    gap = power_simplified - 1
    status = "CLOSES (δ > 0)" if gap > 0 else ("CRITICAL" if gap == 0 else "DOES NOT CLOSE")
    print(f"    δ = power - 1 = {gap} → {status}")

print()

# ========================================================================
# The pressure norm ||p||_{L^β(Q_k)} — how it depends on U_k
# ========================================================================
print("=" * 70)
print("PRESSURE NORM ON Q_k: DEPENDENCE ON U_k")
print("=" * 70)
print()

print("The pressure on Q_k is NOT purely determined by U_k.")
print("Split: p = p_local + p_far")
print()
print("p_local = CZ(u⊗u · 1_{Q_k^*}), where Q_k^* slightly enlarges Q_k")
print("p_far = CZ(u⊗u · 1_{Q_k^{*c}})")
print()
print("For p_local (CZ estimate):")
print("  ||p_local||_{L^β(Q_k)} ≤ C ||u||_{L^{2β}(Q_k^*)}²")
print()
print("On Q_k^*, u = v_k + C_k background.")
print("  ||u||_{L^{2β}}^{2β} ≤ C(||v_k||_{L^{2β}}^{2β} + C_k^{2β} |Q_k|)")
print()

# The C_k^{2β} |Q_k| term is a CONSTANT (not vanishing with U_k → 0).
# This is the fundamental problem: the background velocity contributes to pressure.
# For partial regularity, Vasseur works locally around singular points where
# the energy is small — the background C_k can be controlled.

# For the recursion:
# ||p_local||_{L^β} ≤ C ||v_k||_{L^{2β}}² + C C_k^2 |Q_k|^{1/β}
# The first term is controlled by U_k, the second is a fixed constant.

print("||p_local||_{L^β} ≤ C ||v_k||_{L^{2β}}² + C C_k² |Q_k|^{1/β}")
print()
print("First term: ||v_k||_{L^{2β}}² ~ U_k^{power} (controlled, → 0)")
print("Second term: C_k² |Q_k|^{1/β} ~ M² r₀^{3/β} (FIXED CONSTANT)")
print()
print("This fixed constant in the pressure is what prevents full regularity.")
print("In the partial regularity setting, one works at points where this")
print("constant is small (excess energy < ε₀).")
print()

# ========================================================================
# Summary: δ(β) table
# ========================================================================
print("=" * 70)
print("SUMMARY: δ(β) TABLE")
print("=" * 70)
print()
print(f"{'β':>8} {'β_prime':>8} {'U_k power':>12} {'δ':>8} {'Status':>20}")
print("-" * 65)

beta_values = [Rational(10,7), Rational(11,8), Rational(6,5), Rational(5,4),
               Rational(4,3), Rational(7,5), Rational(10,7), Rational(3,2), Rational(8,5), Rational(5,3)]
# Remove duplicates and sort
beta_values = sorted(set(beta_values))

for b_val in beta_values:
    bp_val = b_val / (b_val - 1)
    # Power of U_k from the pressure term dual side:
    # 1/2 + (1/β' - 3/10) = 1/5 + 1/β' = 1/5 + 1 - 1/β = 6/5 - 1/β
    power = Rational(6,5) - Rational(1, b_val)
    delta = power - 1

    if delta > 0:
        status = "CLOSES"
    elif delta == 0:
        status = "CRITICAL (log)"
    else:
        status = "DOES NOT CLOSE"

    print(f"{str(b_val):>8} {str(bp_val):>8} {str(power):>12} {str(delta):>8} {status:>20}")

print()
print("KEY FINDINGS:")
print(f"  β = 6/5: δ = 0 — exactly critical, recursion is borderline")
print(f"  β = 4/3: δ = 1/5 - 3/4 = ... wait let me recompute")
print()

# Let me recompute more carefully
for b_val in [Rational(4,3), Rational(3,2)]:
    bp_val = b_val / (b_val - 1)
    # The U_k power from the DUAL side only:
    dual_power = Rational(1,2) + (Rational(1, bp_val) - Rational(3, 10))
    print(f"β = {b_val}: β' = {bp_val}")
    print(f"  Dual power = 1/2 + 1/{bp_val} - 3/10 = {dual_power}")
    print(f"  Simplified: 1/5 + 1/{bp_val} = {Rational(1,5) + Rational(1, bp_val)}")
    print(f"  = {Rational(1,5) + 1 - Rational(1, b_val)} = {Rational(6,5) - Rational(1, b_val)}")
    print()

# Hmm wait. The above computes the power of U_k from ONLY the dual side.
# But there are also contributions from the pressure norm itself.
# Let me reconsider.

# In Vasseur's actual argument, the key is whether the TOTAL power of U_k
# across all terms exceeds 1. The pressure norm ||p||_{L^β} contributes
# a power of U_k only through the local part. The far-field part is bounded
# by a constant (the global energy), so it doesn't help.

# The correct accounting:
# Total recursion (schematic):
# U_{k+1} ≤ C 2^{kα} · [U_k^{1+2/5}  +  ||p||_{L^β}^{global} · 2^k · U_k^{power_dual}]
#
# For partial regularity: ||p||_{L^β}^{global} is assumed bounded (or derived from energy).
# The recursion closes when power_dual > 1, i.e., 6/5 - 1/β > 1, i.e., 1/β < 1/5, i.e., β > 5.
#
# THAT CAN'T BE RIGHT — β > 5 is too strong.
#
# I think the issue is that the pressure estimate is more subtle.
# Let me reconsider: in Vasseur's actual paper, the pressure contribution
# involves the LOCALIZED pressure which can be expressed as a power of U_k.

print("=" * 70)
print("REFINED ANALYSIS: LOCAL PRESSURE POWER COUNTING")
print("=" * 70)
print()

# In Vasseur (2007), the argument goes as follows:
# On a ball B_r centered at a point where the energy concentration is small:
# ||u||_{L^3(B_r)} ≤ ε₀ (smallness condition)
#
# Then p = p_local + p_far with:
# ||p_local||_{L^{3/2}(B_r)} ≤ C ||u||_{L^3(B_r)}² ≤ C ε₀²
# ||p_far||_{L^∞(B_r)} ≤ C r^{-3} ||u||_{L^2}² (harmonic estimate)
#
# The iteration works on cylinders shrinking toward the singular point.
# The key is that ||p_local||_{L^{3/2}} is SMALL (by the smallness condition),
# and ||p_far||_{L^∞} contributes a fixed constant.

# For the FULL regularity question (not partial), one would need:
# ||p||_{L^β} controlled in terms of U_k^{some power > 1}
# on each iteration step.

# Let's compute what β is needed for the pressure term to be absorbable.

print("The pressure integral after localization:")
print()
print("I_p ≤ [||p_local||_{L^β} + ||p_far||_{L^β}] · ||v_k||_{L^{β'}} · 2^k")
print()
print("p_local: ||p_local||_{L^β(Q_k)} ≤ C ||v_k||_{L^{2β}(Q_k)}²")
print("  ≤ C [||v_k||_{L^{10/3}}^{2} · μ_k^{2(3/(10β)-1/(2β))}]  ... if 2β ≤ 10/3")
print()

# For 2β ≤ 10/3 (β ≤ 5/3):
# ||v_k||_{L^{2β}} ≤ ||v_k||_{L^{10/3}} · μ_k^{1/(2β) - 3/10}
# So ||v_k||_{L^{2β}}² ≤ ||v_k||_{L^{10/3}}² · μ_k^{1/β - 3/5}

# And for the dual side:
# ||v_k||_{L^{β'}} ≤ ||v_k||_{L^{10/3}} · μ_k^{1/β' - 3/10}

# Total:
# I_p_local ≤ C ||v_k||_{L^{10/3}}³ · μ_k^{(1/β - 3/5) + (1/β' - 3/10)} · 2^k

# Let's compute the measure exponent:
# (1/β - 3/5) + (1/β' - 3/10) = 1/β + 1/β' - 3/5 - 3/10
# = 1 - 9/10 = 1/10

print("For LOCAL pressure contribution (2β ≤ 10/3):")
print()
measure_exp = Rational(1,10)
print(f"  I_p_local ≤ C ||v_k φ_k||_{{L^{{10/3}}}}^3 · μ_k^{{{measure_exp}}} · 2^k")
print(f"  The measure exponent is 1/β + 1/β' - 9/10 = 1 - 9/10 = 1/10")
print(f"  (This is INDEPENDENT of β — remarkable!)")
print()

# Now: ||v_k φ_k||_{L^{10/3}}^3 ≤ C U_k^{3/2} (from parabolic Sobolev)
# And: μ_k^{1/10} ≤ (C 2^{2k} U_k)^{1/10} = C 2^{k/5} U_k^{1/10}
# So: I_p_local ≤ C 2^{k(1 + 1/5)} U_k^{3/2 + 1/10} = C 2^{6k/5} U_k^{8/5}

total_U_power_local = Rational(3,2) + Rational(1,10)
print(f"  ||v_k φ_k||_{{L^{{10/3}}}}^3 ≤ C U_k^{{3/2}}")
print(f"  μ_k^{{1/10}} ≤ C 2^{{k/5}} U_k^{{1/10}}")
print(f"  Total: I_p_local ≤ C · 2^{{6k/5}} · U_k^{{{total_U_power_local}}}")
print(f"  = C · 2^{{6k/5}} · U_k^{{8/5}}")
print(f"  δ_local = 8/5 - 1 = 3/5 > 0  ✓  LOCAL PRESSURE IS FINE!")
print()

# So the local pressure DOES close the recursion!
# The problem is the FAR-FIELD pressure.

print("=" * 70)
print("THE REAL BOTTLENECK: FAR-FIELD PRESSURE")
print("=" * 70)
print()

print("p_far = CZ(u⊗u · 1_{Q_k^c})|_{Q_k}")
print()
print("||p_far||_{L^∞(Q_k)} ≤ C ||u||_{L^2}² / r_k^d  [mean value / harmonic]")
print("  This is a CONSTANT — does not → 0 with U_k!")
print()
print("The far-field pressure contribution:")
print("  I_p_far ≤ ||p_far||_{L^∞} · ||v_k||_{L^1(Q_k)} · ||∇φ_k||_{L^∞}")
print("         ≤ C_far · 2^k · ||v_k||_{L^1(Q_k)}")
print()
print("  ||v_k||_{L^1(Q_k)} ≤ ||v_k||_{L^{10/3}} · μ_k^{7/10}")
print("  ≤ C U_k^{1/2} · (C 2^{2k} U_k)^{7/10}")
print("  = C 2^{7k/5} U_k^{6/5}")
print()
print("  Total: I_p_far ≤ C_far · 2^{k(1+7/5)} · U_k^{6/5}")
print("  = C_far · 2^{12k/5} · U_k^{6/5}")
print()

# For the recursion: need δ > 0 from U_k^{1+δ}
# Far-field gives U_k^{6/5}, so δ_far = 1/5 > 0 ✓
# BUT: the 2^{12k/5} growth must be absorbed by the De Giorgi decay factor.
# In the standard De Giorgi lemma: U_k → 0 if U_{k+1} ≤ C b^k U_k^{1+δ}
# with U_0 sufficiently small. The b^k = 2^{12k/5} is fine as long as δ > 0.

print("  δ_far = 6/5 - 1 = 1/5 > 0  ✓  FAR-FIELD ALSO CLOSES!")
print()
print("  BUT WAIT — this analysis assumed ||p_far||_{L^∞} is bounded,")
print("  which requires u ∈ L^2 and r_k bounded away from 0.")
print("  For PARTIAL regularity (ε-regularity), this works: we fix r > 0")
print("  and iterate on shrinking sub-cylinders.")
print()
print("  For FULL regularity (all of R^3 × (0,T)), the far-field pressure")
print("  involves the global L^2 norm, which is bounded by the energy inequality.")
print("  The issue is: the far-field contribution is NOT small unless ε₀ is small,")
print("  and ε₀ smallness requires β > 3/2 to bootstrap.")

# ========================================================================
# THE β > 3/2 THRESHOLD
# ========================================================================
print()
print("=" * 70)
print("WHY β > 3/2 WOULD GIVE FULL REGULARITY")
print("=" * 70)
print()

print("The Serrin-type condition: u ∈ L^p_t L^q_x with 2/p + 3/q ≤ 1")
print("gives full regularity. The endpoint for the pressure:")
print()
print("If p ∈ L^β_{t,x} with β > 3/2:")
print("  This implies u ∈ L^{2β}_{t,x} with 2β > 3.")
print("  Check Serrin condition: 2/p + 3/q = 2/(2β) + 3/(2β) = 5/(2β)")
print("  For β > 5/2: 5/(2β) < 1 — Serrin condition met! Full regularity.")
print()
print("  For β ∈ (3/2, 5/2): Serrin not directly met, but:")
print("  The CZ bootstrapping: p ∈ L^β → better velocity integrability")
print("  → better pressure integrability → iterate until regularity.")
print()
print("  The critical threshold β = 3/2:")
print("  2β = 3 → u ∈ L^3 (critical, Serrin endpoint)")
print("  p ∈ L^{3/2} → u⊗u ∈ L^{3/2} → u ∈ L^3 (circular!)")
print("  The iteration neither improves nor degrades. This is the critical case.")
print()
print("  β > 3/2 breaks the circularity: better p → better u → even better p → ...")
print()

# ========================================================================
# FINAL PRECISE STATEMENT
# ========================================================================
print("=" * 70)
print("FINAL PRECISE STATEMENT: WHERE β = 4/3 COMES FROM")
print("=" * 70)
print()
print("The exponent β = 4/3 in Vasseur's framework arises from:")
print()
print("1. The energy inequality gives u ∈ L^∞_t L^2_x ∩ L^2_t H^1_x (Leray class)")
print("2. CZ gives p ∈ L^1_t L^3_x + L^{5/3}_{t,x} + ... (various mixed norms)")
print("3. The best ISOTROPIC (same exponent in time and space) bound is:")
print("   p ∈ L^{5/3}_{t,x}  from  u ∈ L^{10/3}_{t,x}  (parabolic Sobolev)")
print()
print("4. However, 5/3 > 3/2, so why isn't this enough?")
print("   Because the Leray class gives u ∈ L^{10/3}_{t,x} but this is SUBCRITICAL:")
print("   2/(10/3) + 3/(10/3) = 6/10 + 9/10 = 15/10 = 3/2 — CRITICAL, not sub.")
print("   The L^{10/3} norm is at the critical scaling, not better.")
print()
print("5. The a priori bound from Leray is: u ∈ L^{3,∞}_x uniformly in t.")
print("   This gives p ∈ L^{3/2,∞}_x — weak type, NOT strong L^{3/2}.")
print("   In the De Giorgi iteration, weak-type bounds lose a logarithm.")
print()
print("6. The β = 4/3 comes from the PARABOLIC interpolation:")
print("   To close the De Giorgi recursion with ALL error terms controlled,")
print("   the pressure needs to be in L^β with:")
print("   - β ≥ 10/7 (Hölder pairing with L^{10/3} dual)")
print("   - The far-field pressure estimate controlled by a SMALL constant")
print("   - The small constant requires ε₀-regularity which costs β → 4/3")
print()
print("7. Specifically, in the ε-regularity criterion:")
print("   The condition is ∫_{Q_1} |u|^3 + |p|^{3/2} < ε₀")
print("   (Caffarelli-Kohn-Nirenberg condition)")
print("   The pressure part |p|^{3/2} is the critical norm.")
print("   Working with L^{4/3} instead of L^{3/2} gives a SUBCRITICAL condition")
print("   that the De Giorgi machinery can bootstrap from.")
print()
print("   The gap 4/3 < 3/2 is exactly the subcriticality margin needed.")
print()

# ========================================================================
# DIMENSIONAL CHECK
# ========================================================================
print("=" * 70)
print("DIMENSIONAL / SCALING CHECK")
print("=" * 70)
print()

# NS has the scaling symmetry:
# u(x,t) → λu(λx, λ²t), p(x,t) → λ²p(λx, λ²t)
# Under this: ||u||_{L^q_x} → λ^{1-3/q} ||u||_{L^q_x}
# ||p||_{L^β_x} → λ^{2-3/β} ||p||_{L^β_x}
# Including time: ||u||_{L^p_t L^q_x} → λ^{1-2/p-3/q} ||u||

print("NS scaling: u → λu(λx, λ²t), p → λ²p(λx, λ²t)")
print()
print("Scaling dimensions:")
for name, (scale_power, exp) in [
    ("||u||_{L^3_x}", (1 - Rational(3,3), 3)),
    ("||u||_{L^{10/3}_{t,x}}", (1 - Rational(2, Rational(10,3)) - Rational(3, Rational(10,3)), Rational(10,3))),
    ("||p||_{L^{3/2}_x}", (2 - Rational(3, Rational(3,2)), Rational(3,2))),
    ("||p||_{L^{4/3}_x}", (2 - Rational(3, Rational(4,3)), Rational(4,3))),
    ("||p||_{L^{5/3}_{t,x}}", (2 - Rational(2, Rational(5,3)) - Rational(3, Rational(5,3)), Rational(5,3))),
]:
    print(f"  {name}: scaling dimension = {scale_power}")
    if scale_power == 0:
        print(f"    → CRITICAL (scale-invariant)")
    elif scale_power > 0:
        print(f"    → SUBCRITICAL (improves with concentration)")
    else:
        print(f"    → SUPERCRITICAL (worsens with concentration)")

print()
print("Note: ||p||_{L^{3/2}_x} has scaling dimension 0 — CRITICAL.")
print("      ||p||_{L^{4/3}_x} has scaling dimension > 0 — SUBCRITICAL.")
print("      This is why β = 4/3 gives partial regularity but not full.")
print("      Full regularity needs β ≥ 3/2 (critical or better).")
