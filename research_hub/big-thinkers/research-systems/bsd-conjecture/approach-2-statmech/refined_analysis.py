#!/usr/bin/env sage -python
"""
Refined Statistical Mechanics Analysis of BSD — Phase 2
========================================================

With verified curve databases, deeper statistics, and focused tests.
"""

from sage.all import (
    EllipticCurve, primes, prime_range, RealField, ComplexField,
    log, exp, sqrt, pi, RR, CC, ZZ, QQ
)
import json
import os
import math
import sys

RF = RealField(200)
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# VERIFIED CURVE DATABASE
# ============================================================
VERIFIED_CURVES = {
    'rank0': [
        '11a1', '14a1', '15a1', '17a1', '19a1', '20a1', '21a1',
        '24a1', '26a1', '27a1', '30a1', '32a1', '33a1', '34a1', '35a1',
    ],
    'rank1': [
        '37a1', '43a1', '53a1', '57a1', '58a1', '61a1', '65a1',
        '77a1', '79a1', '82a1', '83a1', '88a1', '89a1', '91a1', '99a1',
    ],
    'rank2': [
        '389a1', '433a1', '563a1', '643a1', '655a1', '664a1',
        '707a1', '709a1', '794a1', '817a1',
    ],
    'rank3': [
        '5077a1',
    ],
}


def incremental_log_L(E, s, max_prime):
    """Compute log|L(E,s)| up to max_prime, returning value at each prime."""
    N = int(E.conductor())
    cumlog = 0.0
    trajectory = []

    for p in prime_range(2, max_prime + 1):
        ap = int(E.ap(p))
        is_bad = (N % p == 0)
        ps = float(p) ** (-s)

        if is_bad:
            denom = 1 - ap * ps
        else:
            denom = 1 - ap * ps + p * ps * ps

        if abs(denom) > 1e-50:
            cumlog += -math.log(abs(denom))

        trajectory.append((p, cumlog))

    return cumlog, trajectory


def compute_running_coupling(log_L, Lambda):
    """g(Lambda) = log|L|/log(Lambda) — the 'running coupling'."""
    if Lambda <= 1:
        return 0.0
    return log_L / math.log(Lambda)


# ============================================================
# TEST 1: Running Coupling as Rank Discriminator
# ============================================================
def test_running_coupling_discriminator():
    """
    CORE TEST: At fixed prime cutoff Lambda, does the running coupling
    g(Lambda) = log|L_Lambda(E,1)|/log(Lambda) cleanly separate ranks?
    """
    print("\n" + "=" * 70)
    print("TEST 1: Running Coupling as Rank Discriminator")
    print("=" * 70)

    cutoffs = [1000, 5000, 10000, 20000, 50000]
    all_results = {}

    for Lambda in cutoffs:
        print(f"\n  Lambda = {Lambda}")
        print(f"  {'Label':>10s} {'Rank':>5s} {'log|L|':>10s} {'g(Lambda)':>10s}")
        print(f"  {'-'*40}")

        rank_gs = {0: [], 1: [], 2: [], 3: []}

        for rank_label, curves in VERIFIED_CURVES.items():
            rank = int(rank_label[-1])
            for label in curves:
                E = EllipticCurve(label)
                logL, _ = incremental_log_L(E, 1.0, Lambda)
                g = compute_running_coupling(logL, Lambda)
                rank_gs[rank].append(g)
                if Lambda == 20000:  # Print detailed at one cutoff
                    print(f"  {label:>10s} {rank:>5d} {logL:>10.4f} {g:>10.6f}")

        all_results[Lambda] = rank_gs

        # Statistics
        print(f"\n  Summary at Lambda={Lambda}:")
        for rank in [0, 1, 2, 3]:
            if rank_gs[rank]:
                vals = rank_gs[rank]
                mean = sum(vals) / len(vals)
                if len(vals) > 1:
                    var = sum((v - mean)**2 for v in vals) / (len(vals) - 1)
                    std = var**0.5
                else:
                    std = 0
                print(f"    Rank {rank}: mean(g) = {mean:>9.6f} +/- {std:.6f}  (n={len(vals)})")

        # Separation tests
        for r1, r2 in [(0, 1), (0, 2), (1, 2)]:
            if rank_gs[r1] and rank_gs[r2]:
                m1 = sum(rank_gs[r1]) / len(rank_gs[r1])
                m2 = sum(rank_gs[r2]) / len(rank_gs[r2])
                s1 = (sum((v-m1)**2 for v in rank_gs[r1]) / max(len(rank_gs[r1])-1, 1))**0.5
                s2 = (sum((v-m2)**2 for v in rank_gs[r2]) / max(len(rank_gs[r2])-1, 1))**0.5
                pooled_std = ((s1**2 + s2**2) / 2)**0.5
                if pooled_std > 0:
                    sep = abs(m1 - m2) / pooled_std
                else:
                    sep = float('inf')
                print(f"    Rank {r1} vs {r2}: separation = {abs(m1-m2):.6f}, "
                      f"pooled_std = {pooled_std:.6f}, Cohen's d = {sep:.2f}")

    return all_results


