"""
photon_scattering.py
--------------------
EFT-hedron positivity bounds for photon-photon scattering.

The low-energy photon-photon EFT (below electron mass) is the Euler-Heisenberg Lagrangian:

L = -(1/4) F^2 + (alpha1/(4*m_e^4)) (F_{mu nu} F^{mu nu})^2
                + (alpha2/(4*m_e^4)) (F_{mu nu} F~^{mu nu})^2
                + higher-derivative terms

where alpha1, alpha2 are the EFT coefficients.

For QED (from Euler-Heisenberg):
    alpha1 = (2 alpha_QED^2)/(45 m_e^4)  * (1/4)^2 * something...

The standard form (matching to helicity amplitudes):
    L_EH ∝ a (F_munu F^munu)^2 + b (F_munu F~^munu)^2

where a and b from QED at 1-loop are (in conventional normalization):
    a_EH = 4 * (alpha/m_e^4) * (1/180) * (1/4)
    b_EH = 7 * (alpha/m_e^4) * (1/180) * (1/4)

The photon-photon helicity amplitudes:
    M(++,++) = M(--,--): forward parallel-polarization
    M(+-,+-): forward cross-polarization
    M(++,--): helicity-flip

The EFT-hedron bounds from positivity (Arkani-Hamed et al. 2021):
    For photons, the relevant combination is related to:
    sum over helicities of (Im A(helicities)) >= 0

The simplest bounds from Euler-Heisenberg:
    (1) a >= 0  (positivity of Im amplitude for (++) -> (++) scattering)
    (2) b >= 0  (positivity for (+-)  -> (+-) )
    (3) 4a + 7b >= 0 or a + b >= 0 depending on convention

Actually, for photon scattering the relevant constraint is on the forward amplitudes.
The photon-photon amplitude in terms of helicities h1, h2 -> h3, h4:
    M^{h1 h2 h3 h4}(s,t)

The EFT-hedron bounds translate to:
    At leading order in the EFT, define coefficients c_1, c_2 in:
    M^{++,++}(s,t) = c_1 * s^2 + ...
    M^{+-,+-}(s,t) = c_2 * s^2 + ...

The optical theorem bounds: Im M^{++,++}(s,0) >= 0, Im M^{+-,+-}(s,0) >= 0

And cross-polarization bounds from positivity of the full helicity matrix.

For the Euler-Heisenberg Lagrangian, the helicity amplitudes are:
    M(++,++) ~ 16 * (alpha1 + alpha2) * s^2  [from F^4 and F~^4 terms]
    M(+-,+-) ~ 16 * alpha1 * s^2              [from F^4 only, F~^4 cancels]
    M(++,--) ~ 16 * (alpha1 - alpha2) * s^2  [helicity flip]

The EFT-hedron bounds (physical constraints for UV completability):
    alpha1 >= 0
    alpha2 >= 0
    alpha1 + alpha2 >= 0   (automatically satisfied if both >= 0)

For the QED Euler-Heisenberg result:
    alpha1/alpha2 = 4/7 (from 1-loop electron box)

This satisfies all bounds: both positive.

References:
    - Euler-Heisenberg (1936)
    - Adams et al. (2006) for the general method
    - Arkani-Hamed et al. arXiv:2012.15849 Sec. 4 for photons
    - Caron-Huot & Van Duong (2020) arXiv:2005.03571 for detailed photon bounds
"""

import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))


def euler_heisenberg_coefficients(alpha_em=1/137.036, m_e=0.511e-3):
    """
    Euler-Heisenberg Lagrangian coefficients in GeV units.

    L_EH = -(1/4) F^2 + c1 (F F)^2 + c2 (F F~)^2

    From QED 1-loop:
        c1 = 2 alpha_em^2 / (45 m_e^4)
        c2 = 7 alpha_em^2 / (90 m_e^4)   [note: 7/2 ratio]

    So c2/c1 = (7/90)/(2/45) = (7/90)*(45/2) = 7/4

    In some conventions, the standard EH Lagrangian is:
        L = (alpha_em^2 / (90 m_e^4)) [4 (F^2)^2 + 7 (F F~)^2]
    giving coefficients 4:7 ratio.
    """
    prefactor = alpha_em**2 / (90 * m_e**4)  # units: GeV^{-4}
    c1 = 4 * prefactor   # coefficient of (F^2)^2
    c2 = 7 * prefactor   # coefficient of (F~F)^2
    return c1, c2


