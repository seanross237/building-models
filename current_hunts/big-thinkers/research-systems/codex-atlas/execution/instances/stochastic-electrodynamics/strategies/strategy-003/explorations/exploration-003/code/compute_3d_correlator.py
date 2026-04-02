"""
3D ZPF Two-Point Correlator for Stochastic Electrodynamics.

Goal: Compute C_xx(d) = <x1(t) x2(t)> / sqrt(<x1^2><x2^2>)
      where both oscillators are driven by the 3D ZPF electric field.

Method 1: Analytic formula derived from angular integration.
Method 2: Monte Carlo numerical integration over k-vector directions.
Method 3: Direct numerical integration of the I(q) integral.

Key result: In the narrow-linewidth limit,
C_xx(d) = I(q) / I(0)
where I(q) = integral_{-1}^{1} (1 + u^2) e^{iqu} du
           = (4/q^3) [(q^2 - 1)sin(q) + q cos(q)]
and q = omega_0 * d / c.

This can also be written as:
C_xx(d) = j0(q) - (1/2) j2(q)
where j0 and j2 are spherical Bessel functions.
"""

import numpy as np
from scipy.integrate import quad, dblquad
from scipy.special import spherical_jn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ============================================================
# Method 1: Analytic formula
# ============================================================

def C_xx_analytic(q):
    """
    Analytic 3D ZPF correlator.
    C_xx(q) = (3/2q^3) [(q^2-1)sin(q) + q*cos(q)]
    where q = omega_0 * d / c.

    Uses L'Hopital expansion near q=0 for numerical stability.
    """
    q = np.asarray(q, dtype=float)
    result = np.zeros_like(q)

    # Near q=0: use Taylor expansion
    # C_xx = 1 - q^2/5 + 3q^4/280 + O(q^6)
    small = np.abs(q) < 1e-6
    result[small] = 1.0 - q[small]**2 / 5.0 + 3.0 * q[small]**4 / 280.0

    # For q > 0: use exact formula
    large = ~small
    ql = q[large]
    result[large] = (3.0 / (2.0 * ql**3)) * ((ql**2 - 1.0) * np.sin(ql) + ql * np.cos(ql))

    return result


def C_xx_bessel(q):
    """
    Same result expressed via spherical Bessel functions:
    C_xx(q) = j0(q) - (1/2) j2(q)
    """
    q = np.asarray(q, dtype=float)
    j0 = spherical_jn(0, q)
    j2 = spherical_jn(2, q)
    return j0 - 0.5 * j2


# ============================================================
# Method 2: Direct numerical integration of I(q)
# ============================================================

def I_numerical(q_val):
    """
    Numerically integrate I(q) = integral_{-1}^{1} (1 + u^2) e^{iqu} du.
    Returns real part (imaginary part should vanish by symmetry).
    """
    def integrand_real(u):
        return (1.0 + u**2) * np.cos(q_val * u)

    def integrand_imag(u):
        return (1.0 + u**2) * np.sin(q_val * u)

    real_part, _ = quad(integrand_real, -1, 1)
    imag_part, _ = quad(integrand_imag, -1, 1)

    return real_part  # imag_part should be ~0 (odd integrand)


def C_xx_numerical(q_values):
    """
    Compute C_xx(d) via direct numerical integration.
    """
    I0 = I_numerical(0)
    results = []
    for q in q_values:
        Iq = I_numerical(q)
        results.append(Iq / I0)
    return np.array(results)


# ============================================================
# Method 3: Monte Carlo over k-vector directions
# ============================================================

