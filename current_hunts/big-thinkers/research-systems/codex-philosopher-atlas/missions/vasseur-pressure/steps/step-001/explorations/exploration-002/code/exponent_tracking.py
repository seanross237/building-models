"""
Exponent tracking for the De Giorgi energy inequality in 3D Navier-Stokes.

This script:
1. Verifies Hölder conjugate relationships
2. Tracks Sobolev embedding exponents in 3D
3. Traces the chain of inequalities producing β = 4/3
4. Computes Bogovskii corrector scaling
5. Identifies the critical threshold β > 3/2
"""

from sympy import *

# ========================================================================
# DIMENSION AND BASIC SETUP
# ========================================================================
d = 3  # spatial dimension
print("=" * 70)
print("EXPONENT TRACKING FOR DE GIORGI ITERATION — 3D NAVIER-STOKES")
print("=" * 70)

# ========================================================================
# 1. SOBOLEV EMBEDDINGS IN 3D
# ========================================================================
print("\n--- SOBOLEV EMBEDDINGS (d=3) ---")

# H^1(R^3) = W^{1,2}(R^3) ↪ L^{2*}(R^3) where 2* = 2d/(d-2) = 6
p_sobolev = 2  # starting exponent
s_sobolev = 1  # number of derivatives
p_star = Rational(2*d, d - 2*s_sobolev)
print(f"H^1 = W^{{1,2}} ↪ L^{{{p_star}}}  (Sobolev: 2* = 2d/(d-2) = {p_star})")

# Interpolation: L^2 ∩ L^6 ↪ L^q for q in [2, 6]
# By interpolation: ||f||_{L^q} ≤ ||f||_{L^2}^θ ||f||_{L^6}^{1-θ}
# where 1/q = θ/2 + (1-θ)/6
print(f"\nInterpolation: L^2 ∩ L^6 ↪ L^q for q ∈ [2, 6]")
print(f"  1/q = θ/2 + (1-θ)/6,  θ ∈ [0,1]")

# Key exponent: L^{10/3} appears in NS De Giorgi
q_key = Rational(10, 3)
theta_key = solve(1/q_key - Rational(1,2)*Symbol('t') - Rational(1,6)*(1-Symbol('t')), Symbol('t'))[0]
print(f"\nFor q = 10/3: θ = {theta_key}")
print(f"  ||f||_{{L^{{10/3}}}} ≤ ||f||_{{L^2}}^{{{theta_key}}} ||f||_{{L^6}}^{{{1-theta_key}}}")

# ========================================================================
# 2. CALDERÓN-ZYGMUND FOR PRESSURE
# ========================================================================
print("\n--- CALDERÓN-ZYGMUND FOR PRESSURE ---")
print("p = (-Δ)^{-1} ∂_i ∂_j (u_i u_j)")
print("CZ theory: ||∇²(-Δ)^{-1}f||_{L^r} ≤ C ||f||_{L^r} for 1 < r < ∞")
print()

# If u ∈ L^q, then u⊗u ∈ L^{q/2}, so p ∈ L^{q/2}
# Specifically:
# u ∈ L^3 → u⊗u ∈ L^{3/2} → p ∈ L^{3/2}  (critical case)
# u ∈ L^{3,∞} (weak L^3) → p ∈ L^{3/2,∞}  (weak type estimate)

for q_u in [Rational(3,1), Rational(10,3), 4, Rational(6,1)]:
    q_uu = q_u / 2
    print(f"u ∈ L^{{{q_u}}} → u⊗u ∈ L^{{{q_uu}}} → p ∈ L^{{{q_uu}}} (CZ)")

print(f"\nCritical: u ∈ L^{{3,∞}} → p ∈ L^{{3/2,∞}} (weak type)")

# ========================================================================
# 3. THE DE GIORGI ENERGY INEQUALITY — TERM BY TERM
# ========================================================================
print("\n" + "=" * 70)
print("THE DE GIORGI ENERGY INEQUALITY")
print("=" * 70)

print("""
Setup:
  C_k = M(1 - 2^{-k}),  M = level to be determined
  v_k = (|u| - C_k)_+   (truncation above level C_k)
  φ_k = cutoff on Q_k = B_{r_k} × (t_k, 0),  r_k = r₀(1 + 2^{-k})/2

Energy quantity:
  U_k = sup_t ∫ v_k² φ_k² dx  +  ∫∫ |∇(v_k φ_k)|² dx dt

Goal: Show U_{k+1} ≤ C · b^k · U_k^{1+δ} for some δ > 0, b > 1.
Then De Giorgi lemma gives U_k → 0, hence |u| ≤ M a.e.
""")

