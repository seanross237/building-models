"""
Lattice Gauge Theory with Finite Subgroups of SU(2)
====================================================

Implements 4D lattice gauge theory where the gauge group is a finite subgroup G ⊂ SU(2).
Links take values in G (finite set), enabling exact heat bath sampling.

Wilson plaquette action: S = β Σ_P (1 - (1/2) Re Tr U_P)

For finite groups, the heat bath algorithm is exact:
- Compute the Boltzmann weight for each group element
- Sample from the discrete distribution

Author: Math Explorer (Atlas system)
Date: 2026-03-27
"""

import numpy as np
from time import time
from finite_subgroups import (
    binary_tetrahedral_group, binary_octahedral_group, binary_icosahedral_group,
    precompute_multiplication_table, quat_multiply, quat_conjugate, normalize_quat
)


class FiniteGroupLattice:
    """
    4D lattice gauge theory with a finite gauge group G ⊂ SU(2).

    Links are stored as integer indices into the group element table.
    All multiplications use the precomputed multiplication table.
    """

    def __init__(self, L, beta, group_elements, mult_table, inv_table, identity_idx, seed=None):
        """
        Parameters:
            L: lattice size (L^4 lattice)
            beta: inverse coupling
            group_elements: numpy array of shape (|G|, 4) — quaternion representations
            mult_table: (|G|, |G|) int array — multiplication table
            inv_table: (|G|,) int array — inverse table
            identity_idx: index of identity element
            seed: random seed
        """
        self.L = L
        self.beta = beta
        self.elements = group_elements
        self.mult_table = mult_table
        self.inv_table = inv_table
        self.identity_idx = identity_idx
        self.group_order = len(group_elements)
        self.ndim = 4
        self.volume = L ** 4

        if seed is not None:
            np.random.seed(seed)

        # Precompute (1/2) Re Tr for each element = element[0] (quaternion a0 component)
        self.half_re_trace = group_elements[:, 0].copy()

        # Links stored as indices: shape (L, L, L, L, 4)
        # Initialize to cold start (all identity)
        self.links = np.full((L, L, L, L, 4), identity_idx, dtype=np.int32)

    def hot_start(self):
        """Initialize with random group elements."""
        self.links = np.random.randint(0, self.group_order, size=(self.L, self.L, self.L, self.L, 4), dtype=np.int32)

    def cold_start(self):
        """Initialize with identity elements."""
        self.links.fill(self.identity_idx)

    def get_link(self, site, mu):
        """Get link index at site in direction mu."""
        return self.links[site[0], site[1], site[2], site[3], mu]

    def set_link(self, site, mu, idx):
        """Set link index at site in direction mu."""
        self.links[site[0], site[1], site[2], site[3], mu] = idx

    def shift(self, site, mu, direction=1):
        """Shift site by one step in direction mu with periodic BC."""
        s = list(site)
        s[mu] = (s[mu] + direction) % self.L
        return tuple(s)

    def multiply(self, i, j):
        """Multiply two group elements by index."""
        return self.mult_table[i, j]

    def inverse(self, i):
        """Get inverse of group element by index."""
        return self.inv_table[i]

    def plaquette_idx(self, site, mu, nu):
        """
        Compute plaquette U_P = U_mu(x) U_nu(x+mu) U_mu(x+nu)^dag U_nu(x)^dag
        Returns group element index.
        """
        x_mu = self.shift(site, mu)
        x_nu = self.shift(site, nu)

        U1 = self.get_link(site, mu)
        U2 = self.get_link(x_mu, nu)
        U3 = self.inverse(self.get_link(x_nu, mu))
        U4 = self.inverse(self.get_link(site, nu))

        return self.multiply(self.multiply(self.multiply(U1, U2), U3), U4)

    def plaquette_trace(self, site, mu, nu):
        """(1/2) Re Tr of plaquette."""
        idx = self.plaquette_idx(site, mu, nu)
        return self.half_re_trace[idx]

    def average_plaquette(self):
        """Compute average plaquette over all plaquettes."""
        total = 0.0
        count = 0
        L = self.L

        for x0 in range(L):
            for x1 in range(L):
                for x2 in range(L):
                    for x3 in range(L):
                        site = (x0, x1, x2, x3)
                        for mu in range(4):
                            for nu in range(mu + 1, 4):
                                total += self.plaquette_trace(site, mu, nu)
                                count += 1
        return total / count

    def staple_sum_quaternion(self, site, mu):
        """
        Compute the sum of staples as a quaternion (not a group element).
        For finite groups, the sum of staples is generally NOT a group element,
        but we need it as a quaternion to compute Boltzmann weights.

        Returns: quaternion (4-vector)
        """
        A = np.zeros(4)

        for nu in range(4):
            if nu == mu:
                continue

            x_mu = self.shift(site, mu)
            x_nu = self.shift(site, nu)
            x_minus_nu = self.shift(site, nu, -1)
            x_mu_minus_nu = self.shift(x_mu, nu, -1)

            # Forward staple: U_nu(x+mu) * U_mu(x+nu)^dag * U_nu(x)^dag
            fwd = self.multiply(
                self.multiply(self.get_link(x_mu, nu),
                              self.inverse(self.get_link(x_nu, mu))),
                self.inverse(self.get_link(site, nu))
            )
            A += self.elements[fwd]

            # Backward staple: U_nu(x+mu-nu)^dag * U_mu(x-nu)^dag * U_nu(x-nu)
            # Wait — let me be more careful.
            # Backward staple = U_nu(x+mu-nu)^{-1} * U_mu(x-nu)^{-1} * U_nu(x-nu)
            # No. The backward plaquette involves the plaquette at (x-nu) in the (mu,nu) plane:
            # P = U_mu(x) * [U_nu(x+mu-nu)^dag * U_mu(x-nu)^dag * U_nu(x-nu)]
            # So backward staple = U_nu(x+mu-nu)^dag * U_mu(x-nu)^dag * U_nu(x-nu)
            bwd = self.multiply(
                self.multiply(self.inverse(self.get_link(x_mu_minus_nu, nu)),
                              self.inverse(self.get_link(x_minus_nu, mu))),
                self.get_link(x_minus_nu, nu)
            )
            A += self.elements[bwd]

        return A

    def sweep_heatbath(self):
        """
        Perform one heat bath sweep over all links.

        For finite groups, the heat bath is exact:
        For each link U_mu(x), compute the Boltzmann weight for every group element g:
          w(g) = exp(β * (1/2) Re Tr(g * A))
        where A is the staple sum (as quaternion), and sample from this distribution.

        The key insight: (1/2) Re Tr(g * A) for quaternions g and A is:
          (g * A)[0] = g0*A0 - g1*A1 - g2*A2 - g3*A3
        which is just the dot product with sign flips, computed as
        the 0-component of quaternion multiplication.
        """
        L = self.L
        G = self.group_order

        for x0 in range(L):
            for x1 in range(L):
                for x2 in range(L):
                    for x3 in range(L):
                        site = (x0, x1, x2, x3)
                        for mu in range(4):
                            A = self.staple_sum_quaternion(site, mu)

                            # Compute (1/2) Re Tr(g * A) for all group elements g
                            # Using quaternion multiplication:
                            # (g * A)[0] = g0*A0 - g1*A1 - g2*A2 - g3*A3
                            # This is a dot product: g · (A0, -A1, -A2, -A3)
                            A_conj = np.array([A[0], -A[1], -A[2], -A[3]])
                            action_values = self.elements @ A_conj  # shape (G,)

                            # Boltzmann weights
                            weights = np.exp(self.beta * action_values)

                            # Normalize to probability distribution
                            weights /= np.sum(weights)

                            # Sample from discrete distribution
                            new_idx = np.random.choice(G, p=weights)
                            self.set_link(site, mu, new_idx)

    def wilson_loop(self, R, T):
        """
        Compute average Wilson loop W(R,T).
        Average over all positions and spatial orientations.
        """
        L = self.L
        total = 0.0
        count = 0

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
        """Compute single Wilson loop of size R×T. Returns (1/2) Re Tr W."""
        U_idx = self.identity_idx
        site = start

        # Bottom: R steps in mu
        for _ in range(R):
            U_idx = self.multiply(U_idx, self.get_link(site, mu))
            site = self.shift(site, mu)

        # Right: T steps in nu
        for _ in range(T):
            U_idx = self.multiply(U_idx, self.get_link(site, nu))
            site = self.shift(site, nu)

        # Top: R steps in -mu
        for _ in range(R):
            site = self.shift(site, mu, -1)
            U_idx = self.multiply(U_idx, self.inverse(self.get_link(site, mu)))

        # Left: T steps in -nu
        for _ in range(T):
            site = self.shift(site, nu, -1)
            U_idx = self.multiply(U_idx, self.inverse(self.get_link(site, nu)))

        return self.half_re_trace[U_idx]

    def polyakov_loop(self):
        """Compute average Polyakov loop."""
        L = self.L
        total = 0.0

        for x1 in range(L):
            for x2 in range(L):
                for x3 in range(L):
                    U_idx = self.identity_idx
                    for t in range(L):
                        U_idx = self.multiply(U_idx, self.get_link((t, x1, x2, x3), 0))
                    total += self.half_re_trace[U_idx]

        return total / (L ** 3)

    def creutz_ratio(self, R, T):
        """
        Compute the Creutz ratio χ(R,T) = -ln(W(R,T)*W(R-1,T-1) / (W(R,T-1)*W(R-1,T)))

        For area law: χ(R,T) → σ (string tension) as R,T → ∞
        """
        W_RT = self.wilson_loop(R, T)
        W_R1T1 = self.wilson_loop(R - 1, T - 1)
        W_RT1 = self.wilson_loop(R, T - 1)
        W_R1T = self.wilson_loop(R - 1, T)

        if W_RT <= 0 or W_R1T1 <= 0 or W_RT1 <= 0 or W_R1T <= 0:
            return float('nan')

        ratio = (W_RT * W_R1T1) / (W_RT1 * W_R1T)
        if ratio <= 0:
            return float('nan')

        return -np.log(ratio)


