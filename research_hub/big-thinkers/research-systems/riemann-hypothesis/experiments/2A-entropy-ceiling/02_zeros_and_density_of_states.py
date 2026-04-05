"""
02_zeros_and_density_of_states.py
=================================
Investigate the density of states of the primon gas using the explicit formula.

The density of states g(x) counts the number of "primon gas microstates"
at energy E = log(x). The key connection:

  zeta(s) = sum_{n=1}^{inf} a(n)/n^s

where a(n) counts the number of ways to write n as an ordered product of
prime powers (for the free boson primon gas). For the standard zeta function,
a(n) = 1 for all n, which corresponds to counting each integer state once.

More usefully, the NUMBER-THEORETIC density of states is given by the
Perron formula / explicit formula:

  N(x) = sum_{n <= x} 1 = [x] (integer part)

But the SMOOTHED density of states, whose logarithm gives the entropy,
is obtained from the inverse Mellin transform:

  Psi(x) = (1/2pi*i) integral_{c-iT}^{c+iT} zeta(s)/s * x^s ds

The explicit formula gives:
  Psi(x) = x - sum_{rho} x^rho / rho - zeta'(0)/zeta(0) - (1/2)log(1 - x^{-2})

where the sum is over nontrivial zeros rho of zeta(s).

Actually, let me be more precise. The quantity most directly related to
the primon gas partition function is:

  log(zeta(s)) = sum_p sum_k (1/k) p^{-ks}

This is the "free energy" in the canonical ensemble. The density of states
for the primon gas is related to the LOGARITHMIC derivative, not zeta itself.

Let me work with the Chebyshev function psi(x) = sum_{p^k <= x} log(p),
which has the explicit formula:

  psi(x) = x - sum_rho x^rho/rho - log(2*pi) - (1/2)log(1 - x^{-2})

The oscillatory terms from the zeros are x^rho/rho = x^{sigma+it}/(sigma+it).

KEY INSIGHT:
- If rho = 1/2 + it, the oscillatory contribution is x^{1/2+it}/(1/2+it),
  with magnitude ~ x^{1/2}/|t|
- If rho = sigma + it with sigma > 1/2, the contribution is x^{sigma+it}/(sigma+it),
  with magnitude ~ x^{sigma}/|t|
- The main term is x (from the pole at s=1)
- So zero oscillations are O(x^{1/2}) under RH, vs O(x^{sigma}) if a zero is off-line

For the ENTROPY, we need the density of states g(E) where E = log(x).
The microcanonical entropy is S(E) = log(g(E)).

Actually, let me think about this more carefully. The partition function is:
  Z(beta) = zeta(beta) = sum_{n=1}^inf n^{-beta}

The density of states (number of states at energy E = log(n)) is:
  Omega(E) = #{n : log(n) = E} = 1 for each integer

But this is the EXACT microcanonical ensemble. The SMOOTHED density of states,
from the inverse Laplace transform, is:

  Omega_smooth(E) = (1/2pi*i) integral zeta(beta) e^{beta*E} dbeta

Using the residue at beta=1 plus the sum over zeros:

  Omega_smooth(E) ~ e^E + sum_rho e^{rho*E}/f(rho) + ...

where the zeros contribute oscillatory terms e^{(sigma+it)E}.

THIS is where the concavity argument lives: if all zeros have sigma=1/2,
then oscillations in Omega_smooth are O(e^{E/2}), small relative to the
main term e^E. The entropy S(E) = log(Omega_smooth) ~ E + small corrections.
But if sigma > 1/2, oscillations are O(e^{sigma*E}), and can create
bumps that violate concavity.

Author: Strategy 2A exploration
Date: 2026-04-04
"""

import mpmath
import numpy as np
import json

mpmath.mp.dps = 30


def get_first_n_zeros(n):
    """Get the first n nontrivial zeros of zeta (on the critical line)."""
    zeros = []
    for k in range(1, n + 1):
        z = mpmath.zetazero(k)
        zeros.append({
            'n': k,
            'real': float(z.real),
            'imag': float(z.imag),
        })
    return zeros


