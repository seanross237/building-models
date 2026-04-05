"""
6-Point MHV Amplitude — Parke-Taylor Baseline

A₆^MHV(1⁻,2⁻,3⁻,4⁺,5⁺,6⁺) = ⟨12⟩⁴ / (⟨12⟩⟨23⟩⟨34⟩⟨45⟩⟨56⟩⟨61⟩)

Wait — Parke-Taylor for (1⁻,2⁻,3⁻,4⁺,5⁺,6⁺) is not a pure MHV amplitude!
MHV = exactly 2 negative helicities. NMHV = exactly 3 negative helicities.

So the helicity configuration (1⁻,2⁻,3⁻,4⁺,5⁺,6⁺) IS the NMHV case.

The MHV "baseline" in the NMHV decomposition is:
  A₆^NMHV = A₆^MHV × F_NMHV

where the "A₆^MHV" factor can be taken as ANY MHV amplitude at 6 points.
Conventionally we use the MHV amplitude with the same external momenta but
different helicities, e.g. A₆^MHV(1⁻,2⁻,3⁺,4⁺,5⁺,6⁺):

  A₆^MHV(i⁻,j⁻) = ⟨ij⟩⁴ / (⟨12⟩⟨23⟩⟨34⟩⟨45⟩⟨56⟩⟨61⟩)

The NMHV/MHV ratio is a function of R-invariants.

For the BCFW computation of A₆^NMHV, we compute it directly (not as a ratio).
This script computes all MHV amplitudes A₆(i⁻,j⁻) as cross-checks.
"""

import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../exploration-001/code'))
sys.path.insert(0, os.path.dirname(__file__))

from spinor_helicity import ab, sb
from kinematics_6pt import make_6pt_kinematics, validate_6pt


def parke_taylor_6pt_mhv(particles, i_minus, j_minus):
    """Parke-Taylor formula for A₆^MHV with negative helicities at positions i,j (1-indexed).

    A₆^MHV = ⟨ij⟩⁴ / (⟨12⟩⟨23⟩⟨34⟩⟨45⟩⟨56⟩⟨61⟩)

    Color-ordered, all-outgoing convention.
    """
    n = 6
    p = particles
    i = i_minus - 1  # 0-indexed
    j = j_minus - 1

    numerator = ab(p[i], p[j])**4

    # Cyclic product ⟨12⟩⟨23⟩⟨34⟩⟨45⟩⟨56⟩⟨61⟩
    denom = 1.0
    for k in range(n):
        denom *= ab(p[k], p[(k+1) % n])

    return numerator / denom


def compute_all_mhv_6pt(particles, verbose=True):
    """Compute all C(6,2)=15 MHV amplitudes at 6 points."""
    n = 6
    results = {}
    if verbose:
        print("All 6-point MHV amplitudes A₆(i⁻,j⁻):")
        print("-" * 50)

    for i in range(1, n+1):
        for j in range(i+1, n+1):
            A = parke_taylor_6pt_mhv(particles, i, j)
            results[(i,j)] = A
            if verbose:
                print(f"  A₆({i}⁻,{j}⁻) = {A.real:+.8f} {A.imag:+.8f}i  "
                      f"  |A| = {abs(A):.6f}")

    return results


if __name__ == "__main__":
    print("=" * 60)
    print("6-POINT MHV AMPLITUDES (PARKE-TAYLOR BASELINE)")
    print("=" * 60)

    for seed in [42, 137, 999]:
        print(f"\n--- Seed = {seed} ---")
        parts = make_6pt_kinematics(seed=seed)
        mom_err, mass_err = validate_6pt(parts, verbose=False)
        print(f"Kinematics: mom_err={mom_err:.2e}, mass_err={mass_err:.2e}")
        results = compute_all_mhv_6pt(parts, verbose=True)
