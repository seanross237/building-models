#!/usr/bin/env sage -python
"""
Statistical Mechanics Framework for BSD Conjecture
===================================================

Models elliptic curve L-functions as partition functions and applies
renormalization group (RG) flow analysis to connect local prime data
to global rank.

Key mappings:
  - Prime p  <-->  lattice site / energy level
  - a_p      <-->  local interaction / coupling
  - s        <-->  inverse temperature beta
  - L(E,s)   <-->  partition function Z(beta)
  - rank     <-->  order of phase transition at critical temp beta_c (s=1)
  - -log|L|  <-->  free energy F(beta)

Author: BSD StatMech Agent
Date: 2026-04-04
"""

from sage.all import (
    EllipticCurve, primes, prime_range, RealField, ComplexField,
    log, exp, sqrt, pi, floor, ceil, RR, CC, ZZ, QQ, cached_function
)
import json
import os
import sys
import time
from collections import defaultdict

# High precision
RF = RealField(200)
CF = ComplexField(200)


# ============================================================
# SECTION 1: Elliptic Curve Data Acquisition
# ============================================================

# Curated test set: curves of known rank with varied conductors
CURVE_DATABASE = {
    # Rank 0 curves
    'rank0': [
        ('11a1', 0),
        ('14a1', 0),
        ('15a1', 0),
        ('17a1', 0),
        ('19a1', 0),
        ('20a1', 0),
        ('21a1', 0),
        ('24a1', 0),
        ('26a1', 0),
        ('27a1', 0),
        ('32a1', 0),
        ('36a1', 0),
        ('44a1', 0),
        ('48a1', 0),
        ('54a1', 0),
        ('56a1', 0),
        ('64a1', 0),
        ('72a1', 0),
        ('80a1', 0),
        ('96a1', 0),
    ],
    # Rank 1 curves
    'rank1': [
        ('37a1', 1),
        ('43a1', 1),
        ('53a1', 1),
        ('57a1', 1),
        ('58a1', 1),
        ('61a1', 1),
        ('65a1', 1),
        ('67a1', 1),
        ('73a1', 1),
        ('77a1', 1),
        ('79a1', 1),
        ('82a1', 1),
        ('83a1', 1),
        ('88a1', 1),
        ('89a1', 1),
        ('91a1', 1),
        ('92a1', 1),
        ('99a1', 1),
        ('101a1', 1),
        ('102a1', 1),
    ],
    # Rank 2 curves
    'rank2': [
        ('389a1', 2),
        ('433a1', 2),
        ('446a1', 2),
        ('563a1', 2),
        ('571a1', 2),
        ('643a1', 2),
        ('655a1', 2),
        ('664a1', 2),
        ('681a1', 2),
        ('707a1', 2),
        ('709a1', 2),
        ('718a1', 2),
        ('794a1', 2),
        ('817a1', 2),
        ('916a1', 2),
        ('997a1', 2),
    ],
    # Rank 3 curves (rare, higher conductor)
    'rank3': [
        ('5077a1', 3),
    ],
}


def load_curve(label):
    """Load an elliptic curve by Cremona label."""
    E = EllipticCurve(label)
    return E


def get_ap_data(E, prime_bound):
    """Get a_p values for all primes up to prime_bound.

    Returns list of (p, a_p) pairs. Handles bad primes correctly.
    """
    N = int(E.conductor())
    data = []
    for p in prime_range(2, prime_bound + 1):
        ap = int(E.ap(p))
        is_bad = (N % p == 0)
        data.append((p, ap, is_bad))
    return data


# ============================================================
# SECTION 2: Partition Function / L-function Computation
# ============================================================

def euler_factor(p, ap, s, is_bad=False):
    """Compute the local Euler factor at prime p.

    Good prime: (1 - a_p * p^{-s} + p^{1-2s})^{-1}
    Bad prime:  (1 - a_p * p^{-s})^{-1}

    In stat mech language: local partition function at site p.
    """
    ps = RF(p) ** (-RF(s))
    if is_bad:
        denom = 1 - RF(ap) * ps
    else:
        denom = 1 - RF(ap) * ps + RF(p) * ps * ps
    if abs(denom) < 1e-50:
        return RF('inf')
    return 1 / denom


