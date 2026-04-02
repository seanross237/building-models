# Exploration 001 — Summary

## Goal
Numerically reproduce the SED harmonic oscillator ground state: var_x = 0.5, Gaussian distribution, E0 = 0.5 (natural units).

## What Was Tried
1. Inherited a partial simulation (theory + Python code, never run). Found 2 bugs (undefined `rng`, unseeded noise generator) and a critical normalization error in the ZPF spectral density (off by factor of pi).
2. Replaced the O(N^2) time-domain Velocity Verlet with an exact frequency-domain solution X(w) = F(w)/H(w), exploiting linearity.
3. Fixed the spectral density: S_F^one = 2*tau*hbar*w^3/m (not (2*tau*hbar/(pi*m))*w^3).
4. Ran 3 parameter regimes: tau=0.01 (N=2000), tau=0.001 (N=2000), tau=0.01 with 5x higher UV cutoff (N=2000).

## Outcome: PARTIAL SUCCESS

**Position variance: PASS.** var_x = 0.507 +/- 0.05 vs target 0.5 (1.4% error for best run). Confirmed across all parameter regimes. Insensitive to UV cutoff. Gaussian distribution confirmed (KS p > 0.5).

**Total energy: FAIL (but explained).** The total energy is UV-divergent because the velocity variance grows logarithmically with the frequency cutoff: var_v = 0.65 at w_max=31, 5.7 at w_max=63, 38.6 at w_max=314. This is a real physics effect (electromagnetic self-energy divergence), not a simulation bug. The potential energy PE = 0.25 matches QM correctly.

## Verification Scorecard
- **[VERIFIED]**: 2 (spectral density derivation cross-checked 3 ways; FFT normalization confirmed)
- **[COMPUTED]**: 8 (position variance, velocity variance, energy, Gaussianity tests, parameter sensitivity, UV divergence scaling, transfer function comparison, potential energy)
- **[CHECKED]**: 1 (Boyer 1975 / Marshall 1963 analytic result)
- **[CONJECTURED]**: 0

## Key Takeaway
The SED harmonic oscillator reproduces the **position distribution** of the QM ground state exactly (Gaussian with correct variance), but the **velocity/energy** is UV-divergent and requires mass renormalization. The physical prediction is var_x = hbar/(2*m*w0), NOT the total energy. The full Abraham-Lorentz transfer function (not the effective damping approximation) is required for the position variance to converge.

## Proof Gaps / Open Issues
1. **Mass renormalization**: How to extract the finite "physical" energy from the UV-divergent total energy. This would require implementing the SED renormalization procedure (separating the bare mass from the electromagnetic mass).
2. **Effective damping validity**: The commonly cited "effective Langevin equation" with Gamma*v damping gives a UV-divergent position variance. This approximation must be used with a matched UV cutoff, not independently.
3. **Multi-time correlations**: This exploration only checks single-time statistics (var_x, distribution shape). Multi-time correlations are known to differ from QM (Blanchard et al. 1986) — not tested here.

## Unexpected Findings
1. The spectral density normalization error (missing factor of pi) was present in the original theory section AND was copied into the code. The FFT amplitude formula happened to have a compensating error (extra factor of pi) that partially masked the problem — making var_x come out 2x too large instead of pi^2 times wrong. Two wrongs almost making a right.
2. The UV divergence in velocity is MUCH worse than expected: var_v scales roughly as w_max (not ln(w_max)) in the intermediate regime where |H|^2 ~ w^4 transitions to tau^2*w^6. Only at asymptotically high frequencies does the logarithmic scaling set in.

## Computations for Later
1. Implement mass renormalization to extract the physical energy E0 = hbar*w0/2.
2. Test with anharmonic potential (x^4 perturbation) — this breaks the frequency-domain approach and requires true time-domain SED simulation.
3. Compute the two-time position autocorrelation <x(t)x(0)> and compare to the QM propagator.
4. Investigate whether a form factor / spatial cutoff at the Compton wavelength gives finite velocity variance.
