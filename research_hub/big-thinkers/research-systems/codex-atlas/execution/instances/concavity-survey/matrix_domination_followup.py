"""
Follow-up analysis on matrix domination test.

Key findings from first run:
  - H(I) >= H(Q) (PSD) FAILS universally — 100% violation rate
  - Majorization lambda(H(Q)) ≺ lambda(H(I)) appears to HOLD
  - Eigenvalue-by-eigenvalue inequality needs checking

This script does deeper analysis:
1. Eigenvalue-by-eigenvalue comparison (all sorted eigenvalues)
2. Larger majorization test (1000 samples per dimension)
3. Characterize the violating eigenvectors
4. Check anti-instanton configs specifically
"""

import numpy as np
from scipy.linalg import expm, eigvalsh
import time

np.random.seed(42)

# ============================================================================
# SU(2) and lattice setup (same as main test)
# ============================================================================

sigma = [
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
]
T_gen = [1j * s / 2 for s in sigma]
I2 = np.eye(2, dtype=complex)

def su2_from_vec(v):
    return sum(vi * ti for vi, ti in zip(v, T_gen))

def Ad(Q, v_mat):
    return Q @ v_mat @ Q.conj().T

def re_tr(M):
    return np.trace(M).real

def random_SU2():
    a = np.random.randn(4)
    a /= np.linalg.norm(a)
    return (a[0] * I2 + 1j * (a[1] * sigma[0] + a[2] * sigma[1] + a[3] * sigma[2]))


class Lattice:
    def __init__(self, L, d):
        self.L = L
        self.d = d
        self.Nsites = L ** d
        self.Nlinks = d * self.Nsites
        self.Ndof = 3 * self.Nlinks
        self.plaquettes = self._build_plaquettes()
        self.Nplaq = len(self.plaquettes)

    def site_index(self, x):
        idx = 0
        for i in range(self.d):
            idx = idx * self.L + (x[i] % self.L)
        return idx

    def site_coords(self, idx):
        x = []
        r = idx
        for i in range(self.d):
            x.append(r % self.L)
            r //= self.L
        return list(reversed(x))

    def link_index(self, x, mu):
        return mu * self.Nsites + self.site_index(x)

    def neighbor(self, x, mu, direction=1):
        y = list(x)
        y[mu] = (y[mu] + direction) % self.L
        return y

    def _build_plaquettes(self):
        plaquettes = []
        for s in range(self.Nsites):
            x = self.site_coords(s)
            for mu in range(self.d):
                for nu in range(mu + 1, self.d):
                    e1 = self.link_index(x, mu)
                    e2 = self.link_index(self.neighbor(x, mu), nu)
                    e3 = self.link_index(self.neighbor(x, nu), mu)
                    e4 = self.link_index(x, nu)
                    plaquettes.append((e1, e2, e3, e4))
        return plaquettes


def build_hessian(lat, Q, beta=1.0):
    Ndof = lat.Ndof
    H = np.zeros((Ndof, Ndof))

    for (e1, e2, e3, e4) in lat.plaquettes:
        U = Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T
        P2 = Q[e1].copy()
        P3 = Q[e1] @ Q[e2] @ Q[e3].conj().T

        edges = [e1, e2, e3, e4]
        signs = [1, 1, -1, -1]
        Ad_ops = [I2, P2, P3, U]

        wka = np.zeros((4, 3, 2, 2), dtype=complex)
        for k in range(4):
            for a in range(3):
                wka[k, a] = signs[k] * Ad(Ad_ops[k], T_gen[a])

        for k in range(4):
            for a in range(3):
                i = 3 * edges[k] + a
                for l in range(4):
                    for b in range(3):
                        j = 3 * edges[l] + b
                        if k == l:
                            val = 0.5 * (re_tr(wka[k, a] @ wka[k, b] @ U) +
                                         re_tr(wka[k, b] @ wka[k, a] @ U))
                        elif k < l:
                            val = re_tr(wka[k, a] @ wka[l, b] @ U)
                        else:
                            val = re_tr(wka[l, b] @ wka[k, a] @ U)
                        H[i, j] += -(beta / 2) * val

    H = (H + H.T) / 2
    return H


def make_identity_config(lat):
    Q = np.zeros((lat.Nlinks, 2, 2), dtype=complex)
    for i in range(lat.Nlinks):
        Q[i] = I2.copy()
    return Q


def make_random_config(lat):
    Q = np.zeros((lat.Nlinks, 2, 2), dtype=complex)
    for i in range(lat.Nlinks):
        Q[i] = random_SU2()
    return Q


def make_anti_instanton(lat, axes=(0, 0, 2, 1)):
    """Anti-instanton: Q_mu = i*sigma_{axes[mu]} for each direction."""
    Q = np.zeros((lat.Nlinks, 2, 2), dtype=complex)
    for i in range(lat.Nlinks):
        mu = i // lat.Nsites  # direction of this link
        if mu < len(axes):
            Q[i] = 1j * sigma[axes[mu]]
        else:
            Q[i] = I2.copy()
    return Q


# ============================================================================
# Eigenvalue-by-eigenvalue comparison
# ============================================================================

