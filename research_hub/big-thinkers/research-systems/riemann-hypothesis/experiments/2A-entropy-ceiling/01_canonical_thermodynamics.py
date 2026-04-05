"""
01_canonical_thermodynamics.py
==============================
Compute the canonical thermodynamic functions of the primon gas:
  Z(beta) = zeta(beta)   (partition function)
  F(beta) = -log(zeta(beta))   (free energy, in units where k_B = 1)
  E(beta) = -zeta'(beta)/zeta(beta)  (mean energy)
  S(beta) = beta*E - F = beta*E + log(zeta(beta))  (entropy via Legendre)
  C(beta) = -beta^2 * dE/dbeta  (heat capacity)

We work at real beta > 1 (the convergent region of the Euler product).
The Hagedorn transition at beta = 1 (pole of zeta) is the critical point.

Author: Strategy 2A exploration
Date: 2026-04-04
"""

import mpmath
import numpy as np
import json

mpmath.mp.dps = 50  # 50 decimal places of precision


def canonical_thermodynamics(beta_val):
    """Compute all thermodynamic quantities at inverse temperature beta > 1."""
    beta = mpmath.mpf(beta_val)

    # Partition function
    Z = mpmath.zeta(beta)

    # Free energy
    F = -mpmath.log(Z)

    # Mean energy: E = -d/dbeta log(Z) = -zeta'(beta)/zeta(beta)
    # Use mpmath numerical derivative for zeta'
    zeta_prime = mpmath.diff(mpmath.zeta, beta)
    E = -zeta_prime / Z

    # Entropy via Legendre transform
    S = beta * E + mpmath.log(Z)

    # Heat capacity: C = -beta^2 * dE/dbeta
    # dE/dbeta = d/dbeta[-zeta'/zeta]
    # We compute this numerically
    def E_func(b):
        z = mpmath.zeta(b)
        zp = mpmath.diff(mpmath.zeta, b)
        return -zp / z

    dE_dbeta = mpmath.diff(E_func, beta)
    C = -beta**2 * dE_dbeta

    return {
        'beta': float(beta),
        'Z': float(Z),
        'F': float(F),
        'E': float(E),
        'S': float(S),
        'C': float(C),
        'dE_dbeta': float(dE_dbeta),
    }


def compute_near_transition():
    """Study behavior as beta -> 1+ (approaching the Hagedorn transition)."""
    # Near beta = 1, zeta(beta) ~ 1/(beta-1), so:
    #   F ~ -log(1/(beta-1)) = log(beta-1) -> -inf
    #   E ~ 1/(beta-1) -> +inf
    #   S ~ beta/(beta-1) + log(1/(beta-1)) -> +inf
    #   C ~ beta^2/(beta-1)^2 -> +inf

    results = []
    # Start far from transition, approach it
    betas = list(np.linspace(3.0, 1.1, 50)) + [1.05, 1.02, 1.01, 1.005, 1.002, 1.001]

    for b in betas:
        try:
            r = canonical_thermodynamics(b)
            results.append(r)
        except Exception as e:
            print(f"  beta={b:.4f}: FAILED ({e})")

    return results


def verify_pole_scaling():
    """Verify the scaling near the Hagedorn point beta=1.

    Near beta=1: zeta(beta) ~ 1/(beta-1) + gamma_EM + ...
    So: E(beta) ~ 1/(beta-1) + O(1)
        S(beta) ~ log(1/(beta-1)) + 1 + O(beta-1)
        C(beta) ~ 1/(beta-1)^2 + O(1/(beta-1))
    """
    print("\n=== Scaling verification near Hagedorn point ===")
    print(f"{'beta-1':>12s} {'E':>14s} {'1/(b-1)':>14s} {'E_ratio':>10s} {'S':>14s} {'log(1/(b-1))':>14s} {'C':>14s} {'1/(b-1)^2':>14s}")

    results = []
    for eps in [0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001]:
        beta = 1.0 + eps
        r = canonical_thermodynamics(beta)
        pole_E = 1.0 / eps
        pole_S = np.log(1.0 / eps) + 1.0
        pole_C = 1.0 / eps**2

        print(f"{eps:12.4f} {r['E']:14.4f} {pole_E:14.4f} {r['E']/pole_E:10.4f} "
              f"{r['S']:14.4f} {pole_S:14.4f} {r['C']:14.2f} {pole_C:14.2f}")

        results.append({
            'eps': eps,
            'beta': beta,
            **r,
            'pole_E': pole_E,
            'pole_S': pole_S,
            'pole_C': pole_C,
        })

    return results


