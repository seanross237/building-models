"""
Cross-check: BCFW [2-,4+> shift for A6(1-,2-,3-,4+,5+,6+).

|2^> = |2> + z|4>,   |4^] = |4] - z|2]

Four channels (2^ and 4^ on opposite sides):
  Ch1: {2^,3}    | {4^,5,6,1} -- both left neg-hel -> 0
  Ch2: {2^,1}    | {3,4^,5,6} -- both left neg-hel -> 0
  Ch3: {2^,1,6}  | {3,4^,5}   -- MHV4 x MHV4 -> NON-ZERO
  Ch4: {2^,1,6,5}| {3,4^}     -- MHV5 x MHV3 -> NON-ZERO

Expected: Ch3+Ch4 == A6^NMHV from [1,2> shift.
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../exploration-001/code'))
sys.path.insert(0, os.path.dirname(__file__))

from spinor_helicity import Particle, ab, sb, spinors_from_momentum
from kinematics_6pt import make_6pt_kinematics, validate_6pt
from bcfw_6pt import (A3_MHV, A_MHV, mom_sq, spinor_outer_4vec,
                      dot4, particle_from_neg_mom, A6_NMHV_BCFW)


def find_pole_24(particles, left_labels):
    """[2,4> shift: q = lambda_4 ⊗ lambda_tilde_2"""
    p = particles
    P0 = sum(p[i-1].four_momentum for i in left_labels)
    P0_sq = mom_sq(P0)
    q = spinor_outer_4vec(p[3].lam, p[1].lam_tilde)  # lambda_4 ⊗ lambda_tilde_2
    denom = 2.0 * dot4(P0, q)
    if abs(denom) < 1e-14:
        return None, None
    return -P0_sq / denom, P0_sq


def shifted_24(particles, z):
    p = particles
    p2h = Particle(2, p[1].lam + z * p[3].lam,  p[1].lam_tilde.copy())
    p4h = Particle(4, p[3].lam.copy(), p[3].lam_tilde - z * p[1].lam_tilde)
    return p2h, p4h


def channel3_24(particles, verbose=False):
    """
    {2^,1,6} | {3,4^,5}: A4^MHV(K+,2^-,1-,6+) x A4^MHV((-K)-,3-,4^+,5+)

    Cyclic order of left:  K, 2^, 1, 6   (going backward: 6->1->2^->K)
      Actually: left set {2,1,6}. Original order of left going 2->1->6 backward.
      Color order with K: K, 6, 1, 2^  (K at boundary, then cycle: 6,1,2)
    Cyclic order of right: (-K), 3, 4^, 5  (K at boundary, then 3,4^,5)
    """
    p = particles
    z_star, P0_sq = find_pole_24(p, [2, 1, 6])
    if z_star is None: return 0.0

    p2h, p4h = shifted_24(p, z_star)
    K_vec = p2h.four_momentum + p[0].four_momentum + p[5].four_momentum
    K  = spinors_from_momentum(K_vec,  label=97)
    mK = particle_from_neg_mom(K_vec, label=96)

    # Left A4^MHV(K+, 6+, 1-, 2^-)
    # Cyclic order: K(pos0,+), 6(pos1,+), 1(pos2,-), 2^(pos3,-)
    left_parts = [K, p[5], p[0], p2h]
    A_L = A_MHV(left_parts, 2, 3)   # neg-hel at pos 2 (p[0]=particle1) and pos 3 (p2h)

    # Right A4^MHV((-K)-, 3-, 4^+, 5+)
    # Cyclic order: (-K)(pos0,-), 3(pos1,-), 4^(pos2,+), 5(pos3,+)
    right_parts = [mK, p[2], p4h, p[4]]
    A_R = A_MHV(right_parts, 0, 1)  # neg-hel at pos 0 (-K) and pos 1 (particle3)

    if verbose:
        print(f"    z* = {z_star:.6f}, K^2={mom_sq(K_vec):.2e}")
        print(f"    A_L = {A_L:.8f}, A_R = {A_R:.8f}, P^2 = {P0_sq:.8f}")

    return A_L * A_R / P0_sq


def channel4_24(particles, verbose=False):
    """
    {2^,1,6,5} | {3,4^}: A5^MHV x A3^MHV

    Left: A5^MHV(K+,5+,6+,1-,2^-)
      Cyclic order: K(pos0,+), 5(pos1,+), 6(pos2,+), 1(pos3,-), 2^(pos4,-)
    Right: A3^MHV((-K)-,3-,4^+)
      Cyclic order: (-K)(pos0,-), 3(pos1,-), 4^(pos2,+)
    """
    p = particles
    z_star, P0_sq = find_pole_24(p, [2, 1, 6, 5])
    if z_star is None: return 0.0

    p2h, p4h = shifted_24(p, z_star)
    K_vec = p2h.four_momentum + p[0].four_momentum + p[5].four_momentum + p[4].four_momentum
    K  = spinors_from_momentum(K_vec,  label=97)
    mK = particle_from_neg_mom(K_vec, label=96)

    # Left A5^MHV: K+, 5+, 6+, 1-, 2^-
    # Cyclic: K(0), 5(1), 6(2), 1(3), 2^(4)  [going backward from 2^: 2^->1->6->5->K]
    left_parts = [K, p[4], p[5], p[0], p2h]
    A_L = A_MHV(left_parts, 3, 4)   # neg-hel at pos 3 (1) and pos 4 (2^)

    # Right A3^MHV: (-K)-, 3-, 4^+
    A_R = A3_MHV(mK, p[2], p4h)    # MHV((-K)-, 3-, 4^+)

    if verbose:
        print(f"    z* = {z_star:.6f}, K^2={mom_sq(K_vec):.2e}")
        print(f"    A_L = {A_L:.8f}, A_R = {A_R:.8f}, P^2 = {P0_sq:.8f}")

    return A_L * A_R / P0_sq


def A6_NMHV_BCFW_24(particles, verbose=False):
    """[2,4> shift: only Ch3 and Ch4 contribute."""
    if verbose: print("  [2,4> Ch3:")
    C3 = channel3_24(particles, verbose=verbose)
    if verbose: print("  [2,4> Ch4:")
    C4 = channel4_24(particles, verbose=verbose)
    return C3 + C4, (C3, C4)


if __name__ == "__main__":
    print("=" * 70)
    print("CROSS-CHECK: [2,4> vs [1,2> BCFW")
    print("=" * 70)

    all_ok = True
    for seed in [42, 137, 999, 7, 1234, 5678]:
        parts = make_6pt_kinematics(seed=seed)

        A_12, (C1, C2, C3) = A6_NMHV_BCFW(parts, verbose=False)
        A_24, (D3, D4) = A6_NMHV_BCFW_24(parts, verbose=(seed==42))

        ratio = A_24 / A_12 if abs(A_12) > 1e-10 else float('nan')
        err = abs(ratio - 1) if not np.isnan(ratio) else float('nan')
        ok = err < 1e-6 if not np.isnan(err) else False
        if not ok: all_ok = False

        print(f"\nSeed {seed:4d}:")
        print(f"  [1,2>]: C1={C1:.6f}  C2={C2:.6f}  Total={A_12:.6f}")
        print(f"  [2,4>]: D3={D3:.6f}  D4={D4:.6f}  Total={A_24:.6f}")
        if not np.isnan(ratio):
            print(f"  Ratio [2,4>/[1,2>] = {ratio:.8f}  |ratio-1| = {err:.2e}  {'OK' if ok else 'FAIL'}")

    print(f"\n{'ALL CROSS-CHECKS PASSED' if all_ok else 'SOME FAILED'}")
