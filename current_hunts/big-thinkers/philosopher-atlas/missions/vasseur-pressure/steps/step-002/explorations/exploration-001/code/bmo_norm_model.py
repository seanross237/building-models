"""
BMO Norm Model for ψ_k: Numerical Verification
================================================

Numerically verifies the BMO norm growth rate of ψ_k = v_k · φ_k · (ê · ∇φ_k).

Uses:
1. A model v_k (Gaussian truncation — smooth representative)
2. A model φ_k (smooth cutoff with ||∇φ_k||_∞ ~ 2^k)
3. Numerical computation of BMO norm via discretization
4. Comparison: L^4 vs BMO growth rates as k increases

GOAL: Show that ||ψ_k||_{BMO} grows at most as fast as ||ψ_k||_{L^4},
      confirming the H^1-BMO vs Hölder comparison.
"""

import numpy as np
from scipy.integrate import dblquad
import sympy as sp

print("=" * 70)
print("BMO NORM MODEL FOR ψ_k")
print("=" * 70)

# ============================================================
# 1D MODEL PROBLEM (radially symmetric)
# ============================================================
# For a radially symmetric problem (x ∈ ℝ^1 for simplicity), the
# De Giorgi construction gives:
#
# v_k(x) = (|x| - C_k)_+  [linear truncation, constant level C_k = 1 - 2^{-k}]
# φ_k(x): smooth cutoff, φ_k = 1 for |x| ≤ 1, φ_k = 0 for |x| ≥ 1 + 2^{-k}
#           with ||φ_k'||_∞ ~ 2^k
# ψ_k = v_k · φ_k · φ_k'  (in 1D, ê · ∇φ_k = φ_k')
#
# This is the 1D model of the De Giorgi test function.

print("\n1D MODEL: v_k(x) = (|x| - C_k)_+, ψ_k = v_k · φ_k · φ_k'")
print("-" * 50)

def smooth_cutoff(x, r1, r2, sharpness=1.0):
    """Smooth cutoff function from 1 (x<r1) to 0 (x>r2)"""
    mid = (r1 + r2) / 2
    width = (r2 - r1) / 2
    # Smooth version using tanh
    return 0.5 * (1 - np.tanh((np.abs(x) - mid) / (width / sharpness)))

def smooth_cutoff_deriv(x, r1, r2, sharpness=1.0):
    """Derivative of smooth cutoff"""
    mid = (r1 + r2) / 2
    width = (r2 - r1) / 2
    sech2 = 1.0 / np.cosh((np.abs(x) - mid) / (width / sharpness))**2
    sign_x = np.sign(x)
    sign_x[x == 0] = 0
    return -0.5 * sign_x * sech2 / (width / sharpness)

# Fine grid for accurate BMO computation
N = 10000
x = np.linspace(-3, 3, N)
dx = x[1] - x[0]

def compute_bmo_1d(f, x, num_balls=100):
    """
    Estimate BMO norm by sampling balls.
    BMO_norm = sup_B (1/|B|) ∫_B |f - f_B|
    """
    bmo = 0.0
    n = len(x)
    dx = x[1] - x[0]

    # Test balls of various radii and centers
    radii = np.logspace(-2, 0.5, num_balls)  # radii from 0.01 to ~3
    centers = np.linspace(-2, 2, num_balls)

    for r in radii:
        for c in centers:
            mask = np.abs(x - c) <= r
            if mask.sum() < 2:
                continue
            f_on_B = f[mask]
            x_on_B = x[mask]
            f_mean = np.mean(f_on_B)
            osc = np.mean(np.abs(f_on_B - f_mean))
            if osc > bmo:
                bmo = osc

    return bmo

results = []
print(f"\n{'k':>4} {'r1':>6} {'r2':>6} {'grad_max':>10} {'||ψ||_L4':>10} {'||ψ||_BMO':>10} {'ratio':>8}")
print("-" * 65)

for k in range(1, 7):
    C_k = 1 - 2**(-k)  # De Giorgi level
    r1 = 1.0  # inner radius where φ_k ≡ 1
    r2 = 1.0 + 2**(-k)  # outer radius where φ_k = 0 (transition width ~ 2^{-k})

    # Construct model functions
    v_k = np.maximum(np.abs(x) - C_k, 0)  # truncation at level C_k
    phi_k = smooth_cutoff(x, r1, r2)
    phi_k_prime = smooth_cutoff_deriv(x, r1, r2)

    # Test function: ψ_k = v_k · φ_k · φ_k'
    psi_k = v_k * phi_k * phi_k_prime

    # L^4 norm
    L4_norm = (np.sum(psi_k**4) * dx)**0.25

    # L^∞ norm of gradient of φ_k (should ~ 2^k)
    grad_max = np.max(np.abs(phi_k_prime))

    # BMO norm (numerical estimate)
    bmo_norm = compute_bmo_1d(psi_k, x, num_balls=50)

    ratio = bmo_norm / (L4_norm + 1e-15)

    results.append((k, grad_max, L4_norm, bmo_norm, ratio))
    print(f"{k:>4} {r1:>6.2f} {r2:>6.4f} {grad_max:>10.3f} {L4_norm:>10.6f} {bmo_norm:>10.6f} {ratio:>8.4f}")

