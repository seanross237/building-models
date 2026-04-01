"""Compute Li coefficients λ_n for Riemann zeta zeros."""
import numpy as np
from mpmath import mp, mpc, re as mpre
import time

mp.dps = 25

def compute_lambda_zeta(n_val, zeros_imag):
    """Compute λ_n using zeros with imaginary parts in zeros_imag.

    λ_n = Σ_ρ [1 - (1 - 1/ρ)^n]
    For each conjugate pair (ρ, ρ̄) with ρ = 1/2 + it:
    contribution = 2 - 2*Re[(1 - 1/ρ)^n]  (using symmetry)
    """
    total = mp.mpf(0)
    for t in zeros_imag:
        rho = mpc('0.5', str(t))
        one_minus_inv_rho = 1 - 1/rho
        power_val = one_minus_inv_rho ** n_val
        # Conjugate pair: ρ̄ = 0.5 - it gives (1-1/ρ̄)^n = conj((1-1/ρ)^n)
        # So sum = 2 - 2*Re[(1-1/ρ)^n]
        real_part = float(mpre(power_val))
        total += 2.0 - 2.0 * real_part
    return float(total)

# Load zeros
zeros_2k = np.load('t_zeros_2k.npy')
print(f"Loaded {len(zeros_2k)} zeros, range: {zeros_2k[0]:.6f} to {zeros_2k[-1]:.6f}")

# Compute at key n values
n_values = [1, 10, 50, 100, 200, 300, 400, 500]
results = {}

for n_val in n_values:
    t0 = time.time()
    lam = compute_lambda_zeta(n_val, zeros_2k)
    elapsed = time.time() - t0
    results[n_val] = lam
    print(f"λ_{n_val}^zeta (2k zeros) = {lam:.4f}  [{elapsed:.1f}s]")

# Save results
np.savez('li_zeta_2k.npz', n_values=n_values, lambda_values=[results[n] for n in n_values])
print("\nSaved to li_zeta_2k.npz")

# E002 reference values
e002_ref = {100: 59.72, 200: 288.97, 500: 881.43}
print("\nComparison with E002:")
print(f"{'n':>5} {'E008 (2k)':>15} {'E002 ref':>12} {'Match%':>10}")
for n_val in [100, 200, 500]:
    if n_val in results:
        pct = abs(results[n_val] - e002_ref[n_val]) / e002_ref[n_val] * 100
        print(f"{n_val:>5} {results[n_val]:>15.4f} {e002_ref[n_val]:>12.2f} {pct:>9.3f}%")