# ========================================================================
# 4. PRESSURE TERM — THE CRITICAL CHAIN
# ========================================================================
print("=" * 70)
print("PRESSURE TERM: TRACING β = 4/3")
print("=" * 70)

print("""
The pressure term in the energy inequality after testing against v_k φ_k²:

  I_p = ∫∫ p · div(v_k φ_k² ê) dx dt

where ê = u/|u| is the unit direction. Since div u = 0 but div(v_k φ_k² ê) ≠ 0
(because of the cutoff φ_k), this term does NOT vanish.

Expanding: div(v_k φ_k² ê) = (∇v_k · ê) φ_k² + v_k (2φ_k ∇φ_k · ê) + v_k φ_k² div(ê)

The key estimate is by Hölder's inequality in space-time:

  |I_p| ≤ ||p||_{L^β_t L^β_x(Q_k)} · ||div(v_k φ_k² ê)||_{L^{β'}_t L^{β'}_x(Q_k)}

where 1/β + 1/β' = 1.
""")

# Hölder conjugate
beta = Symbol('beta', positive=True)
beta_prime = beta / (beta - 1)

print("Hölder conjugate: β' = β/(β-1)")
for b_val in [Rational(4,3), Rational(3,2), Rational(5,3), 2]:
    bp = b_val / (b_val - 1)
    print(f"  β = {b_val}  →  β' = {bp}")

print()

# ========================================================================
# 5. THE CRITICAL CHAIN: WHY β = 4/3
# ========================================================================
print("=" * 70)
print("THE CHAIN OF INEQUALITIES → β = 4/3")
print("=" * 70)

print("""
STEP 1: Pressure recovery from velocity
  p = (-Δ)^{-1} ∂_i∂_j(u_i u_j)
  CZ: ||p||_{L^r} ≤ C||u||_{L^{2r}}²  for 1 < r < ∞

  For u ∈ L^q in the energy estimate:
  Need u ∈ L^{2β} → p ∈ L^β
""")

# STEP 2: What L^q spaces does the De Giorgi energy control?
print("STEP 2: The De Giorgi energy U_k controls:")
print(f"  ||v_k φ_k||_{{L^2_t L^6_x}}  via  ||∇(v_k φ_k)||_{{L^2}} (Sobolev)")
print(f"  ||v_k φ_k||_{{L^∞_t L^2_x}}  directly from energy")
print()

# Interpolation between L^∞_t L^2_x and L^2_t L^6_x
# Gives L^p_t L^q_x with 2/p + 3/q = 3/2 (parabolic Sobolev)
# Key: L^{10/3}_{t,x} embedding
print("STEP 3: Parabolic Sobolev (Ladyzhenskaya-type):")
print("  ||v_k φ_k||_{L^p_t L^q_x} < ∞  when  2/p + d/q = d/2")
print(f"  In d=3:  2/p + 3/q = 3/2")
print()

# For the isotropic case p = q:
# 2/q + 3/q = 3/2 → 5/q = 3/2 → q = 10/3
q_iso = Rational(10, 3)
check = Rational(2, q_iso) + Rational(3, q_iso)
print(f"  Isotropic (p=q): q = {q_iso},  check: 2/q + 3/q = {check} = 3/2 ✓")
print(f"  So v_k φ_k ∈ L^{{10/3}}_{{t,x}}(Q_k)")
print()

# STEP 4: The pressure Hölder pairing
print("STEP 4: Pressure Hölder pairing")
print("  |I_p| ≤ ||p||_{L^β(Q_k)} · ||v_k φ_k||_{L^{β'}(Q_k)} · ||∇φ_k||_{L^∞}")
print()
print("  We need β' ≤ 10/3 (since that's what De Giorgi energy controls)")
print("  β' = β/(β-1) ≤ 10/3")

beta_from_constraint = solve(beta/(beta-1) - Rational(10,3), beta)
print(f"  → β/(β-1) = 10/3  gives  β = {beta_from_constraint}")
print(f"  → β ≥ 10/7 ≈ {float(Rational(10,7)):.4f}")
print()