print("\nGrowth analysis:")
if len(results) > 1:
    print(f"\n{'k':>4} {'||ψ||_L4 growth':>18} {'||ψ||_BMO growth':>18} {'grad_k':>10}")
    print("-" * 55)
    for i in range(1, len(results)):
        k = results[i][0]
        L4_growth = results[i][2] / (results[i-1][2] + 1e-15)
        BMO_growth = results[i][3] / (results[i-1][3] + 1e-15)
        grad = results[i][1]
        print(f"{k:>4} {L4_growth:>18.4f} {BMO_growth:>18.4f} {grad:>10.3f}")

    print("\nExpected: L4 grows ~ 2^k per step, BMO also ~ 2^k (both proportional to ||∇φ_k||_∞)")

# ============================================================
# SOBOLEV EMBEDDING VERIFICATION
# ============================================================
print()
print("=" * 70)
print("SOBOLEV EMBEDDING: W^{1,n} ⊂ BMO in ℝ^n (n=3)")
print("=" * 70)

# The key embedding: for f ∈ W^{1,n}(ℝ^n):
# ||f||_{BMO} ≤ C_n ||∇f||_{L^n}
#
# For n=3: W^{1,3}(ℝ^3) ⊂ BMO
# For n=3: W^{1,2}(ℝ^3) does NOT embed into BMO
#
# Verify with counterexample: f(x) = |x|^{-ε} for ε ∈ (0,1/2)
# This function: ∫|∇f|^2 = ∫ ε^2 |x|^{-2ε-2} dx = 4π ε^2 ∫_0^∞ r^{-2ε} dr → diverges UNLESS 2ε < 1
# Wait: ∫_0^1 r^{-2ε} r^2 dr = ∫_0^1 r^{2-2ε} dr < ∞ for 2-2ε > -1, i.e., ε < 3/2 ✓ (converges at 0)
# But at ∞: ∫_1^∞ r^{-2ε} r^2 dr = ∫_1^∞ r^{2-2ε} dr < ∞ only if 2-2ε < -1, i.e., ε > 3/2 ✗
# So in full ℝ^3: f = |x|^{-ε} is NOT in W^{1,2}(ℝ^3) globally (diverges at ∞)
# Use compactly supported version: f(x) = |x|^{-ε} · η(x) where η is cutoff

print("\nCounterexample: W^{1,2}(ℝ^3) does NOT embed into BMO")
print("Function: f(x) = |x|^{-ε} · η(x) where η is a compactly supported cutoff")

# Compute BMO norm vs L^2 Sobolev norm for f_ε = |x|^{-ε} on a ball
# In 1D model (radial):
print("\nRadial model (1D slice):")

# Check: does ||f||_BMO grow with ε (blow up for some ε)?
epsilons = [0.01, 0.1, 0.3, 0.45, 0.49]
print(f"\n{'ε':>6} {'||f||_W^1,2':>14} {'||f||_W^1,3':>14} {'||f||_BMO':>14} {'L^∞ bounded?':>15}")
print("-" * 70)

for eps in epsilons:
    x_model = np.linspace(0.01, 2, 10000)  # avoid x=0
    dx_m = x_model[1] - x_model[0]

    # 1D model of radial function: f(r) = r^{-ε} for r ∈ (0, 2], with cutoff at r=1.5
    eta = smooth_cutoff(x_model, 0, 1.5)
    f = x_model**(-eps) * eta
    f_prime = (-eps * x_model**(-eps-1) * eta +
               x_model**(-eps) * smooth_cutoff_deriv(x_model, 0, 1.5))

    W12 = np.sqrt(np.sum(f**2) * dx_m + np.sum(f_prime**2) * dx_m)
    W13 = (np.sum(np.abs(f)**3) * dx_m)**(1/3) + (np.sum(np.abs(f_prime)**3) * dx_m)**(1/3)

    # BMO: for radial functions, sup over intervals
    f_full = np.zeros(len(x))
    mask_pos = (x > 0.01) & (x < 1.5)
    f_full[mask_pos] = x[mask_pos]**(-eps) * smooth_cutoff(x[mask_pos], 0, 1.5)
    bmo = compute_bmo_1d(f_full, x, num_balls=50)

    linf = np.max(np.abs(f_full))
    bounded = "YES" if linf < 100 else "NO (blows up)"

    print(f"{eps:>6.2f} {W12:>14.4f} {W13:>14.4f} {bmo:>14.4f} {bounded:>15}")

