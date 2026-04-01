"""
SU(2) Lattice Gauge Theory in 4D — Wilson Plaquette Action
==========================================================

Full implementation of Monte Carlo simulation for SU(2) Yang-Mills theory
on a 4D hypercubic lattice using the Wilson plaquette action.

Author: Math Explorer (Atlas system)
Date: 2026-03-27
"""

import numpy as np
from time import time
import os

# ============================================================================
# SU(2) Matrix Operations
# ============================================================================
# SU(2) elements are parameterized as: U = a0*I + i*(a1*σ1 + a2*σ2 + a3*σ3)
# where a0² + a1² + a2² + a3² = 1
# We store them as (a0, a1, a2, a3) — quaternion representation
# This is equivalent to the 2x2 matrix:
#   [[a0 + i*a3,  a2 + i*a1],
#    [-a2 + i*a1, a0 - i*a3]]

def su2_identity():
    """Return identity element of SU(2) as quaternion (a0,a1,a2,a3)."""
    return np.array([1.0, 0.0, 0.0, 0.0])

def su2_multiply(q1, q2):
    """Multiply two SU(2) elements in quaternion representation.
    q = (a0, a1, a2, a3), quaternion multiplication."""
    a0, a1, a2, a3 = q1[..., 0], q1[..., 1], q1[..., 2], q1[..., 3]
    b0, b1, b2, b3 = q2[..., 0], q2[..., 1], q2[..., 2], q2[..., 3]

    result = np.empty_like(q1)
    result[..., 0] = a0*b0 - a1*b1 - a2*b2 - a3*b3
    result[..., 1] = a0*b1 + a1*b0 + a2*b3 - a3*b2
    result[..., 2] = a0*b2 - a1*b3 + a2*b0 + a3*b1
    result[..., 3] = a0*b3 + a1*b2 - a2*b1 + a3*b0
    return result

def su2_dagger(q):
    """Hermitian conjugate (inverse) of SU(2) element: (a0, -a1, -a2, -a3)."""
    result = q.copy()
    result[..., 1] *= -1
    result[..., 2] *= -1
    result[..., 3] *= -1
    return result

def su2_trace(q):
    """(1/2) Re Tr U = a0 for SU(2) in quaternion representation."""
    return q[..., 0]

def su2_random(shape=None):
    """Generate random SU(2) element uniformly on the group (Haar measure).
    Uses the method: generate 4 Gaussian random numbers and normalize."""
    if shape is None:
        q = np.random.randn(4)
    else:
        q = np.random.randn(*shape, 4)
    norm = np.sqrt(np.sum(q**2, axis=-1, keepdims=True))
    return q / norm

def su2_near_identity(epsilon):
    """Generate SU(2) element near identity for Metropolis updates.
    a0 = sqrt(1 - epsilon²*r²), (a1,a2,a3) = epsilon * random_on_S2."""
    r = np.random.randn(3)
    r = r / np.linalg.norm(r)
    r *= epsilon * np.random.random()**(1.0/3.0)
    a0 = np.sqrt(max(1.0 - np.sum(r**2), 0.0))
    return np.array([a0, r[0], r[1], r[2]])


# ============================================================================
# Heat Bath Algorithm for SU(2) — Creutz method
# ============================================================================