def eigenvalue_by_eigenvalue_test(lat, H_I, N_samples=500, beta=1.0):
    """
    For each sample Q, sort eigenvalues of H(I) and H(Q) in descending order.
    Check whether eig_I[k] >= eig_Q[k] for all k (eigenvalue-by-eigenvalue).
    This is stronger than lambda_max comparison but weaker than PSD domination.
    """
    print("\n" + "=" * 70)
    print(f"EIGENVALUE-BY-EIGENVALUE TEST: d={lat.d}, N={N_samples}")
    print("=" * 70)

    eigs_I = np.sort(eigvalsh(H_I))[::-1]  # Descending

    violations_count = 0
    max_violation_per_rank = np.zeros(lat.Ndof)  # worst violation at each rank
    violation_ranks = []

    for trial in range(N_samples):
        Q = make_random_config(lat)
        H_Q = build_hessian(lat, Q, beta)
        eigs_Q = np.sort(eigvalsh(H_Q))[::-1]

        diffs = eigs_I - eigs_Q  # Should be >= 0 for domination
        bad = np.where(diffs < -1e-10)[0]
        if len(bad) > 0:
            violations_count += 1
            violation_ranks.extend(bad.tolist())
            for r in bad:
                if diffs[r] < max_violation_per_rank[r]:
                    max_violation_per_rank[r] = diffs[r]

        if (trial + 1) % 100 == 0:
            print(f"  [{trial+1}/{N_samples}] violations={violations_count}")

    print(f"\n  RESULT: {violations_count}/{N_samples} configs have eigenvalue-by-eigenvalue violations")

    if violations_count > 0:
        # Which ranks are violated?
        unique_ranks = sorted(set(violation_ranks))
        print(f"\n  Violated ranks (0=top eigenvalue): {unique_ranks[:20]}{'...' if len(unique_ranks) > 20 else ''}")
        print(f"  Total unique violated ranks: {len(unique_ranks)}/{lat.Ndof}")

        print(f"\n  Worst violation by rank (top 10):")
        worst_ranks = np.argsort(max_violation_per_rank)[:10]
        for r in worst_ranks:
            if max_violation_per_rank[r] < 0:
                print(f"    Rank {r}: worst = {max_violation_per_rank[r]:.6f}, eig_I={eigs_I[r]:.6f}")
    else:
        print("  *** Eigenvalue-by-eigenvalue ordering HOLDS for all samples ***")

    return violations_count, max_violation_per_rank


# ============================================================================
# Thorough majorization test
# ============================================================================

def majorization_test_thorough(lat, H_I, N_samples=1000, beta=1.0):
    """
    Check weak majorization: sum_{k=1}^m lambda_k(H(Q)) <= sum_{k=1}^m lambda_k(H(I))
    for all m = 1, ..., Ndof (eigenvalues sorted descending).
    """
    print("\n" + "=" * 70)
    print(f"THOROUGH MAJORIZATION TEST: d={lat.d}, N={N_samples}")
    print("=" * 70)

    eigs_I = np.sort(eigvalsh(H_I))[::-1]
    cum_I = np.cumsum(eigs_I)

    violations = 0
    worst_gap = 0.0
    worst_m = -1

    for trial in range(N_samples):
        Q = make_random_config(lat)
        H_Q = build_hessian(lat, Q, beta)
        eigs_Q = np.sort(eigvalsh(H_Q))[::-1]
        cum_Q = np.cumsum(eigs_Q)

        gaps = cum_Q - cum_I  # Should be <= 0 for majorization
        worst_idx = np.argmax(gaps)
        if gaps[worst_idx] > 1e-10:
            violations += 1
            if gaps[worst_idx] > worst_gap:
                worst_gap = gaps[worst_idx]
                worst_m = worst_idx

        if (trial + 1) % 200 == 0:
            print(f"  [{trial+1}/{N_samples}] violations={violations}")

    print(f"\n  RESULT: Majorization violations = {violations}/{N_samples}")
    if violations == 0:
        print("  *** Weak majorization HOLDS for all samples ***")
    else:
        print(f"  Worst violation: gap = {worst_gap:.8f} at partial sum index m={worst_m}")

    # Also check: what's the tightest margin?
    print(f"\n  Checking margins (how close is majorization to failing)...")
    min_margins = np.full(lat.Ndof, np.inf)
    for trial in range(min(200, N_samples)):
        Q = make_random_config(lat)
        H_Q = build_hessian(lat, Q, beta)
        eigs_Q = np.sort(eigvalsh(H_Q))[::-1]
        cum_Q = np.cumsum(eigs_Q)
        margins = cum_I - cum_Q
        min_margins = np.minimum(min_margins, margins)

    print(f"  Tightest margin across all partial sums:")
    print(f"    Overall min margin: {min_margins.min():.6f}")
    tight_idx = np.argmin(min_margins)
    print(f"    At partial sum index m={tight_idx}: margin={min_margins[tight_idx]:.6f}")

    return violations


# ============================================================================
# Anti-instanton specific test
# ============================================================================