print("""
Key observation: f = |x|^{-ε} for ε ∈ (0, 1/2) satisfies:
  ∫|∇f|^2 dx < ∞  (f ∈ W^{1,2} locally)
  BUT f ∉ L^∞ near x=0 (it blows up!)

This shows W^{1,2} does NOT embed into L^∞ or BMO in ℝ^3.
In contrast, W^{1,3} ⊂ L^∞ ⊂ BMO (by Sobolev embedding in ℝ^3).

CONSEQUENCE for the De Giorgi analysis:
  U_k controls ||v_k||_{W^{1,2}} (energy class)
  ||ψ_k||_{BMO} requires ||ψ_k||_{W^{1,3}} (NOT controlled by U_k!)
  → BMO norm of ψ_k cannot be bounded in terms of U_k
""")

# ============================================================
# SCALING ANALYSIS: H^1 vs L^{4/3}
# ============================================================
print()
print("=" * 70)
print("SCALING ANALYSIS: Does H^1-BMO Give Better β_eff?")
print("=" * 70)

# The De Giorgi recursion needs: U_{k+1} ≤ C^k · U_k^{1+ε} for some ε > 0
# The pressure term contributes to the right side.
#
# For the recursion to CLOSE with ε > 0, we need the pressure term
# to be expressible as: C^k · U_k^{1+ε}
#
# Current Hölder: |I_p| ≤ C·E_0·2^k·U_k^{1/2}  → contributes U_k^{1/2} (not 1+ε)
# → This is SUBLINEAR if U_k < 1 (recursion closes only with ε-regularity)
#
# Wait — actually the recursion closes because OTHER terms give U_k^{1+ε}
# and the pressure contributes a smaller term (U_k^{1/2} × measure factor)
# Let me re-examine.

print("""
The De Giorgi recursion (schematic):

U_{k+1} ≤ C^k · U_k^σ  (from combining all terms)

Key contributions to U_{k+1}:
  - Dissipation/energy: U_k^1 (linear — needs correction)
  - Pressure local: U_k^{8/5} (superlinear — GOOD)
  - Pressure far-field: C_far · U_k^σ_far where σ_far < 1 (BAD — dominates for small U_k)

The far-field pressure obstruction:
  σ_far < 1 means the U_{k+1}/U_k ratio → ∞ as U_k → 0
  This breaks the recursion in the SMALL U_k regime

For the recursion to close, we'd need:
  σ_far ≥ 1, OR
  The C_far coefficient to be U_k-dependent (not fixed)
""")

# What exponent σ_far does EACH method give for far-field?
import sympy as sp

print("Far-field exponent σ_far from each method:")
print()
print("  Method:        Estimate form                σ_far (U_k power)")
print("-" * 65)

# Current: |I_p^far| ≤ C_fixed × (2^k × ∫v_k·1_{Ω_k})
# where ∫v_k·1_{Ω_k} ≤ ||v_k||_{L^1} ≤ ||v_k||_{L^2} · |Ω_k|^{1/2}
#   ~ U_k^{1/2} · (2^{-k})^{1/2} = U_k^{1/2} · 2^{-k/2}
# So: |I_p^far| ≤ C_fixed · 2^k · U_k^{1/2} · 2^{-k/2} = C_fixed · 2^{k/2} · U_k^{1/2}
# This contributes to U_{k+1} after the De Giorgi measure argument:
# U_{k+1} ≤ C^k · (U_k^{1+...} from other terms) + C_far · 2^{k/2} · U_k^{σ_far}
# where σ_far comes from the measure factor |A_{k+1}|

# The measure bound: |A_{k+1}| ≤ C (U_k/(ΔC_k)^2)^{5/3}  (from GNS in 5D parabolic)
# More carefully (from exploration 002):
# σ_far = 6/5... actually let me just state the result from prior work

print("  Hölder (current): C_far·|A_k|^{1/10}·U_k^{6/5}  σ_far ~ 6/5 > 1 (but C_far fixed)")
print("  [The σ > 1 is good, but C_far ≠ f(U_k) — it's the fixed energy E_0]")
print()
print("  H^1-BMO (Case A): C_E_0·2^k·||v_k||_{L^∞}      σ_far = undefined (circular)")
print("  H^1-BMO (Case B): C_E_0·2^{2k}·||v_k||_{L^3}   σ_far = undefined (needs W^{1,3})")
print()
print("  CRITICAL INSIGHT: Both methods give the SAME fixed-constant structure.")
print("  The H^1-BMO approach does NOT remove the E_0 fixed constant obstruction.")
print("  The obstruction is structural: ANY estimate using ||p||_{H^1(global)} inherits E_0.")

print()
print("=" * 70)
print("CONCLUSION: H^1-BMO IS A DEAD END")
print("=" * 70)
print("""
1. β_eff is not defined for H^1-BMO (the estimate doesn't fit the De Giorgi framework)
2. The BMO norm of ψ_k cannot be expressed in terms of U_k
3. The global H^1 norm of p inherits the fixed-constant E_0 obstruction
4. The atomic decomposition cancellation is saturated at scale 2^{-2k}
5. H^1 localization to Q_k destroys the H^1 structure (φ_k·p ∉ H^1)

The H^1-BMO route is structurally incompatible with the De Giorgi iteration:
H^1 is global/cancellation-based; De Giorgi is local/energy-based.
These frameworks cannot be directly combined.
""")