def partial_L(E, s, prime_bound, return_factors=False):
    """Compute partial Euler product L(E,s) up to prime_bound.

    This is the partition function Z(beta) with cutoff Lambda = prime_bound.
    """
    N = int(E.conductor())
    product = RF(1)
    factors = []

    for p in prime_range(2, prime_bound + 1):
        ap = int(E.ap(p))
        is_bad = (N % p == 0)
        f = euler_factor(p, ap, s, is_bad)
        product *= f
        if return_factors:
            factors.append((p, ap, is_bad, float(f), float(product)))

    if return_factors:
        return float(product), factors
    return float(product)


def log_partial_L(E, s, prime_bound):
    """Compute log of partial L-function (= -free energy in stat mech).

    log L(E,s) = -F(beta) where F is free energy.
    We sum log of individual Euler factors for numerical stability.
    """
    N = int(E.conductor())
    total = RF(0)

    for p in prime_range(2, prime_bound + 1):
        ap = int(E.ap(p))
        is_bad = (N % p == 0)
        ps = RF(p) ** (-RF(s))

        if is_bad:
            denom = 1 - RF(ap) * ps
        else:
            denom = 1 - RF(ap) * ps + RF(p) * ps * ps

        if abs(denom) > 1e-50:
            total += log(abs(denom))  # Note: this is -log(factor), so total = -log(product)

    return -float(total)  # Return log|L| = -sum(log|denom|)


# ============================================================
# SECTION 3: Thermodynamic Quantities
# ============================================================

def free_energy(E, s, prime_bound):
    """Free energy F(beta) = -log|Z(beta)| = -log|L(E,s)|.

    At the critical point s=1:
    - Rank 0: F(1) = -log|L(E,1)| is finite and negative (L(E,1) > 0)
    - Rank 1: F(1) -> +infinity (L(E,1) = 0, first order zero)
    - Rank 2: F(1) -> +infinity faster (second order zero)
    """
    return -log_partial_L(E, s, prime_bound)


def specific_heat(E, s, prime_bound, ds=0.001):
    """Specific heat C(beta) = -beta^2 * d^2F/dbeta^2 = d^2(log|L|)/ds^2.

    Computed via finite differences at inverse temperature s.
    """
    f_plus = log_partial_L(E, s + ds, prime_bound)
    f_center = log_partial_L(E, s, prime_bound)
    f_minus = log_partial_L(E, s - ds, prime_bound)

    d2f = (f_plus - 2 * f_center + f_minus) / (ds * ds)
    return d2f


def susceptibility(E, s, prime_bound, ds=0.001):
    """Magnetic susceptibility analog: d(log|L|)/ds.

    This is the first derivative of the free energy.
    Near a zero of L(E,s), this diverges.
    """
    f_plus = log_partial_L(E, s + ds, prime_bound)
    f_minus = log_partial_L(E, s - ds, prime_bound)

    return (f_plus - f_minus) / (2 * ds)


def compute_thermodynamics(E, s_values, prime_bound):
    """Compute full thermodynamic profile: F, C, chi as functions of s."""
    results = []
    for s in s_values:
        logL = log_partial_L(E, s, prime_bound)
        F = -logL
        C = specific_heat(E, s, prime_bound)
        chi = susceptibility(E, s, prime_bound)
        results.append({
            's': s,
            'logL': logL,
            'free_energy': F,
            'specific_heat': C,
            'susceptibility': chi,
        })
    return results


# ============================================================
# SECTION 4: Renormalization Group Flow
# ============================================================

