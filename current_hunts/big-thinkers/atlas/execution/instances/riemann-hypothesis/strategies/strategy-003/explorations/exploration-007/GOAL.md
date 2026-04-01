# Exploration 007: Adversarial Novelty Review — Two Live Claims

## Mission Context

We are 7 explorations into an investigation of the spectral rigidity gap: Δ₃_sat(zeta) = 0.155 vs GUE analytic ≈ 0.294 (47% more rigid). This exploration performs an adversarial/novelty review of the two claims that remain scientifically uncertain. Pre-assessment from prior work has already settled the others (see Pre-Settled Claims section below).

**Your task is a literature search and synthesis — no computation required.** Use WebSearch, WebFetch, and reading to assess novelty and find closest prior work.

---

## Pre-Settled Claims (Do NOT spend time on these — record the verdict and move on)

### Claim 1: Flat Δ₃ saturation plateau (<1% variation L=15-30)
**VERDICT: NOT NOVEL.** Berry (1985, Proc. R. Soc. A 400:229) predicted the saturation and level. Odlyzko (1987, 2001) confirmed numerically at large scale. Our measurement is methodologically clean but adds precision, not novelty. Record this verdict and move on.

### Claim 4: K_primes correct normalization is (log p)²/p^m (not (log p)²)
**VERDICT: WEAK (prior source exists).** This is the standard semiclassical amplitude from Berry (1985). It's a useful technical clarification but Berry is the prior source. Record as "already in Berry (1985)" and move on.

### Claim 5: C1 matrix gives Δ₃=0.285 (intermediate between zeta 0.155 and GUE 0.294)
**VERDICT: RETRACTED.** Flat-amplitude test (S002 work) showed: H_flat gives Δ₃_sat=0.256, C1 gives 0.243, GUE control gives 0.227 — all within ~1σ of each other when using the correct finite-size N=500 GUE baseline. The "intermediate Δ₃" observation was an artifact of using the wrong GUE baseline (infinite-N theory ~0.566 instead of finite-N sim ~0.23). Formally record the retraction and move on.

---

## Live Claim 1 (Your Primary Goal): λ_n^zeta/λ_n^GUE < 1 for n>300

### The Claim

Li's criterion: RH ⟺ λ_n ≥ 0 for all n, where λ_n = Σ_ρ [1-(1-1/ρ)^n].

**We computed:** λ_n^zeta vs λ_n^GUE (mean of 1000 GUE matrix Li coefficients, N=100), and found:
- For n < 300: λ_n^zeta ≈ λ_n^GUE (97.1% correlation overall)
- For n > 300: **λ_n^zeta < λ_n^GUE**, falling to ratio ~0.95 at n=500

Specific values:
| n | λ_n^zeta | λ_n^GUE (mean ± std) |
|---|---------|----------------------|
| 100 | 59.72 | 57.82 ± 0.83 |
| 200 | 288.97 | 279.39 ± 2.13 |
| 300 | (transition) | — |
| 500 | 881.43 | 929.10 ± 2.68 |

Proposed mechanism: super-rigidity (Δ₃_sat=0.155 << GUE 0.294) → more evenly distributed zero phases → more efficient phase cancellation → smaller λ_n at large n relative to GUE.

### Literature Search Task

Search these specific papers for any comparison of zeta λ_n vs GUE or RMT λ_n:

**Must-check:**
1. **Li (1997)** — "The Positivity of a Sequence of Numbers and the Riemann Hypothesis", J. Number Theory 65:325
2. **Keiper (1992)** — "Power series expansions of Riemann's ξ function", Math. Comp. 58:765
3. **Bombieri & Lagarias (1999)** — "Complements to Li's criterion for the Riemann hypothesis", J. Number Theory 77:274
4. **Coffey (2004)** — "Relations and positivity results for the derivatives of the Riemann ξ function", J. Comput. Appl. Math. 166:525 (or similar Coffey papers on Li coefficients)
5. **Schumayer & Hutchinson (2011)** — "Physics of the Riemann Hypothesis", Rev. Mod. Phys. 83:307 — the main review paper; check if it mentions GUE comparison of λ_n

**Also search:** "Li coefficients GUE", "Li criterion random matrix theory", "Keiper-Li coefficients spectral statistics"

**What you're looking for:** Does ANY prior paper:
- Compare λ_n^zeta to λ_n of GUE random matrices?
- Observe the crossover (λ_n^zeta < λ_n^GUE for large n)?
- Connect Li coefficient growth rate to spectral rigidity or Δ₃?

**Verdict options:**
- **NOVEL** (1-5 on novelty scale 5 = entirely new): If no paper compares zeta vs GUE λ_n and identifies the crossover
- **PARTIALLY NOVEL**: If prior work compares λ_n to RMT but misses the crossover direction or mechanism
- **NOT NOVEL**: If prior work already documents λ_n^zeta < λ_n^GUE for large n and links it to spectral statistics