def helicity_amplitudes_EH(s, alpha1, alpha2):
    """
    Leading-order photon-photon helicity amplitudes from Euler-Heisenberg.

    For massless photons (s,t,u with s+t+u=0):
    At leading order (s^2 dependence):

    M(++,++) = 16 * (alpha1 + alpha2) * s^2
    M(+-,+-) = 16 * alpha1 * (s^2 + 4st + t^2)  [simplification at t->0: 16 alpha1 s^2]
    M(++,--) = 16 * (alpha1 - alpha2) * s^2       [helicity flip]

    In the forward limit t=0 (u=-s):
    M(++,++)|_{t=0} = 16 (alpha1 + alpha2) s^2
    M(+-,+-)|_{t=0} = 16 alpha1 s^2
    M(++,--)|_{t=0} = 16 (alpha1 - alpha2) s^2

    Returns (M_pp_pp, M_pm_pm, M_pp_mm) at t=0 for the s^2 coefficient
    """
    M_pp_pp = 16 * (alpha1 + alpha2)  # coefficient of s^2
    M_pm_pm = 16 * alpha1
    M_pp_mm = 16 * (alpha1 - alpha2)
    return M_pp_pp, M_pm_pm, M_pp_mm


def positivity_bounds_photon(alpha1, alpha2):
    """
    Check EFT-hedron positivity bounds for photon-photon scattering.

    From forward-limit unitarity (Im M(s,0) >= 0):
    1. Im M(++,++) >= 0  ->  alpha1 + alpha2 >= 0
    2. Im M(+-,+-) >= 0  ->  alpha1 >= 0
    3. Helicity sum: full positivity matrix must be PSD

    The full positivity matrix at leading order in s^2 is:
    P = | M(++,++) M(++,+-) M(++,--) |
        | M(+-,++) M(+-,+-) M(+-,--) |
        | M(--,++) M(--,+-) M(--,--) |

    For the diagonal elements (forward scattering):
    P_{++,++} = (alpha1 + alpha2)  # coefficient x 16
    P_{+-,+-} = alpha1             # coefficient x 16
    P_{--,--} = (alpha1 + alpha2)  # same as ++ by CPT

    PSD of this matrix requires:
    (a) P_{++,++} >= 0  ->  alpha1 + alpha2 >= 0
    (b) P_{+-,+-} >= 0  ->  alpha1 >= 0
    (c) det(2x2 submatrix) = P_{++,++} * P_{--,--} - |P_{++,--}|^2 >= 0
        -> (alpha1+alpha2)^2 - (alpha1-alpha2)^2 = 4*alpha1*alpha2 >= 0
        -> alpha2 >= 0  (given alpha1 >= 0)

    So the complete set of leading-order constraints is:
    alpha1 >= 0, alpha2 >= 0
    """
    bounds = {}

    # Bound 1: alpha1 + alpha2 >= 0
    bounds['alpha1_plus_alpha2'] = {
        'value': alpha1 + alpha2,
        'satisfied': (alpha1 + alpha2) >= 0,
        'formula': 'alpha1 + alpha2 >= 0 (from M(++,++) >= 0)'
    }

    # Bound 2: alpha1 >= 0
    bounds['alpha1'] = {
        'value': alpha1,
        'satisfied': alpha1 >= 0,
        'formula': 'alpha1 >= 0 (from M(+-,+-) >= 0)'
    }

    # Bound 3: alpha2 >= 0
    bounds['alpha2'] = {
        'value': alpha2,
        'satisfied': alpha2 >= 0,
        'formula': 'alpha2 >= 0 (from positivity matrix PSD)'
    }

    # Bound 4: Full PSD condition - the 4*alpha1*alpha2 >= 0 reduces to above
    det_22 = 4 * alpha1 * alpha2  # should be >= 0
    bounds['det_2x2'] = {
        'value': det_22,
        'satisfied': det_22 >= 0,
        'formula': '4*alpha1*alpha2 >= 0 (from 2x2 submatrix PSD)'
    }

    return bounds


def apply_to_euler_heisenberg():
    """
    Apply positivity bounds to the QED Euler-Heisenberg result.
    """
    alpha_em = 1/137.036
    m_e = 0.511e-3  # GeV
    c1, c2 = euler_heisenberg_coefficients(alpha_em, m_e)

    # In the EH normalization, alpha1 = c1, alpha2 = c2
    alpha1 = c1
    alpha2 = c2

    print("Euler-Heisenberg coefficients from QED 1-loop:")
    print(f"  alpha1 = c1 = {alpha1:.4e} GeV^{{-4}}")
    print(f"  alpha2 = c2 = {alpha2:.4e} GeV^{{-4}}")
    print(f"  Ratio alpha2/alpha1 = {alpha2/alpha1:.4f}  (expect 7/4 = {7/4:.4f})")

    bounds = positivity_bounds_photon(alpha1, alpha2)

    print("\nPositivity bounds check for Euler-Heisenberg QED:")
    all_satisfied = True
    for name, info in bounds.items():
        status = "✓ SATISFIED" if info['satisfied'] else "✗ VIOLATED"
        print(f"  {info['formula']}")
        print(f"    value = {info['value']:.4e}  {status}")
        if not info['satisfied']:
            all_satisfied = False

    print(f"\n  Overall: {'ALL BOUNDS SATISFIED' if all_satisfied else 'VIOLATION FOUND'}")
    print(f"  (Expected: satisfied — QED is UV complete)")

    return alpha1, alpha2, bounds