# ============================================================
# TEST 2: RG Beta Function — Does It Have Universal Shape?
# ============================================================
def test_beta_function():
    """
    The RG beta function beta(g) = dg/d(log Lambda) describes
    how the coupling runs. If this is universal within a rank class,
    we have a genuine universality result.
    """
    print("\n" + "=" * 70)
    print("TEST 2: RG Beta Function Universality")
    print("=" * 70)

    max_prime = 30000
    # Build dense trajectory for each curve
    beta_data = {}

    for rank_label, curves in VERIFIED_CURVES.items():
        rank = int(rank_label[-1])
        beta_data[rank] = []

        for label in curves[:8]:  # Use up to 8 per rank
            E = EllipticCurve(label)
            _, traj = incremental_log_L(E, 1.0, max_prime)

            # Sample at exponentially spaced points
            sample_indices = []
            idx = 10
            while idx < len(traj):
                sample_indices.append(idx)
                idx = int(idx * 1.2) + 1

            gs = []
            log_lambdas = []
            for i in sample_indices:
                if i < len(traj):
                    p, logL = traj[i]
                    g = compute_running_coupling(logL, p)
                    gs.append(g)
                    log_lambdas.append(math.log(p))

            # Compute beta = dg/d(log Lambda)
            betas = []
            for i in range(1, len(gs)):
                dlL = log_lambdas[i] - log_lambdas[i-1]
                if dlL > 0:
                    betas.append((gs[i] - gs[i-1]) / dlL)

            beta_data[rank].append({
                'label': label,
                'gs': gs,
                'betas': betas,
                'log_lambdas': log_lambdas,
            })

            print(f"  {label} (rank {rank}): final g={gs[-1]:.6f}, "
                  f"mean beta={sum(betas)/len(betas) if betas else 0:.6f}")

    # Analyze: for each rank, compute mean beta function
    print("\n  Beta function statistics by rank:")
    for rank in [0, 1, 2]:
        if beta_data[rank]:
            # All curves: average final 5 beta values
            final_betas = []
            for curve in beta_data[rank]:
                if len(curve['betas']) >= 5:
                    final_betas.append(sum(curve['betas'][-5:]) / 5)

            if final_betas:
                mean_fb = sum(final_betas) / len(final_betas)
                if len(final_betas) > 1:
                    std_fb = (sum((v-mean_fb)**2 for v in final_betas) / (len(final_betas)-1))**0.5
                else:
                    std_fb = 0
                print(f"    Rank {rank}: mean(final beta) = {mean_fb:.6f} +/- {std_fb:.6f}")
                print(f"      Values: {[f'{v:.6f}' for v in final_betas]}")

    return beta_data