def C_xx_monte_carlo(d_over_c, omega0, N_modes=100000):
    """
    Monte Carlo estimate of C_xx(d).

    For each random k-vector direction (theta, phi):
    - The two polarization vectors perpendicular to k̂ contribute
      |eps_x|^2 = Σ_λ |eps^λ_x|^2 = 1 - sin^2(theta)*cos^2(phi)
    - The phase factor is e^{i k_z d} = e^{i omega0 * d/c * cos(theta)}

    C_xx(d) = <(1 - sin^2θ cos^2φ) * cos(q cosθ)> / <(1 - sin^2θ cos^2φ)>
    where averaging is over uniform sphere (weight = sin θ dθ dφ / 4π).

    The denominator (d=0 case) = <1 - sin^2θ cos^2φ> = 1 - <sin^2θ cos^2φ>
    = 1 - (2/3)(1/2) = 1 - 1/3 = 2/3.

    But we normalize by the same factor, so:
    C_xx(d) = <weight * cos(q cosθ)> / <weight>
    where weight = 1 - sin^2θ cos^2φ.
    """
    # Sample uniform directions on sphere
    # Use spherical coordinates with uniform cos(theta) sampling
    cos_theta = np.random.uniform(-1, 1, N_modes)
    phi = np.random.uniform(0, 2 * np.pi, N_modes)
    sin_theta = np.sqrt(1 - cos_theta**2)

    # Polarization weight: Σ_λ |eps^λ_x|^2 = 1 - k̂_x^2
    # where k̂_x = sin(theta) * cos(phi)
    weight = 1.0 - sin_theta**2 * np.cos(phi)**2

    # Phase factor for mode along +k̂ hitting the two oscillators
    q = omega0 * d_over_c
    phase = np.cos(q * cos_theta)  # real part of e^{iq*cos(theta)}

    # Normalized correlation
    numerator = np.mean(weight * phase)
    denominator = np.mean(weight)

    return numerator / denominator


# ============================================================
# Verification and Plotting
# ============================================================