def rg_flow_trajectory(E, s, cutoff_schedule=None, num_steps=20):
    """Compute the RG flow trajectory for curve E at temperature s.

    The RG flow is: as we increase the prime cutoff Lambda from small to large,
    how does the "running coupling" (partial L-value) evolve?

    In RG language:
    - Lambda (UV cutoff) = prime_bound
    - Running coupling g(Lambda) = log|L_Lambda(E,s)| / log(Lambda)
    - Fixed point = limiting behavior as Lambda -> infinity

    For rank 0: g(Lambda) -> finite constant (L(E,1) != 0)
    For rank r: g(Lambda) ~ r * log(log(Lambda)) / log(Lambda) -> 0 (but slowly)

    Returns list of (Lambda, log_L, running_coupling, raw_L) tuples.
    """
    if cutoff_schedule is None:
        # Exponentially spaced cutoffs: 10, 20, 40, ..., ~10*2^19
        cutoff_schedule = [int(10 * 2**(i * 0.8)) for i in range(num_steps)]
        cutoff_schedule = sorted(set(cutoff_schedule))

    trajectory = []
    N = int(E.conductor())

    # Accumulate incrementally for efficiency
    cumulative_log = 0.0
    prime_idx = 0
    all_primes = list(prime_range(2, max(cutoff_schedule) + 1))

    for Lambda in cutoff_schedule:
        while prime_idx < len(all_primes) and all_primes[prime_idx] <= Lambda:
            p = all_primes[prime_idx]
            ap = int(E.ap(p))
            is_bad = (N % p == 0)

            ps = float(p) ** (-s)
            if is_bad:
                denom = 1 - ap * ps
            else:
                denom = 1 - ap * ps + p * ps * ps

            if abs(denom) > 1e-50:
                cumulative_log += -log(float(abs(denom)))

            prime_idx += 1

        logL = cumulative_log
        logLambda = log(float(Lambda))
        running_coupling = logL / logLambda if logLambda > 0 else 0
        raw_L = float(exp(RF(logL))) if abs(logL) < 500 else float('inf')

        trajectory.append({
            'Lambda': Lambda,
            'log_L': logL,
            'running_coupling': running_coupling,
            'num_primes': prime_idx,
            'raw_L': raw_L,
        })

    return trajectory


def rg_flow_multi_scale(E, s_values, max_prime=10000):
    """Compute RG flow at multiple temperatures simultaneously.

    This reveals how the flow topology changes as we cross the critical
    temperature s=1.
    """
    N = int(E.conductor())
    all_p = list(prime_range(2, max_prime + 1))

    # Cutoff schedule
    cutoffs = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, max_prime]
    cutoffs = [c for c in cutoffs if c <= max_prime]

    results = {s: [] for s in s_values}

    for s in s_values:
        cumlog = 0.0
        pidx = 0
        for Lambda in cutoffs:
            while pidx < len(all_p) and all_p[pidx] <= Lambda:
                p = all_p[pidx]
                ap = int(E.ap(p))
                is_bad = (N % p == 0)
                ps = float(p) ** (-s)
                if is_bad:
                    denom = 1 - ap * ps
                else:
                    denom = 1 - ap * ps + p * ps * ps
                if abs(denom) > 1e-50:
                    cumlog += -log(float(abs(denom)))
                pidx += 1

            results[s].append({
                'Lambda': Lambda,
                'log_L': cumlog,
                'running_coupling': cumlog / log(float(Lambda)),
            })

    return results


# ============================================================
# SECTION 5: Universality Class Detection
# ============================================================

