---
topic: Frequency-localized De Giorgi via Littlewood-Paley — LP decomposition cannot improve beta (Bernstein structural obstruction)
confidence: computed + conjectured
date: 2026-03-30
source: "vasseur-pressure s2-exploration-005; Bony 1981 paraproduct; Bernstein inequality"
---

## Main Finding: LP Decomposition Cannot Improve Beta

Littlewood-Paley (LP) frequency decomposition of the De Giorgi pressure P^{21} **cannot** improve beta beyond 4/3. The obstruction is structural (dimensional), not technical. Four independent lines of evidence converge on the same conclusion.

CZ is already the optimal frequency-by-frequency estimate: LP decomposition makes explicit the frequency structure that CZ handles implicitly, without improvement.

## Four Independent Lines of Evidence

### 1. Spectral Peak Shift [COMPUTED]

The LP block j* carrying the most L^2 energy in P^{21} shifts to HIGHER frequencies as the De Giorgi level k increases:

| k | Peak block j* | Peak freq 2^{j*+1} | Active fraction |
|---|---|---|---|
| 1 | 0 | 2 | 0.414 |
| 4 | 3 | 16 | 0.011 |
| 6 | 4 | 32 | 0.001 |
| 7 | 5 | 64 | 0.000008 |

(N=128, Re=1000, Taylor-Green.) The upward migration is monotonic and consistent across all tested datasets (Taylor-Green N=64, Kida-Pelz N=64, Taylor-Green N=128). This makes the high-frequency problem WORSE at exactly the De Giorgi levels where the recurrence needs to close.

### 2. Growing I_hi/I_total with k [COMPUTED]

The high-frequency fraction of the bottleneck integral I_k = int |P^{21}| |d_k| 1_{v_k>0} dx increases with k:

| k | I_hi/I_total (TG) | I_hi/I_total (KP) |
|---|---|---|
| 1 | 0.006 | 0.016 |
| 3 | 0.028 | 0.092 |
| 6 | 0.203 | -- |

The LP-unimprovable portion grows from ~1% at k=1 to ~20% at k=6. Even magically zeroing the low-frequency contribution leaves an irreducible high-frequency residual at the De Giorgi levels where the argument must work.

### 3. Bernstein Inflation [COMPUTED]

The LP route gives L^{10/3} bounds that are **5-10x worse** than direct CZ:

| k | LP Bernstein bound / actual L^{10/3} |
|---|---|
| 1 | 5.75x |
| 2 | 8.17x |
| 3 | 7.80x |
| 4 | 7.48x |
| 5 | 7.22x |

(N=128, Re=1000.) At N=64 Kida-Pelz, the inflation ratio is even worse: 10.2x. The Bernstein factor 2^{3j/5} overwhelms the spectral decay at high k.

### 4. Analytical Exponent Chain [CONJECTURED]

Three LP-based approaches all introduce a growing factor 2^{alpha J} with alpha > 0 that cannot be eliminated:

- **Approach A (Bernstein + L^2):** ||S_J P^{21}||_{L^{10/3}} <= C 2^{3J/5} ||S_J P^{21}||_{L^2}. Penalty 2^{3J/5} grows with J.
- **Approach B (Commutator + Bernstein):** CLMS gives L^1, but L^1 -> L^{10/3} via Bernstein costs 2^{21J/10}. Catastrophically bad.
- **Approach C (Paraproduct block):** Each Dyadic block: ||Delta_j P_T||_{L^{10/3}} <= C ||u^{below}||_{L^{10/3}} 2^{3j/5} ||Delta_j u^{above}||_{L^2}. Summing: same 2^{3J/5} penalty.

The optimum over J is NEVER better than unsplit CZ.

## Bernstein Exchange Rate: 2^{3j/5} Is Dimensional and Structural