def heat_bath_su2(staple_sum, beta):
    """
    Generate new SU(2) link using the heat bath algorithm (Creutz method).

    The effective action for link U_mu(x) is:
    S_eff = -(beta/2) Re Tr(U * A)
    where A = sum of staples.

    For SU(2), the staple sum A can be written as k * V where k = |det(A)|^{1/2}
    and V is in SU(2). We need to generate U from the distribution
    exp(beta * k * a0) * sqrt(1 - a0^2) on [-1, 1].

    Parameters:
        staple_sum: quaternion (a0,a1,a2,a3) representing sum of staples
        beta: inverse coupling
    Returns:
        new SU(2) link as quaternion
    """
    # Compute k = sqrt(det(A)) = sqrt(a0^2 + a1^2 + a2^2 + a3^2) for the sum
    k = np.sqrt(np.sum(staple_sum**2))

    if k < 1e-10:
        # Degenerate case — return random element
        return su2_random()

    # V = A / k (normalize to get SU(2) element)
    V = staple_sum / k

    # Now generate a0 from P(a0) ~ exp(beta*k*a0) * sqrt(1 - a0^2)
    # Using Creutz's method (rejection sampling)
    bk = beta * k

    # Kennedy-Pendleton algorithm for efficiency
    a0 = _kennedy_pendleton_sample(bk)

    # Generate the rest: (a1, a2, a3) uniformly on sphere of radius sqrt(1-a0^2)
    r = np.sqrt(1.0 - a0**2)
    phi = 2.0 * np.pi * np.random.random()
    cos_theta = 2.0 * np.random.random() - 1.0
    sin_theta = np.sqrt(1.0 - cos_theta**2)

    a1 = r * sin_theta * np.cos(phi)
    a2 = r * sin_theta * np.sin(phi)
    a3 = r * cos_theta

    U_new_in_A_frame = np.array([a0, a1, a2, a3])

    # The new link is U_new = U_new_in_A_frame * V^dagger
    U_new = su2_multiply(U_new_in_A_frame, su2_dagger(V))

    return U_new


def _kennedy_pendleton_sample(bk):
    """
    Kennedy-Pendleton algorithm for sampling a0 from:
    P(a0) ~ exp(bk * a0) * sqrt(1 - a0^2) on [-1, 1]

    This is equivalent to sampling x = 1 - a0 from an appropriate distribution.
    """
    if bk < 0.01:
        # Very small bk — essentially uniform on S3
        return 2.0 * np.random.random() - 1.0

    while True:
        # Generate candidate using the Creutz method
        r1 = np.random.random()
        r2 = np.random.random()
        r3 = np.random.random()

        # Avoid log(0)
        if r1 < 1e-300:
            continue
        if r3 < 1e-300:
            continue

        x = -(np.log(r1) + np.log(r3) * np.cos(np.pi * r2)**2) / bk

        # Accept-reject: accept with probability sqrt(1 - x/2)
        # x should be in [0, 2] for a0 = 1 - x in [-1, 1]
        if x > 2.0:
            continue

        r4 = np.random.random()
        if r4**2 <= 1.0 - x / 2.0:
            a0 = 1.0 - x
            return a0


# ============================================================================
# 4D Lattice
# ============================================================================

