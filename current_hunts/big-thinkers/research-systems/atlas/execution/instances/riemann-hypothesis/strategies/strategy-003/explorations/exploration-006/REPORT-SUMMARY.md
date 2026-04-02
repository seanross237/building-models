# Exploration 006 Summary: K(tau) from Prime Orbit Sums

## Goal
Determine whether Berry's prime orbit diagonal approximation predicts Delta_3_sat = 0.155 (zeta zeros value) or 0.294 (GUE value), by computing K_primes(tau) and feeding it through the Sigma_2 -> Delta_3 chain.

## What Was Tried
1. Computed K_primes(tau) from the diagonal approximation with corrected weight (log p)^2 / p^m (the GOAL.md template was missing the critical 1/p^m factor)
2. Attempted K(tau) -> Sigma_2 -> Delta_3 integral chain for three K models (no-cap, cap, GUE)
3. Computed Berry's direct formula Delta_3_sat = (1/pi^2) log(log(T/(2*pi))) at several T values

## Outcome: PARTIAL SUCCESS

**Berry's direct formula predicts Delta_3_sat ≈ 0.155.** At T=600, Berry gives 0.154 (0.6% error). At T_geo=1127, Berry gives 0.167 (8% error). The prime counting structure encoded in log(log(T)) directly explains the 47% rigidity gap over GUE.

**The K(tau) -> Sigma_2 integral route has an unresolved normalization issue.** The GUE control case gives Delta_3(L=10) = 0.491 vs the known value 0.226 (~2x too large). Relative comparisons show K_primes-cap is only 3.3% above GUE, meaning the cap essentially recovers GUE — the diagonal approximation K ≈ tau for tau<1 is too close to K_GUE to differentiate them through this route.

## Verification Scorecard
- [COMPUTED]: 6 claims
- [CHECKED]: 2 claims
- [CONJECTURED]: 1 claim

## Key Takeaway
The prime orbit structure explains Delta_3_sat = 0.155 through Berry's analytical formula, not through the K(tau) integral. The diagonal approximation gives K_primes ≈ 0.94*tau for tau<1 (close to GUE), but K_primes decays to 0 past tau=1 (unlike GUE which stays at 1). The super-rigidity arises because the Heisenberg-time saturation mechanism in Berry's derivation yields a log(log(T)) growth rate that is fundamentally slower than GUE's log(L) growth.

## Proof Gaps Identified
- The Fourier relation Sigma_2 = L - (2/pi^2) integral [1-K] sin^2/tau^2 dtau yields GUE values ~2x too large. Suspect a Fourier convention mismatch (angular vs ordinary frequency) or a missing 1/2 factor. Resolving this would make the K -> Delta_3 route quantitative.

## Unexpected Findings
- GOAL.md template had wrong weight: (log p)^2 instead of (log p)^2 / p^m. Without the 1/p^m semiclassical amplitude factor, K_primes was O(100) instead of O(1). This is a critical normalization that must be included.
- K_primes with saturation cap gives Delta_3 essentially equal to GUE (within 3%), not 0.155. The super-rigidity is NOT visible in the K<1 region — it's entirely a consequence of the saturation mechanism (how K behaves near and beyond tau=1).

## Computations Identified
- Fix the Sigma_2 ↔ K(tau) normalization (resolve the 2x discrepancy in GUE control values)
- Compute K(tau) empirically from the zero data (Fourier transform of R_2) and compare to K_primes — E003 attempted this but got noisy results
- Test Berry's formula at larger T (10000+ zeros) to see if the 8% discrepancy at T_geo grows or shrinks
