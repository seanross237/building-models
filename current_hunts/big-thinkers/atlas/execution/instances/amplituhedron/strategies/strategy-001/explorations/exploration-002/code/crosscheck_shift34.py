"""
Cross-check: BCFW with [3,4> shift for A6(1-,2-,3-,4+,5+,6+).

With [3,4>: |3^> = |3> + z|4>,  |4^] = |4] - z|3]

Analysis of 3 channels:
  Ch A: {3^,2} | {4^,5,6,1}  -> NONZERO: A3^MHV x A5^MHV
  Ch B: {3^,2,1} | {4^,5,6}  -> ZERO: left has 3 neg-helicity gluons at n=4 -> 0
  Ch C: {3^,2,1,6} | {4^,5}  -> ZERO: right A3 has [4^5]=0 at pole -> 0

So A6^NMHV = Ch_A only.  Compare with [1,2>] = C1 + C2 + 0.
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../exploration-001/code'))
sys.path.insert(0, os.path.dirname(__file__))

from spinor_helicity import Particle, ab, sb, spinors_from_momentum
from kinematics_6pt import make_6pt_kinematics, validate_6pt
from bcfw_6pt import (A3_MHV, A_MHV, mom_sq, spinor_outer_4vec,
                      dot4, particle_from_neg_mom, A6_NMHV_BCFW)


def find_pole_shift34(particles, left_labels):
    """[3,4> shift: q = lambda_4 ⊗ lambda_tilde_3 (0-indexed: p[3].lam, p[2].lam_tilde)"""
    p = particles
    P0 = sum(p[i-1].four_momentum for i in left_labels)
    P0_sq = mom_sq(P0)
    q = spinor_outer_4vec(p[3].lam, p[2].lam_tilde)   # lambda_4 ⊗ lambda_tilde_3
    denom = 2.0 * dot4(P0, q)
    if abs(denom) < 1e-14:
        return None, None
    z_star = -P0_sq / denom
    return z_star, P0_sq


def shifted_particles_34(particles, z):
    """[3,4> shift at complex z."""
    p = particles
    lam3_hat    = p[2].lam + z * p[3].lam
    ltilde4_hat = p[3].lam_tilde - z * p[2].lam_tilde
    p3h = Particle(3, lam3_hat, p[2].lam_tilde.copy())
    p4h = Particle(4, p[3].lam.copy(), ltilde4_hat)
    return p3h, p4h


def channel_A_shift34(particles, verbose=False):
    """
    Ch A: {3^,2} | {4^,5,6,1}

    Pole: z* from (p3^+p2)^2 = s23 + 2z<24>[23] = 0
          z* = -s23 / (2<24>[23]) = <23>/(2<24>)   (using s23 = <23>[32] = -<23>[23])

    Left:  A3^MHV(3^-, 2-, K+) = <3^2>^3/(<2K><K3^>)
    Right: A5^MHV((-K)-, 4^+, 5+, 6+, 1-) with neg-hel at pos 0 (-K) and pos 4 (1)
    """
    p = particles
    left_labels = [3, 2]  # 1-indexed
    z_star, P0_sq = find_pole_shift34(p, left_labels)
    if z_star is None:
        print("  Ch A: could not find pole")
        return 0.0

    p3h, p4h = shifted_particles_34(p, z_star)

    K_vec = p3h.four_momentum + p[1].four_momentum   # p3^ + p2
    K  = spinors_from_momentum(K_vec, label=97)
    mK = particle_from_neg_mom(K_vec, label=96)

    if verbose:
        print(f"  Ch A: z* = {z_star:.6f}")
        print(f"    K^2 = {mom_sq(K_vec):.2e}")
        print(f"    <3^,2> = {ab(p3h, p[1]):.8f}  (nonzero? {abs(ab(p3h,p[1])):.4f})")
        print(f"    [4^,5] at pole: {sb(p4h, p[4]):.8f}  (should NOT be 0)")

    # Left: A3^MHV(3^-, 2-, K+): cyclic order 3^, 2, K  => a=3^, b=2, c=K
    A_L = A3_MHV(p3h, p[1], K)

    # Right: A5^MHV((-K)-, 4^+, 5+, 6+, 1-)
    # Cyclic order in right sector: (-K), 4^, 5, 6, 1
    right_parts = [mK, p4h, p[4], p[5], p[0]]
    A_R = A_MHV(right_parts, 0, 4)   # neg-hel at pos 0 (-K) and pos 4 (1)

    if verbose:
        print(f"    A_L = {A_L:.8f}")
        print(f"    A_R = {A_R:.8f}")
        print(f"    P^2(0) = {P0_sq:.8f}")

    return A_L * A_R / P0_sq


if __name__ == "__main__":
    print("=" * 70)
    print("CROSS-CHECK: [3,4> SHIFT vs [1,2> SHIFT")
    print("=" * 70)

    all_ok = True
    for seed in [42, 137, 999, 7, 1234, 5678]:
        parts = make_6pt_kinematics(seed=seed)
        mom_err, _ = validate_6pt(parts, verbose=False)

        # [1,2> shift: C1 + C2 (C3=0)
        A_12, (C1, C2, C3) = A6_NMHV_BCFW(parts, verbose=False)

        # [3,4> shift: Ch A only
        A_34 = channel_A_shift34(parts, verbose=(seed == 42))

        ratio = A_34 / A_12 if abs(A_12) > 1e-15 else float('nan')
        err   = abs(ratio - 1) if not np.isnan(ratio) else float('nan')
        ok    = err < 1e-6 if not np.isnan(err) else False
        if not ok: all_ok = False

        print(f"\nSeed {seed:4d}: A[1,2>] = {A_12.real:+.6f}{A_12.imag:+.6f}i")
        print(f"          A[3,4>] = {A_34.real:+.6f}{A_34.imag:+.6f}i")
        print(f"          ratio   = {ratio:.8f}  |ratio-1| = {err:.2e}  {'OK' if ok else 'FAIL'}")

    print(f"\n{'ALL CROSS-CHECKS PASSED' if all_ok else 'SOME FAILED'}")