# ============================================================
# TEST 3: Free Energy Scaling with System Size (Conductor)
# ============================================================
def test_free_energy_scaling():
    """
    In stat mech, free energy scales with system size.
    Here 'system size' ~ log(N) (conductor).

    Does F(s=1) scale linearly with rank * something?
    """
    print("\n" + "=" * 70)
    print("TEST 3: Free Energy Scaling at s=1")
    print("=" * 70)

    prime_bound = 30000
    results = {0: [], 1: [], 2: [], 3: []}

    for rank_label, curves in VERIFIED_CURVES.items():
        rank = int(rank_label[-1])
        for label in curves:
            E = EllipticCurve(label)
            N = int(E.conductor())
            logL, _ = incremental_log_L(E, 1.0, prime_bound)
            F = -logL  # Free energy
            results[rank].append({
                'label': label,
                'N': N,
                'logN': math.log(N),
                'F': F,
                'logL': logL,
            })
            print(f"  {label}: rank={rank}, N={N}, logN={math.log(N):.3f}, "
                  f"logL={logL:.4f}, F={F:.4f}")

    # For each rank: fit F vs log(N)
    print("\n  Free energy scaling (F vs log(N)):")
    for rank in [0, 1, 2]:
        data = results[rank]
        if len(data) < 3:
            continue

        xs = [d['logN'] for d in data]
        ys = [d['F'] for d in data]

        n = len(xs)
        sx = sum(xs)
        sy = sum(ys)
        sxx = sum(x*x for x in xs)
        sxy = sum(x*y for x, y in zip(xs, ys))
        denom = n * sxx - sx * sx

        if abs(denom) > 1e-10:
            slope = (n * sxy - sx * sy) / denom
            intercept = (sy - slope * sx) / n
            # R^2
            y_mean = sy / n
            ss_res = sum((y - (slope * x + intercept))**2 for x, y in zip(xs, ys))
            ss_tot = sum((y - y_mean)**2 for y in ys)
            r_sq = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        else:
            slope, intercept, r_sq = 0, 0, 0

        print(f"    Rank {rank}: F ~ {slope:.3f} * log(N) + {intercept:.3f}  (R^2={r_sq:.4f})")

    # KEY: ratio of mean F values
    print("\n  Mean free energy by rank:")
    for rank in [0, 1, 2, 3]:
        data = results[rank]
        if data:
            mean_F = sum(d['F'] for d in data) / len(data)
            print(f"    Rank {rank}: mean(F) = {mean_F:.4f}")

    print("\n  Ratios:")
    for rank in [0, 1, 2, 3]:
        data = results[rank]
        if data and results[0]:
            mean_F = sum(d['F'] for d in data) / len(data)
            mean_F0 = sum(d['F'] for d in results[0]) / len(results[0])
            if mean_F0 != 0:
                print(f"    F(rank {rank}) / F(rank 0) = {mean_F / mean_F0:.4f}")

    return results


