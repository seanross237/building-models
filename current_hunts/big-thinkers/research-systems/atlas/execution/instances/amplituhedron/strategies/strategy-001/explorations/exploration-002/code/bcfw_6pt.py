"""
BCFW Recursion for 6-Point NMHV Amplitude A₆(1⁻,2⁻,3⁻,4⁺,5⁺,6⁺)

Uses [1,2> shift: |1^> = |1> + z|2>,  |2^] = |2] - z|1]

Three channels (partition 1^ and 2^ on opposite sides):
  Ch1: {1^,6}   | {2^,3,4,5}   -> A3 x A5
  Ch2: {1^,6,5} | {2^,3,4}     -> A4 x A4  (both MHV)
  Ch3: {1^,6,5,4}| {2^,3}      -> A5 x A3
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../exploration-001/code'))
sys.path.insert(0, os.path.dirname(__file__))

from spinor_helicity import Particle, ab, sb, spinors_from_momentum, sigma, sigma_bar
from kinematics_6pt import make_6pt_kinematics, validate_6pt


# ── helpers ────────────────────────────────────────────────────────────────────

def p4(particle):
    return particle.four_momentum

def mom_sq(pvec):
    """p² with (+,-,-,-) signature from a 4-vector array."""
    return (pvec[0]**2 - pvec[1]**2 - pvec[2]**2 - pvec[3]**2)

def dot4(a, b):
    return a[0]*b[0] - a[1]*b[1] - a[2]*b[2] - a[3]*b[3]

def spinor_outer_4vec(lam, lam_tilde):
    """Convert |lam>[lam_tilde| to 4-vector via Tr(sigma_bar · M)."""
    M = np.outer(lam, lam_tilde)
    result = np.zeros(4, dtype=complex)
    for mu in range(4):
        result[mu] = 0.5 * np.trace(sigma_bar[mu] @ M)
    return result

def particle_from_neg_mom(pvec, label):
    """Build a Particle with momentum -pvec."""
    return spinors_from_momentum(-pvec, label=label)


# ── 3-point amplitudes ─────────────────────────────────────────────────────────

def A3_MHV(pa, pb, pc):
    """A3^MHV(a-,b-,c+) = <ab>^3/(<bc><ca>). Cyclic order a,b,c."""
    return ab(pa, pb)**3 / (ab(pb, pc) * ab(pc, pa))

def A3_aMHV(pa, pb, pc):
    """A3^aMHV(a+,b+,c-) = [ab]^3/([bc][ca]). Cyclic order a,b,c."""
    return sb(pa, pb)**3 / (sb(pb, pc) * sb(pc, pa))


# ── n-point MHV and aMHV (Parke-Taylor) ──────────────────────────────────────

def A_MHV(particles, i_minus, j_minus):
    """A_n^MHV with negative helicities at positions i_minus, j_minus (0-indexed).
    Parke-Taylor: <ij>^4 / (<12><23>...<n1>)
    """
    n = len(particles)
    p = particles
    num = ab(p[i_minus], p[j_minus])**4
    den = 1.0
    for k in range(n):
        den *= ab(p[k], p[(k+1) % n])
    return num / den

def A_aMHV(particles, i_plus, j_plus):
    """A_n^aMHV with positive helicities at positions i_plus, j_plus (0-indexed).
    = [ij]^4 / ([12][23]...[n1])
    """
    n = len(particles)
    p = particles
    num = sb(p[i_plus], p[j_plus])**4
    den = 1.0
    for k in range(n):
        den *= sb(p[k], p[(k+1) % n])
    return num / den


# ── find BCFW pole ──────────────────────────────────────────────────────────────

def find_pole(particles, left_labels, verbose=False):
    """
    For [1,2> shift, find z* such that P_left^2(z) = 0.

    P(z) = P(0) + z * q   where q = lambda_2 ⊗ lambda_tilde_1  (as 4-vector)
    P^2(z) = P^2(0) + 2z * P(0)·q    (since q^2=0)
    z* = -P^2(0) / (2 P(0)·q)
    """
    p = particles  # 0-indexed; label i -> p[i-1]
    P0 = sum(p[i-1].four_momentum for i in left_labels)
    P0_sq = mom_sq(P0)

    # q = lambda_2 ⊗ lambda_tilde_1 as 4-vector
    q = spinor_outer_4vec(p[1].lam, p[0].lam_tilde)
    denom = 2.0 * dot4(P0, q)

    if abs(denom) < 1e-14:
        return None, None

    z_star = -P0_sq / denom

    if verbose:
        print(f"    P^2(0) = {P0_sq:.6f}, 2P·q = {denom:.6f}, z* = {z_star:.6f}")

    return z_star, P0_sq


def shifted_particles(particles, z):
    """Return copies of particles 1 and 2 with [1,2> shift applied."""
    p = particles
    lam1_hat = p[0].lam + z * p[1].lam
    ltilde2_hat = p[1].lam_tilde - z * p[0].lam_tilde
    p1_hat = Particle(1, lam1_hat, p[0].lam_tilde.copy())
    p2_hat = Particle(2, p[1].lam.copy(), ltilde2_hat)
    return p1_hat, p2_hat


# ── Channel 2: {1^,6,5} | {2^,3,4} — both sub-amps are 4-pt MHV ──────────────

def channel2(particles, verbose=False):
    """
    Left:  A4(K^-, 5^+, 6^+, 1^-) = MHV with minuses at K(pos 0) and 1^(pos 3)
    Right: A4(2^-, 3^-, 4^+, (-K)^+) = MHV with minuses at 2^(pos 0) and 3(pos 1)

    Pole: P = p1^ + p5 + p6, z* from P^2(z)=0.
    Since 1^ is angle-shifted, pole comes from angle bracket condition.
    """
    p = particles
    left_labels = [1, 5, 6]  # 1-indexed
    z_star, P0_sq = find_pole(p, left_labels, verbose=verbose)
    if z_star is None:
        return 0.0

    p1h, p2h = shifted_particles(p, z_star)

    # Internal momentum K = p1^ + p5 + p6
    K_vec = p1h.four_momentum + p[4].four_momentum + p[5].four_momentum
    K = spinors_from_momentum(K_vec, label=97)
    mK = particle_from_neg_mom(K_vec, label=96)  # -K

    if verbose:
        print(f"    K^2 at pole = {mom_sq(K_vec):.2e}")

    # Left: A4(K^-, p5^+, p6^+, p1h^-) in cyclic order K,5,6,1^
    # Two minuses at positions 0 (K) and 3 (p1h) — but Parke-Taylor needs cyclic order
    left_parts = [K, p[4], p[5], p1h]
    A_L = A_MHV(left_parts, 0, 3)  # i_minus=0 (K), j_minus=3 (p1h)

    # Right: A4((-K)^+, p2h^-, p3^-, p4^+) in cyclic order -K,2^,3,4
    # Two minuses at positions 1 (p2h) and 2 (p3)
    right_parts = [mK, p2h, p[2], p[3]]
    A_R = A_MHV(right_parts, 1, 2)  # i_minus=1 (p2h), j_minus=2 (p3)

    if verbose:
        print(f"    A_L = {A_L:.8f}")
        print(f"    A_R = {A_R:.8f}")
        print(f"    P^2 = {P0_sq:.8f}")

    return A_L * A_R / P0_sq


# ── Channel 1: {1^,6} | {2^,3,4,5} ──────────────────────────────────────────

def channel1(particles, verbose=False):
    """
    Pole: z* from <1^6>=0, i.e. z* = -<16>/<26>
    Left: A3^aMHV(6^+, K^+, 1^-) — anti-MHV, positives at 6 and K
    Right: A5^aMHV((-K)^-, 2^-, 3^-, 4^+, 5^+) — aMHV with positives at 4,5
    """
    p = particles
    left_labels = [1, 6]
    z_star, P0_sq = find_pole(p, left_labels, verbose=verbose)
    if z_star is None:
        return 0.0

    p1h, p2h = shifted_particles(p, z_star)

    # Verify <1^6>=0 at this z*
    bracket_check = ab(p1h, p[5])
    if verbose:
        print(f"    z* = {z_star:.6f}, <1^6> = {bracket_check:.2e} (should be ~0)")

    K_vec = p1h.four_momentum + p[5].four_momentum
    K = spinors_from_momentum(K_vec, label=97)
    mK = particle_from_neg_mom(K_vec, label=96)

    if verbose:
        print(f"    K^2 at pole = {mom_sq(K_vec):.2e}")

    # Left: A3^aMHV(6^+, K^+, 1^-) — cyclic order 6, K, 1^
    # anti-MHV: two plusses at 6(pos 0) and K(pos 1), minus at 1^(pos 2)
    A_L = A3_aMHV(p[5], K, p1h)

    # Right: A5^aMHV((-K)^-, 2^-, 3^-, 4^+, 5^+)
    # Cyclic order: -K, 2^, 3, 4, 5 ; positives at pos 3(p4) and pos 4(p5)
    right_parts = [mK, p2h, p[2], p[3], p[4]]
    A_R = A_aMHV(right_parts, 3, 4)  # i_plus=3 (p4), j_plus=4 (p5)

    if verbose:
        print(f"    A_L (aMHV) = {A_L:.8f}")
        print(f"    A_R (aMHV) = {A_R:.8f}")
        print(f"    P^2 = {P0_sq:.8f}")

    return A_L * A_R / P0_sq


# ── Channel 3: {1^,6,5,4} | {2^,3} ────────────────────────────────────────────

def channel3(particles, verbose=False):
    """
    Pole: z* from [2^3]=0, i.e. [2^3]=[23]-z*[13]=0 => z*=[23]/[13]
    Left: A5^MHV(K^-, 1^-, 6^+, 5^+, 4^+) — MHV with minuses at K(0) and 1^(1)
    Right: A3^MHV(2^-, 3^-, (-K)^+) — MHV
    """
    p = particles
    left_labels = [1, 4, 5, 6]
    z_star, P0_sq = find_pole(p, left_labels, verbose=verbose)
    if z_star is None:
        return 0.0

    p1h, p2h = shifted_particles(p, z_star)

    # Verify [2^3]=0 at this z*
    bracket_check = sb(p2h, p[2])
    if verbose:
        print(f"    z* = {z_star:.6f}, [2^3] = {bracket_check:.2e} (should be ~0)")

    K_vec = p1h.four_momentum + p[3].four_momentum + p[4].four_momentum + p[5].four_momentum
    K = spinors_from_momentum(K_vec, label=97)
    mK = particle_from_neg_mom(K_vec, label=96)

    if verbose:
        print(f"    K^2 at pole = {mom_sq(K_vec):.2e}")

    # Left: A5^MHV(K^-, 1^-, 6^+, 5^+, 4^+) — cyclic order K,1^,6,5,4
    # MHV: two minuses at pos 0 (K) and pos 1 (1^)
    left_parts = [K, p1h, p[5], p[4], p[3]]
    A_L = A_MHV(left_parts, 0, 1)

    # Right: A3^MHV(2^-, 3^-, (-K)^+) — cyclic order 2^, 3, -K
    A_R = A3_MHV(p2h, p[2], mK)

    if verbose:
        print(f"    A_L (MHV5) = {A_L:.8f}")
        print(f"    A_R (MHV3) = {A_R:.8f}")
        print(f"    P^2 = {P0_sq:.8f}")

    return A_L * A_R / P0_sq


# ── Total NMHV amplitude ────────────────────────────────────────────────────────

def A6_NMHV_BCFW(particles, verbose=False):
    """
    A6^NMHV(1-,2-,3-,4+,5+,6+) via BCFW recursion with [1,2> shift.
    Sum of 3 channels.
    """
    if verbose:
        print("\n  CHANNEL 1: {1^,6} | {2^,3,4,5}")
    C1 = channel1(particles, verbose=verbose)

    if verbose:
        print("\n  CHANNEL 2: {1^,6,5} | {2^,3,4}")
    C2 = channel2(particles, verbose=verbose)

    if verbose:
        print("\n  CHANNEL 3: {1^,6,5,4} | {2^,3}")
    C3 = channel3(particles, verbose=verbose)

    total = C1 + C2 + C3

    if verbose:
        print(f"\n  C1 = {C1:.10f}")
        print(f"  C2 = {C2:.10f}")
        print(f"  C3 = {C3:.10f}")
        print(f"  Total = {total:.10f}")

    return total, (C1, C2, C3)


# ── Cross-check: BCFW with [2,3> shift ─────────────────────────────────────────
# We verify the [1,2> result against [2,3> shift as an independent check.
# For [2,3> shift: |2^> = |2>+z|3>, |3^] = |3]-z|2]
# Channels: {2^,1} | {3^,4,5,6}, {2^,1,6} | {3^,4,5}, {2^,1,6,5} | {3^,4}

def find_pole_shift23(particles, left_labels, verbose=False):
    """For [2,3> shift, find z* such that P_left^2(z)=0."""
    p = particles
    P0 = sum(p[i-1].four_momentum for i in left_labels)
    P0_sq = mom_sq(P0)
    q = spinor_outer_4vec(p[2].lam, p[1].lam_tilde)  # lambda_3 ⊗ lambda_tilde_2
    denom = 2.0 * dot4(P0, q)
    if abs(denom) < 1e-14:
        return None, None
    z_star = -P0_sq / denom
    return z_star, P0_sq

def A6_NMHV_BCFW_shift23(particles, verbose=False):
    """
    A6^NMHV via BCFW with [2,3> shift as independent cross-check.
    Channels (containing 2^ but not 3^):
      Ch A: {2^,1}     | {3^,4,5,6}
      Ch B: {2^,1,6}   | {3^,4,5}
      Ch C: {2^,1,6,5} | {3^,4}
    """
    p = particles

    total = 0.0 + 0j
    contributions = []

    # Channel A: {2^,1} left, {3^,4,5,6} right
    # Left A3: A3(1^- ... actually 1 is NOT shifted here, 2^ is
    # Helicities: left has 2^-(shifted) and 1-, right has 3^-(shifted),4+,5+,6+
    z_A, P0_sq_A = find_pole_shift23(p, [2, 1], verbose=False)
    if z_A is not None:
        lam2h = p[1].lam + z_A * p[2].lam
        lt3h  = p[2].lam_tilde - z_A * p[1].lam_tilde
        p2h = Particle(2, lam2h, p[1].lam_tilde.copy())
        p3h = Particle(3, p[2].lam.copy(), lt3h)

        K_vec = p2h.four_momentum + p[0].four_momentum
        K  = spinors_from_momentum(K_vec, label=97)
        mK = particle_from_neg_mom(K_vec, label=96)

        # Left A3: particles 1-(pos0), 2^-(pos1), K+ (pos2) in cyclic order
        # Need to determine: pole from <2^1>=0 or [3^...]=0?
        # [2,3> shift: pole for ch A comes from <2^1>=<21>+z<31>=0 => z=-<21>/<31>
        # So aMHV on left: A3^aMHV(1+,K+,2^-)?? No: helicities are 1- and 2^-.
        # With aMHV need 2 plusses. But both left particles have minus helicity!
        # So left must be A3^MHV(1-,2^-,K+): <1,2^>^3/(<2^,K><K,1>)
        # (pole <2^1>=0 means K angle spinor parallel to 1 angle spinor)
        A_L_A = A3_MHV(p[0], p2h, K)  # MHV: 1-, 2^-, K+

        # Right A5: (-K)+, 3^-, 4+, 5+, 6+ with 3 positives → aMHV with pos at -K,4,5,6?
        # Actually: helicities are (-K)^+?, 3^-, 4+, 5+, 6+
        # Wait: 5-pt with helicities: K+, 3-, 4+, 5+, 6+ → 4 positives, 1 negative = aMHV
        # A5^aMHV with one minus at pos 1 (3^): use [ij]^4/prod for positives at 0,2,3,4
        # But Parke-Taylor aMHV needs EXACTLY 2 positives... hmm
        # For n=5, aMHV = n-2 = 3 negatives, or equivalently k=2 positives.
        # Right here has: (-K)+, 3^-, 4+, 5+, 6+ => 3 positives, 2 negatives?
        # No: -K has + helicity? Let's see: K was + from left so -K is + outgoing momentum
        # but -K as an incoming particle has - helicity... conventions are confusing.

        # Let me use: the right amplitude is A5(mK, p3h, p4, p5, p6)
        # with helicity assignments: mK uses opposite helicity from K
        # K was chosen with + helicity (aMHV on left needed K+), so mK = -K has - helicity
        # A5: mK-, 3^-, 4+, 5+, 6+ => 2 minuses = MHV
        right_parts = [mK, p3h, p[3], p[4], p[5]]
        A_R_A = A_MHV(right_parts, 0, 1)  # MHV: mK-(pos0), 3^-(pos1)

        ch_A = A_L_A * A_R_A / P0_sq_A
        total += ch_A
        contributions.append(('A', ch_A))

    # Channel B: {2^,1,6} left, {3^,4,5} right
    z_B, P0_sq_B = find_pole_shift23(p, [2, 1, 6], verbose=False)
    if z_B is not None:
        lam2h = p[1].lam + z_B * p[2].lam
        lt3h  = p[2].lam_tilde - z_B * p[1].lam_tilde
        p2h = Particle(2, lam2h, p[1].lam_tilde.copy())
        p3h = Particle(3, p[2].lam.copy(), lt3h)

        K_vec = p2h.four_momentum + p[0].four_momentum + p[5].four_momentum
        K  = spinors_from_momentum(K_vec, label=97)
        mK = particle_from_neg_mom(K_vec, label=96)

        # Left A4: 1-, 6+, 2^-, K+ in some cyclic order
        # MHV with minuses at 1(pos?) and 2^
        # Cyclic order in original trace going left: K, 2^, 1, 6 (or reversed)
        # Let's use: left_parts = [K, p2h, p[0], p[5]] cyclic from original 1,6 sector
        # Actually original order is 1,2,3,4,5,6 cyclic. Left sector: {2,1,6}+K
        # Going with original order: K appears before 2^ and 6 after 1
        # Color order: K, 2^, (1, 6 reversed? or direct?)
        # From original 1,...,6 cycle: split at {2^,1,6}|{3^,4,5}
        # The left cycle is ...,6,1,2^,K and right is K,-K,3^,4,5,...
        # Color order of left: K,2^,1,6 going in the positive direction
        # Actually: in BCFW, left amplitude is color-ordered as (K, ...left set... in cycle order)
        # Left set in original order: 1,6 plus 2^, plus K at the boundary
        # Cyclic order of {1,2,6} in 1,2,3,4,5,6: going 1->2->...->6->1, the left set is {1,2,6}
        # which in cyclic order is: 6,1,2 (reading counterclockwise from 2 to 6)
        # With internal K: left sub-amplitude is A4(K,1,6,2^) or A4(2^,1,6,K)?
        # Convention: A_L has particles (...left in cycle..., K)
        # going from (right's last particle +1) around to (left's last before K)
        # Right side: {3^,4,5} = {3,4,5} in cycle. So right goes 3->4->5.
        # Left goes 6->1->2^ and then K back to 3.
        # So left color order is: K, 6, 1, 2^ (K at start, then 6,1,2^ in cycle order)

        left_parts_B = [K, p[5], p[0], p2h]
        # Helicities: K+, 6+, 1-, 2^- => two minuses at pos 2 (p[0]=1) and pos 3 (p2h=2^)
        # But wait: K's helicity? At this pole the condition is [3^K]=0? or <2^1>=0?
        # For {2^,1,6} left: the pole comes from (p2^ + p1 + p6)^2 = 0.
        # The shift is |2^>=|2>+z|3>, so the pole condition involves 3^ (angle-shifted).
        # Let me check: is the pole from <2^j>=0 or [3^j]=0?
        # P_B = p2 + p1 + p6 + z*(lambda_3 ⊗ lambda_tilde_2)
        # The pole: for left containing 2^ (angle-shifted), pole from angle bracket <2^j>=0
        # for some j in the right set. But the right set is {3^,4,5} and 3^ is square-shifted.
        # Since 2^ is angle-shifted and 3^ is square-shifted, and they're on opposite sides:
        # For left set {2^,1,6}: the particle 2^ has |2^>=|2>+z|3>, so if <2^6>=0 or <2^1>=0
        # at the pole... but momentum conservation + lightlike constraint uniquely determines z*.
        # For right set {3^,4,5}: A4(mK,3^,4,5) with some helicities.
        # If K is -, then mK is + and: right A4(mK+,3^-,4+,5+) = 1 minus = not valid MHV(need 2)
        # If K is +, then mK is - and: right A4(mK-,3^-,4+,5+) = 2 minuses = MHV ✓
        # Left A4(K+,6+,1-,2^-): 2 minuses at pos 2 (1) and pos 3 (2^) = MHV ✓

        A_L_B = A_MHV(left_parts_B, 2, 3)  # MHV: 1(pos2), 2^(pos3)

        right_parts_B = [mK, p3h, p[3], p[4]]
        # mK-, 3^-, 4+, 5+? Wait: mK is -K and if K is +, mK as outgoing has - helicity
        # A4(mK-, 3^-, 4+, 5+) but right only has {3^,4,5} + mK = 4 particles ✓
        # Wait: right set is {3^,4,5} with 3 particles plus mK = 4 total.
        # Color order of right: mK, 3^, 4, 5 (mK at start, then 3^,4,5 in cycle order)
        # A4(mK-,3^-,4+,5+): MHV with minuses at pos 0 (mK) and pos 1 (3^)
        # But the original helicities: 3 is negative (3-), 4 is positive, 5 is positive.
        # So right is A4(mK-,3^-,4+,5+): ✓
        A_R_B = A_MHV(right_parts_B, 0, 1)

        ch_B = A_L_B * A_R_B / P0_sq_B
        total += ch_B
        contributions.append(('B', ch_B))

    # Channel C: {2^,1,6,5} left, {3^,4} right
    z_C, P0_sq_C = find_pole_shift23(p, [2, 1, 6, 5], verbose=False)
    if z_C is not None:
        lam2h = p[1].lam + z_C * p[2].lam
        lt3h  = p[2].lam_tilde - z_C * p[1].lam_tilde
        p2h = Particle(2, lam2h, p[1].lam_tilde.copy())
        p3h = Particle(3, p[2].lam.copy(), lt3h)

        K_vec = p2h.four_momentum + p[0].four_momentum + p[5].four_momentum + p[4].four_momentum
        K  = spinors_from_momentum(K_vec, label=97)
        mK = particle_from_neg_mom(K_vec, label=96)

        # Right A3: mK, 3^-, 4+
        # [3^4]=0 at this pole => square brackets of 3^ and 4 vanish
        # MHV: A3^MHV(3^-, 4+, mK+)? Needs <3^,mK>? Or aMHV?
        # Since 3^ is square-shifted (|3^]=|3]-z|2]), at [3^4]=0: square spinors of 3^ and 4
        # become proportional. This is the condition for A3^aMHV to potentially be non-zero.
        # A3^aMHV(4+,mK+,3^-): [4,mK]^3/([mK,3^][3^,4])
        # Alternatively A3^MHV(3^-,4+,mK+): needs <3^,4>=0? Not necessarily at this pole.
        # At [3^4]=0, the MHV amplitude A3^MHV(3^-,4+,mK+)=<3^,mK>^3/(<mK,4><4,3^>)
        # which may be non-zero since angle brackets aren't constrained.
        # The aMHV amplitude A3^aMHV(4+,mK+,3^-)=[4,mK]^3/([mK,3^][3^,4]) → [3^,4]=0
        # means this DIVERGES unless [4,mK]=0 too. Actually this might be 0/0 situation.

        # Let me check: [3^4]=0 means square spinors of 3^ and 4 are proportional.
        # K = -(p3^ + p4) = -(p2^+p1+p5+p6), lightlike when [3^4]=0.
        # With [3^4]=0, K^{αα̇} = -(λ₃^α λ̃₃^{α̇} + λ₄^α λ̃₄^{α̇})
        # K is rank 1, so mK = -K is also rank 1.
        # For A3^MHV(3^-,mK+,4+): <3^,mK>^3/(<mK,4><4,3^>)
        # At [3^4]=0: λ̃₃^∝λ̃₄, so K=-(λ₃λ̃₃^+λ₄λ̃₄) → needs more analysis.
        # Let's just try MHV and aMHV and see which is non-zero.
        # Actually: K = -(p2^+p1+p5+p6) and at pole [3^4]=[34]-z*[24]=0 => z*=[34]/[24]
        # K is determined by LEFT sector: K = p2^+p1+p5+p6
        # = p1+p2+p5+p6 + z*(lambda3 ⊗ lambda_tilde_2)·(p1+p5+p6 directions)... complicated.
        # Let's just try both A3 options numerically.

        # Try A3^MHV(3^-, 4+, mK+): cyclic 3^,4,mK with minuses only at 3^
        # Only 1 minus: NOT MHV (need 2). So A3^MHV is zero (all-plus or single-minus vanish).
        # Try A3^aMHV(3^-, mK+, 4+): actually need 2 plusses for aMHV:
        # A3^aMHV(4+, mK+, 3^-) = [4,mK]^3/([mK,3^][3^,4])

        A_R_C = A3_aMHV(p[3], mK, p3h)  # aMHV(4+, mK+, 3^-): a=4, b=mK, c=3^

        # Left A5: K-, 2^-, 1-, 6+, 5+ — 3 minuses?
        # Color order of left: K, 5, 6, 1, 2^ (K at start, then in cycle order 5->6->1->2^)
        # Wait: original order 1,2,3,4,5,6. Left set = {2,1,6,5}.
        # Cycle going 1->2->...->6->1, left particles in order: 5,6,1,2^
        # Color order with K at boundary: K, 5, 6, 1, 2^ or 2^, 1, 6, 5, K?
        # Convention: left amplitude is traversed from K going into the left sector.
        # Left: K, 2^, 1, 6, 5 (going from K, following original cycle 2->1->6->5)
        # Actually for the [2,3> shift the ordering is: right to left in the 1,...,6 cycle,
        # the left sector is {2,1,6,5} and going in cycle order: 5,6,1,2 (backwards from 3).
        # Standard BCFW: left amp cyclic order is (K, ..., shifted_particle) or similar.

        # Let me use: left color order K, 2^, 1, 6, 5 (K then continuing the cycle from 2 backwards: 2^->1->6->5)
        # Alternatively: 5,6,1,2^,K reading in cycle direction.
        # I'll use: left_parts_C = [K, p2h, p[0], p[5], p[4]]
        # Helicities: K?, 2^-, 1-, 6+, 5+
        # K: if mK has + helicity (as used in A3^aMHV), then K has - helicity.
        # Left A5(K-, 2^-, 1-, 6+, 5+): 3 minuses = aMHV (anti-MHV at 5-pt = 2 positives)
        # aMHV with positives at 6 and 5: A5^aMHV with i_plus=3 (p[5]=6), j_plus=4 (p[4]=5)
        left_parts_C = [K, p2h, p[0], p[5], p[4]]
        # Positives at pos 3 (6) and pos 4 (5)
        A_L_C = A_aMHV(left_parts_C, 3, 4)

        ch_C = A_L_C * A_R_C / P0_sq_C
        total += ch_C
        contributions.append(('C', ch_C))

    if verbose:
        for name, val in contributions:
            print(f"  Shift23 Ch{name} = {val:.10f}")
        print(f"  Shift23 Total = {total:.10f}")

    return total, contributions


# ── Main test ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 70)
    print("BCFW 6-POINT NMHV AMPLITUDE A6(1-,2-,3-,4+,5+,6+)")
    print("=" * 70)

    for seed in [42, 137, 999]:
        print(f"\n{'─'*60}")
        print(f"Seed = {seed}")
        parts = make_6pt_kinematics(seed=seed)
        mom_err, _ = validate_6pt(parts, verbose=False)
        print(f"Kinematics valid: mom_err={mom_err:.2e}")

        print("\n[1,2> shift:")
        A_total, (C1, C2, C3) = A6_NMHV_BCFW(parts, verbose=True)

        print(f"\n[2,3> shift (cross-check):")
        A_shift23, contribs = A6_NMHV_BCFW_shift23(parts, verbose=True)

        if abs(A_total) > 1e-15:
            ratio = A_shift23 / A_total
            print(f"\n  Ratio [2,3> / [1,2> = {ratio:.8f} (should be 1+0i)")
            print(f"  Agreement: {abs(ratio - 1):.2e}")
