# Exploration 003: Distance-from-Gibbs Characterization

## Goal

Map TTH discrepancy vs. relative entropy (distance from Gibbs) for two families of states on coupled harmonic oscillators:
- **Family 1: Squeezed states** — S(r) applied to Gibbs, r in [0, 1.0]
- **Family 2: Post-quench states** — thermal state of H(lambda - delta_lambda), delta_lambda in [0, 0.5]

Setup: H_AB = (1/2)(p_A^2 + omega^2 q_A^2) + (1/2)(p_B^2 + omega^2 q_B^2) + lambda q_A q_B
Parameters: lambda = 0.3, beta = 2.0, omega = 1.0, N = 20 (Fock truncation)
Normal modes: omega_+ = sqrt(1.3) ~ 1.140, omega_- = sqrt(0.7) ~ 0.837

For each state: compute relative entropy S(rho || rho_Gibbs), global TTH correlator (modular flow), QM correlator (Hamiltonian flow), discrepancy, and FFT classification (structural vs quantitative).

## Control Check

**[COMPUTED]** Gibbs state (r=0 / delta_lambda=0):
- S(rho_gibbs || rho_gibbs) = 5.70e-14 (machine zero)
- ||C_QM - C_TTH|| / ||C_QM|| = 6.69e-13 (machine zero)
- **CONTROL: PASS**

## Family 1: Squeezed States

**[COMPUTED]** Two-mode squeezing S(r) = exp[r(a_A a_B - a_A† a_B†)] applied to Gibbs state. 11 data points, r from 0.0 to 1.0.

### Physics of Squeezed Discrepancy

For the squeezed state rho_sq = S rho_Gibbs S†:
- K_sq = S (beta H + logZ I) S† = beta SHS† + const
- K_sq/beta = SHS† + const — modular flow is under the unitarily-conjugated Hamiltonian
- SHS† has the **same eigenvalues** as H (unitarily equivalent)
- Therefore TTH correlator has the **same frequencies** as the QM correlator (both omega_pm)
- But different amplitudes because the observable x_A is effectively "rotated" by S
- Discrepancy is purely **QUANTITATIVE** — correct frequencies, wrong amplitudes

### Results Table

| r   | S_rel   | Discrepancy | Disc%  | Classification |
|-----|---------|-------------|--------|----------------|
| 0.0 | 0.0000  | 0.000000    | 0.0%   | QUANTITATIVE   |
| 0.1 | 0.0526  | 0.000000    | 0.0%   | QUANTITATIVE   |
| 0.2 | 0.2127  | 0.000000    | 0.0%   | QUANTITATIVE   |
| 0.3 | 0.4865  | 0.000001    | 0.0%   | QUANTITATIVE   |
| 0.4 | 0.8851  | 0.000023    | 0.0%   | QUANTITATIVE   |
| 0.5 | 1.4250  | 0.000215    | 0.0%   | QUANTITATIVE   |
| 0.6 | 2.1302  | 0.001238    | 0.1%   | QUANTITATIVE   |
| 0.7 | 3.0410  | 0.004967    | 0.5%   | QUANTITATIVE   |
| 0.8 | 4.2336  | 0.014862    | 1.5%   | QUANTITATIVE   |
| 0.9 | 5.8533  | 0.034985    | 3.5%   | QUANTITATIVE   |
| 1.0 | 8.1466  | 0.067681    | 6.8%   | QUANTITATIVE   |

### Key Observations — Family 1

**[COMPUTED]** Squeezed states remain QUANTITATIVE at all squeezing levels. Maximum discrepancy is only 6.8% even at r=1.0 (S_rel = 8.15). Correlation analysis: disc ~ S_rel^0.70, Pearson r = 0.93 (linear), 0.79 (log-log).

**[CONJECTURED]** The small discrepancy at large r is a Fock truncation artifact, not a true physics effect. Since S is unitary, K_sq/beta has exactly the same spectrum as H. The discrepancy arises because the squeezed state populates higher Fock levels that approach the truncation boundary N=20. In the continuum limit (N -> infinity), squeezed states should have exactly zero discrepancy at all r.

## Family 2: Post-Quench States

**[COMPUTED]** Post-quench state: rho = exp(-beta H(lambda - delta_lambda))/Z, dynamics under H(lambda). 11 data points, delta_lambda from 0.0 to 0.5.

### Physics of Quench Discrepancy