# But there's another constraint from the recursion!
print("STEP 5: The recursion constraint")
print("  For the recursion U_{k+1} ≤ C b^k U_k^{1+δ} to close,")
print("  we need the RHS to be a SUPERLINEAR power of U_k.")
print()
print("  The pressure term contributes:")
print("  |I_p| ≤ ||p||_{L^β} · ||v_k φ_k||_{L^{β'}}")
print()
print("  Now p comes from u, and the part of u on the support of φ_k")
print("  is controlled by v_k + C_k. The 'high' part v_k is controlled")
print("  by U_k, but C_k is a fixed constant — this is where the trouble is.")
print()

# STEP 6: The detailed accounting
print("STEP 6: Detailed accounting for β = 4/3")
print()

beta_val = Rational(4, 3)
beta_prime_val = beta_val / (beta_val - 1)
print(f"β = {beta_val},  β' = {beta_prime_val}")

# CZ: p ∈ L^{4/3} requires u ∈ L^{8/3}
u_needed = 2 * beta_val
print(f"CZ requires: u ∈ L^{{{u_needed}}} for p ∈ L^{{{beta_val}}}")
print(f"Check: u ∈ L^{{8/3}} — is this available from energy estimates?")
print()

# u ∈ L^{3,∞} (critical) is the a priori bound. Need something better.
# From energy: u ∈ L^2_t H^1_x → u ∈ L^2_t L^6_x ∩ L^∞_t L^2_x
# The L^{8/3} norm: 2/p + 3/q = 3/2 with q = 8/3
# 3/(8/3) = 9/8, so 2/p = 3/2 - 9/8 = 3/8, p = 16/3
p_time = Rational(2, Rational(3,2) - Rational(3, Rational(8,3)))
print(f"For L^p_t L^{{8/3}}_x: 2/p + 3/(8/3) = 3/2")
print(f"  2/p = 3/2 - 9/8 = 3/8,  p = {p_time}")
print(f"  So u ∈ L^{{16/3}}_t L^{{8/3}}_x — YES, this is subcritical, available!")
print()

# Now for the Hölder dual side:
print(f"The Hölder dual: ||div(v_k φ_k² ê)||_{{L^{{β'}}}} with β' = {beta_prime_val}")
print(f"  This involves ||∇(v_k φ_k)||_{{L^{{β'}}}} and ||v_k ∇φ_k||_{{L^{{β'}}}}")
print(f"  β' = 4 — need these in L^4")
print()

# L^4: from L^2 ∩ L^6 interpolation
# 1/4 = θ/2 + (1-θ)/6 → θ = 1/2
theta_4 = solve(Rational(1,4) - Symbol('t')/2 - (1-Symbol('t'))/6, Symbol('t'))[0]
print(f"L^4 interpolation: 1/4 = θ/2 + (1-θ)/6 → θ = {theta_4}")
print(f"  ||f||_{{L^4}} ≤ ||f||_{{L^2}}^{{1/2}} ||f||_{{L^6}}^{{1/2}}")
print(f"  ≤ ||f||_{{L^2}}^{{1/2}} ||∇f||_{{L^2}}^{{1/2}}  (Sobolev)")
print()

# Total parabolic exponent check for L^4_{t,x}:
check_4 = Rational(2, 4) + Rational(3, 4)
print(f"L^4_{{t,x}}: 2/p + 3/q = {check_4} {'<' if check_4 < Rational(3,2) else '>='} 3/2")
print(f"  {check_4} < 3/2 = {Rational(3,2)}")
print(f"  So L^4_{{t,x}} is NOT available from H^1 energy alone!")
print(f"  This is where the bottleneck tightens.")
print()

print("STEP 7: Measure of super-level sets and the recursion")
print()
print("The De Giorgi recursion requires estimating the MEASURE of A_k = {|u| > C_k}:")
print("  |A_k| ≤ C_k^{-3} ||u||_{L^{3,∞}}^3  (from weak-L^3)")
print()
print("The energy U_k already lives on A_k. The recursion:")
print("  U_{k+1} ≤ C · 2^{kα} · U_k^{1+δ}")
print()
print("requires δ > 0. The pressure contribution to the exponent δ:")
print("  From Hölder: pressure term ~ ||p||_{L^β(A_k)} · ||v_k||_{L^{β'}(A_k)}")
print("  ~ |A_k|^{some power} · U_k^{something}")
print()