def bounds_for_hypothetical_eft():
    """
    Check what happens for various hypothetical EFT coefficients.
    Some satisfy the bounds (UV-completable), some don't.
    """
    test_cases = [
        ("QED Euler-Heisenberg", 4.0, 7.0),        # satisfies all bounds
        ("Both positive, equal", 1.0, 1.0),          # satisfies
        ("alpha1 > 0, alpha2 < 0 (small)", 1.0, -0.5),  # violates alpha2 >= 0
        ("alpha1 < 0, alpha2 > 0", -1.0, 2.0),      # violates alpha1 >= 0
        ("Both negative", -1.0, -1.0),               # violates all
        ("alpha1 > 0, alpha2 = 0", 1.0, 0.0),        # marginally satisfies
        ("Large alpha2, small alpha1", 0.1, 10.0),   # satisfies
    ]

    print("\nHypothetical EFT coefficients — positivity scan:")
    print(f"  {'Theory':40s}  {'a1':>8}  {'a2':>8}  {'a1>=0':>6}  {'a2>=0':>6}  {'a1+a2>=0':>9}  {'4a1a2>=0':>9}")
    print("  " + "-" * 100)

    for name, a1, a2 in test_cases:
        b = positivity_bounds_photon(a1, a2)
        ok1 = "✓" if b['alpha1']['satisfied'] else "✗"
        ok2 = "✓" if b['alpha2']['satisfied'] else "✗"
        ok3 = "✓" if b['alpha1_plus_alpha2']['satisfied'] else "✗"
        ok4 = "✓" if b['det_2x2']['satisfied'] else "✗"
        print(f"  {name:40s}  {a1:8.2f}  {a2:8.2f}  {ok1:>6}  {ok2:>6}  {ok3:>9}  {ok4:>9}")


def gravity_photon_bounds():
    """
    EFT-hedron bounds for graviton-photon scattering (minimal coupling + GR corrections).

    From the graviton-photon EFT at leading order, the relevant operators are:
    L = -(1/4) F^2 + (1/M_P^2) [c1 R_abcd F^ab F^cd + c2 R F^2 + c3 R^ab F_ac F_b^c]

    The positivity bound (from unitarity in graviton-photon scattering):
    c1 >= 0 (from dispersion relation for graviton-photon elastic amplitude)

    Reference: Arkani-Hamed et al. (2021), and Caron-Huot, Van Duong (2020).

    Physical meaning: Any graviton-photon EFT arising from a UV-complete theory
    must have c1 >= 0. This constrains quantum gravity corrections to electromagnetism.
    """
    print("\nGraviton-photon EFT bounds (gravitational corrections to photon propagation):")
    print("  Operator basis: R_abcd F^ab F^cd (coefficient c1)")
    print("                  R F^2             (coefficient c2)")
    print("                  R^ab F_ac F_b^c   (coefficient c3)")
    print()
    print("  EFT-hedron positivity constraint (leading order):")
    print("    c1 >= 0  [from Im M(graviton+photon -> graviton+photon) >= 0]")
    print()
    print("  Physical interpretation:")
    print("    c1 < 0 would mean photons are 'repelled' by curvature in a way")
    print("    inconsistent with any UV completion (no such quantum gravity exists).")
    print()
    print("  Known values from string theory (D-brane compactifications):")
    print("    c1 > 0 in all known examples (consistent with bound)")
    print("    The bound is non-trivial: general higher-dimensional gravity")
    print("    can have c1 of either sign until truncated to 4D")


if __name__ == "__main__":
    print("=" * 70)
    print("PHOTON-PHOTON SCATTERING — EFT-Hedron Bounds")
    print("Reference: Arkani-Hamed et al. arXiv:2012.15849 (2021)")
    print("           Caron-Huot & Van Duong arXiv:2005.03571 (2020)")
    print("=" * 70)

    # Main calculation: Euler-Heisenberg
    alpha1_eh, alpha2_eh, bounds_eh = apply_to_euler_heisenberg()

    # Scan over hypothetical EFTs
    bounds_for_hypothetical_eft()

    # Graviton-photon bounds
    gravity_photon_bounds()

    print("\n" + "=" * 70)
    print("SUMMARY:")
    print("  QED Euler-Heisenberg: satisfies all EFT-hedron positivity bounds")
    print("  Ratio alpha2/alpha1 = 7/4 (from 1-loop electron box)")
    print("  Constraint: alpha1 >= 0, alpha2 >= 0, 4*alpha1*alpha2 >= 0")
    print("  Physical: QED is UV-complete, so bounds are automatically satisfied")
    print("  Non-trivial: theories with alpha1 < 0 or alpha2 < 0 are EXCLUDED")
    print("               from having any UV completion")
