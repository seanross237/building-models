# Strategy 002 — Final Report

**Mission:** Riemann Hypothesis Operator Construction
**Strategy:** Operator Construction Tournament — build new operators and test them against the 10-constraint catalog from S001
**Explorations completed:** 9 (E001–E009; E010 skipped — budget sufficiently used)
**Date:** 2026-03-27

---

## Executive Summary

Strategy 002 ran a systematic operator construction tournament. Starting from the S001 finding that all known operators score 0/10, S002 built 7 novel Hermitian matrix constructions, subjected the best candidate to adversarial review, and conducted a final novelty literature search.

**Key outcome:** No construction achieved zeta-like long-range rigidity (Δ₃_sat ≈ 0.155). The best construction (C1, random complex phases on Von Mangoldt Hankel amplitude) is simply a GUE-class matrix — its spectral statistics are entirely explained by random phase structure with no arithmetic content. Two novel claims survive adversarial review: a quantitative N²/p scaling law for Gauss sum matrices and an algebraic impossibility proof for Dirichlet character Hamiltonians.

---

## What Was Tried: 9 Explorations in 3 Phases

### Phase 1: Construction Tournament (E001–E003)

**E001 (succeeded):** Seven complex Hermitian arithmetic matrix constructions tested at N=500:
- C1 (random phases + Von Mangoldt Hankel): β=1.675, KS_GUE PASS — best result
- C3b (Gauss sum phases, p=997): β=1.092, GOE-class
- All real symmetric constructions: β ≤ 1 (capped — mathematical fact)
- Key insight: phase non-factorizability (φ(j,k) ≠ g(j) ± g(k)) is required for β > 1

**E002 (inconclusive):** Gradient-based optimization of operator matrix — histogram loss is non-differentiable; gradient methods fail entirely.

**E003 (inconclusive):** Two-point pair correlation from prime sums — normalization issues; prime form factor computation failed.

### Phase 2: Deep Dives (E004–E006)

**E004 (succeeded):** Berry saturation formula Δ₃_sat = (1/π²)log(log(T/2π)) confirmed with 7.6% accuracy across height-resolved bins of 2000 Riemann zeros. Zeta zeros show 3× super-rigidity vs. GUE (Δ₃=0.155 vs 0.565 theory).

**E005 (succeeded):** C1 re-scored with corrected formulas. C1 pair correlation MRD=7.9% (PASS). Gauss sum phase sweep: β peaks at N²/p≈309 (p=809, β=1.154) then collapses to Poisson for large p. β NEVER reaches GUE — permanently GOE.

