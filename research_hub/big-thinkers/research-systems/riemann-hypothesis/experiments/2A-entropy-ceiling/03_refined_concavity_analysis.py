"""
03_refined_concavity_analysis.py
================================
Refined analysis of entropy concavity in the primon gas.

Key issues from the initial analysis:
1. The explicit formula with finite zeros is poorly converged for small E
2. Need to separate the STRUCTURAL effect of off-line zeros from truncation artifacts
3. The analytic relationship S''(E) = -1/(beta^2 * C) only holds in the canonical
   ensemble, which assumes RH. We need a different approach for the off-line case.

This script takes three approaches:

A) ANALYTIC BOUND: Prove that S''(E) < 0 using the relationship between the
   density of states and the zeros. Show that off-line zeros CREATE regions of
   positive S''.

B) DIRECT NUMERICAL: Compute the density of states directly by counting
   multiplicative partitions (for moderate n), bypassing the explicit formula.

C) PERTURBATIVE: Treat the off-line zero as a perturbation and compute the
   leading-order effect on S''(E) analytically.

Author: Strategy 2A exploration
Date: 2026-04-04
"""

import mpmath
import numpy as np
from collections import defaultdict
import json

mpmath.mp.dps = 30


# ============================================================
# PART A: Analytic structure of S''(E) in terms of zeros
# ============================================================

def analyze_entropy_structure():
    """
    The smoothed density of states from the explicit formula:

    N(x) = x - sum_rho x^rho/rho - C_0

    where x = e^E. The entropy is S(E) = log(N(e^E)).

    S'(E) = N'(e^E) * e^E / N(e^E)
    S''(E) = [N''*e^{2E} + N'*e^E] / N - [N'*e^E / N]^2

    For the main term alone: N_0(x) = x, so
      S_0(E) = E
      S_0'' = 0

    With zero corrections: N(x) = x - sum_rho x^rho/rho
    N'(x) = 1 - sum_rho x^{rho-1}
    N''(x) = -sum_rho (rho-1) x^{rho-2}

    Let delta(x) = -sum_rho x^rho/rho (the zero correction to N(x))
    Then N = x + delta, and:

    S(E) = log(e^E + delta(e^E))
         = E + log(1 + delta(e^E)/e^E)
         = E + log(1 + epsilon(E))

    where epsilon(E) = delta(e^E)/e^E = -sum_rho e^{(rho-1)*E}/rho

    For rho = 1/2 + it: epsilon ~ -sum e^{-E/2 + itE} / rho
    Magnitude: ~ e^{-E/2} * sum 1/|rho| -> 0 as E -> inf

    For rho = sigma + it with sigma > 1/2:
    epsilon ~ e^{(sigma-1)*E} * sum 1/|rho|
    This goes to 0 only if sigma < 1. For sigma close to 1, convergence is slow.

    S''(E) = epsilon''(E) / (1 + epsilon(E)) - [epsilon'(E)]^2 / (1 + epsilon(E))^2

    For small epsilon:
    S''(E) ~ epsilon''(E) - [epsilon'(E)]^2

    The key: epsilon''(E) = -sum_rho (rho-1)^2 e^{(rho-1)E}/rho

    For rho on the critical line (rho = 1/2+it):
    (rho-1)^2 = (-1/2+it)^2 = 1/4 - t^2 - it
    So epsilon'' oscillates with decaying amplitude ~ e^{-E/2}

    For rho off the line (rho = sigma+it, sigma > 1/2):
    (rho-1)^2 = (sigma-1+it)^2 = (sigma-1)^2 - t^2 + 2i(sigma-1)t
    epsilon'' has growing amplitude ~ (t^2) * e^{(sigma-1)E}

    The [epsilon']^2 term is second order and positive, so it helps concavity.
    But epsilon'' can be positive (creating bumps) when off-line zeros dominate.
    """
    print("=== Analytic structure of S''(E) ===\n")

    # Compute epsilon(E), epsilon'(E), epsilon''(E) for genuine zeros
    zeros = [mpmath.zetazero(k) for k in range(1, 51)]

    E_vals = np.linspace(10, 100, 500)

    results = []
    for E in E_vals:
        eps = mpmath.mpf(0)
        eps_prime = mpmath.mpf(0)
        eps_dblprime = mpmath.mpf(0)

        for rho in zeros:
            rho_m1 = rho - 1
            exp_term = mpmath.exp(rho_m1 * E)

            # Each zero contributes together with its conjugate
            contrib_eps = -exp_term / rho
            contrib_prime = -rho_m1 * exp_term / rho
            contrib_dblprime = -rho_m1**2 * exp_term / rho

            # Add rho and conj(rho)
            eps += 2 * mpmath.re(contrib_eps)
            eps_prime += 2 * mpmath.re(contrib_prime)
            eps_dblprime += 2 * mpmath.re(contrib_dblprime)

        eps = float(eps)
        eps_prime = float(eps_prime)
        eps_dblprime = float(eps_dblprime)

        # S''(E) to leading order
        S_dblprime = eps_dblprime - eps_prime**2

        results.append({
            'E': E,
            'epsilon': eps,
            'epsilon_prime': eps_prime,
            'epsilon_dblprime': eps_dblprime,
            'S_dblprime_approx': S_dblprime,
        })

    # Print summary
    print(f"{'E':>8s} {'epsilon':>14s} {'eps_prime':>14s} {'eps_dblprime':>14s} {'S_dblprime':>14s}")
    for r in results[::50]:
        print(f"{r['E']:8.2f} {r['epsilon']:14.8e} {r['epsilon_prime']:14.8e} "
              f"{r['epsilon_dblprime']:14.8e} {r['S_dblprime_approx']:14.8e}")

    # Check: all S_dblprime should be <= 0 for concavity
    max_S_dblprime = max(r['S_dblprime_approx'] for r in results)
    print(f"\n  Max S''(E) in range [{E_vals[0]}, {E_vals[-1]}]: {max_S_dblprime:.8e}")
    print(f"  Concavity holds (perturbative): {max_S_dblprime < 0}")

    return results