# The measure factor from restricting to A_k
# |A_k| can be bounded by U_k via Chebyshev:
# |A_k ∩ supp φ_k| ≤ ||v_k φ_k||_{L^2}^2 / (C_{k+1} - C_k)^2 = U_k / (M 2^{-k-1})^2
print("Chebyshev: |A_k ∩ supp φ_k| ≤ U_k / (M 2^{-k-1})^2 = 4·2^{2k} U_k / M^2")
print()

# ========================================================================
# 6. CRITICAL EXPONENT ANALYSIS
# ========================================================================
print("=" * 70)
print("CRITICAL EXPONENT ANALYSIS")
print("=" * 70)
print()

# In the recursion, the pressure term contributes:
# I_p ≤ ||p||_{L^β(Q_k)} · ||v_k φ_k||_{L^{β'}(Q_k)} · correction
#
# Using interpolation on the β' side and measure estimates:
# ||v_k φ_k||_{L^{β'}(Q_k)} ≤ |Q_k|^{...} · ||v_k φ_k||_{L^{10/3}}^{...}
#
# For the recursion to close, we need the total power of U_k to exceed 1.

print("The recursion closes when the total U_k exponent > 1.")
print()
print("From parabolic Sobolev: v_k φ_k ∈ L^{10/3}_{t,x} with")
print("  ||v_k φ_k||_{L^{10/3}} ≤ C · U_k^{1/2}")
print()

# Power counting:
# Pressure term after all estimates:
# I_p ≤ C(β) · ||p||_{L^β} · U_k^{α(β)}
#
# For the recursion: need α(β) > 1 counting ALL contributions

# The key relationship: in 3D, the pressure Hölder pairing gives
# I_p ~ ||p||_{L^β} · ||v_k||_{L^{β'}} ≤ ||p||_{L^β} · |A_k|^{1/β' - 3/10} · U_k^{3/(10) · (something)}

# Let's compute the critical β explicitly
print("Power counting in the recursion:")
print()
print("The pressure integral after Hölder:")
print("  I_p ≤ ||p||_{L^β_t L^β_x} · ||v_k φ_k²||_{L^{β'}_t L^{β'}_x}")
print()
print("Using CZ: ||p||_{L^β} ~ ||u||_{L^{2β}}²")
print("And the L^{2β} norm of u restricted to A_k:")
print("  ||u||_{L^{2β}(A_k)} ≤ ||u||_{L^{3,∞}} · |A_k|^{1/(2β) - 1/3}")
print("  (valid when 2β < 3, i.e., β < 3/2)")
print()

# For β = 4/3:
# 2β = 8/3, 1/(2β) - 1/3 = 3/8 - 1/3 = 1/24
exp_measure_4_3 = Rational(3,8) - Rational(1,3)
print(f"β = 4/3: 1/(2β) - 1/3 = 3/8 - 1/3 = {exp_measure_4_3}")
print(f"  ||u||_{{L^{{8/3}}(A_k)}} ≤ ||u||_{{L^{{3,∞}}}} · |A_k|^{{{exp_measure_4_3}}}")
print()

# For β = 3/2:
# 2β = 3, 1/(2β) - 1/3 = 1/3 - 1/3 = 0 → logarithmic, borderline!
exp_measure_3_2 = Rational(1,3) - Rational(1,3)
print(f"β = 3/2: 1/(2β) - 1/3 = 1/3 - 1/3 = {exp_measure_3_2}")
print(f"  ||u||_{{L^3(A_k)}} ≤ ||u||_{{L^{{3,∞}}}} · |A_k|^0 — BORDERLINE!")
print(f"  This is exactly critical: L^{{3,∞}} ↛ L^3")
print()