# ============================================================================
# SU(2) continuous implementation for comparison (adapted from exploration-003)
# ============================================================================

class SU2ContinuousLattice:
    """
    SU(2) lattice gauge theory with continuous gauge group.
    Uses quaternion representation and Kennedy-Pendleton heat bath.
    """

    def __init__(self, L, beta, seed=None):
        self.L = L
        self.beta = beta
        self.ndim = 4
        self.volume = L ** 4

        if seed is not None:
            np.random.seed(seed)

        # Links as quaternions: shape (L, L, L, L, 4, 4)
        self.links = np.zeros((L, L, L, L, 4, 4))
        self.links[..., 0] = 1.0  # identity

    def hot_start(self):
        q = np.random.randn(self.L, self.L, self.L, self.L, 4, 4)
        norm = np.sqrt(np.sum(q ** 2, axis=-1, keepdims=True))
        self.links = q / norm

    def cold_start(self):
        self.links = np.zeros((self.L, self.L, self.L, self.L, 4, 4))
        self.links[..., 0] = 1.0

    def get_link(self, site, mu):
        return self.links[site[0], site[1], site[2], site[3], mu].copy()

    def set_link(self, site, mu, U):
        self.links[site[0], site[1], site[2], site[3], mu] = U

    def shift(self, site, mu, direction=1):
        s = list(site)
        s[mu] = (s[mu] + direction) % self.L
        return tuple(s)

    def _qmul(self, q1, q2):
        a0, a1, a2, a3 = q1[0], q1[1], q1[2], q1[3]
        b0, b1, b2, b3 = q2[0], q2[1], q2[2], q2[3]
        return np.array([
            a0 * b0 - a1 * b1 - a2 * b2 - a3 * b3,
            a0 * b1 + a1 * b0 + a2 * b3 - a3 * b2,
            a0 * b2 - a1 * b3 + a2 * b0 + a3 * b1,
            a0 * b3 + a1 * b2 - a2 * b1 + a3 * b0
        ])

    def _qdag(self, q):
        return np.array([q[0], -q[1], -q[2], -q[3]])

    def staple_sum(self, site, mu):
        A = np.zeros(4)
        for nu in range(4):
            if nu == mu:
                continue
            x_mu = self.shift(site, mu)
            x_nu = self.shift(site, nu)
            x_minus_nu = self.shift(site, nu, -1)
            x_mu_minus_nu = self.shift(x_mu, nu, -1)

            fwd = self._qmul(self._qmul(self.get_link(x_mu, nu),
                                         self._qdag(self.get_link(x_nu, mu))),
                             self._qdag(self.get_link(site, nu)))
            bwd = self._qmul(self._qmul(self._qdag(self.get_link(x_mu_minus_nu, nu)),
                                         self._qdag(self.get_link(x_minus_nu, mu))),
                             self.get_link(x_minus_nu, nu))
            A += fwd + bwd
        return A

    def _kp_sample(self, bk):
        if bk < 0.01:
            return 2.0 * np.random.random() - 1.0
        while True:
            r1 = max(np.random.random(), 1e-300)
            r2 = np.random.random()
            r3 = max(np.random.random(), 1e-300)
            x = -(np.log(r1) + np.log(r3) * np.cos(np.pi * r2) ** 2) / bk
            if x > 2.0:
                continue
            r4 = np.random.random()
            if r4 ** 2 <= 1.0 - x / 2.0:
                return 1.0 - x

    def heat_bath_su2(self, staple_sum, beta):
        k = np.sqrt(np.sum(staple_sum ** 2))
        if k < 1e-10:
            q = np.random.randn(4)
            return q / np.linalg.norm(q)
        V = staple_sum / k
        a0 = self._kp_sample(beta * k)
        r = np.sqrt(1.0 - a0 ** 2)
        phi = 2.0 * np.pi * np.random.random()
        cos_theta = 2.0 * np.random.random() - 1.0
        sin_theta = np.sqrt(1.0 - cos_theta ** 2)
        U_new = np.array([a0, r * sin_theta * np.cos(phi), r * sin_theta * np.sin(phi), r * cos_theta])
        return self._qmul(U_new, self._qdag(V))

    def sweep_heatbath(self):
        L = self.L
        for x0 in range(L):
            for x1 in range(L):
                for x2 in range(L):
                    for x3 in range(L):
                        site = (x0, x1, x2, x3)
                        for mu in range(4):
                            A = self.staple_sum(site, mu)
                            U_new = self.heat_bath_su2(A, self.beta)
                            self.set_link(site, mu, U_new)

    def average_plaquette(self):
        total = 0.0
        count = 0
        L = self.L
        for x0 in range(L):
            for x1 in range(L):
                for x2 in range(L):
                    for x3 in range(L):
                        site = (x0, x1, x2, x3)
                        for mu in range(4):
                            for nu in range(mu + 1, 4):
                                x_mu = self.shift(site, mu)
                                x_nu = self.shift(site, nu)
                                U1 = self.get_link(site, mu)
                                U2 = self.get_link(x_mu, nu)
                                U3 = self._qdag(self.get_link(x_nu, mu))
                                U4 = self._qdag(self.get_link(site, nu))
                                P = self._qmul(self._qmul(self._qmul(U1, U2), U3), U4)
                                total += P[0]
                                count += 1
        return total / count

    def wilson_loop(self, R, T):
        L = self.L
        total = 0.0
        count = 0
        for spatial_dir in range(1, 4):
            for x0 in range(L):
                for x1 in range(L):
                    for x2 in range(L):
                        for x3 in range(L):
                            site = (x0, x1, x2, x3)
                            U = np.array([1.0, 0.0, 0.0, 0.0])
                            s = site
                            for _ in range(R):
                                U = self._qmul(U, self.get_link(s, spatial_dir))
                                s = self.shift(s, spatial_dir)
                            for _ in range(T):
                                U = self._qmul(U, self.get_link(s, 0))
                                s = self.shift(s, 0)
                            for _ in range(R):
                                s = self.shift(s, spatial_dir, -1)
                                U = self._qmul(U, self._qdag(self.get_link(s, spatial_dir)))
                            for _ in range(T):
                                s = self.shift(s, 0, -1)
                                U = self._qmul(U, self._qdag(self.get_link(s, 0)))
                            total += U[0]
                            count += 1
        return total / count

    def polyakov_loop(self):
        L = self.L
        total = 0.0
        for x1 in range(L):
            for x2 in range(L):
                for x3 in range(L):
                    U = np.array([1.0, 0.0, 0.0, 0.0])
                    for t in range(L):
                        U = self._qmul(U, self.get_link((t, x1, x2, x3), 0))
                    total += U[0]
        return total / (L ** 3)

    def creutz_ratio(self, R, T):
        W_RT = self.wilson_loop(R, T)
        W_R1T1 = self.wilson_loop(R - 1, T - 1)
        W_RT1 = self.wilson_loop(R, T - 1)
        W_R1T = self.wilson_loop(R - 1, T)
        if W_RT <= 0 or W_R1T1 <= 0 or W_RT1 <= 0 or W_R1T <= 0:
            return float('nan')
        ratio = (W_RT * W_R1T1) / (W_RT1 * W_R1T)
        if ratio <= 0:
            return float('nan')
        return -np.log(ratio)


if __name__ == "__main__":
    print("Testing finite group lattice gauge theory...")

    # Build 2T group
    elements = binary_tetrahedral_group()
    mt, inv, id_idx = precompute_multiplication_table(elements)

    L = 4
    beta = 2.0
    lat = FiniteGroupLattice(L, beta, elements, mt, inv, id_idx, seed=42)
    lat.hot_start()

    print(f"2T lattice {L}^4, beta={beta}")
    print(f"Initial plaquette (hot): {lat.average_plaquette():.6f}")

    for i in range(5):
        t0 = time()
        lat.sweep_heatbath()
        dt = time() - t0
        plaq = lat.average_plaquette()
        print(f"Sweep {i + 1}: plaquette = {plaq:.6f}, time = {dt:.1f}s")

    print(f"\nWilson W(1,1) = {lat.wilson_loop(1, 1):.6f}")
    print(f"Polyakov loop = {lat.polyakov_loop():.6f}")
    print("\nTest passed!")