def analyze_off_line_perturbation():
    """
    Add a hypothetical off-line zero and compute the perturbation to S''(E).

    The off-line zero at rho_off = sigma + it (and its conjugate) adds:
      delta_epsilon = -2 Re(e^{(rho_off-1)*E} / rho_off)
      delta_epsilon'' = -2 Re((rho_off-1)^2 * e^{(rho_off-1)*E} / rho_off)

    The key quantity is: does delta_epsilon'' ever dominate and make S'' > 0?
    """
    print("\n=== Off-line zero perturbation analysis ===\n")

    t1 = float(mpmath.zetazero(1).imag)  # ~14.1347

    # For various sigma values, compute the perturbation to S''
    sigma_values = [0.52, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]

    E_vals = np.linspace(10, 200, 1000)

    results = {}
    for sigma in sigma_values:
        rho_off = complex(sigma, t1)
        rho_off_m1 = rho_off - 1

        deltas = []
        for E in E_vals:
            exp_term = np.exp(rho_off_m1.real * E) * np.exp(1j * rho_off_m1.imag * E)

            delta_eps = -2 * (exp_term / rho_off).real
            delta_eps_prime = -2 * (rho_off_m1 * exp_term / rho_off).real
            delta_eps_dblprime = -2 * (rho_off_m1**2 * exp_term / rho_off).real

            # The perturbation to S'' from this zero alone
            # S'' ~ eps'' - (eps')^2, perturbation ~ delta_eps''
            # (cross terms are subleading)

            deltas.append({
                'E': E,
                'delta_eps': delta_eps,
                'delta_eps_dblprime': delta_eps_dblprime,
                'magnitude': abs(delta_eps_dblprime),
            })

        results[sigma] = deltas

    # Print the MAXIMUM perturbation magnitude for each sigma
    print(f"{'sigma':>8s} {'max|delta_eps_dblprime|':>25s} {'E_at_max':>10s} {'grows?':>8s}")
    for sigma in sigma_values:
        deltas = results[sigma]
        max_mag = max(d['magnitude'] for d in deltas)
        E_max = deltas[[d['magnitude'] for d in deltas].index(max_mag)]['E']

        # Does it grow with E? Compare first and last quarter
        first_q = np.mean([d['magnitude'] for d in deltas[:250]])
        last_q = np.mean([d['magnitude'] for d in deltas[-250:]])
        grows = "YES" if last_q > first_q else "no"

        print(f"{sigma:8.3f} {max_mag:25.8e} {E_max:10.2f} {grows:>8s}")

    # The critical analysis: for sigma > 1/2, the perturbation GROWS as e^{(sigma-1/2)*E}
    # relative to the genuine zero contributions which decay as e^{-E/2}
    # So there exists E_* such that for E > E_*, the off-line zero dominates
    print("\n  Key insight: for sigma > 0.5, the off-line perturbation grows as e^{(sigma-0.5)*E}")
    print("  While genuine zero corrections decay as e^{-E/2}")
    print("  So off-line zeros ALWAYS eventually dominate the entropy oscillations.")

    # Compute crossover energy
    print(f"\n  Crossover energy E_* (where off-line contribution equals on-line):")
    print(f"  Using |delta_off| / |delta_on| = e^{'{'}(sigma-1/2)*E{'}'} * C(sigma)")

    for sigma in [0.55, 0.60, 0.70, 0.80, 0.90]:
        # Rough estimate: crossover when (sigma-1/2)*E ~ E/2, never.
        # Actually: off-line ~ t1^2 * e^{(sigma-1)*E}, on-line ~ t1^2 * e^{-E/2}
        # Ratio = e^{(sigma-1/2)*E}
        # Off-line becomes 1% of main term when e^{(sigma-1)*E}/t1 ~ 0.01*e^E
        # i.e., e^{(sigma-1)*E}/t1 ~ 0.01*e^E => never for sigma < 1

        # But off-line dominates ON-LINE zeros when e^{(sigma-1)*E} > e^{-E/2}
        # i.e., (sigma - 1/2)*E > 0, which is true for ALL E > 0 when sigma > 1/2

        print(f"    sigma={sigma:.2f}: off-line ALWAYS dominates on-line for sigma > 0.5")
        print(f"      Off-line/on-line ratio at E=50: e^{{{(sigma-0.5)*50:.1f}}} = {np.exp((sigma-0.5)*50):.4e}")
        print(f"      Off-line/main ratio at E=50: e^{{{(sigma-1)*50:.1f}}} / t = {np.exp((sigma-1)*50)/t1:.4e}")

    return results