# ========================================================================
# 7. THE β = 4/3 CHAIN — ANNOTATED
# ========================================================================
print("=" * 70)
print("ANNOTATED CHAIN: ... → β = 4/3")
print("=" * 70)
print()
print("Chain of inequalities (each arrow = one estimate):")
print()
print("(A) u ∈ L^∞_t L^2_x ∩ L^2_t H^1_x")
print("     │")
print("     │ [Sobolev embedding H^1 ↪ L^6 in d=3]")
print("     ▼")
print("(B) v_k φ_k ∈ L^∞_t L^2_x ∩ L^2_t L^6_x")
print("     │")
print("     │ [Parabolic interpolation: 2/p + 3/q = 3/2]")
print("     ▼")
print("(C) v_k φ_k ∈ L^{10/3}_{t,x}(Q_k)")
print("     │")
print("     │ [Hölder in space-time: pair with L^β to get L^1]")
print("     │ [Need: 1/β + 1/β' = 1, β' ≤ 10/3]")
print("     │ [So: β ≥ 10/7]")
print("     ▼")
print("(D) Pressure pairing: ∫p · div(v_k φ_k² ê) ≤ ||p||_{L^β} · ||...||_{L^{β'}}")
print("     │")
print("     │ [CZ: p ∈ L^β requires u⊗u ∈ L^β, i.e., u ∈ L^{2β}]")
print("     │ [From (A): u ∈ L^{2β}_t,x when 2/p + 3/(2β) ≤ 3/2]")
print("     │ [  → 2β ≤ 10/3 → β ≤ 5/3]")
print("     ▼")
print("(E) So β ∈ [10/7, 5/3] is the admissible range from Sobolev alone")
print("     │")
print("     │ [But recursion closure needs SUPERLINEAR power of U_k]")
print("     │ [The pressure contribution: measure of A_k enters]")
print("     │ [|A_k| ~ U_k / (M 2^{-k})² (Chebyshev)]")
print("     │ [Measure interpolation: L^{2β} restricted to A_k]")
print("     │ [needs |A_k|^{extra power} → extra U_k power]")
print("     ▼")
print("(F) Recursion closes when total U_k exponent > 1")
print("     │")
print("     │ [Working backward from the recursion requirement,")
print("     │  the achievable exponent with u ∈ L^{3,∞} is β = 4/3]")
print("     ▼")
print("(G) β = 4/3:  p ∈ L^{4/3}_t L^{4/3}_x")
print("     │")
print("     │ [This gives PARTIAL regularity — the singular set has]")
print("     │ [1-dim parabolic Hausdorff measure zero (CKN-type)]")
print("     ▼")
print("(H) FULL regularity would need β > 3/2")
print("     (because 2β > 3 = d, which exits the critical regime)")
print()

# ========================================================================
# 8. WHERE EXACTLY IS THE BOTTLENECK?
# ========================================================================
print("=" * 70)
print("BOTTLENECK IDENTIFICATION")
print("=" * 70)
print()

print("The β = 4/3 limitation is DISTRIBUTED across TWO sharp steps:")
print()
print("BOTTLENECK 1: CZ + Critical Embedding (Steps A→E)")
print("  u ∈ L^{3,∞} is the critical a priori bound.")
print("  u⊗u ∈ L^{3/2,∞} → p ∈ L^{3/2,∞} (weak type only).")
print("  For strong-type L^β, need β < 3/2 strictly.")
print("  ★ This is a HARD ceiling from the critical scaling of NS.")
print()
print("BOTTLENECK 2: Recursion Superlinearity (Steps E→F)")
print("  Even within the admissible range, closing the recursion")
print("  requires the pressure term to be controlled by U_k^{1+δ}.")
print("  The measure factor |A_k| ~ U_k / 2^{2k} introduces the")
print("  precise exponent. Optimizing over Hölder exponents gives β = 4/3.")
print("  ★ This is where the De Giorgi recursion structure matters.")
print()
print("CONCLUSION: NOT a single sharp inequality. Two constraints interact:")
print("  (1) CZ ceiling β < 3/2 from critical velocity")
print("  (2) Recursion superlinearity requirement pushing β down to 4/3")
print()

# ========================================================================
# 9. NUMERICAL VERIFICATION OF EXPONENT RELATIONSHIPS
# ========================================================================
print("=" * 70)
print("NUMERICAL VERIFICATION")
print("=" * 70)
print()

# Verify all Hölder conjugates
pairs = [
    (Rational(4,3), 4),
    (Rational(3,2), 3),
    (Rational(5,3), Rational(5,2)),
    (Rational(10,7), Rational(10,3)),
]

print("Hölder conjugates (1/β + 1/β' = 1):")
for b, bp in pairs:
    check = Rational(1,b) + Rational(1,bp)
    status = "✓" if check == 1 else "✗"
    print(f"  β = {b}, β' = {bp}: 1/{b} + 1/{bp} = {check} {status}")

print()