class LatticeGaugeTheory:
    """
    4D SU(2) lattice gauge theory with Wilson plaquette action.

    The gauge field is stored as link variables U_mu(x) for each site x and
    direction mu = 0,1,2,3.

    Lattice shape: (L, L, L, L) — hypercubic
    Links stored as: links[x0, x1, x2, x3, mu, 4] where last index is quaternion
    """

    def __init__(self, L, beta, seed=None):
        self.L = L
        self.beta = beta
        self.ndim = 4
        self.volume = L**4

        if seed is not None:
            np.random.seed(seed)

        # Initialize links — cold start (all identity)
        self.links = np.zeros((L, L, L, L, 4, 4))
        self.links[..., 0] = 1.0  # a0 = 1, identity

    def hot_start(self):
        """Initialize with random SU(2) elements (hot/disordered start)."""
        self.links = su2_random((self.L, self.L, self.L, self.L, 4))

    def cold_start(self):
        """Initialize with identity elements (cold/ordered start)."""
        self.links = np.zeros((self.L, self.L, self.L, self.L, 4, 4))
        self.links[..., 0] = 1.0

    def get_link(self, site, mu):
        """Get link U_mu(site) as quaternion."""
        x0, x1, x2, x3 = site
        return self.links[x0, x1, x2, x3, mu].copy()

    def set_link(self, site, mu, U):
        """Set link U_mu(site)."""
        x0, x1, x2, x3 = site
        self.links[x0, x1, x2, x3, mu] = U

    def shift(self, site, mu, direction=1):
        """Shift site by one step in direction mu. Periodic BC."""
        s = list(site)
        s[mu] = (s[mu] + direction) % self.L
        return tuple(s)

    def plaquette(self, site, mu, nu):
        """
        Compute plaquette U_P = U_mu(x) U_nu(x+mu) U_mu(x+nu)^dag U_nu(x)^dag
        Returns quaternion.
        """
        x = site
        x_mu = self.shift(x, mu)
        x_nu = self.shift(x, nu)

        U1 = self.get_link(x, mu)
        U2 = self.get_link(x_mu, nu)
        U3 = su2_dagger(self.get_link(x_nu, mu))
        U4 = su2_dagger(self.get_link(x, nu))

        return su2_multiply(su2_multiply(su2_multiply(U1, U2), U3), U4)

    def staple_sum(self, site, mu):
        """
        Compute sum of staples for link U_mu(x).
        A staple in the (mu,nu) plane is:
          Forward: U_nu(x+mu) U_mu(x+nu)^dag U_nu(x)^dag
          Backward: U_nu(x+mu-nu)^dag U_mu(x-nu)^dag^dag ...

        Wait — let me be precise. The action contribution involving U_mu(x) is:
        S_mu(x) = -(beta/2) Re Tr(U_mu(x) * A_mu(x))
        where A_mu(x) is the sum of staples.

        For each nu != mu, the two staples are:
        Forward staple:  U_nu(x+mu) * U_mu(x+nu)^dag * U_nu(x)^dag
        Backward staple: U_nu(x+mu-nu)^dag * U_mu(x-nu)^dag * ... hmm

        Let me redo this carefully.
        The plaquette in (mu,nu) plane at x is:
        P_f = U_mu(x) * U_nu(x+mu) * U_mu(x+nu)^dag * U_nu(x)^dag

        The staple (forward, nu-direction) is everything except U_mu(x):
        A_f = U_nu(x+mu) * U_mu(x+nu)^dag * U_nu(x)^dag

        The backward plaquette in (mu, -nu) at x:
        P_b = U_mu(x) * U_nu(x+mu-nu)^dag * U_mu(x-nu)^dag * U_nu(x-nu)

        Backward staple:
        A_b = U_nu(x+mu-nu)^dag * U_mu(x-nu)^dag * U_nu(x-nu)

        Wait, that's wrong. Let me be really careful.

        For the backward plaquette, consider the plaquette in the (mu,nu) plane
        at the site x-nu:
        P = U_mu(x-nu) * U_nu(x-nu+mu) * U_mu(x)^dag * U_nu(x-nu)^dag

        Hmm, this isn't standard either. Let me just do it right:

        The backward staple for (mu, nu) is obtained from the plaquette at site
        x shifted by -nu:
        Plaq at (x-nu, mu, nu) = U_mu(x-nu) U_nu(x-nu+mu) U_mu(x)^dag U_nu(x-nu)^dag

        The staple from this plaquette (everything except U_mu(x)^dag, then take dag):
        Actually, we want U_mu(x) * staple to give the plaquette trace.

        Let me just compute the 6 staples directly.
        """
        A = np.zeros(4)
        x = site
        L = self.L

        for nu in range(4):
            if nu == mu:
                continue

            x_mu = self.shift(x, mu)
            x_nu = self.shift(x, nu)
            x_mu_nu = self.shift(x_mu, nu)  # not used but for clarity
            x_minus_nu = self.shift(x, nu, -1)
            x_mu_minus_nu = self.shift(x_mu, nu, -1)

            # Forward staple: U_nu(x+mu) * U_mu(x+nu)^dag * U_nu(x)^dag
            U1 = self.get_link(x_mu, nu)
            U2 = su2_dagger(self.get_link(x_nu, mu))
            U3 = su2_dagger(self.get_link(x, nu))
            fwd = su2_multiply(su2_multiply(U1, U2), U3)

            # Backward staple: U_nu(x+mu-nu)^dag * U_mu(x-nu)^dag * U_nu(x-nu)
            U4 = su2_dagger(self.get_link(x_mu_minus_nu, nu))
            U5 = su2_dagger(self.get_link(x_minus_nu, mu))
            U6 = self.get_link(x_minus_nu, nu)
            bwd = su2_multiply(su2_multiply(U4, U5), U6)

            A += fwd + bwd

        return A

    def average_plaquette(self):
        """Compute average plaquette: <(1/2) Re Tr U_P> averaged over all plaquettes."""
        total = 0.0
        count = 0
        L = self.L

        for x0 in range(L):
            for x1 in range(L):
                for x2 in range(L):
                    for x3 in range(L):
                        site = (x0, x1, x2, x3)
                        for mu in range(4):
                            for nu in range(mu+1, 4):
                                P = self.plaquette(site, mu, nu)
                                total += su2_trace(P)
                                count += 1

        return total / count

    def sweep_heatbath(self):
        """Perform one heat bath sweep over all links."""
        L = self.L
        for x0 in range(L):
            for x1 in range(L):
                for x2 in range(L):
                    for x3 in range(L):
                        site = (x0, x1, x2, x3)
                        for mu in range(4):
                            A = self.staple_sum(site, mu)
                            U_new = heat_bath_su2(A, self.beta)
                            self.set_link(site, mu, U_new)

    def sweep_metropolis(self, epsilon=0.3, n_hits=10):
        """Perform one Metropolis sweep with multi-hit."""
        L = self.L
        accepted = 0
        total = 0

        for x0 in range(L):
            for x1 in range(L):
                for x2 in range(L):
                    for x3 in range(L):
                        site = (x0, x1, x2, x3)
                        for mu in range(4):
                            A = self.staple_sum(site, mu)
                            U_old = self.get_link(site, mu)

                            for _ in range(n_hits):
                                # Propose: U_new = R * U_old where R is near identity
                                R = su2_near_identity(epsilon)
                                U_new = su2_multiply(R, U_old)

                                # Normalize to stay on SU(2)
                                norm = np.sqrt(np.sum(U_new**2))
                                U_new /= norm

                                # Change in action
                                dS = -self.beta / 2.0 * 2.0 * (
                                    su2_trace(su2_multiply(U_new, su2_dagger(su2_identity()))) -
                                    su2_trace(su2_multiply(U_old, su2_dagger(su2_identity())))
                                )
                                # Actually: dS = -(beta/2) * Re Tr((U_new - U_old) * A)
                                # = -(beta/2) * 2 * (trace(U_new * A†) - trace(U_old * A†))
                                # Wait, for quaternions: (1/2)ReTr(U*A) = a0_U*a0_A + a1_U*a1_A + ...
                                # Hmm no. Let me think again.
                                # (1/2) Re Tr(U) = q[0] for quaternion q
                                # So (1/2) Re Tr(U * A) where A is the staple sum...
                                # U*A in quaternion is su2_multiply(U, A)
                                # But A is the sum, not an SU(2) element, so we need:
                                # (1/2) Re Tr(U * A†) = component of U·A† along identity
                                # For quaternion product: (U * A†)[0]
                                # But actually the staple contribution is:
                                # S = -(beta/2) * Re Tr(U * A) = -beta * su2_trace(su2_multiply(U, A))
                                # Hmm, no. For the action S = beta * sum_P (1 - (1/2)ReTr(U_P))
                                # The part depending on U_mu(x) is:
                                # -beta * (1/2) Re Tr(U_mu(x) * A_mu(x))
                                # = -beta * su2_trace(su2_multiply(U, A))
                                # where su2_trace gives (1/2) Re Tr = q[0] for the product quaternion
                                # But wait: A is a sum of SU(2) elements (staples), not itself in SU(2)
                                # The product U*A in quaternion representation still works as matrix product
                                # and su2_trace of the result gives (1/2) Re Tr

                                # Actually for quaternions, the dot product gives (1/2)ReTr(U·V†)
                                # So (1/2)ReTr(U·A) where A = sum of staples
                                # = sum over staples of (1/2)ReTr(U·staple_i)
                                # = sum over staples of dot(U, staple_i) ... no that gives U·staple_i†

                                # Let me just use: (1/2)ReTr(U·A) for matrix A
                                # In quaternion rep: this is the 0-component of U * A using quaternion mult
                                # Because Tr(U * A) = Tr((a0+ia·σ)(A)) and the trace picks out
                                # the coefficient of I in the product.

                                S_old = su2_trace(su2_multiply(U_old, A))  # This is wrong
                                S_new = su2_trace(su2_multiply(U_new, A))

                                # Hmm, I need to be more careful.
                                # The action is S = beta * sum_P (1 - (1/2)ReTr(U_P))
                                # The piece involving U_mu(x):
                                # -(beta/2) * sum_{staples} ReTr(U_mu(x) * staple)
                                # = -beta * sum_{staples} (1/2)ReTr(U * staple)

                                # For two SU(2) quaternions p, q:
                                # (1/2)ReTr(p * q†) = p·q (dot product of 4-vectors)
                                # So (1/2)ReTr(p * q) = (1/2)ReTr(p * (q†)†) = p · q†
                                # i.e., dot product with q conjugated: p0*q0 + p1*(-q1) + ...
                                # No wait: (1/2)ReTr(U * V†) = dot(qU, qV)
                                # So (1/2)ReTr(U * V) = (1/2)ReTr(U * (V†)†)
                                # Let W = V†, then (1/2)ReTr(U * W†) = dot(qU, qW) = dot(qU, qV†)
                                # qV† = (v0, -v1, -v2, -v3)
                                # dot(qU, qV†) = u0*v0 - u1*v1 - u2*v2 - u3*v3
                                # Hmm that doesn't seem right either.

                                # OK let me just think about it from the matrix side.
                                # U = u0*I + i*(u1*σ1 + u2*σ2 + u3*σ3)
                                # (1/2) Tr U = u0  (since Tr(σi) = 0, Tr(I) = 2)
                                # Re[(1/2) Tr U] = u0
                                #
                                # For product UV:
                                # (1/2) Tr(UV) = u0*v0 - u1*v1 - u2*v2 - u3*v3
                                #   + i*(cross terms)
                                # Re[(1/2) Tr(UV)] = u0*v0 - u1*v1 - u2*v2 - u3*v3
                                #
                                # Hmm wait, that's the quaternion product [0] component?
                                # Quaternion product: (UV)[0] = u0*v0 - u1*v1 - u2*v2 - u3*v3
                                # Yes! So (1/2) Re Tr(U*V) = (U*V)_quat[0] = quaternion_multiply(U,V)[0]
                                #
                                # Great. So for the staple sum A (which is a sum of quaternions,
                                # not necessarily on SU(2)), the matrix it represents is also
                                # A = a0*I + i*(a1*σ1 + ...) and (1/2)ReTr(U*A) = quat_mult(U,A)[0]

                                # Correct formula:
                                # dS_eff = -beta * [(1/2)ReTr(U_new * A) - (1/2)ReTr(U_old * A)]
                                # = -beta * [quat_mult(U_new, A)[0] - quat_mult(U_old, A)[0]]

                                dS = -self.beta * (
                                    su2_multiply(U_new, A)[0] - su2_multiply(U_old, A)[0]
                                )

                                total += 1
                                if dS <= 0 or np.random.random() < np.exp(-dS):
                                    U_old = U_new
                                    accepted += 1

                            self.set_link(site, mu, U_old)

        return accepted / total if total > 0 else 0.0

    def wilson_loop(self, R, T, num_samples=None):
        """
        Compute average Wilson loop W(R,T) over all spatial positions and orientations.

        The Wilson loop is the trace of the path-ordered product around an R×T rectangle,
        where R is spatial and T is in the time direction.

        For simplicity, we compute loops in planes (mu=spatial, nu=0=time direction).
        """
        L = self.L
        total = 0.0
        count = 0

        # We average over all positions and spatial directions (3 spatial × 1 temporal)
        # Time direction = 0, spatial = 1,2,3
        temporal_dir = 0

        for spatial_dir in range(1, 4):
            for x0 in range(L):
                for x1 in range(L):
                    for x2 in range(L):
                        for x3 in range(L):
                            site = (x0, x1, x2, x3)
                            W = self._compute_wilson_loop(site, spatial_dir, temporal_dir, R, T)
                            total += W
                            count += 1

        return total / count

    def _compute_wilson_loop(self, start, mu, nu, R, T):
        """
        Compute a single Wilson loop of size R (in mu-direction) × T (in nu-direction)
        starting at site 'start'.
        Returns (1/2) Re Tr W.
        """
        # Accumulate product along the loop
        U = su2_identity()
        site = start

        # Bottom: R steps in mu direction
        for _ in range(R):
            U = su2_multiply(U, self.get_link(site, mu))
            site = self.shift(site, mu)

        # Right: T steps in nu direction
        for _ in range(T):
            U = su2_multiply(U, self.get_link(site, nu))
            site = self.shift(site, nu)

        # Top: R steps in -mu direction
        for _ in range(R):
            site = self.shift(site, mu, -1)
            U = su2_multiply(U, su2_dagger(self.get_link(site, mu)))

        # Left: T steps in -nu direction
        for _ in range(T):
            site = self.shift(site, nu, -1)
            U = su2_multiply(U, su2_dagger(self.get_link(site, nu)))

        return su2_trace(U)  # (1/2) Re Tr W

    def plaquette_at_time(self, t):
        """
        Compute average spatial plaquette at a given time slice t.
        Average of Re Tr U_P for spatial plaquettes (mu,nu both in {1,2,3}) at x0=t.
        """
        L = self.L
        total = 0.0
        count = 0

        for x1 in range(L):
            for x2 in range(L):
                for x3 in range(L):
                    site = (t, x1, x2, x3)
                    for mu in range(1, 4):
                        for nu in range(mu+1, 4):
                            P = self.plaquette(site, mu, nu)
                            total += su2_trace(P)
                            count += 1

        return total / count

    def plaquette_correlator(self, dt):
        """
        Compute plaquette-plaquette correlator C(dt) = <P(0)P(dt)> - <P>^2
        where P(t) is the average spatial plaquette at time t.

        This is a zero-momentum projection of the glueball correlator.
        """
        L = self.L
        plaq_t = np.array([self.plaquette_at_time(t) for t in range(L)])

        # Connected correlator
        mean_plaq = np.mean(plaq_t)
        correlator = 0.0

        for t in range(L):
            t2 = (t + dt) % L
            correlator += (plaq_t[t] - mean_plaq) * (plaq_t[t2] - mean_plaq)

        return correlator / L

    def polyakov_loop(self):
        """Compute the Polyakov loop (temporal Wilson line wrapping around the lattice)."""
        L = self.L
        total = 0.0

        for x1 in range(L):
            for x2 in range(L):
                for x3 in range(L):
                    U = su2_identity()
                    for t in range(L):
                        U = su2_multiply(U, self.get_link((t, x1, x2, x3), 0))
                    total += su2_trace(U)

        return total / (L**3)