def chebyshev_psi_explicit(x, zeros, num_trivial=10):
    """Compute psi(x) using the explicit formula.

    psi(x) = x - sum_rho x^rho/rho - log(2*pi) - (1/2)log(1 - x^{-2})

    where the sum is over nontrivial zeros (paired: rho and conj(rho)).
    """
    if x <= 1:
        return 0.0

    result = mpmath.mpf(x)

    # Sum over nontrivial zeros (take both rho and conj(rho))
    for z in zeros:
        rho = mpmath.mpc(z['real'], z['imag'])
        rho_conj = mpmath.conj(rho)

        # x^rho/rho + x^{conj(rho)}/conj(rho) = 2*Re(x^rho/rho)
        term = mpmath.power(x, rho) / rho
        result -= 2 * mpmath.re(term)

    # Constant term
    result -= mpmath.log(2 * mpmath.pi)

    # Trivial zero contributions: sum_{n=1}^{N} x^{-2n}/(-2n) = -(1/2)log(1-x^{-2})
    if x > 1:
        result -= 0.5 * mpmath.log(1 - mpmath.power(x, -2))

    return float(result)


def smoothed_density_of_states(E, zeros, include_off_line_zero=None):
    """Compute the smoothed density of states Omega(E) using the explicit formula.

    From the inverse Laplace transform of zeta(s):

    Omega_smooth(E) ~ e^E/E + sum_rho e^{rho*E} / f(rho) + ...

    More precisely, using the explicit formula for zeta:
    The saddle-point approximation of the inverse Laplace transform gives:

    Omega(E) = (1/2pi) integral_{-inf}^{inf} zeta(1 + it) e^{(1+it)E} dt

    But the residue at s=1 gives the leading term e^E, and each zero rho
    gives a contribution proportional to e^{rho*E}.

    For our purposes, the key decomposition is:
    Omega_smooth(E) = main_term(E) + oscillatory_corrections(E)

    where:
    main_term ~ e^E  (from the pole at s=1)
    oscillatory ~ sum_rho e^{Re(rho)*E} * cos(Im(rho)*E + phase) / |rho|

    We compute log(Omega) = S(E) = E + log(1 + corrections/e^E)
    """
    x = mpmath.exp(E)

    # Main term from the pole at s=1
    # From Perron's formula: residue at s=1 of zeta(s)*x^s/s = x/1 = x = e^E
    main_term = mpmath.exp(E)

    # Correction from each zero: -x^rho / rho (from Perron)
    zero_correction = mpmath.mpf(0)
    for z in zeros:
        rho = mpmath.mpc(z['real'], z['imag'])
        rho_conj = mpmath.conj(rho)

        # Each pair contributes: -x^rho/rho - x^{conj(rho)}/conj(rho)
        # = -2 Re(x^rho / rho)
        term = mpmath.power(x, rho) / rho
        zero_correction -= 2 * mpmath.re(term)

    # Add hypothetical off-line zero if specified
    off_line_correction = mpmath.mpf(0)
    if include_off_line_zero is not None:
        sigma, t = include_off_line_zero
        rho_off = mpmath.mpc(sigma, t)
        term = mpmath.power(x, rho_off) / rho_off
        off_line_correction = -2 * mpmath.re(term)

    total = main_term + zero_correction + off_line_correction

    return {
        'E': float(E),
        'main_term': float(main_term),
        'zero_correction': float(zero_correction),
        'off_line_correction': float(off_line_correction) if include_off_line_zero else 0.0,
        'total_Omega': float(total),
        'log_Omega': float(mpmath.log(abs(total))) if total > 0 else float('-inf'),
        'relative_correction': float(zero_correction / main_term),
    }


def compute_entropy_with_and_without_offline_zero(zeros, E_range, off_line_zeros):
    """Compare S(E) = log(Omega(E)) with genuine zeros vs. with added off-line zeros."""

    results = {
        'E': [],
        'S_genuine': [],         # S(E) with only genuine critical-line zeros
        'S_with_offline': {},    # S(E) for each hypothetical off-line zero
        'corrections': {},
    }

    for olz in off_line_zeros:
        key = f"sigma={olz[0]:.2f}_t={olz[1]:.2f}"
        results['S_with_offline'][key] = []
        results['corrections'][key] = []

    for E in E_range:
        # Genuine zeros only
        r_genuine = smoothed_density_of_states(E, zeros)
        results['E'].append(float(E))
        results['S_genuine'].append(r_genuine['log_Omega'])

        # With each hypothetical off-line zero
        for olz in off_line_zeros:
            key = f"sigma={olz[0]:.2f}_t={olz[1]:.2f}"
            r_off = smoothed_density_of_states(E, zeros, include_off_line_zero=olz)
            results['S_with_offline'][key].append(r_off['log_Omega'])
            results['corrections'][key].append(r_off['off_line_correction'])

    return results


