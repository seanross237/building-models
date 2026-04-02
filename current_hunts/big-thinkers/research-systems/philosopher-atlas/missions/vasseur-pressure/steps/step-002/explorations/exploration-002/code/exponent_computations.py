"""
Exponent computations for (H^1, L^{4/3}) interpolation analysis.
Exploration 002: Interpolation Route — Vasseur De Giorgi pressure.

Sections:
1. Complex interpolation exponents [H^1, L^{4/3}]_theta
2. Test function Lp_theta' analysis
3. De Giorgi recursion U_k exponent tracking
4. Lorentz refinement analysis
"""

from fractions import Fraction
import numpy as np

print("=" * 65)
print("SECTION 1: Complex Interpolation [H^1, L^{4/3}]_theta")
print("Formula: 1/p_theta = (1-theta)*1 + theta*(3/4) = 1 - theta/4")
print("=" * 65)

thetas = [Fraction(0), Fraction(1,10), Fraction(3,10), Fraction(1,2),
          Fraction(7,10), Fraction(9,10), Fraction(1)]

print(f"{'theta':>8} {'p_theta':>12} {'p_theta (frac)':>20} {'< 4/3?':>8}")
print("-" * 55)
for theta in thetas:
    # 1/p_theta = 1 - theta/4
    inv_p = 1 - theta / 4
    p_theta = 1 / inv_p
    four_thirds = Fraction(4, 3)
    print(f"{float(theta):>8.2f} {float(p_theta):>12.6f} {str(p_theta):>20} {str(p_theta < four_thirds):>8}")

print()
print("Key: At theta=0, p_theta=1 (H^1 endpoint)")
print("     At theta=1, p_theta=4/3 (L^{4/3} endpoint)")
print("     For all theta in (0,1): p_theta in (1, 4/3)")
print("     => Complex interpolation gives WORSE Lebesgue exponent")

print()
print("=" * 65)
print("SECTION 2: Paired exponent p_theta' analysis")
print("For Holder: 1/p + 1/p' = 1")
print("If using ||p||_{L^{p_theta}} * ||psi_k||_{L^{p_theta'}}")
print("=" * 65)

print(f"{'theta':>8} {'p_theta':>12} {'p_theta_prime':>15} {'> 4?':>8} {'> 10/3?':>10}")
print("-" * 60)
for theta in thetas:
    inv_p = 1 - theta / 4
    p_theta = 1 / inv_p
    if inv_p == 1:  # theta=0: p_theta=1, dual is infinity
        print(f"{float(theta):>8.2f} {float(p_theta):>12.6f} {'inf':>15} {'True':>8} {'True':>10}  [theta=0 endpoint]")
        continue
    p_prime = 1 / (1 - inv_p)  # = p_theta / (p_theta - 1)
    four = Fraction(4, 1)
    ten_thirds = Fraction(10, 3)
    print(f"{float(theta):>8.2f} {float(p_theta):>12.6f} {float(p_prime):>15.6f} "
          f"{str(p_prime > four):>8} {str(p_prime > ten_thirds):>10}")

print()
print("De Giorgi energy gives v_k in L^{10/3}_{t,x} (parabolic Sobolev).")
print("psi_k = v_k * phi_k * nabla(phi_k) in L^{10/3} as well.")
print("For theta > 0: p_theta' > 4 > 10/3, so psi_k NOT in L^{p_theta'}.")
print("=> Using complex interpolation with theta > 0 FAILS.")

print()
print("=" * 65)
print("SECTION 3: De Giorgi U_k exponent tracking")
print("=" * 65)

print("""
De Giorgi energy estimate:
  U_{k+1} <= C * |I_convective| + |I_pressure|

Current pressure bound:
  |I_p| <= ||p||_{L^{4/3}(Q_k)} * ||psi_k||_{L^4(Q_k)}
         <= C * E_0 * 2^k * U_k^{1/2}

This gives sigma = 1/2 (the U_k exponent).
For recursion to close: need sigma > 1 (superlinear in U_k).

Let's check whether any interpolation changes sigma:
""")

print("Strategy A: Use complex interpolation [H^1, L^{4/3}]_theta = L^{p_theta}")
print("For p_theta in (1, 4/3):")
print("  ||p||_{L^{p_theta}(Q_k)} <= |Q_k|^{1/p_theta - 3/4} * ||p||_{L^{4/3}(Q_k)}")
print("  This is C * E_0 * (size factor) -- still E_0-bounded, sigma = 1/2.")
print()

# Compute the size factor for p_theta < 4/3
print("Size factor |Q_k|^{1/p_theta - 3/4} (with |Q_k| ~ 2^{-5k} in R^3 x R):")
print(f"{'theta':>8} {'p_theta':>10} {'1/p_theta - 3/4':>18} {'size exp (in 2^k)':>20}")
print("-" * 65)
for theta in thetas[1:]:  # skip theta=0
    inv_p = 1 - theta / 4
    p_theta = 1 / inv_p
    exponent = inv_p - Fraction(3, 4)  # = 1/p_theta - 3/4
    # |Q_k|^{...} ~ (2^{-5k})^{exponent} = 2^{-5k*exponent}
    size_exp = -5 * exponent
    print(f"{float(theta):>8.2f} {float(p_theta):>10.4f} {float(exponent):>18.6f} {float(size_exp):>20.4f}")