def compute_rg_signature(E, max_prime=50000):
    """Compute a compact 'RG signature' for a curve.

    This signature captures how the curve flows under coarse-graining.
    Hypothesis: curves of the same rank have similar signatures
    (= same universality class).

    Signature components:
    1. Running coupling at s=1 for several cutoffs
    2. Derivative of running coupling (beta function)
    3. Curvature of running coupling
    """
    s = 1.0

    # Dense cutoff schedule
    cutoffs = []
    x = 10
    while x <= max_prime:
        cutoffs.append(int(x))
        x *= 1.3
    cutoffs = sorted(set(cutoffs))

    traj = rg_flow_trajectory(E, s, cutoff_schedule=cutoffs)

    # Extract running couplings
    lambdas = [t['Lambda'] for t in traj]
    gs = [t['running_coupling'] for t in traj]
    log_lambdas = [log(float(l)) for l in lambdas]

    # Beta function: dg/d(log Lambda)
    betas = []
    for i in range(1, len(gs)):
        dlL = log_lambdas[i] - log_lambdas[i-1]
        if dlL > 0:
            betas.append((gs[i] - gs[i-1]) / dlL)
        else:
            betas.append(0)

    # Signature
    sig = {
        'final_running_coupling': gs[-1] if gs else 0,
        'mean_running_coupling': sum(gs) / len(gs) if gs else 0,
        'mean_beta_function': sum(betas) / len(betas) if betas else 0,
        'final_beta_function': betas[-1] if betas else 0,
        'running_couplings': gs,
        'beta_functions': betas,
        'cutoffs': cutoffs,
    }

    return sig


def universality_test(curves_by_rank, max_prime=50000):
    """Test whether curves of the same rank have similar RG signatures.

    Returns statistics on within-class and between-class signature distances.
    """
    signatures = {}

    for rank_label, curve_list in curves_by_rank.items():
        signatures[rank_label] = []
        for label, expected_rank in curve_list:
            try:
                E = load_curve(label)
                sig = compute_rg_signature(E, max_prime=max_prime)
                sig['label'] = label
                sig['rank'] = expected_rank
                signatures[rank_label].append(sig)
                print(f"  {label}: g_final={sig['final_running_coupling']:.6f}, "
                      f"beta_final={sig['final_beta_function']:.6f}")
            except Exception as e:
                print(f"  {label}: ERROR - {e}")

    # Compute within-class variance of final running coupling
    stats = {}
    for rank_label, sigs in signatures.items():
        if len(sigs) < 2:
            continue
        vals = [s['final_running_coupling'] for s in sigs]
        mean = sum(vals) / len(vals)
        var = sum((v - mean)**2 for v in vals) / len(vals)
        stats[rank_label] = {
            'mean_g': mean,
            'var_g': var,
            'std_g': var**0.5,
            'n': len(vals),
            'values': vals,
        }

    return signatures, stats


# ============================================================
# SECTION 6: Critical Exponent Extraction
# ============================================================

def critical_exponents(E, prime_bound=50000, s_center=1.0, ds_range=0.5, num_points=50):
    """Extract critical exponents near s=1.

    Near a phase transition, thermodynamic quantities scale as power laws:
    - Free energy: F ~ |s-1|^{2-alpha}
    - Susceptibility: chi ~ |s-1|^{-gamma}
    - Specific heat: C ~ |s-1|^{-alpha}

    For rank r curve: L(E,s) ~ (s-1)^r * c_r + ...
    So log|L(E,s)| ~ r * log|s-1| + const
    And F = -log|L| ~ -r * log|s-1|

    This means alpha = 2 - r (or rather, the singularity type encodes rank).
    """
    s_values = [s_center + ds_range * (2*i/(num_points-1) - 1)
                for i in range(num_points)]
    # Remove s=1 exactly to avoid log singularity
    s_values = [s for s in s_values if abs(s - 1.0) > 0.001]

    results = []
    for s in sorted(s_values):
        logL = log_partial_L(E, s, prime_bound)
        F = -logL
        results.append({
            's': s,
            'delta_s': s - 1.0,
            'log_delta_s': log(abs(s - 1.0)) if abs(s - 1.0) > 1e-10 else None,
            'log_L': logL,
            'free_energy': F,
        })

    # Fit: log|F| vs log|s-1| to extract exponent
    # For s > 1 side
    xs, ys = [], []
    for r in results:
        if r['log_delta_s'] is not None and r['delta_s'] > 0.01:
            xs.append(r['log_delta_s'])
            ys.append(log(abs(r['free_energy'])) if abs(r['free_energy']) > 1e-50 else 0)

    # Simple linear regression
    if len(xs) >= 3:
        n = len(xs)
        sx = sum(xs)
        sy = sum(ys)
        sxx = sum(x*x for x in xs)
        sxy = sum(x*y for x, y in zip(xs, ys))

        denom = n * sxx - sx * sx
        if abs(denom) > 1e-10:
            slope = (n * sxy - sx * sy) / denom
            intercept = (sy - slope * sx) / n
        else:
            slope, intercept = 0, 0
    else:
        slope, intercept = 0, 0

    return {
        'exponent': slope,
        'intercept': intercept,
        'data': results,
    }