# ============================================================
# TEST 4: Phase Transition Order from Specific Heat Divergence
# ============================================================
def test_phase_transition_order():
    """
    At a phase transition, specific heat C = -d^2F/ds^2 diverges.
    The type of divergence encodes the order of the transition.

    For rank r: L(E,s) ~ (s-1)^r near s=1
    So log|L| ~ r*log|s-1| and F = -log|L| ~ -r*log|s-1|
    Then C = d^2F/ds^2 ~ r/(s-1)^2

    The AMPLITUDE of the specific heat peak should scale with rank.
    """
    print("\n" + "=" * 70)
    print("TEST 4: Specific Heat as Phase Transition Order Detector")
    print("=" * 70)

    prime_bound = 20000
    # Compute specific heat at several s values near 1
    s_values = [0.8, 0.85, 0.9, 0.95, 0.98, 0.99, 1.0, 1.01, 1.02, 1.05, 1.1, 1.15, 1.2]
    ds = 0.002

    results = {}
    for rank_label, curves in VERIFIED_CURVES.items():
        rank = int(rank_label[-1])
        # Use 3 representative curves per rank
        for label in curves[:3]:
            E = EllipticCurve(label)
            print(f"\n  {label} (rank {rank}):")

            profile = []
            for s in s_values:
                # Compute logL at s-ds, s, s+ds
                logL_minus, _ = incremental_log_L(E, s - ds, prime_bound)
                logL_center, _ = incremental_log_L(E, s, prime_bound)
                logL_plus, _ = incremental_log_L(E, s + ds, prime_bound)

                # Specific heat
                C = (logL_plus - 2*logL_center + logL_minus) / (ds * ds)
                # Susceptibility
                chi = (logL_plus - logL_minus) / (2 * ds)

                profile.append({
                    's': s,
                    'logL': logL_center,
                    'C': C,
                    'chi': chi,
                })

                if abs(s - 1.0) < 0.06:
                    print(f"    s={s:.2f}: logL={logL_center:.4f}, C={C:.2f}, chi={chi:.4f}")

            results[label] = {'rank': rank, 'profile': profile}

    # Compare specific heat at s=1 across ranks
    print("\n  Specific heat at s=1 by rank:")
    C_by_rank = {0: [], 1: [], 2: [], 3: []}
    chi_by_rank = {0: [], 1: [], 2: [], 3: []}

    for label, data in results.items():
        rank = data['rank']
        for p in data['profile']:
            if abs(p['s'] - 1.0) < 0.001:
                C_by_rank[rank].append(abs(p['C']))
                chi_by_rank[rank].append(abs(p['chi']))

    for rank in [0, 1, 2, 3]:
        if C_by_rank[rank]:
            mean_C = sum(C_by_rank[rank]) / len(C_by_rank[rank])
            mean_chi = sum(chi_by_rank[rank]) / len(chi_by_rank[rank])
            print(f"    Rank {rank}: mean|C| = {mean_C:.2f}, mean|chi| = {mean_chi:.4f}")

    return results


# ============================================================
# TEST 5: Anomalous Dimension — the Key Observable
# ============================================================
def test_anomalous_dimension():
    """
    In the RG framework, the anomalous dimension gamma governs how
    correlation functions scale.

    Here: gamma = -2 * d(log L) / d(log Lambda) at s=1

    This measures how fast the L-function converges as more primes
    are included. The key prediction:

      gamma ~ 0 for rank 0 (L(E,1) is nonzero, product converges)
      gamma ~ positive for rank >= 1 (product vanishes, each new prime
              contributes to the approach to zero)

    If gamma cleanly distinguishes ranks, we have a genuine RG-theoretic
    rank invariant.
    """
    print("\n" + "=" * 70)
    print("TEST 5: Anomalous Dimension as Rank Invariant")
    print("=" * 70)

    max_prime = 50000
    gamma_by_rank = {0: [], 1: [], 2: [], 3: []}

    for rank_label, curves in VERIFIED_CURVES.items():
        rank = int(rank_label[-1])
        for label in curves:
            E = EllipticCurve(label)
            _, traj = incremental_log_L(E, 1.0, max_prime)

            # Compute gamma at various scales using finite differences
            # Sample at half and full range
            n = len(traj)
            if n < 100:
                continue

            # Use last quarter vs last half to estimate local gamma
            i_half = n // 2
            i_quarter = 3 * n // 4

            p_half, logL_half = traj[i_half]
            p_quarter, logL_quarter = traj[i_quarter]
            p_full, logL_full = traj[-1]

            # gamma from half to full
            dlogL = logL_full - logL_half
            dlogP = math.log(p_full) - math.log(p_half)
            gamma_hf = -2 * dlogL / dlogP if dlogP > 0 else 0

            # gamma from quarter to full
            dlogL2 = logL_full - logL_quarter
            dlogP2 = math.log(p_full) - math.log(p_quarter)
            gamma_qf = -2 * dlogL2 / dlogP2 if dlogP2 > 0 else 0

            gamma_by_rank[rank].append({
                'label': label,
                'gamma_hf': gamma_hf,
                'gamma_qf': gamma_qf,
                'logL_final': logL_full,
            })

            print(f"  {label} (rank {rank}): gamma_hf={gamma_hf:.6f}, "
                  f"gamma_qf={gamma_qf:.6f}, logL={logL_full:.4f}")

    print("\n  Anomalous dimension statistics:")
    for rank in [0, 1, 2, 3]:
        data = gamma_by_rank[rank]
        if data:
            gammas = [d['gamma_hf'] for d in data]
            mean_g = sum(gammas) / len(gammas)
            if len(gammas) > 1:
                std_g = (sum((v - mean_g)**2 for v in gammas) / (len(gammas)-1))**0.5
            else:
                std_g = 0
            print(f"    Rank {rank}: mean(gamma) = {mean_g:.6f} +/- {std_g:.6f}  (n={len(gammas)})")

    # Separation tests
    print("\n  Separation tests (Cohen's d):")
    for r1, r2 in [(0, 1), (0, 2), (1, 2)]:
        d1 = [d['gamma_hf'] for d in gamma_by_rank[r1]]
        d2 = [d['gamma_hf'] for d in gamma_by_rank[r2]]
        if d1 and d2:
            m1, m2 = sum(d1)/len(d1), sum(d2)/len(d2)
            s1 = (sum((v-m1)**2 for v in d1) / max(len(d1)-1, 1))**0.5
            s2 = (sum((v-m2)**2 for v in d2) / max(len(d2)-1, 1))**0.5
            pooled = ((s1**2 + s2**2) / 2)**0.5
            d = abs(m1 - m2) / pooled if pooled > 0 else float('inf')
            print(f"    Rank {r1} vs {r2}: |delta_mean| = {abs(m1-m2):.6f}, "
                  f"pooled_std = {pooled:.6f}, Cohen's d = {d:.2f}")

    return gamma_by_rank