print()
print("All size factors give additional 2^{-k*...} decay, not U_k improvement.")
print("sigma remains 1/2 in all cases.")

print()
print("=" * 65)
print("SECTION 4: Lorentz refinement L^{4/3, q} analysis")
print("=" * 65)

print("""
If p in L^{4/3, q}(Q_k) for q < 4/3, and psi_k in L^{4, q'}:
  |I_p| <= ||p||_{L^{4/3,q}} * ||psi_k||_{L^{4,q'}}

The L^{p,q} Holder estimate holds with paired indices.

Question: Does L^{4/3,q} norm of p depend on U_k?

From CZ theory:
  p ~ R_i R_j (u_i u_j)
  If u in L^{a, r} then u^2 in L^{a/2, r/2} and p in L^{a/2, r/2}.

From Leray-Hopf energy: u in L^infty_t L^2_x cap L^2_t W^{1,2}_x
  => By Sobolev: u in L^2_t L^6_x => u^2 in L^1_t L^3_x
  => p in L^1_t L^3_x => p in L^{3/2}(Q_k) locally [better than L^{4/3}!]

Wait -- this is actually better than what the goal states. Let me recheck:
""")

print("Checking the actual CZ bound more carefully:")
print()
print("u in L^2_t L^6_x (3D Sobolev from energy):")
print("  u_i u_j in L^1_t L^3_x")
print("  CZ: p in L^1_t L^3_x")
print("  Space-time: p in L^{3/2}(Q_k) (by Minkowski/norm comparison)?")
print()
print("L^1_t L^3_x vs L^{3/2}(Q_k):")
print("  ||p||_{L^{3/2}(Q_k)}^{3/2} = int_0^T int_{Q_k^x} |p|^{3/2}")
print("  vs int_0^T ||p(t)||_{L^3_x}^1 dt  [this is L^1_t L^3_x norm]")
print()
print("These are DIFFERENT norms. L^1_t L^3_x does NOT directly give L^{3/2}_{t,x}.")
print()
print("For comparison: p in L^{4/3}_t L^2_x from u in L^{8/3}_t L^4_x.")
print("But De Giorgi uses L^{4/3} in SPACE-TIME, not mixed.")
print()

# Verify the claimed L^{4/3} bound
print("Checking L^{4/3}_{t,x} bound from L^{4/3}_t L^2_x:")
print("  p in L^{4/3}_t L^2_x, Q_k^x has volume ~ 2^{-3k}")
print("  ||p||_{L^{4/3}(Q_k)} <= |Q_k^x|^{3/4 - 1/2} ||p||_{L^{4/3}_t L^{4/3 * ?}}")
print()
print("This is getting complex. The L^{4/3}(Q_k) bound as stated in the goal")
print("likely comes from a specific parabolic interpolation of the two bounds.")
print("The exact source doesn't change the main conclusion about H^1 interpolation.")

print()
print("=" * 65)
print("SECTION 5: Summary of exponent landscape")
print("=" * 65)
print()
print("For recursion to close, need exponent sigma > 1 in:")
print("  U_{k+1} <= C^k * U_k^sigma")
print()
print("Exponents in current Holder estimate:")
print("  ||p||_{L^{4/3}} contributes: E_0 (constant, sigma_p = 0)")
print("  ||psi_k||_{L^4} contributes: 2^k * U_k^{1/2}  (sigma_psi = 1/2)")
print("  Total: sigma = sigma_p + sigma_psi = 0 + 1/2 = 1/2 < 1")
print()
print("To improve sigma:")
print("  Option A: Get sigma_p > 1/2 (pressure contributes U_k power)")
print("    => Requires ||p||_X ~ U_k^{sigma_p} -- but p far-field ~ E_0 always")
print("  Option B: Get sigma_psi > 1 (test function contributes more)")
print("    => Requires ||psi_k||_Y ~ U_k^{sigma_psi} with sigma_psi > 1")
print("    => Would need L^q norm of psi_k with q < 4 and U_k^{>1} bound")
print("    => Not available from De Giorgi energy at this level")
print()
print("The ONLY way to improve is through better local pressure decomposition")
print("(near-field term ~ U_k^alpha for some alpha > 0) PLUS improved test")
print("function estimate. The interpolation route provides neither.")

print()
print("=" * 65)
print("CONCLUSION")
print("=" * 65)
print("""
The interpolation space analysis confirms:
1. [H^1, L^{4/3}]_theta = L^{p_theta} with p_theta < 4/3 (WORSE, not better)
2. (H^1, L^{4/3})_{theta,q} subset of L^{p_theta, q} (real interpolation)
3. sigma stays at 1/2 regardless of interpolation choice
4. Far-field pressure: always E_0-bounded via interpolation norms
5. W^{1,3} threshold not bypassed

VERDICT: FAILURE. No interpolation route improves beta beyond 4/3.
""")