def legendre_transform_check():
    """Verify the Legendre transform is well-defined by checking that
    E(beta) is monotonically decreasing (equivalently, C > 0).

    This is the canonical ensemble stability condition.
    If C > 0 for all beta > 1, the canonical ensemble is stable.
    """
    print("\n=== Legendre transform well-definedness (C > 0?) ===")
    betas = np.linspace(1.01, 10.0, 200)

    all_positive = True
    min_C = float('inf')
    min_C_beta = None

    for b in betas:
        r = canonical_thermodynamics(b)
        if r['C'] < 0:
            all_positive = False
            print(f"  WARNING: C({b:.3f}) = {r['C']:.6f} < 0!")
        if r['C'] < min_C:
            min_C = r['C']
            min_C_beta = b

    print(f"  Heat capacity positive for all tested beta > 1: {all_positive}")
    print(f"  Minimum C = {min_C:.6f} at beta = {min_C_beta:.3f}")

    return all_positive, min_C, min_C_beta


def compute_beta_to_energy_map():
    """Build the beta -> E mapping needed for the Legendre transform.

    The microcanonical entropy is:
      S(E) = max_beta [beta*E + log(zeta(beta))]

    At the maximum: E = -zeta'(beta*)/zeta(beta*), so beta*(E) is found by inversion.
    Then S(E) = beta*(E) * E + log(zeta(beta*(E)))
    """
    print("\n=== Beta-to-Energy mapping ===")

    betas = np.logspace(np.log10(1.001), np.log10(20.0), 300)
    mapping = []

    for b in betas:
        r = canonical_thermodynamics(b)
        mapping.append({'beta': b, 'E': r['E'], 'S': r['S']})

    # Print some representative values
    print(f"{'beta':>10s} {'E':>14s} {'S(E)':>14s}")
    for m in mapping[::30]:
        print(f"{m['beta']:10.4f} {m['E']:14.6f} {m['S']:14.6f}")

    return mapping


def microcanonical_entropy_from_legendre(E_values):
    """Compute S(E) via Legendre transform of log(zeta(beta)).

    S(E) = inf_{beta > 1} [beta*E + log(zeta(beta))]

    Wait -- the correct Legendre convention:
    The canonical free energy (Massieu function) is:
      Phi(beta) = log(Z(beta)) = log(zeta(beta))

    The entropy is the Legendre transform:
      S(E) = inf_beta [beta*E - Phi(beta)]  ... no, that gives -S.

    Let me be careful. The canonical relation is:
      Phi(beta) = log Z(beta) = S - beta*E   (using physics convention)

    So: S(E) = Phi(beta*(E)) + beta*(E) * E
    where beta*(E) solves dPhi/dbeta = -E, i.e., E = -Phi'(beta) = -zeta'(beta)/zeta(beta)

    For the Legendre transform to be well-defined, Phi must be convex in beta.
    Phi''(beta) = d^2/dbeta^2 log(zeta(beta))
    """
    print("\n=== Microcanonical entropy S(E) via Legendre transform ===")

    results = []

    for E_target in E_values:
        # Find beta* such that E(beta*) = E_target
        # E(beta) = -zeta'(beta)/zeta(beta) is monotonically decreasing from +inf to 0
        # as beta goes from 1+ to +inf

        def E_minus_target(beta_val):
            b = mpmath.mpf(beta_val)
            z = mpmath.zeta(b)
            zp = mpmath.diff(mpmath.zeta, b)
            return float(-zp / z) - E_target

        try:
            # E is large near beta=1, small for large beta
            # Find the beta where E = E_target using bisection
            from scipy.optimize import brentq

            # Check bounds
            E_low = float(-mpmath.diff(mpmath.zeta, mpmath.mpf(50.0)) / mpmath.zeta(mpmath.mpf(50.0)))
            E_high = float(-mpmath.diff(mpmath.zeta, mpmath.mpf(1.001)) / mpmath.zeta(mpmath.mpf(1.001)))

            if E_target < E_low or E_target > E_high:
                continue

            beta_star = brentq(E_minus_target, 1.001, 50.0, xtol=1e-12)

            # Compute S(E) = beta* * E + log(zeta(beta*))
            b_star = mpmath.mpf(beta_star)
            Phi = mpmath.log(mpmath.zeta(b_star))
            S = float(Phi) + beta_star * E_target

            results.append({
                'E': E_target,
                'beta_star': beta_star,
                'S': S,
                'Phi': float(Phi),
            })
        except Exception as e:
            print(f"  E={E_target:.4f}: FAILED ({e})")

    # Print results
    print(f"{'E':>10s} {'beta*':>12s} {'S(E)':>14s} {'Phi(beta*)':>14s}")
    for r in results:
        print(f"{r['E']:10.4f} {r['beta_star']:12.6f} {r['S']:14.8f} {r['Phi']:14.8f}")

    return results


