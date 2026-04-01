---
topic: Strategy 002 final novelty verdicts — five claims assessed against prior literature
confidence: verified
date: 2026-03-27
source: "riemann-hypothesis strategy-002 exploration-008 (literature search and synthesis)"
---

## Overview

After 2 strategies and 18 explorations (S001-E001 through S002-E007 + E008 synthesis + E009 flat-amplitude test), this entry records the final novelty verdicts for all major findings from Strategy 002. *Updated by E009: C1 rigidity claim downgraded from WEAK to NOT NOVEL.* Literature searches were conducted by the strategizer directly (standard explorers consistently failed to complete the literature-search + synthesis task in a single exploration; see curator log for S002-E008 meta-notes).

---

## Final Novelty Verdict Table

| Claim | Our Finding | Literature Status | Verdict |
|---|---|---|---|
| **N²/p ≈ 250–310 scaling (Gauss sum matrices, N=500)** | β peaks at N²/p≈309; collapses to Poisson for large p; β < 1.2 always; **S003-E004: multi-N universality REJECTED (peak varies 200–309); β_max decreases with N; weaker claim N²/p≈290–310 for N≥500 via Brody MLE partially supported** | Not documented; band matrix analogue exists (Fyodorov-Mirlin 1991 W²/N~1) but different class | **SUPPORTED (N=500 observation); UNIVERSAL claim REJECTED** |
| **Dirichlet character impossibility (both routes GOE)** | Algebraic proof: multiplicative route → real symmetric; factorizable route → D A D† | Not documented for this construction; follows from Dyson (1962) threefold way; not stated for Dirichlet character matrices | **SUPPORTED** |
| **C1 anomalous intermediate rigidity (Δ₃=0.285)** | ~~Between GUE=0.565 and zeta=0.156; Von Mangoldt Hankel-specific~~ **RETRACTED (E009): Δ₃_sat = 0.243 is generic finite-size GUE; H_flat indistinguishable at 1σ; Von Mangoldt amplitude irrelevant** | Not documented; MOOT | **NOT NOVEL (E009 retraction)** |
| **Berry saturation confirmed height-resolved** | 7.6% accuracy, strictly monotone with T (Δ₃_sat = 0.1435→0.1595) | Berry (1985) predicted; Odlyzko confirmed numerically | **NOT NOVEL** |
| **Prime form factor normalization resolved (14.5% MAD)** | K_primes = Berry diagonal approx; cosine ≠ K(τ); correct normalization K_primes = K_density/(2πρ̄)² | Berry (1985) is prior source; normalization subtlety not explicitly stated | **WEAK** |

---

## Detail: SUPPORTED Claims

### Claim 1 — Gauss Sum N²/p Scaling

**Specific result:** For the N×N Hermitian Gauss sum matrix H_{jk} = Λ(|j-k|+1) × exp(2πijk/p), level repulsion exponent β peaks at p ≈ N²/275. For N=500: peak at p=809 with β=1.154, N²/p=309. For p >> N²/250, β collapses to near-Poisson (β=0.086 at p=99991). ALL constructions satisfy β < 1.2 permanently.

**Why novel:** No prior paper studies this matrix class for level statistics. The Zadoff-Chu / chirp matrix literature is entirely in telecommunications (OFDM, LTE) with no crossover to RMT. The Fyodorov-Mirlin band matrix transition (W²/N ~ 1) is structurally analogous but involves random matrices, a different constant (~1 vs. 250–310), and has no β-cap.

**Defensible version:** "Empirically observed for N=500." **S003-E004 UPDATE: Multi-N universality tested at N=250, 500, 1000 — REJECTED.** Peak N²/p_opt varies from 200 to 309; peak β_max decreases with N (1.318 → 1.154 → 1.019). The "universal constant" claim is not supported. The N=500 observation itself remains SUPPORTED (not in prior literature), but cannot be extended to other N values. See `n2p-scaling-universality-rejected.md`.

### Claim 2 — Dirichlet Character Impossibility

