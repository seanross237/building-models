"""
partial_waves.py
----------------
Spectral density utilities for 2->2 scalar scattering.

PHYSICAL SETUP:
For a massive scalar EFT with UV cutoff scale M (particle mass), the spectral
density Im M(s, t=0) is supported ONLY for s > s_threshold = (2m)^2 where m
is the lightest exchanged particle. Below threshold: Im M = 0.

The dispersion relation for Wilson coefficients:
    g_{n,0} = (1/pi) * integral_{s_thr}^{inf} ds Im M(s, 0) / s^{n+1}   [n >= 2]

Since Im M(s, 0) >= 0 (optical theorem) for s > s_thr, all g_{n,0} >= 0.

MODELS:
1. Narrow-width resonance: Im M ~ delta(s - M_res^2)
2. Breit-Wigner (thresholded above s_thr): smooth resonance profile
3. Power-law continuum: Im M = norm * (s - s_thr)^alpha for s > s_thr
"""

import numpy as np
from scipy import integrate


# ---------------------------------------------------------------------------
# Core spectral density models
# ---------------------------------------------------------------------------

def spectral_density_narrow_resonance(s, M_res, width_ratio=0.01, coupling=1.0):
    """
    Narrow Breit-Wigner resonance STRICTLY ABOVE threshold s_thr = (0.8 * M_res)^2.

    Im M(s, 0) = 16 * pi^2 * coupling^2 * delta_approx(s - M_res^2)

    Approximated as a narrow Lorentzian: Gamma = width_ratio * M_res.
    The function is exactly zero for s < s_thr.

    Parameters
    ----------
    s : array_like
        Mandelstam s
    M_res : float
        Resonance mass (s_pole = M_res^2)
    width_ratio : float
        Gamma / M_res
    coupling : float
        Coupling strength (overall normalization)

    Returns
    -------
    array : Im M(s, 0)
    """
    s = np.asarray(s, dtype=float)
    Gamma = width_ratio * M_res
    # Set threshold just below the resonance: s_thr = (M_res - 5*Gamma)^2
    # This correctly represents a physical resonance at M_res where the spectral
    # density is essentially zero for s << M_res^2
    s_thr = max(0.0, M_res - 5 * Gamma)**2

    result = np.zeros_like(s)
    above = s > s_thr
    if np.any(above):
        sa = s[above]
        num = coupling**2 * M_res * Gamma
        denom = (M_res**2 - sa)**2 + (M_res * Gamma)**2
        result[above] = 16 * np.pi * num / denom

    return result


def spectral_density_power_law(s, M_threshold, alpha=1.0, norm=1.0):
    """
    Power-law spectral density above threshold:
        Im M(s, 0) = norm * (s/M_threshold^2 - 1)^alpha * theta(s - M_threshold^2)

    This models a broad continuum above the threshold.
    Clearly positive for s > M_threshold^2.

    Parameters
    ----------
    s : array_like
    M_threshold : float
        Threshold mass (integration starts at M_threshold^2)
    alpha : float
        Power-law exponent (default 1)
    norm : float
        Overall normalization
    """
    s = np.asarray(s, dtype=float)
    s_thr = M_threshold**2
    result = np.zeros_like(s)
    above = s > s_thr
    if np.any(above):
        result[above] = norm * (s[above] / s_thr - 1)**alpha
    return result


def spectral_density_multi_resonance(s, resonances):
    """
    Sum of narrow resonances.

    Parameters
    ----------
    s : array_like
    resonances : list of (M_res, width_ratio, coupling) tuples

    Returns
    -------
    array : Im M(s, 0) from sum of resonances
    """
    s = np.asarray(s, dtype=float)
    result = np.zeros_like(s)
    for M_res, width_ratio, coupling in resonances:
        result += spectral_density_narrow_resonance(s, M_res, width_ratio, coupling)
    return result


# ---------------------------------------------------------------------------
# Wilson coefficient computation
# ---------------------------------------------------------------------------

def compute_wilson_coefficients(spectral_fn, s_threshold, n_max=8, **kwargs):
    """
    Compute Wilson coefficients via the dispersion relation:
        g_{n,0} = (1/pi) * integral_{s_thr}^{inf} ds Im M(s, 0) / s^{n+1}

    Parameters
    ----------
    spectral_fn : callable
        spectral_fn(s_array, **kwargs) -> Im M(s, 0) (should be zero below s_threshold)
    s_threshold : float
        Lower integration limit (s_thr = threshold in units of s = energy^2)
    n_max : int
        Maximum n to compute
    kwargs :
        Passed to spectral_fn

    Returns
    -------
    dict : {n: g_{n,0}} for n in 2..n_max
    """
    g = {}

    for n in range(2, n_max + 1):
        def integrand(s_val, n=n):
            rho = spectral_fn(np.array([s_val]), **kwargs)
            return float(rho[0]) / s_val**(n + 1)

        # Adaptive integration with high accuracy near the threshold
        result, error = integrate.quad(
            integrand,
            s_threshold * 1.001,
            np.inf,
            limit=500,
            epsabs=0.0,
            epsrel=1e-8
        )
        g[n] = result / np.pi

    return g