def check_microcanonical_concavity(S_results):
    """Check whether S(E) is concave by computing S''(E) numerically.

    For concavity: S''(E) < 0 everywhere.

    We know S''(E) = -1 / C(beta*(E)) * beta*(E)^2
    where C is the heat capacity. So S''(E) < 0 iff C > 0.

    This is the key connection: microcanonical concavity <=> canonical stability.
    """
    print("\n=== Microcanonical concavity check: S''(E) ===")

    if len(S_results) < 3:
        print("  Not enough points for second derivative")
        return []

    E_vals = np.array([r['E'] for r in S_results])
    S_vals = np.array([r['S'] for r in S_results])
    beta_vals = np.array([r['beta_star'] for r in S_results])

    # Compute S''(E) using finite differences
    concavity_results = []
    print(f"{'E':>10s} {'S':>14s} {'S_prime':>14s} {'S_double_prime':>16s} {'beta*':>12s} {'Concave?':>10s}")

    for i in range(1, len(E_vals) - 1):
        dE_minus = E_vals[i] - E_vals[i-1]
        dE_plus = E_vals[i+1] - E_vals[i]

        S_prime = (S_vals[i+1] - S_vals[i-1]) / (E_vals[i+1] - E_vals[i-1])
        S_dblprime = 2 * ((S_vals[i+1] - S_vals[i]) / dE_plus - (S_vals[i] - S_vals[i-1]) / dE_minus) / (dE_plus + dE_minus)

        concave = S_dblprime < 0

        concavity_results.append({
            'E': E_vals[i],
            'S': S_vals[i],
            'S_prime': S_prime,
            'S_dblprime': S_dblprime,
            'beta_star': beta_vals[i],
            'concave': concave,
        })

        print(f"{E_vals[i]:10.4f} {S_vals[i]:14.8f} {S_prime:14.8f} {S_dblprime:16.10f} {beta_vals[i]:12.6f} {'YES' if concave else '*** NO ***':>10s}")

    all_concave = all(r['concave'] for r in concavity_results)
    print(f"\n  S(E) is concave everywhere in sampled range: {all_concave}")

    # Also verify via the analytic relation S'' = -1/(beta^2 * C)
    print(f"\n  Analytic check: S''(E) = -1/(beta^2 * C(beta))")
    for r in concavity_results[::5]:
        thermo = canonical_thermodynamics(r['beta_star'])
        analytic_S_dblprime = -1.0 / (r['beta_star']**2 * thermo['C']) if thermo['C'] != 0 else float('nan')
        print(f"    E={r['E']:.4f}: numerical S''={r['S_dblprime']:.10f}, analytic S''={analytic_S_dblprime:.10f}")

    return concavity_results


if __name__ == '__main__':
    print("=" * 80)
    print("PRIMON GAS: CANONICAL THERMODYNAMICS")
    print("=" * 80)

    # 1. Compute thermodynamics at sample points
    print("\n=== Sample thermodynamic values ===")
    print(f"{'beta':>8s} {'Z':>12s} {'F':>12s} {'E':>12s} {'S':>12s} {'C':>12s}")
    sample_betas = [1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 8.0, 10.0, 15.0, 20.0]
    for b in sample_betas:
        r = canonical_thermodynamics(b)
        print(f"{r['beta']:8.2f} {r['Z']:12.6f} {r['F']:12.6f} {r['E']:12.6f} {r['S']:12.6f} {r['C']:12.6f}")

    # 2. Verify pole scaling
    scaling_results = verify_pole_scaling()

    # 3. Check canonical stability (C > 0)
    stable, min_C, min_C_beta = legendre_transform_check()

    # 4. Build beta-to-E mapping
    mapping = compute_beta_to_energy_map()

    # 5. Compute microcanonical entropy
    E_values = np.linspace(0.5, 50.0, 100)
    S_results = microcanonical_entropy_from_legendre(E_values)

    # 6. Check concavity
    concavity_results = check_microcanonical_concavity(S_results)

    # 7. Save all results
    all_results = {
        'canonical_samples': [canonical_thermodynamics(b) for b in sample_betas],
        'scaling': scaling_results,
        'stability': {'all_positive': stable, 'min_C': min_C, 'min_C_beta': min_C_beta},
        'microcanonical': S_results,
        'concavity': concavity_results,
    }

    output_path = '/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/riemann-hypothesis/experiments/2A-entropy-ceiling/results_canonical.json'
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)

    print(f"\n\nResults saved to {output_path}")
    print("\n=== KEY FINDINGS ===")
    print(f"1. Heat capacity C > 0 for all beta > 1: {stable}")
    print(f"2. Minimum C = {min_C:.6f} at beta = {min_C_beta:.3f}")
    print(f"3. Microcanonical entropy S(E) computed for {len(S_results)} energy values")
    if concavity_results:
        all_concave = all(r['concave'] for r in concavity_results)
        print(f"4. S(E) strictly concave: {all_concave}")
        if concavity_results:
            max_S_dblprime = max(r['S_dblprime'] for r in concavity_results)
            print(f"5. Maximum S''(E) = {max_S_dblprime:.10f} (should be < 0 for concavity)")