**[SECTION COMPLETE — write this section before starting Live Claim 2]**

---

## Live Claim 2 (Secondary Goal): Berry Formula Growing Discrepancy

### The Claim

Berry (1985) formula: Δ₃_sat = (1/π²) log(log(T/2π))

**We measured** (using 2000 zeta zeros, height-resolved bins):

| T | Berry prediction | Measured Δ₃_sat | Error |
|---|-----------------|-----------------|-------|
| 383 | 0.143 | 0.1435 | 0.2% |
| 600 | 0.154 | ~0.155 | 0.6% |
| 1108 | 0.166 | 0.1545 | 7.8% |
| 1696 | 0.175 | 0.1569 | 11.2% |
| 2245 | 0.180 | 0.1595 | 12.5% |

Pattern: **error grows systematically from 0.2% to 12.5% as T increases from 383 to 2245.**

This is surprising because Berry's formula should be more accurate at larger T (the prime orbit sum is an asymptotic formula for T→∞). Why would accuracy DECREASE with T?

One possible explanation: with N=2000 total zeros, at T≈383 we're using zeros near the bottom of the spectrum (more zeros per unit interval), while at T≈2245 we're using zeros near T=2245 where the dataset is sparse. The "bin 4" measurements (T≈2245) may have fewer zeros and higher measurement noise.

Another: Berry's formula has a known correction term. Search for whether this is discussed.

### Literature Search Task

**Must-check:**
1. **Berry (1985)** — same paper as above, but look for: (a) any correction terms to the formula beyond log(log(T)); (b) any discussion of formula accuracy vs. T; (c) the range of T for which the formula is claimed valid.
2. **Bogomolny & Keating (1996)** — "Gutzwiller's trace formula and spectral statistics: beyond the diagonal approximation", Phys. Rev. Lett. 77:1472 — do they correct or refine Berry's formula?
3. **Odlyzko (1987)** — "On the distribution of spacings between zeros of the zeta function", Math. Comp. 48:273 — does he report Δ₃ at different heights with comparison to Berry's prediction?
4. **Montgomery (1973)** — "The pair correlation of zeros" — does it discuss the height range?

**What you're looking for:**
- Does Berry himself discuss accuracy vs. T?
- Is the growing discrepancy at T>1000 a known feature, explained by correction terms?
- OR: Is it a measurement artifact from having too few zeros in the high-T bins?

**Verdict options:**
- **NOVEL (weak)**: Our quantitative measurement of the growing discrepancy at T=383-2245, if prior work doesn't have this specific table
- **EXPLAINED**: Berry (1985) or BK (1996) already explains why accuracy decreases at this T range
- **ARTIFACT**: The growing discrepancy is known to be due to sparse sampling at high T (statistical noise)

**[SECTION COMPLETE — write this section before starting Synthesis]**

---

## Synthesis (Task 3)

After completing both live claims, write a consolidated novelty verdict table:

| Claim | Verdict | Novelty (1-5) | Strongest Surviving Evidence | Best Counterargument |
|-------|---------|---------------|------------------------------|---------------------|
| Flat Δ₃ plateau | NOT NOVEL | 0 | — | Berry (1985) predicted it |
| λ_n^zeta < λ_n^GUE crossover | ? | ? | Crossover at n≈300, ratio 0.95 at n=500 | May be GUE class property |
| Berry formula accuracy table | ? | ? | Quantitative T-resolved table | May be artifact of sparse bins |
| K_primes normalization | WEAK | 1 | — | Berry (1985) is prior source |
| C1 Δ₃=0.285 intermediate | RETRACTED | 0 | — | Wrong baseline (finite-N GUE) |

Then answer: **What is the strongest single novel claim from this entire strategy?**

If the λ_n ratio claim is novel: describe specifically what would need to be true for it to be a publishable observation (what larger zero dataset or GUE ensemble size would be needed to confirm the 0.95 ratio at n=500 definitively)?

**[SECTION COMPLETE — then write REPORT-SUMMARY.md]**

---

## Success Criteria

**Success:** Clear novelty verdict for both live claims. At least one claim survives with rating ≥ 3 (new observation not previously documented).

**Partial:** Both claims have known prior art but our quantitative precision adds something.

**Failure:** Both live claims have clear prior art documenting exactly what we found. We have no novel claims.

---

## Key Prior Context

- Strategy: Riemann Hypothesis spectral rigidity (Atlas mission)
- Budget: This is exploration 7 of 10; 3 remain after this
- E002 source: λ_n computed from 2000 zeta zeros + GUE ensemble N=100, 1000 matrices
- E003 source: Δ₃_sat=0.1545 confirmed directly; 2000 zeros, sliding window
- E006 source: Berry formula 0.154 at T=600, 0.167 at T=1127

## Output Required

Write REPORT.md incrementally — write [SECTION COMPLETE] after each section.
Final section: REPORT-SUMMARY.md (200-300 words): novelty scorecard, strongest surviving claim, best evidence for it.