The factor 2^{3j/5} is the Bernstein inequality cost of going from L^2 to L^{10/3} on a dyadic shell at frequency 2^j. It equals exactly the 3/10 effective derivatives required by the Sobolev embedding L^2_{3/10} -> L^{10/3} in 3D. The Holder triple (10/3, 10/7, 2) is fixed by dimensional analysis. This cost is the SAME as what CZ already accounts for via elliptic regularity. The exchange rate is NOT technical but STRUCTURAL: it is set by dimension and integrability target.

## Paraproduct Transition: Resonance -> Paraproduct Dominance [COMPUTED]

Bony (1981) paraproduct decomposition u^{below} u^{above} = T_{u^below} u^{above} + T_{u^above} u^{below} + R(u^{below}, u^{above}) reveals a k-dependent character change:

| k | Dominant term | Notes |
|---|---|---|
| 1-2 | R (resonance) | Same-frequency interaction, hardest to estimate |
| 3+ | T_{u^below} u^{above} (paraproduct) | Smooth x rough = exactly CZ exponents |

T_{u^above} u^{below} is always negligible (<5%). The transition means NO single technique handles all De Giorgi levels optimally: resonance dominates where commutator tools might help, but paraproduct dominates where the De Giorgi argument most needs to close. The paraproduct piece inherits exactly the standard CZ estimate.

## Why LP Fails: CZ IS the Optimal Frequency-by-Frequency Estimate [CONJECTURED]

The CZ theorem already encodes the optimal way to sum frequency contributions. LP decomposition merely reveals this structure. The only scenario where LP could help is if the BILINEAR structure gave better estimates than single-function CZ:

- T_{u^below} u^{above}: inherits CZ exponents (smooth x rough = standard estimate)
- T_{u^above} u^{below}: WORSE (rough x smooth requires Bernstein on rough factor)
- R(u^{below}, u^{above}): same-frequency interaction, no improvement possible

## Clarification of E004's Commutator Gain [CONJECTURED]

E004 found that [R_iR_j, u^{below}] u^{above} has better high-frequency behavior. This is true for REGULARITY (H^s with s > 0), not L^p INTEGRABILITY. The De Giorgi method requires L^{10/3} integrability, and converting regularity to integrability via Bernstein/Sobolev costs exactly the improvement gained. Fundamental tension: De Giorgi operates in L^p, frequency-localized improvements live in Sobolev/Besov. The exchange rate is fixed by dimensional analysis.

## Status: LP Route CLOSED

Frequency-localized De Giorgi should be REMOVED from the list of viable approaches (identified as direction 2 in the S2-E004 remaining directions). The obstruction is structural, not technical. Remaining directions after this closure:

1. Nonlinear dissipation lower bounds (use NS equation, not just energy inequality)
2. ~~Frequency-localized De Giorgi~~ **CLOSED by S2-E005**
3. Quantitative unique continuation
4. Topological/geometric constraints

## Verification Scorecard

| Tag | Count |
|-----|-------|
| [COMPUTED] | 8 (LP spectra 2 datasets, bottleneck splits 2 datasets, paraproducts 2 datasets, Bernstein cost, numerical beta_eff) |
| [CONJECTURED] | 4 (analytical exponent chain, CZ optimality interpretation, E004 commutator clarification, implications) |
| [VERIFIED] | 0 |
| [CHECKED] | 0 |

## Cross-References

- [compensated-compactness-commutator-obstruction.md](compensated-compactness-commutator-obstruction.md) -- S2-E004 identified frequency-localized De Giorgi as remaining direction 2; S2-E005 now closes it
- [beta-current-value-four-thirds.md](beta-current-value-four-thirds.md) -- LP route closed; down to 3 remaining directions
- [vorticity-degiorgi-universal-barrier.md](vorticity-degiorgi-universal-barrier.md) -- Fourth evidence for 4/3 universality: LP toolkit also saturates
- [proposition-3-sharpness-audit.md](proposition-3-sharpness-audit.md) -- Confirms direction (b) tested via LP also non-viable; Bernstein exchange rate = dimensional cost of Step 3b Chebyshev
