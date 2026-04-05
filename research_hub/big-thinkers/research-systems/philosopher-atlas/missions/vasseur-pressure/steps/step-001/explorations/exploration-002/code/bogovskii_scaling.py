"""
Bogovskii corrector scaling analysis.

Computes whether the Bogovskii corrector on shrinking De Giorgi annuli
is compatible with the recursion U_k → 0.
"""

from sympy import *

d = 3
k = Symbol('k', positive=True, integer=True)
M = Symbol('M', positive=True)
r0 = Symbol('r0', positive=True)

print("=" * 70)
print("BOGOVSKII CORRECTOR SCALING — DETAILED ANALYSIS")
print("=" * 70)
print()

# ========================================================================
# De Giorgi iteration geometry
# ========================================================================
print("De Giorgi geometry:")
print(f"  Levels: C_k = M(1 - 2^{{-k}}), ΔC_k = C_{{k+1}} - C_k = M·2^{{-k-1}}")
print(f"  Radii: r_k = r₀(1 + 2^{{-k}})/2, Δr_k = r_k - r_{{k+1}} = r₀·2^{{-k-2}}")
print(f"  Cutoff: φ_k with ||∇φ_k||_∞ ≤ C/Δr_k = C·2^{{k+2}}/r₀ ~ 2^k")
print()

# ========================================================================
# Bogovskii problem setup
# ========================================================================
print("Bogovskii problem:")
print("  Given: div(φ_k u) = u · ∇φ_k + φ_k div u = u · ∇φ_k  (since div u = 0)")
print("  Find: w_k with div w_k = u · ∇φ_k")
print("  Then: div(φ_k u - w_k) = 0 and the pressure term vanishes")
print()
print("  w_k = B[u · ∇φ_k]  where B is the Bogovskii operator on Ω_k")
print("  Ω_k = annular region where ∇φ_k ≠ 0")
print("  Width of Ω_k: δ_k = Δr_k ~ r₀ 2^{-k-2}")
print()

# ========================================================================
# Bogovskii operator estimates
# ========================================================================
print("Bogovskii operator estimates:")
print("  ||B[f]||_{W^{1,q}(Ω)} ≤ C(Ω) ||f||_{L^q(Ω)}  for 1 < q < ∞")
print()
print("  The constant C(Ω) depends on the geometry of Ω:")
print("  For a star-shaped domain: C(Ω) ~ diam(Ω)")
print("  For an annulus of width δ and radius R:")
print("    C(Ω) ~ R/δ  (Acosta-Durán estimate for John domains)")
print()

# For the De Giorgi annulus:
# R_k ~ r₀ (fixed), δ_k ~ r₀ 2^{-k-2}
# C(Ω_k) ~ R_k/δ_k ~ 2^{k+2}
print("  For De Giorgi annuli:")
print("  R_k ~ r₀,  δ_k ~ r₀ 2^{-k-2}")
print("  C(Ω_k) ~ R_k/δ_k ~ 2^{k+2}")
print()

# ========================================================================
# Source term scaling
# ========================================================================
print("Source term: f_k = u · ∇φ_k")
print("  ||f_k||_{L^q(Ω_k)} ≤ ||u||_{L^q(Ω_k ∩ A_k)} · ||∇φ_k||_{L^∞}")
print("  ≤ ||u||_{L^q(Ω_k ∩ A_k)} · C 2^k")
print()
print("  where A_k = {|u| > C_k} (the De Giorgi level set)")
print()

# ========================================================================
# Measure of the support
# ========================================================================
print("Measure of Ω_k ∩ A_k:")
print("  Ω_k has spatial volume ~ R_k^2 · δ_k ~ r₀² · r₀ 2^{-k} ~ r₀³ 2^{-k}")
print("  A_k = {|u| > C_k} has measure ≤ ||u||_{L^{3,∞}}^3 · C_k^{-3}")
print()
print("  For k large: C_k ≈ M, so |A_k| ≤ C M^{-3}")
print("  The intersection: |Ω_k ∩ A_k| ≤ min(|Ω_k|, |A_k|)")
print("  For typical scenarios: |Ω_k ∩ A_k| ~ r₀³ 2^{-k} (annulus dominates)")
print()

# ========================================================================
# Corrector norm estimate
# ========================================================================
print("=" * 70)
print("CORRECTOR W^{1,q} ESTIMATE")
print("=" * 70)
print()

for q_val in [2, Rational(8,3), 3, Rational(10,3), 4]:
    print(f"q = {q_val}:")

    # ||w_k||_{W^{1,q}} ≤ C(Ω_k) ||f_k||_{L^q}
    # ≤ 2^{k+2} · ||u||_{L^q(Ω_k)} · 2^k
    # = 2^{2k+2} · ||u||_{L^q(Ω_k)}

    # ||u||_{L^q(Ω_k)} on the annulus where |u| ~ C_k ~ M:
    # ≈ M · |Ω_k|^{1/q} ≈ M · (r₀³ 2^{-k})^{1/q}

    measure_exp = Rational(1, q_val)
    u_norm = f"M · (r₀³ 2^{{-k}})^{{1/{q_val}}}"
    w_growth = 2 + Rational(1, q_val)  # from 2^{2k} · 2^{-k/q}
    net_k_exp = 2 - Rational(1, q_val)  # 2k - k/q = k(2-1/q)

    print(f"  ||u||_{{L^{{{q_val}}}(Ω_k)}} ~ M · r₀^{{3/{q_val}}} · 2^{{-k/{q_val}}}")
    print(f"  ||w_k||_{{W^{{1,{q_val}}}}} ≤ 2^{{2k}} · M · r₀^{{3/{q_val}}} · 2^{{-k/{q_val}}}")
    print(f"  = M r₀^{{3/{q_val}}} · 2^{{k(2-1/{q_val})}}")
    print(f"  = M r₀^{{3/{q_val}}} · 2^{{k·{net_k_exp}}}")
    print(f"  Net growth: 2^{{k·{net_k_exp}}} = 2^{{{float(net_k_exp):.3f}k}}")
    print()