For the quench state rho_q = exp(-beta H')/Z:
- K_q = beta H' + logZ — modular flow is under H' (the **wrong** Hamiltonian)
- H' = H(lambda - delta_lambda) has **different** normal mode frequencies from H(lambda)
- omega_pm(H') = sqrt(1 +/- (lambda - delta_lambda)) vs omega_pm(H) = sqrt(1 +/- lambda)
- TTH correlator oscillates at omega_pm(H'), QM correlator oscillates at omega_pm(H)
- The frequency mismatch produces a **STRUCTURAL** discrepancy — wrong dynamical generator

### Results Table

| delta_lambda | lambda_eff | S_rel  | Discrepancy | Disc%  | omega+_state | omega-_state |
|--------------|------------|--------|-------------|--------|--------------|--------------|
| 0.00         | 0.300      | 0.0000 | 0.000000    | 0.0%   | 1.1402       | 0.8367       |
| 0.05         | 0.250      | 0.0016 | 0.679144    | 67.9%  | 1.1180       | 0.8660       |
| 0.10         | 0.200      | 0.0060 | 1.252492    | 125.2% | 1.0954       | 0.8944       |
| 0.15         | 0.150      | 0.0130 | 1.589970    | 159.0% | 1.0724       | 0.9220       |
| 0.20         | 0.100      | 0.0223 | 1.478987    | 147.9% | 1.0488       | 0.9487       |
| 0.25         | 0.050      | 0.0340 | 1.441425    | 144.1% | 1.0247       | 0.9747       |
| 0.30         | 0.000      | 0.0480 | 1.593298    | 159.3% | 1.0000       | 1.0000       |
| 0.35         | -0.050     | 0.0646 | 1.442532    | 144.3% | 0.9747       | 1.0247       |
| 0.40         | -0.100     | 0.0840 | 1.481549    | 148.2% | 0.9487       | 1.0488       |
| 0.45         | -0.150     | 0.1067 | 1.583214    | 158.3% | 0.9220       | 1.0724       |
| 0.50         | -0.200     | 0.1332 | 1.232570    | 123.3% | 0.8944       | 1.0954       |

### Key Observations — Family 2

**[COMPUTED]** Post-quench discrepancy jumps immediately to 68% at the smallest non-zero quench (delta_lambda = 0.05, S_rel = 0.0016). It saturates in the range 120-160% for all non-zero delta_lambda. There is no gradual onset — the transition from zero to catastrophic discrepancy is effectively discontinuous.

**[COMPUTED]** The discrepancy does not grow monotonically with S_rel. It fluctuates between 123% and 159% across all non-zero quench magnitudes, with no clear trend. The Pearson correlation between S_rel and discrepancy is only r = 0.43 (linear), though log-log correlation is higher at r = 0.99 — this is misleading since it's driven by the single delta_lambda = 0 control point.

### Note on FFT Classification

The automated FFT classifier labeled most quench states as "QUANTITATIVE" — this is an artifact of the frequency tolerance (0.08) being too coarse. At delta_lambda = 0.05, the frequency shifts are only Delta_omega ~ 0.02-0.03, which fall within the tolerance window. However, over the full time range tau in [0, 16pi ~ 50.3], even these small frequency shifts produce phase differences of ~1-1.5 radians, causing 68% norm discrepancy. The correct physical classification is **STRUCTURAL** for all non-zero delta_lambda: the modular flow generates dynamics under H', not H.

## Combined Analysis

### The Two Families Do NOT Fall on the Same Curve

**[COMPUTED]** This is the central finding. Comparing the families at similar relative entropy reveals a dramatic difference:

| Family   | Parameter   | S_rel  | Discrepancy |
|----------|-------------|--------|-------------|
| Quench   | delta_lambda = 0.05 | 0.0016 | 67.9%  |
| Quench   | delta_lambda = 0.10 | 0.0060 | 125.2% |
| Squeezed | r = 0.1     | 0.0526 | 0.0%        |
| Quench   | delta_lambda = 0.50 | 0.1332 | 123.3% |
| Squeezed | r = 0.2     | 0.2127 | 0.0%        |

At S_rel ~ 0.05, the squeezed state has 0.0% discrepancy while the quench state has ~144%. The quench family produces 100x larger discrepancy at 30x smaller relative entropy. **Relative entropy alone does not determine TTH discrepancy.**

### The Discriminating Factor: Hamiltonian Spectrum Preservation

**[CONJECTURED]** The critical distinction is whether the departure from Gibbs preserves the Hamiltonian's eigenvalue spectrum:

- **Squeezed states**: rho_sq = S rho_Gibbs S† with S unitary. The modular Hamiltonian K_sq = beta SHS† has the same spectrum as beta H. Modular flow generates dynamics under a "rotated" copy of H. Same frequencies, different amplitudes. Result: **quantitative** discrepancy, bounded by truncation effects, converges to zero in the continuum.

- **Quench states**: rho_q = exp(-beta H')/Z with H' != H. The modular Hamiltonian K_q = beta H' has a genuinely different spectrum. Modular flow generates dynamics under the wrong Hamiltonian. Different frequencies entirely. Result: **structural** discrepancy, O(1) immediately, does not converge to zero.

This is a clean theoretical prediction: **TTH discrepancy is controlled not by distance-from-Gibbs but by the spectral distance between the modular Hamiltonian and the true Hamiltonian.**

### Structural vs Quantitative Transition

**[COMPUTED]** For the squeezed family: no transition exists. All points are quantitative at all r values.

**[COMPUTED]** For the quench family: the transition is effectively a step function at delta_lambda = 0 -> any nonzero delta_lambda. There is no gradual crossover. The smallest quench (delta_lambda = 0.05) already produces 68% discrepancy.

**[CONJECTURED]** This step-function behavior is expected from the mechanism. Any nonzero delta_lambda gives H' != H, which means the modular flow generates the wrong time evolution. The phase mismatch grows linearly with time, so the integrated norm discrepancy is O(1) regardless of how small delta_lambda is (as long as the time window is large enough). The relevant scale is delta_omega * tau_max ~ 1, which is satisfied for delta_lambda = 0.05 at our tau_max = 16pi.

### Relative Entropy Ranges

**[COMPUTED]** The two families span very different relative entropy ranges:
- Squeezed: S_rel in [0, 8.15]
- Quench: S_rel in [0, 0.13]

The quench family has much smaller relative entropy because S(exp(-beta H') || exp(-beta H)) scales as beta^2 delta_lambda^2 for small delta_lambda (second-order in the perturbation), while the squeezed relative entropy scales as sinh^2(r) which grows exponentially.

## Summary Data Table

**[COMPUTED]** All 22 data points:

| # | Family   | Parameter        | S_rel   | Disc%   | Type         |
|---|----------|------------------|---------|---------|--------------|
| 1 | squeezed | r = 0.0          | 0.0000  | 0.0%    | QUANTITATIVE |
| 2 | squeezed | r = 0.1          | 0.0526  | 0.0%    | QUANTITATIVE |
| 3 | squeezed | r = 0.2          | 0.2127  | 0.0%    | QUANTITATIVE |
| 4 | squeezed | r = 0.3          | 0.4865  | 0.0%    | QUANTITATIVE |
| 5 | squeezed | r = 0.4          | 0.8851  | 0.0%    | QUANTITATIVE |
| 6 | squeezed | r = 0.5          | 1.4250  | 0.0%    | QUANTITATIVE |
| 7 | squeezed | r = 0.6          | 2.1302  | 0.1%    | QUANTITATIVE |
| 8 | squeezed | r = 0.7          | 3.0410  | 0.5%    | QUANTITATIVE |
| 9 | squeezed | r = 0.8          | 4.2336  | 1.5%    | QUANTITATIVE |
| 10| squeezed | r = 0.9          | 5.8533  | 3.5%    | QUANTITATIVE |
| 11| squeezed | r = 1.0          | 8.1466  | 6.8%    | QUANTITATIVE |
| 12| quench   | delta_lambda = 0.00 | 0.0000 | 0.0%   | CONTROL      |
| 13| quench   | delta_lambda = 0.05 | 0.0016 | 67.9%  | STRUCTURAL   |
| 14| quench   | delta_lambda = 0.10 | 0.0060 | 125.2% | STRUCTURAL   |
| 15| quench   | delta_lambda = 0.15 | 0.0130 | 159.0% | STRUCTURAL   |
| 16| quench   | delta_lambda = 0.20 | 0.0223 | 147.9% | STRUCTURAL   |
| 17| quench   | delta_lambda = 0.25 | 0.0340 | 144.1% | STRUCTURAL   |
| 18| quench   | delta_lambda = 0.30 | 0.0480 | 159.3% | STRUCTURAL   |
| 19| quench   | delta_lambda = 0.35 | 0.0646 | 144.3% | STRUCTURAL   |
| 20| quench   | delta_lambda = 0.40 | 0.0840 | 148.2% | STRUCTURAL   |
| 21| quench   | delta_lambda = 0.45 | 0.1067 | 158.3% | STRUCTURAL   |
| 22| quench   | delta_lambda = 0.50 | 0.1332 | 123.3% | STRUCTURAL   |

(Quench classification corrected from automated FFT label to physical mechanism: K_q generates flow under wrong Hamiltonian.)

## Key Findings

1. **[COMPUTED] The two families do NOT fall on the same curve.** At comparable relative entropy (~0.05), squeezed states have 0% discrepancy while quench states have ~140%. Relative entropy does not determine TTH discrepancy.

2. **[COMPUTED] Squeezed states are always quantitative.** Discrepancy grows smoothly from 0% to 6.8% as r goes from 0 to 1.0. All 11 squeezed points have correct frequencies (omega_pm) in both TTH and QM correlators.

3. **[COMPUTED] Quench states have immediate structural failure.** The smallest quench (delta_lambda = 0.05, S_rel = 0.0016) already produces 68% discrepancy. The transition is a step function, not gradual.

4. **[CONJECTURED] The discriminant is spectrum preservation, not distance.** Unitary deformations of the Gibbs state (squeezed) preserve the modular Hamiltonian spectrum -> quantitative discrepancy only. Non-unitary deformations (quench/different Hamiltonian) change the spectrum -> immediate structural failure. This is the key theoretical insight.

5. **[COMPUTED] Quench discrepancy saturates at ~120-160%.** It does not grow monotonically with delta_lambda or S_rel. Instead it fluctuates, consistent with incommensurate-frequency interference effects.
