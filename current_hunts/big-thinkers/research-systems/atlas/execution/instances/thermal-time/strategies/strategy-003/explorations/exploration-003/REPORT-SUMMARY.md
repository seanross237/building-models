# Exploration 003 Summary: Distance-from-Gibbs Characterization

## Goal
Map TTH discrepancy vs. relative entropy for two families of non-Gibbs states (squeezed and post-quench) on coupled harmonic oscillators (N=20 Fock space, lambda=0.3, beta=2.0).

## What Was Tried
Computed 22 data points: 11 squeezed states (r = 0 to 1.0) and 11 post-quench states (delta_lambda = 0 to 0.5). For each: relative entropy S(rho || rho_Gibbs), global TTH correlator (modular flow), QM correlator (Hamiltonian flow), norm discrepancy, and FFT spectral classification. Control check passed (discrepancy = 6.7e-13 at Gibbs).

## Outcome: SUCCEEDED — with a surprising twist

The two families produce completely different discrepancy behaviors, disproving the hypothesis that relative entropy alone determines TTH discrepancy.

- **Squeezed states**: Always quantitative. Discrepancy grows smoothly from 0% (r=0) to 6.8% (r=1.0, S_rel=8.15). Correct frequencies at all r values.
- **Post-quench states**: Immediate structural failure. Discrepancy jumps to 68% at the smallest quench (delta_lambda=0.05, S_rel=0.0016) and saturates at 120-160%. Step function, not gradual transition.

At comparable relative entropy (~0.05): squeezed = 0% discrepancy, quench = ~140%. The families are on completely different curves.

## Verification Scorecard
- **COMPUTED**: 18 claims (all numerical results, tables, both family curves, control check)
- **CONJECTURED**: 3 claims (spectrum preservation mechanism, truncation artifact interpretation, step-function scaling argument)
- **VERIFIED**: 0
- **CHECKED**: 0

## Key Takeaway

**Relative entropy (distance from Gibbs) does not control TTH discrepancy. The discriminant is whether the departure preserves the Hamiltonian spectrum.** Unitary deformations (squeezing) preserve the modular Hamiltonian's eigenvalues, producing only quantitative discrepancy that vanishes in the continuum. Non-unitary deformations (quench = different Hamiltonian Gibbs state) change the spectrum, producing immediate O(1) structural failure regardless of how small the relative entropy is.

## Proof Gaps Identified
- The claim that squeezed discrepancy is purely a truncation artifact needs verification at larger N (N=25, 30).
- The step-function nature of the quench transition deserves analytic confirmation: is the discrepancy truly O(1) for any nonzero delta_lambda in the infinite-time limit?

## Unexpected Findings
- The quench discrepancy does NOT grow monotonically with delta_lambda or S_rel. It fluctuates between 123% and 159%, suggesting interference effects from incommensurate frequencies.
- The automated FFT classifier fails to distinguish structural from quantitative for small quenches because frequency shifts are below the resolution threshold, even though norm discrepancy is 68-159%. Classification must use the physical mechanism (is K proportional to H?), not just peak-matching.

## Computations Identified
- Verify squeezed-state discrepancy vanishes at larger N (convergence study)
- Analytic calculation of quench discrepancy as a function of delta_omega * tau_max
- Test a third family (e.g., mixed states with variable purity) to further probe the spectrum-preservation hypothesis
- Compute spectral distance ||spectrum(K/beta) - spectrum(H)|| and check if it correlates better with discrepancy than relative entropy does