def compute_concavity_comparison(E_vals, S_genuine, S_offline_dict):
    """Compute S''(E) for the genuine case and each off-line case."""

    results = {'E': [], 'S_dblprime_genuine': []}
    for key in S_offline_dict:
        results[f'S_dblprime_{key}'] = []

    E = np.array(E_vals)
    S_g = np.array(S_genuine)

    for i in range(1, len(E) - 1):
        dE_m = E[i] - E[i-1]
        dE_p = E[i+1] - E[i]

        S_dblprime_g = 2 * ((S_g[i+1] - S_g[i])/dE_p - (S_g[i] - S_g[i-1])/dE_m) / (dE_p + dE_m)

        results['E'].append(E[i])
        results['S_dblprime_genuine'].append(S_dblprime_g)

        for key, S_off in S_offline_dict.items():
            S_o = np.array(S_off)
            S_dblprime_o = 2 * ((S_o[i+1] - S_o[i])/dE_p - (S_o[i] - S_o[i-1])/dE_m) / (dE_p + dE_m)
            results[f'S_dblprime_{key}'].append(S_dblprime_o)

    return results


def analyze_zero_contribution_magnitudes(zeros, E_values):
    """For each zero, compute |x^rho / rho| relative to the main term x = e^E.

    This shows how much each zero contributes to fluctuations in Omega(E).
    """
    results = []

    for E in E_values:
        x = np.exp(E)
        main_term = x  # e^E

        contributions = []
        for z in zeros[:20]:  # First 20 zeros
            sigma = z['real']
            t = z['imag']
            # |x^rho / rho| = x^sigma / |rho|
            magnitude = x**sigma / np.sqrt(sigma**2 + t**2)
            relative = magnitude / main_term  # = x^(sigma-1) / |rho|
            contributions.append({
                'zero_n': z['n'],
                'sigma': sigma,
                't': t,
                'magnitude': magnitude,
                'relative': relative,
            })

        results.append({
            'E': E,
            'main_term': main_term,
            'contributions': contributions,
        })

    return results


def off_line_zero_critical_sigma(E, t, threshold=0.01):
    """Find the critical sigma at which an off-line zero at sigma+it creates
    oscillations large enough to potentially break concavity.

    The ratio of zero contribution to main term is:
      r = e^{(sigma-1)*E} / |sigma + it|

    For this to be significant, we need r > threshold.
    So sigma > 1 + log(threshold * |sigma+it|) / E

    This is approximately sigma > 1 + log(threshold * t) / E for large t.
    """
    # Solve: e^{(sigma-1)*E} / sqrt(sigma^2 + t^2) = threshold
    # (sigma-1)*E = log(threshold * sqrt(sigma^2 + t^2))
    # sigma = 1 + log(threshold * sqrt(sigma^2 + t^2)) / E

    # Iterate
    sigma = 0.5
    for _ in range(50):
        sigma_new = 1.0 + np.log(threshold * np.sqrt(sigma**2 + t**2)) / E
        if abs(sigma_new - sigma) < 1e-12:
            break
        sigma = sigma_new

    return sigma


