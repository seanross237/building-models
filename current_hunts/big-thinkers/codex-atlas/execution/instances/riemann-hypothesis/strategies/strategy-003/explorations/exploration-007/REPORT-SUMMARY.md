# Exploration 007 Summary: Adversarial Novelty Review

**Goal:** Literature search to assess novelty of two live claims from the Riemann Hypothesis spectral rigidity mission.

## Key Answers (Direct)

- **Did any paper compare λ_n^zeta to λ_n^GUE?** NO. Searches across Li (1997), Bombieri-Lagarias (1999), Schumayer-Hutchinson (2011 review), and general queries for "Li coefficients GUE", "Keiper-Li spectral statistics" returned zero hits on any such comparison. The number theory community treats Li coefficients as a positivity criterion; the RMT community studies zeta zeros via pair correlations and form factors — these streams do not overlap.

- **Closest prior work on Li coefficients vs RMT:** Bombieri-Lagarias (1999) gives the asymptotic λ_n ~ (1/2) n log n + C₁ n + O(√n log n) for zeta under RH. This is for zeta alone — no GUE ensemble comparison. No prior work defines or computes λ_n for GUE matrices or identifies a crossover ratio λ_n^zeta / λ_n^GUE < 1 at large n.

- **Does Berry (1985) discuss formula accuracy degrading at high T?** NO (with high confidence). Berry's paper presents the leading-order formula Δ₃_sat = (1/π²) log(L_max) as an asymptotic result. The Royal Society page returned a 403, but all secondary sources confirm: no correction terms and no numerical accuracy table across heights in the original paper.

## Novelty Verdicts

| Claim | Verdict | Rating |
|-------|---------|--------|
| Flat Δ₃ plateau | NOT NOVEL | 0/5 |
| λ_n^zeta < λ_n^GUE crossover at n≈300 | **NOVEL** | 4/5 |
| Berry formula accuracy table T=383–2245 | ARTIFACT (likely) | 1–2/5 |
| K_primes normalization | WEAK (Berry prior art) | 1/5 |
| C1 Δ₃=0.285 intermediate | RETRACTED | 0/5 |

## Strongest Surviving Claim

**λ_n^zeta / λ_n^GUE crossover at n≈300 (ratio 0.95 at n=500).** No prior paper computes this comparison. The mechanism (super-rigidity → more uniform zero phases → efficient phase cancellation at large n) is also new. To make this publishable: would need ≥10,000 zeta zeros, GUE matrices of N ≥ 500 averaged over ≥ 5000 matrices, and a statistical test that the ratio at n=500 is significantly < 1 (currently signal-to-noise ~(1-0.95)/std requires careful estimation).

## Unexpected Finding

The complete absence of any Li-coefficients-vs-RMT comparison in the literature is itself notable — it's a natural comparison that has never been made. The two communities (Li criterion / number theory vs RMT / quantum chaos) appear to have worked in parallel without cross-pollination on this specific observable.

## Computations Identified

1. **λ_n^zeta vs λ_n^GUE with large N:** Compute with N=10,000 zeros, GUE N=1000 matrices averaged over 5000 samples. Test whether ratio at n=500 is robust. ~100-line numpy script, moderate compute.
2. **Berry formula with large zero datasets:** Repeat Δ₃_sat measurement using Odlyzko's high-T zeros (height ~10^12) with T-resolved bins, each bin containing ≥500 zeros. Would distinguish sparse-sampling artifact from genuine formula degradation.

DONE