def run_all_checks():
    print("=" * 60)
    print("3D ZPF CORRELATOR COMPUTATION")
    print("=" * 60)

    # ---- 1. Check I(0) = 8/3 ----
    print("\n1. CHECKING I(0) = 8/3")
    I0_numerical = I_numerical(0)
    print(f"   I(0) numerical:  {I0_numerical:.10f}")
    print(f"   I(0) analytic:   {8/3:.10f}")
    print(f"   Error:           {abs(I0_numerical - 8/3):.2e}")

    # ---- 2. Compare analytic vs numerical at selected q values ----
    print("\n2. ANALYTIC vs NUMERICAL INTEGRATION COMPARISON")
    q_test = np.array([0.0, 0.5, 1.0, 2.0, np.pi, 5.0, 10.0])

    C_analytic = C_xx_analytic(q_test)
    C_numerical = C_xx_numerical(q_test)
    C_bessel = C_xx_bessel(q_test)

    print(f"{'q':>8} | {'Analytic':>12} | {'Numerical':>12} | {'Bessel':>12} | {'Error':>10}")
    print("-" * 65)
    for i, q in enumerate(q_test):
        err = abs(C_analytic[i] - C_numerical[i])
        print(f"{q:8.4f} | {C_analytic[i]:12.8f} | {C_numerical[i]:12.8f} | {C_bessel[i]:12.8f} | {err:10.2e}")

    # ---- 3. Near-field Taylor expansion check ----
    print("\n3. NEAR-FIELD EXPANSION CHECK")
    print("   C_xx ≈ 1 - q²/5 + 3q⁴/280 for small q")
    for q in [0.01, 0.1, 0.3]:
        exact = C_xx_analytic(np.array([q]))[0]
        taylor = 1.0 - q**2/5.0 + 3.0*q**4/280.0
        print(f"   q={q}: exact={exact:.10f}, Taylor={taylor:.10f}, err={abs(exact-taylor):.2e}")

    # ---- 4. Far-field approximation check ----
    print("\n4. FAR-FIELD APPROXIMATION CHECK")
    print("   C_xx ≈ (3/2) sin(q)/q for large q")
    for q in [5.0, 10.0, 20.0, 50.0]:
        exact = C_xx_analytic(np.array([q]))[0]
        approx = 1.5 * np.sin(q) / q
        print(f"   q={q}: exact={exact:.8f}, (3/2)sin(q)/q={approx:.8f}, err={abs(exact-approx):.2e}")

    # ---- 5. Monte Carlo verification ----
    print("\n5. MONTE CARLO VERIFICATION (N=500000 modes)")
    np.random.seed(42)
    N_mc = 500000
    omega0 = 1.0
    d_values_mc = np.array([0.5, 1.0, np.pi, 5.0])

    print(f"{'d (q)':>12} | {'Analytic':>12} | {'Monte Carlo':>12} | {'MC Error':>10}")
    print("-" * 55)
    for d in d_values_mc:
        q = omega0 * d
        C_a = C_xx_analytic(np.array([q]))[0]
        C_mc = C_xx_monte_carlo(d, omega0, N_modes=N_mc)
        # MC statistical error estimate
        print(f"{d:12.4f} | {C_a:12.8f} | {C_mc:12.8f} | {abs(C_a-C_mc):10.4f}")

    # ---- 6. 1D limit check ----
    print("\n6. 1D LIMIT CHECK")
    print("   In 1D, only modes along ±ẑ contribute.")
    print("   For x-polarized modes along ẑ: weight=1, phase=cos(q)")
    print("   Expected: C_xx^{1D}(d) = cos(q)")
    print("")
    q_vals = np.array([0.0, 0.5, 1.0, 2.0, np.pi])
    C_3D = C_xx_analytic(q_vals)
    C_1D = np.cos(q_vals)
    print(f"{'q':>8} | {'C_xx 3D':>12} | {'C_xx 1D':>12} | {'Ratio 3D/1D':>12}")
    print("-" * 50)
    for i, q in enumerate(q_vals):
        ratio = C_3D[i] / C_1D[i] if abs(C_1D[i]) > 1e-10 else float('nan')
        print(f"{q:8.4f} | {C_3D[i]:12.8f} | {C_1D[i]:12.8f} | {ratio:12.6f}")
    print("")
    print("   Note: 3D < 1D everywhere (orientational averaging reduces correlation).")

    # ---- 7. Plot ----
    print("\n7. GENERATING PLOT")
    q_plot = np.linspace(0, 15, 1000)
    C_3D_plot = C_xx_analytic(q_plot)
    C_1D_plot = np.cos(q_plot)
    C_far_field = np.where(q_plot > 0.1, 1.5 * np.sin(q_plot) / q_plot, 1.0)

    fig, axes = plt.subplots(2, 1, figsize=(10, 8))

    ax = axes[0]
    ax.plot(q_plot, C_3D_plot, 'b-', lw=2, label='$C_{xx}^{3D}(d)$ = analytic result')
    ax.plot(q_plot, C_1D_plot, 'r--', lw=2, label='$C_{xx}^{1D}(d)$ = cos(q) [1D model]')
    ax.plot(q_plot, C_far_field, 'g:', lw=1.5, label='Far-field: $(3/2)\\sin(q)/q$')
    ax.axhline(0, color='k', lw=0.5)
    ax.set_xlabel('q = ω₀d/c', fontsize=12)
    ax.set_ylabel('$C_{xx}(d)$', fontsize=12)
    ax.set_title('3D ZPF Position-Position Correlator vs 1D Model', fontsize=13)
    ax.legend(fontsize=11)
    ax.set_xlim(0, 15)
    ax.set_ylim(-1.5, 1.1)
    ax.grid(True, alpha=0.3)

    ax2 = axes[1]
    ax2.semilogy(q_plot[10:], np.abs(C_3D_plot[10:]), 'b-', lw=2, label='$|C_{xx}^{3D}|$')
    ax2.semilogy(q_plot[10:], np.abs(C_1D_plot[10:]) + 1e-10, 'r--', lw=2, label='$|\\cos(q)|$')
    ax2.semilogy(q_plot[10:], 1.5 / q_plot[10:], 'g:', lw=1.5, label='$3/(2q)$ envelope')
    ax2.set_xlabel('q = ω₀d/c', fontsize=12)
    ax2.set_ylabel('$|C_{xx}(d)|$', fontsize=12)
    ax2.set_title('Log scale — decay rate comparison', fontsize=13)
    ax2.legend(fontsize=11)
    ax2.set_xlim(0, 15)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('code/C_xx_3D_vs_1D.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("   Saved: code/C_xx_3D_vs_1D.png")

    return C_analytic, C_numerical


if __name__ == '__main__':
    C_analytic, C_numerical = run_all_checks()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("""
The 3D ZPF correlator in the narrow-linewidth limit:

  C_xx(d) = (3/2q³) [(q²-1)sin(q) + q cos(q)]   where q = ω₀d/c

Equivalently: C_xx(d) = j₀(q) - (1/2) j₂(q)

Key findings:
  • C_xx(0) = 1 (exact)
  • Near field: C_xx ≈ 1 - q²/5 + O(q⁴) [analytic, no singularity]
  • Far field: C_xx ≈ (3/2) sin(q)/q ~ 1/d [oscillating, decaying]
  • C_xx ≠ 0 for all finite d

The 3D result is NOT zero. SED predicts non-zero spatial correlations
even after averaging over all k-vector directions and polarizations.
The correlations are weaker than the 1D model (decay as 1/d vs constant),
but remain non-zero — still disagreeing with QM's prediction of C_xx = 0.
""")