# ============================================================
# SECTION 7: Conductor Scaling Analysis
# ============================================================

def conductor_scaling(curves_by_rank, s=1.0, prime_factor=10):
    """How do thermodynamic quantities scale with conductor N?

    For each rank class, compute F, C, chi at s values near 1,
    with prime_bound = prime_factor * N.

    In stat mech: how does the free energy scale with system size?
    - For rank 0: F should approach a constant
    - For rank >= 1: F should grow (diverge) in a way that depends on rank
    """
    results = {}

    for rank_label, curve_list in curves_by_rank.items():
        results[rank_label] = []
        for label, expected_rank in curve_list:
            try:
                E = load_curve(label)
                N = int(E.conductor())
                pb = min(prime_factor * N, 100000)
                pb = max(pb, 1000)

                logL = log_partial_L(E, s, pb)
                F = -logL
                C = specific_heat(E, s, pb)
                chi = susceptibility(E, s, pb)

                results[rank_label].append({
                    'label': label,
                    'rank': expected_rank,
                    'conductor': N,
                    'prime_bound': pb,
                    'log_L_at_1': logL,
                    'free_energy': F,
                    'specific_heat': C,
                    'susceptibility': chi,
                })
                print(f"  {label}: N={N}, F={F:.4f}, C={C:.4f}, chi={chi:.4f}")
            except Exception as e:
                print(f"  {label}: ERROR - {e}")

    return results


# ============================================================
# SECTION 8: "Local Energy" Analysis
# ============================================================

def local_energy_spectrum(E, prime_bound=1000):
    """Analyze the distribution of local energies (a_p values).

    The Sato-Tate distribution tells us a_p / (2*sqrt(p)) is distributed
    as semicircle for non-CM curves. But HOW the fluctuations around
    Sato-Tate correlate with rank is the interesting question.

    Returns binned histogram of normalized a_p and running statistics.
    """
    N = int(E.conductor())
    normalized = []
    raw = []

    for p in prime_range(2, prime_bound + 1):
        ap = int(E.ap(p))
        is_bad = (N % p == 0)
        if not is_bad:
            norm_ap = ap / (2 * float(p)**0.5)
            normalized.append(norm_ap)
            raw.append((p, ap, norm_ap))

    if not normalized:
        return {'error': 'no good primes'}

    mean = sum(normalized) / len(normalized)
    var = sum((x - mean)**2 for x in normalized) / len(normalized)

    # Running mean of normalized a_p (detects drift)
    running_mean = []
    cumsum = 0
    for i, x in enumerate(normalized):
        cumsum += x
        running_mean.append(cumsum / (i + 1))

    return {
        'mean': mean,
        'variance': var,
        'std': var**0.5,
        'count': len(normalized),
        'running_mean': running_mean,
        'raw': raw,
    }


# ============================================================
# MAIN EXECUTION
# ============================================================