def analytic_delta_resonance(M_res, coupling=1.0):
    """
    Analytic result for a single delta-function resonance:
        Im M(s, 0) = 16 * pi^2 * coupling^2 * delta(s - M_res^2)

    Integration formula:
        g_{n,0} = (1/pi) * 16 * pi^2 * coupling^2 / M_res^{2(n+1)}
                = 16 * pi * coupling^2 / M_res^{2(n+1)}

    Hankel ratio:
        g_{n,0} / g_{n-1,0} = 1 / M_res^2

    Key property: SATURATES the 2x2 Hankel bound:
        g_{2,0} * g_{4,0} = g_{3,0}^2  (equality, not strict inequality)
    """
    g = {}
    for n in range(2, 9):
        g[n] = 16 * np.pi * coupling**2 / M_res**(2 * (n + 1))
    return g


# ---------------------------------------------------------------------------
# Verification and self-consistency checks
# ---------------------------------------------------------------------------

def verify_spectral_density(spectral_fn, s_threshold, n_samples=1000, **kwargs):
    """
    Quick checks:
    1. Im M(s, 0) >= 0 for all s (optical theorem)
    2. Im M(s, 0) = 0 for s < s_threshold
    """
    s_below = np.linspace(s_threshold * 0.1, s_threshold * 0.999, 100)
    s_above = np.linspace(s_threshold * 1.001, s_threshold * 20, n_samples)

    rho_below = spectral_fn(s_below, **kwargs)
    rho_above = spectral_fn(s_above, **kwargs)

    all_zero_below = np.all(rho_below == 0)
    all_positive_above = np.all(rho_above >= 0)

    return {
        'zero_below_threshold': all_zero_below,
        'positive_above_threshold': all_positive_above,
        'max_negative': float(np.min(rho_above)) if len(rho_above) > 0 else 0,
    }


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 65)
    print("Spectral Densities and Partial Waves — Demo")
    print("=" * 65)

    # ---------- Single resonance at M_res = 2, threshold at (M_res/2)^2 ----------
    M_res = 2.0
    s_thr = (M_res / 2)**2  # = 1.0

    print(f"\nSingle resonance: M_res = {M_res}, threshold s_thr = {s_thr}")

    def single_res(s, **kw):
        return spectral_density_narrow_resonance(s, M_res, width_ratio=0.01, coupling=1.0)

    # Verify spectral density
    check = verify_spectral_density(single_res, s_thr)
    print(f"  Zero below threshold: {check['zero_below_threshold']} ✓")
    print(f"  Positive above threshold: {check['positive_above_threshold']} ✓")

    # Numerical Wilson coefficients
    g_num = compute_wilson_coefficients(single_res, s_thr, n_max=8)

    # Analytic delta-function prediction
    g_ana = analytic_delta_resonance(M_res, coupling=1.0)

    print(f"\nWilson coefficients g_{{n,0}} — numerical vs analytic (delta-function limit):")
    print(f"  {'n':>4}  {'g_num':>14}  {'g_ana':>14}  {'ratio':>8}")
    for n in range(2, 9):
        ratio = g_num[n] / g_ana[n]
        print(f"  {n:4d}  {g_num[n]:14.6e}  {g_ana[n]:14.6e}  {ratio:8.4f}")

    # Check all positive
    print(f"\nAll g_{{n,0}} > 0: {all(v > 0 for v in g_num.values())} [UV complete]")

    # Check Hankel ratios approach 1/M_res^2
    print(f"\nHankel ratios g_{{n,0}}/g_{{n-1,0}} (expect 1/M_res^2 = {1/M_res**2:.4f}):")
    for n in range(3, 8):
        ratio = g_num[n] / g_num[n-1]
        print(f"  g_{{{n}}}/g_{{{n-1}}} = {ratio:.6f}  (error = {abs(ratio - 1/M_res**2)/abs(1/M_res**2)*100:.2f}%)")

    # ---------- Power-law continuum ----------
    print(f"\nPower-law continuum: threshold M_thr = {M_res}, alpha = 1.5")

    def power_fn(s, **kw):
        return spectral_density_power_law(s, M_res, alpha=1.5, norm=1.0)

    g_pl = compute_wilson_coefficients(power_fn, M_res**2, n_max=6)
    print(f"  All positive: {all(v > 0 for v in g_pl.values())} ✓")
    for n in range(2, 7):
        print(f"  g_{{{n},0}} = {g_pl[n]:.4e}")

    print("\n[DONE] partial_waves.py")