**Specific result:** Any Hermitian H_{jk} = A_{jk} × f(χ(j+1), χ(k+1)) for a completely multiplicative Dirichlet character χ and real amplitude A is either (a) unitarily equivalent to a real symmetric matrix, or (b) real symmetric itself. Both routes yield GOE (β ≤ 0.28 empirically for χ₅ and χ₁₃; GOE proved algebraically).

**Why novel:** The specific proof for the Dirichlet character construction is not stated in prior literature. Consistent with Dyson's threefold way + Katz-Sarnak, but the explicit application to this construction fills a gap for practitioners designing Hilbert-Pólya Hamiltonians. Schumayer-Hutchinson (Rev. Mod. Phys. 83, 307, 2011) does not discuss this.

**Scope limit:** Only covers multiplicative character phases. Non-multiplicative arithmetic phases (Jacobi sums, Ramanujan τ, non-factorizable sums of characters) are not ruled out.

---

## Detail: Non-Novel and Weak Claims

### Berry Saturation (NOT NOVEL)
Δ₃_sat = (1/π²)log(log(T/2π)) was predicted by Berry (1985, Proc. R. Soc. A 400:229). The quantitative confirmation to 7.6% accuracy and the height-resolved monotone behavior (Δ₃_sat strictly increasing with T) are good numerical work but do not add to Berry's theoretical prediction. Odlyzko's large-scale computations already confirmed the qualitative saturation.

### C1 Anomalous Rigidity (NOT NOVEL — E009 Retraction)

**RETRACTED by S002-E009.** The flat-amplitude test proved that Δ₃_sat = 0.243 is generic finite-size GUE behavior at N=500. H_flat (flat amplitude, no arithmetic structure) gives Δ₃_sat = 0.256 — indistinguishable from C1 at 1σ. GUE control gives 0.227. All three are consistent within noise.

The prior "50% of GUE" framing compared Δ₃_sat against the infinite-N GUE theory value (~0.566), which is the wrong baseline at N=500. The correct finite-size GUE baseline is ~0.22–0.26. Against that baseline, C1 is unremarkable.

**The Von Mangoldt amplitude plays no role in spectral rigidity at N=500.** This claim is downgraded from WEAK to NOT NOVEL — it is not even weakly supported.

### Prime Form Factor Normalization (WEAK)
The resolution of the normalization ambiguity (K_primes = K_density/(2πρ̄)², not (2πρ̄)²×K_density as one might naively write) is a correct technical clarification. It is consistent with Berry (1985) and does not constitute a novel result. It would be appropriate as a footnote in a paper citing Berry.

---

## Central Open Problem After Strategy 002

**Two strategies, 18 explorations, zero constructions have achieved Δ₃_sat ≈ 0.156 (the zeta zeros' 3× super-rigidity vs. GUE).** All N=500 ensembles — including C1, H_flat, and GUE control — give Δ₃_sat in the range 0.23–0.26. The gap to zeta zeros (~40%) is a finite-size GUE property that no construction has bridged.

The key insight from E009: the gap is NOT an arithmetic-structure problem. Generic GUE matrices (flat amplitude) perform identically to Von Mangoldt matrices. The zeta zeros are genuinely more rigid than any N=500 GUE-class matrix; the explanation requires going beyond random matrix universality.

**Strategy 003 priority questions** (updated after E009):
1. ~~Does flat-amplitude random phase give the same Δ₃ = 0.285?~~ **ANSWERED (E009): YES — H_flat ≈ C1 ≈ GUE within noise. Von Mangoldt amplitude irrelevant.**
2. ~~Does the N²/p ≈ 275 constant generalize?~~ **ANSWERED (S003-E004): NO — peak N²/p varies from 200 to 309 across N=250, 500, 1000; β_max decreases with N. Universal scaling REJECTED.**
3. Can a prime-indexed construction H_{p_j, p_k} = f(p_j × p_k) achieve GUE class with Δ₃ < 0.2? (Most ambitious; most directly targets the Hilbert-Pólya program — still open)