if __name__ == '__main__':
    print("=" * 80)
    print("PRIMON GAS: DENSITY OF STATES AND ZERO CONTRIBUTIONS")
    print("=" * 80)

    # 1. Get the first 100 nontrivial zeros
    print("\n=== Computing first 100 nontrivial zeros ===")
    zeros = get_first_n_zeros(100)
    print(f"  First 5 zeros: {[(z['real'], z['imag']) for z in zeros[:5]]}")
    print(f"  All zeros on critical line (Re=0.5): {all(abs(z['real'] - 0.5) < 1e-10 for z in zeros)}")

    # 2. Compute density of states with explicit formula
    print("\n=== Smoothed density of states (genuine zeros) ===")
    E_values = np.linspace(5, 60, 200)
    genuine_results = []

    print(f"{'E':>8s} {'main_term':>14s} {'zero_corr':>14s} {'total_Omega':>14s} {'S(E)':>14s} {'rel_corr':>14s}")
    for E in E_values[::20]:
        r = smoothed_density_of_states(E, zeros)
        genuine_results.append(r)
        print(f"{r['E']:8.2f} {r['main_term']:14.4e} {r['zero_correction']:14.4e} "
              f"{r['total_Omega']:14.4e} {r['log_Omega']:14.6f} {r['relative_correction']:14.8f}")

    # 3. Compare with hypothetical off-line zeros
    print("\n=== Effect of hypothetical off-line zeros ===")

    # Hypothetical zeros: shift the first zero (0.5 + 14.13i) off the line
    t1 = zeros[0]['imag']  # ~ 14.134725
    off_line_zeros = [
        (0.55, t1),   # Slightly off: sigma = 0.55
        (0.6, t1),    # Moderately off: sigma = 0.6
        (0.7, t1),    # Significantly off: sigma = 0.7
        (0.8, t1),    # Very off: sigma = 0.8
        (0.9, t1),    # Nearly at boundary: sigma = 0.9
    ]

    E_dense = np.linspace(5, 60, 500)
    comparison = compute_entropy_with_and_without_offline_zero(zeros, E_dense, off_line_zeros)

    # Print comparison at select points
    print(f"\n{'E':>8s} {'S_genuine':>14s}", end='')
    for olz in off_line_zeros:
        print(f" {'S(σ=' + f'{olz[0]:.2f})':>14s}", end='')
    print()

    for i in range(0, len(E_dense), 50):
        E = comparison['E'][i]
        S_g = comparison['S_genuine'][i]
        print(f"{E:8.2f} {S_g:14.6f}", end='')
        for olz in off_line_zeros:
            key = f"sigma={olz[0]:.2f}_t={olz[1]:.2f}"
            S_o = comparison['S_with_offline'][key][i]
            print(f" {S_o:14.6f}", end='')
        print()

    # 4. Concavity comparison
    print("\n=== Concavity comparison: S''(E) ===")
    concavity = compute_concavity_comparison(
        comparison['E'],
        comparison['S_genuine'],
        comparison['S_with_offline']
    )

    # Report
    print(f"\n{'E':>8s} {'S_gen':>14s}", end='')
    for olz in off_line_zeros:
        key = f"sigma={olz[0]:.2f}_t={olz[1]:.2f}"
        print(f" {'S_σ=' + f'{olz[0]:.2f}':>14s}", end='')
    print()

    violations = {f"sigma={olz[0]:.2f}_t={olz[1]:.2f}": 0 for olz in off_line_zeros}
    gen_violations = 0

    for i in range(0, len(concavity['E']), 50):
        E = concavity['E'][i]
        sdp_g = concavity['S_dblprime_genuine'][i]
        if sdp_g > 0:
            gen_violations += 1
        print(f"{E:8.2f} {sdp_g:14.8f}", end='')
        for olz in off_line_zeros:
            key = f"sigma={olz[0]:.2f}_t={olz[1]:.2f}"
            sdp_o = concavity[f'S_dblprime_{key}'][i]
            if sdp_o > 0:
                violations[key] += 1
            print(f" {sdp_o:14.8f}", end='')
        print()

    print(f"\n  Concavity violations (S'' > 0):")
    print(f"    Genuine zeros: {gen_violations}/{len(concavity['E'])}")
    for olz in off_line_zeros:
        key = f"sigma={olz[0]:.2f}_t={olz[1]:.2f}"
        total = len(concavity[f'S_dblprime_{key}'])
        print(f"    Off-line σ={olz[0]:.2f}: {violations[key]}/{total}")

    # 5. Analyze contribution magnitudes
    print("\n=== Zero contribution magnitudes ===")
    mag_results = analyze_zero_contribution_magnitudes(zeros, [10, 20, 30, 50])
    for mr in mag_results:
        print(f"\n  E = {mr['E']:.0f}:")
        print(f"    Main term = {mr['main_term']:.4e}")
        print(f"    {'Zero':>6s} {'σ':>6s} {'t':>10s} {'|contrib|':>14s} {'relative':>14s}")
        for c in mr['contributions'][:5]:
            print(f"    {c['zero_n']:6d} {c['sigma']:6.3f} {c['t']:10.4f} {c['magnitude']:14.4e} {c['relative']:14.8e}")

    # 6. Critical sigma analysis
    print("\n=== Critical sigma: what sigma breaks concavity? ===")
    for E in [10, 20, 30, 50, 100]:
        for threshold in [0.01, 0.05, 0.1]:
            sigma_crit = off_line_zero_critical_sigma(E, t1, threshold)
            print(f"  E={E:4d}, threshold={threshold:.2f}: sigma_crit = {sigma_crit:.4f}")

    # Save results
    save_data = {
        'zeros_used': len(zeros),
        'first_5_zeros': zeros[:5],
        'comparison_E_range': [float(E_dense[0]), float(E_dense[-1])],
        'off_line_zeros_tested': off_line_zeros,
        'concavity_violations_genuine': gen_violations,
        'concavity_violations': violations,
    }

    output_path = '/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/riemann-hypothesis/experiments/2A-entropy-ceiling/results_density_of_states.json'
    with open(output_path, 'w') as f:
        json.dump(save_data, f, indent=2, default=str)

    print(f"\nResults saved to {output_path}")