# ============================================================
# TEST 6: Convergence Rate at Off-Critical Temperatures
# ============================================================
def test_off_critical_convergence():
    """
    Away from s=1, the partial L-product should converge to a finite
    value regardless of rank. The RATE of convergence, however,
    should differ by rank.

    At s=2 (well above critical temp): all curves converge fast.
    At s=1.1 (just above critical): rank-0 converges, rank >= 1 converges to nonzero.
    At s=0.9 (just below critical): convergence rate differs.
    """
    print("\n" + "=" * 70)
    print("TEST 6: Convergence Rates at Different Temperatures")
    print("=" * 70)

    s_values = [0.9, 0.95, 1.0, 1.05, 1.1, 1.5, 2.0]
    max_prime = 20000

    for rank_label, curves in VERIFIED_CURVES.items():
        rank = int(rank_label[-1])
        label = curves[0]  # Just use first curve per rank
        E = EllipticCurve(label)

        print(f"\n  {label} (rank {rank}):")
        for s in s_values:
            logL, traj = incremental_log_L(E, s, max_prime)

            # Measure convergence: compare last quarter to second-to-last quarter
            n = len(traj)
            q3 = 3 * n // 4
            q2 = n // 2

            _, logL_q2 = traj[q2]
            _, logL_q3 = traj[q3]
            _, logL_full = traj[-1]

            delta_recent = logL_full - logL_q3
            delta_older = logL_q3 - logL_q2

            # Convergence rate: how much does adding more primes change things?
            print(f"    s={s:.2f}: logL={logL_full:.4f}, "
                  f"delta_recent={delta_recent:.6f}, delta_older={delta_older:.6f}")

    return