**E006 (succeeded):** Two-point spectral form factor K(τ): K_primes matches K_GUE ramp with 14.5% MAD (Berry's diagonal approximation confirmed). Dirichlet character constructions: algebraically proved impossible for GUE — both construction routes (multiplicative Hermitianized + factorizable) collapse to real symmetric matrices.

### Phase 3: Adversarial Review + Synthesis (E007–E009)

**E007 (succeeded):** Three serious attacks on C1 pair correlation:
1. Flat-amplitude random phase achieves MRD=6.8% (< C1's 7.9%) → Von Mangoldt unnecessary
2. Per-realization MRD = 15.5% mean (0/20 realizations pass 10% threshold) → 7.9% was averaging artifact
3. GOE-class Toeplitz matrix achieves MRD=9.0% → test not discriminating at N=500
Pair correlation PASS downgraded from "Von Mangoldt confirmed" to "GUE class membership confirmed."

**E008 (succeeded):** Literature synthesis + novelty search. Found no prior work on either Gauss sum matrix level statistics or Dirichlet character Hamiltonian classification. Both claims assessed as SUPPORTED.

**E009 (succeeded — completed manually after explorer death):** Flat-amplitude Δ₃ comparison:
- H_flat: Δ₃_sat = 0.256 ± 0.010
- C1: Δ₃_sat = 0.243 ± 0.017
- GUE control: Δ₃_sat = 0.227 ± 0.010
- GUE theory (infinite N): 0.242
All three agree within noise. Von Mangoldt amplitude does NOT affect Δ₃. C1 "anomalous intermediate rigidity" claim retracted.

---

## Final Scorecard

| Construction | β (Brody) | Δ₃_sat | Pair corr. | GUE class? |
|---|---|---|---|---|
| C1 (Von Mangoldt + random phases) | 1.675 | 0.243 | PASS (averaging) | YES (random phases only) |
| C3b (Gauss sum, p=997) | 1.092 | — | — | NO (GOE) |
| Gauss sum (p=809, optimal) | 1.154 | — | — | NO (GOE cap) |
| Dirichlet character (any) | 0.28 | — | — | PROVED IMPOSSIBLE |
| Riemann zeta zeros (target) | ~2 | **0.155** | — | GUE |

No construction achieves Δ₃_sat < 0.2. The best value is 0.243 (C1), which is ~57% higher than zeta zeros (0.155).

---

## Novel Claims

### Claim A: Gauss Sum Hamiltonians Have a Quantitative N²/p Scaling for Level Statistics

**Claim:** For H_{jk} = Λ(|j-k|+1) × exp(2πijk/p), the level repulsion exponent β peaks at p ≈ N²/275 (for N=500: peak at p=809, β=1.154, N²/p=309). For p >> N²/250, β collapses to Poisson (β=0.086 at p=99991). All Gauss sum constructions satisfy β < 1.2 — permanently GOE class, never GUE.

**Evidence:** 27 values of p from p=97 to p=99991 at N=500; fine sweep of 21 primes (p=503 to p=5003). β peak at p=809. [COMPUTED, S002-E005]

**Novelty search:** No prior paper found on Gauss sum / chirp matrix level statistics. Closest analogue is Fyodorov-Mirlin band matrix transition (W²/N~1) — different matrix class, different constant (~275 vs ~1), different cap behavior (our matrices β-capped at 1.2; band matrices can reach full GOE). [SEARCHED, S002-E008]

**Status: SUPPORTED** — new specific quantitative result.

**Strongest counterargument:** Only N=500 tested. The constant 275 may be N-dependent. "Universal" claim requires multi-N verification (planned for S003 Computations-For-Later item 12).

---

### Claim B: Dirichlet Character Hamiltonians Are Algebraically Confined to GOE

**Claim:** Any Hermitian matrix H_{jk} = A_{jk} × f(χ(j+1), χ(k+1)) for a completely multiplicative Dirichlet character χ and real amplitude A is either (a) real symmetric after Hermitianizing, or (b) unitarily equivalent to a real symmetric matrix. Both routes yield GOE statistics. No Dirichlet character construction can achieve GUE.

**Evidence:**
- Route 1: H_{jk} = Λ × χ(j)χ(k) is not Hermitian. After (H+H†)/2 Hermitianizing: Λ × Re(χ(j)χ(k)) = real symmetric → GOE. [PROVED algebraically + COMPUTED: β_mul13=0.281, β_mul5=−0.514, S002-E006]
- Route 2: H_{jk} = Λ × χ(j)χ*(k) = Λ_{|j-k|} exp(i(g_j−g_k)) = D A D† where D=diag(exp(ig_j)), A=real Hankel → unitarily equivalent to real → GOE. [PROVED algebraically + COMPUTED: β_fact13=0.218, S002-E006]

**Novelty search:** Not explicitly documented as theorem. Consistent with Dyson's threefold way (D A D† ~ real) + Katz-Sarnak (quadratic L-functions → orthogonal symmetry). Schumayer-Hutchinson review (Rev. Mod. Phys. 83, 307, 2011) does not discuss character-based Hamiltonians. [SEARCHED, S002-E008]

**Status: SUPPORTED** — proof is new in this specific context. Expert would regard as "expected from general principles," but explicitly closes a gap for practitioners designing Hilbert-Pólya Hamiltonians with character entries.

**Strongest counterargument:** Only covers completely multiplicative characters. Non-multiplicative arithmetic phases (Jacobi sums, Ramanujan τ, non-factorizable sums of characters) are not covered. The result does not rule out GUE from all arithmetic constructions.

---

### Withdrawn Claims

**C1 anomalous intermediate Δ₃:** RETRACTED (E009). C1's Δ₃_sat=0.243 is generic GUE finite-size behavior at N=500, not caused by Von Mangoldt arithmetic.

**C1 pair correlation:** DOWNGRADED (E007). The PASS (MRD=7.9%) is a property of GUE class membership, not Von Mangoldt arithmetic. Von Mangoldt amplitude is unnecessary.

---

## What Strategy 003 Should Focus On

### The Central Unsolved Problem

**The zeta zeros' super-rigidity gap:** Δ₃_sat(zeta) = 0.155 vs. any GUE-class matrix at N=500 = 0.243. This ~57% gap (factor ~1.6×) is large, consistent across all constructions, and not a finite-size artifact (zeta zeros show it at large T, Berry E004).

The core problem: GUE statistics arise easily (any random-phase matrix at N=500 gives β≈1.5, pair correlation PASS), but the zeta zeros' anomalously *low* Δ₃ — their super-rigidity — is not reproducible by any construction. The gap is worse for Δ₃ than for β.

### Recommendations for S003

**Priority 1: Investigate what causes zeta zero super-rigidity.** The answer is almost certainly in the non-diagonal periodic orbit corrections to the pair correlation — the "off-diagonal" terms in the Bogomolny-Keating-Snaith framework that GUE matrices lack. S003 should focus on constructing matrices where the off-diagonal form factor contributions are explicitly built in.

**Priority 2: Test non-arithmetic phases with structure.** All arithmetic phases tested (Gauss sum, Dirichlet character) give GOE. Random phases give GUE. The question is whether *structured* non-arithmetic phases (e.g., algebraic numbers, quasiperiodic, or fractal phases) can produce super-rigidity. This is unexplored territory.

**Priority 3: N-scaling of N²/p (Computations-For-Later item 12).** Test N=250, N=1000 to determine whether N²/p≈275 is a genuine universal constant or N-dependent. Low-cost confirmation or revision of Claim A.

**Priority 4: Investigate Connes' spectral triple approach.** The only framework that explicitly targets GUE + super-rigidity is the Connes-Marcolli noncommutative geometry approach. S001 found this was computationally inaccessible; S003 could attempt a more targeted literature extraction of its spectral predictions.

### What S003 Should NOT Repeat

- Random-phase explorations: GUE class is easy; the problem is long-range rigidity
- Gradient optimization: non-differentiable losses, dead end
- Dirichlet character variations: proved impossible, no path forward
- Gauss sum variations: β-capped at 1.2, no path to GUE

---

## Reflections on Methodology

The Operator Construction Tournament worked well for clearing the space of obvious arithmetic constructions. Phase 3 adversarial review was essential — without E007 and E009, we would have reported C1 as a novel finding when it was generic GUE behavior.

**Explorer completion rate was poor:** 4 of 9 explorations required manual report completion (E006, E007, E008, E009). The consistent failure mode: explorer computes results, enters extended thinking loop, writes skeleton with placeholders, never fills them. This is the single biggest operational problem for this mission.

**Budgeting:** Phase 3 used 3 explorations (E007 adversarial, E008 synthesis, E009 validation). This was the right allocation — adversarial review caught two important errors before the final report.
