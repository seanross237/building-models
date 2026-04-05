#!/usr/bin/env python3
"""
Contour deformation analysis and the ensemble equivalence breakdown.

Demonstrates that the saddle-point approximation (ensemble equivalence)
works for Re(s) > 1 but breaks down at Re(s) = 1/2 due to the
Bohr-Jessen variance divergence.

Also computes the Dickman function and the density of N-smooth numbers.
"""

import numpy as np

# ============================================================
# Utilities
# ============================================================

def primes_up_to(N):
    if N < 2:
        return []
    sieve = [True] * (N + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(N**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, N + 1, i):
                sieve[j] = False
    return [i for i in range(2, N + 1) if sieve[i]]


# ============================================================
# Part 1: |Z_N(sigma+it)| fluctuations along vertical lines
# ============================================================

def fluctuation_analysis():
    print("=" * 70)
    print("|Z_N(sigma+it)| FLUCTUATIONS ALONG VERTICAL LINES")
    print("=" * 70)

    print(f"\n{'N':>6} {'sigma':>6} {'mean':>12} {'max':>12} {'std':>12}")

    for N in [100, 1000]:
        ps = primes_up_to(N)
        for sigma in [2.0, 1.5, 1.0, 0.75, 0.5]:
            vals = []
            for t in np.linspace(1, 100, 500):
                s = complex(sigma, t)
                log_Z = sum(-np.log(abs(1 - p**(-s))) for p in ps
                           if abs(1 - p**(-s)) > 1e-300)
                vals.append(np.exp(log_Z) if log_Z < 100 else np.inf)

            finite_vals = [v for v in vals if np.isfinite(v)]
            if finite_vals:
                arr = np.array(finite_vals)
                print(f"{N:>6} {sigma:>6.2f} {np.mean(arr):>12.4f} "
                      f"{np.max(arr):>12.4f} {np.std(arr):>12.4f}")


# ============================================================
# Part 2: Bohr-Jessen variance verification
# ============================================================

def bohr_jessen_verification():
    print("\n" + "=" * 70)
    print("BOHR-JESSEN VARIANCE: THEORY vs NUMERICAL")
    print("=" * 70)

    print(f"\n{'N':>6} {'sigma':>6} {'V_numerical':>14} {'V_theory':>14} {'ratio':>10}")

    for N in [100, 1000, 10000]:
        ps = primes_up_to(N)
        for sigma in [0.50, 0.55, 0.60, 0.75, 1.00, 1.50, 2.00]:
            # Theoretical: V = (1/2) * sum_p p^{-2*sigma}
            V_theory = 0.5 * sum(p**(-2*sigma) for p in ps)

            # Numerical: compute log|Z_N(sigma+it)| for many t
            log_vals = []
            for t in np.linspace(10, 1000, 2000):
                s = complex(sigma, t)
                log_Z = 0.0
                for p in ps:
                    z = 1 - p**(-s)
                    if abs(z) > 1e-300:
                        log_Z += -np.log(abs(z))
                log_vals.append(log_Z)

            V_numerical = np.var(log_vals)
            ratio = V_numerical / V_theory if V_theory > 0 else float('nan')
            print(f"{N:>6} {sigma:>6.2f} {V_numerical:>14.4f} {V_theory:>14.4f} {ratio:>10.4f}")

    print("""
  At sigma = 0.5: V diverges as (1/2)*sum_p 1/p ~ (1/2)*log(log N).
  At sigma > 0.5: V converges to a finite limit.

  This is the mechanism: growing fluctuations at sigma=1/2 produce
  near-zeros of Z_N that become actual zeros of zeta in the limit.
  """)


# ============================================================
# Part 3: Dickman's function
# ============================================================

def dickman_rho(u, num_steps=10000):
    """Compute Dickman's rho function numerically."""
    if u <= 0:
        return 0.0
    if u <= 1:
        return 1.0
    if u <= 2:
        return 1 - np.log(u)

    h = (u - 1.0) / num_steps
    grid = np.linspace(1.0, u, num_steps + 1)
    rho_vals = np.zeros(num_steps + 1)
    rho_vals[0] = 1.0

    for i in range(num_steps):
        t = grid[i]
        t_m1 = t - 1.0
        if t_m1 <= 0:
            rho_tm1 = 0.0
        elif t_m1 <= 1:
            rho_tm1 = 1.0
        elif t_m1 <= 2:
            rho_tm1 = 1 - np.log(t_m1)
        else:
            idx = int((t_m1 - 1.0) / h)
            idx = min(idx, len(rho_vals) - 1)
            if idx + 1 < len(rho_vals):
                frac = (t_m1 - grid[idx]) / h
                rho_tm1 = rho_vals[idx] * (1 - frac) + rho_vals[idx + 1] * frac
            else:
                rho_tm1 = rho_vals[idx]

        rho_vals[i + 1] = rho_vals[i] + h * (-rho_tm1 / t)

    return rho_vals[-1]


def dickman_analysis():
    print("\n" + "=" * 70)
    print("DICKMAN'S FUNCTION AND N-SMOOTH NUMBER DENSITY")
    print("=" * 70)

    print("\n  Dickman's function rho(u):")
    for u in [0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 7.0, 10.0]:
        r = dickman_rho(u)
        print(f"    rho({u:.1f}) = {r:.8f}")

    print(f"\n  Density of states quality: Omega_N(E) ~ e^E * rho(E/log N)")
    print(f"  {'N':>8} {'E':>6} {'u=E/logN':>10} {'rho(u)':>12} {'quality':>20}")

    for N in [10, 100, 1000, 10000, 100000]:
        for E in [5, 10, 20]:
            u = E / np.log(N)
            r = dickman_rho(u)
            quality = "main term dominates" if r > 0.99 else \
                      "moderate correction" if r > 0.5 else "poor approximation"
            print(f"  {N:>8} {E:>6} {u:>10.4f} {r:>12.8f} {quality:>20}")


# ============================================================
# Part 4: Large deviation rate function
# ============================================================

def rate_function_analysis():
    print("\n" + "=" * 70)
    print("LARGE DEVIATION RATE FUNCTION")
    print("=" * 70)

    def phi_N(beta, primes):
        """Free energy per particle."""
        return sum(-np.log(1 - p**(-beta)) for p in primes) / len(primes)

    def phi_N_prime(beta, primes):
        return sum(np.log(p) * p**(-beta) / (1 - p**(-beta)) for p in primes) / len(primes)

    # Verify strict concavity of rate function
    print("\n  Concavity verification of I_N(e) = sup_beta [beta*e - phi_N(beta)]:")

    for N in [10, 100, 1000]:
        ps = primes_up_to(N)

        e_vals = []
        I_vals = []

        for beta in np.linspace(0.5, 10.0, 200):
            e = phi_N_prime(beta, ps)
            I = beta * e - phi_N(beta, ps)
            e_vals.append(e)
            I_vals.append(I)

        violations = 0
        for i in range(1, len(e_vals) - 1):
            if e_vals[i+1] != e_vals[i-1]:
                t = (e_vals[i] - e_vals[i-1]) / (e_vals[i+1] - e_vals[i-1])
                I_interp = (1 - t) * I_vals[i-1] + t * I_vals[i+1]
                if I_vals[i] < I_interp - 1e-10:
                    violations += 1

        print(f"    N={N}: {violations} concavity violations out of {len(e_vals)-2} checks")


# ============================================================
# Part 5: Summary of the failure mechanism
# ============================================================

def print_summary():
    print("\n" + "=" * 70)
    print("THE ENSEMBLE EQUIVALENCE BREAKDOWN MECHANISM")
    print("=" * 70)
    print("""
  The inverse Laplace transform for the density of states:

    Omega_N(E) = (1/2pi*i) * integral Z_N(s) * e^{sE} ds

  WORKS (saddle-point valid) when:
    - Contour at Re(s) = c > 1
    - Z_N(s) is smooth and nonzero along contour
    - Fluctuations bounded (Bohr-Jessen variance < infinity)

  FAILS when deforming to Re(s) = 1/2 because:
    - Bohr-Jessen variance V(1/2) ~ (1/2)*log(log N) -> infinity
    - |Z_N(1/2+it)| develops near-zeros
    - Saddle-point approximation breaks down
    - The explicit formula's oscillatory terms (from zeta zeros) are
      precisely the NON-GAUSSIAN contributions that the saddle-point misses

  CONSEQUENCE:
    Ensemble equivalence proves concavity for REAL energies E.
    RH requires concavity of the EXPLICIT FORMULA entropy, which includes
    oscillatory corrections from the zeros. These corrections are invisible
    to the saddle-point (ensemble equivalence) approach.

  THE GAP IS EXACTLY RH.
  """)


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    fluctuation_analysis()
    bohr_jessen_verification()
    dickman_analysis()
    rate_function_analysis()
    print_summary()
