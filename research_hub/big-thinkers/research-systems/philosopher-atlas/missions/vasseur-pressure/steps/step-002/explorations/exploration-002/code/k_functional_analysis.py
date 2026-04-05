"""
K-functional monotonicity and real interpolation analysis.
Exploration 002: Interpolation Route.

Demonstrates that (H^1, L^{4/3})_{theta,q} is a SUBSPACE of L^{p_theta, q}
and cannot improve the pressure Holder estimate.
"""

from fractions import Fraction
import numpy as np

print("=" * 65)
print("K-FUNCTIONAL MONOTONICITY ANALYSIS")
print("(H^1, L^{4/3})_{theta,q} vs (L^1, L^{4/3})_{theta,q}")
print("=" * 65)

print("""
Setup:
  X_0 = H^1(R^3), ||.||_{H^1} = ||.||_{L^1} + sum_j ||R_j f||_{L^1}
  X_1 = L^{4/3}(R^3)
  Y_0 = L^1(R^3)  (contains H^1)

Key inequality: For all f in H^1,
  ||f||_{L^1} <= ||f||_{H^1}

K-functional definitions:
  K(t, f; H^1, L^{4/3}) = inf_{f=f0+f1} (||f0||_{H^1} + t*||f1||_{L^{4/3}})
  K(t, f; L^1, L^{4/3}) = inf_{f=f0+f1} (||f0||_{L^1}  + t*||f1||_{L^{4/3}})

Monotonicity argument:
  For any admissible decomposition f = f0 + f1 with f0 in H^1:
    ||f0||_{H^1} + t*||f1||_{L^{4/3}} >= ||f0||_{L^1} + t*||f1||_{L^{4/3}}

  The H^1 decompositions are a SUBSET of L^1 decompositions.
  Therefore:
    K(t, f; H^1, L^{4/3}) >= K(t, f; L^1, L^{4/3})  for all t > 0.

Consequence for interpolation norms:
  ||f||_{(H^1, L^{4/3})_{theta,q}}
    = (int_0^infty (t^{-theta} K(t,f; H^1, L^{4/3}))^q dt/t)^{1/q}
    >= (int_0^infty (t^{-theta} K(t,f; L^1, L^{4/3}))^q dt/t)^{1/q}
    = ||f||_{(L^1, L^{4/3})_{theta,q}}
    = ||f||_{L^{p_theta, q}}  [standard Lorentz space identification]

where 1/p_theta = 1 - theta/4.

This means:
  {f : ||f||_{(H^1, L^{4/3})_{theta,q}} < infty}
  SUBSET OF
  {f : ||f||_{L^{p_theta, q}} < infty} = L^{p_theta, q}
""")

print("Verification of Lorentz space identification:")
print("(L^1, L^{4/3})_{theta,q} = L^{p_theta, q} with 1/p_theta = 1-theta/4")
print()
print("Standard result: (L^{p_0}, L^{p_1})_{theta,q} = L^{p,q}")
print("with 1/p = (1-theta)/p_0 + theta/p_1")
print()

thetas = [Fraction(1,4), Fraction(1,2), Fraction(3,4)]
for theta in thetas:
    p0, p1 = Fraction(1,1), Fraction(4,3)
    inv_p = (1-theta)/p0 + theta/p1
    p = 1/inv_p
    print(f"  theta={float(theta):.2f}: 1/p = (1-{float(theta):.2f})*1 + {float(theta):.2f}*(3/4) = {float(inv_p):.4f}, p = {float(p):.4f} = {p}")

print()
print("=" * 65)
print("GLOBAL NORM ARGUMENT (Far-field pressure)")
print("=" * 65)

print("""
The pressure p satisfies (from CLMS 1993 and Leray-Hopf energy):
  ||p||_{H^1(R^3)} <= C * ||u||_{L^2}^2 <= C * E_0  [CLMS]
  ||p||_{L^{4/3}(Q_k)} <= C * E_0  [CZ estimate, each Q_k]

For any interpolation norm (with 0 < theta < 1):
  ||p||_{(H^1, L^{4/3})_{theta,q}}
  <= C(theta,q) * ||p||_{H^1}^{1-theta} * ||p||_{L^{4/3}}^theta  [interpolation norm bound]
  <= C(theta,q) * E_0^{1-theta} * E_0^{theta}
  = C(theta,q) * E_0

The interpolation norm of p is BOUNDED BY E_0, the global energy.

This is INDEPENDENT of k. The De Giorgi recursion requires the pressure
contribution to depend on U_k (the local dyadic energy). Since U_k <= E_0,
any estimate of the form:
  |I_p| <= C * ||p||_{(H^1, L^{4/3})_{theta,q}} * ||psi_k||_Y
         <= C * E_0 * ||psi_k||_Y

gives a bound that does NOT improve with k (it doesn't shrink for small U_k).
The recursion closes only if |I_p| <= C * U_k^{1+eps} for some eps > 0.
""")

print("=" * 65)
print("NEAR/FAR SPLIT (attempting to rescue the argument)")
print("=" * 65)

print("""
One might try: split p = p_near + p_far where
  p_near: localized to Q_{k-1}  => ||p_near||_X ~ U_k^{1/2}  (CZ from local u)
  p_far:  from outside Q_{k-1}  => ||p_far||_X <= C * E_0  (global, unrescuable)

The near term can be made U_k-dependent: good.
The far term is bounded only by E_0: problematic.

For the recursion:
  |I_p| = |I_{p_near}| + |I_{p_far}|
  |I_{p_near}| ~ C * U_k^{1/2} * 2^k * U_k^{1/2} = C * 2^k * U_k  [sigma=1, close!]
  |I_{p_far}|  ~ C * E_0 * 2^k * U_k^{1/2}         [sigma=1/2, problematic]

The near term DOES give sigma = 1 (linear). This is the strategy that NEARLY works.
The far term prevents closure.

Question: Does interpolation improve the far-field bound?
Answer: NO. The far-field pressure p_far ∈ H^1(R^3) with ||p_far||_{H^1} <= C*E_0.
Any interpolation space norm of p_far is still O(E_0).

The issue is fundamental: p_far depends on u outside Q_{k-1}, which is
controlled only by the global energy E_0, not U_k.
""")

print("=" * 65)
print("DUALITY ARGUMENT ATTEMPT")
print("=" * 65)

print("""
Alternative: use the duality of (H^1, L^{4/3})_{theta,q}:
  Dual of (H^1, L^{4/3})_{theta,q} is (BMO, L^4)_{theta, q'}

If psi_k ∈ (BMO, L^4)_{theta, q'}, we could use:
  |int p * psi_k| <= ||p||_{(H^1, L^{4/3})_{theta,q}} * ||psi_k||_{(BMO,L^4)_{theta,q'}}

But:
  (BMO, L^4)_{theta, q'} contains LARGER functions than L^4 alone (BMO is wider).
  We need psi_k to be in a RESTRICTED space for the norm to depend on U_k.

  Specifically: ||psi_k||_{BMO} ~ sup_{ball B} (1/|B| int_B |psi_k - avg|)
  From De Giorgi energy: psi_k ∈ L^4 with ||psi_k||_{L^4} ~ 2^k * U_k^{1/2}
  The BMO norm of psi_k: NOT controlled by the De Giorgi energy.

  In fact: ||psi_k||_{BMO} could be large (the cutoff derivative psi_k can oscillate).
  Using BMO gives WORSE control, not better.

VERDICT: Duality approach also fails.
""")

print("All routes confirm: interpolation between H^1 and L^{4/3} cannot")
print("improve the De Giorgi pressure estimate. FAILURE confirmed.")
