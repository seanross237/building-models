# Computation Registry

Computations identified during explorations that would significantly advance the mission. Maintained by the strategizer, read by the missionary and future strategizers.

## 1. Number Variance Sigma^2(L) Computation
- **What:** Count zeros in sliding windows of length L (unfolded coordinates), compute variance, compare to GUE prediction Sigma^2(L) ~ (2/pi^2)(log(2*pi*L) + gamma + 1 - pi^2/8)
- **Why:** Probes long-range correlations where Berry predicts saturation effects. Different from pair correlation — sensitive to non-universal corrections.
- **Would resolve:** Whether there are deviations from GUE at long range (which would constrain the periodic orbit structure of the Riemann operator)
- **Source:** Exploration 001
- **Difficulty:** Easy (~50-line numpy script, uses same 2000 zeros)
- **Key references:** Berry (1985) "Semiclassical theory of spectral rigidity", Bogomolny & Keating (1996)

## 2. Exact GUE Spacing Distribution (Fredholm Determinant)
- **What:** Replace Wigner surmise with exact GUE spacing distribution (Fredholm determinant of sine kernel), compare to zeta zero spacings
- **Why:** Exploration 001's KS test marginally rejected Wigner surmise at 5%. Need to distinguish Wigner approximation error from real signal.
- **Would resolve:** Whether the marginal KS failure is an artifact of the Wigner approximation or a genuine departure from GUE
- **Source:** Exploration 001
- **Difficulty:** Medium (~100-line script using Bornemann's method or Gaudin's recursion)
- **Key references:** Bornemann (2010) "On the numerical evaluation of Fredholm determinants", Mehta (2004) "Random Matrices"

## 3. Large-Scale Zero Computation (Odlyzko-Schonhage Algorithm)
- **What:** Implement Riemann-Siegel formula + FFT to compute 10^5-10^6 zeros at heights t ~ 10^6
- **Why:** Would sharpen all GUE statistics by 10-30x, enable definitive GSE exclusion, and test height-dependence of GUE match
- **Would resolve:** Whether GUE agreement improves at large height (as Odlyzko's published results suggest), sharpen GSE exclusion from 1.2x to definitive
- **Source:** Exploration 001
- **Difficulty:** Hard (~500-line specialized script)
- **Key references:** Odlyzko (1987, 2001), Odlyzko & Schonhage (1988)

## 4. Height-Resolved Saturation Analysis
- **What:** Bin the 2000 zeros by height (e.g., T < 500, 500 < T < 1500, T > 1500), compute Sigma^2(L) separately for each bin. Test whether saturation scale L_max increases with height as Berry predicts.
- **Why:** Exploration 002 found saturation onset at L~2-5, earlier than Berry's L_max~100 for geometric mean height. This could be due to height mixing or indicate stronger-than-expected prime orbit corrections.
- **Would resolve:** Whether the early saturation onset is a height-mixing artifact or a genuine physical effect
- **Source:** Exploration 002
- **Difficulty:** Easy (~30-line extension of existing code)
- **Key references:** Berry (1985), exploration 002 analysis code

## 5. Quantitative Comparison to Berry's Explicit Saturation Formula
- **What:** Berry (1985) gives an explicit formula for saturated Sigma^2 in terms of sums over primes. Compute this theoretical prediction and compare to our measured saturation values (Sigma^2 ~ 0.3-0.5).
- **Why:** Would test quantitative, not just qualitative, correctness of Berry's theory. If the predicted saturation value matches, it confirms the prime orbit interpretation.
- **Would resolve:** Whether the EXACT saturation level matches Berry's prediction, or whether there's an unexplained quantitative discrepancy
- **Source:** Exploration 002
- **Difficulty:** Medium (~50-line script plus formula extraction from Berry's paper)
- **Key references:** Berry (1985) eq. 3.15 or similar, Bogomolny & Keating

## 6. Precomputed Zero Tables (LMFDB)
- **What:** Download zeros from LMFDB database (zeros up to height ~10^10) and rerun all statistics with 10^4-10^6 zeros
- **Why:** Would dramatically improve statistical significance of all results. Would enable definitive GSE exclusion and sharper saturation measurements.
- **Would resolve:** All precision-limited questions from explorations 001-002
- **Source:** Exploration 002
- **Difficulty:** Easy-Medium (mainly data format parsing)
- **Key references:** LMFDB (https://www.lmfdb.org), Odlyzko tables