print()
print("=" * 70)
print("COMPARISON WITH De GIORGI ENERGY DECAY")
print("=" * 70)
print()

print("For the De Giorgi recursion U_{k+1} ≤ C b^k U_k^{1+δ} to give U_k → 0:")
print("U_k ~ (C U_0)^{(1+δ)^k} · b^{-k/δ}  (for U_0 << 1)")
print("This decays SUPER-EXPONENTIALLY in k.")
print()
print("The corrector grows as 2^{k(2-1/q)} — exponential in k.")
print("Since super-exponential decay beats exponential growth for large k,")
print("the corrector growth is POTENTIALLY manageable if U_0 is small enough.")
print()
print("BUT: the corrector enters the energy inequality at EVERY step,")
print("modifying the recursion. The effective recursion becomes:")
print("  U_{k+1} ≤ C b^k [U_k^{1+δ} + ||w_k||^{something}]")
print()
print("The ||w_k|| term must itself be expressed as a power of U_k for the")
print("recursion to close. This is the key question.")
print()

# ========================================================================
# Can the corrector be expressed as a power of U_k?
# ========================================================================
print("=" * 70)
print("CORRECTOR IN TERMS OF U_k")
print("=" * 70)
print()

print("The corrector replaces the pressure term. After the substitution")
print("φ_k u → φ_k u - w_k (divergence-free), the energy inequality gains:")
print()
print("  Additional dissipation: -∫ |∇w_k|² (favorable)")
print("  Additional transport: ∫ w_k · ∇(v_k φ_k²) (needs estimation)")
print("  No pressure term: ∫ p div(...) = 0 (GONE! This is the point)")
print()
print("The transport term from w_k:")
print("  |∫ w_k · ∇(v_k φ_k²)| ≤ ||w_k||_{L^q} · ||∇(v_k φ_k)||_{L^{q'}} · ||φ_k||_{L^∞}")
print()

# For q = 2 (natural energy space):
# ||w_k||_{L^2} ~ 2^{3k/2} (from table above, net exp = 3/2)
# ||∇(v_k φ_k)||_{L^2} ≤ U_k^{1/2}
# Product: 2^{3k/2} U_k^{1/2}
# This is 2^{3k/2} times something from U_k — NOT a power of U_k alone.
# The 2^{3k/2} growth contaminates the recursion.

print("For q = 2, q' = 2:")
print("  ||w_k||_{L^2} · ||∇(v_k φ_k)||_{L^2}")
print("  ~ 2^{k·3/2} · U_k^{1/2}")
print()
print("  This introduces a factor 2^{3k/2} into the recursion.")
print("  The recursion becomes: U_{k+1} ≤ C 2^{3k/2} · U_k^{1/2} + ...")
print("  Since the U_k exponent is 1/2 < 1, this is SUBLINEAR!")
print()

# For q = 10/3, q' = 10/7:
# ||w_k||_{L^{10/3}} ~ 2^{k(2-3/10)} = 2^{17k/10}
# ||v_k φ_k||_{L^{10/7}} ≤ ||v_k φ_k||_{L^{10/3}} · μ_k^{7/10-3/10} = ||v_k φ_k||_{L^{10/3}} · μ_k^{2/5}
# ≤ U_k^{1/2} · (2^{2k} U_k)^{2/5} = 2^{4k/5} U_k^{9/10}
# Product: 2^{17k/10} · 2^{4k/5} · U_k^{9/10} = 2^{25k/10} · U_k^{9/10} = 2^{5k/2} · U_k^{9/10}

print("For q = 10/3, q' = 10/7:")
print("  ||w_k||_{L^{10/3}} · ||v_k φ_k||_{L^{10/7}}")
print("  ~ 2^{17k/10} · [U_k^{1/2} · (2^{2k} U_k)^{2/5}]")
print("  = 2^{17k/10} · 2^{4k/5} · U_k^{9/10}")
print("  = 2^{5k/2} · U_k^{9/10}")
print()
print("  U_k exponent = 9/10 < 1 — STILL SUBLINEAR!")
print()

print("=" * 70)
print("BOGOVSKII CORRECTOR VERDICT")
print("=" * 70)
print()
print("The Bogovskii corrector approach FAILS for De Giorgi iteration because:")
print()
print("1. The corrector w_k grows as 2^{k(2-1/q)} — exponentially in k")
print("   Source: thin annulus Bogovskii constant 2^k × cutoff gradient 2^k = 2^{2k}")
print()
print("2. The corrector introduces a SUBLINEAR perturbation into the recursion")
print("   Even in the best case (q = 10/3), the U_k exponent is 9/10 < 1")
print()
print("3. Unlike the pressure-in-Lβ approach, the corrector destroys the")
print("   recursion structure that De Giorgi iteration relies on")
print()
print("4. The fundamental issue: Bogovskii constant C(Ω) ~ diam/width blows up")
print("   on thin annuli, and this blowup is UNAVOIDABLE — it's a geometric")
print("   property of the operator on elongated domains")
print()
print("KEY INSIGHT: The Bogovskii approach transfers the pressure difficulty")
print("into a CORRECTOR GROWTH problem. The growth is worse than the original")
print("pressure problem because it adds a geometric constant that compounds")
print("with the cutoff gradient. Net cost: 2^{2k} vs the original pressure")
print("estimate which involves 2^k from ∇φ_k alone.")