def run_full_analysis():
    """Run the complete statistical mechanics analysis of BSD."""

    output_dir = os.path.dirname(os.path.abspath(__file__))

    print("=" * 70)
    print("STATISTICAL MECHANICS ANALYSIS OF BSD CONJECTURE")
    print("=" * 70)
    print()

    # ---- Phase 1: RG Flow Trajectories ----
    print("PHASE 1: RG Flow Trajectories at s=1 (critical temperature)")
    print("-" * 60)

    test_curves = [
        ('11a1', 0), ('14a1', 0), ('15a1', 0), ('17a1', 0), ('19a1', 0),
        ('37a1', 1), ('43a1', 1), ('53a1', 1), ('57a1', 1), ('58a1', 1),
        ('389a1', 2), ('433a1', 2), ('446a1', 2), ('563a1', 2), ('571a1', 2),
        ('5077a1', 3),
    ]

    rg_data = {}
    for label, rank in test_curves:
        print(f"\n  Computing RG flow for {label} (rank {rank})...")
        E = load_curve(label)
        traj = rg_flow_trajectory(E, s=1.0, num_steps=25)
        rg_data[label] = {
            'rank': rank,
            'conductor': int(E.conductor()),
            'trajectory': traj,
        }
        # Print key points
        for t in traj[::5]:
            print(f"    Lambda={t['Lambda']:>8d}  log(L)={t['log_L']:>10.4f}  "
                  f"g={t['running_coupling']:>8.4f}  L={t['raw_L']:.6g}")

    # Save RG data
    rg_save = {}
    for label, data in rg_data.items():
        rg_save[label] = {
            'rank': data['rank'],
            'conductor': data['conductor'],
            'trajectory': data['trajectory'],
        }
    with open(os.path.join(output_dir, 'rg_flow_data.json'), 'w') as f:
        json.dump(rg_save, f, indent=2, default=str)
    print("\n  -> Saved rg_flow_data.json")

    # ---- Phase 2: Thermodynamic Profiles ----
    print("\n\nPHASE 2: Thermodynamic Profiles Near s=1")
    print("-" * 60)

    s_values = [0.5 + 0.05*i for i in range(21)]  # s from 0.5 to 1.5
    thermo_data = {}

    for label, rank in [('11a1', 0), ('37a1', 1), ('389a1', 2), ('5077a1', 3)]:
        print(f"\n  Computing thermodynamics for {label} (rank {rank})...")
        E = load_curve(label)
        pb = 10000
        thermo = compute_thermodynamics(E, s_values, pb)
        thermo_data[label] = {
            'rank': rank,
            'conductor': int(E.conductor()),
            'prime_bound': pb,
            'data': thermo,
        }
        # Print near s=1
        for t in thermo:
            if abs(t['s'] - 1.0) < 0.16:
                print(f"    s={t['s']:.2f}  logL={t['logL']:>10.4f}  "
                      f"F={t['free_energy']:>10.4f}  C={t['specific_heat']:>10.4f}  "
                      f"chi={t['susceptibility']:>10.4f}")

    with open(os.path.join(output_dir, 'thermo_data.json'), 'w') as f:
        json.dump(thermo_data, f, indent=2, default=str)
    print("\n  -> Saved thermo_data.json")

    # ---- Phase 3: Universality Test ----
    print("\n\nPHASE 3: Universality Class Test")
    print("-" * 60)

    test_set = {
        'rank0': CURVE_DATABASE['rank0'][:8],
        'rank1': CURVE_DATABASE['rank1'][:8],
        'rank2': CURVE_DATABASE['rank2'][:8],
    }

    print("\n  Computing RG signatures (max_prime=20000)...")
    sigs, stats = universality_test(test_set, max_prime=20000)

    print("\n  Universality statistics:")
    for rank_label, s in stats.items():
        print(f"    {rank_label}: mean(g) = {s['mean_g']:.6f} +/- {s['std_g']:.6f}  "
              f"(n={s['n']})")

    # Between-class separation
    if 'rank0' in stats and 'rank1' in stats:
        sep01 = abs(stats['rank0']['mean_g'] - stats['rank1']['mean_g'])
        noise01 = (stats['rank0']['std_g'] + stats['rank1']['std_g']) / 2
        print(f"\n    Rank 0 vs 1 separation: {sep01:.6f} (noise: {noise01:.6f}, "
              f"SNR: {sep01/noise01 if noise01 > 0 else float('inf'):.2f})")
    if 'rank0' in stats and 'rank2' in stats:
        sep02 = abs(stats['rank0']['mean_g'] - stats['rank2']['mean_g'])
        noise02 = (stats['rank0']['std_g'] + stats['rank2']['std_g']) / 2
        print(f"    Rank 0 vs 2 separation: {sep02:.6f} (noise: {noise02:.6f}, "
              f"SNR: {sep02/noise02 if noise02 > 0 else float('inf'):.2f})")
    if 'rank1' in stats and 'rank2' in stats:
        sep12 = abs(stats['rank1']['mean_g'] - stats['rank2']['mean_g'])
        noise12 = (stats['rank1']['std_g'] + stats['rank2']['std_g']) / 2
        print(f"    Rank 1 vs 2 separation: {sep12:.6f} (noise: {noise12:.6f}, "
              f"SNR: {sep12/noise12 if noise12 > 0 else float('inf'):.2f})")

    with open(os.path.join(output_dir, 'universality_data.json'), 'w') as f:
        json.dump({
            'stats': stats,
            'signatures': {
                rank_label: [
                    {k: v for k, v in s.items() if k != 'running_couplings' and k != 'beta_functions' and k != 'cutoffs'}
                    for s in sig_list
                ]
                for rank_label, sig_list in sigs.items()
            }
        }, f, indent=2, default=str)
    print("\n  -> Saved universality_data.json")

    # ---- Phase 4: Critical Exponents ----
    print("\n\nPHASE 4: Critical Exponent Extraction")
    print("-" * 60)

    crit_data = {}
    for label, rank in [('11a1', 0), ('37a1', 1), ('389a1', 2), ('5077a1', 3)]:
        print(f"\n  Extracting critical exponents for {label} (rank {rank})...")
        E = load_curve(label)
        result = critical_exponents(E, prime_bound=20000)
        crit_data[label] = {
            'rank': rank,
            'exponent': result['exponent'],
            'intercept': result['intercept'],
        }
        print(f"    Fitted exponent (slope of log|F| vs log|s-1|): {result['exponent']:.4f}")
        print(f"    Expected for rank {rank}: ~1.0 (log singularity for rank>=1)")

    with open(os.path.join(output_dir, 'critical_exponents.json'), 'w') as f:
        json.dump(crit_data, f, indent=2, default=str)
    print("\n  -> Saved critical_exponents.json")

    # ---- Phase 5: Conductor Scaling ----
    print("\n\nPHASE 5: Conductor Scaling Analysis")
    print("-" * 60)

    scaling_set = {
        'rank0': CURVE_DATABASE['rank0'][:10],
        'rank1': CURVE_DATABASE['rank1'][:10],
        'rank2': CURVE_DATABASE['rank2'][:8],
    }

    scaling_results = conductor_scaling(scaling_set, s=1.0, prime_factor=5)

    with open(os.path.join(output_dir, 'conductor_scaling.json'), 'w') as f:
        json.dump(scaling_results, f, indent=2, default=str)
    print("\n  -> Saved conductor_scaling.json")

    # ---- Phase 6: Multi-temperature RG Flow ----
    print("\n\nPHASE 6: Multi-Temperature RG Flow")
    print("-" * 60)

    s_scan = [0.8, 0.9, 0.95, 1.0, 1.05, 1.1, 1.2]
    multi_temp = {}

    for label, rank in [('11a1', 0), ('37a1', 1), ('389a1', 2)]:
        print(f"\n  {label} (rank {rank}):")
        E = load_curve(label)
        result = rg_flow_multi_scale(E, s_scan, max_prime=10000)
        multi_temp[label] = {'rank': rank, 'data': {str(s): v for s, v in result.items()}}
        for s in s_scan:
            final = result[s][-1]
            print(f"    s={s:.2f}: final log(L)={final['log_L']:.4f}, "
                  f"g={final['running_coupling']:.4f}")

    with open(os.path.join(output_dir, 'multi_temp_rg.json'), 'w') as f:
        json.dump(multi_temp, f, indent=2, default=str)
    print("\n  -> Saved multi_temp_rg.json")

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)

    return rg_data, thermo_data, sigs, stats, crit_data, scaling_results, multi_temp


if __name__ == '__main__':
    run_full_analysis()