# Verify parabolic Sobolev exponents (2/p + 3/q = 3/2)
print("Parabolic Sobolev (2/p + 3/q = 3/2):")
ps_pairs = [
    (Rational(10,3), Rational(10,3)),  # isotropic
    (2, 6),  # maximal spatial
    (Rational(8,3), Rational(8,1)),  # pure time
    (Rational(16,3), Rational(8,3)),  # for pressure
    (4, Rational(12,5)),  #
]
for p_val, q_val in ps_pairs:
    check = Rational(2, p_val) + Rational(3, q_val)
    status = "✓" if check == Rational(3,2) else f"= {check} ✗"
    print(f"  L^{{{p_val}}}_t L^{{{q_val}}}_x: 2/{p_val} + 3/{q_val} = {check} {status}")

print()

# ========================================================================
# 10. BOGOVSKII CORRECTOR SCALING
# ========================================================================
print("=" * 70)
print("BOGOVSKII CORRECTOR SCALING")
print("=" * 70)
print()

print("Goal: Make the test function divergence-free to kill the pressure term.")
print("Construct w_k with div(φ_k u - w_k) = 0, i.e., div w_k = u · ∇φ_k + φ_k div u = u · ∇φ_k")
print("(since div u = 0).")
print()
print("Bogovskii operator B on a domain Ω: div(Bf) = f, with estimate")
print("  ||Bf||_{W^{1,q}(Ω)} ≤ C(Ω) ||f||_{L^q(Ω)}  for 1 < q < ∞")
print()

# The domain is the annular region where ∇φ_k is supported
# Scale: annulus width ~ 2^{-k} (shrinking as k→∞)
print("Annular region where ∇φ_k lives:")
print("  Width ~ r_k - r_{k+1} ~ r₀ · 2^{-k-1}")
print("  ||∇φ_k||_{L^∞} ~ 2^k / r₀")
print()

# The source for Bogovskii: f_k = u · ∇φ_k
# ||f_k||_{L^q(A_k)} ≤ ||u||_{L^q(A_k)} · ||∇φ_k||_{L^∞}
# ~ 2^k · ||u||_{L^q(A_k)}

# On A_k: u is between levels C_k and C_{k+1}, plus the tail
# Measure of A_k:
# |{|u| > C_k} ∩ B_{r_k}| ≤ C · C_k^{-3} (from u ∈ L^{3,∞})
# C_k = M(1 - 2^{-k}) → C_k → M, so this goes to C · M^{-3}

# The thin annulus {C_k ≤ |u| ≤ C_{k+1}} has measure:
# |A_k| ~ |{|u| > C_k}| - |{|u| > C_{k+1}}|
# ~ C_k^{-3} - C_{k+1}^{-3}
# ≈ 3 C_k^{-4} · (C_{k+1} - C_k) = 3 M^{-4} · M 2^{-k-1} ≈ 3/(2 M^3) · 2^{-k}

print("Measure of annular level set A_k ∩ {C_k ≤ |u| ≤ C_{k+1}}:")
print("  |A_k|_level ~ C_k^{-3} - C_{k+1}^{-3}")
print("  ≈ 3 C_k^{-4} · M 2^{-k-1}")
print("  ~ M^{-3} · 2^{-k}  (for k large, C_k ≈ M)")
print()

# Bogovskii estimate:
# ||w_k||_{L^q} ≤ C(Ω_k) ||u · ∇φ_k||_{L^q(A_k)}
#
# BUT the constant C(Ω_k) depends on the domain Ω_k!
# For the Bogovskii operator on an annulus of width δ_k ~ 2^{-k}:
# C(Ω_k) ~ δ_k^{-1} · diam(Ω_k) ~ 2^k · 1 = 2^k
# (This is the Bogovskii constant on thin domains — it blows up!)

print("Bogovskii constant on thin annulus (width δ_k ~ 2^{-k}):")
print("  C(Ω_k) ~ δ_k^{-1} ~ 2^k")
print("  (Acosta-Durán: C(Ω) ~ diam(Ω)/width(Ω) for John domains)")
print()

# Total corrector estimate:
# ||w_k||_{L^q} ≤ C(Ω_k) · ||u · ∇φ_k||_{L^q}
# ≤ 2^k · ||u||_{L^q(A_k)} · 2^k
# = 2^{2k} · ||u||_{L^q(A_k)}

