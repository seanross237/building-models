---
topic: Choi-Vasseur (2014) three-way pressure decomposition and P_3 absorption
confidence: verified
date: 2026-03-30
source: "vasseur-pressure exploration-005"
---

## Finding

Choi & Vasseur (2014, AIHP, arXiv:1105.1526) introduced a three-way pressure decomposition P = P_{1,k} + P_{2,k} + P_3 that simplifies the energy inequality by absorbing the k-independent piece P_3 into a time-dependent truncation level. This is a technical simplification of Vasseur (2007), NOT an improvement of the recurrence exponent beta.

### The Decomposition (Lemma 3.3, Eq. 26)

- **P_{1,k} (non-local, k-dependent):** Captures contributions from the annular region between outer cutoff and k-th iteration scale. Bounded by ||nabla P_{1,k}||_{L^inf} <= Lambda_1 * 2^{12k} * ||A||_{L^1}.
- **P_{2,k} (local, k-dependent):** All local terms including CZ-critical piece. Defined globally via Riesz transforms.
- **P_3 (k-INDEPENDENT):** Collects terms involving derivatives of the outer cutoff psi_1. Support separated from the iteration region.

### P_3 Absorption Mechanism

Since nabla P_3 is bounded in L^1_t L^inf_x, the authors define a time-dependent truncation level:

  E_k(t) = (1 - 2^{-k})_+ * integral_{-1}^{t} ||nabla P_3(s)||_{L^inf} ds

This replaces the constant truncation level (1 - 2^{-k}) used in Vasseur (2007). The P_3 contribution to the energy inequality has a FAVORABLE sign (Eq. 47: v_k * ||nabla P_3||_{L^inf} + (v_k/|u|) * u . nabla P_3 >= 0) and can be dropped. Remark 3.5 states explicitly: "the above inequality (46) does not contain the P_3 term."

The mechanism: you "pay" for the pressure gradient by letting the truncation level rise, and since nabla P_3 is integrable in time, the total rise is bounded.

### Comparison with Vasseur (2007)

In Vasseur (2007), the pressure was split four ways: P_k^1 (non-local), P_k^{21} (BOTTLENECK, non-divergence), P_k^{22}, P_k^{23} (divergence form, favorable). CV14 reorganizes:
- P_{1,k} absorbs the non-local piece (analogous to P_k^1)
- P_{2,k} absorbs ALL local terms (combines P_k^{21}, P_k^{22}, P_k^{23})
- P_3 captures outer cutoff derivative terms (genuinely new piece)

### Achieved Exponent

**Beta = 7/6** (Lemma 3.4). Remark 3.1 explicitly states: "the exponent 7/6 is not optimal and we can make it close to (4/3) arbitrarily. However, any exponent bigger than 1 is enough for our study."

This is LESS than Vasseur's beta < 4/3. The paper's purpose is proving fractional derivatives nabla^alpha u are locally integrable for 1 < alpha < 3, for which any beta > 1 suffices.

### Does NOT Bypass the P_k^{21} Bottleneck

The local pressure P_{2,k} contains the same non-divergence CZ-limited term that limits beta in Vasseur (2007). CV14 simply chose not to decompose P_{2,k} further because they don't need beta > 7/6. If one further decomposed P_{2,k}, one would recover the same P_k^{21}-type bottleneck. The P_3 absorption removes terms that were ALREADY favorable in Vasseur (2007) — it is a technical convenience, not a path around the bottleneck.