def anti_instanton_test(lat, H_I, beta=1.0):
    """Test matrix domination specifically against anti-instanton configs."""
    print("\n" + "=" * 70)
    print(f"ANTI-INSTANTON TEST: d={lat.d}")
    print("=" * 70)

    if lat.d < 4:
        print("  Skipping (anti-instanton configs are most relevant for d=4)")
        return

    eigs_I = np.sort(eigvalsh(H_I))[::-1]
    cum_I = np.cumsum(eigs_I)

    configs = [
        ("(0,0,2,1)", (0, 0, 2, 1)),
        ("(1,1,0,2)", (1, 1, 0, 2)),
        ("(0,0,1,2)", (0, 0, 1, 2)),
        ("(0,1,2,0)", (0, 1, 2, 0)),
    ]

    for name, axes in configs:
        Q = make_anti_instanton(lat, axes)
        H_Q = build_hessian(lat, Q, beta)
        eigs_Q = np.sort(eigvalsh(H_Q))[::-1]
        diff = H_I - H_Q
        eigs_diff = eigvalsh(diff)

        print(f"\n  Config {name}:")
        print(f"    lambda_max(H(Q)) = {eigs_Q[0]:.6f} (vs H(I): {eigs_I[0]:.6f})")
        print(f"    min_eig(H(I)-H(Q)) = {eigs_diff[0]:.6f} (PSD: {'YES' if eigs_diff[0] > -1e-10 else 'NO'})")

        cum_Q = np.cumsum(eigs_Q)
        margins = cum_I - cum_Q
        print(f"    Majorization min margin: {margins.min():.6f} (at index {np.argmin(margins)})")

        # Eigenvalue-by-eigenvalue
        evev_diffs = eigs_I - eigs_Q
        evev_violations = np.sum(evev_diffs < -1e-10)
        print(f"    Eigenvalue-by-eigenvalue violations: {evev_violations}/{lat.Ndof}")
        if evev_violations > 0:
            worst_rank = np.argmin(evev_diffs)
            print(f"    Worst: rank {worst_rank}, gap={evev_diffs[worst_rank]:.6f}")


# ============================================================================
# Summary of what the violation eigenvectors look like
# ============================================================================

def characterize_violations(lat, H_I, N_samples=20, beta=1.0):
    """
    For a few violating Q, find the eigenvector of H(I)-H(Q) with most
    negative eigenvalue. Characterize it.
    """
    print("\n" + "=" * 70)
    print(f"VIOLATION CHARACTERIZATION: d={lat.d}")
    print("=" * 70)

    eigs_I_all = eigvalsh(H_I)[::-1]

    worst_overall = 0
    for trial in range(N_samples):
        Q = make_random_config(lat)
        H_Q = build_hessian(lat, Q, beta)
        diff = H_I - H_Q

        evals, evecs = np.linalg.eigh(diff)
        # evals sorted ascending, so evals[0] is most negative
        min_eval = evals[0]
        v_worst = evecs[:, 0]

        # Rayleigh quotient of v_worst in H(I) and H(Q)
        rq_I = v_worst @ H_I @ v_worst
        rq_Q = v_worst @ H_Q @ v_worst

        # Plaquette holonomies
        plaq_traces = []
        for (e1, e2, e3, e4) in lat.plaquettes:
            U = Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T
            plaq_traces.append(re_tr(U))

        avg_plaq = np.mean(plaq_traces)
        min_plaq = np.min(plaq_traces)

        if min_eval < worst_overall or trial < 3:
            worst_overall = min(worst_overall, min_eval)
            print(f"\n  Trial {trial}: min_eig(H(I)-H(Q)) = {min_eval:.6f}")
            print(f"    v_worst^T H(I) v = {rq_I:.6f}")
            print(f"    v_worst^T H(Q) v = {rq_Q:.6f}")
            print(f"    H(Q) exceeds H(I) in this direction by {rq_Q - rq_I:.6f}")
            print(f"    Avg plaquette trace: {avg_plaq:.4f} (min: {min_plaq:.4f})")

    print(f"\n  Worst min_eig overall: {worst_overall:.6f}")
    print(f"\n  Key insight: Even though lambda_max(H(Q)) < lambda_max(H(I)),")
    print(f"  some directions v have v^T H(Q) v > v^T H(I) v.")
    print(f"  Matrix domination requires ALL directions to satisfy the inequality.")


# ============================================================================
# Main
# ============================================================================

def main():
    beta = 1.0

    for d_val in [2, 3, 4]:
        print("\n\n" + "#" * 70)
        print(f"# DIMENSION d={d_val}")
        print("#" * 70)

        lat = Lattice(L=2, d=d_val)
        Q_I = make_identity_config(lat)
        H_I = build_hessian(lat, Q_I, beta)

        N_eig = 500 if d_val <= 3 else 200
        N_maj = 1000 if d_val <= 3 else 300

        eigenvalue_by_eigenvalue_test(lat, H_I, N_samples=N_eig, beta=beta)
        majorization_test_thorough(lat, H_I, N_samples=N_maj, beta=beta)
        characterize_violations(lat, H_I, N_samples=10, beta=beta)
        anti_instanton_test(lat, H_I, beta=beta)


if __name__ == "__main__":
    main()