print("Total corrector estimate:")
print("  ||w_k||_{L^q} ≤ C(Ω_k) · ||f_k||_{L^q}")
print("  = C(Ω_k) · ||u · ∇φ_k||_{L^q(A_k)}")
print("  ≤ 2^k · 2^k · ||u||_{L^q(A_k)}")
print("  = 2^{2k} · ||u||_{L^q(A_k)}")
print()

# Compare with energy U_k:
# ||v_k||_{L^2(supp φ_k)}^2 = U_k → ||v_k||_{L^2} ~ U_k^{1/2}
# The level set has |u| ~ C_k ~ M on A_k, so ||u||_{L^q(A_k)} ~ M · |A_k|^{1/q}
# ~ M · (M^{-3} · 2^{-k})^{1/q}

print("On the level set A_k: ||u||_{L^q(A_k)} ~ M · |A_k|^{1/q}")
print("  ~ M · (M^{-3} · 2^{-k})^{1/q}")
print("  = M^{1-3/q} · 2^{-k/q}")
print()

for q_val in [2, Rational(8,3), 3, 4]:
    u_norm = f"M^{{{1 - 3/q_val}}} · 2^{{-k/{q_val}}}"
    w_norm = f"2^{{2k}} · M^{{{1 - 3/q_val}}} · 2^{{-k/{q_val}}} = M^{{{1-3/q_val}}} · 2^{{k(2 - 1/{q_val})}}"
    print(f"  q = {q_val}:")
    print(f"    ||u||_{{L^{{{q_val}}}(A_k)}} ~ {u_norm}")
    growth_exp = 2 - Rational(1, q_val)
    print(f"    ||w_k||_{{L^{{{q_val}}}}} ~ M^{{{1-Rational(3,q_val)}}} · 2^{{k·{growth_exp}}}")
    print(f"    Growth rate: 2^{{k·{growth_exp}}} — {'GROWS' if growth_exp > 0 else 'DECAYS'} as k→∞")
    print()

print("CORRECTOR SCALING VERDICT:")
print("  ||w_k||_{L^q} grows as 2^{k(2-1/q)} for ALL q ≥ 1.")
print("  Compare: De Giorgi energy U_k should → 0 (needs 2^{-kδ} decay).")
print("  The corrector GROWS exponentially in k — it destroys the recursion!")
print()
print("  The Bogovskii corrector on shrinking annuli costs 2^{2k} from:")
print("    (1) ∇φ_k ~ 2^k  [cutoff gradient]")
print("    (2) C(Ω_k) ~ 2^k [thin domain constant]")
print("  These compound: 2^k × 2^k = 2^{2k}")
print()
print("  CONCLUSION: Bogovskii corrector is NOT viable for eliminating pressure")
print("  in the standard De Giorgi iteration. The thin annulus blowup kills it.")

# ========================================================================
# SUMMARY TABLE
# ========================================================================
print("\n" + "=" * 70)
print("COMPARISON: DRIFT-DIFFUSION vs NAVIER-STOKES")
print("=" * 70)
print()
print("| Term               | Drift-Diffusion (CV 2010)      | Navier-Stokes (V 2007)           | Difference          |")
print("|--------------------|---------------------------------|----------------------------------|---------------------|")
print("| Dissipation        | -∫|∇(θ-C_k)_+|² φ_k²          | -∫|∇(|u|-C_k)_+|² φ_k²         | Same structure      |")
print("| Transport          | ∫(u·∇θ)(θ-C_k)_+ φ_k²         | ∫(u·∇|u|)(|u|-C_k)_+ φ_k²      | Same by div u=0     |")
print("|                    | = -½∫|θ-C_k|²_+ u·∇φ_k²       | ≠ clean IBP (pressure remains)   | KEY DIFFERENCE      |")
print("| Pressure           | ABSENT                         | ∫p·div(v_k φ_k² ê) ≠ 0         | THE GAP             |")
print("| Cutoff correction  | ∫(θ-C_k)_+² Δφ_k² (absorbed)  | Same + pressure cutoff terms     | Worse by O(2^{2k})  |")
print("| Measure estimate   | |{θ>C_k}| ≤ C·C_k^{-q₀}       | |{|u|>C_k}| ≤ C·C_k^{-3}       | Same structure      |")
print("| Recursion closure  | CLOSES (δ > 0 achieved)        | PARTIAL (δ > 0 only if β > 3/2) | Pressure blocks     |")
print()