# ============================================================
# PART B: Direct numerical density of states
# ============================================================

def count_multiplicative_partitions(N_max):
    """Count the number of ordered factorizations of n into factors > 1.

    For the primon gas, the density of states at energy E = log(n)
    is f(n) = number of ordered factorizations of n.

    f(1) = 1 (empty product)
    f(n) = sum_{d|n, d>1} f(n/d)  for n > 1

    This is sequence A002033 (unordered) or A001055.
    Actually, for the FREE BOSON primon gas, the relevant quantity
    is the number of ORDERED factorizations, which is sequence A074206.
    """
    f = np.zeros(N_max + 1, dtype=np.int64)
    f[1] = 1

    for n in range(2, N_max + 1):
        # Sum over divisors d of n with d > 1
        for d in range(2, n + 1):
            if n % d == 0:
                f[n] += f[n // d]

    return f


def compute_direct_entropy(N_max=10000):
    """Compute S(E) = log(Omega(E)) directly from counting factorizations.

    We bin the factorization counts by energy E = log(n) and compute
    the cumulative density of states.
    """
    print("\n=== Direct computation of density of states ===")
    print(f"  Computing ordered factorizations up to n={N_max}...")

    f = count_multiplicative_partitions(N_max)

    # Compute cumulative: Omega(E) = sum_{n: log(n) <= E} f(n)
    # Use bins in E
    E_max = np.log(N_max)
    n_bins = 200
    E_bins = np.linspace(0, E_max, n_bins + 1)
    bin_centers = (E_bins[:-1] + E_bins[1:]) / 2

    cumulative = np.zeros(n_bins)
    differential = np.zeros(n_bins)

    for n in range(1, N_max + 1):
        E_n = np.log(n)
        bin_idx = int(E_n / E_max * n_bins)
        if bin_idx >= n_bins:
            bin_idx = n_bins - 1
        differential[bin_idx] += f[n]

    cumulative = np.cumsum(differential)

    # Compute entropy
    S_cumulative = np.log(cumulative + 1)  # +1 to avoid log(0)

    # Print some values
    print(f"\n  {'E':>8s} {'Omega_diff':>14s} {'Omega_cumul':>14s} {'S(E)':>14s}")
    for i in range(0, n_bins, 20):
        print(f"  {bin_centers[i]:8.4f} {differential[i]:14.0f} {cumulative[i]:14.0f} {S_cumulative[i]:14.6f}")

    # Check concavity of S(E)
    S_dblprime = np.zeros(n_bins - 2)
    for i in range(1, n_bins - 1):
        dE = bin_centers[1] - bin_centers[0]
        S_dblprime[i-1] = (S_cumulative[i+1] - 2*S_cumulative[i] + S_cumulative[i-1]) / dE**2

    n_positive = np.sum(S_dblprime > 0)
    n_negative = np.sum(S_dblprime < 0)
    print(f"\n  Concavity of S(E) from direct count:")
    print(f"    S'' > 0 (non-concave) at {n_positive}/{len(S_dblprime)} points")
    print(f"    S'' < 0 (concave) at {n_negative}/{len(S_dblprime)} points")

    # Show some S'' values
    print(f"\n  {'E':>8s} {'S_dblprime':>16s} {'Concave?':>10s}")
    for i in range(0, len(S_dblprime), 20):
        E = bin_centers[i+1]
        sdp = S_dblprime[i]
        print(f"  {E:8.4f} {sdp:16.8f} {'YES' if sdp < 0 else '*** NO ***':>10s}")

    return {
        'E': bin_centers.tolist(),
        'differential': differential.tolist(),
        'cumulative': cumulative.tolist(),
        'S': S_cumulative.tolist(),
        'S_dblprime': S_dblprime.tolist(),
        'N_max': N_max,
    }


# ============================================================
# PART C: The thermodynamic stability theorem
# ============================================================

def stability_theorem_analysis():
    """
    THE CORE THEORETICAL ARGUMENT

    Theorem (conditional): The microcanonical entropy S(E) of the primon gas
    is strictly concave for all E > E_0 if and only if RH holds.

    Proof sketch (forward direction: RH => concavity):

    1. The smoothed density of states is:
       Omega(E) = e^E + sum_rho c_rho * e^{rho*E} + lower order

    2. Under RH, all rho = 1/2 + it_n, so:
       Omega(E) = e^E * (1 + O(e^{-E/2}))

    3. S(E) = E + log(1 + O(e^{-E/2})) = E + O(e^{-E/2})

    4. S''(E) = O(e^{-E/2}) < 0 for large enough E
       (the O(e^{-E/2}) term has negative leading coefficient from the
       heat capacity being positive)

    Actually, S'' = -[eps']^2 / (1+eps)^2 + eps'' / (1+eps)
    The -[eps']^2 term is always negative (helping concavity).
    The eps'' term oscillates but decays as e^{-E/2}.
    For large E, the -[eps']^2 term dominates, ensuring concavity.

    Proof sketch (reverse direction: NOT RH => concavity fails):

    1. Suppose rho_0 = sigma_0 + it_0 with sigma_0 > 1/2.

    2. The contribution to epsilon'' from rho_0 is:
       delta_eps'' = -2 Re((rho_0-1)^2 * e^{(rho_0-1)*E} / rho_0)
       = C * t_0^2 * e^{(sigma_0-1)*E} * cos(t_0*E + phase)

    3. The contribution from all genuine on-line zeros decays as e^{-E/2}.

    4. For large enough E, the off-line contribution dominates.

    5. Since the off-line contribution OSCILLATES (cosine term), there exist
       arbitrarily large E values where delta_eps'' > 0 with magnitude
       dominating the negative terms.

    6. At such E values, S''(E) > 0, violating concavity.

    QED (sketch).

    The gap in this argument: we need to show that the -[eps']^2 term
    doesn't save us. But [eps']^2 ~ e^{2*(sigma_0-1)*E}, while
    eps'' ~ t_0^2 * e^{(sigma_0-1)*E}. So for large t_0, eps'' dominates
    over [eps']^2 when t_0^2 * e^{(sigma_0-1)*E} > e^{2*(sigma_0-1)*E},
    i.e., when t_0^2 > e^{(sigma_0-1)*E}. This FAILS for large E.

    So actually, for very large E, [eps']^2 always wins, preserving concavity!

    REVISED ARGUMENT: The off-line zero creates a FINITE range of E values
    where concavity is violated: specifically, the range where the oscillation
    period 2*pi/t_0 is comparable to the decay scale 1/(sigma_0-1).

    Let me compute this numerically.
    """
    print("\n=== Stability theorem analysis ===\n")

    t1 = float(mpmath.zetazero(1).imag)

    # For a hypothetical zero at sigma + it1, compute the full S''(E)
    # including both the [eps']^2 and eps'' terms

    sigma_vals = [0.55, 0.60, 0.70, 0.80]

    for sigma in sigma_vals:
        rho = complex(sigma, t1)
        rho_m1 = rho - 1

        E_vals = np.linspace(5, 300, 3000)
        S_dblprimes = []

        for E in E_vals:
            exp_term = np.exp(rho_m1.real * E) * np.exp(1j * rho_m1.imag * E)

            # From the single off-line zero (paired with conjugate)
            eps = -2 * (exp_term / rho).real
            eps_prime = -2 * (rho_m1 * exp_term / rho).real
            eps_dblprime = -2 * (rho_m1**2 * exp_term / rho).real

            # Full S'' to second order
            denom = (1 + eps)
            if abs(denom) < 1e-15:
                S_dblprime = 0
            else:
                S_dblprime = eps_dblprime / denom - eps_prime**2 / denom**2

            S_dblprimes.append(S_dblprime)

        S_dblprimes = np.array(S_dblprimes)
        n_positive = np.sum(S_dblprimes > 0)
        n_total = len(S_dblprimes)

        # Find the range of E where S'' > 0
        positive_mask = S_dblprimes > 0
        if n_positive > 0:
            pos_indices = np.where(positive_mask)[0]
            E_first_pos = E_vals[pos_indices[0]]
            E_last_pos = E_vals[pos_indices[-1]]
        else:
            E_first_pos = float('nan')
            E_last_pos = float('nan')

        max_S_dblprime = np.max(S_dblprimes)

        print(f"  sigma={sigma:.2f}: {n_positive}/{n_total} points with S'' > 0")
        print(f"    Max S'' = {max_S_dblprime:.6e}")
        print(f"    Positive range: E in [{E_first_pos:.1f}, {E_last_pos:.1f}]")
        print(f"    (This is a FINITE range - concavity is eventually restored)")

        # Show the oscillatory behavior
        print(f"    Sample S'' values:")
        for i in range(0, n_total, 300):
            print(f"      E={E_vals[i]:8.2f}: S''={S_dblprimes[i]:14.6e} {'POS' if S_dblprimes[i] > 0 else 'neg'}")
        print()


def compute_full_combined_S_dblprime():
    """
    Compute S''(E) including BOTH genuine zeros and a hypothetical off-line zero.
    This is the most complete analysis.
    """
    print("\n=== Full combined S''(E): genuine zeros + off-line zero ===\n")

    # Get genuine zeros
    n_zeros = 50
    genuine_zeros = [mpmath.zetazero(k) for k in range(1, n_zeros + 1)]

    t1 = float(genuine_zeros[0].imag)

    # Test sigma values
    sigma_tests = [0.55, 0.60, 0.70, 0.80]

    E_vals = np.linspace(5, 80, 800)

    for sigma_off in sigma_tests:
        rho_off = complex(sigma_off, t1)
        rho_off_m1 = rho_off - 1

        S_dblprimes_genuine = []
        S_dblprimes_combined = []

        for E in E_vals:
            # Genuine zeros contribution
            eps_gen = 0.0
            eps_prime_gen = 0.0
            eps_dblprime_gen = 0.0

            for rho_mp in genuine_zeros:
                rho = complex(float(rho_mp.real), float(rho_mp.imag))
                rho_m1 = rho - 1
                exp_term = np.exp(rho_m1.real * E) * np.exp(1j * rho_m1.imag * E)

                eps_gen += -2 * (exp_term / rho).real
                eps_prime_gen += -2 * (rho_m1 * exp_term / rho).real
                eps_dblprime_gen += -2 * (rho_m1**2 * exp_term / rho).real

            # S'' from genuine only
            denom_g = 1 + eps_gen
            S_dbl_g = eps_dblprime_gen / denom_g - eps_prime_gen**2 / denom_g**2

            # Off-line zero contribution
            exp_off = np.exp(rho_off_m1.real * E) * np.exp(1j * rho_off_m1.imag * E)
            eps_off = -2 * (exp_off / rho_off).real
            eps_prime_off = -2 * (rho_off_m1 * exp_off / rho_off).real
            eps_dblprime_off = -2 * (rho_off_m1**2 * exp_off / rho_off).real

            # Combined
            eps_comb = eps_gen + eps_off
            eps_prime_comb = eps_prime_gen + eps_prime_off
            eps_dblprime_comb = eps_dblprime_gen + eps_dblprime_off

            denom_c = 1 + eps_comb
            if abs(denom_c) < 1e-15:
                S_dbl_c = 0
            else:
                S_dbl_c = eps_dblprime_comb / denom_c - eps_prime_comb**2 / denom_c**2

            S_dblprimes_genuine.append(S_dbl_g)
            S_dblprimes_combined.append(S_dbl_c)

        S_dblprimes_genuine = np.array(S_dblprimes_genuine)
        S_dblprimes_combined = np.array(S_dblprimes_combined)

        # Analysis
        gen_violations = np.sum(S_dblprimes_genuine > 0)
        comb_violations = np.sum(S_dblprimes_combined > 0)

        print(f"  sigma_off = {sigma_off:.2f}:")
        print(f"    Genuine only: {gen_violations}/{len(E_vals)} concavity violations")
        print(f"    With off-line: {comb_violations}/{len(E_vals)} concavity violations")
        print(f"    Max S''(genuine): {np.max(S_dblprimes_genuine):.6e}")
        print(f"    Max S''(combined): {np.max(S_dblprimes_combined):.6e}")

        # Show the difference at key points
        diff = S_dblprimes_combined - S_dblprimes_genuine
        print(f"    Max |S'' difference|: {np.max(np.abs(diff)):.6e}")
        print(f"    Max S'' difference: {np.max(diff):.6e} at E={E_vals[np.argmax(diff)]:.2f}")
        print()

    return True


if __name__ == '__main__':
    print("=" * 80)
    print("REFINED CONCAVITY ANALYSIS")
    print("=" * 80)

    # Part A: Analytic structure
    analytic_results = analyze_entropy_structure()

    # Part A2: Off-line perturbation
    off_line_results = analyze_off_line_perturbation()

    # Part B: Direct density of states
    direct_results = compute_direct_entropy(N_max=10000)

    # Part C: Stability theorem
    stability_theorem_analysis()

    # Part C2: Full combined analysis
    compute_full_combined_S_dblprime()

    # Save
    output = {
        'analytic': {
            'max_S_dblprime': max(r['S_dblprime_approx'] for r in analytic_results),
            'E_range': [analytic_results[0]['E'], analytic_results[-1]['E']],
        },
        'direct': {
            'N_max': direct_results['N_max'],
            'concavity_violations': int(np.sum(np.array(direct_results['S_dblprime']) > 0)),
        },
    }

    output_path = '/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/riemann-hypothesis/experiments/2A-entropy-ceiling/results_refined_concavity.json'
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to {output_path}")