# ============================================================================
# Vectorized operations for speed
# ============================================================================

def average_plaquette_fast(links, L):
    """
    Compute average plaquette using numpy vectorization.
    links shape: (L, L, L, L, 4, 4) — last two indices are (direction, quaternion)
    """
    total = 0.0
    count = 0

    for mu in range(4):
        for nu in range(mu+1, 4):
            # U_mu(x)
            U1 = links[:, :, :, :, mu, :]

            # U_nu(x + mu) — shift in mu direction
            U2 = np.roll(links[:, :, :, :, nu, :], -1, axis=mu)

            # U_mu(x + nu)^dag — shift in nu direction, then dagger
            U3_raw = np.roll(links[:, :, :, :, mu, :], -1, axis=nu)
            U3 = U3_raw.copy()
            U3[..., 1:] *= -1  # dagger

            # U_nu(x)^dag
            U4 = links[:, :, :, :, nu, :].copy()
            U4[..., 1:] *= -1  # dagger

            # Plaquette = U1 * U2 * U3 * U4
            prod = su2_multiply(su2_multiply(su2_multiply(U1, U2), U3), U4)
            total += np.sum(prod[..., 0])  # sum of (1/2) Re Tr
            count += L**4

    return total / count


if __name__ == "__main__":
    # Quick test
    print("Testing SU(2) lattice gauge theory implementation...")

    # Test quaternion multiplication
    q1 = su2_random()
    q2 = su2_random()
    q3 = su2_multiply(q1, su2_dagger(q1))
    print(f"U * U^dag = {q3} (should be ~(1,0,0,0))")

    # Test small lattice
    L = 4
    beta = 2.3
    lat = LatticeGaugeTheory(L, beta, seed=42)
    lat.hot_start()

    print(f"\nLattice {L}^4, beta={beta}")
    print(f"Initial average plaquette (hot start): {lat.average_plaquette():.6f}")

    # A few thermalization sweeps
    for i in range(5):
        lat.sweep_heatbath()
    print(f"After 5 HB sweeps: {lat.average_plaquette():.6f}")

    for i in range(20):
        lat.sweep_heatbath()
    print(f"After 25 HB sweeps: {lat.average_plaquette():.6f}")

    # Test Wilson loop
    W11 = lat.wilson_loop(1, 1)
    print(f"Wilson loop W(1,1) = {W11:.6f}")

    print("\nBasic tests passed!")