# ============================================================
# TEST 7: "Magnetic Order Parameter" — Running Average of a_p
# ============================================================
def test_order_parameter():
    """
    In stat mech, the order parameter M distinguishes phases.

    Analogy: M(Lambda) = (1/pi(Lambda)) * sum_{p<=Lambda} a_p / (2*sqrt(p))

    By Sato-Tate, this should converge to 0. But the RATE of convergence
    and the FLUCTUATIONS might differ by rank.

    For rank 0: L(E,1) != 0, so the Euler product converges, and the
                sum of log(euler factors) converges, meaning a_p values
                on average "cooperate" to produce a finite product.
    For rank >= 1: The Euler product vanishes, so there must be
                   systematic cancellation. The a_p values on average
                   must "conspire" to make the product small.
    """
    print("\n" + "=" * 70)
    print("TEST 7: Order Parameter (Running a_p Average)")
    print("=" * 70)

    max_prime = 50000

    for rank_label, curves in VERIFIED_CURVES.items():
        rank = int(rank_label[-1])
        print(f"\n  Rank {rank}:")

        for label in curves[:5]:
            E = EllipticCurve(label)
            N = int(E.conductor())

            cumsum = 0.0
            count = 0
            log_cumsum = 0.0  # Weighted: sum a_p / p (a kind of Dirichlet series)

            for p in prime_range(2, max_prime + 1):
                ap = int(E.ap(p))
                is_bad = (N % p == 0)
                if not is_bad:
                    norm = ap / (2 * math.sqrt(p))
                    cumsum += norm
                    count += 1
                    log_cumsum += ap / float(p)

            mean_ap = cumsum / count if count > 0 else 0
            mean_weighted = log_cumsum

            print(f"    {label}: mean(a_p/2sqrt(p)) = {mean_ap:.6f}, "
                  f"sum(a_p/p) = {mean_weighted:.4f}")


# ============================================================
# TEST 8: Partition Function Zeros (Lee-Yang Zeros Analog)
# ============================================================
def test_partition_zeros():
    """
    In stat mech, Lee-Yang zeros of the partition function in the complex
    temperature plane approach the real axis at the phase transition.

    For L-functions, the zeros of L(E,s) in the critical strip are
    exactly this. By GRH, they lie on Re(s)=1. The DENSITY of zeros
    near s=1 should be related to rank.

    We can't compute true zeros easily, but we CAN look at how
    |L(E, 1+it)| varies with t. The number of near-zeros for small t
    is related to the rank.
    """
    print("\n" + "=" * 70)
    print("TEST 8: Partition Function Near-Zeros (Lee-Yang Analog)")
    print("=" * 70)

    prime_bound = 10000
    t_values = [i * 0.5 for i in range(21)]  # t from 0 to 10

    for label, rank in [('11a1', 0), ('37a1', 1), ('389a1', 2), ('5077a1', 3)]:
        E = EllipticCurve(label)
        N = int(E.conductor())

        print(f"\n  {label} (rank {rank}): |L(E, 1+it)| along critical line")

        for t in t_values:
            s = complex(1.0, t)
            # Compute partial L at complex s
            cumlog_re = 0.0
            cumlog_im = 0.0

            for p in prime_range(2, prime_bound + 1):
                ap = int(E.ap(p))
                is_bad = (N % p == 0)

                # p^{-s} = p^{-1} * exp(-i*t*log(p))
                p_neg_s = p**(-1.0) * complex(math.cos(-t * math.log(p)),
                                               math.sin(-t * math.log(p)))

                if is_bad:
                    denom = 1 - ap * p_neg_s
                else:
                    denom = 1 - ap * p_neg_s + p * p_neg_s**2

                if abs(denom) > 1e-50:
                    cumlog_re += -math.log(abs(denom))

            print(f"    t={t:>5.1f}: log|L| = {cumlog_re:>10.4f}, "
                  f"|L| ~ {math.exp(cumlog_re) if abs(cumlog_re) < 500 else 0:.6g}")


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 70)
    print("REFINED STATISTICAL MECHANICS ANALYSIS OF BSD")
    print("=" * 70)
    print(f"Using verified curve database:")
    for rank_label, curves in VERIFIED_CURVES.items():
        print(f"  {rank_label}: {len(curves)} curves")

    # Run all tests
    results = {}

    results['running_coupling'] = test_running_coupling_discriminator()
    results['beta_function'] = test_beta_function()
    results['free_energy_scaling'] = test_free_energy_scaling()
    results['anomalous_dimension'] = test_anomalous_dimension()
    test_off_critical_convergence()
    test_order_parameter()
    results['phase_transition'] = test_phase_transition_order()
    test_partition_zeros()

    print("\n" + "=" * 70)
    print("ALL TESTS COMPLETE")
    print("=" * 70)

    return results


if __name__ == '__main__':
    main()
